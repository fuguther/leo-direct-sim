# 片段 s5：CODE/SimulationRL.py 第 10238–12556 行（文件末尾段）

## 文件 `CODE/SimulationRL.py`（实测 12556 行）

> 本片段只覆盖第 10238–12556 行。第 1–10237 行（全部 imports、全局常量/env 读取、`Logger`、`Results`、`DataBlock`、`Gateway`、`Earth`、`hyperparam`、`QLearning`、`DDQNAgent`、`ExperienceReplay` 等类与中部函数）由前序片段覆盖。
>
> 本范围内 `grep -nE '^(class |def )'` 结果：**0 个 class、35 个 def**。另有 1 个模块级 `if __name__ == '__main__':` 块（12528–12556）。

### 模块级说明（仅限 10238–12556 范围）

- **10255–10257、11490–11492、12018、12523–12526**：注释分隔带（`#####...`），分别标注 `Q-Learning - Rewards`、`Simulation && Results`、`Main` 三个分节，无代码 (FACT)。
- **12528–12556 `if __name__ == '__main__':` 块**（模块级可执行代码，FACT）：
  - 12529：`os.makedirs(outputPath, exist_ok=True)`（`outputPath` 全局变量定义于 653 行的另一个 `if __name__ == '__main__':` 块内，由 `SIM_RESULTS_ROOT` env、pathing、Test length、ArriveReward、w1、w2、GTs、流量标签拼成）。
  - 12530：`sys.stdout = Logger(outputPath + 'logfile.log')`（`Logger` 定义于 173，属前序片段）。
  - 12532–12547：若 env `SIM_WANDB` ∈ {1,true,yes,on}，尝试 `import wandb` 并 `wandb.init(project=WANDB_PROJECT 或 "leo-drl-routing", name=SIM_RUN_LABEL, group=SIM_CFG_PATH_TAG, config=全部 SIM_* env, mode=WANDB_MODE 默认 "offline")`；任何异常打印 `[wandb] init skipped (...)` 并继续（12546–12547）。
  - 12548–12555：`try: RunSimulation(GTs, './', outputPath, populationMap, radioKM=rKM)`；`finally` 中若 wandb run 存在则 `wandb.run.finish()`（异常吞掉）。`GTs`(276)、`populationMap`(663)、`rKM`(292) 均为文件头部全局变量。
  - 12556：注释掉的 `cProfile.run(...)` 替代入口。

#### 本片段消费、但定义于文件头部（1–10237）的全局符号速查（均为 FACT，仅列定义行）

| 符号 | 定义行 | 含义（依定义行注释/代码） |
|---|---|---|
| `pathing` | 226 | 路由方法选择，来自 env `SIM_PATHING`(225)，默认 `pathings[3]`=`'slant_range'`；可选列表见 222 |
| `SIM_ROUTING_MODE` | 231 | DDQN 路由变体（`_parse_sim_routing_mode()`） |
| `_SIM_FAIL_CLOSED` | 219 | env `SIM_FAIL_CLOSED` 开关 |
| `FL_Test` | 234 | CKA/联邦学习测试开关 |
| `plotAllThro` / `plotAllCon` | 236 / 237 | 吞吐图/拥塞图是否逐路径分别绘制 |
| `movementTime` / `ndeltas` | 239 / 241 | 星座位置更新周期 / 运动加速因子 |
| `Train` / `explore` / `importQVals` / `onlinePhase` | 260 / 261 / 262 / 263 | 训练/探索/导入 Q 值/多智能体在线相位开关 |
| `w1` / `w2` / `w4` | 270 / 271 / 272 | 奖励权重（w1、w2 可被 env `SIM_W1`/`SIM_W2` 覆盖） |
| `GTs` / `rKM` | 276 / 292 | 网关数列表 / 网关覆盖半径 km |
| `BLOCK_SIZE` | 318 | 数据块大小（bit），吞吐计算用 |
| `saveISLs` / `const_moved` / `matching` / `mixLocs` | 324 / 325 / 326 / 328 | ISL 图保存/移动标志/匹配算法/网关位置洗牌 |
| `diff_lastHop` | 334 | 29 维状态开关（env `SIM_DIFF_LAST_HOP`） |
| `_SIM_M1_FIX` / `_M1_BETA` | 344 / 345 | 队列奖励 exp 修复开关 / β=200 s⁻¹ |
| `_SIM_REWARD_LINEAR` / `_LINEAR_ALPHA` | 350 / 351 | 线性队列奖励开关（env `SIM_REWARD_LINEAR`/`SIM_LINEAR_ALPHA`） |
| `_SIM_STATE_MODE` / `_SIM_STATE_VIS_K` | 374 / 375 | 状态模式（c2–c7）/ k 跳邻居数 |
| `_SIM_VIS_K_STALE_STEPS` / `_SIM_VIS_K_UPDATE_INTERVAL_S` | 379 / 383 | 过期邻居状态步数 / 定时快照间隔 |
| `_GRAPH_MAX_NODES` / `_GRAPH_HIDDEN_DIM` / `_GRAPH_ATT_HEADS` / `_GRAPH_LAYERS` / `_GRAPH_LOG_EVERY` | 391 / 398 / 399 / 400 / 401 | 图状态编码器配置 |
| `_RAAC_AOI_SCALE_S` / `_RAAC_AOI_GATE` | 395 / 396 | RAAC AoI 门参数 |
| `_SIM_MULTISTEP` | 467 | n-step/TD(λ) 开关（由 `_SIM_NSTEP`、`_SIM_TDLAMBDA_ON` 推出） |
| `_SIM_CSR_MODE` | 474–479 | `SIM_CSR_MODE=csr` 时模块加载即 `raise RuntimeError`（提示 `legacy.routing_csr` 不在保留代码中） |
| `_SIM_CRITIC_GLOBAL` | 499 | 集中式 critic 开关 |
| `ddqn` / `alpha_dnn` | 555 / 559 | DDQN 双网络开关 / DNN 学习率 |
| `plotDeliver` | 564 | 送达路径绘图开关 |
| `winSize` / `markerSize` | 567 / 568 | 绘图滚动窗口 / 散点大小 |
| `ArriveReward` / `againPenalty` / `unavPenalty` | 579 / 583 / 584 | 送达奖励 / 回环惩罚 / 不可用方向惩罚 |
| `biggestDist` | 585 | 距离奖励归一化因子，初值 -1，在 `createGraph`（8655，前序片段）的 8691–8703 行更新 |
| `_SIM_POTENTIAL_SHAPING` / `distanceRew` | 589 / 590 | 势函数塑形开关 / 距离奖励版本选择（默认 4） |
| `MIN_EPSILON` / `LAMBDA` / `decayRate` | 598 / 599 / 600 | ε 下限与衰减参数（均可被 env 覆盖） |
| `stopLoss` / `nLosses` / `lThreshold` | 610 / 611 / 612 | 止损训练开关组 |
| `TrainThis` / `CurrentGTnumber` | 613 / 617 | 单场景训练开关 / 当前网关数 |
| `nnpath` / `nnpathTarget` | 625 / 626 | 预训练网络路径（env `SIM_NN_PATH`/`SIM_NN_TARGET`） |
| `outputPath` / `populationMap` | 653 / 663 | 结果输出目录 / 人口密度 tif 路径（`__main__` 块内定义） |
| `receivedDataBlocks` / `createdBlocks` | 673 / 674 | 全局已收/已建数据块列表 |
| `_SEED` | 680 | 随机种子（env `SIM_SEED`，默认 42；681–686 行播种 np/random/tf） |
| `upGSLRates` / `downGSLRates` / `interRates` / `intraRate` | 688–691 | 链路速率采样列表 |
| `REPLAY_TRACE` / `SIM_FAST_ENV` | 694 / 696 | 回放轨迹开关；`SIM_FAST=1` 时 `REPLAY_TRACE=False`（697–698） |
| `_SIM_GSL_KEEP_STABLE` | 746 | GSL 切换保留稳定链路开关 |
| `_SIM_PATH_CREDIT` | 753 | path-credit 开关（`_env_int`） |
| `_SIM_FAST_TRAIN` | 802 | 编译版训练步开关 |
| `_SIM_CHECKPOINT_FRACTIONS` | 823–833 | 按仿真时间分数存中间检查点的列表（env `SIM_CHECKPOINT_FRACTIONS`，逗号分隔，仅收 (0,1) 区间值） |
| 外部 import `assess_path_credit_effect` / `assess_temporal_effect` / `attempt_checkpoint_load` / `new_checkpoint_receipt` | 27–32 | 来自 `CODE/runtime_effect_receipt.py`（文件已确认存在） |

---

## 函数逐个说明

### Q 表与几何工具

#### `def createQTable(NGT)` — CODE/SimulationRL.py:10238
- 定位：CODE/SimulationRL.py:10238–10252
- 职责：创建并返回一个 6 维全零 numpy 数组作为 Q(s,a) 表：形状 `(3,3,3,3,NGT,4)`，前 4 维为上/下/右/左邻居离散状态（各 3 档），第 5 维为目的网关编号，第 6 维为 4 个动作 `('N','S','E','W')`（10246–10250）(FACT)。函数内 docstring 称「10 GTs 时 4050 values」（10250 行注释）(FACT：注释原文如此)。
- 输入/输出：入 `NGT`（网关数）；出 `np.zeros((3,3,3,3,NGT,4))`。
- 依赖关系：**调用方未确认——CODE/ 全库 grep `createQTable` 仅命中定义行本身**。`QLearning.__init__`(5683) 在 `qTable is None` 时用 `np.random.rand(satUp, satDown, satRight, satLeft, NGT, self.nActions)` 内联初始化（5703–5704），不经过本函数 (FACT)。(INFERENCE：本函数是 QLearning 表初始化的未接线替代/遗留实现。)

#### `def getSlantRange(satA, satB)` — CODE/SimulationRL.py:10261
- 定位：CODE/SimulationRL.py:10261–10265
- 职责：返回两卫星 ECEF 坐标 `(x,y,z)` 之差的 L2 范数，即斜距（米）(FACT)。
- 输入/输出：入两个带 `.x/.y/.z` 属性的卫星对象；出 float（`np.linalg.norm` 结果）。
- 依赖关系：调用 `np.linalg.norm`。被调方：`_set_distance_diag`(1200,1201)、`DDQNAgent.getNextHop`(6879,6894，MAPPO-BP 打分的 progress 项)、同文件 `getDistanceReward`(10309,10310)、`getDistanceRewardV2`(10322,10328–10337)、`getDistanceRewardV3`(10351,10355–10361)、`getDistanceRewardV4`(10368,10369)、`getDistanceRewardV5`(10379)、`getDistanceRewardPotential`(10392,10393) (FACT)。

### 奖励函数群

#### `def getQueueReward(queueTime, w1)` — CODE/SimulationRL.py:10269
- 定位：CODE/SimulationRL.py:10269–10292
- 职责：把排队时延（秒）映射为队列奖励，三个互斥分支 (FACT)：
  1. `_SIM_REWARD_LINEAR` 为真（env `SIM_REWARD_LINEAR`，350）：返回 `-_LINEAR_ALPHA * max(queueTime, 0.0)`（10285–10288）；
  2. `_SIM_M1_FIX` 为真（env `SIM_M1_FIX`，344）：返回 `w1 * math.exp(-_M1_BETA * max(queueTime, 0.0))`，β=200 s⁻¹（10289–10291）；
  3. 默认：返回 `w1*(1-10**queueTime)`（10292）。
- 关键状态/结构：只读全局开关 `_SIM_REWARD_LINEAR`、`_LINEAR_ALPHA`、`_SIM_M1_FIX`、`_M1_BETA`；docstring（10270–10284）记录原公式数值量级问题与 M1 修复的校准说明（FACT：docstring 原文声明）。
- 输入/输出：入 `queueTime`(秒)、`w1`(权重)；出 float 奖励。
- 依赖关系：被 `QLearning.makeAction`(5784) 与 `DDQNAgent.makeDeepAction`(7176,7270) 调用；两处均为 `if block.queueTime else 0` 的守卫调用 (FACT)。

#### `def getDistanceReward(satA, satB, destination, w2)` — CODE/SimulationRL.py:10296
- 定位：CODE/SimulationRL.py:10296–10311
- 职责：距离奖励 V1：`w2*((2*TSLa-TSLb)/TSLa - 1)`，其中 `TSLa=getSlantRange(satA,destination)`、`TSLb=getSlantRange(satB,destination)`，`balance=-1` 使结果以 0 为中心（10307–10311）(FACT)。
- 输入/输出：入当前卫星、下一跳卫星、目的卫星对象、权重 `w2`；出 float。
- 依赖关系：调 `getSlantRange`。被 `QLearning.makeAction`(5783，QLearning 的唯一距离奖励路径) 与 `DDQNAgent.makeDeepAction`(7249，`distanceRew == 1` 分支) 调用 (FACT)。

#### `def getDistanceRewardV2(sat, nextSat, satU, satD, satR, satL, destination, w2)` — CODE/SimulationRL.py:10314
- 定位：CODE/SimulationRL.py:10314–10342
- 职责：距离奖励 V2：`w2 * (SLr / SLav)`；`SLr` 为选 nextSat 带来的到 destination 斜距缩减量，`SLav` 为 4 个方向邻居中非 None 者到 `sat` 的平均斜距（10322–10340）；`SLav == 0` 或无邻居（count=0）时返回 0（10340–10342）(FACT)。
- 输入/输出：入当前/下一跳卫星、4 方向邻居（可 None）、目的卫星、`w2`；出 float。
- 依赖关系：调 `getSlantRange`。被 `DDQNAgent.makeDeepAction`(7253，`distanceRew == 2` 分支) 调用 (FACT)。

#### `def getDistanceRewardV3(sat, nextSat, satU, satD, satR, satL, destination, w2)` — CODE/SimulationRL.py:10345
- 定位：CODE/SimulationRL.py:10345–10363
- 职责：距离奖励 V3：`w2 * SLr / max(SLrs)`；`SLrs` 为各非 None 邻居分别能取得的斜距缩减量列表，取最大值归一（10351–10363）(FACT)。若 4 个邻居全为 None，`max([])` 将抛 `ValueError`（Python 内置语义，FACT）。
- 输入/输出：同 V2；出 float。
- 依赖关系：调 `getSlantRange`。被 `DDQNAgent.makeDeepAction`(7257，`distanceRew == 3` 分支) 调用 (FACT)。

#### `def getDistanceRewardV4(sat, nextSat, satDest, w2, w4)` — CODE/SimulationRL.py:10366
- 定位：CODE/SimulationRL.py:10366–10375
- 职责：距离奖励 V4：`w2*(SLr - TravelDistance/w4)/biggestDist`；`SLr` 为到 `satDest` 的斜距缩减，`TravelDistance` 为本跳实际飞行斜距，`biggestDist` 为全局归一化因子（585 定义初值 -1，`createGraph` 内 8691–8703 更新）（10367–10373）(FACT)。10370–10372 有一个 `if TravelDistance > biggestDist: pass` 空分支（原 print 已注释）(FACT)。10374–10375 有两行注释掉的替代返回式 (FACT)。
- 输入/输出：入当前/下一跳卫星、目的卫星、`w2`、`w4`；出 float。
- 依赖关系：调 `getSlantRange`；读写全局 `biggestDist`。被 `DDQNAgent.makeDeepAction`(7175, 7264，`distanceRew == 4` 且 `_SIM_POTENTIAL_SHAPING` 为假时) 调用 (FACT)。

#### `def getDistanceRewardV5(sat, nextSat, w2)` — CODE/SimulationRL.py:10378
- 定位：CODE/SimulationRL.py:10378–10380
- 职责：距离奖励 V5：`w2 * getSlantRange(sat, nextSat) / 1000000`，只与本跳飞行距离成正比，不含目的地项 (FACT)。
- 输入/输出：入当前/下一跳卫星、`w2`；出 float。
- 依赖关系：调 `getSlantRange`。被 `DDQNAgent.makeDeepAction`(7186, 7268，`distanceRew == 5` 分支) 调用 (FACT)。

#### `def getDistanceRewardPotential(prevSat, nextSat, satDest, w2, gamma=0.99)` — CODE/SimulationRL.py:10383
- 定位：CODE/SimulationRL.py:10383–10394
- 职责：势函数奖励塑形（docstring 引 Ng et al. 1999）：`F = w2*(γ*Φ(next) - Φ(prev))`，`Φ(s) = -getSlantRange(s, satDest)/d`，`d = max(float(biggestDist), 1.0)`（10390–10394）(FACT)。docstring 声明经 env `SIM_POTENTIAL_SHAPING=1` 启用（10388，开关定义于 589）(FACT：docstring 声明与开关定义行)。
- 输入/输出：入上一步/当前卫星、目的卫星、`w2`、`gamma`（默认 0.99）；出 float。
- 依赖关系：调 `getSlantRange`；读全局 `biggestDist`。被 `DDQNAgent.makeDeepAction`(7173, 7262，`distanceRew == 4` 且 `_SIM_POTENTIAL_SHAPING` 为真时) 调用 (FACT)。

### 保存/加载函数群

#### `def saveHyperparams(outputPath, inputParams, hyperparams)` — CODE/SimulationRL.py:10397
- 定位：CODE/SimulationRL.py:10397–10430
- 职责：把星座名、importQ、plotPath、Test length、alpha（QLearning 与全局 `alpha_dnn`）、gamma、epsilon 三件套、ArriveR、w1/w2/w4、again/unav 惩罚、坐标粒度、updateF、batchSize、bufferSize、hardUpdate、explore、ddqn、latBias/lonBias、diff、reducedState、online 等字段格式化为字符串列表，逐行写入 `outputPath + 'hyperparams.txt'`（10399–10430）(FACT)。
- 输入/输出：入输出目录、inputParams（pandas DataFrame，取 `['Constellation'][0]`、`['Test length'][0]`）、hyperparams 对象；出写文件，无返回。
- 依赖关系：读全局 `alpha_dnn`(559)。被 `initialize(...)` 内 8075 行调用（`saveHyperparams(earth.outputPath, inputParams, hyperparams)`）(FACT)。

#### `def saveQTables(outputPath, earth)` — CODE/SimulationRL.py:10433
- 定位：CODE/SimulationRL.py:10433–10444
- 职责：在 `outputPath + 'qTablesExport_{len(earth.gateways)}GTs/'` 建目录，遍历 `earth.LEO` 各轨道面各卫星，把 `sat.QLearning.qTable` 用 `np.save` 存为 `{sat.ID}.npy`（10436–10444）(FACT)。
- 输入/输出：入输出目录、Earth 对象；出每卫星一个 .npy 文件。
- 依赖关系：被 `RunSimulation`(12481，`pathing == 'Q-Learning'` 时) 与 `save_on_interrupt`(11377) 调用 (FACT)。

#### `def saveDeepNetworks(outputPath, earth)` — CODE/SimulationRL.py:10447
- 定位：CODE/SimulationRL.py:10447–10472
- 职责：保存 DDQN 网络权重 (FACT)：
  - 非 `onlinePhase`：`earth.DDQNA.qNetwork.save(outputPath+'qNetwork_{N}GTs.h5')`；若全局 `ddqn`(555) 为真再存 `qTarget_...h5`（10450–10453）。随后 `try: import temporal_encoder as _te_save; _te_save.save(outputPath)`，成功打印「gru weights saved」，任何异常打印 `[temporal] save skipped`（10456–10461；注释说明 GRU 编码器权重与 qNetwork 同目录以便 eval 部署）。若 `earth.DDQNA.routing_mode == "ddqn_csr"`：`from legacy.routing_csr import save_csr_w` 并调用 `_save_w(outputPath, len(earth.gateways), earth.DDQNA.csr_w)`（10464–10466）。
  - `onlinePhase`：遍历逐卫星存 `{sat.ID}qNetwork_{N}GTs.h5`（及 ddqn 时 qTarget）（10467–10472）。
- 关键状态/结构：(FACT) `CODE/legacy/` 目录在当前工作区不存在（Glob `**/routing_csr.py` 与 `**/legacy/__init__.py` 均无匹配）；文件头 474–479 行在 `SIM_CSR_MODE=csr` 时模块加载即 `raise RuntimeError(... legacy.routing_csr, which is not present in retained CODE ...)`，因此 10464–10466 的 csr 分支在当前工作区不可达（INFERENCE：「不可达」是由前两条 FACT 推出的结论）。
- 输入/输出：入输出目录（函数内 `os.makedirs(outputPath, exist_ok=True)`）、Earth 对象；出 .h5/npz 文件。
- 依赖关系：依赖外部模块 `CODE/temporal_encoder.py`（已确认存在）。被 `RunSimulation`(12483) 与 `save_on_interrupt`(11370) 调用 (FACT)。

#### `def save_replay_buffer(outputPath, GTnumber, buffer)` — CODE/SimulationRL.py:10475
- 定位：CODE/SimulationRL.py:10475–10489
- 职责：把 DDQN 经验回放 deque 拆成 `states(float32)/actions(int32)/rewards(float32)/next_states(float32)/dones(bool)` 五个数组，`np.savez_compressed` 到 `outputPath/NNs/replay_buffer_{GTnumber}GTs.npz`（10477–10488）；buffer 为空时打印提示并直接 return（10479–10481）(FACT)。
- 输入/输出：入输出目录、网关数、buffer（元素为 5 元组）；出 .npz 文件。
- 依赖关系：被 `save_on_interrupt`(11414) 调用 (FACT)。

#### `def load_replay_buffer_into(earth, path)` — CODE/SimulationRL.py:10492
- 定位：CODE/SimulationRL.py:10492–10506
- 职责：从上述 .npz 读回五数组，逐条调用 `earth.DDQNA.experienceReplay.store(...)` 重建回放缓冲，返回加载条数；文件不存在时打印提示并返回 0（10494–10496）(FACT)。
- 输入/输出：入 Earth 对象、npz 路径；出 int 条数。
- 依赖关系：被 `RunSimulation`(12119) 在 env `SIM_REPLAY_PATH` 非空且 `pathing == "Deep Q-Learning"` 且非 `onlinePhase` 时调用 (FACT)。

#### `def _save_pc_replay(pc_replay, path)` — CODE/SimulationRL.py:10509
- 定位：CODE/SimulationRL.py:10509–10572
- 职责：把 PathTrajectoryReplay（路径信用轨迹回放）序列化为 .npz (FACT)。内部 `_flatten(bucket, terminal_label)`（10523–10543）把 delivered/lost 两个 deque 摊平成 `(n, max_hops, state_dim)` 零填充的 states float32 数组、`(n, max_hops)` 的 actions int32 / mc_returns float32 数组和 lengths int32 数组；state_dim 从首条轨迹首跳的 `state.shape[-1]` 推断（10530）。另存 `max_hops`、`gamma`、`baseline_delivered`、`baseline_lost`（Welford 基线，10548–10553）。`np.savez_compressed` 落盘并打印条数（10569–10572）。
- 输入/输出：入 pc_replay 对象（需有 `.max_hops/.gamma/.delivered/.lost/.baseline()`）、npz 路径；出 .npz 文件。
- 依赖关系：函数内 `from routing_path_credit import TERMINAL_DELIVERED, TERMINAL_LOST`（10517，`CODE/routing_path_credit.py` 已确认存在）。被 `save_on_interrupt`(11423) 调用 (FACT)。

#### `def _load_pc_replay_into(pc_replay, path)` — CODE/SimulationRL.py:10575
- 定位：CODE/SimulationRL.py:10575–10614
- 职责：上函数的逆操作：文件不存在则 `raise FileNotFoundError`（10578–10579）；恢复 Welford 基线 `pc_replay._mean[TERMINAL_*]`（10583–10586）；内部 `_repopulate(...)`（10588–10607）按 lengths 逐条重建轨迹 dict（`state/action/mc_return`，`reward` 固定填 0.0，注释说明训练只用 mc_return，10602），append 到 delivered/lost 对应 bucket；返回总轨迹数 (FACT)。
- 输入/输出：入 pc_replay 对象、npz 路径；出 int 轨迹数。
- 依赖关系：被 `RunSimulation`(12153) 经 `attempt_checkpoint_load(..., fail_closed=_SIM_FAIL_CLOSED)` 包装调用（env `SIM_PC_REPLAY_PATH` 非空时）(FACT)。

### 回执/审计函数群

#### `def _packet_count_meta(earth)` — CODE/SimulationRL.py:10617
- 定位：CODE/SimulationRL.py:10617–10627
- 职责：返回包计数字典 `{"created": len(createdBlocks), "received": len(receivedDataBlocks), "lost": lost_link_break, "lost_link_break": lost_link_break, "in_flight_at_sim_end": max(0, created-received-lost_link_break)}`，其中 `lost_link_break = int(getattr(earth, "lostBlocks", 0) or 0)`（10618–10627）(FACT)。`"lost"` 与 `"lost_link_break"` 恒为同值 (FACT)。
- 输入/输出：入 Earth 对象；出 dict。
- 依赖关系：读全局列表 `createdBlocks`(674)、`receivedDataBlocks`(673)。被 `save_on_interrupt`(11406) 与 `RunSimulation`(12303) 展开进 replay-trace meta (FACT)。

#### `def _trace_traffic_receipt(earth)` — CODE/SimulationRL.py:10630
- 定位：CODE/SimulationRL.py:10630–10682
- 职责：构造「不可变 trace 流量」的比特守恒终结台账（schema `leo-legacy-trace-receipt/v1`）(FACT)：
  - `earth.trace_traffic_enabled` 为假 → 返回 None（10632–10633）；
  - `earth.trace_traffic_manifest` 不是 dict → 返回 `valid=False` 且 errors 含「manifest is absent」（10634–10640）；
  - 否则从全局 `createdBlocks` 筛出带 `trace_packet_id` 的块，校验：packet id 无重复（10647–10648）、发出包数等于 manifest 的 `offered_packets`（10656–10657）、发出比特数等于 `offered_bits`（10658–10659）、比特守恒 `emitted == delivered + lost + in_system`（10660–10661，按 `trace_terminal_status` 0=delivered/1=lost/None=in_system 分类，10650–10655）；
  - 返回含 trace_sha256、projection（原样回传 manifest）、packets/bits 五元计数（offered/emitted/delivered/lost/in_system_at_stop）的 dict（10662–10682）。
- 输入/输出：入 Earth 对象；出 dict 或 None。
- 依赖关系：读全局 `createdBlocks`。被 `_run_audit_meta`(10833) 与 `RunSimulation`(12309) 调用 (FACT)。

#### `def _git_value(args)` — CODE/SimulationRL.py:10685
- 定位：CODE/SimulationRL.py:10685–10699
- 职责：以本文件所在目录为 cwd 执行 `git <args>`（`subprocess.run`，`capture_output=True, text=True, check=False, timeout=2`），returncode==0 时返回 `stdout.strip()`，任何异常或失败返回 `""` (FACT)。
- 输入/输出：入 git 参数列表；出 str（可为空串）。
- 依赖关系：被 `_run_audit_meta` 调用 3 次：`rev-parse HEAD`(11329)、`branch --show-current`(11330)、`status --porcelain`(11334) (FACT)。

#### `def _run_audit_meta(earth, natural_end)` — CODE/SimulationRL.py:10702
- 定位：CODE/SimulationRL.py:10702–11353（652 行，本片段最大函数）
- 职责：汇总一次运行的「声明值 vs 运行时实测值」审计元数据，产出 mismatches 清单与 `research_eligible` 判定，作为 replay-trace meta 的一部分 (FACT)。
- 关键状态/结构：内部子结构 `_effective_receipt`（schema `leo-effective-receipt/v1`，11149–11310），顶层返回 dict（11312–11353）。
- 关键流程（按行号分阶段，均 FACT）：
  1. **定位 agent 与图编码层**（10703–10718）：取 `earth.DDQNA`，为空则遍历 `earth.LEO` 各卫星找第一个带 `DDQNA` 者；再取 `qnet = ddqna.qNetwork`，尝试 `qnet.get_layer("graph_encoder")`。
  2. **参数计数工具**（10720–10728）：内部 `_count_params(obj, trainable=False)`，trainable 时累加 `trainable_variables` 元素数，否则 `obj.count_params()`，异常返回 None。
  3. **解析声明侧 env JSON**（10730–10748）：`SIM_SCENARIO_IDENTITY_JSON`、`SIM_INFORMATION_CONTRACT_JSON`、`SIM_EXECUTION_SEMANTICS_JSON`，解析失败一律置 None。
  4. **推导执行语义**（10749–10767）：`_effective_execution_semantics`：`kind` = learning（pathing ∈ {Deep Q-Learning, Q-Learning}）否则 non_learning；`run_phase` = evaluation/training/non_learning（看 `SIM_RL_EVAL` env）；`dormant_config_paths` 非学习时为 10749–10753 列出的 14 个配置路径；`optimizer_activity_expected` = 学习类且非 eval。
  5. **读运行时计数器**（10769–10781）：`_pc_train_successes`、`_critic_train_successes`、`_global_state_observations`、`_temporal_apply_successes`、`_stale_neighbor_reads/history_hits`、`_timed_state_reads/hits/misses`、`_graph_state_builds/nodes_seen/edges_seen/overflow_nodes`，全部 `getattr(earth, ..., 0)`。
  6. **推导信息契约 `_effective_info`**（10783–10825）：train/evaluation/deployment 三相位初始各含 `local_observation/local_queue/neighbor_link_state`；非学习 pathing 清空 train；`slant_range` 时清空 evaluation/deployment 并根据图上的 `_slant_range_marker`/`_slant_range_runtime`（读自 `earth.graph.graph`，无图时用空 `nx.Graph()`，10793–10802）判定 `_slant_proven`，为真则补 `full_topology/global_link_slant_range`；state mode ∈ {c2..c7} 追加 `k_hop_queue_state`；按 stale/timed/temporal/pc/global-state 计数器追加对应标签；`oracle_global_dijkstra` 在 evaluation/deployment 追加 `full_topology/global_queue_state`；10825 去重排序。
  7. **收集 requested vs effective 原始事实**（10827–10884）：推理后端（`SIM_INFER_BACKEND` 默认 keras、`earth._infer_backends_effective`）、流量模式（`SIM_REQUESTED_TRAFFIC_MODE`、`earth.traffic_od_meta["mode"]`）、OD 矩阵哈希（`_array_sha256`，35）、突发/昼夜流量计数与配置哈希、GSL 切换计数（`earth._gsl_handover_*`）、链路中断统计（`earth._link_outage*`）；10880–10883 把 `mlab`+`mlab_hourly` 视为匹配别名。
  8. **mismatch 检测**（10885–11147，内部 `_mismatch(field, requested, effective, reason)` 追加 dict）：依次检查——
     - `SIM_RUN_ID` 缺失（10895–10896）；`_SIM_FAIL_CLOSED` 为假（10897–10898）；
     - 信息契约声明≠推导（10899–10900）；slant_range 运行未被证明（10901–10907）；
     - 执行语义声明≠推导（10908–10914）；流量模式不符（10915–10916）；OD 矩阵不可用（10917–10918）；流量配置哈希不符（10919–10925）；
     - trace 模式：receipt 无效或 trace_sha256 与 `SIM_EXPECTED_TRAFFIC_TRACE_SHA256` 不符（10926–10940）；
     - 突发流量：calls<1 / effect_calls<1 / 配置哈希不符 / 逐事件检查 resolved_src/dst_indices 非空、active_calls≥1、effect_calls≥1（10941–10976）；
     - 昼夜流量 calls/effect_calls（10977–10980）；GSL handover 模式不符、mbb 模式但切换数<1（10981–10994）；
     - 链路中断：请求了但未初始化 / 配置哈希不符 / evaluations<1（10995–11016）；
     - DQL 时 `routing_mode != SIM_ROUTING_MODE`（11017–11018）；DQL 时推理后端集合与请求不符或为空（11019–11023）；
     - non_learning 语义下出现训练活动/初始化了学习 agent/收到学习检查点（11024–11036），并把 `training_active/q_agent_initialized/checkpoint_requested` 并入 `_effective_execution_semantics`（11037–11042）；
     - path-credit 效果评估：`assess_path_credit_effect(...)`（11043–11051，来自 `runtime_effect_receipt.py`，27–32 import）结果并入 mismatches；
     - 集中式 critic：请求了（`_SIM_CRITIC_GLOBAL`）但 `q_global` 缺失 / 全局状态观测<1 / 训练成功<1（11053–11059）；
     - fast train：请求了（`_SIM_FAST_TRAIN`）但 fast 步数<1 或 eager 步数>0（11060–11067）；
     - temporal：`import temporal_encoder` 取 `last_train_loss()/mode()`（11069–11074），`assess_temporal_effect(...)`（11076–11083）并入 mismatches；请求 temporal 但 apply 成功数<1（11084–11085）；
     - stale/timed 邻居状态：请求了但 history_hits<1 / hits<1（11086–11097）；
     - 图观测（c4–c7）：graph_encoder 缺失或参数量非正 / state_builds<1 / overflow_nodes>0（11098–11119）；
     - RAAC（c6–c7）：encoder 非 reliability_aware / aoi_gate 与请求不符 / 满足采样条件但 `_raac_rel_samples`<1（11120–11147）。
  9. **组装 `_effective_receipt`**（11149–11310）：`requested` 段（pathing、routing_mode、执行语义、流量/突发/昼夜/handover/链路中断请求、信息契约、path_credit、critic、temporal、fast_train、推理后端、graph_observation 配置含 state_mode/vis_k/update_interval/layers/max_nodes/raac 门）；`effective` 段（pathing、routing_mode、执行语义、流量实测含 config 与矩阵哈希、trace receipt、突发/昼夜/handover/链路中断实测计数、信息契约、slant_range 审计、path_credit 评估结果、critic/temporal/stale/timed 实测、graph_observation 实测含 RAAC 门的 decisions/samples/reliability mean/min/max、execution 段含 fast/eager 步数、target 同步数、推理后端与回退记录）；`mismatches`；`research_eligible = bool(natural_end) and not _mismatches`（11309）。
  10. **顶层返回**（11312–11353）：natural_end/interrupted、run_attempt_id（`SIM_RUN_ATTEMPT_ID`）、config 标签与哈希（`SIM_CFG_PATH_TAG`/`SIM_CONFIG_CANONICAL_SHA256`）、`SIM_LAUNCH_NONCE`、`SIM_AUTHORIZATION_SHA256`、实验/运行/arm/角色/方法族/种子等请求标识（`SIM_EXPERIMENT_ID` 等 9 个 env）、scenario_identity 与其哈希、git commit/branch/dirty（env 优先，缺省用 `_git_value`）、state/graph 配置快照、模型与图编码器参数计数（`_count_params`）、`_effective_receipt`、`sim_env`（全部以 `SIM_`/`TF_`/`OMP_` 开头及 `MPLBACKEND` 的环境变量快照，11348–11352）。
- 输入/输出：入 Earth 对象、`natural_end` bool；出审计 dict（不抛异常路径之外的返回值；内部多处容错）。
- 依赖关系：调用 `_trace_traffic_receipt`(10833)、`_git_value`(11329–11334)、`_array_sha256`(10841–10842，定义于 35)、`assess_path_credit_effect`/`assess_temporal_effect`（外部 `CODE/runtime_effect_receipt.py`）、`temporal_encoder` 模块；读全局 `pathing`(226)、`SIM_ROUTING_MODE`(231)、`_SIM_*` 开关系列与 `nx`(8)。被 `save_on_interrupt`(11407，`natural_end=False`) 与 `RunSimulation`(12304，`natural_end=True`) 调用。测试佐证：`CODE/tests/test_runtime_effect_receipt.py` 第 55 行 `import SimulationRL as sim`，264/272/383/404/426/447/477/546 行共 8 处直接调用 `sim._run_audit_meta(earth, natural_end=True)["effective_receipt"]` 做断言（该测试文件用 stub 的 tensorflow/keras，见 20–53 行注释与代码）(FACT)。

#### `def save_on_interrupt(earth1, outputPath, GTnumber, reason)` — CODE/SimulationRL.py:11356
- 定位：CODE/SimulationRL.py:11356–11487
- 职责：训练被中断（KeyboardInterrupt/SIGTERM）时的「安全子集」保存：docstring 声明跳过可能在残缺数据上崩溃的绘图/分析，只写模型、指标 CSV、replay trace、replay buffer 和带恢复提示的 interrupt_meta.json（11357–11359）(FACT：docstring 声明；下列步骤为代码事实)。
- 关键状态/结构：内部 `_try(label, fn)`（11362–11366）捕获一切异常仅打印 `[interrupt-save] <label> failed: ...`，使各步互相隔离 (FACT)。
- 关键流程（编号与代码注释一致，FACT）：
  1. **模型权重**（11368–11377）：`pathing == 'Deep Q-Learning'` → `saveDeepNetworks(outputPath+'/NNs/', earth1)`；若 `earth1.DDQNA.pc_mixer` 存在则 `pc_mixer.save_weights(outputPath/NNs/pc_mixer_{GT}GTs.npz)`。`pathing == 'Q-Learning'` → `saveQTables`。
  2. **指标 CSV/图**（11379–11393）：仅 DQL：`earth1.rewards` 非空 → `save_plot_rewards`；`earth1.loss` 非空 → `save_losses`；取 epsilon（非 onlinePhase 用 `earth1.DDQNA.epsilon`，否则用 `earth1.LEO[0].sats[0].DDQNA.epsilon`）非空 → `save_epsilons`；`earth1.trains` 非空 → `save_training_counts`。
  3. **replay trace**（11395–11410）：`flush_replay_trace(earth1, outputPath, meta={schema_version:'1.2', seed:_SEED, interrupted:True, interrupt_reason/sim_time, pathing, gt_number, **_packet_count_meta(earth1), **_run_audit_meta(earth1, natural_end=False), SIM_RL_EVAL, sim_train_used})`（`flush_replay_trace` 定义于 1259，前序片段）。
  4. **经验回放**（11412–11415）：DQL 且非 onlinePhase 且 DDQNA 存在 → `save_replay_buffer(...)`。
  4b. **pc_replay**（11417–11423）：DQL 且非 onlinePhase 且 `earth1.pc_replay` 与 `DDQNA.pc_mixer` 均存在 → `_save_pc_replay` 到 `NNs/pc_replay_{GT}GTs.npz`。
  4c. **blocks.npy**（11425–11448）：`receivedDataBlocks` 为空则打印并跳过（返回 False）；否则逐块包 `BlocksForPickle`（定义于 1771）并用 `_atomic_save_npy`（定义于 58）存 `outputPath/Congestion_Test/blocks_{GT}.npy`（allow_pickle=True）。
  4c（注释编号重复，FACT）. **experiment_bundle**（11450–11458）：`blocks_saved` 且非 `SIM_FAST_ENV` 时 `from experiment_bundle import postprocess_run_dir; postprocess_run_dir(outputPath, pathing=pathing)`（`CODE/experiment_bundle.py` 已确认存在）。
  5. **interrupt_meta.json**（11460–11487）：写 `outputPath/run_trace/interrupt_meta.json`，含 reason、interrupt_sim_time、wall_time、gt_number、pathing、n_steps（`ddqna.step`）、n_trains、replay_buffer_size、`resume_hint`（SIM_NN_PATH/SIM_NN_TARGET/SIM_REPLAY_PATH/SIM_PC_MIXER_PATH/SIM_PC_REPLAY_PATH 五个指向本次输出的路径）。
- 输入/输出：入 Earth、输出目录、网关数、中断原因 str；出上述文件，无返回（调用方随后 `sys.exit(130)`，见 12287）。
- 依赖关系：调 `saveDeepNetworks/saveQTables/save_plot_rewards/save_losses/save_epsilons/save_training_counts/flush_replay_trace/_packet_count_meta/_run_audit_meta/save_replay_buffer/_save_pc_replay/_atomic_save_npy`；读全局 `pathing/onlinePhase/_SEED/SIM_FAST_ENV`。被 `RunSimulation`(12285) 在 `earth1.interrupted` 为真时调用 (FACT)。

### 绘图函数群

#### `def plotLatenciesBars(percentages, outputPath)` — CODE/SimulationRL.py:11495
- 定位：CODE/SimulationRL.py:11495–11522。职责：画百分比堆叠条形图——每个网关数场景一根柱，Propagation/Queue/Transmission time 三段堆叠（颜色 #b5ffb9/#f9bc86/#a3acff），存 `outputPath + 'Percentages_{len(GTnumber)+1}_Gateways.png'`（11520，注意文件名取 GT 数 +1）(FACT)。输入：含 4 个键的 dict；输出：png 文件。**调用方未确认——唯一调用点 12511 行处于注释状态（`# plotLatenciesBars(percentages, outputPath)`），`RunSimulation` 12022–12027 与 12459–12477 中构造 percentages 的代码也整体注释** (FACT)。

#### `def plotQueues(queues, outputPath, GTnumber)` — CODE/SimulationRL.py:11525
- 定位：CODE/SimulationRL.py:11525–11536。职责：画队列长度累计直方图（`bins=max(queues)`, cumulative, density, step 型），存 `pngQueues/Queues_{N}_Gateways.png`，并把原始 queues 存 `csv/Queues_{N}_Gateways.csv` (FACT)。docstring 提到 CDF 与 PDF，但代码只画一幅 cumulative 直方图 (FACT)。输入：队列长度列表、输出目录、网关数；输出：png+csv。被 `RunSimulation`(12441，非 onlinePhase 时) 调用 (FACT)。

#### `def extract_block_index(block_id)` — CODE/SimulationRL.py:11539
- 定位：CODE/SimulationRL.py:11539–11540。职责：`int(block_id.split('_')[-1])`，取块 ID 最后一个下划线段的整数 (FACT)。输入：块 ID 字符串；输出：int。被 `plotSaveAllLatencies`(11853，`df['Block ID'].apply(...)`) 调用 (FACT)。

#### `def save_plot_rewards(outputPath, reward, GTnumber, window_size=200)` — CODE/SimulationRL.py:11543
- 定位：CODE/SimulationRL.py:11543–11581。职责：把 `[reward, time]` 对列表转成 DataFrame，计算滚动均值（window=200）与滚动 Top10%/Bottom10% 均值（`np.partition` 实现，11552–11553），画三条曲线存 `Rewards/rewards_{N}_gateways.png`，DataFrame 存 `csv/rewards_{N}_gateways.csv`，返回 DataFrame (FACT)。x 轴标签 "Time [ms]"（11564）但输入时间未做单位换算 (FACT)。被 `save_on_interrupt`(11382) 与 `RunSimulation`(12409) 调用 (FACT)。

#### `def save_epsilons(outputPath, eps, GTnumber)` — CODE/SimulationRL.py:11584
- 定位：CODE/SimulationRL.py:11584–11600。职责：画 epsilon-时间折线存 `epsilons/epsilon_{N}_gateways.png`，同数据存 `csv/epsilons_{N}_gateways.csv`，返回 DataFrame (FACT)。被 `save_on_interrupt`(11390) 与 `RunSimulation`(12416，仅 `Train` 为真时) 调用 (FACT)。

#### `def save_training_counts(outputPath, train_times, GTnumber)` — CODE/SimulationRL.py:11603
- 定位：CODE/SimulationRL.py:11603–11629。职责：把时间列表 ×1000 转 ms（11605），画累计训练次数折线存 `trainings/trainings_{N}_gateways.png`，存 `csv/trainings_{N}_gateways.csv`；末尾有注释掉的 `# return df`（11629），函数实际无返回 (FACT)。被 `save_on_interrupt`(11392) 与 `RunSimulation`(12417) 调用 (FACT)。

#### `def save_losses(outputPath, earth1, GTnumber)` — CODE/SimulationRL.py:11632
- 定位：CODE/SimulationRL.py:11632–11663。职责：从 `earth1.loss`（[loss,time] 对）画两张图——按时间（`loss_{N}_gatewaysTime.png`）与按步数（`loss_{N}_gatewaysSteps.png`），再从 `earth1.lossAv` 画平均 loss 图（`loss_{N}_gatewaysAverage.png`），均存 `loss/` 目录；loss 数据存 `csv/loss_{N}_gateways.csv` (FACT)。被 `save_on_interrupt`(11385) 与 `RunSimulation`(12427，仅 DQL) 调用 (FACT)。

#### `def plotSavePathLatencies(outputPath, GTnumber, pathBlocks)` — CODE/SimulationRL.py:11666
- 定位：CODE/SimulationRL.py:11666–11694。职责：取 `pathBlocks[0]` 的 (latency, arrival) 对，画两张红色散点图——x 轴分别为到达时刻（`pngLatencies/{N}_gatewaysTime.png`）与到达序号（`pngLatencies/{N}_gateways.png`），数据存 `csv/pathLatencies_{N}_gateways.csv` (FACT)。注释称「figure of latencies between two first gateways」（11667）(FACT：注释原文)。被 `RunSimulation`(12399) 调用 (FACT)。

#### `def plot_packet_latencies_and_uplink_downlink_throughput(data, outputPath, bins_num=30, save=False, plot_separately=True)` — CODE/SimulationRL.py:11697
- 定位：CODE/SimulationRL.py:11697–11774。职责：按 `(block.path[0][0], block.path[-1][0])` 把数据块按源-目的路径分组（11708–11712）；内部 `plot_path_data(blocks, src, dst)`（11715–11766）对每个分组：按 creationTime 排序，画到达时刻(ms) vs 端到端时延(ms) 散点（主轴），副轴用 `np.histogram` 在时间 bin 上统计创建/到达计数，乘 `BLOCK_SIZE`(318) 除以 bin 宽得上/下行吞吐折线——换算因子为 `/1e3` 且注释标注 Mbps（11739–11741）(FACT：代码与注释如此；同文件 `plot_throughput_cdf` 用 `/1e6`，11806–11808)。`save=True` 存 `Throughput/{src}_{dst}_path_latency_throughput.png`（或 combined），否则 `plt.show()`（11761–11765）。`plot_separately=True` 逐路径出图，False 合并一张 (FACT)。输入：数据块列表；输出：png 或屏幕显示。被 `RunSimulation`(12403，`save=True, plot_separately=plotAllThro`) 调用 (FACT)。

#### `def plot_throughput_cdf(data, outputPath, bins_num=100, save=False, plot_separately=True)` — CODE/SimulationRL.py:11777
- 定位：CODE/SimulationRL.py:11777–11842。职责：与上函数相同的分组与吞吐计算（但换算因子 `/1e6`，11806–11808），对上/下行吞吐序列排序后画经验 CDF（`np.arange(1,n+1)/n`），存 `Throughput/Throughput_CDF_{src}_to_{dst}.png` 或 `Throughput_CDF_All_Paths.png` (FACT)。被 `RunSimulation`(12406) 调用 (FACT)。

#### `def plotSaveAllLatencies(outputPath, GTnumber, allLatencies, epsDF=None, annotate_min_latency=True)` — CODE/SimulationRL.py:11845
- 定位：CODE/SimulationRL.py:11845–11937。职责 (FACT)：
  - 预处理：allLatencies → 9 列 DataFrame（Creation Time/Latency/Arrival Time/Source/Destination/Block ID/QueueTime/TxTime/PropTime），用 `extract_block_index` 加 Block Index 列并按 (Source,Destination,Block Index) 排序，存 `csv/allLatencies_{N}_gateways.csv`（11851–11855）；时间列 ×1000 转 ms（11858–11862）。
  - 按 `Path`（"src -> dst"）分组算滚动均值，窗口用全局 `winSize`(567)（11865–11866）。
  - 画 2×2 子图（figsize 18×18）：左列为 Arrival Time / Creation Time 的滚动均值折线（sns.lineplot），右列为原始时延散点（marker 大小用全局 `markerSize`(568)）（11872–11905）。
  - `annotate_min_latency` 且 x 为 Creation Time 时，对每条路径在滚动均值最小点加箭头注释（`math.isfinite` 守卫，异常打印错误继续，11882–11898）。
  - `epsDF` 非 None 时在左列加副轴画 epsilon 紫线并合并图例（11908–11918）。
  - `GTnumber > 4` 时隐藏所有图例（11924–11929，阈值 `GTnumber_Max = 4` 定义于 11847）。
  - 存 `pngAllLatencies/{N}_gateways_All_Latencies_subplots.png`（dpi=300），结尾 `sns.set()` 复原 seaborn 设置（11933–11937）。
- 输入/输出：入输出目录、网关数、时延记录列表、可选 epsilon DataFrame；出 png+csv。
- 依赖关系：调 `extract_block_index`；读全局 `winSize/markerSize`。被 `RunSimulation`(12423 带 epsDF、12434 不带) 调用 (FACT)。

#### `def plotRatesFigures()` — CODE/SimulationRL.py:11940
- 定位：CODE/SimulationRL.py:11940–11965。职责：对全局列表 `interRates`、`upGSLRates`、`downGSLRates`（688–690）各画一幅累计直方图（/1e9 转 Gbps，density），标题分别为 Inter plane ISL/Uplink/Downlink data rates，用 `plt.show()` 显示而非存盘 (FACT)。`intraRate`(691) 被放进 `values` 列表（11941）但没有任何绘图语句使用 `values` 或 `intraRate` (FACT)。被 `RunSimulation`(12290，`testType == "Rates"` 时) 调用 (FACT)。

#### `def plotCongestionMap(self, paths, outPath, GTnumber, plot_separately=True)` — CODE/SimulationRL.py:11968
- 定位：CODE/SimulationRL.py:11968–12015。职责：模块级函数但首参数命名为 `self`，期望传入 Earth 实例（FACT：11997/12011 行调用 `self.plotMap(...)`，即 `Earth.plotMap`(5343)；12445 行实际调用传 `earth1`）。流程 (FACT)：内部 `extract_gateways(path)`（11969–11974）按全局 `pathing` 取块的首末节点——Q-Learning/Deep Q-Learning 用 `path.QPath[0][0]/QPath[-1][0]`，否则用 `path.path[...]`；统计每条 (源,目的) 网关对的块数，过滤出计数 >100 的路由（11989，行内注释 `# REVIEW Packet threshold for path visualization 500`）；先画全部过滤后路由的合图 `all_routes_CongestionMap_{N}GTs.png`，`plotMap` 返回 -1 时打印不可用；`plot_separately=True` 再逐路由画 `CongestionMap_{src}_to_{dst}_{N}GTs.png`。输入：Earth 实例、块数组、输出目录、网关数；输出：png 文件。被 `RunSimulation`(12444–12446) 调用 (FACT)。

### 主入口

#### `def RunSimulation(GTs, inputPath, outputPath, populationData, radioKM)` — CODE/SimulationRL.py:12019
- 定位：CODE/SimulationRL.py:12019–12521（503 行）
- 职责：整个仿真的主驱动：读输入参数，对 `GTs` 列表里每个网关数各建一次 simpy 环境跑仿真，负责热启动恢复、中断保护、运行后统计/绘图/回执落盘与多场景间状态清理 (FACT)。
- 关键状态/结构：声明并改写的全局变量：`CurrentGTnumber/Train/TrainThis/explore/importQVals/nnpath`（12053–12058）、`nnpathTarget`（ddqn 时，12061–12062）、`diff_lastHop`(12063)、`CKA_Values`（FL_Test 时，12059–12060）。
- 关键流程（按行号分阶段，均 FACT）：
  1. **参数读取**（12020–12049）：`pd.read_csv(_resolve_input_rl_path(default=inputPath+"inputRL.csv"))`；取 `Test type`、`Test length`；env `SIM_TIME_LIMIT` 可覆盖 testLength（非法值打印并回退 CSV 值）；`simulationTimelimit = testLength`（testType ≠ "Rates"）或 `movementTime*testLength + 10`（Rates）。
  2. **GT 循环开头与 eval 模式**（12051–12074）：对 `GTnumber in GTs`；先存 `_saved_train_flags = (Train, explore, importQVals, diff_lastHop)`；若 env `SIM_RL_EVAL` ∈ {1,true,yes} 且 DQL：强制 `Train=False, explore=False, importQVals=True`，`diff_lastHop` 由 env `SIM_DIFF_LAST_HOP` 决定（默认 False，注释说明与预训练 3GT 模型 28 维输入兼容）；`TrainThis = Train`。
  3. **跨场景权重接力**（12076–12082）：首个 GT 用文件头 `nnpath`(625)；后续 GT 改指 `outputPath/NNs/qNetwork_{GTnumber-1}GTs.h5`（及 ddqn 时 qTarget）。
  4. **建环境**（12087–12111）：`simpy.Environment()`；`mixLocs` 为真时对前 `max(GTs)` 个网关位置洗牌；`inputParams['Locations']` 截断到 GTnumber；打印一批全局配置；`earth1, _, _, _ = initialize(env, populationData, inputPath+'Gateways.csv', radioKM, inputParams, movementTime, locations, outputPath, matching=matching)`（`initialize` 定义于 7885）；在 earth1 上记录 `outputPath/sim_train_used/sim_explore_used/sim_import_used/sim_rl_eval_env`。
  5. **热启动恢复**（12113–12163）：env `SIM_REPLAY_PATH` 且 DQL 且非 onlinePhase → `load_replay_buffer_into`；`earth1._pc_checkpoint_loads = {"mixer": new_checkpoint_receipt(SIM_PC_MIXER_PATH), "replay": new_checkpoint_receipt(SIM_PC_REPLAY_PATH)}`；两路径非空时分别经 `attempt_checkpoint_load(..., label=..., fail_closed=_SIM_FAIL_CLOSED)` 加载 pc_mixer 权重/`_load_pc_replay_into`，组件缺失时走 `_missing_pc_component` 抛 RuntimeError（12131–12132），加载结果打印。
  6. **初始 ISL 地图**（12165–12175）：`saveISLs` 为真时 `earth1.plotMap(...)` 存 `outputPath/ISL_maps/`；否则打印跳过（注释说明 `SIM_FAST=1` 会置 saveISLs=False）。
  7. **注册仿真进程**（12177–12196）：`env.process(simProgress(...))`；`REPLAY_TRACE` 为真时注册 `_queue_snapshot_proc`：每 0.02 s 仿真时间对全部卫星记录 `(t, sat.ID, qU, qD, qR, qL, gsl_q)` 到 `earth1.queue_snapshots`（单卫星异常静默吞掉，12193–12194）。
  8. **中断保护**（12198–12210）：安装 SIGTERM 处理器 `_handle_sigterm`，把 SIGTERM 转成 `KeyboardInterrupt`；在 earth1 上置 `interrupted/interrupt_sim_time/interrupt_reason`。
  9. **分数检查点**（12212–12230）：`_SIM_CHECKPOINT_FRACTIONS` 非空且 TrainThis 且 DDQNA 存在时，对每个分数 `_f` 注册 `_ckpt_proc`，在 `simulationTimelimit*_f` 时刻存 `NNs/qNetwork_{N}GTs_frac{NNN}.h5`（及 ddqn 时 qTarget），异常仅打印。
  10. **跑仿真**（12232–12245）：`env.run(simulationTimelimit)`；捕获 KeyboardInterrupt → 标记 earth1.interrupted、记录 sim_time 与原因；finally 恢复原 SIGTERM 处理器。
  11. **收敛摘要打印**（12247–12278）：若 `earth1.loss` 非空：打印总步数、train 调用数、按公式 `minEps + (maxEps-minEps)*exp(-LAMBDA*step/(decayRate*GT²))` 估算的最终 ε、loss 首 20/末 20 均值与趋势（↓/↑/→），并估算 ε<0.5 所需步数与仿真秒数（12268–12277）。
  12. **中断分支**（12280–12287）：`earth1.interrupted` 为真 → `save_on_interrupt(...)` 后 `sys.exit(130)`（注释说明 130 是 SIGINT 的 shell 约定）。
  13. **正常结束统计与回执**（12289–12338）：testType == "Rates" → `plotRatesFigures()`；否则 `results, allLatencies, pathBlocks, blocks = getBlockTransmissionStats(timeToSim, locations, constellation, earth1)`（1324），打印 `earth1.lostBlocks`，然后 `flush_replay_trace(earth1, outputPath, meta={...})`——meta 含 schema 1.2、seed、pathing、gt_number、`_packet_count_meta`、`_run_audit_meta(natural_end=True)`、仿真时长、流量模式/配置/OD 矩阵（`.tolist()`）、trace 回执、`SIM_RL_EVAL`、训练/探索/导入标志、`SIM_ROUTING_MODE`、quantile 尾部分支信息（routing_mode == "ddqn_cvar" 时 `__import__("legacy.routing_tailguard", ...)` 取 `tailguard_fallback_note`，12321–12328；注意 `legacy` 包在当前工作区不存在，见 saveDeepNetworks 条目）、`ddqn_mcp_hash` 时的 4 个 MCP env 快照（12329–12336）。
  14. **trace 数组落盘**（12339–12388）：`REPLAY_TRACE` 时把 `earth1.decision_trace`（12 列，列名 json 同步写出）与 `earth1.queue_snapshots`（7 列）各存 .npy + columns.json 到 `outputPath/run_trace/`。
  15. **绘图与 bundle**（12390–12457，仅非 `SIM_FAST_ENV`）：`experiment_bundle.postprocess_run_dir(outputPath, pathing=pathing)`（异常打印跳过）；`plotSavePathLatencies`；两个吞吐图（`plot_separately=plotAllThro`）；DQL/QL 时 `save_plot_rewards`、取 epsilon（onlinePhase 取首卫星）、`Train` 时 `save_epsilons`+`save_training_counts` 得 epsDF、`plotSaveAllLatencies(..., epsDF)`；DQL 专属 `save_losses`，`FL_Test and const_moved` 时 `plot_cka_over_time`（1679）；非 DQL 时 `plotSaveAllLatencies`（无 epsDF）；`pathBlocks[1]` 非空时 `plotShortestPath`（8968）否则打印跳过；非 onlinePhase 时 `plotQueues`；`plotCongestionMap(earth1, np.asarray(blocks), outputPath+'/Congestion_Test/', GTnumber, plot_separately=plotAllCon)`；`pathBlocks[1]` 非空时打印 Path 与 `findBottleneck`（8087）结果。`SIM_FAST` 分支只打印网关数（12456–12457）。
  16. **学习成果保存**（12479–12483）：QL → `saveQTables`；DQL → `saveDeepNetworks(outputPath+'/NNs/', earth1)`。
  17. **清理**（12485–12499）：清空全局列表 `receivedDataBlocks/createdBlocks/pathBlocks/allLatencies/upGSLRates/downGSLRates/interRates/intraRate`；`del results/earth1/env/_`；恢复 `_saved_train_flags`；`gc.collect()`。控制流事实链 (FACT)：①`results/allLatencies/pathBlocks` 三个名字仅在 12292 行由 `getBlockTransmissionStats(...)` 的解包绑定（模块级无定义，全文件 grep `^(pathBlocks|allLatencies|results)\s*=` 无匹配；`allLatencies`/`pathBlocks` 仅在 `getBlockTransmissionStats` 内部 1336–1337 作为局部变量创建）；②testType=="Rates" 分支（12289–12290）跳过该绑定；③12488–12494 的 `pathBlocks.clear()`/`allLatencies.clear()`/`del results` 无条件执行且外层无 try 包裹。由 Python 局部变量语义，Rates 路径执行到 12488 时会抛 `UnboundLocalError`（由 ①②③ 直接推出，FACT）。
  18. **计时打印**（12501–12520）：多 GT 时打印每档耗时；循环结束后打印总耗时。
- 输入/输出：入网关数列表、输入目录、输出目录、人口数据路径、网关覆盖半径；出全部结果文件（无返回）。
- 依赖关系：调用 `_resolve_input_rl_path`(634)、`initialize`(7885)、`simProgress`(1416)、`load_replay_buffer_into`/`_load_pc_replay_into`/`new_checkpoint_receipt`/`attempt_checkpoint_load`（外部 runtime_effect_receipt）、`getQueues`(9050)、`save_on_interrupt`、`getBlockTransmissionStats`(1324)、`flush_replay_trace`(1259)、`_packet_count_meta`、`_run_audit_meta`、`_trace_traffic_receipt`、`plotRatesFigures`、`plotSavePathLatencies`、`plot_packet_latencies_and_uplink_downlink_throughput`、`plot_throughput_cdf`、`save_plot_rewards`、`save_epsilons`、`save_training_counts`、`save_losses`、`plotSaveAllLatencies`、`plot_cka_over_time`(1679)、`plotShortestPath`(8968)、`plotQueues`、`plotCongestionMap`、`findBottleneck`(8087)、`saveQTables`、`saveDeepNetworks`；读写全局 `pathing/onlinePhase/ddqn/Train/explore/importQVals/diff_lastHop/nnpath/nnpathTarget/movementTime/ndeltas/MIN_EPSILON/ArriveReward/stopLoss/nLosses/lThreshold/matching/mixLocs/FL_Test/const_moved/REPLAY_TRACE/SIM_FAST_ENV/saveISLs/plotAllThro/plotAllCon/LAMBDA/decayRate/SIM_ROUTING_MODE/_SIM_FAIL_CLOSED/_SIM_CHECKPOINT_FRACTIONS` 与全局块列表。被调方：仅 `if __name__ == '__main__':` 块（12549）；CODE/ 下无其他文件调用 `RunSimulation`（跨文件 `import SimulationRL` 仅 5 处：tests/test_runtime_effect_receipt.py:55、tests/test_state_vis_k.py:21、tests/test_raac_aoi_gate.py:49、tests/test_raac_tensorflow_contract.py:34、tools/benchmark_graph_execution.py:33，均不调用 RunSimulation）(FACT)。
