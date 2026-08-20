#!/usr/bin/env python3
"""Build the sanitized public mirror of the Qwen3.8 quality campaign.

The source campaign remains untouched. Text files are copied byte-for-byte
except for the explicit host-specific substitutions below. Large JSONL and log
files are compressed independently with zstd so every artifact stays below
GitHub's 100 MiB per-file limit and can still be streamed without extraction.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path


SKIP_NAMES = {"__pycache__"}
SKIP_SUFFIXES = {".pid", ".pyc"}
COMPRESS_SUFFIXES = {".jsonl", ".log"}
COMPRESS_MIN_BYTES = 1_000_000

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sanitize(data: bytes, replacements: list[tuple[str, bytes, bytes]]) -> tuple[bytes, dict[str, int]]:
    counts: Counter[str] = Counter()
    for label, source, replacement in replacements:
        count = data.count(source)
        if count:
            data = data.replace(source, replacement)
            counts[label] += count
    return data, dict(counts)


def should_skip(relative: Path) -> bool:
    if any(part in SKIP_NAMES for part in relative.parts):
        return True
    return relative.suffix in SKIP_SUFFIXES


def export_one(
    source: Path,
    destination_root: Path,
    relative: Path,
    replacements: list[tuple[str, bytes, bytes]],
) -> dict:
    source_bytes = source.read_bytes()
    public_bytes, replacement_counts = sanitize(source_bytes, replacements)

    compress = source.suffix in COMPRESS_SUFFIXES and len(public_bytes) >= COMPRESS_MIN_BYTES
    public_relative = Path(str(relative) + ".zst") if compress else relative
    destination = destination_root / public_relative
    destination.parent.mkdir(parents=True, exist_ok=True)

    if compress:
        process = subprocess.run(
            ["zstd", "-q", "-f", "-10", "-T0", "-o", str(destination)],
            input=public_bytes,
            check=True,
        )
        del process
    else:
        destination.write_bytes(public_bytes)

    return {
        "source_path": relative.as_posix(),
        "public_path": public_relative.as_posix(),
        "source_size": len(source_bytes),
        "public_size": destination.stat().st_size,
        "source_sha256": sha256_bytes(source_bytes),
        "sanitized_sha256": sha256_bytes(public_bytes),
        "public_sha256": sha256_file(destination),
        "compressed": compress,
        "replacements": replacement_counts,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="private campaign root")
    parser.add_argument("destination", type=Path, help="empty public raw directory")
    parser.add_argument(
        "--replacement-file",
        required=True,
        type=Path,
        help="private JSON array of {label, source, replacement}; never copied",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_root = args.source.resolve()
    destination_root = args.destination.resolve()
    if not source_root.is_dir():
        raise SystemExit(f"source is not a directory: {source_root}")
    if destination_root.exists() and any(destination_root.iterdir()):
        raise SystemExit(f"destination must be empty: {destination_root}")
    destination_root.mkdir(parents=True, exist_ok=True)

    replacement_config = json.loads(args.replacement_file.read_text(encoding="utf-8"))
    replacements = []
    labels = set()
    for item in replacement_config:
        label = item["label"]
        if label in labels:
            raise SystemExit(f"duplicate replacement label: {label}")
        labels.add(label)
        replacements.append(
            (label, item["source"].encode(), item["replacement"].encode())
        )
    replacements.sort(key=lambda item: len(item[1]), reverse=True)

    records = []
    skipped = []
    for source in sorted(source_root.rglob("*")):
        relative = source.relative_to(source_root)
        if source.is_symlink():
            skipped.append({"path": relative.as_posix(), "reason": "symlink"})
            continue
        if not source.is_file():
            continue
        if should_skip(relative):
            skipped.append({"path": relative.as_posix(), "reason": "ephemeral"})
            continue
        records.append(export_one(source, destination_root, relative, replacements))

    replacement_totals: Counter[str] = Counter()
    for record in records:
        replacement_totals.update(record["replacements"])

    manifest = {
        "schema_version": 1,
        "source_campaign": "Qwen3.8-27B-quant-quality-2026-08-18",
        "policy": {
            "description": "Sanitized raw export; source data is never modified in place.",
            "compressed_suffixes": sorted(COMPRESS_SUFFIXES),
            "compress_min_bytes": COMPRESS_MIN_BYTES,
            "skipped_names": sorted(SKIP_NAMES),
            "skipped_suffixes": sorted(SKIP_SUFFIXES),
            "replacement_totals": dict(replacement_totals),
        },
        "files": records,
        "skipped": skipped,
    }
    manifest_path = destination_root.parent / "MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    checksum_paths = [manifest_path]
    checksum_paths.extend(p for p in destination_root.rglob("*") if p.is_file())
    checksum_root = destination_root.parent
    checksum_lines = [
        f"{sha256_file(path)}  {path.relative_to(checksum_root).as_posix()}"
        for path in sorted(checksum_paths)
    ]
    (checksum_root / "SHA256SUMS").write_text("\n".join(checksum_lines) + "\n")

    print(
        json.dumps(
            {
                "exported_files": len(records),
                "skipped_files": len(skipped),
                "source_bytes": sum(r["source_size"] for r in records),
                "public_bytes": sum(r["public_size"] for r in records),
                "replacement_totals": dict(replacement_totals),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
