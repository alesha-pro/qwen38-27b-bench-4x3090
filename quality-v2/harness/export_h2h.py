#!/usr/bin/env python3
"""Export Mirai S vs Bonsai 2 PQ2_0 head-to-head numbers (quant-bench v2) to JSON.
Same estimator/convention as the published table: paired_diff.py, --errors-as-failures."""
import sys, json, glob, statistics as st, collections
sys.path.insert(0, "$RUN_ROOT/quant-bench-v2/harness")
import paired_diff as pd
pd.ERRORS_AS_FAILURES = True
R = "$RUN_ROOT/quant-bench-v2/runs"
REF = {"xhigh": ["ref-final", "ref-ext"], "off": ["ref-final-efforts"], "low": ["ref-final-efforts"], "medium": ["ref-final-efforts"]}
ARMS = {"mirai": ["quant-mirai-s"], "bonsai": ["quant-bonsai2-pq2"]}
SEED = 20260824
out = {"effort": {}, "block_xhigh": {}, "tokens": {}, "reps": {}}
for e in ["off", "low", "medium", "xhigh"]:
    rr, blk, rrep, _ = pd.load(REF[e], e)
    q = {k: pd.load(v, e) for k, v in ARMS.items()}
    T = sorted(set(rr) & set(q["mirai"][0]) & set(q["bonsai"][0]))
    row = {"n": len(T), "ref": sum(rr[t] for t in T) / len(T) * 100}
    for k in ARMS:
        a = q[k][0]
        d, lo, hi, p, _ = pd.stats([a[t] - rr[t] for t in T], SEED)
        row[k] = {"rate": sum(a[t] for t in T) / len(T) * 100, "diff": d, "lo": lo, "hi": hi, "p": p}
    d, lo, hi, p, _ = pd.stats([q["bonsai"][0][t] - q["mirai"][0][t] for t in T], SEED)
    row["b_minus_m"] = {"diff": d, "lo": lo, "hi": hi, "p": p}
    out["effort"][e] = row
    if e == "xhigh":
        out["reps"] = {k: dict(collections.Counter(q[k][2][t] for t in T)) for k in ARMS}
        for b in sorted(set(blk[t] for t in T)):
            S = [t for t in T if blk[t] == b]
            br = {"n": len(S), "ref": sum(rr[t] for t in S) / len(S) * 100}
            for k in ARMS:
                a = q[k][0]
                d, lo, hi, p, _ = pd.stats([a[t] - rr[t] for t in S], SEED)
                br[k] = {"rate": sum(a[t] for t in S) / len(S) * 100, "diff": d, "p": p}
            out["block_xhigh"][b] = br
def tok(runs, e):
    L, cap, byb, capb = [], 0, collections.defaultdict(list), collections.Counter()
    for r in runs:
        for f in glob.glob(f"{R}/{r}/{e}/*/*.json"):
            d = json.load(open(f)); x = d.get("response")
            if not x or d.get("error"): continue
            n = x["usage"]["completion_tokens"]; L.append(n); byb[d["block"]].append(n)
            if x["choices"][0].get("finish_reason") == "length": cap += 1; capb[d["block"]] += 1
    return {"mean": st.mean(L), "n": len(L), "cap": cap,
            "block": {b: {"mean": st.mean(v), "n": len(v), "cap": capb[b]} for b, v in byb.items()}}
for k, runs in {"bf16": None, **ARMS}.items():
    out["tokens"][k] = {e: tok(REF[e] if k == "bf16" else runs, e) for e in ["off", "low", "medium", "xhigh"]}
out["gens"] = {k: sum(len(glob.glob(f"{R}/{v[0]}/*/*/*.json")) for _ in [0]) for k, v in ARMS.items()}
json.dump(out, open(sys.argv[1], "w"), indent=1)
print(json.dumps({e: (round(v["mirai"]["diff"], 2), round(v["bonsai"]["diff"], 2), round(v["b_minus_m"]["diff"], 2), round(v["b_minus_m"]["p"], 3)) for e, v in out["effort"].items()}))
print(out["reps"], out["gens"])
