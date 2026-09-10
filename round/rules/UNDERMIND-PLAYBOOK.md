# Undermind 使用手册（本课题专用，v1.0 2026-09-10）

> 依据：`get_orientation` 权威文本（2026-09-10 实取）+ 本会话实测的成功/失败记录。
> 定位：Undermind 是**外部文献发现与全文阅读**的主通道；Zotero+MinerU 是**库内全文精读**通道。两者互补，不互相替代。

## 1. 账号与工作区（硬事实）

| 项 | 值 |
|---|---|
| 账号 | `torak1024@gmail.com` |
| **workspace_id** | `eef99118-f623-4a47-a34a-05c6617b7ecb`（**几乎每个工具都要）** |
| 工作区标题 | l's workspace（owner，1 成员） |
| 本机代理 | `127.0.0.1:8788`，token 每小时自动刷新（日志 `/tmp/undermind-proxy.log`） |
| Web 界面 | `https://app.undermind.ai/projects/eef99118-f623-4a47-a34a-05c6617b7ecb`（用户可直接看工作区） |

## 2. 工具清单与选用判据

| 工具 | 何时用 | 关键参数 | 成本 |
|---|---|---|---|
| `get_orientation` | **每个新会话开始调一次**（了解工作区模型） | **必须传 `{}`**，否则报错 | 极低 |
| `list_workspaces` | 拿 workspace_id | `limit` | 极低 |
| **`search_papers`** | **主力**：语义检索标题+摘要 | `workspace_id`（必填）、`sample_abstract`（查询文本）、`search_type`、`sort_override` | 中 |
| `find_papers_by_author` | 追某作者的全部工作（谱系追溯） | `workspace_id`、`request` | 中 |
| `lookup_papers_by_metadata` | 批量查题录/DOI/**cite_key**（≤300 条/次） | `workspace_id`、**`paper_metadata`（字符串列表，如 `"Title (2025)"`）** —— **不是 `items`，也不是字典列表**（实测两次踩坑） | 低 |
| `launch_deep_search` | 自包含的系统性检索（2–5 分钟，异步） | `workspace_id`、goal | **高** |
| `inspect_deep_searches` | 查深度检索状态/结果 | `workspace_id`、`names`、`status_only`、`papers_only` | 极低 |
| **`read_pdfs`** | **批量全文问答**（内部为每篇起一个子代理） | `workspace_id`、cite_keys、questions | **高** |
| `get_paper_info` | 单篇元数据/DOI/PDF 可得性 | cite_keys、`show_doi` | 低 |
| `inspect_files` / `inspect_folders` | 浏览工作区文件与文件夹 | `workspace_id`、paths/folders | 极低 |
| `write_file` / `create_folder` | **把我们的证据沉淀进工作区** | `workspace_id`、path、content | 低 |
| `star_papers` / `add_papers_to_folder` | 组织关键论文 | cite_keys | 低 |

### search_papers 的四种 search_type（**这是最强杠杆，此前完全没用上**）

| search_type | 作用 | 本课题用法 |
|---|---|---|
| `global`（默认） | 全科学语料语义检索 | 发现新方向、找库外先例 |
| `library` | 只在**工作区库**内检索 | 库内快速定位（替代手工翻 111 篇） |
| **`citing`** | 找**引用了种子论文**的工作 | **找直接对手**：查谁引用了 TAP-DAR / PRIMAL / LOZANO 等关键工作 |
| **`referenced`** | 找种子论文**引用的**工作 | **追溯谱系**：从一篇综述/关键工作向下挖 |

> `citing`/`referenced` 需要提供 `seed_papers`（cite_key 列表）。这两个模式是**最近邻核查与查新**的核心手段，比纯语义检索精确得多。

## 3. 硬性纪律（血泪教训，均已实测）

1. **`search_papers` 必须带 `workspace_id`**，且 `search_type` 取值必须是 `global|library|citing|referenced`。
   实测：省略 workspace_id 或错写 search_type → **参数校验失败**（不计入查询次数，但浪费时间）。
2. **"窄结果/空结果"不等于文献不存在**——原文明确写：
   > *"A narrow or empty search_papers result does not mean the relevant literature is absent."*
   因此**一切"无先例"表述必须限定为**："在本次查询词/语料/时窗内未命中"，**严禁**写成"该方向无人做过"。
   这条直接约束我们卡片的 G1/G5 判定措辞。
3. **`read_pdfs` 要把问题打包成一次调用**（内部按 PDF 起子代理），**跨论文综合必须自己做**，不能让子代理代劳。
4. **`launch_deep_search` 先查工作区是否已有**同类检索（`inspect_deep_searches`），避免重复烧配额；它耗时 2–5 分钟，属异步。
5. `rate_limited` → 等待后重试，不当失败处理。
6. 引用格式（写工作区文件时）：正文用 `[cite_key]`；多个键**必须逗号分隔** `[Smi98, Jon21]`；**不要给论文引用附 URL**；LaTeX 里不要放 cite key。对用户展示时用 `[[key]](https://doi.org/<DOI>)`。

## 4. 本课题的预算纪律

| 角色 | search_papers | read_pdfs | deep_search |
|---|---|---|---|
| 生成器（每路） | ≤3 | ≤2 | **禁止** |
| 历史/近邻审查者 | ≤2 | ≤2 | 禁止 |
| 主控（定向补查） | ≤3/轮 | ≤2 | 仅当工作区无同类时，且须登记理由 |

**计数口径**：只有"返回结果的成功调用"计入；参数校验失败/服务失败不计（但须在诊断节如实记录）。

## 5. 推荐的检索工作流（本课题定制）

### 5.1 生成阶段（探索）
1. `search_papers(search_type="global", sample_abstract=<一段自包含的问题描述>)`
   - `sample_abstract` 写法：**写成一整段"问题描述+关心的现象+条件"**，而非关键词堆叠（语义检索对长文本更好）；
   - 一次检索只问一个轴（强度/空间/突发），便于归因；
   - 迭代：拿首轮命中的关键论文作种子，转 `citing`/`referenced` 深挖。
2. 命中论文 → `get_paper_info(show_doi=true)` 拿 DOI/PDF 可得性 → 能自动取的会自动进工作区库。

### 5.2 查新与最近邻（关键！）
1. **对手追踪**：对已知直接对手（如 TAP-DAR）用 `citing` 找引用它的新工作；
2. **谱系下挖**：对综述/关键奠基工作用 `referenced`；
3. 两者交叉 → 得到"谁在做同一件事"的清单，再逐条比对五元组。

### 5.3 深化阶段（精读）
- 用 `read_pdfs` 一次问 3–5 个跨论文同构问题（例："该文的流量模型是什么？是否扫描了负载强度？训练与评估的负载设置是否相同？"）；
- **自己**做跨论文综合，不要让子代理给结论。

### 5.4 ⚠️ 工作区内容 = 对生成器可见（防火墙推论）

**关键风险**：生成器持有 Undermind 工具（`inspect_files`/`inspect_folders`/`search_papers`），**因此写进 Undermind 工作区的任何内容，都等于放进生成器的可读范围**。

**硬规则**：
- 工作区**只写论文事实**（轴证据表、对手清单、论文级事实条目）；
- **严禁**写入：候选卡、候选标题、淘汰理由、排序、"我们的机会点"、任何指向本课题选题判断的内容；
- 若需记录候选相关的未决问题 → **只写本地** `round/run2/`，不进工作区。
- 违反后果同 §8.1 隔离矩阵：该批生成作废重跑。

### 5.5 证据沉淀（正确用法）
把我们的证据图谱写进工作区，好处：①用 `[cite_key]` 自动链接到论文；②用户可在 Web 界面直接看；③下次会话可直接 `inspect_files` 取回。
建议文件结构：
```
/lit-axes/traffic-intensity.md      # 强度轴：谁做了什么、合同如何
/lit-axes/spatial-nonstationary.md  # 空间轴
/lit-axes/burstiness.md             # 突发轴
/competitors/direct-opponents.md    # 直接对手清单与差异
/open-questions/<card-id>.md        # 每张卡的未决问题（供下轮检索）
```

## 6. 与 Zotero/MinerU 的分工

| 需求 | 通道 | 理由 |
|---|---|---|
| 发现新论文 | **Undermind** | 语义检索 + 引用网络 |
| 判断"是否已有直接对手" | **Undermind**（`citing`/`referenced`） | 引用关系比语义相似更准 |
| 库内 111 篇精读 | **Zotero + MinerU MD** | 全文质量高、可离线、含表格公式 |
| 承重引文回原文 | **MinerU MD → 必要时原 PDF** | 需给节号/表号 |
| 付费墙论文 | Undermind 提示后可让用户上传 PDF | 原文明确支持 |
| 跨论文综合 | **主控自己做** | Undermind 明确要求 |

## 7. 待办（本轮内执行）

1. 在工作区建 §5.4 的文件结构，把 A/B/C 三路的证据表写进去（用 cite_key）；
2. 对 TAP-DAR、PRIMAL、LOZANO、SaTE、Traffic-Aware MARL 五个关键工作跑 `citing` 检索，建立"直接对手清单"；
3. 把 `citing`/`referenced` 两个模式写进生成器与审查者的提示词模板（此前模板只提了 search_papers，未说明模式差异）。
