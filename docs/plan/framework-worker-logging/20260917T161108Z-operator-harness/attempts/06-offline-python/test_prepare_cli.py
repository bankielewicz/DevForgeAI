"""Real preparation CLI contract; never select native dispatch."""
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

TRIAL = Path(r"C:\Projects\DevForgeAI\docs\plan\framework-worker-trials\20260917T122229Z-logging-diagnostic")


class PreparationCliTests(unittest.TestCase):
    def test_prepare_emits_bound_packet_without_native_dispatch(self):
        self.assertFalse((TRIAL / "native-001").exists())
        self.assertFalse((TRIAL / "launch-invocation.json").exists())
        child = subprocess.run([sys.executable, "-B", "-X", "utf8",
                                os.environ["HARNESS_UNDER_TEST"], "--prepare"],
                               cwd=TRIAL, stdin=subprocess.DEVNULL,
                               capture_output=True, timeout=45)
        self.assertEqual(0, child.returncode, child.stderr.decode("utf-8", errors="replace"))
        records = [json.loads(line) for line in child.stdout.splitlines() if line.startswith(b"{")]
        ready = [record for record in records if record.get("stage") == "PREPARED"]
        self.assertEqual(1, len(ready), "Preparation must produce a concrete bound packet, not exit silently")
        self.assertEqual(0, ready[0]["native_preflight_invocations"])
        packet = Path(ready[0]["packet"])
        for name in ("request.json", "review.json", "diagnostics.json", "input-manifest.json"):
            self.assertTrue((packet / name).is_file(), name)
        self.assertFalse((TRIAL / "native-001").exists())
        self.assertFalse((TRIAL / "launch-invocation.json").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
