"""Deterministic geometry-only access coverage audit.

This module samples an already-resolved geometry provider.  It has no route,
queue, learning, or capacity semantics and therefore cannot decide whether a
constellation is sufficient for a traffic experiment.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any


class CoverageAuditError(ValueError):
    """Coverage audit input or geometry contract is invalid."""


# The 56-endpoint x 140-satellite x 3,601-sample audit is about 28.2M
# visibility checks. Keep a generous but finite headroom without allowing an
# accidental tiny step to allocate unbounded time samples.
MAX_COVERAGE_CHECKS = 50_000_000
MAX_COVERAGE_SAMPLES = 1_000_001
MAX_COVERAGE_ENDPOINTS = 10_000


def _finite(value: Any, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CoverageAuditError(f"{name} must be finite numeric")
    value = float(value)
    if not math.isfinite(value):
        raise CoverageAuditError(f"{name} must be finite numeric")
    return value


def _endpoints(endpoints) -> list[dict[str, Any]]:
    if not isinstance(endpoints, (list, tuple)):
        raise CoverageAuditError("endpoints must be a finite list")
    out = []
    seen = set()
    for index, item in enumerate(endpoints):
        if not isinstance(item, dict):
            raise CoverageAuditError(f"endpoint {index} must be a mapping")
        name = item.get("name", item.get("cell"))
        if not isinstance(name, str) or not name:
            raise CoverageAuditError(f"endpoint {index}.name must be non-empty")
        if name in seen:
            raise CoverageAuditError(f"duplicate endpoint name {name!r}")
        seen.add(name)
        lat = _finite(item.get("lat"), f"endpoint {name}.lat")
        lon = _finite(item.get("lon"), f"endpoint {name}.lon")
        if not -90 <= lat <= 90 or not -180 <= lon <= 180:
            raise CoverageAuditError(f"endpoint {name} lat/lon out of range")
        out.append({"name": name, "lat": lat, "lon": lon})
    return sorted(out, key=lambda item: item["name"])


def scan_coverage(geometry, endpoints, *, horizon_s: float, step_s: float,
                  visible_fraction_threshold: float = 0.5,
                  provenance: dict[str, Any] | None = None) -> dict[str, Any]:
    """Scan inclusive samples ``0, step, ..., horizon`` in stable order."""
    horizon = _finite(horizon_s, "horizon_s")
    step = _finite(step_s, "step_s")
    threshold = _finite(visible_fraction_threshold,
                        "visible_fraction_threshold")
    if horizon <= 0:
        raise CoverageAuditError("horizon_s must be > 0")
    if step <= 0:
        raise CoverageAuditError("step_s must be > 0")
    if step > horizon:
        raise CoverageAuditError("step_s must be <= horizon_s")
    if not 0 <= threshold <= 1:
        raise CoverageAuditError("visible_fraction_threshold must be in [0, 1]")
    if not hasattr(geometry, "num_satellites") or not hasattr(
            geometry, "ground_visible"):
        raise CoverageAuditError("geometry must expose num_satellites and ground_visible")
    n_sat = geometry.num_satellites
    if isinstance(n_sat, bool) or not isinstance(n_sat, int) or n_sat < 1:
        raise CoverageAuditError("geometry.num_satellites must be a positive integer")
    endpoint_specs = _endpoints(endpoints)
    if len(endpoint_specs) > MAX_COVERAGE_ENDPOINTS:
        raise CoverageAuditError(
            f"endpoint_count {len(endpoint_specs)} exceeds limit "
            f"{MAX_COVERAGE_ENDPOINTS}")
    interval_count = max(1, math.ceil(horizon / step - 1e-12))
    sample_count = interval_count + 1
    if sample_count > MAX_COVERAGE_SAMPLES:
        raise CoverageAuditError(
            f"sample_count {sample_count} exceeds limit "
            f"{MAX_COVERAGE_SAMPLES}")
    checks = len(endpoint_specs) * sample_count * n_sat
    if checks > MAX_COVERAGE_CHECKS:
        raise CoverageAuditError(
            f"coverage checks {checks} exceeds limit {MAX_COVERAGE_CHECKS} "
            f"(endpoints={len(endpoint_specs)}, samples={sample_count}, "
            f"satellites={n_sat})")
    times = [min(float(i * step), horizon) for i in range(interval_count)]
    times.append(float(horizon))
    results = []
    for endpoint in endpoint_specs:
        counts = []
        for at in times:
            count = sum(bool(geometry.ground_visible(
                sat, endpoint["lat"], endpoint["lon"], at))
                        for sat in range(n_sat))
            counts.append(count)
        visible_samples = sum(count > 0 for count in counts)
        never = visible_samples == 0
        first = next((at for at, count in zip(times, counts) if count > 0), None)
        max_gap = None
        if not never:
            gaps = []
            gap_start = None
            for at, count in zip(times, counts):
                if count == 0 and gap_start is None:
                    gap_start = at
                elif count > 0 and gap_start is not None:
                    gaps.append(at - gap_start)
                    gap_start = None
            if gap_start is not None:
                gaps.append(horizon - gap_start)
            max_gap = max(gaps, default=0.0)
        results.append({
            **endpoint,
            "visible_fraction": visible_samples / len(times),
            "first_visible_wait_s": first,
            "max_no_coverage_gap_s": max_gap,
            "never_visible": never,
            "visible_satellites": {
                "min": min(counts),
                "mean": sum(counts) / len(counts),
                "max": max(counts),
            },
            "min_visible_satellites": min(counts),
            "mean_visible_satellites": sum(counts) / len(counts),
            "max_visible_satellites": max(counts),
        })
    total = len(results)
    return {
        "schema": "leo-sim-coverage-audit/v1",
        "scan": {"horizon_s": horizon, "step_s": step,
                 "sample_count": len(times),
                 "visible_fraction_threshold": threshold},
        "endpoints": results,
        "summary": {
            "endpoints_total": total,
            "never_visible": sum(item["never_visible"] for item in results),
            "threshold_met_fraction": (
                sum(item["visible_fraction"] >= threshold for item in results)
                / total if total else 0.0),
        },
        "provenance": provenance or {},
    }


def stable_json(report: dict[str, Any]) -> str:
    """Serialize a report without nondeterministic key or whitespace changes."""
    return json.dumps(report, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")) + "\n"


def _cli() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True,
                        help="resolved simulator YAML config")
    parser.add_argument("--trace", type=Path, required=True,
                        help="compiled trace.csv or trace directory")
    parser.add_argument("--horizon", type=float)
    parser.add_argument("--step", type=float, required=True)
    parser.add_argument("--threshold", type=float, default=0.5)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    from . import config, grid, model, trace
    resolved = config.load_config_file(str(args.config))
    cfg = resolved["config"]
    horizon = (cfg["scenario"]["duration_s"]
               if args.horizon is None else args.horizon)
    trace_path = args.trace / "trace.csv" if args.trace.is_dir() else args.trace
    rows = trace.load_trace(str(trace_path), horizon_s=horizon,
                            max_packets=cfg["execution"]["max_packets"])
    cells = sorted({cell for row in rows for cell in
                    (row["src_grid_id"], row["dst_grid_id"])})
    endpoints = [{"name": cell, "lat": grid.grid_center(cell)[0],
                  "lon": grid.grid_center(cell)[1]} for cell in cells]
    geometry = model.Constellation(
        cfg["scenario"]["num_satellites"], cfg["scenario"]["num_planes"],
        cfg["scenario"]["altitude_km"], cfg["scenario"]["inclination_deg"],
        cfg["scenario"]["min_elevation_deg"],
        max_isl_km=cfg["links"]["max_isl_km"],
        geometry_epoch_s=cfg["scenario"]["geometry_epoch_s"])
    report = scan_coverage(
        geometry, endpoints, horizon_s=horizon, step_s=args.step,
        visible_fraction_threshold=args.threshold,
        provenance={"config_sha256": resolved["sha256"],
                    "trace_path": str(trace_path),
                    "trace_sha256": hashlib.sha256(trace_path.read_bytes()).hexdigest(),
                    "endpoint_source": "resolved_trace_cells"})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(stable_json(report), encoding="utf-8")
    return 0


if __name__ == "__main__":
    _cli()
