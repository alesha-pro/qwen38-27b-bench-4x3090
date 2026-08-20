## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
gsm-symbolic-30 (v0.1.0) | 30 / 30 | 100% | — | — | 5.43s | 9.70s | ok

TOTAL | 30 / 30 | 100% |  |  |  |  |

Equivalent to: 150/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --custom  (endpoint: http://127.0.0.1:19081/v1, model: bench, thinking=on, 2026-08-18T15:36:37.839409Z) ===

  [1/30] GSM-SYM-0000 ✓ passed pass@1 (6.0s)
  [2/30] GSM-SYM-0000 ✓ passed pass@1 (3.8s)
  [3/30] GSM-SYM-0000 ✓ passed pass@1 (7.3s)
  [4/30] GSM-SYM-0000 ✓ passed pass@1 (5.5s)
  [5/30] GSM-SYM-0000 ✓ passed pass@1 (6.1s)
  [6/30] GSM-SYM-0000 ✓ passed pass@1 (13.5s)
  [7/30] GSM-SYM-0000 ✓ passed pass@1 (4.9s)
  [8/30] GSM-SYM-0000 ✓ passed pass@1 (5.1s)
  [9/30] GSM-SYM-0000 ✓ passed pass@1 (6.7s)
  [10/30] GSM-SYM-0000 ✓ passed pass@1 (7.7s)
  [11/30] GSM-SYM-0000 ✓ passed pass@1 (9.7s)
  [12/30] GSM-SYM-0000 ✓ passed pass@1 (4.1s)
  [13/30] GSM-SYM-0000 ✓ passed pass@1 (5.3s)
  [14/30] GSM-SYM-0000 ✓ passed pass@1 (4.9s)
  [15/30] GSM-SYM-0000 ✓ passed pass@1 (6.5s)
  [16/30] GSM-SYM-0000 ✓ passed pass@1 (6.3s)
  [17/30] GSM-SYM-0000 ✓ passed pass@1 (4.5s)
  [18/30] GSM-SYM-0000 ✓ passed pass@1 (5.3s)
  [19/30] GSM-SYM-0000 ✓ passed pass@1 (5.2s)
  [20/30] GSM-SYM-0000 ✓ passed pass@1 (5.1s)
  [21/30] GSM-SYM-0000 ✓ passed pass@1 (5.8s)
  [22/30] GSM-SYM-0000 ✓ passed pass@1 (5.2s)
  [23/30] GSM-SYM-0000 ✓ passed pass@1 (7.9s)
  [24/30] GSM-SYM-0000 ✓ passed pass@1 (5.7s)
  [25/30] GSM-SYM-0000 ✓ passed pass@1 (6.0s)
  [26/30] GSM-SYM-0000 ✓ passed pass@1 (4.8s)
  [27/30] GSM-SYM-0000 ✓ passed pass@1 (3.9s)
  [28/30] GSM-SYM-0000 ✓ passed pass@1 (8.4s)
  [29/30] GSM-SYM-0000 ✓ passed pass@1 (5.2s)
  [30/30] GSM-SYM-0000 ✓ passed pass@1 (5.1s)
gsm-symbolic-30 (v0.1.0) | pass@1 30 / 30 (100%) | pass@3 30 / 30 (100%) | 5.43s | ok

Pack | Pass@1 | Pass@3 | Flaky | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---
gsm-symbolic-30 (v0.1.0) | 30 / 30 (100%) | 30 / 30 (100%) | 0 | 5.43s | 9.70s | ok

TOTAL | 30 / 30 (100%) | 30 / 30 (100%) | 0 |  |  |

Inline retry classification (clean pass@1 rows omitted):

Scenario | Label | Attempts | Pass@k credit
---|---|---:|---
all scenarios | pass@1 | 1 | yes

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
gsm-symbolic-30 | 0 / 30 (0.0%) | — | — | message.content=30
```

</details>
