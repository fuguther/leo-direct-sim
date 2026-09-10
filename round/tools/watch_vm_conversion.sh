#!/bin/bash
# 监听 VM 上 MinerU 批量转换完成
for i in $(seq 1 180); do
  if ! ssh vm "pgrep -f vm_mineru_batch.py >/dev/null" 2>/dev/null; then
    echo "=== CONVERSION FINISHED (checks=$i) ==="
    ssh vm "tail -4 /data/liguang13/topic-loop-r2/batch.log"
    echo "--- MD files ---"
    ssh vm "find /data/liguang13/topic-loop-r2/md -name '*.md' | wc -l; du -sh /data/liguang13/topic-loop-r2/md"
    exit 0
  fi
  sleep 30
done
echo "=== TIMEOUT 90min ==="
ssh vm "tail -3 /data/liguang13/topic-loop-r2/batch.log"