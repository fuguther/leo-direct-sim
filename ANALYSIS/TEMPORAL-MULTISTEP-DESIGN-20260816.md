# M2 temporal/multistep 迁移设计稿

> 日期：2026-08-16。状态：**只交设计稿**（任务 6 允许的降级路径），实现留后续工作包，理由见 §6 工作量评估。
> 迁移依据：`MIGRATION-BACKLOG-20260816.md` M2 行——routing_multistep 三函数在旧平台无运行时调用（nstep 两函数纯参照；lambda_return_transitions 仅 `_tdl_flush` 调用），**以 SimulationRL.py:6980-7062 内联版为准**；temporal 以 `temporal_encoder.py` 为参照。迁移统一要求：先 golden 表征测试，再实现转绿；观测/奖励语义以任务 1 的 REWARD-DIFF 结论为基准。

## 1. 旧侧参照清点（全部经说明书索引核对）

### multistep（n-step / TD-λ）

| 项 | 位置 | 语义 | 运行时使用 |
|---|---|---|---|
| `_ms_store` | SimulationRL.py:6980-7012 | 每包滑窗：(s,a,r) 追加 `block.ms_buf`；窗满 `_SIM_NSTEP` 时以最老跳的 N 步折扣回报 + 自举 s_new 落一条并左移；terminated 时把窗内全部前缀折扣回报以 done=True 落盘并清空 | 是（`SIM_MULTISTEP` 主路径） |
| `_ms_flush_lost` | :7014-7031 | 丢包时的窗内 flush | 是 |
| `_tdl_store` / `_tdl_flush` | :7033 / :7042-7062 | TD(λ)：只累积轨迹，terminal 时调 `lambda_return_transitions`，value_fn = 当前 online 网 `max_a Q`（7055-7057），每跳以 done=True 存回放 | 是（`SIM_TD_LAMBDA>0`，与 n-step 互斥 :453-459） |
| `nstep_transitions` | routing_multistep.py:36 | 离线整段 n-step 换算（纯 numpy）；五元组契约 `(state, action, R, bootstrap_state, done)` | 否（无调用点） |
| `nstep_transitions_streaming` | routing_multistep.py:69 | 流式滑窗参考版，自述与离线版同多重集合 | 否（无调用点；6986 docstring 称内联版曾对它验证） |
| `lambda_return_transitions` | routing_multistep.py:109 | 前视 λ-回报；恒 done=True、bootstrap=None | 仅 `_tdl_flush`(:7052/7060) |

关键数学（golden 锚点）：
- n-step：`R_k = Σ_{i<n} γ^i·r_{k+i}`，bootstrap 状态 = 第 k+n 跳状态，done=False；窗口越界则折扣累加到终点、done=True（routing_multistep.py:51-65）。
- TD(λ)：前视 λ-回报，λ 加权各 m-step bootstrap 项 + 全程 MC 项（routing_multistep.py:113-116 docstring 公式）。

### temporal（时序编码）

`temporal_encoder.py`（272 行，纯决策 hook，无仿真语义）：
- 三模式：`none`（直通）/`framestack`（K 帧拼接，不足 K 帧首帧左补齐，141-149）/`gru`（共享参数 GRU 单步推进 + 自监督下一帧预测训练，183-239），env `SIM_TEMPORAL_MODE` 选择（48-54）。
- 维度契约：`output_dim(base)`——framestack → `base*K`；gru → `base+units`（85-97）。
- 每卫星状态挂在 sat 对象（`_te_frame_buf/_te_hidden/_te_seqbuf`）；星座移动/ISL handoff 后 `reset_satellite` 清空（111-121，调用点 SimulationRL.py:5262-5269）。
- 与 MAPPO frame-stack 互斥（100-108）。
- GRU 权重 save/load：`temporal_gru.npz`（242-267）。

## 2. 新平台接入点分析

### 2.1 multistep → learner 合同

新平台学习转移唯一入口是 `learner.remember(state, action, reward, next_state, next_mask, done)`（kernel.py `_finish_learning_transition`）。n-step/TD-λ 的滑窗必须**按包分组**——多包转移在 remember 流中交错到达，而旧平台把窗挂在 `block.ms_buf`（每包一个）。

**合同缺口**：`remember` 当前不传包标识，learner 侧无法分窗。两个方案：

- 方案 A（推荐）：`remember(..., packet_key=None)` 增加可选参数，kernel 传 `pkt.pid`。多步包装器 `MultistepLearner` 装饰在 `TensorflowDDQN`/`TabularQLearning` 之外：按 packet_key 维护滑窗，产出换算后的五元组再调内层 remember。choose 直通。优点：kernel 只改一处签名、内层算法零改动、表格/深度两臂同享。
- 方案 B：窗挂 `DataPacket`（对齐旧 block.ms_buf），kernel 在 `_finish_learning_transition` 里做滑窗换算。缺点：训练目标逻辑进 kernel，污染分层；否决。

**与掩码合同的交互**（新平台特有，旧平台无 next_mask）：n-step 自举的 `next_mask` 必须取**第 k+n 跳状态的掩码**（即窗内最新转移的 next_mask），不是最老跳的；滑窗条目须携带各自的 next_mask。丢包 flush：新平台丢包是显式 `terminal_reward=0.0, done=True`（任务 1 已定为有意差异），前缀 flush 语义与旧 `_ms_flush_lost` 对应但终值定义不同——差分测试须按新语义写 golden，不与旧逐数值对照（记「无法对照」项）。

**reward 语义**：多步回报的每个 r 即任务 1 修复后的 M1 实测队列奖励/到达奖励/丢包 0，无需再改。

### 2.2 temporal → 观测组装

新平台观测唯一组装点：`learning.build_observation`（+ kernel `_learning_observation`）。接入设计：

- **framestack**：在每颗卫星维护 K 帧 deque（状态挂 kernel 侧 per-sat，非模块全局——旧平台挂 sat 对象，新平台挂 `Kernel` 的 per-sat 列表，避免旧式模块全局态）。`_learning_observation` 返回后拼接。维度 = `CONTRACT_DIMS[c]*K`，NN input_dim 由合同派生处统一改（`TensorflowDDQN.__init__` 的 input_dim 计算点）。**无未来信息风险点**：帧缓冲只追加当前时刻观测，天然满足；reset 时机 = 拓扑变化（新平台拓扑静态，但 GSL 切换/接入变化不重置——旧平台 reset 是因邻居集变化，新平台 ISL 邻居静态，故无需 reset 钩子，设计稿记录此差异理由）。
- **gru**：自监督 GRU 需 TF，本地不可验证；且其收益假设（时序记忆帮助拥塞预测）与信息年龄主线相关但非前提。建议：**v1 只迁 framestack**，GRU 列为后续工作包（需 VM TF 验收）。

### 2.3 配置面（草案）

```
learning.multistep: "none" | "nstep" | "tdlambda"   # 默认 none
learning.nstep_n: int >= 1                            # 旧 _SIM_NSTEP
learning.tdlambda: float in [0,1)                     # 旧 SIM_TD_LAMBDA；与 nstep 互斥（对齐旧 :453-459）
learning.temporal: "none" | "framestack"              # gru 留后续
learning.temporal_k: int >= 1                         # 旧 SIM_TEMPORAL_K=4
```

与 checkpoint/eval 的交互：维度变化 → eval checkpoint 形状校验已有（TensorflowDDQN 检查 input/output shape），自然覆盖；表格臂不受影响（哈希键）。

## 3. 验证计划（实现时的完成标准）

1. **golden 表征测试**（本地可跑，纯 numpy）：按 §1 公式重算 `nstep_transitions` / `nstep_transitions_streaming` / `lambda_return_transitions` 的手工小轨迹 golden（3-5 跳、γ=0.9、n=2、λ=0.8），注明公式出处行号。新实现的流式滑窗与离线换算**同多重集合**（复刻旧平台 streaming↔离线对照的验证思路，routing_multistep.py:70-79 docstring）。
2. **差分测试**：同 seed 同 trace，multistep=none vs nstep=2 两臂——转移数/守恒/fates 的差必须可归因（决策快照 diff 定位）；n-step 转移总数 = Σ 每包跳数（前缀 flush）解析断言。
3. **维度合同测试**：framestack K=4 时观测维 = 4×基线维，NN input 匹配，eval checkpoint 形状不符 fail-loud。
4. **无未来信息**：观测对 t+Δ 几何摄动不变（验收阶梯 M-8 的捕获测试一并补上）。
5. VM 侧：DDQN+nstep 的 train/eval 全链 + receipt（本地无 TF，只能 VM 验收）。

## 4. 与主线（信息年龄）的关系

framestack 给策略提供队列/占用的短窗口历史，是「信息年龄」的**自身记忆侧**对照臂；n-step/TD-λ 改变信用分配跨度，影响长依赖（多跳拥塞）下年龄信息的利用率。两者都是主线的机制层对照件，非工程还债。

## 5. 风险

- n-step 自举掩码取错跳（取最老跳 mask）会静默合法化当时不可行动作——golden 测试必须覆盖掩码传递。
- 丢包 flush 的新旧终值语义不同（显式 0.0 vs 旧无前缀终结），文档与测试都要写明，防止误当 bug。
- framestack 维度膨胀 ×K 对 GAT/MPNN 图合同未定义——v1 framestack 只支持向量合同（C1/C3-C7），图合同组合先 fail-loud 拒绝。

## 6. 工作量评估（为何只交设计稿）

实现量：合同签名变更（remember + packet_key）+ MultistepLearner 包装器 + framestack 观测管线 + 配置面 + 三组测试 ≈ 两个 PR 的承重改动（动 learning 合同与 kernel 学习路径，按 AGENTS.md 13 条需独立冷启动复核）。且 DDQN 臂本地无 TF 无法验收，半实现=未验证代码，违反「禁止把 import 成功当完成证据」。判断：今夜只交设计稿，实现按 §3 验证计划拆 PR-1（纯回报换算+golden）/PR-2（接线+差分）后续做。
