#!/usr/bin/env python3
"""Resumable Qwen3.8 depth sweep for vLLM or SGLang on Ampere.

The runner owns the vLLM server, writes one atomic JSON file per
configuration/depth/concurrency point, and skips completed points after a
restart.  It is intended to be run by the accompanying user systemd service.

Default fast matrix:
  TP={2,4} x KV={BF16,FP8} x MTP={off,on}
  depth={8K,32K,64K,128K,~248K}
  concurrency={1,2,4,8,16} at 8K; concurrency=1 at deeper contexts

Set SWEEP_PROFILE=full to run every concurrency at every depth.

Environment overrides (comma-separated where applicable):
  RUN_DIR, SWEEP_PROFILE, DEPTHS, CONCURRENCIES, CONFIG_FILTER,
  GEN_TOKENS, CONFIG_WARMUPS, CONFIG_WARMUP_CONCURRENCIES, DEPTH_WARMUPS,
  GPU_MEMORY_UTILIZATION, PORT,
  SGLANG_MAX_RUNNING_REQUESTS, SGLANG_MAX_TOTAL_TOKENS,
  MAX_POINT_ATTEMPTS, SERVER_START_ATTEMPTS, SERVER_START_TIMEOUT_S
"""

from __future__ import annotations

import argparse
import csv
import fcntl
import json
import os
import re
import shutil
import signal
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import bench_matrix


ROOT = Path(__file__).resolve().parent
ENGINE = os.environ.get("ENGINE", "vllm").strip().lower()
MODEL = Path(os.environ.get("MODEL", "$MODELS/Qwen3.8-27B-NVFP4"))
VLLM = Path(
    os.environ.get(
        "VLLM_BIN", "$ENGINES/vllm-cross-kv-env/bin/vllm"
    )
)
SGLANG = Path(
    os.environ.get(
        "SGLANG_BIN", "$ENGINES/sglang-nvfp4-env/bin/sglang"
    )
)
PYTHON = Path(
    os.environ.get(
        "ENGINE_PYTHON",
        os.environ.get(
            "VLLM_PYTHON",
            "$ENGINES/sglang-nvfp4-env/bin/python"
            if ENGINE == "sglang"
            else "$ENGINES/vllm-cross-kv-env/bin/python",
        ),
    )
)
CUDA_HOME = Path(
    os.environ.get(
        "CUDA_HOME",
        "$ENGINES/sglang-nvfp4-env/lib/python3.12/site-packages/nvidia/cu13"
        if ENGINE == "sglang"
        else "$ENGINES/vllm-cross-kv-env/lib/python3.12/site-packages/nvidia/cu13",
    )
)
WEIGHT_QUANTIZATION = os.environ.get("WEIGHT_QUANTIZATION", "").strip().lower()
MTP_NAME = os.environ.get(
    "MTP_NAME", "mtp4" if ENGINE == "sglang" else "mtp2"
)
DEFAULT_RUN_DIR = (
    ROOT / "output" / f"{ENGINE}-depth-autonomous-{MODEL.name.lower()}"
)


def now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def parse_ints(name: str, default: str) -> list[int]:
    raw = os.environ.get(name, default)
    return [int(x.strip()) for x in raw.replace(" ", ",").split(",") if x.strip()]


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + f".tmp-{os.getpid()}")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(value, fh, indent=2, ensure_ascii=False)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


def read_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def model_quantization() -> str:
    if WEIGHT_QUANTIZATION:
        return WEIGHT_QUANTIZATION
    config = read_json(MODEL / "config.json", {})
    quantization = config.get("quantization_config") or {}
    method = str(quantization.get("quant_method", "")).strip().lower()
    if not method:
        raise RuntimeError(
            "WEIGHT_QUANTIZATION is unset and model config has no quant_method"
        )
    return method


def http_json(url: str, payload: dict[str, Any] | None = None, timeout: int = 30) -> Any:
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"} if data is not None else {},
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        raw = response.read()
    return json.loads(raw) if raw else None


@dataclass(frozen=True)
class Config:
    tp: int
    kv: str
    mtp: bool

    @property
    def name(self) -> str:
        return f"tp{self.tp}-{self.kv}-{MTP_NAME if self.mtp else 'nomtp'}"

    @property
    def attention_backend(self) -> str:
        return "FLASHINFER" if self.kv == "fp8" else "TRITON_ATTN"


class Runner:
    def __init__(self, run_dir: Path, dry_run: bool = False) -> None:
        self.run_dir = run_dir
        self.dry_run = dry_run
        self.port = int(os.environ.get("PORT", "18081"))
        self.sweep_profile = os.environ.get("SWEEP_PROFILE", "fast").strip().lower()
        self.depths = parse_ints("DEPTHS", "8192,32768,65536,131072,253952")
        self.concurrencies = parse_ints("CONCURRENCIES", "1,2,4,8,16")
        default_depth_warmups = "1" if self.sweep_profile == "full" else "0"
        self.config_warmups = os.environ.get(
            "CONFIG_WARMUPS", "1"
        ).strip().lower() in {"1", "true", "yes", "on"}
        self.config_warmup_concurrencies = parse_ints(
            "CONFIG_WARMUP_CONCURRENCIES",
            ",".join(str(value) for value in self.concurrencies),
        )
        self.depth_warmups = os.environ.get(
            "DEPTH_WARMUPS", default_depth_warmups
        ).strip().lower() in {"1", "true", "yes", "on"}
        self.gen_tokens = int(os.environ.get("GEN_TOKENS", "128"))
        self.gpu_memory_utilization = float(
            os.environ.get("GPU_MEMORY_UTILIZATION", "0.90")
        )
        self.max_attempts = int(os.environ.get("MAX_POINT_ATTEMPTS", "2"))
        self.server_start_attempts = int(
            os.environ.get("SERVER_START_ATTEMPTS", "2")
        )
        self.start_timeout = int(os.environ.get("SERVER_START_TIMEOUT_S", "1200"))
        wanted = {
            x.strip()
            for x in os.environ.get("CONFIG_FILTER", "").split(",")
            if x.strip()
        }
        configs = [
            Config(tp=tp, kv=kv, mtp=mtp)
            for tp in (2, 4)
            for kv in ("bf16", "fp8")
            for mtp in (False, True)
        ]
        self.configs = [c for c in configs if not wanted or c.name in wanted]
        self.server: subprocess.Popen[bytes] | None = None
        self.server_log_handle: Any = None
        self.server_config: Config | None = None
        self.stop_requested = False
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.log_path = self.run_dir / "run.log"
        self.status_path = self.run_dir / "status.json"

    def concurrencies_for_depth(self, depth: int) -> list[int]:
        if self.sweep_profile == "full" or depth == min(self.depths):
            return self.concurrencies
        return [1] if 1 in self.concurrencies else [min(self.concurrencies)]

    def scheduled_points(self) -> list[tuple[Config, int, int]]:
        return [
            (config, depth, concurrency)
            for config in self.configs
            for depth in self.depths
            for concurrency in self.concurrencies_for_depth(depth)
        ]

    def work_batches(self) -> list[tuple[int, list[int]]]:
        """Put single-stream depth decay before risky aggregate points."""
        if self.sweep_profile == "full":
            return [
                (depth, self.concurrencies_for_depth(depth))
                for depth in self.depths
            ]
        serial_concurrency = 1 if 1 in self.concurrencies else min(self.concurrencies)
        batches = [(depth, [serial_concurrency]) for depth in self.depths]
        base_depth = min(self.depths)
        parallel = [
            concurrency
            for concurrency in self.concurrencies_for_depth(base_depth)
            if concurrency != serial_concurrency
        ]
        if parallel:
            batches.append((base_depth, parallel))
        return batches

    def log(self, message: str) -> None:
        line = f"[{now()}] {message}"
        print(line, flush=True)
        with self.log_path.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")

    def manifest(self) -> dict[str, Any]:
        return {
            "created_or_refreshed_at": now(),
            "engine": ENGINE,
            "model": str(MODEL),
            "vllm": str(VLLM),
            "sglang": str(SGLANG),
            "python": str(PYTHON),
            "cuda_home": str(CUDA_HOME),
            "weight_quantization": model_quantization(),
            "max_model_len": 262144,
            "sweep_profile": self.sweep_profile,
            "depths": self.depths,
            "concurrencies": self.concurrencies,
            "concurrencies_by_depth": {
                str(depth): self.concurrencies_for_depth(depth)
                for depth in self.depths
            },
            "execution_batches": [
                {"depth": depth, "concurrencies": concurrencies}
                for depth, concurrencies in self.work_batches()
            ],
            "config_warmups": self.config_warmups,
            "config_warmup_concurrencies": self.config_warmup_concurrencies,
            "depth_warmups": self.depth_warmups,
            "generation_tokens": self.gen_tokens,
            "gpu_memory_utilization": self.gpu_memory_utilization,
            "configs": [asdict(c) | {"name": c.name} for c in self.configs],
            "metrics": {
                "decode_tok_s_median": "per-request steady decode after first token",
                "aggregate_decode_window_tok_s": "all post-first tokens divided by shared decode window",
                "aggregate_active_decode_rate_sum": "sum of per-request steady decode rates",
                "aggregate_tok_s": "end-to-end output throughput including prefill",
            },
            "notes": [
                "No run uses eager mode; compile and CUDA graphs stay enabled.",
                "vLLM uses TRITON_ATTN for BF16 KV and FLASHINFER for FP8 KV; SGLang uses its default FlashInfer attention backend.",
                "Fast profile measures the full concurrency knee at 8K and single-stream decay at every deeper context.",
                "Every completed point is fsync'd and atomically renamed for reboot-safe resume.",
            ],
        }

    def write_status(self, phase: str, **extra: Any) -> None:
        ok = 0
        failed = 0
        retryable_failed = 0
        scheduled = self.scheduled_points()
        for config, depth, concurrency in scheduled:
            point = self.point_path(config, depth, concurrency)
            data = read_json(point, {})
            if data.get("status") == "ok":
                ok += 1
            elif data.get("status") == "failed" and int(
                data.get("attempts", 0)
            ) >= self.max_attempts:
                failed += 1
            elif data.get("status") == "failed":
                retryable_failed += 1
        total = len(scheduled)
        atomic_json(
            self.status_path,
            {
                "updated_at": now(),
                "phase": phase,
                "completed_ok": ok,
                "completed_failed": failed,
                "retryable_failed": retryable_failed,
                "total_points": total,
                "remaining": max(0, total - ok - failed),
                **extra,
            },
        )

    def preflight(self) -> None:
        errors = []
        if ENGINE not in {"vllm", "sglang"}:
            errors.append("ENGINE must be 'vllm' or 'sglang'")
        if self.sweep_profile not in {"fast", "full"}:
            errors.append("SWEEP_PROFILE must be 'fast' or 'full'")
        if not self.depths:
            errors.append("DEPTHS must contain at least one depth")
        if not self.concurrencies:
            errors.append("CONCURRENCIES must contain at least one value")
        if not MODEL.is_dir():
            errors.append(f"model directory missing: {MODEL}")
        engine_binary = VLLM if ENGINE == "vllm" else SGLANG
        if not engine_binary.is_file():
            errors.append(f"{ENGINE} binary missing: {engine_binary}")
        if not PYTHON.is_file():
            errors.append(f"engine python missing: {PYTHON}")
        if not (CUDA_HOME / "bin" / "nvcc").is_file():
            errors.append(f"nvcc missing under CUDA_HOME: {CUDA_HOME}")
        if max(self.depths) + self.gen_tokens > 262144:
            errors.append("largest depth + generation exceeds max_model_len=262144")
        if max(self.concurrencies) > 16:
            errors.append("concurrency exceeds --max-num-seqs=16")
        if errors:
            raise RuntimeError("; ".join(errors))

        probes: dict[str, Any] = {}
        commands = {
            "nvcc": [str(CUDA_HOME / "bin" / "nvcc"), "--version"],
            "python_env": [
                str(PYTHON),
                "-c",
                f"import torch, {ENGINE}; print(torch.__version__, torch.version.cuda)",
            ],
            "nvidia_smi": [
                "nvidia-smi",
                "--query-gpu=index,name,memory.total,compute_cap,power.limit",
                "--format=csv,noheader",
            ],
        }
        for name, command in commands.items():
            proc = subprocess.run(command, capture_output=True, text=True, timeout=60)
            probes[name] = {
                "returncode": proc.returncode,
                "stdout": proc.stdout.strip(),
                "stderr": proc.stderr.strip(),
            }
            if proc.returncode != 0:
                raise RuntimeError(f"preflight {name} failed: {proc.stderr.strip()}")
        nvcc_text = probes["nvcc"]["stdout"] + probes["nvcc"]["stderr"]
        if "release 13.0" not in nvcc_text:
            raise RuntimeError(
                "FP8 FlashInfer JIT requires the CUDA 13.0 compiler matching torch/header runtime; "
                f"got: {nvcc_text[-300:]}"
            )
        atomic_json(self.run_dir / "preflight.json", {"when": now(), **probes})

    def server_env(self, config: Config) -> dict[str, str]:
        env = os.environ.copy()
        env["CUDA_HOME"] = str(CUDA_HOME)
        env["CUDA_LIB_PATH"] = str(CUDA_HOME / "lib")
        env["PATH"] = (
            f"$USER_HOME/.cargo/bin:{CUDA_HOME / 'bin'}:{env.get('PATH', '')}"
        )
        env["LD_LIBRARY_PATH"] = (
            f"{CUDA_HOME / 'lib'}"
            + (f":{env['LD_LIBRARY_PATH']}" if env.get("LD_LIBRARY_PATH") else "")
        )
        if ENGINE == "vllm":
            env["VLLM_USE_FLASHINFER_SAMPLER"] = "0"
            env["VLLM_WORKER_MULTIPROC_METHOD"] = "spawn"
        env["PYTORCH_ALLOC_CONF"] = "expandable_segments:True"
        env["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
        env["CUDA_VISIBLE_DEVICES"] = ",".join(str(x) for x in range(config.tp))
        return env

    def server_command(self, config: Config) -> list[str]:
        quantization = model_quantization()
        if ENGINE == "vllm":
            command = [
                str(VLLM),
                "serve",
                str(MODEL),
                "--served-model-name",
                "bench",
                "--quantization",
                quantization,
                "--kernel-config",
                '{"linear_backend":"marlin"}',
                "--language-model-only",
                "--tensor-parallel-size",
                str(config.tp),
                "--disable-custom-all-reduce",
                "--attention-backend",
                config.attention_backend,
                "--kv-cache-dtype",
                "bfloat16" if config.kv == "bf16" else "fp8",
                "--gpu-memory-utilization",
                str(self.gpu_memory_utilization),
                "--max-model-len",
                "262144",
                "--max-num-seqs",
                "16",
                "--max-num-batched-tokens",
                "8192",
                "--no-enable-prefix-caching",
                "--port",
                str(self.port),
            ]
            if config.mtp:
                command += [
                    "--speculative-config",
                    '{"method":"mtp","num_speculative_tokens":2}',
                ]
            return command

        command = [
            str(SGLANG),
            "serve",
            "--model-path",
            str(MODEL),
            "--served-model-name",
            "bench",
            "--host",
            "127.0.0.1",
            "--port",
            str(self.port),
            "--tp-size",
            str(config.tp),
            "--context-length",
            "262144",
            "--mem-fraction-static",
            str(self.gpu_memory_utilization),
            "--max-running-requests",
            os.environ.get("SGLANG_MAX_RUNNING_REQUESTS", "16"),
            "--chunked-prefill-size",
            "8192",
            "--cuda-graph-max-bs-prefill",
            os.environ.get("SGLANG_PREFILL_GRAPH_MAX_TOKENS", "256"),
            "--disable-radix-cache",
            "--disable-custom-all-reduce",
            "--language-only",
            "--quantization",
            quantization,
            "--kv-cache-dtype",
            "bf16" if config.kv == "bf16" else "fp8_e4m3",
            "--reasoning-parser",
            "qwen3",
        ]
        if quantization == "compressed-tensors":
            command += ["--fp4-gemm-backend", "marlin"]
        if max_total_tokens := os.environ.get("SGLANG_MAX_TOTAL_TOKENS", "").strip():
            command += ["--max-total-tokens", max_total_tokens]
        if config.mtp:
            command += [
                "--speculative-algorithm",
                "EAGLE",
                "--speculative-num-steps",
                "3",
                "--speculative-eagle-topk",
                "1",
                "--speculative-num-draft-tokens",
                "4",
            ]
        return command

    def healthy(self) -> bool:
        try:
            with urllib.request.urlopen(
                f"http://127.0.0.1:{self.port}/health", timeout=3
            ) as response:
                return response.status == 200
        except Exception:
            return False

    def port_in_use(self) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            return sock.connect_ex(("127.0.0.1", self.port)) == 0

    def start_server(self, config: Config) -> bool:
        self.stop_server()
        if self.port_in_use():
            raise RuntimeError(f"port {self.port} is already in use")
        attempts_dir = self.run_dir / "configs" / config.name
        attempts_dir.mkdir(parents=True, exist_ok=True)
        attempt = len(list(attempts_dir.glob("server-attempt-*.log"))) + 1
        log_path = attempts_dir / f"server-attempt-{attempt:02d}.log"
        command = self.server_command(config)
        atomic_json(
            attempts_dir / f"launch-attempt-{attempt:02d}.json",
            {
                "when": now(),
                "command": command,
                "cuda_visible_devices": self.server_env(config)["CUDA_VISIBLE_DEVICES"],
            },
        )
        self.log(f"starting {config.name}, server attempt {attempt}: {' '.join(command)}")
        self.server_log_handle = log_path.open("ab", buffering=0)
        self.server = subprocess.Popen(
            command,
            cwd=ROOT,
            env=self.server_env(config),
            stdout=self.server_log_handle,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        self.server_config = config
        deadline = time.monotonic() + self.start_timeout
        while time.monotonic() < deadline and not self.stop_requested:
            if self.server.poll() is not None:
                self.log(f"server {config.name} exited rc={self.server.returncode}")
                self.stop_server()
                return False
            if self.healthy():
                self.log(f"server {config.name} is healthy")
                return True
            time.sleep(2)
        if self.stop_requested:
            self.log(f"server {config.name} startup interrupted")
            self.stop_server()
            return False
        self.log(f"server {config.name} readiness timed out")
        self.stop_server()
        return False

    def stop_server(self) -> None:
        proc = self.server
        self.server = None
        self.server_config = None
        if proc is not None and proc.poll() is None:
            try:
                os.killpg(proc.pid, signal.SIGINT)
            except ProcessLookupError:
                pass
            try:
                proc.wait(timeout=45)
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(proc.pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
                try:
                    proc.wait(timeout=15)
                except subprocess.TimeoutExpired:
                    try:
                        os.killpg(proc.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    proc.wait(timeout=10)
        if self.server_log_handle is not None:
            self.server_log_handle.close()
            self.server_log_handle = None

    def ensure_server(self, config: Config) -> bool:
        if (
            self.server is not None
            and self.server_config == config
            and self.server.poll() is None
            and self.healthy()
        ):
            return True
        return self.start_server(config)

    def ensure_server_with_retries(self, config: Config) -> bool:
        for attempt in range(1, self.server_start_attempts + 1):
            if self.stop_requested:
                return False
            try:
                if self.ensure_server(config):
                    return True
            except Exception as exc:
                self.log(
                    f"server start error for {config.name} "
                    f"({attempt}/{self.server_start_attempts}): {exc!r}"
                )
                self.stop_server()
            if attempt < self.server_start_attempts and not self.stop_requested:
                self.log(
                    f"retrying server {config.name} in 10s "
                    f"({attempt + 1}/{self.server_start_attempts})"
                )
                deadline = time.monotonic() + 10
                while time.monotonic() < deadline and not self.stop_requested:
                    time.sleep(0.5)
        return False

    def tokenize_count(self, prompt: str) -> int:
        response = http_json(
            f"http://127.0.0.1:{self.port}/tokenize",
            {
                "model": "bench",
                "messages": [{"role": "user", "content": prompt}],
                "chat_template_kwargs": {"enable_thinking": False},
            },
            timeout=120,
        )
        return int(response["count"])

    def prompt_for_depth(self, depth: int, salt: str) -> tuple[str, int, float]:
        chars_per_token = 5.55
        prompt = ""
        count = 0
        for _ in range(6):
            prompt = bench_matrix.make_prompt(
                0, depth, salt=salt, chars_per_token=chars_per_token
            )
            count = self.tokenize_count(prompt)
            if abs(count - depth) <= 32:
                break
            chars_per_token *= depth / max(count, 1)
        return prompt, count, round(chars_per_token, 6)

    def warm_config(self, config: Config) -> bool:
        path = self.run_dir / "configs" / config.name / "warmup.json"
        if path.exists():
            return read_json(path, {}).get("status") == "ok"
        rows = []
        for concurrency in self.config_warmup_concurrencies:
            row = bench_matrix.run_level(
                f"http://127.0.0.1:{self.port}/v1/chat/completions",
                "bench",
                concurrency,
                16,
                0,
                f"warm-{config.name}-c{concurrency}",
                4.0,
            )
            rows.append(row)
            if row["requests_ok"] != concurrency:
                atomic_json(
                    path,
                    {
                        "when": now(),
                        "status": "failed",
                        "failed_concurrency": concurrency,
                        "rows": rows,
                    },
                )
                return False
        atomic_json(path, {"when": now(), "status": "ok", "rows": rows})
        return True

    def warm_depth(self, config: Config, depth: int, prompt: str, chars_per_token: float) -> None:
        path = self.run_dir / "configs" / config.name / f"depth-{depth}-warmup.json"
        if path.exists():
            return
        row = bench_matrix.run_level(
            f"http://127.0.0.1:{self.port}/v1/chat/completions",
            "bench",
            1,
            8,
            depth,
            f"depth-warm-{config.name}-d{depth}",
            chars_per_token,
        )
        atomic_json(path, {"when": now(), "row": row})
        if row["requests_ok"] != 1:
            raise RuntimeError(f"depth warmup failed: {row['errors']}")

    def point_path(self, config: Config, depth: int, concurrency: int) -> Path:
        return (
            self.run_dir
            / "points"
            / config.name
            / f"depth-{depth}-c{concurrency}.json"
        )

    def point_done(self, path: Path) -> bool:
        data = read_json(path, {})
        if data.get("status") == "ok":
            return True
        return data.get("status") == "failed" and int(data.get("attempts", 0)) >= self.max_attempts

    def run_point(
        self,
        config: Config,
        depth: int,
        concurrency: int,
        chars_per_token: float,
        actual_tokenized_count: int,
    ) -> None:
        path = self.point_path(config, depth, concurrency)
        previous = read_json(path, {})
        attempts = int(previous.get("attempts", 0))
        while attempts < self.max_attempts and not self.stop_requested:
            attempts += 1
            if not self.ensure_server(config):
                error = "server failed to start"
                row = None
            else:
                try:
                    row = bench_matrix.run_level(
                        f"http://127.0.0.1:{self.port}/v1/chat/completions",
                        "bench",
                        concurrency,
                        self.gen_tokens,
                        depth,
                        f"measure-{config.name}-d{depth}-c{concurrency}",
                        chars_per_token,
                    )
                    error = None
                except Exception as exc:
                    row = None
                    error = repr(exc)
            if self.stop_requested:
                self.log(
                    f"interrupted {config.name} depth={depth} c={concurrency}; "
                    "leaving the point uncommitted for resume"
                )
                return
            ok = bool(
                row
                and row.get("requests_ok") == concurrency
                and not row.get("errors")
                and row.get("decode_tok_s_median") is not None
                and int(row.get("total_tokens", 0)) >= 2 * concurrency
            )
            payload = {
                "status": "ok" if ok else "failed",
                "finished_at": now(),
                "attempts": attempts,
                "config": asdict(config) | {"name": config.name},
                "depth_requested": depth,
                "tokenized_prompt_count_probe": actual_tokenized_count,
                "concurrency": concurrency,
                "generation_tokens": self.gen_tokens,
                "row": row,
                "error": error,
            }
            atomic_json(path, payload)
            self.write_summary()
            self.write_status(
                "running",
                current_config=config.name,
                current_depth=depth,
                current_concurrency=concurrency,
            )
            if ok:
                self.log(
                    f"OK {config.name} depth={depth} c={concurrency}: "
                    f"decode={row.get('decode_tok_s_median')} "
                    f"agg_decode={row.get('aggregate_decode_window_tok_s')}"
                )
                return
            self.log(
                f"FAIL {config.name} depth={depth} c={concurrency} attempt={attempts}: "
                f"{error or (row or {}).get('errors')}"
            )
            if self.server is None or self.server.poll() is not None or not self.healthy():
                self.stop_server()

    def write_summary(self) -> None:
        rows: list[dict[str, Any]] = []
        for path in sorted((self.run_dir / "points").glob("**/*.json")):
            point = read_json(path, {})
            row = point.get("row") or {}
            config = point.get("config") or {}
            rows.append(
                {
                    "config": config.get("name"),
                    "tp": config.get("tp"),
                    "kv": config.get("kv"),
                    "mtp": config.get("mtp"),
                    "depth": point.get("depth_requested"),
                    "prompt_tokens": row.get("prompt_tokens_median"),
                    "concurrency": point.get("concurrency"),
                    "status": point.get("status"),
                    "attempts": point.get("attempts"),
                    "decode_tok_s_median": row.get("decode_tok_s_median"),
                    "aggregate_decode_window_tok_s": row.get(
                        "aggregate_decode_window_tok_s"
                    ),
                    "aggregate_active_decode_rate_sum": row.get(
                        "aggregate_active_decode_rate_sum"
                    ),
                    "end_to_end_output_tok_s": row.get("aggregate_tok_s"),
                    "prefill_tok_s_median": row.get("prefill_tok_s_median"),
                    "prefill_tok_s_aggregate": row.get(
                        "prefill_tok_s_aggregate"
                    ),
                    "ttft_p50_ms": row.get("ttft_p50_ms"),
                    "ttft_max_ms": row.get("ttft_max_ms"),
                    "wall_s": row.get("wall_s"),
                }
            )
        atomic_json(self.run_dir / "summary.json", rows)
        csv_tmp = self.run_dir / f"summary.csv.tmp-{os.getpid()}"
        columns = list(rows[0]) if rows else [
            "config",
            "tp",
            "kv",
            "mtp",
            "depth",
            "concurrency",
            "status",
        ]
        with csv_tmp.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=columns)
            writer.writeheader()
            writer.writerows(rows)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(csv_tmp, self.run_dir / "summary.csv")

    def handle_signal(self, signum: int, _frame: Any) -> None:
        self.stop_requested = True
        self.log(f"received signal {signum}; stopping server after current interruption")
        self.stop_server()

    def run(self) -> int:
        self.preflight()
        atomic_json(self.run_dir / "manifest.json", self.manifest())
        if self.dry_run:
            self.log("dry-run successful; matrix validated")
            self.write_status("dry-run")
            return 0
        if (self.run_dir / "DONE").exists():
            self.log("DONE marker already exists; nothing to resume")
            self.write_status("complete")
            return 0

        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)
        self.write_status("starting")
        try:
            for config in self.configs:
                if self.stop_requested:
                    break
                pending = [
                    (depth, concurrency)
                    for depth in self.depths
                    for concurrency in self.concurrencies_for_depth(depth)
                    if not self.point_done(self.point_path(config, depth, concurrency))
                ]
                if not pending:
                    self.log(f"skip complete config {config.name}")
                    continue
                if not self.ensure_server_with_retries(config):
                    if self.stop_requested:
                        break
                    self.log(f"cannot start {config.name}; recording its points as failed")
                    for depth, concurrency in pending:
                        path = self.point_path(config, depth, concurrency)
                        prev = read_json(path, {})
                        atomic_json(
                            path,
                            {
                                "status": "failed",
                                "finished_at": now(),
                                "attempts": self.max_attempts,
                                "config": asdict(config) | {"name": config.name},
                                "depth_requested": depth,
                                "concurrency": concurrency,
                                "row": None,
                                "error": "server failed to start",
                                "previous": prev or None,
                            },
                        )
                    self.write_summary()
                    continue
                if self.config_warmups:
                    try:
                        if not self.warm_config(config):
                            self.log(
                                f"config warmup failed for {config.name}; "
                                "continuing with individually recorded points"
                            )
                            self.stop_server()
                    except Exception as exc:
                        self.log(f"config warmup error for {config.name}: {exc!r}")
                        self.stop_server()
                else:
                    self.log(f"config warmup disabled for resume: {config.name}")
                for depth, batch_concurrencies in self.work_batches():
                    if self.stop_requested:
                        break
                    remaining = [
                        c
                        for c in batch_concurrencies
                        if not self.point_done(self.point_path(config, depth, c))
                    ]
                    if not remaining:
                        continue
                    if not self.ensure_server_with_retries(config):
                        self.log(
                            f"cannot restore {config.name} before depth={depth}; "
                            "leaving its remaining points for service restart"
                        )
                        break
                    salt = f"probe-{config.name}-d{depth}"
                    prompt, token_count, chars_per_token = self.prompt_for_depth(depth, salt)
                    probe_path = (
                        self.run_dir
                        / "configs"
                        / config.name
                        / f"depth-{depth}-prompt-probe.json"
                    )
                    atomic_json(
                        probe_path,
                        {
                            "when": now(),
                            "depth_requested": depth,
                            "token_count": token_count,
                            "chars_per_token": chars_per_token,
                            "prompt_chars": len(prompt),
                        },
                    )
                    if self.depth_warmups:
                        try:
                            self.warm_depth(config, depth, prompt, chars_per_token)
                        except Exception as exc:
                            self.log(f"depth warmup failed {config.name} d={depth}: {exc!r}")
                            self.stop_server()
                    for concurrency in remaining:
                        if self.stop_requested:
                            break
                        self.run_point(
                            config,
                            depth,
                            concurrency,
                            chars_per_token,
                            token_count,
                        )
                self.stop_server()
        finally:
            self.stop_server()
            self.write_summary()

        if self.stop_requested:
            self.write_status("interrupted")
            return 130

        unfinished = [
            (config.name, depth, concurrency)
            for config, depth, concurrency in self.scheduled_points()
            if not self.point_done(self.point_path(config, depth, concurrency))
        ]
        if unfinished:
            self.write_status(
                "incomplete",
                unfinished_count=len(unfinished),
                unfinished_examples=unfinished[:10],
            )
            self.log(
                f"matrix has {len(unfinished)} unfinished points; "
                "exiting non-zero so systemd resumes it"
            )
            return 1
        self.write_status("complete")
        (self.run_dir / "DONE").write_text(now() + "\n", encoding="utf-8")
        self.log("all matrix points finished; DONE marker written")
        return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--run-dir",
        type=Path,
        default=Path(os.environ.get("RUN_DIR", str(DEFAULT_RUN_DIR))),
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    args.run_dir.mkdir(parents=True, exist_ok=True)
    lock_path = args.run_dir / ".runner.lock"
    lock_handle = lock_path.open("w")
    try:
        fcntl.flock(lock_handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print(f"another depth runner already owns {lock_path}", file=sys.stderr)
        return 0

    runner = Runner(args.run_dir, dry_run=args.dry_run)
    try:
        return runner.run()
    except Exception as exc:
        runner.log(f"FATAL: {exc!r}")
        runner.write_status("fatal", error=repr(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
