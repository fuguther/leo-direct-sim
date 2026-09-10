#!/usr/bin/env python3
"""hook #2：审查绑定完整性（PostToolUse）。

监听 ledger.py 的写入操作，检查：
  - revise 承重字段变更 → 必须产生 REVIEWS_INVALIDATED 输出（否则旧审查静默存活）；
  - review-register → 必须带合法的 64 位 candidate_file_sha256 与真实 content_hash；
  - merge → 必须留 reason。

PostToolUse 不能"阻塞已发生的动作"，但能：exit 2 让模型看到错误并要求补救；
因此本 hook 的语义是"事后强制自纠"（比不检查强，比 PreToolUse 弱——协议限制）。
"""
import json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_hook import block, read_input


def main() -> None:
    p = read_input()
    if p.get("_parse_error"):
        sys.exit(0)  # 事后检查不做硬失败
    tool = p.get("tool_name") or ""
    ti = p.get("tool_input") or {}
    blob = json.dumps(ti, ensure_ascii=False)
    resp = json.dumps(p.get("tool_response") or p.get("tool_result") or {}, ensure_ascii=False)

    if "ledger.py" not in blob:
        sys.exit(0)
    joined = blob + " " + resp

    # revise：承重字段变更必须触发审查失效
    if re.search(r"ledger\.py\"?,?\s*\"?revise|revise\s+--cand-id", joined) or "revise" in blob:
        if "承重变化" in joined or "REVISED" in joined:
            if "REVIEWS_INVALIDATED" not in joined and "审查失效" not in joined:
                block(
                    "ledger revise 完成了承重字段变更，但输出中没有 REVIEWS_INVALIDATED —— 旧审查可能仍显示 active（判断可信度漏洞）",
                    "检查是否误用了 --reviews 参数；承重变更必须让审过旧 content_hash 的意见置 needs_review",
                )
    # review-register：必须带 64 位 sha256
    if "review-register" in joined:
        if "REGISTERED" in joined and not re.search(r"[0-9a-f]{16}", joined):
            block(
                "review-register 登记成功但未见 candidate_file_sha256 前缀 —— 双哈希绑定可能不完整",
                "必须用 --candidate-file（工具实算）或 --candidate-file-sha256（64 位十六进制）",
            )
    # merge：必须留理由
    if "merge" in joined and "MERGED" in joined:
        if not re.search(r"理由已留痕|reason", joined):
            block("merge 未见理由留痕", "merge 必须带 --reason，便于日后追溯合并依据")
    sys.exit(0)


if __name__ == "__main__":
    main()