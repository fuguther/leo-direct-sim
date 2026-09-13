# -*- coding: utf-8 -*-
"""CandidatePool 语义测试：added / merged / reopened / 只添不改。"""
import time

from scripts.topic_harness.pool import CandidateCard, CandidatePool, merge_key


def make_pool(tmp_path):
    return CandidatePool(str(tmp_path / "candidates"))


def card(title, difficulty, cause, shift, new_evidence="", card_id="", source_run=""):
    return CandidateCard(
        card_id=card_id, title=title, conditions="高负载时段",
        difficulty=difficulty, cause_hypothesis=cause, decision_shift=shift,
        possible_change="加门控", strongest_alternative="固定权重也能部分解决",
        next_cheap_check="小拓扑 pilot", new_evidence=new_evidence, source_run=source_run,
    )


def test_added_then_merged_without_new_evidence(tmp_path):
    pool = make_pool(tmp_path)
    r1 = pool.add(card("学习型偏离开关", "何时绕行学不到", "固定权重定价错误", "低负载不绕高负载绕"), "run-a")
    assert r1["outcome"] == "added"
    r2 = pool.add(card("偏离开关改名版", "何时绕行学不到", "固定权重定价错误", "低负载不绕高负载绕"), "run-b")
    assert r2["outcome"] == "merged"
    assert r2["card_id"] == r1["card_id"]          # 指向存留卡
    rows = pool.read_all()
    assert len(rows) == 1                           # 只添不改：没有第二行
    assert rows[0].status == "open"


def test_same_key_with_new_evidence_reopens(tmp_path):
    pool = make_pool(tmp_path)
    r1 = pool.add(card("学习型偏离开关", "何时绕行学不到", "固定权重定价错误", "低负载不绕高负载绕"), "run-a")
    r2 = pool.add(card(
        "学习型偏离开关", "何时绕行学不到", "固定权重定价错误", "低负载不绕高负载绕",
        new_evidence="run-b 新读到 GraphPR 原文 Eq.8：绕行定价确为常数比，且给出敏感性缺失", source_run="run-b",
    ), "run-b")
    assert r2["outcome"] == "reopened"
    assert r2["revisit_of"] == r1["card_id"]
    rows = pool.read_all()
    assert len(rows) == 2
    assert rows[1].merged_into == r1["card_id"]
    assert all(r.status == "open" for r in rows)


def test_different_key_adds(tmp_path):
    pool = make_pool(tmp_path)
    pool.add(card("A 线", "困难1", "原因1", "决策变化1"), "run-a")
    r = pool.add(card("B 线", "困难2", "原因2", "决策变化2"), "run-a")
    assert r["outcome"] == "added"
    assert len(pool.read_all()) == 2


def test_render_and_list_open(tmp_path):
    pool = make_pool(tmp_path)
    r = pool.add(card("甲线", "d", "c", "s"), "run-a")
    md = (tmp_path / "candidates" / "cards" / (r["card_id"] + ".md")).read_text(encoding="utf-8")
    assert "## 原因假设" in md and "c" in md
    pool.update_elo(r["card_id"], 1300)
    open_cards = pool.list_open()
    assert open_cards[0].elo == 1300
    assert open_cards[0].card_id == r["card_id"]


def test_merge_key_ignores_punctuation_and_case(tmp_path):
    a = card("t", "何时 绕行，学不到！", "固定权重……定价错误", "低负载不绕高负载绕")
    b = card("t", "何时绕行学不到", "固定权重定价错误", "低负载不绕高负载绕")
    assert merge_key(a) == merge_key(b)