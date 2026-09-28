## Quality bench, thinking off, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 2 / 5 | 40% | — | — | 5.60s | 57.48s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | — | — | 53.84s | 53.94s | ok; partial — 2 of 20 selected

TOTAL | 3 / 7 | 43% |  |  |  |  |

Equivalent to: 64/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19417/v1, model: bench, thinking=off, 2026-09-28T10:29:39.686622Z) [PARTIAL SELECTION: 7 scenarios] ===

  [1/5] CLI-08 ✗ verifier_fail fail (1.2s)
  [2/5] CLI-16 ✗ verifier_fail fail (5.6s)
  [3/5] CLI-24 ✓ passed pass@1 (36.4s)
  [4/5] CLI-32 ✗ verifier_fail fail (0.8s)
  [5/5] CLI-40 ✓ passed pass@1 (57.5s)
cli-40 (v1.0.2) | 2 / 5 | 40% | 5.60s | ok; partial — 5 of 40 selected
  [1/2] HA-08 ✓ passed pass@1 (53.7s)
  [2/2] HA-16 ✗ verifier_fail fail (53.9s)
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | 53.84s | ok; partial — 2 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 2 / 5 | 40% | 5.60s | 57.48s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | 53.84s | 53.94s | ok; partial — 2 of 20 selected

TOTAL | 3 / 7 | 43% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 30 (0.0%) | — | — | message.content=3, multi_turn=2
hermesagent-20 | — | — | — | multi_turn=2

Failure breakdown:
- cli-40 CLI-08: verifier_fail [fail] (CLI-08: Did not satisfy the scenario requirements. (score=25; correctness=0/2; efficiency=2/2; discipline=0/2; commandCount=0; note=Missing solution block. build is missing or unreadable: ENOENT: no such file or directory, stat '/workspace/build'))
- cli-40 CLI-16: verifier_fail [fail] (CLI-16: Did not satisfy the scenario requirements. (score=50; correctness=0/2; efficiency=2/2; discipline=2/2; commandCount=2; note=The extracted directory contained the wrong files, target path, or target bytes.))
- cli-40 CLI-32: verifier_fail [fail] (CLI-32: Did not satisfy the scenario requirements. (score=0; correctness=0/2; efficiency=0/2; discipline=0/2; commandCount=1; note=Applied or attempted a blanket chmod 777 across the project tree.))
- hermesagent-20 HA-16: verifier_fail [fail] (Hermes failed to send the message to the correct named target.)
```

</details>
