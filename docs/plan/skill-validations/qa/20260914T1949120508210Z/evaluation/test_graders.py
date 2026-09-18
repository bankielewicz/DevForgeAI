"""Known-good and adverse evidence vectors; not product acceptance tests."""
import unittest
from graders import metric, ordered_trace, reduce_cases, report_contract

class MetricTests(unittest.TestCase):
    def test_boundary_below(self):
        self.assertEqual(metric(9499,10000), 'FAIL')
    def test_boundary_exact(self):
        self.assertEqual(metric(9500,10000), 'PASS')
    def test_stricter_policy(self):
        self.assertEqual(metric(97,100,floor=98), 'FAIL')
    def test_partial_not_failure(self):
        self.assertEqual(metric(1,100,complete=False), 'NOT_RUN')
    def test_missing_denominator(self):
        self.assertEqual(metric(0,0), 'NOT_RUN')
    def test_crashed_collector(self):
        self.assertEqual(metric(99,100,collector_ok=False), 'NOT_RUN')
    def test_invalid_counts(self):
        for n,d in [(101,100),(-1,100),(True,1),(None,5),(1,None)]:
            with self.subTest(n=n,d=d):
                self.assertEqual(metric(n,d), 'ERROR')

class OrderingTests(unittest.TestCase):
    def test_launch_after_terminal(self):
        self.assertEqual(ordered_trace(['plan_readback','terminal_stop','test_launch']), 'FAIL')
    def test_launch_before_plan(self):
        self.assertEqual(ordered_trace(['test_launch','plan_readback','finished']), 'FAIL')
    def test_normal_run(self):
        self.assertEqual(ordered_trace(['plan_readback','test_launch','finished'],True), 'PASS')
    def test_ordinary_defect_continues(self):
        self.assertEqual(ordered_trace(['plan_readback','ordinary_defect','test_launch','finished'],True), 'PASS')
    def test_static_stop(self):
        self.assertEqual(ordered_trace(['terminal_stop','report','finished']), 'PASS')
    def test_missing_required_launch(self):
        self.assertEqual(ordered_trace(['plan_readback','finished'],True), 'NOT_RUN')
    def test_partial_trace(self):
        self.assertEqual(ordered_trace(['plan_readback','test_launch'],True), 'NOT_RUN')

class AccountingTests(unittest.TestCase):
    def test_failure_precedes_gap(self):
        self.assertEqual(reduce_cases([('A','FAIL'),('B','NOT_RUN')]), 'FAIL')
    def test_gap_prevents_pass(self):
        self.assertEqual(reduce_cases([('A','PASS'),('B','ERROR')]), 'INCOMPLETE')
    def test_duplicate_cannot_inflate(self):
        self.assertEqual(reduce_cases([('A','PASS'),('A','PASS')]), 'ERROR')
    def test_empty_not_passing(self):
        self.assertEqual(reduce_cases([]), 'INCOMPLETE')
    def test_all_pass(self):
        self.assertEqual(reduce_cases([('A','PASS'),('B','PASS')]), 'PASS')
    def test_invalid_result(self):
        self.assertEqual(reduce_cases([('A','SKIP_AS_PASS')]), 'ERROR')

class ReportTests(unittest.TestCase):
    def test_plan_is_nonverdict(self):
        self.assertEqual(report_contract(dict(intent='plan',execution='NOT_STARTED',verdict='NOT_EVALUATED',owner='user',fix=False,remaining=['A'])), 'PASS')
    def test_plan_cannot_pass(self):
        self.assertEqual(report_contract(dict(intent='plan',execution='NOT_STARTED',verdict='PASS',owner='user',fix=False,remaining=[])), 'FAIL')
    def test_static_fail_has_fix_owner(self):
        self.assertEqual(report_contract(dict(intent='run',execution='NOT_STARTED',verdict='FAIL',owner='dev',fix=True,remaining=['A'])), 'PASS')
    def test_qa_cannot_own_repair(self):
        self.assertEqual(report_contract(dict(intent='run',execution='STOPPED',verdict='FAIL',owner='qa',fix=True,remaining=['A'])), 'FAIL')
    def test_gap_not_invented_fix(self):
        self.assertEqual(report_contract(dict(intent='run',execution='COMPLETED',verdict='INCOMPLETE',owner='environment',fix=False,remaining=['A'])), 'PASS')
    def test_unperformed_prevents_pass(self):
        self.assertEqual(report_contract(dict(intent='run',execution='COMPLETED',verdict='PASS',owner='reviewer',fix=False,remaining=['A'])), 'FAIL')
    def test_complete_pass(self):
        self.assertEqual(report_contract(dict(intent='run',execution='COMPLETED',verdict='PASS',owner='reviewer',fix=False,remaining=[])), 'PASS')
    def test_fail_requires_packet(self):
        self.assertEqual(report_contract(dict(intent='run',execution='STOPPED',verdict='FAIL',owner='dev',fix=False,remaining=['A'])), 'FAIL')
    def test_missing_fields(self):
        self.assertEqual(report_contract({'verdict':'PASS'}), 'ERROR')

if __name__=='__main__':
    unittest.main()
