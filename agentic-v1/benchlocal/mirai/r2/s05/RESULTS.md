## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 5 / 5 | 100% | — | — | 44.31s | 895.41s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 2 | 100% | — | — | 48.50s | 76.63s | ok; partial — 2 of 20 selected

TOTAL | 7 / 7 | 100% |  |  |  |  |

Equivalent to: 150/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19410/v1, model: bench, thinking=on, 2026-09-27T18:18:33.438653Z) [PARTIAL SELECTION: 7 scenarios] ===

  [1/5] CLI-06 ✓ passed pass@1 (20.3s)
  [2/5] CLI-14 ✓ passed pass@1 (895.4s)
  [3/5] CLI-22 ✓ passed pass@1 (145.0s)
  [4/5] CLI-30 ✓ passed pass@1 (29.1s)
  [5/5] CLI-38 ✓ passed pass@1 (44.3s)
cli-40 (v1.0.2) | 5 / 5 | 100% | 44.31s | ok; partial — 5 of 40 selected
  [1/2] HA-06 ✓ passed pass@1 (76.6s)
  [2/2] HA-14 ✓ passed pass@1 (20.4s)
hermesagent-20 (v1.0.0) | 2 / 2 | 100% | 48.50s | ok; partial — 2 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 5 / 5 | 100% | 44.31s | 895.41s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 2 | 100% | 48.50s | 76.63s | ok; partial — 2 of 20 selected

TOTAL | 7 / 7 | 100% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 19 (0.0%) | — | — | message.content=2, multi_turn=3
hermesagent-20 | — | — | — | multi_turn=2
```

</details>
