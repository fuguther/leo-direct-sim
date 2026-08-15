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

## Git 纪律

- `main` 永远绿：提交前跑 `python -m pytest CODE/leo_sim/tests CODE/tests -q`（无 TF 环境下学习用例按设计跳过/报错属预期）。
- 工作分支 `codex/<yyyymmdd>-<主题>`，合并即删；CODE/ 改动走分支 + PR + squash merge。
- 文档类（NOTES.md、DECISIONS.md、ANALYSIS/）可直接提交 main。
- 每个工作日结束 push 全部分支。

## 渐进式验证协议

- 任务拆成可独立验收的步骤；每步完成以测试/回执/diff 范围为证据，不以「能跑」「看起来对」代替。
- 行为改动先记录旧版数值，再在新版重跑同一检查（新旧对照）。
- 禁止把「import 成功」「退出码 0」当作完成证据。

## 当前状态

- 见 `NOTES.md`。平台来源与谱系见 `README.md`。
