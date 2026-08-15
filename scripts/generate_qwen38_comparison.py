#!/usr/bin/env python3
"""Build a single auditable report from all Qwen3.8 benchmark summaries."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output"
REPORT = OUTPUT / "QWEN38-FULL-COMPARISON.md"
MERGED_CSV = OUTPUT / "qwen38-full-comparison.csv"
DEPTHS = [8192, 32768, 65536, 131072, 253952]
CONCURRENCIES = [1, 2, 4, 8, 16]
SUITES = [
    ("vLLM", "NVFP4", "vllm-depth-autonomous-qwen38-nvfp4"),
    ("SGLang", "NVFP4", "sglang-depth-autonomous-qwen38-nvfp4"),
    ("vLLM", "FP8", "vllm-depth-autonomous-qwen38-fp8"),
    ("SGLang", "FP8", "sglang-depth-autonomous-qwen38-fp8"),
]


def read_rows() -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for engine, weights, directory in SUITES:
        path = OUTPUT / directory / "summary.json"
        rows = json.loads(path.read_text())
        for row in rows:
            result.append(
                {
                    "engine": engine,
                    "weights": weights,
                    "suite_dir": directory,
                    **row,
                }
            )
    return result


def n(value: Any, digits: int = 2) -> str:
    if value is None:
        return "FAIL"
    return f"{float(value):.{digits}f}"


def depth_label(depth: int) -> str:
    return {
        8192: "8K",
        32768: "32K",
        65536: "64K",
        131072: "128K",
        253952: "254K",
    }.get(depth, f"{depth:,}")


def label(row: dict[str, Any]) -> str:
    mtp_name = "MTP" if row["mtp"] else "no-MTP"
    return f"TP{row['tp']} / {str(row['kv']).upper()} KV / {mtp_name}"


def md_table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    out = [
        "| " + " | ".join(headers) + " |",
        "|" + "|".join("---" for _ in headers) + "|",
    ]
    out.extend("| " + " | ".join(str(cell) for cell in row) + " |" for row in rows)
    return out


def select(
    rows: list[dict[str, Any]], engine: str, weights: str
) -> list[dict[str, Any]]:
    return [r for r in rows if r["engine"] == engine and r["weights"] == weights]


def configs(rows: list[dict[str, Any]]) -> list[str]:
    return sorted(
        {str(r["config"]) for r in rows},
        key=lambda value: (
            int(value.split("-")[0][2:]),
            "fp8" in value,
            "nomtp" not in value,
        ),
    )


def point(
    rows: list[dict[str, Any]], config: str, depth: int, concurrency: int
) -> dict[str, Any] | None:
    return next(
        (
            r
            for r in rows
            if r["config"] == config
            and int(r["depth"]) == depth
            and int(r["concurrency"]) == concurrency
        ),
        None,
    )


def metric_at(
    rows: list[dict[str, Any]],
    config: str,
    depth: int,
    concurrency: int,
    metric: str,
) -> Any:
    row = point(rows, config, depth, concurrency)
    if not row or row.get("status") != "ok":
        return None
    return row.get(metric)


def write_csv(rows: list[dict[str, Any]]) -> None:
    keys = [
        "engine",
        "weights",
        "config",
        "tp",
        "kv",
        "mtp",
        "depth",
        "concurrency",
        "status",
        "attempts",
        "prompt_tokens",
        "decode_tok_s_median",
        "aggregate_decode_window_tok_s",
        "aggregate_active_decode_rate_sum",
        "prefill_tok_s_median",
        "prefill_tok_s_aggregate",
        "ttft_p50_ms",
        "ttft_max_ms",
        "wall_s",
        "suite_dir",
    ]
    with MERGED_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def build_report(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Qwen3.8-27B: vLLM vs SGLang, NVFP4 vs FP8",
        "",
        "Hardware: 4x RTX 3090 (Ampere SM86, PCIe-only). All servers used a "
        "262,144-token context with CUDA graphs enabled; no run used eager mode. "
        "The matrix covers TP2/TP4, BF16/FP8 KV, MTP off/on, five context depths, "
        "and concurrency 1/2/4/8/16 at 8K. Each request generated 128 tokens.",
        "",
        "## Completion",
        "",
    ]
    completion = []
    for engine, weights, directory in SUITES:
        suite = select(rows, engine, weights)
        counts = Counter(str(r.get("status")) for r in suite)
        completion.append(
            [engine, weights, len(suite), counts["ok"], counts["failed"], f"`{directory}`"]
        )
    lines += md_table(
        ["Engine", "Weights", "Points", "OK", "Failed", "Raw suite"], completion
    )

    lines += [
        "",
        "## Practical conclusions",
        "",
        "- Best overall long-context stack on this host: **NVFP4 weights + vLLM + "
        "FP8 KV**. At 254K, no-MTP decode is 52.84 tok/s on TP2 and 74.85 "
        "tok/s on TP4; enabling MTP raises the measured points to 64.39 and "
        "84.26 tok/s respectively.",
        "- Pick **TP2** when TTFT, GPU efficiency, or running two replicas matters. "
        "For NVFP4/vLLM/FP8-KV at 254K it prefills at 1001.8 tok/s versus "
        "744.4 tok/s on TP4. Pick **TP4** when post-prefill single-stream decode "
        "is the priority.",
        "- FP8 KV is essential for vLLM at depth. With NVFP4/no-MTP, switching "
        "BF16 KV to FP8 KV changes 254K decode from 27.26 to 52.84 tok/s on "
        "TP2 and from 31.18 to 74.85 tok/s on TP4. It also prevents most "
        "long-context capacity failures.",
        "- SGLang is competitive and has faster TP4 prefill than vLLM in several "
        "BF16-KV cases, but its best NVFP4 254K decode here is 67.60 tok/s with "
        "BF16-KV/MTP or 65.69 tok/s with FP8-KV/MTP, below vLLM's 84.26 tok/s.",
        "- The FP8-weight checkpoint is slower than NVFP4 in the clean no-MTP/FP8-KV "
        "comparison: at 254K it trails by about 21.5%/14.9% in vLLM TP2/TP4 "
        "and 14.4%/9.6% in SGLang TP2/TP4. It also has more TP2 capacity failures.",
        "- MTP results use only 128 generated tokens and acceptance varies by prompt, "
        "so the irregular depth curves are real measurements but noisy. MTP with "
        "FP8 KV is promising; MTP with BF16 KV is a poor vLLM long-context choice.",
        "- At 8K, literal shared-window aggregate decode usually peaks at c=1 in "
        "vLLM and c=2 in SGLang because long prefills stagger entry into decode. "
        "The decode-only active-rate diagnostic generally plateaus around c=4-8 "
        "for vLLM TP4 and c=2-4 for SGLang TP4; TP2 can keep scaling to c=8-16.",
        "- The 38 remaining failures are capacity limits, not crashes: FP8 weights "
        "with BF16 KV do not fit vLLM TP2 at a 262,144-token model length; SGLang "
        "FP8-weight TP2 cannot fit MTP, and two TP2/BF16-KV configurations miss "
        "only the 254K request.",
    ]

    lines += [
        "",
        "## Single-stream decode by depth",
        "",
        "Values are median steady decode tokens/s after the first generated token.",
    ]
    for engine, weights, _ in SUITES:
        suite = select(rows, engine, weights)
        table = []
        for config in configs(suite):
            exemplar = next(r for r in suite if r["config"] == config)
            table.append(
                [label(exemplar)]
                + [n(metric_at(suite, config, depth, 1, "decode_tok_s_median")) for depth in DEPTHS]
            )
        lines += ["", f"### {engine} / {weights}", ""]
        lines += md_table(["Configuration", "8K", "32K", "64K", "128K", "254K"], table)

    lines += [
        "",
        "## Single-stream prefill by depth",
        "",
        "Values are effective prompt tokens/s to first token.",
    ]
    for engine, weights, _ in SUITES:
        suite = select(rows, engine, weights)
        table = []
        for config in configs(suite):
            exemplar = next(r for r in suite if r["config"] == config)
            table.append(
                [label(exemplar)]
                + [n(metric_at(suite, config, depth, 1, "prefill_tok_s_median"), 1) for depth in DEPTHS]
            )
        lines += ["", f"### {engine} / {weights}", ""]
        lines += md_table(["Configuration", "8K", "32K", "64K", "128K", "254K"], table)

    lines += [
        "",
        "## Depth degradation",
        "",
        "Decode change from 8K to 254K. FAIL means one of the endpoints was unavailable.",
        "",
    ]
    degradation = []
    for engine, weights, _ in SUITES:
        suite = select(rows, engine, weights)
        for config in configs(suite):
            exemplar = next(r for r in suite if r["config"] == config)
            low = metric_at(suite, config, DEPTHS[0], 1, "decode_tok_s_median")
            high = metric_at(suite, config, DEPTHS[-1], 1, "decode_tok_s_median")
            change = "FAIL" if not low or high is None else f"{(high / low - 1) * 100:+.1f}%"
            degradation.append([engine, weights, label(exemplar), n(low), n(high), change])
    lines += md_table(
        ["Engine", "Weights", "Configuration", "8K", "254K", "Change"], degradation
    )

    lines += [
        "",
        "## Aggregate decode and concurrency knee at 8K",
        "",
        "Each concurrency cell is `shared decode-window tok/s / sum of active request "
        "decode rates`. Both peaks are reported: the shared-window peak is the literal "
        "aggregate decode metric, while the active-rate peak is a decode-only diagnostic. "
        "The shared-window number is conservative when chunked prefills stagger entry "
        "into decode.",
        "",
    ]
    concurrency_rows = []
    for engine, weights, _ in SUITES:
        suite = select(rows, engine, weights)
        for config in configs(suite):
            exemplar = next(r for r in suite if r["config"] == config)
            cells = []
            shared_candidates = []
            active_candidates = []
            for concurrency in CONCURRENCIES:
                shared = metric_at(
                    suite, config, DEPTHS[0], concurrency, "aggregate_decode_window_tok_s"
                )
                active = metric_at(
                    suite, config, DEPTHS[0], concurrency, "aggregate_active_decode_rate_sum"
                )
                cells.append("FAIL" if shared is None or active is None else f"{shared:.2f} / {active:.2f}")
                if shared is not None:
                    shared_candidates.append((float(shared), concurrency))
                if active is not None:
                    active_candidates.append((float(active), concurrency))
            shared_peak = f"c={max(shared_candidates)[1]}" if shared_candidates else "FAIL"
            active_peak = f"c={max(active_candidates)[1]}" if active_candidates else "FAIL"
            concurrency_rows.append(
                [engine, weights, label(exemplar), *cells, shared_peak, active_peak]
            )
    lines += md_table(
        [
            "Engine",
            "Weights",
            "Configuration",
            "c1",
            "c2",
            "c4",
            "c8",
            "c16",
            "Shared peak",
            "Active peak",
        ],
        concurrency_rows,
    )

    lines += [
        "",
        "## Aggregate prefill at 8K",
        "",
    ]
    prefill_rows = []
    for engine, weights, _ in SUITES:
        suite = select(rows, engine, weights)
        for config in configs(suite):
            exemplar = next(r for r in suite if r["config"] == config)
            prefill_rows.append(
                [engine, weights, label(exemplar)]
                + [
                    n(metric_at(suite, config, DEPTHS[0], c, "prefill_tok_s_aggregate"), 1)
                    for c in CONCURRENCIES
                ]
            )
    lines += md_table(
        ["Engine", "Weights", "Configuration", "c1", "c2", "c4", "c8", "c16"],
        prefill_rows,
    )

    lines += [
        "",
        "## Terminal failures",
        "",
    ]
    failure_rows = []
    for engine, weights, _ in SUITES:
        suite = select(rows, engine, weights)
        for config in configs(suite):
            failed = [r for r in suite if r["config"] == config and r.get("status") != "ok"]
            if not failed:
                continue
            exemplar = failed[0]
            points = ", ".join(
                f"{depth_label(int(r['depth']))}/c{r['concurrency']}"
                for r in sorted(
                    failed, key=lambda x: (x["depth"], x["concurrency"])
                )
            )
            failure_rows.append([engine, weights, label(exemplar), len(failed), points])
    if failure_rows:
        lines += md_table(["Engine", "Weights", "Configuration", "Count", "Points"], failure_rows)
    else:
        lines.append("No failed points.")

    lines += [
        "",
        "## Raw data",
        "",
        f"Merged machine-readable table: `{MERGED_CSV.name}`. Every source suite also "
        "contains its per-point JSON files, `summary.json`, server logs, launch manifests, "
        "and status history.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    rows = read_rows()
    write_csv(rows)
    REPORT.write_text(build_report(rows), encoding="utf-8")
    print(REPORT)
    print(MERGED_CSV)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
