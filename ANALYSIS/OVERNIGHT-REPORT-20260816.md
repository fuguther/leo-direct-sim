# 隔夜工作晨报（2026-08-16）

> 范围：任务队列 1–8。工作方式：每任务独立分支 + PR，CI 绿自动合并，NOTES.md 逐条留痕。无任务卡死；无用户授权事项触发停止条件。

## 1. 任务状态总览

| # | 任务 | 状态 | PR | 产出 |
|---|---|---|---|---|
| 1 | reward + 观测逐分量对照 | **完成（发现 3 个漂移 bug 并修复）** | #11 | `ANALYSIS/REWARD-DIFF-20260816.md`、`test_reward_migration.py` |
| 2 | 手工可算最小场景 | 完成（4 场景） | #12 | `test_analytic_scenarios.py` |
| 3 | 决策级差分快照 | 完成 | #13 | kernel decision sink + comparison 双臂 decisions.jsonl |
| 4 | 验收阶梯成文 | 完成 | #14 | `ANALYSIS/ACCEPTANCE-LADDER-20260816.md` |
| 5 | 迁移 M1 Q-Learning 表 | 完成 | #15 | `learning.TabularQLearning` + `test_qlearning_migration.py` |
| 6 | M2 temporal/multistep | **部分：按任务授权的降级路径只交设计稿** | #16 | `ANALYSIS/TEMPORAL-MULTISTEP-DESIGN-20260816.md` |
| 7 | 链路预算表征测试 + 集成设计稿 | 完成（设计稿范围内） | #17 | `test_link_budget_characterization.py`、`ANALYSIS/LINK-BUDGET-DESIGN-20260816.md` |
| 8 | 性能 profile 基线 | 完成 | #18 | `ANALYSIS/PERF-PROFILE-20260816.md` |

## 2. 合并 PR 清单与 CI 证据

| PR | 主题 | CI（GitHub Actions pytest） | 本地全量（CI 范围：CODE/leo_sim/tests + CODE/tests） |
|---|---|---|---|
| #11 | fix: reward/观测迁移对齐 | pass 14s | 319 passed / 0 failed（基线 313） |
| #12 | test: 解析最小场景 ×4 | pass 16s | 323 / 0 |
| #13 | feat: 决策快照 JSONL | pass 17s | 329 / 0 |
| #14 | docs: 验收阶梯 | pass 15s | 329 / 0（无代码） |
| #15 | feat: TabularQLearning | pass 18s | 338 / 0 |
| #16 | docs: temporal/multistep 设计稿 | pass 18s | 338 / 0（无代码） |
| #17 | test: 链路预算表征 + 设计稿 | pass 16s | 342 / 0 |
| #18 | docs: 性能基线 | pass 20s | 342 / 0（无代码） |

全部经 `gh pr merge --auto --squash --delete-branch` 在 CI 绿后自动合并；分支已远端清理。

## 3. 发现的 bug 清单（带行号）

任务 1 确认的三处迁移语义漂移（锚点：LEO-V2-ORIGINAL-PLAN.md:86「M1 正确队列奖励 + M2 本地出向队列观测吸收为统一基线」）：

1. **队列奖励公式漂移**：新平台为 `exp(−队列占用比)`（kernel.py 原 1381-1383），应为 M1 修正版 `w1·exp(−β·t)`（w1=20、β=200 s⁻¹；旧 getQueueReward M1 分支 SimulationRL.py:10289-10291）。输入量纲（占用比 vs 实测排队秒数）、量级（max 1 vs 20）全错。
2. **奖励时机/语义漂移**：新平台在决策时刻用所选链路当前占用（前验代理）；旧平台用包在上一跳队列的**实测**等待（SimulationRL.py:2052 checkPointsSend−checkPoints）。已修：ISL 服务实际开始时刻结算（kernel `_transmit`）。
3. **M2 观测丢失逐方向信息**：新 own_state 为全方向聚合队列比（learning.py 原 532-541）；旧 M2 为逐方向 4 维占用、缺方向按 infQueue 截断记 1.0（SimulationRL.py:9866-9875、9077-9092）。已修：own 块 4→7 维。
另：deliver 奖励 1.0 → 50（旧 ArriveReward，SimulationRL.py:579），保持队列奖励（max 20）与到达奖励的相对量级。

**非 bug 的有意差异**（记录在 REWARD-DIFF，未改）：距离奖励 v1 计划内排除；again/unav 惩罚由掩码/候选过滤机制替代；丢包显式 terminal 0.0（旧 1-step 基线丢包不存终结转移，SimulationRL.py:7117-7121）。

**非本队列发现**：`CODE/experiment_platform/tests` 5 个失败为 main 既有（缺 `EXPERIMENTS/EXP-20260715-VM-SMOKE-R04/request.json`、`ANALYSIS/paired_analysis.py`，不在 CI 范围）——已在 clean main 复验与本队列无关，处置方式待用户决定（修或移除）。

## 4. 「无法对照」项及原因

- **距离奖励 V4 数值**：v1 计划内排除，无新侧对应物；恢复时需重做 golden（V4 依赖全局运行时归一因子 biggestDist，SimulationRL.py:585、8691-8703）。
- **丢包终结转移**：旧 1-step 基线无此转移，新平台显式 terminal 0.0——语义层差异，非数值可对照。
- **队列单位**：旧包数（infQueue=5000，SimulationRL.py:573）vs 新比特（isl_queue_bits）——按归一化占用比等价，绝对量纲不可对照。
- **旧臂逐跳候选集/观测**：旧平台只读禁止修改，其非学习策略不记录逐跳候选/观测——决策快照旧臂只能到「每包路径」粒度（packet_fate_log，SimulationRL.py:1292），字段置 null 并注明。
- **旧多步/TD-λ flush 终值**：与新平台丢包 terminal 0.0 语义不同，差分时按新语义写 golden（设计稿 §2.1）。
- **NN/DDQN 热路径数值**：本机无 TF，旧 SimulationRL.py 模块级 import TF 不能 import；所有旧函数 golden 均按说明书核对公式以 math/numpy 重算并在测试注明出处行号。

## 5. 各任务要点

- **任务 3**：决策快照为 output-only，行为不变由同场景有/无 sink 双跑 10 键全等证明（fates/totals/deliveries/occupied/queue_area/access/service_log/handover/events_processed）。
- **任务 5**：TabularQLearning 纯 numpy 无需 TF；eval 不更新表；receipt 新增 qlearning 分支（q_table.json SHA + 计数器对账）；E2E（真控制面+hop 路由）+ receipt verify 通过。合同适配（连续观测哈希键、V2 ε 调度、V2 reward 喂入）在类 docstring 逐条声明。
- **任务 6**：只交设计稿的理由——实现涉 learning 合同承重改动（remember 需 packet_key 扩展；按 AGENTS 13 条需独立复核）且 DDQN 臂本地无 TF 不可验收。拆 PR-1（纯回报换算+golden）/PR-2（接线+差分）留后续。
- **任务 7**：关键发现——旧 `get_data_rate` 的 shannonRate 不进返回值（输出为 MCS 门限量化速率，SimulationRL.py:8315 vs 8318-8326）；旧 RF 参数下 6000 km（新平台默认 max_isl_km）速率=0，新平台常数 1 Gbps 长距不可由旧预算复现。
- **任务 8**：热点=路由最短路几何重算 ~49%（ecef 290 万次调用）+ 接入/切换可见性扫描 ~26%；事件循环自身 ~2-3%；优化优先几何查询缓存（须守无未来信息合同）；GPU/并行不成立；NN 热路径待 VM 补测。

## 6. 待用户决定事项

1. `CODE/experiment_platform/tests` 5 个 main 既有失败：修（补缺失资产或改写测试）还是移除（删测试须用户批准删除路径）。
2. 链路预算 MCS 门限表：沿用旧表（可差分对照，出处未注明）还是换标准 DVB-S2X 表（可辩护但偏离旧数值）。
3. 速率是否进学习观测（v1 设计稿默认不进）。
4. 任务 6 设计稿的两阶段实现是否启动、何时启动（PR-1 本地可做；PR-2 DDQN 臂需 VM TF 验收）。
5. VM 侧遗留（延续既有待办）：/tmp  salvage 目录去留、学习热路径性能补测。

## 7. 下一步建议（按主线相关度）

1. 修复 main 既有 experiment_platform 测试失败（待拍板后）。
2. 任务 6 PR-1：纯回报换算模块 + golden（本地可完整验收）。
3. 链路预算 mcs 速率模型集成（待表选择拍板）。
4. 几何查询缓存优化（依任务 8 基线，先优化前后各跑一次同一 profile 对照）。
