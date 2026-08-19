# 旧平台设计深审：新平台「忘记 / 想不到 / 做得不如」清单

> 日期：2026-08-19。执行人：Codex（本地读码，未派单）。
> 范围：以旧库 `/Users/lge/Desktop/LEO-Research-Workspace/CODE/`（SimulationRL.py 12556 行 + 依赖模块）为「旧平台 1 万行副本」主参照，
> 新平台为本库 `CODE/leo_sim/`（V2 直连）。逐行读码，不是扫两眼的定性对比。
> 判定词：`FACT`（两边代码都读到、行为差异明确）/ `INFERENCE`（代码支持但对研究影响的判断）/
> `未验证`（需进一步实测或确认）。
> 去重：凡已在 `ANALYSIS/MIGRATION-BACKLOG-20260816.md`、`ANALYSIS/REWARD-DIFF-20260816.md`、
> `ANALYSIS/TEMPORAL-MULTISTEP-DESIGN-20260816.md`、`ANALYSIS/LINK-BUDGET-DESIGN-20260816.md` 明确列出的，
> 标注「已在清单」并给清单编号，不重复计为新发现；**新发现**的是这些文档里没提的。

---

## 1. 结论速览

把旧平台设计逐块和新平台对照（物理建模 / 观测 / 奖励 / 训练 / 工程韧性 5 层），
**真正值得补、且新平台目前没有或做得不如的**，按证据强弱排序：

| # | 主题 | 判定 | 状态 | 是否值得迁 |
|---|---|---|---|---|
| D1 | 动态链路速率（Shannon/MCS + GSL/ISL 分级速率） | FACT | 已在清单 B5，**未实现** | 高 |
| D2 | 动态星间拓扑重匹配（星座移动后重建 ISL 对） | FACT | **清单未列** | 中（>5s 长窗才相关） |
| D3 | 多步回报 / TD-λ / temporal（framestack/GRU） | FACT | 已在清单 M2，**未实现** | 中-高 |
| D4 | Path-credit 轨迹级信用分配 | FACT | 已在清单 M3，**未实现** | 中 |
| D5 | 多智能体 / 每星独立模型 + FL + CKA 表示分析 | FACT | **清单未列** | 高（分布式论文臂） |
| D6 | per-action/逐方向链路特征进观测（slant+rate+到目的地向量） | FACT | 图合同部分缺失 | 中 |
| D7 | M3 队列动态特征（Δq 速度 + EMA 趋势）进观测 | FACT | **清单未列** | 中 |
| D8 | 队列/传输/传播时延三分量报告（per-block KPI） | 未验证(旧有) | 新侧需确认 | 中（论文指标） |
| D9 | 回放缓冲持久化 + 续训/热启动 | FACT | 已在清单 C3(低)，建议升级 | 中-高（长训） |
| D10 | 精度按步长/按 GT 数的 ε 调度；stopLoss 早期停止 | INFERENCE | **清单未列** | 低-中 |

> 注意：`D2`、`D5`、`D7`、`D10` 四个是本次**新发现、此前文档未提**的；其余在既有清单里有编号，但多数
> 仍是「只写设计稿 / 未实现」状态，本报告把它们和新增项一起收口。

---

## 2. 物理建模层

### D1 动态链路速率（Shannon/MCS + 分级速率）— FACT，已在清单 B5，未实现

**旧平台（有完整实现）：**
- `get_data_rate`（SimulationRL.py:8295）按 FSPL 距离矩阵 → SNR → MCS 门限表量化成每对卫星速率；
- `RFlink`（:1798-1811）封装 f/B/maxPtx/口径/指向损耗/噪声，G/No/GoT 派生量；
- `edge` 类（:2472-2495）带 `dji/dij/shannonRate/dataRateOG`；
- GSL 动态速率：`Gateway.adjustDataRate`（:2887）、`Satellite.adjustDownRate`（:2361，按当前斜距重算 MCS 速率）、`getGSLDataRates/getISLDataRates`（:5038/5052）；
- `los_slant_range`（:8282）把超门限距离置 inf（不可用）。

**新平台：**
- 链路速率为固定配置常数：`uplink_rate_mbps/downlink_rate_mbps/isl_rate_mbps`（config.py:217/233，kernel.py:682-684），
  传输时长一律 `dur = bits / rate_bps`（kernel.py:307/556）。
- 没有任何距离依赖的分级速率；`LINK-BUDGET-DESIGN-20260816.md` 只写了设计稿 + 表征测试，
  **集成代码尚未落地**（台账 B5）。

**影响判断**：距离→速率→时延 / 拥塞 / 信息的物理链被切断。E1 已发现接入侧瓶颈，速率建模直接影响信息年龄主线结论。
**代价**：实现本身已有表征测试钉死旧数值（test_link_budget_characterization.py），改动集中在服务时长三处采样点，风险可控。
**建议**：按 LINK-BUDGET 设计稿落地 rate_model=constant|mcs（默认 constant 不破既有回执）。

### D2 动态星间拓扑重匹配（星座移动后重建 ISL 邻居对）— FACT，新发现

**旧平台：**
- `moveConstellation`（SimulationRL.py:5183）每 `deltaT`（默认 3600s）重建 graph；
- `markovianMatchingTwo`（:8330）/ `greedyMatching` 用贪心/Markovian 二分匹配重新确定跨平面 ISL 连接对；
- `updateSatelliteProcessesRL/Correct`（:4504/:4092）把在途/排队的数据块按到达时间重新分配到新的 ISL 缓冲，
  停掉失效 ISL 进程、为新邻居建缓冲，处理路径拼接（块路径被 splice 成旧+新）；
- ISL 邻居集合**随时间改变**，且每对有一个独立 `RFlink` 计算的 `shannonRate`。

**新平台：**
- `Constellation.neighbors`（model.py:503-515）：N/S 同面相邻、E/W 固定同 index 的相邻平面卫星；
  `topo` 只在 kernel 初始化时建一次（kernel.py:703 `build_topology`），之后永不重建；
- 变化的是每条链路的**可用性**（`isl_available` 地球遮挡/最大距离，model.py:529），而不是**连接到的对端是否改变**；
- 控制平面广播树 `control_children` 也一次建好，邻居集合静态。

**影响判断**：真实 Walker 星座跨平面链在长时窗会因相对漂移而发生「接缝」重匹配，对端会变。
新平台把它简化为「同一对固定邻居、仅可用/不可用」，在 ≤5s 的论文仿真窗内基本无差异
（旧平台 3600s 才动一次，5s 窗内从不触发，见 temporal_encoder.py 注释）。
但若研究延伸到大时窗 / 长时间信道统计，这是真实的物理保真缺口。
**判定**：`FACT`（代码明确差异）+ `INFERENCE`（当前论文窗是否受影响需按窗长评估）。
**是否值得迁**：中。若要迁，方式是给 `topo` 按时间片提供「对端重匹配」事件，属承重改动需独立复核。

---

## 3. 观测 / 特征构建层

### D6 per-action / 逐方向链路特征进观测 — FACT，图合同部分缺失

**旧平台 RAAC 图观测**（`getDeepStateRAACGraph`，SimulationRL.py:9791）：
- 除节点特征/邻接/readout 外，额外有 **action_feats（4×9）**（:9823-9840）：
  `slant_range/maxSlantRange`（该方向链路斜距归一化）、`dataRateOG/B`（该方向动态速率归一化）、
  邻居→目的地 ECEF 相对向量、根→目的地 ECEF 相对向量 —— 把**每个候选方向的链路物理状态**直接喂给共享动作头。

**新平台图观测**（`build_graph_observation`，learning.py:1204）：
- 节点特征 18 维（queue/hop/degree/root/valid/readout/ECEF/access/vis/AoI）、邻接、方向 readout、own+dest；
- **没有** per-action 的链路斜距 / 链路速率 / 邻居-目的地方向向量特征；方向信息只通过 readout 掩码 + 共享 RNN 聚合表达。

**影响判断**：旧平台让决策头直接看到「每个候选方向的链路代价方向性」；新平台把它折叠进消息传播，信息等价性不显然，
且链路速率本身（D1）也不在观测里。对「信息边界 / 决策能力」对照臂可能是可观测差异。
**建议**：速率/斜距进图观测与否需按信息合同单独评审（D1 同步考虑），列为 follow-up。

### D7 M3 队列动态特征（Δq 速度 + EMA 趋势）— FACT，新发现

**旧平台**（`getDeepStateDiff`，SimulationRL.py:10041-10056，受 `SIM_M3_DYNAMICS` 门控）：
- 在观测里追加 **8 维**：自己在出 4 方向的队列速度 `Δq`（负=排空，正=堆积）+ EMA 平滑趋势；
  用于让策略区分「正在积压还是正在排空」的热点信号。
- 迁移清单把 M3 记为「未处理、全配置 off」，但**这是已设计并有实现**的特征增广臂。

**新平台**：
- `own_state`（learning.py:983）只给当前时刻占用比 + AoI，无任何队列速度/趋势项；
- 原封特性块 `[isl_queue_ratio, access_load_ratio, visible_norm, aoi_norm]` 都是瞬时值。

**影响判断**：没有时序趋势的单帧观测把「正在排空」和「静止空闲」混在一起（这正是旧平台加 M3 的理由）。
新平台的控制平面已带 AoI，但没有派生速度特征。可作为热点/拥塞趋势对照臂的候选（INFERENCE）。

---

## 4. 奖励层

（此处与前作 REWARD-DIFF 对齐：M1 队列奖励、M2 逐方向出向队列、到达奖励=50 已迁移并修好；距离/线性被 v1 排除是计划内判据。）

- 旧平台奖励分量极多样：`getQueueReward`（:10269）+ 6 个距离奖励版本 V1–V5 + potential-based shaping
  （`getDistanceRewardPotential`，:10383，Ng et al. 1999 的 γΦ(s′)−Φ(s) 策略不变塑形）+ again/unav 惩罚 + arrive。
- 新平台 v1 唯一保留 `queue`（config.py 拦截 distance/linear）。**这不是 bug，是计划排除**，但 potential shaping
  是理论上有真凭据的塑形工具，旧平台有实现、新平台没有 —— 若研究臂需要奖励塑形对照，可照旧实现迁入（INFERENCE）。
- again/unav 软惩罚 → 新平台改用**硬动作掩码 + 回环过滤**（kernel.py:1848 `cands = [d ... not in pkt.path]`、learning.py `build_action_mask`）。
  机制替代：新平台直接在决策层禁止回跳/非法方向，旧平台则是存「负惩罚经验」。二选一各有取舍，已在 REWARD-DIFF 记过，不重复。

---

## 5. 训练层

### D3 多步回报 / TD-λ / temporal（framestack/GRU）— FACT，已在清单 M2，未实现

旧平台有**完整实现**：inline n-step/TD-λ（SimulationRL.py:6980-7062，`_ms_store/_tdl_store/_tdl_flush`）+
`temporal_encoder.py`（framestack/GRU）+ `getDeepStateDiff` 的时序钩子。
新平台只有 `TEMPORAL-MULTISTEP-DESIGN-20260816.md` 设计稿，**无代码**。详见该设计稿 §6（工作量与 defer 理由）。
这不影响当前能跑通，但信用分配跨度 / 时序记忆这两个训练维度确实没有出生。

### D5 多智能体 / 每星独立模型 + 联邦学习 + CKA — FACT，新发现（重要）

**旧平台（分布式/多智能体训练能力完整）：**
- `onlinePhase=True`（:263）时每颗卫星是独立 agent（`sat.DDQNA`），另有离线共享版本（`earth.DDQNA`）；
- 联邦：`full_federated_learning`（:1499）、`federate_by_plane`（:1504）、`model_anticipation_federate`（:1518）、
  `update_sats_models`（:1540）、`perform_FL`（:1585，星座每动一次调用，moveConstellation:5296）；
- 表示相似度分析：`compute_full_cka_matrix`（:1549）、`compute_average_cka`（:1580）、`plot_cka_over_time`（:1629/1679），
  `FL_Test` 开关（:234）驱动 —— 用于追踪各星/各面模型表示是否发散（CKA 值随训练变化）。

**新平台：**
- `learning.py:373` 明文「One model is shared by all satellites（单共享策略）」；
- 无每星模型、无 FL、无 CKA（rg 全库仅 receipt/platform_check/config 里出现 "CKA" 子串的无关命中）。

**影响判断**：`FACT`（代码明确）。这是一个**研究能力层的缺口**而非 bug：若论文要做
「去中心化 / 联邦 / 每星差异性 / 表示漂移」这类分布式卫星路由对照，旧平台有现成实现，新平台完全没有。
代价/复杂度：迁移不是小活（多策略副本 + 联邦调度 + CKA 计算），且与当前「单共享策略」的并发模型不同构，
建议作为独立研究臂评估，先出设计稿再审（承重改动，AGENTS.md §13）。

### D9 回放缓冲持久化 / 续训 / 热启动 — FACT，已在清单 C3，建议升级

旧平台：`save_replay_buffer`（:10475）/ `load_replay_buffer_into`（:10492），`SIM_REPLAY_PATH` 热启动
（RunSimulation:12183），路径信用回放同样可续（:12186）；中断后可近似从中断点续训。
新平台：replay 是进程内 `deque`（learning.py:400），无保存/加载；只有模型 checkpoint（save_and_verify）。
对「一次跑好几个小时、中途崩溃就全丢经验」的长训练场景，这是实打实的韧性缺口。
已在清单 C3（低优先），**建议升级为中优先**，与 D10 的早期停止一起服务于长训练工程化。

### D10 按步长/按 GT 数的 ε 调度 + stopLoss 早期停止 — INFERENCE，新发现

**旧平台：**
- `alignEpsilon`（:7315）：`ε = min + (max−min)·exp(−LAMBDA·step/(decayRate·GT²))` —— 按**决策步数**且按 **GT 数平方**归一化，
  收敛速度对负载规模/步数有显式建模；
- `train()` 内 `stopLoss`：平均 loss 低于阈值 → `TrainThis=False`（:7559 一带），自动判定「已收敛、停止训练」。

**新平台：**
- `epsilon(now)`（learning.py:485）：`end + (start−end)·exp(−t/decay_s)` —— 按**墙钟/仿真时间**而不是决策步数衰减；
- 无早期停止机制。

**影响判断**：按时间衰减 vs 按步数衰减，在流量密度不同的 trace 下训练动力学不同（稀疏 trace 下时间衰减偏慢、密集 trace 下偏快）；
stopLoss 对长训自动收敛检测有用。属训练细节差异（INFERENCE），不一定需要照搬，但应显式记为「有意差异」而非被默认吞掉。

---

## 6. 工程韧性层

### D10b 中断安全保存（save_on_interrupt）— 已 A 类删除，记录取舍

旧平台有完整 SIGTERM 安全的 `save_on_interrupt`（:11356，含 checkpoint/meta/回放/metric）。
新平台按计划 A 类「自然结束回执 = 唯一完成形态」删除（MIGRATION-BACKLOG A 行），
这和新平台的 fail-loud/回执治理一致，是**有意取舍**不是遗漏。但要说明：代价是崩溃/中断的运行没有落盘产物，
对长训练（D9）与在线迭代不友好 —— 两者可并案重议（可做「training 中间产物的 opt-in 快照」而不破坏 formal receipt 语义）。

---

## 7. 尚未核实项（未验证）

- **D8 per-block λ 三分量报告**：旧平台 `getBlockTransmissionStats`（:1324）+ `Results`（:1756）给出
  每包 queue/tx/prop latency 及占比。新平台 receipt/ledger 有 fate/occupied/queue_area，但我未逐字段核实
  是否输出等价的「每包队列/传输/传播时延分解」指标 —— 这将影响论文指标层。若缺，需补一个 output-only 分析器。

---

## 8. 与既有台账/清单的去重对照

| 本报告编号 | 既有对应 | 处置 |
|---|---|---|
| D1 | MIGRATION-BACKLOG B5 / LINK-BUDGET-DESIGN | 已列，未实现；保持开 |
| D2 | 清单未列 | **新发现**，建议入backlog评估 |
| D3 | MIGRATION-BACKLOG M2 / TEMPORAL-MULTISTEP-DESIGN | 已列，只设计稿；保持开 |
| D4 | MIGRATION-BACKLOG M3 | 已列，未迁移；保持开 |
| D5 | 清单未列 | **新发现**（FL+CKA+每星模型），建议入backlog |
| D6 | 图节点特征增广的 follow-up | 链路速率部分归 D1；方向性特征建议单列 |
| D7 | 清单未列 | **新发现**（M3 队列动态特征），建议入backlog |
| D8 | 未验证 | 需在 receipt 侧核实后判定 |
| D9 | MIGRATION-BACKLOG C3(低) | 已列；建议升级中优先 |
| D10 | 清单未列 | **新发现**（训练调度差异），记有意差异或入backlog |

---

## 9. 下一步建议（按性价比）

1. **落 D1 速率模型**（表证已就位，只缺接线）→ 直接服务于信息年龄主线，收益最确定。
2. **D5 分布式/FL/CKA 出独立设计稿**（不动单共享策略默认路径）→ 打开分布式论文臂，成本为承重评审一次。
3. **D9 回放持久化升级为公共长训基础设施**（配合正式 receipt，opt-in 快照）→ 让长训练可续、可救。
4. **D2/D6/D7/D8/D10 记 follow-up**：D2 需先定长时窗范围；D6/D7 需按信息合同评审；D8 先在 receipt 侧核实；
   D10 显式记「时间衰减 = 有意差异」。

> 本报告只做设计审计与建议，未改动任何平台代码。是否实现 / 以何优先级，等三方（Codex/Kimi/GPT）交叉审阅与用户拍板。
