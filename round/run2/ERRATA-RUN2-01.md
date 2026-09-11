# 勘误表 ERRATA-RUN2-01（2026-09-11）

> **性质**：对已冻结生成产物的**证据等级更正**，不改动原文（保持版本可比）。
> **触发**：EFFECTIVE-RULES-R2 §8.0.1 承重锚件全文核验（由历史审查指出"锚件出自 truncated 全文"→ 主控用 MinerU 全文核验）。
> **适用范围**：`round/run2/staging/path-A-intensity.md`、`path-B-hotspot.md` 中引用 **CMNCS52M** 的断言。
> **核验底本**：`/data/liguang13/topic-loop-r2/md/CMNCS52M/CMNCS52M/txt/CMNCS52M.md`（MinerU pipeline_txt，92,432 字符）

## 核验结论

| 项 | 结果 |
|---|---|
| 数字本身 | ✅ **属实**（§VI 原文：zone NMB≈15%；population 70%→40%；traffic 55%→20%；表 3 含 mean E2ED/NMB/hops/PDR 四指标） |
| 作为**单因素因果证据** | ❌ **不成立** —— 三个模型同时改变 **5 个变量** |

**原文 §III 逐字**：
> "Each model defines a different **queue capacity or maximum queue length**… scenarios with **higher queue occupancy must use smaller queue capacities**, whereas those with lower occupancy can rely on larger capacities."

**原文对 zone 模型的自述**：
> "an **illustrative and academic example** with strong network congestion"；且 zone 模型 "is **not time-dependent**"，故 "the time-related observation feature has been **removed from the state representation**, resulting in a **reduced input dimensionality**"。

**五变量对照表**：

| # | 变量 | zone | population | traffic |
|---|---|---|---|---|
| 1 | 空间分布模型 | 分区（人造） | 人口 GPWv4 | 人口+通信能力 |
| 2 | 队列容量 | 小 | 中 | 大 |
| 3 | 平均占用率 | 0.5（强拥塞） | ≈0.06 | 更低 |
| 4 | 是否时变 | 静态 | 时变（地转） | 时变（地转） |
| 5 | 状态输入维度 | 降维 | 全维 | 全维 |

## 逐条更正（含行号与原句）

### 更正 1｜path-A-intensity.md 第 75 行（**最重要**）
- **原句**：「【原文事实】CMNCS52M（Vol.7 2026, p.1372–1378）：同一算法族在静态 zone 队列分布下 NMB≈15%，在因地球自转而时变的 population/traffic 分布下 DQN-BL NMB 达 70%/55%，DQN-LSNR 亦达 40%/20%——**负载/拥塞分布漂移本身已实质性伤害策略**，即使不跨模型迁移。」
- **更正**：破折号后的因果断言 **不成立**。应改为：「…NMB 达 70%/55%，DQN-LSNR 亦达 40%/20%。**【更正】该差异不能归因于分布漂移本身**——三模型同时改变了队列容量、平均占用率、时变性与状态输入维度；原文自述 zone 为人为构造的强拥塞例，且为静态、状态维度更低。」
- **等级**：因果断言从【原文事实】→ **降级为【待证】**。

### 更正 2｜path-A-intensity.md 第 117 行
- **原句**：「【原文事实】强度变化改变**占用分布**：CMNCS52M 三模型的平均占用率 zone=0.5、population≈0.06（≈8× 摆动），且队列容量被反调以维持 ~1s 平均排队时延（§III.B）→ 绝对队长的"同一读数"在强度/模型间语义漂移。」
- **更正**：**前半句属实**（占用率差异 + 容量反调，原文逐字支持）；**箭头后的推演不构成"强度变化"的证据**——这里的"模型间"差异是**人为设定**的（人为选容量以维持 ~1s 时延），不是"负载强度变化"造成的。该推演应标注【推演】而非【原文事实】，且不得用于支撑"强度变化"论点。
- **等级**：链接结论从【原文事实】→ **【推演】**。

### 更正 3｜path-A-intensity.md 第 118 行
- **原句**：「【原文事实】强度变化改变**最优结构**：CMNCS52M population 场景中 SP 选择"traversing longer but less congested paths"…静态 zone 下 DQN-BL NMB≈15% vs 时变下 70%（Table 3 上下文）。」
- **更正**：SP 绕行 **属实**（原文逐字）；但"15% vs 70%"是**跨模型比较**，同样受 5 变量混淆——不得作为"强度变化改变最优结构"的证据。
- **等级**：跨模型数字比较 → **降级为【待证】**。

### 更正 4｜path-B-hotspot.md（引用同一锚件处）
- 同源问题：凡以"zone 15% → population/traffic 70%/55%"论证"时变空间负载致退化"的段落，均须按更正 1 处理。

## 对本轮卡片的处置

| 卡 | 处置 |
|---|---|
| A1（已合并入 B3） | 卡内 `difficulty`/`cause_hypothesis` 已追加锚件复核注；其"合同审计"价值**不受影响**（那是元层面证据，与本锚件无关） |
| A2 | 通道 1 证据降级；通道 2/3 不受影响 |
| B1 | 自变量是**热点位置**（非分布模型替换），须在深化时明确区分二者；"时变致恶化"的因果表述须重新取证 |
| B3 | **反向受益**：本文正是"多因素混在一起、无法归因"的现成实例，强化 B3 的评估协议必要性 |

## 教训（已写入 EFFECTIVE-RULES-R2 §8.0.1）

1. **截断全文的承重锚必须回全文核验**——本次若不做，混淆会一路带进深化与交付；
2. **"同一张表里的不同条件" ≠ "单因素对照"**——读数字必须同读实验合同（本例的容量/占用率/维度差异就写在同节文字里）；
3. 该问题由**独立历史审查（发现锚件截断）+ 主控回全文核验（发现 5 变量混淆）**两段接力发现，**任一环缺失都会漏掉**。
