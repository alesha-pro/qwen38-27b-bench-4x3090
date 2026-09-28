## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 4 / 4 | 100% | — | — | 89.70s | 553.07s | ok; partial — 4 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 2 | 100% | — | — | 76.45s | 90.42s | ok; partial — 2 of 20 selected

TOTAL | 6 / 6 | 100% |  |  |  |  |

Equivalent to: 150/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19420/v1, model: bench, thinking=on, 2026-09-27T18:13:11.941566Z) [PARTIAL SELECTION: 6 scenarios] ===

  [1/4] CLI-07 ✓ passed pass@1 (553.1s)
  [2/4] CLI-17 ✓ passed pass@1 (163.6s)
  [3/4] CLI-27 ✓ passed pass@1 (13.3s)
  [4/4] CLI-37 ✓ passed pass@1 (15.8s)
cli-40 (v1.0.2) | 4 / 4 | 100% | 89.70s | ok; partial — 4 of 40 selected
  [1/2] HA-07 ✓ passed pass@1 (62.5s)
  [2/2] HA-17 ✓ passed pass@1 (90.4s)
hermesagent-20 (v1.0.0) | 2 / 2 | 100% | 76.45s | ok; partial — 2 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 4 / 4 | 100% | 89.70s | 553.07s | ok; partial — 4 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 2 | 100% | 76.45s | 90.42s | ok; partial — 2 of 20 selected

TOTAL | 6 / 6 | 100% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 9 (0.0%) | — | — | message.content=2, multi_turn=2
hermesagent-20 | — | — | — | multi_turn=2
```

</details>
