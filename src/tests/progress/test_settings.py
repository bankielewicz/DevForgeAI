"""Tests for SPEC-013's progress settings script (src/claude/DevForgeAI/progress/settings.py).

ModeRules checks IF-01 (VER-02) and SetModeRules checks IF-02 (VER-03), both against BEH-18's reading of the
local preference file (ADR-003 A3). The *UnderS classes run every test with the script under `python3 -S`
(QR-04). The script runs as a separate process, as its contract is exit codes, stdout, stderr and a file;
every spawn uses -B, so no __pycache__ lands in the plugin folder, which deploys.

Run from the repository root:
    PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -p no:cacheprovider src/tests/progress
"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SETTINGS = ROOT / "src/claude/DevForgeAI/progress/settings.py"
LOCAL = Path(".claude/devforgeai.local.md")
IGNORED = "ignored .claude/devforgeai.local.md progress.mode ("


class Base(unittest.TestCase):
    INTERPRETER = (sys.executable, "-B")

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def run_settings(self, *args):
        return subprocess.run(list(self.INTERPRETER) + [str(SETTINGS)] + [str(a) for a in args], cwd=ROOT,
                              capture_output=True, text=True)

    def write_local(self, text):
        path = self.root / LOCAL
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))
        return path

    def mode(self):
        return self.run_settings("mode", "--root", self.root)

    def set_mode(self, value):
        return self.run_settings("set-mode", "--root", self.root, "--value", value)

    def files(self):
        return sorted(str(p.relative_to(self.root)) for p in self.root.rglob("*"))


class ModeRules(Base):
    """VER-02: IF-01 resolves progress.mode from the local preference file or the framework default."""

    def assert_mode(self, proc, line, ignored=None):
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stdout, line + "\n")
        if ignored is None:
            self.assertEqual(proc.stderr, "")
        else:
            self.assertEqual(proc.stderr, IGNORED + ignored + ")\n")

    def test_no_file_is_the_framework_default(self):
        self.assert_mode(self.mode(), "observe framework-default")

    def test_enforce_from_the_local_file(self):
        self.write_local("---\ndevforgeai_local: 1\nprogress.mode: enforce\n---\n")
        self.assert_mode(self.mode(), "enforce local")

    def test_observe_from_the_local_file(self):
        self.write_local("---\ndevforgeai_local: 1\nprogress.mode: observe\n---\n")
        self.assert_mode(self.mode(), "observe local")

    def test_quoted_values_count(self):
        self.write_local("---\ndevforgeai_local: 1\nprogress.mode: \"enforce\"\n---\n")
        self.assert_mode(self.mode(), "enforce local")
        self.write_local("---\ndevforgeai_local: '1'\nprogress.mode: 'enforce'\n---\n")
        self.assert_mode(self.mode(), "enforce local")

    def test_other_entries_are_left_to_the_skills(self):
        self.write_local("---\ndevforgeai_local: 1\ninterview.max_calls: 5\nprogress.mode: enforce\n---\n")
        self.assert_mode(self.mode(), "enforce local")

    def test_no_progress_entry_is_the_default_with_nothing_reported(self):
        self.write_local("---\ndevforgeai_local: 1\ninterview.max_calls: 5\n---\n")
        self.assert_mode(self.mode(), "observe framework-default")

    def test_a_bad_value_is_ignored_and_reported(self):
        self.write_local("---\ndevforgeai_local: 1\nprogress.mode: strict\n---\n")
        self.assert_mode(self.mode(), "observe framework-default", "'strict' is not observe or enforce")

    def test_a_missing_format_version_is_ignored_and_reported(self):
        self.write_local("---\nprogress.mode: enforce\n---\n")
        self.assert_mode(self.mode(), "observe framework-default", "devforgeai_local is not 1")
        self.write_local("---\ndevforgeai_local: 2\nprogress.mode: enforce\n---\n")
        self.assert_mode(self.mode(), "observe framework-default", "devforgeai_local is not 1")

    def test_text_after_the_frontmatter_is_ignored_and_reported(self):
        self.write_local("---\ndevforgeai_local: 1\nprogress.mode: enforce\n---\nnotes\n")
        self.assert_mode(self.mode(), "observe framework-default", "the file isn't frontmatter-only")
        self.write_local("devforgeai_local: 1\nprogress.mode: enforce\n")
        self.assert_mode(self.mode(), "observe framework-default", "the file isn't frontmatter-only")

    def test_blank_lines_after_the_frontmatter_are_allowed(self):
        self.write_local("---\ndevforgeai_local: 1\nprogress.mode: enforce\n---\n\n\n")
        self.assert_mode(self.mode(), "enforce local")

    def test_a_root_that_is_not_a_folder_exits_2(self):
        proc = self.run_settings("mode", "--root", self.root / "missing")
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(proc.stdout, "")
        self.assertIn("missing", proc.stderr)
        self.assertEqual(len(proc.stderr.splitlines()), 1)

    def test_mode_writes_nothing(self):
        self.write_local("---\ndevforgeai_local: 1\nprogress.mode: enforce\n---\n")
        before = self.files()
        self.mode()
        self.assertEqual(self.files(), before)


class SetModeRules(Base):
    """VER-03: IF-02 saves the user's choice, keeping the rest of the file as it was."""

    def assert_saved(self, proc, value):
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stdout, "saved progress.mode=%s to .claude/devforgeai.local.md\n" % value)
        self.assertEqual(proc.stderr, "")

    def local_text(self):
        return (self.root / LOCAL).read_bytes().decode("utf-8")

    def test_creates_the_folder_and_the_file(self):
        self.assert_saved(self.set_mode("enforce"), "enforce")
        self.assertEqual(self.local_text(), "---\ndevforgeai_local: 1\nprogress.mode: enforce\n---\n")
        self.assertEqual(self.files(), [".claude", ".claude/devforgeai.local.md"])

    def test_replaces_the_entry_and_keeps_every_other_line(self):
        self.write_local("---\ndevforgeai_local: 1\n# my settings\ninterview.max_calls: 5\n"
                         "progress.mode: enforce\nprd.style: \"short\"\n---\n")
        self.assert_saved(self.set_mode("observe"), "observe")
        self.assertEqual(self.local_text(), "---\ndevforgeai_local: 1\n# my settings\ninterview.max_calls: 5\n"
                                            "progress.mode: observe\nprd.style: \"short\"\n---\n")

    def test_adds_the_entry_before_the_closing_line(self):
        self.write_local("---\ndevforgeai_local: 1\ninterview.max_calls: 5\n---\n")
        self.assert_saved(self.set_mode("enforce"), "enforce")
        self.assertEqual(self.local_text(),
                         "---\ndevforgeai_local: 1\ninterview.max_calls: 5\nprogress.mode: enforce\n---\n")

    def test_adds_the_format_version_when_it_is_missing(self):
        self.write_local("---\ninterview.max_calls: 5\n---\n")
        self.assert_saved(self.set_mode("enforce"), "enforce")
        self.assertEqual(self.local_text(),
                         "---\ndevforgeai_local: 1\ninterview.max_calls: 5\nprogress.mode: enforce\n---\n")
        self.assertEqual(self.mode().stdout, "enforce local\n")

    def test_keeps_crlf_line_endings(self):
        self.write_local("---\r\ndevforgeai_local: 1\r\nprogress.mode: observe\r\n---\r\n")
        self.assert_saved(self.set_mode("enforce"), "enforce")
        self.assertEqual(self.local_text(), "---\r\ndevforgeai_local: 1\r\nprogress.mode: enforce\r\n---\r\n")

    def test_refuses_a_file_that_is_not_frontmatter_only(self):
        original = "---\ndevforgeai_local: 1\nprogress.mode: observe\n---\nnotes\n"
        path = self.write_local(original)
        proc = self.set_mode("enforce")
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(proc.stdout, "")
        self.assertEqual(len(proc.stderr.splitlines()), 1)
        self.assertEqual(path.read_bytes(), original.encode("utf-8"))

    def test_refuses_another_format_version(self):
        original = "---\ndevforgeai_local: 2\nprogress.mode: observe\n---\n"
        path = self.write_local(original)
        proc = self.set_mode("enforce")
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(path.read_bytes(), original.encode("utf-8"))

    def test_rejects_a_value_other_than_observe_or_enforce(self):
        proc = self.set_mode("strict")
        self.assertEqual(proc.returncode, 2)
        self.assertFalse((self.root / LOCAL).exists())

    def test_leaves_no_temporary_file(self):
        self.write_local("---\ndevforgeai_local: 1\n---\n")
        self.assert_saved(self.set_mode("enforce"), "enforce")
        self.assertEqual(self.files(), [".claude", ".claude/devforgeai.local.md"])

    def test_keeps_the_file_permissions(self):
        path = self.write_local("---\ndevforgeai_local: 1\n---\n")
        path.chmod(0o644)
        self.assert_saved(self.set_mode("enforce"), "enforce")
        self.assertEqual(path.stat().st_mode & 0o777, 0o644)
        path.chmod(0o640)
        self.assert_saved(self.set_mode("observe"), "observe")
        self.assertEqual(path.stat().st_mode & 0o777, 0o640)

    def test_a_new_file_is_readable_by_others_as_usual(self):
        self.assert_saved(self.set_mode("enforce"), "enforce")
        self.assertEqual((self.root / LOCAL).stat().st_mode & 0o777, 0o644)

    def test_an_empty_file_is_set_up(self):
        self.write_local("")
        self.assert_saved(self.set_mode("enforce"), "enforce")
        self.assertEqual(self.local_text(), "---\ndevforgeai_local: 1\nprogress.mode: enforce\n---\n")

    def test_a_byte_order_mark_is_read_past(self):
        self.write_local("\ufeff---\ndevforgeai_local: 1\nprogress.mode: observe\n---\n")
        self.assertEqual(self.mode().stdout, "observe local\n")
        self.assert_saved(self.set_mode("enforce"), "enforce")
        self.assertEqual(self.local_text(), "---\ndevforgeai_local: 1\nprogress.mode: enforce\n---\n")

    def test_a_root_that_is_not_a_folder_exits_2(self):
        proc = self.set_mode_in(self.root / "missing", "enforce")
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(len(proc.stderr.splitlines()), 1)

    def set_mode_in(self, root, value):
        return self.run_settings("set-mode", "--root", root, "--value", value)


class ModeRulesUnderS(ModeRules):
    INTERPRETER = (sys.executable, "-S", "-B")


class SetModeRulesUnderS(SetModeRules):
    INTERPRETER = (sys.executable, "-S", "-B")


if __name__ == "__main__":
    unittest.main()
