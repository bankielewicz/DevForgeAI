import hashlib
from pathlib import Path
import tempfile
import unittest
from graders import metric, unit_counts, verify_reference, reduce_cases

class GraderTests(unittest.TestCase):
    def test_exact_floors(self):
        self.assertEqual(metric(9499,10000),'FAIL')
        self.assertEqual(metric(95,100),'PASS')
        self.assertEqual(metric(100,100,100),'PASS')
        self.assertEqual(metric(99,100,100),'FAIL')

    def test_unresolved_metrics(self):
        for pair in [(0,0),(None,2),(1,None)]:
            self.assertEqual(metric(*pair),'INCOMPLETE')

    def test_invalid_metrics(self):
        for pair in [(2,1),(-1,1),(True,1),(1.0,2),(1,-1)]:
            with self.assertRaises(ValueError): metric(*pair)
        with self.assertRaises(ValueError): metric(1,1,94)

    def test_unit_retry_category_and_skip(self):
        inv=[{'id':'A','platform':'Windows'},{'id':'B','platform':'Windows'},{'id':'A','platform':'Linux'}]
        attempts=[{'id':'A','platform':'Windows','category':'unit','status':'FAIL'}, {'id':'A','platform':'Windows','category':'unit','status':'PASS'}, {'id':'B','platform':'Windows','category':'unit','status':'NOT_RUN'}, {'id':'setup','platform':'Windows','category':'setup','status':'PASS'}]
        self.assertEqual(unit_counts(inv,attempts),{'passing':1,'required':3,'result':'FAIL','attempts':4})

    def test_invalid_inventory_and_attempts(self):
        with self.assertRaises(ValueError): unit_counts([{'id':'a','platform':'W'}]*2,[])
        with self.assertRaises(ValueError): unit_counts([], [{'id':'x','platform':'W','category':'unit','status':'PASS'}])
        with self.assertRaises(ValueError): unit_counts([{'id':'x','platform':'W'}],[{'id':'x','platform':'W','category':'unit','status':'SKIP_AS_PASS'}])
        self.assertEqual(unit_counts([],[])['result'],'INCOMPLETE')

    def test_bound_reference(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'résumé file'; p.write_bytes(b'actual')
            ref={'path':p.name,'sha256':hashlib.sha256(b'actual').hexdigest()}
            self.assertTrue(verify_reference(d,ref))
            p.write_bytes(b'changed')
            self.assertFalse(verify_reference(d,ref))
            self.assertFalse(verify_reference(d,{'path':'missing','sha256':'0'*64}))

    def test_reference_escape(self):
        with tempfile.TemporaryDirectory() as d:
            for p in ['../escape','C:/escape','/escape','a\\b']:
                with self.assertRaises(ValueError): verify_reference(d,{'path':p,'sha256':'0'*64})

    def test_complete_reduction_and_precedence(self):
        cases=[{'case_id':'A'},{'case_id':'B'},{'case_id':'C'}]
        rows=[{'case_id':'A','result':'PASS'},{'case_id':'B','result':'FAIL'}]
        result=reduce_cases(cases,rows)
        self.assertEqual(result,{'outcome':'FAIL','passing':1,'failed':1,'unperformed':1,'required':3,'evaluated':2})
        self.assertEqual(reduce_cases(cases,rows[:1])['outcome'],'INCOMPLETE')
        self.assertEqual(reduce_cases([cases[0]],rows[:1])['outcome'],'PASS')

    def test_reduction_rejects_count_inflation(self):
        for cases,rows in [([{'case_id':'A'}]*2,[]),([{'case_id':'A'}],[{'case_id':'A','result':'PASS'}]*2),([{'case_id':'A'}],[{'case_id':'B','result':'PASS'}]),([{'case_id':'A'}],[{'case_id':'A','result':'SKIPPED_PASS'}])]:
            with self.assertRaises(ValueError): reduce_cases(cases,rows)

if __name__=='__main__': unittest.main()
