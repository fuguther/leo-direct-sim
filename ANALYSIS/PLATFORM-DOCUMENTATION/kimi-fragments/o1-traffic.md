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
