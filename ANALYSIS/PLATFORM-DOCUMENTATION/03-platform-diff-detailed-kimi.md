# 旧平台 vs 新平台差异对照（详细版）

> 依据：`ANALYSIS/PLATFORM-DOCUMENTATION/02-kimi-platform-spec.md`（两平台逐行通读说明书）。
> 每行差异都附代码证据（`文件:行号`）。本表只列「不同在哪」，不评价哪个好、不建议取舍。
> 日期：2026-08-15。

## 一、总体形态

| # | 维度 | 旧平台 | 新平台 | 证据 |
|---|---|---|---|---|
| 1 | 代码组织 | 单体主文件 12556 行（含 17 类 + 144 顶层函数）+ 13 个外围模块，合计 17257 行 | 19 个模块各管一件事，合计 7116 行（34 类 + 110 顶层函数） | `CODE/SimulationRL.py`；`CODE/leo_sim/*.py` |
| 2 | 网络架构 | **Gateway 汇聚路径**：流量在地面网关生成/汇聚，经卫星与 ISL 转发到目的网关下行 | **卫星直连路径**：地面 TrafficEndpoint 直接上星，包内不存在 Gateway 概念 | 旧：`class Gateway`(SimulationRL.py:2573)、`class Cell`(3260)、`class Earth`(3322)；新：`class TrafficEndpoint`(kernel.py:199)、`leo_sim/__init__.py:1-9` docstring 明言「Gateway 概念不存在」 |
| 3 | 运行入口 | `RunSimulation` 主函数 + 文件内 `__main__` 块 + 生产侧 `run.py` | 统一 CLI `python -m CODE.leo_sim`，8 个子命令 | 旧：SimulationRL.py:12019、12528-12556；新：`__main__.py:314-371`（config validate / trace compile / experiment compile / run / receipt verify / acceptance run / compare run / platform check） |

## 二、需求与配置

| # | 维度 | 旧平台 | 新平台 | 证据 |
|---|---|---|---|---|
| 4 | 需求表示 | 网关间 OD 权重矩阵（(n,n) 行随机、对角 0；mlab 变体 (24,n,n)），运行时在网关侧按矩阵生成包 | **不可变数据包 trace**：先离线编译成逐包 CSV（packet_id/时间/源/宿/bits/deadline），配 manifest + SHA-256，运行只消费不重生成 | 旧：`build_od_matrix_for_gateways`(traffic_od.py:347)；新：`compile_trace`(trace.py:221)、`validate_packet_rows`(trace.py:46) |
| 5 | 流量模式 | uniform / h2 / gravity / gravity_corridors / mlab 五种 OD 模式 + Burst（时间窗乘子）+ Diurnal（昼夜乘子）后两个叠加在前者之上 | 8 种 demand 模式（含 population_gravity，直接读 GPW 人口 TIFF 聚合），burst/diurnal 作为 trace 编译期的速率乘子 | 旧：traffic_od.py:104/116/178/257、traffic_mlab.py:122/216、traffic_burst.py:61、traffic_diurnal.py:107；新：trace.py:328-337、config.py:164、population.py:37/96 |
| 6 | 配置方式 | 环境变量（模块头部约 40 组 `os.environ.get`）+ `inputRL.csv` 参数文件 + 模块级全局变量 | 版本化 YAML：SCHEMA 白名单 + 默认值 + profile + 命令行覆盖，`resolve_config` 深合并后做语义校验，非法组合 fail-closed | 旧：SimulationRL.py:124-172（env 读取段）、`_resolve_input_rl_path`(634)；新：config.py SCHEMA(55-161)、DEFAULTS(173-268)、PROFILES(270-276)、`_validate_semantics`(319)、`resolve_config`(581) |
| 7 | 配置身份 | 无单一配置指纹；回执里记录 git 值与部分 env | trace 身份 SHA 与非需求组解耦（路由/接入等改动不变 trace SHA），需求 SHA 绑定输入字节 | 旧：`_git_value`(SimulationRL.py:10685)；新：`trace_identity_payload`/`trace_identity_sha256`(config.py:540/564) |

## 三、仿真内核

| # | 维度 | 旧平台 | 新平台 | 证据 |
|---|---|---|---|---|
| 8 | 事件内核 | SimPy 进程分散挂在 Earth/Gateway/Satellite 的方法上（如 `Earth.__init__` 3674 行把 `moveConstellation` 进程赋成同名实例属性）；无统一事件预算 | 统一 `Kernel` 类集中调度；**有界性硬帽**：max_entities / max_packets / max_events 超帽即 `CapExceeded` 中断 | 旧：SimulationRL.py:3322-5637；新：kernel.py:586、`CapExceeded`(61)、帽检查 686/764/1526-1527 |
| 9 | 队列语义 | 软阈值概念：`infQueue=5000` 只是「观测状态时任其视为无穷」的界限，非硬容量 | 有限队列硬上界，溢出是显式 packet fate（进账本） | 旧：SimulationRL.py:573、9075-9095；新：`QueueArea`(kernel.py:84)，测试佐证 tests/test_kernel.py:58/72 |
| 10 | 队列结算 | 无队列面积概念 | `QueueArea` 按时间积分结算到 horizon | 新：kernel.py:84-110 |
| 11 | 接入调度 | Gateway 按 Cell 覆盖接入；`Gateway.adjustDataRate` 算出的 shannonRate 未被使用（死值） | K 个接入槽 + FIFO 等待 + 租期轮转；Uplink/Downlink 各自 DRR（差额轮询）按比特公平调度 | 旧：SimulationRL.py:2911；新：`UplinkServer`(kernel.py:255)、`DownlinkServer`(343)、`_DRRMixin`(220)，测试 test_kernel.py:86/256 |
| 12 | 星间链路 | RFlink/FSOlink 容器 + matching（markovianMatchingTwo / greedyMatching）建图；两函数参数来源不对称（前者硬编码 26e9/500e6，后者用全局 f/B/maxPtx） | `ISLLink` 统一建模；拓扑构造校验双向性，单向链路 fail-closed | 旧：SimulationRL.py:1798/1827/8330/8438；新：kernel.py:439、`build_topology`(routing.py:63)，测试 test_review_round4.py:114 |
| 13 | 切换（handover） | `SIM_GSL_HANDOVER_MODE` = legacy / mbb 两档，环境变量驱动 | BBM / MBB 显式状态机：迟滞、最小驻留、acquisition delay、MBB 硬退休 deadline | 旧：SimulationRL.py:744-751、5100、5253；新：kernel.py 接入服务逻辑，测试 test_handover.py:47-155 |
| 14 | 几何 | OrbitalPlane/Satellite 自管旋转与可见性（`rotate` 2439、`GetmaxSlantRange` 1963） | `Constellation`（Walker-delta）+ **认证式变化检测**：`_next_change_adaptive` 用速率界证明区间内无变化，不能认证即 `GeometryCertificationError` | 旧：SimulationRL.py:1842/1891；新：model.py:156、56、49 |

## 四、路由与学习

| # | 维度 | 旧平台 | 新平台 | 证据 |
|---|---|---|---|---|
| 15 | 路由算法族 | Q 表学习（QLearning）、DDQN 多状态编码（getDeepState 家族 15+ 种变体）、oracle 全局 Dijkstra、最短路径；routing_hooks 钩子层抽象打分/选路 | `choose_next_hop` 一个函数内四个策略分支：hop / delay / capacity / oracle（oracle 显式标注为分析上界） | 旧：SimulationRL.py:5682、6190、9547-10237、8807/8903、routing_hooks.py:34-129；新：routing.py:126、ORACLE_LABEL routing.py:28 |
| 16 | 学习算法 | DDQNAgent（1580 行大类）+ MAPPO（循环 actor/集中 critic）+ path-credit mixer + n-step/TD(λ) + 时序 GRU 编码器 + 联邦学习/CKA 分析 | TensorflowDDQN（canonical Double-DQN：online argmax + target 评估 + 双重 mask）+ 可选 GAT/MPNN 图编码器 | 旧：SimulationRL.py:6190、routing_mappo.py:435、routing_path_credit.py:341/1014、routing_multistep.py:36/69/109、temporal_encoder.py:124-270、SimulationRL.py:1484-1679；新：learning.py:276、`ddqn_targets`(804)、`V2GraphEncoder`(102) |
| 17 | 信息条件 | 隐式：`getObservedQueues`/`getStaleQueues`/`getTimedObservedQueues` 等函数在观测时施加延迟/陈旧 | 显式合同：C1/C3–C7 学习合同，`information_set` 统一定义每个合同能看到什么；观测只用「实际到达且未过期」的控制缓存 | 旧：SimulationRL.py:9050-9183；新：learning.py:593、724，测试 test_learning.py:29-48 |
| 18 | 控制平面 | 无独立控制平面；邻居状态经函数调用直接读取（可加延迟） | 独立控制平面：ControlPacket 真实逐跳排队、占 ISL 带宽、受 TTL/丢失约束；LocalCache 只保留最新鲜快照；vis_k 有界最短路径广播树 | 旧：SimulationRL.py:9152-9183；新：kernel.py:111、control.py:14/57/86、routing.py:31 |
| 19 | 死代码/未接线 | 相当数量无调用点符号（plot_cka_over_time_v0、createQTable、RecurrentMAPPOAgent、FrameStackBPAgent、nstep_transitions 等）；引用了当前工作区不存在的 `CODE/legacy/` 包（csr 有加载期 guard，cvar/mcp_hash 无） | 仅个别工具函数只被测试调用（geometry_loss、active_aggregate_cells）；无缺失包引用 | 旧：spec「未确认」清单（SimulationRL.py:1629/10238、routing_mappo.py:435/574、routing_multistep.py:36 等）；新：outage.py:24、grid.py:76 |

## 五、中断、随机性、账本与回执

| # | 维度 | 旧平台 | 新平台 | 证据 |
|---|---|---|---|---|
| 20 | 链路中断 | `LinkOutageSchedule`：环境变量给出的确定性调度表（按 resource_id 上下线） | 双机制：几何失效（几何不可用即丢）+ Gilbert-Elliott 两态马尔可夫随机中断，每条链路独立 RNG 流 | 旧：link_outage.py:50/166；新：outage.py:24/29、rng.py:37 |
| 21 | 随机性管理 | 单一全局种子：`SIM_SEED` 同时灌给 np.random / random / tf | 命名流：每个用途一条独立 `np.random.Generator`（demand/ge_gsl/ge_isl/…），每链路再派生独立流；学习种子与场景种子分离 | 旧：SimulationRL.py:675-687；新：rng.py:26/32/37，测试 test_learning.py:232 |
| 22 | 数据包账本 | 日志追加式：`_append_packet_fate_log` 等写 CSV/JSONL，事后由 `_run_audit_meta` 汇总审计 | 双账本运行时守恒：DataFateLedger（唯一 fate + 位守恒）/ ControlFateLedger；畸形记录报错不崩溃 | 旧：SimulationRL.py:1109、10702；新：fates.py:38/99，测试 test_fates_outage.py:7/27/36 |
| 23 | 运行回执 | `runtime_effect_receipt.py` 评估 checkpoint/temporal/path-credit 是否真生效；`_run_audit_meta` 生成 run_meta | `receipt.py` 完整 fail-closed 验证链：`verify_receipt_dir` 逐步重算 manifest、账本、计数器关系、stop==horizon、deps 版本；篡改任一字段即拒 | 旧：runtime_effect_receipt.py:13/26/65/102；新：receipt.py:585、`_validate_ledgers`(374)、`_validate_manifest`(161) |
| 24 | 中断保存 | `save_on_interrupt`：收到中断时落盘模型/队列/状态 | 无等价物；运行以 horizon 自然结束为唯一正常完成形态（`natural_end`） | 旧：SimulationRL.py:11356；新：receipt.py、kernel.py:1526-1528 |

## 六、治理、验收与对照

| # | 维度 | 旧平台 | 新平台 | 证据 |
|---|---|---|---|---|
| 25 | 治理链 | 代码包内无治理模块；授权链在外部 `CODE/experiment_platform/` | 包内自带 `governance.py`：build_run_intent 绑定 request/config/trace/代码 SHA；compile_experiment 产出可审阅 artifact | 新：governance.py:57/113；旧：无对应模块（外部见 experiment_platform/authorize_experiment.py） |
| 26 | 自检/验收 | 无包内验收工具 | `platform_check`（五类机制场景顺序跑，失败即停）+ `acceptance`（逐场景断言） | 新：platform_check.py:192、acceptance.py:136 |
| 27 | 新旧对照 | 无 | `comparison.py`：同一 immutable trace 双臂跑——直连臂走内核，legacy 臂用子进程调旧 `SimulationRL.py`，强制对齐物理时间倍率/Walker-delta/拓扑步长/seed | 新：comparison.py:102/128/203（legacy 调用点 170-174） |
| 28 | 监控 | 独立 dashboard 进程 `monitor.py`，读 `CODE/Results/*/metrics.jsonl`（该文件的写入方在当前代码树中未确认） | 无 dashboard；监控计数器在 Kernel 内（测试证明 monitor 不改变行为） | 旧：monitor.py:197/256、o3 片段「未确认」；新：kernel.py，测试 test_kernel.py:229 |

## 七、两侧都有但实现方式不同的点（速查）

- 星座几何：旧自管 rotate/可见性 vs 新 Walker-delta + 认证变化检测（见 #14）。
- 中断：调度表 vs Gilbert-Elliott（见 #20）。
- 种子：单全局种子 vs 命名流（见 #21）。
- 切换：legacy/mbb 两档 vs BBM/MBB 状态机（见 #13）。
- 队列：软阈值 vs 硬容量 + 面积结算（见 #9/#10）。
- oracle：两侧都有全局最短路径上界；旧经 `_oracle_global_dijkstra_edge_weight`(8807)，新经 `choose_next_hop` 的 oracle 分支且强制标注 ORACLE_LABEL。

## 八、只在单侧存在的能力（FACT：另一侧 grep 无对应物）

- 只在新平台：不可变 trace 编译器与 SHA 身份、位守恒双账本、fail-closed receipt 验证链、包内治理 intent、platform_check/acceptance/comparison 工具、规范 grid_id、人口重力需求、命名 RNG 流、队列面积、MBB 硬退休、认证式几何变化检测。
- 只在旧平台：Q 表学习、MAPPO、path-credit、n-step/TD(λ)、时序 GRU 编码器、联邦学习/CKA 分析、FSOlink 容器、markovian/greedy 匹配建图、monitor dashboard、中断落盘保存、15+ 种 DDQN 状态编码变体、burst/diurnal 运行时乘子调度器（新平台把昼夜/突发挪到了 trace 编译期）。
