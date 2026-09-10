# 选题循环架构审查材料（v1，2026-09-10）

> **状态：选题流程已按用户指令冻结。** 三路发现已产出 12 张卡（试运行证据），合并裁决/深化/审查/推荐一律未做，等你审完架构再定。
> 位置：worktree `agent/20260910-topic-loop`（base=origin/main 8a30409），本文件与全部组件在该 worktree 内。

## 一、架构分层（复用 research-ops 已有层 + 本轮补齐件）

```
L5 汇报层   ANALYSIS/TOPIC-LOOP-20260910/（交付物骨架已建）+ PR 证据合同
L4 选题层   入口合同 RESEARCH-ENTRIES.md（白名单/黑名单/阅读配额/Undermind限用途）
            ├ 三路生成器（A场景推演/B文献行为/C方法迁移，隔离上下文）
            ├ 候选台账 round/CANDIDATE-LEDGER.csv（pool.py 15字段schema，只添不改）
            ├ 合并工具 round/tools/{merge_sim.py,ledger_add.py}（只读复用 dedup/pool 真实现）
            └ 三角色审查模板 round/tools/REVIEW-ROLE-PROMPTS.md（建设者/近邻替代/证据）
            ※ Elo 已裁掉排序权（workbuddy 评审结论 + 工作包规定：不按票数/Elo推荐）
L3 文献层   SOURCES.csv(52) + notes/raw(41篇已去倾向) + KNOWLEDGE-MAP + Zotero(44) + 本地PDF(15)
L3.5 防火墙 LITERATURE/README.md 四阶段：冷启动生成→外部碰撞→本地证据揭示→廉价pilot裁决
L2 实验平台 leo_sim（本轮不动；阶段3未进入）
L1 治理层   AGENTS.md 硬规则 + hygiene/governance 检查器（已跑，2项STALE_CURRENT记录在案）
L0 运行时   DSH harness：主控(本会话) + 后台/前台 subagent + worktree 隔离
```

## 二、本轮数据流（一段话说清）

三路生成器各拿同一份"研究目标+资源边界+证据规范+入口白名单"，互相不可见，各自产出 3-5 张卡到
`round/staging/path-{A,B,C}-*.md` → 主控按 (困难,原因,决策变化) 合并（工具只出相似度线索，判定在人）
→ 与 16 张历史候选对账（复现须带新证据）→ 幸存卡进台账 → 每卡近邻核查 → 深化(7步链) →
三角色审查+实质修订 → 交付物。**当前执行到第一步的产出，后面的全部未启动。**

## 三、架构试运行证据（真实跑过的部分）

| 环节 | 证据 | 结果 |
|---|---|---|
| 组件可用性 | dedup实测 dice=1.0/两论文0.232/近重复0.996；novelty查询抽取OK；checks六检查器可导入 | 通过（嵌入后端缺失→Dice回退，限制已记录） |
| 检索通道 | Undermind search_papers 端到端命中；arXiv API；S2 公共档 429（curl 取证） | 通过/受限替代已落 |
| 证据链抽查 | PRIMAL表I p9 定位成功（std异常 62.0±85.0 原文确认）；QARR 笔记断言获摘要直接支持 | 2/2 定位成功（小样本，不外推） |
| 三路生成 | A/B/C 各4卡落盘；三份合规自报：无笔记论文占比 55%/73%/75%（≥40%达标）、Undermind 限额遵守、撞见声明×3 | 通过 |
| 防火墙 | 生成器提示词锁死黑名单；三份撞见声明均"跳过未采信"；主控暴露声明在 ROUND-LOG §1 | 运行中（见问题#1） |

## 四、已知问题（按严重度排序，请重点审）

1. **KNOWLEDGE-MAP.md 入口污染（设计缺陷）**：入口合同把它列入生成白名单（SUPPORTING），但其"外部碰撞补充(2026-09-03)"一节夹带旧候选A-D的关系标注。三个生成器全部撞见并按规则声明跳过——防线没破，但靠的是生成器自觉+主控去重，不是结构保证。可选修法：a) 把该节拆出白名单文件；b) 白名单移除 KNOWLEDGE-MAP；c) 接受现状+主控对账兜底。
2. **语义同族检测弱**：sentence-transformers 不可用，dedup 退化为字符 Dice（近重复 0.996 可测，换名不换内容测不出）。兜底=主控人工按合并键判定。可选修法：装 sentence-transformers，或接受人工兜底。
3. **S2 公共档 429**：novelty.py 的 S2 判定链不可依赖，近邻核验改走 Undermind/arXiv/本地全文，已实测可行。
4. **LOZANO 版本歧义**：本地 PDF 是 DRAFT 版（奖励 eq.(5)-(8) 无投递终局项），而笔记深读节记录"投递+50"——承重引用前必须锁版本（生成器已标注）。
5. **异模型审查通道不可用**：chatgpt_dispatch 插件输出契约错误（health 探测失败，非登录问题）。当前方案=同模型三角色分离+你转 Codex 终审。
6. **未验证项**：checks.py 六机械检查器只做过 import 测试，未在真卡上跑过；三角色审查流程未实测。

## 五、冻结清单（等你裁决）

- 已产出未处理：12 张卡在 `round/staging/path-{A,B,C}-*.md`（C2 是"先例占位如实弃卡"的检验记录）。
- 未做：合并入账、旧候选对账落账、近邻核查、深化、三角色审查、推荐、四份交付物。
- 请你拍板：
  ① 架构整体行不行，哪层要改？
  ② 问题#1 的 KNOWLEDGE-MAP 入口怎么处理？
  ③ 已产出的 12 张卡：保留作输入继续跑，还是作废重跑（重跑=重新派三路生成器）？

## 六、关键文件索引

- 主控台账（体检/暴露声明/组件核验/派发/合并协议）：`round/ROUND-LOG.md`
- 三路产出：`round/staging/path-A-scenario.md` / `path-B-literature.md` / `path-C-transfer.md`
- 工具：`round/tools/{merge_sim.py, ledger_add.py, REVIEW-ROLE-PROMPTS.md}`
- 入口合同（research-ops worktree，只读引用）：`.worktrees/research-ops/LITERATURE/RESEARCH-ENTRIES.md`
- 防火墙合同：`LITERATURE/README.md`（origin/main 版）
