import importlib.util
import json
import os
import sys
import unittest
from prepare_validation import ROOT,PROJECT,put
out=ROOT/'observations/regression-schema-correction'
out.mkdir(parents=True,exist_ok=False)
os.environ['AUTHORING_BUILDER_ROOT']=str(ROOT/'source')
sys.path.insert(0,str(ROOT/'inputs/regressions'))
sys.path.insert(0,str(PROJECT/'.agents/skills/skill-validator/scripts'))
import test_authoring
test_authoring.PACKAGE=PROJECT/'.agents/skills/skill-validator'
def setup(self):
    self.project=ROOT/'trials/regression-schema-correction'
    self.project.mkdir(parents=True,exist_ok=False)
    self.target=self.project/'skills'/ 'brief-note'
    self.counter=0
test_authoring.AuthoringTests.setUp=setup
put(out/'plan.json',{'case':'test_new_record_schemas_match_actual_outputs','expected':'PASS','correction':'Point copied regression PACKAGE at actual loaded validator; assertions unchanged.','timeout_seconds':120})
with (out/'stdout.txt').open('w',encoding='utf-8') as stream:
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.TestSuite([test_authoring.AuthoringTests('test_new_record_schemas_match_actual_outputs')]))
put(out/'result.json',{'result':'PASS' if result.wasSuccessful() else 'FAIL','tests_run':result.testsRun,'errors':result.errors,'failures':result.failures})
print('PASS' if result.wasSuccessful() else 'FAIL')
