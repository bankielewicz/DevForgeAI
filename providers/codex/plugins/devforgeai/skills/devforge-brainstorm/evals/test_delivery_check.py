"""Independent mechanical fixtures; test artifacts belong in the run workspace."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('delivery_check', Path(__file__).parents[1] / 'scripts/delivery_check.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class DeliveryChecks(unittest.TestCase):
    def test_vocabulary(self):
        for value in ('PASS', 'FAIL', 'NOT_RUN', 'COULD_NOT_RUN', 'NOT_APPLICABLE'):
            with self.subTest(value=value):
                self.assertEqual(checker.outcomes('| Check | Outcome | Evidence |\n| --- | --- | --- |\n| Receipt | '+value+' | Detail |')['result'], 'PASS')
        for value in ('Recorded externally', 'PASS later', '', 'pass'):
            with self.subTest(value=value):
                self.assertEqual(checker.outcomes('| Check | Outcome | Evidence |\n| --- | --- | --- |\n| Receipt | '+value+' | Detail |')['result'], 'FAIL')

    def test_missing_pending_completed_and_digest(self):
        with tempfile.TemporaryDirectory() as folder:
            project = Path(folder)
            handoff = project / 'handoff.md'
            handoff.write_text('| Check | Outcome | Evidence |\n| --- | --- | --- |\n| Receipt | NOT_RUN | Planned after this save |\n')
            receipt = project / 'receipt.json'
            code, result = checker.check(project, handoff)
            self.assertEqual((code, result['receipt_status'], result['semantic_claim_review']), (0, 'NOT_RUN', 'NOT_EVALUATED'))
            code, result = checker.check(project, handoff, receipt, [receipt])
            self.assertEqual((code, result['receipt_status'], result['files'][0]['result']), (1, 'FAIL', 'FAIL'))
            receipt.write_text(json.dumps({'files': [{'path': 'handoff.md', 'sha256': hashlib.sha256(handoff.read_bytes()).hexdigest()}]}))
            code, result = checker.check(project, handoff, receipt, [receipt])
            self.assertEqual((code, result['receipt_status']), (0, 'PASS'))
            unrelated = project / 'unrelated.txt'; unrelated.write_text('An unrelated file')
            receipt.write_text(json.dumps({'files': [{'path': 'unrelated.txt', 'sha256': hashlib.sha256(unrelated.read_bytes()).hexdigest()}]}))
            self.assertEqual(checker.check(project, handoff, receipt)[0], 1)
            receipt.write_text(json.dumps({'files': [{'path': 'handoff.md', 'sha256': hashlib.sha256(handoff.read_bytes()).hexdigest()}]}))
            handoff.write_text(handoff.read_text()+'Changed bytes\n')
            self.assertEqual(checker.check(project, handoff, receipt)[0], 1)

    def test_invalid_receipt_and_missing_table(self):
        with tempfile.TemporaryDirectory() as folder:
            project = Path(folder)
            handoff = project / 'handoff.md'; handoff.write_text('No check table')
            self.assertEqual(checker.check(project, handoff)[0], 1)
            receipt = project / 'receipt.json'; receipt.write_text('{')
            self.assertEqual(checker.check(project, handoff, receipt)[0], 2)
            self.assertEqual(checker.check(project, project / 'absent.md')[0], 2)


if __name__ == '__main__':
    unittest.main()
