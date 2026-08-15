# 卫星网络路由仿真平台说明书（Kimi 独立通读版）

> 本文档由 Kimi 按「独立平台说明书任务提示词」（`ANALYSIS/PLATFORM-DOCUMENTATION/prompt-for-kimi.md`）产出，
> 与主脑（Codex）的 `01-legacy-platform.md` 相互独立。本文只做事实性通读说明：代码里有什么、每部分做什么、怎么做。
> 不含任何迁移/优劣/取舍判断。日期：2026-08-15。

## 阅读方式声明

- 全部 33 个目标文件由 13 个并行阅读代理分工完成：每个代理先用 `wc -l` 实测行数、用 `grep -nE '^(class |def )'` 生成覆盖核对清单，再用 Read 分页把自己负责的范围逐行读完，写完片段后逐符号回核。
- `CODE/SimulationRL.py`（12556 行）按行号切成 5 段（1–2471、2472–5637、5638–7884、7885–10237、10238–12556）分别逐行通读，段间以符号定义行对齐，无重叠无遗漏。
- `CODE/leo_sim/tests/` 与 `CODE/tests/` 未逐行通读，仅作为行为佐证被引用（引用处标注了测试文件:行号）。
- 各片段的中间产物保留在 `ANALYSIS/PLATFORM-DOCUMENTATION/kimi-fragments/`，本文即由这些片段拼接而成，可逐个回溯。

## 实际读到的文件清单（行数均为 `wc -l` 实测）

### 旧平台（14 个文件，合计 17257 行）

| 文件 | 行数 |
|---|---|
| `CODE/SimulationRL.py` | 12556 |
| `CODE/traffic_od.py` | 442 |
| `CODE/traffic_burst.py` | 194 |
| `CODE/traffic_diurnal.py` | 382 |
| `CODE/traffic_mlab.py` | 325 |
| `CODE/link_outage.py` | 197 |
| `CODE/routing_hooks.py` | 133 |
| `CODE/routing_mappo.py` | 631 |
| `CODE/routing_multistep.py` | 138 |
| `CODE/routing_path_credit.py` | 1418 |
| `CODE/temporal_encoder.py` | 272 |
| `CODE/legacy_trace_runtime.py` | 138 |
| `CODE/monitor.py` | 284 |
| `CODE/runtime_effect_receipt.py` | 147 |

注：`CODE/routing_hooks.py` 不在任务清单的显式列表里，但它是 `SimulationRL.py:229` 顶层 import 的本地模块，按任务书「主文件 + 它 import 的本地模块都要覆盖」的要求纳入。

### 新平台（19 个文件，合计 7116 行）

| 文件 | 行数 | 文件 | 行数 |
|---|---|---|---|
| `CODE/leo_sim/__init__.py` | 11 | `CODE/leo_sim/learning.py` | 825 |
| `CODE/leo_sim/__main__.py` | 397 | `CODE/leo_sim/model.py` | 294 |
| `CODE/leo_sim/acceptance.py` | 153 | `CODE/leo_sim/outage.py` | 77 |
| `CODE/leo_sim/comparison.py` | 271 | `CODE/leo_sim/platform_check.py` | 270 |
| `CODE/leo_sim/config.py` | 630 | `CODE/leo_sim/population.py` | 139 |
| `CODE/leo_sim/control.py` | 109 | `CODE/leo_sim/receipt.py` | 941 |
| `CODE/leo_sim/fates.py` | 188 | `CODE/leo_sim/rng.py` | 41 |
| `CODE/leo_sim/governance.py` | 257 | `CODE/leo_sim/routing.py` | 226 |
| `CODE/leo_sim/grid.py` | 87 | `CODE/leo_sim/trace.py` | 522 |
| `CODE/leo_sim/kernel.py` | 1678 | | |

## 覆盖统计（分母 = 各文件 `grep -nE '^(class |def )'` 实测总数）

- 旧平台：类 **35/35**，顶层函数 **221/221**。
  - `SimulationRL.py`：类 17/17（Logger、Results、BlocksForPickle、RFlink、FSOlink、OrbitalPlane、Satellite、edge、DataBlock、Gateway、Cell、Earth、hyperparam、QLearning、GraphMessagePassingReadout、DDQNAgent、ExperienceReplay），顶层函数 144/144。
  - 流量模块组（traffic_od/burst/diurnal/mlab）：类 2/2，函数 24/24。
  - 路由扩展组（routing_hooks/mappo/multistep/path_credit）：类 13/13，函数 17/17。
  - 其余依赖组（link_outage/temporal_encoder/legacy_trace_runtime/monitor/runtime_effect_receipt）：类 3/3，函数 36/36。
- 新平台：类 **34/34**，顶层函数 **110/110**（逐模块核对：kernel 12 类+1 函数；learning 3 类+13 函数；receipt 14 函数；config 2 类+10 函数；trace 1 类+10 函数；rng 3 函数；grid 6 函数；model 2 类+3 函数；control 2 类+1 函数；outage 1 类+1 函数；fates 3 类；routing 7 函数；governance 1 类+4 函数；acceptance 1 类+4 函数；platform_check 1 类+8 函数；comparison 2 类+8 函数；population 3 类+2 函数；__main__ 15 函数；__init__ 0）。
- 合计：**33 个文件、24373 行、类 69/69、顶层函数 331/331**。
- 类方法级覆盖：各片段均做了逐方法清点（例如 Satellite 12/12、Gateway 22/22、Earth 24/24、DDQNAgent 20/20、Kernel 43/43、TensorflowDDQN 10/10、PathCreditMixer 9/9、ReturnPredictor 12/12），无跳过。

## INFERENCE 清单（全文中标注了 (INFERENCE) 的全部位置）

1. `BlocksForPickle` 用途为「pickle 落盘的精简拷贝」— CODE/SimulationRL.py:1771（依据类名、字段选择与落盘调用点推断）。
2. `FSOlink` 中「FSO=自由空间光链路」的解读 — CODE/SimulationRL.py:1827（依据类名与 `__repr__` 标签推断）。
3. `class edge` 职责句 — CODE/SimulationRL.py:2472（该类无 docstring，依据属性名与实例化点推断）。
4. `DDQNAgent` 依赖关系段：运行时触发 cvar/mcp_hash 分支会 ImportError — CODE/SimulationRL.py:6190 起（前提「`CODE/legacy/` 不存在」为 FACT；分支无模块级 guard 的推断标 INFERENCE）。
5. `createQTable` 是「QLearning 表初始化的未接线遗留实现」— CODE/SimulationRL.py:10238（前提「全库无调用方」为 FACT）。
6. `saveDeepNetworks` 的 csr 分支在当前工作区不可达 — CODE/SimulationRL.py:10464–10466（前提「legacy 包不存在 + 模块加载期 guard」为 FACT）。
7. `traffic_burst.py:7-8` 模块 docstring 的用途声明（体育赛事/灾害救援等事件类型意图）——代码只实现时间窗+乘子机制。
8. `traffic_diurnal.py:11-12` 及 56–59 注释的文献依据声明（amplitude 0.4 锚定 WetLinks、peak 20:00 为 ISP primetime）——代码内只有数值可核验。
9. `traffic_mlab.py:20-25` 模块 docstring 中 `sample_count * mean_throughput_mbps` 代理「城市对间交换字节量」的物理解释——代码只执行该乘法聚合。
10. `_graph_custom_objects` 用途（让 Keras 反序列化识别自定义层）— CODE/leo_sim/learning.py:272（由 Keras API 语义推定，代码内无注释）。
11. `_sph_to_ecef` 的 ECEF（地固系）语义 — CODE/leo_sim/model.py:20（函数体只做球面→笛卡尔变换；地固系语义取决于调用方是否已做地球自转修正）。

另有两处措辞说明（未标 INFERENCE，如实记录）：routing_hooks.py 的 `ActionScoringHook`/`ActionSelectorHook` 被称为「抽象基类」仅依据方法体 `raise NotImplementedError` 与继承关系，文件中无 `ABC` 显式声明。

## 「未确认」清单（全文中标注「未确认」的全部位置，按文件归组）

### CODE/SimulationRL.py
- `plot_cka_over_time_v0`（1629）：调用方未确认（全库 grep 无调用点）。
- `compute_average_cka`（1580）：唯一调用方是无调用点的 `plot_cka_over_time_v0`，实际执行路径未确认。
- `FSOlink`（1827）：实例化点未确认。
- `_linked_mask_and_bf`（905）：`_append_decision_log` 之外的调用方未确认。
- `hyperparam.__repr__`（5672）、`ExperienceReplay.getBatch`（7808）：调用方未确认。
- `QLearning`（5682）：直接针对它的测试未确认。
- `edge.__cmp__`（2492）、`Gateway.removeCell`（2988）、`Cell.setGT`（3300）、`Earth.set_window`（3754）、`Earth.updateSatelliteProcessesSimpler`（3878）、`Earth.testFlowConstraint1`（5299）、`Earth.testFlowConstraint2`（5315）、`Earth.plot3D`（5605）：调用方未确认（全库无调用点）。
- `normalize`（8975）、`watchScores`（8990）、`getDirection_deprecated`（9233）、`getDeepStateVisKGAT`（9752）、`createQTable`（10238）、`plotLatenciesBars`（11495）：调用方未确认。
- `getShortestPath`（8903）：同文件 11 处调用与 1 处测试调用已确认，跨文件运行时调用方未确认。
- 8777 行注释引用的 `scripts/oracle_vis_k_smoke.py`：在当前代码库中不存在，未确认。

### 旧平台依赖模块
- `LinkOutageSchedule.summary`（link_outage.py:157）、`LinkOutageSchedule.is_down_at`（link_outage.py:140）、`_positive_float`（link_outage.py:42 跨文件调用方）：未确认。
- `runtime_effect_receipt._mismatch`（runtime_effect_receipt.py:56）：跨文件调用方未确认（文件内私有）。
- `monitor.py` 消费的 `metrics.jsonl` 的写入方：在当前代码树中未确认（grep 仅 monitor.py 自身出现相关键名）；`monitor.py:18` 的 `import os` 无使用点（FACT）。
- `temporal_encoder.py` docstring 内的 SimulationRL 行号引用（createModel@5841、_apply_frame_stack@7465 等）：未逐条核实。
- routing_mappo.py：`FrameStackHelper`(130)、`ppo_clipped_surrogate_loss`(344)、`value_loss_clipped`(359)、`gae_advantages`(370)、`MAPPORolloutBuffer.push/flush_all/is_full`(417/421/427)、`RecurrentMAPPOAgent`(435)、`FrameStackBPAgent`(574)、`parse_env_config`(622)：生产代码调用方未确认。
- routing_multistep.py：`nstep_transitions`(36)、`nstep_transitions_streaming`(69)：运行时调用方未确认。
- routing_path_credit.py：`build_return_predictor`(988)、`ReturnPredictor.predict_g0`(1203)、`ReturnPredictor.save_weights/load_weights`(1381/1396)：生产代码调用方未确认（仅测试或类内部调用）。

### 新平台 CODE/leo_sim/
- `kernel.LearningUnavailable` 别名（kernel.py:54）的消费方；`Kernel.run` 的 `env.peek()` 异常分支（kernel.py:1520–1521）的触发条件；kernel.py:719–723「进程创建顺序决定同时刻事件顺序」注释依赖的 SimPy 调度语义；kernel.py:18–20 docstring 的等待有界性数学声明（无运行时检查）：均未确认。
- `config.demand_sha256`（config.py:573）：调用方未确认（docstring 自称为外部探针脚本保留，该脚本不在仓库内）。
- `rng.STREAM_NAMES`（rng.py:15-23）中 6 个流名的设立意图：未确认（生产代码只用 `demand` 流与 `link_stream`）。
- `grid.active_aggregate_cells`（grid.py:76）、`outage.geometry_loss`（outage.py:24）：生产代码调用方未确认（仅测试调用；生产路径内联了等价逻辑）。
- `_cell_index`(grid.py:15)、`_sph_to_ecef`(model.py:20)、`_reverse_adj`(routing.py:83)、`_multi_source_dist`(routing.py:93)、`_dir_of`(routing.py:222)：同文件内调用边已确认，外部调用方未确认。
- `governance._write_json`（governance.py:50）、`acceptance._max_satellite_occupancy`（acceptance.py:26）、`comparison._GatewaySite`（comparison.py:30）：跨文件调用方未确认（文件内私有）。
- `population.py:1` docstring 中的「GPW」数据源具体所指：未确认。
- `__init__.__version__`（__init__.py:11）的读取方：未确认。
- kernel.py 在 CODE/ 之外的调用方：仅确认 `CODE/scripts/remote/remote_job.py:250` 经子进程间接触达，EXPERIMENTS/ 下契约层面的间接入口未逐一穷举。

## 阅读中发现的 docstring/注释与实现不一致（FACT，仅并列记录，不评价）

- `SimulationRL.py:5822–5832` 注释称 numpy 推理后端「EVAL-ONLY」，6775 行实现注释称已支持 train+eval。
- `SimulationRL.py:7329` `alignQTarget` docstring 自称「未使用」，但 `makeDeepAction`（7305）每个决策都调用它。
- `traffic_od.py:11` docstring 的模式清单不含 `mlab`，但调度器 `build_od_matrix_for_gateways`(401–438) 已实现 mlab 分支。
- `traffic_diurnal.py:20-23` docstring 自称「Phase 4 才会接线」，但接线已存在于 `SimulationRL.py:3169-3180`。
- `CODE/leo_sim/trace.py:8` docstring 列举 7 种 demand 模式，漏列已实现为第 8 种的 `population_gravity`（trace.py:328-337、config.py:164）。
- `CODE/tests/test_runtime_effect_receipt.py` 文件名指向 `runtime_effect_receipt.py`，但其内容不 import 该模块；真正的直接单测在 `CODE/tests/test_runtime_effect_helpers.py`。
- 缺失依赖（FACT）：`legacy.routing_csr`/`legacy.routing_tailguard`/`legacy.routing_mcp_hash` 被 `SimulationRL.py` 多处延迟 import 引用，但 `CODE/legacy/` 目录在当前工作区不存在；`SIM_CSR_MODE=csr` 在模块加载期（474–479 行）有 fail-loud guard，cvar/mcp_hash 分支无对应 guard。

---

# 第一卷 旧平台说明书（Gateway 汇聚路径）

主文件 `CODE/SimulationRL.py`（12556 行）按行号五段展开，随后是它 import/依赖的本地模块。
# 片段 s1：`CODE/SimulationRL.py` 第 1–2471 行

### 文件 `CODE/SimulationRL.py`（实测 12556 行）

本片段只覆盖「定义行落在第 1–2471 行」的顶层符号：7 个顶层 `class`、41 个顶层 `def`。第 2472 行起为 `class edge`，属于下一片段。

#### 模块级说明（第 1–2471 行内的模块级代码）

- 第 1–18 行：基础第三方/标准库导入：`time`、`pandas as pd`、`math`、`numpy as np`、`geopy.distance`、`simpy`、`numba`、`networkx as nx`、`PIL.Image`、`scipy.optimize.linear_sum_assignment`、`pickle`、`random`、`os`、`json`、`csv`、`hashlib`、`tempfile`、`subprocess`。(FACT)
- 第 20–32 行：同包模块导入——`traffic_od`（`build_od_matrix_for_gateways`、`load_traffic_config_from_env`、`traffic_mode_needs_gateway_physical`）、`traffic_burst.load_burst_schedule_from_env`、`traffic_diurnal.load_diurnal_schedule_from_env`、`runtime_effect_receipt`（`assess_path_credit_effect`、`assess_temporal_effect`、`attempt_checkpoint_load`、`new_checkpoint_receipt`）。(FACT)
- 第 147–163 行：第二批导入——`folium`、`IPython.display.display`、`typing.List/Optional/Tuple`、`datetime.datetime`、`seaborn`、`gc`、`cProfile`、`collections.defaultdict`、`glob`、`builtins`、`matplotlib.pyplot as plt`、`matplotlib` 的 `LogNorm`/`Path`/`FancyArrowPatch`/`Normalize`/`cm`。(FACT)
- 第 170–171 行：`sys`、`atexit`（供 `Logger` 使用）。(FACT)
- 第 197–202 行：深度学习框架导入——`tensorflow as tf`、`keras` 的 `Model/Sequential/losses`、`Adam`、`Dense/Embedding/Reshape/Input/Conv2D/Flatten/Layer/Concatenate`、`collections.deque`。(FACT)
- 第 204–212 行：一段被整体注释掉的 GPU 探测代码，注释说明“本场景 RL 训练每步小 batch，不值得用 GPU”。(FACT)
- 第 219–232 行（路由方式选择）：`_SIM_FAIL_CLOSED`（219–221，读 env `SIM_FAIL_CLOSED`）；`pathings` 列表（222，含 `'hop','dataRate','dataRateOG','slant_range','oracle_global_dijkstra','Q-Learning','Deep Q-Learning'`）；`_SIM_PATHING`/`pathing`（225–226，env `SIM_PATHING` 覆盖，缺省为 `pathings[3]` 即 `'slant_range'`）；从 `routing_hooks` 导入 `parse_routing_mode`/`validate_routing_mode` 并立即执行得到 `SIM_ROUTING_MODE`（229–232）。(FACT)
- 第 234–237 行：布尔开关 `FL_Test=False`、`plotSatID=True`、`plotAllThro=True`、`plotAllCon=True`。(FACT)
- 第 239–258 行：`movementTime=10`、`ndeltas=5805.44/20`；env `SIM_MOVEMENT_TIME`/`SIM_MOVEMENT_SPEEDUP` 可覆盖二者，非数值或 speedup 非有限正数时若 `_SIM_FAIL_CLOSED` 为真则 `raise RuntimeError`（242–258）。(FACT)
- 第 260–268 行：`Train=True`、`explore=True`、`importQVals=False`、`onlinePhase=False`；`onlinePhase` 为真时强制 `explore=False` 且 `importQVals=True`，否则强制 `FL_Test=False`（264–268）。(FACT)
- 第 270–274 行：奖励权重 `w1`（env `SIM_W1`，默认 int 20）、`w2`（env `SIM_W2`，默认 float 20）、`w4=5`；折扣因子 `gamma`（env `SIM_GAMMA`，默认 0.99）。(FACT)
- 第 276–289 行：`GTs=[4]`（网关数量列表）；env `SIM_GTS` 可覆盖为逗号分隔整数列表，解析失败则保留默认并打印提示（283–289）。(FACT)
- 第 291–299 行（物理常量）：`rKM=500`、`Re=6378e3`、`G=6.67259e-11`、`Me=5.9736e24`、`Te=86164.28450576939`、`Vc=299792458`、`k=1.38e-23`、`eff=0.55`。(FACT)
- 第 301–310 行（下行链路参数）：`f=20e9`、`B=500e6`、`maxPtx=10`、`Adtx=0.26`、`Adrx=0.26`、`pL=0.3`、`Nf=2`、`Tn=290`、`min_rate=10e3`。(FACT)
- 第 312–315 行（上行参数）：`balancedFlow=False`、`totalFlow=2e9`、`avUserLoad=8593*8`。(FACT)
- 第 318 行：`BLOCK_SIZE=64800`。(FACT)
- 第 324–329 行：`saveISLs=True`、`const_moved=False`、`matching='Greedy'`（注释给出备选 `'Markovian'`）、`minElAngle=30`、`mixLocs=False`、`rotateFirst=False`。(FACT)
- 第 332–337 行（状态预处理）：`coordGran=20`、`diff=True`、`diff_lastHop=False`（env `SIM_DIFF_LAST_HOP` 可覆盖；注释称 False→28 维 `getDeepStateDiff`，True→29 维）。(FACT)
- 第 339–354 行（奖励修复开关）：`_SIM_M1_FIX`（env `SIM_M1_FIX`）与 `_M1_BETA=200.0`（344–345）；`_SIM_REWARD_LINEAR`（env `SIM_REWARD_LINEAR`）与 `_LINEAR_ALPHA`（env `SIM_LINEAR_ALPHA`，默认 200.0）（350–351）；`_SIM_M2_FIX`（env `SIM_M2_FIX`，注释称状态从 28 维扩到 32 维）（354）。(FACT)
- 第 356–364 行（M3 队列动态）：`_SIM_M3_DYNAMICS`（env `SIM_M3_DYNAMICS`）、`_M3_EMA_ALPHA`（env `SIM_M3_EMA_ALPHA`，默认 0.3）、模块级字典 `_sat_queue_dynamics`（`id(sat)` → 前一拍队列与 EMA 增量）。(FACT)
- 第 366–401 行（vis-k / 图状态表示）：`_SIM_STATE_MODE`（env `SIM_STATE_MODE`，注释列出 `''/c1/c2/c3/c4/c5`）、`_SIM_STATE_VIS_K`（env，默认 2）、`_SIM_VIS_K_STALE_STEPS`（env，默认 0）、`_SIM_VIS_K_UPDATE_INTERVAL_S`（env，默认 0）、模块级 `_stale_queue_buffer` 字典（387）、`_GRAPH_MAX_NODES`（env `SIM_GRAPH_MAX_NODES`，默认 32）、`_GRAPH_NODE_FEAT_DIM=14`、`_RAAC_NODE_FEAT_DIM=17`、`_RAAC_ACTION_FEAT_DIM=9`、`_RAAC_AOI_SCALE_S`（env，默认 0.1）、`_RAAC_AOI_GATE`（env，默认开）、`_RAAC_MIN_RELIABILITY_RATE=1e-6`、`_GRAPH_HIDDEN_DIM`（默认 32）、`_GRAPH_ATT_HEADS`（默认 2）、`_GRAPH_LAYERS`（默认等于 `_SIM_STATE_VIS_K`）、`_GRAPH_LOG_EVERY`（默认 500）。(FACT)
- 第 442–467 行（多步信用分配）：`_SIM_NSTEP`（env `SIM_NSTEP`，≥1，447）；`_SIM_TD_LAMBDA`（env `SIM_TD_LAMBDA`，默认 0=关，453–454）；λ 越界则 `SystemExit`（455–456）；`SIM_NSTEP>1` 与 TD(λ) 互斥，同时开启则 `SystemExit`（457–459）；`_SIM_MULTISTEP` 为二者任一开启（467）。(FACT)
- 第 469–480 行（CSR-DQN）：`_SIM_CSR_MODE`（env `SIM_CSR_MODE`）；值为 `'csr'` 时直接 `raise RuntimeError`（476–479），报错文案称 `legacy.routing_csr` 不在 retained CODE 中；`_SIM_CSR_PHI_DIM` 依 env `SIM_CSR_ROLE_FLAG` 取 6 或 5（480）。(FACT)
- 第 482–516 行（MAPPO/BP 先验）：`_SIM_FRAME_STACK_K`（默认 1=关）、`_SIM_BP_BETA`（默认 0=关）、`_SIM_BP_K_PROGRESS`、`_SIM_BP_K_LOOP`、`_SIM_CRITIC_GLOBAL`、`_SIM_BP_ONLY`、`_SIM_MAPPO_MODE`（默认 `'off'`）、`_SIM_BP_CORRECT`、`_SIM_BP_V`（默认 10）；当 mode ∈ {`framestack_bp`,`full_recurrent`,`bp_only`} 时若 `FRAME_STACK_K<1` 强制为 4 并打印配置行（511–516）。(FACT)
- 第 519 行：模块级 `_bp_backlog_cache = {}`（`id(sat)` → `(sim_time, {dest_id: count})`）。(FACT)
- 第 546–549 行：`GLOBAL_STATE_DIM=44`（注释称须与 `routing_mappo.GLOBAL_STATE_DIM` 一致）；`_SIM_DISTILL_LAMBDA`（env，默认 0.5）。(FACT)
- 第 551–552 行：`reducedState=False`、`notAvail=0`。(FACT)
- 第 554–570 行（学习超参数）：`ddqn=True`、`plotPath=False`、`alpha=0.25`、`alpha_dnn=0.01`、`epsilon=0.1`、`tau=0.1`、`learningRate`（env `SIM_LR`，默认 0.001）、`plotDeliver=False`、`GridSize=8`、`winSize=20`、`markerSize=50`、`nTrain`（env `SIM_NTRAIN`，默认 2）、`noPingPong=True`。(FACT)
- 第 572–576 行：`infQueue=5000`、`queueVals=10`、`latBias=90`、`lonBias=180`。(FACT)
- 第 578–594 行（奖励常量）：`ArriveReward=50`、`againPenalty=-10`、`unavPenalty=-10`、`biggestDist=-1`、`firstMove=True`；`_SIM_POTENTIAL_SHAPING`（env `SIM_POTENTIAL_SHAPING`，589）；`distanceRew=4`（590–594，注释列出 1–5 五种取值语义，并称 4 是论文所用）。(FACT)
- 第 596–606 行（深度学习的训练超参数，全部 env 可覆盖）：`MAX_EPSILON`（0.99）、`MIN_EPSILON`（0.001）、`LAMBDA`（0.0005）、`decayRate`（4）、`Clipnorm`（1）、`hardUpdate`（1）、`updateF`（1000）、`batchSize`（16）、`hiddenUnits`（32）、`bufferSize`（1000）。(FACT)
- 第 608–614 行（止损）：`stopLoss=False`、`nLosses=50`、`lThreshold=0.5`、`TrainThis=Train`。(FACT)
- 第 617 行：`CurrentGTnumber=-1`（注释称随网关加入而更新）。(FACT)
- 第 623–631 行（路径）：`nnpath`（env `SIM_NN_PATH`，默认 `./pre_trained_NNs/qNetwork_3GTs.h5`）、`nnpathTarget`（env `SIM_NN_TARGET`，默认 `./pre_trained_NNs/qTarget_3GTs.h5`）、`tablesPath='./pre_trained_NNs/qTablesExport_8GTs/'`；623–630 行含若干注释掉的旧路径。(FACT)
- 第 640–667 行（`if __name__ == '__main__':` 块）：读取 `_resolve_input_rl_path()` 指定的 inputRL.csv（642）；用 `_results_dir_traffic_od_tag()` 与 `_sanitize_run_label_for_path(env SIM_RUN_LABEL)` 及 env `SIM_CFG_PATH_TAG` 拼目录后缀（643–650）；按模板 `'{pathing}_{Test length}s_frac{Fraction}_[{ArriveReward}]_Del_[{w1}]_w2_{w2}_GTs{GTs}{tag}/'` 在 env `SIM_RESULTS_ROOT`（默认 `./Results`）下生成 `outputPath`（651–662）；`populationMap` 指向本文件同级 `population_map/gpw_v4_population_count_rev11_2020_15_min.tif`（663–667）。(FACT)
- 第 673–691 行（Simpy 全局）：`receivedDataBlocks=[]`、`createdBlocks=[]`；`_SEED`（env `SIM_SEED`，默认 42）并分别设置 `np.random.seed`、`random.seed`、`tf.random.set_seed`（try 包裹），`seed=_SEED` 保留旧名（680–687）；`upGSLRates`、`downGSLRates`、`interRates`、`intraRate` 四个空列表（688–691）。(FACT)
- 第 693–706 行：`REPLAY_TRACE=True`；env `SIM_FAST=1` 时关闭 `REPLAY_TRACE/plotSatID/plotAllThro/plotAllCon/saveISLs` 并打印提示。(FACT)
- 第 708–728 行：`_SIM_LOG_LEVEL`（env `SIM_LOG_LEVEL`，0–3，非法/负值钳到 0；注释给出 0–3 各级语义）；`_SIM_BUFFER_SNAPSHOT_INTERVAL`（env，默认 0=关，负值钳 0）。(FACT)
- 第 730–833 行（path-credit / GSL 切换 / 检查点组）：`_SIM_GSL_HANDOVER_MODE`（env，默认 `'legacy'`，不在 `{legacy,mbb}` 则 `SystemExit`，744–752）及 `_SIM_GSL_HANDOVER_MAX_RETIRING_LINKS`、`_SIM_GSL_KEEP_STABLE`；`_SIM_PATH_CREDIT`（env，默认 0）且与 `_SIM_MULTISTEP` 互斥（754–757）；`_SIM_PATH_CREDIT_*` 系列超参数（758–770）；`_SIM_PATH_CREDIT_MODE`（`'attention'|'rudder'`，非法值打印警告并回退 `'attention'`，775–778）；RUDDER 预测器超参数（780–789）；两个消融开关 `SIM_PATH_CREDIT_FORCE_UNIFORM_ALPHA`/`_FORCE_UNIT_W`（790–797）；`_SIM_TRUE_DDQN`、`_SIM_FAST_TRAIN`、`_SIM_SHADOW_INFER`（801–803）；开启时打印配置（804–819）；`SIM_CHECKPOINT_FRACTIONS` 解析为 (0,1) 内去重排序的小数列表（823–833）。(FACT)
- 第 848–887 行：7 个诊断日志列模式常量 `_DECISION_LOG_COLS`、`_REWARD_LOG_COLS`、`_TRAIN_LOG_COLS`、`_PACKET_FATE_COLS`、`_EVAL_CURVE_COLS`、`_STATE_LOG_COLS`、`_GRAPH_STATE_LOG_COLS`、`_ENCODER_LOG_COLS`（853–887；注释称这些列清单是写盘 hook 与 flush 的共同真源）。(FACT)（注：该段行号落在 848–887，位于函数群中，但属于模块级常量。）
- 第 1434–1446 行（联邦学习全局）：`FL_techs=['nothing','modelAnticipation','plane','full','combination']`、`FL_tech=FL_techs[4]`（即 `'combination'`）；为 `'combination'` 时置全局 `FL_counter=1`（1436–1438）；`pathing != 'Deep Q-Learning'` 时强制 `FL_Test=False`（1440–1441）；`FL_Test` 为真时初始化 `CKA_Values=[]`、`num_samples=10` 并打印（1443–1446）。(FACT)

---

#### `def _array_sha256(array) -> str` — CODE/SimulationRL.py:35
- 定位：CODE/SimulationRL.py:35
- 职责：对数值矩阵计算稳定内容哈希；输入为 `None` 或无法转为 float64 时返回空字符串 (FACT)。
- 关键流程：转 `<f8` C 连续数组（40），把 shape 的紧凑 JSON、`b"\0little-endian-float64-c\0"` 标记与原始字节依次喂给 sha256（43–46），返回 hex digest（47）。
- 输入/输出：任意 array-like → 64 位十六进制字符串或 `""`。
- 依赖关系：被本文件 10841–10842 行调用（对 `earth.od_weight_matrix`、`earth.od_weight_matrices_hourly` 做回执哈希）；测试佐证 `CODE/tests/test_runtime_effect_receipt.py:182-188`（稳定性/内容敏感性/None→""）。

#### `def _canonical_json_sha256(value) -> str` — CODE/SimulationRL.py:50
- 定位：CODE/SimulationRL.py:50
- 职责：对可 JSON 序列化的值按 sort_keys+紧凑分隔符序列化后取 sha256；序列化失败返回 `""` (FACT)。
- 输入/输出：任意 JSON 可序列化值 → hex 字符串或 `""`。
- 依赖关系：被本文件 3541、3596 行调用（`class Earth`（定义于 3322 行）内对 `traffic_config` 的哈希）。

#### `def _atomic_save_npy(path_without_ext, array, *, allow_pickle=False) -> str` — CODE/SimulationRL.py:58
- 定位：CODE/SimulationRL.py:58
- 职责：原子写 `.npy`——先写同目录临时文件、fsync、再 `os.replace` 到目标路径；异常时删除临时文件并重新抛出 (FACT，docstring 58–65 与实现一致)。
- 输入/输出：路径前缀（可带或不带 `.npy`）+ ndarray → 实际写入的最终路径字符串。
- 依赖关系：被本文件 1374（`getBlockTransmissionStats` 内）、11436、12474 行调用。

#### `def _results_dir_traffic_od_tag() -> str` — CODE/SimulationRL.py:88
- 定位：CODE/SimulationRL.py:88
- 职责：按当前流量配置生成 Results 目录后缀，区分 uniform / h2 / gravity / gravity_corridors / trace 等模式 (FACT，docstring 89–92)。
- 关键流程：env `SIM_TRAFFIC_TRACE_PATH` 非空时返回 `_m_trace_<sha前8位|unsealed>`（93–98）；env `SIM_TRAFFIC_UNIFORM` 真时返回 `_m_uniform`（99–100）；否则经 `load_traffic_config_from_env()` 取 `mode`，分别拼 `_m_uniform`、`_m_h2_p.._g..`、`_m_gravity_a.._df.._bu..`、`_m_gravity_corridors_pc..`，未知 mode 清洗后拼 `_m_<mode>`（101–119）；任何异常返回 `""`（120–121）。
- 输入/输出：无参（读 env 与 traffic 配置）→ 后缀字符串。
- 依赖关系：被本文件 643 行（`__main__` 块）调用；依赖 `traffic_od.load_traffic_config_from_env`（22 行导入）。

#### `def _sanitize_run_label_for_path(raw: str) -> str` — CODE/SimulationRL.py:124
- 定位：CODE/SimulationRL.py:124
- 职责：把 run label 清洗为可入路径的片段：保留字母数字、`._-` 与 CJK 字符，其余替换为 `_`，去首尾 `_`，截断 120 字符 (FACT，docstring 125–131 与实现一致)。
- 输入/输出：任意字符串 → 清洗后的字符串（空输入返回 `""`）。
- 依赖关系：被本文件 644 行（`__main__` 块）调用。

#### `class Logger` — CODE/SimulationRL.py:173
- 定位：CODE/SimulationRL.py:173
- 职责：stdout 的替身对象，把写入口同时转发到终端与一个追加打开的日志文件 (FACT)。
- 关键状态/结构：`self.terminal`（原 `sys.stdout`）、`self.log`（打开的文件句柄）。
- 关键流程/方法：`__init__`(174) 保存 `sys.stdout`、以追加模式打开 `filename`（默认 `'logfile.log'`）、用 `atexit.register` 注册 `close`；`write`(179) 把 message 同时写终端与文件；`flush`(183) flush 终端并在文件未关时 flush 文件；`close`(188) 在文件未关时关闭文件。
- 输入/输出：构造吃文件路径；`write` 吃字符串，无返回。
- 依赖关系：被本文件 12530 行调用（`sys.stdout = Logger(outputPath + 'logfile.log')`，位于 `__main__` 流程）；依赖模块级 `sys`、`atexit`（170–171）。

#### `def _safe_next_action_mask(mask)` — CODE/SimulationRL.py:404
- 定位：CODE/SimulationRL.py:404
- 职责：校验并规范化 bootstrap 用的下一动作掩码：接受形状 `(4,)` 或 `(B,4)`，全空的（批）行被置为全 True（fail-safe 回退），其余形状 `raise ValueError` (FACT，docstring 405–412 与实现一致)。
- 输入/输出：array-like 布尔掩码 → `np.bool_` 数组，形状同输入。
- 依赖关系：被 `_masked_target_dqn_values`(427)、`_masked_double_dqn_actions`(436) 调用；被本文件 7530 行（DDQN 训练路径）调用。

#### `def _masked_target_dqn_values(target_q, next_action_mask)` — CODE/SimulationRL.py:425
- 定位：CODE/SimulationRL.py:425
- 职责：Target-DQN 的 bootstrap 值：非法动作用 `-1e9` 屏蔽后沿最后一轴取 max；Q 与掩码形状不一致时 `raise ValueError` (FACT)。
- 输入/输出：`(4,)` 或 `(B,4)` 的 target Q 与掩码 → `(B,)` 或标量最大值数组。
- 依赖关系：调用 `_safe_next_action_mask`；被本文件 7552 行（DDQN 训练目标计算，n-step 的 `gamma**N` bootstrap）调用；测试佐证 `CODE/tests/test_runtime_effect_receipt.py:130-138`（非法高 Q 动作不会被选中；空掩码回退为全动作）。

#### `def _masked_double_dqn_actions(online_q, next_action_mask)` — CODE/SimulationRL.py:434
- 定位：CODE/SimulationRL.py:434
- 职责：Double-DQN 的动作选择：非法动作用 `-1e9` 屏蔽后沿最后一轴取 argmax；形状不一致 `raise ValueError` (FACT)。
- 输入/输出：online Q 与掩码 → 动作下标（数组）。
- 依赖关系：调用 `_safe_next_action_mask`；被本文件 7543 行（true-DDQN 的 `a*` 选择）调用；测试佐证 `CODE/tests/test_runtime_effect_receipt.py:130-138`。

#### `def _bp_backlog_counts(s, now, ttl=0.05)` — CODE/SimulationRL.py:521
- 定位：CODE/SimulationRL.py:521
- 职责：统计卫星 `s` 当前发送缓冲区中按目的网关分组的积压块数 `{dest_id: count}`，结果按 `id(s)` 缓存在模块级 `_bp_backlog_cache`，`ttl` 秒（仿真时间）内直接复用缓存 (FACT)。
- 关键流程：缓存命中且未过期则返回（527–529）；否则遍历 `sendBufferSatsIntra`、`sendBufferSatsInter` 两个属性，对每个队列的 `q[1]` 里的块取 `blk.destination`，以其 `ID`（无 `ID` 时用 `id(d)`）计数（530–541）；写缓存后返回（542–543）。
- 输入/输出：Satellite 对象 + 当前仿真时间（+可选 ttl）→ dict。
- 依赖关系：被本文件 6913、6919 行调用（`SIM_BP_CORRECT` 的 per-commodity backpressure 决策分支）；docstring 525 行自述此用途，与调用点一致。

#### `def _resolve_input_rl_path(default="inputRL.csv") -> str` — CODE/SimulationRL.py:634
- 定位：CODE/SimulationRL.py:634
- 职责：返回 inputRL.csv 路径；env `SIM_INPUT_RL_PATH` 非空时优先 (FACT)。
- 输入/输出：可选默认路径 → 路径字符串。
- 依赖关系：被本文件 642（`__main__` 块）、12028 行调用。

#### `def _env_int(k, d)` — CODE/SimulationRL.py:734
- 定位：CODE/SimulationRL.py:734
- 职责：读 env 变量 `k` 并转 int，缺失或转换失败返回默认 `d` (FACT)。输入/输出：`(名字, 默认)` → int。依赖关系：仅被本文件模块级 745–803 行的配置解析调用（grep 全文 `_env_int(`/`_env_float(` 共 24 处匹配 = 2 行定义 + 22 处调用点，均在第 1–2471 行内）。

#### `def _env_float(k, d)` — CODE/SimulationRL.py:739
- 定位：CODE/SimulationRL.py:739
- 职责：同 `_env_int`，转换为 float (FACT)。输入/输出：`(名字, 默认)` → float。依赖关系：同 `_env_int`，仅模块级配置解析调用。

#### `def append_replay_event(earth, sim_time, kind, resource_id, block_id, u, v, queue_len=-1)` — CODE/SimulationRL.py:838
- 定位：CODE/SimulationRL.py:838
- 职责：向 `earth.replay_events` 追加一条 7 元组事件（全部转 str/int/float）；`REPLAY_TRACE` 为假或 `earth is None` 时直接返回；`earth` 无 `replay_events` 属性时现场创建空列表 (FACT)。
- 输入/输出：事件字段 → 无返回（副作用在 `earth.replay_events`）。
- 依赖关系：被本文件 1120（`_append_packet_fate_log` 内）、2160/2241/2306（`Satellite.receiveBlock`/`sendBlock`）、2646/2669/2748/2794（`class Gateway`（2573 行）内）、5137（`class Earth` 的 MBB GSL 切换分支）调用；读取全局 `REPLAY_TRACE`（694）。

#### `def _encode_od_pair(block)` — CODE/SimulationRL.py:890
- 定位：CODE/SimulationRL.py:890
- 职责：把块的源/目的编码成紧凑字符串：优先 `source.active_index`/`destination.active_index` 拼 `"s_d"`，失败回退 `source.ID_destination.ID`，再失败回退 `str(block.ID)` (FACT)。
- 输入/输出：DataBlock → 字符串。
- 依赖关系：被 `_append_decision_log`(1026)、`_append_packet_fate_log`(1124、1165)、本文件 2650 行（Gateway 内）调用。

#### `def _linked_mask_and_bf(linked_sats, actions=("U","D","R","L"))` — CODE/SimulationRL.py:905
- 定位：CODE/SimulationRL.py:905
- 职责：把 `{方向: 邻居或None}` 字典编成 `(位掩码, 可用方向数)` 二元组；任何异常返回 `(0,0)` (FACT)。
- 输入/输出：dict + 方向序列 → `(int mask, int bf)`。
- 依赖关系：被 `_append_decision_log`(1023) 调用；其它调用方未确认。

#### `def _append_state_log(agent, sat, block, state_vec)` — CODE/SimulationRL.py:918
- 定位：CODE/SimulationRL.py:918
- 职责：`_SIM_LOG_LEVEL>=3` 时把完整状态向量（float32 拉平成 list）连同 `(sim_time, sat.ID, block.ID)` 追加到 `agent.earth.state_log`，供状态混叠分析；任何异常静默吞掉 (FACT，docstring 919)。
- 输入/输出：agent/sat/block/状态向量 → 无返回。
- 依赖关系：被本文件 7162 行（DDQNAgent 决策路径）调用；行内注释（925–928）说明 `sat.ID` 必须以字符串存储以避免 `int("0_10")` 式碰撞。

#### `def _append_graph_state_log(earth, sat, block, stats)` — CODE/SimulationRL.py:937
- 定位：CODE/SimulationRL.py:937
- 职责：`_SIM_LOG_LEVEL>=1` 且 `_GRAPH_LOG_EVERY>0` 时，按 `_GRAPH_LOG_EVERY` 计数抽样，把 C4/C5 图状态的结构摘要（节点/边数、pad 比例、溢出节点数、U/D/R/L 四个 readout 计数、0–3 跳计数等 18 个字段）追加到 `earth.graph_state_log`；异常静默 (FACT)。
- 输入/输出：earth/sat/block/统计 dict → 无返回。
- 依赖关系：被本文件 9741 行调用；列模式对应 `_GRAPH_STATE_LOG_COLS`（876–881）。

#### `def _sample_raac_reliability(agent, state)` — CODE/SimulationRL.py:968
- 定位：CODE/SimulationRL.py:968
- 职责：按 `_GRAPH_LOG_EVERY` 对 RAAC 决策抽样：取 `agent._graph_encoder_layer()`，解析 state 张量，累加门控执行次数与可靠性权重的样本数/均值和/min/max 到 `earth._raac_*` 计数器上；docstring 称目的是让回执能证明 AoI reliability gate 真正执行过；异常静默 (FACT，docstring 969–975)。
- 输入/输出：agent + 状态张量 → 无返回。
- 依赖关系：被本文件 6863 行（DDQNAgent 决策路径）调用；调用 encoder layer 的 `_parse` 与 `_reliability_weights`（987–992）。

#### `def _append_decision_log(agent, sat, block, linked_sats, action_index, scores=None, explore_flag=False, epsilon_value=None)` — CODE/SimulationRL.py:1006
- 定位：CODE/SimulationRL.py:1006
- 职责：`_SIM_LOG_LEVEL>=2` 时追加一条逐决策行：`(sim_time, sat_id, block_id, od_pair, q0..q3, action_taken, linked_mask, effective_bf, explore, epsilon)` 到 `agent.earth.decision_log`；scores 形状不规则时拉平补齐/截断到 4 个；异常静默 (FACT)。
- 输入/输出：决策上下文 → 无返回。
- 依赖关系：调用 `_linked_mask_and_bf`(1023)、`_encode_od_pair`(1026)；被本文件 6832、6952 行（DDQNAgent）调用；列模式对应 `_DECISION_LOG_COLS`（853–857）。

#### `def _append_reward_log(earth, sat, block, queue_reward, distance_reward, again_reward, arrive_reward=0.0)` — CODE/SimulationRL.py:1035
- 定位：CODE/SimulationRL.py:1035
- 职责：`_SIM_LOG_LEVEL>=1` 时把本跳四项奖励之和累积到 `block._diag_local_rewards`；`_SIM_LOG_LEVEL>=2` 时再向 `earth.reward_log` 追加完整分解行（含 `queueTime` 末值、`_diag_TSL_prev/curr`）；异常静默 (FACT)。
- 输入/输出：奖励分量 → 无返回。
- 依赖关系：被本文件 7199、7272 行（DDQNAgent 奖励计算处）调用；列模式对应 `_REWARD_LOG_COLS`（858–862）。

#### `def _pc_flush_lost(earth, block)` — CODE/SimulationRL.py:1066
- 定位：CODE/SimulationRL.py:1066
- 职责：丢包时的轨迹收尾。`_SIM_MULTISTEP` 为真时改用 `earth.DDQNA._ms_flush_lost(block)` 冲刷 n-step 滑窗并返回（1075–1086）；否则在 `SIM_PATH_CREDIT` 开启、`earth.pc_replay` 存在、`block.pc_traj` 非空且未收尾过的前提下，置 `block.pc_terminal='lost'` 并把轨迹以 `terminal='lost'` 推入 `earth.pc_replay`（含 lost penalty）；失败时打印警告（每 earth 最多 3 次）(FACT，docstring 称它是所有丢包点的统一入口）。
- 输入/输出：earth/block → 无返回。
- 依赖关系：被本文件 2039（`Satellite.receiveBlock`）、2289（`Satellite.sendBlock` 中断发送丢失分支）、2781（Gateway）、4965/5069（`class Earth`）、7120（DDQNAgent）调用；读取 `_SIM_MULTISTEP`、`_SIM_PATH_CREDIT`、`_SIM_PATH_CREDIT_LOST_PENALTY`。

#### `def _append_packet_fate_log(earth, block, death_time, status)` — CODE/SimulationRL.py:1109
- 定位：CODE/SimulationRL.py:1109
- 职责：记录包的终态（`status` 0=送达、1=丢失）。若块带 `trace_packet_id`，校验终态不冲突——冲突直接 `raise RuntimeError`（1111–1118）；随后经 `append_replay_event` 写一条 RX/LS 事件（1119–1131）；`_SIM_LOG_LEVEL>=1` 时向 `earth.packet_fate_log` 追加行：路径依次取 `block.QPath`、`block.traversed_sats`（前置源网关名）、`block.path`，并算跳数、累计本地奖励、端到端时延 (FACT)。
- 输入/输出：earth/block/死亡时刻/状态 → 无返回。
- 依赖关系：调用 `append_replay_event`、`_encode_od_pair`；被本文件 2038、2288（Satellite）、2780/2861（Gateway）、4964/5068（Earth）、7119（DDQNAgent）调用；列模式对应 `_PACKET_FATE_COLS`（870–873）。

#### `def diagnostic_link_snapshot_process(env, earth, period=0.1)` — CODE/SimulationRL.py:1175
- 定位：CODE/SimulationRL.py:1175
- 职责：SimPy 进程：每 `period` 仿真秒醒一次，`_SIM_LOG_LEVEL>=1` 时对全部卫星采样 U/D/R/L 四方向出队长度（经 `outbound_queue_len_for_neighbor`）加下行 GT 缓冲长度共 5 列，以 float16 矩阵追加到 `earth.link_snap_log`；异常静默 (FACT)。
- 输入/输出：env/earth/周期 → 无限生成器。
- 依赖关系：被本文件 3666 行（`class Earth.__init__`，`_SIM_LOG_LEVEL>=1` 时启动）调用；依赖 `Satellite.outbound_queue_len_for_neighbor`（1975）。

#### `def _set_distance_diag(block, prev_sat, curr_sat, destination_sat)` — CODE/SimulationRL.py:1196
- 定位：CODE/SimulationRL.py:1196
- 职责：`_SIM_LOG_LEVEL>=2` 时把 `getSlantRange(prev_sat, dest)`、`getSlantRange(curr_sat, dest)` 写入 `block._diag_TSL_prev/curr`；任一方为 None 或异常时写 `np.nan` (FACT)。
- 输入/输出：块与三个卫星（可 None）→ 无返回。
- 依赖关系：被本文件 7171、7185、7248、7252、7256 行（DDQNAgent）调用；依赖 `getSlantRange`（定义于本文件 10261 行，属后续片段）。

#### `def _dump_diag_log(rows, columns, out_dir, base_name)` — CODE/SimulationRL.py:1207
- 定位：CODE/SimulationRL.py:1207
- 职责：把元组列表写成 parquet（snappy），pyarrow 不可用时回退 `.csv.gz`；空输入或异常返回 None 并打印，成功返回文件路径 (FACT，docstring 1208–1214)。
- 输入/输出：行列表+列名+目录+基名 → 路径或 None。
- 依赖关系：仅被 `flush_replay_trace`（1289–1298）调用。

#### `def _dump_link_snapshots(rows, out_dir, base_name="link_snapshots")` — CODE/SimulationRL.py:1234
- 定位：CODE/SimulationRL.py:1234
- 职责：把周期链路快照行 `(sim_time, queues[N×K], active_flows|None, hotspot_intensity|None)` 写成单个压缩 `.npz`（`sim_time` float32、`queues` float16，后两者可选）；空输入/异常返回 None (FACT，docstring 1235–1239)。
- 输入/输出：行列表+目录(+基名) → 路径或 None。
- 依赖关系：仅被 `flush_replay_trace`（1296）调用。

#### `def flush_replay_trace(earth, output_path, meta=None)` — CODE/SimulationRL.py:1259
- 定位：CODE/SimulationRL.py:1259
- 职责：把整轮运行痕迹写到 `<output_path>/run_trace/`：`replay_events.csv`（1266–1270）、可选 `run_meta.json`（1271–1273）、`graph_snapshot.json`（取 `earth.graph`，缺省回退 `earth.gateways[0].graph`，node-link JSON，失败打印跳过，1275–1284）；`_SIM_LOG_LEVEL>=1` 时转储 7 类诊断日志与链路快照（1288–1296），`>=3` 时再转储 state_log（1297–1298）；`_SIM_PATH_CREDIT` 开启时把 `earth.pc_log` 写成 `pc_log.csv.gz`（1300–1321）(FACT，docstring 1260)。
- 输入/输出：earth/输出目录/可选元信息 dict → 无返回。
- 依赖关系：调用 `_dump_diag_log`、`_dump_link_snapshots` 与各 `_*_LOG_COLS` 常量；被本文件 11396、12295 行（收尾/主流程）调用。

#### `def getBlockTransmissionStats(timeToSim, GTs, constellationType, earth)` — CODE/SimulationRL.py:1324
- 定位：CODE/SimulationRL.py:1324
- 职责：汇总全部已收块的传输统计并落盘 (FACT)。
- 关键流程：遍历全局 `receivedDataBlocks`：算总时延、跳数，逐块包成 `BlocksForPickle`，记录最大时延/最多跳数块，累积 queue/tx/prop 时延与 `allLatencies` 行；对源==`gateways[0]` 且目的==`gateways[1]` 的块单独收进 `pathBlocks`（1343–1365）；在 `outputPath + '/Congestion_Test/'` 下用 `_atomic_save_npy`（`allow_pickle=True`）保存 `blocks_{CurrentGTnumber}.npy`，`pickle.PicklingError` 时打印错误（1370–1376）；打印运行时长、创建/送达/滞留块数、平均时延与三类时延占比（1391–1400）；构造并返回 `Results`（1402–1413）。注意：1341 行有一行裸表达式 `earth.pathParam`，无赋值无副作用 (FACT)；函数读取模块全局 `outputPath`（仅在 `__main__` 块 653 行赋值）与 `CurrentGTnumber`（1373 行 `global` 声明）(FACT)。
- 输入/输出：`(耗时, GTs参数, 星座类型, earth)` → `(results, allLatencies, pathBlocks, blocks)` 四元组。
- 依赖关系：调用 `BlocksForPickle`（1771）、`Results`（1756）、`_atomic_save_npy`（58）；读取全局 `receivedDataBlocks`、`createdBlocks`、`outputPath`、`CurrentGTnumber`；被本文件 12292 行（主流程非 "Rates" 分支）调用。

#### `def simProgress(simTimelimit, env)` — CODE/SimulationRL.py:1416
- 定位：CODE/SimulationRL.py:1416
- 职责：SimPy 进程：把仿真时长切成 100 步，每步打印一次进度百分比、估计剩余墙钟时间与当前仿真时刻（`\r` 同行刷新）(FACT)。
- 输入/输出：仿真时限+env → 无限生成器。
- 依赖关系：被本文件 12177 行（主流程）调用。

#### `def generate_test_data(num_samples, include_not_avail=False)` — CODE/SimulationRL.py:1448
- 定位：CODE/SimulationRL.py:1448
- 职责：生成合成状态样本矩阵 (FACT)。
- 关键流程：每样本：`diff_lastHop` 为真时先放 1 个 0–4 随机整数（1456–1457）；对 4 个方向各放 4 个按偏态分布（0 取 35%、10 取 20%、1–9 各 5%）抽取的队列值加 2 个 [-2,2] 均匀分布的相对位置（1459–1465）；再放 2 个绝对位置（[0,9]、[0,18]）与 2 个目的差分坐标（[-2,2]）（1467–1473）；`include_not_avail` 时以 10% 概率把样本中 10% 的分量置 -1（1476–1478）。维度合计 28（`diff_lastHop` 假）或 29（真）(FACT，由 1456–1473 行的拼接结构算出）。
- 输入/输出：样本数(+开关) → `np.array`，形状 `(num_samples, 28|29)`。
- 依赖关系：被 `perform_FL`（1592）调用；读取全局 `diff_lastHop`（334）；其它调用方未确认。

#### `def get_models(earth)` — CODE/SimulationRL.py:1484
- 定位：CODE/SimulationRL.py:1484
- 职责：遍历 `earth.LEO` 各轨道面各卫星，收集每星的 `DDQNA.qNetwork` 与卫星 `ID`，返回 `(models, model_names)` (FACT)。
- 输入/输出：earth → 两个等长列表。
- 依赖关系：仅被 `perform_FL`（1593）调用。

#### `def average_model_weights(models)` — CODE/SimulationRL.py:1493
- 定位：CODE/SimulationRL.py:1493
- 职责：对多个 Keras 模型逐层逐张量取权重的逐元素均值，返回新的权重列表 (FACT)。
- 输入/输出：模型列表 → 权重列表（与单模型 `get_weights()` 结构相同）。
- 依赖关系：被 `full_federated_learning`（1500）、`federate_by_plane`（1514）调用。

#### `def full_federated_learning(models)` — CODE/SimulationRL.py:1499
- 定位：CODE/SimulationRL.py:1499
- 职责：全局联邦平均：算全部模型的平均权重并写回每个模型 (FACT)。
- 输入/输出：模型列表 → 无返回（就地 `set_weights`）。
- 依赖关系：调用 `average_model_weights`；被 `perform_FL`（1605、1621）调用。

#### `def federate_by_plane(models, model_names)` — CODE/SimulationRL.py:1504
- 定位：CODE/SimulationRL.py:1504
- 职责：按轨道面联邦平均：用 `name.split('_')[0]` 分组，每组内算平均权重并写回组内模型 (FACT)。
- 输入/输出：模型列表+名字列表 → 无返回。
- 依赖关系：调用 `average_model_weights`；被 `perform_FL`（1603、1616）调用。

#### `def model_anticipation_federate(models, model_names)` — CODE/SimulationRL.py:1518
- 定位：CODE/SimulationRL.py:1518
- 职责：模型预期式联邦：按轨道面分组、组内按 `int(name.split('_')[1])` 排序，从第 2 个模型起，每个模型的权重更新为「自身与前一个模型对应权重的逐元素均值」 (FACT，docstring 1519)。
- 输入/输出：模型列表+名字列表 → 无返回。
- 依赖关系：被 `perform_FL`（1601、1611）调用。

#### `def update_sats_models(earth, models, model_names)` — CODE/SimulationRL.py:1540
- 定位：CODE/SimulationRL.py:1540
- 职责：把（可能已联邦更新过的）模型写回各卫星：`findByID` 定位卫星后赋给 `sat.DDQNA.qNetwork`；全局 `ddqn` 为真时同时赋给 `sat.DDQNA.qTarget` (FACT)。
- 输入/输出：earth+模型列表+名字列表 → 无返回。
- 依赖关系：调用 `findByID`（定义于本文件 9010 行，属后续片段）；读取全局 `ddqn`（555）；被 `perform_FL`（1624）调用；本文件 7481 行注释提及模型对象可能被本函数替换。

#### `def compute_full_cka_matrix(models, data)` — CODE/SimulationRL.py:1549
- 定位：CODE/SimulationRL.py:1549
- 职责：计算模型两两之间的 CKA 矩阵 (FACT，docstring 1550)。
- 关键流程/嵌套函数：`gram_matrix(X)`(1552) 对激活按列去均值后算 `X@X.T/n`；`cka(G,H)`(1558) 返回 `tr(G@H)/sqrt(tr(G@G)*tr(H@H))`；`compute_cka(model1,model2,data)`(1562) 为每个模型搭建以全部层输出为输出的中间模型，前向 `data` 后对对应层激活两两算 CKA 并取均值；主体（1570–1578）填对称矩阵，对角线置 1。
- 输入/输出：模型列表+数据 → `(n,n)` ndarray。
- 依赖关系：被 `perform_FL`（1595、1623）调用。

#### `def compute_average_cka(cka_matrix)` — CODE/SimulationRL.py:1580
- 定位：CODE/SimulationRL.py:1580
- 职责：取 CKA 矩阵严格上三角（k=1）的均值 (FACT)。
- 输入/输出：方阵 → 标量。
- 依赖关系：被 `plot_cka_over_time_v0`（1642、1643）调用；其它调用方未确认。

#### `def perform_FL(earth)` — CODE/SimulationRL.py:1585
- 定位：CODE/SimulationRL.py:1585
- 职责：联邦学习编排：生成测试数据、收集各星模型、算联邦前 CKA、按全局 `FL_tech` 执行 `'nothing'/'modelAnticipation'/'plane'/'full'/'combination'` 五种策略之一（`'combination'` 用全局 `FL_counter` 轮转 modelAnticipation→plane→full）、算联邦后 CKA、把模型写回卫星，返回 `(CKA_before, CKA_after)`；`'nothing'` 时提前返回两个相同矩阵 (FACT)。
- 输入/输出：earth → 两个 `(n,n)` CKA 矩阵。
- 依赖关系：调用 `generate_test_data`、`get_models`、`compute_full_cka_matrix`、三个 federate 函数、`update_sats_models`；读写全局 `FL_tech`（1435）、`FL_counter`（1438）、`num_samples`（1445）；被本文件 5296 行（`class Earth` 的 `moveConstellation`（5183 行）内，`FL_Test` 门控）调用。

#### `def plot_cka_over_time_v0(cka_data, outputPath, nGTs)` — CODE/SimulationRL.py:1629
- 定位：CODE/SimulationRL.py:1629
- 职责：画 CKA 随时间（毫秒）折线+散点图：每时刻的 before/after 均值（经 `compute_average_cka`）用灰色虚线相连，蓝/绿点区分前后；图存 `<outputPath>/FL/CKA_over_time_<nGTs>_GTs`（无扩展名，`savefig` 默认 png），并把均值序列写 `mean_cka_values.csv`、逐时刻 CKA 矩阵写 `cka_matrix_before/after_<i>.csv` (FACT，docstring 1630–1636)。
- 输入/输出：`[CKA_before, CKA_after, timestamp]` 列表+输出路径+网关数 → 无返回（写文件）。
- 依赖关系：调用 `compute_average_cka`；调用方未确认（同文件与 CODE/ 下 grep 均无调用点，只有 1679 行的 `plot_cka_over_time` 被主流程 12430 行调用）。

#### `def plot_cka_over_time(cka_data, outputPath, nGTs)` — CODE/SimulationRL.py:1679
- 定位：CODE/SimulationRL.py:1679
- 职责：v0 的带误差棒版本：before/after 用各时刻矩阵的均值（`np.mean`，注意此处不是 `compute_average_cka`）与 25/75 百分位误差棒（T 形帽），灰点划线连接均值序列；存 `CKA_over_time_<nGTs>_GTs.png`，并同样写 `mean_cka_values.csv` 与逐时刻矩阵 csv (FACT，docstring 1680–1686；`plt.ylim` 被 1728 行注释掉，故 1706–1707 算出的 y 范围未生效）。
- 输入/输出：同 v0 → 无返回（写文件）。
- 依赖关系：被本文件 12430 行（主流程，`FL_Test` 分支）调用。

#### `class Results` — CODE/SimulationRL.py:1756
- 定位：CODE/SimulationRL.py:1756
- 职责：一轮仿真汇总结果的纯数据容器 (FACT)。
- 关键状态/结构：`GTs`、`finishedBlocks`、`constellation`、`meanTotalLatency`、`meanQueueLatency`、`meanPropLatency`、`meanTransLatency`、`perQueueLatency`、`perPropLatency`、`perTransLatency`。
- 关键流程/方法：仅 `__init__`(1757)，把 10 个参数原样存为同名属性。
- 输入/输出：构造吃 10 个统计字段 → 实例。
- 依赖关系：被 `getBlockTransmissionStats`（1402）实例化；其它实例化点未确认。

#### `class BlocksForPickle` — CODE/SimulationRL.py:1771
- 定位：CODE/SimulationRL.py:1771
- 职责：DataBlock 的可 pickle 精简拷贝，只保留落盘所需字段 (FACT，INFERENCE：类名与字段选择暗示用途为 pickle 落盘，实例确被 `_atomic_save_npy(..., allow_pickle=True)` 写入，见 1374/11436/12470 行上下文）。
- 关键状态/结构：`size`（取全局 `BLOCK_SIZE`）、`ID`、`timeAtFull`、`creationTime`、`timeAtFirstTransmission`、`checkPoints`、`checkPointsSend`、`path`、`queueLatency`、`txLatency`、`propLatency`、`totLatency`、`QPath`、`source_name`、`destination_name`。
- 关键流程/方法：仅 `__init__`(1772)，逐字段从传入 block 拷贝；拷贝前先尝试调用 `block.getQueueTime()` 以填充 `queueLatency`（1785–1788，行内注释称 eval/interrupt 路径此前从未调用过导致 queue 字段恒为占位 0；调用被 try 包裹，失败静默）。
- 输入/输出：一个 DataBlock → 实例。
- 依赖关系：被 `getBlockTransmissionStats`（1346）与本文件 11434、12470 行实例化；读取全局 `BLOCK_SIZE`（318）。

#### `class RFlink` — CODE/SimulationRL.py:1798
- 定位：CODE/SimulationRL.py:1798
- 职责：RF 链路的链路预算参数容器，构造时从物理参数算出收发天线增益、总增益、噪声功率与 G/T (FACT，各字段物理含义由 `__repr__` 的输出标签佐证：Carrier frequency/Bandwidth/Transmission power/Gain per antenna/Total antenna gain/Noise power/G-T，1815–1824）。
- 关键状态/结构：`f`、`B`、`maxPtx`、`maxPtx_db`、`Gtx`、`Grx`、`G`、`No`、`GoT`、`min_rate`。
- 关键流程/方法：`__init__`(1799) 用全局 `eff`、`Vc`、`k` 由口径与频率算 `Gtx/Grx`（dB）、`G = Gtx+Grx-2*pointingLoss`、`No`（带宽×玻尔兹曼常数+噪声系数+噪声温度修正）、`GoT`；`__repr__`(1814) 返回多行参数串。
- 输入/输出：9 个链路参数 → 实例。
- 依赖关系：被 `Satellite.__init__`（1935，建 `ngeo2gt`）、`class Gateway`（2617，建 `gs2ngeo`）、本文件 8353（`markovianMatchingTwo`）、8459（`greedyMatching`）、8594（`establishRemainingISLs`）实例化（后三处建 ISL 链路对象）；其字段被 `Satellite.adjustDownRate`（2383–2388）读取。

#### `class FSOlink` — CODE/SimulationRL.py:1827
- 定位：CODE/SimulationRL.py:1827
- 职责：FSO（自由空间光）链路参数容器，仅存 4 个字段 (FACT；「FSO=自由空间光」为 INFERENCE，由类名与 `__repr__` 标签 Data rate/Power/Transmission range/Weight 推测）。
- 关键状态/结构：`data_rate`、`power`、`comm_range`、`weight`。
- 关键流程/方法：`__init__`(1828) 存 4 个参数；`__repr__`(1834) 返回多行参数串（Mbps/W/km/kg）。
- 输入/输出：4 个参数 → 实例。
- 依赖关系：实例化点未确认（同文件与 CODE/ 下 grep 均未找到 `FSOlink(` 调用）。

#### `class OrbitalPlane` — CODE/SimulationRL.py:1842
- 定位：CODE/SimulationRL.py:1842
- 职责：一个轨道面：保存轨道几何与运动学参数，构造时创建该面全部 `Satellite`，并提供按地球自转推进的 `rotate` (FACT)。
- 关键状态/结构：`ID`、`h`（高度）、`longitude`（升交点经度，弧度）、`inclination`（存 `π/2 − 传入值`）、`n_sat`、`period`（由 `Re/G/Me` 算的开普勒周期）、`v`（轨道速度）、`min_elev`、`max_alpha`、`max_beta`、`max_distance_2_ground`、`earth`、`first_sat_ID`、`sats`、`last_sat_ID`。
- 关键流程/方法：`__init__`(1843) 计算上述参数并循环创建 `n_sat` 个 `Satellite`（ID 为 `firstID + str(i)`，1861–1862）；`__repr__`(1866) 返回多行参数串；`rotate(delta_t)`(1876) 把 `longitude` 推进 `2π·delta_t/Te` 并取模，再对面内每星调 `sat.rotate(delta_t, self.longitude, self.period)`。
- 输入/输出：`(ID, h, longitude, inclination, n_sat, min_elev, firstID, env, earth)` → 实例。
- 依赖关系：被本文件 8223 行（`create_Constellation`（8135 行）内）实例化；`rotate` 被 3671（`Earth.__init__` 的 `rotateFirst` 分支）、5237（`Earth.moveConstellation`）调用；创建 `Satellite`（1891）。

#### `class Satellite` — CODE/SimulationRL.py:1891
- 定位：CODE/SimulationRL.py:1891（本片段覆盖到 2470 行方法体结束；下一个顶层 `class edge` 在 2472 行，故 Satellite 全部成员均在本范围内）
- 职责：星座中的一颗卫星：保存轨道位置/坐标、对地与星间链路及发送缓冲区，承载收/发数据块的 SimPy 进程，并在 RL 模式下驱动下一跳决策 (FACT)。
- 关键状态/结构：身份与轨道（`ID`、`orbPlane`、`in_plane`、`i_in_plane`、`quota`、`h`、`power`、`minElevationAngle`、球坐标 `r/theta/phi`、笛卡尔 `x/y/z`、`latitude/longitude`、`polar_angle`）；链路（`ngeo2gt`（RFlink）、`downRate`、`linkedGT`、`GTDist`、`retiring_gt_links`、`intraSats`、`interSats`、`linked/upper/lower/right/left`（后四者由 find*Neighbours 设置））；SimPy 缓冲（`env`、`sendBufferGT=([event],[])`、`sendBlocksGT`、`sendBufferSatsIntra/Inter`、`sendBlocksSatsIntra/Inter`、`tempBlocks`、`newBuffer=[False]`）；RL（`QLearning=None`、`DDQNA=None`、`maxSlantRange`）；其它（`waiting_list`、`applications`、`n_sat`）。
- 关键流程/方法（逐方法）：
  - `__init__`(1892)：按面内索引与经度算球坐标，转成考虑倾角后的笛卡尔坐标与经纬度（1902–1929）；初始化上述全部缓冲/链路字段；建 `ngeo2gt` RFlink（1935）；算 `maxSlantRange`（1961）。
  - `GetmaxSlantRange`(1963)：按最小仰角算覆盖边缘最大斜距 `sqrt((Re+h)^2-(Re·cos ε)^2) − Re·sin ε`（docstring 给出公式出处为 NGSO 星座设计章节）；仅被 `__init__`（1961）调用。
  - `outbound_queue_len_for_neighbor`(1975)：在 `sendBufferSatsIntra/Inter` 中按 `buffer[2]==int(neighbor.ID)` 匹配，累加对应队列长度；`neighbor_sat is None` 返回 0.0；被 `diagnostic_link_snapshot_process`（1188）与本文件 8850 行调用。
  - `__repr__`(1992)：返回 ID/轨道/坐标/经纬度的多行串。
  - `createReceiveBlockProcess`(2011)：为 `receiveBlock(block, propTime)` 起一个 SimPy 进程；被 `Satellite.sendBlock`（2342）与 `Gateway.sendBlock`（2811）调用。
  - `receiveBlock`(2017)：SimPy 进程——块先入 `tempBlocks`，`timeout(propTime)` 模拟传播时延；若 `block.path == -1`（传输期间被取消）则记 fate(status=1)、`_pc_flush_lost` 后返回（2038–2041）；累加 `propLatency`、移出 `tempBlocks`、追加 `queueTime`（用最近一对 checkPointsSend/checkPoints 差，IndexError 静默）与 `checkPoints`、`traversed_sats`（2034–2062）；若本星挂有 QLearning 或（自身/地球的）DDQNA，则调 `makeAction`/`makeDeepAction` 选下一跳并插到 `block.QPath` 倒数第二位，`plotPaths` 开时按块 ID 末位为 0 抽样画路径图（2068–2099）；否则 `oracle_global_dijkstra` 模式下用 `getShortestPath` 重算 `block.path`（2103–2106）；然后在路径中定位自身下标（找不到则打印路径，2110–2116）：若下一跳是目的网关（路径倒数第二位）则放入 `sendBufferGT`，否则在 `intraSats/interSats` 中找下一跳卫星、把目标缓冲当前长度记入 `earth.queues` 与 `block.queue`、写 JQ replay 事件、放入对应 ISL 发送缓冲（2119–2178）；下一跳不在邻居表则打印 ERROR（2180–2183）。
  - `sendBlock`(2185)：SimPy 进程主循环——按 `(destination, isSat, isIntra)` 或关键字 `send_buffer` 定位发送缓冲（2199–2213）；等待缓冲事件后给首块追加 `checkPointsSend`、写 SS replay 事件（2217–2250）；发送时长=块大小/速率（ISL 用 `destination[2]`、下行用 `link_context` 速率或 `downRate`，下限 1.0），传播时延经 `timeToSend`（2252–2266）；若 `earth._link_outage` 存在且发送窗口撞上中断：起点已中断则等待中断结束重试，传输中失败则记 `_link_outage_losses`/`lostBlocks`、fate(status=1)、`_pc_flush_lost`、弹出缓冲后续发（2268–2299）；正常 `timeout(timeToSend)` 后写 ST 事件（2301–2308）；若 `newBuffer` 有 True（星座移动后缓冲被重建）且为 inter 星间链路进程，则重新按 destination 查找缓冲引用并清一位标记（2319–2338）；累加 `txLatency`、调 `receiver.createReceiveBlockProcess` 投递、弹出已发块（缓冲空则补一个新 event）；`drain_once` 且缓冲空则退出循环；`simpy.Interrupt` 时退出循环（2340–2359）。
  - `adjustDownRate`(2361)：内置三张 DVB-S2X 式阈值表（频谱效率/线性/dB，2363–2381）；由 `linkedGT.linkedSat[0]` 的距离算自由空间路损与 SNR、香农速率（2383–2385；`shannonRate` 算出后未被后续读取 (FACT)）；取不超过 SNR 的最高可行频谱效率乘带宽写入 `self.downRate`（2387–2390）。被本文件 4016、4388、4887、5158、8006 行（Earth 的建链/换链流程）调用。
  - `timeToSend`(2392)：传播时延 = `linkedSat[0]`（距离）/光速 `Vc`；被本类 `sendBlock`（2255、2263、2266）调用（2822 行另有 Gateway 自己的同名方法，与本方法无关）。
  - `findIntraNeighbours`(2400)：设置面内邻居——`linked=None`、`upper`=同面前一星（`i_in_plane-1`）、`lower`=同面后一星（末星回绕到 0 号）（2404–2409）；被本文件 4543、8416、8517、8716 行调用。
  - `findInterNeighbours`(2411)：在 `earth.graph` 的邻边中按 `getDirection` 找东（dir==3）西（dir==4）向星间邻居写入 `right/left`；南北向（1/2）与 GT 边跳过；方向无法识别时打印 (FACT，2415–2437)；被本文件 4544、7999、8717 行调用。
  - `rotate`(2439)：按 `delta_t` 推进面内角 `theta += 2π·delta_t/period`、更新 `phi`，重算笛卡尔坐标、`polar_angle`、纬度与经度（与 `__init__` 同一套象限分支）；被 `OrbitalPlane.rotate`（1887）调用。
- 输入/输出：构造吃 `(ID, in_plane, i_in_plane, h, longitude, inclination, n_sat, env, orbitalPlane, quota=500, power=10)` → 实例；收发方法吃 DataBlock 并驱动 SimPy 事件流。
- 依赖关系：仅被 `OrbitalPlane.__init__`（1862）实例化（全文唯一 `Satellite(` 调用点）；被调方包括 `RFlink`（1935）、`append_replay_event`（2160/2241/2306）、`_append_packet_fate_log`（2038/2288）、`_pc_flush_lost`（2039/2289）、`plotShortestPath`（2098，定义于 8968 行）、`getShortestPath`（2104，定义于 8903 行）、`findByID`（2071 等，定义于 9010 行）、`getDirection`（2422，定义于 9266 行）、`getSlantRange`（经 `_set_distance_diag` 间接）；`makeAction`/`makeDeepAction` 由 `QLearning`/`DDQNA` 对象提供（类定义在后续片段）。

---

### 覆盖核对清单（定义行 ∈ [1,2471]）

- class（7/7）：`Logger`(173)、`Results`(1756)、`BlocksForPickle`(1771)、`RFlink`(1798)、`FSOlink`(1827)、`OrbitalPlane`(1842)、`Satellite`(1891)。
- def（41/41）：`_array_sha256`(35)、`_canonical_json_sha256`(50)、`_atomic_save_npy`(58)、`_results_dir_traffic_od_tag`(88)、`_sanitize_run_label_for_path`(124)、`_safe_next_action_mask`(404)、`_masked_target_dqn_values`(425)、`_masked_double_dqn_actions`(434)、`_bp_backlog_counts`(521)、`_resolve_input_rl_path`(634)、`_env_int`(734)、`_env_float`(739)、`append_replay_event`(838)、`_encode_od_pair`(890)、`_linked_mask_and_bf`(905)、`_append_state_log`(918)、`_append_graph_state_log`(937)、`_sample_raac_reliability`(968)、`_append_decision_log`(1006)、`_append_reward_log`(1035)、`_pc_flush_lost`(1066)、`_append_packet_fate_log`(1109)、`diagnostic_link_snapshot_process`(1175)、`_set_distance_diag`(1196)、`_dump_diag_log`(1207)、`_dump_link_snapshots`(1234)、`flush_replay_trace`(1259)、`getBlockTransmissionStats`(1324)、`simProgress`(1416)、`generate_test_data`(1448)、`get_models`(1484)、`average_model_weights`(1493)、`full_federated_learning`(1499)、`federate_by_plane`(1504)、`model_anticipation_federate`(1518)、`update_sats_models`(1540)、`compute_full_cka_matrix`(1549)、`compute_average_cka`(1580)、`perform_FL`(1585)、`plot_cka_over_time_v0`(1629)、`plot_cka_over_time`(1679)。
### 文件 `CODE/SimulationRL.py`（实测 12556 行）— 本片段覆盖第 2472–5637 行

模块级说明：无（本片段范围为第 2472–5637 行；文件头部的 imports、全局常量、环境变量读取位于第 1–2471 行，由前序片段覆盖）。以下为衔接用的事实清单：本片段代码引用到、但定义点在本片段范围之外的符号（FACT，行号为定义/读取位置）：

- 全局常量/列表：`BLOCK_SIZE = 64800`（318）；`receivedDataBlocks = []`（673）；`createdBlocks = []`（674）；`Re = 6378e3`（293）；`Vc = 299792458`（297）；`balancedFlow`（313）、`totalFlow`（314）、`avUserLoad`（315）；`pathing`（225–226，读 `SIM_PATHING`，默认 `'slant_range'`）；`plotPath = False`（557）；`matching = 'Greedy'`（326）；`saveISLs = True`（324）；`rotateFirst = False`（329）；`ndeltas = 5805.44/20`（241）；`importQVals = False`（262）；`tablesPath`（631）；`plotSatID = True`（235）；`FL_Test = False`（234）；`const_moved = False`（325）；`upGSLRates`/`downGSLRates`/`interRates`/`intraRate`（688–691）。
- env 读取的模块级开关：`_SIM_FAIL_CLOSED`（219，`SIM_FAIL_CLOSED`）；`_SEED`（680，`SIM_SEED`，默认 42）；`_SIM_LOG_LEVEL`（715–719，`SIM_LOG_LEVEL`）；`_SIM_GSL_HANDOVER_MODE`（744，`SIM_GSL_HANDOVER_MODE`，默认 `"legacy"`）；`_SIM_GSL_HANDOVER_MAX_RETIRING_LINKS`（745）；`_SIM_GSL_KEEP_STABLE`（746，默认开）；`_SIM_PATH_CREDIT`（753）；`_SIM_PATH_CREDIT_BUFFER_MAXLEN`（760）；`_SIM_PATH_CREDIT_MAX_HOPS`（762）。
- 同文件模块级函数：`_canonical_json_sha256`(50)、`append_replay_event`(838)、`_encode_od_pair`(890)、`_pc_flush_lost`(1066)、`_append_packet_fate_log`(1109)、`diagnostic_link_snapshot_process`(1175)、`perform_FL`(1585)、`create_Constellation`(8135)、`createGraph`(8655)、`getShortestPath`(8903)、`plotShortestPath`(8968)、`findByID`(9010)、`getLinkedSats`(9328)。
- 同文件其他类：`RFlink`(1798)、`Satellite`(1891)、`QLearning`(5682)、`hyperparam`(5638)。
- 跨文件 import（均在文件头部）：`traffic_od` 的 `build_od_matrix_for_gateways`/`load_traffic_config_from_env`/`traffic_mode_needs_gateway_physical`（20–23 行 import 块）；`traffic_burst.load_burst_schedule_from_env`(25)；`traffic_diurnal.load_diurnal_schedule_from_env`(26)；`runtime_effect_receipt.new_checkpoint_receipt`（27–31 行 import 块）；`scipy.optimize.linear_sum_assignment`(10)；`PIL.Image`(9)；`geopy.distance`(5)；`collections.defaultdict`(154)；`typing.Optional`(149)。
- 函数体内局部 import：`link_outage.load_link_outage_schedule_from_env`（3398 行，`CODE/link_outage.py` 存在）；`routing_path_credit.PathTrajectoryReplay`（3416 行，`CODE/routing_path_credit.py` 存在）；`temporal_encoder`（5263 行，`CODE/temporal_encoder.py` 存在）；`legacy_trace_runtime.load_and_project_trace`（3682 行，`CODE/legacy_trace_runtime.py` 存在）。
- 模块级名 `outputPath` 仅在 `if __name__ == '__main__':` 块（640 行）内的 653 行赋值；本片段 5287 行以裸名引用它（FACT）。

---

#### `class edge` — CODE/SimulationRL.py:2472

- 定位：CODE/SimulationRL.py:2472（类体 2472–2494）
- 职责：保存两颗卫星之间一条链路的属性的数据容器（INFERENCE——类无 docstring，依据属性名与实例化点上下文）。`__init__` docstring 自述：`dji`/`dij` 已弃用，不再用于判断左右邻居（改用坐标），仅用于 markovian matching（2474–2477，FACT 引自 docstring）。
- 关键状态/结构：`self.i`/`self.j`（两端卫星 ID，2478–2479）、`self.slant_range`（两星距离，2480）、`self.dji`/`self.dij`（方向标记，2481–2482）、`self.shannonRate`（两星间最大数据率，2483）。
- 关键流程/方法：
  - `__init__`(2473)：把 6 个形参存为同名属性（2478–2483）。
  - `__repr__`(2485)：返回包含 i、j、slant_range、shannonRate 的格式化字符串（2486–2490）。
  - `__cmp__`(2492)：Python 2 风格比较方法；当 `other` 有 `slant_range` 属性时，按自身 `slant_range` 与之比较（2492–2494）。该方法的注释写「returns true if has 'weight' attribute」，与代码实际检查的 `slant_range` 不一致（FACT，2493 行注释）。Python 3 的 `list.sort()`/`sorted()` 不读取 `__cmp__`；本文件内未见对 `__cmp__` 的显式调用（FACT，基于全文件 Grep）。
- 输入/输出：构造输入 = `(sati, satj, slant_range, dji, dij, shannonRate)`；无计算产出，作为数据记录被存入列表。
- 依赖关系：实例化点全部在本片段范围外——`markovianMatchingTwo`（定义于 8330）内的 8398、8422、8430 行（`W_M.append(edge(...))` / `_A_Markovian.append(edge(...))`）与 `greedyMatching`（定义于 8438）内的 8508、8510、8523、8531 行（`_A_Greedy.append(edge(...))`）（FACT）。`__cmp__` 的消费方未确认。

---

#### `class DataBlock` — CODE/SimulationRL.py:2497

- 定位：CODE/SimulationRL.py:2497（类体 2497–2569）
- 职责：网关（GT）间聚合数据块。docstring 自述：不逐个模拟各用户数据包，而是在 GT 处按目的 GT 聚合成块，填满后作为一个单元发往目的 GT（2498–2502，FACT 引自 docstring）。
- 关键状态/结构（全部在 `__init__` 中初始化，2504–2532）：`size`（比特数，取全局 `BLOCK_SIZE`，2505）；`destination`/`source`；`ID`（字符串，形如 `"1_2_12"` = 源ID_目的ID_块序号，2508 注释）；`timeAtFull`/`creationTime`/`timeAtFirstTransmission`（2509–2511）；`checkPoints`（各节点接收时刻列表）与 `checkPointsSend`（各节点发送完成时刻列表）（2512–2513）；`path`/`oldPath`/`newPath`/`QPath`（2514、2520–2522）；时延字段 `queueLatency`（初值 `(None, None)`）、`txLatency`、`propLatency`、`totLatency`（2515–2518）；`isNewPath`（2519）；`traversed_sats`（逐接收点追加的路由无关遍历日志，2523）；`queue`/`queueTime`（2524–2525）；`oldState`/`oldAction`（2526–2527）；path-credit 字段 `pc_traj`/`pc_terminal`（2530–2531，注释自述所有访问由 `_SIM_PATH_CREDIT` 门控，2529）；`ms_buf`（n-step 基线的滑动窗口，注释指向 `DDQNAgent._ms_store`，2532）。
- 关键流程/方法：
  - `__init__`(2504)：初始化上述全部字段（2504–2532）。
  - `getQueueTime`(2534)：按 docstring 的两步式计算排队时延——第一步 = `timeAtFirstTransmission - creationTime`，其后每步 = `checkPointsSend[i] - checkPoints[i]` 累加（2535–2545）；把 `[总值, 分段明细列表]` 写入 `self.queueLatency` 并返回（2540–2548）。
  - `getTotalTransmissionTime`(2550)：若只有 1 个 checkpoint，返回 `checkPoints[0] - timeAtFirstTransmission`（2552–2553）；否则从 `creationTime` 起对相邻 checkpoint 差值求和，写入 `self.totLatency` 并返回（2555–2561）。
  - `__repr__`(2563)：返回含 ID、Source、Destination、totLatency 的字符串（2563–2569）。
- 输入/输出：构造输入 = `(source, destination, ID, creationTime)`（Gateway/DataBlock 实例 + 字符串 + 仿真时刻）；两个计算方法输出时延数值/列表。
- 依赖关系：实例化于 `Gateway.fillBlock`（2696 行）与 `Earth._dispatchTraceRows`（3724 行）（FACT）；测试中经 `sim.DataBlock(...)` 构造（CODE/tests/test_runtime_effect_receipt.py:630）。`getQueueTime`/`getTotalTransmissionTime` 被 `getBlockTransmissionStats`（定义于 1324；调用点 1344、1356、1361）与 `BlocksForPickle`（定义于 1771；调用点 1786）调用（FACT）。读取全局 `BLOCK_SIZE`（318）。

---

#### `class Gateway` — CODE/SimulationRL.py:2573

- 定位：CODE/SimulationRL.py:2573（类体 2573–3256）
- 职责：网关/集中器。docstring 自述：每个地面站是本类一个实例，各自运行独立的进程向所有其他 GT 填充并发送数据块（2574–2577，FACT 引自 docstring）。
- 关键状态/结构：
  - 标识与位置：`name`/`ID`/`earth`/`latitude`/`longitude`（2579–2583）；网格坐标 `gridLocationX`/`gridLocationY`（2586–2587）；`cellsInRange` 列表（2588，元素格式 `[(lat,long), userCount, distance]`，2588 注释）；`totalGTs`/`totalLocations`/`totalAvgFlow`/`totalX`/`totalY`（2589–2593）；由极角换算的地心笛卡尔坐标 `polar_angle`/`x`/`y`/`z`（2596–2599，使用全局 `Re`）。
  - 卫星链路：`satsOrdered`/`satIndex`/`linkedSat = (None, None)`（2602–2604）；`graph = nx.Graph()`（2605）。
  - simpy 结构：`env`（2608）；`datBlocks`（2609）；`fillBlocks` 进程列表（2610）；`sendBlocks = env.process(self.sendBlock())`——构造时即启动发送进程（2611）；`sendBuffer = ([env.event()], [])`——(事件列表, 块列表) 二元队列（2612）；`paths` 字典（目的名→路径，2613）。
  - 通信属性：`dataRate = None`（2616）；`gs2ngeo = RFlink(...)`——30 GHz、500 MHz 带宽、maxPtx 20、收发口径 0.33/0.26 m、指向损耗 0.3、噪声系数 2、噪声温度 290 K、min_rate 10e3（2617–2627；`RFlink` 定义于 1798，在本片段范围外）。
  - `active_index`：不在 `__init__` 内设置，由 `Earth.__init__` 在 3497–3498 行后补（FACT）。
- 关键流程/方法（共 22 个，逐方法）：
  - `__init__`(2578)：建立上述全部状态；并立即用 `env.process` 启动 `sendBlock` 进程（2611）。
  - `makeFillBlockProcesses(self, GTs)`(2629)：对每个非自身 GT 各创建一个运行 `fillBlock(gt)` 的 simpy 进程并追加到 `fillBlocks`（2637–2640）；同时把 `totalGTs` 更新为 `len(GTs)`（2635）。
  - `_record_filled_block(self, block)`(2642)：块填满时记录 `block.timeAtFull = env.now`、追加到全局 `createdBlocks`（674 行定义）、写一条 `"CR"` 类型 replay 事件（`append_replay_event`，838 行定义；OD 对由 `_encode_od_pair` 编码，890 行定义）（2644–2655）。
  - `_enqueue_filled_block(self, block)`(2657)：从 `self.paths` 取当前路由赋给 `block.path`，路径为空则 `raise RuntimeError`（2659–2661）；当 `earth.pathParam` 为 `'Q-Learning'`/`'Deep Q-Learning'` 时构造三元 `QPath`（2662–2663）；触发/补充 sendBuffer 首事件并入队块（2665–2679）；写一条 `"JQ"` replay 事件（2669–2678）。
  - `fillBlock(self, destination)`(2681)：simpy 进程函数，无限循环——创建 `DataBlock`（2696，ID 为 `源ID_目的ID_index`）→ `timeToFullBlock` 算填充时长 → `yield env.timeout` 等待填满（2698–2700）→ `_record_filled_block` 并把 `index` 加 1（2705–2706）→ 若目的 GT 当前无 linkedSat 则进 `unavailableDestinationBuffer` 暂存，否则先排空暂存再 `_enqueue_filled_block`（2708–2713）；捕获 `simpy.Interrupt` 后打印并退出循环（2714–2716）。行为佐证：CODE/tests/test_runtime_effect_receipt.py:212–239（目的不可达时块仍按序创建并记录，ID 连续）。
  - `sendBlock(self)`(2718)：simpy 进程函数，无限循环——等待 sendBuffer 首事件（2737）；无 linkedSat 时每 0.1 s 轮询等待（2740–2741）；`timeToSend` 得传播时延（2744）、`块.size / self.dataRate` 得发送时长（2746）；写 `"SS"` replay 事件并记 `timeAtFirstTransmission`（2748–2758）；若 `earth._link_outage` 存在且发送时长 >0：发送起点即处于中断窗口则 `_outage.record_start_down_wait()`、`earth._link_outage_waits += 1`、等到窗口结束并 `continue`（2759–2770）；发送中途将遇中断则用 `env.any_of([发送完成, 失败时刻])` 竞速，失败先到时记 `record_mid_transmission_loss()`、`earth._link_outage_losses += 1`、`earth.lostBlocks += 1`、写 packet-fate 日志（status=1）、`_pc_flush_lost`、弹出该块并 `continue`（2771–2789）；正常情形 `yield env.timeout(timeToSend)`（2790–2793）；之后写 `"ST"` replay 事件（2794–2803）、`txLatency += timeToSend`（2805）；若块路径为空则打印源/目的并 `exit()`（2807–2809）；调用 `self.linkedSat[1].createReceiveBlockProcess(块, propTime)` 交给链上卫星（2811，`linkedSat[1]` 为 Satellite 实例）；最后按缓冲区长度弹出已发块并补新事件（2814–2820）。行为佐证：CODE/tests/test_runtime_effect_receipt.py:1094–1116（中断窗口内发送计入 `_link_outage_losses` 与 `lostBlocks`，出现 SS/LS 事件、无 ST 事件）。
  - `timeToSend(self, linkedSat)`(2822)：返回 `linkedSat[0] / Vc`，即距离除以光速的传播时延（2823–2825）；不含发送时延。
  - `createReceiveBlockProcess(self, block, propTime)`(2827)：用 `env.process(self.receiveBlock(block, propTime))` 启动一个接收进程（2833）。
  - `receiveBlock(self, block, propTime)`(2835)：simpy 进程函数——`yield env.timeout(propTime)` 等待传播（2848）；`block.propLatency += propTime`（2850）；向 `checkPoints` 追加当前时刻（2852）；向 `block.traversed_sats` 追加自身 `name`（2854–2857）；把块追加到全局 `receivedDataBlocks`（2859，673 行定义）；写 packet-fate 日志（status=0，2860–2863）。docstring 自述：GT 是块路径终点，不再转发，块进入完成列表供仿真结束统计 KPI（2839–2842）。
  - `cellDistance(self, cell)`(2865)：把 cell 的弧度经纬度转角度后，用 `geopy.distance.geodesic`（WGS-84 模型，2868 docstring）计算到本 GT 的距离，返回公里数（2870–2873）。
  - `distance_GSL(self, satellite)`(2875)：用双方地心笛卡尔坐标经 `math.dist` 计算 GT-卫星直线距离（2881–2885）。
  - `adjustDataRate(self)`(2887)：内置三组阈值数组（频谱效率 `speff_thresholds`、线性 `lin_thresholds`、dB `db_thresholds`，2889–2907）；按自由空间路径损耗公式算 `pathLoss`（2909）、由 `maxPtx_db + G - pathLoss - No` 算 `snr`（2910）；计算 `shannonRate = B*log2(1+snr)`（2911，该局部变量算出后未被使用，FACT）；取 `lin_thresholds <= snr` 的最大可行频谱效率，令 `self.dataRate = B * 该效率`（2913–2916）。
  - `orderSatsByDist(self, constellation)`(2918)：遍历星座所有卫星，距离 `<= sat.maxSlantRange * 10` 者收入列表（2929 行带 `#FIXME this x10 is for small constellations` 注释），按距离升序排序后存入 `satsOrdered`，元素为 `(距离, sat, [index])`（2923–2933）。
  - `addRefOnSat(self)`(2935)：贪心 GT-卫星分配用（docstring 自述服务于 `Earth.linkSats2GTs` 的 Greedy 版，2938）：按本地 `satIndex` 指向的有序卫星尝试挂上引用——卫星无引用则直接挂上（2949–2952）；已有引用且本 GT 更近，则让原引用 GT 的 `satIndex` 加一并递归重挂，再把自己挂上（2955–2962）；否则自身 `satIndex` 加一并递归（2963–2970）；列表耗尽时置 `linkedSat = (None, None)` 并打印（2943–2946、2965–2968）。
  - `link2Sat(self, dist, sat)`(2972)：置 `self.linkedSat = (dist, sat)`、回写 `sat.linkedGT`/`sat.GTDist`，并调用 `adjustDataRate()` 更新链路速率（2977–2980）。
  - `addCell(self, cellInfo)`(2982)：把 cell 信息追加到 `cellsInRange`（2986）。
  - `removeCell(self, cell)`(2988)：docstring 自述「Unused function」（2990）；按经纬度在 `cellsInRange` 中查找并尝试 `cellInfo.pop(i)`（2992–2996；注意 `pop` 作用在查到的元素 `cellInfo` 上而非列表自身，FACT）。调用方未确认（全 CODE/ Grep 无调用点）。
  - `findCellsWithinRange(self, earth, maxDistance)`(2998)：从 GT 网格位置向右上、右下、左上、左下四个方向逐列扫描 cell 网格（3018–3128），越界时按环形「roll over」（3024–3025 等）；对每个距离 `<= maxDistance` 的 cell，若尚无 GT 引用或本 GT 更近，则把 `cell.gateway` 置为 `(self, distance)`（3040–3042 等）；docstring 自述只做引用不做链接，链接由 `Earth.linkCells2GTs` 完成（3009–3013）。FACT：左下方向分支的越界回绕写成 `x = earth`（3109），即把 Earth 实例赋给 x，与左上分支的 `x = earth.total_x - 1`（3081）不一致。
  - `timeToFullBlock(self, block)`(3130)：计算填满一块所需时间——若 `earth.od_weight_matrices_hourly` 存在，按 `int(now / sim_duration_s * 24) % 24` 取当小时矩阵（3141–3145），否则取 `earth.od_weight_matrix`（3147）；源/目的都有 `active_index` 时取矩阵权重 `w`（3148–3151），再依次乘上 burst 乘子（`earth.burst_schedule.multiplier(now, s, d)`，并累加 `_burst_multiplier_calls`/`_burst_effect_calls`/`_burst_multiplier_failures` 计数；fail-closed 且配置了 `SIM_TRAFFIC_BURSTS` 时异常上抛，3154–3165）与 diurnal 乘子（`earth.diurnal_schedule.multiplier(now, s)`，同样三组计数与 fail-closed 逻辑，3169–3180），`flow = totalAvgFlow * w`（3181）；无矩阵时退回「均分到 `len(totalLocations)-1` 个目的」（3183）；`flow <= 0` 返回 `inf`（3185–3186）；`avgTime = block.size / flow`，返回 `np.random.exponential(scale=avgTime)`（3187–3191）。docstring 自述按指数分布随机化（3132–3133）。行为佐证：CODE/tests/test_runtime_effect_receipt.py:190–210（burst×diurnal 乘子各计一次调用与一次生效）；CODE/tests/validate_burst_rates.py:62 注释自述镜像本方法。
  - `getTotalFlow(self, avgFlowPerUser, distanceFunc, maxDistance, capacity=None, fraction=1.0)`(3193)：若全局 `balancedFlow`（313）为真则 `totalAvgFlow = totalFlow`（314）（3208–3209）；否则把入参 `avgFlowPerUser` 覆盖为全局 `avUserLoad`（315）（3212，FACT），按 `distanceFunc == "Step"` 直接累加 `cell[1] * avgFlowPerUser`（3214–3216），或 `"Slope"` 按线性坡度随距离衰减累加（3218–3221）；其他取值打印错误并 `exit()`（3223–3228）；无 linkedSat 时把 `dataRate` 置为 `gs2ngeo.min_rate`（3230–3231）；未给 `capacity` 时用 `self.dataRate`（3233–3234）；最终 `totalAvgFlow` 取计算值与 `capacity * fraction` 的较小者（3236–3239）；打印换算成 Gbps 的数值（3241）。
  - `__eq__(self, other)`(3243)：经纬度均相等则相等（3244–3247）。被本文件 `!=` 运算隐式使用：`makeFillBlockProcesses` 的 `if gt != self`（2638）与 `updateGTPaths` 的 `if GT != destination`（5020）（FACT）。
  - `__repr__`(3249)：返回含 name/经纬度/xyz 坐标的字符串（3249–3256）。
- 输入/输出：构造输入 = `(name, ID, latitude, longitude, totalX, totalY, totalGTs, env, totalLocations, earth)`；核心产出 = 填入 sendBuffer 并发送的 DataBlock（经 `receivedDataBlocks` 全局列表成为 KPI 输入）、`totalAvgFlow`、`dataRate`、`linkedSat`。
- 依赖关系：实例化于 `Earth.__init__`（3486、3494 行）；测试中经 `sim.Gateway.__new__(sim.Gateway)` 裸构造（CODE/tests/test_runtime_effect_receipt.py:195、221、1096）。`makeFillBlockProcesses` 被 `Earth.__init__`（3661）与 `initialize`（7987）调用；`getTotalFlow` 被 `initialize`（8051、8053）调用；`findCellsWithinRange`/`addCell` 被 `Earth.linkCells2GTs`（3773、3783）调用；`addCell` 亦被 `Cell.setGT`（3314）调用；`orderSatsByDist`/`addRefOnSat`/`link2Sat` 被 `Earth.linkSats2GTs`（3809、3810、3815、3820、3862）调用；`distance_GSL` 被 `Earth._gsl_in_range`（5074）、`Earth._retire_old_gsl_downlinks`（5105）、`Earth._apply_mbb_gsl_handover`（5153）调用；`adjustDataRate` 被 `link2Sat`（2980）与 `Earth._apply_mbb_gsl_handover`（5157）调用；`cellDistance` 被 `findCellsWithinRange`（3027 等 8 处）与 `Cell.setGT`（3306、3308）调用；`_record_filled_block`/`_enqueue_filled_block` 被 `fillBlock`（2705、2712–2713）与 `Earth._dispatchTraceRows`（3735、3747）调用；`createReceiveBlockProcess` 的同文件调用点为 2342 行（`Satellite.sendBlock` 内，`receiver.createReceiveBlockProcess(...)`，Satellite 类在 1891–2471 行、属另一片段）与 2811 行（本类 `sendBlock` 内，调用对象是卫星实例）（FACT）。`removeCell` 调用方未确认。

---

#### `class Cell` — CODE/SimulationRL.py:3260

- 定位：CODE/SimulationRL.py:3260（类体 3260–3317；类上方 3259 行有注释 `# A single cell on earth`）
- 职责：地球表面网格化后的单个小区，承载人口数与地理位置（FACT——依据 3259 行注释与属性）。
- 关键状态/结构（全部在 `__init__` 中初始化，3261–3285）：`map_x`/`map_y`（在人口数据图上的像素坐标，3263–3264）；`latitude`/`longitude`（由像素坐标换算的弧度经纬度，3266–3267）；`area`（按球面面积公式 `4πRe²·cos(lat)/(total_x·total_y)` 折算的本格面积，3274）；`x`/`y`/`z`（格中心地心笛卡尔坐标，3276–3278）；`users`（人口数，3280）；`f`/`bw`/`noise_power`（频率、带宽、噪声功率，3281–3283）；`rejected = True`（3284，注释自述供 applications 流程标记接受/拒绝）；`gateway = None`（3285，注释注明格式为 `(groundstation, distance)`）。
- 关键流程/方法：
  - `__init__`(3261)：完成上述换算与赋值；当 `latitude < -5 or longitude < -5` 时打印调试信息（3268–3271），其中 `exit()` 已被注释掉（3272，FACT）。
  - `__repr__`(3287)：返回含 users、面积（km²）、经纬度（度）、xyz、图内像素坐标的字符串（3287–3298）。
  - `setGT(self, gateways, maxDistance=60)`(3300)：在入参 gateways 中找出 `cellDistance` 最近的 GT 并写入 `self.gateway`（3306–3311）；若最近距离 `<= maxDistance`（默认 60 km），调用该 GT 的 `addCell` 把 `[(纬度°, 经度°), users, 距离]` 加进其 `cellsInRange`（3313–3314），否则把 `self.users` 置 0（3316）；返回最近 GT 元组（3317）。
- 输入/输出：构造输入 = `(total_x, total_y, cell_x, cell_y, users, Re=6378e3, f=20e9, bw=200e6, noise_power=1/(1e11))`；产出 = 带人口与坐标属性的网格对象，供 Gateway 覆盖扫描与流量统计读取。
- 依赖关系：实例化于 `Earth.__init__`（3449 行，每个像素格一个）。`setGT` 的调用方未确认（全 CODE/ Grep 无调用点）。`gateway` 属性被 `Gateway.findCellsWithinRange` 写入（3042 等 4 处）、被 `Earth.linkCells2GTs` 读取（3782–3786）（FACT）。`cellDistance` 依赖 `Gateway.cellDistance`（3306、3308）。

---

#### `class Earth` — CODE/SimulationRL.py:3322

- 定位：CODE/SimulationRL.py:3322（类体 3322–5635；类上方 3320 行有注释 `# Earth consisting of cells`）
- 职责：仿真世界的聚合根：持有 cell 网格、网关列表、星座、拓扑图、流量配置与事件调度状态，并驱动星座按步长移动与重链（FACT——依据 3320 行注释与 `__init__` 实际建立的属性）。
- 关键状态/结构（`__init__` 内建立，3323–3674）：
  - 基础：`env`、`outputPath`、`plotPaths`（取全局 `plotPath`，557 行定义）、`lostBlocks = 0`、`queues`、`replay_events`（3326–3331）。
  - 诊断日志列表（3332–3342，注释自述由 Hooks 1–7 填充、受 `SIM_LOG_LEVEL` 门控）：`decision_log`、`reward_log`、`train_log`、`link_snap_log`、`packet_fate_log`、`eval_curve`、`state_log`、`graph_state_log`、`encoder_log`；另有 `loss`/`lossAv`/`DDQNA = None`/`step`/`nMovs`/`epsilon`/`rewards`/`trains`/`graph = None`/`CKA`（3343–3352）。
  - 运行时效果计数器（3353–3396，注释自述汇入最终 effective receipt）：`_critic_train_successes`/`_critic_train_failures`/`_pc_train_successes`/`_pc_train_failures`/`_fast_train_steps`/`_eager_train_steps`/`_infer_backends_effective`/`_infer_backend_fallbacks`/`_temporal_checkpoint_load`（`new_checkpoint_receipt()`）/`_pc_checkpoint_loads`（mixer、replay 两个 receipt）/`_burst_multiplier_calls`/`_burst_effect_calls`/`_burst_multiplier_failures`/`_diurnal_multiplier_calls`/`_diurnal_effect_calls`/`_diurnal_multiplier_failures`/`_temporal_apply_successes`/`_temporal_apply_failures`/`_stale_neighbor_reads`/`_stale_neighbor_history_hits`/`_timed_state_reads`/`_timed_state_hits`/`_timed_state_misses`/`_timed_state_age_sum_s`/`_timed_state_age_max_s`/`_timed_queue_history`/`_global_state_observations`/`_global_state_failures`。
  - GSL 切换与链路中断：`_gsl_handover_mode`（取全局 `_SIM_GSL_HANDOVER_MODE`，744 行定义）、`_gsl_handover_events`/`_gsl_handover_count`/`_gsl_handover_stable_links`/`_gsl_handover_retiring_links`/`_gsl_handover_failures`/`_gsl_handover_losses`（3386–3392）；`_link_outage` 经 `link_outage.load_link_outage_schedule_from_env(run_seed=_SEED, fail_closed=_SIM_FAIL_CLOSED)` 初始化，异常时 fail-closed 且配置了 `SIM_LINK_INTERRUPTION_CONFIG` 则抛 `RuntimeError`，否则打印并禁用（3397–3409）。
  - path-credit：`_SIM_PATH_CREDIT`（753 行定义）为真时创建 `routing_path_credit.PathTrajectoryReplay`（gamma 读 `SIM_GAMMA` env，默认 0.99），异常时 fail-closed 上抛、否则打印并置 None（3411–3432）。
  - 人口网格：`Image.open(img_path)` 读人口 tif，负值置 0（3434–3437）；`total_x`/`total_y`/`total_cells`（3440–3442）；按像素逐格创建 `Cell` 组成二维列表 `cells`（3445–3449）。
  - 窗口：`window` 形参给定 `[西经, 东经, 南纬, 北纬]` 时换算出 `lati`/`longi`/`windowx`/`windowy`，否则取全球（3451–3466）。
  - 网关：`pd.read_csv(gt_path)` 读 CSV，按 `inputParams['Locations']` 过滤（`'All'` 时全收），逐个实例化 `Gateway`（3469–3495）；随后给每个 GT 赋 `active_index`（3497–3498）。
  - 路由与流量配置：`pathParam = pathing`（3500，全局 `pathing` 定义于 226）；trace 流量开关读 `SIM_TRAFFIC_TRACE_PATH`（3501–3503）；`sim_duration_s` 读 `SIM_TIME_LIMIT` env 或 `inputParams['Test length'][0]`，异常时取 5.0（3517–3522）；OD 配置：trace 模式要求 `SIM_EXPECTED_TRAFFIC_TRACE_SHA256` 为 64 位十六进制否则抛 `RuntimeError`，并另建 uniform 矩阵供构图（3527–3558）；`traffic_mode_needs_gateway_physical` 为真的模式（如 gravity 系）把 OD 构建推迟到 `linkCells2GTs` 之后（`_od_deferred`/`_pending_traffic_cfg`/`_needs_gt_fill_startup`，3559–3574，落地于 `initialize` 的 7919–7988 行）；其余模式立即 `build_od_matrix_for_gateways`（3575–3584）；任何异常在 fail-closed 下上抛、否则回退 uniform（3585–3601）。
  - burst/diurnal 调度：`load_burst_schedule_from_env`（3608）与 `load_diurnal_schedule_from_env`（3638，diurnal 使用 `SIM_TIME_LIMIT` 或 Test length 折算仿真时长，3633–3637）；均为 fail-closed 下「配置了却初始化失败」即抛错，否则打印并置 None（3606–3656）。
  - 进程启动：非 getRates、非推迟、非 trace 时为每个 GT 调 `makeFillBlockProcesses`（3658–3661）；`create_Constellation(constellation, env, self)` 建星座存入 `self.LEO`（3664，函数定义于 8135）；`_SIM_LOG_LEVEL >= 1` 时启动 `diagnostic_link_snapshot_process`（3665–3666，函数定义于 1175）；全局 `rotateFirst`（329）为真时各轨道面先转 `ndeltas*deltaT`（3668–3671）；最后 `self.moveConstellation = env.process(self.moveConstellation(env, deltaT, getRates))`（3674）——实例属性与方法同名，赋值后该实例上的方法名被 process 对象遮蔽（FACT）。
- 关键流程/方法（共 24 个，逐方法）：
  - `__init__`(3323)：建立上述全部状态并启动移动进程（3323–3674，见上）。
  - `startTraceTraffic(self)`(3676)：trace 模式入口——未启用直接返回（3678–3679）；重复启动抛 `RuntimeError`（3680–3681）；读 `SIM_TRAFFIC_TRACE_PATH`/`SIM_EXPECTED_TRAFFIC_TRACE_SHA256`/`SIM_TRAFFIC_TRACE_MAX_PACKETS`（默认 1000000）（3684–3688）；调 `legacy_trace_runtime.load_and_project_trace` 得到行与 manifest（3689–3696）；按源 GT 的 `active_index` 分组（3697–3700）；每个源 GT 启动一个 `_dispatchTraceRows` 进程（3701–3704）；打印包数/比特数摘要（3705–3708）。调用方：`initialize`（7991 行）。
  - `_dispatchTraceRows(self, source, rows)`(3710)：每个源一个的有序派发进程——按 `emit_time_s` 逐行创建 `DataBlock`（ID 形如 `TRACE:<packet_id>`），覆写 `block.size` 并附加 `trace_packet_id`/`trace_src_grid_id`/`trace_dst_grid_id`/`deadline_at_s`（3722–3734）；`_record_filled_block` 后进入 `waiting` 列表（3735–3737）；每轮（至多每 0.05 s 轮询一次，3717）把「目的 GT 已有 linkedSat 且 `source.paths` 存在非空路径」的块 `_enqueue_filled_block`，其余继续等待（3739–3750）；到达 `sim_duration_s` 视界后返回（3751–3752）。
  - `set_window(self, window)`(3754)：docstring 自述「Unused function」（3756）；按给定窗口重设 `lati`/`longi`/`windowx`/`windowy`（3758–3761）。调用方未确认（全 CODE/ Grep 无调用点）。
  - `linkCells2GTs(self, distance)`(3763)：先让每个 GT 跑 `findCellsWithinRange`（3771–3773），再遍历全部 cell、把已标记 `gateway` 的 cell 信息经 `addCell` 并入对应 GT（3780–3786）；两段各打印耗时（3775、3788）。docstring 自述保证一个 cell 只链接一个 GT（3765–3766）。调用方：`initialize`（7917 行）。
  - `linkSats2GTs(self, method, keep_stable=False)`(3791)：GT-卫星配对。`method == "Greedy"`：清空所有卫星的 `linkedGT`/`GTDist`，各 GT 依次 `orderSatsByDist` + `addRefOnSat`，再让挂有 GT 的卫星回调 `linkedGT.link2Sat`（3804–3815）。`method == "Optimize"`：用各 GT 有序卫星列表的名次构造代价矩阵 `SxGT`（初值 99999，3818–3822），`scipy.optimize.linear_sum_assignment` 求最小代价分配（3825），把行/列下标映射回 `(名次, 卫星)`（3826–3840）；`keep_stable` 为真时，新旧分配一致且卫星仍挂着本 GT 的配对加入 `stable_ids`、跳过重置（3842–3857，docstring 自述避免把每次星座更新当作全量 GSL 重连，3795–3797）；其余卫星清空引用后按分配执行 `link2Sat`，无卫星可分则置 `(None, None)` 并打印（3859–3865）。docstring 另注明一颗卫星只允许链接一个 GT（3793）。调用方：`moveConstellation`（5240 行）、`initialize`（7966 行）；行为佐证：CODE/tests/test_runtime_effect_receipt.py:664–686（keep_stable 下旧配对不被拆除，`link_calls` 各为 1 次）。
  - `getCellUsers(self)`(3867)：返回与 `cells` 同形的二维用户数列表，供绘制人口图（3868 docstring、3871–3876）。调用方：本类 `plotMap`（5558 行）。
  - `updateSatelliteProcessesSimpler(self, graph)`(3878)：星座移动后重建各卫星进程与缓冲的「简单版」——对每颗卫星：把 `sendBufferSatsIntra`/`sendBufferSatsInter`/`sendBufferGT`/`tempBlocks` 中每个块的 `path` 用 `getShortestPath` 重算并与旧路径在当前卫星处拼接，拼不出（当前卫星不在旧路径）则打印并 `exit()`（3906–3964）；按新图找邻居并区分 intra/inter（3966–3987）；中断并清空全部发送进程（3989–3998）；把各缓冲的块按「到达本星时刻」汇总排序（4000–4012、4034–4035）；按新链路重建 GSL/ISL 发送缓冲与进程（4014–4032）；再按块路径的下一跳把块分发回对应缓冲（4036–4090）。docstring 自述：来自非强化实现，会因停进程丢失在传块的传输进度（3884–3887），并自述「this version does work with Q-Learning and Deep-Learning」（3881–3883，原文如此，FACT 照录）。调用方未确认（全 CODE/ Grep 无调用点）。
  - `updateSatelliteProcessesCorrect(self, graph)`(4092)：「正确版」——与简单版同首段 docstring（4095–4097 同样含「does work with Q-Learning and Deep-Learning」字样，原文如此，FACT 照录），差异在 docstring 自述「链路未断的发送进程在星座移动后继续运行」（4112–4113）。实现上：重算各缓冲块路径时若 `getShortestPath` 返回 -1 则直接从缓冲弹出该块（4129–4137、4160–4168、4190–4198、4222–4231；弹出时不增加 `lostBlocks` 计数，FACT），成功则置 `isNewPath` 并记录 `oldPath`/`newPath`（4148–4151 等）；只重建 inter-plane 邻居列表（4250–4264，注释自述假设 intra-plane ISL 不变，4255–4256）；inter 缓冲逐一对照新旧邻居——仍在且首块下一跳不变则保留首块与进程、其余块进再分配列表，下一跳变了则全部再分配并重建进程，邻居消失则清块停进程（4282–4333）；为新邻居补建缓冲与进程（4340–4343）后整体覆写（4346–4347）；intra 缓冲只检查块的去向、必要时重置（4351–4383）；GSL 按「有无 linkedGT × 有无旧进程 × 首块目的地是否仍是 linkedGT」分情形保留/重建发送进程与缓冲（4386–4444）；最后按到达时刻排序、按路径下一跳再分配（4446–4502）。调用方：`moveConstellation`（5281 行，pathParam 非 RL 时）。
  - `updateSatelliteProcessesRL(self, graph)`(4504)：RL 版。docstring 内同时存在「Update: This function works now」与「This function does not work correctly!」两句（4506–4509，原文如此，FACT 照录）。流程：先按 pathParam 更新各星 RL 邻居结构——`'Q-Learning'` 时 `getLinkedSats` 后写入 `sat.QLearning.linkedSats` 的 U/D/R/L（4534–4540），`'Deep Q-Learning'` 时 `sat.findIntraNeighbours`/`sat.findInterNeighbours`（4541–4544）；然后对 intra/inter/GSL 三类缓冲逐块用学习体重新决策下一跳（`QLearning.makeAction` 或 `DDQNA.makeDeepAction`，在线/离线按 `sat.DDQNA`、`self.DDQNA` 是否存在分派；QPath 长度 >3 时传 `prevSat`），决策结果非 0 时覆写 `block.QPath[-2]`（4554–4746；nextHop 为 None 时打印告警，4599–4600）；全局 `plotPaths` 为真且块 ID 末位为 '0' 时调 `plotShortestPath` 出图（4611–4618、4674–4681、4735–4742，三处 ANCHOR 注释）；随后的 inter/intra/GSL 缓冲与进程重建逻辑与 Correct 版同构，但路径一律改用 `QPath`（4748–4943）；再分配按 QPath 找下一跳，若当前卫星不在 QPath 中则打印带 FIXME 的调试说明、`self.lostBlocks += 1`、写 packet-fate 日志（status=1）并 `_pc_flush_lost`（4961–4965）。调用方：`moveConstellation`（5279 行，pathParam 为 `'Q-Learning'`/`'Deep Q-Learning'` 时）；CODE/tests/test_runtime_effect_receipt.py:717、775、855 在测试中将其替换为 lambda 以隔离移动流程。
  - `updateGTPaths(self)`(5012)：对每个有序 GT 对，双方都有 linkedSat 时 `getShortestPath(GT.name, destination.name, self.pathParam, GT.graph)` 写入 `GT.paths`，否则写空路径并打印（5018–5028）；随后把各 GT sendBuffer 中块的 `path` 同步为新路径、置 `isNewPath` 并按首/次/末跳重建三元 `QPath`（5030–5036，注释自述 QPath 之后逐跳插在倒数第二位，5035–5036）。调用方：`moveConstellation`（5283 行）。
  - `getGSLDataRates(self)`(5038)：收集有 linkedSat 的 GT 的上行 `dataRate` 与有 linkedGT 的卫星的下行 `downRate`，返回 `(upDataRates, downDataRates)`（5039–5050）。调用方：`moveConstellation`（5204 行，仅 getRates 为真时）。
  - `getISLDataRates(self)`(5052)：收集所有卫星 `interSats` 条目的速率（`satData[2]`）返回列表（5053–5061）；局部变量 `highRates` 统计 >3e9 的条数但计算后未返回、未使用（5054、5058–5059，FACT）。调用方：`moveConstellation`（5205 行）。
  - `_drop_handover_blocks(self, blocks, death_time)`(5063)：对列表中每个块：`lostBlocks += 1`、`_gsl_handover_losses += 1`、写 packet-fate 日志（status=1）、`_pc_flush_lost`（5065–5069）；docstring 自述用于「无 retiring 链路可排空时的显式切换失败结局」（5064）。调用方：`_retire_old_gsl_downlinks`（5097、5101 行）。
  - `_gsl_in_range(self, gt, sat)`(5071)：返回 `gt.distance_GSL(sat) <= sat.maxSlantRange * 10`（5074），与 `Gateway.orderSatsByDist` 的覆盖判定（2929 行）同式，docstring 亦自述此对齐（5072）；属性/类型/值异常时返回 False（5075–5076）。调用方：`_retire_old_gsl_downlinks`（5096）、`_apply_mbb_gsl_handover`（5151）。
  - `_retire_old_gsl_downlinks(self, old_links)`(5078)：MBB 切换后让旧卫星的下行缓冲继续排空——旧卫星仍挂着该 GT 则跳过（5083–5084）；先中断旧 `sendBlocksGT` 进程（5085–5091）；缓冲为空则重置跳过（5092–5095）；旧星已出覆盖范围则 `_drop_handover_blocks` 弃块（5096–5099）；`retiring_gt_links` 已达 `_SIM_GSL_HANDOVER_MAX_RETIRING_LINKS`（745 行定义，默认 4）同样弃块（5100–5103）；否则以旧速率（<=0 时取 1.0，5106–5108）为旧星创建一个带 `link_context={"rid": ..., "drain_once": True}` 的 `sendBlock` 退休进程（5104–5117），注册回调在进程结束时从 `retiring_gt_links` 移除该条目（5127–5134），入列、计数 `_gsl_handover_retiring_links += 1`、写 `"HB"` replay 事件，并把旧星 `sendBufferGT` 重置为空（5135–5140）。调用方：`_apply_mbb_gsl_handover`（5181 行）；行为佐证：CODE/tests/test_runtime_effect_receipt.py:883–911（退休进程的 rid、`drain_once`、HB 事件均被断言）。
  - `_apply_mbb_gsl_handover(self, old_links)`(5142)：make-before-break 切换——对每条旧链路读取 GT 现行 `linkedSat`：无新星且旧星仍可挂（无引用或仍属本 GT）且在覆盖内，则把 GT 重新指回旧星并双方刷新速率，记 `keep_old_fallback` 事件（5148–5164）；不可回退则 `_gsl_handover_failures += 1` 并记 `failure` 事件（5165–5171）；新星与旧星不同则 `_gsl_handover_count += 1` 并记 `switch` 事件（5172–5180）；最后调 `_retire_old_gsl_downlinks`（5181）。调用方：`moveConstellation`（5254 行，`_SIM_GSL_HANDOVER_MODE == "mbb"` 时）；行为佐证：CODE/tests/test_runtime_effect_receipt.py:913–943（出覆盖弃块计 failure/losses；在覆盖内回退记 keep_old_fallback）。
  - `moveConstellation(self, env, deltaT=3600, getRates=False)`(5183)：simpy 进程函数，无限循环（5200）——每轮先打印，getRates 为真时经 `getGSLDataRates`/`getISLDataRates` 采样进全局 `upGSLRates`/`downGSLRates`/`interRates`（688–690 行定义），首轮前还对 `intraRate`（691 行定义）采样一次（5197–5214）；`yield env.timeout(deltaT)`（5216）；随后快照当前 GSL 配对（5221–5229），清空各 GT 的 `satsOrdered`、且 `_SIM_GSL_KEEP_STABLE`（746 行定义）为假时把 `linkedSat` 置 `(None, None)`（5230–5233）；各轨道面 `rotate(ndeltas*deltaT)`（5236–5237，`ndeltas` 定义于 241）；`linkSats2GTs("Optimize", keep_stable=_SIM_GSL_KEEP_STABLE)` 重配（5240）；keep-stable 下对未换星的旧配对计数 `_gsl_handover_stable_links` 并记 `keep_stable` 事件（5241–5252）；`_SIM_GSL_HANDOVER_MODE == "mbb"` 时调 `_apply_mbb_gsl_handover`（5253–5254）；`temporal_encoder.temporal_enabled()` 为真时对每颗卫星 `reset_satellite`（5262–5269，注释说明因邻居集已变、GRU 隐状态作废；该段包了 ImportError 静默）；`createGraph(self, matching=matching)` 重建拓扑并写入 `self.graph` 与各 GT 的 `graph`（5273–5276，`matching` 全局定义于 326）；按 pathParam 分派 `updateSatelliteProcessesRL` 或 `updateSatelliteProcessesCorrect`（5278–5281）；`updateGTPaths()`（5283）；`nMovs += 1`（5284）；全局 `saveISLs`（324 行定义）为真时用 `plotMap(edges=True)` 存 ISL 图（5285–5290，其中 5287 行以裸名引用模块级 `outputPath`，该名仅在 `if __name__ == '__main__':` 块 653 行赋值，FACT）；全局 `FL_Test`（234 行定义）为真时置全局 `const_moved`（325 行定义）为 True、调 `perform_FL(self)`（1585 行定义）并把前后 CKA 追加到 `self.CKA`（5292–5297）。启动方：`__init__`（3674 行，实例属性遮蔽同名方法）；行为佐证：CODE/tests/test_runtime_effect_receipt.py:688–744（keep-stable 下移动后 `_gsl_handover_stable_links == 2` 且事件序列匹配）、746 行起（keep_stable 关闭时退回旧重链行为）。
  - `testFlowConstraint1(self, graph)`(5299)：找出 `linkedSat` 距离最大的 GT（用 `1/距离` 取最大，5301–5305），统计图中 `slant_range` 大于该距离的边数并打印（5307–5313）。调用方未确认（全 CODE/ Grep 无调用点）。
  - `testFlowConstraint2(self, graph)`(5315)：对每个 GT（跳过 `gateways[0]`），求它到 `gateways[0]` 的最短路，检查中间各跳边权是否超过首跳距离，超出则计为失败并打印总数（5316–5341）；查表遇 KeyError 时尝试反向边并打印（5322–5336）。调用方未确认（全 CODE/ Grep 无调用点）。
  - `plotMap(self, plotGT=True, plotSat=True, path=None, bottleneck=None, save=False, ID=None, time=None, edges=False, arrow_gap=0.008, outputPath='', paths=None, fileName="map.png", n=None)`(5343)：matplotlib 绘图函数——内含两个嵌套函数：`calculate_link_usage(paths)`（5354，统计每条链路被多少块经过并记录坐标）与 `adjust_arrow_points(start, end, gap_value)`（5371，按比例把箭头两端内缩）；`edges=True` 时为每颗卫星的 intra/inter 链路和每个 GT 的 linkedSat 画箭头（5383–5415）；`plotSat` 按轨道面上色画散点并受全局 `plotSatID`（235 行定义）控制标注卫星 ID（5417–5426）；`plotGT` 画红色 x 标（5428–5430）；给定 `path` 时画路径折线，`bottleneck` 存在时把最小速率段前后分成蓝/红/蓝三段（5433–5466）；`paths` 非空时画拥塞图——按全局 `pathing`（226 行定义）选 `QPath` 或 `path` 统计链路用量（5470），归一化后用 `cool` 色图与 `FancyArrowPatch` 画贝塞尔曲线箭头并加 colorbar（5472–5545），无数据时打印并返回 -1（5476–5480）；按入参组合加图例（5547–5552）；`paths is None` 时用 `getCellUsers()` 以 LogNorm 显示人口热力图，否则翻转 y 轴（5557–5561）；给了 `time` 与 `ID` 时加标题（5567–5568）；`save` 时存图（5570–5572）。调用方：`moveConstellation`（5289）、`initialize`（8126）、`plotShortestPath`（8969，函数定义于 8968）、`plotCongestionMap`（11997、12011，函数定义于 11968）、`RunSimulation`（12171，函数定义于 12019）（FACT）。
  - `initializeQTables(self, NGT, hyperparams, g)`(5574)：遍历星座每颗卫星——全局 `importQVals`（262 行定义）为真时从全局 `tablesPath`（631 行定义）读 `<sat.ID>.npy` 并带表构造 `QLearning`（5592–5595），否则不带表构造（5596–5597）；打印导入/创建数量（5599–5603）。`QLearning` 类定义于 5682（本片段范围外）。调用方：`initialize`（8081 行）。
  - `plot3D(self)`(5605)：把全部卫星与 GT 的 xyz 坐标画成 3D 散点（卫星圆点、GT 三角）并 `plt.show()`（5606–5626）。调用方未确认（全 CODE/ Grep 无调用点）。
  - `__repr__`(5628)：返回含 x/y 网格总数、总格数与窗口范围的字符串（5628–5635）。
- 输入/输出：构造输入 = `(env, img_path, gt_path, constellation, inputParams, deltaT, totalLocations, getRates=False, window=None, outputPath='/')`；其中 `img_path` 为人口 tif、`gt_path` 为网关 CSV、`constellation` 传给 `create_Constellation`、`inputParams` 需含 `'Locations'` 与 `'Test length'` 键（3475、3520）。产出 = 随仿真推进填充的各类日志/计数器、`gateways`/`cells`/`LEO`/`graph` 状态，以及经 `plotMap`/`plot3D` 的图文件或屏幕输出。
- 依赖关系：实例化于 `initialize`（7912 行，函数定义于 7885）；`initialize` 还依次调用 `linkCells2GTs`（7917）、`linkSats2GTs`（7966）、`startTraceTraffic`（7991）、`initializeQTables`（8081）、`plotMap`（8126）（FACT）。跨文件引用：`CODE/traffic_mlab.py:144` 注释提到「SimulationRL.Earth」（向后兼容说明）；`CODE/tools/benchmark_graph_execution.py:33` 从本模块 import `GraphMessagePassingReadout`（非本片段符号）；`CODE/tests/test_runtime_effect_receipt.py:55`、`CODE/tests/test_raac_tensorflow_contract.py:34`、`CODE/tests/test_raac_aoi_gate.py:49` 以 `import SimulationRL as sim` 整体引用。`od_weight_matrices_hourly` 在本类只读不写（3141 读、3513 置 None），实际赋值在 `initialize` 的 7951 行（FACT）。
# 片段 s3：`CODE/SimulationRL.py` 第 5638–7884 行

### 文件 `CODE/SimulationRL.py`（实测 12556 行）

本片段覆盖第 5638–7884 行。实测全文件 12556 行（`wc -l`）。本范围符号核对清单（`grep -nE '^(class |def )'` 过滤 5638–7884）：5 个顶层 class（`hyperparam` 5638、`QLearning` 5682、`GraphMessagePassingReadout` 5924、`DDQNAgent` 6190、`ExperienceReplay` 7770），6 个顶层 def（`_np_mlp_forward` 5833、`_shadow_record` 5849、`_shadow_dump` 5876、`graphStateDim` 5901、`raacGraphStateDim` 5913、`_graph_custom_objects` 6186）。

模块级说明（本范围内的模块级语句与常量，带行号）：

- 5822–5832 行：注释块，说明决策时推理后端开关 `SIM_INFER_BACKEND` 的三个取值 `keras`（默认，eager `__call__`）、`tffunc`（`tf.function` 包装活模型）、`numpy`（手写 MLP 前向，注释标注 EVAL-ONLY 但 6775 行实现处注释称已支持 train+eval——两处注释口径不一致，FACT）；并注释说明该加速门控只对标准 3-Dense Sequential MLP 生效，csr/cvar 模型回退 keras。
- 5841–5844 行：注释块，说明 `SIM_SHADOW_INFER` 是只测量开关：比较 numpy 决策前向与 tffunc 在相同活权重下的一致性（argmax/排序翻转率、最小 Q 间隔）。
- 5845–5847 行：模块级全局字典 `_SHADOW`，字段 `n / argmax_flip / order_flip / max_abs / gap_lt_1e-7 … 1e-4 / flip_gaps / skipped / seen`，累计影子对比统计（FACT）。
- 5897–5898 行：`import atexit as _atexit` 并 `_atexit.register(_shadow_dump)`，进程退出时自动转储影子统计（FACT）。
- `_SIM_SHADOW_INFER` 定义在本范围外（`CODE/SimulationRL.py:803`，env `SIM_SHADOW_INFER`，默认 0=关）；本范围内只引用。
- 7879–7881 行：分节注释横幅 `### Functions ###`，7884 行 `# @profile`，其后 7885 行起为顶层函数区（下一个片段范围）。

---

#### `class hyperparam` — CODE/SimulationRL.py:5638

- 定位：CODE/SimulationRL.py:5638
- 职责：把一组模块级全局超参数快照进一个对象，供 `QLearning` / `DDQNAgent` 构造时读取 (FACT)。
- 关键状态/结构：`__init__` 从模块全局拷贝 `alpha, gamma, epsilon, ArriveR(=ArriveReward), w1, w2, w4, again(=againPenalty), unav(=unavPenalty), tau, updateF, batchSize, bufferSize, MAX_EPSILON, MIN_EPSILON, LAMBDA, plotPath, coordGran, ddqn, latBias, lonBias, diff, explore, reducedState, online(=onlinePhase)`（5639–5670；这些全局定义于同文件 231–613 行一带，部分可被 env 覆盖，如 `SIM_W1` 270 行、`SIM_GAMMA` 274 行、`SIM_LR` 563 行）；`hardUpdate` 存为布尔 `hardUpdate==1`（5657）；`importQ` 存 `importQVals`（5658）；`pathing` 为构造入参（5652）。
- 关键流程/方法：`__init__`(5639) 做上述全局→属性的拷贝；`__repr__`(5672) 返回 alpha/gamma/epsilon/w1/w2 的格式化字符串。
- 输入/输出：入参 `pathing`（路由方式标识）；输出为属性容器对象。
- 依赖关系：被 `initialize()` 在 8058 行构造（`hyperparams = hyperparam(pathing)`）；构造出的对象传给 `QLearning.__init__`（5595/5597）与 `DDQNAgent.__init__`（8062/8070）。`__repr__` 调用方未确认。

---

#### `class QLearning` — CODE/SimulationRL.py:5682

- 定位：CODE/SimulationRL.py:5682
- 职责：基于 6 维 numpy Q 表的逐跳表格 Q-Learning 路由 agent（FACT，docstring 5684–5688：Q(s,a) 表前 5 维是环境状态、第 6 维是 4 动作）。
- 关键状态/结构：`linkedSats`（'U'/'D'/'R'/'L' → 邻接卫星或 None，5690–5695）；`actions=('U','D','R','L')`（5697）；`qTable` 形状 `(3,3,3,3,NGT,4)`，未导入时随机初始化（5703–5707）；`nStates = 3*3*3*3*NGT`（5700）；从 `hyperparams` 拷贝 `alpha/gamma/maxEps/minEps/w1/w2`（5709–5716）；`oldState/oldAction`（5718–5719）；`epsilon` 为 list（5712，原直接取 hyperparams.epsilon 的代码被注释掉，5711）。
- 关键流程/方法：
  - `__init__`(5683) 计算四方向邻接卫星（调用 `getLinkedSats`，9328）、建/导入 Q 表、拷贝超参。
  - `makeAction(block, sat, g, earth, prevSat=None)`(5721)：若当前卫星的 linkedGT 即报文目的地，则把 `ArriveReward` 写进上一跳卫星的 Q 表并按需画投递路径（5742–5749）后返回 0；否则 `getState`（9443）取 5 元组状态（5754），explore 时按 `alignEpsilon` 衰减 ε 随机选可用方向（5758–5761），否则对 `qTable[newState]` 取 argmax、不可用方向置 `-np.inf` 后重选（5765–5769）；有 `prevSat` 时按重访惩罚 `againPenalty` 或 `getDistanceReward`+`getQueueReward` 计算奖励（5777–5785），并用 `(1-α)·oldQ + α·(r+γ·maxQ(s'))` 更新**上一跳**卫星的 Q 表（5791–5794）；把 newState/动作下标写回 `block.oldState/oldAction`（5801–5802），返回 `[下一跳ID, 经度°, 纬度°]`（5774, 5806）。
  - `alignEpsilon(earth, sat)`(5808)：按 `minEps + (maxEps-minEps)·exp(-LAMBDA·step/(decayRate·CurrentGTnumber²))` 计算 ε 并追加到 `earth.epsilon`（5809–5812）。
  - `__repr__`(5814)：返回目的地数/动作空间/状态数/qTable 的格式化串。
- 输入/输出：`makeAction` 返回 `0`（已到最后一跳）或 `[ID, lon°, lat°]` 三元组；`alignEpsilon` 返回 float ε。
- 依赖关系：调用 `getLinkedSats`(9328)、`getState`(9443)、`getDistanceReward`(10296)、`getQueueReward`(10269)、`plotShortestPath`(8968)；访问 `prevSat.QLearning.qTable`（5743/5792/5794，即跨卫星互写 Q 表，FACT）。被 `Earth.initializeQTables`(5574) 在 5595/5597 行构造并挂到每颗卫星 `sat.QLearning`；`makeAction` 被 `Satellite.receiveBlock`(2017) 的 2071/2078 行与 `Earth.updateSatelliteProcessesRL`(4504) 的 4562/4582/4632/4650/4694/4712 行调用；`alignEpsilon` 仅被本类 `makeAction` 在 5758 行调用。测试佐证：未找到直接针对 `QLearning` 的测试。

---

#### `def _np_mlp_forward(s, Ws)` — CODE/SimulationRL.py:5833

纯工具函数。以 float32 numpy 复现 `Dense(relu)→Dense(relu)→Dense(linear)` 三层 MLP 前向：`x@W0+b0`、relu、`@W2+b2`、relu、`@W4+b4`（5835–5838，Ws 为 6 个权重数组的列表）(FACT)。输入状态向量 `s` 与权重列表 `Ws`，输出 Q 向量。被 `_shadow_record`(5858) 与 `DDQNAgent._build_infer_fn` 的 numpy 后端闭包 `_np_infer`(6785) 调用。

---

#### `def _shadow_record(agent, s, q_tf)` — CODE/SimulationRL.py:5849

测量辅助函数。取 `agent.qNetwork.weights` 的 numpy 副本，若非 6 个张量（非标准 3-Dense MLP）则计 `skipped` 返回（5852–5856）；否则并行算 `_np_mlp_forward` 与传入的 `q_tf`，累计样本数、max|Δ|、argmax 翻转、全序翻转、最小相邻 Q 间隔分档计数（1e-7…1e-4）到全局 `_SHADOW`（5857–5872）；任何异常吞掉并计 `skipped`（5873–5874）(FACT)。仅被 `DDQNAgent._infer` 在 `SIM_SHADOW_INFER` 采样命中时调用（6728）。

---

#### `def _shadow_dump()` — CODE/SimulationRL.py:5876

测量辅助函数。`_SIM_SHADOW_INFER` 关闭或无样本时直接返回（5878–5879）；否则打印一行汇总（采样数、argmax/order 翻转率、max|Δ|、间隔分档、翻转时间隔最大值、skipped，5881–5885），并把 `_SHADOW` 写成 JSON——路径取 env `SIM_SHADOW_OUT`，未设则为 `<outputPath>/run_trace/shadow_infer.json`（5886–5893），写文件异常静默忽略（5894–5895）(FACT)。仅由 `atexit` 注册调用（5898）。

---

#### `def graphStateDim()` — CODE/SimulationRL.py:5901

纯工具函数。返回 C4/C5 图编码器扁平状态宽度：`n*14 + n*n + 4*n + 12 + (4 if _SIM_M2_FIX else 0)`，其中 `n=_GRAPH_MAX_NODES`，14 即 `_GRAPH_NODE_FEAT_DIM`（5901–5910）(FACT)。被 `DDQNAgent.__init__`（6235）调用以定 `stateSize`；测试 `CODE/tests/test_runtime_effect_receipt.py:103-107` 断言该公式与 `raacGraphStateDim` 的维度契约。

---

#### `def raacGraphStateDim()` — CODE/SimulationRL.py:5913

纯工具函数。返回 C6/C7（reliability-aware action-centric）图状态宽度：`n*17 + n*n + 4*n + 4*9`，17=`_RAAC_NODE_FEAT_DIM`、9=`_RAAC_ACTION_FEAT_DIM`（5913–5921）(FACT)。被 `DDQNAgent.__init__`（6238）调用；测试佐证 `CODE/tests/test_runtime_effect_receipt.py:105`、`CODE/tests/test_raac_tensorflow_contract.py:74`。

---

#### `class GraphMessagePassingReadout(Layer)` — CODE/SimulationRL.py:5924

- 定位：CODE/SimulationRL.py:5924
- 职责：C4/C5（及 RAAC C6/C7）的图编码 Keras 自定义层：解析定长扁平化 k-hop 子图（节点特征 + 有向 ISL 邻接 + U/D/R/L 读出掩码 + 尾部），做边上消息传递，输出 4 方向读出嵌入加尾部 (FACT，docstring 5925–5934；mode='gat' 为 C4 多头注意力，mode='mpnn' 为 C5 非注意力均值聚合)。
- 关键状态/结构：构造参数 `mode/max_nodes/feat_dim/hidden_dim/num_layers/num_heads/tail_dim/reliability_aware/aoi_gate/action_feat_dim`（5935–5951）；`aoi_gate` 只在 `reliability_aware` 为真时生效（5950）；gat 模式要求 `hidden_dim % num_heads == 0`（5952–5953）；建有 `node_in = Dense(hidden_dim, relu)`（5954）与可选 `reliability_rate = Dense(1, softplus)`（5955–5958）。`build` 阶段按模式建权重：gat 为每层 `gat_W`(heads,h,hd)、`gat_a_src/a_dst`(heads,hd)、`gat_self_W`(h,h)、`gat_bias`(h,)（5993–6030）；mpnn 为每层 `msg_W/self_W`(h,h)、`mpnn_bias`(h,)（6031–6053）；另有 `dir_default`(4,h) 零初始化可训练向量（6054–6059）。
- 关键流程/方法：
  - `__init__`(5935) 校验 mode∈{gat,mpnn}、存超参、建输入投影层与可选 reliability 率层。
  - `get_config`(5960) 把全部构造参数并入 Keras 序列化配置。
  - `from_config(cls, config)`(5977, classmethod)：反序列化时若缺 `aoi_gate` 且 `reliability_aware` 为真，用当前运行时全局 `_RAAC_AOI_GATE` 回填该字段（5986–5989；docstring 说明用于加载 2026-07-18 前未序列化该字段的旧 RAAC H5 检查点）。
  - `build(input_shape)`(5991) 按模式创建上述全部可训练权重并调用 `super().build`。
  - `_parse(flat)`(6062)：把扁平输入切回 `node`(B,n,feat)、`adj`(B,n,n)、`readout`(B,4,n)、`tail`（6063–6070）；取节点特征第 7 维作 valid-node 掩码并用它屏蔽邻接与读出（6071–6073）；`action_feat_dim>0` 时把 tail 重形为 (B,4,action_feat_dim)（6074–6077）。
  - `_gat_layer(h, adj, node_mask, layer_idx, reliability=None)`(6079)：多头 GAT 单层——einsum 投影、src/dst 注意力打分、leaky_relu、按邻接边掩码 softmax，可选乘 reliability、再归一化，聚合消息加 self 项与 bias 后 relu 并按节点掩码清零（6080–6100）；返回 (输出, 注意力权重 alpha)。
  - `_mpnn_layer(h, adj, node_mask, layer_idx, reliability=None)`(6102)：非注意力均值聚合——消息 `h@msg_W`、（可选 reliability 加权的）邻接归一化聚合、加 self 项与 bias 后 relu 并掩码（6103–6111）；返回 (输出, 聚合消息 msg)。
  - `_reliability_weights(node, node_mask)`(6113)：RAAC AoI 门控——取节点特征第 15 维（observed）、第 16 维（age_norm，截负为 0），用前 15 维经 `reliability_rate` 得 rate 并加 `_RAAC_MIN_RELIABILITY_RATE`，算 `observed·exp(-rate·age)`；root 节点（特征第 6 维>0.5）强制 reliability=1，最后乘节点掩码（6115–6122）。
  - `_encode(flat, return_stats=False)`(6124)：`_parse`→`node_in` 投影→可选 reliability→按层数跑 gat/mpnn（6125–6137）；方向读出 = 读出掩码（可选 reliability 加权）对 h 加权平均，无方向时用 `dir_default`（6139–6146）；RAAC 模式拼 `[dir_emb, root, action_feat]`（6147–6149），非 RAAC 拼 `[dir_emb 展平, tail]`（6151）；`return_stats` 时附统计：embedding 范数均值、reliability 均值、GAT 注意力熵/最大权重/头均衡 std、MPNN 消息范数均值（6156–6176）。
  - `call(flat)`(6178) 返回 `_encode` 的编码向量（Keras 前向入口）。
  - `diagnostics(flat)`(6181) 返回 `_encode(..., return_stats=True)` 统计项的 float 字典。
- 输入/输出：输入扁平张量 (B, graphStateDim() 或 raacGraphStateDim())；`call` 输出 (B, 4·hidden_dim + tail_dim)（非 RAAC）或 (B, 4, hidden_dim+hidden_dim+action_feat_dim)（RAAC 路径，6147–6149）(FACT)。
- 依赖关系：被 `DDQNAgent._create_graph_model`(7402–7414) 以名 `graph_encoder` 实例化进 qNetwork；经 `_graph_custom_objects`（6186）注册供 `keras.models.load_model` 反序列化（6331/6587/6642）；跨文件被 `CODE/tools/benchmark_graph_execution.py:33,38` import 并实例化。测试佐证：`CODE/tests/test_raac_tensorflow_contract.py:39-71`（from_config 回填 + `_reliability_weights` 门控语义）、`:73-87`（RAAC 模型输出 4 路共享动作分）、`CODE/tests/test_runtime_effect_receipt.py:109-120`（门控公式源码契约）、`CODE/tests/test_raac_aoi_gate.py:78,91`（层实例化）。

---

#### `def _graph_custom_objects()` — CODE/SimulationRL.py:6186

纯工具函数。返回 `{"GraphMessagePassingReadout": GraphMessagePassingReadout}`（6187）(FACT)，供 `keras.models.load_model(..., custom_objects=...)` 反序列化含该自定义层的检查点。被 `DDQNAgent.__init__` 的三处 `load_model` 调用使用（6331、6587、6642）。注：`CODE/leo_sim/learning.py:272` 存在同名函数（新平台侧独立实现），与本函数无调用关系。

---

#### `class DDQNAgent` — CODE/SimulationRL.py:6190

- 定位：CODE/SimulationRL.py:6190（类体延伸至 7766，共约 1577 行，20 个方法）
- 职责：Deep (Double) Q-Network 路由 agent：按多种状态模式构建状态、用 qNetwork/qTarget 做 ε-贪婪决策、把逐跳转移存入经验回放并批量训练 (FACT，类体与方法实现)。
- 关键状态/结构：`actions=('U','D','R','L')`（6192）；`states` 名称列表随 `reducedState/diff_lastHop/_SIM_M2_FIX/_SIM_M3_DYNAMICS/_SIM_STATE_MODE('c2'..'c7')` 变化（6194–6239）；`stateSize`/`_base_state_dim`，MAPPO frame-stack 与 `temporal_encoder` 可改写 `stateSize`（6244–6260）；`routing_mode` 取全局 `SIM_ROUTING_MODE`，`_SIM_CSR_MODE=='csr'` 时强制 `ddqn_csr`（6304–6318）；可选 `_mappo_bp` Backpressure 先验（6265–6281）；导入模式下预加载检查点并按输出维度/伴随 `csr_w_*.npz` 自动判别 `ddqn/ddqn_cvar/ddqn_csr`（6323–6403，`_SIM_FAIL_CLOSED` 下方法不符直接 raise）；`n_quantiles`（6405–6412）；routing hooks 三件套 `_local_stats_hook/_scoring_hook/_selector_hook`（6414–6434）；`experienceReplay = ExperienceReplay(bufferS)`（6444）；`qNetwork/qTarget`（6478–6499 新建或 6573–6672 导入）；可选 `q_global/q_global_target` 集中式 critic（6504–6532）与 `pc_mixer` 路径信用混合器（6538–6572）；`_SHADOW` 影子统计经 `_infer` 采样；`_w_version` 权重版本号（7643）。
- 关键流程/方法（逐个）：
  - `__init__(self, NGT, hyperparams, earth, sat_ID=None)`(6191)：如上组装状态空间定义、超参拷贝（6287–6303）、路由模式判别与 hooks、互斥检查（`_SIM_PATH_CREDIT`×`_SIM_CRITIC_GLOBAL`、`_SIM_PATH_CREDIT`×CSR，6454–6467）、建/导入网络、初始同步 qTarget（6492）、建 critic/pc_mixer、末尾 `_capture_encoder_initial_weights()`（6679）。`sat_ID=None` 表示这是 earth 级共享 agent，打印摘要。
  - `_graph_encoder_layer`(6681)：c4–c7 模式下从 `qNetwork.get_layer('graph_encoder')` 取编码层，否则/异常返回 None。
  - `_encoder_weights_vector`(6689)：把编码层全部可训练变量拼成一个 float32 一维向量，无层/无变量返回 None。
  - `_capture_encoder_initial_weights`(6703)：存编码层初始权重向量副本到 `_encoder_initial_weight_vec`。
  - `_encoder_weight_stats`(6707)：返回 (当前权重范数, 与初始向量的差范数)，无初始快照时后者为 nan。
  - `_infer(newState)`(6717)：决策时 Q 前向入口——惰性构建并缓存 `_infer_fn`（6720–6723），调用之；`_SIM_SHADOW_INFER` 开启时按 1-in-N 采样调 `_shadow_record`（6725–6728）。返回形状 (1, actionSize) 的 np.ndarray。
  - `_build_infer_fn`(6731)：按 env `SIM_INFER_BACKEND` 构建前向闭包——非标准路由模式（csr/cvar）或 backend=keras 时用 eager `net(s).numpy()`（6757–6759）；`tffunc` 用固定输入签名 (1,stateSize) 的 `tf.function`（6749–6755, 6760–6763）；`numpy` 要求 6 个权重张量否则回退 tffunc，命中时用 `_w_version`+网络对象 id 做版本化权重缓存、前向走 `_np_mlp_forward`（6764–6786）；未知后端回退 keras（6787–6789）；经内部 `_record_backend`（6737–6747）把生效后端与回退原因记入 `earth._infer_backends_effective/_infer_backend_fallbacks`。
  - `getNextHop(newState, linkedSats, sat, block)`(6791)：选动作并返回下一跳。explore 分支按 `alignEpsilon` 得 ε 后随机选，不可用方向先存一条 `unavPenalty` 自转移（terminated 语义随 `_SIM_MULTISTEP` 变，6806–6811）再重抽（6801–6814）；exploit 分支：`noPingPong` 时若某邻居即目的地 linkedSat 则直达返回（6818–6836）；调 `_local_stats_hook.on_pre_decision`（6856）；csr 模式走 `csr_q_values` 否则 `_infer`（6857–6861）；c6/c7 调 `_sample_raac_reliability`（6862–6863）；有 `_mappo_bp` 时计算 own/nbr 队列、progress、loop 四方向数组并按 `_SIM_BP_CORRECT` 选 DBPR 逐 commodity 公式或 `compute_bp`，`_SIM_BP_ONLY` 时 Q 置零，融合分数写回 `q_raw`（6867–6937，异常静默退化为纯 Q，6938–6940）；`_scoring_hook.score`→`_selector_hook.select_exploitation` 得动作（6941–6948）；写决策日志（`_append_decision_log`，6952–6955）与 eval 期 `REPLAY_TRACE` 决策轨迹（6958–6972）；返回 `[ID, lon°, lat°], actIndex`，异常返回 -1（6975–6978）。
  - `_ms_store(block, s_old, a_old, reward, s_new, terminated)`(6980)：n 步基线存储——`_SIM_TDLAMBDA_ON` 时转 `_tdl_store`；否则把 (s,a,r) 追加 `block.ms_buf`，terminated 时把窗内全部前缀折扣回报以 done=True 落盘并清空，窗满 `_SIM_NSTEP` 时以最老 hop 的 N 步折扣回报 + 自举 s_new 落一条并左移（6995–7012）。
  - `_ms_flush_lost(block)`(7014)：丢包时把 `block.ms_buf` 中未完成的 n 步窗按 terminal（无自举）全部 flush；`_SIM_TDLAMBDA_ON` 时转 `_tdl_flush`（7018–7031）。
  - `_tdl_store(block, s_old, a_old, reward, terminated)`(7033)：TD(λ) 基线——只追加轨迹，terminal 时调 `_tdl_flush`。
  - `_tdl_flush(block)`(7042)：用 `routing_multistep.lambda_return_transitions` 对缓存轨迹算前向 λ-回报（value_fn = 当前 qNetwork 的 max_a Q，7055–7057），每跳以 done=True 存入回放并清空（7049–7062）。
  - `makeDeepAction(block, sat, g, earth, prevSat=None)`(7064)：主决策入口——`getDeepLinkedSats` 取邻接并建 next_action_mask（7094–7097）；按 `_SIM_STATE_MODE`/reducedState/diff/diff_lastHop 选 `getDeepStateVisK/VisKFlat/VisKGraph/RAACGraph/Reduced/Diff/DiffLastHop/getDeepState` 之一取状态（7098–7115）；状态为 None 记丢包并 flush（7117–7121）；`_apply_frame_stack`、`_temporal_apply` 改写状态（7124–7126）；有 `q_global` 时每 50 个 decision 重建/复用 `build_global_state` 缓存（7130–7159）；`_append_state_log`（7162）；若 linkedGT 即目的地：按 `distanceRew`∈{4,5,其他} 组到达奖励、存 terminal 转移（含 global_state/next_action_mask）、path-credit 轨迹补最后一跳并 push 'delivered'、`TrainThis` 时触发一次 `train`（7227，行内 FIXME 注释质疑此处训练）、按需画路径后返回 0（7165–7233）；否则 `getNextHop` 选动作（7236）；有 prevSat 时按 `distanceRew`∈{1..5} 选 `getDistanceReward/V2/V3/V4(或 _SIM_POTENTIAL_SHAPING 时 Potential)/V5` 加 `again` 惩罚与 `getQueueReward` 得奖励（7239–7272），存（或 n 步存）上一跳转移、path-credit 记 hop、`step % nTrain == 0` 时 `train`（7275–7297）；`ddqn` 时 `alignQTarget(hardUpdate)`（7304–7305）；回写 `block.oldState/oldAction/oldGlobalState`（7308–7311）；返回 nextHop（7313）。
  - `alignEpsilon(step, sat)`(7315)：与 `QLearning.alignEpsilon` 同公式的指数 ε 衰减，追加到 `self.epsilon` 并返回 ε（7324–7327）。
  - `alignQTarget(hardUpdate=True)`(7329)：hard 模式每 `updateF` 次调用整体拷贝 qNetwork→qTarget 并计 `_target_sync_count`（7346–7352）；否则按 `tau` 软更新（7354–7356）。（注：docstring 首句称"此函数现在未使用"，但 7305 行每决策都调用——docstring 与实现不符，FACT。）
  - `createModel`(7358)：按路由模式建网络——`ddqn_cvar` 走 `build_quantile_model`（7359–7363），`ddqn_csr` 走 `build_csr_model`（7364–7373），c4–c7 走 `_create_graph_model`（7376–7377），默认建 `Dense(hiddenUnits,relu)×2 + Dense(actionSize,linear)` 的 Sequential 并以 `Adam(lr=learningRate[, clipnorm=Clipnorm])`、mse 编译（7382–7388）。
  - `_create_graph_model(state_mode)`(7390)：Functional 建模——`Input(stateSize)`→`GraphMessagePassingReadout`（c4/c7 用 gat、c5/c6 用 mpnn；c6/c7 传 reliability_aware/aoi_gate/action_feat_dim，7397–7414）→两个 `Dense(hiddenUnits,relu)`（7415–7418）→RAAC 时 `Dense(1)→Reshape((actionSize,))` 共享动作分（7419–7421），否则 `Dense(actionSize)`（7423）→ mse 编译返回（7424–7427）。
  - `_build_fast_train_fn`(7429)：构建一次性编译的 `tf.function` 训练步（SIM_FAST_TRAIN）：输入签名含 states/actions/rewards/nextStates/not_done/next_action_mask（7442–7449），内部算 masked target（无效动作置 -1e9；`_SIM_TRUE_DDQN` 且 ddqn 时用在线网 argmax、目标网取值，否则 masked target max），`rewards + not_done·γ^N·future` 为目标，MSE/chosen-action/A 反传并 `apply_gradients`（7451–7478）。
  - `_fast_train_step_call(...)`(7480)：模型对象被换（id 变化）时重建编译函数再执行一次训练步（7482–7496）。
  - `train(sat, earth)`(7498)：批量训练入口——cvar/csr 模式分别委托 `train_quantile_ddqn`/`train_csr_ddqn`（7499–7506）；回放样本 < 3·batchS 直接返回 -1（7507–7508）；取批（critic 模式用 `getBatchWithAux`+`getGlobalArraysFromBatch` 对齐 global state，7512–7519）；`_safe_next_action_mask` 处理掩码（7530）；满足 `_SIM_FAST_TRAIN` 等条件走编译步否则 eager 算 expectedRewards（true-DDQN 或 target-DQN  masked 自举，γ 取 `γ^_SIM_NSTEP`，7535–7552）；`stopLoss` 达标时置全局 `TrainThis=False` 并返回（7558–7571）；eager 路径 predict-then-targeted-update 只改被选用动作的目标值（7588–7590）；有 critic 且半数以上样本 valid 时训练 q_global 并按 `_SIM_DISTILL_LAMBDA` 在选用动作处混入蒸馏目标（7597–7633）；编译/普通路径各执行一步训练并计 `earth._fast_train_steps/_eager_train_steps`（7635–7642）；`_w_version` 自增（7643）；记 loss/trains（7644–7645）；每 `updateF` 次训练同步 `q_global_target`（7648–7650）；每 100 次训练打印收敛监控（ε、平均 loss、Q 方差、动作熵；`_SIM_LOG_LEVEL>=1` 时附分位数/动作计数到 `earth.train_log`，c4–c7 附编码器范数与 diagnostics 到 `earth.encoder_log`，7653–7699）；`_SIM_BUFFER_SNAPSHOT_INTERVAL>0` 时定期把回放存 npz（7703–7718）；`_SIM_PATH_CREDIT` 时按 `EVERY_K` 调 `pc_mixer.train_step` 并记 `earth.pc_log`（7723–7766）。
- 输入/输出：`getNextHop` 返回 `([ID, lon°, lat°], actIndex)` 或异常时 `-1`；`makeDeepAction` 返回 nextHop 三元组或 0（到达/丢包）；`train` 返回训练步 loss 转 float 前的控制流结果（cvar/csr 委托返回值、-1 或 None，FACT：主路径无显式 return 值，仅副作用）。
- 依赖关系：
  - 构造方：`initialize()` 的 8062 行（`earth.DDQNA`，共享 agent）与 8070 行（`sat.DDQNA`，per-satellite agent，传 `sat.ID`）。
  - 决策入口被调方：`makeDeepAction` 被 `Satellite.receiveBlock`(2017) 的 2073/2075/2080/2082 行与 `Earth.updateSatelliteProcessesRL`(4504) 的 4567–4721 行多处调用。
  - 内部调用同文件函数：`getDeepLinkedSats`(9381)、各 `getDeepState*`（9547–10192）、`getQueues`(9050)、`getSlantRange`(10261)、`getDistanceReward` 系列（10296–10383）、`getQueueReward`(10269)、`visKFlatDim`(9878)、`graphStateDim/raacGraphStateDim`(5901/5913)、`_append_state_log`(918)、`_sample_raac_reliability`(968)、`_append_decision_log`(1006)、`_append_reward_log`(1035)、`_pc_flush_lost`(1066)、`_append_packet_fate_log`(1109)、`_set_distance_diag`(1196)、`_temporal_apply`(9469)、`_apply_frame_stack`(9499)、`_bp_backlog_counts`(521)、`_safe_next_action_mask`(404)、`_masked_target_dqn_values`(425)、`_masked_double_dqn_actions`(434)、`plotShortestPath`(8968)、`_shadow_record`(5849)、`_np_mlp_forward`(5833)。
  - 跨文件被调方：`routing_hooks`（`LocalStatsHook/build_default_hooks`，6414）、`routing_mappo`（`BackpressurePrior/build_centralized_critic_per_action/build_global_state`，6268/6506/7133）、`routing_path_credit.build_path_credit_mixer`(6540)、`routing_multistep.lambda_return_transitions`(7052)、`temporal_encoder`(6253/6611)、`runtime_effect_receipt`（`new_checkpoint_receipt/attempt_checkpoint_load`，6619–6625，经同文件 30–31 行 import）。
  - **缺失依赖（FACT）**：`legacy.routing_csr`（6314/6361/6662/6858/7365/7504）、`legacy.routing_tailguard`（6423/7360/7500/12322）、`legacy.routing_mcp_hash`（6417）三模块在工作区不存在（无 `CODE/legacy/` 目录，`find` 全工作区无匹配文件）；均为方法内延迟 import，且模块级 474–479 行在 `SIM_CSR_MODE=csr` 时直接 `raise RuntimeError("…legacy.routing_csr, which is not present in retained CODE…")`。因此 csr/cvar/mcp_hash 三条路由路径在当前工作区代码下不可执行到 import 成功 (FACT：import 目标文件不存在；INFERENCE：运行时触发这些分支会 ImportError——csr 分支在模块 import 阶段已被 474–479 行的 guard 阻断，cvar/mcp_hash 分支无对应模块级 guard，会在 `__init__`/`train`/`createModel` 内延迟 import 时失败)。
  - `_ms_flush_lost` 被同文件模块级 `_pc_flush_lost` 在 1083 行调用。
  - 测试佐证：`CODE/tests/test_raac_tensorflow_contract.py:89-110` 直接调用 `DDQNAgent._build_fast_train_fn` 验证 masked target/double-DQN 语义；`CODE/tests/test_runtime_effect_receipt.py:122-128` 断言 `_create_graph_model`/`_build_fast_train_fn` 源码含 `shared_action_score`/`Reshape`/`masked_target`/`masked_online`；`CODE/tests/test_state_vis_k.py:116` 注释引用 `DDQNAgent.__init__` 的状态维度契约。

---

#### `class ExperienceReplay` — CODE/SimulationRL.py:7770

- 定位：CODE/SimulationRL.py:7770
- 职责：DDQN 经验回放缓冲：FIFO deque 存 (state, action, reward, nextState, terminated)，并平行存 global state 对与下一状态动作掩码 (FACT，docstring 7772–7782)。
- 关键状态/结构：`self.buffer = deque(maxlen=maxlen)`（7783）；`self.global_buffer`（存 `(g_state, g_next_state)` 或 None，7786）；`self.next_action_mask_buffer`（7787）；三者同 maxlen、同步 FIFO 淘汰。
- 关键流程/方法：
  - `__init__(maxlen=100)`(7771) 建三条 deque。
  - `store(state, action, reward, nextState, terminated, global_state=None, next_global_state=None, next_action_mask=None)`(7789)：追加转移；`global_state` 非 None 时存 float32 的 (g, g')（g' 缺省取 g），否则存 None（7798–7802）；`next_action_mask` 缺省为全 True，形状必须为 (4,) 否则 `raise ValueError`（7803–7806）。
  - `getBatch(batchSize)`(7808)：`random.sample(self.buffer, batchSize)` 随机取批（只回本地转移）。
  - `getBatchWithGlobal(batchSize)`(7814)：同一组随机下标取本地批与 global 批并返回二者（下标对齐）。
  - `getBatchWithAux(batchSize)`(7825)：同一组随机下标取本地批、global 批与掩码批（掩码缺失补全 True），返回三元组。
  - `getArraysFromBatch(batch)`(7835)：把批按字段拆成 float32 states/rewards、int64 actions、float32 nextStates、bool dones 五个数组。
  - `getGlobalArraysFromBatch(glob_batch)`(7849)：把 global 批转成 (gs, gns, valid_mask)，None 项补零向量（维度 `GLOBAL_STATE_DIM`，同文件 547 行=44）并标 invalid。
  - `buffeSize`(7870, @property)：返回 `len(self.buffer)`。
- 输入/输出：`store` 无返回；各 get 方法返回 list 或 numpy 数组元组。
- 依赖关系：被 `DDQNAgent.__init__` 在 6444 行实例化；`store` 被 `DDQNAgent.getNextHop`（6806）、`makeDeepAction`（7181/7191/7197/7278）、`_ms_store`（7004/7010）、`_ms_flush_lost`（7030）、`_tdl_flush`（7061）调用；`getBatchWithAux/getArraysFromBatch/getGlobalArraysFromBatch` 被 `DDQNAgent.train`（7513–7518）调用；`buffer` 属性被 `train` 的快照逻辑直接读取（7708–7714）；`getBatch` 调用方未确认（范围内未见调用）。测试佐证：`CODE/tests/test_runtime_effect_receipt.py:359-368` 验证 `store`/`getBatchWithAux` 的掩码下标对齐。
# 片段 s4：CODE/SimulationRL.py 第 7885–10237 行

### 文件 `CODE/SimulationRL.py`（实测 12556 行；本片段覆盖 7885–10237 行）

模块级说明：本片段范围内没有 import 语句和全局常量定义（import 集中于文件头 1–229 行，链路/状态常量集中于 293–626 行，均在本片段范围之外）。本片段范围内出现的模块级可执行语句只有两处：

- `_oracle_vis_k_stats = {"used_real_queue": 0, "masked": 0}`（CODE/SimulationRL.py:8778）：k-hop 可见性 oracle 的诊断计数器，注释（8774–8777）声明仅在 `SIM_ORACLE_VIS_K` 激活且给 `_oracle_global_dijkstra_edge_weight()` 传入 source 时被填充，每次 builder 调用时重置（FACT）。
- `_TE_MODULE = None`（CODE/SimulationRL.py:9466）：`temporal_encoder` 模块的惰性缓存，取值 None/模块对象/False（不可导入时），由 `_temporal_apply`（9469）读写（FACT）。

本片段代码引用、但定义在片段之外的模块级符号（行号为定义处）：`_SIM_FAIL_CLOSED`(219)、`pathings`/`_SIM_PATHING`/`pathing`(222/225/226)、`importQVals`/`onlinePhase`(262/263)、`Re`(293)、`Vc`(297)、`f`/`B`/`maxPtx`/`Adtx`/`Adrx`/`pL`/`Nf`/`Tn`/`min_rate`(302–310)、`BLOCK_SIZE`(318)、`coordGran`(332)、`_SIM_M2_FIX`(354)、`_SIM_M3_DYNAMICS`(361)、`_M3_EMA_ALPHA`(362)、`_sat_queue_dynamics`(364)、`_SIM_STATE_MODE`(374)、`_SIM_STATE_VIS_K`(375)、`_SIM_VIS_K_STALE_STEPS`(379)、`_SIM_VIS_K_UPDATE_INTERVAL_S`(383)、`_stale_queue_buffer`(387)、`_GRAPH_MAX_NODES`(391)、`_GRAPH_NODE_FEAT_DIM`(392)、`_RAAC_NODE_FEAT_DIM`(393)、`_RAAC_ACTION_FEAT_DIM`(394)、`_RAAC_AOI_SCALE_S`(395)、`_SIM_FRAME_STACK_K`(495)、`_SIM_MAPPO_MODE`(501)、`notAvail`(552)、`infQueue`(573)、`queueVals`(574)、`latBias`/`lonBias`(575/576)、`biggestDist`/`firstMove`(585/586)、`nnpath`/`nnpathTarget`(625/626)。

---

## 初始化与瓶颈分析

#### `def initialize(env, popMapLocation, GTLocation, distance, inputParams, movementTime, totalLocations, outputPath, matching='Greedy')` — CODE/SimulationRL.py:7885
- 定位：CODE/SimulationRL.py:7885
- 职责：仿真总初始化入口：建 Earth、链小区到 GT、建星座、建图、算全 GT 对最短路径、在各节点上建 SimPy 缓冲与发送进程、按需初始化 Q/DDQN 智能体（FACT，docstring 7886–7896 与函数体一致）。
- 关键状态/结构：读 `inputParams['Constellation'][0]`、`['Fraction'][0]`、`['Test type'][0]`（7900–7902）；构造 `Earth(...)`（7912，class Earth 定义于 3322）；调用 `earth.linkCells2GTs(distance)`（7917）；若 `earth._od_deferred` 且 `earth._pending_traffic_cfg` 非空则调用 `build_od_matrix_for_gateways`（7931，该函数 import 自 `traffic_od`，见第 20 行；定义于 CODE/traffic_od.py:347），失败时 `_SIM_FAIL_CLOSED` 为真则 raise，否则回退 uniform（7935–7942）；`mlab_hourly` 模式把 `hourly_matrices` 从 meta 中 pop 到 `earth.od_weight_matrices_hourly`（7948–7957）；`earth.linkSats2GTs("Optimize")`（7966）；`graph = createGraph(earth, matching=matching)`（7967）并赋给 `earth.graph` 和每个 `gt.graph`（7968–7971）；对所有 GT 对调 `getShortestPath(GT.name, destination.name, earth.pathParam, GT.graph)` 填 `GT.paths`（7976–7982）；`earth._needs_gt_fill_startup` 时调 `gt.makeFillBlockProcesses`（7984–7988）；`earth.trace_traffic_enabled` 时调 `earth.startTraceTraffic()`（7990–7991）；对每颗卫星调 `sat.findInterNeighbours(earth)`（7999），对有 linkedGT 的星调 `sat.adjustDownRate()` 并创建 GSL 发送进程（8005–8008），按图邻居把邻居分为 intra/inter 并创建 `sendBufferSatsIntra/Inter` 与对应 `sendBlock` 进程（8009–8033）；`_SIM_VIS_K_UPDATE_INTERVAL_S > 0` 时启动 `timedQueueSnapshotProcess`（8035–8036）；对 `paths[1]`、`paths[0]` 调 `findBottleneck`（8038–8039）；对每个 GT 调 `findBottleneck` 取最小值并按 GSL 上/下行速率调 `GT.getTotalFlow`（8043–8053）；`pathing` 为 `'Q-Learning'`/`'Deep Q-Learning'` 时构造 `hyperparam(pathing)`（8058，class hyperparam 定义于 5638）并 `saveHyperparams`（8075，定义于 10397）；DQL 且非 `onlinePhase` 时建全局 `DDQNAgent`（8062，class 定义于 6190），否则为每颗卫星各建一个（8068–8070）；Q-Learning 时调 `earth.initializeQTables`（8081）。注意：`pathing`、`onlinePhase`、`importQVals` 是模块级全局变量（226/263/262），不是参数（FACT）。
- 输入/输出：入 SimPy env、人口地图路径、GT csv 路径、覆盖距离、inputParams dict、movementTime、totalLocations、输出路径、matching 算法名；出 `(earth, graph, bottleneck1, bottleneck2)`（8083）。
- 依赖关系：调 Earth、build_od_matrix_for_gateways、createGraph、getShortestPath、findBottleneck、timedQueueSnapshotProcess、hyperparam、saveHyperparams、DDQNAgent；被 `RunSimulation`（定义于 12019）在 12106 行调用。跨文件调用方未确认其他。

#### `def findBottleneck(path, earth, plot=False, minimum=None)` — CODE/SimulationRL.py:8087
- 定位：CODE/SimulationRL.py:8087
- 职责：沿一条路径逐跳收集链路标识/数据率/纬度，求路径瓶颈速率（FACT）。
- 关键流程：首跳取源 GT 的 `GT.dataRate`（8090–8096）；中间跳在 `satellite.interSats`/`intraSats` 中找下一跳邻居并取其数据率（8098–8116）；末跳取目的 GT 的 `GT.linkedSat[1].downRate`（8117–8123）；`minimum` 入参非空时附加 `minimum/速率` 比值列（8096/8109/8116/8123）；`plot=True` 时调 `earth.plotMap` 并 `plt.show()`（8125–8128）；最终 `minimum = np.amin(bottleneck[1])`（8130）。
- 输入/输出：入 path（`getShortestPath` 返回的 [[name,lon,lat],...] 结构）、earth、plot 开关、可选 minimum；出 `(bottleneck, minimum)`，bottleneck 为 4 列列表 [链路名, 数据率, 纬度, 比值]（FACT）。
- 依赖关系：调 `earth.plotMap`、`np.amin`；被 initialize（8038/8039/8048）与 RunSimulation（12453）调用。

---

## 星座与几何/链路工具群

#### `def create_Constellation(specific_constellation, env, earth)` — CODE/SimulationRL.py:8135
- 定位：CODE/SimulationRL.py:8135
- 职责：按名字查表得到 Walker 星座参数（轨道面数 P、每面星数 N_p、总数 N、高度、倾角、Walker star/delta、最小仰角），并实例化全部 `OrbitalPlane`（FACT，参数表 8137–8195，实例化循环 8222–8224）。
- 关键状态/结构：支持 "small"/"Kepler"/"Iridium_NEXT"/"OneWeb"/"Starlink"/"Test" 六种名字（8137–8195）；未知名打印后 `exit()`（8196–8204）；`SIM_WALKER_PATTERN` 环境变量可覆盖 Walker_star，非法值在 `_SIM_FAIL_CLOSED` 下 raise（8206–8212）；Walker star 时分布角减半为 π（8214–8217）。
- 输入/输出：入星座名、env、earth；出 `orbital_planes` 列表（元素为 `OrbitalPlane`，class 定义于 1842）（FACT）。
- 依赖关系：调 `OrbitalPlane`、`os.environ.get`；被 `Earth.__init__` 在 3664 行调用（`self.LEO = create_Constellation(constellation, env, self)`）。

#### `def get_direction(Satellites)` — CODE/SimulationRL.py:8234
- 定位：CODE/SimulationRL.py:8234；职责：返回 N×N int8 矩阵，`direction[i,j]` 为含星 i 倾角与两星 y/z 坐标表达式的符号值（8243–8245），供双收发机方向配对使用（FACT，docstring 8235–8237）；输入：卫星对象列表；输出：np.ndarray (N,N) int8。被 markovianMatchingTwo(8383)、greedyMatching(8488)、establishRemainingISLs(8590) 调用。

#### `def get_pos_vectors_omni(Satellites)` — CODE/SimulationRL.py:8249
- 定位：CODE/SimulationRL.py:8249；职责：抽出全部卫星的 (x,y,z) 坐标矩阵与所在轨道面编号数组（FACT，8253–8259）；输入：卫星列表；输出：`(Positions (N,3), meta (N,))`。被 markovianMatchingTwo(8384)、greedyMatching(8489)、establishRemainingISLs(8589) 调用。

#### `def get_slant_range(edge)` — CODE/SimulationRL.py:8263
- 定位：CODE/SimulationRL.py:8263；职责：返回 `edge.slant_range` 属性（8264）（FACT）；输入：edge 对象；输出：数值。被 markovianMatchingTwo 在 8400 行用作 `sorted` 的 key。

#### `def get_slant_range_optimized(Positions, N)` — CODE/SimulationRL.py:8268
- 定位：CODE/SimulationRL.py:8268；职责：计算 N 颗卫星两两欧氏距离的对称矩阵，对角线置 `math.inf`，只算上三角再转置相加（8272–8277）（FACT）；输入：位置矩阵与 N；输出：(N,N) 距离矩阵。被 markovianMatchingTwo(8385)、greedyMatching(8490)、establishRemainingISLs(8591) 调用。

#### `def los_slant_range(_slant_range, _meta, _max, _Positions)` — CODE/SimulationRL.py:8282
- 定位：CODE/SimulationRL.py:8282；职责：带 `@numba.jit` 装饰（8281）；把距离矩阵中超过 `_max[_meta[i],_meta[j]]`（轨道面对最大可视距离）的元素置为 `math.inf`（8286–8291）（FACT）；输入：距离矩阵、轨道面数组、最大距离矩阵、位置矩阵（_Positions 在函数体内未被使用，FACT）；输出：裁剪后的距离矩阵副本。被 markovianMatchingTwo(8386)、greedyMatching(8491)、establishRemainingISLs(8615) 调用。

#### `def get_data_rate(_slant_range_los, interISL)` — CODE/SimulationRL.py:8295
- 定位：CODE/SimulationRL.py:8295
- 职责：由可视距离矩阵计算全部卫星对的可行数据率矩阵（FACT）。
- 关键流程：内置两张硬编码阈值表 `speff_thresholds`（频谱效率，8299–8304）与 `lin_thresholds`（线性 SNR 门限，8305–8311）；计算自由空间路径损耗 `10*log10((4π·d·f/Vc)^2)`（8313）、SNR（8314）、香农速率（8315，该值算出后未被返回直接使用，FACT）；再逐元素找满足门限的最高频谱效率并乘带宽得 `speffs`（8317–8325）。
- 输入/输出：入可视距离矩阵、`RFlink` 对象（class 定义于 1798，取其 f/maxPtx_db/G/No/B 属性）；出 (N,N) 数据率矩阵（bit/s）（FACT）。
- 依赖关系：用全局 `Vc`(297)；被 markovianMatchingTwo(8387)、greedyMatching(8492)、establishRemainingISLs(8616) 调用。

---

## 匹配/建图函数群

#### `def markovianMatchingTwo(earth)` — CODE/SimulationRL.py:8330
- 定位：CODE/SimulationRL.py:8330
- 职责：为每星两台星间收发机（各占一个方向）贪心地选跨轨道面 ISL，再补上同面上下星 intra ISL，返回 edge 列表（FACT，docstring 8331–8340 与实现一致）。
- 关键流程：硬编码构造 26GHz/500MHz 的 `RFlink`（8353–8363，注意与 greedyMatching 不同，这里不用全局 f/B 等参数，FACT）；按各轨道面高度算面对最大可视距离矩阵 `Max_slnt_rng`（8367–8378）；依次调 get_direction/get_pos_vectors_omni/get_slant_range_optimized/los_slant_range/get_data_rate（8383–8387）；枚举跨面对且方向收发机未被占用的候选边（距离 < 6000km，8394–8398），按 slant_range 升序排序（8400），循环取当前最短且两端方向均未覆盖的边并标记覆盖（8404–8409）；随后对每个轨道面内每颗星调 `sat.findIntraNeighbours(earth)` 并追加 upper/lower 两条 intra 边（8413–8433）。
- 输入/输出：入 earth；出 `_A_Markovian`，元素为 `edge` 类实例（class 定义于 2472），携带 i/j/slant_range/dij/dji/shannonRate（FACT）。
- 依赖关系：调 RFlink、get_direction、get_pos_vectors_omni、get_slant_range_optimized、los_slant_range、get_data_rate、get_slant_range、edge；被 createGraph 在 8685 行（`matching=='Markovian'` 分支）调用。

#### `def greedyMatching(earth)` — CODE/SimulationRL.py:8438
- 定位：CODE/SimulationRL.py:8438
- 职责：贪心建链：每星连同面上下星 + 异面 x 坐标更大/更小方向上最近的星各一颗（"东/西"），返回 edge 列表（FACT，docstring 8439–8444 与实现一致）。
- 关键流程：用模块级全局 f/B/maxPtx/Adtx/Adrx/pL/Nf/Tn/min_rate（302–310）构造 `RFlink`（8459–8469）；算面对最大可视距离（8473–8484）；算方向/位置/距离/可视距离/数据率矩阵（8488–8492）；对每颗星在异面星中按 `Positions[j,0] > Positions[i,0]` 判"东"、`<` 判"西"，取可视距离最小者各加一条边（8495–8510，方向字段传 None）；再加同面 upper/lower 两条 intra 边（8514–8534）。
- 输入/输出：入 earth；出 `_A_Greedy`（edge 列表）（FACT）。
- 依赖关系：调 RFlink、get_direction、get_pos_vectors_omni、get_slant_range_optimized、los_slant_range、get_data_rate、edge；被 createGraph 在 8687 行（`matching=='Greedy'` 分支）调用。

#### `def deleteDuplicatedLinks(satA, g, earth)` — CODE/SimulationRL.py:8539
- 定位：CODE/SimulationRL.py:8539
- 职责：若某星的东（dir 3）或西（dir 4）方向出现重复链路，删除纬度差较大的那条，保留更"水平"的链路（FACT，docstring 8540–8543 与实现一致）。
- 关键流程：内含嵌套函数 `getMostHorizontal(currentSat, satA, satB)`（8545），返回两候选星中纬度更接近 currentSat 者（8549）；遍历 `g.edges(satA.ID)`，对卫星邻居（节点名首字符为数字，8553）调 `findByID`+`getDirection`；东向重复时 `g.remove_edge` 删掉较不水平者（8557–8566），西向同理（8568–8577）。
- 输入/输出：入卫星、图、earth；出无返回值，直接改图 g（FACT）。
- 依赖关系：调 findByID、getDirection；被 createGraph 在 8709 行对每个卫星调用。

#### `def establishRemainingISLs(earth, g)` — CODE/SimulationRL.py:8580
- 定位：CODE/SimulationRL.py:8580
- 职责：为 `right`/`left` 仍为 None 的卫星补建跨面 ISL：把缺右邻的星与缺左邻的星两两配对，按纬度差升序依次建边（FACT，8580–8652）。
- 关键流程：重算位置/方向/距离/可视/数据率矩阵（8589–8616）；收集 `sat.right is None` 与 `sat.left is None` 两个集合（8619–8620）；候选配对要求异面、可视距离有限、经度差 (0,180)（8626–8632），按纬度差排序（8639）；循环中对两端仍空位的配对执行 `g.add_edge(..., slant_range=distance, dataRate=1/_sr, dataRateOG=_sr, hop=1)` 并互设 `sat_r.right`/`sat_l.left`（8643–8649）。
- 输入/输出：入 earth、图 g；出修改后的 g（8652）（FACT）。
- 依赖关系：调 get_pos_vectors_omni、get_direction、get_slant_range_optimized、RFlink、los_slant_range、get_data_rate；被 createGraph 在 8720 行调用。

#### `def createGraph(earth, matching='Greedy')` — CODE/SimulationRL.py:8655
- 定位：CODE/SimulationRL.py:8655
- 职责：构建整个网络拓扑图：卫星与 GT 为节点，GSL/ISL 为边，并给 slant_range 路由封印拓扑校验标记（FACT）。
- 关键流程：`nx.Graph()`（8663）；加全部卫星节点（8667–8669）；为有 linkedSat 的 GT 加节点与 GSL 边（8673–8680，边属性 slant_range/invDataRate/dataRateOG/hop）；按 `matching` 调 markovianMatchingTwo 或 greedyMatching（8684–8687）；把返回的 edge 逐条 `g.add_edge`，`dataRate=1/max(shannonRate,1.0)`、`dataRateOG=max(shannonRate,1.0)`（8694–8701）；`firstMove` 为真时更新全局 `biggestDist`（8702–8703，全局定义于 585/586）；对每星调 deleteDuplicatedLinks（8707–8709）；置 `earth.graph = g` 并对每星调 `findIntraNeighbours`+`findInterNeighbours`（8711–8717）；调 establishRemainingISLs（8720）；随后遍历所有边校验 `slant_range` 为有限正数，生成排序边表并 sha256，把结果封印进 `g.graph["_slant_range_marker"]`，同时初始化 `g.graph["_slant_range_runtime"]` 计数器（8725–8759）；校验出错且 `_SIM_FAIL_CLOSED` 且 `pathing=="slant_range"` 时 raise ValueError（8761–8763）；`firstMove` 首次打印最大星间距并置 False（8766–8768）。
- 输入/输出：入 earth、matching 算法名；出 `nx.Graph`，边属性含 slant_range/dataRate/dataRateOG/hop/dij/dji（FACT）。
- 依赖关系：调 markovianMatchingTwo、greedyMatching、deleteDuplicatedLinks、establishRemainingISLs、hashlib.sha256；被 Earth 方法（5273）与 initialize（7967）调用。

---

## oracle / 最短路径

#### `def _parse_oracle_vis_k(raw)` — CODE/SimulationRL.py:8781
- 定位：CODE/SimulationRL.py:8781；职责：解析 `SIM_ORACLE_VIS_K` 环境变量原值：None/空串/"inf"/"infinity"/不可解析/≤0 一律返回 None（不激活），正整数返回 k（8791–8804）（FACT）；输入：任意原值；输出：int 或 None。被 `_oracle_global_dijkstra_edge_weight` 在 8868 行调用。

#### `def _oracle_global_dijkstra_edge_weight(g, source=None)` — CODE/SimulationRL.py:8807
- 定位：CODE/SimulationRL.py:8807
- 职责：返回一个 networkx 风格的边权函数，权重 = 传播时延 + 单块发送时延×(1+queue_factor×队列长度)，作为"全知"队列感知 Dijkstra 基线（FACT，docstring 8808–8838 与实现一致）。
- 关键流程：`queue_factor` 读 `SIM_ORACLE_QUEUE_FACTOR`（默认 1.0，8839）；内部 `_queue_len(u,v)` 按端点类型取队列长度：星-星调 `sat_u.outbound_queue_len_for_neighbor(sat_v)`，星-GT 取 `len(sat_u.sendBufferGT[1])`，GT-星取 `len(gt_u.sendBuffer[1])`（8841–8855）；`_weight` = `slant_range/Vc + BLOCK_SIZE/max(dataRateOG,1.0) * (1+queue_factor*queue_len)`（8857–8863）；`_parse_oracle_vis_k` 不激活或未传 source 时直接返回 `_weight`（8868–8870）；激活时以 `nx.single_source_shortest_path_length(g, source, cutoff=k)` 求 k 跳内节点集（8877），重置 `_oracle_vis_k_stats`（8884–8885），返回 `_weight_visible_only`：两端都在 k 跳内用真实队列并累计 `used_real_queue`，否则队列按 0 并累计 `masked`（8887–8898）。
- 输入/输出：入拓扑图 g、可选 source 节点 ID；出边权闭包 `(u, v, attrs) -> float`（FACT）。
- 依赖关系：调 _parse_oracle_vis_k、nx.single_source_shortest_path_length；被 getShortestPath 在 8941 行（`weight=='oracle_global_dijkstra'` 分支）调用。注释（8777）提到 `scripts/oracle_vis_k_smoke.py` 使用该计数器，但当前 CODE/scripts 下未找到该文件（FACT：find 无结果），外部引用未确认。

#### `def getShortestPath(source, destination, weight, g)` — CODE/SimulationRL.py:8903
- 定位：CODE/SimulationRL.py:8903
- 职责：计算 source 到 destination 的最短路径并整理成 [节点名, 经度, 纬度] 列表（FACT，docstring 8904–8910）。
- 关键流程：`weight=="slant_range"` 时先做封印校验：`g.graph` 必须有 `_slant_range_marker`、节点/边数与封印一致、标记报告全部边权合法，否则 raise（8915–8927），并定义严格权函数 `_strict_slant_weight`（缺属性、非数值、非有限正值均 raise，8929–8937），累计 `_slant_range_runtime` 计数；其他 weight 若为 `'oracle_global_dijkstra'` 则换 `_oracle_global_dijkstra_edge_weight(g, source=source)`，否则原样传给 `nx.shortest_path`（8941–8942）；对结果做端点绑定与逐跳边存在性校验（8943–8946）；路径首末节点经纬度直接取值、中间节点 `math.degrees` 转换（8947–8952）；异常时若 `_SIM_FAIL_CLOSED` 且 slant_range 则 re-raise，否则打印并返回 -1（8956–8964）。
- 输入/输出：入源/目的节点名、权重模式字符串或权函数、图 g；出 path 列表或 -1（FACT）。
- 依赖关系：调 _oracle_global_dijkstra_edge_weight、nx.shortest_path；被 Satellite 方法（2104）、Earth 多个方法（3910/3925/3939/3953/4128/4159/4189/4220/5022/5321）、initialize（7980）调用；测试 CODE/tests/test_runtime_effect_receipt.py:575 覆盖其 slant_range 失败路径（标记缺失时返回 -1 并计数 failures，见该文件 529–576）。

#### `def plotShortestPath(earth, path, outputPath, ID=None, time=None)` — CODE/SimulationRL.py:8968
- 定位：CODE/SimulationRL.py:8968；职责：调 `earth.plotMap(True, True, path=path, ID=ID, time=time)` 并把图存为 `outputPath + 'popMap_<首节点>_to_<末节点>.png'`（dpi=500），随后 `plt.close()`（8969–8972）（FACT）；输入：earth、path、输出目录、可选 ID/time；输出：无返回，写 PNG 文件。被 2098、4618、4681、4742、5749、7232、12437 行调用。

#### `def normalize(arr, t_min, t_max)` — CODE/SimulationRL.py:8975
- 定位：CODE/SimulationRL.py:8975；职责：把数组 min-max 线性缩放到 [t_min, t_max]（8976–8982）（FACT）；输入：数值序列与目标区间；输出：list。调用方未确认（全文件及 CODE/ 下 grep 仅命中其他文件注释里的 "normalize" 字样，无实际调用）。

---

## 队列观测函数群

#### `def watchScores(earth, g)` — CODE/SimulationRL.py:8990
- 定位：CODE/SimulationRL.py:8990；职责：逐星打印其与每个图邻居之间的 `getSatScore` 分数（邻居为 GT 时打印 "Gateway linked"）（8995–9007）（FACT）；输入：earth、图 g；输出：无返回，仅打印。调用方未确认（grep 无调用点）。

#### `def findByID(earth, satID)` — CODE/SimulationRL.py:9010
- 定位：CODE/SimulationRL.py:9010；职责：线性遍历 `earth.LEO` 各轨道面卫星，返回 ID 匹配的卫星对象；找不到时无显式返回（None）（9014–9017）（FACT）；输入：earth、卫星 ID 字符串；输出：Satellite 或 None。被 1544、2071–2075、2421（Satellite.findInterNeighbours 内）、4565–4709 多处及本片段内 8554/9005/9343 调用。

#### `def computeOutliers(g)` — CODE/SimulationRL.py:9020
- 定位：CODE/SimulationRL.py:9020；职责：对图中所有边的 slant_range 与 dataRateOG 分别做 IQR 统计，返回 (数据率下界 Q1−1.5·IQR, 距离上界 Q3+1.5·IQR)（9025–9047）（FACT）；输入：图 g；出 `(lowerFence, upperFence)`。被 getSatScore 在 9217 行调用。

#### `def getQueues(sat, threshold=None, DDQN=False)` — CODE/SimulationRL.py:9050
- 定位：CODE/SimulationRL.py:9050
- 职责：读取卫星四条出队（intra×2、inter×2）的当前长度；`DDQN=False` 时返回"最长队列超阈值或存在缺失链路"的布尔值，`DDQN=True` 时返回 `{'U','D','R','L'}` 长度字典（9073–9097）（FACT，docstring 9051–9072 描述了队列结构 tuple[list[event], list[DataBlock], ID]）。
- 关键流程：依次读 `sat.sendBufferSatsIntra[0][1]`/`[1][1]` 与 `sat.sendBufferSatsInter[0][1]`/`[1][1]` 的长度；任一索引/属性异常即置 `infQueue=True` 且该方向记 `np.inf`（9077–9092）；非 DDQN 返回 `max(queuesLen) > threshold or infQueue`（9095），DDQN 返回字典（9097）。
- 输入/输出：入卫星、阈值、DDQN 开关；出 bool 或 dict（FACT）。
- 依赖关系：被 6869/6889/6960/12189 行及本片段内 getStaleQueues、timedQueueSnapshotProcess、getObservedQueueRecord、getSatScore、_sat_queue_scores_for_graph、_appendOwnQueueM2、_viskFlatFeat、getDeepStateDiff、getDeepStateDiffLastHop、getDeepState 调用。

#### `def getStaleQueues(sat, DDQN=False, delay=0)` — CODE/SimulationRL.py:9100
- 定位：CODE/SimulationRL.py:9100
- 职责：返回带指定决策步数延迟的队列快照；delay=0 时直接透传 getQueues（FACT，docstring 9101–9119）。
- 关键流程：delay>0 时给 `earth._stale_neighbor_reads` 计数 +1（9122–9124）；以 `id(sat)` 为键在全局 `_stale_queue_buffer`（定义于 387）里维护 `deque(maxlen=delay+1)`，追加当前快照，历史不足 delay+1 时返回当前值，否则返回最旧一项（9125–9135），命中历史时给 `earth._stale_neighbor_history_hits` 计数 +1（9133–9134）。
- 输入/输出：入卫星、DDQN 开关、延迟步数；出与 getQueues 同型（bool 或 dict）（FACT）。
- 依赖关系：调 getQueues；被 getObservedQueueRecord 在 9189 行调用；测试 CODE/tests/test_runtime_effect_receipt.py:290–291 调用（delay=1 的环缓冲行为）。

#### `def timedQueueSnapshotProcess(env, earth)` — CODE/SimulationRL.py:9138
- 定位：CODE/SimulationRL.py:9138；职责：SimPy 进程：每隔 `_SIM_VIS_K_UPDATE_INTERVAL_S` 秒把每颗星的 {U,D,R,L} 队列字典连同 `env.now` 追加到 `earth._timed_queue_history[sat.ID]` 的 deque（9140–9149）；interval≤0 时直接 return（9141–9142）（FACT）；输入：env、earth；输出：生成器（SimPy process）。被 initialize 在 8036 行启动。

#### `def getTimedObservedQueues(observer, target)` — CODE/SimulationRL.py:9152
- 定位：CODE/SimulationRL.py:9152；职责：从 `earth._timed_queue_history[target.ID]` 由新到旧找第一条"采样时刻 + 端到端传播时延 ≤ 当前时刻"的快照返回；传播时延按当前拓扑最短路径逐跳 slant_range/Vc 求和，找不到路径则为 inf；每条候选都不满足时返回全 inf 字典、`float("inf")`、False（9158–9176）；过程中维护 `earth._timed_state_reads/_hits/_misses/_age_sum_s/_age_max_s` 计数（9159、9171–9175）（FACT）；输入：观察者星、目标星；输出 `(queues_dict, age_seconds, valid_bool)`。被 getObservedQueueRecord 在 9188 行调用。

#### `def getObservedQueues(observer, target)` — CODE/SimulationRL.py:9179
- 定位：CODE/SimulationRL.py:9179；职责：`getObservedQueueRecord(observer, target)[0]`，只取队列字典（9180）（FACT）；输入/输出：同 getObservedQueueRecord 的第一项。被 getDeepStateVisK（9595）与 _sat_queue_scores_for_graph（9641）调用。

#### `def getObservedQueueRecord(observer, target)` — CODE/SimulationRL.py:9183
- 定位：CODE/SimulationRL.py:9183；职责：观测分派器：target 即 observer 时返回实时 `getQueues` 结果、age=0、True；`_SIM_VIS_K_UPDATE_INTERVAL_S>0` 时走 getTimedObservedQueues；否则走 getStaleQueues（delay=`_SIM_VIS_K_STALE_STEPS`）、age=0、True（9185–9190）（FACT）；输入：观察者星、目标星；输出 `(queues, age_s, valid)`。被 getObservedQueues（9180）、getDeepStateRAACGraph（9818）调用；测试 CODE/tests/test_runtime_effect_receipt.py:342 及 1161（patch 点）引用。

#### `def hasBadConnection(satA, satB, thresholdSL, thresholdTHR, g)` — CODE/SimulationRL.py:9193
- 定位：CODE/SimulationRL.py:9193；职责：取边 `(satA.ID, satB.ID)` 的 slant_range 与 dataRateOG，返回"距离超阈或吞吐低于阈"的布尔值（9198–9201）（FACT）；输入：两星、两阈值、图；输出 bool。被 getSatScore 在 9221 行调用。

#### `def getSatScore(satA, satB, g)` — CODE/SimulationRL.py:9204
- 定位：CODE/SimulationRL.py:9204；职责：给"从 satA 发到 satB"打 0/1/2 三档分：satB 为 None 或其队列超 125（硬编码阈值，9216）→ 2；链路被 computeOutliers 判为差 → 1；否则 → 0（9219–9224）（FACT；docstring 9206–9214 说明阈值 125 的来源是历史实验观察，属注释声明）；输入：两星、图；输出 int。被 watchScores（9005）与 getState（9458–9461）调用。

#### `def getDeepSatScore(queueLength)` — CODE/SimulationRL.py:9228
- 定位：CODE/SimulationRL.py:9228；职责：把队列长度映射为 0..`queueVals` 的整数分：`queueLength > infQueue` 时返回 `queueVals`，否则返回 `floor(queueVals * log10(queueLength+1) / log10(infQueue))`（9230，用全局 queueVals=10、infQueue=5000，定义于 573/574）（FACT）；输入：队列长度数值；输出 int。被本片段内各深度状态构造函数（getDeepStateVisK 9596、_sat_queue_scores_for_graph 9642、getDeepStateRAACGraph 9819、_viskFlatFeat 9910、getDeepStateDiff 9989 等、getDeepStateDiffLastHop 10122 等、getDeepState 10202 等）调用。

---

## 方向/邻居函数群

#### `def getDirection_deprecated(satA, satB)` — CODE/SimulationRL.py:9233
- 定位：CODE/SimulationRL.py:9233；职责：旧版方向判定：同面按纬度返回 1（上）/2（下）；异面按经度差是否超过 π 决定是否反转东西逻辑，返回 3（右/东）/4（左/西）（9246–9263）（FACT）；输入：两星；输出 int 1–4。调用方未确认（grep 无调用点；名字带 _deprecated 且存在替代函数 getDirection）。

#### `def getDirection(satA, satB)` — CODE/SimulationRL.py:9266
- 定位：CODE/SimulationRL.py:9266；职责：方向判定：同面按纬度返回 1/2；异面把两星经度归一化到 [−π,π] 后按经度差符号返回 3（右）/4（左），处理跨 ±180° 回绕（9271–9295）（FACT）；输入：两星；输出 int 1–4。被 Satellite.findInterNeighbours（2422）、deleteDuplicatedLinks（8555）、getLinkedSats（9344）调用。

#### `def linkedSatsList(g)` — CODE/SimulationRL.py:9298
- 定位：CODE/SimulationRL.py:9298；职责：遍历图中所有非卫星节点（节点名首字符非数字，即 GT），收集其第一条边，返回 `pd.DataFrame`（每行一条 (GT名, 卫星ID) 边）（9302–9306）（FACT）；输入：图 g；输出 DataFrame。被 getDestination 在 9318 行调用。

#### `def getDestination(Block, g, sat=None)` — CODE/SimulationRL.py:9309
- 定位：CODE/SimulationRL.py:9309；职责：取 Block 目的 GT 所连卫星的 ID，在 linkedSatsList 结果中的位置索引并返回；`sat` 参数非 None 的分支只有 `pass` 与被注释掉的代码（9320–9325，即该分支未实现，FACT）；输入：DataBlock、图 g、可选 sat；输出 int 索引。被 getState 在 9455 行调用。

#### `def getLinkedSats(satA, g, earth)` — CODE/SimulationRL.py:9328
- 定位：CODE/SimulationRL.py:9328；职责：基于图边与 getDirection，把 satA 的卫星邻居分入 `{'U','D','R','L'}` 字典；同一方向出现第二个邻居时按纬度把更靠北/南者重排（极区回绕处理，9346–9364）；东/西方向后见者直接覆盖先见者（9366–9374）（FACT）；输入：卫星、图、earth；输出字典（值为 Satellite 或 None）。被 4536（Earth 方法内）与 5691（class QLearning 的方法内）调用。

#### `def getDeepLinkedSats(satA, g, earth)` — CODE/SimulationRL.py:9381
- 定位：CODE/SimulationRL.py:9381；职责：直接读卫星对象的 `upper/lower/right/left` 属性组装 `{'U','D','R','L'}` 字典（9391–9394）；g、earth 参数在函数体内未被使用，替代的图遍历实现整段被注释（9396–9411）（FACT）；输入：卫星、图、earth；输出字典。被 DDQNAgent.makeDeepAction（7064）在 7094/7251/7255 行调用。

#### `def getKHopNeighbors(satA, k)` — CODE/SimulationRL.py:9416
- 定位：CODE/SimulationRL.py:9416；职责：沿 `.upper/.lower/.right/.left` 做 BFS 至 k 跳，返回 `[(sat, hop, first_dir)]` 列表，first_dir 为从 satA 出发的首跳方向；每颗星按首次到达记录一次，None 链路跳过（9425–9440）（FACT，docstring 9417–9424 与实现一致）；输入：卫星、k；输出列表。被 getDeepStateVisK（9594）、getDeepStateVisKGraph（9678）、getDeepStateRAACGraph（9804）调用；测试 CODE/tests/test_state_vis_k.py:48–74 覆盖 k=1/k=2/角落节点/k=0 情形，CODE/tests/test_runtime_effect_receipt.py:1168、1220 处被 patch。

---

## 状态特征函数群

#### `def getState(Block, satA, g, earth)` — CODE/SimulationRL.py:9443
- 定位：CODE/SimulationRL.py:9443；职责：构造 Q-Table 用的 5 维状态：`[U,D,R,L 四方向 getSatScore 分数, 目的卫星索引]`，初始值全 2（最差），邻居来自 `satA.QLearning.linkedSats`（9455–9463）（FACT）；输入：DataBlock、卫星、图、earth；输出 list（调用处 5754 转成 tuple）。被 QLearning.makeAction（class QLearning 定义于 5682，方法定义于 5721）在 5754 行调用。

#### `def _temporal_apply(sat, state)` — CODE/SimulationRL.py:9469
- 定位：CODE/SimulationRL.py:9469；职责：惰性导入 `temporal_encoder` 模块并调其 `apply(sat, state)`；模块不可导入时置 `_TE_MODULE=False` 并原样返回 state；apply 抛异常时给 `earth._temporal_apply_failures` 计数并 re-raise；`mode() != "none"` 时给 `earth._temporal_apply_successes` 计数（9474–9496）（FACT）；输入：卫星、状态数组；输出：处理后的状态或原状态。被 DDQNAgent.makeDeepAction 在 7126 行调用；测试 CODE/tests/test_runtime_effect_receipt.py:285 验证模块缺失时的恒等透传。

#### `def _apply_frame_stack(sat, state)` — CODE/SimulationRL.py:9499
- 定位：CODE/SimulationRL.py:9499；职责：MAPPO 帧堆叠：`_SIM_MAPPO_MODE` 属于 ("framestack_bp","full_recurrent","bp_only") 且 `_SIM_FRAME_STACK_K>1` 时，在每星的 `sat._mappo_frame_buf`（deque(maxlen=K)）里维护最近 K 帧，不足 K 帧时左侧重复填充首帧，输出 (1, K×base_dim) 数组；否则原样透传（9511–9528）（FACT）；输入：卫星、单帧状态；输出 np.ndarray。被 DDQNAgent.makeDeepAction 在 7125 行调用。

#### `def getBiasedLatitude(sat)` — CODE/SimulationRL.py:9531
- 定位：CODE/SimulationRL.py:9531；职责：返回 `(int(degrees(sat.latitude)) + latBias) / coordGran`；AttributeError 时返回 `notAvail`（9532–9536）（FACT）；输入：卫星（或 None）；输出数值。被 getDeepStateReduced、getDeepState 调用。

#### `def getBiasedLongitude(sat)` — CODE/SimulationRL.py:9539
- 定位：CODE/SimulationRL.py:9539；职责：经度版本，`(int(degrees(sat.longitude)) + lonBias) / coordGran`，异常返回 notAvail（9540–9544）（FACT）；输入/输出同上。被 getDeepStateReduced、getDeepState 调用。

#### `def getDeepStateReduced(block, sat, linkedSats)` — CODE/SimulationRL.py:9547
- 定位：CODE/SimulationRL.py:9547；职责：构造 12 维纯位置深度状态：四邻居的 biased 经纬度（8 维）+ 自身 biased 经纬度（2 维）+ 目的星 biased 经纬度（2 维）；目的 GT 无 linkedSat 时打印并返回 None（9548–9563）（FACT）；输入：DataBlock、卫星、linkedSats 字典；输出 (1,12) np.ndarray 或 None。被 DDQNAgent.makeDeepAction 在 7109 行调用。

#### `def getDeepStateVisK(block, satA, k=None)` — CODE/SimulationRL.py:9566
- 定位：CODE/SimulationRL.py:9566
- 职责：C3 状态构造器：k 跳邻居按首跳方向分四组，对每组邻居的四方向队列分（getDeepSatScore(getObservedQueues(...))）取均值 4 维 + 最大值 4 维，再加该方向直连邻居相对位置 2 维，尾部加自身绝对位置 2 维 + 目的相对位置 2 维，`_appendOwnQueueM2` 按 `_SIM_M2_FIX` 门控追加 4 维；k 缺省取 `_SIM_STATE_VIS_K`（9577–9619）（FACT；docstring 9567–9576 声明固定 44 维、k=1 时等价于仅直连邻居）。
- 关键流程：嵌套 `_rel(neighbor_sat, cur, is_lat)` 计算带 ±180° 回绕的相对坐标 /coordGran（9584–9590）；`getKHopNeighbors(satA, k)` 分组聚合（9593–9597）；无邻居方向填 8 个 `float(queueVals)`（9607）；直连邻居缺失填 notAvail（9613）；目的 GT 无 linkedSat 时打印并返回 None（9580–9582）。
- 输入/输出：入 DataBlock、卫星、可选 k；出 (1, 44[+4]) np.float32 数组或 None（FACT）。
- 依赖关系：调 getKHopNeighbors、getObservedQueues、getDeepSatScore、_appendOwnQueueM2；被 DDQNAgent.makeDeepAction 在 7099 行（`_SIM_STATE_MODE=='c3'`）调用；DDQNAgent.__init__ 在 6225–6227 行按 44(+4) 维配套。

#### `def _sat_rel_coord(neighbor_sat, root_sat, is_lat)` — CODE/SimulationRL.py:9622
- 定位：CODE/SimulationRL.py:9622；职责：邻居相对 root 的纬度/经度差，带 ±180° 回绕后 /coordGran；AttributeError 返回 notAvail（9623–9628）（FACT）；输入：两星、纬度开关；输出数值。被 getDeepStateVisKGraph（9699/9700、9716/9717、9722/9723）调用。

#### `def _sat_abs_coord(sat, is_lat)` — CODE/SimulationRL.py:9631
- 定位：CODE/SimulationRL.py:9631；职责：星的绝对纬度/经度加 bias 后 /coordGran；AttributeError 返回 notAvail（9632–9637）（FACT）；输入：星、纬度开关；输出数值。被 getDeepStateVisKGraph（9720/9721）调用。

#### `def _sat_queue_scores_for_graph(sat, *, root=False, observer=None)` — CODE/SimulationRL.py:9640
- 定位：CODE/SimulationRL.py:9640；职责：root 时用实时 getQueues，否则用 getObservedQueues(observer, sat)，返回四方向 getDeepSatScore 列表（9641–9643）（FACT）；输入：星、root 标志、观察者；输出 4 维 list。被 getDeepStateVisKGraph 在 9690 行调用。

#### `def _sat_degree_norm(sat)` — CODE/SimulationRL.py:9646
- 定位：CODE/SimulationRL.py:9646；职责：返回星的 upper/lower/right/left 中非 None 的个数 / 4.0；任何异常返回 0.0（9647–9651）（FACT）；输入：星；输出 float。被 getDeepStateVisKGraph（9692）、getDeepStateRAACGraph（9821）调用。

#### `def getDeepStateVisKGraph(block, satA, k=None)` — CODE/SimulationRL.py:9654
- 定位：CODE/SimulationRL.py:9654
- 职责：C4/C5 图状态构造器：以 satA 为根的 k 跳 ISL 子图，输出定长拼接向量 [节点特征 (MAX_N,14) | 有向邻接 (MAX_N,MAX_N) | 按首跳方向分组的 readout 掩码 (4,MAX_N) | C3 兼容尾部]（FACT，docstring 9655–9664 与实现一致）。
- 关键流程：`discovered` = 根 + getKHopNeighbors，按 (hop, ID) 排序后截断到 `_GRAPH_MAX_NODES`，记录 overflow（9677–9682）；每节点 14 维特征：4 队列分（root 用实时，其余用观测）、hop/k、度归一、is-root、常数 1、首跳方向 one-hot（4 维）、相对坐标 2 维（9689–9700）；邻接按四方向属性建 `adj[dst,src]=1`（9704–9710）；尾部 = 四直连邻居相对坐标 + 自身绝对坐标 + 目的相对坐标 + `_appendOwnQueueM2`（9712–9724）；构造统计写入 `earth._graph_state_builds/_nodes_seen/_edges_seen/_overflow_nodes` 并调 `_append_graph_state_log`（定义于 937）（9726–9741）；最终 concatenate 成一行（9743–9749）。
- 输入/输出：入 DataBlock、卫星、可选 k；出 (1, N) np.float32 数组（N 由 graphStateDim()（5901）对应）或 None（目的 GT 无 linkedSat 时，9667–9670）（FACT）。
- 依赖关系：调 getKHopNeighbors、_sat_queue_scores_for_graph、_sat_degree_norm、_sat_rel_coord、_sat_abs_coord、_appendOwnQueueM2、_append_graph_state_log；被 DDQNAgent.makeDeepAction 在 7103/7105 行（c4/c5 分支）与 getDeepStateVisKGAT（9754）调用。

#### `def getDeepStateVisKGAT(block, satA, k=None)` — CODE/SimulationRL.py:9752
- 定位：CODE/SimulationRL.py:9752；职责：直接返回 `getDeepStateVisKGraph(block, satA, k=k)`（9754）（FACT）；docstring 称其为"旧 smoke 脚本的向后兼容名"（9753，FACT 为注释声明）；输入/输出：同 getDeepStateVisKGraph。调用方未确认（CODE/ 内 grep 无其他调用点）。

#### `def _ecef_relative(src, dst)` — CODE/SimulationRL.py:9757
- 定位：CODE/SimulationRL.py:9757；职责：返回 dst 相对 src 的 ECEF 坐标差向量，按地球半径 Re 归一化；属性/类型异常返回 [0,0,0]（9759–9767）（FACT）；输入：两个带 x/y/z 属性的对象；输出 3 维 list。被 getDeepStateRAACGraph（9826、9842、9855、9856）调用。

#### `def _reachable_without_root(first_hop, root, max_depth)` — CODE/SimulationRL.py:9770
- 定位：CODE/SimulationRL.py:9770；职责：从 first_hop 出发 BFS（不经过 root），深度上限 max_depth，返回可达节点的 id 集合（含 first_hop 自身）；first_hop 为 None 或 max_depth<0 时返回空集（9772–9788）（FACT）；输入：首跳星、根星、深度；输出 set。被 getDeepStateRAACGraph 在 9814 行调用。

#### `def getDeepStateRAACGraph(block, satA, k=None)` — CODE/SimulationRL.py:9791
- 定位：CODE/SimulationRL.py:9791
- 职责：C6/C7 图状态构造器：k 跳子图节点特征 17 维（含观测有效位与 AoI）+ 邻接 + 允许跨动作重叠的 readout 分支掩码 + 每动作 9 维 action 特征（FACT，docstring 9792 与实现一致）。
- 关键流程：发现/排序/截断逻辑与 getDeepStateVisKGraph 相同（9803–9808）；`branches[d]` = `_reachable_without_root(d 方向直连邻居, satA, k-1)`（9813–9816）；每节点特征：4 队列分（经 getObservedQueueRecord，带 age/valid）、hop/3.0、度归一、is-root、常数 1、首跳方向 one-hot、ECEF 相对 3 维、observed 标志、AoI=min(age/`_RAAC_AOI_SCALE_S`,10)（未观测或非有限时取 10）（9817–9829）；非根节点按 branches 成员关系填 readout（9830–9833）；邻接同 C4/C5（9835–9839）；action_feats 每方向 9 维：存在位、slant_range/maxSlantRange、dataRateOG/B、邻居→目的 ECEF 相对 3 维、自身→目的 ECEF 相对 3 维（9841–9856）；统计计数同 C4/C5（9858–9861）；输出 concatenate 后 (1,-1)（9862–9863）。
- 输入/输出：入 DataBlock、卫星、可选 k；出 (1, N) np.float32 数组（N 由 raacGraphStateDim()（5913）对应）或 None（9796–9797）（FACT）。
- 依赖关系：调 getKHopNeighbors、_reachable_without_root、getObservedQueueRecord、getDeepSatScore、_sat_degree_norm、_ecef_relative；被 DDQNAgent.makeDeepAction 在 7107 行（c6/c7 分支）调用；测试 CODE/tests/test_runtime_effect_receipt.py:1120（类 docstring）、1172、1225 调用并断言其输出契约。

#### `def _appendOwnQueueM2(state_list, sat)` — CODE/SimulationRL.py:9866
- 定位：CODE/SimulationRL.py:9866；职责：`_SIM_M2_FIX` 为真时向 state_list 追加 4 维自身出队占用（各方向队列长度/infQueue 截断到 1.0）；否则无操作（9872–9875）（FACT）；输入：可变 list、卫星；输出：无返回，原地修改 list。被 getDeepStateVisK（9618）、getDeepStateVisKGraph（9724）、getDeepStateVisKFlat（9949）调用。

#### `def visKFlatDim(k)` — CODE/SimulationRL.py:9878
- 定位：CODE/SimulationRL.py:9878；职责：返回 C2 扁平状态维度 `4 * (4*(4^k - 1)//3) + 4`（满 4 叉树 k 层节点数 × 4 队列分 + 自身绝对 2 + 目的相对 2）（9884–9885）（FACT）；输入：k；输出 int。被 DDQNAgent.__init__ 在 6230 行调用；测试 CODE/tests/test_state_vis_k.py:85–91、115–120 断言 k=1→20、k=2→84、k=3→340 及与 visKFlatUnroll 输出长度的一致性。

#### `def visKFlatUnroll(node, depth, feat_fn, pad_feat)` — CODE/SimulationRL.py:9888
- 定位：CODE/SimulationRL.py:9888；职责：纯递归位置展开：按 (upper,lower,right,left) 固定顺序把每个方向子树展开到 depth 层，子节点存在则插入 feat_fn(child) 特征，缺失则插入 pad_feat 且整个缺失子树全部填充；输出长度固定（9897–9904）（FACT）；输入：节点、深度、特征函数、填充特征；输出 list。被 getDeepStateVisKFlat 在 9944 行调用；测试 CODE/tests/test_state_vis_k.py:96–120 用 mock 网格覆盖。

#### `def _viskFlatFeat(child)` — CODE/SimulationRL.py:9907
- 定位：CODE/SimulationRL.py:9907；职责：返回该星四方向队列的 getDeepSatScore 列表（实时 getQueues，9909–9911）（FACT）；输入：卫星；输出 4 维 list。被 getDeepStateVisKFlat 在 9944 行作为 feat_fn 传入。

#### `def getDeepStateVisKFlat(block, satA, k=None)` — CODE/SimulationRL.py:9914
- 定位：CODE/SimulationRL.py:9914；职责：C2 扁平状态构造器：`visKFlatUnroll(satA, k, _viskFlatFeat, [queueVals]*4)` 得到位置化队列分序列，尾部加自身绝对位置 2 维 + 目的相对位置 2 维（嵌套 `_rel` 处理回绕），`_appendOwnQueueM2` 按门控追加；目的 GT 无 linkedSat 返回 None（9928–9950）（FACT）；输入：DataBlock、卫星、可选 k；出 (1, visKFlatDim(k)[+4]) np.float32 数组或 None。被 DDQNAgent.makeDeepAction 在 7101 行（c2 分支）调用。

#### `def getDeepStateDiff(block, sat, linkedSats)` — CODE/SimulationRL.py:9953
- 定位：CODE/SimulationRL.py:9953
- 职责：C1 默认深度状态：四个邻居各自的 4 队列分 + 相对坐标 2 维（4×6=24 维）+ 自身绝对坐标 2 维 + 目的相对坐标 2 维，共 26 维；`_SIM_M2_FIX` 追加自身队列占用 4 维；`_SIM_M3_DYNAMICS` 再追加队列速度 dq 4 维与 EMA 趋势 4 维（FACT，9987–10058）。
- 关键流程：嵌套 `normalize_angle_diff`（9954）、`get_relative_position`（9958）、`get_absolute_position`（9968）；目的 GT 无 linkedSat 打印并返回 None（9972–9975）；邻居队列经实时 getQueues 读取（9982–9985）；M3 在全局 `_sat_queue_dynamics`（定义于 364）按 id(sat) 维护 prev/ema_dq，alpha 取 `_M3_EMA_ALPHA`（10042–10056）。
- 输入/输出：入 DataBlock、卫星、linkedSats 字典；出 (1, 26[+4][+8]) np.ndarray 或 None（FACT）。
- 依赖关系：调 getQueues、getDeepSatScore；被 DDQNAgent.makeDeepAction 在 7111 行调用（注释标注 "This is the one being used by default"）。

#### `def getDeepStateDiffLastHop(block, sat, linkedSats)` — CODE/SimulationRL.py:10061
- 定位：CODE/SimulationRL.py:10061
- 职责：getDeepStateDiff 的变体：在最前面多 1 维"上一跳来源方向"特征（0=上/1=下/2=右/3=左/-1=上一跳星已非当前邻居或路径不足），其余结构（26 维 + M2/M3 门控追加）与 getDeepStateDiff 相同（FACT，10118–10189）。
- 关键流程：嵌套 `get_last_satellite(block, sat)`（10080）比较 `block.QPath[-2][0]` 与 sat.upper/lower/right/left 的 ID，要求 `len(block.QPath) > 2`（10087–10101）；其余嵌套函数与 M2/M3 块同 getDeepStateDiff（10062–10078、10163–10187）。
- 输入/输出：入 DataBlock、卫星、linkedSats 字典；出 (1, 27[+4][+8]) np.ndarray 或 None（10103–10106）（FACT）。
- 依赖关系：调 getQueues、getDeepSatScore；被 DDQNAgent.makeDeepAction 在 7113 行调用。

#### `def getDeepState(block, sat, linkedSats)` — CODE/SimulationRL.py:10192
- 定位：CODE/SimulationRL.py:10192；职责：28 维深度状态：四邻居各 4 队列分 + biased 经纬度 2 维（4×6=24 维）+ 自身 biased 经纬度 2 维 + 目的星 biased 经纬度 2 维；目的 GT 无 linkedSat 打印并返回 None（10193–10235）（FACT）；输入：DataBlock、卫星、linkedSats 字典；出 (1,28) np.ndarray 或 None。被 DDQNAgent.makeDeepAction 在 7115 行调用。
# 片段 s5：CODE/SimulationRL.py 第 10238–12556 行（文件末尾段）

## 文件 `CODE/SimulationRL.py`（实测 12556 行）

> 本片段只覆盖第 10238–12556 行。第 1–10237 行（全部 imports、全局常量/env 读取、`Logger`、`Results`、`DataBlock`、`Gateway`、`Earth`、`hyperparam`、`QLearning`、`DDQNAgent`、`ExperienceReplay` 等类与中部函数）由前序片段覆盖。
>
> 本范围内 `grep -nE '^(class |def )'` 结果：**0 个 class、35 个 def**。另有 1 个模块级 `if __name__ == '__main__':` 块（12528–12556）。

### 模块级说明（仅限 10238–12556 范围）

- **10255–10257、11490–11492、12018、12523–12526**：注释分隔带（`#####...`），分别标注 `Q-Learning - Rewards`、`Simulation && Results`、`Main` 三个分节，无代码 (FACT)。
- **12528–12556 `if __name__ == '__main__':` 块**（模块级可执行代码，FACT）：
  - 12529：`os.makedirs(outputPath, exist_ok=True)`（`outputPath` 全局变量定义于 653 行的另一个 `if __name__ == '__main__':` 块内，由 `SIM_RESULTS_ROOT` env、pathing、Test length、ArriveReward、w1、w2、GTs、流量标签拼成）。
  - 12530：`sys.stdout = Logger(outputPath + 'logfile.log')`（`Logger` 定义于 173，属前序片段）。
  - 12532–12547：若 env `SIM_WANDB` ∈ {1,true,yes,on}，尝试 `import wandb` 并 `wandb.init(project=WANDB_PROJECT 或 "leo-drl-routing", name=SIM_RUN_LABEL, group=SIM_CFG_PATH_TAG, config=全部 SIM_* env, mode=WANDB_MODE 默认 "offline")`；任何异常打印 `[wandb] init skipped (...)` 并继续（12546–12547）。
  - 12548–12555：`try: RunSimulation(GTs, './', outputPath, populationMap, radioKM=rKM)`；`finally` 中若 wandb run 存在则 `wandb.run.finish()`（异常吞掉）。`GTs`(276)、`populationMap`(663)、`rKM`(292) 均为文件头部全局变量。
  - 12556：注释掉的 `cProfile.run(...)` 替代入口。

#### 本片段消费、但定义于文件头部（1–10237）的全局符号速查（均为 FACT，仅列定义行）

| 符号 | 定义行 | 含义（依定义行注释/代码） |
|---|---|---|
| `pathing` | 226 | 路由方法选择，来自 env `SIM_PATHING`(225)，默认 `pathings[3]`=`'slant_range'`；可选列表见 222 |
| `SIM_ROUTING_MODE` | 231 | DDQN 路由变体（`_parse_sim_routing_mode()`） |
| `_SIM_FAIL_CLOSED` | 219 | env `SIM_FAIL_CLOSED` 开关 |
| `FL_Test` | 234 | CKA/联邦学习测试开关 |
| `plotAllThro` / `plotAllCon` | 236 / 237 | 吞吐图/拥塞图是否逐路径分别绘制 |
| `movementTime` / `ndeltas` | 239 / 241 | 星座位置更新周期 / 运动加速因子 |
| `Train` / `explore` / `importQVals` / `onlinePhase` | 260 / 261 / 262 / 263 | 训练/探索/导入 Q 值/多智能体在线相位开关 |
| `w1` / `w2` / `w4` | 270 / 271 / 272 | 奖励权重（w1、w2 可被 env `SIM_W1`/`SIM_W2` 覆盖） |
| `GTs` / `rKM` | 276 / 292 | 网关数列表 / 网关覆盖半径 km |
| `BLOCK_SIZE` | 318 | 数据块大小（bit），吞吐计算用 |
| `saveISLs` / `const_moved` / `matching` / `mixLocs` | 324 / 325 / 326 / 328 | ISL 图保存/移动标志/匹配算法/网关位置洗牌 |
| `diff_lastHop` | 334 | 29 维状态开关（env `SIM_DIFF_LAST_HOP`） |
| `_SIM_M1_FIX` / `_M1_BETA` | 344 / 345 | 队列奖励 exp 修复开关 / β=200 s⁻¹ |
| `_SIM_REWARD_LINEAR` / `_LINEAR_ALPHA` | 350 / 351 | 线性队列奖励开关（env `SIM_REWARD_LINEAR`/`SIM_LINEAR_ALPHA`） |
| `_SIM_STATE_MODE` / `_SIM_STATE_VIS_K` | 374 / 375 | 状态模式（c2–c7）/ k 跳邻居数 |
| `_SIM_VIS_K_STALE_STEPS` / `_SIM_VIS_K_UPDATE_INTERVAL_S` | 379 / 383 | 过期邻居状态步数 / 定时快照间隔 |
| `_GRAPH_MAX_NODES` / `_GRAPH_HIDDEN_DIM` / `_GRAPH_ATT_HEADS` / `_GRAPH_LAYERS` / `_GRAPH_LOG_EVERY` | 391 / 398 / 399 / 400 / 401 | 图状态编码器配置 |
| `_RAAC_AOI_SCALE_S` / `_RAAC_AOI_GATE` | 395 / 396 | RAAC AoI 门参数 |
| `_SIM_MULTISTEP` | 467 | n-step/TD(λ) 开关（由 `_SIM_NSTEP`、`_SIM_TDLAMBDA_ON` 推出） |
| `_SIM_CSR_MODE` | 474–479 | `SIM_CSR_MODE=csr` 时模块加载即 `raise RuntimeError`（提示 `legacy.routing_csr` 不在保留代码中） |
| `_SIM_CRITIC_GLOBAL` | 499 | 集中式 critic 开关 |
| `ddqn` / `alpha_dnn` | 555 / 559 | DDQN 双网络开关 / DNN 学习率 |
| `plotDeliver` | 564 | 送达路径绘图开关 |
| `winSize` / `markerSize` | 567 / 568 | 绘图滚动窗口 / 散点大小 |
| `ArriveReward` / `againPenalty` / `unavPenalty` | 579 / 583 / 584 | 送达奖励 / 回环惩罚 / 不可用方向惩罚 |
| `biggestDist` | 585 | 距离奖励归一化因子，初值 -1，在 `createGraph`（8655，前序片段）的 8691–8703 行更新 |
| `_SIM_POTENTIAL_SHAPING` / `distanceRew` | 589 / 590 | 势函数塑形开关 / 距离奖励版本选择（默认 4） |
| `MIN_EPSILON` / `LAMBDA` / `decayRate` | 598 / 599 / 600 | ε 下限与衰减参数（均可被 env 覆盖） |
| `stopLoss` / `nLosses` / `lThreshold` | 610 / 611 / 612 | 止损训练开关组 |
| `TrainThis` / `CurrentGTnumber` | 613 / 617 | 单场景训练开关 / 当前网关数 |
| `nnpath` / `nnpathTarget` | 625 / 626 | 预训练网络路径（env `SIM_NN_PATH`/`SIM_NN_TARGET`） |
| `outputPath` / `populationMap` | 653 / 663 | 结果输出目录 / 人口密度 tif 路径（`__main__` 块内定义） |
| `receivedDataBlocks` / `createdBlocks` | 673 / 674 | 全局已收/已建数据块列表 |
| `_SEED` | 680 | 随机种子（env `SIM_SEED`，默认 42；681–686 行播种 np/random/tf） |
| `upGSLRates` / `downGSLRates` / `interRates` / `intraRate` | 688–691 | 链路速率采样列表 |
| `REPLAY_TRACE` / `SIM_FAST_ENV` | 694 / 696 | 回放轨迹开关；`SIM_FAST=1` 时 `REPLAY_TRACE=False`（697–698） |
| `_SIM_GSL_KEEP_STABLE` | 746 | GSL 切换保留稳定链路开关 |
| `_SIM_PATH_CREDIT` | 753 | path-credit 开关（`_env_int`） |
| `_SIM_FAST_TRAIN` | 802 | 编译版训练步开关 |
| `_SIM_CHECKPOINT_FRACTIONS` | 823–833 | 按仿真时间分数存中间检查点的列表（env `SIM_CHECKPOINT_FRACTIONS`，逗号分隔，仅收 (0,1) 区间值） |
| 外部 import `assess_path_credit_effect` / `assess_temporal_effect` / `attempt_checkpoint_load` / `new_checkpoint_receipt` | 27–32 | 来自 `CODE/runtime_effect_receipt.py`（文件已确认存在） |

---

## 函数逐个说明

### Q 表与几何工具

#### `def createQTable(NGT)` — CODE/SimulationRL.py:10238
- 定位：CODE/SimulationRL.py:10238–10252
- 职责：创建并返回一个 6 维全零 numpy 数组作为 Q(s,a) 表：形状 `(3,3,3,3,NGT,4)`，前 4 维为上/下/右/左邻居离散状态（各 3 档），第 5 维为目的网关编号，第 6 维为 4 个动作 `('N','S','E','W')`（10246–10250）(FACT)。函数内 docstring 称「10 GTs 时 4050 values」（10250 行注释）(FACT：注释原文如此)。
- 输入/输出：入 `NGT`（网关数）；出 `np.zeros((3,3,3,3,NGT,4))`。
- 依赖关系：**调用方未确认——CODE/ 全库 grep `createQTable` 仅命中定义行本身**。`QLearning.__init__`(5683) 在 `qTable is None` 时用 `np.random.rand(satUp, satDown, satRight, satLeft, NGT, self.nActions)` 内联初始化（5703–5704），不经过本函数 (FACT)。(INFERENCE：本函数是 QLearning 表初始化的未接线替代/遗留实现。)

#### `def getSlantRange(satA, satB)` — CODE/SimulationRL.py:10261
- 定位：CODE/SimulationRL.py:10261–10265
- 职责：返回两卫星 ECEF 坐标 `(x,y,z)` 之差的 L2 范数，即斜距（米）(FACT)。
- 输入/输出：入两个带 `.x/.y/.z` 属性的卫星对象；出 float（`np.linalg.norm` 结果）。
- 依赖关系：调用 `np.linalg.norm`。被调方：`_set_distance_diag`(1200,1201)、`DDQNAgent.getNextHop`(6879,6894，MAPPO-BP 打分的 progress 项)、同文件 `getDistanceReward`(10309,10310)、`getDistanceRewardV2`(10322,10328–10337)、`getDistanceRewardV3`(10351,10355–10361)、`getDistanceRewardV4`(10368,10369)、`getDistanceRewardV5`(10379)、`getDistanceRewardPotential`(10392,10393) (FACT)。

### 奖励函数群

#### `def getQueueReward(queueTime, w1)` — CODE/SimulationRL.py:10269
- 定位：CODE/SimulationRL.py:10269–10292
- 职责：把排队时延（秒）映射为队列奖励，三个互斥分支 (FACT)：
  1. `_SIM_REWARD_LINEAR` 为真（env `SIM_REWARD_LINEAR`，350）：返回 `-_LINEAR_ALPHA * max(queueTime, 0.0)`（10285–10288）；
  2. `_SIM_M1_FIX` 为真（env `SIM_M1_FIX`，344）：返回 `w1 * math.exp(-_M1_BETA * max(queueTime, 0.0))`，β=200 s⁻¹（10289–10291）；
  3. 默认：返回 `w1*(1-10**queueTime)`（10292）。
- 关键状态/结构：只读全局开关 `_SIM_REWARD_LINEAR`、`_LINEAR_ALPHA`、`_SIM_M1_FIX`、`_M1_BETA`；docstring（10270–10284）记录原公式数值量级问题与 M1 修复的校准说明（FACT：docstring 原文声明）。
- 输入/输出：入 `queueTime`(秒)、`w1`(权重)；出 float 奖励。
- 依赖关系：被 `QLearning.makeAction`(5784) 与 `DDQNAgent.makeDeepAction`(7176,7270) 调用；两处均为 `if block.queueTime else 0` 的守卫调用 (FACT)。

#### `def getDistanceReward(satA, satB, destination, w2)` — CODE/SimulationRL.py:10296
- 定位：CODE/SimulationRL.py:10296–10311
- 职责：距离奖励 V1：`w2*((2*TSLa-TSLb)/TSLa - 1)`，其中 `TSLa=getSlantRange(satA,destination)`、`TSLb=getSlantRange(satB,destination)`，`balance=-1` 使结果以 0 为中心（10307–10311）(FACT)。
- 输入/输出：入当前卫星、下一跳卫星、目的卫星对象、权重 `w2`；出 float。
- 依赖关系：调 `getSlantRange`。被 `QLearning.makeAction`(5783，QLearning 的唯一距离奖励路径) 与 `DDQNAgent.makeDeepAction`(7249，`distanceRew == 1` 分支) 调用 (FACT)。

#### `def getDistanceRewardV2(sat, nextSat, satU, satD, satR, satL, destination, w2)` — CODE/SimulationRL.py:10314
- 定位：CODE/SimulationRL.py:10314–10342
- 职责：距离奖励 V2：`w2 * (SLr / SLav)`；`SLr` 为选 nextSat 带来的到 destination 斜距缩减量，`SLav` 为 4 个方向邻居中非 None 者到 `sat` 的平均斜距（10322–10340）；`SLav == 0` 或无邻居（count=0）时返回 0（10340–10342）(FACT)。
- 输入/输出：入当前/下一跳卫星、4 方向邻居（可 None）、目的卫星、`w2`；出 float。
- 依赖关系：调 `getSlantRange`。被 `DDQNAgent.makeDeepAction`(7253，`distanceRew == 2` 分支) 调用 (FACT)。

#### `def getDistanceRewardV3(sat, nextSat, satU, satD, satR, satL, destination, w2)` — CODE/SimulationRL.py:10345
- 定位：CODE/SimulationRL.py:10345–10363
- 职责：距离奖励 V3：`w2 * SLr / max(SLrs)`；`SLrs` 为各非 None 邻居分别能取得的斜距缩减量列表，取最大值归一（10351–10363）(FACT)。若 4 个邻居全为 None，`max([])` 将抛 `ValueError`（Python 内置语义，FACT）。
- 输入/输出：同 V2；出 float。
- 依赖关系：调 `getSlantRange`。被 `DDQNAgent.makeDeepAction`(7257，`distanceRew == 3` 分支) 调用 (FACT)。

#### `def getDistanceRewardV4(sat, nextSat, satDest, w2, w4)` — CODE/SimulationRL.py:10366
- 定位：CODE/SimulationRL.py:10366–10375
- 职责：距离奖励 V4：`w2*(SLr - TravelDistance/w4)/biggestDist`；`SLr` 为到 `satDest` 的斜距缩减，`TravelDistance` 为本跳实际飞行斜距，`biggestDist` 为全局归一化因子（585 定义初值 -1，`createGraph` 内 8691–8703 更新）（10367–10373）(FACT)。10370–10372 有一个 `if TravelDistance > biggestDist: pass` 空分支（原 print 已注释）(FACT)。10374–10375 有两行注释掉的替代返回式 (FACT)。
- 输入/输出：入当前/下一跳卫星、目的卫星、`w2`、`w4`；出 float。
- 依赖关系：调 `getSlantRange`；读写全局 `biggestDist`。被 `DDQNAgent.makeDeepAction`(7175, 7264，`distanceRew == 4` 且 `_SIM_POTENTIAL_SHAPING` 为假时) 调用 (FACT)。

#### `def getDistanceRewardV5(sat, nextSat, w2)` — CODE/SimulationRL.py:10378
- 定位：CODE/SimulationRL.py:10378–10380
- 职责：距离奖励 V5：`w2 * getSlantRange(sat, nextSat) / 1000000`，只与本跳飞行距离成正比，不含目的地项 (FACT)。
- 输入/输出：入当前/下一跳卫星、`w2`；出 float。
- 依赖关系：调 `getSlantRange`。被 `DDQNAgent.makeDeepAction`(7186, 7268，`distanceRew == 5` 分支) 调用 (FACT)。

#### `def getDistanceRewardPotential(prevSat, nextSat, satDest, w2, gamma=0.99)` — CODE/SimulationRL.py:10383
- 定位：CODE/SimulationRL.py:10383–10394
- 职责：势函数奖励塑形（docstring 引 Ng et al. 1999）：`F = w2*(γ*Φ(next) - Φ(prev))`，`Φ(s) = -getSlantRange(s, satDest)/d`，`d = max(float(biggestDist), 1.0)`（10390–10394）(FACT)。docstring 声明经 env `SIM_POTENTIAL_SHAPING=1` 启用（10388，开关定义于 589）(FACT：docstring 声明与开关定义行)。
- 输入/输出：入上一步/当前卫星、目的卫星、`w2`、`gamma`（默认 0.99）；出 float。
- 依赖关系：调 `getSlantRange`；读全局 `biggestDist`。被 `DDQNAgent.makeDeepAction`(7173, 7262，`distanceRew == 4` 且 `_SIM_POTENTIAL_SHAPING` 为真时) 调用 (FACT)。

### 保存/加载函数群

#### `def saveHyperparams(outputPath, inputParams, hyperparams)` — CODE/SimulationRL.py:10397
- 定位：CODE/SimulationRL.py:10397–10430
- 职责：把星座名、importQ、plotPath、Test length、alpha（QLearning 与全局 `alpha_dnn`）、gamma、epsilon 三件套、ArriveR、w1/w2/w4、again/unav 惩罚、坐标粒度、updateF、batchSize、bufferSize、hardUpdate、explore、ddqn、latBias/lonBias、diff、reducedState、online 等字段格式化为字符串列表，逐行写入 `outputPath + 'hyperparams.txt'`（10399–10430）(FACT)。
- 输入/输出：入输出目录、inputParams（pandas DataFrame，取 `['Constellation'][0]`、`['Test length'][0]`）、hyperparams 对象；出写文件，无返回。
- 依赖关系：读全局 `alpha_dnn`(559)。被 `initialize(...)` 内 8075 行调用（`saveHyperparams(earth.outputPath, inputParams, hyperparams)`）(FACT)。

#### `def saveQTables(outputPath, earth)` — CODE/SimulationRL.py:10433
- 定位：CODE/SimulationRL.py:10433–10444
- 职责：在 `outputPath + 'qTablesExport_{len(earth.gateways)}GTs/'` 建目录，遍历 `earth.LEO` 各轨道面各卫星，把 `sat.QLearning.qTable` 用 `np.save` 存为 `{sat.ID}.npy`（10436–10444）(FACT)。
- 输入/输出：入输出目录、Earth 对象；出每卫星一个 .npy 文件。
- 依赖关系：被 `RunSimulation`(12481，`pathing == 'Q-Learning'` 时) 与 `save_on_interrupt`(11377) 调用 (FACT)。

#### `def saveDeepNetworks(outputPath, earth)` — CODE/SimulationRL.py:10447
- 定位：CODE/SimulationRL.py:10447–10472
- 职责：保存 DDQN 网络权重 (FACT)：
  - 非 `onlinePhase`：`earth.DDQNA.qNetwork.save(outputPath+'qNetwork_{N}GTs.h5')`；若全局 `ddqn`(555) 为真再存 `qTarget_...h5`（10450–10453）。随后 `try: import temporal_encoder as _te_save; _te_save.save(outputPath)`，成功打印「gru weights saved」，任何异常打印 `[temporal] save skipped`（10456–10461；注释说明 GRU 编码器权重与 qNetwork 同目录以便 eval 部署）。若 `earth.DDQNA.routing_mode == "ddqn_csr"`：`from legacy.routing_csr import save_csr_w` 并调用 `_save_w(outputPath, len(earth.gateways), earth.DDQNA.csr_w)`（10464–10466）。
  - `onlinePhase`：遍历逐卫星存 `{sat.ID}qNetwork_{N}GTs.h5`（及 ddqn 时 qTarget）（10467–10472）。
- 关键状态/结构：(FACT) `CODE/legacy/` 目录在当前工作区不存在（Glob `**/routing_csr.py` 与 `**/legacy/__init__.py` 均无匹配）；文件头 474–479 行在 `SIM_CSR_MODE=csr` 时模块加载即 `raise RuntimeError(... legacy.routing_csr, which is not present in retained CODE ...)`，因此 10464–10466 的 csr 分支在当前工作区不可达（INFERENCE：「不可达」是由前两条 FACT 推出的结论）。
- 输入/输出：入输出目录（函数内 `os.makedirs(outputPath, exist_ok=True)`）、Earth 对象；出 .h5/npz 文件。
- 依赖关系：依赖外部模块 `CODE/temporal_encoder.py`（已确认存在）。被 `RunSimulation`(12483) 与 `save_on_interrupt`(11370) 调用 (FACT)。

#### `def save_replay_buffer(outputPath, GTnumber, buffer)` — CODE/SimulationRL.py:10475
- 定位：CODE/SimulationRL.py:10475–10489
- 职责：把 DDQN 经验回放 deque 拆成 `states(float32)/actions(int32)/rewards(float32)/next_states(float32)/dones(bool)` 五个数组，`np.savez_compressed` 到 `outputPath/NNs/replay_buffer_{GTnumber}GTs.npz`（10477–10488）；buffer 为空时打印提示并直接 return（10479–10481）(FACT)。
- 输入/输出：入输出目录、网关数、buffer（元素为 5 元组）；出 .npz 文件。
- 依赖关系：被 `save_on_interrupt`(11414) 调用 (FACT)。

#### `def load_replay_buffer_into(earth, path)` — CODE/SimulationRL.py:10492
- 定位：CODE/SimulationRL.py:10492–10506
- 职责：从上述 .npz 读回五数组，逐条调用 `earth.DDQNA.experienceReplay.store(...)` 重建回放缓冲，返回加载条数；文件不存在时打印提示并返回 0（10494–10496）(FACT)。
- 输入/输出：入 Earth 对象、npz 路径；出 int 条数。
- 依赖关系：被 `RunSimulation`(12119) 在 env `SIM_REPLAY_PATH` 非空且 `pathing == "Deep Q-Learning"` 且非 `onlinePhase` 时调用 (FACT)。

#### `def _save_pc_replay(pc_replay, path)` — CODE/SimulationRL.py:10509
- 定位：CODE/SimulationRL.py:10509–10572
- 职责：把 PathTrajectoryReplay（路径信用轨迹回放）序列化为 .npz (FACT)。内部 `_flatten(bucket, terminal_label)`（10523–10543）把 delivered/lost 两个 deque 摊平成 `(n, max_hops, state_dim)` 零填充的 states float32 数组、`(n, max_hops)` 的 actions int32 / mc_returns float32 数组和 lengths int32 数组；state_dim 从首条轨迹首跳的 `state.shape[-1]` 推断（10530）。另存 `max_hops`、`gamma`、`baseline_delivered`、`baseline_lost`（Welford 基线，10548–10553）。`np.savez_compressed` 落盘并打印条数（10569–10572）。
- 输入/输出：入 pc_replay 对象（需有 `.max_hops/.gamma/.delivered/.lost/.baseline()`）、npz 路径；出 .npz 文件。
- 依赖关系：函数内 `from routing_path_credit import TERMINAL_DELIVERED, TERMINAL_LOST`（10517，`CODE/routing_path_credit.py` 已确认存在）。被 `save_on_interrupt`(11423) 调用 (FACT)。

#### `def _load_pc_replay_into(pc_replay, path)` — CODE/SimulationRL.py:10575
- 定位：CODE/SimulationRL.py:10575–10614
- 职责：上函数的逆操作：文件不存在则 `raise FileNotFoundError`（10578–10579）；恢复 Welford 基线 `pc_replay._mean[TERMINAL_*]`（10583–10586）；内部 `_repopulate(...)`（10588–10607）按 lengths 逐条重建轨迹 dict（`state/action/mc_return`，`reward` 固定填 0.0，注释说明训练只用 mc_return，10602），append 到 delivered/lost 对应 bucket；返回总轨迹数 (FACT)。
- 输入/输出：入 pc_replay 对象、npz 路径；出 int 轨迹数。
- 依赖关系：被 `RunSimulation`(12153) 经 `attempt_checkpoint_load(..., fail_closed=_SIM_FAIL_CLOSED)` 包装调用（env `SIM_PC_REPLAY_PATH` 非空时）(FACT)。

### 回执/审计函数群

#### `def _packet_count_meta(earth)` — CODE/SimulationRL.py:10617
- 定位：CODE/SimulationRL.py:10617–10627
- 职责：返回包计数字典 `{"created": len(createdBlocks), "received": len(receivedDataBlocks), "lost": lost_link_break, "lost_link_break": lost_link_break, "in_flight_at_sim_end": max(0, created-received-lost_link_break)}`，其中 `lost_link_break = int(getattr(earth, "lostBlocks", 0) or 0)`（10618–10627）(FACT)。`"lost"` 与 `"lost_link_break"` 恒为同值 (FACT)。
- 输入/输出：入 Earth 对象；出 dict。
- 依赖关系：读全局列表 `createdBlocks`(674)、`receivedDataBlocks`(673)。被 `save_on_interrupt`(11406) 与 `RunSimulation`(12303) 展开进 replay-trace meta (FACT)。

#### `def _trace_traffic_receipt(earth)` — CODE/SimulationRL.py:10630
- 定位：CODE/SimulationRL.py:10630–10682
- 职责：构造「不可变 trace 流量」的比特守恒终结台账（schema `leo-legacy-trace-receipt/v1`）(FACT)：
  - `earth.trace_traffic_enabled` 为假 → 返回 None（10632–10633）；
  - `earth.trace_traffic_manifest` 不是 dict → 返回 `valid=False` 且 errors 含「manifest is absent」（10634–10640）；
  - 否则从全局 `createdBlocks` 筛出带 `trace_packet_id` 的块，校验：packet id 无重复（10647–10648）、发出包数等于 manifest 的 `offered_packets`（10656–10657）、发出比特数等于 `offered_bits`（10658–10659）、比特守恒 `emitted == delivered + lost + in_system`（10660–10661，按 `trace_terminal_status` 0=delivered/1=lost/None=in_system 分类，10650–10655）；
  - 返回含 trace_sha256、projection（原样回传 manifest）、packets/bits 五元计数（offered/emitted/delivered/lost/in_system_at_stop）的 dict（10662–10682）。
- 输入/输出：入 Earth 对象；出 dict 或 None。
- 依赖关系：读全局 `createdBlocks`。被 `_run_audit_meta`(10833) 与 `RunSimulation`(12309) 调用 (FACT)。

#### `def _git_value(args)` — CODE/SimulationRL.py:10685
- 定位：CODE/SimulationRL.py:10685–10699
- 职责：以本文件所在目录为 cwd 执行 `git <args>`（`subprocess.run`，`capture_output=True, text=True, check=False, timeout=2`），returncode==0 时返回 `stdout.strip()`，任何异常或失败返回 `""` (FACT)。
- 输入/输出：入 git 参数列表；出 str（可为空串）。
- 依赖关系：被 `_run_audit_meta` 调用 3 次：`rev-parse HEAD`(11329)、`branch --show-current`(11330)、`status --porcelain`(11334) (FACT)。

#### `def _run_audit_meta(earth, natural_end)` — CODE/SimulationRL.py:10702
- 定位：CODE/SimulationRL.py:10702–11353（652 行，本片段最大函数）
- 职责：汇总一次运行的「声明值 vs 运行时实测值」审计元数据，产出 mismatches 清单与 `research_eligible` 判定，作为 replay-trace meta 的一部分 (FACT)。
- 关键状态/结构：内部子结构 `_effective_receipt`（schema `leo-effective-receipt/v1`，11149–11310），顶层返回 dict（11312–11353）。
- 关键流程（按行号分阶段，均 FACT）：
  1. **定位 agent 与图编码层**（10703–10718）：取 `earth.DDQNA`，为空则遍历 `earth.LEO` 各卫星找第一个带 `DDQNA` 者；再取 `qnet = ddqna.qNetwork`，尝试 `qnet.get_layer("graph_encoder")`。
  2. **参数计数工具**（10720–10728）：内部 `_count_params(obj, trainable=False)`，trainable 时累加 `trainable_variables` 元素数，否则 `obj.count_params()`，异常返回 None。
  3. **解析声明侧 env JSON**（10730–10748）：`SIM_SCENARIO_IDENTITY_JSON`、`SIM_INFORMATION_CONTRACT_JSON`、`SIM_EXECUTION_SEMANTICS_JSON`，解析失败一律置 None。
  4. **推导执行语义**（10749–10767）：`_effective_execution_semantics`：`kind` = learning（pathing ∈ {Deep Q-Learning, Q-Learning}）否则 non_learning；`run_phase` = evaluation/training/non_learning（看 `SIM_RL_EVAL` env）；`dormant_config_paths` 非学习时为 10749–10753 列出的 14 个配置路径；`optimizer_activity_expected` = 学习类且非 eval。
  5. **读运行时计数器**（10769–10781）：`_pc_train_successes`、`_critic_train_successes`、`_global_state_observations`、`_temporal_apply_successes`、`_stale_neighbor_reads/history_hits`、`_timed_state_reads/hits/misses`、`_graph_state_builds/nodes_seen/edges_seen/overflow_nodes`，全部 `getattr(earth, ..., 0)`。
  6. **推导信息契约 `_effective_info`**（10783–10825）：train/evaluation/deployment 三相位初始各含 `local_observation/local_queue/neighbor_link_state`；非学习 pathing 清空 train；`slant_range` 时清空 evaluation/deployment 并根据图上的 `_slant_range_marker`/`_slant_range_runtime`（读自 `earth.graph.graph`，无图时用空 `nx.Graph()`，10793–10802）判定 `_slant_proven`，为真则补 `full_topology/global_link_slant_range`；state mode ∈ {c2..c7} 追加 `k_hop_queue_state`；按 stale/timed/temporal/pc/global-state 计数器追加对应标签；`oracle_global_dijkstra` 在 evaluation/deployment 追加 `full_topology/global_queue_state`；10825 去重排序。
  7. **收集 requested vs effective 原始事实**（10827–10884）：推理后端（`SIM_INFER_BACKEND` 默认 keras、`earth._infer_backends_effective`）、流量模式（`SIM_REQUESTED_TRAFFIC_MODE`、`earth.traffic_od_meta["mode"]`）、OD 矩阵哈希（`_array_sha256`，35）、突发/昼夜流量计数与配置哈希、GSL 切换计数（`earth._gsl_handover_*`）、链路中断统计（`earth._link_outage*`）；10880–10883 把 `mlab`+`mlab_hourly` 视为匹配别名。
  8. **mismatch 检测**（10885–11147，内部 `_mismatch(field, requested, effective, reason)` 追加 dict）：依次检查——
     - `SIM_RUN_ID` 缺失（10895–10896）；`_SIM_FAIL_CLOSED` 为假（10897–10898）；
     - 信息契约声明≠推导（10899–10900）；slant_range 运行未被证明（10901–10907）；
     - 执行语义声明≠推导（10908–10914）；流量模式不符（10915–10916）；OD 矩阵不可用（10917–10918）；流量配置哈希不符（10919–10925）；
     - trace 模式：receipt 无效或 trace_sha256 与 `SIM_EXPECTED_TRAFFIC_TRACE_SHA256` 不符（10926–10940）；
     - 突发流量：calls<1 / effect_calls<1 / 配置哈希不符 / 逐事件检查 resolved_src/dst_indices 非空、active_calls≥1、effect_calls≥1（10941–10976）；
     - 昼夜流量 calls/effect_calls（10977–10980）；GSL handover 模式不符、mbb 模式但切换数<1（10981–10994）；
     - 链路中断：请求了但未初始化 / 配置哈希不符 / evaluations<1（10995–11016）；
     - DQL 时 `routing_mode != SIM_ROUTING_MODE`（11017–11018）；DQL 时推理后端集合与请求不符或为空（11019–11023）；
     - non_learning 语义下出现训练活动/初始化了学习 agent/收到学习检查点（11024–11036），并把 `training_active/q_agent_initialized/checkpoint_requested` 并入 `_effective_execution_semantics`（11037–11042）；
     - path-credit 效果评估：`assess_path_credit_effect(...)`（11043–11051，来自 `runtime_effect_receipt.py`，27–32 import）结果并入 mismatches；
     - 集中式 critic：请求了（`_SIM_CRITIC_GLOBAL`）但 `q_global` 缺失 / 全局状态观测<1 / 训练成功<1（11053–11059）；
     - fast train：请求了（`_SIM_FAST_TRAIN`）但 fast 步数<1 或 eager 步数>0（11060–11067）；
     - temporal：`import temporal_encoder` 取 `last_train_loss()/mode()`（11069–11074），`assess_temporal_effect(...)`（11076–11083）并入 mismatches；请求 temporal 但 apply 成功数<1（11084–11085）；
     - stale/timed 邻居状态：请求了但 history_hits<1 / hits<1（11086–11097）；
     - 图观测（c4–c7）：graph_encoder 缺失或参数量非正 / state_builds<1 / overflow_nodes>0（11098–11119）；
     - RAAC（c6–c7）：encoder 非 reliability_aware / aoi_gate 与请求不符 / 满足采样条件但 `_raac_rel_samples`<1（11120–11147）。
  9. **组装 `_effective_receipt`**（11149–11310）：`requested` 段（pathing、routing_mode、执行语义、流量/突发/昼夜/handover/链路中断请求、信息契约、path_credit、critic、temporal、fast_train、推理后端、graph_observation 配置含 state_mode/vis_k/update_interval/layers/max_nodes/raac 门）；`effective` 段（pathing、routing_mode、执行语义、流量实测含 config 与矩阵哈希、trace receipt、突发/昼夜/handover/链路中断实测计数、信息契约、slant_range 审计、path_credit 评估结果、critic/temporal/stale/timed 实测、graph_observation 实测含 RAAC 门的 decisions/samples/reliability mean/min/max、execution 段含 fast/eager 步数、target 同步数、推理后端与回退记录）；`mismatches`；`research_eligible = bool(natural_end) and not _mismatches`（11309）。
  10. **顶层返回**（11312–11353）：natural_end/interrupted、run_attempt_id（`SIM_RUN_ATTEMPT_ID`）、config 标签与哈希（`SIM_CFG_PATH_TAG`/`SIM_CONFIG_CANONICAL_SHA256`）、`SIM_LAUNCH_NONCE`、`SIM_AUTHORIZATION_SHA256`、实验/运行/arm/角色/方法族/种子等请求标识（`SIM_EXPERIMENT_ID` 等 9 个 env）、scenario_identity 与其哈希、git commit/branch/dirty（env 优先，缺省用 `_git_value`）、state/graph 配置快照、模型与图编码器参数计数（`_count_params`）、`_effective_receipt`、`sim_env`（全部以 `SIM_`/`TF_`/`OMP_` 开头及 `MPLBACKEND` 的环境变量快照，11348–11352）。
- 输入/输出：入 Earth 对象、`natural_end` bool；出审计 dict（不抛异常路径之外的返回值；内部多处容错）。
- 依赖关系：调用 `_trace_traffic_receipt`(10833)、`_git_value`(11329–11334)、`_array_sha256`(10841–10842，定义于 35)、`assess_path_credit_effect`/`assess_temporal_effect`（外部 `CODE/runtime_effect_receipt.py`）、`temporal_encoder` 模块；读全局 `pathing`(226)、`SIM_ROUTING_MODE`(231)、`_SIM_*` 开关系列与 `nx`(8)。被 `save_on_interrupt`(11407，`natural_end=False`) 与 `RunSimulation`(12304，`natural_end=True`) 调用。测试佐证：`CODE/tests/test_runtime_effect_receipt.py` 第 55 行 `import SimulationRL as sim`，264/272/383/404/426/447/477/546 行共 8 处直接调用 `sim._run_audit_meta(earth, natural_end=True)["effective_receipt"]` 做断言（该测试文件用 stub 的 tensorflow/keras，见 20–53 行注释与代码）(FACT)。

#### `def save_on_interrupt(earth1, outputPath, GTnumber, reason)` — CODE/SimulationRL.py:11356
- 定位：CODE/SimulationRL.py:11356–11487
- 职责：训练被中断（KeyboardInterrupt/SIGTERM）时的「安全子集」保存：docstring 声明跳过可能在残缺数据上崩溃的绘图/分析，只写模型、指标 CSV、replay trace、replay buffer 和带恢复提示的 interrupt_meta.json（11357–11359）(FACT：docstring 声明；下列步骤为代码事实)。
- 关键状态/结构：内部 `_try(label, fn)`（11362–11366）捕获一切异常仅打印 `[interrupt-save] <label> failed: ...`，使各步互相隔离 (FACT)。
- 关键流程（编号与代码注释一致，FACT）：
  1. **模型权重**（11368–11377）：`pathing == 'Deep Q-Learning'` → `saveDeepNetworks(outputPath+'/NNs/', earth1)`；若 `earth1.DDQNA.pc_mixer` 存在则 `pc_mixer.save_weights(outputPath/NNs/pc_mixer_{GT}GTs.npz)`。`pathing == 'Q-Learning'` → `saveQTables`。
  2. **指标 CSV/图**（11379–11393）：仅 DQL：`earth1.rewards` 非空 → `save_plot_rewards`；`earth1.loss` 非空 → `save_losses`；取 epsilon（非 onlinePhase 用 `earth1.DDQNA.epsilon`，否则用 `earth1.LEO[0].sats[0].DDQNA.epsilon`）非空 → `save_epsilons`；`earth1.trains` 非空 → `save_training_counts`。
  3. **replay trace**（11395–11410）：`flush_replay_trace(earth1, outputPath, meta={schema_version:'1.2', seed:_SEED, interrupted:True, interrupt_reason/sim_time, pathing, gt_number, **_packet_count_meta(earth1), **_run_audit_meta(earth1, natural_end=False), SIM_RL_EVAL, sim_train_used})`（`flush_replay_trace` 定义于 1259，前序片段）。
  4. **经验回放**（11412–11415）：DQL 且非 onlinePhase 且 DDQNA 存在 → `save_replay_buffer(...)`。
  4b. **pc_replay**（11417–11423）：DQL 且非 onlinePhase 且 `earth1.pc_replay` 与 `DDQNA.pc_mixer` 均存在 → `_save_pc_replay` 到 `NNs/pc_replay_{GT}GTs.npz`。
  4c. **blocks.npy**（11425–11448）：`receivedDataBlocks` 为空则打印并跳过（返回 False）；否则逐块包 `BlocksForPickle`（定义于 1771）并用 `_atomic_save_npy`（定义于 58）存 `outputPath/Congestion_Test/blocks_{GT}.npy`（allow_pickle=True）。
  4c（注释编号重复，FACT）. **experiment_bundle**（11450–11458）：`blocks_saved` 且非 `SIM_FAST_ENV` 时 `from experiment_bundle import postprocess_run_dir; postprocess_run_dir(outputPath, pathing=pathing)`（`CODE/experiment_bundle.py` 已确认存在）。
  5. **interrupt_meta.json**（11460–11487）：写 `outputPath/run_trace/interrupt_meta.json`，含 reason、interrupt_sim_time、wall_time、gt_number、pathing、n_steps（`ddqna.step`）、n_trains、replay_buffer_size、`resume_hint`（SIM_NN_PATH/SIM_NN_TARGET/SIM_REPLAY_PATH/SIM_PC_MIXER_PATH/SIM_PC_REPLAY_PATH 五个指向本次输出的路径）。
- 输入/输出：入 Earth、输出目录、网关数、中断原因 str；出上述文件，无返回（调用方随后 `sys.exit(130)`，见 12287）。
- 依赖关系：调 `saveDeepNetworks/saveQTables/save_plot_rewards/save_losses/save_epsilons/save_training_counts/flush_replay_trace/_packet_count_meta/_run_audit_meta/save_replay_buffer/_save_pc_replay/_atomic_save_npy`；读全局 `pathing/onlinePhase/_SEED/SIM_FAST_ENV`。被 `RunSimulation`(12285) 在 `earth1.interrupted` 为真时调用 (FACT)。

### 绘图函数群

#### `def plotLatenciesBars(percentages, outputPath)` — CODE/SimulationRL.py:11495
- 定位：CODE/SimulationRL.py:11495–11522。职责：画百分比堆叠条形图——每个网关数场景一根柱，Propagation/Queue/Transmission time 三段堆叠（颜色 #b5ffb9/#f9bc86/#a3acff），存 `outputPath + 'Percentages_{len(GTnumber)+1}_Gateways.png'`（11520，注意文件名取 GT 数 +1）(FACT)。输入：含 4 个键的 dict；输出：png 文件。**调用方未确认——唯一调用点 12511 行处于注释状态（`# plotLatenciesBars(percentages, outputPath)`），`RunSimulation` 12022–12027 与 12459–12477 中构造 percentages 的代码也整体注释** (FACT)。

#### `def plotQueues(queues, outputPath, GTnumber)` — CODE/SimulationRL.py:11525
- 定位：CODE/SimulationRL.py:11525–11536。职责：画队列长度累计直方图（`bins=max(queues)`, cumulative, density, step 型），存 `pngQueues/Queues_{N}_Gateways.png`，并把原始 queues 存 `csv/Queues_{N}_Gateways.csv` (FACT)。docstring 提到 CDF 与 PDF，但代码只画一幅 cumulative 直方图 (FACT)。输入：队列长度列表、输出目录、网关数；输出：png+csv。被 `RunSimulation`(12441，非 onlinePhase 时) 调用 (FACT)。

#### `def extract_block_index(block_id)` — CODE/SimulationRL.py:11539
- 定位：CODE/SimulationRL.py:11539–11540。职责：`int(block_id.split('_')[-1])`，取块 ID 最后一个下划线段的整数 (FACT)。输入：块 ID 字符串；输出：int。被 `plotSaveAllLatencies`(11853，`df['Block ID'].apply(...)`) 调用 (FACT)。

#### `def save_plot_rewards(outputPath, reward, GTnumber, window_size=200)` — CODE/SimulationRL.py:11543
- 定位：CODE/SimulationRL.py:11543–11581。职责：把 `[reward, time]` 对列表转成 DataFrame，计算滚动均值（window=200）与滚动 Top10%/Bottom10% 均值（`np.partition` 实现，11552–11553），画三条曲线存 `Rewards/rewards_{N}_gateways.png`，DataFrame 存 `csv/rewards_{N}_gateways.csv`，返回 DataFrame (FACT)。x 轴标签 "Time [ms]"（11564）但输入时间未做单位换算 (FACT)。被 `save_on_interrupt`(11382) 与 `RunSimulation`(12409) 调用 (FACT)。

#### `def save_epsilons(outputPath, eps, GTnumber)` — CODE/SimulationRL.py:11584
- 定位：CODE/SimulationRL.py:11584–11600。职责：画 epsilon-时间折线存 `epsilons/epsilon_{N}_gateways.png`，同数据存 `csv/epsilons_{N}_gateways.csv`，返回 DataFrame (FACT)。被 `save_on_interrupt`(11390) 与 `RunSimulation`(12416，仅 `Train` 为真时) 调用 (FACT)。

#### `def save_training_counts(outputPath, train_times, GTnumber)` — CODE/SimulationRL.py:11603
- 定位：CODE/SimulationRL.py:11603–11629。职责：把时间列表 ×1000 转 ms（11605），画累计训练次数折线存 `trainings/trainings_{N}_gateways.png`，存 `csv/trainings_{N}_gateways.csv`；末尾有注释掉的 `# return df`（11629），函数实际无返回 (FACT)。被 `save_on_interrupt`(11392) 与 `RunSimulation`(12417) 调用 (FACT)。

#### `def save_losses(outputPath, earth1, GTnumber)` — CODE/SimulationRL.py:11632
- 定位：CODE/SimulationRL.py:11632–11663。职责：从 `earth1.loss`（[loss,time] 对）画两张图——按时间（`loss_{N}_gatewaysTime.png`）与按步数（`loss_{N}_gatewaysSteps.png`），再从 `earth1.lossAv` 画平均 loss 图（`loss_{N}_gatewaysAverage.png`），均存 `loss/` 目录；loss 数据存 `csv/loss_{N}_gateways.csv` (FACT)。被 `save_on_interrupt`(11385) 与 `RunSimulation`(12427，仅 DQL) 调用 (FACT)。

#### `def plotSavePathLatencies(outputPath, GTnumber, pathBlocks)` — CODE/SimulationRL.py:11666
- 定位：CODE/SimulationRL.py:11666–11694。职责：取 `pathBlocks[0]` 的 (latency, arrival) 对，画两张红色散点图——x 轴分别为到达时刻（`pngLatencies/{N}_gatewaysTime.png`）与到达序号（`pngLatencies/{N}_gateways.png`），数据存 `csv/pathLatencies_{N}_gateways.csv` (FACT)。注释称「figure of latencies between two first gateways」（11667）(FACT：注释原文)。被 `RunSimulation`(12399) 调用 (FACT)。

#### `def plot_packet_latencies_and_uplink_downlink_throughput(data, outputPath, bins_num=30, save=False, plot_separately=True)` — CODE/SimulationRL.py:11697
- 定位：CODE/SimulationRL.py:11697–11774。职责：按 `(block.path[0][0], block.path[-1][0])` 把数据块按源-目的路径分组（11708–11712）；内部 `plot_path_data(blocks, src, dst)`（11715–11766）对每个分组：按 creationTime 排序，画到达时刻(ms) vs 端到端时延(ms) 散点（主轴），副轴用 `np.histogram` 在时间 bin 上统计创建/到达计数，乘 `BLOCK_SIZE`(318) 除以 bin 宽得上/下行吞吐折线——换算因子为 `/1e3` 且注释标注 Mbps（11739–11741）(FACT：代码与注释如此；同文件 `plot_throughput_cdf` 用 `/1e6`，11806–11808)。`save=True` 存 `Throughput/{src}_{dst}_path_latency_throughput.png`（或 combined），否则 `plt.show()`（11761–11765）。`plot_separately=True` 逐路径出图，False 合并一张 (FACT)。输入：数据块列表；输出：png 或屏幕显示。被 `RunSimulation`(12403，`save=True, plot_separately=plotAllThro`) 调用 (FACT)。

#### `def plot_throughput_cdf(data, outputPath, bins_num=100, save=False, plot_separately=True)` — CODE/SimulationRL.py:11777
- 定位：CODE/SimulationRL.py:11777–11842。职责：与上函数相同的分组与吞吐计算（但换算因子 `/1e6`，11806–11808），对上/下行吞吐序列排序后画经验 CDF（`np.arange(1,n+1)/n`），存 `Throughput/Throughput_CDF_{src}_to_{dst}.png` 或 `Throughput_CDF_All_Paths.png` (FACT)。被 `RunSimulation`(12406) 调用 (FACT)。

#### `def plotSaveAllLatencies(outputPath, GTnumber, allLatencies, epsDF=None, annotate_min_latency=True)` — CODE/SimulationRL.py:11845
- 定位：CODE/SimulationRL.py:11845–11937。职责 (FACT)：
  - 预处理：allLatencies → 9 列 DataFrame（Creation Time/Latency/Arrival Time/Source/Destination/Block ID/QueueTime/TxTime/PropTime），用 `extract_block_index` 加 Block Index 列并按 (Source,Destination,Block Index) 排序，存 `csv/allLatencies_{N}_gateways.csv`（11851–11855）；时间列 ×1000 转 ms（11858–11862）。
  - 按 `Path`（"src -> dst"）分组算滚动均值，窗口用全局 `winSize`(567)（11865–11866）。
  - 画 2×2 子图（figsize 18×18）：左列为 Arrival Time / Creation Time 的滚动均值折线（sns.lineplot），右列为原始时延散点（marker 大小用全局 `markerSize`(568)）（11872–11905）。
  - `annotate_min_latency` 且 x 为 Creation Time 时，对每条路径在滚动均值最小点加箭头注释（`math.isfinite` 守卫，异常打印错误继续，11882–11898）。
  - `epsDF` 非 None 时在左列加副轴画 epsilon 紫线并合并图例（11908–11918）。
  - `GTnumber > 4` 时隐藏所有图例（11924–11929，阈值 `GTnumber_Max = 4` 定义于 11847）。
  - 存 `pngAllLatencies/{N}_gateways_All_Latencies_subplots.png`（dpi=300），结尾 `sns.set()` 复原 seaborn 设置（11933–11937）。
- 输入/输出：入输出目录、网关数、时延记录列表、可选 epsilon DataFrame；出 png+csv。
- 依赖关系：调 `extract_block_index`；读全局 `winSize/markerSize`。被 `RunSimulation`(12423 带 epsDF、12434 不带) 调用 (FACT)。

#### `def plotRatesFigures()` — CODE/SimulationRL.py:11940
- 定位：CODE/SimulationRL.py:11940–11965。职责：对全局列表 `interRates`、`upGSLRates`、`downGSLRates`（688–690）各画一幅累计直方图（/1e9 转 Gbps，density），标题分别为 Inter plane ISL/Uplink/Downlink data rates，用 `plt.show()` 显示而非存盘 (FACT)。`intraRate`(691) 被放进 `values` 列表（11941）但没有任何绘图语句使用 `values` 或 `intraRate` (FACT)。被 `RunSimulation`(12290，`testType == "Rates"` 时) 调用 (FACT)。

#### `def plotCongestionMap(self, paths, outPath, GTnumber, plot_separately=True)` — CODE/SimulationRL.py:11968
- 定位：CODE/SimulationRL.py:11968–12015。职责：模块级函数但首参数命名为 `self`，期望传入 Earth 实例（FACT：11997/12011 行调用 `self.plotMap(...)`，即 `Earth.plotMap`(5343)；12445 行实际调用传 `earth1`）。流程 (FACT)：内部 `extract_gateways(path)`（11969–11974）按全局 `pathing` 取块的首末节点——Q-Learning/Deep Q-Learning 用 `path.QPath[0][0]/QPath[-1][0]`，否则用 `path.path[...]`；统计每条 (源,目的) 网关对的块数，过滤出计数 >100 的路由（11989，行内注释 `# REVIEW Packet threshold for path visualization 500`）；先画全部过滤后路由的合图 `all_routes_CongestionMap_{N}GTs.png`，`plotMap` 返回 -1 时打印不可用；`plot_separately=True` 再逐路由画 `CongestionMap_{src}_to_{dst}_{N}GTs.png`。输入：Earth 实例、块数组、输出目录、网关数；输出：png 文件。被 `RunSimulation`(12444–12446) 调用 (FACT)。

### 主入口

#### `def RunSimulation(GTs, inputPath, outputPath, populationData, radioKM)` — CODE/SimulationRL.py:12019
- 定位：CODE/SimulationRL.py:12019–12521（503 行）
- 职责：整个仿真的主驱动：读输入参数，对 `GTs` 列表里每个网关数各建一次 simpy 环境跑仿真，负责热启动恢复、中断保护、运行后统计/绘图/回执落盘与多场景间状态清理 (FACT)。
- 关键状态/结构：声明并改写的全局变量：`CurrentGTnumber/Train/TrainThis/explore/importQVals/nnpath`（12053–12058）、`nnpathTarget`（ddqn 时，12061–12062）、`diff_lastHop`(12063)、`CKA_Values`（FL_Test 时，12059–12060）。
- 关键流程（按行号分阶段，均 FACT）：
  1. **参数读取**（12020–12049）：`pd.read_csv(_resolve_input_rl_path(default=inputPath+"inputRL.csv"))`；取 `Test type`、`Test length`；env `SIM_TIME_LIMIT` 可覆盖 testLength（非法值打印并回退 CSV 值）；`simulationTimelimit = testLength`（testType ≠ "Rates"）或 `movementTime*testLength + 10`（Rates）。
  2. **GT 循环开头与 eval 模式**（12051–12074）：对 `GTnumber in GTs`；先存 `_saved_train_flags = (Train, explore, importQVals, diff_lastHop)`；若 env `SIM_RL_EVAL` ∈ {1,true,yes} 且 DQL：强制 `Train=False, explore=False, importQVals=True`，`diff_lastHop` 由 env `SIM_DIFF_LAST_HOP` 决定（默认 False，注释说明与预训练 3GT 模型 28 维输入兼容）；`TrainThis = Train`。
  3. **跨场景权重接力**（12076–12082）：首个 GT 用文件头 `nnpath`(625)；后续 GT 改指 `outputPath/NNs/qNetwork_{GTnumber-1}GTs.h5`（及 ddqn 时 qTarget）。
  4. **建环境**（12087–12111）：`simpy.Environment()`；`mixLocs` 为真时对前 `max(GTs)` 个网关位置洗牌；`inputParams['Locations']` 截断到 GTnumber；打印一批全局配置；`earth1, _, _, _ = initialize(env, populationData, inputPath+'Gateways.csv', radioKM, inputParams, movementTime, locations, outputPath, matching=matching)`（`initialize` 定义于 7885）；在 earth1 上记录 `outputPath/sim_train_used/sim_explore_used/sim_import_used/sim_rl_eval_env`。
  5. **热启动恢复**（12113–12163）：env `SIM_REPLAY_PATH` 且 DQL 且非 onlinePhase → `load_replay_buffer_into`；`earth1._pc_checkpoint_loads = {"mixer": new_checkpoint_receipt(SIM_PC_MIXER_PATH), "replay": new_checkpoint_receipt(SIM_PC_REPLAY_PATH)}`；两路径非空时分别经 `attempt_checkpoint_load(..., label=..., fail_closed=_SIM_FAIL_CLOSED)` 加载 pc_mixer 权重/`_load_pc_replay_into`，组件缺失时走 `_missing_pc_component` 抛 RuntimeError（12131–12132），加载结果打印。
  6. **初始 ISL 地图**（12165–12175）：`saveISLs` 为真时 `earth1.plotMap(...)` 存 `outputPath/ISL_maps/`；否则打印跳过（注释说明 `SIM_FAST=1` 会置 saveISLs=False）。
  7. **注册仿真进程**（12177–12196）：`env.process(simProgress(...))`；`REPLAY_TRACE` 为真时注册 `_queue_snapshot_proc`：每 0.02 s 仿真时间对全部卫星记录 `(t, sat.ID, qU, qD, qR, qL, gsl_q)` 到 `earth1.queue_snapshots`（单卫星异常静默吞掉，12193–12194）。
  8. **中断保护**（12198–12210）：安装 SIGTERM 处理器 `_handle_sigterm`，把 SIGTERM 转成 `KeyboardInterrupt`；在 earth1 上置 `interrupted/interrupt_sim_time/interrupt_reason`。
  9. **分数检查点**（12212–12230）：`_SIM_CHECKPOINT_FRACTIONS` 非空且 TrainThis 且 DDQNA 存在时，对每个分数 `_f` 注册 `_ckpt_proc`，在 `simulationTimelimit*_f` 时刻存 `NNs/qNetwork_{N}GTs_frac{NNN}.h5`（及 ddqn 时 qTarget），异常仅打印。
  10. **跑仿真**（12232–12245）：`env.run(simulationTimelimit)`；捕获 KeyboardInterrupt → 标记 earth1.interrupted、记录 sim_time 与原因；finally 恢复原 SIGTERM 处理器。
  11. **收敛摘要打印**（12247–12278）：若 `earth1.loss` 非空：打印总步数、train 调用数、按公式 `minEps + (maxEps-minEps)*exp(-LAMBDA*step/(decayRate*GT²))` 估算的最终 ε、loss 首 20/末 20 均值与趋势（↓/↑/→），并估算 ε<0.5 所需步数与仿真秒数（12268–12277）。
  12. **中断分支**（12280–12287）：`earth1.interrupted` 为真 → `save_on_interrupt(...)` 后 `sys.exit(130)`（注释说明 130 是 SIGINT 的 shell 约定）。
  13. **正常结束统计与回执**（12289–12338）：testType == "Rates" → `plotRatesFigures()`；否则 `results, allLatencies, pathBlocks, blocks = getBlockTransmissionStats(timeToSim, locations, constellation, earth1)`（1324），打印 `earth1.lostBlocks`，然后 `flush_replay_trace(earth1, outputPath, meta={...})`——meta 含 schema 1.2、seed、pathing、gt_number、`_packet_count_meta`、`_run_audit_meta(natural_end=True)`、仿真时长、流量模式/配置/OD 矩阵（`.tolist()`）、trace 回执、`SIM_RL_EVAL`、训练/探索/导入标志、`SIM_ROUTING_MODE`、quantile 尾部分支信息（routing_mode == "ddqn_cvar" 时 `__import__("legacy.routing_tailguard", ...)` 取 `tailguard_fallback_note`，12321–12328；注意 `legacy` 包在当前工作区不存在，见 saveDeepNetworks 条目）、`ddqn_mcp_hash` 时的 4 个 MCP env 快照（12329–12336）。
  14. **trace 数组落盘**（12339–12388）：`REPLAY_TRACE` 时把 `earth1.decision_trace`（12 列，列名 json 同步写出）与 `earth1.queue_snapshots`（7 列）各存 .npy + columns.json 到 `outputPath/run_trace/`。
  15. **绘图与 bundle**（12390–12457，仅非 `SIM_FAST_ENV`）：`experiment_bundle.postprocess_run_dir(outputPath, pathing=pathing)`（异常打印跳过）；`plotSavePathLatencies`；两个吞吐图（`plot_separately=plotAllThro`）；DQL/QL 时 `save_plot_rewards`、取 epsilon（onlinePhase 取首卫星）、`Train` 时 `save_epsilons`+`save_training_counts` 得 epsDF、`plotSaveAllLatencies(..., epsDF)`；DQL 专属 `save_losses`，`FL_Test and const_moved` 时 `plot_cka_over_time`（1679）；非 DQL 时 `plotSaveAllLatencies`（无 epsDF）；`pathBlocks[1]` 非空时 `plotShortestPath`（8968）否则打印跳过；非 onlinePhase 时 `plotQueues`；`plotCongestionMap(earth1, np.asarray(blocks), outputPath+'/Congestion_Test/', GTnumber, plot_separately=plotAllCon)`；`pathBlocks[1]` 非空时打印 Path 与 `findBottleneck`（8087）结果。`SIM_FAST` 分支只打印网关数（12456–12457）。
  16. **学习成果保存**（12479–12483）：QL → `saveQTables`；DQL → `saveDeepNetworks(outputPath+'/NNs/', earth1)`。
  17. **清理**（12485–12499）：清空全局列表 `receivedDataBlocks/createdBlocks/pathBlocks/allLatencies/upGSLRates/downGSLRates/interRates/intraRate`；`del results/earth1/env/_`；恢复 `_saved_train_flags`；`gc.collect()`。控制流事实链 (FACT)：①`results/allLatencies/pathBlocks` 三个名字仅在 12292 行由 `getBlockTransmissionStats(...)` 的解包绑定（模块级无定义，全文件 grep `^(pathBlocks|allLatencies|results)\s*=` 无匹配；`allLatencies`/`pathBlocks` 仅在 `getBlockTransmissionStats` 内部 1336–1337 作为局部变量创建）；②testType=="Rates" 分支（12289–12290）跳过该绑定；③12488–12494 的 `pathBlocks.clear()`/`allLatencies.clear()`/`del results` 无条件执行且外层无 try 包裹。由 Python 局部变量语义，Rates 路径执行到 12488 时会抛 `UnboundLocalError`（由 ①②③ 直接推出，FACT）。
  18. **计时打印**（12501–12520）：多 GT 时打印每档耗时；循环结束后打印总耗时。
- 输入/输出：入网关数列表、输入目录、输出目录、人口数据路径、网关覆盖半径；出全部结果文件（无返回）。
- 依赖关系：调用 `_resolve_input_rl_path`(634)、`initialize`(7885)、`simProgress`(1416)、`load_replay_buffer_into`/`_load_pc_replay_into`/`new_checkpoint_receipt`/`attempt_checkpoint_load`（外部 runtime_effect_receipt）、`getQueues`(9050)、`save_on_interrupt`、`getBlockTransmissionStats`(1324)、`flush_replay_trace`(1259)、`_packet_count_meta`、`_run_audit_meta`、`_trace_traffic_receipt`、`plotRatesFigures`、`plotSavePathLatencies`、`plot_packet_latencies_and_uplink_downlink_throughput`、`plot_throughput_cdf`、`save_plot_rewards`、`save_epsilons`、`save_training_counts`、`save_losses`、`plotSaveAllLatencies`、`plot_cka_over_time`(1679)、`plotShortestPath`(8968)、`plotQueues`、`plotCongestionMap`、`findBottleneck`(8087)、`saveQTables`、`saveDeepNetworks`；读写全局 `pathing/onlinePhase/ddqn/Train/explore/importQVals/diff_lastHop/nnpath/nnpathTarget/movementTime/ndeltas/MIN_EPSILON/ArriveReward/stopLoss/nLosses/lThreshold/matching/mixLocs/FL_Test/const_moved/REPLAY_TRACE/SIM_FAST_ENV/saveISLs/plotAllThro/plotAllCon/LAMBDA/decayRate/SIM_ROUTING_MODE/_SIM_FAIL_CLOSED/_SIM_CHECKPOINT_FRACTIONS` 与全局块列表。被调方：仅 `if __name__ == '__main__':` 块（12549）；CODE/ 下无其他文件调用 `RunSimulation`（跨文件 `import SimulationRL` 仅 5 处：tests/test_runtime_effect_receipt.py:55、tests/test_state_vis_k.py:21、tests/test_raac_aoi_gate.py:49、tests/test_raac_tensorflow_contract.py:34、tools/benchmark_graph_execution.py:33，均不调用 RunSimulation）(FACT)。
# 旧平台流量/需求生成模块组说明书片段（o1-traffic）

范围：`CODE/traffic_od.py`、`CODE/traffic_burst.py`、`CODE/traffic_diurnal.py`、`CODE/traffic_mlab.py`。行数均为 `wc -l` 实测。每个符号的职责陈述标注 (FACT)=代码可核验 / (INFERENCE)=从命名、注释或上下文推测。

---

### 文件 `CODE/traffic_od.py`（实测 442 行）

模块级说明：

- 模块 docstring（行 1-20）：声明四种 OD 权重模式 `uniform`/`h2`/`gravity`/`gravity_corridors`、默认行为（`SIM_TRAFFIC_CONFIG` 未设置时为 uniform）、h2 与 gravity_corridors 的 fail-loud 约定、配置 JSON 字段，以及「行 s 对 d≠s 求和为 1」的输出约定 (FACT，与下文各函数实现一致)。注意：docstring 行 11 的模式清单不含 `mlab`，但调度器 `build_od_matrix_for_gateways` 行 401-438 实现了 `mlab` 分支——docstring 未覆盖全部已实现模式 (FACT)。
- imports（行 21-28）：`json`、`math`、`os`、`typing`、`numpy`；无 pandas。
- 全局常量：无。
- env 变量读取点：`load_traffic_config_from_env` 内行 336 读 `SIM_TRAFFIC_UNIFORM`、行 338 读 `SIM_TRAFFIC_CONFIG`。模块内无其他 env 读取 (FACT)。
- 模块被谁调用：`CODE/SimulationRL.py:20-24` 模块级导入 `build_od_matrix_for_gateways`、`load_traffic_config_from_env`、`traffic_mode_needs_gateway_physical`；`CODE/traffic_mlab.py:46-50` 模块级导入 `build_od_weights_uniform`、`haversine_km`、`_row_normalize_od`。测试侧：`CODE/tests/test_traffic_od_fail_loud.py:16-20`、`CODE/tests/test_traffic_mlab.py:32`、`CODE/tests/validate_burst_rates.py:24`。

#### `def _match_name(short, gateway_name)` — CODE/traffic_od.py:31

定位行 31；职责 (FACT)：名称匹配谓词——`short` 去空白后若是 `gateway_name` 的子串，或等于 `gateway_name` 逗号分隔的首段（如 "Malaga" 对 "Malaga, Spain"），返回 True；空 `short` 返回 False（行 32-39）。输入：两个字符串；输出：bool。被 `_indices_for_subset`（行 45）与 `_resolve_subset_indices`（行 61）调用。

#### `def _indices_for_subset(names, gateway_names)` — CODE/traffic_od.py:42

定位行 42；职责 (FACT)：返回 `gateway_names` 中所有被 `names` 里任一名字 `_match_name` 命中的网关下标列表（行 43-47）。输入：名字序列 + 网关名列表；输出：`List[int]`。仅被 `_resolve_subset_indices`（行 67）调用。

#### `def _resolve_subset_indices(names, gateway_names, *, label)` — CODE/traffic_od.py:50

- 定位：CODE/traffic_od.py:50
- 职责 (FACT)：把请求的名字集合解析成网关下标，是 h2 / gravity_corridors 的 fail-loud 闸门：names 为空时 `raise ValueError("{label}: sources/dests list is empty; ...")`（行 57-60）；任一名字无法匹配任何已配置网关时 `raise ValueError("... refusing silent uniform/gravity fallback")`，报错文本含 missing 名字与完整网关名清单（行 61-66）。
- 关键流程：空名单检查 → 逐个名字匹配性检查 → 委托 `_indices_for_subset`（行 67）。
- 输入/输出：名字序列 + 网关名列表 + 错误标签；输出 `List[int]`；异常路径为 `ValueError`。
- 依赖关系：调用 `_match_name`、`_indices_for_subset`；被 `build_od_weights_h2`（行 141-142）、`_corridor_boost_matrix`（行 248-249）调用。行为佐证：`CODE/tests/test_traffic_od_fail_loud.py`（文件级，import 见行 16-20）。

#### `def traffic_mode_needs_gateway_physical(cfg)` — CODE/traffic_od.py:70

定位行 70；职责 (FACT)：判断 OD 构建是否必须推迟到 `linkCells2GTs` 之后（需要网关经纬度/人口质量）；`mode ∈ {gravity, gravity_corridors, mlab}` 返回 True，其余（含缺省 uniform）返回 False（行 74-75）。输入：配置 dict；输出：bool。被 `CODE/SimulationRL.py:3559` 调用以决定 deferred 构建分支；测试引用 `CODE/tests/test_traffic_mlab.py:32`。

#### `def haversine_km(lat1, lon1, lat2, lon2)` — CODE/traffic_od.py:78

定位行 78；职责 (FACT)：haversine 大圆距离，地球半径常量 6371.0 km（行 80），对 `asin` 参数做 [0,1] 截断（行 86）；docstring 称其为 "WGS84 mean Earth radius"（注释声明，代码中只有 6371.0 这个数值可核验）。输入：两点经纬度（度）；输出：距离 km（float）。被 `build_od_weights_gravity`（行 224）调用；被 `CODE/traffic_mlab.py:48` 导入供 `_nearest_gateway_index`（traffic_mlab.py:115）使用；测试引用 `CODE/tests/validate_burst_rates.py:24`。

#### `def _row_normalize_od(w)` — CODE/traffic_od.py:89

定位行 89；职责 (FACT)：OD 矩阵归一化——负值截 0（行 91）、对角线置 0（行 92）、每行除以行和使行和为 1；行和为 0 的「孤立行」回退为该行的均匀分布 `1/(n-1)`（d≠s，行 97-100）。输入：(n,n) ndarray；输出：(n,n) 行随机矩阵、对角线为 0。被本文件行 228、231、254、324 调用；被 `CODE/traffic_mlab.py:49` 导入并在其行 194、198、312、319 使用。

#### `def build_od_weights_uniform(n)` — CODE/traffic_od.py:104

定位行 104；职责 (FACT)：构造 n×n 均匀 OD 矩阵，非对角元素均为 `1/(n-1)`，对角为 0；`n<=1` 时返回全零矩阵（行 106-107）。输入：网关数 n；输出：(n,n) float64 矩阵。被本文件行 125、158、169、202、230、358 调用；被 `CODE/traffic_mlab.py:47` 导入（其行 197、256、318 使用）；测试引用 `CODE/tests/test_traffic_od_fail_loud.py:18`。

#### `def build_od_weights_h2(gateway_names, sources_hot, dests_hot, p, g, weight_floor=1e-15)` — CODE/traffic_od.py:116

- 定位：CODE/traffic_od.py:116
- 职责 (FACT)：构造「热点走廊」OD 矩阵：以均匀矩阵为底，S×D 集合（热点源×热点宿）的元素乘以增益 g，再按 `(1-p)*uniform + p*boosted` 凸混合，可选 weight_floor 下限后再行归一化。
- 关键流程/结构：`n<=1` 直接 `raise ValueError("h2 requires at least two configured gateways; refusing degenerate uniform fallback")`（行 135-136，fail-loud）；p 截断到 [0,1]、g 下限 1.0（行 138-139）；S/D 下标经 `_resolve_subset_indices` 解析，空名单或未匹配名字抛 ValueError（行 141-142，fail-loud 路径）；boost 矩阵行归一化（行 154-156）；凸混合（行 159）；`weight_floor>0` 时对非对角元素施加下限并重归一化，若结果与未加下限的混合矩阵有差异则 `meta["floor_applied"]=True`（行 161-171）。
- 输入/输出：网关名列表 + 热点源/宿名 + 标量 p、g、weight_floor；输出 `(w_out, meta)`，`w_out` 为 (n,n) 行随机矩阵、对角 0；meta 含 mode/p/g/sources_hot/dests_hot/weight_floor/floor_applied/row_sums/gateway_names（行 126-134、173-174）。
- 依赖关系：调用 `build_od_weights_uniform`、`_resolve_subset_indices`；被 `build_od_matrix_for_gateways`（行 368）调用。

#### `def build_od_weights_gravity(gateway_names, lat_deg, lon_deg, mass, *, alpha=2.0, d_floor_km=100.0, blend_uniform=0.0)` — CODE/traffic_od.py:178

- 定位：CODE/traffic_od.py:178
- 职责 (FACT)：引力模型 OD 权重：`w_ij ∝ m_i * m_j / max(d_ij, d_floor_km)^alpha`，行归一化；可选与均匀矩阵凸混合 (FACT，docstring 行 189 与实现行 219-231 一致)。
- 关键流程/结构：`n<=1` 时不报错，返回均匀（全零）矩阵并在 meta 写 `note="n<=1, uniform degenerate"`（行 200-202）；lat/lon/mass 长度与 n 不一致时 `raise ValueError`（行 204-208，fail-loud）；mass 元素下限 1e-12（行 210）；alpha 下限 0.1、d_floor_km 下限 1e-3、blend_uniform 截断 [0,1]（行 215-217）；双重循环用 `haversine_km` 填 raw 矩阵（行 219-226）；`_row_normalize_od` 归一化（行 228）；`blend_uniform>0` 时与均匀矩阵混合后再次归一化（行 229-231）。
- 输入/输出：网关名 + 逐网关纬度/经度/质量序列（与 gateway_names 对齐）；输出 `(w_g, meta)`，`w_g` 为 (n,n) 行随机矩阵、对角 0；meta 含 mode/alpha/d_floor_km/blend_uniform/mass_min/mass_max/mass_sum/row_sums 等（行 193-199、211-213、233）。
- 依赖关系：调用 `haversine_km`、`_row_normalize_od`、`build_od_weights_uniform`；被 `build_od_weights_gravity_corridors`（行 277）、`build_od_matrix_for_gateways`（行 377）调用；测试引用 `CODE/tests/validate_burst_rates.py:24`。

#### `def _corridor_boost_matrix(w_base, gateway_names, sources, dests, g)` — CODE/traffic_od.py:237

定位行 237；职责 (FACT)：复制 `w_base`，把 S×D 内非对角元素乘以 g（g 下限 1.0，行 247），再 `_row_normalize_od`（行 250-254）；S/D 经 `_resolve_subset_indices` 解析，空名单或未匹配名字抛 ValueError（fail-loud，行 248-249）。输入：基础矩阵 + 网关名 + 走廊源/宿名 + 增益 g；输出：(n,n) 行随机矩阵。仅被 `build_od_weights_gravity_corridors`（行 312）调用。

#### `def build_od_weights_gravity_corridors(gateway_names, lat_deg, lon_deg, mass, cfg)` — CODE/traffic_od.py:257

- 定位：CODE/traffic_od.py:257
- 职责 (FACT)：gravity 基底 + 多走廊叠加：先建引力矩阵 `w_base`，对 cfg 中每条走廊生成增益副本，按走廊 `weight` 加权平均为 `w_mix`，最后 `(1-p_corridor)*w_base + p_corridor*w_mix` 并归一化（实现行 277-324，docstring 行 264-266 描述一致）。
- 关键流程/结构：`corridors` 为空时 `raise ValueError("mode=gravity_corridors requires non-empty corridors; use mode=gravity for pure gravity")`（行 271-275，fail-loud）；`n<=1` 时 `raise ValueError("... refusing pure gravity fallback")`（行 300-301，fail-loud）；走廊条目非 dict 时 `raise ValueError`（行 306-307）；每条走廊取 `sources`（或 `sources_hot`）、`dests`（或 `dests_hot`）、`g`（默认 1.0）、`weight`（默认 1.0），经 `_corridor_boost_matrix` 生成矩阵——走廊内空名单/未匹配名字同样抛 ValueError（行 308-314）；走廊权重和 `wsum<=0` 时取第一条走廊矩阵为 w_mix（行 316-318），否则按权重占比加权（行 319-322）；最终混合并归一化（行 324）。
- 输入/输出：网关名 + 经纬度/质量 + cfg dict（读 alpha/d_floor_km/blend_uniform/p_corridor/corridors，行 267-271）；输出 `(w_out, meta)`，`w_out` 为 (n,n) 行随机矩阵、对角 0；meta 含 mode/alpha/d_floor_km/blend_uniform/p_corridor/corridors/mass_*/row_sums 等（行 286-297、325）。
- 依赖关系：调用 `build_od_weights_gravity`、`_corridor_boost_matrix`、`_row_normalize_od`；被 `build_od_matrix_for_gateways`（行 393）调用。

#### `def load_traffic_config_from_env()` — CODE/traffic_od.py:329

- 定位：CODE/traffic_od.py:329
- 职责 (FACT)：按优先级加载 OD 配置——(1) `SIM_TRAFFIC_UNIFORM ∈ {1,true,yes}`（小写化后比较，行 336）→ `({"mode":"uniform"}, None)`；(2) `SIM_TRAFFIC_CONFIG` 非空（行 338）→ 转绝对路径并 `json.load` 该文件（行 340-343）；(3) 否则 `({"mode":"uniform"}, None)`（行 344）。
- 输入/输出：无参数（读环境变量）；输出 `(cfg dict, path 或 None)`。注意：文件不存在或 JSON 解析失败时本函数不捕获异常，`open`/`json.load` 的异常直接上抛（行 341-342）——模块级不兜底；兜底层在调用方 `CODE/SimulationRL.py:3585-3601`（捕获后回退 uniform；若 `_SIM_FAIL_CLOSED` 为真则改抛 `RuntimeError`，SimulationRL.py:3586-3587；`_SIM_FAIL_CLOSED` 定义于 SimulationRL.py:219，源自 env `SIM_FAIL_CLOSED`）。
- 依赖关系：被 `CODE/SimulationRL.py:3539`（Earth 初始化）与 `CODE/SimulationRL.py:102`（`_results_dir_traffic_od_tag` 内）调用；测试引用 `CODE/tests/test_traffic_od_fail_loud.py:19`。env 生产侧：`CODE/run.py:55` 将 `LEO_RUNTIME_TRAFFIC_JSON` 映射为 `SIM_TRAFFIC_CONFIG`，run.py:624-646 负责 set/pop。

#### `def build_od_matrix_for_gateways(gateway_names, cfg, *, lat_deg=None, lon_deg=None, mass=None)` — CODE/traffic_od.py:347

- 定位：CODE/traffic_od.py:347
- 职责 (FACT)：OD 构建总调度器。按 `cfg["mode"]`（缺省 uniform，小写化，行 355）分派：`uniform`（行 356-360）；`h2`（读 p/g/sources 或 sources_hot/dests 或 dests_hot/weight_floor，行 362-369）；`gravity`（缺 lat/lon/mass 任一时 `raise ValueError` 提示须在 linkCells2GTs 后构建，行 371-385）；`gravity_corridors`（同样缺参 `raise ValueError`，行 387-399）；`mlab`（缺 lat/lon `raise ValueError`、缺 `csv_path` `raise ValueError`，行 401-416；`hourly: true` 时本地导入并调用 `build_od_weights_mlab_hourly`，否则调用 `build_od_weights_mlab`，行 421-438）；未知模式 `raise ValueError("Unknown traffic mode ...")`（行 440-442，fail-loud）。
- 关键流程/结构：纯 if 链分派；mlab 的两个导入为函数内局部导入（行 422、431），注释说明目的是隔离 pandas 重依赖（行 402-405、431）。
- 输入/输出：网关名列表 + cfg + 可选物理量；输出 `(W, meta)`，W 恒为 (n,n) 行随机矩阵、对角 0（mlab hourly 分支时 meta 额外携带 `hourly_matrices`，形状 (24,n,n)，见 traffic_mlab.py:206）。
- 依赖关系：调用本文件全部 build_od_weights_* 与 traffic_mlab 的两个构建函数；被 `CODE/SimulationRL.py:3547、3579、3593`（启动期）与 `CODE/SimulationRL.py:7931、7939`（deferred，在 linkCells2GTs 之后，质量 = 网关 `cellsInRange` 人口和，见 SimulationRL.py:7921-7928）调用。产物消费点：`Gateway.timeToFullBlock`（SimulationRL.py:3130-3191），其中 `w = wmat[s_idx, d_idx]`（行 3151），`flow = totalAvgFlow * w`（行 3181）。

---

### 文件 `CODE/traffic_burst.py`（实测 194 行）

模块级说明：

- 模块 docstring（行 1-28）：声明本模块在静态 OD 矩阵之上叠加事件驱动、随时间变化的乘性因子 m(t,s,d)，配置 JSON 路径来自 env `SIM_TRAFFIC_BURSTS`，schema 含 `bursts: [{src, dst, t_start, t_ramp_up, t_hold, t_ramp_down, multiplier, label}]`，多事件因子连乘 (FACT，与 `BurstSchedule.multiplier` 实现一致)。docstring 行 7-8 列举的用途（体育赛事、灾害救援、闪击流量、冲突区）为注释声明的建模意图 (INFERENCE：代码只实现时间窗+乘子机制，不区分事件类型)。
- imports（行 29-35）：`json`、`hashlib`、`os`、`math`、`typing`；无 numpy/pandas。
- 全局常量：无。
- env 变量读取点：`load_burst_schedule_from_env` 内行 171 读 `SIM_TRAFFIC_BURSTS`。
- 模块被谁调用：`CODE/SimulationRL.py:25` 导入 `load_burst_schedule_from_env`；测试 `CODE/tests/test_traffic_burst.py:15`（导入 `BurstSchedule`、`load_burst_schedule_from_env`、`_resolve_indices`）、`CODE/tests/test_runtime_effect_receipt.py:57`（导入 `BurstSchedule`、`canonical_json_sha256`）、`CODE/tests/validate_burst_rates.py:23`。

#### `def canonical_json_sha256(value)` — CODE/traffic_burst.py:38

定位行 38；职责 (FACT)：对任意 JSON 可序列化值做规范化序列化（`sort_keys=True`、紧凑分隔符、`ensure_ascii=False`）后取 SHA-256 hex（行 39-40）。输入：任意值；输出：64 字符 hex 字符串。被 `load_burst_schedule_from_env`（行 190）调用以给配置封缄；测试引用 `CODE/tests/test_runtime_effect_receipt.py:57`。注：`CODE/SimulationRL.py:50` 另有一份独立的 `_canonical_json_sha256`，不从本模块导入 (FACT)。

#### `def _resolve_indices(name_patterns, gateway_names)` — CODE/traffic_burst.py:43

定位行 43；职责 (FACT)：把名字模式解析为网关下标集合，匹配规则与 traffic_od 相同（子串或逗号首段相等，行 51-57）。与 `traffic_od._resolve_subset_indices` 的差异：本函数对匹配不到任何网关的模式不报错，静默跳过（行 47-58 中无 raise 路径；解析结果记录于 `BurstSchedule` 条目的 `resolved_src/resolved_dst` 供事后审计）(FACT)。输入：模式序列 + 网关名序列；输出：`Set[int]`。被 `BurstSchedule.__init__`（行 81-82）调用；测试引用 `CODE/tests/test_traffic_burst.py:15`。

#### `class BurstSchedule` — CODE/traffic_burst.py:61

- 定位：CODE/traffic_burst.py:61
- 职责 (FACT)：持有一组时间窗化的 (src 集合, dst 集合, multiplier) 突发事件，提供逐 (t, s, d) 的乘性因子查询与运行时审计计数。
- 关键状态/结构：`self.entries`，每事件一个 dict（行 83-104），含：原始模式 `src_patterns/dst_patterns`、解析下标 `src_idx/dst_idx`、解析出的网关名 `resolved_src/resolved_dst`、时间点 `t_start/t_ramp_up_end/t_hold_end/t_end`、时长 `t_ramp_up/t_hold/t_ramp_down`、峰值 `multiplier`、`label`，以及五个运行时计数器 `calls/window_calls/od_match_calls/active_calls/effect_calls`（初值 0，行 99-103）；另有 `self.config_sha256`（行 72）。
- 关键流程/方法：
  - `__init__`(行 64)：逐事件解析——时间参数截为非负、multiplier 截为非负（行 74-78）、调用 `_resolve_indices` 解析 src/dst（行 81-82）、预计算 ramp_up 结束/hold 结束/事件结束时刻（行 91-93），append 到 entries（行 105）。
  - `__len__`(行 107)：返回事件数。
  - `multiplier`(行 110)：核心查询。对每个条目先把 `calls` 加 1（行 114）；OD 匹配则 `od_match_calls` 加 1（行 115-116）；t 在 [t_start, t_end] 外则跳过（行 117-118），在窗内 `window_calls` 加 1（行 119）；OD 不匹配跳过（行 120-121），匹配则 `active_calls` 加 1（行 122）；包络计算：上升沿线性 `(t-t_start)/t_ramp_up`、下降沿 `1-(t-t_hold_end)/t_ramp_down`、平台期 1.0（行 123-128），scale 截断 [0,1]（行 129），`factor = 1 + (multiplier-1)*scale`（行 130）；factor 与 1.0 不 isclose（abs_tol=1e-12）时 `effect_calls` 加 1（行 131-132）；多事件 factor 连乘（行 133）。返回乘积 m，1.0 表示无加成。
  - `is_active`(行 136)：任一事件的 [t_start, t_end] 覆盖 t 即返回 True（行 137-140）。
  - `summary`(行 142)：导出每事件的请求/解析/运行时计数清单（含 resolved 下标与名字、时间窗、五个计数器，行 144-166），供运行收据审计。
- 输入/输出：构造吃 burst dict 列表 + 网关名序列；`multiplier(t, s_idx, d_idx)` 吐 float ≥ 0（理论上可低于 1：multiplier 允许 <1，包络使 factor 落在 [min(1,multiplier), max(1,multiplier)] 区间）(FACT)。
- 依赖关系：由 `load_burst_schedule_from_env`（行 187）实例化；被 `CODE/SimulationRL.py:3608` 加载为 `earth.burst_schedule`，每次 packet-fill 决策时在 `Gateway.timeToFullBlock` 内被调用（SimulationRL.py:3154-3165：`burst.multiplier(env.now, s_idx, d_idx)` 乘到 OD 权重 w 上）；`summary()` 与计数器被运行收据检查（SimulationRL.py:10847-10851、10942-10972：fail-closed 模式下 `calls>=1`、`effect_calls>=1`、逐事件 `active_calls/effect_calls` 不符即判 receipt mismatch）。行为佐证：`CODE/tests/test_traffic_burst.py:15`、`CODE/tests/validate_burst_rates.py:23`、`CODE/tests/test_runtime_effect_receipt.py:266-267、388`。

#### `def load_burst_schedule_from_env(gateway_names)` — CODE/traffic_burst.py:169

- 定位：CODE/traffic_burst.py:169
- 职责 (FACT)：从 env `SIM_TRAFFIC_BURSTS`（JSON 文件路径）加载并构造 `BurstSchedule`；env 未设置返回 None（行 172-173）。
- 关键流程/结构：路径转绝对路径；文件不存在时 `print` 并返回 None（行 175-177）；JSON 解析异常时 `print` 并返回 None（行 178-183）；`bursts` 为空返回 None（行 184-186）；构造 `BurstSchedule` 并附 `config_sha256=canonical_json_sha256(cfg)`（行 187-191）；构造后事件数为 0 返回 None（行 192-193）。模块级不是 fail-loud：所有失败路径都是 print+None；fail-closed 升级在调用方 `CODE/SimulationRL.py:3609-3624`（`_SIM_FAIL_CLOSED` 且 env 已设置但 schedule 为 None 时 `raise RuntimeError("requested burst schedule did not initialize")`）。
- 输入/输出：网关名序列；输出 `BurstSchedule` 或 None。
- 依赖关系：调用 `BurstSchedule`、`canonical_json_sha256`；被 `CODE/SimulationRL.py:3608` 调用；测试引用 `CODE/tests/test_traffic_burst.py:15`。env 生产侧：`CODE/run.py:56` 映射 `LEO_RUNTIME_BURSTS_JSON`→`SIM_TRAFFIC_BURSTS`，run.py:655-664 set/pop。

---

### 文件 `CODE/traffic_diurnal.py`（实测 382 行）

模块级说明：

- 模块 docstring（行 1-41）：声明本模块提供按源网关、带经度本地时相位偏移的 24 小时乘性因子；曲线两来源——M-Lab CSV 的 `hour_utc` 列聚合（经验）或合成正弦 `1 + A·sin(2π(h_local−φ)/24)`；时间压缩模型：一个仿真秒代表 `(24h)/sim_duration_s` 墙钟时间，每 `sim_duration_s` 仿真秒走完一个昼夜周期。配置路径来自 env `SIM_TRAFFIC_DIURNAL`（行 25）。以上机制描述与实现一致 (FACT)。docstring 行 11-12 的文献锚点（"WetLinks-anchored amplitude, arXiv 2402.16448"、"peak at hour 20"）为注释声明的取值依据，代码中只有数值 0.4/20.0 可核验 (INFERENCE：文献支持无法从代码核验)。
- **docstring 与现状不一致** (FACT)：行 20-23 称「This module is load-only / multiplier-only. It does NOT call into SimulationRL packet generation — Phase 4 will wire it into the packet-fill loop … see `SimulationRL.py:2738`」，但实际接线已存在于 `CODE/SimulationRL.py:3169-3180`（`diurnal.multiplier(env.now, s_idx)` 在 `Gateway.timeToFullBlock` 内乘到 w 上），且引用行号 2738 与实际接线位置（3130-3191）不符。
- imports（行 42-53）：`json`、`math`、`os`、`typing`、`numpy`；行 53 `from traffic_mlab import _nearest_gateway_index, load_mlab_csv`（模块级）——由于 traffic_mlab 模块级 import pandas（traffic_mlab.py:44），import 本模块即传递依赖 pandas；而 `CODE/SimulationRL.py:26` 模块级导入本模块 (FACT)。
- 全局常量（行 60-63）：`_DEFAULT_AMPLITUDE = 0.4`、`_DEFAULT_PEAK_HOUR_LOCAL = 20.0`、`_DEFAULT_MIN_FLOOR = 0.1`、`_HOURS_PER_DAY = 24`；行 56-59 注释声明 0.4/20.0 的文献出处。
- env 变量读取点：`load_diurnal_schedule_from_env` 内行 337 读 `SIM_TRAFFIC_DIURNAL`。
- 模块被谁调用：`CODE/SimulationRL.py:26` 导入 `load_diurnal_schedule_from_env`；测试 `CODE/tests/test_traffic_diurnal.py:29-35`（导入 `DiurnalSchedule`、`_hour_utc_at_sim_time`、`_interp_24h_pattern`、`_local_hour`、`load_diurnal_schedule_from_env`）。

#### `def _hour_utc_at_sim_time(t_sim, sim_duration_s)` — CODE/traffic_diurnal.py:66

定位行 66；职责 (FACT)：时间压缩映射——`(t_sim / sim_duration_s) * 24 % 24`，把仿真秒映射为压缩 UTC 小时；`sim_duration_s <= 0` 返回 0.0（行 69-71）。输入：仿真时刻 + 仿真时长；输出：[0,24) 的 float 小时。被 `DiurnalSchedule.multiplier`（行 163）调用；测试引用 `CODE/tests/test_traffic_diurnal.py:31`。

#### `def _local_hour(h_utc, lon_deg)` — CODE/traffic_diurnal.py:74

定位行 74；职责 (FACT)：近似本地太阳时——`(h_utc + lon_deg/15) % 24`（经度每 +15° 偏移 1 小时，行 77）。输入：UTC 小时 + 经度；输出：[0,24) float。被 `from_sinusoidal`（行 230）与 `from_mlab_csv`（行 308）在构建期使用；测试引用 `CODE/tests/test_traffic_diurnal.py:33`。

#### `def _interp_24h_pattern(pattern_hours)` — CODE/traffic_diurnal.py:80

定位行 80；职责 (FACT)：把稀疏 `{小时int: 值}` 映射用 `np.interp(..., period=24)` 跨午夜边界线性插值成 24 点数组，再把均值归一为 1.0（均值为 0 时回退全 1，行 99-103）；空输入返回全 1（行 84-85）。输入：`Dict[int, float]`；输出：长度 24 的 float64 数组（乘性曲线，均值 1）。被 `from_mlab_csv`（行 294）调用；测试引用 `CODE/tests/test_traffic_diurnal.py:32`。

#### `class DiurnalSchedule` — CODE/traffic_diurnal.py:107

- 定位：CODE/traffic_diurnal.py:107
- 职责 (FACT)：持有每源网关一条长度 24 的 UTC 小时乘性曲线（均值 1.0），按「仿真时刻 → 压缩 UTC 小时 → 该网关曲线插值」给出 `multiplier(t, src_idx)`。
- 关键状态/结构：`per_gt_pattern_utc`（形状 (n,24) 的 float64 数组，UTC 小时键）、`gateway_names`、`gateway_lon_deg`、`sim_duration_s`、`min_floor`（下限截断，默认 0.1）、`source_label`（行 142-147）。
- 关键流程/方法：
  - `__init__`(行 121)：校验——pattern 形状必须等于 (n,24) 否则 `raise ValueError`（行 131-135）；网关名与经度长度一致否则 `raise ValueError`（行 136-139）；`sim_duration_s > 0` 否则 `raise ValueError`（行 140-141）；随后落盘字段（min_floor 截为非负，行 146）。
  - `__len__`(行 149)：返回网关数。
  - `multiplier`(行 152)：查询入口。`src_idx` 越界返回 1.0（行 161-162）；`_hour_utc_at_sim_time` 得压缩 UTC 小时（行 163）；`np.interp(period=24)` 在该网关曲线上插值（行 164-166）；返回 `max(min_floor, val)`（行 167）。docstring 行 154-159 说明曲线在构建期已按 UTC 键化，查询期不再做经度偏移 (FACT，与 from_sinusoidal 构建逻辑行 225-231 一致)。
  - `pattern_at_utc`(行 169)：诊断用——直接对 (gt, h_utc) 插值，绕开时间压缩、不施加 min_floor（行 172-174）。
  - `summary`(行 176)：导出 per-GT 诊断（gateway/lon_deg/min/max/mean/argmax_utc_hour）与全局字段（source_label/sim_duration_s/min_floor/n_gateways），供 run_meta（行 178-195）。
  - `from_sinusoidal`(行 200，classmethod)：合成正弦构建。`phi = peak_hour_local - 6` 使峰值落在指定本地时（注释行 221：sin 峰值在 h−φ=6）；`curve_local = 1 + A·sin(2π(h−φ)/24)`（行 222-224）；逐网关把本地时曲线按 `h_local = round(h_utc + lon/15) mod 24` 重采样为 UTC 键曲线（行 227-231）——即各网关曲线形状相同、仅相位取经度偏移 (FACT，docstring 行 214-217 同)；`source_label` 形如 `sinusoidal(A=0.40, peak_local=20.0h)`（行 238）。
  - `from_mlab_csv`(行 242，classmethod)：经验曲线构建。校验 names/lat/lon 长度一致否则 `raise ValueError`（行 274-275）；`load_mlab_csv` 读 CSV（行 276）；`pair_weight = sample_count * mean_throughput_mbps`（行 277）；逐行把 client 城市经 `_nearest_gateway_index` 投影到最近网关 si，按 `hour_utc % 24` 聚合 pair_weight 到 (si, hour)（行 280-287）；每网关：不同小时桶数 ≥ `sparse_fallback_min_hours`（默认 4）则 `_interp_24h_pattern` 建经验曲线，否则记入 fallback_gts（行 289-296）；fallback 网关用默认正弦曲线（A=0.4、peak=20）按其经度相位重采样填充（行 299-309）；`source_label` 记录 CSV 基名与经验/回退网关数（行 317-321）。
- 输入/输出：构造吃 (n,24) 数组或 CSV+网关物理量；`multiplier(t, src_idx)` 吐 float ≥ min_floor。
- 依赖关系：调用 `_hour_utc_at_sim_time`、`_local_hour`、`_interp_24h_pattern`、`traffic_mlab.load_mlab_csv`、`traffic_mlab._nearest_gateway_index`；由 `load_diurnal_schedule_from_env`（行 357、370）实例化；被 `CODE/SimulationRL.py:3638` 加载为 `earth.diurnal_schedule`，在 `Gateway.timeToFullBlock` 内于 burst 之后乘性叠加（SimulationRL.py:3169-3180，注释行 3166-3168 说明 diurnal 在 burst 之后施加、两者乘法复合）；运行收据检查见 SimulationRL.py:10978-10980。行为佐证：`CODE/tests/test_traffic_diurnal.py:29-35`、`CODE/tests/test_runtime_effect_receipt.py:389`。

#### `def load_diurnal_schedule_from_env(gateway_names, gateway_lat_deg, gateway_lon_deg, sim_duration_s)` — CODE/traffic_diurnal.py:325

- 定位：CODE/traffic_diurnal.py:325
- 职责 (FACT)：从 env `SIM_TRAFFIC_DIURNAL`（JSON 路径）加载配置并构造 `DiurnalSchedule`；env 未设置返回 None（行 338-339）。
- 关键流程/结构：文件不存在 print 并返回 None（行 341-343）；JSON 解析失败 print 并返回 None（行 344-349）；`mode` 缺省 `sinusoidal`（行 351）；`sim_duration_s` 可被配置覆盖（行 352）；`min_floor` 缺省 0.1（行 353）；`sinusoidal` 分支调 `from_sinusoidal`（行 356-364）；`mlab` 分支缺 `csv_path` 时 print 并返回 None，否则调 `from_mlab_csv`（行 365-377）；未知 mode print 并返回 None（行 378-379）；构造期任何异常 print 并返回 None（行 380-382）。模块级不是 fail-loud（全路径 print+None）；fail-closed 升级在调用方 `CODE/SimulationRL.py:3641-3656`（`_SIM_FAIL_CLOSED` 且 env 已设置但结果为 None 时 `raise RuntimeError("requested diurnal schedule did not initialize")`）。
- 输入/输出：网关名/纬度/经度 + 仿真时长；输出 `DiurnalSchedule` 或 None。
- 依赖关系：调用 `DiurnalSchedule.from_sinusoidal` / `from_mlab_csv`；被 `CODE/SimulationRL.py:3638` 调用（其 sim 时长取 env `SIM_TIME_LIMIT` 覆盖或 `inputParams['Test length'][0]`，SimulationRL.py:3633-3637）；测试引用 `CODE/tests/test_traffic_diurnal.py:34`。env 生产侧：`CODE/run.py:57` 映射 `LEO_RUNTIME_DIURNAL_JSON`→`SIM_TRAFFIC_DIURNAL`，run.py:671-677 set/pop。

---

### 文件 `CODE/traffic_mlab.py`（实测 325 行）

模块级说明：

- 模块 docstring（行 1-37）：声明本模块是 M-Lab Speedtest CSV → 最近网关投影 → 行随机 OD 矩阵的适配层；CSV schema 为 `client_city, client_lat, client_lon, server_city, server_lat, server_lon, hour_utc, sample_count, mean_throughput_mbps`（行 15-18）；权重定义为 `sample_count 之和 * mean_throughput_mbps 之和` 跨 hour 桶聚合、代理「城市对间交换字节量」，同城对过滤、城市按大圆距离投影到最近网关；输出 W 行随机且对角 0 (FACT，除「代理字节量」这一解释为注释声明外（行 20-25），其余与实现一致；(INFERENCE)：weight≈bytes 的物理解释不可从代码核验，代码只计算 `sample_count * mean_throughput_mbps`，行 275)。docstring 行 8-13 描述的四阶段流水线（Phase 1-4）为开发计划注释。
- imports（行 38-50）：`os`、`typing`、`numpy`、`pandas`（行 44，pandas 为硬依赖——本模块被 `traffic_diurnal.py:53` 模块级导入，进而被 `SimulationRL.py:26` 间接导入）；行 46-50 从 traffic_od 导入 `build_od_weights_uniform`、`haversine_km`、`_row_normalize_od`。
- 全局常量（行 53-63）：`_REQUIRED_COLUMNS`，9 个必需 CSV 列名。
- env 变量读取点：无（`os` 仅用于路径判断/绝对路径）。
- 模块被谁调用：被 `CODE/traffic_od.py:422、431` 函数内局部导入（`build_od_weights_mlab_hourly`、`build_od_weights_mlab`，mlab 模式分支）；被 `CODE/traffic_diurnal.py:53` 模块级导入（`_nearest_gateway_index`、`load_mlab_csv`）；测试 `CODE/tests/test_traffic_mlab.py:26-31`（导入全部四个符号）。另 `CODE/scripts/analysis/mlab_autocorr.py:16` 仅在注释中提及本模块 (FACT)。

#### `def load_mlab_csv(csv_path)` — CODE/traffic_mlab.py:66

- 定位：CODE/traffic_mlab.py:66
- 职责 (FACT)：加载并规范化 M-Lab CSV 为 DataFrame；本模块 fail-loud 边界——`csv_path` 为空或文件不存在 `raise FileNotFoundError`（行 74-75）；缺必需列 `raise ValueError`（行 78-83）；零数据行 `raise ValueError`（行 84-85）；数值列强转后全为 NaN 时 `raise ValueError`（行 98-101）。
- 关键流程/结构：`pd.read_csv(comment="#")` 容忍 `#` 注释行（行 77）；城市名去空白（行 88-89）；7 个数值列 `pd.to_numeric(errors="coerce")` 后 dropna（行 92-96）。
- 输入/输出：CSV 路径；输出规范化 `pd.DataFrame`。
- 依赖关系：被本文件 `build_od_weights_mlab`（行 258）、`build_od_weights_mlab_hourly`（行 163）及 `CODE/traffic_diurnal.py:276` 调用；测试引用 `CODE/tests/test_traffic_mlab.py:29`。

#### `def _nearest_gateway_index(lat, lon, gw_lat, gw_lon)` — CODE/traffic_mlab.py:105

定位行 105；职责 (FACT)：线性扫描全部网关，用 `haversine_km` 找大圆距离最近的网关下标（行 112-119）。输入：点经纬度 + 网关纬度/经度序列；输出：int 下标（空网关序列会返回默认值 0——代码无空序列保护，但调用方均保证 n≥1 上下文，此处仅陈述代码事实）。被 `build_od_weights_mlab`（行 290、292）、`build_od_weights_mlab_hourly`（行 173、175）、`CODE/traffic_diurnal.py:282` 调用；测试引用 `CODE/tests/test_traffic_mlab.py:30`。

#### `def build_od_weights_mlab_hourly(gateway_names, lat_deg, lon_deg, csv_path, *, blend_uniform=0.0, sparse_fallback_min_samples=50)` — CODE/traffic_mlab.py:122

- 定位：CODE/traffic_mlab.py:122
- 职责 (FACT)：构建 24 个逐 UTC 小时的行随机 OD 矩阵加一份天平均矩阵：聚合流程与 `build_od_weights_mlab` 相同但按 hour 分桶；样本不足的小时用天平均矩阵回退 (FACT，docstring 行 131-149 与实现一致)。
- 关键流程/结构：names/lat/lon 长度不一致 `raise ValueError`（行 151-155，fail-loud）；先调 `build_od_weights_mlab` 得到天平均矩阵 W_day 作回退底料（行 159-161）；再次 `load_mlab_csv`（行 163）、去同城行（行 164-165）、`pair_weight = sample_count*mean_throughput_mbps`（行 166）、`hour_int = hour_utc.astype(int) % 24`（行 167）；逐行投影 client/server 城市到最近网关并丢弃投影到同一网关的行（行 170-179）；分配 `hourly` 数组 (24,n,n)（行 181）；逐小时：`sample_count` 合计 < `sparse_fallback_min_samples` 的小时直接用 W_day 并记入 `fallback_hours`（行 184-190），否则聚合 raw 矩阵、`_row_normalize_od`、可选 blend_uniform 混合（行 191-199）。
- 输入/输出：网关名 + 逐网关经纬度 + CSV 路径；输出 `(W_day, meta)`——首个返回值是天平均 (n,n) 矩阵（注释行 417-420/traffic_od.py 说明为兼容 `Earth.od_weight_matrix`）；meta 含 `mode="mlab_hourly"`、`hourly_matrices`（(24,n,n) ndarray，行 206）、`per_hour_samples`、`hourly_fallback_hours`、`sparse_fallback_min_samples`、`day_avg_meta` 等（行 201-212）。
- 依赖关系：调用 `load_mlab_csv`、`_nearest_gateway_index`、`build_od_weights_mlab`、`_row_normalize_od`、`build_od_weights_uniform`；被 `CODE/traffic_od.py:423`（`build_od_matrix_for_gateways` 的 mlab+hourly 分支）调用。下游消费：`CODE/SimulationRL.py:7948-7957` 把 `hourly_matrices` 从 meta 弹出存为 `earth.od_weight_matrices_hourly`（保证 meta 可 JSON 序列化），`Gateway.timeToFullBlock` 按压缩 UTC 小时取用对应小时的矩阵（SimulationRL.py:3141-3147）。测试引用 `CODE/tests/test_traffic_mlab.py:28`（其行 253 起为 dispatcher hourly 端到端测试）。

#### `def build_od_weights_mlab(gateway_names, lat_deg, lon_deg, csv_path, *, blend_uniform=0.0)` — CODE/traffic_mlab.py:216

- 定位：CODE/traffic_mlab.py:216
- 职责 (FACT)：从 M-Lab CSV 构建单份行随机 OD 矩阵：同城行过滤 → 按 (client_city, server_city) 跨 hour 桶聚合 pair_weight → 城市投影到最近网关 → 聚合成 raw 矩阵 → 行归一化，可选与均匀矩阵凸混合。
- 关键流程/结构：names/lat/lon 长度不一致 `raise ValueError`（行 242-246，fail-loud）；`n<=1` 不报错，返回均匀（全零）矩阵并写 `meta["note"]`（行 254-256）；`load_mlab_csv`（行 258，其内部 fail-loud 见上）；大小写折叠比较过滤同城行并计数（行 264-266），过滤后无剩余行 `raise ValueError("... only same-city rows ...")`（行 267-271，fail-loud）；`pair_weight = sample_count * mean_throughput_mbps`（行 275）；按六列 groupby 求和（行 276-283）；逐城市对投影，client 与 server 投到同一网关的对被丢弃（`continue`，行 294-297——静默丢弃，仅注释说明理由，无计数进 meta），其余累加进 raw 并记录 `proj_log`（行 298-305）；meta 记录 `projection_log_count`、逐网关出/入向质量（行 307-309）；`_row_normalize_od`（零出量行在该函数内回退为均匀行，traffic_od.py:97-100）（行 312）；`blend_uniform>0` 时凸混合再归一化（行 316-319）；meta 补 `row_sums` 与 `isolated_gateways`（raw 行和为 0 的网关名清单，行 321-324）。
- 输入/输出：网关名 + 逐网关经纬度 + CSV 路径；输出 `(W, meta)`，W 为 (n,n) 行随机矩阵、对角 0。
- 依赖关系：调用 `load_mlab_csv`、`_nearest_gateway_index`、`_row_normalize_od`、`build_od_weights_uniform`；被 `CODE/traffic_od.py:432`（mlab 非 hourly 分支）与本文件 `build_od_weights_mlab_hourly`（行 159）调用。测试引用 `CODE/tests/test_traffic_mlab.py:27`（其行 149 起为 dispatcher 端到端测试）。

---

## 附：跨文件接线速查（供主 agent 拼接时索引）

- 启动路径：`SimulationRL.py:3539` 读 env 配置 → `traffic_mode_needs_gateway_physical`（3559）决定立即构建（3579）还是 deferred（3560-3568）；deferred 在 `linkCells2GTs` 之后于 `SimulationRL.py:7931-7933` 带 lat/lon/mass 重建；任何异常在非 fail-closed 下回退 uniform（3585-3601、7935-7942），fail-closed 下 `raise RuntimeError`（3586-3587、7936-7937）。
- 运行时路径：`Gateway.timeToFullBlock`（SimulationRL.py:3130）取矩阵（hourly 3141-3147 或静态 3147）→ `w = wmat[s,d]`（3151）→ burst 乘子（3154-3165）→ diurnal 乘子（3169-3180）→ `flow = totalAvgFlow * w`（3181）→ 指数分布抽样填充时间（3187-3191）。
- env 变量总表：`SIM_TRAFFIC_UNIFORM`（traffic_od.py:336；SimulationRL.py:99）、`SIM_TRAFFIC_CONFIG`（traffic_od.py:338）、`SIM_TRAFFIC_BURSTS`（traffic_burst.py:171；SimulationRL.py:3164、3611、3621、10843）、`SIM_TRAFFIC_DIURNAL`（traffic_diurnal.py:337；SimulationRL.py:3179、3643、3653、10853）、`SIM_FAIL_CLOSED`（SimulationRL.py:219）、`SIM_TIME_LIMIT`（SimulationRL.py:3517、3633）。生产侧映射：`CODE/run.py:55-57、624-677`。
- 矩阵语义不变式：所有模式输出 (n,n) float64 行随机矩阵，对角 0，行 s 对 d≠s 求和为 1（traffic_od.py:19；`_row_normalize_od` 行 89-101；mlab docstring 行 31-33）；mlab hourly 额外输出 (24,n,n) 数组于 meta（traffic_mlab.py:206），由 SimulationRL 弹出为 `earth.od_weight_matrices_hourly`（SimulationRL.py:7948-7953）。
# 旧平台路由/学习算法扩展模块组说明书片段

范围：`CODE/routing_hooks.py`、`CODE/routing_mappo.py`、`CODE/routing_multistep.py`、`CODE/routing_path_credit.py`。所有行号均为实测（`wc -l` + 全文通读）。标注约定：(FACT) = 代码中可直接确认；(INFERENCE) = 从命名/注释/上下文推测。

---

## 文件 `CODE/routing_hooks.py`（实测 133 行）

模块级说明：
- 模块 docstring（行 1–4）：声明本模块是「DDQNAgent 的最小路由 hook」，未设 `SIM_ROUTING_MODE` 或设为 `ddqn` 时走 identity 打分 + 传统 argmax 掩码路径。
- imports（行 5–10）：`__future__.annotations`、`os`、`typing.Any/Dict/Tuple`、`numpy`。
- 全局常量 `SUPPORTED_ROUTING_MODES = ("ddqn",)`（行 13）：保留 CODE 中唯一受支持的路由模式白名单。
- 被 `CODE/SimulationRL.py:229` 在模块顶层 import（`parse_routing_mode` 别名 `_parse_sim_routing_mode`、`validate_routing_mode` 别名 `_validate_routing_mode`），并在 `CODE/SimulationRL.py:231–232` 模块加载时立即执行解析与校验——即非法 `SIM_ROUTING_MODE` 会在 import 阶段 fail loud。(FACT)
- `CODE/run.py:743–753` 在配置转 env 阶段用自带白名单 `{"ddqn"}` 做另一层校验（不 import 本模块）。(FACT)
- 行为佐证：`CODE/tests/test_routing_mode_contract.py:41–52` 对 `parse_routing_mode`/`validate_routing_mode` 拒绝 legacy 模式与拼写错误做了契约测试。

#### `def parse_routing_mode() -> str` — CODE/routing_hooks.py:16
- 定位：CODE/routing_hooks.py:16
- 职责：读取 env `SIM_ROUTING_MODE`，空串或 `"ddqn"` 返回 `"ddqn"`，其余值抛 `ValueError`（错误信息点名 legacy 模式 `ddqn_cvar/cvar/tailguard`、`ddqn_mcp_hash/mcp/mcp_hash` 未迁移进保留 CODE）。(FACT)
- 输入/输出：无参；返回 `str` 或抛异常。
- 依赖关系：被 `CODE/SimulationRL.py:231` 在模块加载时调用；被 `CODE/tests/test_routing_mode_contract.py:46` 测试。

#### `def validate_routing_mode(mode: str) -> None` — CODE/routing_hooks.py:27
- 定位：CODE/routing_hooks.py:27
- 职责：`mode` 不在 `SUPPORTED_ROUTING_MODES` 中时抛 `ValueError`，否则无操作。(FACT)
- 输入/输出：入 `mode: str`；无返回。
- 依赖关系：被 `CODE/SimulationRL.py:232`、本文件 `build_default_hooks`（行 132）、`CODE/tests/test_routing_mode_contract.py:52` 调用。

#### `class LocalStatsHook` — CODE/routing_hooks.py:34
- 定位：CODE/routing_hooks.py:34
- 职责：决策前本地统计 hook 的默认 no-op 实现（docstring 行 35：「Inference-only local statistics; default is no-op」）。(FACT)
- 关键状态/结构：无任何实例状态（无 `__init__`）。
- 关键流程/方法：`on_pre_decision(self, agent, sat, block, linked_sats)`（行 37）函数体为 `pass`（行 44），什么都不做。
- 输入/输出：入 agent/卫星/数据包/邻居表；无返回。
- 依赖关系：被 `build_default_hooks`（行 133）实例化；被 `CODE/SimulationRL.py:6414` import、行 6425 直接实例化（`ddqn_cvar` 分支）；其方法在 `CODE/SimulationRL.py:6856`（`DDQNAgent.getNextHop` 内）被调用。

#### `class ActionScoringHook` — CODE/routing_hooks.py:47
- 定位：CODE/routing_hooks.py:47
- 职责：抽象基类——把网络原始输出映射成 `(1, n_actions)` 的利用（exploitation）打分（docstring 行 48）。(FACT)
- 关键状态/结构：无实例状态。
- 关键流程/方法：`score(self, agent, q_raw, *, new_state, linked_sats, sat, block)`（行 50）只 `raise NotImplementedError`（行 60）。
- 输入/输出：入原始 Q 输出 `q_raw` 等；契约上返回 `np.ndarray`。
- 依赖关系：被 `IdentityScoringHook`（行 63）继承；自身不直接被调用。

#### `class IdentityScoringHook(ActionScoringHook)` — CODE/routing_hooks.py:63
- 定位：CODE/routing_hooks.py:63
- 职责：标量 Q 的恒等打分——docstring（行 64）注明 `q_raw` 形状为 `(1, 4)`。(FACT)
- 关键状态/结构：无实例状态。
- 关键流程/方法：`score(...)`（行 66）把 `q_raw` 转 `float64`，一维时 reshape 成 `(1, -1)`，返回前 `agent.actionSize` 列（行 76–79），不做任何变换。
- 输入/输出：入 `q_raw`（网络输出）；返回 `(1, actionSize)` 的 `float64` 数组。
- 依赖关系：由 `build_default_hooks`（行 133）实例化；其 `score` 在 `CODE/SimulationRL.py:6941–6943`（`DDQNAgent.getNextHop` 内）被调用。

#### `class ActionSelectorHook` — CODE/routing_hooks.py:82
- 定位：CODE/routing_hooks.py:82
- 职责：抽象基类——从打分中选出一个可行动作（ exploitation 选择）。(FACT)
- 关键状态/结构：无实例状态。
- 关键流程/方法：`select_exploitation(self, agent, scores, q_for_mask, linked_sats, new_state, sat, block)`（行 83）只 `raise NotImplementedError`（行 93）；契约返回 `Tuple[int, str]`（动作索引 + 动作键）。
- 输入/输出：入打分数组与邻居表；契约返回 `(int, str)`。
- 依赖关系：被 `BaselineSelectorHook`（行 96）继承；自身不直接被调用。

#### `class BaselineSelectorHook(ActionSelectorHook)` — CODE/routing_hooks.py:96
- 定位：CODE/routing_hooks.py:96
- 职责：基线选择器——docstring（行 97–99）描述为「Legacy：在 `q_for_mask` 上 argmax，对不可行方向置 `-inf` 直到选中可行方向」。(FACT)
- 关键状态/结构：`self._unav`（行 102）——不可用方向惩罚值（float）。
- 关键流程/方法：
  - `__init__(self, unav_penalty)`（行 101）：存惩罚值到 `self._unav`。
  - `select_exploitation(...)`（行 104）：复制 `q_for_mask` 为 `float64` 并截到 `actionSize` 列（行 114–115）；argmax 取动作（行 117–118）；若该方向 `linked_sats[action] is None`，则循环执行三个副作用——向 `agent.experienceReplay` 存入 `(new_state, act_index, self._unav, new_state, False)` 惩罚经验（行 120）、向 `agent.earth.rewards` 追加 `[self._unav, sat.env.now]`（行 121）、把该方向打分置 `-inf` 后重新 argmax（行 122–124），直到选中可行方向；返回 `(act_index, action)`（行 126）。
- 输入/输出：入打分与 `q_for_mask`；返回 `(动作索引 int, 动作键 str)`；副作用是惩罚经验直接写入 agent 的经验回放与 earth 奖励日志。
- 依赖关系：由 `build_default_hooks`（行 133）实例化；`select_exploitation` 在 `CODE/SimulationRL.py:6946–6948`（`DDQNAgent.getNextHop` 内）被调用；读取 `agent.actions`、`agent.actionSize`、`agent.experienceReplay`、`agent.earth.rewards`。

#### `def build_default_hooks(mode, *, unav_penalty)` — CODE/routing_hooks.py:129
- 定位：CODE/routing_hooks.py:129
- 职责：工厂函数——先 `validate_routing_mode(mode)`（行 132），再返回三元组 `(LocalStatsHook(), IdentityScoringHook(), BaselineSelectorHook(unav_penalty))`（行 133）。(FACT)
- 输入/输出：入路由模式字符串与不可用惩罚值；返回 `(LocalStatsHook, ActionScoringHook, ActionSelectorHook)` 三元组。
- 依赖关系：被 `CODE/SimulationRL.py:6432–6434`（`DDQNAgent.__init__` 的 `else` 分支）调用。注意 `CODE/SimulationRL.py:6416–6430` 的 `ddqn_mcp_hash`/`ddqn_cvar` 分支会 import `legacy.routing_mcp_hash`/`legacy.routing_tailguard`，但 `parse_routing_mode` 在模块加载时（SimulationRL.py:231）已拒绝这两种模式，故该两分支在保留 CODE 中不可达 (FACT——由行 20–24 的抛错逻辑与行 231 的调用顺序决定)。

---

## 文件 `CODE/routing_mappo.py`（实测 631 行）

模块级说明：
- 模块 docstring（行 1–44）：自述为「Recurrent MAPPO + Centralized Critic + Backpressure Prior 完整版 framework 实现」，列出 5 个 gap-decomposition 基线（B0–B4）与实施现状标记（✅/🟡）。docstring 中「今晚跑」「明天 debug」等表述是开发当时的状态记录。(FACT：docstring 存在；其陈述的完成度属作者自述)
- imports（行 45–52）：`os`、`collections`、`numpy`、`typing`、`tensorflow`/`keras`/`layers`。注意本模块在 import 时即需要 TensorFlow（与 routing_path_credit.py 的 lazy-import 不同）。(FACT)
- 全局常量 `GLOBAL_STATE_DIM = 44`（行 337）；`CODE/SimulationRL.py:546–547` 重复定义同名常量并注释「must match routing_mappo.GLOBAL_STATE_DIM」。(FACT)
- SimulationRL.py 侧的配套 env 解析在 `CODE/SimulationRL.py:495–516`（`SIM_FRAME_STACK_K`、`SIM_BP_BETA`、`SIM_BP_K_PROGRESS`、`SIM_BP_K_LOOP`、`SIM_CRITIC_GLOBAL`、`SIM_BP_ONLY`、`SIM_MAPPO_MODE` 等），而非经本模块的 `parse_env_config`。(FACT)

#### `class BackpressurePrior` — CODE/routing_mappo.py:59
- 定位：CODE/routing_mappo.py:59
- 职责：Backpressure 风格动作先验：按 docstring 公式（行 61–74）`BP(a) = (own_q[a] − nbr_q[a]) + k_progress·progress(a) − k_loop·loop(a)` 计算每方向分数，并与 DQN 的 Q 值做 z-归一化加权融合。(FACT)
- 关键状态/结构：四个超参数属性 `beta`、`k_progress`、`k_loop`、`invalid_score`（行 81–84）。
- 关键流程/方法：
  - `__init__(beta=0.3, k_progress=0.3, k_loop=1.0, invalid_score=-1e9)`（行 76）：存四个 float 超参数。
  - `compute_bp(own_queues, neighbor_queues, progress, is_loop, valid_mask)`（行 86）：对 4 个方向（U/D/R/L）按上述公式算 BP 分数，`valid_mask` 为假的方向覆写为 `invalid_score`（行 94–99）；返回 shape `[4]` 数组。
  - `score_actions(q_values, bp_values)`（行 101）：以 `bp_values > invalid_score/2` 判定有效方向（行 109）；全无效时原样返回 `q_values`（行 111–113）；否则在有效子集上分别对 Q 与 BP 做 z-归一化（均值/标准差取自有效子集，行 116–119），算 `score = q_norm + beta·b_norm`，无效方向置 `-1e9`（行 120–123）。
- 输入/输出：吃 4 维队列/进度/回环/掩码数组与 Q 值数组；吐 4 维 BP 分数或融合分数。
- 依赖关系：在 `CODE/SimulationRL.py:6268–6273`（`DDQNAgent.__init__`，条件 `_SIM_BP_BETA > 0.0`）实例化为 `self._mappo_bp`；`compute_bp` 在 `CODE/SimulationRL.py:6924–6930` 被调用，`score_actions` 在行 6935 被调用（均在 `DDQNAgent.getNextHop` 的 BP 融合段内）；`invalid_score`、`k_loop` 属性在行 6914、6922 被 `SIM_BP_CORRECT` 分支直接读取。同文件内还被 `RecurrentMAPPOAgent.__init__`（行 486–488）与 `FrameStackBPAgent.__init__`（行 597–599）实例化。SimulationRL.py:502–507 的注释称该 aggregate 版 BP「is broken」并提供 `SIM_BP_CORRECT` 修正路径——这是代码内注释的陈述，非本说明书的评价。

#### `class FrameStackHelper` — CODE/routing_mappo.py:130
- 定位：CODE/routing_mappo.py:130
- 职责：把最近 K 帧观测拼成单个 stacked 观测（docstring 行 131–141，示例用法是挂在 Satellite 实例上）。(FACT)
- 关键状态/结构：`self.K`、`self.obs_dim`、`self._buffer`（`collections.deque(maxlen=K)`，行 143–145）。
- 关键流程/方法：
  - `__init__(K=4, obs_dim=33)`（行 142）：初始化 deque。
  - `reset()`（行 147）：清空 deque。
  - `push_and_get(current_obs)`（行 150）：把输入 flatten 成 `float32`，维度不等于 `obs_dim` 时截断或零填充（行 153–158），append 进 deque；不足 K 帧时在左侧重复填充当前帧（行 161–162）；返回拼接后的 `(K*obs_dim,)` `float32` 数组（行 163–164）。
- 输入/输出：吃单帧观测；吐 `(K*obs_dim,)` 拼接向量。
- 依赖关系：调用方未确认——grep 全 CODE 无 import/实例化点。`CODE/SimulationRL.py:9499–9528` 的 `_apply_frame_stack` 用 `sat._mappo_frame_buf`（deque）在行内重新实现了同样的 K 帧拼接逻辑，并未使用本类。(FACT)

#### `def build_recurrent_actor(obs_dim, action_size, hidden_units=64, gru_units=64)` — CODE/routing_mappo.py:171
- 定位：CODE/routing_mappo.py:171
- 职责：工厂函数——构建 GRU 循环 actor 的 Keras 模型：两层 Dense(relu) 编码器（行 190–191）→ `GRUCell` 单步（行 194–195）→ 线性 action logits 头（行 198）；模型输入 `[obs, h_prev]`、输出 `[logits, h_new]`（行 200–201）。(FACT)
- 输入/输出：入维度参数；返回未编译的 `keras.Model`（name=`recurrent_actor`）。
- 依赖关系：唯一调用方是本文件 `RecurrentMAPPOAgent.__init__`（行 472–474）。

#### `def build_centralized_critic(global_state_dim, hidden_units=128)` — CODE/routing_mappo.py:209
- 定位：CODE/routing_mappo.py:209
- 职责：工厂函数——构建集中式 critic（V 值版）：输入 global state，两层 Dense(relu)，标量线性输出 `V(s_global)`（行 226–230）。(FACT)
- 输入/输出：入维度参数；返回 `keras.Model`（name=`centralized_critic`）。
- 依赖关系：唯一调用方是本文件 `RecurrentMAPPOAgent.__init__`（行 475）。

#### `def build_centralized_critic_per_action(global_state_dim, action_size, hidden_units=128)` — CODE/routing_mappo.py:233
- 定位：CODE/routing_mappo.py:233
- 职责：工厂函数——构建 Q 版集中式 critic：输入 global state，两层 Dense(relu)，输出 `action_size` 维 `Q_global`（行 244–248）。(FACT)
- 输入/输出：入维度参数；返回 `keras.Model`（name=`centralized_critic_q`）。
- 依赖关系：被 `CODE/SimulationRL.py:6506–6518`（`DDQNAgent.__init__`，条件 `_SIM_CRITIC_GLOBAL`）调用两次，构建 `self.q_global` 与 `self.q_global_target`；这两个网络在 `DDQNAgent.train` 中参与训练（target 网络 bootstrap 见 SimulationRL.py:7601，在线网络 `train_on_batch` 见行 7608，蒸馏进 local target 见行 7615，周期同步见行 7648–7650）。同文件内被 `FrameStackBPAgent.__init__`（行 603–606）在 `enable_global_critic=True` 时调用。

#### `def build_global_state(earth, current_sat_id=None, n_topk=8)` — CODE/routing_mappo.py:255
- 定位：CODE/routing_mappo.py:255
- 职责：从 `earth` 对象抽取 44 维 global state 向量（供集中式 critic）：行 268–302 遍历 `earth.LEO` 各 plane 的卫星，累加每颗 `sendBufferSatsIntra`/`sendBufferSatsInter` 缓冲长度得到全网队列长度数组，取 top-16 拥塞值；行 304–310 追加均值/最大/最小/方差 4 维；行 312–315 把同一份 top-16 复用为「ISL 队列摘要」16 维（行 312 注释自述「粗暴复用」）；行 317–320 追加 4 维硬编码 OD 指示 `[1,1,1,0]`（行 319 注释：占位 one-hot）；行 322–332 追加当前卫星的 plane/sat 归一化编号 4 维（解析 `current_sat_id` 的 `plane_sat` 格式，分别除以 7.0/20.0）。(FACT)
- 输入/输出：入 earth 实例与可选卫星 ID；返回 shape `(44,)` 的 `float32` 数组。任何遍历异常被静默吞掉（行 286–287 回退为 140 个 0）。
- 依赖关系：被 `CODE/SimulationRL.py:7133–7141`（`DDQNAgent.makeDeepAction`，条件 `self.q_global is not None`）调用，带每 50 次决策重算一次的缓存（SimulationRL.py:7134–7152）。

#### `def ppo_clipped_surrogate_loss(old_log_probs, new_log_probs, advantages, clip_eps=0.2)` — CODE/routing_mappo.py:344
- 定位：CODE/routing_mappo.py:344
- 职责：PPO clipped surrogate 目标函数，按公式 `L = −E[min(r·A, clip(r,1±eps)·A)]` 实现（行 353–356，`r = exp(new−old)`）。(FACT)
- 输入/输出：入三个 `tf.Tensor`；返回标量 loss 张量。
- 依赖关系：调用方未确认（CODE 内 grep 无调用点）。

#### `def value_loss_clipped(old_values, new_values, returns, clip_eps=0.2)` — CODE/routing_mappo.py:359
- 定位：CODE/routing_mappo.py:359
- 职责：PPO 的 clipped value loss：`0.5·mean(max((v_new−R)², (v_clip−R)²))`（行 364–367）。(FACT)
- 输入/输出：入三个 `tf.Tensor`；返回标量 loss 张量。
- 依赖关系：调用方未确认（CODE 内 grep 无调用点）。

#### `def gae_advantages(rewards, values, dones, gamma=0.99, lam=0.95)` — CODE/routing_mappo.py:370
- 定位：CODE/routing_mappo.py:370
- 职责：广义优势估计（GAE）：对长度 T 的轨迹反向递推 `δ_t = r_t + γ·V_{t+1}·(1−done) − V_t`、`A_t = δ_t + γλ(1−done)·A_{t+1}`（行 379–386），返回 `(advantages, returns=advs+values[:T])`（行 387–388）。(FACT)
- 输入/输出：入 T 长度 rewards/dones 与 T+1 长度 values（numpy）；返回两个长度 T 的 `float32` 数组。
- 依赖关系：调用方未确认（CODE 内 grep 无调用点）。

#### `class MAPPORolloutBuffer` — CODE/routing_mappo.py:395
- 定位：CODE/routing_mappo.py:395
- 职责：PPO 用的 on-policy rollout 缓冲，按卫星 ID 分桶存 transition 字典（docstring 行 396–411）。(FACT)
- 关键状态/结构：`self.max_steps`、`self._buffers`（`defaultdict(list)`，sat_id → transition 列表）、`self._total`（总计数）（行 413–415）。
- 关键流程/方法：
  - `__init__(max_steps=4096)`（行 412）：初始化上述三个字段。
  - `push(sat_id, transition)`（行 417）：向对应桶追加并 `_total += 1`。
  - `flush_all()`（行 421）：把 `_buffers` 拷成普通 dict 返回，随后重置 `_buffers` 与 `_total`。
  - `is_full()`（行 427）：返回 `_total >= max_steps`。
- 输入/输出：`push` 吃 `(sat_id, dict)`；`flush_all` 吐 `{sat_id: [transition, ...]}`。
- 依赖关系：唯一实例化点是本文件 `RecurrentMAPPOAgent.__init__`（行 494）；`push`/`flush_all`/`is_full` 无外部调用方（CODE 内 grep 无）。

#### `class RecurrentMAPPOAgent` — CODE/routing_mappo.py:435
- 定位：CODE/routing_mappo.py:435
- 职责：完整 MAPPO agent 组合体（GRU actor + 集中式 critic + BP prior + rollout buffer；docstring 行 436–450）。(FACT：组合关系；「完整」为 docstring 自述)
- 关键状态/结构：`self.actor`（GRU actor 模型，行 472–474）、`self.critic`（V 值集中式 critic，行 475）、`self.optimizer`（Adam，行 476）、PPO/GAE 超参数集（行 479–483）、`self.bp`（BackpressurePrior，行 486–488）、`self._hidden_states`（sat_id → GRU 隐状态向量，行 491）、`self.rollout`（MAPPORolloutBuffer，行 494）。
- 关键流程/方法：
  - `__init__(...)`（行 451）：按参数建 actor/critic/optimizer/BP/rollout，初始化隐状态字典。
  - `get_hidden(sat_id)`（行 496）：返回该卫星的 GRU 隐状态，不存在则建零向量。
  - `reset_hidden(sat_id=None)`（行 501）：清空全部或指定卫星的隐状态。
  - `select_action(obs, sat_id, bp_inputs, training=True)`（行 507）：取隐状态→`actor.predict` 单步得 logits 与新隐状态并回存（行 516–522）→ `bp.compute_bp(**bp_inputs)` 后用 `bp.score_actions` 把 BP 融合进 logits（行 525–527）→ `training=True` 时对 softmax 概率采样（含 1e-8 裁剪与重归一，行 530–536），否则 argmax（行 538–540）；返回 `(action, log_prob, score)`。
  - `critic_value(global_state)`（行 544）：`critic.predict` 返回标量 V 值。
  - `train_ppo_update(n_epochs=4, batch_size=256)`（行 551）：函数体只有 `raise NotImplementedError(...)`（行 564–567）——PPO 更新未实现。(FACT)
- 输入/输出：`select_action` 吃单帧 obs + BP 输入字典，吐动作/对数概率/融合分数。
- 依赖关系：调用方未确认（CODE 内 grep 无实例化点）。

#### `class FrameStackBPAgent` — CODE/routing_mappo.py:574
- 定位：CODE/routing_mappo.py:574
- 职责：简化组合体（docstring 行 575–583：不用 GRU、不用 PPO，DDQN + Frame Stack + BP prior + 可选集中式 Q 辅助头）。(FACT)
- 关键状态/结构：`self.K/obs_dim/action_size/enable_global_critic`（行 593–596）、`self.bp`（BackpressurePrior，行 597–599）、`self.global_critic`（`enable_global_critic=True` 时为编译好的 Q 版集中式 critic，MSE + Adam(1e-3)，否则 `None`，行 603–608）。docstring 行 601 注明 frame stack 缓冲由 satellite 自持、本类不存。
- 关键流程/方法：
  - `__init__(frame_stack_k=4, obs_dim=33, action_size=4, bp_beta=0.3, bp_k_progress=0.3, bp_k_loop=1.0, enable_global_critic=False, global_state_dim=GLOBAL_STATE_DIM)`（行 584）：初始化上述字段。
  - `score_actions(q_values, bp_inputs)`（行 610）：`bp.compute_bp(**bp_inputs)` 后 `bp.score_actions(q_values, bp_score)`，返回融合分数。
- 输入/输出：`score_actions` 吃 Q 值与 BP 输入字典，吐 4 维融合分数。
- 依赖关系：调用方未确认（CODE 内 grep 无实例化点；docstring 行 582 自述「由 SimulationRL.py 的 DDQNAgent 代理调用」，但 SimulationRL.py 中实际接线的是直接实例化的 `BackpressurePrior`（行 6268–6273）与 `build_centralized_critic_per_action`（行 6506–6518），未经过本类）。(FACT)

#### `def parse_env_config()` — CODE/routing_mappo.py:622
- 定位：CODE/routing_mappo.py:622
- 职责：从 `SIM_FRAME_STACK_K`/`SIM_BP_BETA`/`SIM_BP_K_PROGRESS`/`SIM_BP_K_LOOP`/`SIM_CRITIC_GLOBAL`/`SIM_MAPPO_MODE` 六个 env 读配置，返回 dict（行 624–631）。(FACT)
- 输入/输出：无参；返回 6 键配置字典。
- 依赖关系：调用方未确认（CODE 内 grep 无调用点；SimulationRL.py 在行 495–501 自行解析同名 env，不经本函数）。(FACT)

---

## 文件 `CODE/routing_multistep.py`（实测 138 行）

模块级说明：
- 模块 docstring（行 1–32）：声明本模块是 n-step DDQN 与 TD(λ) 训练方法基线的「纯多步回报计算」，只改训练目标、部署策略不变；强调纯 numpy、无 simulator import，便于脱离 SimPy 单测；定义了轨迹 dict 格式（`state/action/reward/next_state/is_terminal`）与返回 transition 的五元组契约 `(state, action, target_reward, bootstrap_state, done)`，并说明 n-step 需 `gamma**N` bootstrap、TD(λ) 以 `done=True` 阻止二次 bootstrap。(FACT：docstring 内容)
- imports（行 33）：仅 `numpy`。(FACT)
- docstring 行 13–14 引用的校验脚本 `scripts/diagnostic/verify_multistep.py` 在保留 CODE 树中不存在（glob `CODE/**/verify_multistep*` 无匹配）。(FACT)

#### `def nstep_transitions(traj, gamma, n)` — CODE/routing_multistep.py:36
- 定位：CODE/routing_multistep.py:36
- 职责：离线（整段轨迹）n-step 回报换算。对每跳 k：`k+n ≤ L−1` 时 `R = Σ_{i<n} γ^i·r_{k+i}`、bootstrap 状态取 `traj[k+n]['state']`、`done=False`；窗口越过终点时折扣累加到终点、`bootstrap_state` 为零向量、`done=True`（行 51–65）。空轨迹返回 `[]`（行 46–47）。(FACT)
- 输入/输出：入轨迹 list[dict]、`gamma`、`n`；返回 `(state, action, R, bootstrap_state, done)` 五元组列表（state 为 `float32`）。
- 依赖关系：调用方未确认（CODE 内 grep 无调用点）。SimulationRL.py 的 n-step 路径是在 `DDQNAgent._ms_store`（SimulationRL.py:6980–7012）与 `_ms_flush_lost`（行 7014–7031）内联重写的，未调用本函数。

#### `def nstep_transitions_streaming(traj, gamma, n)` — CODE/routing_multistep.py:69
- 定位：CODE/routing_multistep.py:69
- 职责：流式滑窗版 n-step——用 FIFO 缓冲模拟「窗口一满就发射最老跳的 n-step transition、到终点时把残余 <n 跳全部按终端回报 flush」的在线逻辑（行 85–105）；docstring（行 70–79）自述与 `nstep_transitions` 产出同一 transition 多重集合、仅顺序不同，并定位为「in-sim 滑窗代码可对照验证的纯本地参考」。(FACT)
- 输入/输出：同 `nstep_transitions`。
- 依赖关系：调用方未确认（CODE 内 grep 无调用点）。`CODE/SimulationRL.py:6986`（`_ms_store` docstring）注明 in-sim 滑窗逻辑「validated against routing_multistep.nstep_transitions_streaming (scripts/diagnostic/verify_multistep.py)」——即关系是对照参考而非运行时调用；所引用的校验脚本不在保留 CODE 树中。(FACT)

#### `def lambda_return_transitions(traj, gamma, lam, value_fn)` — CODE/routing_multistep.py:109
- 定位：CODE/routing_multistep.py:109
- 职责：TD(λ) 前视 λ-回报换算。先用 `value_fn`（契约 `V(s)=max_a Q(s,a)`）对每个状态估值（行 123），再对每跳 k 按 docstring 公式（行 113–116）累加各 m-step bootstrap 项与全程 MC 项的 λ 加权（行 125–135），逐跳输出 `(s_k, a_k, G^λ_k, None, True)`——恒 `done=True`、bootstrap 状态为 `None`（行 136–137）。空轨迹返回 `[]`。(FACT)
- 输入/输出：入轨迹、`gamma`、`lam`、`value_fn` 回调；返回五元组列表。
- 依赖关系：被 `CODE/SimulationRL.py:7052` import（`DDQNAgent._tdl_flush`，函数定义在行 7042）并在行 7060 被调用，`value_fn` 为行 7055–7057 定义的 `_vf`（`max_a` 过 `self.qNetwork`）；产出经 `experienceReplay.store` 入池（行 7061）。调用条件：`SIM_TD_LAMBDA>0`（SimulationRL.py:453–459 解析并与 `SIM_NSTEP>1` 互斥）。docstring 引用的单测脚本 `verify_multistep.py` 不在保留 CODE 树中（见模块级说明）。

---

## 文件 `CODE/routing_path_credit.py`（实测 1418 行）

模块级说明：
- 模块 docstring（行 1–26）：声明本模块实现「path-credit mixer 辅助训练（path_credit v1）」——逐跳 MC 回报回归 + 注意力加权信用分配，损失核心式 `L_path = Σ_k α_k·w_k·(q_k − stop_grad(R̃_k))²`；部署时只加载 qNetwork、丢弃 GRU/Transformer/mixer；模块分两部分（纯 Python 的 `PathTrajectoryReplay` 与 TF 部分），TF 为 lazy import 以便无 TF 环境跑 replay 单测。(FACT：docstring 内容；lazy-import 结构在行 317、384、471 等处的函数内 `import tensorflow as tf` 可确认)
- imports（行 27–33）：`__future__.annotations`、`collections`、`random`、`typing.Any`、`numpy`。(FACT)
- 全局常量：`TERMINAL_DELIVERED = "delivered"`（行 40）、`TERMINAL_LOST = "lost"`（行 41）、`TERMINAL_IDX = {delivered: 0, lost: 1}`（行 44，sample() 的 terminal_type 张量编码）。两个字符串常量被 `CODE/SimulationRL.py:10517` 与 `10577` import。(FACT)
- 训练时额外读取的 env：`_train_step_inner`（行 785–787）与 `_train_step_inner_rudder`（行 894–896）经 `__import__('os').environ` 在每次训练步读取 `SIM_PC_QW`（默认 0.3）、`SIM_PC_ALPHA_W`（默认 0.1）、`SIM_PC_W_PRIOR_W`（默认 0.05）作为三项辅助损失权重。(FACT)
- SimulationRL.py 侧配套 env 解析集中在 `CODE/SimulationRL.py:753–797`（`SIM_PATH_CREDIT*`、`SIM_PRED_*` 系列）；`SIM_PATH_CREDIT` 与多步基线（`SIM_NSTEP>1`/`SIM_TD_LAMBDA>0`）在行 754–757 互斥，与 `SIM_CRITIC_GLOBAL` 在行 6454–6458 互斥，与 CSR 在行 6462–6467 互斥。(FACT)
- 行为佐证：`CODE/tests/test_path_credit.py`（行 20–23 import `PathTrajectoryReplay` 与两个 TERMINAL 常量；模块 docstring 行 3–6 注明 replay 测试 1–7 为纯 Python、TF 测试 8–13 gated）；`CODE/tests/test_return_predictor.py:40` import `build_return_predictor`。

#### `class PathTrajectoryReplay` — CODE/routing_path_credit.py:47
- 定位：CODE/routing_path_credit.py:47
- 职责：双桶 FIFO 轨迹回放池——按包的结局（delivered/lost）分桶存完整逐跳轨迹，采样时 50/50 混合并按 `max_hops` 补齐/截断，用 Welford 运行均值按结局类型维护 MC 回报基线（docstring 行 48–65）。(FACT)
- 关键状态/结构：`self.delivered`/`self.lost`（两个 `deque(maxlen=maxlen//2)`，行 69–71）、`self.max_hops`、`self.gamma`（行 72–73）、`self._mean`/`self._count`（按结局类型的 Welford 运行均值与计数，行 76–77）。
- 关键流程/方法：
  - `__init__(maxlen=2000, max_hops=20, gamma=0.99)`（行 67）：`maxlen` 均分两桶，初始化上述字段。
  - `push(traj, terminal, lost_penalty=0.0)`（行 81）：空轨迹或非法 terminal 直接返回（行 91–92）；超长时保留末尾 `max_hops` 跳（行 98）；对每跳 dict 做防御性拷贝、`state`/`next_state` 深拷贝为 `float32`（行 99–105）；lost 轨迹把 `lost_penalty` 加到最后一跳 reward（行 108–110）；自后向前累乘 `γ` 算逐跳 MC 回报 `mc_return` 并写回每条目（行 113–122）；用每个 R_k 更新对应桶的 Welford 均值（行 125–129）；append 进对应桶（行 132–133）。
  - `size()`（行 137）：返回两桶轨迹总数。
  - `baseline(terminal)`（行 140）：返回该结局类型的运行均值（缺省 0.0）。
  - `__len__()`（行 143）：等同 `size()`。
  - `sample(batch_size)`（行 148）：双池空时抛 `RuntimeError`（行 163–165）；尽量 50/50、单桶空时全从另一桶抽（行 168–176）；桶够大则无放回抽样、不够则有放回（行 180–185）；把轨迹填入 `(B,H,D)` 的 `states/actions/mc_returns/mask/terminal_type` 数组（行 194–213）；训练目标 `targets` 取**原始 mc_return** 而非减基线的 advantage（行 215–235，行 216–226 注释给出理由：与 1-step TD 渐近目标一致、避免两个损失互相抵消），`advantages` 字段保留为诊断量；返回 8 键字典（含 `targets`、`baselines_per_traj`，行 237–246）。
- 输入/输出：`push` 吃逐跳 dict 列表 + 结局标签；`sample` 吐 numpy 批量字典。
- 依赖关系：在 `CODE/SimulationRL.py:3416–3425`（`Earth.__init__`，条件 `_SIM_PATH_CREDIT`）实例化为 `earth.pc_replay`（gamma 读 `SIM_GAMMA`，行 3420）。`push`：delivered 端在 `SimulationRL.py:7219`（`makeDeepAction` 目的 GT 分支），lost 端在行 1099（集中 helper `_pc_flush_lost`，定义在行 1066，由行 7120 等丢失点调用），lost_penalty 用 `_SIM_PATH_CREDIT_LOST_PENALTY`（行 1100）。`sample` 在 `SimulationRL.py:7728`（`DDQNAgent.train` 的 path-credit 段，行 7723–7732 门控：`_SIM_PATH_CREDIT` 且 `pc_mixer` 非空且 `size() >= _SIM_PATH_CREDIT_MIN_BUFFER`，每 `EVERY_K` 次一训）。`size()` 另用于行 7726、7757；`baseline()` 与 `max_hops`/`gamma` 属性在 `_save_pc_replay`（行 10520、10550–10552）被读；`_mean` 在 `_load_pc_replay_into`（行 10584–10586）被直接写。测试：`CODE/tests/test_path_credit.py`（如行 58 起 `TestReplay`）。

#### `def sinusoidal_position_encoding(max_hops, d_model)` — CODE/routing_path_credit.py:253
- 定位：CODE/routing_path_credit.py:253
- 职责：标准 Transformer 正弦位置编码表：偶数维 sin、奇数维 cos，`pos/10000^(2·(i//2)/d_model)`（行 256–262）。(FACT)
- 输入/输出：入序列长与模型维；返回 `(max_hops, d_model)` 的 `float32` numpy 数组。
- 依赖关系：被本文件 `PathCreditMixer.__init__`（行 431）与 `ReturnPredictor.__init__`（行 1057）调用；无 CODE 内其他调用方。

#### `def build_path_credit_mixer(state_dim, n_actions, d_model=64, ..., force_unit_w=False)` — CODE/routing_path_credit.py:269
- 定位：CODE/routing_path_credit.py:269
- 职责：工厂函数——lazy import TF（行 317）后把所有参数透传构造 `PathCreditMixer`（行 318–338）。docstring（行 290–316）说明 `use_gru=False` 时用正弦位置编码替代 GRU、`mode` 选 `'attention'`（PRD-A）或 `'rudder'`（PRD-T）、`pred_*` 仅 rudder 模式有效、`force_uniform_alpha`/`force_unit_w` 为消融开关（前向保留、输出被覆写）。(FACT)
- 输入/输出：入结构/超参；返回 `PathCreditMixer` 实例。
- 依赖关系：被 `CODE/SimulationRL.py:6540–6560`（`DDQNAgent.__init__`，条件 `_SIM_PATH_CREDIT`，行 6538）调用，产物存 `self.pc_mixer`；被 `CODE/tests/test_return_predictor.py:168` 与 `CODE/tests/test_path_credit.py:235` 调用。

#### `class PathCreditMixer` — CODE/routing_path_credit.py:341
- 定位：CODE/routing_path_credit.py:341
- 职责：token 编码 + （可选 GRU 或位置编码）+ 多头自注意力 + 双信用头（α、w）的辅助训练模块；组合量 `Q_path = Σ α·w·q`（q 来自被训的 qNetwork，梯度贯通），主损失为 `Q_path` 对全路径折扣回报的 Huber 回归（docstring 行 342–360）。(FACT)
- 关键状态/结构：超参数集（`state_dim/n_actions/d_model/gru_units/n_heads/max_hops/action_emb_dim/gpath_clip/use_gru`，行 388–396）；`mode`（`'attention'|'rudder'`，行 399–402，非法值抛 `ValueError`）与 `pred_warmup_steps`、`_pc_train_count` 训练步计数（行 403–404）；`pred_contrib_mode`（`'attention'|'increment'`，行 409–414）；`self.predictor`（仅 `mode=='rudder'` 时惰性挂一个 `ReturnPredictor`，否则 `None`，行 417–428）；`self._pe`（正弦位置编码常量，行 431–432）；Keras 层：`action_emb`（Embedding）、`token_proj`（Dense+relu）、可选 `gru`、`transformer`（MultiHeadAttention）、`alpha_proj`、`w_proj`（Dense(1)）（行 435–455）；`self.optimizer`（独立 Adam，带 clipnorm=1.0，行 462）；`self._tf_train_step`/`self._captured_q`/`self._retrace_count`（tf.function 缓存，行 465–466、651–652）。
- 关键流程/方法：
  - `__init__(...)`（行 362）：落盘超参与开关、按需建 `ReturnPredictor`、建全部 Keras 层、跑 `_build_once` 实体化权重、建独立优化器。
  - `_build_once()`（行 470）：用全零 dummy 输入跑一遍前向（行 473–492），使各层 `trainable_variables` 就位。
  - `trainable_variables`（property，行 494/495）：汇总 action_emb/token_proj/transformer/alpha_proj/w_proj（及可选 gru）的可训练变量列表（行 496–505）。
  - `_forward(q_network, states, actions, mask)`（行 509）：拍平批次经 `q_network` 得逐动作 Q，按 one-hot 取出所执行动作的 `q_k`（梯度通 qNetwork，行 526–531）；`stop_gradient(q_k)` 与 state/action 嵌入拼 token（行 534–537）；GRU 或「token+正弦 PE」进 MultiHeadAttention（带 `mask∧mask^T` 注意力掩码，行 540–550）；`alpha_proj` logits 经 −1e9 掩码后 softmax 得 α（行 553–556），`force_uniform_alpha` 时覆写为掩码感知的均匀分布（行 564–568）；`w_proj` 经 softplus 得 w（行 571），`force_unit_w` 时覆写为有效跳 1/填充 0（行 577–579）；返回 `(q_k, alpha, w)`。
  - `train_step(q_network, batch, lambda_path=0.1)`（行 585）：把 batch 各字段转 tensor（行 611–616）、`_pc_train_count += 1`；rudder 模式先用同批数据训 predictor（`predictor.train_step`，行 627），过 warmup 后取 `predictor.compute_contribution` 作为外部 α 软目标（行 630–634），warmup 期传零占位 + `ext_active=False`（行 656–660）；按模式把 `_train_step_inner` 或 `_train_step_inner_rudder` 包成带 `input_signature` 的 `tf.function`（行 637–684）并执行；汇总 10 项标量指标（α 熵、q_mean、w_mean、各分项损失、α 最大值、w 标准差、Q_path/G_path 均值），rudder 时并带 `pred_*` 前缀的 predictor 指标（行 686–701）；返回 `(loss, metrics)`。
  - `_train_step_inner(states, actions, targets, mask, lambda_path)`（行 703，PRD-A）：GradientTape 内 `_forward` 得 `(q_k, α, w)`；`G_path` 取 hop-0 的 mc_return、`stop_gradient` 并 clip 到 `±gpath_clip`（行 737–739，行 727–736 注释记录了一次未 clip 导致发散的失败案例）；`Q_path = Σ α·w·q_k·mask`（行 740）；`L_path_global` 为 δ=50 的 Huber（行 742–748）；`L_q` 为 α/w 停梯度加权的逐跳 MC 回报 MSE（行 755–763）；`L_alpha` 为 α 对「逐跳平方误差归一化分布」的交叉熵（行 767–773）；`L_w_prior` 为 `(w−1)²` 锚（行 776–779）；总损失 `L_path = L_path_global + Q_W·L_q + ALPHA_W·L_alpha + W_PRIOR_W·L_w_prior`，乘 `lambda_path`（行 785–789）；对 qNetwork + mixer 全部变量求梯度、过滤 None 后用自有优化器更新（行 791–795）；返回损失与 10 项指标（行 798–814）。
  - `_train_step_inner_rudder(..., alpha_tilde_external, lambda_path, ext_active)`（行 816，PRD-T）：与 `_train_step_inner` 相同，唯一差异是 `L_alpha` 的软目标用 `tf.cond(ext_active, ...)` 在外部 RUDDER 贡献增量（停梯度、掩码后重归一，行 871–874）与残差归一化回退之间切换（行 877–881）。
  - `save_weights(path)`（行 925）：把 mixer 各层（含可选 GRU，**不含 qNetwork**——行 926 注释）按 `层名__序号` 键存 `np.savez_compressed`（行 927–940）。
  - `load_weights(path)`（行 942）：按同一键约定从 npz 读回并 `set_weights`（行 943–960）。
- 输入/输出：`train_step` 吃 qNetwork + `PathTrajectoryReplay.sample()` 的 batch 字典，吐 `(loss float, metrics dict)`。
- 依赖关系：实例化见 `build_path_credit_mixer`（SimulationRL.py:6540–6560 → `self.pc_mixer`）。`train_step` 在 `SimulationRL.py:7729–7732`（`DDQNAgent.train`）被调用，传入 `self.qNetwork`；`save_weights` 在行 11375（interrupt-save）被调用；`load_weights` 在行 12138（warm-start resume，经 `attempt_checkpoint_load`，env `SIM_PC_MIXER_PATH` 提供路径）被调用。类内引用 `ReturnPredictor`（行 419）。

#### `def build_return_predictor(state_dim, n_actions, d_model=64, ..., dropout=0.0)` — CODE/routing_path_credit.py:988
- 定位：CODE/routing_path_credit.py:988
- 职责：工厂函数——lazy import TF（行 1000）后透传构造 `ReturnPredictor`（行 1001–1011）。(FACT)
- 输入/输出：入结构/超参；返回 `ReturnPredictor` 实例。
- 依赖关系：被 `CODE/tests/test_return_predictor.py:40`、`149` 调用；CODE 内生产代码无调用点（`PathCreditMixer` 在行 419 直接实例化 `ReturnPredictor`，不经本工厂）。(FACT)

#### `class ReturnPredictor` — CODE/routing_path_credit.py:1014
- 定位：CODE/routing_path_credit.py:1014
- 职责：因果 Transformer 编码器，在每个前缀位置预测整条路径的总折扣回报 G_0，用于 RUDDER 风格贡献分解（PRD-T 模式的 α 软目标来源；类前注释行 963–986 与 docstring 行 1015–1031）。贡献定义 `c_k = |g0_hat^k − g0_hat^(k−1)|`（`g0_hat^{−1}:=0`），归一化后得 `alpha_tilde`。(FACT)
- 关键状态/结构：超参数集（行 1047–1054）；`self._pe`（正弦位置编码常量，行 1057–1058）；`self.action_emb`、`self.token_proj`（行 1061–1069）；`self.encoder_layers`（n_layers 个 dict，各含 `mha`/`ln1`/`ffn1`/`ffn2`/`ln2` 五个子层，行 1072–1086）；`self.head`（Dense(1) 标量预测头，行 1089）；`self.optimizer`（独立 Adam，clipnorm=1.0，行 1095）；`self._tf_train_step`/`self._tf_predict`（tf.function 缓存，行 1097–1098）。
- 关键流程/方法：
  - `__init__(state_dim, n_actions, d_model=64, n_heads=4, n_layers=2, max_hops=20, lr=1e-4, action_emb_dim=8, dropout=0.0)`（行 1033）：建层、`_build_once` 实体化、建优化器。
  - `_build_once()`（行 1100）：全零 dummy 前向一遍以实体化权重（行 1103–1107）。
  - `trainable_variables`（property，行 1109/1110）：汇总 action_emb/token_proj/head 与各编码器子层的可训练变量（行 1111–1125）。
  - `_make_causal_mask(H, key_mask)`（行 1127）：生成 `(B,H,H)` 布尔注意力掩码 = 下三角因果掩码 ∧ key 有效性（行 1142–1146）。
  - `_forward(states, actions, mask, training=False, return_attention=False)`（行 1148）：`[state, action_emb]` 拼 token → Dense+relu → 加 PE（行 1169–1172）；逐编码器层做带因果掩码的 MHA + 残差/LN + FFN + 残差/LN（行 1177–1196），`return_attention=True` 时收集各层注意力权重；`head` 输出 squeeze 成 `(B,H)` 的 `g0_hat`（行 1198–1201）。
  - `predict_g0(states, actions, mask)`（行 1203）：eager 前向封装（转 tensor 后调 `_forward`），返回 `(B,H)`。
  - `_attention_contribution(attn_scores_per_layer, mask)`（行 1211）：SECRET 风格读出——取最后一层注意力、按头取均值、以「最后一个有效位置」为 query 取其对各 key 的注意力分布（`tf.gather(..., batch_dims=1)`，行 1232–1243），乘掩码后重归一，得 `(B,H)` 的 `alpha_tilde`。
  - `compute_contribution(states, actions, mask, mode="increment")`（行 1254）：`mode='attention'` 时走 `_forward(return_attention=True)` + `_attention_contribution`（行 1280–1291）；`mode='increment'` 时算相邻前缀 `g0_hat` 差分的绝对值、掩码后按行归一（行 1294–1303）；两模式都在行贡献和退化（<2e-6）时回退为掩码均匀分布（行 1289–1290、1305–1310）；`mode` 非法抛 `ValueError`（行 1276–1278）。
  - `train_step(states, actions, mask, g0_true)`（行 1313）：把 `_train_step_inner` 包成带 `input_signature` 的 `tf.function`（行 1334–1343）执行，返回 `{L_pred, g0_mae, contribution_entropy}` 三项 float 指标（行 1345–1350）。
  - `_train_step_inner(states, actions, mask, g0_true)`（行 1352）：GradientTape 内前向得 `g0_hat`，`L_pred` = 掩码内 `(g0_hat − G_0)²` 均值（G_0 广播到逐前缀，行 1355–1362）；用自有优化器更新自身变量（行 1364–1367）；另算 MAE 与贡献熵诊断量（行 1370–1378）。
  - `save_weights(path)`（行 1381）：把 action_emb/token_proj/head 及各编码器子层按 `rp_*__序号` 键存 npz（行 1382–1394）。
  - `load_weights(path)`（行 1396）：按同键约定读回 `set_weights`（行 1397–1418）。
- 输入/输出：`train_step` 吃 `(B,H,D)` states、`(B,H)` actions/mask、`(B,)` 的 G_0 真值，吐指标 dict；`compute_contribution` 吐 `(B,H)` 归一化 `alpha_tilde`。
- 依赖关系：被本文件 `PathCreditMixer.__init__`（行 419，`mode=='rudder'` 时）实例化；`train_step`/`compute_contribution` 被 `PathCreditMixer.train_step`（行 627、631–633）调用；`predict_g0` 仅被 `CODE/tests/test_return_predictor.py`（行 63、73、77、147、155）调用；`save_weights`/`load_weights` 调用方未确认（CODE 生产代码 grep 无调用点——SimulationRL.py 的 resume/save 只覆盖 mixer 与 replay，见行 11375、12138）。
# 旧平台依赖模块组说明书片段（o3-misc-modules）

覆盖文件：`CODE/link_outage.py`、`CODE/temporal_encoder.py`、`CODE/legacy_trace_runtime.py`、`CODE/monitor.py`、`CODE/runtime_effect_receipt.py`。行数均为 `wc -l` 实测。调用方行号均来自对 `CODE/SimulationRL.py`、`CODE/run.py`、`CODE/leo_sim/comparison.py` 的 grep 实证。

---

### 文件 `CODE/link_outage.py`（实测 197 行）

模块级说明：
- 行 1-8：模块 docstring，自述为「Gilbert-Elliott 风格两状态 Markov 链路中断调度器」，声明该模块为 opt-in：无 outage 配置时不动旧传输路径，中断区间由 run seed 派生的私有 RNG 惰性生成，并声明「不是校准过的 Starlink 模型」(FACT，docstring 声明)。
- 行 10-18：imports：`__future__.annotations`、`copy`、`hashlib`、`json`、`os`、`typing.{Any,Dict,List,Optional,Tuple}`、`numpy as np` (FACT)。
- 行 21-25：全局常量 `DEFAULT_LINKS`：三类链路的默认参数 —— `gsl_uplink` 与 `gsl_downlink` 为 `mean_good_s=15.0, mean_bad_s=0.05`，`isl` 为 `mean_good_s=60.0, mean_bad_s=0.2` (FACT)。
- 模块级不读 env；env 读取发生在 `load_link_outage_schedule_from_env` 函数体内（行 170、189-191）(FACT)。

#### `def canonical_json_sha256(value)` — CODE/link_outage.py:28
- 定位：CODE/link_outage.py:28-30
- 职责：把任意可 JSON 序列化的值规范化序列化（`sort_keys=True`、紧凑分隔符、非 ASCII 不转义）后取 SHA-256 十六进制摘要 (FACT)。
- 输入/输出：任意值 → 64 字符 hex 字符串。
- 依赖关系：被本文件 `__init__`(行 90) 与 `load_link_outage_schedule_from_env`(行 188) 调用；被测试 `CODE/tests/test_link_outage.py:96,99` 使用。注意 `CODE/traffic_burst.py:38` 存在一个同名独立实现，`CODE/SimulationRL.py:50` 有私有 `_canonical_json_sha256`，三者不是同一函数 (FACT)。

#### `def resource_class(resource_id)` — CODE/link_outage.py:33
- 定位：CODE/link_outage.py:33-39
- 职责：把资源 id 映射到链路类别 (FACT)。规则：`rid` 以 `"GW:"` 开头 → `"gsl_uplink"`（行 35-36）；`rid` 含子串 `"downlink"` → `"gsl_downlink"`（行 37-38）；其余 → `"isl"`（行 39）(FACT)。
- 输入/输出：字符串 → 三个类别字符串之一。
- 依赖关系：被本文件 `_params`(行 93) 调用；被测试 `CODE/tests/test_link_outage.py:22`（`test_resource_class_mapping`）覆盖。调用方传入的 rid 实例见 `CODE/SimulationRL.py:2762`（`f"GW:{self.name}:uplink"`）(FACT)。

#### `def _positive_float(value, default)` — CODE/link_outage.py:42
- 定位：CODE/link_outage.py:42-47
- 职责：把值转为正 float；转换失败（TypeError/ValueError）或结果 ≤0 时返回 `default` (FACT)。
- 输入/输出：任意值 + 默认 float → 正 float。
- 依赖关系：被本文件 `LinkOutageSchedule.__init__`(行 75-80) 调用；文件内私有（名字带下划线），跨文件调用方未确认。

#### `class LinkOutageSchedule` — CODE/link_outage.py:50
- 定位：CODE/link_outage.py:50-163
- 职责：按资源维度维护 good/bad 交替的中断区间序列，区间用私有 RNG 按需惰性生成 (FACT)。
- 关键状态/结构：`self.cfg`（配置副本，行 54）、`self.mode`（行 55）、`self.run_seed`/`self.seed`（行 64-65）、`self._rng`（`np.random.default_rng`，行 66）、`self.links`（三类链路参数，行 69-80）、`self._intervals`（`Dict[str, List[Tuple[float,float]]]`，每资源的中断区间列表，行 82）、`self.stats`（五个计数器：evaluations / bad_interval_checks / intervals_generated / start_down_waits / mid_transmission_losses，行 83-89）、`self.config_sha256`（行 90）。
- 关键流程/方法：
  - `__init__(cfg, *, run_seed=42)`（行 53)：校验 `mode=="gilbert_elliott"`，否则 `ValueError`（行 56-59）；`seed = run_seed + seed_offset`（`seed_offset` 解析失败按 0，行 60-65）；建私有 RNG（行 66）；以 `DEFAULT_LINKS` 深拷贝为底、叠加 `cfg["links"]` 中已知类别的正数参数，未知类别跳过（行 68-80）；初始化区间表与计数器（行 82-89）；算 `config_sha256`（行 90）。
  - `_params(resource_id)`（行 92)：经 `resource_class` 取该类 `(mean_good_s, mean_bad_s)`（行 93-95）。
  - `_ensure_until(resource_id, t)`（行 97)：惰性生成区间直到覆盖时刻 `t`：循环从指数分布采 `good`/`bad` 时长（行 103-104），把 `(start,end)` 追加到该资源区间表并累计 `intervals_generated`（行 105-109）。
  - `first_outage_in(resource_id, t0, t1)`（行 111)：`t1<=t0` 直接返回 `None`（行 117-118）；`evaluations` 计数 +1（行 119）；`_ensure_until` 后扫描区间表，返回第一个与 `[t0,t1)` 相交的 bad 区间，返回 dict 含 `rid/start/end/overlap_start/overlap_end` 并累计 `bad_interval_checks`（行 121-137）；无相交返回 `None`（行 138）。
  - `is_down_at(resource_id, t)`（行 140)：`_ensure_until` 后判断 `t` 是否落在任一 bad 区间内，返回 bool（行 141-149）。
  - `record_start_down_wait()`（行 151)：`stats["start_down_waits"] += 1`。
  - `record_mid_transmission_loss()`（行 154)：`stats["mid_transmission_losses"] += 1`。
  - `summary()`（行 157)：返回 `{mode, seed, links 深拷贝, stats 副本}`（行 158-163）。
- 输入/输出：构造输入为配置 dict 与 run seed；查询接口输入资源 id + 时刻/区间，输出中断区间 dict 或 bool；`summary()` 输出状态 dict。
- 依赖关系：实例由 `CODE/SimulationRL.py:3398-3401`（`Earth.__init__`，类定义在 `CODE/SimulationRL.py:3322`）经 `load_link_outage_schedule_from_env` 创建，挂在 `earth._link_outage`。`first_outage_in` 被 `Satellite.sendBlock`（`CODE/SimulationRL.py:2271-2273`，方法起于 2185，类起于 1891）与 `Gateway.sendBlock`（`CODE/SimulationRL.py:2761-2765`，方法起于 2718，类起于 2573）调用；`record_start_down_wait`/`record_mid_transmission_loss` 在 `CODE/SimulationRL.py:2275,2285` 与 `2767,2777` 调用；`stats` 被 receipt 段 `CODE/SimulationRL.py:10876-10879` 读取。`summary()` 与 `is_down_at` 的调用方未确认（对 `CODE/SimulationRL.py` grep 无匹配）。测试佐证：`CODE/tests/test_link_outage.py:38`（私有种子区间可复现）、`:54`（`first_outage_in` 返回交集）、`:69`（两个计数器显式累加）。

#### `def load_link_outage_schedule_from_env(*, run_seed=42, fail_closed=True)` — CODE/link_outage.py:166
- 定位：CODE/link_outage.py:166-197
- 职责：从 env 变量 `SIM_LINK_INTERRUPTION_CONFIG`（行 170）指向的 JSON 文件加载中断配置并构造 `LinkOutageSchedule` (FACT)。
- 关键流程：env 为空 → 返回 `None`（行 171-172）；文件不存在 → `fail_closed` 时抛 `RuntimeError`，否则返回 `None`（行 174-179）；JSON 解析失败同样按 `fail_closed` 分支（行 180-186）；若 env `SIM_EXPECTED_LINK_INTERRUPTION_CONFIG_SHA256`（行 189-191）非空且与配置实际摘要不一致 → 抛 `RuntimeError`（行 192-196）；成功则返回 `LinkOutageSchedule(cfg, run_seed=run_seed)`（行 197）。
- 输入/输出：无位置参数（仅关键字 `run_seed`、`fail_closed`）→ `LinkOutageSchedule` 或 `None`。
- 依赖关系：调用方为 `CODE/SimulationRL.py:3398-3401`（`Earth.__init__`，传入 `run_seed=_SEED, fail_closed=_SIM_FAIL_CLOSED`）。测试佐证：`CODE/tests/test_link_outage.py:29`（默认禁用）、`:77`（SHA 不匹配拒绝）。

---

### 文件 `CODE/temporal_encoder.py`（实测 272 行）

模块级说明：
- 行 1-41：模块 docstring，自述为「每卫星决策时刻时间记忆」模块，声明三种模式（`none`/`framestack`/`gru`，由 env `SIM_TEMPORAL_MODE` 选择）、与 MAPPO frame-stack 互斥、以及在 `SimulationRL.py` 的 hook 点 (FACT，docstring 声明；docstring 内的行号引用如 `createModel @5841`、`_apply_frame_stack @7465` 未逐条核实）。
- 行 43-45：imports：`os`、`collections`、`numpy as np` (FACT)。
- 行 48-64：import 时一次性读取的 env 全局配置 (FACT)：`_MODE`=`SIM_TEMPORAL_MODE` 默认 `"none"`（行 48）；`_K`=`SIM_TEMPORAL_K` 默认 4（行 49）；`_GRU_UNITS`=`SIM_TEMPORAL_GRU_UNITS` 默认 32（行 50）；`_MODE` 不在 `("none","framestack","gru")` 时 import 即抛 `ValueError`（行 52-54）；GRU 超参 `_GRU_BURN_IN`(57)、`_GRU_SEQ_LEN`(58)、`_GRU_TRAIN_EVERY`(59)、`_GRU_BATCH`(60)、`_GRU_MIN_BUF`(61)、`_GRU_BUF_MAX`(62)、`_GRU_LR`(63)，分别来自 `SIM_TEMPORAL_BURN_IN/SEQ_LEN/EVERY_K/BATCH/MIN_BUF/BUF_MAXLEN/LR`；`_GRU_IS_EVAL` = (`SIM_RL_EVAL == "1"`)（行 64）。
- 行 66-72：**模块级全局状态**（任务要求说明项，FACT）：`_gru_layer`（`tf.keras.layers.GRU`，行 67）、`_gru_pred`（`Dense` 预测头，行 68）、`_gru_opt`（独立 Adam 优化器，行 69）三个惰性构建的全局对象；`_gru_seq_replay = collections.deque(maxlen=_GRU_BUF_MAX)`（跨卫星共享的序列回放缓冲，行 70）；`_gru_calls = 0`（apply 调用计数，行 71）；`_gru_last_loss = None`（最近一次自监督 loss，行 72）。行 66 注释声明该 GRU 在所有卫星间共享参数 (FACT，注释声明；代码上确实只有一份全局层对象）。
- 本模块无 class；每卫星的状态（`_te_frame_buf`、`_te_hidden`、`_te_seqbuf`）挂在传入的 `sat` 对象属性上 (FACT，见行 118-121、144-145、196、207-208)。

#### `def mode()` — CODE/temporal_encoder.py:75
- 定位：CODE/temporal_encoder.py:75-77。职责：返回当前 `_MODE` 字符串 (FACT)。输入/输出：无参 → str。调用方：`CODE/SimulationRL.py:6258`（打印）、`6613`（判断是否 gru eval）、`9490`（`_temporal_apply` 内判断是否 active）、`11072`（receipt）。

#### `def temporal_enabled()` — CODE/temporal_encoder.py:80
- 定位：CODE/temporal_encoder.py:80-82。职责：`_MODE in ("framestack","gru")` 时返回 True（即 encoder 会改变状态维度）(FACT)。输入/输出：无参 → bool。调用方：`CODE/SimulationRL.py:5264`（`Earth.moveConstellation`）、`6255`（`DDQNAgent.__init__`）。

#### `def output_dim(base_dim)` — CODE/temporal_encoder.py:85
- 定位：CODE/temporal_encoder.py:85-97。职责：给出当前模式下 Q 网输入维度 (FACT)：`framestack` → `base_dim * _K`（行 93-94）；`gru` → `base_dim + _GRU_UNITS`（行 95-96）；否则 → `base_dim`（行 97）。输入/输出：int → int。调用方：`CODE/SimulationRL.py:6256`（设置 `self.stateSize`）。

#### `def assert_not_conflicting_with_mappo(mappo_mode)` — CODE/temporal_encoder.py:100
- 定位：CODE/temporal_encoder.py:100-108。职责：`mappo_mode` 属于 `("framestack_bp","full_recurrent","bp_only")` 且本模块 enabled 时抛 `RuntimeError`（两者都改写状态，行 103-108）(FACT)。输入/输出：str → 无返回值或异常。调用方：`CODE/SimulationRL.py:6254`（`DDQNAgent.__init__`）。测试佐证：`CODE/tests/test_temporal_encoder.py:107`（`test_mappo_conflict_guard`）。

#### `def reset_satellite(sat)` — CODE/temporal_encoder.py:111
- 定位：CODE/temporal_encoder.py:111-121。职责：清空该卫星的 `_te_frame_buf`（行 118-119）并把 `_te_hidden` 置 `None`（行 120-121）(FACT)；docstring 声明用于 ISL handoff 后丢弃过时记忆 (FACT，docstring 声明）。输入/输出：sat 对象 → 原地修改，无返回。调用方：`CODE/SimulationRL.py:5263-5267`（`Earth.moveConstellation`，方法起于 5183，在 ISL handoff 后对全部卫星调用；该调用被 `temporal_enabled()` 门控）。测试佐证：`CODE/tests/test_temporal_encoder.py:94,135`。

#### `def apply(sat, state)` — CODE/temporal_encoder.py:124
- 定位：CODE/temporal_encoder.py:124-138。职责：决策 hook (FACT)：`none` 模式原样返回输入（行 131-132）；否则把 state 展平为 float32 向量（行 133），按模式分派到 `_apply_framestack`（行 135）或 `_apply_gru`（行 137）。输入/输出：`(1, base_dim)` 或 `(base_dim,)` 数组 → `(1, output_dim)` 数组（`none` 时原样）。调用方：`CODE/SimulationRL.py:9484`（模块级包装 `_temporal_apply`，函数起于 9469，带 `_TE_MODULE` 缓存 9466/9475-9480 与失败计数 9485-9488），实际 hook 点在 `DDQNAgent.makeDeepAction` 的 `CODE/SimulationRL.py:7126`（`newState = _temporal_apply(sat, newState)`）。测试佐证：`CODE/tests/test_temporal_encoder.py:41`（none 直通）、`:83`（两种输入形状）。

#### `def _apply_framestack(sat, flat)` — CODE/temporal_encoder.py:141
- 定位：CODE/temporal_encoder.py:141-149。职责：在 `sat._te_frame_buf`（`deque(maxlen=_K)`，惰性创建，行 144-145）追加当前帧（行 146），不足 K 帧时用首帧向左补齐（行 147-148），拼接为 `(1, K*base_dim)`（行 149）(FACT)。输入/输出：sat + 1D float32 向量 → `(1, K*base_dim)` 数组。调用方：本文件 `apply`(行 135)。测试佐证：`CODE/tests/test_temporal_encoder.py:54`（维度与窗口行为）。

#### `def _build_gru(base_dim)` — CODE/temporal_encoder.py:170
- 定位：CODE/temporal_encoder.py:170-180。职责：惰性构建全局 GRU（`return_sequences=True, return_state=True`，行 175-177）、`Dense(base_dim)` 下一帧预测头（行 178-179）、学习率 `_GRU_LR` 的 Adam（行 180），写入全局 `_gru_layer/_gru_pred/_gru_opt`（行 173）(FACT)；tensorflow 在函数体内 import（行 174）。输入/输出：int → 无返回（写全局）。调用方：本文件 `_apply_gru`(行 188)、`_train_gru_step`(行 224)、`load`(行 261)。

#### `def _apply_gru(sat, flat)` — CODE/temporal_encoder.py:183
- 定位：CODE/temporal_encoder.py:183-202。职责：用该卫星当前帧单步推进共享 GRU (FACT)：`sat._te_hidden` 缺省取零向量（行 189-191）；以 `(B=1,T=1,base)` 形状单步调用 GRU（行 192-195）；新 hidden 存回 `sat._te_hidden`（行 196）；非 eval（`_GRU_IS_EVAL` 为假）时调用 `_record_gru` 并每 `_GRU_TRAIN_EVERY` 次触发一次 `_train_gru_step`（行 197-201）；返回 `concat(flat, h)` 的 `(1, base+units)` 数组（行 202）。调用方：本文件 `apply`(行 137)。测试佐证：`CODE/tests/test_temporal_gru.py:47`。

#### `def _record_gru(sat, flat)` — CODE/temporal_encoder.py:205
- 定位：CODE/temporal_encoder.py:205-211。职责：维护 `sat._te_seqbuf`（`deque(maxlen=_GRU_SEQ_LEN)`，行 207-209），窗口满时把 `(SEQ_LEN, base)` 序列 `np.stack` 后放入全局 `_gru_seq_replay`（行 210-211）(FACT)。输入/输出：sat + 向量 → 无返回。调用方：本文件 `_apply_gru`(行 198)。

#### `def _train_gru_step()` — CODE/temporal_encoder.py:214
- 定位：CODE/temporal_encoder.py:214-239。职责：执行一步自监督训练 (FACT)：缓冲不足 `_GRU_MIN_BUF` 返回 `None`（行 218-219）；随机抽 batch（行 220-222）；burn-in 长度 `bi=min(_GRU_BURN_IN, _GRU_SEQ_LEN-2)`（行 227）；`GradientTape` 下全序列前向（行 229），用第 `[bi, L-2]` 步的 hidden 预测第 `[bi+1, L-1]` 帧（行 231-233），MSE loss（行 234）；对 GRU + 预测头的可训练变量 `apply_gradients`（行 235-237）；把 loss 存入全局 `_gru_last_loss` 并返回（行 238-239）。输入/输出：无参 → float 或 None。调用方：本文件 `_apply_gru`(行 201)。测试佐证：`CODE/tests/test_temporal_gru.py:62`（自监督训练使 loss 下降）。

#### `def save(path_dir)` — CODE/temporal_encoder.py:242
- 定位：CODE/temporal_encoder.py:242-251。职责：GRU 未构建时返回 `False`（行 245-246）；否则把 GRU 与预测头权重写入 `<path_dir>/temporal_gru.npz`，附带 `n_cell` 记录 GRU 权重张量数（行 248-250），返回 `True`（行 251）(FACT)。输入/输出：目录路径 str → bool。调用方：`CODE/SimulationRL.py:10457-10458`（顶层函数 `saveDeepNetworks`，起于 10447）。测试佐证：`CODE/tests/test_temporal_gru.py:90`（save/load 往返）。

#### `def load(path_dir, base_dim)` — CODE/temporal_encoder.py:254
- 定位：CODE/temporal_encoder.py:254-267。职责：`temporal_gru.npz` 不存在返回 `False`（行 257-259）；GRU 未构建则先 `_build_gru`（行 260-261）；按 `n_cell` 切分数组并 `set_weights` 到 GRU 与预测头（行 262-266）；返回 `True`（行 267）(FACT)。输入/输出：目录 str + int → bool。调用方：`CODE/SimulationRL.py:6621`（`DDQNAgent.__init__` 的 gru eval 分支，经 `attempt_checkpoint_load` 包装，见 6611-6624）。

#### `def last_train_loss()` — CODE/temporal_encoder.py:270
- 定位：CODE/temporal_encoder.py:270-272。职责：返回全局 `_gru_last_loss` (FACT)。输入/输出：无参 → float 或 None。调用方：`CODE/SimulationRL.py:11071`（`_run_audit_meta`，起于 10702，用于 temporal receipt）。

跨文件配置方：`CODE/run.py:853-875` 把 config 的 `temporal.*` 字段映射为上述 `SIM_TEMPORAL_*` env 变量并校验 mode 合法（run.py 不 import 本模块，只设 env）(FACT)。

---

### 文件 `CODE/legacy_trace_runtime.py`（实测 138 行）

模块级说明：
- 行 1-7：模块 docstring，自述为「保留的 Gateway runtime 的 immutable-demand 适配器」，声明本模块不含仿真进程逻辑，只做 trace 校验与地理网格到 Gateway 集合的投影 (FACT，docstring 声明）。
- 行 8-13：imports：`__future__.annotations`、`hashlib`、`math`、`pathlib.Path`、`typing.{Any,Sequence}` (FACT)。
- 行 15-20：双模式 import (FACT)：先尝试 `from leo_sim.grid import grid_center` 与 `from leo_sim.trace import TraceError, load_trace`（行 16-17），`ModuleNotFoundError` 时回退 `from CODE.leo_sim.*`（行 19-20）；行 15 注释说明原因（SimulationRL 从 CODE 目录执行，包 CLI 走 `CODE.*`）。
- 无模块级 env 读取、无全局可变状态 (FACT)。

#### `class LegacyTraceError(ValueError)` — CODE/legacy_trace_runtime.py:23
- 定位：CODE/legacy_trace_runtime.py:23-24
- 职责：`ValueError` 子类，作为本模块所有校验失败的异常类型 (FACT)；docstring（行 24）声明「trace 无法被保留 runtime 诚实表示」。无任何方法或状态。
- 输入/输出：异常消息 str。
- 依赖关系：被本文件行 76、79、82、85、94、113、117 抛出；被测试 `CODE/tests/test_legacy_trace_runtime.py:14` import 并用于断言。

#### `def _haversine_km(lat1, lon1, lat2, lon2)` — CODE/legacy_trace_runtime.py:27
- 定位：CODE/legacy_trace_runtime.py:27-33。职责：用 haversine 公式（地球半径 6371.0 km，行 28）算两点大圆距离 (FACT)。输入/输出：四个 float（度）→ 距离 km float。调用方：本文件 `_nearest_gateway`(行 48)。

#### `def _sha256(path)` — CODE/legacy_trace_runtime.py:36
- 定位：CODE/legacy_trace_runtime.py:36-41。职责：以 1 MiB 分块流式读取文件并计算 SHA-256 hex 摘要 (FACT)。输入/输出：`Path` → 64 字符 hex str。调用方：本文件 `load_and_project_trace`(行 80)。

#### `def _nearest_gateway(grid_id, gateways)` — CODE/legacy_trace_runtime.py:44
- 定位：CODE/legacy_trace_runtime.py:44-55。职责：取 `grid_center(grid_id)` 的经纬（行 45），对每个 gateway 算 haversine 距离（行 46-53），按 `(距离, 下标)` 取最小（行 54），返回 `(gateway, distance_km)`（行 55）(FACT)。输入/输出：网格 id str + gateway 序列 → (gateway 对象, float)。调用方：本文件 `load_and_project_trace`(行 100)。

#### `def load_and_project_trace(path, gateways, *, horizon_s, expected_sha256, max_packets)` — CODE/legacy_trace_runtime.py:58
- 定位：CODE/legacy_trace_runtime.py:58-138
- 职责：校验一份不可变 V2 trace 并把它确定性地投影到活跃 Gateway 集合 (FACT)。
- 关键流程（全部 fail-closed，FACT）：
  1. 路径 resolve 后非普通文件 → `LegacyTraceError`（行 74-76）。
  2. `expected_sha256` 必须是 64 位小写 hex，否则 `LegacyTraceError`（行 77-79）。
  3. 实际 SHA-256 与期望不一致 → `LegacyTraceError`（行 80-83）。
  4. 活跃 Gateway 少于 2 个 → `LegacyTraceError`（行 84-85）。
  5. 调 `load_trace(path, horizon_s, max_packets)`，`OSError/TraceError/ValueError` 包装为 `LegacyTraceError`（行 87-94）。
  6. 收集所有源/目的网格 id（行 96），每个网格经 `_nearest_gateway` 投影，projection 条目含 `gateway` 名、`gateway_active_index`、四舍五入到 9 位的 `distance_km`（行 97-106）。
  7. 逐行检查：源/目的投影到同一 Gateway → `LegacyTraceError`（行 112-115）；`deadline_at_s` 非 None → `LegacyTraceError`（行 116-119）。
  8. 通过的行附加 `source_gateway`/`destination_gateway` 字段后入结果表（行 120-124）。
  9. 返回 manifest：`schema="leo-legacy-trace-projection/v1"`、trace 路径/SHA、horizon、包数/比特数、投影策略与同 Gateway/截止时间策略标记、projection 表（行 126-137）。
- 输入/输出：trace 路径 + gateway 序列 + 三个关键字参数 → `(projected: list[dict], manifest: dict)`。
- 依赖关系：调用方两处 (FACT)：`CODE/SimulationRL.py:3682,3690-3696`（`Earth.startTraceTraffic`，方法起于 3676；trace 路径、期望 SHA、max_packets 分别来自 env `SIM_TRAFFIC_TRACE_PATH`、`SIM_EXPECTED_TRAFFIC_TRACE_SHA256`、`SIM_TRAFFIC_TRACE_MAX_PACKETS`，见 `CODE/SimulationRL.py:3684-3689`）；`CODE/leo_sim/comparison.py:22` import、`CODE/leo_sim/comparison.py:227` 调用。被调方：`leo_sim.grid.grid_center`、`leo_sim.trace.load_trace`/`TraceError`（行 16-20）。测试佐证：`CODE/tests/test_legacy_trace_runtime.py:44`（投影保持需求）、`:78`（哈希不匹配拒绝）、`:98`（同 Gateway 冲突拒绝）、`:118`（截止时间拒绝），测试类 `LegacyTraceRuntimeTests` 起于 `:43`。

---

### 文件 `CODE/monitor.py`（实测 284 行）

模块级说明：
- 行 1：shebang `#!/usr/bin/env python3`。行 2-12：docstring，自述为「LEO-DRL 实验实时训练 dashboard」，读取 `<最新 Results 目录>/metrics.jsonl` 并渲染 Rich 面板；声明独立用法（`python monitor.py [--path ...]`）与「由 run.py 自动启动，除非传 `--no-monitor`」(FACT，docstring 声明；与 `CODE/run.py:1400-1401,1503-1509` 一致）。
- 行 13-21：imports：`__future__.annotations`、`argparse`、`json`、`math`、`os`、`time`、`collections.deque`、`pathlib.Path` (FACT)。其中 `os`（行 18）在本文件内无任何 `os.` 使用点 (FACT，全文 grep 无匹配）。
- 行 23-32：`rich` 可选 import：成功则 `_RICH=True`（行 30），`ImportError` 则 `_RICH=False`（行 32）(FACT)。
- 行 34：`ROOT = Path(__file__).resolve().parent`，即 `CODE/` 目录 (FACT，文件位于 `CODE/monitor.py`)。
- 行 283-284：`if __name__ == "__main__": raise SystemExit(main())` (FACT)。
- 模块级不读 env (FACT)。

**任务要求的两个专项问题**：
- 它读什么文件：`ROOT/"Results"/<子目录>/metrics.jsonl`（行 38-49 的自动探测；行 269 的 `_pending` 回退路径），逐行按 JSON 解析（`run` 内行 218-225、242-248）。
- 是否被 SimulationRL 直接 import：**否** (FACT：对 `CODE/SimulationRL.py` grep `monitor`/`monitor.py` 无任何匹配）。它由 `CODE/run.py:1508-1509` 以 `subprocess.Popen([sys.executable, ROOT/"monitor.py"])` 作为独立子进程启动，受 `--no-monitor`（`CODE/run.py:1400-1401`）与 env `SIM_METRICS_DISABLED`（`CODE/run.py:1504`）门控，并在 `CODE/run.py:1636-1637` 被 `terminate()`。

#### `def _find_latest_metrics()` — CODE/monitor.py:38
- 定位：CODE/monitor.py:38-49。职责：`ROOT/"Results"` 不存在返回 `None`（行 40-41）；否则在直接子目录中找含 `metrics.jsonl` 者，按文件 mtime 降序取最新（行 42-49）(FACT)。输入/输出：无参 → `Path | None`。调用方：本文件 `main`(行 266)。

#### `def _bar(fraction, width=30, fill="█", empty="░")` — CODE/monitor.py:52
- 定位：CODE/monitor.py:52-54。职责：把 `[0,1]` 比例渲染为定宽填充条字符串 (FACT)。输入/输出：float + 可选参数 → str。调用方：本文件 `_render_rich`(行 128、136)。

#### `def _action_bar(dist)` — CODE/monitor.py:57
- 定位：CODE/monitor.py:57-63。职责：把 4 维动作分布格式化为 `U:x% D:x% R:x% L:x%` 字符串 (FACT)。输入/输出：`list[float]`（长度 4）→ str。调用方：本文件 `_render_rich`(行 154)。

#### `def _collapse_warning(dist)` — CODE/monitor.py:66
- 定位：CODE/monitor.py:66-70。职责：分布对 0.25 的均方根偏差 < 0.005 时返回 `[COLLAPSE ALERT]` 告警字符串，否则返回空串 (FACT)。输入/输出：`list[float]` → str。调用方：本文件 `_render_rich`(行 155)。

#### `def _reward_sparkline(history, width=30)` — CODE/monitor.py:73
- 定位：CODE/monitor.py:73-81。职责：取 history 末尾 `width` 个值，线性映射到 9 级块字符生成 sparkline；空 history 返回全空格串 (FACT)。输入/输出：`deque` + int → str。调用方：本文件 `_render_rich`（行 144 用于 reward、行 149 用于 loss）。

#### `class DashState` — CODE/monitor.py:86
- 定位：CODE/monitor.py:86-117
- 职责：聚合 dashboard 当前展示所需全部字段的状态容器 (FACT)。
- 关键状态/结构：`step/sim_pct/sim_t/epsilon/loss/reward_ma/action_dist/delivered/dropped/q_mean`（行 88-97），`reward_history` 与 `loss_history` 两个 `deque(maxlen=window)`（行 98-99，`window` 默认 200）。
- 关键流程/方法：
  - `__init__(window=200)`（行 87)：初始化上述字段，`loss/reward_ma` 初值 `nan`，`action_dist` 初值四等分 `[0.25]*4`（行 88-99）。
  - `update(row)`（行 101)：从 metrics 行 dict 按 key 就地更新（行 102-108）；`loss` 非 None 且非 NaN 才更新并追加进 `loss_history`（行 109-111）；`reward_ma` 非 None 才更新并追加进 `reward_history`（行 112-114）；`action_dist` 长度须为 4 才接受（行 115-117）。
- 输入/输出：`update` 消费一行 JSON dict；无返回。
- 依赖关系：被本文件 `run`(行 198) 实例化，`update` 在 `run` 内行 222、235、246 调用。可识别的 metrics 键集合：`t, sim_pct, step, epsilon, delivered, dropped, q_mean, loss, reward_ma, action_dist` (FACT，行 102-117)。**这些键（及 `metrics.jsonl` 本身）的写入方在当前 `CODE/` 树中未确认**：grep 全部 `CODE/**/*.py`（排除 tests 与 __pycache__）仅 `monitor.py` 自身出现 `metrics.jsonl`、`action_dist`、`reward_ma`、`sim_pct` 字样 (FACT）。

#### `def _render_rich(state, metrics_path)` — CODE/monitor.py:122
- 定位：CODE/monitor.py:122-178。职责：把 `DashState` 渲染为 Rich `Panel` (FACT)：delivery 率（行 123-124）、进度条（行 127-133）、ε 条与步数（行 136-141）、reward/loss sparkline（行 144-151）、动作分布及 collapse 标红（行 154-157、168-169）、delivery 按 ≥85/≥60 阈值着色（行 160-165），组装成带标题的圆角 Panel 返回（行 167-178）。输入/输出：`DashState` + `Path` → `rich.panel.Panel`。调用方：本文件 `run`(行 227、238)。

#### `def _render_plain(state)` — CODE/monitor.py:181
- 定位：CODE/monitor.py:181-192。职责：无 rich 时的单行 `\r` 覆盖式文本输出，字段与 rich 版相同 (FACT)。输入/输出：`DashState` → 无返回（写 stdout）。调用方：本文件 `run`(行 249)。

#### `def run(metrics_path, refresh=0.5)` — CODE/monitor.py:197
- 定位：CODE/monitor.py:197-253。职责：dashboard 主循环 (FACT)：等待 metrics 文件出现，最长 120 秒，超时打印后返回（行 201-208）；打开文件后 tail 式循环：读新行、JSON 解析失败跳过、有变化才刷新（行 216-228 rich 分支 / 行 241-250 plain 分支）；`sim_pct >= 99.9` 时读完尾部剩余行后退出循环（行 230-239、251-252）。输入/输出：`Path` + float → 无返回。调用方：本文件 `main`(行 277)。

#### `def main()` — CODE/monitor.py:256
- 定位：CODE/monitor.py:256-280。职责：CLI 入口 (FACT)：解析 `--path/-p` 与 `--refresh`（行 257-262）；未给 path 时自动探测，探测不到则回退等待 `Results/_pending/metrics.jsonl`（行 264-270）；无 rich 时打印降级提示（行 273-275）；调 `run` 并捕获 `KeyboardInterrupt`（行 276-279）；返回 0（行 280）。输入/输出：无参（读 `sys.argv`）→ int 退出码。调用方：模块 `__main__` guard（行 284）；进程级启动方为 `CODE/run.py:1508-1509`。

---

### 文件 `CODE/runtime_effect_receipt.py`（实测 147 行）

模块级说明：
- 行 1-5：模块 docstring，自述为「SimulationRL 使用的纯 runtime-effect receipt 辅助函数」，声明刻意不依赖 simulator/ML 以便不启动仿真即可单测 (FACT，docstring 声明；代码上确实只有标准库 import）。
- 行 7-10：imports：`__future__.annotations`、`collections.abc.Callable`、`typing.Any` (FACT)。
- 无全局常量、无 env 读取、无 class (FACT)。

#### `def new_checkpoint_receipt(path="")` — CODE/runtime_effect_receipt.py:13
- 定位：CODE/runtime_effect_receipt.py:13-23
- 职责：构造一个 checkpoint 加载收据 dict (FACT)：`requested` = path 非空（行 14-16），`attempted=False`、`loaded=False`、`failures=0`、`error=None`、`result=None`（行 18-22）。
- 输入/输出：路径 str → dict。
- 依赖关系：调用方 `CODE/SimulationRL.py:3363`（`Earth.__init__` 的 `_temporal_checkpoint_load`）、`3365-3366`（`_pc_checkpoint_loads` 的 mixer/replay 两项）、`6619`（`DDQNAgent.__init__` gru eval 分支）、`12127-12128`（顶层函数 `RunSimulation`，起于 12019）；测试 `CODE/tests/test_runtime_effect_helpers.py`（import 于 `:10-15`）。

#### `def attempt_checkpoint_load(receipt, loader, *, label, fail_closed)` — CODE/runtime_effect_receipt.py:26
- 定位：CODE/runtime_effect_receipt.py:26-53
- 职责：执行一次被请求的 checkpoint 加载并就地更新收据 (FACT)。关键流程：`requested` 为假直接返回 `None`（行 34-35）；置 `attempted=True`（行 36）；调用 `loader()`（行 38）；loader 返回 `False` 视为显式失败并抛 `RuntimeError`（行 41-42，注释说明 `None` 是 Keras `load_weights` 的正常返回）；成功则置 `loaded=True`，标量结果记入 `result`（行 43-46）；异常时置 `loaded=False`、`failures` 加一、记录 `error`，`fail_closed` 为真时抛 `RuntimeError`，否则返回 `None`（行 47-53）。
- 输入/输出：receipt dict + 无参 callable + 两个关键字参数 → loader 返回值或 None。
- 依赖关系：调用方 `CODE/SimulationRL.py:6620-6624`（temporal GRU eval 加载，label `"temporal GRU"`）、`12136-12143`（path-credit mixer，label `"path-credit mixer"`）、`12151-12158`（path-credit replay，label `"path-credit replay"`），均传 `fail_closed=_SIM_FAIL_CLOSED`；测试 `CODE/tests/test_runtime_effect_helpers.py:19`（`test_requested_checkpoint_false_result_fails_closed`）。

#### `def _mismatch(field, requested, effective, reason)` — CODE/runtime_effect_receipt.py:56
- 定位：CODE/runtime_effect_receipt.py:56-62。职责：构造 `{field, requested, effective, reason}` 四键不一致记录 dict (FACT)。输入/输出：str + 三个任意值 → dict。调用方：本文件行 82、89、94、125、131、137、143；文件内私有，跨文件调用方未确认。

#### `def assess_temporal_effect(*, requested_mode, actual_mode, training_active, last_train_loss, checkpoint_receipt)` — CODE/runtime_effect_receipt.py:65
- 定位：CODE/runtime_effect_receipt.py:65-99
- 职责：核对 temporal encoder 的请求状态与实际效果，产出 effective 状态 dict 与不一致列表 (FACT)。规则：组装 `effective`（mode/training_active/last_train_loss/checkpoint 副本，行 74-79）；`actual_mode != requested_mode` → 记 `temporal_mode` 不一致（行 81-85）；`requested_mode=="gru"` 且处于训练阶段但 `last_train_loss is None` → 记 `temporal_training` 不一致（行 86-92）；`requested_mode=="gru"` 且非训练阶段但 checkpoint 未 `loaded` → 记 `temporal_checkpoint` 不一致（行 93-98）。
- 输入/输出：五个关键字参数 → `(effective: dict, mismatches: list[dict])`。
- 依赖关系：调用方 `CODE/SimulationRL.py:11076-11081`（`_run_audit_meta`，起于 10702）。测试佐证：`CODE/tests/test_runtime_effect_helpers.py:27`（gru eval 必须已加载权重）、`:41`（gru 训练必须产生真实更新）。

#### `def assess_path_credit_effect(*, requested, training_active, replay_initialized, mixer_initialized, train_successes, train_failures, checkpoint_receipts)` — CODE/runtime_effect_receipt.py:102
- 定位：CODE/runtime_effect_receipt.py:102-147
- 职责：核对 path-credit 机制的请求状态与实际效果 (FACT)。规则：组装 `effective`（阶段/两个初始化标记/训练成功失败计数/checkpoint 收据副本，行 113-122）；`requested` 但非训练阶段 → 记 `path_credit.phase` 不一致（行 124-128）；`requested` 且训练阶段：replay 或 mixer 未初始化 → 记 `path_credit.initialized` 不一致（行 129-135），`train_successes < 1` → 记 `path_credit.train_successes` 不一致（行 136-140）；任何 `requested` 但未 `loaded` 的 checkpoint → 记 `path_credit.checkpoint.<name>` 不一致（行 141-146）。
- 输入/输出：七个关键字参数 → `(effective: dict, mismatches: list[dict])`。
- 依赖关系：调用方 `CODE/SimulationRL.py:11043`（`_run_audit_meta`）。测试佐证：`CODE/tests/test_runtime_effect_helpers.py:49`（要求初始化对象与真实更新）、`:60`（评估阶段拒绝 path-credit）。

备注 (FACT)：`CODE/tests/test_runtime_effect_receipt.py` 文件名虽指向本模块，但其内容不 import 本模块（该行 57 import 的是 `traffic_burst.canonical_json_sha256`）；本模块的直接单测在 `CODE/tests/test_runtime_effect_helpers.py:10-15`（import）与 `:18`（测试类 `RuntimeEffectHelperTests`）。

---

## 符号覆盖核对清单（本片段）

- `CODE/link_outage.py`：`canonical_json_sha256` ✓、`resource_class` ✓、`_positive_float` ✓、`LinkOutageSchedule`（含 8 个方法）✓、`load_link_outage_schedule_from_env` ✓ —— 1/1 类、4/4 顶层 def。
- `CODE/temporal_encoder.py`：`mode` ✓、`temporal_enabled` ✓、`output_dim` ✓、`assert_not_conflicting_with_mappo` ✓、`reset_satellite` ✓、`apply` ✓、`_apply_framestack` ✓、`_build_gru` ✓、`_apply_gru` ✓、`_record_gru` ✓、`_train_gru_step` ✓、`save` ✓、`load` ✓、`last_train_loss` ✓ —— 0 类、14/14 顶层 def。
- `CODE/legacy_trace_runtime.py`：`LegacyTraceError` ✓、`_haversine_km` ✓、`_sha256` ✓、`_nearest_gateway` ✓、`load_and_project_trace` ✓ —— 1/1 类、4/4 顶层 def。
- `CODE/monitor.py`：`_find_latest_metrics` ✓、`_bar` ✓、`_action_bar` ✓、`_collapse_warning` ✓、`_reward_sparkline` ✓、`DashState`（含 2 个方法）✓、`_render_rich` ✓、`_render_plain` ✓、`run` ✓、`main` ✓ —— 1/1 类、9/9 顶层 def。
- `CODE/runtime_effect_receipt.py`：`new_checkpoint_receipt` ✓、`attempt_checkpoint_load` ✓、`_mismatch` ✓、`assess_temporal_effect` ✓、`assess_path_credit_effect` ✓ —— 0 类、5/5 顶层 def。

---

# 第二卷 新平台说明书（卫星直连，模块化内核 `CODE/leo_sim/`）

按模块展开：config / trace / rng → grid / model / control / outage / fates / routing → kernel → learning / receipt → governance / acceptance / platform_check / comparison / population / __main__ / __init__。
# 片段 n3：新平台 `leo_sim` 配置解析 / 需求迹编译 / 随机流

范围：`CODE/leo_sim/config.py`、`CODE/leo_sim/trace.py`、`CODE/leo_sim/rng.py`。
行数均为 `wc -l` 实测。标注约定：(FACT) = 可直接在代码/文档字符串中核验；(INFERENCE) = 从命名/注释/上下文推测。

---

## 文件 `CODE/leo_sim/config.py`（实测 630 行）

模块级说明：

- 模块 docstring（行 1-7）：声明解析顺序为内置默认值 → 具名 profile → 用户文件 → 显式 overrides；产物是带 SHA256 身份的单一 canonical 对象；未知字段与非法组合被拒绝（fail closed）；明确声明「本包不存在环境变量桥」。(FACT)
- imports（行 9-17）：`__future__.annotations`、stdlib `copy`/`hashlib`/`json`/`math`/`typing.{Any,Mapping}`、第三方 `yaml`（PyYAML）。无环境变量读取（与 docstring 一致）。(FACT)
- 版本常量（行 19-20）：`CONFIG_SCHEMA_VERSION = "leo-sim-config/v1"`；`TRACE_IDENTITY_VERSION = "leo-sim-trace-identity/v1"`。(FACT)
- `SCHEMA`（行 55-161，行 54 为注释）：9 个顶层组（`scenario`/`endpoints`/`demand`/`access`/`links`/`control_plane`/`routing`/`learning`/`execution`/`outputs`）各自允许的字段名及类型表；组外字段被拒绝。(FACT)
- 合法值枚举（行 163-171）：`VALID_DEMAND_MODES`（8 个：uniform、gravity、population_gravity、hotspot、burst、diurnal、csv、mlab）、`VALID_ASSOCIATION`（bbm/mbb）、`VALID_POLICIES`（hop/delay/capacity/oracle）、`VALID_CONTRACTS`（C1/C3/C4/C5/C6/C7/GAT/MPNN）、`VALID_ALGORITHMS`（none/ddqn）、`VALID_ISL_DIRS`（N/S/E/W）。(FACT)
- `DEFAULTS`（行 173-268）：9 组的完整默认值（例如 scenario：60 s、0.1 s 步长、66 星 6 面、550 km、53°、最小仰角 25°、seed 42；demand 默认 uniform 1.0 Mbps 等；行 229 注释声明 `ge_gsl`/`ge_isl` 默认值「未按任何真实星座运营商校准」）。(FACT)
- `PROFILES`（行 270-276）：只定义一个 profile `"smoke"`（5 s、12 星 3 面、0.5 Mbps、max_events 50_000、max_packets 5_000）。(FACT)

#### `class ConfigError` — CODE/leo_sim/config.py:23
- 定位：CODE/leo_sim/config.py:23
- 职责：一切配置校验失败抛出的异常类型，继承 `ValueError`（行 23-24，类体只有 docstring，无任何方法）。(FACT)
- 关键状态/结构：无。
- 关键流程/方法：无方法。
- 输入/输出：构造参数为错误消息字符串。
- 依赖关系：在 config.py 内被 `_check_group`、`_check_finite`、`_validate_semantics`、`resolve_config`、`load_config_file` 抛出（行 283-537、595、599、622、624、629 等）；被 `CODE/leo_sim/__main__.py:34,61,186,384` 捕获；测试佐证 `CODE/leo_sim/tests/test_config.py:18-64`。

#### `class _UniqueKeyLoader` — CODE/leo_sim/config.py:27
- 定位：CODE/leo_sim/config.py:27
- 职责：继承 `yaml.SafeLoader`，拒绝同一 mapping 内重复键的 YAML 加载器（类 docstring，行 28）。(FACT)
- 关键状态/结构：无实例状态；行 49-51 通过 `_UniqueKeyLoader.add_constructor(...)` 把 `_construct_unique_mapping` 注册为默认 mapping tag 的构造器（类级注册，模块导入时执行）。
- 关键流程/方法：无自有方法；行为全部来自注册的构造器 `_construct_unique_mapping`。
- 输入/输出：供 `yaml.load(..., Loader=_UniqueKeyLoader)` 使用（行 620）。
- 依赖关系：仅被本文件 `load_config_file`（行 620）使用。

#### `def _construct_unique_mapping(loader, node, deep=False)` — CODE/leo_sim/config.py:31
- 定位：CODE/leo_sim/config.py:31
- 职责：逐键构造 YAML mapping；遇到不可哈希键或重复键时抛 `yaml.constructor.ConstructorError`（行 36-44），否则返回普通 dict（行 45-46）。(FACT)
- 输入/输出：入 `(loader, node, deep=False)`，出 `dict` 或抛 `ConstructorError`。
- 依赖关系：在行 49-51 注册到 `_UniqueKeyLoader`；调用方为 PyYAML 构造流程（间接来自 `load_config_file`）。

#### `def _check_group(group: str, values: Mapping[str, Any]) -> None` — CODE/leo_sim/config.py:279
- 定位：CODE/leo_sim/config.py:279
- 职责：按 `SCHEMA[group]` 检查一组字段：未知字段报错（行 282-283）；类型不符报错（行 288-289）；当期望类型不含 bool 时，Python `bool` 值被显式拒绝（行 286-287，因 `bool` 是 `int` 子类需单独拦截）。(FACT)
- 输入/输出：入组名与字段映射，无返回；失败抛 `ConfigError`。
- 依赖关系：调用方 `resolve_config`（行 603-604）；被调 `SCHEMA`。测试佐证 `test_config.py:63-64`（seed=True 被拒）。

#### `def _deep_merge(base: dict, override: Mapping) -> dict` — CODE/leo_sim/config.py:292
- 定位：CODE/leo_sim/config.py:292
- 职责：深拷贝 `base` 后递归合并 `override`：两边都是 mapping 时递归（行 295-296），否则整体覆盖并深拷贝（行 297-298）。(FACT)
- 输入/输出：入两个 dict/Mapping，出合并后的新 dict（不改入参）。
- 依赖关系：调用方 `resolve_config`（行 600-602）及自身递归（行 296）。

#### `def _check_finite(node: Any, path: str = "") -> None` — CODE/leo_sim/config.py:302
- 定位：CODE/leo_sim/config.py:302
- 职责：递归遍历合并后的配置树，拒绝任何 NaN/±Inf 的 float（bool 直接放行，行 304-305；float 非有限则抛错并带路径，行 306-308；Mapping/list/tuple 递归，行 310-316）。(FACT)
- 输入/输出：入任意配置子树与路径前缀，无返回；失败抛 `ConfigError`。
- 依赖关系：调用方 `resolve_config`（行 605）。

#### `def _validate_semantics(cfg: Mapping[str, Any]) -> None` — CODE/leo_sim/config.py:319
- 定位：CODE/leo_sim/config.py:319
- 职责：对合并后配置做跨字段语义校验（大函数，行 319-537），任何一条不满足即抛 `ConfigError`。按组分述（均为 FACT）：
  - scenario（行 325-347）：`duration_s`>0、`time_step_s`>0、`altitude_km`∈[300,2000]（行 329-332 注释说明 LEO 包络理由）、`inclination_deg`∈[0,180]、`seed`≥0、卫星数/面数≥1 且整除、`min_elevation_deg`∈(0,90)。
  - endpoints（行 348-391）：`grid_deg`/`aggregation_deg`>0 且 agg≥grid；两者都必须整除 180 与 360（保证格网 id 稳定，行 352-361）；agg 必须是 grid 的整数倍（行 362-364）；`sites` 逐项校验：必须是 mapping、必含 name/lat/lon、只允许额外字段 `demand_weight`、name 非空且不重复、lat∈[-90,90]、lon∈[-180,180]、demand_weight 为正有限数（缺省 1.0，行 388）。
  - demand（行 392-420）：mode ∈ `VALID_DEMAND_MODES`；`offered_mbps`/`packet_bits`>0；mode=csv 必须有 `csv_path`；mode=population_gravity 必须有 `population_path`；人口指数>0；mode=burst 必须有非负 `burst_start_s` 与正的 `burst_duration_s`；`deadline_s` 设置时必须>0；gravity 参数>0；hotspot_fraction∈(0,1]、hotspot_concentration∈[0,1]；burst_multiplier>0；diurnal_amplitude≥0、diurnal_phase_h∈[0,24)。
  - access（行 421-445）：association∈{bbm,mbb}；slots≥1；上下行速率>0；队列≥0；DRR quantum≥1；hysteresis/dwell/acquisition≥0；retirement_deadline_s>0、retiring_link_limit≥0；slot_lease_s/idle_release_s>0；association=mbb 要求 dual_connect=true 且 retiring_link_limit≥1（行 439-443；行 444-445 是同条件的重复检查）。
  - links（行 446-458）：`isl_dirs` 为 {N,S,E,W} 的非空子集；isl_rate_mbps/max_isl_km>0；isl_queue_bits≥0；`ge_gsl`/`ge_isl` 必须恰好含 `mean_good_s`/`mean_bad_s` 两个正数。
  - control_plane（行 459-464）：vis_k≥0；ttl_s/advertise_interval_s>0；packet_bits≥1；priority 必须等于 `"nonpreemptive_priority"`。
  - routing（行 465-470）：policy∈`VALID_POLICIES`；max_hops≥1；contract∈`VALID_CONTRACTS`。
  - learning 交叉约束（行 471-516）：learning_enabled 与 algorithm≠none 必须互相匹配；learning 禁止配 oracle policy；learning 要求 control_plane.enabled=true；algorithm∈{none,ddqn}；mode∈{train,eval}；seed/obs_hops 为 null 或非负 int；obs_hops≤control_plane.vis_k；checkpoint_path 为 null 或非空字符串；checkpoint_sha256 为 null 或 64 位小写十六进制；algorithm=none 时禁止 eval 模式与任何 checkpoint 字段；eval 模式必须同时给 checkpoint_path+sha256；train 模式禁止加载 checkpoint。
  - learning 超参与 execution（行 517-537）：reward 必须等于 `"queue"`（行 517-522 注释声明 distance/linear reward 被排除出 v1）；lr>0；batch_size/replay_size/target_update_interval≥1 且 batch≤replay；epsilon_decay_s>0；gamma∈[0,1]；0≤epsilon_end≤epsilon_start≤1；execution 三项上限≥1。
- 关键状态/结构：只读入 `cfg`，无持有状态。
- 输入/输出：入完整合并配置 dict，无返回；失败抛 `ConfigError`。
- 依赖关系：调用方 `resolve_config`（行 606）；读取行 163-171 的枚举常量。测试佐证 `test_config.py:33-47`、`test_learning.py:226,248`、`test_review_regressions.py:133-146`。

#### `def trace_identity_payload(resolved: dict) -> dict` — CODE/leo_sim/config.py:540
- 定位：CODE/leo_sim/config.py:540
- 职责：从 resolved 配置中抽取「决定 trace 字节内容/编译边界」的子集组成 payload：identity/config 版本、scenario 的 duration_s 与 seed、完整 endpoints 组、完整 demand 组、execution.max_packets（行 553-561）；docstring（行 541-551）声明 routing/access/links/control_plane/learning/outputs/执行上限（除 max_packets 外）刻意不含在内，因为不同机制臂必须消费同一不可变 trace。(FACT)
- 输入/输出：入 `resolve_config` 的返回 dict，出 payload dict。
- 依赖关系：调用方 `trace_identity_sha256`（行 567）；未找到其它调用方。

#### `def trace_identity_sha256(resolved: dict, input_sha256: str = "") -> str` — CODE/leo_sim/config.py:564
- 定位：CODE/leo_sim/config.py:564
- 职责：把 `trace_identity_payload` 加上 `input_sha256`（csv/mlab 输入文件内容哈希，合成模式为空串）后按 sort_keys 紧凑 JSON 序列化并取 SHA256（行 567-570）。(FACT)
- 输入/输出：入 resolved dict 与可选输入哈希，出 64 位小写十六进制字符串。
- 依赖关系：调 `trace_identity_payload`；被 `CODE/leo_sim/trace.py:429`（写入 manifest）、`CODE/leo_sim/governance.py:106`（写入 run intent）、`CODE/leo_sim/__main__.py:164`（加载预编译 trace 时重算比对）、本文件 `demand_sha256`（行 578）调用。测试佐证 `CODE/leo_sim/tests/test_trace.py:50,183`。

#### `def demand_sha256(resolved: dict) -> str` — CODE/leo_sim/config.py:573
- 定位：CODE/leo_sim/config.py:573
- 职责：`trace_identity_sha256(resolved)`（不带 input 哈希）的别名；docstring（行 574-577）声明已 DEPRECATED，仅为引用旧名的冻结外部探针脚本保留。(FACT，保留理由为 docstring 原文)
- 输入/输出：入 resolved dict，出十六进制哈希字符串。
- 依赖关系：调 `trace_identity_sha256`；在 `CODE/` 内未找到任何调用方——调用方未确认（docstring 指向仓库外脚本）。

#### `def resolve_config(user=None, profile=None, overrides=None) -> dict` — CODE/leo_sim/config.py:581
- 定位：CODE/leo_sim/config.py:581
- 职责：配置解析主入口。流程（FACT）：拒绝未知顶层组（行 592-595）→ 深拷贝 `DEFAULTS`（行 596）→ 可选套用 `PROFILES[profile]`，未知 profile 报错（行 597-600）→ 依次 `_deep_merge` user、overrides（行 601-602）→ 逐组 `_check_group`（行 603-604）→ `_check_finite`（行 605）→ `_validate_semantics`（行 606）→ sort_keys 紧凑 JSON 序列化并取 SHA256（行 607-608）。返回 `{"version", "config", "canonical_json", "sha256"}`（行 609-614）。
- 输入/输出：入可选用户映射/profile 名/overrides 映射，出上述四键 dict；失败抛 `ConfigError`。
- 依赖关系：调 `_deep_merge`/`_check_group`/`_check_finite`/`_validate_semantics`；被 `load_config_file`（行 630）、`CODE/leo_sim/governance.py:79`、`CODE/leo_sim/platform_check.py:167`、`CODE/leo_sim/receipt.py:695` 调用；测试佐证 `CODE/leo_sim/tests/helpers.py:47`、`test_config.py:8-64`。

#### `def load_config_file(path: str) -> dict` — CODE/leo_sim/config.py:617
- 定位：CODE/leo_sim/config.py:617
- 职责：YAML 配置入口。用 `_UniqueKeyLoader` 解析文件（行 619-620，YAML 错误转成 `ConfigError`，行 621-622）；顶层必须是 mapping（行 623-624）；取出 `profile` 键（行 626）；`config_version` 缺省为当前版本，显式给出且不等于 `CONFIG_SCHEMA_VERSION` 时拒绝（行 627-629）；余下内容交 `resolve_config`（行 630）。(FACT)
- 输入/输出：入 YAML 文件路径，出 `resolve_config` 的返回 dict。
- 依赖关系：调 `resolve_config`；被 `CODE/leo_sim/__main__.py:28`、`CODE/leo_sim/platform_check.py:102,144`、`CODE/experiment_platform/authorize_experiment.py:314`、`CODE/scripts/remote/remote_job.py:196-198` 调用；测试佐证 `test_config.py:67-77`、`test_comparison.py:15,52`。

---

## 文件 `CODE/leo_sim/trace.py`（实测 522 行）

模块级说明：

- 模块 docstring（行 1-11）：声明产物为 `trace.csv`（packet_id, emit_time_s, src_grid_id, dst_grid_id, bits, deadline_at_s）加 manifest（含 schema 版本、config/input 哈希、RNG 流映射、offered 包/比特台账、活跃端点数、时间范围）；声明相同 config+input+seed 字节可复现；声明 mlab 模式只把 M-Lab 数据复用为 OD 权重、provenance 恒为 `measurement_proxy`。(FACT)
- 注意（事实性出入）：docstring 行 8 列举的支持模式为「uniform, gravity, hotspot, burst, diurnal, csv, mlab」7 种，未列 `population_gravity`；但代码实现了第 8 种 `population_gravity`（行 328-337、140-145；`config.py:164` 的 `VALID_DEMAND_MODES` 亦含之）。(FACT)
- imports（行 12-21）：stdlib `csv`/`hashlib`/`json`/`math`/`os`/`pathlib.Path`；同包 `from . import config, grid, population, rng`（行 21）。(FACT)
- 常量（行 23-29）：`TRACE_SCHEMA = "leo-sim-trace/v1"`；`TRACE_MANIFEST_SCHEMA = "leo-sim-trace-manifest/v1"`；`PACKET_ID_CONTRACT`（合成模式 id 为发射序 1..N，csv 模式原样保留源 id）；`REPO_MLAB_CSV` 指向 `CODE/data/traffic/mlab_2026-05-27.csv`（该文件存在，已核实）；`TIME_DECIMALS = 6`。(FACT)

#### `class TraceError` — CODE/leo_sim/trace.py:32
- 定位：CODE/leo_sim/trace.py:32
- 职责：trace 编译/加载/校验一切失败的异常类型，继承 `ValueError`，类体仅 `pass`（行 32-33，无方法）。(FACT)
- 输入/输出：构造参数为错误消息字符串。
- 依赖关系：在 trace.py 内被各函数抛出；被 `CODE/leo_sim/__main__.py:61,217,384` 与 `CODE/legacy_trace_runtime.py:17-20,93` 捕获；测试佐证 `test_review_round3.py:80-134`、`test_review_round4.py:229-249,408-409,497-498`。

#### `def _format_time(value: float) -> str` — CODE/leo_sim/trace.py:36
定位 CODE/leo_sim/trace.py:36；职责：把时间格式化为字节可复现的十进制字符串——保留 6 位小数后去尾零与尾小数点，空串回退 `"0"`（行 38-39）(FACT)；入 float 出 str。调用方：`_serialized_time`（行 43）、`compile_trace`（行 420-421）。

#### `def _serialized_time(value: float) -> float` — CODE/leo_sim/trace.py:42
定位 CODE/leo_sim/trace.py:42；职责：`float(_format_time(value))`，即「写进 CSV 的字符串再读回」的数值，用于让编译期校验作用于真实序列化值（配合行 401-402 注释）(FACT)；入 float 出 float。调用方：`compile_trace`（行 404-405）。

#### `def validate_packet_rows(rows, horizon_s, max_packets) -> None` — CODE/leo_sim/trace.py:46
- 定位：CODE/leo_sim/trace.py:46
- 职责：统一的包行契约（docstring 行 48-56 声明在编译、加载预编译 trace、内核入口三处同一执行）。逐行校验（FACT）：总数≤max_packets（行 57-60）；packet_id 为正 int 且非 bool、不重复（行 70-74）；emit_time_s 有限、≥0、≤horizon（行 75-81）；bits 为正 int（行 82-83）；src/dst 通过 `grid.is_valid_grid_id` 且 src≠dst（行 84-87）；deadline 为空或有限且≥emit_time（行 88-93）；行序列必须按 (emit_time_s, packet_id) 稳定升序（行 94-98）。任何违反抛 `TraceError`。
- 输入/输出：入 dict 行列表、horizon 秒、包数上限；无返回。
- 依赖关系：调 `grid.is_valid_grid_id`（grid.py:48）；调用方：`compile_trace`（行 408）、`load_trace`（行 518）、`CODE/leo_sim/kernel.py:639`（内核入口重查）、`CODE/leo_sim/receipt.py:716`（receipt 校验重查）；测试佐证 `test_review_round3.py:128-134`（内核是最后闸门）、`test_review_round4.py:497-498`。

#### `def _haversine_km(lat1, lon1, lat2, lon2)` — CODE/leo_sim/trace.py:101
定位 CODE/leo_sim/trace.py:101；职责：haversine 大圆距离公式（R=6371.0 km，行 102-107）(FACT)；入两点经纬度（度），出距离 km。调用方：`_dst_choices`（行 148）。

#### `def _endpoints(cfg: dict) -> list[dict]` — CODE/leo_sim/trace.py:110
- 定位：CODE/leo_sim/trace.py:110
- 职责：把 `endpoints.sites` 展开为端点列表：每个 site 算细格 `grid.grid_id(lat,lon,grid_deg)` 再算 `grid.aggregate_id(...,aggregation_deg)`，条目含 name/lat/lon/weight（demand_weight 缺省 1.0）/agg_grid_id（行 115-125）；随后做稀疏激活——每个活跃聚合格只保留第一个端点（行 126-130）；sites 为空抛 `TraceError`（行 113-114）。(FACT)
- 输入/输出：入完整 config dict，出端点 dict 列表。
- 依赖关系：调 `grid.grid_id`（grid.py:21）、`grid.aggregate_id`（grid.py:43）；调用方：`compile_trace`（行 339）。

#### `def _dst_choices(gen, mode, endpoints, i, t, dm, mlab_weights=None)` — CODE/leo_sim/trace.py:133
- 定位：CODE/leo_sim/trace.py:133
- 职责：按 demand 模式为源端点 i 选目的端点；候选 = 其它聚合格中的端点，候选为空抛 `TraceError`（行 135-137）。各模式（FACT）：
  - uniform/burst/diurnal：均匀随机选一候选（行 138-139）。
  - gravity/population_gravity：权重 = `weight^destination_exponent / max(haversine, d_floor)^alpha`，其中 destination_exponent 仅 population_gravity 取 `destination_population_exponent`，gravity 固定 1.0（行 140-149）；用轮盘赌（`gen.random()*total` 累加命中，行 150-157）选目的。
  - hotspot：取候选列表前 `max(1, round(len*hotspot_fraction))` 个为热点（行 160-161，注释说明顺序确定、选择随机）；以概率 `hotspot_concentration` 在热点内均匀选，否则在冷点内均匀选（行 163-167）。
  - mlab：按 `mlab_weights[(src_agg, dst_agg)]` 轮盘赌（行 168-183）；源到所有候选权重和≤0 时抛 `TraceError`（行 171-176，注释声明无平滑回退、触发即缺陷）。
  - 其它模式名抛 `TraceError`（行 184）。
- 输入/输出：入 RNG、模式名、端点列表、源下标、时间、demand 组、可选 mlab 权重；出目的端点 dict。
- 依赖关系：调 `_haversine_km`；调用方：`compile_trace`（行 387）。

#### `def _rate_multiplier(mode, t, src_lon, dm)` — CODE/leo_sim/trace.py:187
定位 CODE/leo_sim/trace.py:187；职责：时间调制的速率倍率——burst 模式在 `[burst_start_s, burst_start_s+burst_duration_s)` 内返回 `burst_multiplier`、否则 1.0（行 188-192）；diurnal 模式按经度换算本地时 `(t/3600 + lon/15) % 24`，返回 `max(0, 1 + amplitude·cos(2π(local_h − phase_h)/24))`（行 193-197）；其它模式恒 1.0（行 198）(FACT)；入模式/时刻/源经度/demand 组，出 float 倍率。调用方：`compile_trace`（行 384）。

#### `def _load_mlab_weights(endpoints, grid_deg, agg_deg)` — CODE/leo_sim/trace.py:201
- 定位：CODE/leo_sim/trace.py:201
- 职责：把 M-Lab 吞吐样本聚合到活跃聚合格上的 OD 权重。文件不存在抛 `TraceError`（行 207-208）；逐行读 `REPO_MLAB_CSV`，把 client/server 经纬度映射到聚合格，缺列或数值非法的行跳过（行 212-216），权重按 `mean_throughput_mbps × sample_count` 累加（行 217）。(FACT)
- docstring（行 202-206）声明映射必须用 resolved 配置的格网度数，否则权重与端点脱钩（并提及旧的固定默认格网曾靠 1e-9 平滑掩盖该问题）。(FACT，历史陈述为 docstring 原文)
- 输入/输出：入端点列表与两级格网度，出 `{(src_agg, dst_agg): float}` dict。
- 依赖关系：调 `grid.grid_id`/`grid.aggregate_id`；调用方：`compile_trace`（行 343）。

#### `def compile_trace(resolved: dict, out_dir: str) -> dict` — CODE/leo_sim/trace.py:221
- 定位：CODE/leo_sim/trace.py:221
- 职责：编译不可变 trace 并返回 manifest dict（大函数，行 221-479）。流程（FACT）：
  1. 输出目录防护（行 229-241）：out_dir 不得为符号链接；`trace.csv`/`manifest.json` 已存在时必须是普通文件且不得是符号链接。
  2. csv 模式分支（行 247-325）：要求 `csv_path` 存在（行 249-250）并对文件字节取 SHA256 作 input_hash（行 251）；要求列含 packet_id/emit_time_s/src_lat/src_lon/dst_lat/dst_lon/bits（行 253-257）；packet_id 必须是唯一正整数的原文（拒绝重编号，行 258-274）；emit_time_s 必须有限且落在 [0, duration]（行 275-287，注释声明超界记录不静默丢弃）；坐标映射到聚合格且 src≠dst（行 288-297）；bits 为正整数原文（行 298-308）；deadline 原样保留（行 309-319）；按 (emit_time, id) 排序（行 321）；活跃格直接来自 CSV，`endpoints.sites` 在 csv 模式非必需（行 322-325）。
  3. 合成模式分支（行 326-391）：population_gravity 用 `population.load_population_regions(population_path, aggregation_deg)` 生成端点（weight=人口），provenance=`population_proxy`、input_hash=人口表 source_sha256（行 328-337）；其余模式用 `_endpoints`（行 339）。RNG 取 `rng.streams(seed)["demand"]`（行 340）。mlab 模式加载 `_load_mlab_weights`，provenance=`measurement_proxy`，input_hash=M-Lab 文件 SHA256，并做覆盖检查：每个活跃源格必须对至少一个其它活跃格有正权重，否则抛 `TraceError`（fail closed，无均匀回退，行 342-362）。总速率 = `offered_mbps×1e6/packet_bits` 包/秒，按 `weight^source_exponent`（source_exponent 仅 population_gravity 取配置值，否则 1.0）分到各源（行 363-372）。发包用泊松细化（thinning）：以 `base_rate×max_mult` 抽指数间隔，再按 `_rate_multiplier(t)/max_mult` 接受（行 373-389；max_mult：burst 取 `max(1,burst_multiplier)`，diurnal 取 `1+|amplitude|`，行 374-378）。deadline 配置存在时写 `t+deadline`（行 388）。最后排序并把 packet_id 重编号为发射序 1..N（行 390-391）。
  4. 编译期上界（行 393-399）：行数超过 `execution.max_packets` 直接抛 `TraceError`。
  5. 序列化值校验（行 401-413）：对 `_serialized_time` 处理后的值（而非内存高精度值）跑 `validate_packet_rows`，保证「编译成功 ⇒ load_trace 成功」（行 401-402 注释）。
  6. 写 `trace.csv`（行 415-421，时间经 `_format_time`）并取文件 SHA256（行 422）。
  7. 组 manifest（行 424-445，结构见下）并写 `manifest.json`（indent=2, sort_keys，行 476-478），返回 manifest dict（行 479）。
- manifest 结构（FACT，行 425-445）：`schema`(=TRACE_MANIFEST_SCHEMA)、`trace_schema`、`trace_sha256`、`trace_identity_sha256`(=`config.trace_identity_sha256(resolved, input_hash)`，行 429)、`config_version`、`input_sha256`、`mode`、`provenance`（synthetic/population_proxy/measurement_proxy）、`rng_streams`(=`rng.stream_mapping(seed, ["demand"])`)、`packet_id_contract`、`offered_packets`、`offered_bits`、`ledger:{packets,bits}`、`active_endpoints`（从实际序列化行的 src/dst 格去重计数，行 441-442）、`time_range_s`（首/末行时间，空 trace 为 [0.0,0.0]）。条件字段：measurement_proxy 加 `not_calibrated_user_demand` 与 `provenance_note`（行 446-451）；population_proxy 再加上述两字段及 `population` 块（source_path/sha256/shape/resolution_deg/aggregation_deg/total_population/candidate_regions/三个人口与距离指数，行 452-475）。
- 输入/输出：入 `resolve_config` 返回 dict 与输出目录，出 manifest dict；副作用为写两个文件；失败抛 `TraceError`。
- 依赖关系：调 `_endpoints`/`_dst_choices`/`_rate_multiplier`/`_load_mlab_weights`/`_serialized_time`/`_format_time`/`validate_packet_rows`、`config.trace_identity_sha256`、`grid.*`、`population.load_population_regions`（population.py:96）、`rng.streams`/`rng.stream_mapping`；调用方：`CODE/leo_sim/__main__.py:45`、`CODE/leo_sim/platform_check.py:50`、`CODE/leo_sim/acceptance.py:97`、`CODE/leo_sim/comparison.py:216`；测试佐证 `test_trace.py:42-116`（字节可复现、csv 模式、mlab 标签、五种合成模式全量生成）、`test_review_round2.py:77-97`、`test_review_round4.py:96,229-249,383-409`。

#### `def load_trace(path, horizon_s=None, max_packets=None) -> list[dict]` — CODE/leo_sim/trace.py:482
- 定位：CODE/leo_sim/trace.py:482
- 职责：加载已编译 trace.csv。列集合必须精确等于六列契约（行 493-494）；逐行解析 packet_id/emit_time_s/bits 与可选 deadline（行 495-509）；最后跑 `validate_packet_rows`，horizon 未给时用 `math.inf`、max_packets 未给时用 `1<<62`（行 518-521）；返回 dict 行列表。(FACT)；docstring（行 484-489）声明内核入口无论 loader 参数如何都会重查 horizon 与 max_packets。
- 输入/输出：入 trace.csv 路径与可选上限，出 dict 行列表；失败抛 `TraceError`。
- 依赖关系：调 `validate_packet_rows`；调用方：`CODE/leo_sim/__main__.py:50,176`、`CODE/leo_sim/receipt.py:623`、`CODE/leo_sim/platform_check.py:55`、`CODE/leo_sim/acceptance.py:102`、`CODE/leo_sim/comparison.py:222`、`CODE/legacy_trace_runtime.py:88`；测试佐证 `test_review_round3.py:80-110`（拒绝坏行、强制 max_packets）、`test_review_round4.py:511-512`。

---

## 文件 `CODE/leo_sim/rng.py`（实测 41 行）

模块级说明：

- 模块 docstring（行 1-8）：声明每个机制从同一种子派生独立命名流，启停一个机制不扰动其它机制的随机性；链路级 Gilbert-Elliott 信道用 `link_stream(seed, key)`——由运行种子与稳定链路身份字符串派生的私有流，与对象创建顺序和其它链路流量无关。(FACT)
- imports（行 9-13）：`__future__.annotations`、stdlib `hashlib`、`numpy`。(FACT)
- `STREAM_NAMES`（行 15-23）：7 个流名——`demand`、`ge_gsl`、`ge_isl`、`association`、`routing`、`control`、`monitor`。(FACT)
- 事实备注：在生产代码（非测试）中，`streams()` 唯一的调用点是 `trace.py:340`，只消费 `"demand"` 流；GE 信道实际走的是 `link_stream`（kernel.py:461,773）。`STREAM_NAMES` 中其余 6 个名字在生产代码中未见经 `streams()` 消费的调用点（Grep 全 CODE/ 核实）。(FACT)；这些名字是否为后续机制预留，代码内无说明——未确认。

#### `def streams(seed: int, names=STREAM_NAMES) -> dict[str, np.random.Generator]` — CODE/leo_sim/rng.py:26
- 定位：CODE/leo_sim/rng.py:26
- 职责：`np.random.SeedSequence(seed)` 后 `spawn(len(names))` 个并列子序列，每个名字配一个 `np.random.default_rng(child)`（行 27-29）。(FACT)
- 输入/输出：入整数种子与流名序列，出 `{流名: Generator}` dict。
- 依赖关系：调用方 `CODE/leo_sim/trace.py:340`（取 `["demand"]`）；测试佐证 `CODE/leo_sim/tests/test_trace.py:31-38`（同种子两次调用逐流一致、不同流序列不同）、`test_fates_outage.py:64-82`。

#### `def stream_mapping(seed: int, names=STREAM_NAMES) -> dict[str, str]` — CODE/leo_sim/rng.py:32
- 定位：CODE/leo_sim/rng.py:32
- 职责：生成人类可读的 种子→流 映射 `{name: "SeedSequence(seed).spawn[i]"}`，docstring 声明其记录在 trace manifest 中（行 33-34）。(FACT)
- 输入/输出：入种子与流名序列，出字符串 dict。
- 依赖关系：调用方 `CODE/leo_sim/trace.py:434`（写 manifest 的 `rng_streams`，只传 `["demand"]`）、`CODE/leo_sim/receipt.py:202`（receipt 校验时重算比对）。

#### `def link_stream(seed: int, link_key: str) -> np.random.Generator` — CODE/leo_sim/rng.py:37
- 定位：CODE/leo_sim/rng.py:37
- 职责：按链路身份字符串派生私有流：`sha256(link_key)` 摘要取前 8 字节小端转 int，再以 `SeedSequence([seed, key_int])` 建 Generator（行 39-41）。(FACT)
- 输入/输出：入运行种子与链路 key 字符串，出独立 `np.random.Generator`。
- 依赖关系：调用方 `CODE/leo_sim/kernel.py:461`（ISL 方向链路，key 形如 `isl:{sat}:{direction}`）、`CODE/leo_sim/kernel.py:773`（GSL 链路，key 形如 `gsl:{sat}:{cell}`）；测试佐证 `CODE/leo_sim/tests/test_fates_outage.py:89-93`（同 key 序列一致、与创建顺序无关）。
# 新平台片段 n4：地理网格 / 几何模型 / 控制面 / 中断 / 台账 / 路由

范围：`CODE/leo_sim/{grid,model,control,outage,fates,routing}.py`。行数均为 `wc -l` 实测。

---

## 文件 `CODE/leo_sim/grid.py`（实测 87 行）

模块级说明：

- 模块 docstring（grid.py:1-6）声明：grid ID 把经纬度编码进可配置分辨率的格子（默认 0.25 度），聚合格（默认 1 度）把细格分组，只有出现在需求 trace 里的格子被激活。
- imports（grid.py:7-9）：`from __future__ import annotations`、`math`。无第三方依赖。
- 全局常量：`DEFAULT_GRID_DEG = 0.25`（grid.py:11）；`DEFAULT_AGG_DEG = 1.0`（grid.py:12）。无环境变量读取。

### `def _cell_index(v, lo, deg, span)` — CODE/leo_sim/grid.py:15

一维格索引工具函数：计算 `floor((v-lo)/deg)`，再用 `min(..., n-1)` 把边界坐标（lat=90、lon=180）钳进最后一格（实现见 grid.py:17-18，注释在 grid.py:16）。输入：坐标值 `v`、下界 `lo`、格宽 `deg`、总跨度 `span`；输出：整数格索引。被 `grid_id`（grid.py:26-27）调用；外部调用方未确认。

### `def grid_id(lat, lon, deg=DEFAULT_GRID_DEG)` — CODE/leo_sim/grid.py:21

把 (lat, lon) 编码为字符串格 ID。FACT：lat 越界 `[-90, 90]` 或 lon 越界 `[-180, 180]` 时抛 `ValueError`（grid.py:22-25）；分别调用 `_cell_index` 得到 ilat/ilon（grid.py:26-27）；返回 `f"G{deg:g}:{ilat}:{ilon}"`，即把分辨率量化进 ID（grid.py:28-30）。输入：经纬度浮点、可选格宽；输出：形如 `G0.25:485:542` 的字符串。调用方：`trace.py:117,213,214,289,290`（端点格编码）、`population.py:85`、`kernel.py` 间接经 `TrafficEndpoint`（kernel.py:204 用的是 `grid_center`）、测试 `tests/test_grid.py:8-38`、`tests/helpers.py:15`。

### `def grid_center(gid)` — CODE/leo_sim/grid.py:33

把格 ID 解码回格中心经纬度：按 `:` 切分、解析 deg/ilat/ilon，计算 `-90 + (ilat+0.5)*deg`、`-180 + (ilon+0.5)*deg`，并 `round(..., 9)` 去掉浮点噪声（grid.py:34-40，注释在 grid.py:39）。输入：格 ID 字符串；输出：`(lat, lon)` 二元组。调用方：本文件 `aggregate_id`（grid.py:44）、`kernel.py:204`（TrafficEndpoint 取端点坐标）、`population.py:89`、`tests/helpers.py:19`、测试 `tests/test_grid.py:10,29`。

### `def aggregate_id(gid, agg_deg=DEFAULT_AGG_DEG)` — CODE/leo_sim/grid.py:43

把细格 ID 映射到聚合格 ID：先 `grid_center(gid)` 取细格中心，再以 `agg_deg` 重新调用 `grid_id`（grid.py:44-45）。FACT：映射依据是细格中心点落入的聚合格。输入：细格 ID、可选聚合度；输出：聚合格 ID 字符串。调用方：本文件 `active_aggregate_cells`（grid.py:85）、`trace.py:118,213-214,289-290`、测试 `tests/test_grid.py:26-29`、`tests/helpers.py:15`。

### `def is_valid_grid_id(gid)` — CODE/leo_sim/grid.py:48

校验一个 grid ID 是否为「规范拼写」（canonical）。FACT（docstring grid.py:49-54）：一个物理格只接受一种拼写，拒绝 `G1.0:090:180` 这类别名。实现逐项检查（grid.py:55-73）：必须是 str；切分后恰 3 段且首段以 `G` 开头；deg 可解析为有限正数；`180/deg` 与 `360/deg` 必须是整数（容差 1e-9，grid.py:67-70）；ilat/ilon 在界内（grid.py:71-72）；最后要求 `gid == f"G{deg:g}:{ilat}:{ilon}"` 完全等于规范重编码（grid.py:73）。输入：任意对象；输出：bool。调用方：`trace.py:84`（校验 trace 行的 src/dst 格）；测试 `tests/test_review_round4.py:493`（非规范 ID fail-closed）。

### `def active_aggregate_cells(sites, deg=DEFAULT_GRID_DEG, agg_deg=DEFAULT_AGG_DEG)` — CODE/leo_sim/grid.py:76

把一组站点 (lat, lon) 映射为「聚合格 → 有序细格列表」的稀疏字典（docstring grid.py:81）。实现（grid.py:82-87）：对每个站点算细格 ID 与聚合格 ID，用 set 去重收集，最终按键排序输出 `{agg: sorted(fines)}`。输入：站点坐标列表；输出：`dict[str, list[str]]`，聚合格与细格均排序。调用方未确认（生产代码中未找到调用；仅测试 `tests/test_grid.py:43` 调用）。

---

## 文件 `CODE/leo_sim/model.py`（实测 294 行）

模块级说明：

- 模块 docstring（model.py:1-6）声明：简化 Walker-delta 星座几何；时间秒、距离 km、角度度；位置是 t 的纯函数，kernel 只在当前仿真时刻查询（不读未来星历）。
- imports（model.py:7-9）：`from __future__ import annotations`、`math`。
- 全局常量：`EARTH_RADIUS_KM = 6371.0`（model.py:11）；`EARTH_ROT_RATE_RAD_S = 7.2921159e-5`（model.py:12）；`C_KM_S = 299_792.458`（model.py:13）；`ELEV_RATE_DEG_S = 2.0`（model.py:45）；`RANGE_RATE_KM_S = 20.0`（model.py:46）。后两个是「认证变化检测」的速率上界，推导注释在 model.py:30-44，注释声明它们覆盖高度 300–2000 km、任意倾角、任意地面点的配置域（注释原文，model.py:30-33）。无环境变量读取。

### `def propagation_delay_s(distance_km)` — CODE/leo_sim/model.py:16

传播时延 = `distance_km / C_KM_S`（model.py:17）。输入：距离 km；输出：秒。调用方：`kernel.py:338,434,554,1103,1417`（GSL/ISL 链路时延计算、作为 `choose_next_hop` 的 `prop_delay` 参数传入）、测试 `tests/test_review_round4.py:132,145`。

### `def _sph_to_ecef(lat_deg, lon_deg, r_km)` — CODE/leo_sim/model.py:20

球坐标（度）转直角坐标：`(r·cos lat·cos lon, r·cos lat·sin lon, r·sin lat)`（model.py:21-27）。(FACT) 这是标准的球面→笛卡尔变换；(INFERENCE) 函数名中的 "ECEF"（地固系）语义依赖调用方传入的经度是否已含地球自转修正——`Constellation.subpoint` 在 model.py:193 做了自转修正，因此经 `ecef()` 路径得到的是地固坐标，但直接调用本函数时该保证不成立。输入：纬度/经度（度）、半径 km；输出：(x, y, z) 三元组。调用方：本文件 `Constellation.ecef`（model.py:199）、`elevation_deg`（model.py:206）、`slant_range_km`（model.py:223）；外部调用方未确认。

### `class GeometryCertificationError(RuntimeError)` — CODE/leo_sim/model.py:49

- 定位：model.py:49（无方法，仅 docstring）。
- 职责：(FACT，docstring model.py:49-53) 当 next-change 搜索无法认证答案时抛出（迭代预算耗尽、非有限输入/margin、非法参数）；语义是 fail-closed——只有证明 `(t0, t1]` 内无变化时才允许返回 None。
- 关键状态/结构：无自有状态，继承 `RuntimeError`。
- 输入/输出：异常载体；构造参数为错误消息字符串。
- 依赖关系：由 `_next_change_adaptive` 在 model.py:80,82,84,91,102,112,117,124,135,141,151 等处抛出；测试 `tests/test_review_round4.py` 覆盖 `_next_change_adaptive` 行为（test_review_round4.py:176-186）。

### `def _next_change_adaptive(margin, t0, t1, rate_bound, tol=1e-9, max_iter=1_000_000)` — CODE/leo_sim/model.py:56

- 定位：model.py:56。
- 职责：(FACT，docstring model.py:58-78) 在 `(t0, t1]` 内找 margin(t) 首次过零（available↔unavailable 翻转）的时刻；margin>0 表示可用，恰在阈值上视为不可用；采用认证步进：若真实 margin 速率不超过 `rate_bound`，则在 `|margin|/rate_bound` 内符号不可能翻转，故不会跳过任何穿越；每个被夹逼的穿越用二分法细化到 `tol` 秒。docstring 还声明 SCHEDULING-ONLY 契约（model.py:75-77）：仅供离散事件调度器计算物理链路事件，路由/关联/学习决策不得通过它读未来几何。
- 关键流程：
  - 参数校验（model.py:79-84）：区间非法、`rate_bound` 非有限或 ≤0、`tol` 非法均抛 `GeometryCertificationError`。
  - 内部 `_bisect(lo, hi, ref_sign)`（model.py:85-97）：对夹逼的符号变化做确定性二分到 `tol`；中点 margin 非有限则抛错。
  - 起点采样（model.py:99-118）：`margin(t0)` 非有限抛错；恰为 0 时向 `(t0,t1]` 内步进 epsilon 重采样，仍为零则判定退化并抛错（fail closed）。
  - 主循环（model.py:119-150）：步长 `step = |prev_v|/rate_bound`（下限 `tol`）；候选点越出 t1 时显式评估 `margin(t1)`——同号返回 None（整区间认证无变化），异号则二分返回；候选点 margin 恰为 0 或符号翻转时立即二分返回；非有限抛错。
  - 循环耗尽 `max_iter` 抛 `GeometryCertificationError`，拒绝猜测（model.py:151-153）。
- 输入：margin 回调（t→float）、区间 `(t0, t1]`、速率上界、容差、迭代预算；输出：首次穿越时刻 float，或 None（认证无变化）。
- 依赖关系：被 `Constellation.next_gsl_change`（model.py:273）与 `next_isl_change`（model.py:294）调用；测试 `tests/test_review_round4.py:176-186` 直接调用验证。

### `class Constellation` — CODE/leo_sim/model.py:156

- 定位：model.py:156。
- 职责：(FACT，docstring model.py:157-163) `num_planes × sats_per_plane` 的 Walker-delta 星座几何提供者；类属性 `certifies_change_times = True`（model.py:165）声明其 `next_gsl_change`/`next_isl_change` 使用认证自适应求根。
- 关键状态/结构：卫星数、轨道面数、每面卫星数、高度、倾角、最小仰角、最大 ISL 距离、轨道半径 `self.r`、轨道周期 `self.period_s`（均在 `__init__` 赋值，model.py:172-182）。
- 关键流程/方法：
  - `__init__(num_satellites, num_planes, altitude_km, inclination_deg, min_elevation_deg=25.0, max_isl_km=6000.0)`（model.py:167）：卫星数不能被轨道面数整除时抛 `ValueError`（model.py:170-171）；保存全部参数；`self.r = 6371 + altitude`（model.py:179）；以 μ=398600.4418 km³/s² 算圆轨道周期 `period_s`（model.py:181-182）。
  - `subpoint(sat_id, t)`（model.py:184）：算卫星星下点的测地经纬度（度）与高度。实现：plane/idx 拆分（model.py:186-187），RAAN 按面均分（model.py:188），相位含 `t/period_s`（model.py:189），`lat = asin(sin inc·sin phase)`（model.py:191），惯性经度由 atan2 加 RAAN 再减地球自转 `EARTH_ROT_RATE_RAD_S·t`（model.py:192-193），经度归一化到 [-180,180)（model.py:194）。
  - `ecef(sat_id, t)`（model.py:197）：取 subpoint 后调 `_sph_to_ecef(lat, lon, self.r)` 得直角坐标（model.py:198-199）。
  - `positions(t)`（model.py:201）：返回全部卫星 ECEF 坐标的 tuple（model.py:202）。
  - `elevation_deg(sat_id, lat, lon, t)`（model.py:204）：地面点看卫星的仰角。实现：卫星与地面点各转 ECEF（model.py:205-206），算斜距向量（model.py:207-208），斜距为 0 返回 90.0（model.py:209-210），取地面→卫星向量与当地天顶方向夹角的余角（`asin(cos_z)`，钳到 [-1,1]，model.py:212-214）。
  - `ground_visible(sat_id, lat, lon, t)`（model.py:216）：`elevation_deg > min_elevation_deg` 严格大于（model.py:219），注释说明与认证 next-change 的符号约定一致（model.py:217-218）。
  - `slant_range_km(sat_id, lat, lon, t)`（model.py:221）：卫星到地面点的 ECEF 距离（`math.dist`，model.py:222-224）。
  - `isl_range_km(a, b, t)`（model.py:226）：两星 ECEF 距离（model.py:227）。
  - `neighbors(sat_id, dirs)`（model.py:229）：方向性 ISL 邻居。N/S 为同面 ±1（取模 per_plane，model.py:234-237），E/W 为相邻面同序号（取模 num_planes，model.py:238-241）；只返回 `dirs` 中出现的方向。
  - `gsl_available(sat_id, lat, lon, t)`（model.py:246）：直接返回 `ground_visible(...)`（model.py:247）。
  - `isl_available(a, b, t)`（model.py:249）：ISL 可用性 = 距离 < `max_isl_km` 且距离非 0（model.py:256-257）且 a–b 线段到地心最近点 > 地球半径（地球遮挡检验，投影参数 s 钳到 [0,1]，model.py:258-263）。
  - `next_gsl_change(sat_id, lat, lon, t, limit)`（model.py:265）：以 `elevation_deg - min_elevation_deg` 为 margin（model.py:271-272），用 `ELEV_RATE_DEG_S` 调 `_next_change_adaptive` 返回 `(t, limit]` 内 GSL 可用性首次翻转时刻或 None（model.py:273）。
  - `next_isl_change(a, b, t, limit)`（model.py:275）：margin = `min(max_isl_km - range, 地心净距 - R_earth)`（model.py:281-292，逻辑与 `isl_available` 同构），用 `RANGE_RATE_KM_S` 调 `_next_change_adaptive`（model.py:294）。
- 输入/输出：构造吃星座参数；方法吃 sat_id/坐标/时刻，吐坐标、仰角、距离、可用性 bool、变化时刻。
- 依赖关系：调用 `_sph_to_ecef` 与 `_next_change_adaptive`（同文件）。被调方：`kernel.py:613` 构造（geometry 为 None 时）；kernel 大量使用其方法——`gsl_available`（kernel.py:379,805,1400）、`isl_available`（kernel.py:475,813,1435）、`next_gsl_change`（kernel.py:808）、`next_isl_change`（kernel.py:499,816）、`ground_visible`（kernel.py:993,1081,1192,1271,1338）、`slant_range_km`（kernel.py:339,435）、`isl_range_km`（kernel.py:555,1104）、`elevation_deg`（kernel.py:994,997,1193,1272）、`subpoint`（kernel.py:1349）、`neighbors`（经 `routing.build_topology`，routing.py:72）；`control.build_snapshot` 调 `ground_visible`（control.py:96）与 `positions`（control.py:101）。kernel 在启用 geometry_loss 时检查 `certifies_change_times` 属性，缺失则 fail closed（kernel.py:618-626）。测试 `tests/test_model.py:9-46` 覆盖布局确定性、仰角可见性、方向邻居、斜距/时延为正等。

---

## 文件 `CODE/leo_sim/control.py`（实测 109 行）

模块级说明：

- 模块 docstring（control.py:1-8）声明：控制面包是真实包——占用方向性 ISL 服务时间、相对排队数据有非抢占优先级、最多传播 vis_k 跳、携带 TTL/AoI，是远端状态的唯一来源；卫星本地缓存只含实际到达且未过期的条目。
- imports（control.py:9-11）：`from __future__ import annotations`、`math`。无全局常量，无环境变量读取。

### `class CacheEntry` — CODE/leo_sim/control.py:14

- 定位：control.py:14。
- 职责：(FACT，docstring control.py:15-22) 一条已到达的通告（advertisement）记录；时间契约为 `generated_at <= received_at <= now <= generated_at + ttl_s` 时在 `now` 有效；AoI 从生成时刻起算。
- 关键状态/结构：`__slots__ = ("origin", "payload", "generated_at", "received_at", "ttl_s", "hops")`（control.py:24）。
- 关键流程/方法：
  - `__init__(origin, payload, generated_at, received_at, ttl_s, hops=0)`（control.py:26）：校验三个时间字段为有限数且非 bool（control.py:27-31）、`ttl_s > 0`（control.py:32-33）、`received_at >= generated_at`（control.py:34-36），违例抛 `ValueError`；时间字段转 float 保存（control.py:39-41）；`hops` 记录通告实际走过的 ISL 跳数（control.py:42）。
  - `valid_at(now)`（control.py:44）：`now` 非有限抛 `ValueError`（control.py:47-49）；返回 `generated_at <= received_at <= now <= generated_at + ttl_s`（control.py:50-51）。
  - `aoi(now)`（control.py:53）：返回 `now - generated_at`（control.py:54）。
- 输入/输出：构造吃来源卫星 ID、payload dict、三个时间戳、跳数；`valid_at` 吐 bool，`aoi` 吐秒。
- 依赖关系：由 `LocalCache.put` 持有；kernel 在控制包送达时构造（kernel.py:1157-1158）；`routing.choose_next_hop` 经 `cache.entry(a)` 读取其 payload（routing.py:162-171,193-198）；测试 `tests/test_control.py:36`、`tests/test_review_round4.py:129-328`、`tests/test_learning.py:21-76` 使用。

### `class LocalCache` — CODE/leo_sim/control.py:57

- 定位：control.py:57。
- 职责：(FACT，docstring control.py:58) 每颗卫星一份的、按 origin 键控的已到达控制信息缓存。
- 关键状态/结构：`self._entries: dict[int, CacheEntry]`（control.py:61）；`self.expirations = 0`（control.py:62）。FACT：`expirations` 在 `valid_entries` 里只做 `+= 0`（control.py:76，注释称"过期是惰性观察而非事件"），即该计数器在当前实现中永远为 0。
- 关键流程/方法：
  - `__init__()`（control.py:60）：初始化空字典与 expirations=0。
  - `put(entry)`（control.py:64）：同 origin 已有更新（`old.generated_at >= entry.generated_at`）的条目时拒绝写入（保留较新者，control.py:65-67）；否则覆盖（control.py:68）。
  - `valid_entries(now)`（control.py:70）：遍历全部条目，返回 `valid_at(now)` 为真的子字典（control.py:71-77）。
  - `entry(origin)`（control.py:79）：按 origin 取单条，无则 None（control.py:80）。
  - `count_expired(now)`（control.py:82）：统计当前无效条目数（control.py:83）。
- 输入/输出：`put` 吃 CacheEntry；`valid_entries` 吐 `dict[int, CacheEntry]`。
- 依赖关系：kernel 为每颗卫星建一份（kernel.py:660），送达时 `put`（kernel.py:1159）；`routing.destinations_in_cache` 调 `valid_entries`（routing.py:120），`choose_next_hop` 调 `entry`（routing.py:162,193）；测试 `tests/test_control.py:45-48`、`tests/test_routing.py:18-24` 等使用。

### `def build_snapshot(sat_id, now, geometry, active_cells, isl_queue_bits, isl_propagation_s, slots_used, slots_cap)` — CODE/leo_sim/control.py:86

- 定位：control.py:86。
- 职责：(FACT，docstring control.py:89-93) 生成 `now` 时刻本地可直接观察状态的快照 dict。
- 关键流程：遍历 `active_cells`（{cell: (lat, lon)}），用 `geometry.ground_visible` 筛出当前可见格（control.py:94-97）；组装 dict：origin、generated_at、position（`geometry.positions(now)[sat_id]`）、排序后的 visible_cells、`isl_queue_bits` 与 `isl_propagation_s` 的拷贝、接入时隙用量/上限（control.py:98-109）。注释（control.py:104-106）声明 isl_propagation_s 是快照生成时直接测量的出向链路指标，远端只能在包真实到达后使用。
- 输入：卫星 ID、时刻、geometry 对象、活动格 dict、两个 ISL 指标 dict、时隙计数；输出：快照 dict（注意：kernel 在调用后额外塞入 `serve_cells` 键，kernel.py:1115）。
- 依赖关系：调用 geometry 的 `ground_visible`/`positions`；被 `kernel.py:1110-1114`（`_advertise`）调用；`serve_cells` 键被 `routing.destinations_in_cache` 消费（routing.py:121）。

---

## 文件 `CODE/leo_sim/outage.py`（实测 77 行）

模块级说明：

- 模块 docstring（outage.py:1-16）声明：两种独立机制——geometry loss 是确定性的（端点在 t 时刻不互可用则击落在飞包，无 RNG）；Gilbert-Elliott 是可选、可复现的连续时间两态马尔可夫信道（指数驻留），状态轨迹是给定私有 RNG 流后时间的纯函数，与查询频率无关；默认禁用；GE 只建模随机链路中断，不建模拥塞或切换；传输中丢失只按已占用服务结算，无暂停/恢复、无 ARQ。
- imports（outage.py:17-21）：`from __future__ import annotations`、`math`、`numpy as np`。无全局常量，无环境变量读取。

### `def geometry_loss(available, enabled)` — CODE/leo_sim/outage.py:24

纯函数：返回 `bool(enabled and not available)`（outage.py:26），即启用且当前不可用时判定丢失。输入：两个 bool；输出：bool。调用方未确认（生产代码中未找到调用；kernel 在 kernel.py:1435 等处内联做等价判断而不调本函数；仅测试 `tests/test_fates_outage.py:103-105` 调用）。

### `class GilbertElliott` — CODE/leo_sim/outage.py:29

- 定位：outage.py:29。
- 职责：(FACT，docstring outage.py:30-35) 连续时间两态（好/坏）马尔可夫信道；状态翻转发生在指数驻留时刻，按轨迹顺序惰性抽取——每次翻转恰好消耗一次 RNG 抽取，因此 `is_down(t)` 与调用方查询模式无关；要求 t 非递减。
- 关键状态/结构：`mean_good_s`、`mean_bad_s`、RNG 生成器 `self._gen`、`enabled` 开关、当前坏态标志 `self._bad`、上次查询时刻 `self._last_t`、下次翻转时刻 `self._next_flip`（outage.py:41-48）。
- 关键流程/方法：
  - `__init__(mean_good_s, mean_bad_s, gen, enabled=False)`（outage.py:37）：两个平均驻留必须 > 0，否则 `ValueError`（outage.py:39-40）；初始状态为好（`_bad=False`，outage.py:45）；启用时从好态驻留分布抽首次翻转时刻，禁用时置 `math.inf`（outage.py:48）。
  - `_advance(t)`（outage.py:50）：t 小于上次查询超过 1e-12 时抛 `ValueError`（outage.py:51-52）；while 循环推进所有已过去的翻转：翻转 `_bad`、按新态均值抽下一次驻留并累加到 `_next_flip`（outage.py:54-57）。
  - `is_down(t)`（outage.py:59）：未启用恒返回 False（outage.py:60-61）；否则 `_advance(t)` 后返回 `_bad`（outage.py:62-63）。
  - `next_down(t)`（outage.py:65）：未启用返回 `math.inf`；启用时推进后，若当前坏态返回 t，否则返回 `_next_flip`（outage.py:67-70）。
  - `next_up(t)`（outage.py:72）：未启用返回 t；启用时推进后，若当前坏态返回 `_next_flip`，否则返回 t（outage.py:74-77）。
- 输入/输出：构造吃两个平均驻留秒数、`np.random.Generator`、启用开关；查询方法吃时刻 t，吐 bool 或未来翻转时刻。
- 依赖关系：kernel 为每条 ISL 建一个（kernel.py:459，ISLLink 内），GSL 按需建（kernel.py:771，`_gsl_ge` 惰性创建，缓存于 kernel.py:663 的 `gsl_ge` dict）；kernel 调用 `is_down`（kernel.py:473,830）、`next_up`（kernel.py:502,844）、`next_down`（kernel.py:867）；测试 `tests/test_fates_outage.py:63-93` 验证查询频率无关性与按流独立。

---

## 文件 `CODE/leo_sim/fates.py`（实测 188 行）

模块级说明：

- 模块 docstring（fates.py:1-6）声明：每个 offered 数据包恰有一个终局 fate 或显式 `IN_SYSTEM_AT_STOP`；控制包在独立台账中，不进入数据比特守恒方程。
- imports（fates.py:7）：仅 `from __future__ import annotations`。
- 全局常量：`DATA_FATES`（fates.py:9-19）——9 种数据包终局（DELIVERED、ACCESS_REJECTED、ACCESS_QUEUE_OVERFLOW、ISL_QUEUE_OVERFLOW、GEOMETRY_LOSS_IN_FLIGHT、RANDOM_OUTAGE_IN_FLIGHT、NO_ROUTE、DATA_DEADLINE_EXPIRED、IN_SYSTEM_AT_STOP）；`TERMINAL_LOSS_FATES`（fates.py:20-22）——DATA_FATES 中除 DELIVERED 与 IN_SYSTEM_AT_STOP 外的集合；`CONTROL_FATES`（fates.py:23-25）——7 种控制包终局（DELIVERED、CONTROL_EXPIRED、IN_SYSTEM_AT_STOP、QUEUE_OVERFLOW、GEOMETRY_LOSS_IN_FLIGHT、RANDOM_OUTAGE_IN_FLIGHT、DUPLICATE）；`CONTROL_TERMINAL_LOSS`（fates.py:26-27）；`CONTROL_ARRIVAL_FATES = {"DELIVERED", "DUPLICATE"}`（fates.py:31），注释（fates.py:28-30）说明 CONTROL_EXPIRED 刻意不在其中（TTL 可能在排队时过期——无接收时刻，也可能在接收方传播后过期——有接收时刻）。无环境变量读取。

### `class FateError(RuntimeError)` — CODE/leo_sim/fates.py:34

空异常子类（fates.py:34-35），台账所有违约（重复登记、非法 fate、未登记包、重复 fate、守恒破坏等）的统一抛出类型。由本文件两个台账抛出；测试 `tests/test_fates_outage.py:14-57` 断言其抛出。

### `class DataFateLedger` — CODE/leo_sim/fates.py:38

- 定位：fates.py:38。
- 职责：(FACT，docstring fates.py:39) 每个 offered 数据包一条记录，fate 恰被指派一次。
- 关键状态/结构：`self._fates`（pid→fate）、`self._bits`（pid→bits）、`self._offered`（pid→登记 bits）（fates.py:42-44）。
- 关键流程/方法：
  - `__init__()`（fates.py:41）：初始化三个空 dict。
  - `register(packet_id, bits)`（fates.py:46）：重复登记抛 `FateError`（fates.py:47-48）；记录 offered bits（fates.py:49）。
  - `record(packet_id, fate, bits=None)`（fates.py:51）：fate 不在 DATA_FATES、包未登记、或已有 fate 时分别抛 `FateError`（fates.py:52-57）；bits 缺省取登记值（fates.py:59）。
  - `fate_of(packet_id)`（fates.py:61）：查 fate，无则 None（fates.py:62）。
  - `close_at_stop()`（fates.py:64）：仿真结束时把所有无 fate 的 offered 包置为 `IN_SYSTEM_AT_STOP` 并回填 bits（fates.py:65-69）。
  - `totals()`（fates.py:71）：按 fate 分类汇总 bits，返回 offered/delivered/terminal_loss/in_system 四键 dict（fates.py:72-81）。
  - `check_conservation()`（fates.py:83）：校验 offered = delivered + terminal_loss + in_system，不等则抛 `FateError`（fates.py:84-86）；再校验无缺失 fate 的包（fates.py:87-89）；通过则返回 totals（fates.py:90）。
  - `fate_counts()`（fates.py:92）：返回每种 DATA_FATE 的包数（fates.py:93-96）。
- 输入/输出：吃包 ID/bits/fate 字符串；`totals`/`check_conservation` 吐四键 bits dict，`fate_counts` 吐计数 dict。
- 依赖关系：kernel 构造（kernel.py:688）、`register`（kernel.py:910）、`record`（kernel.py:1493,1508）、`close_at_stop`（kernel.py:1560）、`check_conservation`（kernel.py:1566）、`fate_counts`（kernel.py:1636）；`receipt.py` 用 `DATA_FATES`/`TERMINAL_LOSS_FATES` 重算核验（receipt.py:806-815）；测试 `tests/test_fates_outage.py:8-32`。

### `class ControlFateLedger` — CODE/leo_sim/fates.py:99

- 定位：fates.py:99。
- 职责：(FACT，docstring fates.py:100-110) 每个控制包实例一条记录；守恒式 offered = delivered + terminal_loss + in_system_at_stop；geometry loss 与 random outage 是不同 fate，不合并；每条记录携带接收时刻——DELIVERED/DUPLICATE 与接收方观察到的 CONTROL_EXPIRED 为实际到达时刻，未到达实例（含队列侧 TTL 过期）为 None。
- 关键状态/结构：`self._offered`、`self._fates`、`self._bits`、`self._received`（iid→received_at 或 None）（fates.py:113-116）。
- 关键流程/方法：
  - `__init__()`（fates.py:112）：初始化四个空 dict。
  - `register(iid, bits)`（fates.py:118）：重复实例抛 `FateError`；登记 offered bits（fates.py:119-121）。
  - `record(iid, fate, bits, received_at=None)`（fates.py:123）：fate 非法、未登记、重复记录分别抛错（fates.py:125-130）；到达类 fate（DELIVERED/DUPLICATE）必须带 received_at（fates.py:131-133）；非到达类且非 CONTROL_EXPIRED 的 fate 禁止带 received_at（fates.py:134-136）；落库三个 dict（fates.py:137-139）。
  - `close_at_stop()`（fates.py:141）：无 fate 实例补 `IN_SYSTEM_AT_STOP`、回填 bits、received_at=None（fates.py:142-146）。
  - `totals()`（fates.py:148）：与 DataFateLedger 同构的四键 bits 汇总（fates.py:149-158）。
  - `check_conservation()`（fates.py:160）：守恒等式与缺失 fate 检查，违例抛 `FateError`（fates.py:161-168）。
  - `bits`（property，fates.py:170-175）：以 offered/delivered/terminal_loss/in_system 短键导出 totals。
  - `instances()`（fates.py:177）：导出每实例 `[fate, bits, received_at]` 列表的 dict，供运行台账 artifact 使用（docstring fates.py:178-180；实现 fates.py:181-182）。
  - `fate_counts()`（fates.py:184）：每种 CONTROL_FATE 的实例计数（fates.py:185-188）。
- 输入/输出：吃实例 ID/bits/fate/接收时刻；吐汇总 dict 与实例明细 dict。
- 依赖关系：kernel 构造（kernel.py:689）、`register`（kernel.py:1127,1167）、`record`（kernel.py:1130,1140,1146,1151,1155,1170,1500）、`close_at_stop`（kernel.py:1561）、`check_conservation`（kernel.py:1567）、`fate_counts`（kernel.py:1579）；`receipt.py` 用 `CONTROL_FATES`/`CONTROL_ARRIVAL_FATES`/`CONTROL_TERMINAL_LOSS` 重算核验（receipt.py:834-868）；测试 `tests/test_fates_outage.py:37-57`。

---

## 文件 `CODE/leo_sim/routing.py`（实测 226 行）

模块级说明：

- 模块 docstring（routing.py:1-22）声明信息边界（binding）：deliver 动作用且仅用本星对目的端点的当前直接可见性；hop/delay/capacity 只从本星本地控制缓存（实际到达、未过期的通告）发现"谁能看见目的格"；静态星座拓扑是先验知识且有向，可达性与下一跳成本只在真实有向边上计算（从目标反向邻接），物理双向性在拓扑构建时验证一次；capacity 额外用缓存中的通告队列状态，首跳用本星直接观察的队列；delay/capacity 首跳用直接测量的传播时延、远端边只用已到达未过期的通告值，绝不查全局当前几何；oracle 被显式标注为 ANALYSIS UPPER BOUND，可用全局当前知识（可决定等待），永不喂学习；没有任何策略读未来星历或隐藏全局队列。
- imports（routing.py:23-26）：`from __future__ import annotations`、`heapq`、`collections.deque`。
- 全局常量：`ORACLE_LABEL = "analysis_upper_bound"`（routing.py:28），kernel 在结果里为 oracle 策略打标（kernel.py:1669）。无环境变量读取。

### `def control_broadcast_children(topo, origin, max_hops)` — CODE/leo_sim/routing.py:31

- 定位：routing.py:31。
- 职责：(FACT，docstring routing.py:32-39) 构建一棵确定性最短路径广播树：每个到达的卫星恰有一个父节点，因此一份快照对每颗到达卫星至多产生一次真实控制包传输；保留逐跳传播时延、排队、带宽消耗与丢失/过期，同时避免在带环/跨面链路的星座上指数级重复洪泛。
- 关键流程：origin 不在拓扑中抛 `ValueError`（routing.py:40-41）；max_hops 必须是非负 int 且非 bool（routing.py:42-43）；BFS（routing.py:44-60）：depth 记录跳数，达到 max_hops 不再扩展（routing.py:49-50）；出边按 `(peer_id, direction)` 排序保证确定性平局打破（routing.py:51-53，注释 51-52）；首次到达的 peer 记录深度并把方向追加到 `children[node]`（routing.py:55-59）。返回 `{sat: [方向...]}`。
- 输入：拓扑 dict、源卫星、最大跳数；输出：`dict[int, list[str]]`（每星向其孩子转发时应用的方向列表）。
- 依赖关系：被 kernel 在初始化时为每颗卫星预计算（kernel.py:652-656，`vis_k` 作 max_hops），控制面广播与转发处消费（kernel.py:1120,1161）。

### `def build_topology(geometry, num_sats, dirs)` — CODE/leo_sim/routing.py:63

- 定位：routing.py:63。
- 职责：(FACT，docstring routing.py:64-69) 构建静态先验邻居图；排除自环；物理 ISL 双向性在此处被验证（fail closed）：若几何提供者给出单向边，则拒绝建拓扑而不是在路由中静默捏造反向边。
- 关键流程：对每颗星调 `geometry.neighbors(s, dirs)` 并剔除指向自己的边（routing.py:70-73）；双向性检查：若 `s -d-> n` 而 n 的邻居值中不含 s，抛 `ValueError`（routing.py:74-79）。
- 输入：geometry 对象、卫星数、方向集合（如 `("N","S","E","W")`）；输出：`dict[int, dict[str, int]]`（卫星 → 方向 → 邻居卫星）。
- 依赖关系：调 `Constellation.neighbors`（或任何提供同名方法的几何提供者，routing.py:72）；被 kernel 初始化调用（kernel.py:650-651）；测试 `tests/test_routing.py:29`、`tests/test_review_round4.py:120`（单向边拒绝）。

### `def _reverse_adj(topo)` — CODE/leo_sim/routing.py:83

内部工具：构建真实有向边下的反向邻接——`x ∈ radj[y]` 当且仅当 `topo[x]` 含指向 y 的边（docstring routing.py:84-85；实现 routing.py:86-90，不捏造反向链接）。输入：拓扑；输出：`dict[int, set[int]]`。被 `choose_next_hop` 调用（routing.py:155）；外部调用方未确认。

### `def _multi_source_dist(adj, sources, edge_cost)` — CODE/leo_sim/routing.py:93

多源 Dijkstra：所有 source 距离置 0 入堆（routing.py:96-99）；标准懒删除堆循环（routing.py:100-112），邻居按序遍历（routing.py:104），`edge_cost` 为 inf 的边跳过（routing.py:106-107），松弛带 1e-15 容差（routing.py:109）。输入：邻接 dict、源集合、边成本回调；输出：`dict[int, float]` 距离图。被 `choose_next_hop` 调用（routing.py:205）；外部调用方未确认。

### `def destinations_in_cache(cache, dst_cell, now)` — CODE/leo_sim/routing.py:115

- 定位：routing.py:115。
- 职责：(FACT，docstring routing.py:116-118) 返回其有效且实际到达的通告报告了对 `dst_cell` 的当前服务能力（`serve_cells`）的 origin 列表——仅可见性不足以成为合法出口。
- 关键流程：遍历 `cache.valid_entries(now)`，payload 的 `serve_cells` 含 dst_cell 者收集，排序返回（routing.py:119-123）。
- 输入：LocalCache、目的格 ID、时刻；输出：排序的卫星 ID 列表。
- 依赖关系：调 `LocalCache.valid_entries`；被 `choose_next_hop` 调用（routing.py:145）；测试 `tests/test_review_round4.py:332`。

### `def choose_next_hop(policy, sat, dst_cell, now, geometry, topo, cache, own_queue_bits, isl_rate_bps, prop_delay, oracle_targets=None, best_only=False)` — CODE/leo_sim/routing.py:126

- 定位：routing.py:126。
- 职责：(FACT，docstring routing.py:131-137) 返回 `(有序候选方向列表, status)`；status ∈ `"ok"`（候选非空）、`"no_info"`（无目的通告）、`"unreachable"`（有通告但无路径）；只有通告了 `serve_cells` 当前服务能力的卫星算合法出口。
- 关键流程：
  - 策略校验：policy 必须 ∈ {hop, delay, capacity, oracle}，否则 `ValueError`（routing.py:138-139）。
  - 目标集：oracle 策略直接用调用方传入的 `oracle_targets`（注释：分析上界，调用方传真实当前服务卫星，routing.py:141-143）；其余策略调 `destinations_in_cache`（routing.py:145）。剔除自身（routing.py:146）；为空返回 `([], "no_info")`（routing.py:147-148）。
  - 反向邻接（routing.py:155）：多源搜索从目标沿反向邻接反向扩展，`dist[x]` 即 x 到最近目标的真实有向路径成本（注释 routing.py:150-154,203-204）。
  - 内部 `observed_propagation(a, b)`（routing.py:157-171）：首跳（a == sat）用当前几何直接测量 `prop_delay(geometry.isl_range_km(a, b, now))`（routing.py:159-161）；远端边从 cache 取 a 的条目，无效/缺失返回 None（routing.py:162-164），用 `_dir_of` 找方向后从 payload 的 `isl_propagation_s` 取值，非有限数/负数返回 None（routing.py:165-171）。
  - 各策略分支的边成本 `fwd_cost(a, b)`：
    - `hop`（routing.py:173-174）：每边恒 1.0。
    - `oracle`（routing.py:175-178）：`prop_delay(geometry.isl_range_km(a, b, now))`——用全局当前几何（完美知识）。
    - `delay`（routing.py:179-182）：`observed_propagation` 的值，None 则为 inf（未知即不可走）。
    - `capacity`（routing.py:183-201）：传播时延 + 排队时延 `qb / isl_rate_bps`；首跳队列取本星直接观察的 `own_queue_bits[dir]`（routing.py:188-191），远端边取 cache 条目 payload 的 `isl_queue_bits[dir]`（routing.py:192-198）；队列状态未知（qb 为 None）返回 inf——未知不假设空闲（routing.py:199-200，注释 200）。
  - 多源最短路（routing.py:205）：`edge_cost` 以 `(u,v)→fwd_cost(v,u)` 反向求值。`dist[sat]` 为 inf 返回 `([], "unreachable")`（routing.py:206-207）。
  - 首跳打分（routing.py:208-214）：对 sat 的每个出向边计算 `fwd_cost(sat,n) + dist[n]`，按 `(成本, 方向)` 排序。
  - `best_only`（routing.py:215-218）：只保留与最优成本相对差 ≤ 1e-12 的方向（供学习动作者集合）。
  - 返回 `([方向...], "ok")`（routing.py:219）。
- 输入：策略名、当前卫星、目的格、时刻、geometry、拓扑、LocalCache、本星各方向队列 bits、ISL 速率、传播时延函数、oracle 目标、best_only 开关；输出：(方向列表, status) 二元组。
- 依赖关系：调 `_reverse_adj`、`_multi_source_dist`、`destinations_in_cache`、`_dir_of`（同文件）与 geometry 的 `isl_range_km`；被 kernel 的包转发决策调用（kernel.py:1415-1419，oracle_targets 来自 `self._serving_sats`，best_only 在启用学习时为真）；kernel 消费返回方向时做环路规避（kernel.py:1430）与链路可用性/容量过滤（kernel.py:1433-1440）；测试 `tests/test_routing.py:36-110`、`tests/test_acceptance_review.py:213`。

### `def _dir_of(topo, a, b)` — CODE/leo_sim/routing.py:222

线性查找方向标签：在 `topo[a]` 里找邻居等于 b 的方向并返回，找不到返回 None（routing.py:223-226）。输入：拓扑与两个卫星 ID；输出：方向字符串或 None。被 `choose_next_hop` 内部调用（routing.py:165,190,197）；外部调用方未确认。
# 片段 n1-kernel：新平台离散事件内核

### 文件 `CODE/leo_sim/kernel.py`（实测 1678 行）

模块级说明：

- 第 1–41 行：模块 docstring，声明本文件是「有界 SimPy 离散事件内核」，并声明四条契约：(a) 数据路径不含 Gateway，为 trace → TrafficEndpoint → 有限关联（K 个接入槽 + 捕获时延）→ 卫星入站 → 动态有限 ISL → 控制面缓存 → 合法下行发现 → 有限下行 → 目的端点（1–8）；(b) 公平有限接入：端点按当前需求请求关联，卫星侧确定性 FIFO 等待队列，持有者按 slot_lease_s 或 idle_release_s 轮换（10–20）；(c) 传输竞速语义：每次服务在「服务完成 / 几何丢失 / Gilbert-Elliott 中断 / 数据期限 / 硬退役」之间竞速，无 ARQ、无暂停恢复（22–31）；(d) 闭区间 horizon `[0, duration_s]`，由专门的 closer 进程保证时钟到达精确 horizon（33–35）；GSL 上下行是显式全双工资源、各自独立容量、按 DRR 共享；ISL 每方向一条队列、数据与控制共享单一容量、控制非抢占优先（37–40）。以上 (a)–(d) 为 docstring 声明；对应实现位置在下文各符号条目中逐条标注。
- 第 42 行：`from __future__ import annotations`。
- 第 44–52 行 imports：`math`（44）、`collections.deque`（45）、`numpy as np`（47）、`simpy`（48）；包内导入 `control, fates, grid as gridmod, learning as _learning, model`（50）、`outage, rng as rngmod, routing`（51）、`trace as tracemod`（52）。
- 第 54 行：`LearningUnavailable = _learning.LearningUnavailable`，把 `learning.py:89` 定义的异常类别进本模块命名空间（FACT）。CODE/ 内 grep 未发现以 `kernel.LearningUnavailable` 形式引用它的代码（`__main__.py:251` 捕获的是 `learning.LearningUnavailable`）；该别名的消费方未确认。
- 无环境变量读取、无其他模块级常量（FACT，基于对 1–56 行的逐行阅读）。

#### 全局结构速览（SimPy 事件流 / 队列·账本·计数器结构 / 跨文件调用边）

**SimPy 事件流（FACT，均指 kernel.py 行号）**

- `Kernel.__init__` 创建 `simpy.Environment`（600）。服务进程在构造时自注册：`UplinkServer._run`（265）、`DownlinkServer._run`（356）、`ISLLink._run`（463）。
- `Kernel.__init__` 末尾按固定顺序注册周期/一次性进程（724–733）：逐端点 `_endpoint_ticker`（724–725）→ 控制面启用时逐星 `_control_advertiser`（726–728）→ 逐端点 `_emitter`（729–730）→ 逐星 `_pending_ticker`（731–732）→ 最后 `_horizon_closer`（733）。注释（719–723）声明该创建顺序使 t=0 的切换 tick 与广告先于 t=0 的发射、且 horizon 上的事件仍被处理；该「创建顺序即同时刻排序」的保证依赖 SimPy 调度语义，本文件内无法验证（未确认）。
- `Kernel.run`（1512）不用 `env.run()`，而是手动循环：`env.peek()` 取下一事件时刻（1519），超过 horizon 或为 `math.inf` 则停（1522），否则 `env.step()` 并计数（1524–1525），事件数超 `cfg_ex["max_events"]` 抛 `CapExceeded`（1526–1527）；`peek()` 抛任何异常时直接结束循环（1520–1521，捕获裸 `Exception`，触发条件代码未注明，未确认）。
- `_horizon_closer`（895）`timeout(self.horizon)`（899）后记录 `closed_at = env.now`（900），保证时钟到达精确 horizon。
- 传输过程统一走 `_transmit`（784）这一 SimPy 进程：内部用 `env.timeout` 等待（858、877）、用 `wait | interrupt` 竞速硬退役中断（879）。
- 传播时延段由一次性进程承载：`_ingress_after_prop`（340 处 spawn）、`_deliver_after_prop`（436）、`_ctrl_arrive_after_prop`（557）、`_isl_arrive_after_prop`（559）；关联激活由 `_activate_after_delay`（1209）、硬退役中断由 `_fire_interrupt`（1052、1307）spawn。

**队列 / 账本 / 计数器结构（FACT）**

- 端点上队列：`TrafficEndpoint.queue`（`deque[DataPacket]`，205）、`queued_bits`（206）、`area`（`QueueArea`，208）；容量上限 `cfg_access["uplink_queue_bits"]` 在 `_emitter` 中检查（921）。
- 下行队列：`DownlinkServer.queues`（cell → `deque`，349）、`queued_bits`（350）、`area`（351）；容量 `cfg_access["downlink_queue_bits"]` 由 `room`（358–359）检查。
- ISL 队列：`ISLLink.data_q`/`ctrl_q`（450–451）、`data_bits`/`ctrl_bits`（452–453）、`data_area`/`ctrl_area`（454–455）；数据与控制共享单一容量 `cfg_links["isl_queue_bits"]`，由 `_used`+`room`（465–469）检查。
- 卫星侧待决队列：`Kernel.pending`（每星一个 `list[DataPacket]`，661）；公平接入状态 `slots`（659）、`access_wait`（每星 FIFO dict cell→请求时刻，668）、`access_last_busy`（669）、`access_stats`（670–675）。
- 控制面状态：`caches`（每星 `control.LocalCache`，660）、`seen_ctrl`（每星 `(origin, seq)` 集合，662）、`ctrl_seq`/`ctrl_iid` 计数器（699–700）。
- 中断账本：`self.ledger = fates.DataFateLedger()`（688，定义 fates.py:38）、`self.ctrl_ledger = fates.ControlFateLedger()`（689，定义 fates.py:99）；`run()` 末尾 `close_at_stop`（1560–1561），自然结束时 `check_conservation()`、中断时 `totals()`（1562–1567）。
- 占用与机制计数器：`occupied`（四类占用秒数，691–692）、`service_log`（693–694）、`mech`（GE 查询/等待/失败、控制面各阶段、MBB、learning 等计数，701–716）、`data_packet_count`（698）、`deliveries`（690）、`handover_events`（695）、`monitor_log`（696–697）。
- 结果下游消费方：`Kernel.run()` 返回的 dict（1628–1671）被 `CODE/leo_sim/receipt.py` 读取（`result["fates"]`、`result["control"]["instances"]`、`result["mechanism_counters"]`、`result["occupied"]`、`result["queue_area_bits_s"]`、`result["handover"]["events"]`、`result["access"]`、`result["deliveries"]`、`result["mechanisms"]`、`result["research_eligible"]`、`result["routing_label"]`、`result["totals"]` 等，见 receipt.py:275–320）（FACT）。

**跨文件调用边（FACT，定义行号均已逐一核对）**

kernel.py 调用出边：
- `fates`：`DataFateLedger`（688←fates.py:38）、`ControlFateLedger`（689←fates.py:99）、`FateError`（1528 捕获←fates.py:34）。
- `routing`：`build_topology`（650←routing.py:63）、`control_broadcast_children`（653←routing.py:31）、`choose_next_hop`（1415←routing.py:126）、`ORACLE_LABEL`（1669←routing.py:28）。
- `learning`（`_learning`）：`LearningUnavailable`（54←learning.py:89）、`require_tensorflow`（741←learning.py:93）、`TensorflowDDQN`（604←learning.py:276）、`own_state`（1340←learning.py:532）、`destination_features`（1350←learning.py:559）、`build_observation`（1352←learning.py:724）、`ACTIONS`（1406、1443、1491、1505←learning.py:64）、`CONTRACT_DIMS`（1490、1504←learning.py:56 及 85–86）。
- `control`：`LocalCache`（660←control.py:57）、`build_snapshot`（1110←control.py:86）、`CacheEntry`（1157←control.py:14）。
- `outage`：`GilbertElliott`（459、771←outage.py:29）。
- `model`：`Constellation`（613←model.py:156）、`propagation_delay_s`（338、434、554、1103、1417←model.py:16）；geometry 对象方法 `gsl_available`/`isl_available`/`next_gsl_change`/`next_isl_change`/`ground_visible`/`elevation_deg`/`slant_range_km`/`isl_range_km`/`subpoint`（分别对应 model.py:246/249/265/275/216/204/221/226/184）及属性 `certifies_change_times`（619←model.py:165）。
- `rng`（`rngmod`）：`link_stream`（461、773←rng.py:37）。
- `trace`（`tracemod`）：`validate_packet_rows`（639←trace.py:46）。
- `grid`（`gridmod`）：`grid_center`（204←grid.py:33）。

kernel.py 被调用入边：
- `CODE/leo_sim/__main__.py:246` 调用 `kernel.run_simulation(resolved, rows, learning_out_dir=...)`；`__main__.py:254` 捕获 `kernel.CapExceeded`；`__main__.py:251` 捕获 `learning.LearningUnavailable`（未捕获 `KernelError` 基类本身，245–256 的 except 列表中无 `KernelError` 分支）（FACT）。
- `CODE/leo_sim/acceptance.py:108`、`CODE/leo_sim/comparison.py:106`、`CODE/leo_sim/platform_check.py:65` 与 `:109` 均调用 `kernel.run_simulation`。
- `CODE/scripts/remote/remote_job.py:250` 以子进程方式执行 `python -m CODE.leo_sim run`（`sys.executable, "-m", "CODE.leo_sim", "run"`），即经 `__main__.py` 间接进入 kernel（FACT）。
- 测试入边（非逐行阅读，仅作行为佐证）：`CODE/leo_sim/tests/test_kernel.py:3` 声明所有测试经 `kernel.run_simulation` 驱动真实内核；`test_review_regressions.py:200–203` 直接构造 `kernel.Kernel`、`kernel.DataPacket`、`kernel.ControlPacket`；`test_acceptance_review.py:190–191` 直接构造 `kernel.Kernel` 与 `kernel.DataPacket`；`test_review_round2.py:190–191` 断言未认证 geometry 抛 `kernel.KernelError`；其余调用文件包括 test_handover.py、test_control.py、test_routing.py、test_learning.py、test_review_round2/3/4.py、test_outage_trace_gaps.py、test_acceptance_review.py。
- 仓库级 grep（`--include='*.py'`，排除 `./CODE/`）未发现 CODE/ 之外的 `import kernel`/`leo_sim.kernel` 调用方（FACT，检索范围限制：仅 .py 文件与上述模式）。

#### `class KernelError` — CODE/leo_sim/kernel.py:57
- 定位：CODE/leo_sim/kernel.py:57
- 职责：`RuntimeError` 的子类，内核错误基类；类体仅 `pass`（58）（FACT）。
- 关键状态/结构：无（空类体）。
- 关键流程/方法：无方法。
- 输入/输出：不适用（异常类型）。
- 依赖关系：被 `CapExceeded` 继承（61）；在 `Kernel.__init__`（623，geometry 不能认证变更时刻时）与 `Kernel._decide`（1409，DDQN 在 deliver-only 掩码下选出非 deliver 动作时）抛出；`Kernel.run` 的 except 列表（1528）不含它；测试佐证 test_review_round2.py:190–191。

#### `class CapExceeded` — CODE/leo_sim/kernel.py:61
- 定位：CODE/leo_sim/kernel.py:61
- 职责：`KernelError` 子类；docstring（62）声明语义为「配置的上界（事件/实体/包）被超过，fail closed」（FACT，引自 docstring）。
- 关键状态/结构：无（空类体，仅 docstring）。
- 关键流程/方法：无方法。
- 输入/输出：不适用。
- 依赖关系：抛出点——`Kernel.__init__`（686，实体数超 `max_entities`）、`Kernel._count_data_packet`（764，超 `max_packets`）、`Kernel.run`（1527，超 `max_events`）；捕获点——`Kernel.run`（1528，转为 interrupted 结果）、`__main__.py:254`（退出码 4）。

#### `class DataPacket` — CODE/leo_sim/kernel.py:65
- 定位：CODE/leo_sim/kernel.py:65
- 职责：数据包载体对象，`__slots__` 固定字段集（66–68）（FACT）。
- 关键状态/结构：`pid, src, dst, bits, deadline, emitted_at, path, assigned_sat, learning_state, learning_action, learning_reward`（66–68）。
- 关键流程/方法：`__init__`（70）赋值六个构造参数，`path` 初始化为空 list（77），`assigned_sat` 置 None（78），三个 learning 字段置 None（79–81）。
- 输入/输出：构造入参 `(pid, src, dst, bits, deadline, emitted_at)`；对象在 kernel 内流转，`path` 在 `_ingress_after_prop`（1470）与 `_isl_arrive_after_prop`（1479）追加，`assigned_sat` 在 297、927、1310、1239–1240、1261–1263 等处读写。
- 依赖关系：由 `Kernel._emitter`（908–909）创建；test_review_regressions.py:202、test_acceptance_review.py:191 直接构造；被 `fates.DataFateLedger.register/record`（910、1493、1508）登记。

#### `class QueueArea` — CODE/leo_sim/kernel.py:84
- 定位：CODE/leo_sim/kernel.py:84
- 职责：排队比特×秒积分的精确累加器；docstring（85–86）声明变更必须带当前时刻调用 add/remove、`close(t)` 在停止时刻结算（FACT，引自 docstring 与实现）。
- 关键状态/结构：`__slots__ = ("area", "bits", "last")`（88）：累计积分、当前比特数、上次结算时刻。
- 关键流程/方法：`__init__`（90）三者清零；`_acc`（95）把 `bits * (now - last)` 累入 `area` 并更新 `last`；`add`（99）先 `_acc` 再加比特；`remove`（103）先 `_acc` 再减比特；`close`（107）只在时刻 `t` 结算一次 `_acc`。
- 输入/输出：入 `bits: int, now/t: float`；积分结果经 `.area` 属性读取。
- 依赖关系：被 `TrafficEndpoint`（208）、`DownlinkServer`（351）、`ISLLink`（454–455）持有；`Kernel.run` 在停止时刻统一 `close`（1543–1549）并汇总进 `queue_area` dict（1550–1557）。

#### `class ControlPacket` — CODE/leo_sim/kernel.py:111
- 定位：CODE/leo_sim/kernel.py:111
- 职责：控制面包载体；docstring（112–121）声明字段契约（origin、seq、generated_at、received_at、ttl、remaining_hops、payload_bits、validity/AoI），并声明 `received_at` 在物理到达前为 None、`valid_at(t)` 为生成时刻起的 TTL 窗口、AoI 为 `t - generated_at`（FACT，引自 docstring；实现见下）。
- 关键状态/结构：`__slots__ = ("iid", "origin", "seq", "generated_at", "_received_at", "ttl_s", "remaining_hops", "payload_bits", "payload")`（123–124）。
- 关键流程/方法：`__init__`（126）先校验四类字段——`generated_at` 须为有限非负数值（128–131）、`ttl_s` 有限且 >0（132–134）、`remaining_hops` 非负 int（135–137）、`payload_bits` 正 int（138–139），不合法抛 `ValueError`——再赋值（140–148，`_received_at` 置 None）；`bits` property（151）返回 `payload_bits`（注释称其为兼容别名）；`received_at` property（156）返回 `_received_at`；`mark_received`（159）只允许设置一次（160–161）且要求时刻有限且 ≥ generated_at（162–166），否则 `ValueError`；`valid_at`（168）返回 `generated_at <= t <= generated_at + ttl_s`；`aoi`（171）校验时刻后返回 `t - generated_at`（172–175）。
- 输入/输出：构造入参 `(iid, origin, seq, generated_at, ttl_s, remaining_hops, bits, payload)`；`payload` 携带快照 dict。
- 依赖关系：由 `Kernel._advertise`（1123–1126）与 `Kernel._ctrl_arrive_after_prop` 的转发分支（1164–1166）创建；经 `ISLLink.put_ctrl`（483）入队；`_transmit`（819–821）用其 TTL 计算过期；字段校验的测试佐证 test_review_round4.py:415、443、447。

#### `class Link` — CODE/leo_sim/kernel.py:178
- 定位：CODE/leo_sim/kernel.py:178
- 职责：端点↔卫星关联状态记录；docstring（179–183）声明 `cause` 记录进入 retiring 的原因（"mbb" | "lease"），`interrupt` 在 `retire_at` 触发使在途服务与硬退役期限竞速（FACT，引自 docstring）。
- 关键状态/结构：`__slots__ = ("sat", "state", "since", "ready_at", "retire_at", "cause", "interrupt")`（185–186）；行内注释（191）列出 `state` 取值 `acquiring | active | retiring`。
- 关键流程/方法：`__init__`（188）逐字段赋值（默认 `ready_at=0.0, retire_at=None, cause=None, interrupt=None`）。
- 输入/输出：纯数据载体，无行为方法。
- 依赖关系：由 `Kernel._associate`（1199–1200）创建（`interrupt=self.env.event()`）；状态迁移分布在 `_activate_after_delay`（1213–1214）、`_access_tick_endpoint`（1049–1051）、`_evaluate_handover`（1303–1306）、`_on_link_retired`（1229–1242）；`interrupt` 由 `_fire_interrupt`（779–782）触发。

#### `class TrafficEndpoint` — CODE/leo_sim/kernel.py:199
- 定位：CODE/leo_sim/kernel.py:199
- 职责：稀疏激活的地面端点：持有 cell 坐标、上行 FIFO 队列与逐星 `Link` 表（FACT）。
- 关键状态/结构：`__slots__ = ("cell", "lat", "lon", "queue", "queued_bits", "links", "area")`（200）。
- 关键流程/方法：`__init__`（202）用 `gridmod.grid_center(cell)`（204←grid.py:33）取 `lat, lon`，初始化 `queue` 为 `deque[DataPacket]`（205）、`queued_bits=0`（206）、`links: dict[int, Link]`（207）、`area=QueueArea()`（208）；`primary_link`（210）在 `links` 中选出状态为 `active`/`acquiring` 且 `since` 最新的一条（211–217），无则返回 None。
- 输入/输出：构造入参 `cell`（grid id 字符串）；`primary_link` 返回 `Link | None`。
- 依赖关系：由 `Kernel.__init__`（647）按 trace 行创建；被 `UplinkServer._pick`（267–280）、`DownlinkServer._servable`（368–381）及 Kernel 各接入/切换方法读写。

#### `class _DRRMixin` — CODE/leo_sim/kernel.py:220
- 定位：CODE/leo_sim/kernel.py:220
- 职责：Deficit Round-Robin 选择逻辑 mixin（docstring 221）（FACT）。
- 关键状态/结构：`quantum`（float）、`deficit: dict[str, float]`、`rr_cursor`（int），由 `_drr_init` 建立（223–226）。
- 关键流程/方法：`_drr_init`（223）存 quantum（转 float）并初始化 deficit dict 与轮转游标；`_drr_select`（228）——docstring（229–237）声明按轮转序访问有积压的 key、每次访问加一个 quantum、队首包 ≤ 累积赤字即服务、超 quantum 的包跨多次访问累积赤字——实现：先对有序 `items` 用 `pick(k)` 取队首包并过滤空（238–241），之后 `while True` 循环中每轮从 `rr_cursor % n` 起扫描（244–246），给被访问 key 加 quantum（248–249），首个满足 `pkt.bits <= dc` 的 key 扣减赤字、推进游标并返回 `(k, pkt)`（250–253）；`avail` 为空返回 None（240–241）。
- 输入/输出：`_drr_select(items, pick)` 入有序 key 列表与取包函数，返回 `(key, pkt)` 或 None。
- 依赖关系：被 `UplinkServer`（255）、`DownlinkServer`（343）继承；行为佐证 test_kernel.py:256（`test_drr_bit_fairness_with_mixed_packet_sizes`，混合包长下的比特级公平）。

#### `class UplinkServer` — CODE/leo_sim/kernel.py:255
- 定位：CODE/leo_sim/kernel.py:255
- 职责：每星一个的共享 GSL 上行服务进程，按 DRR 在已关联端点间调度（docstring 256）（FACT）。
- 关键状态/结构：`k`（Kernel 引用，259）、`sat`（260）、`wake`（SimPy event，261）、`current`（在服务的 `(ep, pkt)`，262）、`_svc`（服务起始记账 tuple，263）、DRR 状态（264）。
- 关键流程/方法：`__init__`（258）初始化上述状态、以 `cfg_access["drr_quantum_bits"]` 调 `_drr_init`（264），并 `env.process(self._run())` 自注册（265）；`_pick`（267）——返回该端点队列中本条链路可服务的首个包：链路不存在或非 `active`/`retiring` 返回 None（269–271），retiring 且已过 `retire_at` 返回 None（272–273），retiring 时只服务 `assigned_sat == self.sat` 的包（275–277），active 时服务 `assigned_sat in (None, self.sat)` 的首包（278–279），注释称保持逐链路 FIFO（268）；`_run`（282）——主循环：对所有端点 cell 排序后 `_drr_select`（285–286），无可服务则挂起等 `wake`（288–290）；选中后从端点队列移除并更新 `queued_bits`/`area`（293–295）、未指派则指派本星（296–297）、记 `current`（298）、`_note_busy`（299）、写 `service_log["uplink"]`（300）；服务时长 `bits / ul_rate_bps`（301），记 `_svc`（302），`yield` `Kernel._transmit`（303–305，`link_ref=("gsl", sat, ep, link)`，占用键 `"gsl_uplink_s"`）；返回后写 `service_log["uplink_bits"]`（306）并清 `_svc`/`current`（307–308）；`outcome == "retired"` 时把包全量重新放回队首、恢复计数、`_on_link_retired` 并唤醒该端点所有链路的上行服务（309–322）；`"stalled"` 时放回队首，已到 horizon 则跳出循环，否则挂起（323–334）；其他非 `"ok"` 结果直接继续（335–336）；`"ok"` 时按 `geometry.slant_range_km` + `model.propagation_delay_s` 算传播时延并 spawn `_ingress_after_prop`（337–340）。
- 输入/输出：消费 `TrafficEndpoint.queue` 中的 `DataPacket`；产出为传入 `_transmit` 的服务与 `_ingress_after_prop` 进程。
- 依赖关系：由 `Kernel.__init__`（678）逐星创建；调用 Kernel 的 `_note_busy`、`_transmit`、`_on_link_retired`、`_poke`、`_ingress_after_prop`；被 `_emitter`（934–935）、`_associate`（1207）、`_activate_after_delay`（1215）经 `wake` 唤醒。

#### `class DownlinkServer` — CODE/leo_sim/kernel.py:343
- 定位：CODE/leo_sim/kernel.py:343
- 职责：每星一个的共享 GSL 下行服务进程：有限共享队列，按 DRR 在目的端点间调度（docstring 344）（FACT）。
- 关键状态/结构：`queues: dict[str, deque[DataPacket]]`（349）、`queued_bits`（350）、`area`（351）、`wake`（352）、`current`（353）、`_svc`（354）、DRR 状态（355）。
- 关键流程/方法：`__init__`（346）初始化上述状态并自注册 `_run` 进程（356）；`room`（358）返回 `queued_bits + bits <= cfg_access["downlink_queue_bits"]`；`put`（361）按 `pkt.dst` 入队、累加计数与面积、`_note_busy(pkt.dst)` 并 `poke(wake)`（362–366）；`_servable`（368）——该 cell 队首包在本星当前可合法服务时返回之：队列空返回 None（370–372），链路非 `active`/`retiring` 返回 None（374–376），retiring 且过 `retire_at` 返回 None（377–378），`geometry.gsl_available` 此刻不成立返回 None（379–380），否则返回 `q[0]`（381）；`_run`（383）——主循环：先把「端点已不再持有本星关联」的队首包退回 `Kernel.pending[sat]`（386–396），再 `_drr_select`（397）；空则挂起（398–401）；选中后出队、更新计数（403–405）、记 `current` 与 `service_log["downlink"]`（406–408）；时长 `bits / dl_rate_bps`（409），记 `_svc` 并 `yield _transmit`（410–413，占用键 `"gsl_downlink_s"`）；`"retired"` 时包进 `pending[sat]` 并 `_on_link_retired`（416–421）；`"stalled"` 时放回队首、到 horizon 跳出、否则挂起（422–430）；非 `"ok"` 继续（431–432）；`"ok"` 时算传播时延并 spawn `_deliver_after_prop`（433–436）。
- 输入/输出：入 `DataPacket`（经 `put`）；产出 `_deliver_after_prop` 进程。
- 依赖关系：由 `Kernel.__init__`（679）逐星创建；`put` 的调用方是 `Kernel._decide`（1410）；队列被 `_sweep_downlink_queues`（954–966）清扫、被 `_downlink_demand_sats`（983）查询。

#### `class ISLLink` — CODE/leo_sim/kernel.py:439
- 定位：CODE/leo_sim/kernel.py:439
- 职责：一条有向 ISL：单一有限容量由数据与控制共享，控制非抢占优先（docstring 439–443：排队的控制在链路下次空闲时越过排队数据，在途服务永不中断；可用性每次使用时重查）（FACT，引自 docstring 与实现）。
- 关键状态/结构：`data_q`/`ctrl_q`（450–451）、`data_bits`/`ctrl_bits`（452–453）、`data_area`/`ctrl_area`（454–455）、`wake`（456）、`_svc`（457）、`ge`（本链路私有 GilbertElliott，458–462）。
- 关键流程/方法：`__init__`（445）记录 `sat/dir/peer`、初始化上述队列与计数，并以 `cfg_links["ge_isl"]` 的均值参数与 `rngmod.link_stream(seed, f"isl:{sat}:{direction}")` 构造私有 GE 通道（458–462，`enabled=kern.ge_enabled`），自注册 `_run`（463）；`_used`（465）返回数据+控制比特和；`room`（468）检查 `_used() + bits <= cfg_links["isl_queue_bits"]`；`available_now`（471）——GE 启用且此刻 down 返回 False（473–474），否则返回 `geometry.isl_available(sat, peer, now)`（475）；`put_data`（477）/`put_ctrl`（483）分别入对应队列、累加计数与面积并 `poke(wake)`；`_run`（489）——主循环：先 `_expire_waiting`（492），双队列空则挂起（493–496）；`available_now` 为假时计算最早恢复时刻（几何 `next_isl_change` 与 `ge.next_up`，498–503）与队内包过期时刻（504–506），取落在 `(now, horizon]` 的最早者做带超时等待（507–514），无可等时刻则挂起（509–512）；可服务时控制优先出队（518–519，`is_ctrl = bool(self.ctrl_q)`），更新计数（520–526）、控制则 `mech["control_tx_started"] += 1`（523）、写 `service_log["isl"]`（527–528）；时长 `bits / isl_rate_bps`（529），占用键 `"ctrl_isl_s"`/`"isl_s"`（530），记 `_svc` 并 `yield _transmit`（531–533，`link_ref=("isl", sat, peer, ge)`）；`"stalled"` 放回对应队首、到 horizon 跳出、否则挂起（535–548）；非 `"ok"` 继续（549–550）；`"ok"` 时控制包 `mech["control_tx_completed"] += 1`（551–552），按 `isl_range_km` 算传播时延（553–555），控制 spawn `_ctrl_arrive_after_prop`（556–557）、数据 spawn `_isl_arrive_after_prop`（558–559）；`_expire_waiting`（561）——把队列里已到 TTL/期限的包逐条判负：控制包 `now >= generated_at + ttl_s` 记 `CONTROL_EXPIRED`（567–571），数据包过 `deadline` 记 `DATA_DEADLINE_EXPIRED`（576–580），其余保留（572–574、581–583）；docstring（562–564）声明即使 ISL 永久 down 也要在包自身期限处退役。
- 输入/输出：入 `DataPacket`/`ControlPacket`（`put_data`/`put_ctrl`）；产出 `_isl_arrive_after_prop`/`_ctrl_arrive_after_prop` 进程与 `_fail` 判负。
- 依赖关系：由 `Kernel.__init__`（681–683）按 `routing.build_topology` 的输出逐方向创建；`put_data` 调用方为 `Kernel._decide`（1447），`put_ctrl` 调用方为 `_advertise`（1133）与 `_ctrl_arrive_after_prop`（1173）。

#### `class Kernel` — CODE/leo_sim/kernel.py:586
- 定位：CODE/leo_sim/kernel.py:586（类体延伸至 1671）
- 职责：离散事件内核本体：构造全部仿真状态与进程（587–733），承载接入控制、控制面、切换、路由决策、学习钩子与终止结算的全部逻辑（FACT）。
- 关键状态/结构：配置切片 `cfg_sc/cfg_access/cfg_links/cfg_cp/cfg_rt/cfg_learning/cfg_ex`（591–597）；`horizon`、`time_step`（598–599）；`env`（600）；`learner`（603–610）；`geometry`（612–627）；速率 `ul/dl/isl_rate_bps`（632–634）；`endpoints`（642–648）；`topo`（650–651）；`control_children`（652–656）；逐星状态 `slots/caches/pending/seen_ctrl`（659–662）与 `gsl_ge`（663）；公平接入状态（668–675）；服务器数组 `uplinks/downlinks/isls`（678–683）；账本与计数器（688–717，见上方速览）。
- 关键流程/方法（逐方法，共 44 个）：
  - `__init__`（587）：读配置切片（589–597）；建 `simpy.Environment`（600）；过 `learning_gate`（601）；`learning.algorithm == "ddqn"` 时构造 `_learning.TensorflowDDQN`（603–610，种子取 learning.seed 否则 scenario.seed）；`geometry` 缺省用 `model.Constellation`（612–617）；`links.geometry_loss` 为真而 provider 无 `certifies_change_times` 属性时抛 `KernelError`（618–626）；按 `(emit_time_s, packet_id)` 排序 trace 行并 `tracemod.validate_packet_rows` 校验（638–641）；为 trace 出现的 src/dst cell 建 `TrafficEndpoint`（642–648）；建拓扑与控制广播子节点表（650–656）；初始化逐星状态与公平接入状态（658–675）；创建上/下行服务器与 ISL（677–684），实体数超 `max_entities` 抛 `CapExceeded`（685–686）；建账本、计数器（688–717）；按固定顺序注册进程（719–733）。
  - `learning_gate`（737，`@staticmethod` 736）：当 `routing.learning_enabled` 或 `learning.algorithm != "none"`（738–739）时调用 `_learning.require_tensorflow()`（741），不可用时由其抛 `LearningUnavailable`。
  - `_poke`（743）：事件未触发则 `succeed()`（744–745）。
  - `_note_busy`（747）：把 `access_last_busy[cell]` 刷为当前时刻（749）。
  - `_log`（751）：`monitor` 开启时向 `monitor_log` 追加 `(now, kind, sorted(kv))`（752–753）。
  - `_count_data_packet`（755）：`data_packet_count += 1`，超 `cfg_ex["max_packets"]` 抛 `CapExceeded`（762–764）；docstring（756–761）说明控制包不在此计数。
  - `_gsl_ge`（766）：按 `(sat, cell)` 懒建 GSL 用 `GilbertElliott`（767–776），RNG 流为 `rngmod.link_stream(seed, f"gsl:{sat}:{cell}")`（773）。
  - `_fire_interrupt`（779）：`timeout` 到 `at` 后触发 `link.interrupt`（780–782）。
  - `_transmit`（784）：通用服务进程。按 `link_ref` 是 `("gsl", sat, ep, link)` 还是 `("isl", a, b, ge)` 组装 `avail`/`next_change` 闭包与 GE 通道（799–816）；按包类型取过期时刻与 fate 名（819–824，`ControlPacket` 用 TTL→`CONTROL_EXPIRED`，数据包用 deadline→`DATA_DEADLINE_EXPIRED`）；主循环：查 GE/几何可用性（826–830，GE 查询计数 828）；retiring 链路过 `retire_at` 直接返回 `"retired"`（831–836）；链路 down 时算最早恢复（838–845），恢复晚于过期则 `_fail` 并返回 `"fail"`（846–848），horizon 内永不恢复则等待到 horizon 返回 `"stalled"`（849–857），否则睡到最早恢复点重查（858–859）；链路 up 时计算服务结束点与最早失败点——几何丢失（862–865）、GE 下转（866–869）、过期（870–871）、硬退役（872–873）；用 `wait | interrupt` 竞速（876–881）；按实际经过时间记账 `occupied[occ_key]`（882）；被中断提前唤醒则重算整场比赛（883–884）；到期按 `fail_kind` 返回 `"ok"`/`"retired"`，或对 `RANDOM_OUTAGE_IN_FLIGHT` 计数（890）后 `_fail` 并返回 `"fail"`（885–892）。docstring（785–798）声明返回值语义与「服务未开始前的等待不算暂停/恢复」。
  - `_horizon_closer`（895）：`timeout(self.horizon)`（899）后写 `closed_at = env.now`（900）。
  - `_emitter`（902）：按行发射——睡到 `emit_time_s`（903–906）；`_count_data_packet`（907）；构造 `DataPacket` 并 `ledger.register`（908–910）；生成即过期判 `DATA_DEADLINE_EXPIRED`（911–914）；无链路且无任何可见星判 `ACCESS_REJECTED`（915–920）；超 `uplink_queue_bits` 判 `ACCESS_QUEUE_OVERFLOW`（921–923）；`assigned_sat` 取当前 active 主链路星否则 None（924–927）；入队并更新计数、面积、busy 戳（928–931）；无链路时 `_request_or_grant`（932–933）；唤醒该端点所有链路的上行服务（934–935）；`yield timeout(0.0)` 让服务进程在同一时刻先出队（936–938，注释称保证同时刻顺序确定性）。
  - `_endpoint_ticker`（940）：每 `time_step` 循环执行 `_sweep_endpoint_queue`（942）、`_access_tick_endpoint`（943）、`_evaluate_handover`（944）。
  - `_pending_ticker`（947）：每 `time_step` 循环执行 `_redecide_pending`（950）、`_sweep_downlink_queues`（951）、`_access_tick_sat`（952）。
  - `_sweep_downlink_queues`（954）：把下行队列中过 deadline 的包移出并判 `DATA_DEADLINE_EXPIRED`（957–966）。
  - `_endpoint_demand`（969）：端点上行队列非空、或某星持有发往该端点的流量（pending 或下行队列）即返回 True（970–975）。
  - `_downlink_demand_sats`（977）：返回 `pending[s]` 或 `downlinks[s].queues` 中含发往 `cell` 的包的卫星列表（978–985）。
  - `_candidates`（987）：候选关联卫星表——先列「持有该端点下行流量且当前可见」的星（按仰角降序、星号升序，992–994），再列其余可见星（995–997）；docstring（988–991）声明只用当前几何、不用未来星历。
  - `_try_grant`（999）：按候选顺序找首个有空槽的星，弹出等待记录、`_associate`、按 `preposition` 分别累计 `preposition_grants` 或 `grants` 与等待时长统计（1000–1013），成功返回 True。
  - `_request_or_grant`（1016）：先试 `_try_grant`；失败且有候选时把端点记入最优候选星的 FIFO 等待队列（`access_wait[s][cell] = now`）并累计 `requests`（1020–1028）。
  - `_access_tick_endpoint`（1030）：计算 idle（无上行队列、无下行需求、无在服务包，1036–1038）；对处于 `active` 且所在星有等待者的链路：持有满 `slot_lease_s` 则转 `retiring`（cause="lease"，`retire_at = now + retirement_deadline_s`）、spawn `_fire_interrupt`、记 `lease_retire` 切换事件（1042–1056）；idle 满 `idle_release_s` 则 `_release`（1057–1058）；之后处理新关联：已有主链路或有 retiring 链路则不动（1061–1064），有需求则 `_request_or_grant`（1065–1066），全网无等待者时做空槽预置 `_try_grant(preposition=True)`（1067–1068）。
  - `_access_tick_sat`（1070）：按 FIFO 请求顺序把空槽授予等待端点——清过期请求（1074–1078）、槽满即停（1079–1080）、几何不可见则留队（1081–1082）、授予并累计统计（1083–1089）。
  - `_control_advertiser`（1091）：循环 `_advertise(sat)` 后睡 `cfg_cp["advertise_interval_s"]`（1092–1095）。
  - `_advertise`（1098）：递增 `ctrl_seq`（1099）；收集各方向 ISL 占用比特（1100–1101）与传播时延（1102–1106）、当前 active 服务小区表（1107–1109）；调 `control.build_snapshot`（1110–1114←control.py:86）并补 `serve_cells`（1115）；`mech["control_snapshots"] += 1`（1116）；把自己的 `(origin, seq)` 预置为已见（1117–1119，注释称 origin 永不接受自己的广告）；对每个广播子方向：构造 `ControlPacket`（1120–1126）、`ctrl_ledger.register` 并计数（1127–1128）、队列放不下记 `QUEUE_OVERFLOW`（1129–1131）、否则计数并 `put_ctrl`（1132–1133）。
  - `_ctrl_arrive_after_prop`（1135）：睡传播时延（1136）；`mark_received`（1138）；过期记 `CONTROL_EXPIRED`（1139–1142）；`origin == sat` 记 `DUPLICATE`（1143–1148）；`(origin, seq)` 已见记 `DUPLICATE`（1149–1153）；否则记 `DELIVERED`（1155），按 `hops = vis_k - remaining_hops + 1` 建 `control.CacheEntry` 放入本星缓存（1156–1159）；`remaining_hops > 1` 时沿 `control_children[origin][sat]` 转发新 `ControlPacket`（同样 register/计数/溢出检查/入队，1160–1173）。
  - `_sweep_endpoint_queue`（1176）：把端点队列中过 deadline 的包移出并判 `DATA_DEADLINE_EXPIRED`（1177–1186）。
  - `_visible_sats`（1188）：返回当前 `ground_visible` 的 `(仰角, 星号)` 表，按仰角降序、星号升序（1189–1195）。
  - `_associate`（1197）：建 `Link(state="acquiring", ready_at=now + acquisition_delay_s, interrupt=env.event())`（1198–1200），登记 `ep.links` 与 `slots[sat]`（1201–1202），记 `associate` 切换事件（1203–1204）；捕获时延 ≤0 直接转 `active` 并唤醒上行（1205–1207），否则 spawn `_activate_after_delay`（1208–1209）。
  - `_activate_after_delay`（1211）：睡到 `ready_at`，若该链路仍为 `acquiring` 则转 `active` 并唤醒上行（1212–1215）。
  - `_release`（1217）：摘除链路、释放槽位、累计 `slot_hold_s_total` 与 `releases[reason]`、记 `release` 切换事件（1218–1227）。
  - `_on_link_retired`（1229）：链路处于 `retiring` 且已过 `retire_at` 时，把队列中仍指派给该星的包解指派（1238–1240），以 `f"{cause}_retire_deadline"` 释放（1241–1242）。
  - `_in_service`（1244）：该端点在此星的上行 `current` 或下行 `current`（按 `pkt.dst` 匹配）非空即 True（1245–1249）。
  - `_evaluate_handover`（1251）：先做 retiring 链路清理——已 drain（无指派包且无在服务）按 `f"{cause}_drained"` 释放（1255–1259），过期限且不在服务则解指派并按 `f"{cause}_retire_deadline"` 释放（1260–1265）；再评估切换：无主链路返回（1267–1269）；当前星仍可见时，无候选/已最优/仰角差小于 `hysteresis_deg`/持有不足 `min_dwell_s` 均保持（1271–1282）；选首个有空槽的非当前星为目标（1284–1290），无目标时当前不可见则 `geometry_lost_no_candidate` 释放（1291–1294）；满足 MBB 条件（`association == "mbb"` 且 `dual_connect` 且当前可见且 retiring 链路数低于 `retiring_link_limit`，1295–1299）则旧链路转 retiring（cause="mbb"，带硬期限与中断）、未指派包钉到旧星、关联新星、记 `mbb` 事件（1300–1315）；否则 BBM——在服务中则推迟（1317–1319），否则 `bbm_switch` 释放旧链并关联新星（1320–1324）。
  - `_serving_sats`（1327）：返回与端点 `active` 关联的卫星有序表（1330–1331）；docstring（1328–1329）声明仅供带标签的 oracle 使用；唯一直接调用点为 `_decide`（1418）。
  - `_learning_observation`（1333）：汇总本星各方向 ISL 占用（1334–1335）、可见端点数（1336–1339），调 `_learning.own_state`（1340–1344）与 `_learning.destination_features`（1349–1351，经 `geometry.subpoint` 取星下点），最后 `_learning.build_observation` 组装观测向量（1352–1356）。
  - `_finish_learning_transition`（1358）：`learner` 存在且包上有 `learning_state` 时，以给定或包上累计的 reward 调 `learner.remember(...)`（1361–1368），并清空包上三个 learning 字段（1369–1371）。
  - `_learning_action`（1373）：取观测（1374）、先完结上一转移（1375）、`learner.choose(state, mask, now)` 选动作（1376）；reward：`"deliver"` 为 1.0，否则为 `exp(-队列占用比)`（1377–1383）；把 state/action/reward 记到包上并返回动作（1384–1387）。
  - `_decide`（1389）：单包路由决策。过 deadline 判 `DATA_DEADLINE_EXPIRED`（1391–1393）；`len(path) > max_hops` 判 `NO_ROUTE`（1394–1396）；目的端点在本星有 `active` 关联且 GSL 可用时：下行队列有空间则（有 learner 时先走 deliver-only 掩码的 `_learning_action`，选出非 deliver 抛 `KernelError`）`dl.put(pkt)`，否则判 `ACCESS_QUEUE_OVERFLOW`（1397–1413）；否则调 `routing.choose_next_hop`（1414–1419，传 `oracle_targets` 与 `best_only=learner 是否存在`）；`"unreachable"` 判 `NO_ROUTE`（1420–1422）；`"no_info"` 时控制面关闭且策略非 oracle 判 `NO_ROUTE`，否则进 `pending[sat]` 待重决（1423–1428）；过滤会成环的候选（1429–1430）；逐候选查几何可用性与队列空间得 `legal` 表（1431–1440）；`legal` 非空：有 learner 按掩码选动作，否则取 `legal[0]`，`put_data` 入 ISL（1441–1448）；有候选但暂不可用进 `pending`（1449–1451）；有候选但全满判 `ISL_QUEUE_OVERFLOW`，无候选判 `NO_ROUTE`（1452–1455）。
  - `_redecide_pending`（1457）：把 `pending[sat]` 整体取出逐包重走 `_decide`（1458–1463）。
  - `_ingress_after_prop`（1465）：睡传播时延（1466）；过 deadline 判负（1467–1469）；`path.append(sat)`、`_note_busy(pkt.dst)`、`_decide`（1470–1472）。
  - `_isl_arrive_after_prop`（1474）：同形：睡传播、期限检查、`path.append(sat)`、`_note_busy`、`_decide`（1475–1481）。
  - `_deliver_after_prop`（1483）：睡传播（1484）；过 deadline 判负（1486–1488）；以零向量状态和全 False 掩码完结学习转移（done=True，1489–1492）；`ledger.record(pid, "DELIVERED", bits)`（1493）；`deliveries[pid] = {"delivered_at", "path"}`（1494）；`_log("delivered", ...)`（1495）。
  - `_fail`（1498）：`ControlPacket` 记控制账本（1499–1500）；数据包先以 `terminal_reward=0.0` 完结学习转移（1502–1507），再 `ledger.record(pid, fate, bits)`（1508）并 `_log("fate", ...)`（1509）。
  - `run`（1512）：手动步进主循环（1516–1527，见速览）；捕获 `(CapExceeded, fates.FateError)` 记 interrupted 与 error（1528–1530）；把停止时仍在服务的占用时间计入 `occupied`（1531–1540）；`stop_time = env.now`（1541）；在停止时刻 `close` 全部 `QueueArea`（1542–1549）并汇总 `queue_area`（1550–1557）；记 `waiting_at_stop`（1558–1559）；两本账本 `close_at_stop`，自然结束走 `check_conservation()`、中断走 `totals()`（1560–1567）；组装 `requested`（1568–1578）、控制计数器（1579–1593）、`effective` 机制有效性表（1594–1609：控制面要求真有包进过链路队列、GE 要求查询计数 >0、MBB 要求事件数 >0）；有 learner 时取 `diagnostics()`/`save_and_verify()` 并回填 learning 计数与 `effective["learning"]`（1610–1622）；`research_eligible` 恒为 False（1623–1627，注释声明本地内核不能自授权科研结果）；返回包含 `natural_end/interrupted/error/events_processed/horizon_s/stop_time_s/fates/fate_counts/totals/deliveries/occupied/queue_area_bits_s/access/service_log/handover/control/caches/mechanisms/learning/mechanism_counters/research_eligible/monitor_log/routing_label` 的结果 dict（1628–1671），其中 `"fates"` 直接读 `self.ledger._fates`（1635）、`routing_label` 在策略为 oracle 时取 `routing.ORACLE_LABEL`（1669）。
- 输入/输出：构造入参 `(resolved: dict, rows: list[dict], geometry=None, learning_out_dir=None)`；`run()` 返回结果 dict（键表见上，1628–1671）。
- 依赖关系：调用出边与被调用入边见上方「跨文件调用边」；类内被 `UplinkServer`/`DownlinkServer`/`ISLLink` 通过组合引用（`self.k`）回调 `_transmit`、`_poke`、`_note_busy`、`_fail`、`_on_link_retired`、`_gsl_ge`、`_ingress_after_prop`、`_deliver_after_prop`、`_ctrl_arrive_after_prop`、`_isl_arrive_after_prop` 等。

#### `def run_simulation(resolved, rows, geometry=None, learning_out_dir=None)` — CODE/leo_sim/kernel.py:1674
- 定位：CODE/leo_sim/kernel.py:1674
- 职责：构造 `Kernel` 并返回其 `run()` 结果（1676–1678）（FACT）。
- 输入/输出：入参与 `Kernel.__init__` 相同；输出为 `Kernel.run()` 的结果 dict。
- 依赖关系：调用方——`__main__.py:246`、`acceptance.py:108`、`comparison.py:106`、`platform_check.py:65` 与 `:109`，以及 tests 下多个测试文件（见入边清单）；`remote_job.py:250` 经 CLI 子进程间接到达。

<!-- 覆盖核对：12/12 class（KernelError 57、CapExceeded 61、DataPacket 65、QueueArea 84、ControlPacket 111、Link 178、TrafficEndpoint 199、_DRRMixin 220、UplinkServer 255、DownlinkServer 343、ISLLink 439、Kernel 586）+ 1/1 顶层 def（run_simulation 1674）；Kernel 43 个方法、其余类 33 个方法（全文件共 76 个方法）全部逐条列出。 -->
# 片段 n2：新平台 learning.py + receipt.py

### 文件 `CODE/leo_sim/learning.py`（实测 825 行）

模块级说明：

- 模块 docstring（learning.py:1-14）声明：本模块定义学习合同 C1/C3/C4/C5/C6/C7 与 canonical Double-DQN target 数学；信息边界为「每个合同只观测当前卫星自己直接测量的状态 + 实际到达且未过期的本地控制缓存」，C1 进一步限制到 1-hop origins，C3–C7 共享同一信息集（vis_k 缓存）、只在表示/聚合与 AoI 处理上不同；无可用 TensorFlow 时学习运行 fail closed（LearningUnavailable）。(FACT，源自 docstring)
- imports（learning.py:15-25）：`__future__.annotations`、`importlib.util`(17)、`hashlib`(18)、`json`(19)、`math`(20)、`os`(21)、`collections.deque`(22)、`pathlib.Path`(23)、`numpy as np`(25)。其中 `importlib.util` 在本文件内除 import 行外无任何引用（FACT，全文件 grep 仅命中行 17）。
- TensorFlow 可选导入（learning.py:27-30）：`try: import tensorflow as tf`，`ImportError` 时 `tf = None`；全模块的 fail-closed 语义都建立在该变量上。
- 全局常量：
  - `CONTRACTS`(32) = `("C1", "C3", "C4", "C5", "C6", "C7", "GAT", "MPNN")`。
  - `ORIGIN_FEATURES`(36) = 4；注释（34-35）给出逐 origin 特征块布局 `[isl_queue_ratio, access_load_ratio, n_visible_cells_norm, aoi_norm]`。
  - `DEST_FEATURES`(42) = 3；注释（37-41）给出布局 `[dst_bearing_sin, dst_bearing_cos, dst_dist_norm]`，bearing 为当前星 ENU 切平面内方位角（N=0、E=90°），距离为星下点到目的地大圆距离、按 20000 km 归一。`_DEST_DIST_NORM_KM`(43) = 20000.0；`_EARTH_R_KM`(44) = 6371.0。
  - 合同维度常量（45-53）：`C3_DIM = 4 + ORIGIN_FEATURES`(45)、`C4_DIM = 4 + ORIGIN_FEATURES`(46)、`C5_DIM = 4 + ORIGIN_FEATURES + 1`(47)、`C6_MAX_HOPS = 4`(48)、`C6_DIM = 4 + 4*ORIGIN_FEATURES`(49)、`C7_MAX_ENTRIES = 5`(50)、`C7_DIM = 4 + 5*(ORIGIN_FEATURES+1)`(51)、`C1_MAX_NEIGHBORS = 4`(52)、`C1_DIM = 4 + 4*ORIGIN_FEATURES`(53)。
  - `CONTRACT_DIMS`(56-63)：每个合同维度 = 上述 DIM + `DEST_FEATURES`，即 C1=23、C3=11、C4=11、C5=12、C6=23、C7=32（对 45-53 与 56-63 行做算术，FACT）。
  - `ACTIONS`(64) = `("deliver", "N", "S", "E", "W")`。
  - 图合同常量：注释（66-68）声明 GAT/MPNN 是新名字、不复用 V1 的 C4/C5 语义（V2 的 C4/C5 是缓存聚合规则）；`GRAPH_MAX_NODES = 32`(69)、`GRAPH_NODE_FEAT_DIM = 15`(70)、`GRAPH_DIRS = ("N", "S", "E", "W")`(71)、`GRAPH_CONTRACTS = ("GAT", "MPNN")`(72)。
  - `GRAPH_CONTRACT_DIMS`(84) = 每个图合同调 `graph_state_dim()`；`CONTRACT_DIMS` 在行 85-86 合并图合同维度。默认参数下 GAT/MPNN 观测宽度 = 32*15 + 32*32 + 4*32 + 4 + 3 = 1639（对 78-81 行做算术，FACT）。
- 环境变量：模块级无。`LEO_FAST_TRAIN` 在 `TensorflowDDQN.__init__`（learning.py:334）读取，值不在 `("0", "false", "no")` 时启用 tf.function 编译训练路径；注释（331-333）声称该路径与 eager 路径 bit 等价、快约 5-6 倍（FACT：注释内容如此；本片段不对该等价性做验证）。

学习合同定义位置与各自观测内容（本文件范围内汇总）：

- 合同名字集合定义于 learning.py:32（`CONTRACTS`）；配置侧合法值集合定义于 CODE/leo_sim/config.py:169（`VALID_CONTRACTS = {"C1", "C3", "C4", "C5", "C6", "C7", "GAT", "MPNN"}`），config.py:469-470 对 `routing.contract` 不在集合内抛 `ConfigError`；config.py:130 注释标注该键为 "C1|C3|C4|C5|C6|C7 (observation contracts)"；默认值 `"C3"` 在 config.py:241-242。learning 超参默认值（algorithm/mode/seed/obs_hops/checkpoint_path/checkpoint_sha256/gamma/lr/batch_size/replay_size/target_update_interval/reward/epsilon_*）在 config.py:243-259。
- 各合同观测内容由 `build_observation`（learning.py:724）各分支与 `build_graph_observation`（learning.py:663）决定，逐合同内容见下文 `build_observation` 条目。信息集（合同能看到哪些缓存条目）由 `information_set`（learning.py:593）决定：C1 只见 `{本星} ∪ 1-hop 邻居`（603-605）；C3–C7 与 GAT/MPNN 见同一集合——全部有效已到达条目，可选按 `obs_hops` 限制条目跳数（606-609）。测试佐证：test_learning.py:29-31 断言 C3–C7 信息集相同；test_learning.py:39 断言 C1 只见 1-hop origin；test_learning.py:120-128 断言 obs_hops 过滤生效。

#### `def graph_state_dim(max_nodes=GRAPH_MAX_NODES, node_feat_dim=GRAPH_NODE_FEAT_DIM) -> int` — CODE/leo_sim/learning.py:75

工具函数（压缩六字段）：定位 learning.py:75-81。职责 (FACT)：返回图合同扁平观测的宽度 = `max_nodes*node_feat_dim + max_nodes*max_nodes + len(GRAPH_DIRS)*max_nodes + 4 + DEST_FEATURES`（78-81；注释在行 81 标注末尾为 own-state tail + destination features）。输入两个 int（默认取 GRAPH_MAX_NODES=32、GRAPH_NODE_FEAT_DIM=15）；输出 int，默认参数下为 1639。调用方：learning.py:84（构造 `GRAPH_CONTRACT_DIMS`）、learning.py:718（`build_graph_observation` 的宽度断言）；CODE/ 内无外部调用方（全 CODE/ grep 仅命中本文件，FACT）。

#### `class LearningUnavailable(RuntimeError)` — CODE/leo_sim/learning.py:89

- 定位：learning.py:89-90。
- 职责 (FACT，源自 docstring 行 90)：请求学习执行但无真实 TensorFlow 运行时时抛出的异常类型。
- 关键状态/结构：无自定义状态、无自定义方法，空子类。
- 关键流程/方法：无方法。
- 输入/输出：构造接收异常消息字符串。
- 依赖关系：抛出点为 learning.py:96（`require_tensorflow`）、306/309/315（`TensorflowDDQN.__init__` 的 checkpoint 检查）、512（`save_and_verify` 验证失败）；kernel.py:54 将其重导出为 `kernel.LearningUnavailable`；捕获方为 __main__.py:251-253（打印 "RUN REFUSED (fail closed)" 并返回退出码 3）；测试 test_learning.py:196、210 断言无 TF 时经 `kernel.run_simulation` 抛出。

#### `def require_tensorflow()` — CODE/leo_sim/learning.py:93

工具函数（压缩六字段）：定位 learning.py:93-99。职责 (FACT)：`tf is None` 时抛 `LearningUnavailable`（消息中含 "learning runs fail closed"，96-98），否则返回 `tf` 模块对象（99）；docstring（94）称之为 "Fail closed unless a genuinely importable TensorFlow exists"。输入无；输出 tensorflow 模块或抛异常。调用方：learning.py:289（`TensorflowDDQN.__init__`）、kernel.py:741（`Kernel.learning_gate`，当 `routing.learning_enabled` 或 `learning.algorithm != "none"` 时调用，kernel.py:738-741）。

#### `class V2GraphEncoder` — CODE/leo_sim/learning.py:102

- 定位：learning.py:102-269。
- 职责 (FACT，源自 docstring 103-112 与 `call` 实现)：GAT/MPNN 图编码器 Keras 层：把 `build_graph_observation` 产出的扁平观测解析为节点特征 `[MAX_N,15]`、邻接 `[MAX_N,MAX_N]`（`adj[dst,src]=1` 表示真实 ISL 边）、readout 掩码 `[4,MAX_N]`、own-state tail `[4]`，运行 GAT（多头注意力）或 MPNN（均值消息传递）层，返回四个方向 readout 嵌入与 own-state tail 的拼接，供共享 dense Q 头使用。
- 关键状态/结构：类定义行 102 的基类为条件表达式 `tf.keras.layers.Layer if tf is not None else object`（FACT）——无 TF 主机上该类退化为 `object` 子类仍可被定义；docstring（114-117）声明本类在 import 时引用 `tf`，因此模块应在 `require_tensorflow()` 成功后使用（FACT：docstring 内容；同时测试 test_learning.py:7 无条件 import 本模块、并在 188-211 行验证无 TF 主机上 fail closed，FACT）。实例状态：`enc_mode/n_nodes/f_dim/h_dim/layers/heads`（128-133）、`node_in` Dense 层（134-135）、可训练权重 `dir_default`（形状 (4, h_dim)，zeros 初始化，136-138）、`build` 中按模式创建的逐层权重（见下）。
- 关键流程/方法：
  - `__init__(self, enc_mode, n_nodes, f_dim, h_dim, layers, heads, **kwargs)`(120)：校验 `enc_mode ∈ {"gat","mpnn"}`（123-125）、GAT 时 `h_dim % heads == 0`（126-127），存配置并创建 `node_in` 与 `dir_default`。
  - `get_config(self)`(140)：返回含六个超参的序列化配置 dict（141-150）。
  - `from_config(cls, config)`(152，@classmethod)：从配置 dict 重建实例（153-158）。
  - `build(self, input_shape)`(160)：GAT 模式创建每层权重 `gat_W`（heads×h_dim×hd，glorot_uniform，163-168）、`gat_a_src`（169-174）、`gat_a_dst`（175-180）、`gat_self_W`（h_dim×h_dim，181-186）、`gat_bias`（zeros，187-191）；MPNN 模式创建 `msg_W`（193-198）、`self_W`（199-204）、`mpnn_bias`（205-209）；末尾调 `super().build`（210）。
  - `_parse(self, flat)`(212)：把扁平输入 reshape 成 node/adj/readout/tail 四段（214-219）；取节点特征张量索引 7 的切片 `node[:, :, 7:8]`（即 `_graph_node_features` 写入的 valid flag，learning.py:655）作为 `node_mask`，用它屏蔽 adj 的行列与 readout 的列（220-222）；返回五元组。
  - `_gat_layer(self, h, adj, node_mask, l)`(225)：单层 GAT——`einsum` 把节点嵌入投影到多头（227）、分别与 `gat_a_src`/`gat_a_dst` 打分（228-231）、LeakyReLU(alpha=0.2) 得注意力 logits（232-233）、按邻接掩码把无边位置压到 -1e9 后 softmax 并按行归一（234-238）、聚合消息经转置 reshape 后与自变换 `gat_self_W`、偏置相加过 ReLU（239-243），输出乘 `node_mask`（244）。
  - `_mpnn_layer(self, h, adj, node_mask, l)`(246)：单层 MPNN——源消息线性变换（247）、按度数归一的邻接均值聚合（248-249）、自变换+偏置过 ReLU（250-251），输出乘 `node_mask`（252）。
  - `call(self, flat, training=False)`(254)：`_parse` → `node_in` 嵌入并乘掩码（255-256）→ 按模式堆叠 `self.layers` 层（257-261）→ 按 readout 掩码做四方向均值 readout，某方向无节点时用可训练的 `dir_default` 兜底（262-267）→ 拼接 `4*h_dim` 方向嵌入与 tail 返回（268-269）。
- 输入/输出：输入扁平张量 `[batch, graph_state_dim()]`；输出 `[batch, 4*h_dim + tail_len]`（tail_len 由输入剩余段决定，图观测下为 4+3=7，见 build_graph_observation 708-715）。
- 依赖关系：被 `TensorflowDDQN._network` 实例化（learning.py:343，固定 h_dim=64、layers=1、heads=2）；经 `_graph_custom_objects`（272-273）注册进 `keras.models.load_model` 的 `custom_objects`（learning.py:312、494）；CODE/ 内无其他直接调用方。

#### `def _graph_custom_objects()` — CODE/leo_sim/learning.py:272

工具函数（压缩六字段）：定位 learning.py:272-273。职责 (FACT)：返回 `{"V2GraphEncoder": V2GraphEncoder}`。输入无；输出单键 dict。该 dict 被传给 `keras.models.load_model` 的 `custom_objects` 参数（learning.py:312、494）；其用途是让 Keras 反序列化时识别自定义层类 (INFERENCE——代码内无注释说明，由 Keras API 语义推定)。调用方：learning.py:312、494；无外部调用方。

#### `class TensorflowDDQN` — CODE/leo_sim/learning.py:276

- 定位：learning.py:276-529。
- 职责 (FACT，源自 docstring 277-284)：V2 hop-by-hop 运行时使用的共享策略 Double-DQN；一个模型被所有卫星共享，每次决策只消费该卫星的本地观测与合法掩码；合法掩码由 kernel 而非网络构造，因此探索不会选出隐藏全局、成环、满队列或几何上不可用的动作（docstring 陈述的设计约束）。
- 关键状态/结构：`contract`、`input_dim = CONTRACT_DIMS[contract]`（295-296）、`cfg`、`seed`、`rng = np.random.default_rng(seed)`（299）、`replay = deque(maxlen=cfg["replay_size"])`（300）、`mode = cfg["mode"]`（301）、`online`/`target` 两个网络、`optimizer = Adam(lr=cfg["lr"])`（325-326）、计数器 `decisions/transitions/train_steps/last_loss`（327-330）、`loaded_checkpoint`/`loaded_checkpoint_sha256`（317-318 或 321-322）、`_fast_enabled`/`_fast_train_fn`/`_fast_train_net_id`/`_fast_train_tgt_id`（334-337）。
- 关键流程/方法：
  - `__init__(self, contract, cfg, seed)`(286)：合同不在 `CONTRACT_DIMS` 抛 ValueError（287-288）；调 `require_tensorflow()`（289）；尝试 `enable_op_determinism()`，异常被静默吞掉（290-293）；`set_random_seed(seed)`（294）；若 `cfg["checkpoint_path"]` 非空：文件不存在抛 LearningUnavailable（303-306）、文件 SHA-256 与 `cfg["checkpoint_sha256"]` 不符抛 LearningUnavailable（307-310）、`load_model` 后输入形状须为 `(None, input_dim)`、输出形状须为 `(None, len(ACTIONS))`，不符抛 LearningUnavailable（311-316）；无 checkpoint 时用 `_network()` 新建（319-322）；`target` 网络新建并复制 `online` 权重（323-324）；建 Adam 优化器（325-326）；读 `LEO_FAST_TRAIN` 环境变量（334）。
  - `_network(self)`(339)：图合同建 `Input → V2GraphEncoder(enc_mode, n_nodes=32, f_dim=15, h_dim=64, layers=1, heads=2) → Dense(64, relu) → Dense(5, linear)` 的 Model（341-350）；其他合同建 `Input → Dense(64,relu) → Dense(64,relu) → Dense(5,linear)` 的 Sequential（351-356）。
  - `epsilon(self, now)`(358)：`mode == "eval"` 返回 0.0（359-360）；否则返回 `epsilon_end + (epsilon_start - epsilon_end) * exp(-max(0, now)/epsilon_decay_s)`（361-364）。
  - `_mask_array(mask)`(366，@staticmethod)：按 `ACTIONS` 顺序把 mask dict 转成 bool np 数组，缺键按 False（367-368）。
  - `choose(self, observation, mask, now)`(370)：合法动作集为空抛 ValueError（371-374）；以 `epsilon(now)` 概率在合法下标中均匀随机（376-377），否则 online 网络前向并在合法下标上取 argmax（379-380）；`decisions += 1`（381）；返回动作名字符串（382）。
  - `remember(self, state, action, reward, next_state, next_mask, done)`(384)：未知动作名抛 ValueError（386-387）；把 transition（state 数组、动作下标、reward、next_state 数组、next_mask 数组、done）追加进 `replay`（388-393）；`transitions += 1`（394）；`mode == "train"` 且 `len(replay) >= batch_size` 时调 `_train_once()`（395-396）。
  - `_train_once(self)`(398)：无放回抽样一个 batch（399-407）；fast 路径（408-428）：首次或 online/target 对象 id 变化时重建 tf.function（409-415），调用编译好的训练步（416-423），记录 loss、`train_steps += 1`，每逢 `target_update_interval` 同步 target 权重（424-427）；eager 路径（429-444）：online/target 前向、`ddqn_targets` 算目标值、GradientTape 内算 MSE loss、`apply_gradients`、同样按间隔同步 target。
  - `_build_fast_train_fn(self)`(446)：构造并返回一个 `@tf.function(input_signature=..., reduce_retracing=True)` 编译的训练步（453-462）；步内逻辑：online/target 前向（464-465）、整行无合法动作时把掩码退化为全 1 的 `safe_mask`（466-470）、掩码后 argmax 得 a*（471-473）、`not_done` 为假时 bootstrap 置 0（474-475）、`expected = stop_gradient(rewards + gamma * bootstrap)`（476）、tape 内算 MSE 并 `apply_gradients`（477-482）、返回 loss（483）。
  - `save_and_verify(self, directory)`(487)：把 `online` 存为 `directory/online.keras`（488-491）；算文件 SHA-256（492）；重新 `load_model`（493-494）；用 `np.linspace(-0.5, 0.5, input_dim)` 探针比较保存前后输出，`rtol=0.0, atol=1e-7`（495-498）；写 `metadata.json`（含 `schema="leo-sim-ddqn/v1"`、checkpoint 文件名/SHA-256/`checkpoint_verified`/探针最大绝对误差，499-510）；验证未通过抛 LearningUnavailable（511-512）；返回 metadata dict（513）。
  - `diagnostics(self)`(515)：返回含 algorithm/contract/mode/loaded_checkpoint(_sha256)/actions/decisions/transitions/train_steps/replay_size/last_loss/seed 的 dict（516-529）。
- 输入/输出：构造吃合同名、learning 配置 dict（键来自 config.py:243-259 的 learning 段）、seed；`choose` 吃观测向量 + mask dict + 仿真时刻，返回 `ACTIONS` 中的字符串；`remember` 吃一条 transition；`save_and_verify` 写盘并返回 metadata dict。
- 依赖关系：被 `Kernel.__init__` 在 `learning.algorithm == "ddqn"` 时实例化（kernel.py:603-610）；kernel 经 `_learning_action` 调 `choose`（kernel.py:1376）、经 `_finish_learning_transition` 调 `remember`（kernel.py:1365-1368）、在 `run()` 收尾调 `diagnostics()` 与 `save_and_verify()`（kernel.py:1612-1615）并把 decisions/transitions/train_steps 写回机制计数器（kernel.py:1616-1618）；测试 test_learning.py:215 直接构造。内部调用：`require_tensorflow`(289)、`_graph_custom_objects`(312, 494)、`V2GraphEncoder`(343)、`ddqn_targets`(431)。

#### `def own_state(slots_used, slots_cap, isl_queue_bits, isl_queue_cap, n_visible, n_cells) -> np.ndarray` — CODE/leo_sim/learning.py:532

工具函数（压缩六字段）：定位 learning.py:532-541。职责 (FACT)：构造 4 维本星自有状态向量 `[slots_used/max(1,slots_cap), 各方向 ISL 队列比特总和/max(1, isl_queue_cap*方向数), n_visible/max(1,n_cells), 1.0]`（534-541）；第 4 维注释（540）为 "bias/valid flag marking real own measurement"。输入 6 个参数（4 个标量 + 方向→比特 dict + 队列上限）；输出 float64 np.ndarray，shape (4,)。调用方：kernel.py:1340（`Kernel._learning_observation`）、test_learning.py:26、test_review_round4.py:333。

#### `def _origin_features(entry, now, isl_queue_cap) -> np.ndarray` — CODE/leo_sim/learning.py:544

工具函数（压缩六字段）：定位 learning.py:544-556。职责 (FACT)：把一条缓存 entry 编成 4 维归一化特征 `[entry 的 isl_queue_bits 总和/max(1, isl_queue_cap*4), access_slots_used/max(1,access_slots_cap), min(1, 可见小区数/10), min(1, max(0,entry.aoi(now))/max(entry.ttl_s,1e-9))]`（545-556）；entry 缺字段时用 `payload.get(..., 默认)` 兜底（546-549）。输入 `CacheEntry`、`now`、`isl_queue_cap`；输出 float64 np.ndarray，shape (4,)。调用方：learning.py:734（`build_observation` 全合同）、770（C5 分支）、785（C7 分支）；无外部调用方。entry 的 `payload/aoi()/ttl_s/hops` 字段语义见 control.py:37-54（CacheEntry）。

#### `def destination_features(sat_lat_deg, sat_lon_deg, dst_lat_deg, dst_lon_deg) -> np.ndarray` — CODE/leo_sim/learning.py:559

工具函数（压缩六字段）：定位 learning.py:559-590。职责 (FACT，docstring 行 561 + 实现)：3 维目的地条件特征 `[sin(bearing), cos(bearing), min(1, 大圆距离km/20000)]`（586-590）；bearing 计算：经纬度转弧度后求两地地心笛卡尔坐标差 (dx,dy,dz)（568-573），投影到卫星星下点 ENU 的 east/north 分量（574-577），`atan2(east, north)` 得方位角（578）；距离用 haversine 公式（581-585）。输入两对经纬度（度）；输出 float64 np.ndarray，shape (3,)。调用方：kernel.py:1350（`Kernel._learning_observation`，仅当目的地小区存在时计算）、test_learning.py:111。

#### `def information_set(contract, sat, cache, now, topo, obs_hops=None) -> dict` — CODE/leo_sim/learning.py:593

- 定位：learning.py:593-610。
- 职责 (FACT，docstring 595-601 + 实现)：返回一个合同恰好允许看到的缓存条目 dict。
- 关键状态/结构：无持有状态；输入 `cache` 需提供 `valid_entries(now)`（control.py:70-77 的 `LocalCache.valid_entries`，只返回生成≤到达≤now≤生成+ttl 的条目）。
- 关键流程/方法：`entries = cache.valid_entries(now)`（602）；C1 → `allowed = {sat} | set(topo.get(sat, {}).values())`，只保留 origin ∈ allowed 的条目（603-605）；C3/C4/C5/C6/C7/GAT/MPNN → `obs_hops is None` 返回全部条目副本，否则只保留 `e.hops <= obs_hops` 的条目（606-609）；未知合同抛 ValueError（610）。
- 输入/输出：输入合同名、卫星 id、缓存对象、时刻、拓扑 dict、可选跳数上限；输出 `{origin: CacheEntry}` dict。
- 依赖关系：调用方 learning.py:676（`build_graph_observation`）、732（`build_observation`）；测试 test_learning.py:31/39/47/124、test_review_round4.py:335。被调方：`LocalCache.valid_entries`（control.py:70）。

#### `def _bfs_first_dirs(sat, topo) -> dict[int, str]` — CODE/leo_sim/learning.py:613

工具函数（压缩六字段）：定位 learning.py:613-634。职责 (FACT，docstring 614-619 + 实现)：从 `sat` 出发对静态 ISL 邻接做 BFS，给每个可达节点标注「从根出发第一跳的方向」，返回 `{node: first_dir}`；根节点自身不出现在结果中（618-619）；docstring 称此为 "V1-style directional readout"（617）。实现：初始 frontier 为按方向名排序的直接邻居（621-625），此后逐层扩展、子节点继承其父节点的 first_dir（626-633）。输入卫星 id 与 topo dict；输出 `{int: str}` dict。调用方：learning.py:678（`build_graph_observation`）；无外部调用方。

#### `def _graph_node_features(origin, entry, root, first_dir, topo, isl_queue_cap, root_pos=(0,0,0)) -> np.ndarray` — CODE/leo_sim/learning.py:637

工具函数（压缩六字段）：定位 learning.py:637-660。职责 (FACT，docstring 640 + 实现)：为一个子图节点构造 15 维特征向量——`feats[0:4]` = 四方向 ISL 队列比特各除以 `max(1, isl_queue_cap)` 并截断到 1（650-651）；`feats[4]` = `min(1, hops/4)`（652）；`feats[5]` = `min(1, 节点度数/4)`，度数按 topo 中邻居值非 None 的项数计算（648、653）；`feats[6]` = 是否根节点的 0/1（654）；`feats[7]` = 恒 1.0 的 valid 节点标志，注释（655）说明 padding 行保持 0；`feats[8:12]` = `first_dir` 的 one-hot（656-657）；`feats[12:15]` = 节点 payload 的 `position` 与 `root_pos` 之差除以 7000.0（658-659；该归一化常数在代码中无注释解释，FACT）。`entry is None` 时各 payload 字段取默认值（641-647）。输入 origin id、可空 entry、根 id、可空 first_dir、topo、isl_queue_cap、root_pos；输出 float64 np.ndarray，shape (15,)。调用方：learning.py:691（`build_graph_observation`）；无外部调用方。

#### `def build_graph_observation(contract, sat, cache, now, topo, own, isl_queue_cap=256_000_000, obs_hops=None, dst_feats=None) -> np.ndarray` — CODE/leo_sim/learning.py:663

- 定位：learning.py:663-721。
- 职责 (FACT，docstring 668-675 + 实现)：为 GAT/MPNN 图合同构造定宽扁平 k-hop 子图观测；布局 = 节点特征 `[MAX_N,15]` + 有向邻接 `[MAX_N,MAX_N]` + 方向 readout 掩码 `[4,MAX_N]` + own-state tail `[4]`（+ 目的地特征）；docstring 声明节点为实际到达的有效缓存 origins 加根节点、节点特征只来自已到达 ControlPacket 携带的 payload 字段（无未来几何、无隐藏全局队列）。
- 关键状态/结构：无持有状态；内部构造 `feats (32,15)`、`adj (32,32)`、`readout (4,32)` 三个零矩阵与 tail 向量。
- 关键流程/方法：取 `information_set`（676）与 `_bfs_first_dirs`（678）；节点序列 = 根 + 排序后 origins 截断到前 31 个（680-683；`overflow` 计数于 682 计算但未再使用，FACT）；根位置取根 entry payload 的 `position`（684-686）；逐节点填 `_graph_node_features`（688-693）；按 topo 填邻接，`adj[dst, src] = 1` 当节点间有 ISL 边且非自环（695-700）；按 first_dir 填 readout one-hot（702-706）；`own` 必须 reshape 后为 4 维否则 ValueError（708-710）；`dst_feats` 为 None 时补 3 维零、维度不符抛 ValueError（711-714）；拼接后总宽度必须等于 `graph_state_dim()`，不等抛 AssertionError（716-720）。
- 输入/输出：输入合同名、卫星 id、缓存、时刻、topo、own 向量、队列上限、可选 obs_hops、可选目的地特征；输出 float64 np.ndarray，shape (1639,)（默认常量下）。
- 依赖关系：调用方仅 learning.py:729（`build_observation` 的图合同分支）；内部调 `information_set`(676)、`_bfs_first_dirs`(678)、`_graph_node_features`(691)、`graph_state_dim`(718)。

#### `def build_observation(contract, sat, cache, now, topo, own, isl_queue_cap=256_000_000, obs_hops=None, dst_feats=None) -> np.ndarray` — CODE/leo_sim/learning.py:724

- 定位：learning.py:724-791。
- 职责 (FACT)：按合同名构造观测向量；图合同委托 `build_graph_observation`，其余合同按各自的聚合规则拼接。
- 关键状态/结构：无持有状态；内部定义闭包 `_finish(base)`（741-742）把目的地特征拼到末尾。
- 关键流程/方法：图合同分支（728-731）；取 `information_set`（732）、对每个 origin 算 `_origin_features`（734）；`own` 转 float64（735）；`dst_feats` 为 None 补零、维度不符抛 ValueError（736-739）。逐合同分支：
  - C1（744-748）：`own` + topo 邻居排序后各邻居的 origin 特征块（缺条目补零块），块数截断/补齐到 `C1_MAX_NEIGHBORS = 4`，+ 目的地特征 → 23 维。
  - C3（750-753）：`own` + 全部条目特征的逐维均值（空缓存时全零块）+ 目的地特征 → 11 维。
  - C4（755-762）：`own` + AoI 加权平均（权重 `exp(-max(0,aoi)/max(ttl,1e-9))`，759-760；空缓存全零）+ 目的地特征 → 11 维。
  - C5（764-770）：`own` + 最新鲜（`aoi` 最小）条目的特征 + 1 维标志（有条目为 1.0、无条目为 0.0 且特征块全零）+ 目的地特征 → 12 维；常量注释（47）把该标志称为 "staleness flag"。
  - C6（772-779）：`own` + 按 `min(max(1,hops),4)` 分入 4 个跳数桶的桶内均值（空桶全零）+ 目的地特征 → 23 维。
  - C7（781-789）：`own` + 按 `aoi` 升序前 `C7_MAX_ENTRIES = 5` 个条目、每条 `[特征, 1.0]` 块，不足补全零块 + 目的地特征 → 32 维。
  - 未知合同抛 ValueError（791）。
- 输入/输出：输入与 `build_graph_observation` 同形；输出 float64 np.ndarray，shape = `(CONTRACT_DIMS[contract],)`。
- 依赖关系：调用方 kernel.py:1352（`Kernel._learning_observation`）；测试 test_learning.py:54-55/65/81/114/128/137、test_review_round4.py:336。佐证：test_learning.py:53-58 逐合同断言输出宽度等于 `CONTRACT_DIMS`、两次调用结果一致且全部有限；test_learning.py:133-144 在空缓存场景断言各合同输出宽度、own 块在位且未提供目的地时目的地特征为零块。内部调 `build_graph_observation`(729)、`information_set`(732)、`_origin_features`(734/770/785)。

#### `def build_action_mask(can_deliver, isl_room) -> dict` — CODE/leo_sim/learning.py:794

工具函数（压缩六字段）：定位 learning.py:794-801。职责 (FACT)：构造合法动作掩码 dict——`"deliver": bool(can_deliver)`，再按方向名排序把 `isl_room` 各项转 bool 放入（798-800）；docstring（795-797）声明语义为「deliver 仅在直接可见且有下行余量时合法、每个 ISL 方向仅在队列有余量时合法、由 kernel 从当前本地状态计算」。输入 bool 与 `{方向: 余量}` dict；输出 mask dict。调用方：全 CODE/ grep 仅命中测试 test_learning.py:156、158（FACT）；kernel 实际决策路径不调本函数，而是在 kernel.py:1406 与 1443 用内联 dict 推导 `{a: ... for a in _learning.ACTIONS}` 构造掩码（FACT）。

#### `def ddqn_targets(q_online_next, q_target_next, next_mask, rewards, dones, gamma) -> np.ndarray` — CODE/leo_sim/learning.py:804

工具函数（压缩六字段）：定位 learning.py:804-825。职责 (FACT，docstring 807-812 + 实现)：canonical Double-DQN 目标——online Q 在非法动作处置 `-inf` 后逐行 argmax 得 a*（816-817）；非终态行若选中值非有限（即无合法动作）抛 ValueError（821-822，注释 819-820 说明终态行不需要合法动作）；`y = rewards + gamma * (1-dones) * Q_target(s', a*)`（823-825，终态 bootstrap 置 0 于 824）。输入两个 `(batch, n_actions)` Q 矩阵、bool mask、`(batch,)` rewards/dones、标量 gamma；输出 float64 np.ndarray，shape (batch,)。调用方：learning.py:431（`TensorflowDDQN._train_once` eager 路径）；测试 test_learning.py:166/176/183、test_acceptance_review.py:25。佐证：test_learning.py:162-170 验证掩码 argmax 数学、173-178 验证终态不 bootstrap、181-185 验证无合法动作抛 ValueError。

### 文件 `CODE/leo_sim/receipt.py`（实测 941 行）

模块级说明：

- 模块 docstring（receipt.py:1-22）声明信任模型：本地验证只证明盘上 artifacts（resolved config、trace.csv、manifest.json、ledgers.json、receipt.json）之间的内部一致性，没有外部锚——能同时重写 ledgers.json 并重绑 `receipt.ledgers_sha256` 的人可以伪造出一致的运行；正式防篡改需要治理链（干净的已提交代码身份、授权 manifest、外部 artifact-hash 锚），该 gate 不在本模块解决（FACT，源自 docstring 行 3-10）。docstring 还定义字段权威三类（12-22）：`recomputed`（验证器从 trace.csv/resolved_config.json 重建）、`ledger_consistency`（被 ledgers SHA 绑定、查 schema 与内部关系但不可独立重算）、`diagnostic`（只报告、查 schema、永不可作为研究资格或科学指标证据）。
- imports（receipt.py:23-32）：`__future__.annotations`、`csv`(25)、`hashlib`(26)、`json`(27)、`math`(28)、`platform`(29)、`pathlib.Path`(30)、同包 `config as config_mod, fates, rng as rng_mod, trace as trace_mod`(32)。其中 `csv` 在本文件内除 import 行外仅出现在 docstring（行 379 的 "trace.csv" 字样），无任何 `csv.` 调用（FACT，全文件 grep）。
- 全局常量：
  - `RECEIPT_SCHEMA`(34) = `"leo-sim-receipt/v3"`。
  - `RECEIPT_KEYS`(37-44)：receipt.json 顶层键的精确集合（25 个键），注释（36）声明未知或缺失键都会使验证失败。
  - `DEP_KEYS`(45) = `{python, simpy, numpy, pyyaml}`；`REQUESTED_KEYS`(46-47) = `{policy, association, ge_enabled, control_enabled, monitor, learning_algorithm, learning_mode}`；`EFFECTIVE_KEYS`(48) = `{control_plane, ge, mbb, learning}`。
  - `LEDGER_KEYS`(50-55)：ledgers.json 顶层键精确集合（13 个，含 `field_authority` 与 `learning`）。
  - `CONTROL_COUNTER_KEYS`(56-60)：12 个控制面计数器键；`MECHANISM_COUNTER_KEYS`(61-67)：16 个机制计数器键；`MECHANISM_COUNTER_BOOLS`(68-69) = `{control_initialized, ge_initialized, learning_initialized}`（三键必须为 bool）。
  - `OCCUPIED_KEYS`(70)、`QUEUE_AREA_KEYS`(71)、`ACCESS_KEYS`(72-75)、`ACCESS_INT_KEYS`(76)、`HANDOVER_TYPES`(77) = `{associate, release, bbm, mbb, lease_retire}`。
  - `FIELD_AUTHORITY`(79-92)：12 个 ledger 字段到权威类的映射——`recomputed`：packet_fates、stop_time_s、deliveries、learning；`ledger_consistency`：control_instances、control_counters、mechanism_counters；`diagnostic`：occupied、queue_area_bits_s、handover_events、access、events_processed。
- 环境变量：无（全文件无 `os.environ` 读取，FACT）。

#### `def code_sha256() -> str` — CODE/leo_sim/receipt.py:95

工具函数（压缩六字段）：定位 receipt.py:95-102。职责 (FACT，docstring 96 + 实现)：对 leo_sim 包目录下全部 `*.py` 按文件名排序，逐个把「文件名 + 文件内容 SHA-256 摘要」喂进滚动 SHA-256，返回 hexdigest（97-102）。输入无；输出 64 字符小写 hex 字符串。调用方：receipt.py:308（`build_receipt`）、736（`verify_receipt_dir` 步骤 3）、CODE/leo_sim/governance.py:108、CODE/experiment_platform/authorize_experiment.py:344 与 510（以 `v2_receipt` 别名导入，authorize_experiment.py:240/496）。

#### `def dependency_versions() -> dict` — CODE/leo_sim/receipt.py:105

工具函数（压缩六字段）：定位 receipt.py:105-114。职责 (FACT)：返回 `{python: platform.python_version(), simpy: simpy.__version__, numpy: numpy.__version__, pyyaml: yaml.__version__}`（106-114；numpy/simpy/yaml 在函数体内 import）。输入无；输出 4 键 dict。调用方：receipt.py:310（`build_receipt`）、741 与 743（`verify_receipt_dir` 步骤 3 的重算比对）。

#### `def requested_from_config(cfg) -> dict` — CODE/leo_sim/receipt.py:117

工具函数（压缩六字段）：定位 receipt.py:117-127。职责 (FACT，docstring 118 + 实现)：仅从 resolved config 重建「请求的机制」dict——`policy = cfg["routing"]["policy"]`、`association = cfg["access"]["association"]`、`ge_enabled = bool(cfg["links"]["ge_enabled"])`、`control_enabled = bool(cfg["control_plane"]["enabled"])`、`monitor = bool(cfg["execution"]["monitor"])`、`learning_algorithm = cfg["learning"]["algorithm"]`、`learning_mode = cfg["learning"]["mode"]`（119-127）。输入 resolved config dict；输出 7 键 dict。调用方：receipt.py:299（`build_receipt`）、920（`verify_receipt_dir` 步骤 6）。

#### `def effective_from_counters(counters, requested) -> dict` — CODE/leo_sim/receipt.py:130

工具函数（压缩六字段）：定位 receipt.py:130-147。职责 (FACT，docstring 131-132 + 实现)：从原始机制计数器重算「生效标志」——`control_plane = control_entered_queue > 0`（134）；`ge = requested.ge_enabled 且 (ge_gsl_queries + ge_isl_queries) > 0`（135-137）；`mbb = mbb_events > 0`（138）；`learning`：`requested.learning_mode == "train"` 时看 `learning_train_steps > 0`，否则（含 eval）看 `learning_decisions > 0`（142-146；注释 139-141 说明 eval 合法地不做梯度更新，故以真实模型的路由决策数为准）。输入计数器 dict 与 requested dict；输出 4 键 bool dict。调用方：receipt.py:930（`verify_receipt_dir` 步骤 6）；测试 test_learning.py:254-261 佐证 eval 模式 decisions>0 即判 effective。

#### `def expected_research_eligible(requested, effective, natural_end, interrupted) -> bool` — CODE/leo_sim/receipt.py:150

工具函数（压缩六字段）：定位 receipt.py:150-158。职责 (FACT)：函数体恒 `return False`（158）；docstring（152-157）说明本地 artifacts 永不赋予正式研究资格，四个参数仅作为兼容面与机制诊断保留，正式资格属于绑定评审、授权与部署 commit 的外部治理 receipt。输入四个参数（均不被读取）；输出恒 `False`。调用方：receipt.py:934-936（`verify_receipt_dir` 步骤 6）；无其他调用方。

#### `def _validate_manifest(manifest, resolved_cfg, resolved_version) -> list[str]` — CODE/leo_sim/receipt.py:161

- 定位：receipt.py:161-260。
- 职责 (FACT，docstring 163)：校验 trace manifest 中「不必信任 manifest 自身即可推导」的全部字段；全程向 errors 列表追加字符串、不抛异常。
- 关键状态/结构：局部 `errors` 列表；键集 `base_keys`(165-170)、`proxy_keys`(171)、`population_keys`(172)。
- 关键流程/方法：按 `manifest["mode"]` 决定期望键集（mlab 加 proxy_keys、population_gravity 再加 "population"，173-178），键集不符记错误（179-182）；`schema`/`trace_schema`/`packet_id_contract` 分别比对 `trace_mod.TRACE_MANIFEST_SCHEMA`/`TRACE_SCHEMA`/`PACKET_ID_CONTRACT`（183-188）；`config_version` 比对（189-190）；`resolved_cfg is None` 时提前返回（191-192）；`mode` 必须等于 resolved config 的 `demand.mode`（193-195）；`provenance` 必须等于 `{"mlab": "measurement_proxy", "population_gravity": "population_proxy"}.get(mode, "synthetic")`（196-201）；`rng_streams` 必须等于 `rng_mod.stream_mapping(seed, ["demand"])`（202-205）；`input_sha256`：csv/mlab/population_gravity 模式必须是 64 位小写 hex，synthetic 模式必须为空串（206-212）；mlab 模式要求 `not_calibrated_user_demand is True` 且 `provenance_note` 逐字等于给定英文串（213-219）；population_gravity 模式要求同款声明与另一逐字串（220-227），且 `population` 子表键集精确（228-237）、`source_sha256 == input_sha256`（239-240）、`aggregation_deg`/两个种群指数/`distance_exponent`/`distance_floor_km` 与 resolved config 对应字段逐项相等（241-253）、`total_population` 为正数（254-256）、`candidate_regions >= 2`（257-259）。
- 输入/输出：输入 manifest dict、可空 resolved config、可空版本字符串；输出错误字符串列表（空 = 通过）。
- 依赖关系：调用方 receipt.py:723（`verify_receipt_dir` 步骤 2）；内部调 `_is_nonneg_num`(254)、`_is_nonneg_int`(257)、`rng_mod.stream_mapping`(202)、引用 `trace_mod` 三个常量(183-187)。

#### `def _sha_file(path) -> str` — CODE/leo_sim/receipt.py:263

工具函数（压缩六字段）：定位 receipt.py:263-264。职责 (FACT)：返回 `hashlib.sha256(path.read_bytes()).hexdigest()`。输入 `Path`；输出 64 字符 hex。调用方：receipt.py:353（`write_run` 对 ledgers.json 算 SHA）、422（`_validate_ledgers` 重算 checkpoint SHA）、620/650/755（`verify_receipt_dir` 中 trace.csv/manifest 交叉、ledgers.json 绑定）。

#### `def build_ledgers(result, rows) -> dict` — CODE/leo_sim/receipt.py:267

- 定位：receipt.py:267-291。
- 职责 (FACT)：从 kernel 运行结果与 trace 行组装结构化 run-ledger dict；docstring/NOTE（268-271）声明这是运行自身的陈述、不是独立 ground truth。
- 关键状态/结构：输出 dict 的 13 个键对应 `LEDGER_KEYS`。
- 关键流程/方法：`bits_by_pid` 从 rows 建 pid→bits 映射（272）；`packet_fates` = `{pid: [fate, bits]}`（274-275）；`control_instances` 转字符串键列表对（276-277）；直接搬运 `control_counters`/`mechanism_counters`/`occupied`/`queue_area_bits_s`/`handover_events`/`access`/`events_processed`/`stop_time_s`（278-285）；`deliveries` 键转字符串（286）；`learning` 取 `result["learning"]`、为 None 时落 `{"algorithm": "none"}`（287-289）；`field_authority` 放 `FIELD_AUTHORITY` 副本（290）。
- 输入/输出：输入 kernel result dict 与 trace rows list；输出 ledgers dict。
- 依赖关系：调用方仅 receipt.py:350（`write_run`）。

#### `def build_receipt(resolved, manifest, result, rows, ledgers, ledgers_sha256) -> dict` — CODE/leo_sim/receipt.py:294

- 定位：receipt.py:294-335。
- 职责 (FACT)：组装 receipt.json 的完整 dict（25 个顶层键，对应 `RECEIPT_KEYS`）。
- 关键状态/结构：无持有状态。
- 关键流程/方法：`packet_fates` 重建（296-298）；`requested` 来自 `requested_from_config`（299）；`effective` 取 `result["mechanisms"]["effective"]` 的 `EFFECTIVE_KEYS` 四键（300）；汇总 schema/config_sha256/config_version/trace_manifest_sha256/trace_sha256/trace_identity_sha256/code_sha256()/ledgers_sha256/deps/seed/horizon_s/natural_end/interrupted/error/events_processed/mechanisms/research_eligible/routing_label/totals/fate_counts/packet_fates/control(counters+totals+fate_counts)/occupied/handover_event_count（301-329）；`conservation_ok` = `offered_bits == delivered_bits + terminal_loss_bits + in_system_bits_at_stop`（330-334）。
- 输入/输出：输入 resolved、manifest（含 `__sha256`/`__trace_sha256` 内部键）、result、rows、ledgers、ledgers_sha256；输出 receipt dict。
- 依赖关系：调用方仅 receipt.py:354（`write_run`）；内部调 `requested_from_config`(299)、`code_sha256`(308)、`dependency_versions`(310)。

#### `def write_run(out_dir, resolved, trace_csv, manifest, result, rows) -> dict` — CODE/leo_sim/receipt.py:338

- 定位：receipt.py:338-362。
- 职责 (FACT)：把一次运行的全部 artifacts 写入 `out_dir` 并返回 receipt dict。
- 关键流程/方法：建目录（340-341）；写 `resolved_config.json`（version+config，sorted keys，342-345）；写 `trace.csv` 字节（346）；写 `manifest.json`（剔除 `__` 前缀内部键，347-349）；`build_ledgers` 后写 `ledgers.json`（350-352）并用 `_sha_file` 算其 SHA（353）；`build_receipt`（354-355）；`result["monitor_log"]` 非空时写 `monitor.log`（每行 `t kind {dict}`，356-359）；写 `receipt.json`（360-361）；返回 receipt（362）。
- 输入/输出：输入输出目录、resolved、trace 字节串、manifest、result、rows；输出 receipt dict。
- 依赖关系：调用方 __main__.py:257（`_cmd_run`）、comparison.py:108、acceptance.py:110、platform_check.py:67 与 110、测试 test_review_round4.py:105、test_acceptance_review.py:110/150；内部调 `build_ledgers`(350)、`_sha_file`(353)、`build_receipt`(354)。

#### `def _is_nonneg_num(x) -> bool` — CODE/leo_sim/receipt.py:365

工具函数（压缩六字段）：定位 receipt.py:365-367。职责 (FACT)：`x` 是 int/float、非 bool、`math.isfinite` 且 `>= 0` 时返回 True。输入任意值；输出 bool。调用方：receipt.py:254（`_validate_manifest`）、`_validate_ledgers` 内多处（443、479、501、517、519、538-539 等）、receipt.py:845/857。

#### `def _is_nonneg_int(x) -> bool` — CODE/leo_sim/receipt.py:370

工具函数（压缩六字段）：定位 receipt.py:370-371。职责 (FACT)：`x` 是 int、非 bool 且 `>= 0` 时返回 True。输入任意值；输出 bool。调用方：receipt.py:257（`_validate_manifest`）、`_validate_ledgers` 内多处（407、505、514、524、554、556、580 等）。

#### `def _validate_ledgers(ledgers, receipt, trace_rows, verify_root, resolved_cfg) -> list[str]` — CODE/leo_sim/receipt.py:374

- 定位：receipt.py:374-582。
- 职责 (FACT，docstring 376-380)：对 ledgers.json 做 schema/类型/范围与内部关系校验；docstring 声明全程防御式——畸形内容只追加错误字符串、从不抛异常。
- 关键状态/结构：局部 `errors` 列表；`trace_rows` 为 pid(str) → `{bits, emit, deadline}` 映射。
- 关键流程/方法（按代码顺序）：
  - 顶层：`ledgers` 非 dict 直接返回单错误（382-383）；顶层键精确比对 `LEDGER_KEYS`，不符记错误但继续（384-388，注释 388 说明继续检查在场字段）；`field_authority` 必须精确等于 `FIELD_AUTHORITY`（389-390）。
  - learning 段（396-439，注释 392-395 说明该段防止保存/加载后的模型被静默替换）：receipt 请求的 `learning_algorithm == "none"` 时 ledger 必须恰为 `{"algorithm": "none"}`（399-401）；`== "ddqn"` 时：ledger 必须是 dict（403-404）；`decisions/transitions/train_steps/replay_size` 必须非负 int（406-408）；`algorithm == "ddqn"`（409-410）；`mode ∈ {"train","eval"}`（411-412）；`checkpoint_verified is True`（413-414）；`checkpoint_sha256` 必须是 64 位小写 hex（415-418）；`verify_root/ddqn/online.keras` 必须存在、非 symlink、且文件 SHA 与 ledger 一致（419-423）；与 `mechanism_counters` 的 `learning_decisions/learning_transitions/learning_train_steps` 三项必须一致（424-431）；`mode == "eval"` 时 `train_steps` 必须为 0（432-434），且 resolved config 提供 `learning.checkpoint_sha256` 时 `loaded_checkpoint_sha256` 必须与之相等（435-439）。
  - `stop_time_s`：必须有限非负（442-445）；`receipt.natural_end` 为真时必须恰等于 `receipt.horizon_s`（446-449）。
  - `packet_fates`：必须是 dict（452-455）；每条必须是 `[fate 字符串, 正 int bits]` 二元列表（456-461）。
  - `deliveries`：必须是 dict（464-467）；键集必须恰等于 fate 为 DELIVERED 的 pid 集（468-473）；每条恰含 `delivered_at`/`path` 两键（474-477）；`delivered_at` 有限非负、不早于 trace 的 emit、不晚于 trace 的 deadline（若有）、不晚于 stop_time（478-489）；`path` 必须是 int 列表（490-492）。
  - `occupied`/`queue_area_bits_s`：键集精确、各值有限非负（494-502）。
  - `events_processed`：非负 int（504-506）。
  - `access`：键集精确（509-511）；`ACCESS_INT_KEYS` 四键非负 int（513-515）；三个时长字段有限非负（516-518）；`wait_time_s_max <= wait_time_s_total + 1e-9`（519-522）；`releases` 必须是「字符串原因 → 非负 int」映射（523-526）。
  - `handover_events`：必须是列表（529-531）；每条含 `t`/`endpoint`/`type`（533-537）；`t` 有限非负且不晚于 stop_time（538-541）；`type ∈ HANDOVER_TYPES`（542-543）；`release` 类型必须带字符串 `reason`（544-545）。
  - `control_counters`：键集精确（548-551）；各值非负 int（553-555）；生命周期单调关系：`entered_queue <= registered`、`transmission_started <= entered_queue`、`transmission_completed <= transmission_started`、`arrived <= transmission_completed`（556-564）；`arrived+expired+lost+geometry_lost+overflow+duplicate+in_system == registered`（565-569）。
  - `mechanism_counters`：键集精确（572-574）；`MECHANISM_COUNTER_BOOLS` 三键必须 bool、其余非负 int（575-581）。
- 输入/输出：输入 ledgers（任意值）、receipt dict、trace_rows 映射、verify_root Path、可空 resolved config；输出错误字符串列表。
- 依赖关系：调用方仅 receipt.py:763（`verify_receipt_dir` 步骤 5，且调用被 try/except 包裹、异常转成错误字符串，receipt.py:761-766）；内部调 `_is_nonneg_num`/`_is_nonneg_int`/`_sha_file`(422)。

#### `def verify_receipt_dir(out_dir) -> list[str]` — CODE/leo_sim/receipt.py:585

- 定位：receipt.py:585-941。
- 职责 (FACT，docstring 586)：「重算每一条可校验的声明」，返回错误字符串列表，空列表 = 验证通过。
- 关键状态/结构：局部 `errors`、`receipt`、`manifest`、`trace_rows/trace_list`、`resolved_cfg/resolved_version`、`ledgers`。
- 关键流程/方法（fail-closed 验证链条，按代码顺序）：
  - 前置门禁：`receipt.json` 不存在立即返回单错误（589-591）；JSON 解析异常立即返回（592-595，注释 594 声明损坏 JSON 不得使 verify 崩溃）；解析结果非 dict 立即返回（596-597）。
  - 步骤 0（599-608）：receipt 顶层键精确等于 `RECEIPT_KEYS`；`schema == "leo-sim-receipt/v3"`；`natural_end/interrupted/research_eligible/conservation_ok` 必须为 bool。
  - 步骤 1（610-670）artifact 哈希与 trace/manifest 交叉：`trace.csv` 必须存在且非 symlink（617-618）；文件 SHA 须等于 `receipt.trace_sha256`（620-621）；`trace_mod.load_trace` 解析失败只记错误不崩溃（622-635）。`manifest.json` 同样存在性/非 symlink（636-638）且 SHA 绑定 `receipt.trace_manifest_sha256`（640-641）；解析防御（642-648）；`manifest.trace_sha256` 与 trace 文件实算 SHA 交叉（649-651）；`offered_packets`/`offered_bits`/`ledger`/`time_range_s`/`active_endpoints` 与 trace 实算逐项比对（652-670）。
  - 步骤 2（672-733）config 身份：`resolved_config.json` 存在且非 symlink（675-676）； canonical JSON（sort_keys、紧凑分隔符）SHA 须等于 `receipt.config_sha256`（678-684）；解析失败记错误（685-686）；必须含 scenario/routing 两个组（687-692）；`config_mod.resolve_config` 语义重校验、结果须与原文档逐键相等且 version 一致，失败记错误并置 `resolved_cfg = None`（693-702）；`receipt.config_version`/`seed`/`horizon_s` 分别比对 resolved config 的 version/`scenario.seed`/`scenario.duration_s`（703-709）；`routing_label`：`routing.policy == "oracle"` 时须为 `"analysis_upper_bound"`、否则须为 None（710-713）；`trace_mod.validate_packet_rows` 按 config 的 duration_s/max_packets 校验 trace（714-721）；调 `_validate_manifest`（722-723）；用 `config.trace_identity_sha256` 由 resolved config + manifest 的 `input_sha256` 重算 trace 身份并同时比对 manifest 与 receipt（724-733）。
  - 步骤 3（735-743）代码与依赖身份：`code_sha256()` 现算与 receipt 比对（736-737，错误消息明示"sources changed since the run"）；`deps` 键集精确等于 `DEP_KEYS` 且与当前环境 `dependency_versions()` 完全相等（738-743）。
  - 步骤 4（745-747）运行完成状态：`natural_end` 必须为 True 且 `interrupted` 必须为 False，否则记错误——非自然结束的 run 验证失败。
  - 步骤 5（749-906）ledgers：`ledgers.json` 存在且非 symlink（751-753）；SHA 绑定 `receipt.ledgers_sha256`（755-756）；解析防御（757-760）；调 `_validate_ledgers`，其内部任何异常被捕获转成错误（761-766）；receipt 与 ledgers 的 `packet_fates` 键集与内容必须相等（767-776）、`events_processed`/`occupied`/`handover_event_count` 一致（777-783）；只用 schema 合法的 `[fate, bits]` 对参与后续重算（789-797，注释 789-790 说明这使畸形 artifacts 保持 fail-closed 而不二次崩溃）；packet_fates 键集必须等于 trace pid 集（798-801）；bits 与 trace 一致、fate ∈ `fates.DATA_FATES`（802-807）；重算 `fate_counts` 并与 receipt 比对（808-813）；按 fate 分类求和 delivered/loss/in_system 与 `receipt.totals` 比对、三者之和须等于 `offered_bits`（814-823）；`receipt.conservation_ok` 必须为 True（824-825）；`manifest.offered_bits == receipt.totals.offered_bits`（826-827）；控制面 ledger 重算：每实例须为 `[fate, 正 int bits, received_at|None]`（830-843）、到达类 fate 必须有 received_at、未到达类 fate（CONTROL_EXPIRED 除外）不得有 received_at、received_at 不得晚于 stop_time（844-859）、fate ∈ `fates.CONTROL_FATES` 并逐 fate 计数（860-864）；由有效实例重算 control totals/fate_counts 并与 `receipt.control` 整体比对（865-880）；`control_counters` 与 `mechanism_counters` 的五项对应关系必须相等（884-893）、`registered` 须等于有效实例数（894-895）、各 fate 计数须等于对应计数器（896-906）。
  - 步骤 6（908-940）机制与研究资格：`mechanisms` 恰含 requested/effective（910-913）；requested 无未知键（914-915）；effective 键集精确等于 `EFFECTIVE_KEYS`（916-917）；`requested_from_config(resolved_cfg)` 重算并与 receipt 比对（918-923）；`effective_from_counters(ledgers.mechanism_counters, req)` 重算并与 receipt 比对（926-933）；`expected_research_eligible(...)` 重算（恒 False，见 receipt.py:150-158）并与 `receipt.research_eligible` 比对（934-938）；`requested.monitor` 为真时 `monitor.log` 必须存在（939-940）。
  - 返回 `errors`（941）。
- 输入/输出：输入运行输出目录路径字符串；输出错误字符串列表（空 = 通过）。
- 依赖关系：调用方 __main__.py:273（`_cmd_receipt_verify`，对应 CLI 子命令 `receipt verify`，注册于 __main__.py:350-354）、comparison.py:110、acceptance.py:112、platform_check.py:69 与 112；测试 test_review_round2.py:252-257/314、test_review_round3.py:257/314-333、test_review_round4.py:285/292-298/551-646、test_review_regressions.py:104-128、test_acceptance_review.py:125/160。被调方：`_sha_file`、`trace_mod.load_trace`/`validate_packet_rows`、`config_mod.resolve_config`、`config.trace_identity_sha256`、`_validate_manifest`、`_validate_ledgers`、`code_sha256`、`dependency_versions`、`requested_from_config`、`effective_from_counters`、`expected_research_eligible`、`fates` 的 fate 常量集。

fail-closed 验证链条要点（本文件范围内汇总，均为 FACT）：

1. 缺文件/坏 JSON/非 dict 立即返回错误，不继续（589-597）；后续各段的解析与校验异常一律捕获转成错误字符串而非崩溃（594 注释、632-635、646-648、685-686、700-701、759-766）。
2. 所有读盘 artifact 拒绝 symlink：trace.csv(617)、manifest.json(637)、resolved_config.json(675)、ledgers.json(752)、DDQN checkpoint(420)。
3. 哈希绑定链：receipt 绑定 trace.csv、manifest.json、ledgers.json、resolved_config 的 SHA（620、640、683、755）；manifest 再绑定 trace SHA（649-651）；ledgers 绑定 DDQN checkpoint 文件 SHA 并由验证器重算（415-423）；`code_sha256` 把 receipt 绑定到 leo_sim 包源码（736-737）。
4. 重算而非信任：fate_counts/totals/conservation/control 汇总/requested/effective/research_eligible 全部由验证器从 trace.csv + resolved_config.json + ledgers.json 重算后比对（767-938）。
5. 非自然结束（`natural_end` 非 True 或 `interrupted` 为 True）直接记错误（746-747）；`research_eligible` 的期望值恒为 False（150-158、934-938）。
6. 模块 docstring（1-10）明示该链条只证明内部一致性，外部锚（治理链）不在本模块。
# 片段 n5：leo_sim 治理链 / 验收 / 平台检查 / 对照 / 人口流量 / CLI

范围：`CODE/leo_sim/governance.py`、`CODE/leo_sim/acceptance.py`、`CODE/leo_sim/platform_check.py`、`CODE/leo_sim/comparison.py`、`CODE/leo_sim/population.py`、`CODE/leo_sim/__main__.py`、`CODE/leo_sim/__init__.py`。所有行号经 `wc -l` 实测与逐行通读核实。

---

## 文件 `CODE/leo_sim/governance.py`（实测 257 行）

模块级说明：
- 模块 docstring（第 1–9 行）声明本模块是「retained experiment compiler/authorization chain 引用 V2 runtime 的唯一预期入口」，不接受 shell 命令、不回退到旧 Gateway runtime，把 run intent 绑定到 config SHA、trace identity 和运行时代码 SHA；声明 compile → review → authorization → run-remote 的绑定仍是 VM 阶段门禁（FACT：docstring 原文如此；其中「唯一入口」是声明性表述，代码层面未见强制机制阻止其他模块直接调用 kernel）。
- imports（第 10–18 行）：`__future__.annotations`；stdlib `hashlib`、`json`、`pathlib.Path`；同包 `config`（别名 config_mod，第 16 行）、`receipt`（第 17 行）、`trace`（第 18 行）。
- 模块级常量（FACT）：
  - `RUNTIME_KIND = "leo_sim_v2"`（第 20 行）
  - `INTENT_SCHEMA = "leo-sim-run-intent/v1"`（第 21 行）
  - `REQUEST_SCHEMA = "leo-sim-experiment-request/v1"`（第 22 行）
  - `COMPILE_REPORT_SCHEMA = "leo-sim-experiment-compile-report/v1"`（第 23 行）
  - `RUN_MANIFEST_SCHEMA = "leo-sim-experiment-run-manifest/v1"`（第 24 行）
  - `ANALYSIS_REQUEST_SCHEMA = "leo-sim-analysis-request/v1"`（第 25 行）
  - `EXECUTION_CHAIN_PATHS`（第 26–31 行）：四个相对路径元组——`CODE/experiment_platform/authorize_experiment.py`、`CODE/scripts/remote/deployment_guard.py`、`CODE/scripts/remote/remote_job.py`、`CODE/scripts/remote/run-remote.sh`。
- 无环境变量读取。

### `class IntentError` — CODE/leo_sim/governance.py:34
- 定位：CODE/leo_sim/governance.py:34
- 职责：`ValueError` 子类，空体（`pass`，第 35 行），作为本模块所有校验失败的异常类型（FACT）。
- 关键状态/结构：无自有字段或方法。
- 关键流程/方法：无方法。
- 输入/输出：由 `execution_chain_sha256`（第 45 行）、`_write_json`（第 52 行）、`build_run_intent`（第 68/71/73/78/91/94/99 行）、`compile_experiment`（第 123/127/131/135/139/145/151/155/158/164/167/169 行）抛出。
- 依赖关系：被 `CODE/leo_sim/__main__.py:76` 捕获（experiment compile 失败返回退出码 2）；`__main__.py` 还在第 87/95/99/122/126/140/144 行自行抛出同一异常类。

### `def execution_chain_sha256()` — CODE/leo_sim/governance.py:38
- 定位：CODE/leo_sim/governance.py:38
- 职责：对 `EXECUTION_CHAIN_PATHS` 列出的四个授权/部署/启动文件逐一计算 SHA-256，返回 `{相对路径: hex digest}` 字典（FACT）。
- 关键流程：以 `Path(__file__).resolve().parents[2]`（即工作区根，第 40 行）为基准拼路径；任一文件是符号链接或不是常规文件即抛 `IntentError`（第 44–45 行）。
- 输入：无参数。输出：`dict[str, str]`。
- 依赖关系：调用 stdlib `hashlib.sha256`。被本文件 `compile_experiment`（第 193 行）调用写入 planned_run；被 `CODE/experiment_platform/authorize_experiment.py:346` 和第 511–512 行调用做授权复核；测试佐证 `CODE/leo_sim/tests/test_governance.py:26`。

### `def _write_json(path, value)` — CODE/leo_sim/governance.py:50
- 定位：CODE/leo_sim/governance.py:50
- 职责：把任意值以 `json.dumps(indent=2, sort_keys=True) + "\n"` 写入指定路径；路径是符号链接时抛 `IntentError` 拒绝写入（FACT，第 51–54 行）。
- 输入：`path: Path`、`value: object`。输出：无返回值，副作用是写文件。
- 依赖关系：仅被本文件 `compile_experiment` 调用（第 183、205、217、256 行）。外部调用方未确认。

### `def build_run_intent(request, *, project_root=None)` — CODE/leo_sim/governance.py:57
- 定位：CODE/leo_sim/governance.py:57
- 职责：校验一个 experiment-request 风格的 dict 并返回「封印的」run intent dict；docstring（第 58–66 行）声明除 `runtime_kind`/`config`/`profile` 外的字段一律拒绝（fail closed）（FACT）。
- 关键流程：
  - 非 dict 抛错（第 67–68 行）；未知字段抛错（第 69–71 行）。
  - `runtime_kind` 必须等于 `"leo_sim_v2"`，否则抛错，错误消息明示「legacy Gateway runtime 永不是隐式回退」（第 72–75 行）。
  - `config` 必须是 dict（第 76–78 行），随后调 `config_mod.resolve_config(user, profile=request.get("profile"))` 得到 resolved config（第 79 行）。
  - 按 `resolved["config"]["demand"]["mode"]` 分支（第 80 行）：`csv` 模式（第 82–95 行）解析 `csv_path`——相对路径基于 `project_root`（缺省 `Path.cwd()`），提供 `project_root` 时路径逃逸（`relative_to` 失败）抛错（第 87–92 行），文件不存在或是符号链接抛错（第 93–94 行），然后对文件字节算 SHA-256 得 `input_sha256`；`mlab` 模式（第 96–100 行）对 `trace_mod.REPO_MLAB_CSV`（`CODE/leo_sim/trace.py:28` 定义）做同样校验与哈希。其他 mode 时 `input_sha256` 保持空串 `""`（第 81 行，FACT——代码无 else 分支）。
  - 返回 dict（第 101–110 行）：`schema`、`runtime_kind`、`config_sha256`（取自 resolved）、`input_sha256`、`trace_identity_sha256`（调 `config_mod.trace_identity_sha256`，config.py:564）、`code_sha256`（调 `receipt_mod.code_sha256()`，receipt.py:95）、`resolved`（完整 resolved config 字典）。
- 输入：`request: dict`，关键字 `project_root: Path | None`。输出：intent dict。
- 依赖关系：调用 `config_mod.resolve_config`、`config_mod.trace_identity_sha256`、`receipt_mod.code_sha256`。被本文件 `compile_experiment`（第 159 行）调用；被 `CODE/experiment_platform/authorize_experiment.py:320` 和第 335 行调用（授权时重建 intent 比对）；测试佐证 `CODE/leo_sim/tests/test_governance.py:12-66`、`CODE/leo_sim/tests/test_acceptance_review.py:73-77`。

### `def compile_experiment(request_path, out_dir, project_root=None)` — CODE/leo_sim/governance.py:113
- 定位：CODE/leo_sim/governance.py:113
- 职责：把一份实验请求 JSON「编译」成一组可审阅的不变产物（request.json、resolved config、run-manifest.json、analysis-request.json、RUNBOOK.md、compile-report.json）；docstring（第 115–119 行）声明编译从不授权或启动运行，输出目录必须是新或空目录（FACT）。
- 关键流程：
  - 校验 `request_path` 非符号链接且是常规文件（第 122–123 行）；读取并 JSON 解析，失败抛 `IntentError`（第 124–127 行）。
  - 请求 dict 键集合必须恰好是 `{schema, experiment_id, runtime_kind, work_finalization, acceptance, config}`（第 128–133 行）；`schema` 必须等于 `REQUEST_SCHEMA`（第 134–135 行）。
  - `experiment_id` 必须是以 `EXP-` 开头、去掉 `-`/`_` 后全字母数字的字符串（第 136–139 行）。
  - `work_finalization` 必须是以 `CODE/work/` 开头、以 `/finalization.json` 结尾且路径分量不含 `..` 的字符串（第 140–146 行）。
  - `acceptance` 必须是键集合恰为 `{min_delivered_packets, min_multisat_deliveries, require_data_isl, require_control_delivery}` 的 dict（第 147–151 行）；前两者必须是非负 int 且非 bool（第 152–155 行），后两者必须是 bool（第 156–158 行）。
  - 用请求的 `runtime_kind`/`config` 调 `build_run_intent`（第 159–162 行）。
  - 输出目录：符号链接拒绝（第 163–164 行）；已存在但不是目录或非空拒绝（第 165–169 行）；不存在则 `mkdir(parents=True)`（第 170–171 行）；建 `resolved/` 子目录（第 172–173 行）。
  - `run_id = f"{experiment_id}-main-s{seed}"`，seed 取自 resolved config 的 `scenario.seed`（第 174 行）。
  - 写 `resolved/<run_id>.leo-sim.yaml`：内容为 `{"config_version": ..., **resolved["config"]}` 的 JSON（注释第 177 行说明「JSON 是 YAML 子集」）（第 175–181 行）。
  - 写 `request.json`（第 182–183 行）并对其字节算 `request_sha`（第 184 行）。
  - 组装 `planned_run`（第 185–196 行）：含 run_id、runtime_kind、config 相对路径、config_sha256、trace_identity_sha256、input_sha256、code_sha256、`execution_chain_sha256()` 的结果、acceptance 副本、seed。
  - 写 `run-manifest.json`（第 197–205 行）：`execution_authorized: False`、`planned_runs: [planned_run]`；算其 SHA-256（第 206–207 行）。
  - 写 `analysis-request.json`（第 208–217 行）：含 `comparison_contract: "same trace identity, seed and resource config"`。
  - 生成 `RUNBOOK.md` 文本（第 218–239 行）：内嵌授权命令（`CODE/experiment_platform/authorize_experiment.py`）与启动命令（`CODE/scripts/remote/run-remote.sh --runtime-kind leo_sim_v2 ...`）。
  - 对 `out_dir` 下所有文件算 `artifact_hashes`（第 241–244 行），写 `compile-report.json`（第 245–256 行）：`status: "COMPILED_REVIEW_REQUIRED"`、`execution_authorized: False`、`launcher_generated: False`。
- 输入：`request_path: Path`、`out_dir: Path`、可选 `project_root`。输出：compile-report dict（同时写出一目录产物）。
- 依赖关系：调用 `build_run_intent`、`execution_chain_sha256`、`_write_json`。被 `CODE/leo_sim/__main__.py:74`（CLI `experiment compile`）调用；被 `CODE/experiment_platform/tests/test_authorize_experiment.py:242` 调用；测试佐证 `CODE/leo_sim/tests/test_governance.py:96/126/145`。

---

## 文件 `CODE/leo_sim/acceptance.py`（实测 153 行）

模块级说明：
- 模块 docstring（第 1–7 行）声明这是「面向结果的验收运行器」，与单元测试不同：把若干真实 Walker 几何场景跑过公开 runtime，并检查所请求机制确实在事件/归宿账本中被观察到，仅到达时界不算通过（FACT：docstring 原文；具体检查逻辑见 `_case_checks`）。
- imports（第 8–15 行）：`__future__.annotations`；stdlib `hashlib`、`json`、`time`、`pathlib.Path`；同包 `config`、`kernel`、`receipt`、`trace`（第 15 行）。
- 模块级常量（FACT）：`PROFILE_DIR = <包目录>/profiles/acceptance`（第 18 行）；`SCENARIOS = ("direct", "k1", "bbm", "mbb", "ge")`（第 19 行）。`CODE/leo_sim/profiles/acceptance/` 目录实测存在 direct.yaml、k1.yaml、bbm.yaml、mbb.yaml、ge.yaml（另有 ddqn.yaml 等）。
- 无环境变量读取。

### `class AcceptanceError` — CODE/leo_sim/acceptance.py:22
- 定位：CODE/leo_sim/acceptance.py:22
- 职责：`RuntimeError` 子类，空体（第 23 行），本模块失败异常类型（FACT）。
- 关键状态/结构：无。关键流程/方法：无方法。
- 输入/输出：由 `_case_checks`（第 90 行）、`run_acceptance`（第 139/141 行）抛出。
- 依赖关系：被 `CODE/leo_sim/__main__.py:284` 捕获（CLI 退出码 2）。

### `def _max_satellite_occupancy(events)` — CODE/leo_sim/acceptance.py:26
- 定位：CODE/leo_sim/acceptance.py:26
- 职责：从切换事件序列计算单颗卫星同时关联 endpoint 数的峰值（FACT）。
- 关键流程：维护 `{sat: {endpoint集合}}`（第 27 行）；`type == "associate"` 时加入集合并刷新最大值（第 34–36 行），`type == "release"` 时 discard（第 37–38 行）；`sat` 非 int 或 `endpoint` 非 str 的事件跳过（第 32–33 行）。
- 输入：`events: list[dict]`。输出：`int`（峰值占用数）。
- 依赖关系：仅被本文件 `_case_checks` 的 `k1` 分支调用（第 66 行）。外部调用方未确认。

### `def _case_checks(name, result)` — CODE/leo_sim/acceptance.py:42
- 定位：CODE/leo_sim/acceptance.py:42
- 职责：按场景名返回该场景的通过条件字典 `{检查名: bool}`（FACT）。
- 关键流程：所有场景共享 `common` 三项（第 47–51 行）：`natural_end is True`、`conservation_ok is True`、`fates["DELIVERED"] > 0`。各场景附加项（FACT，均直接读 result 字段）：
  - `direct`（第 52–59 行）：`occupied["isl_s"] > 0`（多星数据服务）、控制计数 `arrived > 0`、`effective["control_plane"] is True`、`routing_label != "oracle"`。
  - `k1`（第 60–67 行）：access `requests > 0`、`wait_time_s_max > 0`、`grants > 0`、`_max_satellite_occupancy(events) <= 1`（单槽位不超限）。
  - `bbm`（第 68–73 行）：事件里存在 `type == "bbm"`、access `releases["bbm_switch"] > 0`。
  - `mbb`（第 74–82 行）：事件里存在 `type == "mbb"`、`effective["mbb"] is True`、access `releases` 中存在以 `mbb_` 开头且计数 > 0 的键。
  - `ge`（第 83–89 行）：`effective["ge"] is True`、`fates["RANDOM_OUTAGE_IN_FLIGHT"] > 0`、`effective["ge_failures"] > 0`。
  - 其他名字抛 `AcceptanceError`（第 90 行）。
- 输入：场景名 `name: str`、运行结果 dict（含 `handover`/`fate_counts`/`access`/`mechanisms`/`conservation_ok`/`routing_label` 等键）。输出：`dict[str, bool]`。
- 依赖关系：调用 `_max_satellite_occupancy`。仅被本文件 `_run_case` 调用（第 116 行）。

### `def _run_case(name, out_dir)` — CODE/leo_sim/acceptance.py:93
- 定位：CODE/leo_sim/acceptance.py:93
- 职责：加载 `PROFILE_DIR/<name>.yaml`，编译 trace、跑仿真、写回执并自校验，然后按 `_case_checks` 判定 PASS/FAIL，返回该用例的结果 dict（FACT）。
- 关键流程：`config.load_config_file`（第 95 行）→ 建输出目录（`exist_ok=False`，第 96 行）→ `trace.compile_trace`（第 97 行）→ 读 trace.csv 字节并把 `__trace_sha256`、`__sha256` 两个键补进 manifest dict（第 98–101 行）→ `trace.load_trace`（第 102–106 行，horizon 与 max_packets 取自 resolved config）→ `kernel.run_simulation` 并计 wall 时间（第 107–109 行）→ `receipt.write_run`（第 110–111 行）→ `receipt.verify_receipt_dir`（第 112 行）→ 把 receipt 的 `conservation_ok`/`routing_label` 并入 observed（第 113–115 行）→ `_case_checks` 加 `receipt_verified`（第 116–117 行）→ 返回含 status/profile（相对于工作区根，第 120 行）/result_dir/wall_seconds/checks/receipt_errors/outcomes 的 dict（第 118–133 行）。
- 输入：场景名与输出目录 `Path`。输出：用例结果 dict；副作用是写出一整个 run 目录。
- 依赖关系：调用 `config.load_config_file`、`trace.compile_trace`、`trace.load_trace`、`kernel.run_simulation`、`receipt.write_run`、`receipt.verify_receipt_dir`、`_case_checks`。仅被本文件 `run_acceptance` 调用（第 145 行）。

### `def run_acceptance(out_dir)` — CODE/leo_sim/acceptance.py:136
- 定位：CODE/leo_sim/acceptance.py:136
- 职责：对 `SCENARIOS` 五个场景逐个跑 `_run_case`，汇总写 `acceptance-summary.json`，返回汇总 dict（FACT）。
- 关键流程：输出目录为符号链接（第 138–139 行）或已存在且非空/非目录（第 140–141 行）时抛 `AcceptanceError`；否则建目录（第 142 行），循环跑用例（第 143–145 行）；汇总 schema 为 `"leo-sim-acceptance/v1"`，全部用例 PASS 才总 PASS（第 146–150 行），落盘（第 151–152 行）。
- 输入：`out_dir: str | Path`。输出：`{"schema", "status", "cases"}` dict。
- 依赖关系：调用 `_run_case`。被 `CODE/leo_sim/platform_check.py:222`（mechanisms 阶段）与 `CODE/leo_sim/__main__.py:283`（CLI `acceptance run`）调用；测试中以 monkeypatch 替身出现于 `CODE/leo_sim/tests/test_platform_check.py:29、45`。

---

## 文件 `CODE/leo_sim/platform_check.py`（实测 270 行）

模块级说明：
- 模块 docstring（第 1–7 行）声明这是「面向用户的闭环检查路径，不是又一个评审层」：跑真实机制场景、保留的 Gateway/direct 同 trace 对照、以及 TensorFlow DDQN train/save/load/eval 链；首个失败阶段即停并记入 `platform-summary.json`（FACT：docstring 原文；阶段编排见 `run_platform_check`）。
- imports（第 8–18 行）：`__future__.annotations`；stdlib `copy`、`hashlib`、`importlib.metadata`、`json`、`platform`、`datetime/timezone`、`pathlib.Path`；同包 `acceptance`、`comparison`、`config`、`kernel`、`receipt`、`trace`（第 18 行）。
- 模块级常量（FACT）：`DDQN_PROFILE = profiles/acceptance/ddqn.yaml`（第 21 行）、`COMPARISON_PROFILE = profiles/comparison.yaml`（第 22 行）、`POPULATION_PROFILE = profiles/population_gravity.yaml`（第 23 行），三者均基于包目录拼接；三个文件实测存在。
- 无环境变量读取。

### `class PlatformCheckError` — CODE/leo_sim/platform_check.py:26
- 定位：CODE/leo_sim/platform_check.py:26
- 职责：`RuntimeError` 子类，空体（第 27 行），本模块失败异常类型（FACT）。
- 关键状态/结构：无。关键流程/方法：无方法。
- 输入/输出：由 `_run_population`（第 104 行）、`_run_ddqn_chain`（第 148/156 行）、`run_platform_check`（第 199/204/226/234/242/249 行）抛出。
- 依赖关系：被 `CODE/leo_sim/__main__.py:307` 捕获（CLI 退出码 9）；测试佐证 `CODE/leo_sim/tests/test_platform_check.py:72、81`。

### `def _utc_now()` — CODE/leo_sim/platform_check.py:30
第 30–31 行：返回 `datetime.now(timezone.utc).isoformat()`（FACT）。输入无；输出 ISO 格式 UTC 时间字符串。仅被本文件 `run_platform_check` 调用（第 210、257、262 行）。

### `def _write_summary(root, summary)` — CODE/leo_sim/platform_check.py:34
第 34–36 行：把 summary dict 以 `json.dumps(indent=2, sort_keys=True) + "\n"` 写到 `<root>/platform-summary.json`（FACT）。输入为目录 `Path` 与 dict；无返回值。仅被本文件 `run_platform_check` 调用（第 218、224、232、240、258、269 行）。

### `def _dependency_snapshot()` — CODE/leo_sim/platform_check.py:39
第 39–46 行：返回依赖版本快照 dict——`python` 取 `platform.python_version()`；对 `numpy`、`simpy`、`pyyaml`、`tensorflow` 逐包用 `importlib.metadata.version` 取版本，未安装时记 `None`（捕获 `PackageNotFoundError`）（FACT）。输入无；输出 dict。仅被本文件 `run_platform_check` 调用（第 212 行）。

### `def _compile_trace(resolved, trace_dir)` — CODE/leo_sim/platform_check.py:49
第 49–60 行：调 `trace.compile_trace`（第 50 行），读回 trace.csv 与 manifest.json 字节并把 `__trace_sha256`、`__sha256` 补进 manifest dict（第 51–54 行），再按 resolved config 的 duration/max_packets 调 `trace.load_trace`（第 55–59 行），返回 `(manifest, trace_bytes, rows)` 三元组（FACT）。输入：resolved config dict 与输出目录；输出三元组。被本文件 `_run_population`（第 106 行）与 `_run_ddqn_chain`（第 150 行）调用。

### `def _run_learning_arm(name, resolved, rows, trace_bytes, manifest, out_dir)` — CODE/leo_sim/platform_check.py:63
- 定位：CODE/leo_sim/platform_check.py:63
- 职责：跑一个带学习机制的仿真臂（train 或 eval），写回执并按学习账本判定 PASS/FAIL（FACT）。
- 关键流程：`kernel.run_simulation(..., learning_out_dir=out_dir/"ddqn")`（第 65–66 行）→ `receipt.write_run`（第 67–68 行）→ `receipt.verify_receipt_dir`（第 69 行）→ 取 `result["learning"]` 账本与期望 mode（第 70–71 行）→ 公共检查七项（第 72–80 行：natural_end、data_conservation、receipt_verified、delivered_data、learning_effective、mode_exact、model_save_load_verified 即 `checkpoint_verified is True`）→ train 模式加查 `train_steps > 0`（第 81–82 行）；eval 模式加查 `decisions > 0`、`train_steps == 0`、`loaded_checkpoint_sha256` 等于配置请求的 `checkpoint_sha256`（第 83–88 行）→ 返回含 status/name/result_dir/trace_sha256/fate_counts/learning/checks/receipt_errors 的 dict（第 89–98 行）。
- 输入：臂名、resolved config、trace 行、trace 字节、manifest、输出目录。输出：臂结果 dict。
- 依赖关系：调用 `kernel.run_simulation`、`receipt.write_run`、`receipt.verify_receipt_dir`。仅被本文件 `_run_ddqn_chain` 调用（第 152、168 行）。

### `def _run_population(profile, out_dir)` — CODE/leo_sim/platform_check.py:101
- 定位：CODE/leo_sim/platform_check.py:101
- 职责：用 population_gravity 配置编译 trace 并跑一臂 satellite_direct 仿真，验证人口代理流量相关声明与运行结果（FACT）。
- 关键流程：`config.load_config_file`（第 102 行）→ demand mode 必须是 `"population_gravity"`，否则抛 `PlatformCheckError`（第 103–105 行）→ `_compile_trace`（第 106–107 行）→ `kernel.run_simulation`（第 109 行）→ `receipt.write_run` + `verify_receipt_dir`（第 110–112 行）→ 从 trace 行统计源/目的 grid 集合（第 113–114 行）→ 八项检查（第 115–125 行）：manifest `provenance == "population_proxy"`、`not_calibrated_user_demand is True`、源区域数 > 1、目的区域数 > 1、natural_end、data_conservation、`DELIVERED > 0`、receipt_verified → 返回含 status/profile/result_dir/trace_sha256/offered_packets/活跃源与目的区域数/manifest 的 `population.candidate_regions` 与 `total_population`/fate_counts/checks/receipt_errors 的 dict（第 126–140 行）。
- 输入：profile 路径与输出目录。输出：阶段结果 dict。
- 依赖关系：调用 `config.load_config_file`、`_compile_trace`、`kernel.run_simulation`、`receipt.write_run`、`receipt.verify_receipt_dir`。仅被本文件 `run_platform_check` 调用（第 229 行）。

### `def _run_ddqn_chain(profile, out_dir)` — CODE/leo_sim/platform_check.py:143
- 定位：CODE/leo_sim/platform_check.py:143
- 职责：执行 DDQN train → 保存 checkpoint → 构造 eval 配置 → eval 的闭环链，并验证两段跑的是同一 trace、eval 加载的是训练出的 checkpoint（FACT）。
- 关键流程：加载配置并强制要求 `learning.algorithm == "ddqn"` 且 `mode == "train"`，否则抛 `PlatformCheckError`（第 144–148 行）→ `_compile_trace`（第 150–151 行）→ `_run_learning_arm("ddqn_train", ...)`（第 152–154 行），train 不 PASS 直接抛错并附检查 JSON（第 155–158 行）→ 取训练产物 `train/ddqn/online.keras` 的绝对路径与其 SHA-256（第 160–161 行）→ `copy.deepcopy` 配置改 eval：场景名加 `-eval` 后缀、`mode="eval"`、写入 checkpoint 路径与 SHA（第 162–166 行）→ `config.resolve_config` 重新解析（第 167 行）→ `_run_learning_arm("ddqn_eval", ...)`，注意复用同一 `rows`/`trace_bytes`/`manifest`（第 168–170 行）→ 四项汇总检查（第 172–180 行：train_passed、eval_passed、same_immutable_trace 即两臂 trace_sha256 相等、eval_loaded_trained_checkpoint）→ 返回含 status/trace_sha256/trained_checkpoint(及 SHA)/checks/train/eval 的 dict（第 181–189 行）。
- 输入：profile 路径与输出目录。输出：链式结果 dict。
- 依赖关系：调用 `config.load_config_file`、`config.resolve_config`、`_compile_trace`、`_run_learning_arm`。仅被本文件 `run_platform_check` 调用（第 245 行）。

### `def run_platform_check(out_dir, comparison_config=..., ddqn_config=..., population_config=...)` — CODE/leo_sim/platform_check.py:192
- 定位：CODE/leo_sim/platform_check.py:192
- 职责：按固定顺序编排四个阶段并汇总为单一最终结果；docstring（第 196 行）「Run every executable platform path and return one final outcome」（FACT）。
- 关键流程：
  - 输出目录：符号链接拒绝（第 198–200 行）；resolve 后已存在且非目录/非空则抛 `PlatformCheckError`（第 201–205 行）；建目录（第 206 行）。
  - 初始化 summary（第 207–217 行）：schema `"leo-sim-platform-check/v1"`、status RUNNING、起始时间、result_dir、依赖快照、以及 `evidence_scope` 声明「仅工程执行证据；本检查不证明算法优越性或经校准的物理保真度」（FACT，第 213–215 行原文）；立即落盘（第 218 行）。
  - 阶段 `mechanisms`（第 220–226 行）：调 `acceptance.run_acceptance`，写入 summary 并落盘，非 PASS 抛错。
  - 阶段 `population_traffic`（第 228–234 行）：调 `_run_population`，同样模式。
  - 阶段 `gateway_vs_direct`（第 236–242 行）：调 `comparison.run_comparison`，同样模式。
  - 阶段 `ddqn_train_eval`（第 244–249 行）：调 `_run_ddqn_chain`；注意该阶段结果写入 summary 后未立即落盘即检查（FACT：第 247–249 行之间无 `_write_summary`，失败路径由 except 分支统一落盘）。
  - 任一异常（`except Exception`，第 250–259 行）：status 置 FAIL、记录 `failed_stage` 与异常 type/message、写完成时间、落盘并返回 summary。
  - 全部通过（第 261–270 行）：status PASS、写完成时间与四项布尔 checks（all_mechanisms_ran / population_gravity_traffic_ran / same_trace_gateway_and_direct_ran / ddqn_train_save_load_eval_ran），落盘返回。
- 输入：`out_dir` 及三个可选配置路径（默认取模块级三个 PROFILE 常量）。输出：summary dict；副作用是整棵结果目录与逐阶段更新的 `platform-summary.json`。
- 依赖关系：调用 `acceptance.run_acceptance`、`comparison.run_comparison`、`_run_population`、`_run_ddqn_chain`、`_dependency_snapshot`、`_utc_now`、`_write_summary`。被 `CODE/leo_sim/__main__.py:303`（CLI `platform check`）调用；测试佐证 `CODE/leo_sim/tests/test_platform_check.py:35、61`（及 monkeypatch 第 29–30、45、55、88 行）。

---

## 文件 `CODE/leo_sim/comparison.py`（实测 271 行）

模块级说明：
- 模块 docstring（第 1–8 行）声明这是「同一条不可变需求 trace 上的一命令诊断对照」：direct 臂用 leo_sim V2，保留臂（retained arm）调 SimulationRL、关闭其内生 Gateway 流量并把同一 trace 注入其真实 Gateway 上行；声明这是需求受控的工程对照，不是算法效果实验，也不声称两套几何实现物理一致（FACT：docstring 原文）。
- imports（第 9–21 行）：`__future__.annotations`；stdlib `csv`、`hashlib`、`json`、`os`、`subprocess`、`sys`、`time`、`dataclasses.dataclass`、`pathlib.Path`；同包 `config`、`kernel`、`receipt`、`trace`（第 21 行）；第 22 行 `from CODE.legacy_trace_runtime import load_and_project_trace`（该文件存在，其 docstring 自述为「保留 Gateway runtime 的不可变需求适配器」）。
- 无模块级常量；无环境变量读取（但 `_legacy_arm` 会向子进程注入大量 `SIM_*` 环境变量，见下）。

### `class ComparisonError` — CODE/leo_sim/comparison.py:25
- 定位：CODE/leo_sim/comparison.py:25
- 职责：`RuntimeError` 子类，空体（第 26 行），本模块失败异常类型（FACT）。
- 关键状态/结构：无。关键流程/方法：无方法。
- 输入/输出：由 `_legacy_constellation`（第 59 行）、`_legacy_pathing`（第 82 行）、`_write_legacy_input`（第 90 行）、`_direct_arm`（第 112 行）、`_legacy_arm`（第 177/181/186/188 行）、`run_comparison`（第 206/211/213 行）抛出。
- 依赖关系：被 `CODE/leo_sim/__main__.py:294` 捕获（CLI 退出码 8）；测试佐证 `CODE/leo_sim/tests/test_comparison.py:47、71`。

### `class _GatewaySite` — CODE/leo_sim/comparison.py:30
- 定位：CODE/leo_sim/comparison.py:30（`@dataclass` 装饰器在第 29 行）
- 职责：承载一个旧平台 Gateway 站点的名称、经纬度与在 Gateways.csv 中的行号（FACT：字段定义如此）。
- 关键状态/结构：四个字段——`name: str`（第 31 行）、`latitude: float`（第 32 行）、`longitude: float`（第 33 行）、`active_index: int`（第 34 行）。
- 关键流程/方法：无自定义方法（dataclass 自动生成 `__init__` 等）。
- 输入/输出：由 `_gateway_sites` 构造（第 68–76 行）；被 `run_comparison` 经 `load_and_project_trace` 的投影结果按 `active_index` 筛选（第 230–232 行）；`_legacy_arm` 消费其实例列表。
- 依赖关系：仅本文件内使用。外部调用方未确认。

### `def _canonical_sha(value)` — CODE/leo_sim/comparison.py:37
第 37–39 行：对 dict 做 `json.dumps(ensure_ascii=False, sort_keys=True, separators=(",", ":"))` 序列化后取 SHA-256 hex（FACT）。输入 dict；输出 hex 字符串。仅被本文件 `_legacy_arm` 调用（第 160 行，用于构造 `SIM_EXPECTED_TRAFFIC_CONFIG_SHA256`）。

### `def _legacy_constellation(cfg)` — CODE/leo_sim/comparison.py:42
- 定位：CODE/leo_sim/comparison.py:42
- 职责：把 scenario 配置的五元组（卫星数、平面数、高度、倾角、最小仰角，第 44–48 行）映射到旧平台星座壳名称（FACT）。
- 关键流程：内置映射表（第 49–55 行）：`(32,4,1000.0,53.0,30.0)→"small"`、`(140,7,600.0,98.6,30.0)→"Kepler"`、`(66,6,780.0,86.4,30.0)→"Iridium_NEXT"`、`(648,18,1200.0,86.4,30.0)→"OneWeb"`、`(1584,72,550.0,53.0,25.0)→"Starlink"`；查不到抛 `ComparisonError`（第 56–61 行）。测试佐证 `CODE/leo_sim/tests/test_comparison.py:47`（未知星座被拒）。
- 输入：`cfg`（含 `scenario` 段的 dict）。输出：星座名字符串。
- 依赖关系：仅被本文件 `_legacy_arm` 调用（第 134 行）。

### `def _gateway_sites(code_dir)` — CODE/leo_sim/comparison.py:64
- 定位：CODE/leo_sim/comparison.py:64
- 职责：读 `<code_dir>/Gateways.csv`，把每行（DictReader 字段 `Location`/`Latitude`/`Longitude`）转成 `_GatewaySite`，`active_index` 为行号（FACT，第 64–76 行）。`CODE/Gateways.csv` 实测存在。
- 输入：`code_dir: Path`。输出：`list[_GatewaySite]`。
- 依赖关系：仅被本文件 `run_comparison` 调用（第 226 行）。

### `def _legacy_pathing(policy)` — CODE/leo_sim/comparison.py:79
第 79–84 行：把 V2 路由策略名映射为旧平台 pathing 名——`{"hop": "hop", "delay": "slant_range", "capacity": "dataRate"}`；不在表内抛 `ComparisonError`（错误消息说明「无对应非 oracle 等价物」）（FACT）。输入策略名；输出旧平台 pathing 字符串。仅被本文件 `_legacy_arm` 调用（第 143 行）。

### `def _write_legacy_input(path, gateway_names, constellation, duration_s)` — CODE/leo_sim/comparison.py:87
- 定位：CODE/leo_sim/comparison.py:87
- 职责：生成旧平台 SimulationRL 的 inputRL CSV 文件（FACT）。
- 关键流程：站点数少于 2 抛 `ComparisonError`（第 89–90 行）；写表头 `Locations,Constellation,Fraction,Test type,Test length`（第 93 行）；第一站写 `[别名, constellation, 0.5, "Latency", duration_s]`（第 96–97 行），其余站写别名加四个空字段（第 98–99 行）；别名 = 全名第一个逗号前部分（第 95 行）。
- 输入：输出路径、站点全名列表、星座名、时长秒。输出：无返回值，写 CSV 文件。
- 依赖关系：仅被本文件 `_legacy_arm` 调用（第 135 行）。

### `def _direct_arm(resolved, rows, trace_bytes, manifest, out_dir)` — CODE/leo_sim/comparison.py:102
- 定位：CODE/leo_sim/comparison.py:102
- 职责：跑 V2 内核这一臂：仿真、写回执、自校验，失败即抛错，成功返回臂摘要 dict（FACT）。
- 关键流程：建目录（`exist_ok=False`，第 104 行）→ `kernel.run_simulation` 计时（第 105–107 行）→ `receipt.write_run`（第 108–109 行）→ `receipt.verify_receipt_dir`（第 110 行）→ 非 natural_end 或有校验错误抛 `ComparisonError`（第 111–114 行）→ 返回 `runtime="satellite_direct"`、wall_seconds、trace_sha256、natural_end、conservation_ok、fate_counts、totals、mechanisms、result_dir（第 115–125 行）。
- 输入：resolved config、trace 行、trace 字节、manifest、输出目录。输出：臂摘要 dict。
- 依赖关系：调用 `kernel.run_simulation`、`receipt.write_run`、`receipt.verify_receipt_dir`。仅被本文件 `run_comparison` 调用（第 234 行）。

### `def _legacy_arm(resolved, trace_path, trace_sha, selected, out_dir, code_dir)` — CODE/leo_sim/comparison.py:128
- 定位：CODE/leo_sim/comparison.py:128
- 职责：以子进程方式跑旧平台 SimulationRL 这一臂：准备输入、注入受控环境变量、执行、校验其运行回执消费了同一 trace，返回臂摘要 dict（FACT）。
- 关键流程：
  - 建 `out_dir/results`（第 131–132 行）；调 `_legacy_constellation`（第 134 行）与 `_write_legacy_input` 生成 inputRL.csv（第 133–138 行）。
  - 构造 `trace_cfg = {"mode": "trace", "trace_sha256": trace_sha}`（第 139 行）。
  - 复制当前环境并注入变量（第 140–166 行）：`MPLBACKEND=Agg`、`SIM_PATHING`（`_legacy_pathing` 结果）、`SIM_FAST=1`、`SIM_FAIL_CLOSED=1`、`SIM_GTS=选中站点数`、`SIM_TIME_LIMIT=时长`、`SIM_MOVEMENT_TIME=步长`、`SIM_MOVEMENT_SPEEDUP=1`、`SIM_WALKER_PATTERN=delta`（第 149–152 行注释说明：旧默认约 290 倍压缩轨道时间且 Kepler 用 Walker-star 半 RAAN 布局，此处显式对齐物理秒与 Walker-delta 而不改动旧运行时其他处的默认值）、`SIM_INPUT_RL_PATH`、`SIM_TRAFFIC_TRACE_PATH`、`SIM_EXPECTED_TRAFFIC_TRACE_SHA256`、`SIM_TRAFFIC_TRACE_MAX_PACKETS`、`SIM_REQUESTED_TRAFFIC_MODE=trace`、`SIM_EXPECTED_TRAFFIC_CONFIG_SHA256`（`_canonical_sha(trace_cfg)`）、`SIM_RESULTS_ROOT`、`SIM_SEED`、`SIM_GSL_KEEP_STABLE=1`、`SIM_GSL_HANDOVER_MODE`（access.association 为 mbb 时 `"mbb"`，否则 `"legacy"`）。
  - 子进程执行 `[sys.executable, <code_dir>/SimulationRL.py]`，cwd=code_dir，stdout/stderr 并入 `legacy.log`，`check=False`（第 167–174 行）；退出码非 0 抛错（第 176–178 行）。
  - 在 `legacy_root` 下 glob `*/run_trace/run_meta.json`，必须恰好一个（第 179–182 行）；解析后要求 `trace_traffic` 是 dict 且 `valid` 为真（第 183–186 行）、其 `trace_sha256` 与本臂 trace SHA 一致（第 187–188 行）。
  - 返回 `runtime="legacy_gateway"`、wall_seconds、trace_sha256、natural_end、conservation_ok（= `trace_traffic.errors` 为空）、packets、bits、projection、result_dir、log（第 189–200 行）。
- 输入：resolved config、trace 文件路径与其 SHA、选中 `_GatewaySite` 列表、输出目录、代码目录。输出：臂摘要 dict。
- 依赖关系：调用 `_legacy_constellation`、`_write_legacy_input`、`_legacy_pathing`、`_canonical_sha`；经 `subprocess` 调 `CODE/SimulationRL.py`。仅被本文件 `run_comparison` 调用（第 238 行）。

### `def run_comparison(config_path, out_dir)` — CODE/leo_sim/comparison.py:203
- 定位：CODE/leo_sim/comparison.py:203
- 职责：编译一条不可变 trace，先后跑 satellite_direct（V2 内核）与 legacy_gateway（旧 SimulationRL 子进程）两臂，按八项检查汇总对照结论并写 `comparison-summary.json`（FACT）。
- 关键流程：
  - 输出目录 resolve 后：符号链接或已存在且非空/非目录抛 `ComparisonError`（第 204–206 行）；建目录（第 207 行）。
  - `config.load_config_file`（第 208 行）；拒绝 learning 算法非 `"none"`（第 210–211 行）；拒绝开启 GE（错误消息：断链参数未跨 runtime 校准，第 212–213 行）。
  - `code_dir = Path(__file__).resolve().parents[1]`，即 `CODE/` 目录（第 214 行）。
  - 编译 trace 到 `immutable_trace/`：与 acceptance/platform_check 相同的 manifest 补键模式（第 215–224 行）。
  - `_gateway_sites(code_dir)` 读全部站点（第 226 行）；调 `load_and_project_trace`（`CODE/legacy_trace_runtime.py`，带 `expected_sha256` 与 max_packets）把 trace 投影到站点（第 227–229 行）；收集投影实际用到的源/目的站点 `active_index`，取 `selected` 子列表（第 230–232 行）。
  - 先跑 `_direct_arm`（第 234–235 行），再建 `legacy_gateway/` 目录跑 `_legacy_arm`（第 236–239 行）。
  - 八项检查（第 240–252 行）：same_trace（两臂 SHA 均等于编译 SHA）、same_offered_bits（direct totals.offered_bits == legacy bits.offered）、direct_natural_end、legacy_natural_end、direct_conservation、legacy_conservation、direct_delivered（DELIVERED > 0）、legacy_delivered（packets.delivered > 0）。
  - 汇总 dict（第 253–268 行）：schema `"leo-sim-access-comparison/v1"`；`comparison_scope` 声明「同一不可变需求、物理时间尺度、Walker-delta 模式与壳参数；两个 runtime 的几何实现仍然不同」；`alignment`（movement_speedup=1.0、walker_pattern=delta、topology_tick_s）；`scientific_effect_claim: False`（FACT，第 262 行硬编码）；seed；两臂摘要。
  - 写 `comparison-summary.json`（第 269–270 行）并返回 summary。
- 输入：配置文件路径与输出目录。输出：summary dict。
- 依赖关系：调用 `config.load_config_file`、`trace.compile_trace`、`trace.load_trace`、`_gateway_sites`、`load_and_project_trace`、`_direct_arm`、`_legacy_arm`。被 `CODE/leo_sim/platform_check.py:237`（gateway_vs_direct 阶段）与 `CODE/leo_sim/__main__.py:293`（CLI `compare run`）调用；测试佐证 `CODE/leo_sim/tests/test_comparison.py:47、71`；monkeypatch 见于 `CODE/leo_sim/tests/test_platform_check.py:30、55`。

---

## 文件 `CODE/leo_sim/population.py`（实测 139 行）

模块级说明：
- 模块 docstring（第 1 行）：「Deterministic GPW population aggregation for V2 traffic endpoints」（FACT：原文）。其中 GPW 所指数据源在本文件内无进一步说明（未确认）。
- imports（第 2–11 行）：`__future__.annotations`；stdlib `hashlib`、`math`、`dataclasses.dataclass`、`pathlib.Path`；第三方 `numpy`（第 9 行）；同包 `grid`（第 11 行）。PIL（`from PIL import Image`）在 `load_population_regions` 内惰性导入（第 102 行）。
- 无模块级常量；无环境变量读取。

### `class PopulationError` — CODE/leo_sim/population.py:14
- 定位：CODE/leo_sim/population.py:14
- 职责：`ValueError` 子类，空体（第 15 行），本模块校验失败异常类型（FACT）。
- 关键状态/结构：无。关键流程/方法：无方法。
- 输入/输出：由 `aggregate_population_array`（第 49/55/57/62/67/74/92 行）与 `load_population_regions`（第 100/107/112/120/128 行）抛出。
- 依赖关系：测试佐证 `CODE/leo_sim/tests/test_population.py:29、50`（pytest.raises 匹配）。

### `class PopulationRegion` — CODE/leo_sim/population.py:19
- 定位：CODE/leo_sim/population.py:19（`@dataclass(frozen=True)` 在第 18 行）
- 职责：不可变记录一个聚合地理网格的人口：grid_id、中心纬度、中心经度、人口数（FACT：字段定义如此）。
- 关键状态/结构：`grid_id: str`（第 20 行）、`lat: float`（第 21 行）、`lon: float`（第 22 行）、`population: float`（第 23 行）。
- 关键流程/方法：无自定义方法。
- 输入/输出：由 `aggregate_population_array` 构造（第 90 行）；作为 `PopulationTable.regions` 的元素类型。
- 依赖关系：测试直接构造见 `CODE/leo_sim/tests/test_trace.py:122-124、164-165`。

### `class PopulationTable` — CODE/leo_sim/population.py:27
- 定位：CODE/leo_sim/population.py:27（`@dataclass(frozen=True)` 在第 26 行）
- 职责：不可变记录一次人口栅格聚合的完整结果与来源指纹（FACT：字段定义如此）。
- 关键状态/结构：`regions: tuple[PopulationRegion, ...]`（第 28 行）、`source_path: str`（第 29 行）、`source_sha256: str`（第 30 行）、`source_shape: tuple[int, int]`（第 31 行）、`source_resolution_deg: tuple[float, float]`（第 32 行）、`aggregation_deg: float`（第 33 行）、`total_population: float`（第 34 行）。
- 关键流程/方法：无自定义方法。
- 输入/输出：由 `load_population_regions` 构造返回（第 129–138 行）。
- 依赖关系：测试直接构造见 `CODE/leo_sim/tests/test_trace.py:126、167`。

### `def aggregate_population_array(values, *, west, north, pixel_lon_deg, pixel_lat_deg, aggregation_deg)` — CODE/leo_sim/population.py:37
- 定位：CODE/leo_sim/population.py:37
- 职责：把「自北向南」的二维人口栅格按规范地理网格聚合为 `PopulationRegion` 元组（FACT：docstring 第 46 行与实现一致）。
- 关键流程：
  - 转 float64 数组，必须非空二维（第 47–49 行）；五个标量参数必须有限（第 50–55 行）；像元尺寸与聚合度必须为正（第 56–57 行）。
  - `aggregation_deg` 必须是两个像元尺寸的整数倍（容差 1e-9，第 58–63 行）；且必须能整除 180 与 360（第 64–67 行）。
  - 由宽高与像元尺寸推出 east/south，范围越出地球（±180/±90，容差 1e-9）抛错（第 69–74 行）。
  - 非有限或 ≤0 的像元清零（第 76 行）；逐像元算中心经纬度（`lat = north - (row+0.5)*pixel_lat_deg`，第 79 行；`lon = west + (col+0.5)*pixel_lon_deg`，第 84 行），正人口像元经 `grid.grid_id`（`CODE/leo_sim/grid.py:21`）归入网格累加（第 77–86 行）。
  - 按 grid_id 排序，用 `grid.grid_center`（grid.py:33）取中心构造 `PopulationRegion`（第 87–90 行）；区域数少于 2 抛错（第 91–92 行）。
- 输入：二维 numpy 数组 + 栅格地理参数（仅关键字参数）。输出：`tuple[PopulationRegion, ...]`。
- 依赖关系：调用 `grid.grid_id`、`grid.grid_center`。被本文件 `load_population_regions` 调用（第 122 行）；测试直接调用见 `CODE/leo_sim/tests/test_population.py:18、30`。

### `def load_population_regions(path, aggregation_deg)` — CODE/leo_sim/population.py:96
- 定位：CODE/leo_sim/population.py:96
- 职责：读取一个全球北向 WGS84 GeoTIFF 人口栅格，聚合为 `PopulationTable` 并附来源 SHA-256 等指纹（FACT）。
- 关键流程：路径必须是常规文件且非符号链接（第 98–100 行）；函数内 `from PIL import Image` 打开，任何异常包装为 `PopulationError`（第 101–107 行）；读 GeoTIFF tag 33550（像元尺度）与 33922（tie point），缺失抛错（第 108–112 行）；取 `pixel_lon_deg/pixel_lat_deg/west/north`（第 113–114 行）；强制全球幅面校验：宽 ≈360/pixel_lon、高 ≈180/pixel_lat、west=-180、north=90（容差 1e-6，第 115–121 行）；调 `aggregate_population_array`（第 122–125 行）；总人口必须有限且 >0（第 126–128 行）；构造 `PopulationTable`（第 129–138 行）——其中 `source_path` 保留配置原拼写，第 131–132 行注释说明原因（绝对检出路径会让相同 manifest 跨机器不一致）；`source_sha256` 为文件字节 SHA-256（第 134 行）。
- 输入：GeoTIFF 路径与聚合度。输出：`PopulationTable`。
- 依赖关系：调用 `aggregate_population_array`、PIL.Image。被 `CODE/leo_sim/trace.py:329` 调用（population_gravity 流量模式的 trace 编译路径）；测试佐证 `CODE/leo_sim/tests/test_population.py:38、51`，monkeypatch 见于 `CODE/leo_sim/tests/test_trace.py:130、171`。

---

## 文件 `CODE/leo_sim/__main__.py`（实测 397 行）

模块级说明：
- 模块 docstring（第 1–11 行）列出五条 canonical CLI 用法（config validate / trace compile / run / receipt verify / platform check），并声明「处处 fail closed：未知字段、哈希不匹配、机制缺失、学习依赖不可用均以非零退出码报错」（FACT：docstring 原文；实际子命令共八个，含 docstring 未列出的 experiment compile / acceptance run / compare run，见 `main`）。
- imports（第 12–24 行）：`__future__.annotations`；stdlib `argparse`、`hashlib`、`json`、`sys`、`pathlib.Path`；同包 `acceptance`、`comparison`、`config`、`governance`、`kernel`、`learning`、`platform_check`、`receipt`、`trace`（第 20–24 行，均起 `*_mod` 别名，governance/kernel/learning 除外）。另有两处函数内惰性 import：`tempfile`（第 208 行）、`CODE.experiment_platform.authorize_experiment.verify_authorization_for_leo_sim_v2_config`（第 100–102 行）。
- 无模块级常量；无环境变量读取。

### `def _load(path)` — CODE/leo_sim/__main__.py:27
第 27–28 行：`config_mod.load_config_file(path)` 的薄封装（FACT）。输入配置路径；输出 resolved config dict。被本文件 `_cmd_config_validate`（第 33 行）、`_cmd_trace_compile`（第 59 行）、`_cmd_run`（第 185 行）调用。

### `def _cmd_config_validate(args)` — CODE/leo_sim/__main__.py:31
- 定位：CODE/leo_sim/__main__.py:31
- 职责：实现 `config validate <file.yaml> [--show]` 子命令：加载并严格校验配置，打印状态 JSON（FACT）。
- 关键流程：`ConfigError`/`FileNotFoundError` 时打印 `CONFIG INVALID: ...` 返回 2（第 32–36 行）；成功打印 `{"status": "ok", "version", "sha256"}`（第 37–38 行）；`--show` 时再打印完整 resolved config（第 39–40 行）；返回 0。
- 输入：argparse namespace（`args.file`、`args.show`）。输出：退出码 int。测试佐证 `CODE/leo_sim/tests/test_cli.py:27、33`。

### `def _compile(resolved, out_dir)` — CODE/leo_sim/__main__.py:44
第 44–54 行：调 `trace_mod.compile_trace`，读回 trace.csv 与 manifest.json 字节，把 `__trace_sha256`、`__sha256` 补进 manifest，再按 duration/max_packets `load_trace`，返回 `(manifest, trace_bytes, rows)`（FACT；与 `platform_check._compile_trace` 逻辑相同）。输入 resolved config 与输出目录；输出三元组。被本文件 `_cmd_trace_compile`（第 60 行）与 `_cmd_run`（第 216 行）调用。

### `def _cmd_trace_compile(args)` — CODE/leo_sim/__main__.py:57
- 定位：CODE/leo_sim/__main__.py:57
- 职责：实现 `trace compile --config <yaml> --out <dir>` 子命令（FACT）。
- 关键流程：`_load` + `_compile`；`ConfigError`/`TraceError`/`FileNotFoundError` 打印 `TRACE COMPILE FAILED` 返回 2（第 58–63 行）；成功打印 trace_sha256、manifest_sha256、offered_packets、offered_bits、provenance（第 64–68 行），返回 0。测试佐证 `CODE/leo_sim/tests/test_cli.py:41`（字节级可复现）。

### `def _cmd_experiment_compile(args)` — CODE/leo_sim/__main__.py:72
- 定位：CODE/leo_sim/__main__.py:72
- 职责：实现 `experiment compile --request <json> --out <dir>` 子命令：调 `governance.compile_experiment`，`project_root` 固定为 `Path.cwd()`（FACT，第 74–75 行）。
- 关键流程：`governance.IntentError` 打印 `EXPERIMENT COMPILE FAILED` 返回 2（第 76–78 行）；成功打印 compile-report JSON 返回 0（第 79–80 行）。

### `def _project_root_for(path)` — CODE/leo_sim/__main__.py:83
第 83–87 行：从 `path` 自身向上逐级找同时含 `CODE/leo_sim/` 与 `EXPERIMENTS/` 目录的祖先，作为项目根返回；找不到抛 `governance.IntentError`（FACT）。输入路径；输出 `Path`。仅被本文件 `_verify_formal_args` 调用（第 104 行）。

### `def _verify_formal_args(args, resolved)` — CODE/leo_sim/__main__.py:90
- 定位：CODE/leo_sim/__main__.py:90
- 职责：处理正式运行（formal run）的授权参数：三参数（`--authorization`/`--launch-nonce`/`--expect-run-id`）要么全不给（返回 `None`，非正式运行，第 91–93 行），要么全给（缺一抛 `IntentError`，第 94–96 行）（FACT）。
- 关键流程：`launch_nonce` 必须是 32 位小写十六进制（第 97–99 行）；惰性导入 `verify_authorization_for_leo_sim_v2_config`（第 100–102 行）；解析 config 绝对路径、项目根、授权文件路径并调该函数验证（第 103–107 行）；返回 formal dict：run_id、launch_nonce、authorization_sha256（授权文件字节哈希）、config_sha256、code_sha256（`receipt_mod.code_sha256()`）、results_dir（`<根>/CODE/Results`）（第 108–115 行）。
- 输入：args namespace 与 resolved config。输出：`dict | None`。
- 依赖关系：调用 `_project_root_for`、`CODE/experiment_platform/authorize_experiment.py` 的 `verify_authorization_for_leo_sim_v2_config`、`receipt_mod.code_sha256`。仅被本文件 `_cmd_run` 调用（第 191 行）。

### `def _write_formal_witness(out_dir, formal, receipt_payload)` — CODE/leo_sim/__main__.py:118
- 定位：CODE/leo_sim/__main__.py:118
- 职责：正式运行自然结束后写「证人」文件 `formal_run.json` 并在结果目录的兄弟目录 `_run_receipts/` 下写以 launch_nonce 命名的指针文件（FACT）。
- 关键流程：输出目录 resolve 后必须等于 `<results_dir>/<run_id>`，否则抛错（第 120–123 行）；先自校验回执目录，有错抛错（第 124–127 行）；写 `formal_run.json`：schema `"leo-sim-formal-run/v1"` + formal 除 results_dir 外的字段 + receipt_sha256 + natural_end + conservation_ok（第 128–137 行）；`_run_receipts` 目录是符号链接则抛错（第 138–141 行）；指针文件是符号链接也抛错（第 142–144 行）；写入输出目录绝对路径（第 145 行）。
- 输入：输出目录、formal dict、回执 dict。输出：无返回值，写两个文件。
- 依赖关系：调用 `receipt_mod.verify_receipt_dir`。仅被本文件 `_cmd_run` 调用（第 260 行）。

### `def _load_precompiled(resolved, trace_dir)` — CODE/leo_sim/__main__.py:148
- 定位：CODE/leo_sim/__main__.py:148
- 职责：消费已编译的不可变 trace（docstring 第 149–150 行声明：trace scope 身份与 resolved config 不符即 fail closed）（FACT）。
- 关键流程：`manifest.json`/`trace.csv` 必须都是常规文件且非符号链接（第 151–156 行）；manifest 必须是 JSON object（第 157–162 行）；用 `config.trace_identity_sha256(resolved, manifest["input_sha256"])` 重算期望身份，与 manifest 的 `trace_identity_sha256` 不等即抛 `TraceError`（第 163–169 行）；trace.csv 字节哈希与 manifest `trace_sha256`（若存在）不符抛错（第 170–173 行）；补 `__trace_sha256`/`__sha256` 键（第 174–175 行）；`load_trace` 返回 `(manifest, trace_bytes, rows)`（第 176–180 行）。测试佐证 `CODE/leo_sim/tests/test_cli.py:108`。
- 输入：resolved config 与 trace 目录。输出：三元组。
- 依赖关系：调用 `config.trace_identity_sha256`（经第 163 行函数内 `from . import config as _config`）、`trace_mod.load_trace`。仅被本文件 `_cmd_run` 调用（第 214 行）。

### `def _cmd_run(args)` — CODE/leo_sim/__main__.py:183
- 定位：CODE/leo_sim/__main__.py:183
- 职责：实现 `run --config <yaml> [--out <dir>] [--dry-run] [--expect-trace-sha256 <hex>] [--authorization <f> --launch-nonce <h> --expect-run-id <id>]` 子命令——V2 仿真的主入口（FACT）。
- 关键流程：
  - 加载配置失败打印 `CONFIG INVALID` 返回 2（第 184–188 行）。
  - `_verify_formal_args` 抛任何异常打印 `RUN REFUSED (formal authorization)` 返回 3（第 190–194 行）。
  - 输出目录取 `--out` 或配置 `outputs.out_dir`（第 195 行）；formal 模式下目标已存在且非空/符号链接/非目录则拒绝返回 3（第 196–204 行）。
  - `--dry-run` 且未指定 `--out` 时用 `tempfile.TemporaryDirectory()` 作输出，注释说明 dry-run 不在工作区写运行产物（第 205–210 行）。
  - 配置含 `outputs.trace_path` 时走 `_load_precompiled`，否则 `_compile` 现编译；`TraceError`/`FileNotFoundError` 返回 2（第 211–219 行）。
  - `--expect-trace-sha256` 与实际不符返回 2（第 220–224 行）。
  - 组装 plan dict（第 225–241 行）：config_sha256、trace_sha256、code_sha256、offered_packets/bits、active_endpoints、horizon_s、三项执行上限（max_events/max_entities/max_packets）、机制五元组（routing policy、access association、control_plane enabled、ge_enabled、learning algorithm）。
  - `--dry-run`：打印 `{"status": "DRY RUN", **plan}` 返回 0，不跑仿真（第 242–244 行）。
  - `kernel.run_simulation`（learning 算法为 ddqn 时传 `learning_out_dir=<out>/ddqn`）（第 245–250 行）；`learning.LearningUnavailable` 返回 3、`kernel.CapExceeded` 返回 4（第 251–256 行）。
  - `receipt_mod.write_run` 写回执（第 257 行）；formal 且 natural_end 时 `_write_formal_witness`，失败返回 6（第 258–263 行）。
  - 打印结果 JSON（status ok/interrupted + plan + natural_end + fate_counts + conservation_ok），natural_end 返回 0，否则返回 5（第 264–269 行）。
- 输入：args namespace。输出：退出码 int（0/2/3/4/5/6）。
- 依赖关系：本文件内调 `_load`、`_verify_formal_args`、`_load_precompiled`、`_compile`、`_write_formal_witness`；跨模块调 `kernel.run_simulation`、`receipt_mod.write_run`/`code_sha256`、`trace_mod` 编译/加载。被 `main` 经 `set_defaults` 绑定（第 348 行）；测试佐证 `CODE/leo_sim/tests/test_cli.py:52、60、83、98、108`。VM 上由 `CODE/scripts/remote/remote_job.py:250` 以 `python -m CODE.leo_sim run --config ... --authorization ...` 形式发起（另见 `CODE/tests/test_remote_workspace_scripts.py:261` 的命令前缀断言）。

### `def _cmd_receipt_verify(args)` — CODE/leo_sim/__main__.py:272
第 272–278 行：实现 `receipt verify <dir>`：调 `receipt_mod.verify_receipt_dir`，有错误打印 `FAILED` + 错误列表返回 2，否则打印 `verified` 返回 0（FACT）。测试佐证 `CODE/leo_sim/tests/test_cli.py:60、70`（篡改后校验失败）。

### `def _cmd_acceptance_run(args)` — CODE/leo_sim/__main__.py:281
第 281–288 行：实现 `acceptance run --out <dir>`：调 `acceptance_mod.run_acceptance`；`AcceptanceError` 打印 `ACCEPTANCE REFUSED` 返回 2；成功打印 summary，PASS 返回 0 否则返回 7（FACT）。

### `def _cmd_compare_run(args)` — CODE/leo_sim/__main__.py:291
第 291–298 行：实现 `compare run [--config <yaml>] --out <dir>`：调 `comparison_mod.run_comparison`；`ComparisonError` 打印 `COMPARISON FAILED` 返回 8；成功打印 summary，PASS 返回 0 否则返回 8（FACT：失败与拒跑同为 8）。

### `def _cmd_platform_check(args)` — CODE/leo_sim/__main__.py:301
第 301–311 行：实现 `platform check --out <dir> [--comparison-config ...] [--ddqn-config ...] [--population-config ...]`：调 `platform_check_mod.run_platform_check` 并透传三个配置路径；`PlatformCheckError` 打印 `PLATFORM CHECK REFUSED` 返回 9；成功打印 summary，PASS 返回 0 否则返回 9（FACT）。

### `def main(argv=None)` — CODE/leo_sim/__main__.py:314
- 定位：CODE/leo_sim/__main__.py:314
- 职责：argparse 入口，注册全部子命令并分发到各 `_cmd_*` 处理器，外加两层兜底异常网（FACT）。
- 关键流程：prog 名 `"python -m CODE.leo_sim"`（第 315 行）；子命令树（第 318–379 行）：`config validate`（位置参数 file + `--show`）、`trace compile`（`--config`/`--out` 必填）、`experiment compile`（`--request`/`--out` 必填）、`run`（参数见 `_cmd_run`，第 339–348 行）、`receipt verify`（位置参数 dir）、`acceptance run`（`--out` 必填）、`compare run`（`--config` 默认 `profiles/comparison.yaml`、`--out` 必填）、`platform check`（`--out` 必填，三个配置默认值分别指向 `profiles/comparison.yaml`、`profiles/acceptance/ddqn.yaml`、`profiles/population_gravity.yaml`，第 369–379 行）。分发（第 381–383 行）；兜底一：`ConfigError`/`TraceError` 打印 `FAILED` 返回 2（第 384–388 行，注释称其为各处理器遗漏路径的 fail-closed 网）；兜底二：`ValueError`/`TypeError`/`KeyError`/`OSError`/`JSONDecodeError` 打印 `FAILED (fail closed)` 返回 2（第 389–393 行，注释称公共入口不得暴露裸 traceback）。
- 输入：可选 argv 列表。输出：退出码 int。
- 第 396–397 行：`if __name__ == "__main__": sys.exit(main())`。
- 依赖关系：分发到本文件全部 `_cmd_*`。调用方：命令行 `python -m CODE.leo_sim`（文档 `CODE/README.md:10` 示例为 `platform check`；VM 正式路径 `CODE/scripts/remote/remote_job.py:250`）；测试中直接 `main([...])` 见 `CODE/leo_sim/tests/test_cli.py` 多处与 `CODE/leo_sim/tests/test_review_round4.py:20`（import main）。

---

## 文件 `CODE/leo_sim/__init__.py`（实测 11 行）

模块级说明：
- 包 docstring（第 1–9 行）：声明 `leo_sim` 是「formal LEO simulation platform V2 runtime」，并给出正式数据路径：不可变需求 trace → 稀疏地理 TrafficEndpoint → 有限卫星接入服务 → 卫星 ingress → ISL 路由 → 本地目的可见性发现 → 有限下行 → 目的 TrafficEndpoint；末行声明「旧 runtime 的 Gateway 概念在本包中不存在」（FACT：docstring 原文；其中 Gateway 概念缺席这一点与本片段范围一致——`comparison.py` 的 Gateway 相关代码全部位于对旧运行时的进程外调用侧）。
- 唯一语句：`__version__ = "2.0.0"`（第 11 行，FACT）。
- 无 imports、无常量、无环境变量读取、无符号定义。
- 依赖关系：作为包初始化文件被所有 `CODE.leo_sim.*` / `leo_sim.*` 导入间接触发；`__version__` 的直接读取方在 CODE/ 下未确认（grep 未见引用）。
