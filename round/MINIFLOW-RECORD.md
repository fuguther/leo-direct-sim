# 单卡完整小流程记录（MINIFLOW-RECORD，2026-09-10）

> 目的：返工包第四组第二步——用一张现有冻结卡验证「入账→建设→近邻→证据→主控→修订后状态」全链。
> 卡：path-B 卡3（星历可预报的链路剩余寿命不在观测向量）。**本轮=流程验证，不含价值裁决。**

| 步骤 | 实际执行 | 所审/产物版本 | 结果与证据 |
|---|---|---|---|
| 1 入账 | ledger.py add（v1） | cand_id=cc72be0cbef，content_hash=haa9dadab679e | 台账行1；`round/CANDIDATE-LEDGER.csv` |
| 1b 旧题匹配 | add --old 旧台账（12卡） | — | **未触发**：合并键为词汇级归一化，跨 run 措辞不同不键撞（与旧 TTNE 卡的语义同族由主控人工认定）；键撞报告路径已用合成同键旧卡离线演示：OLD_TOPIC_MATCH 报告且照常入账（不淘汰） |
| 2 建设者 | 前台 subagent，意见 7 条 B1-B7+机械检查 MC1-MC6 | v1 文件 sha256=28acb6…e2bc（三角色各自实算一致） | `round/miniflow/op-builder.md` |
| 3 近邻替代 | 前台 subagent；通道实测 degraded/incomplete 原样记录；Undermind×2（20 命中） | v1 同上 | `round/miniflow/op-neighbor.md`；覆盖判定=条件/机制级比对（四篇均不覆盖；N3 Yan25b 同信号异层、N4 Ort25 表级利用、N1 SHORT 可预报性条件质疑） |
| 4 证据审查 | 前台 subagent；本地 PDF 逐字抽查（PyMuPDF），18 项意见 | v1 同上 | `round/miniflow/op-evidence.md`；结论=可信（未发现 BLOCK），修订项均属"证据不足" |
| 5 主控整合 | B1-B7/N1,N3,N4,A1,A3/E8-E15 全部采纳，无驳回；写 v2 整合卡 | `round/miniflow/card-B3-v2.md`（sha256:7287dd…） | 修订理由见台账 note |
| 6 审查失效 | ledger.py revise（v2，承重变化=6 字段） | R1-R3 自动置 needs_review（审的是 v1 hash） | 台账 stdout：REVIEWS_INVALIDATED ['R1','R2','R3'] |
| 7 修订后状态 | ledger.py status → awaiting_evidence（v3） | 当前版本=v3（只追加，v1/v2 保留） | 台账 3 行 + reviews.csv 3 行 |

## 过程中发现并当场修复

- status 子命令缺 --writer 参数（回归未覆盖该命令）→ 修复并把 status_change 纳入 T3 回归；回归曾因此 9/10，补齐后 10/10。
- round 台账曾残留旧 15 列 schema 头 → ledger.py 增加 LEDGER_SCHEMA_MISMATCH 拒写校验；台账以新 schema 重建（重建动作记录于此，无历史数据丢失——旧头文件仅含表头）。

## 语义边界（如实记录）

- 语义同族检测仍是主控职责（Dice 回退+词汇级合并键）；本轮无 sentence-transformers，未新增该能力（按收口标准明确不做）。
- novelty 通道 S2 429 → incomplete：失败未产生任何新颖性表述；近邻线索单独依赖 Undermind（已记录额度与命中）。
- 三份意见按同模型互补分工处理（异模型通道故障未恢复）。
