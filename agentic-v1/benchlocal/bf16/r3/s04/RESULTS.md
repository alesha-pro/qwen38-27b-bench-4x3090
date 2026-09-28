## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 4 / 4 | 100% | — | — | 21.88s | 1034.02s | ok; partial — 4 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 2 | 100% | — | — | 47.34s | 61.59s | ok; partial — 2 of 20 selected

TOTAL | 6 / 6 | 100% |  |  |  |  |

Equivalent to: 150/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19420/v1, model: bench, thinking=on, 2026-09-27T18:05:18.506020Z) [PARTIAL SELECTION: 6 scenarios] ===

  [1/4] CLI-05 ✓ passed pass@1 (30.3s)
  [2/4] CLI-15 ✓ passed pass@1 (1034.0s)
  [3/4] CLI-25 ✓ passed pass@1 (13.4s)
  [4/4] CLI-35 ✓ passed pass@1 (6.0s)
cli-40 (v1.0.2) | 4 / 4 | 100% | 21.88s | ok; partial — 4 of 40 selected
  [1/2] HA-05 ✓ passed pass@1 (61.6s)
  [2/2] HA-15 ✓ passed pass@1 (33.1s)
hermesagent-20 (v1.0.0) | 2 / 2 | 100% | 47.34s | ok; partial — 2 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 4 / 4 | 100% | 21.88s | 1034.02s | ok; partial — 4 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 2 | 100% | 47.34s | 61.59s | ok; partial — 2 of 20 selected

TOTAL | 6 / 6 | 100% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 6 (0.0%) | — | — | message.content=3, multi_turn=1
hermesagent-20 | — | — | — | multi_turn=2
```

</details>
