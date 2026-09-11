# 候选卡 A1（R3 历史碰撞审查流程用切片）

> 来源：round/staging/path-A-scenario.md 卡A 节原文（L18-L37），带试运行材料标签。

## 卡A 队列状态的信息龄没有进入观测:陈旧邻居状态下的过矫正振荡

1) **场景与可观察现象**:卫星 n 在包到达时刻 t 选下一跳;可用的邻居队列/拥塞状态是 t−Δ 时刻的快照,Δ=传播(ISL 千至数千 km,单跳毫秒级,量级为本人估算【推演】)+对端排队+周期性状态更新间隔。LOZANO-2025-CONTINUAL 原文明确邻居拥塞向量"can be updated periodically",但从未给出周期、也未把龄期喂给代理【原文事实:arXiv 2405.12308 DRAFT版 §IV-A "The feedback needed by agents is minimal" 段;28字段状态=16拥塞+8邻居坐标+2本星坐标+2目的坐标,§III】。可观察:仿真日志对每条决策所用状态打时间戳→统计"决策时队短、执行时已满"条件概率、下游链路负载的极限环(切换频率/振幅)、age 分布对误判率的条件曲线;现象与到达率(误入满队→溢出丢弃)和时延(振荡绕行)直接挂钩。

2) **困难与原因假设**:【推演】多个上游节点看到同一"短队列"并同时转入(羊群),随后同时转出——tao25 引 Tanenbaum 描述的 flapping 在多智能体学习下被放大:陈旧观测使 TD 目标与策略梯度相对当前网络有偏,且"其他代理在学"构成非平稳;机制层面=部分可观测×多智能体非平稳的复合失败。【原文事实:tao25 §1 p.1-2:"two routers sharing two links simultaneously notice that one of the links is not congested and both attempt to use it...oscillating between the two links — flapping"】。竞争解释:①不是陈旧性而是奖励对切换不对称(进慢链被罚、退出无成本);②是 ε-greedy 探索噪声而非信息龄;③拓扑周期性本身产生周期性拥塞,与决策机制无关。三者均可在同一日志上判别。

3) **拟议改动**:改观测+训练环节:给每条邻居特征打时间戳,把 age 作为策略输入(age-conditioned policy);训练时按龄对特征加噪/衰减做数据增强。机制:策略学会对老信息降权→减少过矫正切换→少误入满队(到达率↑)、少绕行(时延↓);若 age 特征无增益,则得到"该信息价值可忽略"的否定结论,同样可发表。

4) **初步近邻**:WEIL-2024-RMP 把消息刷新速度当通信开销旋钮,从不量化陈旧损伤【原文事实:§3.1 "increased number of iterations...information to traverse the network faster but also increases the communication overhead";§5 表2:无带宽限制时所有方法与最短路完全打平 2.26/4.39/4.52】;PRIMAL 异步事件驱动,观测无龄期字段【原文事实:表I;§III 观测定义】;KM 记录 stale state AND routing 于 arXiv 检索零命中(2026-09-03)【原文事实:KNOWLEDGE-MAP 检索记录节】;Undermind 语义检索(S1)最近命中为 Bhavanasi2023 与 eligibility-traces 自适应路由(未读),无"龄期条件化策略"命中;泛 MARL 陈旧观测补偿 2605.26286 仅摘要级、非 LEO【摘要】。结论:LEO 逐包路由内的 age-conditioned 观测 未核(本轮检索范围内未见)。

5) **简单替代**:①带滞回的固定阈值规则(TLR 式红绿灯)本身能压乒乓,可解决轻中度负载下的大半【推演;SONG-2014-TLR 笔记:作者自设防死循环机制】;②给 ELB 信令加时间戳+信任衰减=给基线同等信息;③成熟 RL 慢更新+低 ε 也能压振荡。猜想:固定规则在稳态够用,负载阶跃附近的中间带是学习式的残余增益区——未证。

6) **立即淘汰条件**:现实 ISL 时延/更新间隔尺度下,age-aware 与 age-blind 策略的到达率/时延差 < 噪声;或实测 Δ/队列排空时间在全部负载合同里恒 <0.1(陈旧性物理上无关紧要)。

7) **下一项廉价核验**:两队列负载均衡小算例(M/M/1+信息龄 Δ):推导或微仿真"陈旧均衡策略"的振荡幅度随 Δ/排空时间比的增长曲线;一天内可出数,不需要新算法。

8) **来源指针**:tao25.pdf §1 p.1-2;LOZANO-2025-CONTINUAL §III/§IV-A(arXiv 2405.12308 DRAFT);WEIL-2024-RMP §3.1/§5表2;HE-2025-PRIMAL 表I;KNOWLEDGE-MAP.md 检索记录(2026-09-03);Undermind S1。

---
