# 旧平台说明书（SimulationRL.py + 依赖模块）

> 本卷由主脑 Codex 独立通读产出，与 Kimi 的独立产出（见 prompt-for-kimi.md）交叉对照。
> 状态：分多轮推进中。本文件只陈述代码事实，标注 `文件:行号`；不做迁移/优劣判断。

## 0. 阅读范围与统计

- 主文件：`CODE/SimulationRL.py`，12556 行。
- 依赖本地模块（SimulationRL.py import）：`traffic_od.py`(442)、`traffic_burst.py`(194)、
  `traffic_diurnal.py`(382)、`traffic_mlab.py`(325)、`link_outage.py`(197)、
  `routing_mappo.py`(631)、`routing_multistep.py`(138)、`routing_path_credit.py`(1418)、
  `temporal_encoder.py`(272)、`legacy_trace_runtime.py`(138)、`monitor.py`(284)、
  `runtime_effect_receipt.py`(待补)。

## 1. 全局常量与配置（SimulationRL.py 顶部）

- `GTs = [4]`（`SimulationRL.py:276`）：被测网关数量，默认 4，可经 `SIM_GTS` 环境变量扫多值。
- 奖励权重（`:270-272, :579-584`）：
  - `w1 = 20`（`SIM_W1`）：队列奖励（reward 得到空队列）。
  - `w2 = 20`（`SIM_W2`）：距离奖励。
  - `w4 = 5`：距离奖励归一化分母。
  - `ArriveReward = 50`：送达奖励。
  - `againPenalty = -10`：跳到已访问过的 hop 的惩罚。
  - `unavPenalty = -10`：选无可达链路方向的惩罚。
- `movementTime = 10`（`:239`）：每 10 秒更新卫星位置并重建图。
- 学习率：`alpha = 0.25`（Q 表）、`alpha_dnn = 0.01`（DNN）（`:558-559`）。
- 队列观测：`infQueue = 5000`、`queueVals = 10`（`:573-574`）。

## 2. 物理链路层

### `class RFlink`（`SimulationRL.py:1798`）

职责：射频（RF）链路预算计算。FACT：构造时用频率、带宽、发射功率、收发天线直径、
指向损耗、噪声系数、噪声温度，算出天线增益 Gtx/Grx、总增益 G、噪声功率 No、G/T，并保留
`min_rate`。INFERENCE：`min_rate` 是最小保证速率下限。`__repr__` 只做文本展示。
依赖：全局物理常数 `eff`（天线效率）、`Vc`（光速）、`k`（玻尔兹曼常数）。

### `class FSOlink`（`SimulationRL.py:1827`）

职责：自由空间光（FSO）链路参数容器，只存 `data_rate/power/comm_range/weight`，无计算。
FACT：旧代码主数据路径实际用的是 RFlink（卫星间 ISL 与 GSL 都构造 RFlink），FSOlink 仅作
参数模型存在，未见热路径调用。

## 3. 星座几何层

### `class OrbitalPlane`（`SimulationRL.py:1842`）

职责：一个轨道面。构造时按 Walker 参数算轨道周期 `period`、轨道速度 `v`，由最小仰角
`min_elev` 推出最大地心角 `max_alpha`、最大星视角 `max_beta`、最大服务地面距离
`max_distance_2_ground`。按 `n_sat` 生成该面所有 `Satellite`。

- `rotate(delta_t)`（`:1876`）：地球自转引起的经度漂移 + 逐卫星调用 `sat.rotate`。

### `class Satellite`（`SimulationRL.py:1891`）

职责：单颗卫星。核心状态：球坐标 `r/theta/phi`、笛卡尔 `x/y/z`、`latitude/longitude`、
倾角、`quota/power`；GSL 侧 `ngeo2gt`（一个 RFlink）、`downRate`；以及多组发送缓冲
`sendBufferGT / sendBufferSatsIntra / sendBufferSatsInter`；学习侧 `QLearning / DDQNA`。

关键方法：
- `GetmaxSlantRange`（`:1963`）：由最小仰角 + 高度算最大覆盖斜距。
- `outbound_queue_len_for_neighbor`（`:1975`）：给某邻居的出口队列长度（供状态/奖励用）。
- `receiveBlock`（`:2017`，SimPy 进程）：等待传播时延 `propTime` 后，把 block 加入正确
  发送缓冲；同时在此处为 Q-Learning/DDQN 选下一跳、更新 `block.QPath`、记队列长度与
  replay 事件。若 `block.path == -1` 则记 fate 丢包（`:2033-2036`）。
- `sendBlock`（`:2185`，SimPy 进程）：监控某条链路（GSL 或 ISL）的发送缓冲，按块大小/
  速率算传输时延，处理 `_link_outage` 的中途断链丢包（`:2269-2290`），再触发接收方
  `createReceiveBlockProcess`。含星座移动后重建 buffer 引用的 `newBuffer` 逻辑。
- `adjustDownRate`（`:2361`）：用香农公式 `shannonRate = B*log2(1+SNR)` 配合查表
  （谱效率 vs 线性 SNR 阈值）算出下行速率 `downRate`。
- `timeToSend`（`:2392`）：`距离/Vc` 算传播时延。
- `findIntraNeighbours`（`:2400`）：同轨前后星（`upper/lower`）。
- `findInterNeighbours`（`:2411`）：由 `earth.graph` 边 + `getDirection` 找东西向邻星
  （`right/left`）。
- `rotate`（`:2439`）：推进 `theta/phi`，重算笛卡尔坐标与经纬度。

### `class edge`（`SimulationRL.py:2472`）

职责：图边，存 `slant_range`、`dji/dij`、`shannonRate`，`__cmp__` 供排序。

### `class DataBlock`（`SimulationRL.py:2497`）

职责：被路由的数据块实体。FACT：含 `source/destination/ID/creationTime`，记录
`getQueueTime/getTotalTransmissionTime`，并在路径 `checkPoints/checkPointsSend` 上累计
队列/传输时延。后续章节补路由、学习、流量、诊断各层。

## 4. 地面接入层（Gateway / Cell / Earth）

### `class Gateway`（`SimulationRL.py:2573`）

职责：地面网关（concentrator），**同时是业务源、业务宿、地面接入汇聚点**。旧平台
数据路径的「业务端点」就是它：`fillBlock` 造块 → `sendBlock` 上行到卫星 →
卫星间转发 → 目的网关 `receiveBlock` 收块。这是 V2 要替换掉的核心假设。

关键状态：`name/ID/latitude/longitude`、`gridLocationX/Y`、`cellsInRange`、`totalGTs`、
`totalAvgFlow`、笛卡尔坐标、`linkedSat=(dist,sat)`、`graph`(nx.Graph)、`sendBuffer`、
`paths`（目的→路径字典）、`gs2ngeo`（一个 RFlink，GSL 上行 30GHz/500MHz/20W）、
`dataRate`。

关键方法：
- `makeFillBlockProcesses`（`:2629`）：为每个目的网关各启动一个 `fillBlock` 进程。
- `fillBlock`（`:2681`，SimPy 进程）：循环创建 `DataBlock`，用 `timeToFullBlock`
  算填充时长，`yield timeout` 后 `_record_filled_block` + `_enqueue_filled_block`。
  目的网关暂时无链接卫星时先缓存（`unavailableDestinationBuffer`），有链接再排空。
- `_record_filled_block`（`:2642`）：封块时记录 `timeAtFull`、加入 `createdBlocks`。
- `_enqueue_filled_block`（`:2657`）：解析路径、写入 `block.path`，加入上行 `sendBuffer`。
- `sendBlock`（`:2718`，SimPy 进程）：等卫星链接，算传播/传输时延，处理 `_link_outage`
  中途断链丢包（`:2759-2772`），再触发卫星 `createReceiveBlockProcess`。
- `receiveBlock`（`:2835`，SimPy 进程）：等传播时延后把块加入 `receivedDataBlocks`，
  记 `_append_packet_fate_log(status=0)`（送达）。
- `adjustDataRate`（`:2887`）：香农公式 `shannonRate = B*log2(1+SNR)` 配合谱效率查表，
  算出上行 `dataRate`（与 `Satellite.adjustDownRate` 同构）。
- `orderSatsByDist`（`:2918`）：按 GSL 距离排序可见卫星。
- `addRefOnSat`（`:2935`）：贪心给网关分配卫星（一星一网关）。
- `link2Sat`（`:2972`）：建立网关↔卫星链接并 `adjustDataRate`。
- `findCellsWithinRange`（`:2998`）：由网关位置向外扩散找覆盖范围内的小区。
- `timeToFullBlock`（`:3130`）：由 OD 权重矩阵（含 burst 时变乘子 + diurnal 日变乘子）
  + 指数分布算块填充时间；无 OD 矩阵则均分流量。
- `getTotalFlow`（`:3193`）：由覆盖小区用户数（Step/Slope 两种距离衰减）算总平均流量。

### `class Cell`（`SimulationRL.py:3260`）

职责：地面网格单元。状态：`map_x/map_y`、`latitude/longitude`（弧度）、`area`、
笛卡尔坐标、`users`（人口）、`gateway=(gateway,distance)`。

- `setGT`（`:3300`）：找最近网关，若距离 ≤ `maxDistance` 则把自己加入该网关
  `cellsInRange`，否则 `users=0`。

### `class Earth`（`SimulationRL.py:3322`）

职责：整个仿真环境/地球模型。FACT 核心职责：读人口 TIFF 建 `cells` 网格；读
`Gateways.csv` 建 `gateways`；初始化流量配置（trace/OD/burst/diurnal）、链路中断
`_link_outage`、path-credit replay；建立星座 `self.LEO`；持有全部诊断 log 列表。

关键状态（`:3330-3450` 附近）：`cells`、`gateways`、`LEO`、`graph`、`lostBlocks`、
`queues`、`replay_events`、七类诊断 log（`decision_log/reward_log/train_log/
link_snap_log/packet_fate_log/eval_curve/state_log/graph_state_log/encoder_log`）、
运行时效果计数器（`_critic_train_successes`、`_pc_train_successes`、`_fast_train_steps`、
`_infer_backends_effective`、`_burst_multiplier_calls`、`_diurnal_multiplier_calls`、
`_temporal_apply_successes`、`_stale_neighbor_reads`、`_timed_state_reads`、
`_gsl_handover_*`、`_link_outage_*`、`_pc_checkpoint_loads` 等）。

关键方法：
- `__init__`（`:3322`）：读人口 TIFF → `cells`；读 `Gateways.csv` → `gateways`；
  初始化 `_link_outage`（`link_outage.load_link_outage_schedule_from_env`）、`pc_replay`
  （`routing_path_credit.PathTrajectoryReplay`）、流量 OD 矩阵（uniform/h2/gravity/
  mlab/trace 分派）、burst 与 diurnal schedule；`create_Constellation` 建星座；
  启动 `moveConstellation` 进程。
- `startTraceTraffic`（`:3676`）：`legacy_trace_runtime.load_and_project_trace` 读外部
  不可变 trace，投影到真实 Gateway 上行（`_dispatchTraceRows`），关闭内生 Gateway 造块。
- `_dispatchTraceRows`（`:3710`）：按 emit_time 顺序把 trace 行转成 `DataBlock` 注入。
- `linkCells2GTs`（`:3763`）：对所有网关跑 `findCellsWithinRange`，再把小区挂到最近网关。
- `linkSats2GTs`（`:3791`）：网关↔卫星链路分配，`method="Greedy"`（逐网关贪心）或
  `method="Optimize"`（`linear_sum_assignment` 最小化总代价）；`keep_stable=True` 时
  同星保留不重建。
- `getCellUsers`（`:3867`）：（后续继续）

## 5. ISL 建链层（图匹配 + 链路预算）

### `los_slant_range`（`:8282`）
职责：把超过最大可视斜距的星间距离置为 `inf`（按轨道面对的最大斜距矩阵 `_max` 过滤）。

### `get_data_rate`（`:8295`）
职责：给定斜距矩阵 + `interISL`（RFlink），用香农公式 `shannonRate = B*log2(1+SNR)`
配合谱效率查表，算出星间数据速率矩阵 `speffs`。FACT：旧平台 ISL 容量是物理链路预算
算出来的，不是固定常量。

### `markovianMatchingTwo`（`:8330`）
职责：Markovian 匹配建 ISL。每个卫星两个 inter-plane 收发器，按斜距贪心配对
（`covered` 集合保证每个收发器只用一次），再加同轨上下邻居（intra-ISL）。注释声明
「非最优但快 10–1000 倍」。

### `greedyMatching`（`:8438`）
职责：贪心建 ISL。每星连同轨上下邻居 + 异轨东西方向最近邻（按 `Positions` 东西判定）。
同样用 `get_data_rate` 算 Shannon 速率。

### `deleteDuplicatedLinks`（`:8539`）
职责：去重东西向重复链路，保留纬度差更小（更水平）的一条。

### `establishRemainingISLs`（`:8580`）
职责：对缺右/缺左邻居的卫星，按纬度差从小到大补建水平链路。

### `createGraph`（`:8655`）
职责：建 `nx.Graph`——卫星节点 + 已链接的 Gateway 节点（GSL 边）+ ISL 边。每条边带
`slant_range / dataRate(1/rate) / dataRateOG(rate) / hop / dij / dji`。建完去重、补链、
更新每星 `findIntraNeighbours/findInterNeighbours`，并对 slant_range 做 fail-closed 校验
（`_slant_range_marker` + `topology_slant_sha256`）。`matching` 参数选 `Greedy`/`Markovian`。

## 6. 路由层

### `getShortestPath`（`:8903`）
职责：Dijkstra 最短路。`weight` 可为 `dataRate / slant_range / hop /
oracle_global_dijkstra`。`slant_range` 走严格校验闭包；`oracle_global_dijkstra` 走
`_oracle_global_dijkstra_edge_weight`。返回节点路径（含经纬度），失败返回 -1。

### `_oracle_global_dijkstra_edge_weight`（`:8807`）
职责：oracle 的边权重闭包 = 传播时延 + 单块传输时延 + `queue_factor`×当前队列。
FACT：这是「全知贪心全局基线」，能读实时队列。支持 `SIM_ORACLE_VIS_K=k` 时对 k 跳外的
边用 queue=0（建模决策节点拿不到远邻拥塞信息）。

### `getDirection`（`:9266`）/ `getDirection_deprecated`（`:9233`）
职责：由两星经纬度判方向（同轨 1=上/2=下，异轨 3=右/4=左，处理经度环绕）。

### `getLinkedSats`（`:9328`）/ `getDeepLinkedSats`（`:9381`）
职责：返回某星 U/D/R/L 四方向邻居（前者遍历图边，后者直接用 `.upper/.lower/.right/.left`）。

### `getKHopNeighbors`（`:9416`）
职责：沿 `.upper/.lower/.right/.left` BFS 到 k 跳，返回 `(sat, hop, first_dir)` 列表，
供 vis-k 聚合（`SIM_STATE_MODE=c3`）按出方向池化。

### 辅助：`getDestination`（`:9309`）、`findByID`（`:9010`）、`computeOutliers`（`:9020`）、
`hasBadConnection`（`:9193`）、`getSatScore`（`:9204`）、`getDeepSatScore`（`:9228`）、
`linkedSatsList`（`:9298`）

职责：分别为——取目的网关所连卫星、按 ID 找卫星对象、算斜距/速率离群阈值、判弱链路、
算发送分数（低斜距+高吞吐+低队列=0，高队列=2）、队列打分、列网关↔卫星链接表。

## 7. 队列观测与「信息年龄」近似

### `getQueues`（`:9050`）
职责：读某星 U/D/R/L 四方向发送队列长度。缺队列或无双链路按 `infQueue`（高队列）处理。
`DDQN=True` 返回 `{U,D,R,L}` 字典，否则返回是否超阈值布尔。

### `getStaleQueues`（`:9100`）
职责：**旧平台的「信息年龄」近似**。`delay>0` 时用每星 ring-buffer 返回 `delay` 步前的
旧快照，模拟周期性广播的年龄代价。FACT：注释明说「不改 SimPy 事件循环」——即不是真实
控制包，只是把历史快照延迟给 agent 看。

### `timedQueueSnapshotProcess`（`:9138`）+ `getTimedObservedQueues`（`:9152`）
职责：物理仿真时钟定时采样全星座队列，观测时取「采样时刻 + 最短路径传播时延 ≤ now」
的最新快照。FACT：这是比 stale-steps 更接近真实的「定时采样 + 传播时延」模型，但注释
明说「Bandwidth contention is intentionally outside this minimal model」——仍无真实控制包占带宽。

### `getObservedQueues`（`:9179`）/ `getObservedQueueRecord`（`:9183`）
职责：统一观测入口。自己看自己是 `getQueues(DDQN=True)`；否则按
`SIM_VIS_K_UPDATE_INTERVAL_S>0` 走定时采样、否则走 `getStaleQueues(delay=SIM_VIS_K_STALE_STEPS)`。
返回 `(queues, age_seconds, valid)`。

## 8. 状态/观测层（C1–C7 的旧观测合同）

这一层是「C1/C3–C7 观测合同」的旧实现，通过 `SIM_STATE_MODE` 分派，维度固定如下：

- `getState`（`:9443`）：Q-Learning 状态，5 维 = U/D/R/L 四方向 `getSatScore` + 目的
  网关所连卫星索引。
- `_temporal_apply`（`:9469`）：调用 `temporal_encoder`（`SIM_TEMPORAL_MODE`）改造状态。
- `_apply_frame_stack`（`:9499`）：MAPPO frame-stack，拼 K 帧为 `(1, K*base_dim)`。
- `getBiasedLatitude`/`getBiasedLongitude`（`:9531/9539`）：经纬度离散化。
- `getDeepStateReduced`（`:9547`）：12 维纯位置状态。

### C1 基线：`getDeepStateDiff`（`:9953`）

28 维（+ M2 4 维 + M3 8 维可选）：四方向邻居各自的 4 队列分数 + 相对经纬度（每方向
6 维）+ 自己绝对经纬度（2）+ 目的相对位置（2）。`getDeepStateDiffLastHop`（`:10061`）
额外加 1 维「上一跳卫星方向」（0/1/2/3）。

### C3：`getDeepStateVisK`（`:9566`）

固定 44 维：`getKHopNeighbors` 收集 k 跳邻居，按**首跳方向** U/D/R/L 池化，每个方向
输出「4 维队列分数 mean + 4 维 max + 直接邻居相对位置 2」，加自己绝对位置 2 + 目的
相对位置 2。k=1 时等于只看直接邻居。FACT：与 C1 的唯一差别是「1 跳邻居出队列」vs
「k 跳邻居按方向聚合」，队列特征编码相同（控制变量）。

### C2：`getDeepStateVisKFlat`（`:9914`）

朴素扁平展开：`visKFlatUnroll` 递归按 U/D/R/L 位置序展开到 k 层，每节点 4 维队列分数，
缺链接用最坏 `queueVals` 填充。维度 `visKFlatDim(k) = 4·(4^k−1)/3·4 + 4`（`:9878`），
k=1→20、k=2→84、k=3→340——这个臂存在的意义就是暴露「维度爆炸」墙，不追求胜出。

### C4/C5：`getDeepStateVisKGraph`（`:9654`）

k 跳局部 ISL 子图：节点特征 14 维（4 队列分数 + hop/度/root 标记/有效标记/首跳方向
one-hot/相对坐标）+ 有向邻接 `[MAX_N,MAX_N]` + 4 方向 readout + C3 兼容 tail。C4 用
GAT、C5 用 MPNN（`GraphMessagePassingReadout`），观测状态完全相同，只编码器不同。
`getDeepStateVisKGAT`（`:9752`）是向后兼容别名。

### C6/C7：`getDeepStateRAACGraph`（`:9791`）

带 per-node AoI/valid 的图状态：节点特征含 `observed` 标记 + 归一化 age（`age_s`），
action 分支特征（slant_range/dataRate/ECEF 相对位置），`_reachable_without_root`
（`:9770`）算「走某方向后可达的节点集」做重叠分支 readout。

### 主入口：`getDeepState`（`:10192`）

按 `SIM_STATE_MODE` 分派到上述各 builder。

FACT：旧 C1/C3–C7 的「远程状态」来自 `getObservedQueues`（stale 步延迟或定时采样），
**不是真实控制包**；新平台对应合同改从「实际到达且未过期的控制缓存」取，这是两套
观测合同最本质的实现差异。

## 9. 奖励层（多组件，含 5 个距离变体）

### `createQTable`（`:10238`）
职责：建 6D Q 表（四方向 satScore + 目的索引 + 4 动作），初值 0。这是 Q-Learning 专用。

### `getQueueReward`（`:10269`）
职责：队列奖励，三种形式——原始 `w1*(1-10^t)`（注释明说在 0–5ms 实际队列时间下数值
可忽略，有饱和 bug）、M1 fix `w1*exp(-beta*t)`（`SIM_M1_FIX=1`，beta=200）、线性
`-alpha*t`（`SIM_REWARD_LINEAR`）。

### 距离奖励（5 个变体）

- `getDistanceReward`（`:10296`）：`w2*((2*TSLa - TSLb)/TSLa - 1)`，奖励靠近目的地。
- `getDistanceRewardV2`（`:10314`）：用「到目的地的斜距减少 / 邻居平均斜距」归一。
- `getDistanceRewardV3`（`:10345`）：用「斜距减少 / 所有邻居里最大斜距减少」归一。
- `getDistanceRewardV4`（`:10366`）：`w2*(SLr - TravelDistance/w4)/biggestDist`。
- `getDistanceRewardV5`（`:10378`）：`w2*SLr/1e6`（纯斜距比例）。
- `getDistanceRewardPotential`（`:10383`）：potential-based shaping（Ng 1999），
  `F = gamma*Phi(s') - Phi(s)`，`Phi = -slant_range/biggestDist`。

### `getSlantRange`（`:10261`）
职责：两星三维欧氏斜距。

FACT：旧奖励 = `queue(w1=20) + distance(w2=20, 6 种公式) + arrive(+50) + again(-10) +
unav(-10) + path_credit(-10)`，正负混合、尺度几十；这是第 1 节已列权重的函数实现。

## 10. 学习/训练层

### `class hyperparam`（`:6183`）
职责：超参数容器（learning rate、epsilon、gamma、batch size、动作数、Q 表路径等）。

### `class QLearning`（`:6329`）
职责：Q-Learning agent。`makeAction`（`:6340` 附近）按 ε-greedy 选动作、更新 Q 表；
`alignEpsilon` 随步数衰减 ε。这是计划书明确要删的旧算法。

### `class DDQNAgent`（`:6775`）
职责：Double-DQN agent（旧平台核心学习器），每星一个实例（或共享）。关键方法：
- `_infer`（`:6910` 附近）：前向算 Q 值。
- `getNextHop`（`:7019` 附近）：按 mask 选下一跳（explore/exploit）。
- `makeDeepAction`（`:7077`）：**奖励组合的核心**，见下方「奖励组合」小节。
- `train`（`:7452` 附近）：从经验回放采样、算 TD target、更新网络。
- `createModel`（`:6940` 附近）/ `_create_graph_model`（`:6970` 附近）：建 DNN 或图编码器模型。
- `alignQTarget`（`:6948` 附近）：硬/软更新 target 网络。
- `_build_fast_train_fn`/`_fast_train_step_call`（`:7450` 附近）：tf.function 编译的快速训练步。

关键实现细节：
- `_build_fast_train_fn`（`:7452`）：编译训练步，**含 `true_ddqn` 开关**——`true_ddqn=1`
  时用 online argmax + target evaluation（真 Double-DQN），否则 `reduce_max(masked_target)`
  （退化 max-DQN）。这是计划书第 3 节明确要「删除开关、固定 canonical DDQN」的源头。
- `_ms_store`/`_ms_flush_lost`（`:6980` 附近）：n-step 多步回报存储（`SIM_NSTEP`），
  滑窗累加 `gamma^i·r_{k+i}`，终态整体 flush。
- `_tdl_store`/`_tdl_flush`（`:7033` 附近）：TD(λ) 回报存储（`SIM_TDLAMBDA_ON`），
  调用 `routing_multistep.lambda_return_transitions` 算前向 λ-return。

### 奖励组合（`makeDeepAction`，`:7177-7301`）

FACT，旧平台的奖励是**多组件加权和**：

- 到达目的网关：`reward = distanceReward + queueReward + arriveReward(+50)`（`distanceRew`
  按 1–5 选不同距离公式，`queueReward` 由 `getQueueReward` 算，`arriveReward=50`）。
- 正常转发：`again = againPenalty(-10)` 若重复访问否则 0，`reward = distanceReward +
  again + queueReward`。
- 首跳（上一跳是 Gateway）：`reward = 0`。
- `unavPenalty(-10)` 用于选无可达方向（`:6420-6433` 初始化处）。

这是第 9 节列出的「全套奖励」的实际组合位置。新平台把这套砍成了单队列 + deliver。

### `class GraphMessagePassingReadout`（`:6938` 附近，Keras Layer）
职责：GAT/MPNN 图消息传递读出层（`_gat_layer`/`_mpnn_layer`/`_reliability_weights`），
供 C4/C5/RAAC 图状态使用。这是后来迁入 V2 `learning.py` 的 `V2GraphEncoder` 的旧版。

### `class ExperienceReplay`（`:7789`）
职责：经验回放缓冲。`store`/`getBatch`/`getArraysFromBatch`，支持带 global/aux 状态的批次。

### 联邦学习（`:1484-1755`）
职责：`full_federated_learning`/`federate_by_plane`/`model_anticipation_federate`/
`update_sats_models`/`compute_full_cka_matrix`/`perform_FL`——按轨道面或全局聚合模型权重、
算 CKA 相似度、画 CKA 曲线。FACT：这一整套在新平台 `leo_sim` 中无对应。

### 星座移动与 MBB 切换（Earth 方法，`:5063-5246`）
职责：`moveConstellation`（`:5240` 附近）周期移动星座并重建图/链路；
`_apply_mbb_gsl_handover`（`:5142`）做 make-before-break GSL 切换（新星已链、旧星下行
先排空再退休）；`_drop_handover_blocks`（`:5063`）处理无排空路径的切换丢块；
`_gsl_in_range`/`_retire_old_gsl_downlinks` 辅助。`linkSats2GTs(method, keep_stable=True)`
同星保留不重建（`:3791`）。

`moveConstellation` 完整流程（`:5240` 附近）：`linkSats2GTs("Optimize", keep_stable)`
→ 可选 `_apply_mbb_gsl_handover` → `temporal_encoder.reset_satellite`（拓扑变了重置 GRU
隐藏态）→ `createGraph` 重建图 → `updateSatelliteProcessesRL/Correct` →
`updateGTPaths` → 若 `FL_Test` 则 `perform_FL` + CKA。另 `updateSatelliteProcessesSimpler/
Correct/RL`（`:3900` 附近）在星座移动后重建发送进程；`getGSLDataRates/getISLDataRates`
（`:3950` 附近）重算 GSL/ISL 速率。

## 11. 流量模型（traffic_* 依赖模块）

- `traffic_od.py`（442 行）：OD 权重矩阵，模式 `uniform/h2/gravity/gravity_corridors`。
  fail-loud：h2 缺 sources/dests、gravity_corridors 缺 corridors、名字不匹配网关都 raise，
  不静默回落。`build_od_matrix_for_gateways` 是入口。
- `traffic_burst.py`（194 行）：`BurstSchedule`，事件驱动的时变突发乘子
  （`t_ramp_up/t_hold/t_ramp_down/multiplier`），叠在静态 OD 权重上。
- `traffic_diurnal.py`（382 行）：`DiurnalSchedule`，24h 日变乘子（每源网关本地时相位），
  曲线来自 M-Lab `hour_utc` 经验聚合或正弦合成；时间压缩模型「1 sim 秒 = 24h/sim_duration」。
- `traffic_mlab.py`（325 行）：M-Lab Speedtest CSV → 行归一 OD 矩阵（adapter 层），
  城市投影到最近网关，`weight = sample_count×mean_throughput`。

## 12. 链路中断（link_outage.py，197 行）

职责：**Gilbert-Elliott 两状态马尔可夫中断调度器**（`LinkOutageSchedule`）。每类链路
（`gsl_uplink/gsl_downlink/isl`）有 good/bad 两态、指数驻留时间，中断区间按 run seed
派生私有 RNG 惰性生成。FACT：旧平台的中断在这里（主文件 `SimulationRL.py` 通过
`load_link_outage_schedule_from_env` 接入，见 Earth.__init__）。注释明说「是突发/中断
抽象，不是校准过的 Starlink 模型」。

## 13. 路由/学习扩展（routing_* / temporal_encoder）

- `routing_mappo.py`（631 行）：Recurrent MAPPO + Centralized Critic + Backpressure
  Prior。类：`BackpressurePrior`、`FrameStackHelper`、`MAPPORolloutBuffer`、
  `RecurrentMAPPOAgent`、`FrameStackBPAgent`；函数 `build_recurrent_actor`、
  `build_centralized_critic`、`build_global_state`、`ppo_clipped_surrogate_loss`、`gae_advantages`。
- `routing_multistep.py`（138 行）：纯 numpy 的 n-step / TD(λ) 多步回报
  （`nstep_transitions`、`lambda_return_transitions`），只改训练 target，不改部署策略。
- `routing_path_credit.py`（1418 行）：Path-Credit v1 辅助训练。`PathTrajectoryReplay`
  （纯 Python）+ `PathCreditMixer`/`ReturnPredictor`（TF/Keras，注意力加权逐跳 MC 回报）。
  部署时只加载 qNetwork。
- `temporal_encoder.py`（272 行）：每星时序记忆，`SIM_TEMPORAL_MODE` 支持
  `none/framestack/gru`，`apply(sat,state)` 在决策钩子改造状态。

### 详细实现

**`routing_multistep.py`**：三个纯 numpy 函数——`nstep_transitions`（n-step DDQN 回报，
内部跳用 `Σγ^i r_{k+i}` + bootstrap s_{k+n}，终跳折现到 terminal done=True）、
`nstep_transitions_streaming`（滑窗流式，与仿真内逐包窗口同语义）、
`lambda_return_transitions`（TD(λ) 前向 λ-return，`G^λ = (1-λ)Σ λ^{m-1} G^{(m)} +
λ^{T-1} G^{MC}`，λ=0→1-step、λ=1→MC）。只改训练 target，部署策略恒为 argmax Q。

**`temporal_encoder.py`**：每星时序记忆三模式。`none` 透传；`framestack` 用
`deque(maxlen=K)` 拼 K 帧（warm-start 重复首帧）；`gru` 用共享 GRU（参数共享，
`_apply_gru` 每星独立 hidden state）+ 自监督 next-frame prediction 训练（R2D2 风格
burn-in + BPTT，独立 Adam，不碰 DDQN TD 循环）。`reset_satellite` 在 ISL handoff 时清
stale 状态。`assert_not_conflicting_with_mappo` 保证与 MAPPO frame-stack 互斥。

**`routing_mappo.py`**：`BackpressurePrior` 的 BP 公式
`BP(a) = (own_q[a] − nbr_q[a]) + k_progress·progress(a) − k_loop·loop(a)`，融合
`score = znorm(Q) + beta·znorm(BP)`（Tassiulas MaxWeight）。`build_global_state` 构造
44 维 privileged 全局状态（top-K 拥塞队列 + 聚合统计 + ISL 摘要 + OD one-hot + sat
embedding）供 centralized critic 训练（部署不用）。`build_recurrent_actor` 是
GRU-based actor；`build_centralized_critic`/`build_centralized_critic_per_action` 是
V(s)/Q(s,a) critic；`gae_advantages`/`ppo_clipped_surrogate_loss`/`value_loss_clipped`
是 PPO 损失/优势。

**`routing_path_credit.py`**：`PathTrajectoryReplay` 是两桶（delivered/lost）FIFO，
`push` 截断到 max_hops（保 terminal 端）、lost 加 lost_penalty、backward MC 累加算
`mc_return`、Welford 更新 baseline；`sample` 50/50 混合采样 padded 到 max_hops，训练
target 用 raw mc_return（不用 advantage，避免与 TD 目标冲突）。`PathCreditMixer` 架构：
`token = Dense([state, action_emb, stop_grad(q_k)])` → +正弦位置编码 → MultiHeadAttention
→ `alpha_proj→softmax→α`、`w_proj→softplus→w`，`Q_path = Σ α·w·q`；`train_step` 跑
`Huber(Q_path − G_path) + 0.3L_q + 0.1L_alpha + 0.05L_w_prior`；部署只加载 qNetwork。
`mode="attention"`=PRD-A，`mode="rudder"`=PRD-T（挂 `ReturnPredictor`）。

## 14. 其他依赖（legacy_trace_runtime / monitor / runtime_effect_receipt）

- `legacy_trace_runtime.py`（138 行）：V2 不可变 trace 的适配器。`load_and_project_trace`
  校验 V2 trace、把网格投影到旧 Gateway 集，供「同 trace 双臂对照」（`comparison.py` 调用）。
  FACT：它 import `leo_sim.grid/trace`，是新旧两套代码唯一被允许的显式桥接点。
- `monitor.py`（284 行）：实时训练 dashboard（Rich panel），读 `metrics.jsonl` 渲染，
  `run.py` 自动拉起。
- `runtime_effect_receipt.py`：纯函数回执助手（`new_checkpoint_receipt`、
  `attempt_checkpoint_load`、`assess_temporal_effect`、`assess_path_credit_effect`），
  记录「实际执行了什么」，供 fail-closed 与 train/eval 回执。

## 15. 持久化与诊断绘图

- 持久化：`saveHyperparams`（`:10397`）、`saveQTables`（`:10433`）、`saveDeepNetworks`
  （`:10447`）、`save_replay_buffer`/`load_replay_buffer_into`（`:10475/10492`）、
  `_save_pc_replay`/`_load_pc_replay_into`（`:10509/10575`）、`save_on_interrupt`（`:11356`）。
- 诊断/绘图：`plotShortestPath`（`:8968`）、`plotLatenciesBars`（`:11495`）、
  `plotQueues`（`:11525`）、`save_plot_rewards`（`:11543`）、`save_epsilons`（`:11584`）、
  `save_losses`（`:11632`）、`plotSavePathLatencies`（`:11666`）、
  `plot_packet_latencies_and_uplink_downlink_throughput`（`:11697`）、
  `plot_throughput_cdf`（`:11777`）、`plotSaveAllLatencies`（`:11845`）、
  `plotRatesFigures`（`:11940`）、`plotCongestionMap`（`:11968`）、`plot_cka_over_time`
  （`:1629/1679`）、`plotMap`（Earth 方法）。
- 入口：`RunSimulation`（`:12019`）是旧平台主运行入口。

### 工具函数全景（哈希/日志/几何辅助/shadow）

- 哈希/序列化：`_array_sha256`（`:35`）、`_canonical_json_sha256`（`:50`）、
  `_atomic_save_npy`（`:58`）—— 数组/JSON 的 SHA 身份与原子落盘。
- 诊断日志（7 类 Hook 的写函数）：`append_replay_event`（`:838`）、`_encode_od_pair`
  （`:890`）、`_append_state_log`（`:918`）、`_append_graph_state_log`（`:937`）、
  `_append_decision_log`（`:1006`）、`_append_reward_log`（`:1035`）、`_pc_flush_lost`
  （`:1066`）、`_append_packet_fate_log`（`:1109`）、`diagnostic_link_snapshot_process`
  （`:1175`）、`_dump_diag_log`（`:1207`）、`_dump_link_snapshots`（`:1234`）、
  `flush_replay_trace`（`:1259`）—— 分别写 replay 事件、OD 编码、状态/图/决策/奖励/
  fate 日志、链路快照、诊断 dump、回放 trace。
- 几何/建链辅助：`get_direction`（`:8234`）、`get_pos_vectors_omni`（`:8249`）、
  `get_slant_range`（`:8263`）、`get_slant_range_optimized`（`:8268`）、`normalize`
  （`:8975`）—— 方向判定、全向位置向量、斜距矩阵、归一化（供 matching/createGraph 用）。
- shadow 测量：`_shadow_record`（`:5849`）、`_shadow_dump`（`:5876`）——
  比较 tffunc 编译前向 vs numpy 前向（`SIM_SHADOW_INFER`），只测量不改行为。
- 其他：`findBottleneck`（`:8087`）、`getBlockTransmissionStats`（`:1324`）、
  `simProgress`（`:1416`）、`generate_test_data`（`:1448`）。

## 旧平台第一卷 · 完成度

- 已覆盖：主文件 `SimulationRL.py` 的常量/物理层/几何层/接入层/ISL 建链/路由/
  队列观测/状态观测/奖励/学习训练/持久化/绘图，以及全部 import 依赖模块。
- 未逐行展开但已定位：`getDeepStateVisK*`/`getDeepStateDiff*` 系列内部逐行实现
  （已按其观测合同概述）；`routing_mappo.py`/`routing_path_credit.py` 内部方法
  （已按类/函数清单概述）。

## 进度标记

- 已读并写入：全局常量、物理链路层（RFlink/FSOlink）、星座几何层
  （OrbitalPlane/Satellite/edge/DataBlock）、地面接入层（Gateway/Cell/Earth）、
  ISL 建链层（matching/createGraph）、路由层、队列观测/信息年龄近似、状态观测层、
  奖励层（含 5 个距离变体）、学习/训练层（QLearning/DDQNAgent/GAT-MPNN/联邦学习/MBB）、
  流量模型（traffic_*）、链路中断（link_outage）、路由/学习扩展（routing_*/temporal）、
  其他依赖、持久化与绘图。
- 状态：**旧平台第一卷主体完成**。下一卷读新平台 `leo_sim`。
