# Data dictionary and trace guide

## Three levels of data

1. **Scenario result**: what BenchLocal scored. Open
   `raw/<lane>/<model>/<effort>/<suite>/result.json` and navigate to
   `packs[].scenarios[]`.
2. **Request telemetry**: every direct or hidden HTTP model call. Stream the
   model's `telemetry.jsonl.zst`.
3. **Combined analysis**: joins scored scenarios to proxy calls by campaign
   timestamps and scenario session tags. Read the CSVs in
   `raw/combined-results/`.

## Scenario `result.json`

Important fields in `packs[].scenarios[]`:

| Field | Meaning |
|---|---|
| `id` | Pack-local scenario ID |
| `passed` | Authoritative Pass@1 verdict |
| `pass_at_k` | Failure-only retry diagnostic |
| `request` | Direct OpenAI-compatible request body |
| `raw_response` | Original direct response retained by BenchLocal |
| `assistant_messages` | Parsed assistant turns for multi-turn packs |
| `tool_calls` | Parsed tool calls |
| `token_metrics` | Direct-response token accounting |
| `verifier_trace` | Deterministic/sandbox verifier evidence |
| `failure_mode`, `detail` | Failure classification and explanation |
| `latency_seconds` | Scenario wall time, not comparable engine speed |

All 4,800 accepted scenario rows have a non-null `raw_response`.

## Proxy telemetry JSONL

Each line is one proxied HTTP operation. Chat-completion records include:

| JSON path | Meaning |
|---|---|
| `scenario` | Session tag joining hidden calls to a scored scenario |
| `attempt` | Request attempt number |
| `started_at`, `duration_seconds` | Timing |
| `request_reasoning_effort` | Normalized requested effort |
| `request_chat_template_kwargs` | Template controls seen in the request |
| `request_has_max_tokens`, `request_max_tokens` | Cap audit |
| `request` | Request actually forwarded to the model server |
| `response` | Original JSON/SSE response normalized into JSON storage |
| `response_summary` | Finish reason, usage, stream and character counts |
| `response_extracted.reasoning_content` | Universal extracted reasoning text |
| `response_extracted.content` | Final answer text |
| `response_extracted.tool_calls` | Parsed tool calls |
| `error` | Proxy/transport error detail when applicable |

Engine-native reasoning keys varied: some used
`response.choices[0].message.reasoning`, others `reasoning_content`.
`response_extracted.reasoning_content` is the stable cross-engine path.

Telemetry totals are:

| Model | JSONL records | Non-empty reasoning traces |
|---|---:|---:|
| FP8 | 3,713 | 1,459 |
| AWQ INT4 | 3,963 | 1,416 |
| NInfer | 3,716 | 1,486 |
| NVFP4 | 3,891 | 1,392 |
| GGUF Q4_K_M | 3,513 | 1,418 |

Not every telemetry record should contain reasoning: off calls, health or
non-chat operations, final answer-only turns, tool results, and failed requests
can legitimately have none.

## Combined CSVs

`per-request.csv` intentionally contains metrics, not the full trace text. Its
most useful columns are `model`, `effort`, `suite`, `scenario`, `attempt`,
`reasoning_tokens`, `reasoning_source`, `reasoning_chars`, reported usage,
request cap controls, finish reason, HTTP status, and duration.

`per-scenario.csv` is the task-level join. `all_calls_*` columns aggregate the
direct response and hidden agent calls. `direct_*` is only the scored direct
response. `any_max_tokens`, `finish_reasons`, and
`request_reasoning_efforts` are validity diagnostics.

`paired-vs-fp8.csv` reports matched task flips against FP8 at the same effort
and suite. `paired-effort-vs-off.csv` reports matched flips caused by changing
effort within one artifact. Both include exact two-sided McNemar p-values.

## Useful commands

```bash
# All NInfer xhigh traces as JSONL
python3 quality/scripts/inspect_traces.py \
  --model ninfer --effort xhigh --json > /tmp/ninfer-xhigh-traces.jsonl

# Find every task where AWQ fixed an FP8 failure
python3 - <<'PY'
import csv
with open("quality/raw/combined-results/paired-vs-fp8.csv", newline="") as f:
    for row in csv.DictReader(f):
        if row["candidate"] == "awq-int4":
            print(row["group"], row["fixes_vs_fp8"])
PY

# Inspect the raw response for one scenario
jq '.packs[].scenarios[] | select(.id == "HumanEval-22") |
    {passed, request, raw_response, token_metrics, verifier_trace}' \
  quality/raw/results/fp8/medium/reasoning/result.json | less
```
