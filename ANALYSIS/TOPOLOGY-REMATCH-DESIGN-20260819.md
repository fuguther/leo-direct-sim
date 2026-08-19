# 动态 ISL 拓扑重匹配（D2）设计稿

> 日期：2026-08-19。对应旧平台设计深审 D2（LEGACY-DESIGN-AUDIT-20260819.md）
> 与旧平台 `moveConstellation`（SimulationRL.py:5183，默认 deltaT=3600）、
> `markovianMatchingTwo`（:8330）。目标：让 V2 的长时窗实验也能反映星座
> 移动造成的跨面邻居重配，同时不把旧平台 `updateSatelliteProcessesRL`
> docstring 自述的「does not work correctly」（:4506-4509）搬进新库。

## 1. 现状与差异（FACT）

- V2 `Constellation.neighbors`（model.py:503-515）按卫星 ID 静态给出 N/S 面内
  与 E/W 相邻面固定邻居；`routing.build_topology` 在 Kernel 构造时只建一次
  （kernel.py:700-708），之后 `self.topo`、反向邻接、单源广播树都冻结。
  星座移动只通过 `isl_available`（地球遮挡/最大距离）表现为链路瞬时可用性
  变化，**不改变“这个方向连到哪颗星”**。
- 旧平台每个 `deltaT`（默认 3600 s）推进星座并重跑 `markovianMatchingTwo`：
  跨面候选按两两距离、可用收发机方向槽、每面对最大可视距离过滤后做
  **贪心最短边匹配**；面内 N/S 邻居固定不重算（:8413-8433）。随后重配 GSL、
  重建图、重算所有在途块路径（:5273-5283）。
- 用户实验窗默认 5 s：旧平台 3600 s 重匹配一次，**5 s 内行为与 V2 静态拓扑
  完全相同**。因此 D2 默认值必须保持 V2 现状，只有显式配置重算间隔才改变。

## 2. 设计决定

### 2.1 配置

```yaml
topology:
  recompute_interval_s: null   # null/缺省＝静态（完全保持 V2 现状）；>0 才启用
  matching: "markovian"        # 仅支持旧平台 Markovian 贪心最短边匹配
```

- `recompute_interval_s` 为 `null` 或大于 0 的有限数；`0` 拒绝（语义不清）。
- 只作用 ISL 拓扑；GSL 建链/换链已由 V2 的 BBM/MBB 状态机连续处理，不并入
  该周期（旧平台 moveConstellation 里的 `linkSats2GTs`/`_apply_mbb_gsl_handover`
  在 V2 有等价或更细粒度的对应物）。

### 2.2 匹配算法（实现层，非旧代码复制）

每次重算时刻 `t`，为全部卫星重算跨面 E/W 候选：

1. 候选边：不同面、`geometry.isl_available(a,b,t)` 为真、两端各自 E/W 收发机
   方向槽尚未占用。
2. 权重：`isl_range_km(a,b,t)`（旧平台用 slant_range 升序做贪心，:8400）。
3. 贪心：按距离升序，逐条接受两端方向槽都空闲的边，直到无可用候选。
4. 面内 N/S 保持现有的按索引固定邻居（旧平台语义：intra 不变）。
5. 结果必须双向：`build_topology(..., t=t)` 复用现有双向校验，单向边 fail
   closed，不静默补边。

实现位置：
- `Constellation.neighbors_at(sat_id, dirs, t)`：N/S 直接复用现有索引规则；
  E/W 调 `Constellation._cross_plane_matching(dirs, t)` 输出配对映射。
  匹配逻辑放在 `model.py`，避免几何模型反向依赖 routing；`MemoizedGeometry`
  对该时间查询做透明委托/缓存。
- `routing.build_topology(geometry, num_sats, dirs, t=None)`：`t=None` 走
  原 `geometry.neighbors`（字节级同现状）；`t` 指定时走 `neighbors_at`。

### 2.3 重算事件与在途语义

- Kernel 增 `_topology_ticker()`（仅 `recompute_interval_s` 非空时创建）：
  `yield timeout(interval)`，`now < horizon` 时执行一次重算，循环至地平线。
  地平线边界处不再重算（最终统计 epoch 保持连续）。
- 重算步骤（原子完成，同一事件时刻执行完再继续调度）：
  1. `new_topo = routing.build_topology(..., t=now)`。
  2. 对每个方向 d，若旧 `self.isls[s][d]` 的对端仍是 `new_topo[s][d]`，
     保留该 ISLLink 对象；否则把该旧链路上的**数据包**回退到
     `self.pending[s]`（移出 `data_q`、扣 `data_bits/data_area`），由既有
     pending 重决策路径自然处理；正在服务的包不打断（物理上已开始）。
  3. 为新对端创建新 `ISLLink` 并替换 `self.isls[s][d]`；旧对象服务完成后
     队列为空，自然等待，不再有新包入队。
  4. 重建 `topo`、`_routing_reverse_adj`、`_routing_sorted_rev_adj`、
     `control_children`，`_state_version += 1`。
  5. 控制包留在旧链路队列（有限容量 + TTL，drain 或过期都有回执），不做
     静默丢弃；广播树自下一个 advertise 周期用新拓扑。
- 诚实边界：旧平台在自己注释里承认重匹配时重排队失败（:4506-4509）；V2
  的数据包回退到 pending 是**有意的更优选择**，会在 PR 里写明与旧平台的
  差异，不做“照搬旧 bug”的差分。

### 2.4 receipt / 观测

- `mechanisms.requested` 增 `topology_recompute_interval_s`（或布尔
  `topology_recompute`）；`effective` 增 `dynamic_topology`（由
  `topo_recomputes>0` 推导）。
- `MECHANISM_COUNTER_KEYS` 增 `topo_recomputes`。
- 观测合同不变：路由/学习的顶层信息边界仍按“拓扑是星座先验”的 C 类上下文
  处理；重算本身是物理层事实，不注入任何未来信息。D6/D7 的 per-action
  链路特征是否进观测仍按旧计划单独评审。

## 3. 验证计划

1. `build_topology(..., t)` 静态/动态分支与双向校验单测；缺省 `t=None`
   与原输出逐字节一致。
2. 脚本几何：`neighbors_at` 在 t=1 改变；`recompute_interval_s` 触发 3 次
   重算（0.5/1.0/1.5），`topo_recomputes` 计数正确。
3. 队列迁移：重算前滞留在旧链路 data_q 的包在重算后被 pending 重决策，
   不产生 NEW/DUP 比特账目缺口；`check_conservation` 通过。
4. 默认（null）全量测试回归：405 通过、receipt 键集闭合。
5. 长时窗差分（后续实验包）：5 s 臂与启用 1 s 重算臂在拓扑边界处产生可
   观测的时延/拥塞差异，差异可归因到 `topo_recomputes`。

## 4. 待拍板

- 控制包留在旧链路 drain 的取舍是否接受（备选：重算时对旧链路控制包记
  `CONTROL_EXPIRED`；我不推荐，因为那不是“过期”）。
- 重算边界是否同步刷新学习体（旧平台对 temporal encoder 调
  `reset_satellite`，:5262-5269）：V2 learning 无时序隐状态时不需要，先留
  open item。
