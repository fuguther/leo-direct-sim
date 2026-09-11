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

## 9FLZ88LZ — QMIX: Monotonic Value Function Factorisation for Deep Multi-Agent Reinforcement Learning (ICML 2018, Oxford/Whiteson)

**1. 一句话**
证明做"集中训练、分散执行"（CTDE）**不需要把联合 Q 值拆成各智能体的和**（VDN 的做法），只要保证 Q_tot 对每个 Q_a **单调**就够了——具体做法是让混合网络的权重恒非负（由 hypernetwork 生成），于是分散执行时各智能体仍然只需对自己的 Q_a 取 argmax。

**2. 问题设定**
团队协作任务里，智能体必须**分散执行**（只看自己的局部观测），但**训练时通常能拿到全局状态**（L22 CTDE 范式）。问题是：联合动作值函数怎么表示？
- **一个极端 IQL**（L26）：每个智能体独立学自己的 Q_a，无法显式表达智能体之间的交互，且因为别人也在学，环境非平稳，**可能不收敛**。
- **另一个极端 COMA/全集中**（L28）：学一个完整的 Q_tot(s,u)，但需要 on-policy（样本效率低），而且"训练全集中 critic 在智能体超过一小撮时就不可行"。
- **中间 VDN**（L30）：Q_tot = Σ Q_a，分散策略自然产生（各自贪心），但 **"VDN severely limits the complexity of centralised action-value functions that can be represented and ignores any extra state information available during training"**（L30 逐字）。
**核心洞察（L32）**：从 VDN 的**完全分解**退到 QMIX 的**单调性约束**——只需要全局 argmax 与各自 argmax 一致即可。

**3. 方法骨架**

**问题形式**：Dec-POMDP 七元组 G = <S, U, P, r, Z, O, n, γ>（L62）。每个智能体有动作-观测历史 τ^a，策略 π^a(u^a|τ^a)。所有智能体**共享同一个奖励函数** r(s,u)（L62）。

**核心约束式 (5)（L113）**：∂Q_tot / ∂Q_a ≥ 0, ∀a ∈ A

**等价条件式 (4)（L105）**：argmax_u Q_tot(τ,u) = ( argmax_{u^1} Q_1(τ^1,u^1), …, argmax_{u^n} Q_n(τ^n,u^n) )

**三层架构（L116-L124）**：
1. **Agent networks**：每个智能体一个，用 **DRQN** 实现，输入是当前局部观测 o_t^a 和上一个动作 u_{t-1}^a（L118）。
2. **Mixing network**（L120）：前馈网络，把各 Q_a 非线性地混合成 Q_tot。**为了强制单调性，权重（不含偏置）被限制为非负**；作者引 Dugas et al. 2009 论证这样"能任意逼近任何单调函数"。
3. **Hypernetworks**（L122）：**每个 hypernetwork 以全局状态 s 为输入，生成 mixing network 某一层的权重**。每个 hypernetwork = 单线性层 + **绝对值激活**（保证权重非负），输出向量再 reshape 成权重矩阵。**偏置同样由 hypernetwork 产生，但不限制非负**；最后一个偏置用 2 层带 ReLU 的 hypernetwork 产生。

**为什么用 hypernetwork 而不把 s 直接喂进 mixing network（L124，关键设计理由）**：原文 "because Q_tot is allowed to depend on the extra state information in **nonmonotonic** ways. Thus, it would be overly constraining to pass some function of s through the monotonic network alongside the per-agent values." —— 即**状态可以非单调地影响 Q_tot，只有 agent Q 那一路必须是单调的**。这是与 VDN 的核心区别。

**训练**：端到端最小化式 (6)（L134）：L(θ) = Σ_i ( y_i^tot − Q_tot(τ,u,s;θ) )²，其中 y^tot = r + γ·max_{u'} Q_tot(τ',u',s';θ⁻)，θ⁻ 是目标网（同 DQN）。**因为式 (4) 成立，对 Q_tot 取 max 的复杂度是智能体数的线性，而不是最坏情况的指数**（L137）。

**表示能力（§4.1, L141）**：QMIX 能表示的类 = "任何在**完全可观测**设定下能分解为各智能体值函数的**非线性单调组合**的值函数"，严格包含 VDN 的线性单调类。**代价**：式 (5) 让它**无法表示不满足这种分解的值函数**——L143 逐字 "any value function for which an agent's best action depends on the actions of the other agents at the same time step will not factorise appropriately"。附录 A.1（L337）进一步指出**在 Dec-POMDP 里 QMIX 不一定能表示**（因为局部观测可能区分不出真实状态，导致 Q_a 的排序与 Q_tot 不一致）。

**4. 它声称的效果**
- **两步博弈（§5, L156）**：100% 探索（ε=1）下训练 5000 episode。**VDN 收敛到次优策略**（第一步选 A，回报 7），**QMIX 找到最优**（回报 **8**）。Table 2（L158）给出学到的 Q_tot。
- **StarCraft II 微观操作（§7）**：6 张图 **3m / 5m / 8m / 2s3z / 3s5z / 1c3s5z**（L170）。QMIX 在**所有图**上最好，**异质单位图（2s3z, 3s5z, 1c3s5z）差距最大**（L223, L235）。IQL "在所有场景都学不出能稳定取胜的策略"，且训练高度不稳定（L219）。VDN 在 5m/8m 上能学会 focus firing，但 **3m（需要更精细控制）上学不会**；在 3s5z 和 1c3s5z 上 **VDN 打不过简单的启发式**（L235）。
- **消融（§7.2, L239）**：
  - **3m（同质单位）**：非线性分解**不总是必需**，但加了隐藏层也不拖慢学习。
  - **2s3z / 3s5z（异质单位）**：**必须同时有"中心状态信息"+"非线性值分解"**才能做好。
  - **QMIX-NS**（去掉 hypernetwork，权重直接学、取绝对值）"performs on par or slightly better than VDN"——说明**不结合状态时，非线性分解不一定有益**。
  - **VDN-S 对比 QMIX-Lin**：证明"要充分利用中心状态，必须有非线性混合"。
- **学到的策略（§7.3, L243）**：2s3z 上 VDN 只会"先往左跑、进射程就打"，不管站位和兵种克制；**QMIX 学会让 Zealot 先挡住并攻击敌方 Zealot，Stalker 在安全距离输出**——因为 Zealot 克制 Stalker（L243）。8m 上 QMIX 和 VDN 都学会"摆成半圆从侧面开火"。
- **启发式基线胜率（Table 7, L397）**：3m **76%**、5m 60%、8m **95%**、2s3z 82%、3s5z **45%**、1c3s5z 70%。
- **两步博弈最终回报（Table 6, L372）**：IQL 7 / VDN 7 / VDN-S 7 / **QMIX 8** / QMIX-Lin 7 / **QMIX-NS 8**。

**5. 实验条件**
- **平台**：StarCraft II Learning Environment (SC2LE)，**不是** SC1/BW（L168，作者说 SC2LE 有官方支持、更稳定）。
- **设置（§6.1）**：双方**同数量同类型**单位对称放置；我方由学习智能体控制，敌方由**内置 medium 难度 AI + 手工启发式**控制（L170）；每 episode 开始敌方被命令进攻。
- **动作空间（L172）**：move[direction]（只能东南西北）、attack[enemy id]（仅当敌人在射程内）、stop、noop。**刻意禁用了游戏的 attack-move 宏操作和待机自动还击**，逼智能体自己探索。
- **部分可观测（L174）**：用**视野范围**实现；智能体只能看到存活且在视野内的单位，**无法区分"死了"和"视野外"**。
- **奖励（L176）**：每步 = 对敌方造成的**总伤害**；每击杀 1 个 +10；全歼 +200。**归一化到 episode 最大累计回报 = 20**。
- **训练细节（附录 C.2, L386-L392）**：agent network = DRQN（GRU 64 维隐状态，前后各一个全连接层）；ε 从 1.0 线性退火到 0.05（50k 步）；γ=0.99；replay buffer 最近 5000 episode；batch 32 episode 且**完整展开**；目标网每 200 episode 更新；RMSprop，lr 5e-4；**所有 agent network 共享参数**（故把 agent id one-hot 拼到观测上）。mixing network 单隐藏层 32 单元 + ELU；最后偏置的 hypernetwork 单隐藏层 32 + ReLU。
- **episode 长度上限（L390）**：3m/5m 60 步，8m/2s3z 120 步，3s5z 150 步，1c3s5z 200 步；超时算输。
- **评估（§7, L213）**：训练每 100 episode 暂停一次，跑 **20 个独立 episode**（各智能体贪心分散执行），"test win rate" = 全歼敌方的比例；曲线是 **20 次 run 的均值 + 95% 置信区间**。
- **训练与评估的关系**：**同一套地图和环境**，仅靠 ε-greedy 的贪心执行做评估，**没有跨地图/跨规模的泛化测试**（虽然对比了 6 张不同图，但每张图都是独立训练）。

**6. 它自己承认的局限**（逐字引用）
- L141（§4.1）："However, the constraint in (5) prevents QMIX from representing value functions that do not factorise in such a manner."
- L143："Intuitively, any value function for which an agent's best action depends on the actions of the other agents at the same time step will not factorise appropriately, and hence cannot be represented perfectly by QMIX."
- L337（附录 A.1，最尖锐的一条）："In a Dec-POMDP, QMIX **cannot necessarily** represent the value function. This is because each agent's observations are no longer the full state, and thus they might not be able to distinguish the true state given their local observations."
- L253（未来工作）："In the near future, we aim to conduct additional experiments to compare the methods across tasks with a larger number and greater diversity of units. In the longer term, we aim to complement QMIX with more coordinated exploration schemes for settings with many learning agents."（**即：单位数更多、异质性更强的场景没测**）

**7. 它没做但看起来能做的地方（基于内容）**
1. **单调性约束在 Dec-POMDP 下的失效**是作者自己承认的（L337），但**没有给出任何补救或诊断工具**——能不能检测"当前场景下 QMIX 的分解是否成立"？这是个明确的空白。
2. **智能体数量最多只到 9 个左右**（1c3s5z = 1+3+5），**规模从未推到几十/上百**（L253 自述）。而 LEO 星座动辄几百上千颗星——QMIX 的规模适用边界完全没探。
3. **hypernetwork 生成权重意味着参数量随 mixing network 规模增长**，但论文没有给任何**计算/显存开销分析**，也没有推理时延数据。
4. **ε 退火后的探索完全靠独立 ε-greedy**（L386），L253 说要"更协调的探索"——**多智能体协同探索**是它自己指出的下一步。
5. **奖励用总伤害 + 击杀奖励**（L176），这是**密集奖励**。如果换成稀疏奖励（如只给最终胜率），单调分解是否仍然有效？没测。
6. **只跟 value-based 方法比（IQL/VDN）与启发式基线**，没有跟当时更强的 policy-gradient 类 MARL 做同条件对比（虽然 §2 讨论了 COMA）。

**8. 和同批其他篇的关系**
**这是本批唯一一篇纯 MARL 算法论文，含 0 行 LEO/卫星/网络内容**。全库范围内它是"方法供体"而非"应用论文"——如果本批/全库里有 LEO 多智能体路由论文（比如 S85KQ4FC 提到的 FDR-MARL），很可能**引 QMIX 或用 QMIX 做基线**，或者引它的前身 VDN（L311）与 COMA（L273）。
- **概念上与 9C6HB6AF 相反**：9C6HB6AF 用**集中式单智能体**（NCC 一个 PPO/DQN 决定全网分流），QMIX 恰恰是为**分散执行**设计的。两者代表 LEO 路由的两条路线：集中优化 vs 分散 MARL。
- **与 8N9QJHC2 的血统关系**：8N9QJHC2 用表格 Q-learning 逐节点维护 Q 表（本质是**独立学习**，接近 IQL 的朴素形态），而 QMIX 正是为了修 IQL 的非平稳性而生。把 8N9QJHC2 的"每星一张 Q 表"换成 QMIX 式分解，是一个自然但没人做的组合。
- **对 S85KQ4FC 的直接价值**：S85KQ4FC 关心"星上推理成本"，而 QMIX 的 agent network 是 DRQN（带 GRU），**推理时延比前馈网络更高**——这正好是 S85KQ4FC 那篇要解决的问题的另一面。
*[回填位：读完本批/全库后补：本批是否有篇目引用 VDN/QMIX]*

**9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实**
**没有直接贡献，而且是彻底的无关**。这篇的"环境"是 StarCraft II 战斗，**没有网络、没有链路、没有队列、没有到达率、没有时延**；它的"负载"概念是敌方单位数量与兵种构成（3m/5m/8m/2s3z/3s5z/1c3s5z），不是流量强度。奖励是伤害值和击杀（L176），与排队时延无关。
**唯一可迁移的方法论**：它示范了"**把联合目标分解为局部量、同时保证分散执行的最优性**"这一模式（单调性约束）。如果 LEO 路由要把"全局时延/到达率"分解到每颗星的局部决策上，QMIX 的单调分解是现成的工具——**但这个迁移本篇没做，也没暗示要做**。

**10. 一句话评价**
CTDE 范式的**里程碑式方法论文**（单调值分解 + hypernetwork 条件状态），在 MARL 方法谱系里是 VDN 与 IQL/COMA 之间的关键一环；**但它是一篇纯 RL 算法论文，与 LEO 网络、与负载/时延问题没有任何交集**——它在 111 篇语料里的价值是"可被引用的方法组件"，不是"领域事实"。

## 9GPFG5U3 — Link-Identified Routing Architecture in Space (IEEE JSAC, Beihang University)

**1. 一句话**
**不给卫星/接口命名，改给每条 ISL 一个全局唯一标识**；源卫星把一串 ISL 标识塞进**包头里的 Bloom Filter** 做源路由转发——代价是 BF 假阳性会造成"多余转发"，于是论文用 LEO 的规则网格拓扑**解析地推出多余转发的闭式期望**，并解出"源与中间星分段编码"的最优策略。

**2. 问题设定**
LEO 星座有**确定性邻居关系**（L17 逐字："the LEO satellite constellation exhibits a deterministic neighbor relation"，每星固定 4 个邻居：同轨 2 + 异轨 2）。而地面 IP 架构假设邻居关系**先验未知**、要靠报文交换建立——**直接把 IP 搬到 LEO 会把这一拓扑特性"埋掉"**（L17 逐字："If IP architecture is directly adopted in LEO constellation, then the aforementioned topology characteristics will be 'buried'"）。三个关键问题（L19/L23/L27）：
- Q1 怎么利用这个拓扑特性做高效转发？→ 用 ISL 标识 + 源路由。
- Q2 怎么基于拓扑特性**优化** BF 转发的开销？→ 因为 BF 有假阳性，编进去的 ISL 越多、多余转发越多。
- Q3 怎么在源路由风格下处理拓扑动态（ISL 间歇、GSL 频繁切换）？

**3. 方法骨架**

**(A) LiR 架构（第 III 节）**
- **每条单向 ISL 分配全局唯一标识**（L71），每星关联 4 个 ISL 标识。
- **BF 形式化（L84）**：M 位向量 + K 个哈希函数表示 N 个元素。假阳性率式 (1)：$p(M,N,K) = [1-(1-1/M)^{KN}]^K$。**关键性质（L82）：BF 只会假阳性、不会假阴性**——所以 LiR **不会丢包**，只会多转发（Fig 4 标题就是"No packet loss"）。
- **转发规则（L113）**：中间星收到包后，检查**除入端口外的另外 3 条出向 ISL** 是否被编码在包头 BF 里，是则转发。

**(B) 开销解析（§III-C，全文最硬核的部分）**
- **Theorem 1（L133）**：错误转发开销 $f_{IFO}(N,M,K) = \dfrac{(2N+1)(M+C)\,p(N,M,K)}{1-3p(N,M,K)}$。推导（L138-L159）：每条 N 跳路径有 $2N+1$ 个潜在错误方向，每跳错误转发成本 $M+C$；定义 $E(p)$ = 沿单一错误方向的期望转发跳数，递归 $E(p) = (1-p)\cdot 0 + p\cdot[1+3E(p)]$ → $E(p) = p/(1-3p)$。**注意分母 $1-3p$ 在 $p \to 1/3$ 时发散**。
- **Theorem 2（L174）**：正确转发开销 $f_{CFO}(N,M) = MN$（BF 本身占的带宽）。
- 总开销式 (7)：$f_{FO} = f_{IFO} + f_{CFO}$。最优 BF 长度式 (8)：$f(N) = \min_{M\geq 0} f_{FO}(N,M,K)$。
- **关键结构性发现（L189）**：$f(N)$ **关于 N 凸增**（"f(N) is convexly increasing ... the marginal forwarding overhead is increasing"）——**边际开销递增**，所以一次编太多 ISL 不划算。**这正是分段编码的动机**。

**(C) 分段编码设计（第 IV 节）**
- **权衡（L243）**：源星与中间星**分段编码**，每段编少量 ISL → 降低假阳性/多余转发；代价是中间编码星要**重算路由或查表**，**牺牲转发速度（编码时延 τ）**。
- **策略模型（L255-L269）**：$(N+1)$ 维二值向量 $\mathbf x$，$x_n=1$ 表示第 n 颗星清空 BF 重新编码（付 τ），$x_n=0$ 表示直接转发。约束 $x_1 = x_{N+1} = 1$。
- **目标函数（式 13, L302）**：总"时间开销" $\sum_{n=1}^{N}\left[\dfrac{f(r_n(\mathbf x)-n)}{B} + \tau\right]x_n$，其中 $r_n(\mathbf x)$（式 11）是 n 之后**下一个编码星的索引**，B 是 ISL 带宽。**第二项 τ 是编码时延，第一项是多余转发造成的排队时延**。
- **Problem 1（式 14, L310）**：$\mathbf x^\star = \arg\min \sum_n [\cdot]x_n$。**作者明确说：这是二值非线性规划，一般 NP-hard，且"not monotonic or sub-modular, thus the greedy algorithm has no performance guarantee"（L313）**。
- **解法（§IV-C）**：利用**可分解结构**做 DP。子问题 $H(i)$（式 15）定义"第 i+1 颗星必为编码星"时的最小开销；**引理 1（式 17, L369）**：$H(i) = \min_{0\leq q<i}\{H(q) + [f(i-q)/B + \tau]\}$。**Algorithm 1** 是标准 $O(N^2)$ DP + 回溯构造 $\mathbf x^\star$。
- **运行时行为（L382-L384）**：卫星若发现自己的出向 ISL 在 BF 里 → 直接转发；若一个都没有 → 自己是"重编码卫星"，查路由表算新段、清空并重编 BF。**作者注：这个计算可以预先做好以减少处理时间**。

**(D) ISL 失效管理（第 V 节）**：三种方案
- **LSA**（L392）：传统链路状态通告，hello 包周期广播（OSPF 是 5 s）。
- **ODR**（L394）：**不扩散链路状态**，每星实时监控自己的 ISL；收到包发现该走的那条 ISL 挂了 → **重算到目的地的路由并更新 BF**。
- **ODD**（L396）：同样不扩散，但**激活一条预先算好的等价路径**绕开。等价路径 = **绕开某条失效 ISL 的最少跳数路径**，网格拓扑下分**顺时针/逆时针**两种（L421）。用一个**单独的等价路径 BF**（equivalent-path BF）承载（L425），每星维护**等价路径转发表**映射到出接口（L427）。

**(E) GSL 切换（第 VI 节）**：用**多播**做到无缝切换——把包同时送到多颗覆盖该地面用户的卫星，让它们**缓存**以备切换（L444）。LiR 天然支持多播（**不需要像 IP 那样重配多播组地址**，L448）。两种多播：
- **SPF 多播（L461）**：源到每个目的地各算最短路，**取并集**编码进 BF。
- **PNB 多播（L469）**：选一个目的地为**主节点**，编码"源→主节点"+"主节点→其他目的地"的并集，**减少冗余**。

**4. 它声称的效果**（全部给定条件）
- **路径表示效率（§III-E, L232）**：对比 **Starlink 2027 年预期星座（4408 颗星）**。基线 **ELR**（显式链路表示，SRv6/MicroSID/GSRv6 的下界）：头部长度 $N\lceil\log_2 L\rceil$ 位、总转发开销 $N^2\lceil\log_2 L\rceil$。**LiR 在包头长度和转发开销上都更优**。
- **vs SRv6（§III-D / §VII-E）**：LiR 载荷比更高；转发开销更低。包级实验（Fig 17, L550）：**跳数 <8 时 SRv6 端到端时延略大于 LiR；跳数 >8 时 SRv6 时延显著上升**（作者归因于包头变长引发拥塞）。
- **Theorem 1 验证（§VII-B）**：(b) Matlab 随机假阳性事件（500 次运行）与理论曲线**几乎重合**；(c) OMNeT++ 上假阳性率 **< 0.27 时两曲线几乎重合，> 0.27 时实测低于理论**——作者归因于 Matlab 与 OMNeT 对**环路（loop）的处理不同**（L513，**主动承认的不一致**）。
- **单流（§VII-C, Fig 15）**：hops $N \in \{3,...,12\}$。**最优分段编码 vs 源编码的时间开销差距随源-目的距离增大而增大**（L526）→ 论证分段编码的必要性。Matlab 数值与 OMNeT++ 包级结果一致。
- **多流（§VII-D, Fig 16）**：4 对双向源-目的对、**有重叠 ISL**，每源**发送率 1250 pps**。BF 长度 $M \in \{30,40,...,70\}$。**BF 小的时候最优编码显著优于源编码；BF 大时两曲线收敛到"无错误转发时的排队时延"**（L532）。**作者还观察到一条反直觉现象：源编码曲线（蓝菱形）随 BF 增大而轻微上升，因为"the increment of traffic load due to the BF size"（L532）**——即**包头开销本身增加了负载**。
- **ISL 失效管理（§VII-F, Fig 18）**：失效率 $\{0\%,5\%,10\%,15\%,20\%\}$，源发送率 **100 pps**。三条观察：
  1. **LiR-ODR 与 LiR-ODD 的投递率几乎相同**（都接近 100%），但 **LiR-ODR 的端到端时延更优**——因为 ODD 的等价路径"may not be the delay-minimizing one"（L573）。
  2. **同样 1 s 的 LSA，OSPF-LSA(1s) 投递率更高但时延更大**：OSPF 由中间节点逐跳决策，LSA 不及时只会绕路（时延大）；LiR-LSA 由源星定好整条路径，LSA 不及时**直接投递失败**（L575-L586）。**这是一个非对称的失效模式对比，写得很好。**
  3. **LiR-ODR/ODD 在投递率上优于 LiR-LSA(1s)**，因为它们利用确定性邻居关系，而 LSA 是为地面互联网设计的（L588）。
- **多播（§VII-G, Fig 19）**：one-to-N，$N\in\{2,...,6\}$，发送率 **1.6 Mbps**。三条观察：(1) Multicast-PNB/SPF 的时延与投递率都优于单播两种；(2) **PNB 略优于 SPF**（PNB 编码的标识更少、错误转发更少，L608）；(3) Unicast-Optimal 优于 Unicast-Source。

**5. 实验条件**
- **仿真平台（L485-L493）**：**OMNeT++ + INET 4.2.2** 自建三大模块——星座模块（用 **OsgEarth 库获取实时卫星位置**来算 ISL 传播时延）、网络模块（协议栈/排队/路由）、流量生成模块。运行在 VMware ESXi 6.5.0 + Ubuntu 20.04。
- **星座**：**Iridium，66 颗 LEO 卫星，高度 780 km**（L481），典型极轨星座。
- **链路与参数**：每条 ISL **10 Mbps**；BF 替换耗时 $\tau$ = **10 微秒**；每包有效数据 $C$ = **1 KB**；哈希函数数 **K = 5**（Fig 6, L169）。
- **拓扑动态**：**ISL 失效与恢复事件按 Poisson 过程随机生成**，给定失效率（L487）。
- **负载设定**：**每个实验固定一个发送率**——多流 1250 pps（L530）、SRv6 对比 1000 pps（L550）、失效管理 100 pps（L554）、多播 1.6 Mbps（L592）。**没有对发送率做扫描**。
- **扫描的变量是**：跳数 N（3–12）、BF 长度 M（20–50 位 / 30–70 位）、ISL 失效率（0–20%）、多播组大小 N（2–6）。
- **训练与评估**：**无训练**（纯解析 + 协议设计 + 仿真验证），解析结果与仿真结果做了交叉验证（Theorem 1 的 (b)(c) 两条曲线）。

**6. 它自己承认的局限**（逐字引用）
- L313："Problem 1 is a binary non-linear programming, which is **NP-hard in general**. Moreover, it is **not monotonic or sub-modular, thus the greedy algorithm has no performance guarantee**."
- L513（Theorem 1 验证的不一致）："When the false positive rate is greater than 0.27, however, the number of incorrect forwarding hops under OMNeT++ simulation is smaller than that of the theoretical result. **This inconsistency can be attributed to different handling of loops between the Matlab and OMNeT implementation.**"
- L616（未来工作）："In the future, it would be interesting to investigate how to implement the LiR architecture in the Linux kernel. ... A proper implementation should be incremental."（**即：本文只做了仿真，没有任何真实实现**）
- L550 的时延对比只在跳数 <8 时有利——作者没有把这条当作局限写出来，是结果里隐含的边界。

**7. 它没做但看起来能做的地方（基于内容）**
1. **$\tau$（BF 替换耗时）被设成常数 10 微秒**（L481），但 ODR/ODD 场景下卫星要**重算路由**——重算时间远大于 10 μs 且随星座规模增长。**"编码时延"这个代价项在最需要它的失效场景里恰恰没被建模**。
2. **没有对发送率/到达率做任何扫描**。四个实验各用了一个固定发送率（1250 / 1000 / 100 pps / 1.6 Mbps），而**多流实验里作者自己观察到"BF 变大导致负载增加、排队时延上升"**（L532）——说明这条轴是敏感的，却没扫。
3. **最优性只在"单流、给定 N"下证明**。多流场景下各流的编码策略会互相影响（共享 ISL），**论文的 DP 是逐流独立做的**，没有联合优化。
4. **等价路径（ODD）是预先算好的静态表**（L427），但 LEO 拓扑在变，**表什么时候失效、如何更新**没说。
5. **ISL 失效用 Poisson 过程随机生成**（L487），**与 LEO 真实的"缝区/极区几何性失效"无关**——而极轨星座的 ISL 失效恰恰是**周期可预测**的（作者自己在 L17 强调"deterministic neighbor relation"），却用了一个**无记忆的随机模型**。**这是论文内在的一个不自洽**。
6. **只测了 Iridium（66 星）**，而路径表示效率分析用的是 Starlink 4408 星（L232）——**解析与仿真在不同星座上**，规模差 66 倍。
7. **$1-3p$ 分母在 $p\to1/3$ 时发散**（式 2），论文没有讨论这个奇点的物理含义或安全边界。

**8. 和同批其他篇的关系**
- **明确引用了 8AYW2Y78 (Hypatia)**：参考文献 [2]（L635）就是 Kassing et al. 的 Hypatia。**这是本批内已确认的第一条引用链。** 它还引了 Handley 的 "Delay is not an option" [5]（L641）和 Giuliari 的 "Internet backbones in space" [4]（L639）——后者正是 Hypatia 的参考文献 [26]。
- **和 8AYW2Y78 的关系是"互补而非竞争"**：Hypatia 是**测量基础设施**（发现时变拓扑的挑战），LiR 是**协议设计**（提出一套新架构去应对）。两者都基于"确定性邻居关系 + 网格拓扑"这个前提。
- **和 8N9QJHC2 的对照很尖锐**：8N9QJHC2 用**贝叶斯推断**去判"链路是临时故障还是永久故障"，再做差异化路由；**LiR 完全不做故障分型，ODR/ODD 都是"发现挂了就绕"**。两者对同一问题（ISL 间歇）给出了**完全不同哲学的解**：一个是"先诊断再决策"，一个是"不诊断、本地反应"。
- **和 S85KQ4FC 的关系**：S85KQ4FC 关心星上 DNN 推理的算力瓶颈；LiR 关心星上 **BF 查表 + 可能的 BF 重编码**。**两者都在往包头/星上处理能力上加负担**，但都只把"处理时延"当作一个参数（S85KQ4FC 是 $C_k/f_{i,k}$，LiR 是常数 τ），没当成一等约束去优化。
- **跟 9C6HB6AF 完全不同的路线**：9C6HB6AF 是集中式 NCC 算分流比例（控制面集中），LiR 是**源路由把路径写进包头**（控制面分散到源星），两者是 LEO 路由架构的两极。
- *[回填位：本批剩余篇目引用核实]*

**9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实**
**有间接但真实的两条贡献**，不过它**没有做负载扫描**（四个实验各固定一个发送率：1250/1000/100 pps、1.6 Mbps）：
1. **包开销本身会改变负载，进而改变排队时延**（L532 逐字："The blue diamond curve is slightly increasing. This is because of the increment of traffic load due to the BF size."）——**这是"协议开销 → 有效到达率 → 排队时延"链条的一条直接证据**，而且是反直觉的：BF 变大降低了错误转发，却因为包头变大而抬高了负载，两者相互抵消。
2. **时延上升的两个来源被明确区分开**：式 (12) 把每跳开销写成 $f(\cdot)/B + \tau$，前者是**多余转发挤占带宽造成的排队时延**，后者是**编码处理时延**。全篇的时延论证都建立在这个区分上。
3. **失效率扫描（0–20%）间接给出了"有效到达率下降"下的时延/投递率曲线**：失效率升高 → 有效可用链路减少 → 投递率与端到端时延变化（Fig 18）。**但这是链路可用性维度，不是负载维度**。
4. 值得记的一条边界：**LiR-LSA 在链路状态不及时会直接丢包，而 OSPF-LSA 只会绕路**（L575-L586）——即**源路由架构对"信息陈旧"的惩罚是丢包而非时延**，这个失效模式的不对称性对"负载突变下谁先崩"有参考价值。

**10. 一句话评价**
**把 Bloom Filter 源路由这一数据中心/发布订阅领域的技术，第一次系统地按 LEO 拓扑特性重新推导了开销闭式解并做了最优分段编码**（Theorem 1 的 $E(p)=p/(1-3p)$ 递归与 $f(N)$ 凸性是好工作），是 LEO 路由谱系里**非学习路线的代表**；但它**用无记忆 Poisson 过程模拟一个自己反复强调"确定性、可预测"的拓扑**，且把最需要建模的"星上重算时延"简化成常数 10 μs——这两点削弱了它在真实动态场景下的说服力。

## 9KZDXPKC — How to Route CUBIC and BBR Packets in Space (IEEE INFOCOM, Beihang University)

**1. 一句话**
不改终端上的 CUBIC/BBR，而是**改路由**：给 GSL 切换配一条**默认路由**、给 ISL 失效配一组**备份路由**，让链路事件期间到达的包"有表可查"而不是被丢掉——从而**不让拓扑动态伪装成拥塞信号**去骗 CUBIC 砍窗、骗 BBR 低估带宽。

**2. 问题设定**
CUBIC 是**丢包驱动**、BBR 是**带宽估计驱动**，两者都假设"丢包/时延上升 = 拥塞"——这个假设在地面光纤网成立，在 LEO 不成立（L23）。LEO 有两种拓扑动态（L32, L34）：
- **GSL 切换**：卫星只能服务覆盖范围内的地面站，轨道周期短 → GSL 频繁切换。
- **ISL 失效**：每星 4 条 ISL（2 异轨 + 2 同轨），**相邻卫星相对速度高时，天线跟踪瞄准能力受限导致 ISL 不稳定**。

两者都会造成**丢包或 RTT 突变**（L36）：GSL 切换时路由表还没来得及更新，包被丢；ISL 失效时同理；即使路由更新及时，**星座内路径变了，RTT 也会突变**。
**关键洞察**：路由收敛前的窗口里，丢包**不是拥塞造成的**，但 CUBIC/BBR 分不出来。
作者明确说"individually revise CUBIC or BBR for LEO"不实际（L43），所以从路由侧下手。
**已有工作的缺口（Table I, L39 + L78）**：Cao et al. [19] 的 SatCP 用**链路层通知**，但 (a) 开销大、且**要求地面终端改写拥塞控制**；(b) 其 Mininet 测试床**不支持分布式路由软件，用集中式路由计算代替**——"Such a simplification hides the impact of link-state changes in terms of routing reachability"（L78）。

**3. 方法骨架**

**(A) 两个先导实验（第 III 节，都是"先证明问题存在"）**
- **CUBIC 原理**（L94-L126）：三个重复 ACK 触发快重传并砍窗 $\mathrm{cwnd}_{new} = \mathrm{cwnd}_{old}\cdot\beta$，$\beta = 0.7$（式 1）；然后按三次函数增长 $W(t) = C(t-K)^3 + W_{max}$（式 2）。
- **BBR 原理**（L136-L150）：带宽估计 $\mathrm{BW} = \frac{\mathrm{Delivered} - \mathrm{packet.delivered}}{\mathrm{Now} - \mathrm{packet.delivered\_time}}$（式 3）；取最近 **10 轮**的最大值为 $BW_{max}$；$\mathrm{Pacing\_rate} = BW_{max}\cdot\mathrm{pacing\_gain}$（式 4），**pacing gain 在 {1.25, 0.75, 1, 1, 1, 1, 1, 1, ...} 间周期变化**。

**(B) DB-R 机制（第 IV 节）——两个独立子机制**

**① 默认路由对付 GSL 切换（§IV-A）**
- **丢包机理（L180）**：GSL 断开 → 对应接口的路由表项**立即消失** → 卫星重算路由。但 LSA 传播要时间，期间仍有包沿旧路径到达该星 → **没有匹配的表项 → 丢包**。
- **关键量化（L188）**：作者实测这个"表项缺失窗口"**只有几十毫秒**（"such a period lasts for about tens of milliseconds"）——**这是用低成本的默认路由就能补上的依据**。
- **默认路由定义（L190）**：节点转发时找不到匹配表项时的兜底选择。
- **触发条件（§IV-A3）**：需要两个前提（L198, L200）——(a) 同一 GS 的所有 GSL 的 IP 地址**共享同一前缀**；(b) 每星维护一个 **GSL Array** 记录在用的 GSL IP。**检测逻辑**：路由表出现新表项时，检查其目的地址前缀是否与 GSL Array 中任一 IP 相同 → 是则说明**即将发生切换**，立即加默认路由项。
- **接口选择（§IV-A4, L216）**：旧 GSL 所属卫星**算到新 GSL 所属卫星的最短路**，把**该新表项的出口接口**用作默认路由的出口。
- **设计巧妙处**：**无需额外的信令**——"新 GSL 建立"本身就是切换的先行信号（L196），默认路由的触发完全搭在 OSPF 已有的 LSA 上。

**② 备份路由对付 ISL 失效（§IV-B）**
- **丢包机理（L220）**：ISL 因天线失准断开 → 该接口不可用 → 涉及该接口的路由表项被删 → 卫星更新 LSDB、重算、扩散 LSA。**更新完成前到达的包因无匹配表项被丢**。
- **机制（L230）**：每星有 4 个接口通向目的地、代价各异。**代价最小的为主路由，其余三个按代价排序全部保留为备份路由**。某个接口不可用，就自动落到下一个。
- **关键前提（L228）**："The topology of LEO constellations yields multiple equivalent path"——**LEO 的网格拓扑天然存在多条等价路径**，这是备份路由可行的原因（与 LiR 论文依赖的是同一个拓扑事实）。

**4. 它声称的效果**（全部给定条件）
**先导实验（问题有多严重）**：
- **GSL 切换**：CUBIC 的 RTT 突变 + 丢包 → CWND 立即下降再慢慢爬回（Fig 5, L130）；**BBR 的 BW 从 180 Mbps 暴跌到 80 Mbps 再爬回**（L170）。**FCT 与 slowdown 放大到 5×**（L132）。
- **ISL 失效**（配置了 **5 秒**的失效事件）：RTT **从 130 ms 突增到 170 ms**（L130, L170）；**BBR 的 BW 从 150 Mbps 跌到 50 Mbps 再爬回**（L170）。FCT/slowdown **放大到 5×**（L172）；BBR 在 GSL 切换下是 **4.9×**（L172）。
- **总体（L53）**：GSL 切换与 ISL 失效会让 CUBIC 平均吞吐下降**最多 67%**、BBR 最多 **41%**。

**DB-R 的效果**：
- **长流验证（§V-A）**：CUBIC 在 **第 95 秒**发生 GSL 切换时，OSPF 曲线**跌到 120 Mbps 再缓慢升回 160 Mbps**，而 **DB-R 曲线只跌到 160 Mbps**（即只体现传播时延增加导致的合理下降，**没有多余的拥塞误判**）（L246）。ISL 失效（**第 50 秒**，持续 5 s）：OSPF 跌到 **46 Mbps** 再升回 150 Mbps，DB-R 直接落在 **150 Mbps**（L248）。
- **经验流分布评估（§V-B）**：按 **Poisson 过程**随机生成不同大小的流，统计**事件发生后 1 秒内**的平均吞吐/FCT/slowdown（L252）。
  - **吞吐**：DB-R 对 CUBIC 与 BBR 都有提升。**关键观察（L254）：OSPF 下 BBR 优于 CUBIC，但 DB-R 下两者几乎一样**——"This means that packet loss caused by link dynamics plays an even worse role on CUBIC than BBR."
  - **FCT**：同样，**OSPF 下 BBR 的 FCT 更低，DB-R 下两者持平**（L256）。
  - **Slowdown**：DB-R 显著降低两者的 slowdown（L258）。
- **总改进（摘要 L13 / 结论 L262）**：平均吞吐 CUBIC 提升**最多 37%**、BBR **最多 18%**（对比经典 OSPF）。**FCT 最多降低 52%（CUBIC）/ 42%（BBR）**（L59）。
- **注意**：摘要与结论都**只报了吞吐数字**，FCT 的 52%/42% 只出现在贡献列表（L59），**结论段没有重复**。

**5. 实验条件**
- **平台**：**OpenSN**（作者自己组的开源 LEO 仿真库，参考文献 [20]，L329）——基于容器，且**跑真实的分布式路由软件 FRR**（L80, L331）。作者选 OpenSN 的理由是"efficiency on constructing mega-constellations and updating concurrent network states"（L238）。
- **对比的既有测试床（L238）**：LeoEM [19]、StarryNet [24]、OpenSN [20]。
- **星座**：**Iridium，walker-star，66 颗星，6 个轨道面，高度 780 km**（L238）。
- **链路带宽**：**GSL 200 Mbps，ISL 1000 Mbps**（L238）。
- **地面站**：**上海与洛杉矶**两个（L238），可建立多条 TCP 连接。
- **先导实验的另一组条件**：Starlink Shell-I（h=550 km, β=25°）用于算会话时长分布与传播时延分布（L88，Fig 3/Fig 4）；CUBIC/BBR 影响的例子里用 **上海–洛杉矶 via Iridium**（L128, L152）。
- **负载设定**：长流（long-lived flow）验证 + **经验流长分布 [22]**（L252, L333）。**没有做负载/到达率扫描**；实验的"触发变量"是**链路事件的时刻与持续时间**（GSL 切换、5 秒 ISL 失效）。
- **实现**：**Linux kernel 5.19.0**（L57），真实内核改动，不是纯仿真。
- **训练与评估**：无训练。评估是同一测试床上的对照实验（OSPF vs DB-R），未做跨星座泛化。

**6. 它自己承认的局限**（逐字引用）
论文**没有 Limitations 节**，只在相关工作里批评别人时**间接暴露了自己的边界**：
- L78（批评 Cao et al. [19]，但这段也定义了本文的参照标准）："First, the link-layer notification incurs additional overhead, and requires the terrestrial end hosts to modify the congestion control mechanisms... Second, the testbed in [19] does not support distributed routing software, but relies on centralized routing calculation as the alternative. **Such a simplification hides the impact of link-state changes in terms of routing reachability.**"
- L43（对可行解的自我限定）："**It is not practically feasible to revise CUBIC or BBR individually for LEO constellations.** Thus, this paper aims to address the above drawbacks from another direction."
- L188 里那个"几十毫秒"是**本文机制成立的隐含前提**，但作者只说"According to our experiments on virtual network emulation environment"，**没有给这个窗口的分布或上界**。

**7. 它没做但看起来能做的地方（基于内容）**
1. **"表项缺失窗口只有几十毫秒"是 DB-R 全部合理性的支点**（L188），但论文只给了一个粗略说法，**没给统计分布**。如果某类事件的窗口达到几百毫秒，默认路由是否还够用？没答。
2. **默认路由只有一个出口**（L216）。若切换期间同时发生 ISL 失效，默认路由指向的接口恰好也挂了怎么办？**两个子机制之间没有任何交互设计**——GSL 切换用默认路由、ISL 失效用备份路由，**但论文没有讨论二者同时发生**。
3. **没有负载/到达率扫描**。所有实验固定流长分布与链路带宽，扫的是"事件时刻"。而 DB-R 要解决的恰恰是**事件期间瞬时到达率被拥塞控制误砍**的问题——**把背景负载从 0 加到接近饱和，DB-R 的收益是否还在？这是最直接的缺口。**
4. **只测了 Iridium（66 星）+ 上海–洛杉矶单对 GS**（L238）。星上默认路由/备份路由机制在几百上千颗星的星座里是否还成立（表项数量、收敛时间），未验证。
5. **BBR 版本未说明**（是 BBRv1 还是 v2？），而 BBR 的 pacing gain 序列 {1.25, 0.75, 1, ...}（L150）是 v1 的特征。BBRv2 对丢包的敏感度不同，结论未必迁移。
6. **没有与 Cao et al. [19] 的 SatCP 做直接实验对比**（只在 Table I 和文字上比），而那是本文最接近的对手。
7. **pacing gain 的周期变化本身就是一个"内生到达率振荡"**（L150），论文把它当背景交代，**没有分析它与链路事件叠加时的相位效应**。

**8. 和同批其他篇的关系**
- **同一个作者群的"系列作"**：本文作者 **Zhiyuan Wang / Shan Zhang / Qingkai Meng / Hongbin Luo**（L3）与 **9GPFG5U3 (LiR)** 的作者群**完全重合**（LiR 作者：Hefan Zhang, Zhiyuan Wang, Shan Zhang, Qingkai Meng, Hongbin Luo）。本文参考文献 **[10]**（L307）正是 LiR 的会议版 "Optimizing link-identified forwarding framework in LEO satellite networks" (WiOpt 2023)——而这也正是 9GPFG5U3 的参考文献 [1]（L633）。**两条引用链在同一个组内完全对上。**
- **直接引用了 8AYW2Y78 (Hypatia)**：参考文献 [4]（L295）即 Kassing et al. Hypatia。**这是本批内第二条确证的 Hypatia 引用**（第一条是 LiR 的 [2]）。
- **与 9GPFG5U3 (LiR) 是互补而非竞争**：LiR 解决"包**怎么走**"（用 BF 编码路径），DB-R 解决"链路事件期间包**别被丢**"（默认/备份路由）。两者都建立在**同一个拓扑事实**上——LEO 网格有确定性邻居与多条等价路径（L228 vs LiR 的 L17）。**但 DB-R 面向的是 IP/OSPF 栈（FRR、路由表、LSA），LiR 是推倒重来的新架构**；DB-R 更像是"在不改协议栈的前提下尽量拿到 LiR 想要的好处"。
- **与 8AYW2Y78 (Hypatia) 的结论直接互证**：Hypatia 说"loss 和 delay 都是糟糕的拥塞信号"（Hypatia L254/L256）；DB-R 用具体数字量化了这件事——**CUBIC 吞吐最多掉 67%、BBR 最多掉 41%**（L53），并且给出了机制解释（丢包→砍窗 / RTT→低估 BW）。**这是本批里对 Hypatia 那条结论最直接的一次定量延伸。**
- **与 S85KQ4FC 的对照**：S85KQ4FC 认为要高通量就得**别逐包推理**；DB-R 反过来强调**逐包查表必须快**（默认路由是查表兜底）。两者都在星上转发路径上做文章，但一个砍推理、一个加表项。
- **与 9C6HB6AF 的区别**：9C6HB6AF 用集中式 NCC 决定分流比例；DB-R 是**纯分布式**（跑 FRR，L80），且刻意避开集中式——它批评 Cao et al. 的一点就是对方测试床用集中式路由计算（L78）。
- *[回填位：本批剩余篇目引用核实]*

**9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实**
**这是本批目前对"时延/吞吐的瞬态响应"给出最细颗粒数据的论文**，而且它的因果方向和通常的"负载→时延"是**反向的**——它展示的是**事件→拥塞控制误判→到达率塌陷→吞吐下降→缓慢恢复**这条链。具体可用的事实：
1. **一次链路事件会把发送率打掉再慢慢爬回**，且**爬回过程可持续数十秒**：ISL 失效 5 秒，CUBIC 吞吐从 150 掉到 46 Mbps 再回升（L248）；BBR 的 BW 从 150 掉到 50 Mbps 再回升（L170）。**这就是一条"到达率对扰动的响应曲线"，只是扰动源是链路事件而不是负载变化。**
2. **CUBIC 与 BBR 对同一次事件的响应差别很大**：GSL 切换下 BBR 的 BW 从 180→80 Mbps，ISL 失效下从 150→50 Mbps（L170）——**同样的 RTT 变化（130→170 ms），两种算法的估计器反应不同**。
3. **丢包型信号比时延型信号更脆弱**：DB-R 消除了丢包后，**CUBIC 与 BBR 的性能变得几乎相同**（L254, L256）——反过来说，**在 OSPF 下两者的差距几乎全部来自丢包，而不是来自时延**。这是对"LEO 里哪种拥塞信号更不可靠"的一个干净的分离实验。
4. **RTT 的具体数值**：ISL 失效使端到端 RTT **从 130 ms 变到 170 ms**（L130, L170）——**这是"路径变化（而非排队）带来的时延阶跃"的一个实测样本**，与 Hypatia 的 Rio–St. Petersburg 96→111 ms（Hypatia L207）是同性质的现象、不同星座。
5. **BBR 的 pacing gain 序列 {1.25, 0.75, 1, 1, ...}**（L150）意味着**即使链路完全稳定，BBR 的发送率本身也在周期性振荡**——这是分析"到达率"时容易被忽略的内生项。
**但**：本文**完全没有做负载扫描**，背景流量固定；"经验流"虽按 Poisson 过程生成（L252），但那是**流到达**的随机性，不是**到达率水平**的变化。所以对"负载水平变化下的时延曲线"，它没有贡献。

**10. 一句话评价**
**从"改路由而不是改传输层"这个角度切入 CUBIC/BBR 在 LEO 的失效问题，工程上极其干净**（默认路由搭在既有 LSA 上、零额外信令；备份路由蹭 LEO 网格的多等价路径），且有**真实 Linux 内核 + 真实分布式路由软件**的实现背书；它是本批里把 Hypatia"loss/delay 都是坏信号"这条定性结论**做成可量化、可修复的工程方案**的第一篇——但**它止步于"消除丢包"，没有回答"负载升高后这套机制还灵不灵"**，也没有处理默认路由与备份路由同时被触发的情形。
