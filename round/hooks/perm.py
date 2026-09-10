#!/usr/bin/env python3
"""权限清单（run-scoped）：把"角色 → 读写范围"绑定到运行时 session_id。

设计依据（HOOK-CONTRACT.md 实测）：
  - PreToolUse 载荷只有 session_id 是可靠身份，角色无法推断 → 必须由派发端登记；
  - 因此本工具是"派发端断言角色"的唯一入口，hook 只读清单、不做身份猜测；
  - 不使用任何环境变量判定子代理身份（父会话的标记不得让子代理整体豁免）。

用法：
  perm.py init --run <runId>              # 初始化（自动读取 DSH_SESSION_ID 作为主控）
  perm.py bind --session <sid> --role <role> [--note ...] [--extra-read P] [--extra-write P]
  perm.py unbind --session <sid>
  perm.py show
  perm.py resolve --session <sid>         # 返回角色（供 hook 调用）
  perm.py grants --role <role>            # 打印角色授权（供文档/提示词）
  perm.py audit                           # 审计未登记会话的访问记录
"""
import argparse, json, os, sys, time
from pathlib import Path

HOOK_DIR = Path(__file__).resolve().parent
PERM_FILE = HOOK_DIR / "permissions.json"
LOG_FILE = HOOK_DIR / "unregistered.log"

# ── 中性资料（所有研究角色可读；不含任何历史候选/淘汰材料）────────────────
NEUTRAL_READ = [
    "round/zotero/ZOTERO-INDEX.md",
    "round/zotero/ZOTERO-MD-INDEX.md",
    "round/zotero/KEY-PAPERS-CITEKEYS.md",
    "round/zotero/CITEKEY-CROSSWALK.md",
    "round/zotero/CITEKEY-CROSSWALK.json",
    "round/knowledge/notes-neutral/**",
    "round/knowledge/NEUTRAL-KNOWLEDGE-VIEW.md",
    "round/knowledge/CORPUS-COVERAGE.md",
    "LITERATURE/SOURCES.csv",
    "LITERATURE/papers/**",
]

ROLE_GRANTS = {
    # 主控：全权（编排、台账、交付、hook 管理）
    "orchestrator": {"read": ["**"], "write": ["**"], "shell": "full"},
    # 生成器：只读中性资料，只写自己的候选草稿
    "generator": {
        "read": NEUTRAL_READ,
        "write": [],   # 需派发端 --extra-write 指定具体文件（防同角色互相覆盖）
        "shell": "best_effort",
    },
    # 深化者：中性资料 + 指定候选 + 本卡反馈；只写自己的深化稿
    "deepener": {
        "read": NEUTRAL_READ + ["round/run2/cards/**", "round/run2/feedback/**"],
        "write": [],   # 同上：深化稿路径由派发端指定
        "shell": "best_effort",
    },
    # 历史审查者：可读历史库与旧卡（这是它的职责），只写自己的报告
    "history_reviewer": {
        "read": NEUTRAL_READ + [
            "round/history/**",
            "round/run1/**",
            "round/CANDIDATE-LEDGER.csv",
            "round/reviews/**",
            "round/run2/cards/**",
            "round/run2/staging/**",
        ],
        "write": ["round/run2/op-history-review*.md"],
        "shell": "best_effort",
    },
    # 三角色审查者：读被审卡与中性资料，只写自己的意见
    "reviewer": {
        "read": NEUTRAL_READ + ["round/run2/cards/**", "round/run2/staging/**", "round/run2/drafts/**"],
        "write": [],   # 同上：意见文件路径由派发端指定
        "shell": "best_effort",
    },
    # 审计者（污染审计/文档审计等）：只读全域，只写审计报告
    "auditor": {"read": ["**"], "write": ["round/run2/audit/**"], "shell": "best_effort"},
}


def load() -> dict:
    if PERM_FILE.exists():
        try:
            return json.loads(PERM_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save(d: dict) -> None:
    d["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    PERM_FILE.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    try:
        os.chmod(PERM_FILE, 0o600)
    except Exception:
        pass


def cmd_init(a) -> int:
    orch = a.orchestrator or os.environ.get("DSH_SESSION_ID") or ""
    if not orch:
        print("REFUSED: 无法确定主控 session_id（未提供 --orchestrator 且无 DSH_SESSION_ID）", file=sys.stderr)
        return 2
    d = load()
    d.update({
        "run_id": a.run,
        "orchestrator_session": orch,
        "created_at": d.get("created_at") or time.strftime("%Y-%m-%dT%H:%M:%S"),
        "sessions": d.get("sessions", {}),
    })
    save(d)
    print("INIT run=%s orchestrator=%s" % (a.run, orch))
    return 0


def cmd_bind(a) -> int:
    if a.role not in ROLE_GRANTS:
        print("REFUSED: 未知角色 %s（可用：%s）" % (a.role, ", ".join(ROLE_GRANTS)), file=sys.stderr)
        return 2
    d = load()
    if not d:
        print("REFUSED: 未初始化，先跑 perm.py init", file=sys.stderr)
        return 2
    if a.session == d.get("orchestrator_session"):
        print("REFUSED: 不能把主控会话绑定为研究角色（主控是全权）", file=sys.stderr)
        return 2
    d.setdefault("sessions", {})[a.session] = {
        "role": a.role,
        "note": a.note or "",
        "extra_read": a.extra_read or [],
        "extra_write": a.extra_write or [],
        "bound_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    save(d)
    print("BOUND %s -> %s%s%s" % (a.session, a.role,
          (" +read:" + ",".join(a.extra_read)) if a.extra_read else "",
          (" +write:" + ",".join(a.extra_write)) if a.extra_write else ""))
    return 0


def cmd_unbind(a) -> int:
    d = load()
    s = d.get("sessions", {})
    if a.session in s:
        del s[a.session]
        save(d)
        print("UNBOUND", a.session)
    else:
        print("NOT-BOUND", a.session)
    return 0


def cmd_show(a) -> int:
    d = load()
    if not d:
        print("(未初始化)")
        return 0
    print("run_id: %s" % d.get("run_id"))
    print("orchestrator: %s" % d.get("orchestrator_session"))
    sess = d.get("sessions", {})
    print("bound sessions: %d" % len(sess))
    for sid, info in sess.items():
        print("  %-40s %-16s extra_read=%s extra_write=%s" % (
            sid, info.get("role"), info.get("extra_read") or "-", info.get("extra_write") or "-"))
    if LOG_FILE.exists():
        n = sum(1 for _ in LOG_FILE.open(encoding="utf-8", errors="ignore"))
        print("unregistered access log lines: %d" % n)
    return 0


def cmd_resolve(a) -> int:
    d = load()
    if a.session and a.session == d.get("orchestrator_session"):
        print("orchestrator"); return 0
    info = (d.get("sessions") or {}).get(a.session or "")
    print(info.get("role") if info else "unknown")
    return 0


def cmd_grants(a) -> int:
    g = ROLE_GRANTS.get(a.role)
    if not g:
        print("未知角色：%s；可用：%s" % (a.role, ", ".join(ROLE_GRANTS)), file=sys.stderr)
        return 2
    print(json.dumps(g, ensure_ascii=False, indent=1))
    return 0


def cmd_audit(a) -> int:
    """审计：未登记会话的访问记录（说明有多少次操作落在授权体系之外）。"""
    if not LOG_FILE.exists():
        print("AUDIT: 无未登记访问记录")
        return 0
    lines = [l for l in LOG_FILE.read_text(encoding="utf-8", errors="ignore").splitlines() if l.strip()]
    by_sess = {}
    for l in lines:
        sid = l.split("\t", 1)[0]
        by_sess[sid] = by_sess.get(sid, 0) + 1
    print("AUDIT: %d 条未登记访问，涉及 %d 个会话" % (len(lines), len(by_sess)))
    for sid, n in sorted(by_sess.items(), key=lambda x: -x[1])[:20]:
        print("  %-42s %d 次" % (sid, n))
    print("  （若某会话应受约束却出现在这里 → 派发时漏了 perm.py bind）")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("init"); i.add_argument("--run", required=True); i.add_argument("--orchestrator", default="")
    b = sub.add_parser("bind"); b.add_argument("--session", required=True); b.add_argument("--role", required=True)
    b.add_argument("--note", default=""); b.add_argument("--extra-read", action="append"); b.add_argument("--extra-write", action="append")
    u = sub.add_parser("unbind"); u.add_argument("--session", required=True)
    sub.add_parser("show")
    r = sub.add_parser("resolve"); r.add_argument("--session", required=True)
    g = sub.add_parser("grants"); g.add_argument("--role", required=True)
    sub.add_parser("audit")
    a = ap.parse_args()
    return {"init": cmd_init, "bind": cmd_bind, "unbind": cmd_unbind, "show": cmd_show,
            "resolve": cmd_resolve, "grants": cmd_grants, "audit": cmd_audit}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())