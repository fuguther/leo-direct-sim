#!/usr/bin/env python3
"""VM 转换守护：反复跑直到 111 篇全部产出，失败篇单独重试，最后出汇总。

用法（在 VM 上）: python3 vm_mineru_finish.py <pdf_dir> <out_dir> [max_rounds]
"""
import json, subprocess, sys, time
from pathlib import Path

ONE = "/data/liguang13/topic-loop-r2/scripts/vm_mineru_one.py"


def find_md(out_dir: Path, key: str):
    base = out_dir / key
    if not base.exists():
        return None
    cands = [p for p in base.rglob(key + ".md") if "_origin" not in p.name]
    return max(cands, key=lambda p: p.stat().st_size) if cands else None


def main():
    pdf_dir = Path(sys.argv[1]); out_dir = Path(sys.argv[2])
    max_rounds = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    pdfs = [p for p in sorted(pdf_dir.glob("*.pdf")) if not p.name.startswith("._")]
    for rnd in range(1, max_rounds + 1):
        missing = [p for p in pdfs if find_md(out_dir, p.stem) is None]
        print("ROUND %d: 缺 %d / 共 %d" % (rnd, len(missing), len(pdfs)), flush=True)
        if not missing:
            break
        keys = ",".join(p.stem for p in missing)
        cmd = [sys.executable, ONE, str(pdf_dir), str(out_dir), "pipeline_txt", "--only", keys]
        subprocess.run(cmd, timeout=3600 * 6)
        time.sleep(2)
    # 汇总
    done = [p.stem for p in pdfs if find_md(out_dir, p.stem) is not None]
    miss = [p.stem for p in pdfs if find_md(out_dir, p.stem) is None]
    total_bytes = sum(find_md(out_dir, k).stat().st_size for k in done)
    summary = {"total": len(pdfs), "done": len(done), "missing": miss,
               "total_md_bytes": total_bytes, "finished_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
    (out_dir / "CONVERSION-SUMMARY.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    print("FINAL done=%d missing=%d bytes=%d" % (len(done), len(miss), total_bytes), flush=True)
    if miss:
        print("MISSING:", miss, flush=True)


if __name__ == "__main__":
    main()