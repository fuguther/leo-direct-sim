#!/usr/bin/env python3
"""VM 批量 MinerU 转换：<itemKey>.pdf -> <itemKey>.md（并行分片，每片一个 mineru 进程）。
用法: python3 vm_mineru_batch.py <pdf_dir> <out_dir> [parallel_shards]
"""
import os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

MINERU = "/data/liguang13/mineru/.venv/bin/mineru"

def run_one(pdf: Path, out_dir: Path, shard: int):
    key = pdf.stem
    dest = out_dir / key
    md = dest / "auto" / (key + ".md")
    if md.exists() and md.stat().st_size > 1000:
        return (key, "skip", md.stat().st_size)
    dest.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env["MINERU_DEVICE_MODE"] = env.get("MINERU_DEVICE_MODE", "cuda")
    env["OMP_NUM_THREADS"] = "8"
    cmd = [MINERU, "-p", str(pdf), "-o", str(dest), "-b", "pipeline", "-d", "cuda"]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=1800, env=env)
    except subprocess.TimeoutExpired:
        return (key, "TIMEOUT", 0)
    if md.exists():
        return (key, "ok", md.stat().st_size)
    tail = (r.stderr or r.stdout or "")[-300:].replace("\n", " ")
    return (key, "FAIL: " + tail, 0)

def main():
    pdf_dir = Path(sys.argv[1]); out_dir = Path(sys.argv[2])
    shards = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    out_dir.mkdir(parents=True, exist_ok=True)
    pdfs = sorted(pdf_dir.glob("*.pdf"))
    print("pdfs:", len(pdfs), "shards:", shards, flush=True)
    t0 = time.time(); ok = skip = fail = 0
    with ThreadPoolExecutor(max_workers=shards) as ex:
        futs = {ex.submit(run_one, p, out_dir, i % shards): p for i, p in enumerate(pdfs)}
        for i, f in enumerate(as_completed(futs), 1):
            key, status, size = f.result()
            if status == "ok": ok += 1
            elif status == "skip": skip += 1
            else:
                fail += 1
                print("  FAIL", key, status[:200], flush=True)
            if i % 10 == 0:
                print("  [%d/%d] ok=%d skip=%d fail=%d %.0fs" % (i, len(pdfs), ok, skip, fail, time.time()-t0), flush=True)
    print("DONE ok=%d skip=%d fail=%d elapsed=%.1fs" % (ok, skip, fail, time.time()-t0), flush=True)

if __name__ == "__main__":
    main()