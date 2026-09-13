#!/bin/bash
# 监听 VM 转换全部完成（守护脚本退出即完成）
for i in $(seq 1 720); do
  if ! ssh vm "pgrep -f vm_mineru_finish >/dev/null" 2>/dev/null; then
    echo "=== VM CONVERSION ALL DONE (checks=$i) ==="
    ssh vm "tail -5 /data/liguang13/topic-loop-r2/finish.log; echo ---; cat /data/liguang13/topic-loop-r2/md/CONVERSION-SUMMARY.json 2>/dev/null"
    exit 0
  fi
  sleep 30
done
echo "=== WATCH TIMEOUT 6h ==="; ssh vm "tail -3 /data/liguang13/topic-loop-r2/finish.log"