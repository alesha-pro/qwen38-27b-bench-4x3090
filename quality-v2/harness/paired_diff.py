#!/usr/bin/env python3
"""Paired pass-rate difference between a quant arm and the BF16 reference.

Pre-registered 2026-08-24, BEFORE the 200-task extension finished running.

Why not the old retention.py: that one used "tasks the reference passed 3 of 3"
as the denominator. Selecting the denominator on the reference outcome makes a
gain impossible by construction, so the arm can only ever look worse, and the
matching null is unstable (a p-value anywhere between 0.04 and 0.77 depending
on how per-task pass probabilities are smoothed). Both problems are gone here:
nothing is selected on any arm's outcome.

ESTIMAND (primary): mean over tasks of (quant pass rate - reference pass rate),
each rate over its own repeats at xhigh. One number, in points of accuracy, on
this frozen suite.

INFERENCE: paired bootstrap over tasks for the interval, sign-flip permutation
for the p-value. Both are assumption-free about how a task behaves; the pairing
is the only structure used.

Tie handling, measured 24.08 and worth stating: per-task rates are multiples of
1/3, so on the first 100 tasks 13.9% of permutations land EXACTLY on the
observed statistic. Whether those count decides p between 0.21 and 0.36, and
comparing raw floats catches an arbitrary subset of them. This uses the
conservative convention, ties count as evidence against the effect, with an
explicit tolerance rather than float equality, and the standard (h+1)/(B+1)
estimator. The tie share is printed so the reader can see how much of the
p-value rests on that convention.

PROVIDER ERRORS ARE MISSING DATA, NOT FAILURES (added 2026-08-24, after
seeing the reference traces and BEFORE any quant arm finished). The paid API
returned finish_reason "error" with an empty answer on 8 of its 900 xhigh
generations; the same tasks completed on the reference's own other repeats
(one errored at 43,763 tokens and finished at 91,217 on another pass) and
completed on the local arms (one of them at 117,072 tokens). A local engine
cannot fail this way at all, so counting these as wrong answers depresses only
the reference and hands every quant a free ~0.9 pp head start against a ~2.3 pp
effect. Such responses are dropped from the task's rate; a task with no valid
repeat in either arm leaves the analysis. The rule is symmetric and applies to
any arm. Note the direction: it RAISES the reference and therefore makes every
quant look worse, so it is not a correction chosen to flatter the result.

finish_reason "length" is NOT excluded. Every arm gets the identical 131,072
token budget, so exhausting it without answering is the model failing, not the
provider. One FP8 generation did exactly that and counts as a failure.

ALSO REPORTED, explicitly secondary:
  - the same difference per block,
  - the same difference restricted to tasks at least one arm ever solved. Floor
    tasks contribute exactly zero, so this only rescales the effect and its
    interval; the p-value is identical by construction,
  - a plain count of tasks that moved, as description only.
"""
import argparse, collections, json, random
from pathlib import Path

ROOT = Path("$RUN_ROOT/quant-bench-v2")
B = 20000


ERRORS_AS_FAILURES = False


def provider_error(run, effort, rep, task_id):
    if ERRORS_AS_FAILURES:
        return False
    """True if this generation died on the provider side and carries no
    information about the model. Driver-level errors count too."""
    f = ROOT / "runs" / run / effort / rep / f"{task_id}.json"
    if not f.exists():
        return False
    try:
        d = json.loads(f.read_text())
    except Exception:
        return False
    if d.get("error"):
        return True
    try:
        return d["response"]["choices"][0].get("finish_reason") == "error"
    except Exception:
        return False


def load(runs, effort="xhigh"):
    rate, blk, reps = {}, {}, {}
    acc = collections.defaultdict(list)
    dropped = 0
    for r in runs:
        f = ROOT / "runs" / r / "scored.jsonl"
        if not f.exists():
            raise SystemExit(f"missing {f}")
        for line in f.open():
            d = json.loads(line)
            if d["effort"] != effort:
                continue
            if provider_error(r, effort, d["rep"], d["task_id"]):
                dropped += 1
                continue
            # В режиме устойчивости несосчитанная генерация (обрыв) идёт как провал.
            acc[d["task_id"]].append(bool(d.get("pass", False)))
            blk[d["task_id"]] = d["block"]
    for t, v in acc.items():
        rate[t], reps[t] = sum(v) / len(v), len(v)
    return rate, blk, reps, dropped


EPS = 1e-12


def stats(diffs, seed):
    """Returns (diff_pp, lo_pp, hi_pp, p, tie_share). Independent RNG streams
    per statistic so a result never depends on call order."""
    n = len(diffs)
    d = sum(diffs) / n
    rb = random.Random(seed)
    bs = sorted(sum(rb.choice(diffs) for _ in range(n)) / n for _ in range(B))
    lo, hi = bs[int(.025 * B)], bs[int(.975 * B)]
    rp = random.Random(seed + 1)
    hits = ties = 0
    for _ in range(B):
        s = sum(x if rp.random() < .5 else -x for x in diffs) / n
        if abs(abs(s) - abs(d)) < EPS:
            ties += 1
        if abs(s) >= abs(d) - EPS:          # conservative: ties count against
            hits += 1
    return d * 100, lo * 100, hi * 100, (hits + 1) / (B + 1), ties / B


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", nargs="+", required=True)
    ap.add_argument("--quant", nargs="+", required=True)
    ap.add_argument("--label", default="quant")
    # Проверка на устойчивость: считать обрывы не пропуском, а провалом модели.
    # Нужна там, где обрывы бьют по одному арму сильнее (llama.cpp медленнее,
    # и клиентский таймаут ловит именно самые длинные генерации).
    ap.add_argument("--errors-as-failures", action="store_true")
    a = ap.parse_args()
    global ERRORS_AS_FAILURES
    ERRORS_AS_FAILURES = a.errors_as_failures
    seed = 20260824

    rr, blk, rrep, rdrop = load(a.ref)
    qr, _, qrep, qdrop = load(a.quant)
    tasks = sorted(set(rr) & set(qr))
    thin = [t for t in tasks if rrep[t] < 3 or qrep[t] < 3]

    print(f"=== {a.label} vs BF16 reference, xhigh ===")
    print(f"reference runs : {', '.join(a.ref)}")
    print(f"quant runs     : {', '.join(a.quant)}")
    print(f"paired tasks   : {len(tasks)}"
          + (f"   ({len(rr)} ref / {len(qr)} quant scored)" if len(rr) != len(tasks)
             or len(qr) != len(tasks) else ""))
    if rdrop or qdrop:
        print(f"provider errors dropped as missing data: "
              f"reference {rdrop}, {a.label} {qdrop}")
    if thin:
        print(f"NOTE: {len(thin)} task(s) with fewer than 3 valid repeats "
              f"(a dropped provider error leaves fewer): {thin[:6]}")
    print()

    diffs = [qr[t] - rr[t] for t in tasks]
    d, lo, hi, p, tie = stats(diffs, seed)
    mr = sum(rr[t] for t in tasks) / len(tasks) * 100
    mq = sum(qr[t] for t in tasks) / len(tasks) * 100
    print("PRIMARY  mean pass rate")
    print(f"  reference {mr:6.2f} %   {a.label} {mq:6.2f} %")
    print(f"  difference {d:+.2f} pp   95% CI [{lo:+.2f}, {hi:+.2f}]   p = {p:.4f}")
    print(f"  ({tie:.1%} of permutations tie the observed value and are counted "
          f"against the effect)")
    print()

    live = [t for t in tasks if rr[t] > 0 or qr[t] > 0]
    dl, ll, hl, pl, _ = stats([qr[t] - rr[t] for t in live], seed + 100)
    print(f"SECONDARY  on the {len(live)} tasks either arm ever solved")
    print(f"  difference {dl:+.2f} pp   95% CI [{ll:+.2f}, {hl:+.2f}]   p = {pl:.4f}")
    print()

    print("BY BLOCK")
    print(f"  {'block':22s} {'n':>4} {'ref%':>7} {'quant%':>7} {'diff':>8} {'95% CI':>18} {'p':>7}")
    for b in sorted({blk[t] for t in tasks}):
        sub = [t for t in tasks if blk[t] == b]
        db, lb, hb, pb, _ = stats([qr[t] - rr[t] for t in sub], seed + 200)
        print(f"  {b:22s} {len(sub):4d} "
              f"{sum(rr[t] for t in sub)/len(sub)*100:7.2f} "
              f"{sum(qr[t] for t in sub)/len(sub)*100:7.2f} "
              f"{db:+8.2f} [{lb:+6.2f},{hb:+6.2f}] {pb:7.4f}")
    print()

    down = sum(1 for t in tasks if qr[t] < rr[t])
    up = sum(1 for t in tasks if qr[t] > rr[t])
    print(f"DESCRIPTIVE ONLY  tasks moved down {down}, up {up}, unchanged "
          f"{len(tasks)-down-up}")
    print("  (a raw count, not a test: it ignores how far each task moved)")


if __name__ == "__main__":
    main()
