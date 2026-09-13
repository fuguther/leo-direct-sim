#!/usr/bin/env python3
"""hook：台账操作事后诊断（PostToolUse）——【诊断件，非门禁】。

定位修正（Codex 收口 #3）：
  - 本 hook 只做**事后诊断**，不声称能自动纠正任何已发生的操作；
  - 真正的前置门禁在台账内部（ledger.py status 对 recommended_* 的判定绑定校验）；
  - 因此：载荷解析失败 → 记录并放行（诊断件不应因协议异常阻断研究接力）。
"""
import json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_hook import note, read_input


def main() -> None:
    p = read_input()
    if p.get("_parse_error"):
        note("台账诊断：载荷无法解析，跳过（诊断件不阻断）")
        sys.exit(0)
    ti = p.get("tool_input") or {}
    blob = json.dumps(ti, ensure_ascii=False)
    resp = p.get("tool_response")
    if isinstance(resp, (dict, list)):
        resp = json.dumps(resp, ensure_ascii=False)
    joined = blob + " " + str(resp or "")
    if "ledger.py" not in joined:
        sys.exit(0)
    if "revise" in blob and "REVISED" in joined and "REVIEWS_INVALIDATED" not in joined and "承重变化=[]" not in joined:
        note("诊断：revise 有承重变化但未见 REVIEWS_INVALIDATED —— 请复查是否漏传 --reviews")
    if "review-register" in joined and "REGISTERED" in joined and not re.search(r"[0-9a-f]{16}", joined):
        note("诊断：review-register 未见 candidate_file_sha256 前缀 —— 双哈希绑定可能不完整")
    if "merge" in joined and "MERGED" in joined and "理由已留痕" not in joined:
        note("诊断：merge 未见理由留痕 —— 请确认 --reason 已记录")
    sys.exit(0)


if __name__ == "__main__":
    main()