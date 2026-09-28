## Quality bench, thinking off, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 2 / 5 | 40% | — | — | 11.14s | 78.03s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 2 | 100% | — | — | 154.10s | 260.98s | ok; partial — 2 of 20 selected

TOTAL | 4 / 7 | 57% |  |  |  |  |

Equivalent to: 86/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19416/v1, model: bench, thinking=off, 2026-09-28T10:28:38.048877Z) [PARTIAL SELECTION: 7 scenarios] ===

  [1/5] CLI-07 ✗ verifier_fail fail (4.1s)
  [2/5] CLI-15 ✗ verifier_fail fail (6.3s)
  [3/5] CLI-23 ✓ passed pass@1 (78.0s)
  [4/5] CLI-31 ✗ verifier_fail fail (11.1s)
  [5/5] CLI-39 ✓ passed pass@1 (47.2s)
cli-40 (v1.0.2) | 2 / 5 | 40% | 11.14s | ok; partial — 5 of 40 selected
  [1/2] HA-07 ✓ passed pass@1 (261.0s)
  [2/2] HA-15 ✓ passed pass@1 (47.2s)
hermesagent-20 (v1.0.0) | 2 / 2 | 100% | 154.10s | ok; partial — 2 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 2 / 5 | 40% | 11.14s | 78.03s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 2 | 100% | 154.10s | 260.98s | ok; partial — 2 of 20 selected

TOTAL | 4 / 7 | 57% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 24 (0.0%) | — | — | message.content=3, multi_turn=2
hermesagent-20 | — | — | — | multi_turn=2

Failure breakdown:
- cli-40 CLI-07: verifier_fail [fail] (CLI-07: Did not satisfy the scenario requirements. (score=50; correctness=0/2; efficiency=2/2; discipline=2/2; commandCount=2; note=The archive, remaining input files, or file bytes did not match the expected age-based move.))
- cli-40 CLI-15: verifier_fail [fail] (CLI-15: Did not satisfy the scenario requirements. (score=50; correctness=0/2; efficiency=2/2; discipline=2/2; commandCount=2; note=answer.txt is missing or unreadable: ENOENT: no such file or directory, open '/workspace/answer.txt'))
- cli-40 CLI-31: verifier_fail [fail] (CLI-31: Did not satisfy the scenario requirements. (score=0; correctness=0/2; efficiency=0/2; discipline=0/2; commandCount=1; note=Submitted a blanket destructive delete.))
```

</details>
