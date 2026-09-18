"""Synthetic unit fixtures test evidence reduction, never counted as real trial logs."""
import hashlib
import importlib.util
from pathlib import Path
import unittest

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


if __name__ == '__main__':
    unittest.main()
