## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 3 / 5 | 60% | — | — | 124.02s | 1542.14s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | — | — | 76.93s | 93.91s | ok; partial — 2 of 20 selected

TOTAL | 4 / 7 | 57% |  |  |  |  |

Equivalent to: 86/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19410/v1, model: bench, thinking=on, 2026-09-27T17:46:01.664324Z) [PARTIAL SELECTION: 7 scenarios] ===

  [1/5] CLI-08 ✗ verifier_fail fail (1542.1s)
  [2/5] CLI-16 ✓ passed pass@1 (537.5s)
  [3/5] CLI-24 ✓ passed pass@1 (53.8s)
  [4/5] CLI-32 ✗ verifier_fail fail (16.4s)
  [5/5] CLI-40 ✓ passed pass@1 (124.0s)
cli-40 (v1.0.2) | 3 / 5 | 60% | 124.02s | ok; partial — 5 of 40 selected
  [1/2] HA-08 ✓ passed pass@1 (59.9s)
  [2/2] HA-16 ✗ verifier_fail fail (93.9s)
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | 76.93s | ok; partial — 2 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 3 / 5 | 60% | 124.02s | 1542.14s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | 76.93s | 93.91s | ok; partial — 2 of 20 selected

TOTAL | 4 / 7 | 57% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 12 (0.0%) | — | — | message.content=2, message.reasoning=1, multi_turn=2
hermesagent-20 | — | — | — | multi_turn=2

Failure breakdown:
- cli-40 CLI-08: verifier_fail [fail] (CLI-08: Did not satisfy the scenario requirements. (score=25; correctness=0/2; efficiency=2/2; discipline=0/2; commandCount=0; note=Missing solution block. build is missing or unreadable: ENOENT: no such file or directory, stat '/workspace/build'))
- cli-40 CLI-32: verifier_fail [fail] (CLI-32: Did not satisfy the scenario requirements. (score=0; correctness=0/2; efficiency=0/2; discipline=0/2; commandCount=1; note=Applied or attempted a blanket chmod 777 across the project tree.))
- hermesagent-20 HA-16: verifier_fail [fail] (Hermes failed to send the message to the correct named target.)
```

</details>
