#!/usr/bin/env python3
"""Run one leo_sim V2 learning experiment cell-matrix.

Purpose: execute Experiment 1 (hop sweep, fixed contract) and Experiment 2
(contract sweep, fixed hops) with separated train/traffic seeds, and emit a
single summary JSON per run plus a final matrix summary.

Usage:
  python3 run_learning_experiment.py --worktree <V2_worktree> \
      --config <base.yaml> --out <dir> \
      --contracts GAT --vis-k 1,2,3 --offered-mbps 300 \
      --train-seeds 41,42,43 --traffic-seed 101 --duration-s 60

Only learning.algorithm=ddqn contracts are trained.  Each (contract, vis_k,
train_seed) cell writes to <out>/<contract>-k<vis_k>-s<train_seed>/ and the
analysis metrics are appended to <out>/matrix-summary.json after every cell
(so a single failed cell does not lose the rest).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def _load_config_mod(worktree: Path):
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "leo_sim_config", worktree / "CODE" / "leo_sim" / "config.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["leo_sim_config"] = mod
    spec.loader.exec_module(mod)
    return mod


def _dump_yaml(data) -> str:
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
    receipt = json.loads((run_dir / "receipt.json").read_text(encoding="utf-8"))
    ledgers = json.loads((run_dir / "ledgers.json").read_text(encoding="utf-8"))
    trace_rows = []
    with (run_dir / "trace.csv").open(encoding="utf-8") as fh:
        header = fh.readline().strip().split(",")
        for line in fh:
            row = dict(zip(header, line.strip().split(",")))
            trace_rows.append(row)
    emit = {int(r["packet_id"]): float(r["emit_time_s"]) for r in trace_rows}
    deliveries = ledgers.get("deliveries", {})
    latencies = [
        float(d["delivered_at"]) - emit[int(pid)]
        for pid, d in deliveries.items() if int(pid) in emit]
    fates = ledgers.get("packet_fates", {})
    n_offered = len(trace_rows)
    n_delivered = len(deliveries)
    n_in_system = sum(1 for f in fates.values() if f[0] == "IN_SYSTEM_AT_STOP")
    lat = sorted(latencies)
    p95 = lat[int(0.95 * len(lat)) - 1] if lat else None
    learning = ledgers.get("learning", {})
    qa = ledgers.get("queue_area_bits_s", {})
    return {
        "completion_ratio": round(n_delivered / n_offered, 4) if n_offered else None,
        "mean_latency_s": round(sum(latencies) / len(latencies), 4) if latencies else None,
        "p95_latency_s": round(p95, 4) if p95 is not None else None,
        "in_system_ratio": round(n_in_system / n_offered, 4) if n_offered else None,
        "conservation_ok": bool(receipt.get("conservation_ok")),
        "natural_end": bool(receipt.get("natural_end")),
        "train_steps": learning.get("train_steps"),
        "decisions": learning.get("decisions"),
        "last_loss": learning.get("last_loss"),
        "checkpoint_verified": learning.get("checkpoint_verified"),
        "queue_area": {k: round(v, 2) for k, v in qa.items()},
    }


def _run_cell(worktree: Path, config_mod, base_cfg: str, out_root: Path,
              python: str, *, contract: str, vis_k: int, train_seed: int,
              traffic_seed: int, offered_mbps: float, duration_s: float,
              obs_hops: int | None = None) -> dict:
    loaded = config_mod.load_config_file(base_cfg)
    cfg = json.loads(json.dumps(loaded["config"]))  # deep copy
    cfg["scenario"]["seed"] = int(traffic_seed)
    cfg["scenario"]["duration_s"] = float(duration_s)
    cfg["demand"]["offered_mbps"] = float(offered_mbps)
    cfg["control_plane"]["vis_k"] = int(vis_k)
    if obs_hops is not None:
        cfg["learning"]["obs_hops"] = int(obs_hops)
    else:
        cfg["learning"]["obs_hops"] = int(vis_k)
    cfg["routing"]["policy"] = "hop"
    cfg["routing"]["learning_enabled"] = True
    cfg["routing"]["contract"] = contract
    cfg["learning"]["algorithm"] = "ddqn"
    cfg["learning"]["mode"] = "train"
    cfg["learning"]["seed"] = int(train_seed)
    cell_dir = out_root / f"{contract}-k{vis_k}-s{train_seed}"
    cell_dir.mkdir(parents=True, exist_ok=True)
    tmp_cfg = cell_dir / "cell-config.yaml"
    tmp_cfg.write_text(_dump_yaml(cfg), encoding="utf-8")
    cmd = [python, "-B", "-m", "CODE.leo_sim", "run",
           "--config", str(tmp_cfg), "--out", str(cell_dir / "out")]
    proc = subprocess.run(cmd, cwd=worktree, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"cell {contract}/k{vis_k}/s{train_seed} failed rc={proc.returncode}: "
            f"{proc.stdout[-800:]}{proc.stderr[-800:]}")
    return _analyze(cell_dir / "out")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--worktree", required=True, type=Path)
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--contracts", required=True, help="comma-separated")
    ap.add_argument("--vis-k", required=True, help="comma-separated hop values")
    ap.add_argument("--offered-mbps", type=float, required=True)
    ap.add_argument("--train-seeds", required=True, help="comma-separated")
    ap.add_argument("--traffic-seed", type=int, required=True)
    ap.add_argument("--duration-s", type=float, default=60.0)
    ap.add_argument("--obs-hops", type=int, default=None,
                    help="observation aggregation hops (default: vis_k)")
    ap.add_argument("--python", default=sys.executable)
    args = ap.parse_args()

    worktree = args.worktree.resolve()
    config_mod = _load_config_mod(worktree)
    out_root = args.out.resolve()
    out_root.mkdir(parents=True, exist_ok=True)
    summary_path = out_root / "matrix-summary.json"
    summary = {"traffic_seed": args.traffic_seed,
               "offered_mbps": args.offered_mbps,
               "duration_s": args.duration_s, "cells": {}}
    if summary_path.is_file():
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
    for contract in args.contracts.split(","):
        for vis_k in [int(x) for x in args.vis_k.split(",")]:
            for train_seed in [int(x) for x in args.train_seeds.split(",")]:
                key = f"{contract}|k{vis_k}|s{train_seed}"
                try:
                    metrics = _run_cell(
                        worktree, config_mod, args.config, out_root,
                        args.python, contract=contract, vis_k=vis_k,
                        train_seed=train_seed, traffic_seed=args.traffic_seed,
                        offered_mbps=args.offered_mbps,
                        duration_s=args.duration_s, obs_hops=args.obs_hops)
                    summary["cells"][key] = metrics
                    print(f"{key}: completion={metrics['completion_ratio']} "
                          f"mean={metrics['mean_latency_s']} "
                          f"p95={metrics['p95_latency_s']} "
                          f"train={metrics['train_steps']} "
                          f"verified={metrics['checkpoint_verified']} "
                          f"end={metrics['natural_end']}")
                except Exception as exc:
                    summary["cells"][key] = {"error": str(exc)[-500:]}
                    print(f"{key}: FAILED -> {str(exc)[-300:]}")
                summary_path.write_text(
                    json.dumps(summary, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")
    print(f"summary -> {summary_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
