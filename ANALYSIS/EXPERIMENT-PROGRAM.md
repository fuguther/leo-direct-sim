# LEO 拥塞控制与链路利用率实验总计划

> CURRENT；最后核验：2026-08-21。当前 main `42ff519` 已部署 VM；此前同代码的非正式/MCS/burst 工程 smoke 已通过，本文是实验路线的人类真相源，机器可执行索引见 `../EXPERIMENTS/experiment-program.yaml`。

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

## 2.1 2026-08-21 锁定：训练预算与拓扑时间尺度

这条规则是本项目的执行合同，后续实验不得为了省时间擅自缩短仿真时间，
也不得在没有测量的情况下把拓扑当成静态。

### 时间尺度的区分

当前代码中有三个不同含义的时间参数，不能互相替代：

| 参数 | 人话含义 | 主实验起始候选 |
|---|---|---:|
| `scenario.time_step_s` | 仿真推进和几何计算的时间粒度 | **0.1 s** |
| `topology.recompute_interval_s` | 卫星邻居重新匹配一次的间隔 | **先扫 0.5/1/2/5 s，1 s 为候选默认** |
| `control_plane.advertise_interval_s` | 邻居状态广告刷新间隔 | **1 s** |

`topology.recompute_interval_s` 不是越小越好：过小会显著增加事件量和内存，
过大又会把已经飞开的邻居继续当成可用邻居。正式选择规则是：在同一短 trace、
同一负载和同一 seed 下比较 0.5 s 与 1 s；若送达率相差不超过 2 个百分点、
利用率 p95 相差不超过 5%，且 1 s 的墙钟时间/峰值内存更低，则正式主实验使用
1 s，并把 0.5 s 作为 cadence 敏感性对照。若不收敛，则使用更小的间隔，不能
用 1 s 强行掩盖拓扑变化。

### 仿真时长与训练时长

仿真时长和训练墙钟时间是两个不同的预算：

- **3–5 s**：只用于 import、冒烟、单元场景和管线接线，不产生论文结论；
- **训练 episode 起始候选 20 s**：在 1 s 拓扑间隔下至少包含 20 次重匹配，
  并必须覆盖完整 burst 及其排空阶段；若实际 burst 更长，episode 随之延长；
- **正式评估起始候选 60–120 s**：用于观察稳定队列、多个拓扑变化和尾部指标；
- 最终时长以 E0 和资源 profiling 为准，但不得通过把 episode 压回 3–5 s 来
  “解决”训练过慢。

训练过慢时优先按以下顺序处理：

1. 先测 1/2/4/8 个 CPU 核的 steps/s、峰值 RSS 和每 episode 墙钟时间；
2. 选择达到平台最快区间且保留至少 20% 内存余量的核数；
3. 固定 episode 时长，减少并行 run 数、无效日志和重复评估，不在同一台 VM
   上并发挤压多个训练；
4. 按预注册的固定 update budget 或预注册的 patience 停止，不能事后挑最好
   checkpoint；
5. 长训正式实验必须恢复 replay、online/target、optimizer、训练计数器和 RNG，
   并通过“中断续训 vs 不间断训练”对照后才能进入论文矩阵。

每个训练臂都要保存 `resource_profile.json`，至少包含：代码 SHA、配置 SHA、
CPU 核数、线程环境、峰值 RSS、墙钟时间、steps/s、episode 时长、训练更新数、
checkpoint 选择规则和是否发生恢复。训练与评估分开排队执行；内存预算不足时在
启动前 fail closed，不允许运行到中途 OOM。

### “平台完成”的不可省略定义

平台完成不是“pytest 全绿”，也不是“模型类可以 import”。在进入正式实验前，必须
在同一已部署 SHA 上留下以下真实产物：

1. 非学习基线自然结束、守恒回执和指标重算；
2. Q-learning：训练自然结束、checkpoint 保存并重载、固定 trace 评估自然结束；
3. DDQN：TensorFlow 训练自然结束、checkpoint 保存并重载、同一 trace 评估自然结束；
4. 若正式矩阵使用 GAT/MPNN graph contract，则每个声称使用的 contract 各跑一个
   train/eval smoke，不能把“观察编码器存在”当成“算法已跑通”；
5. 每个学习臂都有峰值 RSS、墙钟、steps/s、训练步数和 checkpoint 血缘；
6. 任何一个必要学习臂没有这些证据，平台状态只能是 `learning_runtime_blocked`，
   后续不能开始该学习臂的正式实验。

为了让目标可实现，最低平台门只要求当前 runtime 已接入的学习臂；未接入的模型不
   先写入正式结果矩阵，必须先单独接入并通过同一 train/eval 门，或明确从论文范围
   移除。这样既保证“最后确实能训练”，又不把尚未存在的模型假定成可运行能力。

## 3. 实际执行顺序

### P0：论文级平台底座

先关闭会改变任何后续结论的底层问题：

- 合入并验证 D1/D2；
- 冻结物理目标与奖励语义，保留动作 mask 信息边界回归；
- 闭合 V2 `compile → review → authorize → run → receipt → metric recomputation → paired analysis → claim`；
- 冻结同一 main SHA，独立冷审后部署到 VM，跑 natural-end smoke；当前 `42ff519` 已部署，正式授权 cohort 仍需按 runbook 执行。

P0 的验收是“同一 SHA 的结果可以被重新算出来并拒绝篡改”，不是仅有 pytest 绿。

### P1：真实流量与测量底座

#### TOPO-CADENCE

- 在冻结 D1/D2 的同一 SHA 上，以 0.5/1/2/5 s 扫描 `topology.recompute_interval_s`；
- 保持流量 trace、负载、拓扑 seed 和评估算法不变，只改变重匹配间隔；
- 记录重匹配次数、退役/新建链路、在途/holding 包、送达率、利用率 p95、墙钟和峰值 RSS；
- 按 §2.1 的收敛规则选择主实验间隔；没有通过收敛检查前，不得把静态拓扑结果当作动态拓扑结果。

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

- 先用确定性路由和真实流量/代理 trace 扫负载；
- 冻结低、中、高三档：低档接近无拥塞，中档能区分机制，高档明显积压但非全面塌缩；
- uniform E0 只作 sanity 和边界对照；旧 50/100/200 Mbps 只作历史先验。

#### RESOURCE-PROFILE

- 用 E0 选出的低/转折/高负载各跑一个短训练 profiling cell；
- 只改变 CPU 核数（1/2/4/8），其余配置、trace、训练 seed 固定；
- 选择 steps/s 已进入平台最快区间且峰值 RSS 留出至少 20% 余量的配置；
- 该配置写入后续 request，训练和评估不得临时改变线程数或并发度；
- profiling 只估算成本，不选择最好模型，也不构成算法效果结论。

### P2：先诊断现有系统

#### PILOT-BASELINES

每个基线至少一个完整 cell，检查 natural_end、守恒、trace provenance、探索关闭、checkpoint 血缘、双种子、V2 分析闭环、墙钟/峰值 RSS/方差。必须使用已通过 `RESOURCE-PROFILE` 的 CPU/线程预算。pilot 只校验链和估算成本，不给论文效果结论。

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

进入长训前完成 replay 续训：持久化 replay transitions、online/target、optimizer、训练计数器、RNG、schema/config/SHA，并用“中断续训 vs 不间断训练”对照验证。

先跑 NEW-SCHEME-TINY 和压力反例；失败则回到诊断，不直接扩大矩阵。

### P5：正式实验

#### EXP-CC-FORMAL（主实验）

- 主场景：来源明确的真实流量/代理 trace，多 OD，含自然或受控突发；
- arms：非学习锚点、最强现有学习基线、新方案、机制消融；
- 配对：同 trace × traffic seed × training seed；
- 主指标优先为按时交付/完成率与 backlog，链路利用率、吞吐、公平性、三段时延用于解释；
- 正式样本量由 pilot 的配对差方差和最小有意义效果确定。

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
