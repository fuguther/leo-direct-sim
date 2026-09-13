#!/usr/bin/env python3
"""精确会话权限与暂停/接续。匿名票据停用；CLI 写入由 flock 串行化。"""
import argparse, json, os, sys, time, fcntl
from pathlib import Path

HOOK_DIR = Path(__file__).resolve().parent
PERM_FILE = HOOK_DIR / "permissions.json"
ORCH_FILE = HOOK_DIR / "orchestrator.id"
LOG_FILE = HOOK_DIR / "unregistered.log"

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
HISTORY_READ = ["round/history/**", "round/run1/**", "round/CANDIDATE-LEDGER.csv", "round/reviews/**"]

ROLE_GRANTS = {
    "orchestrator": {"read": ["**"], "write": ["**"], "shell": "full"},
    "generator": {"read": NEUTRAL_READ, "write": [], "shell": "best_effort"},
    "deepener": {"read": NEUTRAL_READ, "write": [], "shell": "best_effort"},
    "history_reviewer": {"read": NEUTRAL_READ + HISTORY_READ, "write": [], "shell": "best_effort"},
    "reviewer": {"read": NEUTRAL_READ, "write": [], "shell": "best_effort"},
    "auditor": {"read": ["**"], "write": [], "shell": "best_effort"},
}


def load():
    """返回 (manifest, status)；status ∈ ok / missing / corrupt。"""
    if not PERM_FILE.exists():
        return {}, "missing"
    try:
        d = json.loads(PERM_FILE.read_text(encoding="utf-8"))
        return (d, "ok") if isinstance(d, dict) else ({}, "corrupt")
    except Exception:
        return {}, "corrupt"


def save(d: dict) -> None:
    d["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    tmp = PERM_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tmp, PERM_FILE)
    try:
        os.chmod(PERM_FILE, 0o600)
    except Exception:
        pass


def cmd_init(a) -> int:
    orch = a.orchestrator or os.environ.get("DSH_SESSION_ID") or ""
    if not orch:
        print("REFUSED: 无法确定主控 session_id", file=sys.stderr)
        return 2
    d, _ = load()
    old = d.get("sessions") or {}
    if d and d.get("run_status", "active") == "active":
        print("REFUSED: 已有活动运行；先 pause，再显式 resume 接续或 init 新建", file=sys.stderr)
        return 2
    if a.keep:
        print("REFUSED: init 不继承旧权限；接续请用 resume", file=sys.stderr)
        return 2
    if old and not a.keep:
        print("CLEARED %d 个旧会话绑定（新 run 不继承旧权限）" % len(old))
    save({
        "run_id": a.run, "run_status": "active",
        "orchestrator_session": orch,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "sessions": old if a.keep else {},
        "tickets": (d.get("tickets") or []) if a.keep else [],
    })
    ORCH_FILE.write_text(orch, encoding="utf-8")
    try:
        os.chmod(ORCH_FILE, 0o600)
    except Exception:
        pass
    print("INIT run=%s orchestrator=%s" % (a.run, orch))
    return 0


def cmd_reserve(a):
    print("REFUSED: 匿名票据已停用。create 后按 session_id bind，再派发工作。", file=sys.stderr)
    return 2


def claim_ticket(session_id):
    return None, "匿名领取已停用"


def cmd_bind(a) -> int:
    if a.role not in ROLE_GRANTS:
        print("REFUSED: 未知角色 %s" % a.role, file=sys.stderr)
        return 2
    d, st = load()
    if st != "ok":
        print("REFUSED: 权限清单状态 %s，先 init" % st, file=sys.stderr)
        return 2
    if a.session == d.get("orchestrator_session"):
        print("REFUSED: 不能把主控会话绑定为研究角色", file=sys.stderr)
        return 2
    if a.role == "orchestrator":
        print("REFUSED: 子任务不可提升为主控", file=sys.stderr); return 2
    existing = (d.get("sessions") or {}).get(a.session)
    if existing:
        print("REFUSED: session 已绑定；不得静默覆盖", file=sys.stderr); return 2
    for value in (a.extra_write or []):
        if any(c in value for c in "*?[") or Path(value).is_absolute() or ".." in Path(value).parts:
            print("REFUSED: 写授权必须是工作区内确切文件", file=sys.stderr); return 2
    d.setdefault("sessions", {})[a.session] = {
        "role": a.role, "note": a.note or "",
        "extra_read": a.extra_read or [], "extra_write": a.extra_write or [],
        "bound_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    save(d)
    print("BOUND %s -> %s" % (a.session, a.role))
    return 0


def cmd_unbind(a) -> int:
    d, st = load()
    if st != "ok":
        print("清单状态 %s" % st, file=sys.stderr); return 2
    d.setdefault("sessions", {})[a.session] = {"role": "revoked"}
    save(d)
    print("UNBOUND", a.session)
    return 0


def cmd_pause(a):
    d, st = load()
    if st != "ok": return 2
    d["run_status"] = "paused"
    save(d)
    print("PAUSED: 后续工具调用拒绝；仍需在 Harness 取消活动请求并核对完成状态")
    return 0


def cmd_resume(a):
    d, st = load()
    if st != "ok" or d.get("run_status") != "paused" or d.get("run_id") != a.run:
        print("REFUSED: 只能接续匹配的暂停运行", file=sys.stderr); return 2
    if not a.orchestrator or not a.receipt or not Path(a.receipt).is_file():
        print("REFUSED: 须提供新主控身份及任务接续核对记录", file=sys.stderr); return 2
    try:
        receipt = json.loads(Path(a.receipt).read_text())
        if receipt.get("run_id") != a.run or receipt.get("active_sessions") != []:
            raise ValueError("run_id 不匹配或仍有活动会话")
        jobs = receipt["tasks"]
        if not isinstance(jobs, list) or not all(isinstance(x, dict) and x.get("task_id") and
                x.get("state") in {"completed", "cancelled", "failed", "pending"} for x in jobs):
            raise ValueError("任务核对记录不完整")
        for task in jobs:
            if task["state"] == "completed":
                import hashlib
                artifact = Path(task["artifact"])
                if hashlib.sha256(artifact.read_bytes()).hexdigest() != task["sha256"]:
                    raise ValueError("完成产物缺失或哈希变化")
    except Exception as exc:
        print("REFUSED: 接续记录校验失败: %s" % exc, file=sys.stderr); return 2
    # Old worker sessions remain revoked; outputs and research ledger remain intact.
    d["sessions"] = {sid: {"role": "revoked"} for sid in d.get("sessions", {})}
    d["tickets"] = []
    d["orchestrator_session"] = a.orchestrator
    d["run_status"] = "active"
    d["resume_receipt"] = str(Path(a.receipt).resolve())
    save(d)
    ORCH_FILE.write_text(a.orchestrator, encoding="utf-8")
    print("RESUMED: 根据核对记录只派发未完成任务，旧子会话权限已撤销")
    return 0


def cmd_show(a) -> int:
    d, st = load()
    print("清单状态: %s" % st)
    if st != "ok":
        return 0
    print("run_id: %s" % d.get("run_id"))
    print("orchestrator: %s" % d.get("orchestrator_session"))
    sess = d.get("sessions") or {}
    print("bound sessions: %d" % len(sess))
    for sid, info in sess.items():
        print("  %-44s %-18s +read=%s +write=%s" % (sid, info.get("role"),
              info.get("extra_read") or "-", info.get("extra_write") or "-"))
    pend = d.get("tickets") or []
    print("pending tickets: %d %s" % (len(pend), [t.get("role") for t in pend] or ""))
    return 0


def cmd_grants(a) -> int:
    g = ROLE_GRANTS.get(a.role)
    if not g:
        print("未知角色：%s" % a.role, file=sys.stderr); return 2
    print(json.dumps(g, ensure_ascii=False, indent=1))
    return 0


def cmd_audit(a) -> int:
    if not LOG_FILE.exists():
        print("AUDIT: 无未登记访问记录")
        return 0
    lines = [l for l in LOG_FILE.read_text(encoding="utf-8", errors="ignore").splitlines() if l.strip()]
    by = {}
    for l in lines:
        sid = l.split("\t", 1)[0]
        by[sid] = by.get(sid, 0) + 1
    print("AUDIT: %d 条未登记访问，涉及 %d 个会话" % (len(lines), len(by)))
    for sid, n in sorted(by.items(), key=lambda x: -x[1])[:20]:
        print("  %-44s %d 次" % (sid, n))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("init"); i.add_argument("--run", required=True)
    i.add_argument("--orchestrator", default=""); i.add_argument("--keep", action="store_true")
    r = sub.add_parser("reserve"); r.add_argument("--role", required=True); r.add_argument("--count", type=int, default=1)
    r.add_argument("--extra-read", action="append"); r.add_argument("--extra-write", action="append"); r.add_argument("--note", default="")
    b = sub.add_parser("bind"); b.add_argument("--session", required=True); b.add_argument("--role", required=True)
    b.add_argument("--note", default=""); b.add_argument("--extra-read", action="append"); b.add_argument("--extra-write", action="append")
    u = sub.add_parser("unbind"); u.add_argument("--session", required=True)
    sub.add_parser("pause")
    rs = sub.add_parser("resume"); rs.add_argument("--run", required=True)
    rs.add_argument("--orchestrator", required=True); rs.add_argument("--receipt", required=True)
    sub.add_parser("show")
    g = sub.add_parser("grants"); g.add_argument("--role", required=True)
    sub.add_parser("audit")
    a = ap.parse_args()
    lock = open(HOOK_DIR / "permissions.lock", "a")
    fcntl.flock(lock, fcntl.LOCK_EX)
    return {"init": cmd_init, "reserve": cmd_reserve, "bind": cmd_bind, "unbind": cmd_unbind,
            "pause": cmd_pause, "resume": cmd_resume, "show": cmd_show, "grants": cmd_grants, "audit": cmd_audit}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())