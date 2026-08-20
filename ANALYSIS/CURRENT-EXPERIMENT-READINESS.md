# leo_sim V2 当前实验就绪状态

> 状态最后核验：2026-08-21；当前 main 为 `0c378a5`。V2 结果适配器、trace provenance（含 burst/diurnal 变换参数）已合入；当前 SHA 已部署 VM 并通过非正式工程 smoke，真实授权 cohort/E0 论文数据仍未完成。
> 判定词：`FACT` 为当前可核验证据；`INFERENCE` 为基于证据的判断；`ESTIMATE` 为带前提的工期范围，不是承诺。

## 1. 两个目标

| 目标 | 完成定义 | 当前位置 | 剩余工作的性质 | 时间估计 |
|---|---|---|---|---|
| A. 可可信跑真实流量诊断/pilot | D1/D2 与核心语义冻结；V2 证据链闭合；真实流量、多 OD/突发、利用率和三段时延可重算；同一 SHA 经审阅部署 VM | **部分达到：D1/D2、奖励门和最小事件观测已合入；V2 适配器已有真实 receipt/paired 重算测试；仍缺真实 provenance、利用率正式分母、授权 cohort 与当前 SHA 的 VM/pilot** | 补 provenance/分母口径，部署 `2f577a5` 后跑授权 smoke、E0-REAL、基线 pilot | **ESTIMATE：3–7 个专注工作日**；当前测试/工程 smoke 不能当论文数据 |
| B. 可支撑论文主结论 | 目标 A 通过；完成 Q0-I/Q0-F、候选方向物理特征、逐字段 AoI、replay 续训；诊断后提出方案并完成配对正式矩阵 | **尚未达到；Q0 只有快照，信息/续训能力未闭合** | 理论归因、机制反例、长训恢复、正式统计与外部有效性 | **ESTIMATE：目标 A 后 4–10 周**；取决于诊断是否支持明确机制及训练成本 |

目标 B 必须定义为“本研究范围内的 practical ceiling”，不能定义成所有卫星网络机制都完美。未校准的 Doppler、天线、ARQ、天气或链路参数即使代码存在，也不自动提高科研可信度。

## 2. 当前事实快照

| 项目 | 当前事实 | 判定 |
|---|---|---|
| GitHub main | `0c378a5`（完整 SHA `0c378a5...`）；本地完整套件 `565 passed, 1 skipped, 3 subtests passed` | FACT |
| D1 动态链路速率 | PR #55 已合入 main；独立冷审 APPROVE；D1 定向 `51 passed`，合并后 CI 绿 | FACT |
| D2 动态拓扑/holding 语义 | PR #56 已合入 main；合并提交前本地 `555 passed, 1 skipped, 3 subtests passed`，CI pytest SUCCESS | FACT |
| 当前 VM | 已部署精确 main `0c378a5`；deployment receipt `7a3c06a6...`，source tree SHA `abf0c049...` | FACT |
| VM 工程 smoke | `CODE/Results/_codex_vm_smoke_499d2e6`（前一版）和 `CODE/Results/_codex_vm_burst_smoke_0c378a5`（修复版）自然结束；修复版 receipt verify=`verified`、85/85 delivered、burst 参数已写入 provenance | FACT；非正式、非授权运行 |
| 真实流量/测量 | CSV 已支持 packet-level 多 OD；M-Lab 与 population-gravity 是代理；burst window 已有。trace manifest 绑定 source type/path/SHA、单位、OD 映射、目标/实际 offered load 及 burst/diurnal 变换参数；事件层由 `2f577a5` 合入并由 ledgers 重算；整段可用时间分母和正式 provenance 仍 open | FACT；当前 SHA 已部署 |
| Q0 | snapshot 已在 main；planned-vs-executed、holding、Q0-I tiny 存在于未合入候选分支并收到 REQUEST_CHANGES；Q0-F 精确交叉验证未完成。Q0 不阻塞 E0/pilot，但阻塞理论归因和新方案冻结 | FACT |
| 正式分析链 | generic 链已恢复；新增 `CODE/experiment_platform/v2_analysis.py`，可校验 V2 receipt/formal/governance/ledgers、重算指标并做 paired analysis，且 RUNBOOK 已生成入口；尚无真实授权 cohort 的持久化分析产物 | FACT，partial；R7-F1 仍 blocking |
| 三轮三方无新问题 | 只完成局部 PR/局部模块审阅，没有在最终冻结平台上完成连续三轮 | FACT，未满足 |

## 3. 目标 A：真实流量诊断/pilot 就绪门禁

工期按“代码和评审资源连续可用、VM 正常、没有新 blocking”估计；任务可部分并行，但最终审计与 VM 部署必须在冻结代码之后串行。

| 工作包 | 验收证据 | 当前状态 | ESTIMATE |
|---|---|---|---:|
| A0 文档与合同收敛 | 主线、阶段门禁、机器清单和 claim 边界一致 | 本 PR 处理 | <1 日 |
| A1 D1/D2 入 main | 精确 head 复核有效；CI 绿；合入后 main 全量与行为对照绿 | **已完成**：#55/#56 已合入；D1/D2 合入记录在 `66be0ad`，当前 main 继续保留 | 已完成 |
| A2 已知科学 blocker | 奖励正循环、mask 信息泄漏、deadline/Q0 控制范围有明确修复或冻结决策 | mask 已由 #62 关闭；其余 open | 2–5 日 |
| A3 正式证据链 | compile、review、authorize、run、receipt、analysis、claim 测试均存在并在 CI/本地通过 | V2 结果适配器与重算测试已存在；真实授权 cohort、持久化 output 和 claim review 仍 open | 1–2 日 |
| A4 真实流量与测量 | provenance、多 OD/突发；逐向利用率分子/分母；每包 queue/tx/prop；拥塞指标可从 artifact 重算 | trace provenance 合同已实现（source/SHA、单位、OD 映射、offered-load）；服务窗事件与重算已合入；整段可用时间分母选择和 VM 验收仍 open | 1–2 日 |
| A5 最终平台审计 | 冻结 commit 上三轮 Codex/不同模型/网页 GPT 无新增 blocking/major | 未开始最终三轮 | 2–5 日 |
| A6 VM 与 pilot | 部署同一 main SHA；VM/TF 门禁、真实 smoke、E0-REAL、基线诊断与 pilot 自然结束 | **当前 SHA VM 工程/MCS/burst smoke 已完成；E0-REAL/基线 pilot 尚未开始** | 1–3 日 |

最早的真实流量 smoke 会早于目标 A 完成，但它只能暴露工程问题。Q0 不阻塞这个 smoke 或 E0-REAL；V2 分析链、利用率分母和三段时延才是把诊断升级为论文证据的硬门。

## 4. 目标 B：论文主结论就绪路线

| 层 | 需要补到什么程度 | 当前主要缺口 | 是否阻塞目标 A |
|---|---|---|---|
| 物理/拓扑 | D1/D2；长时窗接缝、极区、接入/切换边界；选择性加入 Doppler/ARQ/天线并校准 | D1/D2 未合；高级物理尚无实证校准 | D1/D2 是；高级物理否 |
| 信息 | 每类信息来源、传播、年龄、预测性与 mask 完全一致 | #62 已关闭已知 cache-hop 旁路；逐候选物理特征和逐字段 AoI 未完成 | 不阻塞 E0；阻塞信息归因/相应学习臂 |
| 控制 | 路由、等待、服务顺序、接入分配的权限分层 | Q0-I/Q0-J 控制范围未完全冻结 | 不阻塞诊断；阻塞理论归因 |
| 流量 | 真实/代理 trace 为主，uniform 为控制；多 OD 与突发 | CSV/M-Lab/gravity/burst 骨架已有，provenance 合同需补 | 阻塞 E0-REAL |
| 学习 | 公平训练/评估、收敛诊断、完整断点恢复 | replay/optimizer/target/RNG 不持久 | 不阻塞短基线；阻塞昂贵长训和新方案正式训练 |
| 测量 | 端到端指标、丢包/积压、逐向利用率、queue/tx/prop 分解、V2 可重算分析 | 利用率分母、每包三分量与 V2 分析入口缺失 | 阻塞论文级拥塞诊断 |
| 校准/反驳 | 旧新行为对照、极端反例、参数敏感性、外部数据校准 | 尚未形成覆盖各层的校准套件 | 部分在目标 A 后进行 |

目标 B 应以论文 claim 为边界逐项验收，而不是一次性把旧平台全部功能搬回。能力取舍见 `PLATFORM-CAPABILITY-LEDGER.md`。

## 5. 下一步顺序

1. 完成本轮主线与机器清单收敛，不再让旧 EXP1→EXP3 顺序支配当前工作。
2. D1/D2、奖励门和事件观测已合入；V2 适配器本地全量绿，但 R7-F1 仍要用真实授权结果收口。
3. 合入并部署 trace provenance 合同；用 CSV 多 OD/突发样本验收 source/SHA、单位、OD 映射和 offered-load 重算，并在论文实验合同中明确服务窗容量或整段可用时间分母。
4. 当前 `0c378a5` 已部署并通过非正式/MCS/burst smoke；下一步用正式 trace/provenance 合同跑授权 smoke，再跑 E0-REAL、DIAG-CONGESTION 与基线 pilot。
5. 从诊断窗口实现并交叉验证 Q0-I/Q0-F tiny，再补候选方向物理特征和逐字段 age 信息阶梯。
6. 根据诊断与 Q0 差距提出机制；长训前补 replay/optimizer/target/RNG 完整恢复。
7. 小规模反例通过后冻结配对正式矩阵，运行 `EXP-CC-FORMAL`；旧 hops/aggregation 实验仅在能解释主机制时触发。
