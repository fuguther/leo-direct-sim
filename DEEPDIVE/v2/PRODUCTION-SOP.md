# 文献管线生产 SOP（2026-09-05 定稿）

> 原则：检索多源化、提取上 VM、大文件权威源=VM、本地=工作副本、同步必校验、命令全固化。
> 适用：新文献检索 → 全文获取 → MinerU 提取 → 入库 → 索引更新。

## 0. 权威源定义（防止再分散）
- **大文件（PDF/MD/TXT）权威源 = VM**：/data/论文/papers-lib/PAPER-LIBRARY/
- **本地 = 工作副本**：DEEPDIVE/v2/PAPER-LIBRARY/（git 只收索引与脚本）
- 新增文件一律先进 VM，再同步本地；删改同样先 VM。

## 1. 检索（多源强制）
- 四系统：arXiv(https) / Crossref(rows=8) / OpenAlex / Semantic Scholar(限速3s)
- **第五路必开 = 用户 Zotero 库**（~/Zotero，120+ PDF）——覆盖盲区教训 2026-09-05
- 查询：单词 AND 组合，禁整句引号；每查询 sleep 2-3
- 所有结果落盘 retrieval/，合并去重（注意 JSON 转义与嵌套 dict 陷阱）

## 2. 全文获取分级
| 来源 | 通道 | 注意 |
|---|---|---|
| arXiv | https://arxiv.org/pdf/{id}(v1 兜底) | 2026 新稿要 v1；禁 http |
| IEEE | CARSI 会话（headless=False、18s 限速） | 单篇跑别打包；3 篇打包会挂 |
| MDPI | 浏览器 profile（403 反爬） | 见 pdf 技能；curl 必 403 |
| Elsevier/Wiley | TDM 待开通 | 先登记 stub |
| 用户 Zotero | ~/Zotero/storage/*/*.pdf | 直接复制，别动原库 |

## 3. 提取（MinerU，VM A100）
- 环境：ssh vm，venv=/data/论文/papers-lib/mineru-venv，模型缓存 hf-cache/
- 命令：`./mineru-venv/bin/mineru -p <pdf> -o <outdir> -b pipeline -l en`（单篇约41s GPU）
- 批量：/data/论文/papers-lib/run-batch.sh 逐篇串行
- env 必带：HF_HOME=/data/论文/papers-lib/hf-cache HF_HUB_CACHE=同
- 本地 mac 环境为兜底：/private/tmp/mineru-venv（同样命令）

## 4. 传输（禁止 tar|ssh 大目录）
- 从 VM 拉：`scp -q "vm:/data/论文/papers-lib/PAPER-LIBRARY/*.md" <本地目录>/`
- 本地推 VM：`scp -q <本地文件> vm:/data/论文/papers-lib/PAPER-LIBRARY/`
- **传完必校验**：`bash sync-check.sh`（文件数+MD5 抽样 10%）

## 5. 同步校验（每次传输后）
- 脚本：DEEPDIVE/scripts/sync-check.sh <本地目录> <远端目录>
- 输出：两边文件数、大小差、抽样哈希命中率

## 6. 索引（每次入库后）
- `python3 DEEPDIVE/scripts/gen-index.py` → 更新 LIBRARY-INDEX.md → git commit+push

## 7. 精读
- flash 并发 ≤3；7+1 模板；引用核对 verify_quotes.py（零伪造门槛）
- 每篇 note 落 notes/，fulltext 落 fulltext/ 或 PAPER-LIBRARY/

## 8. 踩坑速查
| 坑 | 解法 |
|---|---|
| tqdm 刷屏吞错误 | 不 grep tqdm 行，直接尾部 200B 读 |
| tar 中文路径断流 | 改 scp 直传 |
| MinerU 批量 3 篇挂 | 单篇串行 |
| torchvision::nms 缺 | 同 cu126 源重装 torchvision |
| libGL 缺 | opencv-python-headless |
| 沙箱禁 ~/.cache | HF_HOME 指 /private/tmp 或 VM 数据目录 |
