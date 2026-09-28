## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 2 / 4 | 50% | — | — | 358.31s | 831.45s | ok; partial — 4 of 40 selected
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | — | — | 44.54s | 48.81s | ok; partial — 2 of 20 selected

TOTAL | 3 / 6 | 50% |  |  |  |  |

Equivalent to: 75/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19420/v1, model: bench, thinking=on, 2026-09-27T17:35:44.382657Z) [PARTIAL SELECTION: 6 scenarios] ===

  [1/4] CLI-10 ✗ verifier_fail fail (831.4s)
  [2/4] CLI-20 ✗ verifier_fail fail (554.2s)
  [3/4] CLI-30 ✓ passed pass@1 (91.5s)
  [4/4] CLI-40 ✓ passed pass@1 (162.4s)
cli-40 (v1.0.2) | 2 / 4 | 50% | 358.31s | ok; partial — 4 of 40 selected
  [1/2] HA-10 ✓ passed pass@1 (48.8s)
  [2/2] HA-20 ✗ verifier_fail fail (40.3s)
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | 44.54s | ok; partial — 2 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 2 / 4 | 50% | 358.31s | 831.45s | ok; partial — 4 of 40 selected
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | 44.54s | 48.81s | ok; partial — 2 of 20 selected

TOTAL | 3 / 6 | 50% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 19 (0.0%) | — | — | message.content=2, multi_turn=2
hermesagent-20 | — | — | — | multi_turn=2

Failure breakdown:
- cli-40 CLI-10: verifier_fail [fail] (CLI-10: Did not satisfy the scenario requirements. (score=50; correctness=0/2; efficiency=2/2; discipline=2/2; commandCount=1; note=The flat directory did not contain the expected collision-safe filenames, bytes, or emptied source file tree.))
- cli-40 CLI-20: verifier_fail [fail] (CLI-20: Did not satisfy the scenario requirements. (score=50; correctness=0/2; efficiency=2/2; discipline=2/2; commandCount=1; note=new.tar did not match the expected repacked archive.))
- hermesagent-20 HA-20: verifier_fail [fail] (Hermes failed the ambiguous destructive-request scenario.)
```

</details>
