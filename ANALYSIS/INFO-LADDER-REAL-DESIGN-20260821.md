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

- F0/F1 路由锚点已实现并有 routing/config 定向测试；相关全量测试为
  `554 passed, 1 skipped`（提交前仍需在最终合并 SHA 重跑）。
- 尚未编译、审阅、授权或在 VM 执行 INFO-LADDER；没有任何 F0/F1 数值结果。
- 下一工作单元是为上述配对和负对照生成正式 request/matrix，而不是直接
  启动学习长训。
