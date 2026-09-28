## Quality bench, thinking off, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 4 / 5 | 80% | — | — | 102.43s | 124.91s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | — | — | 96.38s | 139.34s | ok; partial — 2 of 20 selected

TOTAL | 5 / 7 | 71% |  |  |  |  |

Equivalent to: 107/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19416/v1, model: bench, thinking=off, 2026-09-28T10:26:42.395001Z) [PARTIAL SELECTION: 7 scenarios] ===

  [1/5] CLI-05 ✗ verifier_fail fail (1.8s)
  [2/5] CLI-13 ✓ passed pass@1 (4.4s)
  [3/5] CLI-21 ✓ passed pass@1 (102.4s)
  [4/5] CLI-29 ✓ passed pass@1 (124.9s)
  [5/5] CLI-37 ✓ passed pass@1 (115.6s)
cli-40 (v1.0.2) | 4 / 5 | 80% | 102.43s | ok; partial — 5 of 40 selected
  [1/2] HA-05 ✓ passed pass@1 (139.3s)
  [2/2] HA-13 ✗ verifier_fail fail (53.4s)
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | 96.38s | ok; partial — 2 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 4 / 5 | 80% | 102.43s | 124.91s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | 96.38s | 139.34s | ok; partial — 2 of 20 selected

TOTAL | 5 / 7 | 71% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 45 (0.0%) | — | — | message.content=2, multi_turn=3
hermesagent-20 | — | — | — | multi_turn=2

Failure breakdown:
- cli-40 CLI-05: verifier_fail [fail] (CLI-05: Did not satisfy the scenario requirements. (score=50; correctness=0/2; efficiency=2/2; discipline=2/2; commandCount=1; note=redacted.txt is missing or unreadable: ENOENT: no such file or directory, open '/workspace/redacted.txt'))
- hermesagent-20 HA-13: verifier_fail [fail] (Hermes failed the cron creation scenario.)
```

</details>
