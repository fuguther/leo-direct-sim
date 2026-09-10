# -*- coding: utf-8 -*-
"""应用器测试：move/split/幂等/未命中跳过。"""
import json
import os

from scripts.topic_harness.apply_note_patches import apply_proposal, load_state, save_state


def make_env(tmp_path):
    raw = tmp_path / "raw"; raw.mkdir()
    prop = tmp_path / "proposals"; prop.mkdir()
    note = raw / "N-1.md"
    note.write_text("论文事实A。与我们对账：我们的空白很多。论文事实B。", encoding="utf-8")
    p1 = prop / "N-1.md.json"
    p1.write_text(json.dumps({
        "file": str(note),
        "segments": [
            {"quote": "与我们对账：我们的空白很多。", "op": "move-to-annex", "class": "PROJECT", "reason": "r"},
            {"quote": "不存在的句子", "op": "move-to-annex", "class": "PROJECT", "reason": "r"},
        ]}, ensure_ascii=False), encoding="utf-8")
    annex = tmp_path / "annex.md"
    state = tmp_path / "state.json"
    return str(note), str(p1), str(annex), str(state)


def test_move_and_skip_miss(tmp_path):
    note, p1, annex, state = make_env(tmp_path)
    lines, report, done = [], [], load_state(state)
    apply_proposal(p1, "t1", os.path.dirname(note) + "/", lines, done, report)
    s = open(note, encoding="utf-8").read()
    assert s == "论文事实A。论文事实B。"
    assert any(r.startswith("OK") for r in report)
    assert any(r.startswith("SKIP") for r in report)


def test_idempotent(tmp_path):
    note, p1, annex, state = make_env(tmp_path)
    done = set()
    lines, report = [], []
    apply_proposal(p1, "t1", os.path.dirname(note) + "/", lines, done, report)
    save_state(state, done)
    done2 = load_state(state)
    lines2, report2 = [], []
    apply_proposal(p1, "t1", os.path.dirname(note) + "/", lines2, done2, report2)
    assert not any(r.startswith("OK") for r in report2), report2


def test_split_requires_replacement(tmp_path):
    raw = tmp_path / "raw2"; raw.mkdir()
    prop = tmp_path / "proposals2"; prop.mkdir()
    note = raw / "N-2.md"
    note.write_text("前半事实，后半是我们的判断。", encoding="utf-8")
    p = prop / "N-2.md.json"
    p.write_text(json.dumps({"file": str(note), "segments": [
        {"quote": "前半事实，后半是我们的判断。", "op": "split", "class": "PROJECT", "replacement": "前半事实。"}
    ]}, ensure_ascii=False), encoding="utf-8")
    lines, report, done = [], [], set()
    apply_proposal(str(p), "t2", str(raw) + "/", lines, done, report)
    assert open(note, encoding="utf-8").read() == "前半事实。"
    assert any(r.startswith("OK") for r in report)