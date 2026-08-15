"""Critical orchestration checks for the one-command platform outcome."""
from pathlib import Path

import pytest

from CODE.leo_sim import platform_check
from CODE.leo_sim.__main__ import main


def test_platform_check_runs_each_real_stage_once(tmp_path, monkeypatch):
    calls = []

    def fake_acceptance(out):
        calls.append(("mechanisms", Path(out)))
        return {"status": "PASS", "cases": {}}

    def fake_comparison(cfg, out):
        calls.append(("comparison", Path(out)))
        return {"status": "PASS", "same_trace": True}

    def fake_ddqn(cfg, out):
        calls.append(("ddqn", Path(out)))
        return {"status": "PASS", "checks": {}}

    def fake_population(cfg, out):
        calls.append(("population", Path(out)))
        return {"status": "PASS", "checks": {}}

    monkeypatch.setattr(platform_check.acceptance, "run_acceptance", fake_acceptance)
    monkeypatch.setattr(platform_check.comparison, "run_comparison", fake_comparison)
    monkeypatch.setattr(platform_check, "_run_ddqn_chain", fake_ddqn)
    monkeypatch.setattr(platform_check, "_run_population", fake_population)

    out = tmp_path / "platform"
    result = platform_check.run_platform_check(out)
    assert result["status"] == "PASS"
    assert [name for name, _ in calls] == [
        "mechanisms", "population", "comparison", "ddqn"]
    assert (out / "platform-summary.json").is_file()


def test_platform_check_stops_at_first_failed_stage_and_keeps_summary(
        tmp_path, monkeypatch):
    monkeypatch.setattr(
        platform_check.acceptance, "run_acceptance",
        lambda out: {"status": "PASS", "cases": {}})
    monkeypatch.setattr(
        platform_check, "_run_population",
        lambda cfg, out: {"status": "PASS", "checks": {}})

    def fail_comparison(cfg, out):
        raise RuntimeError("legacy process exited 1")

    monkeypatch.setattr(
        platform_check.comparison, "run_comparison", fail_comparison)
    monkeypatch.setattr(
        platform_check, "_run_ddqn_chain",
        lambda *args: pytest.fail("DDQN must not run after comparison failure"))

    out = tmp_path / "platform"
    result = platform_check.run_platform_check(out)
    assert result["status"] == "FAIL"
    assert result["failed_stage"] == "gateway_vs_direct"
    assert result["error"]["message"] == "legacy process exited 1"
    assert (out / "platform-summary.json").is_file()


def test_platform_check_rejects_nonempty_output(tmp_path):
    out = tmp_path / "platform"
    out.mkdir()
    (out / "existing").write_text("do not overwrite")
    with pytest.raises(platform_check.PlatformCheckError, match="new or empty"):
        platform_check.run_platform_check(out)


def test_platform_check_rejects_symlink_output(tmp_path):
    target = tmp_path / "target"
    target.mkdir()
    link = tmp_path / "platform"
    link.symlink_to(target, target_is_directory=True)
    with pytest.raises(platform_check.PlatformCheckError, match="symbolic link"):
        platform_check.run_platform_check(link)


def test_platform_check_cli_returns_nonzero_for_failed_outcome(
        tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(
        platform_check, "run_platform_check",
        lambda *args, **kwargs: {"status": "FAIL", "failed_stage": "ddqn"})
    rc = main(["platform", "check", "--out", str(tmp_path / "out")])
    assert rc == 9
    assert '"status": "FAIL"' in capsys.readouterr().out
