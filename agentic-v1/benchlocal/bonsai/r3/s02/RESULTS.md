## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 4 / 5 | 80% | — | — | 76.95s | 1371.82s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 3 | 67% | — | — | 23.32s | 54.27s | ok; partial — 3 of 20 selected

TOTAL | 6 / 8 | 75% |  |  |  |  |

Equivalent to: 113/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19412/v1, model: bench, thinking=on, 2026-09-27T18:13:17.116181Z) [PARTIAL SELECTION: 8 scenarios] ===

  [1/5] CLI-03 ✓ passed pass@1 (96.4s)
  [2/5] CLI-11 ✓ passed pass@1 (1371.8s)
  [3/5] CLI-19 ✗ verifier_fail fail (77.0s)
  [4/5] CLI-27 ✓ passed pass@1 (37.1s)
  [5/5] CLI-35 ✓ passed pass@1 (4.0s)
cli-40 (v1.0.2) | 4 / 5 | 80% | 76.95s | ok; partial — 5 of 40 selected
  [1/3] HA-03 ✓ passed pass@1 (10.4s)
  [2/3] HA-11 ✓ passed pass@1 (23.3s)
  [3/3] HA-19 ✗ verifier_fail fail (54.3s)
hermesagent-20 (v1.0.0) | 2 / 3 | 67% | 23.32s | ok; partial — 3 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 4 / 5 | 80% | 76.95s | 1371.82s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 3 | 67% | 23.32s | 54.27s | ok; partial — 3 of 20 selected

TOTAL | 6 / 8 | 75% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 15 (0.0%) | — | — | message.content=4, multi_turn=1
hermesagent-20 | — | — | — | multi_turn=3

Failure breakdown:
- cli-40 CLI-19: verifier_fail [fail] (CLI-19: Did not satisfy the scenario requirements. (score=25; correctness=0/2; efficiency=2/2; discipline=0/2; commandCount=1; note=slice.hex did not match the expected byte-for-byte content.))
- hermesagent-20 HA-19: verifier_fail [fail] (Hermes retried deployment partially, but the corrective-action trace or final success was incomplete.)
```

</details>
