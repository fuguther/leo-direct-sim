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

**总原则：`main` 永远绿、永远可部署。一切改动经 PR + CI 绿合入；远端 ruleset 硬执行（直推 main 会被拒），本节是行为细则。**

1. **开工**：先 `git status`，非 clean 先处置（发现他人未提交改动：停下报告，不擅自处理）；从最新 main 切 `<agent>/<yyyymmdd>-<主题>` 分支（如 `codex/20260816-fix-reward`）。一个分支一件事，寿命 < 3 天。
2. **提交**：类型前缀 `feat|fix|docs|exp|chore` + 中文简述；一个 commit 一个主题（代码、数据、文档不混；重构与修 bug 不混）；正文附证据（测试数字、回执、diff 范围）。
3. **PR**：`gh pr create --base main`；正文三要素：改了什么、为什么、验证证据（真实 passed/failed/skipped 数字）。禁止自夸式描述。
4. **合并**：条件 = CI `pytest` 绿（远端硬检查，红了物理上合不进）。统一用 `gh pr merge --auto --squash --delete-branch`：CI 绿自动合入、自动删分支。
5. **授权（长期有效，2026-08-16 用户授予）**：同时满足以下四条时，Agent 可自主走完 commit → push → PR → 合并 → 删分支全流程，无需逐次请示：CI 绿；PR 证据齐；diff 只含声明的主题；不碰删除/移动/覆盖已跟踪路径。**仍需当场授权**：删除/移动路径、改 ruleset 或仓库设置、force-push、改可见性、建删 tag、发 release。每次自主合并在 NOTES.md 留痕（PR 号、主题、CI 证据）。
6. **收尾**：每个工作单元结束 = commit + push + 更新 NOTES.md（做了什么、证据在哪、下一步）；工作区必须 clean，做不到就 stash 并在 NOTES.md 写明原因；每个工作日结束 push 全部分支；PR 挂起超 1 天未推进必须关闭、转 draft 或报告原因。
7. **禁止入库**：`CODE/Results/`、`leo_sim_out/`、`out/`、`remote.env`、`.env`、`__pycache__/`、`.DS_Store`（.gitignore 已配；发现漏网先补 gitignore 再提交）。
8. **VM 部署**：只允许 main 上的干净 commit，经 `CODE/scripts/remote/push-remote.sh` 执行；跑实验前必须已部署；部署后记录回执 SHA。
9. **矛盾处理**：发现历史/文档/代码互相矛盾时，并列报告出处与影响，禁止静默融合或擅自覆盖。

## 防失控护栏

10. **禁止刷提交**：禁止空 commit；CI 红之后，每次推送必须附带新的诊断或修复——无新信息的重推一律禁止；连续 2 次修复仍红，停止操作，在 PR 写明失败分析（错误原文、定位、假设），报告用户等指示。
11. **禁止削弱检查**：CI 红时只能修代码缺陷或测试自身的真实缺陷；禁止删测试、放宽断言、注释检查、改 workflow 让它「看起来过」。确需调整测试门槛的，单独 PR 并在标题明示「测试调整」。
12. **main 红优先**：发现 main 红（无论谁造成），优先修 main，不在红 main 上继续堆新 PR。
13. **多 Agent 仲裁**：一个分支写入者唯一，禁止多 Agent 写同一分支；并行会话用独立 worktree/clone（`git worktree add`），不在他人分支/PR 上追加提交（续作从 main 新切分支，或由原写入者明确交接）；涉及 `CODE/leo_sim/kernel.py`、`receipt.py`、`governance.py`、`learning.py` 或 `experiment_platform/` 授权链的承重改动，生产者不得自批，需独立冷启动复核。

## 三端职责（本地 / GitHub / VM，单向链）

继承旧调研《三端工作流与边界》（2026-06-26，存旧库）：**本地**做设计/开发/分析，不当唯一备份；**GitHub** 是唯一代码版本真相源（本地与远端不得漂移，全分支每日 push）；**VM** 只做受控执行与生产原始证据，不长期维护代码、不手工改、不跑未提交代码。从论文 claim 必须能反溯：本地分析 → GitHub commit → VM 原始实验。

## 渐进式验证协议

- 任务拆成可独立验收的步骤；每步完成以测试/回执/diff 范围为证据，不以「能跑」「看起来对」代替。
- 行为改动先记录旧版数值，再在新版重跑同一检查（新旧对照）。
- 禁止把「import 成功」「退出码 0」当作完成证据。

## 当前状态

- 见 `NOTES.md`。平台来源与谱系见 `README.md`。
