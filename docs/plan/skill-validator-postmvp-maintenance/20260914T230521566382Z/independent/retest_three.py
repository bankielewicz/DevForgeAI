import hashlib,json,sys
from pathlib import Path
origin=Path(__file__).resolve().parent
root=origin/'retest-002';root.mkdir()
scripts=origin.parents[4]/'src/agents/skills/skill-validator/scripts'
sys.path.insert(0,str(scripts))
import trial_runner as r
rows=[]
for name in ('native-empty','preexisting','boolean-json'):
    top=root/name;top.mkdir();project=top/'project';project.mkdir()
    code=top/'command.py';code.write_text('from pathlib import Path\nPath("report.json").write_text("{\\"total\\": true}")\n' if name=='boolean-json' else 'print("complete")\n')
    outputs=[] if name=='native-empty' else [dict(path='report.json',kind='json',requirement_id='result',value={'total':1})]
    if name=='preexisting': (project/'report.json').write_text('{"total":1}')
    plan=dict(schema_version='trial-plan-v1',case_id=name,kind='native',argv=[sys.executable,'-B',str(code)],cwd=str(project),permitted_write_root=str(project),inputs=[dict(path=str(code),sha256=r.digest(code))],prompt=None,requirement_ids=['result'],dependencies=[],expected_outputs=outputs,timeout_seconds=5)
    (top/'plan.json').write_text(json.dumps(plan));expected='FAIL' if name=='boolean-json' else 'REJECTED'
    try:
        r.seal(top/'plan.json',top/'attempt');actual=r.run(top/'attempt')['outcome']
    except ValueError as error: actual='REJECTED'
    rows.append(dict(case=name,expected=expected,actual=actual,passed=actual==expected))
(root/'results.json').write_text(json.dumps(rows,indent=2))
(root/'runner-sha256.txt').write_text(r.digest(scripts/'trial_runner.py'))
print(json.dumps(rows,indent=2))
