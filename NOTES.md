# NOTES.md

> ROLLING LOG；最后整理：2026-08-20。
> 本文件只记录最近操作、证据位置和下一步，不是平台状态真相源。
> 当前状态见 `ANALYSIS/CURRENT-EXPERIMENT-READINESS.md`；截至 2026-08-19 的原记录见
> `ANALYSIS/HISTORY/NOTES-THROUGH-20260819.md`。

## 2026-08-19（有限 holding queue：容量/面积/WAIT 语义）

- 分支：`codex/20260819-holding-queue`。
- 实现 `SatelliteHoldingQueue`，替代 kernel 内部无界 `pending` list 的运行时语义：
  每星 bits 容量、FIFO、`queued_bits`、`QueueArea` 面积、快照占用与 `holding_until`。
- 所有 pending 回退/重决策/Q0 WAIT 写入统一经 `_hold_packet`；容量不足记录独立
  `HOLDING_QUEUE_OVERFLOW` fate，进入数据守恒与 receipt；不再静默无界增长。
- pending ticker 增加 holding deadline sweep；WAIT 只在 `until` 到达后释放，快照可观察等待截止时间。
- 配置新增 `access.holding_queue_bits`，receipt `queue_area_bits_s` 新增 `holding`，机制计数新增
  `holding_queue_overflows`。
- 验证：`pytest -q CODE/leo_sim/tests` = **409 passed**；新增 holding queue/Q0 回归覆盖容量、FIFO、
  面积、overflow fate、快照、WAIT 和 deadline。
- 边界：尚未实现 Q0-I/Q0-F tiny 求解器、planned-vs-executed 回放门禁；D1/D2 仍需独立冷启动复核，
  本分支不得作为论文正式基线。
- 冷启动复核：初审发现 Q0 WAIT 未校验目标卫星，可能把包等待在错误节点；已在 `2d9581e` 修复并
  增加原子性回归。随后静态盘点确认生产路径均经 `_hold_packet`，Q0 位置索引、面积结算和 deadline
  sweep 无遗漏；复核后平台测试为 **411 passed**。

## 2026-08-19（D1/D2 靠拢、旧平台账本与实验路线图）

- 用户已决定 D1 动态链路速率、D2 动态拓扑重匹配按旧平台行为继续推进。
- D1 独立分支 `codex/20260819-d1-dynamic-rate`：原实现 `c0a1f18` 经复核为
  REQUEST_CHANGES；本轮修复零速率快照除零、MCS/控制发送计数时机、ISL 合法掩码、
  GSL 零速率等待唤醒与 FIFO 越过，提交 `5e2d779`，`CODE/leo_sim/tests` 为
  406 passed。仍需不同模型冷启动复核，暂不合入。
- D2 独立分支 `codex/20260819-d2-dynamic-topology`：实现已提交 `7cb11e8`，
  `CODE/leo_sim/tests` 为 400 passed；尚无独立冷启动复核，暂不合入。
- 主分支文档提交 `101088b`：新增 `ANALYSIS/LEGACY-FEATURE-LEDGER-20260819.md`
  和 `ANALYSIS/EXPERIMENT-READINESS-ROADMAP-20260819.md`，并把 Q0 信息裁剪组合矩阵
  补入 `ANALYSIS/Q0-ALGO-RESEARCH-20260818.md`。
- 当前结论：已有基线/机制验收链可以继续做低风险平台验证；D1/D2 未复核版本不能作为
  正式论文实验基线。Q0 调研不再无限扩张，矩阵定稿后进入合同冻结与 tiny 原型。

## 2026-08-19（Q0 合同层与只读计划校验）

- 新增 `CODE/leo_sim/q0.py`：不可变 `PlanAction`/`JointPlan` 合同，版本绑定和未知/重复动作
  fail-closed；Kernel 新增只读 `validate_joint_plan`，校验当前版本、live packet 位置、
  拓扑邻接、服务中/在途不可操作和 ISL 容量预留。
- 回归：`CODE/leo_sim/tests/test_q0_contract.py` 4 passed；平台测试全量 402 passed。
- 明确未完成：`apply_joint_plan`、有限 holding queue、Q0-I/Q0-F tiny 求解器和
  planned-vs-executed 回放门禁仍未实现；本次只完成 Q0 实现顺序第 1 步的一部分。

## 2026-08-19（Q0 计划原子应用）

- `Kernel.apply_joint_plan()` 已接入：第一版只接受 pending 数据包，整份计划先复核版本、
  live 位置、拓扑/容量/GSL 条件，再一次性迁移；非法混合计划不会部分修改。
- 记录 `q0_plan_audit`，成功应用后递增 `state_version`；同一计划内 ISL/downlink 容量按总量校验。
- Q0 合同测试 6 passed；平台全量测试 404 passed。
- 明确边界：尚未把所有 pending 路径统一成有限 holding queue，尚未实现 Q0 tiny 求解器和
  planned-vs-executed 回放门禁；本提交不是正式 Q0 上界结果。

## 2026-08-19（R6-G2b 收口：台账置 fixed）
## 记录规则

- 任务级证据放 PR；本文件只在合并改变当前平台状态、风险或下一步时更新。
- 设计解释写入对应 CURRENT/SUPPORTING 文档，NOTES 只留链接。
- 当前周期结束后原样归档；不得通过压缩删除失败、REQUEST_CHANGES 或未验证记录。
- 实时问题状态只在 `ANALYSIS/FINDINGS-REGISTRY.md` 更新。

## 2026-08-20：文档真相源收敛

- PR #58 已 squash 合并为 `e15c457d71db42e279d3599ecbbe5969608e8261`；主题为
  实验就绪/Q0/平台能力/实验计划真相源收敛。GitHub CI `pytest` SUCCESS（15 s），
  本地 `411 passed`，diff 无删除或移动路径。
- 隔离分支：`codex/20260820-doc-consolidation`，基线 main
  `4c8d38ff38031ae134ae6738b3ebaa405e0f06f7`。
- 开工基线：`python3 -m pytest CODE/leo_sim/tests CODE/tests -q` =
  `411 passed`。
- 新 CURRENT 文档：
  - `ANALYSIS/CURRENT-EXPERIMENT-READINESS.md`：两个平台目标、门禁和带前提工期；
  - `ANALYSIS/PLATFORM-CAPABILITY-LEDGER.md`：当前能力差距与优先级；
  - `ANALYSIS/Q0-INFORMATION-ABLATION-PROTOCOL.md`：从最优向下裁剪为主、
    从现实向上增加为辅；
  - `ANALYSIS/EXPERIMENT-PROGRAM.md` 与
    `EXPERIMENTS/experiment-program.yaml`：实验总计划与机器清单。
- 已停止把不存在的 `ANALYSIS/paired_analysis.py` 写成可运行入口；正式分析链
  登记为 R7-F1 blocking。clean main 实测：experiment_platform+work =
  `21 passed, 5 failed, 3 subtests passed`；focused identity = `1 failed`，均为缺失绑定输入。
- FINDINGS 补入 R1-A1 奖励正循环与 R1-A2 mask 信息旁路；未把 #43 的局部奖励
  修复冒充为关闭 R1-A1。

## 2026-08-20：当前外部状态核验

- GitHub main = `4c8d38f`；#57 已合入。
- D1 PR #55：head `408d368c...`，CLEAN，CI pytest SUCCESS，未合入 main。
- D2 PR #56：head `6be16cd2...`，CLEAN，CI pytest SUCCESS，未合入 main。
- VM deployment receipt：commit `a2a588d9...`、clean、
  `2026-08-20T01:51:43+08:00`；落后 main 且不含 D1/D2。
- Q0 replay/tiny 是未合入候选并有 REQUEST_CHANGES；Q0-F 尚未完成。
- 上述状态是 2026-08-20 核验快照，后续变化必须更新 CURRENT 文档，不能只追加 NOTES。

## 下一步

1. 合入 Git 生命周期治理；随后按
   `ANALYSIS/GIT-WORKTREE-RECONCILIATION-20260820.md` 对 24 个 clean+merged
   worktree 候选逐条申请回收，保护 3 个 dirty、2 个 orphan 和 5 个 detached 项。
2. D1/D2 合入后更新 CURRENT 文档中的精确 main/VM 状态。
3. 修 R7-F1 正式分析链，再关闭 R1-A1/R1-A2 与 Q0 blocker。
4. 最终冻结平台三轮审计后部署 VM，重跑 E0 与全臂 pilot。
