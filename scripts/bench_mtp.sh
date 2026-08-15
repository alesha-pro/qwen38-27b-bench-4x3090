#!/usr/bin/env bash
# MTP: одиночная генерация со спекулятивным декодингом и без него.
#
#   bash bench_mtp.sh /path/model.gguf [карт]
#
# MTP-голова лежит внутри самого кванта (blk.64.nextn.*), отдельная драфт-модель
# не нужна. llama.cpp грузит эти тензоры только когда просят через --spec-type
# draft-mtp — без флага он их выбрасывает с warning "unused tensor ... ignoring".
#
# llama-bench спекулятивный декодинг не умеет, поэтому меряем через llama-server
# и bench_matrix.py на одном потоке.
set -euo pipefail

MODEL="${1:?укажи путь к .gguf}"
NGPU="${2:-1}"
PORT=18000
CTX="${CTX:-8192}"
GEN="${GEN:-256}"
NDRAFT="${NDRAFT:-3}"
BIN="${LLAMA_BIN:-$ENGINES/llama.cpp-rw/build/bin}"

STAMP="$(date +%Y-%m-%d-%H%M%S)"
OUTDIR="$BENCH_ROOT/output/mtp-$(basename "$MODEL" .gguf)-${NGPU}gpu-${STAMP}"
mkdir -p "$OUTDIR"
DEVS="$(seq -s, 0 $((NGPU - 1)))"

echo "модель: $MODEL"
echo "карт:   $NGPU, ctx $CTX, генерируем $GEN токенов, черновик $NDRAFT токена"
echo "выход:  $OUTDIR"

run_case() {
  local name="$1"; shift
  echo
  echo "=== $name ==="
  CUDA_VISIBLE_DEVICES="$DEVS" "$BIN/llama-server" \
    --model "$MODEL" \
    --host 127.0.0.1 --port "$PORT" \
    --alias bench \
    --n-gpu-layers 999 \
    --ctx-size "$CTX" \
    --parallel 1 \
    --flash-attn on \
    "$@" \
    > "$OUTDIR/server-$name.log" 2>&1 &
  local pid=$!
  local i ready=0
  for i in $(seq 1 120); do
    if curl -sf "http://127.0.0.1:$PORT/health" > /dev/null 2>&1; then ready=1; break; fi
    kill -0 "$pid" 2>/dev/null || break
    sleep 2
  done
  if [ "$ready" -eq 0 ]; then
    echo "сервер не поднялся:"; tail -20 "$OUTDIR/server-$name.log"
    kill "$pid" 2>/dev/null || true
    return 1
  fi

  # грузятся ли вообще тензоры MTP — единственный надёжный признак, что флаг сработал
  if grep -q "unused tensor blk.*nextn" "$OUTDIR/server-$name.log"; then
    echo "  ВНИМАНИЕ: тензоры nextn выброшены как unused — MTP НЕ включился"
  else
    echo "  тензоры nextn не выброшены — MTP на месте"
  fi

  python3 bench_matrix.py --port "$PORT" --model bench --levels 1 \
    --max-tokens "$GEN" --label "$name" --out "$OUTDIR/$name.json" \
    | tee "$OUTDIR/$name.txt" | grep -E "^c=|ПРОВАЛ"

  # llama-server пишет статистику черновика в лог по завершении запроса
  grep -aiE "draft acceptance|n_draft|accept" "$OUTDIR/server-$name.log" | tail -5 || true

  kill "$pid" 2>/dev/null || true
  wait "$pid" 2>/dev/null || true
  sleep 3
}

run_case "bez-mtp"
run_case "s-mtp" --spec-type draft-mtp --spec-draft-n-max "$NDRAFT"

echo
echo "готово: $OUTDIR"
echo "NB: выигрыш от спекулятивного декодинга зависит от того, насколько текст"
echo "предсказуем. Здесь temperature 0.7 и один фиксированный промпт — это одна"
echo "точка, а не универсальное число."
