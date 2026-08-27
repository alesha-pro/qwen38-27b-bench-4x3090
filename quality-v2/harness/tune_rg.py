#!/usr/bin/env python3
"""Dry-run inspection of the harder RG configs, then emit the tuning pool.

--inspect : generate and print samples + self-verification, NO api calls.
            Checks that every generated item is solvable by its own verifier
            (feed the reference answer back into score_answer -> must be 1.0)
            and reports prompt sizes.
--emit    : write dev-pool/devpool-rg-v2.jsonl (12 tasks x tuned families)
"""
import argparse
import json
import sys
from pathlib import Path

import reasoning_gym

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rg_configs  # noqa: E402
from rg_configs import RG_V2, TUNED_FAMILIES  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DEV_SEED = 20260822
PER_FAMILY = 12

# Which config dict and which families this invocation works on.
CONFIGS = RG_V2
FAMILIES = TUNED_FAMILIES
ID_PREFIX = "rg2"


def make(family, size=PER_FAMILY, seed=DEV_SEED):
    return reasoning_gym.create_dataset(family, size=size, seed=seed,
                                        **CONFIGS[family])


def inspect():
    for fam in FAMILIES:
        print(f"\n{'='*70}\n{fam}  config={CONFIGS[fam]}\n{'='*70}")
        try:
            ds = make(fam)
        except Exception as e:
            print(f"  !! GENERATOR FAILED: {type(e).__name__}: {e}")
            continue
        items = list(ds)
        selfcheck = []
        for it in items:
            entry = {k: v for k, v in it.items()}
            # Some families (graph_color) have no single reference answer:
            # many solutions are valid, the reference lives in metadata.
            ref = it["answer"]
            if ref is None:
                pa = (it.get("metadata") or {}).get("possible_answer")
                ref = json.dumps({str(k): v for k, v in pa.items()}) if pa \
                    else None
            try:
                s = float(ds.score_answer(answer=str(ref), entry=entry))
            except Exception as e:
                s = f"ERR {type(e).__name__}"
            selfcheck.append(s)
        infeasible = sum(1 for it in items
                         if str(it["answer"]).strip().lower() == "infeasible")
        ok = sum(1 for s in selfcheck if s == 1.0)
        lens = [len(it["question"]) for it in items]
        print(f"  generated {len(items)}, self-verify pass {ok}/{len(items)}"
              f"  (must be all 1.0 -> tasks are solvable & scorable)")
        print(f"  prompt chars: min {min(lens)} / median "
              f"{sorted(lens)[len(lens)//2]} / max {max(lens)}")
        if infeasible:
            print(f"  degenerate-answer check: {infeasible}/{len(items)} "
                  f"answer 'infeasible' (guessable modal answer if high)")
        if ok != len(items):
            print(f"  !! selfcheck values: {selfcheck}")
        q = items[0]["question"]
        print(f"  --- sample ---\n  {q[:600]}")
        print(f"  --- answer: {str(items[0]['answer'])[:120]}")


def emit(outname):
    out = ROOT / "dev-pool" / outname
    tasks = []
    for fam in FAMILIES:
        ds = make(fam)
        for i, item in enumerate(ds):
            tasks.append({
                "id": f"{ID_PREFIX}-{fam}-{i:03d}",
                "block": "quant-core-rg",
                "family": fam,
                "prompt": item["question"],
                "answer_meta": {
                    "answer": item["answer"],
                    "entry": {k: v for k, v in item.items()
                              if k != "question"},
                    "scorer": "reasoning_gym.score_answer",
                },
                "source": {"kind": "reasoning_gym", "seed": DEV_SEED,
                           "index": i, "config_version": ID_PREFIX,
                           "gen_config": CONFIGS[fam]},
            })
    with out.open("w") as fh:
        for t in tasks:
            fh.write(json.dumps(t, ensure_ascii=False, default=str) + "\n")
    print(f"wrote {len(tasks)} tasks -> {out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--inspect", action="store_true")
    ap.add_argument("--emit", metavar="OUTFILE",
                    help="write pool to dev-pool/OUTFILE")
    ap.add_argument("--set", default="v2", choices=["v2", "ease", "final"],
                    help="which config set to use")
    a = ap.parse_args()
    if a.set == "ease":
        CONFIGS = rg_configs.RG_EASE
        FAMILIES = list(rg_configs.RG_EASE)
        ID_PREFIX = "rge"
    elif a.set == "final":
        CONFIGS = rg_configs.RG_FINAL
        FAMILIES = list(rg_configs.RG_FINAL)
        ID_PREFIX = "rg"
    globals().update(CONFIGS=CONFIGS, FAMILIES=FAMILIES, ID_PREFIX=ID_PREFIX)
    if a.inspect:
        inspect()
    if a.emit:
        emit(a.emit)
