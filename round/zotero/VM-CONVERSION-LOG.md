# VM 语料转换记录（2026-09-10）

> 用户指示：**先批量转完，再让生成器读转好的 MD**——避免生成器各自重复下载/生成笔记，也便于统一回原文。

## 1. 为什么用 VM

- 本机 Zotero：**111 篇论文，434 MB PDF，全部有本地文件**；
- 本机已有通道 `zotero_fulltext` 可抽文本（实测单篇 2.9 万字符），但**对表格/公式/多栏排版的处理弱**；
- VM 已部署 **MinerU 3.4.5**（`/data/liguang13/mineru`，含 `.venv`），可输出结构化 Markdown（保留章节标题、公式 LaTeX、表格、图片引用、页码）；
- VM 资源：**A100-P40GB（空闲）+ 256 核 + 628 GB 内存**，转换本身不占用研究预算。

## 2. 环境取证（五步法）

| 检查 | 结果 |
|---|---|
| SSH 连通 | ✅ `vm` 可用，hostname=`cuda-liguang13` |
| GPU | ✅ A100-PCIE-40GB，驱动 570.133.20（CUDA 12.8），**0% 占用、4 MiB 显存** |
| MinerU 版本 | ✅ 3.4.5，`.venv/bin/mineru` |
| **历史失败原因** | ⚠️ 2026-09-08 的 `smoke.log` 记录：`hybrid-engine` 后端报 `RuntimeError: NVIDIA driver too old (found version 12080)` → 该次**失败源于 torch/驱动版本错配**，非环境不可用 |
| 本次对策 | 改用 `-b pipeline` 后端（更通用、CPU/GPU 皆可），实测成功 |
| 冒烟验证 | ✅ `comst_demo.pdf`（41 页综述）转换成功，输出 `comst_demo.md` **257 KB**，保留章节结构/公式/表格/图引用 |

## 3. 批量任务

- **输入**：`/data/liguang13/topic-loop-r2/pdfs/`（111 个 PDF，415 MB，按 `<itemKey>.pdf` 命名）
- **输出**：`/data/liguang13/topic-loop-r2/md/<itemKey>/auto/<itemKey>.md`
- **脚本**：`round/tools/vm_mineru_batch.py`（6 分片并行，单篇超时 30 分钟，已完成的跳过、可断点续跑）
- **日志**：`/data/liguang13/topic-loop-r2/batch.log`
- **监听作业**：DSH 后台 `bash-2`（`round/tools/watch_vm_conversion.sh`），完成后自动报告

## 4. 转换完成后的流程（既定）

1. 拉回 MD 到 `round/zotero/md/`（或保留 VM 侧、主控按需读取）；
2. 生成 **MD 语料索引**（`round/zotero/ZOTERO-MD-INDEX.md`）：itemKey ↔ 标题 ↔ 年份 ↔ MD 路径 ↔ 篇幅；
3. 把它加入白名单，**生成器直接读 MD**：
   - 承重引文给「篇名 + itemKey + 章节号」，可直接对照 MD 中的 `## I. INTRODUCTION` 一类标题定位；
   - 不再要求生成器各自下载 PDF、各自写笔记；
4. 生成器跑完后，主控把其引用的证据**沉淀进 notes-neutral 的统一格式**（避免重复劳动）。

## 5. 待确认

- 转换失败的篇目（如有）需逐个排查：是 PDF 加密/扫描件，还是脚本超时；
- 扫描件（图片型 PDF）MinerU 会走 OCR，耗时更长但可用；
- MD 中图片为相对路径引用（`images/xxx.jpg`），如需看图须把 `images/` 一并同步。
