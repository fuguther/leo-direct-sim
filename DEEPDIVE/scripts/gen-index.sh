#!/usr/bin/env bash
# gen-index.sh — 重建 LIBRARY-INDEX.md 并提交
cd /private/tmp/leo-coldstart-deepdive-20260903
python3 - <<'PYEOF'
import os, glob
LIB = "DEEPDIVE/v2/PAPER-LIBRARY"
files = sorted(glob.glob(LIB + "/*"))
def kind(f):
    b = os.path.basename(f)
    return "PDF" if b.endswith(".pdf") else ("MD" if b.endswith(".md") else "TXT")
rows = ["| 文件 | 类型 | 大小 |", "|---|---|---|"]
for f in files:
    b = os.path.basename(f)
    rows.append(f"| {b[:70]} | {kind(f)} | {os.path.getsize(f)//1024}KB |")
pdfs = len([f for f in files if f.endswith(".pdf")]); mds = len([f for f in files if f.endswith(".md")]); txts = len([f for f in files if f.endswith(".txt")])
head = f"# 统一文献库索引 v4\n\n位置: DEEPDIVE/v2/PAPER-LIBRARY/ — {len(files)} 文件(PDF {pdfs} / MD {mds} / TXT {txts})。VM 副本: /data/论文/papers-lib/PAPER-LIBRARY/\n\n"
open("DEEPDIVE/v2/LIBRARY-INDEX.md", "w").write(head + "\n".join(rows))
print(f"索引: {len(rows)} 行")
PYEOF
git add DEEPDIVE/v2/LIBRARY-INDEX.md
git -c user.name=agent -c user.email=agent@local commit -m "docs: 索引重建" --quiet
git push --quiet
echo INDEX_DONE
