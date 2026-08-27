#!/usr/bin/env python3
"""Paired comparison of the rig arm against the paid AkashML reference.

Marginal pass rates on 47 tasks would not settle anything on their own, so the
comparison is paired: same frozen tasks, same effort, majority of three repeats
per task, McNemar on the tasks where the two arms disagree.
"""
import json, math, os, sys
from collections import defaultdict

ROOT = "/mnt/nvme/work/benchmarks/quant-bench-v2"


def load(path, keep=None):
    per = defaultdict(list)
    meta = {}
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        t = r["task_id"]
        if keep and t not in keep:
            continue
        per[t].append(bool(r.get("pass")))
        meta[t] = r.get("block")
    return per, meta


def mcnemar(b, c):
    """Exact two-sided binomial test on the discordant pairs."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(k + 1)) * (0.5 ** n)
    return min(1.0, 2 * tail)


def main():
    pool = [json.loads(l)["id"]
            for l in open(f"{ROOT}/final-pool/canarypool.jsonl", encoding="utf-8")]
    keep = set(pool)
    ref, blocks = load(f"{ROOT}/runs/ref-final/scored.jsonl", keep)
    rig_path = sys.argv[1] if len(sys.argv) > 1 else f"{ROOT}/runs/canary-rig-bf16/scored.jsonl"
    if not os.path.exists(rig_path):
        sys.exit(f"rig scores not found: {rig_path}")
    rig, _ = load(rig_path, keep)

    common = sorted(set(ref) & set(rig))
    print(f"canary pool: {len(pool)} tasks | scored on both arms: {len(common)}")
    missing = sorted(keep - set(rig))
    if missing:
        print(f"missing on rig arm ({len(missing)}): {', '.join(missing[:6])}"
              + (" ..." if len(missing) > 6 else ""))
    print()

    def rate(per, tasks):
        tr = [v for t in tasks for v in per[t]]
        return sum(tr) / len(tr) if tr else float("nan"), len(tr)

    print("=== marginal pass rate (all trials) ===")
    print("%-18s %6s %8s %8s" % ("block", "tasks", "AkashML", "rig bf16"))
    byb = defaultdict(list)
    for t in common:
        byb[blocks.get(t, "?")].append(t)
    for b in sorted(byb):
        ra, na = rate(ref, byb[b])
        rb, nb = rate(rig, byb[b])
        print("%-18s %6d %8.3f %8.3f" % (b, len(byb[b]), ra, rb))
    ra, na = rate(ref, common)
    rb, nb = rate(rig, common)
    print("%-18s %6d %8.3f %8.3f   (%d vs %d trials)"
          % ("ALL", len(common), ra, rb, na, nb))
    print(f"difference: {(rb - ra) * 100:+.1f} pp")
    print()

    def maj(v):
        return sum(v) * 2 > len(v)

    b_only = [t for t in common if maj(ref[t]) and not maj(rig[t])]
    c_only = [t for t in common if maj(rig[t]) and not maj(ref[t])]
    both = sum(1 for t in common if maj(ref[t]) and maj(rig[t]))
    neither = sum(1 for t in common if not maj(ref[t]) and not maj(rig[t]))
    p = mcnemar(len(b_only), len(c_only))
    print("=== paired, majority of 3 repeats per task ===")
    print(f"  both pass      {both}")
    print(f"  both fail      {neither}")
    print(f"  only AkashML   {len(b_only)}   {', '.join(b_only[:5])}")
    print(f"  only rig       {len(c_only)}   {', '.join(c_only[:5])}")
    print(f"  McNemar exact two-sided p = {p:.4f}"
          f"   -> {'no significant difference' if p > 0.05 else 'SIGNIFICANT DIFFERENCE'}")
    print()

    stable = [t for t in common if all(ref[t]) and len(ref[t]) >= 3]
    if stable:
        rr, _ = rate(rig, stable)
        print("=== on the reference's own stable set (passed all repeats) ===")
        print(f"  tasks: {len(stable)} of {len(common)}")
        print(f"  rig retention on that set: {rr:.3f}")
        print("  (this is the denominator the real retention numbers will use)")
    print()
    print("=== per-task pass counts, disagreements only ===")
    dis = [t for t in common if sum(ref[t]) != sum(rig[t])]
    print(f"  tasks with different pass counts: {len(dis)} of {len(common)}")
    for t in dis[:15]:
        print("   %-34s akash %d/%d   rig %d/%d"
              % (t, sum(ref[t]), len(ref[t]), sum(rig[t]), len(rig[t])))
    if len(dis) > 15:
        print(f"   ... and {len(dis) - 15} more")


if __name__ == "__main__":
    main()
