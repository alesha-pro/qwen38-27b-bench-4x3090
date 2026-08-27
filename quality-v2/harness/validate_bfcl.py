#!/usr/bin/env python3
"""Validate our simplified BFCL matcher against BFCL's own AST checker.

The official checker lives inside a package that imports every provider SDK at
import time, so we stub the parts we do not use (tree-sitter grammars for
Java/JS, the model-config registry) and import the checker module itself.
Our categories are Python-schema only, so nothing stubbed is on the path.

Runs both checkers over every BFCL result of a finished run and reports
disagreements.
"""
import json
import sys
import types
from pathlib import Path

BFCL = ("/mnt/nvme2/datasets/local-quant-bench-v2/repos/bfcl/"
        "berkeley-function-call-leaderboard")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))


def load_official():
    fake = types.ModuleType("tree_sitter")

    class _L:
        def __init__(self, *a, **k):
            pass

    class _P:
        def __init__(self, *a, **k):
            pass

        def set_language(self, *a, **k):
            pass

    fake.Language, fake.Parser = _L, _P
    sys.modules["tree_sitter"] = fake
    for m in ("tree_sitter_java", "tree_sitter_javascript"):
        mm = types.ModuleType(m)
        mm.language = lambda: None
        sys.modules[m] = mm

    # model registry: only .underscore_to_dot is read, and only for models
    # that mangle dots in function names. Ours does not.
    cfg = types.ModuleType("bfcl_eval.constants.model_config")

    class _Cfg:
        underscore_to_dot = False

    class _Map(dict):
        def __getitem__(self, k):
            return _Cfg()

    cfg.MODEL_CONFIG_MAPPING = _Map()
    sys.modules["bfcl_eval.constants.model_config"] = cfg

    sys.path.insert(0, BFCL)
    from bfcl_eval.constants.enums import Language
    from bfcl_eval.eval_checker.ast_eval.ast_checker import ast_checker
    return ast_checker, Language


def to_official_output(rec):
    """Our runner stores OpenAI tool_calls; BFCL wants [{name: {args}}]."""
    try:
        msg = rec["response"]["choices"][0]["message"]
    except (KeyError, TypeError, IndexError):
        return []
    out = []
    for c in msg.get("tool_calls") or []:
        fn = c.get("function", {})
        try:
            args = json.loads(fn.get("arguments") or "{}")
        except json.JSONDecodeError:
            args = {}
        out.append({fn.get("name", ""): args})
    return out


def main(run_name, pool_file):
    import score_run
    ast_checker, Language = load_official()

    pool = {t["id"]: t for t in
            (json.loads(l) for l in (ROOT / pool_file).open())}
    rundir = ROOT / "runs" / run_name

    agree = disagree = skipped = 0
    diffs = []
    for f in sorted(rundir.rglob("r*/*.json")):
        rec = json.loads(f.read_text())
        task = pool.get(rec["task_id"])
        if not task or task["block"] != "tool-calling" or rec.get("error"):
            continue
        cat = task["answer_meta"]["category"]
        if cat == "irrelevance":
            skipped += 1        # official path differs; ours is a plain rule
            continue
        ours, _ = score_run.score_bfcl(task, rec)
        try:
            res = ast_checker(
                task.get("tools_raw"),
                to_official_output(rec),
                task["answer_meta"]["ground_truth"],
                Language.PYTHON,
                cat,
                "qwen-local",
            )
            theirs = 1.0 if res.get("valid") else 0.0
        except Exception as e:
            skipped += 1
            continue
        if ours == theirs:
            agree += 1
        else:
            disagree += 1
            diffs.append((rec["task_id"], ours, theirs,
                          str(res.get("error"))[:110]))

    print(f"compared: {agree + disagree}  agree: {agree}  "
          f"disagree: {disagree}  skipped: {skipped}")
    if diffs:
        print("\ndisagreements (ours / official / official error):")
        for d in diffs[:25]:
            print(f"  {d[0]:34} {d[1]:.0f} / {d[2]:.0f}  {d[3]}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "calib-xhigh",
         sys.argv[2] if len(sys.argv) > 2 else "dev-pool/devpool.jsonl")
