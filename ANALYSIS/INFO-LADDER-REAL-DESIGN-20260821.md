# 真实信息阶梯：F0/F1 诊断锚点（2026-08-21）

## 目的

R02/R03 已经证明 200 Mbps M-Lab measurement-proxy 压力负载会稳定暴露
holding overflow、在系统积压和长尾等待，但还不能回答“差距来自信息不足，
还是来自决策能力”。本文件冻结下一步最小诊断对照；它不是论文结论，也
不是把内核真值自动喂给学习器的声明。

## 两个新增锚点

| 名称 | 配置值 | 决策时允许使用的信息 | 明确禁止 |
|---|---|---|---|
| F0 queue/direction | `routing.policy=info_queue` | 当前卫星自己的各方向 ISL 队列；已到达且未过期的目的地服务广告；静态当前拓扑；路径剩余跳数 | 远端当前队列、远端当前距离/速率、未来几何、oracle serving-sat 真值 |
| F1 distance/rate/availability | `routing.policy=info_physical` | F0 全部信息；当前第一跳的斜距、几何可用性和由当前斜距推导的速率；当前卫星自己的第一跳队列 | 远端当前队列/物理值、未来几何、oracle 真值 |

F0/F1 是确定性路由诊断锚点，不是 DDQN/GAT/MPNN 的观测向量。当前学习
向量仍由 `routing.contract` 决定；`--decision-log` 中的
`candidate_truth` 仍标记为 `truth_audit_not_learner_tensor`。因此不能把
F1 跑通写成“学习器已经看到了距离和速率”。

## 设计与配对

第一轮只改变 `routing.policy`，固定 R03 已验证的 200 Mbps pressure 合同：
140 星、20 s、M-Lab 多 OD + 8--16 s 2× burst、MCS、1 s topology
recompute、相同 trace identity、相同 seed。`hop` 是现有方向/跳数锚点，
F0/F1 是新增对照。每个 policy 至少 seed 7 和 11；同一 seed 内使用同一
trace 和同一 config 之外的所有字段。

主要输出按原始 ledger 重算：按时交付/交付率、holding overflow、
`IN_SYSTEM_AT_STOP`、`NO_ROUTE`、最大及逐向链路利用率、queue/tx/prop/holding
四段等待。F0→F1 的差值只能解释为“加入第一跳物理信息后的诊断变化”；
它不是算法 superiority 或因果拥塞控制效果。

## 负对照与停止条件

正式授权前必须保留两类负对照设计：

1. F0 中对同一时刻的本地方向队列做可复现置换，验证提升不是方向标签或
   固定 tie-break 造成；
2. F1 中对第一跳速率/距离做固定或置换版本，验证提升不是增加一个参数
   向量就自动发生。

如果任一负对照显示“没有物理字段也得到同样提升”，回到信息映射审计，
不扩大训练矩阵。只有 candidate truth、policy 输出、ledger 指标和
claim boundary 全部可重算，才进入 V2 编译/独立审阅/授权。

## 当前状态

- F0/F1 路由锚点已实现并有 routing/config 定向测试；F0 正式矩阵已完成
  编译、三方复核、授权、合入、同 SHA VM 部署和 4 个串行实跑。
- 合入主线为 `c34fac937e865cb2f5543bacba2223eb4f34477e`；部署 receipt
  SHA=`2d5535cea66aa3bac4065ace991d5cccdced5d3813df72902947cd3bf6378ce0`，
  source tree SHA=`1d4830e0a8f4850d333dce5f4d01fdd50e98ee369f8e26d6c0f225d9eedcd17a`，
  authorization SHA=`69019af696ff81e7ebeb3e35a3a3527c9590082de1e00beae11ef659e2181d77`。
- 4/4 cells 均 `success`、`natural_end=true`、守恒通过、receipt verify 为
  `verified`；治理回执 `research_eligible=true`。运行目录中的本地
  `receipt.json` 保持 `research_eligible=false` 是设计语义：本地工件不能
  自行授予研究资格，资格由外部治理回执授予。
- seed 7 两臂交付率均为 `0.4291118717`（2,382 delivered）；seed 11
  两臂均为 `0.4408871400`（2,465 delivered）。V2 分析为 `VERIFIED`，
  `verified_runs=4`，manifest SHA=`a5bba6f34b66700bf9e356723aaa615b1c8040b43914de0ea064371b4b1fd4f2`，
  `info_queue_minus_hop` 差值为 `[0.0, 0.0]`；持久化 verifier 返回
  `ok=True, errors=[]`。
- 这只是“当前压力合同下 F0 的诊断结果”，不是论文结论，也不能解释为
  队列信息没有价值。路线事件审计显示它确实改变了少量决策：seed 7
  有 3/352 个出现 ISL 路径差异，seed 11 有 4/401 个；但交付率和主要
  终态没有改变。下一步先记录该路线/队列诊断，再做 F1；不启动学习长训。

## 2026-08-22：INFO-LADDER F1 R02 已完成三方复核、授权、VM 实跑与 V2 重算

- R02 比较 `info_queue`（F0）与 `info_physical`（F1），只改变
  `routing.policy`，trace seed=7/11，各一对 non-learning cell；M-Lab
  输入仍是 measurement proxy，不称真实运营商流量。
- 三方独立复核均 PASS，finalization=`ACCEPTED`；PR #138 合入后，
  authorization PR #139 合入。执行主线 exact SHA=
  `fead4a594a916258b1063ea63621b58076a60b51`，部署 receipt SHA=
  `636a535ce44824998b4e9fd3cad7dc268f76f4321ce1b47a5e701e737aca3233`，
  source tree SHA=`39da2af8a3a499675f487ea93dff8b1210080d3762b9a28033eecf500a0a47f6`，
  authorization SHA=`4d896398c475f461fc8402301fbc1f8de160cb76051825f1abbfe6eea92ad9cc`。
- 4/4 cells 严格串行自然结束，exit=0、`conservation_ok=true`、receipt
  verify 全部为 `verified`，治理回执全部 `research_eligible=true`。运行时
  观察到单进程约满 1 个 CPU 核，RSS 约 556--657 MB；这是工程观察值，
  不是正式资源 profile。
- V2 分析返回 `VERIFIED`、`verified_runs=4`；正确的持久化 verifier（传入
  `analysis-manifest.json`）返回 `(True, [])`。analysis-manifest SHA=
  `86133383ae3b18fdcc6990aeb938a22bcb54893540781e625d277335a4c0d491`，
  summary SHA=`d166e19044028233a81d8b9f31ddc9b27e90b57380fb24c633968b707fd57ae6`。
- 主指标 `delivery_rate` 的 `info_physical - info_queue` paired differences
  为 `[0.0, 0.0]`，均值 `0.0`。路线事件审计表明 F1 并非没有改变决策：
  seed 7 有 `125/352=0.3551` 的包路径不同，seed 11 有
  `146/401=0.3641`；但两 seed 的包命运计数完全一致：seed 7
  delivered=2382、access_rejected=2597、holding_overflow=167、
  in_system=405；seed 11 delivered=2465、access_rejected=2557、
  holding_overflow=180、in_system=389。
- 解释边界：在这个固定 20 s、200 Mbps M-Lab burst 压力合同下，F1 改变了
  约三分之一有 ISL 路径的包的路线，但当前接入/持有瓶颈使交付率和终态
  没变。这是可复核的诊断，不是“物理信息无价值”、不是因果拥塞控制效果，
  也不是论文 superiority 结果。下一步应转向队列/利用率逐向差异与负对照，
  再进入学习器观测或 Q0 归因实验。
