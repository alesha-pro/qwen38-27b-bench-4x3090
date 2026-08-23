## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
humaneval-plus-30 (v0.1.0) | 22 / 30 | 73% | — | — | 10.49s | 23.01s | ok
lcb-v6-30 (v0.1.0) | 28 / 30 | 93% | — | — | 85.73s | 721.41s | ok
gpqa-diamond (v0.1.0) | 0 / 0 | - | — | — | - | - | skipped
gsm-symbolic-30 (v0.1.0) | 30 / 30 | 100% | — | — | 9.08s | 15.36s | ok

TOTAL | 80 / 90 | 89% |  |  |  |  |

Equivalent to: 133/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --reasoning  (endpoint: http://127.0.0.1:19092/v1, model: bench, thinking=on, 2026-08-21T14:21:30.641562Z) ===

  [1/30] HumanEval-0 ✗ verifier_fail pass@2 (18.6s)
  [2/30] HumanEval-1 ✗ verifier_fail fail (49.3s)
  [3/30] HumanEval-2 ✓ passed pass@1 (12.0s)
  [4/30] HumanEval-3 ✓ passed pass@1 (9.9s)
  [5/30] HumanEval-4 ✓ passed pass@1 (15.0s)
  [6/30] HumanEval-5 ✗ verifier_fail pass@2 (9.7s)
  [7/30] HumanEval-6 ✓ passed pass@1 (16.4s)
  [8/30] HumanEval-7 ✓ passed pass@1 (7.7s)
  [9/30] HumanEval-8 ✓ passed pass@1 (9.9s)
  [10/30] HumanEval-9 ✗ verifier_fail pass@3 (9.6s)
  [11/30] HumanEval-10 ✓ passed pass@1 (23.0s)
  [12/30] HumanEval-11 ✓ passed pass@1 (11.4s)
  [13/30] HumanEval-12 ✓ passed pass@1 (10.6s)
  [14/30] HumanEval-13 ✓ passed pass@1 (5.7s)
  [15/30] HumanEval-14 ✓ passed pass@1 (6.9s)
  [16/30] HumanEval-15 ✓ passed pass@1 (5.4s)
  [17/30] HumanEval-16 ✓ passed pass@1 (6.7s)
  [18/30] HumanEval-17 ✗ verifier_fail fail (12.1s)
  [19/30] HumanEval-18 ✓ passed pass@1 (13.4s)
  [20/30] HumanEval-19 ✓ passed pass@1 (11.6s)
  [21/30] HumanEval-20 ✓ passed pass@1 (17.7s)
  [22/30] HumanEval-21 ✗ verifier_fail pass@2 (10.3s)
  [23/30] HumanEval-22 ✗ verifier_fail pass@2 (10.1s)
  [24/30] HumanEval-23 ✓ passed pass@1 (3.1s)
  [25/30] HumanEval-24 ✓ passed pass@1 (22.8s)
  [26/30] HumanEval-25 ✓ passed pass@1 (17.9s)
  [27/30] HumanEval-26 ✓ passed pass@1 (12.6s)
  [28/30] HumanEval-27 ✓ passed pass@1 (10.4s)
  [29/30] HumanEval-28 ✗ verifier_fail fail (4.2s)
  [30/30] HumanEval-29 ✓ passed pass@1 (7.1s)
humaneval-plus-30 (v0.1.0) | pass@1 22 / 30 (73%) | pass@3 27 / 30 (90%) | 10.49s | ok
  [1/30] LCBv6-3702 ✓ passed pass@1 (32.9s)
  [2/30] LCBv6-3634 ✓ passed pass@1 (27.8s)
  [3/30] LCBv6-3715 ✓ passed pass@1 (290.9s)
  [4/30] LCBv6-3562 ✓ passed pass@1 (370.2s)
  [5/30] LCBv6-3684 ✓ passed pass@1 (49.2s)
  [6/30] LCBv6-3716 ✓ passed pass@1 (209.5s)
  [7/30] LCBv6-3688 ✓ passed pass@1 (721.4s)
  [8/30] LCBv6-3708 ✓ passed pass@1 (28.0s)
  [9/30] LCBv6-3677 ✓ passed pass@1 (146.9s)
  [10/30] LCBv6-3720 ✓ passed pass@1 (119.6s)
  [11/30] LCBv6-3674 ✗ wrong_answer pass@2 (484.4s)
  [12/30] LCBv6-3731 ✓ passed pass@1 (15.9s)
  [13/30] LCBv6-3714 ✓ passed pass@1 (67.4s)
  [14/30] LCBv6-3737 ✓ passed pass@1 (104.1s)
  [15/30] LCBv6-3725 ✓ passed pass@1 (194.7s)
  [16/30] LCBv6-3704 ✓ passed pass@1 (11.4s)
  [17/30] LCBv6-3721 ✓ passed pass@1 (47.5s)
  [18/30] LCBv6-3751 ✓ passed pass@1 (47.5s)
  [19/30] LCBv6-3753 ✓ passed pass@1 (12.3s)
  [20/30] LCBv6-3754 ✓ passed pass@1 (132.5s)
  [21/30] LCBv6-3697 ✓ passed pass@1 (62.8s)
  [22/30] LCBv6-3748 ✓ passed pass@1 (26.5s)
  [23/30] LCBv6-3760 ✓ passed pass@1 (36.2s)
  [24/30] LCBv6-3696 ✓ passed pass@1 (313.9s)
  [25/30] LCBv6-3762 ✗ wrong_answer fail (1048.5s)
  [26/30] LCBv6-3709 ✓ passed pass@1 (31.2s)
  [27/30] LCBv6-3779 ✓ passed pass@1 (109.4s)
  [28/30] LCBv6-3771 ✓ passed pass@1 (534.5s)
  [29/30] LCBv6-3733 ✓ passed pass@1 (352.6s)
  [30/30] LCBv6-3768 ✓ passed pass@1 (16.6s)
lcb-v6-30 (v0.1.0) | pass@1 28 / 30 (93%) | pass@3 29 / 30 (97%) | 85.73s | ok
gpqa-diamond (v0.1.0) | 0 / 0 | - | - | skipped
  [1/30] GSM-SYM-0000 ✓ passed pass@1 (9.8s)
  [2/30] GSM-SYM-0000 ✓ passed pass@1 (6.6s)
  [3/30] GSM-SYM-0000 ✓ passed pass@1 (8.0s)
  [4/30] GSM-SYM-0000 ✓ passed pass@1 (7.6s)
  [5/30] GSM-SYM-0000 ✓ passed pass@1 (8.8s)
  [6/30] GSM-SYM-0000 ✓ passed pass@1 (10.1s)
  [7/30] GSM-SYM-0000 ✓ passed pass@1 (15.4s)
  [8/30] GSM-SYM-0000 ✓ passed pass@1 (8.7s)
  [9/30] GSM-SYM-0000 ✓ passed pass@1 (12.7s)
  [10/30] GSM-SYM-0000 ✓ passed pass@1 (8.5s)
  [11/30] GSM-SYM-0000 ✓ passed pass@1 (10.5s)
  [12/30] GSM-SYM-0000 ✓ passed pass@1 (10.3s)
  [13/30] GSM-SYM-0000 ✓ passed pass@1 (13.6s)
  [14/30] GSM-SYM-0000 ✓ passed pass@1 (10.6s)
  [15/30] GSM-SYM-0000 ✓ passed pass@1 (9.0s)
  [16/30] GSM-SYM-0000 ✓ passed pass@1 (8.6s)
  [17/30] GSM-SYM-0000 ✓ passed pass@1 (7.2s)
  [18/30] GSM-SYM-0000 ✓ passed pass@1 (24.8s)
  [19/30] GSM-SYM-0000 ✓ passed pass@1 (9.2s)
  [20/30] GSM-SYM-0000 ✓ passed pass@1 (7.4s)
  [21/30] GSM-SYM-0000 ✓ passed pass@1 (7.2s)
  [22/30] GSM-SYM-0000 ✓ passed pass@1 (7.7s)
  [23/30] GSM-SYM-0000 ✓ passed pass@1 (9.3s)
  [24/30] GSM-SYM-0000 ✓ passed pass@1 (8.4s)
  [25/30] GSM-SYM-0000 ✓ passed pass@1 (10.3s)
  [26/30] GSM-SYM-0000 ✓ passed pass@1 (6.9s)
  [27/30] GSM-SYM-0000 ✓ passed pass@1 (7.1s)
  [28/30] GSM-SYM-0000 ✓ passed pass@1 (14.9s)
  [29/30] GSM-SYM-0000 ✓ passed pass@1 (9.8s)
  [30/30] GSM-SYM-0000 ✓ passed pass@1 (9.3s)
gsm-symbolic-30 (v0.1.0) | pass@1 30 / 30 (100%) | pass@3 30 / 30 (100%) | 9.08s | ok

Pack | Pass@1 | Pass@3 | Flaky | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---
humaneval-plus-30 (v0.1.0) | 22 / 30 (73%) | 27 / 30 (90%) | 5 | 10.49s | 23.01s | ok
lcb-v6-30 (v0.1.0) | 28 / 30 (93%) | 29 / 30 (97%) | 1 | 85.73s | 721.41s | ok
gpqa-diamond (v0.1.0) | 0 / 0 (-) | - | - | - | - | skipped
gsm-symbolic-30 (v0.1.0) | 30 / 30 (100%) | 30 / 30 (100%) | 0 | 9.08s | 15.36s | ok

TOTAL | 80 / 90 (89%) | 86 / 90 (96%) | 6 |  |  |

Inline retry classification (clean pass@1 rows omitted):

Scenario | Label | Attempts | Pass@k credit
---|---|---:|---
humaneval-plus-30/HumanEval-0 | pass@2 | 2 | yes
humaneval-plus-30/HumanEval-1 | fail | 3 | no
humaneval-plus-30/HumanEval-5 | pass@2 | 2 | yes
humaneval-plus-30/HumanEval-9 | pass@3 | 3 | yes
humaneval-plus-30/HumanEval-17 | fail | 3 | no
humaneval-plus-30/HumanEval-21 | pass@2 | 2 | yes
humaneval-plus-30/HumanEval-22 | pass@2 | 2 | yes
humaneval-plus-30/HumanEval-28 | fail | 3 | no
lcb-v6-30/LCBv6-3674 | pass@2 | 2 | yes
lcb-v6-30/LCBv6-3762 | fail | 3 | no

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
humaneval-plus-30 | 0 / 42 (0.0%) | code_start=42 | no_fenced_block=42 | message.content=42
lcb-v6-30 | 0 / 33 (0.0%) | code_start=31, last_fenced=1, opening_fence_anywhere=1 | no_fenced_block=30, none=1, prose_before_code=1, prose_before_unterminated_fence=1 | message.content=30, message.reasoning_content=3
gsm-symbolic-30 | 0 / 30 (0.0%) | — | — | message.content=30

Failure breakdown:
- humaneval-plus-30 HumanEval-0: verifier_fail [pass@2] (HumanEval-0: Traceback (most recent call last):
  File "/tmp/tmpe64l5tdb.py", line 1, in <module>
    def has_close_elements(numbers: List[float], threshold: float) -> bool:
                                    ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-1: verifier_fail [fail] (HumanEval-1: Traceback (most recent call last):
  File "/tmp/tmpibbj6dc3.py", line 1, in <module>
    def separate_paren_groups(paren_string: str) -> List[str]:
                                                    ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-5: verifier_fail [pass@2] (HumanEval-5: Traceback (most recent call last):
  File "/tmp/tmpzqs3etza.py", line 1, in <module>
    def intersperse(numbers: List[int], delimeter: int) -> List[int]:
                             ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-9: verifier_fail [pass@3] (HumanEval-9: Traceback (most recent call last):
  File "/tmp/tmpvhezdxdc.py", line 1, in <module>
    def rolling_max(numbers: List[int]) -> List[int]:
                             ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-17: verifier_fail [fail] (HumanEval-17: Traceback (most recent call last):
  File "/tmp/tmp1xgibe2f.py", line 1, in <module>
    def parse_music(music_string: str) -> List[int]:
                                          ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-21: verifier_fail [pass@2] (HumanEval-21: Traceback (most recent call last):
  File "/tmp/tmpivj6ht_2.py", line 1, in <module>
    def rescale_to_unit(numbers: List[float]) -> List[float]:
                                 ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-22: verifier_fail [pass@2] (HumanEval-22: Traceback (most recent call last):
  File "/tmp/tmprpap94q1.py", line 1, in <module>
    def filter_integers(values: List[Any]) -> List[int]:
                                ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-28: verifier_fail [fail] (HumanEval-28: Traceback (most recent call last):
  File "/tmp/tmpj6_qzm4t.py", line 1, in <module>
    def concatenate(strings: List[str]) -> str:
                             ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- lcb-v6-30 LCBv6-3674: wrong_answer [pass@2] (LCBv6-3674: Traceback (most recent call last):
  File "/tmp/tmp63bzp9u_.py", line 127, in <module>
    _run()
  File "/tmp/tmp63bzp9u_.py", line 126, in _run
    raise AssertionError(f"test {i}: expected {expected!r}, got {got!r}")
AssertionError: test 0: expected 17, got 21
)
- lcb-v6-30 LCBv6-3762: wrong_answer [fail] (LCBv6-3762: Traceback (most recent call last):
  File "/tmp/tmpl2adqam8.py", line 56, in <module>
    _run()
  File "/tmp/tmpl2adqam8.py", line 55, in _run
    raise AssertionError(f"test {i}: expected {expected!r}, got {got!r}")
AssertionError: test 0: expected 4, got None
)

Warnings:
- GPQA is gated on Hugging Face; authenticate and run the future pack builder to materialize gpqa-diamond scenarios. No GPQA data is committed here.
```

</details>
