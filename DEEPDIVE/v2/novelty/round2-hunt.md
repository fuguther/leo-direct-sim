# 查新轮 2 对抗性猎杀报告（round2-hunt）

- 执行者：fresh-context 终稿查新轮 2 猎杀代理（仅读 cards/、novelty/、maps/ 三目录）
- 方法：8 组查询额度全部用完。核验工具：OpenAlex（DOI 解析 + title_and_abstract 过滤）+ arXiv API（布尔检索），组内 sleep 2 节流。
- 判决口径：【杀死】= 在先工作已给出同现象+同判别机制的答复；【压缩】= 在先工作覆盖了本卡某一创新点的实质部分，须收窄/重述声明才存活；【无威胁】= 相邻但不构成答复。
- 攻点：①换社区词表（排队论/控制论/运筹/时序图/移动计算）；②复核轮 1 存疑项（card-02 三条、card-04 六条）。

---

## card-01-fi（F-I 拓扑动态×决策失配 / ρ 失效相图）

### 发现的威胁

**威胁 A（控制论词表：NCS 稳定域×决策间隔——最强压缩线）。** 网络化控制系统（NCS）社区对'以决策/传输间隔为参数的稳定域'是成熟研究对象，其数学形态与本卡 ρ 相图同构：
- OpenAlex 过滤命中 IEEE TAC 2007「A Lyapunov Proof of an Improved Maximum Allowable Transfer Interval for Networked Control Systems」（10.1109/tac.2007.895913）——MATI（最大允许传输间隔）理论即'决策回路间隔 → 稳定性/性能边界'的正式坐标系（Walsh/Bushnell 系 NCS 稳定域经典一脉，非孤立点）。
- 数学侧：delay differential equations 的稳定性判据与时滞诱发振荡（1967「Differential Equations: Stability, Oscillations, Time Lags」、1996「Frustration, Stability, and Delay-Induced Oscillations in a Neural Network Model」）证明'时延轴上的非单调结构（振荡带、失稳边界）'本身不新。

**威胁 B（AoI 词表：卫星网络时延/新鲜度建模已有——压缩'观测状态年龄 instrumentation'）。** arXiv 布尔检索命中：
- 2512.00985v2「Age Optimal Sampling and Routing under Intermittent Links and Energy Constraints」——卫星-地面一体化网络中的年龄最优采样+路由联合设计；
- 2007.05449v1「Information Freshness of Updates Sent over LEO Satellite Multi-Hop Networks」——LEO 多跳 AoI 分析；
- 2602.15145v1「Exploring Performance Tradeoffs in Age-Aware Remote Monitoring with Satellites」——卫星高时延下的年龄-性能折中。

### 证据（id + 标题 + 为何直接答复/为何不是直接答复）

| id | 标题 | 与本卡关系 |
|---|---|---|
| 10.1109/tac.2007.895913 | A Lyapunov Proof of an Improved Maximum Allowable Transfer Interval for Networked Control Systems | 控制论等价物：稳定域以'决策回路间隔'为参数——与本卡 ρ 相图坐标系同构但单回路、线性/非线性小系统、无 LEO 场景、无多环互相过期修正、无'反超带'概念。**压缩（非杀死）**：本卡'相图坐标系'创新须显式限定为 LEO 巨型星座多决策回路（学习/协议/重算/重配置）×实测时标锚定的形态，并声明 NCS 稳定域为理论同源工具（卡 §7 已自列'时滞控制论待查'，本轮部分闭合）。 |
| 2512.00985 / 2007.05449 / 2602.15145 | Age Optimal Sampling and Routing… / Information Freshness…LEO Multi-Hop / Age-Aware Remote Monitoring with Satellites | AoI 社区在卫星网络已有采样/路由/折中建模——'观测状态年龄'的记录与分析有成熟对应物。但这些工作以新鲜度（AoI 值）为代价函数做优化/分析，并非'年龄→决策性能失效模式判别曲线（H1/H2/H3 相图）'。**压缩**：卡 §10 创新点 3 的'全程记录观测状态年龄'须降级为'（AoI 方法作 instrumentation 载体）+（首次把年龄与 LEO 失效相图判别关联）'，避免'从未被记录'的绝对表述。 |

### 判定：压缩（非杀死）

- 三条压缩线（NCS MATI 稳定域 / 时滞诱发振荡数学 / 卫星 AoI 路由）均不构成同现象+同判别机制的答复：无一在 LEO 巨型星座做'决策回路时延向量×拓扑显著变化间隔'的失效相图扫掠，无一检验反超带/崩塌带结构，无一做非同源评估三因子析因。
- 必须做的措辞修正：①'ρ 相图坐标系'首见声明收窄为'LEO 决策系统场景下的首见'，并引 NCS MATI 文献为理论底座；②'振荡失效态'标注为判别性假设（数学上非新，实证上在 LEO 多环场景未测）；③'观测状态年龄全程记录'改写为 AoI instrumentation 的 LEO 场景化。
- 崩塌带（无正例锚点、假设区）维持：本轮未发现任何 LEO 决策系统'信息质量阈值崩塌'的在先实证（AoI 社区做的是年龄阈值优化，非性能崩塌相图）。

---

## card-02-f2（F-II 供需错配谱结构 / 全口径击穿点 / 策略边界）

### 发现的威胁

**威胁 A（本组最强命中）：ICPE'25（ACM）「A Detailed Characterization of Starlink One-way Delay」已做周期成分识别 + 时延成分分离 + 15 s 重配置归因 + 混叠警示。** 摘要全文验证：
- 'reveal minor diurnal latency variation' ——昼夜周期成分已被观测；
- 'provide means to separate out the delay components contributing to the observed one-way delay' ——时延成分**分离方法**已给出；
- 'uplink delays more affected by Starlink's periodic 15-second reconfiguration cycles' ——15 s 重配置周期已作为成因被归因（且指向上行链路各向异性）；
- 'limitations of using too coarse measurement intervals, which can introduce aliasing effects' ——粗采样混叠问题已被点名（与本卡'15 s 混叠必须考虑'动机同源）；
- 开放 OWD 数据集 + 流量生成工具（10 天、5 亿探测包）。

**威胁 B（轮 1 存疑复核）：** 10.1109/iwqos70441.2026.11661268「Inferring Starlink Latency Structure from Public RIPE Atlas Measurements」——OpenAlex 无摘要字段（IEEE'26 新文未入索引），标题级确认其为'Starlink 时延结构推断'（同问题域+同数据源+RIPE 公共数据），**残余威胁需全文复核**：若其已做周期来源分解则进一步压缩 RQ1。

**威胁 C（轮 1 存疑复核）：** 10.14722/ndss.2025.230109「Time-varying Bottleneck Links in LEO Satellite Networks: Identification, Exploits, and Countermeasures」——摘要确认**安全取向**（瓶颈时变特征刻画用于 SKYFALL 攻击分析与链路洪泛防护，非供给侧周期归因、非队列保真击穿语义）→ 降为相邻。

### 证据与判定

| id | 判定 | 理由 |
|---|---|---|
| 10.1145/3748749.3749090（ICPE'25 OWD 刻画） | **压缩 RQ1** | 已做：15 s/昼夜周期识别、时延成分分离、粗采样混叠警示、数据集开源。**未做**：≥4 格供给侧完整分解表（15 s/轨道/昼夜/地面段——轨道格与地面段格缺失）、方差份额量化、'以实测击穿相关性为评比准则'、击穿换算链、策略适用域边界。RQ1 创新点须收窄为'**全口径来源分解表 + 方差份额 + H0（无轨道周期成分）检验**'，'首测周期结构'表述删除。 |
| 10.1109/iwqos70441.2026.11661268 | **压缩（待全文）** | 标题级同域威胁；无摘要可判。风险实质化：IWQoS'26 已有人用 RIPE 公共数据推断 Starlink 时延结构——与卡 RQ1 的数据源（公共实测）重叠。建议投稿前取全文；若其无谱级分解与来源归因则仍为相邻。 |
| 10.14722/ndss.2025.230109 | **无威胁（相邻）** | 摘要证实为攻击面研究；'时变瓶颈识别'与 RQ2 击穿点定位同为主题词但机制判别（队列语义+供给侧归因）与目标（安全 vs 击穿语义）不同。 |
| 排队论词表复检（drop-front/AQM） | **无威胁** | 本轮未发现把'drop-front ~1500 包共享队列'纳入 E2E/会话级击穿换算链的工作；Jacobson 1988（AQM 经典）仍为方法学底座而非竞争者。 |

### 判定：压缩存活

- RQ1（谱结构来源分解）被 ICPE OWD 刻画实质压缩：周期成分识别+成分分离+15 s 归因已先行，必须收窄至'全口径（≥4 格）方差份额分解 + H0 检验 + 击穿关联'，并引 ICPE 为直接在先（差异化=分解表完整性+份额量化+击穿语义）。
- RQ2（击穿点全口径定位）/ RQ3（策略边界）未受威胁：轮 1 与轮 2 均未见 drop-front 击穿换算链、固定 vs 按需策略适用域边界以实测击穿为准的在先工作。
- 残留风险：iwqos70441（IWQoS'26）待全文复核。

---

## card-03-f3（F-III 切片化静态近似误差的坐标依赖结构）

### 发现的威胁

**威胁 A（时序图/时间聚合词表——压缩线，非杀死）。** 时序网络社区对'时间粒度/聚合窗口影响网络指标'已有既有讨论（轮 1 已列：1102.4599 时间粒度对时序图任务影响、2311.12255 时序网络指标定义学、10.70675 stream graph 连续时间路径计算、WSC 2023 DES 离散化误差最小化）。本轮换词表（time aggregation/bias/direction）复检：
- arXiv 布尔检索（'time aggregation' AND 'temporal network' AND metrics/bias）0 命中——说明**该词表下无直接打中'聚合窗口→误差方向/幅度地图'的实证**；
- OpenAlex 过滤命中为生态学/医学等噪声，无网络路由/仿真域的先在；
- 轮 1 存疑项未获升级：Trotter 离散步（2603.01172v1）、reflected fBm 离散化符号偏差（wsc.2016.7822095）、时序网络方法地图（2601.03730v1）均无摘要级升级证据。

**威胁 B（控制论/数值分析词表）。** 离散化误差方向（高估/低估）在数值分析/DES 社区有零散方法学先例（WSC'23 DES 实体粒度、ADMOS'23 误差估计），但均为通用仿真方法学，无 LEO 场景、无层×指标×Δt 坐标结构地图、无连续参考系+留出实测绘校协议。

### 证据与判定

| id | 判定 | 理由 |
|---|---|---|
| 1102.4599v1 / 2311.12255v2（轮 1 复判） | **压缩（声明侧）** | '时序图粒度影响指标/指标定义学'社区已有讨论——卡'无人画坐标系'的表述须限定为'**LEO 网络仿真/接触计划域 + 连续参考系 + 实测绘校**的组合首见'，并引该社区为方法论近邻。 |
| WSC 60868.2023.10408088（DES 离散化误差） | **无威胁（相邻）** | 通用 DES 实体粒度最小化，无 LEO、无误差符号坐标结构、无跨层归因。 |
| 本轮新检索 | **无威胁** | 时间聚合/偏倚词表下无直接答复命中；锚点（11308874/2607.04405）前向引用仍为 0（数据源同轮 1，无新吸收者）。 |

### 判定：压缩存活

- 双锚点的层×指标×Δt 坐标结构地图、连续时间参考系、留出实测绘校、快照伪影 vs 记账跨层分置归因——联合体未被任何社区在先工作覆盖。
- 须做的措辞修正：将'无人画坐标地图'限定到 LEO 仿真/接触计划域，并显式引用时序网络粒度效应文献（1102.4599/2311.12255）与 DES 离散化误差文献（WSC'23）划清坐标差异，防止审稿人以'时序网络社区已有粒度敏感性研究'砍新颖性声明。
- 无杀死证据：未发现任何工作在同一坐标系（层×指标×Δt）下测量 LEO 切片误差符号/收敛结构。

---

## card-04-n1（N1 实测动态盲的 RL 路由评估）

### 发现的威胁（轮 1 六条存疑全部复核）

| 存疑项 | 轮 2 证据（摘要级） | 判定 |
|---|---|---|
| 10.1109/netsoft70012.2026.11603525「Hybrid Table-Assisted and RL-Based Dynamic Routing for NGSO Satellite Networks」 | 摘要全文：预计算路由表 + DQL 回退的混合策略，**'Simulation results in large-scale NGSO networks'** ——纯仿真、无实测队列/重配置/PoP 注入，无重评估议程 | **无威胁（相邻）**：与池内 2509.14909 方法族同类，非'实测动态重审 RL 结论'。 |
| 10.1109/icmlcn59089.2024.10624807「Q-learning for distributed routing in LEO satellite constellations」 | 摘要全文：POMDP 分布式 Q-learning，基线含'instantaneous queueing delays available at all satellites'的 genie 算法——**纯仿真**，genie 基线恰是假设即时状态（与卡 N1 的'信息新鲜'批判对象同侧） | **无威胁（相邻）**：方法论文，非评估保真度研究。 |
| arXiv 2604.27478v1「Toward Scalable SDN for LEO Mega-Constellations: A Graph Learning Approach」（2601.13662 前向） | 摘要全文：GNN 表示星座拓扑 + Koopman 线性化，目标为可扩展网络管理架构——非 RL 路由重评估 | **无威胁（相邻）**。 |
| 10.2139/ssrn.5798349（=5274748 重复收录）「Expert-driven Jumpstart RL for Managing Network Congestion Control」 | OpenAlex 无摘要；标题级=拥塞控制 RL（传输层 CC 域，非 LEO 路由重评估；SSRN 预印本） | **无威胁（相邻-弱）**：域不同，即使其用实测 traces 评测，也是 CC 域评估先例，非'LEO RL 路由结论重审'。 |
| 10.61951/sciencepaperonline.202401.0007「Traffic Engineering in Segment Routing Network Based on DRL」 | OpenAlex 无摘要；标题级=地面 SR 网流量工程（非卫星、非把关实测动态） | **无威胁（相邻-弱）**。 |
| 「A Cross-US View of Starlink's PoP and Satellite Assignment Strategy to Mobile Users」（2310.09242 前向） | arXiv 标题检索未命中原文；OpenAlex 返回泛化结果（Dissecting SNOs 等）——无摘要可判 | **无威胁（相邻）**：测量侧策略测绘，无 RL 评测议程；即使全文也至多供给 PoP 参数（卡已自持该参数，无新增）。 |

### 本轮新增检定

- 跨域同范式最强压缩已在轮 1 锁定（2608.20575 URB 车联网真实感 RL 路由基准）——**'真实感基准重审 RL 路由'范式的首个声明须限定为 LEO 卫星域**，本轮无新竞争者。
- 锚点前向引用（2310.09242 20 条 / 2605.27717 1 条 / 2604.12382 0 条 / 2601.13662 1 条）在轮 2 复检中未见任何'把实测动态注入 RL 训练/评测'的闭环工作——Puzzle 段'两社区脱节'证据维持。

### 判定：无威胁（存活）

- 六条存疑全部降为相邻/弱相邻；无任何条目构成'同现象（实测动态重审 RL 路由）+ 同机制（保真度梯度注入重测排序/增益）'的直接答复。
- 现象段'47 篇池内无一篇纳入实测动态'未被证伪；识别出的新增邻域（NGSO 混合表+RL、LEO SDN GNN）均属'新方法含理想化仿真评测'路线，恰印证 Puzzle 而非法案。
- 保留的边界声明：①'首个'必须限定卫星域（URB 车联网先例）；②SSRN/无摘要条目按标题级处理，投稿前对 2026 新文（含 iwqos70441、ICPE）作全文级复核。

---

## 总判定

| 卡 | 判定 |
|---|---|
| card-01-fi | **压缩存活**（NCS MATI 稳定域/AoI 卫星路由/时滞振荡数学三条压缩线；相图核心+H1/H2/H3 判别+非同源析因协议未被在先工作覆盖，须加 LEO 场景化限定与理论底座引用） |
| card-02-f2 | **压缩存活**（ICPE'25 OWD 刻画已做周期识别+成分分离+15 s 归因+混叠警示 → RQ1 收窄为全口径分解表+份额量化+H0 检验；RQ2/RQ3 存活；iwqos70441 残留威胁待全文） |
| card-03-f3 | **压缩存活**（时序网络粒度效应/DES 离散化误差为方法论近邻，组合首见限定在 LEO 仿真/接触计划域+连续参考系+实测绘校；无杀死证据） |
| card-04-n1 | **存活**（六条存疑全部降相邻；无直接答复；'首个'声明须限定卫星域） |

一行返回：card-01 压缩存活 ｜ card-02 压缩存活 ｜ card-03 压缩存活 ｜ card-04 存活