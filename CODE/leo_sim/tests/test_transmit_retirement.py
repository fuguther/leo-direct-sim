"""Regression tests for the _transmit down-wait neighbourhood.

K1/K2/K3 from round-3 hunting (Kimi reproduced dynamically):
- K1: a down-wait must race the link retirement interrupt, otherwise a
  retiring link stays pinned past its hard deadline until the outage
  recovers, blocking the whole server.
- K2: the stop-time settle must not book pre-service down-wait as occupied
  (the caller's _svc timestamp must be restamped when transmission actually
  starts).
- K3: a packet waiting on a down link must never be failed with the expiry
  fate BEFORE its deadline (retirement may free it for re-association);
  the expiry fate may only be assigned once the deadline is reached.
"""
import pytest

from CODE.leo_sim import kernel, outage, rng as rngmod
from CODE.leo_sim.tests.helpers import StaticGeometry, cell, cell_center, make_cfg, row

A, B = cell(0.0, 0.0), cell(0.0, 10.0)
AC, BC = cell_center(A), cell_center(B)


def _two_sat_geo():
    def elev(s, lat, lon, t):
        if (lat, lon) == AC:
            return 90.0 if s == 0 else 80.0
        return 90.0 if s == 0 else -10.0  # B visible only to sat0

    def vis(s, lat, lon, t):
        return elev(s, lat, lon, t) >= 25.0

    return StaticGeometry(2, neighbors_map={0: {"E": 1}, 1: {"W": 0}},
                          visible=vis, elevation=elev, isl_changes=[])


def _contention_cfg(seed=19, monitor=False):
    return make_cfg({
        "scenario": {"num_satellites": 2, "num_planes": 1, "duration_s": 10.0,
                     "time_step_s": 0.1, "seed": seed},
        "access": {"slots_per_satellite": 1, "slot_lease_s": 1.0,
                   "retirement_deadline_s": 0.5, "idle_release_s": 999.0,
                   "min_dwell_s": 0.0, "hysteresis_deg": 0.0,
                   "acquisition_delay_s": 0.0},
        "links": {"ge_enabled": True,
                  "ge_gsl": {"mean_good_s": 1.0, "mean_bad_s": 2.0},
                  "ge_isl": {"mean_good_s": 1.0, "mean_bad_s": 2.0}},
        "control_plane": {"enabled": False},
        "execution": {"monitor": monitor},
    })


def test_downwait_races_retirement_interrupt():
    """K1: with slot contention forcing a lease retirement at ~1.5 s while
    the GSL is down, the packet must be retired (and re-associated) at the
    retirement deadline, not pinned until the outage recovers at ~5 s."""
    rows = [row(1, 0.6, A, B), row(2, 0.0, B, A)]  # B waits -> contention
    res = kernel.run_simulation(_contention_cfg(), rows, geometry=_two_sat_geo())
    assert res["fates"][1] == "DELIVERED"
    retire = [e for e in res["handover"]["events"]
              if e["type"] == "release"
              and str(e["reason"]).startswith("lease_retire")]
    assert retire and retire[0]["t"] < 2.0, (
        "retirement was not raced: link pinned until the outage recovered")


def test_no_premature_deadline_fail_while_retirement_pending():
    """K3: with a 2.0 s deadline and a retirement pending at ~1.5 s, the
    packet must not be failed with DATA_DEADLINE_EXPIRED at t0=0.6; the
    expiry fate may only be recorded once the deadline is actually reached
    (or the packet is rescued)."""
    rows = [row(1, 0.6, A, B, deadline=2.0), row(2, 0.0, B, A)]
    res = kernel.run_simulation(_contention_cfg(monitor=True), rows,
                                geometry=_two_sat_geo())
    fate_events = [t for t, kind, kv in res["monitor_log"]
                   if kind == "fate" and dict(kv).get("pid") == 1]
    assert fate_events, "missing fate monitor event"
    assert res["fates"][1] in ("DELIVERED", "DATA_DEADLINE_EXPIRED")
    if res["fates"][1] == "DATA_DEADLINE_EXPIRED":
        assert fate_events[0] >= 2.0, (
            "packet failed before its deadline (premature fail-fast)")


def test_stop_settle_excludes_preservice_downwait():
    """K2: when a GSL uplink is down before service starts, recovers at r
    within the horizon, and the service then crosses the stop, the stop-time
    settle must count only the real transmission time (horizon - r), never
    the pre-service down-wait from the caller's original _svc stamp."""
    cfg = make_cfg({
        "scenario": {"num_satellites": 1, "num_planes": 1, "duration_s": 1.2033,
                     "time_step_s": 0.1, "seed": 4},
        "access": {"uplink_rate_mbps": 1.0},
        "links": {"ge_enabled": True,
                  "ge_gsl": {"mean_good_s": 1.0, "mean_bad_s": 2.0}},
        "control_plane": {"enabled": False},
    })
    geo = StaticGeometry(1, visible=lambda *_: True)
    res = kernel.run_simulation(cfg, [row(1, 0.6, A, B)], geometry=geo)
    assert res["fates"][1] == "IN_SYSTEM_AT_STOP"
    # replay the private GE stream to recover the true up-time r
    ge = outage.GilbertElliott(1.0, 2.0,
                               rngmod.link_stream(4, "gsl:0:" + A),
                               enabled=True)
    r = None
    t = 0.6
    horizon = cfg["config"]["scenario"]["duration_s"]
    while t <= horizon + 1e-6:
        if not ge.is_down(t):
            r = t
            break
        t += 0.0005
    assert r is not None
    expected = horizon - r
    # the replay scan is quantized to 5e-4 s, so allow that tolerance
    assert res["occupied"]["gsl_uplink_s"] == pytest.approx(expected, abs=1e-3)
