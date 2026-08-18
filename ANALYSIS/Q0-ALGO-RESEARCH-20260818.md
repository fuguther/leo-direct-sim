# Q0 完全信息最优算法选型与信息裁剪（2026-08-18 网页双路终稿）

> 来源：僚机 op 13934832（web_chat 双 lane：primary + independent_review，均 EVIDENCE_READY，
> 3 blocking + 9 major，判定 NEEDS_REWORK=设计合同未冻结，不是代码缺陷）。
> 结论为候选证据，Codex 已完成交叉汇总；进入实现前需用户冻结 §5 的合同选项。

## 1. 结论（两路一致）

1. **必须区分三个最优对象**：
   - `Q0-I`：仅知当前全局状态、不知未来，但知转移律 → 严格在线最优。
   - `Q0-J`：联合调度/路由能力上界（可与 Q0-I 不同信息集）。
   - `Q0-F`：已知完整未来（clairvoyant）的离线最优 → 唯一能用"全局信息"名义称为数值上界的对象。
   把 Q0-F 的 MILP 直接叫"当前信息上界"会把未来信息优势错误归因为完全当前信息优势。
2. **Q0-I 的理论精确族**：完整 Markov 状态上的事件驱动 SMDP/PDMP 动态规划
   （已知转移律时）；状态爆炸，只适合极小实例（≤ 2-3 星、少量包）。
3. **Q0-F 的精确上界**：包粒度、连续/事件时间、非抢占的 MILP/CP-SAT，
   在固定未来 trace 上求解（显式建模 deadline、GE/几何中断、有限队列、不可分包）。
   **普通时间扩展网络流 / min-cost flow 只能做松弛上界或候选路径**——
   其流体化/可抢占/可分流的假设与当前平台包模型不等价。
4. **Q0-I 的可扩展近似**：rolling-horizon MILP/MPC（每步用当前快照 + 有限未来窗口）。
5. **最优性指标**：lexicographic 物理目标（按时交付包数 → 队列成本 → E2E 时延）；
   M1 shaped queue reward 与物理目标不序等价，**不能**作为 Q0 最优性判据，只作对照诊断。
6. **tiny 原型**：Q0-I 用 memoized event DP；Q0-F 用 CP-SAT 交叉验证同一场景；
   千包级改 rolling horizon / online control。

## 2. 四层证据

- **文献**（评审引用，均在 /tmp/q0_research.txt 证据列表）：SMDP/PDMP 动态规划经典
  （MDP/optimal control 线）、连续时间调度 MILP 与 deadline-aware 网络流、
  在线/滚动时域最优控制（receding horizon MPC）文献链；具体 DOI 以原文为准。
- **数学**：Q0-F 的精确模型=事件时间 MILP（每个包决策变量+链路服务/中断事件约束）；
  Q0-I 的精确模型=Bellman 最优方程 over 全局状态；min-cost flow 是 LP 松弛（可分性丢失）。
- **复杂度**：MILP 包粒度变量数 O(P·E·H)，小规模可精确、千包级不可行；
  DP 状态=全局快照×事件集，指数级，仅 tiny；rolling horizon 多项式可控。
- **平台对应**：与 snapshot_global()（#40 已修）契约一致：Q0-I 用当前快照；
  Q0-F 需要未来 trace/时间线注入接口（规划结果注入接口，尚未实现——记入实现清单）。

## 3. 信息裁剪（砍掉一个或两个信息后的算法适用性）

- 砍远端队列 → Q0-I DP/MILP 仍可解但状态空间缩水；滚动 MILP 退化为基于本地+邻域
  的近似；理论最优性保持性依赖"队列信息是否影响转移律"——不影响则仍最优，否则降级。
- 砍远端拓扑 → 同理：若拓扑可预测（轨道力学已知），裁剪只影响观测实现，不影响转移律；
  若拓扑本身随机且不可观测，Q0-I 需 POMDP 或次优（分散 RL/局部贪心）。
- 砍 AoI/信息新鲜度 → 对物理交付目标影响小（AoI 只影响控制面缓存），
  最优算法族不变，但观测表示退化需重训/重标定。
- **判定规则**：裁剪后若被裁信息不进入系统转移律，原最优族仍适用（实现层裁剪）；
  若进入转移律且不可观测，则需换 POMDP/RL/贪心（模型层裁剪）。实现前按 §5 冻结。

## 4. 实现建议

1. 先实现 Q0-F tiny：固定 trace + CP-SAT/MILP 精确解（复用 #40 快照 + trace.csv），
   与 memoized event DP 在 2-3 星场景交叉验证。
2. 再实现 Q0-I tiny：事件 DP + 当前快照；与 Q0-F 差距量化"未来信息价值"。
3. 规划结果注入接口：Q0-F 输出路径/动作序列 → 注入 kernel 决策点（记入 Q0 实现清单）。

## 5. 需用户冻结的合同选项（open items）

- 是否允许控制器用已知轨道力学预测未来 geometry/topology（决定 Q0-I 是否含未来几何窗口）。
- deadline 等时刻的 `>=` vs `>` 与 `service_end==deadline` 语义必须唯一冻结。
- Q0 是否知道未来 traffic arrival、GE/topology 转移律（决定 SMDP 定义完整性）。
- Q0-I 控制能力是否冻结现有 DRR、control priority、forced-deliver、无显式 WAIT。
- tiny 原型中 control advertisement/generation 处理（未知随机/固定外生/关闭）。

## 6. 台账登记

- R6-F1/Q0-I vs Q0-F 区分：open（设计合同，须用户冻结 §5）。
- R6-F3/M1 奖励不可作 Q0 最优性判据：open（设计决策）。
- R6-M*/min-cost flow 仅松弛：open（实现选型已定，文档留痕）。
