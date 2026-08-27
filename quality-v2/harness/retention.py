#!/usr/bin/env python3
"""Paired retention of a quant arm against the BF16 reference.

Denominator is pre-registered: the 75 tasks the reference passed 3 of 3 at
xhigh. Tasks the reference itself flips or fails cannot measure a quant, so
they are excluded before any quant number is looked at.
"""
import json, sys, collections
ROOT = "/mnt/nvme/work/benchmarks/quant-bench-v2"
run = sys.argv[1] if len(sys.argv) > 1 else "quant-fp8"
effort = sys.argv[2] if len(sys.argv) > 2 else "xhigh"

ref = collections.defaultdict(list); blk = {}
for l in open(f"{ROOT}/runs/ref-final/scored.jsonl"):
    r = json.loads(l); ref[r["task_id"]].append(bool(r["pass"])); blk[r["task_id"]] = r["block"]
stable = {t for t, v in ref.items() if len(v) >= 3 and all(v)}

q = collections.defaultdict(list)
for l in open(f"{ROOT}/runs/{run}/scored.jsonl"):
    r = json.loads(l)
    if r["effort"] == effort:
        q[r["task_id"]].append(bool(r["pass"]))
if not q:
    sys.exit(f"no {effort} rows scored yet for {run}")

reps = max(len(v) for v in q.values())
def maj(v): return sum(v) * 2 > len(v)

print(f"=== {run} / {effort}  ({reps} repeat(s), {len(q)} tasks scored) ===")
print()
print("PAIRED RETENTION vs BF16, denominator = the 75 stable reference tasks")
print("%-18s %7s %9s %9s" % ("block", "stable", "quant ok", "retention"))
tot_n = tot_k = 0
for b in sorted(set(blk[t] for t in stable)):
    ts = [t for t in stable if blk[t] == b and t in q]
    if not ts: continue
    k = sum(1 for t in ts if maj(q[t]))
    tot_n += len(ts); tot_k += k
    print("%-18s %7d %9d %8.1f%%" % (b, len(ts), k, 100 * k / len(ts)))
print("%-18s %7d %9d %8.1f%%" % ("ALL", tot_n, tot_k, 100 * tot_k / tot_n if tot_n else 0))
missing = len(stable) - tot_n
if missing:
    print(f"({missing} of the 75 not scored yet)")
print()
mk = sum(sum(v) for v in q.values()); mn = sum(len(v) for v in q.values())
rk = sum(1 for t in q for _ in [0] if False)
print("marginal pass on all %d scored tasks: %d/%d = %.3f" % (len(q), mk, mn, mk / mn))
refm = [x for t in q for x in ref[t]]
print("reference on those same tasks:       %d/%d = %.3f"
      % (sum(refm), len(refm), sum(refm) / len(refm)))
print()
lost = sorted(t for t in stable if t in q and not maj(q[t]))
if lost:
    print("tasks the reference always passed and the quant lost (%d):" % len(lost))
    for t in lost: print("   %-34s %s" % (t, blk[t]))
