#!/usr/bin/env python3
"""候选问题池（选题 harness 第三层）：只添不改、新者重赛、按原因合并。

设计来源（详见 GROUP-MEETINGS-LOCAL/90-RAW-INBOX/RESEARCH-HARNESS-BORROWING-20260910.md）：
- Co-Scientist: Evolution 只生成新假设、绝不改旧假设，新者重新参赛。
- run-20260910 内容裁决: 重现必须带来新的实质依据，不能靠改名重新排第一。
- 合并键 = (困难, 原因, 决策变化)，不是题目名称。

数据区: out/research-ops/candidates/（gitignored，RESEARCH-OPS.md 合同指定 out/research-ops/ 为研究数据区）。
ledger.csv 是唯一索引（只追加）；cards/<card_id>.md 是给人看渲染，不参与逻辑。
"""
from __future__ import annotations

import csv
import hashlib
import os
import re
import time
from dataclasses import dataclass

CARD_FIELDS = (
    "card_id", "title", "conditions", "difficulty", "cause_hypothesis",
    "possible_change", "strongest_alternative", "decision_shift",
    "next_cheap_check", "new_evidence", "status", "merged_into",
    "elo", "created_at", "source_run",
)
MERGE_FIELDS = ("difficulty", "cause_hypothesis", "decision_shift")
LEDGER_HEADER = list(CARD_FIELDS)

_STRIP = re.compile(r"[^\w]+")


def _norm(text: str) -> str:
    """合并键归一化：小写、去空白与标点、截断。"""
    text = (text or "").lower()
    return _STRIP.sub("", text)[:240]


def merge_key(card: "CandidateCard") -> tuple:
    """按原因合并的键：困难 + 原因假设 + 决策变化。"""
    return tuple(_norm(getattr(card, f)) for f in MERGE_FIELDS)


def new_card_id(title: str, when: float | None = None) -> str:
    when = time.time() if when is None else when
    digest = hashlib.sha256((title + str(when)).encode("utf-8")).hexdigest()[:10]
    slug = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]+", "-", (title or ""))[:24].strip("-") or "card"
    return slug + "-" + digest


@dataclass
class CandidateCard:
    card_id: str
    title: str
    conditions: str = ""            # 重要条件：该困难在什么条件下成立
    difficulty: str = ""            # 具体困难：现有方法做不到什么（可观察）
    cause_hypothesis: str = ""      # 原因假设：为什么做不到（可攻击）
    possible_change: str = ""       # 可能改动：针对原因的最小改动
    strongest_alternative: str = "" # 最强替代：简单方法/成熟 RL 能解决多少
    decision_shift: str = ""        # 决策变化：若成立，谁在什么决策上改变什么
    next_cheap_check: str = ""      # 下一项廉价核验
    new_evidence: str = ""          # 重现时必须携带的新实质依据
    status: str = "open"            # open | merged | closed
    merged_into: str = ""           # merged 时指向存留卡；reopened 时指向旧卡
    elo: int = 1200
    created_at: str = ""
    source_run: str = ""

    def to_row(self) -> dict:
        return {k: str(getattr(self, k)) for k in CARD_FIELDS}

    @classmethod
    def from_row(cls, row: dict) -> "CandidateCard":
        kwargs = {k: (row.get(k) or "") for k in CARD_FIELDS}
        kwargs["elo"] = int(float(kwargs.get("elo") or 1200))
        return cls(**kwargs)


class CandidatePool:
    def __init__(self, root: str):
        self.root = root
        self.cards_dir = os.path.join(root, "cards")
        self.ledger_path = os.path.join(root, "ledger.csv")
        os.makedirs(self.cards_dir, exist_ok=True)
        if not os.path.exists(self.ledger_path):
            with open(self.ledger_path, "w", newline="", encoding="utf-8") as f:
                csv.DictWriter(f, fieldnames=LEDGER_HEADER).writeheader()

    # ---------- IO ----------
    def read_all(self) -> list:
        with open(self.ledger_path, newline="", encoding="utf-8") as f:
            return [CandidateCard.from_row(r) for r in csv.DictReader(f)]

    def _append(self, card: CandidateCard) -> None:
        with open(self.ledger_path, "a", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=LEDGER_HEADER).writerow(card.to_row())
        self._render(card)

    def _render(self, card: CandidateCard) -> None:
        path = os.path.join(self.cards_dir, card.card_id + ".md")
        lines = [
            "# " + card.title,
            "",
            "- card_id: " + card.card_id,
            "- status: " + card.status + ("" if not card.merged_into else " (rel: " + card.merged_into + ")"),
            "- elo: " + str(card.elo) + " | created: " + card.created_at + " | run: " + card.source_run,
            "",
            "## 重要条件", card.conditions or "（未填）", "",
            "## 具体困难", card.difficulty or "（未填）", "",
            "## 原因假设", card.cause_hypothesis or "（未填）", "",
            "## 可能改动", card.possible_change or "（未填）", "",
            "## 最强替代", card.strongest_alternative or "（未填）", "",
            "## 决策变化", card.decision_shift or "（未填）", "",
            "## 下一项廉价核验", card.next_cheap_check or "（未填）", "",
            "## 新实质依据（重现时必填）", card.new_evidence or "（首见为空）", "",
        ]
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    # ---------- 语义 ----------
    def add(self, card: CandidateCard, source_run: str = "") -> dict:
        """入池。返回 {"outcome": added|merged|reopened, ...}。

        - 与 open 卡 merge_key 相同且无新实质依据 → merged（不落新卡，旧卡原样保留）
        - 相同但携带 new_evidence → reopened（新卡入池，merged_into 记旧卡）
        - 否则 added
        只添不改：任何情况下都不修改已存在的 ledger 行。
        """
        if source_run:
            card.source_run = source_run
        if not card.created_at:
            card.created_at = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        if not card.card_id:
            card.card_id = new_card_id(card.title)
        for existing in self.read_all():
            if existing.status != "open":
                continue
            if merge_key(existing) == merge_key(card):
                if _norm(card.new_evidence):
                    card.status = "open"
                    card.merged_into = existing.card_id
                    self._append(card)
                    return {"outcome": "reopened", "card_id": card.card_id,
                            "revisit_of": existing.card_id}
                return {"outcome": "merged", "card_id": existing.card_id,
                        "merged_into": existing.card_id}
        card.status = "open"
        self._append(card)
        return {"outcome": "added", "card_id": card.card_id}

    def list_open(self) -> list:
        cards = [c for c in self.read_all() if c.status == "open"]
        return sorted(cards, key=lambda c: -c.elo)

    def update_elo(self, card_id: str, new_elo: int) -> None:
        """锦标赛结算后回写 Elo。追加一行新状态（append-only），旧行保留。"""
        rows = self.read_all()
        target = None
        for c in rows:
            if c.card_id == card_id and c.status == "open":
                target = c
        if target is None:
            raise KeyError("no open card: " + card_id)
        new = CandidateCard(**{**target.__dict__, "elo": int(new_elo)})
        self._append(new)
