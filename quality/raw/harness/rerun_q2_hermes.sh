#!/usr/bin/env bash
# Пересдача hermesagent-20 для ud-q2-k-xl/xhigh/full на СВЕЖЕМ сервере.
#
# Зачем: в основном прогоне сценарий HA-13 разогнался до 255K токенов и
# повесил llama.cpp; HA-14..HA-20 умерли по agent_runner_timeout, счёт арма
# испорчен. Пересдаём весь пак (20 сценариев) на чистом сервере, результат
# кладём РЯДОМ (full-rerun-hermes), исходный result.json не трогаем.
#
# Запускать ТОЛЬКО когда GPU 0-1 свободны (полоса full убита).
set -euo pipefail

ROOT=$RUN_ROOT
ARM=$ROOT/ladder-full/ud-q2-k-xl
OUT=$ARM/xhigh/full-rerun-hermes
BENCH=$BENCHLOCAL_ROOT/.venv/bin/benchlocal-cli
PROXY=$ROOT/harness/telemetry_proxy.py
PORT=18093   # свои порты, чтобы не пересечься ни с чем живым
PPORT=19093

mkdir -p "$OUT"

echo "[rerun] launching fresh llama.cpp for UD-Q2_K_XL on GPU 0,1"
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

cleanup() {
  kill "$PROXY_PID" "$SERVER_PID" 2>/dev/null || true
}
trap cleanup EXIT

echo "[rerun] waiting for /health (up to 15 min)"
for i in $(seq 1 180); do
  if curl -sf "http://127.0.0.1:$PORT/health" > /dev/null 2>&1; then
    echo "[rerun] server ready after ${i}x5s"
    break
  fi
  sleep 5
  if ! kill -0 "$SERVER_PID" 2>/dev/null; then
    echo "[rerun] SERVER DIED during load, see $OUT/server.log" >&2
    exit 1
  fi
done

echo "[rerun] running benchlocal --pack hermesagent-20 @ xhigh"
"$BENCH" run --full --pack hermesagent-20 --enable-thinking \
  --reasoning-effort xhigh --thinking-max-tokens 0 \
  --tokenizer $MODEL_ROOT_FAST/Qwen3.8-27B-FP8 \
  --save-json "$OUT/result.json" \
  --sandbox-log-dir "$OUT/sandbox-logs" \
  --endpoint "http://127.0.0.1:$PPORT/v1" --model bench \
  --timeout-per-case 86400 --timeout-ceiling-s 0 --model-turn-timeout 0 \
  --progress --strict-thinking

echo "[rerun] done, result: $OUT/result.json"
