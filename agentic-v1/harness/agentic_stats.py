import json,glob,collections,random,math
R="$RUN_ROOT/agentic-v1/runs"
E="$ENGINE_ROOT/appworld/repo/experiments/outputs/simplified_react_code_agent/local"
arms=["bf16","mirai","bonsai"]
def bench(arm):
    got={}
    for f in glob.glob(f"{R}/{arm}/r*/s*/result.json"):
        rep=f.split("/")[-3]
        for p in json.load(open(f)).get("packs",[]):
            for sc in p.get("scenarios",[]): got[(rep,p["pack_id"],sc["id"])]=int(bool(sc.get("passed")))
    per=collections.defaultdict(list)
    for (rep,pk,i),v in got.items(): per[(pk,i)].append(v)
    return {k:sum(v)/len(v) for k,v in per.items()}
B={a:bench(a) for a in arms}
def signflip(d,n=200000,seed=20260824):
    rnd=random.Random(seed); obs=abs(sum(d)); c=0
    nz=[x for x in d if x]
    for _ in range(n):
        if abs(sum(x if rnd.random()<.5 else -x for x in nz))>=obs-1e-12: c+=1
    return c/n
def boot(d,n=20000,seed=20260824):
    rnd=random.Random(seed); m=[]
    for _ in range(n): s=[d[rnd.randrange(len(d))] for _ in d]; m.append(sum(s)/len(s))
    m.sort(); return m[int(.025*n)],m[int(.975*n)]
out={"benchlocal":{}, "appworld":{}}
for pk in ["cli-40","hermesagent-20",None]:
    keys=sorted(k for k in B["bf16"] if pk is None or k[0]==pk)
    name=pk or "both"
    out["benchlocal"][name]={a:round(100*sum(B[a][k] for k in keys)/len(keys),1) for a in arms}
    for x,y in [("mirai","bf16"),("bonsai","bf16"),("bonsai","mirai")]:
        d=[B[x][k]-B[y][k] for k in keys]; lo,hi=boot(d)
        out["benchlocal"][f"{name}:{x}-{y}"]={"diff":round(100*sum(d)/len(d),1),"ci":[round(100*lo,1),round(100*hi,1)],"p":round(signflip(d),4)}
A={a:json.load(open(f"{E}/agentic-v1-{a}/test_normal/evaluations/test_normal.json")) for a in arms}
ok={a:{t for t,v in A[a]["individual"].items() if v["success"]} for a in arms}
def binom2(k,n):
    if n==0: return 1.0
    k=min(k,n-k); p=sum(math.comb(n,i) for i in range(k+1))/2**n; return min(1,2*p)
for a in arms: out["appworld"][a]=A[a]["aggregate"]
for x,y in [("mirai","bf16"),("bonsai","bf16"),("bonsai","mirai")]:
    only_y=len(ok[y]-ok[x]); only_x=len(ok[x]-ok[y])
    out["appworld"][f"{x}-{y}"]={f"only_{x}":only_x,f"only_{y}":only_y,"p_mcnemar_exact":binom2(only_x,only_x+only_y)}
# tests passed fraction (partial credit view) per arm
for a in arms:
    iv=A[a]["individual"].values(); out["appworld"][a+"_test_pass_frac"]=round(100*sum(len(v["passes"]) for v in iv)/sum(v["num_tests"] for v in iv),1)
# per-task steps and tokens from lm_calls
for a in arms:
    steps=[];ctoks=[]
    for t in glob.glob(f"{E}/agentic-v1-{a}/test_normal/tasks/*/logs/lm_calls.jsonl"):
        L=[json.loads(l) for l in open(t)]; steps.append(len(L))
    out["appworld"][a+"_steps"]={"mean":round(sum(steps)/len(steps),1),"at_cap_50":sum(s>=50 for s in steps),"n":len(steps)}
for a in arms:
    ct=[];
    for f in glob.glob(f"{R}/appworld-{a}/telemetry-*.jsonl"):
        for l in open(f):
            r=json.loads(l)
            if r["status_code"]==200 and isinstance(r.get("response"),dict):
                u=r["response"].get("usage") or {}; ct.append(u.get("completion_tokens",0))
    out["appworld"][a+"_tok"]={"per_call":round(sum(ct)/len(ct)),"per_task":round(sum(ct)/168),"total":sum(ct)}
json.dump(out,open(f"{R}/agentic_summary.json","w"),indent=1)
print(json.dumps(out,indent=1))
