# NOTES.md

> ROLLING LOG；最后整理：2026-08-20。
> 本文件只记录最近操作、证据位置和下一步，不是平台状态真相源。
> 当前状态见 `ANALYSIS/CURRENT-EXPERIMENT-READINESS.md`；截至 2026-08-19 的原记录见
> `ANALYSIS/HISTORY/NOTES-THROUGH-20260819.md`。

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

## 2026-08-20：R1-A2 信息边界修复合入

- 隔离分支 `codex/20260820-r1-mask-information` 复现为 FACT：在学习观测不变时，
  `obs_hops` 外的两跳目的地广告会让旧代码开启 forward 动作。
- 修复让学习选路的目的地广告、远端传播与队列指标和 observation 共用 cache-hop
  边界；C1 同时约束当前邻居来源与实际一跳传播。
- #62 head `614fd23` 独立冷启动复核 APPROVE；定向 `41 passed`、仿真内核全量
  `410 passed`、GitHub pytest SUCCESS；squash 合入 main `758b606`，R1-A2 已 fixed。

## 2026-08-20：R7 generic 证据链部分恢复

- PR #64 head `4e6d665` 经独立冷启动复核 APPROVE，Hosted CI pytest SUCCESS；
  squash 合入 main `12bf306`。
- main fresh 验证：当前 CI 范围 `425 passed`；无参数全量
  `470 passed, 1 skipped, 3 subtests passed`。
- 恢复范围仅为 generic `experiment-run-manifest/v2` 的持久化 paired analysis、
  claim schema、严格重验和 CI bridge；`leo_sim_v2` 使用不同合同及结果布局，
  因此 R7-F1 仍为 `open`（generic 部分恢复），不得据此授权正式 V2 实验。
- V2 矩阵 Stage 1 候选 `4664a223` 已收到 REQUEST_CHANGES：真实 launch 授权路径、
  acceptance、配对完整性、checkpoint 血缘、控制变量和 symlink containment 均需返工。

## 下一步

1. 关闭 R7-F1 的 V2 矩阵、artifact 指标重算、paired analysis 与 claim gate；
   generic #64 只作为可复用基础，不代表 V2 完成。
2. 获得所需语义/冲突授权后合入 D1/D2，并更新 CURRENT 中的精确 main/VM 状态。
3. 关闭 R1-A1 与 Q0 replay/Q0-I/Q0-F blocker；保留 R1-A2 回归。
4. 最终冻结平台三轮审计后部署同一 main SHA，重跑 E0 与全臂 pilot。
5. 平台关键门禁不再被文档/Git 清理抢占；回收 worktree 时继续保护 dirty、orphan 与 detached 项。
