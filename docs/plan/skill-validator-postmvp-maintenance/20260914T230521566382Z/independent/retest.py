import copy
import hashlib
import json
from pathlib import Path
import sys

ORIGIN = Path(__file__).resolve().parent
BASE = ORIGIN / 'retest-001'
BASE.mkdir()
SCRIPTS = ORIGIN.parents[4] / 'src/agents/skills/skill-validator/scripts'
sys.path.insert(0, str(SCRIPTS))
import trial_runner as runner
ROWS = []
def save(path, value): path.write_text(json.dumps(value, indent=2), encoding='utf-8')
def row(case, expected, actual):
    ROWS.append(dict(case=case, expected=expected, observed=actual, passed=expected==actual))
    save(BASE/'results.json', ROWS)
def ref(path): return dict(path=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest())
def fixture(name, code, outputs=None, inputs_inside=False, timeout=5):
    top = BASE/name; top.mkdir(); project = top/'project'; project.mkdir()
    script = (project if inputs_inside else top)/'command.py'; script.write_text(code, encoding='utf-8')
    plan = dict(schema_version='trial-plan-v1',case_id=name,kind='native',argv=[sys.executable,'-B',str(script)],cwd=str(project),permitted_write_root=str(project),inputs=[ref(script)],prompt=None,requirement_ids=['outcome'],dependencies=[],expected_outputs=outputs or [],timeout_seconds=timeout)
    save(top/'plan.json',plan)
    return top, top/'plan.json',top/'attempt'
def output(value): return dict(path='report.json',kind='json',requirement_id='outcome',value=value)
def checked(attempt):
    try: return runner.check_attempt(attempt)['outcome']
    except (ValueError,KeyError,TypeError): return 'REJECTED'

save(BASE/'source-before.json', [ref(SCRIPTS/name) for name in ('trial_runner.py','windows_trial.py','trial_worker.py')])
top, plan, attempt = fixture('correct-output', 'from pathlib import Path\nPath("report.json").write_text("{\\"total\\": 23}")\n',[output({'total':23})])
runner.seal(plan,attempt); original = runner.run(attempt)
row('positive-output','PASS',checked(attempt))
for tag, change in [('missing-streams', {'streams':[]}),('changed-timeout',{'timeout_seconds':999}),('wrong-schema',{'schema_version':'invalid'}),('boolean-exit',{'exit_code':False}),('negative-duration',{'elapsed_seconds':-999}),('missing-manifests',{'manifests':[]}),('hidden-changes',{'changed_paths':[]})]:
    modified = dict(original, **change); save(attempt/'result.json',modified)
    save(top/('tamper-'+tag+'.json'),modified)
    row('receipt-'+tag,'REJECTED',checked(attempt))
save(attempt/'result.json',original)

dep_top,dep_plan,dep_attempt = fixture('dependent','from pathlib import Path\nPath("report.json").write_text("{}")\n',[output({})])
data=runner.read(dep_plan);data['dependencies']=['correct-output'];data['dependency_attempts']={'correct-output':str(attempt)};save(dep_plan,data)
runner.seal(dep_plan,dep_attempt);runner.run(dep_attempt)
try: actual = runner.summarize([dict(case_id='dependent',attempt=str(dep_attempt),dependencies=[])])['outcome']
except ValueError: actual='REJECTED'
row('omitted-dependency','REJECTED',actual)

top,plan,attempt = fixture('side-effect','from pathlib import Path\nPath("report.json").write_text("{}")\nPath("unexpected.txt").write_text("side effect")\n',[output({})])
runner.seal(plan,attempt);result=runner.run(attempt)
row('side-effect-observed',True,'unexpected.txt' in result['changed_paths'])
row('side-effect-valid-readback','PASS',checked(attempt))
(top/'project/unexpected.txt').write_text('modified after run')
row('unlisted-output-drift','REJECTED',checked(attempt))

top,plan,attempt = fixture('inside-input','from pathlib import Path\nPath("report.json").write_text("{}")\n',[output({})],inputs_inside=True)
runner.seal(plan,attempt);runner.run(attempt)
row('clarified-inside-input-unchanged','PASS',checked(attempt))
(top/'project/command.py').write_text('print("drift")')
row('inside-input-drift','REJECTED',checked(attempt))

top,plan,attempt = fixture('plan-drift','print("not launched")\n')
runner.seal(plan,attempt); data=runner.read(plan);data['timeout_seconds']=33;save(plan,data)
try: runner.run(attempt); actual='LAUNCHED'
except ValueError: actual='REJECTED'
row('plan-drift-prelaunch','REJECTED',actual)
row('plan-drift-no-start',False,(attempt/'started.json').exists())

top,plan,attempt = fixture('no-native-obligations','print("completed")\n')
try:
    runner.seal(plan,attempt); result=runner.run(attempt); actual=result['outcome']
except ValueError: actual='REJECTED'
row('native-no-obligations','REJECTED',actual)

top,plan,attempt = fixture('preexisting-output','print("completed but did nothing")\n',[output({'total':23})])
(top/'project/report.json').write_text('{"total":23}')
try:
    runner.seal(plan,attempt);result=runner.run(attempt);actual=result['outcome']
except ValueError: actual='REJECTED'
row('preexisting-output-not-proven-delivered','REJECTED',actual)

top,plan,attempt = fixture('boolean-json','from pathlib import Path\nPath("report.json").write_text("{\\"total\\": true}")\n',[output({'total':1})])
runner.seal(plan,attempt);result=runner.run(attempt)
row('boolean-not-json-number','FAIL',result['outcome'])
save(BASE/'source-after.json',[ref(SCRIPTS/name) for name in ('trial_runner.py','windows_trial.py','trial_worker.py')])
print(json.dumps(ROWS,indent=2))
