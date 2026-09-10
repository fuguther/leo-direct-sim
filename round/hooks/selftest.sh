#!/bin/bash
# hook 套件自测：11 个用例，全部应通过。可反复运行。
W="$(cd "$(dirname "$0")/../.." && pwd)"
H="$W/round/hooks"
pass=0; fail=0

chk() { # chk <名称> <期望exit> <实际exit>
  if [ "$2" = "$3" ]; then echo "  PASS $1 (exit=$3)"; pass=$((pass+1));
  else echo "  FAIL $1 (期望 $2, 实际 $3)"; fail=$((fail+1)); fi
}

run() { # run <脚本> <json> [env]
  if [ -n "$3" ]; then echo "$2" | env DSH_SUBAGENT_ID="$3" python3 "$H/$1" >/dev/null 2>&1; else echo "$2" | python3 "$H/$1" >/dev/null 2>&1; fi
  echo $?
}

echo "== hook #1 黑名单拦截 =="
J1="{\"hook_event_name\":\"PreToolUse\",\"tool_name\":\"read\",\"tool_input\":{\"file_path\":\"round/run1/card-B3-window.md\"},\"cwd\":\"$W\"}"
J1s="{\"hook_event_name\":\"PreToolUse\",\"tool_name\":\"read\",\"tool_input\":{\"file_path\":\"round/run1/card-B3-window.md\"},\"cwd\":\"$W\",\"agent_id\":\"sub-1\"}"
chk "生成器读黑名单→阻塞" 2 "$(run hook_blacklist_guard.py "$J1s" sub-1)"
chk "主控读同文件→放行"  0 "$(run hook_blacklist_guard.py "$J1")"
J3s="{\"hook_event_name\":\"PreToolUse\",\"tool_name\":\"read\",\"tool_input\":{\"file_path\":\"round/zotero/ZOTERO-INDEX.md\"},\"cwd\":\"$W\",\"agent_id\":\"sub-1\"}"
chk "生成器读白名单→放行" 0 "$(run hook_blacklist_guard.py "$J3s" sub-1)"
J4s="{\"hook_event_name\":\"PreToolUse\",\"tool_name\":\"bash\",\"tool_input\":{\"command\":\"ls round/run1/\"},\"cwd\":\"$W\",\"agent_id\":\"sub-1\"}"
chk "ls 黑名单目录→阻塞"  2 "$(run hook_blacklist_guard.py "$J4s" sub-1)"

echo "== hook #2 台账完整性 =="
J5="{\"hook_event_name\":\"PostToolUse\",\"tool_name\":\"bash\",\"tool_input\":{\"command\":\"python3 round/tools/ledger.py revise\"},\"tool_response\":{\"stdout\":\"REVISED x v2 承重变化=[conditions]\"}}"
chk "revise 无失效→阻塞" 2 "$(run hook_ledger_integrity.py "$J5")"
J6="{\"hook_event_name\":\"PostToolUse\",\"tool_name\":\"bash\",\"tool_input\":{\"command\":\"python3 round/tools/ledger.py revise\"},\"tool_response\":{\"stdout\":\"REVISED x v2 承重变化=[c] REVIEWS_INVALIDATED: [R1]\"}}"
chk "revise 带失效→放行" 0 "$(run hook_ledger_integrity.py "$J6")"
J7="{\"hook_event_name\":\"PostToolUse\",\"tool_name\":\"bash\",\"tool_input\":{\"command\":\"ls\"},\"tool_response\":{\"stdout\":\"ok\"}}"
chk "非 ledger→放行"     0 "$(run hook_ledger_integrity.py "$J7")"

echo "== hook #3 交付门槛 =="
J8="{\"hook_event_name\":\"PreToolUse\",\"tool_name\":\"write\",\"tool_input\":{\"file_path\":\"ANALYSIS/TOPIC-LOOP-20260910/run2/MAIN-REPORT.md\"},\"cwd\":\"$W\",\"agent_id\":\"sub-9\"}"
chk "子代理无闸门表→阻塞" 2 "$(run hook_delivery_gate.py "$J8" sub-9)"
chk "主控写交付物→放行"   0 "$(echo "$J8" | env -u DSH_SUBAGENT_ID python3 "$H/hook_delivery_gate.py" >/dev/null 2>chk "主控写交付物→放行"   0 "$(run hook_delivery_gate.py "$J8")"1; echo $?)"

echo "== hook #4 提示词边界 =="
J10="{\"hook_event_name\":\"PreToolUse\",\"tool_name\":\"subagent\",\"tool_input\":{\"prompt\":\"请阅读 round/history/HISTORY-INDEX.md 后深化\"}}"
chk "提示词含历史全集→阻塞" 2 "$(run hook_prompt_scope.py "$J10")"
J11="{\"hook_event_name\":\"PreToolUse\",\"tool_name\":\"subagent\",\"tool_input\":{\"prompt\":\"输入：本卡 + round/run2/feedback/x-feedback.md\"}}"
chk "提示词仅本卡反馈→放行" 0 "$(run hook_prompt_scope.py "$J11")"

echo; echo "SUMMARY $pass passed / $fail failed"
[ "$fail" = "0" ]