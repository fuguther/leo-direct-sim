#!/usr/bin/env python3
"""Formal experiment orchestrator: train + eval, parallel across train cells.

Runs on the VM (or any host with the leo_sim runtime). Each cell is
   train (learning.mode=train, one train_seed x one traffic_seed)
   -> eval  (learning.mode=eval, checkpoint loaded, epsilon=0, per eval seed)
Train cells run concurrently up to --max-workers; each finished train cell's
eval seeds run immediately. Results are written incrementally to
<out>/matrix-summary.json so a crash loses nothing already done.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


ACTIONS = ("deliver", "N", "S", "E", "W")


def _load_config_mod(worktree: Path):
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


def _emit(lines, key, value, indent):
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


def _run(worktree: Path, python: str, cfg: dict, out: Path):
    tmp = out / "resolved.yaml"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(_dump_yaml(cfg), encoding="utf-8")
    cmd = [python, "-B", "-m", "CODE.leo_sim", "run",
           "--config", str(tmp), "--out", str(out)]
    proc = subprocess.run(cmd, cwd=worktree, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"rc={proc.returncode}\nstdout={proc.stdout[-1500:]}\n"
            f"stderr={proc.stderr[-1500:]}")
    return out


def _metrics(run_dir: Path) -> dict:
    receipt = json.loads((run_dir / "receipt.json").read_text(encoding="utf-8"))
    ledgers = json.loads((run_dir / "ledgers.json").read_text(encoding="utf-8"))
    trace = []
    with (run_dir / "trace.csv").open(encoding="utf-8") as fh:
        header = fh.readline().strip().split(",")
        for line in fh:
            trace.append(dict(zip(header, line.strip().split(","))))
    emit = {int(r["packet_id"]): float(r["emit_time_s"]) for r in trace}
    deliveries = ledgers.get("deliveries", {})
    lats = [float(d["delivered_at"]) - emit[int(pid)]
            for pid, d in deliveries.items() if int(pid) in emit]
    fates = ledgers.get("packet_fates", {})
    n_off = len(trace)
    n_del = len(deliveries)
    n_sys = sum(1 for f in fates.values() if f[0] == "IN_SYSTEM_AT_STOP")
    lat = sorted(lats)
    p95 = lat[int(0.95 * len(lat)) - 1] if lat else None
    learning = ledgers.get("learning", {})
    return {
        "completion_ratio": round(n_del / n_off, 4) if n_off else None,
        "mean_latency_s": round(sum(lats) / len(lats), 4) if lats else None,
        "p95_latency_s": round(p95, 4) if p95 is not None else None,
        "in_system_ratio": round(n_sys / n_off, 4) if n_off else None,
        "conservation_ok": bool(receipt.get("conservation_ok")),
        "natural_end": bool(receipt.get("natural_end")),
        "train_steps": learning.get("train_steps"),
        "decisions": learning.get("decisions"),
        "last_loss": learning.get("last_loss"),
    }


def _build_cfg(config_mod, base_cfg: str, *, traffic_seed: int, duration_s: float,
               offered_mbps: float, vis_k: int, obs_hops: int, contract: str,
               mode: str, seed: int, checkpoint_path=None, checkpoint_sha256=None) -> dict:
    loaded = config_mod.load_config_file(base_cfg)
    cfg = json.loads(json.dumps(loaded["config"]))
    cfg["scenario"]["seed"] = int(traffic_seed)
    cfg["scenario"]["duration_s"] = float(duration_s)
    cfg["demand"]["offered_mbps"] = float(offered_mbps)
    cfg["control_plane"]["vis_k"] = int(vis_k)
    cfg["routing"]["policy"] = "hop"
    cfg["routing"]["learning_enabled"] = True
    cfg["routing"]["contract"] = contract
    cfg["learning"]["algorithm"] = "ddqn"
    cfg["learning"]["mode"] = mode
    cfg["learning"]["seed"] = int(seed)
    cfg["learning"]["obs_hops"] = int(obs_hops)
    cfg["learning"]["checkpoint_path"] = checkpoint_path
    cfg["learning"]["checkpoint_sha256"] = checkpoint_sha256
    return cfg


def _run_cell(worktree, config_mod, base_cfg, out_root, python, *, contract,
              obs_hops, offered_mbps, train_seed, traffic_seed, eval_seeds,
              train_dur, eval_dur, vis_k):
    key = (f"{contract}|h{obs_hops}|m{offered_mbps:g}|ts{train_seed}"
           f"|fs{traffic_seed}")
    cell = out_root / key
    train_cfg = _build_cfg(
        config_mod, base_cfg, traffic_seed=traffic_seed, duration_s=train_dur,
        offered_mbps=offered_mbps, vis_k=vis_k, obs_hops=obs_hops,
        contract=contract, mode="train", seed=train_seed)
    train_dir = cell / "train"
    _run(worktree, python, train_cfg, train_dir)
    ddqn_dir = train_dir / "ddqn"
    meta = json.loads((ddqn_dir / "metadata.json").read_text(encoding="utf-8"))
    ckpt = ddqn_dir / meta["checkpoint"]
    sha = meta["checkpoint_sha256"]
    train_metrics = _metrics(train_dir)
    evals = []
    for es in eval_seeds:
        eval_cfg = _build_cfg(
            config_mod, base_cfg, traffic_seed=traffic_seed, duration_s=eval_dur,
            offered_mbps=offered_mbps, vis_k=vis_k, obs_hops=obs_hops,
            contract=contract, mode="eval", seed=es,
            checkpoint_path=str(ckpt), checkpoint_sha256=sha)
        ev = cell / f"eval-{es}"
        _run(worktree, python, eval_cfg, ev)
        evals.append({"seed": es, **_metrics(ev)})
    return {
        "key": key,
        "contract": contract,
        "obs_hops": obs_hops,
        "offered_mbps": offered_mbps,
        "train_seed": train_seed,
        "traffic_seed": traffic_seed,
        "train": train_metrics,
        "eval": evals,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--worktree", required=True, type=Path)
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--contracts", required=True)
    ap.add_argument("--obs-hops", required=True)
    ap.add_argument("--levels", required=True, help="offered_mbps list")
    ap.add_argument("--train-seeds", required=True)
    ap.add_argument("--traffic-seeds", required=True)
    ap.add_argument("--eval-seeds", default="201,202,203")
    ap.add_argument("--vis-k", type=int, default=12)
    ap.add_argument("--train-dur", type=float, default=120.0)
    ap.add_argument("--eval-dur", type=float, default=60.0)
    ap.add_argument("--max-workers", type=int, default=8)
    ap.add_argument("--python", default=sys.executable)
    args = ap.parse_args()

    worktree = args.worktree.resolve()
    config_mod = _load_config_mod(worktree)
    out_root = args.out.resolve()
    out_root.mkdir(parents=True, exist_ok=True)
    summary_path = out_root / "matrix-summary.json"
    summary = {"cells": {}}
    if summary_path.is_file():
        summary = json.loads(summary_path.read_text(encoding="utf-8"))

    jobs = []
    for contract in args.contracts.split(","):
        for obs_hops in [int(x) for x in args.obs_hops.split(",")]:
            for level in [float(x) for x in args.levels.split(",")]:
                for ts in [int(x) for x in args.train_seeds.split(",")]:
                    for fs in [int(x) for x in args.traffic_seeds.split(",")]:
                        jobs.append((contract, obs_hops, level, ts, fs))

    def _wrap(job):
        contract, obs_hops, level, ts, fs = job
        key = f"{contract}|h{obs_hops}|m{level:g}|ts{ts}|fs{fs}"
        if key in summary["cells"] and "error" not in summary["cells"][key]:
            return None
        try:
            return _run_cell(
                worktree, config_mod, args.config, out_root, args.python,
                contract=contract, obs_hops=obs_hops, offered_mbps=level,
                train_seed=ts, traffic_seed=fs,
                eval_seeds=[int(x) for x in args.eval_seeds.split(",")],
                train_dur=args.train_dur, eval_dur=args.eval_dur,
                vis_k=args.vis_k)
        except Exception as exc:
            return {"key": key, "error": str(exc)[-1200:]}

    with ThreadPoolExecutor(max_workers=args.max_workers) as ex:
        futs = [ex.submit(_wrap, j) for j in jobs]
        for fut in as_completed(futs):
            r = fut.result()
            if r is None:
                continue
            summary["cells"][r["key"]] = r
            if "error" in r:
                print(f"{r['key']}: FAILED -> {r['error'][-300:]}", flush=True)
            else:
                m = r["train"]
                print(f"{r['key']}: train completion={m['completion_ratio']} "
                      f"train_steps={m['train_steps']} eval={len(r['eval'])} "
                      f"end={m['natural_end']}", flush=True)
            summary_path.write_text(
                json.dumps(summary, indent=2, sort_keys=True) + "\n",
                encoding="utf-8")
    print(f"summary -> {summary_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
