import os
import subprocess
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "src" / "limit_cli.py"


class LimitCliTests(unittest.TestCase):
    def test_happy_path(self):
        environment = dict(os.environ, LIMIT="7")
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            capture_output=True,
            text=True,
            env=environment,
            check=False,
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "limit=7\n")
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
