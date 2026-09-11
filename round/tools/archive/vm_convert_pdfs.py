#!/usr/bin/env python3
"""VM 批量转换：Zotero PDF -> 纯文本（带页标记）。并行，自包含。
用法: python3 vm_convert_pdfs.py <manifest.json> <pdf_dir> <out_dir> [workers]
"""
import json, os, sys, time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

def convert_one(args):
    itemKey, pdf_path, out_dir = args
    out = Path(out_dir) / (itemKey + ".txt")
    if out.exists() and out.stat().st_size > 500:
        return (itemKey, "skip", out.stat().st_size, 0)
    try:
        import fitz  # pymupdf
        doc = fitz.open(pdf_path)
        parts = []
        for i, page in enumerate(doc, 1):
            parts.append("\n===== PAGE %d =====\n" % i)
            parts.append(page.get_text("text"))
        n = doc.page_count
        doc.close()
        txt = "".join(parts)
        out.write_text(txt, encoding="utf-8")
        return (itemKey, "ok", len(txt), n)
    except Exception as e:
        return (itemKey, "ERROR: %s" % repr(e)[:150], 0, 0)

def main():
    man = json.load(open(sys.argv[1]))
    pdf_dir = Path(sys.argv[2])
    out_dir = Path(sys.argv[3]); out_dir.mkdir(parents=True, exist_ok=True)
    workers = int(sys.argv[4]) if len(sys.argv) > 4 else 64
    jobs = []
    for m in man:
        p = pdf_dir / (m["itemKey"] + ".pdf")
        if p.exists():
            jobs.append((m["itemKey"], str(p), str(out_dir)))
    print("jobs:", len(jobs), "workers:", workers, flush=True)
    t0 = time.time(); ok = err = skip = 0; chars = 0
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(convert_one, j) for j in jobs]
        for i, f in enumerate(as_completed(futs), 1):
            key, status, size, pages = f.result()
            if status == "ok": ok += 1; chars += size
            elif status == "skip": skip += 1; chars += size
            else: err += 1; print("  FAIL", key, status, flush=True)
            if i % 25 == 0:
                print("  progress %d/%d  %.1fs" % (i, len(jobs), time.time()-t0), flush=True)
    print("DONE ok=%d skip=%d err=%d chars=%d elapsed=%.1fs" % (ok, skip, err, chars, time.time()-t0))

if __name__ == "__main__":
    main()