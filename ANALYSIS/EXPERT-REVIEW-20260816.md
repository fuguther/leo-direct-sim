# 外部专家审阅合并（2026-08-16/17，6 路）

> 来源：E1 网络架构×2、E2 路由/RL×2、E3 验证/工程×2（GPT 网页端独立审阅，候选证据）。
> 处置状态：✔ 已修 / 🔧 待修（低风险可自主）/ ⚠ 需拍板（语义/设计）/ 📋 已列计划。
> 全文证据在 /tmp/expert_*.txt（本地留痕），关键项附仓库行号。

## A. 威胁研究结论（高优先）

| # | 发现 | 严重度 | 来源 | 处置 |
|---|---|---|---|---|
| A1 | **正奖励绕路漏洞**：转发奖励 (0,20]×γ^hops、到达 50、失败 0、无距离/时延/跳数成本 → 多走空闲跳可获更高累计回报 | blocking | E2×2 | ⚠ 奖励塑形需拍板（加跳数/时延成本或 shaping） |
| A2 | **动作掩码信息侧信道**：候选由 vis_k=12 完整缓存+静态图可达性生成，观测仅 obs_hops=2 → 掩码泄露观测外信息 | blocking | E2 独立、E3 | ⚠ 目标发现应与观测同一信息集 |
| A3 | **因果泄漏（未来端点）**：kernel 用全时域 trace 建全部 endpoints，未来端点提前参与槽位预置/控制广告/观测分母 | blocking | E3×2 | 🔧 改为按活跃集/惰性构建（需对照实验） |
| A4 | **确定性不 fail-closed**：enable_op_determinism 失败仅记字符串，receipt 接受失败串，platform_check 不要求 True | major | E3×2 | ✔ 已修（见 PR 24） |

## B. 建模真实性（E1 网络架构）

| # | 发现 | 严重度 | 处置 |
|---|---|---|---|
| B1 | Walker 简化：无 F 相位/偏心率/星历；RAAN 等间隔+同 idx 同相位 → 结论限特定星座 | major | 📋 论文限制节；小时/天级实验需 SGP4 |
| B2 | 极区/接缝缺失：98.6° 近极轨 E/W 跨面链路无极区断开/重建、无天线转向约束 | major | 📋 建模待办 |
| B3 | 固定速率+链路预算未集成：6000km 旧 MCS=0 vs 新 1Gbps → 可达路径/拥塞位置失真 | major | 📋 B5 已列（MCS 表待拍板） |
| B4 | 无 Doppler/指向/真实信道/ARQ：几何可见=可用且恒速，高估边缘 GSL/跨面 ISL；无 ARQ 使链路失效=网络层丢包 | major | 📋 论文限制节；ARQ 属协议假设需声明 |
| B5 | K 槽≠波束/时频资源模型；接入抽象反向改变路由路径 | major | 📋 声明接入抽象边界 |
| B6 | **MBB 积压包语义偏差**：切换把未分配积压包钉在旧链；dual_connect 不限制为两链（retiring_link_limit=4） | major | 🔧 需对照实验后修（手over 承重） |
| B7 | 控制包固定 8000 bit 与 payload 大小脱钩；广播树静态、断链不重算 | major | 📋 控制面计费/树重算待办 |
| B8 | 正式实验仅 Malaga↔Tokyo 单 OD → 不足以支撑全局负载均衡结论 | major | 📋 论文范围限制 |

## C. 学习设定（E2 路由/RL）

| # | 发现 | 严重度 | 处置 |
|---|---|---|---|
| C1 | horizon 右删失：长等待/慢路径样本被选择性丢弃 | major | 📋 已显式计数；长跑/续训缓解 |
| C2 | deliver 被强制：出口可用即 deliver-only；下行满直接 overflow 不绕行 | major | ⚠ 需拍板（业务合同 or bug） |
| C3 | 奖励不计传播/接入/下行时延，γ 按转移次数而非物理秒 | major | ⚠ 奖励塑形设计 |
| C4 | 无历史状态（framestack/GRU 未实现）→ 无法区分“旧但上升/下降” | major | 📋 TEMPORAL 设计稿已列 |
| C5 | GAT/MPNN 32 节点静默截断（按 sat id 排序） | minor | 📋 overflow 应编码/报警 |
| C6 | TabularQ 精确浮点键 → 更新但不泛化 | major | ⚠ 基线处置待拍板（禁用/离散化） |
| C7 | hop 基线是缓存感知最短跳，非全局最短路；应并列 delay/capacity/oracle 基线 | major | 📋 实验设计 |

## D. 验证/工程（E3 验证）

| # | 发现 | 严重度 | 处置 |
|---|---|---|---|
| D1 | comparison PASS ≠ C 层归因（只查执行完整性，不自动比对分歧） | major | 📋 归因门禁待建 |
| D2 | 解析锚点共享生产 C_KM_S → 常数改错测试仍绿 | major | ✔ 已修（PR 24） |
| D3 | 控制报文 bit 未绑定配置（receipt 只验正整数） | major | ✔ 已修（PR 24） |
| D4 | population_gravity 输入未在 intent 阶段绑定 SHA | major | ✔ 已修（PR 24） |
| D5 | 变异测试 M-3/M-4/M-8/M-9 捕获测试缺失 | major | 📋 已列 |
| D6 | deadline 等时刻语义不统一（>= vs >；service_end==deadline 完成优先） | minor/major | 📋 统一语义待办 |
| D7 | C 层证据粒度不对称（direct 逐跳 vs legacy 仅路径） | major | 📋 对照设计 |
| D8 | 性能 profile 只测非学习臂；5s≈1h 未归因；几何缓存需 VM 验证 | major | 📋 VM 学习臂 profile（闸门） |

## E. 已确认正确的部分（专家背书）

- 逐包逐跳、5 动作、局部信息、真实控制包+TTL/AoI、到达缓存信息边界（设计较强）。
- 到达奖励/转移生命周期修复（hard-retire 白拿 50、horizon 丢弃计数、decisions==transitions+discarded）已被专家确认有效。
- 去预裁剪修复有效；GAT/MPNN 已含 AoI 特征（E2 纠正了旧表述）。

## F. 下一步（自动推进）

1. PR 24：op_determinism fail-closed、控制 bit 绑定、population SHA、C_KM_S 独立（已完成，待复核合并）。
2. 几何记忆化缓存 + hop BFS（等价优化第二批）。
3. A3 未来端点因果泄漏：改活跃集/惰性构建 + 对照实验。
4. B6 MBB 积压包语义：对照实验后修。
5. A1/C3 奖励塑形、A2/C2 掩码/出口语义：等专家结果已齐，列设计稿待拍板。
