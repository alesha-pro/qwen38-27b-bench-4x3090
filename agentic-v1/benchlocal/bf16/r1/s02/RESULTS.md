## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 3 / 4 | 75% | — | — | 203.44s | 1687.44s | ok; partial — 4 of 40 selected
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | — | — | 93.41s | 163.48s | ok; partial — 2 of 20 selected

TOTAL | 4 / 6 | 67% |  |  |  |  |

Equivalent to: 100/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19420/v1, model: bench, thinking=on, 2026-09-27T17:35:44.362846Z) [PARTIAL SELECTION: 6 scenarios] ===

  [1/4] CLI-03 ✓ passed pass@1 (31.5s)
  [2/4] CLI-13 ✓ passed pass@1 (373.8s)
  [3/4] CLI-23 ✓ passed pass@1 (33.1s)
  [4/4] CLI-33 ✗ server_error fail (1687.4s)
cli-40 (v1.0.2) | pass@1 3 / 4 (75%) | pass@3 3 / 4 (75%) | 203.44s | ok; partial — 4 of 40 selected
  [1/2] HA-03 ✓ passed pass@1 (23.3s)
  [2/2] HA-13 ✗ verifier_fail fail (163.5s)
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | 93.41s | ok; partial — 2 of 20 selected

Pack | Pass@1 | Pass@3 | Flaky | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 3 / 4 (75%) | 3 / 4 (75%) | 0 | 203.44s | 1687.44s | ok; partial — 4 of 40 selected
hermesagent-20 (v1.0.0) | 1 / 2 (50%) | - | - | 93.41s | 163.48s | ok; partial — 2 of 20 selected

TOTAL | 4 / 6 (67%) | 3 / 4 (75%) | 0 |  |  |

Inline retry classification (clean pass@1 rows omitted):

Scenario | Label | Attempts | Pass@k credit
---|---|---:|---
cli-40/CLI-33 | fail | 2 | no
hermesagent-20/HA-13 | fail | 1 | no

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 1 / 9 (11.1%) | — | — | message.content=3, message.reasoning=1, multi_turn=1
hermesagent-20 | — | — | — | multi_turn=2

Failure breakdown:
- cli-40 CLI-33: server_error [fail] (CLI-33: verifier raised OSError: [Errno 7] Argument list too long: 'node')
- hermesagent-20 HA-13: verifier_fail [fail] (Hermes failed the cron creation scenario.)
```

</details>
