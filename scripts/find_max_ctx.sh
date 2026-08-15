#!/usr/bin/env bash
# Максимальный контекст на ОДНОЙ карте: двоичный поиск по -c.
#
#   bash find_max_ctx.sh /path/model.gguf [верхняя_граница]
#
# Один слот (-np 1), все слои на GPU. Успех — сервер ответил на /health;
# провал — упал или не поднялся. Веса после первой попытки лежат в page cache,
# поэтому итерации идут быстрее первой.
set -euo pipefail

MODEL="${1:?укажи путь к .gguf}"
HI_START="${2:-262144}"
PORT=18000
GPU="${GPU:-0}"
BIN="${LLAMA_BIN:-$ENGINES/llama.cpp-rw/build/bin}"
[ -x "$BIN/llama-server" ] || BIN=$ENGINES/llama.cpp/build-rw/bin

STAMP="$(date +%Y-%m-%d-%H%M%S)"
OUTDIR="$BENCH_ROOT/output/maxctx-$(basename "$MODEL" .gguf)-${STAMP}"
mkdir -p "$OUTDIR"

STEP=1024          # гранулярность ответа
LO=0               # заведомо влезает (0 = ещё не подтверждено)
HI=$HI_START       # заведомо не влезает или предел модели
BEST=0

echo "== модель: $MODEL"
echo "== карта:  GPU $GPU, один слот"
echo "== поиск в [$STEP, $HI], шаг $STEP" | tee "$OUTDIR/log.txt"

probe() {
  local ctx="$1"
  local log="$OUTDIR/probe-$ctx.log"
  CUDA_VISIBLE_DEVICES="$GPU" "$BIN/llama-server" \
    --model "$MODEL" \
    --host 127.0.0.1 --port "$PORT" \
    --alias bench \
    --n-gpu-layers 999 \
    --ctx-size "$ctx" \
    --parallel 1 \
    --flash-attn on \
    > "$log" 2>&1 &
  local pid=$!
  local rc=1
  local i
  for i in $(seq 1 180); do
    if curl -sf "http://127.0.0.1:$PORT/health" > /dev/null 2>&1; then
      rc=0
      break
    fi
    kill -0 "$pid" 2>/dev/null || break
    sleep 2
  done
  kill "$pid" 2>/dev/null || true
  wait "$pid" 2>/dev/null || true
  sleep 3          # дать драйверу отпустить память до следующей попытки
  return $rc
}

while [ $(( HI - LO )) -gt $STEP ]; do
  MID=$(( ((LO + HI) / 2 / STEP) * STEP ))
  [ "$MID" -le "$LO" ] && break
  printf '%s  пробую ctx=%s ... ' "$(date +%H:%M:%S)" "$MID" | tee -a "$OUTDIR/log.txt"
  if probe "$MID"; then
    echo "влез" | tee -a "$OUTDIR/log.txt"
    LO=$MID
    BEST=$MID
  else
    echo "не влез" | tee -a "$OUTDIR/log.txt"
    HI=$MID
  fi
done

echo
if [ "$BEST" -eq 0 ]; then
  echo "НИ ОДИН контекст не поднялся на одной карте — смотри $OUTDIR/probe-*.log" | tee -a "$OUTDIR/log.txt"
  exit 1
fi
echo "МАКСИМУМ на одной карте: $BEST токенов (следующий шаг $(( BEST + STEP )) уже не влез)" | tee -a "$OUTDIR/log.txt"
echo "$BEST" > "$OUTDIR/max_ctx.txt"
echo "сырьё: $OUTDIR"
