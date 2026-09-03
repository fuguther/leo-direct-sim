# 对抗性评审 Round 1（Reviewer-2，fresh-context）

被攻击对象：F-I 判别核心 —— ρ = 控制决策回路时延 / 拓扑显著变化间隔，跨阈值时集中/半集中控制进入"过时决策—振荡—决策缺失"失效相图；及"轨道预测拓扑对实际转发决策解释力落差"的量化。
弹药：笔记①（arXiv:2410.15546，CGR 容量/缓存约束）、笔记②（arXiv:2601.21383，KubeSpace 控制面）、笔记③（arXiv:2501.13280，DoTD 时变拓扑）。仅用此三篇，不读工作区任何文件。

---

## 1. 迷你三图

### Claim Map（谁主张了什么与拓扑可预测性/控制时延相关的结论）

| 论文 | 主张 | 与 ρ / 落差的关系 |
|---|---|---|
| ① 2410.15546 | 只要 contact plan（=轨道预测拓扑）完美且瞬时共享，CGR 前置约束后仍保送达时间最优 | 把 ρ→0 当作公理而非变量："We assume instantaneous sharing of the network information among source routing nodes, perfect topology knowledge, no unexpected disruptions."；对 ρ>0 只留一句自认："We acknowledge that these assumptions are not realistic." |
| ② 2601.21383 | 多地面控制节点 + 轨道预测（TLE/SGP4）驱动的指派与切换，可同时获得低时延与零管理中断 | 回路时延被当成被最小化的常数（240ms），不是与拓扑变化率联动的变量；振荡用启发式压制（阈值比 δ）而非刻画，引用："a handover is triggered only when the candidate node's distance is shorter than that of the current node by a predefined ratio." |
| ③ 2501.13280 | TLE 预测驱动的时变拓扑设计（T≈10min, τ≈1s）能同时提升容量/时延并抑制 churn | 显式承认更新间隔受稳定性和服务连续性约束："This update interval is restricted by constraints related to configuration complexity, service continuity, and stability, which prevent updates at sub-second intervals." —— 即承认存在某种"太快会坏"的边界，但从不测量它 |

**综合**：三篇都隐含承认"控制/更新节奏与拓扑动态之间存在张力"，但没有任何一篇把 ρ 当作自变量扫描、没有相图、没有失效模式分类。①主张"预测完美则最优"，②③主张"预测足够好则工程可行"——全部落在 ρ 小、预测落差≈0 的舒适区内。

### Assumption Map（共同默认假设）

三篇共享的默认（F-I 的天然攻击面同时也是防御面）：

1. **轨道预测→行为的确定性传递**：①"perfect topology knowledge"直接决定路由；②"Since propagation delay dominates satellite-ground communication latency, we approximate it using spatial distances..."；③假设"satellite positions are accurately predictable over shorter time frames"。三篇都把"轨道可预测 ⇒ 转发/控制行为可预测"当作输入假设，无一检验。
2. **同源闭环评估**：③的评估在同一 TLE 驱动的确定性仿真器内闭环（跳数/时延/churn 全由同一 TLE 生成），②用空间距离既生成决策又当评估度量，①"delivery ratio is one: all bundles eventually reach the destination"。预测拓扑与"实际"行为之间没有独立误差源，落差结构性无法测出。
3. **失效被当工程噪声而非相**：①用 safety margin 兜底（"The safety margin must balance two requirements..."），②用阈值 δ 抑制，③用反 churn 权重项。三套机制都在"抑制症状"，没有一个给出症状出现的条件边界。
4. **无实测**：三篇均为仿真（①MATLAB 理想化、②KVM+tc 注入、③Mininet 类）；②③用真实 TLE 但无在轨/半实物对照。

### Evidence Map（证据类型与强度）

| 论文 | 类型 | 强度 | 规模 | 关键缺口 |
|---|---|---|---|---|
| ① | 形式化+最优性证明（§IV-C）+理想仿真 | 证明强但悬于 ρ=0；仿真证据"delivery ratio is one"（作者自注 idealistic） | Walker 星座，bundle 级 | 无信息时延/扰动扫描，"The effectiveness under stochastic contact or buffer variations is left for future work." |
| ② | 原型实现+全天仿真，真实 TLE，三星座 | 工程证据较硬（有系统数字：切换时延 -84%、不可见时长降为 0） | Starlink 1584 / Kuiper 1296 / OneWeb 636 | 距离代理时延未对照真实路由；δ 无稳定域分析；无 ρ 类变量 |
| ③ | 算法证明（打分有界/多项式）+仿真对比两基线 | 证明只对打分目标负责；仿真无统计检验、无实测 | Starlink 907 颗，5 对 GS | T 固定经验值；预测-转发同源闭环 |

---

## 2. 猎杀 F-I

**攻击 1（"问题已被工程解决"论）**：②提供了硬数字——无缝切换机制下"the satellite remains visible to the control plane at all times"、节点不可见时长降为 0、服务中断为 0。若"决策缺失"模式可以被机制性消除，F-I 相图中该相是否存在？
- **反驳**：②的零中断是在"地面控制节点 + 有线互联 + 真实 TLE 仿真 + 传播时延主导"的受限条件下取得的（自认局限："pulling and distributing container images can become a deployment bottleneck..."，且未处理星间控制面）。它是**单个设计点在低 ρ 区的工程解**，恰恰没有跨 ρ 扫描，因此不能证明高 ρ 区不失效，更不能给出边界。攻击失败，反而确证了"边界从未被画"。

**攻击 2（"过时决策有标准补救，非失效相"论）**：①的 safety margin、③的反 churn 项、②的阈值 δ 都是文献对"过时决策/振荡"的成熟应对；可否说 F-I 把已解决的工程问题错误包装成科学问题？
- **反驳**：三家的补救全部是**开环启发式、无调优理论**：①自认 safety margin 大小"must balance two requirements"但无方法；②δ 是"predefined ratio"，笔记②Tension 明言"未给出稳定域/相图分析"；③ w1=w2=0.4 无敏感性分析。即：文献承认症状、给出止痛药、从未诊断病理。F-I 的"相图边界+可观测症状"恰是这三家共同缺失的诊断层。攻击失败。

**攻击 3（"预测落差可忽略"论，最实质的攻击）**：若 TLE 预测在分钟级确实足够准（③声称"no practical need to forecast satellite positions several minutes in advance"），则"解释力落差"可能天然≈0，F-I 第二半量化的是空集。
- **部分成立**：轨道位置确实高度可预测[常识-未核验]；拓扑几何层面的落差可能很小。但 F-I 的落差主张若限于"轨道位置→拓扑"则确实弱；真正落差在**拓扑→转发行为**：队列/拥塞/故障/策略使实际转发偏离预测拓扑上的最短路，①自己承认"cause many collisions and increase the average delivery time"（被动管理失效即落差症状）。因此此攻击只压缩 F-I 措辞，不淘汰：落差必须定义在"预测拓扑 ⇒ 转发行为"层，而非"轨道 ⇒ 拓扑"层。
- **且三篇都无法反驳该落差的存在**，因为它们的评估全部同源闭环（Assumption Map 第 2 条）——它们没有提供任何独立"实际"作对照，故既不支持也不否定落差幅度。**弹药在"落差是否显著为非零"这一方向上不足**。

**判定：部分相邻（再收窄）**。三篇一致确认：ρ 类张力被承认（③的 sub-second 引用、②的切换振荡、①的不现实自认）但从未被参数化扫描；预测—行为落差被假设掉而非测量。F-I 的相图核心无覆盖；落差量化的存在性有间接支持（①的碰撞/重路由现象），但幅度无任何一篇可判。

再收窄建议：
1. 相图半：明确以③的 (T, τ) 和②的切换回路为实例化的 ρ 轴坐标，失效症状对齐②的实测类量（不可见时长、nginx 中断 9.7s/次量级）——即用②③做"低 ρ 工程样本点"，F-I 贡献的是外推边界。
2. 落差半：必须把落差定义为"预测拓扑上的预期转发 vs 实际转发（含拥塞/故障/策略）"，并设计**非同源评估**（预测用 TLE，实际用带独立扰动源的仿真/实测 trace），否则会被攻击 3 咬住。

## 3. 生长（ONE 个改写方案）

**改写 RQ**：原 F-I 第二半改为——"在预测拓扑与实际转发行为**非同源**（预测由 TLE 生成、行为由含独立拥塞/故障/策略扰动的执行环境产生）的评估协议下，量化'按轨道预测的拓扑知识'对实际转发决策的解释力 R，并刻画 R 随 ρ 与扰动强度的衰减结构；同时给出 ρ 跨阈值时三种失效模式的相图边界。"
方法论切入点正是三图暴露的**共同同源闭环缺陷**：三篇最近邻全部在同源闭环内评估，任何一篇都无法测量 R<1，因此该缺口既是 F-I 的攻击面也是其方法论贡献——"非同源评估协议"本身即可作为判别实验设计的核心创新（用①的 idealistic 设定作 R=1 上界锚点，用②的实测类症状指标作相边界的观测量）。

## 4. 诚实条款

- 三篇弹药足以判定"相图无覆盖"（三篇均无 ρ 扫描、无失效分类，引证见上）；**不足以判定"落差幅度"**——没有任何一篇提供预测与独立实际行为的对照数据。
- 还需要的文献类型：(a) 星历/拓扑预测误差传播的定量研究（TLE 漂移→链路可用性误差）；(b) SDN/分布式控制面在动态网络中的稳定性分析（拥塞控制振荡、路由抖动理论，可移植失效相图方法）；(c) 带实测 trace 的 LEO 转发行为数据集（非 TLE 同源），用于 R 的可测性；d) 半集中式路由（如分布式 CGR）的收敛时延实测。
