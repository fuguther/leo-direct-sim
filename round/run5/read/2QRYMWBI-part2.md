# 2QRYMWBI 分片 2（覆盖行号区间 L501–L1000）

> 全文 1933 行；本片为第 2 片。**已逐字读完 L501–L1000 全部 500 行**，无跳读、无关键词检索。
> 读取方式：ssh vm + sed -n "501,1000p" 全量落盘后逐页读；对超过 2000 字符的 5 行（L566/L616/L618/L630/L858）另做定长切片补读，确保一字不漏。
> 本片性质：**这是一篇大综述的中段**，不是单篇方法论文。L501–L898 是综述主体（用例分类学 + 星上 AI 硬件盘点 + 开放挑战），**L900 起进入 REFERENCES**（L902–L1000 为 [1]–[50] 条目）。因此第 3/5 项（方法骨架/实验条件）按"综述片段"如实作答，不硬套实验论文口径。

---

## 1. 一句话

本片是"用例分类学 + 星上 AI 硬件盘点 + 开放挑战"三段主体（L504–L898）：把 SATCOM/NTN 里的 ML 工作按 11 个用例逐条归档（NOMA、RSMA、星座路由、IoT 接入调度、流量/拥塞预测、星地融合、边缘计算与缓存、ISAC、协同卫星、图像处理、地面段规划），随后盘点了可用于星上的神经形态处理器与 COTS AI 芯片（含每瓦算力实测/标称对比），最后列出部署位置、数据集、辐射、安全、成本等开放问题。

## 2. 问题设定

本片要回答的不是"某一个优化问题怎么解"，而是：**在卫星通信里用 ML，到底卡在哪**。它给出的三条主线麻烦：

- **算力/功耗/辐射约束**：星上部署受功率、质量、附加接口、散热、辐射限制；地面段则宽松得多（L683、L772、L798、L808、L810、L816、L830–L834）。
- **数据集与真实世界可核验性**：DL/DRL 需要大数据集才收敛，而用仿真器造大数据集"费时费钱"，且仿真数据的准确性本身就是开放问题；开源数据集几乎只有卫星影像（L822）。
- **没有成本-收益权衡**：作者明确说找不到任何"ML 潜在性能收益 vs 星上附加成本与复杂度"的权衡工作（L798 逐字见第 6 项）。

谁在什么条件下遇到麻烦：想上星上 ML 的载荷设计者（L798、L808、L818）、想做星地融合切片/编排的运营商（L592–L602）、以及想把 RL/DL 用到接入与路由的研究者（L504–L566）。

## 3. 方法骨架

本片**不是算法论文，没有自己的算法**。它的骨架是一套**统一的四段式分类学**，对每个用例依次展开：

a) Motivation → b) Description → c) Conventional Solutions and Issues → d) Proposed ML Solutions

本片内可完整看到的用例（含行号）：

| 用例 | 行号 |
|---|---|
| （上一片"用户调度"小节尾部） | L501–L502 |
| 2) NOMA 多址 | L504–L522 |
| 3) Rate Splitting (RSMA) | L524–L540 |
| 4) Constellation Routing | L542–L550 |
| 5) IoT Channel Access to Scheduling | L552–L566 |
| C. Upper Layers → 1) Traffic/Congestion Prediction | L568–L588 |
| 2) Integrated Satellite-Terrestrial Networks | L590–L602（含 TABLE IV，L596–L598） |
| 3) Edge Computing and Caching | L604–L618 |
| D. Others → 1) ISAC | L620–L634 |
| 2) Cooperative Satellite Communications | L636–L649（含 Fig.6，L644–L645） |
| 3) Image Processing | L651–L669 |
| 4) Ground Segment Dimensioning | L671–L679 |
| V. HARDWARE SOLUTIONS（A 神经形态 / B AI 芯片 / C 对比） | L681–L792 |
| VI. CHALLENGES AND OPEN DISCUSSION | L794–L898 |

对每个被引工作，本片记录的"主干"元素是：**优化目标 + 状态/动作/奖励（RL 类）+ 量化收益**。本片内 MDP/RL 结构交代最完整的三处：

- **[132] 随机接入（L566）**：状态 = 每颗卫星连接的设备数；动作 = 可用 RAO 数（离散集）；奖励 ∈ {1,0,−1}，取决于下一步利用率相对当前"更高/相等/更低"；状态转移概率对 contention-based 与 contention-free 两类接入**按 Poisson 过程解析给出**；约束是"传输时延低于给定阈值"，目标是最大化空闲 RAO 利用率；拥塞时启用 EAB。方案为 Deep Dyna-Q，并与 model-free Deep Q-learning 对比。
- **[127] CA-DRL（L562）**：经典 DAMA + RA 请求 + 动态信道分配 + DRL；优化在卫星侧；状态 = 带宽、传输完成时间、每时隙已调度传输数；奖励随"传输完成时间之和下降"而增大。
- **[82]/其扩展（L564）**：把任务（按大小与位置定义）分配到信道与波束的 MDP；动作空间 = 所有可能的信道分配，**通过"信道→波束"顺序分配来缩小动作空间**；奖励 = 功率管理与 QoS 满足（时间窗内服务阻塞率）的折中；用户请求被**编码成图像**作为 NN 输入以缩小输入规模、加速学习。

对非 RL 类，骨架是"用什么模型解什么非凸问题"：如 [120] MDP+DRL 做 age-optimal 功率分配（L520/L566）、[118] 用 DNN 把队列/信道状态映射到 SIC 解码顺序 + Lyapunov 优化转成在线子问题（L522/L566）、[113] Deep Belief Network 端到端解联合下行资源分配（L522）、[121]/[122] Deep Unfolding + 动量加速投影梯度下降（L540）、[116] 数据驱动学习 + 模型优化混合（L520/L878）。

## 4. 它声称的效果

**本片自身没有实验、没有图、没有自己的数字**。以下全部是它**转述被引工作**的量化结论（引用时须回引文核实，本片不为其真实性背书）：

- CA-DRL 把**请求满足时延降低最多 87%**，对比 **first-come-first-served 与 pure ALOHA**；**未与 CRDSA 等更先进技术比较**（L562）。
- 多波束 DRL 调度（[82] 扩展）：**能耗降低最多 67%**，对比 **random 与 greedy**；并在所有算法中最小化服务阻塞率（L564）。
- Deep Dyna-Q / model-free Deep Q：**接入效率相对经典动态 RAO 分配提升 3.5 倍**；Deep Dyna-Q 表现与 model-free DQ 相当，且不需要卫星与 IoT 设备间的反馈交互（L566）。
- IoT-STRN + NOMA 的 model-free Q-learning：**频谱效率相对 SA-NOMA 提升最多 18%**（L566）。
- CNN 做链路拥塞预测：在四类 ML 算法中最高，**达 98.3%**（L584）。
- CNN+LSTM 混合：对**某一波束**给出 **2 小时窗、5 分钟分辨率**的流量预测，用的是欧洲卫星运营商数月流量统计；**无法检测离群点与峰值**，只在趋势层面有效（L588）。
- 星上红外探测器算法的实测加速（[435]，L776）：**2k×2k 像素图像**下，CPU 实现相对 **LEON2 快 98 倍、相对 PowerPC 750 快 15.5 倍**；GPU 实现相对两者分别快 **806 倍与 128 倍**。
- XILINX 应用笔记（L788）：Versal AI Core VC1902 做 5G NR 大规模 MIMO 波束成形，**每瓦性能相对 Intel Agilex FPGA 提升 2.14 倍**。
- XILINX 方案简介（L790）：VC1902 做视觉/视频 AI 推理，**每瓦性能 2.7 倍于 Intel Agilex FPGA，功耗 87 W**（XPE 工具估算）。
- 每瓦算力（Fig.7 文字，L761–L766）：INT8 上 **Cloud AI 100 最好（2.8–5.33 TOPs/W）**，其次 Orin NX（3.5–4）、Orin Nano（2–4）、AGX Orin（2.7–2.83）、Versal AI Edge（0.55–2.69）；FP16 上 Cloud AI 100 为 1.4–2.6 TFLOPs/W、AGX Orin 为 1.35–1.41，Versal AI 该类数据未报告；FP32 上 **Versal AI Edge 最好（最高 221 GFLOPs/W）**，其次 Instinct MI200（151–171，矩阵运算）、Versal AI Core VC1902 AI Engine（最高 91）、Jetson AGX（CUDA 核，84.1–88.6）。
- 星上空间天气检测（[469]，L784）：FPGA 类中 **Versal ACAP AI Core 在 CME 检测与粒子检测推理上最好，Kintex Ultrascale KU040 最差**；单核 LEON4 的**未优化**实现已足够做星上检测且时延优于"下传后地面检测"；ARM Cortex A53 MPSoC 上的 CNN 比同平台 FPGA 实现**慢 5.8 倍**；SBC 类中 Unibap iX5 GPU 在 CME 检测最好，Myriad X 在粒子检测上**好 3 倍**。
- RA 方法（引 [353]，L560）：在高负载（**≥1**）下仍可达 **PLR < 1e-3**。
- 卫星图像超分（L669）：Cycle-CNN 在多光谱真实遥感卫星图像重建上表现好；RDN + 任意上采样 + 边缘增强模块恢复边缘纹理。

## 5. 它的实验条件

**本片是综述片段，没有自己的仿真、拓扑、规模或负载设定，也没有自己的训练/评估划分。** 这正是本片最大的信息缺口，需在第 9 项和第 7 项里作为事实陈述。

对"条件"的可提取事实只有零散几条，且都是被引工作的：

- **拓扑/规模**：本片**未给出**任何被引工作的卫星数、轨道面数、波束数、ISL 数等规模参数（L562/L564/L566/L584/L588 均无）。
- **负载**：仅两处触及——L560 提到"high (≥1) network loads"（无更细扫描范围）；L566 提到约束为"transmission delay under a given threshold"（未给阈值数值）。
- **到达过程**：仅 [132] 明确按 **Poisson 过程**解析给出转移概率（含 contention-based 与 contention-free 两类）（L566）。
- **训练/评估是否同源**：**本片无任何一处说明**。最接近的两条：(a) L566 明确 [132] "consider onboard training without, however, offering an overview of the demanded computational power"——即训练在星上但**算力成本未报告**；(b) L878 描述 hybrid 方法的范式是"训练集离线生成 → 用少量实测数据在线优化"，但这是方法描述而非实验条件。
- **硬件实测平台**（V-C 是唯一有明确平台清单的部分）：GPU4S 用 ARM Mali G-72、NVIDIA Xavier NX、NVIDIA TX2、AMD Ryzen V1605B（L774）；红外算法用 NVIDIA Jetson Xavier 的 GPU + Carmel CPU（L776）；空间天气检测用 Zynq-7000 SoC、Zynq Ultrascale+、Kintex Ultrascale、Versal ACAP、GR740/Leon4、Zynq US+ MPSoC 的 ARM Cortex A53、SBC Unibap iX5 与 Myriad X（L782）。
- **星地融合实测**：[370] 在 5G + 卫星网络上实现并演示端到端服务与 QoS 连续性（L600）；[372] 用信道模拟器 + 改造的 4G OpenAirInterface 协议栈在物理试验台上验证（L600）。**这两条是本片内唯一的"物理试验台"级证据**。

## 6. 它自己承认的局限（逐字引用）

本片是综述，所以"自述局限"表现为**作者对自己领域现状的否定式断言与对被引工作的点名批评**：

- L798：**"At this point, we could not identify any previous work where a tradeoff in terms of ML potential performance benefit versus added cost and complexity on the satellite device."**（本片最重要的一句自述缺口）
- L822：**"This review paper has shown that the development of the Machine Learning research does not go hand in hand with the development and availability of training datasets."** 紧接：**"it is pretty rare to find open high-resolution datasets for the other use-cases presented in Section IV. This makes it a tremendous challenge to compute the accuracy and scalability of the proposed Machine Learning models in the real world."**
- L630：**"Given these substantial challenges, research of Integrated Sensing and Communication for Satellite Communication is still in its infancy stage."**
- L677：**"The application of this field for the optimized design in the GS that allows selecting the position of the gateways based on criteria beyond the service requirements is still in its infancy."**
- L588（转述 [361] 的自限）：**"Despite it is not possible to detect outliers and peaks in traffic prediction, the results unveil predictions at trending level"**
- L562（对本片所引工作的点名批评）：**"However, no comparison is offered against more advanced techniques like CRDSA."**
- L566（批评 [132]）：**"consider onboard training without, however, offering an overview of the demanded computational power to run the proposed Reinforcement Learning algorithm."**
- L618（批评缓存类工作）：**"authors in [382], [383] have not considered improving the learning convergence rate of the distributed caching by coordinating the cache through satellite connectivity. Furthermore, backhaul and user link capacities were not included in the optimization model."** 以及对 [389] 的：**"it does not consider the backhaul cost, user link, cache storage limit, handling the dropped packets at the gateway, and the interaction between the macrocell and SBSs."**
- L880（对 hybrid ML 的判断）：**"we believe incorporating expert knowledge in Machine Learning models will receive increasing attention in the next future to overcome the conventional NN complexity"**（"will receive" = 现在还没有）

## 7. 它没做但看起来能做的地方（基于本片内容）

1. **"ML 收益 vs 星上成本/复杂度"的权衡研究**——作者自己说找不到（L798）。可做：把星上 ML 的算力、功耗、质量、冗余增量与性能收益放进同一个目标函数，做量化 tradeoff。
2. **面向非影像用例的开放数据集**——L822 明说 Section IV 的用例（接入、路由、缓存、切片……）几乎没有开放高分辨率数据集。自然下一步：可复现的仿真数据生成器 + 数据集保真度评估协议（且必须回答"仿真数据够不够真"）。
3. **统一评测协议**——本片反复点名三类缺失：没跟新基线比（L562，CRDSA）、没折算算力（L566）、没算回传/用户链路成本与缓存上限（L618）。把"算力 + 回传成本 + 强基线"三件纳入统一 benchmark 是直接可做的下一步。
4. **拓扑感知的流量/拥塞预测**——L586 指出 CNN/LSTM/全连接 DNN 忽略网络拓扑因而预测性能低，DCRNN 能捕捉拓扑性质但只在一般网络提出；把它搬到 **NGSO 时变拓扑**上是明显空白（且 L588 的 CNN+LSTM 明确测不到峰值）。
5. **异构算力卸载的端到端设计**——L616 的 [136] 已有"UAV（近）/ 地面 BS（算力强）/ LEO（覆盖广）"三者互补的卸载骨架，但本片未给出跨这三者的统一策略与代价模型。
6. **小卫星算力卸载**——L874 指出低轨 CubeSat/小卫星星上处理器信息处理能力"rather low"，提出用量子/天基量子云 + FSO 组网卸载算力，但完全是展望、无实验，是可落地的方向。

（不以"未见自述"收尾，因为本片自述缺口非常明确。）

## 8. 和同批其他篇的关系

**注意：本片无法判定"同批"是哪些 key**（分片任务未告知批次清单），以下只给**本片内可核验的引用关系**，供主控用全库 key 对照去重：

- 本片最重引的同族综述（若同批包含，则本片是它们的**下游引用者**）：
  - **[7] Kodheli et al., "Satellite Communications in the New Space Era: A Survey and Future Challenges," IEEE COMST 23(1):70–109, 2020（L914）**——本片在 L556（IoT 接入方式分类，引 [7, pp.92]）与 L606（边缘计算作为 B5G 卫星关键技术，引 [7]）两处把它当**事实来源**使用。
  - **[3] Ortiz et al., "Onboard processing in satellite communications using AI accelerators," Aerospace 10(2):101, 2023（L906）**——本片在 L707（星上/独立应用的最关键实现点）与 L808（ML 组件冗余增加卫星复杂度与研制成本）引用它，正好落在"星上 AI 硬件"这一本片核心章节。
  - **[16] Centenaro et al., "A survey on technologies, standards and open challenges in satellite IoT," IEEE COMST 2021（L932）**——L556 引用。
  - **[17] Homssi et al., "AI Techniques for Next-Generation Mega Satellite Networks," arXiv 2207.00414, 2022（L934）**、**[18] Fourati & Alouini, "AI for Satellite Communication: A Review," 2021（L936）**——与本片选题高度重叠，列在参考文献前段。
  - **[6] Azari et al., "Evolution of Non-terrestrial Networks from 5G to 6G: A survey," 2022（L912）**、**[12] Al-Hraishawi et al., NGSO 系统通信视角综述（L924）**、**[24] Zhu & Jiang, 星地融合面向 6G（L948）**（本片 L594 引用 [24] 列 6G-卫星融合挑战）。
- **像谁/不像谁**：本片像**分类学型综述（taxonomy survey）**，按"用例 × 四段式"组织；不像**方法型论文**（无自研算法、无自研实验）。与同为综述的 [7]/[18] 的区别在于本片把**硬件章节（V）与开放挑战（VI）单独成章且占本片约 1/3 体量**（L681–L898）。
- **是否引用同批其他篇**：无法判定（缺批次清单）。

## 9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实

本片**没有给出任何自己的到达率-时延曲线**，但有若干条可直接引用的相关事实（均为转述）：

1. **L562（CA-DRL）**：RA 请求场景下"请求满足时延"相对 FCFS 与纯 ALOHA **降低最多 87%**——本片内**唯一一条以时延为因变量的量化结论**。缺陷：**未给负载扫描范围**，也未与 CRDSA 比。
2. **L566（[132]）**：本片内**对"到达率→时延"建模最结构化的一段**——状态取"每星连接设备数"（即到达强度的直接写照），转移概率**按 Poisson 解析给出**（区分 contention-based / contention-free），**时延作为硬约束**（"keeping the transmission delay under a given threshold"），奖励按利用率升降取 {1,0,−1}；效果为接入效率 **3.5 倍**。缺陷：作者自己指出**未报告所需算力**。
3. **L564（[82] 扩展）**：奖励中**直接含"时间窗内服务阻塞率"**这一 QoS 满足度指标，并在所有对比算法中最小化该阻塞率，同时能耗降 **67%**——这是"负载 → 阻塞率"方向的一条事实（阻塞率与到达率强相关，但本片未给到达率轴）。
4. **L560**：RA 方法在高负载（**≥1**）下仍可达 **PLR < 1e-3**（引 [353]）——高负载下的丢包事实，无时延数据。
5. **L576–L578 + L584**：把拥塞定义为"**速率测量超过预设或动态调整的阈值**"，并指出**负载均衡本身不足以有效预防拥塞**，因此必须做拥塞预测；CNN 预测准确率 **98.3%**（L584）。
6. **L588**：波束级流量预测 **2 小时窗 / 5 分钟分辨率**，但**测不到离群点与峰值**——即"突变型负载变化"正是当前预测能力的盲区，这对"负载变化下"的课题是**否定性但有价值的事实**。
7. **L874**：低轨 CubeSat/小卫星星上处理器算力"rather low"——解释了为什么把动态负载响应放到星上是受限的。

**总结一句**：本片对"负载变化下到达率/时延"的贡献是**间接的、可引用的、但缺原始数据的**——最有用的是 L566 的 Poisson 到达+时延阈值建模范式、L562 的 87% 时延降幅、L588 的"峰值不可预测"否定事实；**不能**从本片直接得到任何到达率-时延的定量关系。

## 10. 一句话评价

这是一篇**组织型综述**而非方法创新：它把 2016–2022 年的 SATCOM+ML 工作按用例归档，并用一整章（V，L681–L792）给出星上 AI 硬件的实测/标称对比表；在方法谱系里它的位置是"**把已有 X 编目成一张用例-方法-缺口的索引，未提出新的 X**"。对本项目（LEO 直连仿真、负载变化下到达率/时延）真正有价值的不是它的方法，而是它反复点破的三件事：**没有成本-性能权衡研究（L798）、没有开放数据集（L822）、没有统一含算力与回传成本的评测（L562/L566/L618）**。

---

## 本片要点（供主控合并）

1. **本片 = 综述主体，不是方法论文，无自研实验。** L501–L898 为"用例分类学（L504–L679）+ 星上 AI 硬件盘点（V，L681–L792）+ 开放挑战（VI，L794–L898）"；**L900 起即 REFERENCES**（L902–L1000 为 [1]–[50]）。合并时不要把本片当作有实验的论文来提取"效果/条件"——第 4/5 项的数字全部是它转述他文。（L900、L902–L1000）

2. **作者自认的最大缺口（原话，最有引用价值的两句）**：L798 **"we could not identify any previous work where a tradeoff in terms of ML potential performance benefit versus added cost and complexity on the satellite device."**；L822 **"it is pretty rare to find open high-resolution datasets for the other use-cases presented in Section IV. This makes it a tremendous challenge to compute the accuracy and scalability of the proposed Machine Learning models in the real world."** 这两句可直接作为选题依据。（L798、L822）

3. **星上硬件是本片最硬的干货**（V-C，证据强度高于其他部分）：星上红外算法实测——CPU 版 98× (LEON2) / 15.5× (PowerPC 750)，GPU 版 806× / 128×（2k×2k 图，L776）；Versal AI Core VC1902 波束成形每瓦性能 2.14× Intel Agilex FPGA（L788）但 AI 推理需 87 W，**对星上过高**（L790）；作者结论是 **Versal AI Edge 每瓦性能区间最宽，是星上 SATCOM 的好选择**（L766）；AMD 首个宇航级 XQR Versal AI Core XQRVC1902 计划 2023 年初供货、Class B + 抗辐射、45×45 mm²，但**功耗与算力数据仍缺**（L792）。另注：**所有 COTS AI 芯片都不是 RHBD**（L774）。

4. **与"负载/到达率/时延"最相关的三条转述事实（全带基线，但全无原始曲线）**：① CA-DRL 请求满足时延 **−87% vs FCFS / pure ALOHA**，且**未与 CRDSA 比**（L562）；② [132] 用**每星连接设备数为状态 + Poisson 解析转移 + 时延阈值约束 + {1,0,−1} 奖励**，接入效率 **3.5×**（L566）；③ 波束级流量预测 2h 窗/5min 分辨率但**测不到峰值与离群点**（L588）。另有 RA 高负载（≥1）PLR < 1e-3（L560）、多波束 DRL 能耗 −67% 且最小化服务阻塞率（L564）、拥塞预测准确率 98.3%（L584）。

5. **去重提示（需主控用全库 key 对照）**：本片把 [7] Kodheli et al. COMST 2020（L914）、[3] Ortiz et al. Aerospace 2023（L906）、[16] Centenaro et al.（L932）、[17] Homssi et al.（L934）、[18] Fourati & Alouini（L936）当**事实来源/同族综述**引用；若这些篇也在同批 111 篇内，合并时应标注"同一事实被多篇综述重复"，避免把重复叙述当成多条独立证据。本片**无法自行判定批次成员**。
