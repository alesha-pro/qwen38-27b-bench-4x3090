## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 3 / 4 | 75% | — | — | 27.86s | 124.15s | ok; partial — 4 of 40 selected
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | — | — | 57.97s | 67.27s | ok; partial — 2 of 20 selected

TOTAL | 4 / 6 | 67% |  |  |  |  |

Equivalent to: 100/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19420/v1, model: bench, thinking=on, 2026-09-27T17:59:24.473288Z) [PARTIAL SELECTION: 6 scenarios] ===

  [1/4] CLI-09 ✓ passed pass@1 (124.2s)
  [2/4] CLI-19 ✗ verifier_fail fail (16.1s)
  [3/4] CLI-29 ✓ passed pass@1 (25.4s)
  [4/4] CLI-39 ✓ passed pass@1 (30.3s)
cli-40 (v1.0.2) | 3 / 4 | 75% | 27.86s | ok; partial — 4 of 40 selected
  [1/2] HA-09 ✓ passed pass@1 (67.3s)
  [2/2] HA-19 ✗ verifier_fail fail (48.7s)
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | 57.97s | ok; partial — 2 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 3 / 4 | 75% | 27.86s | 124.15s | ok; partial — 4 of 40 selected
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | 57.97s | 67.27s | ok; partial — 2 of 20 selected

TOTAL | 4 / 6 | 67% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 10 (0.0%) | — | — | message.content=2, multi_turn=2
hermesagent-20 | — | — | — | multi_turn=2

Failure breakdown:
- cli-40 CLI-19: verifier_fail [fail] (CLI-19: Did not satisfy the scenario requirements. (score=25; correctness=0/2; efficiency=2/2; discipline=0/2; commandCount=1; note=slice.hex did not match the expected byte-for-byte content.))
- hermesagent-20 HA-19: verifier_fail [fail] (Hermes retried deployment partially, but the corrective-action trace or final success was incomplete.)
```

</details>
