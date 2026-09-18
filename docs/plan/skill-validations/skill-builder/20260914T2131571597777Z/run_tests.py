"""Frozen JSONL case runner with independent deterministic reduction."""
import datetime as dt
import json
import os
from pathlib import Path
import sys
import time
import unittest
from prepare_validation import ROOT,put,sha
import coverage

out=ROOT/'observations'/'independent-tests'
out.mkdir(parents=True,exist_ok=False)
source=ROOT/'source'
cov=coverage.Coverage(data_file=str(out/'.coverage'),source=[str(source/'scripts'),str(source/'assets/adaptive-runtime')],branch=True)
cov.start()
import test_independent_design
suite=unittest.defaultTestLoader.loadTestsFromModule(test_independent_design)
def flatten(s):
    for t in s:
        if isinstance(t,unittest.TestSuite): yield from flatten(t)
        else: yield t.id()
expected={name:'PASS' for name in flatten(suite)}
put(out/'expected.json',expected)
put(out/'plan.json',dict(timeout_seconds=120,source_denominator='All first-party captured scripts/*.py plus assets/adaptive-runtime/check_project_binding.py; zero excluded first-party behavior',required_cases=list(expected),oracles='Independent assertions from SBP-009 through SBP-014',fixtures='Retained under trials/independent; no source writes',bundle_sources={p.name:sha(p) for p in [ROOT/'test_independent_design.py',ROOT/'run_tests.py',ROOT/'prepare_validation.py']}))
rows=[]
class Result(unittest.TextTestResult):
    def startTest(self,t): self.start=time.monotonic(); super().startTest(t)
    def emit(self,t,result,detail=''):
        row=dict(case_id=t.id(),result=result,detail=detail,elapsed_seconds=time.monotonic()-self.start)
        rows.append(row)
        with (out/'results.jsonl').open('a',encoding='utf-8') as f: f.write(json.dumps(row,ensure_ascii=False)+'\n')
    def addSuccess(self,t): super().addSuccess(t); self.emit(t,'PASS')
    def addFailure(self,t,e): super().addFailure(t,e); self.emit(t,'FAIL',self._exc_info_to_string(e,t))
    def addError(self,t,e): super().addError(t,e); self.emit(t,'ERROR',self._exc_info_to_string(e,t))
    def addSkip(self,t,r): super().addSkip(t,r); self.emit(t,'NOT_RUN',r)
result=unittest.TextTestRunner(resultclass=Result,verbosity=2).run(suite)
cov.stop(); cov.save(); cov.json_report(outfile=str(out/'coverage.json'))
grade={'required_total':len(expected),'passing':sum(r['result']=='PASS' for r in rows),'failing':sum(r['result']=='FAIL' for r in rows),'error':sum(r['result']=='ERROR' for r in rows),'missing':sorted(set(expected)-{r['case_id'] for r in rows}),'duplicates':len(rows)!=len({r['case_id'] for r in rows}),'source':'Independent expectations, not builder design challenges.'}
grade['pass_percentage']=100*grade['passing']/grade['required_total']
put(out/'grade.json',grade)
print(json.dumps(grade))
sys.exit(0 if result.wasSuccessful() else 1)
