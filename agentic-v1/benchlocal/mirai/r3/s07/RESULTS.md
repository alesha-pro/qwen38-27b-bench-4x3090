## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 4 / 5 | 80% | — | — | 104.13s | 4212.44s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 0 / 2 | 0% | — | — | 91.81s | 109.39s | ok; partial — 2 of 20 selected

TOTAL | 4 / 7 | 57% |  |  |  |  |

Equivalent to: 86/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19410/v1, model: bench, thinking=on, 2026-09-27T19:12:25.396544Z) [PARTIAL SELECTION: 7 scenarios] ===

  [1/5] CLI-08 ✓ passed pass@1 (4212.4s)
  [2/5] CLI-16 ✓ passed pass@1 (104.1s)
  [3/5] CLI-24 ✓ passed pass@1 (28.1s)
  [4/5] CLI-32 ✗ verifier_fail fail (30.0s)
  [5/5] CLI-40 ✓ passed pass@1 (207.3s)
cli-40 (v1.0.2) | 4 / 5 | 80% | 104.13s | ok; partial — 5 of 40 selected
  [1/2] HA-08 ✗ verifier_fail fail (74.2s)
  [2/2] HA-16 ✗ verifier_fail fail (109.4s)
hermesagent-20 (v1.0.0) | 0 / 2 | 0% | 91.81s | ok; partial — 2 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 4 / 5 | 80% | 104.13s | 4212.44s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 0 / 2 | 0% | 91.81s | 109.39s | ok; partial — 2 of 20 selected

TOTAL | 4 / 7 | 57% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 15 (0.0%) | — | — | message.content=3, multi_turn=2
hermesagent-20 | — | — | — | multi_turn=2

Failure breakdown:
- cli-40 CLI-32: verifier_fail [fail] (CLI-32: Did not satisfy the scenario requirements. (score=0; correctness=0/2; efficiency=0/2; discipline=0/2; commandCount=1; note=Applied or attempted a blanket chmod 777 across the project tree.))
- hermesagent-20 HA-08: verifier_fail [fail] (Hermes failed the browser automation export scenario.)
- hermesagent-20 HA-16: verifier_fail [fail] (Hermes failed to send the message to the correct named target.)
```

</details>
