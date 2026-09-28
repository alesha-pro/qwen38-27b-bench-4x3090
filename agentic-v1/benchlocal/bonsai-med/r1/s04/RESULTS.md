## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 3 / 5 | 60% | — | — | 95.70s | 370.10s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | — | — | 260.88s | 300.17s | ok; partial — 2 of 20 selected

TOTAL | 4 / 7 | 57% |  |  |  |  |

Equivalent to: 86/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19414/v1, model: bench, thinking=on, 2026-09-28T10:22:11.690362Z) [PARTIAL SELECTION: 7 scenarios] ===

  [1/5] CLI-05 ✗ verifier_fail fail (95.7s)
  [2/5] CLI-13 ✗ verifier_fail fail (32.6s)
  [3/5] CLI-21 ✓ passed pass@1 (78.6s)
  [4/5] CLI-29 ✓ passed pass@1 (370.1s)
  [5/5] CLI-37 ✓ passed pass@1 (136.0s)
cli-40 (v1.0.2) | 3 / 5 | 60% | 95.70s | ok; partial — 5 of 40 selected
  [1/2] HA-05 ✓ passed pass@1 (221.6s)
  [2/2] HA-13 ✗ agent_runner_timeout fail (300.2s)
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | 260.88s | ok; partial — 2 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 3 / 5 | 60% | 95.70s | 370.10s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | 260.88s | 300.17s | ok; partial — 2 of 20 selected

TOTAL | 4 / 7 | 57% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 39 (0.0%) | — | — | message.content=2, multi_turn=3
hermesagent-20 | — | — | — | multi_turn=2

Failure breakdown:
- cli-40 CLI-05: verifier_fail [fail] (CLI-05: Did not satisfy the scenario requirements. (score=25; correctness=0/2; efficiency=2/2; discipline=0/2; commandCount=1; note=redacted.txt did not match the expected content.))
- cli-40 CLI-13: verifier_fail [fail] (CLI-13: Did not satisfy the scenario requirements. (score=25; correctness=0/2; efficiency=2/2; discipline=0/2; commandCount=1; note=errors.txt did not contain the expected ERROR lines in file and source-line order.))
- hermesagent-20 HA-13: agent_runner_timeout [fail] (HA-13: upstream /run-scenario exceeded 300s)
```

</details>
