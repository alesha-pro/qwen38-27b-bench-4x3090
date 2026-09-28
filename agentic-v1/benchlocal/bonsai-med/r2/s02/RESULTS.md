## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 4 / 5 | 80% | — | — | 86.32s | 1022.52s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 3 | 67% | — | — | 88.83s | 171.50s | ok; partial — 3 of 20 selected

TOTAL | 6 / 8 | 75% |  |  |  |  |

Equivalent to: 113/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19414/v1, model: bench, thinking=on, 2026-09-28T10:26:54.511130Z) [PARTIAL SELECTION: 8 scenarios] ===

  [1/5] CLI-03 ✓ passed pass@1 (22.8s)
  [2/5] CLI-11 ✓ passed pass@1 (1022.5s)
  [3/5] CLI-19 ✗ verifier_fail fail (86.3s)
  [4/5] CLI-27 ✓ passed pass@1 (187.4s)
  [5/5] CLI-35 ✓ passed pass@1 (9.5s)
cli-40 (v1.0.2) | 4 / 5 | 80% | 86.32s | ok; partial — 5 of 40 selected
  [1/3] HA-03 ✓ passed pass@1 (18.5s)
  [2/3] HA-11 ✓ passed pass@1 (88.8s)
  [3/3] HA-19 ✗ verifier_fail fail (171.5s)
hermesagent-20 (v1.0.0) | 2 / 3 | 67% | 88.83s | ok; partial — 3 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 4 / 5 | 80% | 86.32s | 1022.52s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 3 | 67% | 88.83s | 171.50s | ok; partial — 3 of 20 selected

TOTAL | 6 / 8 | 75% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 11 (0.0%) | — | — | message.content=4, multi_turn=1
hermesagent-20 | — | — | — | multi_turn=3

Failure breakdown:
- cli-40 CLI-19: verifier_fail [fail] (CLI-19: Did not satisfy the scenario requirements. (score=25; correctness=0/2; efficiency=2/2; discipline=0/2; commandCount=0; note=Missing solution block. slice.hex is missing or unreadable: ENOENT: no such file or directory, open '/workspace/slice.hex'))
- hermesagent-20 HA-19: verifier_fail [fail] (Hermes retried deployment partially, but the corrective-action trace or final success was incomplete.)
```

</details>
