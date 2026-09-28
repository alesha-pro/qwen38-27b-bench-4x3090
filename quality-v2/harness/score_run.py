#!/usr/bin/env python3
"""Score a collected run of the dev pool.

Verifiers:
  quant-core-rg    reasoning_gym's own score_answer (dataset rebuilt from the
                   same seed); answer extracted from <answer></answer> tags,
                   fallback: text after last 'answer'-marker, then last line.
                   pass = score >= 1.0
  quant-core-math  last \\boxed{...} vs expected, normalized exact match
  quant-core-if    IFBench official strict evaluator (evaluation_lib)
  tool-calling     BFCL ground-truth matcher (function name + every required
                   param value in the allowed list; irrelevance passes iff no
                   tool call).
                   Validated 2026-08-23 against BFCL's own ast_checker over
                   135 scored calls: 134 agree, 1 differs (harness/validate_
                   bfcl.py). In that case the model sent 1 of 5 requested
                   parameters; the official checker recurses into nested dicts
                   key-by-key and passes it, ours compares the whole structure
                   and fails it. We keep the stricter rule on purpose: dropping
                   arguments is exactly the degradation this benchmark hunts.

Usage: score_run.py --run-name calib-xhigh [--efforts xhigh] [--repeats 1 2 3]
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IFBENCH_REPO = "$DATA_ROOT/datasets/local-quant-bench-v2/repos/ifbench"


# ---------- answer extraction ----------

def response_text(rec):
    try:
        msg = rec["response"]["choices"][0]["message"]
    except (KeyError, TypeError, IndexError):
        return "", None
    # Отступ в начале content это след движка, а не выбор модели: vLLM и API
    # оставляют перенос строки после </think>, llama.cpp его срезает. На блоке if
    # есть требования вида «в выводе не должно быть пробельных символов», и без
    # нормализации мы сравнивали бы движки, а не модели.
    return (msg.get("content") or "").strip(), msg


def extract_tagged(text):
    m = re.findall(r"<answer>(.*?)</answer>", text, flags=re.S | re.I)
    return m[-1].strip() if m else None


def extract_boxed(text):
    # last \boxed{...} with brace balancing
    starts = [m.end() for m in re.finditer(r"\\boxed\{", text)]
    if not starts:
        return None
    s = starts[-1]
    depth, i = 1, s
    while i < len(text) and depth:
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
        i += 1
    return text[s:i - 1].strip() if not depth else None


# ---------- scorers ----------

class RGScorer:
    def __init__(self):
        import reasoning_gym
        self.rg = reasoning_gym
        self.ds = {}

    def dataset(self, family, gen_config):
        # Must rebuild with the SAME generator config the task was made with,
        # otherwise tuned (v2) tasks get scored by a default-config dataset.
        key = (family, json.dumps(gen_config, sort_keys=True, default=str))
        if key not in self.ds:
            self.ds[key] = self.rg.create_dataset(
                family, size=12, seed=20260822, **(gen_config or {}))
        return self.ds[key]

    def score(self, task, rec):
        text, _ = response_text(rec)
        if not text:
            return 0.0, "empty"
        src = task.get("source", {})
        # probe pools label the family as "<family>::<level>"; the real
        # generator name lives in source.rg_family
        ds = self.dataset(src.get("rg_family") or task["family"],
                          src.get("gen_config"))
        entry = dict(task["answer_meta"]["entry"])
        entry["question"] = task["prompt"]
        cands = []
        tagged = extract_tagged(text)
        if tagged is not None:
            cands.append(tagged)
        lines = [l.strip() for l in text.strip().splitlines() if l.strip()]
        if lines:
            cands.append(lines[-1])
        cands.append(text.strip())
        best = 0.0
        for c in cands:
            try:
                best = max(best, float(ds.score_answer(answer=c, entry=entry)))
            except Exception:
                pass
            if best >= 1.0:
                break
        return best, "tagged" if tagged is not None else "fallback"


def norm_math(s):
    s = s.strip().replace(" ", "").replace("\\,", "").replace("{,}", "")
    s = re.sub(r"^\\d?frac\{(.+?)\}\{(.+?)\}$", r"\1/\2", s)
    s = s.lstrip("0") or "0" if s.isdigit() else s
    return s


def score_math(task, rec):
    text, _ = response_text(rec)
    got = extract_boxed(text)
    if got is None:
        return 0.0, "no_boxed"
    ok = norm_math(got) == norm_math(str(task["answer_meta"]["answer"]))
    return (1.0 if ok else 0.0), got[:40]


class IFScorer:
    def __init__(self):
        sys.path.insert(0, IFBENCH_REPO)
        import evaluation_lib
        self.lib = evaluation_lib

    def score(self, task, rec):
        text, _ = response_text(rec)
        if not text:
            return 0.0, "empty"
        am = task["answer_meta"]
        inp = self.lib.InputExample(
            key=0, instruction_id_list=am["instruction_id_list"],
            prompt=task["prompt"],
            kwargs=[{k: v for k, v in (kw or {}).items() if v is not None}
                    for kw in am["kwargs"]])
        try:
            out = self.lib.test_instruction_following_strict(
                inp, {task["prompt"]: text})
            return (1.0 if out.follow_all_instructions else 0.0), \
                "".join("1" if x else "0" for x in out.follow_instruction_list)
        except Exception as e:
            return 0.0, f"eval_error:{type(e).__name__}"


def loose_eq(got, allowed):
    """BFCL: param value matches if it equals any allowed variant."""
    def norm(x):
        if isinstance(x, str):
            return x.strip().strip("'\"").lower()
        if isinstance(x, bool):
            return str(x).lower()
        if isinstance(x, (int, float)):
            return str(float(x)).rstrip("0").rstrip(".")
        return json.dumps(x, sort_keys=True)
    return any(norm(got) == norm(a) for a in allowed)


def score_bfcl(task, rec):
    text, msg = response_text(rec)
    calls = (msg or {}).get("tool_calls") or []
    gt = task["answer_meta"]["ground_truth"]
    if task["answer_meta"]["category"] == "irrelevance":
        return (1.0 if not calls else 0.0), f"{len(calls)} calls"
    if gt is None:
        return 0.0, "no_ground_truth"
    if len(calls) != len(gt):
        return 0.0, f"want {len(gt)} calls, got {len(calls)}"
    remaining = list(gt)
    for c in calls:
        fn = c.get("function", {})
        name = fn.get("name", "")
        try:
            args = json.loads(fn.get("arguments") or "{}")
        except json.JSONDecodeError:
            return 0.0, "bad_json_args"
        hit = None
        for g in remaining:
            gname, gparams = next(iter(g.items()))
            if gname.replace(".", "_") != name.replace(".", "_"):
                continue
            ok = True
            for p, allowed in gparams.items():
                required = "" not in allowed
                if p in args:
                    if not loose_eq(args[p], allowed):
                        ok = False
                        break
                elif required:
                    ok = False
                    break
            if ok and all(k in gparams for k in args):
                hit = g
                break
        if hit is None:
            return 0.0, f"unmatched call {name}"
        remaining.remove(hit)
    return 1.0, "match"


# ---------- main ----------

def wilson(p, n, z=1.96):
    if n == 0:
        return (0, 0)
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / den
    return (max(0, c - h), min(1, c + h))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-name", required=True)
    ap.add_argument("--efforts", nargs="+", default=None)
    ap.add_argument("--pool", default="dev-pool/devpool.jsonl")
    a = ap.parse_args()

    pool = {t["id"]: t for t in
            (json.loads(l) for l in (ROOT / a.pool).open())}
    rundir = ROOT / "runs" / a.run_name
    rg, ifs = RGScorer(), IFScorer()

    rows = []
    for eff_dir in sorted(rundir.iterdir()):
        if not eff_dir.is_dir():
            continue
        if a.efforts and eff_dir.name not in a.efforts:
            continue
        for rep_dir in sorted(eff_dir.iterdir()):
            for f in sorted(rep_dir.glob("*.json")):
                rec = json.loads(f.read_text())
                task = pool.get(rec["task_id"])
                if task is None or rec.get("error"):
                    why = rec.get("error") or "task not in the given pool"
                    rows.append({"task_id": rec.get("task_id"),
                                 "effort": eff_dir.name, "rep": rep_dir.name,
                                 "block": rec.get("block"), "score": None,
                                 "detail": str(why)[:120]})
                    continue
                blk = task["block"]
                if blk == "quant-core-rg":
                    s, d = rg.score(task, rec)
                elif blk == "quant-core-math":
                    s, d = score_math(task, rec)
                elif blk == "quant-core-if":
                    s, d = ifs.score(task, rec)
                else:
                    s, d = score_bfcl(task, rec)
                u = (rec.get("response") or {}).get("usage") or {}
                rows.append({"task_id": rec["task_id"], "effort": eff_dir.name,
                             "rep": rep_dir.name, "block": blk,
                             "family": task.get("family"),
                             "score": s, "pass": s >= 1.0,
                             "detail": str(d)[:120],
                             "completion_tokens": u.get("completion_tokens"),
                             "cost": u.get("cost")})
    out = rundir / "scored.jsonl"
    with out.open("w") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    # summary
    print(f"{'effort':8} {'rep':4} {'block':16} {'pass':>9} {'rate':>6} "
          f"{'95% CI':>15}")
    agg = {}
    for r in rows:
        if r["score"] is None:
            continue
        k = (r["effort"], r["rep"], r["block"])
        agg.setdefault(k, []).append(r["pass"])
    for k in sorted(agg):
        v = agg[k]
        p = sum(v) / len(v)
        lo, hi = wilson(p, len(v))
        print(f"{k[0]:8} {k[1]:4} {k[2]:16} {sum(v):4}/{len(v):<4} "
              f"{p:6.3f} [{lo:.3f},{hi:.3f}]")
    errs = [r for r in rows if r["score"] is None]
    if errs:
        print(f"\nUNSCORED (errors): {len(errs)}")
        for r in errs[:10]:
            print(" ", r["task_id"], r["detail"])
    print(f"\nsaved: {out}")


if __name__ == "__main__":
    main()
