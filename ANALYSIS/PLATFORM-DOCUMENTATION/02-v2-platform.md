# 新平台说明书（leo_sim）

> 本卷由主脑 Codex 独立通读产出。新平台是模块化内核，入口 `python -m leo_sim`。
> 只陈述代码事实，标注 `文件:行号`，不做优劣判断。

## 0. 阅读范围与统计

模块化内核 `CODE/leo_sim/`（不含 tests）共 7116 行，16 个模块：

| 模块 | 行数 | 职责 |
|---|---:|---|
| config.py | 630 | 版本化 YAML 配置 + SHA |
| trace.py | 522 | 不可变需求 trace 编译器 + manifest |
| model.py | 294 | Walker-delta 星座几何 |
| grid.py / population.py | 87 / 139 | 网格 ID / GPW 人口聚合 |
| kernel.py | 1678 | 有界 SimPy 离散事件内核 |
| control.py | 109 | 控制平面 / 本地缓存 |
| outage.py | 77 | 几何失效 + Gilbert-Elliott |
| fates.py | 188 | 数据/控制双账本守恒 |
| routing.py | 226 | hop/delay/capacity/oracle 路由 |
| learning.py | 825 | C1/C3-C7 合同 + Double-DQN |
| receipt.py | 941 | 回执 + fail-closed 验证 |
| governance.py / acceptance.py / comparison.py / platform_check.py | 257/153/271/270 | 治理链/验收/双臂对照/平台检查 |
| __main__.py / rng.py | 397/41 | CLI / RNG stream |

## 1. config.py — 版本化配置（630 行）

- `SCHEMA`（`:53`）：顶层 10 组严格字段白名单 `scenario/endpoints/demand/access/
  links/control_plane/routing/learning/execution/outputs`，每组只允许声明字段，未知字段
  一律 fail-closed。
- 解析优先级：内置默认 → 命名 profile → 用户文件 → 显式覆盖，产出唯一 canonical
  object + SHA256 身份。
- `_UniqueKeyLoader`（`:24`）：拒绝 YAML 重复键。
- 关键物理/运行边界校验（`:396-522` 附近）：LEO 海拔、倾角、seed 非负、站点名/权重、
  网格度整除、`reward=="queue"`（distance/linear 直接 `ConfigError`）、NaN/Inf 拒绝。
- FACT：无环境变量桥（旧平台依赖大量 `SIM_*`，这里明确没有）。

## 2. trace.py — 不可变 trace 编译器（522 行）

- `validate_packet_rows`（`:46`）：行合同三关口——NaN/负 bits、重复 ID、超 horizon、
  非法 deadline/grid、非排序、超 max_packets 一律拒。
- `compile_trace`（`:221`）：生成 `trace.csv`（packet_id, emit_time_s, src_grid_id,
  dst_grid_id, bits, deadline_at_s）+ `manifest.json`（schema/config/input 哈希、RNG
  stream、offered bits、活跃端点、时间范围）。
- `load_trace`（`:482`）：加载 + 按 resolved horizon/max_packets 重验。
- FACT：编译与仿真消费完全分离；相同 config+input+seed 字节可复现。

## 3. grid.py + population.py — 网格与人口（87/139 行）

- `grid.py`：规范网格 ID（默认 0.25°，聚合默认 1°），`grid_center` 给单元中心经纬度。
- `population.py`：读 GPW 2020 TIFF，负值/NoData 归零，按 `population^beta` 聚合为
  `TrafficEndpoint` 候选源区；manifest 绑定 TIFF SHA + 有效人口 + 参数。

## 4. model.py — Walker-delta 几何（294 行）

- `propagation_delay_s`（`:16`）：距离/光速。
- `_sph_to_ecef`（`:20`）：球坐标→ECEF。
- `GeometryCertificationError` + `_next_change_adaptive`（`:49/:56`）：**几何变化认证**，
  二分定位 (t0,t1] 内的可见性/距离变化点，None 只表示「证无变化」，非有限/退化一律 raise。
- `class Constellation`（`:156`）：num_satellites/num_planes/altitude/inclination。
  方法 `subpoint/ecef/positions/elevation_deg/ground_visible/slant_range_km/isl_range_km/
  neighbors/gsl_available/isl_available/next_gsl_change/next_isl_change`。
  FACT：位置是 t 的纯函数，内核只在当前仿真时刻查询，**从不读未来星历**。

## 5. kernel.py — 内核（1678 行）

### 实体
- `DataPacket`（`:65`）：`pid/src/dst/bits/deadline/emitted_at/path/assigned_sat/
  learning_state/learning_action/learning_reward`。
- `QueueArea`（`:84`）：精确 queued-bits×seconds 积分（守恒/排队面积结算用）。
- `ControlPacket`（`:111`）：真实控制包 `iid/origin/seq/generated_at/ttl_s/remaining_hops/
  payload_bits`；`received_at` 一次性赋值（`:159`）、`valid_at(t)`（`:168` TTL 窗口）、
  `aoi(t)`（`:171` = t-generated_at）。
- `Link`（`:178`）：端点↔卫星关联，`acquiring/active/retiring` 三态 + `retire_at` 硬退休。
- `TrafficEndpoint`（`:199`）：地面端点 `cell/lat/lon/queue/queued_bits/links/area`。
- `_DRRMixin`（`:220`）：deficit round-robin 公平调度（`_drr_select`，bit 级公平，
  超大包不会死锁）。
- `UplinkServer`/`DownlinkServer`/`ISLLink`（`:255/343/439`）：上行/下行/ISL 服务器，
  各带有限队列与非抢占优先。

### 数据路径（Kernel 类，`:586`）
- `_emitter`（`:902`）：端点发射数据包。
- `_transmit`（`:784`）：**传输中断竞态核心**——把「服务完成 vs 几何失效 vs GE 中断
  vs deadline vs（GSL）硬退休」做单点竞态。返回 `ok`（全程链路 up）/`retired`（硬退休，
  无 fate、重排队）/`stalled`（horizon 前链路未恢复，无 fate，结算 IN_SYSTEM_AT_STOP）/
  否则包得唯一 fate。链路在服务开始前 down 只**延迟开始**（非 pause/resume）；中断时
  `self.occupied[occ_key]` 记账已占用服务时间。
- `_candidates`/`_try_grant`/`_request_or_grant`/`_access_tick_*`（`:987-1070`）：接入
  请求/授权——K 槽 + DRR 公平 + 租期轮转 + 空闲释放。
- `_associate`（`:1197`）：关联（`acquisition_delay_s` 建链时延）。
- `_evaluate_handover`（`:1251`）：切换——同星保留 + 仰角迟滞 `hysteresis_deg` + 最短驻留
  `min_dwell_s`；MBB（`association=="mbb"` + `dual_connect` + 未超 retiring 上限）旧链
  retiring 排空 + 硬退休 `retirement_deadline_s`；否则 BBM（不抢占在服务包）。
- `_control_advertiser`/`_advertise`/`_ctrl_arrive_after_prop`（`:1091-1135`）：控制面，
  真实控制包逐跳传播、占带宽、TTL/AoI。
- `_decide`（`:1389`）：路由决策——`deliver`（当前星可见目的端且下行可服务）或选 ISL。
- `_ingress_after_prop`/`_isl_arrive_after_prop`/`_deliver_after_prop`（`:1465-1498`）：
  上行/ISL 转发/下行送达。
- `_fail`（`:1498`）：写 fate（`DATA_DEADLINE_EXPIRED`/`NO_ROUTE`/几何失效等）。
- `run`（`:1512`）：主事件循环，产出 result。

接入调度细节：`_candidates`（`:987`）需求感知——先「已持有该端点下行流量的卫星」再
「其他可见卫星」，都按仰角排，只用当前几何；`_try_grant`（`:999`）有空槽即 associate；
`_request_or_grant`（`:1016`）无空槽则进最佳候选的 FIFO 等待队列（确定性）；
`_access_tick_endpoint`（`:1030`）做租期轮转（`slot_lease_s` 到期 graceful retire）、
空闲释放（`idle_release_s`，无 waiter 时 keep-stable 优先）、需求请求或空槽
preposition；`_access_tick_sat`（`:1070`）把释放槽按 FIFO 顺序 grant 给等待端点。

### 学习奖励（`_learning_action`，`:1373-1386`）

FACT，新平台奖励只有两条：
```python
if action == "deliver": reward = 1.0
else: reward = exp(-(data_bits + ctrl_bits)/isl_queue_bits)   # (0,1]
```
无距离奖励、无 again/unav 惩罚、无 arrive 高奖励（对照旧平台第 9 节的整套奖励）。

## 6. control.py — 控制平面（109 行）

- `CacheEntry`（`:14`）：`origin/payload/generated_at/received_at/ttl_s/hops`，`valid_at`/
  `aoi`。
- `LocalCache`（`:57`）：每星本地缓存，只存实际到达且未过期的条目，`valid_entries`/
  `count_expired`。FACT：这是所有学习算法唯一的远程信息源，无全局状态。
- `build_snapshot`（`:86`）：构造控制快照 payload。

## 7. outage.py — 中断（77 行）

- `geometry_loss`（`:24`）：确定性几何失效（两端不可见即断，不用 RNG）。
- `class GilbertElliott`（`:29`）：GSL/ISL 独立 GE 两状态中断，`mean_good_s/mean_bad_s`，
  `is_down/next_down/next_up`，私有 RNG 可复现。FACT：几何失效与随机中断分离。

## 8. fates.py — 双账本守恒（188 行）

- `DataFateLedger`（`:38`）：每数据包唯一终态（register→record 一次性），
  `check_conservation`（`:83`）校验 `offered = delivered + terminal_loss + in_system`。
- `ControlFateLedger`（`:99`）：控制包单独账本（DELIVERED/EXPIRED/QUEUE_OVERFLOW/DUPLICATE），
  不进数据位守恒方程。

## 9. routing.py — 路由（226 行）

- `build_topology`（`:63`）：由几何 `neighbors(s,dirs)` 建静态有向邻居图，双向性
  fail-closed（拒绝虚构反向边）。
- `control_broadcast_children`（`:31`）：确定性最短路广播树。
- `choose_next_hop`（`:126`）：`hop/delay/capacity/oracle` 四策略；deliver 只用当前星
  直接可见目的端；oracle 显式标注「分析上界」可用全局。

## 10. learning.py — 学习合同（825 行）

- 合同维度（`:45-62`）：C1/C3/C4/C5/C6/C7 各自固定状态维；C1 只看一跳已到达，
  C3–C7 共享同一 `vis_k` 缓存，差别只在表示/聚合与 AoI 处理。
- `V2GraphEncoder`（`:102`）：模块级可序列化 Keras 层（GAT/MPNN），`get_config/from_config`。
- `TensorflowDDQN`（`:276`）：canonical Double-DQN（online argmax + target eval + next
  mask + terminal mask），`choose/remember/_train_once/_build_fast_train_fn/save_and_verify`。
- `build_observation`/`information_set`/`build_action_mask`（`:593-794`）：观测/信息集/
  动作掩码，`deliver` 合法仅当本地可见目的端且下行可服务。

## 11. receipt.py — 回执（941 行）

- `build_receipt`（`:294`）：组装 receipt（resolved config/trace/代码/输入 SHA、ledgers、
  机制生效、deps）。
- `_validate_ledgers`/`verify_receipt_dir`（`:374/585`）：fail-closed 验证，逐字段篡改即拒。
  `_validate_ledgers` 校验：`LEDGER_KEYS` 精确键集、`field_authority` 分级、learning 账本
  （decisions/transitions/train_steps/replay_size 非负整数、checkpoint SHA 与实际文件 SHA
  一致、eval 模式 train_steps==0）、`stop_time_s`（natural_end 时 == horizon）、
  `packet_fates` 格式、`deliveries` == DELIVERED 集合精确一致。信任模型明确：只证
  「内部一致性」，无外部锚点。

## 12. 治理/验收/对照/检查

- `governance.py`（257 行）：`build_run_intent`/`compile_experiment`，绑定 config SHA、
  trace 身份、代码 SHA、授权 SHA、launch nonce，不接受 shell 命令、不回退旧 Gateway。
- `acceptance.py`（153 行）：面向结果的机制验收 runner（五类机制场景，机制确实在
  ledger 中观察到才算过）。
- `comparison.py`（271 行）：同 trace 双臂对照（leo_sim 直连 vs 旧 SimulationRL Gateway），
  显式对齐物理时间倍率/Walker/壳层/拓扑步长/seed。
- `platform_check.py`（270 行）：`platform check` 端到端收口（五类机制 + 双臂 + TF DDQN
  train/eval），任一步失败即停并写 `platform-summary.json`。

治理/验收细节：`build_run_intent`（governance `:57`）要求 `runtime_kind` 严格等于
`leo_sim_v2`（旧 Gateway runtime 永不隐式回退），拒绝未知字段，绑定 `config_sha256/
input_sha256/trace_identity_sha256/code_sha256`，csv 输入必须落在 project_root 内。
`acceptance.py` 的 `SCENARIOS = ("direct","k1","bbm","mbb","ge")`（`:19`）——每个场景
`_case_checks` 必须观察到对应机制（如 bbm 要 `bbm_switch_observed`、mbb 要
`mbb_effective_receipt`、ge 要 `RANDOM_OUTAGE_IN_FLIGHT` 计数），「仅到 horizon 不算过」。

## 13. __main__.py + rng.py（397/41 行）

- `__main__.py`：CLI `config validate / trace compile / run --dry-run / run / receipt
  verify`，`python -m leo_sim` 入口。
- `rng.py`：派生 RNG stream，保证可复现随机流。

## 新平台第二卷 · 完成度

- 已覆盖：全部 16 模块的职责、关键类/方法、数据路径、机制。
- 未逐行展开但已定位：`kernel.py` 的 `_transmit`/`_sweep_*` 内部细节、`receipt.py` 的
  逐字段校验实现、`__main__.py` 的 CLI 解析细节（已按职责概述）。
