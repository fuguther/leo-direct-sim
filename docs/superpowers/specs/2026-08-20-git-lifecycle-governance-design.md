# Git 生命周期治理设计

日期：2026-08-20
适用仓库：`fuguther/leo-direct-sim`

## 1. 问题与证据

现有 `AGENTS.md` 已规定：从最新 `main` 开分支、一个分支一个主题、CI 绿后 squash merge、一个分支写入者唯一、并行任务使用独立 worktree。缺口不是缺少原则，而是缺少从本地工作到合并回收的显式状态机。

2026-08-20 本地只读盘点发现：

- Git 登记 37 个 worktree；
- 24 个本地分支的上游显示 `gone`，但相应 worktree 仍登记；
- 3 个 worktree 含未提交改动；
- 多个已远端删除的历史分支仍占用本地 worktree；
- `NOTES.md` 被要求由每个任务修改，容易成为并行 PR 的冲突热点。

以上只能证明本地生命周期没有闭合。`gone` 不自动等于“已安全合并”，在没有 PR 与 `main` 证据前不得删除。

## 2. 目标

1. 明确 commit、push、Draft PR、Ready、merge 各自含义，禁止把“已上传”误写成“可合并”。
2. 达到门禁的 PR 立即进入 auto-merge，不因等待批处理而长期悬挂。
3. 一个分支在整个生命周期内只有一个写入者；复核者只读。
4. 合并或放弃后及时回收 clean worktree，同时保护所有 dirty、未核实或可能含唯一提交的工作区。
5. 让 GitHub 成为代码版本真相源，但不把未跟踪文件、实验结果或本地脏改动误称为已备份。
6. 降低 `NOTES.md` 的并行写冲突和重复留痕。

## 3. 非目标

- 本轮不修改 GitHub ruleset、CI workflow、仓库可见性或权限。
- 本轮不自动删除任何 worktree、分支或用户文件。
- 本轮不合并 D1、D2、Q0 等承重分支；它们仍按各自 exact-SHA 复核门禁处理。
- 本轮不建立集中式锁服务或新的常驻后台进程。

## 4. 分支状态机

| 状态 | 含义 | 必须满足 | 允许动作 |
|---|---|---|---|
| `LOCAL-WIP` | 尚未形成远端检查点 | 单一写入者、独立 worktree | 编辑、测试、形成可解释 checkpoint |
| `DRAFT` | commit 已 push，GitHub 有远端备份，但不可合并 | Draft PR 写明 owner、base SHA、write set、当前 blocker | 继续实现、请求只读审阅 |
| `REVIEW` | 实现完成，正在核验证据 | diff 范围固定、测试证据齐、承重改动绑定 exact SHA | 复核、修正；任何承重修改使旧复核失效 |
| `READY` | 满足合并条件 | CI 绿、证据齐、必需独立复核通过、已同步最新 main、无未解决 blocker | 立即设置 auto-merge |
| `BLOCKED` | 当前不能进入 READY | PR 写明阻塞证据、责任人和恢复条件 | 修复、降回 Draft、关闭或建立续作 |
| `MERGED` | squash commit 已进入 main | 核验 PR merged、main SHA、工作区 clean | 记录必要状态、回收 worktree/本地分支 |
| `ABANDONED` | 明确不再继续 | 唯一提交已 push，PR/记录说明原因与替代项 | 关闭 PR；核验后再回收 |

状态转换原则：`push != READY`，`CI green != independent review`，`review approved != deployed`，`merged != VM receipt`。

## 5. 提交、上传与合并时机

- 有意义的最小工作单元完成后提交；切换任务、结束当天、请求复核或开始高风险改动前必须先形成可解释 checkpoint。
- 第一个有意义的 commit 当天 push，并建立 Draft PR。Draft PR 同时承担远端备份索引和写入者占用声明。
- 不完整 checkpoint 可使用 `chore(wip): ...`，但必须保持 fail-loud，且不能进入 READY。
- Ready 门禁全部满足后立即执行 `gh pr merge --auto --squash --delete-branch`，不等待与无关任务批量合并。
- 开 PR 后 24 小时无进展必须更新 blocker；72 小时无恢复路径则关闭、标记 abandoned 或建立明确续作。

## 6. 单一写入者与交接

- 一个任务对应一个 branch、一个 worktree、一个终身写入者。
- 其他 Agent 可以在不同 checkout 上只读审阅，但不能向生产分支提交。
- 需要换人时，原写入者先提交并 push，记录 exact SHA、测试、dirty 状态和 blocker，然后冻结原分支。
- 接手者从声明的 exact SHA 新建续作分支和新 PR；旧 PR 标明 superseded。禁止两名写入者先后共写同一分支。
- 新任务默认从最新 `origin/main` 创建。除显式记录依赖外，禁止从另一个未合并 feature 分支继续堆功能。

## 7. 同步与复核

- PR 进入 READY 前必须 fetch 并与最新 `origin/main` 对账；已发布分支禁止依赖 force-push 重写历史。
- 承重文件修改后的独立复核只对被审 exact full SHA 有效。任何承重行为修改都要求新 SHA 复核。
- 复核者不得成为该分支写入者；需要修复时由原 owner 改，或按交接规则建立新分支。

## 8. 合并后回收

- 回收前同时确认：PR 状态为 merged/closed、目标结果已进入 `origin/main`、worktree clean、没有未跟踪唯一文件。
- 任何一项未知时分类为 `ORPHAN-UNVERIFIED`，不得删除。
- dirty worktree 一律分类为 `DIRTY-PROTECT`，先报告文件和 owner，不 stash、不 reset、不覆盖。
- detached worktree 必须先证明只是验证 checkout；否则同样保留。

## 9. 留痕策略

- PR 正文保存任务级 owner、write set、测试、复核、blocker 和合并门禁，是任务证据主入口。
- `NOTES.md` 只维护当前平台状态和真正改变当前真相的合并结果，不要求所有并行分支都修改。
- 文档 PR 或纯历史整理不额外制造“为记录上一次合并而再开一次 PR”的无限链；PR 自身和 GitHub merge commit 已构成可核验回执。

## 10. 当前存量治理

先生成只读分类账，将现有 worktree 分成：`ACTIVE`、`DIRTY-PROTECT`、`MERGED-CLEANUP-CANDIDATE`、`ORPHAN-UNVERIFIED`、`DETACHED-VERIFY`。本轮只生成分类与证据，不执行删除。待远端 PR 和 main 归属逐项核实后，再把明确可回收路径逐条提交用户批准。
