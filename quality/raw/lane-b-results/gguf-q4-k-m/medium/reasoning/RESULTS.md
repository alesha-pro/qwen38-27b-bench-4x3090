## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
humaneval-plus-30 (v0.1.0) | 25 / 30 | 83% | — | — | 11.95s | 20.09s | ok
lcb-v6-30 (v0.1.0) | 27 / 30 | 90% | — | — | 118.10s | 783.17s | ok
gpqa-diamond (v0.1.0) | 0 / 0 | - | — | — | - | - | skipped
gsm-symbolic-30 (v0.1.0) | 30 / 30 | 100% | — | — | 9.01s | 15.74s | ok

TOTAL | 82 / 90 | 91% |  |  |  |  |

Equivalent to: 137/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --reasoning  (endpoint: http://127.0.0.1:19082/v1, model: bench, thinking=on, 2026-08-19T05:02:39.096209Z) ===

  [1/30] HumanEval-0 ✓ passed pass@1 (11.8s)
  [2/30] HumanEval-1 ✓ passed pass@1 (22.9s)
  [3/30] HumanEval-2 ✓ passed pass@1 (8.0s)
  [4/30] HumanEval-3 ✓ passed pass@1 (7.3s)
  [5/30] HumanEval-4 ✓ passed pass@1 (13.0s)
  [6/30] HumanEval-5 ✓ passed pass@1 (10.4s)
  [7/30] HumanEval-6 ✗ verifier_fail fail (12.8s)
  [8/30] HumanEval-7 ✓ passed pass@1 (9.0s)
  [9/30] HumanEval-8 ✓ passed pass@1 (10.0s)
  [10/30] HumanEval-9 ✓ passed pass@1 (15.4s)
  [11/30] HumanEval-10 ✓ passed pass@1 (16.4s)
  [12/30] HumanEval-11 ✓ passed pass@1 (17.5s)
  [13/30] HumanEval-12 ✗ verifier_fail pass@2 (11.1s)
  [14/30] HumanEval-13 ✓ passed pass@1 (5.9s)
  [15/30] HumanEval-14 ✗ verifier_fail pass@2 (5.1s)
  [16/30] HumanEval-15 ✓ passed pass@1 (4.8s)
  [17/30] HumanEval-16 ✓ passed pass@1 (5.4s)
  [18/30] HumanEval-17 ✗ verifier_fail pass@2 (12.1s)
  [19/30] HumanEval-18 ✓ passed pass@1 (15.6s)
  [20/30] HumanEval-19 ✓ passed pass@1 (12.9s)
  [21/30] HumanEval-20 ✓ passed pass@1 (20.1s)
  [22/30] HumanEval-21 ✓ passed pass@1 (15.0s)
  [23/30] HumanEval-22 ✓ passed pass@1 (15.9s)
  [24/30] HumanEval-23 ✓ passed pass@1 (2.6s)
  [25/30] HumanEval-24 ✓ passed pass@1 (18.0s)
  [26/30] HumanEval-25 ✗ timeout fail (16.2s)
  [27/30] HumanEval-26 ✓ passed pass@1 (15.5s)
  [28/30] HumanEval-27 ✓ passed pass@1 (6.2s)
  [29/30] HumanEval-28 ✓ passed pass@1 (3.7s)
  [30/30] HumanEval-29 ✓ passed pass@1 (9.4s)
humaneval-plus-30 (v0.1.0) | pass@1 25 / 30 (83%) | pass@3 28 / 30 (93%) | 11.95s | ok
  [1/30] LCBv6-3702 ✓ passed pass@1 (56.8s)
  [2/30] LCBv6-3634 ✓ passed pass@1 (33.9s)
  [3/30] LCBv6-3715 ✗ verifier_fail pass@2 (207.4s)
  [4/30] LCBv6-3562 ✓ passed pass@1 (340.6s)
  [5/30] LCBv6-3684 ✓ passed pass@1 (68.9s)
  [6/30] LCBv6-3716 ✓ passed pass@1 (185.0s)
  [7/30] LCBv6-3688 ✓ passed pass@1 (686.1s)
  [8/30] LCBv6-3708 ✓ passed pass@1 (34.1s)
  [9/30] LCBv6-3677 ✗ wrong_answer pass@2 (163.9s)
  [10/30] LCBv6-3720 ✓ passed pass@1 (134.1s)
  [11/30] LCBv6-3674 ✓ passed pass@1 (783.2s)
  [12/30] LCBv6-3731 ✓ passed pass@1 (15.9s)
  [13/30] LCBv6-3714 ✓ passed pass@1 (138.4s)
  [14/30] LCBv6-3737 ✓ passed pass@1 (180.3s)
  [15/30] LCBv6-3725 ✓ passed pass@1 (228.2s)
  [16/30] LCBv6-3704 ✓ passed pass@1 (10.7s)
  [17/30] LCBv6-3721 ✓ passed pass@1 (88.6s)
  [18/30] LCBv6-3751 ✓ passed pass@1 (57.0s)
  [19/30] LCBv6-3753 ✓ passed pass@1 (11.6s)
  [20/30] LCBv6-3754 ✓ passed pass@1 (102.1s)
  [21/30] LCBv6-3697 ✓ passed pass@1 (97.6s)
  [22/30] LCBv6-3748 ✓ passed pass@1 (36.9s)
  [23/30] LCBv6-3760 ✓ passed pass@1 (39.2s)
  [24/30] LCBv6-3696 ✓ passed pass@1 (483.0s)
  [25/30] LCBv6-3762 ✓ passed pass@1 (959.7s)
  [26/30] LCBv6-3709 ✓ passed pass@1 (15.1s)
  [27/30] LCBv6-3779 ✓ passed pass@1 (157.9s)
  [28/30] LCBv6-3771 ✓ passed pass@1 (600.3s)
  [29/30] LCBv6-3733 ✗ wrong_answer fail (662.2s)
  [30/30] LCBv6-3768 ✓ passed pass@1 (13.1s)
lcb-v6-30 (v0.1.0) | pass@1 27 / 30 (90%) | pass@3 29 / 30 (97%) | 118.10s | ok
gpqa-diamond (v0.1.0) | 0 / 0 | - | - | skipped
  [1/30] GSM-SYM-0000 ✓ passed pass@1 (10.9s)
  [2/30] GSM-SYM-0000 ✓ passed pass@1 (8.4s)
  [3/30] GSM-SYM-0000 ✓ passed pass@1 (15.8s)
  [4/30] GSM-SYM-0000 ✓ passed pass@1 (12.9s)
  [5/30] GSM-SYM-0000 ✓ passed pass@1 (13.2s)
  [6/30] GSM-SYM-0000 ✓ passed pass@1 (14.4s)
  [7/30] GSM-SYM-0000 ✓ passed pass@1 (9.2s)
  [8/30] GSM-SYM-0000 ✓ passed pass@1 (11.0s)
  [9/30] GSM-SYM-0000 ✓ passed pass@1 (9.7s)
  [10/30] GSM-SYM-0000 ✓ passed pass@1 (9.1s)
  [11/30] GSM-SYM-0000 ✓ passed pass@1 (11.7s)
  [12/30] GSM-SYM-0000 ✓ passed pass@1 (8.1s)
  [13/30] GSM-SYM-0000 ✓ passed pass@1 (14.2s)
  [14/30] GSM-SYM-0000 ✓ passed pass@1 (15.7s)
  [15/30] GSM-SYM-0000 ✓ passed pass@1 (9.6s)
  [16/30] GSM-SYM-0000 ✓ passed pass@1 (10.1s)
  [17/30] GSM-SYM-0000 ✓ passed pass@1 (8.1s)
  [18/30] GSM-SYM-0000 ✓ passed pass@1 (8.6s)
  [19/30] GSM-SYM-0000 ✓ passed pass@1 (8.7s)
  [20/30] GSM-SYM-0000 ✓ passed pass@1 (8.6s)
  [21/30] GSM-SYM-0000 ✓ passed pass@1 (8.1s)
  [22/30] GSM-SYM-0000 ✓ passed pass@1 (8.9s)
  [23/30] GSM-SYM-0000 ✓ passed pass@1 (8.1s)
  [24/30] GSM-SYM-0000 ✓ passed pass@1 (7.9s)
  [25/30] GSM-SYM-0000 ✓ passed pass@1 (8.9s)
  [26/30] GSM-SYM-0000 ✓ passed pass@1 (8.7s)
  [27/30] GSM-SYM-0000 ✓ passed pass@1 (7.6s)
  [28/30] GSM-SYM-0000 ✓ passed pass@1 (8.3s)
  [29/30] GSM-SYM-0000 ✓ passed pass@1 (7.7s)
  [30/30] GSM-SYM-0000 ✓ passed pass@1 (10.2s)
gsm-symbolic-30 (v0.1.0) | pass@1 30 / 30 (100%) | pass@3 30 / 30 (100%) | 9.01s | ok

Pack | Pass@1 | Pass@3 | Flaky | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---
humaneval-plus-30 (v0.1.0) | 25 / 30 (83%) | 28 / 30 (93%) | 3 | 11.95s | 20.09s | ok
lcb-v6-30 (v0.1.0) | 27 / 30 (90%) | 29 / 30 (97%) | 2 | 118.10s | 783.17s | ok
gpqa-diamond (v0.1.0) | 0 / 0 (-) | - | - | - | - | skipped
gsm-symbolic-30 (v0.1.0) | 30 / 30 (100%) | 30 / 30 (100%) | 0 | 9.01s | 15.74s | ok

TOTAL | 82 / 90 (91%) | 87 / 90 (97%) | 5 |  |  |

Inline retry classification (clean pass@1 rows omitted):

Scenario | Label | Attempts | Pass@k credit
---|---|---:|---
humaneval-plus-30/HumanEval-6 | fail | 3 | no
humaneval-plus-30/HumanEval-12 | pass@2 | 2 | yes
humaneval-plus-30/HumanEval-14 | pass@2 | 2 | yes
humaneval-plus-30/HumanEval-17 | pass@2 | 2 | yes
humaneval-plus-30/HumanEval-25 | fail | 1 | no
lcb-v6-30/LCBv6-3715 | pass@2 | 2 | yes
lcb-v6-30/LCBv6-3677 | pass@2 | 2 | yes
lcb-v6-30/LCBv6-3733 | fail | 3 | no

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
humaneval-plus-30 | 0 / 35 (0.0%) | code_start=34, last_fenced=1 | no_fenced_block=34, none=1 | message.content=35
lcb-v6-30 | 0 / 34 (0.0%) | code_start=32, last_fenced=2 | no_fenced_block=32, none=2 | message.content=34
gsm-symbolic-30 | 0 / 30 (0.0%) | — | — | message.content=30

Failure breakdown:
- humaneval-plus-30 HumanEval-6: verifier_fail [fail] (HumanEval-6: Traceback (most recent call last):
  File "/tmp/tmptzo_4uxy.py", line 1, in <module>
    def parse_nested_parens(paren_string: str) -> List[int]:
                                                  ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-12: verifier_fail [pass@2] (HumanEval-12: Traceback (most recent call last):
  File "/tmp/tmpcebgey4e.py", line 1, in <module>
    def longest(strings: List[str]) -> Optional[str]:
                         ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-14: verifier_fail [pass@2] (HumanEval-14: Traceback (most recent call last):
  File "/tmp/tmpbxp3_e5n.py", line 1, in <module>
    def all_prefixes(string: str) -> List[str]:
                                     ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-17: verifier_fail [pass@2] (HumanEval-17: Traceback (most recent call last):
  File "/tmp/tmp4us4i1fm.py", line 1, in <module>
    def parse_music(music_string: str) -> List[int]:
                                          ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-25: timeout [fail] (HumanEval-25: TIMEOUT)
- lcb-v6-30 LCBv6-3715: verifier_fail [pass@2] (LCBv6-3715: Traceback (most recent call last):
  File "/tmp/tmptn_2u79i.py", line 90, in <module>
    _run()
  File "/tmp/tmptn_2u79i.py", line 87, in _run
    got = fn(*args)
          ^^^^^^^^^
  File "/tmp/tmptn_2u79i.py", line 57, in maximumCoins
    val = compute_f(x)
          ^^^^^^^^^^^^
  File "/tmp/tmptn_2u79i.py", line 26, in compute_f
    left_idx = bisect_left(r_arr, x)
               ^^^^^^^^^^^
NameError: name 'bisect_left' is not defined
)
- lcb-v6-30 LCBv6-3677: wrong_answer [pass@2] (LCBv6-3677: Traceback (most recent call last):
  File "/tmp/tmp0rhovsrl.py", line 72, in <module>
    _run()
  File "/tmp/tmp0rhovsrl.py", line 71, in _run
    raise AssertionError(f"test {i}: expected {expected!r}, got {got!r}")
AssertionError: test 0: expected 8, got 7
)
- lcb-v6-30 LCBv6-3733: wrong_answer [fail] (LCBv6-3733: Traceback (most recent call last):
  File "/tmp/tmp6uddud1g.py", line 145, in <module>
    _run()
  File "/tmp/tmp6uddud1g.py", line 144, in _run
    raise AssertionError(f"test {i}: expected {expected!r}, got {got!r}")
AssertionError: test 0: expected 5, got 3
)

Warnings:
- GPQA is gated on Hugging Face; authenticate and run the future pack builder to materialize gpqa-diamond scenarios. No GPQA data is committed here.
```

</details>
