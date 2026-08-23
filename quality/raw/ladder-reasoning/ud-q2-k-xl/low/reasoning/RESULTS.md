## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
humaneval-plus-30 (v0.1.0) | 18 / 30 | 60% | — | — | 9.64s | 16.83s | ok
lcb-v6-30 (v0.1.0) | 29 / 30 | 97% | — | — | 99.21s | 1026.79s | ok
gpqa-diamond (v0.1.0) | 0 / 0 | - | — | — | - | - | skipped
gsm-symbolic-30 (v0.1.0) | 29 / 30 | 97% | — | — | 6.10s | 8.26s | ok

TOTAL | 76 / 90 | 84% |  |  |  |  |

Equivalent to: 127/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --reasoning  (endpoint: http://127.0.0.1:19092/v1, model: bench, thinking=on, 2026-08-22T16:16:36.479407Z) ===

  [1/30] HumanEval-0 ✗ verifier_fail fail (8.1s)
  [2/30] HumanEval-1 ✗ verifier_fail pass@3 (16.8s)
  [3/30] HumanEval-2 ✓ passed pass@1 (13.4s)
  [4/30] HumanEval-3 ✗ verifier_fail pass@3 (6.0s)
  [5/30] HumanEval-4 ✗ verifier_fail fail (9.8s)
  [6/30] HumanEval-5 ✓ passed pass@1 (10.5s)
  [7/30] HumanEval-6 ✓ passed pass@1 (15.3s)
  [8/30] HumanEval-7 ✓ passed pass@1 (4.6s)
  [9/30] HumanEval-8 ✓ passed pass@1 (10.2s)
  [10/30] HumanEval-9 ✗ verifier_fail pass@3 (8.7s)
  [11/30] HumanEval-10 ✗ verifier_fail pass@2 (19.8s)
  [12/30] HumanEval-11 ✓ passed pass@1 (7.8s)
  [13/30] HumanEval-12 ✗ verifier_fail fail (7.0s)
  [14/30] HumanEval-13 ✓ passed pass@1 (10.5s)
  [15/30] HumanEval-14 ✓ passed pass@1 (4.4s)
  [16/30] HumanEval-15 ✓ passed pass@1 (5.4s)
  [17/30] HumanEval-16 ✓ passed pass@1 (5.2s)
  [18/30] HumanEval-17 ✓ passed pass@1 (14.4s)
  [19/30] HumanEval-18 ✓ passed pass@1 (15.6s)
  [20/30] HumanEval-19 ✓ passed pass@1 (10.7s)
  [21/30] HumanEval-20 ✓ passed pass@1 (16.6s)
  [22/30] HumanEval-21 ✗ verifier_fail fail (9.4s)
  [23/30] HumanEval-22 ✗ verifier_fail fail (11.7s)
  [24/30] HumanEval-23 ✓ passed pass@1 (2.5s)
  [25/30] HumanEval-24 ✓ passed pass@1 (10.2s)
  [26/30] HumanEval-25 ✗ verifier_fail pass@3 (9.6s)
  [27/30] HumanEval-26 ✗ verifier_fail pass@2 (9.7s)
  [28/30] HumanEval-27 ✓ passed pass@1 (7.0s)
  [29/30] HumanEval-28 ✗ verifier_fail pass@2 (3.0s)
  [30/30] HumanEval-29 ✓ passed pass@1 (3.6s)
humaneval-plus-30 (v0.1.0) | pass@1 18 / 30 (60%) | pass@3 25 / 30 (83%) | 9.64s | ok
  [1/30] LCBv6-3702 ✓ passed pass@1 (100.8s)
  [2/30] LCBv6-3634 ✓ passed pass@1 (29.4s)
  [3/30] LCBv6-3715 ✓ passed pass@1 (366.2s)
  [4/30] LCBv6-3562 ✓ passed pass@1 (282.1s)
  [5/30] LCBv6-3684 ✓ passed pass@1 (57.2s)
  [6/30] LCBv6-3716 ✓ passed pass@1 (160.2s)
  [7/30] LCBv6-3688 ✓ passed pass@1 (429.5s)
  [8/30] LCBv6-3708 ✓ passed pass@1 (22.2s)
  [9/30] LCBv6-3677 ✓ passed pass@1 (105.3s)
  [10/30] LCBv6-3720 ✓ passed pass@1 (91.1s)
  [11/30] LCBv6-3674 ✓ passed pass@1 (1026.8s)
  [12/30] LCBv6-3731 ✓ passed pass@1 (21.8s)
  [13/30] LCBv6-3714 ✓ passed pass@1 (97.6s)
  [14/30] LCBv6-3737 ✓ passed pass@1 (243.9s)
  [15/30] LCBv6-3725 ✓ passed pass@1 (325.7s)
  [16/30] LCBv6-3704 ✓ passed pass@1 (11.3s)
  [17/30] LCBv6-3721 ✓ passed pass@1 (49.8s)
  [18/30] LCBv6-3751 ✓ passed pass@1 (61.6s)
  [19/30] LCBv6-3753 ✓ passed pass@1 (6.9s)
  [20/30] LCBv6-3754 ✓ passed pass@1 (255.1s)
  [21/30] LCBv6-3697 ✗ verifier_fail pass@2 (80.7s)
  [22/30] LCBv6-3748 ✓ passed pass@1 (49.2s)
  [23/30] LCBv6-3760 ✓ passed pass@1 (39.7s)
  [24/30] LCBv6-3696 ✓ passed pass@1 (540.6s)
  [25/30] LCBv6-3762 ✓ passed pass@1 (1215.3s)
  [26/30] LCBv6-3709 ✓ passed pass@1 (16.7s)
  [27/30] LCBv6-3779 ✓ passed pass@1 (546.6s)
  [28/30] LCBv6-3771 ✓ passed pass@1 (316.6s)
  [29/30] LCBv6-3733 ✓ passed pass@1 (357.3s)
  [30/30] LCBv6-3768 ✓ passed pass@1 (6.8s)
lcb-v6-30 (v0.1.0) | pass@1 29 / 30 (97%) | pass@3 30 / 30 (100%) | 99.21s | ok
gpqa-diamond (v0.1.0) | 0 / 0 | - | - | skipped
  [1/30] GSM-SYM-0000-I000 ✓ passed pass@1 (8.3s)
  [2/30] GSM-SYM-0000-I001 ✓ passed pass@1 (5.9s)
  [3/30] GSM-SYM-0000-I002 ✓ passed pass@1 (6.2s)
  [4/30] GSM-SYM-0000-I003 ✓ passed pass@1 (6.0s)
  [5/30] GSM-SYM-0000-I004 ✓ passed pass@1 (8.9s)
  [6/30] GSM-SYM-0000-I005 ✓ passed pass@1 (6.9s)
  [7/30] GSM-SYM-0000-I006 ✓ passed pass@1 (5.4s)
  [8/30] GSM-SYM-0000-I007 ✓ passed pass@1 (6.7s)
  [9/30] GSM-SYM-0000-I008 ✓ passed pass@1 (7.0s)
  [10/30] GSM-SYM-0000-I009 ✓ passed pass@1 (6.0s)
  [11/30] GSM-SYM-0000-I010 ✓ passed pass@1 (5.6s)
  [12/30] GSM-SYM-0000-I011 ✓ passed pass@1 (6.5s)
  [13/30] GSM-SYM-0000-I012 ✓ passed pass@1 (5.7s)
  [14/30] GSM-SYM-0000-I013 ✓ passed pass@1 (6.8s)
  [15/30] GSM-SYM-0000-I014 ✗ wrong_answer pass@2 (7.3s)
  [16/30] GSM-SYM-0000-I015 ✓ passed pass@1 (6.5s)
  [17/30] GSM-SYM-0000-I016 ✓ passed pass@1 (5.4s)
  [18/30] GSM-SYM-0000-I017 ✓ passed pass@1 (4.7s)
  [19/30] GSM-SYM-0000-I018 ✓ passed pass@1 (7.0s)
  [20/30] GSM-SYM-0000-I019 ✓ passed pass@1 (8.0s)
  [21/30] GSM-SYM-0000-I020 ✓ passed pass@1 (5.6s)
  [22/30] GSM-SYM-0000-I021 ✓ passed pass@1 (6.0s)
  [23/30] GSM-SYM-0000-I022 ✓ passed pass@1 (8.0s)
  [24/30] GSM-SYM-0000-I023 ✓ passed pass@1 (5.7s)
  [25/30] GSM-SYM-0000-I024 ✓ passed pass@1 (5.1s)
  [26/30] GSM-SYM-0000-I025 ✓ passed pass@1 (5.8s)
  [27/30] GSM-SYM-0000-I026 ✓ passed pass@1 (6.2s)
  [28/30] GSM-SYM-0000-I027 ✓ passed pass@1 (5.5s)
  [29/30] GSM-SYM-0000-I028 ✓ passed pass@1 (7.5s)
  [30/30] GSM-SYM-0000-I029 ✓ passed pass@1 (5.7s)
gsm-symbolic-30 (v0.1.0) | pass@1 29 / 30 (97%) | pass@3 30 / 30 (100%) | 6.10s | ok

Pack | Pass@1 | Pass@3 | Flaky | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---
humaneval-plus-30 (v0.1.0) | 18 / 30 (60%) | 25 / 30 (83%) | 7 | 9.64s | 16.83s | ok
lcb-v6-30 (v0.1.0) | 29 / 30 (97%) | 30 / 30 (100%) | 1 | 99.21s | 1026.79s | ok
gpqa-diamond (v0.1.0) | 0 / 0 (-) | - | - | - | - | skipped
gsm-symbolic-30 (v0.1.0) | 29 / 30 (97%) | 30 / 30 (100%) | 1 | 6.10s | 8.26s | ok

TOTAL | 76 / 90 (84%) | 85 / 90 (94%) | 9 |  |  |

Inline retry classification (clean pass@1 rows omitted):

Scenario | Label | Attempts | Pass@k credit
---|---|---:|---
humaneval-plus-30/HumanEval-0 | fail | 3 | no
humaneval-plus-30/HumanEval-1 | pass@3 | 3 | yes
humaneval-plus-30/HumanEval-3 | pass@3 | 3 | yes
humaneval-plus-30/HumanEval-4 | fail | 3 | no
humaneval-plus-30/HumanEval-9 | pass@3 | 3 | yes
humaneval-plus-30/HumanEval-10 | pass@2 | 2 | yes
humaneval-plus-30/HumanEval-12 | fail | 3 | no
humaneval-plus-30/HumanEval-21 | fail | 3 | no
humaneval-plus-30/HumanEval-22 | fail | 3 | no
humaneval-plus-30/HumanEval-25 | pass@3 | 3 | yes
humaneval-plus-30/HumanEval-26 | pass@2 | 2 | yes
humaneval-plus-30/HumanEval-28 | pass@2 | 2 | yes
lcb-v6-30/LCBv6-3697 | pass@2 | 2 | yes
gsm-symbolic-30/GSM-SYM-0000-I014 | pass@2 | 2 | yes

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
humaneval-plus-30 | 0 / 51 (0.0%) | code_start=39, last_fenced=12 | no_fenced_block=39, none=12 | message.content=51
lcb-v6-30 | 0 / 31 (0.0%) | code_start=24, last_fenced=7 | no_fenced_block=24, none=7 | message.content=31
gsm-symbolic-30 | 0 / 31 (0.0%) | — | — | message.content=31

Failure breakdown:
- humaneval-plus-30 HumanEval-0: verifier_fail [fail] (HumanEval-0: Traceback (most recent call last):
  File "/tmp/tmp14tt5a4b.py", line 1, in <module>
    def has_close_elements(numbers: List[float], threshold: float) -> bool:
                                    ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-1: verifier_fail [pass@3] (HumanEval-1: Traceback (most recent call last):
  File "/tmp/tmpl52w8h0v.py", line 1, in <module>
    def separate_paren_groups(paren_string: str) -> List[str]:
                                                    ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-3: verifier_fail [pass@3] (HumanEval-3: Traceback (most recent call last):
  File "/tmp/tmpmcsglz9l.py", line 1, in <module>
    def below_zero(operations: List[int]) -> bool:
                               ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-4: verifier_fail [fail] (HumanEval-4: Traceback (most recent call last):
  File "/tmp/tmpqt12x56h.py", line 1, in <module>
    def mean_absolute_deviation(numbers: List[float]) -> float:
                                         ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-9: verifier_fail [pass@3] (HumanEval-9: Traceback (most recent call last):
  File "/tmp/tmpa6jo9lw0.py", line 1, in <module>
    def rolling_max(numbers: List[int]) -> List[int]:
                             ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-10: verifier_fail [pass@2] (HumanEval-10: Traceback (most recent call last):
  File "/tmp/tmpz7j9et5_.py", line 53, in <module>
    check(make_palindrome)
  File "/tmp/tmpz7j9et5_.py", line 50, in check
    assertion(candidate(*inp), exp, 0)
              ^^^^^^^^^^^^^^^
  File "/tmp/tmpz7j9et5_.py", line 15, in make_palindrome
    if is_palindrome(suffix):
       ^^^^^^^^^^^^^
NameError: name 'is_palindrome' is not defined. Did you mean: 'make_palindrome'?
)
- humaneval-plus-30 HumanEval-12: verifier_fail [fail] (HumanEval-12: Traceback (most recent call last):
  File "/tmp/tmpd5b8mebu.py", line 1, in <module>
    def longest(strings: List[str]) -> Optional[str]:
                         ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-21: verifier_fail [fail] (HumanEval-21: Traceback (most recent call last):
  File "/tmp/tmpbmensz02.py", line 1, in <module>
    def rescale_to_unit(numbers: List[float]) -> List[float]:
                                 ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-22: verifier_fail [fail] (HumanEval-22: Traceback (most recent call last):
  File "/tmp/tmp0stccsbk.py", line 1, in <module>
    def filter_integers(values: List[Any]) -> List[int]:
                                ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-25: verifier_fail [pass@3] (HumanEval-25: Traceback (most recent call last):
  File "/tmp/tmpe_qd43ul.py", line 1, in <module>
    def factorize(n: int) -> List[int]:
                             ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-26: verifier_fail [pass@2] (HumanEval-26: Traceback (most recent call last):
  File "/tmp/tmp0r3a2ir5.py", line 1, in <module>
    def remove_duplicates(numbers: List[int]) -> List[int]:
                                   ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-28: verifier_fail [pass@2] (HumanEval-28: Traceback (most recent call last):
  File "/tmp/tmph4u137hn.py", line 1, in <module>
    def concatenate(strings: List[str]) -> str:
                             ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- lcb-v6-30 LCBv6-3697: verifier_fail [pass@2] (LCBv6-3697: Traceback (most recent call last):
  File "/tmp/tmprrpu2k3e.py", line 63, in <module>
    _run()
  File "/tmp/tmprrpu2k3e.py", line 60, in _run
    got = fn(*args)
          ^^^^^^^^^
  File "/tmp/tmprrpu2k3e.py", line 13, in minimumIncrements
    lcm_val = lcm_val * target[i] // math.gcd(lcm_val, target[i])
                                     ^^^^
NameError: name 'math' is not defined. Did you mean: 'Match'? Or did you forget to import 'math'?
)
- gsm-symbolic-30 GSM-SYM-0000-I014: wrong_answer [pass@2] (expected numeric value 5)

Warnings:
- GPQA is gated on Hugging Face; authenticate and run the future pack builder to materialize gpqa-diamond scenarios. No GPQA data is committed here.
```

</details>
