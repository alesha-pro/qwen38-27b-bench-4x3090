## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
humaneval-plus-30 (v0.1.0) | 28 / 30 | 93% | — | — | 9.78s | 21.32s | ok
lcb-v6-30 (v0.1.0) | 28 / 30 | 93% | — | — | 123.04s | 816.30s | ok
gpqa-diamond (v0.1.0) | 0 / 0 | - | — | — | - | - | skipped
gsm-symbolic-30 (v0.1.0) | 30 / 30 | 100% | — | — | 9.29s | 10.61s | ok

TOTAL | 86 / 90 | 96% |  |  |  |  |

Equivalent to: 143/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --reasoning  (endpoint: http://127.0.0.1:19081/v1, model: bench, thinking=on, 2026-08-18T19:31:51.720190Z) ===

  [1/30] HumanEval-0 ✓ passed pass@1 (11.6s)
  [2/30] HumanEval-1 ✓ passed pass@1 (16.9s)
  [3/30] HumanEval-2 ✓ passed pass@1 (7.0s)
  [4/30] HumanEval-3 ✓ passed pass@1 (8.2s)
  [5/30] HumanEval-4 ✗ verifier_fail pass@2 (7.6s)
  [6/30] HumanEval-5 ✓ passed pass@1 (10.2s)
  [7/30] HumanEval-6 ✓ passed pass@1 (13.7s)
  [8/30] HumanEval-7 ✓ passed pass@1 (5.1s)
  [9/30] HumanEval-8 ✓ passed pass@1 (11.3s)
  [10/30] HumanEval-9 ✓ passed pass@1 (10.4s)
  [11/30] HumanEval-10 ✓ passed pass@1 (27.3s)
  [12/30] HumanEval-11 ✓ passed pass@1 (12.1s)
  [13/30] HumanEval-12 ✓ passed pass@1 (9.1s)
  [14/30] HumanEval-13 ✓ passed pass@1 (5.7s)
  [15/30] HumanEval-14 ✓ passed pass@1 (6.5s)
  [16/30] HumanEval-15 ✓ passed pass@1 (6.3s)
  [17/30] HumanEval-16 ✓ passed pass@1 (6.3s)
  [18/30] HumanEval-17 ✓ passed pass@1 (13.9s)
  [19/30] HumanEval-18 ✓ passed pass@1 (18.3s)
  [20/30] HumanEval-19 ✓ passed pass@1 (9.3s)
  [21/30] HumanEval-20 ✓ passed pass@1 (15.3s)
  [22/30] HumanEval-21 ✓ passed pass@1 (11.2s)
  [23/30] HumanEval-22 ✗ wrong_answer pass@2 (13.4s)
  [24/30] HumanEval-23 ✓ passed pass@1 (2.8s)
  [25/30] HumanEval-24 ✓ passed pass@1 (18.8s)
  [26/30] HumanEval-25 ✓ passed pass@1 (21.3s)
  [27/30] HumanEval-26 ✓ passed pass@1 (6.8s)
  [28/30] HumanEval-27 ✓ passed pass@1 (5.1s)
  [29/30] HumanEval-28 ✓ passed pass@1 (3.7s)
  [30/30] HumanEval-29 ✓ passed pass@1 (5.2s)
humaneval-plus-30 (v0.1.0) | pass@1 28 / 30 (93%) | pass@3 30 / 30 (100%) | 9.78s | ok
  [1/30] LCBv6-3702 ✓ passed pass@1 (30.3s)
  [2/30] LCBv6-3634 ✓ passed pass@1 (35.7s)
  [3/30] LCBv6-3715 ✓ passed pass@1 (257.3s)
  [4/30] LCBv6-3562 ✗ wrong_answer pass@2 (569.2s)
  [5/30] LCBv6-3684 ✓ passed pass@1 (38.2s)
  [6/30] LCBv6-3716 ✓ passed pass@1 (200.8s)
  [7/30] LCBv6-3688 ✓ passed pass@1 (444.0s)
  [8/30] LCBv6-3708 ✓ passed pass@1 (25.2s)
  [9/30] LCBv6-3677 ✓ passed pass@1 (130.6s)
  [10/30] LCBv6-3720 ✓ passed pass@1 (110.3s)
  [11/30] LCBv6-3674 ✓ passed pass@1 (460.8s)
  [12/30] LCBv6-3731 ✓ passed pass@1 (19.3s)
  [13/30] LCBv6-3714 ✓ passed pass@1 (115.5s)
  [14/30] LCBv6-3737 ✓ passed pass@1 (816.3s)
  [15/30] LCBv6-3725 ✓ passed pass@1 (280.7s)
  [16/30] LCBv6-3704 ✓ passed pass@1 (19.2s)
  [17/30] LCBv6-3721 ✓ passed pass@1 (86.4s)
  [18/30] LCBv6-3751 ✓ passed pass@1 (61.8s)
  [19/30] LCBv6-3753 ✓ passed pass@1 (13.0s)
  [20/30] LCBv6-3754 ✓ passed pass@1 (228.8s)
  [21/30] LCBv6-3697 ✓ passed pass@1 (177.7s)
  [22/30] LCBv6-3748 ✓ passed pass@1 (37.0s)
  [23/30] LCBv6-3760 ✓ passed pass@1 (43.8s)
  [24/30] LCBv6-3696 ✓ passed pass@1 (565.9s)
  [25/30] LCBv6-3762 ✓ passed pass@1 (941.0s)
  [26/30] LCBv6-3709 ✓ passed pass@1 (29.7s)
  [27/30] LCBv6-3779 ✓ passed pass@1 (262.1s)
  [28/30] LCBv6-3771 ✓ passed pass@1 (612.3s)
  [29/30] LCBv6-3733 ✗ wrong_answer pass@3 (456.6s)
  [30/30] LCBv6-3768 ✓ passed pass@1 (7.7s)
lcb-v6-30 (v0.1.0) | pass@1 28 / 30 (93%) | pass@3 30 / 30 (100%) | 123.04s | ok
gpqa-diamond (v0.1.0) | 0 / 0 | - | - | skipped
  [1/30] GSM-SYM-0000 ✓ passed pass@1 (10.2s)
  [2/30] GSM-SYM-0000 ✓ passed pass@1 (7.6s)
  [3/30] GSM-SYM-0000 ✓ passed pass@1 (10.6s)
  [4/30] GSM-SYM-0000 ✓ passed pass@1 (8.3s)
  [5/30] GSM-SYM-0000 ✓ passed pass@1 (10.8s)
  [6/30] GSM-SYM-0000 ✓ passed pass@1 (10.4s)
  [7/30] GSM-SYM-0000 ✓ passed pass@1 (10.1s)
  [8/30] GSM-SYM-0000 ✓ passed pass@1 (9.6s)
  [9/30] GSM-SYM-0000 ✓ passed pass@1 (9.5s)
  [10/30] GSM-SYM-0000 ✓ passed pass@1 (8.8s)
  [11/30] GSM-SYM-0000 ✓ passed pass@1 (8.9s)
  [12/30] GSM-SYM-0000 ✓ passed pass@1 (8.0s)
  [13/30] GSM-SYM-0000 ✓ passed pass@1 (9.8s)
  [14/30] GSM-SYM-0000 ✓ passed pass@1 (9.2s)
  [15/30] GSM-SYM-0000 ✓ passed pass@1 (8.4s)
  [16/30] GSM-SYM-0000 ✓ passed pass@1 (9.0s)
  [17/30] GSM-SYM-0000 ✓ passed pass@1 (8.6s)
  [18/30] GSM-SYM-0000 ✓ passed pass@1 (9.1s)
  [19/30] GSM-SYM-0000 ✓ passed pass@1 (10.3s)
  [20/30] GSM-SYM-0000 ✓ passed pass@1 (10.6s)
  [21/30] GSM-SYM-0000 ✓ passed pass@1 (8.6s)
  [22/30] GSM-SYM-0000 ✓ passed pass@1 (8.7s)
  [23/30] GSM-SYM-0000 ✓ passed pass@1 (10.3s)
  [24/30] GSM-SYM-0000 ✓ passed pass@1 (9.7s)
  [25/30] GSM-SYM-0000 ✓ passed pass@1 (8.6s)
  [26/30] GSM-SYM-0000 ✓ passed pass@1 (9.6s)
  [27/30] GSM-SYM-0000 ✓ passed pass@1 (10.5s)
  [28/30] GSM-SYM-0000 ✓ passed pass@1 (8.5s)
  [29/30] GSM-SYM-0000 ✓ passed pass@1 (9.4s)
  [30/30] GSM-SYM-0000 ✓ passed pass@1 (9.2s)
gsm-symbolic-30 (v0.1.0) | pass@1 30 / 30 (100%) | pass@3 30 / 30 (100%) | 9.29s | ok

Pack | Pass@1 | Pass@3 | Flaky | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---
humaneval-plus-30 (v0.1.0) | 28 / 30 (93%) | 30 / 30 (100%) | 2 | 9.78s | 21.32s | ok
lcb-v6-30 (v0.1.0) | 28 / 30 (93%) | 30 / 30 (100%) | 2 | 123.04s | 816.30s | ok
gpqa-diamond (v0.1.0) | 0 / 0 (-) | - | - | - | - | skipped
gsm-symbolic-30 (v0.1.0) | 30 / 30 (100%) | 30 / 30 (100%) | 0 | 9.29s | 10.61s | ok

TOTAL | 86 / 90 (96%) | 90 / 90 (100%) | 4 |  |  |

Inline retry classification (clean pass@1 rows omitted):

Scenario | Label | Attempts | Pass@k credit
---|---|---:|---
humaneval-plus-30/HumanEval-4 | pass@2 | 2 | yes
humaneval-plus-30/HumanEval-22 | pass@2 | 2 | yes
lcb-v6-30/LCBv6-3562 | pass@2 | 2 | yes
lcb-v6-30/LCBv6-3733 | pass@3 | 3 | yes

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
humaneval-plus-30 | 0 / 32 (0.0%) | code_start=6, last_fenced=26 | no_fenced_block=6, none=26 | message.content=32
lcb-v6-30 | 0 / 33 (0.0%) | code_start=6, last_fenced=26, opening_fence=1 | no_fenced_block=6, none=26, unterminated_fence=1 | message.content=33
gsm-symbolic-30 | 0 / 30 (0.0%) | — | — | message.content=30

Failure breakdown:
- humaneval-plus-30 HumanEval-4: verifier_fail [pass@2] (HumanEval-4: Traceback (most recent call last):
  File "/tmp/tmpceap7xvx.py", line 1, in <module>
    def mean_absolute_deviation(numbers: List[float]) -> float:
                                         ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-22: wrong_answer [pass@2] (HumanEval-22: Traceback (most recent call last):
  File "/tmp/tmp346jj2fr.py", line 47, in <module>
    check(filter_integers)
  File "/tmp/tmp346jj2fr.py", line 44, in check
    assertion(candidate(*inp), exp, 0)
  File "/tmp/tmp346jj2fr.py", line 37, in assertion
    assert exact_match
           ^^^^^^^^^^^
AssertionError
)
- lcb-v6-30 LCBv6-3562: wrong_answer [pass@2] (LCBv6-3562: Traceback (most recent call last):
  File "/tmp/tmp_yn907ir.py", line 72, in <module>
    _run()
  File "/tmp/tmp_yn907ir.py", line 71, in _run
    raise AssertionError(f"test {i}: expected {expected!r}, got {got!r}")
AssertionError: test 0: expected [2, 3], got []
)
- lcb-v6-30 LCBv6-3733: wrong_answer [pass@3] (LCBv6-3733: Traceback (most recent call last):
  File "/tmp/tmpc9t5666r.py", line 126, in <module>
    _run()
  File "/tmp/tmpc9t5666r.py", line 125, in _run
    raise AssertionError(f"test {i}: expected {expected!r}, got {got!r}")
AssertionError: test 0: expected 5, got 4
)

Warnings:
- GPQA is gated on Hugging Face; authenticate and run the future pack builder to materialize gpqa-diamond scenarios. No GPQA data is committed here.
```

</details>
