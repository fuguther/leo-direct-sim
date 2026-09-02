# Traffic-Aware Domain Partitioning and Load-Balanced Inter-Domain Routing for LEO (ZHOU-2026-DTAR)

> 来源: https://arxiv.org/abs/2604.12382（2026-04 preprint）

它把 LEO 域间路由拆成两段：NSGA-II 离线按流量划分域，GAT 动态编码链路流量强度/负载/故障状态，交给 action-masked PPO 在线决策。声称在 288 星 Walker 星座上显著降低负载不均衡与端到端时延，提升路由成功率、降低丢包，且覆盖正常/流量激增/故障三种场景。证据是仿真，但摘要未交代流量模型、MCS/链路速率假设以及域划分目标函数权重的设定。最关键的不适感：域级抽象把决策粒度抬到"域"而非"星间逐跳"，与我们 280×14 逐包逐跳的仿真直接错位。它对"信息年龄"仍无意识，但"把链路负载/故障状态动态编码进 GNN"其实就是我们要量化的"路由信息新鲜度"的粗糙版。可作参照系，也提示：就算状态又全又新，域级粒度也撑不起对拥塞的响应——和我们 ISL 利用率 <3% 的发现同构。2026 新 preprint，与既有工作的对照强度未核实。

**评级**：A

> 状态: 摘要；未核实字段: 流量/速率模型、域划分权重设定、与既有基线对照的统计细节、是否开源。


## 全文深读（2026-09-03 补，ar5iv/arxiv HTML 全文）

**方法骨架**：两段式——离线 NSGA-II 域划分（III-A，目标1=域内流量比 IDTR 最大化 Eq.4，目标2=域间负载标准差 σL 最小化 Eq.5）+ 在线 GAT 域状态编码（III-B：域节点 6 维特征=域内星数/流量负载/跨域链路数/故障节点比/负载指数/surge 热点；域边 3 维=可用链路比/负载/故障标志；2 层 GAT，hidden 64，4 头，输出 32）+ action-masked PPO 域间逐跳路由（III-C：reward Eq.8=δ·方向塑形(d−d′)−β 每跳罚+到达奖 rs−β·h−失败罚 r_f；mask=故障邻居+超 H_max 剩余跳预算邻居；PPO，lr 3e-4，2.5e6 步，batch 256，熵 0.03，~1.5e6 步收敛 IV-D）。
**实验合同**（IV-A Table I）：288 星=12 平面×24 星，1450 km，89°，K=18 域；144 步/回合、3 flows/步（flow 级，非包级）；H_max=9；域间链路故障 p_f=p_r=0.02；surge μ=5× 局部热点（II-B）；流量=日模式时空不均矩阵，无 Mbps/Gbps 量级；基线 Dijkstra/ELB/QRLSN/CDPAR 同训 2.5e6 步，评估 100 episodes 取均值；指标 CV/端到端时延/丢包率/路由成功率。结果（IV-B）多为图3定性：fault 下成功率较 Dijkstra +9.25pp、较 CDPAR +8.89pp，ELB/QRLSN <80%；消融（IV-C）：去 GAT 或去 NSGA-II 均劣化。
**与我们对账**：① F0/F1——他们把"实时链路负载/故障"编进 GNN 状态（≈我们的 F1 物理信息阶梯），但 normal/surge 场景只报 CV/延迟改善、**无交付率量化提升**，fault 场景才有 pp 级收益；与 VM 实测"信息多了路径变了、交付率零差异"结构同构：低负载下拥塞感知无从发力。② ISL 利用率<3%——flow 级 3 流/步 + 18 域，域间链路远未饱和，CV 优化就是低利用率下的摆布，同构。③ holding/access 瓶颈完全缺席：无地面段/接入链路/排队；"端到端时延"口径未明（IV-A 截断处）。
**可复用**：action masking（连通性+跳预算）可直接移植我们 DDQN/GAT 臂；GAT 节点/边特征模板与 δ 方向塑形奖励；离线划分+在线路由两时间尺度解耦；开源 https://github.com/ChenZ-code/DTAR_Routing。**危险**：CV/延迟无精确数字（图为主），delay 口径、MCS/链路容量假设未交代，p_f=p_r 独立随机故障不合真实相关性，域级粒度与逐包逐跳仿真错位。
> 深读状态: 全文已读[arxiv.org/html/2604.12382]；未核实: CV/延迟精确数值、delay 口径、MCS/链路容量、fault 场景 ELB/QRLSN <80% 具体值、域划分 NSGA-II 权重设置。

