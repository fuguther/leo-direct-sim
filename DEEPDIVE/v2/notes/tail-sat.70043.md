# 摘要级笔记：10.1002/sat.70043
全文不可取得=是（Wiley 403；仅摘要可得）

**标题**: Path-Based Deep Reinforcement Learning for On-Board Routing in Satellite Constellation Networks

## 七要素
- 研究问题：重型负载下互联卫星星座网络中，如何在星间链路上优化流量分布以满足 QoS、提升宽带服务的资源利用效率。
- 方法/框架：基于深度强化学习的自适应流量工程框架；路径决策（path-based）策略——集中式 agent 将到达的流请求分配到候选路径集合；近似求解多商品流（multicommodity flow）问题，计算复杂度较低。
- 场景/数据：卫星星座网络（星间链路）；不同候选路径集合与流量模式的多种场景。
- 评估指标：摘要未披露具体指标数值（以性能对比形式评估）。
- 主要结果：在多种场景下优于最先进的基于规则的基准；量化了候选路径集合与流量模式对性能的影响；计算复杂度低，适合星上处理受限的在轨网络控制，可集成入 SDN 控制器逻辑。
- 局限：集中式 agent（依赖集中控制/SDN 架构）；摘要未披露训练开销与可扩展性上限。
- 可复用资产：path-based 决策+候选路径集的 MDP 建模思路；与规则基准的对比协议。

## RL 领域块
- 算法类型：DRL，路径级（path-based）决策
- 状态/动作/奖励设计：动作=将流请求映射到候选路径；状态/奖励细节摘要未披露
- 训练/部署方式：集中式训练的 agent，面向星上/在轨部署（处理受限）与 SDN 控制器集成
- 与基线对比：state-of-the-art 规则型基准

## 摘要引用
> [abstract] "Our approach employs a path‐based decision‐making strategy, using a centralized agent to distribute incoming flow requests on a set of candidate paths."
> [abstract] "This method approximates optimal solutions to the multicommodity flow problem with relatively low computational complexity, making it suitable for in‐space network control despite on‐board processing limitations."
> [abstract] "We quantify the impact on performance of different candidate path sets and traffic patterns."

## 与选题空间的关系（摘要级-低置信）
与"LEO 星座 DRL 路由"高度相关：提供了 path-based/候选路径集的建模范式与星上部署约束论证，可作为方法设计参照与必比基准来源；因未读全文，具体网络规模、奖励函数与泛化性未知。