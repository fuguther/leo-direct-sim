#!/usr/bin/env python3
"""闸门判定记录：把「候选 ID + 当前版本 + 判定」绑定成可校验的记录。

替代此前的"扫目录式"交付检查（Codex 收口 #3）：
  - 旧做法：看 gates/ 目录里有没有文件、有没有 BLOCK —— 无关 TODO 能放行、无关 BLOCK 能误拦；
  - 新做法：判定记录绑定候选的 **当前 content_hash**；台账把候选置为推荐时校验该绑定。

用法：
  gate_verdict.py record --cand-id <id> --verdict PASS|BLOCK|INPUT_INSUFFICIENT \
      --card <深化稿路径> --ledger round/CANDIDATE-LEDGER.csv [--note ...]
  gate_verdict.py check --cand-id <id> --ledger round/CANDIDATE-LEDGER.csv   # 供台账调用
  gate_verdict.py show [--cand-id <id>]
"""
import argparse, csv, hashlib, json, os, sys, time
from pathlib import Path

WT = Path(__file__).resolve().parents[2]
GATE_DIR = WT / "round" / "run2" / "gates"
VERDICTS = ("PASS", "REVISE", "BLOCK", "INPUT_INSUFFICIENT")


def current_hash(ledger: Path, cand_id: str):
    """返回 (content_hash, version)；找不到返回 (None, None)。"""
    if not ledger.exists():
        return None, None
    rows = []
    try:
        with ledger.open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
    except Exception:
        return None, None
    best = None
    for r in rows:
        if r.get("cand_id") == cand_id:
            if best is None or int(r.get("version") or 0) > int(best.get("version") or 0):
                best = r
    if best is None:
        return None, None
    return best.get("content_hash"), best.get("version")


def verdict_path(cand_id: str) -> Path:
    return GATE_DIR / ("%s.json" % cand_id)


def cmd_record(a) -> int:
    if a.verdict not in VERDICTS:
        print("REJECTED: 未知判定 %s（可用 %s）" % (a.verdict, ", ".join(VERDICTS)), file=sys.stderr)
        return 2
    ch, ver = current_hash(Path(a.ledger), a.cand_id)
    if ch is None:
        print("REJECTED: 台账中找不到候选 %s" % a.cand_id, file=sys.stderr)
        return 2
    card = Path(a.card)
    if not card.exists():
        print("REJECTED: 卡文件不存在 %s" % a.card, file=sys.stderr)
        return 2
    csha = hashlib.sha256(card.read_bytes()).hexdigest()
    GATE_DIR.mkdir(parents=True, exist_ok=True)
    rec = {
        "cand_id": a.cand_id,
        "ledger_content_hash": ch,
        "ledger_version": ver,
        "card": str(card.relative_to(WT)) if str(card).startswith(str(WT)) else str(card),
        "card_sha256": csha,
        "verdict": a.verdict,
        "note": a.note or "",
        "recorded_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    verdict_path(a.cand_id).write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    print("RECORDED %s %s @%s v%s (card=%s)" % (a.cand_id, a.verdict, ch, ver, csha[:12]))
    return 0


def check(cand_id: str, ledger_path: Path):
    """返回 (ok: bool, reason: str)。供台账与 hook 共用。"""
    ch, ver = current_hash(ledger_path, cand_id)
    if ch is None:
        return False, "候选 %s 不在台账中" % cand_id
    p = verdict_path(cand_id)
    if not p.exists():
        return False, "候选 %s 无闸门判定记录（先跑 gate_verdict.py record）" % cand_id
    try:
        rec = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        return False, "判定记录损坏：%s" % e
    if rec.get("ledger_content_hash") != ch:
        return False, ("判定记录绑定的是旧版本（记录 %s / 当前 %s）—— 卡内容已变更，须重新判定"
                       % (rec.get("ledger_content_hash"), ch))
    v = rec.get("verdict")
    if v != "PASS":
        return False, "候选 %s 当前版本判定为 %s（%s）" % (cand_id, v, rec.get("note") or "无备注")
    # #5b 修复（Codex 实查）：卡文件缺失时必须失败，不能跳过校验后返回 PASS。
    card = WT / rec["card"] if not os.path.isabs(rec.get("card", "")) else Path(rec["card"])
    if not card.exists():
        return False, ("被审卡文件不存在（%s）—— 判定记录失去可校验对象，视为未通过；"
                       "请补齐卡文件或重新判定" % rec.get("card"))
    now = hashlib.sha256(card.read_bytes()).hexdigest()
    if now != rec.get("card_sha256"):
        return False, "卡文件在判定后已被修改（sha256 不匹配）—— 须重新判定"
    return True, "PASS @%s v%s" % (ch, ver)


def cmd_check(a) -> int:
    ok, why = check(a.cand_id, Path(a.ledger))
    print(("GATE_OK: " if ok else "GATE_FAIL: ") + why)
    return 0 if ok else 2


def cmd_show(a) -> int:
    if not GATE_DIR.is_dir():
        print("(无判定记录)"); return 0
    files = sorted(GATE_DIR.glob("*.json"))
    if a.cand_id:
        files = [f for f in files if f.stem == a.cand_id]
    for f in files:
        try:
            rec = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            print("  %-14s <损坏>" % f.stem); continue
        print("  %-14s %-18s @%s v%s  %s" % (f.stem, rec.get("verdict"),
              rec.get("ledger_content_hash"), rec.get("ledger_version"), rec.get("note", "")[:40]))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("record"); r.add_argument("--cand-id", required=True); r.add_argument("--verdict", required=True)
    r.add_argument("--card", required=True); r.add_argument("--ledger", required=True); r.add_argument("--note", default="")
    c = sub.add_parser("check"); c.add_argument("--cand-id", required=True); c.add_argument("--ledger", required=True)
    s = sub.add_parser("show"); s.add_argument("--cand-id", default="")
    a = ap.parse_args()
    return {"record": cmd_record, "check": cmd_check, "show": cmd_show}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())