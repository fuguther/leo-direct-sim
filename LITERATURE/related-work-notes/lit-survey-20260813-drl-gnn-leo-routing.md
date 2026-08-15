# 文献调研：动态拓扑、拥塞与部分/陈旧观测下的 LEO DRL/GNN 路由（2026-08-13）

调研问题：深度强化学习逐跳路由决策中，GNN/MPNN/GAT 等图表示如何融合节点队列、目的地信息、链路状态、传播距离、链路容量与信息年龄（AoI），以改善数据包完成率、goodput、平均/尾部时延与路由稳定性。

- 检索日期：2026-08-13；时间窗 2021—2026（奠基工作放宽至 2018 后；经典基线例外单列）。
- 来源：arXiv、IEEE Xplore、ACM DL、ScienceDirect、Springer、IET/Wiley、MDPI、Crossref、NASA ADS、dblp、高校机构库。
- 核验方式：每篇至少打开 arXiv/出版社页面一次，或经两个独立来源交叉核对；核不到的字段标"未验证"；引用次数一律不给。
- 本笔记是候选登记与筛选结论，不代表论文结论正确；引用前须按 `LITERATURE/README.md` 回到原文核对具体位置。

## 一、筛选结论

### 最相关 8 篇
1. **GraphPR**（Ran et al., IEEE TVT 2025, 10.1109/TVT.2024.3499933）——GAT+MADRL 逐包全分布式路由，POMDP，队列长度为核心指标，RSPH 防环。与本研究设定逐点对齐。
2. **RAoI/ADRLRM**（Gao et al., IEEE/ACM ToN 2026, 10.1109/TON.2025.3597928）——Routing-aware AoI 直接进 DRL 奖励 + Spatial-Temporal GNN。其 AoI 度量的是被转发数据新鲜度，非路由状态信息陈旧度。
3. **POMAP**（Li et al., IEEE IoT-J 2025, 10.1109/JIOT.2025.3610772）——POMDP + 排队论（G/G/1/K+AQM+优先级）+ MAPPO Pareto 多目标。S/A/R 细节未能从原文核实（付费墙）。
4. **Continual DRL**（Lozano-Cuadra et al., IEEE TCOM 2025, 10.1109/TCOMM.2025.3562522）——部分知识+拥塞自适应+模型陈旧（continual learning/model anticipation/联邦）。代码公开：github.com/SatCom-TELMA/MA-DRL_Routing_Simulator（仓库已验证存在）。本地有全文。
5. **GRLR**（Zhang et al., IEEE TVT 2025, 10.1109/TVT.2024.3471658）——GNN 特征提取 + Actor-Critic 分布式逐跳，mega 星座。常被后续工作当基线。本地有全文。
6. **RRS-DRL**（Chu et al., Electronics Letters 2023, 10.1049/ell2.12820）——LEO 逐跳 DQN，奖励含目的地距离 + 下一跳 AoI + 队列增长率。状态空间极简（无链路状态/邻居队列）。
7. **Chou et al. spatial-temporal routing**（arXiv:2605.02413, 2026，**预印本**）——状态=[本星队列+邻居链路时延+拓扑特征]，r=−(αD+βQ)、β>α，GAT+LSTM+DQN，直接以 GraphPR 为基线。仅 45 星，未经同行评审。
8. **Weil et al. recurrent message passing**（AAMAS 2024, arXiv:2402.05027）——唯一直面 "partial or outdated observations" 的 MARL 路由机制工作；**场景为通用有线图，非 LEO**。代码公开：github.com/jw3il/graph-marl。

### 建议精读 3 篇
GraphPR（最近邻 + 多方共同基线）、RAoI（ToN，AoI 机制正面对标）、Continual DRL（开源可复现，可作实验底座）。备选：Chou et al.（设计参照，预印本）、Weil et al.（陈旧观测机制）。

## 二、A/B/C 分类

- **A 直接相关（LEO+路由+DRL/GNN）**：GraphPR、RAoI、POMAP、Continual DRL、GRLR、CMADR（JSAC 2024）、RRS-DRL、Transformer-MIX（IoT-J 2025）、MATGCIR（Comm. Lett. 2025）、Rao et al.（IoT-J 2025）、GRL-RR（ComNet 2025，SDN 域控+链路权重，非逐跳）、GMR（TVT 2024，集中式多径 TE）、Q-routing（ICMLCN 2024）、GRouting（HotICN 2021，路径级动作）、DQN-LLRA（Remote Sensing 2023）、GNN+DQN（Appl. Sci. 2024，地面 NSFNet 训练）、DMR（Electronics 2024，集中式 TE）、Chou et al.（预印本）、Liaq et al.（arXiv:2605.04448，预印本）、DTAR（arXiv:2604.12382，预印本，域级抽象）、PRIMAL（arXiv:2510.27506，预印本）。
- **B 机制相关（部分观测/AoI/拥塞感知）**：Weil et al.（outdated obs）、LUR（IoT-J 2023, 10.1109/JIOT.2022.3229028，LEO AoI 优化派基线）、PRIMAL（异步决策+CVaR 尾部时延）、NGAT（arXiv:2404.18084，GAT+AoI 组播，非 LEO）、经典基线 ELB（ToN 2009, 10.1109/TNET.2008.918084）、TLR（TWC 2014, 10.1109/TWC.2014.041014.130040）。
- **C 方法基础（GNN+RL 路由，非 LEO 场景）**：Weil et al.（AAMAS 2024）、Almasan et al.（ComCom 2022, 10.1016/j.comcom.2022.09.029，edge-level MPNN + destination/action-conditioned 表示）、Bhavanasi et al.（TNSM 2023, 10.1109/TNSM.2023.3287936）、Manfredi et al.（WoWMoM 2021, 10.1109/WoWMoM51794.2021.00029，队列等待显式建模）、Wigmore & Modiano（MobiHoc 2025, 10.1145/3704413.3764422，平均+最坏时延）、备查 GROM（JNCA 2024）、GAPPO（PIMRC 2023）、SK-CFR（ComNet 2025）。

## 三、核验存疑与空白点

- 未验证：Rao et al.（IoT-J 2025）、MATGCIR、Federated GRL（WCL 2025）仅核对到书目，DOI 未验证；POMAP 的 S/A/R 细节未从原文提取。
- 冲突条目：Anti-Jamming Routing Based GNN（Xplore doc 11456689）venue 三来源互相矛盾（JSAC/TAES/IoT-J），未纳入，如引用以 Xplore 页面为准。
- 2026 预印本（Chou、Liaq、DTAR）未经同行评审，只作设计参照。
- **空白点**：未见把"邻居/链路路由状态信息本身的年龄"显式作为状态分量或分析对象的 LEO DRL 路由论文——现有工作要么用 AoI 度量被传数据（RAoI、RRS-DRL），要么用 POMDP/异步框架隐式消化信息滞后（Continual DRL、PRIMAL、Weil）。这是本研究的差异化空间（基于本轮检索，非穷尽性结论）。

## 四、候选详表要点（S/A/R 等细节）

完整逐篇字段（研究问题、场景、状态/动作/奖励、模型、机制覆盖、基线指标、代码、相关性、借鉴、局限）见 2026-08-13 会话记录；要点已登记进 `LITERATURE/SOURCES.csv` 对应行 notes/scope。逐跳路径级动作与集中式 TE 类（GRL-RR、GMR、GRouting、DMR、DTAR）在引用时必须与逐包逐跳类区分决策粒度。
