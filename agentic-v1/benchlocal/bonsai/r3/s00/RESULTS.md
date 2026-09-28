## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 4 / 5 | 80% | — | — | 85.99s | 533.73s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 3 | 67% | — | — | 49.08s | 178.67s | ok; partial — 3 of 20 selected

TOTAL | 6 / 8 | 75% |  |  |  |  |

Equivalent to: 113/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19412/v1, model: bench, thinking=on, 2026-09-27T18:04:33.973545Z) [PARTIAL SELECTION: 8 scenarios] ===

  [1/5] CLI-01 ✓ passed pass@1 (16.0s)
  [2/5] CLI-09 ✓ passed pass@1 (374.8s)
  [3/5] CLI-17 ✓ passed pass@1 (533.7s)
  [4/5] CLI-25 ✓ passed pass@1 (86.0s)
  [5/5] CLI-33 ✗ verifier_fail fail (2.9s)
cli-40 (v1.0.2) | 4 / 5 | 80% | 85.99s | ok; partial — 5 of 40 selected
  [1/3] HA-01 ✓ passed pass@1 (15.8s)
  [2/3] HA-09 ✓ passed pass@1 (49.1s)
  [3/3] HA-17 ✗ verifier_fail fail (178.7s)
hermesagent-20 (v1.0.0) | 2 / 3 | 67% | 49.08s | ok; partial — 3 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 4 / 5 | 80% | 85.99s | 533.73s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 3 | 67% | 49.08s | 178.67s | ok; partial — 3 of 20 selected

TOTAL | 6 / 8 | 75% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 19 (0.0%) | — | — | message.content=4, multi_turn=1
hermesagent-20 | — | — | — | multi_turn=3

Failure breakdown:
- cli-40 CLI-33: verifier_fail [fail] (CLI-33: Did not satisfy the scenario requirements. (score=25; correctness=0/2; efficiency=2/2; discipline=0/2; commandCount=0; note=Missing solution block. results/alpha.done is missing or unreadable: ENOENT: no such file or directory, open '/workspace/results/alpha.done' results/count.txt is missing or unreadable: ENOENT: no such file or directory, open '/workspace/results/count.txt' data/tasks.sorted.txt is missing or unreadable: ENOENT: no such file or directory, open '/workspace/data/tasks.sorted.txt' The final task workspace contained unexpected files or bytes.))
- hermesagent-20 HA-17: verifier_fail [fail] (Hermes produced a merged result, but the delegation trace or artifact correctness was incomplete.)
```

</details>
