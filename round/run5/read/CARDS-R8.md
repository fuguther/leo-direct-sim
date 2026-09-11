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



