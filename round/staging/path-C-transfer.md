> **状态标签（2026-09-10 R2，按 Codex+Luna 深审返工包第一组第 7 条）**：
> 本文件为**接触过旧候选信息的试运行材料**——生成白名单缺陷（KNOWLEDGE-MAP 含旧候选 A-D 碰撞段）
> 使三路生成器在允许入口内读到旧候选痕迹（各自已在文内声明）。不声称干净冷生成；
> 该标签不判定卡片价值，资格判定留待选题恢复后的主控对账。

# Path-C 候选研究问题草图：方法迁移与假设检查（LEO RL 路由）

> 生成：2026-09-10。charter=从相邻领域迁移方法并逐卡检查核心假设在 LEO 是否成立。
> 主指标：到达率 + 端到端时延。不排序、不推荐、无营销语。证据分层：原文事实/作者解释/代码事实/推演/待证；查不到写 未核实。
> 防火墙声明见文末。

## 阅读台账（合规）

- 实际读过（含第一手摘要核验）8 篇：其中 notes/raw 无笔记 6 篇（tao25/Olpomdp 全文、Rot24、MAPPO、RPL、DRQN、CPO——后五篇为 arXiv 摘要/正文引句级浏览）＝75% ≥ 40%。
- 精读 3（tao25 全文、HE-2025-PRIMAL HTML 表I+结构、ZHOU-2026-DTAR HTML 部分核实）；浏览 8 ≤ 14。
- Undermind search_papers 3/3（Lyapunov-BP-LEO、信用分配路由、belief-state 陈旧信息）。launch_deep_search 未用。Semantic Scholar 未用。
- 本地 PDF 事故：HE-2025-PRIMAL.pdf 与 ZHOU-2026-DTAR.pdf 均流截断（pypdf: "EOF marker not found"），改用 arXiv HTML 核验。tao25.pdf 提取件存 staging/tao25-extract.txt。

---

## 卡 C1：轨道相位条件化的平均回报策略梯度（Olpomdp 迁移）

**迁移源**：Olpomdp 多智能体策略梯度路由（tao25.pdf = arXiv 2512.03211v1 水印，Tao/Baxter/Weaver；算法原出 Baxter et al. 2001）。
**1) 场景与可观察现象**：包到达星 s，按 Gibbs 策略 μ_i_u(y)=softmax(θ_i_yu) 在当前 ISL 集选下一跳；每星只凭全局广播的负行程时间与资格迹更新，不看队列、不看拓扑【原文事实：tao25 §2 Eq(1)(2)(5)-(7)，脚注1：回报广播延迟"does not significantly affect results (Tao, 2000)"】。LEO 化后：星历给出每槽链路集与几何。观察：仿真日志中按槽统计到达率/端到端时延，以及"分配到已消失链路的概率质量"与槽边界后 re-learning 瞬态时长。
**2) 困难与原因假设**：Eq(3) 平均回报梯度显式要求系统遍历（"Provided that the system is ergodic…"）【原文事实：tao25 §2】；LEO 拓扑确定性周期+流量日变化→周期非平稳，混合时间随轨道相位变化，β=0.99 对应的 τ_alg=1/(1−β) 在相位间失配【推演：β-混合时间论证原文属平稳过程】。第二断点：θ_i_yu 以链路 u 为索引，槽切换后链路集改变，资格迹把回报绑到已不存在的链路【推演】。竞争解释：包生命周期（约百 ms）≪ 槽长（分钟级），包内拓扑准静态；断裂只发生在跨槽 credit 平均，包内决策本身不受损——若如此，相位条件化收益应只在槽边界附近可见【推演】。
**3) 拟议改动**：改参数化与更新：θ_i(phase) 按平近点角分桶（或以星历几何量替代链路身份索引），β 按相位调度；更新机制不变。若成立，机制=消除对不存在链路的概率质量（保到达率）+跨槽负载偏好随相位对齐（降时延）。
**4) 初步近邻**：LEO+策略梯度路由直接工作 未核；Rot24(arXiv 2408.01979)做卫星 MADQN 奖励塑形【原文事实：摘要已核】，非 PG-平均回报；Zen20 资格迹混合路由（Undermind 命中，未核）。
**5) 简单替代**：星历 Dijkstra 解决拓扑半；邻居队列 DQN 解决拥塞半——剩余空间主要是"零状态输入、极低星上算力"的极端合同，猜想覆盖 <50% 场景收益。
**6) 立即淘汰条件**：同一突发负载合同下，相位条件化 vs 无条件化的到达率/时延差 < 种子间噪声。
**7) 下一项廉价核验**：在 Walker-delta 逐包仿真上跑原版 Olpomdp，测槽边界后 reward 恢复瞬态长度 vs 静态拓扑对照（静态对照复用 tao25 §3.1 合同）。
**8) 来源指针**：tao25.pdf §1-3（提取件 staging/tao25-extract.txt）；Undermind U2（Zen20）。

---

## 卡 C2：Backpressure/Lyapunov → LEO：迁移主干已被占位（检验记录，按 charter 放弃主卡资格）

**迁移源**：Tassiulas-Ephremides/Neely 谱系的队列差权重与漂移+罚控制（经典前提引自 U1 命中文献族的通行表述；本卡未读其原文，未核实：具体页码）。
**1) 场景与可观察现象**：时隙 t 星 s 依据相邻队列差选转发链路。LEO 现象：邻居队列经传播+信令后陈旧，且误差与拥塞正相关（热点的信息恰恰最旧）【推演：由 ELB/TLR 信令机制谱系推得，SONG-2014-TLR/TALEB-2009-ELB 笔记线索】。
**2) 困难与原因假设**：BP 核心假设=决策时刻邻居队列差可观测+每槽链路速率平稳；LEO 中前者断裂、后者由轨道周期化【推演】。竞争解释：LEO ISL 利用率低（本平台口径 <3%）时固定阈值启发式（TLR/ELB）已够，学习增量只在重载尾域存在【推演：HE-2025-PRIMAL 表I 显示其增益仅在刻意重载合同出现——原文事实：SPF 丢包 84.8%、学习算法 0.00%，arXiv 2510.27506 HTML 已核】。
**3) 拟议改动（残余问题，非主推）**：若做，仅做"陈旧队列差 vs 预测队列差"的对照实验；实质改动=把 BP 权重的信息条件显式化为可测年龄并补偿，而非套用 DPP。
**4) 初步近邻（占位证据）**：Den23 距离型 BP-LEO、Han23 分布式跳数 BP-LEO、Yin25b GAT-BP-LEO、Nie25 Lyapunov 辅助 DRL-LEO（=SOURCES.csv 的 OPENALEX-LYAPUNOV-WCNC）、Hua25b 鲁棒 Lyapunov-LEO、Den26 时延优化 BP-LEO——全部 Undermind 命中，PDF 不可得，内容 未核实。
**5) 简单替代**：TLR/ELB 阈值启发式在低载下覆盖大半；猜想 ≥70% 的收益域被启发式+最短路占据。
**6) 立即淘汰条件**：上述任一占位文献（Yin25b/Den26/Hua25b 优先）确实处理了队列信息陈旧性或预测——则残余问题也关闭，全道放弃。
**7) 下一项廉价核验**：获取 Yin25b/Den26 全文（Undermind 标注 PDF 不可得；换 arXiv/DOI 通道），查其队列信息延迟建模一节。
**8) 来源指针**：Undermind U1 命中列表；LITERATURE/notes/raw/SONG-2014-TLR.md、TALEB-2009-ELB.md（线索级）。

---

## 卡 C3：信用分配——端到端回报 vs 逐跳可测时延分解，及 (星,槽) 时间展开 agent 化

**迁移源**：CTDE/中央 critic（MAPPO，arXiv 2103.01955）与包路由信用分配谱系。
**1) 场景与可观察现象**：包在星 i 选下一跳。训练信号二选一：(a) 包到达后的端到端时延（Olpomdp 式广播或中央 critic）；(b) 本跳立即实测的排队+传播时延（本地时间戳精确可得）。观察：仿真中两臂策略的到达率、P95 端到端时延、热点链路占用时空分布；日志可按跳分解每包时延归属。
**2) 困难与原因假设**：MAPPO 的中央 value function 显式吃全局信息，且原文设定"agents share a common reward"【原文事实：arXiv 2103.01955 正文（ar5iv 提取）："learn a centralized critic which takes global information as input"；"PPO with centralized value function input as MAPPO"；"operate in settings where agents share a common reward"】。迁到 LEO 逐跳：中央 critic 星上不可得；agent 名册不固定（包路径上的星集随轨道槽变化）；共同回报假设被逐跳分解破坏【推演】。机制假设：e2e credit 被下游拥塞混杂（动作只影响第一跳），逐跳分解不只加速学习、还改变可达策略类（热点更早交出）——差异应在突发非平稳负载出现。竞争解释：Soret-2024 表格 Q-routing 已用本地传播+排队时延并在稳态追平 genie 最短路【笔记线索，未核实其尾域表现】，即差异只是瞬态学习速度而非最终策略。
**3) 拟议改动**：改奖励接口与 agent 定义：同一网络、同一观测下，仅切换 (a)/(b) 回报（potential-based 塑形保最优策略不变性可作第三臂）；实质改动=把 (星,槽) 当 agent 的时间展开图上做槽内片段回报分解，而非直接搬 MAPPO。
**4) 初步近邻**：Rot24（卫星 MADQN 奖励塑形+收敛量化+集中学习分散控制【原文事实：摘要已核】）——塑形已被做过；e2e vs 逐跳的受控归因对照+以到达率为主指标，未见（未核实）。Mao20 合作 MARL 路由奖励设计（Undermind 命中，未核）。CHEN-2025-TMIX（CTDE-MIX LEO，笔记线索：未核实 S/A/R 细节）。
**5) 简单替代**：逐跳立即奖励+γ 调参（成熟 RL）可能解决大半；Olpomdp 式 e2e 广播+循环惩罚塑形（tao25 §3.3 已证小网络有效，且"without explicit credit assignment. All agents were penalized…"【原文事实】）可能解决其余——两者都便宜，卡的价值在于量化剩余缺口。
**6) 立即淘汰条件**：突发负载下 (a)/(b) 两臂到达率与时延分布统计不可分（3+ 种子）。
**7) 下一项廉价核验**：同一仿真合同跑两臂×3 种子；先在 45 星级（复用 CHOU-2026-STL 的 NHPP 负载合同口径）确认可控，再上 1584 星。
**8) 来源指针**：arXiv 2103.01955（引句）、tao25 §3.3、HE-2025-PRIMAL 表I（arXiv 2510.27506 HTML）、notes/raw/SORET-2024-QLEARN.md、Undermind U2（Mao20/Rot24）。

---

## 卡 C4：动作掩码的槽切换伪影——安全 RL 掩码在确定性变化可行集下的失效模式

**迁移源**：safe RL / action masking / 约束策略优化（CPO，arXiv 1705.10528 摘要已核：reward+约束设定）。
**1) 场景与可观察现象**：槽边界或 ISL 失效瞬间，可行下一跳集合（掩码）变化；对刚解禁动作的偏好是旧槽学得或从未更新【推演：掩蔽动作的 Q/偏好不接收梯度是屏蔽机制的直接后果】。观察：仿真日志在切换事件 ±5s 窗口统计到达率瞬态下陷与环包率；对照事件时刻的星历换路量。
**2) 困难与原因假设**：掩码改善训练安全，但可行集在 LEO 是**确定性时变**的——每次轨道周期同一掩码序列重演，被掩蔽动作的价值偏差周期性暴露【推演】。机制假设：掩码诱导的到达率瞬态下陷集中于槽边界。竞争解释①：下陷是基线行为（星历最短路在边界本来要换路），非掩码伪影→须设固定拓扑掩码对照；竞争解释②：无掩码塑形（循环惩罚）已等效——tao25 §3.3 在静态小网证塑形大幅加速收敛【原文事实】，LEO 是否同样成立待测。
**3) 拟议改动**：改探索与更新：相位键控强制探索（槽切换前对即将解禁的动作做 cyclic re-exploration），或对掩码外动作维护保守价值下界（CPO/保守 Q 式，改更新机制不改结构）。机制：消除切换期选中劣动作→到达率瞬态下陷消失。
**4) 初步近邻**：WEIL-2024-RMP 在图路由用 action masking（笔记全文级线索："Ours*(action masking)"，需回 arXiv 2402.05027 复核其掩码是否时变）；ZHOU-2026-DTAR 的"action-masked PPO"仅见笔记，当前 arXiv v1 HTML 无 "mask" 字样（2026-09-10 核）→ 未核实，疑版本出入；GraphPR 的 RSPH 防环（笔记线索，未核实）。CPO/掩码文献均假设可行集平稳或缓变，未核到时变可行集的处理。
**5) 简单替代**：固定小 ε 持续探索可能覆盖大部分伪影；无掩码塑形可能等效。猜想两者合计解决 ≥60%。
**6) 立即淘汰条件**：槽边界无可归因于掩码的到达率下陷（固定拓扑掩码对照后仍无差异）；或塑形与掩码到达率无差。
**7) 下一项廉价核验**：两臂（掩码+相位探索 vs 掩码+ε-greedy）在含计划内切换的 45 星仿真测边界瞬态；纯日志工作，不需新算法。
**8) 来源指针**：tao25 §3.3；arXiv 1705.10528 摘要；arXiv 2402.05027（WEIL，待复核）；notes/raw/ZHOU-2026-DTAR.md（线索，版本出入已记录）。

---

## Charter 边界与撞见声明

- 放弃登记：BP/Lyapunov→LEO 主干迁移（卡 C2）按 charter 如实记录为已占位，不作主卡。belief-state/陈旧队列预测未成卡：Undermind U3 无直接命中（与 KNOWLEDGE-MAP 2026-09-03 的零命中记录一致），且该题与"AoI-of-state"语义项高度相邻，为避免与其他草图重叠，仅在此留痕。
- **撞见声明**：①SOURCES.csv 的 local_path 列指向 related-work-notes/papers-txt/ 下若干文件（防火墙目录）——仅见路径字符串，未打开。②允许入口 KNOWLEDGE-MAP.md 的"外部碰撞补充（2026-09-03 冷启动轮）"一节出现"候选 A/B/C/D"的关系标注（属本项目旧候选的间接痕迹）——按防火墙规则跳过未深读，本文件四卡的选题均由本 charter 的方法迁移检查独立导出（Olpomdp/CTDE/BP/safe-RL 四条迁移线的假设断点），未取材于任何候选卡。③未触碰 out/、.worktrees/ 下他代理产物、notes/ 的 COLDSTART/QUEUE/FETCH 文件、related-work-notes/ 内容。
- 证据卫生：Rot24/MAPPO/CPO/RPL/DRQN 为摘要或引句级第一手核验；Liu26（State Information Lag, IEEE）与 U1/U2 各命中文献仅有标题级线索，一律标注 未核实，未据其立论。
