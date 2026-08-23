## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
humaneval-plus-30 (v0.1.0) | 29 / 30 | 97% | — | — | 12.04s | 87.12s | ok
lcb-v6-30 (v0.1.0) | 30 / 30 | 100% | — | — | 245.05s | 1661.68s | ok
gpqa-diamond (v0.1.0) | 0 / 0 | - | — | — | - | - | skipped
gsm-symbolic-30 (v0.1.0) | 30 / 30 | 100% | — | — | 9.51s | 17.58s | ok

TOTAL | 89 / 90 | 99% |  |  |  |  |

Equivalent to: 148/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --reasoning  (endpoint: http://127.0.0.1:19092/v1, model: bench, thinking=on, 2026-08-21T17:13:57.766349Z) ===

  [1/30] HumanEval-0 ✓ passed pass@1 (30.9s)
  [2/30] HumanEval-1 ✓ passed pass@1 (33.3s)
  [3/30] HumanEval-2 ✓ passed pass@1 (17.2s)
  [4/30] HumanEval-3 ✓ passed pass@1 (10.1s)
  [5/30] HumanEval-4 ✓ passed pass@1 (26.2s)
  [6/30] HumanEval-5 ✓ passed pass@1 (11.9s)
  [7/30] HumanEval-6 ✓ passed pass@1 (12.2s)
  [8/30] HumanEval-7 ✓ passed pass@1 (9.4s)
  [9/30] HumanEval-8 ✓ passed pass@1 (10.9s)
  [10/30] HumanEval-9 ✓ passed pass@1 (11.3s)
  [11/30] HumanEval-10 ✓ passed pass@1 (208.2s)
  [12/30] HumanEval-11 ✓ passed pass@1 (17.3s)
  [13/30] HumanEval-12 ✓ passed pass@1 (9.9s)
  [14/30] HumanEval-13 ✓ passed pass@1 (9.9s)
  [15/30] HumanEval-14 ✓ passed pass@1 (8.6s)
  [16/30] HumanEval-15 ✓ passed pass@1 (10.7s)
  [17/30] HumanEval-16 ✓ passed pass@1 (10.4s)
  [18/30] HumanEval-17 ✓ passed pass@1 (13.1s)
  [19/30] HumanEval-18 ✓ passed pass@1 (44.6s)
  [20/30] HumanEval-19 ✓ passed pass@1 (17.2s)
  [21/30] HumanEval-20 ✓ passed pass@1 (26.1s)
  [22/30] HumanEval-21 ✓ passed pass@1 (15.1s)
  [23/30] HumanEval-22 ✗ wrong_answer pass@2 (87.1s)
  [24/30] HumanEval-23 ✓ passed pass@1 (3.6s)
  [25/30] HumanEval-24 ✓ passed pass@1 (70.5s)
  [26/30] HumanEval-25 ✓ passed pass@1 (24.5s)
  [27/30] HumanEval-26 ✓ passed pass@1 (10.1s)
  [28/30] HumanEval-27 ✓ passed pass@1 (4.0s)
  [29/30] HumanEval-28 ✓ passed pass@1 (8.0s)
  [30/30] HumanEval-29 ✓ passed pass@1 (10.2s)
humaneval-plus-30 (v0.1.0) | pass@1 29 / 30 (97%) | pass@3 30 / 30 (100%) | 12.04s | ok
  [1/30] LCBv6-3702 ✓ passed pass@1 (198.1s)
  [2/30] LCBv6-3634 ✓ passed pass@1 (70.0s)
  [3/30] LCBv6-3715 ✓ passed pass@1 (708.5s)
  [4/30] LCBv6-3562 ✓ passed pass@1 (814.9s)
  [5/30] LCBv6-3684 ✓ passed pass@1 (49.7s)
  [6/30] LCBv6-3716 ✓ passed pass@1 (464.6s)
  [7/30] LCBv6-3688 ✓ passed pass@1 (2400.5s)
  [8/30] LCBv6-3708 ✓ passed pass@1 (32.0s)
  [9/30] LCBv6-3677 ✓ passed pass@1 (206.7s)
  [10/30] LCBv6-3720 ✓ passed pass@1 (213.8s)
  [11/30] LCBv6-3674 ✓ passed pass@1 (887.8s)
  [12/30] LCBv6-3731 ✓ passed pass@1 (17.7s)
  [13/30] LCBv6-3714 ✓ passed pass@1 (282.2s)
  [14/30] LCBv6-3737 ✓ passed pass@1 (121.7s)
  [15/30] LCBv6-3725 ✓ passed pass@1 (392.9s)
  [16/30] LCBv6-3704 ✓ passed pass@1 (13.0s)
  [17/30] LCBv6-3721 ✓ passed pass@1 (276.3s)
  [18/30] LCBv6-3751 ✓ passed pass@1 (127.3s)
  [19/30] LCBv6-3753 ✓ passed pass@1 (13.1s)
  [20/30] LCBv6-3754 ✓ passed pass@1 (293.6s)
  [21/30] LCBv6-3697 ✓ passed pass@1 (858.1s)
  [22/30] LCBv6-3748 ✓ passed pass@1 (37.3s)
  [23/30] LCBv6-3760 ✓ passed pass@1 (102.4s)
  [24/30] LCBv6-3696 ✓ passed pass@1 (615.7s)
  [25/30] LCBv6-3762 ✓ passed pass@1 (1661.7s)
  [26/30] LCBv6-3709 ✓ passed pass@1 (27.3s)
  [27/30] LCBv6-3779 ✓ passed pass@1 (1092.0s)
  [28/30] LCBv6-3771 ✓ passed pass@1 (734.8s)
  [29/30] LCBv6-3733 ✓ passed pass@1 (1222.0s)
  [30/30] LCBv6-3768 ✓ passed pass@1 (12.4s)
lcb-v6-30 (v0.1.0) | pass@1 30 / 30 (100%) | pass@3 30 / 30 (100%) | 245.05s | ok
gpqa-diamond (v0.1.0) | 0 / 0 | - | - | skipped
  [1/30] GSM-SYM-0000 ✓ passed pass@1 (12.6s)
  [2/30] GSM-SYM-0000 ✓ passed pass@1 (10.0s)
  [3/30] GSM-SYM-0000 ✓ passed pass@1 (10.7s)
  [4/30] GSM-SYM-0000 ✓ passed pass@1 (7.6s)
  [5/30] GSM-SYM-0000 ✓ passed pass@1 (10.9s)
  [6/30] GSM-SYM-0000 ✓ passed pass@1 (9.0s)
  [7/30] GSM-SYM-0000 ✓ passed pass@1 (21.5s)
  [8/30] GSM-SYM-0000 ✓ passed pass@1 (9.7s)
  [9/30] GSM-SYM-0000 ✓ passed pass@1 (11.5s)
  [10/30] GSM-SYM-0000 ✓ passed pass@1 (9.9s)
  [11/30] GSM-SYM-0000 ✓ passed pass@1 (9.3s)
  [12/30] GSM-SYM-0000 ✓ passed pass@1 (8.5s)
  [13/30] GSM-SYM-0000 ✓ passed pass@1 (17.6s)
  [14/30] GSM-SYM-0000 ✓ passed pass@1 (11.2s)
  [15/30] GSM-SYM-0000 ✓ passed pass@1 (9.3s)
  [16/30] GSM-SYM-0000 ✓ passed pass@1 (9.6s)
  [17/30] GSM-SYM-0000 ✓ passed pass@1 (9.4s)
  [18/30] GSM-SYM-0000 ✓ passed pass@1 (8.3s)
  [19/30] GSM-SYM-0000 ✓ passed pass@1 (11.4s)
  [20/30] GSM-SYM-0000 ✓ passed pass@1 (8.0s)
  [21/30] GSM-SYM-0000 ✓ passed pass@1 (9.1s)
  [22/30] GSM-SYM-0000 ✓ passed pass@1 (7.0s)
  [23/30] GSM-SYM-0000 ✓ passed pass@1 (12.4s)
  [24/30] GSM-SYM-0000 ✓ passed pass@1 (5.8s)
  [25/30] GSM-SYM-0000 ✓ passed pass@1 (7.8s)
  [26/30] GSM-SYM-0000 ✓ passed pass@1 (9.2s)
  [27/30] GSM-SYM-0000 ✓ passed pass@1 (8.7s)
  [28/30] GSM-SYM-0000 ✓ passed pass@1 (9.8s)
  [29/30] GSM-SYM-0000 ✓ passed pass@1 (9.7s)
  [30/30] GSM-SYM-0000 ✓ passed pass@1 (8.0s)
gsm-symbolic-30 (v0.1.0) | pass@1 30 / 30 (100%) | pass@3 30 / 30 (100%) | 9.51s | ok

Pack | Pass@1 | Pass@3 | Flaky | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---
humaneval-plus-30 (v0.1.0) | 29 / 30 (97%) | 30 / 30 (100%) | 1 | 12.04s | 87.12s | ok
lcb-v6-30 (v0.1.0) | 30 / 30 (100%) | 30 / 30 (100%) | 0 | 245.05s | 1661.68s | ok
gpqa-diamond (v0.1.0) | 0 / 0 (-) | - | - | - | - | skipped
gsm-symbolic-30 (v0.1.0) | 30 / 30 (100%) | 30 / 30 (100%) | 0 | 9.51s | 17.58s | ok

TOTAL | 89 / 90 (99%) | 90 / 90 (100%) | 1 |  |  |

Inline retry classification (clean pass@1 rows omitted):

Scenario | Label | Attempts | Pass@k credit
---|---|---:|---
humaneval-plus-30/HumanEval-22 | pass@2 | 2 | yes

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
humaneval-plus-30 | 0 / 31 (0.0%) | code_start=31 | no_fenced_block=31 | message.content=31
lcb-v6-30 | 0 / 30 (0.0%) | code_start=30 | no_fenced_block=30 | message.content=30
gsm-symbolic-30 | 0 / 30 (0.0%) | — | — | message.content=30

Failure breakdown:
- humaneval-plus-30 HumanEval-22: wrong_answer [pass@2] (HumanEval-22: Traceback (most recent call last):
  File "/tmp/tmphfyb5p3t.py", line 46, in <module>
    check(filter_integers)
  File "/tmp/tmphfyb5p3t.py", line 43, in check
    assertion(candidate(*inp), exp, 0)
  File "/tmp/tmphfyb5p3t.py", line 36, in assertion
    assert exact_match
           ^^^^^^^^^^^
AssertionError
)

Warnings:
- GPQA is gated on Hugging Face; authenticate and run the future pack builder to materialize gpqa-diamond scenarios. No GPQA data is committed here.
```

</details>
