#!/usr/bin/env python3
"""MinerU 逐篇转换队列（一篇一篇、串行、可断点续跑、质量记录）。

设计要点（按用户要求"一篇一篇、要最好的"）：
- 串行处理：每篇独占 GPU，避免并行争抢导致的显存抖动与降级；
- 断点续跑：已有合格 md 的跳过；
- 质量记录：每篇记录字符数/页数/标题数/表格数/公式数/图片数/耗时，写 results.json；
- 失败重试：先按主模式跑，失败则该篇记录失败原因，不改用低质量模式（质量优先）。

用法:
  python3 vm_mineru_one.py <pdf_dir> <out_dir> <mode> [--limit N] [--only KEY,KEY]
  mode ∈ pipeline_txt | pipeline_ocr | vlm | hybrid_high | hybrid_medium
"""
import argparse, json, os, re, subprocess, sys, time
from pathlib import Path

MINERU = "/data/liguang13/mineru/.venv/bin/mineru"
MIN_CHARS = 2000

MODE_ARGS = {
    "pipeline_txt":   ["-b", "pipeline", "-m", "txt"],
    "pipeline_ocr":   ["-b", "pipeline", "-m", "ocr"],
    "vlm":            ["-b", "vlm-engine"],
    "hybrid_medium":  ["-b", "hybrid-engine", "--effort", "medium"],
    "hybrid_high":    ["-b", "hybrid-engine", "--effort", "high"],
}

def find_md(out_dir: Path, key: str):
    base = out_dir / key
    if not base.exists(): return None
    cands = [p for p in base.rglob("*.md") if "_origin" not in p.name]
    return max(cands, key=lambda p: p.stat().st_size) if cands else None

def stats(md: Path):
    t = md.read_text(encoding="utf-8", errors="ignore")
    imgs = len(list((md.parent / "images").glob("*"))) if (md.parent / "images").exists() else 0
    return {
        "chars": len(t),
        "pages": t.count("===== PAGE ") or len(re.findall(r"\n\s*#{0,3}\s*\d+\s*\n", t)) or 0,
        "headings": len(re.findall(r"^#{1,4} ", t, flags=re.M)),
        "tables_pipe": len(re.findall(r"^\|.*\|\s*$", t, flags=re.M)),
        "tables_html": len(re.findall(r"<table", t, flags=re.I)),
        "formulas": len(re.findall(r"\$[^$\n]{2,}\$", t)),
        "imgs": imgs,
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf_dir"); ap.add_argument("out_dir"); ap.add_argument("mode", choices=list(MODE_ARGS))
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--only", default="")
    ap.add_argument("--timeout", type=int, default=3600)
    a = ap.parse_args()
    pdf_dir, out_dir = Path(a.pdf_dir), Path(a.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    res_path = out_dir / ("results_%s.json" % a.mode)
    results = json.loads(res_path.read_text()) if res_path.exists() else {}

    pdfs = [p for p in sorted(pdf_dir.glob("*.pdf")) if not p.name.startswith("._")]
    if a.only:
        want = {k.strip() for k in a.only.split(",") if k.strip()}
        pdfs = [p for p in pdfs if p.stem in want]
    if a.limit: pdfs = pdfs[:a.limit]

    env = dict(os.environ)
    env["TMPDIR"] = "/data/liguang13/tmp"; Path(env["TMPDIR"]).mkdir(parents=True, exist_ok=True)
    env["OMP_NUM_THREADS"] = "16"

    print("MODE=%s PDFS=%d OUT=%s" % (a.mode, len(pdfs), out_dir), flush=True)
    t_all = time.time()
    ok = skip = fail = 0
    for i, pdf in enumerate(pdfs, 1):
        key = pdf.stem
        prev = results.get(key, {})
        if prev.get("status") == "ok" and prev.get("chars", 0) >= MIN_CHARS:
            skip += 1; print("[%d/%d] SKIP %s (%d chars)" % (i, len(pdfs), key, prev["chars"]), flush=True); continue
        dest = out_dir / key
        dest.mkdir(parents=True, exist_ok=True)
        cmd = [MINERU, "-p", str(pdf), "-o", str(dest), "-d", "cuda"] + MODE_ARGS[a.mode]
        t0 = time.time()
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=a.timeout, env=env)
            err = (p.stderr or p.stdout or "")[-400:]
        except subprocess.TimeoutExpired:
            results[key] = {"status": "timeout", "sec": round(time.time()-t0,1), "mode": a.mode}
            fail += 1; res_path.write_text(json.dumps(results, ensure_ascii=False, indent=1))
            print("[%d/%d] TIMEOUT %s" % (i, len(pdfs), key), flush=True); continue
        dt = round(time.time()-t0, 1)
        md = find_md(out_dir, key)
        if md is None or md.stat().st_size < 200:
            results[key] = {"status": "fail", "sec": dt, "mode": a.mode, "err": err[-250:]}
            fail += 1
            print("[%d/%d] FAIL %s :: %s" % (i, len(pdfs), key, err[-160:].replace("\n"," ")), flush=True)
        else:
            st = stats(md); st.update({"status": "ok", "sec": dt, "mode": a.mode, "md": str(md)})
            results[key] = st; ok += 1
            print("[%d/%d] OK %s chars=%d heads=%d tbl=%d/%d eq=%d imgs=%d %.0fs" % (
                i, len(pdfs), key, st["chars"], st["headings"], st["tables_pipe"], st["tables_html"],
                st["formulas"], st["imgs"], dt), flush=True)
        res_path.write_text(json.dumps(results, ensure_ascii=False, indent=1))
    print("DONE mode=%s ok=%d skip=%d fail=%d total=%.0fs" % (a.mode, ok, skip, fail, time.time()-t_all), flush=True)

if __name__ == "__main__":
    main()