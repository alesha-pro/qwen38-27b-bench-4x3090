#!/usr/bin/env python3
"""Build a one-shot difficulty probe: several levels per family, 12 tasks each.

Single repeat is intentional. The probe only has to tell levels apart
(1.00 vs ~0.8 vs ~0.6); the winning level is confirmed with 3 repeats on the
frozen final set. Levels that the generator cannot produce in reasonable time
were dropped by the dry-run sweep (graph_color p>=0.30, zebra >7 people).
"""
import json
from pathlib import Path

import reasoning_gym

ROOT = Path(__file__).resolve().parent.parent
SEED = 20260822

PROBE = {
    # family: [(level tag, config)]
    "graph_color": [("L2", dict(min_num_vertices=22, max_num_vertices=26,
                                edge_probability=0.25, num_colors=3))],
    "zebra_puzzles": [("L2", dict(num_people=7, num_characteristics=7))],
    "cryptarithm": [("L2", dict(min_words=5, max_words=7)),
                    ("L3", dict(min_words=8, max_words=10))],
    "shortest_path": [("L2", dict(min_rows=20, max_rows=24, min_cols=20,
                                  max_cols=24, p_blocked=0.25)),
                      ("L3", dict(min_rows=28, max_rows=32, min_cols=28,
                                  max_cols=32, p_blocked=0.28))],
    "intermediate_integration": [
        ("L2", dict(problem_types=("cyclic", "repeated_parts"),
                    problem_type_weights=[0.5, 0.5],
                    min_poly_degree=3, max_poly_degree=6,
                    min_linear_degree=4, max_linear_degree=8))],
    "number_sequence": [("L2", dict(min_terms=6, max_terms=10,
                                    max_complexity=5, min_value=-500,
                                    max_value=500))],
    "propositional_logic": [("L2", dict(min_vars=4, max_vars=6,
                                        min_statements=4, max_statements=6,
                                        min_complexity=2, max_complexity=4))],
    "jugs": [("L2", dict(num_jugs=4, difficulty=15))],
}


def main():
    tasks = []
    for fam, levels in PROBE.items():
        for tag, cfg in levels:
            ds = reasoning_gym.create_dataset(fam, size=12, seed=SEED, **cfg)
            for i, item in enumerate(ds):
                tasks.append({
                    "id": f"pr-{fam}-{tag}-{i:03d}",
                    "block": "quant-core-rg",
                    "family": f"{fam}::{tag}",
                    "prompt": item["question"],
                    "answer_meta": {
                        "answer": item["answer"],
                        "entry": {k: v for k, v in item.items()
                                  if k != "question"},
                        "scorer": "reasoning_gym.score_answer",
                    },
                    "source": {"kind": "reasoning_gym", "seed": SEED,
                               "index": i, "rg_family": fam, "level": tag,
                               "gen_config": cfg},
                })
            print(f"{fam} {tag}: 12 tasks", flush=True)
    out = ROOT / "dev-pool" / "devpool-probe.jsonl"
    with out.open("w") as fh:
        for t in tasks:
            fh.write(json.dumps(t, ensure_ascii=False, default=str) + "\n")
    print(f"wrote {len(tasks)} -> {out}")


if __name__ == "__main__":
    main()
