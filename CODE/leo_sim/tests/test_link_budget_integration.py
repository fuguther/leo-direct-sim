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


def test_mcs_zero_rate_head_does_not_bypass_endpoint_fifo():
    topo = {0: {"E": 1}, 1: {"W": 0}}
    geo = _Scripted(
        2, neighbors_map=topo,
        isl_range_fn=lambda a, b, t: 5900.0 if t < 1.0 else 1000.0,
        visible=lambda s, lat, lon, t: (
            (s == 0 and (lat, lon) == AC)
            or (s == 1 and (lat, lon) == BC)))
    cfg = make_cfg({
        "scenario": {"duration_s": 2.0},
        "links": {"rate_model": "mcs"},
    })
    res = kernel.run_simulation(
        cfg, [row(1, 0.0, A, B, bits=1_000_000),
              row(2, 0.0, A, B, bits=1_000_000)], geometry=geo)
    assert res["fates"][1] == "DELIVERED"
    assert res["fates"][2] == "DELIVERED"
    assert [pid for _cell, pid in res["service_log"]["uplink"]] == [1, 2]


def test_mcs_zero_rate_isl_head_stays_queued_until_recovery():
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
    k = kernel.Kernel(cfg, [], geometry=geo)
    pkt = kernel.DataPacket(1, A, B, 1_000_000, None, 0.0)
    link = k.isls[0]["E"]
    link.put_data(pkt)

    # Let the ISL server attempt its first scheduling step.  A zero MCS
    # rate is not a service start and must not dequeue/head-of-line block the
    # packet while waiting for rate recovery.
    for _ in range(6):
        k.env.step()
    assert link.data_q and link.data_q[0] is pkt
    assert link.data_bits == pkt.bits
    assert link._svc is None


def test_mcs_gsl_down_does_not_dequeue_shared_uplink_head():
    """A GSL outage must not pin the shared server on a dequeued packet."""
    geo = _Scripted(
        2, neighbors_map={0: {"E": 1}, 1: {"W": 0}},
        visible=lambda s, lat, lon, t: t >= 1.0 and (
            (s == 0 and (lat, lon) == AC)
            or (s == 1 and (lat, lon) == BC)),
        slant_km=600.0)
    cfg = make_cfg({
        "scenario": {"duration_s": 2.0},
        "access": {"acquisition_delay_s": 0.0},
        "links": {"rate_model": "mcs"},
    })
    k = kernel.Kernel(cfg, [row(99, 2.0, A, B)], geometry=geo)
    ep = k.endpoints[A]
    pkt = kernel.DataPacket(1, A, B, 1_000_000, None, 0.0)
    ep.queue.append(pkt)
    ep.queued_bits += pkt.bits
    ep.area.add(pkt.bits, k.env.now)
    k._poke(k.uplinks[0].wake)
    k.env.step()
    assert [p.pid for p in ep.queue] == [1]
    assert ep.queued_bits > 0
    assert k.uplinks[0].current is None


def test_mcs_gsl_ge_down_does_not_dequeue_shared_downlink_head():
    """A GSL GE outage must be handled before downlink dequeue as well."""
    geo = _Scripted(
        2, neighbors_map={0: {"E": 1}, 1: {"W": 0}},
        visible=lambda s, lat, lon, t: True,
        slant_km=600.0)
    cfg = make_cfg({
        "scenario": {"duration_s": 2.0},
        "access": {"acquisition_delay_s": 0.0},
        "links": {"rate_model": "mcs", "ge_enabled": True,
                   "ge_gsl": {"mean_good_s": 0.001,
                               "mean_bad_s": 1000.0}},
    })
    k = kernel.Kernel(cfg, [row(99, 2.0, A, B)], geometry=geo)
    pkt = kernel.DataPacket(1, A, B, 1_000_000, None, 0.0)
    k.downlinks[1].put(pkt)
    ge = k._gsl_ge(1, B)
    ge._bad = True
    ge._last_t = 0.0
    ge._next_flip = float("inf")
    assert k.downlinks[1]._servable(B) is None
    assert [p.pid for p in k.downlinks[1].queues[B] ] == [1]
    assert k.downlinks[1].current is None


def test_mcs_zero_rate_downlink_waits_then_delivers_after_recovery():
    """Real GSL scenario: destination visible but beyond MCS range.

    The downlink slant range starts at 5900 km (zero feasible MCS rate for
    the legacy downlink RF, max range ~4482 km) and closes to 600 km at
    t=1.0.  The packet must wait — never be failed — and only be delivered
    once a positive rate exists.
    """
    assert link_budget.mcs_rate_bps(
        5900.0, link_budget.LEGACY_DOWNLINK_RF) == 0.0

    def slant(s, lat, lon, t):
        if (lat, lon) == BC:
            return 5900.0 if t < 1.0 else 600.0
        return 600.0

    geo = _Scripted(
        1, neighbors_map={0: {}},
        visible=lambda s, lat, lon, t: (lat, lon) in (AC, BC),
        slant_range_fn=slant)
    cfg = make_cfg({
        "scenario": {"duration_s": 2.0, "num_satellites": 1},
        "links": {"rate_model": "mcs"},
    })
    res = kernel.run_simulation(cfg, [row(1, 0.0, A, B)], geometry=geo)
    assert res["fates"][1] == "DELIVERED"
    assert res["deliveries"][1]["delivered_at"] >= 1.0
    assert res["mechanism_counters"]["mcs_rate_samples"] > 0


def test_mcs_zero_rate_downlink_is_not_a_legal_deliver_action():
    """Decision-level mask: zero downlink rate must not enqueue for deliver.

    Consistent with the ISL legal mask (zero-rate directions are excluded),
    a zero-rate downlink must park the packet in ``pending`` for re-decision
    instead of putting it into a downlink queue that cannot be served.
    """
    geo = _Scripted(
        1, neighbors_map={0: {}},
        visible=lambda s, lat, lon, t: (lat, lon) in (AC, BC),
        slant_range_fn=lambda s, lat, lon, t: (
            5900.0 if (lat, lon) == BC else 600.0))
    cfg = make_cfg({
        "scenario": {"duration_s": 2.0, "num_satellites": 1},
        "links": {"rate_model": "mcs"},
    })
    k = kernel.Kernel(cfg, [row(99, 1.5, A, B)], geometry=geo)
    # let the association ticker run so B has an active link to sat 0
    for _ in range(6):
        k.env.step()
    assert k.endpoints[B].links[0].state == "active"

    pkt = kernel.DataPacket(1, A, B, 1_000_000, None, 0.0)
    k._decide(pkt, 0)
    assert k.downlinks[0].queued_bits == 0
    assert list(k.pending[0]) == [pkt]


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


def test_mcs_zero_rate_uplink_recovers_at_certified_time_not_next_tick():
    """F1: a zero-rate GSL must wake at the certified recovery instant.

    Uplink slant starts at 12500 km (beyond the uplink MCS max range of
    ~12068 km, so rate is exactly zero) and closes to 600 km at t=1.0.
    With time_step=0.7 the blind ticks land at 0.7 and 1.4; polling would
    start the service at 1.4, the certified recovery is 1.0.
    """
    assert link_budget.mcs_rate_bps(
        12500.0, link_budget.LEGACY_UPLINK_RF) == 0.0

    def slant(s, lat, lon, t):
        if (lat, lon) == AC:
            return 12500.0 if t < 1.0 else 600.0
        return 600.0

    geo = _Scripted(
        1, neighbors_map={0: {}},
        visible=lambda s, lat, lon, t: (lat, lon) in (AC, BC),
        slant_range_fn=slant)
    cfg = make_cfg({
        "scenario": {"duration_s": 2.0, "time_step_s": 0.7,
                     "num_satellites": 1},
        "links": {"rate_model": "mcs"},
    })
    res = kernel.run_simulation(cfg, [row(1, 0.0, A, B)], geometry=geo)
    assert res["fates"][1] == "DELIVERED"
    # service started at the certified recovery (1.0 + tx + prop), not at
    # the next blind tick 1.4
    assert res["deliveries"][1]["delivered_at"] < 1.2


def test_mcs_zero_rate_deadline_before_horizon_expires_not_in_system():
    """F1: a deadline between the last tick and the horizon must still expire.

    The downlink is beyond MCS range for the whole run, so the packet parks
    behind the zero-rate gate.  Its deadline (0.95) falls after the last
    ticker pass (0.9) but before the horizon (0.96): stop-close must settle
    it as DATA_DEADLINE_EXPIRED, not IN_SYSTEM_AT_STOP.
    """
    geo = _Scripted(
        1, neighbors_map={0: {}},
        visible=lambda s, lat, lon, t: (lat, lon) in (AC, BC),
        slant_range_fn=lambda s, lat, lon, t: (
            5900.0 if (lat, lon) == BC else 600.0))
    cfg = make_cfg({
        "scenario": {"duration_s": 0.96, "num_satellites": 1},
        "links": {"rate_model": "mcs"},
    })
    res = kernel.run_simulation(
        cfg, [row(1, 0.0, A, B, deadline=0.95)], geometry=geo)
    assert res["fates"][1] == "DATA_DEADLINE_EXPIRED"


def test_mcs_zero_rate_isl_wait_expires_each_packet_at_its_own_deadline():
    """F2: the ISL zero-rate wait must race wake and all queued expiries.

    p1 (no deadline) holds the zero-rate ISL probe; p2 arrives at t=0.2
    with deadline 0.5.  p2 must expire at its own deadline (queue area
    0.3e6 bit*s), not ride until the horizon (1.8e6 bit*s).
    """
    geo = _Scripted(
        2, neighbors_map={0: {"E": 1}, 1: {"W": 0}},
        isl_range_fn=lambda a, b, t: 5900.0,
        visible=lambda s, lat, lon, t: (
            (s == 0 and (lat, lon) == AC)
            or (s == 1 and (lat, lon) == BC)))
    cfg = make_cfg({
        "scenario": {"duration_s": 2.0},
        "links": {"rate_model": "mcs"},
    })
    k = kernel.Kernel(cfg, [], geometry=geo)
    p1 = kernel.DataPacket(1, A, B, 1_000_000, None, 0.0)
    k.ledger.register(p1.pid, p1.bits)
    k.isls[0]["E"].put_data(p1)
    while k.env.now < 0.2:
        k.env.step()
    p2 = kernel.DataPacket(2, A, B, 1_000_000, 0.5, 0.2)
    k.ledger.register(p2.pid, p2.bits)
    k.isls[0]["E"].put_data(p2)

    res = k.run()
    assert res["natural_end"]
    assert res["fates"][2] == "DATA_DEADLINE_EXPIRED"
    assert res["fates"][1] == "IN_SYSTEM_AT_STOP"
    # p1 waits 0->2.0 (2.0e6 bit*s); p2 waits 0.2->0.5 (0.3e6 bit*s)
    assert res["queue_area_bits_s"]["isl_data"] == pytest.approx(
        2.3e6, rel=1e-9)


def test_mcs_all_zero_rate_run_marks_mechanism_effective():
    """F5: zero-rate gating IS the MCS mechanism affecting scheduling.

    A run whose links are all beyond MCS range the whole time must report
    effective.mcs=True (packets were held by the gate) even though no
    transmission was ever paced (mcs_rate_samples == 0).
    """
    geo = _Scripted(
        1, neighbors_map={0: {}},
        visible=lambda s, lat, lon, t: (lat, lon) in (AC, BC),
        slant_range_fn=lambda s, lat, lon, t: (
            5900.0 if (lat, lon) == BC else 12500.0))
    cfg = make_cfg({
        "scenario": {"duration_s": 0.96, "num_satellites": 1},
        "links": {"rate_model": "mcs"},
    })
    res = kernel.run_simulation(
        cfg, [row(1, 0.0, A, B, deadline=0.95)], geometry=geo)
    counters = res["mechanism_counters"]
    assert counters["mcs_rate_samples"] == 0
    assert counters["mcs_zero_rate_holds"] > 0
    assert res["mechanisms"]["effective"]["mcs"] is True


def test_mcs_receipt_records_sampled_rate_range():
    """F5: sampled MCS rates are attributed with a min/max range in bps."""
    topo = {0: {"E": 1}, 1: {"W": 0}}
    geo = _Scripted(
        2, neighbors_map=topo,
        isl_range_fn=lambda a, b, t: 1000.0,
        visible=lambda s, lat, lon, t: (
            (s == 0 and (lat, lon) == AC)
            or (s == 1 and (lat, lon) == BC)),
        slant_km=600.0)
    cfg = make_cfg({
        "scenario": {"duration_s": 2.0},
        "links": {"rate_model": "mcs"},
    })
    res = kernel.run_simulation(cfg, [row(1, 0.0, A, B)], geometry=geo)
    assert res["fates"][1] == "DELIVERED"
    counters = res["mechanism_counters"]
    # samples: uplink@600km ~2.95e9, isl@1000km ~1.81e9, downlink@600 ~2.10e9
    assert 1.8e9 < counters["mcs_rate_min_bps"] < 1.82e9
    assert 2.9e9 < counters["mcs_rate_max_bps"] < 3.0e9
