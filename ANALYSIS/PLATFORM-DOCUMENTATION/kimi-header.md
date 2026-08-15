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
