## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 4 / 5 | 80% | — | — | 170.60s | 278.07s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | — | — | 116.02s | 159.57s | ok; partial — 2 of 20 selected

TOTAL | 5 / 7 | 71% |  |  |  |  |

Equivalent to: 107/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19414/v1, model: bench, thinking=on, 2026-09-28T10:53:58.546593Z) [PARTIAL SELECTION: 7 scenarios] ===

  [1/5] CLI-05 ✓ passed pass@1 (278.1s)
  [2/5] CLI-13 ✗ verifier_fail fail (70.8s)
  [3/5] CLI-21 ✓ passed pass@1 (176.9s)
  [4/5] CLI-29 ✓ passed pass@1 (133.5s)
  [5/5] CLI-37 ✓ passed pass@1 (170.6s)
cli-40 (v1.0.2) | 4 / 5 | 80% | 170.60s | ok; partial — 5 of 40 selected
  [1/2] HA-05 ✓ passed pass@1 (72.5s)
  [2/2] HA-13 ✗ verifier_fail fail (159.6s)
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | 116.02s | ok; partial — 2 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 4 / 5 | 80% | 170.60s | 278.07s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | 116.02s | 159.57s | ok; partial — 2 of 20 selected

TOTAL | 5 / 7 | 71% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 46 (0.0%) | — | — | message.content=2, multi_turn=3
hermesagent-20 | — | — | — | multi_turn=2

Failure breakdown:
- cli-40 CLI-13: verifier_fail [fail] (CLI-13: Did not satisfy the scenario requirements. (score=25; correctness=0/2; efficiency=2/2; discipline=0/2; commandCount=0; note=Missing solution block. errors.txt is missing or unreadable: ENOENT: no such file or directory, open '/workspace/errors.txt'))
- hermesagent-20 HA-13: verifier_fail [fail] (Hermes failed the cron creation scenario.)
```

</details>
