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

<!-- END -->
