# 读卡批次 R3

> 批次：8AYW2Y78 8N9QJHC2 9C6HB6AF 9FLZ88LZ 9GPFG5U3 9KZDXPKC A7QNRKML AF674CSF AIH4GK37 AJJI57M9 AZ72LM9Z
> 读法：读卡者逐字通读 VM MinerU MD 全文（共 5456 行）；行号对应 VM MD 行号。

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
*[回填位·已回填]* **本批内确证被四篇引用**：9GPFG5U3 (LiR) 参考文献 [2]、9KZDXPKC (DB-R) 参考文献 [4]、AIH4GK37 (PBAR) 参考文献 [10]、AZ72LM9Z (Roman-HitchHiking) 参考文献 [24]（把它归入"LEO 测量/仿真系统"一类）；AF674CSF (LPIH) 引的则是它的同源文献 Handley "Delay is not an option"。**引用方式分两档**：LiR/DB-R 引它佐证"时变拓扑是真问题"，**AIH4GK37 则把它当仿真基座直接使用**（"Our constellation topological state is generated using Hypatia"）。**即 Hypatia 在 2020–2026 间完成了从"论点来源"到"标准基础设施"的角色转变**；北航系（LiR/LPIH/DB-R）与 UCLA 系（PBAR/Roman-HitchHiking）都建立在它确立的现象之上。

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
*[回填位·已回填]* **本批内未被任何篇目直接引用**。但它是本批唯一延续 Boyan & Littman 1993 Q-routing 表格型血统的论文——9FLZ88LZ (QMIX) 处理的正是它这种"每节点独立维护 Q 表"的非平稳性病根（虽然两者互不知晓）。**它的"故障分型"思路在本批内唯一的呼应是 9GPFG5U3 (LiR) 的反面**：LiR 完全不诊断故障类型，只用"PID 对应多条物理 ISL"的冗余绕开。

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
*[回填位·已回填]* **本批内未被直接引用**。它的两个关键对手在本批里有回响：（a）它批评 DDPG-TE 的"状态/动作维度随拓扑变"，而 **9GPFG5U3 (LiR) 用 BF 包头、AF674CSF (LPIH) 用 PID 序列，都是在回避同一维度的膨胀问题**；（b）它给出的"负载升高 → 被迫走跳数更多的路径 → 时延上升"（L465）与 **AF674CSF 的负载结论方向一致**。**本批内它是唯一使用 GNN 的论文。**

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
*[回填位·已回填]* **本批内无任何篇目引用 QMIX 或 VDN**（无一篇的参考文献出现本文）。**这是本批唯一的纯 MARL 算法论文，与其余 10 篇在引用网络上完全孤立**——它既不被 LEO 论文引用，也不引用 LEO 论文。**与 A7QNRKML (LOTR) 并列为本批两个"语料离题项"**，但性质不同：QMIX 至少是"可被引用的方法组件"（CTDE 单调分解），LOTR 连这个价值都没有。

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
*[回填位·已回填]* **本批内的引用关系（双向确证）**：（a）**它引用了 8AYW2Y78 (Hypatia)**（其参考文献 [2]）；（b）它在 **AF674CSF (LPIH)** 的参考文献里以会议版身份出现（AF674CSF 的 [10]：Zhang, Wang, Zhang, Meng, Luo, WiOpt 2023）；（c）**AIH4GK37 (PBAR) 在 Related Work 里点名批评了它与 ASER**——"ASER... studies ISL churn in a polar shell, **uses one fixed partition, and provides no geometry-based model**"（AIH4GK37 L427），**这句话同样适用于用同一分组法的 LPIH**。它与 9KZDXPKC (DB-R) **同属北航 Zhiyuan Wang / Shan Zhang / Qingkai Meng / Hongbin Luo 课题组**，两者是"包头里放 BF"与"路由表里放默认/备份路由"的两种答案。

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
*[回填位·已回填]* **它引用了 8AYW2Y78 (Hypatia)**（其参考文献 [4]）。**与 9GPFG5U3 (LiR) 同课题组**（Zhiyuan Wang / Shan Zhang / Qingkai Meng / Hongbin Luo），**且 LiR 的会议版正是 DB-R 的参考文献 [10]**——两条引用链在组内对得上。**本批内它对 8AYW2Y78 的延伸最直接**：Hypatia 定性说"loss/delay 都是坏信号"，DB-R 把它量化成"CUBIC 吞吐最多掉 67%、BBR 掉 41%"并给出修复方案。**与 AZ72LM9Z 形成参数对照**：DB-R 实验配置的是 5 秒 ISL 失效，而实测中断是 50–75 秒量级（AZ72LM9Z L136）——**DB-R 的事件参数偏乐观**。

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

## A7QNRKML — LOTR: Face Landmark Localization Using Localization Transformer (IEEE Access, Sertis Vision Lab)

**1. 一句话**
用 **Transformer（DETR 的思路）做人脸关键点的"直接坐标回归"**，绕开热力图方法的昂贵后处理，并顺手修掉了 Wing loss 在阈值处和零点处的**梯度不连续**（提出 smooth-Wing loss）。

**2. 问题设定**
人脸关键点定位（L17）有两条主流路线：
- **坐标回归**（L23）：CNN + 全连接直接出坐标。问题是**特征图在全连接前被压缩，造成空间信息丢失**（L23 逐字："most regression-based approaches suffer from spatial information loss due to the compression of feature maps before the fully-connected layers"）；早期级联 CNN 路线还有架构复杂度高、推理慢的问题。
- **热力图回归**（L25）：预测每个像素的关键点概率图，性能更好、收敛更快，但**依赖计算量很大的后处理把热力图转成坐标，推理时间被拖长**（L25 逐字："these approaches usually rely on a computationally intense postprocessing step"）。**这就是本文的首要动机**（L25："tackling this issue is the primary motivation behind this paper"）。

**3. 方法骨架**

**(A) LOTR 架构（§III-A）**——三模块（Fig 1, L28）：
1. **Visual backbone**（L128）：预训练 CNN（**MobileNetV2 / ResNet50 / HRNet**）产生特征图，1×1 卷积降维；特征图分辨率太低（192×192 输入只有 6×6）时**可选地插反卷积上采样层**。
2. **Transformer 模块**（L130-L183）：特征图 $F \in \mathbb R^{W\times H\times C}$ 经 1×1 卷积 + reshape 成 token 序列 $X^0 \in \mathbb R^{WH\times D}$（式 8）。**编码器** L 层（MHSA + PFFN，带残差与 LN，2D 位置编码只加在 query/key 上，与 DETR 一致，式 9-13）；**解码器** L 层（MHSA + **MHCA 交叉注意力** + PFFN，式 14-18），输入是 **N 个可学习的 landmark queries** $Y^0 \in \mathbb R^{N\times D}$，N = 要预测的关键点数。
3. **Landmark prediction head**（L185）：两层隐层（512 节点，ReLU）的 PFFN，**输出层只有 2 个节点且无激活函数**（式 19），直接给出 (x, y)。
- **与 DETR 的两点差别（L100）**：(1) 没有类别预测头（所有关键点同属一个类别）；(2) **不需要匈牙利损失**（关键点数量固定）→ 可以端到端训练，无需后处理。
- **复杂度（L193）**：编码器 MHSA 随特征图尺寸**平方增长** $O((WH)^2 D + WHD^2)$；解码器 MHSA 只随关键点数 $O(N^2D + ND^2)$；MHCA 线性 $O(NWHD + (N+WH)D^2)$。

**(B) smooth-Wing loss（§III-B，本文的第二个贡献）**
- **Wing loss 的缺陷（L120）**：在阈值 $w$ 处**梯度不连续**，在零误差处也不连续（Fig 2 底排），"might affect the stability of training"。
- **smooth-Wing（式 21）** 三段式：$|x|<t$ 时用**二次** $sx^2$（让零点梯度平滑）；$|x|>w$ 时退化为 L1 形式 $|x|-c_1-c_2$；中间段用对数 $(w+\epsilon)\ln(1+|x|/\epsilon)-c_2$。常数 $s = \frac{w+\epsilon}{2t(\epsilon+t)}$（式 22）、$c_1$（式 23）、$c_2 = st^2$（式 24）**是解出来的，目的就是在内阈值 t 和外阈值 w 两处都让损失与梯度连续**。
- 作者用的参数：**内阈值 t = 0.01，外阈值 w = 10，陡度 ε = 2**（L251）。

**4. 它声称的效果**
- **WFLW 数据集（Table II, L270）**：LOTR-HR+ 达到 **NME 4.31%**、**AUC 60.14%**——"surpassing all the state-of-the-arts by a large margin (0.44–6.91 points)"（L259）。**NME 与失败率上不如 HIH**（HIH NME 4.18%），但 **AUC 更高**（L259）。
- **JD-landmark 数据集（Table III, L287）**：**LOTR-R+ AUC 87.71%、失败率 0.00%、NME 0.98%**；最小的 **LOTR-M 也有 87.05%**，**比挑战赛榜首（Baidu-VIS 84.01%）高出 3 分以上**（L289）。相比热力图方法 [34]（Xiong et al.，AUC 83.34%）**高出 3.7–4.5 分**。
- **速度（§IV-G1, Table V, L307）**：相比热力图基线 [1]，**GPU 推理时间减少约 4–6×**，模型大小与参数量相当。**LOTR-R+ 带 flip 比 [1] 的 MobileNetV2 模型带 flip 快约 4.4×**。人脸检测预处理固定耗时 **43.36 ± 4.82 ms**（L307）。
- **FLOPS（L291）**：LOTR-M 仅 **0.23 GFLOPS**；LOTR-M+ 因上采样层高 47%（0.44 GFLOPS）；LOTR-R+ 因 ResNet50 达 **3.23 GFLOPS**。
- **消融（§IV-G）**：
  - **损失函数（Table VI, L329）**：L2 (84.52) < L1 (86.90) ≈ smooth-L1 (86.87) < Wing (86.92) < **smooth-Wing (87.05)**（以 LOTR-M 为例），**smooth-Wing 在三个模型上一致最优**。
  - **CNN+FFN 对照（Table V, L325）**：把 Transformer 换成 FFN 后性能下降（MobileNetV2 上 85.85 vs LOTR-M 的 86.39），说明 Transformer 模块确有贡献。
  - **层数（Table VII, L341）**：**L=2 最好**；L≥3 开始变差；**L=5/6 时出现 NaN 或崩到 44%**（L345："might be a consequence of training instability when the number of layers becomes very large"）。
- **下游人脸识别（§IV-F, Table IV, L299）**：用 LOTR 的 106 点中抽出 5 点做人脸对齐，**CPLFW 上 LOTR-R+ 提升 10.83 分**（大姿态数据集），CFP-FP、CALFW、IJB-B/C 也有小幅提升；**LFW 上无提升**（已饱和）。

**5. 实验条件**
- **数据集**：**JD-landmark**（106 点；11393 训练 / 2000 验证 / 2000 测试，L231）与 **WFLW**（98 点；7500 训练 / 2500 测试，L233）。WFLW 超过 78% 的测试图带 1–4 种属性标注（姿态/表情/光照/化妆/遮挡/模糊）。
- **预处理（L235）**：用 Deng et al. 的 ResNet50 人脸检测器取框和 5 个关键点做裁剪对齐，**JD 缩放到 192×192，WFLW 缩放到 256×256**。
- **指标（§IV-B）**：NME（式 25，JD 用 $\sqrt{W_{bbox}H_{bbox}}$ 归一化，WFLW 用瞳距归一化）、失败率（JD 阈值 8%、WFLW 10%）、AUC。
- **训练（§IV-C, L251）**：He 初始化；位置编码与 landmark queries 都用标准正态初始化（queries 标准差 $10^{-4}$）；**LAMB 优化器，基础学习率 $10^{-3}$，100 epoch，第 50/75 epoch 各降 0.1 倍，batch size 32**；MXNet + Gluon；**单张 NVIDIA Titan X**。
- **评估硬件（L305）**：Intel Xeon E5-2698 v4 + **NVIDIA Tesla V100 SXM2, 32 GB**。
- **推理技巧（L289）**：与 [1] 一样用**水平翻转平均**提升精度。
- **训练与评估**：标准监督学习（有明确 train/val/test 划分），**与本文的 LEO 主题无关，不存在"同分布/跨分布"问题在 LEO 意义上的对应**。

**6. 它自己承认的局限**（逐字引用）
- L259："Although our proposed LOTR model does not surpass the performance of HIH in terms of NME and failure rate, it outperforms this state-of-the-art model on the AUC metric."（**在 NME 与失败率上并未超过 HIH**）
- L345："The results of the deepest models, i.e., L equals 6, is NaN, which might be a consequence of **training instability when the number of layers becomes very large**."（**深模型的训练不稳定问题被观察到但没有解决**）
- L299："The results reported in Table IV indicate **no improvement on LFW** with either of the face detectors and the LOTR models."
- L74/L80（对 HIH 的评价里隐含本文的边界）：热力图方法的"post-processing complexity and the lack of an end-to-end pipeline"**remain unaddressed**——即本文认为这个问题到 HIH 为止都还没解决。
论文**没有 Limitations 章节**，也没有未来工作章节（第 V 节 Conclusion 后直接是参考文献）。

**7. 它没做但看起来能做的地方（基于内容）**
1. **L≥5 训练崩溃（NaN）没有解释也没有缓解**（L345）。这是 Transformer 深度的典型问题，作者只观察未处理；LayerScale / 更好的 warmup / 预 LayerNorm 都是显然的下一步。
2. **LOTR 与 DETR 的差别之一是"不需要匈牙利损失因为 N 固定"**（L100）。**如果关键点数量可变或存在遮挡导致部分点不可见**，映射关系就不再天然对齐——作者在 WFLW（有遮挡子集）上仍用固定对应，**没有利用"不确定度/可见性"建模**（对比 LUVLi [47] 就是这个方向）。
3. **smooth-Wing 的 $t$ 固定为 0.01、$w$ 固定为 10**（L251），**没有对 t 做敏感性分析**，而 t 恰恰是"多小算小误差"的分界，直接决定损失在近零区的曲率。
4. **只在人脸关键点上验证 smooth-Wing**。作为一条通用损失函数，它在**其他回归任务（位姿、光流、关键点以外的检测框回归）**上是否也优于 Wing，没测。
5. **AUC 高但 NME/失败率不如 HIH**（L259）——作者把 AUC 当作主打指标，**没有解释这个指标分歧的来源**（AUC 对整体分布敏感，NME 对尾部敏感）。

**8. 和同批其他篇的关系**
**与同批其他 10 篇没有任何关系**：
- 本批其余篇目全部是 **LEO 卫星网络 / 路由 / 传输层 / 多智能体 RL** 主题，本篇是**纯计算机视觉的人脸关键点定位**，两者在问题域、方法域、数据集、评测指标上**零交集**。
- **不引用同批任何一篇**，也**不可能被同批任何一篇引用**（参考文献 [1]-[76]，L365-L518，全部是人脸识别/关键点/CV 领域的文献）。
- **与 9FLZ88LZ (QMIX) 的相似性是"表层的"**：两者都是**方法论文**（不含任何应用领域数据），都用到了注意力/序列建模的思路；但 QMIX 是多智能体 RL 的值分解，LOTR 是 CV 的回归架构，**机制上没有可迁移的共享组件**。
- **唯一勉强算得上"谱系相关"的点**：LOTR 是 "**Transformer 编码器-解码器 + 可学习 query 集合 + 直接回归**" 这一模式（源自 DETR）的一个应用实例。**如果 111 篇全库里存在用 Transformer/注意力做 LEO 路由决策的论文，那它们与本篇共享的是同一个架构母题（DETR 式 set prediction）**——但这只是架构层面的远亲，不构成实质关联。本批目前尚未见到这类论文（8AYW2Y78 是仿真器、9C6HB6AF 是 GNN+DRL、9FLZ88LZ 是 MARL、9GPFG5U3 是 BF 源路由、9KZDXPKC 是内核路由、8N9QJHC2 是 Q-learning）。

**9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实**
**没有任何贡献，而且是彻底的无关。** 本篇：
- 没有网络、没有链路、没有队列、没有到达率、没有时延；
- 评测指标是 **NME / 失败率 / AUC / 推理时间（ms）/ FLOPS**，全部是视觉精度与算力指标；
- 全文唯一的"时间"概念是**模型推理耗时**（4.6 ms 量级，Table V, L317），与网络时延无关。
**唯一可以跨域借用的一句观察**（但作者并非为此而写）：L307-L309 指出热力图方法"**some complex operations in its post-processing stage could not efficiently utilize GPU acceleration, resulting in high computational time**"——**即"算法的一部分不适合硬件加速 → 端到端时延被拖垮"**。这与 S85KQ4FC 关心的"星上推理速度跟不上转发速度"在**抽象层面**是同一类失效（计算管线中的瓶颈段决定端到端表现的尾部），但**本篇完全在 CV 语境下，不能、也不应该被用来支撑 LEO 的论断**。

**10. 一句话评价**
一篇**质量正常但与本课题完全不相关**的人脸关键点定位论文（DETR 式直接回归 + 修好梯度连续的 smooth-Wing loss，工程扎实、消融完整）；它在 111 篇语料里的存在只能说明**语料构成里混入了非 LEO 的计算机视觉文献**，对"负载变化下的到达率/时延"这一选题**不提供任何事实、方法或引用价值**。

## AF674CSF — Logic Path Identified Hierarchical Routing for Large-Scale LEO Satellite Networks (IEEE TNSM 2024, Beihang)

**1. 一句话**
把星座**切成若干卫星组**、只在组内通告 ISL 状态变化（治"收敛慢"），再用一个**逻辑路径标识 PID** 表示相邻组之间的通路——**一个 PID 对应多条物理 ISL**，所以组间转发天然抗单链路失效；同时把组内路由（host-centric，push）和组间路由（information-centric，pull）**解耦**，兼得两种范式的便宜。

**2. 问题设定**
大规模星座有三个让路由设计难做的原因（L17）：
1. **异轨 ISL 会周期性断开**：卫星进入极区时天线失配，对应的 ISL 会被规律性地关闭/开启（L17 逐字："the inter-orbit ISLs will be regularly turned down (or on, respectively) when the satellite enters (or leaves, respectively) polar zones as the antennas of the corresponding satellites are misaligned in polar zones"）。
2. **ISL 偶发失效/恢复**。
3. **GSL 频繁切换**：地面站对单颗卫星的可见时间只有约 **2–3 分钟**（L17）。

**关键量化（Fig 1）**：**拓扑稳定时长（相邻两次拓扑变化之间的间隔）随星座规模增大而缩短**，ISL 失效时更严重（L17）。
**两类现有方案的死穴（L28, L30）**：
- **host-centric（ASER/OSPF）**：靠**事件触发式全局扩散**链路状态——小星座能用，**大星座 + 频繁链路变化必然陷入路由收敛问题**。
- **information-centric（NLSR）**：内容沿 Interest 反向路径回传，路径记在 **PIT** 里——**只要转发路径上有一条 ISL 失效，Data 包就丢**（L30 逐字："Data packets will be lost if one of the intermediate ISLs fails during the Data packet forwarding"）。**星座越大越严重**。

**3. 方法骨架**

**(A) 星座分组 + PID（§III-A）**
- **确定性邻居关系是前提（L72）**：Walker 星座中卫星沿轨道均匀分布，**任意两颗卫星的相对相位是确定的且固定不变** → 确定性的邻接关系。附录 A（L502）给出推导：同轨相邻角距 $\omega = 2\pi/M$，相邻轨相位偏移 $\Delta\omega = \pi/M$。
- **分组（L76）**：每组 = p 个轨道面 × 每面 s 颗星。**相邻组之间由 p 条同轨 ISL 或 s 条异轨 ISL 相连**。作者明确说组规模 (p, s) 的调优"is a significant topic that requires specific research, **which is not our main focus**"，直接沿用了 ASER [12] 的分组法。
- **PID（L81）**：表示相邻组之间（或 GS 与其连接组之间）的**逻辑通路**。**一个 PID 关联多条物理 ISL**（L111）→ **只要不是所有链路同时失效，PID 就保持不变**。PD 只在相邻两组之间已知，不向全网通告。
- **三维命名空间（L109）**：PID（逻辑路径）+ NID（节点标识，扁平结构，不用接口 IP，L117）+ content name。

**(B) 两类卫星（L121, L123）**
- **管理卫星**：记录全网内容可达性，为 GET 包追加下一跳组的 PID。每组 1 个或多个，由运营商决定。**作者给了个漂亮的定位（L121）**："NLSR and OSPF correspond to two extreme cases, where all the satellites exhibit the functionality of management satellites for NLSR and no satellite exhibits this functionality for OSPF." —— **即 LPIH 是 NLSR 与 OSPF 之间的连续谱**。
- **转发卫星**：按管理卫星追加的 PID 转发；维护组内路由表；需要知道 **PID → 边界卫星 NID 的映射（静态映射，开销很小）**。

**(C) 分层路由与两类 LSA（§III-C）**
- **组内 LSA**：传播每条物理 ISL 的连接状态，**在组内洪泛**（事件触发 push）。
- **组间 LSA**：传播相邻两组的连接状态；**只有当逻辑邻接关系变化时**（即两组的组间 ISL 全部同时失效）才生成，由管理卫星发给相邻组的管理卫星（L179）。
- **组内路由表（Fig 4, L145）**：目的 NID + 内容名 + 下一跳 NID + 度量（跳数）。
- **组间内容路由表（Fig 5, L175）**：内容名 + 下一跳组 + 对应 PID + 度量。

**(D) 包转发（§III-D, Fig 6）**
- **GET 包**（含内容名、消费者 NID、PID 序列）：收到后先查本地缓存（命中直接回）→ 查组内路由表（组内能解决就组内转）→ 否则若不是管理卫星就转给管理卫星 → 管理卫星追加 PID 并转到对应边界卫星。
- **DATA 包**：**沿 GET 记录的反向 PID 序列回传**。中间卫星**顺路缓存**（L253）。判断消费者是否在本组靠 **PID 序列是否为空**：空 → 按消费者 NID 转发；非空 → 转到下一跳组的边界卫星。
- 类似的源路由思路它自己承认像 [2] Handley，但强调目的是"整合 host-centric 与 information-centric 两种特性"（L93）。

**(E) 与 OSPF / NLSR 的机制对照（第 IV 节）**
- **OSPF（L271）**：ISL 失效 → 全网洪泛 LSA → 全网更新路由表；**同一内容被多用户请求会产生大量重复 DATA 包 → 拥塞**（L275）。
- **NLSR（L279）**：周期性 pull 式逐跳同步 LSA 名，再取 LSA DATA，**收敛比 OSPF 更慢**；靠 Interest 聚合与网内缓存降冗余，**但 ISL 失效会摧毁 PIT 记录的路由**（L289）。
- **LPIH（L293）**：组内通告 + 组间按 PID 通告 → **收敛更快、开销更小**；PID 对应多条物理 ISL → 单条失效时**可换到替代的组间 ISL**（L295）。

**4. 它声称的效果**（全部给定条件）
- **收敛时间与协议开销（§V-B, Fig 9）**：LPIH 与 ASER 的收敛时间**都小于 OSPF 和 NLSR**（因为只在组内扩散）；**分组数越多，收敛时间与开销越小**（L361）。LPIH 收敛时间与 ASER 相当，**但协议开销在分成 12 组时比 ASER 少最多 75.2%**（L363），原因是 LPIH 只在 LSA 是新的时才转给邻居（非入端口），冗余 LSA 被取消而不洪泛。
- **不同流量模式下的投递率（§V-C1, Fig 10/11）**：
  - **无 ISL 失效（Fig 10）**：LPIH 与 NLSR 的 PDR 相当，都好于 ASER；**ASER 的 PDR 从 point-to-point (U8P8) 转向 content-sharing (U8P1) 时持续下降**（host-centric 的重复传输导致拥塞丢包），**时延也因显著排队而上升**（L385）。
  - **ISL 失效率 20%（Fig 11）**：ASER 与 NLSR 的 PDR 从 U8P8 到 U8P1 **下降**，而 **LPIH 的 PDR 反而是上升的**（L387）。
- **不同 ISL 失效率（§V-C2, Fig 12/13）**：失效率 $\{0\%,1\%,...,20\%\}$。
  - **point-to-point (U8P8)**：三者 PDR 都随失效率下降；LPIH 与 ASER 相当；**NLSR 下降最快**（PIT 有状态转发更脆弱）。**LPIH-1 的 PDR 比 NLSR 高最多 105.3%**（L408）。时延都随失效率上升，**LPIH-A 时延最小**。
  - **content-sharing (U8P1)**：**LPIH-1 的 PDR 比 ASER 高最多 155.6%、比 NLSR 高最多 70.9%**，且 **LPIH 时延最小**（L410）。
- **不同流量负载（§V-C3, Fig 14/15）**——**这一节对本课题最关键**：
  - 设定：**ISL 失效率固定 20%**，负载 = 每个用户的内容请求率（requests per second）。
  - **总体趋势（L437）**：**更重的负载 → 三个协议的 PDR 都更低、时延都更高。**
  - **point-to-point (U8P8)**：**LPIH-A 的 PDR 最高，NLSR 最低**（NLSR 处理不了偶发链路失效）。**LPIH-A 时延小于 ASER；但 NLSR 的时延比 LPIH 更低**——作者给了理由（L437）："**This is because we only take into account the successful packet delivery.**"（**即只统计成功送达的包——存在幸存者偏差**）
  - **content-sharing (U8P1)**：**ASER 的 PDR 随负载上升显著下降，LPIH 只轻微下降**；**LPIH-1 的 PDR 比 ASER 高最多 266.9%、比 NLSR 高最多 67.8%**（L439）。
- **星座规模可扩展性（§V-D, Fig 16/17）**：跨 Telesat / OneWeb / Starlink-S2 / GW 四种规模（统一 9×10 分组），**LPIH 的收敛时间基本持平**（因为只在组内通告）；**LPIH 的路由表比 ASER 小**（PID 解耦了组内可达性 + 用 NID 而非 IP 前缀，L462）。
- **多壳星座（§V-D3, Fig 18）**：Starlink-S1（高壳，内容提供者）+ S2（低壳，用户），**LPIH 在四种流量模式下 PDR 都高**；时延随模式从 U8P8 转向 U8P1 而**下降**（网内缓存减少冗余传输）。

**5. 实验条件**
- **平台**：**OMNeT++ 6.0.1** 自建仿真平台，三大模块——星座模块、网络模块（协议栈/排队策略/网内缓存）、流量生成模块（L303-L316）。跑在 Ubuntu 20.04 + VMware ESXi 6.5.0 + 曙光服务器上。
- **拓扑（Table I, L312）**：**Telesat 351 颗（27×13, i=98.98°, 1015 km）**、**OneWeb 720 颗（18×40, i=87.9°, 1200 km）**、**Starlink-S1 720 颗（36×20, i=70°, 570 km）**、**Starlink-S2 1584 颗（72×22, i=53°, 550 km）**、**GW（国网）2000 颗（40×50, i=50°, 600 km）**。每星最多 4 条 ISL（2 同轨 + 2 异轨）。
- **主实验星座**：**OneWeb**，采用 **6×10 分组 → 12 组，每组 60 颗星**（L367）。
- **分组方案扫描**：$\{1,4,8,12\}$ 组，对应 $\{18\times40, 18\times10, 9\times10, 6\times10\}$（L330）。
- **链路与包**：**所有链路（ISL 与 GSL）容量 10 Mbps**，**每条 ISL 缓冲区 500 个包**，**DATA 包载荷 1 KB**（L340）。
- **拓扑动态**：**ISL 失效与恢复事件按 Poisson 过程随机、独立生成**，给定速率 λ（L305）。失效率扫 $\{0\%,1\%,...,20\%\}$（L367）。
- **流量模式（L334）**：记作 $U_xP_y$ = x 个用户向 y 个提供者请求内容；从 **U8P8（point-to-point）** 到 **U8P1（content-sharing）**。
- **负载设定（L336）**：**"Traffic load is characterized by the content request rate of each user, which is measured by the number of requests per second"** —— **这就是一条真正的到达率轴**（每用户请求数/秒）。
- **训练与评估**：**无训练**（协议设计 + 仿真），三个协议（LPIH-1 / LPIH-A / ASER / NLSR）在同一平台上对照。

**6. 它自己承认的局限**（逐字引用）
- L76（分组规模）：「In practice, the group scale (p, s) could be flexibly set to achieve the desired tradeoff between inner-group routing stability and inter-group routing stability under LPIH routing mechanism. **This is a significant topic that requires specific research, which is not our main focus.** Thus, we adopt a similar constellation partition method with ASER [12].」（**核心超参没有自己的方法，直接抄 ASER**）
- L437（最诚实的一条，且直接暴露了度量缺陷）：「the average packet delay of NLSR is smaller than that of LPIH. **This is because we only take into account the successful packet delivery.**」（**只统计成功的包 → 时延对比有幸存者偏差，作者自己点破了**）
- L496（结论里的未来工作）：「There are some open issues that need to be investigated in the future. **First, we would study how to improve the network throughput via multipath content delivery. Second, it is also interesting to extend LPIH to the multi-shell constellation.**」（**注意：多壳其实在第 V-D3 节已经做了实验**（Fig 18），结论却说"未来再扩展"，**前后不一致**）
- L37（对自身定位的限定）：「based on our previous work in [1]」——本文是会议版 [1] 的期刊扩展。

**7. 它没做但看起来能做的地方（基于内容）**
1. **分组规模 (p, s) 是全文最关键的旋钮**（决定组内/组间稳定性的权衡），却被明确推给未来工作（L76）。**做一次 (p,s) 的二维扫描**是最直接的缺口——而且代价很低，仿真平台已经搭好了。
2. **时延统计只算成功包**（L437），作者自己承认。**把丢包计入时延（或同时报"丢包率-时延"的联合分布）**会显著改变 NLSR vs LPIH 的结论。这是一个现成的、可复现的修正实验。
3. **PID ↔ 多条物理 ISL 的映射是静态的**（L123 说"static mapping, thus merely incurs little overhead"）。但在极区，**异轨 ISL 会被规律性地关闭**（L17）——**映射表是否需要随轨道位置变化？** 论文没有讨论静态假设与"极区周期性断链"之间的冲突。
4. **组间 LSA 只在"所有组间 ISL 同时失效"时才生成**（L179）。那么**部分失效（比如 4 条组间 ISL 挂了 3 条）**时，PID 仍然有效但带宽骤降——**这个中间状态如何被感知、如何影响转发？没有讨论**。
5. **缓存策略没有具体设计**（L253 只说"顺路缓存"）。缓存放哪、多大、替换策略是什么——**全部留白**，而这是 information-centric 收益的主要来源。
6. **只对比了 ASER 和 NLSR**，没有对比同作者组的 LiR（9GPFG5U3 的 BF 源路由）或 DB-R（9KZDXPKC）。
7. **流量负载只扫了 PDR 和时延，没有报吞吐**，尽管结论里说未来要"improve network throughput via multipath"（L496）——**当前连单路径的吞吐数字都没给**。

**8. 和同批其他篇的关系**
- **和 9GPFG5U3 (LiR) / 9KZDXPKC (DB-R) 是同一作者群的系列作**：本文作者 **Fei Yan, Zhiyuan Wang, Shan Zhang, Qingkai Meng, Hongbin Luo**（L3）——**Zhiyuan Wang / Shan Zhang / Qingkai Meng / Hongbin Luo 与 LiR、DB-R 三篇完全重合**。这是一个北航团队在 LEO 路由方向的**系统性产出线**。
- **引用了 Handley 的 "Delay is not an option" [2]**（L514）——本批 8AYW2Y78 的参考文献 [29] 也是这一篇。**三篇同源文献（Hypatia 系列）在这个组的引用里反复出现**（本文引了 Handley，LiR 和 DB-R 引了 Hypatia 和 Handley）。
- **与 9GPFG5U3 (LiR) 是"同一个拓扑事实的两种用法"**：两者都建立在**确定性邻居关系**上（本文 L72/L502 vs LiR L17）。但 **LiR 把路径信息压进包头的 Bloom Filter**，本文 **LPIH 把路径信息记成 PID 序列放进包**（也是源路由风格）——**两者是"包头里放什么"的两条不同答案**，且同样面对"包头开销 vs 状态开销"的权衡。
- **与 9KZDXPKC (DB-R) 互补**：DB-R 处理的是"链路事件瞬间丢包"，LPIH 处理的是"事件通告范围太大导致收敛慢"。**两者治的是同一场病的不同症状**（DB-R 治丢包，LPIH 治收敛/开销）。
- **与 8N9QJHC2 的对照**：8N9QJHC2 用贝叶斯把故障**分型**（临时 vs 永久）再差异化处理；**LPIH 完全不分型**，用的是"分组 + PID 冗余"来**绕过**这个问题。哲学完全不同。
- **与 8AYW2Y78 (Hypatia) 的关系**：Hypatia 指出"路径频繁变化"（其 L304-L308，200 秒内中位数 4 次换路）；**LPIH 正是针对这一点做的架构**——把"全局路径变化"降级为"局部链路变化"。**这是一条清晰的"问题提出 → 架构回应"链**（Hypatia 提出 → LiR/LPIH/DB-R 三种回应）。
- **与 9C6HB6AF / S85KQ4FC 的分野**：那两篇用 RL/DRL 做决策；**LPIH 是纯协议设计，零学习成分**，靠的是拓扑确定性 + 分层。
*[回填位·已回填]* **本批内的引用关系**：（a）它引用了 **AJJI57M9 (Ekici et al.)**（其参考文献 [11]）与 **Handley**（[2]）；（b）**它被 AIH4GK37 (PBAR) 引用并点名批评**——PBAR 引其作者群的 [20]（F. Yan, H. Luo, S. Zhang, Z. Wang, P. Lian），并指出前人"uses one fixed partition, and provides no geometry-based model"（AIH4GK37 L427）；（c）**它与 9GPFG5U3 (LiR)、9KZDXPKC (DB-R) 同属北航 Zhiyuan Wang / Shan Zhang / Qingkai Meng / Hongbin Luo 课题组**——三篇构成本批最大的单一课题组产出线。**与 AIH4GK37 是同一问题（泛洪扩散范围）的两条解法**：LPIH 用自定义 PID 推倒 OSPF 重来，PBAR 坚持标准 RFC 兼容。

**9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实**
**这是本批第二篇真做了负载扫描的论文**（第一篇是 9C6HB6AF），而且**它的负载定义比 9C6HB6AF 更接近"到达率"**——L336 逐字："**Traffic load is characterized by the content request rate of each user, which is measured by the number of requests per second**"。具体贡献：
1. **负载-时延的单调关系被三个协议共同证实**：L437「**a heavier traffic load will lead to a lower average PDR and higher average packet delay for the three routing protocols**」——**在 ISL 失效率固定 20% 的条件下**，负载上升 → PDR 降、时延升。
2. **不同架构对负载的敏感度差异极大**：同样是从 point-to-point 转向 content-sharing，**ASER 的 PDR 随负载"显著下降"，而 LPIH 只"轻微下降"**（L439）。**这是"协议设计决定负载-性能曲线斜率"的直接证据。**
3. **作者自己暴露了一个度量陷阱（L437）**："the average packet delay of NLSR is smaller than that of LPIH. **This is because we only take into account the successful packet delivery.**" —— **只统计成功包的时延会系统性偏袒丢包率高的协议**。这是一条对任何"到达率 vs 时延"实验都通用的方法学警告，价值很高。
4. **负载效应与失效效应是可以分离的两个轴**：论文分别扫了 ISL 失效率（0–20%，Fig 12/13）和流量负载（Fig 14/15），**且在第 V-C3 节把失效率固定在 20% 再扫负载**。这个"固定一个轴、扫另一个轴"的做法是对的，虽然**没有做二维联合扫描**。
5. **一个反直觉的趋势**：在 ISL 失效 20% 下，**LPIH 的 PDR 随流量模式转向 content-sharing 反而上升**（L387），而 ASER/NLSR 下降。**即"负载组成的变化"（用户/提供者比例）比"负载大小"影响更大**——这对"到达率"这个词的界定有直接启示：**到达率的分布结构（谁向谁发）与时延的关系，可能强于到达率的绝对大小**。

**10. 一句话评价**
**这篇文章把"确定性邻居关系"这条 LEO 拓扑真理用到了极致**（分组收敛 + PID 抽象成多物理链路的逻辑通路 + host/information-centric 分层解耦），并给出了本批少见的**真实流量负载扫描**；**最值得记住的其实是它自己承认的那句"只统计成功包"**——这既是它结论的软肋，也是对全库所有"负载-时延"实验的一记通用警告。分组规模这个核心旋钮被推给未来工作、缓存设计完全留白，是它留给后人的两个明确接口。

## AIH4GK37 — How Area Geometry Shapes Link-State Routing Scalability in LEO Networks (UCLA / U. Arizona)

**1. 一句话**
PBAR（代理式区域路由）能压住 LEO 链路状态泛洪，但**"区域怎么切"从来没规矩**；这篇用**环面网格几何**推出三条设计规则（存在中间最优尺寸、形状要方正、绕行代价取决于是否保住环面回绕方向），再用 ns-3 上的 OSPF 实现跑了 **18 种区域划分**去验证。

**2. 问题设定**
大规模 LEO 星座是"数千卫星 + 数万 ISL"的密集动态骨干，**轨道运动、网关切换、链路失效三者持续产生路由事件**，压垮链路状态协议的可扩展性（L21）。**扁平设计把每次更新泛洪到全网**，开销随网络规模与事件频率双双增长（L78）。
已有的收敛手段是**区域路由**（PBAR：RFC 9666 定义 IS-IS 机制 [2]，RFC 9717 把它用到卫星 [1]，ASER [3] 在极轨星座上做了 OSPF 实现）——**但**（L29 逐字）："Unlike terrestrial networks, LEO constellations inherit no administrative or geographic area boundaries. **Prior work evaluates a fixed partition but does not explain how geometry governs local versus global flooding or how to choose a division**."
**关键结构性差异（L87）**：地面 OSPF 区域预设一个**骨干区 Area 0**，所有跨区流量必经它，summary（Type-3/4）与 external（Type-5）LSA 跨 ABR 流动；**而 LEO 星座没有稳定的骨干子集来扮演这个角色**——所以要用 proxy-based 设计，让每个区域**直接向其余星座做自我摘要**。
**作者明确声明研究立场（L25）**：不比较"分散式链路状态 vs 集中式路由"谁更优，**而是把"用分布式链路状态"当作前提**，只研究它的区域结构该怎么配。

**3. 方法骨架**

**(A) 系统模型（第 II 节）**
- **四个邻居的结构化 ISL 图（L57）**：每星 **2 条沿轨（同轨道面）+ 2 条跨轨（相邻轨道面）**。因为壳层是**倾斜而非极轨**，相邻轨道面的卫星**近乎平行运动、相对速度低**，所以跨轨 ISL 可以持续存在 → **整体构成一个在两个方向都能回绕的环面网格（toroidal grid）**。卫星位置持续变化，**但网格结构本身稳定**。
- **作者自己划定了结论边界（L57）**："Our conclusions are scoped to this stable four-neighbor graph. **Richer topologies, including dynamic links between northbound and southbound tracks, require planned updates for predictable changes and are outside this study.**"
- **网关中心的可达性模型（§II-B, L64，遵循 RFC 9717）**：每个网关持有 IP 前缀，对外用 BGP 通告、对内通过其服务卫星注入星座；用户终端从本地网关前缀下取地址。**因为地址分配不涉及路由协议，用户终端的接入与移动不产生路由更新**——这是一个干净的解耦。
- **两类路由事件（§II-C）**：**GSL 驱动**（网关切换服务卫星集合 → 前缀撤回/重新注入）与 **ISL 驱动**（邻接图变化）。论文**把两者独立评估**以隔离各自影响。

**(B) PBAR 机制（第 III 节）**
- 每颗卫星**恰好属于一个区域**（按卫星而非按链路划分，L251）；每区选一个 **area leader** 作为代理（area proxy 是 RFC 定义的机制名，area leader 是执行它的路由器，L93——作者刻意区分这两个词）。
- **区域内部拓扑对外隐藏**，只暴露紧凑的 **area summary**。
- **事件二分（L97）**：**本地事件**（不改动导出摘要，如区内链路变化）只在发起区内泛洪；**全局事件**（改变导出摘要）由 leader 生成新摘要并**全网泛洪**。在 OSPF 实现里，**全网阶段可以在本地泛洪完全收敛前就开始，两个阶段时间上可重叠**（L113）。
- **两种代表性划分（Fig 4）**：**stripe-based（条带，横跨整个轨道面）**与 **grid-based（网格，两个方向都受限）**。

**(C) 解析模型（第 IV 节，全文核心）**
设壳层有 $W_0$ 个轨道位置 × 每轨 $H_0$ 颗星 = $N = W_0H_0$ 颗（式 1），呈**环面网格**；每星 4 条 ISL → $2N$ 条不同 ISL。
- **区域数（式 2）**：$K(w,h) = \frac{W_0}{w}\cdot\frac{H_0}{h} = \frac{N}{wh}$。
- **区内 ISL 数（式 3）**：$E_{in}(w,h) = (w-1)h + w(h-1) + \mathbf 1_{\{w=W_0\}}h + \mathbf 1_{\{h=H_0\}}w$，**两个指示项专门处理"区域横跨整个壳层时环面回绕链路仍属区内"**。
- **本地泛洪开销（式 4）**：$C_{loc} = \gamma_{loc}E_{in}$——**区域越大，单次本地泛洪越贵**。
- **边界暴露（式 5-6）**：$E_{cut}$ 是跨区 ISL 数，$\beta(w,h) = E_{cut}/(2N)$。**对均匀采样的 ISL 失效，β 恰好就是"失效链路是跨区链路"的概率**（L177）。
- **全局传播概率（式 7）**：$q = \min\{1, \alpha\beta\}$。**α 是事件类型相关的缩放因子，作者明确说"leave uncalibrated"**（L183）。
- **式 (8)（最漂亮的一条）**：当 $w<W_0$ 且 $h<H_0$ 时，$\beta(w,h) = \frac{1}{2}\left(\frac{1}{w}+\frac{1}{h}\right)$ —— **固定面积 $wh$ 时，越方正（balanced）的区域边界暴露越小**（L191）。
- **总开销率（式 10）**：$R(w,h) = \lambda\left[C_{loc}(w,h) + q(w,h)C_{glob}\right]$，其中 $C_{glob} = 2\gamma_{glob}N$（式 9），**λ 是路由事件率**。**增大 w、h 抬高 $C_{loc}$ 但降低 q；减小则相反 → 最优在中间**（L205）。
- **收敛（式 11-13）**：区直径 $D_{loc}(w,h) = (w-1)+(h-1)$；$T_{loc} = \delta_{loc}D_{loc}$；$T \approx T_{loc} + q\cdot T_{glob}$。作者**自己声明式 (13) 不是严格串行时序模型**，只是一阶期望（L231）。
- **三条预测（L237-L241）**：
  - **P1（中间最优）**：开销与收敛时间都在**中间区域尺寸**取得最小。
  - **P2（方正形状）**：给定面积，方正划分优于细长划分（同时减小边界暴露与区内直径）。
  - **P3（回绕对齐）**：路径伸长的关键**不是区域数量，而是边界是否保住了较短的环面回绕方向**——**所以伸长率对区域粒度可以非单调**。
  - 作者补一句（L243）：**开销最优与收敛最优的划分未必重合**，因为开销由泛洪的邻接总数驱动，收敛更直接取决于传播距离。

**(D) 事件生成（§V-D）**
- **GSL 切换**：用公开整理的 Starlink 网关数据集（**129 个网关**，L288）。每个网关被**并发接入卫星数上限 $C_g$** 约束（相控阵天线数与波束预算）。**三种关联策略**：
  - **Closest-$C_g$**：始终接最近的 $C_g$ 颗（最激进，换得最勤）；
  - **Keep-$C_g$**：能保持就保持，只在必要时换（最保守）；
  - **Keep-$C_g$ with margin**：在 Keep 基础上加一个距离边际再换（居中）。
  - **关键机制（L296）**：**所有接入卫星通告同一个前缀**——所以一次切换只是改变了该前缀的**起始点集合**。
- **ISL 失效/恢复**：**同一时刻至多一条 ISL 失效**（隔离单次扰动）。用**单一 Pareto 分布**同时刻画 down 与 up 持续时间（**shape k=2.5, scale $x_m = 7.2$ s, 均值 12 s**），参数参考 Starlink 演示中报告的 ISL 建立时间（L298）。

**(E) 仿真实现（§V-A）**
- **ns-3** + **自研开源原生 ns-3 OSPF 模块**（ns3-ospf，L249）。
- **拓扑用 Hypatia 生成**（L249 逐字："Our constellation topological state is generated using **Hypatia**, which provides time-indexed satellite positions and link availability for ns-3 simulation [10]"）。
- **两类 LSA（L253-L255）**：**Local LSAs**（Local-Link 描述区内链路；Local-Prefix 携带本地外部前缀）**只在区内泛洪**；**Area LSAs**（Area-Prefix 汇总区内前缀通告全星座；Area-Link 把一个区域的跨区邻接**当作单个全局可见节点**通告）。
- **泛洪范围由转发逻辑强制**：Local-* 只发给同区邻居，Area-* 全局泛洪（L257）。
- **area leader 选举**：**确定性选 Router ID 最大的那台**（L259）。

**4. 它声称的效果**（全部给定条件）
- **无区域划分的基线（flat）**：
  - GSL 场景：**每次网关切换把 Local-Prefix LSA 泛洪到全部 1584 颗星，观测到的切换率下产生约 60 万包/秒**（L327）。
  - ISL 场景：**72×22 基线约 2800 包/秒**（L352）。
- **PBAR 对 GSL 动态（§VI-A, Fig 8/9）**：
  - **$C_g$ 越大，区域路由越有效**（因为同区内多颗卫星同时承载同一前缀，切换在前缀集合内发生 → **被本地吸收，零全局泛洪**）。作者给这个现象起名 **prefix replication**（L325）。
  - 完整 Keep-8 扫描下，**18×22 与 18×11 表现最好，控制包开销相对扁平泛洪最多降低 87%**（L327）。**流量体积下降比包数更平缓**，因为全局传播的 Area-Prefix LSA 聚合了多个网关前缀、**单包更大**（L327）。
  - **形状效应（L331）**：**72×2 划分（11 条两行条带，每条横跨全部 72 个轨道面）产出超过 160 MB/s 的跨区流量，是所有划分里最高的**；而 **4×11 在同面积下比 2×22 产生远少的全局触发**，因为形状紧凑、边界暴露小。
  - **Fig 9(c) 揭示对抗机制**：区域越大，越多的切换被保留为纯本地事件（绿），但每次本地泛洪的范围更大；区域越小，单次泛洪便宜但更多卫星暴露在边界上，全局触发增多（橙）。
- **PBAR 对 ISL 动态（§VI-B, Fig 10）**：
  - **即使最粗的划分（36×22、36×11）也能把包率降低一半以上**（L352）。
  - **形状（L356）**：**2×22（两个轨道面/区、占满整列）每列 21 条垂直 ISL 里只有 1 条在区内，另外一半落在跨区边界**；**h=2 的矮宽条带（横跨全部 72 个轨道面）把几乎一半的垂直 ISL（每列 21 条中 10 条）放在跨区接缝上**，全局触发率最高。
  - **与 GSL 情形的对比（L378）**：**ISL 情形下流量体积与包数成比例缩放**（每条 Area-Link LSA 只通告本区跨区邻接，包大小大致恒定），**而 GSL 情形不成比例**。
- **收敛时间（§VI-C/D, Fig 11/12）**：
  - **GSL 场景**：prefix replication 让大量切换保持本地，Area-LSA 比例更低，**总收敛时间更小，最小值仍在中间尺寸**（L386）。
  - **ISL 场景（最干净的一条）**：**最优划分 18×11 把平均收敛时间从 72×22 基线的 189.75 ms 降到 91.21 ms**（L396）——**"roughly halves convergence"**。
- **路径伸长（§VI-E, Fig 13/14）**：在基线 72×22 上取 **10 万个均匀随机的源-目的对**。**平均伸长在多数划分下接近 1**；**最差是 36×11：跳数伸长峰值 1.073、时延伸长峰值 1.079**（即 <8%）。**时延伸长略小于跳数伸长**，说明回绕方向的模糊决策"加了跳数但没有成比例地增加相对时延"（L406）。当区域横跨环面某一轴时，回绕歧义消失，伸长回落到 1。

**5. 实验条件**
- **仿真器**：**ns-3** + 自研 ns3-ospf 模块（L249）；**拓扑由 Hypatia 生成**（L249）。
- **星座**：**Starlink Phase 1 Shell 1，53° 倾角，72 个轨道面 × 每面 22 颗 = 1584 颗**（L280）。另算了 $\{48\times16, 64\times20, 72\times22, 90\times28\}$ 四种密度下的"可见候选卫星数"，高度与倾角固定。
- **区域划分**：**只在基线 72×22 上做矩形精确整除的划分**（保证无残余碎块），$w \in \{72,36,18,9,4,2\}$，$h \in \{22,11,2\}$，**共 18 种**（L280）。唯一例外是扫 $C_g$ 的 Fig 8，因为 22 只有 4 个因数（1,2,11,22），2 与 11 之间没有方正的中间高度，所以用了近似区域尺寸。
- **链路参数（Table I, L266）**：**ISL 带宽 10 Gbps**、MTU 8192 字节、FIFO 队列、**最大队列 100 000 包**、传播时延 = 发送时刻的 $\mathrm{dist}(t)/c$、链路 down 期间**丢包**。
- **三条关键假设（§V-B, L270-L276）**：
  - **(a) 固定路由度量**：所有 ISL 每跳度量固定为 1（同 ASER [3]），**使时延变化不触发路由更新**；
  - **(b) 不注入数据面流量**：L272 逐字 "**No user or data traffic is injected, avoiding congestion effects that could obscure control-plane behavior.**"；
  - **(c) 排除检测时延**（L274）：事件生成器决定变更何时对路由进程可见，**收敛从第一次通告发送测到最后一次处理**；周期性 Hello 也不计入开销。
- **作者自述的刻意排除（L276）**：多壳/极轨壳、并发 ISL 失效、数据面流量、协议检测定时器——**都刻意排除**，理由是"会引入额外机制，混淆本文的目标问题"。**目标是隔离控制面效应，而不是最大化场景广度。**
- **事件率**：GSL 场景用 **129 个真实 Starlink 网关**，仿真 **300 s**（Fig 8）与 **5 分钟**（Fig 9/11）；ISL 场景**一个轨道周期 5688 s**，MTTF = MTTR = 12 s（Fig 10/12）。
- **训练与评估**：无训练。**结论只在"稳定四邻居倾斜壳层"这个范围内有效**（L57）。

**6. 它自己承认的局限**（逐字引用）
这篇的自我限定写得**异常克制且具体**，几乎每节都加一句免责：
- L15（摘要）："**they do not claim that PBAR supersedes centralized or geographic routing.**"
- L35："Thus, PBAR can scale in the evaluated setting when distributed link state is selected. **This does not establish superiority over centralized or geographic routing.**"
- L57："**Our conclusions are scoped to this stable four-neighbor graph.** Richer topologies, including dynamic links between northbound and southbound tracks, require planned updates for predictable changes and are **outside this study**."
- L183："where $\alpha > 0$ is an event-type-specific scaling factor that **we leave uncalibrated**. The model is intended as an **explanatory tool rather than a quantitative fit** to simulation output."
- L231："Equation (13) is **not a strict serial timing model**; it is a first-order expectation that abstracts away overlap between area-leader re-origination and the tail of local flooding."
- L207："The 18×22 and 18×11 layouts are **results for our workload, not general optima**."
- L276（最关键的排除）："we intentionally exclude those factors here because they introduce additional mechanisms that would confound the paper's target question... **The goal of this study is therefore not to maximize scenario breadth, but to isolate the control-plane effects**..."
- L298（参数来源）："**Because public measurements of ISL outage and restoration times are limited**, we use a single Pareto distribution..."

**7. 它没做但看起来能做的地方（基于内容）**
1. **作者自己在第 IX 节 Future Work 里列了最诚实的缺口（L435）**，**第一条就是本课题的正中靶心**："**Congestion with mixed control/data traffic requires load-dependent costs and transient end-to-end evaluation.**" —— 即：**本文的模型里 $\gamma_{loc}$、$\gamma_{glob}$、$\delta_{loc}$ 全是常数，与负载无关**。把控制面开销与数据面拥塞耦合起来，是它自己指出的下一步。
2. **α（事件类型的缩放因子）未被标定**（L183）。这意味着模型能预测"存在中间最优"但不能预测"最优在哪"。**用仿真数据反标定 α，就能把模型从定性工具变成定量工具**——作者没做。
3. **λ 被当作常数**（式 10），但 GSL 事件率**本身强烈依赖于纬度与网关策略**（Fig 7(a) 显示 50° 纬度处 Closest-$C_g$ 比 Keep-$C_g$ 多约 1.3× 事件）。**用空间/纬度相关的 λ(x) 替换常数 λ** 是 Future Work 里也提到的一条（L435："spatial event rates"）。
4. **单条 ISL 失效**（L298）——作者自己承认"并发事件需要更丰富的事件模型"（L435）。
5. **Pareto 参数（k=2.5, $x_m$=7.2 s）来自一次 Starlink 演示的 ISL 建立时间**（L298），**几乎是无从校准的**。作者自述 "public measurements ... are limited"。
6. **多壳与极轨壳被排除**（L57, L276）。而 AF674CSF 恰好做了多壳（Starlink-S1+S2），且 LiR/DB-R 用的是极轨 Iridium——**这三篇的适用拓扑互相不重叠**，谁也没有把结论推广到对方的地形上。
7. **只测了矩形精确整除划分**（L280）。作者说框架支持非整除（L149, L431），但**没给非矩形的结果**——而真实星座的极区接缝会天然破坏矩形性。

**8. 和同批其他篇的关系**
- **直接使用 8AYW2Y78 (Hypatia) 作为拓扑生成器**（L249, 参考文献 [10] 在 L457）。**这是本批内第三条确证的 Hypatia 引用，而且是"当作工具用"而非"当作对比对象"**——与 LiR/DB-R 的"引用 Hypatia 佐证问题存在"不同，本篇是**把 Hypatia 当作仿真基座**。这标志着 Hypatia 到 2025-2026 年已成为该领域的**标准基础设施**。
- **与 AF674CSF (LPIH) 是"同一问题的两条解法，且互相引用"**：两者都把 LEO 分成区域/组以限制泛洪扩散。**但关键差异**：LPIH 用**自定义的 PID 抽象 + 内容中心分层**（推倒 OSPF 重来），AIH4GK37 则**坚持标准 OSPF/RFC 兼容**（L23, L410 "autonomous, standards-compatible link state"）。**更值得注意的是 AIH4GK37 引用了 LPIH 作者群的 [20]（L477：F. Yan, H. Luo, S. Zhang, Z. Wang, P. Lian，"A comparative study of IP-based and ICN-based link-state routing protocols in LEO satellite networks"）** —— 而且**明确点名批评前人**（L427）："ASER [3], the closest work, confines most LSAs within areas using designated area leaders. **It studies ISL churn in a polar shell, uses one fixed partition, and provides no geometry-based model.**" —— **这句话同时打到了 ASER 和（隐含地）LPIH**，因为 LPIH 也正是"固定分组 + 无几何模型"（AF674CSF L76 自己承认分组法直接抄 ASER）。**这是本批内最尖锐的一次实质性互评。**
- **与 9GPFG5U3 (LiR) / 9KZDXPKC (DB-R)**：那两篇是**北航组**的（Zhiyuan Wang 等），本篇是 **UCLA/Arizona 组**，**两派在"用不用标准协议栈"上立场不同**：北航派（LiR 用 BF 源路由、LPIH 用 PID、DB-R 用内核默认/备份路由）都**保留或改造 IP/OSPF 栈**；UCLA 这篇**明确站在"分布式链路状态 + RFC 兼容"这一侧**（L23, L410），**并在 Related Work 里把 OPSPF、ASER、Yan et al. 逐一点名划界**（L427）。
- **与 9C6HB6AF / S85KQ4FC 的分野**：那两篇用 DRL 做路由决策，**本篇零学习成分**，是纯几何+协议。**本批目前形成清晰的三派：DRL 派（9C6HB6AF, S85KQ4FC）、协议/架构派（LiR, LPIH, DB-R, AIH4GK37）、故障诊断派（8N9QJHC2）。**
- **与 A7QNRKML (LOTR) 的关系**：无。且本篇的存在进一步说明 **A7QNRKML 确实是语料里的离题项**——本批其余 LEO 论文彼此紧密交织（共享引用、共享作者、互相点名），而 LOTR 完全在外。
*[回填位·已回填]* **本批内引用关系（最密集的一篇）**：（a）**它把 8AYW2Y78 (Hypatia) 当仿真基座直接使用**（L249，参考文献 [10]）；（b）它引用了 **AJJI57M9 (Ekici et al.)**（参考文献 [15]）与 **ASER**（[3]）；（c）它引用了 **AF674CSF 作者群**的 [20] 并**点名批评**前人"uses one fixed partition, and provides no geometry-based model"（L427）；（d）**它与 AZ72LM9Z (Roman-HitchHiking) 是同一课题组的姊妹篇**（Lixia Zhang / Liz Izhikevich / Sirapop Theeranantachai / Beichuan Zhang 两篇共有）——**PBAR 是设计侧，Roman-HitchHiking 是测量侧**。**⭐ 最重要的关系是它被 AZ72LM9Z 的实测数据反驳**：它假设"at most one ISL down at a time"（L298），而实测到 597 次中断同时发生（AZ72LM9Z L141）。

**9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实**
**直接贡献：几乎没有——因为它把数据面流量和拥塞刻意排除了**（L272 逐字："No user or data traffic is injected, avoiding congestion effects"；L276 再次确认）。**全文没有包到达率、没有排队时延、没有负载扫描**；时延只出现在两处，且都不是负载时延：（a）路径伸长的**时延比值**（Fig 14，最大值 1.079，且是**传播时延**而非排队时延）；（b）传播时延按 $\mathrm{dist}(t)/c$ 逐包计算（L263）。
**但有三个概念性贡献值得记（都是"换个意义下的到达率"）：**
1. **本文的"到达率"是 λ = 路由事件率**（式 10 的 $R = \lambda[C_{loc}+qC_{glob}]$）。**在控制面语境下，"事件到达率"与"包到达率"是两条独立的轴**——本文证明前者对开销/收敛的影响可以被几何（区域形状）深刻调节。**这提示：在 LEO 里讨论"到达率对时延的影响"时，必须区分"数据包到达率"与"控制事件到达率"，二者由不同机制驱动、可被不同旋钮调节。**
2. **作者自己把"负载相关"明确列为未做（L435）**："**Congestion with mixed control/data traffic requires load-dependent costs and transient end-to-end evaluation.**" —— **这是一句可以直接引用为"研究缺口"的自述**：本文的 $\gamma_{loc}, \gamma_{glob}, \delta_{loc}$ 全为常数，把负载依赖引入成本模型是公认的下一步。
3. **一个可迁移的量化事实**：**控制面开销的量级本身极大**——扁平链路状态下，**每次网关切换要把 LSA 泛洪到 1584 颗星，观测切换率下约 60 万包/秒**（L327）；ISL 场景下基线约 **2800 包/秒**（L352）。**如果控制面与数据面共享链路（本文的排除假设一旦拿掉），这 60 万包/秒会直接转化为数据面的拥塞与排队时延**——这是"控制负载 → 数据面到达率/时延"耦合的一个现成量级估计，**但本篇没有做这个转换，是留给后人的**。

**10. 一句话评价**
**把"区域怎么切"这件工程直觉变成可推导的几何命题**（$\beta = \frac12(1/w+1/h)$ 与"存在中间最优"两条尤其干净），并用 18 种划分 + 两类事件在 ns-3/Hypatia 上做了扎实验证，**学术诚实度是本批最高的**（每节都写清结论适用边界，主动声明"不主张优越性"）；**但它把数据面流量与拥塞整体排除在外**，因此对"负载变化下的到达率/时延"这一选题**只贡献了缺口声明与量级参照，没有贡献任何负载-时延事实**——而且它自己把"负载依赖的成本模型"写进了 Future Work 第一条，等于亲手把这个口子留给了后来者。

## AJJI57M9 — A Distributed Routing Algorithm for Datagram Traffic in LEO Satellite Networks (Ekici / Akyildiz / Bender, IEEE/ACM ToN)

**1. 一句话**
LEO 路由的**祖师爷论文**：用"**逻辑位置**"（虚拟节点）把卫星运动从路由问题里彻底消掉，为每颗卫星**预先算好一张决策图**（decision map）塞进星上，于是**每包独立决策、零拓扑信息交换、零路由表**，走出近似最小传播时延的路径。

**2. 问题设定**
LEO 星座的包要经多跳才能从源到目的（L25）。卫星间由 ISL 相连：**同轨（intraplane）距离恒定**，**异轨（interplane）距离随纬度变化**——"horizontal distances are longest when satellites are over the equator and shortest when they are over the polar region boundaries"（L25）。**拓扑持续变化，但已建立的连接必须维持**（L25）。
**当时的主流方案都不合用（L27）**：既有 LEO 路由算法大多假设**面向连接**的网络结构（星上 ATM 或类 ATM 交换），**路径在地面交换机上集中计算**，再把路由表配到卫星上；卫星只负责按表转发。问题是**卫星运动会让初始路径分配失去最优性**，于是有了"path handover"方案——但**其性能严重依赖初始路径建立得有多好**（L27）。
而 IP 化趋势意味着**需要无连接（datagram）路由**，文献里尝试极少（L29）：**Darting 算法 [8]** 试图解决拓扑更新报文开销，但实验显示**Darting 的开销是扩展 Bellman-Ford 的数倍，而端到端时延还一样**（L29）。

**3. 方法骨架**

**(A) 网络模型（第 II 节）**
- **Walker 极轨星座 $M\times N/N/0^\circ$**（L40）：N 个轨道面均匀分布（角距 $360^\circ/(2N)$），**只在南北极上空相交**；每面 M 颗星（角距 $360^\circ/M$）。
- **逻辑位置（本文最核心的抽象，L42）**："**the entire Earth is covered by logical locations of satellites. These logical locations do not move and are filled by the nearest satellite.**" —— 整个地球被**不动的逻辑位置**铺满，每个逻辑位置由**最近的卫星**占据。卫星的物理身份与逻辑位置**永久解耦**（位置由同轨后继卫星接管）。**"The routing is performed basically by considering these logical locations as hops. By this way, we do not need to be concerned with the satellite movements."** —— 一句话把连续运动问题变成静态图问题。
- **ISL 长度**：同轨 $L_v = \sqrt2 R\sqrt{1-\cos(360^\circ/M)}$（式 1，**恒定**）；异轨 $L_h = \alpha\cos(\mathrm{lat})$（式 2），其中 $\alpha = \sqrt2 R\sqrt{1-\cos(360^\circ/(2N))}$ —— **异轨长度随纬度余弦变化**，这是全文所有几何推导的根源。
- **极区行为（L51）**：异轨 ISL **只在极区之外工作**——卫星接近极区时异轨 ISL 变短，跨越极点时相邻面的两颗星**交换位置**，所以异轨 ISL **在极区内关闭、在极区外重建**。
- **缝（seam）**：反向旋转的卫星边界（L49）。

**(B) 决策图（§III-B）——纯几何解析，无搜索**
- 定义 3 **初始对齐**：缝两侧的卫星处于同一纬度，此时所有异轨 ISL 平行于赤道。
- 定义 4 **水平环**：同一纬度上的卫星及其之间的 ISL 构成一个水平环。
- **Lemma 1（L126-L143）**：设源 $S_0$ 纬度高于目的 $S_n$，则最小传播时延路径**必经**"与源同一水平环、与目的同一轨道面"的那颗卫星——**同半球时是 $\langle p_{S_n}, s_{S_0}\rangle$，异半球时是 $\langle p_{S_n}, N-1-s_{S_0}\rangle$**。**推论（L143）**：所有源-目的对都必经这样一颗卫星，而从它到目的**只剩垂直跳**。
- **Lemma 2（L145-L147）**：不穿越极区时，水平跳应尽量在**纬度更高（靠近极区）的环**上做，因为异轨 ISL 在那里更短；垂直跳的长度在两方案中相同。
- **Theorem 1（式 6, L157）**：给出**"是否应该穿越极区"**的判据——水平跳数 $n_h$ 大于某个关于 $\cos(\mathrm{lat}_{min})$、$L_v/\alpha$ 与候选环纬度 $\mathrm{lat}+a\frac{360^\circ}{M}$ 的阈值函数时，跨界更优。
- **Theorem 2（式 8, L175）**：给出**"留在源所在环还是升到更高环"**的判据。
- **决策图（Fig 6, L186, L267）**：横轴是当前卫星纬度，纵轴是剩余水平跳数，**实线上方 = 满足式 (6)（应穿极区），虚线下方的区域 = 满足式 (8)（留在本环）**。**"The decision map of a satellite network can be stored on-board of each satellite since it does not change throughout the lifetime of the network."**（L267）—— **一次算好，终身不变，无需任何表更新**。

**(C) 三阶段逐包决策（§III-C）**
1. **方向估计（Direction Estimation, L197）**：**先假设所有 ISL 等长**，此时最小时延路径 = 最小跳数路径。用逻辑位置算最小跳数度量——一对方向指示 $d_v, d_h \in \{-1,0,+1\}$ 和一对跳数 $n_v \in \{0..M\}, n_h \in \{0..N\}$。分"同缝侧/异缝侧"两情形，用 **Table I（走 $P^H$，不穿极区）** 与 **Table II（走 $P^V$，穿极区）** 查方向。
2. **方向增强（Direction Enhancement, L253）**：**承认异轨 ISL 长度不同**（式 2），把第一步的方向标为 **primary/secondary**。规则（L255-L265）：(1) 当前星在极区 → 下一步必须同轨，$d_v$ 为主、$d_h$ 置零；(2) 当前星在极区前最后一个水平环 → 优先水平跳（那里异轨 ISL 最短）；(3) 其他位置按式 (6)(8) 判断——满足 (6) 则 $d_v$ 为主（保证水平跳在最小环上做），否则 $d_v$ 指向更高纬度，**其余情形比较源与目的纬度，高者优先水平跳**。
   **作者强调（L251）**："**Taking the horizontal and vertical hops in any combination would produce a minimum-hop path.** In fact, the ISLs have different lengths and the packets can be routed on $P^*$ only if they are taken in a specific order." —— **即前两阶段的差别正是"跳的顺序"**；**未被选为 primary 的其他最小跳数路径被留作拥塞/故障时的备份**。
3. **拥塞避免（Congestion Avoidance, §III-C3）——本课题的关键之处**
   - **前提（L269）**："**In the datagram routing algorithm, the satellites do not exchange traffic load information.**" —— **完全不做负载信息交换**。
   - **检测方式（L271）**：**只看自己输出缓冲区的填充水平**。若主方向的输出缓冲**超过 $\xi$ 个包**，就判为拥塞。**主方向拥塞时就改走 secondary 方向**。
   - **五条规则（L273-L279）**：(1) 已到目的星 → 不转发，交给地面；(2) secondary 方向为零 → 无论缓冲多少都走 primary；(3) primary 缓冲 < ξ → 走 primary；(4) **primary ≥ ξ 且 secondary < ξ → 走 secondary；两条都 ≥ ξ → 仍然走 primary**（即**宁可排队也不乱走**）。
   - **结果（L281）**："As a result of this phase, the packets are routed on one of the minimum-hop paths." —— **拥塞绕行只在最小跳数路径集合内切换，不会走远路**。且**为保证无环，包永不发回上一跳**（除非当前星在极区）。
4. **卫星失效（L283-L295）**：不再以"减少排队"为首要目标，而是**优先不丢包**——把包**偏转到正交方向**绕开失效点。(1)-(5) 条规则，包括"极区内下一跳失效则只能发回上一跳"。**作者承认（L295）**："**it does not guarantee that the packets are routed on a minimum-hop path.**"

**(D) 复杂度（§III-D）**
- 常规最短路方法（Dijkstra $O(N^2)$、Bellman $O(N^3)$ 最坏 / $O(N\log N)$ 平均）在卫星网络里因为**链路长度持续变化且影响超过一半链路**而必须极频繁重算，**可扩展性成问题**（L299-L303）。
- **本文算法：与网络规模无关的常数级处理**——**实测每包下一跳决策耗时 5 μs**（Intel Pentium III 450 MHz，L305）。**存储复杂度**：决策图预嵌入路由代码，**不需要任何路由表空间**；而其他方法至少需要 $M^2\times N^2$ 的连接矩阵，可能还要 $M\times N$ 的路由表（L307）。

**4. 它声称的效果**（全部给定条件）
四组实验（L316-L322），星座统一为 **M=12 个轨道面 × 每面 N=24 颗星，面内与星间角距均 15.0°**，极区定义为 **75°–90°**（南北），第 22、23 号星位于 82.5°N 的极区内，**极区内异轨 ISL 假定断开**（L324）。前三组对**所有源-目的对**取平均（假设每对等概率）。
- **实验 I 路径最优性（§IV-A, Fig 9）**：与 **Bellman 最短路算法**对比。卫星偏离逻辑位置越远，平均百分比偏差越大，原因**是同环内异轨 ISL 长度偏离初始对齐时的值**（一半卫星向北、一半向南，ISL 距离不同）。**最坏情况下平均偏差 < 0.3%**（L339）。
- **实验 II 增强阶段的作用（§IV-B, Fig 10）**：**带增强阶段时最坏平均偏差 < 0.3%；只用方向估计阶段则平均偏差始终 > 8.1%**（L353）——作者据此说增强阶段"is an essential part of our algorithm"。
- **实验 III 卫星失效（§IV-C, Fig 11）**：失效卫星从赤道移向极点时，平均偏差**从 6.25% 降到 4.4%**；**当失效星位于最靠近极区的环时偏差升到 15%，位于极区内时 16%**（L362）。原因是极区/近极区的失效会导致包被发回进入极区的那颗星，而**异轨 ISL 在极区不工作**。作者仍称"These increases in the overall average propagation delay are still negligible."
- **实验 IV 典型时延（§IV-D, Fig 12）**：北美 → 中欧，卫星高度假定 **1375 km**。卫星运动四分之一周期内：
  - **Bellman 最短路：43.5 → 47.1 ms（实线）**；
  - **本文算法：43.5 → 48 ms（虚线）**；
  - **偏差最大 0.9 ms，约占总理时延的 2%**（L379）。
- **作者的核心论断（L377）**："**Therefore, propagation delay can be regarded as the dominant factor of delay in satellite networks.**"（前提是并行处理 + 高速传输使处理与传输时间变得很小）

**5. 实验条件**
- **星座**：M=12 面 × N=24 星 = **288 颗**，角距 15.0°，**极区 75°–90°**，极区内异轨 ISL 断开，**轨道高度 1375 km**（L324, L366）。
- **流量模型（L324）**："In the first three experiments, we computed the average values for **all possible source–destination pairs**. **We assume that each source–destination pair occurs with the same probability.**" —— **即源-目的对均匀随机，这是唯一涉及"负载"的设定**。
- **负载/到达率**：**全文没有注入任何流量，没有到达率、没有排队仿真、没有吞吐测量**。拥塞避免阶段**只有机制描述与规则，没有任何拥塞场景的实验结果**（实验 I–IV 中没有一项在拥塞下评估）。
- **对比基线**：**Bellman 最短路算法**（仅用于路径长度/时延对比，L333）；相关工作里讨论了 Darting [8] 与扩展 Bellman-Ford [9]。
- **评估方式**：**解析/数值对比为主**（用 Bellman 算出真最优，再算本文算法的百分比偏差），**不是包级仿真**（虽然摘要说 "performance of the algorithm is evaluated through simulations"，但正文实验是数值比较；处理时间 5 μs 是实测）。
- **训练与评估**：无训练。**没有任何学习方法**。

**6. 它自己承认的局限**（逐字引用）
- L295（卫星失效重路由）："This rerouting strategy finds alternative routes for packets that would normally pass through a failed satellite. **However, it does not guarantee that the packets are routed on a minimum-hop path.**"
- L269（拥塞避免的前提）："In the datagram routing algorithm, **the satellites do not exchange traffic load information.**"
- L339（偏差来源）："The main cause for the deviations is based on the changing lengths of the ISLs. The length of the interplane ISLs within the same horizontal ring deviates from its original value at the initial alignment because half of the satellites move to North and half of them to South."
- L362（极区失效最差）："the average deviation increases to 15%. Similarly, the average deviation is 16% when failure is inside the polar region."
- L27（对既有集中式方案的批评，也隐含本文的对照基准）："the performance of the existing path handovers depends heavily on the optimality of the initial path establishments."
- **未见自述**：论文**没有 Limitations 节，也没有未来工作节**（第 V 节 Conclusion 共 3 句）。**特别是：从未承认"拥塞避免阶段没有任何实验验证"这件事**——这是全文最大的未言明缺口。

**7. 它没做但看起来能做的地方（基于内容）**
1. **拥塞避免阶段有完整机制设计（L269-L281），但零实验验证**。这是最刺眼的空白：ξ 阈值取多少？主/备切换会不会引起震荡（oscillation）？**两条都拥塞时"仍然走 primary"（L279）会不会造成不公平？全部没测。**
2. **"propagation delay 是主导时延项"这个论断（L377）没有任何负载条件下的验证**。它成立的前提是"处理与传输时间很小"——而这恰好在**高负载下被排队时延推翻**。9KZDXPKC 后来的实测（排队把 RTT 推远超计算值）**直接否定了这条假设的普适性**。
3. **卫星失效只有"永久失效"模型**（L283-L295），没有失效持续时间的概念，更没有恢复。而现代 LEO 的 ISL 失效是**间歇性、可恢复**的（对比 AF674CSF/AIH4GK37 的 Poisson/Pareto 失效模型）。
4. **逻辑位置抽象在极区会失效**：极区内异轨 ISL 断开、卫星跨越极点交换位置（L51），决策图在极区附近的偏差升到 15-16%（L362）——**作者用"仍然可忽略"带过，但这是抽象本身的边界**。
5. **只测了 $M=12 \times N=24 = 288$ 颗星的单一星座配置**（L324），**没有做星座规模的敏感性分析**。而决策图的形状依赖 (M, N)，换个星座就要重算。
6. **没有跟任何 datagram 路由基线做端到端对比实验**——Darting 的对比数字是引用别人的（L29 引 [9]），不是自己跑的。
7. **"逻辑位置"与真实卫星的错位没有做误差传播分析**：偏差 <0.3% 是平均，**尾部（最坏源-目的对）没给**。

**8. 和同批其他篇的关系**
- **这是本批（乃至全库）的谱系起点**。它是 **ASER [3]** 的直系祖先，而 **ASER 又同时被 AF674CSF (LPIH) 和 AIH4GK37 (PBAR) 引用为对比基线**（AF674CSF 参考文献 [12] 在 L534；AIH4GK37 参考文献 [3] 在 L443）。**AF674CSF 的参考文献 [11]（L532）就是本文**（Ekici, Akyildiz, Bender, "A distributed routing algorithm for datagram traffic in LEO satellite networks", IEEE/ACM ToN 9(2):137-147, 2001）——**本批内确证引用**。
- **AIH4GK37 也引了本文**（其参考文献 [15]，L467，同一标题）——**本批内第二处确证引用**。
- **"逻辑位置"这个抽象在本批其他篇里以变体形式延续**：LiR 的 **ISL 标识**（9GPFG5U3: 不给节点/接口命名，改给链路命名）、LPIH 的 **PID**（AF674CSF: 用逻辑路径标识代表一组物理 ISL）、DB-R 的**等价路径**——**这些都是"用逻辑抽象吸收物理动态"这同一个思想的现代版本**。本文是这条思想链的源头。
- **与 9GPFG5U3 (LiR) 的强烈呼应**：两者都强调 LEO 的**确定性邻居关系**与**预计算**（本文的决策图"does not change throughout the lifetime of the network" L267；LiR 的 ISL 标识"predetermined and fixed when the constellation is deployed"）。**相隔二十余年，同一思路**。
- **与 AIH4GK37 (PBAR) 的环面网格同构**：本文的水平环 + 垂直轨道 = 网格（作者自己引 Manhattan Street Network [12]，L124），AIH4GK37 称之为 toroidal grid。**两者是同一个几何对象的两种用法**：本文用它做逐包几何决策，AIH4GK37 用它做区域划分的解析。
- **与 9KZDXPKC (DB-R) 的直接对立**：本文假定"传播时延主导"且不做任何拥塞控制；DB-R 整篇都在处理**排队与拥塞控制被拓扑事件误导**的问题。**DB-R 面对的病，正是本文假设不存在的那部分现实。**
- **与 S85KQ4FC 的对照**：本文的星上决策是 **5 μs**（Pentium III 时代！），而 S85KQ4FC 的 DNN 逐包推理在网络级会造成 17.5 ms 决策时延。**S85KQ4FC 想解决的问题，正是本文这种几何/查表式方案所不需要的**——SS85KQ4FC 用流级复用来逼近本文的常数级开销。**这两篇串起来是一条完整的"决策成本"叙事线。**
*[回填位·已回填]* **它是本批的谱系起点，被两篇直接引用**：（a）**AF674CSF (LPIH)** 参考文献 [11] 即本文；（b）**AIH4GK37 (PBAR)** 参考文献 [15] 即本文。它也是 **ASER** 的直系祖先，而 ASER 同时是 AF674CSF（[12]）与 AIH4GK37（[3]）的对比基线——**一条 Hypatia → ASER → {LPIH, PBAR} 的完整引用链，源头是本文**。**与 9KZDXPKC (DB-R) 构成正面对立**：本文假设"传播时延是主导时延"（L377），DB-R 整篇在处理排队与拓扑事件对拥塞控制的误导；**与 AZ72LM9Z 对照**：本文的失效模型是永久性的，实测的是 50–75 秒量级可恢复的簇状中断。

**9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实**
**有间接但关键的两点贡献，但整体上是"假设掉"了这个问题：**
1. **拥塞避免机制是一个"只靠本地缓冲占用率、不交换负载信息"的负载响应方案**（L269-L271）。这是本批最早出现的**负载感知路由**雏形：用 $\xi$ 个包的输出缓冲阈值作为拥塞信号，主方向拥塞就走次方向。**它的意义在于证明"负载响应可以不做任何信令交换"**——这与 9KZDXPKC (DB-R) 的"默认路由 + 备份路由"、以及所有集中式 DRL 方案形成鲜明对照。**但它没有任何实验**，"ξ 应该取多少""负载升高时它到底有没有用"完全未知。
2. **"传播时延主导"这条假设（L377）明确地把排队时延排除在模型之外**。原文的前提是"processing and transmission times become very small"（L368, L377）——**这是在低负载、高处理速度假设下的结论**。作者的实测数字（Bellman 43.5–47.1 ms vs 本文 43.5–48 ms）**全部是无拥塞条件下的传播时延**，偏差最大 0.9 ms / 2%（L379）。
   **这条假设是本课题的反面靶子**：后来 DB-R 实测到"链路事件把 RTT 从 130 ms 推到 170 ms"（9KZDXPKC L130），以及队列把 RTT 推远超计算值——**都是本文假设之外的现象**。
3. **"所有源-目的对等概率"的均匀流量假设（L324）**是一种**空间均匀的到达率分布**，但**没有时间维度**——没有到达率大小、没有突发性。它解决的是"路径平均有多好"，不是"负载变化时路径会怎样"。
4. **一条可迁移的量化基线**：**每包下一跳决策 5 μs**（L305）。这是"几何/查表式路由"的星上开销基准；任何声称"星上智能路由可行"的方案，都应该跟这个数字对齐——S85KQ4FC 的 17.5 ms 是它的 **3500 倍**。

**10. 一句话评价**
**LEO 路由的奠基之作**：用"逻辑位置"把连续运动坍缩成静态图、用"决策图 + 三阶段逐包决策"把路由复杂度压到与网络规模无关的常数级（5 μs），此后二十余年的 LEO 路由工作（ASER、LiR、LPIH、PBAR）**无一例外都在它的框架里或针对它的盲区展开**；**但它把排队时延整体假设掉了**——"传播时延主导"这条论断成立的前提（低负载 + 快处理）恰好在高负载下崩塌，而它设计的拥塞避免机制**从未被实验验证过**，这是它留给后人最大的一块空地。

## AZ72LM9Z — Towards Global Outage Detection for LEO Networks (LEO-Net '25, UCLA)

**1. 一句话**
把已有的 HitchHiking 测量法**从"逐客户探测"改成"按共享前卫星路由器去重"**（罗马大道的思路：多条路通向同一个罗马），把测量引发的丢包从 **73.4% 压到 0.01% 以下**，从而第一次能**全球、近实时、秒级**地测 Starlink 的客户级中断——然后发现**中断是大规模同时发生的簇**，不是独立随机事件。

**2. 问题设定**
LEO 用户持续遭遇**频繁、短时**的中断，其性质与地面网不同（L37）：来源包括**卫星移动、天线遮挡、地磁风暴**（L37）。而**至今没有任何系统化的全球办法**研究 LEO 中断，因为这类分析需要**广地理尺度上近实时的高分辨率数据**（L46）。
**传统中断检测系统不适用（L48）**：它们针对**大规模、长时**中断（IODA 探 /24 块每 10 分钟、Hubble 看 15 分钟以上的可达性问题、Trinocular 11 分钟粒度、Cloudflare Radar/ThousandEyes 10–15 分钟），**而 LEO 的中断时间尺度是秒级**。
已有 HitchHiking 方法 [13] 能测 Starlink 客户时延，**但作者实验证明它无法扩展到"全球同时"的中断采集**——"naively running HitchHiking leads to massive packet loss"（L48）。

**3. 方法骨架**

**(A) 基础方法 HitchHiking（§2）**
- **中断定义（L61，本文采用比 Starlink SLA 更窄的定义）**：SLA 定义是"无法向 Starlink PoP 的服务器收发 ping"；**本文定义为"Starlink 客户对其前卫星跳路由器无响应"的那段时间**——即**聚焦卫星链路这一段**。
- **测量原理（L63, Fig 1）**：先用 **ICMP Paris traceroute** 找到**前卫星跳（pre-satellite hop）**，再用 **TTL 受限的 ping** 分别打前卫星跳和客户天线，两者的时延差即估计**卫星链路时延**。
- **中断判定（L65）**：**前卫星跳有响应、但客户端点无响应 → 判定为一次中断**。作者声明这是"outside-in"单向测量，**无法区分客户是发不出还是收不到**；并论证持续性的过滤策略不太可能解释这个现象（因为客户在中断前后都响应探测）。
- **四类测量结果（附录 A.3, L257-L263）**：**Success**（两者都可达）、**Outage**（前跳可达、端点不可达）、**Loss**（两者都不可达，即测量路径完全失效）、**Pre-satellite failure**（端点可达、前跳不可达）。

**(B) 朴素方法的失败（§3.1）**
- 朴素做法：对**每个暴露的服务路由器和其对应的地面路由器同时发 TTL ping**。要在 60 秒窗口内以 1 秒间隔测所有客户，就**每秒给每个客户服务和其前卫星跳各发一次探测**（L73）。
- **结果（Fig 2, L73）**：从 Stanford 于 2025-05-20 实测，**朴素 HitchHiking 导致前卫星跳处超过 50% 的丢包，且与探测的端点数无关**。原因**不是客户丢包，而是路由器对 ICMP 响应做限速以防 DoS**。
- **Fig 3（L82）**：按 /24 子网分区并在其中抽样，**探测超过 4 个客户后丢包显著上升**。

**(C) Roman-HitchHiking 的核心洞见与设计（§3.2）**
- **核心洞见（L86）**："**Many exposed customer services converge on the same pre-satellite hop router—in the worst case, up to 288 customers share a router in our experiment.**" —— **路径冗余**。既然"所有路都通向罗马"，**只要在某一刻从一条路径能（或不能）到达前卫星跳，就有很高概率从其他路径也一样**。
- **设计（L88）**：**对每个暴露端点各发一次 TTL ping（不省），但对每个唯一的前卫星跳路由器只发一次 TTL ping（去重）**。
- **第二条设计（L90）**：**把探测分散到多个源 IP**（本文用 **8 个**），因为过滤常按源 IP 触发（引 [29]）。

**(D) 测量有效性的三重验证（§3.3）**
1. **规模与丢包（Fig 4, L98）**：朴素设置丢包可达 **79.7%**；Roman-HitchHiking 压到 **0.01%**（四个数量级改善）。
2. **源 IP 多样性的作用（L100）**：**仅去重只能把丢包降 1.93 倍**，单源 IP 时仍有 **37.9%** 丢包（多为"两者都不响应"的完全丢失）；**用满 8 个源 IP 后降到 0.01%**。
3. **准确性保持（L107-L117）**：三种配置（Naive n=4 / Roman n=4 / Roman Large n=8），每端点每秒探一次、持续 5 分钟。
   - **案例研究（Fig 5, L113）**：三种配置探测同一客户，**检测到完全相同的三段时间中断**（[23,54]、[173,177]、[240,274]）。
   - **统计一致性（L115）**：在 1092 个重叠客户上，**Naive 与 Roman Large 的 Jaccard 相似度：5 秒中断 0.85、15 秒中断 0.88**；两个不同源 IP 的两个 vantage point，在 1265 个重叠客户上 **Jaccard 均为 0.88**。
   - **假阳/假阴的直接检验（L117）**：分析朴素配置里并发发出的前卫星跳探测，**没有发现任何一例"同一前卫星跳沿一条地面路径可达、沿另一条不可达"**——这直接支撑了去重不引入偏差的做法。

**4. 它声称的效果**（全部给定条件）
- **测量开销**：丢包 **73.4%（既有方法）→ <0.01%**（摘要 L52；正文不同实验点给到 79.7% → 0.01%，L98），**"enabling over four orders of magnitude greater coverage for simultaneously measuring customer outages"**（L52）。
- **数据规模（§4 Dataset, L134）**：Roman-HitchHiking + 8 个源 IP，5 分钟采样、1 秒间隔，**三个不同日期（2025 年 5 月 27–29 日）**。地理定位用 Starlink 公开的 IP Geolocation feed。过滤掉无成功 Paris traceroute 的端点、以及丢包超过均值 2 个标准差的端点后，**每天剩 14 436 – 15 068 个可测端点，分布在 98–101 个国家**（占 Starlink 有客户国家的 63.64–65.58%）。
- **中断频次（L136）**：**超过 5 秒的中断事件：5/27 有 812 次、5/28 有 344 次、5/29 有 574 次**。
- **中断时长分布（Fig 6, L136）**：**大多数中断短于 60 秒**，但**很多落在 50–75 秒区间**——"long enough to affect applications like video calls or gaming"。5/27 与 5/29 在约 55 秒和 75 秒处有大幅累积跳变，归因于国家级中断事件。
- **最重要的发现：中断是成簇同时发生的（L141）**：
  - **5/27：597 次中断同时发生，每次持续 70–75 秒——占当天全部中断的 73.5%**。
  - **5/29：观察到两簇，分别持续 50–55 秒与 70–75 秒，且两簇在时间上重叠**。
  - 作者判断："**These events suggest centralized failures, likely at the satellite link level, that affect many users at once.**"
- **地理分布（L149）**：5/27 事件影响智利 64%、阿根廷 10%、澳大利亚 18% 的受影响用户；5/29 的 50–55 秒中断影响墨西哥 38% 的用户，70–75 秒中断的 34% 发生在弗吉尼亚。**这种全球散布使得"本地地面条件"不太可能是原因**。
- **区域不平等（L151）**：**澳大利亚在每一个测量样本中都是受影响最严重的国家之一**（无论次数还是时长）；其他高影响区包括智利、阿根廷、所罗门群岛、汤加——指向**南半球的覆盖缺口或切换效率问题**。用 **95% 置信度的 z 检验**：5/27 智利/阿根廷/澳大利亚显著偏高，5/28 意大利/秘鲁，5/29 澳大利亚/墨西哥。**结论：中断风险在网络中分布不均。**

**5. 实验条件**
- **被测网络**：**Starlink**（最大的 LEO 提供商，L52）。
- **数据来源**：用 **Censys** 找暴露的 Starlink 服务，过滤出客户端点并**排除使用 PEP（性能增强代理）的端点**；用 **Scamper** 跑 Paris traceroute 确定前卫星跳（L96）。地理定位用 **Starlink 官方 GeoIP feed**（L134）。
- **探测方式**：TTL 受限 ICMP ping，**每秒一次**，持续 **5 分钟**（§3.3）/ **60 秒窗口**（§3.1 朴素对比）。**8 个源 IP**。
- **中断判定阈值（L109）**：聚焦 **>5 秒**与 **>15 秒**两类。选 5 秒是因为**这是 Starlink 手机 App 能分类的最大中断长度（0.1s+ / 2s+ / 5s+）**；选 15 秒是因为**已有工作表明 Starlink 有一个 15 秒的重配置周期 [20]**——**"If an outage persists for more than 15 seconds, it suggests that even satellite handovers failed to resolve the issue."**
- **判定一致性规则（L109）**：只要时间段有重叠就算所有配置都检测到；只在某一方法中出现且超过所评估时长（5s+/15s+）的中断，算作**该方法特有的检测**。**排除丢包率超过均值 2 个标准差的端点**。
- **对比基线**：Naive HitchHiking（每 /24 探 4 个，这是丢包飙升前的最大规模）；另有单源 IP 版本。
- **训练与评估**：无训练。**这是纯测量论文。**

**6. 它自己承认的局限**（逐字引用）
这篇的诚实度很高，把最大的短板单列一段：
- **L119（ground truth 缺失，全文最关键的局限）**："**Obtaining ground truth for Starlink outages is challenging due to the scarcity of public measurement data, limited access to community-operated vantage points, and the absence of our own hardware deployment.**" 并逐条排除替代方案：**RIPE Atlas** 粒度太粗，抓不到亚分钟级瞬态；**LEOScope** 当时只有 3 个节点活跃、且都不暴露公网 IP，无法从"outside-in"视角验证"inside-out"中断；**现有中断检测平台**只报持续性宏观中断。结论：**"As a result, direct validation remains an open challenge."**
- **L65（单向测量的信息损失）**："since we are only conducting one-way measurements from the 'outside-in,' an unresponsive client can indicate that they are unable to send or receive pings from our server, **but we cannot distinguish between the two**."
- **L48/L73（被测对象的行为不可控）**：丢包"**likely due to routers rate-limiting ICMP responses to prevent denial-of-service attacks**"——即**测量结果的瓶颈可能是被测网络的防护策略，而非网络本身**。
- **L121（伦理与足迹）**：作者专门声明遵守 [13][9] 的最佳实践，scanner IP 会重定向到说明页并提供 opt-out，**且强调 Roman-HitchHiking 发送的包比先前方法更少、足迹更小**。

**7. 它没做但看起来能做的地方（基于内容）**
1. **ground truth 完全缺失**（L119），作者自己也说这是开放挑战。**自己部署一台 Starlink 终端做对照**是它在未来工作里明确承诺的（L119），**但没做**。
2. **只有 3 天数据（5/27–29）**，且**每天只是 5 分钟采样**（L134）。**中断的日间/季节性规律、与地磁活动的相关性**都无法从这么短的窗口里得出——而作者在引言里恰恰把**地磁风暴**列为中断三大来源之一（L37）。
3. **没有把测量结果与任何网络状态量做关联**：57 秒/75 秒的簇状中断被归因为"centralized failures, likely at the satellite link level"（L141），**但这只是推测**——没有卫星轨道数据、没有 Starlink 的状态公告、没有 BGP 数据做交叉验证。
4. **"前卫星跳"的粒度**：去重后每个唯一前卫星跳只探一次，**那么"一个前卫星跳挂了"会同时标记所有汇聚到它的客户为中断**（最坏 288 个，L86）。**作者验证了"可达性一致"（L117），但没有验证"不可达性一致"在同一时刻是否也成立**——即**共享前跳是否会把局部故障放大成簇状假象**。这直接关系到第 4 节"簇状中断"结论的解释力。
5. **只测 Starlink 一家**（L52），且依赖 Censys 暴露的服务与公网 IP。**不暴露服务的客户、使用 CGNAT 的客户完全不在样本里**。
6. **15 秒阈值的依据来自别人的工作**（[20]，L109），本文没有独立验证 Starlink 的重配置周期。

**8. 和同批其他篇的关系**
- **与 AIH4GK37 (PBAR) 是同一课题组的姊妹篇**：作者群高度重叠——**Lixia Zhang、Liz Izhikevich、Sirapop Theeranantachai、Beichuan Zhang** 全部同时出现在两篇上（AIH4GK37 L3 vs 本文 L3-L17）。**AIH4GK37 是"设计侧"（怎么切区域），本篇是"测量侧"（真实网络到底有多差）**，UCLA 组在做"测量 → 建模 → 设计"的完整闭环。
- **明确引用了 8AYW2Y78 (Hypatia)**：参考文献 [24]（L217）即 Kassing et al. Hypatia，**归在"LEO 测量系统"这一类里**（L159：community-driven platforms、research testbeds and simulations（LEOScope、**Hypatia**、StarryNet）、industry tools）。**这是本批内第四条确证的 Hypatia 引用**，而且**用法最独特——把 Hypatia 归为"测量/仿真手段"而非"问题陈述者"**。
- **⭐ 对本批其他论文的假设构成直接经验反驳（最重要的关系）**：
  - **AF674CSF (LPIH)** 用 **Poisson 过程**生成 ISL 失效事件，理由是"it aligns with the assumption that **link failures in satellite networks occur randomly and independently**"（AF674CSF L305）。
  - **AIH4GK37 (PBAR)** 更进一步，明确假设"**at most one ISL down at a time to isolate individual disruptions**"（AIH4GK37 L298），失效时长用单一 Pareto 分布（k=2.5, $x_m$=7.2 s, 均值 12 s）。
  - **而本篇的实测结果直接打脸这两条假设**：**5/27 有 597 次中断同时发生、持续 70–75 秒、占当天全部中断的 73.5%**（L141），且跨智利/阿根廷/澳大利亚/巴西/意大利/墨西哥/日本等**地理上远离的区域**（L144, L149）。**残差：中断不是独立随机的，而是高度成簇的；"同一时刻至多一条链路失效"在真实网络里显然不成立。**
  - **同时，本篇的中断时长分布也与 Pareto 假设不符**：实测"大多数中断短于 60 秒，但很多落在 50–75 秒区间"（L136）——**分布有明确的众数区间，而不是重尾**。
  - **这是本批内最有价值的一条跨篇发现**：**三篇论文同批出现，其中两篇的仿真事件模型被第三篇的实测数据证伪。**
- **与 9KZDXPKC (DB-R) 的呼应**：DB-R 关心的正是"链路事件导致的丢包与 RTT 突变"，而本篇给出的是**真实网络里这类事件的规模与持续时间**（50–75 秒量级，远长于 DB-R 实验里配置的 5 秒 ISL 失效，DB-R L248）。**DB-R 的 5 秒事件参数明显偏乐观。**
- **与 AJJI57M9 (Ekici)**：祖师爷假定"传播时延主导、卫星失效是永久性的"；本篇实测到的是**持续数十秒但会恢复的间歇性中断**，并且**存在 15 秒的重配置周期**（L109）——**这正是 Ekici 那篇没有的"时间维度"**。
*[回填位·已回填 — 本批全部读完]* **⭐ 本篇是本批最有价值的"证伪者"**：它用实测数据反驳了同批两篇仿真论文的事件模型假设——**AF674CSF (LPIH)** 假设 ISL 失效是"randomly and independently"的 Poisson 过程（AF674CSF L305），**AIH4GK37 (PBAR)** 明确假设"at most one ISL down at a time"（AIH4GK37 L298）；而本篇实测到 **5/27 有 597 次中断同时发生、占当天 73.5%、持续 70–75 秒、跨智利/阿根廷/澳大利亚/巴西/意大利/墨西哥/日本**（L141, L144）。**同时，它引用了 8AYW2Y78 (Hypatia)**（参考文献 [24]，归入"LEO 测量/仿真系统"类），且**与 AIH4GK37 是同一 UCLA 课题组的姊妹篇**。

**9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实**
**它测的不是负载，而是"可达性随时间的变化"——但这恰好是本课题最缺的那类真实数据**，且贡献具体：
1. **给出了真实网络里"链路不可用"的持续时长分布**：**大多数中断 <60 秒，大量集中在 50–75 秒**（L136）；单日 >5 秒的中断次数在 **344–812 次**量级（L136）。**任何"负载变化下的到达率/时延"模型，都需要一个链路可用性的时间常数——这篇提供了实测值。**
2. **⭐ 中断是成簇的同时事件，不是独立随机事件**：5/27 的 **597 次同时中断占当天 73.5%**（L141）。**这意味着：把链路失效建成独立 Poisson 过程（AF674CSF L305）会系统性低估"同时多链路失效"的概率，从而低估拥塞与丢包的尾部。** 对"负载突变"这个议题而言，**成簇失效会在同一时刻把大量流量挤到剩余链路上，这正是负载突变的物理来源之一**。
3. **区域不均衡（L151）**：澳大利亚在**每一个**样本里都是最严重的国家之一，南半球（智利、阿根廷、所罗门群岛、汤加）系统性偏高（95% z 检验显著）。**即"到达率/时延"的分布在地理上是不均匀的，不能用均匀随机的源-目的对假设**——而本批多篇仿真论文恰恰用了均匀假设（AJJI57M9 L324 的"每对等概率"、AIH4GK37 的 10 万个均匀随机源-目的对 L400）。
4. **一个可直接用作参数的量**：**Starlink 的重配置周期约 15 秒**（L109 引 [20]）——超过 15 秒的中断意味着**连星间切换都救不回来**。这是"系统从扰动中恢复"的时间尺度基准。
5. **一条方法学警告**：**QoS 测量本身会因被测网络的 ICMP 限速而失真**（朴素方法丢包 50–79.7%，L73/L98）——**任何"测时延/丢包随负载变化"的实验，都必须先排除"测量强度本身触发了限速"这一混杂因素**。这与会期内 AF674CSF L437 的"只统计成功包"警告是同一类陷阱的两个侧面。

**10. 一句话评价**
**一篇"测量先行"的短文，方法学贡献比结论更硬**（用自己的路由器去重 + 多源 IP 把测量丢包压掉四个数量级，并用 Jaccard 0.85–0.88 与"同一前跳跨路径可达性一致"证明去重不失真）；**它的实测结论对本批两篇路由论文的仿真假设构成直接反驳**——真实 LEO 中断是**成簇、跨区域、50–75 秒量级**的，而非 AF674CSF 假设的独立 Poisson、也非 AIH4GK37 假设的"同一时刻至多一条链路失效"；**唯一的硬伤是 ground truth 缺位**（作者自己承认且列全了为什么替代方案都不可行），所以"597 次同时中断"这个数字的解释仍需谨慎——它也可能部分来自共享前卫星跳的放大效应，而这一点论文没有排除。
