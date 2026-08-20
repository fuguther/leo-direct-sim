# leo_sim V2 平台能力账本

> CURRENT；最后核验：2026-08-21，runtime main `4990e61`。本文只记录已经有当前代码、测试或 VM 证据支撑的状态；旧平台逐行证据见 `LEGACY-DESIGN-AUDIT-20260819.md`，历史迁移决策见 `MIGRATION-BACKLOG-20260816.md`。

## 判定与优先级

- `BLOCKER-P0`：不关闭就不能相信平台核心语义或 V2 正式证据链。
- `BLOCKER-DIAG`：不关闭就不能把真实流量拥塞/利用率诊断写成论文证据。
- `BLOCKER-THEORY`：不关闭就不能完成信息 vs 决策归因或冻结新方案。
- `BLOCKER-LONGTRAIN`：不关闭就不能可信恢复昂贵训练或启动正式新方案长训。
- `CONDITIONAL`：只在诊断表明确需要该机制时进入正式矩阵。
- `INTENTIONAL`：有意不迁移或已有等价表达，必须声明边界。

## 当前能力对照

| 能力 | 旧平台 | V2 当前状态 | 优先级 | 现行处置 |
|---|---|---|---|---|
| 距离→SNR/MCS→速率 | 有 | **代码已合入、测试通过**；VM 只完成基础 smoke，尚未完成旧平台 MCS 表征与 V2 的 VM 对照实验 | BLOCKER-P0 | 在 VM 固定几何/距离样例上完成旧新速率、服务时长、观测和 receipt 对照 |
| 动态 ISL 对端重匹配 | 有 | **代码已合入、退役/在途/holding 测试通过**；尚缺长时间 VM 重匹配验证 | BLOCKER-P0 | 在 VM 长窗验证重匹配、退役链路、在途包归属和等待队列 |
| 包守恒、FIFO、等待、在途语义 | 有 | 基础内核与回归测试已有，VM 基础 smoke 守恒通过；正式结果中的持久化分析和长窗覆盖尚未完成 | BLOCKER-P0 | 用长窗、多 OD、失败/积压/在途负对照完成 VM 与 receipt 验收 |
| 未来端点惰性激活 | 旧行为曾泄漏 | V2 #28 已合入 main | 已关闭 | 保留回归 |
| 接入 FIFO / downlink 恢复 | 旧语义参照 | V2 #26/#25 已合入 main | 已关闭 | 保留回归 |
| 奖励无正循环/物理目标一致 | 旧平台奖励族复杂 | **R1-A1 仍是 blocker**；已有针对额外跳数正回报的修复/回归，但尚未完成独立终审和正式学习语义冻结 | BLOCKER-THEORY | 先关闭 R1-A1，再允许学习算法正式实验；Q0 不得以 shaped reward 判最优 |
| 动作 mask 与观测信息集一致 | 旧/新均需审 | 已修复明确的 cache-hop 偷看问题；仍缺逐动作物理特征和逐字段 AoI，不能宣称整体信息公平已完成 | BLOCKER-THEORY | 保留已通过的旁路回归；完成 per-action distance/rate/availability 与 field-age 合同 |
| 正式证据链 | V2 目标更强 | **矩阵编译/授权 Stage 1 已完成**；artifact→指标重算→配对分析→claim 的真实授权闭环仍缺，当前没有正式 cohort 产物 | BLOCKER-P0 | 用当前 main 跑真实授权 cohort，核验持久化 analysis manifest、paired output 和 claim gate；禁止用 fixture 冒充论文数据 |
| Q0 当前全局快照 | 无等价严格接口 | snapshot 已进 main | Q0 前置已完成 | 保留只读、因果和版本测试 |
| Q0 计划注入与执行归因 | 无 | 候选分支存在但审阅未通过，尚未形成可用于正式结论的执行归因闭环 | BLOCKER-THEORY | action_id 贯穿执行；receipt 持久化 verdict/errors/executed；不阻塞工程 smoke，但阻塞 Q0 结论 |
| Q0-I/Q0-F tiny | 无统一实现 | Q0-I/Q0-F tiny 尚未完成可接受的交叉验证闭环 | BLOCKER-THEORY | 独立穷举/第二算法交叉验证；从真实诊断窗口抽 tiny |
| 真实流量 provenance、多 OD、突发 | 有多种模式 | M-Lab 文件、source/SHA、字段/小时覆盖、OD 映射和 burst 变换已合入；M-Lab/人口仍是代理，当前 main 尚未完成 VM receipt/授权验收；小时用于覆盖审计而非逐小时强度重放 | BLOCKER-DIAG | 用当前 SHA 的 VM 多 OD/突发样本完成 offered-load 和 receipt 验收；代理不得冒充原始 packet trace |
| 逐向链路利用率可重算 | 聚合统计较多 | 有服务窗容量/served bits 及本地 queue/tx/prop 重算；**分母仍是已记录服务窗容量，不是几何 available capacity，正式 VM 证据尚未完成** | BLOCKER-DIAG | 明确 available-capacity 分母，按方向/窗口持久化并做独立重算与负对照 |
| per-action 斜距/速率/方向特征 | RAAC 有 4×9 action_feats | V2 内部路由能访问相关量，但 decision sink 无逐动作等价物 | BLOCKER-THEORY | INFO-LADDER 前加入 distance/rate/availability/observed_at/source；不默认给所有臂 |
| 逐字段 AoI | 旧有定时观测/年龄统计 | V2 是 cache-entry 级 age，未有字段级 generated/received/source age | BLOCKER-THEORY | AGE-LADDER 前完成并做 shuffle/fixed-fresh 负对照 |
| 每包 queue/tx/prop 分解 | 有 | 内部事件和本地重算已有；receipt 已修复合法 horizon in-flight 传播的重算，正式 VM artifact、三段和校验及失败/积压覆盖仍未完成 | BLOCKER-DIAG | 在正式 receipt/analysis 中逐包持久化 queue/tx/prop/e2e，并完成三段和 gate |
| replay buffer 持久化 | 有 | V2 只有 online model checkpoint；replay、optimizer、target network、RNG 尚未完整持久化 | BLOCKER-LONGTRAIN | 正式长训前做中断续训 vs 不间断训练等价验收，绑定 schema/SHA/config |
| 学习算法 VM smoke | 有 | 尚未完成当前 main 上的训练/评估 VM smoke；目前只有非学习/内核工程 smoke | BLOCKER-P0（学习实验） | R1-A1 关闭后，至少完成一个训练和一个评估臂的自然结束、checkpoint 血缘和 receipt 验收 |
| 多步/TD-λ/temporal | 有 | V2 只有设计稿 | CONDITIONAL | 诊断若指向信用分配问题，再作为研究臂 |
| path-credit | 有 | V2 未接运行时 | CONDITIONAL | 诊断若指向端到端信用分配，再立单独研究臂 |
| 每星模型、FL、CKA | 有 | V2 单共享策略 | CONDITIONAL | 只有分布式异质性成为主机制时需要 |
| 队列 Δq/EMA 趋势 | 有 | V2 主要是瞬时队列/cache age | CONDITIONAL | 作为拥塞趋势候选信息，只在 DIAG/Q0 支持时进入新方案 |
| ε 按决策步/GT 数、早停 | 有 | V2 按仿真时间，无 stopLoss | CONDITIONAL | 先由 pilot 评估训练动力学，不照搬 |
| h2 命名走廊 | 有 | V2 无同名模式，CSV 可表达 | INTENTIONAL | 用 CSV 复现并记录 provenance |
| FSO、完整 Doppler/ARQ/天线 | 有限或实验性 | V2 不覆盖 | INTENTIONAL/CONDITIONAL | 有校准数据且诊断表明会改变拥塞结论时才实现 |
| GE 中断、优先级、流量模式 | 有 | V2 已有等价或更强实现 | 已覆盖 | 维持表征/等价验收 |
| receipt、守恒、artifact 治理 | 较弱 | V2 fail-loud、字段权威、hash 链更强 | V2 优势 | 修复分析入口后维持为核心能力 |

## 研究高保真上限的边界

“顶点”按以下顺序定义，而不是按代码行数：

1. **结论有效性**：会改变主结论的语义和证据链先完整。
2. **可反驳性**：每个提升有负对照、等价基线或极端反例。
3. **可校准性**：参数能对应公开/实测数据；无法校准的高级模型明确列局限。
4. **可扩展性**：tiny 精确验证与大规模近似分开，不能用可扩展性换掉正确性标签。
5. **可复现性**：代码 SHA、部署 SHA、原始产物、分析代码和 claim 可反溯。

## 尚不能下的结论

- 不能说旧平台优点已全部枚举：D1/D2 已对齐，但当前仍只有局部交叉审计，不满足最终三轮门禁。
- 不能说 V2 已经优于旧平台：治理链更强是局部事实，物理/训练/测量仍有明确缺口。
- 不能把未校准的物理细节数量当作仿真真实性。
