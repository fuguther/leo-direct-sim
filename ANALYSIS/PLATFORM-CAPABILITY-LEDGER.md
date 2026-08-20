# leo_sim V2 平台能力账本

> CURRENT；最后核验：2026-08-20。本文维护现行结论；旧平台逐行证据见 `LEGACY-DESIGN-AUDIT-20260819.md`，历史迁移决策见 `MIGRATION-BACKLOG-20260816.md`。

## 判定与优先级

- `BLOCKER-A`：不关闭就不能宣布平台可跑正式实验。
- `CLAIM-GATED`：只有论文/实验要声明该能力时才成为前置。
- `CEILING`：提高研究平台上限，但不阻塞首批实验。
- `INTENTIONAL`：有意不迁移或已有等价表达，必须声明边界。

## 当前能力对照

| 能力 | 旧平台 | V2 当前状态 | 优先级 | 现行处置 |
|---|---|---|---|---|
| 距离→SNR/MCS→速率 | 有 | PR #55 候选，未进 main | BLOCKER-A | 合入后做旧数值表征、服务时长、观测与 receipt 对照 |
| 动态 ISL 对端重匹配 | 有 | PR #56 候选，未进 main | BLOCKER-A | 合入；5 秒窗影响小，但长窗语义必须正确 |
| 未来端点惰性激活 | 旧行为曾泄漏 | V2 #28 已合入 main | 已关闭 | 保留回归 |
| 接入 FIFO / downlink 恢复 | 旧语义参照 | V2 #26/#25 已合入 main | 已关闭 | 保留回归 |
| 奖励无正循环/物理目标一致 | 旧平台奖励族复杂 | 专家审阅 A1 未正式关闭；Q0 不得以 shaped reward 判最优 | BLOCKER-A | 构造正循环反例；冻结物理字典序目标 |
| 动作 mask 与观测信息集一致 | 旧/新均需审 | 专家审阅 A2 指出 mask 可能泄漏 obs_hops 外信息 | BLOCKER-A | 同一信息合同生成 observation 与 mask；做信息不可区分反例 |
| 正式证据链 | V2 目标更强 | 当前硬绑定分析文件/旧 request 缺失，CI 未覆盖全链 | BLOCKER-A | 恢复持久化分析器、fixture 和 CI 门 |
| Q0 当前全局快照 | 无等价严格接口 | snapshot 已进 main | Q0 前置已完成 | 保留只读、因果和版本测试 |
| Q0 计划注入与执行归因 | 无 | 候选分支存在，审阅未通过 | BLOCKER-A | action_id 贯穿执行；receipt 持久化 verdict/errors/executed |
| Q0-I/Q0-F tiny | 无统一实现 | Q0-I 候选；Q0-F 未完成 | BLOCKER-A（按用户流程） | 独立穷举/第二算法交叉验证 |
| per-action 斜距/速率/方向特征 | RAAC 有 4×9 action_feats | V2 无等价逐动作物理特征 | CLAIM-GATED | EXP2b 单独消融，不默认塞入所有臂 |
| 逐字段 AoI | 旧有定时观测/年龄统计 | V2 有传播缓存，显式逐字段 age 研究层未完成 | CLAIM-GATED | EXP3 前完成并做 shuffle/fixed-fresh 负对照 |
| 每包 queue/tx/prop 分解 | 有 | V2 现有事件不足以离线重算 | CLAIM-GATED | 论文若声明时延组成，先加 opt-in 事件与分析器 |
| replay buffer 持久化 | 有 | V2 只有模型 checkpoint | CEILING（已 defer） | 不自动迁移；pilot 若证明失败成本不可接受，再由用户重新拍板 |
| 多步/TD-λ/temporal | 有 | V2 只有设计稿 | CEILING | 作为信用分配研究臂，不混入首批基线 |
| path-credit | 有 | V2 未接运行时 | CEILING | 单独研究臂 |
| 每星模型、FL、CKA | 有 | V2 单共享策略 | CEILING | 只有分布式学习 claim 需要 |
| 队列 Δq/EMA 趋势 | 有 | V2 主要是瞬时队列/AoI | CEILING（未批准迁移） | 只保留为拥塞趋势候选臂，需要时重新拍板 |
| ε 按决策步/GT 数、早停 | 有 | V2 按仿真时间，无 stopLoss | CEILING | 先由 pilot 评估训练动力学，不照搬 |
| h2 命名走廊 | 有 | V2 无同名模式，CSV 可表达 | INTENTIONAL | 用 CSV 复现并记录 provenance |
| FSO、完整 Doppler/ARQ/天线 | 有限或实验性 | V2 不覆盖 | INTENTIONAL/CEILING | 有校准数据和对应 claim 时才实现 |
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

- 不能说旧平台优点已全部枚举：当前只有两轮本地/局部交叉审计，不满足最终三轮门禁。
- 不能说 V2 已经优于旧平台：治理链更强是局部事实，物理/训练/测量仍有明确缺口。
- 不能把未校准的物理细节数量当作仿真真实性。
