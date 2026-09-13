#!/usr/bin/env python3
"""P0 修复后指纹固化：重算 notes-neutral 当前 sha256，与 sanitizer 初次产出的 out_sha256 对照，
记录修改过的文件（即经人工定点修复者）。输出 notes-neutral-manifest-v2.json。"""
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NEU = ROOT / "round" / "knowledge" / "notes-neutral"
M1 = ROOT / "round" / "knowledge" / "notes-neutral-manifest.json"
OUT = ROOT / "round" / "knowledge" / "notes-neutral-manifest-v2.json"

m1 = json.loads(M1.read_text(encoding="utf-8"))
prev = {e["file"]: e.get("out_sha256") for e in m1["entries"]}
entries, changed = [], []
for f in sorted(NEU.glob("*.md")):
    b = f.read_bytes()
    h = hashlib.sha256(b).hexdigest()
    same = prev.get(f.name) == h
    entries.append({"file": f.name, "sha256": h, "changed_since_sanitize": not same})
    if not same:
        changed.append(f.name)

OUT.write_text(json.dumps({
    "generated": "2026-09-10",
    "stage": "post-P0-fix (语义抽查定点修复 + 3 处承重事实回补)",
    "supersedes_out_hashes_in": "notes-neutral-manifest.json",
    "files_total": len(entries),
    "files_changed_since_sanitize": len(changed),
    "changed_files": changed,
    "note": "sanitize 阶段 out_sha256 已过期；本文件为当前权威指纹。语义修复依据见 P0-SEMANTIC-SPOTCHECK.md。",
    "entries": entries,
}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"files={len(entries)} changed={len(changed)}")
for c in changed:
    print("  changed:", c)
