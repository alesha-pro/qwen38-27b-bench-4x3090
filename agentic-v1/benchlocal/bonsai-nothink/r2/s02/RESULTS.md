## Quality bench, thinking off, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 2 / 5 | 40% | — | — | 4.88s | 55.79s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 3 | 67% | — | — | 45.91s | 103.86s | ok; partial — 3 of 20 selected

TOTAL | 4 / 8 | 50% |  |  |  |  |

Equivalent to: 75/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19416/v1, model: bench, thinking=off, 2026-09-28T10:26:29.056744Z) [PARTIAL SELECTION: 8 scenarios] ===

  [1/5] CLI-03 ✗ verifier_fail fail (4.9s)
  [2/5] CLI-11 ✗ verifier_fail fail (8.7s)
  [3/5] CLI-19 ✗ verifier_fail fail (4.7s)
  [4/5] CLI-27 ✓ passed pass@1 (55.8s)
  [5/5] CLI-35 ✓ passed pass@1 (3.7s)
cli-40 (v1.0.2) | 2 / 5 | 40% | 4.88s | ok; partial — 5 of 40 selected
  [1/3] HA-03 ✓ passed pass@1 (6.7s)
  [2/3] HA-11 ✓ passed pass@1 (45.9s)
  [3/3] HA-19 ✗ verifier_fail fail (103.9s)
hermesagent-20 (v1.0.0) | 2 / 3 | 67% | 45.91s | ok; partial — 3 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 2 / 5 | 40% | 4.88s | 55.79s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 3 | 67% | 45.91s | 103.86s | ok; partial — 3 of 20 selected

TOTAL | 4 / 8 | 50% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 11 (0.0%) | — | — | message.content=4, multi_turn=1
hermesagent-20 | — | — | — | multi_turn=3

Failure breakdown:
- cli-40 CLI-03: verifier_fail [fail] (CLI-03: Did not satisfy the scenario requirements. (score=25; correctness=0/2; efficiency=2/2; discipline=0/2; commandCount=0; note=Missing solution block. data.json is missing or unreadable: ENOENT: no such file or directory, open '/workspace/data.json'))
- cli-40 CLI-11: verifier_fail [fail] (CLI-11: Did not satisfy the scenario requirements. (score=50; correctness=0/2; efficiency=2/2; discipline=2/2; commandCount=1; note=top10.txt is missing or unreadable: ENOENT: no such file or directory, open '/workspace/top10.txt'))
- cli-40 CLI-19: verifier_fail [fail] (CLI-19: Did not satisfy the scenario requirements. (score=25; correctness=0/2; efficiency=2/2; discipline=0/2; commandCount=2; note=slice.hex did not match the expected byte-for-byte content.))
- hermesagent-20 HA-19: verifier_fail [fail] (Hermes retried deployment partially, but the corrective-action trace or final success was incomplete.)
```

</details>
