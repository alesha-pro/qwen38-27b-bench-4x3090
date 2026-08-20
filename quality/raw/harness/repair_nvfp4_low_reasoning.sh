#!/usr/bin/env bash
set -euo pipefail

ROOT=$RUN_ROOT
MODEL_ROOT="$ROOT/lane-b-results/nvfp4"
ARM="$MODEL_ROOT/low/reasoning"
REPAIR="$ARM/repairs/gsm-resume"
VLLM=$VLLM_ENV/bin/vllm
BENCH=$BENCHLOCAL_ROOT/.venv/bin/benchlocal-cli
TOKENIZER=$MODEL_ROOT_FAST/Qwen3.8-27B-FP8

mkdir -p "$REPAIR"
export CUDA_VISIBLE_DEVICES=2,3
export CUDA_HOME=$VLLM_ENV/lib/python3.12/site-packages/nvidia/cu13
export BENCHLOCAL_SANDBOX_PORT_OFFSET=100

server_pid=
proxy_pid=
cleanup() {
  if [[ -n "$proxy_pid" ]]; then
    kill -TERM -- "-$proxy_pid" 2>/dev/null || true
  fi
  if [[ -n "$server_pid" ]]; then
    kill -TERM -- "-$server_pid" 2>/dev/null || true
  fi
  for _ in $(seq 1 30); do
    if ! ss -ltn | rg -q ':(18082|19082) '; then
      return
    fi
    sleep 1
  done
  if [[ -n "$proxy_pid" ]]; then
    kill -KILL -- "-$proxy_pid" 2>/dev/null || true
  fi
  if [[ -n "$server_pid" ]]; then
    kill -KILL -- "-$server_pid" 2>/dev/null || true
  fi
}
trap cleanup EXIT

setsid "$VLLM" serve $MODEL_ROOT_FAST/Qwen3.8-27B-NVFP4 \
  --tokenizer "$TOKENIZER" --served-model-name bench \
  --quantization compressed-tensors --kernel-config '{"linear_backend":"marlin"}' \
  --language-model-only --tensor-parallel-size 2 --disable-custom-all-reduce \
  --attention-backend FLASHINFER --kv-cache-dtype fp8 \
  --gpu-memory-utilization 0.90 --max-model-len 262144 \
  --max-num-seqs 1 --max-num-batched-tokens 8192 --no-enable-prefix-caching \
  --reasoning-parser qwen3 --enable-auto-tool-choice --tool-call-parser qwen3_xml \
  --port 18082 > "$REPAIR/server.log" 2>&1 &
server_pid=$!

setsid python3 "$ROOT/harness/telemetry_proxy.py" \
  --port 19082 --target http://127.0.0.1:18082 \
  --log "$REPAIR/telemetry.jsonl" > "$REPAIR/proxy.log" 2>&1 &
proxy_pid=$!

for _ in $(seq 1 180); do
  if curl -fsS http://127.0.0.1:19082/health >/dev/null 2>&1; then
    break
  fi
  kill -0 "$server_pid"
  kill -0 "$proxy_pid"
  sleep 5
done
curl -fsS http://127.0.0.1:19082/health >/dev/null

BENCHLOCAL_TELEMETRY_SESSION_PATHS=1 "$BENCH" run \
  --pack gsm-symbolic-30 --enable-thinking --reasoning-effort low \
  --thinking-max-tokens 0 --tokenizer "$TOKENIZER" \
  --incremental --save-json "$REPAIR/result.json" \
  --endpoint http://127.0.0.1:19082/v1 --model bench \
  --timeout-per-case 86400 --timeout-ceiling-s 0 --model-turn-timeout 0 \
  --progress --strict-thinking --history-file "$ROOT/lane-b-results/history.csv" \
  --report md --report-out "$REPAIR/RESULTS.md" > "$REPAIR/run.log" 2>&1

test "$(jq -r '.totals.total' "$REPAIR/result.json")" = 30

tmp="$ARM/result.json.repaired.tmp"
jq --slurpfile repair "$REPAIR/result.json" '
  ($repair[0].packs[] | select((.pack.pack_id // .pack_id // .id) == "gsm-symbolic-30")) as $gsm
  | .packs = [.packs[] |
      if ((.pack.pack_id // .pack_id // .id) == "gsm-symbolic-30")
      then $gsm else . end]
  | ([.packs[].passed] | add) as $passed
  | ([.packs[].total] | add) as $total
  | .totals.passed = $passed
  | .totals.total = $total
  | .totals.score = ($passed / $total)
  | .finished_at = $repair[0].finished_at
  | .warnings = ((.warnings // []) +
      ["gsm-symbolic-30 replaced from targeted low-effort repair after interrupted resume"])
' "$ARM/result.json" > "$tmp"
mv "$tmp" "$ARM/result.json"

cleanup
trap - EXIT

BENCHLOCAL_SANDBOX_PORT_OFFSET=100 nohup python3 "$ROOT/harness/run_quality_matrix.py" \
  --root "$ROOT/lane-b-results" --models nvfp4 gguf-q4-k-m \
  --target-port 18082 --proxy-port 19082 \
  --gpu-map-json '{"nvfp4":"2,3","gguf-q4-k-m":"2,3"}' \
  > "$ROOT/lane-b-driver.log" 2>&1 &
echo "$!" > "$ROOT/lane-b-driver.pid"
