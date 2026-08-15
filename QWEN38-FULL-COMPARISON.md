# Qwen3.8-27B: vLLM vs SGLang, NVFP4 vs FP8

Hardware: 4x RTX 3090 (Ampere SM86, PCIe-only). All servers used a 262,144-token context with CUDA graphs enabled; no run used eager mode. The matrix covers TP2/TP4, BF16/FP8 KV, MTP off/on, five context depths, and concurrency 1/2/4/8/16 at 8K. Each request generated 128 tokens.

## Completion

| Engine | Weights | Points | OK | Failed | Raw suite |
|---|---|---|---|---|---|
| vLLM | NVFP4 | 72 | 72 | 0 | `vllm-depth-autonomous-qwen38-nvfp4` |
| SGLang | NVFP4 | 72 | 71 | 1 | `sglang-depth-autonomous-qwen38-nvfp4` |
| vLLM | FP8 | 72 | 54 | 18 | `vllm-depth-autonomous-qwen38-fp8` |
| SGLang | FP8 | 72 | 53 | 19 | `sglang-depth-autonomous-qwen38-fp8` |

## Practical conclusions

- Best overall long-context stack on this host: **NVFP4 weights + vLLM + FP8 KV**. At 254K, no-MTP decode is 52.84 tok/s on TP2 and 74.85 tok/s on TP4; enabling MTP raises the measured points to 64.39 and 84.26 tok/s respectively.
- Pick **TP2** when TTFT, GPU efficiency, or running two replicas matters. For NVFP4/vLLM/FP8-KV at 254K it prefills at 1001.8 tok/s versus 744.4 tok/s on TP4. Pick **TP4** when post-prefill single-stream decode is the priority.
- FP8 KV is essential for vLLM at depth. With NVFP4/no-MTP, switching BF16 KV to FP8 KV changes 254K decode from 27.26 to 52.84 tok/s on TP2 and from 31.18 to 74.85 tok/s on TP4. It also prevents most long-context capacity failures.
- SGLang is competitive and has faster TP4 prefill than vLLM in several BF16-KV cases, but its best NVFP4 254K decode here is 67.60 tok/s with BF16-KV/MTP or 65.69 tok/s with FP8-KV/MTP, below vLLM's 84.26 tok/s.
- The FP8-weight checkpoint is slower than NVFP4 in the clean no-MTP/FP8-KV comparison: at 254K it trails by about 21.5%/14.9% in vLLM TP2/TP4 and 14.4%/9.6% in SGLang TP2/TP4. It also has more TP2 capacity failures.
- MTP results use only 128 generated tokens and acceptance varies by prompt, so the irregular depth curves are real measurements but noisy. MTP with FP8 KV is promising; MTP with BF16 KV is a poor vLLM long-context choice.
- At 8K, literal shared-window aggregate decode usually peaks at c=1 in vLLM and c=2 in SGLang because long prefills stagger entry into decode. The decode-only active-rate diagnostic generally plateaus around c=4-8 for vLLM TP4 and c=2-4 for SGLang TP4; TP2 can keep scaling to c=8-16.
- The 38 remaining failures are capacity limits, not crashes: FP8 weights with BF16 KV do not fit vLLM TP2 at a 262,144-token model length; SGLang FP8-weight TP2 cannot fit MTP, and two TP2/BF16-KV configurations miss only the 254K request.

## Single-stream decode by depth

Values are median steady decode tokens/s after the first generated token.

### vLLM / NVFP4

| Configuration | 8K | 32K | 64K | 128K | 254K |
|---|---|---|---|---|---|
| TP2 / BF16 KV / no-MTP | 58.56 | 52.77 | 46.66 | 40.17 | 27.26 |
| TP2 / BF16 KV / MTP | 62.32 | 36.64 | 21.28 | 15.48 | 8.35 |
| TP2 / FP8 KV / no-MTP | 60.03 | 58.92 | 60.62 | 56.75 | 52.84 |
| TP2 / FP8 KV / MTP | 63.64 | 70.17 | 75.13 | 75.28 | 64.39 |
| TP4 / BF16 KV / no-MTP | 73.84 | 65.20 | 56.54 | 44.13 | 31.18 |
| TP4 / BF16 KV / MTP | 73.50 | 33.90 | 23.28 | 13.59 | 7.88 |
| TP4 / FP8 KV / no-MTP | 76.68 | 76.26 | 77.25 | 77.77 | 74.85 |
| TP4 / FP8 KV / MTP | 57.18 | 60.77 | 81.46 | 73.71 | 84.26 |

### SGLang / NVFP4

| Configuration | 8K | 32K | 64K | 128K | 254K |
|---|---|---|---|---|---|
| TP2 / BF16 KV / no-MTP | 57.02 | 53.86 | 50.68 | 44.87 | 37.07 |
| TP2 / BF16 KV / MTP | 77.73 | 85.04 | 85.75 | 79.09 | FAIL |
| TP2 / FP8 KV / no-MTP | 57.10 | 55.05 | 52.96 | 49.41 | 43.53 |
| TP2 / FP8 KV / MTP | 73.04 | 98.18 | 54.86 | 70.54 | 61.20 |
| TP4 / BF16 KV / no-MTP | 75.58 | 72.78 | 68.40 | 62.87 | 54.44 |
| TP4 / BF16 KV / MTP | 76.08 | 84.62 | 81.37 | 77.96 | 67.60 |
| TP4 / FP8 KV / no-MTP | 76.37 | 72.61 | 70.27 | 66.84 | 61.55 |
| TP4 / FP8 KV / MTP | 82.55 | 80.61 | 79.59 | 92.62 | 65.69 |

### vLLM / FP8

| Configuration | 8K | 32K | 64K | 128K | 254K |
|---|---|---|---|---|---|
| TP2 / BF16 KV / no-MTP | FAIL | FAIL | FAIL | FAIL | FAIL |
| TP2 / BF16 KV / MTP | FAIL | FAIL | FAIL | FAIL | FAIL |
| TP2 / FP8 KV / no-MTP | 47.62 | 47.07 | 46.32 | 46.68 | 41.46 |
| TP2 / FP8 KV / MTP | 60.73 | 64.54 | 66.32 | 59.04 | 53.82 |
| TP4 / BF16 KV / no-MTP | 63.84 | 57.53 | 50.84 | 40.25 | 28.84 |
| TP4 / BF16 KV / MTP | 66.94 | 38.90 | 23.15 | 13.60 | 7.95 |
| TP4 / FP8 KV / no-MTP | 65.72 | 65.39 | 65.20 | 68.54 | 63.73 |
| TP4 / FP8 KV / MTP | 42.69 | 70.64 | 66.84 | 74.24 | 72.37 |

### SGLang / FP8

| Configuration | 8K | 32K | 64K | 128K | 254K |
|---|---|---|---|---|---|
| TP2 / BF16 KV / no-MTP | 46.88 | 45.03 | 42.37 | 38.33 | FAIL |
| TP2 / BF16 KV / MTP | FAIL | FAIL | FAIL | FAIL | FAIL |
| TP2 / FP8 KV / no-MTP | 46.71 | 45.32 | 43.88 | 41.34 | 37.28 |
| TP2 / FP8 KV / MTP | FAIL | FAIL | FAIL | FAIL | FAIL |
| TP4 / BF16 KV / no-MTP | 66.08 | 62.68 | 60.19 | 55.98 | 49.10 |
| TP4 / BF16 KV / MTP | 100.63 | 93.78 | 99.58 | 71.54 | 70.75 |
| TP4 / FP8 KV / no-MTP | 66.56 | 63.84 | 62.46 | 59.66 | 55.65 |
| TP4 / FP8 KV / MTP | 78.20 | 78.75 | 93.21 | 82.25 | 60.90 |

## Single-stream prefill by depth

Values are effective prompt tokens/s to first token.

### vLLM / NVFP4

| Configuration | 8K | 32K | 64K | 128K | 254K |
|---|---|---|---|---|---|
| TP2 / BF16 KV / no-MTP | 1819.5 | 1454.4 | 1144.6 | 801.6 | 511.5 |
| TP2 / BF16 KV / MTP | 1751.1 | 1445.4 | 1143.7 | 798.5 | 510.7 |
| TP2 / FP8 KV / no-MTP | 1900.7 | 1753.2 | 1577.6 | 1315.8 | 1001.8 |
| TP2 / FP8 KV / MTP | 1779.5 | 1722.3 | 1539.7 | 1269.2 | 964.5 |
| TP4 / BF16 KV / no-MTP | 814.5 | 836.4 | 783.8 | 690.8 | 558.3 |
| TP4 / BF16 KV / MTP | 821.9 | 838.1 | 788.9 | 688.9 | 556.0 |
| TP4 / FP8 KV / no-MTP | 823.9 | 874.4 | 860.8 | 822.3 | 744.4 |
| TP4 / FP8 KV / MTP | 839.9 | 862.5 | 837.5 | 790.6 | 715.4 |

### SGLang / NVFP4

| Configuration | 8K | 32K | 64K | 128K | 254K |
|---|---|---|---|---|---|
| TP2 / BF16 KV / no-MTP | 1798.8 | 1715.1 | 1563.3 | 1326.0 | 1032.7 |
| TP2 / BF16 KV / MTP | 1795.8 | 1668.7 | 1515.1 | 1283.2 | FAIL |
| TP2 / FP8 KV / no-MTP | 1824.7 | 1680.9 | 1510.2 | 1260.0 | 963.4 |
| TP2 / FP8 KV / MTP | 1774.4 | 1631.9 | 1465.5 | 1215.2 | 925.6 |
| TP4 / BF16 KV / no-MTP | 944.7 | 1020.5 | 993.7 | 944.8 | 853.1 |
| TP4 / BF16 KV / MTP | 1027.9 | 871.9 | 853.2 | 811.1 | 740.1 |
| TP4 / FP8 KV / no-MTP | 859.0 | 855.9 | 841.7 | 799.0 | 724.4 |
| TP4 / FP8 KV / MTP | 857.7 | 843.6 | 819.8 | 774.2 | 700.8 |

### vLLM / FP8

| Configuration | 8K | 32K | 64K | 128K | 254K |
|---|---|---|---|---|---|
| TP2 / BF16 KV / no-MTP | FAIL | FAIL | FAIL | FAIL | FAIL |
| TP2 / BF16 KV / MTP | FAIL | FAIL | FAIL | FAIL | FAIL |
| TP2 / FP8 KV / no-MTP | 1851.8 | 1719.2 | 1545.4 | 1289.3 | 986.3 |
| TP2 / FP8 KV / MTP | 1712.1 | 1676.5 | 1500.4 | 1243.9 | 946.3 |
| TP4 / BF16 KV / no-MTP | 805.0 | 815.0 | 768.4 | 677.4 | 548.1 |
| TP4 / BF16 KV / MTP | 776.4 | 798.1 | 759.4 | 667.3 | 541.4 |
| TP4 / FP8 KV / no-MTP | 814.5 | 869.2 | 855.2 | 819.4 | 744.8 |
| TP4 / FP8 KV / MTP | 823.6 | 858.3 | 836.4 | 790.0 | 716.0 |

### SGLang / FP8

| Configuration | 8K | 32K | 64K | 128K | 254K |
|---|---|---|---|---|---|
| TP2 / BF16 KV / no-MTP | 1750.2 | 1640.0 | 1501.0 | 1281.5 | FAIL |
| TP2 / BF16 KV / MTP | FAIL | FAIL | FAIL | FAIL | FAIL |
| TP2 / FP8 KV / no-MTP | 1742.0 | 1608.7 | 1449.3 | 1215.1 | 935.7 |
| TP2 / FP8 KV / MTP | FAIL | FAIL | FAIL | FAIL | FAIL |
| TP4 / BF16 KV / no-MTP | 1025.3 | 1013.0 | 989.7 | 938.0 | 852.0 |
| TP4 / BF16 KV / MTP | 1211.7 | 1207.4 | 1160.2 | 1089.4 | 964.6 |
| TP4 / FP8 KV / no-MTP | 864.0 | 859.1 | 839.1 | 796.2 | 723.1 |
| TP4 / FP8 KV / MTP | 850.7 | 840.9 | 816.9 | 772.5 | 700.0 |

## Depth degradation

Decode change from 8K to 254K. FAIL means one of the endpoints was unavailable.

| Engine | Weights | Configuration | 8K | 254K | Change |
|---|---|---|---|---|---|
| vLLM | NVFP4 | TP2 / BF16 KV / no-MTP | 58.56 | 27.26 | -53.4% |
| vLLM | NVFP4 | TP2 / BF16 KV / MTP | 62.32 | 8.35 | -86.6% |
| vLLM | NVFP4 | TP2 / FP8 KV / no-MTP | 60.03 | 52.84 | -12.0% |
| vLLM | NVFP4 | TP2 / FP8 KV / MTP | 63.64 | 64.39 | +1.2% |
| vLLM | NVFP4 | TP4 / BF16 KV / no-MTP | 73.84 | 31.18 | -57.8% |
| vLLM | NVFP4 | TP4 / BF16 KV / MTP | 73.50 | 7.88 | -89.3% |
| vLLM | NVFP4 | TP4 / FP8 KV / no-MTP | 76.68 | 74.85 | -2.4% |
| vLLM | NVFP4 | TP4 / FP8 KV / MTP | 57.18 | 84.26 | +47.4% |
| SGLang | NVFP4 | TP2 / BF16 KV / no-MTP | 57.02 | 37.07 | -35.0% |
| SGLang | NVFP4 | TP2 / BF16 KV / MTP | 77.73 | FAIL | FAIL |
| SGLang | NVFP4 | TP2 / FP8 KV / no-MTP | 57.10 | 43.53 | -23.8% |
| SGLang | NVFP4 | TP2 / FP8 KV / MTP | 73.04 | 61.20 | -16.2% |
| SGLang | NVFP4 | TP4 / BF16 KV / no-MTP | 75.58 | 54.44 | -28.0% |
| SGLang | NVFP4 | TP4 / BF16 KV / MTP | 76.08 | 67.60 | -11.1% |
| SGLang | NVFP4 | TP4 / FP8 KV / no-MTP | 76.37 | 61.55 | -19.4% |
| SGLang | NVFP4 | TP4 / FP8 KV / MTP | 82.55 | 65.69 | -20.4% |
| vLLM | FP8 | TP2 / BF16 KV / no-MTP | FAIL | FAIL | FAIL |
| vLLM | FP8 | TP2 / BF16 KV / MTP | FAIL | FAIL | FAIL |
| vLLM | FP8 | TP2 / FP8 KV / no-MTP | 47.62 | 41.46 | -12.9% |
| vLLM | FP8 | TP2 / FP8 KV / MTP | 60.73 | 53.82 | -11.4% |
| vLLM | FP8 | TP4 / BF16 KV / no-MTP | 63.84 | 28.84 | -54.8% |
| vLLM | FP8 | TP4 / BF16 KV / MTP | 66.94 | 7.95 | -88.1% |
| vLLM | FP8 | TP4 / FP8 KV / no-MTP | 65.72 | 63.73 | -3.0% |
| vLLM | FP8 | TP4 / FP8 KV / MTP | 42.69 | 72.37 | +69.5% |
| SGLang | FP8 | TP2 / BF16 KV / no-MTP | 46.88 | FAIL | FAIL |
| SGLang | FP8 | TP2 / BF16 KV / MTP | FAIL | FAIL | FAIL |
| SGLang | FP8 | TP2 / FP8 KV / no-MTP | 46.71 | 37.28 | -20.2% |
| SGLang | FP8 | TP2 / FP8 KV / MTP | FAIL | FAIL | FAIL |
| SGLang | FP8 | TP4 / BF16 KV / no-MTP | 66.08 | 49.10 | -25.7% |
| SGLang | FP8 | TP4 / BF16 KV / MTP | 100.63 | 70.75 | -29.7% |
| SGLang | FP8 | TP4 / FP8 KV / no-MTP | 66.56 | 55.65 | -16.4% |
| SGLang | FP8 | TP4 / FP8 KV / MTP | 78.20 | 60.90 | -22.1% |

## Aggregate decode and concurrency knee at 8K

Each concurrency cell is `shared decode-window tok/s / sum of active request decode rates`. Both peaks are reported: the shared-window peak is the literal aggregate decode metric, while the active-rate peak is a decode-only diagnostic. The shared-window number is conservative when chunked prefills stagger entry into decode.

| Engine | Weights | Configuration | c1 | c2 | c4 | c8 | c16 | Shared peak | Active peak |
|---|---|---|---|---|---|---|---|---|---|
| vLLM | NVFP4 | TP2 / BF16 KV / no-MTP | 58.56 / 58.56 | 17.33 / 60.94 | 13.20 / 106.86 | 11.72 / 103.21 | 10.77 / 88.94 | c=1 | c=4 |
| vLLM | NVFP4 | TP2 / BF16 KV / MTP | 62.32 / 62.32 | 34.54 / 79.37 | 9.25 / 18.89 | 10.95 / 114.31 | 11.83 / 103.28 | c=1 | c=8 |
| vLLM | NVFP4 | TP2 / FP8 KV / no-MTP | 60.03 / 60.03 | 19.08 / 62.42 | 14.54 / 108.67 | 13.43 / 111.15 | 12.55 / 103.14 | c=1 | c=8 |
| vLLM | NVFP4 | TP2 / FP8 KV / MTP | 63.64 / 63.64 | 13.27 / 58.08 | 10.71 / 20.06 | 11.98 / 119.67 | 11.61 / 91.67 | c=1 | c=8 |
| vLLM | NVFP4 | TP4 / BF16 KV / no-MTP | 73.84 / 73.84 | 9.25 / 68.13 | 6.52 / 98.66 | 5.44 / 75.12 | 5.68 / 56.04 | c=1 | c=4 |
| vLLM | NVFP4 | TP4 / BF16 KV / MTP | 73.50 / 73.50 | 8.56 / 64.01 | 6.49 / 77.45 | 6.24 / 80.77 | 5.64 / 59.43 | c=1 | c=8 |
| vLLM | NVFP4 | TP4 / FP8 KV / no-MTP | 76.68 / 76.68 | 7.72 / 65.61 | 7.29 / 99.70 | 5.70 / 76.24 | 6.62 / 59.11 | c=1 | c=4 |
| vLLM | NVFP4 | TP4 / FP8 KV / MTP | 57.18 / 57.18 | 9.43 / 45.72 | 4.59 / 12.36 | 5.46 / 75.64 | 5.44 / 56.48 | c=1 | c=8 |
| SGLang | NVFP4 | TP2 / BF16 KV / no-MTP | 57.02 / 57.02 | 81.14 / 103.97 | 38.80 / 131.52 | 29.18 / 143.44 | 22.80 / 146.28 | c=2 | c=16 |
| SGLang | NVFP4 | TP2 / BF16 KV / MTP | 77.73 / 77.73 | 27.93 / 157.59 | 15.91 / 315.75 | 15.89 / 609.86 | 18.07 / 1319.55 | c=1 | c=16 |
| SGLang | NVFP4 | TP2 / FP8 KV / no-MTP | 57.10 / 57.10 | 81.80 / 104.90 | 35.46 / 129.56 | 31.51 / 149.72 | 26.45 / 128.10 | c=2 | c=8 |
| SGLang | NVFP4 | TP2 / FP8 KV / MTP | 73.04 / 73.04 | 104.40 / 139.36 | 29.80 / 180.02 | 20.02 / 284.91 | 20.60 / 449.70 | c=2 | c=16 |
| SGLang | NVFP4 | TP4 / BF16 KV / no-MTP | 75.58 / 75.58 | 92.24 / 123.00 | 24.24 / 113.54 | 15.59 / 97.05 | 12.15 / 87.43 | c=2 | c=2 |
| SGLang | NVFP4 | TP4 / BF16 KV / MTP | 76.08 / 76.08 | 107.84 / 128.15 | 21.14 / 107.07 | 14.18 / 117.05 | 13.09 / 86.68 | c=2 | c=2 |
| SGLang | NVFP4 | TP4 / FP8 KV / no-MTP | 76.37 / 76.37 | 96.21 / 120.59 | 21.77 / 106.89 | 13.07 / 86.31 | 12.69 / 75.16 | c=2 | c=2 |
| SGLang | NVFP4 | TP4 / FP8 KV / MTP | 82.55 / 82.55 | 110.37 / 112.86 | 27.75 / 122.18 | 11.43 / 99.28 | 11.91 / 68.50 | c=2 | c=4 |
| vLLM | FP8 | TP2 / BF16 KV / no-MTP | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL |
| vLLM | FP8 | TP2 / BF16 KV / MTP | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL |
| vLLM | FP8 | TP2 / FP8 KV / no-MTP | 47.62 / 47.62 | 17.77 / 51.78 | 14.76 / 91.35 | 9.93 / 84.93 | 11.99 / 92.31 | c=1 | c=16 |
| vLLM | FP8 | TP2 / FP8 KV / MTP | 60.73 / 60.73 | 13.85 / 47.12 | 8.80 / 18.15 | 13.31 / 113.97 | 11.88 / 88.94 | c=1 | c=8 |
| vLLM | FP8 | TP4 / BF16 KV / no-MTP | 63.84 / 63.84 | 10.83 / 57.94 | 7.58 / 89.83 | 5.51 / 69.98 | 5.46 / 52.34 | c=1 | c=4 |
| vLLM | FP8 | TP4 / BF16 KV / MTP | 66.94 / 66.94 | 32.72 / 68.15 | 4.97 / 14.42 | 5.72 / 74.98 | 4.90 / 51.17 | c=1 | c=8 |
| vLLM | FP8 | TP4 / FP8 KV / no-MTP | 65.72 / 65.72 | 11.86 / 59.97 | 7.67 / 90.98 | 5.83 / 71.77 | 6.06 / 56.15 | c=1 | c=4 |
| vLLM | FP8 | TP4 / FP8 KV / MTP | 42.69 / 42.69 | 7.52 / 46.48 | 5.41 / 14.93 | 6.33 / 81.09 | 6.42 / 61.21 | c=1 | c=8 |
| SGLang | FP8 | TP2 / BF16 KV / no-MTP | 46.88 / 46.88 | 82.14 / 84.64 | 27.98 / 104.23 | 13.75 / 98.70 | 12.83 / 102.09 | c=2 | c=4 |
| SGLang | FP8 | TP2 / BF16 KV / MTP | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL |
| SGLang | FP8 | TP2 / FP8 KV / no-MTP | 46.71 / 46.71 | 75.38 / 85.53 | 24.16 / 103.51 | 14.51 / 104.28 | 13.17 / 104.12 | c=2 | c=8 |
| SGLang | FP8 | TP2 / FP8 KV / MTP | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL |
| SGLang | FP8 | TP4 / BF16 KV / no-MTP | 66.08 / 66.08 | 94.29 / 101.40 | 16.58 / 92.05 | 9.39 / 79.13 | 7.35 / 66.37 | c=2 | c=2 |
| SGLang | FP8 | TP4 / BF16 KV / MTP | 100.63 / 100.63 | 126.64 / 141.98 | 24.82 / 131.92 | 12.07 / 109.01 | 9.10 / 62.07 | c=2 | c=2 |
| SGLang | FP8 | TP4 / FP8 KV / no-MTP | 66.56 / 66.56 | 88.66 / 105.40 | 14.40 / 92.29 | 7.88 / 73.31 | 6.64 / 49.67 | c=2 | c=2 |
| SGLang | FP8 | TP4 / FP8 KV / MTP | 78.20 / 78.20 | 126.87 / 139.67 | 17.08 / 106.21 | 9.49 / 103.45 | 6.52 / 72.69 | c=2 | c=2 |

## Aggregate prefill at 8K

| Engine | Weights | Configuration | c1 | c2 | c4 | c8 | c16 |
|---|---|---|---|---|---|---|---|
| vLLM | NVFP4 | TP2 / BF16 KV / no-MTP | 1819.5 | 1836.2 | 1840.8 | 1843.9 | 1843.4 |
| vLLM | NVFP4 | TP2 / BF16 KV / MTP | 1751.1 | 1533.2 | 1759.3 | 1800.0 | 1798.2 |
| vLLM | NVFP4 | TP2 / FP8 KV / no-MTP | 1900.7 | 1919.2 | 1925.6 | 1930.2 | 1928.2 |
| vLLM | NVFP4 | TP2 / FP8 KV / MTP | 1779.5 | 1590.9 | 1876.4 | 1882.3 | 1872.2 |
| vLLM | NVFP4 | TP4 / BF16 KV / no-MTP | 814.5 | 876.1 | 900.3 | 907.1 | 904.7 |
| vLLM | NVFP4 | TP4 / BF16 KV / MTP | 821.9 | 859.2 | 888.4 | 895.5 | 895.2 |
| vLLM | NVFP4 | TP4 / FP8 KV / no-MTP | 823.9 | 899.5 | 907.0 | 912.4 | 915.6 |
| vLLM | NVFP4 | TP4 / FP8 KV / MTP | 839.9 | 811.0 | 881.8 | 877.8 | 881.0 |
| SGLang | NVFP4 | TP2 / BF16 KV / no-MTP | 1798.8 | 1702.5 | 1855.1 | 1862.8 | 1808.2 |
| SGLang | NVFP4 | TP2 / BF16 KV / MTP | 1795.8 | 1640.6 | 1581.7 | 1496.7 | 1454.6 |
| SGLang | NVFP4 | TP2 / FP8 KV / no-MTP | 1824.7 | 1834.1 | 1847.9 | 1854.1 | 1799.3 |
| SGLang | NVFP4 | TP2 / FP8 KV / MTP | 1774.4 | 1764.5 | 1667.4 | 1621.8 | 1603.2 |
| SGLang | NVFP4 | TP4 / BF16 KV / no-MTP | 944.7 | 981.2 | 1043.6 | 1040.8 | 1018.7 |
| SGLang | NVFP4 | TP4 / BF16 KV / MTP | 1027.9 | 859.9 | 865.5 | 891.7 | 876.0 |
| SGLang | NVFP4 | TP4 / FP8 KV / no-MTP | 859.0 | 878.1 | 887.9 | 890.0 | 875.7 |
| SGLang | NVFP4 | TP4 / FP8 KV / MTP | 857.7 | 856.7 | 864.9 | 867.2 | 852.5 |
| vLLM | FP8 | TP2 / BF16 KV / no-MTP | FAIL | FAIL | FAIL | FAIL | FAIL |
| vLLM | FP8 | TP2 / BF16 KV / MTP | FAIL | FAIL | FAIL | FAIL | FAIL |
| vLLM | FP8 | TP2 / FP8 KV / no-MTP | 1851.8 | 1840.8 | 1865.4 | 1581.6 | 1881.1 |
| vLLM | FP8 | TP2 / FP8 KV / MTP | 1712.1 | 1554.4 | 1823.8 | 1828.6 | 1806.4 |
| vLLM | FP8 | TP4 / BF16 KV / no-MTP | 805.0 | 838.1 | 862.4 | 823.1 | 881.3 |
| vLLM | FP8 | TP4 / BF16 KV / MTP | 776.4 | 774.8 | 828.8 | 851.2 | 857.7 |
| vLLM | FP8 | TP4 / FP8 KV / no-MTP | 814.5 | 877.9 | 899.1 | 846.3 | 911.6 |
| vLLM | FP8 | TP4 / FP8 KV / MTP | 823.6 | 815.7 | 885.2 | 886.4 | 885.7 |
| SGLang | FP8 | TP2 / BF16 KV / no-MTP | 1750.2 | 1757.9 | 1764.9 | 1773.6 | 1747.0 |
| SGLang | FP8 | TP2 / BF16 KV / MTP | FAIL | FAIL | FAIL | FAIL | FAIL |
| SGLang | FP8 | TP2 / FP8 KV / no-MTP | 1742.0 | 1747.1 | 1760.0 | 1765.2 | 1724.6 |
| SGLang | FP8 | TP2 / FP8 KV / MTP | FAIL | FAIL | FAIL | FAIL | FAIL |
| SGLang | FP8 | TP4 / BF16 KV / no-MTP | 1025.3 | 1019.4 | 1036.7 | 1040.8 | 1024.8 |
| SGLang | FP8 | TP4 / BF16 KV / MTP | 1211.7 | 1231.9 | 1240.2 | 1243.6 | 1217.0 |
| SGLang | FP8 | TP4 / FP8 KV / no-MTP | 864.0 | 872.8 | 881.3 | 886.7 | 877.5 |
| SGLang | FP8 | TP4 / FP8 KV / MTP | 850.7 | 858.4 | 860.7 | 863.9 | 852.2 |

## Terminal failures

| Engine | Weights | Configuration | Count | Points |
|---|---|---|---|---|
| SGLang | NVFP4 | TP2 / BF16 KV / MTP | 1 | 254K/c1 |
| vLLM | FP8 | TP2 / BF16 KV / no-MTP | 9 | 8K/c1, 8K/c2, 8K/c4, 8K/c8, 8K/c16, 32K/c1, 64K/c1, 128K/c1, 254K/c1 |
| vLLM | FP8 | TP2 / BF16 KV / MTP | 9 | 8K/c1, 8K/c2, 8K/c4, 8K/c8, 8K/c16, 32K/c1, 64K/c1, 128K/c1, 254K/c1 |
| SGLang | FP8 | TP2 / BF16 KV / no-MTP | 1 | 254K/c1 |
| SGLang | FP8 | TP2 / BF16 KV / MTP | 9 | 8K/c1, 8K/c2, 8K/c4, 8K/c8, 8K/c16, 32K/c1, 64K/c1, 128K/c1, 254K/c1 |
| SGLang | FP8 | TP2 / FP8 KV / MTP | 9 | 8K/c1, 8K/c2, 8K/c4, 8K/c8, 8K/c16, 32K/c1, 64K/c1, 128K/c1, 254K/c1 |

## Raw data

Merged machine-readable table: `qwen38-full-comparison.csv`. Every source suite also contains its per-point JSON files, `summary.json`, server logs, launch manifests, and status history.
