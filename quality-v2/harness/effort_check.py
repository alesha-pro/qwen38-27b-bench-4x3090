#!/usr/bin/env python3
"""Anti-fake check: verify reasoning_effort actually reaches the local model.

Forcing a reasoning mode the wrong way silently routes the chain of thought
into a truncated channel and produces a plausible-looking but meaningless run.

Gate design (rewritten 2026-08-24 after the old gate produced a false FAIL):
the old version compared xhigh against off on a three-step arithmetic problem
and demanded an absolute 500 chars of thinking. Both halves were wrong.
  - off vs xhigh only proves the thinking channel toggles, and that toggle
    goes through enable_thinking in the chat template, not through effort.
  - an easy task legitimately gives a short xhigh trace; the old run failed on
    495 chars against a 500 floor while the knob was in fact working.
So: compare LOW against XHIGH (the actual gradient), on a real pool task where
the paid reference showed a large gradient, with no output cap. Measured
2026-08-24 on BF16 weights: rg-propositional_logic-001 gave 400 -> 9938
completion tokens (24.8x), against the reference's 500 -> 12331 (24.7x).

For the record, the knob is only a system-prompt line: Qwen3.8's chat template
accepts low | medium | xhigh (xhigh is the DEFAULT, medium injects no system
message at all), and raises on high / max / none.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import or_client
from run_devpool import build_request
import json

ROOT = "$RUN_ROOT/quant-bench-v2"
# Reference gradient at xhigh/low, from runs/ref-final-efforts + ref-final.
PROBE = "rg-propositional_logic-001"
REF_LOW, REF_XHIGH = 500, 12331
MIN_RATIO = 2.0


def probe(task, effort):
    msgs, tools = build_request(task)
    r = or_client.chat(msgs, effort, effort_mode="raw", tools=tools,
                       max_tokens=131072, timeout=3600, retries=2)
    if r["error"]:
        print(f"  {effort}: ERROR {r['error'][:200]}")
        return None
    ch = r["response"]["choices"][0]
    msg = ch["message"]
    think = msg.get("reasoning_content") or msg.get("reasoning") or ""
    u = r["response"].get("usage") or {}
    n = u.get("completion_tokens") or 0
    print(f"  {effort:<6} completion={n:>7} thinking_chars={len(think):>7} "
          f"answer_chars={len(msg.get('content') or ''):>6} "
          f"finish={ch.get('finish_reason')}")
    if ch.get("finish_reason") == "length":
        print("  !! hit the output ceiling - the gradient is hidden, raise it")
    return n


pool = {json.loads(l)["id"]: json.loads(l)
        for l in open(f"{ROOT}/final-pool/canarypool.jsonl", encoding="utf-8")}
if PROBE not in pool:
    sys.exit(f"probe task {PROBE} is not in the canary pool")

print(f"effort gradient on {PROBE} (reference: {REF_LOW} -> {REF_XHIGH} tok, "
      f"{REF_XHIGH / REF_LOW:.1f}x):")
lo = probe(pool[PROBE], "low")
xh = probe(pool[PROBE], "xhigh")
if not lo or not xh:
    sys.exit("probe failed")
ratio = xh / lo
if ratio < MIN_RATIO:
    sys.exit(f"FAIL: xhigh/low = {ratio:.2f}x (need >= {MIN_RATIO}x). The "
             f"effort knob is not reaching the model; the reference saw "
             f"{REF_XHIGH / REF_LOW:.1f}x on this task.")
print(f"OK: xhigh spends {ratio:.1f}x the tokens of low "
      f"(reference {REF_XHIGH / REF_LOW:.1f}x on the same task)")
