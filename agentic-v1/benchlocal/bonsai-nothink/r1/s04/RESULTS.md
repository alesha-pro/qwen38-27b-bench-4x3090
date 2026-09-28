## Quality bench, thinking off, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 3 / 5 | 60% | — | — | 47.37s | 77.51s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | — | — | 87.78s | 97.43s | ok; partial — 2 of 20 selected

TOTAL | 4 / 7 | 57% |  |  |  |  |

Equivalent to: 86/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19416/v1, model: bench, thinking=off, 2026-09-28T10:21:41.986081Z) [PARTIAL SELECTION: 7 scenarios] ===

  [1/5] CLI-05 ✗ verifier_fail fail (9.0s)
  [2/5] CLI-13 ✗ verifier_fail fail (5.2s)
  [3/5] CLI-21 ✓ passed pass@1 (77.5s)
  [4/5] CLI-29 ✓ passed pass@1 (57.8s)
  [5/5] CLI-37 ✓ passed pass@1 (47.4s)
cli-40 (v1.0.2) | 3 / 5 | 60% | 47.37s | ok; partial — 5 of 40 selected
  [1/2] HA-05 ✓ passed pass@1 (97.4s)
  [2/2] HA-13 ✗ verifier_fail fail (78.1s)
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | 87.78s | ok; partial — 2 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 3 / 5 | 60% | 47.37s | 77.51s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | 87.78s | 97.43s | ok; partial — 2 of 20 selected

TOTAL | 4 / 7 | 57% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 39 (0.0%) | — | — | message.content=2, multi_turn=3
hermesagent-20 | — | — | — | multi_turn=2

Failure breakdown:
- cli-40 CLI-05: verifier_fail [fail] (CLI-05: Did not satisfy the scenario requirements. (score=25; correctness=0/2; efficiency=2/2; discipline=0/2; commandCount=0; note=Missing solution block. redacted.txt is missing or unreadable: ENOENT: no such file or directory, open '/workspace/redacted.txt'))
- cli-40 CLI-13: verifier_fail [fail] (CLI-13: Did not satisfy the scenario requirements. (score=50; correctness=0/2; efficiency=2/2; discipline=2/2; commandCount=1; note=errors.txt did not contain the expected ERROR lines in file and source-line order.))
- hermesagent-20 HA-13: verifier_fail [fail] (Hermes failed the cron creation scenario.)
```

</details>
