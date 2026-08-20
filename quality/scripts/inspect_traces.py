#!/usr/bin/env python3
"""Stream reasoning traces from the public telemetry files."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, TextIO


TELEMETRY = {
    "fp8": "results/fp8/telemetry.jsonl",
    "awq-int4": "results/awq-int4/telemetry.jsonl",
    "ninfer": "results/ninfer/telemetry.jsonl",
    "nvfp4": "lane-b-results/nvfp4/telemetry.jsonl",
    "gguf-q4-k-m": "lane-b-results/gguf-q4-k-m/telemetry.jsonl",
}


@contextmanager
def open_text(path: Path) -> Iterator[TextIO]:
    compressed = Path(str(path) + ".zst")
    if path.exists():
        with path.open(encoding="utf-8") as handle:
            yield handle
        return
    if not compressed.exists():
        raise FileNotFoundError(path)
    process = subprocess.Popen(
        ["zstd", "-q", "-dc", str(compressed)],
        stdout=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    assert process.stdout is not None
    try:
        yield process.stdout
    finally:
        if process.poll() is None:
            process.terminate()
        process.stdout.close()
        return_code = process.wait()
        if return_code not in (0, -13, -15):
            raise RuntimeError(f"zstd exited with {return_code}: {compressed}")


def effort_matches(row: dict, requested: str | None) -> bool:
    if requested is None:
        return True
    actual = row.get("request_reasoning_effort")
    if requested == "off":
        return actual in (None, "none", "off")
    return actual == requested


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-root", type=Path, default=Path(__file__).parents[1] / "raw")
    parser.add_argument("--model", choices=["all", *TELEMETRY], default="all")
    parser.add_argument("--effort", choices=["off", "low", "medium", "xhigh"])
    parser.add_argument("--scenario", help="case-insensitive substring")
    parser.add_argument("--limit", type=int, default=0, help="0 means unlimited")
    parser.add_argument("--show-answer", action="store_true")
    parser.add_argument("--json", action="store_true", help="emit one compact JSON object per trace")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    models = TELEMETRY if args.model == "all" else {args.model: TELEMETRY[args.model]}
    emitted = 0
    needle = args.scenario.lower() if args.scenario else None

    for model, relative in models.items():
        with open_text(args.raw_root / relative) as handle:
            for line_number, line in enumerate(handle, 1):
                row = json.loads(line)
                extracted = row.get("response_extracted") or {}
                reasoning = extracted.get("reasoning_content")
                if not reasoning or not effort_matches(row, args.effort):
                    continue
                scenario = str(row.get("scenario") or "")
                if needle and needle not in scenario.lower():
                    continue

                record = {
                    "model": model,
                    "scenario": scenario,
                    "attempt": row.get("attempt"),
                    "effort": row.get("request_reasoning_effort"),
                    "started_at": row.get("started_at"),
                    "duration_seconds": row.get("duration_seconds"),
                    "status_code": row.get("status_code"),
                    "telemetry_line": line_number,
                    "reasoning": reasoning,
                }
                if args.show_answer:
                    record["answer"] = extracted.get("content")

                if args.json:
                    print(json.dumps(record, ensure_ascii=False))
                else:
                    print(
                        f"===== {model} | {scenario} | effort={record['effort']} "
                        f"| attempt={record['attempt']} | line={line_number} ====="
                    )
                    print(reasoning)
                    if args.show_answer:
                        print("\n----- answer -----")
                        print(record.get("answer") or "")
                    print()

                emitted += 1
                if args.limit and emitted >= args.limit:
                    return

    if emitted == 0:
        print("No matching reasoning traces.", file=sys.stderr)


if __name__ == "__main__":
    main()
