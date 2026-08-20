## Quality bench, thinking off, benchlocal-cli v0.9.8, repeat = 1

Pack | Pass / Total | Score | Std | CV | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---:|---
humaneval-plus-30 (v0.1.0) | 30 / 30 | 100% | — | — | 4.08s | 8.09s | ok
lcb-v6-30 (v0.1.0) | 24 / 30 | 80% | — | — | 39.62s | 311.56s | ok
gpqa-diamond (v0.1.0) | 0 / 0 | - | — | — | - | - | skipped
gsm-symbolic-30 (v0.1.0) | 30 / 30 | 100% | — | — | 13.27s | 17.25s | ok

TOTAL | 84 / 90 | 93% |  |  |  |  |

Equivalent to: 140/150

<details>
<summary>Raw data</summary>

```
=== benchlocal-cli --reasoning  (endpoint: http://127.0.0.1:19082/v1, model: bench, thinking=off, 2026-08-18T21:41:19.866676Z) ===

  [1/30] HumanEval-0 ✓ passed pass@1 (5.0s)
  [2/30] HumanEval-1 ✓ passed pass@1 (6.1s)
  [3/30] HumanEval-2 ✓ passed pass@1 (2.9s)
  [4/30] HumanEval-3 ✓ passed pass@1 (4.4s)
  [5/30] HumanEval-4 ✓ passed pass@1 (4.9s)
  [6/30] HumanEval-5 ✓ passed pass@1 (4.3s)
  [7/30] HumanEval-6 ✓ passed pass@1 (5.8s)
  [8/30] HumanEval-7 ✓ passed pass@1 (3.3s)
  [9/30] HumanEval-8 ✓ passed pass@1 (4.4s)
  [10/30] HumanEval-9 ✓ passed pass@1 (4.7s)
  [11/30] HumanEval-10 ✓ passed pass@1 (8.1s)
  [12/30] HumanEval-11 ✓ passed pass@1 (3.9s)
  [13/30] HumanEval-12 ✓ passed pass@1 (3.6s)
  [14/30] HumanEval-13 ✓ passed pass@1 (3.1s)
  [15/30] HumanEval-14 ✓ passed pass@1 (2.5s)
  [16/30] HumanEval-15 ✓ passed pass@1 (2.7s)
  [17/30] HumanEval-16 ✓ passed pass@1 (2.6s)
  [18/30] HumanEval-17 ✓ passed pass@1 (7.2s)
  [19/30] HumanEval-18 ✓ passed pass@1 (4.4s)
  [20/30] HumanEval-19 ✓ passed pass@1 (6.6s)
  [21/30] HumanEval-20 ✓ passed pass@1 (8.5s)
  [22/30] HumanEval-21 ✓ passed pass@1 (5.2s)
  [23/30] HumanEval-22 ✓ passed pass@1 (3.5s)
  [24/30] HumanEval-23 ✓ passed pass@1 (1.9s)
  [25/30] HumanEval-24 ✓ passed pass@1 (2.9s)
  [26/30] HumanEval-25 ✓ passed pass@1 (5.8s)
  [27/30] HumanEval-26 ✓ passed pass@1 (3.4s)
  [28/30] HumanEval-27 ✓ passed pass@1 (2.0s)
  [29/30] HumanEval-28 ✓ passed pass@1 (2.2s)
  [30/30] HumanEval-29 ✓ passed pass@1 (3.1s)
humaneval-plus-30 (v0.1.0) | pass@1 30 / 30 (100%) | pass@3 30 / 30 (100%) | 4.08s | ok
  [1/30] LCBv6-3702 ✓ passed pass@1 (5.5s)
  [2/30] LCBv6-3634 ✓ passed pass@1 (25.5s)
  [3/30] LCBv6-3715 ✓ passed pass@1 (127.6s)
  [4/30] LCBv6-3562 ✗ wrong_answer fail (240.1s)
  [5/30] LCBv6-3684 ✓ passed pass@1 (9.0s)
  [6/30] LCBv6-3716 ✓ passed pass@1 (11.0s)
  [7/30] LCBv6-3688 ✓ passed pass@1 (46.7s)
  [8/30] LCBv6-3708 ✓ passed pass@1 (6.2s)
  [9/30] LCBv6-3677 ✓ passed pass@1 (32.5s)
  [10/30] LCBv6-3720 ✓ passed pass@1 (151.1s)
  [11/30] LCBv6-3674 ✓ passed pass@1 (141.1s)
  [12/30] LCBv6-3731 ✓ passed pass@1 (2.7s)
  [13/30] LCBv6-3714 ✓ passed pass@1 (32.2s)
  [14/30] LCBv6-3737 ✓ passed pass@1 (49.3s)
  [15/30] LCBv6-3725 ✗ wrong_answer fail (77.5s)
  [16/30] LCBv6-3704 ✓ passed pass@1 (3.2s)
  [17/30] LCBv6-3721 ✓ passed pass@1 (11.3s)
  [18/30] LCBv6-3751 ✓ passed pass@1 (77.3s)
  [19/30] LCBv6-3753 ✓ passed pass@1 (3.6s)
  [20/30] LCBv6-3754 ✓ passed pass@1 (149.8s)
  [21/30] LCBv6-3697 ✗ verifier_fail fail (66.0s)
  [22/30] LCBv6-3748 ✓ passed pass@1 (21.1s)
  [23/30] LCBv6-3760 ✓ passed pass@1 (16.4s)
  [24/30] LCBv6-3696 ✓ passed pass@1 (311.6s)
  [25/30] LCBv6-3762 ✗ verifier_fail fail (257.3s)
  [26/30] LCBv6-3709 ✓ passed pass@1 (9.7s)
  [27/30] LCBv6-3779 ✓ passed pass@1 (104.8s)
  [28/30] LCBv6-3771 ✗ token_limit fail (409.1s)
  [29/30] LCBv6-3733 ✗ wrong_answer fail (127.8s)
  [30/30] LCBv6-3768 ✓ passed pass@1 (3.1s)
lcb-v6-30 (v0.1.0) | pass@1 24 / 30 (80%) | pass@3 24 / 30 (80%) | 39.62s | ok
gpqa-diamond (v0.1.0) | 0 / 0 | - | - | skipped
  [1/30] GSM-SYM-0000 ✓ passed pass@1 (15.1s)
  [2/30] GSM-SYM-0000 ✓ passed pass@1 (13.0s)
  [3/30] GSM-SYM-0000 ✓ passed pass@1 (13.5s)
  [4/30] GSM-SYM-0000 ✓ passed pass@1 (14.0s)
  [5/30] GSM-SYM-0000 ✓ passed pass@1 (15.1s)
  [6/30] GSM-SYM-0000 ✓ passed pass@1 (14.6s)
  [7/30] GSM-SYM-0000 ✓ passed pass@1 (11.1s)
  [8/30] GSM-SYM-0000 ✓ passed pass@1 (17.2s)
  [9/30] GSM-SYM-0000 ✓ passed pass@1 (12.6s)
  [10/30] GSM-SYM-0000 ✓ passed pass@1 (16.6s)
  [11/30] GSM-SYM-0000 ✓ passed pass@1 (12.8s)
  [12/30] GSM-SYM-0000 ✓ passed pass@1 (18.8s)
  [13/30] GSM-SYM-0000 ✓ passed pass@1 (11.1s)
  [14/30] GSM-SYM-0000 ✓ passed pass@1 (14.0s)
  [15/30] GSM-SYM-0000 ✓ passed pass@1 (13.7s)
  [16/30] GSM-SYM-0000 ✓ passed pass@1 (17.2s)
  [17/30] GSM-SYM-0000 ✓ passed pass@1 (10.2s)
  [18/30] GSM-SYM-0000 ✓ passed pass@1 (11.2s)
  [19/30] GSM-SYM-0000 ✓ passed pass@1 (12.4s)
  [20/30] GSM-SYM-0000 ✓ passed pass@1 (13.3s)
  [21/30] GSM-SYM-0000 ✓ passed pass@1 (12.5s)
  [22/30] GSM-SYM-0000 ✓ passed pass@1 (11.2s)
  [23/30] GSM-SYM-0000 ✓ passed pass@1 (12.9s)
  [24/30] GSM-SYM-0000 ✓ passed pass@1 (14.5s)
  [25/30] GSM-SYM-0000 ✓ passed pass@1 (11.2s)
  [26/30] GSM-SYM-0000 ✓ passed pass@1 (10.5s)
  [27/30] GSM-SYM-0000 ✓ passed pass@1 (14.0s)
  [28/30] GSM-SYM-0000 ✓ passed pass@1 (13.3s)
  [29/30] GSM-SYM-0000 ✓ passed pass@1 (14.8s)
  [30/30] GSM-SYM-0000 ✓ passed pass@1 (11.4s)
gsm-symbolic-30 (v0.1.0) | pass@1 30 / 30 (100%) | pass@3 30 / 30 (100%) | 13.27s | ok

Pack | Pass@1 | Pass@3 | Flaky | p50 latency | p95 latency | Status
---|---:|---:|---:|---:|---:|---
humaneval-plus-30 (v0.1.0) | 30 / 30 (100%) | 30 / 30 (100%) | 0 | 4.08s | 8.09s | ok
lcb-v6-30 (v0.1.0) | 24 / 30 (80%) | 24 / 30 (80%) | 0 | 39.62s | 311.56s | ok
gpqa-diamond (v0.1.0) | 0 / 0 (-) | - | - | - | - | skipped
gsm-symbolic-30 (v0.1.0) | 30 / 30 (100%) | 30 / 30 (100%) | 0 | 13.27s | 17.25s | ok

TOTAL | 84 / 90 (93%) | 84 / 90 (93%) | 0 |  |  |

Inline retry classification (clean pass@1 rows omitted):

Scenario | Label | Attempts | Pass@k credit
---|---|---:|---
lcb-v6-30/LCBv6-3562 | fail | 3 | no
lcb-v6-30/LCBv6-3725 | fail | 3 | no
lcb-v6-30/LCBv6-3697 | fail | 3 | no
lcb-v6-30/LCBv6-3762 | fail | 3 | no
lcb-v6-30/LCBv6-3771 | fail | 1 | no
lcb-v6-30/LCBv6-3733 | fail | 3 | no

Completion and extraction diagnostics:

Pack | finish_reason=length | extraction_method | extraction_issue | response_field_used
---|---:|---|---|---
humaneval-plus-30 | 0 / 30 (0.0%) | last_fenced=30 | none=30 | message.content=30
lcb-v6-30 | 1 / 40 (2.5%) | last_fenced=32, opening_fence=8 | none=32, unterminated_fence=8 | message.content=40
gsm-symbolic-30 | 0 / 30 (0.0%) | — | — | message.content=30

Failure breakdown:
- lcb-v6-30 LCBv6-3562: wrong_answer [fail] (LCBv6-3562: Traceback (most recent call last):
  File "/tmp/tmpole8382b.py", line 502, in <module>
    _run()
  File "/tmp/tmpole8382b.py", line 501, in _run
    raise AssertionError(f"test {i}: expected {expected!r}, got {got!r}")
AssertionError: test 1: expected [1, 3, 5, 6], got [6]
)
- lcb-v6-30 LCBv6-3725: wrong_answer [fail] (LCBv6-3725: Traceback (most recent call last):
  File "/tmp/tmpncgz4msc.py", line 243, in <module>
    _run()
  File "/tmp/tmpncgz4msc.py", line 242, in _run
    raise AssertionError(f"test {i}: expected {expected!r}, got {got!r}")
AssertionError: test 0: expected 20, got 23
)
- lcb-v6-30 LCBv6-3697: verifier_fail [fail] (LCBv6-3697: Traceback (most recent call last):
  File "/tmp/tmpqvatle4j.py", line 185, in <module>
    _run()
  File "/tmp/tmpqvatle4j.py", line 182, in _run
    got = fn(*args)
          ^^^^^^^^^
  File "/tmp/tmpqvatle4j.py", line 120, in minimumIncrements
    g = math.gcd(a, b)
        ^^^^
NameError: name 'math' is not defined. Did you mean: 'Match'? Or did you forget to import 'math'?
)
- lcb-v6-30 LCBv6-3762: verifier_fail [fail] (LCBv6-3762:   File "/tmp/tmpe5l0ghb3.py", line 616
    import json as _json
IndentationError: expected an indented block after function definition on line 9
)
- lcb-v6-30 LCBv6-3771: token_limit [fail] (output truncated at token limit (finish_reason=length); underlying verdict was wrong_answer: LCBv6-3771: Traceback (most recent call last):
  File "/tmp/tmpi4r3s0v5.py", line 982, in <module>
    _run()
  File "/tmp/tmpi4r3s0v5.py", line 981, in _run
    raise AssertionError(f"test {i}: expected {expected!r}, got {got!r}")
AssertionError: test 0: expected True, got None
)
- lcb-v6-30 LCBv6-3733: wrong_answer [fail] (LCBv6-3733: Traceback (most recent call last):
  File "/tmp/tmp3af3mz8q.py", line 342, in <module>
    _run()
  File "/tmp/tmp3af3mz8q.py", line 341, in _run
    raise AssertionError(f"test {i}: expected {expected!r}, got {got!r}")
AssertionError: test 0: expected 5, got 4
)

Warnings:
- GPQA is gated on Hugging Face; authenticate and run the future pack builder to materialize gpqa-diamond scenarios. No GPQA data is committed here.
```

</details>
