# 片段 n2：新平台 learning.py + receipt.py

### 文件 `CODE/leo_sim/learning.py`（实测 825 行）

模块级说明：

- 模块 docstring（learning.py:1-14）声明：本模块定义学习合同 C1/C3/C4/C5/C6/C7 与 canonical Double-DQN target 数学；信息边界为「每个合同只观测当前卫星自己直接测量的状态 + 实际到达且未过期的本地控制缓存」，C1 进一步限制到 1-hop origins，C3–C7 共享同一信息集（vis_k 缓存）、只在表示/聚合与 AoI 处理上不同；无可用 TensorFlow 时学习运行 fail closed（LearningUnavailable）。(FACT，源自 docstring)
- imports（learning.py:15-25）：`__future__.annotations`、`importlib.util`(17)、`hashlib`(18)、`json`(19)、`math`(20)、`os`(21)、`collections.deque`(22)、`pathlib.Path`(23)、`numpy as np`(25)。其中 `importlib.util` 在本文件内除 import 行外无任何引用（FACT，全文件 grep 仅命中行 17）。
- TensorFlow 可选导入（learning.py:27-30）：`try: import tensorflow as tf`，`ImportError` 时 `tf = None`；全模块的 fail-closed 语义都建立在该变量上。
- 全局常量：
  - `CONTRACTS`(32) = `("C1", "C3", "C4", "C5", "C6", "C7", "GAT", "MPNN")`。
  - `ORIGIN_FEATURES`(36) = 4；注释（34-35）给出逐 origin 特征块布局 `[isl_queue_ratio, access_load_ratio, n_visible_cells_norm, aoi_norm]`。
  - `DEST_FEATURES`(42) = 3；注释（37-41）给出布局 `[dst_bearing_sin, dst_bearing_cos, dst_dist_norm]`，bearing 为当前星 ENU 切平面内方位角（N=0、E=90°），距离为星下点到目的地大圆距离、按 20000 km 归一。`_DEST_DIST_NORM_KM`(43) = 20000.0；`_EARTH_R_KM`(44) = 6371.0。
  - 合同维度常量（45-53）：`C3_DIM = 4 + ORIGIN_FEATURES`(45)、`C4_DIM = 4 + ORIGIN_FEATURES`(46)、`C5_DIM = 4 + ORIGIN_FEATURES + 1`(47)、`C6_MAX_HOPS = 4`(48)、`C6_DIM = 4 + 4*ORIGIN_FEATURES`(49)、`C7_MAX_ENTRIES = 5`(50)、`C7_DIM = 4 + 5*(ORIGIN_FEATURES+1)`(51)、`C1_MAX_NEIGHBORS = 4`(52)、`C1_DIM = 4 + 4*ORIGIN_FEATURES`(53)。
  - `CONTRACT_DIMS`(56-63)：每个合同维度 = 上述 DIM + `DEST_FEATURES`，即 C1=23、C3=11、C4=11、C5=12、C6=23、C7=32（对 45-53 与 56-63 行做算术，FACT）。
  - `ACTIONS`(64) = `("deliver", "N", "S", "E", "W")`。
  - 图合同常量：注释（66-68）声明 GAT/MPNN 是新名字、不复用 V1 的 C4/C5 语义（V2 的 C4/C5 是缓存聚合规则）；`GRAPH_MAX_NODES = 32`(69)、`GRAPH_NODE_FEAT_DIM = 15`(70)、`GRAPH_DIRS = ("N", "S", "E", "W")`(71)、`GRAPH_CONTRACTS = ("GAT", "MPNN")`(72)。
  - `GRAPH_CONTRACT_DIMS`(84) = 每个图合同调 `graph_state_dim()`；`CONTRACT_DIMS` 在行 85-86 合并图合同维度。默认参数下 GAT/MPNN 观测宽度 = 32*15 + 32*32 + 4*32 + 4 + 3 = 1639（对 78-81 行做算术，FACT）。
- 环境变量：模块级无。`LEO_FAST_TRAIN` 在 `TensorflowDDQN.__init__`（learning.py:334）读取，值不在 `("0", "false", "no")` 时启用 tf.function 编译训练路径；注释（331-333）声称该路径与 eager 路径 bit 等价、快约 5-6 倍（FACT：注释内容如此；本片段不对该等价性做验证）。

学习合同定义位置与各自观测内容（本文件范围内汇总）：

- 合同名字集合定义于 learning.py:32（`CONTRACTS`）；配置侧合法值集合定义于 CODE/leo_sim/config.py:169（`VALID_CONTRACTS = {"C1", "C3", "C4", "C5", "C6", "C7", "GAT", "MPNN"}`），config.py:469-470 对 `routing.contract` 不在集合内抛 `ConfigError`；config.py:130 注释标注该键为 "C1|C3|C4|C5|C6|C7 (observation contracts)"；默认值 `"C3"` 在 config.py:241-242。learning 超参默认值（algorithm/mode/seed/obs_hops/checkpoint_path/checkpoint_sha256/gamma/lr/batch_size/replay_size/target_update_interval/reward/epsilon_*）在 config.py:243-259。
- 各合同观测内容由 `build_observation`（learning.py:724）各分支与 `build_graph_observation`（learning.py:663）决定，逐合同内容见下文 `build_observation` 条目。信息集（合同能看到哪些缓存条目）由 `information_set`（learning.py:593）决定：C1 只见 `{本星} ∪ 1-hop 邻居`（603-605）；C3–C7 与 GAT/MPNN 见同一集合——全部有效已到达条目，可选按 `obs_hops` 限制条目跳数（606-609）。测试佐证：test_learning.py:29-31 断言 C3–C7 信息集相同；test_learning.py:39 断言 C1 只见 1-hop origin；test_learning.py:120-128 断言 obs_hops 过滤生效。

#### `def graph_state_dim(max_nodes=GRAPH_MAX_NODES, node_feat_dim=GRAPH_NODE_FEAT_DIM) -> int` — CODE/leo_sim/learning.py:75

工具函数（压缩六字段）：定位 learning.py:75-81。职责 (FACT)：返回图合同扁平观测的宽度 = `max_nodes*node_feat_dim + max_nodes*max_nodes + len(GRAPH_DIRS)*max_nodes + 4 + DEST_FEATURES`（78-81；注释在行 81 标注末尾为 own-state tail + destination features）。输入两个 int（默认取 GRAPH_MAX_NODES=32、GRAPH_NODE_FEAT_DIM=15）；输出 int，默认参数下为 1639。调用方：learning.py:84（构造 `GRAPH_CONTRACT_DIMS`）、learning.py:718（`build_graph_observation` 的宽度断言）；CODE/ 内无外部调用方（全 CODE/ grep 仅命中本文件，FACT）。

#### `class LearningUnavailable(RuntimeError)` — CODE/leo_sim/learning.py:89

- 定位：learning.py:89-90。
- 职责 (FACT，源自 docstring 行 90)：请求学习执行但无真实 TensorFlow 运行时时抛出的异常类型。
- 关键状态/结构：无自定义状态、无自定义方法，空子类。
- 关键流程/方法：无方法。
- 输入/输出：构造接收异常消息字符串。
- 依赖关系：抛出点为 learning.py:96（`require_tensorflow`）、306/309/315（`TensorflowDDQN.__init__` 的 checkpoint 检查）、512（`save_and_verify` 验证失败）；kernel.py:54 将其重导出为 `kernel.LearningUnavailable`；捕获方为 __main__.py:251-253（打印 "RUN REFUSED (fail closed)" 并返回退出码 3）；测试 test_learning.py:196、210 断言无 TF 时经 `kernel.run_simulation` 抛出。

#### `def require_tensorflow()` — CODE/leo_sim/learning.py:93

工具函数（压缩六字段）：定位 learning.py:93-99。职责 (FACT)：`tf is None` 时抛 `LearningUnavailable`（消息中含 "learning runs fail closed"，96-98），否则返回 `tf` 模块对象（99）；docstring（94）称之为 "Fail closed unless a genuinely importable TensorFlow exists"。输入无；输出 tensorflow 模块或抛异常。调用方：learning.py:289（`TensorflowDDQN.__init__`）、kernel.py:741（`Kernel.learning_gate`，当 `routing.learning_enabled` 或 `learning.algorithm != "none"` 时调用，kernel.py:738-741）。

#### `class V2GraphEncoder` — CODE/leo_sim/learning.py:102

- 定位：learning.py:102-269。
- 职责 (FACT，源自 docstring 103-112 与 `call` 实现)：GAT/MPNN 图编码器 Keras 层：把 `build_graph_observation` 产出的扁平观测解析为节点特征 `[MAX_N,15]`、邻接 `[MAX_N,MAX_N]`（`adj[dst,src]=1` 表示真实 ISL 边）、readout 掩码 `[4,MAX_N]`、own-state tail `[4]`，运行 GAT（多头注意力）或 MPNN（均值消息传递）层，返回四个方向 readout 嵌入与 own-state tail 的拼接，供共享 dense Q 头使用。
- 关键状态/结构：类定义行 102 的基类为条件表达式 `tf.keras.layers.Layer if tf is not None else object`（FACT）——无 TF 主机上该类退化为 `object` 子类仍可被定义；docstring（114-117）声明本类在 import 时引用 `tf`，因此模块应在 `require_tensorflow()` 成功后使用（FACT：docstring 内容；同时测试 test_learning.py:7 无条件 import 本模块、并在 188-211 行验证无 TF 主机上 fail closed，FACT）。实例状态：`enc_mode/n_nodes/f_dim/h_dim/layers/heads`（128-133）、`node_in` Dense 层（134-135）、可训练权重 `dir_default`（形状 (4, h_dim)，zeros 初始化，136-138）、`build` 中按模式创建的逐层权重（见下）。
- 关键流程/方法：
  - `__init__(self, enc_mode, n_nodes, f_dim, h_dim, layers, heads, **kwargs)`(120)：校验 `enc_mode ∈ {"gat","mpnn"}`（123-125）、GAT 时 `h_dim % heads == 0`（126-127），存配置并创建 `node_in` 与 `dir_default`。
  - `get_config(self)`(140)：返回含六个超参的序列化配置 dict（141-150）。
  - `from_config(cls, config)`(152，@classmethod)：从配置 dict 重建实例（153-158）。
  - `build(self, input_shape)`(160)：GAT 模式创建每层权重 `gat_W`（heads×h_dim×hd，glorot_uniform，163-168）、`gat_a_src`（169-174）、`gat_a_dst`（175-180）、`gat_self_W`（h_dim×h_dim，181-186）、`gat_bias`（zeros，187-191）；MPNN 模式创建 `msg_W`（193-198）、`self_W`（199-204）、`mpnn_bias`（205-209）；末尾调 `super().build`（210）。
  - `_parse(self, flat)`(212)：把扁平输入 reshape 成 node/adj/readout/tail 四段（214-219）；取节点特征张量索引 7 的切片 `node[:, :, 7:8]`（即 `_graph_node_features` 写入的 valid flag，learning.py:655）作为 `node_mask`，用它屏蔽 adj 的行列与 readout 的列（220-222）；返回五元组。
  - `_gat_layer(self, h, adj, node_mask, l)`(225)：单层 GAT——`einsum` 把节点嵌入投影到多头（227）、分别与 `gat_a_src`/`gat_a_dst` 打分（228-231）、LeakyReLU(alpha=0.2) 得注意力 logits（232-233）、按邻接掩码把无边位置压到 -1e9 后 softmax 并按行归一（234-238）、聚合消息经转置 reshape 后与自变换 `gat_self_W`、偏置相加过 ReLU（239-243），输出乘 `node_mask`（244）。
  - `_mpnn_layer(self, h, adj, node_mask, l)`(246)：单层 MPNN——源消息线性变换（247）、按度数归一的邻接均值聚合（248-249）、自变换+偏置过 ReLU（250-251），输出乘 `node_mask`（252）。
  - `call(self, flat, training=False)`(254)：`_parse` → `node_in` 嵌入并乘掩码（255-256）→ 按模式堆叠 `self.layers` 层（257-261）→ 按 readout 掩码做四方向均值 readout，某方向无节点时用可训练的 `dir_default` 兜底（262-267）→ 拼接 `4*h_dim` 方向嵌入与 tail 返回（268-269）。
- 输入/输出：输入扁平张量 `[batch, graph_state_dim()]`；输出 `[batch, 4*h_dim + tail_len]`（tail_len 由输入剩余段决定，图观测下为 4+3=7，见 build_graph_observation 708-715）。
- 依赖关系：被 `TensorflowDDQN._network` 实例化（learning.py:343，固定 h_dim=64、layers=1、heads=2）；经 `_graph_custom_objects`（272-273）注册进 `keras.models.load_model` 的 `custom_objects`（learning.py:312、494）；CODE/ 内无其他直接调用方。

#### `def _graph_custom_objects()` — CODE/leo_sim/learning.py:272

工具函数（压缩六字段）：定位 learning.py:272-273。职责 (FACT)：返回 `{"V2GraphEncoder": V2GraphEncoder}`。输入无；输出单键 dict。该 dict 被传给 `keras.models.load_model` 的 `custom_objects` 参数（learning.py:312、494）；其用途是让 Keras 反序列化时识别自定义层类 (INFERENCE——代码内无注释说明，由 Keras API 语义推定)。调用方：learning.py:312、494；无外部调用方。

#### `class TensorflowDDQN` — CODE/leo_sim/learning.py:276

- 定位：learning.py:276-529。
- 职责 (FACT，源自 docstring 277-284)：V2 hop-by-hop 运行时使用的共享策略 Double-DQN；一个模型被所有卫星共享，每次决策只消费该卫星的本地观测与合法掩码；合法掩码由 kernel 而非网络构造，因此探索不会选出隐藏全局、成环、满队列或几何上不可用的动作（docstring 陈述的设计约束）。
- 关键状态/结构：`contract`、`input_dim = CONTRACT_DIMS[contract]`（295-296）、`cfg`、`seed`、`rng = np.random.default_rng(seed)`（299）、`replay = deque(maxlen=cfg["replay_size"])`（300）、`mode = cfg["mode"]`（301）、`online`/`target` 两个网络、`optimizer = Adam(lr=cfg["lr"])`（325-326）、计数器 `decisions/transitions/train_steps/last_loss`（327-330）、`loaded_checkpoint`/`loaded_checkpoint_sha256`（317-318 或 321-322）、`_fast_enabled`/`_fast_train_fn`/`_fast_train_net_id`/`_fast_train_tgt_id`（334-337）。
- 关键流程/方法：
  - `__init__(self, contract, cfg, seed)`(286)：合同不在 `CONTRACT_DIMS` 抛 ValueError（287-288）；调 `require_tensorflow()`（289）；尝试 `enable_op_determinism()`，异常被静默吞掉（290-293）；`set_random_seed(seed)`（294）；若 `cfg["checkpoint_path"]` 非空：文件不存在抛 LearningUnavailable（303-306）、文件 SHA-256 与 `cfg["checkpoint_sha256"]` 不符抛 LearningUnavailable（307-310）、`load_model` 后输入形状须为 `(None, input_dim)`、输出形状须为 `(None, len(ACTIONS))`，不符抛 LearningUnavailable（311-316）；无 checkpoint 时用 `_network()` 新建（319-322）；`target` 网络新建并复制 `online` 权重（323-324）；建 Adam 优化器（325-326）；读 `LEO_FAST_TRAIN` 环境变量（334）。
  - `_network(self)`(339)：图合同建 `Input → V2GraphEncoder(enc_mode, n_nodes=32, f_dim=15, h_dim=64, layers=1, heads=2) → Dense(64, relu) → Dense(5, linear)` 的 Model（341-350）；其他合同建 `Input → Dense(64,relu) → Dense(64,relu) → Dense(5,linear)` 的 Sequential（351-356）。
  - `epsilon(self, now)`(358)：`mode == "eval"` 返回 0.0（359-360）；否则返回 `epsilon_end + (epsilon_start - epsilon_end) * exp(-max(0, now)/epsilon_decay_s)`（361-364）。
  - `_mask_array(mask)`(366，@staticmethod)：按 `ACTIONS` 顺序把 mask dict 转成 bool np 数组，缺键按 False（367-368）。
  - `choose(self, observation, mask, now)`(370)：合法动作集为空抛 ValueError（371-374）；以 `epsilon(now)` 概率在合法下标中均匀随机（376-377），否则 online 网络前向并在合法下标上取 argmax（379-380）；`decisions += 1`（381）；返回动作名字符串（382）。
  - `remember(self, state, action, reward, next_state, next_mask, done)`(384)：未知动作名抛 ValueError（386-387）；把 transition（state 数组、动作下标、reward、next_state 数组、next_mask 数组、done）追加进 `replay`（388-393）；`transitions += 1`（394）；`mode == "train"` 且 `len(replay) >= batch_size` 时调 `_train_once()`（395-396）。
  - `_train_once(self)`(398)：无放回抽样一个 batch（399-407）；fast 路径（408-428）：首次或 online/target 对象 id 变化时重建 tf.function（409-415），调用编译好的训练步（416-423），记录 loss、`train_steps += 1`，每逢 `target_update_interval` 同步 target 权重（424-427）；eager 路径（429-444）：online/target 前向、`ddqn_targets` 算目标值、GradientTape 内算 MSE loss、`apply_gradients`、同样按间隔同步 target。
  - `_build_fast_train_fn(self)`(446)：构造并返回一个 `@tf.function(input_signature=..., reduce_retracing=True)` 编译的训练步（453-462）；步内逻辑：online/target 前向（464-465）、整行无合法动作时把掩码退化为全 1 的 `safe_mask`（466-470）、掩码后 argmax 得 a*（471-473）、`not_done` 为假时 bootstrap 置 0（474-475）、`expected = stop_gradient(rewards + gamma * bootstrap)`（476）、tape 内算 MSE 并 `apply_gradients`（477-482）、返回 loss（483）。
  - `save_and_verify(self, directory)`(487)：把 `online` 存为 `directory/online.keras`（488-491）；算文件 SHA-256（492）；重新 `load_model`（493-494）；用 `np.linspace(-0.5, 0.5, input_dim)` 探针比较保存前后输出，`rtol=0.0, atol=1e-7`（495-498）；写 `metadata.json`（含 `schema="leo-sim-ddqn/v1"`、checkpoint 文件名/SHA-256/`checkpoint_verified`/探针最大绝对误差，499-510）；验证未通过抛 LearningUnavailable（511-512）；返回 metadata dict（513）。
  - `diagnostics(self)`(515)：返回含 algorithm/contract/mode/loaded_checkpoint(_sha256)/actions/decisions/transitions/train_steps/replay_size/last_loss/seed 的 dict（516-529）。
- 输入/输出：构造吃合同名、learning 配置 dict（键来自 config.py:243-259 的 learning 段）、seed；`choose` 吃观测向量 + mask dict + 仿真时刻，返回 `ACTIONS` 中的字符串；`remember` 吃一条 transition；`save_and_verify` 写盘并返回 metadata dict。
- 依赖关系：被 `Kernel.__init__` 在 `learning.algorithm == "ddqn"` 时实例化（kernel.py:603-610）；kernel 经 `_learning_action` 调 `choose`（kernel.py:1376）、经 `_finish_learning_transition` 调 `remember`（kernel.py:1365-1368）、在 `run()` 收尾调 `diagnostics()` 与 `save_and_verify()`（kernel.py:1612-1615）并把 decisions/transitions/train_steps 写回机制计数器（kernel.py:1616-1618）；测试 test_learning.py:215 直接构造。内部调用：`require_tensorflow`(289)、`_graph_custom_objects`(312, 494)、`V2GraphEncoder`(343)、`ddqn_targets`(431)。

#### `def own_state(slots_used, slots_cap, isl_queue_bits, isl_queue_cap, n_visible, n_cells) -> np.ndarray` — CODE/leo_sim/learning.py:532

工具函数（压缩六字段）：定位 learning.py:532-541。职责 (FACT)：构造 4 维本星自有状态向量 `[slots_used/max(1,slots_cap), 各方向 ISL 队列比特总和/max(1, isl_queue_cap*方向数), n_visible/max(1,n_cells), 1.0]`（534-541）；第 4 维注释（540）为 "bias/valid flag marking real own measurement"。输入 6 个参数（4 个标量 + 方向→比特 dict + 队列上限）；输出 float64 np.ndarray，shape (4,)。调用方：kernel.py:1340（`Kernel._learning_observation`）、test_learning.py:26、test_review_round4.py:333。

#### `def _origin_features(entry, now, isl_queue_cap) -> np.ndarray` — CODE/leo_sim/learning.py:544

工具函数（压缩六字段）：定位 learning.py:544-556。职责 (FACT)：把一条缓存 entry 编成 4 维归一化特征 `[entry 的 isl_queue_bits 总和/max(1, isl_queue_cap*4), access_slots_used/max(1,access_slots_cap), min(1, 可见小区数/10), min(1, max(0,entry.aoi(now))/max(entry.ttl_s,1e-9))]`（545-556）；entry 缺字段时用 `payload.get(..., 默认)` 兜底（546-549）。输入 `CacheEntry`、`now`、`isl_queue_cap`；输出 float64 np.ndarray，shape (4,)。调用方：learning.py:734（`build_observation` 全合同）、770（C5 分支）、785（C7 分支）；无外部调用方。entry 的 `payload/aoi()/ttl_s/hops` 字段语义见 control.py:37-54（CacheEntry）。

#### `def destination_features(sat_lat_deg, sat_lon_deg, dst_lat_deg, dst_lon_deg) -> np.ndarray` — CODE/leo_sim/learning.py:559

工具函数（压缩六字段）：定位 learning.py:559-590。职责 (FACT，docstring 行 561 + 实现)：3 维目的地条件特征 `[sin(bearing), cos(bearing), min(1, 大圆距离km/20000)]`（586-590）；bearing 计算：经纬度转弧度后求两地地心笛卡尔坐标差 (dx,dy,dz)（568-573），投影到卫星星下点 ENU 的 east/north 分量（574-577），`atan2(east, north)` 得方位角（578）；距离用 haversine 公式（581-585）。输入两对经纬度（度）；输出 float64 np.ndarray，shape (3,)。调用方：kernel.py:1350（`Kernel._learning_observation`，仅当目的地小区存在时计算）、test_learning.py:111。

#### `def information_set(contract, sat, cache, now, topo, obs_hops=None) -> dict` — CODE/leo_sim/learning.py:593

- 定位：learning.py:593-610。
- 职责 (FACT，docstring 595-601 + 实现)：返回一个合同恰好允许看到的缓存条目 dict。
- 关键状态/结构：无持有状态；输入 `cache` 需提供 `valid_entries(now)`（control.py:70-77 的 `LocalCache.valid_entries`，只返回生成≤到达≤now≤生成+ttl 的条目）。
- 关键流程/方法：`entries = cache.valid_entries(now)`（602）；C1 → `allowed = {sat} | set(topo.get(sat, {}).values())`，只保留 origin ∈ allowed 的条目（603-605）；C3/C4/C5/C6/C7/GAT/MPNN → `obs_hops is None` 返回全部条目副本，否则只保留 `e.hops <= obs_hops` 的条目（606-609）；未知合同抛 ValueError（610）。
- 输入/输出：输入合同名、卫星 id、缓存对象、时刻、拓扑 dict、可选跳数上限；输出 `{origin: CacheEntry}` dict。
- 依赖关系：调用方 learning.py:676（`build_graph_observation`）、732（`build_observation`）；测试 test_learning.py:31/39/47/124、test_review_round4.py:335。被调方：`LocalCache.valid_entries`（control.py:70）。

#### `def _bfs_first_dirs(sat, topo) -> dict[int, str]` — CODE/leo_sim/learning.py:613

工具函数（压缩六字段）：定位 learning.py:613-634。职责 (FACT，docstring 614-619 + 实现)：从 `sat` 出发对静态 ISL 邻接做 BFS，给每个可达节点标注「从根出发第一跳的方向」，返回 `{node: first_dir}`；根节点自身不出现在结果中（618-619）；docstring 称此为 "V1-style directional readout"（617）。实现：初始 frontier 为按方向名排序的直接邻居（621-625），此后逐层扩展、子节点继承其父节点的 first_dir（626-633）。输入卫星 id 与 topo dict；输出 `{int: str}` dict。调用方：learning.py:678（`build_graph_observation`）；无外部调用方。

#### `def _graph_node_features(origin, entry, root, first_dir, topo, isl_queue_cap, root_pos=(0,0,0)) -> np.ndarray` — CODE/leo_sim/learning.py:637

工具函数（压缩六字段）：定位 learning.py:637-660。职责 (FACT，docstring 640 + 实现)：为一个子图节点构造 15 维特征向量——`feats[0:4]` = 四方向 ISL 队列比特各除以 `max(1, isl_queue_cap)` 并截断到 1（650-651）；`feats[4]` = `min(1, hops/4)`（652）；`feats[5]` = `min(1, 节点度数/4)`，度数按 topo 中邻居值非 None 的项数计算（648、653）；`feats[6]` = 是否根节点的 0/1（654）；`feats[7]` = 恒 1.0 的 valid 节点标志，注释（655）说明 padding 行保持 0；`feats[8:12]` = `first_dir` 的 one-hot（656-657）；`feats[12:15]` = 节点 payload 的 `position` 与 `root_pos` 之差除以 7000.0（658-659；该归一化常数在代码中无注释解释，FACT）。`entry is None` 时各 payload 字段取默认值（641-647）。输入 origin id、可空 entry、根 id、可空 first_dir、topo、isl_queue_cap、root_pos；输出 float64 np.ndarray，shape (15,)。调用方：learning.py:691（`build_graph_observation`）；无外部调用方。

#### `def build_graph_observation(contract, sat, cache, now, topo, own, isl_queue_cap=256_000_000, obs_hops=None, dst_feats=None) -> np.ndarray` — CODE/leo_sim/learning.py:663

- 定位：learning.py:663-721。
- 职责 (FACT，docstring 668-675 + 实现)：为 GAT/MPNN 图合同构造定宽扁平 k-hop 子图观测；布局 = 节点特征 `[MAX_N,15]` + 有向邻接 `[MAX_N,MAX_N]` + 方向 readout 掩码 `[4,MAX_N]` + own-state tail `[4]`（+ 目的地特征）；docstring 声明节点为实际到达的有效缓存 origins 加根节点、节点特征只来自已到达 ControlPacket 携带的 payload 字段（无未来几何、无隐藏全局队列）。
- 关键状态/结构：无持有状态；内部构造 `feats (32,15)`、`adj (32,32)`、`readout (4,32)` 三个零矩阵与 tail 向量。
- 关键流程/方法：取 `information_set`（676）与 `_bfs_first_dirs`（678）；节点序列 = 根 + 排序后 origins 截断到前 31 个（680-683；`overflow` 计数于 682 计算但未再使用，FACT）；根位置取根 entry payload 的 `position`（684-686）；逐节点填 `_graph_node_features`（688-693）；按 topo 填邻接，`adj[dst, src] = 1` 当节点间有 ISL 边且非自环（695-700）；按 first_dir 填 readout one-hot（702-706）；`own` 必须 reshape 后为 4 维否则 ValueError（708-710）；`dst_feats` 为 None 时补 3 维零、维度不符抛 ValueError（711-714）；拼接后总宽度必须等于 `graph_state_dim()`，不等抛 AssertionError（716-720）。
- 输入/输出：输入合同名、卫星 id、缓存、时刻、topo、own 向量、队列上限、可选 obs_hops、可选目的地特征；输出 float64 np.ndarray，shape (1639,)（默认常量下）。
- 依赖关系：调用方仅 learning.py:729（`build_observation` 的图合同分支）；内部调 `information_set`(676)、`_bfs_first_dirs`(678)、`_graph_node_features`(691)、`graph_state_dim`(718)。

#### `def build_observation(contract, sat, cache, now, topo, own, isl_queue_cap=256_000_000, obs_hops=None, dst_feats=None) -> np.ndarray` — CODE/leo_sim/learning.py:724

- 定位：learning.py:724-791。
- 职责 (FACT)：按合同名构造观测向量；图合同委托 `build_graph_observation`，其余合同按各自的聚合规则拼接。
- 关键状态/结构：无持有状态；内部定义闭包 `_finish(base)`（741-742）把目的地特征拼到末尾。
- 关键流程/方法：图合同分支（728-731）；取 `information_set`（732）、对每个 origin 算 `_origin_features`（734）；`own` 转 float64（735）；`dst_feats` 为 None 补零、维度不符抛 ValueError（736-739）。逐合同分支：
  - C1（744-748）：`own` + topo 邻居排序后各邻居的 origin 特征块（缺条目补零块），块数截断/补齐到 `C1_MAX_NEIGHBORS = 4`，+ 目的地特征 → 23 维。
  - C3（750-753）：`own` + 全部条目特征的逐维均值（空缓存时全零块）+ 目的地特征 → 11 维。
  - C4（755-762）：`own` + AoI 加权平均（权重 `exp(-max(0,aoi)/max(ttl,1e-9))`，759-760；空缓存全零）+ 目的地特征 → 11 维。
  - C5（764-770）：`own` + 最新鲜（`aoi` 最小）条目的特征 + 1 维标志（有条目为 1.0、无条目为 0.0 且特征块全零）+ 目的地特征 → 12 维；常量注释（47）把该标志称为 "staleness flag"。
  - C6（772-779）：`own` + 按 `min(max(1,hops),4)` 分入 4 个跳数桶的桶内均值（空桶全零）+ 目的地特征 → 23 维。
  - C7（781-789）：`own` + 按 `aoi` 升序前 `C7_MAX_ENTRIES = 5` 个条目、每条 `[特征, 1.0]` 块，不足补全零块 + 目的地特征 → 32 维。
  - 未知合同抛 ValueError（791）。
- 输入/输出：输入与 `build_graph_observation` 同形；输出 float64 np.ndarray，shape = `(CONTRACT_DIMS[contract],)`。
- 依赖关系：调用方 kernel.py:1352（`Kernel._learning_observation`）；测试 test_learning.py:54-55/65/81/114/128/137、test_review_round4.py:336。佐证：test_learning.py:53-58 逐合同断言输出宽度等于 `CONTRACT_DIMS`、两次调用结果一致且全部有限；test_learning.py:133-144 在空缓存场景断言各合同输出宽度、own 块在位且未提供目的地时目的地特征为零块。内部调 `build_graph_observation`(729)、`information_set`(732)、`_origin_features`(734/770/785)。

#### `def build_action_mask(can_deliver, isl_room) -> dict` — CODE/leo_sim/learning.py:794

工具函数（压缩六字段）：定位 learning.py:794-801。职责 (FACT)：构造合法动作掩码 dict——`"deliver": bool(can_deliver)`，再按方向名排序把 `isl_room` 各项转 bool 放入（798-800）；docstring（795-797）声明语义为「deliver 仅在直接可见且有下行余量时合法、每个 ISL 方向仅在队列有余量时合法、由 kernel 从当前本地状态计算」。输入 bool 与 `{方向: 余量}` dict；输出 mask dict。调用方：全 CODE/ grep 仅命中测试 test_learning.py:156、158（FACT）；kernel 实际决策路径不调本函数，而是在 kernel.py:1406 与 1443 用内联 dict 推导 `{a: ... for a in _learning.ACTIONS}` 构造掩码（FACT）。

#### `def ddqn_targets(q_online_next, q_target_next, next_mask, rewards, dones, gamma) -> np.ndarray` — CODE/leo_sim/learning.py:804

工具函数（压缩六字段）：定位 learning.py:804-825。职责 (FACT，docstring 807-812 + 实现)：canonical Double-DQN 目标——online Q 在非法动作处置 `-inf` 后逐行 argmax 得 a*（816-817）；非终态行若选中值非有限（即无合法动作）抛 ValueError（821-822，注释 819-820 说明终态行不需要合法动作）；`y = rewards + gamma * (1-dones) * Q_target(s', a*)`（823-825，终态 bootstrap 置 0 于 824）。输入两个 `(batch, n_actions)` Q 矩阵、bool mask、`(batch,)` rewards/dones、标量 gamma；输出 float64 np.ndarray，shape (batch,)。调用方：learning.py:431（`TensorflowDDQN._train_once` eager 路径）；测试 test_learning.py:166/176/183、test_acceptance_review.py:25。佐证：test_learning.py:162-170 验证掩码 argmax 数学、173-178 验证终态不 bootstrap、181-185 验证无合法动作抛 ValueError。

### 文件 `CODE/leo_sim/receipt.py`（实测 941 行）

模块级说明：

- 模块 docstring（receipt.py:1-22）声明信任模型：本地验证只证明盘上 artifacts（resolved config、trace.csv、manifest.json、ledgers.json、receipt.json）之间的内部一致性，没有外部锚——能同时重写 ledgers.json 并重绑 `receipt.ledgers_sha256` 的人可以伪造出一致的运行；正式防篡改需要治理链（干净的已提交代码身份、授权 manifest、外部 artifact-hash 锚），该 gate 不在本模块解决（FACT，源自 docstring 行 3-10）。docstring 还定义字段权威三类（12-22）：`recomputed`（验证器从 trace.csv/resolved_config.json 重建）、`ledger_consistency`（被 ledgers SHA 绑定、查 schema 与内部关系但不可独立重算）、`diagnostic`（只报告、查 schema、永不可作为研究资格或科学指标证据）。
- imports（receipt.py:23-32）：`__future__.annotations`、`csv`(25)、`hashlib`(26)、`json`(27)、`math`(28)、`platform`(29)、`pathlib.Path`(30)、同包 `config as config_mod, fates, rng as rng_mod, trace as trace_mod`(32)。其中 `csv` 在本文件内除 import 行外仅出现在 docstring（行 379 的 "trace.csv" 字样），无任何 `csv.` 调用（FACT，全文件 grep）。
- 全局常量：
  - `RECEIPT_SCHEMA`(34) = `"leo-sim-receipt/v3"`。
  - `RECEIPT_KEYS`(37-44)：receipt.json 顶层键的精确集合（25 个键），注释（36）声明未知或缺失键都会使验证失败。
  - `DEP_KEYS`(45) = `{python, simpy, numpy, pyyaml}`；`REQUESTED_KEYS`(46-47) = `{policy, association, ge_enabled, control_enabled, monitor, learning_algorithm, learning_mode}`；`EFFECTIVE_KEYS`(48) = `{control_plane, ge, mbb, learning}`。
  - `LEDGER_KEYS`(50-55)：ledgers.json 顶层键精确集合（13 个，含 `field_authority` 与 `learning`）。
  - `CONTROL_COUNTER_KEYS`(56-60)：12 个控制面计数器键；`MECHANISM_COUNTER_KEYS`(61-67)：16 个机制计数器键；`MECHANISM_COUNTER_BOOLS`(68-69) = `{control_initialized, ge_initialized, learning_initialized}`（三键必须为 bool）。
  - `OCCUPIED_KEYS`(70)、`QUEUE_AREA_KEYS`(71)、`ACCESS_KEYS`(72-75)、`ACCESS_INT_KEYS`(76)、`HANDOVER_TYPES`(77) = `{associate, release, bbm, mbb, lease_retire}`。
  - `FIELD_AUTHORITY`(79-92)：12 个 ledger 字段到权威类的映射——`recomputed`：packet_fates、stop_time_s、deliveries、learning；`ledger_consistency`：control_instances、control_counters、mechanism_counters；`diagnostic`：occupied、queue_area_bits_s、handover_events、access、events_processed。
- 环境变量：无（全文件无 `os.environ` 读取，FACT）。

#### `def code_sha256() -> str` — CODE/leo_sim/receipt.py:95

工具函数（压缩六字段）：定位 receipt.py:95-102。职责 (FACT，docstring 96 + 实现)：对 leo_sim 包目录下全部 `*.py` 按文件名排序，逐个把「文件名 + 文件内容 SHA-256 摘要」喂进滚动 SHA-256，返回 hexdigest（97-102）。输入无；输出 64 字符小写 hex 字符串。调用方：receipt.py:308（`build_receipt`）、736（`verify_receipt_dir` 步骤 3）、CODE/leo_sim/governance.py:108、CODE/experiment_platform/authorize_experiment.py:344 与 510（以 `v2_receipt` 别名导入，authorize_experiment.py:240/496）。

#### `def dependency_versions() -> dict` — CODE/leo_sim/receipt.py:105

工具函数（压缩六字段）：定位 receipt.py:105-114。职责 (FACT)：返回 `{python: platform.python_version(), simpy: simpy.__version__, numpy: numpy.__version__, pyyaml: yaml.__version__}`（106-114；numpy/simpy/yaml 在函数体内 import）。输入无；输出 4 键 dict。调用方：receipt.py:310（`build_receipt`）、741 与 743（`verify_receipt_dir` 步骤 3 的重算比对）。

#### `def requested_from_config(cfg) -> dict` — CODE/leo_sim/receipt.py:117

工具函数（压缩六字段）：定位 receipt.py:117-127。职责 (FACT，docstring 118 + 实现)：仅从 resolved config 重建「请求的机制」dict——`policy = cfg["routing"]["policy"]`、`association = cfg["access"]["association"]`、`ge_enabled = bool(cfg["links"]["ge_enabled"])`、`control_enabled = bool(cfg["control_plane"]["enabled"])`、`monitor = bool(cfg["execution"]["monitor"])`、`learning_algorithm = cfg["learning"]["algorithm"]`、`learning_mode = cfg["learning"]["mode"]`（119-127）。输入 resolved config dict；输出 7 键 dict。调用方：receipt.py:299（`build_receipt`）、920（`verify_receipt_dir` 步骤 6）。

#### `def effective_from_counters(counters, requested) -> dict` — CODE/leo_sim/receipt.py:130

工具函数（压缩六字段）：定位 receipt.py:130-147。职责 (FACT，docstring 131-132 + 实现)：从原始机制计数器重算「生效标志」——`control_plane = control_entered_queue > 0`（134）；`ge = requested.ge_enabled 且 (ge_gsl_queries + ge_isl_queries) > 0`（135-137）；`mbb = mbb_events > 0`（138）；`learning`：`requested.learning_mode == "train"` 时看 `learning_train_steps > 0`，否则（含 eval）看 `learning_decisions > 0`（142-146；注释 139-141 说明 eval 合法地不做梯度更新，故以真实模型的路由决策数为准）。输入计数器 dict 与 requested dict；输出 4 键 bool dict。调用方：receipt.py:930（`verify_receipt_dir` 步骤 6）；测试 test_learning.py:254-261 佐证 eval 模式 decisions>0 即判 effective。

#### `def expected_research_eligible(requested, effective, natural_end, interrupted) -> bool` — CODE/leo_sim/receipt.py:150

工具函数（压缩六字段）：定位 receipt.py:150-158。职责 (FACT)：函数体恒 `return False`（158）；docstring（152-157）说明本地 artifacts 永不赋予正式研究资格，四个参数仅作为兼容面与机制诊断保留，正式资格属于绑定评审、授权与部署 commit 的外部治理 receipt。输入四个参数（均不被读取）；输出恒 `False`。调用方：receipt.py:934-936（`verify_receipt_dir` 步骤 6）；无其他调用方。

#### `def _validate_manifest(manifest, resolved_cfg, resolved_version) -> list[str]` — CODE/leo_sim/receipt.py:161

- 定位：receipt.py:161-260。
- 职责 (FACT，docstring 163)：校验 trace manifest 中「不必信任 manifest 自身即可推导」的全部字段；全程向 errors 列表追加字符串、不抛异常。
- 关键状态/结构：局部 `errors` 列表；键集 `base_keys`(165-170)、`proxy_keys`(171)、`population_keys`(172)。
- 关键流程/方法：按 `manifest["mode"]` 决定期望键集（mlab 加 proxy_keys、population_gravity 再加 "population"，173-178），键集不符记错误（179-182）；`schema`/`trace_schema`/`packet_id_contract` 分别比对 `trace_mod.TRACE_MANIFEST_SCHEMA`/`TRACE_SCHEMA`/`PACKET_ID_CONTRACT`（183-188）；`config_version` 比对（189-190）；`resolved_cfg is None` 时提前返回（191-192）；`mode` 必须等于 resolved config 的 `demand.mode`（193-195）；`provenance` 必须等于 `{"mlab": "measurement_proxy", "population_gravity": "population_proxy"}.get(mode, "synthetic")`（196-201）；`rng_streams` 必须等于 `rng_mod.stream_mapping(seed, ["demand"])`（202-205）；`input_sha256`：csv/mlab/population_gravity 模式必须是 64 位小写 hex，synthetic 模式必须为空串（206-212）；mlab 模式要求 `not_calibrated_user_demand is True` 且 `provenance_note` 逐字等于给定英文串（213-219）；population_gravity 模式要求同款声明与另一逐字串（220-227），且 `population` 子表键集精确（228-237）、`source_sha256 == input_sha256`（239-240）、`aggregation_deg`/两个种群指数/`distance_exponent`/`distance_floor_km` 与 resolved config 对应字段逐项相等（241-253）、`total_population` 为正数（254-256）、`candidate_regions >= 2`（257-259）。
- 输入/输出：输入 manifest dict、可空 resolved config、可空版本字符串；输出错误字符串列表（空 = 通过）。
- 依赖关系：调用方 receipt.py:723（`verify_receipt_dir` 步骤 2）；内部调 `_is_nonneg_num`(254)、`_is_nonneg_int`(257)、`rng_mod.stream_mapping`(202)、引用 `trace_mod` 三个常量(183-187)。

#### `def _sha_file(path) -> str` — CODE/leo_sim/receipt.py:263

工具函数（压缩六字段）：定位 receipt.py:263-264。职责 (FACT)：返回 `hashlib.sha256(path.read_bytes()).hexdigest()`。输入 `Path`；输出 64 字符 hex。调用方：receipt.py:353（`write_run` 对 ledgers.json 算 SHA）、422（`_validate_ledgers` 重算 checkpoint SHA）、620/650/755（`verify_receipt_dir` 中 trace.csv/manifest 交叉、ledgers.json 绑定）。

#### `def build_ledgers(result, rows) -> dict` — CODE/leo_sim/receipt.py:267

- 定位：receipt.py:267-291。
- 职责 (FACT)：从 kernel 运行结果与 trace 行组装结构化 run-ledger dict；docstring/NOTE（268-271）声明这是运行自身的陈述、不是独立 ground truth。
- 关键状态/结构：输出 dict 的 13 个键对应 `LEDGER_KEYS`。
- 关键流程/方法：`bits_by_pid` 从 rows 建 pid→bits 映射（272）；`packet_fates` = `{pid: [fate, bits]}`（274-275）；`control_instances` 转字符串键列表对（276-277）；直接搬运 `control_counters`/`mechanism_counters`/`occupied`/`queue_area_bits_s`/`handover_events`/`access`/`events_processed`/`stop_time_s`（278-285）；`deliveries` 键转字符串（286）；`learning` 取 `result["learning"]`、为 None 时落 `{"algorithm": "none"}`（287-289）；`field_authority` 放 `FIELD_AUTHORITY` 副本（290）。
- 输入/输出：输入 kernel result dict 与 trace rows list；输出 ledgers dict。
- 依赖关系：调用方仅 receipt.py:350（`write_run`）。

#### `def build_receipt(resolved, manifest, result, rows, ledgers, ledgers_sha256) -> dict` — CODE/leo_sim/receipt.py:294

- 定位：receipt.py:294-335。
- 职责 (FACT)：组装 receipt.json 的完整 dict（25 个顶层键，对应 `RECEIPT_KEYS`）。
- 关键状态/结构：无持有状态。
- 关键流程/方法：`packet_fates` 重建（296-298）；`requested` 来自 `requested_from_config`（299）；`effective` 取 `result["mechanisms"]["effective"]` 的 `EFFECTIVE_KEYS` 四键（300）；汇总 schema/config_sha256/config_version/trace_manifest_sha256/trace_sha256/trace_identity_sha256/code_sha256()/ledgers_sha256/deps/seed/horizon_s/natural_end/interrupted/error/events_processed/mechanisms/research_eligible/routing_label/totals/fate_counts/packet_fates/control(counters+totals+fate_counts)/occupied/handover_event_count（301-329）；`conservation_ok` = `offered_bits == delivered_bits + terminal_loss_bits + in_system_bits_at_stop`（330-334）。
- 输入/输出：输入 resolved、manifest（含 `__sha256`/`__trace_sha256` 内部键）、result、rows、ledgers、ledgers_sha256；输出 receipt dict。
- 依赖关系：调用方仅 receipt.py:354（`write_run`）；内部调 `requested_from_config`(299)、`code_sha256`(308)、`dependency_versions`(310)。

#### `def write_run(out_dir, resolved, trace_csv, manifest, result, rows) -> dict` — CODE/leo_sim/receipt.py:338

- 定位：receipt.py:338-362。
- 职责 (FACT)：把一次运行的全部 artifacts 写入 `out_dir` 并返回 receipt dict。
- 关键流程/方法：建目录（340-341）；写 `resolved_config.json`（version+config，sorted keys，342-345）；写 `trace.csv` 字节（346）；写 `manifest.json`（剔除 `__` 前缀内部键，347-349）；`build_ledgers` 后写 `ledgers.json`（350-352）并用 `_sha_file` 算其 SHA（353）；`build_receipt`（354-355）；`result["monitor_log"]` 非空时写 `monitor.log`（每行 `t kind {dict}`，356-359）；写 `receipt.json`（360-361）；返回 receipt（362）。
- 输入/输出：输入输出目录、resolved、trace 字节串、manifest、result、rows；输出 receipt dict。
- 依赖关系：调用方 __main__.py:257（`_cmd_run`）、comparison.py:108、acceptance.py:110、platform_check.py:67 与 110、测试 test_review_round4.py:105、test_acceptance_review.py:110/150；内部调 `build_ledgers`(350)、`_sha_file`(353)、`build_receipt`(354)。

#### `def _is_nonneg_num(x) -> bool` — CODE/leo_sim/receipt.py:365

工具函数（压缩六字段）：定位 receipt.py:365-367。职责 (FACT)：`x` 是 int/float、非 bool、`math.isfinite` 且 `>= 0` 时返回 True。输入任意值；输出 bool。调用方：receipt.py:254（`_validate_manifest`）、`_validate_ledgers` 内多处（443、479、501、517、519、538-539 等）、receipt.py:845/857。

#### `def _is_nonneg_int(x) -> bool` — CODE/leo_sim/receipt.py:370

工具函数（压缩六字段）：定位 receipt.py:370-371。职责 (FACT)：`x` 是 int、非 bool 且 `>= 0` 时返回 True。输入任意值；输出 bool。调用方：receipt.py:257（`_validate_manifest`）、`_validate_ledgers` 内多处（407、505、514、524、554、556、580 等）。

#### `def _validate_ledgers(ledgers, receipt, trace_rows, verify_root, resolved_cfg) -> list[str]` — CODE/leo_sim/receipt.py:374

- 定位：receipt.py:374-582。
- 职责 (FACT，docstring 376-380)：对 ledgers.json 做 schema/类型/范围与内部关系校验；docstring 声明全程防御式——畸形内容只追加错误字符串、从不抛异常。
- 关键状态/结构：局部 `errors` 列表；`trace_rows` 为 pid(str) → `{bits, emit, deadline}` 映射。
- 关键流程/方法（按代码顺序）：
  - 顶层：`ledgers` 非 dict 直接返回单错误（382-383）；顶层键精确比对 `LEDGER_KEYS`，不符记错误但继续（384-388，注释 388 说明继续检查在场字段）；`field_authority` 必须精确等于 `FIELD_AUTHORITY`（389-390）。
  - learning 段（396-439，注释 392-395 说明该段防止保存/加载后的模型被静默替换）：receipt 请求的 `learning_algorithm == "none"` 时 ledger 必须恰为 `{"algorithm": "none"}`（399-401）；`== "ddqn"` 时：ledger 必须是 dict（403-404）；`decisions/transitions/train_steps/replay_size` 必须非负 int（406-408）；`algorithm == "ddqn"`（409-410）；`mode ∈ {"train","eval"}`（411-412）；`checkpoint_verified is True`（413-414）；`checkpoint_sha256` 必须是 64 位小写 hex（415-418）；`verify_root/ddqn/online.keras` 必须存在、非 symlink、且文件 SHA 与 ledger 一致（419-423）；与 `mechanism_counters` 的 `learning_decisions/learning_transitions/learning_train_steps` 三项必须一致（424-431）；`mode == "eval"` 时 `train_steps` 必须为 0（432-434），且 resolved config 提供 `learning.checkpoint_sha256` 时 `loaded_checkpoint_sha256` 必须与之相等（435-439）。
  - `stop_time_s`：必须有限非负（442-445）；`receipt.natural_end` 为真时必须恰等于 `receipt.horizon_s`（446-449）。
  - `packet_fates`：必须是 dict（452-455）；每条必须是 `[fate 字符串, 正 int bits]` 二元列表（456-461）。
  - `deliveries`：必须是 dict（464-467）；键集必须恰等于 fate 为 DELIVERED 的 pid 集（468-473）；每条恰含 `delivered_at`/`path` 两键（474-477）；`delivered_at` 有限非负、不早于 trace 的 emit、不晚于 trace 的 deadline（若有）、不晚于 stop_time（478-489）；`path` 必须是 int 列表（490-492）。
  - `occupied`/`queue_area_bits_s`：键集精确、各值有限非负（494-502）。
  - `events_processed`：非负 int（504-506）。
  - `access`：键集精确（509-511）；`ACCESS_INT_KEYS` 四键非负 int（513-515）；三个时长字段有限非负（516-518）；`wait_time_s_max <= wait_time_s_total + 1e-9`（519-522）；`releases` 必须是「字符串原因 → 非负 int」映射（523-526）。
  - `handover_events`：必须是列表（529-531）；每条含 `t`/`endpoint`/`type`（533-537）；`t` 有限非负且不晚于 stop_time（538-541）；`type ∈ HANDOVER_TYPES`（542-543）；`release` 类型必须带字符串 `reason`（544-545）。
  - `control_counters`：键集精确（548-551）；各值非负 int（553-555）；生命周期单调关系：`entered_queue <= registered`、`transmission_started <= entered_queue`、`transmission_completed <= transmission_started`、`arrived <= transmission_completed`（556-564）；`arrived+expired+lost+geometry_lost+overflow+duplicate+in_system == registered`（565-569）。
  - `mechanism_counters`：键集精确（572-574）；`MECHANISM_COUNTER_BOOLS` 三键必须 bool、其余非负 int（575-581）。
- 输入/输出：输入 ledgers（任意值）、receipt dict、trace_rows 映射、verify_root Path、可空 resolved config；输出错误字符串列表。
- 依赖关系：调用方仅 receipt.py:763（`verify_receipt_dir` 步骤 5，且调用被 try/except 包裹、异常转成错误字符串，receipt.py:761-766）；内部调 `_is_nonneg_num`/`_is_nonneg_int`/`_sha_file`(422)。

#### `def verify_receipt_dir(out_dir) -> list[str]` — CODE/leo_sim/receipt.py:585

- 定位：receipt.py:585-941。
- 职责 (FACT，docstring 586)：「重算每一条可校验的声明」，返回错误字符串列表，空列表 = 验证通过。
- 关键状态/结构：局部 `errors`、`receipt`、`manifest`、`trace_rows/trace_list`、`resolved_cfg/resolved_version`、`ledgers`。
- 关键流程/方法（fail-closed 验证链条，按代码顺序）：
  - 前置门禁：`receipt.json` 不存在立即返回单错误（589-591）；JSON 解析异常立即返回（592-595，注释 594 声明损坏 JSON 不得使 verify 崩溃）；解析结果非 dict 立即返回（596-597）。
  - 步骤 0（599-608）：receipt 顶层键精确等于 `RECEIPT_KEYS`；`schema == "leo-sim-receipt/v3"`；`natural_end/interrupted/research_eligible/conservation_ok` 必须为 bool。
  - 步骤 1（610-670）artifact 哈希与 trace/manifest 交叉：`trace.csv` 必须存在且非 symlink（617-618）；文件 SHA 须等于 `receipt.trace_sha256`（620-621）；`trace_mod.load_trace` 解析失败只记错误不崩溃（622-635）。`manifest.json` 同样存在性/非 symlink（636-638）且 SHA 绑定 `receipt.trace_manifest_sha256`（640-641）；解析防御（642-648）；`manifest.trace_sha256` 与 trace 文件实算 SHA 交叉（649-651）；`offered_packets`/`offered_bits`/`ledger`/`time_range_s`/`active_endpoints` 与 trace 实算逐项比对（652-670）。
  - 步骤 2（672-733）config 身份：`resolved_config.json` 存在且非 symlink（675-676）； canonical JSON（sort_keys、紧凑分隔符）SHA 须等于 `receipt.config_sha256`（678-684）；解析失败记错误（685-686）；必须含 scenario/routing 两个组（687-692）；`config_mod.resolve_config` 语义重校验、结果须与原文档逐键相等且 version 一致，失败记错误并置 `resolved_cfg = None`（693-702）；`receipt.config_version`/`seed`/`horizon_s` 分别比对 resolved config 的 version/`scenario.seed`/`scenario.duration_s`（703-709）；`routing_label`：`routing.policy == "oracle"` 时须为 `"analysis_upper_bound"`、否则须为 None（710-713）；`trace_mod.validate_packet_rows` 按 config 的 duration_s/max_packets 校验 trace（714-721）；调 `_validate_manifest`（722-723）；用 `config.trace_identity_sha256` 由 resolved config + manifest 的 `input_sha256` 重算 trace 身份并同时比对 manifest 与 receipt（724-733）。
  - 步骤 3（735-743）代码与依赖身份：`code_sha256()` 现算与 receipt 比对（736-737，错误消息明示"sources changed since the run"）；`deps` 键集精确等于 `DEP_KEYS` 且与当前环境 `dependency_versions()` 完全相等（738-743）。
  - 步骤 4（745-747）运行完成状态：`natural_end` 必须为 True 且 `interrupted` 必须为 False，否则记错误——非自然结束的 run 验证失败。
  - 步骤 5（749-906）ledgers：`ledgers.json` 存在且非 symlink（751-753）；SHA 绑定 `receipt.ledgers_sha256`（755-756）；解析防御（757-760）；调 `_validate_ledgers`，其内部任何异常被捕获转成错误（761-766）；receipt 与 ledgers 的 `packet_fates` 键集与内容必须相等（767-776）、`events_processed`/`occupied`/`handover_event_count` 一致（777-783）；只用 schema 合法的 `[fate, bits]` 对参与后续重算（789-797，注释 789-790 说明这使畸形 artifacts 保持 fail-closed 而不二次崩溃）；packet_fates 键集必须等于 trace pid 集（798-801）；bits 与 trace 一致、fate ∈ `fates.DATA_FATES`（802-807）；重算 `fate_counts` 并与 receipt 比对（808-813）；按 fate 分类求和 delivered/loss/in_system 与 `receipt.totals` 比对、三者之和须等于 `offered_bits`（814-823）；`receipt.conservation_ok` 必须为 True（824-825）；`manifest.offered_bits == receipt.totals.offered_bits`（826-827）；控制面 ledger 重算：每实例须为 `[fate, 正 int bits, received_at|None]`（830-843）、到达类 fate 必须有 received_at、未到达类 fate（CONTROL_EXPIRED 除外）不得有 received_at、received_at 不得晚于 stop_time（844-859）、fate ∈ `fates.CONTROL_FATES` 并逐 fate 计数（860-864）；由有效实例重算 control totals/fate_counts 并与 `receipt.control` 整体比对（865-880）；`control_counters` 与 `mechanism_counters` 的五项对应关系必须相等（884-893）、`registered` 须等于有效实例数（894-895）、各 fate 计数须等于对应计数器（896-906）。
  - 步骤 6（908-940）机制与研究资格：`mechanisms` 恰含 requested/effective（910-913）；requested 无未知键（914-915）；effective 键集精确等于 `EFFECTIVE_KEYS`（916-917）；`requested_from_config(resolved_cfg)` 重算并与 receipt 比对（918-923）；`effective_from_counters(ledgers.mechanism_counters, req)` 重算并与 receipt 比对（926-933）；`expected_research_eligible(...)` 重算（恒 False，见 receipt.py:150-158）并与 `receipt.research_eligible` 比对（934-938）；`requested.monitor` 为真时 `monitor.log` 必须存在（939-940）。
  - 返回 `errors`（941）。
- 输入/输出：输入运行输出目录路径字符串；输出错误字符串列表（空 = 通过）。
- 依赖关系：调用方 __main__.py:273（`_cmd_receipt_verify`，对应 CLI 子命令 `receipt verify`，注册于 __main__.py:350-354）、comparison.py:110、acceptance.py:112、platform_check.py:69 与 112；测试 test_review_round2.py:252-257/314、test_review_round3.py:257/314-333、test_review_round4.py:285/292-298/551-646、test_review_regressions.py:104-128、test_acceptance_review.py:125/160。被调方：`_sha_file`、`trace_mod.load_trace`/`validate_packet_rows`、`config_mod.resolve_config`、`config.trace_identity_sha256`、`_validate_manifest`、`_validate_ledgers`、`code_sha256`、`dependency_versions`、`requested_from_config`、`effective_from_counters`、`expected_research_eligible`、`fates` 的 fate 常量集。

fail-closed 验证链条要点（本文件范围内汇总，均为 FACT）：

1. 缺文件/坏 JSON/非 dict 立即返回错误，不继续（589-597）；后续各段的解析与校验异常一律捕获转成错误字符串而非崩溃（594 注释、632-635、646-648、685-686、700-701、759-766）。
2. 所有读盘 artifact 拒绝 symlink：trace.csv(617)、manifest.json(637)、resolved_config.json(675)、ledgers.json(752)、DDQN checkpoint(420)。
3. 哈希绑定链：receipt 绑定 trace.csv、manifest.json、ledgers.json、resolved_config 的 SHA（620、640、683、755）；manifest 再绑定 trace SHA（649-651）；ledgers 绑定 DDQN checkpoint 文件 SHA 并由验证器重算（415-423）；`code_sha256` 把 receipt 绑定到 leo_sim 包源码（736-737）。
4. 重算而非信任：fate_counts/totals/conservation/control 汇总/requested/effective/research_eligible 全部由验证器从 trace.csv + resolved_config.json + ledgers.json 重算后比对（767-938）。
5. 非自然结束（`natural_end` 非 True 或 `interrupted` 为 True）直接记错误（746-747）；`research_eligible` 的期望值恒为 False（150-158、934-938）。
6. 模块 docstring（1-10）明示该链条只证明内部一致性，外部锚（治理链）不在本模块。
