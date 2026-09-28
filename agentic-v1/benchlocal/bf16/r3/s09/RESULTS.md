## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 2 / 4 | 50% | — | — | 186.02s | 435.58s | ok; partial — 4 of 40 selected
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | — | — | 40.75s | 45.59s | ok; partial — 2 of 20 selected

TOTAL | 3 / 6 | 50% |  |  |  |  |

Equivalent to: 75/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19420/v1, model: bench, thinking=on, 2026-09-27T18:18:43.081711Z) [PARTIAL SELECTION: 6 scenarios] ===

  [1/4] CLI-10 ✗ verifier_fail fail (328.7s)
  [2/4] CLI-20 ✗ verifier_fail fail (435.6s)
  [3/4] CLI-30 ✓ passed pass@1 (18.7s)
  [4/4] CLI-40 ✓ passed pass@1 (43.3s)
cli-40 (v1.0.2) | 2 / 4 | 50% | 186.02s | ok; partial — 4 of 40 selected
  [1/2] HA-10 ✓ passed pass@1 (45.6s)
  [2/2] HA-20 ✗ verifier_fail fail (35.9s)
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | 40.75s | ok; partial — 2 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 2 / 4 | 50% | 186.02s | 435.58s | ok; partial — 4 of 40 selected
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | 40.75s | 45.59s | ok; partial — 2 of 20 selected

TOTAL | 3 / 6 | 50% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 11 (0.0%) | — | — | message.content=2, multi_turn=2
hermesagent-20 | — | — | — | multi_turn=2

Failure breakdown:
- cli-40 CLI-10: verifier_fail [fail] (CLI-10: Did not satisfy the scenario requirements. (score=25; correctness=0/2; efficiency=0/2; discipline=2/2; commandCount=13; note=The flat directory did not contain the expected collision-safe filenames, bytes, or emptied source file tree.))
- cli-40 CLI-20: verifier_fail [fail] (CLI-20: Did not satisfy the scenario requirements. (score=50; correctness=0/2; efficiency=2/2; discipline=2/2; commandCount=1; note=new.tar did not match the expected repacked archive.))
- hermesagent-20 HA-20: verifier_fail [fail] (Hermes failed the ambiguous destructive-request scenario.)
```

</details>
