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





