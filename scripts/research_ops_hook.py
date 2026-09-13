#!/usr/bin/env python3
"""Opt-in CC PreToolUse gate. Local attestations, not a security boundary.

Unbound sessions pass through. Stop is deliberately not intercepted.
"""
import argparse
import json
from pathlib import Path
import sys

from research_ops import Invalid, Store, digest, require


def decide(payload, bindings_path):
    if payload.get("hook_event_name") != "PreToolUse" or payload.get("tool_name") != "update_goal":
        return
    if payload.get("tool_input", {}).get("action") != "complete":
        return
    bindings = json.loads(Path(bindings_path).read_text())
    binding = bindings.get("sessions", {}).get(payload.get("session_id"))
    if not binding:
        return
    require(Path(payload.get("cwd", ".")).resolve() == Path(binding["cwd"]).resolve(), "bound session cwd mismatch")
    store = Store(binding["store"])
    require((store.root / "state.json").is_file(), "bound store missing")
    with store.lock():
        state = store.read()
        store.validate(state)
        store.verify_blobs(state)
        task = state["tasks"].get(binding["task_id"])
        require(task and task["worker_session"] == payload["session_id"], "task/session mismatch")
        require(task["execution"] == "delivered", "submit artifact receipt before completing execution")
        require(task["currency"] == "current", "task evidence needs recheck")
        require(task["review"] in {"accept", "reject", "revise", "unavailable"}, "record review outcome (including reject/unavailable) before completing execution")
        require(digest(Path(task["artifact_path"]).read_bytes()) == task["artifact_sha256"], "delivered artifact changed")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bindings", required=True)
    args = parser.parse_args()
    try:
        decide(json.load(sys.stdin), args.bindings)
        print("{}")
    except (Invalid, OSError, KeyError, TypeError, AttributeError, json.JSONDecodeError) as exc:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                                "permissionDecisionReason": str(exc)}}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
