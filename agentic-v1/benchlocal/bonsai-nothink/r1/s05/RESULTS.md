## Quality bench, thinking off, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 4 / 5 | 80% | — | — | 33.09s | 82.04s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 2 | 100% | — | — | 41.40s | 61.76s | ok; partial — 2 of 20 selected

TOTAL | 6 / 7 | 86% |  |  |  |  |

Equivalent to: 129/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19417/v1, model: bench, thinking=off, 2026-09-28T10:21:41.984611Z) [PARTIAL SELECTION: 7 scenarios] ===

  [1/5] CLI-06 ✓ passed pass@1 (4.1s)
  [2/5] CLI-14 ✗ verifier_fail fail (4.3s)
  [3/5] CLI-22 ✓ passed pass@1 (45.8s)
  [4/5] CLI-30 ✓ passed pass@1 (33.1s)
  [5/5] CLI-38 ✓ passed pass@1 (82.0s)
cli-40 (v1.0.2) | 4 / 5 | 80% | 33.09s | ok; partial — 5 of 40 selected
  [1/2] HA-06 ✓ passed pass@1 (61.8s)
  [2/2] HA-14 ✓ passed pass@1 (21.0s)
hermesagent-20 (v1.0.0) | 2 / 2 | 100% | 41.40s | ok; partial — 2 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 4 / 5 | 80% | 33.09s | 82.04s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 2 | 100% | 41.40s | 61.76s | ok; partial — 2 of 20 selected

TOTAL | 6 / 7 | 86% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 36 (0.0%) | — | — | message.content=2, multi_turn=3
hermesagent-20 | — | — | — | multi_turn=2

Failure breakdown:
- cli-40 CLI-14: verifier_fail [fail] (CLI-14: Did not satisfy the scenario requirements. (score=50; correctness=0/2; efficiency=2/2; discipline=2/2; commandCount=1; note=alice_heavy.txt did not match the expected content.))
```

</details>
