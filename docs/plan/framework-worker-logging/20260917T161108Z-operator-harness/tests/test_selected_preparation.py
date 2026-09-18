"""Real retained-source regression; no native worker is executed."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import unittest

WORKSPACE = Path(r"C:\Projects\DevForgeAI")
TRIAL = WORKSPACE / "docs/plan/framework-worker-trials/20260917T122229Z-logging-diagnostic"


class SelectedPreparationTests(unittest.TestCase):
    def test_selected_current_sources_do_not_require_removed_historical_sites(self):
        config = json.loads((TRIAL / "operator-harness-001/configuration.json").read_text())
        inventory = json.loads(Path(config["approved_inventory"]["path"]).read_text())
        files = [entry for entry in inventory["entries"] if entry["state"] == "file"]
        self.assertEqual(26, len(files))
        # Establish the exact intended condition independently: every selected
        # current file exists and matches, but the historical package is gone.
        for entry in files:
            self.assertEqual(entry["sha256"], hashlib.sha256(Path(entry["path"]).read_bytes()).hexdigest())
        self.assertFalse(Path(r"C:\Users\bryan\.codex\plugins\cache\openai-curated-remote\sites\0.1.65").exists())
        target = Path(os.environ["HARNESS_UNDER_TEST"])
        spec = importlib.util.spec_from_file_location("selected_preparation_under_test", target)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        try:
            result = module.verify_preservation()
        except FileNotFoundError as error:
            self.fail("Preparation still requires a removed historical source despite valid current bindings: " + str(error))
        self.assertEqual(26, result["current_reviewed_files_hashed"])


if __name__ == "__main__":
    unittest.main()
