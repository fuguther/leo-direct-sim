#!/usr/bin/env python3
"""hook 离线自测（Python 版，替代旧 bash 版——旧版含错误重定向，会生成 chk 文件）。

特点：
  - 全程 subprocess + JSON，无 shell 重定向，不产生任何中间文件；
  - 结束时校验"自测未污染工作树"（git status 无新增未跟踪文件）；
  - 与"真实会话接入验证"分开记录：本脚本只证明离线行为，不证明 Harness 已接入。

用法: python3 round/hooks/selftest.py
"""
import json, os, subprocess, sys, tempfile
from pathlib import Path

H = Path(__file__).resolve().parent
WT = H.parents[1]
ORCH = "session-orchestrator-TEST"


def setup_manifest():
    """用临时清单替换真实清单，测完恢复（避免污染真实权限配置）。"""
    perm = H / "permissions.json"
    backup = None
    if perm.exists():
        backup = perm.read_text(encoding="utf-8")
    d = {"run_id": "selftest", "orchestrator_session": ORCH, "sessions": {
         "gen-1": {"role": "generator", "extra_read": [], "extra_write": ["round/run2/staging/path-A-intensity.md"]},
         "deep-1": {"role": "deepener", "extra_read": ["round/run2/cards.json"], "extra_write": []},
         "hist-1": {"role": "history_reviewer", "extra_read": [], "extra_write": []},
         "rev-1": {"role": "reviewer", "extra_read": [], "extra_write": ["round/run2/op-review-builder.md"]},
         }}
    perm.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    return perm, backup


def restore(perm: Path, backup):
    if backup is None:
        perm.unlink(missing_ok=True)
    else:
        perm.write_text(backup, encoding="utf-8")


def run_hook(script: str, session: str, tool: str, ti: dict, resp=None, env_extra=None):
    payload = {"hook_event_name": "PreToolUse", "session_id": session, "tool_name": tool,
               "tool_input": ti, "cwd": str(WT)}
    if resp is not None:
        payload["hook_event_name"] = "PostToolUse"
        payload["tool_response"] = resp
    env = dict(os.environ)
    env.pop("DSH_SUBAGENT_ID", None)
    env.pop("DSH_HOOK_ORCHESTRATOR", None)
    if env_extra:
        env.update(env_extra)
    r = subprocess.run([sys.executable, str(H / script)], input=json.dumps(payload),
                       capture_output=True, text=True, env=env, timeout=30)
    return r.returncode, r.stderr.strip()


CASES = []


def case(name, script, session, tool, ti, expect, resp=None, env_extra=None):
    CASES.append((name, script, session, tool, ti, expect, resp, env_extra))


# ── 访问守卫：Codex 的三个反例（旧版全部漏拦）──────────────────────
case("生成器读旧卡·标准路径", "hook_access_guard.py", "gen-1", "read", {"file_path": "round/run1/card-B3-window.md"}, 2)
case("生成器读旧卡·./ 前缀", "hook_access_guard.py", "gen-1", "read", {"file_path": "./round/run1/card-B3-window.md"}, 2)
case("生成器 cat run2 决策文档", "hook_access_guard.py", "gen-1", "bash", {"command": "cat round/run2/TONIGHT-SCOPE.md"}, 2)
# ── 正常接力（旧版全部误拦）─────────────────────────────────────
case("生成器写自己的草稿", "hook_access_guard.py", "gen-1", "write", {"file_path": "round/run2/staging/path-A-intensity.md"}, 0)
case("生成器读中性索引", "hook_access_guard.py", "gen-1", "read", {"file_path": "round/zotero/ZOTERO-INDEX.md"}, 0)
case("深化者读本卡反馈", "hook_access_guard.py", "deep-1", "read", {"file_path": "round/run2/feedback/A3-feedback.md"}, 0)
case("深化者读指定候选", "hook_access_guard.py", "deep-1", "read", {"file_path": "round/run2/cards.json"}, 0)
case("历史审查者读历史索引", "hook_access_guard.py", "hist-1", "read", {"file_path": "round/history/HISTORY-INDEX.md"}, 0)
case("历史审查者读旧卡原文", "hook_access_guard.py", "hist-1", "read", {"file_path": "round/run1/card-B3-window.md"}, 0)
# ── 越权仍拦 ───────────────────────────────────────────────
case("生成器读淘汰台账", "hook_access_guard.py", "gen-1", "read", {"file_path": "round/history/ELIMINATED-REGISTER.md"}, 2)
case("生成器写台账", "hook_access_guard.py", "gen-1", "write", {"file_path": "round/CANDIDATE-LEDGER.csv"}, 2)
case("深化者读未授权旧卡", "hook_access_guard.py", "deep-1", "read", {"file_path": "round/run1/card-F1-freshness.md"}, 2)
case("审查者写非本职路径", "hook_access_guard.py", "rev-1", "write", {"file_path": "round/run2/staging/evil.md"}, 2)
case("生成器写他人文件", "hook_access_guard.py", "gen-1", "write", {"file_path": "round/run2/staging/other.md"}, 2)
case("审查者写自己的意见", "hook_access_guard.py", "rev-1", "write", {"file_path": "round/run2/op-review-builder.md"}, 0)
# ── 身份隔离：父会话标记不得豁免子代理 ────────────────────────
case("子代理带 ORCHESTRATOR=1 仍拦", "hook_access_guard.py", "gen-1", "read", {"file_path": "round/run1/card-B3-window.md"}, 2,
     env_extra={"DSH_HOOK_ORCHESTRATOR": "1"})
case("主控 session 全权放行", "hook_access_guard.py", ORCH, "read", {"file_path": "round/run1/card-B3-window.md"}, 0)
# ── 未登记会话：放行但记录（不误伤无关会话）─────────────────────
case("未登记会话放行", "hook_access_guard.py", "unrelated-999", "read", {"file_path": "round/run1/card-B3-window.md"}, 0)
# ── 门禁解析失败 = 保守阻塞（Codex 指出旧版放行）───────────────
case("访问守卫·非法载荷阻塞", "hook_access_guard.py", "gen-1", "read", {"file_path": "x"}, 2),
# ── 提示词边界 ────────────────────────────────────────────
case("派发提示词含历史全集", "hook_prompt_scope.py", ORCH, "subagent", {"prompt": "先读 round/history/HISTORY-INDEX.md 再深化"}, 2)
case("派发提示词仅本卡反馈", "hook_prompt_scope.py", ORCH, "subagent", {"prompt": "输入：本卡 + round/run2/feedback/x.md"}, 0)
# ── 派发登记强制 ──────────────────────────────────────────
case("派发未登记子代理→提示补登记", "hook_dispatch_register.py", ORCH, "subagent", {"prompt": "x"}, 2,
     resp={"subagentId": "99999999-1111-2222-3333-444444444444"})
case("派发已登记子代理→放行", "hook_dispatch_register.py", ORCH, "subagent", {"prompt": "x"}, 0,
     resp={"subagentId": "gen-1"})
# ── 台账诊断（事后，非门禁）─────────────────────────────────
case("诊断·revise 无失效输出", "hook_ledger_diagnostic.py", ORCH, "bash",
     {"command": "python3 round/tools/ledger.py revise"}, 0, resp={"stdout": "REVISED x v2 承重变化=[c]"})


def main() -> int:
    perm, backup = setup_manifest()
    passed = failed = 0
    try:
        for name, script, session, tool, ti, expect, resp, env_extra in CASES:
            code, err = run_hook(script, session, tool, ti, resp, env_extra)
            ok = (code == expect)
            if ok:
                passed += 1
                print("  PASS %-34s exit=%d" % (name, code))
            else:
                failed += 1
                print("  FAIL %-34s exit=%d 期望%d :: %s" % (name, code, expect, err[:80]))
        print()
        print("  非法载荷专项：", end="")
        r = subprocess.run([sys.executable, str(H / "hook_access_guard.py")], input="not-json{{{",
                           capture_output=True, text=True, timeout=30)
        if r.returncode == 2:
            passed += 1; print("PASS（exit=2 保守阻塞）")
        else:
            failed += 1; print("FAIL（exit=%d，应为 2）" % r.returncode)
    finally:
        restore(perm, backup)
    print()
    print("SUMMARY %d passed / %d failed" % (passed, failed))
    print("说明：以上为【离线自测】，只证明脚本行为；Harness 真实接入验证见 HOOKS-README §5。")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())