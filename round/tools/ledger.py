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
  needs_review（归一化后仅标点/空白差异不触发）。
- 旧题匹配只报告（old_topic_match + stdout OLD_TOPIC_MATCH），不自动淘汰；处置权在主控
  （revise/status/merge）。判定语义归一化复制自 pool.py@sha256:15989feaeedc497d。
- new_evidence 非空必须同时给 --evidence-source 与 --evidence-judgment（主控判定），否则拒绝。
- 状态词表: backlog(待建设) awaiting_evidence(待证据) needs_revision(需修订)
  recommended_pending_review(推荐待审) archived(归档) merged(合并簿记)。
- 中断恢复: 追加即时 flush+fsync；doctor 校验行完整性，残尾行 --repair 用临时文件+原子替换截除。

用法:
  python3 ledger.py add --cards cards.json --ledger L.csv [--old OLD.csv] [--writer WHO]
  python3 ledger.py revise --cand-id ID --set '{"difficulty":"新值"}' --reason "为何" --ledger L.csv [--status S]
  python3 ledger.py status --cand-id ID --status awaiting_evidence --reason "为何" --ledger L.csv
  python3 ledger.py show --ledger L.csv [--all]
  python3 ledger.py doctor --ledger L.csv [--repair]
  python3 ledger.py review-register --review-id R1 --cand-id ID --content-hash H --role builder --file F --reviews RV.csv
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
import time

CARD_FIELDS = ("title", "conditions", "difficulty", "cause_hypothesis", "possible_change",
               "strongest_alternative", "decision_shift", "next_cheap_check")
EVIDENCE_FIELDS = ("new_evidence", "new_evidence_source", "evidence_judgment")
LOAD_BEARING = ("conditions", "difficulty", "cause_hypothesis", "possible_change",
                "strongest_alternative", "decision_shift", "new_evidence")
STATUSES = ("backlog", "awaiting_evidence", "needs_revision",
            "recommended_pending_review", "archived", "merged")

HEADER = ["row_no", "cand_id", "version", "op", "status", "title"] + list(CARD_FIELDS[1:]) + [
    "new_evidence", "new_evidence_source", "evidence_judgment", "old_topic_match",
    "supersedes_row", "content_hash", "source", "writer", "written_at", "note"]

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
    """承重比较归一化：去全部空白与标点后小写（标点级修改不触发审查失效）。"""
    return re.sub(r"[\s\W_]+", "", (text or "").lower(), flags=re.UNICODE)


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
        print("LEDGER_TAINTED: 台账存在坏行，先 doctor --repair 再入账", file=sys.stderr)
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
        cid = cand_id_for(card)
        dup = next((r for r in rows + added if r["cand_id"] == cid and r["content_hash"] == ch and r["op"] == "add"), None)
        if dup:
            skipped.append({"cand_id": cid, "title": card.get("title", ""), "reason": "content_hash 与既有行相同（幂等跳过）"})
            continue
        key = merge_key(card)
        old_hit = old_proj.get(key)
        sibling = proj.get(cid)
        version = (int(sibling["version"]) + 1) if sibling else 1
        note = ""
        if sibling:
            note = "同键同候选的新版本卡（同批/重入），需主控决定合并或保留"
        row = {
            "row_no": len(rows) + len(added) + 1, "cand_id": cid, "version": version,
            "op": "add", "status": "awaiting_evidence", "title": card.get("title", ""),
            **{f: card.get(f, "") for f in CARD_FIELDS[1:]},
            "new_evidence": ev, "new_evidence_source": card.get("new_evidence_source", ""),
            "evidence_judgment": card.get("evidence_judgment", ""),
            "old_topic_match": ("old:" + old_hit) if old_hit else "",
            "supersedes_row": sibling["row_no"] if sibling else "",
            "content_hash": ch, "source": card.get("source", ""), "writer": args.writer,
            "written_at": _now(), "note": note,
        }
        _append(args.ledger, row)
        added.append(row)
        proj[cid] = row
        if old_hit:
            print("OLD_TOPIC_MATCH: %s <-> 旧卡 %s（仅报告，处置权在主控；同键无新证据不自动淘汰）"
                  % (cid, old_hit))
        print("ADDED %s v%s %s" % (cid, version, str(card.get("title", ""))[:40]))
    for s in skipped:
        print("SKIPPED %s %s | %s" % (s["cand_id"], str(s["title"])[:40], s["reason"]))
    print("SUMMARY added=%d skipped=%d" % (len(added), len(skipped)))
    return 0


def cmd_revise(args):
    updates = json.loads(args.set)
    if not _check_schema(args.ledger):
        print("LEDGER_SCHEMA_MISMATCH", file=sys.stderr)
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
    allowed = set(HEADER) - {"row_no", "cand_id", "version", "op", "supersedes_row", "content_hash", "written_at"}
    illegal = set(updates) - allowed
    if illegal:
        print("REJECTED: 不可修订字段 %s（身份/版本/哈希由工具管理）" % sorted(illegal), file=sys.stderr)
        return 2
    lb_changed = [f for f in LOAD_BEARING
                  if _norm_lb(cur.get(f, "")) != _norm_lb(updates.get(f, cur.get(f, "")))]
    row = dict(cur)
    row.update(updates)
    if args.status:
        if args.status not in STATUSES:
            print("REJECTED: 未知状态 %s（词表 %s）" % (args.status, STATUSES), file=sys.stderr)
            return 2
        row["status"] = args.status
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
    row = dict(cur)
    row.update({"row_no": len(rows) + 1, "version": int(cur["version"]) + 1, "op": "status_change",
                "status": args.status, "writer": args.writer, "written_at": _now(),
                "note": "status_change: " + args.reason})
    _append(args.ledger, row)
    print("STATUS %s -> %s (v%s)" % (args.cand_id, args.status, row["version"]))
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
    if args.repair:
        good_lines = raw.splitlines(keepends=True)
        bad_lines = {p["line"] for p in problems if isinstance(p["line"], int)}
        kept = [ln for i, ln in enumerate(good_lines, start=1) if i not in bad_lines]
        text = "".join(kept)
        if text and not text.endswith("\n"):
            text += "\n"
        _atomic_replace(args.ledger, text)
        rows2, bad2 = _read_ledger(args.ledger)
        fixed = not bad2
        print("REPAIRED: 移除 %d 个坏行（截尾/坏行），原子替换完成；复验 %s"
              % (len(bad_lines), "通过" if fixed else "仍有问题"))
        return 0 if fixed else 1
    print("HINT: 加 --repair 截除坏行（不做其他改写）")
    return 1


def invalidate(cand_id: str, old_hash: str, reviews_path: str):
    """把审过旧 content_hash 的意见标 needs_review。返回失效的 review_id 列表。"""
    if not reviews_path or not os.path.exists(reviews_path):
        return []
    rrows, _ = _read_ledger(reviews_path)
    changed = []
    for r in rrows:
        if r["cand_id"] == cand_id and r["content_hash"] == old_hash and r["status"] == "active":
            r["status"] = "needs_review"
            r["updated_at"] = _now()
            r["note"] = (r.get("note") or "") + " | 承重字段变更，自动置待复核"
            changed.append(r["review_id"])
    if changed:
        _atomic_replace(reviews_path, _dump_csv(rrows, ["review_id", "cand_id", "content_hash", "role", "file", "status", "updated_at", "note"]))
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
    rows = []
    if os.path.exists(args.reviews):
        rows, bad = _read_ledger(args.reviews)
        if bad:
            print("REVIEWS_TAINTED", file=sys.stderr)
            return 2
    dup = next((r for r in rows if r["review_id"] == args.review_id), None)
    if dup:
        print("REJECTED: review_id 已存在 %s（意见不可覆盖，登记新 id）" % args.review_id, file=sys.stderr)
        return 2
    rows.append({"review_id": args.review_id, "cand_id": args.cand_id, "content_hash": args.content_hash,
                 "role": args.role, "file": args.file, "status": "active",
                 "updated_at": _now(), "note": args.note or ""})
    _atomic_replace(args.reviews, _dump_csv(rows, ["review_id", "cand_id", "content_hash", "role", "file", "status", "updated_at", "note"]))
    print("REGISTERED %s -> %s@%s (%s)" % (args.review_id, args.cand_id, args.content_hash, args.role))
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
    p = sub.add_parser("doctor"); p.add_argument("--ledger", required=True); p.add_argument("--repair", action="store_true")
    p = sub.add_parser("review-register"); p.add_argument("--review-id", required=True); p.add_argument("--cand-id", required=True)
    p.add_argument("--content-hash", required=True); p.add_argument("--role", default="reviewer")
    p.add_argument("--file", required=True); p.add_argument("--reviews", required=True); p.add_argument("--note")
    p = sub.add_parser("invalidate-reviews"); p.add_argument("--cand-id", required=True)
    p.add_argument("--content-hash", required=True); p.add_argument("--reviews", required=True)
    args = ap.parse_args(argv)
    return {"add": cmd_add, "revise": cmd_revise, "status": cmd_status, "show": cmd_show,
            "doctor": cmd_doctor, "review-register": cmd_review_register,
            "invalidate-reviews": cmd_invalidate}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))