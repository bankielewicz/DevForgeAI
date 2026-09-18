"""Synthetic unit fixtures test evidence reduction, never counted as real trial logs."""
import hashlib
import importlib.util
from pathlib import Path
import unittest
import tempfile

spec = importlib.util.spec_from_file_location('helper_reducer', Path(__file__).with_name('reduce.py'))
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)


class ReducerTests(unittest.TestCase):
    def test_distinct_passes(self):
        text = 'test_a (fixture.Case) ... ok\ntest_b (fixture.Case) ... ok\nRan 2 tests in 0.1s\n\nOK\n'
        self.assertEqual({'passed': 2, 'required': 2}, r.grade_execution({'exit_code': 0}, text, 2))

    def test_duplicate_cases_cannot_inflate_denominator(self):
        text = 'test_a (fixture.Case) ... ok\ntest_a (fixture.Case) ... ok\nRan 2 tests in 0.1s\n\nOK\n'
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            r.grade_execution({'exit_code': 0}, text, 2)

    def test_failure_and_skips_are_not_passes(self):
        for state in ('FAIL', 'ERROR', 'skipped reason'):
            text = f'test_a (fixture.Case) ... {state}\nRan 1 test in 0.1s\n\nOK\n'
            with self.subTest(state=state), self.assertRaises(ValueError):
                r.grade_execution({'exit_code': 0}, text, 1)

    def test_nonzero_exit_and_wrong_count_rejected(self):
        text = 'test_a (fixture.Case) ... ok\nRan 1 test in 0.1s\n\nOK\n'
        for receipt, count in (({'exit_code': 1}, 1), ({'exit_code': 0}, 2)):
            with self.subTest(receipt=receipt, count=count), self.assertRaises(ValueError):
                r.grade_execution(receipt, text, count)

    def test_bound_bytes_accept_exact_digest(self):
        with tempfile.TemporaryDirectory() as name:
            p = Path(name) / 'receipt.json'
            p.write_bytes(b'original')
            ref = {'path': str(p), 'sha256': hashlib.sha256(b'original').hexdigest()}
            self.assertEqual(b'original', r.bound_bytes(ref))

    def test_changed_receipt_digest_rejected(self):
        with tempfile.TemporaryDirectory() as name:
            p = Path(name) / 'receipt.json'
            p.write_bytes(b'changed')
            ref = {'path': str(p), 'sha256': hashlib.sha256(b'original').hexdigest()}
            with self.assertRaisesRegex(ValueError, 'digest'):
                r.bound_bytes(ref)

    def test_coverage_exact_floor_and_missing_measurements(self):
        expected = {'file': 'helper.py', 'total_statements': 100, 'minimum_line_percent': 95}
        summary = {'excluded_lines': 0, 'num_statements': 100, 'covered_lines': 95, 'covered_branches': 9, 'num_branches': 10}
        value = {'summary': summary, 'executed_lines': list(range(1, 96)), 'missing_lines': list(range(96, 101))}
        self.assertEqual(95, r.grade_coverage({'files': {'helper.py': value}}, expected)['line_percent'])
        summary['covered_lines'] = 94
        value['executed_lines'] = list(range(1, 95))
        value['missing_lines'] = list(range(95, 101))
        with self.assertRaisesRegex(ValueError, 'below'):
            r.grade_coverage({'files': {'helper.py': value}}, expected)
        summary['excluded_lines'] = 1
        with self.assertRaisesRegex(ValueError, 'denominator/exclusion'):
            r.grade_coverage({'files': {'helper.py': value}}, expected)

    def test_package_binding_includes_added_files(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            (root / 'SKILL.md').write_bytes(b'fixture')
            before = r.package_rows(root)
            (root / 'extra').write_bytes(b'unbound')
            self.assertNotEqual(before, r.package_rows(root))


if __name__ == '__main__':
    unittest.main()
