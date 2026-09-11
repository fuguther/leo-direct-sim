
---

## 4. IP7RRM3A — From Connectivity to Advanced Internet Services: A Comprehensive Review of Small Satellites Communications and Networks

- 本地定位：TIER-ASSIGNMENT.md:105，"综述：只取共识与开放问题，不承重"
- MD 总行数：492
- 读取范围：第 1–38 行（题录/摘要/1. Introduction）、200–262 行（6. Advances in Communications and Network Protocols 全节 + 7. Perspectives and Open Challenges 全节 + 8. Conclusions）。
- **未通读（如实声明）**：39–199 行（2. 小卫星演化史、3. 服务与应用、4. 载荷演化、5. 新电信架构）。该区间仅做关键词检索（见 4.3），未逐段阅读，故其开放问题可能**有遗漏**。

### 4.1 该综述认定的开放问题清单（逐字 + 行号）

该节标题即 L220 "## 7. Perspectives and Open Challenges"，其编号子节构成问题清单：

| # | 行号 | 逐字原文 |
|---|---|---|
| O1 | 224 | "The provision of advanced Internet services through mega-constellations of pico/nanosatellites is going to become reality in the near future. However, several challenges must be faced yet, which are summarized in the following." |
| O2 | 228 | "(a) The use of frequency bands higher than Kaband and the use of free space optical (FSO) communications for Earth-satellite links (i.e., not only for intersatellite links), as reported in Section 4, raise one important challenge: the propagation channel can be strongly attenuated." |
| O3 | 228 | "Both for high frequency RF transmission and for FSO, this issue could be overcome by providing a ground network with a high number of ground stations at highly diverse sites. The concept of site diversity has been extensively studied in the field of High Throughput Satellite (HTS), and recent works have highlighted the fact that SDN paradigm could provide the gateways implementing the concept of Smart Diversity, a high level of reconfigurability that could allow eficient resources allocation during trafic switching events" |
| O4 | 230 | "(b) Besides the few theoretical studies mentioned in Section 6.1, and some transceiver implementing ACM techniques, much more work is needed to design optimized modulation and coding schemes able to satisfy strict requirements in terms of mass, weight, size, and power consumption." |
| O5 | 234 | "(ii) MAC Layer. In view of emerging system constraints, the implementation in small satellites of the scheduled and random-access MAC protocols adopted in existing satellite networks needs further investigation." |
| O6 | 238 | "(iii) Upper Layers. Definition is needed for interoperable applicationlayer protocols to be employed on top of the lower layer satellite protocols, addressing a wide range of application scenarios and trafic data configurations." |
| O7 | 242 | "(iv) Routing over Time. Due to the frequent topology changes in a CubeSat network, successful data delivery will require ample long-term storage at intermediate nodes to deal with satellite link disruptions." |
| O8 | 246 | "CubeSats are susceptible to Denial of Service (DoS) attacks as well as eavesdropping and data can be accessed by unauthorized user. The attacker could send spurious commands causing excessive resources consumption, data loss, or mission failure." |
| O9 | 246 | "Security mechanisms developed for conventional terrestrial networks, characterized by lengthy handshake exchanges and substantial computational efort, can hardly be directly applied to networks of small satellites. Power, space, and weight constraints related to CubeSat pose challenges in implementing complicated encryption schemes and computational expensive mechanisms" |
| O10 | 248 | "The challenge is still open. Interesting works are ongoing on the use of physical layer approaches to security in satellite communications [73, 74]. No specific work on application of physical layer security to CubeSat can be found; even this could open novel solutions to overcome the challenges of security in the small satellite framework." |
| O11 | 250 | "Interesting research is ongoing on the use of quantum cryptography." |
| O12 | 254 | "(vi) Adoption of the SDN/NFV. It is clear that SDN/NFV paradigms will play a key role in the integration of satellite systems with 5G. However, the use of SDN/NFV in a network of small satellites has yet to be investigated; as discussed in Section 6, it could be important." |
| O13 | 254 | "For instance, onboard SDN-compatible routers could be developed and operated on small satellites as router functions migrate into software." |
| O14 | 258 | "However, in many other 5G applications scenarios that focus on M2M communications or require extremely low latency, only small satellite constellations can really provide an efective complement to terrestrial systems. It is crucial to efectively face the challenges discussed above in order not to miss the opportunities ofered by the 5G ecosystem." |
| O15 | 218 | "Other activities looking into implementation of network coding for intersatellite links have been also considered, although the aforementioned constraints coming from the space segments were not completely taken into account, hence requiring additional study for a deeper understanding of all underlying implications and requirements." |
| O16 | 216 | "Another point relates to the actual position of NC functionalities in a protocol stack, for which no specific consensus has been reached yet." |

### 4.2 涉及"负载过程/突发/时延/到达率/信用分配/决策成本"的表述（逐字 + 行号）

| 行号 | 逐字原文 | 归类 |
|---|---|---|
| 208 | "The central fact in both circumstances is the potential inability of each network node to request timely assistance from any other, for any purpose, and at any given moment." | **节点无法及时获得外部协助** → 必须本地决策 |
| 208 | "Nodes must be able to make their own operational decisions locally, on their own, with global information that may well be stale or incomplete, and the network must be able to continue to operate at some useful level even when these decisions are flawed." | **决策在信息陈旧/不完整下进行**（决策成本与信息质量） |
| 208 | "It principally difers from IP in that a forwarding node does not immediately discard data items (called “bundles”) for which no onward communication link is currently available; instead, it may store bundles for a lengthy period of time, waiting for a link to become available." | 以存储换链路可用性（时间维度上的缓冲） |
| 212 | "In a space flight mission scenario, end-to-end retransmissions could result in extremely lengthy delays in data delivery because the source and destination of data might be on diferent planets separated by many light minutes of propagation latency." | 传播时延量化（light minutes） |
| 242 | "Due to the frequent topology changes in a CubeSat network, successful data delivery will require ample long-term storage at intermediate nodes to deal with satellite link disruptions." | 拓扑变化 → 中间节点长期存储 |
| 214 | "In particular, the application on random linear network coding of data chunks to be dumped to ground stations would help increase the reliability of data exchange against sporadic fluctuations of the transmission channel quality." | **信道的偶发波动**（sporadic fluctuations） |
| 216 | "As a matter of fact, network coding implementation requires some dedicated computation capability for online coding functions as well as specific on-board storage to keep temporary copies ofthe data chunks being subject to encoding or decoding procedures." | 在线编码的算力/存储成本 |
| 218 | "Although in this case, network coding is implemented only on specific links, the node capability to implement encoding/decoding functionalities as well as to store data prior to processing functions is certainly an important requirement to be taken into account in the system design phase in the light of the typically resources-constrained implementations of nodes in space." | 资源受限下的处理能力要求 |
| 204 | "including error correction capabilities and dynamic adaptation of modulation parameters depending on the current link conditions" | 链路状态自适应的调制参数（链路过程） |
| 234 | "In view of emerging system constraints, the implementation in small satellites of the scheduled and random-access MAC protocols adopted in existing satellite networks needs further investigation." | 调度式 vs 随机接入 MAC |
| 258 | "in many other 5G applications scenarios that focus on M2M communications or require extremely low latency" | 时延等级需求登记 |
| 228 | "efficient resources allocation during trafic switching events" | 流量切换事件中的资源分配 |

### 4.3 负向声明核验（模式 / 实测计数 / 命中判定）

- **信用分配（credit assignment）未见**：模式 `credit` → **实测计数 1**。
  - **命中位置**：L150 "Figure 7: The MARCO communication architecture. Image credit: NASA/JPL-CalTech."。
  - **为何不构成反例**：图片版权署名。补充：该文 L218 有 "node capability to implement encoding/decoding functionalities"，但那是**星上算力**，与 RL 信用分配无关。
- **到达率未见**：模式 `arrival rate` → **实测计数 0**；`arrival process` → 0；`Poisson` → 0。
- **自相似未见**：模式 `self-similar` → **实测计数 0**；`non-stationar` → 0。
- **突发有 1 命中**：模式 `burst` → **实测计数 1**。
  - **命中位置与逐字**：L400 "[65] F. Chiti, R. Fantacci, and T. Pecorella, “An optimized multicast scheme for data burst dissemination over satellite links,” IEEE Transactions on Vehicular Technology, vol. 65, no. 11, pp. 9414– 9419, 2016."。
  - **为何不构成反例**：该命中位于**参考文献条目标题**中，不是本文的论述；本文正文对突发/到达过程无任何建模或讨论。故"该文未涉及突发过程建模"的判断成立。

### 4.4 它提到但本库其他论文未跟进的方向

1. **DTN / Bundle Protocol / LTP 在小型卫星星座上的路由与拥塞控制语义**：208–212。本库 111 篇题录内无以 DTN 为主题的研究论文。
2. **网络编码（Network Coding，含随机线性网络编码）在星上/星间链路的可靠性提升**：214–218。本库无对应论文。
3. **可见光通信（VLC）作为星间链路**：204。本库无对应论文。
4. **智能分集（Smart Diversity）/站点分集与 SDN 网关重构**：228。本库无对应论文。
5. **星上 SDN 兼容路由器的实现**：254。本库无对应论文。
6. **CubeSat 的物理层安全（PLS）**：248。本库无对应论文。
7. **小卫星的量子密钥分发（QKD）**：250。本库无对应论文。
8. **应用层互操作协议（面向海量应用场景与流量数据形态）**：238。本库无对应论文。
9. **以中间节点长期存储应对链路中断的路由（storage-carry-forward）**：242。本库 T1/T2 路由论文均假设缓存有限或无限但即时转发，无 storage-carry-forward 设计。

---

## 5. QSNRQ8PF — Dynamic Routings in Satellite Networks: An Overview

- 本地定位：TIER-ASSIGNMENT.md:107，"综述：只取共识与开放问题，不承重"
- MD 总行数：707
- 读取范围：第 1–30 行（题录/摘要）、107–132 行（3.3. Key Challenges for Satellite Network Routing + 3.4. Key Technologies 全节）、251–277 行（4.2.3. Traffic Balancing Dynamic Routings 全节 + 表 10/11/12）、279–320 行（5. Potential Technologies and Future Directions 全节 + 6. Conclusions）。
- **未通读（如实声明）**：31–106 行（引言/相关工作/系统模型/网络特性）、133–250 行（4.1 单层与 4.2.1–4.2.2 SDN/QoS 路由各节）。

### 5.1 该综述认定的开放问题清单（逐字 + 行号）

| # | 行号 | 逐字原文 |
|---|---|---|
| O1 | 111 | "Therefore, to resolve the re-routing problem and improve the routing performance of satellite networks, more profound studies on link switching strategies are needed in academia and industry." |
| O2 | 111 | "For such routing strategies, the optimal routing of the network is ensured but at the expense of a certain computational overhead." |
| O3 | 113 | "However, when calculating satellite routes with the dynamic routing algorithm onboard, it is extremely challenging to fully reflect the real-time state between satellite links through network state updates alone. Furthermore, the approach is prone to making each satellite node calculate routing tables with inaccurate network state information, leading to the waste of on-star computing resources." |
| O4 | 115 | "With the limited on-star computing power, the on-star routing algorithm must have low implementation complexity (namely, low computational complexity), communication costs, and storage costs." |
| O5 | 115 | "Hence, storing all the status information of the whole network on the star is impractical. Owing to the highly dynamic topology of the satellite network, obtaining link status information from the ground network system alone cannot guarantee accurate results." |
| O6 | 115 | "In addition, owing to the unique launch mode of the satellite, updating and upgrading its functions is hardly possible." |
| O7 | 117 | "For time-varying satellite networks, none of the switches can cause the established routes not to work correctly. Re-routing mechanisms increase network latency and cannot meet QoS latency requirements, causing communication disruptions." |
| O8 | 119 | "Since there is not enough resource space for up/down link (UDL) routing between satellite users, variations in such load traffic may affect some switching strategies in the network." |
| O9 | 119 | "For one, even if the ISL has sufficient resource capacity at the time of establishment, the change in link load traffic can cause network congestion, preventing the link from switching. In addition, even under the same user load traffic conditions, each LEO satellite and ISL may have different load traffic, causing link switching to fail. The blocked link prevents QoS routing, affecting satellite network communication." |
| O10 | 131 | "Therefore, for the different types of services, accurately acquiring the status of the available resources and the flexible scheduling of the multi-dimensional resources are the core issues of dynamic network slice design." |
| O11 | 281 | "Although, there are a variety of multi-layer satellite network routing protocols and algorithms, as previously described, systematic routing algorithms are still lacking." |
| O12 | 287 | "Handling routing tables generated by different layers of satellite nodes in a satellite network is an important challenge in the satellite routing optimization problem. To alleviate the computational overhead of processing the data, ML can be considered to improve the data efficiency of the routing training process, especially for multilayer satellite networks." |
| O13 | 292 | "The satellite routing optimization problems are generally complicated to solve via traditional methods." |
| O14 | 296 | "However, the dynamic routing mechanism requires a high level of data processing due to the satellite’s motion. There is no doubt that edge computing technology with powerful data processing and analysis can solve this problem." |
| O15 | 300 | "Based on the digital twin satellite network model and simulation technology, a dynamic topology model of multi-layer satellite networks is constructed in the information space to predict and simulate dynamic routing changes." |
| O16 | 306 | "Due to the substantial heterogeneity of multi-layer satellite networks, the frequent changes in the constellation topology, and inter-satellite links, flexible control system reconfiguration is more necessary. The new research direction of routing will undoubtedly become a hotspot in future academic work." |
| O17 | 308 | "The satellite networks contain multiple types of network nodes, and the data acquired by the network nodes in different satellite layers are heterogeneous. To facilitate the processing of massive data information, we must consider unifying and integrating data when designing routing algorithms." |
| O18 | 308 | "When the network state changes, the algorithm quickly converges and makes a better routing decision." |
| O19 | 310 | "In the subsequent research, deep learning and reinforcement learning can be used to improve satellite network routing decision making. In particular, improving deep learning technology and expanding MEC’s use in satellite networks to boost network performance will be important." |
| O20 | 314 | "Inter-layer contacts are frequently interrupted in multi-layer satellite networks due to the rapid relative motion between satellites in different layers. The network topology is constantly changing, leading to a frequent dynamic reconfiguration of inter-satellite routes. Hence, building a multi-layer satellite network based on artificial intelligence is the way forward" |
| O21 | 316 | "In the next satellite routing optimization matter, scalability is an important property to satisfy the routing algorithm. Existing ML routing algorithms handle small topological networks with up to 20 satellite nodes. A larger topology means an exponentially growing number of network states and a greater difficulty in routing decisions. Future intelligent routing algorithms must achieve good results on large topologies." |
| O22 | 316 | "Compared with traditional routing algorithms, intelligent routing requires more computational resources and higher routing performance. In addition, for smart routing, how to deploy in real scenarios is also a great challenge. Although SDN networks have enhanced the computational power of the router control layer, intelligent routing algorithms are still difficult to deploy at scale in existing satellite network architectures" |
| O23 | 316 | "In the future, smart routing algorithms may focus on designing smart routing devices." |
| O24 | 257 | "However, the approach has not explicitly proposed an optimal traffic allocation strategy to avoid link congestion problems, and the ability to solve severe network congestion is greatly limited." |
| O25 | 259 | "However, the traffic balancing mechanism fails to account for the queuing delay in the link. Similarly, the existing dynamic balanced routing for traffic focuses on end-to-end delay. Nevertheless, such routing algorithms perform better only when the traffic is not overloaded. As the complexity of the network increases, multi-layer satellite network service requirements grow, causing a high packet loss rate and long queuing delay." |
| O26 | 261 | "Therefore, congestion and queuing delays must be added to the routing scheme for dynamic traffic balancing." |
| O27 | 265 | "Therefore, in future research, for the multi-layer satellite network traffic-balancing dynamic routing algorithm, how to achieve the optimal traffic distribution of heterogeneous links will become the focus of attention of academia and industry." |
| O28 | 253 | "As the satellite network topology is predictable and periodic, the satellite can predict traffic congestion and adjust its routing strategy." |
| O29 | 287 | "However, the high input/output feature dimensionality can be formulated via objective function variables, and the satellite routing optimization problem can be formulated via objective functions." |

### 5.2 涉及"负载过程/突发/时延/到达率/信用分配/决策成本"的表述（逐字 + 行号）

| 行号 | 逐字原文 | 归类 |
|---|---|---|
| 119 | "Unbalanced Load Traffic: Geographical conditions, satellite motion, and the Earth’s rotation characterize the time-varying nature and uneven distribution of load traffic in satellite networks." | **负载过程**：时变 + 不均匀 |
| 119 | "As the satellite is constantly in motion, the number of terminal users and the amount of load traffic within the network are changing." | 到达量随时间变化 |
| 111 | "Complete re-routing means redistributing new routing paths for communicating with users after the link has already completed switching. For such routing strategies, the optimal routing of the network is ensured but at the expense of a certain computational overhead." | **决策成本**（重路由的计算开销） |
| 113 | "The link transmission delay between LEO satellites is 15–25 ms, while the transmission delay between MEO satellites is 40 to 60 ms." | 时延量化登记 |
| 113 | "the approach is prone to making each satellite node calculate routing tables with inaccurate network state information, leading to the waste of on-star computing resources" | 状态信息不准 → 算力浪费（决策成本） |
| 115 | "With the limited on-star computing power, the on-star routing algorithm must have low implementation complexity (namely, low computational complexity), communication costs, and storage costs." | **决策成本三重约束**（算力/通信/存储） |
| 117 | "Re-routing mechanisms increase network latency and cannot meet QoS latency requirements, causing communication disruptions." | 重路由 → 时延 |
| 131 | "The motivation of network slicing in a space information networks (SIN) is to allocate as few resources as possible to satisfy the end-to-end transmission demands. Theresource requirements vary with the types of services. For delaysensitive services, such as video communication, high reliability and low delay paths are required to support the real-time transmission, but the delay-tolerant services, such as Earth observation, require a high data rate with a tolerant time delay." | 业务类型 → 时延/速率需求差异 |
| 253 | "As the satellite network topology is predictable and periodic, the satellite can predict traffic congestion and adjust its routing strategy." | 拓扑可预测 → 拥塞可预测 |
| 257 | "The approach takes full advantage of the real-time queuing delay of the satellite link and the congestion between the current and next-hop satellite nodes. The packet loss rate and queuing delay are diminished, and the transmission efficiency of the network is enhanced." | 队列时延作为路由代价 |
| 257 | "By using the idea of an adaptive routing protocol for QoS (ARPQ), calculating the maximum traffic threshold of the link was proposed in [98]. When the traffic transmitted on the link exceeds the threshold, the congested traffic is assigned to the MEO satellite. Otherwise it is transmitted directly to the LEO satellite." | **到达率阈值触发的分流** |
| 257 | "SLSR takes into account the latency of the network and the expected waiting delay when calculating routes. Such an approach allows network data traffic to be evenly forwarded over multiple lightly loaded links instead of the shortest link." | 期望等待时延（排队过程） |
| 259 | "In multi-layer satellite networks, owing to the non-equal distribution of users, LEO satellites are prone to massive network congestion when they pass through areas of high traffic." | 高流量区导致拥塞 |
| 259 | "Based on the prediction of traffic distribution, the work in [103] presented a parametric adaptive multi-attribute decision making (PASMAD) access and switching algorithm for GEO–LEO heterogeneous satellite networks." | 基于流量分布预测的决策 |
| 259 | "Furthermore, since the algorithm adopts real-time data collection to complete the routing operation, a corresponding load balancing mechanism is omitted." | 实时采集数据的代价 |
| 261 | "The method accurately detects queuing delays and dynamically adjusts routing paths according to queue changes. The solution can predict link conditions before congestion occurs on the link and reasonably select suitable routes based on various traffic situations in the link." | 队列变化驱动路由 |
| 261 | "Moreover, in a multi-layer satellite network, multiple satellite nodes need to transmit data simultaneously. However,the limitation of the storage resources of the satellite network can make the data among the nodes conflicting." | 并发传输 + 存储受限 |
| 261 | "Furthermore, Stackelberg traffic balance routing uses a threshold function to convert non-convex optimization into convex optimization." | 阈值函数（形式化，逐字抄录） |
| 263 | "Link overload traffic in densely populated areas can easily cause network delays and throughput crashes due to satellites’ geographical limitations." | 过载 → 时延/吞吐崩溃 |
| 265 | "Proper end-to-end (E2E) traffic prediction in multi-layer satellite networks plays a critical role in balancing traffic. The work in [108] presented an improved Markov model (HMM)- based method for E2E traffic prediction." | **E2E 流量预测（HMM）** |
| 265 | "Moreover, despite the large volatility of the actual service traffic in existing multi-layer satellite networks, the approach is still better at predicting and tracking the traffic on the links with low error." | **实际业务流量的大波动性**（本篇对"突发"的最近似表述） |
| 265 | "The trained traffic scheduling model can make fast routing decisions for congested traffic detected over the link and maximize link utilization." | 快速决策（决策时延） |
| 265 | "The algorithm introduces a delay upper bound in heterogeneous links to optimize traffic allocation with the least delay." | 时延上界约束 |
| 277 | 表 12 表头逐字："**Scheme \| Time Delay \| Packet Loss Rate \| Calculation Overhead \| Throughput**" | **Calculation Overhead 被列为路由方案的评价维度**（决策成本的制度性登记） |
| 287 | "The trained GNN model is able to achieve 98% accuracy within 15 iterations relative to shortest-path routing." | **收敛速度量化**（15 次迭代） |
| 294 | "So, the high computing agility and low latency can be achieved" | 边缘计算降低时延 |
| 300 | "the large amount of data generated by monitoring the solid satellite platform is used to improve the accuracy and predictability of information space models., significantly reducing the computational complexity of the dynamic routing strategies in multi-layer satellite networks." | 数字孪生降低路由决策复杂度 |
| 316 | "(2) Efficiency. Fast inference based on the input data can obtain the optimized routing decision in polynomial time" | **决策成本＝多项式时间推理** |
| 316 | "A larger topology means an exponentially growing number of network states and a greater difficulty in routing decisions." | 状态空间指数增长 |
| 308 | "MEC platforms allow edge networks to gain management access to computing and services to reduce mobile users’ network latency and bandwidth consumption." | 时延/带宽消耗 |

### 5.3 负向声明核验（模式 / 实测计数 / 命中判定）

- 模式 `credit` → **实测计数 0**。注意：本篇正文 L-unknown 处有 "routing cost"、"minimize path costs" 等词，但 `credit` 作为独立词确实零命中（已用 `grep -ciE 'credit'` 核验，非裸词匹配）。
- 模式 `arrival rate` → **实测计数 0**；`arrival process` → **实测计数 0**；`Poisson` → **实测计数 0**。
- 模式 `burst` → **实测计数 0**。注意：本篇 L265 用 "large volatility of the actual service traffic" 描述波动，但**未使用 burst 一词**（已用精确模式核验）。
- 模式 `self-similar` → **实测计数 0**；`non-stationar` → **实测计数 0**。

### 5.4 它提到但本库其他论文未跟进的方向

1. **数字孪生（Digital Twin）驱动的动态拓扑建模与路由预演**：298–302。本库 111 篇题录内无数字孪生论文。
2. **多尺度信息感知与复杂环境下的算力协同（MEC + 大数据分析驱动路由状态感知）**：308。本库无对应论文。
3. **智能卫星（可重定义需求/软件可重构/功能可重构的星上操作系统）**：312。本库无对应论文。
4. **智能路由设备（面向星上部署的专用硬件）**：316。本库无对应论文。
5. **动态网络切片在空间信息网络中的多维资源柔性调度**：131。本库无网络切片论文。
6. **星间太赫兹/激光高速传输与 IM/DD 检测方案比较**：123、129。本库无物理层传输论文。
7. **星上处理/星上交换/星上路由（OBP/OBS/OBR）硬件技术**：127。本库无对应论文。
8. **以"计算开销（Calculation Overhead）"为独立评价维度的路由方案对比表**：277 表 12。本库 T1 论文普遍只报时延/丢包/吞吐，未见把计算开销列为并列评价维度（需 T1 档复核）。

---

## 6. T9X6QCLL — LEO SATELLITE NETWORKING RELAUNCHED: SURVEY AND CURRENT RESEARCH CHALLENGES

- 本地定位：TIER-ASSIGNMENT.md:108，"综述：只取共识与开放问题，不承重"
- MD 总行数：899
- 读取范围：第 1–31 行（标题/摘要/1. INTRODUCTION）、159–188 行（4.3 Load balancing 全节）、271–284 行（4.8 Low latency networking 全节）、462–501 行（6. CHALLENGES AND FUTURE RESEARCH DIRECTIONS 全节 + 7. CONCLUSIONS）。
- **未通读（如实声明）**：32–158 行（2. Related work、3. 概览、4.1/4.2）、189–270 行（4.4 SDN、4.5 ML、4.6 DTN、4.7 地理路由、4.9 多层）、285–461 行（4.10/4.11 与 5. 标准化 3GPP/IETF）。
- **文本质量警示**：该 MD 存在 MinerU 连字替换伪影（`fi` 被替换为 `ϐ`/`ϔ`、连字符被替换为 `‑`），下列引文**按 MD 原样逐字抄录，未做还原**，以免改变原文。

### 6.1 该综述认定的开放问题清单（逐字 + 行号）

| # | 行号 | 逐字原文 |
|---|---|---|
| O1 | 464 | "Satellite networks have obvious beneϐits in terms of coverage and global latency. However, there are also some downsides and challenges to solve." |
| O2 | 466 | "Challenge ‑ reliability: For instance, a satellite orbit may provide useful coverage for only part of the time; the rest of the time is covering the poles or some empty areas such as oceans." |
| O3 | 466 | "The issue of debris (for instance, as monitored by Leo‑Labs [175]) in space has become an issue, as well as a business opportunity. LEO satellites are lightweight and move extremely fast, which makes any collision or impact challenging." |
| O4 | 466 | "One challenge is to provide reliable networking in an environment that becomes more and more crowded and difϐicult." |
| O5 | 468 | "Challenge ‑ vertical integration: Another future challenge is to further integrate multiple layers: we discussed the interaction ofLEO, MEO and GEO satellites already, but there are layers below as well." |
| O6 | 472 | "There are few, if any, commercial deployments but it seems that a sparse global satellite network augmented with an aerial network over denser areas brings out the best of both worlds." |
| O7 | 476 | "Integrating all these layers probably would require a dynamic framework to manage the network across all these layers, building upon SDN and machine learning." |
| O8 | 478 | "Challenge ‑ application support: At the application layer, there are challenges to support new applications over LEO satellite networks." |
| O9 | 480 | "Yet, such an application requires stringent delay and reliability that is difϐicult to achieve through satellite networks. Providing reliable low latency communications over LEO networks is still an open challenge." |
| O10 | 484 | "Challenge ‑ interoperability: We presented the current status of standardization efforts for satellite networking. There has been some work on giving virtual network operators hooks into the satellite network by using virtualization [182], which is a step into opening satellite networks." |
| O11 | 486 | "However, most satellites are currently incompatible between networks operated by different companies. Each company manages their networks independently and there is little incentive for a large constellation operator to share that infrastructure with a smaller competitor." |
| O12 | 488 | "Further, current satellites have a limited number of ISLs. This is due to the fact that ISLs are complex; the distance between two satellites may reach 2000 miles. Such links can be pointed at other satellites traveling in the same or neighboring orbital planes, since the relative motion is limited (similar speed, similar travel direction). This reduces the need to interoperate, as one single operator may use up these few links to set up their own topology without having the need, nor the resource, to connect to other operators." |
| O13 | 490 | "However, this may be unsustainable. Increasing light pollution, produced by low earth orbit satellites, is becoming an issue for astronomers. Space debris is another issue where coordination is necessary." |
| O14 | 492 | "As the number of links on a satellite grows, this portends towards greater interoperability and the need towards global standards to maximize the utilization of the constellations up in space." |
| O15 | 500 | "We ϐinally discussed some of the challenges that future research should tackle, with an emphasis on network reliability, cross‑layer integration, application support and interoperability." |
| O16 | 187 | "What next? Without data from satellite network operators, it is difϐicult to establish the practical need for load balancing mechanisms." |
| O17 | 187 | "But we would need to know the utilization of these links to assess whether shortest‑path routing leads to congestion issues." |
| O18 | 283 | "What next? Low latency is one important driver for satellite networks. There is a huge premium in delivering some trafϐic faster." |
| O19 | 283 | "It also seems common sense that satellites will not carry huge buffers to introduce some congestion delays. The space for optimization, in addition to some basic QoS mechanisms, seems limited." |
| O20 | 474 | "It was shown to have applicability to space networks in [180], even though the original project targeted low‑connectivity areas in Africa." |

### 6.2 涉及"负载过程/突发/时延/到达率/信用分配/决策成本"的表述（逐字 + 行号）

| 行号 | 逐字原文 | 归类 |
|---|---|---|
| 161 | "Satellite networks suffer from a very uneven distribution of the trafϐic. Indeed, to provide global coverage, the satellites are distributed all over the Earth, which has a very uneven density of population." | 负载不均匀（空间维度） |
| 163 | "But very little trafϐic will originate there. Further, the satellite will follow a trajectory that may take them to areas where they are less critical (say, above the poles, where the distance between satellites shrink when in polar orbit). On the other hand, some links between densely connected areas may see a lot of trafϐic." | 负载随轨道位置变化（时间维度） |
| 165 | "This, plus the dynamic topology, as well as the large number of nodes, creates the need for care in load balancing the trafϐic. This has been a very active area of investigation." | 动态拓扑 + 负载均衡 |
| 167 | "Nodes inform neighbors when they are about to reach a congestion threshold, and ask them to throttle the trafϐic towards them. The neighbors then try to route around the congested node. This is called Explicit Load Balancing (ELB)." | **到达率阈值 + 邻居限流**（拥塞反馈闭环） |
| 171 | "This allows us to decompose the trafϐic into a predictable long‑term baseline, and some variable short‑term ϐluctuations. The former is managed ahead of time using some global optimization, while the latter is handled dynamically and locally." | **负载过程的两尺度分解**（长期基线 + 短期波动）——本批 13 篇中对"负载过程"最明确的表述 |
| 171 | "This takes into account the periodically deterministic nature of the network topology as well, as well as the predictive nature ofthe considered trafϐic (here, IoT but this can be generalized to other forms of trafϐic)." | 拓扑周期性 + 流量可预测性 |
| 173 | "In [72], another hybrid load balancing approach is proposed: they use a prediction of the regional and real‑time network states, as input to a multipath route calculation. The goal is to avoid cascading congestion by balancing trafϐic onto a path that becomes congested, that again shifts the trafϐic away." | **级联拥塞**（负载迁移的次生效应） |
| 175 | "The route selection takes into account both congestion level, as well as end‑to‑end delay estimate. This method combines ofϐline computation and online adjustments. (In addition to load balancing, the paper also takes into account, and simpliϐies, the computation of the route table lookups)." | **离线计算 + 在线调整**；路由表查找计算被简化（决策成本） |
| 177 | "Back‑pressure routing is applied to satellite networks in [74], which proposes a distributed Distance‑based Back‑Pressure Routing (DBPR). The distance metric used is a combination of shortest path and congestion. The routing is restricted to a rectangle deϐined by the source and the destination of the trafϐic, so as to limit hop count and reduce delay." | 背压路由（队列稳定性理论）+ 限制跳数以降时延 |
| 179 | "It uses an ant colony algorithm as heuristics to solve a multiobjective optimization problem, where the objectives include minimizing path costs, but also minimizing congestion (based upon a prediction of the trafϐic) so as to achieve load balancing." | 基于流量预测的拥塞最小化 |
| 181 | "It ϐirst dynamically divides the satellites between a lightly loaded zone, where there is little trafϐic, and a heavily loaded zone, where there is more trafϐic. For instance, densely populated areas would map to heavily loaded zones. As there is little need for load balancing in the lightly loaded zone, a pre‑balancing shortest path algorithm can be applied. In the heavy zone, a congestion index is used to ϐind a minimum weight path so as to spread the trafϐic." | **分区（轻载/重载）差异化策略** |
| 183 | "It is a one‑step distributed computation based on the location of the current node and that of the destination. Further, each node shares with its neighbors its congestion level, so that packets may be directed according to the congestion level of the links." | 单步分布式计算（决策成本极低） |
| 185 | "Indeed, it classiϐies the trafϐic into three categories: latency sensitive, throughput sensitive, and ordinary (best effort) trafϐic." | 业务分类与时延敏感度 |
| 273 | "Here we consider the end‑to‑lend latency of a packet in the network, between leaving the source and arriving at the destination (or alternatively, the Round‑Trip Time (RTT))." | 时延定义口径 |
| 281 | "It obtains the minimal path set based on a delay queueing variant of GERT (DQ‑GERT) then the delay index is computed that includes the delay and the delay variation on the path." | **时延抖动（delay variation）**纳入路径代价 |
| 482 | "An empirical study of the Starlink network [181] for instance ϐinds a loss rate of 0.4% in lightly loaded scenarios, and of 1.5 2% in congested scenarios, as well as a delay that increases signiϐicantly from 50ms median RTT (light load) to roughly 100ms RTT (congested network)." | **负载水平→丢包率/时延的实测定量关系**（本批最有定标价值的一条） |
| 283 | "It also seems common sense that satellites will not carry huge buffers to introduce some congestion delays. The space for optimization, in addition to some basic QoS mechanisms, seems limited." | 缓冲容量受限 → 排队时延空间受限 |

### 6.3 负向声明核验（模式 / 实测计数 / 命中判定）

- 模式 `credit` → **实测计数 0**。
- 模式 `arrival rate` → **实测计数 0**。
- 模式 `arrival process` → **实测计数 0**。
- 模式 `Poisson` → **实测计数 0**。
- 模式 `burst` → **实测计数 0**。注意：本篇 L171 用 "variable short‑term ϐluctuations" 描述短期波动，L173 用 "cascading congestion"，但**均未使用 burst 一词**（已用精确模式 `burst` 核验为 0）。
- 模式 `self-similar` → **实测计数 0**。
- 模式 `non-stationar` → **实测计数 0**。

### 6.4 它提到但本库其他论文未跟进的方向

1. **面向"可预测长期基线 + 短期波动"的两尺度负载管理框架**：171。本库 T1/T2 路由论文均以瞬时负载/队列状态为输入，未见显式两尺度分解的设计（可在 T1/T2 档复核，本档只登记综述侧表述）。
2. **背压路由（Back-Pressure Routing）在卫星网络的应用**：177。本库 111 篇题录内无背压/队列稳定性理论路由论文。
3. **延迟抖动（delay variation）作为路径评价指标（DQ-GERT）**：281。本库 T1 论文的奖励/代价函数未见抖动项（本档仅登记，需 T1 档核验）。
4. **SDN 管理随时间演化的拓扑（Loon/Aalyria 路线）**：474。本库无 SDN 拓扑管理论文。
5. **空天地多层统一动态框架（SDN + ML 跨层）**：476。本库无跨层框架论文。
6. **星座间互操作与虚拟网络运营商（VNO）接口标准化**：484–492。本库无标准化/互操作论文。
7. **天文光污染与碎片协调**：490。本库无对应论文。
8. **以运营商实测数据评估负载均衡的必要性（link utilization 可得性）**：187。本库 T1 全部为仿真，无运营商实测利用率数据驱动的结论。
