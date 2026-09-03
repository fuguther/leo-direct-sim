# 查新报告：card-01-fi（F-I 拓扑动态×决策失配）— 终稿查新轮 1（定向检索）

- 执行者：fresh-context 查新代理；日期：本轮会话
- 输入：/DEEPDIVE/v2/cards/card-01-fi.md（任务书路径多写一层后缀 .md.md，实际文件为 card-01-fi.md，已按同一卡执行）
- 三系统：arXiv / Crossref / OpenAlex；锚点前向引用：Semantic Scholar

## 一、查询组记录（10 组，全卡 ≥8 达标）

命中数格式：arXiv / Crossref / OpenAlex（Crossref 的 total-results 为宽匹配词袋计数，仅作量级参考；判定看 Top 标题相关度）。

| 组 | 查询短语（技术词×场景词） | arXiv | Crossref | OpenAlex | Top3 标题（最有信息量系统） |
|---|---|---|---|---|---|
| G1 | topology dynamics decision latency mismatch LEO satellite routing | 0 (8 词全 AND 过严) | 2.53M | 131 | OpenAlex: 分布式卫星系统架构综述 / 分布式卫星信息网络 / DRL 协同下载 —— 均非失配相图 |
| G2 | stale routing information performance collapse satellite network | 0 (同上) | 6.54M | 322 | OpenAlex Top 混入无关（哲学书）；无陈旧信息×性能崩塌同轴工作 |
| G3 | non-monotonic performance control loop delay constellation routing | 0 (同上) | 7.18M | 420 | OpenAlex: contact graph routing 教程等；无非单调失效结构研究 |
| G4 | phase diagram failure modes networked control time delay | 10 (词: time delay networked stability) | 6.52M | 68836 | arXiv: 时滞神经网络稳定性 / 时滞耦合振子共识 —— 时滞控制论存在但均为固定时滞稳定性分析，无 LEO 场景、无 ρ 相图、无非单调反超带【相邻-理论侧】 |
| G5 | ephemeris prediction error satellite routing reinforcement learning | 10 (词: ephemeris prediction satellite) | 3.80M | 87 | Crossref: DRL 巨型星座鲁棒路由 / MARA-Shunts MARL 星间路由 —— 全部以星历预测有效为前提，无"预测-行为落差"协议【相邻-前提相反】 |
| G6 | routing recomputation interval tradeoff delay packet loss satellite | 0 (词: routing update interval satellite) | 1.01M | 20 | 无重算间隔×失效模式三角的系统扫掠 |
| G7 | synchronization ratio threshold distributed routing constellation consistency | 10 (词: consistency routing satellite) | 983K | 523 | arXiv: LEO 拓扑感知路由 / 卫星网络联邦学习路由 / RL 混合路由 —— 无同步率阈值×成功率崩塌结构 |
| G8 | OSPF convergence snapshot interval LEO constellation simulation | 0 (词: ospf satellite convergence) | 1.29M | 15 | OpenAlex: Starlink self-driving LEO 综述 / SATNET-OSPF —— 快照间隔仅作实现参数，未被当自变量扫掠出非单调拐点 |
| G9 | factorial attribution simulation reality gap network queue dynamics buffer management | 10 (词: simulator queue real network) | 230K | 7 | Crossref: sim-to-real gap 仅机器人领域（"A robot's guide to crossing the reality gap"）；网络侧无析因归因分解【相邻-概念借源】 |
| G10 | information age of observed state routing decision freshness | 10 (词: age information routing) | 6.64M | 78418 | arXiv: AoI 排队网络 / AoI 路由调度 —— AoI 理论成熟但对象是信息流年龄优化，非"决策系统性能 vs 观测状态年龄"的相图判别【相邻-AoI 理论】 |

注：G1–G3 arXiv 8 词全 AND 返回 0 为查询构型问题（过严），非零命中的反证由 G4–G10 的 3–4 词组补足；已在记录中如实标注。

## 二、锚点前向引用扫描（Semantic Scholar，limit=30）

| 锚点 | 返回引用数 | 可疑命中 |
|---|---|---|
| arXiv:2306.01346（学习型路由 <1 s） | 24 | 无 |
| arXiv:2402.17666（学习型路由 <1 s 之二） | 14 | 无 |
| arXiv:2310.09242（Starlink 15 s 全局重配置） | 30（触上限，实际更多） | 2 条标题级可疑，细看均不成立：① "Plan With the Sky"（LEO 边缘×机器人自主协同规划，匹配词为 mismatch 泛义）；② "QoE-Aware Parameter Tuning for ABR in LEO"（参数调优，非失配相图） |
| arXiv:2605.04448（queue-aware DDQN） | 0（S2 未收录） | 无 |
| arXiv:2605.27717（drop-front 队列反推） | 1 | 无 |
| ieee-11308874（OSPFv3 收敛 2.2 s） | 未扫 | **限制**：仅持 IEEE 文档号、无 DOI，无法构造 S2 查询；本轮如实记录为未覆盖 |
| ieee-11556312（R_sync^95 阈值 / TRACE） | 未扫 | 同上限制 |

**失败记录**：两篇 IEEE 锚点的前向引用扫描因缺 DOI 未能执行（非"扫过无命中"）；结论的证据等级据此降级。

## 三、查新结论

- **直接答复（同现象+同机制判别核心）：0 / 10 组查询、0 / 5 可扫锚点**。未发现任何工作在 LEO 星座场景构建"决策回路时延×拓扑动态"的失效模式相图、扫 R_sync/状态年龄阈值轴、或做预测-行为非同源落差的三因子析因分解。
- **相邻清单（6 项，均说明覆盖差异）**：
  1. 【相邻-理论侧】时滞控制论（G4，arXiv 10 篇）：时滞网络稳定性/共识分析工具成熟，可作 H2 的理论弹药，但固定时滞、无场景标定、无相图坐标系。→ 卡 §7 "池外时滞控制论待查"条目部分闭合：工具存在，但不直接给出本卡相图。
  2. 【相邻-前提相反】DRL/MARL LEO 路由（G5、G7）：大量工作**假设**星历预测有效（对应 H3 立场），恰好是本卡要检验的对象而非竞争答复。
  3. 【相邻-AoI 理论】Age of Information（G10）：AoI 优化文献丰富，但目标函数是年龄最小化，不是"年龄→性能失效模式"的判别曲线；可引用为观测状态年龄 instrumentation 的形式化支撑。
  4. 【相邻-单轴先例】Starlink 测量/OSPF 快照类（G8）：快照间隔与重配置均只作固定参数，未见自变量扫掠+非单调拐点报告。
  5. 【相邻-概念借源】sim-to-real reality gap（G9）：概念在机器人领域成熟，网络/星座场景无析因归因分解先例。
  6. 【相邻-阈值现象】无第二处同步率/信息质量崩塌阈值在 ρ 轴上的复现——崩塌带仍无正例锚点，卡"假设区"标注维持。
- **证据等级**：三系统宽检索（非穷尽）；锚点扫描 5/7 完成、2/7 因缺 DOI 未覆盖；跨 2026 预印本收录延迟风险存在（2605.04448/2605.27717 在 S2 零引用或未收录，其被引网络尚未形成）。**"池外无直接答复"判定为中等置信**；维持卡 §7 的"不主张全球首创、检索边界有限"表述不变。
