# 读卡批次 R3

> 批次：8AYW2Y78 8N9QJHC2 9C6HB6AF 9FLZ88LZ 9GPFG5U3 9KZDXPKC A7QNRKML AF674CSF AIH4GK37 AJJI57M9 AZ72LM9Z
> 读法：读卡者逐字通读 VM MinerU MD 全文；行号对应 VM MD 行号。

## 8AYW2Y78 — Exploring the "Internet from space" with Hypatia (IMC '20, ETH Zürich)

**1. 一句话**
造了一台能算 LEO 星座"动起来"之后包级行为的 ns-3 仿真器（+ Cesium 可视化），并用它去量 Starlink/Kuiper/Telesat 三家 FCC/ITU 申报星座：结论是**路径与时延一直在变，而拥塞控制用的 loss 和 delay 两个信号在 LEO 里都不可靠**。

**2. 问题设定**
LEO 星座（h<2000km，周期 ~100 分钟，速度 >27000 km/h）的**核心基础设施本身在动**（L94），导致 GS-卫星链路只能维持几分钟就要切换（L86）、ISL 长度持续变化（L86）。而 2018 年 HotNets 三篇 position paper 指出了一堆挑战，却**没有工具能算出这些挑战到底多大**（L37："progress in precisely fleshing out these challenges and addressing them faces a substantial roadblock: lack of network analysis tools that incorporate the dynamic behavior of LEO networks"）。既有模拟器：SNS3 只做 GEO（L114）；ns-3 卫星移动模型只能转坐标（L114）；[6] 只看 hop 数和距离、不跑包（L114）。**受困者**：想做 LEO 拥塞控制/路由研究的人，只能在纸质假设上做。

**3. 方法骨架**（不是 RL，是"测量基础设施"）
- **星座建模**：从 FCC/ITU 申报里取 Keplerian 根数，自造 TLE（WGS72），用 pyephem 校验（L130, L132）。Table 1（L78）列三家的 shell 参数：Starlink S1 = 72×22 @550km i=53°；Kuiper K1 = 34×34 @630km i=51.9°；Telesat T1 = 27×13 @1015km i=98.98°。
- **ISL 互连**：默认 **4 条 ISL/卫星**，采用 "+Grid"（同轨前后 2 条 + 相邻轨 2 条）网格（L136, L138）。
- **GSL 建模的化简**（L142-L152，逐条列出）：每个卫星/GS 一个 GSL 网卡；**星间与地面之间互不干扰**（L146）；GS 可配"连多星"或"只连最近星"（L148）；切换**无丢包**（L150）。
- **转发状态**：**每 100 ms** 重算一次（默认），用 networkx 建图 + **Floyd-Warshall 最短路**，把状态变化塞进 ns-3 事件队列当静态路由表用（L154, L156）。这是**"连续运动离散化"**，作者明确说会造成实际路径偏离最短路（L154）。
- **流量**：§3.4 可扩展性测试用"100 座人口最多城市互发随机置换"（L179）；§4 用 ping（每 1 ms 一次）+ 单条 TCP（L205）；§5.4 用 100 城市随机置换的长流 TCP（L333）。

**4. 它声称的效果**（全部给定条件）
- **可扩展性**（Fig 2, L159/L191）：TCP 9.2 Gbit/s 全网 goodput 跑 1 虚拟秒 ≈ 555 真实秒；UDP 13.8 Gbit/s ≈ 269 秒。要跑 ~10 Gbps × 10 虚拟秒 ≈ **UDP 33 分钟 / TCP 100 分钟**（L191）。瓶颈在逐包事件处理，不在网络规模（L193）。单核 2.26GHz Xeon L5520（L179）。
- **RTT 波动**（Fig 3, L207/L211）：Rio–St. Petersburg 在 t=32.9s 换路，RTT 从 **96 ms 跳到 111 ms**；Manila–Dalian min 25 / max 48 ms（≈2×）；Istanbul–Nairobi 47–70 ms。且实测 ping 与 networkx 快照计算**基本重合**，尖峰来自转发状态陈旧导致"绕路"（L207）。
- **断连**：St. Petersburg 在 t=155–165s 看不到足够仰角的 Kuiper 卫星，链路直接断（L209, L364）。
- **拥塞控制**（Fig 4/5）：**在完全没有竞争流量的情况下**（L239），NewReno 把队列填满推高时延；Vegas 在 ~33–35s 把时延上升误判为拥塞，cwnd 暴砍、吞吐崩掉（L231, L247）。另有一处 ~140s cwnd 被**减半，但没有丢包**——纯粹是重排序造成的（L222, L243）。
- **Constellation-wide**（Fig 6）：>80% 连接的最大 RTT < 2× 几何光学极限（L268）。反直觉发现：**卫星最少的 Telesat 时延最低，Starlink 反而比 Kuiper 高**（L270），原因是 Telesat 最小仰角只取 10°（vs Starlink 25°、Kuiper 30°）和轨道结构差异（L272-L274）。
- **路径 churn**（Fig 8, L304-L308）：200 s 内中位数 Starlink/Kuiper **4 次换路**、Telesat 2 次；10% 连接 ≥7 次；Starlink 超 1/3 连接的路径比最少跳数多 ≥2 跳；>10% 连接跳数变化超 50%。
- **时间步粒度**（§5.3, L325）：100 ms 步长漏掉 0.4% 连接的路由变化，1000 ms 漏 6%；100 ms 是折中（L327）。
- **带宽波动**（§5.4, Fig 10, L339）：**流量矩阵固定 + 路由策略固定（最短路）**，仍有 **31% 的时间超过 1/3 容量闲置**（对照：把拓扑冻结在 t=0 只有 11%）。原因是交叉流量的构成在随时间漂移（L341）。
- 可视化：跨大西洋 ISL 是热点（L387, L422）。

**5. 实验条件**
- 拓扑：三家申报星座的首壳（S1/K1/T1），GS = 全球 100 座人口最多城市（L262）。
- 规模：Kuiper K1 = 34×34 = 1156 星；Starlink S1 = 72×22 = 1584 星。
- 负载设定：§4/§5.4 把**每条链路容量强行压到 10 Mbps** "to allow us to scale the experiment"（L333）；队列 100 包 = 10 Mbps/100 ms 的 1 个 BDP（L189, L241）。
- 仿真时长：RTT/路径分析 200 s（L203）；§4 的 RTT 分析说 200 s 对 Kuiper 尺度"足以覆盖几乎全部变化范围"（L203）。
- 训练/评估：无训练。评估是单一仿真配置，**没有对到达率或负载强度做扫描**——§3.4 虽然提到"改变链路速率来控制 goodput"，但那是为压测仿真器速度，不是负载敏感性实验（L179, L191）。

**6. 它自己承认的局限**（逐字引用）
- L391："Hypatia is only the first step in building up research infrastructure for a new breed of networks. It has several under-developed pieces, including some where the sparsity of publicly available information was limiting for us."
- L393："The most under-developed aspect is the radio GS-satellite segment design."
- L146："Across satellites and ground stations, no connections interfere with each other. While this is a strong assumption, Starlink and Kuiper mention [47, 68] that frequency management will be software-defined..."
- L152："We make these simplifications, which relax practical constraints and are favorable to LEO networks"
- L602（附录 A）："We thus caution readers against drawing deeper conclusions on TCP behavioral differences in bent-pipe versus ISL connectivity from this small experiment"
- §5.1 还主动劝阻把结果读成"Telesat 设计更好"，指出申报材料有"抢占频谱"动机（L298）。

**7. 它没做但看起来能做的地方（基于内容）**
1. **全篇没有负载/到达率扫描**。§5.4 恰恰证明"流量矩阵固定也会出现 31% 闲置带宽"，但下一步"把流量矩阵乘上一个倍数看看时延怎么涨"没做——而这正是它自己论证的"交叉流量漂移"的直接推手。
2. **只有最短路路由**（L156）。它自己在 L387 说跨大西洋热点"indicates that there will be substantial value in using non-shortest path and multi-path routing"（逐字），却把多路径留给未来工作（L399 "Work on multi-path routing and congestion control will also require some modifications to Hypatia"）。**这句逐字宣言就是后续所有 LEO 路由 RL 论文的出发点**。
3. **时间步是全局同步的固定 100 ms**，作者承认"only be inaccurate ... for at most 1% of the time"（L327），但没说能否按需自适应加密——这是所有后续"预测式路由"论文的隐含前提。
4. **队列配置是单队列**（附录 A 里 ACK 与数据抢同一队列，L598）。它自己说"multiple separate queues for uplink traffic would change the behavior substantially"（L602）——没做。
5. 三个星座只做首壳；多壳（S2-S5）与跨壳路由未测（L260）。

**8. 和同批其他篇的关系**
本批的**共同祖先**：它是 LEO 网络"包级仿真 + 时变拓扑"的开山基础设施，后续论文大概率直接引用它或引用它的对手（Handley 的 HotNets 系列 [29][31]，L486/L490）。与 RL 类论文的差别在于：它是**测量/仿真工具**，不含任何学习或决策算法，路由是 Floyd-Warshall 最短路（L156）。是否被本批其他 10 篇引用：**待读完本批后回填**（先记：若后续论文跑 LEO 时变拓扑实验而不用 Hypatia，需注意仿真器差异）。
*[回填位：读完本批后补]*

**9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实**
贡献的是**反面事实**，而且很关键：**在负载完全不变的情况下，时延照样剧烈波动**（换路 96→111 ms，L207；Starlink 中位 RTT 波动 ~10 ms，L276）。也就是说 LEO 里"时延上升"不等于"到达率上升造成的排队"——delay 作为拥塞信号被结构性污染（L254, L256 逐字："Both loss and delay can be poor signals for congestion control in LEO networks"）。另外给定固定流量矩阵，仍有 31% 时间 1/3 容量闲置（L339），说明**容量利用率对"负载"并不单调响应**。但**它没有做任何到达率扫描**：没有"λ 从 X 涨到 Y，时延/丢包如何变化"的曲线。所以对"负载变化的响应"本身，本篇是**空白**；它提供的是这条曲线的"噪声底"。

**10. 一句话评价**
把"LEO 时变拓扑"从 position paper 的猜想变成可测量实验事实的**基础设施论文**，它的最大遗产不是任何一条结论，而是 L387 那句"应该用非最短路/多径路由"的留白——后续整个 LEO 智能路由方向都在填这个坑，而它自己只提供了测量尺子。

## 8N9QJHC2 — Recovery Routing Based on Q-Learning for Satellite Network Faults (Complexity/Hindawi, 2020, BUPT)

**1. 一句话**
先用**贝叶斯决策**把卫星链路的故障**分成"临时干扰"和"端口永久损坏"两类**并定位到端口粒度，再用一张每节点维护的 **Q 表**做差异化重路由——本意是"别因为一次临时干扰就把整颗星绕开"。

**2. 问题设定**
空间环境里有两类故障（L25）：(i) 带电粒子在天线外形成"壳"临时阻断信道 → 干扰消失即自愈的**临时链路故障**；(ii) 极寒无大气保护下设备被高能粒子击中 → 需人工维修、无法自愈的**永久故障**。而传统抗毁路由的毛病是（L27, L39）：**把故障节点当成一个整体**而不是按端口处理，于是"避开坏节点、找个邻居替它、或者把整条路径重路由"，结果**一个还有 3 个正常端口的卫星被整个弃用**；加上不区分两类故障，**会把完全正常的节点在恢复时丢掉**，导致故障涉及节点的利用率低、抗毁路由找不到最优路径。

**3. 方法骨架**

**(A) 故障检测 IDBB（第 3 节）**——不是 RL，是贝叶斯 + 两阶段：
- 输入变量（L49-L59）：邻接矩阵 V、链路集 L、**Δt 内成功通信的路径集 M**、可达区 R / 不可达区 R̄ / 未知区 U。
- 目标函数式 (1)(2)（L66, L72）：链路为永久故障的后验概率 $p_{di} = (2\sum_{u=1}^{g}\frac{u}{g}p_{d_u})^2 \cdot \frac{p_d\{R,\bar R | l_i=0\}}{p_d\{R,\bar R\}}$，临时故障同理（$p_{ll}$ 替换）。式 (3) 保证两类先验不同，式 (4) 保证两类事件独立（L91）。
- **关键工程点**：**只用"成功传输的路径"做信息采集**（L111-L113），不广播测试包（对比 SLD/DFDS 的"broadcast test task"，L302），把检测开销压下来。
- 区域划分算法 (3)(a)-(g)（L117-L130）：以失败路径的发送端为 R 的种子、接收端为 R̄ 的种子，用成功链路集合 C 做**可达性泛洪扩张**，剩下的进未知区 U。
- **阈值判决而非最大后验**（L29, L295）：作者强调"Unlike the maximum a posteriori probability decision in general Bayesian decision theory, by setting the posterior probability index threshold, multiple failed link detection results can be output"——即允许一次输出多个疑似故障链路，以适配多故障场景。
- 第 7 步按**故障率 20%** 分岔（L158）：<20% 走第一阶段分类，>20% 走第二阶段（利用**极轨星座的缝区/非缝区特性**和拓扑变化后的新邻居节点做再判别，L164）。

**(B) 路由恢复 MFDR（第 4 节）**——Q-learning：
- **状态（L184）**：二维 $(n_i, d_k)$ = 当前节点 × 目的节点（不是"链路状态"）。
- **动作（L186）**：$Y(V,n_i)$ = 当前节点的邻居集合。
- **Q 表（Table 1, L191）**：每节点一张表，行=邻居 $y_z$，列=目的 $d_k$，表项 $Q_i(d_k,y_z)$。
- **回报（L31, L263）**：$r = -(t_q + t_t + t_n - t_c)$，由**排队时延 $t_q$、传输时延 $t_t$、和链路存活相关项**组成；$t_n$=当前时刻，$t_c$=链路预计发生变化的时刻，$t_k$=链路保持连通的总时长。
- **折扣因子（L263）**：$\gamma = [(t_c - t_n)/t_k]^3$ —— **折扣因子随链路剩余寿命衰减，且取三次方**。这是本篇最独特的设计：越接近断链的链路，折扣因子越小，Q 值传播越弱，从而"减少网络动态对路由结果稳定性的影响"（L31）。
- **更新（式 15, L263）**：标准 Q-learning，$Q^{new} = Q^{old} + \alpha[r + \gamma \max Q_{y_z}(d_k,y_m) - Q^{old}]$，max 算子、带学习率 α。
- **故障时的特殊更新（式 14, L248）**：把故障方向的 Q 直接置 $-\infty$：$Q_F^{odd}(d_i,F')=-\infty$、$Q_{F'}^{odd}(d_i,F)=-\infty$，同时只更新两端节点 F/F' 及其**剩余邻居** Y/Y' 的 Q 值——**局部更新**，不是全网重路由。
- **架构（L237-L239）**：地面站**下发** Q 表、γ、α 给卫星；卫星**上报**实时排队时延 $t_q$。**是"地面集中配置 + 星上局部更新"的混合体**，不是纯分布式。
- 约束式 (12)（L212）：$\Delta t \le t_c - t_n \le \max t_k$ —— 保证"在网络拓扑变化前把相关节点的 Q 表更新完"。

**4. 它声称的效果**（全部给定条件）
- **检测准确率**（Fig 3, L282）：故障率 **<10% 时 IDBB 第一阶段略低于 SLD/DFDS**；**>10% 时显著反超**；按最终输出算，IDBB 明显更好。
- **检测完备率**（Fig 4, L293）：<10% 时三者几乎 100%；**>40% 时 DFDS 与 SLD 显著下降，而 IDBB 在故障率 60% 时仍保持 >90%**。
- **检测开销**（Fig 5, L300）：4 种网络规模 × 4 种故障率（15/25/35/45%）下，IDBB 的通信开销**远小于** DFDS 和 SLD；SLD 又小于 DFDS。同一规模下 IDBB 开销随故障率上升而上升。
- **故障分类准确率**（Fig 6, L317）：第一阶段在**故障率 <15% 时 >80%**，**>20% 时急剧下降**；第二阶段准确率高（作者归因于拓扑变化后的新邻居检测）。
- **恢复路径时延**（Fig 7, L330）：Beijing→Los Angeles，第 34 分钟注入故障。故障发生后三者时延都明显上升；**MFDR 的时延大于 BPRP、小于 LRRS**；BPRP 立即恢复稳定波动；**MFDR 在 37 分钟后**恢复（因为要等拓扑变化来识别临时故障）；**稳定后 MFDR 的路径时延最小**。
- **有效资源利用率**（Fig 8, L336）：MFDR 在**所有故障率下都优于** BPRP 和 LRRS；故障率低时优势尤为明显；随着故障率上升，BPRP/LRRS 利用率**略升**而 MFDR **略降**；LRRS 始终略高于 BPRP。

**5. 实验条件**
- **检测实验（§5.1）**：**6×6 静态拓扑**（L278 逐字："The topology adopts a static topology"），随机设 30 条流，链路时延 ~20 ms，信息采集窗口 Δt = 3 s。先验：链路故障 0.1，卫星 4 端口故障概率分别 0.08/0.005/0.001/0.0005；阈值：链路 0.01、端口 0.002；分类阈值 0.0001 / 0.0015（L276-L278）。**注意：故障检测实验用的是静态拓扑**，与"卫星网络拓扑周期变化"的卖点脱节。
- **路由实验（§5.2）**：自研仿真平台 [31]，仿真 6000 s，**故障在第 2040 s（第 34 分钟）注入**，采样间隔 60 s；北京（117°13′E, 40°05′N）发 → 洛杉矶（120°26′W, 34°05′N）收；路径上设两条故障链路（一条端口永久故障、一条介质干扰临时故障）（L321, L328）。
- **资源利用率实验**：20 个地面站终端（10 发 10 收），仿真 1200–3000 s 共 1800 s，**每个故障率下重复 20 次取平均**（L334）。
- **训练与评估**：Q-learning 是在同一次仿真里在线跑的，**没有独立的训练/测试划分**，也**没有跨拓扑泛化测试**。

**6. 它自己承认的局限**（逐字引用）
**未见自述局限章节**。读遍全文：第 6 节 Conclusions（L354-L362）只列 3 条优点，无任何 limitations 措辞；无 Discussion/Future Work 节；唯一近似免责的是数据可用性：
- L366："The software codes used to support the findings of this study are available from the corresponding author upon request."（**代码不公开**）
作者只在结果解释里承认了若干弱点，例如 L132："This assumption will cause an increase in suspected faulty links compared to the original definition, and the accuracy rate may decrease."（假定失败路径的接收端属于不可达区 R̄ 会引入误判），以及 L342 承认故障率升高时第二阶段分类变差会**拖累 MFDR 的资源利用率**。

**7. 它没做但看起来能做的地方（基于内容）**
1. **故障检测用静态拓扑，路由用动态拓扑**（L278 vs L321）——检测机制声称利用了"卫星网络拓扑的周期性"（L41），却在静态拓扑上验证。**用真实时变拓扑重跑检测实验**是最直接的缺口。
2. **γ 的"剩余寿命三次方"假设链路寿命 $t_k$ 和变化时刻 $t_c$ 是已知的**（L263）。极轨星座可以预测，但论文没有说明这个预测从哪来、误差多大，也没有做预测误差的敏感性分析。
3. **故障率扫描有了（15/25/35/45%），到达率/负载扫描完全没有**。而回报函数里明明有 $t_q$（排队时延，负载的直接反映），却从没让负载变过。**"负载变化下的时延"这条轴是空的**。
4. **只比了故障恢复类基线（BPRP/LRRS），没比任何 RL 路由基线**。它自称是"基于 Q-learning 的路由"，但同领域后来的 DRL 路由（如 [28] Boyan & Littman 的 Q-routing 血统）没有对照。
5. **20% 故障率分岔阈值、0.01/0.002/0.0001/0.0015 等一堆阈值全是手工设定**（L158, L278），作者说"derived based on the following simulation results"（L158），即**用测试集调参**，且无敏感性分析。
6. **仿真时长 6000 s 但只注入一次故障**（L321），没有多故障并发/级联场景，尽管相关工作里作者自己研究过级联失效 [22][23]（L422-L424）。

**8. 和同批其他篇的关系**
- **血统上是"最老的一支"**：它引的 RL 源头是 **Boyan & Littman 1993 的 Q-routing**（L434 [28]："Packet routing in dynamically changing networks: a reinforcement learning approach"）——这是所有 Q 路由论文的祖师爷，本批其他 RL 论文大概率共享这条谱系。
- **不像**本批的 DRL 论文：它是**表格型 Q-learning**（状态是"节点×目的"的离散对，不是神经网络的连续状态），没有 DNN、没有经验回放、没有 actor-critic。
- **像** S85KQ4FC 的地方：都把**排队时延**放进奖励；但 S85KQ4FC 是逐包 DNN 推理，本篇是逐邻居查表。
- 关注的失效模式不同：本篇关心**硬件/干扰故障**，S85KQ4FC/Hypatia 关心**拓扑运动与拥塞**。
*[回填位：读完本批后补：是否被本批其他篇引用]*

**9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实**
**几乎没有直接贡献**，而且有一处反例值得记：它在奖励里放了排队时延 $t_q$（L239, L263），说明作者清楚"负载→时延"这条链，但**整个实验没有让负载变过一次**——扫的是**故障率**（15/25/35/45%），不是到达率。它给出的"时延"曲线（Fig 7）是**故障注入前后**的时延恢复过程，第 34 分钟凸起、37 分钟复原，**与到达率无关**。
唯一可迁移的事实是：**故障率升高时探测开销随故障率线性上升**（L300）——但这也不是到达率。另外 γ 用链路剩余寿命调制，本质上是把"链路即将断开"这一**非负载型时延来源**纳入决策——这与 Hypatia 的"delay 不是可靠的拥塞信号"（8AYW2Y78 的 L254）是同一现象的另一面。

**10. 一句话评价**
把 **1993 年的 Q-routing 表格法搬到卫星故障恢复**上、并配了一个相当工程化的贝叶斯两阶段检测器——**创新点在"故障分型"而不在"学习"**；Q-learning 部分基本是教科书式实现，唯一非平凡的设计（剩余寿命三次方折扣）缺乏验证，且检测与路由的实验条件互相脱节。

## 9C6HB6AF — Deep Reinforcement Learning-Based Multipath Routing for LEO Megaconstellation Networks (Electronics 2024, 13, 3054, Space Engineering University)

**1. 一句话**
把"多径路由"拆成**两条互不干扰的子问题**——先用纯几何公式离线算出 L 条最小跳数路径（MHMRD），再用一个 **GNN+PPO** 的中央智能体决定每条流在这 L 条路径上的**分流比例 ω**（GMTS），卖点是"换星座不用重训"。

**2. 问题设定**
MCN 里想用多径提升吞吐/容错，但两个卡点（L38, L40）：
1. **路径发现在时变拓扑里失效**：卫星姿态变化与复杂电磁环境会让激光链路速率下降甚至中断，所以"链路失效在 MCN 里是常态而非例外"（L38 逐字："link failures may occur frequently in MCNs rather than being an exceptional event, as in terrestrial networks"）；AODV 这类广播式按需路由开销爆炸；而且"发现出来的路径可能在真正传数据时已经不存在了"（L38）。
2. **流量调度缺有效信息**：链路质量波动 + 地面流量时变，"fine-grained traffic scheduling between multiple paths frequently lacks effective information"（L40）。
**第三层动机是最关键的**（L40, L42, L66）：**传统 DRL 路由"与输入状态和拓扑强耦合"，星座一变就得重训**——状态维度随星座规模和流量需求急剧膨胀，可扩展性差。GNN 被请来正是为了解决"换个规模的星座就要重训"。

**3. 方法骨架**

**(A) 系统模型（第 3 节）**：Walker Delta N_S N_P/N_P/F，每星 **4 条 ISL**（2 条同轨 + 2 条异轨，L77）。SDN 架构：**NCC 做统一拓扑管理、流量调度、路径控制**（L77）。
- 时延式 (1)（L86）：η = Σ(排队时延 q + 包处理时延 r + 传播时延 γ/c)。
- 分流约束式 (2)（L92）：Σ_l ω_{m,l} = 1。
- 效用函数式 (6)（L118）：U = β1·log(f̄) − β2·log(d̄)，β1+β2=1。
- P0 是 NP-hard，拆成 P1（路径发现）+ P2（流量调度）（L139）。

**(B) MHMRD 路径发现（§4.1）——纯几何解析解，不是学习**：
- **异轨跳数** H_h 由 RAAN 差决定：式 (12)(13)（L174, L178），ΔΩ = 2π/N_P 是常数。
- **同轨跳数** H_v 由相位角差决定，式 (14)-(20)（L188-L216），分**东南/东北/西南/西北四个方向**分别算。
- 端到端最小跳数式 (21)（L224）：四种组合取最小。
- **备份路径生成机制（L227）**：算每条链路的**占用频次** F_{a,b}，设阈值 ξ_ε；占用低的链路权重 m ∈ [r1,r2]，占用高的 ∈ [r2,r3]；**把已选路径的链路从图里删掉**再找次优——这是标准的**链路分离（disjoint）多径**做法。复杂度 **O(N log N)**。
- **关键细节（L156）**：备份路径按**业务量降序**分配——"This is because centralized traffic is more likely to cause bottleneck link congestion than decentralized tiny traffic."（业务量大的流优先拿到备份路径）。

**(C) GMTS 调度（§4.2）——GNN + PPO**：
- **状态式 (24)（L282）**：s_t = [C_t, TR_t, G_t, P_t] = **链路剩余带宽 c_i = BW − f_i（式 23, L276）** + **流量需求矩阵 TR** + **GNN 图结构 G_t** + **路径矩阵 P_t**。
- **动作式 (25)（L292）**：a_t = [ω_{1,1}, ..., ω_{M,L}] —— **连续动作空间**（每条流在 L 条路径上的分流比例）。注意 §2.2 里作者自己批评 DDPG-TE "not applicable to arbitrary satellite constellations, as the dimensions of the state and action spaces are constrained by the size of the input topology and traffic matrices"（L437）——**而 DMR 自己的动作维度同样 = M×L，也是随星座/流量规模变的**，这个矛盾论文没有处理。
- **奖励式 (26)（L302）**：r_t = Σ_m Σ_l U(f̄_{m,l}, d̄_{m,l})，**直接复用效用函数**（吞吐 + 时延）。
- **算法（§4.3）**：PPO（actor-critic），但实现细节是 **DQN 式**的：经验回放 + **优先经验回放（PER）**，TD 误差式 (33)、采样概率式 (35)、IS 权重式 (36)、critic 损失式 (38)、actor 损失式 (39)。目标值式 (32)（L338）：y_i = r_i + ρ(1−χ)·Q(s_{i+1}, a_{i+1}|θ^Q)。
  - **注意矛盾**：摘要/L266/L478 都说 "PPO, actor-critic"，但 Algorithm 2 与式 (32)-(39) 完全是 **DQN + PER** 的写法；§6 结论文又说 "Each routing node is controlled by a **DQN agent**"（L478）。**全篇在 PPO / DQN 之间自相矛盾**。
- **复杂度**：Algorithm 1 O(N log N)，Algorithm 2 O(L)（L335）。

**(D) 工作流（§4.4, L410）**：NCC 按时隙（拓扑在一个时隙内视为稳定）预先算好 L 条路径 → 训练好的 GMTS 生成分流比例 → **在时隙开始前下发给对应卫星**。

**4. 它声称的效果**（全部给定条件）
对照基线 4 个（L431-L437）：**SPF**（最短路）、**NCMCR**[24]（网络编码多径协作路由）、**AMBRLB**[38]（蚁群多径负载均衡，来自 MANET）、**DDPG-TE**[39]（DDPG 流量工程）。
- **吞吐（Fig 6, L443）**：Iridium 上业务量达上限时，DMR 比 SPF **+30.26%**、比 NCMCR **+8.45%**；OneWeb 上流量 8 Gbps 时，比 SPF **+42.64%**、比 NCMCR **+9.55%**。吞吐随流量上升而上升但**增速逐渐放缓**。
- **流完成率（Fig 7, L454）**：8 Gbps 时 Iridium 上比 SPF **+17.39%**、OneWeb 上 **+11.52%**；OneWeb 上比 NCMCR/AMBRLB/DDPG-TE 分别 +1.98% / +2.58% / +6.49%。**大星座（OneWeb）的完成率始终高于小星座（Iridium）**，作者解读为"大规模星座处理高负载的优势"。
- **端到端时延（Fig 8, L465）**：**低负载下 SPF 的端到端时延最低**（因为全网正常时它总走最短路）；**高负载下 SPF 无法动态绕开拥塞路径**。Iridium 上 DMR 比 SPF 降 **3.67%**、比 NCMCR 降 1.78%、比 DDPG-TE 降 1.86%、比 AMBRLB 降 0.86%。**OneWeb 上 DMR 的时延在高负载时与 NCMCR/AMBRLB/DDPG-TE 接近**，"between those of SPF and DDPG-TE"。作者自己解释（L465）："in large-scale constellations, there are always sufficient alternative routes, and the improvement in end-to-end delay metrics is not substantial."
- **泛化（最关键的一条）**：OneWeb 上**DMR 直接复用 Iridium 训练的同一个模型**，而**其他算法都针对新网络重训了**（L443 逐字："DMR employed the same model as that used for the Iridium constellation, while the other algorithms were retrained based on the characteristics of the new network"）。

**5. 实验条件**
- **仿真器**：NS-3 实现路由计算与多径调度（L421）。
- **拓扑**：Iridium（66 星，6 轨 × 11 星，780 km，i=90°，N_G=16）与 OneWeb（648 星，18 轨 × 36 星，550 km，i=53°，N_G=16）（Table 1, L424）。
- **流量**：**基于地面流量密度生成的 traffic dataset，源-目的节点对 50 个**（L421）；训练用的拓扑与流量矩阵来自 **MAWI 真实流量归档**（L429, L582）。
- **超参**（Table 2, L427）：包 1KB、N_B=32、B_max=100、PER 的 α=0.6、β/ρ=0.5。
- **负载扫描**：**这是本批少见的做了负载扫描的论文**——横轴是 traffic intensity / total service volume，从低到 8 Gbps（L443, L454, L465）。
- **训练与评估**：训练用"倾斜轨道星座拓扑与流量矩阵"（指 Iridium），**评估在 Iridium 和 OneWeb 两个星座上做，OneWeb 上不重训**（L443）。这是明确的**跨星座泛化评估**，不是同分布测试。

**6. 它自己承认的局限**（逐字引用）
论文**没有专门的 Limitations 节**。唯一近似自述的是结论最后一段（L480）：
- "It should be noted that as the size of the constellation continues to expand, the computational requirements of DQN-based online routing also rise. In the future, we intend to explore the potential of adopting solutions such as multi-controller deployment to enhance the responsiveness of the network and further validate its efficacy in real-world scenarios."
（注意这句又把它自己的算法叫 **DQN-based**，与摘要的 PPO 矛盾。）
另有一处变相承认，在结果解释里（L465）："in large-scale constellations, there are always sufficient alternative routes, and the improvement in end-to-end delay metrics is not substantial."——即**大星座上时延收益很小**。

**7. 它没做但看起来能做的地方（基于内容）**
1. **PPO / DQN / actor-critic 三者自相矛盾**（L266 vs L338-L403 vs L478）。式 (39) 的 L_μ = −Q(s,a|θ^Q) 不是 PPO 的 clip 目标。**先把这个搞清楚，否则方法不可复现。**
2. **动作维度仍是 M×L，随星座规模变**（式 25, L292），与它批评 DDPG-TE 的理由（L437）完全同构。它声称 GNN 解决了可扩展性，但 **GNN 只解决了状态侧的图结构输入，没解决动作维度**。这是论文最大的逻辑缺口。
3. **MHMRD 是纯几何解析解，与时延/负载无关**。它只按跳数选路（式 21），占用频次阈值 ξ_ε 也是启发式（L227）。**负载完全通过 GMTS 的分流比例体现，路径集合本身对负载是盲的**。可以做"负载感知的多径集合生成"。
4. **L（候选路径数）没有说明取值**，也没做 L 的敏感性分析——多径数量本身是吞吐/时延权衡的核心旋钮。
5. **NCC 是单点**（L77），作者自己在 L480 承认要未来搞多控制器。**NCC 的响应时延没有建模**——这与它引用的 SDN "centralized control approach is susceptible to high latency issues"（L60）是同一个坑。
6. **时隙内拓扑视为稳定**（L410），但没说时隙多长、多长时隙会破坏这个假设。而 Iridium（极轨，高动态）正是最考验这个假设的场景。
7. **只有 50 个源-目的节点对**（L421），相比星座规模（648 星）是很稀疏的负载。

**8. 和同批其他篇的关系**
- **和 8AYW2Y78 (Hypatia) 直接对手戏**：Hypatia 在 L387 逐字说"应该用非最短路/多径路由"，DMR 就是来填这个坑的，而且它真做了 load 扫描（Hypatia 没做）。但 **DMR 用 NS-3 自建而非 Hypatia 的框架**（L421），且星座是 Iridium/OneWeb 而非 Starlink/Kuiper/Telesat。
- **和 S85KQ4FC 形成互补对照**：S85KQ4FC 是**逐包/逐流 DNN 推理的星上决策**，DMR 是**NCC 集中式、时隙级粗粒度**的分流决策。S85KQ4FC 关心"推理成本"，DMR 关心"换星座要重训"。
- **不像 8N9QJHC2**：后者是表格 Q-learning + 故障分型；本篇是 GNN+DRL 的连续动作多径调度，两者唯一交集是把"排队时延"放进目标。
- **引用关系**：它引了 [12] Huang et al. "Pheromone Incentivized Intelligent Multipath Traffic Scheduling"（TWC 2022）与 [11] Huang et al. "GNN-Enabled Multipath Routing"（TVT 2024）——**这两篇极可能在 111 篇库里**，若在，需交叉核对谁是"GNN+多径"的首创。它引的 DDPG-TE [39] 也是本批可能的重叠基线。
*[回填位：读完本批后补]*

**9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实**
**这是本批目前唯一真正扫了负载的论文**，而且给出了三条对"负载-时延"关系有用的具体事实：
1. **负载-时延单调上升，但机制是"绕路"而非纯排队**：L465 逐字 "As the network load increased, the queuing delay also rose, with more flows transmitted along the candidate paths with higher hop counts."——**负载升高 → 被推到跳数更多的路径上 → 时延上升**。这解释了 LEO 多径里时延上升的一部分来自"路径变长"而不是"队列变长"。
2. **低负载时最短路最优、高负载时最短路崩溃**（L467）：SPF 低负载时延最低，但吞吐和完成率最低，且高负载下性能快速恶化。**这是"负载区间决定最优策略"的直接证据**。
3. **星座规模会调节负载-时延曲线**：OneWeb（648 星）上 DMR 的时延改善不显著，因为"替代路径总是足够多"（L465）；完成率则大星座始终高于小星座（L454）。
**但它的"负载"是业务量总量（service volume / traffic intensity，到 8 Gbps），不是到达率 λ**；而且是**时隙级平均**，看不到瞬态。所以对"到达率突变下的时延响应"仍是空白。

**10. 一句话评价**
**把 GNN 用来解决"换星座要重训"这个真问题上、并且是全批少数真做了负载扫描的多径调度论文**，但方法学上有一处硬伤——**动作空间维度照样随星座/流量规模增长，与它批评 DDPG-TE 的理由完全同构**，且 PPO/DQN 的算法描述前后矛盾（式 32-39 是 DQN+PER 的写法，L478 也自称 DQN），复现性存疑。
