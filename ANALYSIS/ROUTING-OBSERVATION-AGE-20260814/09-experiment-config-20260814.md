# 实验一/二完整配置（Codex × Kimi 最终定稿，2026-08-14）

> 目标：把所有可能涉及到的详细配置一次性锁死，跑之前不再有"缺配置/配置冲突"
> 的问题。本文件是配置真相源；与 `08` 矩阵文档冲突时以本文件为准。
> 平台分支：`codex/20260813-platform-v2`，config_version `leo-sim-config/v1`。

## 0. 与 Kimi 协商后的事实修正（重要）

1. Kimi 说"learning.seed 在 schema 里不存在、必须第一优先级补丁"——**已过时**。
   本分支已加 `learning.seed`（`config.py:135`，默认 None→回退 scenario.seed），
   kernel 已用它（`kernel.py:595`），并有测试。这条不再是需要做的事。
2. Kimi 确认的核心结构缺陷仍然成立：**观测聚合跳数与控制面传播跳数现在共用
   一个参数 `control_plane.vis_k`**，必须新增 `learning.obs_hops` 才能解耦。
   这是本文件第一个待实现项。
3. E0 三档数字来自 24 星 smoke（`08` 文档自注"换星座需重扫"），140 星跨洋
   场景**不能直接继承**，必须重扫验收。

## A. 星座与端点

- 星座：140 星（`num_satellites: 140, num_planes: 7, altitude_km: 600,
  inclination_deg: 98.6, min_elevation_deg: 30`），继承 `comparison.yaml`。
- 端点：**保留跨洋 Malaga(36.72, -4.41) ↔ Tokyo(35.68, 139.75)**。不换近距
  端点——换端点等于换研究问题。
- **解耦方案（待实现）**：
  - `control_plane.vis_k: 12`——固定，只负责传播足够远、目的地 serve_cells
    广告能到源端。验收：pilot 全场景 `no_info` = 0；不为 0 升到 15 重验，定稿冻结。
  - 新增 `learning.obs_hops`——实验一的自变量，契约只取跳数 ≤ obs_hops 的
    缓存条目；约束 `obs_hops ≤ control_plane.vis_k`，违反 fail-loud。

## B. 时间配置

- `scenario.time_step_s: 0.1`
- 训练 cell `scenario.duration_s: 120`；评估 cell `60`
- `learning.epsilon_decay_s: 30.0`（默认 300 在 120 s 里 ε 只衰减到 ~0.18，
  探索退不完，必须改；这是默认值与 duration 不匹配的隐患）
- 墙钟：无实测不许估。pilot 每臂 1 cell 必须记录墙钟/更新数/守恒/receipt；
  正式排产 = 实测单 cell 墙钟 × cell 数 ÷ 并发度（VM 24 核/64 GiB cgroup）。

## C. 流量

- `demand.mode: uniform`（主结论；gravity 只作敏感性附录）
- `demand.packet_bits: 8000000`（默认不动）
- `demand.deadline_s: null`（不引入 deadline，尾部时延用 p95/p99）
- 候选档：**低 50 / 中 130 / 高 260 Mbps**（provisional，待 E0 重扫转正）
- E0 必须先在正式场景（140 星、跨洋、hop、vis_k=12）重扫
  {50,100,150,200,250,300,400}，按冻结阈值验收后转正。

## D. 接入

全部用 schema 默认值，不改物理参数：

- `slots_per_satellite: 4, uplink_rate_mbps: 100, downlink_rate_mbps: 100,
  uplink_queue_bits: 64000000, downlink_queue_bits: 64000000, association: bbm`
- 核算：中档 130 Mbps ÷ 2 端点 ≈ 65 Mbps/GT < 单槽 100 Mbps，接入非瓶颈；
  ISL 1000 Mbps / 256M 队列同理。
- E0 验收：中档接入队列占用率 <5%；不满足唯一调整是 `slots_per_satellite`
  升到 8 后重验，**不动速率**，定稿冻结。

## E. 控制面

- `enabled: true, vis_k: 12, ttl_s: 10.0, advertise_interval_s: 1.0,
  packet_bits: 8000, priority: nonpreemptive_priority`
- 开销核算：140 星 × 1 Hz × 8 kbit × 12 跳，摊到每条 ISL <1%，pilot 实测记录。
- **登记现状**：12 跳传播时延 ≪ 1 s 广播周期 → 信息年龄上界 ~1.1 s ≪ ttl 10 s，
  实验一/二里"年龄"近似常量。这是实验三才拆开的问题，本文件只登记，不在实验一/二里声称年龄有区分度。

## F. 学习

- 契约：实验一 = `GAT`；实验二表A = {C3, MPNN, GAT} + 非学习 `hop` 臂；表B =
  {C1@obs1, 表A胜者}
- 超参（冻结）：`gamma: 0.99, lr: 0.001, batch_size: 64, replay_size: 50000,
  target_update_interval: 500, epsilon_start: 1.0, epsilon_end: 0.05,
  epsilon_decay_s: 30.0, algorithm: ddqn`；GAT/MPNN 网络结构按现有 profile 冻结
- 种子分池（冻结）：训练 `learning.seed {41–48}`，流量 `scenario.seed
  {101–108}`，评估 `{201–208}`（eval 模式、ε=0），调优 `{301–303}`；
  receipt 必须同时记录两个种子并 provenance 校验
- 训练预算 = 一次 120 s 在线训练 run。pilot 合格：更新数 ≥2000 且 reward 非平；
  不满足只允许 duration 翻倍重 pilot，不许顺手调超参
- 评估：每个 checkpoint 在评估 seeds {201,202,203} 各跑 60 s，取均值，
  配对在流量 seed 层做

## G. 特征构建（目的地特征补丁，待实现）

统一原则：**信息内容跨契约完全一致，编码随架构**（铁律 1 落地），配表征测试。

- 目的地特征 3 维追加到本星状态尾部：
  - `dst_bearing_sin / dst_bearing_cos`：目的地在本星 ENU 局部切平面内的方位角
    （由 ECEF 差向量投影，不用经纬度差——极区退化）
  - `dst_dist_norm = min(大圆距离/20000 km, 1)`
- 结果维度：C1 20→23、C3 8→11、C4 8→11、C5 9→12、C6 20→23、C7 29→32；
  GAT/MPNN 尾部 4→7，平铺 1636→1639
- 图节点位置 `[12:15]`：绝对 ECEF/7000 → **根相对 ECEF/7000**（可迁移、与相对
  方向特征自洽）
- 不做 per-node 目的地特征、不加边特征（留给实验二b F1）
- 数据层 PR 四项：`learning.seed`（已完成）+ `obs_hops` + 目的地特征 + 相对坐标；
  合并后重验 GAT/MPNN 训练链

## H. 执行顺序与 arm 清单

顺序：数据层 PR（obs_hops + 目的地特征 + 相对坐标）→ E0 重扫定档 → 全臂工程
pilot（1 cell/臂）→ 实验一 pilot（2 train seed × 1 traffic seed 估 σ_d，正式
n≥5）→ 实验一正式 → 定 h* → 实验二。

实验一 arms：`GAT × obs_hops {1,2,3} × 档 {低/中/高}`；中档 5 train × 2 traffic
= 10 cells/臂，低/高档 5×1 = 5 cells/臂；合计 60 cells；`vis_k: 12` 全臂相同。

实验二 arms（obs_hops=h*，中档）：表A {C3, MPNN, GAT} × 10 cells + `hop` 臂
（3 流量 seed 不训练）；表B {C1@obs1, 表A胜者} × 10 cells；高档敏感性 5 cells。

## I. 合格线与失败条件

- 工程合格（每 cell）：`conservation_ok=true`、`natural_end=true`、checkpoint
  sha256 校验通过、`no_info`=0、图截断计数=0、双种子 provenance 一致
- 实验级：中档各学习臂 completion ∈[0.65,0.95]；任一学习臂 < 同档 `hop` 臂 →
  标"学习失败"，降级为探索，不进主对比
- 统计：主对比（实验一 obs1 vs obs2、obs2 vs obs3；实验二 MPNN vs GAT）要求
  ≥2/3 cells 方向一致且配对差 bootstrap 95% CI 不含 0；其余标探索
- 实验无效：E0 阈值不过 → 调档重验；pilot 更新数/墙钟不过 → 按预定路径修，
  不许直接跑正式

## J. 待实现清单（跑之前必须完成）

1. `learning.obs_hops` 字段 + fail-loud 约束（obs_hops ≤ vis_k）
2. 目的地特征 3 维（bearing_sin/cos + dist_norm）进所有契约观测
3. 图节点位置改根相对 ECEF
4. E0 在 140 星正式场景重扫定档
5. pilot 实测墙钟与更新数
6. 全部改动合并 main 并 VM 部署后，正式实验才可启动
