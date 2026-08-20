# 研究执行顺序、真实流量与训练预算设计

> 状态：LOCKED（2026-08-21）
>
> 本文件是本轮已拍板决议的记录。人类可读的持续真相源是
> `ANALYSIS/EXPERIMENT-PROGRAM.md`，当前状态以
> `ANALYSIS/CURRENT-EXPERIMENT-READINESS.md` 为准；本文件不替代运行授权。

## 目标

在“拥塞控制与链路利用率”主线内，把 leo_sim V2 做到：

1. 平台的速率、拓扑、队列、信息边界和数据守恒没有已知会改变主要结论的硬伤；
2. 真实测量驱动的多 OD、突发流量能够稳定变成可复核的 V2 trace；
3. 当前实际接入的非学习和学习运行时都能在 VM 上自然结束；
4. 训练、checkpoint、评估、指标重算和资源证据形成完整闭环；
5. 每组实验单独实现、单独验证、单独产出结果，再进入下一组。

“平台完成”不等于 pytest 全绿。最低运行门包括：非学习基线、Q-learning、DDQN
各自真实运行；学习臂必须完成 train → checkpoint → eval，并留下同一 trace SHA、
checkpoint SHA、自然结束回执、峰值内存和重算后的指标。正式矩阵声称使用 GAT 或
MPNN 时，相应 graph contract 也必须分别通过同一门禁；否则不能写进正式结果。

## 固定的主路线

主路线是逐步往上加，不是一次性把所有实验写完：

```text
平台底座
  → 拓扑更新时间标定
  → 真实测量/多 OD/突发流量
  → E0 负载标定
  → CPU/内存 profiling
  → 全臂 train/eval pilot
  → 拥塞与链路利用率诊断
  → Q0-I/Q0-F 与信息年龄阶梯
  → 新拥塞控制方案
  → 正式配对矩阵
  → 敏感性实验
```

每一层必须先通过小 smoke、自然结束、守恒、指标重算和资源检查，才允许进入
下一层。失败就回到当前层修复，不把失败结果带入后续结论。

从最优逐步裁剪的信息路线（Q0-F/Q0-I → 局部队列 → 陈旧信息）是解释性路线，
用来回答“差距来自信息不足还是决策能力不足”，不取代真实流量下的主诊断路线，
也不阻塞最早的平台 smoke 和 E0。

## 流量决议

- 主实验使用有来源的 M-Lab 测量驱动 OD，按地理坐标映射到 V2 地面网格，再按
  测量权重和时间字段生成需求；它必须标为 `measurement_proxy`，不能冒充卫星
  用户原始业务包。
- 在相同 OD 权重上叠加可复现 burst，形成主流量场景；`uniform` 只做控制组，
  `population_gravity` 只做外部有效性/敏感性对照。
- 每条正式 trace 都绑定源文件 SHA、字段单位、时间映射、OD 映射、burst 变换、
  offered bits 和实际 realized load；trace 不可变，所有算法臂复用同一份 trace。

## 时间尺度与训练预算

代码中的三个时间参数保持分工：

| 参数 | 起始候选 | 选择规则 |
|---|---:|---|
| `scenario.time_step_s` | 0.1 s | D1/D2 主实验的几何/仿真时间粒度；不为了提速随意放大 |
| `topology.recompute_interval_s` | 扫 0.5/1/2/5 s，1 s 为候选默认 | 在同 trace/seed 下比较；0.5 s 与 1 s 的主要指标收敛且 1 s 资源更低时选 1 s |
| `control_plane.advertise_interval_s` | 1 s | 状态广告刷新，不等于邻居重匹配 |

训练和仿真时间分开预算：

- 3–5 s 只用于接线和冒烟；
- 训练 episode 以 20 s 作为起始候选，必须覆盖多个拓扑 tick 以及完整 burst/排空；
- 正式评估以 60–120 s 作为起始候选；
- 最终值由 E0 和 VM profiling 决定，不能通过把仿真时间压回 3–5 s 来掩盖训练慢。

训练前固定 1/2/4/8 核 profiling，只改变 CPU/线程数，记录 steps/s、墙钟、峰值 RSS
和内存余量。正式训练只使用最快且至少保留 20% 内存余量的配置；训练与评估串行，
内存预算不足在启动前 fail closed。长训进入正式矩阵前必须验证 replay、optimizer、
target network、训练计数器和 RNG 的断点恢复。

## 验收定义

### 目标 A：可稳定运行平台与工程 pilot

只有同时具备以下证据，才可称为“平台做好”：

- D1/D2、队列/在途/守恒、奖励和信息 mask 门禁关闭；
- 真实测量驱动多 OD/突发 trace 能生成且 provenance 可重算；
- 拓扑 cadence 已标定；
- 非学习基线在 VM 上自然结束；
- Q-learning 和 DDQN 在 VM 上分别完成 train → checkpoint → eval；
- 若正式矩阵声称 GAT/MPNN，则相应 contract 也完成 train/eval smoke；
- 没有 OOM、静默回退或缺失 checkpoint 血缘；
- V2 receipt、ledgers、metrics 和 paired analysis 可从原始产物重新计算。

### 目标 B：论文主结论就绪

目标 A 通过后，完成 Q0-I/Q0-F、候选物理特征和逐字段信息年龄，
再根据拥塞诊断提出新方案，完成固定 trace、固定 load、分离 seed 的正式配对实验。
目标 B 只要求覆盖本论文研究范围，不要求实现所有卫星通信物理细节。

## 非目标与防偏移规则

- 不先假定新方案有效；先诊断，再理论，再提出方案。
- 不把 smoke、pilot 或历史 uniform 结果写成论文主结论。
- 不把没有实际 runtime 的模型写入正式实验矩阵。
- 不因训练耗时而擅自缩短物理时间尺度；先 profiling、减少并发、优化执行路径，
  再决定预算。
- 每次只推进一个实验组；该组没有真实产物就不能进入下一组。
