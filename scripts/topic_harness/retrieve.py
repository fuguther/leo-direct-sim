# -*- coding: utf-8 -*-
"""LEO 域文献检索适配器（vendor AI-Researcher 的 LEO 化封装）。

上游：NoviScl/AI-Researcher @ e5dd05a90bcadb436c07283c2f429367c6e525d3（MIT）。
参照 vendor/ai_researcher/ai_researcher/src/ 下的
  - lit_review.py（collect_papers 检索-打分-扩展循环）
  - lit_review_tools.py（Semantic Scholar 检索与 paper bank 去重）
vendor 原文件保持逐字节原样；本适配器的差异：
  1. prompt 不用上游 NLP 措辞，改用 prompts/leo_lit_review.txt（LEO 卫星路由/RL 域改写）；
  2. 模型调用走 OpenAI 兼容接口，base_url/model/api_key 从环境变量读取；
  3. S2 检索用 stdlib urllib（harness 保持 std-lib only），有 key 带 key，无 key 走公共限速。

为什么不整体 import 上游 lit_review_tools：该模块 import 时即执行
``open("../keys.json")``（上游设计，缺文件抛 FileNotFoundError），且多数上游模块顶层
依赖 openai/anthropic/retry，非本 harness 强制依赖。可干净导入的 ``utils.py``（纯 stdlib）
通过「sys.path 插入 vendor 目录」真实导入复用；纯函数（paper_filter / format_papers_for_printing /
dedup_paper_bank / 查询解析）在此按上游语义镜像实现并注明来源。
"""
import json
import os
import re
import sys
import time
from pathlib import Path

_HERE = Path(__file__).resolve().parent
VENDOR_SRC = _HERE / "vendor" / "ai_researcher" / "ai_researcher" / "src"
PROMPT_FILE = _HERE / "prompts" / "leo_lit_review.txt"

# ---- vendor 导入：sys.path 插入 vendor 目录（追加在尾部，避免遮蔽宿主环境同名模块）----
if str(VENDOR_SRC) not in sys.path:
    sys.path.append(str(VENDOR_SRC))


def _load_vendor_utils():
    """导入 vendor 的 utils.py（上游 ai_researcher/src/utils.py，纯 stdlib）。

    优先经 sys.path 正常导入；若宿主环境已有同名 ``utils`` 抢占解析，
    则按文件路径以独立模块名加载，绝不污染 sys.modules。
    """
    import importlib
    import importlib.util

    want = str(VENDOR_SRC / "utils.py")
    try:
        spec = importlib.util.find_spec("utils")
        if spec is not None and spec.origin and os.path.samefile(spec.origin, want):
            return importlib.import_module("utils")
    except Exception:
        pass
    spec = importlib.util.spec_from_file_location("ai_researcher_vendor_utils", want)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


vendor_utils = _load_vendor_utils()

# ---------------------------------------------------------------- prompts ----

def _parse_prompt_sections(path=None):
    """解析 prompts/leo_lit_review.txt：[SECTION:名字] 小节 → dict。"""
    text = Path(path or PROMPT_FILE).read_text(encoding="utf-8")
    sections, current = {}, None
    for line in text.splitlines():
        m = re.match(r"^\[SECTION:([A-Za-z_]+)\]\s*$", line)
        if m:
            current = m.group(1)
            sections[current] = []
        elif current is not None:
            sections[current].append(line)
    return {k: "\n".join(v).strip() for k, v in sections.items()}


def build_initial_query(topic):
    """首轮查询：上游 lit_review.initial_search(mode="topic") 的确定性行为，
    直接 KeywordQuery(topic 小写)，不调 LLM。"""
    return 'KeywordQuery("' + topic.lower().strip() + '")'


def build_next_query_prompt(topic, grounding_papers, past_queries):
    """组装下一轮查询扩展 prompt（SECTION:NEXT_QUERY 的 LEO 域改写）。"""
    tpl = _parse_prompt_sections()["NEXT_QUERY"]
    return tpl.format(
        topic=topic.strip(),
        grounding_papers=grounding_papers,
        past_queries="\n".join(past_queries),
        papers="",
    )


def build_scoring_prompt(topic, papers_str):
    """组装论文相关性打分 prompt（SECTION:SCORE 的 LEO 域改写）。"""
    tpl = _parse_prompt_sections()["SCORE"]
    return tpl.format(topic=topic.strip(), grounding_papers="", past_queries="", papers=papers_str)


# ------------------------------------------------- S2 查询解析与执行（镜像） ----

SEARCH_URL = "https://api.semanticscholar.org/graph/v1/paper/search/"
GRAPH_URL = "https://api.semanticscholar.org/graph/v1/paper/"
REC_URL = "https://api.semanticscholar.org/recommendations/v1/papers/forpaper/"

QUERY_RE = re.compile(r'^(KeywordQuery|PaperQuery|GetReferences)\("([^"]+)"\)$')


def parse_llm_query(text):
    """解析 LLM 输出的查询（镜像上游 lit_review_tools.parse_and_execute 的正则约定）。

    返回 (func, arg) 或 None。上游对多行输出逐行处理；这里接受首条可解析行。
    """
    for line in (text or "").strip().splitlines():
        m = QUERY_RE.match(line.strip())
        if m:
            return m.group(1), m.group(2)
    return None


def _s2_get(url, params, tries=3, timeout=30):
    """S2 GET：有 key（LEO_S2_API_KEY/S2_API_KEY）带 x-api-key，无 key 走公共限速。

    429 指数退避重试（公共限速场景）；HTTP 非 200 最终返回 None（对齐上游
    KeywordQuery/PaperQuery 在非 200 时返回 None 的语义）；传输层错误重试后抛 RuntimeError
    （fail-loud，不静默吞网络故障）。
    """
    from urllib.error import HTTPError, URLError
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen

    key = os.environ.get("LEO_S2_API_KEY") or os.environ.get("S2_API_KEY")
    headers = {"User-Agent": "leo-topic-harness (AI-Researcher LEO adapter)"}
    if key:
        headers["x-api-key"] = key
    req_url = url + "?" + urlencode(params)
    last_err = None
    for attempt in range(tries):
        try:
            with urlopen(Request(req_url, headers=headers), timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except HTTPError as e:
            last_err = e
            if e.code == 429 and attempt < tries - 1:
                time.sleep(2 ** attempt + 1)
                continue
            return None
        except (URLError, TimeoutError, OSError) as e:
            last_err = e
            if attempt < tries - 1:
                time.sleep(1)
    raise RuntimeError("Semantic Scholar 请求失败（网络层）: %r" % (last_err,))


def keyword_query(keyword, limit=20):
    """镜像上游 lit_review_tools.KeywordQuery（字段集一致）。"""
    resp = _s2_get(SEARCH_URL, {
        "query": keyword, "limit": limit,
        "fields": "title,year,citationCount,abstract,tldr",
    })
    if resp is None:
        return None
    if "total" in resp and resp["total"] == 0:
        return None
    return resp.get("data", resp)


def paper_query(paper_id, limit=20):
    """镜像上游 lit_review_tools.PaperQuery（S2 推荐接口）。"""
    resp = _s2_get(REC_URL + paper_id, {
        "paperId": paper_id, "limit": limit,
        "fields": "title,year,citationCount,abstract",
    })
    if resp is None:
        return None
    return resp.get("recommendedPapers") or None


def get_references(paper_id, limit=100):
    """镜像上游 lit_review_tools.GetReferences，但用 S2 嵌套字段一次取回引用列表
    （上游对每条引用再发一次详情请求，N+1 次；适配器单请求化，语义保留：返回
    经 paper_filter 过滤的引用论文列表）。"""
    resp = _s2_get(GRAPH_URL + paper_id, {
        "fields": "title,year,citationCount,abstract,references.paperId,references.title,"
                  "references.year,references.abstract,references.citationCount",
    })
    if resp is None:
        return None
    refs = [r for r in (resp.get("references") or []) if r.get("paperId")]
    return paper_filter(refs[:limit]) or None


def execute_query(query):
    """镜像上游 lit_review_tools.parse_and_execute：解析并执行一条查询。"""
    parsed = parse_llm_query(query)
    if parsed is None:
        return None
    func, arg = parsed
    if func == "KeywordQuery":
        papers = keyword_query(arg)
    elif func == "PaperQuery":
        papers = paper_query(arg)
    elif func == "GetReferences":
        papers = get_references(arg)
    else:
        return None
    if papers is None:
        return None
    return paper_filter(papers) or None


def paper_filter(paper_lst):
    """镜像上游 lit_review_tools.paper_filter：剔除 survey/review/position paper。"""
    out = []
    for paper in paper_lst:
        title = (paper.get("title") or "")
        low = title.lower()
        if "survey" in low or "review" in low or "position paper" in low:
            continue
        out.append(paper)
    return out


def format_papers_for_printing(paper_lst, include_abstract=True, include_score=True, include_id=True):
    """镜像上游 lit_review_tools.format_papers_for_printing。"""
    out = ""
    for paper in paper_lst:
        if include_id and paper.get("paperId"):
            out += "paperId: " + str(paper["paperId"]).strip() + "\n"
        out += "title: " + str(paper.get("title", "")).strip() + "\n"
        if include_abstract and paper.get("abstract"):
            out += "abstract: " + str(paper["abstract"]).strip() + "\n"
        elif include_abstract and paper.get("tldr") and paper["tldr"].get("text"):
            out += "tldr: " + paper["tldr"]["text"].strip() + "\n"
        if include_score and "score" in paper:
            out += "relevance score: " + str(paper["score"]) + "\n"
        out += "\n"
    return out


def dedup_paper_bank(sorted_paper_bank):
    """镜像上游 lit_review_tools.dedup_paper_bank（paperId/规范标题/摘要去重，保留先出现者）。

    差异：上游在 collect_papers 流程里已保证摘要非空，故对 None==None 也判重；
    适配器仅在双方摘要非真值时跳过摘要比较，避免两条无摘要的不同论文被误删。
    """
    idx_to_remove = []
    for i in reversed(range(len(sorted_paper_bank))):
        for j in range(i):
            a, b = sorted_paper_bank[i], sorted_paper_bank[j]
            if str(a.get("paperId", "")).strip() == str(b.get("paperId", "")).strip() and a.get("paperId"):
                idx_to_remove.append(i)
                break
            if "".join(str(a.get("title", "")).lower().split()) == \
                    "".join(str(b.get("title", "")).lower().split()):
                idx_to_remove.append(i)
                break
            if a.get("abstract") and b.get("abstract") and a["abstract"] == b["abstract"]:
                idx_to_remove.append(i)
                break
    return [p for i, p in enumerate(sorted_paper_bank) if i not in idx_to_remove]


# ------------------------------------------------------------ LLM 调用 ----

def _llm_config():
    """OpenAI 兼容接口配置：base_url/model 可配（环境变量）。缺一即 fail-loud。"""
    base_url = os.environ.get("LEO_LLM_BASE_URL") or os.environ.get("OPENAI_BASE_URL")
    model = os.environ.get("LEO_LLM_MODEL") or os.environ.get("LEO_LIT_MODEL")
    api_key = os.environ.get("LEO_LLM_API_KEY") or os.environ.get("OPENAI_API_KEY")
    missing = [name for name, val in (("base_url", base_url), ("model", model)) if not val]
    if missing:
        raise RuntimeError(
            "run_lit_review 需要 OpenAI 兼容接口配置，缺少环境变量: "
            + ", ".join("LEO_LLM_" + m.upper() for m in missing)
            + "（或对应 OPENAI_BASE_URL）"
        )
    return base_url, model, api_key


def _make_llm():
    """懒加载 openai 客户端（仅运行期需要；模块导入与离线测试不依赖它）。"""
    base_url, model, api_key = _llm_config()
    try:
        from openai import OpenAI
    except ImportError as e:
        raise RuntimeError("需要安装 openai 包（pip install openai）才能调用 LLM") from e
    client = OpenAI(base_url=base_url, api_key=api_key or "EMPTY")
    return client, model


def _chat(client, model, messages, max_tokens, seed, json_output=False):
    """经 vendor utils.call_api 走上游统一调用契约（OpenAI 兼容分支）。

    说明：call_api 按 model 名含 "claude" 时会走 Anthropic 原生协议；本适配器的
    client 是 OpenAI 兼容客户端，故对 claude 命名 fail-loud 拒绝，避免错路。
    """
    if "claude" in model.lower():
        raise ValueError("LEO harness 仅支持 OpenAI 兼容接口，请勿把 model 配置为 claude 系命名")
    return vendor_utils.call_api(
        client, model, messages, temperature=0.0, max_tokens=max_tokens,
        seed=seed, json_output=json_output,
    )


def _loads_lenient(text):
    """解析打分 JSON；容忍 ```json 围栏（上游直接 json.loads，此处略加固，失败仍 fail-loud）。"""
    t = (text or "").strip()
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        t2 = re.sub(r"^```(?:json)?\s*|\s*```$", "", t, flags=re.S)
        return json.loads(t2)


def _score_papers(client, model, seed, paper_lst, topic):
    """镜像上游 lit_review.paper_score：LLM 对每篇论文 1-10 打分（JSON）。"""
    prompt = build_scoring_prompt(topic, format_papers_for_printing(paper_lst))
    messages = [{"role": "user", "content": prompt}]
    response, cost = _chat(client, model, messages, max_tokens=4000, seed=seed, json_output=True)
    return _loads_lenient(response), cost


# ------------------------------------------------------------ 主入口 ----

def run_lit_review(topic, bank_limit=60, grounding_k=10, max_iters=10, seed=2024, verbose=False):
    """LEO 域文献检索入口（上游 collect_papers 流程的 LEO 化移植）。

    流程：确定性首查 KeywordQuery(topic) → S2 检索 → LLM 打分 → 循环
    （SECTION:NEXT_QUERY 生成新查询 → 检索 → 过滤 → 打分）直至 bank_limit 或 max_iters →
    按分排序 + dedup_paper_bank。

    返回 {"paper_bank": [...], "total_cost": float, "queries": [...]}。
    """
    client, model = _make_llm()
    paper_bank, all_queries, total_cost = {}, [], 0.0

    def _log(msg):
        if verbose:
            print(msg)

    # 首轮：确定性查询（上游 initial_search mode="topic"）
    query = build_initial_query(topic)
    all_queries.append(query)
    paper_lst = execute_query(query)
    _log("initial query: %s" % query)
    if paper_lst:
        paper_lst = [p for p in paper_lst if p.get("abstract") and len(p["abstract"].split()) > 20]
        paper_bank = {p["paperId"]: p for p in paper_lst}
        scores, cost = _score_papers(client, model, seed, paper_lst, topic)
        total_cost += cost or 0
        for k in paper_bank:
            paper_bank[k]["score"] = 0
        for k, v in scores.items():
            if k in paper_bank:
                paper_bank[k]["score"] = v

    # 扩展循环（镜像上游 while len(bank) < max_papers and iter < 10）
    it = 0
    while len(paper_bank) < bank_limit and it < max_iters:
        data_list = [{"id": pid, **info} for pid, info in paper_bank.items()]
        grounding = sorted(data_list, key=lambda x: x.get("score", 0), reverse=True)[:grounding_k]
        prompt = build_next_query_prompt(
            topic, format_papers_for_printing(grounding), all_queries)
        response, cost = _chat(client, model, [{"role": "user", "content": prompt}],
                               max_tokens=100, seed=seed, json_output=False)
        total_cost += cost or 0
        new_query = response.strip()
        all_queries.append(new_query)
        _log("new query: %s" % new_query)
        try:
            paper_lst = execute_query(new_query)
        except Exception:
            paper_lst = None
        if paper_lst:
            paper_lst = [p for p in paper_lst if p.get("abstract") and len(p["abstract"].split()) > 50]
            paper_lst = [p for p in paper_lst if p["paperId"] not in paper_bank]
            for p in paper_lst:
                p["score"] = 0
            paper_bank.update({p["paperId"]: p for p in paper_lst})
            if paper_lst:
                scores, cost = _score_papers(client, model, seed, paper_lst, topic)
                total_cost += cost or 0
                for k, v in scores.items():
                    if k in paper_bank:
                        paper_bank[k]["score"] = v
        else:
            _log("No new papers found in this round.")
        it += 1

    sorted_data = sorted(
        ({"id": pid, **info} for pid, info in paper_bank.items()),
        key=lambda x: x.get("score", 0), reverse=True)
    sorted_data = dedup_paper_bank(sorted_data)
    return {"paper_bank": sorted_data, "total_cost": total_cost, "queries": all_queries}
