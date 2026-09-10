# 返工验收摘要（REWORK SUMMARY，2026-09-10 R2）

> 范围：Codex+Luna 架构深审后的返工包（四组修复+验收+备份）。**选题推荐与实验仍冻结。**
> 状态：**待 Codex 架构返工验收**。完整台账：`round/ROUND-LOG.md`；小流程：`round/MINIFLOW-RECORD.md`。

## 1. 每项发现：复现 → 修法 → 验收

| # | 发现 | 复现结果 | 实际修法 | 验收 | 证据 |
|---|---|---|---|---|---|
| 2A | 检索失败被升级为新颖 | 空近邻→"novel"确认；执行异常裸逃出 novelty_check；test_vendor_adapters.py:195-197 确把空→novel 规定为正确 | patched_novelty.py：四态检索（ok_hits/ok_empty/service_unavailable/exec_error）；失败→incomplete 绝不输出 novel；成功无命中只支持"限定范围未命中"；服务失败即停（断点+未执行查询清单）；输出=线索+未决项，不认证新颖性 | T4 PASS；小流程中真实通道 429→degraded/incomplete 被原样记录 | round/logs/repro-group2.txt §A；round/tools/patched_novelty.py |
| 2B | 标题相似被升级为同一工作 | 判定级确认：dice=0.8632≥0.85→"same"；聚合逻辑按代码对 title-only 卡会输出 collision。**补充发现**：原件对多字段卡用展平文本首行比较，相似度被稀释→行为不稳定 | patched_novelty.py：相似度值域改 high/mid/low_similarity_lead（线索）；卡标题取 title 字段（修稀释）；LLM 提示词重写为覆盖比对（同信号≠覆盖，须引条件/机制依据）；same_or_covering 仅为主控裁决线索，不自动淘汰 | T5 PASS（相似标题不同条件→leads_only，非 collision 非 novel） | 同上 §B |
| 2C | 检查器异常被当作正确否定 | checker 异常与未知检查器在 expected=BLOCK 时 kind=正确、all_ok=True（audit.py 自称 fail-loud 实为 fail-into-pass） | patched_audit.py：五类记账（correct/false_release/false_kill/EXEC_ERROR/UNKNOWN_CHECKER/PARAM_ERROR）；all_ok 收紧=零执行错误；"程序未能检查"与"确实找到反例"分离 | T6 PASS（两类异常均使审计失败） | 同上 §C |
| 2D | 空字段/占位文本假通过 | 四例+补充第五例（rhos 有而 claimed_W 空→PASS）全部复现 | patched_checks.py：新增 INPUT_INSUFFICIENT（占位=TODO/待补/空）与 NOT_APPLICABLE；数值检查只对给定输入负责；PASS 理由限定"给定输入下成立" | T7 PASS（8 断言） | 同上 §D |
| 3A | 台账 CLI 崩溃+幂等缺失 | dataclass AttributeError（Python 3.14.2，根因=spec_from_file_location 未注册 sys.modules）精确复现；批内重复/同证据重试会重复入账（本线原实现自认） | 重写 ledger.py：自含数据结构（不跨 checkout 导入）；content_hash 幂等；批内投影实时更新；cand_id 稳定+唯一当前版本；修订=新版本行+supersedes_row；new_evidence 强制 source+judgment（fail-loud）；旧题匹配只报告不淘汰；LEDGER_SCHEMA_MISMATCH 拒写；doctor 残尾行识别+原子修复；appends fsync | T1/T2/T3/T8/T10 PASS（含重复执行/修订留痕/中断恢复） | round/logs/repro-ledger-cli.txt；round/tools/ledger.py |
| 3B | 审查不绑定版本、路径冲突 | 流程层面缺陷（审查意见无版本锚；模板禁读路径过宽） | REVIEW-ROLE-PROMPTS v2：意见强制记录 cand_id+实算 sha256；只读原件只写意见文件；同模型角色=互补意见声明；EFFECTIVE-RULES-R2 §5；ledger.py 承重修订自动置旧意见 needs_review（触发口径 R4 精化：承重字段仅纯空白差异不触发，标点/符号变化即触发；非承重字段修改不触发） | 小流程实测：R1-R3 登记@v1 哈希→v2 承重修订→自动全部 needs_review | round/MINIFLOW-RECORD.md |

**不同意见**：无未采纳的审查发现。两处精确化：①2B 的"进而 collision"在 title-only 卡成立，多字段卡实为稀释不稳定（已修）；②3A 根因=sys.modules 注册缺失（已记录，供原件 owner 参考）。

## 2. 已更正的旧"通过"声明

- run-test-20260910 验收线"误放0误杀0"→ 审计异常曾计入正确；现 all_ok 含执行错误记账。
- "unnoted≥40%/入池≥6"→ 取消验收资格，降为诊断记录（EFFECTIVE-RULES-R2 §1/§7）。
- "ledger add 完成"→ 原实现幂等/唯一当前版本/中断恢复均不成立，已重写并以回归证明。
- 三路生成产物"冷生成"→ 改标"接触过旧候选信息的试运行材料"（三文件头横幅）。

## 3. 完整小流程走到哪里

七步全部实际执行（入账→建设→近邻→证据→主控整合→修订→失效链→状态），证据=round/MINIFLOW-RECORD.md。
**未验证/超范围**：候选价值裁决（冻结）；语义同族自动检测（明确不做，主控人工兜底）；S2 实通（429，通道状态已记录）；UNDERMIND 深查（按收口标准未扩大）。

## 4. 版本 / 写入范围 / 测试 / 备份

- 分支 `agent/20260910-topic-loop`（base=origin/main 8a30409）；写集=round/**、ANALYSIS/TOPIC-LOOP-20260910/**、ANALYSIS/DOCUMENT-STATUS.json（登记 7 条目，纯增项）、.worktrees 外无触碰；research-ops checkout 只读未改。
- 测试：test_rework_regressions.py **10/10 PASS**；deps_check **20/20 一致**（含修复后重指纹，gen_manifest.py 流程化）；governance 检查在 worktree 内仅余主库既有 2 项 STALE_CURRENT。
- 备份：commit→push→**Draft PR**（见 PR 正文证据合同），未合并（待 Codex 验收）。

## 5. 阻碍恢复选题的事项 / 非阻塞优化

**阻碍**：无技术性阻塞。恢复选题前需 Codex 验收本返工包 + 用户解冻指令（流程性）。
**非阻塞（明确不做，按收口标准）**：sentence-transformers 嵌入后端（语义同族检测）；S2 API key；chatgpt_dispatch 插件修复；检查器覆盖面扩充；任何仪表盘/架构重设计。