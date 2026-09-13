# 核心阅读指引（READING-GUIDE，2026-09-11 续作，主控产出）

> 选题交付物 ④。按"先读什么、为什么、核哪一行"组织；所有定位均经逐字核验（核验记录见各条目）。
> 用途：向老师讲方案时的阅读顺序；也是后续论文 related work 的核验底账。
> 入口索引：round/zotero/ZOTERO-INDEX.md（itemKey↔篇名）；VM MinerU MD 路径 /data/liguang13/topic-loop-r2/md/<KEY>/<KEY>/txt/<KEY>.md。

## A. 第一优先：三卡的承重锚（必读，含核验定位）

### A1. S85KQ4FC — Enabling High-Throughput Routing for LEO Satellite Broadband Networks: A Flow-Centric DRL Approach（2024）
**为什么读**：A3 的现象锚 + 最强近邻；唯一把星上推理成本建成一等约束的 LEO DRL 路由工作。
- §III（MD L75–77）：决策器合同——F=8 推理位、决策缓存 M=300 包、到达率扫描 13k–21k pps；**21k pps 时决策时延 17.5ms、丢包 21%**（VERIFY-A3 逐字核）。
- §I（MD L17）：动机自述"推理时延被忽视可能威胁先前结论"；prior works 假设收到包即可立即决策。
- §VI.A（MD L326）：流级复用第 9 批起退化（>60ms、末两批丢包突增）。
- §VI.B（MD L341）：抖动超门限 θ_thr 触发再推理。
- §VII.D.4（MD L453）：θ 太大滞后/太小推理需求回升；Iridium-like 最优 0.005 vs 大规模 0.008（场景漂移自证）。
- §VII.A（MD L385）：R_loss=总丢弃比，**未拆决策/链路双通道**。
- 边界：悬崖数字绑定 i7-11800H 实测合同 + 单路由器口径，禁外推数值。

### A2. CMNCS52M — Traffic-Aware MARL-Based Distributed Routing for LEO（2026）
**为什么读**：C2 的反面教材 + B3 的混淆风险锚；读它是为了学会"同一张表混改多变量"的陷阱。
- §III.B.1（MD L89）：队列占用由正态分布直接采样（外生、无包级到达过程）。
- §VI.A（MD L177）：zone 模型无时间依赖 → 时间特征从状态删除、输入降维。
- §III.B.3（MD L97）：最真实模型也是人口/GDP 驱动的填充率。
- §VI.D（MD L217）：评估=10,000 次传输固定拓扑。
- **勘误（ERRATA-RUN2-01）**：三模型同改 5 变量（空间分布/队列容量/占用率/时变性/状态维度）→ 跨模型数字（15%/70%/55%/40%/20%）只作描述性事实，禁作因果。

### A3. SaTE / JLF7IEBQ — Low-Latency Traffic Engineering for Satellite Networks（2025）
**为什么读**：评估侧最近邻——唯一见到多档强度扫描的工作，但只扫均值。
- §4（MD L232）：1s 粒度泊松流生成器。附录 G（L671）：泊松到达 λp_αp_β。
- §5.4（MD L292）：四档 125/250/375/500 flows/s **均值**扫描——扫描轴只有强度。

### A4. 47J2H748 — Boyan & Littman, Packet Routing in Dynamically Changing Networks（1994）
**为什么读**：Q-routing 原典；"负载变化下适应不对称"的原文实证。
- Adaptation"Load level"段（MD L73）："when network traffic levels were then lowered again, adaptation was much slower"——下调适应更慢，逐字核验。

### A5. TQF59BD7 — IDLB: SDN-Based Load-Balancing Routing Protocol（Roth 等）
**为什么读**：本轮新发现（AUDIT-EXT-C2）——"有工具、被排除"的最硬盲区证据。
- L371 逐字：仿真器同时具备 ON-OFF 与 CBR 会话，"we focus on the latter for more coherent results"。
- L341：自知 "bursty traffic spikes may result in saturated links"。

## B0. 全库审计后的新增必读（AUDIT-FULL-111 产出）

- **JP79GMZS（ELB 2009）的负载模型**：L215 逐字——600 条 ON-OFF 流、Pareto shape 1.2、平均突发/空闲 200ms——**前 RL 时代 LEO 路由评估就用过突发模型**（形状固定，扫描轴是速率 0.8–1.5 Mbps）。讲方案时用它承认"突发不新"，再钉死"RL 时代 + 同均值参数化"的精确空白。
- **CYMQ2GLA（DRL-THSA）**：L65–67——状态含 EWMA 平均输入/输出速率，但**设计意图是滤掉短期波动**（"The short-term light traffic load needs to be filtered"）；是主线状态件的**反意图近邻**：它平滑瞬态，主线暴露瞬态。
- **TSV3IE8S L309（引用级）**：Gragopoulos 等 2000《…LEO under Self-Similar and Poisson traffic》——自相似 vs 泊松对照在 2000 年已存在（全文未取，引用级登记）。
- **S2QZRBEJ（A first look at Starlink performance）**：L129–133——Starlink 实测丢包突发分布——真实网突发存在的测量级支持。

## B. 第二优先：条件轴对照（按轴选读）

| 轴 | 文献 | 读什么 |
|---|---|---|
| 空间分布 | JP79GMZS（ELB, 2009）§I | 城市 vs 农村拥塞不均的动机原文；显式拥塞信令机制（信令型对照原型） |
| 空间分布 | 42E4NAQU（Queue-Aware MARL）L123 | 均匀/人口双强度模式；状态=邻居瞬时 q（无时间语义，A3/C2 共同对照） |
| 时间过程 | LZKNZA8B（Spatial-Temporal Learning）§II.C L66 | NHPP+正弦确定性调制——"时变≠突发"的判别样本 |
| 强度 | SaTE（见 A3 条） | 只扫均值的评估侧代表 |
| 决策资源 | S85KQ4FC（见 A1 条） | 唯一建模推理成本的工作 |

## C. 第三优先：外部近邻与通用机制（防撞车 + 迁移边界）

1. **[Wan25f]** Wang & Leung, Spatial-Temporal RL for Network Routing with Non-Markovian Traffic, arXiv:2507.22174（2025-07-27）——摘要级已核（NEIGHBOR-WAN25F）：通用网络、非马尔可夫流量、STRL 框架；**无同均值合同、非 LEO**。削弱"状态时间语义"新颖性，不覆盖协议件。论文写作前须取全文核其实验合同。
2. **[Shi03]** The Performance of Routing Algorithms under Bursty Traffic Loads（2003，非卫星域）——题录级："突发下评估路由"是老命题；C2 的贡献定位是合同化而非发现现象。
3. **QGAREQUM** — Boosting RL with Strongly Delayed Feedback（通用 RL）§I：观测时延破坏马尔可夫性——A3 半马尔可夫困难的机制级引用（非 LEO 域，禁支撑 LEO 数字）。

## D. 方法论反面教材与工具

- ERRATA-RUN2-01（CMNCS52M 五变量混淆）——单因素纪律的现成教训；C2/B3 的协议锁死清单即由此来。
- round/knowledge/notes-neutral/CMNCS52M-CONFOUND.md——混淆核验笔记。

## E. 本轮未命中登记（避免重复无效检索）

- 热点**迁移**的时变实测：库内 13 篇定向核验 + grep 未命中（A3 §1①.4 清单）；"未命中"仅指本次范围。
- 决策缓存溢出 vs 链路溢出的双通道记账：同上未命中（A3 §6）。
- 同均值过程形状扫描：19 篇审计 0/19（C2 表 2 + AUDIT-EXT-C2）。
