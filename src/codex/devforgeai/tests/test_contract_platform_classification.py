"""Platform interruptions must not become fabricated behavior judgments."""
import unittest
from summarize_contract_campaign import apply_native_boundary, case_status, native_classification


class PlatformClassificationTests(unittest.TestCase):
    def row(self, **updates):
        row = dict(attempt_state='SEALED', skill='prd', case='warns-unconverged', mode='default',
                   arm='plugin', semantic_pending=True, original_binary=False, corrected_binary=False,
                   original_source_score=0.5, corrected_source_score=0.5,
                   original_failed_checks=['partial'], corrected_failed_checks=['partial'],
                   failed_guards=[], strict_current_write=False)
        row.update(updates)
        return row

    def test_usage_limit_is_not_a_behavior_failure(self):
        row = apply_native_boundary(self.row(), {'status': 'failed', 'error': {'codexErrorInfo': 'usageLimitExceeded'}})
        self.assertEqual(row['behavior_status'], 'NOT_ASSESSED_PLATFORM_LIMIT')
        self.assertFalse(row['semantic_pending'])
        self.assertIsNone(row['corrected_source_score'])
        self.assertEqual(row['partial_artifact_diagnostics']['corrected_source_score'], 0.5)

    def test_completed_missing_semantic_review_stays_pending(self):
        row = apply_native_boundary(self.row(), {'status': 'completed'})
        self.assertEqual(row['behavior_status'], 'REVIEW_REQUIRED')
        self.assertTrue(row['semantic_pending'])

    def test_completed_failure_and_success_stay_assessed(self):
        for passed in (False, True):
            row = apply_native_boundary(self.row(semantic_pending=False, corrected_binary=passed), {'status': 'completed'})
            self.assertEqual(row['behavior_status'], 'PASS' if passed else 'FAIL')
            self.assertEqual(row['corrected_source_score'], 0.5)

    def test_only_declared_plan_question_checkpoint_is_assessable(self):
        task = self.row(skill='architecture', case='existing-arch-not-duplicated', mode='plan')
        self.assertEqual(native_classification(task, {'status': 'awaiting_input'}), 'EXPECTED_QUESTION_GATE')
        self.assertEqual(native_classification({**task, 'mode': 'default'}, {'status': 'awaiting_input'}), 'NATIVE_INTERRUPTION')

    def test_harness_failure_is_distinct_from_platform_limit(self):
        self.assertEqual(native_classification(self.row(), {'status': 'harness_error'}), 'HARNESS_ERROR')
        self.assertEqual(native_classification(self.row(), {'status': 'timeout'}), 'TIMEOUT')
        self.assertEqual(native_classification(self.row(attempt_state='NOT_RUN'), {}), 'NOT_RUN')

    def test_interrupted_third_trial_cannot_pass_or_become_behavior_fail(self):
        passed = self.row(semantic_pending=False, corrected_binary=True, behavior_assessable=True)
        interrupted = apply_native_boundary(self.row(), {'status': 'failed', 'error': {'codexErrorInfo': 'usageLimitExceeded'}})
        self.assertEqual(case_status([passed, passed, interrupted], 'corrected_binary'), 'INCOMPLETE_NATIVE_INTERRUPTION')


if __name__ == '__main__':
    unittest.main()
