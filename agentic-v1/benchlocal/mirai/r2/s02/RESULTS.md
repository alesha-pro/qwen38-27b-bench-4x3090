## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 5 / 5 | 100% | — | — | 40.95s | 1657.73s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 3 | 67% | — | — | 54.80s | 65.00s | ok; partial — 3 of 20 selected

TOTAL | 7 / 8 | 88% |  |  |  |  |

Equivalent to: 131/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19410/v1, model: bench, thinking=on, 2026-09-27T17:57:17.076950Z) [PARTIAL SELECTION: 8 scenarios] ===

  [1/5] CLI-03 ✓ passed pass@1 (45.3s)
  [2/5] CLI-11 ✓ passed pass@1 (1657.7s)
  [3/5] CLI-19 ✓ passed pass@1 (41.0s)
  [4/5] CLI-27 ✓ passed pass@1 (22.3s)
  [5/5] CLI-35 ✓ passed pass@1 (5.1s)
cli-40 (v1.0.2) | 5 / 5 | 100% | 40.95s | ok; partial — 5 of 40 selected
  [1/3] HA-03 ✓ passed pass@1 (18.5s)
  [2/3] HA-11 ✓ passed pass@1 (54.8s)
  [3/3] HA-19 ✗ verifier_fail fail (65.0s)
hermesagent-20 (v1.0.0) | 2 / 3 | 67% | 54.80s | ok; partial — 3 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 5 / 5 | 100% | 40.95s | 1657.73s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 3 | 67% | 54.80s | 65.00s | ok; partial — 3 of 20 selected

TOTAL | 7 / 8 | 88% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 8 (0.0%) | — | — | message.content=4, multi_turn=1
hermesagent-20 | — | — | — | multi_turn=3

Failure breakdown:
- hermesagent-20 HA-19: verifier_fail [fail] (Hermes failed the recover-and-retry deployment scenario.)
```

</details>
