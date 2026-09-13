# 全框架结构图与体检报告（FRAMEWORK-MAP v1.0，2026-09-11）

> 用户要求：**检查所有部分、列出流程图、除完善外还要修剪、修改不合理处**。
> 本文件 = ① 九个子系统的流程图 ② 实测矛盾清单 ③ 修剪方案（删除需批准）。
> 生成方式：全量盘点 `round/rules`（10 份 / 1066 行）、`round/tools`（45 个文件）、目录结构与交叉引用。

---

## 子系统 ①：规则体系（10 份 → 目标 6 份）

~~~~
flowchart LR
    M["TOPIC-SELECTION-METHOD.md<br/>总纲·单一入口"] --> R["EFFECTIVE-RULES-R2.md<br/>强制规则(白名单/流水线/隔离)"]
    M --> G["QUALITY-GATE-R3.md<br/>G1-G5 闸门"]
    M --> L["QUALITY-GATE-R3.md（第二部分：循环控制）<br/>循环与终止"]
    M --> F["EXPLORATION-FALLBACK.md<br/>全灭后怎么办"]
    R --> P["PROMPT-TEMPLATES.md<br/>五类派发模板"]
    P --> RP["⚠ tools/REVIEW-ROLE-PROMPTS.md<br/>旧版·内容重复"]
    P --> HP["⚠ tools/HISTORY-REVIEW-PROMPT.md<br/>旧版·内容重复"]
    M --> U["UNDERMIND-PLAYBOOK.md<br/>检索通道"]
    M --> S["MINERU-CONVERSION-SOP.md<br/>全文转换"]
    M --> RO["ROUTE-POLICY.md<br/>模型路线"]
    M --> C["CHAIN-AUDIT.md<br/>断点审计(一次性报告)"]
~~~~

**问题**：10 份规则存在**职责重叠**与**版本残留**：
- `CHAIN-AUDIT.md` 是一次性审计报告，却放在 `rules/`（应与 `ANALYSIS/.../FRAMEWORK-SELFCHECK.md` 同处）；
- `tools/REVIEW-ROLE-PROMPTS.md` + `tools/HISTORY-REVIEW-PROMPT.md`（共 49 行）已被 `rules/PROMPT-TEMPLATES.md` 取代，属**重复内容**；
- 尚无一份"**文件索引 + 版本状态**"表，导致旧版被误用。

---

## 子系统 ②：语料管道

~~~~
flowchart TD
    Z["Zotero 本机库<br/>111 篇 / 434MB PDF"] --> IDX["ZOTERO-INDEX.md<br/>111 篇 + itemKey"]
    Z --> MAN["pdf-manifest.json<br/>itemKey → 本地 PDF 路径"]
    MAN --> ST["stage_zotero_pdfs.py<br/>复制为 itemKey.pdf"]
    ST --> UP["tar over ssh<br/>(VM 无 rsync)"]
    UP --> VM["VM: /data/liguang13/topic-loop-r2/pdfs"]
    VM --> ONE["vm_mineru_one.py<br/>逐篇串行 pipeline_txt"]
    ONE --> MD["md/&lt;key&gt;/&lt;key&gt;/txt/&lt;key&gt;.md"]
    MD --> VAL{"质量校验"}
    VAL -->|表格/公式/数字| OK["可作承重证据"]
    VAL -->|5% 公式数字空格| FIX["回原 PDF 核"]
    Z --> FT["zotero_fulltext<br/>秒级粗筛"]
    FT --> COARSE["粗筛/定位"]
    OK --> GEN["生成器 / 深化者"]

    UM["Undermind 工作区<br/>111 与库外论文"] --> CK["CITEKEY-CROSSWALK.md<br/>分级防误配"]
    CK --> GEN
~~~~

**问题**：
- `vm_mineru_batch.py` / `batch2` / `batch3` / `vm_convert_pdfs.py` / `vm_extract_evidence.py` / `vm_mineru_quality_test.py` **全部被 `vm_mineru_one.py` 取代**（迭代残留 6 个文件）；
- 4 个 watch 脚本中 3 个已失效。

---

## 子系统 ③：主流水线（当前实际形态）

~~~~
flowchart TD
    A["① 生成 ×3 隔离"] --> B["② 初筛"]
    B --> B2["②b 污染审计<br/>audit_contamination"]
    B2 -->|违规| VOID["作废重跑"]
    B2 -->|干净| IB["批内对账 §8.0<br/>(R5 新增)"]
    IB --> H["③ 历史碰撞审查"]
    H --> NARROW["收窄(主控)"]
    NARROW --> FB["死因反馈 must-address"]
    FB --> D["④ 深化 ×≤3"]
    D --> NE["近邻核查"]
    NE --> RV["⑤ 三角色审查"]
    RV --> GT["⑥ 闸门 G1-G5"]
    GT -->|过| REC["推荐"]
    GT -->|修订| CNT{"轮次<3?"}
    CNT -->|是| D
    CNT -->|否| KILL["淘汰+登记"]
    REC --> DEL["交付五件套"]
    KILL --> DEL
~~~~

**问题**：**§8.0 批内对账的位置在时间线上自相矛盾**——
- 规则 §8.0 写"主控在**初筛之后、历史审查之前**执行"；
- 但实际我在**历史审查完成之后**才做（因为审查者指出该缺口）；
- 且 §8.0 说"历史审查者只审历史，不承担批内对账"——那它就**不应该**发现 A3↔B2 近重复，而它实际发现了。
→ **需修正**：批内对账归主控（保持），但历史审查者在发现**顺带**的批内重复时应"指认不处置"（本次做法正确，写进规则即可）。
---

## 子系统 ④：证据与审查闭环

~~~~
flowchart LR
    CARD["候选卡"] --> HREV["历史审查(独立)"]
    HREV --> V{"五类裁决"}
    V -->|① 无重合| OK1["进入深化"]
    V -->|② 同族差异| OK2["进入深化+差异义务"]
    V -->|③ 重复但可改判| OK3["对账后决定"]
    V -->|④ 旧理由仍适用| K1["停止+登记"]
    V -->|⑤ 依据不足| AB["弃权(不冒充否定)"]
    OK2 --> FB2["must-address 回传"]
    OK3 --> FB2
    FB2 --> DEEP["深化者(仅本卡反馈)"]
    DEEP --> ANCH["锚件全文核验 §8.0.1"]
    ANCH -->|截断/混淆| ERR["勘误表"]
~~~~

**问题**：
- **must-address 回传尚无执行记录**（规则有，未跑过）；
- **锚件核验归谁**未写明：本次是主控做的，但规则只说"主控须逐卡列锚件核验状态"，没说**谁来核**；
→ **需修**：明确"主控执行核验，深化者不得自证"。

---

## 子系统 ⑤：质量闸门与迭代

~~~~
flowchart TD
    IN["深化稿"] --> GC["gate_check.py<br/>机械判定 G0-G5"]
    GC -->|PASS| HUMAN["人工/审查者判 G2-G4 语义项"]
    GC -->|BLOCK| BACK["退回修订"]
    GC -->|INPUT_INSUFFICIENT| BACK
    BACK --> GR["gate_rounds.py<br/>轮次 +1"]
    GR -->|&lt;3| IN
    GR -->|≥3| EX["exceeded → 淘汰"]
    HUMAN -->|全过| PASS2["推荐"]
~~~~

**问题**：闸门**从未对真实卡判过**（未通电）。判定器已建但只测过两个非卡稿文件。

---

## 子系统 ⑥：台账与留痕

~~~~
flowchart LR
    AD["ledger add"] --> RV["revise"]
    RV --> IV["invalidate<br/>(双哈希绑定)"]
    ST["status"] --> MG["merge"]
    MG --> REG["ELIMINATED-REGISTER<br/>§6 追加"]
    RV --> RG2["gate_rounds 计数"]
~~~~

**问题**：台账 34 行中**混有 run1 的卡与 run2 的卡**，且 `merged_into` 跨轮次指向（run2 → run1 的 ID），**轮次边界不清晰**。

---

## 子系统 ⑦：失败升级

~~~~
flowchart TD
    ALLFAIL["全灭"] --> ATTR["死因归因"]
    ATTR -->|G1 集中| E1["补证据地基"]
    ATTR -->|G4 集中| E2["转边界/归因型"]
    ATTR -->|G5 集中| E3["引用网络查新"]
    E1 --> L1["① 同轴换角度"]
    L1 --> L2["② 轴扩展(8切面)"]
    L2 --> L3["③ 提问类型转换"]
    L3 --> STOP["④ 停止+如实报告"]
~~~~

**问题**：**从未触发**，三级阶梯的判据（"死因 >60%"）是拍的，未经验证。

---

## 子系统 ⑧：污染防护

~~~~
flowchart LR
    GEN["生成器"] -.禁止.-> BL["黑名单"]
    AU["audit_contamination"] -->|读子会话日志| CHECK{"违规?"}
    CHECK -->|是| VOID["作废"]
    CHECK -->|否| PASS["放行"]
    MAT["§8.1 隔离矩阵"] --> GEN
    UM2["Undermind 工作区"] -.=<br/>对生成器可见.-> GEN
~~~~

**问题**：审计工具版本残留（v2/v3 有误报，v4 才正确），但**旧版未删**，新会话可能误用。

---

## 子系统 ⑨：工具层（45 → 目标 18）

| 类别 | 文件 | 处置建议 |
|---|---|---|
| **核心保留（8）** | `ledger.py` `patched_checks.py` `patched_audit.py` `patched_novelty.py` `test_rework_regressions.py` `gate_check.py` `gate_rounds.py` `audit_contamination.py` | 保留（`audit_contamination` 建议改名去掉版本号） |
| **语料管道（7）** | `sanitize_notes.py` `gen_neutral_view.py` `gen_manifest.py` `deps_check.py` `gen_zotero_index.py` `zotero_pdf_manifest.py` `stage_zotero_pdfs.py` `build_citekey_crosswalk.py` `vm_mineru_one.py` `watch_one_txt.sh` | 保留（9 个） |
| **一次性已完成（9）** | `fix_chu.py` `revert_backfill.py` `neutral_residual_fix1/2.py` `backfill_facts_min.py` `annotate_confound.py` `freeze_neutral_hashes.py` `spotcheck_removed2.py` `corpus_gap.py` `check_local_paths.py` `zotero_compare.py` `audit_reads2.py` | **归档**（移入 `round/tools/archive/`；保留证据可追溯性） |
| **迭代残留（8）** | `vm_mineru_batch.py` `batch2` `batch3` `vm_convert_pdfs.py` `vm_extract_evidence.py` `vm_mineru_quality_test.py` `audit_contamination2.py` `audit_reads.py` `spotcheck_removed.py` | **删除**（被取代，且旧版有已知缺陷/误报） |
| **失效监听（3）** | `watch_qtest.sh` `watch_vm_conversion.sh` `watch_vm_v3.sh` | **删除**（对应任务已废弃） |
| **已废弃（2）** | `ledger_add.py`（规则明说废弃）、`merge_sim.py` | **删除**（`ledger_add` 缺陷已复现存档于规则） |
| **重复模板（2）** | `HISTORY-REVIEW-PROMPT.md` `REVIEW-ROLE-PROMPTS.md` | **删除**（内容已并入 `rules/PROMPT-TEMPLATES.md`） |

---

## 实测矛盾清单（必改）

| # | 矛盾 | 位置 | 修法 |
|---|---|---|---|
| **C1** | 回归"10 项" vs 实际 **12 项** | `EFFECTIVE-RULES-R2.md:77` | 改为 12 项（并改为"以脚本输出为准"避免再漂移） |
| **C2** | 白名单**版本号三处不一致**：§2 标题写 v3、§2 正文已含 v4 内容、其他文档写 v4 | `EFFECTIVE-RULES-R2.md:20,126` | 统一为 **v4** |
| **C3** | 流水线**步骤数不一致**：§8 写 7 段、总纲写"十步" | 两份规则 | 以 §8 为唯一权威，总纲改为引用 |
| **C4** | §8.0 批内对账**时机**与实际执行不符（规则说"历史审查前"，实际在"后"） | `EFFECTIVE-RULES-R2.md §8.0` | 改为"初筛后即可做；历史审查若顺带发现批内重复，只指认不处置" |
| **C5** | 锚件核验**责任人不明** | `§8.0.1` | 明确"主控执行，深化者不得自证" |
| **C6** | 轮次计数与台账**分离**（`gate_rounds.json` 不在 ledger） | 工具层 | 保持分离（避免污染 hash），但须在规则中注明二者关系 |
