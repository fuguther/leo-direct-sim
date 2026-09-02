# 论文选题去锚定与材料清理 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 删除会把候选题伪装成既定方向的成品和结论层，并建立“先独立选题、后揭示旧实验”的官方材料读取顺序。

**Architecture:** `AGENT-START-HERE.md` 负责按任务类型路由，`LITERATURE/README.md` 负责选题证据防火墙，三份 CURRENT 文档只报告当前边界而不生成论文题目。底层论文笔记、来源和实验工件继续保留；候选裁决、冻结说法和实验设计从 supporting 文档中移除。

**Tech Stack:** Markdown、JSON 文档治理登记、Git、仓库自带文档治理与工作区卫生检查脚本。

---

### Task 1: 建立中立的选题入口与证据防火墙

**Files:**
- Modify: `AGENT-START-HERE.md`
- Modify: `LITERATURE/README.md`

- [ ] **Step 1: 在文献合同中写入四阶段证据防火墙**

将 `LITERATURE/README.md` 扩展为选题与文献的当前合同，明确：冷启动问题生成、外部文献碰撞、本地证据揭示、廉价 Pilot 与裁决四阶段；旧实验只允许在第三阶段用于反证、边界和可行性判断；平台现成功能不得为候选题加分；证据不足时不强制推荐中心问题。

- [ ] **Step 2: 在统一入口中增加选题任务的条件路由**

修改 `AGENT-START-HERE.md` 的最短阅读顺序：论文选题任务在读取详细实验计划、历史结果和专题合同前，先读取 `LITERATURE/README.md` 并形成不含旧内部术语的冷启动候选；实验、实现和复核任务继续读取 CURRENT 文档与专题合同。

- [ ] **Step 3: 验证入口没有反向引用旧候选**

Run:

```bash
rg -n "证据防火墙|冷启动问题生成|本地证据揭示|不强制推荐" LITERATURE/README.md AGENT-START-HERE.md
rg -n "远端信息价值|状态陈旧|图模型收益来源|联合路由调度" LITERATURE/README.md AGENT-START-HERE.md
```

Expected: 第一条命令命中新合同；第二条命令无输出。

- [ ] **Step 4: 运行文档治理检查**

Run:

```bash
python3 scripts/check_document_governance.py --mode all --report /tmp/leo-selection-debias-task1.json
git diff --check
```

Expected: `0 selected errors, 0 warnings, 0 archive candidates`；`git diff --check` 退出码为 0。

- [ ] **Step 5: 提交入口重构**

```bash
git add AGENT-START-HERE.md LITERATURE/README.md
git commit -m "docs: 建立选题证据防火墙"
```

### Task 2: 撤销 CURRENT 文档的旧候选默认地位

**Files:**
- Modify: `ANALYSIS/CURRENT-EXPERIMENT-READINESS.md`
- Modify: `ANALYSIS/EXPERIMENT-PROGRAM.md`
- Modify: `ANALYSIS/PLATFORM-CAPABILITY-LEDGER.md`
- Modify: `ANALYSIS/DOCUMENT-STATUS.json`

- [ ] **Step 1: 改写当前就绪状态的选题边界**

在 `ANALYSIS/CURRENT-EXPERIMENT-READINESS.md` 顶部 CURRENT 节明确：中心问题未冻结；旧候选、历史实验解释和平台能力不得用于生成或排序候选；选题完成前实验矩阵继续暂停。

- [ ] **Step 2: 改写实验总计划的当前裁决**

在 `ANALYSIS/EXPERIMENT-PROGRAM.md` 顶部 CURRENT 节删除旧四候选清单，只保留“先形成可证伪问题、再决定最小实验合同”的门禁，并把 `ACCESS_LIMITED` 等旧结果限定为第三阶段反证材料。

- [ ] **Step 3: 改写平台能力账本的用途边界**

在 `ANALYSIS/PLATFORM-CAPABILITY-LEDGER.md` 顶部 CURRENT 节明确：平台能力只能在候选形成后判断可攻击性、成本和测量能力，不能决定问题的重要性、新颖性或优先级。

- [ ] **Step 4: 同步文档治理登记**

更新 `ANALYSIS/DOCUMENT-STATUS.json` 的 `updated_at` 为 `2026-09-03`，并把 `LITERATURE/README.md` 的 purpose 扩展为文献核验与选题证据防火墙；保持 `KNOWLEDGE-MAP` 和 `notes` 为 `SUPPORTING / may_direct_current_work=false`。

- [ ] **Step 5: 验证 CURRENT 顶部不再限定旧候选**

Run:

```bash
sed -n '1,15p' ANALYSIS/CURRENT-EXPERIMENT-READINESS.md
sed -n '1,15p' ANALYSIS/EXPERIMENT-PROGRAM.md
sed -n '1,15p' ANALYSIS/PLATFORM-CAPABILITY-LEDGER.md
rg -n "远端信息价值、状态陈旧、图模型收益来源、是否扩大到联合路由调度" ANALYSIS/CURRENT-EXPERIMENT-READINESS.md ANALYSIS/EXPERIMENT-PROGRAM.md ANALYSIS/PLATFORM-CAPABILITY-LEDGER.md
```

Expected: 三份顶部均声明问题未冻结和材料揭示边界；最后一条命令无输出。

- [ ] **Step 6: 运行治理检查并提交**

```bash
python3 scripts/check_document_governance.py --mode all --report /tmp/leo-selection-debias-task2.json
git diff --check
git add ANALYSIS/CURRENT-EXPERIMENT-READINESS.md ANALYSIS/EXPERIMENT-PROGRAM.md ANALYSIS/PLATFORM-CAPABILITY-LEDGER.md ANALYSIS/DOCUMENT-STATUS.json
git commit -m "docs: 撤销旧候选的当前默认地位"
```

Expected: 治理检查零错误、零警告；提交只包含四份声明文件。

### Task 3: 删除冻结成品并把知识地图还原为证据地图

**Files:**
- Delete: `LITERATURE/notes/ONE-PAGE-OPENING-v0.1.md`
- Delete: `LITERATURE/notes/ONE-PAGE-OPENING-v1.0.md`
- Modify: `LITERATURE/KNOWLEDGE-MAP.md`
- Modify: `LITERATURE/notes/README.md`
- Modify: `LITERATURE/notes/00-READING-QUEUE.md`

- [ ] **Step 1: 删除两份伪装成冻结结论的开题页**

使用补丁删除两份 `ONE-PAGE-OPENING` 文件。删除已由用户按精确路径批准，内容仍可由 Git 历史恢复。

- [ ] **Step 2: 把知识地图裁剪为证据层**

保留 `LITERATURE/KNOWLEDGE-MAP.md` 的 Claim Map、Assumption Map、Evidence Map、空白点检索证据和逐篇深读对账表；删除 Puzzle/RQ 生成、9 关、F1/F2/F3 推荐、冻结说法、竞争假设和实验设计。文件顶部增加 `SUPPORTING` 边界：不得推荐或冻结中心问题。

- [ ] **Step 3: 去除阅读规则的第一遍实验映射要求**

修改 `LITERATURE/notes/README.md`：第一遍只记录论文自己的问题、主张、机制、证据、假设、边界和张力；“与本项目实验的关系”只能在独立候选形成后的第二遍对账中添加，并须区分实验观测与历史解释。

- [ ] **Step 4: 标注阅读队列的抽样偏差**

修改 `LITERATURE/notes/00-READING-QUEUE.md`：说明它是围绕旧问题形成的种子语料，不是系统综述总体，也不能证明领域空白；删除变更日志中“中心问题拟冻结”和“空白点关闭”的裁决，只保留阅读数量与状态。

- [ ] **Step 5: 验证删除与残留**

Run:

```bash
test ! -e LITERATURE/notes/ONE-PAGE-OPENING-v0.1.md
test ! -e LITERATURE/notes/ONE-PAGE-OPENING-v1.0.md
rg -n "拟冻结|建议冻结|F3×F2|推荐与裁决|扰动合同|T1 判别实验|中心问题拟冻结|空白点.*关闭" LITERATURE/KNOWLEDGE-MAP.md LITERATURE/notes/README.md LITERATURE/notes/00-READING-QUEUE.md
rg -n "Claim Map|Assumption Map|Evidence Map|深读批摘要与对账表|SUPPORTING" LITERATURE/KNOWLEDGE-MAP.md
```

Expected: 两个 `test` 均成功；第一条 `rg` 无输出；第二条 `rg` 命中保留的证据层。

- [ ] **Step 6: 运行治理检查并提交**

```bash
python3 scripts/check_document_governance.py --mode all --report /tmp/leo-selection-debias-task3.json
git diff --check
git add -A LITERATURE ANALYSIS/DOCUMENT-STATUS.json
git commit -m "docs: 删除选题冻结成品并保留证据层"
```

Expected: 治理检查零错误、零警告；提交包含两项删除和三份 supporting 文档修改。

### Task 4: 全量验收与远端交接

**Files:**
- Verify only: all files changed since `987195135ce099fb4c56304b9e42056e3bb2a24a`

- [ ] **Step 1: 运行完整文档与工作区检查**

```bash
python3 scripts/check_workspace_hygiene.py --phase start
python3 scripts/check_document_governance.py --mode all --report /tmp/leo-selection-debias-final.json
git diff --check 987195135ce099fb4c56304b9e42056e3bb2a24a..HEAD
```

Expected: worktree 为 `CLEAN [CONTINUE]`；治理检查零错误、零警告；diff check 退出码为 0。

- [ ] **Step 2: 核对精确 write set 和禁区**

```bash
git diff --name-status 987195135ce099fb4c56304b9e42056e3bb2a24a..HEAD
git diff --stat 987195135ce099fb4c56304b9e42056e3bb2a24a..HEAD
git diff 987195135ce099fb4c56304b9e42056e3bb2a24a..HEAD -- AGENTS.md CODE EXPERIMENTS LITERATURE/notes/raw LITERATURE/SOURCES.csv
```

Expected: write set 只包含规格、计划和设计声明的治理/文献文件；最后一条命令无输出。

- [ ] **Step 3: 核对内容门禁**

```bash
rg -n "先.*旧实验|本地证据揭示|不得.*生成.*候选|不强制推荐" AGENT-START-HERE.md LITERATURE/README.md ANALYSIS/CURRENT-EXPERIMENT-READINESS.md ANALYSIS/EXPERIMENT-PROGRAM.md ANALYSIS/PLATFORM-CAPABILITY-LEDGER.md
rg -n "建议冻结|只差.*拍板|F3×F2|真实扰动合同下的韧性裁决" LITERATURE AGENT-START-HERE.md ANALYSIS/CURRENT-EXPERIMENT-READINESS.md ANALYSIS/EXPERIMENT-PROGRAM.md ANALYSIS/PLATFORM-CAPABILITY-LEDGER.md
```

Expected: 第一条命中防火墙；第二条无输出。

- [ ] **Step 4: 推送续作分支并建立新 PR**

```bash
git push -u origin codex/20260903-selection-debias
```

使用 `.github/pull_request_template.md` 创建新 Draft PR，声明旧 PR #194 被本续作替代、base/head SHA、精确删除路径、未运行实验、治理检查结果和恢复方式。新 PR 创建成功后，在旧 PR #194 留下 superseded 说明并关闭旧 PR；不 force-push、不修改旧分支。

- [ ] **Step 5: 等待 CI 并按七态报告**

读取新 PR 的检查状态。只有 CI 绿、diff 与声明一致、证据齐全且无 blocker 时才从 REVIEW 进入 READY；否则保持 Draft/BLOCKED，并记录原始错误和恢复条件。
