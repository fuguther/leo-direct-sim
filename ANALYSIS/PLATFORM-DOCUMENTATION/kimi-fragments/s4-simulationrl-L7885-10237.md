# 片段 s4：CODE/SimulationRL.py 第 7885–10237 行

### 文件 `CODE/SimulationRL.py`（实测 12556 行；本片段覆盖 7885–10237 行）

模块级说明：本片段范围内没有 import 语句和全局常量定义（import 集中于文件头 1–229 行，链路/状态常量集中于 293–626 行，均在本片段范围之外）。本片段范围内出现的模块级可执行语句只有两处：

- `_oracle_vis_k_stats = {"used_real_queue": 0, "masked": 0}`（CODE/SimulationRL.py:8778）：k-hop 可见性 oracle 的诊断计数器，注释（8774–8777）声明仅在 `SIM_ORACLE_VIS_K` 激活且给 `_oracle_global_dijkstra_edge_weight()` 传入 source 时被填充，每次 builder 调用时重置（FACT）。
- `_TE_MODULE = None`（CODE/SimulationRL.py:9466）：`temporal_encoder` 模块的惰性缓存，取值 None/模块对象/False（不可导入时），由 `_temporal_apply`（9469）读写（FACT）。

本片段代码引用、但定义在片段之外的模块级符号（行号为定义处）：`_SIM_FAIL_CLOSED`(219)、`pathings`/`_SIM_PATHING`/`pathing`(222/225/226)、`importQVals`/`onlinePhase`(262/263)、`Re`(293)、`Vc`(297)、`f`/`B`/`maxPtx`/`Adtx`/`Adrx`/`pL`/`Nf`/`Tn`/`min_rate`(302–310)、`BLOCK_SIZE`(318)、`coordGran`(332)、`_SIM_M2_FIX`(354)、`_SIM_M3_DYNAMICS`(361)、`_M3_EMA_ALPHA`(362)、`_sat_queue_dynamics`(364)、`_SIM_STATE_MODE`(374)、`_SIM_STATE_VIS_K`(375)、`_SIM_VIS_K_STALE_STEPS`(379)、`_SIM_VIS_K_UPDATE_INTERVAL_S`(383)、`_stale_queue_buffer`(387)、`_GRAPH_MAX_NODES`(391)、`_GRAPH_NODE_FEAT_DIM`(392)、`_RAAC_NODE_FEAT_DIM`(393)、`_RAAC_ACTION_FEAT_DIM`(394)、`_RAAC_AOI_SCALE_S`(395)、`_SIM_FRAME_STACK_K`(495)、`_SIM_MAPPO_MODE`(501)、`notAvail`(552)、`infQueue`(573)、`queueVals`(574)、`latBias`/`lonBias`(575/576)、`biggestDist`/`firstMove`(585/586)、`nnpath`/`nnpathTarget`(625/626)。

---

## 初始化与瓶颈分析

#### `def initialize(env, popMapLocation, GTLocation, distance, inputParams, movementTime, totalLocations, outputPath, matching='Greedy')` — CODE/SimulationRL.py:7885
- 定位：CODE/SimulationRL.py:7885
- 职责：仿真总初始化入口：建 Earth、链小区到 GT、建星座、建图、算全 GT 对最短路径、在各节点上建 SimPy 缓冲与发送进程、按需初始化 Q/DDQN 智能体（FACT，docstring 7886–7896 与函数体一致）。
- 关键状态/结构：读 `inputParams['Constellation'][0]`、`['Fraction'][0]`、`['Test type'][0]`（7900–7902）；构造 `Earth(...)`（7912，class Earth 定义于 3322）；调用 `earth.linkCells2GTs(distance)`（7917）；若 `earth._od_deferred` 且 `earth._pending_traffic_cfg` 非空则调用 `build_od_matrix_for_gateways`（7931，该函数 import 自 `traffic_od`，见第 20 行；定义于 CODE/traffic_od.py:347），失败时 `_SIM_FAIL_CLOSED` 为真则 raise，否则回退 uniform（7935–7942）；`mlab_hourly` 模式把 `hourly_matrices` 从 meta 中 pop 到 `earth.od_weight_matrices_hourly`（7948–7957）；`earth.linkSats2GTs("Optimize")`（7966）；`graph = createGraph(earth, matching=matching)`（7967）并赋给 `earth.graph` 和每个 `gt.graph`（7968–7971）；对所有 GT 对调 `getShortestPath(GT.name, destination.name, earth.pathParam, GT.graph)` 填 `GT.paths`（7976–7982）；`earth._needs_gt_fill_startup` 时调 `gt.makeFillBlockProcesses`（7984–7988）；`earth.trace_traffic_enabled` 时调 `earth.startTraceTraffic()`（7990–7991）；对每颗卫星调 `sat.findInterNeighbours(earth)`（7999），对有 linkedGT 的星调 `sat.adjustDownRate()` 并创建 GSL 发送进程（8005–8008），按图邻居把邻居分为 intra/inter 并创建 `sendBufferSatsIntra/Inter` 与对应 `sendBlock` 进程（8009–8033）；`_SIM_VIS_K_UPDATE_INTERVAL_S > 0` 时启动 `timedQueueSnapshotProcess`（8035–8036）；对 `paths[1]`、`paths[0]` 调 `findBottleneck`（8038–8039）；对每个 GT 调 `findBottleneck` 取最小值并按 GSL 上/下行速率调 `GT.getTotalFlow`（8043–8053）；`pathing` 为 `'Q-Learning'`/`'Deep Q-Learning'` 时构造 `hyperparam(pathing)`（8058，class hyperparam 定义于 5638）并 `saveHyperparams`（8075，定义于 10397）；DQL 且非 `onlinePhase` 时建全局 `DDQNAgent`（8062，class 定义于 6190），否则为每颗卫星各建一个（8068–8070）；Q-Learning 时调 `earth.initializeQTables`（8081）。注意：`pathing`、`onlinePhase`、`importQVals` 是模块级全局变量（226/263/262），不是参数（FACT）。
- 输入/输出：入 SimPy env、人口地图路径、GT csv 路径、覆盖距离、inputParams dict、movementTime、totalLocations、输出路径、matching 算法名；出 `(earth, graph, bottleneck1, bottleneck2)`（8083）。
- 依赖关系：调 Earth、build_od_matrix_for_gateways、createGraph、getShortestPath、findBottleneck、timedQueueSnapshotProcess、hyperparam、saveHyperparams、DDQNAgent；被 `RunSimulation`（定义于 12019）在 12106 行调用。跨文件调用方未确认其他。

#### `def findBottleneck(path, earth, plot=False, minimum=None)` — CODE/SimulationRL.py:8087
- 定位：CODE/SimulationRL.py:8087
- 职责：沿一条路径逐跳收集链路标识/数据率/纬度，求路径瓶颈速率（FACT）。
- 关键流程：首跳取源 GT 的 `GT.dataRate`（8090–8096）；中间跳在 `satellite.interSats`/`intraSats` 中找下一跳邻居并取其数据率（8098–8116）；末跳取目的 GT 的 `GT.linkedSat[1].downRate`（8117–8123）；`minimum` 入参非空时附加 `minimum/速率` 比值列（8096/8109/8116/8123）；`plot=True` 时调 `earth.plotMap` 并 `plt.show()`（8125–8128）；最终 `minimum = np.amin(bottleneck[1])`（8130）。
- 输入/输出：入 path（`getShortestPath` 返回的 [[name,lon,lat],...] 结构）、earth、plot 开关、可选 minimum；出 `(bottleneck, minimum)`，bottleneck 为 4 列列表 [链路名, 数据率, 纬度, 比值]（FACT）。
- 依赖关系：调 `earth.plotMap`、`np.amin`；被 initialize（8038/8039/8048）与 RunSimulation（12453）调用。

---

## 星座与几何/链路工具群

#### `def create_Constellation(specific_constellation, env, earth)` — CODE/SimulationRL.py:8135
- 定位：CODE/SimulationRL.py:8135
- 职责：按名字查表得到 Walker 星座参数（轨道面数 P、每面星数 N_p、总数 N、高度、倾角、Walker star/delta、最小仰角），并实例化全部 `OrbitalPlane`（FACT，参数表 8137–8195，实例化循环 8222–8224）。
- 关键状态/结构：支持 "small"/"Kepler"/"Iridium_NEXT"/"OneWeb"/"Starlink"/"Test" 六种名字（8137–8195）；未知名打印后 `exit()`（8196–8204）；`SIM_WALKER_PATTERN` 环境变量可覆盖 Walker_star，非法值在 `_SIM_FAIL_CLOSED` 下 raise（8206–8212）；Walker star 时分布角减半为 π（8214–8217）。
- 输入/输出：入星座名、env、earth；出 `orbital_planes` 列表（元素为 `OrbitalPlane`，class 定义于 1842）（FACT）。
- 依赖关系：调 `OrbitalPlane`、`os.environ.get`；被 `Earth.__init__` 在 3664 行调用（`self.LEO = create_Constellation(constellation, env, self)`）。

#### `def get_direction(Satellites)` — CODE/SimulationRL.py:8234
- 定位：CODE/SimulationRL.py:8234；职责：返回 N×N int8 矩阵，`direction[i,j]` 为含星 i 倾角与两星 y/z 坐标表达式的符号值（8243–8245），供双收发机方向配对使用（FACT，docstring 8235–8237）；输入：卫星对象列表；输出：np.ndarray (N,N) int8。被 markovianMatchingTwo(8383)、greedyMatching(8488)、establishRemainingISLs(8590) 调用。

#### `def get_pos_vectors_omni(Satellites)` — CODE/SimulationRL.py:8249
- 定位：CODE/SimulationRL.py:8249；职责：抽出全部卫星的 (x,y,z) 坐标矩阵与所在轨道面编号数组（FACT，8253–8259）；输入：卫星列表；输出：`(Positions (N,3), meta (N,))`。被 markovianMatchingTwo(8384)、greedyMatching(8489)、establishRemainingISLs(8589) 调用。

#### `def get_slant_range(edge)` — CODE/SimulationRL.py:8263
- 定位：CODE/SimulationRL.py:8263；职责：返回 `edge.slant_range` 属性（8264）（FACT）；输入：edge 对象；输出：数值。被 markovianMatchingTwo 在 8400 行用作 `sorted` 的 key。

#### `def get_slant_range_optimized(Positions, N)` — CODE/SimulationRL.py:8268
- 定位：CODE/SimulationRL.py:8268；职责：计算 N 颗卫星两两欧氏距离的对称矩阵，对角线置 `math.inf`，只算上三角再转置相加（8272–8277）（FACT）；输入：位置矩阵与 N；输出：(N,N) 距离矩阵。被 markovianMatchingTwo(8385)、greedyMatching(8490)、establishRemainingISLs(8591) 调用。

#### `def los_slant_range(_slant_range, _meta, _max, _Positions)` — CODE/SimulationRL.py:8282
- 定位：CODE/SimulationRL.py:8282；职责：带 `@numba.jit` 装饰（8281）；把距离矩阵中超过 `_max[_meta[i],_meta[j]]`（轨道面对最大可视距离）的元素置为 `math.inf`（8286–8291）（FACT）；输入：距离矩阵、轨道面数组、最大距离矩阵、位置矩阵（_Positions 在函数体内未被使用，FACT）；输出：裁剪后的距离矩阵副本。被 markovianMatchingTwo(8386)、greedyMatching(8491)、establishRemainingISLs(8615) 调用。

#### `def get_data_rate(_slant_range_los, interISL)` — CODE/SimulationRL.py:8295
- 定位：CODE/SimulationRL.py:8295
- 职责：由可视距离矩阵计算全部卫星对的可行数据率矩阵（FACT）。
- 关键流程：内置两张硬编码阈值表 `speff_thresholds`（频谱效率，8299–8304）与 `lin_thresholds`（线性 SNR 门限，8305–8311）；计算自由空间路径损耗 `10*log10((4π·d·f/Vc)^2)`（8313）、SNR（8314）、香农速率（8315，该值算出后未被返回直接使用，FACT）；再逐元素找满足门限的最高频谱效率并乘带宽得 `speffs`（8317–8325）。
- 输入/输出：入可视距离矩阵、`RFlink` 对象（class 定义于 1798，取其 f/maxPtx_db/G/No/B 属性）；出 (N,N) 数据率矩阵（bit/s）（FACT）。
- 依赖关系：用全局 `Vc`(297)；被 markovianMatchingTwo(8387)、greedyMatching(8492)、establishRemainingISLs(8616) 调用。

---

## 匹配/建图函数群

#### `def markovianMatchingTwo(earth)` — CODE/SimulationRL.py:8330
- 定位：CODE/SimulationRL.py:8330
- 职责：为每星两台星间收发机（各占一个方向）贪心地选跨轨道面 ISL，再补上同面上下星 intra ISL，返回 edge 列表（FACT，docstring 8331–8340 与实现一致）。
- 关键流程：硬编码构造 26GHz/500MHz 的 `RFlink`（8353–8363，注意与 greedyMatching 不同，这里不用全局 f/B 等参数，FACT）；按各轨道面高度算面对最大可视距离矩阵 `Max_slnt_rng`（8367–8378）；依次调 get_direction/get_pos_vectors_omni/get_slant_range_optimized/los_slant_range/get_data_rate（8383–8387）；枚举跨面对且方向收发机未被占用的候选边（距离 < 6000km，8394–8398），按 slant_range 升序排序（8400），循环取当前最短且两端方向均未覆盖的边并标记覆盖（8404–8409）；随后对每个轨道面内每颗星调 `sat.findIntraNeighbours(earth)` 并追加 upper/lower 两条 intra 边（8413–8433）。
- 输入/输出：入 earth；出 `_A_Markovian`，元素为 `edge` 类实例（class 定义于 2472），携带 i/j/slant_range/dij/dji/shannonRate（FACT）。
- 依赖关系：调 RFlink、get_direction、get_pos_vectors_omni、get_slant_range_optimized、los_slant_range、get_data_rate、get_slant_range、edge；被 createGraph 在 8685 行（`matching=='Markovian'` 分支）调用。

#### `def greedyMatching(earth)` — CODE/SimulationRL.py:8438
- 定位：CODE/SimulationRL.py:8438
- 职责：贪心建链：每星连同面上下星 + 异面 x 坐标更大/更小方向上最近的星各一颗（"东/西"），返回 edge 列表（FACT，docstring 8439–8444 与实现一致）。
- 关键流程：用模块级全局 f/B/maxPtx/Adtx/Adrx/pL/Nf/Tn/min_rate（302–310）构造 `RFlink`（8459–8469）；算面对最大可视距离（8473–8484）；算方向/位置/距离/可视距离/数据率矩阵（8488–8492）；对每颗星在异面星中按 `Positions[j,0] > Positions[i,0]` 判"东"、`<` 判"西"，取可视距离最小者各加一条边（8495–8510，方向字段传 None）；再加同面 upper/lower 两条 intra 边（8514–8534）。
- 输入/输出：入 earth；出 `_A_Greedy`（edge 列表）（FACT）。
- 依赖关系：调 RFlink、get_direction、get_pos_vectors_omni、get_slant_range_optimized、los_slant_range、get_data_rate、edge；被 createGraph 在 8687 行（`matching=='Greedy'` 分支）调用。

#### `def deleteDuplicatedLinks(satA, g, earth)` — CODE/SimulationRL.py:8539
- 定位：CODE/SimulationRL.py:8539
- 职责：若某星的东（dir 3）或西（dir 4）方向出现重复链路，删除纬度差较大的那条，保留更"水平"的链路（FACT，docstring 8540–8543 与实现一致）。
- 关键流程：内含嵌套函数 `getMostHorizontal(currentSat, satA, satB)`（8545），返回两候选星中纬度更接近 currentSat 者（8549）；遍历 `g.edges(satA.ID)`，对卫星邻居（节点名首字符为数字，8553）调 `findByID`+`getDirection`；东向重复时 `g.remove_edge` 删掉较不水平者（8557–8566），西向同理（8568–8577）。
- 输入/输出：入卫星、图、earth；出无返回值，直接改图 g（FACT）。
- 依赖关系：调 findByID、getDirection；被 createGraph 在 8709 行对每个卫星调用。

#### `def establishRemainingISLs(earth, g)` — CODE/SimulationRL.py:8580
- 定位：CODE/SimulationRL.py:8580
- 职责：为 `right`/`left` 仍为 None 的卫星补建跨面 ISL：把缺右邻的星与缺左邻的星两两配对，按纬度差升序依次建边（FACT，8580–8652）。
- 关键流程：重算位置/方向/距离/可视/数据率矩阵（8589–8616）；收集 `sat.right is None` 与 `sat.left is None` 两个集合（8619–8620）；候选配对要求异面、可视距离有限、经度差 (0,180)（8626–8632），按纬度差排序（8639）；循环中对两端仍空位的配对执行 `g.add_edge(..., slant_range=distance, dataRate=1/_sr, dataRateOG=_sr, hop=1)` 并互设 `sat_r.right`/`sat_l.left`（8643–8649）。
- 输入/输出：入 earth、图 g；出修改后的 g（8652）（FACT）。
- 依赖关系：调 get_pos_vectors_omni、get_direction、get_slant_range_optimized、RFlink、los_slant_range、get_data_rate；被 createGraph 在 8720 行调用。

#### `def createGraph(earth, matching='Greedy')` — CODE/SimulationRL.py:8655
- 定位：CODE/SimulationRL.py:8655
- 职责：构建整个网络拓扑图：卫星与 GT 为节点，GSL/ISL 为边，并给 slant_range 路由封印拓扑校验标记（FACT）。
- 关键流程：`nx.Graph()`（8663）；加全部卫星节点（8667–8669）；为有 linkedSat 的 GT 加节点与 GSL 边（8673–8680，边属性 slant_range/invDataRate/dataRateOG/hop）；按 `matching` 调 markovianMatchingTwo 或 greedyMatching（8684–8687）；把返回的 edge 逐条 `g.add_edge`，`dataRate=1/max(shannonRate,1.0)`、`dataRateOG=max(shannonRate,1.0)`（8694–8701）；`firstMove` 为真时更新全局 `biggestDist`（8702–8703，全局定义于 585/586）；对每星调 deleteDuplicatedLinks（8707–8709）；置 `earth.graph = g` 并对每星调 `findIntraNeighbours`+`findInterNeighbours`（8711–8717）；调 establishRemainingISLs（8720）；随后遍历所有边校验 `slant_range` 为有限正数，生成排序边表并 sha256，把结果封印进 `g.graph["_slant_range_marker"]`，同时初始化 `g.graph["_slant_range_runtime"]` 计数器（8725–8759）；校验出错且 `_SIM_FAIL_CLOSED` 且 `pathing=="slant_range"` 时 raise ValueError（8761–8763）；`firstMove` 首次打印最大星间距并置 False（8766–8768）。
- 输入/输出：入 earth、matching 算法名；出 `nx.Graph`，边属性含 slant_range/dataRate/dataRateOG/hop/dij/dji（FACT）。
- 依赖关系：调 markovianMatchingTwo、greedyMatching、deleteDuplicatedLinks、establishRemainingISLs、hashlib.sha256；被 Earth 方法（5273）与 initialize（7967）调用。

---

## oracle / 最短路径

#### `def _parse_oracle_vis_k(raw)` — CODE/SimulationRL.py:8781
- 定位：CODE/SimulationRL.py:8781；职责：解析 `SIM_ORACLE_VIS_K` 环境变量原值：None/空串/"inf"/"infinity"/不可解析/≤0 一律返回 None（不激活），正整数返回 k（8791–8804）（FACT）；输入：任意原值；输出：int 或 None。被 `_oracle_global_dijkstra_edge_weight` 在 8868 行调用。

#### `def _oracle_global_dijkstra_edge_weight(g, source=None)` — CODE/SimulationRL.py:8807
- 定位：CODE/SimulationRL.py:8807
- 职责：返回一个 networkx 风格的边权函数，权重 = 传播时延 + 单块发送时延×(1+queue_factor×队列长度)，作为"全知"队列感知 Dijkstra 基线（FACT，docstring 8808–8838 与实现一致）。
- 关键流程：`queue_factor` 读 `SIM_ORACLE_QUEUE_FACTOR`（默认 1.0，8839）；内部 `_queue_len(u,v)` 按端点类型取队列长度：星-星调 `sat_u.outbound_queue_len_for_neighbor(sat_v)`，星-GT 取 `len(sat_u.sendBufferGT[1])`，GT-星取 `len(gt_u.sendBuffer[1])`（8841–8855）；`_weight` = `slant_range/Vc + BLOCK_SIZE/max(dataRateOG,1.0) * (1+queue_factor*queue_len)`（8857–8863）；`_parse_oracle_vis_k` 不激活或未传 source 时直接返回 `_weight`（8868–8870）；激活时以 `nx.single_source_shortest_path_length(g, source, cutoff=k)` 求 k 跳内节点集（8877），重置 `_oracle_vis_k_stats`（8884–8885），返回 `_weight_visible_only`：两端都在 k 跳内用真实队列并累计 `used_real_queue`，否则队列按 0 并累计 `masked`（8887–8898）。
- 输入/输出：入拓扑图 g、可选 source 节点 ID；出边权闭包 `(u, v, attrs) -> float`（FACT）。
- 依赖关系：调 _parse_oracle_vis_k、nx.single_source_shortest_path_length；被 getShortestPath 在 8941 行（`weight=='oracle_global_dijkstra'` 分支）调用。注释（8777）提到 `scripts/oracle_vis_k_smoke.py` 使用该计数器，但当前 CODE/scripts 下未找到该文件（FACT：find 无结果），外部引用未确认。

#### `def getShortestPath(source, destination, weight, g)` — CODE/SimulationRL.py:8903
- 定位：CODE/SimulationRL.py:8903
- 职责：计算 source 到 destination 的最短路径并整理成 [节点名, 经度, 纬度] 列表（FACT，docstring 8904–8910）。
- 关键流程：`weight=="slant_range"` 时先做封印校验：`g.graph` 必须有 `_slant_range_marker`、节点/边数与封印一致、标记报告全部边权合法，否则 raise（8915–8927），并定义严格权函数 `_strict_slant_weight`（缺属性、非数值、非有限正值均 raise，8929–8937），累计 `_slant_range_runtime` 计数；其他 weight 若为 `'oracle_global_dijkstra'` 则换 `_oracle_global_dijkstra_edge_weight(g, source=source)`，否则原样传给 `nx.shortest_path`（8941–8942）；对结果做端点绑定与逐跳边存在性校验（8943–8946）；路径首末节点经纬度直接取值、中间节点 `math.degrees` 转换（8947–8952）；异常时若 `_SIM_FAIL_CLOSED` 且 slant_range 则 re-raise，否则打印并返回 -1（8956–8964）。
- 输入/输出：入源/目的节点名、权重模式字符串或权函数、图 g；出 path 列表或 -1（FACT）。
- 依赖关系：调 _oracle_global_dijkstra_edge_weight、nx.shortest_path；被 Satellite 方法（2104）、Earth 多个方法（3910/3925/3939/3953/4128/4159/4189/4220/5022/5321）、initialize（7980）调用；测试 CODE/tests/test_runtime_effect_receipt.py:575 覆盖其 slant_range 失败路径（标记缺失时返回 -1 并计数 failures，见该文件 529–576）。

#### `def plotShortestPath(earth, path, outputPath, ID=None, time=None)` — CODE/SimulationRL.py:8968
- 定位：CODE/SimulationRL.py:8968；职责：调 `earth.plotMap(True, True, path=path, ID=ID, time=time)` 并把图存为 `outputPath + 'popMap_<首节点>_to_<末节点>.png'`（dpi=500），随后 `plt.close()`（8969–8972）（FACT）；输入：earth、path、输出目录、可选 ID/time；输出：无返回，写 PNG 文件。被 2098、4618、4681、4742、5749、7232、12437 行调用。

#### `def normalize(arr, t_min, t_max)` — CODE/SimulationRL.py:8975
- 定位：CODE/SimulationRL.py:8975；职责：把数组 min-max 线性缩放到 [t_min, t_max]（8976–8982）（FACT）；输入：数值序列与目标区间；输出：list。调用方未确认（全文件及 CODE/ 下 grep 仅命中其他文件注释里的 "normalize" 字样，无实际调用）。

---

## 队列观测函数群

#### `def watchScores(earth, g)` — CODE/SimulationRL.py:8990
- 定位：CODE/SimulationRL.py:8990；职责：逐星打印其与每个图邻居之间的 `getSatScore` 分数（邻居为 GT 时打印 "Gateway linked"）（8995–9007）（FACT）；输入：earth、图 g；输出：无返回，仅打印。调用方未确认（grep 无调用点）。

#### `def findByID(earth, satID)` — CODE/SimulationRL.py:9010
- 定位：CODE/SimulationRL.py:9010；职责：线性遍历 `earth.LEO` 各轨道面卫星，返回 ID 匹配的卫星对象；找不到时无显式返回（None）（9014–9017）（FACT）；输入：earth、卫星 ID 字符串；输出：Satellite 或 None。被 1544、2071–2075、2421（Satellite.findInterNeighbours 内）、4565–4709 多处及本片段内 8554/9005/9343 调用。

#### `def computeOutliers(g)` — CODE/SimulationRL.py:9020
- 定位：CODE/SimulationRL.py:9020；职责：对图中所有边的 slant_range 与 dataRateOG 分别做 IQR 统计，返回 (数据率下界 Q1−1.5·IQR, 距离上界 Q3+1.5·IQR)（9025–9047）（FACT）；输入：图 g；出 `(lowerFence, upperFence)`。被 getSatScore 在 9217 行调用。

#### `def getQueues(sat, threshold=None, DDQN=False)` — CODE/SimulationRL.py:9050
- 定位：CODE/SimulationRL.py:9050
- 职责：读取卫星四条出队（intra×2、inter×2）的当前长度；`DDQN=False` 时返回"最长队列超阈值或存在缺失链路"的布尔值，`DDQN=True` 时返回 `{'U','D','R','L'}` 长度字典（9073–9097）（FACT，docstring 9051–9072 描述了队列结构 tuple[list[event], list[DataBlock], ID]）。
- 关键流程：依次读 `sat.sendBufferSatsIntra[0][1]`/`[1][1]` 与 `sat.sendBufferSatsInter[0][1]`/`[1][1]` 的长度；任一索引/属性异常即置 `infQueue=True` 且该方向记 `np.inf`（9077–9092）；非 DDQN 返回 `max(queuesLen) > threshold or infQueue`（9095），DDQN 返回字典（9097）。
- 输入/输出：入卫星、阈值、DDQN 开关；出 bool 或 dict（FACT）。
- 依赖关系：被 6869/6889/6960/12189 行及本片段内 getStaleQueues、timedQueueSnapshotProcess、getObservedQueueRecord、getSatScore、_sat_queue_scores_for_graph、_appendOwnQueueM2、_viskFlatFeat、getDeepStateDiff、getDeepStateDiffLastHop、getDeepState 调用。

#### `def getStaleQueues(sat, DDQN=False, delay=0)` — CODE/SimulationRL.py:9100
- 定位：CODE/SimulationRL.py:9100
- 职责：返回带指定决策步数延迟的队列快照；delay=0 时直接透传 getQueues（FACT，docstring 9101–9119）。
- 关键流程：delay>0 时给 `earth._stale_neighbor_reads` 计数 +1（9122–9124）；以 `id(sat)` 为键在全局 `_stale_queue_buffer`（定义于 387）里维护 `deque(maxlen=delay+1)`，追加当前快照，历史不足 delay+1 时返回当前值，否则返回最旧一项（9125–9135），命中历史时给 `earth._stale_neighbor_history_hits` 计数 +1（9133–9134）。
- 输入/输出：入卫星、DDQN 开关、延迟步数；出与 getQueues 同型（bool 或 dict）（FACT）。
- 依赖关系：调 getQueues；被 getObservedQueueRecord 在 9189 行调用；测试 CODE/tests/test_runtime_effect_receipt.py:290–291 调用（delay=1 的环缓冲行为）。

#### `def timedQueueSnapshotProcess(env, earth)` — CODE/SimulationRL.py:9138
- 定位：CODE/SimulationRL.py:9138；职责：SimPy 进程：每隔 `_SIM_VIS_K_UPDATE_INTERVAL_S` 秒把每颗星的 {U,D,R,L} 队列字典连同 `env.now` 追加到 `earth._timed_queue_history[sat.ID]` 的 deque（9140–9149）；interval≤0 时直接 return（9141–9142）（FACT）；输入：env、earth；输出：生成器（SimPy process）。被 initialize 在 8036 行启动。

#### `def getTimedObservedQueues(observer, target)` — CODE/SimulationRL.py:9152
- 定位：CODE/SimulationRL.py:9152；职责：从 `earth._timed_queue_history[target.ID]` 由新到旧找第一条"采样时刻 + 端到端传播时延 ≤ 当前时刻"的快照返回；传播时延按当前拓扑最短路径逐跳 slant_range/Vc 求和，找不到路径则为 inf；每条候选都不满足时返回全 inf 字典、`float("inf")`、False（9158–9176）；过程中维护 `earth._timed_state_reads/_hits/_misses/_age_sum_s/_age_max_s` 计数（9159、9171–9175）（FACT）；输入：观察者星、目标星；输出 `(queues_dict, age_seconds, valid_bool)`。被 getObservedQueueRecord 在 9188 行调用。

#### `def getObservedQueues(observer, target)` — CODE/SimulationRL.py:9179
- 定位：CODE/SimulationRL.py:9179；职责：`getObservedQueueRecord(observer, target)[0]`，只取队列字典（9180）（FACT）；输入/输出：同 getObservedQueueRecord 的第一项。被 getDeepStateVisK（9595）与 _sat_queue_scores_for_graph（9641）调用。

#### `def getObservedQueueRecord(observer, target)` — CODE/SimulationRL.py:9183
- 定位：CODE/SimulationRL.py:9183；职责：观测分派器：target 即 observer 时返回实时 `getQueues` 结果、age=0、True；`_SIM_VIS_K_UPDATE_INTERVAL_S>0` 时走 getTimedObservedQueues；否则走 getStaleQueues（delay=`_SIM_VIS_K_STALE_STEPS`）、age=0、True（9185–9190）（FACT）；输入：观察者星、目标星；输出 `(queues, age_s, valid)`。被 getObservedQueues（9180）、getDeepStateRAACGraph（9818）调用；测试 CODE/tests/test_runtime_effect_receipt.py:342 及 1161（patch 点）引用。

#### `def hasBadConnection(satA, satB, thresholdSL, thresholdTHR, g)` — CODE/SimulationRL.py:9193
- 定位：CODE/SimulationRL.py:9193；职责：取边 `(satA.ID, satB.ID)` 的 slant_range 与 dataRateOG，返回"距离超阈或吞吐低于阈"的布尔值（9198–9201）（FACT）；输入：两星、两阈值、图；输出 bool。被 getSatScore 在 9221 行调用。

#### `def getSatScore(satA, satB, g)` — CODE/SimulationRL.py:9204
- 定位：CODE/SimulationRL.py:9204；职责：给"从 satA 发到 satB"打 0/1/2 三档分：satB 为 None 或其队列超 125（硬编码阈值，9216）→ 2；链路被 computeOutliers 判为差 → 1；否则 → 0（9219–9224）（FACT；docstring 9206–9214 说明阈值 125 的来源是历史实验观察，属注释声明）；输入：两星、图；输出 int。被 watchScores（9005）与 getState（9458–9461）调用。

#### `def getDeepSatScore(queueLength)` — CODE/SimulationRL.py:9228
- 定位：CODE/SimulationRL.py:9228；职责：把队列长度映射为 0..`queueVals` 的整数分：`queueLength > infQueue` 时返回 `queueVals`，否则返回 `floor(queueVals * log10(queueLength+1) / log10(infQueue))`（9230，用全局 queueVals=10、infQueue=5000，定义于 573/574）（FACT）；输入：队列长度数值；输出 int。被本片段内各深度状态构造函数（getDeepStateVisK 9596、_sat_queue_scores_for_graph 9642、getDeepStateRAACGraph 9819、_viskFlatFeat 9910、getDeepStateDiff 9989 等、getDeepStateDiffLastHop 10122 等、getDeepState 10202 等）调用。

---

## 方向/邻居函数群

#### `def getDirection_deprecated(satA, satB)` — CODE/SimulationRL.py:9233
- 定位：CODE/SimulationRL.py:9233；职责：旧版方向判定：同面按纬度返回 1（上）/2（下）；异面按经度差是否超过 π 决定是否反转东西逻辑，返回 3（右/东）/4（左/西）（9246–9263）（FACT）；输入：两星；输出 int 1–4。调用方未确认（grep 无调用点；名字带 _deprecated 且存在替代函数 getDirection）。

#### `def getDirection(satA, satB)` — CODE/SimulationRL.py:9266
- 定位：CODE/SimulationRL.py:9266；职责：方向判定：同面按纬度返回 1/2；异面把两星经度归一化到 [−π,π] 后按经度差符号返回 3（右）/4（左），处理跨 ±180° 回绕（9271–9295）（FACT）；输入：两星；输出 int 1–4。被 Satellite.findInterNeighbours（2422）、deleteDuplicatedLinks（8555）、getLinkedSats（9344）调用。

#### `def linkedSatsList(g)` — CODE/SimulationRL.py:9298
- 定位：CODE/SimulationRL.py:9298；职责：遍历图中所有非卫星节点（节点名首字符非数字，即 GT），收集其第一条边，返回 `pd.DataFrame`（每行一条 (GT名, 卫星ID) 边）（9302–9306）（FACT）；输入：图 g；输出 DataFrame。被 getDestination 在 9318 行调用。

#### `def getDestination(Block, g, sat=None)` — CODE/SimulationRL.py:9309
- 定位：CODE/SimulationRL.py:9309；职责：取 Block 目的 GT 所连卫星的 ID，在 linkedSatsList 结果中的位置索引并返回；`sat` 参数非 None 的分支只有 `pass` 与被注释掉的代码（9320–9325，即该分支未实现，FACT）；输入：DataBlock、图 g、可选 sat；输出 int 索引。被 getState 在 9455 行调用。

#### `def getLinkedSats(satA, g, earth)` — CODE/SimulationRL.py:9328
- 定位：CODE/SimulationRL.py:9328；职责：基于图边与 getDirection，把 satA 的卫星邻居分入 `{'U','D','R','L'}` 字典；同一方向出现第二个邻居时按纬度把更靠北/南者重排（极区回绕处理，9346–9364）；东/西方向后见者直接覆盖先见者（9366–9374）（FACT）；输入：卫星、图、earth；输出字典（值为 Satellite 或 None）。被 4536（Earth 方法内）与 5691（class QLearning 的方法内）调用。

#### `def getDeepLinkedSats(satA, g, earth)` — CODE/SimulationRL.py:9381
- 定位：CODE/SimulationRL.py:9381；职责：直接读卫星对象的 `upper/lower/right/left` 属性组装 `{'U','D','R','L'}` 字典（9391–9394）；g、earth 参数在函数体内未被使用，替代的图遍历实现整段被注释（9396–9411）（FACT）；输入：卫星、图、earth；输出字典。被 DDQNAgent.makeDeepAction（7064）在 7094/7251/7255 行调用。

#### `def getKHopNeighbors(satA, k)` — CODE/SimulationRL.py:9416
- 定位：CODE/SimulationRL.py:9416；职责：沿 `.upper/.lower/.right/.left` 做 BFS 至 k 跳，返回 `[(sat, hop, first_dir)]` 列表，first_dir 为从 satA 出发的首跳方向；每颗星按首次到达记录一次，None 链路跳过（9425–9440）（FACT，docstring 9417–9424 与实现一致）；输入：卫星、k；输出列表。被 getDeepStateVisK（9594）、getDeepStateVisKGraph（9678）、getDeepStateRAACGraph（9804）调用；测试 CODE/tests/test_state_vis_k.py:48–74 覆盖 k=1/k=2/角落节点/k=0 情形，CODE/tests/test_runtime_effect_receipt.py:1168、1220 处被 patch。

---

## 状态特征函数群

#### `def getState(Block, satA, g, earth)` — CODE/SimulationRL.py:9443
- 定位：CODE/SimulationRL.py:9443；职责：构造 Q-Table 用的 5 维状态：`[U,D,R,L 四方向 getSatScore 分数, 目的卫星索引]`，初始值全 2（最差），邻居来自 `satA.QLearning.linkedSats`（9455–9463）（FACT）；输入：DataBlock、卫星、图、earth；输出 list（调用处 5754 转成 tuple）。被 QLearning.makeAction（class QLearning 定义于 5682，方法定义于 5721）在 5754 行调用。

#### `def _temporal_apply(sat, state)` — CODE/SimulationRL.py:9469
- 定位：CODE/SimulationRL.py:9469；职责：惰性导入 `temporal_encoder` 模块并调其 `apply(sat, state)`；模块不可导入时置 `_TE_MODULE=False` 并原样返回 state；apply 抛异常时给 `earth._temporal_apply_failures` 计数并 re-raise；`mode() != "none"` 时给 `earth._temporal_apply_successes` 计数（9474–9496）（FACT）；输入：卫星、状态数组；输出：处理后的状态或原状态。被 DDQNAgent.makeDeepAction 在 7126 行调用；测试 CODE/tests/test_runtime_effect_receipt.py:285 验证模块缺失时的恒等透传。

#### `def _apply_frame_stack(sat, state)` — CODE/SimulationRL.py:9499
- 定位：CODE/SimulationRL.py:9499；职责：MAPPO 帧堆叠：`_SIM_MAPPO_MODE` 属于 ("framestack_bp","full_recurrent","bp_only") 且 `_SIM_FRAME_STACK_K>1` 时，在每星的 `sat._mappo_frame_buf`（deque(maxlen=K)）里维护最近 K 帧，不足 K 帧时左侧重复填充首帧，输出 (1, K×base_dim) 数组；否则原样透传（9511–9528）（FACT）；输入：卫星、单帧状态；输出 np.ndarray。被 DDQNAgent.makeDeepAction 在 7125 行调用。

#### `def getBiasedLatitude(sat)` — CODE/SimulationRL.py:9531
- 定位：CODE/SimulationRL.py:9531；职责：返回 `(int(degrees(sat.latitude)) + latBias) / coordGran`；AttributeError 时返回 `notAvail`（9532–9536）（FACT）；输入：卫星（或 None）；输出数值。被 getDeepStateReduced、getDeepState 调用。

#### `def getBiasedLongitude(sat)` — CODE/SimulationRL.py:9539
- 定位：CODE/SimulationRL.py:9539；职责：经度版本，`(int(degrees(sat.longitude)) + lonBias) / coordGran`，异常返回 notAvail（9540–9544）（FACT）；输入/输出同上。被 getDeepStateReduced、getDeepState 调用。

#### `def getDeepStateReduced(block, sat, linkedSats)` — CODE/SimulationRL.py:9547
- 定位：CODE/SimulationRL.py:9547；职责：构造 12 维纯位置深度状态：四邻居的 biased 经纬度（8 维）+ 自身 biased 经纬度（2 维）+ 目的星 biased 经纬度（2 维）；目的 GT 无 linkedSat 时打印并返回 None（9548–9563）（FACT）；输入：DataBlock、卫星、linkedSats 字典；输出 (1,12) np.ndarray 或 None。被 DDQNAgent.makeDeepAction 在 7109 行调用。

#### `def getDeepStateVisK(block, satA, k=None)` — CODE/SimulationRL.py:9566
- 定位：CODE/SimulationRL.py:9566
- 职责：C3 状态构造器：k 跳邻居按首跳方向分四组，对每组邻居的四方向队列分（getDeepSatScore(getObservedQueues(...))）取均值 4 维 + 最大值 4 维，再加该方向直连邻居相对位置 2 维，尾部加自身绝对位置 2 维 + 目的相对位置 2 维，`_appendOwnQueueM2` 按 `_SIM_M2_FIX` 门控追加 4 维；k 缺省取 `_SIM_STATE_VIS_K`（9577–9619）（FACT；docstring 9567–9576 声明固定 44 维、k=1 时等价于仅直连邻居）。
- 关键流程：嵌套 `_rel(neighbor_sat, cur, is_lat)` 计算带 ±180° 回绕的相对坐标 /coordGran（9584–9590）；`getKHopNeighbors(satA, k)` 分组聚合（9593–9597）；无邻居方向填 8 个 `float(queueVals)`（9607）；直连邻居缺失填 notAvail（9613）；目的 GT 无 linkedSat 时打印并返回 None（9580–9582）。
- 输入/输出：入 DataBlock、卫星、可选 k；出 (1, 44[+4]) np.float32 数组或 None（FACT）。
- 依赖关系：调 getKHopNeighbors、getObservedQueues、getDeepSatScore、_appendOwnQueueM2；被 DDQNAgent.makeDeepAction 在 7099 行（`_SIM_STATE_MODE=='c3'`）调用；DDQNAgent.__init__ 在 6225–6227 行按 44(+4) 维配套。

#### `def _sat_rel_coord(neighbor_sat, root_sat, is_lat)` — CODE/SimulationRL.py:9622
- 定位：CODE/SimulationRL.py:9622；职责：邻居相对 root 的纬度/经度差，带 ±180° 回绕后 /coordGran；AttributeError 返回 notAvail（9623–9628）（FACT）；输入：两星、纬度开关；输出数值。被 getDeepStateVisKGraph（9699/9700、9716/9717、9722/9723）调用。

#### `def _sat_abs_coord(sat, is_lat)` — CODE/SimulationRL.py:9631
- 定位：CODE/SimulationRL.py:9631；职责：星的绝对纬度/经度加 bias 后 /coordGran；AttributeError 返回 notAvail（9632–9637）（FACT）；输入：星、纬度开关；输出数值。被 getDeepStateVisKGraph（9720/9721）调用。

#### `def _sat_queue_scores_for_graph(sat, *, root=False, observer=None)` — CODE/SimulationRL.py:9640
- 定位：CODE/SimulationRL.py:9640；职责：root 时用实时 getQueues，否则用 getObservedQueues(observer, sat)，返回四方向 getDeepSatScore 列表（9641–9643）（FACT）；输入：星、root 标志、观察者；输出 4 维 list。被 getDeepStateVisKGraph 在 9690 行调用。

#### `def _sat_degree_norm(sat)` — CODE/SimulationRL.py:9646
- 定位：CODE/SimulationRL.py:9646；职责：返回星的 upper/lower/right/left 中非 None 的个数 / 4.0；任何异常返回 0.0（9647–9651）（FACT）；输入：星；输出 float。被 getDeepStateVisKGraph（9692）、getDeepStateRAACGraph（9821）调用。

#### `def getDeepStateVisKGraph(block, satA, k=None)` — CODE/SimulationRL.py:9654
- 定位：CODE/SimulationRL.py:9654
- 职责：C4/C5 图状态构造器：以 satA 为根的 k 跳 ISL 子图，输出定长拼接向量 [节点特征 (MAX_N,14) | 有向邻接 (MAX_N,MAX_N) | 按首跳方向分组的 readout 掩码 (4,MAX_N) | C3 兼容尾部]（FACT，docstring 9655–9664 与实现一致）。
- 关键流程：`discovered` = 根 + getKHopNeighbors，按 (hop, ID) 排序后截断到 `_GRAPH_MAX_NODES`，记录 overflow（9677–9682）；每节点 14 维特征：4 队列分（root 用实时，其余用观测）、hop/k、度归一、is-root、常数 1、首跳方向 one-hot（4 维）、相对坐标 2 维（9689–9700）；邻接按四方向属性建 `adj[dst,src]=1`（9704–9710）；尾部 = 四直连邻居相对坐标 + 自身绝对坐标 + 目的相对坐标 + `_appendOwnQueueM2`（9712–9724）；构造统计写入 `earth._graph_state_builds/_nodes_seen/_edges_seen/_overflow_nodes` 并调 `_append_graph_state_log`（定义于 937）（9726–9741）；最终 concatenate 成一行（9743–9749）。
- 输入/输出：入 DataBlock、卫星、可选 k；出 (1, N) np.float32 数组（N 由 graphStateDim()（5901）对应）或 None（目的 GT 无 linkedSat 时，9667–9670）（FACT）。
- 依赖关系：调 getKHopNeighbors、_sat_queue_scores_for_graph、_sat_degree_norm、_sat_rel_coord、_sat_abs_coord、_appendOwnQueueM2、_append_graph_state_log；被 DDQNAgent.makeDeepAction 在 7103/7105 行（c4/c5 分支）与 getDeepStateVisKGAT（9754）调用。

#### `def getDeepStateVisKGAT(block, satA, k=None)` — CODE/SimulationRL.py:9752
- 定位：CODE/SimulationRL.py:9752；职责：直接返回 `getDeepStateVisKGraph(block, satA, k=k)`（9754）（FACT）；docstring 称其为"旧 smoke 脚本的向后兼容名"（9753，FACT 为注释声明）；输入/输出：同 getDeepStateVisKGraph。调用方未确认（CODE/ 内 grep 无其他调用点）。

#### `def _ecef_relative(src, dst)` — CODE/SimulationRL.py:9757
- 定位：CODE/SimulationRL.py:9757；职责：返回 dst 相对 src 的 ECEF 坐标差向量，按地球半径 Re 归一化；属性/类型异常返回 [0,0,0]（9759–9767）（FACT）；输入：两个带 x/y/z 属性的对象；输出 3 维 list。被 getDeepStateRAACGraph（9826、9842、9855、9856）调用。

#### `def _reachable_without_root(first_hop, root, max_depth)` — CODE/SimulationRL.py:9770
- 定位：CODE/SimulationRL.py:9770；职责：从 first_hop 出发 BFS（不经过 root），深度上限 max_depth，返回可达节点的 id 集合（含 first_hop 自身）；first_hop 为 None 或 max_depth<0 时返回空集（9772–9788）（FACT）；输入：首跳星、根星、深度；输出 set。被 getDeepStateRAACGraph 在 9814 行调用。

#### `def getDeepStateRAACGraph(block, satA, k=None)` — CODE/SimulationRL.py:9791
- 定位：CODE/SimulationRL.py:9791
- 职责：C6/C7 图状态构造器：k 跳子图节点特征 17 维（含观测有效位与 AoI）+ 邻接 + 允许跨动作重叠的 readout 分支掩码 + 每动作 9 维 action 特征（FACT，docstring 9792 与实现一致）。
- 关键流程：发现/排序/截断逻辑与 getDeepStateVisKGraph 相同（9803–9808）；`branches[d]` = `_reachable_without_root(d 方向直连邻居, satA, k-1)`（9813–9816）；每节点特征：4 队列分（经 getObservedQueueRecord，带 age/valid）、hop/3.0、度归一、is-root、常数 1、首跳方向 one-hot、ECEF 相对 3 维、observed 标志、AoI=min(age/`_RAAC_AOI_SCALE_S`,10)（未观测或非有限时取 10）（9817–9829）；非根节点按 branches 成员关系填 readout（9830–9833）；邻接同 C4/C5（9835–9839）；action_feats 每方向 9 维：存在位、slant_range/maxSlantRange、dataRateOG/B、邻居→目的 ECEF 相对 3 维、自身→目的 ECEF 相对 3 维（9841–9856）；统计计数同 C4/C5（9858–9861）；输出 concatenate 后 (1,-1)（9862–9863）。
- 输入/输出：入 DataBlock、卫星、可选 k；出 (1, N) np.float32 数组（N 由 raacGraphStateDim()（5913）对应）或 None（9796–9797）（FACT）。
- 依赖关系：调 getKHopNeighbors、_reachable_without_root、getObservedQueueRecord、getDeepSatScore、_sat_degree_norm、_ecef_relative；被 DDQNAgent.makeDeepAction 在 7107 行（c6/c7 分支）调用；测试 CODE/tests/test_runtime_effect_receipt.py:1120（类 docstring）、1172、1225 调用并断言其输出契约。

#### `def _appendOwnQueueM2(state_list, sat)` — CODE/SimulationRL.py:9866
- 定位：CODE/SimulationRL.py:9866；职责：`_SIM_M2_FIX` 为真时向 state_list 追加 4 维自身出队占用（各方向队列长度/infQueue 截断到 1.0）；否则无操作（9872–9875）（FACT）；输入：可变 list、卫星；输出：无返回，原地修改 list。被 getDeepStateVisK（9618）、getDeepStateVisKGraph（9724）、getDeepStateVisKFlat（9949）调用。

#### `def visKFlatDim(k)` — CODE/SimulationRL.py:9878
- 定位：CODE/SimulationRL.py:9878；职责：返回 C2 扁平状态维度 `4 * (4*(4^k - 1)//3) + 4`（满 4 叉树 k 层节点数 × 4 队列分 + 自身绝对 2 + 目的相对 2）（9884–9885）（FACT）；输入：k；输出 int。被 DDQNAgent.__init__ 在 6230 行调用；测试 CODE/tests/test_state_vis_k.py:85–91、115–120 断言 k=1→20、k=2→84、k=3→340 及与 visKFlatUnroll 输出长度的一致性。

#### `def visKFlatUnroll(node, depth, feat_fn, pad_feat)` — CODE/SimulationRL.py:9888
- 定位：CODE/SimulationRL.py:9888；职责：纯递归位置展开：按 (upper,lower,right,left) 固定顺序把每个方向子树展开到 depth 层，子节点存在则插入 feat_fn(child) 特征，缺失则插入 pad_feat 且整个缺失子树全部填充；输出长度固定（9897–9904）（FACT）；输入：节点、深度、特征函数、填充特征；输出 list。被 getDeepStateVisKFlat 在 9944 行调用；测试 CODE/tests/test_state_vis_k.py:96–120 用 mock 网格覆盖。

#### `def _viskFlatFeat(child)` — CODE/SimulationRL.py:9907
- 定位：CODE/SimulationRL.py:9907；职责：返回该星四方向队列的 getDeepSatScore 列表（实时 getQueues，9909–9911）（FACT）；输入：卫星；输出 4 维 list。被 getDeepStateVisKFlat 在 9944 行作为 feat_fn 传入。

#### `def getDeepStateVisKFlat(block, satA, k=None)` — CODE/SimulationRL.py:9914
- 定位：CODE/SimulationRL.py:9914；职责：C2 扁平状态构造器：`visKFlatUnroll(satA, k, _viskFlatFeat, [queueVals]*4)` 得到位置化队列分序列，尾部加自身绝对位置 2 维 + 目的相对位置 2 维（嵌套 `_rel` 处理回绕），`_appendOwnQueueM2` 按门控追加；目的 GT 无 linkedSat 返回 None（9928–9950）（FACT）；输入：DataBlock、卫星、可选 k；出 (1, visKFlatDim(k)[+4]) np.float32 数组或 None。被 DDQNAgent.makeDeepAction 在 7101 行（c2 分支）调用。

#### `def getDeepStateDiff(block, sat, linkedSats)` — CODE/SimulationRL.py:9953
- 定位：CODE/SimulationRL.py:9953
- 职责：C1 默认深度状态：四个邻居各自的 4 队列分 + 相对坐标 2 维（4×6=24 维）+ 自身绝对坐标 2 维 + 目的相对坐标 2 维，共 26 维；`_SIM_M2_FIX` 追加自身队列占用 4 维；`_SIM_M3_DYNAMICS` 再追加队列速度 dq 4 维与 EMA 趋势 4 维（FACT，9987–10058）。
- 关键流程：嵌套 `normalize_angle_diff`（9954）、`get_relative_position`（9958）、`get_absolute_position`（9968）；目的 GT 无 linkedSat 打印并返回 None（9972–9975）；邻居队列经实时 getQueues 读取（9982–9985）；M3 在全局 `_sat_queue_dynamics`（定义于 364）按 id(sat) 维护 prev/ema_dq，alpha 取 `_M3_EMA_ALPHA`（10042–10056）。
- 输入/输出：入 DataBlock、卫星、linkedSats 字典；出 (1, 26[+4][+8]) np.ndarray 或 None（FACT）。
- 依赖关系：调 getQueues、getDeepSatScore；被 DDQNAgent.makeDeepAction 在 7111 行调用（注释标注 "This is the one being used by default"）。

#### `def getDeepStateDiffLastHop(block, sat, linkedSats)` — CODE/SimulationRL.py:10061
- 定位：CODE/SimulationRL.py:10061
- 职责：getDeepStateDiff 的变体：在最前面多 1 维"上一跳来源方向"特征（0=上/1=下/2=右/3=左/-1=上一跳星已非当前邻居或路径不足），其余结构（26 维 + M2/M3 门控追加）与 getDeepStateDiff 相同（FACT，10118–10189）。
- 关键流程：嵌套 `get_last_satellite(block, sat)`（10080）比较 `block.QPath[-2][0]` 与 sat.upper/lower/right/left 的 ID，要求 `len(block.QPath) > 2`（10087–10101）；其余嵌套函数与 M2/M3 块同 getDeepStateDiff（10062–10078、10163–10187）。
- 输入/输出：入 DataBlock、卫星、linkedSats 字典；出 (1, 27[+4][+8]) np.ndarray 或 None（10103–10106）（FACT）。
- 依赖关系：调 getQueues、getDeepSatScore；被 DDQNAgent.makeDeepAction 在 7113 行调用。

#### `def getDeepState(block, sat, linkedSats)` — CODE/SimulationRL.py:10192
- 定位：CODE/SimulationRL.py:10192；职责：28 维深度状态：四邻居各 4 队列分 + biased 经纬度 2 维（4×6=24 维）+ 自身 biased 经纬度 2 维 + 目的星 biased 经纬度 2 维；目的 GT 无 linkedSat 打印并返回 None（10193–10235）（FACT）；输入：DataBlock、卫星、linkedSats 字典；出 (1,28) np.ndarray 或 None。被 DDQNAgent.makeDeepAction 在 7115 行调用。
