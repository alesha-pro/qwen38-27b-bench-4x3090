#!/usr/bin/env python3
"""Pick a canary subset of the frozen 100 under a GPU-token budget.

Selection is stratified on purpose. Cheapest-first alone would return only
tool-calling and short reasoning-gym, and a canary made of 200-token answers
says nothing about long-context behaviour. So: every tool-calling task (they
are nearly free and give the pass-rate comparison its task count), a cost-spread
sample of rg/if, and the three cheapest math tasks to keep long outputs in.
"""
import glob, json, os, statistics as st
from collections import defaultdict

ROOT = "/mnt/nvme/work/benchmarks/quant-bench-v2"
os.chdir(ROOT)

cost, block = {}, {}
for rep in ("r1", "r2", "r3"):
    for f in glob.glob(f"runs/ref-final/xhigh/{rep}/*.json"):
        r = json.load(open(f))
        u = (r.get("response") or {}).get("usage") or {}
        cost.setdefault(r["task_id"], []).append(u.get("completion_tokens") or 0)
        block[r["task_id"]] = r.get("block")
mean = {t: st.mean(v) for t, v in cost.items()}

pool = {json.loads(l)["id"]: json.loads(l)
        for l in open("final-pool/finalpool.jsonl")}

by = defaultdict(list)
for t in mean:
    by[block[t]].append(t)
for b in by:
    by[b].sort(key=lambda t: mean[t])


def spread(tasks, n):
    """n tasks spanning the cost range, not just the cheap end."""
    if n >= len(tasks):
        return list(tasks)
    idx = [round(i * (len(tasks) - 1) / (n - 1)) for i in range(n)]
    return [tasks[i] for i in sorted(set(idx))]


picked = (list(by["tool-calling"])
          + spread(by["quant-core-rg"], 12)
          + spread(by["quant-core-if"], 8)
          + by["quant-core-math"][:3])

picked.sort(key=lambda t: mean[t])
with open("final-pool/canarypool.jsonl", "w") as fh:
    for t in picked:
        fh.write(json.dumps(pool[t], ensure_ascii=False) + "\n")

print("%-16s %5s %14s" % ("block", "n", "tokens x3rep"))
tot = 0
for b in sorted(by):
    sel = [t for t in picked if block[t] == b]
    s = sum(sum(cost[t]) for t in sel)
    tot += s
    print("%-16s %5d %14s" % (b, len(sel), f"{s:,}"))
print("%-16s %5d %14s" % ("TOTAL", len(picked), f"{tot:,}"))
print()
print("cost range of picked tasks: %d .. %d tokens (mean per repeat)"
      % (min(mean[t] for t in picked), max(mean[t] for t in picked)))
print()
print("cumulative budget by --limit (tokens for 3 repeats):")
run = 0
for i, t in enumerate(picked, 1):
    run += sum(cost[t])
    if i % 6 == 0 or i == len(picked):
        print("  limit %3d -> %10s tokens  (~%.1f h at 30 tok/s)"
              % (i, f"{run:,}", run / 30 / 3600))
