# LEO 仿真平台 V2 本地实现报告（2026-08-13，四轮审查修复后修订版）

> 本版取代文末附录中的初版报告。初版"本地实现完成（89 tests）"结论已被第一轮 Codex 独立反例审查否决，其后经第二轮（20 项）、第三轮（4 类）Codex 独立探针审查与第四轮 Codex 验收审查（7 组冻结缺陷）修复。各轮权威记录分别见：
> - `PLATFORM-V2-REMEDIATION-20260813.md`（第一轮：10 探针否决与修复）
> - `PLATFORM-V2-REMEDIATION-ROUND2-20260813.md`（第二轮：20 项）
> - `PLATFORM-V2-REMEDIATION-ROUND3-20260813.md`（第三轮：4 类）
> - 第四轮：7 组缺陷的红→绿证据见本报告 §4b（按指令不单独建 ROUND4 文件）
>
> **来源口径（准确）**：第一~四轮均为 Codex 运行的独立探针/验收审查；冻结计划的正式三角色审阅链（cold-start / satellite-DRL / adversarial review）**至今未执行**，仍是 EXTERNAL_GATE。本报告只描述**当前代码的真实状态**；凡与附录初版冲突处，以本版与三份 REMEDIATION 报告为准。附录原文保留为历史声明，不作状态依据。

- 冻结计划书：`/private/tmp/m2-leo-platform-v2-runs/20260812T163928Z-22ae650a/task.json`（SHA-256 `8367990338e92953f08df186078abe7c56accf86535100b770b59bb1805a0ae9`，2026-08-13 核验一致）。
- 实施位置：隔离工作树 `/private/tmp/m2-leo-platform-v2-runs/20260812T163928Z-22ae650a/worktree`，base commit `4fe918f`。**全部改动未提交**（约束禁止 commit/push/deploy/SSH）。
- 口径：FACT = 有第一手命令证据；INFERENCE = 由证据推导；UNVERIFIED / EXTERNAL_GATE = 本地无法验证或需外部授权。
- 状态：**CODEX_LOCAL_ACCEPTANCE_CANDIDATE**（Codex 已复测并直接修复第四轮后发现的 6 组封口缺陷；尚未提交、三角色审阅或上 VM，不得引本报告声称 VERIFIED_VM 或任何算法效果）。

## 1. task.json 验收矩阵（逐项判定）

| # | 验收标准（摘要） | 判定 | 证据位置 |
|---|---|---|---|
| 1 | `CODE/leo_sim` 模块化、真实本地路径无 Gateway 依赖、有界 endpoint→satellite→endpoint 交付 | DONE_WITH_EVIDENCE | 包内无 Gateway import（仅 docstring/测试提及）；`test_kernel.py::test_direct_uplink_downlink_delivery`、`test_isl_forwarding_delivery`；Walker smoke（§2） |
| 2 | 严格 CLI、schema/config resolver、确定性 trace 编译器、manifest/hash/provenance 经公开接口工作 | DONE_WITH_EVIDENCE | §2 验证命令；`test_config.py`/`test_trace.py`/`test_cli.py` |
| 3 | 有限接入与 ISL 资源、BBM/MBB、GSL/ISL 中断分离、真实带宽消耗控制包、本地 stale cache、fate 唯一与 bit 守恒 | DONE_WITH_EVIDENCE | §4 机制→测试映射 |
| 4 | 非学习路由可执行；C1/C3/C4/C5/C6/C7 与 canonical Double-DQN 有显式共享信息/动作合同；无真实 TF 时 fail closed | DONE_WITH_EVIDENCE | `test_routing.py`（7 项）、`test_learning.py`（12 项，含 `test_learning_run_fails_closed_unconditionally`） |
| 5 | 新确定性测试覆盖全部要求机制并通过；旧治理与回归套件除 4 项预登记环境例外与合法 TF 跳过外通过 | DONE_WITH_EVIDENCE | §2：266 passed；337 passed / 17 skipped / 4 deselected |
| 6 | 旧 Gateway 代码保持不动（仅允许回归覆盖的最小非破坏集成点）；不删除任何旧路径或证据 | DONE_WITH_EVIDENCE | `git diff --stat`：仅 `NOTES.md`(+7 行）为既有文件改动，其余全部为新增未跟踪文件；未做任何删除 |
| 7 | 本地实现报告、清理候选报告、NOTES 准确区分 FACT/INFERENCE/UNVERIFIED，不声称 VM 验收或算法效果 | 本版即为此项修订 | 本报告、`PLATFORM-V2-CLEANUP-CANDIDATES-20260813.md`、`NOTES.md` |
| 8 | compileall、CLI validate/dry-run、pytest、git diff 按声明命令通过 | DONE_WITH_EVIDENCE | §2 全部按 task.json verify 原文执行 |

## 2. 验证命令与真实计数（FACT，2026-08-13 最终电池）

解释器为 task.json verify 指定的 `/private/tmp/m2-leo-platform-v2-verify/bin/python`（Python 3.12.12 / NumPy 2.4.6 / SimPy 4.1.2 / PyYAML 6.0.3 / pytest 9.1.1，无 TensorFlow）；工作目录为工作树根：

| 命令（task.json verify 原文） | 真实结果（2026-08-13 第四轮修复后） |
|---|---|
| `pytest -B -q -p no:cacheprovider CODE/leo_sim/tests` | **266 passed / 0 failed / 0 skipped** |
| `pytest -B -q -p no:cacheprovider CODE/tests CODE/experiment_platform/tests CODE/work/tests -k "not test_read_cgroup_used_gb and not test_output_dim_and_apply_shape and not test_self_supervised_training_reduces_loss and not test_save_load_roundtrip"` | **337 passed / 17 skipped / 4 deselected / 21 subtests passed** |
| `python -B -m compileall -q CODE/leo_sim` | 通过，无输出 |
| `python -B -m CODE.leo_sim config validate CODE/leo_sim/profiles/smoke.yaml` | 退出码 0；输出 `status=ok`、`version=leo-sim-config/v1`、config sha256 `08a5c8d9…` |
| `python -B -m CODE.leo_sim run --config CODE/leo_sim/profiles/smoke.yaml --dry-run` | 退出码 0；输出 config/trace/code 三个 SHA、caps 与机制清单；不写任何运行产物 |
| `git diff --check` | 通过，无输出 |

VM 同版本栈复跑（`/private/tmp/leo-v2-vm-compat`：Python 3.11.14 / NumPy 1.24.3 / SimPy 4.0.1 / PyYAML 6.0.2，与 VM 一致）：leo_sim **266 passed / 0 failed**（1 个 warning 为 SimPy 4.0.1 的 pkg_resources 弃用提示，环境固有）。

补充端到端证据（verify 解释器，第四轮修复后）：

| 证据 | 真实结果 |
|---|---|
| 真实 Walker 星座 smoke（12 星 3 面）：`run --config …/smoke.yaml --out /private/tmp/leo-v2-r4-smoke/out`（第四轮修复后重跑） | `natural_end=true`、`fate_counts.DELIVERED=1`、其余 fate 全 0、`conservation_ok=true`；产物 5 件（trace.csv/manifest.json/resolved_config.json/ledgers.json/receipt.json） |
| `receipt verify /private/tmp/leo-v2-r4-smoke/out` | `{"status": "verified"}`，退出码 0 |
| 篡改负例：改 `receipt.json` 的 fate_counts 后 verify | 退出码 2，错误 `recomputed fate_counts != receipt fate_counts` |
| CLI `trace compile` 直调（第四轮后） | 两次字节一致；trace SHA `47a4af9f…` 与 dry-run 跨命令一致 |
| 第二轮独立探针 `PYTHONPATH=. … /private/tmp/leo_v2_review_round2.py`（第四轮后复跑） | 退出码 0，全部检查通过 |
| 第三轮独立探针 `PYTHONPATH=.:CODE /tmp/leo-test-env/bin/python /tmp/leo_v2_round3_probe.py`（第四轮后复跑） | 退出码 0；基线 receipt 核验 `[]`；伪造 stop_time/deliveries/queue_area/access 后 5 条错误全部命中 |

跳过/排除说明：4 个 deselected 是任务书预登记的本地环境限制（`test_read_cgroup_used_gb` 与 3 个 temporal_gru 需 TensorFlow），为基线证据而非本次缺陷；17 个 skipped 为旧测试自身条件跳过，与本次改动无关；leo_sim 219 项中 0 skipped。

## 3. 交付物与架构（FACT）

新增 `CODE/leo_sim/`（全新文件；既有文件仅 `NOTES.md` 追加状态条目）：

| 模块 | 职责 |
|---|---|
| `config.py` | 版本化 YAML schema（十顶层组：scenario/endpoints/demand/access/links/control_plane/routing/learning/execution/outputs）；未知字段、非法组合、NaN/±Inf、非法物理量（LEO 海拔 [300,2000] km、倾角 [0,180]、seed 非负整数、站点名/权重、网格度整除关系、learning 数值域）全部在 `resolve_config` 阶段 ConfigError fail closed；站点 lat/lon/weight 非法类型（字符串/bool/None）与 YAML 语法错误同样受控拒绝（第四轮）；defaults→profile→user 解析为 canonical JSON + SHA256；独立的 `trace_identity_sha256`（只含需求生成相关字段，路由/接入/链路/控制/学习参数不改变 trace 身份，保证公平 A/B 同 trace） |
| `grid.py` | 0.25° 规范网格 ID、默认 1° 聚合、稀疏激活；同一物理单元只接受唯一规范拼写，别名 fail closed |
| `trace.py` | 不可变 trace 编译器（uniform/gravity/hotspot/burst/diurnal/csv/mlab）；manifest 含 schema 版本、trace 身份 SHA、输入文件 SHA、RNG 流映射、offered 账本、活跃端点数、时间范围；mlab 复用仓库数据 `CODE/data/traffic/mlab_2026-05-27.csv`，权重键使用 resolved config 的 grid_deg/aggregation_deg，无活跃 OD 覆盖即 TraceError fail closed（无 1e-9 平滑回退），强制 `measurement_proxy` 标记；CSV 字段级解析全部 TraceError 化；实际写盘前按相同规范时间字符串验证，保证成功编译的 trace 可被 load/kernel 接受；`validate_packet_rows` 单一行合同在编译出口、预编译加载、receipt、内核入口共用 |
| `rng.py` | SeedSequence 分派独立命名随机流（demand/ge_gsl/ge_isl/association/routing/control/monitor）；GE 链路流由 run seed + 稳定链路身份派生，与对象创建顺序无关 |
| `model.py` | Walker-delta 几何（位置/仰角/斜距/ISL 邻居，纯时间函数，无未来星历接口）；认证式几何变化检测 `_next_change_adaptive`（速率界步进 + 二分，区间终点 t1 显式求值，跨越恰在 t1 不再漏报），`None` 只表示已证无变化，迭代耗尽/非有限/退化零 margin 一律 `GeometryCertificationError`；速率界覆盖整个配置域（仰角界 2.0°/s：300 km 天顶推导上界 ≈1.57°/s、稠密扫描实测 ≈1.42°/s；斜距界 20 km/s），推导写入注释；该接口只服务事件调度器，不是路由/学习的信息信道 |
| `outage.py` | 几何失效（确定性）与 Gilbert-Elliott 随机中断（连续时间两状态，默认关闭，GSL/ISL 独立流，状态与查询模式无关） |
| `control.py` | 本地缓存（freshest-only、TTL/AoI、跳数记录、去重）；CacheEntry 时间合同：全有限时间、ttl>0、received_at ≥ generated_at 否则 ValueError；有效性 = generated_at ≤ received_at ≤ now ≤ generated_at + ttl（未来到达不是信息），缓存/路由/学习合同共用此规则 |
| `kernel.py` | SimPy 有界内核：TrafficEndpoint、每星 K 接入槽、需求驱动公平关联（FIFO 等待队列 + slot_lease 轮转 + 空闲释放 + 无竞争预置）、有限上下行队列、共享 GSL DRR 公平调度、方向性有限 ISL（控制非抢占优先）、keep-stable/hysteresis_deg/min_dwell/acquisition_delay、BBM 默认、能力门控 MBB 硬退休、deadline、fate/控制双账本、事件/实体/包三上限、精确 horizon 结算、monitor 开关；ControlPacket 全合同（origin/seq/generated_at/received_at/ttl_s/remaining_hops/payload_bits/payload + valid_at + aoi），`bits` 仅为只读兼容别名，接收时刻经校验后只允许在真实到达路径设置一次；控制包几何中断产生独立 GEOMETRY_LOSS_IN_FLIGHT fate |
| `routing.py` | hop/propagation-delay/available-capacity 最短路 + oracle（标 `analysis_upper_bound`）；可达性与下一跳只按真实有向边计算（反向邻接多源 Dijkstra），物理双向性在拓扑构造时验证 fail closed，不再静默补边；目的发现只读本地已到达未过期缓存；deliver 仅在目的端当前关联且下行资源合法时可用 |
| `learning.py` | C1/C3-C7 观测合同（同一信息集，仅表示/聚合/AoI 处理不同）、动作掩码、canonical Double-DQN target（online argmax + target evaluation + next-action mask + terminal bootstrap mask,numpy）；无真实 TF 一律 `LearningUnavailable` fail closed |
| `fates.py` | 数据 fate 唯一账本 + 控制独立账本（几何损失与随机中断分列；到达 fate 强制携带接收时刻）+ bit 守恒校验 |
| `receipt.py` | receipt v3：ledgers.json 结构化账本；verify 全量重算 + LEDGER_KEYS 精确键集 + 防御式类型/关系校验；复用统一 trace 解析/验证，重复 ID、非规范 grid、排序、数值域及 manifest 的 offered 数/bit/时间范围/ledger 失配均拒绝；畸形 packet fate 与任一 ledger 顶层错误类型只返回错误列表，不发生二次崩溃；信任模型如实标注为"内部一致性"，外部锚点留给治理链 |
| `governance.py` | 治理链本地集成面：`build_run_intent` 密封 runtime_kind=config SHA+trace 身份 SHA+code SHA；非 `leo_sim_v2` 一律 IntentError fail closed；不接受 shell 命令 |
| `__main__.py` | CLI：`config validate` / `trace compile` / `run [--dry-run] [--expect-trace-sha256]` / `receipt verify`；`run` 可消费预编译不可变 trace 并核验调用方期望 SHA；main() 兜底网：任何泄露的 ValueError/TypeError/KeyError/JSONDecodeError 受控为非零退出，永不打印 traceback |
| `profiles/smoke.yaml` | 12 星 3 面真实 Walker 星座 smoke |
| `tests/`（17 个测试文件 + helpers，266 测试） | 见 §4 与 §4b |

## 4. 机制 → 行为测试映射（FACT）

| 冻结计划要求 | 永久测试（节选） |
|---|---|
| 直连上行—ISL—下行交付 | `test_direct_uplink_downlink_delivery`、`test_isl_forwarding_delivery`、`test_smoke_profile_real_constellation_delivers` |
| 有限队列拒绝/溢出 | `test_access_rejected_when_no_visible_satellite`、`test_access_queue_overflow`、`test_isl_queue_overflow`、`test_access_slot_admission_limit` |
| 公平调度 | `test_uplink_fair_scheduling_alternates`、`test_drr_bit_fairness_with_mixed_packet_sizes`；K=1 公平关联见 `test_review_round2.py` |
| BBM | `test_bbm_switches_on_better_elevation`、`test_hysteresis_blocks_switch`、`test_min_dwell_blocks_voluntary_switch`、`test_forced_switch_on_geometry_loss_despite_dwell`、`test_acquisition_delay_queues_without_rejection` |
| 能力门控 MBB + 硬退休 | `test_mbb_drains_old_link_without_loss`、`test_mbb_retirement_deadline_reassigns_leftover`、`test_mbb_requires_dual_connect_fail_closed` + round2 在传包与退休期限竞争测试 |
| GSL/ISL 中断分离 | `test_geometry_loss_flag`、`test_random_outage_in_flight`、`test_geometry_loss_in_flight_accounts_occupied_time`、`test_ge_disabled_by_default_and_never_down`、`test_ge_deterministic_and_eventually_down`、`test_ge_state_is_query_pattern_independent`、`test_ge_link_streams_order_independent` |
| 中途失效记账 | `test_geometry_loss_in_flight_accounts_occupied_time` + round2 窄中断（0.1 ms）检测回归 |
| 控制带宽竞争/非抢占优先 | `test_control_nonpreemptive_priority_and_bandwidth`、`test_control_ledger_accounts_bits` |
| vis_k/TTL/AoI/stale cache | `test_advertisement_reaches_two_hops_with_vis_k_2`、`test_vis_k_1_limits_propagation`、`test_ttl_expiry_blocks_use_of_stale_info`、`test_cache_contains_only_arrived_info`、`test_cache_entry_validity_and_aoi`、`test_ring_topology_duplicate_advertisements_deduplicated` |
| 数据 deadline | `test_data_deadline_expired_while_waiting`、`test_data_deadline_expired_in_transit` |
| no-route / 环路上限 | `test_no_route_when_discovery_impossible`、`test_data_packet_loop_cap` |
| horizon 未完成 | `test_in_system_at_stop_when_destination_never_found` + round2 精确 horizon 结算测试 |
| fate 唯一与 bit 守恒 | `test_unique_fate_and_conservation`、`test_invalid_fate_and_unregistered_rejected`、`test_conservation_across_mixed_fates`、`test_control_ledger_full_accounting_and_conservation` |
| monitor 无干扰 / 同时刻顺序 | `test_monitor_does_not_change_behavior`、`test_same_time_emission_order_is_packet_id_order` |
| trace 确定性/公平 A/B 同 trace | `test_compile_trace_byte_reproducible`、`test_trace_compile_byte_reproducible`(CLI)、round2 trace 身份测试组 |
| 路由策略 | `test_hop_policy_picks_fewest_hops`、`test_delay_policy_uses_propagation_not_hops`、`test_capacity_policy_avoids_advertised_congestion`、`test_oracle_is_labeled_analysis_upper_bound`、`test_integration_hop_vs_delay_paths_differ` |
| 学习合同与 DDQN 数学 | `test_c3_to_c7_share_exactly_the_same_information_set`、`test_c1_sees_only_direct_neighbors`、`test_action_mask_legality`、`test_canonical_ddqn_target_math`、`test_ddqn_terminal_transition_blocks_bootstrap`、`test_learning_run_fails_closed_unconditionally` |
| 配置/trace/receipt fail-closed | `test_config.py`、`test_trace.py`、`test_review_round3.py`（含恶意 artifact 伪造拒绝） |
| 治理集成面 | `test_governance.py`（4 项） |

## 4b. 第四轮验收审查（Codex，7 组冻结缺陷）红→绿证据

第四轮由 Codex 验收审查给出 7 组产品缺陷（均为本地可修复）；每组先写行为测试确认在旧实现上失败（合计 39 红 / 7 绿），再最小修复转绿。永久回归测试全部在 `CODE/leo_sim/tests/test_review_round4.py`（46 项）。按指令不单独建 ROUND4 报告文件。

| 组 | 缺陷（旧实现实测） | 修复 | 红→绿证据 |
|---|---|---|---|
| 1 控制包几何中断 fate | ISL 上在传控制包遇几何失效 → `FateError: invalid control fate GEOMETRY_LOSS_IN_FLIGHT`，natural_end=false | 控制账本新增 GEOMETRY_LOSS_IN_FLIGHT（与随机中断分列），计数器加 `geometry_lost`，receipt 计数键集同步 | `test_control_geometry_loss_in_flight_is_legal_and_accounted`（红：natural_end=False → 绿：natural_end=True、几何损失=2、随机=0、守恒成立、占用 1.0s 记账）、`test_control_geometry_loss_receipt_roundtrip`（verify 全过且 fate 正确报告） |
| 2 方向性 ISL 路由 | `_undirected` 虚构反向链路，可把死路方向当候选 | 拓扑构造时验证物理双向性（缺反向边即 ValueError fail closed）；路径计算改用真实有向边的反向邻接多源 Dijkstra | `test_topology_construction_fails_closed_on_unidirectional_link`、`test_directed_routing_never_fabricates_reverse_paths`（红：返回 `["N"]` 指向死路 → 绿：`unreachable`/空候选）、`test_directed_routing_follows_real_forward_edges`（前后皆绿的对照） |
| 3 几何变化认证 | `ELEV_RATE_DEG_S=1.0` 不覆盖配置域（300 km 实测 ≈1.4223247°/s）；变化恰在区间终点 t1 时返回 None | 速率界按天顶推导重定 2.0°/s（推导注释入代码）；`_next_change_adaptive` 对 t1 显式求值，二分重构为共享助手 | `test_elevation_rate_bound_covers_the_supported_config_domain`（红：实测 1.42 > 旧界 1.0 → 绿：1.40 < 实测 < 新界 2.0，300 km×4 倾角×4 经度稠密扫描）、`test_next_change_detected_exactly_at_interval_end`（红：None → 绿：≈t1）、`test_next_change_start_stays_open_and_deterministic`（对照） |
| 4 公共入口 fail-closed | 站点 lat/lon 字符串/bool 泄露 TypeError 或被接受；CSV bits/坐标/时间/deadline 非法文本泄露 ValueError；损坏 receipt/manifest/resolved_config/ledgers JSON 与损坏/缺列 trace.csv 使 verify 抛 JSONDecodeError/ValueError/KeyError | 站点字段类型检查 + YAML 解析包装为 ConfigError；CSV 字段级 TraceError 化；verify 全部加载点防御式包装 + 类型守卫；`_load_precompiled` 包装；`main()` 兜底网（ConfigError/TraceError/ValueError/TypeError/KeyError/JSONDecodeError → 非零退出，永不打印 traceback） | `test_site_field_types_fail_closed`（7 例）、`test_cli_config_validate_bad_site_controlled_exit`、`test_cli_config_validate_malformed_yaml_controlled_exit`、`test_csv_bits_must_be_plain_positive_int`（5 例）、`test_csv_field_text_fail_closed`（4 例）、`test_cli_trace_compile_bad_csv_controlled_exit`、`test_receipt_verify_corrupted_json_returns_errors`（4 文件）、`test_receipt_verify_corrupted_trace_csv_returns_errors`、`test_receipt_verify_trace_csv_missing_columns_returns_errors`、`test_receipt_verify_receipt_json_wrong_type_returns_errors` |
| 5 缓存到达时间 | `valid_at` 只查 generated_at：未来 received_at 的条目被当作有效信息 | CacheEntry 构造校验（有限时间、ttl>0、received_at ≥ generated_at 否则 ValueError）；有效性 = generated_at ≤ received_at ≤ now ≤ generated_at+ttl，缓存/路由/学习共用 | `test_cache_entry_future_arrival_is_not_valid`（红：now=3 判有效 → 绿：未来到达无效）、`test_cache_entry_rejects_malformed_times`（6 例）、`test_information_set_routing_and_learning_share_the_arrival_rule`（红：路由返回未到达源、学习信息集非空 → 绿：三者同规则） |
| 6 M-Lab 网格映射 | 权重固定默认网格键，自定义聚合下与端点失配后被 1e-9 平滑静默吞掉 | 适配器使用 resolved config 的 grid_deg/aggregation_deg；每源活跃 OD 覆盖检查，无覆盖即 TraceError；删除 1e-9 平滑 | `test_mlab_weights_follow_configured_grid_degrees`（红：旧代码 2° 端点失配 → 目的分布 ≈50/50 → 绿：1000:1 权重下 >90% 流向 b）、`test_mlab_without_active_od_coverage_fails_closed`（红：静默编译 → 绿：TraceError）；既有 `test_mlab_adapter_labels_measurement_proxy` 的站点改为真实有覆盖的 OD 对（Amagasaki↔Tokyo）并保留全部 provenance 断言 |
| 7 ControlPacket 合同 | 缺 received_at 运行语义与共享 validity 规则；账本实例不含接收时刻 | ControlPacket 增加 received_at（仅真实到达时设置）与 valid_at（TTL 窗，到达路径实际使用）；控制账本到达 fate 强制携带 received_at，实例导出 [fate, bits, received_at]，receipt 校验三元组与到达/未到达一致性 | `test_control_packet_carries_task_contract_fields`（红：AttributeError → 绿：全字段 + valid_at 语义）、`test_control_received_at_enters_ledger_and_matches_cache`（红：实例二元组 unpack 失败 → 绿：账本接收时刻 = 缓存 received_at，AoI 一致） |

注：第四轮有两处既有测试按新合同适配（非削弱）：`test_fates_outage.py` 的到达 fate 记录现携带 received_at（G7 强制）；`test_trace.py` 的 mlab 站点改为有真实覆盖的 OD 对（G6 覆盖 fail-closed 使原站点组合成为非法配置）。守恒、fate 唯一性、provenance 等原断言全部保留。

### Codex 本地验收封口（第四轮复测后）

Codex 原样复跑 `/tmp/leo_v2_round4_probe.py` 时发现 6 组测试盲区并直接接管修复：网格 ID 别名、trace 时间序列化闭包、畸形 packet fate 二次崩溃、重复 trace ID 被字典覆盖、畸形 mechanism counters 崩溃、ControlPacket 缺 payload_bits/AoI/接收时刻一次性校验。第一批永久反例继续放在 `test_review_round4.py`；修复前该文件 **27 failed / 57 passed**，修复后 **85 passed**。随后针对同一信任边界追加 8 个先红后绿反例：receipt 按 resolved horizon/max_packets 重验 trace、重算 manifest 活跃端点、畸形 control instance 不触发二次崩溃；该文件最终 **93 passed**，V2 全量 **266 passed**。独立探针未修改，结果变为 alias REJECTED、compiler output ACCEPTED、receipt 攻击返回非空错误列表且不崩溃。全量与 smoke 证据见 §2。

## 5. 关键语义决定（现行；INFERENCE 处已标注，代码 docstring 同步）

1. **信息边界分级**：deliver 只许当前卫星对目的端的直接当前可见性 + 合法下行资源；hop/delay/capacity 的目的发现只读本地缓存中实际到达且未过期的广告；oracle 是唯一可用全局当前知识的策略且固定 `analysis_upper_bound` 标签，不进训练；未来星历任何决策路径都不可用（几何变化预测接口只服务事件调度器）。
2. **GSL 与 ISL 几何均可失效**：Walker 几何提供认证式下一变化时刻；不能认证的 provider 在 geometry_loss 启用时被内核拒绝（fail closed）。本条取代附录初版"ISL 几何不失效"的旧假设。
3. **传输中失效记账**：服务与"完成/几何失效/随机中断/deadline/退休期限"事件竞争；中途失败按已占用服务时间记账并产生唯一 fate；无暂停续传、无隐式 ARQ。
4. **MBB 硬退休**：新链建立后新包只走新链；旧链只排空已分配数据；retirement deadline 到达旧链必须结束，在传包被打断后整体回队重传（不构成重复 fate）； retirement 与几何失效、GE、packet deadline 同台竞争。
5. **公平有限接入**：接入由需求驱动（有数据待发/有合法出口需求才请求）；每星 FIFO 等待队列；`slot_lease_s` 租期轮转 + `retirement_deadline_s` 硬兜底 + `idle_release_s` 空闲释放（仅在有等待者时）；K=1 下所有符合条件端点有界获得服务，不再按 cell 字典序永久占槽。
6. **迟滞物理量**：`hysteresis_deg` 为仰角差门限（度），名称与物理量一致；不冒称 dB 链路预算。
7. **trace 身份与运行配置身份分离**：`trace_identity_sha256` 只含需求生成相关字段；路由/接入/链路/控制/学习参数改变不改变 trace 身份——两臂公平 A/B 消费同一不可变 trace 由此保证。
8. **receipt 信任模型**：本地 verify 只证明 artifact 间内部一致性；外部防篡改锚点（clean commit、授权 manifest、外部 hash）属治理链阶段，本报告不假装已解决。
9. **M1/M2 吸收**：corrected queue reward 与本地出向队列观测为唯一基线语义（`learning.reward=queue` 为唯一合法值）；无 M1/M2/M3 开关、无线性/distance 奖励、无旧 checkpoint 兼容。
10. **有向 ISL 路由**：路径与可达性只按真实有向边计算；物理链双向性在拓扑构造时验证（fail closed），路由层永不补边（第四轮）。
11. **缓存时间合同**：条目仅在 generated_at ≤ received_at ≤ now ≤ generated_at+ttl 时有效；未来到达、非有限时间、received_at < generated_at 一律拒绝或无效；缓存/路由/学习共用（第四轮）。
12. **M-Lab 覆盖 fail-closed**：权重键绑定 resolved config 的网格度；无活跃 OD 覆盖即拒绝编译，不存在任何静默均匀回退（第四轮）。
13. **控制包全合同**：origin/sequence/generated_at/received_at/ttl/remaining_hops/payload_bits 均为真实运行字段；接收时刻进入控制账本与缓存合同；几何损失与随机中断为控制账本中两个分列 fate（第四轮）。

## 6. 与旧治理链的集成状态（FACT + EXTERNAL_GATE）

- FACT：`governance.py` 提供密封 run intent（runtime_kind 必须 `leo_sim_v2`，否则 fail closed；绑定 config SHA + trace 身份 SHA + code SHA；拒绝未知字段与 shell 命令），被 `test_governance.py` 4 项覆盖；旧治理代码零改动，旧回归 337 项保持绿，未削弱任何既有 fail-closed 门。
- EXTERNAL_GATE：把 V2 intent 嵌入正式 `compile_experiment`/`authorize_experiment`/受控 dispatcher/`remote_job` 的 schema 级接线属于 VM/治理阶段——本轮约束禁止改动旧治理链与部署，且该链路只能在授权 + VM 环境下端到端验证。旧 Gateway runtime 保留为对照 runtime，绝不做 V2 fallback。

## 7. 未完成 / UNVERIFIED / EXTERNAL_GATE（如实）

- **TensorFlow 真实 DDQN 未验证**（本环境无 TF）：真实建模/一步推理/一步训练/action mask/save/load/固定 seed 重现是 VM 门；本地学习运行一律 fail closed（`LearningUnavailable`，退出码 3）。不得引本报告声称算法迁移完成。
- **三角色审阅、finalization、授权、VM 部署、自然结束收据链**：未执行，属 EXTERNAL_GATE。
- **依赖版本对齐**：方案 B 已本地验证——VM 同版本栈（Py3.11.14/NumPy 1.24.3/SimPy 4.0.1/PyYAML 6.0.2，`/private/tmp/leo-v2-vm-compat`）下 leo_sim 266 全绿、smoke+verify 通过，非学习场景 VM 侧零依赖变更可行；跨版本 receipt 核验实测拒绝。学习门仍需 VM leo-i39 的 TF 2.13.1（仅 CPU）。
- **提交/push**：约束禁止；工作树全部改动未提交，进入治理链前需用户授权提交策略（handoff §2 拆分已经仿真验证：22/88/219）。
- **算法效果、速度收益**：无任何结论；oracle 仅为分析上界；旧平台 2.09–5.78× 加速数字不继承。
- **M-Lab**：仅 OD 权重 proxy，强制 `measurement_proxy`，未做代表性校准。
- **oracle 等待决策**：v1 oracle 用当前全局知识做最短路，不用未来可见性优化等待，上界偏松（INFERENCE）。
- **大星座/长 horizon scaling**：未验证（UNVERIFIED）。
- **几何速率界**（仰角 2.0°/s、斜距 20 km/s）为覆盖配置域的推导保守界（300 km 天顶推导 ≈1.57°/s、稠密扫描实测 ≈1.42°/s），非 Starlink 校准；超界 provider 不得使用。

## 8. 复现方式

```bash
cd /private/tmp/m2-leo-platform-v2-runs/20260812T163928Z-22ae650a/worktree
PY=/private/tmp/m2-leo-platform-v2-verify/bin/python
$PY -B -m pytest -q -p no:cacheprovider CODE/leo_sim/tests
$PY -B -m CODE.leo_sim run --config CODE/leo_sim/profiles/smoke.yaml --out /private/tmp/leo-smoke
$PY -B -m CODE.leo_sim receipt verify /private/tmp/leo-smoke
```

---

## 附录：初版报告原文（2026-08-13 第一轮前；已被独立审查否决，保留为历史声明，不作状态依据）

> 以下为初版全文，未作改动。其"本地实现完成"结论与 89 passed 计数仅证明当时已有测试通过，不证明机制正确；其中"ISL 几何不失效"等语义决定已被第二轮修复取代。

# LEO 仿真平台 V2 本地实现报告（2026-08-13）

> **状态撤回（2026-08-13 第二轮）**：本报告原述的"本地实现完成"结论已被独立反例审查否决（10 个探针全部复现，见 `PLATFORM-V2-REMEDIATION-20260813.md`)。本文保留为**被审查的历史声明**，不再作为状态依据。当前状态：**LOCAL_PROTOTYPE / REVIEW_FAILED**。下文计数（89 passed 等）仅证明当时已有测试通过，不证明机制正确。

- 范围：冻结任务书 `/private/tmp/m2-leo-platform-v2-20260813/task.yaml` 的本地可实现部分。
- 实施位置：隔离工作树 `/private/tmp/m2-leo-platform-v2-runs/20260812T163928Z-22ae650a/worktree`,base `4fe918f`。
- 本文状态口径：FACT = 有第一手命令证据；INFERENCE = 由证据推导；UNVERIFIED = 本轮无法本地验证。

## 1. 验证命令与真实计数（FACT）

在工作树根目录执行，解释器 `/private/tmp/m2-leo-platform-v2-verify/bin/python`(Python 3.12，含 simpy/numpy/pyyaml，无 TensorFlow):

| 命令 | 结果 |
|---|---|
| `pytest -q -p no:cacheprovider CODE/leo_sim/tests` | **89 passed, 0 failed, 0 skipped** |
| `pytest -q CODE/tests CODE/experiment_platform/tests CODE/work/tests -k "not test_read_cgroup_used_gb and not test_output_dim_and_apply_shape and not test_self_supervised_training_reduces_loss and not test_save_load_roundtrip"` | **337 passed, 17 skipped, 4 deselected**(4 个 deselect 为任务书预登记的环境限制项，非本次改动引入） |
| `python -B -m compileall -q CODE/leo_sim` | 通过，无输出 |
| `python -B -m CODE.leo_sim config validate CODE/leo_sim/profiles/smoke.yaml` | 退出码 0，输出 config sha256 |
| `python -B -m CODE.leo_sim run --config CODE/leo_sim/profiles/smoke.yaml --dry-run` | 退出码 0，输出 config/trace/code 三个 sha 与资源上限，不写任何运行产物（dry-run 用临时目录） |
| `git diff --check` | 通过，无输出 |
| 真实星座 smoke 全跑（`run --config smoke.yaml --out <tmp>`，非 dry-run) | `natural_end=true`,`DELIVERED=1`,`conservation_ok=true`;`receipt verify` 退出码 0 |

跳过项说明：17 个 skipped 为旧测试自身的条件跳过（与本次无关）;leo_sim 测试内有 2 处 `pytest.skip` 保护（本环境无 TensorFlow 时执行 fail-closed 断言；若环境有 TF 则跳过）——本轮实际执行为"无 TF"分支，断言的是 fail-closed 行为本身。

## 2. 交付物（FACT)

新增 `CODE/leo_sim/`（全部为新文件，未修改任何既有文件）:

| 模块 | 职责 |
|---|---|
| `config.py` | 版本化 YAML schema（十顶层组），未知字段/非法组合 fail closed;defaults→profile→user→overrides 解析为 canonical JSON + SHA256 |
| `grid.py` | 0.25° 规范网格 ID、默认 1° 聚合、稀疏激活 |
| `trace.py` | 不可变 trace 编译器（uniform/gravity/hotspot/burst/diurnal/csv/mlab),manifest 含 schema/config SHA/输入 SHA/RNG 流映射/offered 账本/活跃端点/时间范围；mlab 强制 `measurement_proxy` 标记 |
| `rng.py` | SeedSequence 分派独立随机流（demand/ge_gsl/ge_isl/…) |
| `model.py` | Walker-delta 几何（位置/仰角/斜距/ISL 邻居），纯时间函数，无未来星历接口 |
| `outage.py` | 几何失效（确定性）与 Gilbert-Elliott 随机中断（默认关闭，GSL/ISL 独立流） |
| `control.py` | ControlPacket 快照、本地缓存（freshest-only、TTL/AoI、跳数记录） |
| `kernel.py` | SimPy 有界内核：TrafficEndpoint、K 接入槽、有限上下行队列、共享 GSL DRR 公平调度、方向性有限 ISL（控制非抢占优先）、BBM/MBB 切换、deadline、fate 账本、事件/实体/包三上限、monitor 开关 |
| `routing.py` | hop/delay/capacity 最短路 + oracle（标 `analysis_upper_bound`)；目的发现只读本地缓存（oracle 除外） |
| `learning.py` | C1/C3-C7 观测合同（同一信息集，仅表示/AoI 处理不同）、动作掩码、canonical Double-DQN target(numpy)；无 TF 一律 `LearningUnavailable` fail closed |
| `fates.py` | 数据 fate 唯一账本 + 控制独立账本 + bit 守恒校验 |
| `receipt.py` | receipt 构建/落盘/核验：config/trace/manifest/code 四个 SHA、自然结束、机制 requested-vs-effective、fate 唯一与守恒重算 |
| `__main__.py` | CLI:`config validate` / `trace compile` / `run [--dry-run]` / `receipt verify` |
| `profiles/smoke.yaml` | 12 星 3 面真实 Walker 星座 smoke |
| `tests/`(13 个文件，89 测试） | 行为测试：交付路径、有限队列拒绝/溢出、DRR 公平、BBM/MBB、几何/GE 中断（GSL 与 ISL 独立流）、控制带宽/优先级/vis_k/TTL、路由分歧、学习合同、CLI/receipt 闭环、trace CSV 重复 ID/非法坐标拒绝、monitor 无干扰、同时刻顺序 |

## 3. 关键语义决定（INFERENCE，已在代码 docstring 标注）

1. **信息边界分级**:deliver 动作只许当前卫星直接可见性；hop/delay/capacity 的目的发现只许读本地缓存中"实际到达且未过期"的广告；oracle 是唯一可用全局当前知识的策略且被打上分析上界标签；未来星历任何路径都不可用。
2. **ISL 几何不失效**:Walker-delta 邻居关系在 v1 被视为几何稳定，几何失效只作用于 GSL;GE 随机中断分别作用于 GSL/ISL。这是显式建模假设，不是遗漏。
3. **传输中失效记账**:在完成时刻做确定性失效判定，占用服务时间全额计入 `occupied`，产生唯一 fate；无暂停续传/ARQ。
4. **溢出语义**：下行队列满计入 `ACCESS_QUEUE_OVERFLOW`（下行属接入服务）;ISL 全候选满计 `ISL_QUEUE_OVERFLOW`；"无可用动作"(control 开启但无任何目的信息）进入 pending 等每 tick 重决策，不静默丢弃；control 关闭时同等情形判 `NO_ROUTE`。
5. **MBB**：仅 `dual_connect` 且 retiring 数未超限且新星有空槽时启用；旧链只排空已分配数据包，退休时限到后未发完的包重指派到新链；任何切换不抢占在传数据包（BBM 顺延、MBB 退休顺延）。
6. **M1/M2 吸收**:corrected queue reward 与本地出向队列观测写死为唯一基线语义（`learning.reward=queue` 为默认且唯一合法学习奖励语义之一）,v1 无 M1/M2/M3 开关、无线性奖励、无旧 checkpoint 兼容。

## 4. 与旧治理链的本地集成状态（FACT/INFERENCE)

- FACT：本包自带 config/trace/code/receipt 的 SHA 绑定与 fail-closed 核验，可作为后续 compile→review→authorize 链路的哈希基板。
- FACT：既有 `CODE/experiment_platform`、`CODE/work` 测试全部保持绿（337 passed)，未削弱任何既有 fail-closed 门。
- INFERENCE：把 leo_sim receipt 嵌入正式 experiment contract(compile_experiment/authorize_experiment 的 schema 扩展）属于 VM 阶段工作，本地安全范围内未改动治理代码。

## 5. 明确未完成 / UNVERIFIED

- **TensorFlow 真实训练未验证**（本环境无 TF)：真实 Double-DQN 构建/一步训练/save/load 是 VM 门；本地只有 numpy 版 canonical target 数学与观测/动作合同测试。学习运行本地一律 fail closed（退出码 3)。
- **VM 部署、三角色审阅、授权、自然结束收据链**:UNVERIFIED，未执行也不允许本轮执行。
- **算法效果、速度收益**:UNVERIFIED，本轮无任何算法优劣结论；oracle 仅是分析上界标签。
- **M-Lab**：仅作 OD 权重 proxy,`measurement_proxy`，未做代表性校准。
- **oracle 的"等待"决策**:v1 使用当前全局知识做最短路，不使用未来可见性做等待优化；上界因此偏松（INFERENCE)。
- **大星座性能**:66+ 星、长 horizon 的运行时/内存未做 scaling 验证（UNVERIFIED)。

## 6. 复现方式

```bash
cd <worktree>
PY=/private/tmp/m2-leo-platform-v2-verify/bin/python
$PY -B -m pytest -q -p no:cacheprovider CODE/leo_sim/tests
$PY -B -m CODE.leo_sim run --config CODE/leo_sim/profiles/smoke.yaml --out /tmp/leo-smoke
$PY -B -m CODE.leo_sim receipt verify /tmp/leo-smoke
```
