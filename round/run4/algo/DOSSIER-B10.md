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

---

## 4. IP7RRM3A — From Connectivity to Advanced Internet Services: A Comprehensive Review of Small Satellites Communications and Networks

- 本地定位：TIER-ASSIGNMENT.md:105，"综述：只取共识与开放问题，不承重"
- MD 总行数：492
- 读取范围：第 1–38 行（题录/摘要/1. Introduction）、200–262 行（6. Advances in Communications and Network Protocols 全节 + 7. Perspectives and Open Challenges 全节 + 8. Conclusions）。
- **未通读（如实声明）**：39–199 行（2. 小卫星演化史、3. 服务与应用、4. 载荷演化、5. 新电信架构）。该区间仅做关键词检索（见 4.3），未逐段阅读，故其开放问题**可能有遗漏**。

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
  - **为何不构成反例**：该命中位于**参考文献条目标题**中，不是本文的论述；本文正文对突发/到达过程无任何建模或讨论。故"该文正文未涉及突发过程建模"的判断成立。

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
| 277 | 表 12 表头逐字："Scheme / Time Delay / Packet Loss Rate / Calculation Overhead / Throughput" | **Calculation Overhead 被列为路由方案的评价维度**（决策成本的制度性登记） |
| 287 | "The trained GNN model is able to achieve 98% accuracy within 15 iterations relative to shortest-path routing." | **收敛速度量化**（15 次迭代） |
| 294 | "So, the high computing agility and low latency can be achieved" | 边缘计算降低时延 |
| 300 | "the large amount of data generated by monitoring the solid satellite platform is used to improve the accuracy and predictability of information space models., significantly reducing the computational complexity of the dynamic routing strategies in multi-layer satellite networks." | 数字孪生降低路由决策复杂度 |
| 316 | "(2) Efficiency. Fast inference based on the input data can obtain the optimized routing decision in polynomial time" | **决策成本＝多项式时间推理** |
| 316 | "A larger topology means an exponentially growing number of network states and a greater difficulty in routing decisions." | 状态空间指数增长 |
| 308 | "MEC platforms allow edge networks to gain management access to computing and services to reduce mobile users’ network latency and bandwidth consumption." | 时延/带宽消耗 |

### 5.3 负向声明核验（模式 / 实测计数 / 命中判定）

- 模式 `credit` → **实测计数 0**。已用精确整词模式核验（非裸词），全文无 "credit" 出现；本篇正文出现的 cost 类词汇是 "routing cost"、"minimize path costs"、"computational overhead"，与此无关。
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
- 模式 `burst` → **实测计数 0**。注意：本篇 L171 用 "variable short‑term ϐluctuations"，L173 用 "cascading congestion"，但**均未使用 burst 一词**（已用精确模式 `burst` 核验为 0）。
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

---

## 7. LRSXMWX9 — A Survey on Technologies, Standards and Open Challenges in Satellite IoT

- 本地定位：TIER-ASSIGNMENT.md:106，"综述：只取共识与开放问题，不承重"
- MD 总行数：986
- 读取范围：第 1–10 行（题录/摘要）、434–593 行（VI. OPEN CHALLENGES AND FUTURE DIRECTIONS 全节：A. Innovative Approaches to Tackle Technical Challenges、B. Future Standardization and Regulation、C. Business Development Opportunities + VII. CONCLUSION）。
- **未通读（如实声明）**：11–433 行（1. 引言、2. 长距 IoT 分类、3. 卫星 IoT 新范式、4. 卫星 IoT 使能技术、5. 工业界实践）。

### 7.1 该综述认定的开放问题清单（逐字 + 行号）

| # | 行号 | 逐字原文 |
|---|---|---|
| O1 | 436 | "In this section, we focus on the analysis of the gaps that remain both from the technological point of view and standardization/regulation point of view, starting from the remarks provided in Section IV-C, in order to fully unleash the potential of satellite IoT." |
| O2 | 452 | "The antenna design is a challenging aspect. Clearly, the utilized frequency band and the form factor of the satellite constitute contrasting objectives for the size of the antenna. On the one hand, the lower spectrum requires larger antennas and higher spectrum requires more power and directivity [32]. On the other hand, the antenna has to fit a form factor given by the satellite." |
| O3 | 462 | "On the other hand, we observe that an effective downlink communication (from satellites towards MTDs) may be hard to achieve as well, because of synchronization and interference issues between the transmitter and the receiver." |
| O4 | 462 | "For example, in NB-IoT bidirectional communication is needed for RRM purposes, but the delay introduced by the satellite links will possibly require to modify time advance mechanisms." |
| O5 | 468 | "5) Network and Higher-Layer Protocols: A relevant technological challenge is represented by the need for IoT-oriented protocol stacks capable of going beyond TCP/IP limitations." |
| O6 | 470 | "The direct use of unmodified mainstream protocols, such as HTTP/1 and TCP, is challenging in resource limited IoT devices (e.g., CPU, memory, power) and constrained networks (e.g., high-latency, low-power, lossy). As mentioned earlier in the paper, the CoAP can be used in LPWANs for IoT services. However, the protocol is still open to the implementation of a Go-Back-N ARQ to make more efficient use of the available resources and reduce the delivery delay in high-latency networks such as satellite;" |
| O7 | 482 | "Specific interest and related open challenges are related to the emerging concept of network slicing." |
| O8 | 487 | "However, while functionalities and interfaces are being standardized, e.g., by the 3GPP, the relevant open challenge is related to understanding the specific QoS requirements of long range IoT services and to define how to configure and provision a proper mMTC slice. Those represent open challenges in this area and promising research topics for the future." |
| O9 | 496 | "Traditional satellites are designed and optimized for specific applications, and therefore are highly customized. Embracing the MEC paradigm presupposes therefore a paradigm shift. For the MEC framework being adapted to satellites we have to rethink the role both the satellite node and the ground station, taking into account the limited on-board resources and communications specific characteristics, specially when it comes to small satellites." |
| O10 | 536 | "2) Spectrum Harmonization: A prominent technical challenge to enable a worldwide support of satellite IoT system is related to spectrum. If fact, a device, without knowing its position, should be able to adapt its transceiver to the correct regional regulations (e.g., switching from CEPT to FCC)." |
| O11 | 548 | "As a conclusion, the issue of the frequency allocation for small satellites like Cubesat is still open. The 148–149.9 MHz uplink band implies that the antennas for the MTDs would have a dimension too big for the IoT devices." |
| O12 | 550 | "Let us remark that the CEPT scope is the free market circulation of equipment into the countries that are members of CEPT. The big issue, however, is that non-geostationary satellites (like the CubeSat) fly all over the globe so achieving the “approval” from CEPT is a necessary step but not sufficient. The big step for companies that want to operate a CubeSat network is to achieve the approval from ITU." |
| O13 | 554 | "The whole procedure of authorization takes a minimum of 9 months and a maximum of 7 years, depending on the accuracy of submitted information, on the reactions (e.g., from national regulators) on the pre-publication of the information about the new satellite networks, and so on." |
| O14 | 570 | "All of these issues highlight the importance of spectrum coordination and allocation aspects, which are often neglected in the scientific literature. The need for a streamlined procedure to put in operation CubeSat (or, more in general, LEO small satellites) is evident, to support the market growth of this type of networks. The establishment of this new streamlined procedure, however, is not at all simple to achieve" |
| O15 | 588 | "Moreover, in order to reduce the complexity of a satellite back-hauling based on ISLs, and thus its deployment cost which would curb the adoption of such paradigm, appropriate satellite trajectories and constellations should be designed to ensure line of sight between IoTsupporting satellites and the ground station network." |
| O16 | 588 | "Finally, there is the option of eventually providing an incomplete coverage on the Earth, rather concentrating it on localized areas on Earth according to the specific IoT use case [33], thus reducing the deployment costs." |

### 7.2 涉及"负载过程/突发/时延/到达率/信用分配/决策成本"的表述（逐字 + 行号）

| 行号 | 逐字原文 | 归类 |
|---|---|---|
| 460 | "For example, [88] proposes a distributed method to tune the transmission probability of each MTD according to current traffic load at the serving satellite." | **按当前负载调节发送概率**（接入层的负载反馈） |
| 442 | "the authors of [77] proposed a folded chirp-rate shift keying modulation, characterized by high resilience to Doppler and other unexpected frequency drifts" | 应对非预期频漂（链路过程扰动） |
| 470 | "constrained networks (e.g., high-latency, low-power, lossy)" | 时延/丢包作为受限网络特征 |
| 470 | "to make more efficient use of the available resources and reduce the delivery delay in high-latency networks such as satellite" | **投递时延**的协议层优化 |
| 472 | "This transition could lead to the standardization of an HTTP/3 supported by QUIC, with the advantage that QUIC provides reliable data transfer and pluggable congestion control, which can be optimized for IoT scenarios." | 可插拔拥塞控制 |
| 474 | "SCHC prevents synchronization between elements communicating on the network, and this is one of the operations that consumes most bandwidth. This can be achieved since in LPWANs networks, the nature of data flows is highly predictable." | **LPWAN 数据流的"高度可预测"性质** |
| 478 | "Numerical simulations of [100] show a 50-65% delay reduction for RLNC with respect to the state-of-the-art Reliable Datagram Protocol (RDP), used for comparison in all the considered scenarios." | 时延降低量化（50–65%） |
| 464 | "It is finally worth mentioning that some recent (at the time of writing) studies appeared in literature have been characterizing the medium access across satellite clusters communicating via ISLs. These studies have been addressing the connection establishment [92], the information aging against the number of hops [93], and the average delay [94]." | **信息时效（information aging）随跳数变化** + 平均时延（与本库 T3 AoI 主题呼应） |
| 462 | "Another possible solution could be based on grouping of MTDs according to their location, channel characteristics, and traffic features to alleviate the signaling overhead, as envisioned in [16, Sec. V]." | 按流量特征分组以降信令开销（决策/控制开销） |
| 520 | "As far as radio-communications are concerned, the International Telecommunication Union (ITU) represents the framework for the international regulation of spectrum utilization [106]." | 频谱治理（非算法） |
| 452 | "the antenna has to fit a form factor given by the satellite" | 物理约束（非算法） |

### 7.3 负向声明核验（模式 / 实测计数 / 命中判定）

- 模式 `credit` → **实测计数 0**。
- 模式 `arrival rate` → **实测计数 0**；`arrival process` → **实测计数 0**；`Poisson` → **实测计数 0**。
- 模式 `self-similar` → **实测计数 0**。
- 模式 `burst` → **实测计数 1**。
  - **命中位置与逐字**：L232 "Burst Data, and ii) a cloud-based solution th..."（原文为星座/系统条目描述的一部分）。
  - **为何不构成反例**：该命中是某一商业系统的**名称/功能短语**（"Burst Data"），不是对突发到达过程的建模或讨论。本篇全文无突然到达过程的量化建模。
- 模式 `non-stationar` → **实测计数 1**。
  - **命中位置与逐字**：L430 "working through the Doppler and range issues unique to non-stationary satellites (NB-IoT in LEO satellites is challenging, due to high Doppler and d..."。
  - **为何不构成反例**：此处的 "non-stationary" 修饰的是**卫星平台的运动性**（多普勒与距离变化），**不是"非平稳到达过程/非平稳流量"**。故此篇在"负载过程的非平稳性建模"上仍属未见。

### 7.4 它提到但本库其他论文未跟进的方向

1. **卫星簇内 ISL 上的介质访问（连接建立、信息时效随跳数、平均时延）**：464。本库 T3 有 AoI 主题论文（4QG5VYHQ、BLFJ6CLV、GV9PPNZT、R5QTFKD2），但**卫星簇内 ISL 多跳 AoI** 与路由耦合的方向未见。
2. **LPWAN 场景的 SCHC 头压缩以消除同步开销**：474。本库无对应论文。
3. **面向 IoT 的 HTTP/3 over QUIC 与可插拔拥塞控制在卫星链路的适配**：472。本库无传输层拥塞控制论文。
4. **随机交织复用（random interleaving multiplexing）与星座编码/解码的多址**：446。本库无对应论文。
5. **LoRa-E 跳频扩频（FHSS）上行多址**：442。本库无对应论文。
6. **按位置/信道/流量特征对 MTD 分组以降低信令开销**：462。本库无对应论文。
7. **ITU 授权流程与频谱协调（9 个月–7 年）对系统设计的约束**：554、570。本库无对应论文。
8. **降低星间回传复杂度的轨迹/星座设计（保证星地 LoS）**：588。本库无对应论文。

---

## 8. Z74SR656 — Evolution of Non-Terrestrial Networks From 5G to 6G: A Survey

- 本地定位：TIER-ASSIGNMENT.md:109，"综述：只取共识与开放问题，不承重"
- MD 总行数：1293
- 读取范围：第 1–8 行（题录/摘要）、434–513 行（IX. NTNS INTEGRATION IN 6G 全节：A. Prospective Use Cases、B. Architectures、C. Technological Enablers、D. Higher Layer Aspects + Key Takeaways）。
- **未通读（如实声明）**：9–433 行（I. 引言、II. 5G 集成、III. mmWave、IV. IoT、V. MEC、VI. ML 赋能 NTN、VII. 高层进展、VIII. 现场试验）。第 434–513 行之外的内容未逐段阅读，故其开放问题**可能有遗漏**（尤其 VI. ML-Empowered NTNs 一节，与本题最相关，本次未通读——**这是本批的一处明确缺口**）。

### 8.1 该综述认定的开放问题清单（逐字 + 行号）

| # | 行号 | 逐字原文 |
|---|---|---|
| O1 | 461 | "Based on the above discussion, it becomes obvious that integrated GAS networks could greatly benefit from the ORAN movement. However, the adoption of the terrestrial ORAN designs, components, interfaces and controllers would not be straightforward due to the particularities of the GAS networks." |
| O2 | 461 | "The first and foremost challenge is the new control/communication interfaces needed to interconnect the RAN which is part of the network control center (NCC) with the air-space control center (SCC), which is responsible for the orchestration of the UAV and/or satellite assets. From an algorithmic point of view, this motivates new ORAN intelligent controllers which would be responsible for the communication control co-design." |
| O3 | 463 | "In this context, there is a wealth of challenges to be addressed. Firstly, lowmass low-power antennas would be needed so that nanosats can effectively communicate directly with the large LEO space Internet providers." |
| O4 | 463 | "In parallel, radio access for the LEO space Internet satellites would have to be redesigned taking into account all possible terminals located on ground, air, or space and their heterogeneous requirements in terms of link budgets and relative speeds." |
| O5 | 463 | "In parallel, the intra- and inter-layer backhauling network will have to be densified to allow uninterrupted connectivity." |
| O6 | 463 | "As always, the development of low-mass low-power transceivers is a crucial challenge given the energy limitations of UAVs and the launch mass limitations of satellites." |
| O7 | 467 | "Nevertheless, there are yet several challenges to be addressed. The presence of thousands LEO satellites cause significant adjacent satellite interference (ASI) where other orbital constellations generate signal interference [358]." |
| O8 | 467 | "Thus, an extremely careful network management is required to avoid interference coming from different layers and orbital constellations under various propagation delay characteristics." |
| O9 | 467 | "In addition, debris is an important issue while deploying large LEO constellation which makes the near space activities difficult." |
| O10 | 473 | "In this context, one of the great challenges in the 6G GAS vision is to develop efficient and resilient algorithms for the codesign of communication and control parameters. These algorithms should ideally be deployed in a distributed and autonomous fashion to avoid single points of failure." |
| O11 | 475 | "For joint communication and sensing, bandwidth is however much desirable and waveform design for joint communication and sensing is still an open issue." |
| O12 | 477 | "Nevertheless, there are many challenges associated with the aerial deployment of IRSs [369]. The main challenge would be to incorporate IRSs in antennas attached to flying assets, where the main objectives are low-mass, lowpower, and large range flexibility. Another challenge would be to implement effective controllers for the surface configuration given that the channel might be changing aggressively, while the propagation distance/delay between the flying BS and the surface would be considerable." |
| O13 | 485 | "Despite its advantages, the THz communication is still in its nascent stage and dedicated research efforts are required to make this technology a reality in practice. For instance, the channel modelling for THz propagation is yet to be fully understood." |
| O14 | 487 | "In the presence of 3D multi-segments and mega LEO constellations, 6G networks become super heterogeneous even in vertical dimension, where a ground terminal may have access to several communication segments and may operate in multi-frequencies for various purposes. While this appears as an opportunity from an end-user perspective, the network management becomes a more complex task. Therefore, AIbased algorithms can assist to provide solutions with reduced response time and operating costs." |
| O15 | 487 | "In particular, an E2E learning-based corrective actions are required to provide a harmonized integration of air/space networks into 6G ecosystem [285]." |
| O16 | 493 | "Nevertheless, there are some underlying challenges for realizing the quantum communication in space. For instance, quantum signals through free space are traversed by various noise sources such as atmospheric turbulence, background noise from stray light, diffraction, etc. In addition, the development of quantum technologies is necessary that can endure and withstand the harsh space weather." |
| O17 | 497 | "The upcoming 6G networks will accommodate an extensive range of different technologies, thus posing some challenges on the management of such heterogeneous networks in higher layers [27], [382]." |
| O18 | 506 | "For NTN, the implementation of the virtualization feature must address at least two major challenges; (1) Highly dynamic networks. These networks requires the dynamic VNs implementations schemes in order to adapt efficiently the VNs configurations according to the changing network conditions, and; (2) Network “awareness”. In the context of network slicing implementations, the development of increasingly efficient advanced Virtual Network Embedding algorithms (e.g., AI-based), requires real-time and detailed network state information." |
| O19 | 508 | "This opens the opportunity of developing new architectures, protocols, and APIs in order to fully integrate the NTN elements for a global network orchestration schemes in the context of network slicing implementations." |
| O20 | 510 | "However, 6G will require not only the decentralized computing and storage concept, but a highly decentralized network architecture where each node is equipped with sufficient intelligence and self-reconfiguration capabilities. For instance, each node is expected to intelligently route the data packets to the suitable network slice according to its requirements. The latter is only possible if each node is aware of the network status." |

### 8.2 涉及"负载过程/突发/时延/到达率/信用分配/决策成本"的表述（逐字 + 行号）

| 行号 | 逐字原文 | 归类 |
|---|---|---|
| 506 | "the development of increasingly efficient advanced Virtual Network Embedding algorithms (e.g., AI-based), requires real-time and detailed network state information. This information can range from **traffic load**, processing capacity, energy consumption, and even topology and capacity in case of dynamic networks (e.g., Non-GEO satellite constellations)." | **把 traffic load 列为网络状态信息的构成项**（决策输入） |
| 487 | "AIbased algorithms can assist to provide solutions with reduced response time and operating costs." | **决策响应时间 + 运行成本**（决策成本显式化） |
| 442 | "Depending on the computing requirement, UAVs and satellites may support the ground infrastructure in both computing and coordination. For instance, for an intensive computation task, ubiquitous availability of satellites enable a fair distribution of the computation load, yet they may assist the network with coordinating the tasks over the available resources." | 计算负载的摊分（计算资源而非网络流量） |
| 444 | "Furthermore, a better data delivery can be provided by using satellite paths compared to the terrestrial Internet routing paths." | 卫星路径优于地面路径的时延断言 |
| 446 | "The effectiveness of AI applications in wireless networks heavily depends on reliable data at the network disposal." | AI 决策依赖数据可得性 |
| 448 | "the integration of NTN will allow fine-grained contextawareness, enabling multi-modal communication and quality of service based on the current location or context." | 上下文感知 QoS |
| 453 | "Effective UTM, which will essentially control the air traffic for UAV, can ensure the safe BVLoS operation by using the support from terrestrial and/or low latency LEO satellite networks." | 低时延作为 UAV 控制前提 |
| 455 | "Further to the communication rate and latency requirement, UAVs THz sensors can offer highly accurate environmental cognition" | 速率与时延需求 |
| 467 | "an extremely careful network management is required to avoid interference coming from different layers and orbital constellations under various propagation delay characteristics" | 传播时延差异下的管理 |
| 475 | "joint communication and sensing is believed to be a key driver for 6G systems as well" | 通感一体（非负载） |
| 491 | "reducing the overall delay in accomplishing the computing task - as the satellite constellation acts as a distributed processing system at the edge of the network" | 任务完成总时延 |
| 510 | "As the latency requirements becomes more critical and the amount of traffic does not cease to increase, the cloud-RAN architecture suffers from congestion caused by the fact that a substantial amount of data has to go through the core." | **流量增长 + 时延要求 → C-RAN 拥塞** |
| 504 | "(i) combines the transport and crypto to minimize the connection latency (i.e., zero Round-trip time (RTT) connection establishment); (ii) independent streams multiplexed in a single connection, thus avoiding the so-called “Head-of-line blocking” occurring when one lost packet blocks the rest of the data" | **队头阻塞（HOL blocking）**：单包丢失阻塞其余数据（与"失败事件的传播效应"直接相关） |

### 8.3 负向声明核验（模式 / 实测计数 / 命中判定）

- 模式 `credit` → **实测计数 0**。
- 模式 `arrival rate` → **实测计数 0**；`arrival process` → **实测计数 0**。
- 模式 `Poisson` → **实测计数 0**。
- 模式 `burst` → **实测计数 0**。
- 模式 `self-similar` → **实测计数 0**。
- 模式 `non-stationar` → **实测计数 0**。

### 8.4 它提到但本库其他论文未跟进的方向

1. **控制-通信联合设计（control-communication co-design），且算法须分布式自治以避免单点故障**：473。本库无对应论文。
2. **任务导向通信（Task-Oriented Communication, TOC）**：489–491。本库无对应论文。
3. **量子卫星网络（QKD）与自由空间噪声/空间天气耐受**：493。本库无对应论文。
4. **智能可重构表面（IRS）的空基部署与控制器**：477。本库无对应论文。
5. **3D 无蜂窝（cell-free）卫星通信与跨层幅度信息分辨**：465。本库无对应论文。
6. **多模通信（sub-6 GHz/mmWave/THz/VLC 无缝切换）与卫星"超级小区"协助切换**：479。本库无对应论文。
7. **面向 6G 的开放 RAN 智能控制器（NCC 与 SCC 之间的新接口）**：461。本库无对应论文。
8. **QUIC 在 NTN 的队头阻塞规避**：504。本库无传输层论文。
9. **数字化/VNE 实时网络状态（含 traffic load）驱动的切片编排**：506–508。本库无网络切片论文。
10. **THz 信道建模**：485。本库无物理层信道论文。

---

## 9. L5F3DK68 — Satellite-based communications security: A survey of threats, solutions, and research challenges

- 本地定位：TIER-ASSIGNMENT.md:110，"综述：只取共识与开放问题，不承重"
- MD 总行数：835
- 读取范围：第 51–62 行（标题/作者）、334–369 行（5. Emerging research challenges 全节 + 6. Conclusion）。
- **未通读（如实声明）**：63–333 行（摘要、1. 引言、2. 背景、3. 物理层安全方案、4. 密码学技术）。该区间仅做关键词检索（见 9.3）。

### 9.1 该综述认定的开放问题清单（逐字 + 行号）

| # | 行号 | 逐字原文 |
|---|---|---|
| O1 | 336 | "However, in addition to the identified research areas, our investigation highlighted further security-related SATCOM-based application domains that are receiving increasing attention from the scientific and business community." |
| O2 | 338 | "Still, doubts are there on the actual applicability of cognitive radio techniques in the context of satellite–terrestrial networks. This is mainly because of the extremely wide coverage of satellites, where the CR techniques might not work well." |
| O3 | 340 | "In the context of SATCOM, one of the most critical challenges consists of allowing secure communication between small/commercial UAVs and satellites." |
| O4 | 342 | "In the context of SATCOM, AI techniques could be used for many purposes, e.g., to identify physical-layer characteristics of the signals emitted by the satellites, to discriminate between authentic and injected signals, and for intrusion detection, to name a few ." |
| O5 | 346 | "However, SDN also come with their security issues, that are further specialized in SATCOM use-cases [206]. Additional research is needed in this context." |
| O6 | 348 | "However, there are neither common strategies nor protocols suitable to design a network slice in the context of SATCOM. Despite initial studies in this context are available [208,209], major work is still to be done, and we expect increasing attention towards this topic." |
| O7 | 350 | "However, reducing the cost and the impact of the satellite inevitably could affect the provided security services. This emerging research area, also suggested from the ESA [210], leads to a potential redesign of the existing procedures and technologies, also including the security domain." |
| O8 | 352 | "The usage of additional satellite constellations could provide reliability and spoofing detection mechanisms for devices on Earth, and more research into the robustness of such solutions is needed." |
| O9 | 358 | "In this context, none specifications edited by the 3GPP specifically took into account network security issues for NTNs. As a result, the current approach recommended by the 3GPP consists of a straightforward integration of the 5G security architecture and protocols into NTNs. Such an integration, however, comes with several challenges, in terms of communication overhead, software updates, and unreliability of the wireless links." |
| O10 | 358 | "However, the 3GPP refused to investigate further into the issue, at the time of this writing, still recommending a straightforward integration of 5G security into the NTN domain [218]." |
| O11 | 360 | "Nonetheless, due to the forecasted performance issues arising from such the integration of 5G-security into NTNs, we expect significant contributions by the research community in the years to come, potentially triggering dedicated and ad-hoc initiatives by the 3GPP." |
| O12 | 362 | "It is crucial that any security proposal framed in this context protect the communications while guaranteeing reliability, low latency, and secure and efficient transmission services." |
| O13 | 362 | "In the context of 6G initiatives, the 3GPP claimed that for the next few years (2030s) additional research is needed into this application area. Adapting and integrating the security services on satellites with mobile terrestrial/sea systems while meeting the requirements of 6G communication services will indeed represent a complex and difficult challenge [220]." |
| O14 | 368 | "Overall, we believe that the exposed research challenges highlight that the design and testing of cybersecurity strategies for SATCOMs is still an active research domain." |
| O15 | 354 | "The National Institute of Standards and Technology (NIST) is seeking comments on the draft specification NISTIR 8270, which describes the security procedures and the concepts for commercial space operations." |

### 9.2 涉及"负载过程/突发/时延/到达率/信用分配/决策成本"的表述（逐字 + 行号）

| 行号 | 逐字原文 | 归类 |
|---|---|---|
| 358 | "Such an integration, however, comes with several challenges, in terms of **communication overhead**, software updates, and unreliability of the wireless links." | **安全机制带来的通信开销**（安全成本 → 时延/带宽） |
| 362 | "It is crucial that any security proposal framed in this context protect the communications while guaranteeing reliability, low latency, and secure and efficient transmission services." | 安全与低时延/可靠性的权衡 |
| 350 | "However, reducing the cost and the impact of the satellite inevitably could affect the provided security services." | **降本与安全强度的权衡**（成本维度） |
| 342 | "the authors in [202] experimentally show that using a dedicated Convolutional Neural Network (CNN) it is possible to fingerprint the raw IQ samples received from LEO Satellites (Iridium) and authenticate the emitting transceiver on board of the satellite, despite the large distances." | 基于 CNN 的物理层指纹（学习方法的非路由用途） |
| 340 | "the authors in [198] investigated the IoT computing offloading problem by proposing a reinforcement learning approach to allocate the resources of the UAV edge server efficiently." | **RL 用于边缘服务器资源分配**（本文提及的唯一 RL 用例，与路由无关） |
| 338 | "They assume a scenario where the primary network is constituted by GEO, MEO, or LEO satellites, sending confidential messages to the fixed-satellite operator in the presence of eavesdroppers (secondary users) attempting to capture the satellite information signal." | 干扰/窃听场景（非负载） |

**判定**：本篇属安全综述，**与"负载过程/到达率/信用分配"无实质交集**。上表为全篇相关表述的**穷举**（范围＝第 334–369 行正文 + 关键词检索 63–333 行）。本篇对本题的价值仅在于：它给出了"安全机制开销"这一**决策成本的另一维**（L358），以及"3GPP 未针对 NTN 做专门安全设计"这一**标准化缺口**（L358）。

### 9.3 负向声明核验（模式 / 实测计数 / 命中判定）

- 模式 `credit` → **实测计数 0**。
- 模式 `arrival rate` → **实测计数 0**；`arrival process` → **实测计数 0**；`Poisson` → **实测计数 0**。
- 模式 `self-similar` → **实测计数 0**；`non-stationar` → **实测计数 0**。
- 模式 `burst` → **实测计数 2**。
  - **命中位置与逐字**：L177 "**Meteor Burst Communications**"（表 3 中的 GNSS 欺骗检测手段行）；L502 "[59] S. Sciancalepore, G. Oligeri, R.D. Pietro, Shooting to the stars: Secure location verification via meteor burst communications, in: 2018 IEEE Conference on Communications ..."（参考文献条目）。
  - **为何不构成反例**：两处均指**流星余迹通信（Meteor Burst Communications）**这一物理层通信手段，与"业务到达的突发性"完全无关。

### 9.4 它提到但本库其他论文未跟进的方向

1. **UAV-卫星安全通信与物理层安全（人工噪声辅助）**：340。本库无对应论文。
2. **认知卫星地面网络（cognitive satellite-terrestrial networks）的安全**：338。本库无对应论文。
3. **基于 CNN 的星上发射机射频指纹认证**：342。本库无对应论文。
4. **星基机会导航（利用 Starlink 等信号定位）与欺骗检测**：352。本库无对应论文。
5. **绿色卫星（environmentally-friendly satellites）对安全服务的冲击**：350。本库无对应论文。
6. **面向 SATCOM 的网络切片安全策略与协议**：348。本库无对应论文。
7. **SDN 在 SATCOM 的特有安全问题**：346、344。本库无对应论文。
8. **IoST 的网络安全标准与 NISTIR 8270 落地**：354。本库无对应论文。
9. **面向 NTN 的 3GPP 安全标准化缺口（5G 安全直接搬用的问题）**：358。本库无对应论文。

---

## 10. UMKF328H — LEO Satellites in 5G and Beyond Networks: A Review From a Standardization Perspective

- 本地定位：TIER-ASSIGNMENT.md:111，"综述：只取共识与开放问题，不承重"
- MD 总行数：624
- 读取范围：第 84–97 行（I. INTRODUCTION）、451–506 行（VIII. STANDARDIZATION FOR 6G SATELLITE COMMUNICATIONS NETWORKS 全节：A. MOBILITY MANAGEMENT、B. ROUTING、C. ADOPTION OF SDN/NFV、D. INTELLIGENT MANAGEMENT AND ORCHESTRATION、E. FAULT-TOLERANCE SOLUTIONS、F. DYNAMIC SPECTRUM MANAGEMENT + IX. CONCLUSION）。
- **未通读（如实声明）**：98–450 行（II–VII 各节：3GPP 标准化活动、星地接入架构、NR 适配、管理编排、其他标准化组织）。

### 10.1 该综述认定的开放问题清单（逐字 + 行号）

| # | 行号 | 逐字原文 |
|---|---|---|
| O1 | 453 | "Most of the standardization work carried out by 3GPP and other standardization organizations focuses on the physical and MAC layers. Consideration has also been given to defining satellite use cases and architectural options in the context of integrated satellite 5G networks. The following subsections highlight several issues that need to be considered in standardization work in order to achieve the complete integration of satellite and terrestrial 6G networks." |
| O2 | 457 | "LEO satellites provide shorter propagation delays and higher data rates than GEO satellites. However, these advantages come with the price of frequent handover and topology changes, which yields a time-varying communication channel." |
| O3 | 470 | "Such a scenario will lead to thousands of UE being connected to an LEO satellite and this large group of users will need to go through a frequent handover process at almost the same time. Managing the handover of thousands of users simultaneously or semi-simultaneously using conventional handover management schemes will create huge network loads. New handover management schemes are required to deal with this issue in 6G LEO SatNets." |
| O4 | 472 | "However, such protocols were not designed to deal with the high topology change rate in SatNets, where everything is moving including the gNB (LEO satellite base station)." |
| O5 | 474 | "The fast-moving footprint of LEO satellites affects the paging procedure, which is primarily related to the tracking area management. The tracking area is the satellite coverage area (footprint); it can be fixed or moving. Although the moving tracking area accommodates the LEO satellite moving footprint, it results in high paging loads that are difficult to manage by the network." |
| O6 | 474 | "In addition, supporting dual-connectivity and vertical handovers in future LEO Sat-Nets requires novel mechanisms to provide seamless mobility in integrated 6G networks and to improve global network coverage and service." |
| O7 | 478 | "Due to the frequent topology changes in an LEO SatNet, ISLs have a limited lifetime. In addition, some ISLs may get congested due to high traffic loads at certain partitions of the SatNet." |
| O8 | 478 | "Moreover, as LEO SatNets are expected to serve different types of applications, there are certain QoS requirements (e.g., packet delivery delay, packet delivery ratio) that need to be met for each type of applications. Therefore, successful data delivery will require robust routing schemes that can fulfil the QoS requirements of each application type and adapt to the unique characteristics of LEO SatNets." |
| O9 | 478 | "Thus, it is crucial to develop standard routing protocols that adapt to the SatNet dynamic environment and satisfy the various user application requirements. Standards should support interoperability among the different satellite constellations and operators. Moreover, cross network routing (i.e., across satellite, aerial, and terrestrial networks) should be considered to achieve the full integration in 6G. To support efficient routing, topics such as resource allocation, network monitoring, and congestion control should be considered as part of the standardization work." |
| O10 | 482 | "The SDN/NFV paradigms will play a key role in future integrated networks. However, the use of SDN/NFV in an LEO SatNet has not yet been fully investigated." |
| O11 | 482 | "For instance, on-board SDN-compatible routers could be developed following a specific standard to operate on LEO satellites and provide a softwareized routing function that can adapt to changes in the dynamic environment of LEO SatNets." |
| O12 | 489 | "However, in the area of satellite networks, the adoption of these concepts and technologies is still in its infancy. Further investigations are required to identify the requirements needed to adopt NFV in SatNets. In addition, the support for NFV should be considered in the design of satellite network components." |
| O13 | 493 | "However, both ENI and SON concepts are still limited to the 5G context and may not be sufficiently agile in coping with the immense levels of complexity, heterogeneity, and mobility in the envisioned beyond-5G integrated networks." |
| O14 | 493 | "Nevertheless, SEN is quite a recent concept and has not yet been considered by standardization organizations." |
| O15 | 497 | "Satellite network environment is very vulnerable to faults and malfunctioning that are difficult to fix while the satellite being in space. Satellites communication functionality might get disabled which makes the satellite be as a dead node in the network. In addition, upgrading a satellite base station is not as easy as upgrading a terrestrial base station [42]. Moreover, the satellite scarce power supply my disturbs the normal telecommunication functionality." |
| O16 | 497 | "Therefore, the satellite network design should be based on the concept of fault-tolerance in order to maintain the survivability of the network. In addition, the satellite related standardization activities should support the fault-tolerance concept in future densely deployed satellite networks." |
| O17 | 501 | "The problem of spectrum scarcity is one of the key challenges facing future SatNets as more satellites are deployed and more applications are emerging. The factors of unpredictable user mobility and satellite mobility make dynamic spectrum allocation necessary but difficult as well." |
| O18 | 501 | "Although various kinds of static and dynamic spectrum allocation schemes have been studied by satellite researchers, this issue is not covered sufficiently in the standardization works." |
| O19 | 505 | "The 3GPP community has achieved some advancements in the NTN integration with 5G from a standardization perspective. However, more standardization efforts are needed to realize the full integration of SatNets and 5G+ on the physical layer level up to the application level." |

### 10.2 涉及"负载过程/突发/时延/到达率/信用分配/决策成本"的表述（逐字 + 行号）

| 行号 | 逐字原文 | 归类 |
|---|---|---|
| 478 | "In addition, some ISLs may get congested due to high traffic loads at certain partitions of the SatNet." | **局部高流量导致 ISL 拥塞**（负载的空间局部性） |
| 470 | "Managing the handover of thousands of users simultaneously or semi-simultaneously using conventional handover management schemes will create huge network loads." | **信令负载**（同步切换产生的负载，非数据负载） |
| 474 | "Although the moving tracking area accommodates the LEO satellite moving footprint, it results in high paging loads that are difficult to manage by the network." | 寻呼负载 |
| 478 | "there are certain QoS requirements (e.g., **packet delivery delay, packet delivery ratio**) that need to be met for each type of applications" | 时延与投递率作为 QoS 指标 |
| 478 | "To support efficient routing, topics such as **resource allocation, network monitoring, and congestion control** should be considered as part of the standardization work." | 拥塞控制被列为标准化议题 |
| 457 | "these advantages come with the price of frequent handover and topology changes, which yields a time-varying communication channel" | 时变信道 |
| 472 | "However, such protocols were not designed to deal with the high topology change rate in SatNets" | **拓扑变化率**（时间尺度） |
| 493 | "SEN can be adopted to support real-time decisions, seamless control, intelligent management in SatNets to achieve high-level autonomous operations." | **实时决策**（决策时延要求） |
| 493 | "SEN utilizes AI/ML to make future integrated networks fully automated, and it intelligently evolves with respect to the provision, adaptation, optimization, and management aspects of networking, communications, computation, and infrastructure nodes’ mobility." | 自治演化 |
| 501 | "The factors of unpredictable user mobility and satellite mobility make dynamic spectrum allocation necessary but difficult as well." | 不可预测的用户移动性（负载源的不确定性） |

### 10.3 负向声明核验（模式 / 实测计数 / 命中判定）

- 模式 `credit` → **实测计数 0**。
- 模式 `arrival rate` → **实测计数 0**；`arrival process` → **实测计数 0**。
- 模式 `Poisson` → **实测计数 0**。
- 模式 `burst` → **实测计数 0**。
- 模式 `self-similar` → **实测计数 0**。
- 模式 `non-stationar` → **实测计数 0**。

### 10.4 它提到但本库其他论文未跟进的方向

1. **自演化网络（Self-Evolving Network, SEN）用于 6G 星地一体化**：493。本库无对应论文。
2. **ETSI ENI（体验式网络智能）的推荐/管理模式与 3GPP SON 的局限**：493。本库无对应论文。
3. **面向标准化的一致性/互操作路由协议（跨星座、跨运营商、跨空天地）**：478。本库无标准化论文。
4. **星上 SDN 兼容路由器（按标准实现）**：482。本库无对应论文。
5. **卫星网络的 NFV 采纳要求**：489。本库无对应论文。
6. **跟踪区管理（移动跟踪区带来的高寻呼负载）**：474。本库无移动性管理论文。
7. **动态频谱管理在标准化工作中的缺位（含 THz 与 FSO）**：501。本库无对应论文。
8. **星上基站升级困难与功率受限导致的功能退化**：497。本库无对应论文（注：8N9QJHC2 的故障恢复路由与之相关，但那是 T1 档，不在本档结论范围）。

---

## 11. BV4XI6CU — Load Balancing for 5G Integrated Satellite-Terrestrial Networks

- 本地定位：TIER-ASSIGNMENT.md:112，"综述：只取共识与开放问题，不承重"（**注**：该篇实为**算法研究论文**，非综述；定档表将其归入 T5。本档按 T5 深度要求执行，但因其含完整算法，第 2 项的负载相关表述密度是本批最高）
- MD 总行数：485
- 读取范围：第 3–16 行（题录/摘要/索引词）、17–37 行（I. INTRODUCTION）、92–180 行（II.D LOAD MEASUREMENT IN 5G MULTI-RATs + II.E PROBLEM FORMULATION）、184–315 行（III. THE PROPOSED ALGORITHM 全节）、316–330 行（IV.A SIMULATION ENVIRONMENTS）、398–409 行（IV.F IMPACT OF DELAY-TOLERANT FLOWS WITH DIFFERENT NETWORK LOAD + V. CONCLUSION）。**基本通读**（除 IV.B–IV.E 的结果图描述外）。

### 11.1 该文认定的开放问题清单（逐字 + 行号）

该文为非综述研究论文，"开放问题"以引言中的既有工作缺口形式呈现：

| # | 行号 | 逐字原文 |
|---|---|---|
| O1 | 13（摘要） | "However, previous load balancing algorithms do not consider the coexistence of NTNs and TNs and ignore the different resource allocation units in a multi-RAT network." |
| O2 | 29 | "The previous work used a multi-RAT network to increase capacity and coverage of the TNs, but did not consider load balancing in terrestrial RAT. Further, previous work did not devise a common metric to measure RAT traffic loads, which is necessary in a multi-RAT network because different RATs use different time frequency r..." |
| O3 | 100 | "However, the total number of PRBs, `$N _ { P R B }$`, in 5G changes dynamically with changes in subcarrier spacing [21]. Therefore, the RBUR cannot be directly used to measure the cell load in 5G RAT." |
| O4 | 102 | "Furthermore, radio resources are not allocated in terms of the PRBs in an NTN. Since, we need a common metric/parameter to measure the radio resources utilization of different RATs for a 5G multi-RAT network." |
| O5 | 120 | "If RRUR is more than a predefined threshold, the cell is overloaded, and UEs moving to that cell will either be dropped or will experience low data rates. Hence, new UEs in an overloaded cell will reduce the per UE data rates." |
| O6 | 25 | "However, sometimes UEs cannot move to neighboring cells due to a scarcity of resources and limited coverage. This affects efficient load balancing among cells, and decreases QoS of the users." |
| O7 | 408 | "The proposed algorithm depends on the availability of delay-tolerant flows to achieve better performance." |
| O8 | 404 | "When the network load is high, the adaptive multi-RAT MLB requires a higher ratio of delay-tolerant flows to balance the terrestrial cells. Hence, we can say that the adaptive multi-RAT MLB depends on the availability of delay-tolerant flows for inter-RAT offloading to achieve better performance." |

### 11.2 涉及"负载过程/突发/时延/到达率/信用分配/决策成本"的表述（逐字 + 行号）

本篇是本批 **"负载"主题的核心来源**，逐条如下：

| 行号 | 逐字原文 | 归类 |
|---|---|---|
| 94 | "Proper load measurement of cells is crucial for optimizing the performance of a network through load balancing. For that purpose, a common load measurement metric is needed to measure the load of each RAT in a multi-RAT network." | **负载度量的前置性** |
| 97 | `$overline { { R B } } _ { n } = rac { 1 } { T cdot N _ { P R B } } sum _ { 	au in ( t - T , t ) } R B _ { n }$`（式 2） | **负载＝时间窗 T 内的资源块占用均值**（公式逐字抄录） |
| 100 | "where `$R B _ { n }$` and `$N _ { P R B }$` are the number of allocated resource blocks and the total number of resource blocks in the cell, respectively." | 式 2 符号定义（逐字） |
| 104 | "In this paper, we introduce the radio resource usage ratio (RRUR) as a load measurement metric for the multi-RAT network. We defined RRUR as the ratio of bandwidth used by RAT to the total RAT bandwidth." | RRUR 定义 |
| 107 | `$eta _ { n } = rac { 1 } { T cdot omega _ { n } } sum _ { 	au in ( t - T , t ) } gamma _ { 	au } cdot arsigma _ { 	au }$`（式 3） | 5G RAT 的 RRUR（公式逐字抄录） |
| 110 | "where `$omega _ { n }$` is the total bandwidth of 5G cell `$n ,$` and `$gamma _ { 	au }$` and `$arsigma _ { 	au }$` are the allocated PRBs and resource block bandwidth at time τ, respectively. The resource block bandwidth depends on the numerologies." | 式 3 符号定义（逐字） |
| 115 | `$eta _ { S } = rac { 1 } { T cdot omega _ { s a t } } sum _ { 	au in ( t - T , t ) } Omega _ { 	au }$`（式 4） | 卫星 RAT 的 RRUR（公式逐字抄录） |
| 118 | "where `$Omega _ { 	au }$` is the bandwidth allocated to UEs based on the Shannon formula and `$omega _ { s a t }$` is the total bandwidth of the satellite at time τ ." | 式 4 符号定义（逐字） |
| 120 | "Based on the common load measure metric, i.e., RRUR, load distribution among cells of different RATs is determined. A higher RRUR of a cell indicates that the cell has a higher load to serve and fewer available resources." | 负载→资源可得性 |
| 124 | "In a network, if the RRUR of a RAT cell is close to 1, a user that moves into the cell will either be dropped or will experience a low data rate." | **负载水平→用户被丢弃** |
| 129 | `$operatorname* { m i n } quad sum _ { orall n in mathcal { T } } | overline { { eta } } - eta _ { n } | ^ { 2 }$` + `$mathrm { s u b j e c t ~ t o : ~ } eta _ { S } leq T h r _ { a d p } ,$` + `$eta _ { kappa } ^ { i } geq ho _ { i } , quad kappa in mathcal { N }$`（式 5） | **优化目标：最小化各小区 RRUR 与目标值的平方距离**；约束含自适应阈值与每用户资源下限（公式逐字抄录） |
| 132 | "where `$eta _ { n }$` is the RRUR of terrestrial cell n, `$eta _ { S }$` is the RRUR of a satellite cell S, `$T h r _ { a d p }$` is the adaptive threshold, `$eta _ { kappa } ^ { i }$` is the resource allocated to user i by cell κ, and `$ho _ { i }$` is the resources required by user i, from which `$ho _ { i }$` is calculated based on the minimum data rate required by UE i." | 式 5 符号定义（逐字） |
| 161 | `$overline { { eta } } = E [ eta _ { n } ]$`（式 7） | 目标负载＝RRUR 的期望（公式逐字抄录） |
| 189 | `$T h r _ { a d p t } = m a x ( overline { { eta } } , t h r _ { i n i t } )$`（式 8） | **自适应阈值＝均值与初始阈值的较大者**（公式逐字抄录） |
| 192 | "where `$t h r _ { i n i t }$` is the fixed initial threshold used to determine whether there is a need for load balancing in the network. The adaptive threshold, `$T h r _ { a d p t }$`, is used to adopt the network load. **The network load can vary over time because of user mobility and variances in required data rates of the UEs.**" | **负载随时间变化的两大成因**（用户移动 + 需求速率方差）——本批对"负载过程"成因最明确的表述之一 |
| 203 | `$eta _ { n } > T h r _ { a d p t } , n in mathcal { T }$`（式 9） | **过载判定：RRUR 超过自适应阈值**（公式逐字抄录） |
| 215 | `$hat { eta } _ { Gamma _ { k } } ^ { e _ { 1 } } = rac { ho _ { e _ { 1 } } arsigma } { omega _ { Gamma _ { k } } }$`（式 10） | **目标小区负载增量的预估**（公式逐字抄录） |
| 221 | `$eta _ { Gamma _ { k } } + hat { eta } _ { Gamma _ { k } } ^ { e _ { 1 } } < T h r _ { a d p t }$`（式 11） | 目标小区不过载约束（公式逐字抄录） |
| 225 | `$eta _ { o } - hat { eta } _ { o } ^ { e _ { 1 } } > eta _ { Gamma _ { k } } + hat { eta } _ { Gamma _ { k } } ^ { e _ { 1 } } .$`（式 12） | **源小区减载后仍高于目标小区**——防乒乓（公式逐字抄录） |
| 218 | "Before offloading UE `$e _ { 1 }$` to cell `$Gamma _ { k }$`, the algorithm checks the following conditions in order to restrict the target cell load to below overload status and to avoid unnecessary offloading of UEs to neighboring cells, i.e., to avoid ping-pongs:" | **乒乓（ping-pong）规避** |
| 210 | "For intra-RAT load balancing, first the UEs of `$E _ { o }$` with delay-sensitive flows, and then UEs with delay-tolerant flows, move to underloaded neighboring cells one by one based on the load status of cell `$o .$`" | **按业务时延敏感度排序迁移**（决策次序） |
| 210 | "The UEs in `$E _ { o } = \{ e _ { 1 } , . . , e _ { n } \}$` are then sorted in ascending order of serving cell RSRPs and the UEs are arranged according to data flow type." | 按 RSRP 升序 + 按流类型排序（迁移候选的排序规则） |
| 262 | "After intra-RAT load balancing, the algorithm again checks the load status of the cell o. If the cell is still overloaded, i.e., `$eta _ { o } ~ > ~ T h r _ { a d p }$`, the algorithm performs inter-RAT load balancing by transferring the load of cell o to satellite cell S by offloading the delay-tolerant flows of UEs if" | **两级负载均衡（先 intra-RAT 后 inter-RAT）** |
| 265 | `$eta _ { S } < T h r _ { a d p }$`（式 13） | 卫星未过载条件（公式逐字抄录） |
| 299 | `$eta _ { S } + hat { eta } _ { S } ^ { arepsilon _ { 1 } } < T h r _ { a d p t }$`（式 14） | 卫星不过载约束（公式逐字抄录） |
| 302 | "The above condition prevents the satellite from being overloaded. For the offloading of data flows, the UPF directs the flow of UE `$arepsilon _ { 1 }$` to NTN gNB as we considered the separate user plane for each RAT." | 用户面按 RAT 分离 |
| 305 | `$eta _ { S } = eta _ { S } + hat { eta } _ { S } ^ { arepsilon _ { 1 } } ,  mathrm { a n d } $` + `$eta _ { o } = eta _ { o } - hat { eta } _ { o } ^ { arepsilon _ { 1 } } .$`（式 15） | **负载状态的增量更新式**（公式逐字抄录） |
| 310 | "When UEs moves to a satellite, they will experience a long delay. However, offloading UEs with delay-tolerant data flows will not affect the QoS of the UEs, whereas UEs with delay-sensitive data are served by the 5G RAT." | **时延承受度作为分流依据** |
| 312 | "We analyzed the computational complexity of the proposed algorithm using big O notation." | **决策成本（复杂度）显式分析**——本批唯一做此分析的篇目 |
| 314 | "the overall computational complexity of the proposed load balancing algorithm becomes `$O ( | T | ^ { 2 } ) + O (  { mathcal { T } } | T | )$`. Generally, `$mathcal { T } gg | mathcal { T } |$` so we can say that the computational complexity for the proposed load balancing algorithm is O(I|T|)." | **算法复杂度结果：O(I·|T|)**（公式逐字抄录） |
| 400 | "For the different network load, we changed the required data rate of each UE. The required data rates for each UE were 5-10 Mbps and 10-15 Mbps for low and high network load, respectively." | **负载水平＝每用户需求速率**（负载的定义方式登记） |
| 404 | "By increasing delay-tolerant traffic, the adaptive multi-RAT MLB finds more UEs with delay-tolerant flows, and offloads the UEs from overloaded cells to a satellite to balance the network." | 分流比例随可分流业务占比变化 |
| 408 | "Based on intra-RAT and inter-RAT offloading, the load across terrestrial cells became more balanced and the number of satisfied UEs increased in the network." | 结果（不作贡献，仅登记） |

**信用分配**：本篇为**非学习**的路由/负载均衡算法（阈值 + 逐用户贪心），不存在 RL 信用分配问题。与"负载/时延/决策成本"相关的表述已在上表穷举。

### 11.3 负向声明核验（模式 / 实测计数 / 命中判定）

- 模式 `credit` → **实测计数 0**。
- 模式 `arrival rate` → **实测计数 0**；`arrival process` → **实测计数 0**。
- 模式 `Poisson` → **实测计数 0**。
- 模式 `burst` → **实测计数 0**。
- 模式 `self-similar` → **实测计数 0**。
- 模式 `non-stationar` → **实测计数 0**。

**重要限定**：本篇虽有"负载随时间变化"的定性表述（L192）与时间窗均值度量（式 2/3/4），但**全文未对负载的到达过程做任何随机过程建模**（无 Poisson、无 burst、无自相似、无马尔可夫到达过程）。负载在其模型中是**可测量、可预测均值的确定性量**（式 7 的期望），这构成与本库"负载过程/突发"选题的**明确缺口对照**。

### 11.4 它提到但本库其他论文未跟进的方向

1. **多 RAT 统一负载度量（RRUR）**：104–118。本库 T1/T2 路由论文的负载度量均为单一网络内的队列长度/链路利用率，**无跨 RAT 统一度量**的设计。
2. **自适应阈值（式 8）驱动的过载判定**：189。本库 T2 的 ELB（JP79GMZS）用固定阈值 + 队列占用；式 8 的"阈值随网络均值浮动"在 T2 档需复核是否被采用。
3. **防乒乓（ping-pong）的双向约束（式 11+12）**：218–226。本库 T2 负载均衡论文未见对"迁移后再迁回"的显式约束。
4. **按业务时延敏感度决定迁移次序**：210。本库 T2 有按优先级分流的方案（T9X6QCLL L185 记载），但未见"迁移候选排序 = RSRP 升序 × 流类型"的组合规则。
5. **显式的算法复杂度分析**：312–314。本库多数路由论文不报复杂度（需 T1/T2 档复核）。
6. **延迟容忍流占比作为性能前提**：404、408。本库 T1/T2 论文较少把"可分流业务占比"作为性能的前提条件显式声明。

---

## 12. 524XNF29 — Non-Terrestrial Networks in 5G & Beyond: A Survey

- 本地定位：TIER-ASSIGNMENT.md:113，"综述：只取共识与开放问题，不承重"
- MD 总行数：771
- 读取范围：第 4–23 行（题录/摘要/索引词）、333–439 行（VII. OPEN ISSUES AND FUTURE DIRECTIONS 全节 + VIII. TOWARD 6G SATELLITE COMMUNICATIONS + IX. CONCLUSIONS）。
- **未通读（如实声明）**：24–332 行（I–VI 各节：引言、NTN 描述、NTN 架构、NTN 在蜂窝中的角色、5G 中的 NTN、3GPP 研究活动）。

### 12.1 该综述认定的开放问题清单（逐字 + 行号）

| # | 行号 | 逐字原文 |
|---|---|---|
| O1 | 335 | "In this section, we discuss the main open issues and pave the way to future research directions. In particular, we focus on the management of mobility, propagation delay, and radio resources." |
| O2 | 339 | "However, the motion of both the NGSO satellites around Earth and the UEs in a given region yields a time-varying NGSO channel. The dynamic nature of NGSO satellite links has an important implication on handover and paging procedures." |
| O3 | 341 | "In the case of NGSO satellites, frequent intra-satellite handovers are related to high speeds of the beam footprint on the ground." |
| O4 | 360 | "The moving tracking area incurs high paging loads that are difficult to manage by the network. Indeed, the NGSO beam footprints do not correspond to the terrestrial cells on the ground. As a consequence, the NGSO satellite-based RAN is not able to provide the exact information on the UE tracking area during the initial registration. Furthermore, the UE cannot always establish its location for Registration Update and Paging procedures." |
| O5 | 366 | "None of the works in past literature considered the 5G NR. Future studies might integrate the NR technology with the NTN to improve compatibility with 5G NR terrestrial networks." |
| O6 | 366 | "New procedures to support dual-connectivity and novel mechanisms for vertical handovers might be proposed to improve global network coverage, service continuity, and seamless mobility in hybrid/integrated terrestrial and NTN systems." |
| O7 | 366 | "Further, solutions for UE geolocation are required to determine the belonging beam (satellite), the beam (satellite) belonging time, and the next-to-switch beam (satellite) to simplify handover and paging procedures." |
| O8 | 370 | "The propagation delay has a profound impact on the system performance in non-terrestrial communications and can be considered as one of the main challenges for URLLC applications and critical communications (i.e., public safety)." |
| O9 | 376 | "In NGSO satellite-based communications, the UE radio channel is characterized by rapid fluctuations over time; hence, after the propagation time has elapsed, the UE may no longer be able to decode the received data or can perceive an undesired QoS." |
| O10 | 380 | "In future research activities, it might be essential to investigate the ways how these factors lead to changes in the user channel as well as how to cope with abrupt channel variations by considering propagation delay to ensure service continuity." |
| O11 | 384 | "Radio resource management is one of the major considerations in 5G NR technology. Hence, efficient radio resource allocation is essential to avoid the following:" |
| O12 | 398 | "The availability of new frequency bands (i.e., mmWave) and the introduction of scalable 5G NR numerology [134] led to additional challenges in the management of the radio spectrum for NTN systems." |
| O13 | 398 | "Indeed, different numerologies (i.e., different subcarrier spacings) may coexist over a given frequency band, thus generating novel types of interference, known as inter-numerology interference (INI) [135]." |
| O14 | 400 | "Therefore, the research community might address the issue of INI mitigation in multinumerology NTN systems for 5G and beyond technologies." |
| O15 | 400 | "Future research activities can focus on new solutions to boost the capacity by limiting inter-beam interference in multi-spotbeam satellite systems." |
| O16 | 400 | "Finally, novel radio resource allocation techniques might be required to handle the transmission of several services and to cope with inter radio access network interference in hybrid/integrated terrestrial-NTN systems." |
| O17 | 427 | "Here, the 6G NTN is expected to support emerging critical use cases (i.e., disaster prediction) and achieve global connectivity with seamless network access in maritime and mountainous scenarios." |

### 12.2 涉及"负载过程/突发/时延/到达率/信用分配/决策成本"的表述（逐字 + 行号）

| 行号 | 逐字原文 | 归类 |
|---|---|---|
| 370 | "The propagation delay is defined as the latency either from the NTN gateway to the NTN terminal via space/airborne platform (i.e., transparent payload) or from the space/airborne platform to the NTN terminal (i.e., regenerative payload)." | **传播时延的定义口径**（逐字） |
| 370 | "Furthermore, the propagation delay depends on the NTN platform altitude, the NTN gateway position and elevation angle, and the NTN terminal position [3]." | 传播时延的依赖因子 |
| 372 | "• One-way propagation delay considers the time needed by the information to travel from the NTN gateway to the NTN terminal through the NTN platform (in the case of the transparent payload-based satellite) or from the NTN platform to the NTN terminal (in the case of the regenerative payload-based satellite)." | 单向传播时延定义（逐字） |
| 374 | "• Two-way propagation delay, also known as Round Trip Time (RTT), takes into account the time required by the information to travel from the NTN gateway to the NTN terminal through the NTN platform and back (in the case of the transparent payload-based satellite) or from the NTN platform to the NTN terminal and back (in the case of the regenerative payload-based satellite)." | 双向传播时延/RTT 定义（逐字） |
| 376 | "Furthermore, the propagation delay is a crucial parameter to be considered during the choice of transmission parameters (i.e., MCS)." | **时延作为决策参数**（MCS 选择） |
| 376 | "In NGSO satellite-based communications, the UE radio channel is characterized by **rapid fluctuations over time**; hence, after the propagation time has elapsed, the UE may no longer be able to decode the received data or can perceive an undesired QoS." | **信道快速波动 + 反馈时延 → 决策失效**（决策时标与过程时标的错配） |
| 380 | "The NTN channel is modeled by considering relative movements of both the NTN platform and the UE, NTN altitude and orbit, UE antenna type, atmospheric conditions, presence or absence of obstacles (i.e., building, foliage, mountains), deployment scenario, and frequency bands." | 信道模型输入的穷举（逐字） |
| 360 | "The moving tracking area incurs **high paging loads** that are difficult to manage by the network." | 寻呼负载 |
| 362 | "In [119], the authors modeled the handover process and proposed a strategy for inter-beam satellite handover based on the potential game for mobile terminals to minimize the number of handovers, **balance the LEO constellation load**, and reduce the handover time." | **切换次数最小化 + 星座负载均衡 + 切换时间**（三目标） |
| 388 | "In the case of heterogeneous NTN systems, when an NGSO satellite enters the LoS conditions with the GEO satellite, dynamic RRM techniques aid in coping with mitigating interference between the GEO and the NGSOs inside the GEO LoS cone." | 干扰（非负载） |
| 390 | "The integration of NTNs with terrestrial systems may be exploited in many 5G scenarios to extend cellular coverage or to **offload terrestrial traffic**. In the latter case, radio resources need to be allocated to limit the interference between the GEO (or NGSO) and the gNBs." | **地面流量卸载到 NTN** |
| 425 | "• Artificial Intelligence for real-time satellite decisions and seamless satellite control to achieve high-level autonomous operations." | **实时卫星决策**（决策时延要求） |
| 410 | "• Time Engineered Applications, such as industrial automation, autonomous systems, and massive sensor networks, where the time factor is extremely important for real-time response." | 时间要素作为 6G 应用类别 |
| 348 | 表 8 中 "Propagation delay. Varying NTN channel" → Effect: "Channel estimation / Scheduling" → Issues: "**Delay-CSI-MCS management**: new techniques to select transmission parameters (i.e., MCS) to ensure that UE may perceive satisfactory service quality and reliably decode transmitted data **despite rapid channel fluctuations and long propagation delays**." | **延迟-CSI-MCS 联合管理** |

### 12.3 负向声明核验（模式 / 实测计数 / 命中判定）

- 模式 `credit` → **实测计数 0**。
- 模式 `arrival rate` → **实测计数 0**；`arrival process` → **实测计数 0**。
- 模式 `Poisson` → **实测计数 0**。
- 模式 `burst` → **实测计数 0**。
- 模式 `self-similar` → **实测计数 0**。
- 模式 `non-stationar` → **实测计数 0**。注意：本篇 L339 用 "time-varying NGSO channel"、L376 用 "rapid fluctuations over time" 表述信道时变性，但**未使用 non-stationar 一词**（已用精确模式核验）。

### 12.4 它提到但本库其他论文未跟进的方向

1. **延迟-CSI-MCS 联合管理（应对快速信道波动 + 长传播时延）**：348 表 8、376。本库无对应论文。
2. **星历数据管理（向 UE 高效提供并更新星历）**：348 表 8。本库无对应论文。
3. **馈电链路切换（feeder link switch-over）的无缝管理**：348 表 8。本库无对应论文。
4. **交错 numerology 干扰（INI）在 NTN 的抑制**：398–400。本库无对应论文。
5. **面向 UE 地理定位以简化切换与寻呼的机制**：366。本库无移动性管理论文。
6. **全息无线电 / 非射频（光）NTN**：421–423。本库无对应论文。
7. **多播预编码与用户聚类（k-means）以抑制多波束干扰**：392–396。本库无对应论文。
8. **以势博弈（potential game）同时最小化切换次数、均衡星座负载、降低切换时间**：362。本库 T1/T2 未见势博弈方法的切换/负载联合优化（需 T1/T2 档复核）。
9. **地面流量向 NTN 卸载及其干扰约束**：390。本库 BV4XI6CU 做了相邻工作，但无跨档系统比较，仅在综述层登记。

---

## 13. 5AZHJE7N — Network Simulators for Satellite-Terrestrial Integrated Networks: A Survey

- 本地定位：TIER-ASSIGNMENT.md:114，"综述：只取共识与开放问题，不承重"
- MD 总行数：721
- 读取范围：第 3–18 行（题录/摘要/索引词）、126–137 行（III.C STIN SIMULATION EVALUATION METRICS 全节）、413–465 行（VI. FUTURE RESEARCH DIRECTIONS 全节 + VII. CONCLUSION）。
- **未通读（如实声明）**：19–125 行（I. INTRODUCTION、II. STIN BACKGROUND、III.A/III.B）、138–412 行（IV. 仿真框架与工具、V. 仿真器文献综述——本批未通读的最大区块）。

### 13.1 该综述认定的开放问题清单（逐字 + 行号）

| # | 行号 | 逐字原文 |
|---|---|---|
| O1 | 419 | "The dynamic integration simulation of the packet-level network simulator and the astrodynamics simulator is still not satisfactory. Due to the complex natures of these isolated simulators, most of the simulations in the literature are based on a static file exchange fashion, e.g., a static satellite trace file is generated by STK first and then loaded by other tools, which is not flexible." |
| O2 | 421 | "While some early attempts to build a dynamic integration environment have been made in the literature, e.g., in GEMINI [83], there is not yet a perfect solution, especially for large-scale LEO constellations." |
| O3 | 423 | "Under this situation, the network simulator should possess the ability to model the evolving network topology and evaluate the adapted network management schemes, e.g., new routing methods when the previous ones no longer work." |
| O4 | 427 | "For most existing STIN simulators, the generated network traffic follows some empirical distributions or emulates some specific services, e.g, web browsing or live streaming. The network functions and protocols are evaluated with these normal behaviors and Monte-Carlo simulations, without considering malicious and abnormal user behaviors in more realistic scenarios." |
| O5 | 429 | "The common cyber-attacks in terrestrial networks could be applied in different layers if similar protocols are to be used in STIN, which include the denial-of-service (DoS) and distributed DoS attacks in the networking layer and blocking, jamming, and spoofing in the physical layer." |
| O6 | 431 | "The complex user behavior emulation has only been considered in several studies [98], [99], and there is still room for improvement [100]." |
| O7 | 444 | "Further integration between cloud computing and STIN simulation is required with better support for large-scale simulation and web-based GUIs if millions of users and thousands of network nodes are to be emulated. It is not only a scientific problem to build an efficient and distributed simulation platform, but also a challenging engineering problem to implement a scalable and sustainable cloud-based STIN simulation platform, which is worth further exploration." |
| O8 | 448 | "AI has been proven effective for network optimization and management of satellite and terrestrial networks in previous studies [101]–[105]. However, previous applications of AI in networking rely on external simulation tools, e.g., TensorFlow and PyTorch. For those researchers who are not familiar with these development tools, it is difficult to leverage the state-of-the-art AI models. It is still in an early stage to integrate AI tools and network simulators, so that new network-related models and algorithms can be designed more efficiently" |
| O9 | 450 | "Another potential direction is to benchmark AI-based networking solutions in STIN scenarios. While AI models have been introduced in many studies, their performance is evaluated in different settings and without a unified dataset, e.g., ImageNet for image classification." |
| O10 | 450 | "The challenge is that real-world traffic data are difficult to acquire in satellite-terrestrial integrated networks for both the technical and political reasons [109]. One potential alternative solution is to embed the STIN simulators with some common parameters or simulation data that can be loaded directly and used as benchmarks for evaluating and comparing different AI models [110]." |
| O11 | 458 | "Some research progress has been made in the literature. However, dedicated simulation tools have not been developed yet [15]." |
| O12 | 458 | "Most of the existing relevant studies are based on MATLAB and Monte Carlo simulations [116]–[118], and there is still a huge research space for developing efficient simulation tools." |
| O13 | 464 | "It is observed that the research of developing STIN simulators is still in an early exploration stage with no mature solutions." |
| O14 | 128 | "However, these existing discussion for KPIs is not comprehensive, and in this survey, we present a novel and comprehensive taxonomy of STIN simulation evaluation metrics as shown in Figure 4." |

### 13.2 涉及"负载过程/突发/时延/到达率/信用分配/决策成本"的表述（逐字 + 行号）

| 行号 | 逐字原文 | 归类 |
|---|---|---|
| 132 | "The network layer metrics focus on the end-to-end communication capacities for services in STIN scenarios, including **throughput, packet error rate (PER), end-to-end delay, delay jitter**, etc. Since multiple routes can be leveraged in an STIN, e.g., through the satellite segment or the ground segment, it would become more complex to evaluate the networking performance when multiple paths are involved." | **网络层评价指标的穷举**（吞吐/PER/时延/抖动） |
| 132 | "The evaluation metrics for specific network protocols and algorithms are also considered, e.g., the routing and load balancing algorithms, which include **the convergence time of routing protocols** and **the load balancing ability to avoid network congestion**." | **收敛时间与负载均衡能力被列为评价指标**（决策成本的度量口径） |
| 301 | "in a predefined way with the simulation scenario setup or following a **Poisson probability distribution with an arrival rate**. The traffic demand of each user is set to ..."（SatSysSim [75] 的描述） | **业务到达的 Poisson 分布 + 到达率**（`arrival rate` 与 `Poisson` 的唯一命中） |
| 427 | "the generated network traffic follows some empirical distributions or emulates some specific services, e.g, web browsing or live streaming" | **现有仿真器的流量生成方式：经验分布或特定业务模拟** |
| 130 | "Scalability is also a very important evaluation metric to evaluate whether the network can support large numbers of users in both satellite and terrestrial domains." | 可扩展性（用户规模） |
| 134 | "The physical layer metrics focus on the context of shared spectrum access (SSA) for both the satellite and terrestrial links. The wireless links can be interrupted by various factors, e.g., adversarial attacks or background noises." | 物理层指标与链路中断因素 |
| 136 | "The specific geometrical metrics include satellite constellation coverage, system redundancy, link duration, etc." | 几何指标（含链路持续时间） |
| 13（摘要） | "Simulation challenges arise with the fast growth of LEO mega-constellations, including frequent re-connection and handover, long satellite transmission delay, high dynamics of satellite network topologies, and the integ..." | 仿真挑战清单（含长传播时延、高动态拓扑） |
| 423 | "the network simulator should possess the ability to model the evolving network topology and evaluate the adapted network management schemes, e.g., new routing methods when the previous ones no longer work" | 拓扑演化建模 |
| 462 | "Five requirements are also listed and recommended when designing new STIN simulators from the perspectives of **fidelity, scalability, extensibility, agility, and real-time**" | 仿真器的五项设计要求（含 real-time） |

**关键判定**：本篇对本题的价值在于 **L132**——它把 **"路由协议的收敛时间"** 与 **"负载均衡能力（避免网络拥塞）"** 并列为标准评价指标。这是本批 13 篇中**对"决策成本应被度量"最制度化的一次表述**，可作为本库 T1/T2 论文评价体系缺口的对照基准。

### 13.3 负向声明核验（模式 / 实测计数 / 命中判定）

- 模式 `credit` → **实测计数 0**。
- 模式 `arrival process` → **实测计数 0**。
- 模式 `burst` → **实测计数 0**。
- 模式 `self-similar` → **实测计数 0**；`non-stationar` → **实测计数 0**。
- 模式 `arrival rate` → **实测计数 1**。
  - **命中位置与逐字**：L301 "...in a predefined way with the simulation scenario setup or following a Poisson probability distribution with an arrival rate. The traffic demand of each user is set to..."。
  - **判定**：该处是对**第三方仿真器 SatSysSim [75] 的流量生成方式**的描述（"或按 Poisson 分布以某到达率生成"），**不是该综述自身对负载过程的建模或主张**。故"该综述本身未给出到达过程模型"的判断成立，但需登记：**本篇是全 13 篇中唯一提到'仿真器可用 Poisson 到达率生成流量'的篇目**。
- 模式 `Poisson` → **实测计数 1**（同上 L301）。

### 13.4 它提到但本库其他论文未跟进的方向

1. **面向 AI 的网络仿真统一基准数据集（类比 ImageNet）**：450。本库无基准数据集论文；该文明确指出**实测流量数据因技术与政治原因难以获取**——与本库 T3 档测量类论文形成呼应。
2. **动态集成仿真（包级网络仿真器 × 天体动力学仿真器，非静态文件交换）**：419–421。本库无仿真平台论文。
3. **恶意与异常用户行为仿真（DoS/DDoS、阻塞、干扰、欺骗）**：427–431。本库无对应论文。
4. **网络仿真即服务（NEaaS）与云化大规模仿真平台**：433–444。本库无对应论文。
5. **AI 工具嵌入仿真器（免去用户配置 TensorFlow/PyTorch 环境）**：448。本库无对应论文。
6. **通导感一体化（navigation-sensing-communication integration）的专用仿真工具**：452–458。本库无对应论文。
7. **路由协议收敛时间作为标准评价指标**：132。本库 T1 论文普遍不报收敛时间（需 T1 档复核）。
8. **链路持续时间（link duration）作为几何层评价指标**：136。本库 T1/T2 论文较少把 link duration 单列（需复核）。

<!--APPEND-->



