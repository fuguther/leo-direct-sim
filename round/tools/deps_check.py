#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""依赖指纹漂移检查器（本线所有）。

读取 round/deps/DEPENDENCIES.md 表格中的 sha256（64 位十六进制），重算比对。
- 全部一致 → exit 0
- 任何 drift / 文件缺失 → exit 1 并列出（依赖变化必须显式报告，禁止静默换版）
用法: python3 deps_check.py [--manifest round/deps/DEPENDENCIES.md]
"""
from __future__ import annotations
import hashlib, os, re, sys

DEFAULT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "deps", "DEPENDENCIES.md")

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()

def main(argv):
    manifest = os.path.abspath(argv[argv.index("--manifest") + 1]) if "--manifest" in argv else os.path.abspath(DEFAULT)
    if not os.path.exists(manifest):
        print("MANIFEST_MISSING:", manifest); return 1
    text = open(manifest, encoding="utf-8").read()
    rows = re.findall(r"^\|([^|]+)\|([^|]+)\|([^|]+)\|\s*([0-9a-f]{64})\s*\|", text, re.M)
    if not rows:
        print("NO_FINGERPRINT_ROWS"); return 1
    drift, missing, ok = [], [], 0
    for name, path, owner, digest in rows:
        path = path.strip()
        if not os.path.exists(path):
            missing.append((name.strip(), path)); continue
        actual = sha256(path)
        if actual == digest:
            ok += 1
        else:
            drift.append((name.strip(), path, digest[:12], actual[:12]))
    print(f"fingerprint rows={len(rows)} ok={ok} drift={len(drift)} missing={len(missing)}")
    for n, p, o, a in drift:
        print(f"DRIFT {n} | {p} | manifest {o}.. -> actual {a}..")
    for n, p in missing:
        print(f"MISSING {n} | {p}")
    return 1 if (drift or missing) else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
