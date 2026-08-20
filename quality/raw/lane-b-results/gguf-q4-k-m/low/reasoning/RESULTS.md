## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
humaneval-plus-30 (v0.1.0) | 29 / 30 | 97% | — | — | 8.08s | 20.52s | ok
lcb-v6-30 (v0.1.0) | 26 / 30 | 87% | — | — | 86.15s | 1192.25s | ok
gpqa-diamond (v0.1.0) | 0 / 0 | - | — | — | - | - | skipped
gsm-symbolic-30 (v0.1.0) | 30 / 30 | 100% | — | — | 7.80s | 9.62s | ok

TOTAL | 85 / 90 | 94% |  |  |  |  |

Equivalent to: 142/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --reasoning  (endpoint: http://127.0.0.1:19082/v1, model: bench, thinking=on, 2026-08-19T00:11:21.034440Z) ===

  [1/30] HumanEval-0 ✓ passed pass@1 (12.6s)
  [2/30] HumanEval-1 ✓ passed pass@1 (26.1s)
  [3/30] HumanEval-2 ✓ passed pass@1 (10.0s)
  [4/30] HumanEval-3 ✓ passed pass@1 (6.6s)
  [5/30] HumanEval-4 ✓ passed pass@1 (9.8s)
  [6/30] HumanEval-5 ✓ passed pass@1 (11.5s)
  [7/30] HumanEval-6 ✓ passed pass@1 (17.6s)
  [8/30] HumanEval-7 ✓ passed pass@1 (4.5s)
  [9/30] HumanEval-8 ✓ passed pass@1 (6.8s)
  [10/30] HumanEval-9 ✓ passed pass@1 (6.3s)
  [11/30] HumanEval-10 ✗ verifier_fail pass@2 (20.5s)
  [12/30] HumanEval-11 ✓ passed pass@1 (7.1s)
  [13/30] HumanEval-12 ✓ passed pass@1 (4.9s)
  [14/30] HumanEval-13 ✓ passed pass@1 (5.6s)
  [15/30] HumanEval-14 ✓ passed pass@1 (5.3s)
  [16/30] HumanEval-15 ✓ passed pass@1 (6.1s)
  [17/30] HumanEval-16 ✓ passed pass@1 (5.4s)
  [18/30] HumanEval-17 ✓ passed pass@1 (13.4s)
  [19/30] HumanEval-18 ✓ passed pass@1 (14.8s)
  [20/30] HumanEval-19 ✓ passed pass@1 (8.3s)
  [21/30] HumanEval-20 ✓ passed pass@1 (9.3s)
  [22/30] HumanEval-21 ✓ passed pass@1 (10.0s)
  [23/30] HumanEval-22 ✓ passed pass@1 (9.3s)
  [24/30] HumanEval-23 ✓ passed pass@1 (2.6s)
  [25/30] HumanEval-24 ✓ passed pass@1 (16.3s)
  [26/30] HumanEval-25 ✓ passed pass@1 (16.8s)
  [27/30] HumanEval-26 ✓ passed pass@1 (7.9s)
  [28/30] HumanEval-27 ✓ passed pass@1 (3.8s)
  [29/30] HumanEval-28 ✓ passed pass@1 (3.5s)
  [30/30] HumanEval-29 ✓ passed pass@1 (4.8s)
humaneval-plus-30 (v0.1.0) | pass@1 29 / 30 (97%) | pass@3 30 / 30 (100%) | 8.08s | ok
  [1/30] LCBv6-3702 ✗ wrong_answer pass@2 (32.0s)
  [2/30] LCBv6-3634 ✓ passed pass@1 (39.5s)
  [3/30] LCBv6-3715 ✓ passed pass@1 (263.0s)
  [4/30] LCBv6-3562 ✓ passed pass@1 (493.0s)
  [5/30] LCBv6-3684 ✓ passed pass@1 (42.0s)
  [6/30] LCBv6-3716 ✓ passed pass@1 (214.0s)
  [7/30] LCBv6-3688 ✓ passed pass@1 (245.2s)
  [8/30] LCBv6-3708 ✓ passed pass@1 (15.4s)
  [9/30] LCBv6-3677 ✓ passed pass@1 (122.2s)
  [10/30] LCBv6-3720 ✓ passed pass@1 (77.9s)
  [11/30] LCBv6-3674 ✗ wrong_answer pass@2 (1192.3s)
  [12/30] LCBv6-3731 ✓ passed pass@1 (16.9s)
  [13/30] LCBv6-3714 ✓ passed pass@1 (99.0s)
  [14/30] LCBv6-3737 ✓ passed pass@1 (119.5s)
  [15/30] LCBv6-3725 ✓ passed pass@1 (167.5s)
  [16/30] LCBv6-3704 ✓ passed pass@1 (11.9s)
  [17/30] LCBv6-3721 ✓ passed pass@1 (64.2s)
  [18/30] LCBv6-3751 ✓ passed pass@1 (49.6s)
  [19/30] LCBv6-3753 ✓ passed pass@1 (9.9s)
  [20/30] LCBv6-3754 ✓ passed pass@1 (135.1s)
  [21/30] LCBv6-3697 ✓ passed pass@1 (93.5s)
  [22/30] LCBv6-3748 ✓ passed pass@1 (37.5s)
  [23/30] LCBv6-3760 ✓ passed pass@1 (38.5s)
  [24/30] LCBv6-3696 ✓ passed pass@1 (872.2s)
  [25/30] LCBv6-3762 ✗ wrong_answer pass@3 (1488.5s)
  [26/30] LCBv6-3709 ✓ passed pass@1 (12.3s)
  [27/30] LCBv6-3779 ✓ passed pass@1 (78.8s)
  [28/30] LCBv6-3771 ✓ passed pass@1 (298.3s)
  [29/30] LCBv6-3733 ✗ verifier_fail pass@3 (361.5s)
  [30/30] LCBv6-3768 ✓ passed pass@1 (14.8s)
lcb-v6-30 (v0.1.0) | pass@1 26 / 30 (87%) | pass@3 30 / 30 (100%) | 86.15s | ok
gpqa-diamond (v0.1.0) | 0 / 0 | - | - | skipped
  [1/30] GSM-SYM-0000 ✓ passed pass@1 (6.2s)
  [2/30] GSM-SYM-0000 ✓ passed pass@1 (7.8s)
  [3/30] GSM-SYM-0000 ✓ passed pass@1 (7.1s)
  [4/30] GSM-SYM-0000 ✓ passed pass@1 (6.9s)
  [5/30] GSM-SYM-0000 ✓ passed pass@1 (8.2s)
  [6/30] GSM-SYM-0000 ✓ passed pass@1 (7.2s)
  [7/30] GSM-SYM-0000 ✓ passed pass@1 (7.0s)
  [8/30] GSM-SYM-0000 ✓ passed pass@1 (9.5s)
  [9/30] GSM-SYM-0000 ✓ passed pass@1 (8.6s)
  [10/30] GSM-SYM-0000 ✓ passed pass@1 (8.5s)
  [11/30] GSM-SYM-0000 ✓ passed pass@1 (7.4s)
  [12/30] GSM-SYM-0000 ✓ passed pass@1 (9.1s)
  [13/30] GSM-SYM-0000 ✓ passed pass@1 (8.7s)
  [14/30] GSM-SYM-0000 ✓ passed pass@1 (9.6s)
  [15/30] GSM-SYM-0000 ✓ passed pass@1 (8.5s)
  [16/30] GSM-SYM-0000 ✓ passed pass@1 (6.3s)
  [17/30] GSM-SYM-0000 ✓ passed pass@1 (6.2s)
  [18/30] GSM-SYM-0000 ✓ passed pass@1 (8.0s)
  [19/30] GSM-SYM-0000 ✓ passed pass@1 (6.8s)
  [20/30] GSM-SYM-0000 ✓ passed pass@1 (8.0s)
  [21/30] GSM-SYM-0000 ✓ passed pass@1 (8.1s)
  [22/30] GSM-SYM-0000 ✓ passed pass@1 (7.3s)
  [23/30] GSM-SYM-0000 ✓ passed pass@1 (7.5s)
  [24/30] GSM-SYM-0000 ✓ passed pass@1 (7.7s)
  [25/30] GSM-SYM-0000 ✓ passed pass@1 (8.7s)
  [26/30] GSM-SYM-0000 ✓ passed pass@1 (7.0s)
  [27/30] GSM-SYM-0000 ✓ passed pass@1 (9.7s)
  [28/30] GSM-SYM-0000 ✓ passed pass@1 (7.8s)
  [29/30] GSM-SYM-0000 ✓ passed pass@1 (8.2s)
  [30/30] GSM-SYM-0000 ✓ passed pass@1 (7.1s)
gsm-symbolic-30 (v0.1.0) | pass@1 30 / 30 (100%) | pass@3 30 / 30 (100%) | 7.80s | ok

Pack | Pass@1 | Pass@3 | Flaky | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---
humaneval-plus-30 (v0.1.0) | 29 / 30 (97%) | 30 / 30 (100%) | 1 | 8.08s | 20.52s | ok
lcb-v6-30 (v0.1.0) | 26 / 30 (87%) | 30 / 30 (100%) | 4 | 86.15s | 1192.25s | ok
gpqa-diamond (v0.1.0) | 0 / 0 (-) | - | - | - | - | skipped
gsm-symbolic-30 (v0.1.0) | 30 / 30 (100%) | 30 / 30 (100%) | 0 | 7.80s | 9.62s | ok

TOTAL | 85 / 90 (94%) | 90 / 90 (100%) | 5 |  |  |

Inline retry classification (clean pass@1 rows omitted):

Scenario | Label | Attempts | Pass@k credit
---|---|---:|---
humaneval-plus-30/HumanEval-10 | pass@2 | 2 | yes
lcb-v6-30/LCBv6-3702 | pass@2 | 2 | yes
lcb-v6-30/LCBv6-3674 | pass@2 | 2 | yes
lcb-v6-30/LCBv6-3762 | pass@3 | 3 | yes
lcb-v6-30/LCBv6-3733 | pass@3 | 3 | yes

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
humaneval-plus-30 | 0 / 31 (0.0%) | code_start=6, last_fenced=25 | no_fenced_block=6, none=25 | message.content=31
lcb-v6-30 | 0 / 36 (0.0%) | code_start=8, empty=1, last_fenced=26, opening_fence=1 | empty_code=1, no_fenced_block=8, none=26, unterminated_fence=1 | message.content=34, message.reasoning_content=2
gsm-symbolic-30 | 0 / 30 (0.0%) | — | — | message.content=30

Failure breakdown:
- humaneval-plus-30 HumanEval-10: verifier_fail [pass@2] (HumanEval-10: Traceback (most recent call last):
  File "/tmp/tmppkp6enuv.py", line 54, in <module>
    check(make_palindrome)
  File "/tmp/tmppkp6enuv.py", line 51, in check
    assertion(candidate(*inp), exp, 0)
              ^^^^^^^^^^^^^^^
  File "/tmp/tmppkp6enuv.py", line 17, in make_palindrome
    if is_palindrome(string[i:]):
       ^^^^^^^^^^^^^
NameError: name 'is_palindrome' is not defined. Did you mean: 'make_palindrome'?
)
- lcb-v6-30 LCBv6-3702: wrong_answer [pass@2] (LCBv6-3702: Traceback (most recent call last):
  File "/tmp/tmpz3d5e842.py", line 51, in <module>
    _run()
  File "/tmp/tmpz3d5e842.py", line 50, in _run
    raise AssertionError(f"test {i}: expected {expected!r}, got {got!r}")
AssertionError: test 0: expected 5, got 0
)
- lcb-v6-30 LCBv6-3674: wrong_answer [pass@2] (LCBv6-3674: Traceback (most recent call last):
  File "/tmp/tmpcjtgdg17.py", line 104, in <module>
    _run()
  File "/tmp/tmpcjtgdg17.py", line 103, in _run
    raise AssertionError(f"test {i}: expected {expected!r}, got {got!r}")
AssertionError: test 0: expected 17, got None
)
- lcb-v6-30 LCBv6-3762: wrong_answer [pass@3] (LCBv6-3762: no runnable-looking Python code extracted)
- lcb-v6-30 LCBv6-3733: verifier_fail [pass@3] (LCBv6-3733: Traceback (most recent call last):
  File "/tmp/tmpmfcck4eg.py", line 111, in <module>
    _run()
  File "/tmp/tmpmfcck4eg.py", line 108, in _run
    got = fn(*args)
          ^^^^^^^^^
  File "/tmp/tmpmfcck4eg.py", line 34, in lenOfVDiagonal
    arr[r][c] = 1 + run[d*2 + (1-v)][nr][nc]
                    ~~~^^^^^^^^^^^^^
IndexError: list index out of range
)

Warnings:
- GPQA is gated on Hugging Face; authenticate and run the future pack builder to materialize gpqa-diamond scenarios. No GPQA data is committed here.
```

</details>
