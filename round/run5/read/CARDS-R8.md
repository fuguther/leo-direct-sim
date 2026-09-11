# 读卡批次 R8

> 读法：子代理逐字通读全文（VM MinerU MD），行号对应 VM 路径 `/data/liguang13/topic-loop-r2/md/<KEY>/<KEY>/txt/<KEY>.md`。
> 批次：QGAREQUM QSNRQ8PF R37BNQQ8 R5QTFKD2 S2QZRBEJ SBCHGBCP T9X6QCLL TAUEF8PF TQF59BD7 TRM2HPFN TSV3IE8S（11 篇）。

## QGAREQUM — Boosting Reinforcement Learning with Strongly Delayed Feedback Through Auxiliary Short Delays

**1. 一句话**
给"观测延迟"型 RL 配一个"延迟更短"的辅助任务：在短延迟上先学一个容易学的 Q 函数 $Q^\tau$，再用它去 bootstrap 长延迟的 Q，从而绕开增广状态空间随延迟指数爆炸的问题（L30、L122-133）。

**2. 问题设定**
延迟分三类——观测延迟/动作延迟/奖励延迟（L13）；本文只做**观测延迟**，且限定为 "non-anonymous and constant observation delay under finite MDP"，延迟常数且 agent 已知（L13）。麻烦在于：观测延迟**破坏马尔可夫性**（L13 逐字："it disrupts the Markovian property of systems"），而增广法（把最近观测状态 + 延迟步的动作序列拼成 information state）虽能恢复马尔可夫性，却让状态空间随延迟指数增长、学不动（L15）；BPQL 用"零辅助延迟"的近似来省算力，代价是信息损失过大、随机任务上崩掉（L15、L137）。注意：这是**通用 RL 论文，与 LEO/卫星网络无关**，全文（含 L1-L884）未出现任何卫星/网络路由语境。

**3. 方法骨架**（不是网络路由 RL，是延迟 RL 的通用框架）
- 记号：原始延迟 $\Delta$，辅助延迟 $\Delta^\tau < \Delta$，增广态 $x_t=(s_{t-\Delta},a_{t-\Delta},\dots,a_{t-1})$（L78）；辅助增广态 $x_t^\tau$ 与 $x_t$ 共享子序列 $(a_{t-\Delta^\tau},\dots,a_{t-1})$（L131）。
- 桥梁是 **delayed belief** $b_\Delta(x_t^\tau|x_t)$，式(2) L128；**Remark 4.1 说不需要显式学 belief**——因为 CD-MDP 里每个状态最终都会被观测到，可从完整轨迹"合成"任意延迟的增广态（L131）。这是全文最关键的工程简化。
- 离散：AD-VI 的辅助延迟 Bellman 算子 $\mathcal{T}$，式(3) L157——**用 $Q^\tau$ 在辅助态上取值、用 $Q$ 在原始态上 argmax 选动作**；延拓到网络即 AD-DQN（L160）。
- 连续：AD-SPI，评价式(4) L167、改进式(5) L175、策略梯度式(6) L181；再加 n-step 值估计加速（L184）。
- 实现（附录 A）：同时维护两套网络 $(Q_\psi,Q^\tau_\theta)$，每步问两个网络各出最优动作，**再用 $Q^\tau$ 在两者间取 argmin（保守动作）**——作者说实验中 argmin 比 argmax 稳（L477、L490）。更新时以 0.5 概率二选一更新 $Q^\tau$ 或 $Q$（L496-502）。AD-SAC 同理维护两套 actor，双 critic 取 min（L481、L525-533）。超参表 L471：网络 [256,256]、lr 3e-4(actor)/1e-3(critic)、buffer 1e6、batch 256、n=3、$\Delta^\tau$=0（MuJoCo 确定性场景）。

**4. 它声称的效果**（基线 A-DQN / A-SAC / DC/AC / DIDA / BPQL）
- 玩具例 Fig 1（L28）：$\Delta=10$ 时 AD-QL(5) 在确定性下更快，但随机 MDP (p=0.1) 下"短延迟不一定好"，AD-QL(0) 反而掉点。
- 确定性 Acrobot：500k 步内 AD-DQN 明显快于 A-DQN（L307）；延迟扫 5–50 时，**A-DQN 在 20 延迟以后学不出有用策略，AD-DQN 到 50 延迟仍稳**（L307 逐字："A-DQN is not able to learn any useful policy after 20 delays... robust performance even under 50 delays"）。
- 随机延迟 MuJoCo（Table 2，L310）：AD-SAC 在 9 个任务上全面领先，含对 BPQL（例：Ant 0.69 vs BPQL 0.58；Humanoid 0.97 vs 0.40）。
- 随机 Acrobot（Fig 3(c)，L318）：**最优辅助延迟不规则**，"$\Delta^\tau=0$ 并不总是最优"。
- 随机 MuJoCo 50 延迟（Table 3，L323）：$\Delta^\tau_{best}$ 逐任务漂移（Ant=4, HalfCheetah=2, Hopper=5, Humanoid=0, Pusher=3, Reacher=1, HumanoidStandup=1, Swimmer=0, Walker2d=0）。
- 理论：定理 C.2（L766）给出 $I(x_t)=\frac{L_QL_\pi}{1-\gamma}\sigma\frac{\sqrt2}{\sqrt\pi}[\sqrt\Delta-\sqrt{\Delta^\tau}]$，即性能差随 $\Delta-\Delta^\tau$ 增大而增大——**样本效率与近似误差的显式 trade-off**（L787）。

**5. 它的实验条件**
- 基准：Acrobot（离散）+ MuJoCo 9 任务（连续）（L299）；随机化方式是**给动作叠加均匀噪声、概率 0.1**（L301、L314），随机延迟是"$\Delta=5$ 概率 0.9、$\Delta\in[1,5]$ 概率 0.1"（L314）。
- 训练/评估：**同一环境**，无跨分布测试；10 个随机种子（L303）；Acrobot 500k 步、MuJoCo 1M 步（L471）。
- 公平性处理：作者让所有方法总梯度步数相同，因此 AD-RL 里 $\pi$ 的训练次数只有基线的一半（L303）——**这条降低了自己主策略的更新量，是效果声明的一个隐含条件**。

**6. 它自述的局限**（第 9 节 "Limitations and Chanllenges"，L339-345）
- 逐字："the performance of AD-RL is subject to the selection of the auxiliary delays $\Delta^{\tau}_{best}$. Such selection is deeply related to the specific tasks and even the delay $\Delta$, and is highly challenging: Fig. 3(c) demonstrates that the relation between $\Delta^{\tau}_{best}$ and $\Delta$ is not linear or parabolic."（L341）
- 逐字："AD-RL implicitly represents the belief function by sampling in two augmented state spaces... leading to additional memory cost compared to conventional augmentation-based approaches."（L343）
- 逐字："While a longer auxiliary delay achieves better performance, it brings back the sample inefficiency issue, which will be investigated in the next step."（L345）

**7. 它没做但看起来能做的地方**（基于内容）
1. **$\Delta^\tau_{best}$ 全靠网格搜索手选**，作者自己承认关系"非线非抛物"（L341）——Table 3 的 9 个最优值散布在 0–5，这是现成的"超参自适应"缺口；文中的定理 C.2 恰好给了目标函数 $\sqrt\Delta-\sqrt{\Delta^\tau}$，却没拿它做自动选择。
2. **随机性强度 $\sigma$/$p$ 没有扫过**：全部实验固定在 p=0.1（L301、L314），而定理 C.2 里 $\sigma$ 是显式出现的系数——随机程度升高时 $\Delta^\tau_{best}$ 如何移动，无人测。
3. **延迟非平稳（随时间变化）的设定完全没做**：全文只做 constant delay（L13）与"固定分布的随机延迟"（L314），没有 delay 随时间漂移的场景，而 Remark 4.1（L131）的"事后合成增广态"恰好天然支持任意 $\Delta$ 变化。
4. 保守动作选择（argmin，L477/L490）是实验发现的经验技巧，没有理论或消融支撑其必要性。

**8. 和同批其他篇的关系**
与本批的 LEO 路由论文**基本无交集**：它是 ICML 系通用 RL 理论/算法论文，实验是 Acrobot/MuJoCo 控制任务，参考文献（L357-L463）全是延迟 RL、DDE、机器人控制、HVAC，**没有任何一篇 LEO/卫星/网络论文**，也未引用同批其他篇。方法谱系上它对接的是 BPQL(Kim 2023)、DIDA(Liotet 2022)、DC/AC(Bouteiller 2020) 这条"延迟 RL"线。与同批 LEO 论文唯一的抽象联系是"用陈旧/延迟信息做决策"这一母题。

**9. 对"负载变化下到达率/时延"的贡献**
**没有直接贡献**——全文无网络、无到达率、无排队、无时延指标（通读 L1-L884，实验指标只有 Acrobot/MuJoCo 的 normalized return）。唯一的**间接**价值是一个可迁移的形式化：它把"决策时观测到的状态是 $\Delta$ 步之前的"这件事写成 CD-MDP 并给出样本复杂度的代价（L78、L190-194），而 LEO 星上路由的陈旧拓扑/队列信息正是这个结构；但它既没有网络模型，也没有任何到达率-时延曲线。

**10. 一句话评价**
**把"延迟 RL"的增广法用"短延迟辅助任务 $+$ 隐式 belief"救活的通用算法论文**：理论完整（样本效率/性能差界/收敛，L190-293、L541-737），但与 LEO 卫星网络零接触，其"最优辅助延迟靠手调且不规则"的自述缺口（L341）才是它自己暴露的最大问题。

## QSNRQ8PF — Dynamic Routings in Satellite Networks: An Overview

**1. 一句话**
一篇 2022 年的卫星网络动态路由**综述**（Sensors 22(12):4552，MDPI），把单层（拓扑平面化/虚拟节点/虚拟拓扑）与多层（SDN 基/QoS 基/流量均衡）两类路由方案逐条梳理成表，并给出 ML、MEC、数字孪生、智能卫星四个未来方向（L11、L318-320）。

**2. 问题设定**
卫星网络拓扑高动态、星上算力/存储受限、星间链路时延相对大，导致地面路由协议不能直接搬用（L35 逐字："terrestrial network routing algorithms are not directly applicable to satellite networks due to their high complexity and processing requirements"）。作者把挑战归纳成五条（L109-119）：链路切换引起的重路由、高传输时延与高信道误码、星上算力存储受限、拓扑高度动态、**负载不均衡**。**注意：这是综述，不是新算法论文**。

**3. 方法骨架**
无算法，方法是**分类学 + 对比表**。骨架为四段：
① 系统模型与特征（第 3 节，L83-131）：单层/多层（GEO/LEO、MEO/LEO、GEO/MEO/LEO 三层的对比见 Table 3 L99）；关键使能技术为星间激光/太赫兹、快照序列路由、星上处理 OBP/OBS/OBR、ISL、动态网络切片（L123-131）。
② 单层路由三条技术路线（第 4.1 节，L149-192）：拓扑平面化（Table 4，L164）、虚拟节点（Table 5，L175）、虚拟拓扑（Table 6，L188）。
③ 多层路由三条路线（第 4.2 节，L194-277）：SDN 基（Table 8，L231）、QoS 基（Table 9，L244）、流量均衡（Table 10，L267）。
④ 性能横向矩阵：Table 7（单层，L191）与 Table 12（多层，L276）按"时延/丢包率/计算开销/吞吐"四列给方案打勾。
**这里有一处我没读懂**：Table 7 与 Table 12 的勾叉矩阵在 MinerU 转换后已被压成乱码字符串（如 L277 的 `X/××X//×//×/×//××//V×/`），无法还原逐格取值，因此"哪个方案在哪项指标上被判定为优"我读不出来。

**4. 它声称的效果**
综述无自设实验，只有对**被引工作**的数字转述，例如：某算法"可节省 30% 卫星链路容量"（L54）；某蚁群 QoS 算法的"平均时延以秒计、路径时延抖动以毫秒计、每路径丢包率仅 0.11%"（L242）；GRU+GNN 分布式智能路由"相对最短路达到 98% 精度、15 次迭代内收敛"（L287）。这些数字出自原文，本文**未复现、未统一口径**。

**5. 它的实验条件**
**没有实验**——这是文献综述，不设拓扑、规模、负载，也没有训练/评估之分。所有"实验条件"信息只能追到被引原文（第 438-707 行的参考文献表，共 135 条）。

**6. 它自述的局限**（逐字）
- 对领域整体：L281 逐字——"Although, there are a variety of multi-layer satellite network routing protocols and algorithms, as previously described, **systematic routing algorithms are still lacking**."
- 对 ML 路由的可扩展性：L316 逐字——"**Existing ML routing algorithms handle small topological networks with up to 20 satellite nodes.** A larger topology means an exponentially growing number of network states and a greater difficulty in routing decisions."
- 对 SDN 类方案的可迁移性：L229 逐字——"the routing optimization algorithms in this subsection apply only to one satellite network model and no other constellation model in the longer term."
- 对智能路由的落地：L316 逐字——"intelligent routing algorithms are still difficult to deploy at scale in existing satellite network architectures"。

**7. 它没做但看起来能做的地方**（基于内容）
1. **Table 7 / Table 12 的勾叉矩阵没有被换算成分数或统计**：作者手里有一张"方案 × 指标"的二维表，却只停在定性打勾，没有做"哪类指标被研究得最少"的计数——这正是它自己列的缺口（L281 说缺 systematic）。
2. **时延口径没有分层对齐**：它自己在 Table 11（L273-274）里把时延拆成物理层（信号/传播）、数据链路层（切换/拥塞控制/重传）、网络层（切换/IP 移动性/路由算法），但 Table 7/12 的"Time Delay"列是单一格子，**分层拆分与横向对比矩阵没有打通**。
3. **负载维度没有成为分类轴**：全文反复出现"负载不均衡"（L119、L253）与"高负载"（L186），但方案的分类按技术手段（SDN/QoS/流量均衡）而非按"在什么负载区间有效"——第 259 行它自己承认流量均衡算法"只在不过载时表现更好"，这条本可做成一条负载-收益曲线。

**8. 和同批其他篇的关系**
它是本批的**地图**：把同批 DRL 论文所引用的经典对照全部点名——ELB（参考文献 [94]，L626）、TLR（[95]，L628）、LCRA（[38]，L514）、DCCR（[53]，L544）、DTBR（[50]，L538）、排队状态路由（[104]，L646），以及被当作"逐包 DRL 代表"的 DRL-ER（[134]，L706）。与 QGAREQUM 那种通用 RL 论文**完全不像**（一个是领域综述，一个是控制任务上的算法）。它不引用同批其他篇（2022 年截稿，批次里多数论文晚于它或同期）。

**9. 对"负载变化下到达率/时延"的贡献**
**本批里与这个主题最直接相关的一篇**，但贡献是**定性的**：
- 给出 LEO 星间链路传输时延量级：**LEO 之间 15–25 ms，MEO 之间 40–60 ms**（L113）——这是全批少见的硬数字。
- 把"负载变化"写成独立挑战（L119 逐字："Geographical conditions, satellite motion, and the Earth's rotation characterize the time-varying nature and **uneven distribution of load traffic** in satellite networks"），并指出一个关键的**非单调机制**："even if the ISL has sufficient resource capacity at the time of establishment, the change in link load traffic can cause network congestion, preventing the link from switching"（L119）——即**建链时的余量不能保证链路可用**。
- 记录了一条负载依赖的适用边界（L259 逐字）："such routing algorithms perform better only when the traffic is not overloaded"。这意味着"负载均衡路由的收益随负载升高而消失"，但**没有给拐点数字**。
- 时延分层表（L273-274）指出网络层时延包含"切换时延 + IP 移动性管理 + 路由算法"，为"时延从哪来"提供了拆解口径。
**缺口**：全篇没有到达率（pps/λ）这一根轴，没有排队模型，没有"负载 → 时延/丢包"的曲线。

**10. 一句话评价**
**一张 2022 年的领域地图，不是新方法**：价值在于它把"负载不均衡"明确列为卫星路由的独立挑战（L119）并给出跨层时延拆解（L273-274），且自己承认 ML 路由只做到 ≤20 节点（L316）；但它的对比矩阵停在定性打勾（且该表在 MD 里已损坏），无法支撑任何定量结论。

## R37BNQQ8 — SDN-Based End-to-End Fragment-Aware Routing for Elastic Data Flows in LEO Satellite-Terrestrial Network

**1. 一句话**
在 SDN 统一管控的"LEO 星座 + 地面网"一体化网络里，把业务流建成"有保底带宽 CRB 与峰值带宽 MSB 的弹性流"，用蚁群启发式（ACO-EFPC）在"卫星段 + 星地链路 + 地面段"三类链路上选端到端路径，目标是同时压时延、波长碎片、总分配带宽和负载不均衡（L21、L45、L195-198）。

**2. 问题设定**
现有 ISTN 路由研究基本只做卫星网内部路由、把地面网当附属并通过**预先指定**的星地链路衔接（L33 逐字："most researches on routing mainly focus on the limitation of one network of ISTN... and coordinate the two types of networks through the specified gateway between them"）。作者指出两个新特征使老办法失效：①三类链路（ISL / STL / 地面光纤）**动态性、容量、时延、碎片约束各不相同**；②星地之间是"点对区"覆盖，一颗星可连多个地面站、一个地面节点可连多颗星，因此存在**大量潜在 STL**，且随地球自转与星座周期变化（L39-43）。同时业务流是"弹性的"（L31 逐字："the data flow in LEO is fluctuating, which means the data flow requires a basic fixed bandwidth and a shared bandwidth, which we call them elastic bandwidth requirements"）——按固定带宽预分配会浪费资源或降级业务。

**3. 方法骨架**（**非 RL**，是蚁群启发式 + SDN 集中式路径计算）
- 网络建模：$G(t)=G_s(t)\cup G_t\cup E_{st}(t)$（式1，L95），卫星网/地面网/星地链路三部分；ISL 为 IP/MPLS over WDM，容量 $B_s=\sum_{i=1}^{W}\lambda_i^s$（式2，L103）；STL 为 Ka/Ku 多波束，$B_{st}=\sum_{i=1}^{U}\lambda_i^{st}$（式3，L111）。
- 弹性流模型（式4-5，L136-144）：$f_i(t)=[T_b^i,T_e^i,S_i(t),D_i,B_c^i,B_m^i]$，其中 $B_c$ 是必须保障的 CRB、$B_m$ 是 MSB；链路上的需求带宽 $q_{ij}(t)=\upsilon_{ij}(t)+\tau_{ij}(t)$，即"CRB 之和 + 共享弹性带宽之和"。
- 优化目标（式8，L198）：$\Theta(t)=\omega_1 l(t)+\omega_2 F_r(t)+\omega_3\sigma^s(t)+\omega_4\mu^s(t)+\omega_5\eta(t)$ —— 分别是**时延因子、波长碎片率、分配带宽方差、极差（max-min）、MSB 超用因子**。作者明确 σ 管"整体均衡"、μ 管"避免最差链路"（L209）。被判为 NP-complete（L215）。
- **没读懂：式(9)**（L204）——该式本应给出 $l(t),F_r(t),\sigma^s(t),\mu^s(t),\eta(t)$ 的具体算式，但 MinerU 输出已退化成重复的 $\mathbf{x}_t^{\prime\prime}$ 乱码，无法还原。我只能从 L209 的散文推断各因子含义。
- 蚁群主干（第 IV 节）：转移概率由五项相乘（式12，L238）——信息素 $\tau_{ij}^k$、时延因子 $d_{ij}^k$、**拥塞因子 $\eta_{ij}^k$（支持业务后的剩余带宽占比）**、**碎片比 $\upsilon_{ij}^k$**、MSB 超用因子 $\rho_{ij}^k$（式11，L238），且**三类链路的五个指数各取一套值**（式13，L244）。信息素更新式14（L257），用 $\tau^k_{ij}(t)=1-\Theta_k(t)/\max_i\Theta_i(t)$ 奖励代价小的蚂蚁。
- 工程简化：**蚂蚁一旦进入地面网就停止搜索，剩余路径交给 Dijkstra**（Algorithm 1 Step7-9，L284-288、L303），以省算力。
- 两个子算法：Algorithm 1 处理新到流（L270-299），Algorithm 2 处理在传流——仅在源切换或原路径失效时才重算（L305-331）。全部路径计算在服务器侧完成，再下发物理网（L333）。

**4. 它声称的效果**（基线：**SADR**[22] 与"用同一套因子的 Dijkstra"）
- 容量：多潜在 STL 的一体化场景比"单一指定 STL"的传统场景，**被接受业务数高 24.48%–80.15%**（L372）。
- 时延：150 流时时延比 Dijkstra 低 **7.52%**；Dijkstra 收敛慢，第 10 个虚拟拓扑之后仍比 ACO-EFPC 高 **3.42%**（L389）。
- 碎片：150 流时比 Dijkstra 少 **18.24%**、比 SADR 少 **8.22%**；跨负载平均比 Dijkstra 少 23.58%、比 SADR 少 19.78%（L398、L406）。
- 弹性带宽：比 Dijkstra 少 **26.22%**、比 SADR 少 **16.32%**（150 流）；跨负载平均少 10.23% / 9.23%（L410、L418）。
- 负载均衡（已分配波长数的方差）：比 Dijkstra 低 **16.72%**、比 SADR 低 **3.65%**（L427）；跨负载 16.55% / 3.49%（L437）。
- **最关键的一条（负载依赖）**：作者自述"the ACO-EFPC has got an advantage in bandwidth fragment, bandwidth utilization, and load balancing, **only with little inferior in latency while network load is high**"（L439，摘要 L21 亦重复）。

**5. 它的实验条件**
- 星座：Iridium-like 极轨 π 星座，**66 星 / 6 轨道面 × 11 星**，倾角 86.4°，高度 780 km，相位因子 0，ISL 2 条同轨 + 2 条异轨、**非永久**、无跨缝链路，仰角 8.2°（Table 1，L344）。
- 地面网：CERNET 骨干网参数，主要节点设地面站（L346、L351）。
- 容量：ISL 单波长 800 Mbps × 3 波长 = **2400 Mbps**；STL 单波束 960 Mbps × 3 波束 = **2880 Mbps**（Table 2，L354，参考 LeoSat[10]）。
- 时延模型：链路时延在一个时间片内视为**静态**（取区间最大值，L181、L360）；节点**处理时延固定 100 μs**（L358）。**注意：没有排队时延项**。
- 业务：**300 个弹性流请求**，一端全球随机、一端在地面网；MSB 与 CRB 服从均匀分布，均值 150 Mbps / 75 Mbps（L370）；投入 **20 个连续时间片**；用 MATLAB 仿真（L364）。
- **负载扫描**：服务数从 **30 到 180，步长 30**；作者说明 180 是 ISTN 容量的上限（L378）。
- 对比方法：SADR 与"同因子 Dijkstra"，**因子权重完全相同**（L376）。
- 无训练环节（启发式），因此"训练/评估同不同套"不适用。

**6. 它自述的局限**（逐字）
- L439："the ACO-EFPC has got an advantage in bandwidth fragment, bandwidth utilization, and load balancing, **only with little inferior in latency while network load is high**."
- L439 同一段："**Though we do not simulate the ACO-EFPC in every time slice**, the corresponding indicators are statistically advantageous."
- L181："As the dynamic of the topology, the ISTN **cannot guarantee the stable latency**, so we suppose that the ISTN should provide the best effort on latency. Meanwhile, we suppose the latency is fixed and equals the maximum value of the interval in each slicing time."
- L157："we suppose that the terrestrial network **can satisfy the traffic of data flows in ISTN without any constraint besides latency**."
- L378（作者主动补做负载扫描的理由）："it is the situation that only reflect the performance of the fixed load as 150 services, and **cannot fully explain the superiority of the algorithm under various utilization of the network**."

**7. 它没做但看起来能做的地方**（基于内容）
1. **五个权重 $\omega_1..\omega_5$ 是固定常数**（L198、L376 说对比方法"same weight of factors"），但结果偏偏显示优势/劣势**随负载翻转**（低负载时 SADR 时延更好、180 流时被反超，L394）——负载自适应权重是现成缺口，作者已用数据证明翻转点的存在却没做机制。
2. **时延模型里没有排队时延**：只有传播时延 + 固定 100 μs 处理时延（L358），而它的拥塞因子 $\eta_{ij}^k$ 用的是"剩余带宽占比"（L231）。这使"高负载时延延劣"只能来自**路径变长**（可用链路被占），而非排队——把排队时延显式建进代价函数是最直接的下一步。
3. **负载轴用的是"流数"而非到达率**：30–180 是**并发服务数**，不是 λ（L378）。同一组数据换一个自变量就能得到"到达率 → 时延/阻塞"曲线。
4. **阻塞只在容量实验里出现**（L372 的 accepted services），性能对比部分所有流都被接受（"the transport path of the flows will not interrupt until the original path is unavailable"，L376）——**阻塞率与性能指标没有在同一张图上对齐**。
5. 蚂蚁进地面网即交接 Dijkstra（L303）是一个未经消融的工程折衷。

**8. 和同批其他篇的关系**
它属于**启发式/优化**谱系，与同批 DRL 论文（FDR-MARL、DRL-ER 那一支）**不像**：没有状态/动作/奖励，靠蚁群信息素在线迭代 + SDN 集中计算。与 QSNRQ8PF 那份综述是"被收录对象"的关系：本文的基线 SADR 正是综述里的 [77]（QSNRQ8PF L592），本文引用的 LCRA[20] 也是综述里的 [38]（QSNRQ8PF L514）——两篇通过这几条经典工作间接相连。与 QGAREQUM 完全无关（一个网络优化，一个控制 RL）。

**9. 对"负载变化下到达率/时延"的贡献**
**本批目前最直接的一篇**，给出三条可用的实证事实：
- **有明确的负载扫描**（30→180 并发流，步长 30，L378），且作者说明 180 是容量上限——这是"负载接近饱和"的锚点。
- **不同算法的差距随负载收缩**（L394 逐字）："When the number of flow requests is small (lower load), the data flows have more free paths to select, as the load increases, the data flows have fewer paths to choose from because of the block of part of the links in ISTN. Thus, as the number of flow requests increases, **the gap between different algorithms will be smaller and smaller in statistical**." 并在 **180 流处发生时延交叉**（ACO-EFPC 反超 SADR，L394）。
- **算法优势是分指标的、且方向随负载反转**：碎片/带宽/均衡全负载占优，时延仅**高负载**时略劣（L439、L21）。
**但它对"时延"的刻画有结构性缺陷**：没有排队时延项（L358），所以这里的"高负载时延"不能当作拥塞时延的证据。

**10. 一句话评价**
**把"弹性带宽流 + 多潜在星地链路"这一 ISTN 特有问题形式化，并用蚁群启发式求解的工程型工作**；它的真正价值不在蚁群本身，而在它无意中给出的"**算法优劣随负载发生方向反转**"这条实证（L394、L439）——但因为它没有排队时延模型，这个反转还只是路径结构效应。

## R5QTFKD2 — Age-Optimal Sampling and Routing under Intermittent Links and Energy Constraints

**1. 一句话**
把"什么时候采样"和"走哪条路"合成一个决策：在 N 条异构路径（部分时断时续、时延分布各异、能耗不同）上，最小化接收端的**长期平均 AoI 惩罚**（可为任意单调非减函数），并证明最优策略是"阈值式"结构，再用一个不做状态离散化的 Bisec-REAVI 算法算出来（L5、L32-34）。

**2. 问题设定**
面向卫星—地面一体化（TN-NTN）场景：**路径（route）而非逐跳转发**——源采样后选 N 条路中的一条送到监视端（Fig.1，L22、L40）。麻烦在于：①地面链路易受拥塞/覆盖空洞影响但通常低时延、稳定；②非地面链路（卫星）**间歇可用**——轨道几何、波束/足迹切换、网关重关联、ISL 重构都会把服务切成可用/不可用epoch，雨衰（Ku/Ka）、云冰水、电离层扰动、地磁暴还会造成 SNR 抖动甚至中断，即使物理可用期也会有随机接入碰撞与波束调度造成的突发性（L24）；③各路径时延可能是**相关的**（共享基础设施/频谱/可见性），且能耗按路径不同（L26）。作者要在"及时性 vs 能耗"之间做联合优化。

**3. 方法骨架**
- 路径分类：持续可用 $\mathcal{R}_\infty$（$p_k=1$，光纤/蜂窝，且假设非空以保证基线连通）与时断可用 $\mathcal{R}_{<\infty}$（$0<p_k<1$，卫星链路）（L46-48）。可用性是**逐 epoch 独立同分布的伯努利**（L218）。
- 时延：$\mathbf{Y}_i=(Y_{i,1},...,Y_{i,N})$ 取自平稳多元分布 $\mathbf{Q}$（允许跨路径相关）（L52）。**Remark 1（关键）**：因为每次投递后系统状态复位、且只能观测到被选中路径的实现，跨路径相关结构**不提供可利用信息**，最优策略只依赖边缘分布 $\{Q_k\}$（L60 逐字："the joint correlation structure does not provide exploitable information for future epochs... the potential correlation between unselected routes does not impact the achievable optimal age"）。这一条把"相关时延"这个卖点自我消解了。
- 能耗：采样固定成本 $C_s$，传输按路径的**单位时间**成本 $G_k$，长期平均约束 $E_{\max}$（式2-3，L73-85）；非抢占、generate-at-will、收到 ACK 后才生成下一个样本（L80）。
- 年龄：$\Delta(t)\triangleq t-S_i$（式4），惩罚 $f(\cdot)$ 为**连续单调非减**，可线性/指数/对数（L98）。
- 求解链路（第 III 节）：分数目标+分数约束 → 分数约束线性化（式9，L157）→ **Dinkelbach** 转成参数化 CMDP 序列（式10，L165）→ **拉格朗日**乘子 $c$ 把 CMDP 降为标准 MDP（式11，L175）→ 平均代价 MDP $\mathcal{M}(\lambda)$（L202）。
- MDP 三元组：**状态** $\mathcal{S}=[0,\infty)\times\{0,1\}^N$（连续分量 = 上次观测到的时延 $y$，离散分量 = N 条路的可用性向量 $\mathbf{l}$，L204）；**动作** $(R_i,Z_i)$ = 选路 + 等待时长（混合动作空间，L210-212）；**单步代价** 式14（L223）。
- **结构结果（Theorem 1，L238-274）**：(i) 在 Expected Penalty Ordering 条件（式15：$\mu_j\ge\mu_k \Rightarrow \Psi_j(y)\ge\Psi_k(y)\ \forall y$，L243）下，**最优选路是 $y$ 的单调阶梯函数**（式16），阈值至多 $\binom{N}{2}$ 个（L567）；(ii) 对**任意**单调非减 $f$，最优等待是**目标阈值式**：$Z_i^\star=(\beta^\star(R_i)-Y_i)^+$（式17），其中 $\beta^\star(R_i)=\inf\{t\ge0: \mathbb{E}_Y[f(t+Y_{i+1})]\ge\lambda^\star+c^\star E_{\max}\}$（式18，L271）——即"等到投递时刻的期望惩罚触及临界系统代价 $\lambda^\star+c^\star E_{\max}$"。
- Lemma 2（L317）：$\beta^\star_k(\mathbf{l})<\tau_k(\mathbf{l})$——**等待阶段总在"换路变优"之前结束**。
- Lemma 3（L336）：$f(0)\le\lambda^\star\le\min_{k\in\mathcal{R}_\infty}(\cdots)=\lambda^u$，界被用作二分搜索的初始化（L328）。
- **算法 Bisec-REAVI（Algorithm 2，L447-493）**：三层嵌套——外层对 $c$ 二分以满能耗约束、中层对 $\lambda$ 二分（Dinkelbach 根）、内层 REAVI 不动点。核心技巧是把不可数状态 $\mathbb{R}^+$ **消掉**：定义 REAV 函数 $G(r;\lambda,c)\triangleq\mathbb{E}_{Y\sim Q_r,\mathbf{l}\sim p}[W^\star(Y,\mathbf{l};\lambda,c)]$（式29，L384），最优性方程变成**在有限路径集 $\mathcal{N}$ 上的不动点**（式30，L390）。作者声称这是首个**不做离散化**就能解混合状态 CSMDP 并保持结构最优性的算法（L32）。对比：朴素 RVI 需网格离散、复杂度 $\mathcal{O}(|\mathcal{N}|M^2)$ 且引入量化误差（L365）。
- **机制上的关键假设**：$Y_{i+1}$ 与 $\mathbf{L}_{i+1}$ 条件独立，且**时延分布只依赖所选路径、可用性过程独立于历史**（L216-218）——即**时延是外生的、与负载无关**。

**4. 它声称的效果**（基线：MAD-Optimal、MAD-Zero Wait、Route X-ZW、Route X Optimal）
- 非线惩罚（Table II，L667）：$\alpha=1$ 时最优策略代价 4.482，单路最好 11.031 → **降幅近 60%**（L704）。
- 鲁棒性（$\mu_1\pm10\%$，L712）：$\alpha=1$ 且 Route 1 退化（$\mu_1+10\%$）时，Route 1 的**独立代价是 Route 2 的 3 倍以上**，但联合策略仍比只用"更好"的 Route 2 降低 **37% 以上**。
- 饱和阈值（Table III，L693）：$Y_{cap}$ 从 50 增到 400，单路相对最优的代价比从 2.46× 升到 4.11×；$Y_{cap}=400$ 时最优策略相对单路基线**降低超过 75%**（L716）。
- 能耗（Fig 5，L722）：无约束联合最优的能耗 $E=4.14$ **高于**两条单路各自无约束最优（$E_1=3.4$、$E_2=2.75$）——因为避开低时延区选路后平均等待变短、发送更频繁。
- **反直觉发现（作者自称为核心 insight，L36、L736）**："routes with higher mean delay, greater variance, or lower availability can still contribute to minimizing AoI"。
- 严格能耗下（L724）：Route 2 传输成本是 Route 1 的 **6 倍**（$G_2=18$ vs $G_1=3$），却成为 $E_{\max}$ 小时的**唯一选择**——因为高方差路径需要长等待，自然降低了平均发送频率、降低了平均功率。
- 能耗极低时：动态选路相对最佳单路**无可辨识收益**（L726）。
- 可用性（Fig 6/7，L732）：相对 MAD-Optimal 的优势在**低可用性区（小 p）缩小**；当 Route 1 时延特性更差时，两条策略的分岔出现在更大的 p。

**5. 它的实验条件**
- 规模很小：**2 条路（L685、L689）或 3 条路（L662、L698）**，不是星座级仿真；没有 ISL 逐跳、没有拓扑。
- 时延分布：**LEO 卫星路用对数正态**（式48-49，L638-650）；**地面路用 Gamma**（式50-51，L658-672）。参数来自教科书 [36]，非实测。
- 惩罚函数：截断指数 $f(\Delta)=a(\min(e^{\alpha\Delta},e^{\alpha Y_{cap}})-1)$（式52，L680）。
- 场景一（超竞争两路）：$\mu_2=0.1,\sigma_2=6.05$ Gamma；$\sigma_1=3.7$ 对数正态；$\mu_1$ 按每个 $\alpha$ 调到"两路统计上势均力敌"（L685），并做 $\pm10\%$ 敏感性。
- 场景二（能耗）：两路均常可用，线性 AoI，$\mu_1=5,\sigma_1=1$ 对数正态 / $\mu_2=1,\sigma_2=7.3$ Gamma，$G_1=3,G_2=18,C_s=2$，$E_{\max}\in[1,5]$（L689）。
- 场景三（可用性）：$N=3$，Table I（L662）——Route 1 = (Gamma,6,2,1) 常可用，Route 2 = (Log-normal,5,4,p)，Route 3 = (Gamma,3,7,p)，$p$ 为扫描变量。
- 作者明确说明三类因素（非线惩罚、能耗、可用性）是**分开单独分析**的，并给出理由（避免混淆；避免与"永远可用单路基线"比较时收益被任意放大）（L573-577）。
- 无训练环节（解析/迭代求解），故"训练/评估同套"不适用。

**6. 它自述的局限**（逐字）
**没有独立的 Limitations 章节**；以下是我读到的自认边界：
- L260 Remark 2："For general convex functions $( \mathrm{e.g.}, f(\Delta)=\Delta^2 )$, this monotonicity is **not guaranteed** due to the coupling of current age with higher-order delay moments."（即单调阶梯式选路结构**不保证**一般凸惩罚成立）
- L573："we analyze the impact of non-linear age penalty functions, energy constraints, and stochastic route availability **in isolation**."（三个因素未联合测试）
- L726："in this low-energy regime, **the dynamic routing policy offers no discernible benefit** over the best single-route strategy."
- L732："it may be beneficial to apply the proposed MAD-Optimal policy (smaller complexity) in cases where the routes in $\mathcal{R}_\infty$ are uncompetitive and routes in $\mathcal{R}_{<\infty}$ have low joint availability"（承认在低可用区可以用更简单的策略替代）
- L601："This policy can be undesirable over simpler policies like route k-Zero Wait."

**7. 它没做但看起来能做的地方**（基于内容）
1. **时延是外生的、与负载无关**：$Q_k$ 平稳且给定，且 MDP 转移里 $\mathbb{P}(Y_{i+1}|R_i=r)$ 只依赖路径（L216、L52）。它自己在动机里提到地面路的可靠性"is susceptible to **network congestion**, coverage holes"（L19），但模型里没有任何拥塞/到达率项——**把时延改成负载的函数**是最自然的下一步，而且会直接改变"低时延路永远优先"的结论。
2. **可用性是 i.i.d. 伯努利**（L48、L218），而它在动机里逐字列出的中断来源（轨道几何、波束切换、ISL 重构）**恰恰是高度可预测或强时间相关的**（L24）。用马尔可夫 on/off 或轨道确定性模型替代 i.i.d. 伯努利，是这个模型最明显的失真点。
3. **只有 2–3 条路、无逐跳**：与真实 ISTN 的"卫星段 + 星地链路 + 地面段"多跳结构差得远（对比 R37BNQQ8 的场景）；把每条"路"展开成多跳路径、并让每跳的可用性/时延耦合，是自然的扩展。
4. **Remark 1（L60）删掉了它自己引入的相关性卖点**：既然结论是"相关结构无信息量"，那么"何时相关性才会变得有用"（例如状态不复位、或能观测到未选路的实现）就是一个明确的开放问题。
5. 能耗约束是**长期平均**（L66、L117），没有瞬时/电池状态约束——对真正的能量受限平台（作者提到太阳能卫星、电池地面终端）偏弱。
6. 论文自述在 $\alpha$ 大时收益更大（L704），但 Table II 里 $\alpha=0.1$ 时最优 1.5748 vs 单路 1.844/1.827，收益仅 ~14%——**没有刻画"什么时候不值得做联合优化"的判据**（L732 只给了可用性维度的一条经验）。

**8. 和同批其他篇的关系**
- 与 **R37BNQQ8** 同属"ISTN/SDN 一体化 + 端到端路径选择"，但**方法谱系完全不同**：R37BNQQ8 是蚁群启发式 + 集中式 SDN，本文是不做离散化的**精确结构化 MDP + 二分**；R37BNQQ8 优化的是时延/碎片/带宽/均衡的加权和，本文优化的是 **AoI 惩罚**且带长期能耗约束。
- 与 **QSNRQ8PF**（综述）：本文的"间歇可用性"正好对应综述里"Highly Dynamic Network Topology"与"Unbalanced Load Traffic"两条挑战（QSNRQ8PF L117、L119），但本文把它抽象成伯努利 $p_k$，丢掉了负载维度。
- 与 **QGAREQUM**：都做"延迟/年龄下的决策"，但 QGAREQUM 是通用 RL 算法论文（观测延迟），本文是通信网络的排队/年龄优化论文，**互不引用**。
- 它是同批里唯一把 **AoI** 当核心指标的。

**9. 对"负载变化下到达率/时延"的贡献**
**没有直接贡献，而且要说清楚为什么**：全文没有到达率、没有排队、没有负载——数据是 generate-at-will 单包在途、非抢占（L80），路径时延是**给定的平稳分布**（L52、L216）。所以它给不出任何"到达率 ↑ → 时延 ↑"的事实。
**但它贡献了两条与"负载-时延"间接相关、值得记下的事实**：
（a）**指标层面**：L13 逐字指出 AoI "Distinct from traditional latency... Maintaining a low AoI requires both sufficiently frequent updates and low-latency delivery, thus **coupling throughput and delay** in a novel performance metric"——如果选题的因变量是"时延"，本文提示存在一个把吞吐与时延耦合起来的替代口径。
（b）**路径排序层面（最有价值的一条）**：**平均时延最小的路径不一定是最优路径**。因为高方差路径允许更长的等待，从而降低发送频率、节省能量（L724），所以"高均值/高方差/低可用"的路仍可能被选中并带来大幅收益（L36、L712、L736）。这条结论在**负载升高**时尤其值得警惕：若真把时延改成负载的函数，均值排序会随负载漂移，而本文的 $\beta^\star$ 阈值机制恰好提供了"按当前年龄自适应换路"的工具。

**10. 一句话评价**
**把经典 age-optimal sampling（Sun et al. 2017）推广到"多异构路径 + 间歇可用 + 能量约束"的理论工作**：结构定理干净（阈值式采样 + 至多 $\binom{N}{2}$ 个选路阈值），Bisec-REAVI 免离散化是真贡献；代价是完全外生的时延模型（无负载、无排队、可用性 i.i.d.），因此它离"负载变化下的到达率/时延"这条线**只差一个它自己没建的拥塞项**。

## S2QZRBEJ — A First Look at Starlink Performance

**1. 一句话**
一篇纯实测论文（IMC 2022）：在比利时一个固定站点上连续数月测量 Starlink 的**空载 vs 负载**时延、丢包、吞吐与网页 QoE，并用 QUIC（绕开 TCP PEP）把"负载下 RTT/丢包怎么变"单独量了出来（L33、L59）。

**2. 问题设定**
LEO 星座（Starlink，当时 2000+ 星）作为新出现的接入技术，其真实运行表现未被充分研究（L59）；唯一可比的是 Kassem et al. [34]。作者关心的是：**单一观测点访问全球分布式资源时，在高负载/重负载下用 TCP 和 QUIC 会看到什么**（L59）。动机里点明传统 GEO SatCom 的最小往返时延约 600 ms（L57），而 Starlink 承诺约 20 ms 时延、100–200 Mbps（L59）——需要独立核实。

**3. 方法骨架**（**无算法，是测量学**）
- 测试床三台 PC（L67）：PC-Starlink（常规 Starlink 订阅）、PC-Wired（校园 1 Gbit/s）、PC-SatCom（GEO 转售，下行 ≤100 Mbit/s、上行 ≤10 Mbit/s）；拥塞控制均为 Cubic，TCP 接收窗口内核默认。
- **QUIC 是核心工具**：QUIC 报文加密认证、**无法被 PEP 优化**，因此测到的是真实端到端时延；且 QUIC 的包号机制能把**每一个丢包**精确定位、把重传与原包区分开（L69）。两类流量：(i) 100 MB HTTP/3 批量传输；(ii) 轻量消息流——每秒 25 条、每条 5–25 kB，持续 2 分钟，平均码率仅 3 Mbit/s，**远低于链路容量**（L69）。下载/上传各占一半。
- 时延：ping 11 个锚点（7 个 RIPE Atlas 位于欧洲/北美/亚洲 + 4 个比利时志愿者节点），每 5 分钟 3 次 ping（L71）。
- 丢包：下载看客户端 QUIC 收到的包号缺号，上传看服务端返回的 ACK 帧（L118）。
- 吞吐：Ookla SpeedTest CLI，每 30 分钟一次（L78）。
- 网页：BrowserTime 自动访问比利时 top-120 网站，每 30 分钟随机 30 个，取 **onLoad** 与 **SpeedIndex** 两个与 QoE 相关的指标（L80）。
- 中间盒：traceroute + Tracebox 查 PEP；用 **Wehe** 检测流量歧视（TD）（L183-185）。

**4. 它声称的效果**（基线：GEO SatCom 与校园有线网）
- 空载时延：本地锚点中位 RTT **46–52 ms**，95 分位 <70 ms，最小 **20.5 ms**（验证 20 ms 承诺）；德国探针中位 42 ms；旧金山中位 184 ms、新加坡中位 270 ms（L96）。
- 5 个月趋势平坦：欧洲锚点中位稳定在 **~50 ms**（25 分位 40 ms、75 分位 60 ms），最小值约 20 ms（L105）。
- **无昼夜规律**，作者据此推断基础设施**利用率低**——理由是多数运营商的链路都会出现昼夜模式（L105 逐字："this can hint low utilization of the infrastructure as most operator links are impacted by diurnal patterns"）。
- **负载下的时延（H3 批量）**：中位/95 分位/99 分位 RTT = **95 (104) / 175 (237) / 210 (310) ms**，括号内为上传（L107；每条曲线 >200 万个 RTT 样本）。上传的 RTT 增长大于下载，作者解释为下载可用带宽更大、**路由器队列排空更快，因此同等队列长度下排队时延更小**（L107）。
- **低速率消息流**：RTT 基本在 100 ms 以内，下载（上传）中位 **50 (66) ms**、95 分位 71 (87) ms、99 分位 87 (143) ms（L112）。
- **丢包（Table 2，L110）**：H3 下载 **1.56%**、上传 **1.96%**；消息流下载 **0.40%**、上传 **0.45%**。
- 丢包突发结构：H3 下载中 **超过 75% 的丢包事件涉及多个连续包**，上传多为单包；共识别 **244 008** 次丢包事件，事件时长中位 **49 μs**，75/90 分位 58/113 μs，95/99 分位 **1.5/7.5 ms**，另有少量 >1 s 的疑似断连（L120）。消息流丢包更罕见但突发更长，99 分位时长 127 ms，个别突发 >100 包（L133）。
- **关键对照实验**：从阿姆斯特丹（Starlink 出口附近）向服务器发 H3（消息）下载，580 万（280 万）包中仅丢 10（8）个 → 丢包发生在 **Starlink 网络内部**，不是本地或服务器造成（L135）。
- 吞吐：下行 100–250 Mbit/s、中位 **178**、最大 **386** Mbit/s；上行中位 **17** Mbit/s、最大 64 Mbit/s（L152）。SatCom 下行中位 82 Mbit/s、上行 4.5 Mbit/s（L154）。QUIC H3 下行只有 100–150 Mbit/s，低于 Ookla TCP 测速（L158）。
- 网页 QoE：Starlink onLoad 中位 **2.12 s**、SpeedIndex **1.82 s**；SatCom 10.91 s / 8.19 s；有线 1.24 s / 1.0 s（L173-175）。建连耗时 SatCom 平均 2030 ms vs Starlink **167 ms**（L173）。
- 中间盒：两层 NAT（192.168.1.1 与 CGNAT 100.64.0.1），**未发现 PEP**；Wehe 跑十轮**未发现流量歧视**（L183-185）。

**5. 它的实验条件**
- **单站点**（比利时 Louvain-la-Neuve），时间跨度：时延 5 个月、吞吐/网页 4 个月、SatCom 对照 2 周；数据采集期 2021-12-20 至 2022-04-07（L74、L80）。
- 关键背景：**星间链路（ISL）当时未启用**——作者用 traceroute 验证到旧金山与新加坡的出口节点与欧洲相同（荷兰 + 德国各一个），据此判断 ISL 未开（L96）；ISL 计划 2022 年底启用（L191）。
- "负载"是**自造的**：空载 ping vs 自己发起批量传输；**不是**对全网负载的扫描。
- 无训练环节。

**6. 它自述的局限**（逐字，第 4 节 Discussion）
- L189："This study presents an initial characterization of Starlink from the perspective of **a single site in Western Europe**."
- L189："we emphasize the presence of (moderate) packet loss **even at low network utilization**."
- L191："our ping latency measurements are still in the early stages in terms of **temporal and spatial scale**. As we aim at tracking latency evolution over time, **the number of anchors we probe is limited** and does not allow us to provide a complete picture of latency for a comprehensive set of targets worldwide."
- L191："**Inter-satellite links do not seem to be enabled**, but Starlink plans to deploy them by the end of 2022."
- L195："we only studied a limited number of websites... We did **not account for differences in experience that could be due to different browsers, different devices**, or other factors. Also, **we only visited landing pages**."
- L131（方法层面的诚实声明）："from the transport viewpoint, **there is no known way to distinguish between congestion and medium-induced losses**."（即无法把丢包归因到拥塞 vs 介质）

**7. 它没做但看起来能做的地方**（基于内容）
1. **没有真正的"负载扫描"**：负载只有两档（空载 / 100 MB 批量传输），且是**自己产生的**。要得到"到达率 → 时延/丢包"的曲线，只需把批量传输换成受控速率的阶梯（如 10/50/100/200 Mbit/s），设备与 QUIC 采集链已经具备（还公开了 530 GB 抓包，L199）。
2. **无法分离拥塞丢包与介质丢包**（L131 自述）——但作者其实已经拿到区分线索：H3（高码率）丢包频繁且突发短，消息流（低码率）丢包罕见但突发长且 99 分位时长可达 127 ms（L120、L133）。**突发时长 vs 码率**这个二维关系可以直接做成一张"丢包成因判别图"。
3. **ISL 未启用**（L96、L191）：作者把"ISL 开启后包怎么在天上走、性能怎么随地变化"明确留作未来工作——这是全批最干净的一个"当时做不了、现在能做"的窗口。
4. **无昼夜/无趋势**被解释成"利用率低"（L105），但这是**推断**，没有独立的负载证据（如运营商标称容量或第三方拓扑测量）；把"低利用率"变成实测结论需要额外观测。
5. 上行慢的归因只说了一半：报告了 quiche **未实现 packet pacing** 导致 25 kB 大消息堆在网络缓冲里抬高 RTT（L112）——这意味着"上行 RTT 更高"部分是**客户端实现缺陷**而非网络特性，值得用支持 pacing 的实现重测。

**8. 和同批其他篇的关系**
- 它是本批唯一**真实测量**的论文，与其余仿真/理论论文是"地面真值 vs 模型"的关系。
- 与 **R5QTFKD2** 直接互补又直接冲突：R5QTFKD2 把路径时延建成**平稳外生分布**（对数正态/Gamma）且可用性是 i.i.d. 伯努利，本文恰好给出了这些分布的真实形状与**负载依赖**证据（中位 RTT 从 ~50 ms 涨到 ~95 ms）——两篇合起来正好暴露"外生时延"假设的失真。
- 与 **QSNRQ8PF** 综述：综述把"负载不均衡"列为挑战（QSNRQ8PF L119），本文是这条挑战在真实系统里的量化。
- 它引用 **Hypatia**[27] 与 **Kassem et al.**[34]（L189、L259、L273）；不引用同批其他篇。

**9. 对"负载变化下到达率/时延"的贡献**
**本批最硬的一条实证证据**，而且是唯一的真实系统证据：
- **时延随负载接近翻倍**：同一链路，空载中位 RTT ~50 ms → H3 批量负载下中位 **95 ms（下载）/104 ms（上传）**，99 分位 210/310 ms（L105、L107）。
- **给出了机制**（不是相关而是因果解释）：L107 逐字——上传增幅大于下载"may be explained by the larger available bandwidth for downloads allowing **emptying the router queues faster** than for uploads, having thus a **smaller impact on queuing delay** for equally-sized queues"。即：**排队时延**是负载敏感项，且它对"容量/队列比"敏感。
- **低码率几乎不受影响**：3 Mbit/s 消息流的 RTT 中位数 50/66 ms，与空载 ping 同量级（L112）——说明抬升来自**排队**而非路径本身，这为"负载-时延"曲线提供了两个明确的锚点。
- **丢包同样随负载出现**：高码率 1.56%/1.96% vs 低码率 0.40%/0.45%（L110）。
- **一个反直觉的边界条件**：作者未观察到昼夜模式，据此推断网络**利用率低**（L105）——意味着这些负载效应是**自激**的；**全网负载带来的时延抬升，本文没有测到**。
**局限必须说清**：这里没有"到达率 λ"这根轴，只有"空载 vs 饱和批量"两点；也没有排队模型。

**10. 一句话评价**
**一篇把"负载让排队时延显形"测出来的实测锚点论文**：它没有算法、没有 λ 轴，但给出了空载 ~50 ms 与负载 ~95/104 ms 这两个可被任何 LEO 路由仿真直接引用的真值，并明确指出 ISL 当时未启用——对做仿真的人而言，这是"上限有多乐观"的校准基准。

## SBCHGBCP — Segment routing for traffic engineering and effective recovery in low-earth orbit satellite constellations

**1. 一句话**
在没有星间链路（ISL）、只能靠地面中继用 RF 转发的那一类 LEO 星座（Starlink Phase 1 形态）里，把地面网的 **Segment Routing（SR）** 搬上来做两件事：用"延时受限 + 卫星不相交的 2 段路径"做流量分割以压低**单星最大负载（MSL）**，以及用两段备份路径把故障保护覆盖率顶上去（L22、L39-41）。

**2. 问题设定**
Starlink Phase 1 的 1584 颗星（550 km、周期约 90 min）**不支持激光 ISL**，星间通信只能经地面站（中继/网关/用户终端）用相控阵 RF 转发；卫星与地面站距离超过 RF 最大可达距离就断链，因此这个混合拓扑**随时间变化**（L28）。作者点出两类麻烦：①**负载激增**——太阳能卫星能量预算有限，"The surge of load may bring about an increase in **queuing delay** and a sharp drop in energy"，且单条最短路（SPR）在 DDoS 之类的突发流量下很脆弱（L30）；②**节点/链路故障**——约 3% 的 Starlink 卫星已失联，RF 链路又受天气影响，突发故障会中断在传流、造成丢包或乱序（L30）。困难在于：卫星移动快，**负载状态难以采集或预测**，传统 TE/FRR 方案搬不过来（L35）。

**3. 方法骨架**（**非 RL**：图算法 + 源路由 + 启发式选路）
- 星座模型（式1a-c，L79-87）：1584 星、550 km、**72 个轨道面倾角 53°、每面 22 星**；单点波束、可通信仰角 25°以上、**最大 RF 距离约 1123 km、足迹半径 940 km**；任意地面站至少被两颗星同时覆盖（L73）。
- 地面中继布放：密度参数 $\rho$，沿线每隔 $(1/\rho\times\omega)$ 放一个（L102）；$\rho\ge1$ 即可全球覆盖（L104）。
- 时变拓扑用**时间图**建模：时隙 $m$ 内拓扑视为固定，$G_m=(N,L_m)$；**时隙 50 ms**（与 [2] 相同）（L111、L113）。
- SR 的星上实现（关键工程点）：**SID popping 只在（能力更强、易升级的）地面中继做**，卫星只按最上层 SID 查表转发——卫星保持"简单"（L130-134）。**只考虑 2 段路径**（每条段列表至多两个 SID），依据是 IP 网里 2 段已接近最优 TE（L132）。
- 优化目标（式3，L144-146）：最小化 **MSL** $=\max_s\sum_{l\in L_s}\eta_l$。**特意不用"最大链路利用率"**——因为卫星处理能力受限、容易成热点（L144）。
- 路径约束（L155）：①**延时约束**——候选路径时延不超过最短路的 $z$ 倍（$z$ 称 delay factor，扫 $[1,2]$）；②**卫星不相交**——同一流的多条路径不得在卫星处重叠（在地面中继处允许交叉，因为假定拥塞只发生在卫星）。
- **DBTS（Algorithm 1，L161-187）**：先求最短路 $p_0$ 与 $d_0$ 得界 $D=z\cdot d_0$；对每颗卫星 $s$ 构造以 $s$ 为中点的 2 段路径 $\{s,y\}$，时延 $\le D$ 者入候选集 $\Psi$；按延时升序贪心挑选与已选集 $\Phi$ 卫星不相交的路径；**把流量在 $\Phi$ 上均分**（L165）。
- **DBTS+（L189-215）**：令路径代价 $c_k=1/h_k$（$h_k$ 为跳数）→ 分割比 $r_k=c_k/\sum_i c_i$，**给更短的路径分更多流量**，既降低全网总流量也缓解乱序（L196、L212、L215）。
- **快速重路由（第 6 节）**：**LFA** 预计算"备用下一跳"；当备用下一跳不存在时，**LFA+** 枚举卫星/地面中继作中点，预计算一条 **2 段备份路径**（L223-231）。保护覆盖率按 $\delta$（式9）与 $\delta^*$（式10，剔除集合 $\varepsilon$——那些"只被一颗卫星覆盖"的地面中继所致的不可保护路径）度量（L311、L317）。

**4. 它声称的效果**（基线 SPR [2]；Table 2 在 L299）
- 均匀流量：$D=1.5d_0$ 时 MSL 相对 SPR 降约 **20%**（L246）。
- **非单调的 D 效应（核心发现）**：$D$ 从 $1.2d_0$ 增到 $1.5d_0$，MSL 降约 2 个单位（可用不相交路径变多）；但 $D$ 从 $2d_0$ 增到 $\infty$，MSL 反而**升 1 个单位**——多找到的路径更长，抬高了全网流量、制造新热点。**MSL 最低点在 $D=1.5d_0$**，作者称这是"路径多样性与网络总负载之间的良好平衡"（L246）。
- 非均匀流量：DBTS/DBTS+ 相对 SPR 的增益从 20% 降到 **15%**；作者给的反直觉解释是"在非均匀流量模式下，SPR 反而制造了更少的热点"（L248）。
- **代价**：MSL 约 20% 的改善只换来约 **10%** 的加权 RTT 上升（L256）。**注意：摘要（L22）写的是"about 30% lower maximum satellite load"，正文（L246）写的是"about 20% reduction"——两处数字不一致，我按正文取值。**
- 路径/跳数（Table 2，L299，均匀/非均匀）：SPR 平均路由数 1、跳数 4.03/3.86；DBTS 在 $D=1.2/1.5/2/\infty$ 时路由数 2.61/3.58/4.22/4.59、跳数 4.13/4.46/4.72/4.95；DBTS+ 跳数恒小于 DBTS（如 $D=\infty$ 时 4.70 vs 4.95）。
- 快速重路由：$\rho=1$ 时 LFA+ 的保护覆盖率比 LFA **高约 15%**；$\delta$ 与 $\delta^*$ 的差距约 **25%**（说明不可保护路径很多）；$\rho=4$ 时该差距降到约 **13%**，且 **LFA+ 的保护覆盖率超过 99%**，此时 LFA 与 LFA+ 差别很小（L320-324）。

**5. 它的实验条件**
- 仿真器沿用 Handley [2] 为 Starlink 写的那个；地面中继密度 **$\rho=4$**；时隙 **50 ms**；每次仿真 **500 s = 10000 时隙**（L235）。
- 流量矩阵：用户终端用同样的布放模型、密度 **$\rho=1$**，**美国境内共 19 个** → 构成 **19×19** 矩阵（L239、L244）。均匀矩阵：361 条流每条 **1 个单位**（作者注明"可视为 1000 包/秒"）；非均匀矩阵：每条在 $[0,2]$ 随机（L244）。
- 明确假设：**"linking capacity is not the bottleneck"**（L111）——即不做链路容量约束。
- 快速重路由实验：**只考虑美国境内的地面中继**，假定境外无中继（L314）。
- 无训练环节。

**6. 它自述的局限**（逐字）
- L227："It should be noted that even with **LFA+, 100% protection coverage is not guaranteed**."
- L314："we **only consider the ground relays located inside the USA**, i.e., we assume no ground relays outside the USA. Under this assumption, **100% protection coverage is impossible even if an ideal protection mechanism** (supporting arbitrary backup path) is available."
- L239："(Note that, **the traffic matrix used here is only to evaluate our proposed algorithms. It does not mean that such a traffic matrix can be easily collected** or even utilized to construct the corresponding forwarding table.)"
- L142："Besides, **the traffic matrix is never easy to obtain**."
- L102："While finding the optimal locations for ground relays is an interesting problem, **this paper focuses on traffic engineering while assuming that all ground relays are properly placed**."
- L111："In this paper, our goal is to minimize the MSL, and we **assume linking capacity is not the bottleneck**."
- L165（乱序问题被外推）："we **assume that the packet out-of-order problem is solved at the destination** using, e.g., re-sequencing buffers."

**7. 它没做但看起来能做的地方**（基于内容）
1. **负载不是一根轴，只有两个点**：均匀（每条流 1 单位）与非均匀（$[0,2]$ 随机）（L244）。既然目标是**负载均衡**，最自然的下一步就是把流量矩阵整体缩放（0.5×/1×/2×…），看 MSL 与 RTT 如何随总负载变化——设备与仿真器都现成。
2. **模型里没有排队时延**：MSL 是纯负载计数（L144），RTT 是路径时延（式6，L253）；而引言明确指出负载激增会带来**排队时延上升**（L30）。所以那个"$+10\%$ RTT"是**路径变长**的效应，不是拥塞效应——把排队显式建进代价函数是最直接的缺口。
3. **$z$（延时因子）是静态常数**，最优值 1.5 靠扫描发现（L246、L155）。既然 MSL 对 $z$ 非单调，**按当前负载自适应调 $z$** 是现成的机制设计口子。
4. **摘要与正文数字不一致**（30% vs 20%，L22 vs L246）——需要复核，可能有一处是笔误。
5. **能量完全没有进模型**：引言提到太阳能卫星"limited energy budget"与负载激增导致"sharp drop in energy"（L30），但目标函数与约束里没有任何能量项。
6. 地面中继的最优布放被显式排除（L102），但它自己证明 $\rho$ 从 1 到 4 会显著改变保护覆盖率（L320-324）——布放与 TE/FRR 的联合优化是明确空缺。

**8. 和同批其他篇的关系**
- 谱系上是**经典负载均衡路由 + 现代 SR** 的合流：引用的 **TLR**[30] 与 **ELB**[31]（L390、L392）正是 QSNRQ8PF 综述里被反复点名的两个经典对照（QSNRQ8PF 的 [95]、[94]，L628、L626）——本文是把它们放进"无 ISL + 地面中继"这个新拓扑里重做。
- 与 **S2QZRBEJ** 共享同一个现实前提（**Starlink 初期无 ISL**，S2QZRBEJ L96 用 traceroute 实测确认，本文 L28 直接作为建模前提），且都引 **Hypatia**[34]（L398 / S2QZRBEJ L259）。两篇合起来正好构成"ISL 缺失期"的实测 + 仿真两面。
- 与 **R37BNQQ8** 都是"网络优化/启发式"而非 RL，但 R37BNQQ8 做的是 SDN + 蚁群的端到端跨域路径，本文做的是 SR 源路由 + 分段备份，**优化目标也不同**（前者是时延/碎片/带宽/均衡加权和，后者是纯 min-max 单星负载）。
- 与 **R5QTFKD2** 形成对照：R5QTFKD2 是单源到单目的 N 条并行路的年龄优化，本文是全网多商品流的负载均衡——都关心"选哪条路"，但一个优化 AoI、一个优化最大负载。
- 不引用同批其他篇。

**9. 对"负载变化下到达率/时延"的贡献**
**贡献是"负载结构"而非"负载水平"**：
- **它把负载当作要均衡的量，而不是自变量**：MSL 以"单位"（1 单位 ≈ 1000 pps，L244）报告，**没有对总到达率做扫描**——所以给不出 λ → 时延 的曲线。这是它最明显的缺口。
- **一条真正可用的结构性事实（非单调）**：放宽延时界 $D$ 会同时增加"可用不相交路径数 $\Psi$"和"平均跳数 $H$"，前者改善均衡、后者抬升总负载并制造热点；净效果使 MSL 在 **$D=1.5d_0$ 取到极小**（L246）。这是"给路由更多自由度反而更差"的实证，且它把机制拆成了两个可测的中间量（Table 2 的 $\Psi$ 与 $H$，L299）。
- **均衡收益依赖于流量分布形态**：均匀 20% vs 非均匀 15%，且 **SPR 在非均匀流量下反而制造更少热点**（L248）——意味着"负载均衡算法的收益随流量形态变化"，这在讨论"负载变化"时是一条必须区分"总量变化"与"分布变化"的提醒。
- **均衡与时延的定量置换率**：约 **20% MSL 换取约 10% RTT**（L256）。这是本批唯一一条"负载均衡代价"的显式数字。
- 但**没有排队、没有 λ、没有拥塞**——所以对"到达率/时延"只有间接价值。

**10. 一句话评价**
**把地面网的 SR + 流量分割工程化地搬到"无 ISL 的 LEO 星座"上**：方法本身是成熟工具的移植（未改 SR、未改 LFA），真正有信息量的是两条实证——**MSL 对延时界 $D$ 非单调、最优在 $D=1.5d_0$**（L246），以及**均衡收益随流量均匀性从 20% 掉到 15%**（L248）；但它的负载没有成为自变量、时延里没有排队，因此离"负载变化下的到达率/时延"仍隔一层。

## T9X6QCLL — LEO Satellite Networking Relaunched: Survey and Current Research Challenges

**1. 一句话**
Futurewei 三位作者 2023 年的 LEO 卫星网络**综述**：把路由研究拆成 11 个子领域（早期进展/IP/负载均衡/SDN/ML/DTN/地理路由/低时延/多层/杂项/仿真平台）逐条review，再补上 **3GPP 与 IETF 标准化**现状，最后给出四类挑战（L27、L105-107、L343、L462）。

**2. 问题设定**
领域背景：截至 2023-01-01 在轨 6700 颗、其中 **6000 颗在 LEO**；2030 年前计划再上天约 **50 000 颗**（L15）；中国已向 ITU 申报 12 000 颗（L17）。核心转变是通信模式从"弯管（bent-pipe）"变成"星上接收→多跳星间中继→落回地面"，ISL 用自由空间光连接相距 2000 英里的高速运动体（L21）。**这是综述，不是新算法论文**，它要回答的是"这几年这个领域往哪走了"。

**3. 方法骨架**（无算法，是分类学 + 逐条判断）
- 路由两分法（L36-38）：**快照路由**（snapshot，拓扑在一个快照内视为静态、路由表可预计算并上传）与**动态路由**（按当前配置转发）。作者指出该假设合理：单包传输时延是毫秒级，而卫星对地面站的可见时间可达数分钟。
- 第 4 节按 11 个子领域组织（L107），其中与本主题最相关的是：
  - **4.3 负载均衡**（L159-187）：列出 ELB[69]（邻居间显式交换拥塞信息、临近阈值就请邻居限流，L167）、SIDA+SSLB[70]（L169）、全局-局部混合[71]（L171）、HLBR[72]（L173）、[73]（拥塞等级 + 端到端时延估计，L175）、DBPR[74]（背压路由，距离度量 = 最短路与拥塞的组合，L177）、LBRA-CP[75]（蚁群 + 拥塞预测，L179）、[76]（用 SR，把卫星分成轻载区/重载区分别处理，L181）、LCRA[80]（L183）、[81]（把流量分成时延敏感/吞吐敏感/尽力而为三类，L185）。
  - **4.5 机器学习**（L227-245）：DRL-THSA[100]（用两跳邻域链路状态——编码成三个等级——喂 DDQN，L233）、ELM-DR[101]（L235）、ELM+MBAS[102]（L237）、QRLSN[105]（L239）、**FDR-MARL[106]**（L241）。
  - **4.8 低时延**（L271-283）：SpaceRTC[114]（在 LEO 上搭多条近最优路径的 overlay，L275）、LSGI[115]（最小化最大时延同时保持路由稳定，L277）、有向渗流[116]（面向 URLLC：每个包朝更近目的的两个邻居各转一份——一个同轨、一个异轨——中间节点去重，L279）、DQ-GERT[117]（**同时考虑时延与时延抖动**，L281）。
- 第 5 节标准化：3GPP 从 Rel-15 起的一系列 TR（38.811/38.821/36.763/22.822/23.737/28.808/22.926/24.821，L355-369），三种星上载荷形态（透明转发/再生载荷 gNB 上星/gNB-DU 在星、CU 在地，L383-398）；IETF 侧：TCPSat 历史、LISP、**Time-Variant Routing (TVR) WG**（2022 年 IETF115 成立，定义"随时间调度变化"的信息与数据模型，L448）、source routing + 语义寻址的新路由提案[166,167]（L454）、DTN 系列 RFC（L460）。

**4. 它声称的效果**
综述**无自设实验**，只有转述。与主题相关的两条转述：
- **L482（转引 [181]）**："finds a **loss rate of 0.4% in lightly loaded scenarios, and of 1.5 2% in congested scenarios**, as well as a **delay that increases significantly from 50ms median RTT (light load) to roughly 100ms RTT (congested network)**."
- L466：Starlink 累计发射 3055 颗中 2793 颗仍在轨，**约 10% 损耗率**。
- L305：某能量高效路由启发式把卫星电池寿命提升 **40%** 而性能损失很小。

**5. 它的实验条件**
**没有实验**——纯综述。第 4.11 节（L321-341）专门盘点了可用的仿真/建模平台：SaVi[136]、Hypatia[138]（Python + ns-3）、以及若干建模工作（N×N mesh 模型[141]、motif 拓扑设计[142]、容量模型[143]、随机几何[144]、UMCF 建模[148] 等）。

**6. 它自述的局限**（逐字；综述无独立 Limitations 节，以下是它对领域下的判断）
- **L187（最关键）**："**Without data from satellite network operators, it is difficult to establish the practical need for load balancing mechanisms.** It is obvious that traffic is not distributed uniformly... But **we would need to know the utilization of these links to assess whether shortest-path routing leads to congestion issues.**"
- **L283（对低时延研究最关键的判断）**："It also seems **common sense that satellites will not carry huge buffers to introduce some congestion delays. The space for optimization, in addition to some basic QoS mechanisms, seems limited.**"
- L243："This area seems emerging, with applications of a whole range of ML techniques, with **no clear-cut solution that is obviously better than others**."
- L295："This area of investigation is important to integrate multiple layers, but **seems to have slowed down**."（多层卫星网络）
- L229（对训练设定的判断）："training a model under conditions that end up being periodic would lead to good results, **as long as the training set comprises at least a multiple of such periods** (the appropriate period varies... as well as the periodicity of the traffic; **one is of the order of hours and the other is of days or weeks**)."

**7. 它没做但看起来能做的地方**（基于内容）
1. **它自己把最大的口子指出来了却没关**：L187 说没有运营商数据就无法确认"负载均衡到底有没有实际需求"、也无法判断"最短路是否真的导致拥塞"。而它引用的 [181]（本批 S2QZRBEJ）恰好提供了唯一一份公开的负载-时延数据——**把"综述说缺数据"和"唯一那份数据"接起来，就是一条现成的选题**。
2. **L283 的"卫星不会带大缓存、所以拥塞时延有限"是一句常识性断言，不是证据**。它直接决定了"低时延优化的空间有多大"；而 L482 转引的实测又显示负载下 RTT 从 50 ms 涨到约 100 ms——**断言与它自己转引的数据存在张力**，这个张力可以被实验判定。
3. **负载的"可预测基线 + 短期波动"分解（[71]，L171）只是被描述，没被验证**：作者说前者可提前全局优化、后者动态局部处理，但没有给出基线与波动的分离方法或比例。
4. **拓扑周期（小时级）与流量周期（天/周级）不匹配**（L229）被提出来是为了讲训练集要覆盖多个周期，但**没人研究过这个尺度差对训练/评估划分的影响**——对做 RL 路由的人来说这是现成的实验设计缺口。
5. **[117] 的 DQ-GERT 同时建模时延与时延抖动**（L281），是全节唯一把"抖动"当一等量的工作，但它没有与负载挂钩。

**8. 和同批其他篇的关系**
**它是本批的"引用中枢"**，直接引了同批两篇：
- **[9] = QSNRQ8PF**（L520，逐字 "Dynamic Routings in Satellite Networks: An Overview", Sensors 22.12 (2022), p. 4552）——作者把它定位为"**very recent and very thorough survey of dynamic routing**"（L38）。
- **[181] = S2QZRBEJ**（L876，"A First Look at Starlink Performance", IMC '22）——并且把它的核心数字转述进了"应用支持"挑战（L482）。
此外它引 **FDR-MARL[106]**（L720）与 **DRL-THSA[100]**（L706），这两个正是锚件卡 S85KQ4FC 里被批评的"逐包 DRL 代表"那一支；也引 **ELB[69]**、**LCRA[80]** 等同批多篇反复出现的经典对照。三篇（T9X6QCLL / QSNRQ8PF / S2QZRBEJ）构成本批内部一条闭合的引用链。

**9. 对"负载变化下到达率/时延"的贡献**
**贡献是"把这条线的现状和一句反命题摆到台面上"**，具体三条：
- **它明确指出该领域的前提未经证实**（L187 逐字）：负载均衡的必要性、以及"最短路是否导致拥塞"，都需要**运营商链路利用率数据**才能判断——这句话等于官方承认"负载→（拥塞/时延）"在 LEO 路由研究里是**假设而非事实**。
- **它给出一个反命题**（L283 逐字）："satellites will not carry huge buffers to introduce some congestion delays. The space for optimization... seems limited."——即**星上缓存小 ⇒ 排队时延可忽略 ⇒ 负载对时延的影响天然有限**。这条如果成立，会把"负载变化下的时延"这条选题的价值压得很低；但它**只是常识断言**，且与它自己转引的实测（L482：50 ms → ~100 ms）冲突。
- **它转述了唯一的实测锚点**（L482）：轻载丢包 0.4% → 拥塞场景 1.5–2%，中位 RTT 从 50 ms → 约 100 ms。这是把 S2QZRBEJ 的结论升格成"领域共识级"引用的一次传播，做选题检索时值得注意（同一组数字在本批两篇里各出现一次）。

**10. 一句话评价**
**一份偏工业视角（Futurewei）、覆盖到标准化层的 2023 年 LEO 网络地图**：它最有价值的不是罗列，而是两个判断——**负载均衡的实际需求因缺运营商数据而无法确证**（L187），以及**小缓存使拥塞时延优化空间"看起来有限"**（L283）；这两句一正一反正好卡住了"负载变化下的到达率/时延"这条选题的要害，而它自己并未去验证其中任何一句。

## TAUEF8PF — Deep Reinforcement Learning with Double Q-learning

**1. 一句话**
证明 Q-learning/DQN 的 max 算子会系统性**高估动作价值**（不论误差来自函数逼近、噪声还是非平稳），并把表格版 Double Q-learning 推广到深度网络，给出一个"只改 target"的极简修法 **Double DQN**（L7、L17、L105）。

**2. 问题设定**
Q-learning 的 target 里 max 同时承担**选动作**与**评价值**两个角色，因此倾向于挑中被高估的值（L55）。此前有两种解释：逼近器不够灵活（Thrun & Schwartz 1993）与环境噪声（van Hasselt 2010, 2011）；本文把两者统一——**只要动作价值不准确，就会产生正偏**，而学习过程中价值不准是常态（L11 逐字："overestimations can occur when the action values are inaccurate, **irrespective of the source of approximation error**... imprecise value estimates are the norm during learning"）。作者真正要回答的是三个此前未定论的问题：**高估是否常见、是否损害性能、能否被普遍抑制**（L7）。**注意：这是通用 RL 方法论文，全文（L1-356）与 LEO/卫星网络零接触。**

**3. 方法骨架**
- 标准 Q-learning target（式2）：$Y_t^{Q}\equiv R_{t+1}+\gamma\max_a Q(S_{t+1},a;\theta_t)$（L38）；DQN 改用目标网 $\theta^-$（式3，L48）。
- **Double Q-learning**（式4，L66）：$Y_t^{\text{DoubleQ}}\equiv R_{t+1}+\gamma Q\big(S_{t+1},\arg\max_a Q(S_{t+1},a;\theta_t);\theta_t'\big)$ —— **用 $\theta_t$ 选动作、用第二套权重 $\theta_t'$ 评价**，从而把"选择"与"评估"解耦（L69）。
- **Double DQN**（L108）：把上式里的 $\theta_t'$ 换成 DQN 已有的**目标网** $\theta_t^-$：
  $Y_t^{\text{DoubleDQN}}\equiv R_{t+1}+\gamma Q\big(S_{t+1},\arg\max_a Q(S_{t+1},a;\theta_t);\theta_t^-\big)$。作者自述这是"perhaps the minimal possible change to DQN"，**不新增网络、不新增参数**（L111、L113）。
- **Theorem 1（下界，L79）**：若某状态下所有真实最优动作价值相等（$Q_*(s,a)=V_*(s)$），估计值整体无偏（$\sum_a(Q_t-V_*)=0$）但方差非零（$\frac1m\sum_a(Q_t-V_*)^2=C$），则 $\max_a Q_t(s,a)\ge V_*(s)+\sqrt{\frac{C}{m-1}}$，且**该下界是紧的**；而 Double Q-learning 估计的绝对误差下界为 **0**。作者特别指出：**不需要假设不同动作的误差相互独立**（L81）。
- **Theorem 2（L294）**：若误差独立均匀分布于 $[-1,1]$，则 $\mathbb{E}[\max_a Q_t-V_*]=\frac{m-1}{m+1}$。
- 两个必须区分的概念：高估**不是**"面对不确定性的乐观"（探索奖励）——后者鼓励探索，前者发生在**更新之后**，是"面对表面确定性时的过度乐观"，且会**主动阻碍**学到最优策略（L98 逐字："these overestimations occur only after updating, resulting in **overoptimism in the face of apparent certainty**"）。
- **bootstrapping 会放大问题**：用已被高估的值再自举，会把错误在估计中传播，且由于各状态/动作的高估程度不同，被传播的是**错误的相对信息**（L96）。

**4. 它声称的效果**（基线：DQN，超参完全一致）
- **49 个 Atari 游戏全部观察到 DQN 高估**，程度不一（L152）。
- 极端案例 Asterix 与 Wizard of Wor：DQN 的价值估计按**对数尺度**爆炸式上升，而**同期得分反而下降**——直接证明高估在损害策略质量（L152）。
- Table 1（no-op 起步、5 分钟，L154）：中位 93.5%→**114.7%**，均值 241.1%→**330.3%**。
- Table 2（human starts、30 分钟，L164）：中位 47.5%→**88.4%**（调参版 116.7%），均值 122.0%→**273.1%**（调参版 475.2%）。
- 点名涨幅最大的几个：Road Runner 233%→617%、Asterix 70%→180%、Zaxxon 54%→111%、Double Dunk 17%→397%（L176）。
- **反向证据（论文正文未讨论，但 Table 4/Table 5 里可见）**：部分游戏 Double DQN **更差**——Alien 42.75%→40.31%、Atlantis 451.85%→320.85%、Centipede 62.99%→20.75%、Asteroids 7.32%→1.70%（Table 4，L347）。

**5. 它的实验条件**
- 测试床：Atari 2600 + Arcade Learning Environment，49 个游戏（与 Mnih et al. 2015 同列表）（L119、L329）。
- 网络与 DQN 完全相同（L121、L333）：输入 84×84×4 灰度帧，3 层卷积（32 个 8×8 stride 4；64 个 4×4 stride 2；64 个 3×3 stride 1）+ 512 全连接，ReLU，共约 **1.5M 参数**；优化器 RMSProp（momentum 0.95）。
- 超参（L337）：$\gamma=0.99$、$\alpha=0.00025$、目标网更新间隔 $\tau=10{,}000$、训练 **50M 步 = 200M 帧**（单 GPU 约 1 周）、经验回放 **1M** 条、每 4 步更新一次、minibatch 32、$\epsilon$ 在 1M 步内从 1 线性降到 0.1。
- 评价：no-op 起步 5 分钟（18,000 帧）、$\epsilon=0.05$、100 局平均（L162）；另做 human starts——每游戏取 100 个专家轨迹起点、最多 108,000 帧（30 分钟）（L184）。
- **公平性处理**：主对比中 Double DQN **使用与 DQN 完全相同的超参**，作者自述这是为了"controlled experiment focused just on reducing overestimations"（L162）；另有单独的调参版（$\tau$ 10,000→30,000、$\epsilon$ 0.1→0.01、评估 $\epsilon$=0.001、顶层动作价值共享 bias，L186）。
- **训练与评估用同一批游戏、同一环境**，没有跨分布测试；human starts 只是同一游戏内的鲁棒性检验。

**6. 它自述的局限**（逐字；**无独立 Limitations 章节**，以下散见于正文）
- L105："**Although not fully decoupled**, the target network in the DQN architecture provides a natural candidate for the second value function."
- L160："**Overoptimism does not always adversely affect the quality of the learned policy.** For example, DQN achieves optimal behavior in Pong despite slightly overestimating the policy value."
- L162："This evaluation is **somewhat adversarial**, as the used hyperparameters were tuned for DQN but not for Double DQN."
- L186（调参理由隐含承认未调版吃亏）："Some tuning is appropriate because the hyperparameters were tuned for DQN, which is a different algorithm... to reduce overestimations further **because immediately after each switch DQN and Double DQN both revert to Q-learning**."
- 另：表格（Table 4/5，L347、L355）显示多个游戏上 Double DQN 反而变差，**论文正文未就此给出解释或讨论**。

**7. 它没做但看起来能做的地方**（基于内容）
1. **只报告赢的、不解释输的**：L176 只点了 Road Runner/Asterix/Zaxxon/Double Dunk 四个大涨的游戏，而 Table 4（L347）里 Alien、Atlantis、Centipede、Asteroids 明显退化**没有任何讨论**——"什么时候 Double DQN 有害"是一个现成的、有数据支撑的开放问题。
2. **Theorem 1 的假设很强**：要求该状态下所有动作真实价值相等（L79）。作者只放宽了"误差独立"（L81），没碰这条等值假设；**在价值差异大的状态下高估行为如何**，理论上没答。
3. **$\tau$ 与高估的关系只被顺带提到**：调参版把 $\tau$ 从 10,000 提到 30,000 并说能进一步降高估（L186），但**没有系统性研究**"目标网更新间隔 → 高估幅度"这条曲线。
4. **只在 DQN 一族验证**：文中说方法可推广到任意函数逼近（L17），但实验只给了 DQN（离散、Atari）。
5. 没有在**连续代价型目标**（如时延/负载这类代价信号）上验证——而游戏是稀疏奖励，二者对价值偏差的敏感度不同。

**8. 和同批其他篇的关系**
- **它是本批"方法学标尺"**：锚件卡 S85KQ4FC 指出那篇论文自称 DDQN、但式(17)写的其实是**原版 max 目标**，并非本文的 double 目标——TAUEF8PF 正是判定该主张的原文依据。
- **T9X6QCLL** 的 ML 小节提到 DRL-THSA 用 DDQN（T9X6QCLL L233），同一条线。
- **QSNRQ8PF** 也提过卫星物联网路由里的"improved dual-Q learning"，并说未来可以"用两个神经网络替换两张 Q 表"（QSNRQ8PF L186）——恰好就是本文做过的事。
- **与 QGAREQUM 不像**：后者是延迟 RL 的新框架（AD-RL），本文是价值偏差的修正；两篇都是通用 RL，**互不引用**，参考文献（L205-257）全是 RL/DeepMind/机器学习文献，**无任何 LEO/网络论文**。

**9. 对"负载变化下到达率/时延"的贡献**
**没有直接贡献**——全文没有网络、没有到达率、没有时延指标，性能度量只有 Atari 游戏得分（L119、L343）。
**但有一条方法学事实值得记入做 RL 路由的人的工具箱**：
- **高估幅度随动作数 $m$ 增长，且不依赖于误差的来源**（L83、Fig 1）。在 LEO 路由里，下一跳动作空间通常只有**邻居数**那么多（锚件卡 S85KQ4FC 的四邻居即 $m=4$），按 Theorem 2 的均匀误差情形，高估期望为 $\frac{m-1}{m+1}=\frac35=0.6$；按 Theorem 1，下界是 $\sqrt{C/(m-1)}=\sqrt{C/3}$。也就是说**动作空间小并不等于高估可以忽略**，它随价值估计误差 $C$ 增长。
- **对"以时延/负载为代价信号"的 RL 尤其危险**：L96 逐字——高估"has the pernicious effect of propagating the **wrong relative information about which states are more valuable than others**, directly affecting the quality of the learned policies"。若奖励是"负时延/负负载"，那么被扭曲的正是"哪个状态更拥塞"的相对排序——**而这恰恰是负载变化下路由决策所依赖的全部信息**。
- 边界条件：作者自己说高估**不一定**损害策略（L160，Pong 的例子），所以这条是"风险提示"而非"必然失效"。

**10. 一句话评价**
**RL 领域的奠基性方法论文（Double DQN 的出处），在本批语料里的角色是"正确性标尺"**：它解释了为什么 LEO 路由里大量自称 DDQN 的工作需要被逐条核对 target 写法，并给出"高估随动作数增长、且扭曲的正是状态价值的相对排序"这一条与负载感知路由直接相关的警示；但它本身与 LEO 网络毫无交集，对到达率/时延**零贡献**。

## TQF59BD7 — IDLB: An SDN-Based Load-Balancing Routing Protocol for Autonomous Satellite Constellation Networks

**1. 一句话**
DLR + ESA 做的**分布式 SDN 负载均衡路由协议**：把星座切成星上独立簇、每簇一颗星当 SDN 控制器，簇内用"best-of-k 路径 + 按 QoS 类加权的效用函数"做主动负载均衡，簇间用地理信息选出口节点（NHCN）；核心实验是**把网络负载一路加上去，看 QoS 合规率在哪个负载点跌破 95%**（L17、L123、L430）。

**2. 问题设定**
带 ISL 的 LEO 星座里，光 ISL 速率虽高，但**瓶颈依然会出现**：地面终端分布不对称会造成流量尖峰/地理热点，导致链路临时饱和（L23）。作者的论证链是：地面集中控制因物理尺度大而无法及时下发路由调整、且信令开销大（L25）；星上算力有限所以方案必须低复杂度（L25）；因此用**星上分布式 SDN** 换取反应速度，用**主动拥塞缓解 + 自适应负载均衡**换取 QoS 合规（L23-27）。需要注意的是，这与 SBCHGBCP 的前提**正好相反**——那篇假设无 ISL 靠地面中继，本篇假设有 ISL。

**3. 方法骨架**（**非 RL**：协议设计 + 启发式路径计算）
- 参考星座两个（Table 1，L66）：**SCN-288**（288 星、12 面 × 24、780 km、倾角 86.4°、准极轨 Walker star；主战场）与 **SCN-1440**（1440 星、30 面 × 48、600 km）（L59-61）。
- 链路：每星 4 条 ISL（2 同轨 + 2 异轨），速率 **1 Gbps**，每 ISL 输出缓冲 **0.36 Mbit**（=1500 B 包 ×30）FIFO 尾丢弃；大簇用 1.08 Mbit（L70、L76）。**异轨 ISL 在 ±80° 纬度关闭**（极区轨道面相对位置翻转，天线转不过来）（L72-74）。
- 地面（Table 2，L88）：**2000 个活跃 UT**（每个 100 Mbps、最低仰角 30°）+ **39 个 GW**（最低仰角 20°、馈电上行 5000 Mbps / 下行 1000 Mbps）；UT 分布**按全球人口密度采样**并封顶 100 个/km²（L82）。
- **分布式 SDN 架构**：簇是**星座拓扑内固定**的划分（因此相对地面是移动的），簇内居中的一颗星担任控制器（L123）。层次只做一层扁平（但可扩展到多层 SDN）（L127）。
- **两级路由表**（L147-158）：**地理路由表**（地理 cell → 目的节点或 NHCN）判"是否本簇服务"及"从哪条链路出簇"；**簇内路由表**（MAC → 下一跳）做本地解析。作者强调**不做全局终端-卫星映射**，只有局部解析，以压信令。
- 地理分片：等距圆柱 3°×3° 网格直到 ±87°，极区合并 → **6962 个区域**，地理标识至少 13 bit（L164）。
- 簇尺寸：SCN-288 用 12（4×3）/ 24（6×4）/ 48（8×6）；SCN-1440 用 48（6×8）（L170-172）。
- **簇内优化目标**（式2，L223）：$\min_t\max_{(i,j)\in E}u_t(i,j)$，其中 $u_t=f_t/c_t$（式1）。作者说明真正的动态 MCFP 含**时变性、非线性（含传播/排队时延函数 $\tau$）、随机性与动态拓扑**，被判定为多项式时间不可解（式3-4，L226-238），因此退化到启发式。
- **动态 best-of-k 算法**（第 5.1.2 节）：按 QoS 类给不同效用函数（式5-7，L251-259）——QoS1 只用路径时延 $(L(p)+\epsilon)^{-1}$；QoS2/QoS3 用跳数与路径利用率的加权 $\psi\cdot(N_{hops}+\epsilon)^{-1}+(1-\psi)\cdot(U(p)+\epsilon)^{-1}$。复杂度：路径计算 $\mathcal{O}(|F|(|E|+|V|\log|V|+k))$、判决 $\mathcal{O}(|F|k)$、空间从 $\mathcal{O}(|V|^2)$ 降到 $\mathcal{O}(|V|k)$（式9-11，L271-283）。
- **簇间路由**（第 5.2 节 + Algorithm 1）：先在簇级算 SPT，再按 QoS 选 **NHCN**（Next-Hop Cluster Node）；时延敏感走最短路，低优先级**随机化**以打散瓶颈；带 ISL 关闭与负载阈值筛选（L300-339）。
- 两种粒度：**F-IDLB**（逐流）与 **P-IDLB**（逐包，无流状态、路由逻辑更简单但易失稳，需滞回与阈值防抖）（L288-294）。

**4. 它声称的效果**（基线：动态源路由 SPF 与 GEVR 上界）
- **核心结果——QoS 合规率跌破 95% 的负载点**（L449）：源路由 **约 7.6 Gbps**；F-IDLB 12 节点簇 **12.5 Gbps（+64.5%）**；24 节点簇 **约 15.0 Gbps（+97.4%）**；48 节点簇 **约 16.2 Gbps（+113.2%）**。
- 收益递减：48 节点仅比 24 节点多撑 **12%** 负载（L464）。
- 粒度对比：P-IDLB 在 **约 8.6 Gbps** 跌破阈值（已优于源路由），F-IDLB 相对其提升 **45.3%**（L472）。
- 更大星座（SCN-1440，同为 48 节点簇）：95% 合规下约 **20.2 Gbps**——同簇尺寸提升约 **25%**，与物理尺寸相当的 12 节点簇比提升约 **61%**（L502）。
- **路由收敛**（Table 5，L441，负载 13.2 Gbps = 9500 个会话、平均时长 100 s）：12 节点 平均 **56.968 ms** / 最大 104.782 ms；24 节点 平均 **117.338 ms** / 最大 285.276 ms；48 节点 平均 **273.526 ms** / 最大 747.552 ms。**要求是 < 130 ms**（Table 3，L382）——**只有 12 与 24 节点簇满足，48 节点簇平均 273.5 ms 明显超标**，而摘要只引用了 24 节点的 117.338 ms（L17），未提 48 节点的违约。
- 信令开销：0.062% / 0.112% / 0.208%（12/24/48 节点），远低于 5% 要求（Table 5，L441、L457）。
- 丢包率（13.2 Gbps，Table 5，L441）：12 节点 QoS1/2/3 = $1.044\times10^{-4}$ / $3.571\times10^{-4}$ / $3.374\times10^{-4}$；24 节点 $2.948\times10^{-6}$ / $7.050\times10^{-5}$ / $1.344\times10^{-4}$；48 节点 $8.942\times10^{-7}$ / $2.557\times10^{-6}$ / $2.285\times10^{-6}$。
- 时延：QoS1（150 ms）与 QoS2（200 ms）**超预算会话均少于 1%**；QoS3（300 ms）也都在限内（L407）。
- 抖动（48 节点簇，QoS1）：F-IDLB 平均 **2.91 ms**、最大 **85.15 ms**；GEVR 平均 0.64 ms、最大 15.09 ms（L417）。
- GEVR 上界表现更从容：QoS3 流量会主动走更长但低拥塞的路径，延迟分布明显"顶格"在各 QoS 类上限处（L407）。

**5. 它的实验条件**
- 自研 C++/Python **包级系统仿真器**，可快于实时，支持上千星规模（L367）。
- 流量：以 session 为单位（UT-UT 与 UT-GW），**只用 CBR**（作者说为结果一致性，L371）；起始时刻均匀采样、时长按指数分布（均值 100 s）；QoS 占比 **QoS1 10% / QoS2 34% / QoS3 56%**（Table 4，L385）。
- QoS 类定义参照 5G NR 配置与 **ITU Y.1541**：QoS1 时延 150 ms、丢包 $10^{-2}$、抖动 <30 ms；QoS2 200 ms、$10^{-4}$、<50 ms；QoS3 300 ms、$10^{-6}$（Table 4，L385、L117）。
- **网络负载定义**（式16，L435）：单位窗口内进入星座的聚合上行数据量除以窗口时长；包大小一般取 12 kbit。
- **扫描方式就是负载阶梯**：核心图 Fig 9/10/11/12 都是 "QoS compliance vs 网络负载"（L449、L462、L490、L494、L498），SCN-1440 的横轴从 13.9 到 25.0 Gbps（L500）。
- 基准：**GEVR**（瞬时完美全局知识、无信令无延迟的不可实现上界）与**动态源路由**（Dijkstra 最快路、不共享链路负载信息）（L393-395）。
- 无训练环节（协议/启发式）。

**6. 它自述的局限**（逐字）
- L395（基准选择）："Comparisons with other state-of-the-art approaches **can be difficult, as the routing schemes require significant design and implementation efforts**... Thus, we **focused on source routing**."
- L94（链路简化）："ESLs are modeled with constant data rates in this investigation, **omitting aspects such as adaptive coding and modulation to isolate in-space routing effects**... This simplification ensures that ESL dynamics do not confound the analysis of intraconstellation load-balancing."
- L63："In real-world systems, the actual position of a satellite varies slightly... Consequently, **only the theoretical positions of satellites are considered**."
- L102："As this research primarily focuses on protocol characteristics, **solely the presented set of traffic model parameters has been investigated**."
- L438："Due to the ramp up and down of the traffic models, **higher peak loads occur in the shorter simulation window**. So, protocol performance **may be even slightly better** when evaluating longer windows."
- L504："Potential adjustments to the configuration of the algorithms can be made... However, to enable a direct comparison, **the same parameters used for SCN-288 were applied. A more detailed analysis of this larger and varied constellations is left for future work**."
- L506："**Future work should investigate the performance in operational architectures like Starlink or OneWeb**... adjustments to handover policies and cluster boundaries may be required."
- L482（自曝一次失败配置）："Figure 11 illustrates this **systematic error** consisting of periodic drops due to peaks in high-priority signaling traffic. Consequently, **this faulty approach rarely achieves more than 97% QoS compliance**."

**7. 它没做但看起来能做的地方**（基于内容）
1. **排队时延被测量、被写进公式，却从不被优化、也不单独报告**：式14 的端到端时延分解为 $\underbrace{l_s}_{\mu s}+\underbrace{l_r}_{\mu s}+\underbrace{l_q}_{\mu s}+\underbrace{l_p}_{ms}$（L404），作者明确说"Given the chosen buffer sizes, the **queuing delays was observed to be in the domain of milliseconds**"（L401）——但优化目标是 **min-max 链路利用率**（式2），QoS1 的效用函数只用到路径时延、QoS2/3 只用到跳数与利用率（式5-7）。**"负载 → 排队时延"这条曲线完全没画**，而数据显然在手。
2. **纵轴选的是"合规率"而非"时延"**：所有载荷图（Fig 9-12）的纵轴是 QoS compliance（>95% 阈值），不是端到端时延或丢包率。换成时延/丢包作纵轴就能得到一条真正的负载-时延曲线。
3. **48 节点簇违反了它自己设定的收敛要求却没被对账**：Table 3 要求路由收敛 **<130 ms**（L382），Table 5 里 48 节点簇平均 **273.526 ms**、最大 747.552 ms（L441），而正文仍把 48 节点当作负载表现最好（+113.2%）来推荐，只在 L464 提了"收敛显著增加"。**性能-反应性之间的取舍没有被合成一个目标函数**。
4. **只用 CBR 流量**（L371），而全文动机恰恰是**突发尖峰与地理热点**（L23）。用 on-off（仿真器已支持，L371）重跑同一组负载扫描是最直接的补实验。
5. 结论把"使能 ML 增强的流量工程"列为未来方向（L516），而它自己的 best-of-k 效用函数（式6-7）里的权重 $\psi_2,\psi_3$ **是手工常数**（L262）——这正是可学习的参数。

**8. 和同批其他篇的关系**
- 与 **SBCHGBCP** 是"同一问题的镜像前提"：那篇假设**无 ISL、靠地面中继**，用 SR 做 min-max 单星负载；本篇假设**有 ISL**，用分布式 SDN 做 min-max 链路利用率。两篇都引 **Handley**（SBCHGBCP 的 [2] 是 HotNets'19 地面中继；本篇的 [2] 是 HotNets'18 "Delay Is Not an Option: Low Latency Routing in Space"，L530），也都在结论里指向 SR/流量工程的思路（本篇 [18] 即 SR-TE 避热点，L51）。
- 与 **QSNRQ8PF** 综述的 4.2.1 SDN 节和 4.2.2 流量均衡节是同一类工作，但本篇是**带实测式仿真与明确负载阈值**的协议论文，比综述里那些条目扎实得多。
- 与 **T9X6QCLL** 的关系密切：T9X6QCLL 的 4.3 负载均衡节与 4.8 低时延节正是本篇所在的领域；但 T9X6QCLL 判断"卫星不会带大缓存、拥塞时延优化空间有限"（T9X6QCLL L283），而本篇给出**0.36 Mbit（30 包）的小缓冲**设置（L76）且明确说排队时延在毫秒量级（L401）——**两篇合起来正好量化了那条"常识断言"**。
- 与本批 DRL 论文（FDR-MARL 那一支）**不像**：无学习、无状态/动作/奖励，纯协议 + 启发式。

**9. 对"负载变化下到达率/时延"的贡献**
**本批最接近"负载 → 性能"这条曲线的一篇**，但方向要看清：
- **它给的是"负载阈值"而非"时延曲线"**：QoS 合规跌破 95% 的负载点为 源路由 7.6 / F-IDLB-12 12.5 / F-IDLB-24 15.0 / F-IDLB-48 16.2 / SCN-1440-F-IDLB-48 20.2 Gbps（L449、L502）。这是一张可直接引用的"负载容量"表，**但它不是 λ→时延**。
- **给出显式的时延分解式**（式14，L404）：切换（μs）+ 路由查找（μs）+ **排队（μs，实测在毫秒量级）** + 传播（ms）——**排队项被明确列为负载敏感项并给出量级**（L401）。这对任何要给 LEO 路由仿真标定排队时延的人来说，是全批最具体的一条。
- **抖动随负载与重路由出现**：QoS1 抖动平均 2.91 ms、最大 85.15 ms；作者归因于"路径改变（例如重路由）导致传播时延跳变"（L415-417）。即**负载引发的路由调整本身会产生抖动**，这是"负载变化 → 时延稳定性"的一条机制性事实。
- **小缓冲的量化**：0.36 Mbit ≈ 30 个 1500 B 包（L76）。这直接支持 T9X6QCLL L283 的"小缓存"判断，也解释了为什么这里的排队时延只有毫秒级——**在 LEO 上，"负载变化下的时延"这个效应天然被小缓冲压小**。
- 缺口：无逐包到达率轴（负载是聚合 Gbps 而非 λ）、无排队模型、无时延-负载曲线。

**10. 一句话评价**
**本批工程完成度最高的一篇（DLR + ESA、5G NR QoS 档位 + ITU Y.1541 预算、包级仿真）**：它把"负载加到哪里 QoS 会崩"这件事量化成了一张可比的阈值表（7.6 → 16.2 Gbps，L449），并给出含**排队项**的时延分解（L404）；但它把负载当分母而不是自变量，纵轴永远是合规率而非时延，所以离"到达率 → 时延"仍差一张图。

## TRM2HPFN — A Dynamic Routing Concept for ATM-Based Satellite Personal Communication Networks

**1. 一句话**
LEO 卫星 ISL 路由的**祖师爷论文**（Werner, 1997, IEEE JSAC）：把周期性时变拓扑切成 K 个快照，**离线**先为每个时隙建好"虚拟拓扑"（每对起止星一组不相交路径），再跨时隙挑选"路径序列"以最小化**路径切换（VPC handover）带来的时延抖动**——这就是 DT-DVTR，后来几乎所有卫星快照路由的源头（L7、L146）。

**2. 问题设定**
带 ISL 的 LEO/MEO 卫星个人通信网（S-PCN）要跑**面向连接**的业务（ATM），而 ISL 子网拓扑永久在变：既有**离散**的链路通断（极区关掉异轨 ISL），又有**连续**的星间距离变化（L56）。作者指出核心矛盾：**连接建立后若必须在中途换路，新旧路径的传输时延差会带来严重抖动**，他称之为 virtual connection handover（L70 逐字："such connection handovers may introduce severe delay jitter resulting from the difference in transmission delay on the old and new path"）。ATM 是面向连接的、必须保序，所以这个抖动是致命的。缓解的依据是：**LEO/MEO 的"物理"拓扑动态是周期性确定的**，周期即星座轨道周期（Iridium 为 100 min），因此可以离线预制（L72）。

**3. 方法骨架**（**非 RL**：离线图论 + Dijkstra + 序列优化）
- 网络模型四条假设（L109-121）：节点数恒定；无孤立节点；拓扑因**离散链路通断**与**连续距离变化**而变；整个动态**以 T 为周期**。另有三条业务假设（L125-129）：主业务是时延敏感的（话音/视频）；**同一连接双向走同一路径**；系统应天生具备路径失效应对能力，因此**要求备份路径不相交**。
- 离散化：$\Delta t=T/K$，快照 $G(k)=(V,E(k))$，链路代价 $c_{ij}(k)$——**"主要是指节点距离，即传播时延"**（L131）。
- **$\Delta t$ 的有效性条件（两条，L138-142）**：①必须与离散的链路通断行为**同步**，保证 $G(k)$ 在整个区间内正确反映物理拓扑（硬条件）；②必须小到让区间内的连续代价变化可忽略：$(c_{ij}((k+1)\Delta t-0)-c_{ij}(k\Delta t))/c_{ij}(k\Delta t)\ll1$。作者指出这两个条件给出一个权衡：$\Delta t$ 小则区间内变化小，$\Delta t$ 大则相邻区间之间的瞬时偏移少。
- 两个**全离线**模块：
  - **DT-VTS（虚拟拓扑建立）**：对每个 OD 对 $w$ 求一组循环无回路路径 $P_w(k)$；用**迭代调用 Dijkstra 并"删掉"已占用链路**来强制得到不相交路径集——作者说这同时"为简单鲁棒的故障恢复打下基础"（L150）。
  - **DT-PSS（路径序列选择）**：这才是"真正的动态路由"所在——跨连续时隙为每个 OD 对挑路径序列，而不是独立解一串准静态路由再"承受"切换后果。三个优化目标（L157）：①**最小化 HO 时延抖动**；②最小化 HO 次数；③（带限制地）最小化平均时延。
- **两种优化时间窗**（L162、L167）：(1) 在整个周期 T 上优化 → 从 $m^K$ 种可能中得唯一首选序列 $S_{T,1}$，或 Q 条有序（带优先级）序列；(2) **滑动窗** $\tau$ 个时隙 → 对每个 k 得 $S_{\tau,1}(k)$。
- ATM 实现（第 V 节）：完全 **VP/VPC 化**——所有共用同一对首末星的端到端 VCC 聚合为一条跨 ISL 子网的公共 VPC；**中转星只做纯 VP 交换**（L177-179）。VPI 字段 12 bit → 单条 ISL 每步最多 **4096 个 VP**（L183）。

**4. 它声称的效果**（基线：周期内最小化 HO 次数的朴素方案）
- VPI 规模：仿真中单链路 **最多约 400 个 VP**，出现在赤道区、正好在 seam 中段（如 Fig.2 的 22 号与 43 号星），远低于 4096 上限，也低于"终止星对数 = 2145"的理论上界（L188-190）。
- 抖动对比（Fig 12，L219）：对 Iridium 中固定时长 **2 min** 的通话、$\Delta t=1$ min，**滑动窗（最小化 HO 抖动）明显优于周期级（最小化 HO 次数）**。
- 真实业务场景（Fig 13，L219）：电话业务、通话时长负指数分布、**均值 3 min**、滑动窗 **5 min** → **只有不到 20% 的通话会遭遇任何一次切换**；且"只有极低比例的通话需要承受大于 **20–30 ms** 的 HO 抖动"。
- 代价：滑动窗方案用的 VPI 更多——**单链路平均 VPI 数随滑窗尺寸近似线性增长**（L200）。

**5. 它的实验条件**
- 星座：**Iridium**，66 星 / 6 个准极轨（倾角 86.4°）/ 780 km / 周期 100 min；每星 2 条永久同轨 ISL + 0–4 条动态异轨 ISL；**极区关闭异轨 ISL**、**seam 两侧不建链**，因此同时在用的 ISL 数在 **2–4** 之间变化（L25、L37、L56）。
- 参照系统对照表（Table I，L25）：ICO / Odyssey / Globalstar / Iridium / Teledesic 的轨道、星数、ISL 配置与业务定位。
- 仿真工具自研：**ISLSIM**（C 内核 + X/Motif 界面），模块含星座几何、最短路搜索、路径连续性优化、统计评估与可视化（L196）。
- 业务画像：**只做电话（话音）**；呼叫在时间上均匀分布、覆盖所有可能的首/末星组合；2 min 定长通话用于两方案公平对比，3 min 均值负指数通话用于真实场景（L207、L219）。
- 无训练环节（全离线计算）。

**6. 它自述的局限**（逐字）
- **L169（最重要的一条）**："The graph-theoretical framework developed so far... provides a sound basis to extend analytical work and formulate any **minimax target functions** that are related to optimized routing in a wider sense like, e.g., **minimizing worst case link traffic throughout the network by means of traffic adaptive routing**. However, **such an analytical extension is beyond the scope of this paper and is envisaged for further work**; here, we will restrict ourselves to a simulation-based performance evaluation of the presented off-line routing approach."
- L219："Considering such 2 min fixed-length calls is, of course, **not close to reality**, but it is the only way to make a fair (and at least basic) comparison of both approaches."
- L234："In future work, we also intend to **refine the traffic modeling** with respect to both, an improved global geographic traffic distribution and realistic PCN user service/traffic profiles."
- L236："In the medium term, research on **broadband aspects** of the considered systems should also be intensified."
- L192："Observe, however, that short-term 'overlapping' of successive VPC's during controlled VPC handover... will also **increase the worst case VPI requirements**."

**7. 它没做但看起来能做的地方**（基于内容）
1. **模型里完全没有负载**：链路代价"主要由节点距离，即传播时延决定"（L131）；没有容量约束、没有拥塞、没有排队。而作者自己在 L169 明确把"**最小化全网最坏链路流量**"这类 minimax 目标**列为未来工作**——也就是说，**这个领域的源头论文一开始就把负载维度排除在外了**，后来论文里的负载均衡是补上去的。
2. **抖动只算了"几何分量"**：HO 抖动被明确定义为"新旧路径传输时延之差"（L70），即纯传播时延跳变；**排队抖动不在其中**。这给后来做"负载 → 抖动"的人留了一个必须补的缺口。
3. **$\Delta t$ 的选择只有定性两条条件**（L138-142），没有给出选值的算法或优化；而它自己指出这是"低区间内变化"与"少区间间跳变"之间的权衡。
4. **VPI 消耗与抖动的联合优化缺失**：L200 观察到滑窗越大 VPI 越多（近似线性），但两条曲线没有被合成一个目标。
5. 只做电话（L207、L236），宽带被推迟——而正是宽带（大流量、负载敏感）才需要负载均衡。

**8. 和同批其他篇的关系**
- **它是本批的谱系根**：QSNRQ8PF 的 4.1.3 节"Virtual Topology"整节讲的就是 DV-DVTR（QSNRQ8PF L182），并在参考文献里列为 [44] "Werner, M. A dynamic routing concept for ATM-based satellite personal communication networks"（QSNRQ8PF L526）；T9X6QCLL 的早期进展节把 FSA（1995）与快照路由列为里程碑，其参考文献 [37] 正是本篇（T9X6QCLL L404）；SBCHGBCP 也引 [37] Werner（SBCHGBCP L404）。
- **快照/时间图范式**由本篇确立，而 QSNRQ8PF（L125 快照序列路由、L180-182 虚拟拓扑）、SBCHGBCP（时隙 50 ms 的时间图）、TQF59BD7（快照式路径重算）**全都在用**这一范式。
- 与本批 DRL 论文（FDR-MARL 那一支）的关系是"被继承的前提"：DRL 路由通常仍在快照/时间图框架内做决策。
- 与 **S2QZRBEJ** 形成 25 年的时间对照：1997 年假设"拓扑变化是抖动的唯一来源"，2022 年的实测显示**负载**才是把 RTT 从 50 ms 推到 100 ms 的原因。

**9. 对"负载变化下到达率/时延"的贡献**
**没有直接贡献**——全文没有到达率、没有负载、没有排队；链路代价就是传播时延（L131）。
**但有两条可复用的事实**：
- **给出了"路径切换抖动"的量化锚点**：在 Iridium 上、真实电话业务（均值 3 min）下，**不到 20% 的通话会遇到任何一次切换**，且超过 20–30 ms 抖动的比例极低（L219）。这为"把时延抖动分解为**几何分量**（换路）与**排队分量**（负载）"提供了前者的一条具体基线——任何声称"负载导致抖动"的工作都需要先减掉这一项。
- **给出一条可直接复用的离散化判据**（L140）：快照步长 $\Delta t$ 只有在区间内相对代价变化 $\ll1$ 时才有效。这条判据与"负载状态"的离散化同构——若把负载当作慢变量做快照式仿真，可套用同一条件（即负载在一个时隙内变化不能太大）。**反过来说，这也点明了快照范式的固有盲区：它把一个时隙内的任何动态（包括负载的瞬时波动）都抹平了。**
- 一句话：它是"负载维度为何在传统卫星路由里缺席"的**历史成因**——源头论文显式地把 minimax 流量目标推给了未来工作（L169）。

**10. 一句话评价**
**快照/虚拟拓扑范式的开创之作**：把"I SL 拓扑周期性时变"形式化为"离线建虚拟拓扑 + 跨时隙选路径序列"，并正确地把切入点选在**换路抖动**这个 ATM 面连接业务的真痛点上；但它从第一天起就把负载排除在模型外（L131、L169），因此它是"到达率/时延"这条线上游的**前提提供者**，而非贡献者。

## TSV3IE8S — An Adaptive Routing Algorithm for Inter-Satellite Networks Based on the Combination of Multipath Transmission and Q-Learning

**1. 一句话**
两个算法拼在一起：先用**改进 BFS** 一次性找出源到目的的全部最短路径，再按邻居节点的带宽权重与连接数之比挑一条（多路径分流）；当拿不到全局拓扑时，改用 **SDN 控制器做 agent 的表格型 Q-learning**（Q-routing），奖励函数把链路剩余带宽、时延、丢包率加权进去（L11、L36、L196）。

**2. 问题设定**
LEO 星间网络拓扑复杂且快变，作者认为**传统单条最短路已无法满足最优路径要求**，且单路径在流量上升时会拥塞（L11）；又因为低轨高度动态、**全局拓扑常常拿不到**，所以需要一种不依赖全局信息的自适应算法（L11、L89）。目标函数写得很明确（式2a，L134）：$\lambda\max_{(i,j)\in E}load_{ij}+(1-\lambda)\sum_k\sum_{(i,j)}x^k_{ij}d_{ij}$，即在**保证 QoS 的前提下平衡链路负载并尽量压低传输时延**，$load_{ij}$ 定义为链路上所有业务流带宽之和占链路带宽的百分比（L137）。

**3. 方法骨架**（前半是图算法，后半是**表格型** Q-learning，**不是深度 RL**）
- **多路径部分（第 2 节）**：基于邻接矩阵 $AdjMatr[i][j]$（式1，L50）做改进 BFS，逐层记录每个节点的最短跳数 $HopCount$、前向节点 $FrontPoint$ 与前向节点计数 $FrontCount$；四步流程覆盖"未入队/已入队但跳数更小/已出队"三种情形（L61-69）。再按前向节点**逐层回溯**得到源到所有节点的全部最短路（L76）。**选路准则**：若只有一条最短路就用它；若有多条，则优先取"邻居节点带宽容量最大"的路径，并用 $c(s)/w(s)$（连接数 / 带宽权重）衡量链路状态，选比值最小者——作者特意解释：只看"整条路径总占用率最低"可能会选中一条总负载低、但其中某个节点已接近阈值的路径，因此要**单独盯住源节点的邻居**（L83-85）。节点故障或拥塞时权重置 0、不再使用（L85）。
- **Q-learning 部分（第 3 节）**：
  - 架构：**SDN 控制器 = agent**，掌握全局网络状态并下发流表（L114、L202）。
  - **状态**：节点与链路的流量矩阵，代表当前链路负载；**动作**：把包转到哪个节点；**奖励**：式(2i) $R_{ij}=-cost+\alpha_1 BW_{ij}-\alpha_2 delay_{ij}-\alpha_3 loss_{ij}$（L196、L202）。
  - $BW_{ij}$ 用 **sigmoid 曲线**按剩余带宽给分：利用率 >80% 时奖励趋近 0，<30% 时趋近 100，中间平滑过渡（L191-193）；$delay_{ij}$ 与 $loss_{ij}$ 是相对全局最大值的归一化比例，取值 (0,100]（L193）。
  - **更新规则就是原版 Q-learning 的 max 目标**（式2g，L178）：$Q(s_t,a_t)\leftarrow(1-\alpha)Q+\alpha[R+\gamma\max Q]$——**没有用 Double DQN**。
  - 探索：ε-decreasing，$\varepsilon_\tau=\sqrt{1-[\tau/(4|\Lambda|)]^2}$（L173）。
  - MDP 设定：业务请求独立到达、业务类型概率服从**预设的泊松分布**；控制器在每个离散时隙决定**接受或拒绝**新请求，接受则分配最佳路径（L165）。
  - 终止条件：设最大执行时间 $t_{max}$，超时即终止路径分配；作者把它归入"无效策略集 $\Pi_{useless}$"但仍作为 agent 的一个选项（L213）。
  - 收敛性：援引 [21] 的有限样本收敛率与 [20] 的最优性来论证可收敛（L204）。

**4. 它声称的效果**（基线：传统单路径 BFS、Dijkstra、以及 [22] 的拥塞预防 Q-learning）
- 拓扑 16 节点（Fig 7），从 V7 到 V0/V9/V11/V3/V12/V13：**本算法共找到 16 条路径，BFS 只有 6 条**（每个目的节点仅一条）（L248-250）。
- 等待时延：**发送速率越大等待时延越长**；本算法在速率升到某阈值后会把业务分散到其他最短路上，从而减轻等待冲突（L256）。
- 丢包：**发送速率 <40 packets/s 时两者丢包率都极低**（数据量未达带宽容量）；速率上升后两者都升，但多路径算法显著低于单路径（L263）。
- 吞吐：随发送速率上升两者都升，本算法明显更好（L270）。
- Q-routing vs Dijkstra vs [22]（Fig 14/15）：**业务量小时 Q-routing 的路径最大负载最低**，Dijkstra 因反复用最短路而负载最高，[22] 在负载达 80% 阈值前与 Dijkstra 一致、之后绕行（L306）；对时延敏感业务（$\alpha_1=0,\alpha_2=1$），Q-routing 的平均传输时延低于 Dijkstra，且 80% 阈值前 [22] 与 Dijkstra 相同（L317）。
- 收敛：$\alpha=0.6,\gamma=0.3$ 时约 **30 步**收敛；$\gamma$ 增到 0.6/0.9 更快但仍有振荡；$\alpha$ 提到 **0.9** 收敛显著加快且波动更小（L290）；进一步改为**动态学习因子**（初值大、随迭代衰减）后收敛速度再提升（L297）。
- **必须说明的取证限制**：上述所有定量结果都只存在于 **Fig 8/9/10/14/15** 中，正文只给趋势描述、**没有给任何具体数值**；MinerU 的 MD 里图是图片引用，我读不到曲线取值。所以我能确认的是**方向**（多路径优于单路径、Q-routing 优于 Dijkstra），**不能确认幅度**。

**5. 它的实验条件**
- 拓扑：**16 节点的星间网络**（Fig 7），源节点取 V7（L243、L248）。
- **负载扫描（本批少见的到达率轴）**：业务数据包发送速率从 **10 packets/s 加到 100 packets/s**，仿真时长 **1 小时**（L243）。
- 两种业务分布：Fig 14a 源/目的节点固定；Fig 14b 源/目的节点随机（L306）。
- 奖励权重按实验切换：Fig 14 用 $\alpha_1=0.8,\alpha_2=0.2,\alpha_3=0$（偏重负载均衡）；Fig 15 用 $\alpha_1=0,\alpha_2=1,\alpha_3=0$（偏重时延）（L306、L317）。
- 基线：Dijkstra 最短路；[22]（Kim et al., 在 80% 负载时从最短路切换到 Q-learning 的拥塞预防机制，奖励函数简单：到目标给 30、到目标邻居给 20）（L302）。
- **未见**训练集/评估集划分的说明，也未见跨场景测试。

**6. 它自述的局限**（逐字）
**未见独立的 Limitations 章节**；以下是我读到的自认边界：
- L292："However, **speeding up the convergence rate of Q-routing routing needs further study.** At the beginning of training, a larger learning factor can improve the convergence speed of Q matrix. However, as the training level increases, **a larger learning factor causes the Q-matrix to move back and forth on both sides of the optimal point.**"
- L213（把"放弃"当成一个合法动作）："the SDN controller is required to plan an optimal path for the service flow within a time interval $t_{max}$, otherwise the path allocation is terminated. Although the termination search strategy **belongs to the invalid strategy set** $\Pi_{useless}$, it is still used as an option for the agent."
- L336（可复现性）："The data that support the findings are available **on request** from the corresponding authors. **The data are not publicly available due to privacy.**"
- L330："This research received **no external funding**."

**7. 它没做但看起来能做的地方**（基于内容）
1. **"卫星"只是名义上的**：全文只有一个 **16 节点抽象图**（L243、Fig 7），没有轨道高度、倾角、周期、ISL 构型，也没有跨缝或极区关链。所谓"星间网络"实际是一个静态 16 节点 mesh——**拓扑动态性在实验里完全没有体现**，尽管它正是论文的立项理由（L11、L89）。换成真实星座是最直接的补实验。
2. **表格型 Q-learning 无法扩展**：状态是流量矩阵（L202）、Q 表按状态-动作对存储（L99），星数上千时状态空间爆炸；文中未讨论任何函数逼近或泛化。
3. **"等待时延"被测量但没有排队模型**：图 8 的等待时延随速率上升（L256），但奖励里只有归一化的 $delay_{ij}$（L193），没有缓冲区/排队项——**"速率 → 排队时延"这条因果链没有被建模**，只是被观测。
4. **QoS 行为靠人工切权重实现**：所谓"对时延敏感业务更优"，是通过在 Fig 15 的实验里把 $\alpha_1,\alpha_2,\alpha_3$ 手动改成 0/1/0 达成的（L317），而 $BW_{ij}$ 的 sigmoid 形状也是手工设计（L193）。**agent 自己并不学习"该重时延还是重负载"**。
5. **它是 Double DQN 论文点名的那类算法**：式(2g) 用的是原版 max 目标（L178），没有做选择/评估解耦；在"以时延与负载为代价信号"的场景下，这正是 TAUEF8PF 警告会被高估扭曲的方向（TAUEF8PF L96）。

**8. 和同批其他篇的关系**
- 谱系上接**最古老的一支**：参考文献 [2] 是 **FSA（Chang et al. 1998）**（L346）——这一篇同时出现在 TRM2HPFN 的语境里（快照/FSA 谱系），也是 QSNRQ8PF 的 [45]（QSNRQ8PF L528）与 T9X6QCLL 的 [38]（T9X6QCLL L528，T9X6QCLL 的早期进展节把 FSA 与快照路由列为里程碑）。也就是说本批四篇（TRM2HPFN / QSNRQ8PF / T9X6QCLL / 本篇）通过 **FSA 与快照范式**这条线连着。
- 与 **TQF59BD7** 都属于"SDN 控制器集中决策"的一支，但 TQF59BD7 是真的分布式星上控制器 + 明确负载阈值实验，本篇是单控制器 + 16 节点玩具拓扑，**完成度差距明显**。
- 与 **TAUEF8PF** 是"被警告方"与"警告方"的关系（见第 7 条第 5 点）。
- 与 **S2QZRBEJ** 形成"仿真 vs 实测"的对照：本篇连排队模型都没有，而 S2QZRBEJ 直接测出负载把 RTT 从 50 ms 推到 100 ms。
- 参考文献 [3] 是 "Performance study of adaptive routing algorithms for LEO satellite constellations under **Self-Similar and Poisson traffic**"（L348）——**这是本批唯一一条指向"业务到达过程建模"的引用**，说明作者知道这条线存在但没有走进去。

**9. 对"负载变化下到达率/时延"的贡献**
**本批唯一给出明确"包到达率"扫描轴的一篇**（10 → 100 packets/s，L243），因此方向上最贴题，但**证据强度最弱**：
- **方向性事实（可引用）**：①**等待时延随发送速率单调上升**（L256）；②**丢包存在一个明显的拐点：速率 <40 packets/s 时两种算法丢包都极低，超过后都上升**，多路径显著更低（L263）；③吞吐随速率上升，多路径更高（L270）；④Q-routing 的平均传输时延随业务数上升而上升，且低于 Dijkstra（L317）。
- **"负载换收益"的机制**：Q-routing 在业务量小时路径最大负载最低，Dijkstra 因反复使用最短路而负载最高（L306）——这与 R37BNQQ8、SBCHGBCP 的结论方向一致。
- **但它对"到达率/时延"的可引用性很低**：所有数字都在图里、正文零数值；拓扑是 16 节点抽象图、无星座参数；没有排队模型；奖励权重人工切换。**那条 40 packets/s 的丢包拐点也无法换算成任何真实系统量纲。**
- 一条元信息：它引用的 [3] 说明"LEO 星座在自相似与泊松业务下的路由性能"这条线早在 2000 年就有人做（L348），但本篇并未承接。

**10. 一句话评价**
**BFS 多路径 + 表格型 Q-learning 的工程拼装（MDPI Processes）**：它有本批唯一一条真正的"包到达率"扫描轴（10→100 packets/s，L243），方向对得上"负载变化下的到达率/时延"，但**16 节点抽象拓扑、无排队模型、无星座参数、正文零数值**使它的证据强度停在"趋势正确、幅度不可用"；在方法谱系上，它是"把已有的多路径与 Q-learning 各取一半拼起来，两者都没改"。










