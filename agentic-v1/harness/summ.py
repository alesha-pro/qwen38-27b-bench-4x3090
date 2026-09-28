import json,glob,sys,collections
arm=sys.argv[1]
R=f"$RUN_ROOT/agentic-v1/runs/{arm}"
got={}  # (rep, pack, id) -> passed
skipped=collections.Counter(); fm=collections.Counter()
for f in sorted(glob.glob(f"{R}/r*/s*/result.json")):
    rep=f.split("/")[-3]
    d=json.load(open(f))
    for p in d.get("packs",[]):
        if p.get("skipped"): skipped[(rep,p["pack_id"])]+=1
        for sc in p.get("scenarios",[]):
            got[(rep,p["pack_id"],sc["id"])]=bool(sc.get("passed")); fm[sc.get("failure_mode")]+=1
exp={(f"r{r}",pk,f"{'CLI' if pk=='cli-40' else 'HA'}-{i:02d}") for r in (1,2,3) for pk,n in (("cli-40",40),("hermesagent-20",20)) for i in range(1,n+1)}
missing=sorted(exp-set(got))
by=collections.defaultdict(lambda:[0,0])
for (rep,pk,i),v in got.items(): by[pk][0]+=v; by[pk][1]+=1
print(arm, "scored", len(got), "of", len(exp), "| missing", len(missing), missing[:8])
print("  per pack:", {k:f"{a}/{b} = {a/b*100:.1f}%" for k,(a,b) in by.items()})
print("  failure modes:", fm.most_common(8))
