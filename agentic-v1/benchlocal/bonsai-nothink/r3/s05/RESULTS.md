## Quality bench, thinking off, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 3 / 5 | 60% | — | — | 33.73s | 71.86s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | — | — | 26.03s | 39.26s | ok; partial — 2 of 20 selected

TOTAL | 4 / 7 | 57% |  |  |  |  |

Equivalent to: 86/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19417/v1, model: bench, thinking=off, 2026-09-28T10:33:25.468219Z) [PARTIAL SELECTION: 7 scenarios] ===

  [1/5] CLI-06 ✗ verifier_fail fail (9.0s)
  [2/5] CLI-14 ✗ verifier_fail fail (1.8s)
  [3/5] CLI-22 ✓ passed pass@1 (71.9s)
  [4/5] CLI-30 ✓ passed pass@1 (36.5s)
  [5/5] CLI-38 ✓ passed pass@1 (33.7s)
cli-40 (v1.0.2) | 3 / 5 | 60% | 33.73s | ok; partial — 5 of 40 selected
  [1/2] HA-06 ✗ verifier_fail fail (39.3s)
  [2/2] HA-14 ✓ passed pass@1 (12.8s)
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | 26.03s | ok; partial — 2 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 3 / 5 | 60% | 33.73s | 71.86s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | 26.03s | 39.26s | ok; partial — 2 of 20 selected

TOTAL | 4 / 7 | 57% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 43 (0.0%) | — | — | message.content=2, multi_turn=3
hermesagent-20 | — | — | — | multi_turn=2

Failure breakdown:
- cli-40 CLI-06: verifier_fail [fail] (CLI-06: Did not satisfy the scenario requirements. (score=25; correctness=0/2; efficiency=2/2; discipline=0/2; commandCount=0; note=Missing solution block. The final filesystem tree did not match the expected renamed state.))
- cli-40 CLI-14: verifier_fail [fail] (CLI-14: Did not satisfy the scenario requirements. (score=50; correctness=0/2; efficiency=2/2; discipline=2/2; commandCount=1; note=alice_heavy.txt did not match the expected content.))
- hermesagent-20 HA-06: verifier_fail [fail] (Hermes failed the background process management scenario.)
```

</details>
