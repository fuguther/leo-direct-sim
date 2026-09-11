#!/bin/bash
# 监听基线逐篇转换完成
for i in $(seq 1 480); do
  if ! ssh vm "pgrep -f vm_mineru_one >/dev/null" 2>/dev/null; then
    echo "=== ONE-BY-ONE BASELINE FINISHED (checks=$i) ==="
    ssh vm "grep -E '^DONE|SKIP|OK|FAIL' /data/liguang13/topic-loop-r2/one_txt.log | tail -8"
    ssh vm "find /data/liguang13/topic-loop-r2/md -name '*.md' -not -name '*_origin*' | wc -l; du -sh /data/liguang13/topic-loop-r2/md"
    exit 0
  fi
  sleep 30
done
echo "=== TIMEOUT 4h ==="
ssh vm "tail -3 /data/liguang13/topic-loop-r2/one_txt.log"