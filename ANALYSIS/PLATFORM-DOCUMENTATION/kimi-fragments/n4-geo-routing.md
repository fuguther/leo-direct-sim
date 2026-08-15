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
