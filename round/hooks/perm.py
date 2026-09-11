#!/usr/bin/env python3
"""权限清单 v3（按 Codex 5 项实查收口）。

v2 → v3 关键变化：
  #2 票据机制：派发前 reserve，子代理**首次访问时原子领取** → 消除"登记前空窗"；
     无票据的研究会话 → 暂停并报告（不再静默放行）；
  #3 最小授权：deepener/history_reviewer/reviewer 的读与写一律按**具体文件**授予，
     不用 cards/** 这类跨卡通配符；
  #4 运行隔离：init 默认清空旧会话；权限文件损坏 → 研究会话失败关闭（主控可恢复）。
"""
import argparse, json, os, sys, time
from pathlib import Path

HOOK_DIR = Path(__file__).resolve().parent
# 测试隔离（事故根因修复，2026-09-11）：
# 此前验证脚本直接写真实清单，两次把运行中的主控锁死。现支持环境变量重定向：
#   DSH_PERM_FILE / DSH_ORCH_FILE / DSH_HOOK_LOG 指向隔离副本 → 测试全程不碰真实状态。
PERM_FILE = Path(os.environ["DSH_PERM_FILE"]) if os.environ.get("DSH_PERM_FILE") else (HOOK_DIR / "permissions.json")
ORCH_FILE = Path(os.environ["DSH_ORCH_FILE"]) if os.environ.get("DSH_ORCH_FILE") else (HOOK_DIR / "orchestrator.id")
LOG_FILE = Path(os.environ["DSH_HOOK_LOG"]) if os.environ.get("DSH_HOOK_LOG") else (HOOK_DIR / "unregistered.log")

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
    d, st = load()
    prev_orch = d.get("orchestrator_session") or orchestrator_id()
    # 防锁定保护（实测事故）：清单存在且主控身份将变化时，必须显式 --force。
    # 背景：曾用临时清单覆盖真实清单，导致运行中的主控失去权限且无自助恢复路径。
    if st == "ok" and prev_orch and prev_orch != orch and not a.force:
        print("REFUSED: 当前清单主控为 %s，与本次 %s 不同。" % (prev_orch, orch), file=sys.stderr)
        print("  直接覆盖会让运行中的主控失去权限且无法自助恢复。", file=sys.stderr)
        print("  确认交接请加 --force；仅恢复损坏清单请先删除 permissions.json。", file=sys.stderr)
        return 2
    old = d.get("sessions") or {}
    if old and not a.keep:
        print("CLEARED %d 个旧会话绑定（新 run 不继承旧权限）" % len(old))
    hist = [h for h in (d.get("orchestrator_history") or []) if h != orch]
    hist = ([orch] + hist)[:3]
    save({
        "run_id": a.run,
        "orchestrator_session": orch,
        "orchestrator_history": hist,
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


def cmd_reserve(a) -> int:
    if a.role not in ROLE_GRANTS:
        print("REFUSED: 未知角色 %s" % a.role, file=sys.stderr)
        return 2
    d, st = load()
    if st != "ok":
        print("REFUSED: 权限清单状态 %s，先 init" % st, file=sys.stderr)
        return 2
    pend = d.get("tickets") or []
    roles = {t.get("role") for t in pend}
    if roles and roles != {a.role}:
        print("REFUSED: 已有未消费票据属其他角色（%s）——同批票据必须同角色以免错配"
              % ", ".join(sorted(roles)), file=sys.stderr)
        return 2
    # Codex 收口 #1（2026-09-11）：**禁止创建 target 为空的票据**。
    # 空 target 等于"谁先访问谁得权限"——正是原事故的成因。
    target = (getattr(a, "session", "") or "").strip()
    if not target:
        print("REFUSED: reserve 必须指定 --session（票据必须绑定具体子会话 ID；", file=sys.stderr)
        print("         会话 ID 未取得时保持未授权，取得后精确 grant/reserve 再读材料）。", file=sys.stderr)
        return 2
    for _ in range(a.count):
        pend.append({"role": a.role, "extra_read": a.extra_read or [],
                     "extra_write": a.extra_write or [], "note": a.note or "",
                     "session": target,
                     "reserved_at": time.strftime("%H:%M:%S")})
    d["tickets"] = pend
    save(d)
    print("RESERVED %d×%s (pending=%d)" % (a.count, a.role, len(pend)))
    return 0


def claim_ticket(session_id: str):
    """原子领取票据（供 hook 调用）。返回 (entry, reason)。"""
    d, st = load()
    if st != "ok":
        return None, "清单状态 %s" % st
    pend = d.get("tickets") or []
    if not pend:
        return None, "无预留票据"
    # Codex 收口 #1：领取函数**自身**必须验证目标匹配（不能只依赖调用方）。
    idx = next((i for i, t in enumerate(pend) if (t.get("session") or "").strip() == session_id), None)
    if idx is None:
        return None, "无绑定该会话的票据（票据必须用 --session 精确绑定）"
    t = pend.pop(idx)
    entry = {"role": t["role"], "extra_read": t.get("extra_read") or [],
             "extra_write": t.get("extra_write") or [],
             "note": (t.get("note") or "") + " | 票据领取",
             "bound_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
    d.setdefault("sessions", {})[session_id] = entry
    d["tickets"] = pend
    save(d)
    return entry, "claimed:%s" % t["role"]


def cmd_grant(a) -> int:
    """直接授权（推荐用法）：绑定「具体子会话 ID + 角色 + 任务文件」。

    与 reserve 的区别：grant 在**派发前**就知道会话 ID 时使用，直接写入 sessions，
    不经过"票据"这一中间态 —— 这是 Codex 要求的"授权绑定具体子会话"的强形式。
    """
    if a.role not in ROLE_GRANTS:
        print("REFUSED: 未知角色 %s" % a.role, file=sys.stderr)
        return 2
    if not a.session:
        print("REFUSED: grant 必须指定 --session（授权必须绑定具体子会话 ID）", file=sys.stderr)
        return 2
    d, st = load()
    if st != "ok":
        print("REFUSED: 权限清单状态 %s，先 init" % st, file=sys.stderr)
        return 2
    if a.session == d.get("orchestrator_session"):
        print("REFUSED: 不能把主控会话授权为研究角色", file=sys.stderr)
        return 2
    parent, origin = "", ""
    try:
        sys.path.insert(0, str(HOOK_DIR))
        import lib_hook as _L
        parent, origin = _L.session_origin(a.session)
    except Exception:
        pass
    allowed_parents = {d.get("orchestrator_session") or ""} | set(d.get("orchestrator_history") or [])
    allowed_parents.discard("")
    if parent and origin == "subagent" and parent not in allowed_parents:
        print("REFUSED: 该会话的父会话不在本清单主控集合内（parent=%s）" % parent, file=sys.stderr)
        return 2
    d.setdefault("sessions", {})[a.session] = {
        "role": a.role, "note": a.note or "",
        "extra_read": a.extra_read or [], "extra_write": a.extra_write or [],
        "parent": parent, "origin": origin,
        "granted_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    save(d)
    print("GRANTED %s -> %s (parent=%s origin=%s)" % (a.session, a.role, parent or "-", origin or "-"))
    return 0


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
    (d.get("sessions") or {}).pop(a.session, None)
    save(d)
    print("UNBOUND", a.session)
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
    i.add_argument("--force", action="store_true")
    r = sub.add_parser("reserve"); r.add_argument("--role", required=True); r.add_argument("--count", type=int, default=1)
    r.add_argument("--session", default="", help="绑定具体子会话 ID（推荐：指定后只有该会话可领票）")
    r.add_argument("--extra-read", action="append"); r.add_argument("--extra-write", action="append"); r.add_argument("--note", default="")
    b = sub.add_parser("bind"); b.add_argument("--session", required=True); b.add_argument("--role", required=True)
    b.add_argument("--note", default=""); b.add_argument("--extra-read", action="append"); b.add_argument("--extra-write", action="append")
    gr = sub.add_parser("grant"); gr.add_argument("--session", required=True); gr.add_argument("--role", required=True)
    gr.add_argument("--note", default=""); gr.add_argument("--extra-read", action="append"); gr.add_argument("--extra-write", action="append")
    u = sub.add_parser("unbind"); u.add_argument("--session", required=True)
    sub.add_parser("show")
    g = sub.add_parser("grants"); g.add_argument("--role", required=True)
    sub.add_parser("audit")
    a = ap.parse_args()
    return {"init": cmd_init, "reserve": cmd_reserve, "bind": cmd_bind, "grant": cmd_grant,
            "unbind": cmd_unbind, "show": cmd_show, "grants": cmd_grants, "audit": cmd_audit}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())