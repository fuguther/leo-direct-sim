# MinerU 全文转换 SOP（VM 端，v1.0 2026-09-10）

> 目标：把**所有获得的 PDF** 转成**最高质量**的结构化 Markdown，**一篇一篇**跑（串行、可断点、质量优先）。
> 依据：本机实测（下 §2 表格为真实数据，非估计）。

## 1. 环境事实（先看这个）

| 项 | 值 |
|---|---|
| 转换机 | `vm`（`cuda-liguang13`），A100-PCIE-40GB（**驱动 570.133.20 / CUDA 12.8**），256 核，628 GB 内存 |
| **别**用 | `hybrid-engine`（2026-09-08 那次失败的根因是 torch/驱动版本错配，报 `NVIDIA driver too old (found 12080)`）——除非确认 torch 版本已对齐 |
| MinerU | 3.4.5，`/data/liguang13/mineru/.venv/bin/mineru` |
| 模型 | pipeline: PDF-Extract-Kit-1.0；vlm: **MinerU2.5-Pro-2605-1.2B**（均已下载，3.8 GB） |
| 配置 | `~/mineru.json`（`models-dir`、`model-source: modelscope`） |
| 工作目录 | `/data/liguang13/topic-loop-r2/`（pdfs / md / scripts / 日志） |
| 磁盘 | `/data` 359 GB 可用（**首选输出位置**）；`/` 仅 2.7 GB 可用 → 必须设 `TMPDIR=/data/liguang13/tmp` |
| 输入 | 111 个 PDF，按 `<itemKey>.pdf` 命名（`pdfs/`） |

## 2. 模式实测对比（同一篇：CMNCS52M，Traffic-Aware MARL 2026）

| 模式 | 耗时 | 字符 | 标题 | 公式 | 图片 | 备注 |
|---|---|---|---|---|---|---|
| **pipeline + txt** | **103 s** | 92,137 | 25 | 76 | 30 | 表格以 HTML 保留（3 个 `<table>`）；公式 95% 干净 |
| pipeline + ocr | 111 s | 91,999 | 25 | 76 | 30 | **与 txt 逐项相同**（数字版 PDF 无需 OCR） |
| vlm-engine | 见 §4 | — | — | — | — | 单篇 >6 分钟，输出缓冲至结束 |
| hybrid-engine | 见 §4 | — | — | — | — | 历史失败（驱动错配） |

**已确认结论**：
1. **数字版 PDF 用 `-m txt` 即可**：加 OCR 不改任何指标（字符/标题/公式数完全一致）；
2. **表格被保留为 HTML**（`<table><tr><td>`），内容完整、单元格对齐正确——**不需要** `--table true` 之外的额外处理；
3. **已知瑕疵**：约 **5%** 的行内公式把数字拆开（`$1 5 8 4 + 3 \mathrm{GS}$` 应为 `1584+3 GS`；`$9 0 ~ ^{\circ}$` 应为 `90°`）。影响：**从公式里抠数字会出错**。
   → **规避规则**：承重数字优先从**正文文字**或**表格单元格**取（这两处正常）；若只出现在公式里，标注"公式渲染有空格，需回原 PDF 核"。

## 3. 标准流程（逐篇）

```bash
# 0) 一次性：确认环境
ssh vm 'nvidia-smi --query-gpu=memory.used,utilization.gpu --format=csv; pgrep -fc mineru || echo idle'

# 1) 上传 PDF（若无 rsync，用 tar over ssh）
cd <staging-pdf-dir> && tar cf - *.pdf | ssh vm 'cd /data/liguang13/topic-loop-r2/pdfs && tar xf -'
# 注意：macOS 会带 ._ 元数据文件 → 上传后清理
ssh vm 'rm -f /data/liguang13/topic-loop-r2/pdfs/._*.pdf'

# 2) 逐篇转换（串行、断点续跑、质量记录）
ssh vm 'cd /data/liguang13/topic-loop-r2 && nohup python3 scripts/vm_mineru_one.py pdfs md pipeline_txt > one_txt.log 2>&1 &'

# 3) 查看进度与质量
ssh vm 'tail -5 /data/liguang13/topic-loop-r2/one_txt.log'
ssh vm 'cat /data/liguang13/topic-loop-r2/md/results_pipeline_txt.json | python3 -m json.tool | head -30'

# 4) 取回（按需；也可留在 VM 侧由主控读取）
```

**脚本行为**（`round/tools/vm_mineru_one.py`）：
- 串行处理，**每篇独占 GPU**（避免并行显存抖动与降级）；
- 已有合格 MD（≥2000 字符）→ 跳过（断点续跑）；
- 每篇记录：字符数 / 标题数 / 管道表数 / HTML 表数 / 公式数 / 图片数 / 耗时 → `results_<mode>.json`；
- 失败**不改用低质量模式**（质量优先），记录失败原因供人工处置。

## 4. 模式选择决策规则

| 情形 | 用什么 |
|---|---|
| 数字版 PDF（绝大多数期刊/会议论文） | **`pipeline_txt`**（已实测最优性价比） |
| 扫描件 / 图片型 PDF（正文文字抽不出或极短） | 重跑该篇 `pipeline_ocr` |
| 表格/公式极复杂、且该篇是**承重证据来源** | 单独跑 `vlm-engine`（慢，只对关键篇） |
| 批量、要快 | 绝不用 vlm |

**"最好"的工程定义**（本课题）：对 **关键承重论文**用最高质量模式；对其余用已验证的高性价比模式。**盲目全量跑 vlm 是浪费**——除非实测显示它在关键指标上显著更优（§2 待补）。

## 5. 质量校验（每批必做）

1. **产出率**：`results_*.json` 中 ok / skip / fail 计数；
2. **抽检 3 篇**：人工看标题层级、一张表格、一个公式、一段正文是否完整；
3. **数字检查**：抽查 5 个承重数字能否在 MD 中检索到（防公式空格瑕疵误伤）；
4. **失败清单**：逐篇排查原因（加密 PDF / 超时 / 扫描件）；
5. 记录到 `round/zotero/MINERU-RUN-LOG.md`（批次、模式、结果、抽检结论）。

## 6. 与 Zotero 通道的关系

| | `zotero_fulltext` | MinerU MD |
|---|---|---|
| 速度 | 秒级 | 1.7 min/篇 |
| 表格 | 平铺为文本，结构丢失 | **HTML 表保留结构** |
| 公式 | 原样文本 | LaTeX（含 5% 空格瑕疵） |
| 适用 | 快速定位/粗筛 | **承重引文、表格数据抽取** |

**规则**：粗筛用 `zotero_fulltext`；**深化与闸门阶段的承重证据必须用 MinerU MD**（或回原 PDF）。
