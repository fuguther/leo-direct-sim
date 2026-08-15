# 片段 s3：`CODE/SimulationRL.py` 第 5638–7884 行

### 文件 `CODE/SimulationRL.py`（实测 12556 行）

本片段覆盖第 5638–7884 行。实测全文件 12556 行（`wc -l`）。本范围符号核对清单（`grep -nE '^(class |def )'` 过滤 5638–7884）：5 个顶层 class（`hyperparam` 5638、`QLearning` 5682、`GraphMessagePassingReadout` 5924、`DDQNAgent` 6190、`ExperienceReplay` 7770），6 个顶层 def（`_np_mlp_forward` 5833、`_shadow_record` 5849、`_shadow_dump` 5876、`graphStateDim` 5901、`raacGraphStateDim` 5913、`_graph_custom_objects` 6186）。

模块级说明（本范围内的模块级语句与常量，带行号）：

- 5822–5832 行：注释块，说明决策时推理后端开关 `SIM_INFER_BACKEND` 的三个取值 `keras`（默认，eager `__call__`）、`tffunc`（`tf.function` 包装活模型）、`numpy`（手写 MLP 前向，注释标注 EVAL-ONLY 但 6775 行实现处注释称已支持 train+eval——两处注释口径不一致，FACT）；并注释说明该加速门控只对标准 3-Dense Sequential MLP 生效，csr/cvar 模型回退 keras。
- 5841–5844 行：注释块，说明 `SIM_SHADOW_INFER` 是只测量开关：比较 numpy 决策前向与 tffunc 在相同活权重下的一致性（argmax/排序翻转率、最小 Q 间隔）。
- 5845–5847 行：模块级全局字典 `_SHADOW`，字段 `n / argmax_flip / order_flip / max_abs / gap_lt_1e-7 … 1e-4 / flip_gaps / skipped / seen`，累计影子对比统计（FACT）。
- 5897–5898 行：`import atexit as _atexit` 并 `_atexit.register(_shadow_dump)`，进程退出时自动转储影子统计（FACT）。
- `_SIM_SHADOW_INFER` 定义在本范围外（`CODE/SimulationRL.py:803`，env `SIM_SHADOW_INFER`，默认 0=关）；本范围内只引用。
- 7879–7881 行：分节注释横幅 `### Functions ###`，7884 行 `# @profile`，其后 7885 行起为顶层函数区（下一个片段范围）。

---

#### `class hyperparam` — CODE/SimulationRL.py:5638

- 定位：CODE/SimulationRL.py:5638
- 职责：把一组模块级全局超参数快照进一个对象，供 `QLearning` / `DDQNAgent` 构造时读取 (FACT)。
- 关键状态/结构：`__init__` 从模块全局拷贝 `alpha, gamma, epsilon, ArriveR(=ArriveReward), w1, w2, w4, again(=againPenalty), unav(=unavPenalty), tau, updateF, batchSize, bufferSize, MAX_EPSILON, MIN_EPSILON, LAMBDA, plotPath, coordGran, ddqn, latBias, lonBias, diff, explore, reducedState, online(=onlinePhase)`（5639–5670；这些全局定义于同文件 231–613 行一带，部分可被 env 覆盖，如 `SIM_W1` 270 行、`SIM_GAMMA` 274 行、`SIM_LR` 563 行）；`hardUpdate` 存为布尔 `hardUpdate==1`（5657）；`importQ` 存 `importQVals`（5658）；`pathing` 为构造入参（5652）。
- 关键流程/方法：`__init__`(5639) 做上述全局→属性的拷贝；`__repr__`(5672) 返回 alpha/gamma/epsilon/w1/w2 的格式化字符串。
- 输入/输出：入参 `pathing`（路由方式标识）；输出为属性容器对象。
- 依赖关系：被 `initialize()` 在 8058 行构造（`hyperparams = hyperparam(pathing)`）；构造出的对象传给 `QLearning.__init__`（5595/5597）与 `DDQNAgent.__init__`（8062/8070）。`__repr__` 调用方未确认。

---

#### `class QLearning` — CODE/SimulationRL.py:5682

- 定位：CODE/SimulationRL.py:5682
- 职责：基于 6 维 numpy Q 表的逐跳表格 Q-Learning 路由 agent（FACT，docstring 5684–5688：Q(s,a) 表前 5 维是环境状态、第 6 维是 4 动作）。
- 关键状态/结构：`linkedSats`（'U'/'D'/'R'/'L' → 邻接卫星或 None，5690–5695）；`actions=('U','D','R','L')`（5697）；`qTable` 形状 `(3,3,3,3,NGT,4)`，未导入时随机初始化（5703–5707）；`nStates = 3*3*3*3*NGT`（5700）；从 `hyperparams` 拷贝 `alpha/gamma/maxEps/minEps/w1/w2`（5709–5716）；`oldState/oldAction`（5718–5719）；`epsilon` 为 list（5712，原直接取 hyperparams.epsilon 的代码被注释掉，5711）。
- 关键流程/方法：
  - `__init__`(5683) 计算四方向邻接卫星（调用 `getLinkedSats`，9328）、建/导入 Q 表、拷贝超参。
  - `makeAction(block, sat, g, earth, prevSat=None)`(5721)：若当前卫星的 linkedGT 即报文目的地，则把 `ArriveReward` 写进上一跳卫星的 Q 表并按需画投递路径（5742–5749）后返回 0；否则 `getState`（9443）取 5 元组状态（5754），explore 时按 `alignEpsilon` 衰减 ε 随机选可用方向（5758–5761），否则对 `qTable[newState]` 取 argmax、不可用方向置 `-np.inf` 后重选（5765–5769）；有 `prevSat` 时按重访惩罚 `againPenalty` 或 `getDistanceReward`+`getQueueReward` 计算奖励（5777–5785），并用 `(1-α)·oldQ + α·(r+γ·maxQ(s'))` 更新**上一跳**卫星的 Q 表（5791–5794）；把 newState/动作下标写回 `block.oldState/oldAction`（5801–5802），返回 `[下一跳ID, 经度°, 纬度°]`（5774, 5806）。
  - `alignEpsilon(earth, sat)`(5808)：按 `minEps + (maxEps-minEps)·exp(-LAMBDA·step/(decayRate·CurrentGTnumber²))` 计算 ε 并追加到 `earth.epsilon`（5809–5812）。
  - `__repr__`(5814)：返回目的地数/动作空间/状态数/qTable 的格式化串。
- 输入/输出：`makeAction` 返回 `0`（已到最后一跳）或 `[ID, lon°, lat°]` 三元组；`alignEpsilon` 返回 float ε。
- 依赖关系：调用 `getLinkedSats`(9328)、`getState`(9443)、`getDistanceReward`(10296)、`getQueueReward`(10269)、`plotShortestPath`(8968)；访问 `prevSat.QLearning.qTable`（5743/5792/5794，即跨卫星互写 Q 表，FACT）。被 `Earth.initializeQTables`(5574) 在 5595/5597 行构造并挂到每颗卫星 `sat.QLearning`；`makeAction` 被 `Satellite.receiveBlock`(2017) 的 2071/2078 行与 `Earth.updateSatelliteProcessesRL`(4504) 的 4562/4582/4632/4650/4694/4712 行调用；`alignEpsilon` 仅被本类 `makeAction` 在 5758 行调用。测试佐证：未找到直接针对 `QLearning` 的测试。

---

#### `def _np_mlp_forward(s, Ws)` — CODE/SimulationRL.py:5833

纯工具函数。以 float32 numpy 复现 `Dense(relu)→Dense(relu)→Dense(linear)` 三层 MLP 前向：`x@W0+b0`、relu、`@W2+b2`、relu、`@W4+b4`（5835–5838，Ws 为 6 个权重数组的列表）(FACT)。输入状态向量 `s` 与权重列表 `Ws`，输出 Q 向量。被 `_shadow_record`(5858) 与 `DDQNAgent._build_infer_fn` 的 numpy 后端闭包 `_np_infer`(6785) 调用。

---

#### `def _shadow_record(agent, s, q_tf)` — CODE/SimulationRL.py:5849

测量辅助函数。取 `agent.qNetwork.weights` 的 numpy 副本，若非 6 个张量（非标准 3-Dense MLP）则计 `skipped` 返回（5852–5856）；否则并行算 `_np_mlp_forward` 与传入的 `q_tf`，累计样本数、max|Δ|、argmax 翻转、全序翻转、最小相邻 Q 间隔分档计数（1e-7…1e-4）到全局 `_SHADOW`（5857–5872）；任何异常吞掉并计 `skipped`（5873–5874）(FACT)。仅被 `DDQNAgent._infer` 在 `SIM_SHADOW_INFER` 采样命中时调用（6728）。

---

#### `def _shadow_dump()` — CODE/SimulationRL.py:5876

测量辅助函数。`_SIM_SHADOW_INFER` 关闭或无样本时直接返回（5878–5879）；否则打印一行汇总（采样数、argmax/order 翻转率、max|Δ|、间隔分档、翻转时间隔最大值、skipped，5881–5885），并把 `_SHADOW` 写成 JSON——路径取 env `SIM_SHADOW_OUT`，未设则为 `<outputPath>/run_trace/shadow_infer.json`（5886–5893），写文件异常静默忽略（5894–5895）(FACT)。仅由 `atexit` 注册调用（5898）。

---

#### `def graphStateDim()` — CODE/SimulationRL.py:5901

纯工具函数。返回 C4/C5 图编码器扁平状态宽度：`n*14 + n*n + 4*n + 12 + (4 if _SIM_M2_FIX else 0)`，其中 `n=_GRAPH_MAX_NODES`，14 即 `_GRAPH_NODE_FEAT_DIM`（5901–5910）(FACT)。被 `DDQNAgent.__init__`（6235）调用以定 `stateSize`；测试 `CODE/tests/test_runtime_effect_receipt.py:103-107` 断言该公式与 `raacGraphStateDim` 的维度契约。

---

#### `def raacGraphStateDim()` — CODE/SimulationRL.py:5913

纯工具函数。返回 C6/C7（reliability-aware action-centric）图状态宽度：`n*17 + n*n + 4*n + 4*9`，17=`_RAAC_NODE_FEAT_DIM`、9=`_RAAC_ACTION_FEAT_DIM`（5913–5921）(FACT)。被 `DDQNAgent.__init__`（6238）调用；测试佐证 `CODE/tests/test_runtime_effect_receipt.py:105`、`CODE/tests/test_raac_tensorflow_contract.py:74`。

---

#### `class GraphMessagePassingReadout(Layer)` — CODE/SimulationRL.py:5924

- 定位：CODE/SimulationRL.py:5924
- 职责：C4/C5（及 RAAC C6/C7）的图编码 Keras 自定义层：解析定长扁平化 k-hop 子图（节点特征 + 有向 ISL 邻接 + U/D/R/L 读出掩码 + 尾部），做边上消息传递，输出 4 方向读出嵌入加尾部 (FACT，docstring 5925–5934；mode='gat' 为 C4 多头注意力，mode='mpnn' 为 C5 非注意力均值聚合)。
- 关键状态/结构：构造参数 `mode/max_nodes/feat_dim/hidden_dim/num_layers/num_heads/tail_dim/reliability_aware/aoi_gate/action_feat_dim`（5935–5951）；`aoi_gate` 只在 `reliability_aware` 为真时生效（5950）；gat 模式要求 `hidden_dim % num_heads == 0`（5952–5953）；建有 `node_in = Dense(hidden_dim, relu)`（5954）与可选 `reliability_rate = Dense(1, softplus)`（5955–5958）。`build` 阶段按模式建权重：gat 为每层 `gat_W`(heads,h,hd)、`gat_a_src/a_dst`(heads,hd)、`gat_self_W`(h,h)、`gat_bias`(h,)（5993–6030）；mpnn 为每层 `msg_W/self_W`(h,h)、`mpnn_bias`(h,)（6031–6053）；另有 `dir_default`(4,h) 零初始化可训练向量（6054–6059）。
- 关键流程/方法：
  - `__init__`(5935) 校验 mode∈{gat,mpnn}、存超参、建输入投影层与可选 reliability 率层。
  - `get_config`(5960) 把全部构造参数并入 Keras 序列化配置。
  - `from_config(cls, config)`(5977, classmethod)：反序列化时若缺 `aoi_gate` 且 `reliability_aware` 为真，用当前运行时全局 `_RAAC_AOI_GATE` 回填该字段（5986–5989；docstring 说明用于加载 2026-07-18 前未序列化该字段的旧 RAAC H5 检查点）。
  - `build(input_shape)`(5991) 按模式创建上述全部可训练权重并调用 `super().build`。
  - `_parse(flat)`(6062)：把扁平输入切回 `node`(B,n,feat)、`adj`(B,n,n)、`readout`(B,4,n)、`tail`（6063–6070）；取节点特征第 7 维作 valid-node 掩码并用它屏蔽邻接与读出（6071–6073）；`action_feat_dim>0` 时把 tail 重形为 (B,4,action_feat_dim)（6074–6077）。
  - `_gat_layer(h, adj, node_mask, layer_idx, reliability=None)`(6079)：多头 GAT 单层——einsum 投影、src/dst 注意力打分、leaky_relu、按邻接边掩码 softmax，可选乘 reliability、再归一化，聚合消息加 self 项与 bias 后 relu 并按节点掩码清零（6080–6100）；返回 (输出, 注意力权重 alpha)。
  - `_mpnn_layer(h, adj, node_mask, layer_idx, reliability=None)`(6102)：非注意力均值聚合——消息 `h@msg_W`、（可选 reliability 加权的）邻接归一化聚合、加 self 项与 bias 后 relu 并掩码（6103–6111）；返回 (输出, 聚合消息 msg)。
  - `_reliability_weights(node, node_mask)`(6113)：RAAC AoI 门控——取节点特征第 15 维（observed）、第 16 维（age_norm，截负为 0），用前 15 维经 `reliability_rate` 得 rate 并加 `_RAAC_MIN_RELIABILITY_RATE`，算 `observed·exp(-rate·age)`；root 节点（特征第 6 维>0.5）强制 reliability=1，最后乘节点掩码（6115–6122）。
  - `_encode(flat, return_stats=False)`(6124)：`_parse`→`node_in` 投影→可选 reliability→按层数跑 gat/mpnn（6125–6137）；方向读出 = 读出掩码（可选 reliability 加权）对 h 加权平均，无方向时用 `dir_default`（6139–6146）；RAAC 模式拼 `[dir_emb, root, action_feat]`（6147–6149），非 RAAC 拼 `[dir_emb 展平, tail]`（6151）；`return_stats` 时附统计：embedding 范数均值、reliability 均值、GAT 注意力熵/最大权重/头均衡 std、MPNN 消息范数均值（6156–6176）。
  - `call(flat)`(6178) 返回 `_encode` 的编码向量（Keras 前向入口）。
  - `diagnostics(flat)`(6181) 返回 `_encode(..., return_stats=True)` 统计项的 float 字典。
- 输入/输出：输入扁平张量 (B, graphStateDim() 或 raacGraphStateDim())；`call` 输出 (B, 4·hidden_dim + tail_dim)（非 RAAC）或 (B, 4, hidden_dim+hidden_dim+action_feat_dim)（RAAC 路径，6147–6149）(FACT)。
- 依赖关系：被 `DDQNAgent._create_graph_model`(7402–7414) 以名 `graph_encoder` 实例化进 qNetwork；经 `_graph_custom_objects`（6186）注册供 `keras.models.load_model` 反序列化（6331/6587/6642）；跨文件被 `CODE/tools/benchmark_graph_execution.py:33,38` import 并实例化。测试佐证：`CODE/tests/test_raac_tensorflow_contract.py:39-71`（from_config 回填 + `_reliability_weights` 门控语义）、`:73-87`（RAAC 模型输出 4 路共享动作分）、`CODE/tests/test_runtime_effect_receipt.py:109-120`（门控公式源码契约）、`CODE/tests/test_raac_aoi_gate.py:78,91`（层实例化）。

---

#### `def _graph_custom_objects()` — CODE/SimulationRL.py:6186

纯工具函数。返回 `{"GraphMessagePassingReadout": GraphMessagePassingReadout}`（6187）(FACT)，供 `keras.models.load_model(..., custom_objects=...)` 反序列化含该自定义层的检查点。被 `DDQNAgent.__init__` 的三处 `load_model` 调用使用（6331、6587、6642）。注：`CODE/leo_sim/learning.py:272` 存在同名函数（新平台侧独立实现），与本函数无调用关系。

---

#### `class DDQNAgent` — CODE/SimulationRL.py:6190

- 定位：CODE/SimulationRL.py:6190（类体延伸至 7766，共约 1577 行，20 个方法）
- 职责：Deep (Double) Q-Network 路由 agent：按多种状态模式构建状态、用 qNetwork/qTarget 做 ε-贪婪决策、把逐跳转移存入经验回放并批量训练 (FACT，类体与方法实现)。
- 关键状态/结构：`actions=('U','D','R','L')`（6192）；`states` 名称列表随 `reducedState/diff_lastHop/_SIM_M2_FIX/_SIM_M3_DYNAMICS/_SIM_STATE_MODE('c2'..'c7')` 变化（6194–6239）；`stateSize`/`_base_state_dim`，MAPPO frame-stack 与 `temporal_encoder` 可改写 `stateSize`（6244–6260）；`routing_mode` 取全局 `SIM_ROUTING_MODE`，`_SIM_CSR_MODE=='csr'` 时强制 `ddqn_csr`（6304–6318）；可选 `_mappo_bp` Backpressure 先验（6265–6281）；导入模式下预加载检查点并按输出维度/伴随 `csr_w_*.npz` 自动判别 `ddqn/ddqn_cvar/ddqn_csr`（6323–6403，`_SIM_FAIL_CLOSED` 下方法不符直接 raise）；`n_quantiles`（6405–6412）；routing hooks 三件套 `_local_stats_hook/_scoring_hook/_selector_hook`（6414–6434）；`experienceReplay = ExperienceReplay(bufferS)`（6444）；`qNetwork/qTarget`（6478–6499 新建或 6573–6672 导入）；可选 `q_global/q_global_target` 集中式 critic（6504–6532）与 `pc_mixer` 路径信用混合器（6538–6572）；`_SHADOW` 影子统计经 `_infer` 采样；`_w_version` 权重版本号（7643）。
- 关键流程/方法（逐个）：
  - `__init__(self, NGT, hyperparams, earth, sat_ID=None)`(6191)：如上组装状态空间定义、超参拷贝（6287–6303）、路由模式判别与 hooks、互斥检查（`_SIM_PATH_CREDIT`×`_SIM_CRITIC_GLOBAL`、`_SIM_PATH_CREDIT`×CSR，6454–6467）、建/导入网络、初始同步 qTarget（6492）、建 critic/pc_mixer、末尾 `_capture_encoder_initial_weights()`（6679）。`sat_ID=None` 表示这是 earth 级共享 agent，打印摘要。
  - `_graph_encoder_layer`(6681)：c4–c7 模式下从 `qNetwork.get_layer('graph_encoder')` 取编码层，否则/异常返回 None。
  - `_encoder_weights_vector`(6689)：把编码层全部可训练变量拼成一个 float32 一维向量，无层/无变量返回 None。
  - `_capture_encoder_initial_weights`(6703)：存编码层初始权重向量副本到 `_encoder_initial_weight_vec`。
  - `_encoder_weight_stats`(6707)：返回 (当前权重范数, 与初始向量的差范数)，无初始快照时后者为 nan。
  - `_infer(newState)`(6717)：决策时 Q 前向入口——惰性构建并缓存 `_infer_fn`（6720–6723），调用之；`_SIM_SHADOW_INFER` 开启时按 1-in-N 采样调 `_shadow_record`（6725–6728）。返回形状 (1, actionSize) 的 np.ndarray。
  - `_build_infer_fn`(6731)：按 env `SIM_INFER_BACKEND` 构建前向闭包——非标准路由模式（csr/cvar）或 backend=keras 时用 eager `net(s).numpy()`（6757–6759）；`tffunc` 用固定输入签名 (1,stateSize) 的 `tf.function`（6749–6755, 6760–6763）；`numpy` 要求 6 个权重张量否则回退 tffunc，命中时用 `_w_version`+网络对象 id 做版本化权重缓存、前向走 `_np_mlp_forward`（6764–6786）；未知后端回退 keras（6787–6789）；经内部 `_record_backend`（6737–6747）把生效后端与回退原因记入 `earth._infer_backends_effective/_infer_backend_fallbacks`。
  - `getNextHop(newState, linkedSats, sat, block)`(6791)：选动作并返回下一跳。explore 分支按 `alignEpsilon` 得 ε 后随机选，不可用方向先存一条 `unavPenalty` 自转移（terminated 语义随 `_SIM_MULTISTEP` 变，6806–6811）再重抽（6801–6814）；exploit 分支：`noPingPong` 时若某邻居即目的地 linkedSat 则直达返回（6818–6836）；调 `_local_stats_hook.on_pre_decision`（6856）；csr 模式走 `csr_q_values` 否则 `_infer`（6857–6861）；c6/c7 调 `_sample_raac_reliability`（6862–6863）；有 `_mappo_bp` 时计算 own/nbr 队列、progress、loop 四方向数组并按 `_SIM_BP_CORRECT` 选 DBPR 逐 commodity 公式或 `compute_bp`，`_SIM_BP_ONLY` 时 Q 置零，融合分数写回 `q_raw`（6867–6937，异常静默退化为纯 Q，6938–6940）；`_scoring_hook.score`→`_selector_hook.select_exploitation` 得动作（6941–6948）；写决策日志（`_append_decision_log`，6952–6955）与 eval 期 `REPLAY_TRACE` 决策轨迹（6958–6972）；返回 `[ID, lon°, lat°], actIndex`，异常返回 -1（6975–6978）。
  - `_ms_store(block, s_old, a_old, reward, s_new, terminated)`(6980)：n 步基线存储——`_SIM_TDLAMBDA_ON` 时转 `_tdl_store`；否则把 (s,a,r) 追加 `block.ms_buf`，terminated 时把窗内全部前缀折扣回报以 done=True 落盘并清空，窗满 `_SIM_NSTEP` 时以最老 hop 的 N 步折扣回报 + 自举 s_new 落一条并左移（6995–7012）。
  - `_ms_flush_lost(block)`(7014)：丢包时把 `block.ms_buf` 中未完成的 n 步窗按 terminal（无自举）全部 flush；`_SIM_TDLAMBDA_ON` 时转 `_tdl_flush`（7018–7031）。
  - `_tdl_store(block, s_old, a_old, reward, terminated)`(7033)：TD(λ) 基线——只追加轨迹，terminal 时调 `_tdl_flush`。
  - `_tdl_flush(block)`(7042)：用 `routing_multistep.lambda_return_transitions` 对缓存轨迹算前向 λ-回报（value_fn = 当前 qNetwork 的 max_a Q，7055–7057），每跳以 done=True 存入回放并清空（7049–7062）。
  - `makeDeepAction(block, sat, g, earth, prevSat=None)`(7064)：主决策入口——`getDeepLinkedSats` 取邻接并建 next_action_mask（7094–7097）；按 `_SIM_STATE_MODE`/reducedState/diff/diff_lastHop 选 `getDeepStateVisK/VisKFlat/VisKGraph/RAACGraph/Reduced/Diff/DiffLastHop/getDeepState` 之一取状态（7098–7115）；状态为 None 记丢包并 flush（7117–7121）；`_apply_frame_stack`、`_temporal_apply` 改写状态（7124–7126）；有 `q_global` 时每 50 个 decision 重建/复用 `build_global_state` 缓存（7130–7159）；`_append_state_log`（7162）；若 linkedGT 即目的地：按 `distanceRew`∈{4,5,其他} 组到达奖励、存 terminal 转移（含 global_state/next_action_mask）、path-credit 轨迹补最后一跳并 push 'delivered'、`TrainThis` 时触发一次 `train`（7227，行内 FIXME 注释质疑此处训练）、按需画路径后返回 0（7165–7233）；否则 `getNextHop` 选动作（7236）；有 prevSat 时按 `distanceRew`∈{1..5} 选 `getDistanceReward/V2/V3/V4(或 _SIM_POTENTIAL_SHAPING 时 Potential)/V5` 加 `again` 惩罚与 `getQueueReward` 得奖励（7239–7272），存（或 n 步存）上一跳转移、path-credit 记 hop、`step % nTrain == 0` 时 `train`（7275–7297）；`ddqn` 时 `alignQTarget(hardUpdate)`（7304–7305）；回写 `block.oldState/oldAction/oldGlobalState`（7308–7311）；返回 nextHop（7313）。
  - `alignEpsilon(step, sat)`(7315)：与 `QLearning.alignEpsilon` 同公式的指数 ε 衰减，追加到 `self.epsilon` 并返回 ε（7324–7327）。
  - `alignQTarget(hardUpdate=True)`(7329)：hard 模式每 `updateF` 次调用整体拷贝 qNetwork→qTarget 并计 `_target_sync_count`（7346–7352）；否则按 `tau` 软更新（7354–7356）。（注：docstring 首句称"此函数现在未使用"，但 7305 行每决策都调用——docstring 与实现不符，FACT。）
  - `createModel`(7358)：按路由模式建网络——`ddqn_cvar` 走 `build_quantile_model`（7359–7363），`ddqn_csr` 走 `build_csr_model`（7364–7373），c4–c7 走 `_create_graph_model`（7376–7377），默认建 `Dense(hiddenUnits,relu)×2 + Dense(actionSize,linear)` 的 Sequential 并以 `Adam(lr=learningRate[, clipnorm=Clipnorm])`、mse 编译（7382–7388）。
  - `_create_graph_model(state_mode)`(7390)：Functional 建模——`Input(stateSize)`→`GraphMessagePassingReadout`（c4/c7 用 gat、c5/c6 用 mpnn；c6/c7 传 reliability_aware/aoi_gate/action_feat_dim，7397–7414）→两个 `Dense(hiddenUnits,relu)`（7415–7418）→RAAC 时 `Dense(1)→Reshape((actionSize,))` 共享动作分（7419–7421），否则 `Dense(actionSize)`（7423）→ mse 编译返回（7424–7427）。
  - `_build_fast_train_fn`(7429)：构建一次性编译的 `tf.function` 训练步（SIM_FAST_TRAIN）：输入签名含 states/actions/rewards/nextStates/not_done/next_action_mask（7442–7449），内部算 masked target（无效动作置 -1e9；`_SIM_TRUE_DDQN` 且 ddqn 时用在线网 argmax、目标网取值，否则 masked target max），`rewards + not_done·γ^N·future` 为目标，MSE/chosen-action/A 反传并 `apply_gradients`（7451–7478）。
  - `_fast_train_step_call(...)`(7480)：模型对象被换（id 变化）时重建编译函数再执行一次训练步（7482–7496）。
  - `train(sat, earth)`(7498)：批量训练入口——cvar/csr 模式分别委托 `train_quantile_ddqn`/`train_csr_ddqn`（7499–7506）；回放样本 < 3·batchS 直接返回 -1（7507–7508）；取批（critic 模式用 `getBatchWithAux`+`getGlobalArraysFromBatch` 对齐 global state，7512–7519）；`_safe_next_action_mask` 处理掩码（7530）；满足 `_SIM_FAST_TRAIN` 等条件走编译步否则 eager 算 expectedRewards（true-DDQN 或 target-DQN  masked 自举，γ 取 `γ^_SIM_NSTEP`，7535–7552）；`stopLoss` 达标时置全局 `TrainThis=False` 并返回（7558–7571）；eager 路径 predict-then-targeted-update 只改被选用动作的目标值（7588–7590）；有 critic 且半数以上样本 valid 时训练 q_global 并按 `_SIM_DISTILL_LAMBDA` 在选用动作处混入蒸馏目标（7597–7633）；编译/普通路径各执行一步训练并计 `earth._fast_train_steps/_eager_train_steps`（7635–7642）；`_w_version` 自增（7643）；记 loss/trains（7644–7645）；每 `updateF` 次训练同步 `q_global_target`（7648–7650）；每 100 次训练打印收敛监控（ε、平均 loss、Q 方差、动作熵；`_SIM_LOG_LEVEL>=1` 时附分位数/动作计数到 `earth.train_log`，c4–c7 附编码器范数与 diagnostics 到 `earth.encoder_log`，7653–7699）；`_SIM_BUFFER_SNAPSHOT_INTERVAL>0` 时定期把回放存 npz（7703–7718）；`_SIM_PATH_CREDIT` 时按 `EVERY_K` 调 `pc_mixer.train_step` 并记 `earth.pc_log`（7723–7766）。
- 输入/输出：`getNextHop` 返回 `([ID, lon°, lat°], actIndex)` 或异常时 `-1`；`makeDeepAction` 返回 nextHop 三元组或 0（到达/丢包）；`train` 返回训练步 loss 转 float 前的控制流结果（cvar/csr 委托返回值、-1 或 None，FACT：主路径无显式 return 值，仅副作用）。
- 依赖关系：
  - 构造方：`initialize()` 的 8062 行（`earth.DDQNA`，共享 agent）与 8070 行（`sat.DDQNA`，per-satellite agent，传 `sat.ID`）。
  - 决策入口被调方：`makeDeepAction` 被 `Satellite.receiveBlock`(2017) 的 2073/2075/2080/2082 行与 `Earth.updateSatelliteProcessesRL`(4504) 的 4567–4721 行多处调用。
  - 内部调用同文件函数：`getDeepLinkedSats`(9381)、各 `getDeepState*`（9547–10192）、`getQueues`(9050)、`getSlantRange`(10261)、`getDistanceReward` 系列（10296–10383）、`getQueueReward`(10269)、`visKFlatDim`(9878)、`graphStateDim/raacGraphStateDim`(5901/5913)、`_append_state_log`(918)、`_sample_raac_reliability`(968)、`_append_decision_log`(1006)、`_append_reward_log`(1035)、`_pc_flush_lost`(1066)、`_append_packet_fate_log`(1109)、`_set_distance_diag`(1196)、`_temporal_apply`(9469)、`_apply_frame_stack`(9499)、`_bp_backlog_counts`(521)、`_safe_next_action_mask`(404)、`_masked_target_dqn_values`(425)、`_masked_double_dqn_actions`(434)、`plotShortestPath`(8968)、`_shadow_record`(5849)、`_np_mlp_forward`(5833)。
  - 跨文件被调方：`routing_hooks`（`LocalStatsHook/build_default_hooks`，6414）、`routing_mappo`（`BackpressurePrior/build_centralized_critic_per_action/build_global_state`，6268/6506/7133）、`routing_path_credit.build_path_credit_mixer`(6540)、`routing_multistep.lambda_return_transitions`(7052)、`temporal_encoder`(6253/6611)、`runtime_effect_receipt`（`new_checkpoint_receipt/attempt_checkpoint_load`，6619–6625，经同文件 30–31 行 import）。
  - **缺失依赖（FACT）**：`legacy.routing_csr`（6314/6361/6662/6858/7365/7504）、`legacy.routing_tailguard`（6423/7360/7500/12322）、`legacy.routing_mcp_hash`（6417）三模块在工作区不存在（无 `CODE/legacy/` 目录，`find` 全工作区无匹配文件）；均为方法内延迟 import，且模块级 474–479 行在 `SIM_CSR_MODE=csr` 时直接 `raise RuntimeError("…legacy.routing_csr, which is not present in retained CODE…")`。因此 csr/cvar/mcp_hash 三条路由路径在当前工作区代码下不可执行到 import 成功 (FACT：import 目标文件不存在；INFERENCE：运行时触发这些分支会 ImportError——csr 分支在模块 import 阶段已被 474–479 行的 guard 阻断，cvar/mcp_hash 分支无对应模块级 guard，会在 `__init__`/`train`/`createModel` 内延迟 import 时失败)。
  - `_ms_flush_lost` 被同文件模块级 `_pc_flush_lost` 在 1083 行调用。
  - 测试佐证：`CODE/tests/test_raac_tensorflow_contract.py:89-110` 直接调用 `DDQNAgent._build_fast_train_fn` 验证 masked target/double-DQN 语义；`CODE/tests/test_runtime_effect_receipt.py:122-128` 断言 `_create_graph_model`/`_build_fast_train_fn` 源码含 `shared_action_score`/`Reshape`/`masked_target`/`masked_online`；`CODE/tests/test_state_vis_k.py:116` 注释引用 `DDQNAgent.__init__` 的状态维度契约。

---

#### `class ExperienceReplay` — CODE/SimulationRL.py:7770

- 定位：CODE/SimulationRL.py:7770
- 职责：DDQN 经验回放缓冲：FIFO deque 存 (state, action, reward, nextState, terminated)，并平行存 global state 对与下一状态动作掩码 (FACT，docstring 7772–7782)。
- 关键状态/结构：`self.buffer = deque(maxlen=maxlen)`（7783）；`self.global_buffer`（存 `(g_state, g_next_state)` 或 None，7786）；`self.next_action_mask_buffer`（7787）；三者同 maxlen、同步 FIFO 淘汰。
- 关键流程/方法：
  - `__init__(maxlen=100)`(7771) 建三条 deque。
  - `store(state, action, reward, nextState, terminated, global_state=None, next_global_state=None, next_action_mask=None)`(7789)：追加转移；`global_state` 非 None 时存 float32 的 (g, g')（g' 缺省取 g），否则存 None（7798–7802）；`next_action_mask` 缺省为全 True，形状必须为 (4,) 否则 `raise ValueError`（7803–7806）。
  - `getBatch(batchSize)`(7808)：`random.sample(self.buffer, batchSize)` 随机取批（只回本地转移）。
  - `getBatchWithGlobal(batchSize)`(7814)：同一组随机下标取本地批与 global 批并返回二者（下标对齐）。
  - `getBatchWithAux(batchSize)`(7825)：同一组随机下标取本地批、global 批与掩码批（掩码缺失补全 True），返回三元组。
  - `getArraysFromBatch(batch)`(7835)：把批按字段拆成 float32 states/rewards、int64 actions、float32 nextStates、bool dones 五个数组。
  - `getGlobalArraysFromBatch(glob_batch)`(7849)：把 global 批转成 (gs, gns, valid_mask)，None 项补零向量（维度 `GLOBAL_STATE_DIM`，同文件 547 行=44）并标 invalid。
  - `buffeSize`(7870, @property)：返回 `len(self.buffer)`。
- 输入/输出：`store` 无返回；各 get 方法返回 list 或 numpy 数组元组。
- 依赖关系：被 `DDQNAgent.__init__` 在 6444 行实例化；`store` 被 `DDQNAgent.getNextHop`（6806）、`makeDeepAction`（7181/7191/7197/7278）、`_ms_store`（7004/7010）、`_ms_flush_lost`（7030）、`_tdl_flush`（7061）调用；`getBatchWithAux/getArraysFromBatch/getGlobalArraysFromBatch` 被 `DDQNAgent.train`（7513–7518）调用；`buffer` 属性被 `train` 的快照逻辑直接读取（7708–7714）；`getBatch` 调用方未确认（范围内未见调用）。测试佐证：`CODE/tests/test_runtime_effect_receipt.py:359-368` 验证 `store`/`getBatchWithAux` 的掩码下标对齐。
