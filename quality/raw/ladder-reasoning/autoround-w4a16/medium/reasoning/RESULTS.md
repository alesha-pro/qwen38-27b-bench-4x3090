## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
humaneval-plus-30 (v0.1.0) | 24 / 30 | 80% | — | — | 2.33s | 3.51s | ok
lcb-v6-30 (v0.1.0) | 29 / 30 | 97% | — | — | 20.72s | 226.58s | ok
gpqa-diamond (v0.1.0) | 0 / 0 | - | — | — | - | - | skipped
gsm-symbolic-30 (v0.1.0) | 30 / 30 | 100% | — | — | 2.27s | 2.80s | ok

TOTAL | 83 / 90 | 92% |  |  |  |  |

Equivalent to: 138/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --reasoning  (endpoint: http://127.0.0.1:19092/v1, model: bench, thinking=on, 2026-08-20T22:13:38.808236Z) ===

  [1/30] HumanEval-0 ✓ passed pass@1 (3.3s)
  [2/30] HumanEval-1 ✗ verifier_fail pass@3 (3.0s)
  [3/30] HumanEval-2 ✓ passed pass@1 (1.4s)
  [4/30] HumanEval-3 ✗ verifier_fail fail (1.3s)
  [5/30] HumanEval-4 ✓ passed pass@1 (2.3s)
  [6/30] HumanEval-5 ✓ passed pass@1 (1.9s)
  [7/30] HumanEval-6 ✗ verifier_fail fail (2.9s)
  [8/30] HumanEval-7 ✓ passed pass@1 (1.2s)
  [9/30] HumanEval-8 ✗ verifier_fail pass@2 (1.2s)
  [10/30] HumanEval-9 ✓ passed pass@1 (2.8s)
  [11/30] HumanEval-10 ✓ passed pass@1 (4.5s)
  [12/30] HumanEval-11 ✓ passed pass@1 (2.4s)
  [13/30] HumanEval-12 ✓ passed pass@1 (2.5s)
  [14/30] HumanEval-13 ✓ passed pass@1 (2.2s)
  [15/30] HumanEval-14 ✓ passed pass@1 (1.4s)
  [16/30] HumanEval-15 ✓ passed pass@1 (1.4s)
  [17/30] HumanEval-16 ✓ passed pass@1 (1.0s)
  [18/30] HumanEval-17 ✓ passed pass@1 (3.0s)
  [19/30] HumanEval-18 ✓ passed pass@1 (2.9s)
  [20/30] HumanEval-19 ✓ passed pass@1 (2.9s)
  [21/30] HumanEval-20 ✓ passed pass@1 (3.5s)
  [22/30] HumanEval-21 ✓ passed pass@1 (2.5s)
  [23/30] HumanEval-22 ✗ verifier_fail pass@2 (2.4s)
  [24/30] HumanEval-23 ✓ passed pass@1 (0.6s)
  [25/30] HumanEval-24 ✓ passed pass@1 (3.1s)
  [26/30] HumanEval-25 ✓ passed pass@1 (2.4s)
  [27/30] HumanEval-26 ✓ passed pass@1 (1.6s)
  [28/30] HumanEval-27 ✓ passed pass@1 (1.0s)
  [29/30] HumanEval-28 ✗ verifier_fail pass@2 (0.7s)
  [30/30] HumanEval-29 ✓ passed pass@1 (1.4s)
humaneval-plus-30 (v0.1.0) | pass@1 24 / 30 (80%) | pass@3 28 / 30 (93%) | 2.33s | ok
  [1/30] LCBv6-3702 ✓ passed pass@1 (12.8s)
  [2/30] LCBv6-3634 ✓ passed pass@1 (7.7s)
  [3/30] LCBv6-3715 ✓ passed pass@1 (40.7s)
  [4/30] LCBv6-3562 ✓ passed pass@1 (156.8s)
  [5/30] LCBv6-3684 ✓ passed pass@1 (9.8s)
  [6/30] LCBv6-3716 ✓ passed pass@1 (28.0s)
  [7/30] LCBv6-3688 ✓ passed pass@1 (107.6s)
  [8/30] LCBv6-3708 ✓ passed pass@1 (4.5s)
  [9/30] LCBv6-3677 ✓ passed pass@1 (27.5s)
  [10/30] LCBv6-3720 ✓ passed pass@1 (26.9s)
  [11/30] LCBv6-3674 ✓ passed pass@1 (281.8s)
  [12/30] LCBv6-3731 ✓ passed pass@1 (2.8s)
  [13/30] LCBv6-3714 ✓ passed pass@1 (18.9s)
  [14/30] LCBv6-3737 ✓ passed pass@1 (53.5s)
  [15/30] LCBv6-3725 ✓ passed pass@1 (38.6s)
  [16/30] LCBv6-3704 ✓ passed pass@1 (3.2s)
  [17/30] LCBv6-3721 ✓ passed pass@1 (11.4s)
  [18/30] LCBv6-3751 ✓ passed pass@1 (16.5s)
  [19/30] LCBv6-3753 ✓ passed pass@1 (2.6s)
  [20/30] LCBv6-3754 ✓ passed pass@1 (22.5s)
  [21/30] LCBv6-3697 ✓ passed pass@1 (26.1s)
  [22/30] LCBv6-3748 ✓ passed pass@1 (8.3s)
  [23/30] LCBv6-3760 ✓ passed pass@1 (7.5s)
  [24/30] LCBv6-3696 ✓ passed pass@1 (101.5s)
  [25/30] LCBv6-3762 ✗ wrong_answer pass@3 (226.6s)
  [26/30] LCBv6-3709 ✓ passed pass@1 (6.8s)
  [27/30] LCBv6-3779 ✓ passed pass@1 (14.8s)
  [28/30] LCBv6-3771 ✓ passed pass@1 (102.5s)
  [29/30] LCBv6-3733 ✓ passed pass@1 (109.3s)
  [30/30] LCBv6-3768 ✓ passed pass@1 (3.5s)
lcb-v6-30 (v0.1.0) | pass@1 29 / 30 (97%) | pass@3 30 / 30 (100%) | 20.72s | ok
gpqa-diamond (v0.1.0) | 0 / 0 | - | - | skipped
  [1/30] GSM-SYM-0000 ✓ passed pass@1 (2.2s)
  [2/30] GSM-SYM-0000 ✓ passed pass@1 (1.9s)
  [3/30] GSM-SYM-0000 ✓ passed pass@1 (2.3s)
  [4/30] GSM-SYM-0000 ✓ passed pass@1 (1.7s)
  [5/30] GSM-SYM-0000 ✓ passed pass@1 (1.8s)
  [6/30] GSM-SYM-0000 ✓ passed pass@1 (2.0s)
  [7/30] GSM-SYM-0000 ✓ passed pass@1 (1.9s)
  [8/30] GSM-SYM-0000 ✓ passed pass@1 (2.1s)
  [9/30] GSM-SYM-0000 ✓ passed pass@1 (2.6s)
  [10/30] GSM-SYM-0000 ✓ passed pass@1 (2.4s)
  [11/30] GSM-SYM-0000 ✓ passed pass@1 (2.0s)
  [12/30] GSM-SYM-0000 ✓ passed pass@1 (2.3s)
  [13/30] GSM-SYM-0000 ✓ passed pass@1 (2.6s)
  [14/30] GSM-SYM-0000 ✓ passed pass@1 (2.4s)
  [15/30] GSM-SYM-0000 ✓ passed pass@1 (4.7s)
  [16/30] GSM-SYM-0000 ✓ passed pass@1 (2.4s)
  [17/30] GSM-SYM-0000 ✓ passed pass@1 (2.6s)
  [18/30] GSM-SYM-0000 ✓ passed pass@1 (1.5s)
  [19/30] GSM-SYM-0000 ✓ passed pass@1 (1.9s)
  [20/30] GSM-SYM-0000 ✓ passed pass@1 (2.0s)
  [21/30] GSM-SYM-0000 ✓ passed pass@1 (2.5s)
  [22/30] GSM-SYM-0000 ✓ passed pass@1 (2.3s)
  [23/30] GSM-SYM-0000 ✓ passed pass@1 (2.8s)
  [24/30] GSM-SYM-0000 ✓ passed pass@1 (1.8s)
  [25/30] GSM-SYM-0000 ✓ passed pass@1 (1.4s)
  [26/30] GSM-SYM-0000 ✓ passed pass@1 (1.5s)
  [27/30] GSM-SYM-0000 ✓ passed pass@1 (2.2s)
  [28/30] GSM-SYM-0000 ✓ passed pass@1 (2.5s)
  [29/30] GSM-SYM-0000 ✓ passed pass@1 (2.6s)
  [30/30] GSM-SYM-0000 ✓ passed pass@1 (2.4s)
gsm-symbolic-30 (v0.1.0) | pass@1 30 / 30 (100%) | pass@3 30 / 30 (100%) | 2.27s | ok

Pack | Pass@1 | Pass@3 | Flaky | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---
humaneval-plus-30 (v0.1.0) | 24 / 30 (80%) | 28 / 30 (93%) | 4 | 2.33s | 3.51s | ok
lcb-v6-30 (v0.1.0) | 29 / 30 (97%) | 30 / 30 (100%) | 1 | 20.72s | 226.58s | ok
gpqa-diamond (v0.1.0) | 0 / 0 (-) | - | - | - | - | skipped
gsm-symbolic-30 (v0.1.0) | 30 / 30 (100%) | 30 / 30 (100%) | 0 | 2.27s | 2.80s | ok

TOTAL | 83 / 90 (92%) | 88 / 90 (98%) | 5 |  |  |

Inline retry classification (clean pass@1 rows omitted):

Scenario | Label | Attempts | Pass@k credit
---|---|---:|---
humaneval-plus-30/HumanEval-1 | pass@3 | 3 | yes
humaneval-plus-30/HumanEval-3 | fail | 3 | no
humaneval-plus-30/HumanEval-6 | fail | 3 | no
humaneval-plus-30/HumanEval-8 | pass@2 | 2 | yes
humaneval-plus-30/HumanEval-22 | pass@2 | 2 | yes
humaneval-plus-30/HumanEval-28 | pass@2 | 2 | yes
lcb-v6-30/LCBv6-3762 | pass@3 | 3 | yes

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
humaneval-plus-30 | 0 / 39 (0.0%) | code_start=39 | no_fenced_block=39 | message.content=39
lcb-v6-30 | 0 / 32 (0.0%) | code_start=25, empty=2, last_fenced=5 | empty_code=2, no_fenced_block=25, none=5 | message.content=30, message.reasoning=2
gsm-symbolic-30 | 0 / 30 (0.0%) | — | — | message.content=30

Failure breakdown:
- humaneval-plus-30 HumanEval-1: verifier_fail [pass@3] (HumanEval-1: Traceback (most recent call last):
  File "/tmp/tmpdafts9hd.py", line 1, in <module>
    def separate_paren_groups(paren_string: str) -> List[str]:
                                                    ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-3: verifier_fail [fail] (HumanEval-3: Traceback (most recent call last):
  File "/tmp/tmpq3cnzvf6.py", line 1, in <module>
    def below_zero(operations: List[int]) -> bool:
                               ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-6: verifier_fail [fail] (HumanEval-6: Traceback (most recent call last):
  File "/tmp/tmpv5p8mmqn.py", line 1, in <module>
    def parse_nested_parens(paren_string: str) -> List[int]:
                                                  ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-8: verifier_fail [pass@2] (HumanEval-8: Traceback (most recent call last):
  File "/tmp/tmpfqry9jad.py", line 1, in <module>
    def sum_product(numbers: List[int]) -> Tuple[int, int]:
                             ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-22: verifier_fail [pass@2] (HumanEval-22: Traceback (most recent call last):
  File "/tmp/tmpdqttd4kw.py", line 1, in <module>
    def filter_integers(values: List[Any]) -> List[int]:
                                ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-28: verifier_fail [pass@2] (HumanEval-28: Traceback (most recent call last):
  File "/tmp/tmp_w2nrk33.py", line 1, in <module>
    def concatenate(strings: List[str]) -> str:
                             ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- lcb-v6-30 LCBv6-3762: wrong_answer [pass@3] (LCBv6-3762: no runnable-looking Python code extracted)

Warnings:
- GPQA is gated on Hugging Face; authenticate and run the future pack builder to materialize gpqa-diamond scenarios. No GPQA data is committed here.
```

</details>
