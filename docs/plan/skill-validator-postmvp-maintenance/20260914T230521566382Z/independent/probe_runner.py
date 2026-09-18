import copy
import ctypes
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

BASE = Path(__file__).resolve().parent
SCRIPTS = BASE.parents[4] / 'src/agents/skills/skill-validator/scripts'
sys.path.insert(0, str(SCRIPTS))
import trial_runner as runner
import skill_format

ROWS = []
def save(path, value):
    path.write_text(json.dumps(value, indent=2), encoding='utf-8')
def row(case, expected, observed, passed):
    ROWS.append(dict(case=case, expected=expected, observed=observed, passed=passed))
    save(BASE / 'probe-results.json', ROWS)
def ref(path):
    return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
def fixture(name, code, outputs=None, timeout=5, inputs_inside=False):
    top = BASE / name
    top.mkdir()
    project = top / 'project'
    project.mkdir()
    script = (project if inputs_inside else top) / 'command.py'
    script.write_text(code, encoding='utf-8')
    plan = dict(schema_version='trial-plan-v1', case_id=name, kind='native',
                argv=[sys.executable, '-B', str(script)], cwd=str(project),
                permitted_write_root=str(project), inputs=[ref(script)], prompt=None,
                requirement_ids=['independent-outcome'], dependencies=[],
                expected_outputs=outputs or [], timeout_seconds=timeout)
    plan_path = top / 'plan.json'
    save(plan_path, plan)
    return top, plan_path, top / 'attempt'
def output(kind, value=None):
    item = {'path': 'report.json', 'kind':kind, 'requirement_id':'independent-outcome'}
    if value is not None:
        item['value'] = value
    return item

for name, tail, valid in [('valid', 'metadata: {version: "1"}\nallowed-tools: Read\n', True),
                           ('numeric-meta', 'metadata: {version: 1}\n', False),
                           ('tools-sequence', 'allowed-tools: [Read]\n', False),
                           ('mixed-keys', '17: x\nextra: y\n', False),
                           ('duplicate', 'name: second\n', False)]:
    try:
        skill_format.frontmatter('---\nname: skill\ndescription: Work\n'+tail+'---\nText')
        actual = True
    except ValueError:
        actual = False
    row('IND-META-'+name, valid, actual, actual == valid)

top, plan, attempt = fixture('missing-output', 'print("Completed successfully")\n', [output('exists')])
runner.seal(plan, attempt)
result = runner.run(attempt)
row('IND-011', 'FAIL', result['outcome'], result['outcome']=='FAIL')

top, plan, attempt = fixture('wrong-output', 'from pathlib import Path\nPath("report.json").write_text("{\\"total\\": 17}")\n', [output('json', {'total':23})])
runner.seal(plan, attempt)
result = runner.run(attempt)
row('IND-012', 'FAIL', result['outcome'], result['outcome']=='FAIL')

top, plan, attempt = fixture('correct-output', 'from pathlib import Path\nPath("report.json").write_text("{\\"total\\": 23}")\n', [output('json', {'total':23})])
runner.seal(plan, attempt)
result = runner.run(attempt)
row('IND-013', 'PASS', result['outcome'], result['outcome']=='PASS')
original = copy.deepcopy(result)
for tag, change in [('missing-streams', {'streams':[]}), ('changed-timeout', {'timeout_seconds':999}),
                    ('wrong-schema', {'schema_version':'invalid'}), ('boolean-exit', {'exit_code':False}),
                    ('nonsensical-duration', {'elapsed_seconds':-999})]:
    modified = dict(original, **change)
    save(attempt/'result.json', modified)
    try:
        accepted = runner.check_attempt(attempt)['outcome']
    except (ValueError, KeyError, TypeError):
        accepted = 'REJECTED'
    row('IND-RECEIPT-'+tag, 'REJECTED', accepted, accepted=='REJECTED')
    save(top/('tamper-'+tag+'.json'), modified)
save(attempt/'result.json', original)

top2, plan2, attempt2 = fixture('dependent', 'print("done")\n')
plan_data = runner.read(plan2)
plan_data['dependencies'] = ['correct-output']
plan_data['dependency_attempts'] = {'correct-output':str(attempt)}
save(plan2, plan_data)
runner.seal(plan2, attempt2)
runner.run(attempt2)
summary = runner.summarize([{'case_id':'dependent','attempt':str(attempt2),'dependencies':[]}])
row('IND-SUMMARY-OMITTED-DEPENDENCY', 'REJECTED', summary['outcome'], summary['outcome']!='PASS')
save(top2/'omitted-dependency-summary.json', summary)

top, plan, attempt = fixture('inside-input', 'print("done")\n', inputs_inside=True)
try:
    runner.seal(plan, attempt)
    actual = 'SEALED'
except ValueError:
    actual = 'REJECTED'
row('IND-INPUT-BOUNDARY', 'REJECTED by selected SVE-04', actual, actual=='REJECTED')

top, plan, attempt = fixture('unexpected-side-effect', 'from pathlib import Path\nPath("unexpected.txt").write_text("side effect")\n')
runner.seal(plan, attempt)
result = runner.run(attempt)
record_text = json.dumps(result)
row('IND-SIDE-EFFECT-OBSERVATION', 'unexpected.txt present in side effect observations', result, 'unexpected.txt' in record_text)

code = '''import os, subprocess, sys, time
from pathlib import Path
child = subprocess.Popen([sys.executable, '-B', '-c', 'import time; time.sleep(60)'])
Path('child.pid').write_text(str(child.pid))
print('retained-before-timeout', flush=True)
time.sleep(60)
'''
top, plan, attempt = fixture('descendant-timeout', code, timeout=1.5)
runner.seal(plan, attempt)
result = runner.run(attempt)
child_pid = int((top/'project/child.pid').read_text())
kernel = ctypes.WinDLL('kernel32', use_last_error=True)
kernel.OpenProcess.argtypes=[ctypes.c_ulong, ctypes.c_int, ctypes.c_ulong]
kernel.OpenProcess.restype=ctypes.c_void_p
kernel.CloseHandle.argtypes=[ctypes.c_void_p]
handle = kernel.OpenProcess(0x1000, False, child_pid)
alive = False
if handle:
    code = ctypes.c_ulong()
    kernel.GetExitCodeProcess.argtypes=[ctypes.c_void_p, ctypes.POINTER(ctypes.c_ulong)]
    kernel.GetExitCodeProcess(handle, ctypes.byref(code))
    alive = code.value == 259
    kernel.CloseHandle(handle)
row('IND-015-DESCENDANT', 'timeout retained; cleanup VERIFIED; child not alive; marker preserved',
    dict(result=result, child_alive=alive), result['timeout'] and result['cleanup']=='VERIFIED' and not alive and 'retained-before-timeout' in (attempt/'stdout.txt').read_text())
print(json.dumps(ROWS, indent=2))
