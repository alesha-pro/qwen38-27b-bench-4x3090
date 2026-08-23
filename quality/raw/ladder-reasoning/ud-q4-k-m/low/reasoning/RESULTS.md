## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
humaneval-plus-30 (v0.1.0) | 28 / 30 | 93% | — | — | 9.28s | 18.03s | ok
lcb-v6-30 (v0.1.0) | 26 / 30 | 87% | — | — | 89.61s | 1066.90s | ok
gpqa-diamond (v0.1.0) | 0 / 0 | - | — | — | - | - | skipped
gsm-symbolic-30 (v0.1.0) | 30 / 30 | 100% | — | — | 7.53s | 9.03s | ok

TOTAL | 84 / 90 | 93% |  |  |  |  |

Equivalent to: 140/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --reasoning  (endpoint: http://127.0.0.1:19092/v1, model: bench, thinking=on, 2026-08-21T11:15:46.098007Z) ===

  [1/30] HumanEval-0 ✓ passed pass@1 (10.2s)
  [2/30] HumanEval-1 ✓ passed pass@1 (20.8s)
  [3/30] HumanEval-2 ✓ passed pass@1 (8.1s)
  [4/30] HumanEval-3 ✗ verifier_fail pass@2 (6.5s)
  [5/30] HumanEval-4 ✓ passed pass@1 (10.1s)
  [6/30] HumanEval-5 ✓ passed pass@1 (11.7s)
  [7/30] HumanEval-6 ✓ passed pass@1 (14.8s)
  [8/30] HumanEval-7 ✓ passed pass@1 (8.1s)
  [9/30] HumanEval-8 ✓ passed pass@1 (9.2s)
  [10/30] HumanEval-9 ✓ passed pass@1 (11.9s)
  [11/30] HumanEval-10 ✓ passed pass@1 (15.1s)
  [12/30] HumanEval-11 ✓ passed pass@1 (6.8s)
  [13/30] HumanEval-12 ✓ passed pass@1 (8.3s)
  [14/30] HumanEval-13 ✓ passed pass@1 (10.1s)
  [15/30] HumanEval-14 ✓ passed pass@1 (6.0s)
  [16/30] HumanEval-15 ✓ passed pass@1 (4.5s)
  [17/30] HumanEval-16 ✓ passed pass@1 (5.1s)
  [18/30] HumanEval-17 ✓ passed pass@1 (13.1s)
  [19/30] HumanEval-18 ✓ passed pass@1 (16.3s)
  [20/30] HumanEval-19 ✓ passed pass@1 (13.3s)
  [21/30] HumanEval-20 ✗ verifier_fail pass@2 (9.0s)
  [22/30] HumanEval-21 ✓ passed pass@1 (9.3s)
  [23/30] HumanEval-22 ✓ passed pass@1 (10.2s)
  [24/30] HumanEval-23 ✓ passed pass@1 (2.5s)
  [25/30] HumanEval-24 ✓ passed pass@1 (9.1s)
  [26/30] HumanEval-25 ✓ passed pass@1 (18.0s)
  [27/30] HumanEval-26 ✓ passed pass@1 (9.8s)
  [28/30] HumanEval-27 ✓ passed pass@1 (4.3s)
  [29/30] HumanEval-28 ✓ passed pass@1 (3.2s)
  [30/30] HumanEval-29 ✓ passed pass@1 (4.4s)
humaneval-plus-30 (v0.1.0) | pass@1 28 / 30 (93%) | pass@3 30 / 30 (100%) | 9.28s | ok
  [1/30] LCBv6-3702 ✗ wrong_answer pass@2 (27.7s)
  [2/30] LCBv6-3634 ✓ passed pass@1 (18.4s)
  [3/30] LCBv6-3715 ✓ passed pass@1 (128.7s)
  [4/30] LCBv6-3562 ✗ wrong_answer pass@3 (511.6s)
  [5/30] LCBv6-3684 ✓ passed pass@1 (31.0s)
  [6/30] LCBv6-3716 ✓ passed pass@1 (191.0s)
  [7/30] LCBv6-3688 ✓ passed pass@1 (1066.9s)
  [8/30] LCBv6-3708 ✓ passed pass@1 (15.2s)
  [9/30] LCBv6-3677 ✓ passed pass@1 (113.0s)
  [10/30] LCBv6-3720 ✓ passed pass@1 (91.4s)
  [11/30] LCBv6-3674 ✓ passed pass@1 (446.7s)
  [12/30] LCBv6-3731 ✓ passed pass@1 (13.4s)
  [13/30] LCBv6-3714 ✓ passed pass@1 (73.9s)
  [14/30] LCBv6-3737 ✓ passed pass@1 (120.9s)
  [15/30] LCBv6-3725 ✓ passed pass@1 (124.5s)
  [16/30] LCBv6-3704 ✓ passed pass@1 (10.0s)
  [17/30] LCBv6-3721 ✓ passed pass@1 (47.1s)
  [18/30] LCBv6-3751 ✓ passed pass@1 (52.3s)
  [19/30] LCBv6-3753 ✓ passed pass@1 (12.0s)
  [20/30] LCBv6-3754 ✓ passed pass@1 (87.8s)
  [21/30] LCBv6-3697 ✓ passed pass@1 (162.2s)
  [22/30] LCBv6-3748 ✓ passed pass@1 (35.6s)
  [23/30] LCBv6-3760 ✓ passed pass@1 (31.4s)
  [24/30] LCBv6-3696 ✓ passed pass@1 (380.6s)
  [25/30] LCBv6-3762 ✗ verifier_fail fail (1416.8s)
  [26/30] LCBv6-3709 ✓ passed pass@1 (31.3s)
  [27/30] LCBv6-3779 ✓ passed pass@1 (93.8s)
  [28/30] LCBv6-3771 ✓ passed pass@1 (1008.6s)
  [29/30] LCBv6-3733 ✗ wrong_answer pass@3 (582.9s)
  [30/30] LCBv6-3768 ✓ passed pass@1 (14.3s)
lcb-v6-30 (v0.1.0) | pass@1 26 / 30 (87%) | pass@3 29 / 30 (97%) | 89.61s | ok
gpqa-diamond (v0.1.0) | 0 / 0 | - | - | skipped
  [1/30] GSM-SYM-0000 ✓ passed pass@1 (8.9s)
  [2/30] GSM-SYM-0000 ✓ passed pass@1 (6.9s)
  [3/30] GSM-SYM-0000 ✓ passed pass@1 (8.1s)
  [4/30] GSM-SYM-0000 ✓ passed pass@1 (8.6s)
  [5/30] GSM-SYM-0000 ✓ passed pass@1 (7.5s)
  [6/30] GSM-SYM-0000 ✓ passed pass@1 (7.1s)
  [7/30] GSM-SYM-0000 ✓ passed pass@1 (7.3s)
  [8/30] GSM-SYM-0000 ✓ passed pass@1 (8.1s)
  [9/30] GSM-SYM-0000 ✓ passed pass@1 (7.6s)
  [10/30] GSM-SYM-0000 ✓ passed pass@1 (7.3s)
  [11/30] GSM-SYM-0000 ✓ passed pass@1 (7.5s)
  [12/30] GSM-SYM-0000 ✓ passed pass@1 (7.5s)
  [13/30] GSM-SYM-0000 ✓ passed pass@1 (7.3s)
  [14/30] GSM-SYM-0000 ✓ passed pass@1 (8.6s)
  [15/30] GSM-SYM-0000 ✓ passed pass@1 (7.4s)
  [16/30] GSM-SYM-0000 ✓ passed pass@1 (7.1s)
  [17/30] GSM-SYM-0000 ✓ passed pass@1 (7.2s)
  [18/30] GSM-SYM-0000 ✓ passed pass@1 (5.7s)
  [19/30] GSM-SYM-0000 ✓ passed pass@1 (7.4s)
  [20/30] GSM-SYM-0000 ✓ passed pass@1 (7.5s)
  [21/30] GSM-SYM-0000 ✓ passed pass@1 (6.3s)
  [22/30] GSM-SYM-0000 ✓ passed pass@1 (9.0s)
  [23/30] GSM-SYM-0000 ✓ passed pass@1 (7.7s)
  [24/30] GSM-SYM-0000 ✓ passed pass@1 (7.7s)
  [25/30] GSM-SYM-0000 ✓ passed pass@1 (7.9s)
  [26/30] GSM-SYM-0000 ✓ passed pass@1 (7.0s)
  [27/30] GSM-SYM-0000 ✓ passed pass@1 (9.4s)
  [28/30] GSM-SYM-0000 ✓ passed pass@1 (8.9s)
  [29/30] GSM-SYM-0000 ✓ passed pass@1 (7.9s)
  [30/30] GSM-SYM-0000 ✓ passed pass@1 (8.1s)
gsm-symbolic-30 (v0.1.0) | pass@1 30 / 30 (100%) | pass@3 30 / 30 (100%) | 7.53s | ok

Pack | Pass@1 | Pass@3 | Flaky | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---
humaneval-plus-30 (v0.1.0) | 28 / 30 (93%) | 30 / 30 (100%) | 2 | 9.28s | 18.03s | ok
lcb-v6-30 (v0.1.0) | 26 / 30 (87%) | 29 / 30 (97%) | 3 | 89.61s | 1066.90s | ok
gpqa-diamond (v0.1.0) | 0 / 0 (-) | - | - | - | - | skipped
gsm-symbolic-30 (v0.1.0) | 30 / 30 (100%) | 30 / 30 (100%) | 0 | 7.53s | 9.03s | ok

TOTAL | 84 / 90 (93%) | 89 / 90 (99%) | 5 |  |  |

Inline retry classification (clean pass@1 rows omitted):

Scenario | Label | Attempts | Pass@k credit
---|---|---:|---
humaneval-plus-30/HumanEval-3 | pass@2 | 2 | yes
humaneval-plus-30/HumanEval-20 | pass@2 | 2 | yes
lcb-v6-30/LCBv6-3702 | pass@2 | 2 | yes
lcb-v6-30/LCBv6-3562 | pass@3 | 3 | yes
lcb-v6-30/LCBv6-3762 | fail | 3 | no
lcb-v6-30/LCBv6-3733 | pass@3 | 3 | yes

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
humaneval-plus-30 | 0 / 32 (0.0%) | code_start=16, last_fenced=16 | no_fenced_block=16, none=16 | message.content=32
lcb-v6-30 | 0 / 37 (0.0%) | code_start=23, empty=2, last_fenced=11, opening_fence_anywhere=1 | empty_code=2, no_fenced_block=22, none=11, prose_before_code=1, prose_before_unterminated_fence=1 | message.content=33, message.reasoning_content=4
gsm-symbolic-30 | 0 / 30 (0.0%) | — | — | message.content=30

Failure breakdown:
- humaneval-plus-30 HumanEval-3: verifier_fail [pass@2] (HumanEval-3: Traceback (most recent call last):
  File "/tmp/tmpkma0ntp5.py", line 1, in <module>
    def below_zero(operations: List[int]) -> bool:
                               ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-20: verifier_fail [pass@2] (HumanEval-20: Traceback (most recent call last):
  File "/tmp/tmp85tcug42.py", line 1, in <module>
    def find_closest_elements(numbers: List[float]) -> Tuple[float, float]:
                                       ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- lcb-v6-30 LCBv6-3702: wrong_answer [pass@2] (LCBv6-3702: Traceback (most recent call last):
  File "/tmp/tmp9_sj0ng8.py", line 51, in <module>
    _run()
  File "/tmp/tmp9_sj0ng8.py", line 50, in _run
    raise AssertionError(f"test {i}: expected {expected!r}, got {got!r}")
AssertionError: test 0: expected 5, got 0
)
- lcb-v6-30 LCBv6-3562: wrong_answer [pass@3] (LCBv6-3562: Traceback (most recent call last):
  File "/tmp/tmpk_ka682v.py", line 72, in <module>
    _run()
  File "/tmp/tmpk_ka682v.py", line 71, in _run
    raise AssertionError(f"test {i}: expected {expected!r}, got {got!r}")
AssertionError: test 0: expected [2, 3], got []
)
- lcb-v6-30 LCBv6-3762: verifier_fail [fail] (LCBv6-3762:   File "/tmp/tmpr8z1bts4.py", line 27
    if V[i] == max_V
                    ^
SyntaxError: expected ':'
)
- lcb-v6-30 LCBv6-3733: wrong_answer [pass@3] (LCBv6-3733: Traceback (most recent call last):
  File "/tmp/tmpkpvoo39f.py", line 124, in <module>
    _run()
  File "/tmp/tmpkpvoo39f.py", line 123, in _run
    raise AssertionError(f"test {i}: expected {expected!r}, got {got!r}")
AssertionError: test 1: expected 4, got 5
)

Warnings:
- GPQA is gated on Hugging Face; authenticate and run the future pack builder to materialize gpqa-diamond scenarios. No GPQA data is committed here.
```

</details>
