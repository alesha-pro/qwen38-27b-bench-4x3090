# Qwen3.8-27B quant quality matrix

Pass@1 is the quality result; pass@k is a diagnostic for failed-scenario retries. `full` and `reasoning` stay separate because they overlap.

| Model | Effort | Suite | Pass@1 | Pass@k | Reasoning tokens total | Median | p95 | Think calls | max_tokens calls | Valid |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| awq-int4 | low | full | 130/150 (86.7%) | 136/150 (90.7%) | 83440 | 250 | 2130 | 394 | 0 | yes |
| fp8 | low | full | 130/150 (86.7%) | 135/150 (90.0%) | 88513 | 270 | 2131 | 390 | 1 | NO |
| gguf-q4-k-m | low | full | 134/150 (89.3%) | 135/150 (90.0%) | 86367 | 254 | 1751 | 388 | 0 | yes |
| ninfer | low | full | 125/150 (83.3%) | 131/150 (87.3%) | 98093 | 254 | 2864 | 424 | 0 | yes |
| nvfp4 | low | full | 131/150 (87.3%) | 138/150 (92.0%) | 73797 | 224 | 1646 | 377 | 0 | yes |
| awq-int4 | low | reasoning | 90/90 (100.0%) | 90/90 (100.0%) | 380394 | 3160 | 16938 | 90 | 0 | yes |
| fp8 | low | reasoning | 86/90 (95.6%) | 90/90 (100.0%) | 509465 | 3247 | 21126 | 95 | 0 | yes |
| gguf-q4-k-m | low | reasoning | 85/90 (94.4%) | 90/90 (100.0%) | 572195 | 3272 | 15730 | 97 | 0 | yes |
| ninfer | low | reasoning | 86/90 (95.6%) | 90/90 (100.0%) | 432759 | 3674 | 19123 | 95 | 0 | yes |
| nvfp4 | low | reasoning | 90/90 (100.0%) | 61/61 (100.0%) | 413430 | 3160 | 15392 | 90 | 0 | yes |
| awq-int4 | medium | full | 129/150 (86.0%) | 140/150 (93.3%) | 101743 | 273 | 2746 | 365 | 0 | yes |
| fp8 | medium | full | 131/150 (87.3%) | 134/150 (89.3%) | 93063 | 268 | 2589 | 591 | 88 | NO |
| gguf-q4-k-m | medium | full | 132/150 (88.0%) | 137/150 (91.3%) | 147665 | 302 | 2815 | 378 | 0 | yes |
| ninfer | medium | full | 126/150 (84.0%) | 136/150 (90.7%) | 251914 | 334 | 2907 | 381 | 0 | yes |
| nvfp4 | medium | full | 130/150 (86.7%) | 137/150 (91.3%) | 232637 | 266 | 3624 | 372 | 0 | yes |
| awq-int4 | medium | reasoning | 84/90 (93.3%) | 60/61 (98.4%) | 559454 | 3396 | 15705 | 99 | 0 | yes |
| fp8 | medium | reasoning | 78/90 (86.7%) | 85/90 (94.4%) | 664317 | 3768 | 18399 | 110 | 0 | yes |
| gguf-q4-k-m | medium | reasoning | 82/90 (91.1%) | 87/90 (96.7%) | 554665 | 4597 | 21035 | 99 | 0 | yes |
| ninfer | medium | reasoning | 82/90 (91.1%) | 88/90 (97.8%) | 445517 | 3764 | 17045 | 101 | 0 | yes |
| nvfp4 | medium | reasoning | 82/90 (91.1%) | 87/90 (96.7%) | 575618 | 3789 | 13238 | 101 | 0 | yes |
| awq-int4 | off | full | 117/150 (78.0%) | 117/150 (78.0%) | 0 | 0 | 0 | 0 | 484 | yes |
| fp8 | off | full | 121/150 (80.7%) | 121/150 (80.7%) | 179 | 0 | 0 | 1 | 387 | NO |
| gguf-q4-k-m | off | full | 116/150 (77.3%) | 117/150 (78.0%) | 0 | 0 | 0 | 0 | 424 | yes |
| ninfer | off | full | 119/150 (79.3%) | 119/150 (79.3%) | 0 | 0 | 0 | 0 | 440 | yes |
| nvfp4 | off | full | 122/150 (81.3%) | 123/150 (82.0%) | 0 | 0 | 0 | 0 | 431 | yes |
| awq-int4 | off | reasoning | 83/90 (92.2%) | 83/90 (92.2%) | 0 | 0 | 0 | 0 | 102 | yes |
| fp8 | off | reasoning | 85/90 (94.4%) | 85/90 (94.4%) | 0 | 0 | 0 | 0 | 100 | yes |
| gguf-q4-k-m | off | reasoning | 84/90 (93.3%) | 84/90 (93.3%) | 0 | 0 | 0 | 0 | 100 | yes |
| ninfer | off | reasoning | 84/90 (93.3%) | 84/90 (93.3%) | 0 | 0 | 0 | 0 | 102 | yes |
| nvfp4 | off | reasoning | 70/90 (77.8%) | 70/90 (77.8%) | 0 | 0 | 0 | 0 | 130 | yes |
| awq-int4 | xhigh | full | 135/150 (90.0%) | 140/150 (93.3%) | 578123 | 432 | 14463 | 378 | 0 | yes |
| fp8 | xhigh | full | 133/150 (88.7%) | 139/150 (92.7%) | 724404 | 379 | 22530 | 382 | 0 | yes |
| gguf-q4-k-m | xhigh | full | 134/150 (89.3%) | 139/150 (92.7%) | 651281 | 362 | 15854 | 365 | 0 | yes |
| ninfer | xhigh | full | 132/150 (88.0%) | 137/150 (91.3%) | 699018 | 432 | 14002 | 393 | 0 | yes |
| nvfp4 | xhigh | full | 134/150 (89.3%) | 139/150 (92.7%) | 819808 | 390 | 22745 | 362 | 0 | yes |
| awq-int4 | xhigh | reasoning | 90/90 (100.0%) | 90/90 (100.0%) | 817478 | 8516 | 41973 | 90 | 0 | yes |
| fp8 | xhigh | reasoning | 89/90 (98.9%) | 90/90 (100.0%) | 875983 | 9639 | 40747 | 91 | 0 | yes |
| gguf-q4-k-m | xhigh | reasoning | 89/90 (98.9%) | 90/90 (100.0%) | 867644 | 8584 | 39997 | 91 | 0 | yes |
| ninfer | xhigh | reasoning | 88/90 (97.8%) | 90/90 (100.0%) | 1023558 | 9001 | 50412 | 92 | 0 | yes |
| nvfp4 | xhigh | reasoning | 90/90 (100.0%) | 90/90 (100.0%) | 1021509 | 10278 | 49414 | 90 | 0 | yes |

## Artifacts

- `per-scenario.csv`: one task, its verdict, attempts, latency, and all-call token totals.
- `per-request.csv`: every direct and hidden model call with raw usage/control audit.
- `per-arm.csv`: dense arm-level statistics and thinking validity.
- `per-pack.csv`: pack scores, token totals, failure modes, and pass@k.
- `paired-vs-fp8.csv`: matched scenario flips and exact McNemar p-values.
- `paired-effort-vs-off.csv`: quality changes caused by reasoning effort.
- `SUMMARY.json`: lossless machine-readable aggregate, including task flip lists.
