#!/usr/bin/env bash
# Точечная пересдача HA-14..HA-20 для ud-q2-k-xl/xhigh/full.
#
# HA-13 пересдан отдельно и УПАЛ ВОСПРОИЗВОДИМО (разгон 2/2) — его вердикт
# остаётся fail. Здесь на свежем сервере доигрываются только семь сценариев,
# умерших каскадом после его разгона.
set -euo pipefail

ROOT=$RUN_ROOT
OUT=$ROOT/ladder-full/ud-q2-k-xl/xhigh/full-rerun-tail
BENCH=$BENCHLOCAL_ROOT/.venv/bin/benchlocal-cli
PROXY=$ROOT/harness/telemetry_proxy.py
PORT=18093
PPORT=19093

mkdir -p "$OUT"

CUDA_VISIBLE_DEVICES=0,1 $LLAMACPP_ROOT/build/bin/llama-server \
  --model $MODEL_ROOT/Qwen3.8-27B-GGUF-UD3/Qwen3.8-27B-UD-Q2_K_XL.gguf \
  --host 127.0.0.1 --port $PORT --ctx-size 262144 --parallel 1 \
  --cont-batching --no-cache-prompt --flash-attn on --gpu-layers 999 \
  --split-mode layer --tensor-split 1,1 --threads 18 --threads-batch 18 \
  --batch-size 4096 --ubatch-size 1024 \
  --cache-type-k q8_0 --cache-type-v q8_0 \
  --no-context-shift --jinja --reasoning auto --reasoning-budget -1 \
  --reasoning-format deepseek > "$OUT/server.log" 2>&1 &
SERVER_PID=$!

python3 "$PROXY" --port $PPORT --target "http://127.0.0.1:$PORT" \
  --log "$OUT/telemetry.jsonl" > "$OUT/proxy.log" 2>&1 &
PROXY_PID=$!

cleanup() { kill "$PROXY_PID" "$SERVER_PID" 2>/dev/null || true; }
trap cleanup EXIT

for i in $(seq 1 180); do
  curl -sf "http://127.0.0.1:$PORT/health" > /dev/null 2>&1 && break
  sleep 5
  kill -0 "$SERVER_PID" 2>/dev/null || { echo "SERVER DIED" >&2; exit 1; }
done
echo "[rerun2] server ready"

"$BENCH" run --full \
  --scenario hermesagent-20/HA-14 --scenario hermesagent-20/HA-15 \
  --scenario hermesagent-20/HA-16 --scenario hermesagent-20/HA-17 \
  --scenario hermesagent-20/HA-18 --scenario hermesagent-20/HA-19 \
  --scenario hermesagent-20/HA-20 \
  --enable-thinking --reasoning-effort xhigh --thinking-max-tokens 0 \
  --tokenizer $MODEL_ROOT_FAST/Qwen3.8-27B-FP8 \
  --save-json "$OUT/result.json" \
  --sandbox-log-dir "$OUT/sandbox-logs" \
  --endpoint "http://127.0.0.1:$PPORT/v1" --model bench \
  --timeout-per-case 86400 --timeout-ceiling-s 0 --model-turn-timeout 0 \
  --progress --strict-thinking

echo "[rerun2] done"
