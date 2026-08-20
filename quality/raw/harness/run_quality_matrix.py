#!/usr/bin/env python3
"""Resumable 5-quant x 4-effort x 2-suite BenchLocal quality matrix."""

from __future__ import annotations

import argparse
import json
import os
import signal
import socket
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BENCH = "$BENCHLOCAL_ROOT/.venv/bin/benchlocal-cli"
TOKENIZER = "$MODEL_ROOT_FAST/Qwen3.8-27B-FP8"
PROXY_SCRIPT = "$RUN_ROOT/harness/telemetry_proxy.py"
ANALYZER = "$RUN_ROOT/harness/analyze_quality_matrix.py"
CUDA_HOME = "$VLLM_ENV/lib/python3.12/site-packages/nvidia/cu13"
VLLM = "$VLLM_ENV/bin/vllm"
LLAMA = "$LLAMACPP_ROOT/build/bin/llama-server"
NINFER = "$NINFER_ROOT/build-sm86/apps/ninfer-serve"
TARGET_PORT = 18081
PROXY_PORT = 19081


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def vllm_argv(model: str, quantization: str, utilization: str) -> list[str]:
    return [
        VLLM, "serve", model,
        "--tokenizer", TOKENIZER,
        "--served-model-name", "bench",
        "--quantization", quantization,
        "--kernel-config", '{"linear_backend":"marlin"}',
        "--language-model-only",
        "--tensor-parallel-size", "2",
        "--disable-custom-all-reduce",
        "--attention-backend", "FLASHINFER",
        "--kv-cache-dtype", "fp8",
        "--gpu-memory-utilization", utilization,
        "--max-model-len", "262144",
        "--max-num-seqs", "1",
        "--max-num-batched-tokens", "8192",
        "--no-enable-prefix-caching",
        "--reasoning-parser", "qwen3",
        "--enable-auto-tool-choice",
        "--tool-call-parser", "qwen3_xml",
        "--port", str(TARGET_PORT),
    ]


MODELS = {
    "fp8": {
        "engine": "vllm",
        "weights": "$MODEL_ROOT_FAST/Qwen3.8-27B-FP8",
        "context": 262144,
        "kv": "fp8",
        "argv": vllm_argv("$MODEL_ROOT_FAST/Qwen3.8-27B-FP8", "fp8", "0.91"),
        "env": {"CUDA_VISIBLE_DEVICES": "0,1", "CUDA_HOME": CUDA_HOME},
    },
    "nvfp4": {
        "engine": "vllm",
        "weights": "$MODEL_ROOT_FAST/Qwen3.8-27B-NVFP4",
        "context": 262144,
        "kv": "fp8",
        "argv": vllm_argv(
            "$MODEL_ROOT_FAST/Qwen3.8-27B-NVFP4", "compressed-tensors", "0.90"
        ),
        "env": {"CUDA_VISIBLE_DEVICES": "0,1", "CUDA_HOME": CUDA_HOME},
    },
    "awq-int4": {
        "engine": "vllm",
        "weights": "$MODEL_ROOT/Qwen3.8-27B-AWQ-INT4",
        "context": 262144,
        "kv": "fp8",
        "argv": vllm_argv(
            "$MODEL_ROOT/Qwen3.8-27B-AWQ-INT4", "compressed-tensors", "0.90"
        ),
        "env": {"CUDA_VISIBLE_DEVICES": "0,1", "CUDA_HOME": CUDA_HOME},
    },
    "gguf-q4-k-m": {
        "engine": "llama.cpp",
        "weights": "$MODEL_ROOT/Qwen3.8-27B-GGUF/Qwen3.8-27B-Q4_K_M.gguf",
        "context": 262144,
        "kv": "q8_0",
        "argv": [
            LLAMA,
            "--model", "$MODEL_ROOT/Qwen3.8-27B-GGUF/Qwen3.8-27B-Q4_K_M.gguf",
            "--host", "127.0.0.1", "--port", str(TARGET_PORT),
            "--ctx-size", "262144", "--parallel", "1", "--cont-batching",
            "--no-cache-prompt", "--flash-attn", "on", "--gpu-layers", "999",
            "--split-mode", "layer", "--tensor-split", "1,1",
            "--threads", "18", "--threads-batch", "18",
            "--batch-size", "4096", "--ubatch-size", "1024",
            "--cache-type-k", "q8_0", "--cache-type-v", "q8_0",
            "--no-context-shift", "--jinja", "--reasoning", "auto",
            "--reasoning-budget", "-1", "--reasoning-format", "deepseek",
        ],
        "env": {"CUDA_VISIBLE_DEVICES": "0,1"},
    },
    "ninfer": {
        "engine": "ninfer",
        "weights": "$MODEL_ROOT/Qwen3.8-27B-NInfer/qwen3_8_27b.ninfer",
        "context": 187300,
        "kv": "int8",
        "top_level_effort": True,
        "argv": [
            NINFER, "$MODEL_ROOT/Qwen3.8-27B-NInfer/qwen3_8_27b.ninfer",
            "--host", "127.0.0.1", "--port", str(TARGET_PORT),
            "--model-id", "bench", "--max-context", "187300",
            "--kv-capacity", "auto", "--max-concurrency", "1",
            "--max-pending-requests", "1", "--prefill-chunk", "1024",
            "--kv-dtype", "int8", "--default-max-tokens", "187300",
            "--no-prefix-reuse",
        ],
        "env": {"CUDA_VISIBLE_DEVICES": "0"},
    },
}


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def port_is_free(port: int) -> bool:
    with socket.socket() as sock:
        return sock.connect_ex(("127.0.0.1", port)) != 0


def endpoint_ready() -> bool:
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{PROXY_PORT}/health", timeout=3) as response:
            return response.status == 200
    except Exception:
        return False


def stop_group(process: subprocess.Popen | None) -> None:
    if process is None or process.poll() is not None:
        return
    try:
        os.killpg(process.pid, signal.SIGTERM)
        process.wait(timeout=30)
    except (ProcessLookupError, subprocess.TimeoutExpired):
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait(timeout=10)


def result_complete(path: Path, expected: int) -> bool:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return int(data.get("totals", {}).get("total", -1)) == expected
    except (OSError, ValueError, TypeError):
        return False


def effort_args(model: dict, effort: str) -> list[str]:
    if effort == "off":
        args = ["--no-thinking"]
        if model.get("top_level_effort"):
            args += ["--reasoning-effort", "none"]
    else:
        args = ["--enable-thinking", "--reasoning-effort", effort]
    if model.get("top_level_effort"):
        args.append("--reasoning-effort-top-level-only")
    return args


def run_arm(root: Path, model_name: str, model: dict, effort: str, suite: str) -> None:
    arm = root / model_name / effort / suite
    arm.mkdir(parents=True, exist_ok=True)
    result = arm / "result.json"
    expected = 150 if suite == "full" else 90
    if result_complete(result, expected):
        print(f"[{utc_now()}] skip complete {model_name}/{effort}/{suite}", flush=True)
        return
    partial = Path(f"{result}.partial.jsonl")
    report = arm / "RESULTS.md"
    log_path = arm / "run.log"
    common = [
        "--endpoint", f"http://127.0.0.1:{PROXY_PORT}/v1",
        "--model", "bench",
        "--timeout-per-case", "86400",
        "--timeout-ceiling-s", "0",
        "--model-turn-timeout", "0",
        "--progress",
        "--strict-thinking",
        "--history-file", str(root / "history.csv"),
        "--report", "md", "--report-out", str(report),
    ]
    if partial.is_file():
        command = [BENCH, "run", "--resume", str(partial), *common]
    elif result.is_file():
        # A nominally successful run can still be partial when an optional
        # sandbox failed to start. Resume from the folded result so only the
        # absent scenarios are executed instead of repeating the whole arm.
        command = [BENCH, "run", "--resume", str(result), *common]
    else:
        selector = "--full" if suite == "full" else "--reasoning-packs"
        command = [
            BENCH, "run", selector,
            *effort_args(model, effort),
            "--thinking-max-tokens", "0",
            "--tokenizer", TOKENIZER,
            "--incremental", "--save-json", str(result),
            "--sandbox-log-dir", str(arm / "sandbox-logs"),
            *common,
        ]
    write_json(arm / "launch.json", {
        "started_at": utc_now(),
        "argv": command,
        "model": model_name,
        "effort": effort,
        "suite": suite,
        "natural_reasoning": True,
    })
    env = os.environ.copy()
    env["BENCHLOCAL_TELEMETRY_SESSION_PATHS"] = "1"
    print(f"[{utc_now()}] run {model_name}/{effort}/{suite}", flush=True)
    with log_path.open("a", encoding="utf-8") as log:
        log.write(f"\n[{utc_now()}] argv={json.dumps(command)}\n")
        log.flush()
        completed = subprocess.run(
            command,
            stdout=log,
            stderr=subprocess.STDOUT,
            env=env,
            check=False,
        )
    write_json(arm / "status.json", {
        "finished_at": utc_now(),
        "returncode": completed.returncode,
        "complete": result_complete(result, expected),
    })
    if completed.returncode != 0 or not result_complete(result, expected):
        raise RuntimeError(
            f"arm failed: {model_name}/{effort}/{suite} rc={completed.returncode}; see {log_path}"
        )


def run_model(
    root: Path,
    model_name: str,
    model: dict,
    efforts: list[str],
    suites: list[str],
) -> None:
    if not port_is_free(TARGET_PORT) or not port_is_free(PROXY_PORT):
        raise RuntimeError(f"ports {TARGET_PORT}/{PROXY_PORT} are not free")
    model_root = root / model_name
    model_root.mkdir(parents=True, exist_ok=True)
    server_log = (model_root / "server.log").open("a", encoding="utf-8")
    proxy_log = (model_root / "proxy.log").open("a", encoding="utf-8")
    server = None
    proxy = None
    try:
        env = os.environ.copy()
        env.update(model.get("env", {}))
        if model_name == "ninfer":
            model["argv"] += ["--request-log-jsonl", str(model_root / "ninfer-requests.jsonl")]
        write_json(model_root / "server-launch.json", {
            "started_at": utc_now(),
            "engine": model["engine"],
            "weights": model["weights"],
            "context": model["context"],
            "kv": model["kv"],
            "argv": model["argv"],
            "env": model.get("env", {}),
        })
        server = subprocess.Popen(
            model["argv"],
            stdout=server_log,
            stderr=subprocess.STDOUT,
            env=env,
            start_new_session=True,
        )
        proxy = subprocess.Popen(
            [
                sys.executable, PROXY_SCRIPT,
                "--port", str(PROXY_PORT),
                "--target", f"http://127.0.0.1:{TARGET_PORT}",
                "--log", str(model_root / "telemetry.jsonl"),
            ],
            stdout=proxy_log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        deadline = time.monotonic() + 900
        while time.monotonic() < deadline:
            if server.poll() is not None:
                raise RuntimeError(f"model server exited rc={server.returncode}")
            if proxy.poll() is not None:
                raise RuntimeError(f"telemetry proxy exited rc={proxy.returncode}")
            if endpoint_ready():
                break
            time.sleep(1)
        else:
            raise RuntimeError("model endpoint did not become healthy within 900s")
        print(f"[{utc_now()}] ready {model_name}", flush=True)
        for effort in efforts:
            for suite in suites:
                run_arm(root, model_name, model, effort, suite)
    finally:
        stop_group(proxy)
        stop_group(server)
        server_log.close()
        proxy_log.close()


def main() -> int:
    global TARGET_PORT, PROXY_PORT
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--models", nargs="+", choices=MODELS, default=list(MODELS))
    parser.add_argument("--target-port", type=int, default=TARGET_PORT)
    parser.add_argument("--proxy-port", type=int, default=PROXY_PORT)
    parser.add_argument(
        "--efforts", nargs="+", choices=("off", "low", "medium", "xhigh"),
        default=["off", "low", "medium", "xhigh"],
    )
    parser.add_argument(
        "--suites", nargs="+", choices=("full", "reasoning"),
        default=["full", "reasoning"],
    )
    parser.add_argument(
        "--gpu-map-json",
        default="{}",
        help='JSON model-to-CUDA_VISIBLE_DEVICES map, e.g. {"nvfp4":"2,3"}',
    )
    args = parser.parse_args()
    TARGET_PORT = args.target_port
    PROXY_PORT = args.proxy_port
    gpu_map = json.loads(args.gpu_map_json)
    if not isinstance(gpu_map, dict):
        raise ValueError("--gpu-map-json must decode to an object")
    for model_name, model in MODELS.items():
        argv = model["argv"]
        if "--port" in argv:
            argv[argv.index("--port") + 1] = str(TARGET_PORT)
        if model_name in gpu_map:
            model.setdefault("env", {})["CUDA_VISIBLE_DEVICES"] = str(gpu_map[model_name])
    args.root.mkdir(parents=True, exist_ok=True)
    write_json(args.root / f"campaign-{PROXY_PORT}.json", {
        "started_at": utc_now(),
        "models": args.models,
        "efforts": args.efforts,
        "suites": args.suites,
        "benchlocal": BENCH,
        "tokenizer": TOKENIZER,
        "target_port": TARGET_PORT,
        "proxy_port": PROXY_PORT,
        "gpu_map": gpu_map,
        "thinking_max_tokens": None,
        "methodology": "natural endpoint-bounded reasoning; no request max_tokens in thinking arms",
    })
    for model_name in args.models:
        run_model(
            args.root, model_name, dict(MODELS[model_name]), args.efforts, args.suites
        )
    analysis = subprocess.run(
        [
            sys.executable, ANALYZER,
            "--root", str(args.root),
            "--tokenizer-json", f"{TOKENIZER}/tokenizer.json",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    write_json(args.root / f"analysis-status-{PROXY_PORT}.json", {
        "finished_at": utc_now(),
        "returncode": analysis.returncode,
        "stdout": analysis.stdout,
        "stderr": analysis.stderr,
    })
    if analysis.returncode != 0:
        raise RuntimeError(f"final analysis failed rc={analysis.returncode}: {analysis.stderr}")
    write_json(
        args.root / f"LANE-COMPLETE-{PROXY_PORT}.json",
        {"finished_at": utc_now(), "status": "complete"},
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
