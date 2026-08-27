#!/usr/bin/env bash
# quant-bench v2: one quantized arm, full protocol.
#
# Protocol (decisions 2026-08-22/24):
#   - bf16 KV on EVERY local arm. The 2026-08-24 KV canary measured fp8 cache at
#     ~5x the plumbing noise floor, so mixing it into the weight axis would be a
#     real error. v1 ran fp8 cache; v2 does not.
#   - FLASH_ATTN. Same canary put backend choice AT the noise floor (KL 0.0089,
#     top-1 20/20), and fp8 cache was the only reason v1 needed FlashInfer.
#   - efforts off/low/medium once, xhigh three times, so every format carries its
#     own noise estimate.
#   - identical server flags for every format: the arm-to-arm comparison is the
#     product, absolute numbers are secondary.
set -uo pipefail

ARM="${1:?usage: run_quant_arm.sh <arm-name> <weights-path> [quantization]}"
WEIGHTS="${2:?}"
QUANT="${3:-}"

BASE=/mnt/nvme/work/benchmarks/quant-bench-v2
VENV="$BASE/venv/bin/python"
VLLM=/mnt/nvme/engines/vllm-env/bin/vllm
PORT=18000
CTX=163840          # 131072 output ceiling + prompt headroom; no task comes close
SEQS=4
# Pool and stage set are overridable so the same protocol can be run over
# the 24.08 extension pool (extpool.jsonl, 200 tasks) without touching the
# frozen 100. The extension is measured at xhigh only: the effort curve is
# already settled on the first 100 and needs no extra power.
POOL="${QB2_POOL:-final-pool/finalpool.jsonl}"
XHIGH_ONLY="${QB2_XHIGH_ONLY:-0}"
RUN="quant-$ARM"

cd "$BASE"
mkdir -p runs

log() { echo "[$(date -u +%H:%M:%S)] $*"; }

nvidia-smi --query-gpu=index,power.limit --format=csv,noheader > "runs/$RUN-power.txt"
log "power limit: $(tr '\n' ' ' < runs/$RUN-power.txt)"

QUANT_ARG=()
[ -n "$QUANT" ] && QUANT_ARG=(--quantization "$QUANT")

log "starting vLLM: $ARM ($WEIGHTS)"
VLLM_ATTENTION_BACKEND=FLASH_ATTN VLLM_USE_FLASHINFER_SAMPLER=0 \
HF_HOME=/mnt/ssd/hf_cache VLLM_CACHE_ROOT=/mnt/ssd/caches/vllm \
PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \
"$VLLM" serve "$WEIGHTS" \
  --served-model-name qwen3.8-27b \
  --host 127.0.0.1 --port "$PORT" \
  --tensor-parallel-size 4 \
  --max-model-len "$CTX" \
  --gpu-memory-utilization 0.90 \
  --kv-cache-dtype bfloat16 \
  --max-num-seqs "$SEQS" \
  --no-enable-prefix-caching \
  --reasoning-parser qwen3 \
  --enable-auto-tool-choice \
  --tool-call-parser qwen3_xml \
  --language-model-only \
  --trust-remote-code \
  "${QUANT_ARG[@]}" \
  > "runs/$RUN-server.log" 2>&1 &
SERVER_PID=$!

cleanup() {
  log "stopping server $SERVER_PID"
  kill "$SERVER_PID" 2>/dev/null || true
  for _ in $(seq 1 60); do kill -0 "$SERVER_PID" 2>/dev/null || break; sleep 2; done
  kill -9 "$SERVER_PID" 2>/dev/null || true
}
trap cleanup EXIT

for i in $(seq 1 480); do
  curl -sf "http://127.0.0.1:$PORT/v1/models" >/dev/null 2>&1 && { log "ready after $((i*5))s"; break; }
  if ! kill -0 "$SERVER_PID" 2>/dev/null; then
    log "!! SERVER DIED"; grep -iE "error|Traceback|not support" "runs/$RUN-server.log" | tail -15; exit 1
  fi
  sleep 5
  [ "$i" = 480 ] && { log "!! timeout"; exit 1; }
done

export QB2_LOCAL_BASE_URL="http://127.0.0.1:$PORT/v1"
export QB2_LOCAL_MODEL="qwen3.8-27b"

log "=== ANTI-FAKE GATE: effort must reach the model ==="
if ! "$VENV" harness/effort_check.py; then
  log "!! effort gate FAILED, refusing to run the arm"; exit 1
fi

stage() {
  log "=== STAGE: $* ==="
  "$VENV" harness/run_devpool.py --run-name "$RUN" --pool "$POOL" \
     --concurrency "$SEQS" "$@" || { log "!! stage failed: $*"; return 1; }
}

if [ "$XHIGH_ONLY" = "1" ]; then
  stage --efforts xhigh        --repeats 3   # extension: retention only
else
  stage --efforts xhigh        --repeats 1   # headline retention first
  stage --efforts off low medium --repeats 1 # the effort curve
  stage --efforts xhigh        --repeats 3   # r1 skipped, adds r2 and r3
fi

log "=== SCORING ==="
"$VENV" harness/score_run.py --run-name "$RUN" --pool "$POOL" | tee "runs/$RUN-scored.txt"
log "ALL DONE: $ARM"
