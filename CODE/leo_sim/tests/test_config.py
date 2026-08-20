"""Tests for CODE.leo_sim.config — strict versioned YAML configuration."""
import pytest

from CODE.leo_sim import config


def test_defaults_resolve_and_hash_stable():
    r1 = config.resolve_config()
    r2 = config.resolve_config()
    assert r1["version"] == config.CONFIG_SCHEMA_VERSION
    assert r1["sha256"] == r2["sha256"]
    assert r1["canonical_json"] == r2["canonical_json"]
    for group in config.SCHEMA:
        assert group in r1["config"]


def test_unknown_field_rejected():
    with pytest.raises(config.ConfigError, match="unknown field"):
        config.resolve_config({"scenario": {"bogus": 1}})
    with pytest.raises(config.ConfigError, match="unknown top-level"):
        config.resolve_config({"gateway": {}})


def test_profile_and_overrides_resolve():
    r = config.resolve_config(profile="smoke", overrides={"scenario": {"duration_s": 3.0}})
    assert r["config"]["scenario"]["duration_s"] == 3.0
    assert r["config"]["scenario"]["num_satellites"] == 12
    with pytest.raises(config.ConfigError, match="unknown profile"):
        config.resolve_config(profile="nope")


def test_invalid_combinations_rejected():
    with pytest.raises(config.ConfigError, match="dual_connect"):
        config.resolve_config({"access": {"association": "mbb"}})
    with pytest.raises(config.ConfigError, match="csv_path"):
        config.resolve_config({"demand": {"mode": "csv"}})
    with pytest.raises(config.ConfigError, match="burst"):
        config.resolve_config({"demand": {"mode": "burst"}})
    with pytest.raises(config.ConfigError, match="learning"):
        config.resolve_config({"routing": {"learning_enabled": True}})
    with pytest.raises(config.ConfigError, match="divisible"):
        config.resolve_config({"scenario": {"num_satellites": 7, "num_planes": 3}})


def test_available_capacity_sampling_interval_is_positive():
    with pytest.raises(config.ConfigError, match="available_capacity_interval_s"):
        config.resolve_config({"execution": {"available_capacity_interval_s": 0}})
    with pytest.raises(config.ConfigError, match="available_capacity_interval_s"):
        config.resolve_config({"execution": {"available_capacity_interval_s": True}})
    with pytest.raises(config.ConfigError, match="available_capacity_interval_s"):
        config.resolve_config({"execution": {"available_capacity_interval_s": 0.001}})
    with pytest.raises(config.ConfigError, match="100000"):
        config.resolve_config({
            "scenario": {"duration_s": 2000.0},
            "execution": {"available_capacity_interval_s": 0.01},
        })


def test_burst_window_must_intersect_scenario_horizon():
    base = {
        "scenario": {"duration_s": 120.0},
        "demand": {"mode": "burst", "burst_start_s": 121.0,
                   "burst_duration_s": 10.0, "burst_multiplier": 5.0},
    }
    with pytest.raises(config.ConfigError, match="intersect"):
        config.resolve_config(base)
    # window starting exactly at the horizon is also out of [0, duration)
    base["demand"]["burst_start_s"] = 120.0
    with pytest.raises(config.ConfigError, match="intersect"):
        config.resolve_config(base)
    # an intersecting window (including zero-length overlap edge) is valid
    base["demand"]["burst_start_s"] = 110.0
    ok = config.resolve_config(base)
    assert ok["config"]["demand"]["mode"] == "burst"


def test_mlab_burst_requires_complete_intersecting_window():
    with pytest.raises(config.ConfigError, match="mode=mlab"):
        config.resolve_config({
            "demand": {"mode": "mlab", "burst_start_s": 1.0},
        })
    with pytest.raises(config.ConfigError, match="intersect"):
        config.resolve_config({
            "scenario": {"duration_s": 10.0},
            "demand": {"mode": "mlab", "burst_start_s": 10.0,
                       "burst_duration_s": 1.0},
        })


def test_learning_eval_requires_sha_bound_checkpoint():
    with pytest.raises(config.ConfigError, match="checkpoint_path and checkpoint_sha256"):
        config.resolve_config({
            "routing": {"policy": "hop", "learning_enabled": True},
            "control_plane": {"enabled": True},
            "learning": {"algorithm": "ddqn", "mode": "eval"},
        })
    with pytest.raises(config.ConfigError, match="lowercase SHA-256"):
        config.resolve_config({
            "routing": {"policy": "hop", "learning_enabled": True},
            "control_plane": {"enabled": True},
            "learning": {"algorithm": "ddqn", "mode": "eval",
                         "checkpoint_path": "/tmp/model.keras",
                         "checkpoint_sha256": "bad"},
        })
    # DDQN eval with valid checkpoint SHA but no metadata SHA pin must fail
    # closed (the metadata file is the only contract anchor for opaque
    # model artifacts).
    with pytest.raises(config.ConfigError,
                       match="checkpoint_metadata_sha256"):
        config.resolve_config({
            "routing": {"policy": "hop", "learning_enabled": True},
            "control_plane": {"enabled": True},
            "learning": {"algorithm": "ddqn", "mode": "eval",
                         "checkpoint_path": "/tmp/model.keras",
                         "checkpoint_sha256": "ab" * 32},
        })


def test_bool_rejected_for_numeric():
    with pytest.raises(config.ConfigError, match="bool"):
        config.resolve_config({"scenario": {"seed": True}})


def test_load_config_file(tmp_path):
    p = tmp_path / "c.yaml"
    p.write_text(
        "profile: smoke\nscenario:\n  duration_s: 2.0\n  num_satellites: 6\n  num_planes: 2\n"
    )
    r = config.load_config_file(str(p))
    assert r["config"]["scenario"]["duration_s"] == 2.0
    bad = tmp_path / "bad.yaml"
    bad.write_text("config_version: other/v9\n")
    with pytest.raises(config.ConfigError, match="config_version"):
        config.load_config_file(str(bad))


def test_ge_dwell_rejects_bool():
    # bool is an int subclass: must not pass the GE dwell type check
    with pytest.raises(config.ConfigError, match="mean dwell"):
        config.resolve_config({"links": {"ge_enabled": True,
                                         "ge_gsl": {"mean_good_s": True,
                                                    "mean_bad_s": 1.0}}})
