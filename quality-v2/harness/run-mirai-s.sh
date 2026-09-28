#!/usr/bin/env bash
# quant-bench v2: Mirai S Qwen3.8-27B (2.4-bit trellis) on Mirai's own vLLM plugin.
#
# Same protocol as harness/run_quant_arm.sh (bf16 KV, FLASH_ATTN, no prefix
# cache, qwen3 reasoning parser, qwen3_xml tools, 163840 ctx, Qwen card
# sampling from the client, no spec decode). Differences forced by the format:
#   - vLLM 0.30.0 + mirai_s 0.2.1 plugin ($ENGINE_ROOT/mirai-s-vllm-env),
#     the plugin has no TP, so each instance is PP=2 on a pair of cards;
#   - two instances, each takes one half of the 300-task pool (half0/half1).
# Before the arm: effort gate + one long generation checked for the
# "fresh instance degenerates on long outputs" failure seen on 2026-09-25.
set -uo pipefail

IDX="${1:?usage: run-mirai-s.sh 0|1}"
BASE=$RUN_ROOT/quant-bench-v2
ENV=$ENGINE_ROOT/mirai-s-vllm-env
WEIGHTS=$MODEL_ROOT/trymirai-Qwen3.8-27B-S-experimental/vllm
RUN=quant-mirai-s
CTX=163840
SEQS="${QB2_SEQS:-8}"   # 4 at the start (16:21-16:38 UTC 26.09), raised to 8: KV sat at 5%, cards were bound by concurrency
PORT=$((18310 + IDX))
case "$IDX" in 0) DEV=0,1;; 1) DEV=2,3;; *) echo "bad idx"; exit 2;; esac
POOL="final-pool/half$IDX.jsonl"

cd "$BASE"
mkdir -p runs
log() { echo "[$(date -u +%H:%M:%S)][$IDX] $*"; }

nvidia-smi --query-gpu=index,power.limit --format=csv,noheader > "runs/$RUN-power-$IDX.txt"
log "cards $DEV, port $PORT, seqs $SEQS, pool $POOL, power: $(tr '\n' ' ' < runs/$RUN-power-$IDX.txt)"

start_server() {
  CUDA_VISIBLE_DEVICES="$DEV" \
  CUDA_HOME=$ENGINE_ROOT/cuda13.0-nvcc/nvidia/cu13 \
  PATH=$ENGINE_ROOT/cuda13.0-nvcc/nvidia/cu13/bin:$PATH \
  VLLM_USE_FLASHINFER_SAMPLER=0 \
  HF_HOME=$HF_HOME \
  PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \
  "$ENV/bin/vllm" serve "$WEIGHTS" \
    --served-model-name qwen3.8-27b \
    --host 127.0.0.1 --port "$PORT" \
    --pipeline-parallel-size 2 \
    --max-model-len "$CTX" \
    --gpu-memory-utilization 0.90 \
    --kv-cache-dtype bfloat16 \
    --attention-backend FLASH_ATTN \
    --max-num-seqs "$SEQS" \
    --max-num-batched-tokens 2048 \
    --no-enable-prefix-caching \
    --reasoning-parser qwen3 \
    --enable-auto-tool-choice \
    --tool-call-parser qwen3_xml \
    --language-model-only \
    >> "runs/$RUN-server-$IDX.log" 2>&1 &
  SERVER_PID=$!
  log "server pid $SERVER_PID"
  for i in $(seq 1 360); do
    curl -sf "http://127.0.0.1:$PORT/v1/models" >/dev/null 2>&1 && { log "ready after $((i*5))s"; return 0; }
    if ! kill -0 "$SERVER_PID" 2>/dev/null; then
      log "!! SERVER DIED"; grep -iE "error|Traceback" "runs/$RUN-server-$IDX.log" | tail -15; return 1
    fi
    sleep 5
  done
  log "!! server start timeout"; return 1
}

stop_server() {
  [ -n "${SERVER_PID:-}" ] || return 0
  log "stopping server $SERVER_PID"
  kill -INT "$SERVER_PID" 2>/dev/null || true
  for _ in $(seq 1 60); do kill -0 "$SERVER_PID" 2>/dev/null || break; sleep 2; done
  kill -9 "$SERVER_PID" 2>/dev/null || true
  SERVER_PID=
  sleep 10
}
trap stop_server EXIT

export QB2_LOCAL_BASE_URL="http://127.0.0.1:$PORT/v1"
export QB2_LOCAL_MODEL="qwen3.8-27b"
export QB2_TIMEOUT=14400      # 131072 tokens at ~15 tok/s still finish; a timeout is missing data, not a fail

# Health: up to two fresh starts. A degenerate instance gets restarted, not used.
ok=0
for attempt in 1 2; do
  start_server || exit 1
  log "=== ANTI-FAKE GATE: effort must reach the model ==="
  if ! ./venv/bin/python harness/effort_check.py; then
    log "!! effort gate FAILED, refusing to run the arm"; exit 1
  fi
  log "=== HEALTH: one long xhigh generation, repetition per quarter ==="
  ./venv/bin/python harness/mirai_health.py --out "runs/$RUN-health-$IDX-a$attempt.json"
  rc=$?
  if [ "$rc" = 0 ] || [ "$rc" = 2 ]; then   # 2 = no long output to judge, not a failure
    ok=1; break
  fi
  log "!! health check failed on attempt $attempt, restarting the instance"
  stop_server
done
[ "$ok" = 1 ] || { log "!! instance unhealthy twice, giving up"; exit 1; }

stage() {
  log "=== STAGE: $* ==="
  ./venv/bin/python harness/run_devpool.py --run-name "$RUN" --pool "$POOL" \
     --concurrency "$SEQS" "$@" || { log "!! stage failed: $*"; return 1; }
}

stage --efforts xhigh          --repeats 1   # headline retention first
stage --efforts off low medium --repeats 1   # the effort curve
stage --efforts xhigh          --repeats 3   # r1 skipped, adds r2 and r3
# second pass picks up anything that errored (timeouts, server hiccups)
stage --efforts xhigh          --repeats 3
stage --efforts off low medium --repeats 1
log "ALL DONE: mirai-s half $IDX"
