#!/usr/bin/env python3
"""MinerU 质量对比测试：同一篇 PDF 跑 4 种后端，报告耗时/字数/结构保留度。"""
import json, os, re, subprocess, sys, time
from pathlib import Path

MINERU = "/data/liguang13/mineru/.venv/bin/mineru"
pdf = Path(sys.argv[1])
base = Path(sys.argv[2])
key = pdf.stem
MODES = [
    ("pipeline_txt",   ["-b", "pipeline", "-m", "txt"]),
    ("pipeline_ocr",   ["-b", "pipeline", "-m", "ocr"]),
    ("vlm_engine",     ["-b", "vlm-engine"]),
    ("hybrid_high",    ["-b", "hybrid-engine", "--effort", "high"]),
]
env = dict(os.environ)
env["TMPDIR"] = "/data/liguang13/tmp"
Path(env["TMPDIR"]).mkdir(parents=True, exist_ok=True)
res = []
for name, args in MODES:
    dest = base / name
    dest.mkdir(parents=True, exist_ok=True)
    cmd = [MINERU, "-p", str(pdf), "-o", str(dest), "-d", "cuda"] + args
    t0 = time.time()
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=3600, env=env)
        err = (p.stderr or "")[-300:]
    except subprocess.TimeoutExpired:
        res.append({"mode": name, "status": "TIMEOUT", "sec": round(time.time()-t0, 1)}); continue
    dt = round(time.time() - t0, 1)
    mds = [m for m in dest.rglob("*.md") if "_origin" not in m.name]
    if not mds:
        res.append({"mode": name, "status": "FAIL", "sec": dt, "err": err[-200:]}); continue
    md = max(mds, key=lambda x: x.stat().st_size)
    t = md.read_text(encoding="utf-8", errors="ignore")
    imgs = len(list((md.parent / "images").glob("*"))) if (md.parent / "images").exists() else 0
    res.append({
        "mode": name, "status": "ok", "sec": dt,
        "chars": len(t), "imgs": imgs,
        "headings": len(re.findall(r"^#{1,4} ", t, flags=re.M)),
        "tables": len(re.findall(r"\|.*\|.*\|", t)),
        "formulas": len(re.findall(r"\$[^$]+\$", t)),
        "path": str(md),
    })
    print(json.dumps(res[-1], ensure_ascii=False), flush=True)
print("=== SUMMARY ===")
for r in res: print(json.dumps(r, ensure_ascii=False))