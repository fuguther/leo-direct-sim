"""Tests for CODE.leo_sim.model — constellation geometry and visibility."""
import math

import pytest

from CODE.leo_sim import model


def test_constellation_layout_deterministic():
    c1 = model.Constellation(num_satellites=12, num_planes=3, altitude_km=550, inclination_deg=53)
    c2 = model.Constellation(num_satellites=12, num_planes=3, altitude_km=550, inclination_deg=53)
    assert c1.positions(0.0) == c2.positions(0.0)
    assert len(c1.positions(0.0)) == 12
    # positions actually move over time
    assert c1.positions(0.0) != c1.positions(100.0)


def test_visibility_requires_elevation():
    c = model.Constellation(num_satellites=66, num_planes=6, altitude_km=550,
                            inclination_deg=53, min_elevation_deg=25.0)
    # a satellite directly overhead is visible
    lat, lon, alt = c.subpoint(0, 0.0)
    assert c.ground_visible(0, lat, lon, 0.0)
    # antipodal point is not
    assert not c.ground_visible(0, -lat, lon + 180.0 if lon <= 0 else lon - 180.0, 0.0)


def test_isl_neighbors_respect_directions():
    c = model.Constellation(num_satellites=12, num_planes=3, altitude_km=550, inclination_deg=53)
    nb = c.neighbors(0, ("N", "S", "E", "W"))
    assert set(nb) == {"N", "S", "E", "W"}
    nb_ns = c.neighbors(0, ("N", "S"))
    assert set(nb_ns) == {"N", "S"}
    # N/S are intra-plane neighbors and distinct from E/W
    assert nb["N"] != nb["E"]


def test_slant_and_propagation_positive():
    c = model.Constellation(num_satellites=12, num_planes=3, altitude_km=550, inclination_deg=53)
    lat, lon, _ = c.subpoint(0, 0.0)
    d = c.slant_range_km(0, lat, lon, 0.0)
    assert d >= 550.0
    assert model.propagation_delay_s(d) > 0


def test_no_future_ephemeris_api():
    # positions(t) is pure in t; visibility queries take explicit t — the
    # kernel only ever calls them with the current time.
    import inspect
    sig = inspect.signature(model.Constellation.positions)
    assert list(sig.parameters) == ["self", "t"]


def test_memoized_geometry_bit_equivalent_to_inner():
    c = model.Constellation(num_satellites=12, num_planes=3, altitude_km=550,
                            inclination_deg=53, min_elevation_deg=25.0,
                            max_isl_km=6000.0)
    m = model.MemoizedGeometry(c)
    lat, lon, _ = c.subpoint(0, 0.0)
    samples = [
        ("subpoint", (0, 0.0)), ("subpoint", (5, 12.5)),
        ("ecef", (0, 0.0)), ("ecef", (11, 30.25)),
        ("positions", (3.75,)), ("positions", (0.0,)),
        ("elevation_deg", (0, lat, lon, 0.0)),
        ("elevation_deg", (3, lat + 10.0, lon - 5.0, 7.5)),
        ("ground_visible", (0, lat, lon, 0.0)),
        ("slant_range_km", (0, lat, lon, 0.0)),
        ("isl_range_km", (0, 1, 0.0)),
        ("isl_available", (0, 1, 0.0)),
        ("next_isl_change", (0, 1, 0.0, 60.0)),
        ("next_gsl_change", (0, lat, lon, 0.0, 60.0)),
    ]
    for name, args in samples:
        # exact-argument memoization must return bit-identical values
        assert getattr(m, name)(*args) == getattr(c, name)(*args), name
    # repeated identical queries hit the cache and stay identical
    assert m.ecef(0, 0.0) == c.ecef(0, 0.0)


def test_memoized_geometry_caches_per_instant_and_bounds_memory():
    calls = {"ecef": 0}
    c = model.Constellation(num_satellites=12, num_planes=3, altitude_km=550,
                            inclination_deg=53)

    class _Counting(model.Constellation):
        def ecef(self, sat_id, t):
            calls["ecef"] += 1
            return super().ecef(sat_id, t)

    m = model.MemoizedGeometry(_Counting(
        num_satellites=12, num_planes=3, altitude_km=550, inclination_deg=53))
    # one decision at t queries every edge; a second decision at the same t
    # must not recompute any satellite position or edge range
    for _ in range(3):
        for a in range(12):
            for b in range(12):
                m.isl_range_km(a, b, 5.0)
    assert calls["ecef"] == 12  # one ECEF per satellite per instant
    # every directed edge computed once and cached under the same instant
    assert len(m._caches["isl_range_km"][5.0]) == 12 * 12
    # distinct instants evict old slots: memory stays bounded
    for i in range(2 * model.MemoizedGeometry._TIME_CAPACITY):
        m.isl_range_km(0, 1, float(i))
    assert len(m._caches["isl_range_km"]) <= model.MemoizedGeometry._TIME_CAPACITY
    assert len(m._caches["ecef"]) <= model.MemoizedGeometry._TIME_CAPACITY


def test_memoized_geometry_delegates_for_scripted_providers():
    from CODE.leo_sim.tests.helpers import StaticGeometry
    geo = StaticGeometry(2, neighbors_map={0: {"E": 1}, 1: {"W": 0}},
                         visible=lambda s, lat, lon, t: s == 0,
                         elevation=lambda s, lat, lon, t: (
                             90.0 if s == 0 else -10.0))
    m = model.MemoizedGeometry(geo)
    assert m.ground_visible(0, 0.0, 0.0, 1.0) is True
    assert m.ground_visible(1, 0.0, 0.0, 1.0) is False
    assert m.isl_available(0, 1, 2.0) is True
    assert m.next_isl_change(0, 1, 0.0, 10.0) is None
    assert m.elevation_deg(0, 0.0, 0.0, 1.0) == 90.0
