## Quality bench, thinking off, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
humaneval-plus-30 (v0.1.0) | 30 / 30 | 100% | — | — | 5.01s | 9.13s | ok
lcb-v6-30 (v0.1.0) | 24 / 30 | 80% | — | — | 36.80s | 232.35s | ok
gpqa-diamond (v0.1.0) | 0 / 0 | - | — | — | - | - | skipped
gsm-symbolic-30 (v0.1.0) | 30 / 30 | 100% | — | — | 15.08s | 22.34s | ok

TOTAL | 84 / 90 | 93% |  |  |  |  |

Equivalent to: 140/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --reasoning  (endpoint: http://127.0.0.1:19081/v1, model: bench, thinking=off, 2026-08-18T18:15:32.039624Z) ===

  [1/30] HumanEval-0 ✓ passed pass@1 (5.5s)
  [2/30] HumanEval-1 ✓ passed pass@1 (6.9s)
  [3/30] HumanEval-2 ✓ passed pass@1 (3.2s)
  [4/30] HumanEval-3 ✓ passed pass@1 (4.9s)
  [5/30] HumanEval-4 ✓ passed pass@1 (5.8s)
  [6/30] HumanEval-5 ✓ passed pass@1 (4.8s)
  [7/30] HumanEval-6 ✓ passed pass@1 (6.4s)
  [8/30] HumanEval-7 ✓ passed pass@1 (3.6s)
  [9/30] HumanEval-8 ✓ passed pass@1 (5.1s)
  [10/30] HumanEval-9 ✓ passed pass@1 (5.4s)
  [11/30] HumanEval-10 ✓ passed pass@1 (9.1s)
  [12/30] HumanEval-11 ✓ passed pass@1 (6.0s)
  [13/30] HumanEval-12 ✓ passed pass@1 (5.0s)
  [14/30] HumanEval-13 ✓ passed pass@1 (3.5s)
  [15/30] HumanEval-14 ✓ passed pass@1 (2.7s)
  [16/30] HumanEval-15 ✓ passed pass@1 (3.0s)
  [17/30] HumanEval-16 ✓ passed pass@1 (2.6s)
  [18/30] HumanEval-17 ✓ passed pass@1 (8.7s)
  [19/30] HumanEval-18 ✓ passed pass@1 (5.0s)
  [20/30] HumanEval-19 ✓ passed pass@1 (8.4s)
  [21/30] HumanEval-20 ✓ passed pass@1 (9.8s)
  [22/30] HumanEval-21 ✓ passed pass@1 (6.0s)
  [23/30] HumanEval-22 ✓ passed pass@1 (3.8s)
  [24/30] HumanEval-23 ✓ passed pass@1 (1.8s)
  [25/30] HumanEval-24 ✓ passed pass@1 (3.6s)
  [26/30] HumanEval-25 ✓ passed pass@1 (6.7s)
  [27/30] HumanEval-26 ✓ passed pass@1 (5.0s)
  [28/30] HumanEval-27 ✓ passed pass@1 (1.9s)
  [29/30] HumanEval-28 ✓ passed pass@1 (2.3s)
  [30/30] HumanEval-29 ✓ passed pass@1 (3.4s)
humaneval-plus-30 (v0.1.0) | pass@1 30 / 30 (100%) | pass@3 30 / 30 (100%) | 5.01s | ok
  [1/30] LCBv6-3702 ✓ passed pass@1 (6.1s)
  [2/30] LCBv6-3634 ✓ passed pass@1 (45.9s)
  [3/30] LCBv6-3715 ✓ passed pass@1 (96.1s)
  [4/30] LCBv6-3562 ✗ verifier_fail fail (133.4s)
  [5/30] LCBv6-3684 ✓ passed pass@1 (14.4s)
  [6/30] LCBv6-3716 ✓ passed pass@1 (146.1s)
  [7/30] LCBv6-3688 ✓ passed pass@1 (132.8s)
  [8/30] LCBv6-3708 ✓ passed pass@1 (8.2s)
  [9/30] LCBv6-3677 ✓ passed pass@1 (20.4s)
  [10/30] LCBv6-3720 ✓ passed pass@1 (187.0s)
  [11/30] LCBv6-3674 ✓ passed pass@1 (79.1s)
  [12/30] LCBv6-3731 ✓ passed pass@1 (2.9s)
  [13/30] LCBv6-3714 ✓ passed pass@1 (40.3s)
  [14/30] LCBv6-3737 ✓ passed pass@1 (49.6s)
  [15/30] LCBv6-3725 ✗ wrong_answer fail (203.7s)
  [16/30] LCBv6-3704 ✓ passed pass@1 (3.9s)
  [17/30] LCBv6-3721 ✓ passed pass@1 (17.0s)
  [18/30] LCBv6-3751 ✓ passed pass@1 (33.3s)
  [19/30] LCBv6-3753 ✓ passed pass@1 (3.9s)
  [20/30] LCBv6-3754 ✗ wrong_answer fail (232.3s)
  [21/30] LCBv6-3697 ✓ passed pass@1 (9.0s)
  [22/30] LCBv6-3748 ✗ wrong_answer fail (16.0s)
  [23/30] LCBv6-3760 ✓ passed pass@1 (18.2s)
  [24/30] LCBv6-3696 ✗ wrong_answer fail (21.8s)
  [25/30] LCBv6-3762 ✓ passed pass@1 (122.1s)
  [26/30] LCBv6-3709 ✓ passed pass@1 (30.4s)
  [27/30] LCBv6-3779 ✓ passed pass@1 (93.3s)
  [28/30] LCBv6-3771 ✓ passed pass@1 (125.5s)
  [29/30] LCBv6-3733 ✗ wrong_answer fail (268.5s)
  [30/30] LCBv6-3768 ✓ passed pass@1 (3.7s)
lcb-v6-30 (v0.1.0) | pass@1 24 / 30 (80%) | pass@3 24 / 30 (80%) | 36.80s | ok
gpqa-diamond (v0.1.0) | 0 / 0 | - | - | skipped
  [1/30] GSM-SYM-0000 ✓ passed pass@1 (14.5s)
  [2/30] GSM-SYM-0000 ✓ passed pass@1 (15.5s)
  [3/30] GSM-SYM-0000 ✓ passed pass@1 (16.6s)
  [4/30] GSM-SYM-0000 ✓ passed pass@1 (17.5s)
  [5/30] GSM-SYM-0000 ✓ passed pass@1 (15.0s)
  [6/30] GSM-SYM-0000 ✓ passed pass@1 (18.7s)
  [7/30] GSM-SYM-0000 ✓ passed pass@1 (13.2s)
  [8/30] GSM-SYM-0000 ✓ passed pass@1 (14.4s)
  [9/30] GSM-SYM-0000 ✓ passed pass@1 (15.2s)
  [10/30] GSM-SYM-0000 ✓ passed pass@1 (17.6s)
  [11/30] GSM-SYM-0000 ✓ passed pass@1 (16.5s)
  [12/30] GSM-SYM-0000 ✓ passed pass@1 (20.7s)
  [13/30] GSM-SYM-0000 ✓ passed pass@1 (12.6s)
  [14/30] GSM-SYM-0000 ✓ passed pass@1 (16.3s)
  [15/30] GSM-SYM-0000 ✓ passed pass@1 (22.3s)
  [16/30] GSM-SYM-0000 ✓ passed pass@1 (22.6s)
  [17/30] GSM-SYM-0000 ✓ passed pass@1 (12.2s)
  [18/30] GSM-SYM-0000 ✓ passed pass@1 (15.6s)
  [19/30] GSM-SYM-0000 ✓ passed pass@1 (14.1s)
  [20/30] GSM-SYM-0000 ✓ passed pass@1 (14.9s)
  [21/30] GSM-SYM-0000 ✓ passed pass@1 (14.5s)
  [22/30] GSM-SYM-0000 ✓ passed pass@1 (14.4s)
  [23/30] GSM-SYM-0000 ✓ passed pass@1 (16.7s)
  [24/30] GSM-SYM-0000 ✓ passed pass@1 (12.0s)
  [25/30] GSM-SYM-0000 ✓ passed pass@1 (14.8s)
  [26/30] GSM-SYM-0000 ✓ passed pass@1 (12.4s)
  [27/30] GSM-SYM-0000 ✓ passed pass@1 (14.2s)
  [28/30] GSM-SYM-0000 ✓ passed pass@1 (15.7s)
  [29/30] GSM-SYM-0000 ✓ passed pass@1 (18.0s)
  [30/30] GSM-SYM-0000 ✓ passed pass@1 (13.5s)
gsm-symbolic-30 (v0.1.0) | pass@1 30 / 30 (100%) | pass@3 30 / 30 (100%) | 15.08s | ok

Pack | Pass@1 | Pass@3 | Flaky | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---
humaneval-plus-30 (v0.1.0) | 30 / 30 (100%) | 30 / 30 (100%) | 0 | 5.01s | 9.13s | ok
lcb-v6-30 (v0.1.0) | 24 / 30 (80%) | 24 / 30 (80%) | 0 | 36.80s | 232.35s | ok
gpqa-diamond (v0.1.0) | 0 / 0 (-) | - | - | - | - | skipped
gsm-symbolic-30 (v0.1.0) | 30 / 30 (100%) | 30 / 30 (100%) | 0 | 15.08s | 22.34s | ok

TOTAL | 84 / 90 (93%) | 84 / 90 (93%) | 0 |  |  |

Inline retry classification (clean pass@1 rows omitted):

Scenario | Label | Attempts | Pass@k credit
---|---|---:|---
lcb-v6-30/LCBv6-3562 | fail | 3 | no
lcb-v6-30/LCBv6-3725 | fail | 3 | no
lcb-v6-30/LCBv6-3754 | fail | 3 | no
lcb-v6-30/LCBv6-3748 | fail | 3 | no
lcb-v6-30/LCBv6-3696 | fail | 3 | no
lcb-v6-30/LCBv6-3733 | fail | 3 | no

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
humaneval-plus-30 | 0 / 30 (0.0%) | last_fenced=27, opening_fence=3 | none=27, unterminated_fence=3 | message.content=30
lcb-v6-30 | 0 / 42 (0.0%) | code_start=1, last_fenced=41 | no_fenced_block=1, none=41 | message.content=42
gsm-symbolic-30 | 0 / 30 (0.0%) | — | — | message.content=30

Failure breakdown:
- lcb-v6-30 LCBv6-3562: verifier_fail [fail] (LCBv6-3562: Traceback (most recent call last):
  File "/tmp/tmpcmz6ewy8.py", line 331, in <module>
    _run()
  File "/tmp/tmpcmz6ewy8.py", line 328, in _run
    got = fn(*args)
          ^^^^^^^^^
  File "/tmp/tmpcmz6ewy8.py", line 274, in maximumWeight
    p = bisect_left(right_endpoints, l)
        ^^^^^^^^^^^
NameError: name 'bisect_left' is not defined. Did you mean: 'bisect_right'?
)
- lcb-v6-30 LCBv6-3725: wrong_answer [fail] (LCBv6-3725: Traceback (most recent call last):
  File "/tmp/tmp5ydn_dss.py", line 454, in <module>
    _run()
  File "/tmp/tmp5ydn_dss.py", line 453, in _run
    raise AssertionError(f"test {i}: expected {expected!r}, got {got!r}")
AssertionError: test 0: expected 20, got 26
)
- lcb-v6-30 LCBv6-3754: wrong_answer [fail] (LCBv6-3754: Traceback (most recent call last):
  File "/tmp/tmp54dqi66d.py", line 548, in <module>
    _run()
  File "/tmp/tmp54dqi66d.py", line 547, in _run
    raise AssertionError(f"test {i}: expected {expected!r}, got {got!r}")
AssertionError: test 1: expected 6, got 5
)
- lcb-v6-30 LCBv6-3748: wrong_answer [fail] (LCBv6-3748: Traceback (most recent call last):
  File "/tmp/tmp00v_p7e_.py", line 80, in <module>
    _run()
  File "/tmp/tmp00v_p7e_.py", line 79, in _run
    raise AssertionError(f"test {i}: expected {expected!r}, got {got!r}")
AssertionError: test 0: expected [[8, 2, 3], [9, 6, 7], [4, 5, 1]], got [[1, 7, 3], [9, 8, 2], [4, 5, 6]]
)
- lcb-v6-30 LCBv6-3696: wrong_answer [fail] (LCBv6-3696: Traceback (most recent call last):
  File "/tmp/tmpsv_rb5jf.py", line 85, in <module>
    _run()
  File "/tmp/tmpsv_rb5jf.py", line 84, in _run
    raise AssertionError(f"test {i}: expected {expected!r}, got {got!r}")
AssertionError: test 0: expected 11, got 8
)
- lcb-v6-30 LCBv6-3733: wrong_answer [fail] (LCBv6-3733: Traceback (most recent call last):
  File "/tmp/tmpp4sx6b9d.py", line 544, in <module>
    _run()
  File "/tmp/tmpp4sx6b9d.py", line 543, in _run
    raise AssertionError(f"test {i}: expected {expected!r}, got {got!r}")
AssertionError: test 0: expected 5, got 6
)

Warnings:
- GPQA is gated on Hugging Face; authenticate and run the future pack builder to materialize gpqa-diamond scenarios. No GPQA data is committed here.
```

</details>
