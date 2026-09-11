# 合成补遗：B7/B10 的新增轴与最强负证据（主控，2026-09-11）

> B1-B10 全部交齐（111 篇逐篇拆解，11801+1196+1201 行）。本文补两批带来的**改变对照表**的内容。

## 1. 信用分配轴表**新增第 6 轴：边级（Lagrangian 对偶次梯度）**——B7 的 FLQLU3T4

| 工作 | 分解轴 | 进学习信号？ | 覆盖"失败原因"？ |
|---|---|---|---|
| **FLQLU3T4 (DeepLaDu)** | **边（links）** | ✅ 次梯度 $\delta(\lambda)_{i,j}=\sum\hat{q}\hat{x}-\sum r\hat{c}$（式 35）；损失=对偶函数期望（式 33）；$w^{[k+1]}=w^{[k]}+\alpha^{[k]}\sum\delta\nabla\lambda$（式 39） | ❌ 轴是**网络元素（边）**，非失败原因 |
| （其余五轴） | 目标类型 / 约束类型 / 代价来源 / 智能体 / 时间 | — | ❌ 同上 |

**要点**：FLQLU3T4 是 B7 批**唯一含学习成分**的工作，且**无折扣、无回报、无 bootstrapping**——它是"用学习逼近对偶变量"而非"用学习逼近价值"。
**对本方案的影响**：它提供第 6 条可借用的骨架——**若把次梯度的聚合维度从"边"换成"失败原因"，即得 G-A 的又一条实现路径**（与 UKBSA7WN 的多通道 Q 并列）。两条路径共同说明：**结构载体在库里是现成的**，缺的只是"归因到失败原因"这一步。

## 2. G-A 的最强负证据（B10 找到，主控认可其论证价值）

**JP79GMZS（ELB, 2009）L213 逐字**：
> "In all conducted simulations, all links are presumed to be **error-free**. The rationale beneath this assumption is to **avoid any possible confusion between throughput degradation due to packet drops (due in turn to buffer overflows at satellites) and that due to satellite channel errors**."

**含义**：该文**明确命名了两种物理丢包原因**（缓存溢出 vs 信道错误），却选择**用假设消除其一**以"避免混淆"。
→ 这正是 G-A 空白带的**结构性证据**：领域内早已意识到两种原因会混淆，而处理方式是**回避**（假设掉一个），不是**分离**（各自喂给学习通道）。
→ 论证用法：这不是反例，而是"问题被识别却未被解决"的**最强动机证据**，比单纯"没人做过"强得多。

**反向证据（结构性排除）**：J68GU76W L198 逐字 "buffer overflow is not explicitly modeled" —— T1 级 RL 路由论文**在结构上就无法分因**（溢出根本没建模）。

## 3. B10 的其他可用材料

| 材料 | 位置 | 用途 |
|---|---|---|
| 负载过程的**两尺度分解** | T9X6QCLL L171 逐字："decompose the traffic into a predictable long-term baseline, and some variable short-term fluctuations" | 综述层面对"负载过程"最明确的表述；支撑"过程形状值得单独建模" |
| 负载度量公式族 | BV4XI6CU 式 2/3/4/5/7/8/9-15 | **零随机到达建模**（适应性阈值 = max(均值, 初始阈值)，式 8）——阈值结构的工程代表，可作对照臂 |
| 决策成本进评价指标 | 5AZHJE7N L132 | 把**路由协议收敛时间**与负载均衡并列为标准指标——支持"决策成本应被度量" |
| Starlink 定标数字 | T9X6QCLL L482 | 轻载丢包 0.4% / 拥塞 1.5–2%；中位 RTT 50ms→约 100ms |
| 引用热度 | B7 实测 | 67CSKFK4 被 23 篇引（含 3 篇 T1）；FLQLU3T4 / 7TASFUDR / AIH4GK37 / W5Z39E25 **零引用** |

## 4. B10 未读段的处置（主控补读）

- **Z74SR656 第 VI 节（ML-Empowered NTNs）**：补读确认为**ML 应用综述**（按用户/BS/核心网/数据网四实体分类，Fig. 8 归纳），其"挑战"项为切换与干扰管理、MEC 联合策略、多段组网、IoT——**与负载过程/失败归因无关**；缺口关闭，不影响任何主张。
- **5AZHJE7N 第 IV/V 节**：补读确认为**仿真器逐工具综述**（STIN 框架三步骤 + 工具清单 + 评价指标 Fig. 4）；唯一相关点是其 L132 的指标并列（已列入上表）。缺口关闭。

## 5. 全批收口后的口径

- 证据规模：111/111 篇定档；T1 档 34 篇算法级全拆；T2 档 32 篇机制级；T3 档 16 篇证据级；T4 档 11 篇方法级；T5 档 13 篇背景级；T6 档 5 篇登记排除。
- 计数口径：**md-only（111 篇）**，JSON 副本问题见 COUNTING-ERRATUM。
- G-A 最终判定：**成立**（六条分解轴全部不是失败原因；最强负证据 JP79GMZS L213；两条现成结构载体 UKBSA7WN 多通道 Q、FLQLU3T4 边级次梯度）。
