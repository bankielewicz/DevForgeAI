from pathlib import Path
import hashlib
import json
import re
RUN=Path(__file__).resolve().parent
attempt=RUN/'native/ordinary-edit-03'
receipt=json.loads((attempt/'result.json').read_bytes())
project=Path(receipt['cwd'])
assert receipt['exit_code']==0 and not receipt['timed_out']
before={x['path']:x['sha256'] for x in receipt['before']}
after={x['path']:x['sha256'] for x in receipt['after']}
assert [p for p in before if before[p]!=after.get(p)]==['skills/concise-note/SKILL.md']
requests=[p for p in (project/'docs/plan/skill-authorings/concise-note').glob('*/validation-request.json') if json.loads((p.parent/'authoring-record.json').read_bytes())['operation']=='edit']
assert len(requests)==1
request=json.loads(requests[0].read_bytes()); record=json.loads((requests[0].parent/'authoring-record.json').read_bytes())
assert request['authoring_record']['sha256']==hashlib.sha256((requests[0].parent/'authoring-record.json').read_bytes()).hexdigest()
assert record['prior_origin']['kind']=='authored' and record['authoring_state']=='AUTHORED'
assert record['validation_status']==record['testing_status']=='NOT_PERFORMED'
old=(requests[0].parent/'before/SKILL.md').read_bytes()
new=(requests[0].parent/'baseline/SKILL.md').read_bytes()
assert new.replace(b' End every bullet with a period.',b'')==old
events=[json.loads(line) for line in (attempt/'output/stdout.jsonl').read_text(encoding='utf-8').splitlines()]
commands=[x['item']['command'] for x in events if x.get('type')=='item.completed' and x.get('item',{}).get('type')=='command_execution']
assert not any(re.search(r'python[^\n]*(quick_validate|run_evaluation|pytest|unittest|skill-validator.+scripts)',cmd,re.I) for cmd in commands)
result={'case':'BAT-01 focused edit','status':'PASS','target_builder_digest':'ecb5f8056f18e1d9889de0c829a7e8e48a6feafe1b8f29bc09718d226eb20099','checks':['Only original target file changed; all preexisting custody/history files preserved','Exact requested sentence added; other bytes unchanged','Authored prior used without validation prerequisite','New manual request and NOT_PERFORMED quality statuses','No test/checker/validator command observed'],'commands':commands,'limitation':'Explicit native execution; inherited host configuration remains shared.'}
(RUN/'reports/native-edit-assessment.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print('PASS focused native edit')
