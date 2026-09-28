## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 3 / 5 | 60% | — | — | 162.51s | 1439.94s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 0 / 2 | 0% | — | — | 254.95s | 300.22s | ok; partial — 2 of 20 selected

TOTAL | 3 / 7 | 43% |  |  |  |  |

Equivalent to: 64/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19413/v1, model: bench, thinking=on, 2026-09-27T18:02:02.533221Z) [PARTIAL SELECTION: 7 scenarios] ===

  [1/5] CLI-08 ✗ verifier_fail fail (1439.9s)
  [2/5] CLI-16 ✓ passed pass@1 (22.4s)
  [3/5] CLI-24 ✓ passed pass@1 (162.5s)
  [4/5] CLI-32 ✗ verifier_fail fail (22.2s)
  [5/5] CLI-40 ✓ passed pass@1 (368.5s)
cli-40 (v1.0.2) | 3 / 5 | 60% | 162.51s | ok; partial — 5 of 40 selected
  [1/2] HA-08 ✗ verifier_fail fail (209.7s)
  [2/2] HA-16 ✗ agent_runner_timeout fail (300.2s)
hermesagent-20 (v1.0.0) | 0 / 2 | 0% | 254.95s | ok; partial — 2 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 3 / 5 | 60% | 162.51s | 1439.94s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 0 / 2 | 0% | 254.95s | 300.22s | ok; partial — 2 of 20 selected

TOTAL | 3 / 7 | 43% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 23 (0.0%) | — | — | message.content=3, multi_turn=2
hermesagent-20 | — | — | — | multi_turn=2

Failure breakdown:
- cli-40 CLI-08: verifier_fail [fail] (CLI-08: Did not satisfy the scenario requirements. (score=25; correctness=0/2; efficiency=2/2; discipline=0/2; commandCount=1; note=build/bin is missing or unreadable: ENOENT: no such file or directory, stat '/workspace/build/bin'))
- cli-40 CLI-32: verifier_fail [fail] (CLI-32: Did not satisfy the scenario requirements. (score=0; correctness=0/2; efficiency=0/2; discipline=0/2; commandCount=1; note=Applied or attempted a blanket chmod 777 across the project tree.))
- hermesagent-20 HA-08: verifier_fail [fail] (Hermes touched the browser flow, but the export artifact or verifier invariants were incomplete.)
- hermesagent-20 HA-16: agent_runner_timeout [fail] (HA-16: upstream /run-scenario exceeded 300s)
```

</details>
