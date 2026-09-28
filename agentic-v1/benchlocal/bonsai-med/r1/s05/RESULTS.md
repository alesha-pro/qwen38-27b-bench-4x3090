## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 5 / 5 | 100% | — | — | 35.05s | 51.05s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 2 | 100% | — | — | 36.53s | 59.41s | ok; partial — 2 of 20 selected

TOTAL | 7 / 7 | 100% |  |  |  |  |

Equivalent to: 150/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19415/v1, model: bench, thinking=on, 2026-09-28T11:17:57.578384Z) [PARTIAL SELECTION: 7 scenarios] ===

  [1/5] CLI-06 ✓ passed pass@1 (8.3s)
  [2/5] CLI-14 ✓ passed pass@1 (35.1s)
  [3/5] CLI-22 ✓ passed pass@1 (49.0s)
  [4/5] CLI-30 ✓ passed pass@1 (24.5s)
  [5/5] CLI-38 ✓ passed pass@1 (51.1s)
cli-40 (v1.0.2) | 5 / 5 | 100% | 35.05s | ok; partial — 5 of 40 selected
  [1/2] HA-06 ✓ passed pass@1 (59.4s)
  [2/2] HA-14 ✓ passed pass@1 (13.6s)
hermesagent-20 (v1.0.0) | 2 / 2 | 100% | 36.53s | ok; partial — 2 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 5 / 5 | 100% | 35.05s | 51.05s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 2 | 100% | 36.53s | 59.41s | ok; partial — 2 of 20 selected

TOTAL | 7 / 7 | 100% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 39 (0.0%) | — | — | message.content=2, multi_turn=3
hermesagent-20 | — | — | — | multi_turn=2
```

</details>
