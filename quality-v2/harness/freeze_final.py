#!/usr/bin/env python3
"""Freeze the FINAL test set for quant-bench-v2.

Rules enforced here (protocol, 2026-08-22/23):
- RG tasks are generated from a FINAL seed disjoint from the dev seed, using
  the difficulty configs chosen during calibration. Never hand-picked.
- Static tasks are sampled from IDs NOT used in the dev pool (disjoint), by
  strata chosen during calibration. Never hand-picked.
- The manifest records which reference model the difficulty was calibrated
  against, so the set can be re-tuned for another model later.

Composition is declared in FINAL_SPEC below and is the only place to edit.
"""
import hashlib
import json
import random
from pathlib import Path

import reasoning_gym
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rg_configs import RG_FINAL  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DS = Path("/mnt/nvme2/datasets/local-quant-bench-v2")
OUT = ROOT / "final-pool"

FINAL_SEED = 20260823          # disjoint from DEV_SEED 20260822
DEV_SEED = 20260822

CALIBRATED_AGAINST = {
    "model": "qwen/qwen3.8-27b",
    "precision": "bf16",
    "endpoint": "OpenRouter/AkashML (pinned)",
    "effort": "xhigh",
    "target_band": "70-85% per family",
    "runs": ["calib-xhigh (250 tasks x3)", "calib-rg-v2 (60 tasks x3)"],
}

# family -> count in the final set. Filled from calibration results.
# Chosen from calibration (BF16 xhigh pooled rates in brackets).
# Static sources cannot be tuned, so difficulty is set by re-weighting strata:
# saturated strata (aime 1.00, bfcl simple_python/multiple 1.00) are dropped or
# kept only as a small share.
FINAL_SPEC = {
    # RG families chosen for BOTH discrimination and cost. Rates are BF16
    # xhigh pooled; median completion tokens decide whether a family is
    # affordable on the rig (a quant at ~60 tok/s pays a minute per 3.6K).
    # Dropped: graph_color and zebra_puzzles (1.00 at the generator ceiling),
    # cryptarithm and shortest_path (1.00 until they cost 9-31K tokens),
    # jugs (0.86 but 26.8K tokens per task).
    "rg": {"intermediate_integration": 10,  # [0.89]    920 tok
           "propositional_logic": 10,       # [0.89]  2 424 tok
           "word_ladder": 8,                # [0.86]  2 097 tok
           "number_sequence": 8,            # [0.92]  1 594 tok
           "rush_hour": 4},                 # [0.91] 14 916 tok, kept small
    "matharena": {"hmmt_feb_2026": 12,   # [0.70]
                  "aime_2026": 4},        # [1.00] small share on purpose
    "ifbench": 20,                        # [0.77] already in band
    "bfcl": {"live_multiple": 8,          # [0.83]
             "live_simple": 8,            # [0.70]
             "irrelevance": 4,            # [0.67]
             "live_parallel_multiple": 4},# [0.60]
}

PINS = {
    "reasoning_gym": "49b07130b3fcd12f2d064bba7c43869543a0e7e7 (pip 0.1.19)",
    "ifbench": "db69a6f05689830b0068b8f1529ebcfd2f3b164c",
    "matharena_aime_2026_hf": "d2de22f3c656b4f56cf8981212186377d1e23bc3",
    "matharena_hmmt_feb_2026_hf": "02fba4f74d8e68e73e66a02d540fd979c05c274c",
    "bfcl": "6ea57973c7a6097fd7c5915698c54c17c5b1b6c8",
}


def dev_ids():
    """IDs already used in the dev pool, to keep the final set disjoint."""
    used = {"matharena": set(), "ifbench": set(), "bfcl": set()}
    for p in ("dev-pool/devpool.jsonl", "dev-pool/devpool-rg-v2.jsonl"):
        f = ROOT / p
        if not f.exists():
            continue
        for line in f.open():
            t = json.loads(line)
            src = t.get("source", {})
            kind = src.get("kind")
            if kind == "matharena":
                used["matharena"].add(t["id"])
            elif kind == "ifbench":
                used["ifbench"].add(src.get("line"))
            elif kind == "bfcl":
                used["bfcl"].add(t["id"].replace("bfcl-", ""))
    return used


def rg_tasks(spec):
    tasks = []
    for fam, n in spec.items():
        cfg = RG_FINAL[fam]
        ds = reasoning_gym.create_dataset(fam, size=n, seed=FINAL_SEED, **cfg)
        for i, item in enumerate(ds):
            tasks.append({
                "id": f"rg-{fam}-{i:03d}",
                "block": "quant-core-rg",
                "family": fam,
                "prompt": item["question"],
                "answer_meta": {
                    "answer": item["answer"],
                    "entry": {k: v for k, v in item.items()
                              if k != "question"},
                    "scorer": "reasoning_gym.score_answer",
                },
                "source": {"kind": "reasoning_gym", "seed": FINAL_SEED,
                           "index": i, "gen_config": cfg,
                           "pin": PINS["reasoning_gym"]},
            })
    return tasks


def matharena_tasks(spec, used):
    import pandas as pd
    tasks = []
    rng = random.Random(FINAL_SEED)
    for comp, n in spec.items():
        key = f"matharena_{comp}_hf"
        pq = list((DS / "hf" / f"MathArena__{comp}" / "data").glob("*.parquet"))
        df = pd.read_parquet(pq[0]).reset_index(drop=True)
        cands = [i for i in range(len(df))
                 if f"ma-{comp}-{df.iloc[i].get('problem_idx', i)}"
                 not in used["matharena"]]
        if len(cands) < n:
            raise SystemExit(f"{comp}: only {len(cands)} unused items, need {n}")
        for i in sorted(rng.sample(cands, n)):
            row = df.iloc[i]
            pid = row.get("problem_idx", i)
            tasks.append({
                "id": f"ma-{comp}-{pid}",
                "block": "quant-core-math",
                "family": comp,
                "prompt": (str(row["problem"]) +
                           "\n\nPut your final answer within \\boxed{}."),
                "answer_meta": {"answer": str(row["answer"]),
                                "scorer": "boxed_exact"},
                "source": {"kind": "matharena", "competition": comp,
                           "pin": PINS[key]},
            })
    return tasks


def ifbench_tasks(n, used):
    lines = (DS / "repos/ifbench/data/IFBench_test.jsonl").read_text().splitlines()
    cands = [i for i in range(len(lines)) if i not in used["ifbench"]]
    rng = random.Random(FINAL_SEED)
    tasks = []
    for i in sorted(rng.sample(cands, n)):
        rec = json.loads(lines[i])
        tasks.append({
            "id": f"if-{rec.get('key', i)}",
            "block": "quant-core-if",
            "family": "ifbench",
            "prompt": rec["prompt"],
            "answer_meta": {
                "instruction_id_list": rec.get("instruction_id_list"),
                "kwargs": rec.get("kwargs"),
                "scorer": "ifbench_strict",
            },
            "source": {"kind": "ifbench", "line": i, "pin": PINS["ifbench"]},
        })
    return tasks


def bfcl_tasks(spec, used):
    base = DS / "repos/bfcl/berkeley-function-call-leaderboard/bfcl_eval/data"
    rng = random.Random(FINAL_SEED)
    tasks = []
    for cat, n in spec.items():
        lines = (base / f"BFCL_v4_{cat}.json").read_text().splitlines()
        ans_file = base / "possible_answer" / f"BFCL_v4_{cat}.json"
        answers = {}
        if ans_file.exists():
            for ln in ans_file.read_text().splitlines():
                if ln.strip():
                    a = json.loads(ln)
                    answers[a["id"]] = a.get("ground_truth")
        cands = []
        for i in range(len(lines)):
            rid = json.loads(lines[i])["id"]
            if rid not in used["bfcl"]:
                cands.append(i)
        if len(cands) < n:
            raise SystemExit(f"bfcl {cat}: {len(cands)} unused, need {n}")
        for i in sorted(rng.sample(cands, n)):
            rec = json.loads(lines[i])
            tasks.append({
                "id": f"bfcl-{rec['id']}",
                "block": "tool-calling",
                "family": f"bfcl_{cat}",
                "messages": rec["question"],
                "tools_raw": rec.get("function"),
                "answer_meta": {"ground_truth": answers.get(rec["id"]),
                                "scorer": "bfcl_ast", "category": cat},
                "source": {"kind": "bfcl", "category": cat,
                           "pin": PINS["bfcl"]},
            })
    return tasks


def main():
    OUT.mkdir(exist_ok=True)
    used = dev_ids()
    pool = (rg_tasks(FINAL_SPEC["rg"])
            + matharena_tasks(FINAL_SPEC["matharena"], used)
            + ifbench_tasks(FINAL_SPEC["ifbench"], used)
            + bfcl_tasks(FINAL_SPEC["bfcl"], used))
    ids = [t["id"] for t in pool]
    assert len(ids) == len(set(ids)), "duplicate ids in final pool"

    out = OUT / "finalpool.jsonl"
    with out.open("w") as fh:
        for t in pool:
            fh.write(json.dumps(t, ensure_ascii=False, default=str) + "\n")

    counts = {}
    for t in pool:
        counts.setdefault(t["block"], {})
        counts[t["block"]][t["family"]] = \
            counts[t["block"]].get(t["family"], 0) + 1
    manifest = {
        "frozen": "2026-08-23",
        "final_seed": FINAL_SEED,
        "dev_seed_excluded": DEV_SEED,
        "total": len(pool),
        "counts": counts,
        "rg_configs": {f: RG_FINAL[f] for f in FINAL_SPEC["rg"]},
        "calibrated_against": CALIBRATED_AGAINST,
        "pins": PINS,
        "sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
        "disjoint_from_dev": {k: len(v) for k, v in used.items()},
    }
    (OUT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2,
                                                  default=str))
    print(json.dumps(manifest, indent=2, default=str))


if __name__ == "__main__":
    main()
