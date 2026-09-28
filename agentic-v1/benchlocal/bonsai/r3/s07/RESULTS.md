## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 1 / 5 | 20% | — | — | 60.16s | 408.79s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 0 / 2 | 0% | — | — | 91.36s | 115.40s | ok; partial — 2 of 20 selected

TOTAL | 1 / 7 | 14% |  |  |  |  |

Equivalent to: 21/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19413/v1, model: bench, thinking=on, 2026-09-27T18:38:58.390915Z) [PARTIAL SELECTION: 7 scenarios] ===

  [1/5] CLI-08 ✗ verifier_fail fail (8.3s)
  [2/5] CLI-16 ✗ verifier_fail fail (41.3s)
  [3/5] CLI-24 ✓ passed pass@1 (408.8s)
  [4/5] CLI-32 ✗ verifier_fail fail (60.2s)
  [5/5] CLI-40 ✗ verifier_fail fail (260.8s)
cli-40 (v1.0.2) | 1 / 5 | 20% | 60.16s | ok; partial — 5 of 40 selected
  [1/2] HA-08 ✗ verifier_fail fail (67.3s)
  [2/2] HA-16 ✗ verifier_fail fail (115.4s)
hermesagent-20 (v1.0.0) | 0 / 2 | 0% | 91.36s | ok; partial — 2 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 1 / 5 | 20% | 60.16s | 408.79s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 0 / 2 | 0% | 91.36s | 115.40s | ok; partial — 2 of 20 selected

TOTAL | 1 / 7 | 14% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 31 (0.0%) | — | — | message.content=3, multi_turn=2
hermesagent-20 | — | — | — | multi_turn=2

Failure breakdown:
- cli-40 CLI-08: verifier_fail [fail] (CLI-08: Did not satisfy the scenario requirements. (score=25; correctness=0/2; efficiency=2/2; discipline=0/2; commandCount=0; note=Missing solution block. build is missing or unreadable: ENOENT: no such file or directory, stat '/workspace/build'))
- cli-40 CLI-16: verifier_fail [fail] (CLI-16: Did not satisfy the scenario requirements. (score=25; correctness=0/2; efficiency=2/2; discipline=0/2; commandCount=2; note=The extracted directory contained the wrong files, target path, or target bytes.))
- cli-40 CLI-32: verifier_fail [fail] (CLI-32: Did not satisfy the scenario requirements. (score=0; correctness=0/2; efficiency=0/2; discipline=0/2; commandCount=2; note=Applied or attempted a blanket chmod 777 across the project tree.))
- cli-40 CLI-40: verifier_fail [fail] (CLI-40: Did not satisfy the scenario requirements. (score=25; correctness=0/2; efficiency=0/2; discipline=2/2; turnsUsed=12; note=answer.txt did not match the expected content.))
- hermesagent-20 HA-08: verifier_fail [fail] (Hermes touched the browser flow, but the export artifact or verifier invariants were incomplete.)
- hermesagent-20 HA-16: verifier_fail [fail] (Hermes failed to send the message to the correct named target.)
```

</details>
