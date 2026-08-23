## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
humaneval-plus-30 (v0.1.0) | 27 / 30 | 90% | — | — | 1.53s | 3.54s | ok
lcb-v6-30 (v0.1.0) | 28 / 30 | 93% | — | — | 18.48s | 213.42s | ok
gpqa-diamond (v0.1.0) | 0 / 0 | - | — | — | - | - | skipped
gsm-symbolic-30 (v0.1.0) | 30 / 30 | 100% | — | — | 1.47s | 1.79s | ok

TOTAL | 85 / 90 | 94% |  |  |  |  |

Equivalent to: 142/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --reasoning  (endpoint: http://127.0.0.1:19092/v1, model: bench, thinking=on, 2026-08-20T21:42:28.589031Z) ===

  [1/30] HumanEval-0 ✓ passed pass@1 (1.4s)
  [2/30] HumanEval-1 ✗ verifier_fail pass@3 (2.5s)
  [3/30] HumanEval-2 ✓ passed pass@1 (1.8s)
  [4/30] HumanEval-3 ✗ verifier_fail pass@3 (1.2s)
  [5/30] HumanEval-4 ✓ passed pass@1 (1.8s)
  [6/30] HumanEval-5 ✓ passed pass@1 (1.6s)
  [7/30] HumanEval-6 ✓ passed pass@1 (2.8s)
  [8/30] HumanEval-7 ✓ passed pass@1 (0.8s)
  [9/30] HumanEval-8 ✓ passed pass@1 (1.3s)
  [10/30] HumanEval-9 ✓ passed pass@1 (1.6s)
  [11/30] HumanEval-10 ✓ passed pass@1 (4.5s)
  [12/30] HumanEval-11 ✓ passed pass@1 (1.8s)
  [13/30] HumanEval-12 ✓ passed pass@1 (1.5s)
  [14/30] HumanEval-13 ✓ passed pass@1 (1.0s)
  [15/30] HumanEval-14 ✓ passed pass@1 (1.2s)
  [16/30] HumanEval-15 ✓ passed pass@1 (1.1s)
  [17/30] HumanEval-16 ✓ passed pass@1 (1.0s)
  [18/30] HumanEval-17 ✗ verifier_fail fail (2.3s)
  [19/30] HumanEval-18 ✓ passed pass@1 (2.0s)
  [20/30] HumanEval-19 ✓ passed pass@1 (2.2s)
  [21/30] HumanEval-20 ✓ passed pass@1 (3.5s)
  [22/30] HumanEval-21 ✓ passed pass@1 (1.2s)
  [23/30] HumanEval-22 ✓ passed pass@1 (1.8s)
  [24/30] HumanEval-23 ✓ passed pass@1 (0.5s)
  [25/30] HumanEval-24 ✓ passed pass@1 (2.3s)
  [26/30] HumanEval-25 ✓ passed pass@1 (3.1s)
  [27/30] HumanEval-26 ✓ passed pass@1 (1.2s)
  [28/30] HumanEval-27 ✓ passed pass@1 (0.8s)
  [29/30] HumanEval-28 ✓ passed pass@1 (0.8s)
  [30/30] HumanEval-29 ✓ passed pass@1 (0.8s)
humaneval-plus-30 (v0.1.0) | pass@1 27 / 30 (90%) | pass@3 29 / 30 (97%) | 1.53s | ok
  [1/30] LCBv6-3702 ✓ passed pass@1 (5.9s)
  [2/30] LCBv6-3634 ✓ passed pass@1 (5.3s)
  [3/30] LCBv6-3715 ✓ passed pass@1 (128.3s)
  [4/30] LCBv6-3562 ✓ passed pass@1 (176.0s)
  [5/30] LCBv6-3684 ✓ passed pass@1 (9.5s)
  [6/30] LCBv6-3716 ✓ passed pass@1 (83.1s)
  [7/30] LCBv6-3688 ✓ passed pass@1 (87.6s)
  [8/30] LCBv6-3708 ✓ passed pass@1 (3.2s)
  [9/30] LCBv6-3677 ✗ wrong_answer pass@2 (18.7s)
  [10/30] LCBv6-3720 ✓ passed pass@1 (61.9s)
  [11/30] LCBv6-3674 ✓ passed pass@1 (125.0s)
  [12/30] LCBv6-3731 ✓ passed pass@1 (2.3s)
  [13/30] LCBv6-3714 ✓ passed pass@1 (29.7s)
  [14/30] LCBv6-3737 ✓ passed pass@1 (14.0s)
  [15/30] LCBv6-3725 ✓ passed pass@1 (26.9s)
  [16/30] LCBv6-3704 ✓ passed pass@1 (2.2s)
  [17/30] LCBv6-3721 ✓ passed pass@1 (9.2s)
  [18/30] LCBv6-3751 ✓ passed pass@1 (14.1s)
  [19/30] LCBv6-3753 ✓ passed pass@1 (1.9s)
  [20/30] LCBv6-3754 ✓ passed pass@1 (42.0s)
  [21/30] LCBv6-3697 ✓ passed pass@1 (18.3s)
  [22/30] LCBv6-3748 ✓ passed pass@1 (9.6s)
  [23/30] LCBv6-3760 ✓ passed pass@1 (8.6s)
  [24/30] LCBv6-3696 ✓ passed pass@1 (122.8s)
  [25/30] LCBv6-3762 ✓ passed pass@1 (284.8s)
  [26/30] LCBv6-3709 ✓ passed pass@1 (4.2s)
  [27/30] LCBv6-3779 ✓ passed pass@1 (36.6s)
  [28/30] LCBv6-3771 ✗ verifier_fail pass@2 (213.4s)
  [29/30] LCBv6-3733 ✓ passed pass@1 (67.5s)
  [30/30] LCBv6-3768 ✓ passed pass@1 (1.0s)
lcb-v6-30 (v0.1.0) | pass@1 28 / 30 (93%) | pass@3 30 / 30 (100%) | 18.48s | ok
gpqa-diamond (v0.1.0) | 0 / 0 | - | - | skipped
  [1/30] GSM-SYM-0000 ✓ passed pass@1 (1.5s)
  [2/30] GSM-SYM-0000 ✓ passed pass@1 (1.0s)
  [3/30] GSM-SYM-0000 ✓ passed pass@1 (1.4s)
  [4/30] GSM-SYM-0000 ✓ passed pass@1 (1.8s)
  [5/30] GSM-SYM-0000 ✓ passed pass@1 (1.7s)
  [6/30] GSM-SYM-0000 ✓ passed pass@1 (1.5s)
  [7/30] GSM-SYM-0000 ✓ passed pass@1 (1.4s)
  [8/30] GSM-SYM-0000 ✓ passed pass@1 (1.6s)
  [9/30] GSM-SYM-0000 ✓ passed pass@1 (1.5s)
  [10/30] GSM-SYM-0000 ✓ passed pass@1 (1.4s)
  [11/30] GSM-SYM-0000 ✓ passed pass@1 (1.5s)
  [12/30] GSM-SYM-0000 ✓ passed pass@1 (1.4s)
  [13/30] GSM-SYM-0000 ✓ passed pass@1 (1.9s)
  [14/30] GSM-SYM-0000 ✓ passed pass@1 (1.8s)
  [15/30] GSM-SYM-0000 ✓ passed pass@1 (1.5s)
  [16/30] GSM-SYM-0000 ✓ passed pass@1 (1.7s)
  [17/30] GSM-SYM-0000 ✓ passed pass@1 (1.3s)
  [18/30] GSM-SYM-0000 ✓ passed pass@1 (1.1s)
  [19/30] GSM-SYM-0000 ✓ passed pass@1 (1.4s)
  [20/30] GSM-SYM-0000 ✓ passed pass@1 (1.4s)
  [21/30] GSM-SYM-0000 ✓ passed pass@1 (1.5s)
  [22/30] GSM-SYM-0000 ✓ passed pass@1 (1.4s)
  [23/30] GSM-SYM-0000 ✓ passed pass@1 (1.5s)
  [24/30] GSM-SYM-0000 ✓ passed pass@1 (1.3s)
  [25/30] GSM-SYM-0000 ✓ passed pass@1 (1.5s)
  [26/30] GSM-SYM-0000 ✓ passed pass@1 (1.3s)
  [27/30] GSM-SYM-0000 ✓ passed pass@1 (1.7s)
  [28/30] GSM-SYM-0000 ✓ passed pass@1 (1.4s)
  [29/30] GSM-SYM-0000 ✓ passed pass@1 (1.6s)
  [30/30] GSM-SYM-0000 ✓ passed pass@1 (1.7s)
gsm-symbolic-30 (v0.1.0) | pass@1 30 / 30 (100%) | pass@3 30 / 30 (100%) | 1.47s | ok

Pack | Pass@1 | Pass@3 | Flaky | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---
humaneval-plus-30 (v0.1.0) | 27 / 30 (90%) | 29 / 30 (97%) | 2 | 1.53s | 3.54s | ok
lcb-v6-30 (v0.1.0) | 28 / 30 (93%) | 30 / 30 (100%) | 2 | 18.48s | 213.42s | ok
gpqa-diamond (v0.1.0) | 0 / 0 (-) | - | - | - | - | skipped
gsm-symbolic-30 (v0.1.0) | 30 / 30 (100%) | 30 / 30 (100%) | 0 | 1.47s | 1.79s | ok

TOTAL | 85 / 90 (94%) | 89 / 90 (99%) | 4 |  |  |

Inline retry classification (clean pass@1 rows omitted):

Scenario | Label | Attempts | Pass@k credit
---|---|---:|---
humaneval-plus-30/HumanEval-1 | pass@3 | 3 | yes
humaneval-plus-30/HumanEval-3 | pass@3 | 3 | yes
humaneval-plus-30/HumanEval-17 | fail | 3 | no
lcb-v6-30/LCBv6-3677 | pass@2 | 2 | yes
lcb-v6-30/LCBv6-3771 | pass@2 | 2 | yes

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
humaneval-plus-30 | 0 / 36 (0.0%) | code_start=19, last_fenced=17 | no_fenced_block=19, none=17 | message.content=36
lcb-v6-30 | 0 / 32 (0.0%) | code_start=2, last_fenced=30 | no_fenced_block=2, none=30 | message.content=29, message.reasoning=3
gsm-symbolic-30 | 0 / 30 (0.0%) | — | — | message.content=30

Failure breakdown:
- humaneval-plus-30 HumanEval-1: verifier_fail [pass@3] (HumanEval-1: Traceback (most recent call last):
  File "/tmp/tmptxpv4hz3.py", line 1, in <module>
    def separate_paren_groups(paren_string: str) -> List[str]:
                                                    ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-3: verifier_fail [pass@3] (HumanEval-3: Traceback (most recent call last):
  File "/tmp/tmpmetvag0j.py", line 1, in <module>
    def below_zero(operations: List[int]) -> bool:
                               ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-17: verifier_fail [fail] (HumanEval-17: Traceback (most recent call last):
  File "/tmp/tmpsio9463n.py", line 1, in <module>
    def parse_music(music_string: str) -> List[int]:
                                          ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- lcb-v6-30 LCBv6-3677: wrong_answer [pass@2] (LCBv6-3677: Traceback (most recent call last):
  File "/tmp/tmp1dqkmmk1.py", line 80, in <module>
    _run()
  File "/tmp/tmp1dqkmmk1.py", line 79, in _run
    raise AssertionError(f"test {i}: expected {expected!r}, got {got!r}")
AssertionError: test 0: expected 8, got 7
)
- lcb-v6-30 LCBv6-3771: verifier_fail [pass@2] (LCBv6-3771: Traceback (most recent call last):
  File "/tmp/tmpc3r6wf0y.py", line 2, in <module>
    end = i
          ^
NameError: name 'i' is not defined. Did you mean: 'id'?
)

Warnings:
- GPQA is gated on Hugging Face; authenticate and run the future pack builder to materialize gpqa-diamond scenarios. No GPQA data is committed here.
```

</details>
