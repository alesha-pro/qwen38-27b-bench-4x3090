## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 5 / 5 | 100% | — | — | 32.69s | 511.33s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | — | — | 40.04s | 61.21s | ok; partial — 2 of 20 selected

TOTAL | 6 / 7 | 86% |  |  |  |  |

Equivalent to: 129/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19415/v1, model: bench, thinking=on, 2026-09-28T10:39:48.555749Z) [PARTIAL SELECTION: 7 scenarios] ===

  [1/5] CLI-06 ✓ passed pass@1 (32.7s)
  [2/5] CLI-14 ✓ passed pass@1 (511.3s)
  [3/5] CLI-22 ✓ passed pass@1 (26.8s)
  [4/5] CLI-30 ✓ passed pass@1 (22.7s)
  [5/5] CLI-38 ✓ passed pass@1 (81.4s)
cli-40 (v1.0.2) | 5 / 5 | 100% | 32.69s | ok; partial — 5 of 40 selected
  [1/2] HA-06 ✗ verifier_fail fail (61.2s)
  [2/2] HA-14 ✓ passed pass@1 (18.9s)
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | 40.04s | ok; partial — 2 of 20 selected

Pack | Pass / Total | Score | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---
cli-40 (v1.0.2) | 5 / 5 | 100% | 32.69s | 511.33s | ok; partial — 5 of 40 selected
hermesagent-20 (v1.0.0) | 1 / 2 | 50% | 40.04s | 61.21s | ok; partial — 2 of 20 selected

TOTAL | 6 / 7 | 86% |  |  |

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
cli-40 | 0 / 24 (0.0%) | — | — | message.content=2, multi_turn=3
hermesagent-20 | — | — | — | multi_turn=2

Failure breakdown:
- hermesagent-20 HA-06: verifier_fail [fail] (Hermes failed the background process management scenario.)
```

</details>
