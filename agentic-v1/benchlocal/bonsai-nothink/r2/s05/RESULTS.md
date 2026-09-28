## Quality bench, thinking off, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 4 / 5 | 80% | — | — | 40.21s | 70.11s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 2 | 100% | — | — | 43.96s | 74.01s | ok; partial — 2 of 20 selected

TOTAL | 6 / 7 | 86% |  |  |  |  |

Equivalent to: 129/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19417/v1, model: bench, thinking=off, 2026-09-28T10:27:49.808989Z) [PARTIAL SELECTION: 7 scenarios] ===

  [1/5] CLI-06 ✓ passed pass@1 (1.6s)
  [2/5] CLI-14 ✗ verifier_fail fail (1.8s)
  [3/5] CLI-22 ✓ passed pass@1 (40.2s)
  [4/5] CLI-30 ✓ passed pass@1 (45.5s)
  [5/5] CLI-38 ✓ passed pass@1 (70.1s)
cli-40 (v1.0.2) | 4 / 5 | 80% | 40.21s | ok; partial — 5 of 40 selected
  [1/2] HA-06 ✓ passed pass@1 (74.0s)
  [2/2] HA-14 ✓ passed pass@1 (13.9s)
hermesagent-20 (v1.0.0) | 2 / 2 | 100% | 43.96s | ok; partial — 2 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 4 / 5 | 80% | 40.21s | 70.11s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 2 | 100% | 43.96s | 74.01s | ok; partial — 2 of 20 selected

TOTAL | 6 / 7 | 86% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 35 (0.0%) | — | — | message.content=2, multi_turn=3
hermesagent-20 | — | — | — | multi_turn=2

Failure breakdown:
- cli-40 CLI-14: verifier_fail [fail] (CLI-14: Did not satisfy the scenario requirements. (score=25; correctness=0/2; efficiency=2/2; discipline=0/2; commandCount=1; note=alice_heavy.txt did not match the expected content.))
```

</details>
