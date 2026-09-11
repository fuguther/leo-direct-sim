#!/usr/bin/env python3
"""独立反例验证（Codex 验收要求，2026-09-11）。

覆盖：
  A. 推荐门禁：--set 传 status / --status / 同调用改内容+申请推荐 / 已推荐候选承重修改
  B. 角色绑定：同主控生成器不能领取历史审查者权限
  C. 隔离：全程在临时台账与隔离状态目录内运行，真实文件哈希前后一致
"""
import csv, hashlib, json, os, subprocess, sys, tempfile
from pathlib import Path

WT = Path(__file__).resolve().parents[2]
H = WT / "round" / "hooks"
REAL = [WT / "round" / "CANDIDATE-LEDGER.csv", H / "permissions.json", H / "orchestrator.id"]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else "(absent)"


def main() -> int:
    before = {str(p): sha(p) for p in REAL}
    res = []
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        ledger = tdp / "iso-ledger.csv"
        gates = tdp / "gates"
        gates.mkdir()
        card = tdp / "card.md"
        card.write_text("# 验收反例卡\n", encoding="utf-8")
        card2 = tdp / "card2.md"
        card2.write_text("# 验收反例卡 v2\n", encoding="utf-8")
        # 造一张卡
        cardsjson = tdp / "cards.json"
        cardsjson.write_text(json.dumps([{"title": "验收反例卡", "conditions": "t", "difficulty": "t",
            "cause_hypothesis": "t", "possible_change": "t", "strongest_alternative": "t",
            "decision_shift": "t", "next_cheap_check": "t", "source": "acc"}], ensure_ascii=False), encoding="utf-8")
        subprocess.run([sys.executable, "round/tools/ledger.py", "add", "--cards", str(cardsjson),
                        "--ledger", str(ledger)], capture_output=True, cwd=WT)
        rows = list(csv.DictReader(open(ledger, encoding="utf-8")))
        cid = rows[-1]["cand_id"]

        genv = dict(os.environ)
        genv["DSH_GATE_DIR"] = str(gates)   # 判定记录也走隔离目录

        def run(*argv):
            return subprocess.run([sys.executable, *argv], capture_output=True, text=True, cwd=WT, env=genv)

        print("=== A. 推荐门禁（无判定记录时，所有入口都必须被拒）===")
        cases = [
            ("--status 路径", ["round/tools/ledger.py", "status", "--cand-id", cid, "--status",
                              "recommended_pending_review", "--reason", "t", "--ledger", str(ledger)]),
            ("revise --status", ["round/tools/ledger.py", "revise", "--cand-id", cid, "--set", '{"next_cheap_check":"x"}',
                                 "--reason", "t", "--status", "recommended_pending_review", "--ledger", str(ledger)]),
            ("revise --set 塞 status（Codex 反例）", ["round/tools/ledger.py", "revise", "--cand-id", cid,
                                 "--set", '{"status":"recommended_pending_review"}', "--reason", "t", "--ledger", str(ledger)]),
            ("同调用改内容+申请推荐", ["round/tools/ledger.py", "revise", "--cand-id", cid,
                                 "--set", '{"difficulty":"新条件","status":"recommended_pending_review"}',
                                 "--reason", "t", "--ledger", str(ledger)]),
        ]
        for name, argv in cases:
            r = run(*argv)
            res.append((f"A {name}", r.returncode == 2))
            print("  %s %-34s exit=%d" % ("PASS" if r.returncode == 2 else "FAIL", name, r.returncode))
        st = [x for x in csv.DictReader(open(ledger, encoding="utf-8")) if x["cand_id"] == cid][-1]["status"]
        ok = st != "recommended_pending_review"
        res.append(("A 卡未被置为推荐", ok))
        print("  %s 最终状态=%s" % ("PASS" if ok else "FAIL", st))

        print()
        print("=== B. 推荐链路：判定 → 置推荐 → 承重修改自动降级 ===")
        genv = dict(os.environ)
        genv["DSH_GATE_DIR"] = str(gates)
        # B1: 无判定时置推荐必须被拒
        r = run("round/tools/ledger.py", "status", "--cand-id", cid, "--status", "recommended_pending_review",
                "--reason", "t", "--ledger", str(ledger))
        res.append(("B1 无判定置推荐被拒", r.returncode == 2))
        print("  %s 无判定置推荐 exit=%d" % ("PASS" if r.returncode == 2 else "FAIL", r.returncode))
        # B2: 记录 PASS 判定（隔离 gates 目录）
        r = subprocess.run([sys.executable, "round/tools/gate_verdict.py", "record", "--cand-id", cid,
                            "--verdict", "PASS", "--card", str(card), "--ledger", str(ledger),
                            "--note", "验收"], capture_output=True, text=True, cwd=WT, env=genv)
        res.append(("B2 记录判定成功", r.returncode == 0))
        print("  %s record PASS exit=%d" % ("PASS" if r.returncode == 0 else "FAIL", r.returncode))
        # B3: 置推荐应通过
        r = run("round/tools/ledger.py", "status", "--cand-id", cid, "--status", "recommended_pending_review",
                "--reason", "t", "--ledger", str(ledger))
        st = [x for x in csv.DictReader(open(ledger, encoding="utf-8")) if x["cand_id"] == cid][-1]["status"]
        ok = (r.returncode == 0 and st == "recommended_pending_review")
        res.append(("B3 有判定可置推荐", ok))
        print("  %s 置推荐 exit=%d status=%s" % ("PASS" if ok else "FAIL", r.returncode, st))
        # B4: 承重修改 → 自动转 needs_revision
        r = run("round/tools/ledger.py", "revise", "--cand-id", cid,
                "--set", '{"difficulty":"承重修改后的新条件"}', "--reason", "t", "--ledger", str(ledger))
        st2 = [x for x in csv.DictReader(open(ledger, encoding="utf-8")) if x["cand_id"] == cid][-1]["status"]
        auto = "AUTO_DEMOTED" in (r.stdout + r.stderr)
        ok = (r.returncode == 0 and st2 == "needs_revision" and auto)
        res.append(("B4 承重修改自动降级", ok))
        print("  %s 承重修改 status=%s AUTO_DEMOTED=%s" % ("PASS" if ok else "FAIL", st2, auto))
        # B5: 降级后再申请推荐（旧判定已失效）必须被拒
        r = run("round/tools/ledger.py", "status", "--cand-id", cid, "--status", "recommended_pending_review",
                "--reason", "t", "--ledger", str(ledger))
        res.append(("B5 旧判定不能复活推荐", r.returncode == 2))
        print("  %s 旧判定再置推荐 exit=%d" % ("PASS" if r.returncode == 2 else "FAIL", r.returncode))

        print()
        print("=== C. 角色绑定：同主控生成器不能领取历史审查者权限 ===")
        iso_perm = tdp / "iso-perm.json"
        iso_orch = tdp / "iso-orch.id"
        iso_log = tdp / "iso.log"
        ORCH = "session-orch-acc"
        iso_orch.write_text(ORCH, encoding="utf-8")
        iso_perm.write_text(json.dumps({"run_id": "acc", "orchestrator_session": ORCH,
            "orchestrator_history": [ORCH],
            "sessions": {"gen-X": {"role": "generator", "extra_read": [], "extra_write": ["round/run2/staging/p.md"]}},
            "tickets": [{"role": "history_reviewer", "extra_read": [], "extra_write": [], "session": ""}]},
            ensure_ascii=False), encoding="utf-8")
        env = dict(os.environ)
        env.update({"DSH_PERM_FILE": str(iso_perm), "DSH_ORCH_FILE": str(iso_orch), "DSH_HOOK_LOG": str(iso_log)})
        payload = {"hook_event_name": "PreToolUse", "session_id": "gen-X", "tool_name": "read",
                   "tool_input": {"file_path": str(WT / "round/history/HISTORY-INDEX.md")}, "cwd": "/Users/lge/Desktop/leo-direct-sim"}
        rc = subprocess.run([sys.executable, str(H / "hook_access_guard.py")], input=json.dumps(payload),
                            capture_output=True, text=True, env=env).returncode
        res.append(("C 生成器读历史被拦", rc == 2))
        print("  %s 生成器读历史索引 exit=%d (期望2)" % ("PASS" if rc == 2 else "FAIL", rc))
        left = json.loads(iso_perm.read_text(encoding="utf-8")).get("tickets") or []
        ok2 = len(left) == 1
        res.append(("C 票据未被消费", ok2))
        print("  %s 票据剩余=%d (期望1，未被消费)" % ("PASS" if ok2 else "FAIL", len(left)))

    after = {str(p): sha(p) for p in REAL}
    print()
    print("=== 隔离校验（真实文件必须不变）===")
    iso_ok = True
    for k in before:
        same = before[k] == after[k]
        iso_ok = iso_ok and same
        print("  %s %s" % ("PASS" if same else "FAIL", Path(k).name))
    passed = sum(1 for _, ok in res if ok)
    print()
    print("SUMMARY %d/%d 通过 | 隔离:%s" % (passed, len(res), "OK" if iso_ok else "VIOLATED"))
    return 0 if (passed == len(res) and iso_ok) else 1


if __name__ == "__main__":
    sys.exit(main())