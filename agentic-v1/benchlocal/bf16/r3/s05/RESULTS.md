## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 4 / 4 | 100% | — | — | 26.13s | 58.97s | ok; partial — 4 of 40 selected
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | — | — | 84.20s | 105.51s | ok; partial — 2 of 20 selected

TOTAL | 5 / 6 | 83% |  |  |  |  |

Equivalent to: 125/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19420/v1, model: bench, thinking=on, 2026-09-27T18:07:48.780767Z) [PARTIAL SELECTION: 6 scenarios] ===

  [1/4] CLI-06 ✓ passed pass@1 (59.0s)
  [2/4] CLI-16 ✓ passed pass@1 (39.9s)
  [3/4] CLI-26 ✓ passed pass@1 (12.4s)
  [4/4] CLI-36 ✓ passed pass@1 (12.3s)
cli-40 (v1.0.2) | 4 / 4 | 100% | 26.13s | ok; partial — 4 of 40 selected
  [1/2] HA-06 ✓ passed pass@1 (62.9s)
  [2/2] HA-16 ✗ verifier_fail fail (105.5s)
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | 84.20s | ok; partial — 2 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 4 / 4 | 100% | 26.13s | 58.97s | ok; partial — 4 of 40 selected
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | 84.20s | 105.51s | ok; partial — 2 of 20 selected

TOTAL | 5 / 6 | 83% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 8 (0.0%) | — | — | message.content=2, multi_turn=2
hermesagent-20 | — | — | — | multi_turn=2

Failure breakdown:
- hermesagent-20 HA-16: verifier_fail [fail] (Hermes failed to send the message to the correct named target.)
```

</details>
