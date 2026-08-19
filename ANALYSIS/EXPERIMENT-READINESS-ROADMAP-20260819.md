# 从当前状态到可跑正式实验的路线图

## 总目标

在不把未复核承重改动混入正式实验的前提下，把 leo_sim V2 收敛到：

1. 平台物理/信息/奖励语义有可追溯差距账本；
2. 连续三轮、Codex + 独立模型 + 网页 GPT 没有新增 blocking/major 问题；
3. 一条真实 VM 实验从编译、审阅、授权、部署、运行、自然结束到分析重算闭环；
4. 冻结实验合同后，按实验文档逐项产出可复现结果。

## 原目标完成度

| 原目标阶段 | 当前判定 | 证据/未完成项 |
|---|---|---|
| 第 0 阶段 0.1 台账 | 已完成 | `FINDINGS-REGISTRY.md` 已建立并实际使用 |
| 0.2 审阅轮次纪律 | 已完成 | 轮次上限、增量审阅、minor 收敛规则已落地 |
| 0.3 独立审阅 | 部分完成 | 有 DeepSeek/GPT 实例；D1 REQUEST_CHANGES，D2 尚待冷启动复核 |
| 0.4 调度恢复 | 已完成 | ProjectPilot 修复与 550/550 测试证据在 NOTES |
| 0.5 VM/TF 前置 | 已完成/需当前运行复核 | 清单已入文档；当前 VM 在线及新 commit 部署状态未在本次核实 |
| P0 等价优化 | 已完成 | 几何缓存、hop BFS 有差分 ledgers 与测试证据 |
| P1 已知缺陷 | 部分完成 | 代码分支存在，但 #25/#26/#28 等仍有待合并/拍板记录 |
| P2 设计稿 | 部分完成 | reward、temporal、link budget、Q0 文档已有；组合矩阵尚未正式定稿 |
| 旧平台全面差距枚举 | 进行中 | D1-D10 已有；本文件补充目录，但三轮审计尚未完成 |
| Q0 快照接口 | 已完成 | #40 已合入且有独立复核 |
| Q0 规划注入接口 | 未完成 | 尚未实现 |
| Q0 tiny 原型 | 未完成 | CP-SAT/event DP 尚未实现 |
| 正式实验闭环 | 有历史验证，当前合同未冻结 | 旧基线链可跑；D1/D2 新语义尚未形成正式可用 commit |

## 推荐目标拆分

### R0：平台可实验门（先完成）

- D1 修复并独立复核；D2 独立复核并合入或明确降级。
- 完成旧平台差距账本逐项状态，D8 做直接字段核验。
- 收口已知 P1 行为修正和 Q0 合同阻塞项。
- 运行一次当前 main 的 VM smoke，并保存部署 SHA、自然结束 receipt、artifact 和分析验证证据。

### R1：实验合同冻结

- 冻结研究问题、主指标、信息集、算法臂、seed、负载档和统计规则。
- 先做 pilot，不把 pilot 当论文结论。
- 明确 Q0-I、Q0-J、Q0-F，不能用一个“全局上界”名称混在一起。

### R2：Q0 最小闭环

- 完成规划结果注入接口。
- tiny 场景实现 event DP 与 future CP-SAT/MILP 交叉验证。
- planned-vs-executed 逐事件核对，失败回到 R0。

### R3：正式实验

- 按实验矩阵逐组提交 request，经过编译、三方审阅、授权、VM 运行和分析重算。
- 所有结果只存实验产物，不入库；论文 claim 只引用 eligible artifact。

## 当前实验目录

现有文档至少包含两条实验线：

- 路由观测/AoI 线：`ANALYSIS/ROUTING-OBSERVATION-AGE-20260814/07-experiment-plan-20260814.md`
  与 `08-experiment-matrix-20260814.md`，包含跳数、聚合、特征消融、年龄信息实验。
- 平台验收/机制线：`EXPERIMENTS/`、`ACCEPTANCE-LADDER-20260816.md`，用于 direct/k-hop/BBM/MBB/GE
  等机制验收，不等同于算法效果实验。

Q0 线当前只有算法选型和接口设计，规划注入与 tiny 原型尚未完成，不能把它写成“已有正式实验结果”。

## 2026-08-19 当前执行状态

- D1 当前候选分支 `codex/20260819-d1-dynamic-rate`，最新提交
  `9ae6a71294419dc31cc6b24771aeeb91b14ed285`；本地 `CODE/leo_sim/tests` 全量
  `407 passed`。该数字只证明测试通过，不等于独立复核通过；独立复核 operation
  `offload-operation:8115689838821c1d7a5994fbb0a18d77` 在本次记录时仍为
  `DISPATCHING`，因此 D1 仍不得合并、部署或用于论文结论。
- D2 当前候选分支 `codex/20260819-d2-holding-integration`，最新提交
  `0cff2547c59ca2d8f66d690f6b922d6bf71588b9`；本地 `CODE/leo_sim/tests` 全量
  `414 passed`。该数字只证明测试通过，不等于独立复核通过；独立复核 operation
  `offload-operation:f854226eae8ed24762dbc893ce51d16e` 在本次记录时仍为
  `DISPATCHING`，因此 D2 仍不得合并、部署或用于论文结论。
- Q0 当前分支已包含 Q0-I tiny DP 和第一阶段 planned-vs-executed 门禁，平台全量
  `417 passed`；复核 operation `offload-operation:dbd05d1ac037396821a4c375e70242c1`
  在本次记录时仍为 `DISPATCHING`。Q0-F 未来时间线、CP-SAT/MILP 交叉验证和完整
  逐事件轨迹门禁仍未完成。
- 实验矩阵是**设计冻结稿**，不是运行结果：E0 选档 → 全臂工程 pilot → 跳数 →
  聚合 → 特征消融 → 信息年龄；各实验的正式 seed、配对单位、主指标和统计规则已
  记录，但 E0 尚未在当前候选代码上重跑，实验合同仍未达到正式授权门。
- 当前可跑的是已有 V2 基线/机制验收链；不能把 D1/D2 未复核版本或未完成 Q0
  参照产生的数据当正式论文结论。
