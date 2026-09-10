#!/usr/bin/env python3
"""hook 离线自测 v2（路径判定模型；覆盖 Codex 5 项收口）。

特点：
  - 用**临时清单**（测完恢复），不污染真实权限配置；
  - 全程 subprocess + JSON，无 shell 重定向，不产生中间文件（旧 bash 版会生成 chk）；
  - 模拟子代理真实 cwd（主仓库）+ worktree 绝对路径 —— 这是实测发现的漏拦场景；
  - 离线自测只证明脚本行为；真实接入验证另记（见 HOOKS-README §4.2）。
"""
import json, os, subprocess, sys
from pathlib import Path

H = Path(__file__).resolve().parent
WT = H.parents[1]
MAIN = str(WT.parents[1])            # 主仓库（子代理真实 cwd）
ORCH = "session-orchestrator-SELFTEST"


def write_manifest(d):
    (H / "permissions.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


def base_manifest(tickets=None, sessions=None):
    return {"run_id": "selftest", "orchestrator_session": ORCH,
            "sessions": sessions or {}, "tickets": tickets or []}


def run_hook(script, sid, tool, ti, cwd=MAIN):
    p = {"hook_event_name": "PreToolUse", "session_id": sid, "tool_name": tool,
         "tool_input": ti, "cwd": cwd}
    env = dict(os.environ)
    for k in ("DSH_SUBAGENT_ID", "DSH_HOOK_ORCHESTRATOR"):
        env.pop(k, None)
    r = subprocess.run([sys.executable, str(H / script)], input=json.dumps(p),
                       capture_output=True, text=True, env=env, timeout=30)
    return r.returncode


RESULTS = []


def check(name, got, exp):
    RESULTS.append((name, got, exp, got == exp))


def main():
    perm_file = H / "permissions.json"
    backup = perm_file.read_text(encoding="utf-8") if perm_file.exists() else None
    orch_file = H / "orchestrator.id"
    obackup = orch_file.read_text(encoding="utf-8") if orch_file.exists() else None
    orch_file.write_text(ORCH, encoding="utf-8")
    A = lambda p: str(WT / p)
    try:
        # ── 场景 A：已登记角色 + 最小授权 ──
        write_manifest(base_manifest(sessions={
            "gen-1": {"role": "generator", "extra_read": [], "extra_write": ["round/run2/staging/path-A.md"]},
            "deep-1": {"role": "deepener", "extra_read": ["round/run2/feedback/A3.md"], "extra_write": ["round/run2/drafts/A3.md"]},
            "hist-1": {"role": "history_reviewer", "extra_read": [], "extra_write": ["round/run2/op-history-review.md"]},
        }))
        g = "hook_access_guard.py"
        check("生成器读中性资料", run_hook(g, "gen-1", "read", {"file_path": A("round/zotero/ZOTERO-INDEX.md")}), 0)
        check("生成器读旧卡（拦）", run_hook(g, "gen-1", "read", {"file_path": A("round/run1/card-B3-window.md")}), 2)
        check("生成器写授权文件", run_hook(g, "gen-1", "write", {"file_path": A("round/run2/staging/path-A.md")}), 0)
        check("生成器写他人文件（拦）", run_hook(g, "gen-1", "write", {"file_path": A("round/run2/staging/other.md")}), 2)
        check("深化者读本卡反馈", run_hook(g, "deep-1", "read", {"file_path": A("round/run2/feedback/A3.md")}), 0)
        check("深化者读他人卡反馈（拦）", run_hook(g, "deep-1", "read", {"file_path": A("round/run2/feedback/B1.md")}), 2)
        check("深化者写自己深化稿", run_hook(g, "deep-1", "write", {"file_path": A("round/run2/drafts/A3.md")}), 0)
        check("深化者写他人深化稿（拦）", run_hook(g, "deep-1", "write", {"file_path": A("round/run2/drafts/B1.md")}), 2)
        check("历史审查者读历史索引", run_hook(g, "hist-1", "read", {"file_path": A("round/history/HISTORY-INDEX.md")}), 0)
        check("历史审查者写自己报告", run_hook(g, "hist-1", "write", {"file_path": A("round/run2/op-history-review.md")}), 0)
        check("历史审查者写他人报告（拦）", run_hook(g, "hist-1", "write", {"file_path": A("round/run2/op-history-review-X.md")}), 2)
        check("主控全权", run_hook(g, ORCH, "read", {"file_path": A("round/run1/card-B3-window.md")}), 0)
        # ── 场景 B：未登记（#2 首次访问） ──
        check("未登记读研究区（暂停）", run_hook(g, "stranger", "read", {"file_path": A("round/zotero/ZOTERO-INDEX.md")}), 2)
        check("未登记只访问区外（放行）", run_hook(g, "stranger", "read", {"file_path": "/tmp/x.md"}), 0)
        write_manifest(base_manifest(tickets=[{"role": "generator", "extra_read": [], "extra_write": ["round/run2/staging/t.md"]}],
                                     sessions={}))
        check("有票据→首次访问受控启动", run_hook(g, "newsub", "read", {"file_path": A("round/zotero/ZOTERO-INDEX.md")}), 0)
        check("领取后写授权文件", run_hook(g, "newsub", "write", {"file_path": A("round/run2/staging/t.md")}), 0)
        check("领取后读历史（拦）", run_hook(g, "newsub", "read", {"file_path": A("round/history/HISTORY-INDEX.md")}), 2)
        check("票据耗尽后另一会话（暂停）", run_hook(g, "newsub2", "read", {"file_path": A("round/zotero/ZOTERO-INDEX.md")}), 2)
        # ── 场景 C：workdir 相对路径（实测漏洞） ──
        write_manifest(base_manifest(sessions={"gen-2": {"role": "generator", "extra_read": [], "extra_write": ["round/run2/staging/p.md"]}}))
        check("bash+workdir 相对路径读旧卡（拦）",
              run_hook(g, "gen-2", "bash", {"command": "cat round/run1/card-B3-window.md", "workdir": str(WT)}), 2)
        check("bash+workdir 相对路径读中性",
              run_hook(g, "gen-2", "bash", {"command": "cat round/zotero/ZOTERO-INDEX.md", "workdir": str(WT)}), 0)
        # ── 场景 D：#4 清单损坏 ──
        perm_file.write_text("{broken", encoding="utf-8")
        check("损坏→研究会话失败关闭", run_hook(g, "gen-1", "read", {"file_path": A("round/zotero/ZOTERO-INDEX.md")}), 2)
        check("损坏→主控仍可修复", run_hook(g, ORCH, "read", {"file_path": A("round/zotero/ZOTERO-INDEX.md")}), 0)
        check("损坏→区外会话不受影响", run_hook(g, "other", "read", {"file_path": "/tmp/y.md"}, cwd="/tmp"), 0)
        # ── 场景 E：载荷异常 ──
        p = {"hook_event_name": "PreToolUse", "session_id": "gen-1", "tool_name": "read",
             "tool_input": {"file_path": "x"}, "cwd": MAIN}
        r = subprocess.run([sys.executable, str(H / g)], input="not-json{{{", capture_output=True, text=True, timeout=30)
        check("非法载荷→保守阻塞", r.returncode, 2)
    finally:
        if backup is None:
            perm_file.unlink(missing_ok=True)
        else:
            perm_file.write_text(backup, encoding="utf-8")
        if obackup is None:
            orch_file.unlink(missing_ok=True)
        else:
            orch_file.write_text(obackup, encoding="utf-8")
    passed = sum(1 for _, _, _, ok in RESULTS if ok)
    for name, got, exp, ok in RESULTS:
        print("  %s %-34s exit=%d 期望%d" % ("PASS" if ok else "FAIL", name, got, exp))
    print()
    print("SUMMARY %d passed / %d failed" % (passed, len(RESULTS) - passed))
    print("说明：离线自测；真实接入验证见 HOOKS-README §4.2。")
    return 1 if passed != len(RESULTS) else 0


if __name__ == "__main__":
    sys.exit(main())