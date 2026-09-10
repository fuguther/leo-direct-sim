# 过程附件索引（PROCESS-APPENDIX，R2）

> 单一事实源是以下文件；本页只做导航，不复制内容。

| 内容 | 文件 |
|---|---|
| 主控台账（开工体检/暴露声明/组件核验/派发台账/合并协议/冻结与返工全程） | round/ROUND-LOG.md |
| 复现记录（四组发现+台账CLI，含原始输出） | round/logs/repro-group2.txt、repro-ledger-cli.txt |
| 离线回归（10 项） | round/tools/test_rework_regressions.py（运行输出见 ROUND-LOG） |
| 依赖指纹与漂移 | round/deps/DEPENDENCIES.md；round/tools/deps_check.py；round/tools/gen_manifest.py |
| 实际派发记录与提示词 | round/dispatch/DISPATCH-RECORD.md、D123-prompts.md |
| 有效入口规则（唯一权威） | round/rules/EFFECTIVE-RULES-R2.md |
| 中性知识视图（切片溯源） | round/knowledge/NEUTRAL-KNOWLEDGE-VIEW.md；round/tools/gen_neutral_view.py |
| 三路原始产出（试运行材料标签） | round/staging/path-{A,B,C}-*.md |
| 单卡小流程 | round/MINIFLOW-RECORD.md；round/miniflow/{card-B3.md,card-B3-v2.md,op-*.md,b3.json} |
| 审查登记 | round/reviews/reviews.csv |
| 候选台账（当前） | round/CANDIDATE-LEDGER.csv（v1 add→v2 revise→v3 status） |
| 架构审查材料 / 转审包 | ARCHITECTURE-REVIEW.md；REVIEW-REQUEST-FOR-CODEX.md（本目录） |

## 候选演变摘要（至 R2 冻结点）

- B3 卡（cc72be0cbef）：v1 入账 → 三角色审查（v1 指纹绑定）→ 主控整合 20 条意见全采纳 → v2 承重修订（6 字段）→ R1-R3 自动 needs_review → v3 状态 awaiting_evidence。旧候选对账：语义同族（旧 run-test TTNE 卡）由主控认定待恢复后处理；词汇键撞不触发（如实记录）。
- 其余 11 张卡：保留原始产出，未入账未裁决（等解冻后按 EFFECTIVE-RULES-R2 §4 处理）。
