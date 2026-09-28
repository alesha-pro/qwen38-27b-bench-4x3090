## Quality bench, thinking off, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 2 / 5 | 40% | — | — | 5.52s | 63.18s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | — | — | 148.59s | 257.73s | ok; partial — 2 of 20 selected

TOTAL | 3 / 7 | 43% |  |  |  |  |

Equivalent to: 64/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19416/v1, model: bench, thinking=off, 2026-09-28T10:21:41.982038Z) [PARTIAL SELECTION: 7 scenarios] ===

  [1/5] CLI-07 ✗ verifier_fail fail (5.5s)
  [2/5] CLI-15 ✗ verifier_fail fail (4.6s)
  [3/5] CLI-23 ✓ passed pass@1 (61.9s)
  [4/5] CLI-31 ✗ verifier_fail fail (1.2s)
  [5/5] CLI-39 ✓ passed pass@1 (63.2s)
cli-40 (v1.0.2) | 2 / 5 | 40% | 5.52s | ok; partial — 5 of 40 selected
  [1/2] HA-07 ✗ verifier_fail fail (257.7s)
  [2/2] HA-15 ✓ passed pass@1 (39.4s)
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | 148.59s | ok; partial — 2 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 2 / 5 | 40% | 5.52s | 63.18s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | 148.59s | 257.73s | ok; partial — 2 of 20 selected

TOTAL | 3 / 7 | 43% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 33 (0.0%) | — | — | message.content=3, multi_turn=2
hermesagent-20 | — | — | — | multi_turn=2

Failure breakdown:
- cli-40 CLI-07: verifier_fail [fail] (CLI-07: Did not satisfy the scenario requirements. (score=50; correctness=0/2; efficiency=2/2; discipline=2/2; commandCount=4; note=The archive, remaining input files, or file bytes did not match the expected age-based move.))
- cli-40 CLI-15: verifier_fail [fail] (CLI-15: Did not satisfy the scenario requirements. (score=25; correctness=0/2; efficiency=2/2; discipline=0/2; commandCount=2; note=answer.txt is missing or unreadable: ENOENT: no such file or directory, open '/workspace/answer.txt'))
- cli-40 CLI-31: verifier_fail [fail] (CLI-31: Did not satisfy the scenario requirements. (score=0; correctness=0/2; efficiency=0/2; discipline=0/2; commandCount=1; note=Submitted a blanket destructive delete.))
- hermesagent-20 HA-07: verifier_fail [fail] (Hermes failed the programmatic execute_code summarization scenario.)
```

</details>
