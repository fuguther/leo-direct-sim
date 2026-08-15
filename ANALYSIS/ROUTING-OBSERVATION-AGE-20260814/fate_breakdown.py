#!/usr/bin/env python3
"""Aggregate fate counts per (contract, obs_hops, level) across eval seeds.

Uses Python glob so the `|` in cell directory names never goes through a shell.
Split loss into: delivered, access-side (ACCESS_REJECTED + ACCESS_QUEUE_OVERFLOW),
ISL-side (ISL_QUEUE_OVERFLOW + GEOMETRY/RANDOM loss), no-route, deadline, in-system.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


FATE_GROUPS = {
    "delivered": {"DELIVERED"},
    "access_loss": {"ACCESS_REJECTED", "ACCESS_QUEUE_OVERFLOW"},
    "isl_loss": {"ISL_QUEUE_OVERFLOW", "GEOMETRY_LOSS_IN_FLIGHT",
                 "RANDOM_OUTAGE_IN_FLIGHT"},
    "no_route": {"NO_ROUTE"},
    "deadline": {"DATA_DEADLINE_EXPIRED"},
    "in_system": {"IN_SYSTEM_AT_STOP"},
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, type=Path)
    args = ap.parse_args()

    agg = defaultdict(lambda: defaultdict(int))
    n_eval = defaultdict(int)
    for receipt in args.root.glob("*/eval-*/receipt.json"):
        cell = receipt.parents[1].name  # GAT|h1|m50|ts41|fs101
        parts = cell.split("|")
        key = (parts[0], parts[1], parts[2])  # contract, obs_hops, level
        r = json.loads(receipt.read_text(encoding="utf-8"))
        fc = r.get("fate_counts", {})
        if not fc:
            continue
        n_eval[key] += 1
        for fate, cnt in fc.items():
            for grp, names in FATE_GROUPS.items():
                if fate in names:
                    agg[key][grp] += int(cnt)
                    break

    for key in sorted(agg, key=lambda k: (k[0], int(k[1][1:]), float(k[2][1:]))):
        d = agg[key]
        total = sum(d.values())
        print(f"{key[0]} {key[1]} {key[2]}: n_eval={n_eval[key]} total={total}")
        for grp in FATE_GROUPS:
            c = d.get(grp, 0)
            pct = c / total * 100 if total else 0.0
            print(f"    {grp}: {c} ({pct:.1f}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
