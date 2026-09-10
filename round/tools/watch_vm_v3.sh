#!/bin/bash
# 监听 VM MinerU v3 转换完成
for i in $(seq 1 240); do
  if ! ssh vm "pgrep -f vm_mineru_batch3 >/dev/null" 2>/dev/null; then
    echo "=== V3 CONVERSION FINISHED (checks=$i) ==="
    ssh vm "grep -E 'PASS-|SHORT' /data/liguang13/topic-loop-r2/batch3.log | tail -5"
    ssh vm "find /data/liguang13/topic-loop-r2/md -name '*.md' -not -name '*_origin*' | wc -l; du -sh /data/liguang13/topic-loop-r2/md"
    exit 0
  fi
  sleep 30
done
echo "=== TIMEOUT 2h ==="
ssh vm "tail -3 /data/liguang13/topic-loop-r2/batch3.log"