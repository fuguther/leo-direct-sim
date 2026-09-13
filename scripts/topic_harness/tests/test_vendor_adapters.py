# -*- coding: utf-8 -*-
"""vendor AI-Researcher 适配器离线测试：dedup Dice 回退、novelty 响应解析、retrieve prompt 组装。

纪律：全部 mock/离线 —— 不联网、不下模型、不真实调用任何 API；
sentence-transformers 路径只经注入的 FakeModel 验证，Dice 路径经
LEO_DEDUP_BACKEND=dice 强制（本环境本就未安装该包，双保险）。
相似度断言值均为对 scripts/topic_harness/dedup.py 实测校准值。
"""
import os
from types import SimpleNamespace

from scripts.topic_harness import dedup as dedup_mod
from scripts.topic_harness import novelty as novelty_mod
from scripts.topic_harness import retrieve as retrieve_mod

VENDOR_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "vendor", "ai_researcher",
)

# 实测校准值对应的标题对
t_A1 = "DQN based routing for LEO satellite networks"      # 基准
t_A2 = "DQN based routing for LEO satellite networks!"      # 仅标点差异 → dice 1.0
t_A3 = "DQN based routing for LEO satellite network"        # 单复数差异 → dice 0.9877
t_B = "Federated learning for credit card fraud detection"  # 无关 → dice 0.4


def _force_dice(monkeypatch):
    monkeypatch.setenv("LEO_DEDUP_BACKEND", "dice")


# ---------------------------------------------------------------- dedup ----

class _FakeSTModel:
    """替身 sentence-transformers 模型：encode 返回预置单位向量。"""

    def __init__(self, vectors):
        import numpy as np
        self._v = np.array(vectors, dtype=float)

    def encode(self, texts):
        import numpy as np
        return self._v[: len(texts)]


def test_dice_similarity_bounds_and_values():
    assert dedup_mod.dice_similarity(t_A1, t_A1) == 1.0
    assert dedup_mod.dice_similarity("abc", "xyz") == 0.0
    assert dedup_mod.dice_similarity("", "abc") == 0.0
    assert dedup_mod.dice_similarity(t_A1, t_A2) == 1.0          # 标点不影响
    assert round(dedup_mod.dice_similarity(t_A1, t_A3), 4) == 0.9877
    assert round(dedup_mod.dice_similarity(t_A1, t_B), 4) == 0.4
    # 标点规范化对齐上游 process_text
    assert dedup_mod.bigrams("Hello, World!") == dedup_mod.bigrams("hello world")


def test_dice_fallback_backend_and_merge(monkeypatch):
    _force_dice(monkeypatch)
    cards = [t_A1, t_A2, t_B, t_A3]
    suggestions = dedup_mod.dedup(cards)
    assert all(s["backend"] == "dice" and s["threshold"] == dedup_mod.DICE_THRESHOLD
               for s in suggestions)
    assert len(suggestions) == 1
    s = suggestions[0]
    assert s["keep_index"] == 0 and s["keep"] == t_A1
    assert [d["index"] for d in s["drop"]] == [1, 3]            # A2 与 A3 被并入 A1
    sims = {d["index"]: d["similarity"] for d in s["drop"]}
    assert sims[1] == 1.0 and round(sims[3], 4) == 0.9877
    # 无关卡保留
    assert t_B in [cards[i] for i in (2,)] and all(d["card"] != t_B for d in s["drop"])


def test_dedup_threshold_override_strictly_greater(monkeypatch):
    _force_dice(monkeypatch)
    # 上游语义：严格大于阈值才合并（0.9877）
    assert dedup_mod.dedup([t_A1, t_A3], threshold=0.99) == []
    merged = dedup_mod.dedup([t_A1, t_A3], threshold=0.98)
    assert len(merged) == 1 and merged[0]["threshold"] == 0.98


def test_embed_path_with_fake_model(monkeypatch):
    monkeypatch.setattr(dedup_mod, "_load_model", lambda: _FakeSTModel(
        [[1.0, 0.0], [1.0, 0.0], [0.0, 1.0]]))
    emb = dedup_mod.embed_cards(["dup", "dup", "other"])
    assert emb is not None and emb.shape == (3, 2)
    matrix, backend, threshold = dedup_mod.similarity_matrix(["dup", "dup", "other"])
    assert backend == "embed" and threshold == dedup_mod.EMBED_THRESHOLD == 0.8
    assert abs(float(matrix[0][1]) - 1.0) < 1e-9 and abs(float(matrix[0][2])) < 1e-9
    suggestions = dedup_mod.dedup(["dup", "dup", "other"])
    assert len(suggestions) == 1
    assert suggestions[0]["backend"] == "embed"
    assert [d["index"] for d in suggestions[0]["drop"]] == [1]


def test_embed_cards_returns_none_when_forced_dice(monkeypatch):
    _force_dice(monkeypatch)
    assert dedup_mod.embed_cards(["a", "b"]) is None
    matrix, backend, threshold = dedup_mod.similarity_matrix(["a", "b"])
    assert backend == "dice" and threshold == dedup_mod.DICE_THRESHOLD == 0.6


def test_thresholds_are_separate_constants():
    assert dedup_mod.EMBED_THRESHOLD == 0.8 and dedup_mod.DICE_THRESHOLD == 0.6
    assert dedup_mod.EMBED_THRESHOLD != dedup_mod.DICE_THRESHOLD
    assert dedup_mod.MODEL_NAME == "all-MiniLM-L6-v2"


def test_card_text_variants():
    assert dedup_mod.card_text("  raw text  ") == "raw text"
    d = {"title": "T1", "conditions": "cond", "difficulty": "", "unknown": "x"}
    assert dedup_mod.card_text(d) == "T1 cond"
    obj = SimpleNamespace(title="T2", cause_hypothesis="why")
    assert dedup_mod.card_text(obj) == "T2 why"


def test_active_backend_membership(monkeypatch):
    _force_dice(monkeypatch)
    assert dedup_mod.active_backend() == "dice"


# -------------------------------------------------------------- novelty ----

def _paper(pid, title, abstract=None, year=2024, cites=10):
    return {"paperId": pid, "title": title, "year": year,
            "citationCount": cites, "abstract": abstract}


def test_parse_judgment_variants():
    assert novelty_mod.parse_judgment("Both target LEO routing with MARL. Yes") == "same"
    assert novelty_mod.parse_judgment("Different problem. No.") == "different"   # 容忍尾标点
    assert novelty_mod.parse_judgment("cannot decide") == "unclear"
    assert novelty_mod.parse_judgment("") == "unclear"
    assert novelty_mod.parse_judgment("yes") == "same"


def test_normalize_paper_tldr_fallback_and_skip():
    raw = {"paperId": "p1", "title": "T", "abstract": None,
           "year": 2023, "citationCount": 3, "tldr": {"text": "tldr text"}}
    norm = novelty_mod._normalize_paper(raw)
    assert norm["abstract"] == "tldr text" and norm["year"] == 2023
    assert novelty_mod._normalize_paper({"title": "no id"}) is None
    assert novelty_mod._normalize_paper({"paperId": "p"}) is None
    assert novelty_mod._normalize_paper(None) is None


def test_extract_queries_deterministic_with_domain_terms():
    card = {"title": "Multi-Agent Deep RL for LEO Routing",
            "conditions": "We study distributed routing with GNN embeddings and PPO training"}
    q1 = novelty_mod.extract_queries(card)
    q2 = novelty_mod.extract_queries(card)  # 同输入确定性
    assert q1 == q2
    assert len(q1) <= 3
    assert q1[0].startswith("Multi-Agent Deep RL for LEO Routing")
    assert q1[0].endswith("LEO satellite routing")
    assert any("satellite" in q or "routing" in q for q in q1)
    assert novelty_mod.extract_queries("") == ["LEO satellite routing reinforcement learning"]


def _fake_search(papers_or_map):
    """假检索器。

    - 传 list：对任意查询返回同一列表（用于只验证 verdict/去重逻辑的用例）；
    - 传 dict：按查询字符串精确匹配（用于确需区分查询的用例）。
    """
    if isinstance(papers_or_map, dict):
        def search(query):
            return list(papers_or_map.get(query, []))
        return search

    def search(query):
        return list(papers_or_map)
    return search


def test_novelty_check_collision(monkeypatch):
    p_near = _paper("p1", "DQN based routing for LEO satellite networks", abstract="uses DQN")
    p_other = _paper("p2", "Federated learning for credit card fraud detection", abstract="fraud")
    results = [p_near, p_other]
    judge = lambda text, paper: (
        ("same", {"method": "mock"}) if paper["paperId"] == "p1" else ("different", {}))
    out = novelty_mod.novelty_check(
        {"title": "DQN based routing for LEO satellite networks", "conditions": "DQN routing"},
        search_fn=_fake_search(results), judge_fn=judge)
    assert out["verdict"] == "collision"
    assert out["nearest"][0]["paperId"] == "p1" and out["nearest"][0]["judgment"] == "same"


def test_novelty_check_novel_and_empty(monkeypatch):
    judge = lambda text, paper: ("different", {"method": "mock"})
    out = novelty_mod.novelty_check(
        {"title": "A brand new routing idea"},
        search_fn=_fake_search([_paper("p9", "Unrelated Paper", abstract="x")]),
        judge_fn=judge)
    assert out["verdict"] == "novel" and len(out["nearest"]) == 1
    empty = novelty_mod.novelty_check(
        {"title": "A brand new routing idea"}, search_fn=_fake_search({}), judge_fn=judge)
    assert empty["verdict"] == "novel" and empty["nearest"] == []


def test_novelty_check_unclear_band_and_check_n(monkeypatch):
    # 0.6897 ∈ [UNCLEAR_TITLE_DICE, SAME_TITLE_DICE) → 走启发式判 unclear
    out = novelty_mod.novelty_check(
        "LEO satellite routing",
        search_fn=_fake_search([_paper("p1", "LEO routing")]),
        judge_fn=novelty_mod._heuristic_judge)
    assert out["nearest"][0]["judgment"] == "unclear"
    assert out["verdict"] == "unclear"
    assert out["nearest"][0]["evidence"]["method"] == "title-bigram-dice"

    # check_n 截断：6 篇唯一论文只取前 5（对齐上游 --check_n 默认 5）
    papers = [_paper("p%d" % i, "Unique Paper Number %d" % i) for i in range(6)]
    judge = lambda text, paper: ("different", {})
    out5 = novelty_mod.novelty_check("Some LEO routing card",
                                     search_fn=_fake_search(papers), judge_fn=judge)
    assert len(out5["nearest"]) == 5


def test_heuristic_judge_bands_use_real_dice():
    # same 带（实测 0.8824 ≥ 0.85）
    j, ev = novelty_mod._heuristic_judge(
        "Deep reinforcement learning for LEO satellite handover",
        _paper("p", "Deep reinforcement learning for satellite handover optimization"))
    assert j == "same" and ev["score"] == 0.8824
    # different 带（实测 0.4 < 0.5）
    j, ev = novelty_mod._heuristic_judge(t_A1, _paper("p", t_B))
    assert j == "different" and ev["score"] == 0.4


def test_novelty_check_dedups_across_queries_keeping_first(monkeypatch):
    p_dup = _paper("p1", "Same Paper", abstract="a")
    # 按调用次序给不同结果，直接测"跨查询去重、保留首现"，不依赖具体查询串
    seq = [[p_dup, _paper("p2", "Second")], [p_dup]]
    calls = {"n": 0}

    def search(query):
        calls["n"] += 1
        return list(seq[min(calls["n"], len(seq)) - 1])

    seen = []
    judge = lambda text, paper: (seen.append(paper["paperId"]) or ("different", {}))
    out = novelty_mod.novelty_check("LEO routing card", search_fn=search, judge_fn=judge)
    assert [n["paperId"] for n in out["nearest"]] == ["p1", "p2"]  # p_dup 只保留首现
    assert calls["n"] >= 2  # 确实跨了多条查询


# ------------------------------------------------------------- retrieve ----

def test_prompt_sections_exist():
    sections = retrieve_mod._parse_prompt_sections()
    assert sorted(sections) == ["NEXT_QUERY", "SCORE"]
    assert all(sections[k].strip() for k in sections)


def test_next_query_prompt_assembly():
    grounding = retrieve_mod.format_papers_for_printing(
        [{"paperId": "p1", "title": "Grounding Paper", "abstract": "Some LEO abstract"}])
    prompt = retrieve_mod.build_next_query_prompt(
        "LEO satellite routing with multi-agent RL", grounding,
        ['KeywordQuery("old query")'])
    assert "LEO satellite routing with multi-agent RL" in prompt
    assert 'KeywordQuery("keyword")' in prompt          # 上游三函数菜单保留
    assert 'PaperQuery("paperId")' in prompt and 'GetReferences("paperId")' in prompt
    assert "Grounding Paper" in prompt and "KeywordQuery(\"old query\")" in prompt
    assert "LEO" in prompt and "reinforcement learning" in prompt
    assert "{" not in prompt                            # 占位符全部填充
    assert "Natural Language Processing" not in prompt  # NLP 域措辞已改写


def test_scoring_prompt_assembly():
    papers = retrieve_mod.format_papers_for_printing(
        [{"paperId": "p9", "title": "Scored Paper", "abstract": "abstract body",
          "score": 0}])
    prompt = retrieve_mod.build_scoring_prompt("LEO routing via PPO", papers)
    assert "LEO routing via PPO" in prompt
    assert "1 to 10" in prompt and '"paperID: score"' in prompt
    assert "Scored Paper" in prompt and "abstract: abstract body" in prompt
    assert "{" not in prompt and "Natural Language Processing" not in prompt


def test_initial_query_matches_upstream_topic_mode():
    # 上游 lit_review.initial_search(mode="topic")：确定性 KeywordQuery(topic 小写)
    assert retrieve_mod.build_initial_query("LEO Satellite Routing with Multi-Agent RL") \
        == 'KeywordQuery("leo satellite routing with multi-agent rl")'


def test_parse_llm_query_variants():
    assert retrieve_mod.parse_llm_query('KeywordQuery("leo routing")') == ("KeywordQuery", "leo routing")
    assert retrieve_mod.parse_llm_query('intro line\nPaperQuery("abc123")') == ("PaperQuery", "abc123")
    assert retrieve_mod.parse_llm_query('  GetReferences("p1")  ') == ("GetReferences", "p1")
    assert retrieve_mod.parse_llm_query("no query here") is None
    assert retrieve_mod.parse_llm_query("") is None


def test_dedup_paper_bank_mirrors_upstream():
    p1 = {"paperId": "x", "title": "Alpha Routing", "abstract": "a1", "score": 5}
    p2 = {"paperId": "y", "title": "alpha   routing", "abstract": "a2", "score": 4}  # 规范标题同 p1
    p3 = {"paperId": "x", "title": "Other Title", "abstract": "a3", "score": 3}     # paperId 同 p1
    p4 = {"paperId": "z", "title": "Beta Handover", "abstract": "a4", "score": 2}
    out = retrieve_mod.dedup_paper_bank([p1, p2, p3, p4])
    assert out == [p1, p4]
    # 无摘要论文不因摘要比较被误删（适配器差异点）
    q1 = {"paperId": "u1", "title": "T One", "abstract": None, "score": 1}
    q2 = {"paperId": "u2", "title": "T Two", "abstract": None, "score": 1}
    assert retrieve_mod.dedup_paper_bank([q1, q2]) == [q1, q2]


def test_paper_filter_mirrors_upstream():
    papers = [
        {"paperId": "1", "title": "A Survey of LEO Routing"},
        {"paperId": "2", "title": "Position Paper on Handover"},
        {"paperId": "3", "title": "DQN for LEO Routing"},
    ]
    assert [p["paperId"] for p in retrieve_mod.paper_filter(papers)] == ["3"]


# ------------------------------------------------- vendor 完整性与导入 ----

def test_vendor_utils_resolves_to_vendor_path():
    # sys.path 插入 vendor 目录后，utils 应解析到 vendor 快照（或按文件路径等价加载）
    vfile = os.path.realpath(retrieve_mod.vendor_utils.__file__)
    assert vfile == os.path.realpath(
        os.path.join(VENDOR_DIR, "ai_researcher", "src", "utils.py"))
    assert hasattr(retrieve_mod.vendor_utils, "call_api")
    assert hasattr(retrieve_mod.vendor_utils, "format_plan_json")


def test_vendor_snapshot_integrity():
    src_dir = os.path.join(VENDOR_DIR, "ai_researcher", "src")
    expected = {
        "lit_review.py", "lit_review_tools.py", "dedup_ideas.py",
        "analyze_ideas_semantic_similarity.py", "novelty_check.py",
        "utils.py", "self_improvement.py",
    }
    assert expected.issubset(set(os.listdir(src_dir)))
    with open(os.path.join(VENDOR_DIR, "LICENSE"), encoding="utf-8") as f:
        lic = f.read()
    assert "MIT License" in lic and "Chenglei Si" in lic
    with open(os.path.join(VENDOR_DIR, "VENDOR-README.md"), encoding="utf-8") as f:
        readme = f.read()
    assert "e5dd05a90bcadb436c07283c2f429367c6e525d3" in readme
    assert "NoviScl/AI-Researcher" in readme
