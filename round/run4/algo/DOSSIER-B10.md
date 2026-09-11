# DOSSIER-B10：T5 背景级综述 13 篇——开放问题清单 + 负载过程相关表述

> 批次：T5（背景级综述 13 篇），产出文件 DOSSIER-B10.md。
> 依据：`round/run4/algo/TIER-ASSIGNMENT.md` 第 102–114 行将下列 13 篇定为 T5（"综述：只取共识与开放问题，不承重"）。
> 深度定义（TIER-ASSIGNMENT.md:129）："读摘要+开放问题/挑战节；产出该综述认定的开放问题清单含行号、与负载过程/信用分配相关的表述"。
> 全文来源：MinerU MD，VM 路径 `/data/liguang13/topic-loop-r2/md/<itemKey>/<itemKey>/txt/<itemKey>.md`。
> **所有引文均为该 MD 的行号 + 逐字英文原文**；本文件不含我的评价性改写（除每篇第 3 项按要求做的"本库未跟进"对照，其依据写在文中）。
> 红线遵守：负载/流量/评测设置只作条件登记，不作贡献；判"未见"均写明检索词与范围。

**批次清单（13 篇）**：2QRYMWBI、LNA28YZY、7AXASN73、IP7RRM3A、LRSXMWX9、QSNRQ8PF、T9X6QCLL、Z74SR656、L5F3DK68、UMKF328H、BV4XI6CU、524XNF29、5AZHJE7N

---

## 1. 2QRYMWBI — Artificial Intelligence for Satellite Communication and Non-Terrestrial Networks: A Survey

- 本地定位：TIER-ASSIGNMENT.md:102，"综述：只取共识与开放问题，不承重"
- 读取范围：MD 总 1933 行；本次通读第 1–20 行（标题/摘要）、542–604 行（星座路由、IoT 接入、流量/拥塞预测）、794–900 行（VI. CHALLENGES AND OPEN DISCUSSION 全节：A. Implementation Challenges、B. AI Accelerators、C. Future AI Frontiers/Visions、D. Security Aspects、E. Cost Optimization）

### 1.1 该综述认定的开放问题清单（逐字 + 行号）

| # | 行号 | 逐字原文 |
|---|---|---|
| O1 | 796 | "there are still a number of points that need to be further investigated to unleash the potential of ML into the satcom industry." |
| O2 | 796 | "The main point of discussion resides on where the ML is deployed." |
| O3 | 798 | "At this point, we could not identify any previous work where a tradeoff in terms of ML potential performance benefit versus added cost and complexity on the satellite device." |
| O4 | 806 | "One of the main challenges is determining the best place to deploy ML: should it be deployed on the ground or onboard the satellite?" |
| O5 | 808 | "If on-board deployment is chosen, limitations in terms of power consumption, mass, and the need for additional interfaces to interface with the ML block must be considered." |
| O6 | 810 | "However, the challenges of data transmission back and forth between the satellite and the ground control center must be taken into account." |
| O7 | 812 | "There are challenges in selecting the most appropriate ML algorithms for each specific task, the availability of training data, the extensive training length, validating and verifying the model to ensure its reliability, and implementing adequate security systems to protect the ML and the data it handles." |
| O8 | 816 | "It is important to consider the radiation tolerance of the hardware used." |
| O9 | 820 | "it is important to keep in mind that hardware technology continues to evolve rapidly and that hardware component costs can be significant for the development and implementation of ML-based NTN systems." |
| O10 | 822 | "The availability of real world datasets is one of the most crucial preconditions for evaluating any proposed Machine Learning based method. So far, the cost and access difficulty of highly representative datasets has hindered the development in Satellite Communication of Machine Learning techniques." |
| O11 | 822 | "advanced techniques such as Deep Learning and Deep Reinforcement Learning requires a large dataset to converge and reach the desired performance. It is time consuming and costly to generate large dataset for Satellite Communication using simulators. In addition, even assuming large datasets can be produced via simulations, their accuracy remains a key open discussion point." |
| O12 | 822 | "This makes it a tremendous challenge to compute the accuracy and scalability of the proposed Machine Learning models in the real world." |
| O13 | 824 | "Using large data dimensions during the learning and testing increases computational complexity and slows the decision-making process." |
| O14 | 830 | "The deployment of ML onboard satellites faces a significant challenge in terms of radiation tolerance." |
| O15 | 838 | "One of these is limited computational resources in space environments, where efficient and fast data processing is needed." |
| O16 | 842 | "Integrating specialized hardware into existing systems can be costly and require significant changes to satellite infrastructure. In addition, careful design and rigorous validation are required to ensure the reliability and safety of SatCom systems using these advanced technologies." |
| O17 | 844 | "In the future, deploying ML for satellite communications will set new challenges for computer processors, which will have to support large workloads as efficiently as possible in harsh environmental conditions." |
| O18 | 844 | "legacy technologies are expected to hit a ”digital wall” in 2025, potentially forcing a paradigm shift in terms of computing technologies" |
| O19 | 850 | "Satellite Communication’s deployment of systems globally has led to an increasing demand for ML solutions operating in distributed systems." |
| O20 | 854 | "First, local devices and the central server must communicate reliably to ensure data integrity and model updates. In addition, federated ML models need to be able to handle heterogeneous data and devices with different processing capabilities." |
| O21 | 856 | "Another major challenge is ensuring data privacy and security. Because data is held on local devices, robust security and privacy measures must be implemented to protect user and organizational data." |
| O22 | 858 | "ML in blockchain applications applied to SATCOM is currently a crucial challenge where only a few preliminary works are presented in the literature." |
| O23 | 862 | "while the heterogeneity and limited resources of MCU devices present new challenges for on-device training, model updating, and deployment, recent research and the development of MLframeworks such as TensorFlow Lite for Microcontrollers have increased the accessibility of TinyML." |
| O24 | 874 | "a major challenge in the operation of the CubeSats and small satellites within NTNs in lower altitudes is the rather low information processing capabilities of the onboard processors. Consequently, developing and utilizing AI models in these entities can be beyond the capability of a single satellite processor." |
| O25 | 876 | "while it is clear that the next generation of satellites will rely on Artificial Intelligence, it is unclear how Artificial Intelligence should be integrated into the architecture of satellite networks." |
| O26 | 876 | "Most of the data-driven approaches surveyed in this paper (see table III) are based on Neural Network and Deep Reinforcement Learning techniques that require a large amount of data and are complex to process. Therefore, it is convenient to investigate that to mitigate the computational complexity, latency, and power consumption." |
| O27 | 886 | "One of the biggest risks is the potential manipulation of training data and exploitation of vulnerabilities in the trained ML model, which could adversely affect the quality of transmitted data and the integrity of the SatCom system. In addition, the use of real-time ML systems also introduces the possibility of realtime attacks, such as malicious data injection into the ML model." |
| O28 | 884 | "Together with it, explainability, bias also ethical issues are becoming increasingly important as a result of data collection, the approaches used for analysis, the manner and purpose for which the results from such analyzed are used" |
| O29 | 894 | "When considering the deployment of ML systems, the costs of the necessary components and the resources required to train and maintain the ML models must be considered." |
| O30 | 898 | "Cost optimization must also consider the scalability of ML systems. As more and more satellites are deployed, scalable and cost-effective solutions must be found to train and maintain ML models on all satellites." |
| O31 | 566 | "The authors consider the agent to be placed on the satellite and consider onboard training without, however, offering an overview of the demanded computational power to run the proposed Reinforcement Learning algorithm." |

### 1.2 涉及"负载过程/突发/时延/到达率/信用分配/决策成本"的表述（逐字 + 行号）

| 行号 | 逐字原文 | 归类 |
|---|---|---|
| 574 | "Overall, due to population imbalance based on different causes such as terrain shape and weather, traffic convergence to certain satellites usually occurs in constellations of mesh satellites with lower orbits. Therefore, intelligent routing control technology and smart resource management are necessary for multilayer satellite networks to coordinate the traffic load according to QoS requirements effectively." | 负载的空间不平衡（非时间过程） |
| 576 | "Monitoring changes in the incoming traffic rate is the most general way to detect network congestion that occurs when rate measurements exceed a predefined or dynamically adjusted threshold." | 到达率→阈值判据 |
| 576 | "Balancing the load is a timely procedure that, however, might not be enough to prevent network congestion effectively. To overcome this challenge it is necessary to develop and employ congestion prediction mechanisms for load balancing by distributing the traffic amongst available network resources." | 负载均衡 vs 预测（"timely"＝时效性） |
| 578 | "Two categories of prediction methods, based on long and shortterm’s periods, are typically considered. The former, longterm traffic prediction, estimates future capacity requirements, enabling more effective planning decisions. The latter, predictions within minutes, even seconds, is usually linked to dynamic resource allocation." | 负载过程的时间尺度（分钟/秒级 vs 长期） |
| 582 | "In the normal state where no congestion event is detected, an LEO satellite attempts to catch a congestion precursor by simply monitoring the incoming traffic rate and not exhibiting any load balancing behavior." | 拥塞前兆（precursor）监测 |
| 588 | "Authors of [361] introduce an hybrid architecture composed by stacking Convolutional Neural Network and Long Shortterm LSTM which produce predictions of the traffic for a particular beam in a two-hours window with a resolution of 5 minutes." | 负载预测窗口（2 小时窗 / 5 分钟粒度） |
| 588 | "Despite it is not possible to detect outliers and peaks in traffic prediction, the results unveil predictions at trending level, proposing a mechanism to indicate the level of future congestion." | 突发的**不可预测性**：明确说检测不到 peaks/outliers |
| 566 | "Probabilities of transition between states are expressed analytically based on the Poisson process for both contentionbased and contention-free random access." | 到达过程＝Poisson（本文唯一显式到达过程建模处） |
| 566 | "The authors consider the agent to be placed on the satellite and consider onboard training without, however, offering an overview of the demanded computational power to run the proposed Reinforcement Learning algorithm." | 决策/训练成本未被报告（作者批评前作） |
| 576 | "Intelligent routing control technology and smart resource management are necessary for multilayer satellite networks to coordinate the traffic load according to QoS requirements effectively." | 负载与 QoS 的耦合 |
| 550 | "In [125], authors propose a DRL algorithm where the rational agent of the model learns following the replays and selects the route with the smallest Round Trip time. The routes chosen, although in principle crossing more nodes, and therefore longer, in the end, have better effectiveness and a lower load on the bottleneck router." | 时延（RTT）作为路由目标 + 瓶颈负载 |
| 548 | "First, a valuable routing algorithm should guarantee each application’s required QoS, e.g. latency, packet loss, and data rate." | 时延作为 QoS 约束 |
| 560 | "Successive improvements, such as in [353], have allowed new RA methods to achieve low `$( < 1 0 ^ { - 3 } )$` Packet Loss Probability (PLR) even at high (≥ 1) network loads, enabling applications in massive machine-type communications (mMTC)." | 负载水平与丢包率的定量关系（公式逐字抄录） |
| 422 | "While the terminal segment predictions require a time window similar to the propagation delay, the ground segment usually needs longer time windows for performing missionlevel operations such as gateway switching." | 预测时间窗 vs 传播时延（决策时标） |

**信用分配（credit assignment）**：在本篇全文范围内（检索词 `credit`，区分大小写不敏感，范围＝整篇 1933 行）**未见**任何 RL 信用分配/功劳归因表述；`credit` 仅以 "Credits: NASA" 式图片署名的形式出现，无技术含义。（检索命令：`grep -niE 'credit' <MD>`）

### 1.3 它提到但本库其他论文未跟进的方向

判定基准：本库 111 篇题录见 TIER-ASSIGNMENT.md:9–119（T1 路由+学习 34 篇 / T2 路由但非学习 32 篇 / T3 测量平台 AoI 16 篇 / T4 通用 RL 11 篇 / T5 综述 13 篇 / T6 领域外 5 篇）。以下方向在本批 13 篇综述之外的题录中**未见对应论文**。

1. **星上 AI 硬件与容辐（radiation tolerance）**：830–834、816、838–842。本库无任何星上处理器/加速器/容辐硬件论文。
2. **类脑/神经形态处理器（Neuromorphic Computing）作为星上协处理器、流式处理**：844–846。本库无对应论文。
3. **联邦学习（Federated Learning）在卫星星座上的部署与其通信可靠性/异构设备问题**：850–856。本库 T1/T2 全部为单星或星座级 RL 路由，无联邦训练论文。
4. **ML + 区块链（Blockchain）用于 SATCOM 的可信流量卸载**：858。本库无对应论文。
5. **TinyML 在星上 MCU 的端侧训练/模型更新**：860–862。本库无对应论文。
6. **量子计算加速 AI 训练 / 空基量子云卸载算力**：864–874。本库无对应论文。
7. **AI 的可解释性/偏见/伦理在 SATCOM 数据链上的落地**：884。本库无对应论文。
8. **ML 部署的成本优化（$ per Gbps、卫星重量-功耗-寿命权衡、规模化训练维护成本）**：894–898。本库无对应论文；本库所有 RL 路由论文均未把部署成本纳入评价。
9. **数据降维（feature extraction/selection）以降低决策时延**：824–828。本库 T1 路由论文的状态设计未见以"降维以加速决策"为目标的工作。

---

## 2. LNA28YZY — Satellite Communications in the New Space Era: A Survey and Future Challenges

- 本地定位：TIER-ASSIGNMENT.md:103，"综述：只取共识与开放问题，不承重"
- 读取范围：MD 总 1398 行；本次通读第 1–18 行（标题/摘要/引言）、600–694 行（IX. FUTURE & OPEN TOPICS 全节：A. Cooperative Satellite Swarms … J. Digital Twins for Satellite Systems、X. CONCLUSION），并对全文做关键词检索（见 2.2 末）

### 2.1 该综述认定的开放问题清单（逐字 + 行号）

| # | 行号 | 逐字原文 |
|---|---|---|
| O1 | 606 | "Some implementation of DSS, such as constellations and satellite trails, are relatively well-established, whereas satellite swarms are still in an active research and development area" |
| O2 | 610 | "The synchronization of the swarm nodes is a very challenging task due to the dynamic characteristics of the transmission channel between the nodes, and the limited accuracy of the time and frequency references available at the small satellites" |
| O3 | 610 | "For this reason, how to facilitate the ISLs among satellite nodes in a swarm is still an open research topic." |
| O4 | 614 | "However, due to the difference in the height and velocity, link connections between intermediate layers are directly affected, e.g. the HAPS and the UAVs may be frequently disconnected." |
| O5 | 614 | "Therefore, how to harmonize the flight of the UAVs and the HAPS to maintain reliable connections is of great importance, as the current routing protocol is not applicable to vertical space networks." |
| O6 | 614 | "One should note that the desired routing protocol for vertical area networks should take into account the heterogeneous connects between the links, e.g., free space optical among the HAPS, hybrid radio frequency/free space optical between the HAPS and UAVs." |
| O7 | 614 | "Another open problem is how to efficiently deploy the hierarchical area network [22]. A joint design of communications and HAPS/UAV flights is expected to achieve the required global performance and it still represents an open research topic. This includes not only UAVs and HAPs placement design but also trajectory optimizations." |
| O8 | 625 | "Open research topics in this direction include network modeling, routing, and congestion control." |
| O9 | 631 | "Key aspects include serving a terminal using multiple satellites and appropriate routing of the packets over ISLs." |
| O10 | 631 | "Also, another crucial aspect worth considering is the power budget analysis." |
| O11 | 637 | "In this regard, there arises the need to investigate more dynamic/flexible approaches for the realtime mitigation of inline interference events, which may occur while operating GSO-NGSO or NGSO-NGSO satellites over the same frequency band." |
| O12 | 645 | "In particular, the new on-board processing capabilities combined with the emerging role of active antenna systems, require advanced resource management techniques." |
| O13 | 645 | "These novel techniques should be capable of maximizing the satellite resource utilization while maintaining QoS guarantees, and dynamically match the geographic distribution of the traffic demand by following its variations in time." |
| O14 | 657 | "Firstly, one of the main challenges is to devise networkslicing algorithms, e.g., slicing configuration, virtual resource isolation, that can efficiently and autonomously configure the large number of parameters present in a virtualized dynamic graph representing an integrated satellite-terrestrial transport network." |
| O15 | 657 | "Secondly, one should note that most of the works on virtual network embedding (VNE) are based on a static design, i.e., based on a snapshot of a deterministic network graph, but a realistic integrated NGSO satellite-terrestrial network is highly dynamic, resulting in fast variations of the virtual network topology over time." |
| O16 | 657 | "Dealing with the graph dynamics in the context of online network-slice management is an essential challenge." |
| O17 | 657 | "Thirdly, the de facto standard protocol between the data and control planes, i.e., OpenFlow, in SDN/NFV networks has to be extended and become compatible to satelliteterrestrial networks by considering satellite characteristics, e.g., LEO and MEO satellites’ motion, available on-board energy, storage capacity, and computational power." |
| O18 | 663 | "Key to the success of QKD over satellites is the ability to set-up stable optical links by overcoming the various impediments in transmission." |
| O19 | 673 | "some promising use-cases to investigate the applications of ML techniques include: (i) adaptive allocation of carrier/power for the hybrid satellite-terrestrial scenarios, (ii) adaptive beamforming to enhance the performance of multibeam satellites with non-uniform demand, (iii) scheduling and precoding to mitigate interference in multibeam satellites, (iv) beamhopping and resource scheduling in multi-beam satellite systems with heterogeneous traffic demand per beam, and (v) detection of spectrum events in spectrum monitoring applications" |
| O20 | 685 | "However, the introduction of digital twins for satellite industries is relatively new and several challenges need to be addressed to effectively implement this in practical systems." |
| O21 | 685 | "Also, data management being a crucial aspect for the digital twin implementation, one important issue to be addressed is to ensure the privacy of individual entities and to prevent the information misuse." |
| O22 | 685 | "Other future issues include how to manage the space debris and pollution by removing the failed or inoperative satellites and how to regulate the digital twin-enabled infrastructure in terms of preventing data misuse by the governments, criminals or terrorist bodies." |
| O23 | 602 | "This section aims to cover the open research topics and the future trends of satellite communication systems, while highlighting the challenges to be addressed." |

### 2.2 涉及"负载过程/突发/时延/到达率/信用分配/决策成本"的表述（逐字 + 行号）

| 行号 | 逐字原文 | 归类 |
|---|---|---|
| 443 | "In situations where the traffic is bursty, fixed assignment mechanisms lead to an inefficient use of the resources. Random access (RA) protocols are an interesting alternative." | **突发流量**与固定分配的不匹配（逐字含 bursty） |
| 484 | "It is shown in [216] and [217] that the traditionally used demand assignment multiple access (DAMA) protocol for the satellite return link does not perform well under sporadic IoT traffic with low duty-cycles and very short packet length." | **稀疏/低占空比**到达过程（sporadic, duty-cycle） |
| 484 | "Despite being a simple protocol and performing well at very modest traffic, the increased propagation delay in the satellite channel creates potential network stability issues, making it an unattractive solution for modern IoT satellite applications" | 传播时延 → 稳定性问题 |
| 428 | "• Demand satisfaction: We do not need to schedule a user which has an empty queue. We need to schedule users which have large pending data volumes first. But this depends on the Service-Level Agreement (SLA) each user has signed with the satellite operator. An SLA may define a minimum rate over time, a maximum rate over time, an average rate over time, latency, etc." | 队列/待发数据量 + 速率 SLA（到达率约束的合同化表述） |
| 350 | "• frequent trade-offs between performance, latency and complexity for the selection of signal processing and synchronization algorithms. In this context, the high complexity may also lead to processing delays, which negatively affects the performance of the algorithms;" | **算法复杂度 → 处理时延 → 性能** 的显式链条 |
| 645 | "dynamically match the geographic distribution of the traffic demand by following its variations in time" | 负载的时空变化 |
| 657 | "a realistic integrated NGSO satellite-terrestrial network is highly dynamic, resulting in fast variations of the virtual network topology over time" | 拓扑时间变化速率 |
| 418 | "• Packet priority: Lower priority packets can be delayed (or even dropped) in favor of high priority packets. For instance, emergency real-time packets, including emergency medical communications, rescue and natural disaster management related services," | 时延/丢弃作为调度手段 |
| 457 | "The beam hopping procedure, on one hand, allows higher frequency reuse schemes by placing inactive beams as barriers for the co–channel interference, and, on the other hand, allows for the use of a reduced number of on–board power amplifiers at each ti" | 时变需求下的波束调度 |
| 23 | "In this direction, there has recently been a tremendous interest in developing large Low Earth Orbit (LEO) constellations that can deliver high-throughput broadband services with low latency." | 时延作为星座驱动力 |

**信用分配（credit assignment）**：本篇未见。检索词 `credit`（不区分大小写，范围＝整篇 1398 行），命中仅 621 行 "Credits: NASA"（图片署名），无 RL 信用分配含义。

### 2.3 它提到但本库其他论文未跟进的方向

1. **卫星蜂群（satellite swarms）的星间链路与节点同步**：606–610。本库（111 篇题录）无蜂群/编队飞行论文。
2. **垂直空天网络（HAPS/UAV/卫星多层）的路由协议与轨迹联合设计**：614。本库 T1/T2 的路由论文全部限于 LEO/MEO/GEO 星座，无 HAPS/UAV 垂直层路由。
3. **行星际/深空 DTN（Bundle Protocol）的网络建模、路由与拥塞控制**：625。本库无 DTN 论文（TIER-ASSIGNMENT.md:74 的 K93SCUF2 题录未标 DTN；如需可核验其题录短名）。
4. **把 LEO 卫星做成"飞行基站"（on-board gNB、类 CoMP 多星同服）+ 功率预算分析**：631。本库无对应论文。
5. **量子密钥分发（QKD）光学星地链路**：663。本库 L5F3DK68 为安全综述（见第 9 节），但无 QKD 专门研究论文。
6. **数字孪生（Digital Twin）用于卫星系统**：677–685。本库无对应论文。
7. **面向卫星的 Open-RAN / 网络切片自动化（自组织、自优化）**：649、653–657。本库无对应论文。
8. **GSO-NGSO 实时动态干扰规避（认知波束跳变、自适应功率控制）**：639。本库无对应论文。
9. **SDR/软件定义载荷的资源编排**：643–647。本库无对应论文。

---

## 3. 7AXASN73 — A Survey on Nongeostationary Satellite Systems: The Communication Perspective

- 本地定位：TIER-ASSIGNMENT.md:104，"综述：只取共识与开放问题，不承重"
- 读取范围：MD 总 1030 行；本次通读第 9–14 行（I. INTRODUCTION）、48–74 行（C. Scope and Contributions / D. Structure）、227–251 行（III-B Networking Aspects）、293–356 行（IV. NGSO DEPLOYMENT CHALLENGES 全节：A. Regulatory and Coexistence Issues、B. Satellite Constellation Design、C. User Equipment、D. Operational Issues）、357–406 行（V. FUTURE RESEARCH DIRECTIONS AND OPPORTUNITIES 全节：A. Open RAN … G. Aerial Platforms and NGSO Coordination）

### 3.1 该综述认定的开放问题清单（逐字 + 行号）

| # | 行号 | 逐字原文 |
|---|---|---|
| O1 | 308 | "At this point, some aspects and scenarios need further investigations in this direction, which are enumerated and briefly described in the following." |
| O2 | 325 | "It is clear that the efficient use of spectrum is one of the most crucial challenges to be met by international satellite community in order to mitigate the GSO-NGSO interference." |
| O3 | 304 | "Although NGSO systems have potentials of global coverage and high performance, many of their regulatory rules were coined nearly two decades ago based on the proposed technical characteristics of NGSO satellites at the time. This is very challenging from a spectral coexistence viewpoint, and it will require much more agile systems." |
| O4 | 304 | "Moreover, the deployment of NGSO satellites is undergoing a significant densification comparing to existing GSO systems, which is leading to unprecedented inter-satellite coexistence challenges." |
| O5 | 319 | "In view of the constellation and orbital overcrowding, it is very likely that large NGSO constellations will cause interference to other NGSO systems." |
| O6 | 329 | "However, these design approaches do not take into consideration the demand characteristics on Earth, which makes them inefficient strategies when bearing in mind the non-uniform and uncertain demand over the globe." |
| O7 | 331 | "Nonetheless, the optimization of adapting the constellation to growing demand areas is a challenging issue to be addressed in the context of integration an entire hybrid model." |
| O8 | 331 | "Moreover, an integrated framework that accounts for the spatial-temporal traffic distributions and optimizes the expected life cycle cost over multiple potential scenarios can be an initial plan to circumvent the NGSO constellation design challenges" |
| O9 | 333 | "However, designing an optimal regional constellation is a complicated process, which requires optimizing the orbital characteristics (e.g., altitude, inclination) while considering asymmetric constellation patterns, particularly for complex time-varying and spatially-varying coverage requirements. This topic has not been deeply investigated in the literature, and thus, new sophisticated approaches to design optimal constellation patterns are needed to be developed and tailored to different orbital characteristics and NGSO environments." |
| O10 | 337 | "The closer a satellite is placed, the faster its movement is perceived from the user terminals on Earth, which imposes additional challenges to the user terminal equipment because it has to be able to track the satellite movement and perform handover from one satellite to another [255]." |
| O11 | 341 | "User mobility is another challenge to be addressed using inexpensive antennas." |
| O12 | 343 | "This also requires 5G functionalities to take into account the issues of long propagation delays, large Doppler shifts, and moving cells in NTN, and to improve timing and frequency synchronization." |
| O13 | 347 | "Other NGSO operational challenges/concerns are raised by the astronomy community as some rough estimates suggest there could be more than 50,000 satellites in total added to Earth orbits in the near future, which will make our planet blanketed with satellites." |
| O14 | 349 | "Light pollution: The proliferation of LEO satellites at altitudes less than 2,000 km will jeopardize the ability to observe, discover and analyze the cosmos from the Earth’s surface." |
| O15 | 351 | "Space debris: Since the commercialization of NGSO satellites enters the realm of technical feasibility, many orbital debris concerns have been raised due to the long-term impact that results from placing thousands of satellites in orbits and the risk of causing satellite collisions." |
| O16 | 241 | "Thereby, an efficient SDN-based architecture for multi-layer SINs requires more developments to achieve a flexible framework capable of facing the dynamicity of the nodes and the heterogeneity of the traffic." |
| O17 | 245 | "In other words, network slicing is still at an early stage of its application into 5G systems and requires novel algorithms and solutions to involve the NGSO systems." |
| O18 | 245 | "assigning dedicated spectrum resources to individual slices can diminish the multiplexing gains due the scarcity of radio spectrum" |
| O19 | 245 | "Network slicing works efficiently when more information can be provided by the infrastructure about the shared parts to the network slice but exposing such information creates new potential security vulnerabilities between infrastructure providers and their partners." |
| O20 | 369 | "In this context, there are various challenges, since the compatibility of such diverse hardware may require a careful system design. In particular, the availability of data and the way how it is processed in different satellites needs to be taken into account." |
| O21 | 369 | "These use cases need to be analyzed in order to determine the price that needs to be paid for the enhanced flexibility of ORAN." |
| O22 | 377 | "However, the expected connectivity improvement will be achieved at the cost of higher complexity that is essential for load balancing between satellite links and for finding paths with the shortest end-to-end propagation delay, as well as tackling the dynamicity of the nodes (e.g., high relative speeds, frequent handovers), which are yet unexplored areas in the literature." |
| O23 | 381 | "While this application seems very promising, its practical limitations and requirements are not yet fully understood as it has started to attract the attention of researchers only in the last few years." |
| O24 | 387 | "Hence, this infrastructure imposes a significant challenge on developing scheduling algorithms for energy-efficient downloading files from the space-based data centers to meet dynamic demands of users under time-varying channel conditions." |
| O25 | 387 | "Besides, the existing operational algorithms for task scheduling in terrestrial cloud data centers are not applicable to the space-based cloud infrastructures" |
| O26 | 393 | "Nevertheless, the progress is still in an early stage and more research efforts are required for a seamless integration, particularly in connecting NGSO satellites to mobile or stationary IoT devices and supporting ultra reliable low latency communications." |
| O27 | 397 | "However, the time-varying network topology and limited on-board resources in NGSO satellites have to be taken into account when designing caching placement algorithms alongside with their fast convergence and low complexity." |
| O28 | 403 | "Such networks pose many challenges for the coordination, navigation and synchronization." |
| O29 | 403 | "Another challenge is the topology control and multi-hop signal routing for such dynamic networks." |
| O30 | 250 | "However, some prospects in this evolving part are still rather overlooked and require more research efforts for integrating NGSO satellites with the global communication infrastructure." |
| O31 | 365 | "On the other hand, the persistent growth of the traffic demand and number of services with varying requirements, demand timely updates of the network configuration." |
| O32 | 373 | "Therefore, one of the key challenges for future space missions is providing a realtime uninterrupted connectivity, which is fairly infeasible in current satellite system infrastructure due to the magnitude and cost of the needed gateway network on ground." |

### 3.2 涉及"负载过程/突发/时延/到达率/信用分配/决策成本"的表述（逐字 + 行号）

| 行号 | 逐字原文 | 归类 |
|---|---|---|
| 235 | "In this configuration, several challenges imposed at the satellite network level related to dense satellite distribution, transmission delays, QoS priorities, uneven distribution of data flows, and the dynamic change of the network’s topological structure." | 流量分布不均 + 传输时延 + 拓扑动态 |
| 235 | "Designing efficient in-space backhauling protocols starts from evaluating the infrastructure parameters such as topology variation, bandwidth, link delay, in addition to traffic generation profiles of the heterogeneous user services/classes and computational and storage capabilities of the nodes." | **traffic generation profiles**（负载生成过程的显式登记） |
| 231 | "However, the expected better performance of space-based networks will be achieved at the cost of higher complexity that is essential for load balancing between satellite links and for finding paths with the shortest end-to-end propagation delay." | 负载均衡 vs 时延最短路径的代价 |
| 329 | "which makes them inefficient strategies when bearing in mind the non-uniform and uncertain demand over the globe" | 需求非均匀 + 不确定 |
| 331 | "On the other hand, a hybrid constellation design is proposed in [251] to utilize multiple layers and mixed circular-elliptical orbits, and thus, accommodating the asymmetry and heterogeneity of the traffic demand." | 流量需求的非对称/异构 |
| 331 | "an integrated framework that accounts for the spatial-temporal traffic distributions and optimizes the expected life cycle cost over multiple potential scenarios" | 负载的时空分布作为设计输入 |
| 333 | "particularly for complex time-varying and spatially-varying coverage requirements" | 时变+空变需求 |
| 365 | "the persistent growth of the traffic demand and number of services with varying requirements, demand timely updates of the network configuration" | 需求增长 → 配置更新时效 |
| 377 | "the expected connectivity improvement will be achieved at the cost of higher complexity that is essential for load balancing between satellite links and for finding paths with the shortest end-to-end propagation delay, as well as tackling the dynamicity of the nodes (e.g., high relative speeds, frequent handovers)" | 负载均衡 + 时延 + 节点动态 |
| 397 | "the time-varying network topology and limited on-board resources in NGSO satellites have to be taken into account when designing caching placement algorithms alongside with their fast convergence and low complexity" | **算法收敛速度与复杂度**作为设计约束（决策成本的一种表述） |
| 387 | "developing scheduling algorithms for energy-efficient downloading files from the space-based data centers to meet dynamic demands of users under time-varying channel conditions" | 动态需求 + 时变信道 |
| 343 | "This also requires 5G functionalities to take into account the issues of long propagation delays, large Doppler shifts, and moving cells in NTN" | 传播时延登记 |
| 304 | "the deployment of NGSO satellites is undergoing a significant densification comparing to existing GSO systems" | 密度提升（负载侧压力） |
| 220 | "In this context and motivating by the fact that a user terminal can see multiple NGSO satellites at the same time, there is an opportunity to combine the signals from multiple satellites for improving the aggregated data rate, beam load" | 多星同时可见 → 聚合速率/波束负载 |

**信用分配（credit assignment）**：本篇未见。检索词 `credit`（不区分大小写，范围＝整篇 1030 行），无任何命中行（唯一可能的形式为参考文献中的作者名，未出现在命中的正文行）。

### 3.3 它提到但本库其他论文未跟进的方向

1. **面向卫星的 Open RAN（功能拆分 + 厂商无关硬件）及其"灵活性代价"评估**：361–369。本库无对应论文。
2. **空基云（Space-Based Cloud / 空间数据中心）的任务调度与能量高效下载**：383–387。本库无对应论文。
3. **NGSO 缓存放置算法（收敛快、复杂度低）**：395–397。本库无缓存/内容分发论文。
4. **区域覆盖星座设计（在时变/空变覆盖需求下优化轨道参数）**：333。本库无星座设计论文（T2 均为路由）。
5. **天文学光污染与空间碎片减缓**：347–353。本库无对应论文。
6. **NGSO 地球站许可与监管框架**：315–317。本库无对应论文。
7. **EPFD 限值下的 GSO-NGSO 共存与缓解技术**：304–310。本库无对应论文。
8. **UAV/HAPS 与 NGSO 的协调（FSO/RF/混合链路、拓扑控制）**：399–403。本库无对应论文。
9. **多星联合信号合并以提升聚合速率/波束负载**：220。本库 T2 的多星协作路由（如 IXVSNEE3 星地协作）与之相近但非同一问题（需在 T2 档核对，不在本档结论范围）。
## 4. IP7RRM3A — From Connectivity to Advanced Internet Services: A Comprehensive Review of Small Satellites Communications and Networks

- 本地定位：TIER-ASSIGNMENT.md:105，"综述：只取共识与开放问题，不承重"
- 读取范围：MD 总 492 行；本次通读第 1–38 行（题录/摘要/1. Introduction）、200–262 行（6. Advances in Communications and Network Protocols 全节 + 7. Perspectives and Open Challenges 全节 + 8. Conclusions）。**未通读**：39–199 行（2. 小卫星演化史、3. 服务与应用、4. 载荷演化、5. 新电信架构），仅做关键词检索（见 4.2 末）。

### 4.1 该综述认定的开放问题清单（逐字 + 行号）

该节标题即 "(220) ## 7. Perspectives and Open Challenges"，其编号子节构成问题清单：

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
| 208 | "The central fact in both circumstances is the potential inability of each network node to request timely assistance from any other, for any purpose, and at any given moment." | **节点无法及时获得外部协助** → 本地决策 |
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

**信用分配（credit assignment）**：本篇未见。检索词 `credit`（不区分大小写，范围＝整篇 492 行），命中仅 150 行 "Figure 7: The MARCO communication architecture. Image credit: NASA/JPL-CalTech."（图片署名），无技术含义。

### 4.3 它提到但本库其他论文未跟进的方向

1. **DTN / Bundle Protocol / LTP 在小型卫星星座上的路由与拥塞控制语义**：208–212。本库 111 篇题录内无以 DTN 为主题的研究论文。
2. **网络编码（Network Coding，含随机线性网络编码）在星上/星间链路的可靠性提升**：214–218。本库无对应论文。
3. **可见光通信（VLC）作为星间链路**：204。本库无对应论文。
4. **智能分集（Smart Diversity）/站点分集与 SDN 网关重构**：228。本库无对应论文。
5. **星上 SDN 兼容路由器的实现**：254。本库无对应论文。
6. **CubeSat 的物理层安全（PLS）**：248。本库无对应论文。
7. **小卫星的量子密钥分发（QKD）**：250。本库无对应论文。
8. **应用层互操作协议（面向海量应用场景与流量数据形态）**：238。本库无对应论文。

---

## 5. QSNRQ8PF — Dynamic Routings in Satellite Networks: An Overview

- 本地定位：TIER-ASSIGNMENT.md:107，"综述：只取共识与开放问题，不承重"
- 读取范围：MD 总 707 行；本次通读第 1–30 行（题录/摘要）、107–132 行（3.3. Key Challenges for Satellite Network Routing + 3.4. Key Technologies 全节）、251–277 行（4.2.3. Traffic Balancing Dynamic Routings 全节 + 表 10/11/12）、279–320 行（5. Potential Technologies and Future Directions 全节 + 6. Conclusions）。**未通读**：31–106 行（引言/相关工作/系统模型/网络特性）、133–250 行（4.1 单层与 4.2.1–4.2.2 SDN/QoS 路由各节）。

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

### 5.2 涉及"负载过程/突发/时延/到达率/信用分配/决策成本"的表述（逐字 + 行号）

| 行号 | 逐字原文 | 归类 |
|---|---|---|
| 119 | "Unbalanced Load Traffic: Geographical conditions, satellite motion, and the Earth’s rotation characterize the time-varying nature and uneven distribution of load traffic in satellite networks." | **负载过程**：时变 + 不均匀（标题即负载） |
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
| 259 | "Such an approach allows network... However, since the time-varying network topology is not introduced into the network, the reliability of routing cannot be fully guaranteed when large-scale data transmission is performed in the LEO satellite network." / "In multi-layer satellite networks, owing to the non-equal distribution of users, LEO satellites are prone to massive network congestion when they pass through areas of high traffic." | 高流量区导致拥塞 |
| 259 | "Based on the prediction of traffic distribution, the work in [103] presented a parametric adaptive multi-attribute decision making (PASMAD) access and switching algorithm for GEO–LEO heterogeneous satellite networks." | 基于流量分布预测的决策 |
| 259 | "Furthermore, since the algorithm adopts real-time data collection to complete the routing operation, a corresponding load balancing mechanism is omitted." | 实时采集数据的代价 |
| 261 | "The method accurately detects queuing delays and dynamically adjusts routing paths according to queue changes. The solution can predict link conditions before congestion occurs on the link and reasonably select suitable routes based on various traffic situations in the link." | 队列变化驱动路由 |
| 261 | "Moreover, in a multi-layer satellite network, multiple satellite nodes need to transmit data simultaneously. However,the limitation of the storage resources of the satellite network can make the data among the nodes conflicting." | 并发传输 + 存储受限 |
| 261 | "Furthermore, Stackelberg traffic balance routing uses a threshold function to convert non-convex optimization into convex optimization." | 阈值函数（形式化，逐字抄录） |
| 263 | "Link overload traffic in densely populated areas can easily cause network delays and throughput crashes due to satellites’ geographical limitations." | 过载 → 时延/吞吐崩溃 |
| 265 | "Proper end-to-end (E2E) traffic prediction in multi-layer satellite networks plays a critical role in balancing traffic. The work in [108] presented an improved Markov model (HMM)- based method for E2E traffic prediction." | **E2E 流量预测（HMM）** |
| 265 | "Moreover, despite the large volatility of the actual service traffic in existing multi-layer satellite networks, the approach is still better at predicting and tracking the traffic on the links with low error." | **实际业务流量的大波动性**（本文对"突发"的最近似表述） |
| 265 | "The trained traffic scheduling model can make fast routing decisions for congested traffic detected over the link and maximize link utilization." | 快速决策（决策时延） |
| 265 | "The algorithm introduces a delay upper bound in heterogeneous links to optimize traffic allocation with the least delay." | 时延上界约束 |
| 277 | 表 12 表头："**Scheme | Time Delay | Packet Loss Rate | Calculation Overhead | Throughput**" | **Calculation Overhead 被列为路由方案的评价维度**（决策成本的制度性登记） |
| 287 | "The trained GNN model is able to achieve 98% accuracy within 15 iterations relative to shortest-path routing." | **收敛速度量化**（15 次迭代） |
| 294 | "So, the high computing agility and low latency can be achieved" | 边缘计算降低时延 |
| 300 | "the large amount of data generated by monitoring the solid satellite platform is used to improve the accuracy and predictability of information space models., significantly reducing the computational complexity of the dynamic routing strategies in multi-layer satellite networks." | 数字孪生降低路由决策复杂度 |
| 316 | "(2) Efficiency. Fast inference based on the input data can obtain the optimized routing decision in polynomial time" | **决策成本＝多项式时间推理** |
| 316 | "A larger topology means an exponentially growing number of network states and a greater difficulty in routing decisions." | 状态空间指数增长 |
| 308 | "MEC platforms allow edge networks to gain management access to computing and services to reduce mobile users’ network latency and bandwidth consumption." | 时延/带宽消耗 |

**信用分配（credit assignment）**：本篇未见。检索词 `credit`（不区分大小写，范围＝整篇 707 行），无任何命中行。

### 5.3 它提到但本库其他论文未跟进的方向

1. **数字孪生（Digital Twin）驱动的动态拓扑建模与路由预演**：298–302。本库 111 篇题录内无数字孪生论文。
2. **多尺度信息感知与复杂环境下的算力协同（MEC + 大数据分析驱动路由状态感知）**：308。本库无对应论文。
3. **智能卫星（可重定义需求/软件可重构/功能可重构的星上操作系统）**：312。本库无对应论文。
4. **智能路由设备（面向星上部署的专用硬件）**：316。本库无对应论文。
5. **动态网络切片在空间信息网络中的多维资源柔性调度**：131。本库无网络切片论文。
6. **星间太赫兹/激光高速传输与 IM/DD 检测方案比较**：123、129。本库无物理层传输论文。
7. **星上处理/星上交换/星上路由（OBP/OBS/OBR）硬件技术**：127。本库无对应论文。

---

## 6. T9X6QCLL — LEO SATELLITE NETWORKING RELAUNCHED: SURVEY AND CURRENT RESEARCH CHALLENGES

- 本地定位：TIER-ASSIGNMENT.md:108，"综述：只取共识与开放问题，不承重"
- 读取范围：MD 总 899 行；本次通读第 1–31 行（标题/摘要/1. INTRODUCTION）、159–188 行（4.3 Load balancing 全节）、271–284 行（4.8 Low latency networking 全节）、462–501 行（6. CHALLENGES AND FUTURE RESEARCH DIRECTIONS 全节 + 7. CONCLUSIONS）。**未通读**：32–158 行（2. Related work、3. 概览、4.1/4.2）、189–270 行（4.4 SDN、4.5 ML、4.6 DTN、4.7 地理路由、4.9 多层）、285–461 行（4.10/4.11 与 5. 标准化 3GPP/IETF）。
- **文本质量警示**：该 MD 存在 MinerU 连字替换伪影（`fi`→`ϐ`、`fi`→`ϔ`、`-`→`‑`），下列引文按 MD 原样逐字抄录，未做还原。

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

**信用分配（credit assignment）**：本篇未见。检索词 `credit`、`arrival rate`、`arrival process`、`Poisson`、`burst`、`self-similar`（均不区分大小写，范围＝整篇 899 行），**全部零命中**。

### 6.3 它提到但本库其他论文未跟进的方向

1. **面向"可预测长期基线 + 短期波动"的两尺度负载管理框架**：171。本库 T1/T2 路由论文均以瞬时负载/队列状态为输入，未见显式两尺度分解的设计（可在 T1/T2 档复核，本档只登记综述侧表述）。
2. **背压路由（Back-Pressure Routing）在卫星网络的应用**：177。本库 111 篇题录内无背压/队列稳定性理论路由论文。
3. **延迟抖动（delay variation）作为路径评价指标（DQ-GERT）**：281。本库 T1 论文的奖励/代价函数未见抖动项（本档仅登记，需 T1 档核验）。
4. **SDN 管理随时间演化的拓扑（Loon/Aalyria 路线）**：474。本库无 SDN 拓扑管理论文。
5. **空天地多层统一动态框架（SDN + ML 跨层）**：476。本库无跨层框架论文。
6. **星座间互操作与虚拟网络运营商（VNO）接口标准化**：484–492。本库无标准化/互操作论文。
7. **天文光污染与碎片协调**：490。本库无对应论文。

