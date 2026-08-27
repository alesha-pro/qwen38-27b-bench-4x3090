#!/usr/bin/env python3
"""Build the quant-bench-v2 DEV pool (~250 tasks).

Composition (decisions 2026-08-22):
  Reasoning Gym  10 families x 12 = 120   (procedural, exact verifiers)
  MathArena 2026 20                        (AIME 2026 + HMMT Feb 2026)
  IFBench        60                        (programmatic constraint checks)
  BFCL v4        50                        (single-turn tool calling slices)

Dev seeds are fixed here. The FINAL test set will be generated later from
disjoint seeds / disjoint IDs after BF16 calibration — never from this file's
results by hand-picking items.

Output: dev-pool/devpool.jsonl + dev-pool/MANIFEST.json
Each line: {id, block, family, prompt OR messages, tools?, answer_meta,
            source, gen_config}
"""
import hashlib
import json
import random
from pathlib import Path

import reasoning_gym

ROOT = Path(__file__).resolve().parent.parent
DS = Path("/mnt/nvme2/datasets/local-quant-bench-v2")
OUT = ROOT / "dev-pool"
DEV_SEED = 20260822

RG_FAMILIES = [
    "cryptarithm", "graph_color", "jugs", "word_ladder", "number_sequence",
    "shortest_path", "zebra_puzzles", "propositional_logic", "rush_hour",
    "intermediate_integration",
]
RG_PER_FAMILY = 12

PINS = {
    "reasoning_gym": "49b07130b3fcd12f2d064bba7c43869543a0e7e7 (pip 0.1.19 editable)",
    "ifbench": "db69a6f05689830b0068b8f1529ebcfd2f3b164c",
    "matharena_aime_2026_hf": "d2de22f3c656b4f56cf8981212186377d1e23bc3",
    "matharena_hmmt_feb_2026_hf": "02fba4f74d8e68e73e66a02d540fd979c05c274c",
    "bfcl": "6ea57973c7a6097fd7c5915698c54c17c5b1b6c8",
}


def rg_tasks():
    tasks = []
    for fam in RG_FAMILIES:
        ds = reasoning_gym.create_dataset(fam, size=RG_PER_FAMILY,
                                          seed=DEV_SEED)
        for i, item in enumerate(ds):
            tasks.append({
                "id": f"rg-{fam}-{i:03d}",
                "block": "quant-core-rg",
                "family": fam,
                "prompt": item["question"],
                "answer_meta": {
                    "answer": item["answer"],
                    "entry": {k: v for k, v in item.items()
                              if k not in ("question",)},
                    "scorer": "reasoning_gym.score_answer",
                },
                "source": {"kind": "reasoning_gym", "seed": DEV_SEED,
                           "index": i, "pin": PINS["reasoning_gym"]},
            })
    return tasks


def matharena_tasks():
    import pandas as pd
    frames = []
    for name, key in (("aime_2026", "matharena_aime_2026_hf"),
                      ("hmmt_feb_2026", "matharena_hmmt_feb_2026_hf")):
        pq = list((DS / "hf" / f"MathArena__{name}" / "data").glob("*.parquet"))
        df = pd.read_parquet(pq[0])
        df["__comp"] = name
        df["__pin"] = PINS[key]
        frames.append(df)
    allp = pd.concat(frames, ignore_index=True)
    rng = random.Random(DEV_SEED)
    # 10 from each competition, spread over problem indices
    tasks = []
    for comp, grp in allp.groupby("__comp"):
        grp = grp.reset_index(drop=True)
        idx = sorted(rng.sample(range(len(grp)), min(10, len(grp))))
        for i in idx:
            row = grp.iloc[i]
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
                           "problem_idx": int(pid) if str(pid).isdigit() else str(pid),
                           "pin": str(row["__pin"])},
            })
    return tasks


def ifbench_tasks():
    lines = (DS / "repos/ifbench/data/IFBench_test.jsonl").read_text().splitlines()
    rng = random.Random(DEV_SEED)
    picks = sorted(rng.sample(range(len(lines)), min(60, len(lines))))
    tasks = []
    for i in picks:
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


BFCL_SLICES = {  # single-turn categories only; counts sum to 50
    "simple_python": 10,
    "multiple": 10,
    "live_simple": 10,
    "live_multiple": 10,
    "irrelevance": 5,
    "live_parallel_multiple": 5,
}


def bfcl_tasks():
    base = DS / "repos/bfcl/berkeley-function-call-leaderboard/bfcl_eval/data"
    rng = random.Random(DEV_SEED)
    tasks = []
    for cat, n in BFCL_SLICES.items():
        f = base / f"BFCL_v4_{cat}.json"
        lines = f.read_text().splitlines()
        ans_file = base / "possible_answer" / f"BFCL_v4_{cat}.json"
        answers = {}
        if ans_file.exists():
            for ln in ans_file.read_text().splitlines():
                if ln.strip():
                    a = json.loads(ln)
                    answers[a["id"]] = a.get("ground_truth")
        picks = sorted(rng.sample(range(len(lines)), min(n, len(lines))))
        for i in picks:
            rec = json.loads(lines[i])
            tasks.append({
                "id": f"bfcl-{rec['id']}",
                "block": "tool-calling",
                "family": f"bfcl_{cat}",
                "messages": rec["question"],
                "tools_raw": rec.get("function"),
                "answer_meta": {"ground_truth": answers.get(rec["id"]),
                                "scorer": "bfcl_ast",
                                "category": cat},
                "source": {"kind": "bfcl", "category": cat, "line": i,
                           "pin": PINS["bfcl"]},
            })
    return tasks


def main():
    OUT.mkdir(exist_ok=True)
    pool = rg_tasks() + matharena_tasks() + ifbench_tasks() + bfcl_tasks()
    ids = [t["id"] for t in pool]
    assert len(ids) == len(set(ids)), "duplicate task ids"
    out = OUT / "devpool.jsonl"
    with out.open("w") as fh:
        for t in pool:
            fh.write(json.dumps(t, ensure_ascii=False, default=str) + "\n")
    counts = {}
    for t in pool:
        counts[t["block"]] = counts.get(t["block"], 0) + 1
    manifest = {
        "built": "2026-08-22",
        "dev_seed": DEV_SEED,
        "total": len(pool),
        "counts": counts,
        "pins": PINS,
        "sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
        "note": ("DEV pool for BF16 calibration. Final test set must use "
                 "disjoint seeds/IDs, frozen before any quant runs."),
    }
    (OUT / "MANIFEST.json").write_text(json.dumps(manifest, indent=2))
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
