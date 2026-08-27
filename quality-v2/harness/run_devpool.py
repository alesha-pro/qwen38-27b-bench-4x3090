#!/usr/bin/env python3
"""Run the dev pool against the BF16 reference on OpenRouter/AkashML.

Resume-safe: one JSON per (task, effort, repeat) in
runs/<name>/<effort>/r<N>/<task_id>.json — existing OK files are skipped.

Contract notes:
- RG tasks get a fixed answer-tag suffix (same for every model, now and when
  quants run) so extraction never depends on free-form formatting.
- BFCL tools are converted to OpenAI tool schema with BFCL's type mapping.
- effort transport: raw passthrough (smoke 2026-08-22: reasoning.effort of
  OpenRouter does NOT map to Qwen's xhigh; raw reasoning_effort does).
"""
import argparse
import json
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import or_client  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

RG_SUFFIX = ("\n\nWhen you are done, put your final answer between "
             "<answer> and </answer> tags.")

BFCL_TYPE_MAP = {"dict": "object", "float": "number", "tuple": "array",
                 "any": "string", "byte": "integer", "short": "integer",
                 "long": "integer", "double": "number", "char": "string",
                 "list": "array", "integer": "integer", "boolean": "boolean",
                 "string": "string", "array": "array", "object": "object",
                 "number": "number"}


def map_types(node):
    if isinstance(node, dict):
        out = {}
        for k, v in node.items():
            if k == "type" and isinstance(v, str):
                out[k] = BFCL_TYPE_MAP.get(v, v)
            else:
                out[k] = map_types(v)
        return out
    if isinstance(node, list):
        return [map_types(x) for x in node]
    return node


def to_openai_tools(funcs):
    tools = []
    for f in funcs or []:
        tools.append({"type": "function", "function": {
            "name": f["name"],
            "description": f.get("description", ""),
            "parameters": map_types(f.get("parameters",
                                          {"type": "object",
                                           "properties": {}})),
        }})
    return tools


def build_request(task):
    if task["block"] == "tool-calling":
        msgs = task["messages"][0]  # first (only) turn of single-turn cats
        tools = to_openai_tools(task.get("tools_raw"))
        return msgs, tools
    prompt = task["prompt"]
    if task["block"] == "quant-core-rg":
        prompt += RG_SUFFIX
    return [{"role": "user", "content": prompt}], None


_lock = threading.Lock()
_done = 0
_cost = 0.0


def run_one(task, effort, rep, outdir, total):
    global _done, _cost
    out = outdir / f"{task['id']}.json"
    if out.exists():
        try:
            prev = json.loads(out.read_text())
            if prev.get("error") is None:
                with _lock:
                    _done += 1
                return "skip"
        except Exception:
            pass
    msgs, tools = build_request(task)
    # Explicit endpoint ceiling: without it AkashML cuts at 65536 and the
    # "no artificial truncation" contract silently breaks (seen 2026-08-22:
    # 29/750 calibration calls hit finish_reason=length at exactly 65536).
    res = or_client.chat(msgs, effort, effort_mode="raw", tools=tools,
                         max_tokens=131072)
    rec = {"task_id": task["id"], "block": task["block"], "effort": effort,
           "repeat": rep, **res}
    tmp = out.with_suffix(".tmp")
    tmp.write_text(json.dumps(rec, ensure_ascii=False))
    tmp.rename(out)
    s = or_client.usage_summary(res)
    with _lock:
        _done += 1
        _cost += s.get("cost_usd") or 0
        print(f"[{_done}/{total}] {task['id']} {effort} r{rep} "
              f"rt={s.get('reasoning_tokens')} ct={s.get('completion_tokens')} "
              f"${_cost:.2f} {('ERR ' + str(res['error'])[:80]) if res['error'] else ''}",
              flush=True)
    return "err" if res["error"] else "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-name", required=True)
    ap.add_argument("--efforts", nargs="+", default=["xhigh"],
                    choices=["off", "low", "medium", "xhigh"])
    ap.add_argument("--repeats", type=int, default=1)
    ap.add_argument("--concurrency", type=int, default=8)
    ap.add_argument("--blocks", nargs="+", default=None)
    ap.add_argument("--limit", type=int, default=None,
                    help="first N tasks only (smoke)")
    ap.add_argument("--pool", default="dev-pool/devpool.jsonl",
                    help="task pool file, relative to the project root")
    a = ap.parse_args()

    pool = [json.loads(l) for l in (ROOT / a.pool).open()]
    if a.blocks:
        pool = [t for t in pool if t["block"] in a.blocks]
    if a.limit:
        pool = pool[:a.limit]

    jobs = []
    for eff in a.efforts:
        for rep in range(1, a.repeats + 1):
            outdir = ROOT / "runs" / a.run_name / eff / f"r{rep}"
            outdir.mkdir(parents=True, exist_ok=True)
            for t in pool:
                jobs.append((t, eff, rep, outdir))
    total = len(jobs)
    print(f"{len(pool)} tasks x {a.efforts} x {a.repeats} = {total} calls, "
          f"concurrency {a.concurrency}", flush=True)
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=a.concurrency) as ex:
        stats = list(ex.map(lambda j: run_one(*j, total), jobs))
    print(f"done in {(time.time()-t0)/60:.1f} min: "
          f"ok={stats.count('ok')} skip={stats.count('skip')} "
          f"err={stats.count('err')} cost=${_cost:.2f}")


if __name__ == "__main__":
    main()
