## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 5 / 5 | 100% | — | — | 60.58s | 890.84s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | — | — | 188.33s | 300.14s | ok; partial — 2 of 20 selected

TOTAL | 6 / 7 | 86% |  |  |  |  |

Equivalent to: 129/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19410/v1, model: bench, thinking=on, 2026-09-27T18:18:24.008443Z) [PARTIAL SELECTION: 7 scenarios] ===

  [1/5] CLI-05 ✓ passed pass@1 (102.2s)
  [2/5] CLI-13 ✓ passed pass@1 (890.8s)
  [3/5] CLI-21 ✓ passed pass@1 (60.6s)
  [4/5] CLI-29 ✓ passed pass@1 (27.4s)
  [5/5] CLI-37 ✓ passed pass@1 (33.0s)
cli-40 (v1.0.2) | 5 / 5 | 100% | 60.58s | ok; partial — 5 of 40 selected
  [1/2] HA-05 ✓ passed pass@1 (76.5s)
  [2/2] HA-13 ✗ agent_runner_timeout fail (300.1s)
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | 188.33s | ok; partial — 2 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 5 / 5 | 100% | 60.58s | 890.84s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | 188.33s | 300.14s | ok; partial — 2 of 20 selected

TOTAL | 6 / 7 | 86% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 18 (0.0%) | — | — | message.content=2, multi_turn=3
hermesagent-20 | — | — | — | multi_turn=2

Failure breakdown:
- hermesagent-20 HA-13: agent_runner_timeout [fail] (HA-13: upstream /run-scenario exceeded 300s)
```

</details>
