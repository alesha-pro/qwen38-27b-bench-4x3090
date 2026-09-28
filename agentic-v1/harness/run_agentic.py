#!/usr/bin/env python3
"""agentic-v1: BenchLocal CLI-40 + HermesAgent-20 for BF16 (OpenRouter, DeepInfra bf16 pin),
Mirai S (Mirai vLLM plugin) and Bonsai 2 PQ2_0 (PrismML llama.cpp fork).

Identical for every arm: same 60 scenarios, xhigh, 3 repeats, same BenchLocal flags, and a
telemetry proxy that forces the same sampling + output cap into every chat/completions body,
including the calls Hermes makes from inside its sandbox:
  temperature 1.0, top_p 0.95, top_k 20, min_p 0.05, presence 0, repetition 1.0, max_tokens 131072
Each (repeat, shard) is one benchlocal process; shards run in parallel against the arm's endpoint(s).
"""
from __future__ import annotations
import argparse, json, os, signal, subprocess, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
import queue
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("$RUN_ROOT/agentic-v1")
BENCH = "$BENCHLOCAL_ROOT/.venv/bin/benchlocal-cli"
TOKENIZER = "$MODEL_ROOT/Qwen3.8-27B-FP8"
PROXY = str(ROOT / "harness/telemetry_proxy.py")
PACKS = {"cli-40": [f"CLI-{i:02d}" for i in range(1, 41)], "hermesagent-20": [f"HA-{i:02d}" for i in range(1, 21)]}
FORCE = {"temperature": 1.0, "top_p": 0.95, "top_k": 20, "min_p": 0.05,
         "presence_penalty": 0.0, "repetition_penalty": 1.0, "max_tokens": 131072}
OR_PIN = {"provider": {"order": ["DeepInfra"], "allow_fallbacks": False, "quantizations": ["bf16"]},
          "model": "qwen/qwen3.8-27b"}
MIRAI_ENV = "$ENGINE_ROOT/mirai-s-vllm-env"
MIRAI_W = "$MODEL_ROOT/trymirai-Qwen3.8-27B-S-experimental/vllm"
BONSAI_BIN = "$ENGINE_ROOT/bonsai-llama-b10743/llama-prism-b10743-adfffbe/llama-server"
BONSAI_GGUF = "$MODEL_ROOT/bonsai2-gguf/27B/Ternary-Bonsai-2-27B-PQ2_0.gguf"
# Palmer recipe (github.com/professorpalmer/bonsai-ada-surgery @5158a8d): his 33-patch fork on prism@adfffbe,
# PQ2_0 (same file as our bonsai arm), medium effort + 20480 thinking budget with force-close message, or thinking off for agents.
# Kept from our protocol: f16 KV (his is q8_0), -np 4 unified KV, 229376 ctx, same sampling/131K cap. MTP off (speed only).
PALMER_BIN = "$ENGINE_ROOT/bonsai-palmer/src/build/bin/llama-server"
PALMER_GGUF = BONSAI_GGUF  # same PQ2_0 file as the xhigh bonsai arm
PALMER = {
    "bonsai-med": {"gpus": ((0, 18414), (1, 18415)), "proxy": 19414, "aw_proxy": 19514, "slot": 4000,
                   "kw": {"reasoning_effort": "medium"}, "force": {"reasoning_effort": "medium"},
                   "bl": ["--enable-thinking", "--reasoning-effort", "medium"]},
    "bonsai-nothink": {"gpus": ((2, 18416), (3, 18417)), "proxy": 19416, "aw_proxy": 19516, "slot": 5000,
                       "kw": {"reasoning_effort": "medium", "enable_thinking": False}, "force": {"reasoning_effort": None},
                       "bl": ["--no-thinking"]},
}


def palmer_force(arm):
    c = PALMER[arm]
    return dict(FORCE, chat_template_kwargs=c["kw"], **c["force"])


def now():
    return datetime.now(timezone.utc).strftime("%H:%M:%S")


def log(*a):
    print(f"[{now()}]", *a, flush=True)


def wait_http(url, proc=None, secs=1800):
    t = time.time()
    while time.time() - t < secs:
        if proc is not None and proc.poll() is not None:
            raise RuntimeError(f"server exited rc={proc.returncode}")
        try:
            urllib.request.urlopen(url, timeout=3)
            return
        except Exception:
            time.sleep(3)
    raise RuntimeError(f"timeout waiting for {url}")


def port_free(port, wait=300):
    import socket
    t = time.time()
    while time.time() - t < wait:
        with socket.socket() as so:
            if so.connect_ex(("127.0.0.1", port)) != 0:
                return
        time.sleep(5)
    raise RuntimeError(f"port {port} still busy: a previous server is alive")


def start(argv, logpath, env=None):
    e = os.environ.copy(); e.update(env or {})
    return subprocess.Popen(argv, stdout=open(logpath, "a"), stderr=subprocess.STDOUT, env=e, start_new_session=True)


def stop(p):
    if p is None or p.poll() is not None:
        return
    try:
        os.killpg(p.pid, signal.SIGINT); p.wait(timeout=90)
    except Exception:
        try: os.killpg(p.pid, signal.SIGKILL)
        except Exception: pass


def servers(arm, adir):
    """Returns (list of (target_url, proc_or_None)), extra procs."""
    if arm == "bf16":
        return [("https://openrouter.ai/api", None)]
    if arm == "mirai":
        env = {"CUDA_VISIBLE_DEVICES": "0,1", "VLLM_USE_FLASHINFER_SAMPLER": "0", "HF_HOME": "$HF_HOME",
               "CUDA_HOME": "$ENGINE_ROOT/cuda13.0-nvcc/nvidia/cu13",
               "PATH": "$ENGINE_ROOT/cuda13.0-nvcc/nvidia/cu13/bin:" + os.environ["PATH"]}
        argv = [f"{MIRAI_ENV}/bin/vllm", "serve", MIRAI_W, "--served-model-name", "bench", "--host", "127.0.0.1",
                "--port", "18410", "--pipeline-parallel-size", "2", "--max-model-len", "262144",
                "--gpu-memory-utilization", "0.90", "--kv-cache-dtype", "bfloat16", "--attention-backend", "FLASH_ATTN",
                "--max-num-seqs", "8", "--max-num-batched-tokens", "2048", "--reasoning-parser", "qwen3",
                "--enable-auto-tool-choice", "--tool-call-parser", "qwen3_xml", "--language-model-only"]
        port_free(18410)
        return [("http://127.0.0.1:18410", start(argv, adir / "server-mirai.log", env))]
    if arm == "bonsai":
        out = []
        for gpu, port in ((2, 18412), (3, 18413)):
            port_free(port)
            argv = [BONSAI_BIN, "-m", BONSAI_GGUF, "--host", "127.0.0.1", "--port", str(port), "--alias", "bench",
                    "-ngl", "999", "-c", "229376", "--parallel", "4", "--kv-unified", "--jinja",
                    "--reasoning-format", "deepseek", "--no-context-shift", "-fa", "on"]
            out.append((f"http://127.0.0.1:{port}", start(argv, adir / f"server-bonsai-gpu{gpu}.log", {"CUDA_VISIBLE_DEVICES": str(gpu)})))
        return out
    if arm in PALMER:
        c, out = PALMER[arm], []
        for gpu, port in c["gpus"]:
            port_free(port)
            argv = [PALMER_BIN, "-m", PALMER_GGUF, "--host", "127.0.0.1", "--port", str(port), "--alias", "bench",
                    "-ngl", "999", "-c", "229376", "--parallel", "4", "--kv-unified", "--jinja",
                    "--reasoning-format", "deepseek", "--no-context-shift", "-fa", "on", "--spec-type", "none",
                    "--chat-template-kwargs", json.dumps(c["kw"]),
                    "--reasoning-budget", "20480", "--reasoning-budget-message", "Now produce the complete answer.",
                    "--reasoning-effort-allow", "medium", "--reasoning-effort-fallback", "medium",
                    "--reasoning-max-tokens-floor", "24576"]
            out.append((f"http://127.0.0.1:{port}", start(argv, adir / f"server-{arm}-gpu{gpu}.log", {"CUDA_VISIBLE_DEVICES": str(gpu)})))
        return out
    raise ValueError(arm)


SLOTS: "queue.Queue[int]" = queue.Queue()


def job(arm, adir, endpoint, rep, shard, scen):
    jd = adir / f"r{rep}" / f"s{shard:02d}"
    jd.mkdir(parents=True, exist_ok=True)
    sf = jd / "scenarios.txt"
    sf.write_text("\n".join(scen) + "\n")
    result = jd / "result.json"
    partial = Path(f"{result}.partial.jsonl")
    common = ["--endpoint", endpoint, "--model", "bench", "--api-key", "local",
              "--timeout-per-case", "86400", "--timeout-ceiling-s", "0", "--model-turn-timeout", "0",
              "--progress", "--strict-thinking", "--no-retry", "--report", "md", "--report-out", str(jd / "RESULTS.md")]
    try:
        if json.loads(result.read_text()).get("totals", {}).get("total") == len(scen):
            return f"r{rep}/s{shard} skip"
    except Exception:
        pass
    if partial.is_file():
        cmd = [BENCH, "run", "--resume", str(partial), *common]
    else:
        think = PALMER[arm]["bl"] if arm in PALMER else ["--enable-thinking", "--reasoning-effort", "xhigh"]
        cmd = [BENCH, "run", "--scenarios-file", str(sf), "--enable-sandboxed-packs", *think, "--thinking-max-tokens", "0", "--tokenizer", TOKENIZER,
               "--incremental", "--save-json", str(result), "--sandbox-log-dir", str(jd / "sandbox-logs"), *common]
    (jd / "launch.json").write_text(json.dumps({"argv": cmd, "arm": arm, "rep": rep, "shard": shard, "at": now()}, indent=1))
    env = os.environ.copy(); env["BENCHLOCAL_TELEMETRY_SESSION_PATHS"] = "1"
    # BenchLocal binds every sandbox of a pack to one fixed host port; parallel
    # processes need their own offset (native BENCHLOCAL_SANDBOX_PORT_OFFSET).
    off = SLOTS.get()
    env["BENCHLOCAL_SANDBOX_PORT_OFFSET"] = str(off)
    try:
        with open(jd / "run.log", "a") as lf:
            lf.write(f"[{now()}] sandbox port offset {off}\n"); lf.flush()
            rc = subprocess.run(cmd, stdout=lf, stderr=subprocess.STDOUT, env=env).returncode
    finally:
        SLOTS.put(off)
    return f"r{rep}/s{shard} rc={rc}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", required=True, choices=["bf16", "mirai", "bonsai", *PALMER])
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--reps", type=int, nargs="+", default=[1, 2, 3])
    ap.add_argument("--smoke", action="store_true", help="2 scenarios (1 per pack), rep 0")
    a = ap.parse_args()
    adir = ROOT / "runs" / (a.arm + ("-smoke" if a.smoke else ""))
    adir.mkdir(parents=True, exist_ok=True)
    scen = [f"{p}/{s}" for p, ss in PACKS.items() for s in ss]
    if a.smoke:
        scen = ["cli-40/CLI-21", "hermesagent-20/HA-01"]; a.reps = [0]; a.workers = 2
    srv, proxies = [], []
    try:
        srv = servers(a.arm, adir)
        force = palmer_force(a.arm) if a.arm in PALMER else dict(FORCE, **(OR_PIN if a.arm == "bf16" else {}))
        endpoints = []
        for i, (target, proc) in enumerate(srv):
            if proc is not None:
                wait_http(target + "/v1/models", proc)
                log("server ready", target)
            port = ({"bf16": 19420, "mirai": 19410, "bonsai": 19412}.get(a.arm) or PALMER[a.arm]["proxy"]) + i
            pargs = [sys.executable, PROXY, "--host", "0.0.0.0", "--port", str(port), "--target", target,
                     "--log", str(adir / f"telemetry-{i}.jsonl"), "--force-json", json.dumps(force)]
            if a.arm == "bf16":
                pargs += ["--auth-file", "$HOME_DIR/.config/openrouter/key"]
            port_free(port)
            proxies.append(start(pargs, adir / f"proxy-{i}.log"))
            endpoints.append(f"http://127.0.0.1:{port}/v1")
        time.sleep(3)
        for p in proxies:
            if p.poll() is not None:
                raise RuntimeError("telemetry proxy died at start, see proxy-*.log")
        for _, p in srv:
            if p is not None and p.poll() is not None:
                raise RuntimeError("model server died at start")
        (adir / "campaign.json").write_text(json.dumps({"arm": a.arm, "force": force, "endpoints": endpoints,
                                                        "workers": a.workers, "reps": a.reps, "scenarios": len(scen), "at": now()}, indent=1))
        if a.arm == "mirai":
            log("mirai health check (fresh-instance degeneration)")
            env = dict(os.environ, QB2_LOCAL_BASE_URL="http://127.0.0.1:18410/v1", QB2_LOCAL_MODEL="bench", QB2_TIMEOUT="14400")
            rc = subprocess.run(["$RUN_ROOT/quant-bench-v2/venv/bin/python",
                                 "$RUN_ROOT/quant-bench-v2/harness/mirai_health.py",
                                 "--out", str(adir / "health.json")], env=env).returncode
            if rc == 1:
                raise RuntimeError("mirai instance degenerate, restart it")
        jobs = []
        shards = max(1, a.workers if not a.smoke else len(scen))
        for rep in a.reps:
            for k in range(shards):
                sub = scen[k::shards]
                if sub:
                    jobs.append((rep, k, sub))
        base = ({"bf16": 1000, "mirai": 2000, "bonsai": 3000}.get(a.arm) or PALMER[a.arm]["slot"]) + (500 if a.smoke else 0)
        for w in range(a.workers):
            SLOTS.put(base + 10 * w)
        log(f"{a.arm}: {len(jobs)} jobs, {a.workers} workers, endpoints {endpoints}")
        with ThreadPoolExecutor(a.workers) as ex:
            futs = [ex.submit(job, a.arm, adir, endpoints[i % len(endpoints)], rep, k, sub) for i, (rep, k, sub) in enumerate(jobs)]
            for f in futs:
                log(f.result())
        log("ALL DONE", a.arm)
    finally:
        for p in proxies: stop(p)
        for _, p in srv: stop(p)


if __name__ == "__main__":
    main()
