# Q0 最优算法选型调研（2026-08-17）

> 状态：GPT 两路（primary + independent_review）已完成并交叉一致；Codex
> 已交叉审阅并抽查文献真实性；Kimi 复核待派（见 §5）。结论供 Q0 实现前
> 拍板使用，不预设最终实现。

## 1. 结论摘要

- **现有 `routing.oracle` 不是 Q0**：它只是逐包逐跳的「全局当前传播信息」
  路由基线，未联合优化排队、容量、K 槽、切换与共享服务顺序（两路一致）。
- **未来信息上界**：首选「时间扩展网络的连续松弛（乐观上界）+ 事件/时间
  索引 MILP（可实现上界）+ 连续时间/CP 非抢占服务约束」；纯最短路、
  纯最小费用流、纯机器调度都只覆盖子问题。
- **当前信息上界**：理论对象是有限时域 MDP / 多阶段随机整数规划（带
  非预见约束）；极小规模可精确，实际 8–24 星用随机滚动时域 MILP/MPC 作为
  可实施近似——**普通 MPC 不得自称严格上界**（上界来自随机规划的松弛/对偶界
  或 future-MILP clairvoyant ceiling）。
- **信息裁剪**：砍远端队列 → 本地队列 RL/局部贪心/MaxWeight（回压需相邻
  队列差）；砍远端拓扑 → 机会式/分散 RL（需先澄清「静态星座拓扑=先验知识」
  是否保留）；砍 AoI/控制 → Q0 直接读全局真值时 AoI 无角色，分散臂不得把
  旧状态当当前状态；只能看当前 → MDP/随机 MPC/回压合法，离线 MILP 不可执行。
- **必须先冻结**：Q0 目标函数（建议字典序：deadline 前交付 bits → 完成时延
  → 队列积分）；Q0 合同（physics-only 可优化服务/接入/路由 vs
  kernel-policy-preserving 保留 DRR/FIFO/deliver-only）。

## 2. 算法族四层证据

| 候选 | 文献（已抽查真实） | 数学形式 | 复杂度（N=24–140、T=30–60s、万包） | 平台对应性 |
|---|---|---|---|---|
| 时间扩展网络流 / 最小费用流 | Ford & Fulkerson 1958（OR 6(3):419，DOI 10.1287/opre.6.3.419）；Hoppe & Tardos 2000（MOR 25(1):36，DOI 10.1287/moor.25.1.36.15211）；Even-Itai-Shamir 1976（SIAM J. Comput. 5(4):691，DOI 10.1137/0205048） | 节点 (v,t)、传输弧 (i,t)→(j,t+τ)、等待弧 (v,t)→(v,t+Δ)；流守恒跨传播；容量 Σf≤C·Δ·A；队列 Σh≤Q | 单商品动态流多项式可解；**整数多商品流 NP-complete**；逐包×边×时刻变量 ~10^8–10^9 不可行 | 天然表达传播/容量/等待/有限缓存与确定性中断；**K 槽、切换、非抢占、不可分包破坏纯流结构** → 只能做 LP 松弛上界或 MILP 骨架 |
| MILP（主框架） | Chen, Reinelt, Dai, Spitz 2019（EJOR 275(2):694，arXiv:1811.12114）；Augenstein et al. 2016（ICAPS 26，DOI 10.1609/icaps.v26i1.13784）；Δ-MILP DSN 调度（arXiv:2111.11628） | x[p,e,t]∈{0,1} 服务、y[p,v,t] 驻留、a[s,c,t] 接入、切换/顺序/区间变量；容量/队列/K 槽/可用性/切换/优先级约束 | 完整包级模型组合爆炸；**建议事件区间 + 每 OD 3–5 条候选路径 + 流聚合**；8–12 星 100–500 包可解并给 MIP gap | 平台全部约束可表达（接入 K 槽、BBM/MBB 状态、DRR/优先级的精确复制会使模型膨胀——需拍板 physics-only 还是 policy-preserving） |
| 连续时间调度 / 抢占-非抢占 | Graham, Lawler, Lenstra, Rinnooy Kan 1979（Ann. Discrete Math. 5:287，DOI 10.1016/S0167-5060(08)70356-X）；Garey-Johnson-Sethi 1976（Math. Oper. Res. 1(2):117） | packet-hop=operation、链路/GSL=machine；S/C 变量、precedence、no-overlap/availability calendar | 路径固定时很强；联合路由需与 MILP/列生成/CP 结合 | kernel 是**非抢占 abort-and-restart**（hard-retire 整包重排），不是 preemptive-resume——调度模型必须按此语义建 |
| 动态规划 / 时变最短路（含 wait） | Orda & Rom 1990（J. ACM 37(3):607，DOI 10.1145/79147.214078） | V(v,t)=min{Δ+V(v,t+Δ), τe(t)+V(j,t+τ)}（等待项）；Bellman 递推 | 单包精确；联合状态随包数×队列组合爆炸 | 适合单包 oracle、列生成定价子问题、极小规模 ground-truth 校验；不能直接给万包共享系统联合最优 |
| 滚动时域 / MPC | Rockafellar & Wets 1991（MOR 16(1):119，DOI 10.1287/moor.16.1.119）；Mayne et al. 2000 综述（Automatica 36:789） | 每控制时刻解 [t,t+H] 优化、执行首步重算；场景树 + 非预见约束 | 8–24 星实际可行 | 当前信息 Q0 的可实施近似；**严格上界需随机规划松弛/对偶界**，普通 MPC 只算强基线 |
| 其他：回压/MaxWeight | Tassiulas & Ephremides 1992（IEEE TAC 37(12):1936，DOI 10.1109/18.850663） | MaxWeight / 差分背压 | 多项式（每槽 O(E)） | 稳定区域最优（吞吐）；**非有限时延/deadline/切换成本最优**；严格 own-queue-only 不是经典回压 |
| 其他：网络编码 / 拍卖 | Ahlswede et al. 2000（IEEE TIT 46(4):1204，DOI 10.1109/18.850663）；Bertsekas 1992（auction，见 MA 128:45） | 组播编码超路由；拍卖=assignment/min-cost-flow 分布式求解 | — | 编码改变研究对象（当前无编码/ARQ 合同）；拍卖适合 Lagrangian/价格分解，非直接精确求解器 |

## 3. 信息裁剪适用性（GPT 两路一致 + Codex 复核）

| 裁剪 | 原最优算法是否适用 | 建议切换 |
|---|---|---|
| (a) 砍远端队列（只留本地） | 联合 MILP/回压（差分）不再可执行；仍可留作不可达 ceiling | 本地队列 RL、局部贪心、own-queue MaxWeight |
| (b) 砍远端拓扑/可见性 | 全局时变最短路/确定性网络 MILP 不可执行 | 本地邻居发现、机会式/分散 RL；**先澄清静态拓扑先验是否保留** |
| (c) 砍 AoI/控制 | Q0 直读全局真值时 AoI 无角色 | 分散臂不得把「未知年龄旧状态」当当前状态——显式 belief/鲁棒策略 |
| (d) 只能看当前、不能看未来 | 离线 clairvoyant MILP/时间扩展流不可作为可执行策略 | MDP/多阶段随机优化（非预见约束）、随机 MPC、回压、RL |

## 4. Q0 实现建议（Codex 汇总）

1. **冻结 objective**：字典序「max 到期前交付 bits → min Σ 完成时延 → min
   Σ 队列积分」；不直接复用 RL reward（A1/C3 未清）。
2. **冻结合同**：Q0-physics-only（可优化接入/服务/路由，只保持物理约束）为
   主上界；Q0-kernel-policy-preserving（固定 DRR/FIFO/deliver-only）用于
   平台交叉验证。
3. **未来信息臂**：U_future_LP（聚合时间扩展 LP 松弛，乐观 ceiling）+
   U_future_MILP（事件区间 + 路径列 + 非抢占约束，记录 MIP gap）；8–12 星
   ground-truth 生成器 → 回放 kernel 校验容量/队列/K 槽/切换/deadline/唯一 fate。
4. **当前信息臂**：极小规模非预见场景树/DP 作正确性锚点；8–24 星 stochastic
   receding-horizon MILP（每次执行首步）；普通 MPC 只称近似。
5. **对比 arms**：U_future_LP / U_future_MILP / U_current_DP_tiny /
   U_current_stochMPC / oracle / capacity / delay / hop / local-queue-MaxWeight /
   分散 RL；同 trace、同物理机制，只改信息集。
6. **规模扫描**：8/12/24 星变量数、MIP gap、求解时间、回放可行率——正式论文
   前必须实测，本调研数字仅是保守工程起点。

## 5. 三方状态与待办

- GPT primary + independent_review：结论一致（上文），证据留痕
  `/tmp/gpt_q0_primary.txt`、`/tmp/gpt_q0_review.txt`。
- Codex：交叉审阅通过；文献抽查 Chen 2019（EJOR 275(2):694）与 Δ-MILP
  （arXiv:2111.11628）真实；经典文献（Ford-Fulkerson、Hoppe-Tardos、
  Orda-Rom、Rockafellar-Wets、Tassiulas-Ephremides、Graham et al.、
  Even-Itai-Shamir）为领域标准引用。
- 待办：Kimi 复核本结论；按 §4 冻结 objective/合同后进入 Q0 接口实现
  （全局快照 → 联合计划注入 → WAIT 有限 holding queue）。
