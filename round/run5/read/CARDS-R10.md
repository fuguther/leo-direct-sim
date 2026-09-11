# 读卡批次 R10

> 读法：逐字通读 VM MinerU MD 全文，行号对应 `/data/liguang13/topic-loop-r2/md/<KEY>/<KEY>/txt/<KEY>.md`。
> 批次：X2FCSU4S X5K285MW X5Z98UPM XLRW7XXN XM64YRAW XM6NUPM4 Y2H4NPLU YD4JUT7G YI9G7NR7 Z74SR656 ZIUBKVPZ（11 篇）
> 每篇读完即时写卡；批次内交叉关系集中记在第 8 项（写卡时点只引已读篇目 + 原文参考文献）。

## X2FCSU4S — Load Balancing Based on Cache Resource Allocation in Satellite Networks

**1. 一句话**
把 GEO 卫星的剩余缓存当成"商品"，用 Stackelberg 博弈向 LEO 卫星定价出售；LEO 用 Martingale 包络自己估计 backlog（队列积压）来决定买多少空间，把拥塞的 LEO 内容"卸载"到 GEO——本质是缓存资源分配/定价，不是路由算法。

**2. 问题设定**
LEO 高速移动、星地连接间歇，队列变长、缓存溢出丢包（L15 摘要逐字："During a high-speed movement, the satellites are connected intermittently, so the queue length becomes larger and a cache overflow appears"）。物理事实是 GEO 体积/缓存远大于 LEO，所以 LEO 拥塞概率大、GEO 常有空闲缓存（L63）。麻烦在于 GEO 存储有限而多个 LEO **非合作**竞争：谁定价、谁买多少、买不起的节点出局（L23、L260）。参与者是 1 个 GEO（leader）+ K 个 LEO（followers），GEO 必须先满足自身需求，剩余空间才出租（L264）。

**3. 方法骨架**（非 RL：信道建模 + Martingale 界 + 博弈 + 凸优化 + 三个算法）
- 信道：下行 Gilbert-Elliott 两态马尔可夫（式 2），good 态速率式 3，Nakagami-m 阴影 pdf 式 4；上行是 S-ALOHA 接入与 GE 的级联，用指示函数 $I(T)=1$ 表示接入成功（式 6），状态转移矩阵式 7、速率式 8（L110–128）。表 2 给重/轻两套阴影参数（L246）。
- 到达/服务：把到达拆成高优先级 $A^h$、低优先级 $A^f$（SP 调度），Lemma 1（式 9）证明到达过程是超鞅，Corollary 1（式 10）把等效服务过程也建成超鞅（L139–157）。思想是"级联"：用户数据生成 → 信道接入 → GE 信道服务，整体当作缓存的到达过程（L149）。
- backlog 估计：Theorem 1（式 12）给时延上界违反概率 $p(W(T)>kappa)le rac{E(M_{A^t}(0))E(M_S(0))}{H}e^{-	heta_1^*kappakappa_{ss}}$，式 13 是 $	heta_1^*$ 的可行集；FIFO 版式 14–16、SP 版式 17–19，最终得到 $sigma_{FIFO,L}$、$sigma_{SP,L}$（L203–241）。
- 内容热度：Zipf 式 11，$sin[0,1]$ 控制偏斜度（L159–169）。
- 博弈：GEO 收益式 20、Problem 1（式 21，约束是 $sum s(q_{L_k})le h(sigma_G)$，即 GEO 剩余空间）；**Congestion Index** 式 22 $I(q_{L_k})=ln(1+rac{q_{L_k}sigma_{L_k}}{sum_{j
eq k}q_{L_j}sigma_{L_j}})$——作者自述是照抄香农公式的"信干比"结构（L284）；LEO 收益式 23 $R_{LEO}=c f(sigma_{L_k})I(q_{L_k})-eta_{L_k}s(q_{L_k})$，即"收益−买空间的钱"。
- 求解：Lemma 2 式 28 给最优购买比例 $q^*_{L_k}=(rac{cf(sigma_{L_k})}{sigma_{L_k}eta_{L_k}}-y_{L_k})^+$；Problem 3 非凸，作者**假设所有节点都参与**从而转成凸的 Problem 4（L352）；Theorem 2 式 33 给 $eta^*$，Theorem 3 式 34 给参与博弈所需的最小剩余空间，Theorem 4 证明阈值 $x_{L_K}$ 对 K 严格单调递增，Theorem 5/式 36 给分段最优价。
- 算法：Algorithm 1 *Members of a Game*（按 $sqrt{f/y}$ 排序，逐个剔除到 $x_{LU}<h(sigma_G)$，决定参与人数，L398–418）；Algorithm 2 *Distributed Cache Price Bargaining*（按 $sum q$ 与 $h(sigma_G)$ 的差调价 $pmDeltaeta$，直到 $|sum q-h(sigma_G)|<zeta$，L424–444）；Algorithm 3 *Popularity Matching*（把**不受欢迎**的内容传上 GEO，因为缓存成本与热度成反比，L484、L492–506）。
- 均匀定价对照：式 37–41，结论"uniform pricing scheme is inferior to the nonuniform pricing scheme"（L480）。

**4. 它声称的效果**
- Fig 5（L199–201）：Martingale 时延界 vs $10^6$ 次内容仿真的箱线图，作者判"the delay bound ... is quite tight"——参数固定为 $lambda_f=0.6, p_m=0.1, R_{su}=1$。
- Fig 6 / Fig 7（L248–256）：违反概率随 backlog 增大而下降；重阴影下行比轻阴影更容易积压；SP 的高优先级服务 $A^h(T)=0.5T$（仿射）时违反概率偏离无优先级情形。
- Fig 11（L513）：上传价格随 GEO 剩余空间 $h(sigma_G)$ 增大而下降，$L_3$ 最便宜、$L_1$ 最贵。
- Fig 12（L515）：$h(sigma_G)$ 越大能容纳进博弈的 LEO 越多；非均匀价优于均匀价；$s=0.1$（近均匀）比 $s=0.8$（偏斜）能容纳更多 LEO。
- Fig 13（L532）：丢包率对比，**基线是 DSR（最短路）和 TOTD（文中指 [1] Nishiyama 的方法）**，本文最低；作者归因 DSR 造成节点流量不均衡、TOTD 只考虑传播时延且阈值强依赖信道条件。

**5. 实验条件**
网络规模：STK 生成 Iridium-like 星座，66 颗 LEO / 6 个轨道面，外加 3 颗 GEO（L490）；但实际数值分析**只取被 satellite111 长期覆盖的 6 颗 LEO + 1 颗 GEO 共 7 颗星**（L511）。参数：表 2 重/轻阴影；$lambda_f=0.6$、$p_m=0.1$、$R_{su}=1$；Zipf $s=0.1/0.8$。非 RL，无训练/评估之分，也没有独立的验证集。**没有到达率扫描**，没有网络级端到端时延仿真。

**6. 它自己承认的局限**
- L77 脚注 1 逐字："Since this work mainly analyzes the load balancing of satellite data streams, we do not consider the overlap of coverage, which is beyond the scope of our analysis."
- L352 逐字（关键松弛）："Note that the above problem is a non-convex problem. Then, we assume that all nodes participate in the game so that Problem 3 will be transferred into a convex problem without the limit of the indicator."
- L466、L478：两处证明直接省略（"The proof is similar to theorem Theorem 2." / "A detailed proof is omitted because it is similar to that of Theorem 5."）。
- 结论段（L536）**没有**任何局限自述（未见 limitation 小节）。此外全文未讨论把内容传上 GEO 带来的额外星间传播时延。

**7. 它没做但看起来能做的地方**（基于内容）
1. $sigma_L$（LEO backlog）与 $h(sigma_G)$（GEO 剩余空间）在每次博弈里是**静态输入**，而摘要自己说 LEO "connected intermittently"（L15）；没有把时变可见性/时变 backlog 做成滚动博弈。
2. Theorem 4 证明 $x_{L_K}$ 对 K 严格单调递增 → 参与集合存在**阈值切换**：$h(sigma_G)$ 轻微变化就可能让某个 LEO 突然被踢出局（L342、L370–384）。阈值附近的震荡/不连续没有任何实验。
3. Martingale 上界的紧致性只在 $lambda_f=0.6$ **单点**验证（Fig 5）。如果负载升高使界变松，整个定价就建立在偏保守的 backlog 上——这是一个可直接测的缺口。
4. Fig 13 的 x 轴是"单用户数据速率"（服务侧），不是到达率；"丢包率 vs 负载"曲线缺失。
5. Algorithm 2 被命名为 "Distributed"，但每轮需要 GEO 广播 η、收集全部 LEO 的 $q$（L426–444），收敛轮数与信令开销未测。
6. 丢包只做总比例统计，未区分"缓存溢出丢包"与"信道接入失败丢包"（S-ALOHA 冲突本来就会丢，式 6 已建模）。

**8. 和同批其他篇的关系**
（写卡时点=本批第 1 篇，尚无已读可比篇目。）原文参考文献里与本主题相关的锚点：TLR（Song et al., 文献 [2]）、TOTD（Nishiyama [1]）、MLSR（Akyildiz [9]）、LEO 缓存匹配博弈（Liu [30]）。若后续篇目引用本篇将在批次末汇总。

**9. 对"负载变化下到达率/时延"的贡献**
**给了理论骨架但没给实测曲线**。式 12/16/19 把到达率（$kappa_h,kappa_f$）、缓存服务率 $kappa_s$、时延/积压门限 $kappa$ 与违反概率连在一个指数式里，Fig 6/7 显示违反概率随 backlog 阈值单调下降——这是"到达率↑ ⇒ 溢出概率↑"的间接证据。但全文没有任何"时延 vs 到达率"或"丢包 vs 到达率"的扫描图，到达率在公式里是常数率，Markov 到达的突发性（自相关）未建模。对"负载变化下到达率/时延"的直接贡献：**无**；间接贡献是一个可用于推导溢出概率上界的鞅工具链。

**10. 一句话评价**
把地面无线缓存的 Stackelberg 定价线（文献 [23] Hajimirsadeghi 等）整体搬到 GEO/LEO 多层卫星的"缓存卸载"上，数学包装（Martingale 包络 + 非凸转凸）很厚、工程直觉很薄：它把 LEO 的拥塞问题等价替换成"向 GEO 买空间"的问题，而买来空间后内容走星间链路所付的传播/排队时延从头到尾没有进目标函数，7 颗星的数值实验也支撑不起"load balancing（负载均衡）"这个标题。

<!-- END -->
