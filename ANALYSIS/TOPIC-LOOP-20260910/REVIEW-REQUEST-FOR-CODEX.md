# 【转审包】LEO-RL 路由选题循环：架构审查请求（2026-09-10）

## 0. 一段话背景（审阅者所需最小上下文）

主控代理（DSH 会话）按用户工作包搭建"LEO 卫星网络强化学习路由"的选题循环系统。架构已搭完并**试运行到"三路发现共产出 12 张候选卡"为止**。用户随后指令：架构先审、选题冻结——因此**合并裁决、近邻核查、深化、三角色审查、推荐、交付物全部未做**，本请求只审架构与过程，不审选题内容结论。
运行位置：仓库 fuguther/leo-direct-sim，worktree `/Users/lge/Desktop/leo-direct-sim/.worktrees/topic-loop-20260910`，分支 `agent/20260910-topic-loop`（base = origin/main 8a30409）。全部产物**未 commit、未 push**，仅在工作区。

## 1. 架构本身（层图）

```
L5 汇报层   ANALYSIS/TOPIC-LOOP-20260910/（交付物骨架）+ PR 证据合同
L4 选题层   入口合同 RESEARCH-ENTRIES.md（白/黑名单 + 阅读配额 + Undermind 限用途）
            ├ 三路生成器：A 场景推演 / B 文献行为 / C 方法迁移（全新隔离上下文，互不可见）
            ├ 候选台账 round/CANDIDATE-LEDGER.csv（pool.py 15 字段 schema，只添不改）
            ├ 合并工具 round/tools/{merge_sim.py, ledger_add.py}（只读复用 dedup/pool 真实现）
            └ 三角色审查模板 round/tools/REVIEW-ROLE-PROMPTS.md（建设者/近邻替代/证据）
            ※ Elo 已裁掉排序权（前次独立评审结论 + 工作包规定：不按票数/Elo/自评分推荐）
L3 文献层   SOURCES.csv(52) + notes/raw(41 篇已去倾向) + KNOWLEDGE-MAP + Zotero(44) + 本地PDF(15)
L3.5 防火墙 LITERATURE/README.md 四阶段：冷启动生成 → 外部碰撞 → 本地证据揭示 → 廉价 pilot 裁决
L1 治理层   AGENTS.md 硬规则 + hygiene/governance 两个机器检查器（本轮已跑）
L2 实验平台 leo_sim（本轮不动；防火墙阶段 3 未进入）
L0 运行时   DSH harness：主控 + 后台/前台 subagent + 独立 worktree
```

数据流（一段话）：三路生成器各拿同一份〔研究目标+资源边界+证据规范+入口白名单〕互相不可见，各产出 3-5 张卡到 staging → 主控按 (困难, 原因, 决策变化) 合并（相似度工具只出线索，判定在人）→ 与 16 张历史候选对账（复现必须携带新实质证据）→ 幸存卡入台账 → 每卡近邻核查 → 深化七步链 → 三角色审查+实质修订 → 交付。**当前只走到第一个箭头的产出，后续全部未启动。**

## 2. 哪些是真实跑过的（试运行证据，可复核）

| 环节 | 证据 | 结果 |
|---|---|---|
| 组件可用性 | dedup 实测：同文 1.0 / 两论文笔记 0.232 / 单词替换近重复 0.996；novelty 确定性查询抽取 OK；checks 六机械检查器可导入 | 通过；嵌入后端缺失→Dice 回退（限制已记录） |
| 检索通道 | Undermind search_papers 端到端命中（workspace 必传）；arXiv API 可达；Semantic Scholar 公共档 429（curl 取证 HTTP 429，无 API key） | 通过 / 受限替代已落地 |
| 证据链抽查 | PRIMAL Table I 在 PDF p9 定位成功（笔记预警的 std 异常 62.0±85.0ms 原文确认）；QARR 笔记断言"Dijkstra 理想条件时延最低"获原文摘要直接支持 | 2/2 定位成功（小样本，不外推为普遍可靠） |
| 三路生成合规 | A/B/C 各 4 卡落盘；自报无笔记论文占比 73%/55%/75%（合同≥40%）；Undermind 各≤3 次遵守；三份撞见声明齐全 | 通过 |
| 治理检查 | hygiene --phase start exit 0；governance 报 2 项 STALE_CURRENT（实验域文档，选题轮不依赖，记 UNVERIFIED 不沿旧结论执行） | 通过（附遗留） |
| push 授权 | gh auth（fuguther，repo scope）+ push --dry-run 成功 | 通过 |

## 3. 已知问题（按严重度，请重点攻击）

1. **入口污染（结构缺陷）**：KNOWLEDGE-MAP.md 在生成白名单（SUPPORTING），但其"外部碰撞补充(2026-09-03)"节夹带旧候选 A-D 的关系标注。三个生成器全部撞见、按规则声明跳过——防线未破但靠生成器自觉+主控对账兜底，不是结构保证。候选修法：a) 该节拆出白名单；b) 白名单移除 KNOWLEDGE-MAP；c) 接受+主控兜底。
2. **语义同族检测弱**：sentence-transformers 不可用，dedup 退化为字符 Dice（近重复可测、换名不换内容测不出）。兜底=主控按合并键人工判定。候选修法：装 embedding 后端或接受人工兜底。
3. **S2 公共档 429**：novelty.py 的 S2 判定链不可依赖；近邻核验主通道已切 Undermind/arXiv/本地全文（已实测可行）。
4. **LOZANO 版本歧义**：本地 PDF 为 DRAFT 版（奖励 eq.(5)-(8) 无投递终局项），笔记深读节却记"投递+50"——承重引用前必须锁版本（生成器已标注，主控未裁）。
5. **异模型审查通道不可用**：chatgpt_dispatch 插件输出契约错误（health 探测即失败，非登录问题）。当前方案=同模型三角色分离+用户转 Codex 终审。
6. **未验证项**：checks.py 六检查器只做过 import 测试未跑真卡；三角色审查流程未实测；交付物未动笔。

## 4. 需要用户/Codex 拍板的三个决策

① 架构整体是否可用，哪一层要改；
② 问题 1 的 KNOWLEDGE-MAP 入口处理方式（拆/移除/兜底）；
③ 已产出的 12 张卡：保留作继续跑的输入，还是作废重跑（重跑=重新派三路生成器）。

## 5. 文件索引（审阅者可直接读；路径均在 worktree 内）

- 架构审查材料：`/Users/lge/Desktop/leo-direct-sim/.worktrees/topic-loop-20260910/ARCHITECTURE-REVIEW.md`
- 主控台账（开工体检/暴露声明/组件核验/派发台账/合并协议/冻结指令）：`.../round/ROUND-LOG.md`
- 三路产出（选题内容已冻结，仅作管道 QC 材料）：`.../round/staging/path-A-scenario.md`（101 行）、`path-B-literature.md`（119 行）、`path-C-transfer.md`（76 行）
- 工具：`.../round/tools/merge_sim.py`、`ledger_add.py`、`REVIEW-ROLE-PROMPTS.md`
- 台账（仅表头）：`.../round/CANDIDATE-LEDGER.csv`
- 引用的外部合同（只读，属他人 checkout）：`/Users/lge/Desktop/leo-direct-sim/.worktrees/research-ops/LITERATURE/RESEARCH-ENTRIES.md`；origin/main 的 `LITERATURE/README.md`（四阶段防火墙）
- 相关前史（本项目此前对同类 harness 的独立评审，结论已部分采纳：Elo 降权）：`.../research-ops/out/research-ops/run-test-20260910/{ARCH-BRIEF,REPORT}.md` 与 `/Users/lge/Desktop/leo-direct-sim/.workbuddy/memory/2026-09-10.md`

## 6. 对审阅者的边界请求

- 只审架构与过程，**不要替主控做选题内容裁决**（合并/推荐冻结中）；**只读，不改动任何文件**。
- 若读取了 12 张卡内容，请按仓库防火墙惯例声明暴露范围（若你未来参与候选内容终审，需自评锚定风险）。
- 主控暴露声明：主控已接触旧候选台账与冷启动备忘录（见 ROUND-LOG §1），生成器提示词在其之前锁死，未含旧候选信息。

## 7. 验收方式（如何核实以上声明）

- 台账与日志为 markdown，直接读；`git -C /Users/lge/Desktop/leo-direct-sim/.worktrees/topic-loop-20260910 status` 应显示未提交新文件、分支 agent/20260910-topic-loop。
- 组件复测：`cd /Users/lge/Desktop/leo-direct-sim/.worktrees/research-ops && python3 -c "from scripts.topic_harness import dedup; print(dedup.dice_similarity('abc','abc'))"`（只读执行）。
- 生成器合规自报可在三份 path-*.md 文件头尾核对（阅读台账/撞见声明）。
