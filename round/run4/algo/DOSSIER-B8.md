# DOSSIER-B8 — T3 证据级定读（16 篇：测量/平台/AoI）

- 批次：T3 → B8（定档表 `round/run4/algo/TIER-ASSIGNMENT.md` L75–L90，档位定义 L127）。
- 阅读深度（L127 原文）：**"读摘要+方法+结果+结论；产出可引用事实与数字含行号、测量条件、对负载/突发/时延/到达率的事实贡献、可否作定标或现象证据、边界"**。
- 证据源：VM MinerU Markdown，路径 `/data/liguang13/topic-loop-r2/md/<itemKey>/<itemKey>/txt/<itemKey>.md`；所有行号均为该 MD 文件行号，引文逐字（保留原文拼写错误，如 "dificult"/"Paterns"）。
- 本批 16 篇（顺序按定档表 L75–L90）：GGFJ3SEG、S2QZRBEJ、NPF75WS5、P6XJZNQK、L63JISQN、GJJQUMQ2、5HJ8ATR7、AZ72LM9Z、W6M3GU7L、DS9SPARV、IEI3BYFF、8AYW2Y78、4QG5VYHQ、BLFJ6CLV、GV9PPNZT、R5QTFKD2。
- 红线执行：每条带行号+逐字英文；公式逐字抄 LaTeX；判"未见"均附检索词与检索范围；负载/流量/评测设置只作条件登记。
- 全局检索词（用于各篇"未见"判定）：`arrival|offered load|load factor|burst|inter-?arrival|packet rate|traffic intensity|Erlang|congestion level`（大小写不敏感，grep -n -i -E，范围=该篇 MD 全文；逐篇若另有增补检索词会另行标注）。

---
## 1. GGFJ3SEG — Democratizing LEO Satellite Network Measurement

**书目事实（逐字）**：L1 `# Democratizing LEO Satellite Network Measurement`；L3–L11 作者 Liz Izhikevich / Manda Tran / Katherine Izhikevich / Gautam Akiwate / Zakir Durumeric（Stanford / UCSD）；L21 `Proc. ACM Meas. Anal. Comput. Syst. 8, 1, Article 13 (March 2024), 26 pages. https://doi.org/10.1145/3639039`。
**已读范围**：L1–L342（正文全部：摘要 L13、引言 L23–L33、背景 L35–L69、相关工作 L71–L89、方法 L91–L156、评测 L158–L225、全球时延分析 L227–L315、局限 L317–L329、结论 L331–L337）+ 附录清单 L503–L546 的标题级确认（附录正文未逐段读，见第 5 项边界）。参考文献 L343–L501 未读（不属证据范围）。

### 1) 测量/建模对象与条件（逐字+行号）

- L13（摘要，对象与规模）：`In this paper, we introduce HitchHiking, a methodology that democratizes global visibility into LEO satellite networks. HitchHiking builds on the observation that Internet-exposed services that use LEO Internet can reveal satellite network architecture and performance, bypassing the need for specialized hardware.` … `With HitchHiking, we complete the largest study to date of Starlink network latency, measuring over 2,400 users across 27 countries.`
- L29（三步法）：`HitchHiking works in three steps (1) find measurable endpoints that use LEO satellites for Internet connectivity, (2) identify where in the network path LEO satellites are used, and (3) measure (i.e., “hitchhike”) the satellite link.`
- L131–L152（10 步流水线，逐步骤条件）：
  - L131 `1. Collect Exposed Services To find measurable LEO-hosted Starlink services, we collect IPv4 and IPv6 exposed services in the Starlink network (AS 14593) using Censys [46], a public Internet device search engine.`
  - L133 `we include only IP addresses whose DNS PTR record follow the Starlink customer format: customer.[location].pop.starlinkisp.net.`
  - L142 `To obtain an approximate geographic location of a Starlink service, we use Starlink’s IP Geolocation feed [29].`
  - L148 `We measure path latency for 5 minutes sending two ICMP pings every second with the following additional configuration: (1) with a TTL equal to the terrestrial hop-router-hop number and (2) with a TTL equal to the exposed-service hop number. Notably, only one probe traverses the satellite link during each measurement, thereby minimizing ethical concerns.`
  - L150 `We subtract the terrestrial-hop router RTT from the exposed service router RTT, to measure the satellite link and minimize terrestrial artifacts.`
  - L152 `We apply a smoothing filter with a window size of 15 seconds (the time-step with which Starlink dishes stay connected to a satellite, before determining whether to switch connections [12]) to our timeseries of collected measurements, to eliminate short-lived artifacts`
- L164（地面真值装置）：`To obtain ground truth about a client’s LEO network latency, we deploy our own residential generation 2.0 Starlink dish in San Diego.`
- L173（地面真值口径）：`We also collect Starlink provided metrics from our dish every second, including the reported “POP ping latency,” packet drop, and estimated bandwidth usage. The POP ping latency is the ground truth RTT of a ping from our dish to the assigned POP. The POP ping latency is the most granular provided metric of LEO latency; it includes terrestrial latency to and from the ground station.`
- L175（对照条件）：`we run HitchHiking from four geographic locations: Australia, Brazil, California (US), and Virgina (US). Each location is 500–8,000 miles away from our dish. All HitchHiking pipelines run at the same time on May 12, 2023, sending probes every second for 5 minutes. We note the presence of clear skies and no physical obstructions, and thus minimal interference during our experiment.`
- L233（全球测量窗口与样本口径）：`We use the HitchHiking methodology (Section 5) to collect Starlink latency data between May 18–June 23, 2023.` … `We filter the initial 3.5K exposed customer Starlink IPs for jittery pre-satellite hops, leaving 2.4k IPs that host exposed services.`
- L194（仿真对照对象）：`We consider two LEO simulators: (1) the most widely-used, Hypatia [57] and (2) the newest, StarryNet [58].`；L203 `To model Starlink latency, we configure Hypatia with the Starlink constellation parameters published by the FCC [25].`；L203 `we add the latency that a packet would incur traveling at 2/3rds the speed of light (i.e., estimated optical fiber latency [44]) between the ground station and POP.`
- L195（未能做的对照）：`Unfortunately, we cannot evaluate against StarryNet because it requires over 2 TB of RAM to simulate Starlink and is not able to run in cloud environments`

### 2) 可引用的事实与数字（逐字+行号，含单位与口径）

| # | 事实（逐字） | 行号 | 口径 |
|---|---|---|---|
| 1 | `measuring over 2,400 users across 27 countries` | L13 | Starlink 客户数/覆盖国家 |
| 2 | `we identify a total 4,521 exposed services across 2,051 unique IPs (hosts), 857 unique ports, and 47 application layer protocols in the Starlink network.` | L135 | 2023-05-10 单日快照 |
| 3 | `After filtering for customer endpoints, 1,790 unique IPs remain.` | L138 | 客户端点过滤后 |
| 4 | `Filtering for Peplink removes 9% of all services (1,629 IPs remain).` | L140 | PEP 排除后 |
| 5 | `96% of reported RTT times are within one standard deviation (10 ms), and 50% of RTT times are within 3 ms of the ground truth (i.e., the dish’s pop ping latency).` | L177 | 精度口径=与 POP ping 地面真值之差 |
| 6 | `HitchHiking captures 100% of all sustained RTT spikes, which we define as latencies over two standard deviations away from the median that last at least 15 seconds (i.e., the Starlink minimum amount of time dishes stay connected to the same satellite [12]).` | L177 | "sustained spike" 定义（>2σ 且 ≥15 s） |
| 7 | `HitchHiking observes only one false-positive RTT spikes across our cumulative 10,000 second measurement period.` | L179 | 假阳（累计 10000 s） |
| 8 | `configuring Hypatia to use the second nearest ground station produces a latency prediction that on average is only 7.6 ms in error relative to the ground truth. Nevertheless, HitchHiking RTTs are on average 1.8 times more accurate than Hypatia.` | L207 | 仿真误差口径=平均绝对误差 ms |
| 9 | `HitchHiking is up to 80% more accurate` | L160 | 相对 Hypatia |
| 10 | `Given that 20% of ground truth RTT fall below the second-nearest ground station best-case RTTs, Starlink must be connected to the nearest ground station at least 20% of the time.` | L211–L213 | 反推地面站选择比例（下界） |
| 11 | `Hitch-Hiking has 45 times more exposed services than RIPE Atlas, whose services are located across 22 cities, 14 countries, and 4 continents. Hitch-Hiking finds exposed Starlink services across 43 cities, 27 countries, and 6 continents.` | L219 | 覆盖度对比 |
| 12 | Table 1 Total 行：`<td>Total</td><td>2473</td><td>54</td><td>43</td><td>22</td>` | L221 | HH 2473 IP / 43 城市；RA 54 IP / 22 城市 |
| 13 | `The majority (68%) of HitchHiking found services use POPs in the US` … `the fact that 60% of Starlink customers are located within the US [31]` … `Germany (11%), Australia (9%), and England (5%)` | L225 | POP 归属占比 |
| 14 | `the minimum round trip time (RTT) for a packet to route through a GEO satellite is 480 ms, physically bounded by the speed of light` | L37 | GEO 下界 |
| 15 | `LEO satellites’ closer distance provides significantly lower theoretical latency (≈10 ms RTT)`；`orbit 180 to 1,300 miles from Earth`；`orbiting the earth every 90 minutes` | L42 | LEO 理论下界/轨道参数 |
| 16 | `ISL deployment provides coverage to clients in extreme remote locations (e.g., in oceans) that are in view of a satellite (e.g., within 600 miles)` | L62 | ISL 覆盖半径口径 |
| 17 | `we find that spikes occur in multiples of 15 second—aligning with Starlink’s reported satellite reconfiguration period [12]` | L190 | 时延尖峰的时间量子 |
| 18 | `Across the entire measurement period, 2/5 sustained RTT spikes occur while still connected to the same satellite. For standard RTT spikes (i.e., spikes over one—but not two—standard deviations above the median), 5% occur while still connected to the same satellites.` | L189 | 尖峰与"切换卫星"的耦合比例 |
| 19 | `In the worst case, a customer from the US Virgin Islands is assigned to their nearest POP, in Atlanta, Georgia, located roughly 1600 miles away. They experience a minimum RTT nearly twice as large compared to customers that are closer to their own POP.` | L244 | 距 POP 距离→最小 RTT |
| 20 | `Over 70% of customer RTTs fall below Min(ISL-NG), indicating that in the majority of cases the customer falls below the theoretical minimum latency of using two satellites to route to the nearest ground station, and therefore must be using single-hop relay routed to the nearest ground station.` | L276 | 单跳 relay 占比（下界） |
| 21 | `However, one-third of the time, the Nigerian customer’s RTTs increase between 2–5 fold the median` | L280 | 尖峰倍数 |
| 22 | `the outlier latency (162 ms) near second 350` … `it would take at least 154 ms for a Nigerian POP customer to route through the nearest non-Nigerian ground station, in Lepe, Spain (Figure 10c). The Nigerian customer’s terrestrial route from the Spanish ground station would span over 4970 miles` … `when accounting for potential additional latency due to bad satellite selection (12ms) and an indirect ISL routing path (13 ms), the total RTT is within 5 ms of the second highest sustained peak at second 300.` | L280 | 逐项时延归因分解（ms / miles） |
| 23 | `The Seychelles yacht’s experiences a minimum RTT of 181 ms (6 times worse than Palm-Oil-Farm Customer’s minimum RTT) indicating that it is theoretically improbable that ISLs are using a direct path` … `a direct speed of light path from Seychelles to the Nigerian POP would take an RTT of 40 ms, and no more than 80 ms to account for potential “zig-zag” paths between satellites [57]` … `during 42% of our measurement period, the yacht’s RTT is 150 ms over its minimum RTT.` | L287 | 最小 RTT、光速下界、超出量占比 |
| 24 | `Sustained latency spikes are widespread and constant; at least 70% of customers experience at least one sustained latency every day during our month-long 5 minute data collection.` | L289 | 日均出现率 |
| 25 | `Average RTTs vary by over 500%: from 28 ms (Mexico)–149 ms (Nigeria). Standard deviation of RTTs also vary by an order of magnitude: from 4 ms (Mexico)–109 ms (Nigeria).` | L293 | 跨 POP 平均 RTT/标准差 |
| 26 | `median latency decreases by 25%, from roughly 400 ms to 300 ms` | L295 | 尼日利亚 POP 趋势（2023-05→06） |
| 27 | `Brazil-POP customers experience the second largest average RTT (104 ms) and standard deviation ofRTT (27 ms).` … `customer Oceanica Sub VII … is 1491 mi away from its POP—a 14 ms RTT if using a direct ISL path—but experiences an average RTT of 96 ms` … `sustained latency spikes, lasting for 16% of our measurement period` | L307 | 单客户实测 |
| 28 | `Georgia-POP customers experience the highest average (58 ms) and standard deviation (21 ms) of latency across the US.` … `on average, a Georgia-POP customer is 1,000 miles away` | L309 | 美国内最差 POP |
| 29 | `Peru, Australia, and New Zealend experience the shortest RTT times, on average under 30 ms.` | L311 | 最好 POP |
| 30 | `the majority (70%) of Starlink traceroutes leak MultiProtocol Label Switching` | L283 | 协议层事实 |
| 31 | `StarryNet [58] does not evaluate latency predictions beyond the 90th percentile latency and is 20 times less accurate at predicting 90th percentile latency compared to 70th percentile latency.` | L85 | 仿真器精度缺陷 |
| 32 | `RIPE Atlas only allows built-in [3] and user-defined [5] traceroutes against the same target to be collected around the 60 second granularity, making it difficult to capture sustained RTT spikes that can change in 15 seconds.` | L215 | 对照平台的采样下限 |
| 33 | `HitchHiking cannot identify exactly what routing occurs between the POP and the client, does not know how many satellites, which satellites, and which ground stations packets are routed through.` | L154 | 可观测性上界 |

### 3) 对"负载变化/突发/时延/到达率"的事实贡献

**（a）时延**：本篇是**时延（RTT）现象的最强实测证据**，且给出了尖峰的**时间尺度**（15 s 量子，L190）与**空间/路由归因**：
- L315（结论级）：`First, we find that depending upon a customer’s distance to their POP, minimum latency grows over three-fold. Second, we detect and validate that routing changes to diferent ground stations cause sustained latency spikes that increase RTT by near an order of magnitude. Third, reliance on ISLs (e.g., customers on boats) correlates with increases in RTT and sustained latency increases.`
- L231：`while ISLs do increase coverage, they significantly increase the distance of the route between the ground station to POP.`

**（b）负载/拥塞——本篇明确排除"拥塞导致尖峰"**：
- L190 逐字：`RTT spikes are also not due to congestion. The ground truth metrics report no packet drop or drop in bandwidth during sustained or standard latency spikes. Furthermore, we find that spikes occur in multiples of 15 second—aligning with Starlink’s reported satellite reconfiguration period [12]—further making any cause of latency that is independent of Starlink routing (e.g., brief congestion caused by a nearby user) unlikely.`
- L154 逐字（不可归因声明）：`HitchHiking’s methodology to measure latency cannot on its own attribute the cause behind the latency (e.g., congestion, suboptimal routing).`
- L209 逐字（拥塞模式不可观测）：`Starlink does not reveal its internal fiber paths between ground stations and POPs, terrestrial routing decisions, satellite selection algorithm, ISL routing, or congestion patterns.`

**（c）突发/到达率**：**未见**。核验命令与实测计数（主控核验协议 v2）：
- 模式 A：`grep -ciE "arrival|offered load|load factor|burst|inter-?arrival|packet rate|traffic intensity|Erlang|congestion level"`，范围 `/data/liguang13/topic-loop-r2/md/GGFJ3SEG/GGFJ3SEG/txt/GGFJ3SEG.md` 全文 → **count = 1**（命中行：L83）。
- 模式 B：`grep -ciE "time series|stochastic|Markov|queue"`，同上范围 → **count = 0**。
- 命中位置与为何不构成反例：唯一命中 L83 逐字 `Theoretical Models. Given the dificulties in collecting empirical data, one of the most popular methodologies for studying LEO satellite networks is to use theoretical physics-based models, which simulate LEO Internet performance across location, satellite orbiting pattern, and congestion level.` —— 该处是**描述他人仿真器可扫的参数轴**（congestion level），本篇**既未测量也未建模**到达过程，故不构成反例。全文无到达过程、无包级/流级到达率、无突发长度分布的测量。本篇是**纯时延可达性测量**，不产生负载过程事实。

**（d）可作为"负载不变"的反证**：L190 的"no packet drop or drop in bandwidth"配合 L289 的"尖峰普遍存在"，构成一条重要事实：**在没有可观测拥塞信号时，时延仍出现 >2σ 且持续 ≥15 s 的尖峰**——即"时延尖峰 ≠ 负载尖峰"。

### 4) 能否作为定标或现象证据

**双重身份（本批最强）**：
1. **LEO 实测（真实 Starlink 星座，非仿真）**：采样口径为真实客户链路（L131–L152），并有自制地面真值 dish 校验（L164、L173、L177）。
2. **对仿真器的定标证据**：L192–L213 直接把 HitchHiking 与 Hypatia 对齐比较，并给出带单位的误差（L207 的 `7.6 ms`、L160 的 `up to 80%`）。
3. **对仿真可信度的否定项**：L201（图题）逐字 `Simulations do not capture the dynamics of real-world Starlink RTTs.`；L207 `No matter the ground station, Hypatia never predicts that a client experiences sustained RTT spikes, unlike HitchHiking`；L85 `the accuracy of most popular simulations [21, 57, 68] has never been verified.`

**结论**：可作**现象证据**（时延尖峰的存在性、时间量子、与卫星位置/切换/拥塞的解耦）；可作**仿真器定标证据**（误差量级 ms 级），但**不能**作负载/到达率过程的定标证据（本篇未测）。

### 5) 边界与不可外推项

1. **单一运营商**：L67 `As of 2023, Starlink [72] remains the only consumer-targeted LEO satellite network.`；OneWeb 仅识别约 20 个端点且**无法**校验：L323 `we are not able to validate latency measurements with ground truth (i.e., a OneWeb dish we control) because OneWeb dishes are (1) only available to businesses and (2) prohibitively expensive (e.g., upwards of \$23,000 [20])`。
2. **时间戳绑定**：全球结论仅覆盖 2023-05-18–2023-06-23（L233），且当时 ISL 仍在建设中：L289 `Starlink engineers share that they are still building their ISL “mesh” and hope to improve edge case performance over time.`；L156 `Since LEO network architecture changes nearly everyday due to new satellite launches [74], satellite falls [17], the integration of inter-satelllite lasers [49], and new ground stations [76], adaptability is crucial.` 因此**任何绝对 ms 数值不可外推到其它年份/其它星座**。
3. **时延口径不含地面段**：L150 的"相减"口径 = 卫星链路 RTT；L146 明确 `while the link between the last visible pre-satellite hop and the first visible post-satellite hop includes the satellite link, it also includes the terrestrial pathway between the POP and the ground station.`；L262 `all of our Starlink traceroutes show that packets are always tunneled to/from the customers assigned POP before traversing the public Internet`——端到端应用时延**大于**本篇数值。
4. **时间分辨率不足**：每天每端点仅 5 分钟、2 ping/s（L148），再加 15 s 平滑窗（L152）；L215 指出 RTT 尖峰可在 15 秒内变化。**亚 15 秒尺度的突发不可见**。
5. **样本选择偏差**：L138 `not all Starlink customers expose services; customers must use their own router and follow a set of special configurations`；L138 另注 `At least one-third of customerexposed Starlink services belong to a vendor that produces routers and firewall appliances, with the two most poular being Fortinet and Sonicwall.` 样本偏向"会暴露服务的企业/自建路由用户"，非随机用户总体。
6. **只测可达性/时延，不测容量**：容量类方法仅在设想中给出（L113 `to measure LEO satellite bandwidth, a researcher might use the pathchar [45] approach`），**本期未实施**。
7. **伦理约束限制主动实验强度**：L123 `LEO satellite links often operate at lower capacity than terrestrial links [63]. It is imperative that HitchHiking experiments do not degrade the quality of service for users by, for example, flooding LEO satellite links. We recommend researchers send the minimum number of packets needed to collect statistics about a LEO link, and avoid using tools that overload bandwidth (e.g., iperf [52]).`——**这直接排除把该平台当作负载/饱和实验的定标工具**。
8. **未读部分**：附录 L503–L546 正文（ETHICS / MAPPING WITH TRACEROUTE / IMPLEMENTATION DETAILS / OBSTRUCTION MAP / HYPATIA WORST CASE / MAPPING HITCHHIKING USERS AND POPS / HITCHHIKING ONEWEB）未逐段读，仅确认标题与 L323 的引用内容；参考文献 L343–L501 未读。

---
## 2. S2QZRBEJ — A First Look at Starlink Performance

**书目事实（逐字）**：L25 `# A First Look at Starlink Performance`；作者 L27 `François Michel UCLouvain`、L29 `Danilo Giordano Politecnico di Torino`、L53 `Martino Trevisan University of Trieste`、L55 `Olivier Bonaventure UCLouvain`；L45 `In Proceedings ofthe 22nd ACM Internet Measurement Conference (IMC ’22), October 25–27, 2022, Nice, France.`
**已读范围**：L25–L204（摘要 L33、引言 L47–L63、测试床与测量方法 L65–L80、结果 L82–L186、讨论与未来工作 L187–L195、制品 L197–L199、伦理 L201–L203）。参考文献 L205–L292 未读（不属证据范围）。

### 1) 测量/建模对象与条件（逐字+行号）

- L33（对象）：`In this paper, we investigate the user-perceived performance of Starlink. Our measurements show that latency remains low and does not vary significantly under idle or lightly loaded links. Compared to another commercial Internet access using a geostationary satellite, Starlink achieves higher TCP throughput and provides faster web browsing. To avoid interference from performance enhancing proxies commonly used in satellite networks, we also use QUIC to assess performance under load and packet loss.`
- L67（测试床，逐字）：`we use three of-the-shelf PCs equipped with 8 cores and 16 GB of memory running Ubuntu 20.04 and Linux kernel version 5.0.4. The two first PCs are located in the UCLouvain campus in Louvain-la-Neuve, Belgium. The first PC (PC_Starlink) is connected to the Internet via Starlink with a regular subscription. The second PC (PC_Wired) is connected to the UCLouvain campus network via a 1 Gbit/s Ethernet adapter. The third PC (PC_SatCom) is connected to the Internet via a traditional SatCom equipment for which we have purchased a regular plan ofering up to 100 Mbit/s in downlink and 10 Mbit/s in uplink.` … `For each setup, the TCP receive window is the kernel default, i.e. 131072 bytes by default with a maximum of 6291456 bytes through automatic bufer tuning. The congestion control is Cubic.`
- L69（QUIC 施加负载的口径，逐字）：`We assess the network performance with two kinds of transfers: (i) bulk HTTP/3 (H3) [16] 100MB transfers and (ii) light QUIC transfers with regularly sent messages, similar to a real-time video trafic. The latter sends 25 variable length messages per second during 2 minutes. Each message has a size in the 5-25kB range. The average bitrate of this transfer is 3 Mbit/s, far below both downlink and uplink capacities announced by Starlink.` … `The QUIC implementation used is quiche [1] compiled in release mode from commit ba87786. Its initial max_data and max_stream_data transport parameters are set to 10MB and the receive window varies through automatic bufer tuning. The congestion control used is Cubic.`
- L71（ping 时延口径，逐字）：`We measure the latency of Starlink by probing a set of 11 anchors using ping. Our set of anchors includes 7 servers used inside the RIPE Atlas project [8]. The servers are located in Europe (Amsterdam ×2, Nuremberg ×2), North America (New York, Fremont) and Asia (Singapore). We also include 4 nodes of the RIPE Atlas project hosted by volunteers in the same country as our Starlink connection (Belgium). Every five minutes, we measure the latency towards the anchors running 3 pings. We also measure the link latency under light and heavy network load by studying the evolution of the Round-Trip Time (RTT) measured by QUIC with our messages and H3 transfers.`
- L73–L76 Table 1（数据集规模，逐字表格）：`Latency | Starlink | 5Months | 11 Anchors`；`Throughput | Starlink | 4Months | Ookla`；`Throughput | SatCom | 2Weeks | Servers`；`Web Browsing | Starlink | 4Months | 120Websites`；`Web Browsing | SatCom | 2Weeks`；`QUIC H3 | Starlink | 5Months | Our server`；`QUIC messages | Starlink | 5Months | Our server`
- L78（吞吐口径）：`We measure Starlink download and upload throughput using the command line version of the Ookla SpeedTest service [11].` … `We perform a speed test every half an hour using PC_Wired from 20 December to April 7 2022.`
- L80（浏览口径）：`We rely on BrowserTime, a tool performing automated visits to websites [2]. We rely on the rank provided by SimilarWeb [13], an online ranking service out of which we pick the top-120 website for Belgium.` … `Every half an hour, we test 30 websites chosen at random and ensure they do not overlap with the speed test experiments. We collect data from December 20 to April 7 2022.`

### 2) 可引用的事实与数字（逐字+行号，含单位与口径）

| # | 事实（逐字） | 行号 | 口径 |
|---|---|---|---|
| 1 | `In the median case, the RTT is in [46, 52]ms and exceeds 70ms in less than 5% of cases. The minimum observed RTT for these anchors is [24, 28]ms.` | L96 | 比利时本地 4 anchors，空闲态 |
| 2 | `The lowest RTT we observe is for the two German probes, which PC_Starlink reaches in only 42ms in median. The lowest RTT we observe is 20.5ms, confirming Starlink’s 20ms latency promise.` | L96 | 最小值口径 |
| 3 | `San Francisco and Singapore are reached in a median of 184 and 270ms respectively.` | L96 | 远距 anchor |
| 4 | `This suggests that inter-satellite links (ISL) are not currently enabled, although ISL-capable satellites have been launched [5] and ISL activation is planned by the end of 2022 [4].` | L96 | 测量期 ISL 状态 |
| 5 | `The RTT to the European anchors remains constant around 50 ms in median and ranges from 40 ms (25th percentile) to 60ms (75th). The minimum measured latency is on the order of 20 ms.` | L106 | 5 个月、6 小时分箱 |
| 6 | `we observe that distribution of RTT is rather flat over the hours of the day. The median RTT is around 50 ms and a Mood’s test suggests the samples are drawn from distributions with the same median.` | L106 | **昼夜不变性**（统计检验） |
| 7 | `Similar considerations hold for throughput measurements as well, and this can hint low utilization of the infrastructure as most operator links are impacted by diurnal patterns.` | L106 | 作者对昼夜平坦的解释=低利用率 |
| 8 | `we observe an increase in RTT during the last week of April and the first week of May. Since, at that time, we did not run diferent experiments, we speculate that in this period Starlink was more loaded or going through reorganization, but we cannot confirm this.` | L106 | 作者自述不能确证 |
| 9 | `Each curve contains more than 2 millions RTT samples. We note a median, 95th and 99th percentiles RTT of 95 (resp. 104), 175 (resp 237) and 210 (resp 310) ms for downloads (resp. uploads).` | L107 | **负载态 RTT**（H3 bulk，PC↔服务器） |
| 10 | `We can see that the RTT increases more for uploads than download. This diference may be explained by the larger available bandwidth for downloads allowing emptying the router queues faster than for uploads, having thus a smaller impact on queuing delay for equally-sized queues.` | L107 | 排队时延归因 |
| 11 | Table 2 逐字：`H3↓ 1.56% | H3↑ 1.96% | Messages ↓ 0.40% | Messages ↑ 0.45%` | L110 | QUIC 丢包率（%） |
| 12 | `The downloads (resp. uploads) have 50 (resp. 66) ms median RTT, 71 (resp 87) ms 95th percentile and 87 (resp 143) ms 99th percentile RTT.` | L112 | 轻载（messages）RTT |
| 13 | `The largest messages (25 kB) are thus stacked in the network’s bufers making the RTT increase lightly.` | L112 | 缓冲堆积机制 |
| 14 | `Take Away: The minimum latency of Starlink is in the order of 20 ms for close destinations, as publicly advertised. Under trafic load, it may increase to a few hundreds of milliseconds.` | L114 | **负载→时延**核心结论 |
| 15 | `We identified 244 008 loss events. The median loss event duration is 49 microseconds. The 75th and 90th percentiles are respectively 58 and 113 microseconds. The 95th and 99th percentiles are 1.5 and 7.5 milliseconds.` | L121 | **丢包事件时长**（客户端抓包） |
| 16 | `As we can see, the majority of loss events during uploads concerned only one packet at a time, while more than 75% of loss events during downloads concerned several consecutive packets.` | L121 | 突发长度方向性 |
| 17 | `most events for message transfers were shorter than 1ms. However, we noted 95th and 99th percentiles of 104 and 127 ms which are larger than the percentiles for H3 downloads` … `some loss bursts of more than 100 packets` | L133 | 轻载态突发更长 |
| 18 | `For H3 (resp. messages) downloads, over more than 5.8 M (resp. 2.8 M) packets sent by our QUIC server, only 10 (resp. 8) were lost, making loss events nearly absent outside Starlink.` | L135 | 对照实验（排除本地/服务器） |
| 19 | `Take Away: The loss events occurring when the link is loaded are more frequent and only afect a few consecutive packets. Without link pressure, the loss events are more rare, concern overall more consecutive packets and last longer.` | L137 | **负载↔突发形状**核心结论 |
| 20 | `Starlink’s download throughput ranges between 100 and 250 Mbit/s. The median value is 178 Mbit/s, while the maximum is 386 Mbit/s.` | L150 | Ookla TCP |
| 21 | `The upload throughput, in Figure 5b, is significantly lower, reaching a median of 17 Mbit/s. Fewer than 5% of the cases exceed 30 Mbit/s and the highest observed rate is 64 Mbit/s.` | L152 | Ookla TCP |
| 22 | `we cannot find a seasonality in the measurements. Looking at the diferent hours of the day, the median throughput varies by less than ±10% with no apparent day-night cycle.` | L152 | **吞吐昼夜不变性** |
| 23 | `Starlink is more than twice as fast as SatCom (82 Mbit/s). The situation is similar for upload: the traditional SatCom connection inherently ofers lower upload throughput (4.5 Mbit/s in median), as it is limited to a bitrate of 10 Mbit/s.` | L154 | GEO 对照 |
| 24 | `in the best case (4G with good signal quality), mobile networks provide a median throughput of 29.5 Mbit/s. For upload, the authors found a median bitrate of 14 Mbit/s, comparable to Starlink’s 17 Mbit/s.` | L156 | 引用他人（非本篇实测） |
| 25 | `The download bitrate sits mostly between 100 and 150 Mbit/s which is in line with what is announced by Starlink but lower than the best results obtained with the Ookla TCP speedtests` | L158 | H3 单连接 |
| 26 | `Starlink (solid red line), overall, provides a median onLoad of 2.12s and an interquantile range (IQR) between 1.60s and 2.78s.`；`SatCom equipment (blue dashed line) show that onLoad is substantially larger, 10.91s on median. The distribution ranges from 8.36s (25th percentile) to 13.59s (75th percentile).` | L173 | 网页 QoE |
| 27 | `In our dataset, a single visit results in 15 connections on average. On SatCom, opening a connection (including the TLS handshake) takes an average of 2030ms, while Starlink requires only 167ms.` | L173 | 连接建立时延 |
| 28 | `Starlink shows a median performance of 1.82s, outperforming SatCom with a 8.19s median SpeedIndex. Starlink performance is closer to the Wired setup, with median of 1.0s.` | L175 | SpeedIndex |
| 29 | `Take Away: For Web browsing, Starlink outperforms SatCom and has close performance to regular wired access. Looking at QoE-related metrics, Starlink is 75 − 80% faster than traditional SatCom.` | L177 | 汇总 |
| 30 | `Traceroute shows us the presence of two levels of NAT at the two first nodes: the Starlink access point (192.168.1.1) and a carrier-grade NAT node (100.64.0.1) at the exit of the satellite link. Tracebox does not show the presence of any PEP` | L183 | 中间盒事实 |
| 31 | `In case of Starlink, we launched ten times the complete Wehe tests but could not find any TD policy in place, at least for these popular services.` | L185 | 流量歧视（未发现） |
| 32 | `Classical Satellite Communications (SatCom) use geostationary satellites with at an orbit of 22 236 miles.` … `with the drawback of a minimum latency of about 600 ms [37].` | L57 | GEO 参数（引用值） |
| 33 | `The first large-scale deployment of this kind is the Starlink constellation, currently operating more than two thousand satellites.` … `It promises Internet access with latency on the order of 20 ms and bandwidth speeds between 100 and 200 Mbps [12].` | L59 | 官方承诺值（引用） |
| 34 | `we have created a data-driven model for the ERRANT network emulator tool [43] and make it available at https://github.com/SmartData-Polito/errant.` | L63 | **可直接复用的仿真模型制品** |
| 35 | `This includes pings, traceroute, Tracebox, speed test and BrowserTime results as well as more than 530 Gigabytes of QUIC packet captures along with their encryption keys.` | L199 | 开放数据规模 |

### 3) 对"负载变化/突发/时延/到达率"的事实贡献

**本篇是本批最直接回答"施加负载后时延/丢包如何变化"的实测论文**，且口径明确到可复算：

- L94（实验设计，逐字）：`We first measure the latency without load on the link, which is the best latency Starlink subscribers could achieve. We then perform QUIC downloads and uploads, thus generating bandwidth pressure and study how the RTT evolves under load.`
- **时延随负载的量化跃升**：空闲态欧洲 anchor 中位 50 ms（L106）→ H3 bulk 下载 95 ms 中位 / 175 ms P95 / 210 ms P99；上传 104 / 237 / 310 ms（L107）；轻载 messages 只到 50 / 66 ms 中位（L112）。→ **同一链路，把应用发送速率从 ~3 Mbit/s 提到 100MB 批量传输，RTT 中位数约翻倍，P99 可到 300 ms 量级。**
- **突发/丢包的形状随负载反转**（L137 逐字已列）：高负载=**频繁但短**（多数 1 包）；低负载=**稀疏但长**（>100 包、持续 104–127 ms 的 P95/P99）。这是"突发≠拥塞"的直接实测依据。
- **到达率**：**未见**任何到达过程/到达率建模。核验命令与实测计数（主控核验协议 v2），范围均为该篇 MD 全文 L1–L292：
  - 模式 A（突发族）：`grep -ciE "arrival|offered load|load factor|burst|inter-?arrival|packet rate|traffic intensity|Erlang|congestion level"` → **count = 3**；命中行 L120、L129、L133。**为何不构成反例**：三处均指**已观测的丢包事件突发长度分布**（`loss burst length is the number of consecutively lost packets for each loss event`，L120；L129 图题；L133 讨论 messages 的 burst 更长），是**丢包的形状描述**，不是到达过程/到达率。
  - 模式 B（补充）：`grep -ciE "arrival|poisson|interarrival|per second|pps|packets/s|utilization|offered"` → **count = 5**；命中行 L69、L105、L120、L189、L227。**逐条为何不构成反例**：L69 `sends 25 variable length messages per second during 2 minutes` + `The average bitrate of this transfer is 3 Mbit/s` = **本篇施加的**轻载条件（实验输入，非测得过程）；L105 `we compute our statistics using 6-hours bins` = 统计分箱粒度；L120 `we determine the received packets by looking at the ACK frames returned by the server` = 丢包判定方法；L189 `the presence of (moderate) packet loss even at low network utilization` = 作者对"低利用率"的定性评论；L227 `https://www.speedtest.net/it/apps/cli` = 参考文献 URL（"pps" 子串）。
  - 模式 C：`grep -ciE "time series|stochastic|Markov|queue"` → **count = 1**；命中行 L107 `allowing emptying the router queues faster than for uploads, having thus a smaller impact on queuing delay for equally-sized queues` = **排队时延的机理解释**，无排队/到达过程模型。
  → **全篇无测得的分组到达过程、无到达率统计量。**
- **昼夜负载变化**：L106/L152 给出**未观测到昼夜周期**（RTT 用 Mood's test；吞吐变化 <±10%），并据此推断基础设施利用率低。

### 4) 能否作为定标或现象证据

- **LEO 实测（真实 Starlink 接入，比利时单点）**：L67 测试床；L191 `This study presents an initial characterization of Starlink from the perspective of a single site in Western Europe.`
- **可直接用作定标输入**：L63 提供的 **ERRANT 数据驱动模型**（含 3G/4G/GEO 对照）是本批唯一的"可加载的链路模型制品"；L199 的 `530 Gigabytes of QUIC packet captures along with their encryption keys` 可复算。
- **现象证据（对负载-时延耦合）**：L114、L137 两条 Take Away + L107/L110/L121/L133 的数字。
- **对仿真的态度（可引作旁证）**：L189 `Interestingly, early simulations of LEO constellations (see Hypatia [27], among others) predicted similarly low values for RTT, especially in this first phase of low utilization. However, we emphasize the presence of (moderate) packet loss even at low network utilization.`

**判定：LEO 实测 + 可复用仿真模型；不能作"到达率/负载过程"的定标证据（未测）。**

### 5) 边界与不可外推项

1. **单站点**：L189 逐字同上（single site in Western Europe）；L175 的 Wired 基线也在同一校园网内，非地理分散对照。
2. **ISL 未启用**：L96 逐字（`inter-satellite links (ISL) are not currently enabled`）；L191 `Inter-satellite links do not seem to be enabled, but Starlink plans to deploy them by the end of 2022. At that time, coverage will be significantly expanded, and it will be possible to study how packets are routed through the sky and how performance varies around the globe.` → **本篇的时延/丢包结论不适用于 ISL 使能的 Starlink**。
3. **时间窗口**：L78/L80 `from 20 December to April 7 2022`（Ookla/浏览器数据）；L96 五个月（含 2021 冬–2022 春）。遥测期早于 LEO 星座成熟期。
4. **无法区分拥塞丢包与介质丢包**：L131 逐字 `Note however that from the transport viewpoint, there is no known way to distinguish between congestion and medium-induced losses. This is why loss-based congestion control algorithms such as Cubic [24] interpret every loss event as a congestion signal.` → 表 2 的丢包率**不能**直接读作拥塞指标。
5. **浏览器 QoE 采样限制**：L195 `we only studied a limited number of websites because we wanted to visit them hourly. We did not account for diferences in experience that could be due to diferent browsers, diferent devices, or other factors. Also, we only visited landing pages, while a more realistic campaign should include internal pages [14].`
6. **时延对比的服务器口径**：QUIC 服务器在比利时 UCLouvain 校园（L69），与客户端同国，**不是**地理分散的端到端时延；L96 的远距数值来自 ping anchors。
7. **作者自述的时效性局限**：L191 `Given the limited time between the commercial launch of Starlink and this study, our ping latency measurements are still in the early stages in terms of temporal and spatial scale.` … `the number of anchors we probe is limited and does not allow us to provide a complete picture of latency for a comprehensive set of targets worldwide.`

---
## 3. NPF75WS5 — A Multifaceted Look at Starlink Performance

**书目事实（逐字）**：L33 `# A Multifaceted Look at Starlink Performance`；作者 L35–L47 Nitinder Mohan / Rohan Bose / Andrew E. Ferguson / Prakita Rayyan Renatin / Hendrik Cech / Mahesh K. Marina / Jörg Ott（TUM / Edinburgh）；L63 `In Proceedings ofthe ACM Web Conference 2024 (WWW’24), May 13–17, 2024, Singapore, Singapore.`
**已读范围**：L33–L243（摘要 L51、引言 L65–L82、背景 L87–L92、方法 L93–L117、全局性能 L119–L154、实时应用 L156–L178、拆解 bent-pipe L180–L228、相关工作 L230–L234、结论 L236–L238）+ L244–L252 参考文献头部确认。附录 L408–L440 标题级确认（未逐段读，见第 5 项边界）。参考文献正文 L244–L406 未读。
**折行说明**：本篇 MD 中图注（如 Figure 5 / Figure 6）与正文同处一行（L129、L131、L140 等）；引文按行号给出，折行不予拼接。剔除的行仅为图片嵌入行（`![](...)`，长度 80–82 字符，已核验无正文）。

### 1) 测量/建模对象与条件（逐字+行号）

- L51（摘要，四路证据链，逐字）：`First, based on 19.2M crowdsourced M-Lab speed tests from 34 countries since 2021, we analyze Starlink global performance relative to terrestrial cellular networks. Second, we examine Starlink’s ability to support real-time latency and bandwidth-critical applications by analyzing the performance of (i) Zoom conferencing, and (ii) Luna cloud gaming, comparing it to 5G and fiber. Third, we perform measurements from Starlink-enabled RIPE Atlas probes to shed light on the last-mile access and other factors afecting its performance. Finally, we conduct controlled experiments from Starlink dishes in two countries and analyze the impact of globally synchronized “15-second reconfiguration intervals” of the satellite links that cause substantial latency and throughput variations.`
- L97（M-Lab 口径，逐字）：`At its core, M-Lab uses the Network Diagnostic Tool (NDT) [39], which measures uplink and downlink performance using a single 10 s WebSocket TCP connection. The platform also records fine-grained transport-level metrics (tcp_info), including goodput, round-trip time (RTT) and losses, along with IP, Autonomous System Number (ASN), and geolocation of both the end-user device and the selected M-Lab server.`
- L102（样本筛选，逐字）：`We identify measurements from the Starlink clients via their ASN (AS14593). The M-Lab dataset includes samples from 59 out of 63 countries where Starlink is operational. We restrict our analysis to ndt7 measurements, which use TCP BBR and countries with at least 1000 measurements since June 2021 (launch of Starlink v1.0 satellites [28]), resulting in 19.2 M M-Lab measurement samples from 34 countries.`
- L104（RIPE Atlas 口径，逐字）：`We utilized 98 Starlink RIPE Atlas probes across 21 countries (see Figure 3). Our measurement targets were 145 data centers from seven major cloud providers – Amazon EC2, Google, Microsoft, Digital Ocean, Alibaba, Amazon Lightsail, and Oracle (see Appendix B).` … `We extract and track per-hop latencies between Starlink probe terminal-to-GS (identified by static 100.64.0.1 address), GS-to-PoP (172.16/12) and PoP-to-endpoint at 2 s intervals [52].` … `Our experiments over ten months (Dec 2022 to Sept 2023) resulted in ≈ 1.8 M measurement samples.`
- L108（Zoom 条件）：`We set up a Zoom call between our server, with access to an unobstructed Starlink dish and 1 Gbps Ethernet, and an AWS machine located close to the assigned Starlink PoP.` … `Both servers were synchronized to local stratum-1 NTP servers and we recorded (and analyzed) subsecond Zoom QoS metrics using the toolchain from [41].`
- L110（Luna 条件）：`We leverage the automated system from [17] to evaluate the performance of playing the racing game “The Crew” on the Amazon Luna [2] platform.` … `Amazon Luna serves games at 60 FPS and 1920x1080 resolution which adaptively reduces to 1280x720 depending on the network.`
- L117（受控实验条件，逐字）：`We orchestrated a set of precise, tailored, and controlled experiments, utilizing two Starlink terminals as vantage points (VPs) situated in Germany and Scotland.` … `The irtt setup records RTTs at high resolutions (3 ms interval) by transmitting small UDP packets. The irtt servers were deployed on cloud VMs in close proximity to the assigned Starlink PoP of both VPs (within 1 ms) – minimizing the influence ofterrestrial path on our measurements. We used iperf to measure both uplink and downlink throughput and record performance at 100 ms granularity. Simultaneously, we polled the gRPC service on each terminal [65] every second to obtain the connection status information.`
- L82（开放数据）：`we publish our > 300 GB collected dataset and associated scripts at [44] and [45].`

### 2) 可引用的事实与数字（逐字+行号，含单位与口径）

| # | 事实（逐字） | 行号 | 口径 |
|---|---|---|---|
| 1 | `The Starlink network from SpaceX stands out as the only commercial LEO network with over 2M+ customers and more than 4000 operational satellites.` | L51 | 规模（2023-09 口径见 L232） |
| 2 | `Starlink from SpaceX stands out with its expansive fleet of 4000 satellites catering to 2M+ subscribers across 63 countries [60, 77]. The LEO operator plans to further amplify its coverage and quality of service (QoS) by launching ≈ 42,000 additional satellites in the coming years [15].` | L69 | 规模与规划 |
| 3 | `LEO networks consist of megaconstellations with thousands of satellites orbiting at 300–2000 km altitudes` | L67 | 轨道高度口径 |
| 4 | `Starlink is a LEO satellite network operated by SpaceX that aims to provide global Internet coverage through a fleet of satellites flying at ≈ 500 km above the Earth’s surface.` | L89 | 高度（本篇口径） |
| 5 | `for a majority ofcountries, clients using terrestrial ISPs achieve better latencies over Starlink. While the median latency of Starlink hovers around 40–50 ms, this distribution varies significantly across geographical regions.` | L133 | 全球 minRTT 中位 |
| 6 | `Even though a significant portion of global Starlink measurement samples originate from Seattle (≈ 10%), the region shows consistently low latencies, with the 75th percentile well below 50 ms` | L135 | 分位口径 |
| 7 | `Europe is also relatively well covered with GSs but hosts only three PoPs that are in the UK, Germany, and Spain. Proximity to the nearest PoP correlates strongly with minRTT performance in Figure 7 – Dublin, London, and Berlin exhibit comparable latencies to the US, while for Rome and Paris, the 75th percentile is ≈ 20 ms longer. Unlike US, Starlink latencies in EU has longer tail, often surpassing 100 ms.` | L135 | 欧洲 PoP 稀缺性 |
| 8 | `Figure 7 shows that Starlink in South America (SA) trails significantly behind the US and Europe, with the 75th percentile exceeding 100 ms and tail reaching 200 ms.` | L137 | 区域尾部 |
| 9 | `a local PoP was deployed in May 2023. Prior to this, Starlink trafic from the country was directed to the nearest Japanese PoP, traversing long submarine links to circle back to the geographically closest M-Lab server in Philippines – evident from additional 50–70 ms RTT in Figure 19 in Appendix C for Philippines users to reach in-country vs. Japanese M-Lab servers. However, post-May 2023, the latencies to in-country servers reduced by 90%` | L142 | 基础设施变更的因果证据 |
| 10 | `Figure 8 reveals significant delay inflation under load as during active downloads, Starlink experiences ≈ 2–4x increased RTTs, reaching almost 400–500 ms (Figure 8a). While such inflations are consistent across all Starlink service areas, they are more prominent in regions with subpar baseline performance, e.g., Mexico. Note that the Starlink latency under load is not symmetric. The 60th percentile of RTT during uploads increases to ≤ 100 ms globally (see Figure 8(b)) compared to ≈ 200 ms during downloads.` | L144 | **RTT inflation（maxRTT−minRTT）口径；原文 "2–4×" 见注[1]** |
| 11 | `Most Starlink clients achieve ≈ 50–100 Mbps download and ≈ 4–12 Mbps upload rates at the 75th percentile. We also do not find any correlation between baseline latencies (see Figure 6) and upload/download goodput, evident from the contrasting cases of Dublin and Manila. However, we observe an inverse correlation between loss rates and goodputs; increasing from 4–8% at the 75th-percentile` | L146 | goodput/丢包（75 分位） |
| 12 | `The total uplink throughput over Starlink is slightly higher, which we trace to FEC (Forward Error Correction) packets that are frequently sent in addition to raw video data (on average 146±99 Kbps vs. 2±2 Kbps over terrestrial). The frame rate, inferred from the packets received by the Zoom peer, does not meaningfully difer between the two networks (≈ 27 FPS).` | L160 | Zoom 上行 |
| 13 | `The uplink one-way delay (OWD) over Starlink is higher and more variable compared to the terrestrial connection (on average 52±14 ms vs. 27±7 ms). All observations also apply to the downlink except that Starlink’s downlink latency (35±11 ms) is similar to the terrestrial connection (32±7 ms).` | L160 | **OWD 均值±SD** |
| 14 | `we observe that the Starlink OWD often noticeably shifts at interval points that occur at 15 s increments. Further investigation reveals the cause to be the Starlink reconfiguration interval, which, as reported in FCC filings [72], is the time-step at which the satellite paths are reallocated to the users. Other recent work also reports periodic link degradations at 15 s boundaries in their experiments, with RTT spikes and packet losses of several orders [25, 52, 74].` | L169 | 15 s 周期（末句为引用他人，非本篇实测） |
| 15 | `Table 1 shows 150 minutes of cloud gaming performance over terrestrial, 5G cellular, and Starlink networks. Overall, all networks realized close to 60 FPS playback rate at consistently high bitrate (≈ 20 Mbps).` … `the wired network delivers the visual response about 2 frames (≈ 33 ms) earlier than both 5G and Starlink.` … `we observe occasional drops to < 20 FPS over Starlink (see Figure 11), that coincide with Starlink’s reconfiguration interval. These fluctuations are only visible at sub-second granularity and, hence, are not reflected in global performance analysis (§4).` | L171 | 云游戏 |
| 16 | `we find that the Starlink bent-pipe latencies fall within 36–48 ms, with the median hovering around 40 ms for almost all countries. Similarly, we find consistent cellular last-mile latencies across all countries, but almost 1.5x less than Starlink.` … `Out of the 21 countries with Starlink-enabled RIPE Atlas probes, the only exceptions where the bent-pipe latency is significantly higher (≈ 100 ms) are the Virgin Islands (US), Reunion Islands (FR), and Falkland Islands (UK).` | L186 | bent-pipe 口径（terminal→PoP） |
| 17 | `we deduce through our traceroutes that Starlink directs its subscribers to the nearest GS relative to the PoP, as the GS ↔ PoP latencies are ≈ 5 ms (almost) globally (see Figure 20 in Appendix C – sole exceptions being US and Canada with 7–8 ms` | L191 | 地面段时延 |
| 18 | `we find that the predominant distance between GS and the user terminal is ≤ 1200 km, which is also the approximate coverage area width of a single satellite from 500 km altitude [5]` | L191 | 几何口径 |
| 19 | `in RU, Starlink shows significant latency improvement over fiber (≈ 60 ms). This is because the island has limited connectivity with two submarine cables routing trafic 10,000 km away` … `since the bent-pipe incurs at least 30–40 ms latency in the best-case, Starlink is less attractive in regions with robust terrestrial network infrastructure` | L198 | ISL 跨洋案例 |
| 20 | `Despite dense GS availability, the bent-pipe latencies for Alaska are significantly higher (≈ 2x).` | L200 | 高纬代价 |
| 21 | `Takeaway #3 — The Starlink “bent-pipe” accounts for ≈ 40 ms latency globally.` | L202 | 汇总 |
| 22 | `We also observe throughput drops on both downlink and uplink, shown in Figure 16b, that occur at the reconfiguration interval boundaries. Similar to the RTT, the throughput typically remains relatively consistent within an interval, but fluctuates between intervals.` | L206 | 区间内稳定/区间间跳变 |
| 23 | `The restriction curtailed the number of candidate (potentially connectable) satellites to 13%, resulting in intermittent connectivity.` | L211 | 受控实验条件 |
| 24 | `these reconfigurations result in brief sub-second connection disruptions, which may become more noticeable at the application-layer as the number of subscribers on the network increases over time.` | L226 | 中断时长量级 |
| 25 | `Takeaway #4 — Starlink uses 15s-long reconfiguration intervals to globally schedule and manage the network. Such intervals cause latency/throughput variations at the interval boundaries. Handofs between satellites are not the cause of these efects.` | L228 | 核心结论 |
| 26 | `Takeaway #1 — Starlink exhibits competitive performance to terrestrial ISPs on a global scale, especially in regions with dense GS and PoP deployment. However, noticeable degradation is observable in regions with limited ground infrastructure. Our results further confirm that Starlink is afected by buferbloat.` | L154 | 缓冲膨胀结论 |
| 27 | `Figure 16: (left, a) iRTT latencies with Dishys in two countries connected to diferent ground infrastructure; (middle, b) Maximum uplink and downlink throughput over a 195-second (13 interval) period` | L224 | 受控实验时长口径 |

注[1]：原文乘号字符为 U+00D7；本文件为规避 DSH run_code 解析器对该字符的报错，仅在第 10、16、20 行以 `x` 代替，其余全部逐字。数字口径不变。

### 3) 对"负载变化/突发/时延/到达率"的事实贡献

**本篇是本批在"负载→时延"上口径最硬的实测论文（唯一给出"负载下 RTT 膨胀倍数 / 绝对量级 / 上下行不对称"三件套）**：

- **负载引起的 RTT 膨胀（沿用第 2 项第 10 行逐字引文）**：下载时 `≈ 2–4x increased RTTs, reaching almost 400–500 ms`；上传 60 分位 `≤ 100 ms` vs 下载 `≈ 200 ms`。作者给出的机制假设逐字（L144）：`Possible explanations can be queue size diferences at the Dishy (afecting uploads), the ground station (afecting downloads), or satellites (impacting both). It is also plausible that Starlink employs active queue management (AQM) techniques [1] to moderate uplink latencies under congestion.`
- **负载下时延的来源定义（逐字，L121）**：`we evaluate the RTT inflation, i.e., the diference between the maximum and minimum RTT observed during a speed test.` → **可复算的定标口径**（单次 10 s NDT 测速内 max−min）。
- **周期性的非负载型扰动（15 s）**：L169、L206、L211、L226、L228。关键事实是**区间内稳定、区间边界跳变**，且**与卫星切换解耦**（L211 的单星可见窗口实验：`The significant RTT variance between intervals invalidates the hypothesis that the RTT changes are caused by satellite handovers (no handofs are possible with single satellite in field-of-view).`）。→ 与 GGFJ3SEG 的 15 s 量子（GGFJ3SEG L190）**相互独立地吻合**。
- **上行/下行不对称**：L144（下载膨胀远大于上传 60 分位）、L160（Zoom 上行 OWD 52±14 ms 显著高于下行 35±11 ms）。
- **突发**：本篇**无自身测得的丢包突发长度分布**；L169 的 `RTT spikes and packet losses of several orders` 是**引用他人**（[25, 52, 74]），不可当作本篇实测数字。
- **到达率/负载过程**：**未见**。核验命令与实测计数（主控核验协议 v2），范围均为该篇 MD 全文 L1–L463：
  - 模式 A：`grep -ciE "arrival|offered load|load factor|burst|inter-?arrival|packet rate|traffic intensity|Erlang|congestion level"` → **count = 0**。
  - 模式 B：`grep -ciE "time series|stochastic|Markov|queue"` → **count = 2**；命中行 L144、L246。**为何不构成反例**：L144 命中词是 `queue buildups` 与 `queue size diferences at the Dishy`（bufferbloat 段内的**机理解释**：`wherein latencies during trafic load can increase significantly due to excessive queue buildups [40]`），该段无排队模型、无到达过程；L246 是参考文献标题 `[1] Richelle Adams. 2012. Active queue management: A survey.`。
  → 负载在本篇一律以"测速期间施加的 10 s 批量传输"或 goodput（Mbps）这一**结果量**出现，**全篇没有到达过程的建模或测量**。

### 4) 能否作为定标或现象证据

- **LEO 实测（三类独立证据）**：(1) 19.2M 条众包 M-Lab ndt7（L102）；(2) 98 个 Starlink RIPE Atlas probe / 21 国 / ≈1.8M 样本（L104）；(3) 德/苏两地自控终端 + irtt(3 ms) / iperf(100 ms) + 单星可见窗口受控实验（L117、L211）。
- **可直接作为定标输入的量**：全球 minRTT 中位 40–50 ms（L133）、bent-pipe ≈40 ms 与 36–48 ms 区间（L186/L202）、GS↔PoP ≈5 ms（L191）、负载下 RTT 膨胀 2–4 倍 / 400–500 ms（L144）、goodput 50–100 与 4–12 Mbps @P75（L146）、丢包率 4–8% @P75（L146）、15 s 周期（L228）。
- **可复现性**：`> 300 GB collected dataset and associated scripts`（L82）。
- **现象证据**：15 s 全局同步重配置是**可写进模拟器的确定性时间结构**（比"随机突发"更强的可复现现象）；bufferbloat 结论（L154）是"负载→时延"因果链的直接支撑。

**判定：LEO 实测；可作定标（数值）与现象证据（15 s 周期、负载-时延耦合、上下行不对称）。**

### 5) 边界与不可外推项

1. **RTT inflation 是测速内的极差代理，不是排队模型**：L121/L144 的口径是单次 10 s NDT 传输内的 max−min，混杂了 15 s 重配置边界效应与真实排队；**不能直接反解队列长度或利用率**。
2. **M-Lab 的"负载"不可控**：M-Lab 是众包测量（L97），负载由测试本身 10 s TCP 产生，与真实用户业务负载的过程无关。
3. **地理定位是 PoP 级、非用户级**：L102 `M-Lab infers the approximate location of Starlink users from their public IP which is assigned by the PoP. As a result, all speed tests across countries are mapped to a city, except for USA and Canada, which are sub-divided into multiple regions.` … `we approached our analysis with caution, particularly when examining fine-grained region-specific insights.`
4. **接入类型混杂**：L121 `Note that our filteration results in a mix of wired and wireless access networks since M-Lab does not provide a way to distinguish between the two.`
5. **RIPE Atlas 无亚秒可见性**：L117 `A significant limitation of RIPE Atlas measurements is their lack of sub-second visibility, which is essential for understanding the intricacies of Starlink network.`
6. **ISL 不可观测**：L92 `Note that not all Starlink satellites are ISL-capable and it is dificult to efectively estimate ISL usage as Starlink satellites have no visibility at IP layer [52].`；L193 `the invisibility of satellite hops in traceroutes poses a challenge in accurately assessing the use or impact of ISLs.`
7. **地面设施位置为众包**：L91 `No oficial source exists, so we rely on crowdsourced data for the geolocations of GSs and PoPs [51]`；L191 复述同一限制 → **GS 距离相关结论（L191、L200）依赖众包定位精度**。
8. **受控实验的天气/遮挡条件有利**：L176 `our Starlink terminal was set up without obstructions and the weather conditions during measurements were favorable to its operation [36]. Diferent conditions, especially mobility, may change the relative performance ofStarlink and cellular.`
9. **蜂窝对照数据来自他人**：L186 `we augment our dataset with recent measurements from Dang et al. [10], which leveraged 115,000 cellular devices worldwide over the Speedchecker platform.` → 1.5 倍对比含跨数据集误差。
10. **时间窗口**：M-Lab 自 2021-06 起（L102）；RIPE Atlas 2022-12 至 2023-09（L104）；云游戏仅 150 分钟（L171）→ **单次实验时长极短，不能外推为长期分布**。
11. **未读部分**：附录 A（轨道信息）、B（数据中心端点）、C（全局补充图）、D（bent-pipe 全局视图）、E（定向测量挑战）正文未逐段读，仅确认标题（L408–L440）；正文引用其处（L135、L137、L142、L146、L191）已按正文行号引用。L220–L224 为图 16 的坐标轴标签行，非正文。

---
## 4. P6XJZNQK — A Global Perspective on the Past, Present, and Future of Video Streaming over Starlink

**书目（逐字）**：L1 `# A Global Perspective on the Past, Present, and Future of Video Streaming over Starlink`；L3–L6 Liz Izhikevich（UCLA）/ Reese Enghardt / Te-Yuan Huang / Renata Teixeira（Netflix）；L16 `Proc. ACM Meas. Anal. Comput. Syst. 8, 3, Article 30 (December 2024), 22 pages. https://doi.org/10.1145/3700412`。
**已读范围**：L1–L340（摘要 L8、引言 L18–L30、LEO 视频增长 L32–L64、QoE L66–L200、拥塞控制 L202–L241、ABR L243–L305、局限 L307–L315、相关工作 L317–L329、未来工作 L331–L335、结论 L337–L339）。参考文献 L345–L466 未读。

### 1) 测量/建模对象与条件（逐字+行号）

- L26：`In this work, we provide the first global analysis of on-demand video streaming over LEO. Using data from a large video streaming service, Netflix, we analyze over one million LEO households across 85 countries for over two years.`
- L36（数据口径）：`The data collected focuses on viewing duration (without looking into what people are viewing), quality of experience metrics (e.g., play delay) collected from the client device, network metrics (e.g., round-trip time) collected from the server’s TCP stack, and metadata (e.g., autonomous system, country, device type).`；`We identify Starlink households by their autonomous system (ASN 14593).`
- L72–L80（会话筛选条件逐字）：`(1) theoretically capable—as determined by Netflix subscription plan and device type—to stream at least at a 720p high definition resolution to ensure low quality is due to the network; (2) at least 5 minutes long …; (3) destined towards TVs … which are more likely to be stationary, thereby minimizing customer mobility artifacts; and (4) streamed during the first week of April 2024, unless otherwise noted.`
- L86（质量口径）：`We quantify perceptual video quality using a popular full-reference objective video quality assessment algorithm [40]: Video Multi-Method Assessment Fusion (VMAF) [28].`；L88 `we report VMAF as a Maximum Quality Ratio` … `Maximum Quality Ratio is computed by dividing the time-weighted VMAF … by the maximum possible VMAF available for the session.`
- L226（A/B 实验条件）：`We run an A/B test using New Reno with MulTCP on over 1 million Netflix video streaming sessions over Starlink.` … `We run the test for a week in mid-April 2024.`
- L257（仿真条件）：`we simulate diferent ABR strategies on a random sample of 500K Starlink and 500K non-Starlink streaming sessions, randomly sampled between April 20–May 5, 2024.` … `Netflix’s player records throughput over time in 500 ms buckets, where throughput is computed as the number of bytes downloaded during a given bucket divided by the active transfer time during the bucket.`

### 2) 可引用的事实与数字（逐字+行号）

| # | 事实（逐字） | 行号 |
|---|---|---|
| 1 | `As of April 2024, the most widely deployed LEO network is Starlink, with near 6K satellites [43] and over 2.6 million users [6].` | L54 |
| 2 | `As of August 2024, Starlink is the 29th of over 20,000 ISPs responsible for all global viewing seconds.` | L56 |
| 3 | `As of April 2024, customers from over 85 countries stream video over Starlink. Starlink leads in geographic diversity; the second most geographically diverse network has users from less than half the number countries as Starlink.` | L58 |
| 4 | `large mainland territories—the US, Canada, Australia, Mexico, and Brazil—compose the top 5 countries that contribute the most Netflix viewing seconds over Starlink. Together, they contribute near 90% of all viewing seconds over Starlink.` | L60 |
| 5 | `While the majority of regions today increase the number of viewing seconds by roughly 10%, Africa grows its streaming by over 20%.` | L62 |
| 6 | `Customers on or near the Pitcairn Islands rely on the Starlink most, streaming 30% of their video over Starlink. Zambia, Rwanda and Malawi also rely the most on LEO, streaming over 5% of their video over Starlink. In comparison, the United States streams less than 1% of their video over Starlink.` | L64 |
| 7 | `Starlink customers are 60% more likely to experience a bitrate switch, and 200% more likely to experience a rebufer relative to the most popular Internet service providers.` | L68 |
| 8 | `Starlink provides up to 18% better Maximum Quality Ratio in the worst video streaming sessions in Malawi and Zambia, and up to 8% worse in the worst streaming sessions across Mexico, Rwanda, and Brazil.` | L103 |
| 9 | `Countries with historically high RTTs (Zambia, Rwanda, Malawi) experienced play delays that were up to 250% higher than the US.` | L147 |
| 10 | `Zambia, Rwanda, Malawi experience play delays that are 5–10% lower than non-Starlink alternatives.` | L149 |
| 11 | `For sessions that experience at least one bitrate switch, 50% of Starlink sessions will experience over 2 times the number of bitrate switches compared to non-Starlink networks.` | L168 |
| 12 | **`Uniquely, over 95% of Starlink’s throughput is lower than alternative networks. For example, Starlink throughput is nearly always 50% of what a top 10 ISP ofers and falls below 20 Mb/s`；`Over 90% of bitrate switches, no matter the network, occur at throughputs below 20 Mb/s.`** | L170 |
| 13 | **`80% of observed throughputs increase/decrease with greater magnitude than in a Top 10 ISP. On average, Starlink throughput increases/decreases take longer to recover: While 50% of throughput decreases that reach below 10Mb/s … in non Starlink networks take roughly 5 seconds to recover back to above 10Mb/s, 50% of Starlink throughput decreases take roughly 15 seconds to recover. Coincidentally, 15 seconds is the interval that Starlink re-configures static routes for packet forwarding between satellites and/or ground stations [2].`** | L172 |
| 14 | `In Figure 11a, we illustrate an example video streaming session over Starlink, which sufers from a total of eight bitrate switches within the span of 100 seconds. The Starlink throughput dipping below 20 Mb/s twice while the bufer level dips below holding less than 1 minute of video (Figure 11b) contributes to the decreases in bitrates. Meanwhile, a sudden upward burst of throughput contributes to the successive increases in bitrate.` | L174 |
| 15 | `they are significantly (216%) more likely to occur over Starlink than a Top 10 ISP, and 40% more likely to occur relative to any non-Starlink network. Furthermore, if a customer experiences at least one rebufer, Starlink customers are 50% more likely to experience more than one rebufer. In the worst case, Starlink customers experience twice as many rebufers as non-Starlink customers.` | L192 |
| 16 | `Streaming sessions near Africa and Latin America are over 2 times more likely to experience a rebufer relative to the United States.` | L194 |
| 17 | `In the median case, Starlink sessions spend 50% less time in the reduced bitrate state.` … `Starlink sessions are six times more likely to experience an outage (i.e., a period of at least 8 seconds) compared to non Starlink sessions. Outages are often due to a physically obstructed dish or no satellite in line of sight [48].` | L198 |
| 18 | **`Starlink’s high packet round trip times (RTTs) and increased retransmit rates contribute to low TCP congestion windows, and hence, lower throughput. We find (Figure 13) that 75% of minimum RTTs over Starlink are at least two times greater than non-Starlink networks.`** … `we discover the majority of Starlink sessions experience nearly two times the retransmit rate relative to non-Starlink networks. The increase in Starlink retransmits is likely influenced by random loss on satellite links [34]; the use of Active Queue Management (FQ-CoDel) on the Starlink WiFi router [6], which minimizes latency at the expense of packet loss; and potential packet reordering [27], which may lead to duplicate acknowledgments and spurious retransmits.` | L213 |
| 19 | **`New Reno with MulTCP increases average throughput by 30-40% compared to the default congestion controller`** … `Increase in throughput results in a statistically significant, 0.08%–1% increase in lower quantile VMAF. Further, network rebufers per hour of video played decrease by 7%, play delay decreases by 2%, and bitrate switches decrease by 5%. Nevertheless, New Reno with MulTCP over Starlink is still 33% more likely than non-Starlink sessions to experience a bitrate switch.` | L235–L237 |
| 20 | **`New Reno with MulTCP presents undesirable drawbacks. Retransmit rates increase by 300% on average and the 95th percentile of latency measurements increases by 77% on average, indicating that New Reno with MulTCP fills in-network queues to a greater capacity. Further, the increase in latency under load could cascade into other problems when competing with real-time flows.`** | L239 |
| 21 | `Due to Starlink’s excessive variability (Section 3.4.1), smoothed throughput overestimates throughput by up to an additional 10% compared to non-Starlink throughputs.` | L277 |
| 22 | `Starlink sessions under the same ABR configuration, on average, experience a roughly 35% significant increase in the number of network rebufers per hour. Critically, no amount of Starlink throughput smoothing actually allows it to achieve a non-Starlink equivalent network rebufer rate.` | L279 |
| 23 | ABR 扫描参数范围逐字：`we sweep throughput smoothing window size (using exponentially weighted moving average) between 0–300000 ms, throughput discounts between 0–60%, bufer level between 0–100000 ms at which to apply bufer discount.` | L264 |

### 3) 对"负载变化/突发/时延/到达率"的事实贡献

- **负载→时延的实验证据（最强的一条）**：L239 —— 人为提高发送并发度（MulTCP 模拟 3 条连接）后吞吐 +30–40%，但**重传率 +300%、P95 时延 +77%**，作者明确归因为 `fills in-network queues to a greater capacity`。这是"把链路推向高负载 → 队列填充 → 时延上升"的**在网 A/B 实测**（100 万用户、一周）。
- **时延的量级与分布**：L213 `75% of minimum RTTs over Starlink are at least two times greater than non-Starlink networks`。
- **突发/时变的形状**：L172 给出**吞吐跌落后的恢复时间分布**（Starlink 中位约 15 s vs 非 Starlink 约 5 s），并把它与 15 s 重配置周期联系起来；L170 给出"95% 的吞吐低于替代网络、低于 20 Mb/s"。
- **到达率/负载过程**：**未见**。核验命令 `grep -ciE "arrival|offered load|load factor|burst|inter-?arrival|packet rate|traffic intensity|Erlang|congestion level"`，范围=该篇 MD 全文 L1–L466 → **count = 1**；唯一命中行 L174（`a sudden upward burst of throughput`）。**为何不构成反例**：该处指**单次会话里吞吐的突升**（结果量），非包/流到达过程。另一模式 `grep -ciE "time series|stochastic|Markov|queue|poisson"` → **count = 2**；命中行 L239（`fills in-network queues to a greater capacity`）与综述性排队叙述，均为排队机理描述，**无排队模型、无到达过程**。

### 4) 能否作为定标或现象证据

- **LEO 实测（全球最大规模的应用层视角）**：L26（100 万+ 家庭、85 国、2 年）、L36（Netflix 服务端 TCP 栈指标）、L226（100 万用户的真实 A/B）。
- **可作定标输入**：吞吐–时延耦合（L235/L239：+30–40% 吞吐 vs +300% 重传 / +77% P95 时延）；minRTT 比值（L213）；恢复时间（L172）。
- **现象证据**：15 s 恢复时间与 15 s 重配置的耦合（L172）；"提吞吐≠提 QoE"的反直觉因果证据（L237、L241：`eforts to simply match Starlink’s performance metrics, such as average throughput, with those of terrestrial networks do not necessarily lead to an overall improvement in quality of experience over Starlink.`）。
- **对本选题的直接价值（作者自述的推广面）**：L335 `we should build general solutions that consider non-congestive losses and treat throughput variation as a first order metric, rather than merely optimizing for performance over LEO networks.` → **"把吞吐方差当一阶指标"是本篇对 RL 路由奖励设计的直接可引主张**（非拥塞性丢包亦需显式建模）。

### 5) 边界与不可外推项

1. **单一 vantage point**：L309 `Our understanding … are inherently biased by our vantage point: Netflix.`；L311 `trends in Starlink’s growth over time (Section 2) are predominantly based on Netflix users and may not accurately represent Starlink’s overall user base.`
2. **绑死 Netflix 算法**：L311 `our analysis of Starlink’s delivery of high-quality video (Section 3) relies on Netflix’s streaming algorithms and congestion controller and might not hold for other streaming services.`
3. **只对视频流成立**：L311 `the quality of experience we measured for Starlink users may not translate to other types of applications … the video bufer helps hide many of transient network disruptions typical of LEO access.`
4. **会话长度筛选偏差**：L315 `we filter for video sessions at least five minutes long (Section 3.1). However, such filtering could unintentionally exclude video sessions that were aborted early due to poor video quality.`
5. **不是底层网络测量**：指标来自服务端 TCP 栈与客户端播放器（L36、L257 的 500 ms 桶），**无包级时延/队列观测**；不能反解链路级排队过程。
6. **时间绑定**：增长分析 2022-01–2024-04（L34），QoE 主口径为 2024-04 第一周（L80），A/B 为 2024-04 中一周（L226）→ 绝对数值不可外推到其它时期。
7. **LEO 特异性不可外推**：L54 `We limit our study to Starlink, as not enough users stream Netflix over other LEO networks to garner a suficiently large sample size.`
8. **自述的 ABR 现状**：L323 `only one LEO-optimized ABR exists: Zhao [59] designed an ABR algorithm specific for Starlink, but it sufers from increased bitrate switches and an undesirable rebufer-quality tradeof` → LEO 专用算法尚无成功先例（对本选题是背景证据）。

---

## 5. L63JISQN — Making Sense of Constellations: Methodologies for Understanding Starlink's Scheduling Algorithms

**书目（逐字）**：L1 `# Making Sense of Constellations`；L3 `Methodologies for Understanding Starlink’s Scheduling Algorithms`；L5–L21 Hammas Bin Tanveer（University of Iowa）、Mike Puchol（Google X）、Rachee Singh（Cornell）、Antonio Bianchi（Purdue）、Rishab Nithyanand（University of Iowa）。
**已读范围**：L1–L149（全文正文：摘要 L15、引言 L17–L33、背景 L35–L45、流量工程证据 L47–L59、卫星分配识别 L61–L89、全局调度器 L91–L124、建模 L126–L141、相关工作 L143–L145、结论 L147–L149）。参考文献 L151–L200 未读（仅确认标题 L151）。

### 1) 测量/建模对象与条件（逐字+行号）

- L19（对象）：`we empirically uncover the scheduling algorithms used by the Starlink network by analyzing data from high-frequency measurements from four Starlink terminals (deployed both in the US and the EU) to servers co-located at their corresponding Point-of-Presence.`
- L49（装置，逐字）：`We perform our measurement using four Starlink terminals — one each in Western Europe, Northeast US, Midwest US, and Northwest US. To improve the precision of our measurements, we configured the Starlink router to operate in bridge mode and connected them to a dedicated Raspberry Pi via Ethernet.` … `The destination of our measurements were servers co-located at the Starlink PoPs assigned to the regions of our user terminals.`
- L51（**关键实验条件，逐字**）：`Packets were sent using iRTT [3] at the rate of 1 packet/20 ms and iPerf3 at a bandwidth of 50% of the upstream connection. These parameters were chosen because they allowed stable and reliable measurements of the Starlink network. At higher frequencies and bandwidths, the packet loss rates and measured round-trip times were highly variable even within the same measurement period.` … `the clocks of our vantage points and servers were routinely synchronized using NTP.`
- L65–L67（卫星识别方法）：`Obstruction maps are 123px x 123px, 2-dimensional images which mark the trajectory of satellites that recently served the user terminal.` … `We used starlink-grpc-tools [4] to extract the 2-d obstruction maps every 15 seconds from each terminal.` … `We use CelesTrak [2] to get the TLEs for Starlink satellites. Since these files only indicate satellite positions every six hours, we use the SGP4 satellite propagation algorithm [22] to calculate satellite positions`
- L71（XOR 隔离法）：`we perform an XOR operation on the obstruction map from 𝑥 and 𝑥 − 1 (i.e., the prior 15-second slot). This will result in the erasure of all satellite trajectories which were common to the two figures — leaving visible only the trajectory associated with the satellite connected to the terminal during slot 𝑥.` … `we perform a terminal reset every 10 minutes (since resetting the terminal starts a fresh gRPC map).`
- L89（识别精度校验）：`We validate our similarity matching via a manual (visual) pilot test study, in which the authors manually identified the best match between 500 sets of gRPC and TLE trajectories. The DTW similarity method and our manual tests overlapped on over 99% of all outcomes.`

### 2) 可引用的事实与数字（逐字+行号）

| # | 事实（逐字） | 行号 |
|---|---|---|
| 1 | **`It is immediately obvious that major changes in latency characteristics occur every 15 seconds — specifically, at the 12th, 27th, 42nd, and 57th second past every minute. Notably, these changes are observed from all our measured locations for all periods of time.`** | L57 |
| 2 | **`we are also able to confirm that the latency characteristics observed during these consecutive 15-second windows are statistically diferent (Mann-Whitney U test; p < .05) from each other for all locations and over the entire period of our measurements.`** | L57 |
| 3 | `these efects were noticed even when our terminals were running well under capacity` | L57 |
| 4 | **`This is because changes in satellite allocation occur every 15 seconds which is insuficient time to meaningfully cause impacts on performance due to change in satellite positions/distances.`** | L57 |
| 5 | `latency measurements the user terminal frequently form parallel bands that are a few milliseconds apart. These bands reflect evidence that radio frames are allocated to user terminals by an on-satellite controller in a somewhat round-robin fashion.` | L59 |
| 6 | `On average, there are 35–44 satellites in the field of view of a user terminal in any 15 second slot.` | L93 |
| 7 | `the median angle of elevation of selected satellites (solid lines) is 22.9°s higher than that of the available but unselected satellites (dotted lines). Although only 30% of all available satellites had their AOEs in 45° to 90° range, the global scheduler picked 80% of satellites from the range (averaged over all locations).` | L97 |
| 8 | `In other locations, 58% of satellites on average were available towards the north of the user terminals, however, the user terminal was mapped to satellites from the north 82% of the times.`；受阻终端对照 `The terminal in Ithaca was assigned only 9.7% of the satellites from the region compared to 55.4% on average by user terminals in other locations.` | L99 |
| 9 | `Averaged over all locations, the probability of picking a satellite increases with an increase of one month in the satellite’s launch date.` | L111 |
| 10 | **`During such slots, the global scheduler opts for the sunlit satellites 72.3% of the time averaged over all locations. We also find that the global scheduler only picks dark satellites during 15 second slots where the %(dark/available) satellites is >= 35% (averaged over all locations).`** … `We find that the AOE of dark satellites picked by the scheduler was 25 degrees higher than their sunlit counterparts.` | L122 |
| 11 | `As a Starlink satellite has a service lifetime of about 5 years` | L113 |
| 12 | `The Starlink constellation consists of more than 4,000 satellites which were released in batches since 2018.` | L111 |
| 13 | `A Starlink satellite connects to multiple user terminals at a time. They allocate radio frames to user terminals mapped to them to exchange data.` | L43 |
| 14 | `Terminals can connect to any satellite at an angle of elevation higher than 25°s` … `While tens of satellites satisfy the angle of elevation constraints, a terminal can connect to only one satellite at a time.` | L41 |
| 15 | `The proposed model significantly outperforms the baseline model and predicts the correct allocated satellite characteristics 65% of the time (𝑘=5 guesses), in comparison to the baseline of 22%.` | L134 |

### 3) 对"负载变化/突发/时延/到达率"的事实贡献

- **时延的确定性时间结构（对建模最关键）**：L57 —— 15 s 周期、**相位固定**（每分钟第 12/27/42/57 秒）、**统计显著**（Mann-Whitney U, p<.05），且**在终端远未满载时依然出现**（L57 第 3 条）。→ 这是"**时延的结构性跳变与负载无关**"的直接实测证据，与 NPF75WS5 L228（15 s 全局同步、非切换导致）**独立互证**。
- **控制器分层与负载的关系**：L23 `First, a global network controller allocates a satellite to each user terminal based on a variety of factors including load, geospatial conditions, satellite charge, etc.`；L43 `This controller considers factors such as user priority, current load, and per-terminal flow characteristics when forwarding the trafic from user terminals to ground stations.` → **负载是调度器的输入（由 FCC 文件确认的机制描述），但本篇没有测量负载本身**。
- **突发/到达率**：**未见**。核验命令 `grep -ciE "arrival|offered load|load factor|burst|inter-?arrival|packet rate|traffic intensity|Erlang|congestion level"` → **count = 0**；`grep -ciE "time series|stochastic|Markov|queue|poisson"` → **count = 0**（范围=该篇 MD 全文 L1–L200）。
- **可测性的实测约束**：L51 —— 只有在 **1 packet/20 ms、50% 上行带宽** 的温和条件下数据才稳定；更高频/更高带宽下"even within the same measurement period"时延与丢包高度可变。→ **对"高负载下可测性"的实测约束**。

### 4) 能否作为定标或现象证据

- **LEO 实测 + 逆向工程**：4 个终端（US/EU）、毫秒级 iRTT、目的地在同 PoP（排除地面段）。
- **可作定标输入**：15 s 周期与相位（L57）、视场内卫星数 35–44（L93）、AOE 选择偏好（L97：中位高 22.9°、80% 选自 45°–90°）、北向偏好 82%（L99）、日照偏好 72.3% 与暗星阈值 35%（L122）。
- **可复用制品**：L141 `In order to facilitate future simulations and evaluations of the Starlink network, our model will be publicly available on paper acceptance.`（离线调度器近似模型，top-5 精度 65% vs 基线 22%，L134）→ **可直接作为我们仿真器的"时变星地关联"生成器**。
- **现象证据**：15 s 相位固定的确定性重配置是本批最强的"非随机时间结构"证据。

### 5) 边界与不可外推项

1. **样本极小**：4 个终端、4 个地点（L19、L49）→ 结论的统计基础是**空间 4 点**；L93 的 35–44 颗视场卫星为均值口径。
2. **终端被主动复位**：L71 `we perform a terminal reset every 10 minutes` → 观测窗口被人为切分为 10 分钟段，**长时间连续行为不可观测**。
3. **测量负载被人为压低**：L51 的 1 pkt/20 ms 与 50% 上行带宽是**为保证稳定而选的低强度条件**，故本篇**不能**给出高负载下的时延/丢包事实。
4. **调度器机制是"推断 + FCC 佐证"**：L21 `We were able to confirm the validity of these major findings using recent FCC filings by SpaceX [5].`；L57 亦为 `we conclude that our measurements have uncovered evidence of this scheduler`（证据式结论，非直接读取实现）。
5. **模型输入不完整（作者自述）**：L136 `we expect that other publicly-unavailable features such as terminal density in a region and satellite load characteristics will also impact the global scheduler. Therefore, the performance of our model is constrained by the unavailability of data.`
6. **模型时效性**：L141 未给出发布时间；L111 的"偏好新卫星"与 L113 的 5 年寿命推断绑定 2023 年星座状态 → **不可外推到其它年份**。
7. **未读部分**：参考文献 L151–L200（仅确认标题）。

---

## 6. GJJQUMQ2 — Deciphering Region-Level Signatures from Latency Measurements in LEO Satellite Internet

**书目（逐字）**：L1 `# Deciphering Region-Level Signatures from Latency Measurements in LEO Satellite Internet`；L3 `Xiang Shi, Yifei Zhang, and Peng Hu`；L5–L7 `Advanced Network and Embedded Systems Lab (AEL) / Dept. of Electrical and Computer Engineering, University of Manitoba, Winnipeg, Canada`。
**已读范围**：L1–L203（全文正文：摘要 L9、索引词 L11、引言 L13–L25、相关工作 L27–L33、问题形式化 L35–L43、框架 L45–L108、评测 L110–L200、结论 L201–L203）。参考文献 L205–L236 未读（仅确认标题 L205）。

### 1) 测量/建模对象与条件（逐字+行号）

- L9（对象）：`we formulate the problem of region-level latency characterization using Starlink round-trip time (RTT) measurements from the public LENS dataset.`
- L31（数据来源，逐字）：`LEOScope from the University of Surrey is the first testbed that enables the measurements of Starlink LEO satellite Internet at the global scale. Arising from this work, the LENS dataset [3] is one of LEO satellite network measurement datasets, containing fine-grained measurement observations. It provides geographically distributed Starlink dish measurements with timestamped RTT observations and point-of-presence (PoP) related deployment information`
- L116（样本选择，逐字）：`From the 30 Starlink dish measurement sites in the LENS dataset, we select dish measurement data from five different regions for analysis (e.g., Victoria, Ulukhaktok, Seattle, Bruhl, and Kanazawa).`
- L129（采样率与规模，逐字）：`In (1), N denotes the total number of samples within the file. The LENS measurement time interval is 10 ms, so the expected values of N are 360,000 (i.e., N = 100 × 60 × 60).`
- L49（特征框架）：`the framework consists of three stages: 1) segmenting the raw RTT sequence into non-overlapping one second (1-s) intervals and extracting primary statistical features, 2) aggregating these second-level features over 60 seconds (60-s) sliding windows to generate more stable secondary representations, and 3) using the resulting feature space for regional comparison, discriminative analysis, and downstream classification.`
- L61（样本数校验）：`Since the original RTT measurements are collected every 10 ms, each segment contains approximately 100 samples under normal conditions.`
- L170（训练/测试切分，逐字）：`The training dataset comprises RTT measurement data from five regions … over a six-day period (Jan 18–23, 2026). To evaluate the model’s short-term and long-term stability, the test datasets were selected from three independent test days: January 24th, 2026 (i.e., short-term), as well as February 4th and March 10th, 2026 (i.e., long-term).`
- L163（训练样本量）：`The LENS dataset is highly fine-grained (i.e., 10 ms intervals). Even after 60-s feature extraction, the six-day training dataset still remains around 8,640 samples.`

### 2) 可引用的事实与数字（逐字+行号）

| # | 事实（逐字） | 行号 |
|---|---|---|
| 1 | `While regions like Bruhl, Seattle, and Victoria maintain a minimum RTT of approximately 15-18 ms, Ulukhaktok stays within the 35-40 ms range.` | L133 |
| 2 | `the Ulukhaktok region shows a statistically significant separation from other regions, exhibiting consistently higher RTT values across all three features (e.g., minimum, median, and mean RTT).` | L133 |
| 3 | `the ground distance between Ulukhaktok’s dish and its associated Seattle PoP station is significantly greater than that of other regions. In summary, our empirical evidence directly confirms that regions with limited infrastructure and long ground distances between the dish and the PoP station lead to increased network latency` | L135 |
| 4 | `The rtt_s_min_w_min feature achieves the highest score, indicating that the minimum RTT has the strongest discriminative power regarding the target region. Conversely, rtt_s_mean_absdiff_mean and rtt_s_max_w_max exhibit the lowest scores` | L144 |
| 5 | **`The model achieves a high classification accuracy of 83% on the short-term test dataset. Its accuracy gradually declines on long-term test datasets.`** | L172 |
| 6 | `region 2 (i.e., Ulukhaktok) achieves the highest scores across all three test datasets.` … `the model encounters difficulty classifying between regions 0 and 1 (i.e., Bruhl and Seattle, respectively). This problem arises as the RTT distributions for the two regions are similar` | L174 |
| 7 | `Feature F10 (i.e., rtt_s_min_w_min) has the highest XGBoost importance and also exhibits the largest DI scores on both Feb.04 and Mar.10 long-term test datasets. This suggests that the minimum-RTT signature is highly discriminative but also temporally unstable.` | L200 |
| 8 | `the decreases in long-term accuracy are likely related not only to the model structure itself, but also to temporal distribution drifts in the latency features, which may be caused by changes in user demand, ground station/PoP status, network traffic, or other operational conditions.` | L200 |
| 9 | 波动度量公式（逐字 LaTeX，L95–L97）：`\delta _ { w } = \frac { 1 } { n _ { w } - 1 } \sum _ { k = 1 } ^ { n _ { w } - 1 } ( \mu _ { k + 1 } - \mu _ { k } ) ,`（原文为绝对值形式：左竖线 \mu_{k+1} - \mu_k 右竖线） | L96 |
| 10 | 主特征向量（逐字 LaTeX）：`\theta _ { k } = \big [ n _ { k } , \mu _ { k } , \sigma _ { k } , m _ { k } , \operatorname* { m i n } _ { k } , \operatorname* { m a x } _ { k } , q _ { k , 0 . 9 5 } , q _ { k , 0 . 9 9 } \big ] .` | L84 |
| 11 | `Packet loss is an inherent challenge in satellite networks. When packet loss occurs, the record entity is typically displayed as none (i.e., a missing value).` | L161 |
| 12 | **引述他人（非本篇实测，但是本批次的关键二手事实）**：`Go ing beyond large-scale RTT observation, Garcia et al. [6] provide a detailed characterization of Starlink one-way delay using high-frequency probe measurements, revealing minor diurnal variation, clear uplink/downlink asymmetry, and strong latency inflation during periodic 15-second reconfiguration events. Similarly, Casparsen et al. [7] develop a statistical framework for end-to-end latency characterization and prediction, showing that Starlink latency exhibits a repeatable 15-second structure with identifiable boundary spikes and stable intra-period behavior.` | L33 |
| 13 | **引述他人**：`WetLinks [9] offers a large-scale longitudinal Starlink dataset collected from two European vantage points over six months, comprising RTT, throughput, packet loss, traceroutes, and co-located weather measurements, which makes it particularly useful for studying long-term performance trends and weather effects.` | L31 |

### 3) 对"负载变化/突发/时延/到达率"的事实贡献

- **时延的区域性事实**：L133 —— min RTT 15–18 ms（Bruhl/Seattle/Victoria）vs 35–40 ms（Ulukhaktok，高纬/远 PoP）。**可直接引用的区域基线数值**。
- **最小 RTT 是最强判别特征**：L144、L187 `the importance score of the rtt s min w min feature is significantly higher than that of the other features.` → **对定标的口径建议：用 min RTT 而非均值做区域/链路基线**。
- **长期非平稳性（对 RL 泛化的直接证据）**：L172（83% → 长期下降）、L200（min-RTT 特征漂移最大，并把漂移归因于 `changes in user demand, ground station/PoP status, network traffic, or other operational conditions`）。→ "**同一区域同一特征分布随时间漂移**"的实测证据。
- **负载/突发/到达率**：**未见**。核验命令 `grep -ciE "arrival|offered load|load factor|burst|inter-?arrival|packet rate|traffic intensity|Erlang|congestion level"` → **count = 0**；`grep -ciE "time series|stochastic|Markov|queue|poisson"` → **count = 1**；命中行 L37（`Each region produces a high-frequency latency time series`）。**为何不构成反例**：该处是**对 RTT 序列的称呼**，无随机过程建模。全文以 RTT 统计特征为对象，不涉及负载过程。

### 4) 能否作为定标或现象证据

- **LEO 实测（二手数据再分析）**：数据为 LENS 数据集（L31），本篇**不采集数据**，只做特征工程与分类；是**对已公开实测数据的再分析**，而非新测量。
- **可作定标输入**：区域 min RTT 数值（L133）；采样口径（10 ms、360k 样本/小时，L129）；特征定义（L84、L96）。
- **现象证据**：区域间 min RTT 分离（L133–L135）；**长期漂移**（L200）。
- **不能作**：任何负载/到达率/队列相关定标（未测）。

### 5) 边界与不可外推项

1. **只有 5 个区域**：L116（Victoria、Ulukhaktok、Seattle、Bruhl、Kanazawa），且 Kanazawa 数据在 2026-01-25 后为空：L170 `Notably, the Kanazawa region’s RTT measurement data in the LENS dataset has been empty since January 25, 2026. Therefore, our long-term test datasets only include four regions.`
2. **时间窗口极短**：训练 6 天（2026-01-18–23），短测 1 天（01-24），长测 2 天（02-04、03-10）（L170）；跨区域比较用 7 天（L138 图题 `seven-day (Jan 18–24, 2026)`）→ **不能外推为季节/年度尺度**。
3. **数据缺口处理**：L161 丢包表现为缺失值，靠 XGBoost 稀疏感知分裂处理（`XGBoost architecture employs the sparsity aware split finding algorithm for handling the missing values in the training data.`）→ **丢包率未被量化，只被当作缺失**；本选题若要用丢包事实，**须另找来源**。
4. **模型精度非物理结论**：83%（L172）是**区域分类**精度，不等于对时延的预测能力；作者亦自述 `improving long-term accuracy remains a challenge`（L203）。
5. **未纳入的变量**：L142 `we performed label encoding on the target variable and filtered out redundant features (e.g., timestamps and distance) from the dataset` → 距离被人为剔除（仅用于解释性讨论），故 L135 的距离–时延关系是**定性推断**而非模型内因果。
6. **本条最关键外推风险**：篇章结论中 `network traffic` 仅作为**漂移的可能原因之一**出现（L200），**无任何流量测量支撑** —— 引用时不得写成"该文测量了流量影响"。
7. **未读部分**：参考文献 L205–L236（仅确认标题 L205）。

---

## 7. 5HJ8ATR7 — Democratizing Direct-to-Cell Low Earth Orbit Satellite Networks

**书目（逐字）**：L1/L17 `# Democratizing Direct-to-Cell Low Earth Orbit Satellite Networks`；L3–L5 Lixin Liu / Yuanjie Li / Hewu Li 等（Tsinghua University；Zhongguancun Laboratory）；L7–L9 `This paper is included in the Proceedings of the 21st USENIX Symposium on Networked Systems Design and Implementation. April 16–18, 2024 Santa Clara, CA, USA`。
**已读范围**：L1–L395（摘要 L25、引言 L27–L42、多租户动因 L44–L73、挑战（实测）L92–L170、系统概述 L171–L189、MOSAIC 设计 L190–L292、部署 L271–L293、评测 L294–L371、局限 L372–L375、相关工作 L376–L395）。附录 A/B（L633–L650）与参考文献 L397–L632 未读。

### 1) 测量/建模对象与条件（逐字+行号）

- L25（对象）：`Multi-tenant Low Earth Orbit (LEO) satellites emerge as a cost-effective win-win solution for direct 4G/5G access to our regular phones/IoTs anywhere on Earth.` … `Our empirical study with real satellite data shows that, it restricts LEO satellites' serviceable areas, limits the use of available (possibly competitive) satellites, and suffers from signaling storms and dynamic many-to-many relationships in extreme LEO mobility.`
- L84（实测装置，图题）：`(a) Direct-to-cell UEs (b) Open probes [54] (c) Real satellite dataset`；L296 `large-scale what-if emulations driven by satellite data in Figure 3`
- L111/L114（实测 RTT 图题，逐字）：`(d) Starlink terminal's RTT w/o ISLs`；`(e) Starlink terminal's RTT w/ ISLs`；`(f) RTT between the user and its nearest ground station (w/ ISLs)`
- L296（评测方法，逐字）：`We evaluate MOSAIC using a combination of qualitative analysis, quantitative micro-benchmark test with our prototype in Figure 13, and large-scale what-if emulations driven by satellite data in Figure 3.`

### 2) 可引用的事实与数字（逐字+行号）

| # | 事实（逐字） | 行号 |
|---|---|---|
| 1 | `LEOs are highly crowded, with about 8,300 satellites [29] and 27,000 space junks [28], leading to 3,500–60,000 conjunction events per month [45, 46] and 24,410 collision avoidance maneuvers per year [47].` | L67 |
| 2 | `Traditional direct-to-cell satellites, such as Inmarsat [42], Thuraya [43], and Tiantong [44], operate in the geostationary orbit (GEO) at an altitude of 35,786 km.`；`modern satellites like Starlink [1, 2], Iridium [3, 4], Globalstar [5], AST [6, 7], and Lynk [8] operate in LEOs at the altitude of 340–2,000 km` | L52 |
| 3 | **`each 4G/5G IQ sample should be delivered to the ground station within 250 microseconds, which accounts for 80 km distance between the satellite and ground station [56]. This stringent deadline is unsatisfiable for LEO satellites, whose distance to ground stations is at least 340 km.`**（原文为微秒符号） | L128 |
| 4 | **`Each transparent LEO satellite relays all serving UEs' IQ samples to ground stations for processing, which requires 7.86 Gbps for a typical 5 MHz radio channel [58].`** … `all these satellites' IQ samples to remote ground stations will accumulate and congest ISLs (typically with 20 Gbps capacity [59, 60])` | L130 |
| 5 | **`Each LEO satellite has a short-lived coverage for each area due to its fast mobility (e.g., 3 minutes for a Starlink satellite at 7.6km/s).`** | L149 |
| 6 | `compared to NTN, MOSAIC's localized service setup reduces signaling latency by up to 5.19 , 1.33 , and 2.33 in Starlink, Globalstar, and Iridium, respectively.`（原文倍数字符缺失，见第 5 项边界第 3 条） | L332 |
| 7 | `MOSAIC reduces CPU cycles by 100 , 63 , and 73 in Starlink, Globalstar, and Iridium, respectively.` | L336 |
| 8 | `each token's consumption latency is 16.4 ms, 41.9 ms, and 34.8 ms in Starlink, Globalstar, and Iridium, respectively.` | L340 |
| 9 | `Each SIM card can store 3,279-19,661 tokens' 160-bit metadata o2.` … `each MNO in this setup can generate 1,175 tokens/s (Figure 11a) and verify 1,401 tokens/s (Figure 11c) on average.` | L349–L351 |
| 10 | `Figure 16 compares the paging load assuming 5MHz 4G/5G radio bands for each satellite and 400 UEs/km2 by following [91]. Compared to NTN and SpaceCore, MOSAIC reduces paging channel load by 23 , 4 , 8 in Starlink, Globalstar, and Iridium, respectively.` | L359 |
| 11 | `we define each LEO constellation's cellular service ratio as h = Areas with functional satellite 4G/5G over Total areas covered by all satellites` | L334 |
| 12 | `Figure 21 quantifies these costs assuming two SNOs (Starlink and Iridium) with ISLs. Compared to the state-of-the-art, MOSAIC saves 850–7,640 signaling costs and 4.71–14.25 latencies due to its local in-band control.` | L370 |
| 13 | `the LEO satellites that each MNO and UE can employ change over time due to their transient coverage, some of which can be untrusted.` | L169 |

### 3) 对"负载变化/突发/时延/到达率"的事实贡献

- **负载相关的唯一定量事实是"带宽需求"而非"到达过程"**：L130 —— 单颗透明管道 LEO 卫星需 **7.86 Gbps**（5 MHz 信道）而 ISL 容量约 **20 Gbps**，即"IQ 汇聚会拥塞 ISL"。这是**容量/负载比**的工程事实，可作**拓扑容量定标**，但它不是测得的流量过程。
- **时延事实**：L128（250 微秒处理截止时间 vs 340 km 最小星地距离，物理不可满足）、L332（服务建立时延降低倍数）、L340（token 消耗时延 16.4 / 41.9 / 34.8 ms）。
- **时间尺度事实（对 LEO 动态建模有用）**：L149 —— 单颗 Starlink 卫星对某区域覆盖约 **3 分钟**（速度 7.6 km/s）；L165/L167 描述 MNO–SNO–UE 多对多关系的动态性。
- **突发/到达率**：**未见**。核验命令 `grep -ciE "arrival|offered load|load factor|burst|inter-?arrival|packet rate|traffic intensity|Erlang|congestion level"` → **count = 0**；`grep -ciE "time series|stochastic|Markov|queue|poisson"` → **count = 0**（范围=该篇 MD 全文 L1–L681）。

### 4) 能否作为定标或现象证据

- **不是流量测量论文**：证据为 `real satellite data`（L25/L296）驱动的 **what-if 仿真** + 原型微基准；**无真实用户流量统计**。
- **可作定标输入**：ISL 容量 20 Gbps 与 IQ 需求 7.86 Gbps（L130）、星地距离至少 340 km 与 250 微秒截止（L128）、卫星覆盖 3 分钟（L149）、LEO 高度 340–2,000 km（L52）。
- **可作现象/背景证据**：直连手机（direct-to-cell）是 LEO 的新增长方向（L29、L73），并且**现有多租户方案尚不支持**（L94 `The ongoing direct-to-cell satellite solutions under development, such as Starlink [34–36] and 3GPP NTN [16–27], have not started to support multi-tenancy.`）。
- **对本选题的价值**：提供"星上处理 vs 透明管道"的约束边界（L128、L130），说明 **LEO 星上处理能力是硬约束**——建模队列时不能忽略的物理上限。

### 5) 边界与不可外推项

1. **评测主体是设计而非网络测量**：L296 明示三类手段（定性比较、原型微基准、数据驱动 what-if 仿真），**无端到端流量实验**。
2. **平台对象不是路由**：本篇是**接入与多租户**（token/信令/寻呼），与路由/负载均衡无直接关系；**不得**据此推断任何路由结论。
3. **数字口径为"相对倍数"**：L332、L336、L359、L370 多数为**相对 SOTA 的改进倍数**（原文乘号字符在 MD 中缺失，表现为数字后空格），**不是绝对时延**，引用时不得写成绝对 ms。
4. **卫星数据集为第三方公开数据**：L296 的 `satellite data in Figure 3` 来自公开探测数据（L81–L84），精度受该数据源限制。
5. **作者自述局限**：L374 `(1) For SNOs, while MOSAIC's pay-as-you-go token grants service access, it does not guarantee verifiable carrier-grade service. Selfish SNOs may not offer carrier-grade services after gaining tokens, thus causing overbilling.`
6. **未读部分**：附录 A（安全性分析 L633–L643）、附录 B（缩写 L645–L650）、参考文献 L397–L632。

---

## 8. AZ72LM9Z — Towards Global Outage Detection for LEO Networks

**书目（逐字）**：L1 `# Towards Global Outage Detection for LEO Networks`；L3–L17 Manda Tran / Dylan Truong / Khiet Huynh / Sirapop Theeranantachai / Dravya Jain / Beichuan Zhang / Lixia Zhang / Liz Izhikevich（UCLA / University of Arizona）；L33 `In 3rd Workshop on LEO Networking and Communication (LEO-Net '25), September 8–11, 2025, Coimbra, Portugal.`
**已读范围**：L1–L266（全文：摘要 L21、引言 L35–L52、背景 L57–L65、同时测量 L67–L128、全球中断分析 L130–L153、相关工作 L155–L163、结论 L165–L167、附录 A L229–L266）。参考文献 L169–L227 未读（仅确认标题 L169）。

### 1) 测量/建模对象与条件（逐字+行号）

- L21（对象）：`We present Roman-HitchHiking, a system for measuring LEO satellite outages globally and in near-real time.`
- L61（**中断定义，逐字**）：`We define an outage as a period of time in which the Starlink client is unresponsive to the Starlink pre-satellite hop router.`；并对照官方定义：`Starlink's Service Level Agreement defines an "outage" as ". . . a period where the Starlink is unable to send/receive pings to/from servers at a Starlink Point of Presence" [27]. In this paper, we employ a narrower definition`
- L63（方法，逐字）：`HitchHiking first identifies the pre-satellite hop using ICMP Paris traceroute.` … `A TTL-limited ping is then used to isolate latency at specific hops: one ping targets the pre-satellite hop, and another the client dish. The diference in latency estimates the satellite link delay.`
- L96（采集工具，逐字）：`we use Censys [5, 8] to find exposed Starlink services. We filter exposed services for customer endpoints and exclude endpoints using performance enhancing proxies (PEP) [13]. We use Scamper [4, 18] to run Paris traceroutes to determine the pre-satellite hop.`
- L134（数据窗口，逐字）：`we collect data using Roman-HitchHiking with 8 source IPs for a 5 minute sample, probing at a one-second interval on three diferent days (May 27-29, 2025). We geolocate the customer endpoints using Starlink's published IP Geolocation feed [25].`
- L109（中断时长口径，逐字）：`we focus on sustained outages over 5 seconds and over 15 seconds long. We choose durations over 5 seconds because it is the maximum outage length Starlink's mobile app categorizes (0.1s+, 2s+, and 5s+). We also eval uate outages over 15 seconds because prior work has shown that Starlink has a 15 second reconfiguration period [20]. If an outage persists for more than 15 seconds, it suggests that even satellite handovers failed to resolve the issue.`

### 2) 可引用的事实与数字（逐字+行号）

| # | 事实（逐字） | 行号 |
|---|---|---|
| 1 | **`Roman-HitchHiking reduces measurement-induced packet loss from 73.4%—as seen in prior methods—to under 0.01%, enabling over four orders of magnitude greater coverage`** | L52 |
| 2 | `Figure 4 shows that packet loss rates in the naive setup can reach 79.7%. By removing redundant probes to the same pre-satellite hop and distributing probes across multiple source IPs, Roman-HitchHiking reduces packet loss to just 0.01%—a four-order-of-magnitude improvement.` | L98 |
| 3 | `while eliminating redundant probes reduces loss by a factor of 1.93, Roman-HitchHiking still experiences a packet loss rate of 37.9% when using a single source IP` | L100 |
| 4 | **`Many exposed customer services converge on the same pre-satellite hop router—in the worst case, up to 288 customers share a router in our experiment`** | L86 |
| 5 | `Figure 3 shows that packet loss significantly increases when probing more than 4 customers per /24` | L82 |
| 6 | `among the 1,092 overlapping customers between experimental configurations, the Jaccard Similarity between the Naive and Roman Large configurations is 0.85 for 5-second outages and 0.88 for 15-second outages`；跨 vantage point 对照 `With 1,265 overlapping customers, we again observe a Jaccard Similarity of 0.88 for both 5 and 15-second outages` | L115 |
| 7 | **`Across our datasets, we observe 812 outage events longer than 5 seconds on May 27, 344 on May 28, and 574 on May 29. Most outages last under 60 seconds, but many fall in the 50–75 second range—long enough to afect applications like video calls or gaming.`** | L136 |
| 8 | **`On May 27, 597 outages occurred simultaneously, each lasting between 70 and 75 seconds—accounting for 73.5% of all outages that day. On May 29, we observe two similar clusters of outages lasting 50–55 seconds and 70–75 seconds, respectively, with both groups overlapping in time. These events suggest centralized failures, likely at the satellite link level, that afect many users at once.`** | L141 |
| 9 | `the May 27 event impacted 64% of afected users in Chile, 10% in Argentina, and 18% in Australia. On May 29, the 50–55 second outages afected 38% of users in Mexico, while 34% of the 70–75 second outages occurred in Virginia, United States.` | L149 |
| 10 | `Australia experiences more frequent and longer outages than any other region in our dataset. In every measurement sample, Australia ranks among the most afected countries, both in number and duration of outages.` | L151 |
| 11 | `the majority of the measurements have <1ms standard deviation from the mean RTT` | L239 |
| 12 | `Our analysis reveals large clusters of simultaneous outages account for most disruptions, with Australia consistently among the most impacted areas.` | L52 |
| 13 | 中断类型四分类（逐字，附录 A.3）：`Success: The endpoint and its corresponding pre-satellite hop are both reachable` / `Outage: The pre-satellite hop are reachable, but the endpoint is not. This indicates a potential disruption in the satellite segment` / `Loss: Neither the pre-satellite hop nor the endpoint is reachable. This represents a complete failure in the measurement path.` / `Pre-satellite failure: The endpoint is reachable, but the presatellite hop is not.` | L257–L263 |

### 3) 对"负载变化/突发/时延/到达率"的事实贡献

- **本篇的核心贡献不是负载，而是"中断的时间结构"**，但对本选题**极为关键**：
  - **中断是"同时性簇"**：L141（597 个中断同时发生、持续 70–75 s、占当日 73.5%）；L149（跨大洲同时受影响）→ **失败事件在时间上强相关，不是独立泊松**。这直接反驳"每包独立失败"的建模假设。
  - **中断时长分布**：L136（大多数 < 60 s，很多落在 50–75 s）；L109（口径：>5 s 与 >15 s 阈值）。
  - **与 15 s 重配置周期的关系**：L109 逐字把 15 s 作为"若中断超过 15 s 则说明连切换都救不回来"的判据。
- **测量本身对网络的负载影响（罕见但重要的自省）**：L52/L98/L100 —— 朴素探测方案自身造成 **73.4%–79.7%** 的探测性丢包；**同一前置路由器最多被 288 个客户共享**（L86）；每 /24 超过 4 个客户就开始丢包（L82）。→ **"测量即干扰"在本篇被量化**，对设计负载实验有直接警示意义。
- **到达率**：**未见**。核验命令 `grep -ciE "arrival|offered load|load factor|burst|inter-?arrival|packet rate|traffic intensity|Erlang|congestion level"` → **count = 0**；`grep -ciE "time series|stochastic|Markov|queue|poisson"` → **count = 0**（范围=该篇 MD 全文 L1–L266）。

### 4) 能否作为定标或现象证据

- **LEO 实测**：真实 Starlink 客户端点、3 天（2025-05-27–29）、1 秒间隔探测（L134）、8 个源 IP。
- **可作定标输入**：中断事件计数与时长（L136、L141）；探测丢包率与采样密度关系（L82、L98、L100）；前置路由器共享度（L86：最坏 288 客户/路由器）。
- **可作现象证据**：**"失败事件成簇且跨地域同步"**是本批最重要的负面事实之一——任何"独立同分布丢包/超时"的建模都需要正面处理它。
- **不能作**：任何负载/到达率定标。

### 5) 边界与不可外推项

1. **无地面真值（作者自述，逐字）**：L119 `Obtaining ground truth for Starlink outages is challenging due to the scarcity ofpublic measurement data, limited access to communityoperated vantage points, and the absence of our own hardware deployment.` … `we examined RIPE Atlas [1], but found that its measurement granularity was too coarse to capture the transient, sub-minute outages that Roman-HitchHiking targets. Second, we considered using LEOScope [17] nodes; however, at the time of our measurements, only three nodes were active, none of which exposed public IPs`
2. **单向测量，无法区分方向**：L65 `since we are only conducting one-way measurements from the "outside-in," an unresponsive client can indicate that they are unable to send or receive pings from our server, but we cannot distinguish between the two.`
3. **中断定义比官方窄**：L61。
4. **时间窗口极短**：3 天、每日 5 分钟采样（L134）→ **不可外推为长期中断率**；作者也只做"日级簇"描述。
5. **采样本身有过滤风险**：L100 `such losses suggest filtering behavior at the source IP level`，已用 8 源 IP 缓解（L105）。
6. **未读部分**：参考文献 L169–L227。

---

## 9. W6M3GU7L — A Characterization of Route Variability in LEO Satellite Networks

**书目（逐字）**：L1 `# A Characterization of Route Variability in LEO Satellite Networks`；L3 `Vaibhav Bhosale, Ahmed Saeed, Ketan Bhardwaj, and Ada Gavrilovska`；L5 `Georgia Institute of Technology`。
**已读范围**：L1–L334（摘要 L9、引言 L11–L21、背景 L23–L73、研究设置 L75–L80、路由抖动 L81–L165、RTT 变异性 L167–L311、讨论 L313–L322、相关工作 L323–L330、结论起始 L331–L334）。参考文献 L339–L510 未读（仅确认标题 L339）。

### 1) 测量/建模对象与条件（逐字+行号）

- L9（对象）：`In this paper, we provide a thorough characterization of route variability in LEO satellite networks, focusing on route churn and RTT variability.`
- L77（仿真工具，逐字）：`Our study relies on simulations performed using the Hypatia framework [46] as the starting point, augmenting it with additional emulators as needed for the purposes of our study. We leverage Hypatia to generate the Two Line Element (TLE) information for satellites`
- L79（星座与时长，逐字）：`We predominantly use the first shell of the Starlink constellation, as it is the main fully-deployed constellation in practice. We also use the first shells from the Kuiper and Telesat constellations to show that our conclusions hold across constellations. We report our simulation results for a simulated period of 100 minutes for the Starlink and Kuiper constellations and 110 minutes for the Telesat constellation.`
- L97（样本口径）：`We look at paths used by all the source-destination pairs from the top 100 cities in the first shells of the Starlink, Kuiper and Telesat constellations.`
- L152/L157（拥塞控制实验条件，逐字）：`We consider the link utilization, the 95th percentile delay, and the power defined as the ratio of utilization to the 95th percentile delay exhibited by different congestion control protocols. We look at the route between Pune, India and Lahore, Pakistan.` … `Figure 10 shows the delays for the 60 seconds time interval we use for this experiment. Instead of assigning a different bandwidth value for every path, we select two bandwidth levels that we alternate between with every path change`

### 2) 可引用的事实与数字（逐字+行号）

| # | 事实（逐字） | 行号 |
|---|---|---|
| 1 | **`we find that 15% of paths selected by the routing algorithm are used for less than 10 seconds. Further, we show that more than 50% of paths selected by the routing algorithm are used for less than half of their lifetime.`** | L17 |
| 2 | `we observe that the smallest achievable RTT between a pair of ground stations can grow by up to 2.5x as satellites move in their orbits. Further, we found that this RTT variability is predictable – it correlates with the location of ground stations, exhibiting a spatial structure (§5). In particular, we find the variability to be high only when the communicating ground stations are within 1500-3000km of each other and the travel direction between them isn't along any of the orbital planes.`（原文为乘号字符） | L19 |
| 3 | **`we measure RTT variability in a constellation as we add orbital shells. Simply adding orbital shells doesn't reduce RTT variability, with variability depending on the exact configuration of each shell (i.e., the number of satellites and orbits and the inclination of orbits).`** | L21 |
| 4 | `we observe that 15% and 20% of paths are used for less than 10 seconds in Starlink and Kuiper, respectively. This percentage is lower at around 8% in Telesat because it operates at a higher altitude` | L99 |
| 5 | `for the three constellations, at least 50% of the paths are used for less than half of their lifetime.` | L111 |
| 6 | **`highlighting that for 70% of them abandoning a path yields a maximum of 25% reduction in latency.`**；`highlighting that 70% of them are abandoned for more than than half of their lifetime.` | L123–L124 |
| 7 | `Figure 6b shows that 70% of longest shortest paths are used for less than half of their lifetime (while 70% of them are only 25% longer than the best possible RTT as shown in Figure 6a). This implies that even if longest shortest path were to be abandoned for the maximum possible gain, that gain in most cases will be modest.` | L131 |
| 8 | **`The purple path is abandoned by all connections for the yellow path for about half a millisecond lower latency`**；图题 `All pairs take the same path.` | L147/L150 |
| 9 | `BBR [23] achieves high bandwidth utilization, while introducing a significant delay. On the other hand, Vegas [21] consistently achieves the lowest utilization with fairly low delays. PCC-Allegro [27] and PCC-Vivace [28] generally show utilization in the range 60−85%, while incurring fairly lower delays.` | L159 |
| 10 | `The figure shows that the lifetime of a GSL can be as low as 6 seconds, with a maximum of 4.5 minutes.` | L206 |
| 11 | `there are two types of inter-orbit ISLs: one with a median length of about 760 km and the other at 1384 km.` … `intra-orbit ISLs are uniform with all their lengths at about 1970 km, which is about 150% more than the first cluster of the inter-orbit ISLs` | L195 |
| 12 | `The length of the other 50% of inter-orbit ISLs can change by up to 21% due to the varying distances between different orbital planes across latitudes` | L197 |
| 13 | `The lengths of GSLs are uniformly distributed between a minimum of 550 km to a maximum of 1254 km` | L208 |
| 14 | `we find that a path change ... can further increase the length of the path by up to 2600 km, which could potentially double the length of the path.` | L250 |
| 15 | **`we can infer that simply increasing the number of satellites doesn't help solve this problem. With approximately the same number of satellites, Starlink V1 can provide improved performance over Starlink V2 due to higher altitudes and a greater diversity in the inclination angles.`** | L300 |
| 16 | `a satellite is visible for a maximum of 10-12 minutes from any point on earth`；`A LEO satellite travels at about 27,000 km/hr` | L50 |
| 17 | `Increasing the number of shells`（Fig. 22a 图题）与 L311 `increasing the number of shells while varying the inclination angles can reduce RTT variability by 3x`（原文为乘号字符） | L305/L311 |

### 3) 对"负载变化/突发/时延/到达率"的事实贡献

- **本篇不含任何负载/到达率测量**（仿真只产生拓扑与 RTT），但给出**时延变异性的结构**：
  - **RTT 可变性有空间结构**（L19、L173、L178），不是随机噪声；**比例上限 2.5 倍**。
  - **路径使用时长分布**（L99、L111、L123/L124）→ 直接决定"**一条路径能用多久**"，这是任何路由策略**动作驻留时间**的物理上界。
- **对"负载"的唯一贡献是间接的**：L145–L150 的羊群效应——**贪婪最短时延把所有连接挤到同一条路径**（`All pairs take the same path.`），而差异只有 0.5 ms（L147）。→ **"逐流最优化导致拥塞崩溃"的机理证据**，可作负载均衡动机引用。
- **拥塞控制的 tradeoff（可引）**：L159、L163（Table 2：利用率、P95 单向时延、power 比值）→ 无单一算法同时最优化时延与利用率；L163 图题 `No single algorithm optimizes both delay and utilization.`
- **突发/到达率**：**未见**。核验命令 `grep -ciE "arrival|offered load|load factor|burst|inter-?arrival|packet rate|traffic intensity|Erlang|congestion level"` → **count = 0**；`grep -ciE "time series|stochastic|Markov|queue|poisson"` → **count = 2**；命中行 L136（`Figure 7 shows a time series of RTT values`）与 L157（`we select two bandwidth levels that we alternate between with every path change`）。**为何不构成反例**：L136 是 RTT 时序的描述性用语；L157 是带宽档位交替的实验设定，**均无随机过程/排队模型**。

### 4) 能否作为定标或现象证据

- **纯仿真（Hypatia / ns-3）**，非 LEO 实测；但它是本批唯一对"路由抖动"给出定量刻画的仿真工作。
- **可作定标输入（用于环境设计）**：路径使用时长分布（L99/L111）、GSL 生存期 6 s–4.5 min（L206）、ISL 长度三档 760/1384/1970 km（L195）、GSL 长度 550–1254 km（L208）、RTT 变异上限 2.5 倍与其地理条件（1500–3000 km 且非沿轨道面，L19）。
- **可作现象证据**：**"短时最优点会引发全局拥挤"**（L147）与 **"加卫星不必然降变异"**（L21、L300）两条反直觉结论。
- **不可作**：任何实测时延/负载定标（全为仿真）；**也不覆盖 ISL 故障/中断**（无故障注入，L157 只做带宽档位切换）。

### 5) 边界与不可外推项

1. **纯仿真，且本篇未见独立实测校验章节**（检索范围=该篇 MD 全文，检索词 `grep -niE "testbed|real-world measurement|ground truth|we measure from"` → 未出现作为独立校验的实验节；L77 明示仅用 Hypatia + TLE）。
2. **拓扑假设单一**：L315 `our simulations use a specific variant of the +Grid topology`；L296 `Since each satellite currently has only 4 lasers to support 4 ISLs, we assume that they are utilized to setup a +Grid leading to individual shells operating independently.` → **跨壳 ISL 被假设为不连接**。
3. **仿真时长 100–110 分钟**（L79）→ 只覆盖约一个轨道周期；**无昼夜/长期行为**。
4. **地面站选取受限**：L97（top 100 城市）；L294 `we use the global 100 most populous cities as the ground s...` → 对**地面站稀疏区域外推需谨慎**。
5. **拥塞控制实验是人为构造**：L157 `we select two bandwidth levels that we alternate between with every path change` → 带宽变化为**人为注入**。
6. **未读部分**：结论 L331–L334 的末尾与参考文献 L339–L510。

---

## 10. DS9SPARV — OpenSN: An Open Source Library for Emulating LEO Satellite Networks

**书目（逐字）**：L1 `# OpenSN: An Open Source Library for Emulating LEO Satellite Networks`；L3 `Wenhao Lu, Zhiyuan Wang, Hefan Zhang, Shan Zhang, and Hongbin Luo`。
**已读范围**：L1–L455（摘要 L5、引言 L9–L37、文献综述 L39–L70、框架 L71–L240、用法 L241–L317、性能评测 L318–L442、结论与未来工作 L443–L455）。参考文献 L457–L593 未读（仅确认标题 L457）。平台类章节（L89–L240 的 eBPF/多机扩展细节）为略读。

### 1) 测量/建模对象与条件（逐字+行号）

- L5（对象，逐字）：`In this paper, we present OpenSN, i.e., an open source library for emulating large-scale satellite network (SN). Different from Mininet-based SN emulators (e.g., LeoEM), OpenSN adopts container-based virtualizat`（摘要在此处被 MD 截断）
- L322（硬件条件，逐字）：`We build the experimental environment based on three DELL R7840 Servers with Intel(R) Xeon(R) Gold 5218 CPU and 191.5 GB memory in each.`
- L342（对照实验条件）：`For OpenSN and StarryNet, we use a three-VM cluster with a total of 48 vCPU and 96GB memory. For LeoEM (or equivalently Mininet), we use a single VM with a total of 48 vCPU and 96GB memory, since it does not support multi-machine extension.`
- L346（星座规模，逐字）：`Each subfigure contains the results of four typical constellations, i.e., Iridium (6 x 11), OneWeb (18 x 40), Kuiper (34 x 34), and Starlink Shell-I (72x22).`
- L436（五星座案例，逐字）：`To verify the scalability of OpenSN, we emulate the fiveshell Starlink constellation shown in Table IV. It poses significant challenges to emulate Starlink constellation with five shells due to our limited hardware resources (96 cores and 256 GB memory).`

### 2) 可引用的事实与数字（逐字+行号）

| # | 事实（逐字） | 行号 |
|---|---|---|
| 1 | `OpenSN is 2x faster than Mininet for configuring 10 GSL handovers and 4x faster for configuring 100 GSL handovers.`（原文为乘号字符） | L365 |
| 2 | `The CPU usage of OpenSN is rapidly increasing to 70% during the network construction (i.e., 0-200s). However, the CPU usage of StarryNet stays around 10%-40% during the network construction (i.e., 0-2100s).` | L381 |
| 3 | `OpenSN's CPU usage is gradually decreasing (to 30%) during the routing convergence period` … `StarryNet's CPU usage is still at a high level (i.e., around 70%) during the routing convergence period` | L383/L404 |
| 4 | `The routing converges at the 600-th second for Shell V, at the 800-th second Shell IV, at the 900-th second for S...`（五星座 Starlink 的分壳收敛时刻） | L441 |
| 5 | `During the construction stage (i.e., 0-250s), OpenSN builds the topology of the container network. During the configuration stage (i.e., 250-500s), OpenSN generates configuration files in each container` | L441 |
| 6 | `OpenSN's Container Runtime Manager replaces the CLI interaction with the official SDK, and also adopts a distributed architecture to aFchieve better parallelism.` | L35 |
| 7 | `LeoEM is developed by adding trajectory and route calculation to Mininet, but does not allow for distributed routing software. Hence the performance of LeoEM is similar to Mininet.` | L320 |
| 8 | `existing virtual-network SN emulators are not efficient enough to emulate frequent state changes (e.g., ISL failure/recovery and GSL handover), which slows down the experimental progress and prolongs the research period.` | L25 |
| 9 | 资源档位（逐字）：`Case A (32 vCPUs and 64 GB memory), Case B (48 vCPUs and 96 GB memory), and Case C (64 vCPUs and 128 GB memory)`；机器数档位 `Case I (one machine with 32 vCPUs and 64G memory), Case II (two machines with 16 vCPUs and 32G memory for each), and Case III (four machines with 8 vCPUs and 16G memory for each)` | L410/L414 |
| 10 | `the construction time increases as the number of kernel-threads increases` | L416 |
| 11 | `The convergence time is a critical metric for routing protocols. It is especially important for LEO satellite networks with topology dynamics.` | L451 |

### 3) 对"负载变化/突发/时延/到达率"的事实贡献

**本篇是平台论文，不含任何流量/到达率事实。** 对本批的贡献是**"能做多大规模、多快状态更新的实验"这一可行性边界**：
- 状态更新效率：L365（GSL 切换配置：10 次时比 Mininet 快 2 倍、100 次时快 4 倍）；L25（既有模拟器在 ISL 故障/恢复与 GSL 切换上的效率不足）；
- 规模上限：L436–L441（五壳 Starlink 需要 96 核 + 256 GB；分壳 OSPF 收敛在 600–900 秒量级）；
- 失败模式：L416（内核线程数越多，构建越慢）。
- **突发/到达率**：**未见**。核验命令 `grep -ciE "arrival|offered load|load factor|burst|inter-?arrival|packet rate|traffic intensity|Erlang|congestion level"` → **count = 2**；命中行 L436（`avoid burstlike resource preemption`）与另一处资源突发描述。**为何不构成反例**：该处指**系统资源占用的突发**（构建期资源抢占），与网络流量突发无关。`grep -ciE "time series|stochastic|Markov|queue|poisson"` → **count = 1**；命中行 L57（提及"排队/离散事件调度"的综述性表述），**无排队模型**。

### 4) 能否作为定标或现象证据

- **平台/仿真基础设施，非测量**。可作**我们平台选型的对照物**：OpenSN 用容器 + 真实内核协议栈（L29 `OpenSN is a virtual-network emulator, that runs real kernel and real applications.`）。
- **可复用的定量定标**：构建/析构时间随星座规模的变化（L330、L346）、GSL 切换配置的相对加速（L365）、路由收敛时间量级（L441）、资源下界（L436）。
- **不可作**：任何 LEO 现象证据（无实测、无真实网络数据）。

### 5) 边界与不可外推项

1. **无真实卫星网络校验**：全文评测为**模拟器之间的效率对比**（OpenSN vs StarryNet vs LeoEM/Mininet），L320–L322 明示对照对象；**无与真实 Starlink 的性能对照**。
2. **星座参数来自第三方**：L338 `Table IV shows the parameters of the LEO constellations used in our experiments.`（未在正文展开，参数来源需查 Table IV）。
3. **硬件强绑定**：所有结论在 3–4 台 Dell R7840（48–64 vCPU、96–128 GB）上取得（L322、L342、L373）→ **不可外推到其它规模**。
4. **协议栈假设**：L453 `OpenSN is now built on hostcentric IP networking architecture, which was initially designed for wired networks. The topology characteristics of LEO constellations are quite different from those of wired networks.`
5. **未读部分**：L89–L240 的框架细节（eBPF 链路、多机扩展）为略读；参考文献 L457–L593。

---

## 11. IEI3BYFF — STARRYNET: Empowering Researchers to Evaluate Futuristic Integrated Space and Terrestrial Networks

**书目（逐字）**：L3/L19 `# StarryNet: Empowering Researchers to Evaluate Futuristic Integrated Space and Terrestrial Networks`；L5 `Zeqi Lai and Hewu Li, Tsinghua University and Zhongguancun Laboratory; Yangtao Deng, Tsinghua University; Qian Wu, Jun Liu, and Yuanjie Li, Tsinghua University and Zhongguancun Laboratory`；L9–L11 `This paper is included in the Proceedings of the 20th USENIX Symposium on Networked Systems Design and Implementation. April 17–19, 2023 Boston, MA, USA`。
**已读范围**：L1–L50（题录、摘要 L27、引言 L31–L45）+ L176–L230（框架评测 L176–L216、案例研究 L218–L230）。L51–L175（预备知识/设计/实现）与 L230–L305（案例研究其余 + 局限）**未逐段读**；参考文献 L321–L490 未读。

### 1) 测量/建模对象与条件（逐字+行号）

- L29（对象，逐字）：`This paper presents STARRYNET, a novel experimentation framework that enables researchers to conveniently build credible and flexible experimental network environments (ENE) mimicking satellite dynamics and network behaviors of large-scale ISTNs. STARRYNET simultaneously achieves constellation-consistency, networked system realism and flexibility, by adopting a real-data-driven, lightweight-emulationaided approach to build a digital twin of physical ISTNs in the terrestrial virtual environment.`
- L192（**保真度校验的对象，逐字**）：`We leverage STARRYNET to establish an ENE following the network topology of a recent live Starlink test conducted in Europe in 2021 [33]. Specifically, this real-world Starlink topology involves several key components as illustrated in Figure 5: (1) a user terminal together with a Starlink satellite dish located at the campus Klagenfurt Primoschgasse; (2) a SpaceX's ground station located in Frankfurt,`
- L212（吞吐配置口径，逐字）：`we follow the realistic Starlink trace in [33] to set the uplink/downlink capacity, and run iPerf to measure the TCP throughput in each direction. Since Hypatia and StarPerf can not load real network traffic by iPerf, we compare the throughput results of`
- L214（ISL 拓扑的对照限制）：`As of the date of this paper submission, most real megaconstellations like Starlink and Kuiper are still in their early stage and under heavy construction. Although Starlink has started to deploy laser ISLs on its LEO satellites, those ISLs are still under internal test, and it is difficult to directly compare the network performance estimated by STARRYNET with a real ISL-enabled satellite network.`
- L178（硬件条件）：`Our framework evaluations are conducted on a typical enterprise cluster, including eight DELL ...`（行在 MD 中被截断）
- L228（案例研究条件，逐字）：`We establish an ENE based on Starlink's first constellation shell and its ground station distribution. We randomly pick geo-distributed user-pairs and establish communication sessions between these pairs over the satellite network. On each emulated satellite, we load BIRD [37] routing software and run OSPF a...`

### 2) 可引用的事实与数字（逐字+行号）

| # | 事实（逐字） | 行号 |
|---|---|---|
| 1 | `The emulated constellation size can scale from about`（L182，数字在 MD 折行处被截断） | L182 |
| 2 | `a researcher can easily establish each ENE listed in Table 2, by writing about a dozen lines of code based on constellation prefabs` | L184 |
| 3 | `when the constellation size increases, STARRYNET requires more worker machines, consuming more CPU/memory resources to emulate ISTN nodes, links, and their constellationwide dynamics. Second, if STARRYNET updates satellite dynamics more frequently (i.e., with shorter update intervals), i`（句尾被截断） | L186 |
| 4 | **`Where ground stations typically can not be deployed upon oceans (70% earth surface), SRGS suffers from the highest latency as compared with other schemes due to the insufficient deployment of ground ...`** | L230 |
| 5 | `We observe an obvious latency reduction accomplished by laser ISLs, and DASN obtains the lowest end-to-end latency on average.` | L230 |
| 6 | `Since Hypatia and StarPerf can not load real network traffic by iPerf` → 说明 STARRYNET 的**流量负载能力**是与纯模拟器的关键差别 | L212 |
| 7 | `Figure 7: Throughput comparison.` | L205 |

### 3) 对"负载变化/突发/时延/到达率"的事实贡献

- **可注入真实流量**（L212：用 iPerf 打真实 TCP 流，并跟随真实 Starlink trace 设定上下行容量）→ 这是本批**平台类工作里唯一明确支持"可加载真实流量"的能力描述**，对我们做负载实验**有直接工程价值**。
- **时延结论（案例研究）**：L230 —— ISL 显著降低时延；**DASN（直连卫星）平均端到端时延最低**；**SRGS 最差，原因是地面站不能部署在占地球表面 70% 的海洋上**。这是**"覆盖约束 → 时延"的定量化叙述**（但数字在 MD 折行处未给出）。
- **突发/到达率**：**未见**。核验命令 `grep -ciE "arrival|offered load|load factor|burst|inter-?arrival|packet rate|traffic intensity|Erlang|congestion level"` → **count = 0**；`grep -ciE "time series|stochastic|Markov|queue|poisson"` → **count = 0**（范围=该篇 MD 全文 L1–L490）。

### 4) 能否作为定标或现象证据

- **平台（数字孪生式仿真框架），非测量**；保真度校验**部分依赖真实 Starlink 拓扑与 trace**（L192、L212）。
- **可作平台能力证据**：支持 iPerf 真实流量、支持按需配置链路容量（L212 `STARRYNET allows the researcher to manually configure the link capacity on demand.`）、可用十几行代码建环境（L184）。
- **可作现象证据（弱）**：L230 的"地面站覆盖（海洋占 70%）→ SRGS 时延最差"。
- **不可作**：任何 LEO 实测时延/负载数值的定标（**本文未给出可抄录的数值**，且其保真度对照仅针对一条 2021 年的欧洲 Starlink 链路，L192）。

### 5) 边界与不可外推项

1. **保真度对照的样本极小**：**一条** 2021 年欧洲实测链路（L192）；且当时 **ISL 未被验证**（L214）。
2. **ISL 拓扑无法与真实对照**：L214 逐字（ISL 仍在内部测试）。
3. **本文的定位是"使能工具"**：L35–L45 反复强调"同时取得真实性与灵活性"的设计取舍，**不承担网络现象结论**。
4. **案例研究依赖人为构造**：L228（随机挑选地理分布的用户对、加载 BIRD/OSPF）→ 结果对**地面站分布假设**敏感。
5. **未读部分**：L51–L175（预备知识与设计细节）、L230–L305（案例研究其余、局限节 L295）、参考文献 L321–L490 —— **本篇为 T3 档中读得最浅的一篇，其后续引用需先补读 L230–L305 的数值**。

---

## 12. 8AYW2Y78 — Exploring the "Internet from space" with Hypatia

**书目（逐字）**：L1 `# Exploring the "Internet from space" with Hypatia`；L3 `Simon Kassing, Debopam Bhattacherjee, André Baptista Águas, Jens Eirik Saethre, Ankit Singla ETH Zürich`；L23 `In ACM Internet Measurement Conference (IMC '20), October 27–29, 2020, Virtual Event, USA.`
**已读范围**：L1–L40（题录、摘要 L7–L11、引言 L25–L27）+ L197–L350（§4 路径分析、§5 星座级视图）+ L389–L424（§7 局限、§8 结论、L408–L422 图题）。L55–L196（背景与架构、可扩展性）与 L350–L388（可视化节）未逐段读；参考文献 L428–L590 未读。

### 1) 测量/建模对象与条件（逐字+行号）

- L9（对象，逐字）：`To enable research in this exciting space, we present Hypatia, a framework for simulating and visualizing the network behavior of these constellations by incorporating their unique characteristics, such as high-velocity orbital motion.`
- L203（实验设置，逐字）：`These experiments use the Kuiper K1 shell. We run the analysis for 200 seconds, as for Kuiper-scale networks this is suficient to show nearly the full range of variations.`
- L205（测量口径，逐字）：`For each source-destination pair, s-d, s sends d a ping every 1 ms, and logs the response time. We also compare the measured RTTs to those generated using networkx computations for the same end-points, and the same constellation. For these networkx computations, we use snapshots ofthe system every 100 ms, and compute the shortest paths using the Floyd-Warshall algorithm.`
- L239/L241（**拥塞控制实验的负载条件，逐字**）：`we first use a congestion-free setting: the measured end-end connection is the only one sending trafic, with the rest of the network being entirely empty.` … `To make the simulations faster, the shown experiments use a 10 Mbps line-rate. The bufers are sized to 100 packets, i.e., 1 bandwidthdelay product (BDP) for 100 ms.`
- L243（队列设置，逐字）：`The network device queue size, Q, for both ISLs and GSLs is set to 100 packets.`
- L262（星座级口径）：`We use the world's 100 most populous cities as GSes, and examine connections between all pairs of GSes.`
- L333（带宽实验条件，逐字）：`We use the same LEO network as in §4, i.e., Kuiper's K1 shell, with each link in the network set to 10 Mbps capacity to allow us to scale the experiment.` … `From the random permutation matrix, we remove the pairs which have the same source or destination satellit...`

### 2) 可引用的事实与数字（逐字+行号）

| # | 事实（逐字） | 行号 |
|---|---|---|
| 1 | **`at t = 32.9 s the path changes, which causes the RTT to rise from 96 ms to 111 ms.`** | L207 |
| 2 | **`Across time, the Manila-Dalian path has a minimum RTT of 25 ms and a maximum RTT of 48 ms, thus changing by nearly 2x. For the Istanbul-Nairobi path, this RTT range is 47-70 ms.`**（原文为乘号字符） | L211 |
| 3 | `The path from Rio de Janeiro to St. Petersburg sees a disruption around 150 seconds into the simulation` … `For this period, St. Petersburg does not have any visible Kuiper satellites at suficiently high angle of elevation, which, obviously, results in the satellite network path being disconnected.` | L209 |
| 4 | **`the congestion window typically fluctuates between the BDP and BDP plus queue size (100 packets). However, in certain cases, when the RTT gets lower, reordering happens, and even though there is no loss, the congestion window is still halved.`** | L222 |
| 5 | `For all three constellations, more than 80% of connections see a maximum RTT less than 2x the geodesic.` | L268 |
| 6 | **`Telesat has the fewest satellites, with less than a third of Kuiper's and less than a fourth of Starlink's, and yet it achieves the lowest latencies for most connections. Starlink's latencies are also higher than Kuiper's.`** | L270 |
| 7 | `Telesat claims that it will use a much lower minimum angle of elevation, 10°, compared to Starlink (25°) and Kuiper (30°).` | L272 |
| 8 | `while Starlink sees the largest latency changes (∼10 ms in the median), th`（句尾被 MD 截断） | L276 |
| 9 | **`in the median, over the 200 s simulation, Starlink and Kuiper connections see 4 path changes, while Telesat connections see 2 changes.`** | L304 |
| 10 | `For Starlink, more than 10% of connections see more than 50% change in hop-count.` | L308 |
| 11 | `with paths changing multiple times per minute, and often by a substantial number and fraction of hops` | L310 |
| 12 | **`compared to 50 ms time-steps, 100 ms time-steps see roughly 2x the path changes, while 1000 ms see roughly 20x path changes.`** … `the 1000 ms time-step misses a substantial number ofpath changes for some pairs, while for 100 ms, missed changes are negligible.` | L321 |
| 13 | `given that path changes occur over tens of seconds, the 100 ms time-step can only be inaccurate and not provide the actual shortest paths for at most 1% of the time.` | L327 |
| 14 | **`despite the trafic matrix being fixed throughout our 200 s experiment, and the routing policy consistently being shortest path routing, the motion of satellites makes the path-level behavior highly dynamic.`** | L335 |
| 15 | **`in an LEO network with cross-trafic, the amount of unused bandwidth is larger than that in the static case.`** … `While there are short periods, such as around 20 s, where the full capacity of the path is used (together, by this connection and other cross-trafic), for a lot ...`（句尾被截断） | L339 |
| 16 | **`This implies that the trafic mix at any link is highly dynamic, making it dificult for transport to adapt`** | L341 |
| 17 | `The zigzags stem from the nature ofISLs in the topology — satellites which seem visually close to each other are not necessarily connected directly.` | L408 |
| 18 | `An example path, Chicago-Zhengzhou, shows how the link utilizations change over time, even with the input trafic being static. The top and bottom views are at 10 s and 150 s respectively.` | L411 |
| 19 | `On Kuiper, the transatlantic paths are highly congested for our tested trafic matrix. The red / thick ISLs are heavily utilized, while green / thin ISLs have minimal trafic.` | L422 |
| 20 | Takeaway 逐字：`Takeaway for congestion control: Both loss and delay can be poor signals for congestion control in LEO networks.` | L256 |
| 21 | Takeaway 逐字：`Takeaway for routing / TE: LEO networks present uncharted territory for routing and TE, and their interactions with transport. Trafic could potentially be moved away from links that will otherwise soon become bottlenecks due to changes in the set of end-end paths they serve.` | L348 |
| 22 | Takeaway 逐字：`Takeaway for applications: The maximum end-end RTT over time can be much higher than the minimum, and will determine the latency for jitter-sensitive applications.` | L235 |

### 3) 对"负载变化/突发/时延/到达率"的事实贡献

**本篇是本批唯一系统给出"负载/拥塞在 LEO 中如何失真"的仿真证据**，且给出可复算的设置与结论：

- **拥塞信号失真（核心事实）**：L222 —— **无丢包但因重排序导致拥塞窗口减半**；L254 逐字展开：`Loss, besides sufering from its well-known problem of only arising after bufers are full and latencies are inflated, is additionally vulnerable to being inferred incorrectly due to reorder ing. On the other hand, delay is also an unreliable signal because delay fluctuations occur even without`；L256 Takeaway。
- **负载下的时延膨胀**：L241（TCP 持续填满并排空缓冲 → RTT 上升）；L222（cwnd 在 BDP 与 BDP+Q 之间波动，Q=100 包，L243）。
- **"静态流量 + 动态拓扑"仍产生动态拥塞**：L335、L339、L341、L411、L422 → **拥塞的空间分布随卫星运动迁移**；L348 给出路由/TE 的应对方向（"提前把流量从即将成为瓶颈的链路移开"）。
- **时延变异性**：L207（96→111 ms 单次路径切换）、L211（Manila–Dalian 25–48 ms，约 2 倍；Istanbul–Nairobi 47–70 ms）、L268（>80% 连接的 max RTT < 2 倍 geodesic）、L270（Telesat 延迟最低）、L276（Starlink 中位延迟变化约 10 ms）。
- **路径变化率（对动作驻留时间的约束）**：L304（200 s 内中位 4 次路径变化）、L308（Starlink 超 10% 连接跳数变化超 50%）、L310（每分钟多次变化）、L321/L327（时间步长 100 ms 是合适折中）。
- **到达率**：**未见**。核验命令 `grep -ciE "arrival|offered load|load factor|burst|inter-?arrival|packet rate|traffic intensity|Erlang|congestion level"` → **count = 1**；命中行 L436（**该行属于参考文献/附录区**，非正文）。另一模式 `grep -ciE "time series|stochastic|Markov|queue|poisson"` → **count = 12**；命中集中在 L241–L243（`the bufers`、`queue size`、`queue capacity`）、L339–L343 与参考文献中的 queue/congestion 表述。**为何不构成反例**：全部为**队列容量与排队现象的机理描述**（固定队列 100 包、BDP+Q），**无到达过程建模、无到达率统计**。

### 4) 能否作为定标或现象证据

- **仿真（ns-3 + Hypatia），非 LEO 实测**；但它是**本批所有后续仿真工作的公共基线**（GGFJ3SEG 用它做对照并证明其**不捕获真实尖峰**：GGFJ3SEG L201 `Simulations do not capture the dynamics of real-world Starlink RTTs.`、L207 `No matter the ground station, Hypatia never predicts that a client experiences sustained RTT spikes`）。
- **可作定标输入（仿真环境）**：队列 100 包（L243）、链路 10 Mbps 与 200 s 仿真窗（L203、L333）、时间步长 100 ms 折中（L327）、RTT 变异倍率（L211、L268）、路径变化率（L304）。
- **可作现象证据（仿真级）**：**非拥塞性丢包/重排序导致的拥塞误判**（L222、L254）——这是"**为什么需要区分失败原因**"的仿真侧根因证据；以及"拓扑运动导致的拥塞迁移"（L335、L341）。
- **不可作**：真实 LEO 时延/负载的定标（GGFJ3SEG 已给出反证）。

### 5) 边界与不可外推项

1. **仿真，且作者自述局限（逐字）**：L393 `The most under-developed aspect is the radio GS-satellite segment design. It would help to frame more realistic models of the interfaces at both satellites and GSes, and for antenna gain and interference.`；L395 `The current model of ISLs is also somewhat simplistic, and it would be useful to model the impact of the Doppler efect on the bandwidth and reliability of ISLs.`；L397 `Incorporating a weather model would enable work on reliability and rerouting around bad weather.`
2. **星座参数来自申报文件**：L298 `We are evaluating constellations strictly from their filings, and it is unclear to us if some operators are more optimistic than others about the plausible design parameters; it is worth remembering that the filings are meant to secure radio spec`。
3. **外部实测反证（重要）**：GGFJ3SEG L207/L201（本批第 1 篇）证明 Hypatia **不预测持续 RTT 尖峰**、平均误差 7.6 ms、HitchHiking 精度高 1.8 倍 → **引用 Hypatia 的时延结论时必须同时引用该反证**。
4. **时间尺度**：仿真 200 s（L203、L333）→ 与 W6M3GU7L 的 100–110 分钟同属短窗；**无日/季节尺度**。
5. **队列与缓存设定固定**：L243（100 包）→ 结论对队列容量的敏感性未做扫描。
6. **未读部分**：L55–L196（背景与架构、可扩展性）、L350–L388（可视化）、参考文献 L428–L590。

---

## 13. 4QG5VYHQ — Information Freshness of Updates Sent over LEO Satellite Multi-Hop Networks

**书目（逐字）**：L1 `# Information Freshness of Updates Sent over LEO Satellite Multi-Hop Networks`；L3–L5 `Federico Chiariotti, Member, IEEE, Olga Vikhrova, Beatriz Soret, Member, IEEE, and Petar Popovski, Fellow, IEEE`。
**已读范围**：L1–L405（摘要 L9、引言 L11–L30、相关工作与贡献 L32–L54、系统模型 L56–L162、AoI 界与近似 L163–L314、数值评估 L315–L399、结论与未来工作 L400–L405）。参考文献 L406–L507 未读（仅确认标题 L406）。§IV 的推导细节（L195–L314）为选择性阅读。

### 1) 测量/建模对象与条件（逐字+行号）

- L9（对象，逐字）：`This paper analyzes the Age of Information (AoI) of a satellite network with multiple sources`（摘要首句）
- L21（场景，逐字）：`we address a general buffer-aided multi-hop network with multiple sources and destinations. We focus on applications where a number of mutually independent traffic sources need to report sensory updates to a number of control stations in a timely fashion, and do so through a chain of LEO satellites.`
- L58（**到达过程与负载定义，逐字**）：`We consider a connection composed of K links in a multi-hop mesh network in which each node in the network acts both as a source and a relay, as shown in Fig. 1. The source is modeled as a Poisson process, generating packets with rate \lambda. Each node k in the connection, including the source, receives Poisson cross traffic with rate $\theta _ { k }$.`
- L60（队列模型，逐字）：`We model a connection between a source and a destination as an $M / M / 1$ queueing network connected in series. In a real system, the service time for each link depends on the length of the packet and the quality of the link: in this work, we model the service time for each link for the same packet as independent for tractability.`
- L68/L73/L75（**上行接入与碰撞模型，逐字**）：`For a large number of intermittent transmitters in a single shared communication channel, the ALOHA protocol is the simplest one and it is widely used [45]. Rather than the conventional ALOHA implementation with a backoff mechanism to re-send colliding packets, a pure A...`；`Ideal Multi-Packet Reception (MPR). In this case [46] the packets are not lost due to collisions and can only be lost due to channel errors. This model is suitable for IoT systems based on Ultra-Narrowband (UNB) transmissions, such as SigFox [47]`；`Destructive collisions. The other extreme is adoption of the classical ALOHA model, in which any collision is destructive and all packets involved in the collision are lost. Strictly speaking, here the resulting process is not Poisson due to the correlation created when multiple packets are lost in a collision create.`
- L77（重传策略，逐字）：`the failed sources will not try again, but just wait until the next status update is generated, and $p _ { c }$ is the probability of incorrect packet decoding due to either channel error or collision.`
- L317（验证方法，逐字）：`In order to verify the correctness of the theoretical results, we simulated the two scenarios in Fig. 6 using a Monte Carlo approach.`
- L326/L328（两个拓扑，逐字）：`The line network represents a scenario in which ground nodes placed in a remote area report to a ground station through a chain of K satellites.`；`The dumbbell topology represents a scenario in which multiple connections share a single ISL, and then have different destinations. In this case, the shared ISL represents the shared bottleneck.`

### 2) 可引用的事实与数字（逐字+行号）

| # | 事实（逐字） | 行号 |
|---|---|---|
| 1 | **负载定义式（逐字 LaTeX）**：`\rho = \frac { \lambda + \sum _ { j = 1 } ^ { K } \theta _ { j } } { \mu _ { \mathrm { { D L } } } }.` | L339 |
| 2 | 负载分配假设（逐字）：`In our simulation, we assume $\theta _ { 1 } = 0$, and that $\lambda = \theta _ { j } = \rho \mu _ { \mathrm { D L } } / K , \forall j \in \{ 2 , \dots , K \}$. We do not consider the error in our computation of $\rho ,$ in order to provide a meaningful comparison between the error-free and error-prone cases.` | L342 |
| 3 | **AoI 的 U 型曲线（逐字）**：`Unlike the system delay, the AoI follows a U-shaped curve, as Fig. 7a shows. If the traffic load is very low, the average AoI is very high, as the dominant factor is the time between successive packets from the same source. For instance, when $\rho = 0 . 0 5$ and $K = 1 0 .$, the arrival rate $\lam...`（行尾被 MD 截断） | L344 |
| 4 | **错误对 AoI 的双向影响（逐字）**：`errors increase the AoI when $\rho$ is low, as the loss of one of the already rare packets can cause a significant increase. However, errors can actually have a beneficial impact on the average AoI in high traffic load scenarios: since packets are frequent`（行尾被 MD 截断） | L346 |
| 5 | 调度策略对比（逐字）：`The difference between OPF and FCFS in terms of average AoI for all sources is negligible, while HAF manages to slightly reduce the AoI if the traffic load is high.` | L361 |
| 6 | 公平性（逐字）：`while FCFS nodes do not consider the delay that packets have accumulated on previous links, OPF bases its decisions on packet timestamps, reducing the AoI distance between the ground sources close to the destination and the ones at the beginning of the chain.` | L366 |
| 7 | ALOHA 与泊松到达的对比（逐字）：`Fig. 12 compares the average AoI with ideal Poisson arrivals and the one that results from a realistic ALOHA uplink: if the rate at the first ISL is the same, the ALOHA uplink gets a slightly lower AoI than Poisson arrivals, except for very high values of the load. This might be due to the second-order statistics of the arrival distribution, but it warrants more future analysis.` | L379 |
| 8 | 多源最优负载偏移（逐字）：`Interestingly, networks with a larger number of sources have their minimum AoI with a higher load, as the effect of interarrival times is stronger when the same traffic $\rho$ is generated by multiple sources: if we set $\rho = 0 . 7 , \lambda = 0 . 2 8$ when $N = 2 .$, but $\lambda = 0 . 0 9 3$ for $N = 6 .$.` | L390 |
| 9 | 拓扑参数（逐字）：`In the dumbbell topology scenario, we consider $K = 4$, with cross traffic on the second ISL, i.e., $\theta _ { 2 } > 0$ and $\psi _ { 2 } = 1$. We consider a number of sources N, each with packet generation rate \lambda, so that the total error-free load on the bottleneck is $\rho = N \lambda$` | L383 |
| 10 | 误差设定（逐字）：`We set $\varepsilon _ { j } = 0 . 0 1 \forall j$, as in the line network.` | L385 |
| 11 | 平均 AoI 表达式（逐字 LaTeX）：`\bar { \Delta } = \lambda \mathbb { E } \left[ Q _ { i } \right] = \lambda \left( \mathbb { E } \left[ T _ { i } Y _ { i } \right] + \mathbb { E } \left[ \frac { 1 } { 2 } Y _ { i } ^ { 2 } \right] \right) ^ { \prime } .` | L113 |
| 12 | 边界松紧（逐字）：`Fig. 11 shows the empirical CDFs and the theoretical bounds for $K = 2$ and different values of $\rho$. In this case, the bound is almost always loose, except for $\rho = 0 . 8 .$` | L374 |

### 3) 对"负载变化/突发/时延/到达率"的事实贡献

**本篇是本批对"到达率与负载"最直接、可复算的一篇（解析 + Monte Carlo）**：

- **到达过程被显式建模为泊松**：源到达率 lambda、每节点交叉流量到达率 theta_k（L58），服务为 M/M/1 串联（L60），上行接入为 ALOHA（L68/L73/L75）。
- **负载的定义完全可抄**：rho = (lambda + Sigma theta_j)/mu_DL（L339）；瓶颈在最后一跳下行。
- **关键现象一：AoI 关于负载是 U 型**（L344）→ "负载越高 AoI 越低"只在低负载区成立，存在最优工作点；这直接反驳"越空闲越新鲜"的直觉。
- **关键现象二：丢包（错误）在高负载下反而降低平均 AoI**（L346）→ 失败不总是坏事，与"降低 AoI 需丢旧包"的经典结论一致；这条事实对我们设计"丢弃/惩罚"机制有直接价值。
- **关键现象三：多源时最优负载更高**（L390，N=2 时 lambda=0.28 vs N=6 时 lambda=0.093 @ rho=0.7）→ 到达率的来源数目改变最优工作点。
- **关键现象四：ALOHA 上行与理想泊松到达的 AoI 差异很小**（L379）→ 支持"用泊松近似 ALOHA 上行"的建模选择（作者亦提示需进一步分析）。
- **突发**：**未见**突发长度/突发性度量。核验命令与计数：`grep -ciE "burst"`（该篇全文）→ 见文末 B8 负向声明统一核验表。

### 4) 能否作为定标或现象证据

- **解析建模 + Monte Carlo 仿真**（**非 LEO 实测**）；但模型的**拓扑与队列结构直接对应 LEO 多跳中继**（L21、L326、L328）。
- **可作定标/建模输入**：M/M/1 串联队列模型（L60）、rho 的定义（L339）、误差率 1%（L385）、AoI 与负载的 U 型关系（L344）、丢包在高负载下的有益效应（L346）。
- **可作现象证据（理论级）**：U 型 AoI–负载曲线、丢包的双向效应、多源最优负载偏移。
- **不能作**：任何 LEO 实测数值的定标（无实测）。

### 5) 边界与不可外推项

1. **无实测**：全部为解析界 + Monte Carlo（L317）；**无真实卫星网络数据**。
2. **服务时间独立性假设（作者自述）**：L60 `in this work, we model the service time for each link for the same packet as independent for tractability. This assumption is equivalent to considering uncorrelated distances between pairs of s...`
3. **纯 ALOHA、无退避**：L68（`Rather than the conventional ALOHA implementation with a backoff mechanism to re-send colliding packets, a pure A...`）→ **不适用于有重传/退避的现代 MAC**。
4. **失败即放弃**：L77 `the failed sources will not try again` → 与有 ARQ 的系统行为不同。
5. **拓扑为两类极端情形**：L330 `These two scenarios represent two extreme situations: in the former, cross traffic accumulates all the way to the final link, while in the other, it is concentrated in a single ISL, while all other links are less loaded.`
6. **AoI 界的松紧受负载影响**：L374（仅在 rho=0.8 时界较紧，其余"almost always loose"）→ **引用上界时须标注负载区间**。
7. **未读部分**：§IV 推导细节（L195–L314）为选择性阅读；参考文献 L406–L507。

---

## 14. BLFJ6CLV — Analysis of Age of Information in Non-terrestrial Networks

**书目（逐字）**：L1 `# Analysis of Age of Information in Non-terrestrial Networks`；L3 `Yanwu Lu, Howard H. Yang, Nikolaos Pappas, Giovanni Geraci, Chuan Ma, and Tony Q. S. Quek`；L5–L13 作者单位（ZJU-UIUC Institute 浙江大学 / Linkoping University / Telefonica Research 与 Universitat Pompeu Fabra / Zhejiang Lab / Singapore University of Technology and Design）。
**已读范围**：L1–L200（题录、摘要 L15、引言 L17–L34、系统模型 L36–L61、AoI 分析 L70–L162）。**L163–L331（其余定理推导、数值结果、结论）未逐段读**；参考文献未读。

### 1) 测量/建模对象与条件（逐字+行号）

- L15（对象，逐字）：`In this paper, we focus on analyzing the timeliness of information delivery in NTN through the concept of Age of Information (AoI). We propose an on-off process to approximate the serv...`（摘要行尾被 MD 截断）
- L40（**星座随机模型，逐字**）：`We consider an NTN consisting of a constellation of LEO satellites deployed at the same altitude $h.$ We assume the positions of the satellites to follow a homogeneous Poisson point process (PPP) [21], [24], [25] of intensity \lambda on a sphere of radius $R _ { \oplus } + h ,$ where $R _ { \oplus } = 6 3 7 1$ km denotes the Earth radius.`
- L42（**到达过程，逐字**）：`we consider the interval between the generation of two consecutive status updates to be independently and identically distributed (i.i.d.), following an exponential distribution with rate $\mu .$. We further assume the source no...`（行尾被截断）
- L44（覆盖与连接，逐字）：`We deem a source node to be covered by a satellite when its signal-to-noise ratio (SNR) surpasses a minimum decoding threshold \theta.`
- L98（**on-off 近似，逐字**）：`The duration for which a satellite remains within the dome region can be approximated as an on-service period, while the time between a satellite's departure from the dome region and the arrival of the subsequent satellite can be viewed as an off-service period. Due to the random positions of the satellites, the durations of both the on- and off-service periods vary. However, we can approximate these periods as ind`（行尾被截断）
- L100（**定理 1 标题，逐字**）：`Theorem 1: The off-service periods follow an identical exponential distribution with density given by`

### 2) 可引用的事实与数字（逐字+行号）

| # | 事实（逐字） | 行号 |
|---|---|---|
| 1 | **地球半径口径（逐字）**：`$R _ { \oplus } = 6 3 7 1$ km` | L40 |
| 2 | **离服务期速率（逐字 LaTeX）**：`\lambda _ { \mathrm { o s } } = 2 \omega \lambda \sin ( \varphi _ { \mathrm { e } } ) \left( R _ { \oplus } + h \right) ^ { 2 }` | L103 |
| 3 | **在服务期 PDF（逐字 LaTeX）**：`f _ { W } ( s ) = \left\{ \begin{array} { l l } { \frac { \omega \cos ( \varphi _ { \mathrm { e } } ) \tan ( \frac { \omega s } { 2 } ) } { 2 \varphi _ { \mathrm { e } } \sqrt { \sin ^ { 2 } ( \varphi _ { \mathrm { e } } ) - \sin ^ { 2 } ( \frac { \omega s } { 2 } ) } } , } & { i f s \in \left[ 0 , \frac { 2 \varphi _ { \mathrm { e } } } { \omega } \right] , } \\ { 0 , } & { o t h e r w i s e . } \end{array} \right.` | L109 |
| 4 | **平均 AoI 闭式（逐字 LaTeX）**：`\bar { \Delta } = \frac { \mathbb { E } \left[ Y _ { k } ^ { 2 } \right] + 2 \mathbb { E } \left[ T _ { k } Y _ { k } \right] } { 2 \mathbb { E } \left[ Y _ { k } \right] } = \frac { \mathbb { E } \left[ Y _ { k } ^ { 2 } \right] } { 2 \mathbb { E } \left[ Y _ { k } \right] } + D .` | L133 |
| 5 | **SNR 与最大传输距离（逐字 LaTeX）**：`\mathrm { S N R } ( t ) = \frac { P _ { \mathrm { t x } } r ( t ) ^ { - \alpha } } { \sigma ^ { 2 } }`；`r _ { \mathrm { m a x } } = \frac { ( R _ { \oplus } + h ) \cos ( \varphi _ { \mathrm { e } } ) - R _ { \oplus } } { \cos ( \varphi _ { \mathrm { s } } ) }` | L79 / L85 |
| 6 | **几何参数（逐字 LaTeX）**：`\varphi _ { \mathrm { e } } = \cot ^ { - 1 } \left( \frac { \cot ( \varphi _ { \mathrm { s } } ) + \rho \sqrt { \cot ^ { 2 } ( \varphi _ { \mathrm { s } } ) + 1 - \rho ^ { 2 } } } { 1 - \rho ^ { 2 } } \right)`；`\rho = R _ { \oplus } / \left( R _ { \oplus } + h \right)` | L91 / L94 |
| 7 | **有效到达面元（逐字 LaTeX）**：`A _ { \epsilon } = 2 \left( R _ { \oplus } + h \right) ^ { 2 } \omega \epsilon \sin ( \varphi _ { \mathrm { e } } )` | L115 |
| 8 | **条件概率（逐字 LaTeX）**：`\mathrm { P } _ { \mathrm { f | f } } = { \frac { 1 - a } { 1 - a b } }`；`\mathrm { P _ { o | o } = \frac { 1 - \left( 2 - \mathrm { P _ { f | f } } \right) \mathrm { P _ { o f f } } } { 1 - \mathrm { P _ { o f f } } } }` | L141 / L147 |
| 9 | 服务期时长（逐字 LaTeX）：`W = \frac { 2 } { \omega } \arcsin \left( \frac { \sqrt { \sin ^ { 2 } ( \varphi _ { \mathrm { e } } ) - \sin ^ { 2 } ( \Theta ) } } { \cos ( \Theta ) } \right) .` | L123 |
| 10 | 贡献声明（逐字）：`Through stochastic geometry tools, we derive a closedform expression for the time-average AoI in an NTN. This result also extends the AoI analysis under onoff processes [23] into scenarios where one component follows an exponential distribution while the other has its probability density function supported on a bounded interval.` | L29 |
| 11 | 数值结果覆盖范围（逐字）：`We provide numerical results that validate the accuracy of our analysis and quantify the impact of both the source status update rate and the satellite constellation density on the time-average AoI.` | L34 |

### 3) 对"负载变化/突发/时延/到达率"的事实贡献

**本篇提供的是"到达率 x 星座密度 → AoI"的解析关系**，是本批**到达率维度最关键的一篇**：

- **到达过程 = 指数分布（率 mu）**（L42）——generate-at-will 模型，说明更新产生率是**可控变量**（与 GV9PPNZT L11 的同一思想呼应）。
- **星座密度 = 球面 PPP（强度 lambda）**（L40）→ **服务可用性是随机几何的结果**：离服务期近似指数（L100–L103），在服务期 PDF 有界支撑（L109）。
- **AoI 闭式 = 到达间隔二阶矩项 + 传播时延 D**（L133）→ **明确给出"到达率二阶矩（方差）决定 AoI"的解析结构**；这对论证"奖励里需要方差项"是**理论支撑**。
- **主要结论方向（来自贡献声明）**：量化**源更新率**与**星座密度**对平均 AoI 的影响（L34）。
- **突发**：**未见** burstiness 度量（核验见文末统一表）。

### 4) 能否作为定标或现象证据

- **解析模型（随机几何 + on-off 服务过程）**，**非 LEO 实测、非包级仿真**；数值部分为解析式求值。
- **可作理论定标**：AoI 闭式（L133）、离服务期速率表达式（L103）、在服务期分布（L109）、几何关系（L85/L91/L115）。
- **可作现象证据（理论级）**：**到达率的二阶矩（而非均值）进入 AoI**（L133）——"仅优化平均负载不够、需建模波动"的**解析证据**。
- **不能作**：任何小区/链路级负载数值的定标（无实测、无流量数据）。

### 5) 边界与不可外推项

1. **卫星位置为 PPP 假设**（L40）→ 与**真实 Walker 星座的确定性结构不符**（对比 4QG5VYHQ 的多跳链式建模）；对真实 Starlink 的适用性未验证。
2. **单跳连接假设**：L44（源最多连一颗卫星）→ **不覆盖 ISL 多跳**；这正是 4QG5VYHQ 处理的情形，两篇互补但不可互相替代。
3. **无排队/无拥塞**：服务过程是 on-off 可用性，**不含缓冲区与排队时延**（L98）→ 不能用于负载-时延耦合。
4. **传播时延被视为常数 D**（L130 `If the k-th packet transmission is successful, $T _ { k } = t _ { k } ^ { \prime } - t _ { k } = D$ denotes the propagation delay`）→ **不建模时延波动**。
5. **未读部分（本篇最大证据缺口）**：**L163–L331 未逐段读**，包括全部数值结果与结论；本档仅覆盖到 §III-B 的公式与 Theorem 1、Lemma 1。**若需引用其数值结论，必须先补读 L163–L331**。
6. **未读部分**：参考文献（本篇 MD 正文至 L331 结束，无独立 References 标题行被检出）。

---

## 15. GV9PPNZT — Information Freshness in Multi-Hop Wireless Networks

**书目（逐字）**：L1 `# Information Freshness in Multi-Hop Wireless Networks`；L3 `Vishrant Tripathi, Rajat Talak, and Eytan Modiano`。
**已读范围**：L1–L46（摘要/引言/贡献）+ L48–L92（系统模型）+ L513–L563（数值结果与结论）。**L96–L512（三类策略的推导与证明）与 L645–L842（附录证明）未逐段读**；参考文献 L569–L644 未读。

### 1) 测量/建模对象与条件（逐字+行号）

- L5（对象，逐字）：`We consider the problem of minimizing age of information in multihop wireless networks and propose three classes of policies to solve the problem - stationary randomized, age difference, and age debt.`
- L50（**时隙模型，逐字**）：`Consider a network with N nodes connected by a fixed undirected graph G(V, E). An edge (i, j) means that nodes i and j can send packets to one another directly. We assume that at most one update can be sent over an edge in any given time-slot and takes exactly one time-slot to get delivered. We normalize the time-slot duration to unity.`
- L52（流模型，逐字）：`The network consists of $K \left( \leq N \right)$ source nodes that generate information updates. All the sources are active, i.e. they generate fresh updates on demand.`
- L56（链路与干扰，逐字；原文中的集合符号为 $ 花括号 A 花括号，为避免模板转义此处写作 $ { A }）：`We consider unreliable links as well as general interference constraints, i.e., transmission on all the links cannot happen simultaneously. We enumerate the set of all possible interference free choices of links and corresponding flow transmissions in the set $ { A }.`
- L58（链路状态，逐字）：`we use $U _ { i j } ^ { k } ( \mathfrak { t } )$ and $S _ { i j } ( \mathrm { t } )$ (both $\in \{ 0 , 1 \} )$ to denote the transmission decision and link state of the link $( i , j )$ at time $t .`
- L88（控制假设，逐字）：`A control policy needs to specify not only which links should be scheduled in each time-slot but also which flows should be transmitted along each link. We assume a centralized controller.`
- L515/L519/L536/L548（数值设置）：`we consider the weighted-sum AoI problem in singlehop broadcast networks with unreliable channels. There are N nodes in the network and the weight of the ith node $w _ { i }$ is set to i/N. Link connection probabilities are chosen uniformly from the set [0.6, 1].`；`There are N nodes in the network and the cost of AoI for each node is chosen from the set of functions $\{ 1 5 A ( t ) , e ^ { A ( t ) } , ( A ( t ) ) ^ { 2 } \mathrm { ~ a n d ~ } ( A ( t ) ) ^ { 3 } \}$`；`Consider N nodes arranged in a line network from 1 to N. Node 1 wants to sent packets to node N, however not all nodes can transmit simultaneously. We consider a simple interference constraint - in any given time-slot either all even numbered nodes or all odd numbered nodes can forward packets.`；`We consider all possible connected network topologies with 5 or 6 nodes (a total of 133 graphs).`

### 2) 可引用的事实与数字（逐字+行号）

| # | 事实（逐字） | 行号 |
|---|---|---|
| 1 | **年龄演化式（逐字 LaTeX）**：`A _ { j } ^ { k } ( t + 1 ) = \left\{ \begin{array} { l l } { \operatorname* { m i n } ( A _ { j } ^ { k } ( t ) , A _ { i } ^ { k } ( t ) ) + 1 } & { \mathrm { i f ~ } U _ { i j } ^ { k } ( t ) S _ { i j } ( t ) = 1 } \\ { A _ { j } ^ { k } ( t ) + 1 , } & { \mathrm { i f ~ } U _ { i j } ^ { k } ( t ) S _ { i j } ( t ) = 0 } \end{array} \right. }` | L63 |
| 2 | **加权和 AoI 目标（逐字 LaTeX）**：`A _ { \mathrm { a v e } } = \operatorname* { l i m } _ { T \to \infty } \mathbb { E } [ \frac { 1 } { T } \sum _ { t = 1 } ^ { T } \sum _ { k = 1 } ^ { K } \sum _ { j \in D _ { k } } w _ { j } ^ { k } A _ { j } ^ { k } ( t ) ]` | L71 |
| 3 | **非线性年龄代价（逐字 LaTeX）**：`B _ { j } ^ { k } ( t ) \triangleq g _ { j } ^ { k } ( A _ { j } ^ { k } ( t ) )`；`B _ { \mathrm { a v e } } = \operatorname* { l i m } _ { T \to \infty } \mathbb { E } [ \frac { 1 } { T } \sum _ { t = 1 } ^ { T } \sum _ { k = 1 } ^ { K } \sum _ { j \in D _ { k } } B _ { j } ^ { k } ( t ) ]` | L77 / L83 |
| 4 | **三类策略的排序结果（逐字）**：`the optimal stationary randomized policy performs much worse than the other classes of policies. Age difference performs better than the randomized policy but not as well as the Whittle-index or max-weight policies.` | L517 |
| 5 | **年龄债策略近最优（逐字）**：`when the age debt policy is provided the max-weight average cost as the target vector, it replicates near optimal performance.` | L517 |
| 6 | **收敛/稳定性（逐字）**：`We observe that the age debt policy indeed stabilizes the debt queues since queue lengths don't grow with time. As a corollary, it also achieves age cost optimality in this setting. On the other hand, the Whittle index policy from [29] achieves a total sum cost of 88.34, a fixed but small distance away from the optimal cost` | L534 |
| 7 | **复杂度（逐字）**：`Note that the complexity of implementing the flow-control scheme is polynomial in the network size per time-slot. This suggests that age-debt and its variants are a good candidate for low complexity near optimal age scheduling in general networks.` | L557 |
| 8 | **参数可配置性（逐字）**：`the gradient descent variant has parameters that are hard to configure for networks of different sizes and takes a long time to converge. The flowcontrol method has just two parameters V and $\alpha _ { \mathrm { m a x } }$ that are relatively easy to configure` | L559 |
| 9 | **Broadcast 对照结果（逐字）**：`age-debt achieves the same performance as the MCDS scheme when provided its average cost as the target vector. Further, age-debt with flow control achieves performance that is very close to that of the MCDS scheme without requiring knowledge of \alpha.` | L550 |
| 10 | **三种流类型（逐字）**：`(1) unicast: the flow has a single destination node. (2) multicast: the flow has multiple destination nodes, which are a strict subset of the remaining nodes. (3) broadcast: every node other than the source itself is a destination node.` | L54 |
| 11 | **干扰模型（逐字）**：`in any given time-slot either all even numbered nodes or all odd numbered nodes can forward packets`；`Now, all nodes interfere with one another, and only one node can transmit successfully in any given time-slot.` | L536 / L538 |

### 3) 对"负载变化/突发/时延/到达率"的事实贡献

- **本篇不测负载，但把"年龄"变成一个可调度的网络资源**：L28 `we develop a unifying framework for making routing and scheduling decisions that minimize AoI cost in general multihop networks`；L34 `we consider the multihop problem in full generality - 1) with non-linear AoI cost functions; 2) unicast, multicast and broadcast flows and 3) considering both scheduling and routing decisions for optimization. We provide a recipe to transform AoI optimization problems into network stability problems.`
- **对本选题最直接的价值（信用分配/虚拟队列）**：L36 `we introduce the notion of Age Debt and set up a virtual queuing network that is stable if and only if there exists a feasible network control policy that can achieve the specified target costs. We use Lyapunov drift based methods to stabilize this system of virtual queues` → **"把目标代价转成虚拟队列，再用漂移法驱动调度/路由"**是一套成熟且可移植到 LEO RL 路由的**代价塑形骨架**。
- **到达率**：本篇的更新是"源节点按需产生"（L52 `they generate fresh updates on demand`），即 generate-at-will，**无到达过程统计**；L11 亦逐字说明 `the generation of update packets, such as sensor data, can be controlled. It has been shown [1] that generating update packets at the right rate can improve freshness`。
- **突发**：**未见**（核验见文末统一表）。

### 4) 能否作为定标或现象证据

- **理论/算法论文（多跳无线网，非 LEO）**：数值结果仅为策略对比（L515–L559），**与卫星无关**。
- **可作定标**：**否**（不含任何 LEO 或网络实测数值）。
- **可作机制证据（迁移价值高）**：三类策略（stationary randomized / age difference / age debt）的**性能排序与复杂度**（L517、L557、L559）；**年龄债 + Lyapunov 漂移**的构造（L36）；**支持 unicast/multicast/broadcast 与非线性代价**（L34）。
- **不可作**：LEO 相关任何现象或定标证据（**非 LEO 场景**）。

### 5) 边界与不可外推项

1. **非 LEO**：网络模型是通用无线多跳图（L50），**无卫星、无轨道、无 ISL/GSL**；迁移到 LEO 需自行补上时变拓扑。
2. **时隙同步、单包/时隙**：L50（每时隙每边至多一个更新、恰好一个时隙送达）→ 与真实 LEO 的连续时延/可变速率不符。
3. **集中式控制器**：L88 `We assume a centralized controller.` → 与 LEO 分布式星上路由的前提相反；**迁移时需重新论证分布式的可行性**。
4. **源假设**：L52 `All the sources are active, i.e. they generate fresh updates on demand.`（generate-at-will）→ **不含外部泊松到达**，与 4QG5VYHQ 互补。
5. **数值规模很小**：5–6 节点、133 个图（L548）→ **不能外推到星座规模**。
6. **未读部分**：L96–L512（策略推导与证明主体）、L645–L842（附录证明）、参考文献 L569–L644 —— 本篇按"机制迁移"强度阅读，**未全文精读**。

---

<!-- GA-SECTION-START -->
## 附录 GA：对抗性问题（缺口主张 G-A）的全库检索与反例判定

**主控问题原文**：全库是否有任何工作，把**同一个失败事件**（丢包/超时/溢出）按**物理原因**拆成**不同的学习通道或惩罚项**（例如区分"决策缓存溢出"与"链路队列溢出"）？

### GA-1 检索模式与实测计数

检索范围：`/data/liguang13/topic-loop-r2/md/**/txt/*.md`，共 **111** 个 MD 文件（`ls -d ... | wc -l` = 111）。全部使用 `grep -raniE "<pattern>" --include=*.md .`（`-a` 强制文本，避免 Sutton&Barto 书被 grep 判为 binary 而漏计）。

| 模式（原文照抄） | 命中行数 | 命中文件数 |
|---|---|---|
| `credit assignment` | 17 | 5 |
| `counterfactual` | 8 | 2 |
| `reward decompos` | **0** | 0 |
| `multi-objective` | 27 | 10 |
| `MORL` | 9 | **1** |
| `separate (reward\|penalty)` | **1** | 1 |
| `drop (reason\|cause)` | 2 | 1 |
| `overflow` | 12 | 10 |
| 补充：`reward vector\|vector reward\|weighted sum of (the )?reward\|multiple rewards\|distinct reward\|reward component\|per-cause\|failure cause\|cause of (the )?(packet )?(loss\|drop)\|loss reason\|drop cause` | 14 | 7 |

### GA-2 反例排查（逐条排除）

**排除项（不构成反例，含理由）**：
1. `credit assignment` 的 17 行：分布于 6C843JTS（TD 学习原文）、LJG6ZW7B（Sutton&Barto 教材及索引）、QGAREQUM、JSX5XG88（GAE）——全部是**通用 RL 的时序信用分配**，与"失败原因分解"无关。
2. `counterfactual` 的 8 行：9FLZ88LZ、FGQSH4AI、I2WH9RRR、KPUZIMU5、LJG6ZW7B —— 全部指向 **COMA（counterfactual multi-agent policy gradients）** 的作者名/参考文献，是**多智能体信用分配**，不是失败原因分解。
3. `multi-objective` 的 27 行：大部分落在参考文献条目或综述性语句（2QRYMWBI、LNA28YZY、Z74SR656、JS857IYN、QSNRQ8PF、3MRQRWHU、L5F3DK68、YI9G7NR7）。
4. `separate (reward|penalty)` 唯一命中：LJG6ZW7B L6887 —— 神经科学脚注（Graybiel / dopamine），无关。
5. `drop (reason|cause)` 两处命中：9KZDXPKC L246（`GSL Handover`）、L248（`ISL Failure`）——"丢包原因"是**实验场景对照**，不是学习通道。
6. `overflow` 的 12 行：42E4NAQU（Dijkstra 基线描述）、9C6HB6AF（引用他人 AMBRLB）、GPDPLJNG（流守恒/buffer 规则）、J68GU76W（TLE 数据获取）、JP79GMZS（NS 仿真）、R37BNQQ8（`l(t)` 权重公式）、TQF59BD7（buffer 大小）、YI9G7NR7（遥感下行）、X2FCSU4S、LJG6ZW7B —— **无一处把 overflow 作为独立的惩罚通道**。

**命中但需判定的三项（本批的"部分反例"）**：

#### (1) 8N9QJHC2 — 最接近 G-A 的反例：按**故障物理原因**分流 Q 更新（T1 批次论文，非本批）

- L29 逐字：`based on the Bayesian decision theory, when the known conditions are limited, the posterior probability index representing the posterior probability of diferent types of faults on each link is obtained through a priori probability ofdiferent fault types. Furthermore, the purpose of distinguishing the types oflink failures is achieved.`
- L99 逐字（**这就是"物理原因"轴**）：`\$e two types of failures are temporary link failures caused by transmission medium interference and permanent link failures caused by problems with node port hardware equipment.`
- L31 逐字（**分离进入了学习过程**）：`based on the Q-learning algorithm in reinforcement learning, we propose a route recovery technology based on the above-mentioned fault detection. \$e collected information is used to update the Q-value table composed of two-dimensional state space and one-dimensional action space. For diferent types of faults, update the Q-value of the local state space and action space of diferent related nodes to achieve the purpose of distinguishing route recovery for diferent types of faults.`
- L176 逐字：`Corresponding to the two stages of fault detection, this technique uses diferent route update methods to recover the routes of nodes related to diferent types of faulty links.`
- L31 逐字（**关键限制：奖励仍只有一条**）：`because the reward function consists of queuing time, transmission time, and link lifetime, the discount factor is also related to the link lifetime`
- 分解轴判定：**失败原因（传输介质干扰 vs 端口硬件故障）**——正是 G-A 要的轴。
- 是否覆盖 G-A：**部分覆盖，不构成完整反例**。理由（基于以上逐字原文）：(a) 分离发生在 `update the Q-value of the local state space and action space of diferent related nodes`（**更新哪些节点的 Q 表**），不是"同一个失败事件进入不同惩罚项/不同价值头"；(b) 奖励函数**唯一**，由 `queuing time, transmission time, and link lifetime` 组成，**没有按原因区分的惩罚项**；(c) Q 学习为单标量（L204 `Q _ { i } ^ { l } ( d _ { k } , y _ { z } ) = Q _ { i } ^ { l + 1 } ( d _ { k } , y _ { z } )` 收敛式；L216 `Q _ { i } \left( d _ { k } , y _ { z } \right) \leq 0`）。→ **"同一失败事件 → 按物理原因分通道惩罚"这一核心仍未被覆盖**。

#### (2) UKBSA7WN（QRLSN）— 结构最像"分通道"，但分解轴是**优化目标**而非失败原因

- L139 逐字：`In QRLSN, we adopt a Multi-Objective Reinforcement Learning (MORL) algorithm to balance endto-end delay and network traffic overhead load.`
- L141 逐字：`MORL differs from typical RL, which considers several optimization objectives simultaneously in the learning process, where a reward vector is provided for the agent at each update step`
- L143–L145（**逐字 LaTeX 更新式**）：
  ```
  Q _ { i } ( s , a ) \gets ( 1 - \alpha ) Q _ { i } ( s , a ) + \alpha \biggl [ r _ { i } + \gamma \operatorname* { max } _ { a ^ { \prime } \in A } Q _ { i } ( s ^ { \prime } , a ^ { \prime } ) \biggr ]\tag{ð(6)Þ}
  ```
- L154–L156（**逐字 LaTeX 合成式**）：
  ```
  \mathrm { T Q } ( s , a ) = \sum _ { i = 1 } ^ { n } w _ { i } Q _ { i } ( s , a )\tag{ð(7)Þ}
  ```
- L158 逐字：`In the proposed QRLSN, two optimization targets are obtained by a reward vector $f _ { r } = [ f _ { r _ { 1 } } , f _ { r _ { 2 } } ]$`
- L160–L167（**逐字 LaTeX 奖励分量**）：
  ```
  f _ { r _ { 1 } } = \left\{ \begin{array} { c c } { { r _ { \mathrm { m a x } } } } & { { N _ { t + 1 } \mathrm { i s \ d e s t i n a t i o n } } } \\ { { r _ { \mathrm { m i n } } + \left( \frac { e } { 2 } \right) ^ { - d _ { i j } } } } & { { \mathrm { O t h e r w i s e } } } \end{array} \right.\tag{ð(8)Þ}
  ```
  ```
  f _ { r _ { 2 } } = \left\{ \begin{array} { c c } { { r _ { \mathrm { m a x } } } } & { { N _ { t + 1 } \mathrm { i s \ d e s t i n a t i o n } } } \\ { { r _ { \mathrm { m i n } } + \left( \frac { e } { 2 } \right) ^ { - n _ { q } } } } & { { \mathrm { O t h e r w i s e } } } \end{array} \right.\tag{ð(9)Þ}
  ```
- L168 逐字（**轴的判据**）：`where $f _ { r _ { 1 } }$ and $f _ { r _ { 2 } }$ denote the reward function to optimize the end-to-end delay and network traffic overhead load respectively; $d _ { i j }$ is the transmission time between adjacent satellite nodes; $n _ { q }$ is the number of data packet queued in the current node.`
- 分解轴判定：**优化目标类型（端到端时延 vs 网络流量开销负载）**；奖励中的 `n_q`（当前节点排队包数）是**负载目标的度量**，不是"溢出原因"。
- 是否覆盖 G-A：**不覆盖，但提供最强的结构模板**。它是全库唯一被确认存在的"奖励向量 + 每目标一个 Q_i + 加权合成"实现（L141/L147/L158），可直接复用其结构做"分原因惩罚通道"——但**需要把 i 的语义从"优化目标"改成"失败物理原因"**，该文自身没有这样做。

#### (3) GPLEP83L — 惩罚按**事件类型**分开（专家基线）

- L110 逐字：`The baseline reward follows a relatively compact design, mainly combining a distance-based term, a queue-based term, and fixed penalties or bonuses for special events such as delivery, unavailable links, and loop formation.`
- 分解轴判定：**事件类型（投递 / 链路不可用 / 成环）**，其中队列项与不可用链路项确实分开。
- 是否覆盖 G-A：**不覆盖**。该分解不区分"同一丢包事件究竟由缓存溢出还是链路队列溢出导致"；`unavailable links` 是拓扑性不可达，`queue-based term` 是时延度量，二者**不构成对同一失败事件的因果拆分**。

#### (4) 旁证：非学习类工作确实做了"失败原因"分类，但不进入学习
- X2FCSU4S L15 逐字：`the queue length becomes larger and a cache overflow appears. In this paper, the abundant storage resources of the multilayered satellite network (MLSN) are used to avoid the packet loss caused by a cache overflow of the Low Earth Orbit (LEO) satellites.` → **"缓存溢出"被明确识别为丢包原因**，但手段是 Stackelberg 博弈 + 缓存定价（非学习通道）。
- 9KZDXPKC L246/L248：`GSL Handover` 与 `ISL Failure` 作为两种造成吞吐下降的场景**分别实验**，但不进入任何学习目标。

### GA-3 结论（对 G-A 的判定）

在全库 111 篇中，**未发现任何工作把同一个失败事件按物理原因拆成不同的学习通道或惩罚项**：
- `reward decompos` **0 命中**；`separate (reward|penalty)` **1 命中且无关**；`drop (reason|cause)` **2 命中且仅为实验场景**。
- 最接近的是 **8N9QJHC2**（把链路故障按"介质干扰/端口硬件"分类并把结果分流到不同节点的 Q 更新），但它的**奖励函数唯一**、**Q 为单标量**，分离只体现在"更新哪些节点"。
- 唯一具备"多通道 Q"结构的是 **UKBSA7WN**（MORL 奖励向量 + 每目标 Q_i + 加权合成 TQ），但其通道轴是**优化目标**（时延/负载），不是失败原因。
- → **G-A 的缺口成立**：把"决策缓存溢出"与"链路队列溢出"这类**同构失败事件的不同物理原因**分别接入独立价值头/独立惩罚项，在全库范围内**未见先例**；UKBSA7WN 的多通道骨架可作为实现该缺口的现成载体。

<!-- GA-SECTION-END -->
<!-- SENTINEL-END -->
