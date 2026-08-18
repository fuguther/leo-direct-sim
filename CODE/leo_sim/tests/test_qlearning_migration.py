"""Tabular Q-learning migration tests (legacy M1 QLearning -> V2 contract).

Legacy reference: class QLearning, SimulationRL.py:5682. The legacy module
cannot be imported here (module-level TensorFlow import), so golden values
are recomputed from the cited formulas with plain math/numpy:

- init: qTable = np.random.rand(...) per (state, action) — 5703-5704;
- non-terminal update: Q <- (1-alpha)*Q + alpha*(r + gamma*maxQ(s')) —
  5791-5794 (alpha=0.25 at :558, gamma=0.99 at :274);
- terminal: Q(s,a) is written DIRECTLY with the arrive reward — 5743;
- explore: uniform among available directions; exploit: argmax with
  unavailable directions excluded — 5758-5769.
"""
from __future__ import annotations

import hashlib
import json
import math

import numpy as np
import pytest

from CODE.leo_sim import config, kernel, learning, receipt, trace
from CODE.leo_sim.tests.helpers import StaticGeometry, cell, cell_center, make_cfg, row

ALPHA = 0.25   # legacy alpha, SimulationRL.py:558
GAMMA = 0.99   # legacy gamma, SimulationRL.py:274
A = cell(0.0, 0.0)
B = cell(0.0, 10.0)
AC = cell_center(A)
BC = cell_center(B)

FULL_MASK = {a: True for a in learning.ACTIONS}


def _learner(mode="train", contract="C3", **cfg_over):
    cfg = config.resolve_config({
        "routing": {"learning_enabled": True, "policy": "hop"},
        "learning": {"algorithm": "qlearning", "mode": mode, **cfg_over},
    })
    return learning.TabularQLearning(contract, cfg["config"]["learning"], seed=7)


def test_update_rule_golden():
    """Golden: Q <- (1-a)Q + a*(r + g*maxQ(s')), SimulationRL.py:5791-5794."""
    ql = _learner()
    s1 = np.array([0.1, 0.2, 0.3, 0.4])
    s2 = np.array([0.5, 0.6, 0.7, 0.8])
    ql.table[ql._key(s1)] = np.array([0.5, 0.6, 0.7, 0.8, 0.9])
    ql.table[ql._key(s2)] = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    ql.remember(s1, "N", 2.0, s2, FULL_MASK, False)
    # "N" is ACTIONS[1]; old Q = 0.6
    expected = (1 - ALPHA) * 0.6 + ALPHA * (2.0 + GAMMA * 5.0)
    assert ql.table[ql._key(s1)][1] == pytest.approx(expected, rel=1e-15)
    assert ql.train_steps == 1 and ql.transitions == 1


def test_terminal_writes_reward_directly():
    """Golden: terminal Q(s,a) = reward (no EMA, no bootstrap),
    SimulationRL.py:5743."""
    ql = _learner()
    s1 = np.zeros(4)
    ql.table[ql._key(s1)] = np.array([0.5, 0.6, 0.7, 0.8, 0.9])
    ql.remember(s1, "deliver", 50.0, np.ones(4), FULL_MASK, True)
    assert ql.table[ql._key(s1)][0] == 50.0


def test_bootstrap_maxes_over_legal_next_only():
    """maxQ(s') is over legal actions (legacy masks unavailable to -inf,
    5765-5769 -> argmax over legal set)."""
    ql = _learner()
    s1 = np.zeros(4)
    s2 = np.ones(4)
    ql.table[ql._key(s1)] = np.zeros(5)
    ql.table[ql._key(s2)] = np.array([100.0, 1.0, 1.0, 1.0, 1.0])
    mask = {a: a != "deliver" for a in learning.ACTIONS}
    ql.remember(s1, "E", 0.0, s2, mask, False)
    expected = (1 - ALPHA) * 0.0 + ALPHA * (0.0 + GAMMA * 1.0)
    assert ql.table[ql._key(s1)][3] == pytest.approx(expected, rel=1e-15)


def test_fresh_rows_init_uniform_0_1():
    """Golden: fresh Q values are uniform [0,1), SimulationRL.py:5703-5704."""
    ql = _learner()
    row = ql._row(np.zeros(8))
    assert np.all(row >= 0.0) and np.all(row < 1.0)


def test_exploit_picks_best_legal_and_explore_stays_legal():
    row = np.array([9.0, 0.1, 0.2, 0.3, 0.4])  # deliver best but illegal
    s = np.zeros(4)
    mask = {a: a in ("N", "E") for a in learning.ACTIONS}
    ql_force = _learner(epsilon_start=0.0, epsilon_end=0.0)
    ql_force.table[ql_force._key(s)] = row
    assert ql_force.choose(s, mask, 0.0) == "E"
    ql_explore = _learner(epsilon_start=1.0, epsilon_end=1.0)
    for _ in range(20):
        assert ql_explore.choose(s, mask, 0.0) in ("N", "E")


def test_eval_mode_does_not_update_table(tmp_path):
    train = _learner()
    train.remember(np.zeros(4), "E", 1.5, np.ones(4), FULL_MASK, False)
    meta = train.save_and_verify(tmp_path)
    table_path = tmp_path / "q_table.json"
    # eval requires a pinned checkpoint (config contract)
    ql = _learner(mode="eval", checkpoint_path=str(table_path),
                  checkpoint_sha256=meta["checkpoint_sha256"])
    before = {k: v.copy() for k, v in ql.table.items()}
    s = np.zeros(4)
    ql.remember(s, "E", 50.0, np.ones(4), FULL_MASK, True)
    assert ql.table[ql._key(s)][3] == before[ql._key(s)][3]
    assert ql.train_steps == 0 and ql.transitions == 1


def test_eval_mode_does_not_consume_rng_or_mutate_table():
    """Eval mode must evaluate a fixed policy: no epsilon roll per decision,
    and unseen states get a deterministic zero row (first legal action)
    instead of a random-init row inserted into the table."""
    cfg = {"mode": "eval", "gamma": 0.99}
    q = learning.TabularQLearning("C3", cfg, seed=7)
    obs = np.zeros(learning.CONTRACT_DIMS["C3"])
    mask = {"deliver": False, "N": True, "S": False, "E": True, "W": False}
    state_before = q.rng.bit_generator.state
    action = q.choose(obs, mask, 1.0)
    state_after = q.rng.bit_generator.state
    assert q.table == {}  # unseen state must not be written into the table
    assert state_after == state_before  # no RNG consumed
    assert action == "N"  # deterministic: first legal action on a zero row


def test_save_load_roundtrip_verified(tmp_path):
    ql = _learner()
    ql.remember(np.zeros(4), "E", 1.5, np.ones(4), FULL_MASK, False)
    meta = ql.save_and_verify(tmp_path)
    assert meta["checkpoint_verified"] is True
    table_path = tmp_path / "q_table.json"
    sha = hashlib.sha256(table_path.read_bytes()).hexdigest()
    assert meta["checkpoint_sha256"] == sha
    ql2 = _learner(mode="eval", checkpoint_path=str(table_path),
                   checkpoint_sha256=sha)
    assert ql2.table.keys() == ql.table.keys()
    for key, row_vals in ql.table.items():
        assert np.array_equal(ql2.table[key], row_vals)
    with pytest.raises(learning.LearningUnavailable):
        _learner(mode="eval", checkpoint_path=str(table_path),
                 checkpoint_sha256="0" * 64)


def test_checkpoint_contract_mismatch_rejected(tmp_path):
    """A checkpoint trained under one observation contract must not load
    under a different contract with the same input width (C3/C4 both have
    dimension 14 but different semantics)."""
    train = _learner(contract="C3")
    train.remember(np.zeros(4), "E", 1.5, np.ones(4), FULL_MASK, False)
    meta = train.save_and_verify(tmp_path)
    table_path = tmp_path / "q_table.json"
    with pytest.raises(learning.LearningUnavailable,
                       match="contract mismatch"):
        _learner(mode="eval", contract="C4",
                 checkpoint_path=str(table_path),
                 checkpoint_sha256=meta["checkpoint_sha256"])


def test_config_accepts_qlearning_and_validates_alpha():
    cfg = config.resolve_config({
        "routing": {"learning_enabled": True},
        "learning": {"algorithm": "qlearning"},
    })
    assert cfg["config"]["learning"]["qlearning_alpha"] == ALPHA
    for bad in (0.0, -0.1, 1.5):
        with pytest.raises(config.ConfigError):
            config.resolve_config({
                "routing": {"learning_enabled": True},
                "learning": {"algorithm": "qlearning",
                             "qlearning_alpha": bad}})


class _TwoSatGeometry(StaticGeometry):
    def subpoint(self, sat_id, t):
        return (0.0, float(sat_id), 550.0)


def _two_sat_geo():
    nb = {0: {"E": 1}, 1: {"W": 0}}
    vis = lambda s, lat, lon, t: (s == 0 and (lat, lon) == AC) or \
                                 (s == 1 and (lat, lon) == BC)
    return _TwoSatGeometry(2, neighbors_map=nb, visible=vis)


def test_kernel_end_to_end_qlearning_without_tensorflow(tmp_path):
    """Full kernel run with the real tabular learner (no TF), incl. receipt."""
    cfg = make_cfg({
        "endpoints": {"sites": [
            {"name": "a", "lat": 0.0, "lon": 0.0},
            {"name": "b", "lat": 0.0, "lon": 10.0},
        ]},
        "control_plane": {"enabled": True},
        "routing": {"policy": "hop", "learning_enabled": True},
        "learning": {"algorithm": "qlearning"},
    })
    tdir = tmp_path / "compiled"
    manifest = trace.compile_trace(cfg, str(tdir))
    tbytes = (tdir / "trace.csv").read_bytes()
    manifest["__trace_sha256"] = hashlib.sha256(tbytes).hexdigest()
    manifest["__sha256"] = hashlib.sha256(
        (tdir / "manifest.json").read_bytes()).hexdigest()
    rows = trace.load_trace(
        str(tdir / "trace.csv"),
        horizon_s=cfg["config"]["scenario"]["duration_s"],
        max_packets=cfg["config"]["execution"]["max_packets"])
    assert rows, "compiled trace must contain packets for this scenario"
    out = tmp_path / "run"
    result = kernel.run_simulation(cfg, rows, geometry=_two_sat_geo(),
                                   learning_out_dir=out / "qlearning")
    assert result["natural_end"] is True
    lr = result["learning"]
    assert lr["algorithm"] == "qlearning"
    assert lr["decisions"] > 0 and lr["table_size"] > 0
    assert lr["train_steps"] == lr["transitions"]
    assert lr["checkpoint_verified"] is True
    # receipt chain: write + verify with the qlearning artifact
    receipt.write_run(str(out), cfg, tbytes, manifest, result, rows)
    assert receipt.verify_receipt_dir(str(out)) == []


def _legacy_v1_table(path, contract="C3", with_metadata=True):
    """Write a legacy v1 q_table.json (no contract field) plus the sibling
    metadata.json that old save_and_verify produced."""
    payload = {"schema": "leo-sim-qlearning-table/v1",
               "entries": [["00" * 16, [0.1] * len(learning.ACTIONS)]]}
    table = path / "q_table.json"
    table.write_text(json.dumps(payload, sort_keys=True) + "\n")
    sha = hashlib.sha256(table.read_bytes()).hexdigest()
    if with_metadata:
        meta = {"schema": "leo-sim-qlearning/v1", "algorithm": "qlearning",
                "contract": contract, "checkpoint": "q_table.json",
                "checkpoint_sha256": sha, "checkpoint_verified": True,
                "mode": "eval"}
        (path / "metadata.json").write_text(
            json.dumps(meta, sort_keys=True) + "\n")
    return str(table), sha


def test_legacy_v1_table_migrates_via_sibling_metadata(tmp_path):
    """A v1 table without payload contract loads when the sibling metadata
    independently binds contract+filename+SHA."""
    table_path, sha = _legacy_v1_table(tmp_path)
    q = _learner(mode="eval", contract="C3",
                 checkpoint_path=table_path, checkpoint_sha256=sha)
    assert len(q.table) == 1


def test_legacy_v1_table_rejected_without_verifiable_metadata(tmp_path):
    """No payload contract and no usable sibling metadata -> fail closed."""
    table_path, sha = _legacy_v1_table(tmp_path, with_metadata=False)
    with pytest.raises(learning.LearningUnavailable,
                       match="contract mismatch"):
        _learner(mode="eval", contract="C3",
                 checkpoint_path=table_path, checkpoint_sha256=sha)


def test_legacy_v1_table_rejected_on_metadata_contract_mismatch(tmp_path):
    table_path, sha = _legacy_v1_table(tmp_path, contract="C4")
    with pytest.raises(learning.LearningUnavailable,
                       match="contract mismatch"):
        _learner(mode="eval", contract="C3",
                 checkpoint_path=table_path, checkpoint_sha256=sha)


def test_metadata_verifier_fail_closed_on_every_field():
    """DDQN metadata provenance gate: any missing/mismatched field rejects."""
    good = {"schema": "leo-sim-ddqn/v1", "algorithm": "ddqn",
            "contract": "C3", "checkpoint": "online.keras",
            "checkpoint_sha256": "ab" * 32, "checkpoint_verified": True}
    assert learning._verify_checkpoint_metadata(
        good, "C3", "online.keras", "ab" * 32,
        "leo-sim-ddqn/v1", "ddqn") is None
    for mutate in (
            lambda m: m.update({"contract": "C4"}),
            lambda m: m.update({"checkpoint_sha256": "00" * 32}),
            lambda m: m.update({"checkpoint": "other.keras"}),
            lambda m: m.update({"schema": "other"}),
            lambda m: m.update({"algorithm": "qlearning"}),
            lambda m: m.update({"checkpoint_verified": False}),
            lambda m: m.pop("contract")):
        m = dict(good)
        mutate(m)
        with pytest.raises(learning.LearningUnavailable):
            learning._verify_checkpoint_metadata(
                m, "C3", "online.keras", "ab" * 32,
                "leo-sim-ddqn/v1", "ddqn")
    with pytest.raises(learning.LearningUnavailable):
        learning._verify_checkpoint_metadata(
            "not-a-dict", "C3", "online.keras", "ab" * 32,
            "leo-sim-ddqn/v1", "ddqn")

