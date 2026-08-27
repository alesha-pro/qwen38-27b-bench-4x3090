#!/usr/bin/env bash
# Ждём завершения FP8-расширения и пускаем AWQ на всех 300 задачах.
# Полный протокол: xhigh x1, off/low/medium x1, xhigh x3.
# Конкурентность оставлена штатной (4), как у FP8, чтобы сравнение армов
# на риге не тащило ещё и разницу в батчинге.
cd /mnt/nvme/work/benchmarks/quant-bench-v2
log(){ echo "[$(date -u +%H:%M:%S)] $*"; }
log "жду завершения fp8-ext"
while pgrep -f "run_quant_arm.sh fp8-ext" >/dev/null; do sleep 60; done
log "fp8-ext завершён, пауза 90с на освобождение GPU"
sleep 90
log "стартую AWQ, 300 задач, полный протокол"
QB2_POOL=final-pool/allpool.jsonl bash harness/run_quant_arm.sh awq /mnt/ssd/models/Qwen3.8-27B-AWQ-INT4
log "AWQ завершён"
