#!/usr/bin/env python3
"""agentic-v1 / AppWorld test_normal (168 tasks, 1 pass, xhigh) for BF16 / Mirai S / Bonsai 2.

Same agent (simplified ReAct code agent, max 50 steps) and the same forcing telemetry proxy as the
BenchLocal runs: temperature 1.0, top_p 0.95, top_k 20, min_p 0.05, presence 0, repetition 1.0,
max_tokens 131072, reasoning_effort xhigh on every call. The task list is split into N shards with
AppWorld's own balanced chunking (--num-processes N --process-index i); shard i talks to proxy i % P.
Evaluation runs once at the end over the whole experiment.
"""
from __future__ import annotations
import argparse, json, os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from run_agentic import FORCE, OR_PIN, PALMER, palmer_force, PROXY, ROOT, log, port_free, servers, start, stop, wait_http  # noqa: E402

AW = Path("$ENGINE_ROOT/appworld")
PY = str(AW / "venv/bin/python")
CLI = str(AW / "venv/bin/appworld")
FORCE_AW = dict(FORCE, reasoning_effort="xhigh", chat_template_kwargs={"reasoning_effort": "xhigh"})
SMOKE_IDS = ["3d9a636_1", "2d9f728_1"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", required=True, choices=["bf16", "mirai", "bonsai", *PALMER])
    ap.add_argument("--shards", type=int, default=8)
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--reuse-target", nargs="*", default=None,
                    help="already running model server base urls (no /v1); skips starting servers")
    a = ap.parse_args()
    tag = f"agentic-v1-{a.arm}" + ("-smoke" if a.smoke else "")
    adir = ROOT / "runs" / (f"appworld-{a.arm}" + ("-smoke" if a.smoke else ""))
    adir.mkdir(parents=True, exist_ok=True)
    srv, proxies = [], []
    try:
        if a.reuse_target:
            srv = [(t, None) for t in a.reuse_target]
        else:
            srv = servers(a.arm, adir)
        force = palmer_force(a.arm) if a.arm in PALMER else dict(FORCE_AW, **(OR_PIN if a.arm == "bf16" else {}))
        endpoints = []
        for i, (target, proc) in enumerate(srv):
            if target.startswith("http://127.0.0.1"):
                wait_http(target + "/v1/models", proc)
                log("server ready", target)
            port = ({"bf16": 19520, "mirai": 19510, "bonsai": 19512}.get(a.arm) or PALMER[a.arm]["aw_proxy"]) + i
            pargs = [sys.executable, PROXY, "--host", "0.0.0.0", "--port", str(port), "--target", target,
                     "--log", str(adir / f"telemetry-{i}.jsonl"), "--force-json", json.dumps(force)]
            if a.arm == "bf16":
                pargs += ["--auth-file", "$HOME_DIR/.config/openrouter/key"]
            port_free(port)
            proxies.append(start(pargs, adir / f"proxy-{i}.log"))
            endpoints.append(f"http://127.0.0.1:{port}/v1")
        time.sleep(3)
        if any(p.poll() is not None for p in proxies):
            raise RuntimeError("telemetry proxy died at start")

        # one experiment config; base_url overridden per shard
        exp = subprocess.run([PY, str(AW / "tools/make_local_config.py"), "--tag", tag, "--model-id", "bench",
                              "--base-url", endpoints[0], "--dataset", "test_normal", "--max-steps", "50"],
                             capture_output=True, text=True, check=True).stdout.strip()
        (adir / "campaign.json").write_text(json.dumps({"arm": a.arm, "experiment": exp, "force": force,
                                                        "endpoints": endpoints, "shards": a.shards,
                                                        "smoke": a.smoke, "at": time.strftime("%F %T")}, indent=1))
        env = dict(os.environ, OPENAI_API_KEY="local", LOCAL_API_KEY="local", APPWORLD_LM_TIMEOUT="14400")

        def shard_cmd(i, n, ep, task_id=None):
            ov = {"config": {"agent": {"model_config": {"base_url": ep},
                                       "usage_tracker_config": {"max_output_tokens_per_task": 100_000_000}}}}
            cmd = [CLI, "run", exp, "--root", ".", "--no-with-evaluation", "--override", json.dumps(ov)]
            if task_id:
                cmd += ["--task-id", task_id]
            else:
                cmd += ["--num-processes", str(n), "--process-index", str(i)]
            return cmd

        def run(i, cmd):
            e = dict(env, MODEL_SERVER_URL=endpoints[i % len(endpoints)])
            with open(adir / f"shard-{i:02d}.log", "a") as lf:
                rc = subprocess.run(cmd, cwd=AW / "repo", env=e, stdout=lf, stderr=subprocess.STDOUT).returncode
            log(f"shard {i} rc={rc}")
            return rc

        if a.smoke:
            jobs = [(i, shard_cmd(i, 1, endpoints[i % len(endpoints)], t)) for i, t in enumerate(SMOKE_IDS)]
        else:
            jobs = [(i, shard_cmd(i, a.shards, endpoints[i % len(endpoints)])) for i in range(a.shards)]
        log(f"{tag}: {len(jobs)} shards over {len(endpoints)} endpoint(s)")
        with ThreadPoolExecutor(len(jobs)) as ex:
            list(ex.map(lambda j: run(*j), jobs))
        ev = [CLI, "evaluate", exp, "--root", "."]
        if a.smoke:
            for t in SMOKE_IDS:
                subprocess.run(ev + ["--task-id", t], cwd=AW / "repo", env=env,
                               stdout=open(adir / "eval.log", "a"), stderr=subprocess.STDOUT)
        else:
            subprocess.run(ev + ["test_normal"], cwd=AW / "repo", env=env,
                           stdout=open(adir / "eval.log", "a"), stderr=subprocess.STDOUT)
        log("done; outputs:", AW / "repo/experiments/outputs" / exp)
    finally:
        for p in proxies:
            stop(p)
        for _, p in srv:
            stop(p)


if __name__ == "__main__":
    main()
