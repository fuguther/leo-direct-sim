#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""候选台账 CLI v2（本线所有）——替代 round/tools/ledger_add.py。

ledger_add.py 缺陷复现: round/logs/repro-ledger-cli.txt（spec_from_file_location+exec_module
在 Python 3.14.2 触发 dataclass AttributeError，根因=模块未注册 sys.modules；本工具自带
数据结构，运行期不依赖跨 checkout 的 pool.py）+ round/logs/repro-group2.txt（批内重复/重试
幂等缺失为本线原实现缺陷，主控自认）。

语义（对应深审第三组）:
- 只追加不改写历史；cand_id 稳定；当前版本 = 同 cand_id 最大 version 行。
- content_hash 幂等：add 遇同 cand_id 同 content_hash → 跳过（重复/重试不重复入账）。
- 同批重复：批内投影实时更新，同键第二张 → 同 cand_id 的新版本行 + note 标记待主控合并。
- 修订 revise = 同 cand_id version+1、supersedes_row 指旧行；承重字段（条件/困难/原因/改动/
  替代/决策变化/新证据）发生实质变化 → 自动把 reviews.csv 中审过旧 content_hash 的意见置
  needs_review（归一化仅折叠空白：非承重字段修改不触发；承重字段仅纯空白差异不触发；承重字段的标点/符号/小数点变化即触发）。
- 旧题匹配只报告（old_topic_match + stdout OLD_TOPIC_MATCH），不自动淘汰；处置权在主控
  （revise/status/merge）。判定语义归一化复制自 pool.py@sha256:15989feaeedc497d。
- new_evidence 非空必须同时给 --evidence-source 与 --evidence-judgment（主控判定），否则拒绝。
- 状态词表: backlog(待建设) awaiting_evidence(待证据) needs_revision(需修订)
  recommended_pending_review(推荐待审) archived(归档) merged(合并簿记)。
- 中断恢复: 追加即时 flush+fsync；doctor 报告完整性问题；R3 起停用破坏性截断——原件保留，--repair-out 产出重建候选文件由人采纳。

用法:
  python3 ledger.py add --cards cards.json --ledger L.csv [--old OLD.csv] [--writer WHO]
  python3 ledger.py revise --cand-id ID --set '{"difficulty":"新值"}' --reason "为何" --ledger L.csv [--status S]
  python3 ledger.py status --cand-id ID --status awaiting_evidence --reason "为何" --ledger L.csv
  python3 ledger.py show --ledger L.csv [--all]
  python3 ledger.py doctor --ledger L.csv [--backup] [--repair-out PATH]
  python3 ledger.py review-register --review-id R1 --cand-id ID --content-hash H --role builder --file F --reviews RV.csv --candidate-file CAND.md --verify-ledger L.csv
  python3 ledger.py invalidate-reviews --cand-id ID --content-hash H --reviews RV.csv
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
from pathlib import Path
import sys
import time

CARD_FIELDS = ("title", "conditions", "difficulty", "cause_hypothesis", "possible_change",
               "strongest_alternative", "decision_shift", "next_cheap_check")
EVIDENCE_FIELDS = ("new_evidence", "new_evidence_source", "evidence_judgment")
LOAD_BEARING = ("conditions", "difficulty", "cause_hypothesis", "possible_change",
                "strongest_alternative", "decision_shift", "new_evidence")
STATUSES = ("backlog", "awaiting_evidence", "needs_revision",
            "recommended_pending_review", "archived", "merged")

# 审查登记表（R4 补强）：ledger_content_hash=台账 canonical 字段哈希；
# candidate_file/candidate_file_sha256=被审候选文件及其 sha256（工具实算，非人工传参）。
REVIEWS_HEADER = ["review_id", "cand_id", "ledger_content_hash", "candidate_file",
                  "candidate_file_sha256", "role", "file", "status", "updated_at", "note"]

HEADER = ["row_no", "cand_id", "version", "op", "status", "title"] + list(CARD_FIELDS[1:]) + [
    "new_evidence", "new_evidence_source", "evidence_judgment", "old_topic_match",
    "similar_to", "merged_into", "supersedes_row", "content_hash", "source", "writer", "written_at", "note"]

# 归一化语义复制自 research-ops pool.py（sha256 前缀 15989feaeedc497d），保持合并键可比
_STRIP = re.compile(r"[^\w]+")


def _norm(text) -> str:
    return _STRIP.sub("", (text or "").lower())[:240]


def merge_key(card: dict):
    return tuple(_norm(card.get(f, "")) for f in ("difficulty", "cause_hypothesis", "decision_shift"))


def cand_id_for(card: dict) -> str:
    return "c" + hashlib.sha256("|".join(merge_key(card)).encode("utf-8")).hexdigest()[:10]


def content_hash(card: dict) -> str:
    canon = "|".join(str(card.get(k, "") or "").strip() for k in
                     ("title",) + CARD_FIELDS[1:] + ("new_evidence", "new_evidence_source", "source"))
    return "h" + hashlib.sha256(canon.encode("utf-8")).hexdigest()[:12]


def _norm_lb(text) -> str:
    """承重比较归一化（R3 修复1）：仅折叠空白——至多忽略纯空白差异。
    正负号/不等号/小数点等一切符号与标点改变都算承重变化，触发审查失效。"""
    return re.sub(r"\s+", " ", (text or "").lower()).strip()


# ------------------------------------------------------------------ IO ----

def _read_ledger(path: str):
    rows, bad = [], []
    if not os.path.exists(path):
        return rows, bad
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if header is None:
            return rows, bad
        for i, r in enumerate(reader, start=2):
            if len(r) != len(header):
                bad.append({"line": i, "reason": "field_count %d != %d" % (len(r), len(header)), "raw": r})
                continue
            rows.append(dict(zip(header, r)))
    return rows, bad


def _check_schema(path: str) -> bool:
    """目标台账必须是当前 schema（防跨版本混写）。不匹配 → False。"""
    if not os.path.exists(path):
        return True
    with open(path, newline="", encoding="utf-8") as f:
        header = f.readline().rstrip("\n\r")
    return header == ",".join(HEADER)


def _append(path: str, row: dict) -> None:
    new = not os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADER)
        if new:
            w.writeheader()
        w.writerow({k: str(row.get(k, "")) for k in HEADER})
        f.flush()
        os.fsync(f.fileno())


def _atomic_replace(path: str, text: str) -> None:
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def current_projection(rows):
    proj = {}
    for r in rows:
        cid = r["cand_id"]
        if cid not in proj or int(r["version"]) > int(proj[cid]["version"]):
            proj[cid] = r
    return proj


def _now():
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


# ---------------------------------------------------------------- cmd ----

def cmd_add(args):
    cards = json.load(open(args.cards, encoding="utf-8"))
    if not _check_schema(args.ledger):
        print("LEDGER_SCHEMA_MISMATCH: 台账头与本工具 schema 不一致，拒绝写入（防跨版本混写）", file=sys.stderr)
        return 2
    rows, bad = _read_ledger(args.ledger)
    if bad:
        print("LEDGER_TAINTED: 台账存在坏行，先 doctor --repair-out 重建并人工采纳，再入账", file=sys.stderr)
        return 2
    proj = current_projection(rows)
    old_proj = {}
    if args.old and os.path.exists(args.old):
        old_rows, _ = _read_ledger(args.old)
        for r in old_rows:
            key = tuple(_norm(r.get(f, "")) for f in ("difficulty", "cause_hypothesis", "decision_shift"))
            old_proj.setdefault(key, r["cand_id"] if "cand_id" in r else r.get("card_id", "?"))
    added, skipped = [], []
    for card in cards:
        ev = (card.get("new_evidence") or "").strip()
        if ev and (not (card.get("new_evidence_source") or "").strip()
                   or not (card.get("evidence_judgment") or "").strip()):
            print("REJECTED: %s | new_evidence 非空必须同时给 new_evidence_source 与 evidence_judgment（fail-loud）"
                  % card.get("title", "?")[:40], file=sys.stderr)
            return 2
        ch = content_hash(card)
        cid = "c" + ch[1:11]  # 身份=首见内容（R3 修复2：相似≠同一身份；重试同内容→同 id→幂等）
        dup = next((r for r in rows + added if r["cand_id"] == cid and r["content_hash"] == ch and r["op"] == "add"), None)
        if dup:
            skipped.append({"cand_id": cid, "title": card.get("title", ""), "reason": "content_hash 与既有行相同（重试幂等跳过）"})
            continue
        key = merge_key(card)
        old_hit = old_proj.get(key)
        # 相似线索：同合并键的其他候选（仅报告；合并必须主控显式裁决）
        sim = sorted({r["cand_id"] for r in list(proj.values()) + added
                      if r["cand_id"] != cid and merge_key(r) == key})
        if old_hit and old_hit not in sim:
            sim.append(old_hit)
        row = {
            "row_no": len(rows) + len(added) + 1, "cand_id": cid, "version": 1,
            "op": "add", "status": "awaiting_evidence", "title": card.get("title", ""),
            **{f: card.get(f, "") for f in CARD_FIELDS[1:]},
            "new_evidence": ev, "new_evidence_source": card.get("new_evidence_source", ""),
            "evidence_judgment": card.get("evidence_judgment", ""),
            "old_topic_match": ("old:" + old_hit) if old_hit else "",
            "similar_to": " ".join(sim),
            "merged_into": "",
            "supersedes_row": "",
            "content_hash": ch, "source": card.get("source", ""), "writer": args.writer,
            "written_at": _now(), "note": "",
        }
        _append(args.ledger, row)
        added.append(row)
        proj[cid] = row
        if old_hit:
            print("OLD_TOPIC_MATCH: %s <-> 旧卡 %s（仅报告，处置权在主控；同键无新证据不自动淘汰）"
                  % (cid, old_hit))
        if sim:
            print("SIMILAR_CANDIDATES: %s <-> %s（同合并键线索；相似≠同一题，合并须主控显式裁决）"
                  % (cid, ",".join(sim)))
        print("ADDED %s v1 %s" % (cid, str(card.get("title", ""))[:40]))
    for s in skipped:
        print("SKIPPED %s %s | %s" % (s["cand_id"], str(s["title"])[:40], s["reason"]))
    print("SUMMARY added=%d skipped=%d" % (len(added), len(skipped)))
    return 0


def _guard_recommendation(cand_id: str, status: str, ledger_path: str,
                         pending_row: dict | None = None) -> bool:
    """推荐资格校验：状态转换的**共同入口**（status / revise 等一律经过）。

    Codex 要求 #4（2026-09-11 修复）：
      - 校验对象是**最终将写入的候选版本**，而不是仅"当前已存在版本"；
        因此调用方把待写入行（pending_row）传进来，本函数用它的 content_hash 去比对判定记录。
      - 覆盖**所有**状态修改入口（status / revise，含 --set 里的 status）。
    """
    if status != "recommended_pending_review":
        return True
    target_hash = (pending_row or {}).get("content_hash") or ""
    try:
        import importlib.util as _ilu
        _p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gate_verdict.py")
        _spec = _ilu.spec_from_file_location("gate_verdict_guard", _p)
        _gv = _ilu.module_from_spec(_spec)
        sys.modules["gate_verdict_guard"] = _gv
        _spec.loader.exec_module(_gv)
        ok, why = _gv.check(cand_id, Path(ledger_path), expect_hash=target_hash or None)
    except Exception as e:
        print("REJECTED: 无法校验闸门判定（%s）—— 拒绝在无法校验时置为推荐" % e, file=sys.stderr)
        return False
    if not ok:
        print("REJECTED: %s" % why, file=sys.stderr)
        print("  说明：任何进入推荐的路径都必须绑定「候选 ID + **待写入版本** + 通过判定」；"
              "草稿/淘汰/工作记录不受影响。", file=sys.stderr)
        return False
    return True


def cmd_revise(args):
    updates = json.loads(args.set)
    if not _check_schema(args.ledger):
        print("LEDGER_SCHEMA_MISMATCH", file=sys.stderr)
        return 2
    rows, bad = _read_ledger(args.ledger)
    if bad:
        print("LEDGER_TAINTED: 先 doctor --repair-out 重建并人工采纳", file=sys.stderr)
        return 2
    proj = current_projection(rows)
    cur = proj.get(args.cand_id)
    if not cur:
        print("NOT_FOUND: cand_id %s" % args.cand_id, file=sys.stderr)
        return 2
    allowed = set(HEADER) - {"row_no", "cand_id", "version", "op", "supersedes_row", "content_hash", "written_at"}
    illegal = set(updates) - allowed
    if illegal:
        print("REJECTED: 不可修订字段 %s（身份/版本/哈希由工具管理）" % sorted(illegal), file=sys.stderr)
        return 2
    # 修复（Codex 验收反例）：status 也可经 --set 传入，此前该路径完全绕过推荐门禁。
    # 现统一提取并走同一守卫：--status 与 --set {"status": ...} 等价且都必须过闸。
    requested_status = args.status or updates.pop("status", None)
    if requested_status is not None and requested_status not in STATUSES:
        print("REJECTED: 未知状态 %s（词表 %s）" % (requested_status, STATUSES), file=sys.stderr)
        return 2
    lb_changed = [f for f in LOAD_BEARING
                  if _norm_lb(cur.get(f, "")) != _norm_lb(updates.get(f, cur.get(f, "")))]
    row = dict(cur)
    row.update(updates)
    if requested_status is not None:
        row["status"] = requested_status
    # Codex 要求 #4（2026-09-11）：
    #  a) 已推荐候选发生**承重修改** → 自动转 needs_revision（待重审），不保留推荐态；
    #  b) 同一调用内"既改内容又申请推荐" → 用**将写入的 hash** 校验（旧判定会被拒）。
    if lb_changed and cur.get("status") == "recommended_pending_review" \
            and requested_status in (None, "recommended_pending_review"):
        row["status"] = "needs_revision"
        print("AUTO_DEMOTED: 已推荐候选发生承重变更 → needs_revision（须重新审查并重新判定）")
    if requested_status == "recommended_pending_review":
        probe = dict(row)
        probe.update({"content_hash": content_hash(row)})
        if not _guard_recommendation(args.cand_id, requested_status, args.ledger, pending_row=probe):
            return 2
    row.update({
        "row_no": len(rows) + 1, "version": int(cur["version"]) + 1, "op": "revise",
        "supersedes_row": cur["row_no"], "content_hash": content_hash(row),
        "writer": args.writer, "written_at": _now(),
        "note": "revise: " + args.reason,
    })
    _append(args.ledger, row)
    print("REVISED %s v%s (supersede row %s) 承重变化=%s"
          % (args.cand_id, row["version"], cur["row_no"], lb_changed or "无"))
    if lb_changed:
        inv = invalidate(args.cand_id, cur["content_hash"], args.reviews)
        print("REVIEWS_INVALIDATED: %s（旧 content_hash=%s 承重字段变更）" % (inv or "无登记意见", cur["content_hash"]))
    return 0


def cmd_status(args):
    if args.status not in STATUSES:
        print("REJECTED: 未知状态 %s" % args.status, file=sys.stderr)
        return 2
    rows, bad = _read_ledger(args.ledger)
    if bad:
        print("LEDGER_TAINTED: 先 doctor --repair", file=sys.stderr)
        return 2
    proj = current_projection(rows)
    cur = proj.get(args.cand_id)
    if not cur:
        print("NOT_FOUND: cand_id %s" % args.cand_id, file=sys.stderr)
        return 2
    # 推荐资格校验走共同入口；校验对象是**将写入的版本**（这里 status_change 不改内容，
    # 故将写入 hash == 当前 hash；显式传入以保持与 revise 路径同一语义）。
    probe = dict(cur)
    probe["status"] = args.status
    if not _guard_recommendation(args.cand_id, args.status, args.ledger, pending_row=probe):
        return 2
    row = dict(cur)
    row.update({"row_no": len(rows) + 1, "version": int(cur["version"]) + 1, "op": "status_change",
                "status": args.status, "writer": args.writer, "written_at": _now(),
                "note": "status_change: " + args.reason})
    _append(args.ledger, row)
    print("STATUS %s -> %s (v%s)" % (args.cand_id, args.status, row["version"]))
    return 0


def cmd_merge(args):
    """显式合并（R3 修复2）：相似度/同键永不自动合并；只有本命令建立合并关系。"""
    if args.cand_id == args.into:
        print("REJECTED: 不能合并到自身", file=sys.stderr); return 2
    rows, bad = _read_ledger(args.ledger)
    if bad:
        print("LEDGER_TAINTED: 先 doctor --repair-out 重建并人工采纳", file=sys.stderr); return 2
    proj = current_projection(rows)
    src, dst = proj.get(args.cand_id), proj.get(args.into)
    if not src or not dst:
        print("NOT_FOUND: %s / %s" % (args.cand_id, args.into), file=sys.stderr); return 2
    if src["status"] == "merged":
        print("REJECTED: %s 已是 merged（merged_into=%s）" % (args.cand_id, src["merged_into"]), file=sys.stderr); return 2
    row = dict(src)
    row.update({"row_no": len(rows) + 1, "version": int(src["version"]) + 1, "op": "merge",
                "status": "merged", "merged_into": args.into, "writer": args.writer,
                "written_at": _now(), "note": "merge -> %s: %s" % (args.into, args.reason)})
    _append(args.ledger, row)
    print("MERGED %s -> %s (v%s, 理由已留痕)" % (args.cand_id, args.into, row["version"]))
    return 0


def cmd_migrate(args):
    """schema 迁移（R3）：旧头台账 → 当前 HEADER；先备份原件。"""
    rows, bad = _read_ledger(args.ledger)
    if not bad and _check_schema(args.ledger):
        print("ALREADY_CURRENT"); return 0
    import shutil, time as _t
    bak = args.ledger + ".bak-" + _t.strftime("%Y%m%d-%H%M%S")
    shutil.copy2(args.ledger, bak)
    out = []
    for r in rows:
        nr = {k: r.get(k, "") for k in HEADER}
        out.append(nr)
    _atomic_replace(args.ledger, _dump_csv(out, HEADER))
    print("MIGRATED rows=%d backup=%s" % (len(out), bak))
    return 0


def cmd_show(args):
    rows, bad = _read_ledger(args.ledger)
    for b in bad:
        print("BAD_LINE %s: %s" % (b["line"], b["reason"]), file=sys.stderr)
    shown = rows if args.all else [r for r in current_projection(rows).values()]
    for r in sorted(shown, key=lambda x: (x["cand_id"], int(x["version"]))):
        print("%s v%s [%s] op=%s %s | old_match=%s | hash=%s"
              % (r["cand_id"], r["version"], r["status"], r["op"], str(r["title"])[:44],
                 r["old_topic_match"] or "-", r["content_hash"]))
    print("SUMMARY rows=%d shown=%d bad=%d" % (len(rows), len(shown), len(bad)))
    return 0 if not bad else 1


def cmd_doctor(args):
    """完整性报告与**安全**恢复（R3 修复3）：
    - 默认只报告（记录级 csv 解析 + EOF 换行 + 重复键）。
    - 已停用按物理行截断的原地修复（会破坏含多行字段的合法记录）。
    - --backup：原件复制为 <path>.bak-<ts>（原件不动）。
    - --repair-out PATH：从可解析记录重建候选文件写到 PATH；结构级损坏则不产出。
      原件任何情况下不被修改；采纳由人执行（mv/替换）。
    """
    raw = open(args.ledger, encoding="utf-8").read() if os.path.exists(args.ledger) else ""
    rows, bad = _read_ledger(args.ledger)
    problems = list(bad)
    if raw and not raw.endswith("\n"):
        problems.append({"line": "EOF", "reason": "file does not end with newline (可能中断写)", "raw": []})
    seen = {}
    for r in rows:
        k = (r["cand_id"], r["version"])
        if k in seen:
            problems.append({"line": r["row_no"], "reason": "duplicate (cand_id,version) %s" % (k,), "raw": []})
        seen[k] = r["row_no"]
    if not problems:
        print("LEDGER_OK rows=%d" % len(rows))
        return 0
    for p in problems:
        print("PROBLEM line=%s: %s" % (p["line"], p["reason"]))
    if args.backup:
        import shutil, time as _t
        bak = args.ledger + ".bak-" + _t.strftime("%Y%m%d-%H%M%S")
        shutil.copy2(args.ledger, bak)
        print("BACKUP: %s（原件未动）" % bak)
    if args.repair_out:
        struct_bad = any("field_count" not in p["reason"] for p in bad)
        if struct_bad:
            print("REPAIR_ABORTED: 存在 csv 结构级损坏（引号不闭合等），记录级重建不安全；仅保留报告与备份", file=sys.stderr)
            return 1
        kept, kseen = [], set()
        for r in rows:
            k = (r["cand_id"], r["version"])
            if k in kseen:
                continue
            kseen.add(k)
            kept.append(r)
        _atomic_replace(args.repair_out, _dump_csv(kept, HEADER))
        print("REPAIR_OUT: %s（%d 条记录；原件未动；采纳由人执行）" % (args.repair_out, len(kept)))
        return 1  # 存在过问题：即使产出修复件也返回 1，提示人工采纳
    print("HINT: --backup 备份原件；--repair-out PATH 产出重建候选文件（原件不动）")
    return 1


def invalidate(cand_id: str, old_hash: str, reviews_path: str):
    """把审过旧 content_hash 的意见标 needs_review。返回失效的 review_id 列表。"""
    if not reviews_path or not os.path.exists(reviews_path):
        return []
    rrows, _ = _read_ledger(reviews_path)
    changed = []
    for r in rrows:
        if r["cand_id"] == cand_id and r["ledger_content_hash"] == old_hash and r["status"] == "active":
            r["status"] = "needs_review"
            r["updated_at"] = _now()
            r["note"] = (r.get("note") or "") + " | 承重字段变更，自动置待复核"
            changed.append(r["review_id"])
    if changed:
        _atomic_replace(reviews_path, _dump_csv(rrows, REVIEWS_HEADER))
    return changed


def _dump_csv(rows, header):
    import io
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=header)
    w.writeheader()
    for r in rows:
        w.writerow({k: str(r.get(k, "")) for k in header})
    return buf.getvalue()


def cmd_review_register(args):
    """审查登记（R4 补强）：双哈希绑定。
    - --content-hash = 台账 content_hash（canonical 字段哈希）；--verify-ledger 给出时校验其确存在于台账。
    - --candidate-file = 被审候选文件路径（工具实算 sha256）；或 --candidate-file-sha256 显式给出（64 位十六进制）。
      两者至少其一必填；意见文件仍须自录两值以便交叉核对。
    - 同 review_id 已存在且绑定完整 → 拒绝（意见不可覆盖）；存在但缺 candidate_file_sha256 → 允许仅补绑（bind-completion）。
    """
    rows = []
    if os.path.exists(args.reviews):
        rows, bad = _read_ledger(args.reviews)
        if bad:
            print("REVIEWS_TAINTED", file=sys.stderr)
            return 2
    dup = next((r for r in rows if r["review_id"] == args.review_id), None)
    completing = bool(dup and not dup.get("candidate_file_sha256"))
    if dup and not completing:
        print("REJECTED: review_id 已存在且绑定完整 %s（意见不可覆盖，登记新 id）" % args.review_id, file=sys.stderr)
        return 2
    # dryrun-2026-09-10 修复：空/畸形 ledger_content_hash 一律拒绝。
    # 缺陷复现：不传 --verify-ledger 时，--content-hash "" 会被静默接受，
    # 该意见此后永远不会被 invalidate 命中（invalidate 比对真实 hash），
    # 等于一条永不过期的陈旧意见——判断可信度漏洞。
    if not re.fullmatch(r"h?[0-9a-f]{8,}", (args.content_hash or "").strip()):
        print("REJECTED: ledger_content_hash 缺失或格式非法（须为台账 content_hash，如 h0cd8adaad737）",
              file=sys.stderr)
        return 2
    if args.verify_ledger:
        lrows, lbad = _read_ledger(args.verify_ledger)
        if lbad:
            print("LEDGER_TAINTED", file=sys.stderr)
            return 2
        if not any(r["content_hash"] == args.content_hash for r in lrows):
            print("REJECTED: ledger_content_hash %s 不存在于台账 %s（绑定校验失败，防人工传参错绑）"
                  % (args.content_hash, args.verify_ledger), file=sys.stderr)
            return 2
    if args.candidate_file:
        if not os.path.exists(args.candidate_file):
            print("REJECTED: candidate_file 不存在 %s" % args.candidate_file, file=sys.stderr)
            return 2
        csha = hashlib.sha256(open(args.candidate_file, "rb").read()).hexdigest()
    elif args.candidate_file_sha256:
        csha = args.candidate_file_sha256.strip().lower()
        if not re.fullmatch(r"[0-9a-f]{64}", csha):
            print("REJECTED: candidate_file_sha256 必须为 64 位十六进制", file=sys.stderr)
            return 2
    else:
        print("REJECTED: 绑定不完整——必须给 --candidate-file（工具实算）或 --candidate-file-sha256", file=sys.stderr)
        return 2
    if completing:
        dup["candidate_file"] = args.candidate_file or dup.get("candidate_file", "")
        dup["candidate_file_sha256"] = csha
        dup["updated_at"] = _now()
        dup["note"] = (dup.get("note") or "") + " | bind-completion"
        _atomic_replace(args.reviews, _dump_csv(rows, REVIEWS_HEADER))
        print("BOUND %s candidate_file_sha256=%s（补绑完成）" % (args.review_id, csha[:16]))
        return 0
    rows.append({"review_id": args.review_id, "cand_id": args.cand_id,
                 "ledger_content_hash": args.content_hash, "candidate_file": args.candidate_file or "",
                 "candidate_file_sha256": csha, "role": args.role, "file": args.file,
                 "status": "active", "updated_at": _now(), "note": args.note or ""})
    _atomic_replace(args.reviews, _dump_csv(rows, REVIEWS_HEADER))
    print("REGISTERED %s -> %s@%s (%s) file_sha256=%s" % (args.review_id, args.cand_id, args.content_hash, args.role, csha[:16]))
    return 0


def cmd_invalidate(args):
    inv = invalidate(args.cand_id, args.content_hash, args.reviews)
    print("INVALIDATED: %s" % (inv or "无匹配登记意见"))
    return 0


def main(argv):
    ap = argparse.ArgumentParser(prog="ledger.py")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("add"); p.add_argument("--cards", required=True); p.add_argument("--ledger", required=True)
    p.add_argument("--old"); p.add_argument("--writer", default="agent/20260910-topic-loop")
    p = sub.add_parser("revise"); p.add_argument("--cand-id", required=True); p.add_argument("--set", required=True)
    p.add_argument("--reason", required=True); p.add_argument("--ledger", required=True)
    p.add_argument("--reviews", default=""); p.add_argument("--status"); p.add_argument("--writer", default="agent/20260910-topic-loop")
    p = sub.add_parser("status"); p.add_argument("--cand-id", required=True); p.add_argument("--status", required=True)
    p.add_argument("--reason", required=True); p.add_argument("--ledger", required=True)
    p.add_argument("--writer", default="agent/20260910-topic-loop")
    p = sub.add_parser("show"); p.add_argument("--ledger", required=True); p.add_argument("--all", action="store_true")
    p = sub.add_parser("doctor"); p.add_argument("--ledger", required=True)
    p.add_argument("--backup", action="store_true"); p.add_argument("--repair-out")
    p = sub.add_parser("merge"); p.add_argument("--cand-id", required=True); p.add_argument("--into", required=True)
    p.add_argument("--reason", required=True); p.add_argument("--ledger", required=True)
    p.add_argument("--writer", default="agent/20260910-topic-loop")
    p = sub.add_parser("migrate"); p.add_argument("--ledger", required=True)
    p = sub.add_parser("review-register"); p.add_argument("--review-id", required=True); p.add_argument("--cand-id", required=True)
    p.add_argument("--content-hash", required=True); p.add_argument("--role", default="reviewer")
    p.add_argument("--file", required=True); p.add_argument("--reviews", required=True); p.add_argument("--note")
    p.add_argument("--candidate-file"); p.add_argument("--candidate-file-sha256"); p.add_argument("--verify-ledger")
    p = sub.add_parser("invalidate-reviews"); p.add_argument("--cand-id", required=True)
    p.add_argument("--content-hash", required=True); p.add_argument("--reviews", required=True)
    args = ap.parse_args(argv)
    return {"add": cmd_add, "revise": cmd_revise, "status": cmd_status, "show": cmd_show,
            "doctor": cmd_doctor, "merge": cmd_merge, "migrate": cmd_migrate,
            "review-register": cmd_review_register,
            "invalidate-reviews": cmd_invalidate}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))