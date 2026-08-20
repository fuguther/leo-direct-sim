# LEO 路由研究实验总计划

> CURRENT；最后核验：2026-08-20。本文回答“为什么跑、按什么顺序跑、什么证据才算完成”。可机读状态见 `../EXPERIMENTS/experiment-program.yaml`。

## 1. 总研究目标

解释分布式逐跳 LEO 路由的性能受限究竟来自：

- 网络本身没有可优化空间；
- 可用信息不足或过时；
- 决策/聚合能力不足；
- 训练失败或实验链失真。

## 2. 四类实验

| 类别 | 实验 | 目的 |
|---|---|---|
| 平台验收 | VAL-D1、VAL-D2、VM-SMOKE | 证明动态速率、动态拓扑、holding 和部署回执语义正确；不回答算法优劣 |
| 上界诊断 | Q0-I-TINY、Q0-F-TINY、Q0-REPLAY | 分解当前信息、未来信息、控制能力和实际算法的差距 |
| 预实验 | E0、PILOT-ALL | 重新定负载；验证所有 arms 的训练/评估/回执/分析；估计方差和机时 |
| 正式效果实验 | EXP1、EXP2、EXP2B、EXP3 | 依次研究观测范围、聚合架构、信息内容和信息年龄 |

## 3. 完整顺序

### G0 平台冻结

前置：D1/D2 合入；奖励、mask、deadline/Q0 blocker 关闭；正式分析链恢复；最终 commit 三轮审计通过。

产出：冻结 main SHA、审阅 verdict、CI 结果、VM deployment receipt。

### Q0-I-TINY：当前全局因果最优

- 信息：当前全局真值，不知道未来随机实现。
- 控制：先固定现有服务策略，仅优化路由/WAIT；联合调度另列 Q0-J。
- 目的：估计同一当前信息下的决策上限。
- 验收：DP 与独立穷举/第二实现同值；kernel replay 逐事件一致。

### Q0-F-TINY：未来信息上界

- 信息：固定完整未来 trace/中断时间线。
- 算法：事件时间 MILP/CP-SAT。
- 目的：测量未来信息价值，验证 `V_F >= V_I`。
- 验收：可枚举实例交叉一致；所有数据面物理约束保留。

### E0：当前平台负载标定

- 非学习确定性臂；在最终 D1/D2 和正式星座/端点上重新扫描。
- 输出低/中/高档，使低档接近无拥塞、中档可区分、高档明显积压但不完全塌缩。
- 2026-08-15 的 50/100/200 Mbps 与 E1 结果只作历史先验，不能自动沿用。

### PILOT-ALL：全臂工程 pilot

每个计划 arm 至少一个 cell，检查：

- natural_end、conservation、no_info、图截断、checkpoint 与双种子 provenance；
- 训练更新数、reward 曲线、评估探索关闭；
- compile/authorize/run/receipt/analysis 全链；
- 墙钟、内存、方差与失败恢复成本。

pilot 不产生论文效果结论。正式样本量由配对差方差和最小有意义效果决定。

### EXP1：观测跳数

- 固定 GAT、特征、训练预算和控制面传播范围。
- arms：`obs_hops={1,2,3}` × E0 三档。
- 回答：更远局部信息是否有价值，并选后续 `h*`。
- 旧 V2 commit 上的 2026-08-15 90-cell 负结果因平台语义已变化，状态是 `rerun_required`。

### EXP2：聚合架构

- 表 A：同 `h*`、同信息内容，比较 cache aggregation、MPNN、GAT，加非学习最短路锚点。
- 表 B：现状一跳算法 vs 表 A 胜者，明确这是整体系统比较而非纯聚合因果比较。
- 回答：提升来自聚合方式，还是简单路由已经足够。

### EXP2B：信息内容消融

- F0：队列+目的地方向。
- F1：F0+链路速率/可用性。
- F2：F1+逐字段信息年龄。
- 回答：哪类信息有边际价值；与 Q0 信息阶梯对齐。

### EXP3：信息年龄

- G0：无 age；G1：age 进特征不进注意力；G2：age 条件化注意力；G3：窗口内 shuffle age；G4：固定新鲜 age。
- 回答：模型是否因真实新鲜度受益，而不是因为多参数或相关噪声。
- 前置：逐字段 age provenance 和同权重表征测试。

### 条件性补充

- `INT-HOPS-AGG`：只有 EXP1 与 EXP2 结论显示交互时运行。
- `SENS-GRAVITY`：主结论 uniform，gravity 作为敏感性附录。
- 多 OD、temporal、path-credit、FL/CKA、D8 时延分解均按论文 claim 立独立实验，不混进首批矩阵。

## 4. 公平性与统计

- 配对单位是训练 seed × 流量 seed；跨 arm 共用相同 trace。
- 调优、训练、流量、评估 seed 分池且不重叠。
- 先 pilot 冻结样本量、预算、主指标和主对比，再看正式结果。
- 主指标为完成率/按时交付率；同时报告完成包时延、尾部、积压和实际注入流量，避免幸存者偏差。
- 每个正式实验只设 1–2 个主对比；其余标探索性。
- 负结果、学习失败和基础设施失败必须分开。

## 5. 文件与证据形式

| 层级 | 文件 | 作用 |
|---|---|---|
| 项目级人类计划 | `ANALYSIS/EXPERIMENT-PROGRAM.md` | 研究问题、依赖、解释与顺序 |
| 项目级机器清单 | `EXPERIMENTS/experiment-program.yaml` | 稳定 ID、依赖、状态、arms、证据门 |
| 单次正式实验 | `EXPERIMENTS/EXP-*/request.json` | 冻结配置、seeds、指标、验收；经编译和授权 |
| 执行产物 | VM `Results/` | receipt、ledgers、trace、checkpoint、artifact manifest；不入 Git |
| 分析产物 | analysis manifest + summary + report | 从原始产物重算并绑定 hash；当前分析入口待修复 |

YAML 只是计划索引，不能替代 request、授权或自然结束回执。任何状态变化都必须有证据链接，而不能手工把 `status` 改成 completed。
