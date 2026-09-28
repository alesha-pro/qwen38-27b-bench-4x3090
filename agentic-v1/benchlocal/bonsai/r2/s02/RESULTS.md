## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 2 / 5 | 40% | — | — | 88.91s | 970.53s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 3 | 67% | — | — | 50.57s | 105.24s | ok; partial — 3 of 20 selected

TOTAL | 4 / 8 | 50% |  |  |  |  |

Equivalent to: 75/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19412/v1, model: bench, thinking=on, 2026-09-27T17:49:00.157542Z) [PARTIAL SELECTION: 8 scenarios] ===

  [1/5] CLI-03 ✓ passed pass@1 (25.6s)
  [2/5] CLI-11 ✗ verifier_fail fail (970.5s)
  [3/5] CLI-19 ✗ verifier_fail fail (155.0s)
  [4/5] CLI-27 ✗ server_error pass@2 (88.9s)
  [5/5] CLI-35 ✓ passed pass@1 (4.4s)
cli-40 (v1.0.2) | pass@1 2 / 5 (40%) | pass@3 3 / 5 (60%) | 88.91s | ok; partial — 5 of 40 selected
  [1/3] HA-03 ✓ passed pass@1 (20.1s)
  [2/3] HA-11 ✓ passed pass@1 (50.6s)
  [3/3] HA-19 ✗ verifier_fail fail (105.2s)
hermesagent-20 (v1.0.0) | 2 / 3 | 67% | 50.57s | ok; partial — 3 of 20 selected

Pack | Pass@1 | Pass@3 | Flaky | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 2 / 5 (40%) | 3 / 5 (60%) | 1 | 88.91s | 970.53s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 3 (67%) | - | - | 50.57s | 105.24s | ok; partial — 3 of 20 selected

TOTAL | 4 / 8 (50%) | 3 / 5 (60%) | 1 |  |  |

Inline retry classification (clean pass@1 rows omitted):

Scenario | Label | Attempts | Pass@k credit
---|---|---:|---
cli-40/CLI-11 | fail | 1 | no
cli-40/CLI-19 | fail | 1 | no
cli-40/CLI-27 | pass@2 | 2 | yes
hermesagent-20/HA-19 | fail | 1 | no

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 19 (0.0%) | — | — | message.content=4, multi_turn=2
hermesagent-20 | — | — | — | multi_turn=3

Failure breakdown:
- cli-40 CLI-11: verifier_fail [fail] (CLI-11: Did not satisfy the scenario requirements. (score=25; correctness=0/2; efficiency=2/2; discipline=0/2; commandCount=1; note=top10.txt is missing or unreadable: ENOENT: no such file or directory, open '/workspace/top10.txt'))
- cli-40 CLI-19: verifier_fail [fail] (CLI-19: Did not satisfy the scenario requirements. (score=25; correctness=0/2; efficiency=2/2; discipline=0/2; commandCount=3; note=slice.hex did not match the expected byte-for-byte content.))
- cli-40 CLI-27: server_error [pass@2] (CLI-27: Error: Bash command timed out after 30s.
    at BashSession.waitForMarker (file:///app/verification/bash-session.mjs:109:11)
    at process.processTicksAndRejections (node:internal/process/task_queues:95:5)
    at async BashSession.run (file:///app/verification/bash-session.mjs:74:26)
    at async Module.verifyMultiRoundReplay (file:///app/verification/core.mjs:946:22)
    at async file:///app/[eval1]:3:28)
- hermesagent-20 HA-19: verifier_fail [fail] (Hermes retried deployment partially, but the corrective-action trace or final success was incomplete.)
```

</details>
