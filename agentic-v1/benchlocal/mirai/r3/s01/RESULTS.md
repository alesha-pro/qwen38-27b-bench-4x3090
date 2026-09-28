## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 4 / 5 | 80% | — | — | 269.00s | 332.48s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 3 / 3 | 100% | — | — | 58.91s | 252.10s | ok; partial — 3 of 20 selected

TOTAL | 7 / 8 | 88% |  |  |  |  |

Equivalent to: 131/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19410/v1, model: bench, thinking=on, 2026-09-27T18:39:20.588641Z) [PARTIAL SELECTION: 8 scenarios] ===

  [1/5] CLI-02 ✓ passed pass@1 (332.5s)
  [2/5] CLI-10 ✗ verifier_fail fail (331.0s)
  [3/5] CLI-18 ✓ passed pass@1 (9.1s)
  [4/5] CLI-26 ✓ passed pass@1 (21.6s)
  [5/5] CLI-34 ✓ passed pass@1 (269.0s)
cli-40 (v1.0.2) | 4 / 5 | 80% | 269.00s | ok; partial — 5 of 40 selected
  [1/3] HA-02 ✓ passed pass@1 (252.1s)
  [2/3] HA-10 ✓ passed pass@1 (58.9s)
  [3/3] HA-18 ✓ passed pass@1 (40.4s)
hermesagent-20 (v1.0.0) | 3 / 3 | 100% | 58.91s | ok; partial — 3 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 4 / 5 | 80% | 269.00s | 332.48s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 3 / 3 | 100% | 58.91s | 252.10s | ok; partial — 3 of 20 selected

TOTAL | 7 / 8 | 88% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 8 (0.0%) | — | — | message.content=4, multi_turn=1
hermesagent-20 | — | — | — | multi_turn=3

Failure breakdown:
- cli-40 CLI-10: verifier_fail [fail] (CLI-10: Did not satisfy the scenario requirements. (score=38; correctness=0/2; efficiency=1/2; discipline=2/2; commandCount=12; note=The flat directory did not contain the expected collision-safe filenames, bytes, or emptied source file tree.))
```

</details>
