# LEO 仿真平台 V2：卫星直连接入、真实控制链路与旧机制清理计划

## 1. 目标、事实与边界

当前源码仍以 [`SimulationRL.py`](/Users/lge/Desktop/LEO-Research-Workspace/CODE/SimulationRL.py) 的 Gateway 汇聚路径为正式主线；仓库中没有可直接接管正式运行的完整 `satellite_direct` 内核。因此本计划不是“小修补”，而是在保留可信基础设施的前提下建设并切换新内核。

新平台正式定义为：

`不可变需求 trace → 稀疏地理网格端点 → 卫星有限接入 → ISL 路由 → 本地发现目的端 → 地面网格端点`

- 地面网格是业务源和宿；卫星不是业务端点。
- 每颗卫星只要当前可见且资源允许，都可以成为 ingress/egress 卫星。
- 不再依赖 4 个或 31 个 Gateway 作为源端或目的端。
- 接入、排队、切换、链路中断、控制信息延迟和带宽开销都进入离散事件模型。
- v1 是系统级链路抽象，不模拟波形、调制编码、频率复用、波束间干扰或真实 Starlink 专有参数。
- 本轮验收终点是“本地测试 + 三角色审阅 + 授权 + VM 自然结束与收据闭环”，不包含算法优劣结论。
- 在新平台通过验收前，旧代码只冻结、不删除；验收后从正式代码删除，以 Git tag 和 bundle 保存历史，不复制第二套源码归档。

## 2. 新架构与公开接口

### 配置与使用方式

建立模块化 `CODE/leo_sim/`，正式入口为 `python -m leo_sim`，提供：

- `config validate`：校验并解析 YAML。
- `trace compile`：生成不可变需求 trace 和 manifest。
- `run --dry-run`：解析、哈希和资源预检，不启动仿真。
- `run`：训练或评估。
- `receipt verify`：核验自然结束、机制生效、守恒和产物闭环。

用户可以继续用自然语言描述实验，由模型生成 YAML；仿真器本身不嵌入不可审计的自然语言解释器。

配置使用版本化 schema，固定顶层：

- `scenario`
- `endpoints`
- `demand`
- `access`
- `links`
- `control_plane`
- `routing`
- `learning`
- `execution`
- `outputs`

解析优先级为“规范默认值 < 命名 profile < 实验显式覆盖”，最终生成不可变 resolved config 和 SHA256。未知字段、旧环境变量别名、缺少关键物理参数或哈希不一致一律 fail closed。子进程只接收配置路径、配置 SHA 和运行身份，不再依赖大量 `SIM_*` 参数桥。

### 需求与地面端点

- 规范网格 ID 固定为 0.25°；常规 profile 默认聚合至 1°。
- 只实例化 trace 中实际活跃的网格，设置 active-endpoint 上限。
- canonical trace 采用有序 CSV，字段至少包含：
  `packet_id, emit_time_s, src_grid_id, dst_grid_id, bits, deadline_at_s`。
- 配套 manifest 记录 schema、生成配置 SHA、原始数据 SHA、随机流、记录数、offered bits、活跃端点和时间范围。
- 支持 uniform、gravity、hotspot、burst、diurnal、通用 CSV 和 M-Lab。
- M-Lab 可进入正式运行，但必须标记为 `measurement_proxy`；在代表性验证前不得称为真实用户业务流量。
- 数据 deadline 默认关闭；启用后与控制信息 TTL 使用不同 fate。

### 接入、切换和链路

- 每颗卫星有可配置接入槽 `K`、有限上下行队列和共享 GSL 容量。
- 活跃端点之间采用确定性的 deficit round-robin 公平调度。
- 关联只使用当前几何、仰角、局部负载和终端能力，不读取未来星历。
- 默认切换语义：同星保留 + 迟滞 + 最短驻留 + 建链时延 + BBM。
- MBB 仅在终端声明双连接能力且卫星存在额外接入槽时启用；新链建立后，新包转到新链，旧链只排空已分配数据，并受退出时限约束。
- 计划切换不抢占正在发送的包；几何消失或随机中断可使当前包失败。
- GSL 和 ISL Gilbert–Elliott 中断分别配置、分别使用随机流，默认关闭；不得用随机中断代替几何不可见、切换或拥塞。
- 中途断链时，当前数据包或控制包失败，已占用链路时间照计；v1 不隐式暂停、续传或自动 ARQ。
- ISL 按方向设置独立有限队列和容量；无可用动作时数据包等待重新决策，而不是静默丢弃。

### 控制平面与路由

- 卫星周期性采样直接可观测的队列、链路、接入负载和邻居状态。
- 状态封装为真实控制包，携带 `origin, seq, generated_at, ttl, remaining_hops, payload_bits`。
- 控制包最多传播 `vis_k` 跳，与数据包共享 ISL 容量。
- 控制包采用非抢占高优先级：不能打断正在发送的数据包，但在链路下一次空闲时优先于排队数据。
- 每颗卫星只维护实际到达且未过期的本地缓存；所有学习算法消费同一缓存，不允许 C4/C5/C6/C7 获得隐藏全局状态。
- 数据包携带目的网格坐标；当当前卫星能看见目的端且下行资源可用时，`deliver` 成为合法动作，否则只能选择当前可用 ISL 邻居。
- 正式保留：
  - hop 最短路；
  - 传播时延/斜距最短路；
  - 可用容量感知最短路；
  - 全局 Oracle，仅作为分析上界；
  - DDQN 的 C1、C3、C4、C5、C6、C7。
- DDQN 固定采用真正 Double-DQN：online argmax、target evaluation、下一状态 action mask。
- M1 的正确队列奖励和 M2 的本地出向队列观测吸收为统一基线；删除开关。M3、线性奖励和旧 checkpoint 兼容不进入 v1，所有模型重新训练。

## 3. 分阶段实施

### 阶段 0：边界冻结与不可变基线

- 记录当前 commit、工作区状态、完整测试数、VM 部署身份和现有行为收据。
- 创建新的 pre-platform-v2 tag 和可验证 git bundle。
- 在 `ANALYSIS/` 建立唯一设计包，写清实体、资源、时间单位、fate、守恒公式、保留/删除标准和不建模项；重要决定同步到 `DECISIONS.md`。
- 生成旧源码依赖图和候选清理清单，但不删除。

验收：基线可恢复；设计、配置 schema、fate 和守恒口径无未决项。

### 阶段 1：配置、网格与 trace 编译器

- 实现版本化 YAML schema、profile 解析、resolved config 和 SHA 封装。
- 实现稀疏网格注册表以及合成、CSV、人口、M-Lab proxy 适配器。
- trace 编译与仿真消费完全分离；两算法臂只能消费同一份 trace。

验收：相同输入与 seed 产生字节一致 trace；源数据或配置变化必然改变 SHA；错序、重复 ID、无效网格、非法 deadline 和账本不一致均拒绝。

### 阶段 2：新离散事件内核

- 实现 GridEndpoint、Satellite、DataPacket、ControlPacket、AccessScheduler、DirectionalLink、HandoverManager 和 FateLedger。
- 完成有限队列、K 槽、共享 GSL、ISL 非抢占优先、BBM/MBB、几何变化、独立 GSL/ISL 中断和 deadline。
- 使用剩余比特记账处理速率、资源份额或链路状态改变，不用固定 timeout 掩盖中途变化。

验收：确定性微场景逐事件匹配手工结果；监控开关不改变事件顺序；无遗留资源请求、死锁或重复终态。

### 阶段 3：路由与学习算法迁移

- 先接入三类非学习基线和 Oracle，再迁移 C1/C3/C4/C5/C6/C7。
- 重建统一 observation contract、动作掩码和 `deliver` 动作。
- C1 使用自身和一跳已到达状态；C3–C7 使用相同 `vis_k` 缓存，差别只在表示/聚合和 AoI 处理。
- 删除 `true_ddqn`、M1/M2 等补丁开关，建立新 checkpoint family。

验收：无算法读取未来几何、真实全局队列或未到达控制信息；每个保留算法完成真实 TensorFlow 构建、一步训练、保存和重新加载。

### 阶段 4：平台接入与可操作性

- 改造现有实验编译、三角色审阅、授权、远程运行和 artifact manifest，使其绑定新 schema、trace SHA、代码 SHA 和随机流 manifest。
- 默认关闭仿真内绘图，改为离线分析。
- 保留 `tffunc + fast_train`，但在新状态结构上重新做逐位/容差等价 A/B；旧 2.09–5.78× 不能直接继承为新平台结论。
- `movement_interval=10s` 保留为语义基线；30/60s 作为独立敏感性 A/B，不当作无条件执行优化。
- 对 1/2/4/8/12 并发做 24 核、64 GiB cgroup 内 scaling，按吞吐、内存和 OOM 风险选择正式并发度。

验收：自然语言生成的 YAML 可由 schema 精确解释；dry-run 输出完整 resolved config；不存在静默回退或未收据化机制。

### 阶段 5：正式 VM 验收

依次执行最小、可诊断场景：

1. 静态几何直接上行—ISL—直接下行。
2. 默认 BBM 切换。
3. 双连接资源下的 MBB。
4. GSL 随机中断。
5. ISL 随机中断。
6. 控制包拥塞、延迟与 TTL 过期。
7. 数据 deadline。
8. 三类非学习基线及 C1/C3/C4/C5/C6/C7 的真实运行 smoke。

每次严格执行：

`编译 → cold-start 审阅 → satellite-DRL 审阅 → adversarial 审阅 → finalization → authorization → main 部署 → run-remote → 自然结束 → 收据核验`

验收必须同时满足：

- `natural_end=true`、`interrupted=false`；
- 配置、trace、代码和输入 SHA 一致；
- 请求机制确实初始化并在发送路径发生；
- `offered_bits = delivered_bits + terminal_loss_bits + in_system_bits_at_stop`；
- 每个数据包只有一个终态；
- 控制开销、AoI、过期和链路占用均可重算；
- retained algorithms 全部真实执行；
- 完整测试真实报告 passed/skipped/failed 数量；
- GitHub Actions 若仍受账单阻塞，只能标记“hosted CI blocked”，不得写成通过。

## 4. 清理、切换与删除门

VM 验收通过后，先把新 CLI 和新内核切为唯一正式入口，再生成逐路径 `cleanup-manifest`，每项记录路径、删除原因、替代实现、剩余引用扫描和恢复方式。只有用户逐路径批准后才执行 `git rm`。

预期删除范围：

- Gateway 类、Gateway 生成/汇聚/接收适配器、`linkSats2GTs` 和 Gateway→Gateway 数据路径。
- `Gateways.csv`、`inputRL*`、`GTs/num_gateways` 及仅服务旧入口的配置。
- Gateway 绑定的 traffic OD、burst、diurnal 运行时；其中有效逻辑已迁入 trace 编译器。
- `legacy` 切换模式、无条件全量断连重连逻辑。
- Q-Learning、C2、`dataRate/dataRateOG` 重复入口。
- MAPPO、CSR、旧 CVaR/MCP、path-credit、temporal/multistep、M3、线性奖励和旧 checkpoint 自动兼容代码。
- 大量 `SIM_*` 兼容别名、仿真内绘图以及 v1 不再使用的旧静态网页。
- 经无引用和数据来源核查确认无价值的旧图片、geoip、生成配置和脚本。

明确保留：

- 经表征测试确认正确的轨道、几何、ISL 和链路预算计算。
- 人口栅格、M-Lab 原始数据及其 provenance。
- 实验编译、三角色审阅、授权、远程执行、scheduler、receipt、manifest 和分析工具。
- 历史 `EXPERIMENTS/`、`ANALYSIS/`、Git 历史和 VM Results；不清理科研证据。
- MBB、随机中断和 AoI 等“机制思想”，但以新模块重实现，不保留旧单体补丁。

最终清理验收：

- 正式运行代码中没有 `Gateway`、`Gateways.csv`、旧流量入口或旧算法开关引用。
- [`SimulationRL.py`](/Users/lge/Desktop/LEO-Research-Workspace/CODE/SimulationRL.py) 在依赖迁移完成后整体删除，不保留转发壳。
- 新平台完整本地测试和 VM smoke 再跑一遍，结果闭环。
- 更新 [`NOTES.md`](/Users/lge/Desktop/LEO-Research-Workspace/NOTES.md)、设计回执和删除回执；工作区 clean，提交、push，并部署最终 main。

## 5. 报告口径

- 阶段 1–4 通过：只能说“本地实现并通过对应测试”。
- 阶段 5 通过：可以说“新平台已在 VM 完成端到端机制验收”。
- 阶段 5 前不得声称卫星直连已经替代正式 Gateway 路径。
- 平台 smoke、守恒和机制生效不证明算法更优。
- MBB、GE、M-Lab proxy 和系统级链路预算都必须保留抽象与校准边界。
- 算法效果、速度收益和机制收益必须另建同 trace、同 seed、同资源条件的正式 A/B 实验。
