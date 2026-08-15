#!/usr/bin/env python3
"""Load-level scan for leo_sim V2 using the non-learning hop policy.

Purpose (2026-08-14, Codex x Kimi matrix):
  1. E0 选档:用最短路径(非学习)扫细流量档,低成本多跑,定出低/中/高档。
  2. 数据管道验证:每次运行后从 trace+ledgers+receipt 算全套指标,确认
     后续正式实验需要的 completion/latency/backlog/load 都能产出。
  3. 回归哨兵:非学习臂可作为"改平台没改坏"的低成本检查。

Usage:
  python3 scan_load_levels.py --worktree <V2_worktree> --config <yaml> \
      --out <out_dir> --levels 0.5,1.0,1.5,2.0 [--policy hop]

The script runs `python -m CODE.leo_sim run` in the worktree with a per-level
resolved config (only demand.offered_mbps and outputs.out_dir change), then
computes the analysis metrics from the produced artifacts.  It never touches
the source checkout and writes nothing into CODE.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def _load_resolved(worktree: Path, config_path: str) -> dict:
    """Load and resolve a config through the worktree's leo_sim package."""
    import importlib.util

    # Prefer the worktree package over any installed copy.
    spec = importlib.util.spec_from_file_location(
        "leo_sim_config", worktree / "CODE" / "leo_sim" / "config.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["leo_sim_config"] = mod
    spec.loader.exec_module(mod)
    loaded = mod.load_config_file(str(config_path))
    return mod.resolve_config(loaded["config"])


def _run_level(worktree: Path, resolved: dict, python: str, level: float,
               out_dir: Path, policy: str, max_packets: int | None,
               max_events: int | None) -> dict:
    """Run one non-learning level and return its metrics."""
    cfg = json.loads(json.dumps(resolved["config"]))  # deep copy
    cfg["demand"]["offered_mbps"] = float(level)
    cfg["routing"]["policy"] = policy
    cfg["routing"]["learning_enabled"] = False
    cfg["learning"]["algorithm"] = "none"
    cfg["outputs"]["out_dir"] = str(out_dir)
    if max_packets is not None:
        cfg["execution"]["max_packets"] = int(max_packets)
    if max_events is not None:
        cfg["execution"]["max_events"] = int(max_events)
    run_dir = out_dir / f"level-{level:g}"
    run_dir.mkdir(parents=True, exist_ok=True)
    tmp_cfg = run_dir / "scan-config.yaml"
    # Minimal YAML serializer: the config is plain str/num/bool/list/dict.
    tmp_cfg.write_text(_dump_yaml(cfg), encoding="utf-8")

    cmd = [python, "-B", "-m", "CODE.leo_sim", "run",
           "--config", str(tmp_cfg), "--out", str(run_dir / "out")]
    proc = subprocess.run(cmd, cwd=worktree, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"level {level} run failed rc={proc.returncode}\n"
            f"stdout: {proc.stdout[-2000:]}\nstderr: {proc.stderr[-2000:]}")
    return _analyze(run_dir / "out")


def _dump_yaml(data) -> str:
    """Tiny YAML emitter for the resolved config subset."""
    lines = ["config_version: leo-sim-config/v1"]
    for key, value in data.items():
        _emit(lines, key, value, 0)
    return "\n".join(lines) + "\n"


def _emit(lines: list, key, value, indent: int):
    pad = "  " * indent
    if isinstance(value, dict):
        lines.append(f"{pad}{key}:")
        for k, v in value.items():
            _emit(lines, k, v, indent + 1)
    elif isinstance(value, list):
        lines.append(f"{pad}{key}:")
        for item in value:
            lines.append(f"{pad}- {json.dumps(item, ensure_ascii=False)}")
    elif value is None:
        lines.append(f"{pad}{key}: null")
    elif isinstance(value, bool):
        lines.append(f"{pad}{key}: {'true' if value else 'false'}")
    elif isinstance(value, (int, float)):
        lines.append(f"{pad}{key}: {value}")
    else:
        lines.append(f"{pad}{key}: {json.dumps(str(value), ensure_ascii=False)}")


def _analyze(run_dir: Path) -> dict:
    """Compute analysis metrics from trace + ledgers + receipt."""
    receipt = json.loads((run_dir / "receipt.json").read_text(encoding="utf-8"))
    ledgers = json.loads((run_dir / "ledgers.json").read_text(encoding="utf-8"))
    trace_rows = []
    with (run_dir / "trace.csv").open(encoding="utf-8") as fh:
        header = fh.readline().strip().split(",")
        for line in fh:
            vals = line.strip().split(",")
            row = dict(zip(header, vals))
            trace_rows.append(row)
    emit = {int(r["packet_id"]): float(r["emit_time_s"]) for r in trace_rows}
    deliveries = ledgers.get("deliveries", {})
    latencies = []
    for pid_s, d in deliveries.items():
        pid = int(pid_s)
        if pid in emit:
            latencies.append(float(d["delivered_at"]) - emit[pid])
    fates = ledgers.get("packet_fates", {})
    n_offered = len(trace_rows)
    n_delivered = len(deliveries)
    n_in_system = sum(1 for f in fates.values() if f[0] == "IN_SYSTEM_AT_STOP")
    offered_bits = sum(int(r["bits"]) for r in trace_rows)
    delivered_bits = sum(int(f[1]) for f in fates.values() if f[0] == "DELIVERED")
    qa = ledgers.get("queue_area_bits_s", {})
    stop = float(ledgers.get("stop_time_s", 0.0))
    lat = sorted(latencies)
    p95 = lat[int(0.95 * len(lat)) - 1] if lat else None
    return {
        "completion_ratio": round(n_delivered / n_offered, 4) if n_offered else None,
        "mean_latency_s": round(sum(latencies) / len(latencies), 4) if latencies else None,
        "p95_latency_s": round(p95, 4) if p95 is not None else None,
        "in_system_ratio": round(n_in_system / n_offered, 4) if n_offered else None,
        "offered_bits": offered_bits,
        "delivered_bits": delivered_bits,
        "offered_mbps": round(offered_bits / max(stop, 1e-9) / 1e6, 4),
        "conservation_ok": bool(receipt.get("conservation_ok")),
        "natural_end": bool(receipt.get("natural_end")),
        "queue_area": {k: round(v, 2) for k, v in qa.items()},
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--worktree", required=True, type=Path)
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--levels", required=True,
                    help="comma-separated offered_mbps levels")
    ap.add_argument("--policy", default="hop", choices=["hop", "delay", "capacity"])
    ap.add_argument("--python", default=sys.executable)
    ap.add_argument("--max-packets", type=int, default=None,
                    help="override execution.max_packets (prevent high-load "
                         "truncation; use when the base config caps packets)")
    ap.add_argument("--max-events", type=int, default=None,
                    help="override execution.max_events (high-load runs on "
                         "large constellations may exhaust the base budget)")
    args = ap.parse_args()

    resolved = _load_resolved(args.worktree.resolve(), args.config)
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    results = {}
    for level in [float(x) for x in args.levels.split(",")]:
        try:
            metrics = _run_level(args.worktree.resolve(), resolved,
                                 args.python, level, out, args.policy,
                                 args.max_packets, args.max_events)
            results[f"{level:g}"] = metrics
            print(f"level {level:g}: completion={metrics['completion_ratio']} "
                  f"mean={metrics['mean_latency_s']} "
                  f"p95={metrics['p95_latency_s']} "
                  f"in_system={metrics['in_system_ratio']} "
                  f"offered_mbps={metrics['offered_mbps']} "
                  f"consv={metrics['conservation_ok']} "
                  f"end={metrics['natural_end']}")
        except Exception as exc:
            results[f"{level:g}"] = {"error": str(exc)[-500:]}
            print(f"level {level:g}: FAILED -> {str(exc)[-300:]}")
        (out / "scan-summary.json").write_text(
            json.dumps({"policy": args.policy, "levels": results},
                       indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"summary -> {out / 'scan-summary.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
