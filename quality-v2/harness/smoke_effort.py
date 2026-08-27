#!/usr/bin/env python3
"""Smoke: does reasoning effort actually reach the Qwen3.8-27B on AkashML?

Tries both transports for every effort level and reports reasoning-token
counts. Expectation if the knob works: reasoning_tokens grows monotonically
low -> medium -> xhigh, and 'off' produces none.

Verdict is written to runs/smoke-effort/<ts>/ with full traces.
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import or_client  # noqa: E402

PROMPT = ("A bag has 5 red, 7 blue and 8 green balls. Three are drawn "
          "without replacement. What is the probability all three are "
          "different colors? Give the final answer as a fraction.")

EFFORTS = ["off", "low", "medium", "xhigh"]
MODES = ["raw", "openrouter"]


def main():
    ts = time.strftime("%Y%m%dT%H%M%S")
    out = Path(__file__).resolve().parent.parent / "runs" / "smoke-effort" / ts
    out.mkdir(parents=True)
    rows = []
    for mode in MODES:
        for eff in EFFORTS:
            if eff == "off" and mode == "openrouter":
                continue  # off is transport-independent, test once
            tag = f"{mode}-{eff}"
            print(f"--- {tag} ...", flush=True)
            res = or_client.chat(
                [{"role": "user", "content": PROMPT}], eff, effort_mode=mode)
            (out / f"{tag}.json").write_text(
                json.dumps(res, indent=2, ensure_ascii=False))
            s = or_client.usage_summary(res)
            s["tag"] = tag
            s["error"] = res["error"]
            rows.append(s)
            print(json.dumps(s), flush=True)
    (out / "summary.json").write_text(json.dumps(rows, indent=2))
    print(f"\nsaved: {out}")
    # quick verdict
    def rt(tag):
        for r in rows:
            if r["tag"] == tag:
                return r.get("reasoning_tokens") or 0
        return None
    for mode in MODES:
        seq = [rt(f"{mode}-{e}") for e in ("low", "medium", "xhigh")]
        ok = None not in seq and seq[0] < seq[2]
        print(f"{mode}: low/med/xhigh reasoning tokens = {seq} "
              f"{'-> knob WORKS' if ok else '-> knob unclear'}")


if __name__ == "__main__":
    main()
