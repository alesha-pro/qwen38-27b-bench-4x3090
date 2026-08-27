#!/usr/bin/env python3
"""Does the 'think harder' knob actually work on the local server?

Cheap version: cap the output at 4k tokens. We do not need the full answer,
only whether the model is STILL thinking when it hits the cap. If low stops
early and xhigh runs into the cap, the knob works.
"""
import json, time, urllib.request

ROOT = "/mnt/nvme/work/benchmarks/quant-bench-v2"
URL = "http://127.0.0.1:18000/v1/chat/completions"
CAP = 4000
SAMPLING = {"temperature": 1.0, "top_p": 0.95, "top_k": 20,
            "presence_penalty": 0.0, "repetition_penalty": 1.0}

Q = ("Let S be the set of positive integers n < 10000 such that n^2 + 1 is "
     "divisible by a prime p with p ≡ 1 (mod 8) and n is not divisible by 3. "
     "Estimate |S| and justify the estimate carefully, then compute the exact "
     "value for n < 200 by direct verification.")


def call(tag, extra):
    body = {"model": "qwen3.8-27b",
            "messages": [{"role": "user", "content": Q}],
            "max_tokens": CAP, **SAMPLING}
    body.update(extra)
    req = urllib.request.Request(URL, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=900) as r:
            d = json.loads(r.read())
    except Exception as e:
        print("%-44s ERROR %s" % (tag, str(e)[:70]))
        return
    lat = time.time() - t0
    msg = d["choices"][0]["message"]
    think = msg.get("reasoning_content") or msg.get("reasoning") or ""
    u = d.get("usage") or {}
    n = u.get("completion_tokens") or 0
    fin = d["choices"][0].get("finish_reason")
    print("%-44s %6d tok  think %6d ch  %-8s %5.1f tok/s"
          % (tag, n, len(think), fin, n / lat if lat else 0))


print("cap = %d tokens. 'length' finish means the model was still going.\n" % CAP)
print("%-44s %10s %14s %9s %10s" % ("variant", "completion", "think chars", "finish", "speed"))
call("no effort field at all", {})
for eff in ("low", "xhigh"):
    call("top-level  reasoning_effort=%s" % eff, {"reasoning_effort": eff})
    call("template   reasoning_effort=%s" % eff,
         {"chat_template_kwargs": {"reasoning_effort": eff}})
