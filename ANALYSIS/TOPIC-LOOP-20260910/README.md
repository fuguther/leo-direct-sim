# 选题循环工作包：LEO 卫星网络强化学习路由（2026-09-10）

> **状态：正式选题循环 run1 完成——推荐候选 ×2（L1 链路剩余寿命 / B3 负载带塌陷窗）+ 条件保留 ×1（F1 新鲜度家族），待 Codex 内容审核。** 入口见下。
> 分支 agent/20260910-topic-loop（base: origin/main 8a30409）。本轮不启动训练/仿真。

## 交付物（完成后在此索引）

1. `AUDIT-SUMMARY.md` —— 两页审核摘要（实际完成/推荐候选三问直答/价值依据/判断改变点/最大未决/消耗与限制/路径索引）
2. `PROPOSAL.md` —— 研究方案正文（问题/动机/现状/原因/具体RL改进/近邻与简单替代/验证设计/已有基础与风险 + 机制图）
3. `LITERATURE-GUIDE.md` —— 核心文献导读（先读哪几篇/哪部分/支持或挑战什么/核验深度）
4. `PROCESS-APPENDIX.md` —— 过程附件（候选来源与演变/审查处置/证据位置/工具验收）

## 过程与证据目录

- `round/ROUND-LOG.md` —— 主控台账（开工体检/暴露声明/组件核验/派发台账/合并协议/决策记录）
- `round/CANDIDATE-LEDGER.csv` —— 候选台账（pool.py 15 字段 schema，只添不改）
- `round/staging/path-{A,B,C}-*.md` —— 三路生成器原始产出（未修订，审计用）
- `round/tools/merge_sim.py` —— 合并辅助工具（dedup.py 只读复用）

## 依据与边界

- 入口合同：`LITERATURE/RESEARCH-ENTRIES.md`（research-ops worktree，2026-09-10）
- 证据防火墙：`LITERATURE/README.md`（main）四阶段
- 主控暴露声明与旧候选对账记录：见 ROUND-LOG §1/§6