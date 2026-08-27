import json, collections
from pathlib import Path
used = collections.defaultdict(set)
for p in ("dev-pool/devpool.jsonl", "dev-pool/devpool-rg-v2.jsonl",
          "final-pool/finalpool.jsonl", "final-pool/canarypool.jsonl"):
    for l in Path(p).open():
        t = json.loads(l); s = t.get("source", {}); k = s.get("kind")
        if k == "matharena":  used["ma_" + s["competition"]].add(t["id"])
        elif k == "ifbench":  used["if"].add(s.get("line"))
        elif k == "bfcl":     used["bfcl_" + s["category"]].add(t["id"])
tot = {"ma_hmmt_feb_2026": 33, "ma_aime_2026": 30, "if": 300,
       "bfcl_live_multiple": 1053, "bfcl_live_simple": 258,
       "bfcl_irrelevance": 240, "bfcl_live_parallel_multiple": 24}
print("%-30s %6s %6s %6s" % ("source", "total", "used", "free"))
for k, v in tot.items():
    print("%-30s %6d %6d %6d" % (k, v, len(used[k]), v - len(used[k])))
