#!/usr/bin/env python3
"""KV-cache canary probe: compare next-token distributions across arms.

Why a distribution probe and not pass rates: at temp=1.0 the pass-rate noise
floor is 3-4 pp, so "the arms scored the same" can mean "the instrument is too
blunt to see the difference". Scoring one deterministic next-token distribution
after a long prompt has no sampling noise at all.

Constraints discovered against AkashML on 2026-08-24:
  - logprobs come back ONLY with thinking disabled; with reasoning_effort set
    the token goes to the reasoning channel and logprobs is null;
  - assistant prefill is NOT honoured (the trailing assistant message is
    dropped), so teacher-forced scoring of an existing trace is impossible.
Hence: long prompt -> first generated token -> top-k distribution. The KV state
under test is the prompt's KV, which is why prompt length is the axis that
matters.

Arms:
  akash   bf16 weights via OpenRouter, provider pinned, KV dtype unknown
  rig     whatever the local /v1 is serving (set --base-url and --label)

Usage:
  python3 kv_probe.py build   --out probes.jsonl --lengths 4000,16000,48000,100000 --per-length 5
  python3 kv_probe.py run     --probes probes.jsonl --arm akash --out dist-akash.jsonl
  python3 kv_probe.py run     --probes probes.jsonl --arm rig --label rig-kv-bf16 \
                              --base-url http://127.0.0.1:18000/v1 --out dist-rig-bf16.jsonl
  python3 kv_probe.py compare dist-akash.jsonl dist-rig-bf16.jsonl dist-rig-fp8.jsonl
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MODEL_OR = "qwen/qwen3.8-27b"
TOP_K = 20


def api_key() -> str:
    k = os.environ.get("OPENROUTER_API_KEY", "")
    if not k:
        p = os.path.expanduser("~/.config/openrouter/key")
        if os.path.exists(p):
            k = open(p).read().strip()
    if not k:
        raise RuntimeError("no OpenRouter key")
    return k


def post(url: str, body: dict, headers: dict, timeout: int = 600) -> dict:
    req = urllib.request.Request(
        url, data=json.dumps(body).encode(), headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode())


# ---------------------------------------------------------------- build

def iter_traces(runs_dir):
    """Yield (task_id, text) from reference traces already paid for.

    Traces live as one .json per task under runs/<run>/<effort>/<repeat>/,
    with the model text in response.choices[0].message.{reasoning,content}.
    """
    for root, _dirs, files in os.walk(runs_dir):
        for fn in sorted(files):
            if not fn.endswith(".json"):
                continue
            try:
                rec = json.load(open(os.path.join(root, fn), encoding="utf-8"))
            except Exception:
                continue
            if not isinstance(rec, dict):
                continue
            choices = ((rec.get("response") or {}).get("choices") or [])
            if not choices:
                continue
            msg = (choices[0] or {}).get("message") or {}
            text = (msg.get("reasoning") or "") + (msg.get("content") or "")
            if len(text) > 2000:
                yield str(rec.get("task_id") or fn), text


def cmd_build(args):
    lengths = [int(x) for x in args.lengths.split(",")]
    pool = sorted(set(iter_traces(args.runs)), key=lambda tv: -len(tv[1]))
    if not pool:
        sys.exit("no traces under %s" % args.runs)
    total_chars = sum(len(t) for _i, t in pool)
    print("pool: %d traces, %.1fM chars" % (len(pool), total_chars / 1e6))

    # ~3.6 chars per token is the observed ratio for this model's traces.
    # Long probes are built by concatenating traces: what matters is that every
    # arm gets a byte-identical prompt of the target length, not that it reads
    # as one coherent document.
    SEP = "\n\n---\n\n"
    out = []
    cursor = 0
    for want_tok in lengths:
        want_chars = int(want_tok * 3.6)
        if want_chars > total_chars:
            print("warn: %d tok needs %d chars, pool holds %d - skipping"
                  % (want_tok, want_chars, total_chars), file=sys.stderr)
            continue
        for n in range(args.per_length):
            parts, used, size = [], [], 0
            while size < want_chars:
                tid, text = pool[cursor % len(pool)]
                cursor += 1
                parts.append(text)
                used.append(tid)
                size += len(text) + len(SEP)
            prompt = SEP.join(parts)[:want_chars]
            out.append({
                "probe_id": "L%d-%d" % (want_tok, n),
                "target_tokens": want_tok,
                "source_tasks": used,
                "prompt": prompt,
            })
    with open(args.out, "w", encoding="utf-8") as fh:
        for rec in out:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print("wrote %d probes -> %s" % (len(out), args.out))


# ---------------------------------------------------------------- run

INSTRUCTION = ("Below is a partial solution transcript. Continue it with the "
               "single next word. Do not restate anything.\n\n")


def build_body(arm: str, prompt: str) -> dict:
    body = {
        "messages": [{"role": "user", "content": INSTRUCTION + prompt}],
        "max_tokens": 1,
        "temperature": 0,
        "top_p": 1,
        "logprobs": True,
        "top_logprobs": TOP_K,
        "seed": 20260824,
    }
    if arm == "akash":
        body["model"] = MODEL_OR
        body["provider"] = {"order": ["AkashML"], "allow_fallbacks": False,
                            "quantizations": ["bf16"]}
        body["reasoning"] = {"enabled": False}
        body["usage"] = {"include": True}
    else:
        body["model"] = os.environ.get("RIG_MODEL", "qwen3.8-27b")
        body["chat_template_kwargs"] = {"enable_thinking": False}
    return body


def cmd_run(args):
    if args.arm == "akash":
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {"Authorization": "Bearer " + api_key(),
                   "Content-Type": "application/json"}
        label = args.label or "akash-bf16"
    else:
        url = args.base_url.rstrip("/") + "/chat/completions"
        headers = {"Content-Type": "application/json"}
        label = args.label or "rig"

    probes = [json.loads(l) for l in open(args.probes, encoding="utf-8") if l.strip()]
    done = set()
    if args.resume and os.path.exists(args.out):
        for line in open(args.out, encoding="utf-8"):
            try:
                done.add(json.loads(line)["probe_id"])
            except Exception:
                pass

    spent = 0.0
    with open(args.out, "a", encoding="utf-8") as fh:
        for i, p in enumerate(probes, 1):
            if p["probe_id"] in done:
                continue
            body = build_body(args.arm, p["prompt"])
            d = None
            for attempt in range(3):
                try:
                    d = post(url, body, headers)
                    break
                except urllib.error.HTTPError as e:
                    detail = e.read().decode()[:300]
                    if attempt == 2:
                        sys.exit("%s: HTTP %s %s" % (p["probe_id"], e.code, detail))
                    time.sleep(5 * (attempt + 1))
                except Exception as e:
                    if attempt == 2:
                        sys.exit("%s: %s" % (p["probe_id"], e))
                    time.sleep(5 * (attempt + 1))

            prov = d.get("provider")
            if args.arm == "akash" and prov != "AkashML":
                sys.exit("provider swapped to %r - aborting, reference is void" % prov)

            ch = d["choices"][0]
            lp = ch.get("logprobs") or {}
            toks = lp.get("content") or []
            if not toks:
                sys.exit("%s: no logprobs returned (thinking must be off "
                         "for this provider)" % p["probe_id"])
            t0 = toks[0]
            usage = d.get("usage") or {}
            spent += float(usage.get("cost") or 0)
            fh.write(json.dumps({
                "probe_id": p["probe_id"],
                "target_tokens": p["target_tokens"],
                "arm": label,
                "provider": prov,
                "prompt_tokens": usage.get("prompt_tokens"),
                "top": [{"token": a.get("token"), "logprob": a.get("logprob")}
                        for a in (t0.get("top_logprobs") or [])],
                "chosen": t0.get("token"),
            }, ensure_ascii=False) + "\n")
            fh.flush()
            print("[%d/%d] %s prompt=%s chosen=%r spent=$%.4f" % (
                i, len(probes), p["probe_id"], usage.get("prompt_tokens"),
                t0.get("token"), spent))
    print("done, arm=%s, cost=$%.4f" % (label, spent))


# ---------------------------------------------------------------- compare

def dist(rec):
    """Renormalised probability over the reported top-k."""
    items = [(a["token"], math.exp(a["logprob"])) for a in rec["top"]]
    z = sum(p for _t, p in items) or 1.0
    return dict((t, p / z) for t, p in items)


def kl(p, q, floor=1e-6):
    return sum(pv * math.log(pv / max(q.get(t, 0.0), floor))
               for t, pv in p.items() if pv > 0)


def load(path):
    out = {}
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if line:
            r = json.loads(line)
            out[r["probe_id"]] = r
    return out


def cmd_compare(args):
    arms = [load(p) for p in args.files]
    names = [next(iter(a.values()))["arm"] if a else p
             for a, p in zip(arms, args.files)]
    common = set(arms[0])
    for a in arms[1:]:
        common &= set(a)
    if not common:
        sys.exit("no shared probe ids")

    base = 0
    print("baseline arm: %s   shared probes: %d\n" % (names[base], len(common)))
    for j in range(len(arms)):
        if j == base:
            continue
        rows = []
        for pid in sorted(common):
            p, q = dist(arms[base][pid]), dist(arms[j][pid])
            rows.append((arms[base][pid]["target_tokens"],
                         kl(p, q),
                         arms[base][pid]["chosen"] == arms[j][pid]["chosen"]))
        by_len = {}
        for tl, d, same in rows:
            by_len.setdefault(tl, []).append((d, same))
        print("=== %s  vs  %s ===" % (names[base], names[j]))
        print("%10s %3s %10s %9s %10s" % ("prompt tok", "n", "median KL", "max KL", "top1 same"))
        for tl in sorted(by_len):
            vals = sorted(d for d, _ in by_len[tl])
            same = sum(1 for _, s in by_len[tl] if s)
            med = vals[len(vals) // 2]
            print("%10d %3d %10.5f %9.5f %6s/%d" % (
                tl, len(vals), med, vals[-1], same, len(by_len[tl])))
        allv = sorted(d for _tl, d, _s in rows)
        print("%10s %3d %10.5f %9.5f %6s/%d\n" % (
            "ALL", len(allv), allv[len(allv) // 2], allv[-1],
            sum(1 for _, _, s in rows if s), len(rows)))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build")
    b.add_argument("--runs", default=os.path.join(ROOT, "runs"))
    b.add_argument("--out", default="probes.jsonl")
    b.add_argument("--lengths", default="4000,16000,48000,100000")
    b.add_argument("--per-length", type=int, default=5)
    b.set_defaults(func=cmd_build)

    r = sub.add_parser("run")
    r.add_argument("--probes", default="probes.jsonl")
    r.add_argument("--arm", choices=["akash", "rig"], required=True)
    r.add_argument("--label")
    r.add_argument("--base-url", default="http://127.0.0.1:18000/v1")
    r.add_argument("--out", required=True)
    r.add_argument("--resume", action="store_true")
    r.set_defaults(func=cmd_run)

    c = sub.add_parser("compare")
    c.add_argument("files", nargs="+")
    c.set_defaults(func=cmd_compare)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
