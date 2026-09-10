#!/usr/bin/env python3
"""两两配对 Elo 排名（薄实现，无三方依赖）。

Co-Scientist 思想：相对判断对便宜模型更可靠；高名次对多轮辩论、低名次单轮；
配对优先相似假设（省算力、比赛更尖锐）。同对最多复赛两次防刷分。
评分本身由外部进行（LLM 配对裁决或可执行检查），本模块只管调度与积分。
"""
from __future__ import annotations


class Elo:
    def __init__(self, k: float = 24.0, base: float = 1200.0):
        self.k = k
        self.base = base

    def expected(self, ra: float, rb: float) -> float:
        return 1.0 / (1.0 + 10 ** ((rb - ra) / 400.0))

    def apply(self, ra: float, rb: float, score_a: float) -> tuple:
        """score_a: 1 a 胜 / 0.5 平 / 0 b 胜。返回 (new_a, new_b)。"""
        if score_a not in (0.0, 0.5, 1.0):
            raise ValueError("score_a must be 0 / 0.5 / 1")
        ea = self.expected(ra, rb)
        na = ra + self.k * (score_a - ea)
        nb = rb + self.k * ((1.0 - score_a) - (1.0 - ea))
        return na, nb


def _pair_key(a: str, b: str) -> tuple:
    return (a, b) if a <= b else (b, a)


def schedule(ids_elos: list, similarity, top_rounds: int = 3, bottom_rounds: int = 1,
             max_remach: int = 2) -> list:
    """生成两两配对计划。

    ids_elos: [(id, elo), ...]；similarity(id_a, id_b) -> float 越高越像。
    高名次前一半各赛 top_rounds 轮（优先相似对手），后一半各赛 bottom_rounds 轮。
    同一对最多 max_remach 次。返回 [(id_a, id_b), ...]，确定性输出（不引入随机）。
    """
    items = sorted(ids_elos, key=lambda t: (-t[1], t[0]))
    n = len(items)
    if n < 2:
        return []
    top_n = max(1, n // 2)
    top, bottom = items[:top_n], items[top_n:]
    used: dict = {}

    def pick(anchor: str):
        best, best_sim = None, -1.0
        for cand, _ in items:
            if cand == anchor:
                continue
            key = _pair_key(anchor, cand)
            if used.get(key, 0) >= max_remach:
                continue
            sim = float(similarity(anchor, cand))
            if sim > best_sim:
                best, best_sim = cand, sim
        return best

    pairs: list = []
    for anchor, _ in top:
        for _ in range(top_rounds):
            partner = pick(anchor)
            if partner is None:
                break
            key = _pair_key(anchor, partner)
            used[key] = used.get(key, 0) + 1
            pairs.append((anchor, partner))
    for anchor, _ in bottom:
        partner = pick(anchor)
        if partner is not None:
            key = _pair_key(anchor, partner)
            used[key] = used.get(key, 0) + 1
            pairs.append((anchor, partner))
    return pairs
