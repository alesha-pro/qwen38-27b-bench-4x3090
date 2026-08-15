# Qwen3.8-27B-NVFP4 depth sweep on RTX 3090

Date: 2026-08-14

## Completion

- 72/72 scheduled points reached a terminal state: 54 successful measurements and 18 reproducible runtime failures.
- Hardware: 4x RTX 3090 (SM86), PCIe-only.
- vLLM 0.26.0, compiled mode and CUDA graphs; no run used `--enforce-eager`.
- Model context remained `max_model_len=262144` in every run.
- Matrix: TP 2/4, BF16/FP8 KV, MTP off/on, depths 8K/32K/64K/128K/254K.
- Single-stream was measured at every depth; concurrency 1/2/4/8/16 was measured at 8K.
- Each measurement generated 128 tokens. Prefix caching was disabled.

## Single-stream decode by context depth

Tokens per second after the first generated token:

| Configuration | 8K | 32K | 64K | 128K | 254K |
|---|---:|---:|---:|---:|---:|
| TP2, BF16 KV, no MTP | 58.56 | 52.77 | 46.66 | 40.17 | 27.26 |
| TP2, BF16 KV, MTP2 | 62.32 | 36.64 | 21.28 | 15.48 | 8.35 |
| TP2, FP8 KV, no MTP | 60.03 | 58.92 | 60.62 | 56.75 | 52.84 |
| TP4, BF16 KV, no MTP | 73.84 | 65.20 | 56.54 | 44.13 | 31.18 |
| TP4, BF16 KV, MTP2 | 73.50 | 33.90 | 23.28 | 13.59 | 7.88 |
| TP4, FP8 KV, no MTP | 76.68 | 76.26 | 77.25 | 77.77 | 74.85 |
| TP2/TP4, FP8 KV, MTP2 | failed | failed | failed | failed | failed |

Depth loss from 8K to 254K:

- TP2 BF16/no-MTP: -53.5%; TP2 FP8/no-MTP: -12.0%.
- TP4 BF16/no-MTP: -57.8%; TP4 FP8/no-MTP: -2.4%.
- BF16 MTP2: -86.6% on TP2 and -89.3% on TP4.

FP8 KV is the decisive long-context optimization. MTP is useful in the separate
short-prompt test, but its extra draft verification becomes strongly
counterproductive as the KV history grows.

## Single-stream prefill by context depth

Effective prompt tokens per second, computed as prompt tokens divided by TTFT:

| Configuration | 8K | 32K | 64K | 128K | 254K |
|---|---:|---:|---:|---:|---:|
| TP2, BF16 KV, no MTP | 1819.5 | 1454.4 | 1144.6 | 801.6 | 511.5 |
| TP2, FP8 KV, no MTP | 1900.7 | 1753.2 | 1577.6 | 1315.8 | 1001.8 |
| TP4, BF16 KV, no MTP | 814.5 | 836.4 | 783.8 | 690.8 | 558.3 |
| TP4, FP8 KV, no MTP | 823.9 | 874.4 | 860.8 | 822.3 | 744.4 |

At 254K, FP8 improves prefill by 1.96x on TP2 and 1.33x on TP4. TP2 has
substantially better prefill than TP4 on this PCIe topology. MTP does not
materially improve prefill.

At 254K, measured TTFT was 253.5 seconds for TP2/FP8 and 341.2 seconds for
TP4/FP8. TP4 then decodes faster (74.85 versus 52.84 tok/s), but TP4 only
recovers its TTFT deficit after roughly 15.7K generated tokens. For ordinary
responses, TP2/FP8 therefore has lower end-to-end latency and uses half as many
GPUs.

## Concurrency knee at 8K

With 8K prompts, concurrent prefills are staggered by chunked scheduling, so
wall-clock output throughput includes prefill and cannot be read as pure decode
capacity. Using the sum of active per-request decode rates as the closest
decode-only indicator:

- TP2 BF16/no-MTP peaks at c=4.
- TP2 FP8/no-MTP reaches a plateau at c=4 to c=8.
- TP4 BF16/no-MTP and TP4 FP8/no-MTP peak at c=4.
- MTP results are unstable/non-monotonic at depth and are not deployment candidates.

Aggregate prefill is effectively saturated by c=1 and changes little past c=4.
The separate short-prompt matrix remains the correct source for a pure decode
serving knee: TP2 continued scaling through c=16, while TP4's practical knee
was around c=8.

## Failures and context capacity

- `FP8 KV + MTP2` failed all nine scheduled points on both TP2 and TP4.
- The reproducible root error is FlashInfer
  `BatchPrefillWithPagedKVCache failed with error invalid resource handle`.
- This is specific to the combined vLLM 0.26.0 / FlashInfer 0.6.14 / MTP / FP8
  KV path on SM86. FP8 KV without MTP completed every depth and concurrency.
- TP2 BF16+MTP at GPU memory utilization 0.90 missed the 256K startup
  requirement by 0.01 GiB (8.73 GiB available versus 8.74 GiB required).
  It passed at 0.91 without reducing context length.

## Recommendation

1. Default long-context configuration: TP2 + FP8 KV + no MTP.
2. Use TP4 + FP8 KV + no MTP only when post-prefill single-stream decode speed
   matters more than TTFT and GPU efficiency.
3. For four-GPU aggregate serving, prefer two TP2 replicas over one TP4 replica;
   validate the dual-replica interference separately before production.
4. Keep MTP off for long context. Never combine MTP with FP8 KV on this runtime.
5. Keep `max_model_len=262144`, compiled mode, CUDA graphs, Marlin NVFP4, and
   PyNCCL/`--disable-custom-all-reduce` on this PCIe-only host.

Raw point JSON, `summary.json`, and `summary.csv` in this directory contain the
complete measurements, TTFT, prompt throughput, decode rates, and failure rows.
