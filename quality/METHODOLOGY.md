# Methodology

## Question

How much quality and reasoning behavior changes when the same Qwen3.8-27B
family checkpoint is served in five roughly deployment-relevant formats?
FP8 is treated as the reference, but every paired task result is retained so a
reader can audit regressions and fixes rather than infer quality from nominal
bits per weight.

## Hardware snapshot

- 4x NVIDIA RTX 3090, 24 GiB each, Ampere.
- Driver 610.43.02; reported CUDA compatibility 13.3.
- GPU power limit was 320 W per card at the campaign fingerprint.
- All GPU pairs were on PCIe `NODE` links; there is no NVLink.
- The full `nvidia-smi -q` and topology output are in `raw/fingerprints.json`.

Quality arms did not all use four GPUs. vLLM and llama.cpp used two cards per
server so two lanes could run concurrently; NInfer used one card. This dataset
compares model outputs, not inference speed, and latency must not be used as an
apples-to-apples engine benchmark.

## Artifacts and serving configurations

| Label | Pinned artifact | Engine | GPU layout | Context | KV cache |
|---|---|---|---:|---:|---|
| FP8 | `Qwen/Qwen3.8-27B-FP8@017b9c7a` | vLLM 0.26.0 | TP=2 | 262,144 | FP8 |
| NVFP4 | Unsloth Dynamic V3 preview, local HF revision `60e813d4` | vLLM 0.26.0, Marlin | TP=2 | 262,144 | FP8 |
| AWQ INT4 | `cyankiwi/Qwen3.8-27B-AWQ-INT4@63768c10` | vLLM 0.26.0, Marlin | TP=2 | 262,144 | FP8 |
| GGUF Q4_K_M | `unsloth/Qwen3.8-27B-GGUF@430473d9`, Q4_K_M file | llama.cpp build 10013 | 2-GPU layer split | 262,144 | Q8_0 K/V |
| NInfer | `neroued/Qwen3.8-27B-NInfer@35269130` | NInfer `7d715ccd` | 1 GPU | 187,300 | INT8 |

NInfer's 187,300-token context is the largest verified capacity that fit this
single-GPU configuration. It is a physical KV-fit ceiling, not a reasoning
budget. Exact executable argv is in each `server-launch.json`.

Artifact file sizes captured by the campaign were 30.89 GB (FP8), 23.44 GB
(NVFP4), 21.04 GB (AWQ), 17.11 GB (GGUF), and 18.21 GB (NInfer). These are whole
artifact sizes, not clean effective BPW: they include different unquantized
components, metadata, and in some cases MTP or multimodal pieces.

## Benchmark harness

- BenchLocal base commit: `3e677be357b79a2e4380a246e6d4399fd1a80c5c`.
- Campaign patch SHA-256: `8b5ad53bd94bf10bc3720613a9485296c2e1e4ad2d00842a7dadad3c01e5ab43`.
- The patched worktree added natural-reasoning controls, token metrics,
  incremental persistence, strict reasoning validation, and Hermes fallback
  propagation. The complete patch and runner are in `raw/harness/`.
- The Hermes image fix was validated with 412 passing tests; immutable evidence
  is in `raw/harness/hermes-fallback-validation.json`.

The proxy sat between BenchLocal/sandbox agents and each OpenAI-compatible
server. It recorded every request and original JSON or SSE response, including
hidden calls made inside CLI and Hermes loops. The runner separately retained
the scored scenario response and verifier trace.

## Matrix and scoring

- `full`: 150 scenarios from eight deterministic/sandboxed BenchLocal packs.
- `reasoning`: 30 HumanEval+, 30 LiveCodeBench v6, and 30 GSM-Symbolic cases.
- GPQA-Diamond remained gated and contributed zero rows.
- Efforts: `off`, `low`, `medium`, `xhigh`.
- 5 artifacts x 4 efforts x 2 suites = 40 arms.
- Pass@1 is authoritative. A failed scenario could receive verifier-owned retry
  attempts; Pass@k is retained only as a stability diagnostic.
- Pack-default sampling was preserved. Most thinking packs used Qwen's
  recommended temperature-1 sampler; Hermes retained its pack-level greedy
  default. Do not interpret one- or two-case gaps as deterministic.

`full` and `reasoning` are separate views and are not added into one 240-case
score because their skills and workload shapes overlap.

## Natural reasoning contract

For `low`, `medium`, and `xhigh` arms, the intended contract was:

- no request-level `max_tokens` or forced reasoning-token budget;
- `--thinking-max-tokens 0`;
- `--model-turn-timeout 0`;
- `--timeout-ceiling-s 0`;
- effort communicated as model control, not translated into a token quota;
- endpoint context/KV capacity is the only generation ceiling.

The runner did have a one-day scenario watchdog (`--timeout-per-case 86400`) so
an abandoned sandbox could not live forever. No accepted scenario hit it. Off
arms used each pack's ordinary answer cap and were required to emit zero
reasoning. Three FP8/full arms have retained contract exceptions; see
`CAVEATS.md` rather than silently treating them as clean.

## Token accounting

API-reported prompt/completion/reasoning usage is used when present. Otherwise,
the campaign's pinned Qwen tokenizer reconstructs reasoning, final-answer, and
tool-call token counts from the proxy response. `per-request.csv` exposes both
reported and reconstructed values plus a `reasoning_source` column.

Task totals in `per-scenario.csv` include direct and hidden model calls. This is
why they are the right values for “how much reasoning did the model spend to
solve this task?” rather than the direct response's usage alone.

## Reproduction entrypoints

The exact orchestrator is `raw/harness/run_quality_matrix.py`. After replacing
the documented `$PLACEHOLDERS` with local paths, its effective BenchLocal arm
was equivalent to:

```bash
benchlocal-cli run --full \
  --enable-thinking --reasoning-effort xhigh \
  --thinking-max-tokens 0 \
  --timeout-per-case 86400 --timeout-ceiling-s 0 \
  --model-turn-timeout 0 --strict-thinking \
  --incremental --save-json result.json \
  --endpoint http://127.0.0.1:19081/v1 --model bench
```

Replace `--full` with `--reasoning-packs`; replace thinking controls with
`--no-thinking` for the off arm. Do not copy this abbreviated command instead
of the runner when reproducing the full dataset: the runner also pins tokenizer,
sandbox logs, history, telemetry session headers, ports, and launch lifecycle.
