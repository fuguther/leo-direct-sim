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
