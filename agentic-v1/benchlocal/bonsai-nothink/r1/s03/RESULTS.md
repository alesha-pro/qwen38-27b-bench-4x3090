## Quality bench, thinking off, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 3 / 5 | 60% | — | — | 5.40s | 55.61s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 3 | 67% | — | — | 54.52s | 75.92s | ok; partial — 3 of 20 selected

TOTAL | 5 / 8 | 62% |  |  |  |  |

Equivalent to: 94/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19417/v1, model: bench, thinking=off, 2026-09-28T10:21:41.982855Z) [PARTIAL SELECTION: 8 scenarios] ===

  [1/5] CLI-04 ✓ passed pass@1 (3.2s)
  [2/5] CLI-12 ✗ verifier_fail fail (2.9s)
  [3/5] CLI-20 ✗ verifier_fail fail (5.4s)
  [4/5] CLI-28 ✓ passed pass@1 (26.4s)
  [5/5] CLI-36 ✓ passed pass@1 (55.6s)
cli-40 (v1.0.2) | 3 / 5 | 60% | 5.40s | ok; partial — 5 of 40 selected
  [1/3] HA-04 ✓ passed pass@1 (75.9s)
  [2/3] HA-12 ✓ passed pass@1 (32.4s)
  [3/3] HA-20 ✗ verifier_fail fail (54.5s)
hermesagent-20 (v1.0.0) | 2 / 3 | 67% | 54.52s | ok; partial — 3 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 3 / 5 | 60% | 5.40s | 55.61s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 3 | 67% | 54.52s | 75.92s | ok; partial — 3 of 20 selected

TOTAL | 5 / 8 | 62% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 23 (0.0%) | — | — | message.content=3, multi_turn=2
hermesagent-20 | — | — | — | multi_turn=3

Failure breakdown:
- cli-40 CLI-12: verifier_fail [fail] (CLI-12: Did not satisfy the scenario requirements. (score=25; correctness=0/2; efficiency=2/2; discipline=0/2; commandCount=1; note=totals.csv is missing or unreadable: ENOENT: no such file or directory, open '/workspace/totals.csv'))
- cli-40 CLI-20: verifier_fail [fail] (CLI-20: Did not satisfy the scenario requirements. (score=50; correctness=0/2; efficiency=2/2; discipline=2/2; commandCount=4; note=new.tar did not match the expected repacked archive.))
- hermesagent-20 HA-20: verifier_fail [fail] (Hermes failed the ambiguous destructive-request scenario.)
```

</details>
