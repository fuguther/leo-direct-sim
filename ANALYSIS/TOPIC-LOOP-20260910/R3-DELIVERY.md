# R3 交付：历史碰撞审查 + 剩余修复（集中转审包，2026-09-10）

> 分支 `agent/20260910-topic-loop`（本轮新增提交见 §6）；PR #199 自动更新。选题推荐仍冻结。

## 1. 历史选题索引

- 位置：`round/history/HISTORY-INDEX.md`（v1.1）。指针式：每题五元组/当时处置/未通过原因+出处/原因货币性/重开条件；原始材料零改动。
- 覆盖：4 谱系 38 题——A 开题一页纸线 1 题（冻结推荐后被删=锚定流程违规，非证伪）；B 三透镜阶段线 14→9 族→演化淘汰族1/6/7、合并→3 族→2.5 压测→A5 四卡；C 冷启动备忘录 4 题（未裁决）；D run-test 12 卡（open）。
- **缺失材料（如实）**：literature-index.csv（旧44条）、RECONCILED-LIBRARY.csv、archived-topic-stages-20260910、历史 run hypotheses/drafts、旧仓库路径（已不存在）——相关主题历史审查按第五类弃权。
- **判定质量分类已落实**：机制反例否定/已有方法覆盖/证据不足暂缓/工程条件未满足/用户范围不符/未裁决 分开标注（如族1/族6=已有方法覆盖；ONE-PAGE 删除=用户范围/流程；F-II/F-III=增量不足+证据条件未满足；COLDSTART=证据不足暂缓且检索记录过时）；登记的两条复活条件（族6 机制判别、族1-H2 静态场景）至今无人执行。
- **v1.1 修订**：历史审查子代理发现并上报 v1 对 A5 四卡处置记录有误（误记"未裁决"），主控亲证 taste-gate.md 后修订（F-I 收窄存活/F-II、F-III 死亡打捞附复活条件/N1 通过附三交割条件）——索引修订机制实测有效。

## 2. 历史碰撞审查接入与执行证据

- 接入点：独立生成→初筛→**历史碰撞审查**→近邻核查与深化→内容审查→推荐（EFFECTIVE-RULES-R2 §8；模板 round/tools/HISTORY-REVIEW-PROMPT.md）。
- 执行证据：判别样例电池 S1-S5 全判对（④②③③⑤，主控逐项对照索引+原件核实；盲化不完美已如实登记——样例文件含预期行，审查者自查声明并以五元组为据）；真卡 card-A1 审查=③（T-C1 最强匹配/D卡10/T-C3/F-I 同族②/缺失维度⑤），主控处置=继续+四项前置义务（round/miniflow-r3/MASTER-DISPOSITION.md）；意见经 review-register 绑定 content_hash（R5-A1-history）。
- 有限反馈与接力：feedback-cardA1.md（仅 5 条卡相关义务）→ 深化者产出 card-A1-revised-draft.md（对账登记/基线升格/检索义务前置/竞争解释 6 项）；隔离验证：深化者输入无历史库，其草案自证出处=反馈文件。生成端不回流失败理由已入规则 §8（下一批生成全新上下文）。

## 3. 四项修复

| 修复 | 复现 | 修改 | 测试 |
|---|---|---|---|
| 审查失效判断 | _norm_lb 剔全部符号→τ<15s≡τ≤15s 不触发 | 仅折叠空白；符号改变=承重变化 | T8 扩展 PASS（符号触发/纯空白不触发） |
| 身份与相似度分离 | 同键不同内容被自动并为同题新版本 | cand_id=首见内容派生；similar_to 线索；显式 merge 子命令（reason 留痕） | T2 重写 PASS（两身份+线索+显式合并） |
| CSV 恢复保护 | 物理行截断会毁多行字段合法记录 | 停用破坏性修复；--backup/--repair-out（原件永不动，采纳由人） | T10 重写 PASS（多行字段+损坏尾：原件字节不变） |
| 解析失败误记无命中 | _normalize_paper 返回 None 未计数→全败=ok_empty | None 计入 skipped；全败=exec_error→incomplete | T12 PASS（monkeypatch 真路径） |
- 全量回归 **11/11 PASS**（round/tools/test_rework_regressions.py）+ deps_check 21/21。

## 4. 小流程通过/失败/未验证

- 通过：五类判别 5/5；card-A1 全链（初筛→历史审查→处置→有限反馈→深化接力）；意见版本绑定；隔离验证。
- 失败（过程中修复）：T2/T8/T10/T12 首轮各自暴露实现或断言缺陷，均修复后转 PASS（细节 ROUND-LOG §11.3）。
- 未验证：S2 检索实际重跑（429；义务已登记）；age-conditioned 先例存在性（下一步检索义务）；语义级跨 run 键匹配（=历史审查者职责，已由其验证工作）。

## 5. 分支 / 提交 / 写入范围

- 分支 agent/20260910-topic-loop；本轮新增提交见 git log（R3 索引/修复/验收分主题提交）；写入范围=round/**（history/rules/tools/miniflow-r3/ledger/reviews/ROUND-LOG）+ ANALYSIS/TOPIC-LOOP-20260910/（本文档）；research-ops 与其他 worktree 只读未改。

## 6. 是否还有阻止正式选题运行的实质问题

**无实质阻塞。** 恢复选题的条件=用户解冻+按 EFFECTIVE-RULES-R2 §8 流水线执行（历史碰撞审查已接入并有实跑证据）。非阻塞遗留：①S2 公共档 429（通道替代已验证）；②embedding 语义同族检测缺位（Dice+历史审查者人工兜底）；③缺失历史材料 5 项（已弃权规则覆盖）；④COLDSTART 零命中记录过时（card-A1 义务已示范重跑流程）。
