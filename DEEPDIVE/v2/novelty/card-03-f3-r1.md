# 查新轮 1 判读报告：F-III 切片化静态近似误差的坐标依赖结构

- 判读代理：fresh-context（仅读 card-03-f3.md 与 novelty/_raw-r1.json 本卡节）
- 输入：_raw-r1.json "card-03-f3"：6 组查询 × arXiv/Crossref/OpenAlex 各 Top-8，anchors 5 条
- 日期基准：2026-09 检索

## 1. 逐查询组判读

### Q1 "snapshot approximation error time-varying network routing"
- 【无关】其余全部：控制器增益（2311.02473 同 ID 组）、一般路由/缓存、MPLS 带宽画像、快照压缩成像、分布网络重构等——词面撞车（snapshot/time-varying），无一是"离散化静态近似的误差结构"。
- 【存疑-需摘要】2603.01172v1 "Estimating Trotter Approximation Errors to Optimize Hamiltonian Partitioning for Lower Eigenvalue Errors"：量子模拟中对离散化（Trotter）近似误差做估计与分区优化——问题形态（离散化误差的可估计性与分解）与本卡同构，但领域完全不同且无"坐标依赖的误差方向"概念；需摘要确认是否有可迁移的误差估计协议，不至于构成先行。

### Q2 "discretization error direction dynamic network simulation"
- 【相邻】10.1109/wsc60868.2023.10408088 "Choosing the Right Entity Size to Minimize Discretization Error in Discrete Event Simulation Models"（WSC 2023）：同一元问题——离散事件仿真中离散化粒度引入误差并研究如何最小化。差异：通用 DES/实体粒度，非 LEO 时变拓扑，非多坐标（层×指标×Δt）误差符号结构，无连续参考系。
- 【相邻】10.23967/admos.2023.048 "Error estimation (due to discretization and/or modeling)"：离散化/建模误差估计方法学。差异：非网络/非卫星、无方向可预测性问题。
- 【存疑-需摘要】10.1109/wsc.2016.7822095 "Discretization error of reflected fractional Brownian motion"：对反射过程做离散化会产生**有方向的系统偏倚**——"离散化误差非零均值/有符号"的方法论近亲；但对象是随机过程，非网络路由。需摘要确认其误差方向分析是否有可借鉴判别形式。
- 【无关】其余：分子动力学离散化误差、蒙特卡洛、大气同化、DES 输出精度对比、文献计量与软件综述等——领域替换词命中。

### Q3 "time granularity effect satellite routing performance"
- 【相邻】10.1109/cse.2014.93 "A Novel Routing Algorithm Based on Virtual Topology Snapshot in LEO Satellite Networks"：LEO 虚拟拓扑快照路由——正是"消费静态切片"的一类工作，但目的是做路由算法，不度量切片近似误差、无 Δt 敏感性结构。
- 【无关】其余：EV 路径的时间粒度、OpenFlow 转发粒度、LEO 路由算法通类（10.1109/hpsr.2005.1503260 等）、卫星 IoT 综述、DTN 模拟器——均不触及切片误差。

### Q4 "continuous-time reference snapshot comparison LEO"
- 【相邻-弱】2206.06995v2 "Link Reassignment based Snapshot Partition for Polar-orbit LEO Satellite Networks"：LEO 快照划分的使用方，隐含快照边界选择影响性能，但无误差方向/收敛结构分析。
- 【无关】其余：星系 "Leo ring"、快照压缩成像、连续 vs 离散转移率模型（社会学/统计）、连续时间资产配置——纯词面。

### Q5 "temporal graph sampling bias path metrics"（本卡最贴近的相邻族）
- 【相邻】10.70675/68ad0f79ze18bz4661zbc5ez51f6a0c9f3df "Temporal Connectivity and Path Computation for Stream Graph"：连续时间流图上的路径计算理论——本卡"连续参考系"的图论近亲（stream graph 不离散化即定义时序路径），差异：是精确计算理论，不量化"快照化相对连续流的路径度量误差"，也不涉 LEO/仿真。
- 【相邻】1102.4599v1 "Exploring Time Granularity on Temporal Graphs for Dynamic Link Prediction in Real-world Networks"：时间粒度对时序图任务的影响——粒度敏感性现象同族；差异：目标是链接预测效果，非路径/时延指标误差的符号结构。
- 【相邻】2311.12255v2 "Graph Metrics for Temporal Networks"：时序网络指标的定义学（离散 vs 连续时间表示的差异在此有理论讨论）；差异：无 LEO、无近似误差度量协议、无跨层归因。
- 【相邻-综述】2601.03730v1 "A map of approaches to temporal networks"：时序网络方法地图，可能收录"快照序列 vs 连续时间表示"的建模取舍讨论。【存疑-需摘要】：需确认是否明确讨论 snapshot 化引入的度量伪影；若明确且给出系统分类，将压缩本卡的"无人画坐标地图"新颖性声明强度（但不做 LEO 层×指标×Δt 实测，仍非直接答复）。
- 【无关】其余：知识图谱补全、BFS 采样、生态学采样偏倚、攻击图、车辆路径规划——词面。

### Q6 "snapshot interval convergence routing protocol satellite"
- 【相邻】10.1109/milcom.2005.1606129 "Analyzing routing protocol convergence in routed satellite networks"（MILCOM 2005）：卫星网络路由协议收敛分析——与锚点格 1（ieee-11308874）同问题域，是"快照间隔 vs 收敛"最近的历史近亲。差异：按标题看是收敛性能分析，未报告切片误差符号/非单调/跨层对照（需摘要可进一步确证其是否报告了 Δt 敏感性）。
- 【相邻】10.1109/cse.2014.93（同 Q3，快照路由算法）：再次出现，判定同上。
- 【无关】其余：OLSR 建模、MANET 协议、虚拟拓扑路由算法类、联邦学习卫星综述等。

## 2. 逐锚点判读（前向引用）

| 锚点 | n | 前向 Top | 判定 |
|---|---|---|---|
| DOI:10.1109/mswim67937.2025.11308874（锚点格 1） | 0 | — | 无前向引用；无"已做本卡提议"工作 |
| ARXIV:2607.04405（锚点格 2） | 0 | — | 同上 |
| ARXIV:2605.04448（对照模板） | 0 | — | 模板三角（重算间隔轴）尚无人叠加 Δt 轴 |
| ARXIV:2601.21383 | 1 | "Ground-Side Mission Plan Compilation with Policy-as-Code Guardrails for Cloud-Native Satel…" | 【无关】：任务规划编译/护栏工程，不涉切片误差度量 |
| ARXIV:2410.15546 | 1 | "Idle Nodes Detection and Reactivation-Aware-Buffer Management in Delay-Tolerant Network…" | 【无关】：DTN 节点休眠/缓存管理 |

结论：**锚点前向引用中没有任何"已做卡上提议之事"（层×指标×Δt 误差结构地图、连续参考系+留出实测绘校、跨层机制分置归因）的工作**。双锚点过新（2025/2026），前向覆盖为零本身符合预期，但也意味着前向扫描对这两格的排除力弱（依赖收录延迟风险声明）。

## 3. 查新结论

- **直接答复数：0**。未发现"同现象（LEO 切片化静态近似误差）+ 同机制判别核心（层×指标×Δt 坐标决定的误差符号/收敛结构，H1/H2/H3 型判别）"的工作。
- **相邻清单（8 项）**：
  1. 10.1109/wsc60868.2023.10408088（DES 离散化误差最小化，通用仿真）
  2. 10.23967/admos.2023.048（离散化/建模误差估计方法学）
  3. 10.70675/68ad0f79…（stream graph 连续时间路径计算——连续参考系理论近亲）
  4. 1102.4599v1（时间粒度对时序图任务的影响）
  5. 2311.12255v2（时序网络指标定义学）
  6. 2601.03730v1（时序网络方法地图，综述）
  7. 10.1109/milcom.2005.1606129（卫星网络路由收敛分析，锚点格 1 历史近亲）
  8. 10.1109/cse.2014.93 + 2206.06995v2（LEO 快照切片的"消费方"，不度量切片误差）
  共同差异：无一在 LEO 场景下做层×指标×Δt 统一坐标的误差符号/收敛结构测量，无一建连续参考系+实测绘校协议，无一做快照伪影 vs 记账机制的跨层归因分置。
- **存疑清单（3 项，需摘要）**：
  1. 2601.03730v1 "A map of approaches to temporal networks"——综述是否已系统收录 snapshot 化伪影讨论；
  2. 10.1109/wsc.2016.7822095 "Discretization error of reflected fractional Brownian motion"——离散化误差"有方向"的判别形式可迁移性；
  3. 2603.01172v1 "Estimating Trotter Approximation Errors…"——离散化误差估计协议的可迁移性（领域远，风险低）。
- **证据等级**：三系统（arXiv/Crossref/OpenAlex）各 Top-8 宽检索，**非穷尽**——Top-8 截断可能漏掉排序靠后的相关工作；Q5 相邻族提示时序网络理论侧的排除仅到标题级。锚点扫描覆盖度：三个核心引用对象（11308874/2607.04405/2605.04448）前向引用为 0，排除力依赖其被引量增长，**当前为零不代表不存在平行工作**。收录延迟风险：中——双锚点 2025/2026 才出现，同期/更晚的在研工作（尤其 WSC/时序网络社区把离散化误差方法搬到网络仿真）可能尚未被三系统收录或排序命中。综合：**无直接答复，新颖性判断为"未见到在先"，置信度中高（受上述三项存疑与非穷尽限制）**。

---
一行：直接答复 0 + 相邻 8 + 存疑 3
