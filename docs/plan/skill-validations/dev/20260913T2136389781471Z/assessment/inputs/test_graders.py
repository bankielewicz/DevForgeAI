"""Positive and negative tests of evaluator evidence grading, not skill behavior."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'bundle'))
import graders as g

class Graders(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=ROOT/'trials')
        self.root=Path(self.temp.name)
        (self.root/'a Ω $literal.txt').write_bytes(b'value')
        self.reference={'path':'a Ω $literal.txt','sha256':g.sha(b'value')}
        self.row={'path':self.reference['path'],'bytes':5,'sha256':self.reference['sha256']}
        self.manifest={'complete':True,'excluded_boundaries':[],'files':[self.row],'package_digest':g.sha(g.compact([self.row]))}
    def tearDown(self): self.temp.cleanup()
    def test_exact_reference_and_literal_path(self): self.assertEqual(g.verify_refs(self.root,[self.reference]),1)
    def test_stale_reference_rejected(self):
        (self.root/self.reference['path']).write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError,'STALE'): g.verify_refs(self.root,[self.reference])
    def test_duplicate_reference_rejected(self):
        with self.assertRaisesRegex(ValueError,'duplicate'): g.verify_refs(self.root,[self.reference,self.reference])
    def test_traversal_absolute_and_shell_path_rejected(self):
        for path in ('../outside','/absolute','C:/absolute','a\\b','a//b','./a','a\x00b'):
            with self.subTest(path=path),self.assertRaises(ValueError): g.safe_file(self.root,path)
    def test_invalid_digest_rejected(self):
        with self.assertRaisesRegex(ValueError,'SHA'): g.verify_refs(self.root,[dict(self.reference,sha256='ABC')])
    def test_strict_json_rejects_duplicate(self):
        with self.assertRaises(ValueError): g.load('{"x":1,"x":2}')
    def test_strict_json_rejects_nonfinite(self):
        for text in ('NaN','Infinity','-Infinity'):
            with self.subTest(text=text),self.assertRaises(ValueError): g.load(text)
    def test_exact_package(self): self.assertEqual(g.verify_package(self.root,self.manifest),self.manifest['package_digest'])
    def test_extra_package_file(self):
        (self.root/'extra').write_bytes(b'new')
        with self.assertRaisesRegex(ValueError,'file-set'): g.verify_package(self.root,self.manifest)
    def test_changed_package_file(self):
        (self.root/self.reference['path']).write_bytes(b'wrong')
        with self.assertRaisesRegex(ValueError,'STALE_PACKAGE'): g.verify_package(self.root,self.manifest)
    def test_incomplete_capture(self):
        with self.assertRaisesRegex(ValueError,'incomplete'): g.verify_package(self.root,dict(self.manifest,complete=False))
    def test_manifest_digest_mismatch(self):
        with self.assertRaisesRegex(ValueError,'digest'): g.verify_package(self.root,dict(self.manifest,package_digest='0'*64))
    def test_noncanonical_manifest(self):
        with self.assertRaisesRegex(ValueError,'noncanonical'): g.verify_package(self.root,dict(self.manifest,files=[self.row,self.row]))
    def test_metrics_required_nonpasses_count(self):
        rows=[{'case_id':str(i),'required':True,'result':s} for i,s in enumerate(['PASS','FAIL','ERROR','NOT_RUN','NOT_APPLICABLE'])]
        self.assertEqual(g.metrics(rows)['pass_rate'],20)
        self.assertEqual(g.metrics(rows)['required'],5)
    def test_metrics_no_rounding(self):
        rows=[{'case_id':str(i),'required':True,'result':'PASS' if i<949 else 'NOT_RUN'} for i in range(1000)]
        self.assertEqual(g.metrics(rows)['pass_rate'],94.9)
    def test_duplicate_case_rejected(self):
        row={'case_id':'x','required':True,'result':'PASS'}
        with self.assertRaisesRegex(ValueError,'duplicate'): g.metrics([row,row])
    def test_invalid_status_rejected(self):
        with self.assertRaises(ValueError): g.metrics([{'case_id':'x','required':True,'result':'SKIP'}])
    def test_receipt_requires_real_streams(self):
        row={'attempt_id':'a','command':['x'],'working_directory':str(self.root),'started_at':'start','ended_at':'end','exit_code':0,'stdout':self.reference,'stderr':self.reference,'candidate':self.reference,'result':'PASS'}
        # Streams/candidate must have distinct references; duplicate refs are rejected.
        with self.assertRaises(ValueError): g.check_execution(row,self.root)
    def test_incomplete_receipt_rejected(self):
        with self.assertRaisesRegex(ValueError,'incomplete'): g.check_execution({},self.root)
    def test_false_pass_rejected(self):
        row={k:None for k in ('attempt_id','command','working_directory','started_at','ended_at','exit_code','stdout','stderr','candidate','result')}
        row.update(result='PASS',exit_code=1)
        with self.assertRaisesRegex(ValueError,'unsupported PASS'): g.check_execution(row,self.root)
    def test_portable_scan_detects_leak(self):
        (self.root/self.reference['path']).write_text('C:/Author/Project',encoding='utf-8')
        self.assertEqual(len(g.portable_scan(self.root,self.manifest)),1)

if __name__=='__main__': unittest.main()
