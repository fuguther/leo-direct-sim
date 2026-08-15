# V2 补图编码器迁移勘察（2026-08-14）

> 目的：把 V1 的 GAT/MPNN 图编码器迁入 V2，并补上 field-wise observation age
> 数据层地基。本文只做落点清单与改造边界，不写实现。
> 相关决策：`DECISIONS.md` 的 `DEC-20260814-001`。
> 证据：V2 在 `/private/tmp/m2-leo-platform-v2-runs/20260812T163928Z-22ae650a/worktree`，
> 分支 `codex/20260813-platform-v2`；V1 在源仓库 `CODE/SimulationRL.py`。

## 0. 一句话结论

V2 现在没有图编码器：`learning.py` 里所有 C1/C3–C7 都是同一个
`Dense(64)→Dense(64)→Dense(5)` MLP，靠 `build_observation` 手工聚合（均值 /
AoI 加权均值 / 最新一条 / 分跳桶 / AoI 排序）把控制缓存压成定长向量。要做的
迁移 = 把 V1 的 `GraphMessagePassingReadout`（gat/mpnn）搬进 V2，替换手工聚合，
同时把年龄从"每 origin 一个"升级成"每字段一个"。

## 1. V2 现状（FACT）

### 1.1 网络

- `CODE/leo_sim/learning.py:115-122`：`TensorflowDDQN._network` 是
  `Input(CONTRACT_DIMS[contract]) → Dense(64,relu) → Dense(64,relu) → Dense(5,linear)`。
- 动作集 `ACTIONS = ("deliver", "N", "S", "E", "W")`（`learning.py:43`）。
- 无邻接矩阵、无注意力、无消息传递（Kimi 审计 `03-c3-c7-state-encoder-audit.md` 已确认）。

### 1.2 信息聚合（`learning.py:274-326`）

`build_observation` 把 `cache.valid_entries(now)` 压成定长向量：

| contract | 聚合 |
|---|---|
| C1 | 本星 + 1 跳邻居，定长拼接补零 |
| C3 | 全部 entry 等权均值 |
| C4 | exp(−aoi/ttl) 加权均值 |
| C5 | AoI 最新一条 + 有效标志 |
| C6 | 按 hops 分 4 桶，桶内均值 |
| C7 | 按 AoI 升序取前 5，逐条拼有效位 |

### 1.3 已有原料（图编码器可以吃这些）

- `CacheEntry`（`control.py:14-60`）：`origin / payload / generated_at /
  received_at / ttl_s / hops`，`payload` 含 `isl_queue_bits /
  isl_propagation_s / visible_cells / serve_cells / access_slots_used /
  access_slots_cap`。
- `routing.build_topology`（`routing.py:63-82`）返回有向邻接图
  `sat -> {方向: 邻居}`，且已 fail-closed 校验双向性。
- 决策热路径：`kernel.py:1320` `_learning_observation`、`kernel.py:1352`
  `_learning_action`。

## 2. V1 可复用的部分（FACT）

- `CODE/SimulationRL.py:5788` `GraphMessagePassingReadout`：
  - `mode='gat'`：多头注意力，权重 `gat_W / gat_a_src / gat_a_dst`（`5857-5894`）。
  - `mode='mpnn'`：非注意力邻接归一化均值聚合（`5895-5917`）。
  - `reliability_aware / aoi_gate`：RAAC 的 AoI 可靠性门（`5977-5986`），
    这是 V1 里唯一显式用 AoI 的地方。
- 输入是固定宽度的 k 跳子图（节点特征 + 邻接 + 方向掩码 + 位置 tail）。

## 3. 迁移要改的三处（落点，非结论）

1. **方向语义重映射**：V1 方向 `U/D/R/L`（上下左右），V2 方向 `N/S/E/W`
   （北南东西）+ `deliver`。方向命名与邻接方向必须对齐，不能照搬。
2. **动作空间 4→5**：V2 多一个 `deliver`（落地），Q 头 `Dense(4)→Dense(5)`；
   `deliver` 必须受"当前是否可见目的小区"的 mask 约束。
3. **边特征需新增**：V1 邻接是 0/1 二值，无边特征；要 edge-aware 必须在 V2
   新写边特征（带宽/传播时延/可用性），这是 V1 本来就没有的。

## 4. 数据层地基：field-wise observation age（核心，需深挖）

V2 现在是"每 origin 一个年龄"：`CacheEntry.aoi(now) = now - generated_at`
（`control.py:53-54`），`payload` 里所有字段共享同一个 `generated_at`
（`control.py:102` `build_snapshot`）。但设计审查（`02-experimental-design-review.md`
第 7 节）指出：队列、链路可用性、时延的陈旧速度不同，必须逐字段给年龄。

### 4.1 各字段的物理陈旧语义（INFERENCE，需实验验证）

| 字段 | 变化速度 | 年龄语义 |
|---|---|---|
| `isl_queue_bits` | 快（随流量变） | 易失，短龄即失效 |
| `visible_cells / serve_cells` | 中（随几何/关联变） | 几何驱动 |
| `isl_propagation_s` | 慢（几何慢变） | 长龄仍可信 |
| `access_slots_*` | 中（随关联变） | 关联驱动 |

### 4.2 改造落点（下一步深挖目标）

以下为深挖后的精确落点（行号对应当前 worktree HEAD `82be86f`）。

**字段现在在哪里生成（`kernel.py:1085-1121` `_advertise` + `control.py:78-108`
`build_snapshot`）：**

- `isl_queue_bits`：`_advertise` 里 `isl_bits = {d: data_bits + ctrl_bits}`，
  快变（随流量）。
- `isl_propagation_s`：`_advertise` 里由 `model.propagation_delay_s(...)` 现算，
  慢变（几何驱动）。
- `visible_cells`：`build_snapshot` 里 `geometry.ground_visible(...)` 现算。
- `serve_cells`：`_advertise` 里 `snap["serve_cells"] = serve`（`kernel.py:1102`），
  由端点 `links.state == "active"` 现算。
- `access_slots_used / access_slots_cap`：`build_snapshot` 里由 `len(slots[sat])`
  与配置传入。

**字段现在在哪里被消费（改了生成端必须同步改消费端）：**

1. `learning.py:247-259` `_origin_features`：读 `isl_queue_bits`、
   `access_slots_used/cap`、`visible_cells`，且把 `entry.aoi(now)` 当作单一
   `aoi_norm` 压进特征第 4 维。→ 逐字段化后这一维要拆成每字段一个 age。
2. `routing.py:168` `observed_propagation`：读 `isl_propagation_s`。
3. `routing.py:198`（capacity 策略）：读 `isl_queue_bits`。
4. `routing.py:121` `destinations_in_cache`：读 `serve_cells`。
5. `kernel.py:1637-1638`（receipt 里的 caches 快照）：读 `visible_cells`、
   `serve_cells`，并调用 `e.aoi(self.env.now)`。

**逐字段时间戳的最小改造面（若按 field-wise 落地）：**

- `control.py:78-108` `build_snapshot`：`payload` 由"共享 `generated_at`"改为
  "每字段携带自己的 `observed_at`"（可仍保留一个包级 `generated_at` 作
  TTL/有效性锚，另加 `field_age: dict[field, timestamp]`）。
- `control.py:53-54` `CacheEntry.aoi`：改为 `aoi(field=None)`，无 field 时
  回退到包级 age，传 field 时返回该字段 age。
- `learning.py:247-259` `_origin_features`：`aoi_norm` 从单标量改为逐字段，
  `ORIGIN_FEATURES`（`learning.py:29`）随之扩展。
- `kernel.py:1097-1102` `_advertise`：向 `build_snapshot` 传入逐字段时间戳。
- 消费端 5 处（上列）同步适配新 payload 结构，避免"改了生成、断了读取"。

**关键边界（写代码前必须定，否则会引入审查已指出的混淆）：**

- `generated_at`（包级）仍用于 TTL 有效性与传播账本；`field_age` 只用于
  学习/路由的年龄语义。二者不能混。
- 逐字段时间戳的来源必须真实：字段的 `observed_at` 应是"该字段在源卫星被
  实际测量/生成的时刻"，不是"包发出时刻"。否则 field-wise age 是假的，
  会被审查第 7 节抓住。

## 5. 待排雷（不阻塞本文档，但会影响口径）

- Target-Aware GNN-DQN 2026：destination 是否已进 message passing。
- field-wise age 的 provenance 传播是否已有反例。
