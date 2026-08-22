# 分析与实验文档入口

> 文档状态最后核验：2026-08-23。机器可读状态以 `DOCUMENT-STATUS.json` 为准；仓库统一入口为 `../AGENT-START-HERE.md`。带日期的报告、旧工作包和旧实验目录不得自动解释为当前状态。

## 当前真相源

| 文档 | 地位 | 用途 |
|---|---|---|
| `CURRENT-EXPERIMENT-READINESS.md` | CURRENT-VOLATILE | 最近一次平台差距与门禁快照；外部状态需实时复核 |
| `PLATFORM-CAPABILITY-LEDGER.md` | CURRENT-VOLATILE | 旧平台与 V2 能力对照、当前迁移取舍 |
| `Q0-INFORMATION-ABLATION-PROTOCOL.md` | CURRENT-CONTRACT | Q0-F/Q0-I、从最优向下裁剪信息、从现实向上增加信息 |
| `EXPERIMENT-PROGRAM.md` | CURRENT-VOLATILE | 实验顺序、研究问题、依赖、统计和最近诊断状态 |
| `FINDINGS-REGISTRY.md` | CURRENT-VOLATILE | 唯一问题台账；处置状态会继续变化 |
| `../EXPERIMENTS/experiment-program.yaml` | CURRENT-VOLATILE | 可机读的实验依赖与状态快照，不是运行授权 |
| `../NOTES.md` | ROLLING LOG | 最近操作与证据索引，不承担当前状态真相源 |

## 文档状态词

- `CURRENT-CONTRACT`：允许决定现行定义、边界和流程。
- `CURRENT-VOLATILE`：允许提供最近状态，但 SHA、PR、CI、VM、run 和完成进度必须实时复核。
- `SUPPORTING`：保留设计、数学、实测或审阅细节；状态以 CURRENT 文档为准。
- `ROLLING-LOG` / `EVIDENCE-SNAPSHOT`：按时间或 revision 保存证据，不能判断当前状态。
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

正式分析必须从已验证 run ID、manifest、receipt 和 artifact hash 开始，不能从目录名、截图或手工汇总开始。仓库当前存在 `ANALYSIS/paired_analysis.py`，但文件存在或单测通过不等于真实授权 cohort 的“编译 → 授权 → 运行 → 持久化分析 → claim”链已经闭合；是否就绪仍以当前 checkout、真实产物和 `CURRENT-EXPERIMENT-READINESS.md` 的实时复核为准。

每个正式实验实例仍应保存：

- `request.json`：预注册研究问题、arms、配置、seeds、指标和验收门；
- 编译生成的 `run-manifest.json` 与授权产物；
- VM 自然结束 receipt、artifact manifest 和原始产物；
- 重新计算得到的 analysis manifest、整洁 summary 与 report。

实验结果目录继续不入 Git。
