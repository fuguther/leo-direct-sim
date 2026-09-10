#!/usr/bin/env python3
"""闸门轮次计数器（#9 断点补法）：每张卡过闸次数硬计数，到 3 自动标记超限。

设计：不改 ledger（加字段会污染 content_hash、失效全部审查绑定）——独立 JSON 计数。
用法:
  python3 gate_rounds.py bump <cand_id> [--note ...]   # 过闸一次，+1
  python3 gate_rounds.py show [cand_id]                # 查看
  python3 gate_rounds.py reset <cand_id> --reason ...  # 仅在卡内容实质重写后允许，须留理由
"""
import argparse, json, sys
from datetime import datetime
from pathlib import Path

F = Path(__file__).resolve().parents[1] / "run2" / "gate-rounds.json"
MAX_ROUNDS = 3

def load():
    return json.loads(F.read_text(encoding="utf-8")) if F.exists() else {}

def save(d):
    F.parent.mkdir(parents=True, exist_ok=True)
    F.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("bump"); b.add_argument("cand_id"); b.add_argument("--note", default="")
    s = sub.add_parser("show"); s.add_argument("cand_id", nargs="?")
    r = sub.add_parser("reset"); r.add_argument("cand_id"); r.add_argument("--reason", required=True)
    a = ap.parse_args()
    d = load()
    if a.cmd == "bump":
        e = d.setdefault(a.cand_id, {"rounds": 0, "history": [], "status": "active"})
        if e.get("status") == "exceeded":
            print("REFUSED: %s 已超限（%d 轮），须淘汰或先 reset 并说明实质重写理由" % (a.cand_id, e["rounds"]))
            return 2
        e["rounds"] += 1
        e["history"].append({"round": e["rounds"], "at": datetime.now().isoformat(timespec="seconds"), "note": a.note})
        if e["rounds"] >= MAX_ROUNDS:
            e["status"] = "exceeded"
            print("⚠ %s 达到 %d 轮上限 → 状态 exceeded（应淘汰或转方向内其他问题，不得继续修补）" % (a.cand_id, MAX_ROUNDS))
        save(d)
        print("bump %s -> %d/%d" % (a.cand_id, e["rounds"], MAX_ROUNDS))
        return 0
    if a.cmd == "reset":
        d[a.cand_id] = {"rounds": 0, "history": [{"round": 0, "at": datetime.now().isoformat(timespec="seconds"), "note": "RESET: " + a.reason}], "status": "active"}
        save(d); print("reset %s（理由已留痕）" % a.cand_id); return 0
    # show
    if a.cand_id:
        print(json.dumps(d.get(a.cand_id, {"rounds": 0, "status": "unseen"}), ensure_ascii=False, indent=1))
    else:
        print(json.dumps(d, ensure_ascii=False, indent=1))
    return 0

if __name__ == "__main__":
    sys.exit(main())