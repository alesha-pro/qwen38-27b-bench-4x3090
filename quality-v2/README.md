# Qwen3.8-27B quant quality, run v2

A second, independent quality campaign on Qwen3.8-27B. The earlier one lives in
[`../quality/`](../quality/) and is kept as it was. This run answers a narrower
question with a stricter protocol: how far can you compress this model before
the answers get worse, and how does the answer change with the thinking budget.

Eight quantizations from 8 bit down to 1.8, plus a BF16 reference, on the same
300 frozen tasks. Every raw response, every reasoning trace, the frozen pool,
the scorer and the analysis code are in this folder.

## Headline

Pass rate at maximum thinking effort, paired against the BF16 reference:

| Artifact | Bits/weight | Pass rate | vs BF16 | 95% CI | p |
|---|---|---|---|---|---|
| BF16 reference | 16 | 80.3% | | | |
| FP8 | 8 | 81.3% | +1.0 pp | [-1.9, +3.9] | 0.49 |
| GGUF Q6_K_M | 6.5 | 80.8% | +0.4 pp | [-2.3, +3.1] | 0.76 |
| AWQ INT4 | 4.25 | 81.4% | +1.1 pp | [-1.0, +3.2] | 0.31 |
| AutoRound W4A16 | 4.25 | 81.9% | +1.6 pp | [-0.8, +4.0] | 0.19 |
| GGUF Q4_K_XL | 4.8 | 79.6% | -0.7 pp | [-3.0, +1.6] | 0.58 |
| GGUF Q3_K_XL | 3.6 | 79.9% | -0.4 pp | [-3.3, +1.3] | 0.79 |
| GGUF Q2_K_XL | 2.7 | 79.4% | -0.9 pp | [-4.2, +1.1] | 0.54 |
| **GGUF IQ1_M** | **1.8** | **43.0%** | **-37.3 pp** | **[-42.5, -33.1]** | **<0.0001** |

Seven of the eight are inside the noise of the reference. The eighth is not a
degradation, it is a different model. There is no intermediate step between
2.7 bits and 1.8 bits in this data.

## The thinking budget matters more than the quant

Same tasks, same BF16 weights, only the effort knob changes:

| Effort | Pass rate |
|---|---|
| off | 61.3% |
| low | 72.0% |
| medium | 73.0% |
| max | 80.3% |

Twenty points separate `off` from `max`. No quantization in this study moved
the number by more than three. The full effort matrix for every artifact is in
[`RESULTS.txt`](RESULTS.txt).

## How IQ1_M breaks

The 1.8 bit model does not lose ability uniformly. Difference against the
reference by task family, maximum effort:

| Family | Delta |
|---|---|
| Reasoning puzzles | -44.0 pp |
| Instruction following | -47.8 pp |
| Math | -43.8 pp |
| Tool calling | -17.1 pp |

Tool calling degrades least. Selecting the right function from a schema
survives compression that removes most of the reasoning ability.

## Two findings that are easy to miss

**Q2_K_XL only shows damage at a short thinking budget.** At maximum effort it
is 0.9 points below the reference and indistinguishable from it. At `low` it
loses 8.0 points with p=0.003. A long reasoning chain compensates for the
damage; cut the budget and the damage appears.

**One result was an artifact of the engine, not the model.** Q6_K_M first came
out significantly ahead of the reference, driven by the instruction following
block (+9.4 pp, p=0.011). llama.cpp strips the newline that follows the
thinking block and vLLM does not, and part of the instruction suite checks for
whitespace in the answer. All vLLM and API arms had a leading newline in 100%
of those answers, llama.cpp in 0%. Normalizing the scorer removed the effect.
Both corrections are recorded in [`PRE-REGISTRATION.md`](PRE-REGISTRATION.md).

## Two 2 bit builds: Mirai S and Bonsai 2 (added 2026-09-28)

Two more arms on the same 300 tasks and the same protocol:

- `quant-mirai-s`: trymirai Mirai S, 2.4 bits/weight, on Mirai's vLLM plugin.
- `quant-bonsai2-pq2`: PrismML Bonsai 2 PQ2_0, 2.13 bits/weight, on PrismML's
  llama.cpp fork `prism-b10743-adfffbe`.

| Arm | off | low | medium | xhigh | xhigh vs BF16 |
|---|---|---|---|---|---|
| Mirai S | 60.3% | 68.0% | 70.0% | 78.4% | -1.9 pp [-4.4, +0.7] p=0.18 |
| Bonsai 2 PQ2_0 | 58.0% | 75.3% | 69.3% | 78.0% | -2.3 pp [-5.4, +0.7] p=0.15 |

Both are inside the noise of the reference at max effort, and Bonsai minus
Mirai is -0.4 pp (p=0.82). Bonsai's `low` behaves like `xhigh`, as its model
card warns. The Bonsai xhigh arm is partial: 211 tasks with 2 repeats, 72 with
1, 17 with 3. Full matrix and per-block deltas in
[`TWO-BIT-RESULTS.txt`](TWO-BIT-RESULTS.txt), engine logs in `logs/`,
launch scripts `harness/run-mirai-s.sh` and `harness/run-bonsai.sh`.

The same two builds separate in agent loops (AppWorld 89.9 vs 64.3). That run
is in [`../agentic-v1/`](../agentic-v1/).

## Protocol

- 300 frozen tasks, sha256 manifest, in [`pool/allpool.jsonl`](pool/allpool.jsonl).
  Composition: 120 reasoning-gym puzzles, 84 BFCL tool calls, 69 IFBench
  instruction-following cases, 27 MathArena problems.
- Four effort levels per artifact: `off`, `low`, `medium`, `xhigh`.
- `xhigh` repeated 3 times per task for FP8, Q6, AWQ, AutoRound, Q3 and the
  reference; 2 times for Q4, Q2 and IQ1_M. The per-task outcome is the mean of
  the available repeats.
- `max_tokens` 131072 everywhere. Identical sampling per effort level.
- Analysis written before the results were read. Primary estimand is the mean
  over tasks of (quant rate minus reference rate), with no selection of tasks
  by either arm's outcome. Paired bootstrap CI and a sign-flip permutation test,
  20000 resamples, ties counted against the effect.
- Generations that died on the provider or on a client timeout are treated as
  missing data, never as model failures. `finish_reason == "length"` is a model
  failure and counts as one.

## Hardware and engines

BF16 reference through OpenRouter pinned to a single BF16 provider. FP8, AWQ
and AutoRound on vLLM 0.23.0. All GGUF artifacts on llama.cpp at commit
`885c5bbe`, 16 slots, unified KV pool. Arms ran on a 4x RTX 3090 rig at 220 W
per card and on rented single RTX PRO 6000 Blackwell cards. The same artifact
measured on both (AWQ INT4) differs by 1.2 pp with p=0.23, so the hardware
split is below the resolution of this study.

## Layout

```
arms/       raw responses, one JSON per task per effort per repeat, plus scored.jsonl
logs/       engine and driver logs
pool/       the 300 frozen tasks
harness/    request builder, runner, scorer, analysis
RESULTS.txt full effort matrix, per-block deltas
PRE-REGISTRATION.md   the plan, and both corrections made to it
```

## Reproducing a number

```bash
python3 harness/paired_diff.py --ref ref-final ref-ext --quant quant-iq1m --label IQ1_M
```

## Limits

The pool is 300 tasks, so the resolution is roughly 2 to 3 points. Differences
smaller than that are invisible here, and "no measurable difference" is not the
same claim as "no difference". Every task is single-turn: the model answers
once and is scored. Nothing in this dataset says how these quants behave inside
a multi-step agent loop, where per-step errors compound.
