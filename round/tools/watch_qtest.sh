#!/bin/bash
for i in $(seq 1 120); do
  if ! ssh vm "pgrep -f vm_mineru_quality_test >/dev/null" 2>/dev/null; then
    echo "=== QT FINISHED (checks=$i) ==="
    ssh vm "cat /data/liguang13/topic-loop-r2/qtest.log"
    exit 0
  fi
  sleep 30
done
echo "=== QT TIMEOUT ==="; ssh vm "cat /data/liguang13/topic-loop-r2/qtest.log"