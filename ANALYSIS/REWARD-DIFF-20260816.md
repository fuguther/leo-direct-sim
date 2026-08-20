# REWARD-DIFF：reward + 观测路径逐分量对照（旧平台修正版 vs leo_sim V2）

> **SUPPORTING EVIDENCE**：分量对照保留；奖励风险是否关闭只以 `FINDINGS-REGISTRY.md` 为准。

> 日期：2026-08-16；2026-08-20 增补训练目标说明。锚点：`ANALYSIS/LEO-V2-ORIGINAL-PLAN.md:86`——「M1 的正确队列奖励和 M2 的本地出向队列观测吸收为统一基线；删除开关」。
> 旧侧证据一律带 `SimulationRL.py` 行号（只读参照 `/Users/lge/Desktop/LEO-Research-Workspace/CODE/`，经 `ANALYSIS/PLATFORM-DOCUMENTATION/02-kimi-platform-spec.md` 索引核对）；新侧证据带本库 `CODE/leo_sim/` 行号。
> 旧平台有 6 个距离奖励版本（V1–V5 + Potential，`distanceRew` 默认 4，SimulationRL.py:590-594 注释称 4 为论文所用）；实际生效路径经调用点确认：`DDQNAgent.makeDeepAction` 7247-7272（`distanceRew==4` → `getDistanceRewardV4`，7264）与到达分支 7169-7177。

## 1. 逐分量对照表

| 分量 | 旧平台（修正版语义） | 新平台（修复前） | 判定 |
|---|---|---|---|
| 队列奖励公式 | `w1·exp(−β·t)`，M1 分支（SimulationRL.py:10289-10291），w1=20（:270）、β=200 s⁻¹（:345） | `queue_reward()` 保留该原始公式作诊断；训练转发奖励再加 `forward_step_penalty`（默认 −20） | **已修**：原始 M1 数值可对照，同时配置不变量保证额外转发跳数不能带来正收益 |
| 队列奖励输入语义 | 包在发送星队列的**实测**排队等待 `checkPointsSend[-1]−checkPoints[-1]`（SimulationRL.py:2052），奖励归属于产生该等待的上一跳转移（7270-7271） | 决策时刻所选链路当前占用比（前瞻代理量）（kernel.py:1380-1383） | **不一致（bug）**：实测后验 vs 决策时前验；修复后改为服务开始时刻结算实测等待（kernel `_transmit` ISL 分支） |
| 队列奖励空守卫 | `if block.queueTime else 0`——从未进过队列（首跳直连）→ 0；实测等待 0（空队列）→ w1=20（SimulationRL.py:7270、10291） | 无此区分 | 不一致→已修：首颗卫星（上行到达）无在途转移可结算，天然等价于旧守卫；实测等待 0 → w1 |
| 距离奖励 | V4：`w2·(SLr − TravelDistance/w4)/biggestDist`（SimulationRL.py:10366-10373；biggestDist 初值 -1、createGraph 8691-8703 更新） | 无（config.py:517-522 校验「distance/linear 被排除出 v1」） | 不一致但**计划内**：v1 只吸收 M1 队列奖励（test_review_round2.py:421-426 注释明示）；列为已知差异，不修 |
| again 回环惩罚 | `againPenalty=−10`（SimulationRL.py:583），命中 `block.QPath` 重访时施加（7242-7245） | 无惩罚；候选过滤直接禁止转回已访问星（kernel.py:1429-1430） | 不一致但**机制替代**：掩码/过滤使回环动作不可选，惩罚无对象；列为已知差异，不修 |
| unav 不可用惩罚 | `unavPenalty=−10`（SimulationRL.py:584），选到不可用方向时存惩罚经验重选（说明书 1715-1717） | 无；动作掩码只含合法方向（learning.py:794-801 `build_action_mask`） | 同上，机制替代，不修 |
| 到达奖励 | `ArriveReward=50`（SimulationRL.py:579），terminal = 距离 + 队列 + 50（7176-7177，distanceRew=4 分支） | deliver 固定 1.0（kernel.py:1377-1378） | **不一致（bug）**：量级与相对权重（50 vs 队列 max 20）破坏；修复为 arrive_reward=50（v1 无距离分量） |
| 丢包终结 | 1-step 基线丢包**不存** terminal 转移（7117-7121 仅 lostBlocks+1 与 fate 日志；仅 multistep/TD-λ flush 以 done=True 落盘 7004/7030/7061） | `_fail` 显式以 `terminal_reward=0.0`、done=True 完结（kernel.py:1498-1509） | 不一致但**有意**：新平台 fail-loud 守恒语义要求每转移显式终结；保留并记录 |
| terminal 的 next_state | terminal 转移存 newState（当前星观测） | terminal 转移 next_state = 到达星观测（deliver）或当前观测（fail） | 一致（语义等价，均不 bootstrap） |
| M2 自身出向队列观测 | 4 维：逐方向 `min(q_dir/infQueue, 1.0)`，infQueue=5000 包（SimulationRL.py:573），缺链路方向记 np.inf→截断 1.0（9077-9092、9872-9875），追加在状态尾部 | `own_state` 4 维 = [接入槽占用比, **全方向聚合**队列比, 可见小区比, 1.0]（learning.py:532-541），逐方向信息被聚合丢失 | **不一致（bug）**：M2 的逐方向出向队列被聚合掉；修复为逐方向 4 维（N/S/E/W），缺方向按旧 infQueue 语义记 1.0，own 块扩为 7 维 |

## 2. 无法对照项

- **距离奖励 V4 的数值等价**：v1 计划内排除距离奖励，无新侧对应物，无法也不需数值对照。若未来恢复距离奖励，须重做 golden 对照（V4 公式依赖全局 `biggestDist` 运行时归一因子，SimulationRL.py:585、8691-8703）。
- **旧平台丢包无 terminal 转移 vs 新平台 terminal 0.0**：语义层差异（旧侧根本无此转移），无法数值对照；新侧行为更利于收敛信号归因，保留。
- **队列单位**：旧侧队列以「包数」计（infQueue=5000 包），新侧以「比特」计（isl_queue_bits=256 Mbit）。M2 观测对照按归一化占用比等价，绝对量纲不可对照。

## 3. 修复内容（本 PR）

1. `learning.queue_reward(wait_s, w1, beta)`：逐字实现 M1 公式，golden 测试按公式用 math 重算（测试注明出处行号）；`forward_reward()` 在训练路径追加逐跳成本。
2. kernel：ISL 服务实际开始时刻（`_transmit` 通过可用性检查处）结算 `pkt.learning_reward = forward_reward(实测等待, ...)`；deliver 动作 reward = `arrive_reward`（默认 50）；转移完结时 reward 缺失即 fail-loud（KernelError），不允许静默存 None。
3. `learning.own_state`：聚合队列比 → 逐方向 N/S/E/W 占用比（M2 语义），own 块 4→7 维，全合同观测维度 +3。
4. config：`learning.reward_w1=20.0`、`learning.reward_beta=200.0`、`learning.arrive_reward=50.0` 入库并可校验。

## 4. 回归防漂移

- `CODE/leo_sim/tests/test_reward_migration.py`、`test_reward_objective.py`：M1 原始公式 golden 值、M2 逐方向 golden 值、端到端实测等待/到达奖励，以及“非正逐跳成本”与非法配置反例。

## 5. 边界

`4163226` 只关闭“按跳正收益/额外转发刷分”这一已知风险。它没有证明 shaped reward 与“按时交付、少拥塞、低时延”的物理字典序目标等价；该目标仍由 R6-F3 的 Q0 合同负责，正式上界不得直接把本训练奖励当作最优性判据。
- 已一致项（B3 真 Double-DQN：online argmax + target eval + next mask，learning.py:804-825）由既有 `test_learning.py` / `test_acceptance_review.py` 固化，本次未动。
