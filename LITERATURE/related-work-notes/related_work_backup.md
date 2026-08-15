# Related Work Matrix（含深度笔记）

> **Status**: 2026-04-13。矩阵为速览；**RW-001–006** 摘要与实验设计评价见下文 **Part II**（原独立竞品分析文档已并入本文档，避免双文件漂移）。RW-005（Q-learning baseline; 无reroute failure分析）为精读；RW-006为精读（classical SDN baseline；信息范围对照实验）。

---

## Part I — 矩阵（按类别）

### Category 1: DRL Routing in LEO/Satellite Networks

| Paper | Method | Evaluation | Our Gap | Differentiation |
|-------|--------|------------|---------|-----------------|
| **RW-001** — Multi-Agent Deep Reinforcement Learning for Distributed Satellite Routing (2024)<br>arXiv:2402.17666<br>Authors: Federico Lozano-Cuadra, Beatriz Soret | MA-DRL；两阶段（离线全局DNN + 在线本地预训练DNN）；部分环境知识 + 邻接智能体反馈 | 摘要未提及 seed 数 / 统计 / reward shaping 消融 | **无 reward shaping 消融实验**；关注架构而非 reward 设计 | Our paper: DDQN with explicit balance term reward shaping; controlled train-eval ablation |
| **RW-002** — An Open Source MA-DRL Routing Simulator for Satellite Networks (2024)<br>arXiv:2407.11047<br>Authors: Lozano-Cuadra, Thorsager, Leyva-Mayorga, Soret | 开源 SimPy 仿真器；支持 Dijkstra / Q-Routing / MA-DRL；可配置流量 / 拓扑 / 通信参数 | 高度可配置；seed 数 / 统计待全文验证 | **仿真基础设施，非竞争论文**；无 reward shaping 评估 | Our paper: focuses on reward shaping evaluation with controlled experiments |
| **RW-005** — Q-Learning Based Dynamic Distributed Routing Scheme for Mega LEO Satellite Networks (2023)<br>Chinese J. Aeronautics 36(2):284–291<br>Authors: Huang, Wu, Kang, Mu, Huang, Wu, Tang, Cheng | Q-learning（tabular，无experience replay/target network）；1-hop邻居状态；MORL双目标（延迟+队列长）；Walker Delta 288–1152节点 | 无reroute failure分析；Q-learning收敛性未与DDQN对比 | **Q-Routing早期baseline**；与Roth RW-001共享1-hop状态局限；无failure-mode分析 | Our paper: DDQN（有experience replay + target network）；分析reroute failure机制 |
| [NOT FOUND] — Additional DRL LEO routing papers (2022–2026) | arXiv API 搜索未命中；需人工补充 | — | — | — |

### Category 2: DRL Routing in Terrestrial/General Networks

| Paper | Method | Evaluation | Our Gap | Differentiation |
|-------|--------|------------|---------|-----------------|
| **RW-004** — Reinforcement Learning-Based Adaptive Load Balancing for Dynamic Cloud Environments (2024)<br>arXiv:2409.04896<br>Author: Kavish Chawla | RL 自适应负载均衡（云计算） | 待全文验证 | 领域不同（cloud vs LEO）；无卫星特异约束 | Our paper: LEO ISL 约束下的负载均衡路由 |
| [NOT FOUND] — Additional terrestrial DRL routing papers | arXiv API 搜索未命中 | — | — | — |

### Category 3: Reward Shaping / RL for Load Balancing

| Paper | Method | Evaluation | Our Gap | Differentiation |
|-------|--------|------------|---------|-----------------|
| [NO LEO-SPECIFIC PAPER FOUND] — No paper specifically evaluates reward shaping for load-balancing in LEO satellite routing | — | — | **This is the core research gap** | Our paper directly addresses this |

### Category 4: LEO Constellation Routing (non-RL)

| Paper | Method | Evaluation | Our Gap | Differentiation |
|-------|--------|------------|---------|-----------------|
| **RW-003** — Joint Satellite Gateway Placement and Routing for Integrated Satellite-Terrestrial Networks (2020)<br>arXiv:2002.03071<br>Author: Nariman Torkzaban | 网关放置 + 路由联合优化；传统方法（非 DRL） | 最小化网关部署成本 + 延迟约束 | 方法路线不同（优化 vs DRL）；网关放置非在轨决策 | Our paper: 在轨实时 DRL 路由决策 |
| **RW-006** — IDLB: An SDN-Based Load Balancing Routing Protocol for Autonomous Satellite Constellation Networks (2025)<br>Int. J. Satellite Commun. Netw., Wiley<br>Authors: Roth, Brandt, Bischl, Fernandez Pinas, Acar | 分布式SDN；每cluster一个机载控制器；动态best-of-k路径算法；**非RL** | 自建C++/Python系统级仿真器；SCN-288/1440；QoS合规率 vs 网络负载 | **经典基准**：SDN控制器拥有cluster内全局链路利用率状态；为分布式DDQN的"信息范围不足"诊断提供对照实验 | Our paper: DDQN逐跳决策；IDLB=对照实验（信息范围大→启发式即可工作）；两者组合说明**state scope是主因** |
| [NOT FOUND] — Additional non-RL LEO routing papers | — | — | — | — |

---

## Synthesis / Gap Analysis

1. **Reward shaping for load-balancing is underexplored in LEO DRL routing**（RW-001/002 重 MA 架构，无 balance reward 消融）。
2. **Controlled evaluation of load-balancing reward is lacking。**
3. **RQ 表述**：在匹配流量下，显式 balance term 能否改善 LEO 路由决策质量？须严格 train–eval 与多 seed。
4. **RW-006 信息范围对照**（2026-04-13精读）：IDLB用分布式SDN cluster控制器实现cluster内全局链路利用率感知，best-of-k启发式在SCN-288上达到97.4%吞吐量提升（vs无负载均衡source routing）。成功原因：SDN控制器拥有 `ut(i,j) = ft(i,j)/ct(i,j)` 对cluster内所有链路的完整视图。这正是1-hop DDQN agent所缺乏的。**诊断**：DDQN的"可换路但未换路"更可能是**state不足**（看不到下游saturation）而非reward shaping问题。CL-DC（Roth 2024）在RW-006中没有实现评估，两者为并行track。

---

## Part II — 文献深度笔记（原「竞品深度分析」合并节）

> 数据来源：arXiv API（Python urllib，2026-04-12）。全文细节以 PDF 为准。

### 研究景观（Research Landscape）

#### 已验证论文（2026-04-12 抓取）

| ID | 论文 | 年份 | arXiv | 方法定位 | 与本项目关系 |
|----|------|------|-------|----------|------------|
| **RW-001** | Multi-Agent Deep Reinforcement Learning for Distributed Satellite Routing | 2024 | 2402.17666 | MA-DRL，两阶段（离线全局 DNN + 在线本地预训练 DNN） | 同门；MA vs 单智能体 DDQN；**无 reward shaping 消融** |
| **RW-002** | An Open Source Multi-Agent DRL Routing Simulator for Satellite Networks | 2024 | 2407.11047 | 开源 SimPy；Dijkstra、Q-Routing、MA-DRL | 基础设施；**无 reward shaping 评估** |
| **RW-003** | Joint Satellite Gateway Placement and Routing… | 2020 | 2002.03071 | 网关放置 + 路由联合优化（非 DRL） | 路线不同 |
| **RW-004** | RL-Based Adaptive Load Balancing for Dynamic Cloud Environments | 2024 | 2409.04896 | 云负载均衡 RL | 方法参考；领域不同 |
| **RW-005** | Q-Learning Based Dynamic Distributed Routing Scheme for Mega LEO Satellite Networks | 2023 | 本地PDF | Q-learning tabular；1-hop状态；MORL双目标 | **Q-Routing早期baseline**；Roth RW-001的祖先；reroute failure未被分析 |
| **RW-006** | IDLB: An SDN-Based Load Balancing Routing Protocol… | 2025 | 无（非arXiv） | 分布式SDN；cluster内全局链路利用率；best-of-k启发式；非RL | **信息范围对照实验**；同SCN-288拓扑；解释为何DDQN局部状态不足 |

#### 研究空白（文献侧）

1. LEO DRL 路由中 **load-balancing reward shaping** 未被系统评估。  
2. **受控单智能体 DDQN + 显式 balance term** — 未见同类工作。  
3. 显式 balance term 能否改善 LEO 决策质量 — **须本仓库协议回答**（与 `docs/TEAM_HANDOFF.md` 一致：先审平台再写强结论）。

### 代表论文 A：RW-001（2402.17666）

| 字段 | 值 |
|------|-----|
| 标题 | Multi-Agent Deep Reinforcement Learning for Distributed Satellite Routing |
| 作者 | Federico Lozano-Cuadra, Beatriz Soret |
| 方法 | MA-DRL；每星独立智能体；离线全局 DNN + 在线本地 DNN |

**核心摘要（原文节选）**：*"Each satellite is an independent decision-making agent with partial knowledge… offline exploration… global DNN… online exploitation… local pre-trained DNNs."*

**实验设计评价（摘要级）**：Train/Eval 分离、多 seed、reward shaping — **摘要未支撑，须 PDF**；**无负载均衡 reward 项描述**。

**启示**：对象重叠；本项目走 **单智能体 DDQN + balance term** 与 RW-001 架构不同；**消融空白真实存在**。

### 代表论文 B：RW-002（2407.11047）

| 字段 | 值 |
|------|-----|
| 标题 | An Open Source MA-DRL Routing Simulator for Satellite Networks |
| 方法 | SimPy；Dijkstra / Q-Routing / MA-DRL |

**摘要要点**：事件驱动包、队列与时延跟踪；高度可配置。

**评价**：**工具论文**；无 balance reward 评估；queue/latency 与 `docs/METRICS_DEFINITION.md` 口径可对齐引用。

### 代表论文 C：RW-005（Huang 2023，Chinese J. Aeronautics）

| 字段 | 值 |
|------|-----|
| 标题 | Q-Learning Based Dynamic Distributed Routing Scheme for Mega LEO Satellite Networks |
| 作者 | Yixin Huang, Shufan Wu, Zeyu Kang, Zhongcheng Mu, Hai Huang, Xiaofeng Wu, Andrew Jack Tang, Xuebin Cheng |
| 方法 | Q-learning（tabular）；1-hop邻居状态；MORL双目标（delay + queue length）；ε-greedy exploration |

**核心设计（原文）**：QRLSN使用plain Q-learning更新（无experience replay，无target network）；状态 = (当前节点, 下一跳, 目的地)；MORL奖励向量 = [fr1(延迟), fr2(队列长)]，加权求和。

**关键发现**：QRLSN在k≥20（高负载）时优于VT-SPR静态最短路径；在k=5（低负载）时劣于VT-SPR（探索开销不划算）。

**实验设计评价**：Walker Delta 53°/550km；288–1152节点；STK+NetworkX；1000 episodes训练；与我们的4GT仿真不可直接比较（工具不同）。

**与本项目RQ的关系**：Huang (2023) 是 Roth (2024) 的方法祖先——两者均用1-hop状态 + tabular Q-learning。**关键区别**：Roth明确分析了"sub-optimal last hop"失败模式；Huang仅声称"可避免拥塞"，**未分析reroute failure**。Huang的结论"in-depth research on congestion awareness will be the focus"正是本项目RQ的核心。

### 跨论文模式（摘要级）

| 特征 | RW-001 | RW-002 | RW-003 | RW-004 | RW-005 | 本项目 |
|------|--------|--------|--------|--------|--------|--------|
| LEO 背景 | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
| DRL | MA | MA | ❌ | RL | Q-learning（tabular） | DDQN |
| Train–eval | 待全文 | 待全文 | N/A | 待全文 | ✅（1000 episodes） | 协议要求 |
| Reward shaping / 负载均衡 | ❌ | ❌ | N/A | 部分 | 队列长衰减（emergent） | **显式balance term** |
| reroute failure 分析 | ✅（sub-optimal last hop） | ❌ | ❌ | ❌ | ❌ | **核心** |

### 写作提示（避免夸大）

| 表述 | 推荐 | 避免 |
|------|------|------|
| 效果 | 报告 pp 与 seed 数 | 「显著优于」无检验 |
| 局限 | 写清 n 与场景 | 省略污染/可比性 caveat |

### 附录：arXiv 条目标识

| ID | arXiv | 标题简写 |
|----|-------|----------|
| RW-001 | 2402.17666 | MA-DRL Distributed Satellite Routing |
| RW-002 | 2407.11047 | Open Source MA-DRL Routing Simulator |
| RW-003 | 2002.03071 | Gateway Placement and Routing |
| RW-004 | 2409.04896 | RL Load Balancing Cloud |
| RW-005 | 本地PDF（Chinese J. Aeronautics 2023） | Q-Routing Baseline Mega LEO |

---

**维护**：文献增量只改**本文件**；勿再建平行「竞品报告」路径。
