# 旧平台路由/学习算法扩展模块组说明书片段

范围：`CODE/routing_hooks.py`、`CODE/routing_mappo.py`、`CODE/routing_multistep.py`、`CODE/routing_path_credit.py`。所有行号均为实测（`wc -l` + 全文通读）。标注约定：(FACT) = 代码中可直接确认；(INFERENCE) = 从命名/注释/上下文推测。

---

## 文件 `CODE/routing_hooks.py`（实测 133 行）

模块级说明：
- 模块 docstring（行 1–4）：声明本模块是「DDQNAgent 的最小路由 hook」，未设 `SIM_ROUTING_MODE` 或设为 `ddqn` 时走 identity 打分 + 传统 argmax 掩码路径。
- imports（行 5–10）：`__future__.annotations`、`os`、`typing.Any/Dict/Tuple`、`numpy`。
- 全局常量 `SUPPORTED_ROUTING_MODES = ("ddqn",)`（行 13）：保留 CODE 中唯一受支持的路由模式白名单。
- 被 `CODE/SimulationRL.py:229` 在模块顶层 import（`parse_routing_mode` 别名 `_parse_sim_routing_mode`、`validate_routing_mode` 别名 `_validate_routing_mode`），并在 `CODE/SimulationRL.py:231–232` 模块加载时立即执行解析与校验——即非法 `SIM_ROUTING_MODE` 会在 import 阶段 fail loud。(FACT)
- `CODE/run.py:743–753` 在配置转 env 阶段用自带白名单 `{"ddqn"}` 做另一层校验（不 import 本模块）。(FACT)
- 行为佐证：`CODE/tests/test_routing_mode_contract.py:41–52` 对 `parse_routing_mode`/`validate_routing_mode` 拒绝 legacy 模式与拼写错误做了契约测试。

#### `def parse_routing_mode() -> str` — CODE/routing_hooks.py:16
- 定位：CODE/routing_hooks.py:16
- 职责：读取 env `SIM_ROUTING_MODE`，空串或 `"ddqn"` 返回 `"ddqn"`，其余值抛 `ValueError`（错误信息点名 legacy 模式 `ddqn_cvar/cvar/tailguard`、`ddqn_mcp_hash/mcp/mcp_hash` 未迁移进保留 CODE）。(FACT)
- 输入/输出：无参；返回 `str` 或抛异常。
- 依赖关系：被 `CODE/SimulationRL.py:231` 在模块加载时调用；被 `CODE/tests/test_routing_mode_contract.py:46` 测试。

#### `def validate_routing_mode(mode: str) -> None` — CODE/routing_hooks.py:27
- 定位：CODE/routing_hooks.py:27
- 职责：`mode` 不在 `SUPPORTED_ROUTING_MODES` 中时抛 `ValueError`，否则无操作。(FACT)
- 输入/输出：入 `mode: str`；无返回。
- 依赖关系：被 `CODE/SimulationRL.py:232`、本文件 `build_default_hooks`（行 132）、`CODE/tests/test_routing_mode_contract.py:52` 调用。

#### `class LocalStatsHook` — CODE/routing_hooks.py:34
- 定位：CODE/routing_hooks.py:34
- 职责：决策前本地统计 hook 的默认 no-op 实现（docstring 行 35：「Inference-only local statistics; default is no-op」）。(FACT)
- 关键状态/结构：无任何实例状态（无 `__init__`）。
- 关键流程/方法：`on_pre_decision(self, agent, sat, block, linked_sats)`（行 37）函数体为 `pass`（行 44），什么都不做。
- 输入/输出：入 agent/卫星/数据包/邻居表；无返回。
- 依赖关系：被 `build_default_hooks`（行 133）实例化；被 `CODE/SimulationRL.py:6414` import、行 6425 直接实例化（`ddqn_cvar` 分支）；其方法在 `CODE/SimulationRL.py:6856`（`DDQNAgent.getNextHop` 内）被调用。

#### `class ActionScoringHook` — CODE/routing_hooks.py:47
- 定位：CODE/routing_hooks.py:47
- 职责：抽象基类——把网络原始输出映射成 `(1, n_actions)` 的利用（exploitation）打分（docstring 行 48）。(FACT)
- 关键状态/结构：无实例状态。
- 关键流程/方法：`score(self, agent, q_raw, *, new_state, linked_sats, sat, block)`（行 50）只 `raise NotImplementedError`（行 60）。
- 输入/输出：入原始 Q 输出 `q_raw` 等；契约上返回 `np.ndarray`。
- 依赖关系：被 `IdentityScoringHook`（行 63）继承；自身不直接被调用。

#### `class IdentityScoringHook(ActionScoringHook)` — CODE/routing_hooks.py:63
- 定位：CODE/routing_hooks.py:63
- 职责：标量 Q 的恒等打分——docstring（行 64）注明 `q_raw` 形状为 `(1, 4)`。(FACT)
- 关键状态/结构：无实例状态。
- 关键流程/方法：`score(...)`（行 66）把 `q_raw` 转 `float64`，一维时 reshape 成 `(1, -1)`，返回前 `agent.actionSize` 列（行 76–79），不做任何变换。
- 输入/输出：入 `q_raw`（网络输出）；返回 `(1, actionSize)` 的 `float64` 数组。
- 依赖关系：由 `build_default_hooks`（行 133）实例化；其 `score` 在 `CODE/SimulationRL.py:6941–6943`（`DDQNAgent.getNextHop` 内）被调用。

#### `class ActionSelectorHook` — CODE/routing_hooks.py:82
- 定位：CODE/routing_hooks.py:82
- 职责：抽象基类——从打分中选出一个可行动作（ exploitation 选择）。(FACT)
- 关键状态/结构：无实例状态。
- 关键流程/方法：`select_exploitation(self, agent, scores, q_for_mask, linked_sats, new_state, sat, block)`（行 83）只 `raise NotImplementedError`（行 93）；契约返回 `Tuple[int, str]`（动作索引 + 动作键）。
- 输入/输出：入打分数组与邻居表；契约返回 `(int, str)`。
- 依赖关系：被 `BaselineSelectorHook`（行 96）继承；自身不直接被调用。

#### `class BaselineSelectorHook(ActionSelectorHook)` — CODE/routing_hooks.py:96
- 定位：CODE/routing_hooks.py:96
- 职责：基线选择器——docstring（行 97–99）描述为「Legacy：在 `q_for_mask` 上 argmax，对不可行方向置 `-inf` 直到选中可行方向」。(FACT)
- 关键状态/结构：`self._unav`（行 102）——不可用方向惩罚值（float）。
- 关键流程/方法：
  - `__init__(self, unav_penalty)`（行 101）：存惩罚值到 `self._unav`。
  - `select_exploitation(...)`（行 104）：复制 `q_for_mask` 为 `float64` 并截到 `actionSize` 列（行 114–115）；argmax 取动作（行 117–118）；若该方向 `linked_sats[action] is None`，则循环执行三个副作用——向 `agent.experienceReplay` 存入 `(new_state, act_index, self._unav, new_state, False)` 惩罚经验（行 120）、向 `agent.earth.rewards` 追加 `[self._unav, sat.env.now]`（行 121）、把该方向打分置 `-inf` 后重新 argmax（行 122–124），直到选中可行方向；返回 `(act_index, action)`（行 126）。
- 输入/输出：入打分与 `q_for_mask`；返回 `(动作索引 int, 动作键 str)`；副作用是惩罚经验直接写入 agent 的经验回放与 earth 奖励日志。
- 依赖关系：由 `build_default_hooks`（行 133）实例化；`select_exploitation` 在 `CODE/SimulationRL.py:6946–6948`（`DDQNAgent.getNextHop` 内）被调用；读取 `agent.actions`、`agent.actionSize`、`agent.experienceReplay`、`agent.earth.rewards`。

#### `def build_default_hooks(mode, *, unav_penalty)` — CODE/routing_hooks.py:129
- 定位：CODE/routing_hooks.py:129
- 职责：工厂函数——先 `validate_routing_mode(mode)`（行 132），再返回三元组 `(LocalStatsHook(), IdentityScoringHook(), BaselineSelectorHook(unav_penalty))`（行 133）。(FACT)
- 输入/输出：入路由模式字符串与不可用惩罚值；返回 `(LocalStatsHook, ActionScoringHook, ActionSelectorHook)` 三元组。
- 依赖关系：被 `CODE/SimulationRL.py:6432–6434`（`DDQNAgent.__init__` 的 `else` 分支）调用。注意 `CODE/SimulationRL.py:6416–6430` 的 `ddqn_mcp_hash`/`ddqn_cvar` 分支会 import `legacy.routing_mcp_hash`/`legacy.routing_tailguard`，但 `parse_routing_mode` 在模块加载时（SimulationRL.py:231）已拒绝这两种模式，故该两分支在保留 CODE 中不可达 (FACT——由行 20–24 的抛错逻辑与行 231 的调用顺序决定)。

---

## 文件 `CODE/routing_mappo.py`（实测 631 行）

模块级说明：
- 模块 docstring（行 1–44）：自述为「Recurrent MAPPO + Centralized Critic + Backpressure Prior 完整版 framework 实现」，列出 5 个 gap-decomposition 基线（B0–B4）与实施现状标记（✅/🟡）。docstring 中「今晚跑」「明天 debug」等表述是开发当时的状态记录。(FACT：docstring 存在；其陈述的完成度属作者自述)
- imports（行 45–52）：`os`、`collections`、`numpy`、`typing`、`tensorflow`/`keras`/`layers`。注意本模块在 import 时即需要 TensorFlow（与 routing_path_credit.py 的 lazy-import 不同）。(FACT)
- 全局常量 `GLOBAL_STATE_DIM = 44`（行 337）；`CODE/SimulationRL.py:546–547` 重复定义同名常量并注释「must match routing_mappo.GLOBAL_STATE_DIM」。(FACT)
- SimulationRL.py 侧的配套 env 解析在 `CODE/SimulationRL.py:495–516`（`SIM_FRAME_STACK_K`、`SIM_BP_BETA`、`SIM_BP_K_PROGRESS`、`SIM_BP_K_LOOP`、`SIM_CRITIC_GLOBAL`、`SIM_BP_ONLY`、`SIM_MAPPO_MODE` 等），而非经本模块的 `parse_env_config`。(FACT)

#### `class BackpressurePrior` — CODE/routing_mappo.py:59
- 定位：CODE/routing_mappo.py:59
- 职责：Backpressure 风格动作先验：按 docstring 公式（行 61–74）`BP(a) = (own_q[a] − nbr_q[a]) + k_progress·progress(a) − k_loop·loop(a)` 计算每方向分数，并与 DQN 的 Q 值做 z-归一化加权融合。(FACT)
- 关键状态/结构：四个超参数属性 `beta`、`k_progress`、`k_loop`、`invalid_score`（行 81–84）。
- 关键流程/方法：
  - `__init__(beta=0.3, k_progress=0.3, k_loop=1.0, invalid_score=-1e9)`（行 76）：存四个 float 超参数。
  - `compute_bp(own_queues, neighbor_queues, progress, is_loop, valid_mask)`（行 86）：对 4 个方向（U/D/R/L）按上述公式算 BP 分数，`valid_mask` 为假的方向覆写为 `invalid_score`（行 94–99）；返回 shape `[4]` 数组。
  - `score_actions(q_values, bp_values)`（行 101）：以 `bp_values > invalid_score/2` 判定有效方向（行 109）；全无效时原样返回 `q_values`（行 111–113）；否则在有效子集上分别对 Q 与 BP 做 z-归一化（均值/标准差取自有效子集，行 116–119），算 `score = q_norm + beta·b_norm`，无效方向置 `-1e9`（行 120–123）。
- 输入/输出：吃 4 维队列/进度/回环/掩码数组与 Q 值数组；吐 4 维 BP 分数或融合分数。
- 依赖关系：在 `CODE/SimulationRL.py:6268–6273`（`DDQNAgent.__init__`，条件 `_SIM_BP_BETA > 0.0`）实例化为 `self._mappo_bp`；`compute_bp` 在 `CODE/SimulationRL.py:6924–6930` 被调用，`score_actions` 在行 6935 被调用（均在 `DDQNAgent.getNextHop` 的 BP 融合段内）；`invalid_score`、`k_loop` 属性在行 6914、6922 被 `SIM_BP_CORRECT` 分支直接读取。同文件内还被 `RecurrentMAPPOAgent.__init__`（行 486–488）与 `FrameStackBPAgent.__init__`（行 597–599）实例化。SimulationRL.py:502–507 的注释称该 aggregate 版 BP「is broken」并提供 `SIM_BP_CORRECT` 修正路径——这是代码内注释的陈述，非本说明书的评价。

#### `class FrameStackHelper` — CODE/routing_mappo.py:130
- 定位：CODE/routing_mappo.py:130
- 职责：把最近 K 帧观测拼成单个 stacked 观测（docstring 行 131–141，示例用法是挂在 Satellite 实例上）。(FACT)
- 关键状态/结构：`self.K`、`self.obs_dim`、`self._buffer`（`collections.deque(maxlen=K)`，行 143–145）。
- 关键流程/方法：
  - `__init__(K=4, obs_dim=33)`（行 142）：初始化 deque。
  - `reset()`（行 147）：清空 deque。
  - `push_and_get(current_obs)`（行 150）：把输入 flatten 成 `float32`，维度不等于 `obs_dim` 时截断或零填充（行 153–158），append 进 deque；不足 K 帧时在左侧重复填充当前帧（行 161–162）；返回拼接后的 `(K*obs_dim,)` `float32` 数组（行 163–164）。
- 输入/输出：吃单帧观测；吐 `(K*obs_dim,)` 拼接向量。
- 依赖关系：调用方未确认——grep 全 CODE 无 import/实例化点。`CODE/SimulationRL.py:9499–9528` 的 `_apply_frame_stack` 用 `sat._mappo_frame_buf`（deque）在行内重新实现了同样的 K 帧拼接逻辑，并未使用本类。(FACT)

#### `def build_recurrent_actor(obs_dim, action_size, hidden_units=64, gru_units=64)` — CODE/routing_mappo.py:171
- 定位：CODE/routing_mappo.py:171
- 职责：工厂函数——构建 GRU 循环 actor 的 Keras 模型：两层 Dense(relu) 编码器（行 190–191）→ `GRUCell` 单步（行 194–195）→ 线性 action logits 头（行 198）；模型输入 `[obs, h_prev]`、输出 `[logits, h_new]`（行 200–201）。(FACT)
- 输入/输出：入维度参数；返回未编译的 `keras.Model`（name=`recurrent_actor`）。
- 依赖关系：唯一调用方是本文件 `RecurrentMAPPOAgent.__init__`（行 472–474）。

#### `def build_centralized_critic(global_state_dim, hidden_units=128)` — CODE/routing_mappo.py:209
- 定位：CODE/routing_mappo.py:209
- 职责：工厂函数——构建集中式 critic（V 值版）：输入 global state，两层 Dense(relu)，标量线性输出 `V(s_global)`（行 226–230）。(FACT)
- 输入/输出：入维度参数；返回 `keras.Model`（name=`centralized_critic`）。
- 依赖关系：唯一调用方是本文件 `RecurrentMAPPOAgent.__init__`（行 475）。

#### `def build_centralized_critic_per_action(global_state_dim, action_size, hidden_units=128)` — CODE/routing_mappo.py:233
- 定位：CODE/routing_mappo.py:233
- 职责：工厂函数——构建 Q 版集中式 critic：输入 global state，两层 Dense(relu)，输出 `action_size` 维 `Q_global`（行 244–248）。(FACT)
- 输入/输出：入维度参数；返回 `keras.Model`（name=`centralized_critic_q`）。
- 依赖关系：被 `CODE/SimulationRL.py:6506–6518`（`DDQNAgent.__init__`，条件 `_SIM_CRITIC_GLOBAL`）调用两次，构建 `self.q_global` 与 `self.q_global_target`；这两个网络在 `DDQNAgent.train` 中参与训练（target 网络 bootstrap 见 SimulationRL.py:7601，在线网络 `train_on_batch` 见行 7608，蒸馏进 local target 见行 7615，周期同步见行 7648–7650）。同文件内被 `FrameStackBPAgent.__init__`（行 603–606）在 `enable_global_critic=True` 时调用。

#### `def build_global_state(earth, current_sat_id=None, n_topk=8)` — CODE/routing_mappo.py:255
- 定位：CODE/routing_mappo.py:255
- 职责：从 `earth` 对象抽取 44 维 global state 向量（供集中式 critic）：行 268–302 遍历 `earth.LEO` 各 plane 的卫星，累加每颗 `sendBufferSatsIntra`/`sendBufferSatsInter` 缓冲长度得到全网队列长度数组，取 top-16 拥塞值；行 304–310 追加均值/最大/最小/方差 4 维；行 312–315 把同一份 top-16 复用为「ISL 队列摘要」16 维（行 312 注释自述「粗暴复用」）；行 317–320 追加 4 维硬编码 OD 指示 `[1,1,1,0]`（行 319 注释：占位 one-hot）；行 322–332 追加当前卫星的 plane/sat 归一化编号 4 维（解析 `current_sat_id` 的 `plane_sat` 格式，分别除以 7.0/20.0）。(FACT)
- 输入/输出：入 earth 实例与可选卫星 ID；返回 shape `(44,)` 的 `float32` 数组。任何遍历异常被静默吞掉（行 286–287 回退为 140 个 0）。
- 依赖关系：被 `CODE/SimulationRL.py:7133–7141`（`DDQNAgent.makeDeepAction`，条件 `self.q_global is not None`）调用，带每 50 次决策重算一次的缓存（SimulationRL.py:7134–7152）。

#### `def ppo_clipped_surrogate_loss(old_log_probs, new_log_probs, advantages, clip_eps=0.2)` — CODE/routing_mappo.py:344
- 定位：CODE/routing_mappo.py:344
- 职责：PPO clipped surrogate 目标函数，按公式 `L = −E[min(r·A, clip(r,1±eps)·A)]` 实现（行 353–356，`r = exp(new−old)`）。(FACT)
- 输入/输出：入三个 `tf.Tensor`；返回标量 loss 张量。
- 依赖关系：调用方未确认（CODE 内 grep 无调用点）。

#### `def value_loss_clipped(old_values, new_values, returns, clip_eps=0.2)` — CODE/routing_mappo.py:359
- 定位：CODE/routing_mappo.py:359
- 职责：PPO 的 clipped value loss：`0.5·mean(max((v_new−R)², (v_clip−R)²))`（行 364–367）。(FACT)
- 输入/输出：入三个 `tf.Tensor`；返回标量 loss 张量。
- 依赖关系：调用方未确认（CODE 内 grep 无调用点）。

#### `def gae_advantages(rewards, values, dones, gamma=0.99, lam=0.95)` — CODE/routing_mappo.py:370
- 定位：CODE/routing_mappo.py:370
- 职责：广义优势估计（GAE）：对长度 T 的轨迹反向递推 `δ_t = r_t + γ·V_{t+1}·(1−done) − V_t`、`A_t = δ_t + γλ(1−done)·A_{t+1}`（行 379–386），返回 `(advantages, returns=advs+values[:T])`（行 387–388）。(FACT)
- 输入/输出：入 T 长度 rewards/dones 与 T+1 长度 values（numpy）；返回两个长度 T 的 `float32` 数组。
- 依赖关系：调用方未确认（CODE 内 grep 无调用点）。

#### `class MAPPORolloutBuffer` — CODE/routing_mappo.py:395
- 定位：CODE/routing_mappo.py:395
- 职责：PPO 用的 on-policy rollout 缓冲，按卫星 ID 分桶存 transition 字典（docstring 行 396–411）。(FACT)
- 关键状态/结构：`self.max_steps`、`self._buffers`（`defaultdict(list)`，sat_id → transition 列表）、`self._total`（总计数）（行 413–415）。
- 关键流程/方法：
  - `__init__(max_steps=4096)`（行 412）：初始化上述三个字段。
  - `push(sat_id, transition)`（行 417）：向对应桶追加并 `_total += 1`。
  - `flush_all()`（行 421）：把 `_buffers` 拷成普通 dict 返回，随后重置 `_buffers` 与 `_total`。
  - `is_full()`（行 427）：返回 `_total >= max_steps`。
- 输入/输出：`push` 吃 `(sat_id, dict)`；`flush_all` 吐 `{sat_id: [transition, ...]}`。
- 依赖关系：唯一实例化点是本文件 `RecurrentMAPPOAgent.__init__`（行 494）；`push`/`flush_all`/`is_full` 无外部调用方（CODE 内 grep 无）。

#### `class RecurrentMAPPOAgent` — CODE/routing_mappo.py:435
- 定位：CODE/routing_mappo.py:435
- 职责：完整 MAPPO agent 组合体（GRU actor + 集中式 critic + BP prior + rollout buffer；docstring 行 436–450）。(FACT：组合关系；「完整」为 docstring 自述)
- 关键状态/结构：`self.actor`（GRU actor 模型，行 472–474）、`self.critic`（V 值集中式 critic，行 475）、`self.optimizer`（Adam，行 476）、PPO/GAE 超参数集（行 479–483）、`self.bp`（BackpressurePrior，行 486–488）、`self._hidden_states`（sat_id → GRU 隐状态向量，行 491）、`self.rollout`（MAPPORolloutBuffer，行 494）。
- 关键流程/方法：
  - `__init__(...)`（行 451）：按参数建 actor/critic/optimizer/BP/rollout，初始化隐状态字典。
  - `get_hidden(sat_id)`（行 496）：返回该卫星的 GRU 隐状态，不存在则建零向量。
  - `reset_hidden(sat_id=None)`（行 501）：清空全部或指定卫星的隐状态。
  - `select_action(obs, sat_id, bp_inputs, training=True)`（行 507）：取隐状态→`actor.predict` 单步得 logits 与新隐状态并回存（行 516–522）→ `bp.compute_bp(**bp_inputs)` 后用 `bp.score_actions` 把 BP 融合进 logits（行 525–527）→ `training=True` 时对 softmax 概率采样（含 1e-8 裁剪与重归一，行 530–536），否则 argmax（行 538–540）；返回 `(action, log_prob, score)`。
  - `critic_value(global_state)`（行 544）：`critic.predict` 返回标量 V 值。
  - `train_ppo_update(n_epochs=4, batch_size=256)`（行 551）：函数体只有 `raise NotImplementedError(...)`（行 564–567）——PPO 更新未实现。(FACT)
- 输入/输出：`select_action` 吃单帧 obs + BP 输入字典，吐动作/对数概率/融合分数。
- 依赖关系：调用方未确认（CODE 内 grep 无实例化点）。

#### `class FrameStackBPAgent` — CODE/routing_mappo.py:574
- 定位：CODE/routing_mappo.py:574
- 职责：简化组合体（docstring 行 575–583：不用 GRU、不用 PPO，DDQN + Frame Stack + BP prior + 可选集中式 Q 辅助头）。(FACT)
- 关键状态/结构：`self.K/obs_dim/action_size/enable_global_critic`（行 593–596）、`self.bp`（BackpressurePrior，行 597–599）、`self.global_critic`（`enable_global_critic=True` 时为编译好的 Q 版集中式 critic，MSE + Adam(1e-3)，否则 `None`，行 603–608）。docstring 行 601 注明 frame stack 缓冲由 satellite 自持、本类不存。
- 关键流程/方法：
  - `__init__(frame_stack_k=4, obs_dim=33, action_size=4, bp_beta=0.3, bp_k_progress=0.3, bp_k_loop=1.0, enable_global_critic=False, global_state_dim=GLOBAL_STATE_DIM)`（行 584）：初始化上述字段。
  - `score_actions(q_values, bp_inputs)`（行 610）：`bp.compute_bp(**bp_inputs)` 后 `bp.score_actions(q_values, bp_score)`，返回融合分数。
- 输入/输出：`score_actions` 吃 Q 值与 BP 输入字典，吐 4 维融合分数。
- 依赖关系：调用方未确认（CODE 内 grep 无实例化点；docstring 行 582 自述「由 SimulationRL.py 的 DDQNAgent 代理调用」，但 SimulationRL.py 中实际接线的是直接实例化的 `BackpressurePrior`（行 6268–6273）与 `build_centralized_critic_per_action`（行 6506–6518），未经过本类）。(FACT)

#### `def parse_env_config()` — CODE/routing_mappo.py:622
- 定位：CODE/routing_mappo.py:622
- 职责：从 `SIM_FRAME_STACK_K`/`SIM_BP_BETA`/`SIM_BP_K_PROGRESS`/`SIM_BP_K_LOOP`/`SIM_CRITIC_GLOBAL`/`SIM_MAPPO_MODE` 六个 env 读配置，返回 dict（行 624–631）。(FACT)
- 输入/输出：无参；返回 6 键配置字典。
- 依赖关系：调用方未确认（CODE 内 grep 无调用点；SimulationRL.py 在行 495–501 自行解析同名 env，不经本函数）。(FACT)

---

## 文件 `CODE/routing_multistep.py`（实测 138 行）

模块级说明：
- 模块 docstring（行 1–32）：声明本模块是 n-step DDQN 与 TD(λ) 训练方法基线的「纯多步回报计算」，只改训练目标、部署策略不变；强调纯 numpy、无 simulator import，便于脱离 SimPy 单测；定义了轨迹 dict 格式（`state/action/reward/next_state/is_terminal`）与返回 transition 的五元组契约 `(state, action, target_reward, bootstrap_state, done)`，并说明 n-step 需 `gamma**N` bootstrap、TD(λ) 以 `done=True` 阻止二次 bootstrap。(FACT：docstring 内容)
- imports（行 33）：仅 `numpy`。(FACT)
- docstring 行 13–14 引用的校验脚本 `scripts/diagnostic/verify_multistep.py` 在保留 CODE 树中不存在（glob `CODE/**/verify_multistep*` 无匹配）。(FACT)

#### `def nstep_transitions(traj, gamma, n)` — CODE/routing_multistep.py:36
- 定位：CODE/routing_multistep.py:36
- 职责：离线（整段轨迹）n-step 回报换算。对每跳 k：`k+n ≤ L−1` 时 `R = Σ_{i<n} γ^i·r_{k+i}`、bootstrap 状态取 `traj[k+n]['state']`、`done=False`；窗口越过终点时折扣累加到终点、`bootstrap_state` 为零向量、`done=True`（行 51–65）。空轨迹返回 `[]`（行 46–47）。(FACT)
- 输入/输出：入轨迹 list[dict]、`gamma`、`n`；返回 `(state, action, R, bootstrap_state, done)` 五元组列表（state 为 `float32`）。
- 依赖关系：调用方未确认（CODE 内 grep 无调用点）。SimulationRL.py 的 n-step 路径是在 `DDQNAgent._ms_store`（SimulationRL.py:6980–7012）与 `_ms_flush_lost`（行 7014–7031）内联重写的，未调用本函数。

#### `def nstep_transitions_streaming(traj, gamma, n)` — CODE/routing_multistep.py:69
- 定位：CODE/routing_multistep.py:69
- 职责：流式滑窗版 n-step——用 FIFO 缓冲模拟「窗口一满就发射最老跳的 n-step transition、到终点时把残余 <n 跳全部按终端回报 flush」的在线逻辑（行 85–105）；docstring（行 70–79）自述与 `nstep_transitions` 产出同一 transition 多重集合、仅顺序不同，并定位为「in-sim 滑窗代码可对照验证的纯本地参考」。(FACT)
- 输入/输出：同 `nstep_transitions`。
- 依赖关系：调用方未确认（CODE 内 grep 无调用点）。`CODE/SimulationRL.py:6986`（`_ms_store` docstring）注明 in-sim 滑窗逻辑「validated against routing_multistep.nstep_transitions_streaming (scripts/diagnostic/verify_multistep.py)」——即关系是对照参考而非运行时调用；所引用的校验脚本不在保留 CODE 树中。(FACT)

#### `def lambda_return_transitions(traj, gamma, lam, value_fn)` — CODE/routing_multistep.py:109
- 定位：CODE/routing_multistep.py:109
- 职责：TD(λ) 前视 λ-回报换算。先用 `value_fn`（契约 `V(s)=max_a Q(s,a)`）对每个状态估值（行 123），再对每跳 k 按 docstring 公式（行 113–116）累加各 m-step bootstrap 项与全程 MC 项的 λ 加权（行 125–135），逐跳输出 `(s_k, a_k, G^λ_k, None, True)`——恒 `done=True`、bootstrap 状态为 `None`（行 136–137）。空轨迹返回 `[]`。(FACT)
- 输入/输出：入轨迹、`gamma`、`lam`、`value_fn` 回调；返回五元组列表。
- 依赖关系：被 `CODE/SimulationRL.py:7052` import（`DDQNAgent._tdl_flush`，函数定义在行 7042）并在行 7060 被调用，`value_fn` 为行 7055–7057 定义的 `_vf`（`max_a` 过 `self.qNetwork`）；产出经 `experienceReplay.store` 入池（行 7061）。调用条件：`SIM_TD_LAMBDA>0`（SimulationRL.py:453–459 解析并与 `SIM_NSTEP>1` 互斥）。docstring 引用的单测脚本 `verify_multistep.py` 不在保留 CODE 树中（见模块级说明）。

---

## 文件 `CODE/routing_path_credit.py`（实测 1418 行）

模块级说明：
- 模块 docstring（行 1–26）：声明本模块实现「path-credit mixer 辅助训练（path_credit v1）」——逐跳 MC 回报回归 + 注意力加权信用分配，损失核心式 `L_path = Σ_k α_k·w_k·(q_k − stop_grad(R̃_k))²`；部署时只加载 qNetwork、丢弃 GRU/Transformer/mixer；模块分两部分（纯 Python 的 `PathTrajectoryReplay` 与 TF 部分），TF 为 lazy import 以便无 TF 环境跑 replay 单测。(FACT：docstring 内容；lazy-import 结构在行 317、384、471 等处的函数内 `import tensorflow as tf` 可确认)
- imports（行 27–33）：`__future__.annotations`、`collections`、`random`、`typing.Any`、`numpy`。(FACT)
- 全局常量：`TERMINAL_DELIVERED = "delivered"`（行 40）、`TERMINAL_LOST = "lost"`（行 41）、`TERMINAL_IDX = {delivered: 0, lost: 1}`（行 44，sample() 的 terminal_type 张量编码）。两个字符串常量被 `CODE/SimulationRL.py:10517` 与 `10577` import。(FACT)
- 训练时额外读取的 env：`_train_step_inner`（行 785–787）与 `_train_step_inner_rudder`（行 894–896）经 `__import__('os').environ` 在每次训练步读取 `SIM_PC_QW`（默认 0.3）、`SIM_PC_ALPHA_W`（默认 0.1）、`SIM_PC_W_PRIOR_W`（默认 0.05）作为三项辅助损失权重。(FACT)
- SimulationRL.py 侧配套 env 解析集中在 `CODE/SimulationRL.py:753–797`（`SIM_PATH_CREDIT*`、`SIM_PRED_*` 系列）；`SIM_PATH_CREDIT` 与多步基线（`SIM_NSTEP>1`/`SIM_TD_LAMBDA>0`）在行 754–757 互斥，与 `SIM_CRITIC_GLOBAL` 在行 6454–6458 互斥，与 CSR 在行 6462–6467 互斥。(FACT)
- 行为佐证：`CODE/tests/test_path_credit.py`（行 20–23 import `PathTrajectoryReplay` 与两个 TERMINAL 常量；模块 docstring 行 3–6 注明 replay 测试 1–7 为纯 Python、TF 测试 8–13 gated）；`CODE/tests/test_return_predictor.py:40` import `build_return_predictor`。

#### `class PathTrajectoryReplay` — CODE/routing_path_credit.py:47
- 定位：CODE/routing_path_credit.py:47
- 职责：双桶 FIFO 轨迹回放池——按包的结局（delivered/lost）分桶存完整逐跳轨迹，采样时 50/50 混合并按 `max_hops` 补齐/截断，用 Welford 运行均值按结局类型维护 MC 回报基线（docstring 行 48–65）。(FACT)
- 关键状态/结构：`self.delivered`/`self.lost`（两个 `deque(maxlen=maxlen//2)`，行 69–71）、`self.max_hops`、`self.gamma`（行 72–73）、`self._mean`/`self._count`（按结局类型的 Welford 运行均值与计数，行 76–77）。
- 关键流程/方法：
  - `__init__(maxlen=2000, max_hops=20, gamma=0.99)`（行 67）：`maxlen` 均分两桶，初始化上述字段。
  - `push(traj, terminal, lost_penalty=0.0)`（行 81）：空轨迹或非法 terminal 直接返回（行 91–92）；超长时保留末尾 `max_hops` 跳（行 98）；对每跳 dict 做防御性拷贝、`state`/`next_state` 深拷贝为 `float32`（行 99–105）；lost 轨迹把 `lost_penalty` 加到最后一跳 reward（行 108–110）；自后向前累乘 `γ` 算逐跳 MC 回报 `mc_return` 并写回每条目（行 113–122）；用每个 R_k 更新对应桶的 Welford 均值（行 125–129）；append 进对应桶（行 132–133）。
  - `size()`（行 137）：返回两桶轨迹总数。
  - `baseline(terminal)`（行 140）：返回该结局类型的运行均值（缺省 0.0）。
  - `__len__()`（行 143）：等同 `size()`。
  - `sample(batch_size)`（行 148）：双池空时抛 `RuntimeError`（行 163–165）；尽量 50/50、单桶空时全从另一桶抽（行 168–176）；桶够大则无放回抽样、不够则有放回（行 180–185）；把轨迹填入 `(B,H,D)` 的 `states/actions/mc_returns/mask/terminal_type` 数组（行 194–213）；训练目标 `targets` 取**原始 mc_return** 而非减基线的 advantage（行 215–235，行 216–226 注释给出理由：与 1-step TD 渐近目标一致、避免两个损失互相抵消），`advantages` 字段保留为诊断量；返回 8 键字典（含 `targets`、`baselines_per_traj`，行 237–246）。
- 输入/输出：`push` 吃逐跳 dict 列表 + 结局标签；`sample` 吐 numpy 批量字典。
- 依赖关系：在 `CODE/SimulationRL.py:3416–3425`（`Earth.__init__`，条件 `_SIM_PATH_CREDIT`）实例化为 `earth.pc_replay`（gamma 读 `SIM_GAMMA`，行 3420）。`push`：delivered 端在 `SimulationRL.py:7219`（`makeDeepAction` 目的 GT 分支），lost 端在行 1099（集中 helper `_pc_flush_lost`，定义在行 1066，由行 7120 等丢失点调用），lost_penalty 用 `_SIM_PATH_CREDIT_LOST_PENALTY`（行 1100）。`sample` 在 `SimulationRL.py:7728`（`DDQNAgent.train` 的 path-credit 段，行 7723–7732 门控：`_SIM_PATH_CREDIT` 且 `pc_mixer` 非空且 `size() >= _SIM_PATH_CREDIT_MIN_BUFFER`，每 `EVERY_K` 次一训）。`size()` 另用于行 7726、7757；`baseline()` 与 `max_hops`/`gamma` 属性在 `_save_pc_replay`（行 10520、10550–10552）被读；`_mean` 在 `_load_pc_replay_into`（行 10584–10586）被直接写。测试：`CODE/tests/test_path_credit.py`（如行 58 起 `TestReplay`）。

#### `def sinusoidal_position_encoding(max_hops, d_model)` — CODE/routing_path_credit.py:253
- 定位：CODE/routing_path_credit.py:253
- 职责：标准 Transformer 正弦位置编码表：偶数维 sin、奇数维 cos，`pos/10000^(2·(i//2)/d_model)`（行 256–262）。(FACT)
- 输入/输出：入序列长与模型维；返回 `(max_hops, d_model)` 的 `float32` numpy 数组。
- 依赖关系：被本文件 `PathCreditMixer.__init__`（行 431）与 `ReturnPredictor.__init__`（行 1057）调用；无 CODE 内其他调用方。

#### `def build_path_credit_mixer(state_dim, n_actions, d_model=64, ..., force_unit_w=False)` — CODE/routing_path_credit.py:269
- 定位：CODE/routing_path_credit.py:269
- 职责：工厂函数——lazy import TF（行 317）后把所有参数透传构造 `PathCreditMixer`（行 318–338）。docstring（行 290–316）说明 `use_gru=False` 时用正弦位置编码替代 GRU、`mode` 选 `'attention'`（PRD-A）或 `'rudder'`（PRD-T）、`pred_*` 仅 rudder 模式有效、`force_uniform_alpha`/`force_unit_w` 为消融开关（前向保留、输出被覆写）。(FACT)
- 输入/输出：入结构/超参；返回 `PathCreditMixer` 实例。
- 依赖关系：被 `CODE/SimulationRL.py:6540–6560`（`DDQNAgent.__init__`，条件 `_SIM_PATH_CREDIT`，行 6538）调用，产物存 `self.pc_mixer`；被 `CODE/tests/test_return_predictor.py:168` 与 `CODE/tests/test_path_credit.py:235` 调用。

#### `class PathCreditMixer` — CODE/routing_path_credit.py:341
- 定位：CODE/routing_path_credit.py:341
- 职责：token 编码 + （可选 GRU 或位置编码）+ 多头自注意力 + 双信用头（α、w）的辅助训练模块；组合量 `Q_path = Σ α·w·q`（q 来自被训的 qNetwork，梯度贯通），主损失为 `Q_path` 对全路径折扣回报的 Huber 回归（docstring 行 342–360）。(FACT)
- 关键状态/结构：超参数集（`state_dim/n_actions/d_model/gru_units/n_heads/max_hops/action_emb_dim/gpath_clip/use_gru`，行 388–396）；`mode`（`'attention'|'rudder'`，行 399–402，非法值抛 `ValueError`）与 `pred_warmup_steps`、`_pc_train_count` 训练步计数（行 403–404）；`pred_contrib_mode`（`'attention'|'increment'`，行 409–414）；`self.predictor`（仅 `mode=='rudder'` 时惰性挂一个 `ReturnPredictor`，否则 `None`，行 417–428）；`self._pe`（正弦位置编码常量，行 431–432）；Keras 层：`action_emb`（Embedding）、`token_proj`（Dense+relu）、可选 `gru`、`transformer`（MultiHeadAttention）、`alpha_proj`、`w_proj`（Dense(1)）（行 435–455）；`self.optimizer`（独立 Adam，带 clipnorm=1.0，行 462）；`self._tf_train_step`/`self._captured_q`/`self._retrace_count`（tf.function 缓存，行 465–466、651–652）。
- 关键流程/方法：
  - `__init__(...)`（行 362）：落盘超参与开关、按需建 `ReturnPredictor`、建全部 Keras 层、跑 `_build_once` 实体化权重、建独立优化器。
  - `_build_once()`（行 470）：用全零 dummy 输入跑一遍前向（行 473–492），使各层 `trainable_variables` 就位。
  - `trainable_variables`（property，行 494/495）：汇总 action_emb/token_proj/transformer/alpha_proj/w_proj（及可选 gru）的可训练变量列表（行 496–505）。
  - `_forward(q_network, states, actions, mask)`（行 509）：拍平批次经 `q_network` 得逐动作 Q，按 one-hot 取出所执行动作的 `q_k`（梯度通 qNetwork，行 526–531）；`stop_gradient(q_k)` 与 state/action 嵌入拼 token（行 534–537）；GRU 或「token+正弦 PE」进 MultiHeadAttention（带 `mask∧mask^T` 注意力掩码，行 540–550）；`alpha_proj` logits 经 −1e9 掩码后 softmax 得 α（行 553–556），`force_uniform_alpha` 时覆写为掩码感知的均匀分布（行 564–568）；`w_proj` 经 softplus 得 w（行 571），`force_unit_w` 时覆写为有效跳 1/填充 0（行 577–579）；返回 `(q_k, alpha, w)`。
  - `train_step(q_network, batch, lambda_path=0.1)`（行 585）：把 batch 各字段转 tensor（行 611–616）、`_pc_train_count += 1`；rudder 模式先用同批数据训 predictor（`predictor.train_step`，行 627），过 warmup 后取 `predictor.compute_contribution` 作为外部 α 软目标（行 630–634），warmup 期传零占位 + `ext_active=False`（行 656–660）；按模式把 `_train_step_inner` 或 `_train_step_inner_rudder` 包成带 `input_signature` 的 `tf.function`（行 637–684）并执行；汇总 10 项标量指标（α 熵、q_mean、w_mean、各分项损失、α 最大值、w 标准差、Q_path/G_path 均值），rudder 时并带 `pred_*` 前缀的 predictor 指标（行 686–701）；返回 `(loss, metrics)`。
  - `_train_step_inner(states, actions, targets, mask, lambda_path)`（行 703，PRD-A）：GradientTape 内 `_forward` 得 `(q_k, α, w)`；`G_path` 取 hop-0 的 mc_return、`stop_gradient` 并 clip 到 `±gpath_clip`（行 737–739，行 727–736 注释记录了一次未 clip 导致发散的失败案例）；`Q_path = Σ α·w·q_k·mask`（行 740）；`L_path_global` 为 δ=50 的 Huber（行 742–748）；`L_q` 为 α/w 停梯度加权的逐跳 MC 回报 MSE（行 755–763）；`L_alpha` 为 α 对「逐跳平方误差归一化分布」的交叉熵（行 767–773）；`L_w_prior` 为 `(w−1)²` 锚（行 776–779）；总损失 `L_path = L_path_global + Q_W·L_q + ALPHA_W·L_alpha + W_PRIOR_W·L_w_prior`，乘 `lambda_path`（行 785–789）；对 qNetwork + mixer 全部变量求梯度、过滤 None 后用自有优化器更新（行 791–795）；返回损失与 10 项指标（行 798–814）。
  - `_train_step_inner_rudder(..., alpha_tilde_external, lambda_path, ext_active)`（行 816，PRD-T）：与 `_train_step_inner` 相同，唯一差异是 `L_alpha` 的软目标用 `tf.cond(ext_active, ...)` 在外部 RUDDER 贡献增量（停梯度、掩码后重归一，行 871–874）与残差归一化回退之间切换（行 877–881）。
  - `save_weights(path)`（行 925）：把 mixer 各层（含可选 GRU，**不含 qNetwork**——行 926 注释）按 `层名__序号` 键存 `np.savez_compressed`（行 927–940）。
  - `load_weights(path)`（行 942）：按同一键约定从 npz 读回并 `set_weights`（行 943–960）。
- 输入/输出：`train_step` 吃 qNetwork + `PathTrajectoryReplay.sample()` 的 batch 字典，吐 `(loss float, metrics dict)`。
- 依赖关系：实例化见 `build_path_credit_mixer`（SimulationRL.py:6540–6560 → `self.pc_mixer`）。`train_step` 在 `SimulationRL.py:7729–7732`（`DDQNAgent.train`）被调用，传入 `self.qNetwork`；`save_weights` 在行 11375（interrupt-save）被调用；`load_weights` 在行 12138（warm-start resume，经 `attempt_checkpoint_load`，env `SIM_PC_MIXER_PATH` 提供路径）被调用。类内引用 `ReturnPredictor`（行 419）。

#### `def build_return_predictor(state_dim, n_actions, d_model=64, ..., dropout=0.0)` — CODE/routing_path_credit.py:988
- 定位：CODE/routing_path_credit.py:988
- 职责：工厂函数——lazy import TF（行 1000）后透传构造 `ReturnPredictor`（行 1001–1011）。(FACT)
- 输入/输出：入结构/超参；返回 `ReturnPredictor` 实例。
- 依赖关系：被 `CODE/tests/test_return_predictor.py:40`、`149` 调用；CODE 内生产代码无调用点（`PathCreditMixer` 在行 419 直接实例化 `ReturnPredictor`，不经本工厂）。(FACT)

#### `class ReturnPredictor` — CODE/routing_path_credit.py:1014
- 定位：CODE/routing_path_credit.py:1014
- 职责：因果 Transformer 编码器，在每个前缀位置预测整条路径的总折扣回报 G_0，用于 RUDDER 风格贡献分解（PRD-T 模式的 α 软目标来源；类前注释行 963–986 与 docstring 行 1015–1031）。贡献定义 `c_k = |g0_hat^k − g0_hat^(k−1)|`（`g0_hat^{−1}:=0`），归一化后得 `alpha_tilde`。(FACT)
- 关键状态/结构：超参数集（行 1047–1054）；`self._pe`（正弦位置编码常量，行 1057–1058）；`self.action_emb`、`self.token_proj`（行 1061–1069）；`self.encoder_layers`（n_layers 个 dict，各含 `mha`/`ln1`/`ffn1`/`ffn2`/`ln2` 五个子层，行 1072–1086）；`self.head`（Dense(1) 标量预测头，行 1089）；`self.optimizer`（独立 Adam，clipnorm=1.0，行 1095）；`self._tf_train_step`/`self._tf_predict`（tf.function 缓存，行 1097–1098）。
- 关键流程/方法：
  - `__init__(state_dim, n_actions, d_model=64, n_heads=4, n_layers=2, max_hops=20, lr=1e-4, action_emb_dim=8, dropout=0.0)`（行 1033）：建层、`_build_once` 实体化、建优化器。
  - `_build_once()`（行 1100）：全零 dummy 前向一遍以实体化权重（行 1103–1107）。
  - `trainable_variables`（property，行 1109/1110）：汇总 action_emb/token_proj/head 与各编码器子层的可训练变量（行 1111–1125）。
  - `_make_causal_mask(H, key_mask)`（行 1127）：生成 `(B,H,H)` 布尔注意力掩码 = 下三角因果掩码 ∧ key 有效性（行 1142–1146）。
  - `_forward(states, actions, mask, training=False, return_attention=False)`（行 1148）：`[state, action_emb]` 拼 token → Dense+relu → 加 PE（行 1169–1172）；逐编码器层做带因果掩码的 MHA + 残差/LN + FFN + 残差/LN（行 1177–1196），`return_attention=True` 时收集各层注意力权重；`head` 输出 squeeze 成 `(B,H)` 的 `g0_hat`（行 1198–1201）。
  - `predict_g0(states, actions, mask)`（行 1203）：eager 前向封装（转 tensor 后调 `_forward`），返回 `(B,H)`。
  - `_attention_contribution(attn_scores_per_layer, mask)`（行 1211）：SECRET 风格读出——取最后一层注意力、按头取均值、以「最后一个有效位置」为 query 取其对各 key 的注意力分布（`tf.gather(..., batch_dims=1)`，行 1232–1243），乘掩码后重归一，得 `(B,H)` 的 `alpha_tilde`。
  - `compute_contribution(states, actions, mask, mode="increment")`（行 1254）：`mode='attention'` 时走 `_forward(return_attention=True)` + `_attention_contribution`（行 1280–1291）；`mode='increment'` 时算相邻前缀 `g0_hat` 差分的绝对值、掩码后按行归一（行 1294–1303）；两模式都在行贡献和退化（<2e-6）时回退为掩码均匀分布（行 1289–1290、1305–1310）；`mode` 非法抛 `ValueError`（行 1276–1278）。
  - `train_step(states, actions, mask, g0_true)`（行 1313）：把 `_train_step_inner` 包成带 `input_signature` 的 `tf.function`（行 1334–1343）执行，返回 `{L_pred, g0_mae, contribution_entropy}` 三项 float 指标（行 1345–1350）。
  - `_train_step_inner(states, actions, mask, g0_true)`（行 1352）：GradientTape 内前向得 `g0_hat`，`L_pred` = 掩码内 `(g0_hat − G_0)²` 均值（G_0 广播到逐前缀，行 1355–1362）；用自有优化器更新自身变量（行 1364–1367）；另算 MAE 与贡献熵诊断量（行 1370–1378）。
  - `save_weights(path)`（行 1381）：把 action_emb/token_proj/head 及各编码器子层按 `rp_*__序号` 键存 npz（行 1382–1394）。
  - `load_weights(path)`（行 1396）：按同键约定读回 `set_weights`（行 1397–1418）。
- 输入/输出：`train_step` 吃 `(B,H,D)` states、`(B,H)` actions/mask、`(B,)` 的 G_0 真值，吐指标 dict；`compute_contribution` 吐 `(B,H)` 归一化 `alpha_tilde`。
- 依赖关系：被本文件 `PathCreditMixer.__init__`（行 419，`mode=='rudder'` 时）实例化；`train_step`/`compute_contribution` 被 `PathCreditMixer.train_step`（行 627、631–633）调用；`predict_g0` 仅被 `CODE/tests/test_return_predictor.py`（行 63、73、77、147、155）调用；`save_weights`/`load_weights` 调用方未确认（CODE 生产代码 grep 无调用点——SimulationRL.py 的 resume/save 只覆盖 mixer 与 replay，见行 11375、12138）。
