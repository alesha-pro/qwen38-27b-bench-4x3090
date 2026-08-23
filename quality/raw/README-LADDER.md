# Quant ladder extension, 2026-08-20

Adds eight weight formats to the five-quant campaign in this directory: the
seven Unsloth Dynamic 3.0 GGUF quants and the AutoRound W4A16 build from the
syv-ai recipe. Same BenchLocal harness, same natural reasoning contract, same
telemetry proxy, so arms are comparable to the 2026-08-18 matrix.

Runner: `harness/run_ladder.py`. It imports `run_quality_matrix.py` and only
adds model entries, so the benchmark invocation itself is unchanged.

## Matrix

- Models: `autoround-w4a16`, `ud-q4-k-xl`, `ud-q4-k-m`, `ud-iq4-xs`,
  `ud-q3-k-xl`, `ud-q2-k-xl`, `ud-iq2-xxs`, `ud-iq1-m`.
- Efforts: `low`, `medium`, `xhigh`. `off` is dropped: the first campaign
  already showed it loses six to nine points on every format, so it answers no
  open question here.
- Suites: `full` (150 scenarios) and `reasoning` (90).
- 48 arms across two lanes.

## Lanes

Two GPUs per lane, both running at once.

| Lane | Root | GPUs | Suite | Ports |
|---|---|---|---|---|
| A | `ladder-full/` | 0,1 | full | 18091 / 19091 |
| B | `ladder-reasoning/` | 2,3 | reasoning | 18092 / 19092 |

Model order is identical in both lanes and starts with AutoRound, the format
under consideration for daily driving.

Lane B carries the heavier half: reasoning arms ran roughly 1.6x longer than
full arms in the first campaign. When lane A drains, its remaining capacity
gets the tail of lane B's model list. The runner skips completed arms, so a
handoff is a plain restart with the remaining models.

## Engines

Seven GGUF arms use the same llama.cpp server as the original
`gguf-q4-k-m` arm: 262,144 context, q8_0 KV, `--split-mode layer
--tensor-split 1,1`, natural reasoning with `--reasoning-budget -1`.

The AutoRound arm does not use `vllm-cross-kv-env`. That build is vLLM 0.26.0
and cannot load the int8 pack-quantized `embed_tokens` this recipe produces:

    ValueError: There is no module or parameter named
    'embed_tokens.weight_packed' in Qwen3_5Model

So the arm keeps the exact stack that served this model in the same-day speed
run (`Qwen3.8-27B-dailydriver-2026-08-20`): vLLM 0.27.1 from
`vllm-dflash2-w4a16-env`, FLASH_ATTN, bf16 KV, DFlash2 n=4, plus
`VLLM_USE_FLASHINFER_SAMPLER=0` and
`NVCC_PREPEND_FLAGS=-DCCCL_DISABLE_CTK_COMPATIBILITY_CHECK`. Both env vars are
load-bearing: FlashInfer JIT fails on this rig without them, which is what
killed two earlier launch attempts.

Deltas to record when reading results against the first campaign: vLLM 0.27.1
rather than 0.26.0, FLASH_ATTN rather than FLASHINFER, and bf16 KV rather than
fp8 KV. The bf16 KV cache is the more accurate one, so it is a small tailwind
for AutoRound rather than a handicap. It is also what the daily-driver config
would actually run, which is the question this arm exists to answer.

Speculative decoding stays on for that arm. DFlash2 verifies every drafted
token against the target model, so it changes throughput, not output.

## Preflight

Every model was loaded and asked one question before the campaign started.
All eight answered. One note carried forward: `ud-iq1-m` leaked a closing
think tag into its answer channel on the smoke prompt. If its arms fail strict
thinking validation, that is a result about 1-bit quantization, not a harness
fault, and should be reported rather than repaired.

## Analysis

Each lane runs the analyzer over its own root at the end, which will report a
missing FP8 baseline. That is expected. The authoritative pass is a single
analyzer run over a merged tree containing both the first campaign and this
one, as `combined-results/` was built for the first five quants.
