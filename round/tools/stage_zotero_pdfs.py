#!/usr/bin/env python3
"""把 manifest 里的 PDF 复制成 <itemKey>.pdf 到一个暂存目录，便于 rsync 到 VM。"""
import json, shutil, sys
from pathlib import Path
man = json.load(open("round/zotero/pdf-manifest.json"))
st = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/zotero-pdfs")
st.mkdir(parents=True, exist_ok=True)
n = 0
for m in man:
    dst = st / (m["itemKey"] + ".pdf")
    if not dst.exists():
        shutil.copy2(m["src"], dst)
    n += 1
print("staged:", n, "at", st)