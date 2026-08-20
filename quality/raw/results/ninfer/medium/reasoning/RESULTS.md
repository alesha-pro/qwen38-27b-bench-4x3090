## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
humaneval-plus-30 (v0.1.0) | 23 / 30 | 77% | — | — | 14.13s | 29.28s | ok
lcb-v6-30 (v0.1.0) | 29 / 30 | 97% | — | — | 121.20s | 909.74s | ok
gpqa-diamond (v0.1.0) | 0 / 0 | - | — | — | - | - | skipped
gsm-symbolic-30 (v0.1.0) | 30 / 30 | 100% | — | — | 9.76s | 16.76s | ok

TOTAL | 82 / 90 | 91% |  |  |  |  |

Equivalent to: 137/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --reasoning  (endpoint: http://127.0.0.1:19081/v1, model: bench, thinking=on, 2026-08-18T22:03:44.841718Z) ===

  [1/30] HumanEval-0 ✗ verifier_fail pass@3 (14.7s)
  [2/30] HumanEval-1 ✗ verifier_fail fail (19.3s)
  [3/30] HumanEval-2 ✓ passed pass@1 (8.4s)
  [4/30] HumanEval-3 ✗ verifier_fail fail (10.4s)
  [5/30] HumanEval-4 ✓ passed pass@1 (13.2s)
  [6/30] HumanEval-5 ✗ verifier_fail pass@2 (16.2s)
  [7/30] HumanEval-6 ✓ passed pass@1 (20.9s)
  [8/30] HumanEval-7 ✗ verifier_fail pass@2 (7.0s)
  [9/30] HumanEval-8 ✓ passed pass@1 (13.5s)
  [10/30] HumanEval-9 ✓ passed pass@1 (16.6s)
  [11/30] HumanEval-10 ✓ passed pass@1 (29.3s)
  [12/30] HumanEval-11 ✓ passed pass@1 (15.2s)
  [13/30] HumanEval-12 ✓ passed pass@1 (11.1s)
  [14/30] HumanEval-13 ✓ passed pass@1 (6.7s)
  [15/30] HumanEval-14 ✓ passed pass@1 (7.8s)
  [16/30] HumanEval-15 ✓ passed pass@1 (8.5s)
  [17/30] HumanEval-16 ✓ passed pass@1 (10.6s)
  [18/30] HumanEval-17 ✗ verifier_fail pass@2 (15.2s)
  [19/30] HumanEval-18 ✓ passed pass@1 (16.0s)
  [20/30] HumanEval-19 ✓ passed pass@1 (16.4s)
  [21/30] HumanEval-20 ✓ passed pass@1 (35.5s)
  [22/30] HumanEval-21 ✓ passed pass@1 (16.7s)
  [23/30] HumanEval-22 ✗ verifier_fail pass@2 (20.4s)
  [24/30] HumanEval-23 ✓ passed pass@1 (3.0s)
  [25/30] HumanEval-24 ✓ passed pass@1 (21.6s)
  [26/30] HumanEval-25 ✓ passed pass@1 (23.1s)
  [27/30] HumanEval-26 ✓ passed pass@1 (11.4s)
  [28/30] HumanEval-27 ✓ passed pass@1 (5.0s)
  [29/30] HumanEval-28 ✓ passed pass@1 (4.0s)
  [30/30] HumanEval-29 ✓ passed pass@1 (12.3s)
humaneval-plus-30 (v0.1.0) | pass@1 23 / 30 (77%) | pass@3 28 / 30 (93%) | 14.13s | ok
  [1/30] LCBv6-3702 ✓ passed pass@1 (74.2s)
  [2/30] LCBv6-3634 ✓ passed pass@1 (60.4s)
  [3/30] LCBv6-3715 ✓ passed pass@1 (147.9s)
  [4/30] LCBv6-3562 ✓ passed pass@1 (909.7s)
  [5/30] LCBv6-3684 ✓ passed pass@1 (43.8s)
  [6/30] LCBv6-3716 ✓ passed pass@1 (230.3s)
  [7/30] LCBv6-3688 ✓ passed pass@1 (463.2s)
  [8/30] LCBv6-3708 ✓ passed pass@1 (38.9s)
  [9/30] LCBv6-3677 ✓ passed pass@1 (137.9s)
  [10/30] LCBv6-3720 ✓ passed pass@1 (152.2s)
  [11/30] LCBv6-3674 ✓ passed pass@1 (1083.7s)
  [12/30] LCBv6-3731 ✓ passed pass@1 (18.3s)
  [13/30] LCBv6-3714 ✓ passed pass@1 (94.5s)
  [14/30] LCBv6-3737 ✓ passed pass@1 (158.6s)
  [15/30] LCBv6-3725 ✓ passed pass@1 (235.5s)
  [16/30] LCBv6-3704 ✓ passed pass@1 (17.9s)
  [17/30] LCBv6-3721 ✓ passed pass@1 (80.0s)
  [18/30] LCBv6-3751 ✓ passed pass@1 (66.8s)
  [19/30] LCBv6-3753 ✓ passed pass@1 (13.9s)
  [20/30] LCBv6-3754 ✓ passed pass@1 (128.9s)
  [21/30] LCBv6-3697 ✓ passed pass@1 (113.5s)
  [22/30] LCBv6-3748 ✗ wrong_answer pass@2 (58.3s)
  [23/30] LCBv6-3760 ✓ passed pass@1 (32.2s)
  [24/30] LCBv6-3696 ✓ passed pass@1 (803.6s)
  [25/30] LCBv6-3762 ✓ passed pass@1 (568.3s)
  [26/30] LCBv6-3709 ✓ passed pass@1 (24.1s)
  [27/30] LCBv6-3779 ✓ passed pass@1 (158.8s)
  [28/30] LCBv6-3771 ✓ passed pass@1 (685.8s)
  [29/30] LCBv6-3733 ✓ passed pass@1 (336.7s)
  [30/30] LCBv6-3768 ✓ passed pass@1 (19.9s)
lcb-v6-30 (v0.1.0) | pass@1 29 / 30 (97%) | pass@3 30 / 30 (100%) | 121.20s | ok
gpqa-diamond (v0.1.0) | 0 / 0 | - | - | skipped
  [1/30] GSM-SYM-0000 ✓ passed pass@1 (10.3s)
  [2/30] GSM-SYM-0000 ✓ passed pass@1 (11.0s)
  [3/30] GSM-SYM-0000 ✓ passed pass@1 (7.8s)
  [4/30] GSM-SYM-0000 ✓ passed pass@1 (9.5s)
  [5/30] GSM-SYM-0000 ✓ passed pass@1 (12.7s)
  [6/30] GSM-SYM-0000 ✓ passed pass@1 (19.3s)
  [7/30] GSM-SYM-0000 ✓ passed pass@1 (7.5s)
  [8/30] GSM-SYM-0000 ✓ passed pass@1 (13.0s)
  [9/30] GSM-SYM-0000 ✓ passed pass@1 (8.5s)
  [10/30] GSM-SYM-0000 ✓ passed pass@1 (9.2s)
  [11/30] GSM-SYM-0000 ✓ passed pass@1 (8.2s)
  [12/30] GSM-SYM-0000 ✓ passed pass@1 (12.7s)
  [13/30] GSM-SYM-0000 ✓ passed pass@1 (7.5s)
  [14/30] GSM-SYM-0000 ✓ passed pass@1 (13.1s)
  [15/30] GSM-SYM-0000 ✓ passed pass@1 (16.8s)
  [16/30] GSM-SYM-0000 ✓ passed pass@1 (9.3s)
  [17/30] GSM-SYM-0000 ✓ passed pass@1 (7.5s)
  [18/30] GSM-SYM-0000 ✓ passed pass@1 (8.9s)
  [19/30] GSM-SYM-0000 ✓ passed pass@1 (9.9s)
  [20/30] GSM-SYM-0000 ✓ passed pass@1 (7.5s)
  [21/30] GSM-SYM-0000 ✓ passed pass@1 (8.7s)
  [22/30] GSM-SYM-0000 ✓ passed pass@1 (9.6s)
  [23/30] GSM-SYM-0000 ✓ passed pass@1 (7.5s)
  [24/30] GSM-SYM-0000 ✓ passed pass@1 (7.6s)
  [25/30] GSM-SYM-0000 ✓ passed pass@1 (12.1s)
  [26/30] GSM-SYM-0000 ✓ passed pass@1 (12.0s)
  [27/30] GSM-SYM-0000 ✓ passed pass@1 (12.2s)
  [28/30] GSM-SYM-0000 ✓ passed pass@1 (14.1s)
  [29/30] GSM-SYM-0000 ✓ passed pass@1 (9.9s)
  [30/30] GSM-SYM-0000 ✓ passed pass@1 (12.5s)
gsm-symbolic-30 (v0.1.0) | pass@1 30 / 30 (100%) | pass@3 30 / 30 (100%) | 9.76s | ok

Pack | Pass@1 | Pass@3 | Flaky | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---
humaneval-plus-30 (v0.1.0) | 23 / 30 (77%) | 28 / 30 (93%) | 5 | 14.13s | 29.28s | ok
lcb-v6-30 (v0.1.0) | 29 / 30 (97%) | 30 / 30 (100%) | 1 | 121.20s | 909.74s | ok
gpqa-diamond (v0.1.0) | 0 / 0 (-) | - | - | - | - | skipped
gsm-symbolic-30 (v0.1.0) | 30 / 30 (100%) | 30 / 30 (100%) | 0 | 9.76s | 16.76s | ok

TOTAL | 82 / 90 (91%) | 88 / 90 (98%) | 6 |  |  |

Inline retry classification (clean pass@1 rows omitted):

Scenario | Label | Attempts | Pass@k credit
---|---|---:|---
humaneval-plus-30/HumanEval-0 | pass@3 | 3 | yes
humaneval-plus-30/HumanEval-1 | fail | 3 | no
humaneval-plus-30/HumanEval-3 | fail | 3 | no
humaneval-plus-30/HumanEval-5 | pass@2 | 2 | yes
humaneval-plus-30/HumanEval-7 | pass@2 | 2 | yes
humaneval-plus-30/HumanEval-17 | pass@2 | 2 | yes
humaneval-plus-30/HumanEval-22 | pass@2 | 2 | yes
lcb-v6-30/LCBv6-3748 | pass@2 | 2 | yes

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
humaneval-plus-30 | 0 / 40 (0.0%) | code_start=39, last_fenced=1 | no_fenced_block=39, none=1 | message.content=40
lcb-v6-30 | 0 / 31 (0.0%) | code_start=22, last_fenced=9 | no_fenced_block=22, none=9 | message.content=31
gsm-symbolic-30 | 0 / 30 (0.0%) | — | — | message.content=30

Failure breakdown:
- humaneval-plus-30 HumanEval-0: verifier_fail [pass@3] (HumanEval-0: Traceback (most recent call last):
  File "/tmp/tmp5c2cpyef.py", line 1, in <module>
    def has_close_elements(numbers: List[float], threshold: float) -> bool:
                                    ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-1: verifier_fail [fail] (HumanEval-1: Traceback (most recent call last):
  File "/tmp/tmpc07wuz7g.py", line 1, in <module>
    def separate_paren_groups(paren_string: str) -> List[str]:
                                                    ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-3: verifier_fail [fail] (HumanEval-3: Traceback (most recent call last):
  File "/tmp/tmpwq9gjtc8.py", line 1, in <module>
    def below_zero(operations: List[int]) -> bool:
                               ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-5: verifier_fail [pass@2] (HumanEval-5: Traceback (most recent call last):
  File "/tmp/tmpyc6q2ipc.py", line 1, in <module>
    def intersperse(numbers: List[int], delimeter: int) -> List[int]:
                             ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-7: verifier_fail [pass@2] (HumanEval-7: Traceback (most recent call last):
  File "/tmp/tmplob6b6ud.py", line 1, in <module>
    def filter_by_substring(strings: List[str], substring: str) -> List[str]:
                                     ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-17: verifier_fail [pass@2] (HumanEval-17: Traceback (most recent call last):
  File "/tmp/tmpbpsjdwkw.py", line 1, in <module>
    def parse_music(music_string: str) -> List[int]:
                                          ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-22: verifier_fail [pass@2] (HumanEval-22: Traceback (most recent call last):
  File "/tmp/tmpc8ke3tv0.py", line 1, in <module>
    def filter_integers(values: List[Any]) -> List[int]:
                                ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- lcb-v6-30 LCBv6-3748: wrong_answer [pass@2] (LCBv6-3748: Traceback (most recent call last):
  File "/tmp/tmp_aq18h98.py", line 52, in <module>
    _run()
  File "/tmp/tmp_aq18h98.py", line 51, in _run
    raise AssertionError(f"test {i}: expected {expected!r}, got {got!r}")
AssertionError: test 0: expected [[8, 2, 3], [9, 6, 7], [4, 5, 1]], got [[1, 7, 3], [9, 8, 2], [4, 5, 6]]
)

Warnings:
- GPQA is gated on Hugging Face; authenticate and run the future pack builder to materialize gpqa-diamond scenarios. No GPQA data is committed here.
```

</details>
