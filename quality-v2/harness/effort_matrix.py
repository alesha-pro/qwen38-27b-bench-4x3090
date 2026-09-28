#!/usr/bin/env python3
"""Effort matrix for quant-bench v2: pass rate per effort and the paired
difference against the BF16 reference, same estimator and same missing-data
rule as paired_diff.py (imported, not re-implemented).

Usage: effort_matrix.py LABEL=run[,run...] [LABEL=run ...]
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paired_diff as pdiff

REF = {"xhigh": ["ref-final", "ref-ext"], "off": ["ref-final-efforts"],
       "low": ["ref-final-efforts"], "medium": ["ref-final-efforts"]}
EFFORTS = ["off", "low", "medium", "xhigh"]
SEED = 20260824


def row(runs):
    rates, diffs, blocks = {}, {}, None
    for e in EFFORTS:
        rr, blk, _, _ = pdiff.load(REF[e], e)
        try:
            qr, _, _, _ = pdiff.load(runs, e)
        except SystemExit:
            continue
        tasks = sorted(set(rr) & set(qr))
        if not tasks:
            continue
        d, lo, hi, p, _ = pdiff.stats([qr[t] - rr[t] for t in tasks], SEED)
        rates[e] = (sum(qr[t] for t in tasks) / len(tasks) * 100,
                    sum(rr[t] for t in tasks) / len(tasks) * 100, len(tasks))
        diffs[e] = (d, lo, hi, p)
        if e == "xhigh":
            blocks = {}
            for b in sorted({blk[t] for t in tasks}):
                sub = [t for t in tasks if blk[t] == b]
                blocks[b] = sum(qr[t] - rr[t] for t in sub) / len(sub) * 100
    return rates, diffs, blocks


def main():
    args = sys.argv[1:]
    if "--errors-as-failures" in args:   # the convention of the published README table
        args.remove("--errors-as-failures")
        pdiff.ERRORS_AS_FAILURES = True
    arms = [a.split("=", 1) for a in args]
    out = {lab: row(r.split(",")) for lab, r in arms}
    print(f"{'arm':14s}" + "".join(f"{e:>16s}" for e in EFFORTS))
    for lab, (rates, diffs, _) in out.items():
        cells = []
        for e in EFFORTS:
            if e in rates:
                q, r, n = rates[e]
                cells.append(f"{q:6.1f}% (n={n:3d})")
            else:
                cells.append(f"{'-':>15s}")
        print(f"{lab:14s}" + " ".join(f"{c:>15s}" for c in cells))
    print("\ndiff vs BF16 (pp) / p")
    for lab, (rates, diffs, _) in out.items():
        cells = [f"{diffs[e][0]:+5.1f}/p={diffs[e][3]:.3f}" if e in diffs else "-" for e in EFFORTS]
        print(f"{lab:14s}" + " ".join(f"{c:>15s}" for c in cells))
    print("\nxhigh 95% CI")
    for lab, (rates, diffs, _) in out.items():
        if "xhigh" in diffs:
            d, lo, hi, p = diffs["xhigh"]
            print(f"{lab:14s} {d:+.1f} pp [{lo:+.1f}, {hi:+.1f}] p={p:.4f}")
    print("\nxhigh diff by block (pp)")
    for lab, (_, _, blocks) in out.items():
        if blocks:
            print(f"{lab:14s} " + "  ".join(f"{b}={v:+.1f}" for b, v in blocks.items()))


if __name__ == "__main__":
    main()
