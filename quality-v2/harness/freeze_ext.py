#!/usr/bin/env python3
"""Extend the frozen quant-bench-v2 suite from 100 to 300 tasks.

Why: the 100-task suite resolves the paired pass-rate difference only to
about +-4 pp, so FP8 landed at -2.3 pp [-6.7, +1.7] and nothing could be
said. 300 tasks take the standard error to ~1.2 pp.

Rules kept from freeze_final.py (same protocol):
- new seed, disjoint from the dev seed AND from the frozen 100
- static items sampled from IDs not used in dev, final or canary pools
- no hand-picking, composition declared once in EXT_SPEC
- sha256 manifest written before any arm is run

Deliberate deviations, both forced by the pools and both recorded here:
- aime_2026 gets 0 new tasks. The reference solves it at 1.00, so those
  tasks cannot register a loss and only shrink the estimate.
- hmmt_feb_2026 gets 11, which is the whole remaining pool. Math therefore
  drops from 16% to 9% of the suite. The freed budget goes to ifbench and
  bfcl, the families sitting closest to the 0.6-0.9 discriminating band.
"""
import hashlib
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import freeze_final as ff  # noqa: E402

EXT_SEED = 20260824        # static sources only (matharena/ifbench/bfcl)
RG_INDEX_OFFSET = 100      # keeps ids disjoint from the frozen 100

# reasoning_gym gotcha, measured 24.08: adjacent seeds do NOT give independent
# task streams. seed 20260824 reproduced the seed-20260823 sequence shifted by
# one item, so a "new seed" would have silently re-issued the frozen tasks.
# Instead we keep the ORIGINAL seed and take the TAIL of the same stream: the
# stream is size-independent and its head reproduces the frozen 40 exactly, so
# the tail is provably disjoint and drawn from an identical distribution.

EXT_SPEC = {
    "rg": {"intermediate_integration": 20,   # [0.89]    920 tok
           "propositional_logic": 20,        # [0.89]  2 424 tok
           "word_ladder": 16,                # [0.86]  2 097 tok
           "number_sequence": 20,            # [0.92]  1 594 tok
           "rush_hour": 4},                  # [0.91] 14 916 tok, kept tiny
    "matharena": {"hmmt_feb_2026": 11},      # [0.70] whole remaining pool
    "ifbench": 49,                           # [0.77]
    "bfcl": {"live_multiple": 20,            # [0.83]
             "live_simple": 20,              # [0.70]
             "irrelevance": 8,               # [0.67]
             "live_parallel_multiple": 12},  # [0.60] best discriminator
}

ROOT = Path("/mnt/nvme/work/benchmarks/quant-bench-v2")
OUT = ROOT / "final-pool"


def used_ids():
    """Everything already spent: dev, frozen final, and the canary pool."""
    used = {"matharena": set(), "ifbench": set(), "bfcl": set()}
    for p in ("dev-pool/devpool.jsonl", "dev-pool/devpool-rg-v2.jsonl",
              "final-pool/finalpool.jsonl", "final-pool/canarypool.jsonl"):
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


def rg_tail_tasks(spec):
    """Fresh RG tasks: same generator, same seed, items past the frozen head."""
    import reasoning_gym
    frozen = {}
    for line in (OUT / "finalpool-rg.jsonl").open():
        t = json.loads(line)
        frozen.setdefault(t["family"], []).append(t["prompt"])

    tasks = []
    for fam, n in spec.items():
        cfg = ff.RG_FINAL[fam]
        head = frozen[fam]
        ds = list(reasoning_gym.create_dataset(
            fam, size=len(head) + n * 4, seed=ff.FINAL_SEED, **cfg))
        assert [it["question"] for it in ds[:len(head)]] == head, \
            f"{fam}: stream no longer reproduces the frozen head"
        seen, picked = set(head), []
        for i, item in enumerate(ds[len(head):], start=len(head)):
            if item["question"] in seen:      # families repeat items
                continue
            seen.add(item["question"])
            picked.append((i, item))
            if len(picked) == n:
                break
        assert len(picked) == n, f"{fam}: only {len(picked)} fresh items"
        for i, item in picked:
            tasks.append({
                "id": f"rg-{fam}-{i + RG_INDEX_OFFSET:03d}",
                "block": "quant-core-rg",
                "family": fam,
                "prompt": item["question"],
                "answer_meta": {
                    "answer": item["answer"],
                    "entry": {k: v for k, v in item.items()
                              if k != "question"},
                    "scorer": "reasoning_gym.score_answer",
                },
                "source": {"kind": "reasoning_gym", "seed": ff.FINAL_SEED,
                           "index": i, "stream_tail": True,
                           "gen_config": cfg, "pin": ff.PINS["reasoning_gym"]},
            })
    return tasks


def main():
    used = used_ids()
    rg = rg_tail_tasks(EXT_SPEC["rg"])

    ff.FINAL_SEED = EXT_SEED          # static samplers read this global
    pool = (rg
            + ff.matharena_tasks(EXT_SPEC["matharena"], used)
            + ff.ifbench_tasks(EXT_SPEC["ifbench"], used)
            + ff.bfcl_tasks(EXT_SPEC["bfcl"], used))

    old = [json.loads(l) for l in (OUT / "finalpool.jsonl").open()]
    old_ids = {t["id"] for t in old}
    old_prompts = {t.get("prompt") for t in old if t.get("prompt")}

    ids = [t["id"] for t in pool]
    assert len(ids) == len(set(ids)), "duplicate ids inside the extension"
    clash = old_ids & set(ids)
    assert not clash, f"ids collide with the frozen 100: {sorted(clash)[:5]}"
    dup = [t["id"] for t in pool
           if t.get("prompt") and t["prompt"] in old_prompts]
    assert not dup, f"generated prompt already in the frozen 100: {dup[:5]}"

    out = OUT / "extpool.jsonl"
    with out.open("w") as fh:
        for t in pool:
            fh.write(json.dumps(t, ensure_ascii=False, default=str) + "\n")

    counts = {}
    for t in pool:
        counts.setdefault(t["block"], {})
        counts[t["block"]][t["family"]] = \
            counts[t["block"]].get(t["family"], 0) + 1
    combined = {}
    for t in old + pool:
        combined[t["block"]] = combined.get(t["block"], 0) + 1

    manifest = {
        "frozen": "2026-08-24",
        "purpose": "raise the 100-task suite to 300 for a resolvable "
                   "paired pass-rate difference (SE ~4.2pp -> ~1.2pp)",
        "ext_seed": EXT_SEED,
        "extends": {"file": "finalpool.jsonl", "tasks": len(old)},
        "new_tasks": len(pool),
        "total_after": len(old) + len(pool),
        "counts_new": counts,
        "counts_combined_by_block": combined,
        "rg_configs": {f: ff.RG_FINAL[f] for f in EXT_SPEC["rg"]},
        "deviations": {
            "aime_2026": "0 new: reference solves it at 1.00, cannot "
                         "register a loss",
            "hmmt_feb_2026": "11 new = the entire remaining pool",
            "math_share": "16% -> 9% of the suite, pool exhausted",
        },
        "calibrated_against": ff.CALIBRATED_AGAINST,
        "pins": ff.PINS,
        "sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
        "disjoint_from": {k: len(v) for k, v in used.items()},
    }
    (OUT / "EXT-MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, default=str))
    print(json.dumps(manifest, indent=2, default=str))


if __name__ == "__main__":
    main()
