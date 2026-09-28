#!/usr/bin/env python3
"""Health check for a freshly started Mirai S vLLM instance.

Seen 2026-09-25: a fresh instance of the plugin can come up broken so that
short requests look fine while long generations fall into repetition and
garbage; a restart fixed it. The effort gate (~10K tokens) is too short to
be sure, so this sends one pool task that took the BF16 reference ~20K
tokens at xhigh and checks the reasoning for loops, quarter by quarter.

Metric: share of distinct 12-word shingles within each quarter of the
reasoning text. Normal reasoning re-checks itself but stays well above 0.7;
a degenerate loop drives the later quarters toward zero.
Exit 0 = healthy, 1 = degenerate, 2 = inconclusive (no long output).
"""
import argparse, glob, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import or_client
from run_devpool import build_request

ROOT = "$RUN_ROOT/quant-bench-v2"
MIN_DISTINCT = 0.5
MIN_TOKENS = 8000


def ref_lengths():
    out = {}
    for f in glob.glob(f"{ROOT}/runs/ref-final/xhigh/r1/*.json") + \
             glob.glob(f"{ROOT}/runs/ref-ext/xhigh/r1/*.json"):
        d = json.load(open(f))
        if d.get("error") or d.get("block") == "tool-calling":
            continue
        n = ((d.get("response") or {}).get("usage") or {}).get("completion_tokens")
        if n:
            out[d["task_id"]] = n
    return out


def quarters(text, k=12):
    w = text.split()
    res = []
    for q in range(4):
        part = w[len(w) * q // 4: len(w) * (q + 1) // 4]
        sh = [" ".join(part[i:i + k]) for i in range(max(0, len(part) - k + 1))]
        res.append(round(len(set(sh)) / len(sh), 3) if sh else None)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    pool = {json.loads(l)["id"]: json.loads(l)
            for l in open(f"{ROOT}/final-pool/allpool.jsonl", encoding="utf-8")}
    lens = {t: n for t, n in ref_lengths().items() if t in pool}
    cands = sorted(lens, key=lambda t: abs(lens[t] - 20000))[:3]
    report = []
    for tid in cands:
        msgs, tools = build_request(pool[tid])
        r = or_client.chat(msgs, "xhigh", effort_mode="raw", tools=tools,
                           max_tokens=131072, retries=1)
        if r["error"]:
            print(f"  {tid}: ERROR {r['error'][:200]}")
            report.append({"task": tid, "error": r["error"]})
            continue
        ch = r["response"]["choices"][0]
        msg = ch["message"]
        think = msg.get("reasoning_content") or msg.get("reasoning") or ""
        n = (r["response"].get("usage") or {}).get("completion_tokens") or 0
        q = quarters(think)
        rec = {"task": tid, "ref_tokens": lens[tid], "tokens": n,
               "finish": ch.get("finish_reason"), "distinct_12gram_by_quarter": q,
               "latency_s": round(r["latency_s"], 1),
               "tok_per_s": round(n / r["latency_s"], 1) if r["latency_s"] else None,
               "answer_tail": (msg.get("content") or "")[-200:]}
        report.append(rec)
        print(f"  {tid}: ref {lens[tid]} tok, got {n} tok, finish={rec['finish']}, "
              f"{rec['tok_per_s']} tok/s, distinct by quarter {q}")
        if ch.get("finish_reason") == "length" or any(x is not None and x < MIN_DISTINCT for x in q):
            json.dump(report, open(a.out, "w"), indent=1)
            print("DEGENERATE: loops in a long generation")
            sys.exit(1)
        if n >= MIN_TOKENS:
            json.dump(report, open(a.out, "w"), indent=1)
            print("HEALTHY")
            sys.exit(0)
    json.dump(report, open(a.out, "w"), indent=1)
    print("INCONCLUSIVE: no generation reached", MIN_TOKENS, "tokens")
    sys.exit(2)


if __name__ == "__main__":
    main()
