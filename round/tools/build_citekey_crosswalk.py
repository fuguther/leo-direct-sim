#!/usr/bin/env python3
"""构建 Undermind cite_key 与 Zotero itemKey 的对照表（v2：分级置信度，防误配污染）。"""
import json, re
from pathlib import Path

txt = Path("round/zotero/undermind-gap-review.txt").read_text(encoding="utf-8")
um = [{"key": m.group(1), "title": m.group(2), "year": m.group(3)}
      for m in re.finditer(r"^\s{4}\[(\w+)\]\s+(.+?)\s+\((\d{4})\)\s*$", txt, flags=re.M)]
zot = json.load(open("round/zotero/index-raw.json"))

def toks(s): return set(re.findall(r"[a-z]{4,}", (s or "").lower()))

HIGH, MID = 0.75, 0.5
confident, review, none = [], [], []
for u in um:
    ut = toks(u["title"])
    scored = []
    for z in zot:
        zt = toks(z.get("title"))
        if not ut or not zt: continue
        scored.append((len(ut & zt) / max(1, len(ut | zt)), z))
    scored.sort(key=lambda x: -x[0])
    top = scored[0] if scored else (0.0, None)
    rec = {"cite_key": u["key"], "um_title": u["title"], "um_year": u["year"],
           "itemKey": (top[1] or {}).get("key"), "zot_title": (top[1] or {}).get("title"), "score": round(top[0], 2)}
    rec["runner_up"] = [{"itemKey": z["key"], "title": z.get("title"), "score": round(s, 2)} for s, z in scored[:3]]
    if top[0] >= HIGH: confident.append(rec)
    elif top[0] >= MID: review.append(rec)
    else: none.append(rec)

L = ["# Undermind cite_key 与 Zotero itemKey 对照表（v2 分级）", "",
     "> 用途：引用关系检索（citing / referenced 模式）需要 cite_key；Zotero 与 MinerU 精读需要 itemKey。本表打通二者。",
     "> 分级纪律：只把 confident 档（Jaccard >= 0.75）当作可信对照使用；",
     "> 待确认档（0.5 - 0.75）必须人工核对标题后才能用；未匹配档视为 Zotero 中尚无该论文（需下载 PDF 并转 MD）。",
     "> 理由：误配会静默污染下游（引用检索查错论文、证据对错条目）。", "",
     "生成 2026-09-10：共 %d 篇 → confident %d / 待确认 %d / 未匹配 %d" % (len(um), len(confident), len(review), len(none)), "",
     "## A. confident（可信对照）", "",
     "| cite_key | 年份 | Undermind 标题 | Zotero itemKey | 匹配度 |", "|---|---|---|---|---|"]
for r in sorted(confident, key=lambda x: x["cite_key"]):
    L.append("| %s | %s | %s | %s | %.2f |" % (r["cite_key"], r["um_year"], r["um_title"][:68].replace("|", "/"), r["itemKey"], r["score"]))
L += ["", "## B. 待人工确认（核对标题前不得使用）", "",
      "| cite_key | 年份 | Undermind 标题 | 候选 itemKey | 候选标题 | 匹配度 |", "|---|---|---|---|---|---|"]
for r in sorted(review, key=lambda x: x["cite_key"]):
    L.append("| %s | %s | %s | %s | %s | %.2f |" % (r["cite_key"], r["um_year"], r["um_title"][:55].replace("|", "/"), r["itemKey"], (r["zot_title"] or "")[:45].replace("|", "/"), r["score"]))
L += ["", "## C. 未匹配（Undermind 库内有、Zotero 无）", "",
      "| cite_key | 年份 | 标题 | 最佳本地候选 | 匹配度 |", "|---|---|---|---|---|"]
for r in sorted(none, key=lambda x: x["cite_key"]):
    L.append("| %s | %s | %s | %s | %.2f |" % (r["cite_key"], r["um_year"], r["um_title"][:60].replace("|", "/"), (r["zot_title"] or "-")[:40].replace("|", "/"), r["score"]))
Path("round/zotero/CITEKEY-CROSSWALK.md").write_text("\n".join(L) + "\n", encoding="utf-8")
json.dump({"confident": confident, "review": review, "none": none},
          open("round/zotero/citekey-crosswalk.json", "w"), ensure_ascii=False, indent=1)
print("confident=%d review=%d none=%d" % (len(confident), len(review), len(none)))
print()
print("=== confident ===")
for r in sorted(confident, key=lambda x: x["cite_key"]):
    print("  %-7s -> %-10s %.2f  %s" % (r["cite_key"], r["itemKey"], r["score"], r["zot_title"][:50]))
print()
print("=== review ===")
for r in sorted(review, key=lambda x: x["cite_key"]):
    print("  %-7s ~ %-10s %.2f  UM:%s | ZOT:%s" % (r["cite_key"], r["itemKey"], r["score"], r["um_title"][:36], (r["zot_title"] or "")[:32]))