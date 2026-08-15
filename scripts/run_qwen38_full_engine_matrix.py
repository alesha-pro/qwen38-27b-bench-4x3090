#!/usr/bin/env python3
"""Reboot-safe orchestrator for the Qwen3.8 NVFP4/FP8 depth matrices.

Order is intentional: validate the local SGLang Ampere fork on NVFP4 first,
then run the same point set for the FP8 checkpoint on vLLM and SGLang.  Each
child runner is itself resumable at the individual point level.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output" / "qwen38-full-engine-matrix"
STATUS = OUTPUT / "status.json"
LOG = OUTPUT / "orchestrator.log"
RUNNER = ROOT / "run_vllm_depth_autonomous.py"

NVFP4_MODEL = Path("$MODELS/Qwen3.8-27B-NVFP4")
FP8_MODEL = Path("$MODELS/Qwen3.8-27B-FP8")
SGLANG_PYTHON = Path("$ENGINES/sglang-nvfp4-env/bin/python")
VLLM_PYTHON = Path("$ENGINES/vllm-cross-kv-env/bin/python")


STAGES = [
    {
        "name": "sglang-nvfp4",
        "engine": "sglang",
        "model": NVFP4_MODEL,
        "python": SGLANG_PYTHON,
        "run_dir": ROOT / "output" / "sglang-depth-autonomous-qwen38-nvfp4",
        "gpu_memory": "0.90",
        "mtp_name": "mtp4",
    },
    {
        "name": "vllm-fp8",
        "engine": "vllm",
        "model": FP8_MODEL,
        "python": VLLM_PYTHON,
        "run_dir": ROOT / "output" / "vllm-depth-autonomous-qwen38-fp8",
        "gpu_memory": "0.91",
        "mtp_name": "mtp2",
    },
    {
        "name": "sglang-fp8",
        "engine": "sglang",
        "model": FP8_MODEL,
        "python": SGLANG_PYTHON,
        "run_dir": ROOT / "output" / "sglang-depth-autonomous-qwen38-fp8",
        "gpu_memory": "0.90",
        "mtp_name": "mtp4",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + f".tmp-{os.getpid()}")
    with tmp.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, path)


def log(message: str) -> None:
    line = f"[{now()}] {message}"
    print(line, flush=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def checkpoint_problem(model: Path) -> str | None:
    if not (model / "config.json").is_file():
        return "config.json is absent"
    incomplete = sorted(model.rglob("*.incomplete"))
    if incomplete:
        return f"download still has {len(incomplete)} incomplete file(s)"
    index_files = sorted(model.glob("*.safetensors.index.json"))
    for index_path in index_files:
        try:
            index = json.loads(index_path.read_text(encoding="utf-8"))
            shards = {str(value) for value in index.get("weight_map", {}).values()}
        except (OSError, json.JSONDecodeError) as exc:
            return f"cannot parse {index_path.name}: {exc}"
        missing = sorted(name for name in shards if not (model / name).is_file())
        if missing:
            return f"{index_path.name} references {len(missing)} missing shard(s)"
    if not list(model.glob("*.safetensors")):
        return "no safetensors files found"
    return None


def wait_for_checkpoint(stage: dict[str, Any]) -> None:
    model = stage["model"]
    while True:
        problem = checkpoint_problem(model)
        if problem is None:
            return
        log(f"waiting for {stage['name']} checkpoint: {problem}")
        atomic_json(
            STATUS,
            {
                "state": "waiting-for-checkpoint",
                "stage": stage["name"],
                "model": str(model),
                "detail": problem,
                "updated_at": now(),
            },
        )
        time.sleep(60)


def stage_env(stage: dict[str, Any]) -> dict[str, str]:
    env = os.environ.copy()
    for key in (
        "CONFIG_FILTER",
        "WEIGHT_QUANTIZATION",
        "ENGINE_PYTHON",
        "VLLM_PYTHON",
        "VLLM_BIN",
        "SGLANG_BIN",
    ):
        env.pop(key, None)
    env.update(
        {
            "ENGINE": stage["engine"],
            "MODEL": str(stage["model"]),
            "RUN_DIR": str(stage["run_dir"]),
            "MTP_NAME": stage["mtp_name"],
            "SWEEP_PROFILE": "fast",
            "DEPTHS": "8192,32768,65536,131072,253952",
            "CONCURRENCIES": "1,2,4,8,16",
            "GEN_TOKENS": "128",
            "CONFIG_WARMUPS": "1",
            "CONFIG_WARMUP_CONCURRENCIES": "1",
            "DEPTH_WARMUPS": "0",
            "GPU_MEMORY_UTILIZATION": stage["gpu_memory"],
            "MAX_POINT_ATTEMPTS": "1",
            "SERVER_START_ATTEMPTS": "2",
            "SERVER_START_TIMEOUT_S": "1800",
            "SGLANG_PREFILL_GRAPH_MAX_TOKENS": "256",
            "PORT": "18081",
            "PYTHONUNBUFFERED": "1",
        }
    )
    return env


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for index, stage in enumerate(STAGES, start=1):
        wait_for_checkpoint(stage)
        atomic_json(
            STATUS,
            {
                "state": "running",
                "stage_index": index,
                "stage_count": len(STAGES),
                "stage": stage["name"],
                "engine": stage["engine"],
                "model": str(stage["model"]),
                "run_dir": str(stage["run_dir"]),
                "updated_at": now(),
            },
        )
        command = [str(stage["python"]), str(RUNNER)]
        log(f"starting stage {index}/{len(STAGES)} {stage['name']}")
        completed = subprocess.run(command, cwd=ROOT, env=stage_env(stage))
        log(f"stage {stage['name']} exited rc={completed.returncode}")
        if completed.returncode != 0:
            atomic_json(
                STATUS,
                {
                    "state": "stage-retry-needed",
                    "stage_index": index,
                    "stage_count": len(STAGES),
                    "stage": stage["name"],
                    "returncode": completed.returncode,
                    "updated_at": now(),
                },
            )
            return completed.returncode

    completed_at = now()
    atomic_json(
        STATUS,
        {
            "state": "complete",
            "stage_count": len(STAGES),
            "completed_at": completed_at,
            "run_dirs": [str(stage["run_dir"]) for stage in STAGES],
        },
    )
    (OUTPUT / "DONE").write_text(completed_at + "\n", encoding="utf-8")
    log("all benchmark stages complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
