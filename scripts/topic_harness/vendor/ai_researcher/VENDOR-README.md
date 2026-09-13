# VENDOR: AI-Researcher（Stanford NLP）— 只读上游快照，禁止改动

- **上游仓库**: <https://github.com/NoviScl/AI-Researcher>（AI-Researcher: Autonomous Scientific Research，Chenglei Si 等，Stanford NLP）
- **上游 HEAD SHA**: `e5dd05a90bcadb436c07283c2f429367c6e525d3`（2026-09-10 shallow clone）
- **许可证**: MIT（原文见本目录 `LICENSE`，Copyright (c) 2024 Chenglei Si）。本目录及 LEO 适配器遵循该许可证保留版权与许可声明。
- **完整性**: 下列文件均为上游 HEAD 的逐字节拷贝（`cmp` 校验一致），**未做任何修改**。LEO 化适配全部在 `scripts/topic_harness/{retrieve,dedup,novelty}.py` 中以独立适配器实现。

## 复制文件清单（含 SHA256）

| 上游路径 | 本地路径 | SHA256 |
|---|---|---|
| `ai_researcher/src/lit_review.py` | `ai_researcher/src/lit_review.py` | `caf7626e21176d6b64149e2a74d3927f7e1faa52bf121237492a6c8b2ea9219f` |
| `ai_researcher/src/lit_review_tools.py` | `ai_researcher/src/lit_review_tools.py` | `8929b6d1b075ae22919be4971889d5c54f275c0a5758a6597954c47e7a37c45b` |
| `ai_researcher/src/dedup_ideas.py` | `ai_researcher/src/dedup_ideas.py` | `e5780efc9ffddf14a16c47759d73a991cbe31ac8669dc3db63d666076a0e1651` |
| `ai_researcher/src/analyze_ideas_semantic_similarity.py` | `ai_researcher/src/analyze_ideas_semantic_similarity.py` | `cf49f200a2ebccd5dd9969c585068a8736c5c221da9f326dd07ce0a41bcde647` |
| `ai_researcher/src/novelty_check.py` | `ai_researcher/src/novelty_check.py` | `290f3ae8d9cf42ddee362dd3ee5562709cf21f46ea160b470962bc288679e932` |
| `ai_researcher/src/utils.py`（直接 import 的本地辅助） | `ai_researcher/src/utils.py` | `e460fe03e758491ee81f249dc39945412d415dc315b2e19eb412340497a8a59a` |
| `ai_researcher/src/self_improvement.py`（`novelty_check.py` 直接 import 的本地辅助） | `ai_researcher/src/self_improvement.py` | `a9c8c275e2e47076a178e027327f641c8138c984e67e72f61838e6ab4a01eb03` |
| `LICENSE` | `LICENSE` | `3ed0299bfe7ddd1d39b69dd1e98bd3a5ef97fb075457456a7444284d256dc55a` |

## 已知上游导入副作用（为什么适配器不整体 import 这些模块）

1. `lit_review_tools.py` 在 **import 时**执行 `open("../keys.json")`（相对进程 CWD），缺文件即 `FileNotFoundError`；上游设计要求用户先建 `ai_researcher/keys.json`（s2_key 等）。
2. `lit_review.py` / `novelty_check.py` / `self_improvement.py` 顶层 import `openai` / `anthropic` / `retry`；`dedup_ideas.py` / `analyze_ideas_semantic_similarity.py` 顶层 import `nltk` / `sentence_transformers` —— 这些不是本 harness 的强制依赖。

因此 `scripts/topic_harness/` 下的适配器只对可干净导入的 `utils.py` 走「sys.path 插入 vendor 目录」的真实导入（`retrieve.py`/`novelty.py` 复用其 `call_api` / `format_plan_json` / `cache_output`）；其余上游模块作为**算法参照**（适配器内有逐函数镜像并注明来源行号），并在运行期按需懒加载可选依赖。

## LEO 化适配器（本目录之外，新建文件）

| 文件 | 入口 | 说明 |
|---|---|---|
| `../../retrieve.py` | `run_lit_review(topic, bank_limit=60)` | 上游 `collect_papers` 流程；prompt 换用 `../../prompts/leo_lit_review.txt`（NLP 领域措辞 → LEO 卫星路由/RL 域）；模型调用走 OpenAI 兼容接口（`LEO_LLM_BASE_URL`/`LEO_LLM_MODEL`/`LEO_LLM_API_KEY`） |
| `../../dedup.py` | `dedup(cards, threshold)` / `embed_cards(texts)` | all-MiniLM-L6-v2 懒加载；不可用时退化为字符 bigram Dice（Embed 阈值 0.8 / Dice 阈值 0.6，分开定标） |
| `../../novelty.py` | `novelty_check(card)` | Semantic Scholar 检索（有 key 带 key，无 key 公共限速）；逐篇判「是否同一工作」→ `novel\|collision\|unclear` |

## 许可证注意点

- 本快照与适配器按上游 **MIT** 许可证分发：再分发时必须保留 `LICENSE` 原文与本 README 的归属声明；不得以上游作者名义背书衍生作品。
- 上游仓库无额外的专利/商标授予；本目录内容仅作为库内源码引用。
