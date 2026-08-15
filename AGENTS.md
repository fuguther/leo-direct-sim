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

## Git / GitHub 工作流（任何 Agent 必须逐条遵守）

**总原则：`main` 永远绿、永远可部署。一切改动经 PR 合入，CI 全绿才可合并；远端由 ruleset 硬执行，不靠自觉。**

1. **分支**：从最新 `main` 切 `codex/<yyyymmdd>-<主题>`（如 `codex/20260816-fix-reward`）。一个分支只做一件事，寿命 < 3 天，合并即删（远端已开启 merge 后自动删分支）。
2. **提交**：commit message 用类型前缀 `feat|fix|docs|exp|chore` + 中文简述；一个 commit 只含一个变更主题（代码、数据、文档不混；重构与修 bug 不混）。正文写清证据（测试数字、回执、diff 范围）。
3. **PR**：`gh pr create --base main`，标题同 commit，正文必须含：改了什么、为什么、验证证据（真实的 passed/failed/skipped 数字）。禁止自夸式描述。
4. **合并条件（远端硬执行）**：CI `pytest` 检查必须通过；一律 `gh pr merge --squash --delete-branch`。CI 红禁止合并，先把失败修绿。
5. **推送**：每个工作日结束 push 全部分支（GitHub 兼作每日备份）。禁止 force-push main；main 禁止删除。
6. **授权（长期有效，2026-08-16 用户授予）**：满足下列全部条件时，Agent 可自主完成 commit → push → PR → squash merge → 删分支全流程，**无需逐次请示**：
   - CI `pytest` 检查通过（远端 required check 绿）；
   - PR 正文已写明改动内容与真实验证证据（passed/failed/skipped 数字）；
   - diff 只含声明的变更主题，无夹带；
   - 不涉及删除/移动/覆盖已跟踪路径（这类仍须逐条列出等用户批准）。
   可用 `gh pr merge --auto --squash --delete-branch`（仓库已开 auto-merge），CI 绿后自动合入。
   **以下动作仍需用户当场授权**：删除/移动路径、修改 ruleset 或仓库设置、force-push、改仓库可见性、建删 tag、发布 release。
   每次自主合并必须在 NOTES.md 留痕（PR 号、改动主题、CI 证据）。
7. **收尾**：每个工作单元结束 = commit + push + 更新 `NOTES.md`（做了什么、证据在哪、下一步）。工作区必须 clean，做不到就 stash 并在 NOTES.md 写明原因。
8. **禁止入库**：`CODE/Results/`、`leo_sim_out/`、`out/`、`remote.env`、`.env`、`__pycache__/`、`.DS_Store`（.gitignore 已配；发现漏网先补 gitignore 再提交）。
9. **VM 部署**：只允许 main 上的干净 commit，经 `CODE/scripts/remote/push-remote.sh` 执行；跑实验前必须已部署；部署后记录回执 SHA。
10. **冲突处理**：发现历史/文档/代码互相矛盾时，并列报告出处与影响，禁止静默融合或擅自覆盖。

## 三端职责（本地 / GitHub / VM，单向链）

继承旧调研《三端工作流与边界》（2026-06-26，存旧库）：**本地**做设计/开发/分析，不当唯一备份；**GitHub** 是唯一代码版本真相源（本地与远端不得漂移，全分支每日 push）；**VM** 只做受控执行与生产原始证据，不长期维护代码、不手工改、不跑未提交代码。从论文 claim 必须能反溯：本地分析 → GitHub commit → VM 原始实验。

## 多 Agent 写入仲裁

- 一个任务一个分支；分支写入者唯一，禁止多 Agent 写同一分支。
- 并行会话各自从 main 切分支（必要时用 git worktree 隔离工作树），冲突时停在可复核状态并报告，不擅自合并消解。
- 合并以 CI 绿 + PR 记录为凭；生产者不得自批高影响改动。

## 渐进式验证协议

- 任务拆成可独立验收的步骤；每步完成以测试/回执/diff 范围为证据，不以「能跑」「看起来对」代替。
- 行为改动先记录旧版数值，再在新版重跑同一检查（新旧对照）。
- 禁止把「import 成功」「退出码 0」当作完成证据。

## 当前状态

- 见 `NOTES.md`。平台来源与谱系见 `README.md`。
