# 查新轮 1 判读报告 — card-02-f2（F-II 供需错配谱结构+全口径击穿点+策略边界）

> fresh-context 判读，仅基于 cards/card-02-f2.md 与 novelty/_raw-r1.json（本卡 queries + anchors 前向引用）。判定依据：标题级筛选，不足以判定者标【存疑-需摘要】。

## 1. 逐查询组判读（9 组）

### Q1 `satellite network latency periodicity spectral analysis`
- 【相邻】crossref `10.1109/csie.2009.545` "Study of Topological Dynamics and Periodicity of LEO Satellite Networks Based on Spectral Analysis" — 对 LEO 网络做谱分析找周期，但对象是**拓扑动态周期**（快照序列的拓扑重复性），不是 QoS/时延指标的谱结构，更无供给侧来源分解。部分覆盖"谱方法"但不覆盖 RQ1 的现象与判别核心。
- 【相邻】arxiv `2603.01172v1` "Measuring Weather Effects and Link Quality Dynamics in LEO Satellite Networks" — 天气-链路质量实测（卡内已作协变量数据集引用），非周期谱分解。
- 其余（Robin 问题谱渐近、椭圆系统谱理论、暗夜天空、脑网络可控性等）【无关】——检索词 "spectral" 漂移到纯数学/其他领域。

### Q2 `Starlink latency periodic component diurnal`
- 【相邻-重点】crossref `10.1109/iwqos70441.2026.11661268` "Inferring Starlink Latency Structure from Public RIPE Atlas Measurements" — 同为 Starlink 时延结构推断（亦出现在锚点前向引用中，见 §2）。标题显示其做"时延结构"推断，可能部分触及周期成分识别，但标题未显示谱级来源分解或 H0 检验。【存疑-需摘要】：需确认其是否已做周期成分归因——若做了 ≥4 格来源分解则威胁创新点 1。
- 【相邻】openalex `10.1145/3748749.3749090` "A Detailed Characterization of Starlink One-way Delay" — Starlink 单向时延细化刻画，同现象（时延波动刻画）；标题未显示周期性/来源分解，判【相邻】，但与上条同属"需摘要确认"高危带。【存疑-需摘要】。
- 【相邻】arxiv `yt00DiRCuk` "Starlink in Northern Europe: A New Look at Stationary and In-motion Performance" — Starlink 性能实测（静止/移动），同对象不同问题（性能基准，非周期谱）。
- 【相邻】arxiv `2005.10855v1` "A Large-Scale IPv6-Based Measurement of the Starlink Network" — Starlink 大规模测量，同对象非同机制判别。
- 【相邻-弱】openalex `10.1049/cmu2.12863` "Self-similar traffic prediction for LEO satellite networks based on LSTM" — LEO 流量自相似/时序结构，预测导向非归因分解。
- 异常标记：arxiv `2310.09242v2` 返回标题 "Modeling and Optimization of Latency in Erasure-coded Storage Systems" 与已知 2310.09242（A Multifaceted Look at Starlink Performance）不符，疑 API 元数据错配；按卡内精读记录该 arXiv 号即本卡锚点本身，非新竞争者。记录备查。
- 其余（TL-DRAM、GLIDS、古地磁、Charlemagne 周期延迟问题等）【无关】。

### Q3 `QoS periodic signature LEO constellation measurement`
- 【相邻】crossref `10.1109/.2006.1629421` "Polar LEO Satellite Constellation Measurement by Delay Probing" — 极轨 LEO 时延探测（2006），早期测量先例；无谱分解、无现代星座、无击穿语义。【相邻】。
- 【相邻-弱】arxiv `2110.12329v4` "Systematic Performance Evaluation Framework for LEO Mega-Constellation Satellite Networks" — 评估框架，非周期归因。
- 其余（星座 QoS 设计/优化一大簇）【无关】——是"设计满足 QoS"，不是"测量 QoS 波动谱结构"。

### Q4 `structural bottleneck localization satellite network`
- 【存疑-需摘要】crossref `10.14722/ndss.2025.230109` "Time-varying Bottleneck Links in LEO Satellite Networks: Identification, Exploits, and Countermeasures" — **时变 LEO 瓶颈链路识别**，与本卡 RQ2"击穿点全口径定位"部分同现象（时变瓶颈）；但 NDSS 安全取向（exploits/countermeasures），机制判别核心（队列保真语义 + 供给侧周期归因）标题未显示。需摘要确认其"识别"是否含供给侧周期归因或队列语义。
- 【相邻】crossref `10.1109/iucc65928.2024.00020` "Bottleneck Link Identification and Capacity Optimization in Satellite Constellations: A Residual Network-Based..." — 卫星星座瓶颈链路识别（残差网络方法），识别但非实测语义击穿定位。【相邻】。
- 【相邻-弱】crossref `10.1145/3589334.3645665` "GAMMA: ... Multi-Bottleneck Localization for Microservices" — 瓶颈定位方法学（微服务域），可作方法参照，现象不同。
- 其余【无关】。

### Q5 `drop-front queue modeling network simulation`
- 无直接答复。无任何标题涉及 Starlink drop-front/共享队列参数（~1500 包、1.33 ms frame drain）在仿真评估或 E2E 换算中的复用——RQ2 换算链未见已做之工作。
- 【相邻-经典】openalex `10.1145/52324.52356` "Congestion avoidance and control"（Jacobson 1988）— 队列管理/AQM 经典，方法学底座而非竞争者。
- 其余（排队论一般建模、社会仿真、交通junction等）【无关】。

### Q6 `unified congestion metric load balancing definition`
- 【相邻】crossref `10.1109/icm.2005.1590064` "Congestion Prediction: from Metric Definition to Routing Estimation" — 明确处理拥塞**度量定义**问题，方向同 RQ3 紧张度统一操作化；但非 LEO、非"以实测击穿相关性为仲裁准则"。覆盖"多口径拥塞度量"但不覆盖本卡评比协议。【相邻】。
- 其余（负载均衡算法综述大簇）【无关】。

### Q7 `on-demand inter-satellite link versus fixed topology applicability`
- 【相邻】arxiv `1812.09128v1` "On-Demand Routing in LEO Mega-Constellations with Dynamic Laser Inter-Satellite Links" — 即卡内已知滚雪球锚点 taes.2024.3415571 的 arXiv 版，已在卡内作 RQ3 第二锚点，非新威胁。
- 【相邻】arxiv `2406.01953v1` "Distributed On-Demand Routing for LEO Mega-Constellations: A Starlink Case Study" — Starlink 案例的按需路由；属策略侧，未见"固定 vs 按需适用域边界 + 实测击穿参照"的判别设计。【相邻】。建议主会话补入 RQ3 相关工作池。
- 其余（ISL 体系结构书章、调制、跟踪误差）【无关】。

### Q8 `supply demand mismatch mega constellation temporal`
- 【相邻-弱】arxiv `0307072v3` "Estimated Demand for Mega-Constellation Internet Service" — 需求侧估计（市场），非网络资源供需错配谱结构。【无关偏相邻】。
- 【相邻-弱】arxiv `1812.09128v1` / `2406.01953v1` 再次命中（同 Q7）。
- 大量生态/经济/灌溉 supply-demand mismatch【无关】——检索词漂移。

### 汇总（Q9 无独立组；共 9 组 queries 均已覆盖判读）
- **直接答复（同现象+同机制判别核心）：0**
- 相邻清单：csie.2009.545（拓扑周期谱）、2603.01172v1（天气-链路）、iwqos70441.2026.11661268（RIPE 时延结构）、10.1145/3748749.3749090（One-way delay 刻画）、Northern Europe Starlink、2005.10855v1、.2006.1629421（早期时延探测）、2110.12329v4、iucc65928.2024.00020、GAMMA、icm.2005.1590064（拥塞度量定义）、1812.09128v1（已知锚点）、2406.01953v1、0307072v3（弱）。
- 存疑-需摘要：iwqos70441.2026.11661268、10.1145/3748749.3749090、NDSS 230109（Time-varying Bottleneck Links）。

## 2. 逐锚点判读（前向引用扫描）

- **ARXIV:2310.09242**（n=20，取 top 6）：无"已做卡上提议之事"。【相邻】"A Cross-US View of Starlink's PoP and Satellite Assignment Strategy to Mobile Users"——PoP/卫星指派策略测绘，与地面段格相关但非谱分解；"The More We Measure, The Less We See"（测量可复现性）——方法学相邻；HERMES（speed test 复用监测）、Planet-Scale IoT via LEO——测量基础设施相邻。均未做 H0 周期检验或来源分解。
- **ARXIV:2601.08439**（n=6）：【存疑-需摘要】"Deciphering Region-Level Signatures from Latency Measurements in LEO Satellite Internet"——"区域级时延签名"与本卡"来源分解表"在目标上有部分重叠风险（区域签名≈空间分解，但非供给侧周期频带分解）；标题不足以判定，需摘要。其余（MPQUIC 视频、分位数预测远程控制、GAN 数据合成、时序预测 MLP）【相邻-弱/无关】——多为"下游应用 2601.08439 的时延结构"，非归因工作。
- **ARXIV:2605.27717**（n=1）：仅命中自身（"Dissecting the StarLink: Characterizing Queuing and Flow Dynamics..."）。**前向引用中无任何工作把该队列参数用于击穿语义/E2E 换算链**——创新点 2 的"自承 future work"方向在前向引用层面确认为空白。
- **DOI:10.1109/iwqos65803.2025.11143359**（n=3）：三条前向引用（RIPE Atlas 时延结构推断、Starlink 队列配置刻画、Service Tiering 指纹）全部是同族测量刻画，无一看做"地面段一阶因子纳入全口径击穿定位 + 路径记录内置"（创新点 3）。其中"Inferring Starlink Latency Structure"与 Q2 存疑条目同文，已列存疑。其余【相邻】。
- **DOI:10.1109/tcomm.2023.3347775**（n=20，取 top 6）：前向引用簇全部是 DRL/启发式 ISL 调度、拓扑控制、RWA——即卡内已判定的"理想化队列下做策略优化"路线；**无一看做"固定 vs 按需适用域边界 + 实测击穿语义参照"或紧张度统一操作化**（创新点 4）。该簇恰好印证本卡 Puzzle 而非杀死它。

## 3.【查新结论】

- **直接答复数：0**。三系统（arXiv/Crossref/OpenAlex）宽检索 + 五锚点前向引用扫描中，未发现任何工作同时覆盖"QoS 谱结构来源分解 + 实测保真队列击穿语义 + 策略适用域边界"三者，也未发现单独完成任一创新点的完整形态。
- **相邻清单**（13 条，见 §1 汇总）：集中在三类——(a) Starlink 时延结构/性能测量刻画（iwqos70441、ICPE'25 One-way delay、Northern Europe、2005.10855、早期 2006 时延探测）；(b) LEO 瓶颈识别（NDSS 230109、iucc 2024）与拥塞度量定义（icm.2005）；(c) 按需 ISL 策略（1812.09128 已知锚点、2406.01953）。全部只占单腿，无 legs 间的判别链。
- **存疑-需摘要：3 条**——`10.1109/iwqos70441.2026.11661268`（RIPE 时延结构推断，最高危：同问题域+同数据源，需确认其是否已做周期归因）、`10.1145/3748749.3749090`（Starlink 单向时延细化刻画，需确认是否含周期成分分析）、`10.14722/ndss.2025.230109`（时变瓶颈链路识别，需确认"识别"语义是否覆盖供给侧归因）。
- **证据等级**：中。依据——(1) 三系统标题级宽检索，非穷尽：仅标题可判，摘要级覆盖未做；检索词覆盖谱/周期/击穿/队列/紧张度/按需 ISL 六腿，但 supply-demand 腿明显词义漂移（经济/生态结果污染），该腿覆盖度低。(2) 锚点扫描覆盖度：2605.27717 仅 1 条前向、2601.08439 仅 6 条，样本薄；2310.09242 与 tcomm 前向各 20 条（top 6 已判）较厚；iwqos 锚点仅 3 条。前向引用窗口天然滞后（引文本身有 1–2 年延迟）。(3) 收录延迟风险：2601.08439、2605.27717 为 2026 年新作，其前向引用尚未成形——**"已做换算链/分解表"的最新工作可能在 2026 投稿潮中尚未被引**；iwqos70441.2026 条目即是该风险的现实例证，建议查新轮 2 对这三条存疑做摘要级复核。
