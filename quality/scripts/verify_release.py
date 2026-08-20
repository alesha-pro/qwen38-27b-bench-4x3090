#!/usr/bin/env python3
"""Verify checksums, row counts, raw responses, telemetry, and public hygiene."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path


QUALITY_ROOT = Path(__file__).parents[1]
RAW_ROOT = QUALITY_ROOT / "raw"
MODELS = {
    "fp8": RAW_ROOT / "results/fp8",
    "awq-int4": RAW_ROOT / "results/awq-int4",
    "ninfer": RAW_ROOT / "results/ninfer",
    "nvfp4": RAW_ROOT / "lane-b-results/nvfp4",
    "gguf-q4-k-m": RAW_ROOT / "lane-b-results/gguf-q4-k-m",
}
EXPECTED_TELEMETRY = {
    "fp8": (3713, 1459),
    "awq-int4": (3963, 1416),
    "ninfer": (3716, 1486),
    "nvfp4": (3891, 1392),
    "gguf-q4-k-m": (3513, 1418),
}
FORBIDDEN = {
    "private_campaign_path": re.compile(rb"/(?:home|Users)/[^/\s]+/benchmarks/Qwen3\.8-27B-quant-quality"),
    "private_model_or_engine_root": re.compile(rb"/mnt/(?:nvme2?|ssd)/(?:models|engines)"),
    "hf_token": re.compile(rb"hf_[A-Za-z0-9]{20,}"),
    "openai_style_key": re.compile(rb"sk-[A-Za-z0-9_-]{20,}"),
    "bearer_secret": re.compile(rb"Bearer\s+[A-Za-z0-9._~+/=-]{16,}", re.I),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_artifact(path: Path) -> bytes:
    if path.suffix != ".zst":
        return path.read_bytes()
    return subprocess.run(
        ["zstd", "-q", "-dc", str(path)],
        check=True,
        stdout=subprocess.PIPE,
    ).stdout


def verify_checksums() -> int:
    checked = 0
    for line in (QUALITY_ROOT / "SHA256SUMS").read_text().splitlines():
        expected, relative = line.split("  ", 1)
        path = QUALITY_ROOT / relative
        assert path.is_file(), path
        assert sha256(path) == expected, path
        checked += 1
    return checked


def verify_results() -> tuple[int, int, int]:
    arms = scenarios = raw_responses = 0
    for model_root in MODELS.values():
        for path in sorted(model_root.glob("*/*/result.json")):
            arms += 1
            result = json.loads(path.read_text())
            for pack in result["packs"]:
                for scenario in pack["scenarios"]:
                    scenarios += 1
                    raw_responses += scenario.get("raw_response") is not None
    assert arms == 40, arms
    assert scenarios == 4800, scenarios
    assert raw_responses == scenarios, (raw_responses, scenarios)
    return arms, scenarios, raw_responses


def verify_combined() -> tuple[int, int]:
    combined = RAW_ROOT / "combined-results"
    with (combined / "per-scenario.csv").open(newline="") as handle:
        scenario_rows = sum(1 for _ in csv.DictReader(handle))
    with (combined / "per-request.csv").open(newline="") as handle:
        request_rows = sum(1 for _ in csv.DictReader(handle))
    summary = json.loads((combined / "SUMMARY.json").read_text())
    assert scenario_rows == summary["scenario_count"] == 4800
    assert request_rows == summary["request_count"] == 10118
    assert len(summary["arms"]) == 40
    return scenario_rows, request_rows


def verify_telemetry() -> dict[str, tuple[int, int]]:
    observed = {}
    for model, root in MODELS.items():
        data = read_artifact(Path(str(root / "telemetry.jsonl") + ".zst"))
        lines = reasoning = 0
        for line in data.splitlines():
            row = json.loads(line)
            lines += 1
            reasoning += bool((row.get("response_extracted") or {}).get("reasoning_content"))
        observed[model] = (lines, reasoning)
        assert observed[model] == EXPECTED_TELEMETRY[model], (model, observed[model])
    return observed


def verify_hygiene() -> int:
    checked = 0
    for path in RAW_ROOT.rglob("*"):
        if not path.is_file():
            continue
        data = read_artifact(path)
        for label, pattern in FORBIDDEN.items():
            assert not pattern.search(data), f"{label}: {path}"
        checked += 1
    return checked


def main() -> None:
    checksums = verify_checksums()
    arms, scenarios, raw_responses = verify_results()
    scenario_rows, request_rows = verify_combined()
    telemetry = verify_telemetry()
    hygiene_files = verify_hygiene()
    print(
        json.dumps(
            {
                "status": "ok",
                "checksummed_files": checksums,
                "arms": arms,
                "scenarios": scenarios,
                "raw_responses": raw_responses,
                "per_scenario_rows": scenario_rows,
                "per_request_rows": request_rows,
                "telemetry": telemetry,
                "hygiene_files": hygiene_files,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
