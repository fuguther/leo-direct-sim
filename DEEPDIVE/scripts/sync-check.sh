#!/usr/bin/env bash
# sync-check.sh — 本地与 VM 文献库一致性校验
# 用法: bash sync-check.sh
LOCAL="/private/tmp/leo-coldstart-deepdive-20260903/DEEPDIVE/v2/PAPER-LIBRARY"
REMOTE="vm:/data/论文/papers-lib/PAPER-LIBRARY"
echo "== 本地 =="
ls "$LOCAL" | wc -l
echo "== VM =="
ssh vm "ls /data/论文/papers-lib/PAPER-LIBRARY | wc -l"
echo "== MD5 抽样对比（本地随机 10 个文件）=="
for f in $(ls "$LOCAL" | sort -R | head -10); do
  lh=$(md5 -q "$LOCAL/$f" 2>/dev/null)
  rh=$(ssh vm "md5sum /data/论文/papers-lib/PAPER-LIBRARY/$f" 2>/dev/null | cut -d' ' -f1)
  if [ "$lh" = "$rh" ]; then echo "  ✓ $f"; else echo "  ✗ $f 不一致!"; fi
done
echo SYNC_CHECK_DONE
