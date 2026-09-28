## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 4 / 5 | 80% | — | — | 57.36s | 1473.52s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 3 | 67% | — | — | 68.01s | 80.12s | ok; partial — 3 of 20 selected

TOTAL | 6 / 8 | 75% |  |  |  |  |

Equivalent to: 113/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19410/v1, model: bench, thinking=on, 2026-09-27T17:46:01.660076Z) [PARTIAL SELECTION: 8 scenarios] ===

  [1/5] CLI-04 ✓ passed pass@1 (57.4s)
  [2/5] CLI-12 ✓ passed pass@1 (166.6s)
  [3/5] CLI-20 ✗ verifier_fail fail (1473.5s)
  [4/5] CLI-28 ✓ passed pass@1 (17.5s)
  [5/5] CLI-36 ✓ passed pass@1 (20.9s)
cli-40 (v1.0.2) | 4 / 5 | 80% | 57.36s | ok; partial — 5 of 40 selected
  [1/3] HA-04 ✓ passed pass@1 (80.1s)
  [2/3] HA-12 ✓ passed pass@1 (41.8s)
  [3/3] HA-20 ✗ verifier_fail fail (68.0s)
hermesagent-20 (v1.0.0) | 2 / 3 | 67% | 68.01s | ok; partial — 3 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 4 / 5 | 80% | 57.36s | 1473.52s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 3 | 67% | 68.01s | 80.12s | ok; partial — 3 of 20 selected

TOTAL | 6 / 8 | 75% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 10 (0.0%) | — | — | message.content=3, multi_turn=2
hermesagent-20 | — | — | — | multi_turn=3

Failure breakdown:
- cli-40 CLI-20: verifier_fail [fail] (CLI-20: Did not satisfy the scenario requirements. (score=25; correctness=0/2; efficiency=2/2; discipline=0/2; commandCount=1; note=new.tar did not match the expected repacked archive.))
- hermesagent-20 HA-20: verifier_fail [fail] (Hermes failed the ambiguous destructive-request scenario.)
```

</details>
