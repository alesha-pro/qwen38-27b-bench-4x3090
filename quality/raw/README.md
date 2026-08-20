# Qwen3.8-27B quant quality matrix

Quality comparison of five weight formats on the same 4x RTX 3090 rig with
BenchLocal `full` and `--reasoning-packs` suites.

## Matrix

- Models: FP8 reference, NVFP4, AWQ INT4, GGUF Q4_K_M, NInfer.
- Reasoning efforts: `off`, `low`, `medium`, `xhigh`.
- Suites: `full` (150 scenarios) and `reasoning` (90 runnable scenarios).
- 40 independent arms, run sequentially.
- Pass@1 is authoritative. Failure-only retries are retained as pass@3
  diagnostics and never replace pass@1.
- Pack-default sampling is preserved.

## Natural reasoning contract

- Thinking arms send no `max_tokens` or other generated-token budget.
- No benchmark timeout or model-turn timeout is imposed.
- `off` uses the pack's ordinary answer cap, but must emit zero reasoning.
- vLLM and llama.cpp use the model's native 262,144-token context.
- NInfer uses 187,300 tokens, the largest verified capacity that fits its
  single-GPU INT8 KV implementation on this RTX 3090. This is a physical fit
  limit, not a benchmark reasoning budget.
- Every arm runs with strict thinking validation. A proxy independently records
  every request/response, including calls made inside Hermes/Aider agents.

## Per-task telemetry

The patched runner stores reported API usage and tokenizer-reconstructed
reasoning, answer, and tool-call tokens. The lossless proxy covers hidden
agentic calls and preserves the original JSON/SSE response.

Final analysis emits:

- `per-scenario.csv`: verdict, attempts, latency, and total tokens spent solving
  each task across every model call.
- `per-request.csv`: one row for every direct or hidden model call.
- `per-arm.csv` and `per-pack.csv`: dense aggregates and validity audits.
- `paired-vs-fp8.csv`: matched task flips plus exact McNemar p-values.
- `paired-effort-vs-off.csv`: matched quality changes from reasoning.
- `SUMMARY.json` and `SUMMARY.md`: machine- and human-readable rollups.

## Rejected preflight data

The first FP8/off attempt exposed an upstream Hermes fallback bug: after the
tool-loop limit, its direct summary request bypassed `request_overrides` and
silently enabled reasoning. Those incomplete results were stopped and moved to
the remote `rejected/fp8-off-contaminated-before-hermes-fallback-fix` directory.

The fallback was patched to inherit the exact thinking controls, the Hermes
sandbox was rebuilt, all 412 BenchLocal tests passed, and live validation
confirmed:

- off fallback: 9 calls, zero calls with reasoning;
- low: reasoning on, `reasoning_effort=low`, zero calls with `max_tokens`;
- medium: reasoning on, 192 reconstructed reasoning tokens, no `max_tokens`;
- xhigh: reasoning on, 258 reconstructed reasoning tokens, no `max_tokens`.

See `harness/hermes-fallback-validation.json` for the immutable image/patch
fingerprints and smoke evidence.
