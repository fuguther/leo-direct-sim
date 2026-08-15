#!/usr/bin/env python3
"""Analyze run_formal_exp.py output: paired comparisons + bootstrap CIs.

Primary metric = eval completion ratio (epsilon=0, loaded checkpoint), averaged
over eval seeds. Paired unit = (train_seed x traffic_seed). Bootstrap 95% CI on
the paired difference; a direction call requires >=2/3 cells same sign AND the
CI excluding 0 (per 09/08 experiment protocol).
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np


def _cell_eval_mean(cell: dict) -> float | None:
    evs = cell.get("eval") or []
    if not evs:
        return None
    vals = [e["completion_ratio"] for e in evs if e.get("completion_ratio") is not None]
    if not vals:
        return None
    return float(np.mean(vals))


def _paired_diff(a: list[float], b: list[float]) -> tuple[float, float, float, int]:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    d = a - b
    rng = np.random.default_rng(0)
    boots = [np.mean(rng.choice(d, size=n, replace=True)) for _ in range(10000)]
    lo, hi = np.percentile(boots, [2.5, 97.5])
    same = int(np.sum(np.sign(d) == np.sign(np.median(d))))
    return float(np.median(d)), float(lo), float(hi), same


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary", required=True, type=Path)
    ap.add_argument("--group-by", default="obs_hops")
    ap.add_argument("--metric", default="eval_completion")
    args = ap.parse_args()

    data = json.loads(args.summary.read_text(encoding="utf-8"))
    cells = data.get("cells", {})
    groups: dict[str, dict] = {}
    for key, cell in cells.items():
        if "error" in cell:
            continue
        g = cell.get(args.group_by)
        if g is None:
            continue
        level = cell.get("offered_mbps")
        v = _cell_eval_mean(cell) if args.metric == "eval_completion" else cell["train"].get("completion_ratio")
        if v is None:
            continue
        pair_key = (cell.get("train_seed"), cell.get("traffic_seed"))
        groups.setdefault(g, {}).setdefault(level, {})[pair_key] = v

    print("=== per-group eval completion (mean over cells, by level) ===")
    for g in sorted(groups, key=lambda x: float(x)):
        for level in sorted(groups[g], key=float):
            vals = list(groups[g][level].values())
            print(f"  {args.group_by}={g} level={level:g}: "
                  f"n={len(vals)} mean={np.mean(vals):.4f} "
                  f"min={np.min(vals):.4f} max={np.max(vals):.4f}")

    print("=== paired comparisons (median diff + bootstrap 95% CI) ===")
    keys = sorted(groups, key=lambda x: float(x))
    for i in range(len(keys) - 1):
        ga, gb = keys[i], keys[i + 1]
        for level in sorted(set(groups[ga]) & set(groups[gb]), key=float):
            common = sorted(set(groups[ga][level]) & set(groups[gb][level]))
            a = [groups[ga][level][k] for k in common]
            b = [groups[gb][level][k] for k in common]
            if len(a) < 2 or len(b) < 2:
                print(f"  {ga} vs {gb} @ {level:g}: insufficient cells "
                      f"(n={len(a)} vs {len(b)})")
                continue
            med, lo, hi, same = _paired_diff(a, b)
            call = "SIGNIFICANT" if (lo > 0 or hi < 0) else "not-significant"
            print(f"  {ga} vs {gb} @ {level:g}: med={med:+.4f} "
                  f"CI=[{lo:+.4f},{hi:+.4f}] {call} "
                  f"same_sign={same}/{min(len(a),len(b))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
