"""Task 1 receipt contracts: frozen identity/v2 verification and the
identity/v3 split for new compilations.

A v2-contract receipt (trace_identity_contract == identity/v2) must still
verify byte-for-byte under the new code through the frozen v2 builder, and
must fail when any old v2 trace-determining field is tampered.  v5
verification chooses the v2 or v3 builder ONLY from the persisted
trace_identity_contract; no other value is accepted and nothing is guessed
from the current code version or the manifest schema.  identity/v1 support
remains unchanged (covered by the legacy fixtures in the CLI/congestion
tests).
"""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from CODE.leo_sim import config, kernel, receipt, trace

POPULATION_TIFF = (Path(__file__).resolve().parents[2] / "population_map"
                   / "gpw_v4_population_count_rev11_2020_15_min.tif")
POPULATION_PROFILE = (Path(__file__).resolve().parents[2]
                      / "leo_sim" / "profiles" / "population_gravity.yaml")
FROZEN_OLD_V2_TRACE_IDENTITY = (
    "2715dfb316de48d958cd05fa09aafcf22e340766d186e7a0a9a9b6a4b0dd9ad4")


def _build_frozen_v2_run(tmp_path: Path) -> Path:
    """A full run directory whose trace identity contract is frozen v2.

    The trace is compiled with the current code (identity/v3 manifest is
    produced by compile_trace), then the in-memory manifest is re-stamped to
    the frozen v2 identity value and the persisted receipt declares identity
    v2.  Under the new code, v5 verification must select the frozen v2
    builder from that persisted contract and reproduce the identity.
    """
    resolved = config.load_config_file(str(POPULATION_PROFILE))
    tdir = tmp_path / "compiled"
    manifest = trace.compile_trace(resolved, str(tdir))
    tbytes = (tdir / "trace.csv").read_bytes()
    input_sha = manifest["input_sha256"]
    # the frozen v2 identity of this exact profile must be reconstructible
    v2_identity = config.trace_identity_sha256_v2(resolved, input_sha)
    assert v2_identity == FROZEN_OLD_V2_TRACE_IDENTITY

    manifest["trace_identity_sha256"] = v2_identity
    manifest["__trace_sha256"] = hashlib.sha256(tbytes).hexdigest()
    manifest_bytes = json.dumps(
        {k: v for k, v in manifest.items() if not k.startswith("__")},
        indent=2, sort_keys=True) + "\n"
    manifest["__sha256"] = hashlib.sha256(
        manifest_bytes.encode("utf-8")).hexdigest()

    rows = trace.load_trace(
        str(tdir / "trace.csv"),
        horizon_s=resolved["config"]["scenario"]["duration_s"],
        max_packets=resolved["config"]["execution"]["max_packets"])
    result = kernel.run_simulation(resolved, rows)
    out = tmp_path / "run"
    receipt.write_run(str(out), resolved, tbytes, manifest, result, rows)
    # persist the frozen identity CONTRACT (the sha already came from the
    # manifest, which build_receipt reads verbatim)
    rcp_path = out / "receipt.json"
    rcp = json.loads(rcp_path.read_text(encoding="utf-8"))
    rcp["trace_identity_contract"] = config.TRACE_IDENTITY_VERSION_V2
    rcp["trace_identity_sha256"] = v2_identity
    rcp_path.write_text(
        json.dumps(rcp, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out


def test_frozen_v2_receipt_still_verifies_under_new_code(tmp_path):
    out = _build_frozen_v2_run(tmp_path)
    rcp = json.loads((out / "receipt.json").read_text(encoding="utf-8"))
    assert rcp["trace_identity_contract"] == config.TRACE_IDENTITY_VERSION_V2
    assert rcp["trace_identity_sha256"] == FROZEN_OLD_V2_TRACE_IDENTITY
    assert receipt.verify_receipt_dir(str(out)) == []


def test_frozen_v2_receipt_fails_when_trace_determining_field_tampered(
        tmp_path):
    out = _build_frozen_v2_run(tmp_path)
    assert receipt.verify_receipt_dir(str(out)) == []

    # tamper the manifest's trace identity value: the identity gate must fire
    mpath = out / "manifest.json"
    m = json.loads(mpath.read_text(encoding="utf-8"))
    m["trace_identity_sha256"] = "0" * 64
    mpath.write_text(
        json.dumps(m, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    errors = receipt.verify_receipt_dir(str(out))
    assert any("trace identity" in e for e in errors)

    # tamper a demand field inside the resolved config (offered_mbps is a v2
    # trace-determining field): the identity gate must fire even though the
    # artifact set is otherwise internally consistent
    out2 = tmp_path / "run2"
    shutil.copytree(str(out), str(out2))
    cfg_path = out2 / "resolved_config.json"
    rc = json.loads(cfg_path.read_text(encoding="utf-8"))
    rc["config"]["demand"]["offered_mbps"] = rc["config"]["demand"][
        "offered_mbps"] + 1.0
    cfg_path.write_text(
        json.dumps(rc, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    errors = receipt.verify_receipt_dir(str(out2))
    assert any("trace identity" in e for e in errors)


def test_v5_receipt_rejects_unknown_trace_identity_contract(tmp_path):
    out = _build_frozen_v2_run(tmp_path)
    rcp_path = out / "receipt.json"
    rcp = json.loads(rcp_path.read_text(encoding="utf-8"))
    rcp["trace_identity_contract"] = "leo-sim-trace-identity/v999"
    rcp_path.write_text(
        json.dumps(rcp, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    errors = receipt.verify_receipt_dir(str(out))
    assert any("trace_identity_contract" in e for e in errors)


def test_v5_receipt_never_guesses_from_manifest_schema_or_code_version(
        tmp_path):
    """The v2/v3 selection must come from the persisted contract only: a
    manifest schema or the current code default must not masquerade as a
    contract decision."""
    out = _build_frozen_v2_run(tmp_path)
    assert receipt.verify_receipt_dir(str(out)) == []
    # A v3-stamped receipt (new-code default) verifies through the v3
    # builder; the same artifact set with the contract flipped back to v2
    # verifies through the v2 builder.  Both are explicit contract choices.
    out3 = tmp_path / "run3"
    shutil.copytree(str(out), str(out3))
    rcp_path = out3 / "receipt.json"
    rcp = json.loads(rcp_path.read_text(encoding="utf-8"))
    rcp["trace_identity_contract"] = config.TRACE_IDENTITY_VERSION
    rcp_path.write_text(
        json.dumps(rcp, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    errors = receipt.verify_receipt_dir(str(out3))
    # trace_identity_sha256 still holds the frozen v2 value; the v3 builder
    # must NOT accept it (the contract is authoritative, not the code)
    assert any("trace identity" in e for e in errors)


def test_new_compilation_declares_identity_v3(tmp_path, monkeypatch):
    """compile_trace must stamp identity/v3 on fresh compilations and the
    receipt created from such a run carries the v3 contract."""
    from CODE.leo_sim import population
    regions = (
        population.PopulationRegion("G5:18:36", 2.5, 2.5, 2.0),
        population.PopulationRegion("G5:18:37", 2.5, 7.5, 1.0),
    )
    table = population.PopulationTable(
        regions=regions, source_path="/fake/pop.tif", source_sha256="b" * 64,
        source_shape=(720, 1440), source_resolution_deg=(0.25, 0.25),
        aggregation_deg=5.0, total_population=3.0)
    monkeypatch.setattr(population, "load_population_regions",
                        lambda path, aggregation_deg: table)
    cfg = config.resolve_config({
        "scenario": {"duration_s": 5.0, "seed": 3},
        "endpoints": {"aggregation_deg": 5.0},
        "demand": {"mode": "population_gravity",
                   "population_path": "/fake/pop.tif"},
    })
    manifest = trace.compile_trace(cfg, str(tmp_path / "compiled"))
    assert config.trace_identity_payload(cfg)["identity_version"] == \
        config.TRACE_IDENTITY_VERSION
    assert manifest["trace_identity_sha256"] == config.trace_identity_sha256(
        cfg, manifest["input_sha256"])