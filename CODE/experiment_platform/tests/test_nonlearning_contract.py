from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from CODE.experiment_platform.compile_experiment import arm_constraints, compile_request, load_json


class NonLearningContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.request_path = ROOT / "EXPERIMENTS" / "EXP-20260715-VM-SMOKE-R04" / "request.json"
        self.request = load_json(self.request_path)
        self.config = load_json(
            ROOT / "EXPERIMENTS" / "EXP-20260715-VM-SMOKE-R04" / "resolved" / "control.s20260715.config.json"
        )
        catalog = load_json(ROOT / "CODE" / "experiment_platform" / "parameter-catalog.json")
        self.specs = {item["path"]: item for item in catalog["parameters"]}

    def errors_for(self, config=None, arm=None) -> list[str]:
        errors, _warnings, _effective = arm_constraints(
            copy.deepcopy(config or self.config),
            copy.deepcopy(self.request),
            copy.deepcopy(arm or self.request["design"]["arms"][0]),
            self.specs,
        )
        return errors

    def test_r04_compiles_as_non_learning(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "experiment"
            self.assertEqual(compile_request(self.request_path, out), 0)
            manifest = json.loads((out / "run-manifest.json").read_text(encoding="utf-8"))
            self.assertTrue(all(row["run_phase"] == "non_learning" for row in manifest["planned_runs"]))
            self.assertTrue(all(row["checkpoint_lineage"]["mode"] == "not_applicable" for row in manifest["planned_runs"]))
            runbook = (out / "RUNBOOK.md").read_text(encoding="utf-8")
            self.assertIn("set -euo pipefail", runbook)
            self.assertIn("SECONDS + 900", runbook)
            self.assertIn("--launch-nonce", runbook)
            self.assertIn("--run-attempt-id", runbook)
            self.assertIn("verify-pulled-run.py", runbook)
            self.assertNotIn("while :", runbook)

    def test_non_learning_rejects_learning_identity_budget_eval_and_checkpoint(self) -> None:
        arm = copy.deepcopy(self.request["design"]["arms"][0])
        arm["execution_kind"] = "learning"
        self.assertTrue(any("execution_kind" in item for item in self.errors_for(arm=arm)))

        arm = copy.deepcopy(self.request["design"]["arms"][0])
        arm["checkpoint_lineage"]["mode"] = "new_training"
        self.assertTrue(any("not_applicable" in item for item in self.errors_for(arm=arm)))

        arm = copy.deepcopy(self.request["design"]["arms"][0])
        arm["training_budget"]["simulated_seconds"] = 0.3
        self.assertTrue(any("training_budget=0" in item for item in self.errors_for(arm=arm)))

        config = copy.deepcopy(self.config)
        config["routing"]["eval_only"] = True
        self.assertTrue(any("eval_only=false" in item for item in self.errors_for(config=config)))

        config = copy.deepcopy(self.config)
        config["checkpoint"]["path_credit_replay"] = "unexpected.npz"
        self.assertTrue(any("forbids checkpoint" in item for item in self.errors_for(config=config)))

    def test_q_learning_eval_only_is_explicitly_blocked(self) -> None:
        config = copy.deepcopy(self.config)
        config["simulation"]["pathing"] = "Q-Learning"
        config["routing"]["eval_only"] = True
        arm = copy.deepcopy(self.request["design"]["arms"][0])
        arm["execution_kind"] = "learning"
        arm["method_family"] = "q-learning"
        arm["checkpoint_lineage"]["mode"] = "evaluation_only"
        arm["checkpoint_lineage"]["source_run_id"] = "source"
        arm["checkpoint_lineage"]["source_sha256"] = "a" * 64
        arm["evaluation_budget"]["simulated_seconds"] = 0.3
        arm["execution_budget"]["simulated_seconds"] = 0
        self.assertTrue(any("Q-Learning evaluation-only" in item for item in self.errors_for(config=config, arm=arm)))

    def test_raac_rejects_fixed_multistep_until_action_masks_are_wired(self) -> None:
        config = copy.deepcopy(self.config)
        config["simulation"]["pathing"] = "Deep Q-Learning"
        config["state"] = {"mode": "c6", "vis_k": 2}
        config["credit"] = {"method": "nstep", "n": 3}
        arm = copy.deepcopy(self.request["design"]["arms"][0])
        arm["execution_kind"] = "learning"
        arm["method_family"] = "ddqn_nstep"
        arm["checkpoint_lineage"]["mode"] = "new_training"
        arm["training_budget"]["simulated_seconds"] = 0.3
        arm["execution_budget"]["simulated_seconds"] = 0
        self.assertTrue(any("next-action masks" in item for item in self.errors_for(config=config, arm=arm)))


if __name__ == "__main__":
    unittest.main()
