## 总结先行

你现在至少有 **4 组变量被捆绑**：

1. **聚合方式 × 可用信息量**：最严重，当前“聚合”因子不能作因果解释。

2. **(k) × 信息年龄 × 获取成本**：真实系统中本来就耦合，不能简单当三个独立旋钮解释主效应。

3. **(k) × GNN 有效深度/感受野**：如果层数随 (k) 变，所谓 (k) 效应混进了模型深度；如果不变，又可能根本没真正使用新增的远端节点。

4. **age-aware × 额外结构/参数([openreview.net](https://openreview.net/forum?id=rJXMpikCZ&utm_source=chatgpt.com "Graph Attention Networks"))提升不能归因于“显式年龄调制”。

**这个设计可以救，但当前“三因子 + 三条单因素线”的因果叙事需要重排。** 不需要推倒仿真和观测定义，但需要把“系统比较”和“机制验证”拆成两类实验。

---

# 1. fixed-stats vs GNN：你确实把“聚合方式”和“信息权限”混在了一起

### 混淆是什么

当前实际上是：

# [

\text{fixed-stats}

\text{固定聚合}  

+ \color{#b00}{\text{无 edge features}}  
  ]

而：

# [

\text{MPNN}

\text{学习聚合}  

+ \color{#b00}{\text{edge features}}  
  ]

甚至你的 GAT 还必须进一步说明是不是 **edge-aware GAT**。经典 GAT 的注意力系数主要由相邻节点表征计算；而 MPNN 框架从定义上就允许消息函数显式依赖边特征。([proceedings.mlr.press](https://proceedings.mlr.press/v70/gilmer17a/gilmer17a.pdf?utm_source=chatgpt.com "Neural Message Passing for Quantum Chemistry"))

所以现在所谓：

> fixed-stats vs MPNN/GAT

不是“聚合函数不同”，而是：

> **信息集合 + 表示形式 + 学习方式 + 聚合算子一起变化。**

形式上甚至可以写成：

[  
\mathcal I_{\text{fixed}}  
\subset  
\mathcal I_{\text{MPNN}}  
]

你不是让两个模型用同样的信息解决问题。

### 为什么威胁归因

如果 MPNN 赢，你无法知道原因是：

- 使用了链路带宽；

- 使用了链路可用性；

- 使用了传播时延；

- 使用了边方向；

- 图拓扑传播本身；

- learned aggregation；

- 或以上组合。

所以论文不能写：

> learned graph aggregation outperforms fixed aggregation.

最多只能写：

> the graph-based encoder outperforms the legacy fixed-statistics encoder under its richer edge-aware representation.

这是完全不同强度的结论。

### 修复

**保留两个不同性质的比较，不要强行合成一个“聚合”因子。**

第一组叫 **system-level encoder comparison**：

> original fixed-stats / MPNN / GAT / age-aware GAT

允许 fixed-stats 保持原始设计。  
但明确承认这是“整体编码器方案比较”，不作聚合机制归因。

第二组专门做 **information-matched mechanism comparison**：

> edge-aware fixed aggregation / MPNN / edge-aware GAT / age-aware GAT

所有模型访问完全相同的：

[  
{x_v,e_{uv},AoI,destination}  
]

然后才有资格讨论 aggregation mechanism。

---

# 2. (k) 和陈旧度：不是两个完全独立的物理因子

### 混淆是什么

真实系统中，随着 hop distance (d) 增加，一般会同时变化：

[  
d\uparrow  
\Rightarrow  
\begin{cases}  
\text{available information}\uparrow\  
AoI\uparrow\  
\text{communication overhead}\uparrow\  
\text{propagation/update uncertainty}\uparrow  
\end{cases}  
]

所以：

[  
k=3,;AoI=0  
]

可能是一个非常有用的**人工诊断条件**，但未必代表真实可实现的观测系统。

你现在把：

> observation radius

和

> observation freshness

当成独立 factorial factors，统计上可以这么操纵，但物理解释不能直接跟着独立化。

### 为什么威胁归因

假设 (k=3) 比 (k=1) 差。

到底是：

- 远端信息没用；

- 远端信息太旧；

- GNN 无法处理更大的图；

- attention 被更多节点稀释；

- 通信开销造成代价；

- 还是其中几个共同作用？

反过来，若在人工的 (AoI=0) 下 (k=3) 很强，你也不能据此说现实里扩大观测范围有收益。

### 修复 / 重新表述

把问题拆成两个不同研究问题。

**机制问题：**

> 在人为控制 freshness 相同的情况下，增加 observation radius 是否具有潜在信息价值？

这里允许做人工正交：

[  
k\times stale  
]

但明确称为 **controlled stress test / mechanism isolation**。

**系统问题：**

定义真实的：

[  
AoI_d\sim P(AoI\mid d)  
]

以及：

[  
C=C(k)  
]

然后问：

> **在随 hop distance 恶化的 freshness profile 和给定通信预算下，扩大局部观测范围的净收益是多少？**

这才是你真正应该问的系统问题。

---

# 3. “同一张标准观测图”并不自动代表对 fixed-stats 公平

### 混淆是什么

你现在隐含采用了：

> fairness = everyone receives the same graph object.

这个定义不对。

fixed-stats 原来是：

[  
\text{raw observations}  
\rightarrow  
\text{directional statistics}  
\rightarrow  
\text{flat vector}  
]

而 GNN 是：

[  
\text{raw observations}  
\rightarrow  
\text{graph}  
\rightarrow  
\text{message passing}  
]

强迫 fixed-stats 先进入一个为 GNN 设计的数据结构，并不能产生公平性。

### 为什么威胁归因

公平真正应该约束的是：

> **底层可访问测量信息相同。**

而不是：

> 输入 tensor 类型相同。

尤其你这里 fixed-stats 的 inductive bias 本来就是：

[  
\text{neighbor identity}  
\rightarrow  
\text{first-hop direction}  
\rightarrow  
(mean,max)  
]

这种信息丢失本身就是 baseline 的定义。

如果你同时要求它“吃图”和“不使用边”，就把**数据适配器设计**也塞进模型比较了。

### 修复

建立一个比“标准图”更底层的 canonical observation：

[  
O_t^k=  
{  
\text{nodes},  
\text{edges},  
\text{timestamps},  
\text{destination}  
}  
]

之后：

[  
O_t^k  
\xrightarrow{\phi_\text{fixed}}  
z_\text{fixed}  
]

[  
O_t^k  
\xrightarrow{\phi_\text{GNN}}  
G  
]

**允许每个 encoder 使用自己的自然 representation。**

公平条件改成：

> same raw measurements + same timestamp semantics + same information permission.

不是 same tensor。

---

# 4. 你漏掉了一个很严重的 (k\times) 图层数混淆

### 混淆是什么

假设根节点最后负责决策。

标准 message-passing GNN 中，堆叠 (L) 层才使节点逐步接收更远邻域的信息；长程传播还可能产生信息压缩问题。([arXiv](https://arxiv.org/abs/2006.05205?utm_source=chatgpt.com "On the Bottleneck of Graph Neural Networks and its Practical Implications"))

于是：

### 情形 A：固定 (L=1)

你给：

[  
k=1,2,3  
]

但 root 实际只直接整合 1-hop message。

那么所谓 (k=3) **可能根本没有充分使用三跳信息**。

### 情形 B：设置 (L=k)

那么：

[  
k=1\Rightarrow L=1  
]

[  
k=3\Rightarrow L=3  
]

你又偷偷同时改变：

- observation radius；

- network depth；

- nonlinear transformation 次数；

- optimization difficulty；

- 潜在过平滑/过压缩行为。

### 为什么威胁归因

于是：

> “(k=3) 不如 (k=2)”

可能根本不是远邻居没价值，而是三层 GNN 更难训练。

### 修复

不要让 (L=k) 成为默认设计。

至少做一个明确的控制：

[  
L=\text{constant}  
]

并保证各 (k) 的 readout **确实可以接触对应范围的信息**。

例如可以采用：

> 所有节点先统一编码 → root 对整个 observed (k)-hop set 做 readout

从而把：

[  
\text{observation radius}  
]

和：

[  
\text{propagation depth}  
]

拆开。

如果坚持 recursive message passing，则 **(L)** 应该作为独立 architecture ablation，而不能藏进 (k)。

---

# 5. 参数量/模型容量确实是隐藏混淆，但“严格参数完全相同”也不是唯一答案

### 混淆是什么

fixed-stats + MLP、MPNN、多头 GAT、age-aware GAT 很可能参数规模不同。

特别是：

[  
\text{multi-head attention}  
]

可能天然带来更多 projection parameters。

### 为什么威胁归因

如果：

[  
P_{\text{age-GAT}}\gg P_{\text{GAT}}  
]

那么提升可以解释为：

> 更大的函数逼近器。

而不是 age-awareness。

### 修复

主实验至少给一个 **matched-capacity comparison**：

[  
P_i\approx P  
]

并统一：

- hidden dimension；

- training steps；

- replay budget；

- optimizer；

- target update；

- exploration schedule。

同时补一个小规模 capacity sweep：

[  
0.5P,;P,;2P  
]

如果 age-aware 的优势在相近容量范围内仍然存在，归因才稳。

---

# 6. GAT vs age-aware GAT 才是你最应该做到“只差一刀”的实验

这是你的核心贡献，所以标准应该比另外三组严格很多。

### 混淆是什么

你已经把 AoI 放进节点特征。这一点非常关键。

因此普通 GAT 已经能够学习：

# [

\alpha_{ij}

f(h_i,h_j,AoI_j)  
]

至少原则上它有机会从普通 node feature 中学会：

> old information should receive lower attention.

那么 age-aware GAT真正声称的贡献不是：

> GAT 不知道 AoI，而我知道。

而应该是：

> **显式 freshness inductive bias 比仅把 AoI 当普通 feature 更有效。**

### 为什么威胁归因

如果 age-aware GAT 又增加：

- 一个额外 MLP；

- 更多 heads；

- 更多 hidden units；

那你的核心结论立即变成：

> 一个更复杂的 GAT 胜过普通 GAT。

### 修复

这里要求最严格：

[  
\boxed{  
\text{GAT}  
\leftrightarrow  
\text{Age-GAT}  
}  
]

必须：

- 同一输入；

- 两者都看 AoI；

- 同样 hidden size；

- 同样 heads；

- 近似相同参数；

- 同一 message function；

- 同一 destination conditioning；

- **唯一改变是 attention logit / weight 中的 age modulation。**

另外加两个非常便宜但杀伤力很大的 negative controls：

[  
AoI_{\text{shuffle}}  
]

以及

[  
AoI_{\text{constant}}  
]

如果 shuffled AoI 仍然提高性能，你所谓“freshness-aware mechanism”就很可疑。

---

# 7. 你的 AoI 现在似乎只在 node feature，但“陈旧状态”不只来自节点

### 混淆是什么

你写的是：

节点：

> 4向队列、**AoI**……

边：

> bandwidth、availability、delay、direction

但你的研究陈述里“过时信息”包括：

- neighbor queue；

- link availability；

- 甚至 delay/capacity estimate。

那么一个单独的 node AoI：

[  
AoI_v  
]

并不足以描述：

[  
AoI_{queue,v},\quad  
AoI_{availability,e},\quad  
AoI_{delay,e}  
]

### 为什么威胁归因

假设 high-stale condition 同时把 link availability 变旧。

age-aware GAT看到：

> 节点很新。

但对应边状态可能已经非常旧。

那么实验失败可能只是：

> 你提供的 age metadata 与真正 stale 的 datum 对不上。

更严重的是，实验成功后你也不能声称算法处理了“link-state staleness”。

### 修复

要么缩窄 claim：

> age-aware neighbor-state aggregation，主要处理 node-state freshness。

要么显式加入：

[  
AoI_v^{node}  
]

和：

[  
AoI_{uv}^{edge}  
]

最好 AoI 与其对应数据同粒度。

这是我认为你当前设计里**非常容易被 reviewer 抓住的一点**。

---

# 8. 一个比参数量更危险的隐藏混淆：你可能从别的字段偷偷泄漏“新鲜真值”

### 混淆是什么

假设你把 queue / availability 延迟了 (\Delta t)，但随后：

- graph adjacency 使用**当前真实链路**；

- hop count 用**当前拓扑**重新算；

- first-hop direction 用**当前拓扑**重新算；

- action mask 使用**当前 link availability**；

- relative position 使用当前真实位置。

那么模型虽然看到“陈旧特征”，却能通过其他字段获得新鲜结构信息。

尤其是：

> **stale availability + current adjacency**

几乎是直接的信息泄漏。

### 为什么威胁归因

此时 high-AoI 条件不是真正的 partial/stale observation：

[  
O_{t-\Delta}  
]

而是混合体：

[  
O=  
{  
x_{t-\Delta},  
G_t,  
mask_t,  
derived(G_t)  
}  
]

所以你根本不知道模型究竟依赖 old information 还是 fresh structural side-channel。

### 修复

给**每个观测字段**冻结 timestamp semantics。

尤其写清：

[  
G^{obs}_t  
]

到底是：

1. 当前 topology；

2. delayed topology snapshot；

3. candidate topology + stale availability feature。

然后所有 derived features：

- hop；

- first-hop direction；

- neighborhood membership；

必须从**允许看到的同一 snapshot**计算。

action mask 如果使用真实当前链路，也必须明确：

> 当前可行性属于 environment safety interface，不属于被陈旧化的 routing observation。

否则不要称整个 observation stale。

---

# 9. 目的地“什么时候进入”确实可能毁掉 aggregation ablation

### 混淆是什么

考虑：

### 模型 A

先：

[  
\text{aggregate neighbors}  
]

再：

[  
[z,destination]\rightarrow Q  
]

### 模型 B

先把 destination 放进每个 message：

# [

m_{ij}

f(h_j,e_{ij},d)  
]

再 aggregate。

这两个模型解决的已经不是同一个表示问题。

B 可以进行：

> destination-conditioned neighbor selection

A 只能：

> 先无条件压缩，再根据 destination 决策。

### 为什么威胁归因

如果 age-aware GAT 采用 destination-conditioned attention，而普通 GAT 没有，提升就不能归到 age awareness。

### 修复

在核心 GAT vs age-GAT 对照里，强制目的地进入位置一致。

例如统一：

[  
q_i=f(h_i,d)  
]

[  
k_j=f(h_j,e_{ij},d)  
]

然后只修改：

[  
\alpha_{ij}  
]

中的 age term。

destination-in-message 本身应该另做 ablation，不要藏在年龄算法里。

---

# 10. “陈旧度 sweep”还有一个训练分布混淆

### 混淆是什么

假设：

- stale=0：训练一个 policy；

- stale=low：重新训练一个 policy；

- stale=high：重新训练一个 policy。

然后比较 performance。

这测的是：

> 每个算法在**已知其观测质量条件下重新适应后的最优表现**。

不是：

> robustness to observation staleness.

### 为什么威胁归因

age-aware GAT 在 high-stale 上训练以后赢了普通 GAT，并不能证明：

> 它遇到未知 staleness degradation 时更鲁棒。

它可能只是更适合针对该环境重新训练。

### 修复

区分两种实验，不要混称：

**Adaptation capacity：**

[  
train(s)\rightarrow test(s)  
]

**Staleness robustness：**

[  
train(s_0)\rightarrow  
test(0,low,high)  
]

或者：

[  
train(s\sim P_{train})  
\rightarrow  
test(s\sim P_{shift})  
]

如果你的论文要说“robust to stale observation”，后者更重要。

---

# 11. 单因素线本身会掩盖你最需要证明的 interaction

### 混淆是什么

你的核心假设实际上不是：

[  
\text{Age-GAT main effect}>0  
]

而应该近似是：

[  
\boxed{  
\text{Age-GAT advantage}  
\uparrow  
\quad\text{when staleness}\uparrow  
}  
]

也就是：

[  
\text{Aggregator}\times\text{Staleness}  
]

interaction。

甚至很可能还有：

[  
k\times Staleness\times Aggregator  
]

因为 age-aware 聚合应该在：

> “远端信息更多，而且远端信息年龄异质性更大”

时最有价值。

### 为什么威胁归因

如果你只在固定 (k=2) 下扫 stale，得到：

> Age-GAT > GAT

不能证明这种效果对 observation radius 稳健。

反之在一个 (k) 上没赢，也不能否定年龄机制，因为这个 (k) 可能根本没有足够的 age heterogeneity。

### 修复

pilot 全交叉不是只用来“看看趋势”。

它最重要的任务应该是检验：

[  
k\times stale  
]

和：

[  
aggregator\times stale  
]

以及核心的：

[  
k\times aggregator\times stale  
]

如果 interaction 明显，后续就不要再把结果解释成三个独立 main effects。

---

# 12. seed 选择：你提到的这个风险是真实的，而且 pilot 特别危险

### 混淆是什么

如果你跑 pilot：

> seed 1–5

发现某几个 seed “稳定”，然后正式实验继续用这些 seed，就产生选择偏差。

反过来，如果看到某组差距不明显以后继续补 seed，直到显著，也一样污染推断。

DRL 本身就存在较明显的 run-to-run variance；有限 seeds 下仅报告点估计容易改变算法排序或夸大差异，因此 RL 实验通常需要显式报告不确定性。([AAAI Publications](https://ojs.aaai.org/index.php/AAAI/article/view/11694?utm_source=chatgpt.com "Deep Reinforcement Learning That Matters | Proceedings of the AAAI Conference on Artificial Intelligence"))

### 为什么威胁归因

你的变化可能来自：

[  
\text{algorithm effect}  
]

也可能来自：

[  
\text{initialization / traffic / exploration seed}  
]

而你恰好筛选了对新算法有利的 seed。

### 修复

pilot 与正式评估：

# [

S_{\text{pilot}}  
\cap  
S_{\text{final}}

\varnothing  
]

正式比较中对所有算法使用**相同的一组 environment seeds / traffic seeds**，形成 paired comparison。

seed 数量和停止规则在看正式结果之前冻结，并报告 interval，不只报最好 seed 或均值。([AAAI Publications](https://ojs.aaai.org/index.php/AAAI/article/view/11694?utm_source=chatgpt.com "Deep Reinforcement Learning That Matters | Proceedings of the AAAI Conference on Artificial Intelligence"))

---

# 13. 还有一个容易被忽略的：(k) 同时改变“信息范围”和“集合大小”

### 混淆是什么

从 (k=1\rightarrow3)，你不只是获得远端信息，还改变：

[  
N_k=\text{number of observed nodes}  
]

GAT 的 softmax attention 会在不同数量的候选邻居/消息之间归一化。

因此：

> k 增大以后性能下降

可能来自：

1. 远端信息本身有害；

2. stale information 有害；

3. 更多节点造成 aggregation burden；

4. attention normalization / compression 出现问题。

这类长程信息汇聚瓶颈本身也是 message-passing GNN 的已知问题之一。([arXiv](https://arxiv.org/abs/2006.05205?utm_source=chatgpt.com "On the Bottleneck of Graph Neural Networks and its Practical Implications"))

### 为什么威胁归因

你不能直接把：

[  
\Delta Performance(k)  
]

解释成：

> value of farther information.

因为它同时包含了：

> cost of processing a larger set.

### 修复

把问题重写成：

> **net value of expanding observation scope for a given encoder**

而不是：

> informational value of distant nodes.

如果真的要测纯信息价值，可以再做 fixed-budget sampling：

[  
|V_{obs}|=B  
]

比较同样节点数量下：

- near-only；

- mixed-distance；

- far-aware selection。

---

# 14. AoI 与“错误程度”不是同一个变量

### 混淆是什么

AoI 是：

[  
A(t)=t-u(t)  
]

即信息距离其生成/更新时间过去了多久。

但：

[  
AoI=100\text{ ms}  
]

不代表观测误差必然相同。

稳定队列在 100 ms 内可能几乎不变；热点队列在 20 ms 内都可能完全失效。

所以实际危险程度更接近：

# [

\text{staleness harm}

f(AoI,\text{state dynamics})  
]

而不是仅仅：

[  
f(AoI)  
]

AoI 本质上描述信息 freshness，而不是直接描述状态估计误差。([arXiv](https://arxiv.org/pdf/1811.06776?utm_source=chatgpt.com "Reinforcement Learning Based Scheduling Algorithm for ..."))

### 为什么威胁归因

如果 high-AoI 条件刚好也使用高波动 traffic，那么：

> age-aware GAT 在 high stale 下收益变大

可以来自：

[  
AoI\uparrow  
]

也可以来自：

[  
state\ volatility\uparrow  
]

### 修复

冻结 traffic process，再操纵 observation delay。

进一步最好报告：

[  
AoI  
]

和实际误差，例如：

[  
|\hat q-q|  
]

之间的关系。

这样你才能证明 AoI 在你的环境里确实是“信息可靠性”的有效 proxy。

---

# 最终判断

## **能救，但不能继续把当前结构叫做“三个独立因子的实验”。**

不需要推翻：

- simulator；

- (k)-hop observation；

- AoI 特征；

- 四类 encoder；

- full-cross pilot。

需要推翻的是**归因结构**。

我会把整个实验重排成下面三层：

### A. 系统级比较——回答“哪个完整方案更好”

[  
\text{legacy fixed-stats}  
\quad vs\quad  
MPNN  
\quad vs\quad  
GAT  
\quad vs\quad  
Age\text{-}GAT  
]

允许它们保持自然设计。

但结论只能是：

> **encoder/system comparison**

绝不称为纯 aggregation ablation。

---

### B. 核心机制实验——真正证明你的 novelty

只做：

[  
\boxed{GAT\quad vs\quad Age\text{-}GAT}  
]

严格做到：

[  
\begin{aligned}  
&\text{same raw observations}\  
&\text{same AoI}\  
&\text{same edge features}\  
&\text{same destination injection}\  
&\text{same depth}\  
&\text{same parameter budget}\  
&\text{same optimization}\  
&\textbf{only age modulation differs}  
\end{aligned}  
]

然后：

[  
staleness\uparrow  
\Rightarrow  
\Delta_{\text{Age-GAT-GAT}}\uparrow?  
]

这才是你的核心证据。

再用：

[  
AoI_{\text{shuffle}},\quad AoI_{\text{constant}}  
]

攻击自己的机制。

---

### C. (k) 不再作为独立“信息多少”因素，而作为系统 observation scope

真正的问题改成：

> **在 hop-dependent freshness 和 observation cost 下，增加 observation scope 的边际净价值是什么；age-aware aggregation 是否能扩大“值得观察”的有效半径？**

我认为这个表述比：

> (k) 越大是不是越好？

强很多。

甚至你的最终研究问题可以收敛成一句：

[  
\boxed{  
\text{When does additional but increasingly stale neighborhood information remain useful,}  
}  
]

[  
\boxed{  
\text{and can age-aware attention extend that useful observation horizon?}  
}  
]

这个问题把 **(k)、staleness、age-aware attention** 放到了正确的因果关系里，而不是假装它们彼此独立。

因此我的裁决是：**框架可救，实验因子必须重排；fixed-stats 不应再进入“纯聚合因子”，而 (k) 与 stale 必须分成“人工正交的机制实验”和“真实耦合的系统实验”。** 如果不做这两处修改，即使结果全部显著，最核心的两个结论——“GAT 聚合更优”和“扩大 (k) 的效果”——都很容易被审稿人以不可归因为由打掉。
