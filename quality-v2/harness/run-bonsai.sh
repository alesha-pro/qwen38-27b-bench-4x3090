#!/usr/bin/env bash
# quant-bench v2: Ternary Bonsai 2 27B (PrismML) on the PrismML llama.cpp fork, one card per instance.
#
# Protocol as run-rig-q4.sh (the published GGUF arms): llama-server --jinja, --reasoning-format deepseek,
# f16 KV (no -ctk), -fa on, unified KV pool, no context shift, effort through chat_template_kwargs,
# sampling from the client (llama-server's default min_p 0.05 applies, as on every GGUF arm).
# Engine: prism-b10743-adfffbe, linux CUDA 12.8 release binaries (newest pinned release on 2026-09-27).
#
# Effort gate: the model card says low reasons about as long as xhigh, so the token-gradient gate
# (low vs xhigh >= 2x) is informational here. The blocking check is that the rendered prompt carries
# the effort line from the chat template for low and xhigh.
set -uo pipefail

VAR="${1:?usage: run-bonsai.sh pq2|ptq1 <pool name, e.g. quarter0> <gpu>}"
IDX="${2:?}"
GPU="${3:?}"
BASE=$RUN_ROOT/quant-bench-v2
BIN=$ENGINE_ROOT/bonsai-llama-b10743/llama-prism-b10743-adfffbe/llama-server
case "$VAR" in
  pq2)  GGUF=$MODEL_ROOT/bonsai2-gguf/27B/Ternary-Bonsai-2-27B-PQ2_0.gguf; CTX=229376;;
  ptq1) GGUF=$MODEL_ROOT/Ternary-Bonsai-2-27B-gguf/Ternary-Bonsai-2-27B-PTQ1_0.gguf;       CTX=229376;;
  *) echo "bad variant"; exit 2;;
esac
RUN="quant-bonsai2-$VAR"
PAR=4   # 8 slots in 196K overflowed the unified KV 20x in 40 min (27.09): every overflow kills all active slots
PORT=$((19100 + GPU))
POOL="final-pool/$IDX.jsonl"   # 27.09 07:45 UTC: PTQ1 dropped, PQ2 moved to 4 cards on quarter pools
cd "$BASE"; mkdir -p runs
TAG="$RUN-$IDX"
log(){ echo "[$(date -u +%H:%M:%S)][$VAR/$IDX gpu$GPU] $*"; }
nvidia-smi --query-gpu=index,power.limit --format=csv,noheader > "runs/$TAG-power.txt"
log "gguf $GGUF, ctx $CTX, slots $PAR, port $PORT, pool $POOL"

CUDA_VISIBLE_DEVICES="$GPU" "$BIN" -m "$GGUF" \
  --host 127.0.0.1 --port "$PORT" --alias qwen3.8-27b \
  -ngl 999 -c "$CTX" --parallel "$PAR" --kv-unified \
  --jinja --reasoning-format deepseek --no-context-shift -fa on \
  >> "runs/$TAG-server.log" 2>&1 &
SPID=$!
trap 'log "stopping server"; kill $SPID 2>/dev/null; sleep 5; kill -9 $SPID 2>/dev/null' EXIT
for i in $(seq 1 240); do
  curl -sf "http://127.0.0.1:$PORT/v1/models" >/dev/null 2>&1 && { log "ready after $((i*5))s"; break; }
  kill -0 $SPID 2>/dev/null || { log "!! SERVER DIED"; tail -20 "runs/$TAG-server.log"; exit 1; }
  sleep 5; [ "$i" = 240 ] && { log "!! timeout"; exit 1; }
done

export QB2_LOCAL_BASE_URL="http://127.0.0.1:$PORT/v1" QB2_LOCAL_MODEL="qwen3.8-27b"
export QB2_EFFORT_TRANSPORT=chat_template_kwargs
export QB2_TIMEOUT=14400   # same as the Mirai S arm; 3600 was wall-clock, i.e. engine speed, not model (Alexey 27.09)
export PYTHONPATH="$BASE/harness"

log "=== EFFORT GATE (template) ==="
for e in low xhigh; do
  curl -s "http://127.0.0.1:$PORT/apply-template" -H 'Content-Type: application/json' \
    -d "{\"messages\":[{\"role\":\"user\",\"content\":\"hi\"}],\"chat_template_kwargs\":{\"reasoning_effort\":\"$e\"}}" \
    | grep -q "Reasoning effort is set to $e" || { log "!! effort $e not rendered by the template"; exit 1; }
done
log "OK: low and xhigh lines rendered"
if [ "$IDX" = quarter0 ]; then
  log "=== effort token gradient (informational) ==="
  ./venv/bin/python harness/effort_check.py || log "gradient gate below 2x (expected for this model, see card)"
fi

stage(){ log "=== STAGE: $* ==="
  ./venv/bin/python harness/run_devpool.py --run-name "$RUN" --pool "$POOL" --concurrency "$PAR" "$@" \
    || { log "!! stage failed: $*"; return 1; }; }
stage --efforts xhigh          --repeats 1
stage --efforts off low medium --repeats 1
stage --efforts xhigh          --repeats 3
stage --efforts xhigh          --repeats 3     # second pass: errors (context full, timeouts) get retried
stage --efforts off low medium --repeats 1
log "ALL DONE"
