# 阶段 2 碰撞执行计划（草案 v0——未执行，等批准）

> 本文件只定义规程与查询模板；**未发起任何检索**。

## 规程（合并规范 02-MERGE-RUBRIC.md 的延伸）
- 每族：≥2 检索系统 × ≥3 组查询短语；查询日志落盘 PHASE2-LOGS/<family>-<system>.jsonl（时间戳/系统/短语/命中标题+摘要截断/相关性标注）。
- 主动求反：每族 1-2 组"该现象可能已被解决"方向的最强检索（如族1 搜"latency spike attribution LEO measurement"，族2 搜"orbital periodicity capacity planning satellite"等）。
- 碰撞后：审计式演化——每族状态 出生→碰撞→{淘汰/合并/存活}+证据；淘汰+合并 ≥ 族数一半（≥5 族）才算完成；未达标的族不进入阶段 3。
- 旧材料零接触：碰撞检索只面向外部学术/公开源；阶段 1 产出文件仍是唯一候选依据。

## 检索系统与可用性（2026-09-03 实测）
- arXiv API：可用（export.arxiv.org，无需 key）。
- OpenAlex：HTTP 429 限流（需退避重试或分批）。
- Semantic Scholar：HTTP 429（需退避；或改用其公开镜像/延迟轮询）。
- web_search 工具：后端 API key 失效（需修复或改用 anysearch/agent-reach 技能兜底）。

## 每族查询短语模板（源自候选出生记录原文，未跨素材）
- 族1（尖峰归因）："LEO satellite latency spike"; "Starlink latency spike cause handover rerouting"; "satellite network latency anomaly attribution measurement"
- 族2（拍频/供需错配）："LEO constellation capacity demand mismatch periodic"; "satellite network orbital period traffic rhythm"; "mega constellation supply demand temporal imbalance"
- 族3（快拓扑慢控制）："LEO constellation control plane latency topology change"; "satellite routing convergence time dynamic topology"; "space network control loop delay fast topology"
- 族4（可预测性落差）："LEO topology predictability routing behavior"; "satellite constellation deterministic topology routing deviation"
- 族5（按需建链边界）："on-demand laser ISL establish routing LEO"; "laser inter-satellite link scheduling fixed grid tradeoff"; "satellite link resource scarcity temporal hotspots"
- 族6（架构口径）："Starlink OneWeb architecture performance comparison measurement"; "LEO operator architecture difference latency measurement methodology"
- 族7（中断代价放大）："satellite handover impact duration amplification"; "LEO handover transport performance degradation window"
- 族8（均衡击穿边界）："LEO load balancing hotspot failure"; "satellite network congestion spatial distribution population"
- 族9（静态近似误差）："time-expanded graph approximation error dynamic network"; "snapshot static approximation time-varying network routing error"

## 碰撞结果记录格式
每族：命中表（系统x短语x前5条）→ 直接答复？（是/否/部分，附证据）→ 状态初判（存活/需合并/疑似死亡）→ 证据链。