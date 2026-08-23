#!/usr/bin/env python3
"""Quant ladder extension: 7 Unsloth Dynamic 3.0 GGUF quants + AutoRound W4A16.

Reuses run_quality_matrix.py verbatim (same BenchLocal invocation, same natural
reasoning contract, same telemetry proxy) and only adds model entries, so new
arms are directly comparable to the 2026-08-18 five-quant campaign.
"""

from __future__ import annotations

import sys
from pathlib import Path

HARNESS = Path("$RUN_ROOT/harness")
sys.path.insert(0, str(HARNESS))

import run_quality_matrix as base  # noqa: E402

UD3 = "$MODEL_ROOT/Qwen3.8-27B-GGUF-UD3"


def gguf_argv(path: str) -> list[str]:
    return [
        base.LLAMA,
        "--model", path,
        "--host", "127.0.0.1", "--port", str(base.TARGET_PORT),
        "--ctx-size", "262144", "--parallel", "1", "--cont-batching",
        "--no-cache-prompt", "--flash-attn", "on", "--gpu-layers", "999",
        "--split-mode", "layer", "--tensor-split", "1,1",
        "--threads", "18", "--threads-batch", "18",
        "--batch-size", "4096", "--ubatch-size", "1024",
        "--cache-type-k", "q8_0", "--cache-type-v", "q8_0",
        "--no-context-shift", "--jinja", "--reasoning", "auto",
        "--reasoning-budget", "-1", "--reasoning-format", "deepseek",
    ]


def gguf_model(filename: str) -> dict:
    path = f"{UD3}/{filename}"
    return {
        "engine": "llama.cpp",
        "weights": path,
        "context": 262144,
        "kv": "q8_0",
        "argv": gguf_argv(path),
        "env": {"CUDA_VISIBLE_DEVICES": "0,1"},
    }


AUTOROUND = "$MODEL_ROOT/Qwen3.8-27B-W4A16-AutoRound"
DFLASH2_ENV = "$VLLM_ENV"
VLLM_DFLASH2 = f"{DFLASH2_ENV}/bin/vllm"
DFLASH2_CUDA = f"{DFLASH2_ENV}/lib/python3.12/site-packages/nvidia/cu13"

# Verbatim from harness/vllm_arm.sh, the launcher that served this model in the
# 2026-08-20 speed run. FLASHINFER_SAMPLER=0 and the CCCL flag are load-bearing:
# without them FlashInfer JIT fails on this rig (nvcc 12.6 vs cu130 headers).
AUTOROUND_ENV = {
    "PATH": f"{DFLASH2_CUDA}/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
    "CUDA_VISIBLE_DEVICES": "0,1",
    "HF_HOME": "$HF_CACHE",
    "VLLM_CACHE_ROOT": "$VLLM_CACHE",
    "VLLM_USE_FLASHINFER_SAMPLER": "0",
    "CUDA_HOME": DFLASH2_CUDA,
    "NVCC_PREPEND_FLAGS": "-DCCCL_DISABLE_CTK_COMPATIBILITY_CHECK",
    "LD_LIBRARY_PATH": f"{DFLASH2_CUDA}/lib",
    "VLLM_SPEC_DECODE_ATTN": "1",
    "VLLM_SPEC_DECODE_ATTN_QMAX": "5",
    "VLLM_DFLASH2_LOOKUP": "1",
    "VLLM_V2_CUDAGRAPH_MEM_MIB": "1400",
    "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True",
}


def autoround_argv() -> list[str]:
    """The exact launch that served this model in the 2026-08-20 speed run.

    vLLM 0.26.0 in vllm-cross-kv-env cannot load the int8 pack-quantized
    embed_tokens from the syv-ai requantization recipe, and FlashInfer JIT is
    broken in this env, so this arm keeps the working stack verbatim: vLLM
    0.27.1, FLASH_ATTN, bf16 KV, DFlash2 n=4. Only the flags BenchLocal needs
    (tokenizer, tool parser) are added.
    """
    return [
        VLLM_DFLASH2, "serve", AUTOROUND,
        "--tokenizer", base.TOKENIZER,
        "--served-model-name", "bench",
        "--host", "127.0.0.1", "--port", str(base.TARGET_PORT),
        "--tensor-parallel-size", "2",
        "--max-model-len", "262144",
        "--max-num-seqs", "16",
        "--gpu-memory-utilization", "0.94",
        "--no-enable-prefix-caching",
        "--language-model-only",
        "--attention-backend", "FLASH_ATTN",
        "--kv-cache-dtype", "bfloat16",
        "--mamba-ssm-cache-dtype", "float16",
        "--max-num-batched-tokens", "2048",
        "--reasoning-parser", "qwen3",
        "--enable-auto-tool-choice",
        "--tool-call-parser", "qwen3_xml",
        "--trust-remote-code",
        "--compilation-config",
        '{"max_cudagraph_capture_size":80,"custom_ops":["+rms_norm","+silu_and_mul"]}',
        "--speculative-config",
        '{"method":"dflash","model":"$MODEL_ROOT/Qwen3.8-27B-DFlash2-W4A16",'
        '"num_speculative_tokens":4}',
        "--disable-custom-all-reduce",
    ]


LADDER = {
    "autoround-w4a16": {
        "engine": "vllm",
        "weights": AUTOROUND,
        "context": 262144,
        "kv": "bf16",
        "argv": autoround_argv(),
        "env": dict(AUTOROUND_ENV),
    },
    "ud-q4-k-xl": gguf_model("Qwen3.8-27B-UD-Q4_K_XL.gguf"),
    "ud-q4-k-m": gguf_model("Qwen3.8-27B-UD-Q4_K_M.gguf"),
    "ud-iq4-xs": gguf_model("Qwen3.8-27B-UD-IQ4_XS.gguf"),
    "ud-q3-k-xl": gguf_model("Qwen3.8-27B-UD-Q3_K_XL.gguf"),
    "ud-q2-k-xl": gguf_model("Qwen3.8-27B-UD-Q2_K_XL.gguf"),
    "ud-iq2-xxs": gguf_model("Qwen3.8-27B-UD-IQ2_XXS.gguf"),
    "ud-iq1-m": gguf_model("Qwen3.8-27B-UD-IQ1_M.gguf"),
}

base.MODELS.update(LADDER)

if __name__ == "__main__":
    raise SystemExit(base.main())
