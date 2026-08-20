# Caveats and retained anomalies

These are part of the dataset, not footnotes to hide after publishing.

## Three FP8/full arms violate the strict control contract

The combined table marks these rows `Valid=NO`:

- **FP8 off/full**: one of 387 analyzed model calls emitted 179 reconstructed
  reasoning tokens. The other off arms and FP8 off/reasoning stayed silent.
- **FP8 low/full**: one call retained a request `max_tokens` field. It did not
  finish with `length`.
- **FP8 medium/full**: 88 retained calls across 21 tasks still carried an older
  request cap. None finished with `length`. CLI-20, the only observed capped
  runaway, was repaired with one uncapped request; its score remained a fail.

Therefore the FP8 reference is not a perfectly clean natural-reasoning control
for those three `full` rows. The absence of `finish_reason=length` makes score
damage unlikely for the retained capped calls, but it does not erase the
methodology violation. Raw pre/post CLI-20 artifacts and hashes are under
`raw/repair-fp8-medium-cli20-20260820/`.

## Repaired and interrupted arms

- AWQ medium/reasoning and NVFP4 low/reasoning contain targeted GSM-Symbolic
  repairs after interrupted resumes. The merged results retain warnings and
  provenance.
- FP8 medium/full and NVFP4 off/full retain sandbox-start warnings from an
  earlier interrupted pass even though the canonical merged results contain
  all 150 expected scenarios.
- The first FP8/off preflight was stopped because a Hermes iteration-limit
  fallback bypassed no-thinking overrides. It is under `raw/rejected/` and is
  not included in any score. The fix and validation evidence are public.

The current aggregate contains 10,118 request rows rather than the original
10,120 because three old FP8 medium CLI-20 calls were replaced by one uncapped
canonical call. The three originals remain in the repair backup, so no forensic
data was discarded.

## Pass@k is not a ranking metric

Only failed scenarios were eligible for inline retry. Some repaired arms have
partial retry denominators, so Pass@k totals are not always 150 or 90. Use
Pass@1 for quality and use Pass@k only to identify flaky/systematic failures.

## Effort labels are controls, not equal token budgets

`low`, `medium`, and `xhigh` were sent as model reasoning controls. They were not
translated into fixed token quotas and are not guaranteed to be calibrated
identically across vLLM, llama.cpp, and NInfer parsers. The telemetry proves
that reasoning appeared and records how much, but the label itself is not a
portable unit of compute.

## Engine and KV format are confounders

This is a deployment-artifact comparison, not a pure weight-only ablation:

- FP8/NVFP4/AWQ used vLLM with FP8 KV and TP=2.
- GGUF used llama.cpp with Q8_0 K/V cache and a two-GPU layer split.
- NInfer used INT8 KV on one GPU and a smaller physical context ceiling.
- Parsers and tool-call extraction differed by engine.

A task flip can come from weights, quant recipe, KV precision, sampler/parser,
or engine behavior. That is useful for choosing a real setup, but not proof that
weight quantization alone caused the difference.

## Statistical limits

Each scenario has one authoritative Pass@1 sample. Thinking uses non-greedy
sampling, so one-case gaps can move on a rerun. Use paired flips and McNemar
p-values; do not claim that 134/150 is universally better than 133/150.
The unusually weak NVFP4 off/reasoning result (70/90) is preserved as measured,
not silently smoothed or replaced.

## Suite and provenance limits

- GPQA-Diamond was gated and contributed no data.
- `full` and `reasoning` overlap in capability and must remain separate.
- HumanEval+ and LiveCodeBench upstream datasets have moved since the vendored
  30-case projections. Reproduce against the included scenario data and pinned
  artifacts, not today's upstream head.
- Raw requests embed third-party benchmark prompts. Their upstream licenses and
  attribution remain in force; see `ATTRIBUTION.md`.
