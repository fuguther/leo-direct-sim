# DOSSIER-B10：T5 背景级综述 13 篇——开放问题清单 + 负载过程相关表述

> 批次：T5（背景级综述 13 篇），产出文件 DOSSIER-B10.md。作者：文献拆解员（子代理）。
> 依据：`round/run4/algo/TIER-ASSIGNMENT.md` 第 102–114 行将下列 13 篇定为 T5（"综述：只取共识与开放问题，不承重"）。
> 深度定义（TIER-ASSIGNMENT.md:129）："读摘要+开放问题/挑战节；产出该综述认定的开放问题清单含行号、与负载过程/信用分配相关的表述"。
> 全文来源：MinerU MD，VM 路径 `/data/liguang13/topic-loop-r2/md/<itemKey>/<itemKey>/txt/<itemKey>.md`（下文简称"该篇 MD"）。
> **所有引文均为该 MD 的行号 + 逐字英文原文**；本文件不含我的评价性改写。
> 红线遵守：负载/流量/评测设置只作条件登记，不作贡献。

## 0. 负向声明核验协议（本批统一执行）

主控核验协议更新后，本文件所有"未见/没有 X"的声明一律满足三件事：
1. **精确检索模式原文**（模式写在正文里，不用裸词）；
2. **实测计数**（`grep -ciE '<pattern>' <该篇 MD>` 返回的行数）；
3. **若有命中：命中行号 + 逐字片段 + 为何不构成反例**。

统一检索口径：范围＝该篇 MD 全文（行数已逐篇标注），区分大小写关闭（`-i`），ERE 模式（`-E`），逐行匹配。

## 0.1 本批 13 篇的统一负向核验表（模式 × 实测计数）

| itemKey | 总行数 | `credit` | `arrival rate` | `arrival process` | `Poisson` | `burst` | `self-similar` | `non-stationar` |
|---|---|---|---|---|---|---|---|---|
| 2QRYMWBI | 1933 | 0 | **1** | 0 | **2** | 0 | 0 | 0 |
| LNA28YZY | 1398 | **1** | 0 | 0 | 0 | **4** | 0 | 0 |
| 7AXASN73 | 1030 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| IP7RRM3A | 492 | **1** | 0 | 0 | 0 | **1** | 0 | 0 |
| LRSXMWX9 | 986 | 0 | 0 | 0 | 0 | **1** | 0 | **1** |
| QSNRQ8PF | 707 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| T9X6QCLL | 899 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Z74SR656 | 1293 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| L5F3DK68 | 835 | 0 | 0 | 0 | 0 | **2** | 0 | 0 |
| UMKF328H | 624 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| BV4XI6CU | 485 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 524XNF29 | 771 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 5AZHJE7N | 721 | 0 | **1** | 0 | **1** | 0 | 0 | 0 |

**13 篇合计**：`credit` 命中 2 篇（LNA28YZY、IP7RRM3A）；`arrival rate` 命中 3 篇（2QRYMWBI、5AZHJE7N）；`arrival process` **全 13 篇 0 命中**；`Poisson` 命中 2 篇（2QRYMWBI、5AZHJE7N）；`burst` 命中 4 篇（LNA28YZY、IP7RRM3A、LRSXMWX9、L5F3DK68）；`self-similar` **全 13 篇 0 命中**；`non-stationar` 命中 1 篇（LRSXMWX9）。
**每一处命中均已在对应篇目逐条列出并判定是否构成反例。**

---

## 1. 2QRYMWBI — Artificial Intelligence for Satellite Communication and Non-Terrestrial Networks: A Survey

- 本地定位：TIER-ASSIGNMENT.md:102，"综述：只取共识与开放问题，不承重"
- MD 总行数：1933
- 读取范围：第 1–20 行（标题/摘要）、542–604 行（星座路由、IoT 接入、流量/拥塞预测）、794–900 行（VI. CHALLENGES AND OPEN DISCUSSION 全节：A. Implementation Challenges、B. AI Accelerators、C. Future AI Frontiers/Visions、D. Security Aspects、E. Cost Optimization）

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
| O32 | 618 | "The works of [382], [384] consider only one learner in the network which can impose a huge computation load on the learning agent." |
| O33 | 618 | "However, authors in [382], [383] have not considered improving the learning convergence rate of the distributed caching by coordinating the cache through satellite connectivity. Furthermore, backhaul and user link capacities were not included in the optimization model." |

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
| 246 | "To cope with the time-varying and unpredictable wireless channel issues, and differentiated service arrival rates in the multi-beam satellite environment, this work employed the model-free multi-objective deep reinforcement learning approach to learn and retrieve the optimal policy through interactions with the situation." | **到达率（arrival rates）在业务间存在差异**（`arrival rate` 唯一命中）；本篇唯一的 multi-objective DRL 表述 |
| 246 | "To solve the problem with action dimensional disaster, a novel multi-action selection method based on Double-Loop Learning (DLL) is proposed." | 动作空间维灾的应对（决策成本） |
| 246 | "The agents can learn to collaborate by sharing the same reward to achieve the common goal, which refers to maximize the throughput and minimize the delay fairness between cells." | 多智能体**共享同一奖励**（与 G-A 直接相关，见第 14 节） |
| 566 | "Probabilities of transition between states are expressed analytically based on the Poisson process for both contentionbased and contention-free random access." | 到达过程＝Poisson（`Poisson` 命中 #1） |
| 618 | "The work of [385] considers a network of multiple BSs and cache-enabled SBSs where users are spatially distributed according to Poisson point process." | **空间** Poisson 点过程，不是到达过程（`Poisson` 命中 #2；不构成"到达率建模"反例） |
| 566 | "The authors consider the agent to be placed on the satellite and consider onboard training without, however, offering an overview of the demanded computational power to run the proposed Reinforcement Learning algorithm." | 决策/训练成本未被报告（作者批评前作） |
| 550 | "In [125], authors propose a DRL algorithm where the rational agent of the model learns following the replays and selects the route with the smallest Round Trip time. The routes chosen, although in principle crossing more nodes, and therefore longer, in the end, have better effectiveness and a lower load on the bottleneck router." | 时延（RTT）作为路由目标 + 瓶颈负载 |
| 548 | "First, a valuable routing algorithm should guarantee each application’s required QoS, e.g. latency, packet loss, and data rate." | 时延作为 QoS 约束 |
| 560 | "Successive improvements, such as in [353], have allowed new RA methods to achieve low `$( < 1 0 ^ { - 3 } )$` Packet Loss Probability (PLR) even at high (≥ 1) network loads, enabling applications in massive machine-type communications (mMTC)." | 负载水平与丢包率的定量关系（公式逐字抄录） |
| 422 | "While the terminal segment predictions require a time window similar to the propagation delay, the ground segment usually needs longer time windows for performing missionlevel operations such as gateway switching." | 预测时间窗 vs 传播时延（决策时标） |

### 1.3 负向声明核验（模式 / 实测计数 / 命中判定）

- **信用分配（credit assignment）未见**：模式 `credit` → **实测计数 0**，无任何命中行。**原文未出现 "credit" 一词，连图片署名也没有**（本文件前一版曾误报为"仅以 'Credits: NASA' 出现"，现已更正为 0）。
- **突发未见**：模式 `burst` → **实测计数 0**。
- **自相似/长程相关未见**：模式 `self-similar` → **实测计数 0**。
- **非平稳未见**：模式 `non-stationar` → **实测计数 0**。
- **"到达过程"一词未见**：模式 `arrival process` → **实测计数 0**；但 `Poisson` 有 **2 命中**（L566 到达过程 / L618 空间点过程），已在 1.2 逐条列出并判定。

### 1.4 它提到但本库其他论文未跟进的方向

判定基准：本库 111 篇题录见 TIER-ASSIGNMENT.md:9–119（T1 路由+学习 34 / T2 路由但非学习 32 / T3 测量平台 AoI 16 / T4 通用 RL 11 / T5 综述 13 / T6 领域外 5）。以下方向在本批 13 篇综述之外的题录中**未见对应论文**。

1. **星上 AI 硬件与容辐（radiation tolerance）**：830–834、816、838–842。本库无任何星上处理器/加速器/容辐硬件论文。
2. **类脑/神经形态处理器（Neuromorphic Computing）作为星上协处理器、流式处理**：844–846。本库无对应论文。
3. **联邦学习（Federated Learning）在卫星星座上的部署与其通信可靠性/异构设备问题**：850–856。本库 T1/T2 全部为单星或星座级 RL 路由，无联邦训练论文。
4. **ML + 区块链（Blockchain）用于 SATCOM 的可信流量卸载**：858。本库无对应论文。
5. **TinyML 在星上 MCU 的端侧训练/模型更新**：860–862。本库无对应论文。
6. **量子计算加速 AI 训练 / 空基量子云卸载算力**：864–874。本库无对应论文。
7. **AI 的可解释性/偏见/伦理在 SATCOM 数据链上的落地**：884。本库无对应论文。
8. **ML 部署的成本优化（每 Gbps 在轨成本、卫星重量-功耗-寿命权衡、规模化训练维护成本）**：894–898。本库无对应论文；本库所有 RL 路由论文均未把部署成本纳入评价。
9. **数据降维（feature extraction/selection）以降低决策时延**：824–828。本库 T1 路由论文的状态设计未见以"降维以加速决策"为目标的工作。
10. **多波束卫星内业务到达率差异下的多目标 DRL 波束跳变**：246。本库 T1/T2 无波束跳变资源分配论文。
11. **分布式缓存的"学习收敛速率"优化（以卫星连通性协调缓存）**：618。本库无缓存/收敛速率论文。

---

## 2. LNA28YZY — Satellite Communications in the New Space Era: A Survey and Future Challenges

- 本地定位：TIER-ASSIGNMENT.md:103，"综述：只取共识与开放问题，不承重"
- MD 总行数：1398
- 读取范围：第 1–18 行（标题/摘要/引言）、600–694 行（IX. FUTURE & OPEN TOPICS 全节：A. Cooperative Satellite Swarms … J. Digital Twins for Satellite Systems、X. CONCLUSION）

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

### 2.2 涉及"负载过程/突发/时延/到达率/信用分配/决策成本"的表述（逐字 + 行号）

| 行号 | 逐字原文 | 归类 |
|---|---|---|
| 414 | "the packet traffic in broadband services is bursty (i.e., the data rate needed to support the different services is not constant). Therefore, the goal of the forward link satellite scheduler is to optimize the bandwidth (capacity) utilization and QoS in the presence of traffic flows generated by services with different requirements." | **突发的操作性定义**（"所需数据率不是常数"）；调度器目标（`burst` 命中 #1） |
| 443 | "In situations where the traffic is bursty, fixed assignment mechanisms lead to an inefficient use of the resources. Random access (RA) protocols are an interesting alternative." | 突发与固定分配的不匹配（`burst` 命中 #3） |
| 441 | "MF-TDMA is a system of access control to a set of digitally modulated carriers whereby the RCSTs are capable of frequency hopping among those carriers for the purpose of transmitting short bursts of data within assigned time slots." | 短突发（`burst` 命中 #2）；TBTP 时隙分配 |
| 457 | "Beam hopping uncovers entirely new problems that were never considered before in satellite communications: the challenge of designing an illumination pattern able to perfectly match the demands [209], [210], the acquisition and synchronization of bursty transmitted data [211], and the exploitation of extra degrees of freedom provided by the fact that certain regions of the coverage area are inactive." | 突发数据的捕获与同步（`burst` 命中 #4） |
| 484 | "It is shown in [216] and [217] that the traditionally used demand assignment multiple access (DAMA) protocol for the satellite return link does not perform well under sporadic IoT traffic with low duty-cycles and very short packet length." | **稀疏/低占空比**到达过程（sporadic, duty-cycle） |
| 484 | "Despite being a simple protocol and performing well at very modest traffic, the increased propagation delay in the satellite channel creates potential network stability issues, making it an unattractive solution for modern IoT satellite applications" | 传播时延 → 稳定性问题 |
| 428 | "• Demand satisfaction: We do not need to schedule a user which has an empty queue. We need to schedule users which have large pending data volumes first. But this depends on the Service-Level Agreement (SLA) each user has signed with the satellite operator. An SLA may define a minimum rate over time, a maximum rate over time, an average rate over time, latency, etc." | 队列/待发数据量 + 速率 SLA（到达率约束的合同化表述） |
| 350 | "• frequent trade-offs between performance, latency and complexity for the selection of signal processing and synchronization algorithms. In this context, the high complexity may also lead to processing delays, which negatively affects the performance of the algorithms;" | **算法复杂度 → 处理时延 → 性能** 的显式链条 |
| 645 | "dynamically match the geographic distribution of the traffic demand by following its variations in time" | 负载的时空变化 |
| 657 | "a realistic integrated NGSO satellite-terrestrial network is highly dynamic, resulting in fast variations of the virtual network topology over time" | 拓扑时间变化速率 |
| 418 | "• Packet priority: Lower priority packets can be delayed (or even dropped) in favor of high priority packets. For instance, emergency real-time packets, including emergency medical communications, rescue and natural disaster management related services," | 时延/丢弃作为调度手段 |
| 23 | "In this direction, there has recently been a tremendous interest in developing large Low Earth Orbit (LEO) constellations that can deliver high-throughput broadband services with low latency." | 时延作为星座驱动力 |

### 2.3 负向声明核验（模式 / 实测计数 / 命中判定）

- **信用分配（credit assignment）未见**：模式 `credit` → **实测计数 1**。
  - **命中位置**：L621 "Fig. 22. Interplanetary Internet Network Concept. Credits: NASA"。
  - **为何不构成反例**：该处为图片版权署名，与该文任何技术论述无关；该文通篇无 RL 信用分配的讨论（该文 ML 一节 L665–673 只列 ML 用例，未展开信用分配）。
- **到达率未见**：模式 `arrival rate` → **实测计数 0**；`arrival process` → 0；`Poisson` → 0。
- **自相似/长程相关未见**：模式 `self-similar` → **实测计数 0**。
- **非平稳未见**：模式 `non-stationar` → **实测计数 0**。
- **突发有 4 命中**：模式 `burst` → **实测计数 4**（L414、L441、L443、L457），已全部在 2.2 逐条列出。

### 2.4 它提到但本库其他论文未跟进的方向

1. **卫星蜂群（satellite swarms）的星间链路与节点同步**：606–610。本库（111 篇题录）无蜂群/编队飞行论文。
2. **垂直空天网络（HAPS/UAV/卫星多层）的路由协议与轨迹联合设计**：614。本库 T1/T2 的路由论文全部限于 LEO/MEO/GEO 星座，无 HAPS/UAV 垂直层路由。
3. **行星际/深空 DTN（Bundle Protocol）的网络建模、路由与拥塞控制**：625。本库无以 DTN 为主题的研究论文。
4. **把 LEO 卫星做成"飞行基站"（on-board gNB、类 CoMP 多星同服）+ 功率预算分析**：631。本库无对应论文。
5. **量子密钥分发（QKD）光学星地链路**：663。本库 L5F3DK68 为安全综述（见第 9 节），但无 QKD 专门研究论文。
6. **数字孪生（Digital Twin）用于卫星系统**：677–685。本库无对应论文。
7. **面向卫星的 Open-RAN / 网络切片自动化（自组织、自优化）**：649、653–657。本库无对应论文。
8. **GSO-NGSO 实时动态干扰规避（认知波束跳变、自适应功率控制）**：639。本库无对应论文。
9. **SDR/软件定义载荷的资源编排**：643–647。本库无对应论文。
10. **突发业务的波束跳变照明图样匹配 + 突发数据捕获同步**：457。本库 T1/T2 无波束跳变论文。

---

## 3. 7AXASN73 — A Survey on Nongeostationary Satellite Systems: The Communication Perspective

- 本地定位：TIER-ASSIGNMENT.md:104，"综述：只取共识与开放问题，不承重"
- MD 总行数：1030
- 读取范围：第 9–14 行（I. INTRODUCTION）、48–74 行（C. Scope and Contributions / D. Structure）、227–251 行（III-B Networking Aspects）、293–356 行（IV. NGSO DEPLOYMENT CHALLENGES 全节）、357–406 行（V. FUTURE RESEARCH DIRECTIONS AND OPPORTUNITIES 全节）

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
| O33 | 241 | "Furthermore, it has been emphasised in [189] that there is a lack of SDN-based architecture solution specifically designed for small satellites, where all the prior works mainly focus on the traditional LEO, MEO and GSO satellites." |

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

### 3.3 负向声明核验（模式 / 实测计数 / 命中判定）

本篇是本批中**七项模式全部 0 命中**的篇目之一（另见表 0.1）：

- 模式 `credit` → **实测计数 0**（无任何命中行）。
- 模式 `arrival rate` → **实测计数 0**。
- 模式 `arrival process` → **实测计数 0**。
- 模式 `Poisson` → **实测计数 0**。
- 模式 `burst` → **实测计数 0**。
- 模式 `self-similar` → **实测计数 0**。
- 模式 `non-stationar` → **实测计数 0**。

### 3.4 它提到但本库其他论文未跟进的方向

1. **面向卫星的 Open RAN（功能拆分 + 厂商无关硬件）及其"灵活性代价"评估**：361–369。本库无对应论文。
2. **空基云（Space-Based Cloud / 空间数据中心）的任务调度与能量高效下载**：383–387。本库无对应论文。
3. **NGSO 缓存放置算法（收敛快、复杂度低）**：395–397。本库无缓存/内容分发论文。
4. **区域覆盖星座设计（在时变/空变覆盖需求下优化轨道参数）**：333。本库无星座设计论文（T2 均为路由）。
5. **天文学光污染与空间碎片减缓**：347–353。本库无对应论文。
6. **NGSO 地球站许可与监管框架**：315–317。本库无对应论文。
7. **EPFD 限值下的 GSO-NGSO 共存与缓解技术**：304–310。本库无对应论文。
8. **UAV/HAPS 与 NGSO 的协调（FSO/RF/混合链路、拓扑控制）**：399–403。本库无对应论文。
9. **多星联合信号合并以提升聚合速率/波束负载**：220。本库 T2 的多星协作路由（如 IXVSNEE3 星地协作）与之相近但非同一问题（需在 T2 档核对，不在本档结论范围）。
10. **面向小卫星的 SDN 架构（现有一律面向传统 LEO/MEO/GSO）**：241。本库无对应论文。

<!--APPEND-->
