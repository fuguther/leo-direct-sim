# 交接包：run2 选题循环（供 4.1 新会话接手，v2.0 2026-09-10）

> **本文是新会话的唯一起点**。读它即可接续，无需读上一会话。
> 生成者：GLM-5.3 会话（已完成准备工作）；接手者：`deepseek/deepseek-v4.1-flash` 新会话。

---

## 0. 一句话现状

**语料已就绪（111 篇全文索引 + MinerU 逐篇转 MD 进行中）、方法论文档已就绪、9 张候选卡已生成并审计清白、历史碰撞审查进行中。**
接手后：**继续跑选题循环**，直到 **≥2 条合格主线走完全流程**。

---

## 1. 工作目录与硬约束

- **worktree**：`/Users/lge/Desktop/leo-direct-sim/.worktrees/topic-loop-20260910`
  **所有相对路径以此为基准，不是主库**；bash 用 `workdir` 参数指定它。
- **分支**：`agent/20260910-topic-loop`，最近提交 `fc2e266`（已 push；git 可用，注意本机 `/usr/bin/git` 曾因 Xcode 许可门禁失败，现正常）
- **模型路线**：`commandcode-goat-autosync/deepseek/deepseek-v4.1-flash`（**新会话默认即 4.1**；旧会话的允许清单是冻结的，故本包交接）
- **禁止**：Pro 路线 / 训练 / 仿真 / 改 `CODE/` 与授权链 / 删除移动已跟踪路径

---

## 2. 研究范围（用户锁定，不可偏离）

**低轨卫星网络中，负载变化下强化学习路由如何保持良好的到达率与端到端时延。**

配套展开（用户原话要点）：
- 在 LEO 路由方向**围绕时延、负载、到达率等性能**推进；
- **始终围绕三问**：
  1. 现有方法在**某个重要条件下为什么做不好**？
  2. 这个改动**针对了什么原因**？
  3. 为什么**已有简单方法或成熟 RL 方法不能同样解决**？
- **不局限于已有的 9 张卡**——可在小领域内自由选题；
- **并行最多 3 个主题**；
- **直到至少 2 个很好的选题跑完整个流程**，各材料准备齐全。

---

## 3. 用户已确认的执行参数（2026-09-10 对齐）

| 项 | 决定 |
|---|---|
| 深化范围 | **只深化通过筛选的卡**（未被刷掉的）；被淘汰的卡**必须保存理由** |
| 并行度 | **最多 3 个主题**并行 |
| 选题来源 | 不限于 9 张卡，可继续生成 |
| vlm 高质量转换 | **不跑**，全用 `pipeline_txt` |
| 交付形态 | **1 条主线 + 至多 1 条独立备选**（备选需同等强度，不凑数） |
| 停止点 | 停在**"待 Codex 内容审核"** |
| 终止条件 | 循环直到 **≥2 条合格主线跑完全流程**（或触发如实报告的停止条件） |

---

## 4. 语料（白名单 v4，全部已验证可用）

| 通道 | 规模 | 怎么用 |
|---|---|---|
| **`round/zotero/ZOTERO-INDEX.md`** | **111 篇，全部有 PDF** | 总入口，每篇附 itemKey |
| `round/zotero/KEY-PAPERS-CITEKEYS.md` | 15 篇关键论文 | cite_key ↔ itemKey 对照 |
| `round/zotero/CITEKEY-CROSSWALK.md` | 29 篇工作区论文 | **分级**：只信 confident 档（≥0.75） |
| **MinerU MD（VM）** | 转换中（10/111） | `ssh vm 'ls /data/liguang13/topic-loop-r2/md'`；每篇 `md/<key>/<key>/txt/<key>.md` |
| `zotero_fulltext` | 111 篇 | 秒级粗筛（表格结构会丢；**承重证据用 MinerU MD**） |
| `round/knowledge/notes-neutral/*.md` | 41 篇 | 事实笔记（倾向已剥离；只当线索） |
| Undermind | 工作区 `eef99118-f623-4a47-a34a-05c6617b7ecb` | 见 §7 |

**重要事实**：Zotero 111 篇中 **94 篇从未进入旧题录**（此前只用 17 篇）——这才是本次的最大语料升级。

---

## 5. 已完成的准备工作（接手前状态）

| 产物 | 位置 | 作用 |
|---|---|---|
| 方法论总纲 | `round/rules/TOPIC-SELECTION-METHOD.md` | **单一入口**：合格定义、十步流水线、四条原则、文件索引、反面清单 |
| 质量闸门 | `round/rules/QUALITY-GATE-R2.md` | G1–G5 判据、致命项一票否决、≤3 轮迭代 |
| 失败升级协议 | `round/rules/EXPLORATION-FALLBACK.md` | 全灭时怎么办（三级阶梯 + 停止条件） |
| Undermind 手册 | `round/rules/UNDERMIND-PLAYBOOK.md` | 四种检索模式、踩坑、工作区防火墙 |
| MinerU SOP | `round/rules/MINERU-CONVERSION-SOP.md` | 实测四后端对比、质量瑕疵与规避 |
| 提示词模板库 | `round/rules/PROMPT-TEMPLATES.md` | 五类子代理提示词（直接填空用） |
| 流程图 | `ANALYSIS/TOPIC-LOOP-20260910/run2/PIPELINE-MAP.md` | 含隔离矩阵与三道防线 |
| 淘汰台账 | `round/history/ELIMINATED-REGISTER.md` | A/B/C 三类分离 + 复活条件登记 |
| 历史索引 | `round/history/HISTORY-INDEX.md` | 38 题全量 + §5 失败原因货币性 |
| 闸门/反馈模板 | `round/run2/gates/GATE-TEMPLATE.md`、`round/run2/feedback/FEEDBACK-TEMPLATE.md` | 逐条判定与 must-address |
| 工具 | `round/tools/ledger.py`、`patched_novelty.py`、`patched_checks.py`、`patched_audit.py`、`audit_contamination4.py`、`test_rework_regressions.py`（13 项回归） | 台账/查新/检查/审计 |

---

## 6. 当前在途工作（接手时先收口）

### 6.1 9 张候选卡（已入账，等历史审查）
`round/run2/cards.json` + `round/run2/staging/path-{A,B,C}-*.md`

| 卡 | cand_id | 一句话 |
|---|---|---|
| A1 | `c77e62eb00f` | 负载合同审计 + 冻结策略强度扫描 + 强度条件化输入 |
| A2 | `c806e1db789` | 强度三通道分解 → 相对化状态 + 溢出约束更新 |
| A3 | `c37b7753f31` | 塌陷发生在决策器：推理排队瓶颈与前兆 |
| B1 | `c9bbc1f6604` | 热点可辨识性：拥塞场相位注入观测 |
| B2 | `cc0e429067b` | 热点迁移下决策面拥塞：推理丢包作独立通道 |
| B3 | `c3d376febf7` | 守恒 OD 漂移算子：分离三假说的评估协议 |
| C1 | `cdc387b303e` | 突发时长 × 反应时间常数错配 → 瞬态窗塌陷 |
| C2 | `c24abb72218` | 负载过程是训练与评估的共享盲区：同均值突发扫描 |
| C3 | `c6f6c2b12ad` | 突发下瞬时快照的信息可辨识性 |

**三路共同发现**：库内**无一篇** LEO 逐跳 RL 路由工作报告训练-评估在强度/OD分布/突发结构三轴上的分离实验。

### 6.2 历史碰撞审查（进行中）
子代理 `0c226ffe-947a-4845-a286-a0d1ea7d3aad` 输出 `round/run2/op-history-review.md`。
**接手时先看它是否已完成**；未完成则重派（提示词见 `PROMPT-TEMPLATES.md` §3）。

### 6.3 MinerU 逐篇转换（VM 后台）
`ssh vm 'tail -5 /data/liguang13/topic-loop-r2/one_txt.log'`（约 50 秒/篇，剩余约 85 分钟）。
监听作业 `bash-5`（旧会话）；新会话可直接轮询日志。

---

## 7. Undermind 速用（要点）

- **workspace_id**：`eef99118-f623-4a47-a34a-05c6617b7ecb`（**几乎每个工具都要**）
- **四种检索模式**（此前只用过 global）：
  - `global` 全语料语义检索；`library` 只查工作区库；
  - **`citing`** 找引用种子论文的工作 → **追直接对手**；
  - **`referenced`** 找种子引用的工作 → **追谱系**。
- **纪律**：窄/空结果 ≠ 文献不存在（原文明确）→ 只能写"本次检索范围内未命中"。
- **防火墙**：生成器持有 Undermind 工具 → **工作区内容对生成器可见** → 工作区**只写论文事实**，禁写候选/淘汰理由。
- 已建证据图谱：`/lit-axes/load-variation-axes.md`（三轴事实表）。
- 参数坑：`lookup_papers_by_metadata` 用 `paper_metadata`（字符串列表）。

---

## 8. 接手后的执行顺序（建议）

```
① 收口在途：等/重派历史碰撞审查 → 得 9 卡五类裁决 + must-address
② 初筛：按裁决筛出可深化卡（排除 ④ 类撞车；⑥ 保证现象有原文锚点）
   → 未通过的卡**记录理由**入 ELIMINATED-REGISTER §6（不得丢弃）
③ 死因回传：为每张可深化卡写 round/run2/feedback/<卡ID>.md（仅本卡相关内容）
④ 深化（≤3 并行）：三问 + 承重引文回原文（优先 MinerU MD）
⑤ 三角色审查：builder / neighbor / evidence（各新上下文）
⑥ G1–G5 闸门：逐卡判定；致命项一票否决；≤3 轮
⑦ 若合格卡 <2 → 触发 EXPLORATION-FALLBACK：归因 → 轴扩展或提问类型转换 → 继续生成（≥3 并行上限）
   **直到 ≥2 条合格主线走完全流程**
⑧ 交付：主报告 / 完整文稿 / 机制图 / 文献指引 / 取舍记录
⑨ 台账追加 + git 提交推送 + 停在"待 Codex 审核"
```

---

## 9. 纪律红线（违反即作废重跑）

1. 生成器**不读**历史候选/淘汰理由/其他生成器卡面；**列目录也算违规**；
2. 深化者**不拿**历史全集，只拿本卡 must-address；
3. 初筛后必跑 `audit_contamination4.py`；
4. 快照绑定：审查须绑 `ledger_content_hash` + `candidate_file_sha256`（空/畸形一律拒绝）；
5. "论文没测" ≠ "论文做不好"（没测标【待证】）；
6. 不靠改名/加条件/补风险声明维持推荐；
7. 无合格产出时如实报告，不把"流程完成"当"选题成功"。

---

## 10. 环境故障备忘

| 故障 | 现状 |
|---|---|
| git（Xcode 许可门禁） | 已恢复（`git version 2.50.1`） |
| 子代理路线 | 新会话默认 4.1；旧会话白名单冻结（GLM 可用，Qwen/Muse 配额耗尽） |
| VM rsync 缺失 | 用 `tar cf - … \| ssh vm 'tar xf -'`；macOS 会带 `._*` 文件，传后清理 |
| MinerU hybrid 后端 | 历史失败（torch/驱动错配）→ **用 `pipeline`** |
| VM 根分区仅 2.7 GB | 输出走 `/data`；设 `TMPDIR=/data/liguang13/tmp` |
