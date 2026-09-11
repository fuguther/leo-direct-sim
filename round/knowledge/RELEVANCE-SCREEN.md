# 文献相关性筛查（RELEVANCE-SCREEN v1.0，2026-09-11）

> 起因：Codex 指出 `ETTA3DIV` 实为核聚变论文 —— **转换成功 ≠ 与本课题相关**。
> 方法：对全部 111 篇做程序化分层（领域/路由/RL 关键词计数）+ 人工核对标题。

## 分层结果

| 层 | 篇数 | 含义 | 处理 |
|---|---|---|---|
| **A 核心域** | 92 | 卫星/LEO/星座/ISL 域内文献 | **研究检索主入口** |
| **B 方法基础** | 15 | RL/网络方法经典（DQN/PPO/QMIX/Transformer/TD 学习/Q-routing） | 保留但**与域内分层**：仅用于 G3/G4 论证 |
| **C 无关** | 4 | 与课题无关 | **移出检索入口**；原件保留 |

## C 层明细（移出研究检索入口）

| itemKey | 标题 | 判定依据 |
|---|---|---|
| ETTA3DIV | Required toroidal confinement for fusion and omnigeneity | 等离子体磁约束聚变（Boozer, toroidal confinement） |
| A7QNRKML | LOTR: Face Landmark Localization Using Localization Transf | 计算机视觉（人脸关键点定位 LOTR） |
| VACUFEHB | COMPUTATIONALLY EFFICIENT ALGORITHMS FOR THIRD ORDER ADAPT | 信号处理（三阶 Volterra 自适应滤波器） |
| WT839JP7 | Fine-Grained Library Customization | 软件工程（代码膨胀与库裁剪） |

## 使用规则（检索纪律）

1. **域内证据只取自 A 层**；B 层用于方法论证（G3/G4：成熟 RL 为何不足），不作域内证据；
2. C 层**不得**出现在生成器/审查者检索入口；MD 索引中已标注 `[无关·已移出]`；
3. 原件（Zotero 条目 + VM 转换件）**一律保留**；
4. 新增文献须经同流程分层后才进入检索入口。

## 口径更正（Codex 第 2 条）

- 此前「2.0 GB Markdown」是**目录体积（含 MinerU 抽取的图片）**；
- **正文合计 10,411,191 字符 ≈ 10.4 MB**（见 `CONVERSION-SUMMARY.json` 的 `total_md_bytes`）。
