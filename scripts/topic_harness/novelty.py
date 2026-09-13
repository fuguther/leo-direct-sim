# -*- coding: utf-8 -*-
"""LEO 选题卡查新适配器（vendor AI-Researcher novelty_check.py 的 LEO 化移植）。

上游流程（ai_researcher/src/novelty_check.py @ e5dd05a9，逐字节保留于 vendor/）：
LLM 生成 S2 关键词查询 → 检索 → LLM 相似度打分排序 → 对 top-N 逐篇 novelty_score
判定「是否同一工作」→ 任一 Yes 即判不新颖（verdict: collision）。

LEO 适配差异（vendor 文件不改，差异均在适配器内）：
  1. 查询生成不用 LLM：从卡文本确定性抽取关键词并拼接 LEO 域词（可复现、可离线测试）；
  2. S2 检索走 stdlib urllib：有 LEO_S2_API_KEY/S2_API_KEY 带 key，无 key 走公共限速
     （429 指数退避；HTTP 非 200 对齐上游返回 None 的语义；传输层错误重试后 fail-loud）；
  3. 「是否同一工作」判定：配置了 OpenAI 兼容 LLM（LEO_LLM_* 且 openai 可导入）则用与
     上游 novelty_score 同型的 LEO 域 prompt 逐篇判定；否则用确定性启发式
     （标题字符 bigram Dice：≥ SAME_TITLE_DICE → same，≥ UNCLEAR_TITLE_DICE → unclear，
     否则 different）。

verdict 规则：任一 nearest 论文判 same → "collision"；否则存在 unclear → "unclear"；
否则 "novel"。LLM 判定解析对齐上游（取回答最后一个词），但容忍尾随标点（上游会把
"No." 判成未知值），无法解析时按 unclear 处理，绝不把噪声误判成 collision。

测试纪律：novelty_check 的 search_fn / judge_fn 均可注入，离线测试零网络零模型。
"""
import os
import re

try:
    from scripts.topic_harness.dedup import card_text, dice_similarity, bigrams
except ImportError:  # 允许以包内相对方式导入
    from dedup import card_text, dice_similarity, bigrams  # type: ignore

try:
    from scripts.topic_harness import retrieve as _retrieve
except ImportError:
    import retrieve as _retrieve  # type: ignore

CHECK_N = 5                 # 对齐上游 --check_n 默认 5
SAME_TITLE_DICE = 0.85      # 启发式：标题 Dice 达到即判同一工作
UNCLEAR_TITLE_DICE = 0.50   # 启发式：中间带判 unclear
S2_FIELDS = "title,year,citationCount,abstract,tldr"

_STOPWORDS = {
    "a", "an", "the", "of", "in", "on", "for", "to", "and", "or", "with", "by",
    "using", "via", "we", "our", "this", "that", "is", "are", "be", "as", "at",
    "from", "into", "through", "based", "can", "could", "improve", "improves",
    "improved", "improving", "novel", "new", "propose", "proposed", "method",
    "methods", "paper", "study", "approach", "problem", "problems", "scheme",
    "toward", "towards", "its", "their", "how", "what", "which", "when", "under",
}


# ------------------------------------------------------------- S2 检索 ----

def _search_s2(query, limit=20):
    """S2 keyword 检索（复用 retrieve 的 urllib 客户端）并规范化论文字段。"""
    resp = _retrieve.keyword_query(query, limit=limit)
    if resp is None:
        return []
    papers = []
    for raw in resp:
        paper = _normalize_paper(raw)
        if paper is not None:
            papers.append(paper)
    return papers


def _normalize_paper(raw):
    """S2 原始条目 → 统一卡结构；abstract 缺失时回退 tldr.text（上游字段用法）。"""
    if not raw or not raw.get("paperId") or not raw.get("title"):
        return None
    abstract = raw.get("abstract")
    if not abstract and raw.get("tldr") and raw["tldr"].get("text"):
        abstract = raw["tldr"]["text"]
    return {
        "paperId": raw["paperId"],
        "title": raw["title"],
        "year": raw.get("year"),
        "citationCount": raw.get("citationCount", 0),
        "abstract": abstract,
    }


# ----------------------------------------------------------- 查询构造 ----

def extract_queries(text, max_queries=3):
    """从卡文本确定性构造 S2 查询（上游用 LLM 生成 1-3 条；此处为可复现的确定性替代）。

    text: str / dict / CandidateCard；非 str 一律先经 dedup.card_text 展平
    （novelty_check 主入口已经展平，此处为直接调用与测试的同一契约）。

    q1: 标题（首行/首句）+ 固定 LEO 域词（对齐上游把 idea_name 附加 " NLP" 的做法）；
    q2: 正文高频实词 top-6（去停用词）。
    """
    if not isinstance(text, str):
        text = card_text(text)
    text = text.strip()
    if not text:
        return ["LEO satellite routing reinforcement learning"]
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    title = lines[0][:120].strip()

    words = [w for w in re.findall(r"[a-zA-Z][a-zA-Z-]+", text.lower())
         if w not in _STOPWORDS and len(w) > 2]
    counts = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    keywords = [w for w, _ in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:6]]

    queries = []
    if title:
        queries.append(title + " LEO satellite routing")
    if keywords:
        queries.append(" ".join(keywords))
    if not queries:
        queries.append("LEO satellite routing reinforcement learning")
    # 按 (内容, 长度) 去重，保持确定性顺序，截断到 max_queries（上游给 1-3 条）
    seen, out = set(), []
    for q in queries:
        if q.lower() not in seen:
            seen.add(q.lower())
            out.append(q)
    return out[:max_queries]


# ------------------------------------------------------- 同一工作判定 ----

def parse_judgment(response_text):
    """解析 LLM 逐篇判定（上游：取回答最后一个词 yes/no；此处容忍尾随标点）。"""
    tokens = (response_text or "").strip().split()
    if not tokens:
        return "unclear"
    last = tokens[-1].lower().strip(".!?\"'`。，！？")
    if last == "yes":
        return "same"
    if last == "no":
        return "different"
    return "unclear"


def _heuristic_judge(card_text_str, paper):
    """确定性判定：卡标题 vs 论文标题的字符 bigram Dice。"""
    card_title = (card_text_str or "").strip().splitlines()[0] if (card_text_str or "").strip() else ""
    score = dice_similarity(card_title, paper.get("title", ""))
    if score >= SAME_TITLE_DICE:
        judgment = "same"
    elif score >= UNCLEAR_TITLE_DICE:
        judgment = "unclear"
    else:
        judgment = "different"
    return judgment, {"method": "title-bigram-dice", "score": round(score, 4)}


_LEO_JUDGE_PROMPT = (
    "You are a professor specialized in LEO satellite network routing and reinforcement "
    "learning. You have a project proposal and want to find related works. Your job is to "
    "decide whether the given paper is directly relevant to the project and should be cited "
    "as similar work.\n"
    "The project proposal is:\n{card}\n"
    "The paper is:\n{paper}\n"
    "The project proposal and paper abstract are considered a match if both the research "
    "problem and the approach are the same. For example, if they are both trying to improve "
    "routing convergence in LEO constellations and both propose to use multi-agent "
    "reinforcement learning. Note that the method details do not matter, you should only "
    "focus on the high-level concepts and judge whether they are directly relevant.\n"
    "You should first specify what is the proposed research problem and approach. If "
    "answering yes, your explanation should be the one-sentence summary of both the abstract "
    "and the proposal and their similarity. If answering no, give the short summaries of the "
    "abstract and proposal separately, then highlight their differences. Then end your "
    "response with a binary judgment, saying either \"Yes\" or \"No\". Change to a new line "
    "after your explanation and just say Yes or No with no punctuation in the end.\n"
)


def _default_judge():
    """判定器选择：LLM 已配置（env + openai 可导入）→ LLM 判定；否则确定性启发式。"""
    base_url = os.environ.get("LEO_LLM_BASE_URL") or os.environ.get("OPENAI_BASE_URL")
    model = os.environ.get("LEO_LLM_MODEL") or os.environ.get("LEO_LIT_MODEL")
    if not (base_url and model):
        return _heuristic_judge
    try:
        import openai  # noqa: F401
    except ImportError:
        raise RuntimeError(
            "已配置 LEO_LLM_* 但缺少 openai 包；请 pip install openai，"
            "或取消 LEO_LLM_* 配置以使用确定性启发式判定")

    def judge(card_text_str, paper):
        client, model_name = _retrieve._make_llm()
        prompt = _LEO_JUDGE_PROMPT.format(
            card=card_text_str.strip(),
            paper=_retrieve.format_papers_for_printing([paper], include_score=False),
        )
        response, _cost = _retrieve._chat(
            client, model_name, [{"role": "user", "content": prompt}],
            max_tokens=1000, seed=2024, json_output=False)
        return parse_judgment(response), {"method": "llm", "model": model_name}

    return judge


# ------------------------------------------------------------- 主入口 ----

def novelty_check(card, search_fn=None, judge_fn=None, check_n=CHECK_N, max_queries=3):
    """查新：S2 检最似论文，逐篇判「是否同一工作」，给出 verdict。

    card: str / dict / CandidateCard。
    search_fn: query → [paper dict]（缺省 _search_s2；测试注入 mock）。
    judge_fn:  (card_text, paper) → (judgment, evidence)；judgment ∈ same/different/unclear。
    返回 {"queries": [...], "nearest": [...], "verdict": "novel"|"collision"|"unclear"}。
    """
    if search_fn is None:
        search_fn = _search_s2
    if judge_fn is None:
        judge_fn = _default_judge()

    text = card_text(card)
    queries = extract_queries(text, max_queries=max_queries)

    bank = {}  # paperId → paper；跨查询按 S2 相关性序保留首现（镜像上游 paper_bank.update）
    for q in queries:
        for paper in search_fn(q):
            bank.setdefault(paper["paperId"], paper)

    nearest = []
    for paper in list(bank.values())[:check_n]:
        judgment, evidence = judge_fn(text, paper)
        nearest.append({
            "paperId": paper["paperId"],
            "title": paper["title"],
            "year": paper.get("year"),
            "citationCount": paper.get("citationCount", 0),
            "abstract": paper.get("abstract"),
            "judgment": judgment,
            "evidence": evidence,
        })

    judgments = [e["judgment"] for e in nearest]
    if "same" in judgments:
        verdict = "collision"
    elif "unclear" in judgments:
        verdict = "unclear"
    else:
        verdict = "novel"
    return {"queries": queries, "nearest": nearest, "verdict": verdict}
