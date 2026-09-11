# 2QRYMWBI 分片 part1（覆盖行号区间 L1–L500）

**覆盖区间：L1–L500（逐字读完，无跳读）**
**全文体量：1933 行 / 398,804 字节（`wc -l -c` 实测）**
**本篇标题：Artificial Intelligence for Satellite Communication and Non-Terrestrial Networks: A Survey（L1）**
**作者：Gianluca Fontanesi 等 25 人（以 Univ. Luxembourg SnT 为主），IEEE 综述（L3–L5）**

本片覆盖：摘要 + 第 I 节引言 + 第 II 节 ML 概览 + 第 III 节 ML-assisted satellite system（含 onboard/on-ground 之争、工业界动态）+ 第 IV 节 Use Cases 的 **A. Low Layers 全部 15 个用例** 与 **B. Medium Layers 第 1 个用例（User Scheduling）前半**（L476 起，止于 L500）。

---

## 1. 一句话

这是一篇**按 OSI 分层组织的 SATCOM/NTN 用例地图式综述**：它把卫星通信拆成 Low/Medium/Upper 三层共 20 余个用例，逐个写"动机—描述—传统方案—ML 方案"四段，并在 Table III 里给每篇文献打上监督/无监督/NN/RL/DRL 的方法标签，同时贯穿一条"训练在星上还是地面（online/offline）"的实现视角主线（L7、L49–L59、L186、L189）。

它自己不下场做实验，全部内容都是对约 330 篇文献的分类与评述（引用编号在本片内最大到 [329]，L498）。

---

## 2. 问题设定

**谁在什么条件下遇到什么麻烦**（L13–L25、L110–L122）：

- 新太空时代 LEO/NGSO 崛起，用户需求**时间与地理双重依赖**，低轨卫星快速移动 → 催生波束赋形天线与可重构载荷，需要载荷配置能随流量需求自适应（L19）。这是全篇问题的总根。
- 现役 SATCOM 系统**大量依赖人工专家与手动干预**，两大弊端：① 人力控制带来高 OPEX 与高时延；② 新的射频环境变化太快，人工干预根本无法提供自主自适应机制（L21）。
- 未来用例将产生**海量数据**，卫星必须有能力从自身产生的数据里自动生成可靠动作（L21）。
- 载荷数字化（onboard channelization、干扰抑制、数字波束赋形、时间灵活性）解锁了灵活性，但**只有配上自动动态资源分配算法才能把这份灵活性变现**；ML 的定位正是"加速复杂优化流程、最小化人工决策"，并且 ML 也被认为是**网络负载预测**的好工具，而负载预测恰恰是决定"何时、如何重构载荷"的关键（L112）。
- 载荷非线性效应难以建模；地面段从 GEO 时代的少数网关走向**多网关（multi-GW）**（Ka 段拥塞推向 Q/V 段 → 需要站址分集；NGSO 因卫星移动而必须多网关），多网关环境类似蜂窝的 C-RAN，控制面逻辑集中、可做跨层全局优化，正是 ML 自动化的落点（L114–L118）。
- NGSO 的分布式特性带来高度动态、重叠的地面覆盖，衍生一串新问题：**用户星间动态切换（handover）、空间边缘处理、多星协同传输**（L122）。频率与时间失配需补偿，**星历精确估计与预测**是关键（L122）。

**本片第 IV 节每个用例各自的"麻烦"**（L197–L474）：天线设计全波仿真慢 + 在轨阵列无法做近场/远场测量来查故障（L199、L205）；多波束权值优化是带约束优化、星上算力/功耗受限（L219–L231）；波束跳变的搜索空间随波束数指数增长（L242）；功率/带宽"平均分配"遇上非均匀需求必然失配（L252、L270）；固定波束 footprint 无法服务机载/船载等移动宽带用户（L290）；ACM 存在 600–800 ms 的"死区"（L314）；频谱固定分配范式低效、还有故意干扰（L324）；分布式卫星系统需要严格时相同步（L334）；卫星攻击面大、算力受限故难上强密码（L356）；QKD 对环境极敏感、传统"先扫描再传输"有显著停机时间（L380）；预编码矩阵求逆复杂且随调度用户变化需重算（L408）；地面段网关切换需要分钟级延迟的链路质量预测（L420–L430）。

---

## 3. 方法骨架

**这不是一篇提出算法的论文，它的"方法"是分类学 + 综述方法论：**

- **综述方法论**（L67）：先穷举 SATCOM 用例与研究领域及其挑战，再在 IEEE / MDPI / Elsevier / Wiley 四个库中检索传统方案与 ML 方案，**只收期刊与会议论文**；第二轮靠人工检索与个人知识补充。相关综述的检索结果汇总在 Table I（L61–63）。
- **贡献声明四条**（L51–57）：① 按 OSI 导向架构对 SATCOM/NTN 最重要的用例做广谱分类；② 对每个用例给描述、挑战、传统工具、主要 ML 技术，并按"训练在星上还是地面"分类；③ 评估当前与下一代处理器硬件版图，横向比较商用 AI 芯片的 SATCOM 适用性；④ 分析未来网络部署视角下的挑战与未来趋势。
- **结构**（L59）：六节 —— ML 框架简介（明确声明**不讲各种 ML 方法怎么运作**，只给 [22][23] 之类指引）→ 第 III 节 AI 在 SATCOM 中的角色（onboard vs on-ground）→ 第 IV 节用例大全 → 第 V 节硬件 → 第 VI 节挑战与未来方向。
- **三层分类**（L186、L191、L193）：把传统 OSI 层归并成 **Low Layers / Medium Layers / Upper Layers** 三层。
  - Low：Beamforming、Flexible Payload、Link Adaptation、Spectrum Sensing、Interference Management、Intersatellite Synchronization、Precoding、Link Quality Prediction、Predistortion、Coding。
  - Medium：User Scheduling、NOMA Access、Rate Splitting、Constellation Routing、IoT Channel Access Scheduling。
  - Upper：Traffic/Congestion Prediction、Integrated Satellite-Terrestrial、Edge Computing and Caching、Network Security。
  - Other：ISAC、Cooper. Satellite Commun.、Img Processing、Ground Segment Dimensioning。
- **每个用例的固定四段模板**（L186）：(i) Motivation、(ii) Detailed Description、(iii) Conventional solutions、(iv) ML solutions。Table III（L189 的 HTML 表格）是"用例 × ML 框架 × 文献编号"的索引矩阵，列分为 Supervised / Unsupervised / NN&DL / RL / DRL / F（F 列疑似 Federated）。表格说明还标注了 **INMAGENTA 高亮 = offline ML training，INCYAN 高亮 = online**（L188）。
- **贯穿全文的主轴判据**（L136–L153）：AI 芯片在星上还是地面站；以及训练的 online/offline。作者给出 **Table II 的 online/offline 利弊对照**（L155–157）：
  - Online 优点：Lower Latency / Improved Autonomy / Flexibility to adapt to unforeseen changes / Higher Privacy；挑战：Limited Computing Capacity on-board / Longer Processing Time / Limited Power / **Radiation Tolerance**（辐射容限）。
  - Offline 优点：Reduced processing time / Large computational resources；挑战：Not flexible to sudden network changes / Inaccurate in unexpected situations / Higher Latency。
- **术语澄清**（L143）：online 指系统运行中训练，**不论 ML 硬件在星上还是地面**；offline 指系统不活跃时在地面用训练库 + 强 GPU 服务器训练。混合架构：先 online/offline 训练、再用新采集数据更新（L153）。
- **轻量化工具箱点名**（L153）：MobileNets、ShuffleNet、PeleeNet，以及 Model compression、Neural Architecture Search；另一路是"把 ML 算法适配到卫星受限算力"（L153 引 [55]）；或软硬件协同设计在硬件层利用模型压缩。

**ML 基础概念部分（第 II 节，L73–L106）** 是本片前半的方法学铺垫，逐条读了：AI/ML/DL 关系（L77–L85，Fig.1 在 L87–88）；分类/回归/结构化学习（L81）；监督（Naive Bayes、KNN、随机森林、NN、SVM、决策树，L94–96）、无监督（K-means、SOM、HMM、RBM，L98）、**半监督（L100，含 pseudo labeling、manifold/low-density/clustering/smoothness 四假设、EM↔clustering 假设、transductive SVM↔low-density 假设）**、强化学习（L102–106，model-based / model-free，agent + state + action、累积折扣回报、Q 函数/Q-learning 表）。两个关键论断：**RL 的主要优势是不依赖环境的精确数学模型**，且能处理含即时与未来回报的长期优化（L104–L106）；**但状态/动作空间大时难以直接建模每一对 state-action，因此"RL 在实践中很难被使用"（L106 逐字：Reinforcement Learning is hardly used in practice [46]）**。

---

## 4. 它声称的效果

本篇自身无新实验；以下是它**转述的被引文献的数字**，全部带条件（括号内为原文给出的条件）：

- **预编码 / ESA MLSAT**（L410）：两步自编码器方案（第一步学真实信道与估计信道矩阵的映射，第二步从已求逆的估计信道矩阵预测预编码矩阵，从而绕开学习复杂矩阵求逆）；据 ESA MLSAT 项目报告，**平均 SINR 提升 3 dB**。
- **CSI 预测（供 ACM 用）**（L320）：ML 预测模型带来**平均容量提升至多 10.9%**，且开销可接受。同段还有一条 FPGA 硬指标：面向 LEO 的高速率 ACM 方案达到**频谱效率 7.068 bps/Hz（码率 0.8889 的最高速率模式）**（L318）。
- **链路质量预测**（L426）：自动功率控制可对抗 **10–12 dB** 衰落；要 99.99% 地面站可用率，站点须选在年降雨量低于阈值的区域；超出 12 dB 必须依赖 **N+P 网关分集**（N 个标称网关可被 P 个冗余网关替代）。
- **帧同步**（L346）：CNN + softmax 同步模型相对直接相关检测，在正确检测帧头位置上**提升 2 dB**。
- **GNSS 欺骗检测**（L364）：SVM，用码/相位/多普勒/信号强度特征（1 Hz 采样），多数据集上**准确率 > 98.5%**；攻击设定为"中间人授时攻击"，通过模拟卫星钟漂影响接收机钟差。
- **GNSS 欺骗检测（算法横比）**（L366）：SVM-RBF / KNN / AdaBoost / 决策树 / 随机森林对比，**在该场景下简单决策树反而胜过其他方法**，且误报率极低。
- **天线指纹（物理层认证）**（L368）：RNN 捕捉时变特征，在多个 LEO 场景下 **198 天内准确率 99.34%**，且是在**天线因环境因素退化**的条件下取得的。
- **QKD 参数预测**（L382）：LSTM 实时预测并主动控制 QKD 设备，**连续 10 天**稳定；在 QBER 与密钥传输率上与"扫描-传输"传统方案相当，但省掉了扫描停机时间 → 连续运行时系统效率高。另一条（L382）：NN 预测自由空间 QKD 最优参数，在 **Raspberry Pi 3 与手机上运行、功耗 < 5 W**，相比暴力搜索**加速 2–4 个数量级**，同时保住给定协议最优安全密钥率的 **95%–99%**。
- **QKD 协议选择**（L384）：随机森林在给定环境（暗计数率、单光子探测器效率、失配误差率、传输距离）下选最优 QKD 协议，**准确率 > 98%**，优于 SVM/KNN/CNN。
- **载波恢复（CV-QKD）**（L386）：无迹卡尔曼滤波，**20 km 光纤**链路，即使在低导频功率下也表现出低方差与高稳定性的过量噪声。
- **FEC 解码功耗（与"硬件可行性"直接相关）**（L472）：DVB 标准码率 (64800, 29160) 下，LDPC 解码 **12.92 W @ ~4 Gbps**；对最大功耗 50 W 的卫星，**单条接收链的解码就占总载荷功耗 25.84%**；对 CubeSatKit 这类 2 W 预算的小卫星，该吞吐率下的解码**根本不可能**；若 HTS 有 200 个波束、每波束一条同等功耗的 FEC 解码链，总功耗按比例增加约 25.8%。
- **5G 解映射+解码联合方案**（L474）：自编码器 + DNN 组合方案相比传统"星座解映射 + LDPC 解码器"可获得 **3 dB SNR 增益**，且可通过 MIMO 空域分集继续扩大；作者点名为"5G 网络卫星集成的候选方案"。

---

## 5. 它的实验条件

本篇是综述，**没有自己的仿真** —— "实验条件"只能记录它转述的各被引工作的条件与本综述自身的取材边界：

- **取材边界**（L67）：仅 IEEE / MDPI / Elsevier / Wiley 的期刊与会议论文；两轮检索（系统检索 + 人工补充）。
- **范围裁剪**（L15）：NTN 本包含 GEO/MEO/LEO 星座、HAPS、LAPS、空对地网络，但本综述**只覆盖 GEO/MEO/LEO 卫星通信系统**。
- **转述工作中出现真实条件的几处**：
  - DRL 连续功率分配 [78]：用 **SES 提供的时序需求数据**评估，作者证明算法能匹配波束需求（L264）；同一 DRL 模型在 [79] 中与元启发式对比，结论是**时间紧迫、需要秒级解时 DRL 是最合适的选择**（L264）。
  - DRL 带宽分配 [83]：以**地面网关为 agent**，以时频资源块数与用户需求为环境状态；仿真结论是资源利用率优于**遗传算法（GA）与蚁群算法（ACO）**，且计算复杂度低（L284）。
  - DRL 信道分配 [81]：假设**离散时间事件系统、以服务到达事件驱动**，卫星检查给新到达用户终端分配哪个信道；优化目标是**降低系统阻塞概率**（L282）。
  - 波束跳变 DRL [73]：DVB-S2X 场景，两个目标 —— **最小化实时业务传输时延 + 最大化非即时业务吞吐**；用 model-free 多目标 DRL，为处理动作维度灾难提出 **Double-Loop Learning (DLL)** 多动作选择法，多维状态由深度网络重表征（L246）。
  - 波束跳变 MADRL [74]：把带宽与波束图样的联合分配拆给多 agent，**每个 agent 只负责一个波束的照射分配或带宽分配**，agent 间通过共享同一奖励学会协作；目标为吞吐最大 + 小区间时延公平最小（L246）。
  - 波束宽度管理 [85]：对比 **Q-Learning / Deep Q-Learning / Double Deep Q-Learning** 三者在性能、复杂度、附加时延上的差异，并证明**去中心化协作多智能体（CMA）分布优于单智能体**（L308）。
  - 干扰检测 [91]：incumbent 系统为 **DVB-S2**，两级结构（自相关器检测 + DNN 分类 LTE/UMTS/GSM 三类干扰），结论是**一个分类器即可同时检测与分类**，无需每类信号一个分类器（L330）。
  - 频谱共享 [246]：GEO/NGSO/地面网共享同频，下行 Ka（17.7–19.7 GHz）、上行 Ka（27.5–29.5 GHz），**地面网是 incumbent（primary）**（5G 固定无线接入 + 微波链路）；卫星侧多址为 **MF-TDMA**，地面侧为 FDMA（L328）。
  - 用户调度（L492–L498）：地理调度（经纬度分组，无需上报 CSI，[318]）、欧氏距离相关性（[319]）、图论 Least Beam Collision（[320]）、部分 CSI 避免同时调度干扰波束用户（[323]）、余弦相似度顺序选正交信道向量用户（[325]）；关键对照结论是**地理调度在晴空 + 理想前馈补偿下与完美 CSI 同结果，但接近真实操作并考虑衰落时会出现差异**，此时按欧氏距离分组表现仍良好，考虑移动性也成立（L496）。
- **训练与评估是否同一套**：综述未给统一口径；只在 [75][76] 处点明"训练离线完成，因此资源分配计算代价低，但类别数随波束数指数增长会推高复杂度"（L260），以及在 [84] 处点明 CNN 依赖训练所用流量模型、真实流量偏离模型时必须重训（L260、L306）。

---

## 6. 它自己承认的局限（逐字引用）

综述自身的取材局限未设独立小节；以下均为作者在正文中**明确写出的空白与不足**（逐字给原文片段 + 行号）：

- **L211**：we have not identified relevant works in compensation of faulty elements using Machine Learning, which represents a gap to be filled by the research community in the next years.
- **L302**：However, they do not implement adaptivity in terms of flexible beam size and beam position in the beam plan. So far as we are aware, the authors have yet to consider the mobility aspects of non-uniformly distributed users and dynamically to change beam demand during beam pattern and footprint planning.
- **L310**：However, implementing ML to enhance flexibility in geographical positioning has yet to be explored as another possible resource in addition to beamwidth.
- **L344**：Even when there has not yet been any distributed satellite mission performing inter-satellite synchronization with Machine Learning techniques, ...（即：星间同步的 ML 方案**尚无在轨分布式任务验证过**）
- **L464**：While the application of Machine Learning techniques in the field of Digital Predistortion techniques in the field of satellite communications is still limited, we expect a widespread rise in the next future.
- **L500**（本片最后一整段，句末）：Nevertheless, the study does not consider the impact of nonuniform traffic requests on scheduling decisions.（针对 [111] 的聚类调度）
- **L106**：Consequently, Reinforcement Learning is hardly used in practice [46].（作者对 RL 落地难度的直言）
- **L412**：While ML for multi-antenna transmission has been well explored in terrestrial systems [290], [291], there are very few works published on the SATCOM domain.
- **L149**（对 onboard 训练的判词）：implementing such training can be challenging due to the relatively high convergence length and the limited computing capacity onboard [53]，且模型 often have to trade off against processing time, memory, number of computational operations and energy consumption。
- **L151**（对 offline 的判词）：However, this architecture strongly depends on the training data and models used... the model may present significant errors in unexpected situations in the system.
- **L130**：onboard 策略增加卫星复杂度与质量/功耗，且 there is very little chance of repairing/replacement after the asset is put in orbit [7]。

---

## 7. 它没做但看起来能做的地方（基于本片内容）

- **故障阵元补偿（L211 自认空白）**：本片已列了故障检测的 ML 工作（ANN [65]、DL [62]、SVM [63]），但"检测到之后怎么补偿"完全空缺。作者在 L205 交代了传统补偿要"改变其余阵元的幅度/相位"很费时 —— 这正好是一个"检测 → 补偿"闭环的 RL/优化问题。
- **波束地理位置的 ML 化（L310 自认空白）**：搜索空间大是作者给出的理由，正是 model-free DRL 的典型应用面。可把"波束中心位置"作为连续动作，和已有的波束宽度/功率/带宽维度合成一个联合动作空间。
- **星间同步的在轨验证（L344 自认空白）**：已有工作只在端到端链路、帧同步/采样频偏/载波同步/相位噪声表征上验证，**没有任何分布式卫星任务在轨跑过 ML 同步**。作者同时指出分布式系统需严格时相同步 —— 这暗示"用 ML 替代迭代式反馈环"的在轨可行性验证是空位。
- **RL 大空间问题的规避（L106 与 L246 呼应）**：作者说 RL 因大状态/动作空间"难以实用"，但同一节里 [73] 用 DLL、[74] 用 MADRL 分解动作空间来绕开。**"如何系统化地把 SATCOM 的大动作空间分解成多 agent"本身没有被综述者归纳成方法论** —— 这是一个可提炼的研究点。
- **在线/离线混合架构的定量边界（L153 提出混合，但没给量化判据）**：Table II（L157）只给了定性利弊。缺的是"在给定星上算力/功耗/辐射容限与给定需求变化速率下，何时该 online、何时该 offline、何时 hybrid"的判据。
- **辐射容限（L157）被列为 online 训练挑战，但本片 500 行内没有任何一篇被引文献真正量化辐射对在轨训练的影响** —— 空白。
- **跨用例的方法复用（L416 提示）**：作者说 SATCOM 预编码的 ML 可以借鉴地面域进展。同理，本片里"用户聚类"（L500，无监督 K-means++）、"CSI 时序预测"（L320，ORRF/贝叶斯）、"链路质量预测"（L438，DL 时序 + 外部天气特征）三者共享同一套时序/聚类工具，但综述按用例切块、没有横向打通。

---

## 8. 和同批其他篇的关系

**本片无法完成这项判断** —— 我的阅读范围是 2QRYMWBI 的 L1–500，里面**没有出现本批次其他论文的标识**（没有其他 8 位 key、没有"同批"字样）。本片内只能看到两种外部关系：

1. **与更早综述的关系**（Table I，L61–63）：作者把自己和 [1][6][24][7][25][8][10][11][12][13][14]（SACOM 类，ML Focused = No、Implementation Oriented = No）、[15][16][21][18][2][17][19][20][26]（MO & COM 类，其中 [18][2][17][19][20][26] 的 ML Focused = Yes）逐条对比，**只有 "This work" 一行在 Implementation Oriented 列标 Yes**。作者对既有综述的具体批评在 L45：Other works address Deep Learning only [19], [20] or Artificial Intelligence for space missions [21], without however addressing the challenges of onboard or on-ground computing, hardware constraints and limitations.
2. **自身定位**（L49）：A detailed survey of this type was still missing... with an implementation perspective.

若主控需要跨篇关系，只能按"这篇是 SATCOM-AI 综述中覆盖面最宽、且是唯一带硬件实现视角的一篇"这一坐标去和同批其他篇对表；**本片不提供同批内证据**。

---

## 9. 对"负载变化下到达率/时延"这件事，它贡献了什么事实

本片提供了**若干条可直接引用的事实**，集中在 Medium Layers 与几个地面段小节：

1. **非均匀需求 vs 均匀分配 = 需求不满足**（L252、L270）：多波束 footprint 若按每波束均匀功率/带宽分配，低需求波束被超额分配、高需求波束分配不足，"we may be unable to meet some users' demands"。这是"负载变化 → 到达率受损"的最基础机制陈述。
2. **阻塞概率与到达事件是显式建模对象**（L282）：[81] 假设**离散时间事件系统、由服务到达事件驱动**，卫星对每个新到达用户终端决定分配哪个信道，奖励在新服务被满足时为正，**优化目标就是降低阻塞概率**。这是本片里与"到达率"最直接对应的一条。
3. **时延被拆成两类业务分别优化**（L246）：[73] 明确同时最小化"实时业务的传输时延"与最大化"非即时业务吞吐"，并针对**差异化的业务到达率**与不可预测信道，用 model-free 多目标 DRL 学策略。[74] 的目标同样是"吞吐最大 + 小区间时延公平最小"。
4. **固定时延常数（可直接引用的数字）**：
   - ACM 死区 **600–800 ms**，成因是两跳卫星 + 额外平均延迟；期间若 SNR 下降会出现帧错误（L314）。
   - 网关切换：决策到实际切换完成**需要几分钟**，切换后所有终端须与新地面站重新同步，带来不可忽略的附加时延；**短于该延迟的中断不应触发网关切换**（L428）。
   - 信道样本在**几秒量级**的时滞下即变得不相关（L422）。
   - 数学传播模型在 **1 分钟以内**的短期预测表现良好，但网关切换需要**几分钟**的预测窗，因此必须引入外部天气预报信息（L432、L434、L446）。
   - 自动功率控制上限 **10–12 dB** 衰落，超出则须走 N+P 网关分集（L426）。
5. **对预测精度与容量的量化**（L320）：ML 做 CSI 预测使系统平均容量提升至多 **10.9%** —— 这是"负载/信道变化条件下把容量损失补回来"的直接证据。
6. **覆盖/容量失配的度量被形式化为 KPI**（L292–L300）：波束宽度分配的核心 KPI 是**"提供的容量与所需容量之间的差距"（Offered Capacity Error）**与 **Normalized Coverage Error**；[226] 用"在轨每 Gbps 成本 + 归一化覆盖误差 + 每波束提供容量误差"作代价函数。这是"需求-供给错配"在 SATCOM 里的标准度量语言。
7. **本片没有给的**：500 行内**没有任何一篇被引文献报告"负载变化下的到达率/时延曲线"或排队模型数值**（没有 M/M/1、没有丢包率-负载曲线、没有端到端时延分布）。L244 描述 [189] 时提及"shorten the packet queueing delay"，但那是描述传统波束跳变方案的一句话，**未给数字**。

---

## 10. 一句话评价

**这是一张"用例 × ML 方法 × 训练位置"的三维索引图，而不是一个新方法**：它把已有的 SATCOM 优化问题（功率/带宽/波束宽度/波束跳变/调度/预编码/链路预测/干扰分类/QKD/认证/DPD/FEC）逐个贴上"传统解法 vs ML 解法"的对照标签，并额外加了一列别人没加的判据 —— 训练在星上还是地面（Table II，L157）。在方法谱系里，它的位置是**"把已有 ML 工具原样映射到卫星场景，未改工具本身"**：本片里所有 ML 方案都是把地面成熟的 CNN/RNN/LSTM/随机森林/SVM/K-means++/Q-learning/DRL 直接搬到 SATCOM 问题上，作者自己也在 L416 承认"SATCOM 预编码可以借鉴地面域的进展" —— 即**跨域迁移而非方法创新**是这篇综述所刻画的研究现状，也是它留给读者的最大空白。

---

## 本片要点（供主控合并）

1. **【这是一篇无实验的用例地图式综述，唯一独有维度是"训练位置"】**：25 位作者，六节结构（L59），按 OSI 把用例归并成 Low/Medium/Upper 三层（L191、L193），每个用例走"动机—描述—传统方案—ML 方案"四段模板（L186）。Table I（L61–63）显示**只有本篇在 Implementation Oriented 列标 Yes**，作者自我定位是"带实现视角的此类详综述此前一直缺失"（L49）。其方法论是四库（IEEE/MDPI/Elsevier/Wiley）期刊 + 会议两轮检索（L67），范围**只覆盖 GEO/MEO/LEO，排除 HAPS/LAPS/空对地**（L15）。

2. **【online vs offline 的判据表是本篇最有复用价值的一张表（L155–157）】**：Online 好处 = 低时延/高自主/适应未预见变化/高隐私，代价 = 星上算力有限/处理时间更长/功耗受限/**辐射容限**；Offline 好处 = 处理时间短/算力资源大，代价 = 不适应突发网络变化/异常场景不准/时延更高。作者对两者的判词分别是"onboard 训练收敛长度高 + 星上算力受限"（L149）与"offline 严重依赖训练数据与模型、在意外情境下可能显著出错"（L151），并提出**混合架构**（先训后用新数据更新）作为出路（L153），但**未给任何量化切换判据**。

3. **【与"负载变化下到达率/时延"直接相关的事实，本片共 3 条硬料】**：① [81] 显式假设**服务到达事件驱动的离散时间系统**，优化目标即**降低阻塞概率**（L282）；② [73] 在 DVB-S2X 下**同时优化实时业务时延与非即时业务吞吐**，且明确面对**差异化业务到达率**，靠 model-free 多目标 DRL + Double-Loop Learning 处理动作维度灾难（L246）；③ **固定时延常数** —— ACM 死区 **600–800 ms**（L314）、网关切换**需几分钟**且切换后全网终端须重新同步（L428）、信道样本**几秒**即去相关（L422）、传播模型短期预测有效期 **< 1 分钟**而网关切换需**几分钟**故必须引入外部天气预报（L432、L434、L446）。**但本片没有一篇文献给出"负载-到达率/时延曲线"的数值或排队模型**。

4. **【作者自认的空白共 6 处，可直接当选题线索】**：① 故障阵元的 **ML 补偿**尚无相关工作（L211）；② 波束图样规划**未考虑非均匀分布用户的移动性**与动态需求变化（L302）；③ **波束地理位置的 ML 化"尚待探索"**（L310）；④ **星间同步的 ML 方案无任何在轨分布式任务验证**（L344）；⑤ SATCOM 的 ML 数字预失真工作"仍然有限"（L464）；⑥ 多播预编码的聚类调度**未考虑非均匀流量请求对调度决策的影响**（L500）。另加两条作者对 RL 的直言：**"RL 在实践中很难被使用"**（L106），以及 SATCOM 域的 ML 多天线传输工作**"极少"**（L412）。

5. **【可直接引用的量化事实（含硬件功耗天花板）】**：ML 预编码（ESA MLSAT 两步自编码器）**平均 SINR +3 dB**（L410）；ML CSI 预测使**平均容量 +10.9%**（L320）；RNN 天线指纹在**天线退化条件下 198 天准确率 99.34%**（L368）；NN 预测 QKD 参数**加速 2–4 个数量级且保 95–99% 最优密钥率、功耗 < 5 W、可跑在树莓派和手机上**（L382）；**FEC 解码功耗硬顶** —— DVB (64800, 29160) 下 LDPC 解码 **12.92 W @ ~4 Gbps，占 50 W 卫星载荷功耗的 25.84%，在 2 W 预算的 CubeSatKit 上根本不可能**（L472）；5G 联合解映射 + 解码方案 **+3 dB SNR**（L474）。另有一条在轨部署事实：ESA 2020 年用 Intel Movidius 芯片在 **6U CubeSat Φ-Sat-1** 上做地球观测的在轨 DL 推理（L174）。

---

**读卡者备注（供主控判断本卡可信度）**：本片 L1–L500 已逐行读完，未使用关键词检索。L188 与 L189、L191 三处为 MinerU 抽取的 HTML 表格，单元格存在 OCR 讹误（如 L188 的 "MLANDSATELLITECOMMUNICATION"、L189 表头 "Supvvsed/Unsed/N28ND"），我在本卡中只引用其可辨识的语义（层名、方法列名、文献编号），未据讹误字面推断结论。L500 是 Medium Layers 第一个用例的 (d) 段末尾，本片在此截断，User Scheduling 的后续内容在下一片。
