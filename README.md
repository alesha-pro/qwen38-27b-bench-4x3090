# Qwen3.8-27B benchmarks on 4x RTX 3090: speed, quality, raw traces

Shared by @superalesha. Everything here comes from the release day runs on
2026-08-14 and 15. llama.cpp GGUF sweeps started a few hours after the weights
hit HF, the 288 point engine matrix (vLLM vs SGLang, NVFP4 vs FP8 weights)
finished the next evening.

The `quality/` dataset adds a second campaign from 2026-08-18 through 20:
five quantizations, four reasoning-effort settings, two BenchLocal suites,
4,800 scenario-arm results, 10,118 model calls, and the full request/response
telemetry including extracted reasoning traces.

The quant ladder extension (2026-08-20 through 23) pushes the same quality
suites down the bit ladder: seven Unsloth Dynamic GGUF quants from Q4_K_XL to
IQ2_XXS plus AutoRound W4A16, 79 arms total, 235 hours of model time, 30.9M
generated tokens. Raw traces in `quality/raw/ladder-full/` and
`quality/raw/ladder-reasoning/`, findings (runaway generations at 2 bit, the
timeout cascade that almost faked a collapse) in `quality/raw/RUNAWAY-NOTE.md`.

## Setup

| Item | Value |
|---|---|
| GPUs | 4x RTX 3090 (24 GB each), PCIe, no NVLink, power limit 320 W per card |
| CPU | AMD EPYC 7642 |
| Engines | llama.cpp b10428 (885c5bbe8), vLLM 0.26.0, SGLang dev g22dde1dd5 (2026-08-14) |
| Model | Qwen3.8-27B dense, 27.3B params |
| Weights | GGUF Q4_K_M / Q5_K_M / Q6_K, NVFP4 (Marlin), FP8 |
| Context | up to 262144 in the engine matrix, CUDA graphs on, no eager mode |
| Measure | 128 generated tokens per point, prefix caching off, temp 0.7 |

## Layout

- `QWEN38-FULL-COMPARISON.md`: the merged engine matrix report, start here
- `qwen38-full-comparison.csv`: same data, machine readable
- `RESULTS-LLAMACPP-GGUF.md`: llama.cpp day one report (Q4/Q5/Q6 depth sweeps,
  in-GGUF MTP, max context per quant)
- `quality/README.md`: quality/reasoning matrix, raw responses, per-request token
  accounting, exact methodology, caveats, and trace-inspection tools
- `engine-matrix/`: four autonomous suites (vLLM/SGLang x NVFP4/FP8), per point
  JSON, launch manifests, server logs, summaries
- `llamacpp-gguf/`: llama-bench and llama-server raw runs
- `scripts/`: the harness that produced all of it
- `scripts/verify-headline.log`: the recheck that killed one headline number.
  The 84 tok/s MTP cell at 254K was a short window fluke, long generations land
  at ~75, same as no-MTP.

## Notes

- Local paths and the LAN address are replaced with `$VARIABLES`. Nothing else
  in the raw files was edited.
- MTP cells use 128 token generations, acceptance swings between prompts, so
  the depth curves for MTP are noisy. Read the caveats in the reports before
  quoting a single cell.
- Missing points in the FP8 weight suites are capacity limits (model plus
  BF16 KV does not fit at 262K), not crashes.
