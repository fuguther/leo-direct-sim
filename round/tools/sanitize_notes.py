#!/usr/bin/env python3
"""notes/raw -> notes-neutral 倾向剥离器（run2 输入链修复）。

规则（白名单 v3 配套）：
1. 块级删除：以「对账」「与我们对账」开头的行块（含其后续编号行），以及「连接：…」句。
2. 句级过滤：含黑名单词的句子整句删除（我们/机会点/信息阶梯/对账/F0/F1/旧候选/本线/选题/防火墙）。
   注意「候选路径/候选下一跳」等论文术语不含上述词，不受影响。
3. 残留扫描零容忍；输出 manifest（源 sha256、删除句数/块数）。
"""
import hashlib, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "LITERATURE" / "notes" / "raw"
DST = ROOT / "round" / "knowledge" / "notes-neutral"
MANIFEST = ROOT / "round" / "knowledge" / "notes-neutral-manifest.json"

BLACKLIST = re.compile(r"我们|机会点|信息阶梯|对账|F0|F1|旧候选|本线|选题|防火墙|倾向")
# 语义残留检测（2026-09-10 P0 抽查新增）：不含关键词但携带旧候选判断的表述。
# 仅用于残留报告，不做自动删除——语义裁决必须人工逐条进行（见 P0-SEMANTIC-SPOTCHECK.md）。
SEMANTIC_LEAK = re.compile(r"AoI-of-state|零差异|VM 实测|路由状态信息年龄|路由状态年龄|我的推测|holding/access|holding-access|路由状态新鲜度|状态新鲜度|可补的空|不作基线|机会点|可作为我们")
LEDGER_WORDS = re.compile(r"候选台账|候选卡|old_topic|CANDIDATE-LEDGER")
BLOCK_START = re.compile(r"^\s*(?:[-*]\s*)?(?:\*\*)?(?:与我们对账|对账)[:：]")
SECTION_BOUND = re.compile(r"^(?:\*\*(?:方法骨架|实验合同|可复用|危险信号|评级)|## |>\s*状态|---)")
CONNECT_SENT = re.compile(r"连接[:：]")
SENT_SPLIT = re.compile(r"(?<=[。！？；])")

def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def sanitize(text: str):
    out_lines, removed_blocks, removed_sents = [], 0, 0
    in_block = False
    for line in text.splitlines():
        stripped = line.strip()
        if in_block:
            # 对账块延续：编号行/普通行都删，直到遇到明确的新节边界或空行+节边界
            if SECTION_BOUND.match(stripped):
                in_block = False
            elif stripped == "":
                in_block = False
                out_lines.append(line)
                continue
            else:
                removed_blocks += 1
                continue
        if BLOCK_START.match(stripped):
            in_block = True
            removed_blocks += 1
            continue
        # 句级过滤（按中文句读切分，保留无黑名单的句）
        sents = [s for s in SENT_SPLIT.split(line) if s]
        kept = []
        for s in sents:
            if BLACKLIST.search(s) or LEDGER_WORDS.search(s) or CONNECT_SENT.search(s):
                removed_sents += 1
            else:
                kept.append(s)
        new = "".join(kept)
        if new.strip() or stripped == "":
            out_lines.append(new)
    return "\n".join(out_lines) + "\n", removed_blocks, removed_sents

def main():
    DST.mkdir(parents=True, exist_ok=True)
    manifest = []
    for f in sorted(SRC.glob("*.md")):
        raw = f.read_bytes()
        text = raw.decode("utf-8")
        clean, rb, rs = sanitize(text)
        # 残留零容忍校验
        residual = [s for s in SENT_SPLIT.split(clean) if BLACKLIST.search(s) or LEDGER_WORDS.search(s) or CONNECT_SENT.search(s)]
        entry = {
            "file": f.name,
            "source_sha256": sha256(raw),
            "source_relpath": "LITERATURE/notes/raw/" + f.name,
            "removed_blocks": rb,
            "removed_sentences": rs,
            "residual_hits": len(residual),
        }
        if residual:
            entry["residual_samples"] = [s[:80] for s in residual[:3]]
            manifest.append(entry)
            continue  # 不合格不写出
        (DST / f.name).write_text(clean, encoding="utf-8")
        entry["out_sha256"] = sha256(clean.encode("utf-8"))
        manifest.append(entry)
    bad = [m for m in manifest if m["residual_hits"] > 0]
    MANIFEST.write_text(json.dumps({
        "generated": "2026-09-10",
        "rule": "block-drop 对账/连接 + sentence-drop 黑名单(我们/机会点/信息阶梯/F0/F1/旧候选/本线/选题/防火墙/倾向)",
        "files_total": len(manifest),
        "files_clean": len(manifest) - len(bad),
        "entries": manifest,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"total={len(manifest)} clean={len(manifest)-len(bad)} bad={len(bad)}")
    for m in bad:
        print("RESIDUAL:", m["file"], m.get("residual_samples"))
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
