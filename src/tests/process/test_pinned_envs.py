"""The helper that finds the pinned jsonschema environments (#122, #155).

Run from the repository root:

    PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -p no:cacheprovider src/tests/process
"""
import importlib.util
import subprocess
import unittest
from pathlib import Path
from unittest import mock

HELPER = Path(__file__).with_name("pinned_envs.py")
ROOT = Path(__file__).resolve().parents[3]


def load():
    spec = importlib.util.spec_from_file_location("pinned_envs_under_test", HELPER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PinnedEnvs(unittest.TestCase):
    def test_the_environments_are_under_tmp_test_envs(self):
        path = load().python("4.10.3")
        self.assertEqual(path.parts[-5:], ("tmp", "test-envs", "jsonschema-4.10.3", "bin", "python"))

    def test_no_git_falls_back_to_this_checkout(self):
        """Without git on PATH the helper must not raise at import, which would error the whole test file."""
        envs = load()
        with mock.patch.object(envs.subprocess, "run", side_effect=FileNotFoundError("git")):
            self.assertEqual(envs.base(), ROOT)

    def test_a_failing_git_falls_back_to_this_checkout(self):
        envs = load()
        failed = subprocess.CompletedProcess(["git"], 128, stdout="", stderr="not a git repository")
        with mock.patch.object(envs.subprocess, "run", return_value=failed):
            self.assertEqual(envs.base(), ROOT)

    def test_both_test_files_use_the_helper(self):
        for name in ("context/test_context_check.py", "prd/test_validate_policy.py"):
            with self.subTest(file=name):
                text = (ROOT / "src/tests" / name).read_text()
                self.assertIn("pinned_envs.py", text)
                self.assertNotIn("def _pinned_python", text)


if __name__ == "__main__":
    unittest.main()
