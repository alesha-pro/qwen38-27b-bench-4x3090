#!/usr/bin/env bash
# Главный прогон: single decode, prefill и падение скорости с глубиной контекста.
#
#   bash bench_depth.sh /path/model.gguf [карт] [метка]
#
# Задача от Алексея от 14.08: параллельность на llama.cpp не мерим, мерим
# одиночный поток и то, как он проседает по мере роста контекста.
#
# llama-bench делает ровно это: -p даёт prefill (pp), -n даёт decode (tg),
# -d задаёт, сколько токенов уже лежит в контексте к моменту замера.
set -euo pipefail

MODEL="${1:?укажи путь к .gguf}"
NGPU="${2:-4}"
LABEL="${3:-$(basename "$MODEL" .gguf)}"

DEPTHS="${DEPTHS:-0,4096,16384,65536,131072}"
PP="${PP:-4096}"          # длина промпта для prefill
TG="${TG:-128}"           # сколько токенов генерим для decode
REPS="${REPS:-3}"
BIN="${LLAMA_BIN:-$ENGINES/llama.cpp-rw/build/bin}"

STAMP="$(date +%Y-%m-%d-%H%M%S)"
OUTDIR="$BENCH_ROOT/output/depth-${LABEL}-${NGPU}gpu-${STAMP}"
mkdir -p "$OUTDIR"

DEVS="$(seq -s, 0 $((NGPU - 1)))"

{
  echo "модель:  $MODEL"
  echo "карт:    $NGPU (CUDA_VISIBLE_DEVICES=$DEVS)"
  echo "глубины: $DEPTHS"
  echo "pp=$PP tg=$TG повторов=$REPS"
  echo "бинарь:  $BIN ($("$BIN/llama-bench" --version 2>&1 | grep -o 'build [0-9]*' || echo '?'))"
  nvidia-smi --query-gpu=index,power.limit --format=csv,noheader
} | tee "$OUTDIR/setup.txt"

echo
echo "== пошло, это надолго: чем глубже контекст, тем дольше прогрев каждой точки"

# Глубины гоняем ПО ОДНОЙ, а не одним вызовом со списком. 14.08 на одной карте
# llama-bench не смог создать контекст на 131072 и оборвался, унеся с собой json
# с восемью уже посчитанными точками. Отдельный вызов на глубину означает, что
# провал самой глубокой точки не отменяет всё, что посчиталось до неё, — а сам
# факт «сюда уже не влезает» тоже результат и его надо записать.
echo "[" > "$OUTDIR/bench.json"
FIRST=1
: > "$OUTDIR/bench.err"
for D in ${DEPTHS//,/ }; do
  echo "-- глубина $D"
  if CUDA_VISIBLE_DEVICES="$DEVS" "$BIN/llama-bench" \
      --model "$MODEL" \
      --n-gpu-layers 999 \
      --flash-attn on \
      --n-prompt "$PP" \
      --n-gen "$TG" \
      --n-depth "$D" \
      --repetitions "$REPS" \
      --progress \
      -o json > "$OUTDIR/d$D.json" 2>> "$OUTDIR/bench.err"; then
    python3 -c "
import json,sys
rows=json.load(open('$OUTDIR/d$D.json'))
out=open('$OUTDIR/bench.json','a')
for r in rows:
    out.write(('' if $FIRST and r is rows[0] else ',') + json.dumps(r, indent=2))
" && FIRST=0
    echo "   ок"
  else
    echo "   НЕ ВЛЕЗЛО на глубине $D — дальше не иду, предыдущие точки сохранены"
    echo "$D" > "$OUTDIR/failed_depth.txt"
    break
  fi
done
echo "]" >> "$OUTDIR/bench.json"

python3 - "$OUTDIR/bench.json" "$NGPU" <<'PY' | tee "$OUTDIR/table.txt"
import json, sys
rows = json.load(open(sys.argv[1]))
print(f"\n== {rows[0]['model_filename'] if rows else '?'} на {sys.argv[2]} картах ==")
print(f"{'тест':>12} {'глубина':>9} {'tok/s':>10} {'±':>7}")
base = {}
for r in rows:
    kind = 'prefill' if r['n_prompt'] else 'decode'
    d = r.get('n_depth', 0)
    ts, sd = r['avg_ts'], r.get('stddev_ts', 0)
    base.setdefault(kind, ts)
    drop = f"  {100*ts/base[kind]:5.1f}% от глубины 0" if base[kind] else ""
    print(f"{kind:>12} {d:>9} {ts:>10.2f} {sd:>7.2f}{drop}")
PY

echo
echo "готово: $OUTDIR"
