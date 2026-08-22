# LEO 拥塞控制与链路利用率实验总计划

> **2026-08-22 当前执行快照（覆盖下方旧状态说明）**：先做工程 pilot，再做正式论文实验。当前平台已经可以在 VM 上运行真实的 M-Lab measurement-proxy 多 OD + burst、动态 MCS/拓扑和可审计 receipt；E0 R02 六个负载 cell 已跑完并完成 V2 重算。50/100/200 Mbps 仍是扫描档，不是最终冻结：实测三档都落入预注册 medium，暂定最低候选 50 Mbps，需补两个 seed 和低端 bracket。非学习资源候选为 1 vCPU/job、12 jobs 并行；学习训练必须单独做 CPU/RSS profile。学习正式 cohort、三段时延正式 gate、Q0 真实闭环和论文 claim 仍未关闭，故当前顺序是“负载确认 → 非学习诊断 → 学习 pilot → Q0/信息归因 → 新方案”，而不是直接收集论文 headline 数据。

> CURRENT；最后核验：2026-08-21。当前 main `bfae761` 已部署 VM；M-Lab measurement-proxy 的有界多 OD + burst T0、topology cadence 工程校准、receipt horizon 修复、physical available-capacity 分母、新 profile 的 E0 工程负载标定、60 秒 D2 长窗、capacity 负对照和学习 train→eval 工程 smoke 已完成。continuation bundle 已通过 VM 单步恢复等价；50/100/200 Mbps 只冻结为下一阶段的低/中/压力候选，不是正式论文结果；V2 artifact→claim 闭环、逐包三段时延正式 gate、完整长窗中断/不间断等价、formal VM E0/PILOT 仍未完成。本文是实验路线的人类真相源，机器可执行索引见 `../EXPERIMENTS/experiment-program.yaml`。

## 1. 研究主线与工作方法

主线锁定为：**LEO 动态网络中的拥塞控制与链路利用率**。

顺序固定为：

1. **先实验诊断**：用有来源记录的真实流量或测量代理，找出何时拥塞、堵在哪里、容量是否被有效使用、现有算法为什么失效。
2. **再理论解释**：用 Q0-I/Q0-F 和信息裁剪区分物理容量不足、信息不足与决策能力不足。
3. **最后提出方案**：只有诊断和上界共同支持某个机制缺口，才设计新的拥塞控制方法；不能先假定创新点再挑实验。

真实流量是主证据。uniform synthetic 仍保留，但只用于守恒/边界 sanity、可控负载标定和敏感性对照，不能替代外部有效性。

## 2. 什么必须做，以及何时做

用户已指定下列能力全部纳入项目范围。“全部要做”不等于“全部阻塞第一次工程 smoke”；每项只在最早会影响结论的阶段成为硬门。

| 能力 | 最早硬门 | 原因 |
|---|---|---|
| D1 动态链路速率、D2 动态拓扑 | E0-REAL 前 | 不正确的容量和邻居关系会直接伪造拥塞与利用率 |
| 奖励/动作信息边界、V2 正式证据链 | 学习基线或任何论文级 run 前 | 防止算法利用不该知道的信息，并保证结果可重算 |
| 真实流量 provenance、多 OD、突发流量 | E0-REAL 前 | 主线要求先面对真实负载结构；M-Lab/人口重力只能按真实测量代理表述 |
| 链路利用率可重算合同 | DIAG-CONGESTION 前 | 必须同时记录可用容量分母和实际服务分子，按链路、方向、时间窗重算 |
| 每包 queue/tx/prop 三段时延 | DIAG-CONGESTION 前 | 主线要解释拥塞来自排队还是物理传播/发送，不能只报端到端时延 |
| Q0-I/Q0-F 最优参照 | 理论归因和新方案冻结前 | 它回答信息不足还是决策不足；不阻塞 E0、工程 smoke 和基线诊断 |
| 每个候选方向的距离、速率、可用性特征 | INFO-LADDER/使用这些特征的学习臂前 | 测量字段与给算法看的观测必须分开，不能因记录它就默认泄露给所有臂 |
| 逐字段信息年龄 | AGE-LADDER 前 | cache 整体年龄不能冒充每个字段的生成、接收和来源年龄 |
| replay buffer 续训 | 长时学习/新方案训练前 | 一次完整短训练不依赖它；昂贵训练需要恢复 replay、optimizer、target 与 RNG 才可复现 |

## 3. 实际执行顺序

### P0：论文级平台底座

先关闭会改变任何后续结论的底层问题：

- D1/D2 代码已合入并有回归测试；当前 `69c40b1` VM 已部署，MCS/动态拓扑多 OD T0、三档负载标定、60 秒长窗和学习 smoke 均已有同代码系列工程证据，但 D1 旧平台逐距离 MCS 对照仍缺；
- 已知 R1-A1 额外跳数刷分风险已关闭；仍需把 shaped reward 与 Q0 物理目标分离，已修复的 mask 旁路也不能代表整体信息公平完成；
- 闭合 V2 `compile → review → authorize → run → receipt → metric recomputation → paired analysis → claim`；当前只完成矩阵编译/授权 Stage 1，真实 artifact→claim 闭环仍缺；
- 当前 `bfae761` 已部署并承接非学习同 SHA 工程 T0/cadence smoke、E0 负载标定、资源剖析、60 秒 D2 长窗、capacity 负对照和 Q-learning/DDQN/GAT/MPNN train→eval 工程 smoke；continuation bundle 已做 VM 单步恢复等价；正式授权 cohort、formal VM E0/PILOT 和完整长窗等价仍需按 runbook 执行。

P0 的验收是“同一 SHA 的结果可以被重新算出来并拒绝篡改”，不是仅有 pytest 绿。

### P1：真实流量与测量底座

#### TRAFFIC-T0（工程闭环，非论文结果）

`mlab_multiod_burst_t0.yaml` 显式开启 `endpoints.mlab_auto`：从快照的 44,929 条测量、4,752 个有向 OD 对和 2,604 个聚合单元中，按最大强连通测量子图选择 56 个单元，默认上限 64；不用“所有城市都是网关”的假设。trace manifest 记录候选规模、选中单元、source weighting、源文件 SHA 和 `measurement_proxy` 边界。20 s VM T0 已自然结束、守恒、receipt 和 raw metrics 重算均通过；它证明数据映射链可执行，不证明论文效果。

#### TOPOLOGY-CADENCE-CALIBRATION（工程校准，非论文结果）

在进入 E0 负载标定前，用同一份不可变的 M-Lab measurement-proxy + burst trace 比较拓扑重算间隔 `0.5/1/2/5 s`。这一步只回答“更新太慢会不会改变当前负载下的结果、以及运行成本如何”，不把短 smoke 当成 D2 长窗语义已经完全证明。

本轮以合入并部署的 `8e2f1df` 为准：profile 为 140 星、20 s、MCS、50 Mbps、8--16 s burst、56 个测量强连通候选单元；四档均 natural end、conservation true、receipt verified，且 trace SHA 均为 `f6981c327f4c36e659d3f7b5ef66128f94a199d0203591401c88ed0e8ab22de4`。fates 均为 1,299 offered、613 delivered、579 `ACCESS_REJECTED`、107 `IN_SYSTEM_AT_STOP`；raw packet/service/availability ledgers 独立重算均 `validation.ok=true`。该轮仍是工程校准，不是 formal E0 或论文结果。

| cadence | VM 140 星/20 s 结果 | VM 墙钟 | 工程判断 |
|---:|---|---:|---|
| 0.5 s | 613 delivered / 579 rejected / 107 in-system；39 次重算、21,726 availability samples | 171 s | 成本最高；只多采样，未改变交付/每包指标 |
| 1.0 s | 与 2/5 s 逐项相同；19 次重算、10,932 samples | 120 s | **当前 E0 主候选**，保留秒级拓扑变化 |
| 2.0 s | 与 1/5 s 逐项相同；9 次重算、10,932 samples | 107 s | 成本敏感性对照 |
| 5.0 s | 与 1/2 s 逐项相同；3 次重算、10,932 samples | 94 s | 慢更新负对照，不直接作为主设置 |

结论是暂定的：E0 先用 1 s，2 s 做成本敏感性，5 s 做慢更新负对照；只有在低/中/高负载和长窗上仍保持交付、积压、利用率和切换指标稳定，才考虑降低主 cadence。该轮没有把连续进程 RSS 当作逐 run 内存证据；内存门禁留到独立的 E0 资源剖析。

#### E0-LOAD-CALIBRATION（工程负载标定，非正式论文结果）

PR #93 改变了 M-Lab 端点选择（从显式三点变为有界强连通多 OD）；此前 50/100/200 Mbps 三 OD 表格只能作为历史先验，不能直接沿用。现已在 `8e2f1df`、56-cell profile、cadence 1 s 上完成同一 VM 环境的三档工程标定，并记录同一 trace/config/VM 证据。

下面这张表是新 56-cell 多 OD profile 的工程标定结果，不是正式效果比较，也不冻结论文最终负载。旧三 OD 表仍保留在历史 NOTES 中，仅作背景先验。标定只改变 `offered_mbps`，目标是找出无明显溢出、可解释积压和明显压力三个区间。

| offered load | offered / delivered | 主要非交付结果 | VM 墙钟 | 结论 |
|---:|---:|---|---|---|
| 50 Mbps | 1,299 / 613 | 579 `ACCESS_REJECTED`，107 `IN_SYSTEM_AT_STOP`，0 holding overflow | 119 s | 低负载候选 |
| 100 Mbps | 2,756 / 1,253 | 1,270 `ACCESS_REJECTED`，233 `IN_SYSTEM_AT_STOP`，0 holding overflow | 129 s | 中负载候选 |
| 200 Mbps | 5,551 / 2,382 | 2,597 `ACCESS_REJECTED`，405 `IN_SYSTEM_AT_STOP`，167 `HOLDING_QUEUE_OVERFLOW` | 134 s | 压力/过载对照 |

三档均在同一 canonical VM、同一 `8e2f1df`、同一 56-cell M-Lab/burst profile、1 s cadence 下自然结束，`conservation_ok=true`、`receipt verify=verified`，原始 ledger 重算 `validation.ok=true`。对应 trace SHA 为 `f6981c327f4c36e659d3f7b5ef66128f94a199d0203591401c88ed0e8ab22de4`（50）、`e6e7bd329f6822046f5d57611690d609a3647e1dca7639e170e985d891000e09`（100）、`f009c98d8be5757a4ba1afe585fed32d6974143582eb3c9d8657344413a834c6`（200）。因此暂定 `50` 为低负载、`100` 为中负载、`200` 为压力/过载对照；这只是工程标定，不是论文效果结果。正式冻结前仍需完成 available-capacity 独立重算记录、逐包三段时延 artifact、资源 RSS 门禁、replay 续训和正式授权 E0。`10 Mbps` 另作低负载 sanity，不作为主三档之一。

#### TRAFFIC-VALIDATE

- 主输入优先采用有来源、许可证/使用边界、时间范围、字段含义和 SHA 的 packet/flow/OD 数据；
- 当前 CSV 支持多 OD；M-Lab 与 population-gravity 属于测量/人口代理，报告时不得写成原始真实 packet trace；
- 在同一 trace 上构造可复现 burst window，同时保留 uniform 作为控制组；
- 验收包括源文件 hash、单位、时间映射、OD 映射、裁剪规则和注入后 offered bits 重算。

#### METRIC-VALIDATE

最小测量合同必须能从原始事件独立重算：

- offered、admitted、delivered、dropped、deadline-missed、in-system bits/packets；
- 每条有向链路每个时间窗的 available capacity、busy/service bits 和 utilization；
- queue integral、峰值/终值 backlog、overflow、holding；
- 每包 queue、transmission、propagation 和 end-to-end latency，且三段和可校验；
- 路径长度/绕行、公平性及吞吐，避免用高利用率掩盖堵塞或饥饿。

#### E0-REAL

- 先用确定性路由和真实流量/代理 trace 扫负载；当前工程标定已给出低/中/压力三个候选档，下一步在同一 trace/配置合同上做资源剖析和算法 pilot；
- 冻结低、中、高三档：低档接近无拥塞，中档能区分机制，高档明显积压但非全面塌缩；
- uniform E0 只作 sanity 和边界对照；旧 50/100/200 Mbps 只作历史先验。

### P2：先诊断现有系统

#### PILOT-BASELINES

每个基线至少一个完整 cell，检查 natural_end、守恒、trace provenance、探索关闭、checkpoint 血缘、双种子、V2 分析闭环、墙钟/显存/方差。pilot 只校验链和估算成本，不给论文效果结论。

#### DIAG-CONGESTION

pilot 通过后，在配对相同的 trace、load、拓扑和 seed 下运行 deterministic shortest-path/queue-aware 等非学习锚点，以及当前 DDQN、GAT、MPNN 可运行基线。必要的 oracle/负对照可以加入，但不提前加入“新方案”。

回答四个问题：拥塞首先出现在哪里；容量是没被用还是被少数热点占满；丢包/尾时延主要来自哪一段；失败来自路由绕行、陈旧信息、训练失败还是物理容量不足。

### P3：理论归因与信息阶梯

#### Q0-I-TINY

- 当前全局真值，不知道未来随机实现；
- 事件驱动 DP/SMDP 与独立穷举或第二实现同值；
- 通过 planned-vs-executed replay 对齐内核物理；
- 目标使用 delivered/deadline/backlog/utilization/fairness 等物理量，不用 shaped reward 冒充最优。

#### Q0-F-TINY

- 固定完整未来 trace/中断时间线；
- 事件时间 MILP/CP-SAT 与可枚举实例交叉一致；
- 验证同一物理和控制范围下 `V_F >= V_I`。

Q0 tiny 通过后，可从真实诊断 trace 中截取代表性小窗口，估计物理不可达差距、未来信息价值、当前信息下的决策差距和实际学习算法差距。

#### INFO-LADDER / AGE-LADDER

- F0：本地队列与目的地方向；
- F1：增加每个候选方向的距离、速率、当前可用性；
- F2：增加逐字段 generated/received/source age；
- 负对照包括 shuffle age、固定新鲜 age、相同参数量但无真实 freshness 的臂。

### P4：提出并验证新的拥塞控制方案

只有 P2/P3 指向明确缺口后，才写机制假设。例如“瓶颈在热点队列且局部算法因容量/新鲜度不可见而误分流”必须同时有指标、反例和 Q0 差距支持。

进入长训前必须完成中断续训 vs 不间断训练对照。当前 continuation bundle 已持久化 replay transitions、online/target、optimizer、训练计数器、NumPy/TF RNG，并在 VM 通过恢复后继续一步等价；完整长窗对照仍是未闭合门。

先跑 NEW-SCHEME-TINY 和压力反例；失败则回到诊断，不直接扩大矩阵。

### P5：正式实验

#### EXP-CC-FORMAL（主实验）

- 主场景：来源明确的真实流量/代理 trace，多 OD，含自然或受控突发；
- arms：非学习锚点、最强现有学习基线、新方案、机制消融；
- 配对：同 trace × traffic seed × training seed；
- 主指标优先为按时交付/完成率与 backlog，链路利用率、吞吐、公平性、三段时延用于解释；
- 正式样本量由 pilot 的配对差方差和最小有意义效果确定。

E0 的 access boundary 是重标定前门禁：先用有限、显式的 access policy 完成
coverage/horizon audit 和 VM 小样，再冻结 offered load。历史 20 s 50/100/200
诊断只作为工程证据，不是 paper-ready；queue 语义下必须重新 E0 和训练。

#### SENSITIVITY（补充）

- uniform、gravity、不同 burst 强度、多 OD 结构和负载区间；
- 观测跳数、GAT/MPNN、信息内容/信息年龄只保留与主机制相关的消融；
- 不再默认按旧 EXP1→EXP2→EXP2B→EXP3 全部跑完。如果它们不能解释拥塞控制主结论，就降为条件性实验。

## 4. 解释纪律

- “真实流量”必须准确标注：原始 trace、实测聚合代理、人口重力代理或合成流量。
- 高链路利用率不是天然更好：必须同时检查交付、排队、丢包和公平性。
- 完成包时延必须和未完成/丢弃包一起解释，避免幸存者偏差。
- Q0-F 是 clairvoyant 严格参照；普通 MPC/滚动优化是强基线，不自动是严格上界。
- 负结果、学习失败、模型能力不足、信息不足和基础设施失败分别编码。
- 任何行为可观测改动都使旧实验进入 `rerun_required`，不能沿用旧曲线。
- 调优、训练、流量、评估 seed 分池且不重叠；跨 arm 使用相同 trace 配对。
- 先 pilot 冻结样本量、预算、主指标和主对比，再看正式效果。

## 5. 文件与证据形式

| 层级 | 文件 | 作用 |
|---|---|---|
| 项目级人类计划 | `ANALYSIS/EXPERIMENT-PROGRAM.md` | 研究问题、依赖、阶段门禁和解释纪律 |
| 项目级机器清单 | `EXPERIMENTS/experiment-program.yaml` | 稳定 ID、依赖、状态、arms、证据门 |
| 当前平台状态 | `ANALYSIS/CURRENT-EXPERIMENT-READINESS.md` | 当前 SHA、VM、已知缺口与最短下一步 |
| 能力账本 | `ANALYSIS/PLATFORM-CAPABILITY-LEDGER.md` | 旧新平台能力差距及阶段优先级 |
| 单次正式实验 | `EXPERIMENTS/EXP-*/request.json` | 冻结配置、seeds、指标、验收；经编译和授权 |
| 执行产物 | VM `Results/` | receipt、ledgers、trace、checkpoint、artifact manifest；不入 Git |
| 分析产物 | V2 analysis manifest + metrics + contrasts + claim | 从原始事件重算并绑定 hash |

YAML 只是计划索引，不能替代 request、授权或自然结束回执。任何状态变化都必须有证据链接，而不能手工把 `status` 改成 completed。
