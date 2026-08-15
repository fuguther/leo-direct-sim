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
