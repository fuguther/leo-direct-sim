# Git Lifecycle Governance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 leo-direct-sim 的提交、远端备份、单写入者、复核、及时合并和 worktree 回收规则变成一条无歧义的生命周期，并盘点当前存量而不删除用户数据。

**Architecture:** `AGENTS.md` 是强制规则唯一真相源；`.github/pull_request_template.md` 把 owner/state/write set/evidence 变成每个 PR 的操作界面；一份带日期的 `ANALYSIS/GIT-WORKTREE-RECONCILIATION-20260820.md` 保存当前只读审计快照。规则变更与存量删除严格分离。

**Tech Stack:** Git、GitHub PR、Markdown、shell 只读审计命令、pytest。

---

### Task 1: 固化批准设计

**Files:**
- Create: `docs/superpowers/specs/2026-08-20-git-lifecycle-governance-design.md`
- Create: `docs/superpowers/plans/2026-08-20-git-lifecycle-governance.md`

- [ ] **Step 1: 检查设计覆盖**

核对设计必须包含：状态机、commit/push/merge 区分、单一写入者、exact-SHA 复核、stale PR、合并后回收、NOTES 降冲突、存量不自动删除。

- [ ] **Step 2: 扫描占位符和矛盾**

Run: `rg -n 'TBD|TODO|待补|以后再写' docs/superpowers/specs/2026-08-20-git-lifecycle-governance-design.md docs/superpowers/plans/2026-08-20-git-lifecycle-governance.md`

Expected: 只命中本检查命令自身这一行；除此之外无占位符。

- [ ] **Step 3: 提交设计与计划**

```bash
git add docs/superpowers/specs/2026-08-20-git-lifecycle-governance-design.md docs/superpowers/plans/2026-08-20-git-lifecycle-governance.md
git commit -m "docs: 设计 Git 生命周期治理状态机"
```

### Task 2: 更新强制规则与 PR 操作界面

**Files:**
- Modify: `AGENTS.md`
- Create: `.github/pull_request_template.md`

- [ ] **Step 1: 重写 Git/GitHub 工作流段**

在 `AGENTS.md` 中保留现有 main、CI、VM、删除授权和科研门禁；加入七态生命周期、Draft/Ready 语义、24/72 小时规则、禁止 feature stacking、合并后回收、NOTES 只记当前真相。

- [ ] **Step 2: 收紧多 Agent 仲裁**

明确分支终身单写入者；复核只读；交接时冻结旧分支，接手者从 exact SHA 新建续作分支和新 PR。

- [ ] **Step 3: 创建 PR 模板**

模板必须包含以下字段：

```markdown
## 生命周期
- 状态：DRAFT
- Owner：
- Base SHA：
- Head SHA：
- Write set：
- Supersedes：无

## 改动与原因
## 验证证据
## 独立复核
## Blocker / 恢复条件
## READY 检查
```

- [ ] **Step 4: 静态验证规则存在**

Run: `rg -n 'LOCAL-WIP|DRAFT|REVIEW|READY|BLOCKED|MERGED|ABANDONED|终身写入者|24 小时|72 小时|origin/main|NOTES.md' AGENTS.md .github/pull_request_template.md`

Expected: 每个关键状态和门禁至少命中一次。

### Task 3: 生成当前 worktree 分类账

**Files:**
- Create: `ANALYSIS/GIT-WORKTREE-RECONCILIATION-20260820.md`

- [ ] **Step 1: 采集本地事实**

Run: `git worktree list --porcelain`、`git branch -vv`、逐 worktree `git status --porcelain`、`git for-each-ref`。

Expected: 记录 worktree path、branch/detached、HEAD、dirty count、upstream tracking。

- [ ] **Step 2: 采集 GitHub PR 事实**

Run: `gh pr list --state all --limit 200 --json number,state,isDraft,headRefName,baseRefName,headRefOid,mergedAt,closedAt,url,reviewDecision,mergeStateStatus`

Expected: 官方仓库返回 JSON；若网络或授权失败，在审计表中标 `REMOTE-UNVERIFIED`，不得推断。

- [ ] **Step 3: 分类但不删除**

对每个 worktree 标记 `ACTIVE`、`DIRTY-PROTECT`、`MERGED-CLEANUP-CANDIDATE`、`ORPHAN-UNVERIFIED` 或 `DETACHED-VERIFY`，并为候选写出证据和下一动作。不得运行 `git worktree remove`、`git branch -d/-D`、`rm`。

- [ ] **Step 4: 自查数量守恒**

审计表行数必须与 `git worktree list --porcelain | rg '^worktree ' | wc -l` 一致；所有 dirty worktree 必须是 `DIRTY-PROTECT`。

### Task 4: 验证、提交与合并

**Files:**
- Modify: `NOTES.md` only if this merge changes current governance truth

- [ ] **Step 1: 文档静态检查**

Run: `git diff --check`

Expected: 退出码 0，无 whitespace error。

- [ ] **Step 2: 全量回归**

Run: `python3 -m pytest -q`

Expected: 当前 main 基线测试全部通过；若数量变化，记录真实 passed/failed/skipped。

- [ ] **Step 3: 检查 diff 范围**

Run: `git status --short` 和 `git diff --stat origin/main...HEAD`

Expected: 只包含治理设计、计划、`AGENTS.md`、PR 模板、worktree 审计及必要的精简 NOTES 状态行。

- [ ] **Step 4: 提交并 push**

```bash
git add AGENTS.md .github/pull_request_template.md ANALYSIS/GIT-WORKTREE-RECONCILIATION-20260820.md NOTES.md
git commit -m "docs: 闭合 Git 分支提交合并与回收规则"
git push -u origin codex/20260820-git-lifecycle-governance
```

- [ ] **Step 5: 开 PR 并按 READY 门合并**

创建 PR，填写 owner/base/head/write set/测试/复核/blocker。CI 绿且 diff 范围正确后执行：

```bash
gh pr merge --auto --squash --delete-branch
```

### Task 5: 存量回收的独立批准门

**Files:**
- Read: `ANALYSIS/GIT-WORKTREE-RECONCILIATION-20260820.md`

- [ ] **Step 1: 列出精确候选路径**

只列 `MERGED-CLEANUP-CANDIDATE`，逐项包含 path、branch、HEAD、PR、clean 证据。

- [ ] **Step 2: 请求删除批准**

在执行任何 worktree/branch 删除前，把候选清单交给用户。`DIRTY-PROTECT`、`ACTIVE`、`ORPHAN-UNVERIFIED`、`DETACHED-VERIFY` 不进入删除清单。
