import pytest

from CODE.leo_sim import coverage
from CODE.leo_sim.tests.helpers import StaticGeometry


def test_coverage_scan_reports_endpoint_gaps_and_stable_order():
    geo = StaticGeometry(2, visible=lambda sat, _lat, _lon, t:
                         sat == 0 and t < 1.0 or sat == 1 and t >= 1.0)
    endpoints = [
        {"name": "z", "lat": 0.0, "lon": 0.0},
        {"name": "a", "lat": 5.0, "lon": 5.0},
    ]
    got = coverage.scan_coverage(geo, endpoints, horizon_s=2.0, step_s=1.0,
                                 visible_fraction_threshold=0.5)
    assert [item["name"] for item in got["endpoints"]] == ["a", "z"]
    z = got["endpoints"][1]
    assert z["visible_fraction"] == pytest.approx(1.0)
    assert z["first_visible_wait_s"] == 0.0
    assert z["max_no_coverage_gap_s"] == pytest.approx(0.0)
    assert z["visible_satellites"] == {"min": 1, "mean": 1.0, "max": 1}
    assert got["summary"]["endpoints_total"] == 2
    assert got["summary"]["never_visible"] == 0
    assert got["summary"]["threshold_met_fraction"] == 1.0


def test_coverage_scan_rejects_bad_bounds_and_marks_never_visible():
    geo = StaticGeometry(1, visible=lambda *_: False)
    with pytest.raises(coverage.CoverageAuditError, match="step_s"):
        coverage.scan_coverage(geo, [], horizon_s=1.0, step_s=0.0)
    got = coverage.scan_coverage(
        geo, [{"name": "a", "lat": 0.0, "lon": 0.0}],
        horizon_s=1.0, step_s=0.5)
    item = got["endpoints"][0]
    assert item["never_visible"] is True
    assert item["first_visible_wait_s"] is None
    assert item["max_no_coverage_gap_s"] is None
