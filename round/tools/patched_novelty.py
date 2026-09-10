#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""查新（近邻评估）修订版 —— research-ops novelty.py/retrieve.py 判断逻辑的明确补丁（本线所有）。

原件: .worktrees/research-ops/scripts/topic_harness/{novelty.py, retrieve.py}
     sha256 前缀 16b6ac5e356e6827 / d31ab5c282acd6f1（完整指纹见 round/deps/DEPENDENCIES.md）
原件 owner: harness-unify 代理（按单写入者约束本线只读复用其检索客户端，未改原件）
补丁 owner: agent/20260910-topic-loop
复现依据: round/logs/repro-group2.txt §A/§B

修掉的判断权限问题:
1. 检索失败不再升级为新颖：
   - 区分 ok_hits / ok_empty / service_unavailable / exec_error 四态（原件把 HTTP 失败的 None
     折叠成 []，空近邻在原件语义里直接产出 "novel"，且执行异常会裸逃出 novelty_check）。
   - 失败 → verdict="incomplete"（未评估），绝不输出"novel/无先例"。
   - 成功无命中 → verdict="no_hit_in_scope"，只支持"在本次查询词+通道+时间范围内未命中"的表述。
   - 服务失败时立即停止后续查询（不继续无意义的付费扩展），返回断点状态与未执行查询清单。
2. 文本相似只做"近邻线索"，不再自动判"同一工作"：
   - 启发式判定值域改为 high/mid/low_similarity_lead，语义是线索不是结论；
   - LLM 判定提示词重写：仅当 论文=同一工作身份，或 论文同时覆盖候选的〔决策时刻+信息条件+机制
     改动〕时才答 Yes；仅问题域/应用域相关 → 答 No(related)。原提示词"方法细节不重要、只看高层
     概念"的写法废除。
   - 任何 "same_or_covering" 输出为 collision_candidate，须主控比对〔条件/困难/机制/决策变化〕后
     人工裁决，本工具不自动淘汰候选。
3. 输出=近邻线索+证据+未决项；本工具不认证科研新颖性。
4. 通道与范围显式记录（本补丁默认通道仍是 S2 客户端；Undermind/arXiv/本地全文由调用方作为
   替代通道实现，传入自定义 search_fn 即可，status 语义一致）。
"""
from __future__ import annotations

import os
import sys

RO = "/Users/lge/Desktop/leo-direct-sim/.worktrees/research-ops"
if RO not in sys.path:
    sys.path.insert(0, RO)

try:  # 只读复用原件（包导入方式，规避 spec 加载的 dataclass 注册问题）
    from scripts.topic_harness import retrieve as _retrieve
    from scripts.topic_harness import novelty as _orig
except Exception as _e:  # pragma: no cover
    raise ImportError("patched_novelty 需要只读访问 research-ops 的 topic_harness: %r" % (_e,))

S_HIGH = 0.85   # 高相似线索阈值（沿用原件 SAME_TITLE_DICE 的数值，语义降级为"线索"）
S_MID = 0.50

ST_OK_HITS = "ok_hits"
ST_OK_EMPTY = "ok_empty"
ST_SERVICE = "service_unavailable"
ST_EXEC = "exec_error"


# --------------------------------------------------------------- 检索层 ----

def safe_search(query, limit=20):
    """带状态分类的检索包装。返回 {"status", "papers", "error", "channel"}。

    与原件的区别：None（HTTP 非 200/限速）→ service_unavailable，不再折叠成 []；
    传输/解析异常 → exec_error；成功才有 ok_hits/ok_empty。
    """
    try:
        resp = _retrieve.keyword_query(query, limit=limit)
    except Exception as exc:
        return {"status": ST_EXEC, "papers": [], "error": repr(exc), "channel": "s2"}
    if resp is None:
        return {"status": ST_SERVICE, "papers": [],
                "error": "keyword_query returned None (HTTP non-200 / rate limit / network)", "channel": "s2"}
    papers, skipped = [], 0
    for raw in resp:
        try:
            p = _orig._normalize_paper(raw)
        except Exception:
            skipped += 1
            continue
        if p is not None:
            papers.append(p)
    if skipped:
        return {"status": ST_OK_HITS if papers else ST_OK_EMPTY, "papers": papers,
                "error": "%d 条结果解析失败被跳过" % skipped, "channel": "s2"}
    return {"status": ST_OK_HITS if papers else ST_OK_EMPTY, "papers": papers, "error": None, "channel": "s2"}


# --------------------------------------------------------------- 判定层 ----

def _card_title(card) -> str:
    """取候选标题：dict 优先 title 字段（修复原件 card_text 展平导致的稀释不稳定），字符串取首行。"""
    if isinstance(card, dict) and card.get("title"):
        return str(card["title"]).strip()
    text = _orig.card_text(card) if not isinstance(card, str) else card
    lines = [ln.strip() for ln in (text or "").splitlines() if ln.strip()]
    return lines[0] if lines else ""


def heuristic_lead_judge(card, paper):
    """近邻线索判定（启发式，值域=线索强度，不是"同一工作"结论）。"""
    t = _card_title(card)
    score = _orig.dice_similarity(t, paper.get("title", ""))
    if score >= S_HIGH:
        j = "high_similarity_lead"
    elif score >= S_MID:
        j = "mid_similarity_lead"
    else:
        j = "low_similarity"
    return j, {"method": "title-bigram-dice(lead-only)", "score": round(score, 4),
               "card_title": t, "paper_title": paper.get("title", "")}


LEAD_JUDGE_PROMPT = (
    "You are screening neighbor literature for a research-candidate card in LEO satellite "
    "network routing + reinforcement learning. For the given paper, decide ONE of:\n"
    "- same_or_covering: the paper is the same work, OR it already addresses BOTH the same "
    "decision moment & information condition AND the same mechanism change (compare the "
    "card's conditions / difficulty / cause / decision-change fields explicitly).\n"
    "- related_not_covering: problem domain or application overlaps, but the mechanism change "
    "or decision conditions differ. Related is NOT covered.\n"
    "- different\n"
    "- unclear\n"
    "Rules: title/topic similarity alone is never sufficient for same_or_covering; you must "
    "quote which card field (conditions/difficulty/mechanism-change) the paper does or does "
    "not match. End with a single line containing exactly one of the four labels.\n"
    "CARD:\n{card}\nPAPER:\n{paper}\n"
)

LABELS = ("same_or_covering", "related_not_covering", "different", "unclear")


def parse_label(response_text):
    tokens = (response_text or "").strip().split()
    if tokens:
        last = tokens[-1].lower().strip(".!?\"'。，！？")
        if last in LABELS:
            return last
    low = (response_text or "").lower()
    for lab in LABELS:
        if lab in low:
            return lab
    return "unclear"


def llm_lead_judge(card, paper):
    """LLM 线索判定（覆盖比较式提示词）；未配置 LLM 时抛 RuntimeError，由调用方回退启发式。"""
    base_url = os.environ.get("LEO_LLM_BASE_URL") or os.environ.get("OPENAI_BASE_URL")
    model = os.environ.get("LEO_LLM_MODEL") or os.environ.get("LEO_LIT_MODEL")
    if not (base_url and model):
        raise RuntimeError("LEO_LLM_* 未配置")
    import openai  # noqa
    client, model_name = _retrieve._make_llm()
    prompt = LEAD_JUDGE_PROMPT.format(
        card=_orig.card_text(card), paper=_retrieve.format_papers_for_printing([paper], include_score=False))
    response, _cost = _retrieve._chat(client, model_name, [{"role": "user", "content": prompt}],
                                      max_tokens=1000, seed=2024, json_output=False)
    return parse_label(response), {"method": "llm-lead-judge", "model": model_name}


def default_judge():
    if os.environ.get("LEO_LLM_BASE_URL") or os.environ.get("OPENAI_BASE_URL"):
        try:
            return llm_lead_judge
        except Exception:
            pass
    return heuristic_lead_judge


# --------------------------------------------------------------- 主入口 ----

def novelty_assess(card, search_fn=None, judge_fn=None, check_n=5, max_queries=3):
    """近邻评估（不是新颖性认证）。

    返回 {
      "overall_status": "complete" | "degraded",
      "queries": [...], "query_statuses": [{query,status,error,channel}],
      "queries_not_executed": [...],
      "nearest": [{paperId,title,year,lead,lead_evidence,abstract}],
      "verdict": "collision_candidate"|"leads_only"|"no_hit_in_scope"|"incomplete",
      "note": str
    }
    """
    if search_fn is None:
        search_fn = safe_search
    if judge_fn is None:
        judge_fn = default_judge()
    text = _orig.card_text(card)
    queries = _orig.extract_queries(text, max_queries=max_queries)

    bank, q_statuses, not_executed, degraded = {}, [], [], False
    for idx, q in enumerate(queries):
        try:
            res = search_fn(q)
        except Exception as exc:  # 注入函数违约（裸异常）→ 按执行错误分类，不外泄
            res = {"status": ST_EXEC, "papers": [], "error": repr(exc), "channel": "custom"}
        st = {"query": q, "status": res.get("status"), "error": res.get("error"),
              "channel": res.get("channel", "custom")}
        q_statuses.append(st)
        if res["status"] in (ST_SERVICE, ST_EXEC):
            degraded = True
            not_executed = queries[idx + 1:]   # 断点：服务失败不继续烧后续查询
            break
        for paper in res["papers"]:
            bank.setdefault(paper["paperId"], paper)

    nearest = []
    for paper in list(bank.values())[:check_n]:
        lead, ev = judge_fn(text, paper)
        nearest.append({"paperId": paper["paperId"], "title": paper.get("title"),
                        "year": paper.get("year"), "citationCount": paper.get("citationCount", 0),
                        "abstract": paper.get("abstract"), "lead": lead, "lead_evidence": ev})

    leads = [e for e in nearest if e["lead"] in ("high_similarity_lead", "mid_similarity_lead")]
    covering = [e for e in nearest if e["lead"] == "same_or_covering"]
    if degraded:
        verdict = "incomplete"
        note = ("检索通道部分失败（见 query_statuses），未评估的查询已列为断点；"
                "本工具不认证新颖性——失败不构成无先例证据。")
    elif covering:
        verdict = "collision_candidate"
        note = ("存在疑似同/覆盖工作：仅为主控裁决线索。须由人比对〔条件/困难/机制/决策变化〕并保留依据，"
                "本工具不自动淘汰候选。")
    elif leads:
        verdict = "leads_only"
        note = ("仅得到近邻线索（相似度=检索提示）。'相关'不等于'已覆盖'；覆盖判断须回原文比对机制。")
    else:
        verdict = "no_hit_in_scope"
        note = ("在本次查询词+通道+check_n 范围内未命中。只支持限定范围的'未命中'表述，"
                "不等于领域空白；换词/换库/换时间窗须重查。")
    return {"overall_status": "degraded" if degraded else "complete",
            "queries": queries, "query_statuses": q_statuses, "queries_not_executed": not_executed,
            "nearest": nearest, "verdict": verdict, "note": note}


# 兼容别名：给只读引用原件字段的调用方一个明确名字
extract_queries = _orig.extract_queries