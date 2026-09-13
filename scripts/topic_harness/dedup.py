# -*- coding: utf-8 -*-
"""LEO 选题卡去重适配器（vendor AI-Researcher 的 LEO 化封装）。

上游算法参照（vendor/ai_researcher/ai_researcher/src/，逐字节原样保留）：
  - dedup_ideas.py：all-MiniLM-L6-v2 嵌入 + 相似度矩阵，默认阈值 0.8，贪心保留先出现者；
  - analyze_ideas_semantic_similarity.py：嵌入余弦相似度矩阵的构造方式。

vendor 原文件顶层 import nltk/sentence_transformers，非本 harness 强制依赖（且 harness
纪律为 std-lib only）。本适配器：
  - sentence-transformers 可用 → embed_cards() 返回 all-MiniLM-L6-v2 归一化嵌入，
    余弦相似度，阈值 EMBED_THRESHOLD=0.8（对齐上游 --similarity_threshold 默认 0.8）；
  - 不可用（或 LEO_DEDUP_BACKEND=dice 强制）→ 退化为字符 bigram Dice 相似度（纯 stdlib），
    阈值 DICE_THRESHOLD=0.6（Dice 系数分布整体低于嵌入余弦，单独定标，两阈值不混用）。
模型懒加载：首次用到才 SentenceTransformer(MODEL_NAME)，离线/测试路径零下载。

合并建议语义（对齐上游 dedup_ideas.__main__ 的过滤循环）：按输入顺序贪心扫描，
保留先出现者，丢弃与其相似度 > 阈值 的后续卡片（严格大于，同上游）。
"""
import os
import string

MODEL_NAME = "all-MiniLM-L6-v2"
EMBED_THRESHOLD = 0.8  # 嵌入余弦阈值（上游 dedup_ideas 默认 similarity_threshold=0.8）
DICE_THRESHOLD = 0.6   # 字符 bigram Dice 阈值（退化路径单独定标）

_PUNCT_TABLE = str.maketrans("", "", string.punctuation)

# 卡片字段优先级：CandidateCard（scripts/topic_harness/pool.py）字段 + 常见 dict 卡片字段
_CARD_KEYS = (
    "title", "name", "idea_name", "conditions", "description", "summary",
    "difficulty", "cause_hypothesis", "possible_change", "strongest_alternative",
    "method", "text", "abstract",
)


def card_text(card):
    """选题卡 → 去重/查新用的文本。接受 str、dict 或带属性的卡对象（如 CandidateCard）。"""
    if isinstance(card, str):
        return card.strip()
    parts = []
    for key in _CARD_KEYS:
        val = card.get(key) if isinstance(card, dict) else getattr(card, key, None)
        if val:
            parts.append(str(val))
    return " ".join(parts).strip()


# --------------------------------------------------------- Dice 回退路径 ----

def _norm_text(text):
    """小写 + 去标点（对齐上游 process_text 的规范化前两步；不依赖 nltk 停用词）。"""
    return str(text).lower().translate(_PUNCT_TABLE)


def bigrams(text):
    """字符 bigram 集合；规范化后长度 <2 时退化为整串集合。"""
    norm = " ".join(_norm_text(text).split())
    if len(norm) < 2:
        return {norm} if norm else set()
    return {norm[i:i + 2] for i in range(len(norm) - 1)}


def dice_similarity(a, b):
    """Dice 系数 = 2|A∩B| / (|A|+|B|)。空串对返回 0.0。"""
    set_a, set_b = bigrams(a), bigrams(b)
    if not set_a or not set_b:
        return 0.0
    return 2.0 * len(set_a & set_b) / (len(set_a) + len(set_b))


def _dice_matrix(texts):
    """纯 stdlib 两两 Dice 矩阵（list[list[float]]，含对角 1.0）。"""
    gram_sets = [bigrams(t) for t in texts]
    n = len(texts)
    matrix = [[1.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            sa, sb = gram_sets[i], gram_sets[j]
            sim = 2.0 * len(sa & sb) / (len(sa) + len(sb)) if sa and sb else 0.0
            matrix[i][j] = matrix[j][i] = sim
    return matrix


# ------------------------------------------------------- 嵌入路径（懒加载） ----

_MODEL = None
_MODEL_RESOLVED = False


def _load_model():
    """懒加载 all-MiniLM-L6-v2；不可用（未安装/下载失败/被强制 dice）返回 None。

    进程内只解析一次；LEO_DEDUP_BACKEND=dice 可强制走回退路径（离线测试用）。
    """
    global _MODEL, _MODEL_RESOLVED
    if _MODEL_RESOLVED:
        return _MODEL
    _MODEL_RESOLVED = True
    if os.environ.get("LEO_DEDUP_BACKEND", "").lower() == "dice":
        return None
    try:
        from sentence_transformers import SentenceTransformer
        _MODEL = SentenceTransformer(MODEL_NAME)
    except Exception:  # 未安装 / 模型下载失败：按约定退化，不中断主流程
        _MODEL = None
    return _MODEL


def embed_cards(texts, model=None):
    """嵌入一批文本。

    返回 np.ndarray (n, d)（sentence-transformers 可用）；不可用返回 None，
    调用方（similarity_matrix/dedup）据此自动退化为字符 bigram Dice。
    """
    model = model if model is not None else _load_model()
    if model is None:
        return None
    embeddings = model.encode(list(texts))
    import numpy as np
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    return embeddings / np.maximum(norms, 1e-12)  # 归一化后内积即余弦（同上游 model.similarity）


def similarity_matrix(texts):
    """相似度矩阵 + (backend, threshold)。backend ∈ {"embed", "dice"}。"""
    embeddings = embed_cards(texts)
    if embeddings is not None:
        import numpy as np
        return np.asarray(embeddings @ embeddings.T), "embed", EMBED_THRESHOLD
    return _dice_matrix(texts), "dice", DICE_THRESHOLD


def active_backend():
    """当前将使用的后端名（供诊断；触发懒加载）。"""
    return "embed" if _load_model() is not None else "dice"


# ------------------------------------------------------------- 主入口 ----

def dedup(cards, threshold=None):
    """返回合并建议（贪心首现保留，相似度严格大于阈值才合并，同上游）。

    cards: str / dict / 卡对象列表；threshold 缺省按后端取 EMBED_THRESHOLD/DICE_THRESHOLD。
    返回 list[dict]：{keep_index, keep, drop: [{index, card, similarity}], backend, threshold}。
    """
    texts = [card_text(c) for c in cards]
    matrix, backend, default_threshold = similarity_matrix(texts)
    if threshold is None:
        threshold = default_threshold
    dropped, suggestions = set(), []
    for i in range(len(texts)):
        if i in dropped:
            continue
        drops = []
        for j in range(i + 1, len(texts)):
            if j in dropped:
                continue
            sim = float(matrix[i][j])
            if sim > threshold:
                drops.append({"index": j, "card": cards[j], "similarity": round(sim, 6)})
                dropped.add(j)
        if drops:
            suggestions.append({
                "keep_index": i, "keep": cards[i], "drop": drops,
                "backend": backend, "threshold": threshold,
            })
    return suggestions
