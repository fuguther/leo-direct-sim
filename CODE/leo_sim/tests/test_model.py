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
