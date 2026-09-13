# CMNCS52M 锚件核验：发现严重混淆（2026-09-10，MinerU 全文核验）

> **来源**：run2 历史审查 §跨卡观察 2 指出"承重数字锚出自 truncated=true 的截断全文"。
> **动作**：按 EFFECTIVE-RULES-R2 §8.0.1，用 MinerU 全文 MD（`/data/liguang13/topic-loop-r2/md/CMNCS52M/CMNCS52M/txt/CMNCS52M.md`，92,432 字符）核验。
> **结论**：**数字本身核验通过；但该锚件不能支撑"负载分布漂移致退化"的单因素因果**。

## 1. 数字核验：通过

原文 §VI（表 3 附近）逐字确认：

| 队列分布模型 | DQN-BL NMB | DQN-LSNR NMB | 原文措辞 |
|---|---|---|---|
| zone-based（静态） | **≈15%** | ≈15% | "both DQN-BL and DQN-LSNR exhibit comparable performance, achieving an NMB of approximately 15%" |
| population-based（时变） | **70%** | 40% | "reducing the NMB from 70% to 40% in the population-based scenario" |
| traffic-based（时变） | **55%** | 20% | "from 55% to 20% in the traffic-based scenario" |

表 3 数值亦齐（mean E2ED、NMB、mean hops、PDR 四指标 × 三模型 × 六方法）。
→ 生成器引用的 **15% / 70% / 55% / 40% / 20% 数字链属实**。

## 2. **但锚件被混淆污染**：三个模型同时改了五个变量

原文 §III 逐字（第 77 行）：

> "Each model defines a different **queue capacity or maximum queue length**, common for all satellites in the network. The average queue occupancy of a given queue-distribution model is defined as the ratio between the mean queue length and the queue capacity. To keep E2E delays within a few seconds and assuming constant and homogeneous transmission rate across all nodes and models, **scenarios with higher queue occupancy must use smaller queue capacities**, whereas those with lower occupancy can rely on larger capacities."

同一节另有：
- zone-based 被原文自述为 "an **illustrative and academic example** with strong network congestion"（人为构造，非真实）；
- zone 模型 "is **not time-dependent**"，故 "the time-related observation feature has been **removed from the state representation**, resulting in a **reduced input dimensionality**"（表 2 明列"input dimension"三模型不同）。

**因此三个模型之间同时变化的是**：

| # | 变量 | zone | population | traffic |
|---|---|---|---|---|
| 1 | 空间分布模型 | 分区（人造） | 人口（GPWv4） | 人口+通信能力 |
| 2 | **队列容量** | 小（高占用需小容量） | 中 | 大 |
| 3 | **平均占用率** | 高（"strong congestion"） | 中 | 低（原文明言"更多不拥塞节点"） |
| 4 | **是否时变** | 静态 | 时变（地转） | 时变（地转） |
| 5 | **状态输入维度** | 降维（去时间特征） | 全维 | 全维 |

## 3. 后果：不能作为单因素证据

- 生成器 A1/A2/B1/B3 把"zone 15% → population/traffic 70%/55%"读作**"负载分布漂移导致策略退化"**；
- 但同一对照**同时**改变了占用率（拥塞程度）、队列容量、状态维度——**任何一项单独变化都可能解释差异**；
- 尤其 **#3 占用率**与 **#5 状态维度**：前者直接改变任务难度（原文自述 zone 是"strong congestion"的人造例），后者直接改变可观测信息量（去掉时间特征＝信息更少）。

**判定**：该锚件**降级**——可用于"**在三种不同队列分布设定下，RL 的性能差异显著**"（描述性事实），**不可用于**"**负载分布漂移本身导致退化**"（因果断言）。后者需 G2 要求的竞争解释排除，本卡目前**未做**。

## 4. 对 run2 各卡的影响

| 卡 | 引用方式 | 影响 |
|---|---|---|
| A1 | 作为"跨负载分布失配致退化"的间接证据 | **需改写**：降级为描述性事实，或补做混淆控制（固定容量/占用率/维度，仅换分布） |
| A2 | 通道 1（占用分布漂移）现象层 | 同上 |
| B1 | "时变空间负载下 RL 大幅恶化" | 同上；B1 的**自变量是热点位置**，与本文的分布模型替换不同，需区分 |
| B3 | 失败原因三假说分离的必要性 | **反而被强化**：本文正是"多因素混在一起、无法归因"的实例 |

## 5. 教训（已入规则 §8.0.1）

1. **截断全文的承重锚必须回全文核验**——本次若不做，混淆会一路带进深化与交付；
2. **"同一张表里的不同条件"不等于"单因素对照"**——读数字必须同时读**实验合同**（本例的容量/占用率/维度差异就在同一节的文字里）；
3. 该发现由**独立历史审查**（发现锚件截断）→ **主控回全文核验**（发现混淆）两段接力完成，**任一环缺失都会漏掉**。
