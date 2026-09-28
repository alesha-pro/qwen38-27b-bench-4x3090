## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 4 / 4 | 100% | — | — | 37.10s | 281.55s | ok; partial — 4 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 2 | 100% | — | — | 45.39s | 52.94s | ok; partial — 2 of 20 selected

TOTAL | 6 / 6 | 100% |  |  |  |  |

Equivalent to: 150/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19420/v1, model: bench, thinking=on, 2026-09-27T17:35:44.383966Z) [PARTIAL SELECTION: 6 scenarios] ===

  [1/4] CLI-05 ✓ passed pass@1 (50.2s)
  [2/4] CLI-15 ✓ passed pass@1 (281.5s)
  [3/4] CLI-25 ✓ passed pass@1 (23.9s)
  [4/4] CLI-35 ✓ passed pass@1 (5.8s)
cli-40 (v1.0.2) | 4 / 4 | 100% | 37.10s | ok; partial — 4 of 40 selected
  [1/2] HA-05 ✓ passed pass@1 (52.9s)
  [2/2] HA-15 ✓ passed pass@1 (37.8s)
hermesagent-20 (v1.0.0) | 2 / 2 | 100% | 45.39s | ok; partial — 2 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 4 / 4 | 100% | 37.10s | 281.55s | ok; partial — 4 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 2 | 100% | 45.39s | 52.94s | ok; partial — 2 of 20 selected

TOTAL | 6 / 6 | 100% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 7 (0.0%) | — | — | message.content=3, multi_turn=1
hermesagent-20 | — | — | — | multi_turn=2
```

</details>
