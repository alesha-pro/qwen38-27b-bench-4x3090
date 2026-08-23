## Quality bench, thinking on, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
humaneval-plus-30 (v0.1.0) | 28 / 30 | 93% | — | — | 13.89s | 458.85s | ok
lcb-v6-30 (v0.1.0) | 30 / 30 | 100% | — | — | 279.49s | 2288.36s | ok
gpqa-diamond (v0.1.0) | 0 / 0 | - | — | — | - | - | stubbed
gsm-symbolic-30 (v0.1.0) | 30 / 30 | 100% | — | — | 9.18s | 11.58s | ok

TOTAL | 88 / 90 | 98% |  |  |  |  |

Equivalent to: 147/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --reasoning  (endpoint: http://127.0.0.1:19092/v1, model: bench, thinking=on, 2026-08-22T10:26:56.586694Z) ===

  [1/30] HumanEval-0 ✓ passed pass@1 (13.9s)
  [2/30] HumanEval-1 ✓ passed pass@1 (13.9s)
  [3/30] HumanEval-2 ✓ passed pass@1 (458.9s)
  [4/30] HumanEval-3 ✓ passed pass@1 (11.9s)
  [5/30] HumanEval-4 ✗ verifier_fail pass@2 (6.5s)
  [6/30] HumanEval-5 ✓ passed pass@1 (9.7s)
  [7/30] HumanEval-6 ✓ passed pass@1 (13.9s)
  [8/30] HumanEval-7 ✓ passed pass@1 (14.9s)
  [9/30] HumanEval-8 ✓ passed pass@1 (11.8s)
  [10/30] HumanEval-9 ✓ passed pass@1 (28.9s)
  [11/30] HumanEval-10 ✓ passed pass@1 (583.0s)
  [12/30] HumanEval-11 ✓ passed pass@1 (20.8s)
  [13/30] HumanEval-12 ✓ passed pass@1 (10.0s)
  [14/30] HumanEval-13 ✓ passed pass@1 (14.2s)
  [15/30] HumanEval-14 ✗ verifier_fail pass@3 (4.1s)
  [16/30] HumanEval-15 ✓ passed pass@1 (9.4s)
  [17/30] HumanEval-16 ✓ passed pass@1 (10.5s)
  [18/30] HumanEval-17 ✓ passed pass@1 (75.8s)
  [19/30] HumanEval-18 ✓ passed pass@1 (11.0s)
  [20/30] HumanEval-19 ✓ passed pass@1 (14.7s)
  [21/30] HumanEval-20 ✓ passed pass@1 (17.6s)
  [22/30] HumanEval-21 ✓ passed pass@1 (34.3s)
  [23/30] HumanEval-22 ✓ passed pass@1 (30.9s)
  [24/30] HumanEval-23 ✓ passed pass@1 (6.2s)
  [25/30] HumanEval-24 ✓ passed pass@1 (50.1s)
  [26/30] HumanEval-25 ✓ passed pass@1 (21.2s)
  [27/30] HumanEval-26 ✓ passed pass@1 (10.0s)
  [28/30] HumanEval-27 ✓ passed pass@1 (4.0s)
  [29/30] HumanEval-28 ✓ passed pass@1 (8.0s)
  [30/30] HumanEval-29 ✓ passed pass@1 (12.1s)
humaneval-plus-30 (v0.1.0) | pass@1 28 / 30 (93%) | pass@3 30 / 30 (100%) | 13.89s | ok
  [1/30] LCBv6-3702 ✓ passed pass@1 (117.0s)
  [2/30] LCBv6-3634 ✓ passed pass@1 (36.3s)
  [3/30] LCBv6-3715 ✓ passed pass@1 (1153.9s)
  [4/30] LCBv6-3562 ✓ passed pass@1 (2288.4s)
  [5/30] LCBv6-3684 ✓ passed pass@1 (109.7s)
  [6/30] LCBv6-3716 ✓ passed pass@1 (505.0s)
  [7/30] LCBv6-3688 ✓ passed pass@1 (1685.5s)
  [8/30] LCBv6-3708 ✓ passed pass@1 (35.2s)
  [9/30] LCBv6-3677 ✓ passed pass@1 (330.8s)
  [10/30] LCBv6-3720 ✓ passed pass@1 (251.8s)
  [11/30] LCBv6-3674 ✓ passed pass@1 (977.3s)
  [12/30] LCBv6-3731 ✓ passed pass@1 (11.9s)
  [13/30] LCBv6-3714 ✓ passed pass@1 (367.8s)
  [14/30] LCBv6-3737 ✓ passed pass@1 (153.7s)
  [15/30] LCBv6-3725 ✓ passed pass@1 (421.5s)
  [16/30] LCBv6-3704 ✓ passed pass@1 (12.6s)
  [17/30] LCBv6-3721 ✓ passed pass@1 (136.2s)
  [18/30] LCBv6-3751 ✓ passed pass@1 (165.7s)
  [19/30] LCBv6-3753 ✓ passed pass@1 (23.7s)
  [20/30] LCBv6-3754 ✓ passed pass@1 (307.1s)
  [21/30] LCBv6-3697 ✓ passed pass@1 (470.1s)
  [22/30] LCBv6-3748 ✓ passed pass@1 (51.6s)
  [23/30] LCBv6-3760 ✓ passed pass@1 (45.7s)
  [24/30] LCBv6-3696 ✓ passed pass@1 (599.5s)
  [25/30] LCBv6-3762 ✓ passed pass@1 (2879.3s)
  [26/30] LCBv6-3709 ✓ passed pass@1 (24.7s)
  [27/30] LCBv6-3779 ✓ passed pass@1 (1205.8s)
  [28/30] LCBv6-3771 ✓ passed pass@1 (849.5s)
  [29/30] LCBv6-3733 ✓ passed pass@1 (1103.1s)
  [30/30] LCBv6-3768 ✓ passed pass@1 (11.8s)
lcb-v6-30 (v0.1.0) | pass@1 30 / 30 (100%) | pass@3 30 / 30 (100%) | 279.49s | ok
gpqa-diamond (v0.1.0) | 0 / 0 | - | - | stubbed
  [1/30] GSM-SYM-0000-I000 ✓ passed pass@1 (10.3s)
  [2/30] GSM-SYM-0000-I001 ✓ passed pass@1 (7.0s)
  [3/30] GSM-SYM-0000-I002 ✓ passed pass@1 (8.5s)
  [4/30] GSM-SYM-0000-I003 ✓ passed pass@1 (11.0s)
  [5/30] GSM-SYM-0000-I004 ✓ passed pass@1 (10.9s)
  [6/30] GSM-SYM-0000-I005 ✓ passed pass@1 (9.5s)
  [7/30] GSM-SYM-0000-I006 ✓ passed pass@1 (9.6s)
  [8/30] GSM-SYM-0000-I007 ✓ passed pass@1 (11.1s)
  [9/30] GSM-SYM-0000-I008 ✓ passed pass@1 (11.6s)
  [10/30] GSM-SYM-0000-I009 ✓ passed pass@1 (9.1s)
  [11/30] GSM-SYM-0000-I010 ✓ passed pass@1 (7.2s)
  [12/30] GSM-SYM-0000-I011 ✓ passed pass@1 (8.6s)
  [13/30] GSM-SYM-0000-I012 ✓ passed pass@1 (9.2s)
  [14/30] GSM-SYM-0000-I013 ✓ passed pass@1 (10.2s)
  [15/30] GSM-SYM-0000-I014 ✓ passed pass@1 (8.6s)
  [16/30] GSM-SYM-0000-I015 ✓ passed pass@1 (8.7s)
  [17/30] GSM-SYM-0000-I016 ✓ passed pass@1 (6.3s)
  [18/30] GSM-SYM-0000-I017 ✓ passed pass@1 (7.2s)
  [19/30] GSM-SYM-0000-I018 ✓ passed pass@1 (11.6s)
  [20/30] GSM-SYM-0000-I019 ✓ passed pass@1 (9.1s)
  [21/30] GSM-SYM-0000-I020 ✓ passed pass@1 (8.3s)
  [22/30] GSM-SYM-0000-I021 ✓ passed pass@1 (9.5s)
  [23/30] GSM-SYM-0000-I022 ✓ passed pass@1 (14.3s)
  [24/30] GSM-SYM-0000-I023 ✓ passed pass@1 (8.7s)
  [25/30] GSM-SYM-0000-I024 ✓ passed pass@1 (10.1s)
  [26/30] GSM-SYM-0000-I025 ✓ passed pass@1 (7.1s)
  [27/30] GSM-SYM-0000-I026 ✓ passed pass@1 (10.0s)
  [28/30] GSM-SYM-0000-I027 ✓ passed pass@1 (8.1s)
  [29/30] GSM-SYM-0000-I028 ✓ passed pass@1 (10.2s)
  [30/30] GSM-SYM-0000-I029 ✓ passed pass@1 (7.7s)
gsm-symbolic-30 (v0.1.0) | pass@1 30 / 30 (100%) | pass@3 30 / 30 (100%) | 9.18s | ok

Pack | Pass@1 | Pass@3 | Flaky | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---
humaneval-plus-30 (v0.1.0) | 28 / 30 (93%) | 30 / 30 (100%) | 2 | 13.89s | 458.85s | ok
lcb-v6-30 (v0.1.0) | 30 / 30 (100%) | 30 / 30 (100%) | 0 | 279.49s | 2288.36s | ok
gpqa-diamond (v0.1.0) | 0 / 0 (-) | - | - | - | - | stubbed
gsm-symbolic-30 (v0.1.0) | 30 / 30 (100%) | 30 / 30 (100%) | 0 | 9.18s | 11.58s | ok

TOTAL | 88 / 90 (98%) | 90 / 90 (100%) | 2 |  |  |

Inline retry classification (clean pass@1 rows omitted):

Scenario | Label | Attempts | Pass@k credit
---|---|---:|---
humaneval-plus-30/HumanEval-4 | pass@2 | 2 | yes
humaneval-plus-30/HumanEval-14 | pass@3 | 3 | yes

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
humaneval-plus-30 | 0 / 33 (0.0%) | code_start=33 | no_fenced_block=33 | message.content=33
lcb-v6-30 | 0 / 30 (0.0%) | code_start=30 | no_fenced_block=30 | message.content=30
gsm-symbolic-30 | 0 / 30 (0.0%) | — | — | message.content=30

Failure breakdown:
- humaneval-plus-30 HumanEval-4: verifier_fail [pass@2] (HumanEval-4: Traceback (most recent call last):
  File "/tmp/tmpbr0zdpax.py", line 1, in <module>
    def mean_absolute_deviation(numbers: List[float]) -> float:
                                         ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)
- humaneval-plus-30 HumanEval-14: verifier_fail [pass@3] (HumanEval-14: Traceback (most recent call last):
  File "/tmp/tmpbs7nd0x4.py", line 1, in <module>
    def all_prefixes(string: str) -> List[str]:
                                     ^^^^
NameError: name 'List' is not defined. Did you mean: 'list'?
)

Warnings:
- gsm-symbolic-30 IDs repaired from raw_problem.instance; collapsed resume rows reconstructed from lossless proxy telemetry and re-scored with answer_match
```

</details>
