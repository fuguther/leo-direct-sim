#!/usr/bin/env python3
"""VM 批量 MinerU 转换 v3：修正输出路径探测（递归查找 <key>.md），两遍策略。

用法: python3 vm_mineru_batch3.py <pdf_dir> <out_dir> [shards] [txt|ocr|both]
"""
import os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

MINERU = "/data/liguang13/mineru/.venv/bin/mineru"
MIN_CHARS = 3000

def find_md(out_dir: Path, key: str):
    """递归查找该 key 的 markdown（MinerU 输出层级随 method 变化）。"""
    base = out_dir / key
    if not base.exists(): return None
    cands = [p for p in base.rglob(key + ".md") if "_origin" not in p.name]
    if not cands:
        cands = [p for p in base.rglob("*.md") if "_origin" not in p.name]
    if not cands: return None
    return max(cands, key=lambda p: p.stat().st_size)

def run_one(pdf: Path, out_dir: Path, method: str):
    key = pdf.stem
    if key.startswith("._"): return (key, "junk", 0, 0.0)
    md = find_md(out_dir, key)
    if md is not None and md.stat().st_size >= MIN_CHARS:
        return (key, "skip", md.stat().st_size, 0.0)
    dest = out_dir / key
    dest.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ); env["OMP_NUM_THREADS"] = "8"
    cmd = [MINERU, "-p", str(pdf), "-o", str(dest), "-b", "pipeline", "-d", "cuda", "-m", method]
    t0 = time.time()
    try:
        subprocess.run(cmd, capture_output=True, text=True, timeout=2400, env=env)
    except subprocess.TimeoutExpired:
        return (key, "TIMEOUT", 0, time.time()-t0)
    dt = time.time() - t0
    md = find_md(out_dir, key)
    if md is not None and md.stat().st_size >= 100:
        return (key, "ok", md.stat().st_size, dt)
    return (key, "FAIL", 0, dt)

def main():
    pdf_dir = Path(sys.argv[1]); out_dir = Path(sys.argv[2])
    shards = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    which = sys.argv[4] if len(sys.argv) > 4 else "both"
    out_dir.mkdir(parents=True, exist_ok=True)
    pdfs = [p for p in sorted(pdf_dir.glob("*.pdf")) if not p.name.startswith("._")]
    print("pdfs: %d shards: %d pass: %s" % (len(pdfs), shards, which), flush=True)
    for method in (["txt"] if which == "txt" else ["ocr"] if which == "ocr" else ["txt", "ocr"]):
        t0 = time.time(); ok = skip = fail = 0; done = []
        with ThreadPoolExecutor(max_workers=shards) as ex:
            futs = [ex.submit(run_one, p, out_dir, method) for p in pdfs]
            for i, f in enumerate(as_completed(futs), 1):
                key, status, size, dt = f.result()
                if status == "ok": ok += 1; done.append((round(dt,1), key, size))
                elif status in ("skip", "junk"): skip += 1
                else: fail += 1; print("  FAIL[%s] %s" % (method, key), flush=True)
                if i % 10 == 0:
                    print("  [%s %d/%d] ok=%d skip=%d fail=%d %.0fs" % (method, i, len(pdfs), ok, skip, fail, time.time()-t0), flush=True)
        done.sort(reverse=True)
        print("PASS-%s DONE ok=%d skip=%d fail=%d elapsed=%.0fs slowest=%s" % (method, ok, skip, fail, time.time()-t0, done[:3]), flush=True)
    short = []
    for p in pdfs:
        md = find_md(out_dir, p.stem)
        if md is None: short.append((p.stem, -1))
        elif md.stat().st_size < MIN_CHARS: short.append((p.stem, md.stat().st_size))
    print("SHORT_OR_MISSING: %d -> %s" % (len(short), short[:15]), flush=True)

if __name__ == "__main__":
    main()