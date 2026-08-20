# Qwen3.8-27B quant quality and reasoning dataset

This is the raw, verifier-backed quality campaign behind a five-way quant
comparison of Qwen3.8-27B on a 4x RTX 3090 rig. It contains the scored results,
every accepted scenario response, the hidden model calls made by agentic packs,
reasoning traces, token accounting, launch commands, engine logs, repairs, and
the analysis code that produced the tables.

Nothing here is a leaderboard distilled to one number. The useful part is that
you can inspect *which* tasks flipped, how much reasoning each model spent, and
the exact request and response that produced every verdict.

## What is in the matrix

- Five artifacts: FP8 reference, NVFP4, AWQ INT4, GGUF Q4_K_M, and NInfer.
- Four controls: `off`, `low`, `medium`, and `xhigh`.
- Two separately reported suites: BenchLocal `full` (150 cases) and
  `--reasoning-packs` (90 runnable cases).
- 40 arms and 4,800 scenario-arm rows.
- 10,118 analyzed direct and hidden chat-completion calls.
- 18,796 lossless proxy telemetry records.
- 7,171 non-empty extracted reasoning traces.
- Pass@1 is the result. Retry credit is diagnostic only.

## Headline Pass@1 snapshot

The complete low/medium tables and token distributions are in
[`raw/combined-results/SUMMARY.md`](raw/combined-results/SUMMARY.md).

| Quant | Full off | Full xhigh | Reasoning off | Reasoning xhigh |
|---|---:|---:|---:|---:|
| FP8 | 121/150 | 133/150 | 85/90 | 89/90 |
| NVFP4 | 122/150 | 134/150 | 70/90 | 90/90 |
| AWQ INT4 | 117/150 | **135/150** | 83/90 | **90/90** |
| GGUF Q4_K_M | 116/150 | 134/150 | 84/90 | 89/90 |
| NInfer | 119/150 | 132/150 | 84/90 | 88/90 |

Small score gaps are not automatically meaningful: most thinking packs use
the model-recommended non-greedy sampler (Hermes retains its pack-level greedy
default), each scenario has one authoritative Pass@1 sample, and several strict-validity exceptions are documented in
[`CAVEATS.md`](CAVEATS.md). Use the paired task flips and exact McNemar tests,
not just totals.

## Start here

```bash
# Full human-readable matrix
less quality/raw/combined-results/SUMMARY.md

# One row per model x effort x suite
less -S quality/raw/combined-results/per-arm.csv

# One row per scenario, including all-call token totals
python3 - <<'PY'
import csv
with open("quality/raw/combined-results/per-scenario.csv", newline="") as f:
    for row in csv.DictReader(f):
        if row["model"] == "ninfer" and row["effort"] == "xhigh" and row["passed"] == "False":
            print(row["suite"], row["pack"], row["scenario"], row["failure_mode"])
PY

# Stream one reasoning trace and its final answer
python3 quality/scripts/inspect_traces.py \
  --model ninfer --effort xhigh --scenario HumanEval-22 \
  --show-answer --limit 1

# Verify the entire public export
python3 quality/scripts/verify_release.py
```

`zstd` is the only non-Python requirement. Large `.jsonl` and `.log` files are
stored as independent `.zst` streams. For direct access:

```bash
zstd -dc quality/raw/results/ninfer/telemetry.jsonl.zst |
  jq -r 'select(.response_extracted.reasoning_content != null) |
         [.scenario, .request_reasoning_effort,
          .response_extracted.reasoning_content] | @json' |
  less
```

## Dataset map

| Path | Meaning |
|---|---|
| `raw/combined-results/SUMMARY.{md,json}` | Full human/machine summary and paired comparisons |
| `raw/combined-results/per-arm.csv` | 40 arm-level scores, tokens, latency, and validity audits |
| `raw/combined-results/per-pack.csv` | Per-pack results and failure modes |
| `raw/combined-results/per-scenario.csv` | 4,800 task-level rows with all-call token totals |
| `raw/combined-results/per-request.csv` | 10,118 direct/hidden model-call accounting rows |
| `raw/**/<effort>/<suite>/result.json` | BenchLocal result with scenario request, raw response, verdict, and verifier trace |
| `raw/**/telemetry.jsonl.zst` | Lossless proxy request/response records and normalized reasoning extraction |
| `raw/**/server-launch.json` | Actual server argv, environment, context, KV type, and GPU mapping |
| `raw/harness/` | Runner, proxy, analyzer, patches, and validation fingerprints |
| `raw/repair-*`, `raw/**/repairs/` | Targeted repair provenance; originals are retained |
| `raw/rejected/` | Explicitly rejected contaminated preflight data, never counted |
| `MANIFEST.json`, `SHA256SUMS` | Source/public hashes, compression map, sanitization counts, integrity |

See [`DATA_DICTIONARY.md`](DATA_DICTIONARY.md) for the field-level guide,
[`METHODOLOGY.md`](METHODOLOGY.md) for reproduction details, and
[`ATTRIBUTION.md`](ATTRIBUTION.md) for model and dataset provenance.

## Sanitization policy

The private campaign is immutable. This export changes only host-specific
absolute paths and the LAN address into named `$PLACEHOLDERS`; it removes
ephemeral PID files, Python bytecode, and broken absolute symlinks. No prompt,
model answer, reasoning text, score, token count, timestamp, or latency is
otherwise normalized. `MANIFEST.json` records both private-source hashes and
public hashes for each file without disclosing the private values that were
replaced.
