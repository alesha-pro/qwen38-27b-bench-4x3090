## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 4 / 5 | 80% | — | — | 170.23s | 6838.54s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 3 | 67% | — | — | 37.95s | 43.17s | ok; partial — 3 of 20 selected

TOTAL | 6 / 8 | 75% |  |  |  |  |

Equivalent to: 113/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19410/v1, model: bench, thinking=on, 2026-09-27T18:43:30.136823Z) [PARTIAL SELECTION: 8 scenarios] ===

  [1/5] CLI-04 ✓ passed pass@1 (170.2s)
  [2/5] CLI-12 ✓ passed pass@1 (219.2s)
  [3/5] CLI-20 ✗ server_error fail (6838.5s)
  [4/5] CLI-28 ✓ passed pass@1 (14.5s)
  [5/5] CLI-36 ✓ passed pass@1 (10.6s)
cli-40 (v1.0.2) | pass@1 4 / 5 (80%) | pass@3 4 / 5 (80%) | 170.23s | ok; partial — 5 of 40 selected
  [1/3] HA-04 ✓ passed pass@1 (43.2s)
  [2/3] HA-12 ✓ passed pass@1 (36.1s)
  [3/3] HA-20 ✗ verifier_fail fail (37.9s)
hermesagent-20 (v1.0.0) | 2 / 3 | 67% | 37.95s | ok; partial — 3 of 20 selected

Pack | Pass@1 | Pass@3 | Flaky | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 4 / 5 (80%) | 4 / 5 (80%) | 0 | 170.23s | 6838.54s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 2 / 3 (67%) | - | - | 37.95s | 43.17s | ok; partial — 3 of 20 selected

TOTAL | 6 / 8 (75%) | 4 / 5 (80%) | 0 |  |  |

Inline retry classification (clean pass@1 rows omitted):

Scenario | Label | Attempts | Pass@k credit
---|---|---:|---
cli-40/CLI-20 | fail | 3 | no
hermesagent-20/HA-20 | fail | 1 | no

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 2 / 13 (15.4%) | — | — | message.content=2, message.reasoning=3, multi_turn=2
hermesagent-20 | — | — | — | multi_turn=3

Failure breakdown:
- cli-40 CLI-20: server_error [fail] (CLI-20: verifier raised OSError: [Errno 7] Argument list too long: 'node')
- hermesagent-20 HA-20: verifier_fail [fail] (Hermes failed the ambiguous destructive-request scenario.)
```

</details>
