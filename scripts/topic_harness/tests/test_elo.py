# -*- coding: utf-8 -*-
"""Elo 调度测试：期望对称、胜负更新、相似优先、轮数预算、复赛上限。"""
from scripts.topic_harness.elo import Elo, schedule


def test_expected_symmetric():
    e = Elo()
    assert abs(e.expected(1200, 1200) - 0.5) < 1e-9
    assert abs(e.expected(1300, 1200) + e.expected(1200, 1300) - 1.0) < 1e-9
    assert e.expected(1400, 1000) > 0.9


def test_winner_gains_loser_loses():
    e = Elo()
    na, nb = e.apply(1200, 1200, 1.0)
    assert na > 1200 > nb
    na2, nb2 = e.apply(na, nb, 0.0)
    assert na2 < na and nb2 > nb


def test_invalid_score_rejected():
    import pytest
    with pytest.raises(ValueError):
        Elo().apply(1200, 1200, 0.7)


def shared_prefix(a, b):
    n = 0
    for x, y in zip(a, b):
        if x != y:
            break
        n += 1
    return float(n)


def test_similar_first_pairing():
    ids_elos = [("A1", 1300), ("A2-similar", 1250), ("B1", 1200), ("B2", 1150), ("C1", 1100), ("C2", 1050)]
    pairs = schedule(ids_elos, shared_prefix)
    assert pairs, "should produce pairs"
    first = pairs[0]
    # A1 的第一个对手必须是相似度最高的 A2-similar
    assert first == ("A1", "A2-similar")


def test_round_budget_and_remach_cap():
    ids_elos = [("a", 1300), ("b", 1250), ("c", 1200), ("d", 1150)]
    sim = lambda x, y: 1.0  # 全部同样像 → 只能靠复赛上限约束
    pairs = schedule(ids_elos, sim, top_rounds=3, bottom_rounds=1, max_remach=2)
    from collections import Counter
    cnt = Counter(tuple(sorted(p)) for p in pairs)
    assert max(cnt.values()) <= 2
    assert len(pairs) >= 2


def test_too_few_items():
    assert schedule([("only", 1200)], shared_prefix) == []
