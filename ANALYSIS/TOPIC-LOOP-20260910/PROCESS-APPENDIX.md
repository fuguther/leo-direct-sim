# 过程附件（PROCESS-APPENDIX，run1 收口版）

> 单一事实源导航；不复制内容。前史（R2 返工/R3 历史审查）见 ROUND-LOG §10/§11 与 R3-DELIVERY.md。

## run1 流水线执行记录

| 阶段 | 执行 | 产物 |
|---|---|---|
| 三路生成（新上下文，白名单 v2） | A/B/C 后台子代理各 1 个 | round/run1/staging/path-A/B/C-*.md（4+4+4 卡+4 放弃线） |
| 主控初筛+入账 | ledger add ×12（12 独立身份，无键撞） | round/run1/cards.json；round/CANDIDATE-LEDGER.csv |
| 历史碰撞审查 ×2（全新上下文） | 批1（新鲜度四卡）/批2（八卡） | round/run1/op-history-batch1.md、batch2.md |
| 家族合并落账 | 新鲜度家族卡（三机制层）/寿命卡并入 B4/信用族合成 | 台账 v 序列 + merge 行（理由留痕） |
| 深化 ×2（有限反馈接力） | F1/B3 深化者 | round/run1/feedback-F1.md、feedback-B3.md、draft-F1-deepened.md、draft-B3-deepened.md |
| 三角色内容审查 | builder（F1+B3）/neighbor（F1+B3+L1）/evidence（F1+B3+L1） | round/run1/op-review-builder.md、neighbor.md、evidence.md |
| 主控整合+推荐 | B3 v3、L1 v6、F1 v3（条件保留）、backlog×4 | 台账；reviews.csv R6-R13（双哈希绑定，整合修订触发失效链） |

## 候选来源与演变（run1）

- **L1**（cc72be0cbef）：R2 path-B 卡3 → R2 三角色审查整合 v2 → R3 miniflow → v3 → run1 并入 B4（③*合并）→ 三角色审查（neighbor 收窄+evidence 补竞争证据）→ v6 推荐。
- **B3**（cc029fa6119）：run1 path-B 卡B3 原生 → T-C2 机制化切片（批2 ②）→ 深化 → 三角色审查 → v3 推荐。
- **F1**（cc24a3f94e5）：run1-A1/B1/C1/C4 四卡合并（批1 家族裁决）+c30b20940a3（R3 卡并入）→ 深化 → 三角色审查 → M1（TAP-DAR）→ v3 条件保留。
- **信用族**（c5a63c921dd）：run1-C2+B2 合并 → awaiting_evidence（PRIMAL 0% 前提为第一门）。
- **backlog**：run1-A2/A3/A4/C3。

## 审查处置摘要

- 采纳并落账：builder 11 条（F1-S1..S6/B3-S1..S5，含稳态/瞬态两腿拆分）、neighbor 8 条（Wang24b 第二门/LOZANO-continual 对照臂/L1 生存域收窄+GANNON/TEG）、evidence 23 条（M1 TAP-DAR/标签修正×2/夸强×1/竞争证据×2/Yan25b 禁承重）。
- 驳回：无；全部采纳（含"承但降级"类）。
- 失效链：整合修订触发 R6-R13 needs_review（意见已被采纳进修订——复核时以当前版本为准）。

## 关键证据位置

- 原文逐字核对：LOZANO PDF（28 字段句/eq.13/低载分位）、CHOU PDF 行270-281（eq.3）、HE 表I、LIAQ 摘要+§V 原文句、WEIL 表2/4、leo_sim 代码（CacheEntry/control.py:14、learning.py DDQN、info_ladder_tiny field_age、profiles/e0_load_scan.yaml）。
- 库外确认（非全文）：TAP-DAR（Undermind+Crossref，DOI 10.1109/TCCN.2026.3720213）、Wang24b（DOI 10.1109/GLOBECOM52923.2024.10901221）。

## 工具验收状态（收口）

- 回归 11/11 PASS（test_rework_regressions.py）；deps_check 21/21；governance 仅余主库既有 2 项 STALE_CURRENT。
- PR #199：READY + auto-merge 挂起（等 GitHub 侧 approval；run1 提交推上后同 PR 承载）。
