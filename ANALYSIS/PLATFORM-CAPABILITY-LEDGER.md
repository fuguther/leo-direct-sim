# leo_sim V2 平台能力账本

> CURRENT；最后核验：2026-08-20。本文维护现行结论；旧平台逐行证据见 `LEGACY-DESIGN-AUDIT-20260819.md`，历史迁移决策见 `MIGRATION-BACKLOG-20260816.md`。

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
| 距离→SNR/MCS→速率 | 有 | **已合入当前 main `66be0ad...`**；本地/CI 绿，VM 工程 smoke 已跑 constant 路径 | BLOCKER-P0（正式对照证据仍需） | 用旧数值表征与 VM MCS 配置完成服务时长、观测和 receipt 对照 |
| 动态 ISL 对端重匹配 | 有 | **已合入当前 main `66be0ad...`**；退役排空、单收发器、holding 语义有回归 | BLOCKER-P0（长窗正式证据仍需） | 在 VM 长时窗验证重匹配/在途包归属，不再阻塞基础工程 smoke |
| 未来端点惰性激活 | 旧行为曾泄漏 | V2 #28 已合入 main | 已关闭 | 保留回归 |
| 接入 FIFO / downlink 恢复 | 旧语义参照 | V2 #26/#25 已合入 main | 已关闭 | 保留回归 |
| 奖励无正循环/物理目标一致 | 旧平台奖励族复杂 | 专家审阅 A1 未正式关闭；Q0 不得以 shaped reward 判最优 | BLOCKER-P0 | 构造正循环反例；冻结物理字典序目标 |
| 动作 mask 与观测信息集一致 | 旧/新均需审 | #62 已修已知 cache-hop 旁路，独立冷审与不可区分反例通过 | 已关闭已知 blocker | 保留 C1/C3 与远端传播/队列指标回归；最终冻结平台继续找未知旁路 |
| 正式证据链 | V2 目标更强 | V2 矩阵 Stage 1 已合入；artifact→指标重算→paired analysis→claim Stage 2 仍未完成 | BLOCKER-P0 | 复用严格重验原则，完成 V2 结果分析与 claim gate；禁止以 generic 绿冒充 V2 完成 |
| Q0 当前全局快照 | 无等价严格接口 | snapshot 已进 main | Q0 前置已完成 | 保留只读、因果和版本测试 |
| Q0 计划注入与执行归因 | 无 | 候选分支存在，审阅未通过 | BLOCKER-THEORY | action_id 贯穿执行；receipt 持久化 verdict/errors/executed；不阻塞 E0/pilot |
| Q0-I/Q0-F tiny | 无统一实现 | Q0-I 候选；Q0-F 未完成 | BLOCKER-THEORY | 独立穷举/第二算法交叉验证；从真实诊断窗口抽 tiny |
| 真实流量 provenance、多 OD、突发 | 有多种模式 | V2 已有 CSV 多 OD、M-Lab/人口代理及 burst window；缺统一来源/单位/映射合同 | BLOCKER-DIAG | 绑定源 hash、source type、许可/时间/字段、OD/时间映射和 offered-load 重算；代理不得冒充原始 packet trace |
| 逐向链路利用率可重算 | 聚合统计较多 | V2 有 occupied seconds/queue-area 聚合，但无可用容量分母与逐向/逐窗正式事件 | BLOCKER-DIAG | 加 opt-in per-link interval ledger，按 rate×available-time 与 served bits 重算并绑定 receipt |
| per-action 斜距/速率/方向特征 | RAAC 有 4×9 action_feats | V2 内部路由能访问相关量，但 decision sink 无逐动作等价物 | BLOCKER-THEORY | INFO-LADDER 前加入 distance/rate/availability/observed_at/source；不默认给所有臂 |
| 逐字段 AoI | 旧有定时观测/年龄统计 | V2 是 cache-entry 级 age，未有字段级 generated/received/source age | BLOCKER-THEORY | AGE-LADDER 前完成并做 shuffle/fixed-fresh 负对照 |
| 每包 queue/tx/prop 分解 | 有 | V2 可重算 delivered E2E，但现有事件不足以离线重算三段 | BLOCKER-DIAG | 加 per-packet queue enter、service start/end、prop start/arrival 与 link ID，校验分段和 |
| replay buffer 持久化 | 有 | V2 只有 online model checkpoint；replay/optimizer/target/RNG 未持久化 | BLOCKER-LONGTRAIN | 正式长训前做中断续训 vs 不间断训练等价验收，绑定 schema/SHA/config |
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
