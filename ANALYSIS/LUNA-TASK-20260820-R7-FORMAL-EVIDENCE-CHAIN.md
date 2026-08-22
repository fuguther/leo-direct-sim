# Luna 任务书：关闭 R7-F1 正式证据链阻断

> **HISTORICAL TASK**：该任务书只绑定下列旧基线和分支，不是当前 Agent 指令。现行任务从 `../AGENT-START-HERE.md` 进入，并重新核对 finding、SHA 和授权链。

> 状态：`FROZEN TASK CONTRACT`  
> 任务 owner：Luna（唯一代码写入者）  
> 总控与终判：Codex  
> 基线：`origin/main@63cc4a83c96bc51563d519764554bca4f333c0d0`  
> 目标分支：`codex/luna-20260820-r7-formal-evidence-chain`  
> 风险级别：承重改动；涉及 `experiment_platform` 授权/证据链，生产者不得自批

## 1. 背景与目标

用户的近期总目标是尽快把 leo_sim V2 做到“可以可信地跑正式实验”，随后按
`ANALYSIS/EXPERIMENT-PROGRAM.md` 依次完成 Q0、E0、PILOT-ALL 和正式实验。

当前 `ANALYSIS/FINDINGS-REGISTRY.md` 的 `R7-F1` 是明确的 `blocking FACT`：正式
compile → review → authorize → run receipt → analysis → claim 链引用了缺失的
`ANALYSIS/paired_analysis.py`，相关测试还绑定一个不存在的旧实验 request。平台不能在
这条链断裂时宣称“可跑正式实验”。

本任务的唯一目标是：**在不削弱任何门禁的前提下，恢复一条可持续测试、可复现、
fail-loud 的最小正式证据链，并给 Codex 提交可独立复核的候选实现。**

## 2. 已观测基线

2026-08-20 在上述基线执行：

```text
python3 -m pytest CODE/experiment_platform/tests CODE/tests -q
.......F........FFFF.......
5 failed, 22 passed, 3 subtests passed
```

失败分成两类：

1. `CODE/experiment_platform/tests/test_compile_scenario_identity.py` 因
   `ANALYSIS/paired_analysis.py` 缺失而失败。
2. `CODE/experiment_platform/tests/test_nonlearning_contract.py` 的 4 个用例因绑定
   不存在的 `EXPERIMENTS/EXP-20260715-VM-SMOKE-R04/request.json` 而失败。

这只是已知症状，不预设根因只有两个。Luna 必须先检查编译器、授权器、request schema、
receipt/analysis 合同和现有实验样例，再决定最小正确修复。

## 3. 职责与工作顺序

1. 先读 `AGENTS.md`、本任务书、`ANALYSIS/CURRENT-EXPERIMENT-READINESS.md`、
   `ANALYSIS/FINDINGS-REGISTRY.md`、`ANALYSIS/EXPERIMENT-PROGRAM.md`、
   `CODE/experiment_platform/AGENT_EXPERIMENT_PROTOCOL.md`。
2. 独立复现并分类 5 个基线失败，区分“产品缺陷、测试夹具缺失、过时合同、未实现功能”。
3. 追踪 `compile_experiment.py` 生成的 analysis request、RUNBOOK 命令和授权绑定，明确
   `paired_analysis.py` 的输入、输出 schema、哈希/身份绑定、失败语义和 claim 边界。
4. 先写或补强失败测试，再实现最小修复；不得把缺失检查改成跳过或弱断言。
5. 在仓库外临时目录完成至少一条小型端到端证据链演练；不得生成或提交正式实验结果。
6. 形成一个可审阅 commit，交给 Codex 做独立 diff、测试和语义终验。Luna 不得自行批准、
   push、开 PR、合并或部署。

## 4. 允许范围

允许读取整个仓库和旧平台只读索引；允许修改仅限：

- `ANALYSIS/paired_analysis.py`（若证据证明应恢复该正式入口）；
- `CODE/experiment_platform/**` 中与 compile/authorize/analysis 合同直接相关的实现与测试；
- `CODE/tests/**` 中正式证据链的集成测试；
- `EXPERIMENTS/templates/**` 或测试专用 fixture（只有当前 schema 无法用临时生成器表达时）；
- `ANALYSIS/FINDINGS-REGISTRY.md` 中 `R7-F1` 的候选处置记录，但只有完整验收后才能建议
  `fixed`，不得以本地自测冒充关闭。

优先用临时目录生成测试 request/receipt/manifest，避免重新引入已过时的整套历史实验目录。

## 5. 禁止事项

- 不修改 D1 PR #55、D2 PR #56、Q0 replay/tiny、奖励或 mask 代码；
- 不触碰任何其他 worktree、当前桌面主工作区的 dirty 文件或 VM；
- 不复制旧私有仓库代码进本公开仓库；旧库只能作为只读行为证据；
- 不删除、移动或覆盖已跟踪路径；若确实必要，停止并交 Codex 请求用户授权；
- 不改 CI workflow、ruleset、验收口径或 `.gitignore` 来制造绿色；
- 不伪造 receipt、结果、哈希、review、authorization 或 paper claim；
- 不把“脚本退出 0”当作链路完成，必须核对持久化产物和绑定关系；
- 不扩大到 D1/D2、Q0 算法、统计样本量或论文效果分析。

## 6. 必须交付的证据

候选提交至少包含：

1. 根因表：每个原始失败的类别、原因、影响和处置；
2. 实现 diff：最小、单主题、没有未声明路径；
3. `paired_analysis` 合同说明：输入、输出、哈希绑定、状态机、fail-loud 条件、明确不能推出的 claim；
4. 回归测试覆盖：正常链、缺文件、哈希漂移、run cohort 不一致、非自然结束/不合格 receipt、
   空配对或重复 run、输出不可覆盖或其他由代码合同要求的关键反例；
5. 真实命令与逐字统计：
   - `python3 -m pytest CODE/experiment_platform/tests CODE/tests -q`
   - `python3 -m pytest CODE/leo_sim/tests CODE/tests CODE/experiment_platform/tests -q`
   - 一条仓库外临时目录的 compile/authorize/analysis/claim 小型闭环命令与产物摘要；
6. `git status --short`、最终 commit SHA、`git diff origin/main...HEAD --stat`。

## 7. 完成条件与停止条件

只有以下条件全部满足，Luna 才能报告 `CANDIDATE_READY_FOR_CODEX_REVIEW`：

- 原 5 个失败均由真实修复关闭，且没有删除/跳过/放宽测试；
- 新增反例测试能证明哈希、cohort、receipt 和 claim 边界 fail-loud；
- 两组 pytest 全绿，数字如实报告；
- 临时端到端演练生成可重算的 analysis manifest/summary，所有身份与输入哈希可反溯；
- 分支只有 Luna 一个代码写入者，worktree clean，候选 commit 已形成；
- 没有把 synthetic/tiny 演练写成 VM 或正式论文证据。

遇到以下任一情况立即停止并报告 `BLOCKED`，不要自行扩权：

- 正确修复需要删除/移动已有路径、改 CI/ruleset、访问 VM 或凭据；
- 当前 schema 无法唯一确定分析语义，且两个合理方案会改变论文 claim；
- 需要 D1/D2/Q0 未合入行为才能闭环；
- 基线之外出现新的 blocking/major，且不能在本任务允许范围内独立修复。

## 8. 结果信封

最终回复必须包含：

```text
status: CANDIDATE_READY_FOR_CODEX_REVIEW | BLOCKED
branch: codex/luna-20260820-r7-formal-evidence-chain
base_sha: 63cc4a83c96bc51563d519764554bca4f333c0d0
head_sha: <40-char SHA or null>
changed_paths: [...]
tests: [{command, passed, failed, skipped, exit_code}]
e2e_evidence: <path/summary>
open_items: [...]
```

Luna 的信封只是候选证据；是否关闭 `R7-F1`、是否 push/PR/merge，由 Codex 独立终判。
