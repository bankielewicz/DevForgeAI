"""Independent retained-artifact checking; does not invoke either skill."""
from pathlib import Path
import hashlib
import json
import re
RUN=Path(__file__).resolve().parent
attempt=RUN/'native/ordinary-create-03'
project=attempt/'project'
receipt=json.loads((attempt/'result.json').read_bytes())
events=[json.loads(line) for line in (attempt/'output/stdout.jsonl').read_text(encoding='utf-8').splitlines()]
commands=[x['item']['command'] for x in events if x.get('type')=='item.completed' and x.get('item',{}).get('type')=='command_execution']
assert receipt['exit_code']==0 and not receipt['timed_out']
requests=[p for p in (project/'docs/plan/skill-authorings/concise-note').glob('*/validation-request.json') if json.loads((p.parent/'authoring-record.json').read_bytes())['operation']=='create']
assert len(requests)==1
request=json.loads(requests[0].read_bytes())
def reference(ref):
    path=Path(ref['path']); assert path.is_relative_to(project)
    data=path.read_bytes(); assert hashlib.sha256(data).hexdigest()==ref['sha256']
    return json.loads(data)
record=reference(request['authoring_record'])
manifest=reference(request['target_manifest'])
assert record['authoring_state']=='AUTHORED'
assert record['validation_status']==record['testing_status']=='NOT_PERFORMED'
assert request['package_digest']==hashlib.sha256(json.dumps(manifest['files'],ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
observed={row['path']:row for row in receipt['after']}
for row in manifest['files']:
    recorded=observed['skills/concise-note/'+row['path']]
    assert (row['bytes'],row['sha256'])==(recorded['bytes'],recorded['sha256'])
publication=json.loads((requests[0].parent/'publication-readback.json').read_bytes())
assert publication['state']=='PUBLISHED' and publication['authoring_record']==request['authoring_record']
assert publication['package_digest']==request['package_digest']
assert not any(re.search(r'python[^\n]*(quick_validate|run_evaluation|pytest|unittest|skill-validator.+scripts)',cmd,re.I) for cmd in commands)
source=(requests[0].parent/'baseline/SKILL.md').read_text(encoding='utf-8')
assert 'exactly three' in source and 'factual claims' in source
result={'case':'BAT-01 cold create','status':'PASS','target_builder_digest':'ecb5f8056f18e1d9889de0c829a7e8e48a6feafe1b8f29bc09718d226eb20099','package_digest':request['package_digest'],'artifact_checks':['Actual readback-bound authoring record','Manual request exact digest','Target after-manifest agrees with delivered bytes','Quality NOT_PERFORMED','Command trace inspected: no checker/test/validator process','Generated three-bullet behavior and missing-input clarification reviewed'],'commands':commands,'limitations':['Explicit invocation, not implicit discovery.','Shared host loaded installed skill-creator and memory; fully absent-validator environment not established.','Generated skill itself was not executed.','After-manifest and preserved baseline bind the create result even when the separately authorized follow-up edit later changes the live target.']}
(RUN/'reports/native-create-assessment.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print('PASS native create artifact/handoff/trace checks')
