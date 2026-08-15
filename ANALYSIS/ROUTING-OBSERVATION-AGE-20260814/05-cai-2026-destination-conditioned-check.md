# Cai et al. (ICIC 2026) 中 Destination / Target 信息进入 GNN 的位置核查

## 结论

**判定：A**

> 目的地信息是在 GNN / GAT 完成局部子图特征提取之后，再与图表示一起送入 MLP / DQN 决策头；公开材料没有显示 destination / target 信息参与了 GNN 消息构造、注意力权重计算或邻居聚合过程。

因此，这篇论文**没有证伪**以下更窄的新颖性主张：

> **Destination-conditioned message passing**：目的地信息在消息传递阶段直接进入每条邻居消息，例如

$$
m_{j\to i}
=
\phi\!\left(
h_i,\,
h_j,\,
e_{ij},\,
z_d,\,
\Delta_{ij}
\right).
$$

这与“先做 destination-agnostic 图聚合，再把 destination 拼给后续 FCNN / MLP”存在机制层面的区别。

---

## 1. 论文信息

- **题目**：*Target-Aware GNN-DQN Adaptive Routing for LEO Satellite Networks*
- **作者**：Cai et al.
- **会议**：ICIC 2026
- **出版系列**：Lecture Notes in Computer Science (LNCS), Vol. 16643
- **页码**：571–582
- **DOI**：10.1007/978-981-92-3381-6_46
- **Springer 官方页面**：  
  https://link.springer.com/chapter/10.1007/978-981-92-3381-6_46

---

## 2. 直接证据

Springer 官方页面公开摘要中写道：

> “Our approach extracts local subgraph features via multi-head attention and fuses them with target information (destination position, distance, and estimated hops) through a multilayer perceptron (MLP)…”

证据位置：

- **章节**：Abstract
- **论文页码范围**：571–582
- **官方链接**：  
  https://link.springer.com/chapter/10.1007/978-981-92-3381-6_46

这句话给出的处理顺序是明确的：

1. **先通过 multi-head attention 提取 local subgraph features**；
2. **再将这些图特征与 target information 融合**；
3. 融合发生在 **MLP** 中。

因此其公开描述对应的计算结构更接近：

$$
h_i^{\mathrm{GAT}}
=
\operatorname{GAT}(\mathcal{G}_i),
$$

随后

$$
Q_i
=
\operatorname{MLP}
\left(
h_i^{\mathrm{GAT}},
z_d
\right),
$$

其中

$$
z_d
=
\left[
\text{destination position},
\text{distance},
\text{estimated hops}
\right].
$$

而不是：

$$
m_{j\to i}
=
\phi(h_i,h_j,e_{ij},z_d),
$$

也没有公开证据表明其注意力权重采用：

$$
\alpha_{ij}
=
f(h_i,h_j,e_{ij},z_d).
$$

换言之，公开材料显示 **target information 不参与 GAT 的邻居消息或 attention coefficient 计算，而是在 GAT 得到局部子图表示后进入后续 MLP。**

---

## 3. A / B / C 判定

### A. 目的地只在 GNN 消息传递完成之后，作为额外输入拼给 DQN 头

**是。**

公开摘要明确采用：

$$
\text{local subgraph}
\rightarrow
\text{multi-head attention}
\rightarrow
\text{subgraph representation}
\rightarrow
\text{target information fusion via MLP}.
$$

因此属于 **A**。

### B. 目的地作为节点 / 边特征的一部分，在消息传递过程中真正使用

**未发现证据。**

当前公开方法描述没有显示：

- destination 编码进入节点初始化特征；
- destination 编码进入边特征；
- destination 进入 message function；
- destination 调制 attention coefficient；
- destination 在每一层 GNN propagation 中参与更新。

因此不能判为 B。

### C. 公开材料不足以判定

**不采用 C 作为最终判定，但存在正文可访问性限制。**

原因是：虽然当前没有拿到完整付费正文，但 Springer 官方摘要已经明确给出“先通过 multi-head attention 提取局部子图特征，再通过 MLP 与 target information 融合”的处理顺序，因此已经足以支持 A，而无需仅凭标题猜测。

但应保留一个证据边界：

> 当前结论针对的是**公开方法描述所明确呈现的架构顺序**。由于完整正文/结构图未公开访问，不能进一步断言论文正文绝对不存在某个未在摘要中说明的 destination-conditioned GAT 变体。

ResearchGate 页面同样显示该论文目前：

> **No full-text available**

可核验链接：

https://www.researchgate.net/publication/410540251_Target-Aware_GNN-DQN_Adaptive_Routing_for_LEO_Satellite_Networks

---

## 4. 对新颖性主张的影响

Cai et al. (2026) 已经占据了较宽泛的：

> **target-aware / destination-aware GNN-DQN routing**

因此不建议主张：

> “首次在 LEO GNN 路由中引入 destination information。”

这个表述过宽，容易被 Cai et al. 直接反驳。

但目前仍可保留更窄、机制级的主张：

> **Destination-conditioned message passing / destination-conditioned neighborhood aggregation**

其核心区别是：目的地信息并非在 GNN 输出后才进行 late fusion，而是在邻居消息构造或注意力聚合阶段直接改变信息传播。

你的目标机制可以写成：

$$
m_{j\to i}^{(l)}
=
\phi^{(l)}
\left(
h_i^{(l)},
h_j^{(l)},
e_{ij},
z_d,
\Delta_{ij}
\right),
$$

以及进一步的 destination-conditioned attention：

$$
\alpha_{ij}^{(l)}
=
\operatorname{softmax}_{j\in\mathcal N(i)}
\left[
a^{(l)}
\left(
h_i^{(l)},
h_j^{(l)},
e_{ij},
z_d,
\Delta_{ij}
\right)
\right].
$$

此时目的地

$$
z_d
$$

会改变**哪些邻居信息被传播、以及传播多少**，而不仅仅是在 GNN 得到固定图表示后影响最终动作评分。

---

## 5. 最终证伪结论

**Cai et al. (ICIC 2026)：A。**

根据 Springer 官方公开摘要，该论文的机制是：

$$
\boxed{
\text{GAT local-subgraph encoding}
\rightarrow
\text{target-information fusion in MLP}
}
$$

而不是：

$$
\boxed{
\text{destination-conditioned GNN message passing}
}
$$

因此：

> **这篇论文目前不能作为 destination-conditioned message passing 的反例，无法证伪该更窄的新颖性主张。**

但新颖性措辞应明确限定在：

> **destination information conditions the message-passing / neighborhood-aggregation process itself**

而不要扩大成：

> **destination-aware GNN routing** 或 **target-aware GNN routing**。

因为后两种宽泛表述已经被 Cai et al. (2026) 明确覆盖。
