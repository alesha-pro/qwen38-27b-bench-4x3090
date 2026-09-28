## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 5 / 5 | 100% | — | — | 45.68s | 1807.24s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 3 | 67% | — | — | 49.11s | 62.23s | ok; partial — 3 of 20 selected

TOTAL | 7 / 8 | 88% |  |  |  |  |

Equivalent to: 131/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19410/v1, model: bench, thinking=on, 2026-09-27T17:46:01.668463Z) [PARTIAL SELECTION: 8 scenarios] ===

  [1/5] CLI-03 ✓ passed pass@1 (50.5s)
  [2/5] CLI-11 ✓ passed pass@1 (1807.2s)
  [3/5] CLI-19 ✓ passed pass@1 (45.7s)
  [4/5] CLI-27 ✓ passed pass@1 (17.6s)
  [5/5] CLI-35 ✓ passed pass@1 (5.9s)
cli-40 (v1.0.2) | 5 / 5 | 100% | 45.68s | ok; partial — 5 of 40 selected
  [1/3] HA-03 ✓ passed pass@1 (11.4s)
  [2/3] HA-11 ✓ passed pass@1 (49.1s)
  [3/3] HA-19 ✗ verifier_fail fail (62.2s)
hermesagent-20 (v1.0.0) | 2 / 3 | 67% | 49.11s | ok; partial — 3 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 5 / 5 | 100% | 45.68s | 1807.24s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 3 | 67% | 49.11s | 62.23s | ok; partial — 3 of 20 selected

TOTAL | 7 / 8 | 88% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 7 (0.0%) | — | — | message.content=4, multi_turn=1
hermesagent-20 | — | — | — | multi_turn=3

Failure breakdown:
- hermesagent-20 HA-19: verifier_fail [fail] (Hermes retried deployment partially, but the corrective-action trace or final success was incomplete.)
```

</details>
