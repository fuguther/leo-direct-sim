# AGENTS.md（新基地）

本仓库是 LEO 直连仿真平台（leo_sim V2）的干净基线，2026-08-16 从旧科研工作区分拆建立。
旧仓库（私有 `fuguther/leo-research-workspace`）保留全部历史与旧平台代码，本库不带 git 历史。

## 硬事实

1. 科研结论必须可复现、可反驳、可核验；未经当前平台回执验证的结论不得进入论文。
2. 实验结果永不入库：`CODE/Results/`、`leo_sim_out/`、`out/` 一律 gitignore。
3. 正式实验只能走：编译 → 审阅 → 授权 → `CODE/scripts/remote/run-remote.sh` → 自然结束回执 → 分析重算。
4. 失败必须 fail-loud：配置解析、trace、信息条件或 receipt 不符时阻止运行，不允许静默回退。
5. 删除、移动、覆盖任何已跟踪路径前必须逐条列出并等用户批准。
6. 机器私密配置（`remote.env` 等）不入库，只入库 `.template`。

## Git / GitHub 工作流

**总原则：`main` 永远绿、永远可部署。GitHub 是已提交代码的唯一版本真相源；`push` 只表示远端已有 checkpoint，不表示可以合并。所有改动经 PR + CI 绿合入，远端 ruleset 拒绝直推 `main`。**

### 生命周期

1. **七态状态机**：分支必须处于 `LOCAL-WIP → DRAFT → REVIEW → READY → MERGED` 之一；无法推进时标 `BLOCKED`，明确放弃时标 `ABANDONED`。`CI green != independent review`、`review approved != merged`、`merged != deployed/receipt`，禁止跨门声明。
2. **LOCAL-WIP / DRAFT**：形成第一个有意义的 commit 后，当天 push 并开 Draft PR。Draft PR 是远端备份索引和写入者占用声明，不可合并；必须写 owner、base/head SHA、预计 write set、当前 blocker。未跟踪文件、未提交改动和被 gitignore 的实验结果不因 `push` 自动获得备份。
3. **REVIEW / READY**：实现和测试完成后进入 REVIEW；承重改动的独立复核仅对被审 exact full SHA 有效，任何承重行为修改都会使旧 verdict 失效。只有 CI 绿、PR 证据齐、必需复核通过、已与最新 `origin/main` 对账且无 blocker 时才能标 READY。
4. **及时合并**：PR 达到 READY 后立即执行 `gh pr merge --auto --squash --delete-branch`，不等待与无关任务批量合并。BLOCKED/DRAFT 不得因“先备份”或“CI 恰好绿”而合并。

### 开工、所有权与交接

5. **开工**：先 `git fetch origin`、`git status`、`git worktree list`；发现目标 worktree 非 clean 或已有 owner 时停下报告，不 stash/reset/覆盖。新任务从最新 `origin/main` 切 `<agent>/<yyyymmdd>-<主题>`，一个任务一个分支一个 worktree；除 PR 明示依赖外，禁止从未合并 feature 分支继续堆功能。
6. **终身单写入者**：一个分支在整个生命周期内只有一个写入者。其他 Agent 只能在不同 checkout 上只读复核，禁止向生产者分支或 PR 追加提交。需要换人时，原 owner 先提交并 push，记录 exact SHA、测试、dirty 状态和 blocker，然后冻结旧分支；接手者从该 SHA 新建续作分支和新 PR，旧 PR 标 `superseded`。禁止两人先后共写同一分支。
7. **提交时机**：完成可独立解释的最小工作单元就提交；切换任务、结束当天、请求复核、开始高风险修改前必须形成 checkpoint。前缀用 `feat|fix|docs|exp|chore` + 中文简述；一个 commit 一个主题，代码/数据/文档和重构/修 bug 不混。确需保存未完成工作可用 `chore(wip): ...` 推到 Draft PR，但必须 fail-loud，不能进入 READY。

### PR、授权与留痕

8. **PR 证据合同**：使用 `.github/pull_request_template.md`；至少写清状态、owner、base/head SHA、write set、改了什么、为什么、真实 passed/failed/skipped、独立复核、blocker/恢复条件。禁止自夸式描述和无证据的完成声明。
9. **长期授权（2026-08-16）**：同时满足 CI 绿、PR 证据齐、diff 只含声明主题、不碰删除/移动/覆盖已跟踪路径时，Agent 可自主走完 commit → push → PR → auto-merge。**仍需当场授权**：删除/移动路径、改 ruleset/仓库设置、force-push、改可见性、建删 tag、发 release。
10. **NOTES 降冲突**：PR 正文和 GitHub merge 记录是任务级证据主入口。`NOTES.md` 只在合并确实改变“当前平台状态/下一步/风险”时更新，不要求每个并行分支都写，不为补记上一 PR 再制造无限留痕 PR。

### 超时与回收

11. **超时处理**：PR 24 小时无实质进展必须更新 blocker 和恢复条件；72 小时无恢复路径则关闭、标 ABANDONED，或按交接规则新建续作。分支默认寿命 < 3 天；超过时不能静默悬挂。
12. **合并后回收**：只有同时确认 PR 已 merged/closed、结果已进入 `origin/main`、worktree clean、无未跟踪唯一文件时，才可回收 worktree/本地分支。dirty 一律 `DIRTY-PROTECT`；PR/main 归属未知一律 `ORPHAN-UNVERIFIED`；detached checkout 未证明纯验证用途前不得删除。删除 worktree 或本地路径仍受“逐条列出、用户批准”约束。

### 仓库与实验边界

13. **禁止入库**：`CODE/Results/`、`leo_sim_out/`、`out/`、`remote.env`、`.env`、`__pycache__/`、`.DS_Store`（.gitignore 已配；发现漏网先补 gitignore 再提交）。GitHub 备份代码，不替代 VM 原始实验数据和回执保存链。
14. **VM 部署**：只允许 `main` 上的 clean commit，经 `CODE/scripts/remote/push-remote.sh` 执行；跑实验前必须已部署，部署后记录回执 SHA。
15. **矛盾处理**：发现历史/文档/代码互相矛盾时，并列报告出处与影响，禁止静默融合或擅自覆盖。
16. **旧平台参照**：旧平台（Gateway 汇聚）在 `/Users/lge/Desktop/LEO-Research-Workspace`（私有 `fuguther/leo-research-workspace`），只读引用、禁止修改、**禁止复制进本库**（无 LICENSE 第三方仓库的衍生作品，本库公开）。先查 `ANALYSIS/PLATFORM-DOCUMENTATION/02-kimi-platform-spec.md` 行号索引与不一致清单，迁移取舍以 `ANALYSIS/MIGRATION-BACKLOG-20260816.md` 为准。

## 防失控护栏

17. **禁止刷提交**：禁止空 commit；CI 红之后，每次 push 必须附带新的诊断或修复，无新信息的重推禁止；连续 2 次修复仍红，转 BLOCKED，在 PR 写明错误原文、定位和假设。
18. **禁止削弱检查**：CI 红时只能修代码缺陷或测试自身的真实缺陷；禁止删测试、放宽断言、注释检查或改 workflow 让它“看起来绿”。确需调整测试门槛时，单独 PR 并在标题明示“测试调整”。
19. **main 红优先**：发现 main 红（无论谁造成），优先修 main，不在红 main 上继续堆新 PR。
20. **承重改动仲裁**：涉及 `CODE/leo_sim/kernel.py`、`receipt.py`、`governance.py`、`learning.py` 或 `experiment_platform/` 授权链时，生产者不得自批，必须由不同模型冷启动复核或 Codex 独立冷启动自审；复核不可用则 PR 保持 BLOCKED/待复核。

## 三端职责（本地 / GitHub / VM，单向链）

继承旧调研《三端工作流与边界》（2026-06-26，存旧库）：**本地**做设计/开发/分析，不当唯一备份；**GitHub** 是唯一代码版本真相源（本地与远端不得漂移，全分支每日 push）；**VM** 只做受控执行与生产原始证据，不长期维护代码、不手工改、不跑未提交代码。从论文 claim 必须能反溯：本地分析 → GitHub commit → VM 原始实验。

## 渐进式验证协议

- 任务拆成可独立验收的步骤；每步完成以测试/回执/diff 范围为证据，不以「能跑」「看起来对」代替。
- 行为改动先记录旧版数值，再在新版重跑同一检查（新旧对照）。
- 禁止把「import 成功」「退出码 0」当作完成证据。

## 当前状态

- 见 `NOTES.md`。平台来源与谱系见 `README.md`。
