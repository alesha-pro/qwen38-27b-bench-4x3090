#!/usr/bin/env python3
"""Build dense quality/reasoning/token reports from completed matrix artifacts."""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
from collections import Counter as CollectionsCounter
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from tokenizers import Tokenizer


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def percentile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    index = (len(ordered) - 1) * q
    lower = math.floor(index)
    upper = math.ceil(index)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] * (upper - index) + ordered[upper] * (index - lower)


def distribution(values: list[float | int]) -> dict:
    clean = [float(value) for value in values if isinstance(value, (int, float))]
    return {
        "count": len(clean),
        "sum": sum(clean),
        "mean": statistics.fmean(clean) if clean else None,
        "median": statistics.median(clean) if clean else None,
        "p90": percentile(clean, 0.90),
        "p95": percentile(clean, 0.95),
        "max": max(clean) if clean else None,
    }


def count_values(values) -> dict[str, int]:
    return dict(sorted(CollectionsCounter(str(value) for value in values).items()))


def exact_mcnemar_p(regressions: int, fixes: int) -> float:
    """Two-sided exact binomial McNemar p-value for paired pass/fail flips."""
    discordant = regressions + fixes
    if discordant == 0:
        return 1.0
    tail = min(regressions, fixes)
    probability = sum(math.comb(discordant, k) for k in range(tail + 1)) / (2 ** discordant)
    return min(1.0, 2 * probability)


def safe_div(numerator: float | int | None, denominator: float | int | None) -> float | None:
    if numerator is None or not denominator:
        return None
    return float(numerator) / float(denominator)


class Counter:
    def __init__(self, path: Path):
        self.path = path
        self.tokenizer = Tokenizer.from_file(str(path))

    def count(self, value) -> int:
        if value is None:
            return 0
        if isinstance(value, str):
            text = value
        else:
            text = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return len(self.tokenizer.encode(text, add_special_tokens=False).ids) if text else 0


def read_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def request_row(raw: dict, counter: Counter) -> dict:
    summary = raw.get("response_summary") or {}
    extracted = raw.get("response_extracted") or {}
    usage = summary.get("usage") or {}
    details = usage.get("completion_tokens_details") or {}
    reported_reasoning = details.get("reasoning_tokens")
    reconstructed_reasoning = counter.count(extracted.get("reasoning_content"))
    reasoning = (
        reported_reasoning if isinstance(reported_reasoning, int) else reconstructed_reasoning
    )
    completion = usage.get("completion_tokens")
    return {
        "started_at": raw.get("started_at"),
        "scenario": raw.get("scenario"),
        "attempt": raw.get("attempt"),
        "status_code": raw.get("status_code"),
        "duration_seconds": raw.get("duration_seconds"),
        "response_headers_seconds": raw.get("response_headers_seconds"),
        "request_reasoning_effort": raw.get("request_reasoning_effort"),
        "request_chat_template_kwargs": json.dumps(
            raw.get("request_chat_template_kwargs"), ensure_ascii=False, sort_keys=True
        ),
        "request_has_max_tokens": raw.get("request_has_max_tokens"),
        "request_max_tokens": raw.get("request_max_tokens"),
        "reported_prompt_tokens": usage.get("prompt_tokens"),
        "reported_completion_tokens": usage.get("completion_tokens"),
        "reported_total_tokens": usage.get("total_tokens"),
        "reported_reasoning_tokens": reported_reasoning,
        "reconstructed_reasoning_tokens": reconstructed_reasoning,
        "reconstructed_answer_tokens": counter.count(extracted.get("content")),
        "reconstructed_tool_tokens": counter.count(
            extracted.get("tool_calls") or extracted.get("tool_call_fragments")
        ),
        "reasoning_tokens": reasoning,
        "reasoning_source": "reported" if isinstance(reported_reasoning, int) else "reconstructed",
        "reasoning_chars": summary.get("reasoning_chars"),
        "answer_chars": summary.get("answer_chars"),
        "finish_reason": summary.get("finish_reason"),
        "stream": summary.get("stream"),
        "reasoning_share_of_completion": safe_div(reasoning, completion),
        "http_ok": isinstance(raw.get("status_code"), int) and 200 <= raw["status_code"] < 300,
        "error": raw.get("error"),
    }


def sum_int(rows: list[dict], key: str) -> int | None:
    values = [row.get(key) for row in rows if isinstance(row.get(key), int)]
    return sum(values) if values else None


def sum_number(rows: list[dict], key: str) -> float | None:
    values = [row.get(key) for row in rows if isinstance(row.get(key), (int, float))]
    return sum(values) if values else None


def arm_rows(model: str, effort: str, suite: str, result: dict, proxy: list[dict], counter: Counter):
    started = parse_time(result["started_at"])
    finished = parse_time(result["finished_at"])
    raw_requests = [
        row for row in proxy
        if row.get("started_at")
        and started <= parse_time(row["started_at"]) <= finished
        and str(row.get("incoming_path") or "").endswith("/chat/completions")
    ]
    requests = [request_row(row, counter) for row in raw_requests]
    scenario_rows = []
    for pack in result.get("packs", []):
        pack_id = pack["pack_id"]
        for scenario in pack.get("scenarios", []):
            scenario_id = scenario["id"]
            tag_prefix = f"{pack_id}/{scenario_id}/"
            matching = [row for row in requests if str(row.get("scenario") or "").startswith(tag_prefix)]
            metrics = scenario.get("token_metrics") or {}
            all_reasoning = sum_int(matching, "reasoning_tokens")
            all_completion = sum_int(matching, "reported_completion_tokens")
            request_efforts = sorted({
                str(row["request_reasoning_effort"])
                for row in matching if row.get("request_reasoning_effort") is not None
            })
            thinking_kwargs = sorted({
                str(json.loads(row["request_chat_template_kwargs"]).get("enable_thinking"))
                for row in matching
                if row.get("request_chat_template_kwargs") not in {None, "null"}
            })
            scenario_rows.append({
                "model": model,
                "effort": effort,
                "suite": suite,
                "pack": pack_id,
                "scenario": scenario_id,
                "passed": scenario.get("passed"),
                "pass_at_k": scenario.get("pass_at_k"),
                "label": scenario.get("label"),
                "failure_mode": scenario.get("failure_mode"),
                "detail": scenario.get("detail"),
                "latency_seconds": scenario.get("latency_seconds"),
                "attempt_count": scenario.get("attempt_count"),
                "retry_attempt_count": len(scenario.get("retry_attempts") or []),
                "model_request_count": len(matching),
                "direct_prompt_tokens": metrics.get("reported_prompt_tokens"),
                "direct_completion_tokens": metrics.get("reported_completion_tokens"),
                "direct_reasoning_tokens": metrics.get("reasoning_tokens"),
                "direct_answer_tokens": metrics.get("reconstructed_answer_tokens"),
                "all_calls_prompt_tokens": sum_int(matching, "reported_prompt_tokens"),
                "all_calls_completion_tokens": sum_int(matching, "reported_completion_tokens"),
                "all_calls_reasoning_tokens": all_reasoning,
                "all_calls_answer_tokens": sum_int(matching, "reconstructed_answer_tokens"),
                "all_calls_tool_tokens": sum_int(matching, "reconstructed_tool_tokens"),
                "all_calls_duration_seconds": sum_number(matching, "duration_seconds"),
                "reasoning_share_of_completion": safe_div(all_reasoning, all_completion),
                "requests_with_reasoning": sum(
                    (row.get("reasoning_tokens") or 0) > 0 for row in matching
                ),
                "any_max_tokens": any(row.get("request_has_max_tokens") is True for row in matching),
                "max_tokens_values": json.dumps(sorted({
                    row["request_max_tokens"] for row in matching
                    if isinstance(row.get("request_max_tokens"), int)
                })),
                "request_reasoning_efforts": json.dumps(request_efforts),
                "enable_thinking_values": json.dumps(thinking_kwargs),
                "finish_reasons": json.dumps(
                    [row.get("finish_reason") for row in matching], ensure_ascii=False
                ),
                "thinking_validity": (result.get("thinking_validity") or {}).get(pack_id),
            })
    for row in requests:
        row.update({"model": model, "effort": effort, "suite": suite})
    return scenario_rows, requests


def pairwise(reference: list[dict], candidate: list[dict]) -> dict:
    ref = {(row["suite"], row["pack"], row["scenario"]): bool(row["passed"]) for row in reference}
    cand = {(row["suite"], row["pack"], row["scenario"]): bool(row["passed"]) for row in candidate}
    common = sorted(set(ref) & set(cand))
    regressions = [key for key in common if ref[key] and not cand[key]]
    fixes = [key for key in common if not ref[key] and cand[key]]
    ref_passed = sum(ref[key] for key in common)
    candidate_passed = sum(cand[key] for key in common)
    return {
        "common": len(common),
        "reference_passed": ref_passed,
        "candidate_passed": candidate_passed,
        "reference_score": safe_div(ref_passed, len(common)),
        "candidate_score": safe_div(candidate_passed, len(common)),
        "delta_percentage_points": 100 * safe_div(candidate_passed - ref_passed, len(common)) if common else None,
        "same": sum(ref[key] == cand[key] for key in common),
        "regression_count": len(regressions),
        "fix_count": len(fixes),
        "regressions_vs_fp8": ["/".join(key) for key in regressions],
        "fixes_vs_fp8": ["/".join(key) for key in fixes],
        "net": len(fixes) - len(regressions),
        "mcnemar_exact_p": exact_mcnemar_p(len(regressions), len(fixes)),
    }


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    columns = sorted({key for row in rows for key in row})
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def summarize_arm(model: str, effort: str, suite: str, result: dict,
                  scenarios: list[dict], requests: list[dict]) -> tuple[dict, list[dict]]:
    metric_keys = (
        "all_calls_prompt_tokens", "all_calls_completion_tokens",
        "all_calls_reasoning_tokens", "all_calls_answer_tokens",
        "all_calls_tool_tokens", "latency_seconds", "all_calls_duration_seconds",
        "model_request_count", "attempt_count",
    )
    metrics = {
        key: distribution([row[key] for row in scenarios if row.get(key) is not None])
        for key in metric_keys
    }
    reasoning_total = metrics["all_calls_reasoning_tokens"]["sum"]
    completion_total = metrics["all_calls_completion_tokens"]["sum"]
    request_max = [row for row in requests if row.get("request_has_max_tokens") is True]
    reasoning_requests = [row for row in requests if (row.get("reasoning_tokens") or 0) > 0]
    length_requests = [row for row in requests if row.get("finish_reason") == "length"]
    kwargs_values = []
    for row in requests:
        raw = row.get("request_chat_template_kwargs")
        if raw not in {None, "null"}:
            kwargs_values.append((json.loads(raw) or {}).get("enable_thinking"))
    validity = result.get("thinking_validity") or {}
    validity_statuses = count_values(
        observation.get("status") for observation in validity.values() if observation
    )
    expected_reasoning = effort != "off"
    audit = {
        "expected_reasoning": expected_reasoning,
        "requests": len(requests),
        "requests_with_reasoning": len(reasoning_requests),
        "scenarios_with_reasoning": sum((row.get("all_calls_reasoning_tokens") or 0) > 0 for row in scenarios),
        "requests_with_max_tokens": len(request_max),
        "max_tokens_values": sorted({row.get("request_max_tokens") for row in request_max}),
        "finish_reason_counts": count_values(row.get("finish_reason") for row in requests),
        "length_finish_count": len(length_requests),
        "request_reasoning_effort_counts": count_values(
            row.get("request_reasoning_effort") for row in requests
        ),
        "enable_thinking_counts": count_values(kwargs_values),
        "reasoning_source_counts": count_values(row.get("reasoning_source") for row in requests),
        "thinking_validity_statuses": validity_statuses,
        "no_forced_thinking_cap": len(request_max) == 0 if expected_reasoning else None,
        "reasoning_observed": len(reasoning_requests) > 0 if expected_reasoning else None,
        "off_stayed_silent": len(reasoning_requests) == 0 if not expected_reasoning else None,
        "strict_validity_ok": not any(status in {"silent", "contaminated"} for status in validity_statuses),
    }
    pack_rows = []
    for pack in result.get("packs", []):
        matching = [row for row in scenarios if row["pack"] == pack["pack_id"]]
        pack_rows.append({
            "model": model,
            "effort": effort,
            "suite": suite,
            "pack": pack["pack_id"],
            "passed": pack.get("passed"),
            "total": pack.get("total"),
            "score": pack.get("score"),
            "pass_at_k_passed": (pack.get("pass_at_k") or {}).get("passed"),
            "pass_at_k_total": (pack.get("pass_at_k") or {}).get("total"),
            "pass_at_k_score": (pack.get("pass_at_k") or {}).get("score"),
            "credited_flaky": (pack.get("pass_at_k") or {}).get("credited_flaky"),
            "systematic": (pack.get("pass_at_k") or {}).get("systematic"),
            "reasoning_tokens_total": sum(
                row.get("all_calls_reasoning_tokens") or 0 for row in matching
            ),
            "completion_tokens_total": sum(
                row.get("all_calls_completion_tokens") or 0 for row in matching
            ),
            "latency_seconds_total": sum(row.get("latency_seconds") or 0 for row in matching),
            "failure_modes": json.dumps(
                count_values(row.get("failure_mode") for row in matching), sort_keys=True
            ),
            "thinking_validity": json.dumps(validity.get(pack["pack_id"]), sort_keys=True),
        })
    pass_at_k = result.get("pass_at_k") or {}
    arm = {
        "model": model,
        "effort": effort,
        "suite": suite,
        "passed": result["totals"]["passed"],
        "total": result["totals"]["total"],
        "score": result["totals"]["score"],
        "pass_at_k": pass_at_k,
        "failure_modes": count_values(row.get("failure_mode") for row in scenarios),
        "metrics": metrics,
        "model_requests": len(requests),
        "reasoning_share_of_completion": safe_div(reasoning_total, completion_total),
        "thinking_validity": validity,
        "thinking_audit": audit,
        "warnings": result.get("warnings") or [],
    }
    return arm, pack_rows


def comparison_csv_rows(reference_name: str, comparisons: dict) -> list[dict]:
    rows = []
    for group, candidates in comparisons.items():
        for candidate, comparison in candidates.items():
            rows.append({
                "reference": reference_name,
                "group": group,
                "candidate": candidate,
                **{key: value for key, value in comparison.items()
                   if key not in {"regressions_vs_fp8", "fixes_vs_fp8"}},
                "regressions": json.dumps(comparison["regressions_vs_fp8"]),
                "fixes": json.dumps(comparison["fixes_vs_fp8"]),
            })
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--tokenizer-json", type=Path, required=True)
    args = parser.parse_args()
    counter = Counter(args.tokenizer_json)
    scenario_rows: list[dict] = []
    request_rows: list[dict] = []
    arms: list[dict] = []
    pack_rows: list[dict] = []
    by_model_effort: dict[tuple[str, str], list[dict]] = defaultdict(list)
    by_model_effort_suite: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    for model_dir in sorted(path for path in args.root.iterdir() if path.is_dir()):
        proxy = read_jsonl(model_dir / "telemetry.jsonl")
        for effort_dir in sorted(path for path in model_dir.iterdir() if path.is_dir()):
            effort = effort_dir.name
            if effort not in {"off", "low", "medium", "xhigh"}:
                continue
            for suite_dir in sorted(path for path in effort_dir.iterdir() if path.is_dir()):
                result_path = suite_dir / "result.json"
                if not result_path.is_file():
                    continue
                result = json.loads(result_path.read_text(encoding="utf-8"))
                scenarios, requests = arm_rows(
                    model_dir.name, effort, suite_dir.name, result, proxy, counter
                )
                scenario_rows.extend(scenarios)
                request_rows.extend(requests)
                by_model_effort[(model_dir.name, effort)].extend(scenarios)
                by_model_effort_suite[(model_dir.name, effort, suite_dir.name)].extend(scenarios)
                arm, arm_pack_rows = summarize_arm(
                    model_dir.name, effort, suite_dir.name, result, scenarios, requests
                )
                arms.append(arm)
                pack_rows.extend(arm_pack_rows)
    comparisons: dict[str, dict] = {}
    for effort in ("off", "low", "medium", "xhigh"):
        for suite in ("full", "reasoning"):
            reference = by_model_effort_suite.get(("fp8", effort, suite), [])
            if not reference:
                continue
            group = f"{effort}/{suite}"
            comparisons[group] = {
                model: pairwise(reference, rows)
                for (model, row_effort, row_suite), rows in by_model_effort_suite.items()
                if row_effort == effort and row_suite == suite and model != "fp8"
            }
    effort_vs_off: dict[str, dict] = {}
    for model in sorted({key[0] for key in by_model_effort_suite}):
        for suite in ("full", "reasoning"):
            reference = by_model_effort_suite.get((model, "off", suite), [])
            if not reference:
                continue
            effort_vs_off[f"{model}/{suite}"] = {
                effort: pairwise(reference, by_model_effort_suite[(model, effort, suite)])
                for effort in ("low", "medium", "xhigh")
                if (model, effort, suite) in by_model_effort_suite
            }
    summary = {
        "generated_at": datetime.now().astimezone().isoformat(),
        "arms": arms,
        "pairwise_vs_fp8": comparisons,
        "effort_vs_off": effort_vs_off,
        "scenario_count": len(scenario_rows),
        "request_count": len(request_rows),
        "methodology_notes": [
            "full and reasoning are separate requested suites; overlapping scenarios are not pooled into one score",
            "pass@1 is authoritative; pass@k is failure-retry diagnostic",
            "all_calls token totals include hidden agent/tool-loop model calls captured by the proxy",
            "thinking arms are valid only when no request max_tokens was sent and reasoning was observed",
        ],
    }
    write_json = lambda path, value: path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    write_json(args.root / "SUMMARY.json", summary)
    write_csv(args.root / "per-scenario.csv", scenario_rows)
    write_csv(args.root / "per-request.csv", request_rows)
    write_csv(args.root / "per-pack.csv", pack_rows)
    write_csv(args.root / "paired-vs-fp8.csv", comparison_csv_rows("fp8", comparisons))
    write_csv(args.root / "paired-effort-vs-off.csv", comparison_csv_rows("off", effort_vs_off))

    arm_csv = []
    for arm in arms:
        audit = arm["thinking_audit"]
        arm_csv.append({
            "model": arm["model"], "effort": arm["effort"], "suite": arm["suite"],
            "passed": arm["passed"], "total": arm["total"], "score": arm["score"],
            "pass_at_k_passed": arm["pass_at_k"].get("passed"),
            "pass_at_k_total": arm["pass_at_k"].get("total"),
            "pass_at_k_score": arm["pass_at_k"].get("score"),
            "model_requests": arm["model_requests"],
            "prompt_tokens_total": arm["metrics"]["all_calls_prompt_tokens"]["sum"],
            "completion_tokens_total": arm["metrics"]["all_calls_completion_tokens"]["sum"],
            "reasoning_tokens_total": arm["metrics"]["all_calls_reasoning_tokens"]["sum"],
            "reasoning_tokens_median": arm["metrics"]["all_calls_reasoning_tokens"]["median"],
            "reasoning_tokens_p95": arm["metrics"]["all_calls_reasoning_tokens"]["p95"],
            "answer_tokens_total": arm["metrics"]["all_calls_answer_tokens"]["sum"],
            "tool_tokens_total": arm["metrics"]["all_calls_tool_tokens"]["sum"],
            "latency_seconds_total": arm["metrics"]["latency_seconds"]["sum"],
            "latency_seconds_median": arm["metrics"]["latency_seconds"]["median"],
            "latency_seconds_p95": arm["metrics"]["latency_seconds"]["p95"],
            "reasoning_share_of_completion": arm["reasoning_share_of_completion"],
            "requests_with_reasoning": audit["requests_with_reasoning"],
            "requests_with_max_tokens": audit["requests_with_max_tokens"],
            "length_finish_count": audit["length_finish_count"],
            "no_forced_thinking_cap": audit["no_forced_thinking_cap"],
            "reasoning_observed": audit["reasoning_observed"],
            "off_stayed_silent": audit["off_stayed_silent"],
            "strict_validity_ok": audit["strict_validity_ok"],
            "failure_modes": json.dumps(arm["failure_modes"], sort_keys=True),
        })
    write_csv(args.root / "per-arm.csv", arm_csv)

    lines = [
        "# Qwen3.8-27B quant quality matrix",
        "",
        "Pass@1 is the quality result; pass@k is a diagnostic for failed-scenario retries. "
        "`full` and `reasoning` stay separate because they overlap.",
        "",
        "| Model | Effort | Suite | Pass@1 | Pass@k | Reasoning tokens total | Median | p95 | Think calls | max_tokens calls | Valid |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for arm in sorted(arms, key=lambda row: (row["effort"], row["suite"], row["model"])):
        rt = arm["metrics"]["all_calls_reasoning_tokens"]
        best = arm["pass_at_k"]
        audit = arm["thinking_audit"]
        valid = (
            audit["strict_validity_ok"]
            and (audit["off_stayed_silent"] if arm["effort"] == "off" else
                 audit["no_forced_thinking_cap"] and audit["reasoning_observed"])
        )
        lines.append(
            f"| {arm['model']} | {arm['effort']} | {arm['suite']} | "
            f"{arm['passed']}/{arm['total']} ({arm['score']:.1%}) | "
            f"{best.get('passed', '-')}/{best.get('total', '-')} "
            f"({best.get('score', 0):.1%}) | " if best else
            f"| {arm['model']} | {arm['effort']} | {arm['suite']} | "
            f"{arm['passed']}/{arm['total']} ({arm['score']:.1%}) | n/a | "
        )
        lines[-1] += (
            f"{rt['sum']:.0f} | {rt['median'] or 0:.0f} | {rt['p95'] or 0:.0f} | "
            f"{audit['requests_with_reasoning']} | {audit['requests_with_max_tokens']} | "
            f"{'yes' if valid else 'NO'} |"
        )
    lines += [
        "",
        "## Artifacts",
        "",
        "- `per-scenario.csv`: one task, its verdict, attempts, latency, and all-call token totals.",
        "- `per-request.csv`: every direct and hidden model call with raw usage/control audit.",
        "- `per-arm.csv`: dense arm-level statistics and thinking validity.",
        "- `per-pack.csv`: pack scores, token totals, failure modes, and pass@k.",
        "- `paired-vs-fp8.csv`: matched scenario flips and exact McNemar p-values.",
        "- `paired-effort-vs-off.csv`: quality changes caused by reasoning effort.",
        "- `SUMMARY.json`: lossless machine-readable aggregate, including task flip lists.",
    ]
    (args.root / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"arms": len(arms), "scenarios": len(scenario_rows), "requests": len(request_rows)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
