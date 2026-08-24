# EXP-20260824-ISL-BANDWIDTH-PILOT-R03 结果与 claim 审阅

> **EVIDENCE-SNAPSHOT**：绑定 exact main
> `0280de3ba0e27551bc7a737a028f5154743051ce`、analysis manifest SHA
> `5ee795b366b87977cb27bb2e4e90504791b4c8273592b687c8face1e416429d7`
> 与 pressure classification SHA
> `c0075a3647f4f821bf043e734a6c2ffec9dd8984e4da82e4d0f5a477b56cf5b8`。
> 原始 `CODE/Results/` 不入库；本文件不能脱离 manifest、raw artifact hashes、
> external launch witnesses 和 receipt verification 单独作为结果来源。

## 核证事实

- 5 MHz 与 2 MHz 两个授权 cell 均在同一 clean-main 部署上自然结束，退出码为 0，
  包守恒、governance、外部启动见证和 VM 原始 Python 3.11.15 环境 receipt verification
  均通过；V2 persisted analysis 再验证返回 `ok=true`、`errors=[]`。
- 两臂使用同一实际 trace、seed 7、确定性 hop 路由、拓扑、接入、业务、发包、观测和
  排空合同；声明的唯一主动改变量为 `links.rf_isl.bandwidth_hz` 的 5 MHz→2 MHz。
  bandwidth 同时通过噪声、SNR、MCS 和控制包服务时间产生物理后果，因此不是纯容量乘数。
- 全运行期最大有向 ISL 利用率为 `0.15252027036759927`→
  `0.3813006759189982`，配对差为 `0.22878040555139892`，`n_pairs=1`。
  这项全程聚合指标只描述总体变化；压力裁决使用预注册的一秒时间窗与同链路排队重叠证据。
- 5 MHz 臂没有合格压力 episode。2 MHz 臂在三条有向 ISL 上形成合格 episode：
  `isl:147:167`、`isl:167:187`、`isl:222:242`。其中前两条在 23--27/28 s
  连续 4/5 个一秒窗达到约 `0.91866` 利用率；第三条在 13--17 s 连续 4 个窗达到
  `0.85751`--`0.91866`。这些 episode 内均有同链路匹配排队，最大等待分别约
  `5.130 s`、`0.336 s`、`0.784 s`，超过冻结的 `0.1 s` 门槛；episode queue area
  也均超过 `100000 bit-s`。
- 两臂数据命运完全相同：1,299 offered、1,295 delivered、4 `NO_ROUTE`；接入 grants
  均为 59，control failure counters 均为 0，MCS zero-rate holds 均为 0，
  `ISL_QUEUE_OVERFLOW` 均为 0。两臂停止时均无在途数据包，6,863 个 ISL 队列条目
  均成功匹配，无未匹配条目。因此当前压力信号不是由接入差异、NO_ROUTE 增长、
  zero-rate、控制丢失、溢出或未排空造成。
- 冻结分类器在重新核验 persisted analysis 后返回 `PRESSURE_CANDIDATE`：5 MHz
  是本场景的无压力相邻对照，2 MHz 是单 seed 的工程压力候选。

## 当前裁决

当前最强可支持表述是：在这个固定场景和 seed 7 下，5 MHz 臂没有出现满足预注册定义的
局部 ISL 压力 episode，而 2 MHz 臂在三条有向 ISL 上出现了“连续高利用率与同链路、
同时段排队”共同成立的 episode；两臂物理有效、完成排空，且包命运与接入结果相同。
因此 5--2 MHz 构成一个工程 onset 候选区间。

不能写成：2 MHz 是普适拥塞阈值、压力在所有随机流量映射下稳定、带宽具有纯容量因果效应、
信息已经有价值、强化学习优于确定性算法、新算法有效、Q0 最优或已有论文统计证据。三条候选
链路和具体时间段来自单一 seed；4 个两臂共有的 `NO_ROUTE` 仍是独立的历史边界，虽不解释
本轮臂间差异，也不能被改写为拥塞结果。

## 执行事件与平台边界

- canonical 远程启动器第一次准备 2 MHz 前驱门时使用了未激活的系统 Python，因缺少
  TensorFlow 在准备阶段 fail-closed；仿真没有启动，也没有生成结果目录。随后通过显式绑定
  已验证的正式 VM Python，并让前驱验证仍在部署代码与同一授权上执行，正式 2 MHz 运行成功。
- 该事件没有污染两组正式结果，但暴露了远程启动器默认解释器与正式环境激活不一致的可用性
  缺口。核心证据链已经跑通；默认启动路径仍需单独修复和回归，不能把临时显式绑定当作
  平台完全没有遗留问题。

## 下一步与停止条件

- 按冻结动作停止继续降低 bandwidth，不运行 1 MHz，也不把本轮扩成剂量响应曲线。
- 下一工作单元先预注册 5 MHz/2 MHz 相邻两臂的两个新增 trace seeds，建议使用未看结果的
  固定 seeds 11 和 19，使总计三个 seeds；每个 seed 内严格配对，仍只改 bandwidth，沿用
  同一压力判据和物理/排空停止条件。若任一新增 seed 物理无效、未排空、5 MHz 已有压力，
  或 2 MHz 无压力，必须按各自分支报告，不能以多数票掩盖不稳定性。
- 只有新增 seeds 对 5 MHz 无压力、2 MHz 有压力的方向提供一致支持后，才能把这个场景
  冻结为后续 Q0-F/Q0-I 与信息裁剪的压力测试床。即使三 seed 一致，也先比较同信息条件下
  的确定性基线，再训练强化学习；不得直接跳到“新算法”。
- 远程启动器默认解释器缺口应作为独立小修复处理：先加能复现未激活环境的回归，再修改准备
  与 child-start 使用同一显式环境，完成独立审阅和 clean-main 部署后才作为平台闭环。

## 审阅状态

- Codex 原始结果、receipt、外部见证、持久化分析与冻结分类复核：完成。
- 单 seed 工程判断：`PRESSURE_CANDIDATE`，不是 paper-ready claim。
- 新增 seeds 11/19 与启动器修复路线：当前为待独立挑刺的下一步方案，尚未编译、审阅、
  授权或运行。
