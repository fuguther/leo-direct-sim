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

**（c）突发/到达率**：**未见**。检索词 `arrival|offered load|load factor|burst|inter-?arrival|packet rate|traffic intensity|Erlang|congestion level`（grep -n -i -E，范围=该篇 MD 全文 L1–L572）**仅命中 L83 一处**，且该处是描述他人仿真器：`which simulate LEO Internet performance across location, satellite orbiting pattern, and congestion level`（L83）。全文无到达过程、无包级/流级到达率、无突发长度分布的测量。本篇是**纯时延可达性测量**，不产生负载过程事实。

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
- **到达率**：**未见**任何到达过程/到达率建模。补充检索词 `arrival|poisson|interarrival|per second|pps|packets/s|utilization|offered`（grep -n -i -E，范围=该篇 MD 全文 L1–L292）命中 L69、L105、L120、L189、L227，其中 L69 是**施加的**消息速率条件（`sends 25 variable length messages per second during 2 minutes`、`The average bitrate of this transfer is 3 Mbit/s`），L189 是作者对"低利用率"的评论（`the presence of (moderate) packet loss even at low network utilization`）。**全篇无测得的分组到达过程**。
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
- **到达率/负载过程**：**未见**。检索词 `arrival|offered load|load factor|burst|inter-?arrival|packet rate|traffic intensity|Erlang|congestion level`（grep -n -i -E，范围=该篇 MD 全文 L1–L463）与补充词 `time series|stochastic|Markov|queue`（同范围）后：负载一律以"测速期间施加的批量传输"或 goodput（Mbps）这一**结果量**出现，**全篇没有到达过程的建模或测量**。

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
<!-- SENTINEL-END -->
