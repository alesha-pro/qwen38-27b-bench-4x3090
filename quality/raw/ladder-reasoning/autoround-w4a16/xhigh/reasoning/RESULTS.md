## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
humaneval-plus-30 (v0.1.0) | 30 / 30 | 100% | — | — | 3.84s | 36.53s | ok
lcb-v6-30 (v0.1.0) | 29 / 30 | 97% | — | — | 109.82s | 592.20s | ok
gpqa-diamond (v0.1.0) | 0 / 0 | - | — | — | - | - | skipped
gsm-symbolic-30 (v0.1.0) | 29 / 30 | 97% | — | — | 2.31s | 3.61s | ok

TOTAL | 88 / 90 | 98% |  |  |  |  |

Equivalent to: 147/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --reasoning  (endpoint: http://127.0.0.1:19092/v1, model: bench, thinking=on, 2026-08-20T22:46:02.383886Z) ===

  [1/30] HumanEval-0 ✓ passed pass@1 (6.5s)
  [2/30] HumanEval-1 ✓ passed pass@1 (4.3s)
  [3/30] HumanEval-2 ✓ passed pass@1 (40.3s)
  [4/30] HumanEval-3 ✓ passed pass@1 (3.1s)
  [5/30] HumanEval-4 ✓ passed pass@1 (5.7s)
  [6/30] HumanEval-5 ✓ passed pass@1 (3.1s)
  [7/30] HumanEval-6 ✓ passed pass@1 (6.2s)
  [8/30] HumanEval-7 ✓ passed pass@1 (2.8s)
  [9/30] HumanEval-8 ✓ passed pass@1 (2.5s)
  [10/30] HumanEval-9 ✓ passed pass@1 (2.7s)
  [11/30] HumanEval-10 ✓ passed pass@1 (13.2s)
  [12/30] HumanEval-11 ✓ passed pass@1 (25.2s)
  [13/30] HumanEval-12 ✓ passed pass@1 (7.0s)
  [14/30] HumanEval-13 ✓ passed pass@1 (1.8s)
  [15/30] HumanEval-14 ✓ passed pass@1 (3.1s)
  [16/30] HumanEval-15 ✓ passed pass@1 (3.2s)
  [17/30] HumanEval-16 ✓ passed pass@1 (1.5s)
  [18/30] HumanEval-17 ✓ passed pass@1 (36.5s)
  [19/30] HumanEval-18 ✓ passed pass@1 (3.4s)
  [20/30] HumanEval-19 ✓ passed pass@1 (5.8s)
  [21/30] HumanEval-20 ✓ passed pass@1 (21.5s)
  [22/30] HumanEval-21 ✓ passed pass@1 (5.9s)
  [23/30] HumanEval-22 ✓ passed pass@1 (15.1s)
  [24/30] HumanEval-23 ✓ passed pass@1 (1.1s)
  [25/30] HumanEval-24 ✓ passed pass@1 (7.6s)
  [26/30] HumanEval-25 ✓ passed pass@1 (6.8s)
  [27/30] HumanEval-26 ✓ passed pass@1 (3.1s)
  [28/30] HumanEval-27 ✓ passed pass@1 (3.2s)
  [29/30] HumanEval-28 ✓ passed pass@1 (2.0s)
  [30/30] HumanEval-29 ✓ passed pass@1 (2.1s)
humaneval-plus-30 (v0.1.0) | pass@1 30 / 30 (100%) | pass@3 30 / 30 (100%) | 3.84s | ok
  [1/30] LCBv6-3702 ✓ passed pass@1 (54.4s)
  [2/30] LCBv6-3634 ✓ passed pass@1 (16.0s)
  [3/30] LCBv6-3715 ✓ passed pass@1 (436.2s)
  [4/30] LCBv6-3562 ✓ passed pass@1 (1144.6s)
  [5/30] LCBv6-3684 ✓ passed pass@1 (55.3s)
  [6/30] LCBv6-3716 ✓ passed pass@1 (183.1s)
  [7/30] LCBv6-3688 ✓ passed pass@1 (549.7s)
  [8/30] LCBv6-3708 ✓ passed pass@1 (37.2s)
  [9/30] LCBv6-3677 ✓ passed pass@1 (107.3s)
  [10/30] LCBv6-3720 ✓ passed pass@1 (94.8s)
  [11/30] LCBv6-3674 ✓ passed pass@1 (347.6s)
  [12/30] LCBv6-3731 ✓ passed pass@1 (4.2s)
  [13/30] LCBv6-3714 ✓ passed pass@1 (123.5s)
  [14/30] LCBv6-3737 ✓ passed pass@1 (68.8s)
  [15/30] LCBv6-3725 ✓ passed pass@1 (112.3s)
  [16/30] LCBv6-3704 ✓ passed pass@1 (1.9s)
  [17/30] LCBv6-3721 ✓ passed pass@1 (44.2s)
  [18/30] LCBv6-3751 ✓ passed pass@1 (154.3s)
  [19/30] LCBv6-3753 ✓ passed pass@1 (18.5s)
  [20/30] LCBv6-3754 ✓ passed pass@1 (246.5s)
  [21/30] LCBv6-3697 ✓ passed pass@1 (118.9s)
  [22/30] LCBv6-3748 ✗ wrong_answer pass@2 (18.1s)
  [23/30] LCBv6-3760 ✓ passed pass@1 (14.8s)
  [24/30] LCBv6-3696 ✓ passed pass@1 (124.4s)
  [25/30] LCBv6-3762 ✓ passed pass@1 (592.2s)
  [26/30] LCBv6-3709 ✓ passed pass@1 (7.0s)
  [27/30] LCBv6-3779 ✓ passed pass@1 (371.1s)
  [28/30] LCBv6-3771 ✓ passed pass@1 (398.2s)
  [29/30] LCBv6-3733 ✓ passed pass@1 (553.5s)
  [30/30] LCBv6-3768 ✓ passed pass@1 (2.8s)
lcb-v6-30 (v0.1.0) | pass@1 29 / 30 (97%) | pass@3 30 / 30 (100%) | 109.82s | ok
gpqa-diamond (v0.1.0) | 0 / 0 | - | - | skipped
  [1/30] GSM-SYM-0000 ✓ passed pass@1 (2.4s)
  [2/30] GSM-SYM-0000 ✓ passed pass@1 (1.7s)
  [3/30] GSM-SYM-0000 ✓ passed pass@1 (2.4s)
  [4/30] GSM-SYM-0000 ✓ passed pass@1 (2.1s)
  [5/30] GSM-SYM-0000 ✓ passed pass@1 (4.3s)
  [6/30] GSM-SYM-0000 ✓ passed pass@1 (3.0s)
  [7/30] GSM-SYM-0000 ✓ passed pass@1 (2.0s)
  [8/30] GSM-SYM-0000 ✓ passed pass@1 (2.3s)
  [9/30] GSM-SYM-0000 ✓ passed pass@1 (2.1s)
  [10/30] GSM-SYM-0000 ✓ passed pass@1 (3.1s)
  [11/30] GSM-SYM-0000 ✓ passed pass@1 (3.0s)
  [12/30] GSM-SYM-0000 ✓ passed pass@1 (2.1s)
  [13/30] GSM-SYM-0000 ✓ passed pass@1 (3.6s)
  [14/30] GSM-SYM-0000 ✓ passed pass@1 (2.7s)
  [15/30] GSM-SYM-0000 ✓ passed pass@1 (3.3s)
  [16/30] GSM-SYM-0000 ✓ passed pass@1 (3.0s)
  [17/30] GSM-SYM-0000 ✓ passed pass@1 (1.1s)
  [18/30] GSM-SYM-0000 ✓ passed pass@1 (1.9s)
  [19/30] GSM-SYM-0000 ✗ wrong_answer pass@2 (1.9s)
  [20/30] GSM-SYM-0000 ✓ passed pass@1 (2.2s)
  [21/30] GSM-SYM-0000 ✓ passed pass@1 (3.0s)
  [22/30] GSM-SYM-0000 ✓ passed pass@1 (2.3s)
  [23/30] GSM-SYM-0000 ✓ passed pass@1 (3.5s)
  [24/30] GSM-SYM-0000 ✓ passed pass@1 (1.5s)
  [25/30] GSM-SYM-0000 ✓ passed pass@1 (2.5s)
  [26/30] GSM-SYM-0000 ✓ passed pass@1 (1.9s)
  [27/30] GSM-SYM-0000 ✓ passed pass@1 (2.2s)
  [28/30] GSM-SYM-0000 ✓ passed pass@1 (2.3s)
  [29/30] GSM-SYM-0000 ✓ passed pass@1 (3.1s)
  [30/30] GSM-SYM-0000 ✓ passed pass@1 (2.2s)
gsm-symbolic-30 (v0.1.0) | pass@1 29 / 30 (97%) | pass@3 30 / 30 (100%) | 2.31s | ok

Pack | Pass@1 | Pass@3 | Flaky | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---
humaneval-plus-30 (v0.1.0) | 30 / 30 (100%) | 30 / 30 (100%) | 0 | 3.84s | 36.53s | ok
lcb-v6-30 (v0.1.0) | 29 / 30 (97%) | 30 / 30 (100%) | 1 | 109.82s | 592.20s | ok
gpqa-diamond (v0.1.0) | 0 / 0 (-) | - | - | - | - | skipped
gsm-symbolic-30 (v0.1.0) | 29 / 30 (97%) | 30 / 30 (100%) | 1 | 2.31s | 3.61s | ok

TOTAL | 88 / 90 (98%) | 90 / 90 (100%) | 2 |  |  |

Inline retry classification (clean pass@1 rows omitted):

Scenario | Label | Attempts | Pass@k credit
---|---|---:|---
lcb-v6-30/LCBv6-3748 | pass@2 | 2 | yes
gsm-symbolic-30/GSM-SYM-0000 | pass@2 | 2 | yes

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
humaneval-plus-30 | 0 / 30 (0.0%) | code_start=30 | no_fenced_block=30 | message.content=30
lcb-v6-30 | 0 / 31 (0.0%) | code_start=31 | no_fenced_block=31 | message.content=31
gsm-symbolic-30 | 0 / 31 (0.0%) | — | — | message.content=31

Failure breakdown:
- lcb-v6-30 LCBv6-3748: wrong_answer [pass@2] (LCBv6-3748: Traceback (most recent call last):
  File "/tmp/tmpw8zasmgu.py", line 49, in <module>
    _run()
  File "/tmp/tmpw8zasmgu.py", line 48, in _run
    raise AssertionError(f"test {i}: expected {expected!r}, got {got!r}")
AssertionError: test 0: expected [[8, 2, 3], [9, 6, 7], [4, 5, 1]], got [[1, 2, 3], [9, 6, 7], [4, 5, 8]]
)
- gsm-symbolic-30 GSM-SYM-0000: wrong_answer [pass@2] (expected numeric value 5)

Warnings:
- GPQA is gated on Hugging Face; authenticate and run the future pack builder to materialize gpqa-diamond scenarios. No GPQA data is committed here.
```

</details>
