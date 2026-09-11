# 读卡批次 R10

> 读法：逐字通读 VM MinerU MD 全文，行号对应 /data/liguang13/topic-loop-r2/md/<KEY>/<KEY>/txt/<KEY>.md。
> 批次：X2FCSU4S X5K285MW X5Z98UPM XLRW7XXN XM64YRAW XM6NUPM4 Y2H4NPLU YD4JUT7G YI9G7NR7 Z74SR656 ZIUBKVPZ（11 篇）
> 每篇读完即时写卡；批次内交叉关系记在第 8 项（写卡时点只引已读篇目 + 原文参考文献），批次末另有交叉索引。

## X2FCSU4S — Load Balancing Based on Cache Resource Allocation in Satellite Networks

**1. 一句话**
把 GEO 卫星的剩余缓存当成"商品"，用 Stackelberg 博弈向 LEO 卫星定价出售；LEO 用 Martingale 包络自己估计 backlog（队列积压）来决定买多少空间，把拥塞的 LEO 内容"卸载"到 GEO——本质是缓存资源分配/定价，不是路由算法。

**2. 问题设定**
LEO 高速移动、星地连接间歇，队列变长、缓存溢出丢包（L15 摘要逐字："During a high-speed movement, the satellites are connected intermittently, so the queue length becomes larger and a cache overflow appears"）。物理事实是 GEO 体积/缓存远大于 LEO，所以 LEO 拥塞概率大、GEO 常有空闲缓存（L63）。麻烦在于 GEO 存储有限而多个 LEO **非合作**竞争：谁定价、谁买多少、买不起的节点出局（L23、L260）。参与者是 1 个 GEO（leader）+ K 个 LEO（followers），GEO 必须先满足自身需求，剩余空间才出租（L264）。

**3. 方法骨架**（非 RL：信道建模 + Martingale 界 + 博弈 + 凸优化 + 三个算法）
- 信道：下行 Gilbert-Elliott 两态马尔可夫（式 2），good 态速率式 3，Nakagami-m 阴影 pdf 式 4；上行是 S-ALOHA 接入与 GE 的级联，用指示函数 $\mathrm{I}(T)=1$ 表示接入成功（式 6），状态转移矩阵式 7、速率式 8（L110–128）。表 2 给重/轻两套阴影参数（L246）。
- 到达/服务：把到达拆成高优先级 $A^h$、低优先级 $A^f$（SP 调度），Lemma 1（式 9）证明到达过程是超鞅，Corollary 1（式 10）把等效服务过程也建成超鞅（L139–157）。思想是"级联"：用户数据生成 → 信道接入 → GE 信道服务，整体当作缓存的到达过程（L149）。
- backlog 估计：Theorem 1（式 12）给时延上界违反概率 $p(W(T)>\kappa)\le\frac{E(M_{A^t}(0))E(M_S(0))}{H}e^{-\theta_1^*\kappa\kappa_{ss}}$，式 13 是 $\theta_1^*$ 的可行集；FIFO 版式 14–16、SP 版式 17–19，最终得到 $\sigma_{FIFO,L}$、$\sigma_{SP,L}$（L203–241）。
- 内容热度：Zipf 式 11，$s\in[0,1]$ 控制偏斜度（L159–169）。
- 博弈：GEO 收益式 20、Problem 1（式 21，约束 $\sum s(q_{L_k})\le h(\sigma_G)$ 即 GEO 剩余空间）；**Congestion Index** 式 22 $I(q_{L_k})=\ln(1+\frac{q_{L_k}\sigma_{L_k}}{\sum_{j\neq k}q_{L_j}\sigma_{L_j}})$——作者自述是照抄香农公式的"信干比"结构（L284）；LEO 收益式 23 $R_{LEO}=c f(\sigma_{L_k})I(q_{L_k})-\eta_{L_k}s(q_{L_k})$，即"收益 − 买空间的钱"。
- 求解：Lemma 2 式 28 给最优购买比例 $q^{*}_{L_k}=(\frac{c f(\sigma_{L_k})}{\sigma_{L_k}\eta_{L_k}}-y_{L_k})^{+}$；Problem 3 非凸，作者**假设所有节点都参与**从而转成凸的 Problem 4（L352）；Theorem 2 式 33 给 $\eta^{*}$，Theorem 3 式 34 给参与博弈所需的最小剩余空间，Theorem 4 证明阈值 $x_{L_K}$ 对 K 严格单调递增，Theorem 5 / 式 36 给分段最优价。
- 算法：Algorithm 1 *Members of a Game*（按 $\sqrt{f/y}$ 排序，逐个剔除到 $x_{LU}<h(\sigma_G)$，决定参与人数，L398–418）；Algorithm 2 *Distributed Cache Price Bargaining*（按 $\sum q$ 与 $h(\sigma_G)$ 之差调价 $\pm\Delta\eta$，直到 $|\sum q-h(\sigma_G)|<\zeta$，L424–444）；Algorithm 3 *Popularity Matching*（把**不受欢迎**的内容传上 GEO，因为缓存成本与热度成反比，L484、L492–506）。
- 均匀定价对照：式 37–41，结论 "uniform pricing scheme is inferior to the nonuniform pricing scheme"（L480）。

**4. 它声称的效果**
- Fig 5（L199–201）：Martingale 时延界 vs $10^6$ 次内容仿真的箱线图，作者判 "the delay bound ... is quite tight"——参数固定为 $\lambda_f=0.6,\ p_m=0.1,\ R_{su}=1$。
- Fig 6 / Fig 7（L248–256）：违反概率随 backlog 增大而下降；重阴影下行比轻阴影更易积压；SP 当高优先级服务 $A^h(T)=0.5T$（仿射）时，违反概率偏离无优先级情形。
- Fig 11（L513）：上传价格随 GEO 剩余空间 $h(\sigma_G)$ 增大而下降，$L_3$ 最便宜、$L_1$ 最贵。
- Fig 12（L515）：$h(\sigma_G)$ 越大能容纳进博弈的 LEO 越多；非均匀价优于均匀价；$s=0.1$（近均匀）比 $s=0.8$（偏斜）能容纳更多 LEO。
- Fig 13（L532）：丢包率对比，**基线是 DSR（最短路）与 TOTD（文中指文献 [1] Nishiyama 的方法）**，本文最低；作者归因 DSR 造成节点流量不均衡、TOTD 只考虑传播时延且阈值强依赖信道条件。

**5. 实验条件**
网络规模：STK 生成 Iridium-like 星座，66 颗 LEO / 6 个轨道面，外加 3 颗 GEO（L490）；但实际数值分析**只取被 satellite111 长期覆盖的 6 颗 LEO + 1 颗 GEO 共 7 颗星**（L511）。参数：表 2 重/轻阴影；$\lambda_f=0.6$、$p_m=0.1$、$R_{su}=1$；Zipf $s=0.1/0.8$。非 RL，无训练/评估之分，也无独立验证集。**没有到达率扫描**，没有网络级端到端时延仿真。

**6. 它自己承认的局限**
- L77 脚注 1 逐字："Since this work mainly analyzes the load balancing of satellite data streams, we do not consider the overlap of coverage, which is beyond the scope of our analysis."
- L352 逐字（关键松弛）："Note that the above problem is a non-convex problem. Then, we assume that all nodes participate in the game so that Problem 3 will be transferred into a convex problem without the limit of the indicator."
- L466、L478：两处证明直接省略（"The proof is similar to theorem Theorem 2." / "A detailed proof is omitted because it is similar to that of Theorem 5."）。
- 结论段（L536）**没有**任何局限自述（未见 limitation 小节）。另：全文未讨论把内容传上 GEO 所付的额外星间传播时延。

**7. 它没做但看起来能做的地方**（基于内容）
1. $\sigma_L$（LEO backlog）与 $h(\sigma_G)$（GEO 剩余空间）在每次博弈里是**静态输入**，而摘要自己说 LEO "connected intermittently"（L15）；没有把时变可见性/时变 backlog 做成滚动博弈。
2. Theorem 4 证明 $x_{L_K}$ 对 K 严格单调递增 → 参与集合存在**阈值切换**：$h(\sigma_G)$ 轻微变化就可能让某个 LEO 突然出局（L342、L370–384）。阈值附近的震荡/不连续没有实验。
3. Martingale 上界的紧致性只在 $\lambda_f=0.6$ **单点**验证（Fig 5）。若负载升高使界变松，定价就建立在偏保守的 backlog 上——可直接测。
4. Fig 13 的 x 轴是"单用户数据速率"（服务侧），不是到达率；"丢包率 vs 负载"曲线缺失。
5. Algorithm 2 名为 "Distributed"，但每轮需要 GEO 广播 $\eta$、收集全部 LEO 的 $q$（L426–444），收敛轮数与信令开销未测。
6. 丢包只报总比例，未区分"缓存溢出丢包"与"信道接入失败丢包"（S-ALOHA 冲突本就会丢，式 6 已建模）。

**8. 和同批其他篇的关系**
（写卡时点 = 本批第 1 篇，尚无已读可比篇目。）原文参考文献里的相关锚点：TLR（Song et al., 文献 [2]）、TOTD（Nishiyama [1]）、MLSR（Akyildiz [9]）、LEO 缓存匹配博弈（Liu [30]）。后续篇目若有引用，将在批次末交叉索引汇总。

**9. 对"负载变化下到达率/时延"的贡献**
**给了理论骨架但没给实测曲线**。式 12/16/19 把到达率（$\kappa_h,\kappa_f$）、缓存服务率 $\kappa_s$、门限 $\kappa$ 与违反概率连在一个指数式里；Fig 6/7 显示违反概率随 backlog 阈值单调下降——是"到达率↑ ⇒ 溢出概率↑"的间接证据。但全文没有"时延 vs 到达率"或"丢包 vs 到达率"的扫描图，到达率在公式里是常数率，到达的突发性（自相关）未建模。直接贡献：**无**；间接贡献是一套可推导溢出概率上界的鞅工具链。

**10. 一句话评价**
把地面无线缓存的 Stackelberg 定价线（文献 [23] Hajimirsadeghi 等）整体搬到 GEO/LEO 多层卫星的"缓存卸载"上；数学包装（Martingale 包络 + 非凸转凸）很厚、工程直觉很薄——它把 LEO 拥塞问题等价替换成"向 GEO 买空间"的问题，而买来空间后内容走星间链路所付的传播/排队时延从未进目标函数，7 颗星的数值实验也撑不起 "load balancing" 这个标题。

## X5K285MW — Analyzing Source-Routed Approaches for Low Earth Orbit Satellite Constellation Networks（LEO-NET '23）

**1. 一句话**
不提出新路由算法，而是把"源路由（源节点算好整条路径塞进包头、逐跳弹出）"这条老办法在真实系统级仿真里做**消融**：把基于传播时延的 SPF 换成"最小跳集合内**逐流随机选路**"、把均匀 UT 分布换成人口密度分布，量出各改动的收益与代价。

**2. 问题设定**
源路由被广泛用作对比基准，但已被指有热点（hot spot）与链路负载感知昂贵两大毛病（L44 逐字："the decisions are made with limited information. So, in mesh networks with elevated traffic volumes, source-routed approaches are prone to hot spots"）。作者要回答的是：**在完全不用负载信息**的前提下，靠星座自带的路径多样性（path diversity）能榨出多少性能？以及源路由自身的代价（每跳额外操作、额外处理时延、信令开销）到底多大？（L34、L38）

**3. 方法骨架**（非 RL，纯系统级仿真对照实验）
- 参考系统（第 3 节）：Walker **star** 巨型星座 P-288，288 颗星（L51、L54）；每星 **4 条光 ISL** = 2 条同轨 + 2 条异轨（L48）；反向旋转面的缝（seam）处无 ISL；异轨 ISL 在 **±80° 纬度**关闭（L48）。
- 地面段：**2000 个 UT**（最低仰角 15°）+ **39 个 GW**（最低仰角 10°）（L54、L56）；UT 分布基于 GPWv4 人口密度并**下调了大城市/稠密区**权重，GW 分布是"非最优的、按现有互联网基础设施"（L56）。星地/星间切换假设为完全可预测、无缝（L56）。
- 源路由机制（第 4 节）：入星按周期性定时切换策略预计算路径，MPLS 式逐跳弹出（L62）；路径选择用 Dijkstra/SPF 或 SPT（L64）；**仿真里假设入星完全没有链路负载信息**（L62）。
- 路径选择的两个变体（第 4.1 节）：① 基于**传播时延**的最短路（SPF）；② 基于**最小跳数**度量 + **按流（flow-based）随机选一条**（逐流而非逐包，以压低抖动与乱序，L68）。作者给出可扩展方向：放宽最小跳约束、允许 "+2 跳或更多"，只要端到端时延仍满足 QoS 类（L70），并给出算例——P-288 同轨传播时延 ≈ **6 ms**，异轨最大 ≈ **8 ms**，所以额外时延上限可以按星座设计直接估出来（L70）。
- 因为 seam 与异轨关闭纬度导致距离度量难构造，A* 不好用，改用 BFS 枚举最小跳路径，在普通笔记本上毫秒级完成（L72）。
- 信令开销论证（第 4.2 节）：因为 ISL/ESL 连通性可预测，**根本不需要信令**，入星按时改包头即可（L78）。

**4. 它声称的效果**
- 负载锚点（用 Little 定律算的，和仿真实测吻合）：**70000 会话 ≈ 9.72 Gbps**，**120000 会话 ≈ 16.67 Gbps**（L92）。
- 均匀 UT 分布比人口密度分布能多承载 **约 64%** 流量（判据 QoS 合规率 > 95%）（L92）。
- 换用"最小跳 + 逐流随机选路"后，**约多承载 73%** 流量（QoS 合规 > 95%），且入星完全不用负载信息（L96）。
- 时延代价（Fig 5）：传播时延 SPF 平均 **53.66 ms**，增强方案平均 **60.23 ms**——增强方案慢但换来吞吐（L104）。
- 丢包成因二分解：① 出端口 buffer 满；② 包头里写的下一跳因切换已不存在（L92）。
- 处理代价量化：假设每跳每包处理 **50 µs**，即使 **20 跳**也只增加 **0.55 ms**；包头操作数与转发包数线性增长——**3.5×10^6 包 → 约 30.0×10^6 次额外操作 ≈ 每包 8.6 次标签操作**（L106）。
- 信令开销在所有测试中 **< 1%** 总流量（L106）。

**5. 实验条件**
自研 C++ 系统级逐包仿真器，是文献 [15]（作者自己的分布式 SDN 负载均衡工作）环境的扩展（L85）。表 2：仿真时长 **7200 s**，会话数 **[30k, 120k]**，平均会话时长 **100 s**，会话速率 **10 Mbps**（L81）。流量构成：**60% UT↔GW + 40% UT↔UT**（L86）。所有链路**恒定容量**，不考虑 TCP 等传输层影响（L58 逐字："As we want to analyze source-routed schemes in isolation, such influences are not considered in this work. All links are assumed to maintain a constant capacity."）。训练/评估之分不适用（非 RL）；"评估"就是单次长时间仿真。**注意**：Table 1、Table 2 在 MinerU 转换中列结构丢失（表 1 只剩数字串 "288 41224 760 86.4 30 15 7.5 80 1000 0.36 5000 5000"，表 2 的 "Session begin distribution" 一行串成 "uniform normal"），因此我**只**引用了这两段正文文字明确说出的参数。

**6. 它自己承认的局限**（第 5.1 节 "Discussion and Limitations"，L111–117）
- L117 逐字："In the proposed approach, load information is not used, leading to a path distribution that differs from active loadbalancing. Sharing all link load details for every possible entry satellite is considered too expensive given the unpredictable traffic characteristics and the network topology."
- L117 逐字："Comparisons to dedicated load-balancing schemes were omitted due to the scope of the investigation."
- L58 逐字（隔离假设）："As we want to analyze source-routed schemes in isolation, such influences are not considered in this work. All links are assumed to maintain a constant capacity."
- L115：只在 Walker **star** 上做，未在 Walker delta 上验证（虽然作者说方法两者通用）。

**7. 它没做但看起来能做的地方**（基于内容）
1. **QoS 合规率 > 95% 只作判据，没有给"合规率 vs 负载"的完整曲线数值**：文中只给"多承载 64% / 73%"两个相对数（L92、L96），没有绝对拐点负载、没有置信区间。原图的负载轴标度在 MD 里不可读。
2. 时延只报**平均**（53.66 / 60.23 ms），没有尾时延（p95/p99）。作者自己说增强方案"marginally less efficient"——但平均值差的 6.6 ms 是否会在尾部分布上放大，没测。
3. **60% UT↔GW 流量**被作者自己点名为潜在瓶颈来源，并说"取决于 ESL 连通性，路由可能无法避免出口瓶颈，需要额外 ESL 或更高速率"（L87）——即瓶颈从路由问题变成了地面段拓扑问题，而这正是本文实测"增强方案收益"的上限所在，却没有把 ESL 容量作为扫描变量。
4. 随机选路是**逐流**随机（L68），但没有做"随机 vs 轮询 vs 加权"或"随机种子敏感性"的对照；76% 的收益会不会只是单次采样的运气，无从判断。
5. 作者提出放宽最小跳约束（"+2 跳"）能进一步均衡负载（L70），但**仿真里没做这个变体**——这是现成可做的下一步。
6. 论文题目是"分析源路由"，但**唯一的基线是自己的另一个变体**，没有与任何自适应/负载感知方案对比（L117 承认是 scope 决定）。

**8. 和同批其他篇的关系**
与 **S85KQ4FC**（Enabling High-Throughput Routing…）：两者都把"源路由/最短路"当基准、都在 Iridium-like 或 Walker 星座上跑逐包仿真，但 S85KQ4FC 是 DRL 逐包决策（用负载状态），本文恰恰**刻意不用任何负载信息**——两篇构成"信息用量"光谱的两端。本文引用的 **Handley 2018《Delay is Not an Option》[10]**（L147）与 **Bhattacherjee & Singla CoNEXT'19 [2]**（L131）是 LEO 路由谱系的共同祖先，S85KQ4FC 的动机实验里也能看到同一血脉（星上算力/时延）。本文引用的 [15] Roth et al. 2022 分布式 SDN 负载均衡是它自己的上游工作。（本批其余篇目若有呼应，将在批次末索引汇总。）

**9. 对"负载变化下到达率/时延"的贡献**
**本批（截至第 2 篇）唯一一篇把"负载 → 性能"做成主轴的论文**，而且是系统级逐包仿真而非排队论推导。它给出的事实：
- 负载轴存在**明确的合规悬崖**，且悬崖位置强烈依赖**流量空间分布**（人口密度 vs 均匀 → 相差 64%）与**路径选择策略**（时延 SPF vs 最小跳随机 → 相差 73%）——同一个网络、同样的到达率，只换选路策略就能把可承载负载抬 73%。
- 给出"负载 ↔ 时延"的**权衡方向**：更均衡的选路用 +6.57 ms 平均时延（53.66 → 60.23 ms）换 +73% 负载。
- 澄清了失败机理：**丢包来自出端口 buffer 溢出 + 切换导致的下一跳失效**，而不是处理能力不足（处理每跳 50 µs，20 跳仅 0.55 ms）——对"星上算力是瓶颈"这一常见叙事给出了反证。
- 局限：到达率是**会话数驱动**（30k–120k，每会话恒定 10 Mbps），没有做流量突发性/自相似的扫描；没有把 ESL 容量纳入扫描，因此"瓶颈在星上还是在地面出口"无法分离。

**10. 一句话评价**
一篇**诚实的负结果式消融**：不发明算法，只证明"在 LEO 星座里，光靠最小跳集合内的逐流随机选路、零负载信息，就能比传播时延最短路多承载 73% 流量"，代价是平均时延 +6.6 ms——它把"负载均衡收益到底来自信息还是来自路径多样性"这个纠缠不清的问题切开了一半（切掉信息那一半），是评估任何 DRL/负载感知路由时最应该先跑的那个基线。

## X5Z98UPM — DRL-Based Load-Balancing Routing Scheme for 6G Space–Air–Ground Integrated Networks (Remote Sens. 2023, 15, 2801)

**1. 一句话**
在 Iridium 星座上做**逐跳 DQN 下一跳决策**（DQN-LLRA）：状态只含"四个邻居链路时延/带宽 + 邻居队列利用率 + 自己与邻居到目的的最短跳数"，奖励是四项加权和，卖点是在时延只涨一点点的情况下把路径的**最大/平均队列利用率**压下去。

**2. 问题设定**
LEO 星座拓扑高速变化、ISL 时延比地面长、多用户区链路状态变化更频繁（L38），所以地面路由协议不能直接用。具体痛点是**流量分布不均**：高低纬度卫星密度不同、用户分布不同（L40），最短路算法只按路径长度选路，导致**高纬度地区流量汇聚**（L78 逐字："The conventional shortest-path algorithm design for the routing paths only relies on the length of the path, which results in traffic aggregation when the latitude is high"）；地面关口站分布不均也会造成星上负载不均（L78）。作者用 NS3 画的 3D 流量图（Fig 3）显示拥塞主要出现在高纬度和人口稠密区（L78）。

**3. 方法骨架**（RL，DQN，每跳一个 agent）
- 星座：Iridium，6 个极轨×12 星 = **72 颗**（11 通信 + 1 备用）（L95）；每星最多 **4 条 ISL**（2 同轨 + 2 异轨），第 1 与第 6 轨道反向、二者之间无直连（L95）。拓扑建成无向图 $G=(V,E)$（L100）。
- 队列利用率定义式 1：$QU_i=\frac{\text{节点 }i\text{ 队列中当前包数}}{\text{节点 }i\text{ 总队列长度}}$（L102–104）。
- **状态**（L123）：$S_t^i=\{D_{ij},B_{ij},C_i,\hat{C}_j,QU_j,done\}$，$j=1..4$。其中 $D_{ij}$ 是到邻居 j 的 ISL 时延、$B_{ij}$ 是链路带宽、$C_i$ 是当前节点到目的的**最短跳数**、$C_j$ 是邻居到目的的最短跳数（用 **Dijkstra** 算），$QU_j$ 是邻居队列利用率，$done$ 是是否到达目的地的布尔量。作者说 $C_i,C_j$ 这一对是为了**加快收敛并避免乒乓路由**（L123）。
- **动作**（L125）：$a_i=\{\text{neighbor}_j\}, j=1,2,3,4$，四选一。
- **奖励**（式 2，L129–133）：四个分段分支，按 $C_i\le C_j$ 与否、$QU_j\le 0.5$ 与否分成 4 种情形，每支都是 $\alpha_k\frac{C_i-C_j}{p}+\beta_k(1-QU_j)+\gamma_k\frac{D_{ij}}{q}+\omega_k\frac{B_{ij}}{o}$，权重满足 $\alpha+\beta+\gamma+\omega=1$；$o,p,q$ 是量纲对齐因子。**这种"分段权重"是本文最独特的设计**：权重按当前情形切换（好决策奖励更高、坏决策罚更重）。到达目的地时式 3 给 $r_t=1$，累积回报式 4 是标准折扣和。
- **算法**：DQN 标准件——经验回放池、估计网 + 目标网（每 C 步复制参数）、MSE 损失式 6、目标值式 7（注意是 **max 目标**，非 double）、参数更新式 8。**探索率是自定的动态贪心**（式 5，L154–156）：以 $e^{-steps\cdot 0.4}$ 的概率随机，否则取 $\arg\max Q'$——随训练步数指数衰减，非标准 $\varepsilon$-greedy。
- Algorithm 1（训练伪码，L162–184）、Algorithm 2（决策伪码，L195–205）。

**4. 它声称的效果**
- 摘要（L15）：相比 Q-learning 基线，**最大队列利用率降 5%**、**平均队列利用率降 13%**。
- 正文（L292）另给一组：相比 **Dijkstra**，最大降 **8%**、平均降 **15%**；相比 Q-learning，最大降 **5%**、平均降 **13%**。
- 时延（Fig 12，L273）：四种算法里 **Dijkstra 时延最低**，**Dijkstra-QU 最高**（因为它只优化队列利用率、不管跳数和时延），DQN-LLRA 与 Q-learning 居中，**DQN-LLRA 优于 Q-learning**。
- 队列（Fig 13/14，L283、L288）：**Dijkstra-QU 的最大/平均队列利用率最低**，Dijkstra 最高，DQN-LLRA 与 Q-learning 居中，DQN-LLRA 低于 Q-learning。
- 关键叙事（L292）："The path obtained by the DQN-LLRA algorithm in this paper not only ensured a low delay but also responded effectively to the load situation"——即它自居"时延与负载的折中位置"。

**5. 实验条件**
Win11 64 位 + Python 3.9 + PyTorch（L251）。拓扑用官方 Iridium 卫星数据文件 + networkX 生成，6 轨道×12 星（L251）。**链路时延随机取 10–20 ms、带宽固定 10 Mbps**（表 1，L261）——不是按轨道几何算的真实时延。训练：**循环同时生成 70 条数据流**在拓扑里传播，以制造动态队列利用率（L251）；用 **10000 条随机生成的数据流**训练到收敛（L256）；网络是输入层+输出层+**两个隐藏层**（L256）；$\gamma=0.99$、回放池 4000、学习率 0.005（表 1）。评估：**生成 100 对源-目的节点，每种算法算 100 条路径，共 400 条**，做数学分析（L271）。基线四个：Dijkstra、Dijkstra-QU、Q-learning 方案（引 [45] Yin et al.）、本文 DQN-LLRA。
**注意一个刻意的公平性处理**（L269 逐字）："To simulate the overhead resulting from the agent–environment interaction in the machine learning algorithms, we decreased the bandwidth around the decision node in both the Q-Learning-based intelligent routing scheme and the proposed routing scheme. This promoted the fairness of the comparison with other benchmark algorithms."——即给两个 RL 方案人为降低决策节点周边带宽来模拟推理开销。这是本批目前**第二篇**主动把"智能体开销"计入对比的论文（第一篇是 S85KQ4FC，但 S85KQ4FC 是实测 CPU 标定，这里是"人为削减带宽"这种更粗的代理量）。
训练与评估**不是同一套**：训练用 10000 条随机流，评估用 100 对源目的节点，但文中未说明二者的负载是否一致。

**6. 它自己承认的局限**（第 6 节结尾，L296–298）
- L296 逐字："This paper also found that when the number of satellite nodes increased to thousands, the routing path exceeded 20 hops, and then the convergence speed of the DQN-LLRA algorithm decreased, and the accuracy of the decision model also decreased."（**规模扩展性退化**，并建议用 GNN。）
- L298 逐字："the proposed algorithm is evaluated through simulations, and it remains unclear how well it would perform in real-world scenarios."
- L298 逐字："Other factors, such as link reliability, congestion level, and energy efficiency, may also be considered in future work."
- L298 逐字："it is a computationally expensive approach that requires significant training time and resources."

**7. 它没做但看起来能做的地方**（基于内容）
1. **时延与队列利用率的权重是手工设定的 4 组 16 个数**（表 1），作者只说"主优化目标是跳数和队列利用率，所以前两项权重设大"（L133）。没有任何权重敏感性/消融实验，也没有自动调权。
2. **状态里没有下一跳决策队列/缓存占用**，只有邻居的 $QU_j$。S85KQ4FC 已经证明"决策队列"本身会爆——而本文为了"公平"反而人为降低了决策节点周边带宽（L269），等于把这个问题当作噪声消掉，而不是建模。
3. **$QU_j>0.5$ 这个硬阈值**被写死在奖励分段里（式 2），没有说明 0.5 的依据，也没扫过。
4. 链路时延**随机 10–20 ms**（表 1），而不是按轨道几何/纬度算——但论文的核心动机恰恰是"高纬度链路长度变化导致负载失衡"（L78）。用随机时延等于把动机所依赖的物理结构抽掉了。
5. 只有 70 条并发流（L251）——这个负载量相对 72 颗星、100 对源目的节点的评估规模严重偏小，"负载变化"这条轴基本没扫。
6. 评估只跑了 100 对源-目的节点一次，**没有误差棒、没有多随机种子**，而摘要里报的是 5%/13% 这种小差值。

**8. 和同批其他篇的关系**
- 与 **S85KQ4FC**：同为"每星一个 agent 的 DRL 路由"，但**方向相反**——S85KQ4FC 把"推理成本"当成头号约束（流级复用以摊销推理），本文则用"降低决策节点周边带宽"（L269）把它当外围开销一笔带过；S85KQ4FC 的观测含邻居**决策队列**负载，本文只有邻居**转发队列**（$QU_j$）。
- 与 **X5K285MW**：X5K285MW 刻意**不用任何负载信息**，本文则把负载（$QU_j$）放进状态；两者恰好构成"用不用负载信息"的对照。X5K285MW 也做 Walker star/Iridium-like 与逐包仿真。
- 与 **X2FCSU4S**：X2FCSU4S 也是"缓解 LEO 拥塞"，但手段是 GEO 缓存卸载 + 博弈定价，不碰路由；本文批评最短路造成高纬汇聚，手段是换下一跳。
- 原文引用的同族工作：ELB（[23,24]，L388–390）、**TLR（[25] Song et al., L392）**——TLR 在 X2FCSU4S 里也作为经典对照出现；另有 HGL（[14]）、PIR（[15]）、OPSPF（[30]）、GRouting（[19]）、DRL 负载均衡路由（[32] Zuo et al.）。
- 本文的 Q-learning 基线是 **[45] Yin et al.**（L432），该文亦见于 S85KQ4FC 的对比语境。

**9. 对"负载变化下到达率/时延"的贡献**
**给出了"以负载为优化目标时，时延会被牺牲多少"的方向性事实**：Fig 12 显示纯 Dijkstra 时延最低、纯队列利用率导向的 Dijkstra-QU 时延最高（L273），DQN-LLRA 落在两者之间——即"负载均衡是用时延换来的"，且换的幅度可以通过 RL 调权重在谱上滑动。但**没有给出任何"到达率 → 时延"的量化曲线**：负载轴在实验里由"70 条并发流"和"100 对源目的节点"两个离散设定构成，没有从低负载扫到拥塞的曲线，没有映射到 bps 或 Erlang，也没有拐点。作者声称的 5%/13% 改善是在**单一负载点**上测的。因此对"负载变化下到达率/时延"的贡献是**定性的（存在权衡）而非定量的（权衡曲线在哪）**。

**10. 一句话评价**
一篇标准的"把 DQN 套到 LEO 下一跳选择"的工程论文——**方法谱系上是把 DQN（[7] Mnih 2015）与既有负载均衡路由（ELB/TLR）直接拼接**，作者自己加的东西主要是"把奖励按 $C_i\le C_j$ 与 $QU_j\le 0.5$ 分成 4 段取不同权重"这种启发式工程细节；实验里最诚实也最可疑的一笔是"为公平而人为降低 RL 方案的决策节点带宽"（L269）——它承认了智能体开销的存在，却用一个拍出来的常数代替实测，正好是 S85KQ4FC 已经用实测曲线填上的那个洞。

## XLRW7XXN — A DQN-Based Routing Algorithm for Load Balancing in LEO Satellite Networks

**1. 一句话**
又一个"DQN 选下一跳"的负载均衡路由：把网络状态拆成**位置关系矩阵 / 负载矩阵 / 距离矩阵**三张矩阵喂给 **CNN**，奖励是"到目的距离 − 拥塞度 + 剩余带宽"的加权和，在 8×8 单层 mesh 星座上和 Dijkstra、最大流做对比。

**2. 问题设定**
小规模低轨星座里，传统路由（以 Dijkstra 最短路为代表）**缺乏对网络高动态的实时适应性与智能性**（L15、L21）。作者列了传统技术三条硬伤（L21 逐字）：(1) 无法从根本上避免链路/连接切换及随之而来的切换控制与重路由开销；(2) 计算代价高、**难以在星上实现**，通常需要地面系统辅助；(3) 与地面 IP 网络融合需要协议/数据格式转换，带来额外时间与处理成本。此外网络负载不均（L194）。

**3. 方法骨架**（RL，DQN + CNN）
- 星座与拓扑（第 2.1 节，L35）：**8×8 单层 mesh 星座**，**时间切片法**——每个时隙内视为静态拓扑；每星最多 2 条同轨 + 2 条异轨链路；考虑了极区与动态拓扑对连通性的影响。
- 通信模型（第 2.2 节）：AWGN 信道，主要考虑自由空间路损，式 1 $L=(\frac{c}{4\pi D_e f})^2$；式 2 SNR $=\frac{P_tG_tG_r}{k_BTBL}$；式 3 香农容量 $C=B\log_2(1+SNR)$。
- 时延三分量（式 4，L63）：$t_{total}=\sum_{e\in E}t_{prop}+\sum_{n\in N}t_{tran}+t_{queue}$——传播 + 传输 + **排队**。丢包率式 5：$loss=1-pac/n_{total}$。
- 约束（第 2.3 节）：带宽约束式 6（任务带宽 ≤ 路径上最小可用带宽）、**链路连通性约束式 7**（路径上所有链路的最小持续时长 ≥ 时隙长度 $T$）、传输速率约束式 8。**式 7 是这个星座模型里比较少见的一条**：把"链路能撑过整个时隙"写成了可行性条件。
- DQN 基础件（第 2.4 节）：四元组 $(s,a,s',r)$，Q 函数式 9、折扣回报式 10、Bellman 式 11、$\arg\max$ 式 12。注意 L102 说的是"**controller** collects link states... The controller uses this routing strategy to output the optimal next hop"，而 L146 又说策略下发到各卫星节点、逐跳决策——**架构描述前后不一致（集中式控制器 vs 分布式逐星决策）**，全文没有澄清。
- **状态**（L135）：由"链路状态 + 节点信息"组成，具体拆成**位置关系矩阵、负载矩阵、距离矩阵**三张，合并为一个状态；强调"optimize and compress the spatial dimension to improve network training efficiency"。用矩阵是为了让 CNN 吃。
- **动作**（L135）：选下一跳，四个相邻节点 = 四个动作，同时判断四条链路的实时连通性，"不同输出值"。
- **奖励**（式 13，L137–141）：$reward=-\omega_1 d_n-\omega_2 C_n+\omega_3 B_n$，其中 $d_n$ = 到目的节点距离，$C_n=q_n/Q_m$ 是**拥塞度**（当前队列长度 / 最大队列长度），$B_n$ = 链路剩余可用带宽，$\omega_1+\omega_2+\omega_3=1$，权重"可根据网络状况调整"。
- 训练流程（L146）：**离线阶段**用历史流量数据 + 仿真数据预处理后逐跳选动作，存下每跳动作及其前后状态（含连通性、节点拥塞、链路负载等多维矩阵），用**多通道 CNN** 学习；**在线阶段**按 T 更新拓扑、Poisson 分布分配初始负载、节点互发请求建连、按目标函数选下一跳，进入下一时隙时更新拓扑与状态矩阵并继续经验回放、更新参数。

**4. 它声称的效果**（三个图，全是趋势性描述，**无一个绝对数值**）
- Fig 4 端到端总时延（L174）：**网络空闲时三种算法差别不大**（拥塞不严重，时延以传播+传输为主）；**随数据包数增加，最短路算法拥塞明显、节点排队时延增大，总时延显著上升**；最大流算法能换路缓解拥塞但以牺牲距离/时延为代价；**DQN 最低**。
- Fig 5 网络吞吐（L179）：空闲时差别不大；繁忙时最短路最先触顶（链路容量限制）、吞吐最低；最大流因能最大化总流量而吞吐较高，但因时延高，峰值略低于本文；**DQN 最高**。
- Fig 6 **参与转发的卫星数**（L187）：DQN 最大。作者用这个当负载均衡的度量——"参与转发的卫星越多，每个节点被复用的次数越少"；最短路只涉及路径上的节点故复用极重；最大流受流量限制，靠近目的节点饱和后无法再扩展新节点。
- 基线：Dijkstra 最短路、**最大流算法**（L174）。

**5. 实验条件**
STK 生成，**64 颗星 / 8 轨道 × 8 星**，轨道高度 **895.5 km**，倾角 **86.4°**（L172）；用 STK 算连通性与星间距离，生成链路矩阵与距离矩阵（L172）。CNN 两个卷积层，卷积核 16 与 32（L172）。表 1（L177）：信道容量 **100 Mb/s**，单任务最大传输速率 **2 Mb/s**，包长 **512 bit**，节点初始负载服从 **Poisson 分布**，学习率 0.01，软更新权重 0.3，探索衰减 0.998，最小探索率 0.1，奖励衰减 0.9。
**转换缺陷须标注**：MinerU 把 Table 1 的两行串行了——"Number of LEO satellites / Orbit inclination angle" 的值串成 "8×8 86.4°"，"Maximum data rate / Size of packets / Maximum queue length" 的值串成 "2Mb/s 512 bit"，且 "Maximum queue length" 与 "Patch size"（疑为 batch size）行只剩 "100 200"。因此**最大队列长度与批大小的具体归属无法从 MD 确定**，我不做断言。
训练与评估：离线用历史/仿真数据训练，在线阶段继续学习（L146）——**是边跑边学**，训练与评估不是分离的。评估只给"数据包数"作为自变量（Fig 4/5/6 的横轴），**没有说明每一档具体是多少个包**。

**6. 它自己承认的局限**
**未见自述**。第 5 节 Conclusion（L192–194）通读到底，没有任何 limitation、future work 或"未做"的句子；全文也没有 Limitations 小节。读过的段落：摘要（L15）、引言（L19–29）、系统模型（L31–128）、算法（L133–168）、仿真（L170–190）、结论（L192–194）、参考文献（L196–217）。

**7. 它没做但看起来能做的地方**（基于内容）
1. **没有任何绝对数值**：三张图全靠文字描述趋势，摘要也没给百分比。而同一批的 X5Z98UPM 至少给了"降 5%/13%"。本文连一个数都没有，无法与其他工作横向比较。
2. 奖励权重 $\omega_1,\omega_2,\omega_3$ 只说"可根据网络状况调整"（L141），**既没给取值也没做敏感性分析**——而这三个权重恰恰决定了"时延 vs 负载"的折中位置。
3. **"控制器"与"逐星决策"的架构矛盾**（L102 vs L146）未澄清，直接导致"决策到底在哪算、通信开销多少"无法评估。
4. **状态矩阵的维数、CNN 输入尺寸、训练轮数、收敛判据全部缺失**；L135 虽然说"压缩空间维度以提高训练效率"，但没有给压缩前后的维度对比。
5. 丢包率式 5 定义了，但**实验结果里完全没有报丢包**——只有时延、吞吐、参与转发卫星数三个指标。
6. 式 7 的"链路持续时长 ≥ 时隙"约束在算法里怎么用（是剪枝还是惩罚）没写。
7. Algorithm 1 的伪码写成 "While the current node is D"（L155），按上下文应为"**不是** D"——可能是转换漏字，也可能是原文笔误；无论哪种，这份伪码不足以复现。

**8. 和同批其他篇的关系**
- 与 **X5Z98UPM** 几乎同构：都是 Iridium-like/小星座 + DQN 逐跳 + 奖励含"拥塞度/队列利用率"，连拥塞度定义都同形（本文 $C_n=q_n/Q_m$（L141） vs X5Z98UPM 的 $QU_i$（式 1））。差别在：X5Z98UPM 用全连接网（两隐藏层）+ 状态含最短跳数对，本文用 **CNN** 吃三张矩阵 + 状态含**到目的距离**；X5Z98UPM 有 4 段分段奖励，本文是线性三项。
- 与 **X5K285MW**：本文引 **Papa et al. 2020「Design and evaluation of reconfigurable SDN LEO constellations」（[5], L206）**，而同一篇正是 X5K285MW 的参考文献 [14]（L155）——两篇共享同一条 SDN-LEO 基线。
- 与 **S85KQ4FC**：共享 **DRL-ER（Liu et al., 本文 [10], L216）** 这条基线。
- 本文引 **HGL（Liu et al., [2], L200）**，X5Z98UPM 也引 HGL（其 [14]）——HGL 是两篇共同的批评对象（X5Z98UPM 说它在大规模流量突变时失效）。
- 本文引 **Zuo et al. [9]**（L214，DQN 时延导向智能路由），与 X5Z98UPM 的 [32] Zuo et al. 2022 同一作者群。

**9. 对"负载变化下到达率/时延"的贡献**
**给了一条定性但结构清晰的"负载—时延"分段叙事**（L174）：低负载区，三种算法时延几乎一致，因为瓶颈是传播+传输（与拥塞无关的固定项）；负载升高后，**最短路算法的时延因排队分量而显著上翘**，而 DQN 与最大流的上翘更缓。这实际上是在说：**"路由算法之间的差别只在到达率超过某个阈值后才显现"**，且差别几乎全部来自**排队时延项**（式 4 的 $t_{queue}$）。这是与 X5K285MW 的"合规悬崖"同构的观察，只是 X5K285MW 给的是合规率和实际 bps，本文给的是文字描述。
**缺陷**：横轴是"数据包数"而非到达率（packets/s 或 bps），没有给出任何一档的具体数值，也没有丢包曲线；式 4 虽然把时延拆成三项，但**实验结果里没有做分量分解**，所以"排队占了多少"仍不可知。

**10. 一句话评价**
方法谱系上属于"**把 DQN 换成一个 CNN 前端、把状态整理成矩阵**"这一支——核心机制（逐跳 Q 学习 + 拥塞度进奖励）与 X5Z98UPM 无实质差别，真正的增量是 ①用位置/负载/距离三张矩阵 + CNN 替代手工特征，②式 7 把"链路持续时长 ≥ 时隙"写成硬约束；但全文**没有一个绝对数值、没有权重消融、没有丢包结果、没有自述局限**，架构描述自相矛盾，实验规模（64 星、100 Mb/s 链路、2 Mb/s 任务）也远小于同批的 P-288（288 星）与 Iridium（72 星），因此它更像一份阶段性工程报告而非可复现的对比基准。

## XM64YRAW — Inter-Satellite Routing for LEO Satellite Networks: A GNN and DRL Integrated Approach（IEEE/CIC ICCC 2024）

**1. 一句话**
把 **MPNN（消息传递图神经网络）当作 DQN 的 Q 函数逼近器**（作者叫 GQN），并且**把"路径"而不是"下一跳"作为动作空间**（用 Yen k-最短路生成候选），目标是同时压低网络级平均端到端时延和链路利用率的方差。

**2. 问题设定**
要建天基核心网就要星间多跳路由，三个困难（L37）：① LEO 卫星速度 **6.9–7.7 km/s**，拓扑与 ISL 信道增益频繁变化；② 卫星数量激增（举例：**到 2024 年 3 月 Starlink 已部署近 6000 颗**）导致拓扑复杂；③ 业务需求越来越**异构**，为同构流量设计的传统方案效率下降。作者的判断是：**常规 DRL 泛化能力不足**（L39 逐字："conventional DRL algorithms lack generalization ability, hindering their performance in satellite networks with fast-varying topologies"），所以引入 GNN 来学图节点间关系以获得泛化。

**3. 方法骨架**（RL，DQN + MPNN；动作空间是路径）
- 问题建模（第 II 节）：时间按时隙切分，每时隙拓扑固定，建成图 $G(V,E)$；用"四链路算法"建 ISL（L51）。流量是 $N\times N$ 矩阵 $F$，元素 $f_{o,d}$ 是 OD 对所需速率。每条 ISL 两个参数：容量 $R^{total}_{i,j}$ 与直线距离 $W_{i,j}$，**全双工、对称容量**（L51）。
- 目标函数式 5（L85）：$\max\sum_{o,d}\sum_p x^p_{o,d}\left(\alpha\frac{1}{L^{prop}_{p,o,d}}+\beta R^{res}_{p,o,d}\right)$。作者解释动机（L82）：路由决策必须在传输前做，**只能用可测参数估计**，所以用"传播时延的倒数 + 剩余容量"的加权和代理"网络级平均端到端时延"。
- 约束：容量式 6、流量守恒式 7、**单路径选择式 8**（每个 OD 对只选一条路径）。
- 路径剩余容量式 3 定义为**路径上所有边的最小剩余容量**；传播时延式 4 是路径上各边 $W_{i,j}/c$ 之和。
- MPNN 部分（第 III.A 节）：消息聚合式 9、更新式 10、读出式 11；**聚合函数用求和近似**（L120）。
- DQN 部分（第 III.B 节）：Q 值式 12、目标值式 13（**max 目标**）、MSE 损失式 14、$\varepsilon$-greedy（L157）。
- **状态**（L165）：把所有 ISL 的状态向量拼接起来；每条 ISL 的状态 = **该 ISL 收到的流量需求 + 该 ISL 的剩余容量**；为了配合 GNN，拼接向量还要在特定位置**补零**以存放来自相邻 ISL 的聚合信息。**关键设计选择：把 ISL（而不是卫星）当作 GNN 里的节点**（L165 逐字："we set ISLs as nodes in the GNN model"），理由是"ISL 的特征才是影响路由设计的主导因素"。
- **动作**（L175，与同类工作最大的区别）：不是选下一跳，而是**从 OD 对之间的候选路径集中选整条路径**，用 **Yen k-最短路**生成候选集，作者自述这样可以"enhance the model's global awareness"并降低 MDP 维度、加快收敛（L43）。
- **奖励**（式 15，L169–173）：$Reward=\alpha\frac{L_{standard}}{L_{action}}+\beta\frac{R_{action}}{R_{standard}}$——**两项都是"与参考路径的比值"而非绝对值**：第一项比较动作路径与参考路径的时延，第二项比较两者剩余容量。
- 实现（L161）：Behavior Network 与 Target Network 都用 MPNN 搭，消息传递经过全连接层，**用 RNN 迭代 T 次更新历史消息**，再用求和聚合，最后读出函数输出 $Q(s,a;\theta)$。Algorithm 1（L177–198）给出训练循环。

**4. 它声称的效果**（三个指标，全部以"总需求速率"为横轴）
- 时延（Fig 3a，L236 逐字）："when the sum required data rate is low, propagation delay has a significant impact on end-to-end delay, and **GQN does not show significant advantages over SP**. As the sum required data rate increases, the average end-to-end delays of all schemes increase. **GQN achieves the lowest delay among all schemes, and the advantage is more significant under high traffic demands**."
- 丢包（Fig 3b，L250）：SP 丢包最高且随总速率快速增长；DQN 与 LB 较低但**明显受系统负载影响**，高需求速率下丢包上升；**GQN 在所有传输速率下都保持最低丢包**。
- 链路利用率方差（Fig 3c，L268）：SP 走固定路径导致少数最短路承担大部分流量、负载分布不均、方差最高；DQN 优于 LB；**GQN 在不同传输速率下始终保持最低方差**。
- 泛化（Fig 4，L273）：在轨道周期 T 的 **0、0.2T、0.4T、0.6T、0.8T** 五个时点评估，GQN 的链路利用率方差始终最低。
- 基线：**SP**（在所有可能路径里选最短）、**LB**（随机选一条剩余容量非零的路径）、**DQN**（用常规 DNN 而非 MPNN 表示 Q 函数，L208）。
- **注意**：全文只有趋势描述，**没有任何绝对数值**（时延 ms、丢包 %、方差具体值都没有出现在正文里）。

**5. 实验条件**
Python + Keras 搭 MPNN 与 DQN（L206）。星座：**9 条倾斜轨道 × 每轨 12 星 = 108 颗**，倾角 **50°**，高度 **550 km**；每星 4 条 ISL（2 同轨 + 2 异轨）（L206）。**所有 ISL 容量统一 10 Mbps**；业务需求 $f_{o,d}$ **在 1.8–2.7 Mbps 之间波动**；包大小 $\eta$ = **10 Kbs**（L206）。
时延分解（式 16–19）：$L_{E2E}=L_{prop}+L_{que}+L_{tran}$，其中 **$L_{que}=\sum_{(i,j)\in E}\frac{\eta}{\lambda}\left(\frac{\lambda_{i,j}}{R^{total}_{i,j}-\lambda_{i,j}}\right)$**（式 18）——这是一个 M/M/1 型的排队时延求和，$\lambda=\sum f_{o,d}$ 是所有需求之和。丢包按式 20（路径上最严重的"需求超出容量"比例）与式 21（全网平均）算。链路利用率 $\rho_{i,j}=\lambda_{i,j}/R^{total}_{i,j}$（式 22），报告的是**方差**。
训练/评估：Fig 3 是跨"总需求速率"的评估，Fig 4 是跨时隙的泛化评估。

**6. 它自己承认的局限**
**未见自述**。第 V 节 Conclusions（L275–277）通读到底，只有正面总结，没有 limitation、没有 future work；全文也没有 Limitations/Discussion 小节。读过的段落：摘要（L27）、引言（L33–47）、问题建模（L49–104）、算法（L106–200）、实验（L202–273）、结论（L275–277）、参考文献（L279–306）。

**7. 它没做但看起来能做的地方**（基于内容）
1. **$L_{que}$ 是式 18 这种在 $\lambda_{i,j}\to R^{total}_{i,j}$ 时发散的公式**，而丢包率式 20 又只在超容量时才非零——**时延指标在饱和附近会爆炸，丢包指标却是硬截断**，两者对"拥塞"的刻画不一致。作者没有讨论这一点，也没有把时延/丢包在拐点附近的交叉验证做出来。
2. **$k$（Yen k-最短路的 k）在全文从未给出取值**（Algorithm 1 的 Input 里有 $k$，L180，但实验设置 L206 没有），也没做 $k$ 的消融——而 $k$ 同时决定了动作空间大小与"能否绕开拥塞"。
3. **$\alpha,\beta$（目标权重与奖励权重用同一组符号）从未给数值**，也没给两者是否相同。奖励式 15 与目标式 5 用了同一个 $\alpha,\beta$ 记号但含义不同（一个是绝对量的加权，一个是比值加权），**容易误读**。
4. **参考路径 $L_{standard}$/$R_{standard}$ 怎么选从未说明**——这是奖励的基准，却完全没定义。
5. 训练细节（episode 数、T 迭代次数、隐藏层维度、学习率、$\varepsilon$ 衰减）**全部缺失**，无法复现。
6. "泛化能力"只通过**同一星座不同时刻**验证（Fig 4），**没有跨星座/跨规模测试**——而 GNN 的核心卖点正是对"未见过拓扑"的泛化（L39 自己这么说的）。这是它自己立论的最大缺口。
7. 业务需求只有"1.8–2.7 Mbps 区间内波动"一个刻画，**没有说明波动的时间相关性**（是独立采样还是平稳过程），而"diversified traffic demands"是它宣称要解决的三大挑战之一。

**8. 和同批其他篇的关系**
- 与 **X5Z98UPM / XLRW7XXN**：三者都是 DQN 路线，但**动作空间根本不同**——X5Z98UPM 与 XLRW7XXN 都是"四邻居选一"（逐跳），本文是"候选路径里选一条"（逐流）。本文的 GQN 与 XLRW7XXN 又都用 CNN/MPNN 这类结构化网络替代全连接网，但 XLRW7XXN 是把三张矩阵喂 CNN，本文是把图直接喂 MPNN。
- 与 **X5K285MW**：X5K285MW 的核心发现是"最小跳集合内的**逐流随机选路**就能多承载 73% 流量"，而本文的基线 **LB = 随机选一条剩余容量非零的路径**（L208）——两者机制高度相似，但在本文里 LB 输给 DQN。**这是一个可对照的点**：X5K285MW 说随机选路很强，本文说它不够强；差别可能在于本文的 LB 是"剩余容量非零"（无均衡意图）而 X5K285MW 是"最小跳集合内"随机。
- 与 **S85KQ4FC**：S85KQ4FC 的核心论点是"逐包推理跟不上转发"，而本文是**逐流/逐路径决策**（动作空间是路径），天然回避了逐包推理问题——但本文完全没提推理开销，也没在基线上做推理成本对齐。
- 本文引 **Almasan et al. 2022「DRL Meets GNN: Exploring A Routing Optimization Use Case」（[12], L303）**——这是"GNN+DRL 路由"这条线的关键前作（虽未在正文引用位出现，但在参考文献里）。

**9. 对"负载变化下到达率/时延"的贡献**（本批目前贡献最直接的一篇之一）
**它是本批（截至第 5 篇）唯一把"总需求速率（sum required data rate）"明确当作扫描自变量、同时报告时延 + 丢包 + 链路利用率方差三条曲线的论文**，给出了三条可引用的事实：
1. **存在一个"路由算法无关区"**：低负载时传播时延主导，GQN 相对 SP **没有明显优势**（L236 逐字）——这与 XLRW7XXN 的"网络空闲时三种算法差别不大"（L174）和 X5K285MW 的"合规悬崖"是同一个现象的第三次独立观测。
2. **优势随负载单调放大**："the advantage is more significant under high traffic demands"（L236）——即负载感知路由的收益是**负载的函数**，而非常数。
3. **丢包的负载敏感性因算法而异**：SP 的丢包随负载快速增长，DQN 与 LB"较低但明显受负载影响"，GQN 最平（L250）——即**负载感知路由不仅降低丢包水平，还压平了丢包的负载斜率**。
**缺点**：① 横轴"sum required data rate"**没有给出任何具体量纲数值**（既没说总共多少 OD 对，也没给总速率的范围），只有趋势；② 时延/丢包曲线**没有任何数据点被引用**，全部靠读图描述；③ 排队时延用 M/M/1 型公式（式 18）**假设泊松到达与指数服务**，而流量是"1.8–2.7 Mbps 波动"的稳态需求，式 18 里没有体现突发性。

**10. 一句话评价**
在方法谱系上，它是 **"GNN 当 DQN 的 Q 函数逼近器"这一支在 LEO 星间路由上的落地**（引 Almasan et al. 2022 那条线），最实质的两个改动是**把 ISL 而非卫星设为 GNN 节点**、以及**把动作空间从"下一跳"抬到"整条 k-最短路"**；这两个选择都合理且有解释，实验也确实扫了负载轴并给出了"低负载无差别、高负载优势放大"这一与同批多篇互相印证的结论——但它终究是一篇 6 页会议短文：**载荷与权重的全部数值、k 的取值、参考路径的定义、训练超参全部缺失，泛化只在同一星座的 5 个时点验证**，"更强的泛化能力"这个中心论点实际上没有被它自己的实验真正检验（没有跨星座/跨规模）。

## XM6NUPM4 — Your Mega-Constellations Can Be Slim: A Cost-Effective Approach for Constructing Survivable and Performant LEO Satellite Networks

**1. 一句话**
不问"怎么路由"，而问"**到底需要多少颗卫星**"：把"可生存 + 有性能"的星座设计写成整数规划 SPLD（最少卫星数，同时满足冗余路径数、链路容量、端到端时延三类约束），再用 MEGAREDUCE 在多项式时间内反复"可行性判定 + 收缩/扩张"搜索近优解，在 Starlink/Kuiper 真实参数上最多砍掉约 20–22% 的卫星。

**2. 问题设定**
巨型星座的部署既带来**可生存性**（更多冗余备份链路与路径，抗太阳风暴/辐射/硬件故障，L17）和**性能**（更广覆盖、更高星座总容量，L19），也带来**成本**与**治理问题**（空间交会与碎片，L25）。作者指出既有工作要么只优化覆盖/时延/容量而**不考虑空间环境下的可生存性**（L27），要么是**静态地面网络的 SND 问题**、难以直接搬到高动态的天基骨干（L56），要么靠引入 GEO 分层来省卫星但**会抬高时延且 GEO 容量有限**（L58）。核心问题（L13）："from a network perspective, how many LEO satellites exactly does an LSN need"。

**3. 方法骨架**（非 RL：整数规划建模 + 多项式时间可行性判定 + 启发式调优）
- 网络建模（第 III.A 节）：时隙化，$I^t_{ij}$ 表示 i 与 j 在时隙 t 是否互相可见，$e^t_{ij}=1$ 表示该时隙存在活动链路（**链路只有两端可见才能激活**，L70）；LSN 建成时变图 $G_t=(V,E_t)$，$V=S\cup\mathcal{C}$（卫星 ∪ 地面小区，L72）。地面按 H3 方法聚合成**小区**（cell），一个点波束服务一个小区（L74）。
- 容量模型：每条波束的上/下行容量 $Cap^t_{ji}/Cap^t_{ij}$，卫星总上/下行容量受星上供电约束（$Cap^{max}_{up}, Cap^{max}_{down}$）（L74）。**关键假设**：激光 ISL 容量远高于无线 GSL，且在有空间流量调度的情况下 **ISL 不太可能成为瓶颈**（L74 逐字："the capacity of laser ISLs is much higher than that of radio GSLs, and ISLs are unlikely to be the bottleneck in LSNs with existing space traffic steering"）。
- 可生存性定义：需求 d 关联 $i,j$ 是 **R-edge connected**，当且仅当**在所有时隙**下 i 与 j 之间都有至少 R 条边不相交路径（L76–78）。
- **基本 SPLD**（第 III.B 节）：目标 min $\sum_{i\in S}x(i)$，约束 8 条（式 1–8）：可见性、链路端点须在子图内、每星激活 ISL 数 ≤ 发射机数 $N_{ISL}$、每个 cell 上/下行容量、卫星 GSL 容量上限，以及**式 8 的最小割形式可生存性约束**——对任意非空真子集 $\overline{V}$，割边数 ≥ $\max r_{pq}$，保证至少 $r_{pq}$ 条边不相交路径（L122）。
- **加时延约束的 SPLD**（第 III.C 节，核心构造）：把无向图转成**有向分层图**（layered graph），按需求分解成 $|D|$ 个子问题。时延门限取 $L_d=\lceil\lambda\cdot L^{sp}_{ij}\rceil$（$L^{sp}$ 是最短路"长度"，$\lambda\ge1$ 是约束因子，L128）；建 $L_d+1$ 层，边只能从第 $l$ 层连到第 $l+1$ 层，**这样任何从 src 到 dst 的路径都自动满足 L 跳约束**（L137–139）。在分层图上写流量守恒式 9（保证 $r_d$ 单位流、同时保证 $r_d$ 可生存性）、防环式 10、边不相交与卫星入选式 11、链路容量式 12。
- 复杂度：**即使所有 r=1，单时隙 SPLD 也退化为 Steiner Tree，NP-hard**；作者初步实验显示数百颗星的规模就已无法求解（L171）。
- **MEGAREDUCE**（第 IV 节）：核心思想是"最优解难求，但**判定给定 LSN 是否可行可以多项式时间做**"（L177）。四步循环：初始化 → 可行性判定 → 星座调优（可行则 Shrink，不可行则 Expand）→ 在可行解中选卫星数最少的（L182–190）。
  - 搜索范围 $[\mathcal{N}_{min},\mathcal{N}_{max}]$：$\mathcal{N}_{max}$ 取原星座卫星数；**$\mathcal{N}_{min}$ 的关键洞察**——要保证 cell i 与 j 之间有 $r_{ij}$ 条不相交路径，至少要有 $r_{ij}$ 颗卫星对 i、j 可见（L196）。
  - **调优原则（本文最漂亮的一条洞察，L255）**：Walker Delta 星座中任意两颗通信卫星之间最短路径的最大跳数是 $\lceil(O+M)/2\rceil$，**当 $O=M$ 时取最小值**——所以 Shrink/Expand 都朝"让轨道数 O 与每轨星数 M 更接近"的方向调整。
  - Algorithm 1（搜索，L198）、Algorithm 2（FeasibilityCheck，L224）、Algorithm 3（Shrink/Expand，L257）。可行性判定里：对每个时隙的每个 cell 先算可用上/下行容量（Algorithm 2 line 3–6），再对每个需求建分层图、用**最大流**算可达的边不相交路径数并与 $r_{src,dst}$ 比较（line 11–12），最后**逐需求扣减** src 上行与 dst 下行容量（line 14–17）。

**4. 它声称的效果**
- 时延约束用 $\lambda$ 参数化：如已知需 ≥1500/1600 颗星才能满足 $r_{min}=5/6$，则可反推"给 1550 颗星，可支撑的 $r_{min}$ 到 5"（L350，这是函数求逆的用法）。
- Fig 4（L306）：随可生存性要求 $r_{min}$ 提高，MEGAREDUCE 动态增星、构建更多边不相交冗余路径；**即便在 $r_{min}=6$ 的最严苛情形，Starlink 与 Kuiper 的所需卫星总数仍可分别减少 20.05% 与 21.88%**。
- Fig 5（L308）：把**每小区平均容量需求从 20 Mbps 扫到 40 Mbps**，所需卫星数随需求上升（更多高吞吐波束）。
- Fig 6（L310）：$\lambda$ 越小（路径长度约束越紧），需要越密的星座来提供受长度约束的冗余路径。
- Fig 7（L328）：**高度 × 倾角 × 所需卫星数**的 3D 曲面，两个观察：① 所需卫星数**随高度上升而下降**（覆盖更广、单 cell 被更多星服务、冗余链路更多），但作者同时指出**高度上升会带来更高的星地传播时延**；② 所需卫星数**随倾角增大而上升**，因为多数通信小区在 $[-70°,70°]$ 纬度带内，倾角更大的星座能为这些"热点小区"提供更高卫星密度。
- Fig 8 韧性分析（L332）：两种失效模型——**太阳风暴**（邻近一批卫星同时损毁，用例：2022-02-04 报废的 49 颗 Starlink）与**随机失效**（硬件故障/器件老化）。指标是**可达率**（可达通信对 / 总通信对）。**基线是 UltraDense（文献 [12] Deng et al.）**；相同星座规模下 MEGAREDUCE 可达率更高。
- Fig 9a 增量部署（L354）：用 SpaceTrack 的 Starlink 真实历史数据（2019-12 至 2023-06），真实 Starlink 的 $r_{min}$ 在 **3.5 年内从 0 涨到 5**；用同样分批发射数量但改用 MEGAREDUCE 设计，**早期阶段就能取得更高的可生存性**。
- Fig 9b 在轨调整（L356）：Starlink 的**年衰减率 AAR ≈ 2.6%**（每年约 2.6% 卫星失活）；不补星则生存性渐降，按 MEGAREDUCE 及时调整结构可维持较高生存性。

**5. 实验条件**
仿真器：扩展 **StarPerf**（作者自己的前作，L452），增加"灵活调整星座结构"与"可生存性评估"能力；星座信息取自公开监管文件（FCC 的 SpaceX Gen2 与 Kuiper 文档，L448–450）；地面站分布按 starlink.sx（L454）。参数（L284）：**激光 ISL 容量 20 Gbps，共享 GSL 容量 4 Gbps，$N_{ISL}=4$**。**每个实验都仿真一个完整的回归周期**（L284）。优化器基于 **Gurobi** + **SkyField**（高精度轨道/轨迹计算）实现（L284）。流量：结合 Starlink 可用性地图与文献 [11] 的**人口比例流量模型**生成需求矩阵（L286）。初始星座：**Starlink 一期 4408 颗 / 5 个轨道壳层 / 高度 540–570 km**；**Kuiper 3236 颗**（L290）。代码开源：https://github.com/SpaceNetLab/MegaReduce（L362）。
**一个关键交代（L332）**："We assume that the high layer routing protocols can efficiently detect redundant paths and switch to the backup path if the current path fails."——即韧性评估**假设路由协议能即时切换**，路由本身不在本文范围内。

**6. 它自己承认的局限**
**未见自述**。第 VI 节 "CONCLUSION AND ACKNOWLEDGEMENT"（L358–360）通读到底，只有正面总结与致谢，没有 limitation、没有 future work；全文也没有 Limitations 小节。读过的段落：摘要（L5–7）、引言（L9–33）、背景与相关工作（L35–62）、系统模型与问题陈述（L64–171）、优化机制（L173–278）、评估（L280–356）、结论（L358–362）、参考文献（L364–465）。
（可算作**显式假设**而非局限的有：L332 的路由协议即时切换假设；L74 的"ISL 不会是瓶颈"假设。）

**7. 它没做但看起来能做的地方**（基于内容）
1. **时延约束完全是"跳数/路径长度"约束**（$L_d=\lceil\lambda L^{sp}\rceil$，L128），**排队时延完全不建模**。而 LSN 的实际端到端时延在负载高时由排队主导——本文的"acceptable latency"实际只覆盖了传播部分。这是它自己框架内最明显的一处缺口。
2. **容量需求是"每小区平均容量"这一个静态标量**（20–40 Mbps，L308），没有任何时间维度：没有峰值/均值比、没有到达率的时变过程、没有突发性。而它自己的 GSL 容量模型（式 4–7）是按"所有需求之和 ≤ 同时可见卫星容量之和"来判定的，这个判定在时变流量下会完全不同。
3. **可行性判定用的是平均/总量口径**：Algorithm 2 里对每个 cell 只维护一个 $AvaiCap$ 标量并按需求逐个扣减（L241–244），**没有考虑需求之间的时间重叠或随机性**。
4. Rayleigh/多径、干扰、误码率**完全不在模型里**（容量是给定的常数 $Cap$），所以"20 Gbps ISL"这个数字的可靠性未被检验。
5. MEGAREDUCE 是**启发式搜索**（二分式的 Shrink/Expand + 迭代上限 $I_{limit}$），**没有给出与最优解的差距（近似比）**，只说"near-optimal"（L360）。$I_{limit}$ 的取值也没给。
6. **$\lambda$（时延约束因子）的取值范围在正文中没有明确给出**，只说"as the value of λ decreases"（L324）。
7. 韧性评估的失效模型是**两种特定模式**（太阳风暴成簇失效、独立随机失效），**没有考虑相关性失效**（例如同一轨道面系统性退化的共因失效），而 Walker Delta 的轨道面结构恰恰容易产生这类失效。

**8. 和同批其他篇的关系**
- **与 X5K285MW 耦合最深**：两篇共享至少 4 条核心参考文献——**Bhattacherjee & Singla, CoNEXT'19「Network topology design at 27,000 km/hour」**（本文 [11]，X5K285MW 的 [2]）、**Giuliari et al.「Internet backbones in space」**（本文 [17]，X5K285MW 的 [8]）、**Gvozdiev et al.**（本文 [41] "On low-latency-capable topologies…" SIGCOMM'18；X5K285MW 的 [9] "Low-Latency Routing on Mesh-Like Backbones" HotNets'17——**两篇都用了 Gvozdiev 那条关于"额外跳数与传播时延关系"的分析线**）、**Walker 1984**（本文 [42]，X5K285MW 的 [16]）。
- 更实质的呼应：X5K285MW 讨论"**放宽最小跳约束（允许 +2 跳或更多），只要仍满足 QoS 就还能提升负载均衡**"（X5K285MW L70）；本文则把同一件事做成了**硬约束**——$\lambda$ 就是"允许多少倍的跳数"，且 Fig 6 显示 $\lambda$ 越小需要越多卫星（L310）。**两篇从两个方向夹住了同一个变量**：一个问"多给几跳能换来多少吞吐"，一个问"要求几跳要付出多少卫星"。
- 与 **S85KQ4FC**：两篇都在 LEO 巨型星座背景下讨论"网络级性能 vs 资源"，但 S85KQ4FC 关注的是**星上推理资源**，本文关注的是**卫星数量/部署成本**——两个不同的"资源预算"维度。
- 本文引 **OPSPF（Pan et al., [36]）**——该文也出现在 X5Z98UPM 的参考文献（其 [30]），是 LEO 路由领域的共享基线；本文引 **SpaceRTC（Lai et al., [38]）** 与 **resilient routing in STIN（[39]）** 作为"空间流量调度"互补工作。
- 方法谱系上本文与同批三篇 DRL 路由（X5Z98UPM / XLRW7XXN / XM64YRAW）**完全不同路**：那三篇是"给定网络、优化转发策略"，本文是"给定需求、优化网络本身"。**它的基线 UltraDense（[12] Deng et al.）也是"最少需要多少 LEO 卫星"这一路**，不是路由算法。

**9. 对"负载变化下到达率/时延"的贡献**
**是"容量规划"而非"负载动力学"的贡献**，需要分开说：
- **直接贡献**：给出"**需求 → 所需网络规模**"的定量曲线。Fig 5 把每小区平均容量需求从 20 扫到 40 Mbps，给出所需卫星数单调上升（L308）——这是本批唯一一条"负载 → 资源"（而非"负载 → 时延/丢包"）的曲线。Fig 6 给出"时延约束 $\lambda$ 收紧 → 所需卫星数上升"（L310）。Fig 7 给出高度/倾角对所需卫星数的二维影响面。
- **与"到达率/时延"的关系**：**没有直接贡献**。本文的"时延"是**路径长度约束**（跳数 ≤ $\lceil\lambda L^{sp}\rceil$），不含排队时延、不含到达率；"容量需求"是**静态平均值**（Mbps per cell），不含到达过程、不含突发性。换句话说，它回答的是"**为了承载这个量级的流量，网络至少要多大**"，而不是"**到达率变化时，时延会怎么变**"。
- **一个间接但有价值的事实**：L328 明确指出"提高轨道高度可以减少所需卫星数、但会增加星地传播时延"——即**卫星数量与时延之间存在结构性权衡**（不是通过路由，而是通过星座几何）。这与 X5K285MW 的"路径多样性与平均时延权衡"、XM64YRAW 的"负载均衡与传播时延权衡"属于同一族的**权衡结构**，只是调节旋钮从"选路"换成了"星座几何"。

**10. 一句话评价**
本批唯一一篇**站在网络设计者而非路由器角度**的论文：把"最少多少颗卫星"这个运营层面的问题写成一个带最小割可生存性约束的整数规划，用"可行性判定多项式、最优解 NP-hard"这一经典突破把问题拆成"判定 + 二分调优"，并用 $O=M$ 时 $\lceil(O+M)/2\rceil$ 跳数最小这条 Walker Delta 的结构性质作为调优启发式——工程上扎实、真实数据驱动（StarPerf + FCC 文档 + SpaceTrack 历史 + 20/4 Gbps 链路参数）、代码开源，与同批路由论文共享 Bhattacherjee/Gvozdiev/Walker 这条 LEO 拓扑设计血脉；但它与"负载变化下的到达率/时延"这一问题**基本不在同一维度**：时延被简化成跳数约束、容量需求被简化成静态均值，因此它提供的是**规划期的一个标量答案**，而非运行期的动态曲线。

## Y2H4NPLU — Q-learning for distributed routing in LEO satellite constellations

**1. 一句话**
把 1993 年的 **Q-routing**（Boyan & Littman，[8]）搬到 LEO 星座上做**全分布式多智能体**路由：每颗卫星是一个独立 agent，只用 2 bit 编码的邻居链路/队列信息和邻居回传的 Q 值更新自己的 Q 表，**主动与两个"中央集权 + 已知队列状态"的 Dijkstra 基线对比**，证明分布式 Q-routing 支持的负载更高。

**2. 问题设定**
摘要（L5）把 LEO 路由的难点讲得比同批任何一篇都清楚，逐字："The topology, of finite size, is dynamic and predictable, the traffic from/to Earth and transiting the space segment **is highly imbalanced**, and **the delay is dominated by the propagation time in non-congested routes and by the queueing time at Inter-Satellite Links (ISLs) in congested routes**." 既有做法的两个毛病（L5）：**依赖与地面或其他卫星的过量通信**（信令开销），以及**对"通往目的地的各段链路"刻画过度简化**（例如文献 [7] 用截断高斯分布建模排队时延，L15 逐字："the model of the queueing time is too simplistic, e.g., using truncated Gaussian distributions"）。作者还引文献 [4] 的一个实测事实：传统 unipath 源路由的端到端平均时延约 **100 ms**，其中**传播时延占比随负载在 37%–66% 之间变化**（L13）——这直接把"时延的主导项随负载切换"写进了问题设定。

**3. 方法骨架**（RL，**表格型 Q-learning**，非 DQN；多智能体 POMDP）
- POMDP 四元组 $(S,A,P(s,a),R(s,a))$，观测来自自身队列/链路 + 邻居反馈（L62）。
- **状态**（L79）：$S_i=\{L_i,N_i\}$。$L_i$ = 从包头取出的目的节点 + 自身链路连通性 $\mathcal{E}_i$；$N_i$ = 四个邻居（2 同轨 + 2 异轨）各自的**链路质量与缓冲拥塞，每个只用 2 bit 编码**——$s_t=2$ 表示"长队列或链路不可用"，$s_t=0/1$ 分别表示"不拥塞且链路容量高/低"。作者自述这样做是"**minimizes the state space and alleviates the computation cost, which is an advantage for satellites with limited computation capabilities**"（L79）。
- **动作**（L97）：$a_t$ 从 $\mathcal{E}_i\cup\mathcal{E}_{i_G}$ 里选下一跳（邻居卫星或通往网关的链路）。
- **奖励**（式 5–7，L84–95）：三段式——若下一跳 j 的关联网关就是目的地，给 $r_{del}$；若 j 已在包已访问集合 $\mathcal{P}_p$ 中，给循环惩罚 $r_{loop}$；否则 $r_{queue}+r_{dist}$，其中
  $r_{queue}=w_1(1-10^{t_q(j)})$（**随下一跳排队时延指数增长的惩罚**），
  $r_{dist}=w_2\frac{\|id\|-\|jd\|+\|sd\|}{\|sd\|}$（归一化的"到目的地斜距缩短量"）。
- **Q 更新（本文唯一的实质方法学改动）**（式 8，L130）：$Q_i^{*}(s_t,a_t)=(1-\alpha)Q_i(s_t,a_t)+\alpha\left(r_t+\gamma\max_a Q_j(s_{t+1},a)\right)$——注意 $\max$ 里取的是**邻居 j 的 Q 表**，而不是 i 自己的。理由（L103 逐字）："the actions taken by satellite i are observable in the state change of the neighbouring satellites, more specifically in the increased queue length of the next hop j. Therefore, we modify the usual formulation to reflect this partial knowledge and correlation among actions."
- **反馈最小化**（L133）：算法与邻居的唯一交互就是"成功收到包之后回传一个 Q 值"，在一段已经建立的链路上传输。
- $\varepsilon$-greedy，$\varepsilon$ 初期高、随后指数下降（L101）。Algorithm 1（L105–127）。
- **一跳时延**（式 3，L51）：$L(i,j)=\underbrace{t_q(i)}_{\text{排队}}+\underbrace{B/R(i,j)}_{\text{传输}}+\underbrace{\|ij\|/c}_{\text{传播}}$。**链路速率**（式 1，L33）：$R(i,j)=W\max\{\rho: \frac{P_r(i,j)}{k_BT_SB}\ge \mathrm{SNR}_{min}(\rho)\}$，即在 **DVB-S2** 的调制编码方案里选满足 SNR 的**最高频谱效率**——链路速率是**自适应**的，这点同批多数论文都没做。
- **队列模型**（L46）：每星一个 FIFO 发送缓冲，上限 $Q_{max}$，**满则丢包**。
- **流量模型**（L38）：每个活跃网关把等量数据发给其余所有网关，到达服从**泊松分布**速率 $\lambda^{(g)}_{UL}$；定义 $\lambda^*$ 为网络可支持的最大负载（由上下行 GSL 速率算出），**总负载 $\ell=\sum_g\lambda^{(g)}_{UL}/\lambda^*$**——这是一个归一化的、可跨场景比较的负载定义。

**4. 它声称的效果**
- **稳定性分析（本文最硬的实验设计，L141）**：定义"路径稳定"= 端到端时延不随时间增长。做法是取**最后 200 个到达目的地的包**（避开训练期），对"时延 vs 包序号"做线性回归得斜率 $\hat\beta_1$，再做 **t 检验，$H_0:\beta_1\le0$，显著性水平 0.05**；未通过则该路径标记为不稳定。
- Fig 3（L143）不稳定路径比例 vs 活跃网关数：**data rate BM 从 9 个网关起急剧上升**（因为它按高数据速率选路、无法感知拥塞）；**latency genie BM 在 8 个网关就开始上升**但比 data rate BM 慢；**Q-routing 的初始上升最慢**，只有在 **超过 14 个网关**时才比另两者差，但那时三者都 > 0.1、网络已不可用。**8 个网关时 Q-routing 没有任何不稳定路径**；9 个网关时 Q-routing 只有一条不稳定路径（Inuvik, Canada → Córdoba, Argentina）。
- **对"genie 也输"的解释（L143）**：所有不稳定路径有三个共同特征——① 两网关间距离大，② 由南向北，③ **多数有相同的目的地**。原因是 genie 在源端按**当时的**队列状态选路，但包到达远端链路时队列状态早已不同（"If the distance is long, the queue of a distant satellite might be empty at the time the packet is transmitted from the source, but increase significantly before the packet arrives"）。作者据此断言：**即便假设全局瞬时知识，源路由本身也是次优的**。
- Fig 4（L151）时延分解 vs 活跃网关数：**传输时延在所有情形下 < 0.72 ms**，相对传播与排队可忽略、故未画；**latency genie BM 的传播时延最低**，但其**排队时延在 $|G|\ge8$ 时显著上升**；**Q-routing 的传播时延在所有情形下都比另两者略大**，作者给了两条原因（见第 6 项）。
- Fig 5（L160）时延-时间曲线：Q-routing **初期时延较大**（探索阶段随机选路），随后迅速下降到稳定值并转入以利用为主；data rate BM 在 $|G|=3$ 时保持低值，但 $|G|=9$ 时出现**线性增长**——即拥塞的可视化特征。
- **基线有两个，且都很强**（L56）：**data rate BM**（边权 $w_{i,j}=1/R(i,j)$，即偏好高速率链路的传统源路由）与 **latency genie BM**（**假设瞬时已知所有卫星的队列状态**，源网关据此选最小 E2E 时延的路径）。

**5. 实验条件**
自研 Python 仿真器（L137）。星座：**Kepler 星座，$M=7$ 个轨道面，高度 600 km，每面 $N_m=20$ 颗星**（共 140 颗）（L137）。地面：**最多 18 个发射网关**，位置**基本取自真实 KSAT 网络**，逐个列出：Málaga（西班牙）、Los Angeles（美国）、Aalborg（丹麦）、Córdoba（阿根廷）、Tolhuin（阿根廷）、Inuvik（加拿大）、Nemea（希腊）、Nuuk（格陵兰）、Bangalore（印度）、Tokyo（日本）、Port Louis（毛里求斯）、Awarua（新西兰）、Svalbard（挪威）、Vardø（挪威）、Panama（巴拿马）、Azores（葡萄牙）、Singapore（新加坡）（L137）。实验取排序后的前 $|G|$ 个，$2\le|G|\le18$，**流量负载固定 $\ell=0.85$**；作者说这个范围与负载"allow us to analyze very low load up to scenarios with high congestion"（L137）。
通信参数（L139）：发射功率**卫星 10 W / 网关 20 W**；载频**下行 20 GHz、上行 30 GHz、ISL 26 GHz**；抛物面天线**网关 33 cm、卫星 26 cm**；所有链路带宽 $W=$ **500 MHz**；包长 $B=$ **64.8 kbits**。
星上天线配置（L26）：1 副对地天线 + 4 副星间天线（2 副在 roll 轴两侧→同轨 ISL，2 副在 pitch 轴两侧→异轨 ISL），$|\mathcal{E}_i|\le4$，且 $\mathcal{E}_i$ **由文献 [3] 的算法动态更新**。
**负载轴的设计**：论文用"**活跃网关数 $|G|$**"而非"每网关速率"来扫负载（因为总负载 $\ell$ 固定为 0.85，增加网关数即增加总到达率）——这是一个干净的负载扫描设计。

**6. 它自己承认的局限**（三处，均以 future work 形式给出）
- L79 逐字："In the future, we will extend the space space and apply other advanced learning techniques to characterize the tradeoff between complexity of the learning algorithm and performance gain."
- L151 逐字（**明确承认 Q-routing 传播时延更差及其原因**）："The propagation latency with Q-routing is a bit larger than the other two in all cases. There are two reasons for this: (1) we include the exploration stage at the beginning of the simulation when the satellites are mostly trying random paths (see Fig. 5); (2) we use a simple encoding of the status of the link to limit the size of the state space."
- L164 逐字："Future work will look at the extension of the state space to DRL and the evaluation in scenarios with heterogeneous QoS requirements and policies."
（另可视为半自述的是 L15：作者批评文献 [7] 的模型，并声明自己与 [6][7] 的区别在于"考虑地面段拓扑及其与空间段的连通性，并在**每个 ISL 都有队列、且多个并发数据流互相影响**的现实设定下求解"。）

**7. 它没做但看起来能做的地方**（基于内容）
1. **负载只测了单点 $\ell=0.85$**（L137），全部扫描都走"活跃网关数"这一维。$\ell$ 本身（0.5/0.85/1.0）作为横轴从未被扫——而 $\ell$ 才是它自己定义的那个"归一化到达率"。
2. **2 bit 的状态编码是全文最小的那个旋钮，却没做消融**。作者自己说它是"传播时延略大"的原因之一（L151），但没试过 3 bit/更多档位来看能换回多少时延。这是现成的、代价极低的实验。
3. **$Q_j$（邻居 Q 表）的交换假设了"成功收到包"这一前提**（L133）——但**队列满就丢包**（L46）。丢包时反馈丢失、Q 表不更新，而拥塞时丢包最频繁——**恰好在最需要学习的时候学习信号消失**。论文完全没有讨论这个反馈回路的失效模式，也没报过丢包率。
4. **奖励里的 $r_{queue}=w_1(1-10^{t_q(j)})$ 是指数形式**（式 6），$t_q$ 单位是秒，$10^{t_q}$ 在 $t_q$ 略大时就会爆炸；$w_1,w_2$ 的取值全文未给，也没有量纲/稳定性讨论。
5. **两个基线都是集中式源路由**，而作者的卖点之一是"分布式、不经地面"（L5、L164）。**缺一个同级别的分布式基线**（例如 ELB 式的邻居拥塞通告），因此"分布式"的收益与"Q-learning"的收益是纠缠的、无法分离。
6. **$|G|>14$ 之后网络整体不可用**（L143），但从 14 到 18 的区间里 Q-routing 表现更差——作者只解释到"那时三者都不稳定"就停住了，没有进一步刻画拥塞崩溃的过程。
7. 时间尺度论证（L72）说"agent 在 <0.5 s 内学会新路径，远快于星座移动的分钟级尺度"，因此可以不处理拓扑变化与学习的时间尺度耦合。这个论证是**从结果反推的**（"As observed in the results"），且只对 140 颗星的规模成立，大规模星座下未被检验。

**8. 和同批其他篇的关系**
- **与 S85KQ4FC 的关系最关键**：S85KQ4FC 的核心论点是"DRL 逐包推理速度跟不上转发速度，决策队列会堆爆"，而本文是**表格型 Q-learning + 2 bit 状态**——状态空间极小、查表即得，**天然回避了推理开销问题**（作者正是以"limited computation capabilities"为理由做这个编码，L79）。两篇合起来给出一条重要对照：**"把学习问题做小"和"把推理成本当约束优化"是解决同一个瓶颈的两条不同路线**。
- **与 X5K285MW 的呼应**：X5K285MW 实测传播时延占比高、并发现"最小跳集合内逐流随机选路"就能大幅提升可承载负载；本文引文献 [4] 的 **100 ms 端到端、传播占 37%–66% 随负载变化**（L13），并进一步证明**连"已知全局瞬时队列状态"的 genie 源路由都不如分布式 Q-routing**（L143）——这实际上给出了"源路由为何注定次优"的机理解释（决策时刻与到达时刻的队列状态错配），比 X5K285MW 的"路径多样性"解释更深一层。
- **与 XM64YRAW 的对照**：XM64YRAW 也报"低负载时所有方案差不多、高负载时 GQN 优势放大"，但它的动作空间是**整条 k-最短路**（源路由式），而本文用 genie 实验直接论证**源路由式决策在长距离下是次优的**。两篇在"是否应该把决策下沉到每一跳"上给出相反方向的证据，值得并列。
- **与 XM6NUPM4 的对照**：XM6NUPM4 的"时延"是跳数约束（不含排队），本文的式 3 明确是"排队 + 传输 + 传播"三项，且实测传输项 < 0.72 ms 可忽略、排队项在高负载下主导——两篇对"时延到底由什么构成"给出了互补的粒度。
- **共享参考文献**：本文引 **DRL-ER（Liu, Zhao, Xin et al., [6], L178）**——该文同时出现在 **S85KQ4FC** 与 **XLRW7XXN** 的参考文献里，是三篇共同的基线。本文引 **Boyan & Littman 1993「Packet routing in dynamically changing networks」（[8], L182）** 作为 Q-routing 的方法祖先，这是本批唯一一篇明确接续 Q-routing 原始谱系的论文。

**9. 对"负载变化下到达率/时延"的贡献**（**本批目前最直接、最定量的一篇**）
它几乎就是围绕这条轴设计的：
1. **给出了"负载 → 时延主导项切换"的实证**：非拥塞时传播时延主导、拥塞时 ISL 排队时延主导（L5、L54），并进一步用 Fig 4 把三项分开画（L151）。结合文献 [4] 的"传播占比 37%–66% 随负载变化"（L13），可以得到一条清晰的叙事：**时延的构成比例本身是负载的函数**。
2. **用严格的统计判据（t 检验 + 回归斜率）定义了"拥塞拐点"**：不是看某条曲线翘起来，而是判定"端到端时延是否随时间显著增长"，$H_0:\beta_1\le0$、$\alpha=0.05$、最后 200 包（L141）。这是本批**唯一一个把"是否拥塞"形式化成可检验命题**的工作，可直接迁移到其他论文的评测里。
3. **量化了各方案的可承载负载差异**：data rate BM 从 **9 个活跃网关**起崩溃、latency genie BM 从 **8 个**、Q-routing 到 **14 个**才落后（L143）——即在"网络仍可用"的区间内，学习型分布式路由的容量比"已知全局队列状态的源路由"还高。
4. **一个反直觉的事实**：**掌握全局瞬时队列状态的 genie 反而比按速率选路的 BM 更早出现不稳定路径**（8 网关 vs 9 网关，L143）——说明"信息更多"不等于"决策更好"，源路由的决策时刻与执行时刻错配才是瓶颈。
5. **负载定义是可比的**：$\ell=\sum\lambda_{UL}^{(g)}/\lambda^*$，$\lambda^*$ 由 GSL 速率上限算出（L38）——这是一个归一化到"网络容量"的到达率，比同批其他论文用"数据包数"或未说明量纲的"总需求速率"更严谨。
**局限**：$\ell$ 固定 0.85 单点；**没有报丢包率**（而队列满丢包是模型的一部分，L46）；时延只报平均值，无尾分布。

**10. 一句话评价**
本批**方法学上最"小"却最锋利**的一篇：不发明新网络结构、不用 DQN、状态只有 2 bit/邻居，改动只有一处——**把 Q 更新的 bootstrap 目标从"自己的 Q"换成"邻居的 Q"**（式 8），以此显式建模"我的动作体现在邻居队列上"这一多智能体耦合；它同时给出了本批唯一的**形式化拥塞判据（回归斜率 t 检验）**、唯一的**归一化负载定义**（$\ell$ 相对网络容量）、以及一个杀伤力很强的对照实验——**连知道全局瞬时队列状态的源路由 genie 都不如它**。代价是负载只测单点、丢包未报、缺同级别的分布式基线；但作为"把 Q-routing 这条 1993 年的线认真接到 LEO 场景"的工作，它对"负载变化下到达率/时延"这一选题的参考价值高于本批任何一篇 DQN 论文。

## YD4JUT7G — Internet Backbones in Space（ACM SIGCOMM CCR 2020；Giacomo Giuliari, Tobias Klenze, Markus Legner, David Basin, Adrian Perrig, Ankit Singla @ ETH Zürich）

**1. 一句话**
一篇**跨域（inter-domain）路由的架构比较论文**：把"LEO 星座如何接入今天的 Internet 路由体系"拆成四条路线（白盒 BGP / 黑盒 BGP+地面冗余 WAN / CDN 式重路由 ReRo / 理想 PAN+路径控制 PaCo），用**轨道仿真 + BGP 事件计数 + 地面段成本模型 + NOAA 降雨数据**四条证据链比较它们的成本、稳定性与时延，结论是"CDN 式方案在平均意义上接近最优，且今天就能部署"。

**2. 问题设定**
LEO 星座承诺给长距离通信**低于地面光纤的时延**（真空光速 vs 光纤 2c/3，且避开绕行的光纤路由，L25、L53），但它天生与 Internet 路由不兼容。作者列出三个让 SN 无法对等体"隐藏"其物理层特性的因素（L27）：① 大气效应与卫星失效导致连通性时变；② 商业可行性要求**部分部署**，于是连通性按卫星临时可见性呈**间歇**状；③ 卫星传输**时延更低但成本更高**，需要能区分流量、主动决定何时走卫星。第二个矛盾是成本—性能权衡（L73）：卫星连通性带宽受限（稀缺资源）、价格更高，而**今天的 Internet 路由不支持实时通告变化的路径时延**，对等体无法据此选路。

**3. 方法骨架**（非 RL：架构设计与对照评估，四条路线）
- **① 白盒（White Box）**（§2.4）：SN 作为一个普通 AS（SN-AS）参与 BGP，GSL 的连通性变化对域间路由基础设施**完全透明**。作者用仿真量化其致命伤（见第 4 项）。
- **② 黑盒（Black Box）**（§3）：SN-AS 自建/租用**地面冗余 WAN** 互连各 GST，把 GSL 的抖动在域内吃掉，对外呈现稳定连通性。代价是全部地面段成本由 SN 独自承担。
- **③ CDN 式（ReRo）**（§5）：把 GST 类比 CDN 边缘节点——**宿主到合作 ISP 的网络里**（成本分摊，L155–157）；GST 之间持续交换 GSL 连通性/带宽/短期天气预报；**inactive 的 GST 把流量经地面网重路由到 active GST**（L159、L171）。源端用 DNS 或 IP anycast 找最近的 GST（L165）。方案命名为 **ReRo（re-routing）**。
- **④ 理想最优（PAN + PaCo）**（§4）：基于 **路径感知网络（PAN）**，具体用 **SCION** 实现（L137–143）。在控制面 PCB 里嵌入两类额外信息：**(i) connectivity profile**（GSL 连通性变化的表示，使路径无需反复通告/撤销，端主机用各 GST 的 profile 求交即可判断路径在任一时刻是否可用）；**(ii) time-varying bandwidth class**（由当地天气预报与 GST 可见卫星数算出，用来判断 SN 能否支撑所需带宽）（L141）。这叫**路径控制（PaCo）**。
- **时延模型**（§6.1、附录 A.2，L217–221）：源→GST 的地面段 = 大圆距离 × **地面绕行因子 2.3** ÷ (2c/3)；GST→GST 的卫星段 = 路径长度 ÷ **c（真空）**；三项相加。
- **仿真器**（附录 A.2）：自研。空间段按星座参数生成图并复现轨道运动；地面段 GST 之间用 **Delaunay 三角剖分**模拟相邻连接；GST 在卫星仰角超过**最低仰角（Starlink 取 40°）**时可建立 GSL（L416–418）。

**4. 它声称的效果**（分四条证据链）
- **① 白盒的 BGP 抖动量化**（Fig 1，L88）：在 **SpaceX 二期星座的 10% 部署**下仿真。卫星常常**只可见几分钟**；用**过滤阈值**滤掉过短窗口可减少路由更新，但被滤掉即产生**连通性浪费**。**即使阈值设到 6 分钟、大多数事件被滤掉，每个 GST 每天仍有近 20 个事件、每个至少触发一次 BGP 更新**——而代价是 **15%–45% 的可用连通性被浪费**。且每次断开会导致**至少一次、通常很多次** BGP 通告（多个 AS 的前缀在单个 GST 断开后全球不可达），两端都受同样的抖动影响，会触发路由抖动抑制（route flap damping）、使卫星路径被禁用（L90）。
- **② 黑盒的成本**（Table 1，L114–121）：单 GST 成本 = **基础设施 7 M$ + 天线 3 M$**（30 副天线 × 10 万$），WAN 造价 **10 k$/km**。样本结果（1000 次随机部署的平均）：100 个 GST → WAN 0.47 B$、总计 **1.5 B$**；500 → 2.3/7.3 B$；1000 → 4.6/**15 B$**；1833（GDP 采样）→ 8.5/**27 B$**；1833（全球所有 >30 万人口城市）→ 12/**30 B$**。对照：**整个 SpaceX Starlink 星座的估计成本约 100 亿美元**，而黑盒模型在此之上再加约一倍（L121）。
- **③ GST 选址的时延代价**（Fig 2，L225）：两种部署——"每个源城市一个 GST"（基线最优）vs "只在 IXP 部署 GST"。**经 IXP 路由的平均额外时延约 10 ms**；对长距离通信影响不大（空间段时延主导），但**当端到端时延本身很低时，这个增量在相对意义上很可观**。
- **④ 降雨衰减下的 ReRo vs PaCo**（Fig 3，L245）：用 **NOAA 2018 全年历史天气**，每天取两个时刻的降雨累积量，用 **11 个阈值**判定 GST 是否 inactive，得到 **7744 个仿真场景**（L236）。结果：PaCo 与 ReRo 的时延 **CDF 非常接近**，平均损失只有**几个百分点**；但**每个场景内的最大损失（Avg. maximum）可超过 30%**，**所有场景中的绝对最坏情况（Worst case）损失可超过 80%**。作者判断这些损失"可忽略"，因为单向时延本身很低、几毫秒的波动可接受（L245）。
- **汇总（Table 2 + §7）**：**PaCo 能在 95 分位上带来超过 10% 的平均改进**（L262）；白盒最易部署但极度脆弱；黑盒提升稳定性但成本成倍、且可扩展性差；CDN 式解决了可扩展性且平均近最优。
- **两个基线**：IXP 部署 vs 源城市部署（§6.1）；ReRo vs PaCo（§6.2）。PaCo 的搜索空间限制在**最近的 3 个 GST**，作者称仿真显示放开到更多 GST 收益迅速递减（L238）。

**5. 实验条件**
星座：**SpaceX Starlink 二期**，每星 **4 条 ISL**（2 同轨前后 + 2 异轨左右），与同批其他论文的四链路假设一致（L195）。BGP 抖动实验用该星座的 **10% 部署**（L86）。地理：源与目的从**人口 >30 万的城市**中按 UN 数据采样，因星座在极区无覆盖，**限制在 −56° 至 56° 纬度**，共 **1833 个城市**（L195）。IXP：从 Euro-IXP 数据集出发，初始 626 个 IXP，去重后得 **353 个唯一地点**（L211）。GST 选址启发式：按**单位面积 GDP** 的概率分布采样（L106）；WAN 造价只算到最近 IXP 且**剔除超过 1000 km 的连线与跨洋跳**（认为可租用现成光纤）（L108）。时延参数：地面绕行因子 2.3、光纤中光速 2c/3、真空中 c。**注意**：这是**非 RL 的架构研究**，没有训练/评估之分；其"动态"维度是**连通性抖动与降雨**，不是流量负载。

**6. 它自己承认的局限**（无正式 Limitations 小节，但有明确的 scope 声明）
- L106 逐字："The choice of the optimal placement of GSTs given cost and performance constraints is a hard problem, and is outside the scope of this article."
- L57 逐字："We omit further discussion of the direct-to-consumer scenario, as it is simple to implement from the perspective of Internet routing, and focus on an SN aiming to offer transit connectivity."
- L129 逐字："This raises the question of which entity will make the final decision on the choice of forwarding path. **We remain agnostic to this dilemma**."
- L272 逐字（明确指出本文不管域内路由）："Intra-domain satellite routing: Routing inside a satellite constellation is a well studied topic [...]. However, these works do not consider the effects that SNs have on the Internet as a whole."
- L110：成本模型"excludes equipment to light the fiber, support facilities and staff, management costs, and leasing prices for trans-oceanic fiber"，且更复杂的冗余拓扑"could increase this cost manifold"。

**7. 它没做但看起来能做的地方**（基于内容）
1. **时延模型里完全没有排队/拥塞**：卫星段时延 = 路径长度 ÷ c（L221），GSL 只做"可用/不可用"的二元判定。**带宽被当作用来筛掉不可用 GST 的准入门槛，而不是被争用的资源**——于是"路径控制的收益"只在**连通性**维度上被度量，在**负载**维度上完全空白。
2. **L71 那句关于负载的断言是全篇唯一（也是最有价值）的负载相关论断**："Augmenting the throughput between dynamically changing 'hot' end-points will require **non-shortest path routing, trading off some latency for bandwidth**"——但作者**没有做任何实验去量化这个 trade-off**（没有"多绕几跳能换来多少带宽"的曲线）。这是本文自己点出却未兑现的一个实验。
3. **GST 选址只用了 GDP 采样和"所有 >30 万人口城市"两种启发式**（L106、L119），作者自己说最优选址是 hard problem 且超出范围（L106），但**没试过任何贪心/优化基线**——而 Fig 2 已经显示选址对时延的敏感度不小（10 ms 平均差）。
4. **PaCo 只考虑最近 3 个 GST**（L238），且"收益递减"的判断来自未展示的仿真。若端到端时延低时相对损失很大（L225），那么"3 个够不够"应该按时延区间分层回答，而不是给一个全局结论。
5. **ReRo 的重路由只在 GST 层做**，但 §5.2 提到"GSL 拥塞时由负载均衡器把包重路由到附近 GST"（L171）——**这句一笔带过，没有任何拥塞场景的仿真**。这恰恰是"负载变化"进入本文框架的入口，但被略过了。
6. 降雨衰减只用了**降雨阈值**这一个致因（L236）。作者在 §2.3 里列了四个连通性抖动来源（卫星运动、雨衰、部分部署、ISL 带宽约束），但**只仿真了雨衰和部分部署两种**。
7. 成本模型排除了运营支出（L102 逐字："We disregard the recurring operational expenditure"），因此"黑盒成本翻倍"这个结论是**下界**；作者承认了，但没有给出上界区间。

**8. 和同批其他篇的关系**（**本文是本批的"共同祖先"之一**）
- **被同批两篇直接引用**：**X5K285MW** 的参考文献 **[8]** 就是本文（"Internet backbones in space, ACM SIGCOMM CCR 50, 1, 2020"，见 X5K285MW L143）；**XM6NUPM4** 的参考文献 **[17]** 也是本文（见 XM6NUPM4 L396）。两篇都把本文当作"LEO 网络架构"这条线的奠基引用。
- **与 X5K285MW 共享另两条关键文献**：本文引 **Handley 2018「Delay is Not an Option」（HotNets'18）** 为 [20]（L326），而 X5K285MW 引同一篇为 [10]（X5K285MW L147）；本文引 **Bhattacherjee et al. HotNets'18「Gearing up for the 21st century space race」** 为 [3]（L292），X5K285MW 引 **Bhattacherjee & Singla CoNEXT'19** 为 [2]（X5K285MW L131）——**同一作者群的姊妹篇**。**结论：X5K285MW、XM6NUPM4、YD4JUT7G 三篇构成一个紧密的引用三角。**
- **与 XM6NUPM4 共享 del Portillo 的成本/星座对比线**：本文 [7][8][9] 是 del Portillo 系列（L300–304），XM6NUPM4 的 [4] 引用的是同一篇 del Portillo 2019 Acta Astronautica（XM6NUPM4 L370）。
- **与 XM6NUPM4 的实质呼应**：XM6NUPM4 的核心是"最少需要多少颗卫星"（空间段成本），本文的核心是"地面段要花多少钱"（**Table 1b 显示地面段成本可与空间段同量级甚至更高**，L121）——两篇合起来才是 LEO 网络的总成本图景。
- **与 Y2H4NPLU 的对照**：Y2H4NPLU 是**域内逐跳**路由（分布式 Q-learning），本文明确把域内路由划到范围外（L272）；Y2H4NPLU 的一个核心卖点正是"不依赖地面段、信令开销最小"（Y2H4NPLU L5），而本文恰恰在讨论地面段（GST/WAN）的部署与成本——**两篇从"要不要地面段"这个角度互补**。
- **与 S85KQ4FC / XM64YRAW 的关系较远**：那两篇是域内逐包/逐路径的路由优化，本文是跨域架构选择，问题层次不同。

**9. 对"负载变化下到达率/时延"的贡献**
**没有直接贡献**——这是必须如实说的。本文的整条证据链中**没有任何一处扫描流量到达率**：其"动态"轴是 **GSL 连通性抖动**（部分部署）与 **降雨衰减**（天气），时延模型里连排队项都不存在（卫星段 = 路径长度/c，L221），带宽只作为"GST 是否可用"的门槛。因此它不能回答"到达率上升时延如何变化"。
**但它提供了三条对这一问题有支撑价值的事实**：
1. **带宽—时延权衡的存在性论断**（L71 逐字）："Augmenting the throughput between dynamically changing 'hot' end-points will require non-shortest path routing, trading off some latency for bandwidth." 这是**"热点端点的吞吐提升必须以时延为代价"**的明确表述，与 Y2H4NPLU 的"时延主导项随负载切换"、X5K285MW 的"路径多样性换吞吐"、XM64YRAW 的"负载均衡换传播时延"在方向上完全一致——四篇独立论文指向同一个结构性权衡。
2. **ISL 带宽预算的量化**（L71）：ISL 容量估计区间 **5–20 Gbps**。这是任何负载均衡/路由方案可用的**带宽总量级**——XM6NUPM4 采用的 20 Gbps 正落在这个区间上界。
3. **连通性抖动的时间尺度**（L88）：卫星对单个 GST 常常**只可见几分钟**，在 6 分钟过滤阈值下每 GST 每天仍有约 20 次连接—断开事件。这给出了"网络可用性的时间粒度"，是判断"负载变化需要多快被响应"的物理约束。
4. **雨衰的量级**（L67 逐字）："At these frequencies, atmospheric rain fade severely degrades radio communication, **reducing throughput by orders of magnitude**."——即**有效带宽可以在天气尺度上塌陷数个数量级**，这是比流量波动更剧烈的一种"负载—容量失配"来源。

**10. 一句话评价**
本批的**架构层基准文献**：它不提出路由算法，而是把"LEO 星座接入 Internet"这个问题框架化，并用一张**跨域稳定性（BGP 事件数）— 地面段成本（B 美元级）— 端到端时延（ReRo vs PaCo）**的三维权衡表证明"白盒最优部署点不存在、黑盒成本翻倍、CDN 式平均近最优"，因此它被同批的 X5K285MW 与 XM6NUPM4 双双引用并非偶然——**后两篇分别在"域内怎么选路"和"空间段要多少卫星"两个方向上展开，而本文回答的是"地面段怎么落地、代价多少"**。对"负载变化下的到达率/时延"这一问题，它的价值不在于数据而在两处论断：**带宽—时延权衡的存在性**（L71）与**有效带宽可因天气塌陷数个数量级**（L67），前者为整个选题提供了动机层面的引用支撑，后者提醒任何只考虑流量负载的模型都漏掉了一个更剧烈的扰动源。

## YI9G7NR7 — DQDRA: A Dyna-Q-Enhanced Distributed Routing Algorithm for Heterogeneous LEO Constellations（IEICE Trans. Fundamentals, LETTER, 2026）

**1. 一句话**
面向"通信星座 + 遥感星座"的**异构** LEO 网络：先用一个最优时间匹配算法建跨层链路（CLL），再用 **Dyna-Q**（模型 + 无模型混合）做**全分布式**逐跳路由，让每颗星只凭局部观测决定下一跳；实测在 $\ell=0.8/0.9$ 的高负载下时延与送达率都优于集中式与基线分布式方案。

**2. 问题设定**
遥感数据下行的三条既有路径都有硬伤（L23）：① **直连地面**——接触时间太短，紧急任务的传输机会严重受限；② **经 ISL 路由回地面站**——虽然摆脱了可见性约束，但**地面站附近的节点拥塞与受限的下行带宽通常导致缓冲溢出**（这是"负载 → 丢包"的直接陈述）；③ **GEO/MEO 中继**——受信道接入、星上存储与下行带宽限制。既有研究多聚焦单层星座（L27），少数跨层工作**依赖集中式路由**，而集中式需要实时收集全网资源使用信息，面临 "high computational overhead, long update cycles, and insufficient real-time performance"（L27）。

**3. 方法骨架**（RL：**表格型 Q-learning + Dyna-Q 模型增强**；另有非 RL 的链路匹配算法）
- **系统模型**（§2.1）：图 $G=(V,E)$，$E=\{E_{ISL},E_{CLL},E_{S2G}\}$，全部链路**双向**，不依赖地面站即可路由（L35）。速率式 1：$R(i,j)=W\frac{P_t(i)G_t(i)G_r(j)}{k_BT_SB\,L_{total}(i,j)}$；总路损式 2：$L_{total}=L_f L_a L_r L_c$（自由空间、气体吸收、雨衰、云衰）。**频率与衰减的处理有区分**：$E_{S2G}$ 工作在 **65 GHz**，按 ITU-R 标准（典型天气）建模气体/雨/云衰；ISL（**18 GHz**）与 CLL（**40 GHz**）因不经过对流层、大气衰减可忽略，只算自由空间路损（L52）。
- **可见性约束**（式 3–4，L59–66）：两颗卫星的视线角 $\theta_A\ge\beta_A$、$\theta_B\ge\beta_B$，其中 $\beta$ 是**视线与大气层相切的角度**——即显式排除穿过大气的视线。这比同批多数论文的"仰角阈值"更严格。
- **流量与队列**（§2.3）：每星 FIFO 缓冲上限 $Q_{max}$，**满则丢包**（L70）。定义**归一化网络负载** $\ell=\sum_{v_R\in V_R}\lambda^{(v_R)}/\lambda^{*}$，其中 $\lambda^{(v_R)}$ 是每颗遥感星的包生成率，$\lambda^{*}$ 是由 $E_{S2G}$ 速率算出的**最大可承载总负载**（L70）——与 **Y2H4NPLU** 的负载定义同构。
- **时延模型**（式 5，L80）：$L(i,j)=\frac{q_i\cdot B}{R(i,j)}+\frac{B}{R(i,j)}+\frac{\|ij\|}{c}$ = 排队 + 传输 + 传播。
- **① 最优时间匹配算法**（§3.1，**本文独有的贡献**）：先算 $v_i$ 产生的数据包所需传输时间 $T_i$；据轨道参数确定通信域 $C_i$（与 $v_i$ 相位差最小的轨道面内所有可见通信卫星）；算跨层接触时长 $\tau(i,j)$ 及最大者 $\tau_{max}(i)$。若 $\tau_{max}(i)\ge T_i$，**不选 $\tau_{max}$ 那颗**——因为 "Directly selecting the satellite offering $\tau_{max}(i)$ would, however, waste substantial CLL resources and degrade the overall cross-layer capacity"（L89）——而是选 **$i^{*}=\arg\min_{v_j\in C_i}\tau(i,j)$（式 6）**，即**满足传输需求的最短接触时长**，以最大化链路利用率并更均匀地分配流量。若 $\tau_{max}(i)<T_i$（所有 $v_j$ 的缓冲视为饱和），则改用**遥感层内的最短距离原则**选下一跳 $v_n$，并对其通信域 $C_n$ 重复该过程，直到找到通信域内存在满足时长要求的通信卫星的遥感上行星 $v_i^{up}$（L100）。
- **② DQDRA**（§3.2）：POMDP 四元组 $(S,A,P(s,a),R(s,a))$（L109）。**状态** $S_i=\{L_i,N_i\}$：$L_i$ = 包头取出的目的信息；$N_i$ = 链路质量与缓冲拥塞，**2 bit 编码**——"00" = 队列占用 0–20%（不拥塞）、"01" = 20–80%（轻载）、"10" = 80–100%（重载）、"11" = 链路不可用（L111）。**动作**：选下一跳（经 ISL 或 CLL 的邻居星，或通往地面站的链路）（L111）。**奖励**（式 7–9）：到达目的地给 $r_d$；进入环路给 $r_{loop}$；否则 $r_{queue}+r_{dist}$，其中 $r_{queue}=w_1(1-e^{t_q(j)})$、$r_{dist}=w_2\frac{\|id\|-\|jd\|+\|sd\|}{\|sd\|}$（L116–127）。
- **Dyna-Q**（L142）：在真实经验之外，用**已学到的模型**生成模拟经验——每步选一个曾访问过的状态 $s$、一个曾执行过的动作 $a$，由模型预测 $s'$ 与 $r$，再用这条模拟转移更新动作价值函数。
- **Q 更新**（式 10，L147）：$Q_i^{*}(s_t,a_t)=(1-\alpha)Q_i(s_t,a_t)+\alpha\left[r_t+\gamma\max_{a'}Q_j(s'_{t+1},a'_t)\right]$——**bootstrap 目标取的是邻居 $j$ 的 Q 表**。$\varepsilon$-greedy，$\varepsilon=0.1$（表 1）。
- 输出：路由表；每星自主决策，**不需要全局网络状态**（L15）。

**4. 它声称的效果**（本批**数值最具体**的一篇）
- **收敛**（Fig 5a，$\ell=0.8$，L158）：基线分布式方法需要 **240 个 episode** 才接近稳态，且收敛后仍有明显波动（作者判为 "insufficient learning of complex traffic dynamics"）；**DQDRA 在 episode 160 即稳定，比基线分布式快约 33%**。
- **负载扫描 $\ell=0.5\to0.9$**（Fig 5b/5c，L160）：**轻载（$\ell<0.6$）时三种算法都达到低时延且送达率 100%**。
  - $\ell=0.8$：DQDRA 平均 E2E 时延 **241 ms**，优于集中式 **266 ms** 与基线分布式 **256 ms**，分别改善 **9.4%** 与 **5.9%**；送达率 **98.6%**，分别高 **3.6%** 与 **6.8%**。
  - $\ell=0.9$：DQDRA 优势更明显，**时延降低 27.6% 与 18.6%**，**送达率提升 8.4% 与 15.0%**。
- **归因**（L160）：集中式 "assigns routes based on instantaneous link rates, causing load imbalance and excessive queuing delays"；基线分布式 "relies solely on real interaction samples, which leads to insufficient congestion avoidance capability and increased packet loss under heavy traffic"。
- **基线**（L156）：(a) **集中式**——边权 $w_{i,j}=1/R(i,j)$，全局 Dijkstra 最短路；(b) **基线分布式**——model-free RL，每星维护 Q 表，转发给 Q 值最高的邻居。
- **作者自述的权衡**（L162 逐字）："The proposed DQDRA trades increased algorithmic complexity for improved routing performance under high traffic loads. While this may lead to **marginal performance degradation in lightly loaded networks**, it enables significantly better scalability, adaptability, and latency reduction."

**5. 实验条件**
异构星座（L154）：**通信星座 1000 km / 倾角 60° : 1000/36/1**；**遥感星座 500 km / 倾角 75° : 300/15/1**（记法应为 总星数/轨道面数/相位因子）。表 1（L140）：卫星天线**半锥角 55°**；地面站**最低仰角 15°**；发射功率**卫星 20 W / 地面站 50 W**；载频 **ISL 18 GHz、CLL 40 GHz、S2G 65 GHz**；**流量负载 $\ell$ 从 0.5 到 0.9**；$\varepsilon=0.1$；**链路系统带宽 800 MHz**；**包长 64 kbit**。E2E 时延按式 5 计算；**送达率 = $p_{success}/p_{all}$**（L154）。集中式基线是全局 Dijkstra。
**转换缺陷**：Table 1 在 MinerU 中被串行（如 "Carrier Frequency of &1sL (GHz)" 实为 $E_{ISL}$、"Probability €" 实为 $\varepsilon$），LaTeX 符号丢失；正文 L52 引用 **ITU-R 标准为文献 [13]**，但**参考文献列表在 MD 里只到 [12]**（L194），[13] 的条目缺失。

**6. 它自己承认的局限**
- L162 逐字（**唯一的性能相关自述**）："While this may lead to marginal performance degradation in lightly loaded networks, it enables significantly better scalability, adaptability, and latency reduction in heterogeneous LEO constellations."
- L166 逐字（结论段 future work）："Future work will focus on ensuring QoS under link failure scenarios."
- 全文仅 6 页 LETTER，**没有 Limitations 小节**；也未讨论 $w_1,w_2,\alpha,\gamma,Q_{max}$、缓冲容量的取值。

**7. 它没做但看起来能做的地方**（基于内容）
1. **$w_1,w_2,\alpha,\gamma,Q_{max}$ 全部未给**（表 1 只给了 $\varepsilon$），而 $r_{queue}=w_1(1-e^{t_q(j)})$ 里的 $e^{t_q}$ 对 $t_q$ 极其敏感——**这一项的标定直接决定拥塞规避的强度**，不给值等于不可复现。
2. **"轻载时 DQDRA 反而略有退化"被作者承认但从未量化**（L162 只说 marginal）。既然实验已经扫了 $\ell=0.5$ 到 0.9，把 $\ell<0.6$ 区间的三条曲线数值列出来就能回答"退化多少"——这是现成的。
3. **送达率只在 $\ell\ge0.8$ 给出数值**（98.6%），轻载区只说 100%；而**丢包机理（缓冲满 vs 环路 vs 链路不可用）没有分解**。
4. **时间匹配算法的收益没有被单独消融**：Fig 5 的对比是"DQDRA vs 集中式 vs 基线分布式"，三者都跑在同一个 CLL 建立策略下，因此**最优时间匹配（式 6）本身贡献了多少**完全未知。
5. **式 5 的排队项与文字自相矛盾**：正文说 "the packets ahead of it in the queue may be addressed to other nodes and therefore traverse different outgoing links, each potentially offering a different rate $R(i,\cdot)$"（L77），但公式里排队项写的是 $\frac{q_i\cdot B}{R(i,j)}$——用的是**当前包那条链路的速率**，与文字描述的 $R(i,\cdot)$ 不符（Y2H4NPLU 的对应式 3 用的正是 $R(i,\cdot)$）。
6. **Dyna-Q 的模型形式从未说明**：是查表型确定性模型还是概率模型？每步做多少次模拟更新（planning steps $n$）？这是 Dyna-Q 的核心超参，全文未提。
7. **只做了"平稳网络条件"（stationary network conditions，L160）**——作者自己用了这个词，却没有做非平稳（流量突变）实验，而"动态适应性"正是它批评集中式时用的理由（L27）。

**8. 和同批其他篇的关系**
- **与 Y2H4NPLU 高度同源（本批最值得注意的一处重合）**：两篇的**状态定义完全相同**（$S_i=\{L_i,N_i\}$，$L_i$ = 包头目的信息，$N_i$ = 邻居状态**2 bit 编码**）、**奖励结构完全相同**（三段式：$r_{del}$ / $r_{loop}$ / $r_{queue}+r_{dist}$，且 $r_{dist}=w_2\frac{\|id\|-\|jd\|+\|sd\|}{\|sd\|}$ 逐字符相同）、**Q 更新式的形式完全相同**（bootstrap 目标取**邻居 $j$ 的 Q 表** $Q_j$）、**负载定义同构**（$\ell=\sum\lambda/\lambda^{*}$，$\lambda^{*}$ 由星地链路速率算出）、**时延三段分解相同**（排队+传输+传播）、**也都用 $\varepsilon$-greedy 且 $\varepsilon=0.1$**。差别在于：本文是 **Dyna-Q（加模型模拟经验）**、面向**异构双星座 + CLL**、状态编码是**四个队列占用档位**（Y2H4NPLU 是"高/低容量 + 长队列"三档）、并多了一个时间匹配算法。**事实记录**：YI9G7NR7 的参考文献列表（L170–194，[1]–[12]）中**没有出现 Soret / Leyva-Mayorga 等的 Q-learning for distributed routing 一文**；我不对其成因下判断，仅提示主控核对——这可能是同一研究脉络的延续、也可能是引注遗漏，需要在主控层面确认。
- **与 X5Z98UPM / XLRW7XXN / XM64YRAW 的关系**：同属"RL 做 LEO 路由"，但本文是**表格型 Q-learning**（非 DQN），且是唯一处理**异构双星座 + 跨层链路（CLL）**的；XLRW7XXN 与 X5Z98UPM 都是单层同构星座、四邻居动作空间。本文的**动作空间**（ISL/CLL/星地链路三选）也与它们不同。
- **与 X2FCSU4S 的对照**：X2FCSU4S 用 **GEO 缓存**卸载 LEO 拥塞；本文用**通信星座的 CLL** 卸载遥感星座的拥塞——两者都是"把拥塞节点的数据搬到另一层"，但一个是存储卸载 + 博弈定价，一个是链路卸载 + RL 路由。
- **与 YD4JUT7G 的对照**：YD4JUT7G 明确指出高频段**雨衰可使吞吐塌陷数个数量级**（YD4JUT7G L67）；本文在 65 GHz 的 $E_{S2G}$ 上确实按 ITU-R 建模了气体/雨/云衰（L52），**是本批唯一把雨衰写进链路速率公式的路由论文**——两者在这点上互相印证。
- **引用**：本文引 **Wang et al.「Optimization for dynamic laser ISL scheduling with routing: A MADRL approach」（[8], L184）**，即"激光 ISL 调度 + 路由"的多智能体 DRL 方向；引 **Markovitz & Segal「Advanced routing algorithms for low orbit satellite constellations」（[12], L194）** 作为集中式路由的代表。

**9. 对"负载变化下到达率/时延"的贡献**（**本批数值最具体、且带送达率的负载扫描**）
1. **给出了完整的"负载 → 时延 + 送达率"双曲线**，负载轴是**归一化到网络容量的** $\ell\in[0.5,0.9]$（L70、L140），这是本批**唯一同时给出时延绝对值（ms）与送达率绝对值（%）随负载变化**的论文（L160）。
2. **明确了"轻载无差别区"的边界**：**$\ell<0.6$ 时三种算法都是低时延 + 100% 送达率**（L160 逐字："For light traffic loads ($\ell<0.6$) all algorithms achieve low E2E latency with a 100% delivery success rate"）——这是本批第四次独立观测到同一现象（XLRW7XXN「网络空闲时三种算法差别不大」、XM64YRAW「低负载时 GQN 相对 SP 无明显优势」、X5K285MW「闲置网络下时延差异不显著」），**四次独立观测指向同一结论：负载感知路由的收益是负载的函数，且在低负载区趋近于零**。
3. **量化了收益随负载的增长斜率**：$\ell=0.8$ 时时延优势 9.4%/5.9%，到 $\ell=0.9$ 时放大到 27.6%/18.6%（L160）——**负载从 0.8 涨到 0.9，优势翻了三倍**，这是"负载感知路由收益具有强非线性"的一个可直接引用的数据点。
4. **送达率的负载敏感性也随算法而异**：$\ell=0.8$ 时 DQDRA 98.6%，比集中式高 3.6%、比基线分布式高 6.8%；$\ell=0.9$ 时优势扩大到 8.4% 与 15.0%（L160）——**基线在拥塞下的丢包增长明显更快**。
5. **给出"学习曲线"的负载依赖**：收敛 episode 数在最难的 $\ell=0.8$ 下，DQDRA 160 vs 基线分布式 240（L158）。
**局限**：① 只扫了**平稳**流量（作者自述 "under stationary network conditions"，L160），没有突变/非平稳负载；② 负载离散取 0.5–0.9，**曲线上的点数与取值间隔未给**；③ 送达率未做丢包机理分解；④ 时延只报平均值，无尾分布。

**10. 一句话评价**
一篇 6 页 LETTER，**方法增量非常明确**——把 Y2H4NPLU 那条"分布式 Q-routing"的骨架（同一套状态/奖励/邻居 Q 更新）搬到**异构双星座 + 跨层链路**上，并把 model-free 的 Q-learning 换成 **Dyna-Q**（用学到的模型生成模拟经验以加速策略改进，实测收敛快 33%），外加一个**"选满足需求的最短接触时长而非最长"**的时间匹配算法（式 6）——后者的动机（不浪费 CLL 资源、更均匀分配）是本文最有原创性的一点。它的实验是本批**对"负载变化下时延/送达率"贡献最直接**的一篇：给出 $\ell$ 从 0.5 到 0.9 的绝对时延与送达率，并第四次独立复现了"低负载区算法无差别"这一现象。**最需要主控注意的是**：它与 Y2H4NPLU 在状态、奖励、Q 更新、负载定义四处几乎逐式相同而参考文献中未引该文，以及 $w_1,w_2,\alpha,\gamma,Q_{max}$、Dyna-Q 规划步数、[13] 条目等**复现所必需的参数大面积缺失**。

## Z74SR656 — Evolution of Non-Terrestrial Networks From 5G to 6G: A Survey（IEEE COMST 2022; Azari, Solanki, Chatzinotas, Kodheli, Sallouha, Colpaert, Mendoza Montoya, Pollin, Haqiqatnejad, Mostaani, Lagunas, Ottersten）

**1. 一句话**
一篇 1293 行的**综述**（非研究论文）：把 **NTN（非地面网络 = 卫星 + HAP + UAV）** 从 5G 到 6G 的演进按"5G 集成 → mmWave → IoT → MEC → ML → 高层协议 → 外场试验 → 6G 架构/使能技术"九条线全面梳理，**LEO 路由只是其中很小的一块**。

**2. 问题设定**
地面基础设施在偏远/不可达区域（农村、沙漠、海洋）部署不经济或不可能，导致 UE 无法接入（L29）。NTN 与地面网结合可提供连续泛在覆盖并增强容量、覆盖与时延，同时弥补地面设施在可靠性与广域存在性上的短板（L29）。3GPP 已把卫星接入纳入 5G 研究项（L31）。作者要回答的是：**NTN 在 5G/6G 中扮演什么角色、有哪些架构选项、技术使能与未解挑战**。

**3. 方法骨架**（综述，无算法；以下为它梳理出的分类框架）
- **NTN 定义与分类**（§II.A1）：空间段 = GEO（35786 km，波束足迹 200–3500 km）、MEO（7000–25000 km）、LEO（**300–1500 km**，足迹 100–1000 km）；空中段 = HAP（20 km）、UAV（数百米）（L67–69）。
- **四种集成架构**（§II.A2，Fig 1）：① **NT 平台作为用户**（被地面网服务，或高空卫星服务低空平台）；② **NT 平台作为中继**（回传中继 / 终端接入中继，透明载荷即可）；③ **NT 平台作为基站**（再生载荷 + 星上处理）；④ **混合架构**（如上组合）（L76–82）。
- **TN 与 NTN 的技术对比**（Table III，L107）：覆盖 100 km vs 3500 km；**传播时延 ≤0.67 ms（100 km 小区）vs ≤540 ms（GEO 透明载荷）**；路损 ≈138 dB vs ≈190 dB（均 2 GHz）；多普勒 ≈1 kHz（高铁）vs **≈48 kHz（600 km LEO，2 GHz）**；切换：用户移动触发 vs **NGSO 卫星运动导致的周期性切换**。另：GEO 往返时延可达 **270 ms**（L99）。
- **九大章节结构**（L57）：II 5G 集成 → III mmWave → IV IoT → V MEC → VI ML → VII 高层进展 → VIII 外场试验与产业 → IX 6G → X 结论。每章末尾都有 **Key Takeaways** 小节（本文最有信息量的部分）。
- ML 章（§VI）把应用分为**卫星网**（资源分配、波束跳变、IoT、MEC、切换与干扰管理、信道建模）与 **UAV 网**（3D 布放与轨迹、切换与干扰、mmWave、IoT、MEC、信道建模）与**多段网**（L324–375），并有 Table VII 汇总"ML 技术 ↔ 应用 ↔ 文献"（L377）。

**4. 它声称的效果**（综述的"效果"= 它汇总的事实与判断）
- 对 **ML 中的 RL**：明确指出 RL 应用的**主要顾虑是训练阶段的性能很差**，并预测会出现"限制 RL 智能体在探索阶段的不良表现"这一新研究方向，点名 **safe RL / batch RL / off-policy RL** 三条线（L320 逐字："One of the main concerns is **the poor performance of the RL during the training phase**. Accordingly, it is projected to have a new line of applied research where the focus is limiting the bad performance of the RL agent within the exploration phase [278], [279]. Towards this goal, the available literature on safe RL [280], batch RL [281], [282] and off-policy RL [283], [284] are of enough significance meriting special attention."）。
- 对 **多智能体 RL 的一条尖锐批评**（L365 逐字）："The benefit of multiagent MEC system presented in [256] is based on an assumption that **all the edge nodes can perfectly communicate to each other during the training phase**. In many practical cases, such assumption rarely occurs due to imperfect communications among the edge nodes and the highly dynamic network topology."
- 对**卫星 MEC 的量化结论**（L279，转述文献 [161] Kim & Choi）：该分析基于无向图星座模型，**同时考虑传播时延与排队时延、上下行误包率**，考察"平均总时延与抖动"随**收发地面间距、不同卫星高度、卸载率**的变化，结论是 **"latency decreases with the offloading rate while it increases with altitude"**（时延随卸载率下降、随高度上升）。
- 对**波束跳变（Beam Hopping）**（L330 逐字）："In a conventional satellite network, there might exist **a mismatch between requested traffic and offered capacity through the satellite beams**. Beam hopping technique is a promising solution for this issue to manage **asymmetric and variant traffic demands**." 并指出文献 [209] 把照度规划建成 **POMDP 并用 DRL 求解**，且计入了**波束间干扰与流量的时空特征**。
- 对**TCP 与时延/拥塞的相互作用**（L397 逐字）："general TCP protocol was not conceived to work on long-propagation links... **TCP may interpret the long-delay of a packet as a loss event and consider that the link is congested**." 对策是 PEP（性能增强代理，做"TCP 分裂"），但 PEP 会因 spoofing/splitting **破坏 TCP 语义**、引起互操作问题。
- 对 **NGSO 的 NGSO 网关/空中链路路由**（L399 逐字）：主要研究挑战是"the need for **onboard routing and network management mechanisms capable of dealing with the motion of NGSO aerial systems, together with the non-uniformly congested and dynamic network traffic with different QoS classes**"。
- 对 **6G 高度分布式 RAN**（L510 逐字）："As the latency requirements becomes more critical and **the amount of traffic does not cease to increase**, the cloud-RAN architecture **suffers from congestion caused by the fact that a substantial amount of data has to go through the core**." 并主张"each node is expected to **intelligently route the data packets to the suitable network slice** according to its requirements. The latter is only possible if **each node is aware of the network status**"。
- 对 NTN 的整体定位（L134）：NTN 的互补作用是"**offloading an important part of the traffic especially in highly congested areas**"。

**5. 它的实验条件**
**综述无实验**。它汇总的参考文献规模为 **[1]–[385]**（L524–1293）。来源覆盖 3GPP 标准（TR 22.822、TR 38.811、TR 22.829、TR 36.777、TR 38.821、TS 22.125、TS 38.104、TS 24.502 等）、IEEE 期刊/会议、arXiv 预印本、ITU-R WRC-15/19 决议、厂商与项目网页（Viasat、HughesNet、OneWeb、Starlink、Kuiper、Facebook、Google Loon、Nokia、Ericsson、Qualcomm、Vodafone、SES O3b mPOWER、5G-VINNI、5G METEORS、SAT5G、5GENESIS、5G ALLSTAR、5GDrones、SATis5、EdgeSAT、CLOUDSAT、5G-GOA、5GDIVE、SATAI、MLSAT、ATRIA 等）。文献分类表（Table I，L37）列出与既有 8 篇综述/教程的覆盖度对比（√ 覆盖 / ∂ 部分覆盖）。

**6. 它自己承认的局限**
综述没有"本文方法的局限"一节；它的自述属于**对领域的未解问题的声明**，须区分：
- L432 逐字（对 NTN-TN 集成）："Despite the benefits of NTN, there are several challenges which are needed to be addressed for the seamless integration of NTN with TN. For instance, **channel modelling incorporating the Doppler effects, admission control by satellites, storage limitations in air and space, flexible addressing and routing, mobility and constellation management, and spectrum co-existence** are some of the crucial design challenges."
- L200 逐字（mmWave 多段网络）："due to **limited literature in this domain**, additional studies are required to fully understand the behaviour of mmWave links integrated into multi-segment networks."
- L320 逐字（对 RL 领域）："the poor performance of the RL during the training phase"（见第 4 项）。
- L365（对既有 MARL 假设的批评，见第 4 项）。
- L499 逐字（6G 软件定义卫星）："This opens up **new development scenarios for architectures, protocols, traffic routing schemes, etc.**, that meet these new demands."

**7. 它没做但看起来能做的地方**（基于内容）
1. **L279 那条"时延随卸载率下降、随高度上升"的结论是以单句转述出现的**（文献 [161]），综述**没有给出该结论的数值、拓扑或负载范围**。既然综述的目的就是把分散结论汇总，这条与本选题最相关的量化事实被压缩成了一句话——若要追溯必须去读 [161] 原文。
2. **"排队时延"在整篇综述里只出现极少数几次**（L279 是主要的一次）。占据大量篇幅的是传播时延、多普勒、波束成形、轨迹优化，**"负载 → 排队 → 时延"这条链在综述层面基本是缺位的**。
3. **L320 提出的 safe/batch/off-policy RL 三条线是一个现成的研究缺口清单**：作者说"需要专门关注"，但没有进一步指出在 NTN 场景下这三条线各自对应什么问题（例如"训练期性能差"在卫星上意味着什么代价）。这是一个可以直接接续的方向。
4. **L365 对 MARL 的批评（训练期假设节点间完美通信）与 LEO 多智能体路由直接相关**，但综述只在 MEC 语境下提了一次，**没有把这个批评迁移到星座路由的 MARL 工作中去检查**。
5. **L397 的 TCP/拥塞误判问题**（长传播时延被 TCP 误判为丢包/拥塞）在 LEO 路由里同样成立，但综述把它放在"高层协议"章，**与路由章的讨论彼此隔离**。
6. Table III 的对比里 **"Handovers"一行只写了触发原因（周期 vs 用户移动），没有给切换频率或切换中断时长**——而 YD4JUT7G 用"每 GST 每天约 20 次连接—断开事件"给出了这个粒度，两篇可以互补。
7. 综述**没有覆盖跨域路由/域间路由**这一层（YD4JUT7G 的主题），其路由讨论停留在"必须有星上路由与网络管理机制"这类断言（L399）。

**8. 和同批其他篇的关系**
- **与 YD4JUT7G 直接衔接**：YD4JUT7G 正是"LEO 星座如何接入地面 Internet 路由体系（跨域）"的架构研究，而本综述在 L399 只把"星上路由与网络管理机制应对 NGSO 运动 + 非均匀拥塞的动态流量"（逐字见第 4 项）列为待解挑战——**本综述提出问题，YD4JUT7G 是一篇具体回答**。
- **与 YI9G7NR7 的关系**：YI9G7NR7 处理的是"通信星座 + 遥感星座"的跨层链路与分布式路由，属于本综述 §IX.B2 **Multi-Segment 3D Networks** 与 §IX.B4 **Mega LEO Constellation** 两条 6G 架构线（L463、L467）下的具体工作。
- **与 X5K285MW / XM6NUPM4 的关系**：本综述 §IX.B4「Mega LEO Constellation」与 §VI.B「ML-Empowered Satellite Networks」为这两篇提供了背景框架，但两篇都未引用本综述（X5K285MW 与 XM6NUPM4 的参考文献里没有 COMST 2022 这篇）。**本综述可作为它们的上位背景引用**。
- **与 X2FCSU4S / X5Z98UPM 的关系**：X2FCSU4S 的多层 GEO/LEO 缓存卸载对应本综述 §II.A2 的"NT 平台作为中继/基站"架构分类；X5Z98UPM 标题里的 SAGIN 对应本综述的 GAS（ground-air-space）术语体系。
- **本综述引用的、与同批直接相关的文献**：**[190] Sutton & Barto《Reinforcement Learning: An Introduction》**（L902，RL 的教科书根基；本批原分配中被主控裁掉的 LJG6ZW7B 正是该书）；**[192] Mnih et al. Nature 2015（DQN 原始论文）**（L906）——**X5Z98UPM、XLRW7XXN、XM64YRAW 三篇都用 DQN 却没有一篇引它，本综述是这三篇共同的方法祖先索引**；**[193] Lillicrap et al. DDPG**（L908，X5Z98UPM 引其 [40]）；**[194] Feriani & Hossain 单/多智能体 DRL 综述**（L910）；**[210] Wang et al.「Reinforcement learning based congestion control」**（L942）——**这是本综述里与本选题最贴近的一条 RL 工作**；**[304] Chen, Giambene, Yang, Fan, Chen「Analysis of inter-satellite link ...」**（L1130）；**[378] Jiang, Cui, Liu, Wang, Liu, Chen「Cooperative relay assisted ...」**（L1278）——该文与 **X2FCSU4S 的参考文献 [3] 是同一篇**（X2FCSU4S L764："L. Jiang, G. Cui, S. Liu, W. Wang, D. Liu, and Y. Chen, Cooperative relay assisted load balancing scheme based on stackelberg game for hybrid GEO-LEO satellite network"）——**这是本批两篇之间由第三方文献建立的实际连接**。

**9. 对"负载变化下到达率/时延"的贡献**
**贡献稀薄，但有几条可引用的断言**。必须如实说：这是一篇覆盖 NTN 全领域的综述，**负载与排队时延不是它的组织线索**，"arrival rate""queueing"在全文中的出现密度极低。它对该选题的可用事实只有四条：
1. **唯一一条定量关系**（L279，转述自文献 [161]）：卫星 MEC 场景下，**平均总时延随卸载率（可读作到达/卸载负载）上升而下降、随卫星高度上升而上升**，且该分析**同时计入了传播时延与排队时延**——方向与时延分量的处理都与本选题一致，但它是二阶转述，需回溯原文。
2. **"请求流量与卫星波束供给容量之间的失配"**（L330）是一个明确的负载—容量失配陈述，并把波束跳变作为对策、把 DRL+POMDP 作为解法——这是与本批 RL 路由工作同构的另一条负载自适应技术线。
3. **"NTN 的互补角色是在高度拥塞区域卸载相当一部分流量"**（L134）与 **"流量持续增长导致 C-RAN 因大量数据必须穿过核心网而拥塞"**（L510）——两条都是"拥塞驱动架构选择"的动机陈述。
4. **TCP 把长传播时延误判为丢包/拥塞**（L397）——这提醒：在 LEO 场景中，**时延与"拥塞"信号本身会互相污染**，任何用"时延上升"做拥塞判据的方法（例如 Y2H4NPLU 的 t 检验）都必须处理这个混淆。
**总结：直接贡献 ≈ 无；间接价值在于它给出了这四条断言 + 一份把 385 篇文献按主题编排的索引，可用于给本选题做上位背景与"哪些子领域已经成熟、哪些还是空白（如排队时延、safe RL、MARL 通信假设）"的定位。**

**10. 一句话评价**
一篇高质量的**领域地图**而非方法贡献：它把 NTN 从 5G 到 6G 的架构、频谱（mmWave/THz）、垂直行业（IoT/MEC）、使能技术（ML/IRS/QUIC/软件定义卫星/量子）与外场试验铺陈得非常完整，**Table III 的 TN/NTN 技术对比与各章 Key Takeaways 是它最有复用价值的部分**；但对"LEO 路由在负载变化下的到达率/时延"这个问题，它**主要是背景与索引**——唯一的量化关系（时延随卸载率下降、随高度上升）还是转述别人的；不过它对 **RL 训练期性能差**（建议 safe/batch/off-policy RL）与 **MARL 依赖"训练期节点间完美通信"这一不现实假设**的两条批评，恰好命中了本批多篇 LEO MARL/DRL 路由论文共同的软肋。

## ZIUBKVPZ — Routing in Low Earth Orbit Satellite Networks: Constrained DQN-based Approach（Hegde, Roth, Bischl @ DLR）

**1. 一句话**
把 LEO mesh 路由写成**受约束 MDP（CMDP）**，用 **C-DQN** 通过"只让 agent 在预先生成好的**安全路径集合**（k-最短路 ∪ k-简单路）内探索"来实现安全探索，从而在**跳数与链路负载两个约束**下算出既无环路又避开拥塞的路径，并讨论链路失效下的鲁棒性、复杂度与可扩展性。

**2. 问题设定**
摘要（L7 逐字）："The complexity of routing in LEO satellite networks is increasing due to **higher traffic loads**, complex network architectures and their integration with the terrestrial networks. The **time varying satellite network topology, intersatellite link failures and the necessity to satisfy diverse quality of service requirements** demands the need to investigate routing algorithms that can fulfill **multiple objectives**." 对既有源路由的具体批评（L15 逐字）：Dijkstra/A* 等**不考虑路径上各条链路的个体负载**（引文献 [2]，即作者自己团队的 Roth et al. 2022），"A major drawback of these algorithms is that they are **particularly susceptible to link congestion arising from hotspots**." 而多约束多目标路由是 **NP-hard**，经典优化方法需要在每次迭代中遍历所有状态，在大规模 SCN 上计算代价高昂（L17）。此外作者指出 DQN 的一个根本问题（L21）：单纯调奖励函数**无法**在所有拓扑与链路失效情形下保证最优结果；而只在动作选择时屏蔽不安全动作（action masking）、**不改 Q 更新**，虽能短期选到更安全的动作，但当出现路由环路时**仍会违反约束**。

**3. 方法骨架**（RL：DQN + 预计算安全集约束；**集中式**）
- **CMDP**（L27）：$<S,\mathcal{A},\mathcal{P},\mathcal{R},\gamma>$ → 加入约束集 $\mathcal{C}=\{C_k: S\times A\to\mathcal{R}\mid 1\le k\le C_N\}$ 后变为 $<S,\mathcal{A},\mathcal{P},\mathcal{R},\gamma,\mathcal{C}>$。
- **状态**（L34）：全局状态 $S$ 含**活跃卫星节点总数 V、与邻居的链路连接情况、以及各条链路的个体负载**。数学上表示为双向图 $G=(V,E)$（$E$ 为 ISL），$V$ 个卫星节点以 **$X\times Y$ mesh 网格**分布在特定轨道面内；连通性用**邻接矩阵** $A_{i,j}$ 描述；**个体链路负载表示成二维向量 $U_{e_{i,j}}$**。
- **动作**（L36）：每个卫星节点一个**有限动作空间**，对应其四条 ISL 的四个方向 **[E, W, N, S]**；某方向链路不存在或不活跃则置 0；最多四条 ISL ⇒ 最多四个动作。作者特别说明这样做的理由是"链路连接状态动态变化，使输出层难以处理**变长动作空间**"（L36）。
- **安全动作集**（式 1，L41）：$\mathcal{A}_{c_k}=\{a\in\mathcal{A}\mid c_k(s_t,a)\le P_n\}$，其中 $P_n$ 是 n 个顶点之间**所有安全路由路径的集合**。两类安全探索：① 只探索 **k-最短路**上的节点；② 探索**不形成路由环路的一条或多条简单路**上的节点。两者都保证充分探索同时给出**无环的有效路径**（L44）。
- **后端规则算法**（L46）：在后台跑**规则型源路由 Dijkstra**，周期性计算并更新源-目的对 $(s,d)$ 之间的 **k-最短路集 $P^s_{k,s-d}$** 与 **k-简单路集 $P^{si}_{k,s-d}$**，安全探索集 $P_n=\{P^s_{k,s-d},P^{si}_{k,s-d}\}$。**即 RL 与规则算法是耦合的：规则算法负责给出可行路径的"护栏"，RL 负责在护栏内做逐跳决策以绕开拥塞链路。**
- **安全状态集**（式 2）：$S_{c_k}=\{a\in A_{c_k}\mid(s_t,a)\}$。
- **Q 更新**（式 3）：$Q^{c}(s_t,a_t)\gets Q^{c}(s_t,a_t)+\alpha\left(r+\gamma\max_{a\in\mathcal{A}_{c_k}}Q^{c}(s_{t+1},a_{t+1})-Q^{c}(s_t,a_t)\right)$——**注意 $\max$ 是在受限动作集 $\mathcal{A}_{c_k}$ 上取的**，这就是"约束进入 Q 更新"的具体做法。策略式 4：$\pi^{*}(s_t)=\arg\max Q^{c}(s_t,a)$。
- **奖励**（式 5，L69–96）：分段式，$r_t(a_t|s_t)=$
  - $B$：走**最短路**且 $U_{e,i,j}<0.5$（最好奖励）；
  - $B-\psi$：走**简单路**且 $U<0.5$（$\psi$ 是相对最短路的**距离惩罚**）；
  - $B-\sum_{x=1}^{L}x\,v_i$：形成**路由环路**且 $0.4<U<0.8$（$L$ 是在节点 $v_i$ 上形成的环路数，$x v_i$ 项随环路累积）；
  - $-(B-\sum_{x=1}^{L}x v_i-c)$：**既有环路又触发约束违反（CV）**且 $U>0.8$（$c$ 表示约束违反）；
  - $0$：其他一切情形（即在中间节点移动**不给任何奖励**）。
  链路负载的分档阈值：**舒适 $U<0.5$、拥挤 $U>0.8$、环路场景落在 $0.4<U<0.8$**。作者指出约束违反最典型的场景是"多条链路拥塞（$U>0.8$）迫使 agent 走已走过的路径（四个方向都被探索过）"，以及**卫星经过极区时只有两条同轨 ISL 可用**（L96）。
- **Algorithm 1**（L74–94）：先**抽取有效动作空间 $\mathcal{A}_{c_k}$ 与安全状态 $S_{c_k}$**；$\varepsilon$-greedy 选动作；**若下一状态等于上一状态，则改选另一个有效动作 $a'_t$ 并存储**；然后按 mini-batch 计算 MSE 损失、更新目标网络。**"如果回到上一状态就换动作"是对环路的一层显式硬拦截。**
- 参数（Table I，L103）：前馈网络，**2 个隐藏层 × 128 神经元**；学习率 $\alpha$ = **0.001（DQN）/ 0.007（C-DQN）**；折扣 $\gamma$ = **0.99（DQN）/ 0.9（C-DQN）**；$\varepsilon=0.5$；buffer 300；batch 50；目标网络更新频率 100；优化器 **RMSProp**；损失 MSE；**600 episodes、每 episode 10 epochs**；**"Learning and decisions: Centralized"**。

**4. 它声称的效果**
- **路径计算（Fig 2，L137–142）**：**传统 DQN 在 $\varepsilon$-greedy 探索下"环路不可避免"**，作者给出实例——从节点 0 到节点 11，在节点 1 处**所有可能的动作都形成环路**：$[0,1(N),5,6,2,1]$、$[0,1(E),2,6,5,1]$、$[0,1(S),9,5,6,2,1]$、$[0,1(W),0]$，**原因是节点 1 的四条 ISL 负载完全相同，agent 认为选哪个动作都等价**。修正节点 1 的环路后又在节点 5 等处形成环路，直到节点 1 的动作空间被穷尽、**全部结果都是约束违反**。
- **C-DQN 的结果**（L142）：选出了两条无环路径 $R_1=[0,1,2,3,7,11]$、$R_2=[0,8,4,5,6,7,11]$ 且均不违反约束；$R_1$ 因更短而在后续 episode 中被优先选。另一条最短路 $[0,8,9,10,11]$ 起初因链路负载高被避开，**当负载在后续 episode 下降后 agent 又能选它**——这是一个"负载回落 → 路径选择变化"的直接观测。
- **节点探索率**（式 6：$N_e=N_r/N_{s,d}$，L113）：**C-DQN 在两种 mesh 规模下都达到 80–90% 的节点探索率**；Dijkstra 一旦算出就固定给同一组路径；**DQN 的探索比 Dijkstra 好，但由于随机探索导致的约束违反，成功算出路径后的节点探索率只有约 60%**（L144）。
- **平均奖励（Fig 4，L151–156）**：C-DQN 在两种规模下都取得最高奖励，**每个 episode 都能成功算出端到端路由**；DQN 在早期 episode 因约束违反出现**负奖励**（图中紫色区域）。作者结论：**"Repeated loop corrections result in selection of longer paths whose rewards are not so high and leads to potentially longer propagation delays."**
- **收敛（Fig 5，L160）**：**12 节点**时 DQN 与 C-DQN **都收敛稳定**；**24 节点**时 **C-DQN 收敛明显优于 DQN**，因为探索被限制在更安全的状态-动作子集内。
- **复杂度（Table II，L178）**：Dijkstra 时间 $O(|E|+|V|\log V)$、空间 $O(V)$；DQN 时间 $O(\sum_{l=0}^{L-1}n_l n_{l+1})$、空间 $O(|S\times A|+M_B)$；**C-DQN 时间同 DQN，空间降为 $O(|S_{c_k}\times A_{c_k}|+M_B)$**——因为**只存安全动作**，所以 C-DQN 在时间与存储上都比 DQN 更省。
- **基线**：**传统 DQN（带 reward shaping）**，两者在相同 mesh 规模（12 / 24 节点）与相同参数下对比。

**5. 实验条件**
Python 自建环境，**定制 gym API** 实现一个 LEO 卫星 mesh 网络的抽象路由环境；考虑**两种 mesh 簇规模：12 个节点与 24 个节点**（L100）。**部署方式（关键）**：由于星上处理能力有限，**算法部署在位于地面的中央控制器上**，由它统筹整个 LEO mesh 的路由路径计算与决策（L100 逐字："Due to limited on-board processing capabilities of satellite nodes, we deploy the routing algorithms on a central controller on ground that orchestrates the routing path computations and decisions across the LEO satellite mesh network in space."）。评估三个维度：**路径计算、收敛、韧性（鲁棒性 + 复杂度）**（L100、L129）。
**注意**：论文报告的是**抽象 mesh 网格图**上的结果，**没有给出星座参数**（轨道高度/倾角/面数/星数）、**没有给出链路容量或负载的物理量纲**（负载只有归一化的 $U_{e_{i,j}}$）、**没有时延/丢包的实测曲线**，也没有说明负载是如何随 episode 演变的。

**6. 它自己承认的局限**（集中在 §IV.C "Resiliency"，L171，逐字）
- "In conditions with interrupted ISL and ESL connectivity, it **leads to delays in the dissemination of routing information**. This also requires **extensive efforts in model training as the topology gets larger because several future snapshots need to be trained in advance** for the deployed model to react appropriately in the events of connectivity failures."
- "**One of the technical limitations is that the satellite nodes are not able to learn anything about their neighboring nodes in the events of ISL failures.**"
- 关于 GNN："Graph Neural Networks (GNNs) are efficient in extracting topology information and sharing knowledge among both connected and disconnected agents through a message-passing paradigm [11]. **However, they are computationally expensive** and hence their application need to be carefully analyzed by considering the limited computational capabilities of on-board satellite hardware."
- 关于多智能体："Multi-agent systems with distributed learning architectures can off load the learning task on several distributed nodes instead of a single central entity. **However, it becomes difficult to synchronize the learning outcomes of several spatially distributed agents since each of them can only partially observe the environment. Particularly in dynamic topologies and ISL failure situations, this will result in inconsistent learning behavior.**"
- 结论段（L184）逐字："Addressing the resiliency aspects of the C-DQN algorithm, **we believe that there needs to be a mechanism where the satellite nodes can implicitly be aware about the link loads and connectivity conditions of all the other nodes** within the satellite mesh topology. The usage of GNNs to design such a knowledge-graph based routing environment can be considered as the future outlook of this work. However, **the computational complexity and scalability of such an environment needs to be carefully analyzed** by means of realistic simulation models."

**7. 它没做但看起来能做的地方**（基于内容）
1. **论文自称 "Constrained DQN"，但约束的实现方式是"预计算安全路径集 + 在其上取 max"**（式 1–4、Algorithm 1）——**没有 Lagrangian 乘子、没有 CVPO/CPO 之类的约束优化、没有约束违反率的收敛保证**。作者自己承认"只在动作选择时屏蔽不安全动作、不改 Q 更新"是不够的（L21），但其解法本质上仍是**在受限动作集内做标准 DQN**。这个 gap 值得在方法层面追问。
2. **"多条链路负载完全相同时 agent 认为所有动作等价"**（L137）是一个**状态表征的对称性缺陷**：$U_{e_{i,j}}$ 只编码了本节点四条出链路的负载，**不含邻居节点的队列状态或到目的地的方向信息**——这正是 Y2H4NPLU 用邻居 2-bit 编码、X5Z98UPM/XLRW7XXN 用 $QU_j$/$C_n$ 补上的那块信息。作者没有把这条观察推广成"状态设计原则"。
3. **Dijkstra 后端的安全路径集需要周期性重算**（L46），但**重算周期、以及拓扑变化时路径集陈旧导致的可行域收缩/失效**完全没有讨论——而 C-DQN 的整个安全探索都建立在"这个集合是对的"之上。
4. **实验结果全部是抽象 mesh 图上的（12/24 节点）**，节点探索率、奖励、MSE 三个指标都**没有物理量纲**；Fig 2 的路径图例（0→11）在 12 节点网格上，**与 24 节点的结果混在同一套指标里报告**，规模效应只能靠"12 收敛好、24 才显出差距"这一句话判断。
5. **负载的时变过程完全没有交代**：L142 说"当负载在后续 episode 中回落时 agent 又能选那条最短路"，但**没有说明负载是怎么变、变成多少、变化周期多长**，因此这条最有价值的观测无法复现。
6. **中央控制器意味着与地面站的持续交互**，作者以"星上算力有限"为理由（L100），但这与它自己引用的文献 [2]（Roth et al. 2022 分布式 SDN 负载均衡）的分布式路线相反；**两种部署方式的端到端时延/信令开销对比没有做**。
7. 论文**没有报端到端时延或丢包率**——只有"比 DQN 好"的相对指标（节点探索率、奖励、MSE），**"链路负载被均衡到什么程度"没有绝对数字**。

**8. 和同批其他篇的关系**
- **与 Y2H4NPLU 直接互引（本批最明确的一对）**：ZIUBKVPZ 的参考文献 **[10]** 就是 **B. Soret, I. Leyva-Mayorga, F. Lozano-Cuadra, M. D. Thorsager, "Q-learning for distributed routing in LEO satellite constellations," 2023, arXiv:2306.01346**（L210）——即本批的 Y2H4NPLU。两篇还**共同引用 Boyan & Littman 1993**（ZIUBKVPZ [6]，L202；Y2H4NPLU [8]）。**但两者立场相反**：Y2H4NPLU 主张**全分布式**（每星 2-bit 状态、只交换邻居 Q 值、明确以"不依赖地面段、信令开销最小"为卖点），ZIUBKVPZ 则**明确采用地面中央控制器**（Table I 最后一行 "Learning and decisions: Centralized"），理由是"星上处理能力有限"。**这两篇构成本批里关于"决策放在哪"的最直接正面对立。**
- **与 Y2H4NPLU 的另一处对照是反馈依赖**：Y2H4NPLU 的 Q 更新用的是**邻居卫星的 Q 表** $Q_j$（依赖邻居反馈），ZIUBKVPZ 用的是**受限动作集内的自身 bootstrap** $\max_{a\in\mathcal{A}_{c_k}}Q^c(s_{t+1},a)$（式 3，不依赖邻居反馈）——而 ZIUBKVPZ 自己在 L171 承认"ISL 失效时卫星学不到邻居的任何东西"，**这恰好指向了 Y2H4NPLU 那条邻居反馈路线在链路失效下的脆弱性**。
- **与 X5K285MW 通过共同作者与共同参考文献强耦合**：ZIUBKVPZ 的作者含 **Manuel Roth 与 Hermann Bischl**，而 X5K285MW 正是 Roth 的单作者论文；ZIUBKVPZ 的 **[2]** 就是 **Roth, Brandt, Bischl 2022「Distributed SDN-based load-balanced routing」**（L194）——那正是 **X5K285MW 的参考文献 [15]**（X5K285MW L157）。此外 ZIUBKVPZ 的 **[3] Liu, Luo, Huang, Meng「A load balancing routing strategy for LEO satellite network」IEEE Access 2020**（L196）正是 **X5Z98UPM 的参考文献 [26]**（X5Z98UPM L394）；**[4] Gounder, Prakash, Abu-Amara「Routing in LEO-based satellite networks」**（L198）同时是 **X5Z98UPM 的 [13]** 与 **YD4JUT7G 的 [19]**。
- **与 S85KQ4FC 的对照**：S85KQ4FC 的核心发现是"星上逐包推理跟不上转发"，因此做流级复用；ZIUBKVPZ 恰恰**因为星上算力不足而把学习搬到地面**（L100）——**两篇是从"算力不足"这一前提出发的两条相反工程路线**（一条摊销推理，一条外移推理），而 ZIUBKVPZ 的后端还需要跑 Dijkstra 周期性重算安全路径集（L46），这部分开销它自己也没算。
- **与 YD4JUT7G 的对照**：YD4JUT7G 论证"跨域层面地面段成本可与空间段相当、且 BGP 无法承载 GSL 抖动"；ZIUBKVPZ 选择"把路由决策放在地面中央控制器"，属于 YD4JUT7G 所批评的**依赖地面基础设施**的一类做法——但 ZIUBKVPZ 讨论的是域内 mesh 路由，层次不同（YD4JUT7G 明确把域内路由划到范围外，其 L272）。
- **与 XM6NUPM4 的对照**：XM6NUPM4 证明 ISL 容量（20 Gbps）远高于 GSL，因此**ISL 不太可能成为瓶颈**；而 ZIUBKVPZ 的奖励与约束**全部围绕 ISL 链路负载 $U_{e_{i,j}}$** 设计——两篇对"瓶颈在哪一层"给出了**不同层次的假设**，值得并列核验。

**9. 对"负载变化下到达率/时延"的贡献**
**提供的是"负载如何进入决策"的机制性事实，而非负载—时延的定量曲线**：
1. **给出了负载的三段离散化**（$U<0.5$ 舒适 / $0.4<U<0.8$ 环路区 / $U>0.8$ 拥挤，式 5）并把它们写进奖励分段——这是本批唯一一篇**把链路负载利用率作为分段奖励的判据**的论文（X5Z98UPM 的分段依据是**跳数** $C_i\le C_j$ 与**邻居队列** $QU_j\le0.5$，两者结构相似但变量不同）。
2. **观测到"负载回落 → 路径选择改变"**（L142 逐字）："Although the path [0, 8, 9, 10, 11] was another shortest path, it managed to avoid it considering the high link loads. **When the link loads subsided in the later episodes, the agent was able to even select this path.**" ——这是本批唯一一条**明确描述"策略随负载状态变化而切换、且可逆"**的记录（其他论文的负载扫描是静态横截面）。
3. **量化了"高负载导致约束违反"**：作者指出约束违反最突出的场景正是**多条链路拥塞（$U>0.8$）时 agent 被迫走已走过的路径**（L96），且极区只有两条 ISL 时同样如此——即**负载升高会压缩可行动作空间，到某个点后约束无解**。这与它自己 Abstract 的说法一致（L7）："identify conditions where **the constraints cannot be satisfied, necessitating a switch to rule-based source routing algorithms**"（**认清约束无解、必须退回规则型源路由**）。
4. **给出了"未修正环路会导致时延变差"的因果链**（L156 逐字）："Repeated loop corrections result in selection of longer paths whose rewards are not so high and **leads to potentially longer propagation delays**."——但只有因果陈述，**没有时延数值**。
**局限**：本文**没有到达率这个自变量**（负载只以归一化利用率 $U$ 出现，且其演化过程未交代），**没有时延/丢包的绝对数值**，因此**无法从中提取"到达率 → 时延"的任何定量关系**。它对本题的价值在于**机制**：负载如何进入状态、如何进入奖励、如何在哪些条件下使约束失效。

**10. 一句话评价**
本批**唯一一篇把"约束"当一等公民**的论文：用 CMDP 形式化 + "预计算安全路径集作为受限动作空间"实现安全探索，最有价值的两个产物是 ①**对传统 DQN 失败的机理诊断**——"四条 ISL 负载完全相同 ⇒ agent 认为所有动作等价 ⇒ 环路不可避免"（L137），这是一条干净且可复现的状态表征缺陷；②**对"何时应该放弃学习型路由"的明确指认**——约束无解时退回规则型源路由（L7）。但它的"Constrained DQN"实质是**动作掩码 + 受限 max**，没有约束优化的理论保证；实验停留在 12/24 节点的抽象 mesh 图上、无时延无丢包无星座参数、负载时变过程未交代，且**采用地面中央控制器**，与 Y2H4NPLU 的全分布式主张正面相反——两篇互引（ZIUBKVPZ 引 Y2H4NPLU 为 [10]）却给出相反的架构结论，是本批最值得并列阅读的一组对照。

## 批次交叉索引（R10 汇总，供主控使用）

**引用关系（本批内部实测）**
- **ZIUBKVPZ → Y2H4NPLU**：ZIUBKVPZ 参考文献 [10] 即 Soret, Leyva-Mayorga, Lozano-Cuadra, Thorsager, "Q-learning for distributed routing in LEO satellite constellations," arXiv:2306.01346（ZIUBKVPZ L210）。**两篇立场相反**：Y2H4NPLU 全分布式、以"不依赖地面段"为卖点；ZIUBKVPZ 明确 "Learning and decisions: Centralized"（地面中央控制器）。共同祖先：Boyan & Littman 1993（Y2H4NPLU [8]；ZIUBKVPZ [6]）。
- **YI9G7NR7 与 Y2H4NPLU 高度同源但未互引**：状态 $S_i=\{L_i,N_i\}$（邻居 2 bit）、奖励三段式（$r_{queue}+r_{dist}$，$r_{dist}=w_2\frac{\|id\|-\|jd\|+\|sd\|}{\|sd\|}$ 逐字符相同）、Q 更新取**邻居 Q 表** $Q_j$、负载定义 $\ell=\sum\lambda/\lambda^{*}$ 四处几乎逐式相同；**YI9G7NR7 参考文献 [1]–[12] 中无该文**。**需主控核验**（可能为同脉络延续或引注遗漏），我未下判断。
- **YD4JUT7G 被同批两篇引用**：X5K285MW 的 [8] 与 XM6NUPM4 的 [17] 都是 "Internet backbones in space"。
- **X5K285MW / XM6NUPM4 / YD4JUT7G 构成引用三角**：共享 Handley 2018「Delay is Not an Option」（X5K285MW [10]、YD4JUT7G [20]）、Bhattacherjee 团队（X5K285MW [2] CoNEXT'19、YD4JUT7G [3] HotNets'18）、Gvozdiev 的"额外跳数—传播时延"分析线（X5K285MW [9]、YD4JUT7G [41]）、Walker 1984（X5K285MW [16]、YD4JUT7G [42]）、del Portillo 成本线（YD4JUT7G [7][8][9]、XM6NUPM4 [4]）。
- **Roth 一脉**：ZIUBKVPZ 作者含 Roth & Bischl，其 [2] = Roth et al. 2022 分布式 SDN 负载均衡 = X5K285MW 的 [15]。
- **共享基线文献**：DRL-ER（S85KQ4FC、XLRW7XXN、Y2H4NPLU 三篇共同引用）；Liu et al. 2020「A load balancing routing strategy for LEO satellite network」（X5Z98UPM [26] = ZIUBKVPZ [3]）；Gounder et al. 1999（X5Z98UPM [13] = YD4JUT7G [19] = ZIUBKVPZ [4]）；ELB / TLR（X2FCSU4S 与 X5Z98UPM 共同引用）；HGL（X5Z98UPM [14] = XLRW7XXN [2]）；Papa et al. 2020（X5K285MW [14] = XLRW7XXN [5]）；Mnih et al. 2015 DQN 原始论文（Z74SR656 [192]——**本批三篇 DQN 论文无一篇引它**）。

**"低负载区算法无差别"这一现象在本批出现 4 次（独立观测）**
XLRW7XXN L174（网络空闲时三种算法差别不大）｜XM64YRAW L236（低负载时 GQN 相对 SP 无明显优势）｜X5K285MW L92 语境（闲置网络下差异不显著）｜YI9G7NR7 L160（$\ell<0.6$ 时三者都是低时延 + 100% 送达率）。**可作为"负载感知路由收益是负载的函数"的多源证据。**

**本批唯一给出"到达率/负载 → 时延 + 送达率"绝对值的是 YI9G7NR7**（$\ell=0.5$–0.9；$\ell=0.8$ 时 241 ms / 98.6%；$\ell=0.9$ 时时延优势 27.6%/18.6%），其次是 XM64YRAW（只有趋势，无绝对数）。**Y2H4NPLU 给出唯一的归一化负载定义 $\ell=\sum\lambda/\lambda^{*}$ 与唯一的拥塞形式化判据（回归斜率 t 检验，$H_0:\beta_1\le0$，$\alpha=0.05$，末 200 包）**。**X5K285MW 给出唯一的"合规悬崖 + 实际 bps 锚点"**（70000 会话 ≈ 9.72 Gbps、120000 ≈ 16.67 Gbps；随机选路多承载 73%）。

**与"负载/时延"无直接关系（如实标注）**：X2FCSU4S（缓存定价博弈，无到达率扫描）、XM6NUPM4（容量规划，时延=跳数约束、容量需求=静态均值）、YD4JUT7G（跨域架构，动态轴是连通性与降雨，无排队项）、Z74SR656（综述，唯一量化关系为转述：时延随卸载率下降、随高度上升）。

<!-- END -->

