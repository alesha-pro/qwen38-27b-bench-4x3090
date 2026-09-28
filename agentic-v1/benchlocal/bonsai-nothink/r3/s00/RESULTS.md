## Quality bench, thinking off, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 1 / 5 | 20% | — | — | 14.46s | 96.62s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 3 | 67% | — | — | 103.09s | 150.51s | ok; partial — 3 of 20 selected

TOTAL | 3 / 8 | 38% |  |  |  |  |

Equivalent to: 56/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19416/v1, model: bench, thinking=off, 2026-09-28T10:30:10.407329Z) [PARTIAL SELECTION: 8 scenarios] ===

  [1/5] CLI-01 ✗ verifier_fail fail (14.5s)
  [2/5] CLI-09 ✗ verifier_fail fail (18.8s)
  [3/5] CLI-17 ✗ verifier_fail fail (12.8s)
  [4/5] CLI-25 ✓ passed pass@1 (96.6s)
  [5/5] CLI-33 ✗ verifier_fail fail (1.4s)
cli-40 (v1.0.2) | 1 / 5 | 20% | 14.46s | ok; partial — 5 of 40 selected
  [1/3] HA-01 ✓ passed pass@1 (19.3s)
  [2/3] HA-09 ✓ passed pass@1 (150.5s)
  [3/3] HA-17 ✗ verifier_fail fail (103.1s)
hermesagent-20 (v1.0.0) | 2 / 3 | 67% | 103.09s | ok; partial — 3 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 1 / 5 | 20% | 14.46s | 96.62s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 3 | 67% | 103.09s | 150.51s | ok; partial — 3 of 20 selected

TOTAL | 3 / 8 | 38% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 15 (0.0%) | — | — | message.content=4, multi_turn=1
hermesagent-20 | — | — | — | multi_turn=3

Failure breakdown:
- cli-40 CLI-01: verifier_fail [fail] (CLI-01: Did not satisfy the scenario requirements. (score=50; correctness=0/2; efficiency=2/2; discipline=2/2; commandCount=1; note=top_ips.txt did not match the expected content.))
- cli-40 CLI-09: verifier_fail [fail] (CLI-09: Did not satisfy the scenario requirements. (score=25; correctness=0/2; efficiency=2/2; discipline=0/2; commandCount=1; note=The remaining duplicate-set survivors or their bytes did not match the expected oldest files.))
- cli-40 CLI-17: verifier_fail [fail] (CLI-17: Did not satisfy the scenario requirements. (score=13; correctness=0/2; efficiency=1/2; discipline=0/2; commandCount=4; note=out.tar.gz is missing or unreadable: ENOENT: no such file or directory, open '/workspace/out.tar.gz'))
- cli-40 CLI-33: verifier_fail [fail] (CLI-33: Did not satisfy the scenario requirements. (score=25; correctness=0/2; efficiency=2/2; discipline=0/2; commandCount=1; note=results/alpha.done is missing or unreadable: ENOENT: no such file or directory, open '/workspace/results/alpha.done' results/count.txt is missing or unreadable: ENOENT: no such file or directory, open '/workspace/results/count.txt' data/tasks.sorted.txt is missing or unreadable: ENOENT: no such file or directory, open '/workspace/data/tasks.sorted.txt' The final task workspace contained unexpected files or bytes.))
- hermesagent-20 HA-17: verifier_fail [fail] (Hermes failed the parallel delegation scenario.)
```

</details>
