"""Integration tests for D1 distance-dependent MCS rates."""
from __future__ import annotations

import pytest

from CODE.leo_sim import config, kernel, link_budget
from CODE.leo_sim.tests.helpers import StaticGeometry, cell, cell_center, make_cfg, row

A = cell(0.0, 0.0)
B = cell(0.0, 10.0)
AC = cell_center(A)
BC = cell_center(B)


def test_module_goldens_match_characterization():
    goldens = {
        1000e3: 500e6 * 3.620536,
        2000e3: 500e6 * 1.972253,
        4000e3: 500e6 * 0.889135,
        6000e3: 0.0,
    }
    for d_m, expected in goldens.items():
        assert link_budget.mcs_rate_bps(
            d_m / 1000.0, link_budget.LEGACY_ISL_RF) == pytest.approx(
            expected, rel=1e-9), d_m


def test_graded_rf_sets_differ():
    d = 1000.0
    up = link_budget.mcs_rate_bps(d, link_budget.LEGACY_UPLINK_RF)
    down = link_budget.mcs_rate_bps(d, link_budget.LEGACY_DOWNLINK_RF)
    isl = link_budget.mcs_rate_bps(d, link_budget.LEGACY_ISL_RF)
    # pinned from the legacy RF trios (computed 2026-08-19)
    assert up == pytest.approx(2.796581e9, rel=1e-9)
    assert down == pytest.approx(1.4281155e9, rel=1e-9)
    assert isl == pytest.approx(1.810268e9, rel=1e-9)
    assert up > isl > down


def test_max_rate_range_matches_zero_rate():
    for rf in (link_budget.LEGACY_ISL_RF, link_budget.LEGACY_UPLINK_RF,
               link_budget.LEGACY_DOWNLINK_RF):
        lim = link_budget.max_rate_range_km(rf)
        assert link_budget.mcs_rate_bps(lim - 1e-3, rf) > 0
        assert link_budget.mcs_rate_bps(lim + 1e-3, rf) == 0.0


def test_config_mcs_requires_valid_rf():
    cfg = config.resolve_config({"links": {"rate_model": "mcs"}})
    assert cfg["config"]["links"]["rate_model"] == "mcs"
    with pytest.raises(config.ConfigError, match="min_rate_bps"):
        config.resolve_config({
            "links": {
                "rate_model": "mcs",
                "rf_isl": {"min_rate_bps": 5e8},
            }})
    with pytest.raises(config.ConfigError, match="rf_isl"):
        config.resolve_config({
            "links": {
                "rf_isl": {"not_a_key": 1},
            }})


class _Scripted(StaticGeometry):
    """StaticGeometry + scripted range crossing for rate recovery."""

    def __init__(self, num_satellites, *, isl_range_fn=None,
                 slant_range_fn=None, **kw):
        super().__init__(num_satellites, **kw)
        self._isl_range_fn = isl_range_fn or (lambda a, b, t: self.isl_km)
        self._slant_range_fn = slant_range_fn or (
            lambda s, lat, lon, t: self.slant_km)
        self._step = 0.01

    def isl_range_km(self, a, b, t):
        return float(self._isl_range_fn(a, b, t))

    def slant_range_km(self, s, lat, lon, t):
        return float(self._slant_range_fn(s, lat, lon, t))

    def next_isl_range_under(self, a, b, threshold, t, limit):
        prev = self.isl_range_km(a, b, t)
        x = t + self._step
        while x <= limit + 1e-12:
            v = self.isl_range_km(a, b, x)
            if v <= threshold and prev > threshold:
                return x
            prev = v
            x += self._step
        return None

    def next_slant_range_under(self, s, lat, lon, threshold, t, limit):
        prev = self.slant_range_km(s, lat, lon, t)
        x = t + self._step
        while x <= limit + 1e-12:
            v = self.slant_range_km(s, lat, lon, x)
            if v <= threshold and prev > threshold:
                return x
            prev = v
            x += self._step
        return None


def test_mcs_service_waits_for_rate_recovery_then_delivers():
    topo = {0: {"E": 1}, 1: {"W": 0}}

    def ranges(a, b, t):
        return 5900.0 if t < 1.0 else 1000.0

    geo = _Scripted(
        2, neighbors_map=topo, isl_range_fn=ranges,
        visible=lambda s, lat, lon, t: (
            (s == 0 and (lat, lon) == AC)
            or (s == 1 and (lat, lon) == BC)),
        slant_km=600.0)
    cfg = make_cfg({
        "scenario": {"duration_s": 2.0},
        "links": {"rate_model": "mcs", "isl_rate_mbps": 1000.0},
    })
    res = kernel.run_simulation(cfg, [row(1, 0.0, A, B)], geometry=geo)
    assert res["fates"][1] == "DELIVERED"
    assert res["mechanisms"]["effective"]["mcs"] is True
    assert res["mechanism_counters"]["mcs_rate_samples"] > 0


def test_mcs_zero_rate_waits_then_expires_at_deadline():
    topo = {0: {"E": 1}, 1: {"W": 0}}
    geo = _Scripted(
        2, neighbors_map=topo,
        isl_range_fn=lambda a, b, t: 5900.0,
        visible=lambda s, lat, lon, t: (
            (s == 0 and (lat, lon) == AC)
            or (s == 1 and (lat, lon) == BC)))
    cfg = make_cfg({
        "scenario": {"duration_s": 2.0},
        "links": {"rate_model": "mcs"},
    })
    res = kernel.run_simulation(
        cfg, [row(1, 0.0, A, B, deadline=1.0)], geometry=geo)
    assert res["fates"][1] == "DATA_DEADLINE_EXPIRED"
    # the ISL service never started: zero-rate gate held until the deadline
    assert res["occupied"]["isl_s"] == 0.0
    assert res["mechanism_counters"]["mcs_rate_samples"] > 0


def test_constant_rate_default_is_unaffected():
    topo = {0: {"E": 1}, 1: {"W": 0}}
    geo = _Scripted(
        2, neighbors_map=topo,
        isl_range_fn=lambda a, b, t: 5900.0,
        visible=lambda s, lat, lon, t: (
            (s == 0 and (lat, lon) == AC)
            or (s == 1 and (lat, lon) == BC)))
    cfg = make_cfg({"scenario": {"duration_s": 2.0}})
    res = kernel.run_simulation(cfg, [row(1, 0.0, A, B)], geometry=geo)
    assert res["fates"][1] == "DELIVERED"
    assert res["mechanisms"]["effective"]["mcs"] is False
