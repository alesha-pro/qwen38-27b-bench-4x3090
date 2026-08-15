#!/usr/bin/env bash
# MTP по глубине контекста: держится ли выигрыш спекулятивного декодинга,
# когда контекст растёт.
#
#   bash bench_mtp_depth.sh /path/model.gguf [карт]
#
# llama-bench спекулятивный декодинг не поддерживает, поэтому меряем через
# llama-server: подаём промпт нужной длины и смотрим скорость генерации после
# него. Сервер поднимается ДВА раза — с MTP и без, — и каждый проходит все
# глубины, чтобы сравнение шло на одной и той же загруженной модели.
set -euo pipefail

MODEL="${1:?укажи путь к .gguf}"
NGPU="${2:-1}"
PORT=18000
DEPTHS="${DEPTHS:-0 4096 16384 65536}"
GEN="${GEN:-256}"
NDRAFT="${NDRAFT:-3}"
BIN="${LLAMA_BIN:-$ENGINES/llama.cpp-rw/build/bin}"

# Контекст должен вместить самую глубокую точку плюс генерацию с запасом.
MAXD=0; for d in $DEPTHS; do [ "$d" -gt "$MAXD" ] && MAXD=$d; done
CTX=$(( MAXD + GEN + 2048 ))

STAMP="$(date +%Y-%m-%d-%H%M%S)"
OUTDIR="$BENCH_ROOT/output/mtpdepth-$(basename "$MODEL" .gguf)-${NGPU}gpu-${STAMP}"
mkdir -p "$OUTDIR"
DEVS="$(seq -s, 0 $((NGPU - 1)))"

echo "модель:  $MODEL"
echo "карт:    $NGPU, ctx $CTX, генерация $GEN токенов, черновик $NDRAFT"
echo "глубины: $DEPTHS"
echo "выход:   $OUTDIR"

run_config() {
  local name="$1"; shift
  echo
  echo "########## $name ##########"
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
  for i in $(seq 1 150); do
    curl -sf "http://127.0.0.1:$PORT/health" > /dev/null 2>&1 && { ready=1; break; }
    kill -0 "$pid" 2>/dev/null || break
    sleep 2
  done
  if [ "$ready" -eq 0 ]; then
    echo "сервер не поднялся на ctx=$CTX:"; tail -20 "$OUTDIR/server-$name.log"
    kill "$pid" 2>/dev/null || true
    return 1
  fi

  if grep -q "unused tensor blk.*nextn" "$OUTDIR/server-$name.log"; then
    echo "  тензоры nextn выброшены — MTP выключен"
  else
    echo "  тензоры nextn загружены — MTP включён"
  fi

  for d in $DEPTHS; do
    echo "-- глубина $d"
    if [ "$d" -eq 0 ]; then
      python3 bench_matrix.py --port "$PORT" --model bench --levels 1 \
        --max-tokens "$GEN" --label "$name d=$d" \
        --out "$OUTDIR/$name-d$d.json" > "$OUTDIR/$name-d$d.txt" 2>&1
    else
      python3 bench_matrix.py --port "$PORT" --model bench --levels 1 \
        --max-tokens "$GEN" --prompt-tokens "$d" --label "$name d=$d" \
        --out "$OUTDIR/$name-d$d.json" > "$OUTDIR/$name-d$d.txt" 2>&1
    fi
    grep -E "^c=" "$OUTDIR/$name-d$d.txt" || echo "   ПРОВАЛ, см. $name-d$d.txt"
    # приём черновика по последнему запросу
    grep -a "draft acceptance" "$OUTDIR/server-$name.log" | tail -1 \
      | sed 's/.*draft acceptance/   приём:/' || true
  done

  kill "$pid" 2>/dev/null || true
  wait "$pid" 2>/dev/null || true
  sleep 4
}

run_config "bez-mtp"
run_config "s-mtp" --spec-type draft-mtp --spec-draft-n-max "$NDRAFT"

echo
echo "== сводка =="
python3 - "$OUTDIR" "$DEPTHS" <<'PY'
import json, sys, pathlib
out = pathlib.Path(sys.argv[1])
depths = [int(x) for x in sys.argv[2].split()]
print(f"{'глубина':>9} {'без MTP':>10} {'с MTP':>10} {'выигрыш':>9}")
for d in depths:
    vals = {}
    for name in ("bez-mtp", "s-mtp"):
        p = out / f"{name}-d{d}.json"
        if not p.exists():
            continue
        try:
            lv = json.loads(p.read_text())["levels"][0]
        except Exception:
            continue
        vals[name] = lv.get("decode_tok_s_median")
    a, b = vals.get("bez-mtp"), vals.get("s-mtp")
    gain = f"{100 * (b / a - 1):+.1f}%" if a and b else "—"
    print(f"{d:>9} {a if a else '—':>10} {b if b else '—':>10} {gain:>9}")
PY

echo
echo "готово: $OUTDIR"
