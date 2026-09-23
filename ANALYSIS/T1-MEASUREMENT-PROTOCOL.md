# T1 测量与反事实协议（leased from 2026-09-23 分层审查）

> **CURRENT-CONTRACT**；最后核验：2026-09-23。本文定义 T1（邻居状态时间错位 / 候选到达时刻对齐）研究所需的测量与反事实能力契约与五个门禁的验收标准。它**不授权任何实验**：正式运行仍须走编译 → 独立三角色审阅 → 授权 → clean-main 部署 → 自然结束回执 → 分析重算。

## 1. 来源与范围

本文条款来自 2026-09-23 的《leo-direct-sim 平台分层审查报告》，并经 2026-09-23 的实测复核（见 `CURRENT-EXPERIMENT-READINESS.md` 的 2026-09-23 节）。审查结论：

- 平台的数据平面 / SimPy 事件、控制平面 / AoI、信息泄漏控制与正式证据链**足以承担 T1 研究，不需要重写模拟器**；
- 真正缺的是**与这个新因果问题对应的测量能力和反事实能力**，共五类，对应五个门禁。

范围边界：本文只覆盖 T1 的**平台能力**。论文问题候选、claim 冻结与统计设计不在本文内。

## 2. 五个门禁

进入正式 T1 实验前必须依次通过。门禁状态以 `EXPERIMENTS/experiment-program.yaml` 的 `gates` 为准；本文只定义标准。

| 门禁 | 通过标准 |
|---|---|
| `T1-TIME-LEDGER-PASS` | 每个决策有唯一 `decision_id`；同一包的重决策可区分；第 3 节列出的 11 个时间戳可从落盘工件重建，且缺项显式标记为缺失而非静默填 0 |
| `T1-DOWNSTREAM-RESOURCE-PASS` | 对每个候选动作记录**该包到达后实际竞争的出口**（固定 downstream policy 下的具体 egress）、到达前 workload、在服务剩余量与控制积压；不再用「邻居全部方向求和」代替 |
| `T1-COUNTERFACTUAL-REPLAY-PASS` | 存在严格配对的反事实 harness：同 immutable trace / config / seed 重放到同一 decision，校验 pre-branch state hash，只强制改变目标包这一次动作；**不得** deepcopy SimPy 环境，**不得**从原轨迹读取未选候选的未来状态 |
| `T1-COMPUTE-DELAY-PASS` | 决策计算时延进入模拟时间：`decision_start → yield timeout(delay) → revalidate → commit`；默认关闭，关闭时语义与现行为等价 |
| `T1-PRESSURE-WINDOW-PASS` | 存在可解析的 ISL 压力窗口（固定 OD corridor / hotspot、access 不限流、constant PHY），且能量化其有向 ISL 利用率量级 |

## 3. `T1-TIME-LEDGER-PASS` 设计

### 3.1 现状（实测，`8a30409`）

- `_decide` 位于 `CODE/leo_sim/kernel.py:3274-3437`，**区间内 `yield` 计数为 0**：观察、选择、提交发生在同一个 `env.now`。
- 全仓 `decision_id` grep **0 命中**；decision sink 的行使仅以 `(t, pid, sat, kind)` 为键（`kernel.py:3168-3184`）。同一包的多次重决策（`_redecide_pending` `3439-3444`、`_redecide_cell_pending` `2762-2782`）在流中不可区分。

### 3.2 需要的 11 个时间戳

`t_measure`、`t_control_rx`、`t_decision_start`、`t_decision_commit`、`t_local_queue_enter`、`t_service_start`、`t_service_finish`、`t_peer_arrival`、`t_peer_redecision`、`t_peer_target_egress_enter`、`t_peer_target_egress_service_start`。

在 `T1-COMPUTE-DELAY-PASS` 落地前，`t_measure = t_decision_start = t_decision_commit` 三者相等；此三元组在三者相等时**必须仍然分别记录**，不得折叠成一个字段，否则该门禁落地后无法回填语义。

### 3.3 落位决策：只扩展 `info_audit`，不新增 config key

这是本设计最重要的一条，理由来自实测的身份绑定链：

1. `config_sha256` 是对**整份 merged config** 的 canonical JSON 求 SHA（`CODE/leo_sim/config.py:970-976`）。**任何新 config key（哪怕纯输出用）都会改变所有配置的 `config_sha256`**，从而让已编译的 planned-run 行与既有授权失效（`CODE/experiment_platform/authorize_experiment.py:338-339`）。
2. 只往 `info_audit` 里加字段则 `config_sha256` 与 trace identity 都不变；`code_sha256`（对 `CODE/leo_sim/*.py` 逐个求 SHA，`CODE/leo_sim/receipt.py:124-131`）必然改变——这是任何 kernel 改动的固有代价，且是正确的：代码确实变了。
3. decision log 工件**不在 receipt / ledger 信任链内**（不在 `receipt.RECEIPT_KEYS` 与 `LEDGER_KEYS` 中），没有行键白名单。

因此：**T1 时间账本一律实现为 `info_audit` 的纯输出扩展，不引入任何新 config key。**

### 3.4 不改动 `packet_events`

`self.packet_events` 参与 receipt 重算与 `_validate_v2_event_authority`；往事件里加键有破坏既有回执验证的风险。**本次不改 `packet_events`、不改 `congestion_metrics`、不改任何 ledger 顶层键**。里程碑只写入 caller-supplied 的 `decision_sink`。

### 3.5 `decision_id` 语义

- 单调递增整数，由 `Kernel` 持有；**仅在 `decision_sink is not None` 时分配**。
- 分配点在 `_decide` **入口**，使 hold / fail 等未提交尝试（以及随后的重决策）也可区分——这正是 `(pid, t, sat)` 现在做不到的事。
- 提交（forward 或 deliver）时把该 id 记到包上（`DataPacket` 新增 slot），供后续里程碑归属。
- 默认关闭时（`decision_sink is None`）**不分配、不写、不新增热路径分支**：`_record_decision` 的 `if self.decision_sink is None: return`（`kernel.py:3154-3155`）保持为第一道早退。

### 3.6 里程碑的落盘形式

decision sink 是 append-only 流（`_DecisionLogWriter` 逐行写 JSONL）。因此下游时间戳**不能**靠回填既有行，而应以独立里程碑行追加，每条携带 `decision_id`、`pid`、`milestone`、`at`、`sat`；由纯后处理函数折叠成每决策的 11 字段链。后处理放在独立模块，不进入 kernel 热路径。

### 3.7 等价性要求与验证方法

关闭时（默认）必须与旧行为**逐位等价**。按「先记录旧版数值、再在新版重跑同一检查」验证：

1. 改前在基线 `8a30409` 上固定 config + seed 跑一次，记录 receipt SHA、artifact manifest SHA、trace SHA、`fate_counts`、`totals`、`occupied`、`queue_area_bits_s`；
2. 改后用同一 config + seed 重跑，逐项比对上述全部值必须完全相同；
3. 既有 `tests/test_decision_snapshot.py::test_decision_sink_does_not_change_behavior`（断言 fates / totals / deliveries / occupied / queue_area_bits_s / access / service_log / events_processed 相同）必须继续通过；
4. 新增测试：sink **打开**时上述集合仍与 sink 关闭时相同，且里程碑行不改变任何 fate。

### 3.8 验收证据

- 新旧对照的逐项数值记录（写入 PR 正文，不写入库内文档）；
- 全量测试通过的真实计数；
- `decision_id` 唯一性与「同一包多次重决策可区分」的定向测试。

### 3.9 已知语义边界（消费方必读）

独立复核（2026-09-23）与自审后确认的边界，下游分析不得越过：

1. **`t_control_rx` 在非学习运行中是"可能已知"而非"实际使用"**。学习运行按 contract 裁剪 cache 条目；非学习运行没有 contract 可裁，因此记录该节点**全部有效 cache 条目**中最新的 `received_at`（`mapping_status` 仍为 `truth_audit_not_learner_tensor`）。对**从不读 cache 的确定性路由**而言这是一个反事实上界，**不得**读作"路由实际使用的那个值"。
2. **"每个 id 都有归属"这条不变量只在挂载 `timeline_sink` 时成立**。只开 `decision_sink` 时，hold/fail 消费的 id 不落任何记录，于是 sink 中的 id 是稀疏的（例如 14 个已分配 id 只有 2 个出现在决策行里）。需要完整 id 账目时必须同时挂 timeline。
3. **`t_local_queue_enter` 取该决策名下第一条 `queue_enter`**。提交型决策自身的入队必然早于其后任何重新入队，故该字段稳定；但**按 `decision_id` 索引的"全部入队"集合**只包含归属于该决策的那些——链路 stall/退休造成的重新入队不归属任何决策（`decision_id` 为 `None`），这是刻意的（见 R8-A8）。
4. **`t_measure` / `t_decision_start` / `t_decision_commit` 当前恒相等**，三字段分开保留是为 `T1-COMPUTE-DELAY-PASS` 落地时回填，不得据此认为已测量决策时延。

## 4. 其余门禁的设计要点

- **`T1-DOWNSTREAM-RESOURCE-PASS`**：`peer_egress_queue_bits`（`kernel.py:3218-3220`）是邻居全部方向 data+ctrl 求和，不代表包到达后实际进入的队列。真正对应的是同处的 `reverse_link_queue_bits`（`3212-3217`）。需要新增的是**候选动作级**、固定 downstream policy 下的具体 egress、到达前 workload、在服务剩余量与控制积压。保留旧字段以免破坏既有消费方，但必须在文档与 schema 中标注其语义边界。
- **`T1-COUNTERFACTUAL-REPLAY-PASS`**：从相同 immutable trace / config / seed 重放到同一 decision，比对 pre-branch state hash 后只改目标包这一次动作；第一版限定 deterministic router、GE off、learning off。
- **`T1-COMPUTE-DELAY-PASS`**：默认关闭的 `compute_delay_s`；旧实验默认为 0 以保持语义兼容。注意引入 config key 会改变 `config_sha256`，须与重新编译、重新授权一并规划。
- **`T1-PRESSURE-WINDOW-PASS`**：现有 `EXP-20260829-GLOBAL-PRESSURE-BRACKET-R02` 在 10/20/40/80 Mbps 下无可饱和有向 ISL、无持续 hotspot（80 Mbps 的 1 s active-window p99 utilization 约 0.5%，最大约 1%），**不能充当 T1 主压力场景**；须另建固定 OD corridor / hotspot、access 不限流、constant PHY 的可解析场景。

## 5. 明确不做

- 不重写模拟器；不替换 SimPy。
- 不 deepcopy SimPy 环境做反事实；不从原轨迹读取未选候选的未来状态。
- 不加"转发效率"这类与物理带宽混淆的旋钮：`isl_rate_mbps` 已是链路带宽，若用同一参数表示"转发效率"，F2 与 F3 会退化成同一个实验。F2 必须定义为独立于 PHY 带宽的节点处理/调度开销。
- 不在本文授权任何运行。
