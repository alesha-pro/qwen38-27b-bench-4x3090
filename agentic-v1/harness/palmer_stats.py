import json, glob, random, math, os
R = "$RUN_ROOT/agentic-v1/runs"
E = "$ENGINE_ROOT/appworld/repo/experiments/outputs/simplified_react_code_agent/local"
ARMS = ["bf16", "mirai", "bonsai", "bonsai-med", "bonsai-nothink"]


def bench(arm):
    got = {}
    for f in glob.glob(f"{R}/{arm}/r*/s*/result.json"):
        d = json.load(open(f)); rep = f.split("/")[-3]
        for p in d["packs"]:
            for sc in p.get("scenarios", []):
                got[(rep, p["pack_id"], sc["id"])] = int(bool(sc.get("passed")))
    return got


def signflip(a, b, keys, n=200000, seed=20260824):
    # paired by scenario: mean over repeats
    sc = sorted({(k[1], k[2]) for k in keys})
    diffs = []
    for s in sc:
        ka = [k for k in keys if (k[1], k[2]) == s]
        diffs.append(sum(a[k] - b[k] for k in ka) / len(ka))
    obs = sum(diffs) / len(diffs)
    rnd = random.Random(seed); c = 0
    for _ in range(n):
        m = sum(d if rnd.random() < .5 else -d for d in diffs) / len(diffs)
        if abs(m) >= abs(obs) - 1e-12: c += 1
    return 100 * obs, c / n


def mcnemar(x, y):
    n = x + y; k = min(x, y)
    p = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n * 2
    return min(1.0, p)


B = {a: bench(a) for a in ARMS}
print("== BenchLocal")
for a in ARMS:
    row = []
    for pk in ["cli-40", "hermesagent-20"]:
        ks = [k for k in B[a] if k[1] == pk]
        row.append(f"{pk} {100*sum(B[a][k] for k in ks)/len(ks):.1f} n={len(ks)}")
    print(f"{a:15s}", " | ".join(row), f"| all {100*sum(B[a].values())/len(B[a]):.1f}")
for x, y in [("bonsai-med", "bonsai"), ("bonsai-nothink", "bonsai"), ("bonsai-med", "mirai"), ("bonsai-nothink", "mirai")]:
    for pk in ["cli-40", "hermesagent-20", None]:
        keys = [k for k in B[x] if k in B[y] and (pk is None or k[1] == pk)]
        d, p = signflip(B[x], B[y], keys)
        print(f"  {x} - {y} [{pk or 'both'}]: {d:+.1f} p={p:.3f}")

print("== AppWorld")
A, ok = {}, {}
for a in ARMS:
    A[a] = json.load(open(f"{E}/agentic-v1-{a}/test_normal/evaluations/test_normal.json"))
    ok[a] = {t for t, v in A[a]["individual"].items() if v["success"]}
    agg = A[a]["aggregate"]
    print(f"{a:15s} n={len(A[a]['individual'])} TGC {agg.get('task_goal_completion')} SGC {agg.get('scenario_goal_completion')}")
# difficulty
meta = "$ENGINE_ROOT/appworld/repo/data/tasks"
def diff(t):
    try: return json.load(open(f"{meta}/{t}/ground_truth/metadata.json"))["difficulty"]
    except Exception: return None
tasks = sorted(A["bonsai"]["individual"])
D = {t: diff(t) for t in tasks}
for a in ARMS:
    by = {}
    for t in tasks:
        by.setdefault(D[t], []).append(t in ok[a])
    print(f"  {a:15s}", {k: f"{100*sum(v)/len(v):.1f}" for k, v in sorted(by.items(), key=lambda kv: str(kv[0]))})
for x, y in [("bonsai-med", "bonsai"), ("bonsai-nothink", "bonsai"), ("bonsai-med", "mirai"), ("bonsai-nothink", "mirai"), ("bonsai-med", "bonsai-nothink")]:
    only_x = len(ok[x] - ok[y]); only_y = len(ok[y] - ok[x])
    print(f"  {x} vs {y}: only {x} {only_x}, only {y} {only_y}, p={mcnemar(only_x, only_y):.2g}")

print("== AppWorld telemetry")
for a in ["bonsai", "bonsai-med", "bonsai-nothink", "mirai"]:
    calls = 0; comp = 0; rc = 0; tag = 0; tasks_tag = set(); fin = {}; budget_hit = 0
    for f in glob.glob(f"{R}/appworld-{a}/telemetry-*.jsonl"):
        for l in open(f):
            d = json.loads(l)
            if not d["incoming_path"].endswith("chat/completions"): continue
            s = d.get("response_summary") or {}
            calls += 1; comp += (s.get("usage") or {}).get("completion_tokens") or 0
            rc += s.get("reasoning_chars") or 0
            fin[s.get("finish_reason")] = fin.get(s.get("finish_reason"), 0) + 1
            ex = json.dumps(d.get("response_extracted"))
            if "<tool_call>" in ex: tag += 1
            if "Now produce the complete answer" in ex: budget_hit += 1
    # steps per task
    steps = []; cap = 0; drift_tasks = 0
    for t in tasks:
        lf = f"{E}/agentic-v1-{a}/test_normal/tasks/{t}/logs/lm_calls.jsonl"
        n = sum(1 for _ in open(lf)) if os.path.exists(lf) else 0
        steps.append(n); cap += n >= 50
    print(f"{a:15s} calls {calls} tok/call {comp/max(calls,1):.0f} tok/task {comp/len(tasks)/1000:.1f}K steps/task {sum(steps)/len(steps):.1f} cap50 {cap} "
          f"tool_call-tag calls {tag} budget-close {budget_hit} finish {fin}")
