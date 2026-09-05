#!/usr/bin/env bash
# pdf2md.sh — MinerU PDF→Markdown 提取层（深潜管线 v2 标准提取器）
# 替代 pdftotext（修复 A2 实测的数学散字乱码：如 "f t xt (u, v, G(Edt )..."）
# 用法: pdf2md.sh <input.pdf> <outdir> [pipeline|hybrid-engine]
# 实测: ieee-10375570 TCOM 论文 散字行 1→0, 公式完整, 682行 MD
set -euo pipefail
export HF_HOME="${HF_HOME:-/private/tmp/hf-cache}"
export HF_HUB_CACHE="${HF_HUB_CACHE:-/private/tmp/hf-cache}"
MINERU="${MINERU_BIN:-/private/tmp/mineru-venv/bin/mineru}"
PDF="$1"; OUT="$2"; BACKEND="${3:-pipeline}"
[ -f "$PDF" ] || { echo "FATAL: 找不到 $PDF" >&2; exit 1; }
echo "[pdf2md] $PDF -> $OUT ($BACKEND)"
mkdir -p "$OUT"
"$MINERU" -p "$PDF" -o "$OUT" -b "$BACKEND" -l en 2>/dev/null \
  || { echo "WARN: $BACKEND 失败, 回退 pipeline" >&2; "$MINERU" -p "$PDF" -o "$OUT" -b pipeline -l en; }
MD=$(find "$OUT" -name "*.md" | head -1)
[ -n "$MD" ] || { echo "FATAL: 无 Markdown 产出" >&2; exit 2; }
echo "[pdf2md] OK: $MD ($(wc -l < "$MD") 行)"
