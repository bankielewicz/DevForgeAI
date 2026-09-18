"""Fresh independent final-byte replay; old attempts remain unchanged."""
from pathlib import Path
import datetime
import json
import os
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parent))
from capture import RUN, SOURCE, manifest
EXPECTED='7715f8b80a9b089a4349f6bbb3b502a52d55a03bb2eb2ec65f861ea4be77ff3a'
receipt=manifest(SOURCE)
assert receipt['package_digest']==EXPECTED
import test_independent as base
import test_extended as extended
platform='windows' if os.name=='nt' else 'linux'
base.PLATFORM=platform+'-final04'
base.FIXTURES=Path(base.external_fixtures) if base.external_fixtures else RUN/'fixtures'/base.PLATFORM
base.FIXTURES.mkdir(parents=True,exist_ok=True)

class ExclusionCases(base.Independent):
    def check_env(self,name):
        skill,_=self.skill(); (skill/name).write_text('SYNTHETIC_TOKEN=no-secret\n',encoding='utf-8'); self.binding(skill); self.observe(skill,'UNSAFE_PATH')
    def test_env_uppercase(self): self.check_env('.ENV')
    def test_env_mixedcase(self): self.check_env('.Env')
    def test_env_suffix(self): self.check_env('.ENV.local')

suite=unittest.TestSuite()
suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(base.Independent))
suite.addTests(extended.Extended(name) for name in unittest.defaultTestLoader.getTestCaseNames(extended.Extended) if name.startswith('test_extra_'))
suite.addTests(ExclusionCases(name) for name in ('test_env_uppercase','test_env_mixedcase','test_env_suffix'))
plan={'target_digest':EXPECTED,'source_files':receipt['files'],'fixture_root':str(base.FIXTURES),'cases':[test.id() for test in suite],'started':datetime.datetime.now(datetime.timezone.utc).isoformat(),'timeout_seconds':120,'reason':'Final source replay after case-insensitive environment exclusion repair; predecessor results retained.'}
base.save(RUN/'reports'/(platform+'-final04-plan.json'),plan)
with (RUN/'reports'/(platform+'-final04-unittest.txt')).open('w',encoding='utf-8') as stream:
    result=unittest.TextTestRunner(verbosity=2,resultclass=base.LedgerResult,stream=stream).run(suite)
final=manifest(SOURCE)
assert final['package_digest']==EXPECTED
base.save(RUN/'reports'/(platform+'-final04-results.json'),{'target_digest':EXPECTED,'fixture_root':str(base.FIXTURES),'tests_run':result.testsRun,'results':result.rows,'source_unchanged':final['manifest']==receipt['manifest'],'started':plan['started'],'ended':datetime.datetime.now(datetime.timezone.utc).isoformat(),'raw_log':platform+'-final04-unittest.txt'})
print(json.dumps({'platform':platform,'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'source_unchanged':final['manifest']==receipt['manifest']}))
sys.exit(not result.wasSuccessful())
