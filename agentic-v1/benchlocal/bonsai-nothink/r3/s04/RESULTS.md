## Quality bench, thinking off, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 3 / 5 | 60% | — | — | 31.57s | 176.53s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 0 / 2 | 0% | — | — | 36.82s | 53.52s | ok; partial — 2 of 20 selected

TOTAL | 3 / 7 | 43% |  |  |  |  |

Equivalent to: 64/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19416/v1, model: bench, thinking=off, 2026-09-28T10:32:16.331292Z) [PARTIAL SELECTION: 7 scenarios] ===

  [1/5] CLI-05 ✗ verifier_fail fail (16.4s)
  [2/5] CLI-13 ✗ verifier_fail fail (9.1s)
  [3/5] CLI-21 ✓ passed pass@1 (176.5s)
  [4/5] CLI-29 ✓ passed pass@1 (90.2s)
  [5/5] CLI-37 ✓ passed pass@1 (31.6s)
cli-40 (v1.0.2) | 3 / 5 | 60% | 31.57s | ok; partial — 5 of 40 selected
  [1/2] HA-05 ✗ verifier_fail fail (53.5s)
  [2/2] HA-13 ✗ verifier_fail fail (20.1s)
hermesagent-20 (v1.0.0) | 0 / 2 | 0% | 36.82s | ok; partial — 2 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 3 / 5 | 60% | 31.57s | 176.53s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 0 / 2 | 0% | 36.82s | 53.52s | ok; partial — 2 of 20 selected

TOTAL | 3 / 7 | 43% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 47 (0.0%) | — | — | message.content=2, multi_turn=3
hermesagent-20 | — | — | — | multi_turn=2

Failure breakdown:
- cli-40 CLI-05: verifier_fail [fail] (CLI-05: Did not satisfy the scenario requirements. (score=50; correctness=0/2; efficiency=2/2; discipline=2/2; commandCount=1; note=redacted.txt did not match the expected content.))
- cli-40 CLI-13: verifier_fail [fail] (CLI-13: Did not satisfy the scenario requirements. (score=50; correctness=0/2; efficiency=2/2; discipline=2/2; commandCount=1; note=errors.txt is missing or unreadable: ENOENT: no such file or directory, open '/workspace/errors.txt'))
- hermesagent-20 HA-05: verifier_fail [fail] (Hermes changed the project, but the fix or the final verification trace was incomplete.)
- hermesagent-20 HA-13: verifier_fail [fail] (Hermes failed the cron creation scenario.)
```

</details>
