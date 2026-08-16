# Q0 接口设计稿（2026-08-17）

> 依据：Q0 说明书 §9/§10/§12/§13/§20；三方算法调研
> `ANALYSIS/Q0-ALGO-RESEARCH-20260817.md`。本稿只冻结接口与语义，
> 不实现算法。状态：草案，待用户拍板 Q0 目标/合同后进入实现。

## 1. 设计目标

Q0 = 解除调度器信息传播限制（全局当前状态瞬时可见；可扩展完整未来信息），
但保持全部网络物理约束（轨道/拓扑、传播时延、有限容量/队列、接入 K 槽、
BBM/MBB 切换、几何失效/随机中断、共享链路竞争），并允许「等待」与「联合
竞争处理」。三条硬约束：

1. **planner 只读、Kernel 唯一执行**：planner 不得直接调用 `put_data`/
   `DownlinkServer.put`/`_associate`/`_try_grant` 等变更原语（GPT/Kimi
   一致，否则可绕过容量/K/守恒）。
2. **快照与计划都绑定同一状态版本**：过期计划 fail-closed，绝不静默应用。
3. **等待必须占用有限 holding 容量**：不把等待映射到无界 pending
   （GPT review F2/Kimi I 项）。

## 2. 接口一：GlobalStateSnapshot（只读）

`Kernel.snapshot_global() -> GlobalStateSnapshot`，在单个 `env.now` 内原子
构造（快照期间禁止任何事件步进；SimPy 单线程保证同一回调内一致）。

必须覆盖的最小状态集（对应说明书 §9 与三方审计）：

| 组 | 内容 | 来源 |
|---|---|---|
| 拓扑/链路 | 静态 topo + 当前 ISL 可用性 + GE 状态（is_down）+ 下一恢复/失效时刻 | `self.topo`、`geometry`、`isls[*].ge` |
| GSL | 每端点-卫星关联状态（acquiring/active/retiring/retire_at）、K 槽占用 | `ep.links`、`self.slots` |
| 队列 | uplink/downlink/ISL data+ctrl 队列内容（顺序！）、占用 bits | `ep.queue`、`downlinks[*].queues`、`isls[*].data_q/ctrl_q` |
| 服务中 | 每链路当前服务包、服务开始时刻/剩余时长（`_svc`）、`current` | `uplinks/downlinks[*].current/_svc`、`isls[*]` |
| DRR | 每服务器 `deficit`、`rr_cursor`（影响后续服务次序） | `_drr_*` |
| 接入 | `access_wait`（FIFO 顺序+请求时刻）、`access_last_busy`、lease/idle 参数 | `self.access_wait` 等 |
| 包 | 每包位置（排队/服务中/pending/传播中？）、deadline、path、assigned_sat、bits | endpoints/downlinks/isls/pending/ledger |
| pending/holding | 现 pending 列表（后续改造为有限 holding queue） | `self.pending` |
| 控制面 | 每星 cache 有效条目（serve_cells/队列广告/AoI） | `self.caches` |

约束：
- 快照**只含当前时刻**状态；Q0-A 禁止读未来 demand/trace；Q0-B 由独立
  `future_view` 接口提供（说明书 §8 轨道预测单独标注）。
- 快照不可变（dataclass frozen / MappingProxy）；导出带 `env.now` 与
  `state_version`（单调递增计数，任何写操作递增）。

## 3. 接口二：JointPlan 注入（受校验，两阶段）

```python
planner: Callable[[GlobalStateSnapshot, PlanningContext], JointPlan]
# JointPlan = {actions: [PlanAction], version: int}
# PlanAction ∈ FORWARD(pkt_id, egress_dir) | DELIVER(pkt_id, sat) |
#              WAIT(pkt_id, until) | ACCESS_ASSIGN(endpoint, sat) | ...
```

执行链（Kernel 唯一写入口）：

```python
ok, errors = kernel.validate_joint_plan(plan)      # 阶段 1：只读校验
if not ok: fail_closed(plan.version, errors)       # 整份拒绝，不部分应用
kernel.apply_joint_plan(plan)                       # 阶段 2：原子提交
```

校验规则（阶段 1）：
- `plan.version == snapshot.state_version`，否则过期拒绝。
- 每个动作的包存在、位置与快照一致（不在服务中/已终结）。
- 容量/队列/K 槽按**整份计划**原子预留：同链路/同槽/同队列冲突 → 整份拒绝。
- 物理约束复检：几何可用性、GE 状态、deadline、retirement 边界、传播时延
  合法性；计划不得绕过 `_transmit` 的服务时间/竞争裁决。
- FORWARD 目标必须是真实拓扑邻接方向；DELIVER 目标星必须正在服务该 endpoint。
- WAIT 必须落在有限 holding 容量内（见 §4）。

应用语义（阶段 2）：
- 所有动作在同一 `env.now` 提交；服务仍由现有 server `_transmit` 消耗真实
  时间（计划只决定「谁、何时、走哪」，不加速/瞬移）。
- 提交后 `state_version += 1`。
- 记录审计：计划哈希、版本、首个分歧事件（D1 归因门禁）。

## 4. 等待动作与有限 holding queue

现状缺口：`pending` 是无容量 list、不计 queue_area（GPT review F2/Kimi I）。

设计：
- 每星新增 `SatelliteHoldingQueue`：配置容量（bits）+ `queued_bits` 记账 +
  `QueueArea` 积分 + deadline sweep + overflow fate（新 fate
  `HOLDING_QUEUE_OVERFLOW`，入守恒等式）。
- `WAIT(pkt_id, until)`：包进入 holding queue，占用容量/面积；`until` 到点
  或满足释放条件（链路恢复/服务星变化/控制信息到达）时触发重决策。
- `pending` 迁移：所有现有 `pending.append` 路径（no_info/临时不可用/退休
  回退）统一走 holding queue（语义等价 + 容量约束）。
- 报告：holding queue 面积/占用并入 `queue_area_bits_s` 与守恒回执。

## 5. 接入与服务的联合控制范围（待拍板）

按 `Q0-ALGO-RESEARCH` §4 冻结两个合同：
- **physics-only**：planner 可优化接入分配、服务顺序（覆盖 DRR/FIFO）、
  路由与等待——只保持物理约束。主 Q0 上界用此。
- **kernel-policy-preserving**：固定 DRR/FIFO/deliver-only，planner 只注入
  路由与等待——用于平台交叉验证。
- 实现上两个合同共享 `validate_joint_plan` 校验器，用配置开关选择是否允许
  ACCESS_ASSIGN / 服务顺序类动作。

## 6. 目标函数（待拍板，建议字典序）

`max 到期前交付 bits → min Σ 完成时延 → min Σ 队列积分`；求解器内部可另用
加权标量化（Kimi 修正）。Q0 与学习臂比较一律用物理指标（delivery/deadline/
时延 tail），不直接比 reward（A1/C3 未清前尤其禁止）。

## 7. 实现顺序（三步，每步独立可验收）

1. `snapshot_global()` + `state_version` + 测试（快照与事件序列一致性、
   版本单调性、无未来信息）。验收：任意配置下快照字段完整、与 `run()`
   结束状态一致。
2. holding queue 替换 pending（含容量/面积/守恒/overflow fate）+ 回归。
3. `validate_joint_plan`/`apply_joint_plan` + oracle 型 planner 注入
   （先实现 `Q0-I`：只解除信息限制、保持逐包动作，用于估计纯信息损失；
   再 Q0-J：+WAIT+联合；Q0-F 另标未来信息）。

## 8. 验收门禁（对应说明书 §14.4）

- planned-vs-executed 逐事件一致性阈值：服务时刻偏差、队列顺序、K 槽占用
  与计划一致；不一致 > 阈值即 fail（Kimi 修正 §6.5）。
- 变异测试：planner 直写内部状态/过期版本/超容量 WAIT/非邻接 FORWARD 均
  必须整份拒绝（fail-closed）。
- 回放可行率：MILP 计划注入 kernel 的可行率（§4.3），作为 Q0 链路的硬指标。
