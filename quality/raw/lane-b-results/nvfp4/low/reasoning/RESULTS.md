## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
humaneval-plus-30 (v0.1.0) | 30 / 30 | 100% | — | — | 6.51s | 12.86s | ok
lcb-v6-30 (v0.1.0) | 30 / 30 | 100% | — | — | 59.51s | 487.23s | ok
gpqa-diamond (v0.1.0) | 0 / 0 | - | — | — | - | - | stubbed
gsm-symbolic-30 (v0.1.0) | 1 / 1 | 100% | — | — | 4.70s | 4.70s | ok

TOTAL | 61 / 61 | 100% |  |  |  |  |

Equivalent to: 150/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --reasoning  (endpoint: http://127.0.0.1:19082/v1, model: bench, thinking=on, 2026-08-18T06:36:40.991724Z) ===

  [1/30] HumanEval-0 ✓ passed pass@1 (10.6s)
  [2/30] HumanEval-1 ✓ passed pass@1 (10.7s)
  [3/30] HumanEval-2 ✓ passed pass@1 (5.4s)
  [4/30] HumanEval-3 ✓ passed pass@1 (4.2s)
  [5/30] HumanEval-4 ✓ passed pass@1 (6.4s)
  [6/30] HumanEval-5 ✓ passed pass@1 (6.6s)
  [7/30] HumanEval-6 ✓ passed pass@1 (10.8s)
  [8/30] HumanEval-7 ✓ passed pass@1 (2.8s)
  [9/30] HumanEval-8 ✓ passed pass@1 (4.7s)
  [10/30] HumanEval-9 ✓ passed pass@1 (7.1s)
  [11/30] HumanEval-10 ✓ passed pass@1 (14.7s)
  [12/30] HumanEval-11 ✓ passed pass@1 (8.7s)
  [13/30] HumanEval-12 ✓ passed pass@1 (5.7s)
  [14/30] HumanEval-13 ✓ passed pass@1 (3.4s)
  [15/30] HumanEval-14 ✓ passed pass@1 (3.7s)
  [16/30] HumanEval-15 ✓ passed pass@1 (3.3s)
  [17/30] HumanEval-16 ✓ passed pass@1 (3.5s)
  [18/30] HumanEval-17 ✓ passed pass@1 (9.5s)
  [19/30] HumanEval-18 ✓ passed pass@1 (11.0s)
  [20/30] HumanEval-19 ✓ passed pass@1 (8.8s)
  [21/30] HumanEval-20 ✓ passed pass@1 (12.9s)
  [22/30] HumanEval-21 ✓ passed pass@1 (6.2s)
  [23/30] HumanEval-22 ✓ passed pass@1 (8.3s)
  [24/30] HumanEval-23 ✓ passed pass@1 (1.5s)
  [25/30] HumanEval-24 ✓ passed pass@1 (11.5s)
  [26/30] HumanEval-25 ✓ passed pass@1 (11.7s)
  [27/30] HumanEval-26 ✓ passed pass@1 (7.0s)
  [28/30] HumanEval-27 ✓ passed pass@1 (2.3s)
  [29/30] HumanEval-28 ✓ passed pass@1 (2.4s)
  [30/30] HumanEval-29 ✓ passed pass@1 (3.6s)
humaneval-plus-30 (v0.1.0) | pass@1 30 / 30 (100%) | pass@3 30 / 30 (100%) | 6.51s | ok
  [1/30] LCBv6-3702 ✓ passed pass@1 (19.8s)
  [2/30] LCBv6-3634 ✓ passed pass@1 (47.2s)
  [3/30] LCBv6-3715 ✓ passed pass@1 (61.5s)
  [4/30] LCBv6-3562 ✓ passed pass@1 (261.1s)
  [5/30] LCBv6-3684 ✓ passed pass@1 (31.7s)
  [6/30] LCBv6-3716 ✓ passed pass@1 (212.3s)
  [7/30] LCBv6-3688 ✓ passed pass@1 (239.4s)
  [8/30] LCBv6-3708 ✓ passed pass@1 (9.9s)
  [9/30] LCBv6-3677 ✓ passed pass@1 (58.4s)
  [10/30] LCBv6-3720 ✓ passed pass@1 (88.5s)
  [11/30] LCBv6-3674 ✓ passed pass@1 (487.2s)
  [12/30] LCBv6-3731 ✓ passed pass@1 (8.8s)
  [13/30] LCBv6-3714 ✓ passed pass@1 (46.1s)
  [14/30] LCBv6-3737 ✓ passed pass@1 (57.0s)
  [15/30] LCBv6-3725 ✓ passed pass@1 (144.5s)
  [16/30] LCBv6-3704 ✓ passed pass@1 (7.6s)
  [17/30] LCBv6-3721 ✓ passed pass@1 (39.6s)
  [18/30] LCBv6-3751 ✓ passed pass@1 (62.5s)
  [19/30] LCBv6-3753 ✓ passed pass@1 (7.0s)
  [20/30] LCBv6-3754 ✓ passed pass@1 (60.6s)
  [21/30] LCBv6-3697 ✓ passed pass@1 (63.9s)
  [22/30] LCBv6-3748 ✓ passed pass@1 (27.5s)
  [23/30] LCBv6-3760 ✓ passed pass@1 (25.6s)
  [24/30] LCBv6-3696 ✓ passed pass@1 (375.4s)
  [25/30] LCBv6-3762 ✓ passed pass@1 (631.4s)
  [26/30] LCBv6-3709 ✓ passed pass@1 (16.8s)
  [27/30] LCBv6-3779 ✓ passed pass@1 (66.9s)
  [28/30] LCBv6-3771 ✓ passed pass@1 (266.4s)
  [29/30] LCBv6-3733 ✓ passed pass@1 (403.0s)
  [30/30] LCBv6-3768 ✓ passed pass@1 (8.2s)
lcb-v6-30 (v0.1.0) | pass@1 30 / 30 (100%) | pass@3 30 / 30 (100%) | 59.51s | ok
gpqa-diamond (v0.1.0) | 0 / 0 | - | - | stubbed
  [1/1] GSM-SYM-0000 ✓ passed pass@1 (4.7s)
gsm-symbolic-30 (v0.1.0) | pass@1 1 / 1 (100%) | pass@3 1 / 1 (100%) | 4.70s | ok

Pack | Pass@1 | Pass@3 | Flaky | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---
humaneval-plus-30 (v0.1.0) | 30 / 30 (100%) | 30 / 30 (100%) | 0 | 6.51s | 12.86s | ok
lcb-v6-30 (v0.1.0) | 30 / 30 (100%) | 30 / 30 (100%) | 0 | 59.51s | 487.23s | ok
gpqa-diamond (v0.1.0) | 0 / 0 (-) | - | - | - | - | stubbed
gsm-symbolic-30 (v0.1.0) | 1 / 1 (100%) | 1 / 1 (100%) | 0 | 4.70s | 4.70s | ok

TOTAL | 61 / 61 (100%) | 61 / 61 (100%) | 0 |  |  |

Inline retry classification (clean pass@1 rows omitted):

Scenario | Label | Attempts | Pass@k credit
---|---|---:|---
all scenarios | pass@1 | 1 | yes

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
humaneval-plus-30 | 0 / 30 (0.0%) | code_start=5, last_fenced=25 | no_fenced_block=5, none=25 | message.content=30
lcb-v6-30 | 0 / 30 (0.0%) | code_start=12, last_fenced=18 | no_fenced_block=12, none=18 | message.content=29, message.reasoning=1
gsm-symbolic-30 | 0 / 1 (0.0%) | — | — | message.content=1
```

</details>
