"""End-to-end CLI tests: validate, compile, dry-run, run, receipt verify."""
import hashlib
import json
import importlib.util
from pathlib import Path

import pytest

from CODE.leo_sim.__main__ import _DecisionLogWriter, main

SMOKE = str(Path(__file__).resolve().parent.parent / "profiles" / "smoke.yaml")


def _write_cfg(tmp_path, extra=""):
    p = tmp_path / "cfg.yaml"
    p.write_text(
        "scenario:\n  duration_s: 5.0\n  num_satellites: 1\n  num_planes: 1\n  seed: 3\n"
        "endpoints:\n  sites:\n"
        "    - {name: a, lat: 0.1, lon: 0.1}\n"
        "    - {name: b, lat: 2.0, lon: 3.0}\n"
        "demand:\n  mode: uniform\n  offered_mbps: 2.0\n  packet_bits: 1000000\n"
        "routing:\n  policy: oracle\n"
        "control_plane:\n  enabled: false\n"
        f"outputs:\n  out_dir: {tmp_path}/out\n" + extra)
    return str(p)


def test_config_validate_ok(capsys):
    rc = main(["config", "validate", SMOKE])
    out = json.loads(capsys.readouterr().out)
    assert rc == 0 and out["status"] == "ok" and len(out["sha256"]) == 64


def test_config_validate_rejects_unknown_field(tmp_path, capsys):
    p = tmp_path / "bad.yaml"
    p.write_text("scenario:\n  duration_s: 5\n  teleport: true\n")
    rc = main(["config", "validate", str(p)])
    assert rc == 2
    assert "unknown field" in capsys.readouterr().out


def test_trace_compile_byte_reproducible(tmp_path, capsys):
    cfg = _write_cfg(tmp_path)
    main(["trace", "compile", "--config", cfg, "--out", str(tmp_path / "t1")])
    m1 = json.loads(capsys.readouterr().out)
    main(["trace", "compile", "--config", cfg, "--out", str(tmp_path / "t2")])
    m2 = json.loads(capsys.readouterr().out)
    assert m1["trace_sha256"] == m2["trace_sha256"]
    assert m1["manifest_sha256"] == m2["manifest_sha256"]
    assert m1["offered_packets"] > 0


def test_run_dry_run_writes_no_receipt(tmp_path, capsys):
    cfg = _write_cfg(tmp_path)
    rc = main(["run", "--config", cfg, "--out", str(tmp_path / "dry"), "--dry-run"])
    out = json.loads(capsys.readouterr().out)
    assert rc == 0 and out["status"] == "DRY RUN"
    assert not (tmp_path / "dry" / "receipt.json").exists()


def test_full_run_and_receipt_verify(tmp_path, capsys):
    cfg = _write_cfg(tmp_path)
    out_dir = str(tmp_path / "out")
    rc = main(["run", "--config", cfg, "--out", out_dir])
    out = json.loads(capsys.readouterr().out)
    assert rc == 0 and out["natural_end"] is True and out["conservation_ok"] is True
    rc2 = main(["receipt", "verify", out_dir])
    assert rc2 == 0, capsys.readouterr().out


def test_run_writes_optional_decision_log_with_info_audit(tmp_path, capsys):
    cfg = _write_cfg(tmp_path)
    cfg_path = Path(cfg)
    cfg_path.write_text(
        cfg_path.read_text(encoding="utf-8").replace(
            "num_satellites: 1", "num_satellites: 2"),
        encoding="utf-8")
    out_dir = tmp_path / "out"
    decision_log = tmp_path / "decision-snapshots.jsonl"
    rc = main(["run", "--config", cfg, "--out", str(out_dir),
               "--decision-log", str(decision_log)])
    assert rc == 0
    capsys.readouterr()
    rows = [json.loads(line) for line in decision_log.read_text().splitlines()]
    assert rows
    assert all(row["info_audit"]["schema"] == "leo-sim-decision-info/v1"
               for row in rows)
    manifest = json.loads(
        (tmp_path / "decision-snapshots.jsonl.manifest.json").read_text())
    assert manifest["schema"] == "leo-sim-decision-log/v1"
    assert manifest["row_count"] == len(rows)
    assert len(manifest["config_sha256"]) == 64
    assert len(manifest["trace_sha256"]) == 64
    assert len(manifest["code_sha256"]) == 64
    assert len(manifest["receipt_sha256"]) == 64


def test_decision_log_rejects_existing_target_before_simulation(tmp_path, capsys):
    cfg = _write_cfg(tmp_path)
    decision_log = tmp_path / "already-there.jsonl"
    decision_log.write_text("sentinel\n", encoding="utf-8")
    out_dir = tmp_path / "out"
    rc = main(["run", "--config", cfg, "--out", str(out_dir),
               "--decision-log", str(decision_log)])
    assert rc == 3
    assert "destination" in capsys.readouterr().out
    assert not out_dir.exists()
    assert decision_log.read_text(encoding="utf-8") == "sentinel\n"


def test_decision_log_rejects_existing_manifest_before_simulation(tmp_path, capsys):
    cfg = _write_cfg(tmp_path)
    decision_log = tmp_path / "audit.jsonl"
    manifest = tmp_path / "audit.jsonl.manifest.json"
    manifest.write_text("sentinel manifest\n", encoding="utf-8")
    out_dir = tmp_path / "out"
    rc = main(["run", "--config", cfg, "--out", str(out_dir),
               "--decision-log", str(decision_log)])
    assert rc == 3
    assert "destination" in capsys.readouterr().out
    assert not out_dir.exists()
    assert not decision_log.exists()
    assert manifest.read_text(encoding="utf-8") == "sentinel manifest\n"


def test_decision_log_hash_is_incremental_on_close(tmp_path, monkeypatch):
    decision_log = tmp_path / "audit.jsonl"
    writer = _DecisionLogWriter(str(decision_log))
    row = {"kind": "forward", "value": 1}
    writer.append(row)
    encoded = (json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n").encode()

    original_read_bytes = Path.read_bytes

    def reject_target_read_bytes(path):
        if path == decision_log:
            raise AssertionError("close must not read the published log into memory")
        return original_read_bytes(path)

    monkeypatch.setattr(Path, "read_bytes", reject_target_read_bytes)
    assert writer.close() == hashlib.sha256(encoded).hexdigest()


def test_decision_log_rejects_symlink_parent_before_simulation(tmp_path, capsys):
    cfg = _write_cfg(tmp_path)
    real_parent = tmp_path / "real"
    real_parent.mkdir()
    linked_parent = tmp_path / "linked"
    linked_parent.symlink_to(real_parent, target_is_directory=True)
    out_dir = tmp_path / "out"
    rc = main(["run", "--config", cfg, "--out", str(out_dir),
               "--decision-log", str(linked_parent / "audit.jsonl")])
    assert rc == 3
    assert "symlink" in capsys.readouterr().out
    assert not out_dir.exists()
    assert not (real_parent / "audit.jsonl").exists()


def test_receipt_verify_fails_on_tamper(tmp_path, capsys):
    cfg = _write_cfg(tmp_path)
    out_dir = tmp_path / "out"
    main(["run", "--config", cfg, "--out", str(out_dir)])
    capsys.readouterr()
    rcp = json.loads((out_dir / "receipt.json").read_text())
    rcp["totals"]["delivered_bits"] += 1  # tamper
    (out_dir / "receipt.json").write_text(json.dumps(rcp, indent=2, sort_keys=True) + "\n")
    rc = main(["receipt", "verify", str(out_dir)])
    assert rc == 2
    assert "errors" in capsys.readouterr().out


def test_learning_run_fails_closed_without_tensorflow(tmp_path, capsys):
    cfg = _write_cfg(tmp_path)
    p = Path(cfg)
    text = p.read_text(encoding="utf-8").replace(
        "routing:\n  policy: oracle\n",
        "routing:\n  policy: hop\n  learning_enabled: true\n").replace(
        "control_plane:\n  enabled: false\n",
        "control_plane:\n  enabled: true\n")
    p.write_text(text + "learning:\n  algorithm: ddqn\n", encoding="utf-8")
    rc = main(["run", "--config", cfg, "--out", str(tmp_path / "out2")])
    if importlib.util.find_spec("tensorflow") is None:
        assert rc == 3
        assert "fail closed" in capsys.readouterr().out.lower()


def test_smoke_profile_real_constellation_delivers(tmp_path, capsys):
    out_dir = str(tmp_path / "smoke")
    rc = main(["run", "--config", SMOKE, "--out", out_dir])
    out = json.loads(capsys.readouterr().out)
    assert rc == 0 and out["natural_end"] is True
    assert out["fate_counts"]["DELIVERED"] >= 1
    rc2 = main(["receipt", "verify", out_dir])
    assert rc2 == 0


def test_run_consumes_precompiled_trace_with_sha_check(tmp_path, capsys):
    cfg = _write_cfg(tmp_path)
    tdir = tmp_path / "tr"
    assert main(["trace", "compile", "--config", cfg, "--out", str(tdir)]) == 0
    capsys.readouterr()
    # point the config at the precompiled trace; run must NOT recompile
    text = (tmp_path / "cfg.yaml").read_text()
    p2 = tmp_path / "cfg2.yaml"
    p2.write_text(text + f"  trace_path: {tdir}\n")  # under outputs:
    out_dir = str(tmp_path / "out3")
    rc = main(["run", "--config", str(p2), "--out", out_dir])
    assert rc == 0, capsys.readouterr().out
    assert main(["receipt", "verify", out_dir]) == 0
    # a tampered precompiled trace must be refused before any simulation
    (tdir / "trace.csv").write_text(
        (tdir / "trace.csv").read_text().replace("1000000", "1000001", 1))
    rc2 = main(["run", "--config", str(p2), "--out", str(tmp_path / "out4")])
    assert rc2 == 2
    assert "TRACE COMPILE FAILED" in capsys.readouterr().out
