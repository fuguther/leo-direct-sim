# run2 交接包（供 4.1 新会话接手 / 供 Codex 审核参考）

> 用途：若需改用 `deepseek/deepseek-v4.1-flash` 做子代理，**必须新建会话**（本会话白名单已冻结，见下），本文件提供全部上下文，接手者可零背景启动。
> 证据：`@deepseek-ai/dsh-tool-subagent/lib/index.js:585-600` —— 仅 `freshSession` 时从 settings.yaml 读 allowedModels 并冻结进会话事件。

## 1. 工作目录与分支

- worktree：`/Users/lge/Desktop/leo-direct-sim/.worktrees/topic-loop-20260910`
- 分支：`agent/20260910-topic-loop`（最后一次成功 push 的 commit = `7958d82`；此后所有改动**未提交未推送**，原因见 §6）
- 唯一规则文件：`round/rules/EFFECTIVE-RULES-R2.md`（§2 白名单 v3、§8 流水线）

## 2. 用户已锁定的研究范围（本轮唯一主线）

**低轨卫星网络中，负载变化下强化学习路由如何保持良好的到达率与端到端时延。**
- 具体研究问题与改进方法**尚未确定**，本轮目标=形成一条有充分理由、能向老师讲清的研究主线。
- 旧 B3（窄负载带/阈值失标定/课程学习）恢复为**待检查假设**，不得作为生成前提；链路寿命方向**退出**本轮主线。

## 3. 输入链状态（P0 已完成）

- 生成器**只能**读：`LITERATURE/SOURCES.csv`、`round/knowledge/notes-neutral/*.md`、`round/knowledge/NEUTRAL-KNOWLEDGE-VIEW.md`、`LITERATURE/papers/*.pdf`、Zotero、Undermind search_papers(≤3)/arXiv/网页。
- `LITERATURE/notes/raw/**` 已列入黑名单（含 F0/F1 与旧候选倾向句）。
- notes-neutral 由 `round/tools/sanitize_notes.py` 从 raw 剥离生成；manifest=`round/knowledge/notes-neutral-manifest.json`。
- **语义抽查已完成**：`round/knowledge/P0-SEMANTIC-SPOTCHECK.md`（15 处隐含旧判断残留已定点清除；3 处承重事实已回补；含一次回补事故与回退记录）。
- 抽查证实：**关键词清零 ≠ 内容中立**——接手者不得仅凭残留扫描就认定笔记中立。

## 4. 本轮流水线（按 EFFECTIVE-RULES-R2 §8）

三路并行生成（A 整体强度 / B 热点与 OD 分布 / C 突发程度与速度）→ 初筛入账 → **独立历史碰撞审查**（五类裁决，含"旧判断是否仍成立"）→ 深化（≤3 卡，必答三问）→ 三角色审查（builder/neighbor/evidence）→ 主控整合与裁决 → 交付。

**三问（每张深入卡必答）**：
1. 现有方法在什么重要条件下为什么做不好？（具体方法+训练/部署条件+负载变化形式+影响到达率/时延的过程；区分原文观察/作者解释/自己推演/未检验假设；**论文没测≠做不好**）
2. 拟议改动针对什么原因？（先辨因再选法；给出一次具体决策或学习更新；说明何时不起作用）
3. 简单方法与成熟 RL 为何不能同样解决？（混合负载训练、在线微调、已有信息、规则路由、直接近邻，在信息/预算/条件对齐后比较；不许弱化基线）

**纪律**：三路是分工不是配额；允许合并/淘汰/空手；核心理由失败即停止维护该版本，不靠改名或补风险声明维持推荐；性能收益一律写"待验证假设"；本轮不训练、不仿真。

## 5. 交付五件套（`ANALYSIS/TOPIC-LOOP-20260910/run2/`）

1. `MAIN-REPORT.md` 一页主报告（最值得继续的问题，直答三问）
2. `PROPOSAL.md` 完整文稿（场景→现有不足→原因→针对性改动→最近邻差异→验证设计）
3. 机制图（Mermaid，能走通一次决策+一次学习更新）
4. `LITERATURE-GUIDE.md`（核心文献指引+承重原文位置）
5. `TRADEOFF-LOG.md`（取舍记录：比较过哪些实质不同问题、什么证据改变判断、为何推荐这条；独立备选如实提交）

## 6. 已知环境故障（交接时必须知晓）

- **git 不可用**：`/usr/bin/git` 报 `You have not agreed to the Xcode license agreements`；无备用 git 二进制。**未执行 sudo、未接受许可**（用户指示）。
  - 影响：`7958d82` 之后的所有改动（notes-neutral、P0 报告、run2 产物、dispatch 记录）**仅存于本地 worktree，未提交未推送**。
  - 待备份清单：`round/knowledge/notes-neutral/`、`round/knowledge/notes-neutral-manifest.json`、`round/knowledge/P0-SEMANTIC-SPOTCHECK.md`、`round/tools/{sanitize_notes,neutral_residual_fix1,neutral_residual_fix2,fix_chu,spotcheck_removed2,backfill_facts_min,revert_backfill}.py`、`round/rules/EFFECTIVE-RULES-R2.md`（白名单 v3）、`round/ROUND-LOG.md`（§13）、`round/dispatch/DISPATCH-RECORD.md`、`round/run2/**`。
- **子代理路线配额**：`Qwen/Qwen3.8-Flash` 与 `meta/muse-spark-1.3-contributor` 报 403 五小时用量上限；`deepseek-v4-flash` 可用但用户禁止；`z-ai/glm-5.3-flash` 可用（本会话在用）。

## 7. 新会话开工清单（4.1）

1. `cd /Users/lge/Desktop/leo-direct-sim/.worktrees/topic-loop-20260910`，读本文件与 `round/rules/EFFECTIVE-RULES-R2.md`；
2. 确认 `list_subagent_models` 返回含 `deepseek/deepseek-v4.1-flash`；
3. 用 `round/run2/staging/` 下已完成/未完成的产物判断是否需要重跑（若本会话 GLM 三路已产出，可直接续跑历史审查与深化，不必重生成）；
4. 生成器提示词模板见 `round/dispatch/DISPATCH-RECORD.md` 与本文件 §4；
5. 全程遵守：非 Pro 路线、Undermind 预算、不训练不仿真、停在"待 Codex 内容审核"。
