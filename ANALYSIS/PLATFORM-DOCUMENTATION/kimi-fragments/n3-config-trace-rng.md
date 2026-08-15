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
