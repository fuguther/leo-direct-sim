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
