# 2QRYMWBI 分片 P4（覆盖行号区间 L1451–L1933）

> 论文：*Artificial Intelligence for Satellite Communication and Non-Terrestrial Networks: A Survey*
> 全文 1933 行。本片逐行读完 **L1451–L1933 全部 483 行**，无跳读、无关键词检索。

## 0. 本片性质（必须先说明，否则下面 10 项会误导主控）

**本片不含论文正文的任何段落。** 本片 100% 落在 `## REFERENCES` 之后——该节标题在第 899 行（"## REFERENCES"，见 L899–L901），第 900 行起进入文献表，一直延续到第 1922 行的 [501]。

本片行窗的构成：

| 行号 | 内容 |
|---|---|
| L1451 | 空行 |
| L1452–L1922 | 参考文献 **[270] – [501]**，共 232 条编号条目（含少量被 PDF 转换断成两行的条目） |
| L1924–L1926 | TABLE V 标题 + 表体 |
| L1928–L1930 | TABLE VI 标题 + 表体 |
| L1932–L1933 | TABLE VII 标题 + 副标题，**表体缺失，文件到此结束** |

因此，规范 10 项中凡属"正文题项"（第 1、2、3、5、6 项），本片**结构上不可能回答**；我按纪律逐项写明"不可回答"及其原因，并把本片**确实能提供的事实**（表格数值、引用结构、跨片依赖）填在相应位置，绝不编造。

---

## 1. 一句话：这篇做了什么

**本片无法回答**——本片无正文，无摘要、无引言、无结论。

本片能提供的最接近事实：这 232 条文献（L1452–L1922）覆盖的主题序列是——物理层安全 → 量子密钥/抗量子 → 预编码与调度 → NOMA/RSMA → 星地一体化与网络切片 → MEC 与缓存 → ISAC → 协同与星座规模 → 星载 AutoML/数据集 → 地面段与网关 → 神经形态 → 星载 AI 芯片 → 区块链 → 量子优化 → 模型驱动深度学习（主题边界行号见第 8 项的主题分区表）。这**只说明引用覆盖面**，不等于论文自身的贡献。

## 2. 问题设定

**本片无法回答**（无正文）。

可间接得到的一条事实：本片文献集中在第 V 章（硬件）与第 VI 章（挑战）的支撑材料上。其中 L1894–L1908 的 [487]–[494] 是区块链安全专题、L1874–L1884 的 [475]–[482] 是降维专题、L1910–L1922 的 [495]–[501] 是 TinyML 可持续性/量子优化/模型驱动深度学习/对地观测伦理/Ka-Q/V 馈电链路成本优化。**这一片文献全部是"引用他人的综述或器件手册"，本片内看不到任何一处是作者为回答某个问题而设的对照实验。**

## 3. 方法骨架

**本片无法回答**（无正文）。

可提供方法谱系的三段（按本片阅读所得）：

- **神经形态硬件谱系**：L1766–L1786 的 [424]–[433] —— [424] 神经形态计算用于卫星通信（ICSSC 2022）、[425] TrueNorth（65mW，100 万神经元，2015）、[426] Loihi（2018）、[427] Qualcomm Zeroth、[428] SpiNNaker、[429] BrainScales、[430] Neurogrid、[431] Braindrop、[432] Dynap-SE、[433] ODIN（28nm，0.086mm²，12.7pJ/SOP）。
- **星载 AI 芯片选型文献**：L1788–L1876 的 [434]–[471]。其中 [438]–[458] 几乎全是厂商官方文档（NVIDIA Jetson 全系 datasheet、Qualcomm Cloud AI 100、AMD Instinct MI200/MI210、AMD-Xilinx Versal AI Edge/AI Core），**属器件手册而非同行评议文献**。
- **第三方独立评测**：只有 L1848–L1862 的 [462]–[469]（ESA OBDP 2021 的高性能处理器/FPGA 综述、Ramon Space RC64、GPU4S 系列、OBPMark 基准、两个空间天气星载推理应用），以及 L1736 的 [409] SmartSat 星载机器学习报告。

→ 结论：第 V 章的方法骨架是"**器件参数对比**"，不是"提出新算法"。

## 4. 它声称的效果

**正文效果无法回答**（本片无正文）。

但本片承载了第 V 章**唯一的量化证据**，即 TABLE V / TABLE VI 的具体数值，逐字摘录如下：

**TABLE V — AI CHIPSET/ACCELERATORS OFF-THE-SHELF: CORE UNITS（L1924–L1926）**

| 器件 | 厂商 | CPU | 片上加速器 |
|---|---|---|---|
| Myriad Family | Intel | 2x Leon 4 RISC | Image/Video PA SHAVE |
| Jetson Nano | NVIDIA | 4x ARM Cortex-A57MP | 128-CUDA Maxwell |
| Jetson TX2 Family | NVIDIA | 2x ARM64b Denver | 256-CUDA Pascall |
| Jetson Xavier NX | NVIDIA | 4x ARM Cortex-A57MP / 6x ARM64b Carmel | 384-CUDA Volta / 2x NVDLA / 2x PVA |
| Jetson AGX Xavier Family | NVIDIA | 8x Carmel ARM64b | 48 Tensor / 512-CUDA Volta / 2x NVDLA / 2x PVA |
| Jetson Orin NX Family | NVIDIA | 6x/8x ARM64b Cortex-A78AE | 64 Tensor / 1024-CUDA Ampere / 1x/2x NVDLAv2 / 1x PVAv2 / 32 Tensor |
| Jetson AGX Orin Family | NVIDIA | 8x/12x ARM64b Cortex-A78AE | 1782/2048-CUDA Ampere / 2x NVDLAv2 / 1x PVAv2 / 56/64 Tensor |
| Jetson Orin Nano Family | NVIDIA | 6x ARM64b Cortex-A78AE | 512/1024-CUDA Ampere / 16/32 Tensor |
| Cloud AI 100 Family | Qualcomm | Snapdragon 865 MP Kryo 585 CPU | Cloud AI 100 |
| Instinct MI200 Familly | AMD | CDNA2 | 6656/14080-Stream Proc. / 104/220 Core Units |
| Versal AI Edge Family | AMD XILINX | 2x ARM64 Cortex-A72 / 2x ARM Cortex-R5F2 | 8-304 AI Engines/ML / 90-1312 DSP Eng / 43k-1139k System Logic Cells |
| Versal AI Core Family | AMD XILINX | 2x ARM64 Cortex-A72 / 2x ARM Cortex-R5F2 | 128-400 AI Engines / 928-1968 DSP Eng / 504k-1968k System Logic Cells |

**TABLE VI — AI CHIPSET/ACCELERATORS OFF-THE-SHELF: COMPUTER CAPACITY PEROPERATION（L1928–L1930）**
表头为：Device | "I8 (Ops)" | FP16 (FLOPs) | FP32 (FLOPs) | Power (W)

| 器件 | INT8 | FP16 | FP32 | 功耗 |
|---|---|---|---|---|
| Myriad Family | NR | NR | NR | 1~2 W |
| Jetson Nano | NR | 512G | NR | 5-10 W |
| Jetson TX2 Family | NR | X | NR | 7.5-20 W |
| Jetson Xavier NX | 21T | X | NR | 10-20 W |
| Jetson AGX Xavier | 30-32T | 10T | NR | 10-40 W |
| Jetson Orin NX | 70-100T Sparse / 35-50T Dense | X | X | 10-25 W |
| Jetson AGX Orin | 108-170T Sparse / 92-105T Sparse | 58-85T / 67-106T | 3.3-5.3T | 15-60 W |
| Jetson Orin Nano | 2-4T Sparse / 1-1.33T Dense | X | X | 5-15 W |
| Cloud AI 100 | 70-400T | 35-200T | X | 15-75 W |
| Instinct MI200 | 181-383T | 181-383T | 45.3-95.7T (Matrix) / 22.6-45.9T | 300-560 W |
| Versal AI Edge | 5-202T / 0.6-9.1T / 1-17T / 133T | NR | 0.4-16.6T / 0.1-2.1T / 8T | 6-75 W |
| Versal AI Core (VC1902) | 13.6T / 29T | NR | 3.2T | ~87 W |

（"NR" = 未报告，"X" = 该精度不可用/未提供。表体由 PDF 转换而来，**多行 rowspan 错位**，同一器件的多个数字落在不同行，摘录时已按器件归并，但归并本身带不确定性。）

**由这两张表可读出的事实**：星载可用的高算力器件集中在 NVIDIA Orin 系（Orin NX 70–100T INT8 @10–25W；AGX Orin 108–170T INT8 @15–60W）与 Qualcomm Cloud AI 100（70–400T INT8 @15–75W）；AMD Instinct MI200 虽达 181–383T，但功耗 300–560W（L1930），与星载功耗预算不兼容。**表内没有任何一项标注抗辐照等级（TID/SEE），也没有"每瓦有效算力"列。**

## 5. 它的实验条件

**本片无法回答**（无正文、无实验设置、无拓扑、无负载参数）。

本片能核对的**证据层级**：第 V 章的器件参数全部来自厂商公开文档（[438]–[458]，L1796–L1843，NVIDIA/Qualcomm/AMD-Xilinx 的 roadmap、datasheet、product brief、white paper），以及厂商性能指南 [459] Tensor Core DL Performance Guide（L1844）。独立第三方来源只有 [462]–[469] 的 ESA OBDP/GPU4S 系列（L1848–L1862）。**即：器件结论缺少作者自己的复现实验。**

## 6. 它自己承认的局限

**本片无法回答**——本片无正文，因此**未见自述**。已逐行读完 L1451–L1933 全部内容，其中除参考文献条目与三张表格外无任何论述性文字，故不存在"作者自述局限"的段落。

## 7. 它没做但看起来能做的地方（基于本片内容，非套话）

1. **补全 TABLE VII**。L1932–L1933 只有标题 "TABLE VII / AI CHIPSET/ACCELERATORS OFF-THE-SHELF: DIMENSION AND AVAILABILITY"，**表体在全文中完全不存在**，"尺寸与可用性"恰是星载选型（体积、质量、供货与宇航级可用性）的关键一列——这是一个可直接填补的缺口。
2. **给 TABLE VI 加"能效"列**。现有列只有峰值算力（INT8/FP16/FP32）与整板功耗（L1930），而星载的第一约束是功耗与散热；把 "70-100T @10-25W" 折算成 ops/W 才是可决策的量。
3. **加抗辐照维度**。TABLE V/VI（L1926、L1930）无 TID/SEE 标注，而抗辐照恰是"能否上天"的判据；本片所引的 [483] "Towards the use of AI on the edge in space systems: Challenges and opportunities"（L1886）与 [485] 新兴 ML 硬件路线图（L1890）本可支撑这一列，但表格没有做。
4. **补星载 NPU 之外的路线**。本片 [424]–[433]（L1766–L1786）列了 10 种神经形态芯片，但 TABLE V/VI 一个都没有收录——两条证据链在本片内是断裂的。

## 8. 和同批其他篇的关系

本片是 2QRYMWBI 自身的一片，**不涉及与其他篇的关系**（本片不含正文，无从判断引用关系）。

但本片发现一条**必须由主控处理的跨片依赖**：

- 第 V 章 `## V. HARDWARE SOLUTIONS` 标题在第 681 行，其小节 `## C. Hardware Analysis-Solutions Comparison` 在第 770 行（依全文标题索引）。
- 而 **TABLE V / VI / VII 的表体物理位置在 L1924–L1933，即本片**。
- ⇒ 读第 V 章的分片会读到正文对 Table V/VI/VII 的引用，**却读不到表体的任何数值**；合并成卡时这三张表必须由本片回填，否则第 V 章的"效果"一栏会是空的。
- （说明：我严格遵守不越界，未读 L681–L793 的正文；此处结论只依据标题索引行号 + REFERENCES 起始行 L900 + 表体所在行 L1924–L1933。）

**本片内部的主题分区（供主控定位）**：

| 行号 | 文献编号 | 主题 |
|---|---|---|
| L1452–L1458 | [270]–[273] | 物理层安全 / 多波束卫星 MIMO 保密 |
| L1460–L1484 | [274]–[285] | 量子：RSA 因式分解、QKD 基础（BB84/Ekert/MDI）、星地 QKD（Micius） |
| L1486–L1500 | [286]–[293] | 多波束预编码、深度展开 WMMSE、ESA MLSAT |
| L1502–L1518 | [294]–[302] | 电波传播/雨衰/网关分集、AI 电波传播、Deep Gateway Switching |
| L1520–L1532 | [303]–[309] | 成本（ROCSAT-1）、有源天线、RF 功放与数字预失真 |
| L1534–L1540 | [310]–[313] | LDPC 译码器 FPGA 实现与功耗 |
| L1542–L1570 | [314]–[327] | 用户调度与预编码（含 DVB-S2X、多播预编码、联合调度-预编码） |
| L1572–L1586 | [328]–[336] | 联合调度/预编码续、MIMO-NOMA、NOMA 星地中断性能 |
| L1588–L1602 | [337]–[344] | RSMA（速率分割多址）：多波束卫星、多网关、安全 |
| L1604–L1638 | [345]–[362] | 5G/B5G/6G NTN、星间路由、星载联邦学习、随机接入、**流量/拥塞预测** |
| L1640–L1662 | [363]–[372] | 3GPP 与 SaT5G/VITAL、网络切片、LEO 星座 5G 集成、NTN 随机接入 |
| L1664–L1700 | [373]–[391] | MEC、边缘缓存与主动缓存（含 Zipf、多臂老虎机、迁移学习） |
| L1702–L1724 | [392]–[403] | ISAC 通感一体化（含 LEO 大规模 MIMO 波束斜视、太赫兹通感） |
| L1726–L1748 | [404]–[414] | 协同下载、星座规模、星间通信、星载 AutoML、卫星视频目标跟踪 |
| L1750–L1764 | [415]–[423] | 地面段：馈电链路、网关选址与路由、地面站选择、ML 优化综述 |
| L1766–L1786 | [424]–[433] | 神经形态处理器谱系 |
| L1788–L1876 | [434]–[471] | 星载 AI 芯片（厂商文档为主）、OBDP/GPU4S 独立评测 |
| L1878–L1892 | [472]–[486] | 遥感数据集与降维、space edge AI、星载物联网 |
| L1894–L1908 | [487]–[494] | 区块链（空间信息安全、SAGIN 联邦强化学习卸载） |
| L1910–L1922 | [495]–[501] | TinyML 可持续性、QAOA 资源分配、量子×NTN、模型驱动深度学习、EO 伦理、Ka/Q/V 成本优化 |

## 9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实

**没有直接贡献。** 本片是参考文献区，不含任何实验结果、仿真或测量。

本片能提供的、与该主题**唯一相关**的是"这篇综述在这条线上的引用入口"，据此可判断主控能否指望它：

- **[358]** H. Nishiyama, D. Kudoh, N. Kato, N. Kadowaki, "Load balancing and QoS provisioning based on congestion prediction for GEO/LEO hybrid satellite networks," *Proceedings of the IEEE*, 2011 —— **L1626**。最直接相关：GEO/LEO 混合网 + 拥塞预测 → 负载均衡 + QoS。
- **[361]** P. Henarejos, M. A. Vazquez, L. Blanco, "Traffic congestion prediction in satellite broadband communications," ICSSC 2022 —— **L1632**。卫星宽带流量拥塞预测。
- **[359]** J. Wu 等, "Link congestion prediction using machine learning for software-defined-network data plane," CITS 2019 —— **L1628**；**[360]** Y. Li 等, DCRNN 交通流预测, ICLR 2018 —— **L1630**。两条都是**地面/通用方法来源**，非卫星负载场景。
- **[406]** R. Deng 等, "Ultra-dense LEO satellite constellations: How many LEO satellites do we need?" *IEEE TWC* 2021 —— **L1735**。星座规模-容量维度，非动态负载。
- **[335][336]** 不完美 CSI / SIC 下 NOMA 星地系统中断性能 —— **L1582、L1586**。涉及 "outage"，但是链路级而非负载级。
- **[345]** Vanelli-Coralli 等, "5G and beyond 5G non-terrestrial networks: trends and research challenges" —— **L1604**。趋势/挑战类，无数据。

**结论**：这篇综述在"负载变化 → 到达率/时延"上没有自己的实验；它在该主题上只提供"拥塞预测/负载均衡"的**引用入口**，且集中在地面 SDN 流量预测与 GEO/LEO 混合网（L1626–L1632）。**主控不要指望从 2QRYMWBI 拿到负载-时延的定量结论**；若要该主题的硬数据，应去读 [358]、[361] 原文。

## 10. 一句话评价

本片作为"分片"不含正文，其价值不在论证而在**两处结构性证据**：(a) 这篇综述第 V 章的**全部器件量化结论（TABLE V/VI）**与第 VI 章的引用基础都落在本片行窗内，且 TABLE VII 表体全文缺失；(b) 主控的 4 分片方案中，**第 3、4 片双双落在参考文献区**，真正承载论证的正文只有 L1–899。

---

## 本片异常清单（供主控录入质量台账）

1. **TABLE VII 表体全文缺失**：L1932 标题 "TABLE VII"、L1933 副标题 "AI CHIPSET/ACCELERATORS OFF-THE-SHELF: DIMENSION AND AVAILABILITY"，之后文件结束（共 1933 行）。
2. **引用编号失序**：[437]（L1792，LUXonis BW1099EMB Myriad X SoM）排在 [436]（L1794，G. Pang, "The AI Chip Race"）**之前**。
3. **两条文献共用同一 URL**：[446]（L1812，NVIDIA Jetson Orin Nano Series）与 [444]（L1818，NVIDIA Jetson Orin NX Series）都指向 `http://www.papersearch.net/view/detail.asp?detail{ }key=10000715`——两条不同的 NVIDIA 文档指向同一第三方页面，疑为引用错误。
4. **被 PDF 转换断成两行的条目**：[287]（L1486 + L1488）、[327]（L1568 + L1570）、[367]（L1650 + L1652）、[427]（L1772 + L1774）。逐字引用或做引文分析时须先拼接。
5. **TABLE VI 表头错误**：L1929 写作 "I8 (Ops)"，按列内容应为 **INT8**。
6. **TABLE V 错别字/错位**：L1926 "Instinct MI200 Familly"（多一个 l）、"256-CUDA Pascall"（Pascal 多一个 l）；"Jetson Xavier NX" 行的 Provider 单元格被 rowspan 并入 "NVIDIA"；"Versal AI Edge Family" 行被上方 "Instinct MI200" 的 rowspan=4 跨越，导致器件-厂商对应错乱。
7. **TABLE VI 行错位**：同一器件的多个档位数字散落在不同 `<td>` 行（如 AGX Orin 的 108-170T 与 92-105T），且 `rowspan="3"` 的 Orin NX 行内混入了下一个器件的 "20T Sparse"。**引用表内数字前须回原 PDF 核对。**

---

## 本片要点（供主控合并）

1. **【最高优先·分片方案问题】本片 L1451–L1933 是 100% 的参考文献 + 文末表格，不含任何正文。** 核对证据：`## REFERENCES` 标题在 **L899**（L899–L901），L900 起为 [1]；分片边界处 **L958 = [28]**（第 3 片起点 L961 已在文献表内）、**L1449 = [269]**、**L1450/L1451 为空行**、**L1452 = [270]**。⇒ **第 3 片（L961–L1450）同样全是参考文献。** 4 片分工中有 2 片（约 50% 阅读预算）花在文献表上，而全文正文只有 L1–899。**建议：把 L900–1933 合并为 1 片，释放出的 1 片预算投入正文**（如第 IV 章用例分析 L184–L680，或第 III 章 L108–L183、第 VI 章 L794–L899）。

2. **【跨片依赖·合并时必须回填】第 V 章（标题在 L681）所引用的 TABLE V / VI / VII，其表体物理位置在 L1924–L1933，属本片。** 读第 V 章的分片只能读到对表的引用、读不到任何数值 ⇒ 第 V 章读卡的"效果"一栏会空。合并成卡时这三张表须由本片补入。且 **TABLE VII（尺寸与可用性）表体在全文中完全不存在**，L1933 之后即文件结束。

3. **【本片唯一实质内容：星载 AI 芯片算力-功耗对照】** TABLE V（L1926）与 TABLE VI（L1930）给出：Orin NX 70–100T INT8 @10–25W；AGX Orin 108–170T INT8 @15–60W；Cloud AI 100 70–400T INT8 @15–75W；MI200 181–383T @300–560W（功耗与星载预算不兼容）；Versal AI Core VC1902 13.6T/29T INT8 @~87W；Myriad 1~2W 但算力 NR。**全部数字来自厂商 datasheet（[438]–[471]，L1796–L1876），无独立实测、无抗辐照等级列、无能效列。** 表体行错位严重，引用数字前须回原 PDF 核对（见异常清单 5–7）。

4. **【引用结构 / 质量】本片 232 条文献中 16 处出现 Chatzinotas（全文献表 L900–L1922 共 46 处）**，第 V/VI 章相关主题（预编码-调度、星地一体化、量子、神经形态）高度集中于该组论文与 ESA/OBDP 报告。另有编号失序（[437] 在 L1792 而 [436] 在 L1794）、两条不同 NVIDIA 文档共用同一 URL（[444] L1818 与 [446] L1812）、4 处条目被断行（[287]/[327]/[367]/[427]）、TABLE VI 表头 "I8" 应为 INT8（L1929）。

5. **【对选题的直接含义】本片对"负载变化 → 到达率/时延"没有任何直接贡献**（无实验、无数据）。本片内唯一相关的引用是 **[358]（GEO/LEO 混合网拥塞预测驱动负载均衡与 QoS，L1626）** 与 **[361]（卫星宽带流量拥塞预测，L1632）**，均为引用入口、不是本综述的结论。**不能从本片（以及这篇综述的参考文献）获得任何负载-时延定量事实**；需要时应去读 [358]/[361] 原文。

---
*读取方式：`ssh vm` + `sed` 分段逐行读，L1451–L1933 全覆盖，无关键词检索。*
