#!/usr/bin/env python3
"""hook 隔离自测 v3（2026-09-11，事故后重写）。

隔离保证（Codex 要求 #2）：
  1. 全程使用独立隔离状态目录（tempdir），经 DSH_PERM_FILE / DSH_ORCH_FILE / DSH_HOOK_LOG
     重定向 —— 绝不读写真实权限清单；子进程继承隔离环境；
  2. 测试前后核对真实清单与锚点的 sha256，**必须保持不变**。
"""
import hashlib, json, os, subprocess, sys, tempfile
from pathlib import Path

H = Path(__file__).resolve().parent
WT = H.parents[1]
MAIN = "/Users/lge/Desktop/leo-direct-sim"
REAL_PERM = H / "permissions.json"
REAL_ORCH = H / "orchestrator.id"
REAL_LOG = H / "unregistered.log"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else "(absent)"


def real_state() -> dict:
    return {"perm": sha(REAL_PERM), "orch": sha(REAL_ORCH), "log": sha(REAL_LOG)}


def main() -> int:
    before = real_state()
    results = []
    with tempfile.TemporaryDirectory() as iso_tmp:
        iso = Path(iso_tmp)
        perm = iso / "iso-perm.json"
        orch = iso / "iso-orch.id"
        log = iso / "iso.log"
        env = dict(os.environ)
        env.update({"DSH_PERM_FILE": str(perm), "DSH_ORCH_FILE": str(orch), "DSH_HOOK_LOG": str(log)})
        for k in ("DSH_SUBAGENT_ID", "DSH_HOOK_ORCHESTRATOR"):
            env.pop(k, None)
        ORCH = "session-orchestrator-SELFTEST"
        orch.write_text(ORCH, encoding="utf-8")
        A = lambda rel: str(WT / rel)
        G = "hook_access_guard.py"
        P = "hook_prompt_scope.py"

        def write_manifest(sessions=None, tickets=None):
            perm.write_text(json.dumps({"run_id": "selftest", "orchestrator_session": ORCH,
                                        "orchestrator_history": [ORCH],
                                        "sessions": sessions or {}, "tickets": tickets or []},
                                       ensure_ascii=False), encoding="utf-8")

        def run(script, sid, tool, ti, cwd=MAIN):
            payload = {"hook_event_name": "PreToolUse", "session_id": sid, "tool_name": tool,
                       "tool_input": ti, "cwd": cwd}
            return subprocess.run([sys.executable, str(H / script)], input=json.dumps(payload),
                                  capture_output=True, text=True, env=env, timeout=30).returncode

        def chk(name, got, exp):
            results.append((name, got, exp, got == exp))

        # 1. 角色最小授权
        write_manifest(sessions={
            "gen-1": {"role": "generator", "extra_read": [], "extra_write": ["round/run2/staging/path-A.md"]},
            "deep-1": {"role": "deepener", "extra_read": ["round/run2/feedback/A3.md"], "extra_write": ["round/run2/drafts/A3.md"]},
            "hist-1": {"role": "history_reviewer", "extra_read": [], "extra_write": ["round/run2/op-history-review.md"]},
        })
        chk("生成器读中性资料", run(G, "gen-1", "read", {"file_path": A("round/zotero/ZOTERO-INDEX.md")}), 0)
        chk("生成器读旧卡(拦)", run(G, "gen-1", "read", {"file_path": A("round/run1/card-B3-window.md")}), 2)
        chk("生成器写授权文件", run(G, "gen-1", "write", {"file_path": A("round/run2/staging/path-A.md")}), 0)
        chk("生成器写他人文件(拦)", run(G, "gen-1", "write", {"file_path": A("round/run2/staging/other.md")}), 2)
        chk("深化者读本卡反馈", run(G, "deep-1", "read", {"file_path": A("round/run2/feedback/A3.md")}), 0)
        chk("深化者读他人卡反馈(拦)", run(G, "deep-1", "read", {"file_path": A("round/run2/feedback/B1.md")}), 2)
        chk("历史审查者读历史索引", run(G, "hist-1", "read", {"file_path": A("round/history/HISTORY-INDEX.md")}), 0)
        chk("历史审查者写他人报告(拦)", run(G, "hist-1", "write", {"file_path": A("round/run2/op-history-review-X.md")}), 2)
        chk("主控全权", run(G, ORCH, "read", {"file_path": A("round/run1/card-B3-window.md")}), 0)

        # 2. 未授权会话暂停
        chk("未登记读研究区(暂停)", run(G, "stranger", "read", {"file_path": A("round/zotero/ZOTERO-INDEX.md")}), 2)
        chk("未登记只读区外(放行)", run(G, "stranger", "read", {"file_path": "/tmp/x.md"}), 0)

        # 3. 绑定具体会话（Codex 要求 #3）
        write_manifest(tickets=[{"role": "history_reviewer", "extra_read": [], "extra_write": [], "session": ""}])
        chk("无关会话领票(拦)", run(G, "unrelated-xyz", "read", {"file_path": A("round/history/HISTORY-INDEX.md")}), 2)
        write_manifest(sessions={"gen-2": {"role": "generator", "extra_read": [], "extra_write": ["round/run2/staging/p.md"]}},
                       tickets=[{"role": "history_reviewer", "extra_read": [], "extra_write": [], "session": ""}])
        chk("同主控生成器读历史(拦)", run(G, "gen-2", "read", {"file_path": A("round/history/HISTORY-INDEX.md")}), 2)
        write_manifest(tickets=[{"role": "history_reviewer", "extra_read": [], "extra_write": [], "session": "hist-target-1"}])
        chk("票据绑定他人(拦)", run(G, "hist-other-9", "read", {"file_path": A("round/history/HISTORY-INDEX.md")}), 2)

        # 4. shell 尽力检测
        write_manifest(sessions={"gen-3": {"role": "generator", "extra_read": [], "extra_write": ["round/run2/staging/p.md"]}})
        chk("bash 列历史目录(拦)", run(G, "gen-3", "bash", {"command": "ls round/history/", "workdir": str(WT)}), 2)
        chk("bash 读旧卡(拦)", run(G, "gen-3", "bash", {"command": "cat round/run1/card-B3-window.md", "workdir": str(WT)}), 2)
        chk("bash 普通命令(放行)", run(G, "gen-3", "bash", {"command": "echo hello"}, 0), 0)

        # 5. 清单损坏/缺失
        perm.write_text("{broken", encoding="utf-8")
        chk("损坏→研究会话关闭", run(G, "gen-1", "read", {"file_path": A("round/zotero/ZOTERO-INDEX.md")}), 2)
        chk("损坏→主控可修复", run(G, ORCH, "read", {"file_path": A("round/zotero/ZOTERO-INDEX.md")}), 0)
        chk("损坏→区外不受影响", run(G, "other", "read", {"file_path": "/tmp/y.md"}, cwd="/tmp"), 0)
        perm.unlink(missing_ok=True)
        chk("缺失→主控可修复", run(G, ORCH, "read", {"file_path": A("round/zotero/ZOTERO-INDEX.md")}), 0)

        # 6. 非法载荷
        r = subprocess.run([sys.executable, str(H / G)], input="not-json{{{",
                           capture_output=True, text=True, env=env, timeout=30)
        chk("非法载荷→保守阻塞", r.returncode, 2)

        # 7. 历史审查可派发 / 其他角色不可携带历史全集
        def runp(prompt):
            payload = {"hook_event_name": "PreToolUse", "session_id": ORCH, "tool_name": "subagent",
                       "tool_input": {"prompt": prompt}, "cwd": MAIN}
            return subprocess.run([sys.executable, str(H / P)], input=json.dumps(payload),
                                  capture_output=True, text=True, env=env, timeout=30).returncode
        chk("历史审查任务可派发", runp("你是历史碰撞审查者（role: history_reviewer），请读 round/history/HISTORY-INDEX.md"), 0)
        chk("非历史角色带历史全集(拦)", runp("你是生成器，请先读 round/history/HISTORY-INDEX.md"), 2)

    after = real_state()
    passed = sum(1 for _, _, _, ok in results if ok)
    for name, got, exp, ok in results:
        print("  %s %-30s exit=%d 期望%d" % ("PASS" if ok else "FAIL", name, got, exp))
    print()
    print("隔离校验（真实状态必须不变）：")
    isolation_ok = True
    for k in ("perm", "orch", "log"):
        same = before[k] == after[k]
        isolation_ok = isolation_ok and same
        print("  %s %-5s %s" % ("PASS" if same else "FAIL", k, before[k][:16]))
    print()
    print("SUMMARY %d passed / %d failed | 隔离:%s" % (passed, len(results) - passed, "OK" if isolation_ok else "VIOLATED"))
    return 0 if (passed == len(results) and isolation_ok) else 1


if __name__ == "__main__":
    sys.exit(main())