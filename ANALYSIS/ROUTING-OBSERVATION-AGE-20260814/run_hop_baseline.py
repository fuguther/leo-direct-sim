#!/usr/bin/env python3
"""Non-learning hop baseline at the formal traffic seeds, for the
'learning arm < hop arm => learning failure' check.

Reuses the same 140-star cross-ocean hop profile as E0 but overrides
scenario.seed to the formal traffic seeds {101, 102}, so the comparison is
paired on identical traffic.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "CODE"))


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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--worktree", required=True, type=Path)
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--levels", required=True)
    ap.add_argument("--seeds", required=True)
    ap.add_argument("--python", default=sys.executable)
    args = ap.parse_args()

    from leo_sim import config as cfgmod

    base = cfgmod.load_config_file(args.config)["config"]
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    summary = {}
    for seed in [int(x) for x in args.seeds.split(",")]:
        for level in [float(x) for x in args.levels.split(",")]:
            c = json.loads(json.dumps(base))
            c["scenario"]["seed"] = seed
            c["scenario"]["duration_s"] = 60
            c["demand"]["offered_mbps"] = level
            c["routing"]["policy"] = "hop"
            c["learning"]["algorithm"] = "none"
            d = out / f"seed{seed}" / f"level-{level:g}"
            d.mkdir(parents=True, exist_ok=True)
            (d / "cfg.yaml").write_text(_dump_yaml(c), encoding="utf-8")
            cmd = [args.python, "-B", "-m", "CODE.leo_sim", "run",
                   "--config", str(d / "cfg.yaml"), "--out", str(d / "out")]
            p = subprocess.run(cmd, cwd=args.worktree, capture_output=True, text=True)
            if p.returncode != 0:
                summary[f"{seed}|{level:g}"] = {"error": p.stdout[-300:]}
                print(f"seed{seed} level{level:g}: FAILED {p.stdout[-200:]}", flush=True)
                continue
            led = json.loads((d / "out" / "ledgers.json").read_text())
            tr = []
            with (d / "out" / "trace.csv").open() as fh:
                hdr = fh.readline().strip().split(",")
                for line in fh:
                    tr.append(dict(zip(hdr, line.strip().split(","))))
            n_off = len(tr)
            n_del = len(led.get("deliveries", {}))
            summary[f"{seed}|{level:g}"] = {
                "completion_ratio": round(n_del / n_off, 4) if n_off else None,
                "natural_end": True,
            }
            print(f"seed{seed} level{level:g}: completion={summary[f'{seed}|{level:g}']['completion_ratio']}",
                  flush=True)
            (out / "summary.json").write_text(
                json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(f"summary -> {out / 'summary.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
