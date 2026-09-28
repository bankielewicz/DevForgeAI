"""Provider-specific regression checks; these do not execute the skill model."""
import importlib.util
from pathlib import Path
import subprocess
import re
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
PLUGIN = Path(__file__).resolve().parents[1]
SCRIPT = PLUGIN / "skills/brainstorm/scripts/validate_brn.py"
spec = importlib.util.spec_from_file_location("brainstorm_validator", SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
seed = (PLUGIN / "evals/brainstorm/existing-brn/scaffold.sh").read_text(encoding="utf-8")
LEGACY = seed.split("<<'BRN'\n", 1)[1].rsplit("\nBRN", 1)[0] + "\n"
VALID = LEGACY.replace('"claude-code"', '"codex"').replace(
    '| claude-code | Initial draft |', '| codex (session fixture-session) | Initial draft |')


class CodexProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="brainstorm-port-test-")
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "docs/specs/brainstorm/BRN-001.md"
        self.path.parent.mkdir(parents=True)

    def check(self, text):
        self.path.write_text(text, encoding="utf-8")
        return validator.check(str(self.path))

    def test_valid_codex_session(self):
        self.assertEqual(self.check(VALID), [])

    def test_wrong_session_is_rejected(self):
        errors = self.check(VALID.replace('codex (session fixture-session)', 'codex (session different-session)'))
        self.assertTrue(any('session must match' in message for _, message in errors), errors)

    def test_missing_session_in_codex_author_is_rejected(self):
        errors = self.check(VALID.replace('codex (session fixture-session)', 'codex'))
        self.assertTrue(any('author must be' in message for _, message in errors), errors)

    def test_agent_must_match_generated_by_tool(self):
        errors = self.check(VALID.replace('codex (session fixture-session)', 'claude-code (session fixture-session)'))
        self.assertTrue(any('agent must match' in message for _, message in errors), errors)

    def test_extension_preserves_old_claude_row(self):
        text = LEGACY.replace('version: 1', 'version: 2').replace('tool: "claude-code"', 'tool: "codex"')
        text = text.replace('"fixture-session"', '"extending-session"')
        text += '| 2 | 2026-09-27 | codex (session extending-session) | Extended without altering history |\n'
        self.assertIn('| 1 | 2026-09-01 | claude-code | Initial draft |', text)
        self.assertEqual(self.check(text), [])

    def test_valid_claude_latest_row_remains_readable(self):
        text = LEGACY.replace('| claude-code | Initial draft |',
                              '| claude-code (session fixture-session) | Initial draft |')
        self.assertEqual(self.check(text), [])

    def test_unresolved_environment_variable_is_rejected(self):
        errors = self.check(VALID.replace('session: "fixture-session"', 'session: "${CODEX_THREAD_ID}"'))
        self.assertTrue(any('generated_by.session must be' in message for _, message in errors), errors)

    def test_cli_works_without_site_packages(self):
        for text, expected in [(VALID, 0), (VALID.replace('codex (session fixture-session)',
                                                        'codex (session mismatched)'), 1)]:
            with self.subTest(expected_exit=expected):
                self.path.write_text(text, encoding="utf-8")
                result = subprocess.run([sys.executable, '-B', '-S', str(SCRIPT), str(self.path)],
                                        capture_output=True, text=True, check=False)
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)


    def test_existing_brn_grader_matches_historical_fixture(self):
        grader = PLUGIN / 'evals/brainstorm/existing-brn/graders/brn-001-unchanged.md'
        pattern = grader.read_text().split('---', 2)[2].strip()
        self.assertIsNotNone(re.search(pattern, LEGACY))

    def test_unknown_model_or_session_is_not_complete_provenance(self):
        grader = PLUGIN / 'evals/brainstorm/records-provenance/graders/session-substituted.md'
        pattern = grader.read_text().split('---', 2)[2].strip()
        self.assertIsNone(re.search(pattern, VALID))
        for old in ['model: "claude-opus-5-5"', 'session: "fixture-session"']:
            with self.subTest(field=old.split(':')[0]):
                self.assertIsNotNone(re.search(pattern, VALID.replace(old, old.split(':')[0] + ': "unknown"')))


if __name__ == '__main__':
    unittest.main()
