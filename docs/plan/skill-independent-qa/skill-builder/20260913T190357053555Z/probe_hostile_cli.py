"""Actual argv preservation through the native Python CLI, synthetic data only."""
from pathlib import Path
import json
import subprocess
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import test_independent as base
from capture import manifest
expected='7715f8b80a9b089a4349f6bbb3b502a52d55a03bb2eb2ec65f861ea4be77ff3a'
assert manifest(base.BUILDER)['package_digest']==expected
root=base.RUN/'fixtures'/"windows-final04 CLI é $var & (x); apostrophe'"
root.mkdir()
fixture=base.Independent('test_binding_bound'); fixture.root=root
skill,_=fixture.skill(); fixture.binding(skill)
before=base.package(root)
command=[sys.executable,'-B','-X','utf8',str(base.BUILDER/'assets/adaptive-runtime/check_project_binding.py'),'--project-root',str(root),'--skill-root',str(skill)]
base.save(base.RUN/'reports/hostile-cli-plan.json',{'target_digest':expected,'argv':command,'expected_exit':0,'expected_reason':'BOUND','expected_effects':'No file changes','timeout_seconds':120})
result=subprocess.run(command,capture_output=True,timeout=120)
observation=json.loads(result.stdout)
assert result.returncode==0 and observation['reason_code']=='BOUND'
assert before==base.package(root)
base.save(base.RUN/'reports/hostile-cli-result.json',{'target_digest':expected,'status':'PASS','exit_code':result.returncode,'stdout':observation,'stderr':result.stderr.decode(),'effects_unchanged':True,'method':'Native Windows argument vector with spaces, non-ASCII, dollar, ampersand, parentheses, semicolon and apostrophe. No shell interpolation.'})
print('PASS native hostile-path argv handling')
