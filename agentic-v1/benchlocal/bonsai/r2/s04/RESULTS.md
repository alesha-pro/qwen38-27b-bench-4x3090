## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 5 / 5 | 100% | — | — | 104.87s | 689.78s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | — | — | 132.47s | 188.03s | ok; partial — 2 of 20 selected

TOTAL | 6 / 7 | 86% |  |  |  |  |

Equivalent to: 129/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19412/v1, model: bench, thinking=on, 2026-09-27T17:54:17.517755Z) [PARTIAL SELECTION: 7 scenarios] ===

  [1/5] CLI-05 ✓ passed pass@1 (77.5s)
  [2/5] CLI-13 ✓ passed pass@1 (689.8s)
  [3/5] CLI-21 ✓ passed pass@1 (117.3s)
  [4/5] CLI-29 ✓ passed pass@1 (104.9s)
  [5/5] CLI-37 ✓ passed pass@1 (90.6s)
cli-40 (v1.0.2) | 5 / 5 | 100% | 104.87s | ok; partial — 5 of 40 selected
  [1/2] HA-05 ✓ passed pass@1 (76.9s)
  [2/2] HA-13 ✗ verifier_fail fail (188.0s)
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | 132.47s | ok; partial — 2 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 5 / 5 | 100% | 104.87s | 689.78s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | 132.47s | 188.03s | ok; partial — 2 of 20 selected

TOTAL | 6 / 7 | 86% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 39 (0.0%) | — | — | message.content=2, multi_turn=3
hermesagent-20 | — | — | — | multi_turn=2

Failure breakdown:
- hermesagent-20 HA-13: verifier_fail [fail] (Hermes failed the cron creation scenario.)
```

</details>
