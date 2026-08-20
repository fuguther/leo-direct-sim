# 分析与实验文档入口

> 文档状态最后核验：2026-08-20。当前状态必须从本页列出的 `CURRENT` 文档进入；带日期的报告通常只是历史快照。

## 当前真相源

| 文档 | 地位 | 用途 |
|---|---|---|
| `CURRENT-EXPERIMENT-READINESS.md` | CURRENT | 平台两个目标、当前差距、门禁、时间估计和下一步 |
| `PLATFORM-CAPABILITY-LEDGER.md` | CURRENT | 旧平台与 V2 能力对照、必须补/按 claim 补/后续研究臂 |
| `Q0-INFORMATION-ABLATION-PROTOCOL.md` | CURRENT | Q0-F/Q0-I、从最优向下裁剪信息、从现实向上增加信息 |
| `EXPERIMENT-PROGRAM.md` | CURRENT | 完整实验顺序、研究问题、依赖、统计和证据要求 |
| `FINDINGS-REGISTRY.md` | CURRENT | 唯一问题台账；状态不能由其他报告覆盖 |
| `../EXPERIMENTS/experiment-program.yaml` | CURRENT | 可机读的实验依赖与状态清单，不是运行授权 |
| `../docs/superpowers/specs/2026-08-21-research-execution-and-training-budget-design.md` | DECISION RECORD | 本轮锁定的总目标、执行顺序、训练闭环和拓扑时间尺度；详细人类计划仍以 `EXPERIMENT-PROGRAM.md` 为准 |
| `../NOTES.md` | ROLLING LOG | 最近操作与证据索引，不承担当前状态真相源 |

## 文档状态词

- `CURRENT`：允许用于安排下一步和判断当前状态。
- `SUPPORTING`：保留设计、数学、实测或审阅细节；状态以 CURRENT 文档为准。
- `HISTORICAL`：只表示成文日期当时的事实，不允许据此判断现在。
- `SUPERSEDED`：现行结论已经合并到稳定命名的新文档；旧文仅作证据来源。

## 旧文档路由

- Q0 日期稿：`Q0-ALGO-RESEARCH-*`、`Q0-INTERFACE-DESIGN-*` → 当前协议为
  `Q0-INFORMATION-ABLATION-PROTOCOL.md`。
- 平台迁移/旧平台审计：`MIGRATION-BACKLOG-*`、`LEGACY-DESIGN-AUDIT-*` →
  当前结论为 `PLATFORM-CAPABILITY-LEDGER.md`。
- 实验 07/08/09 与 E0/E1 历史结果 → 当前程序为 `EXPERIMENT-PROGRAM.md`；
  历史数值不得自动继承到 D1/D2 后平台。
- `MORNING-REPORT-*`、`OVERNIGHT-REPORT-*`、旧 handoff/implementation report →
  只作历史证据。
- `LINK-BUDGET-DESIGN-*`、`TEMPORAL-MULTISTEP-DESIGN-*`、`REWARD-DIFF-*`、
  `VM-TF-VERIFICATION-*`、`ACCEPTANCE-LADDER-*` → supporting 设计或协议。

## 正式实验事实边界

正式分析必须从已验证 run ID、manifest、receipt 和 artifact hash 开始，不能从目录名、截图或手工汇总开始。当前仓库缺少历史文档曾引用的 `ANALYSIS/paired_analysis.py`，因此“编译 → 授权 → 运行 → 持久化分析 → claim”链目前是阻塞项；在实现并验证新的持久化分析入口之前，不得照抄旧命令或声称分析链可用。

每个正式实验实例仍应保存：

- `request.json`：预注册研究问题、arms、配置、seeds、指标和验收门；
- 编译生成的 `run-manifest.json` 与授权产物；
- VM 自然结束 receipt、artifact manifest 和原始产物；
- 重新计算得到的 analysis manifest、整洁 summary 与 report。

实验结果目录继续不入 Git。
