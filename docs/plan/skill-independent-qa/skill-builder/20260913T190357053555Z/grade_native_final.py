"""Read retained final-byte trials; preserve timeout precedence."""
from pathlib import Path
import hashlib
import json
import re

RUN=Path(__file__).resolve().parent
DIGEST='7715f8b80a9b089a4349f6bbb3b502a52d55a03bb2eb2ec65f861ea4be77ff3a'
rows=[]
for name in ('routing-description','review-equivalent','review-removed','ordinary-import'):
    attempt=RUN/'native'/f'{name}-04'
    result=json.loads((attempt/'result.json').read_bytes())
    events=[json.loads(x) for x in (attempt/'output/stdout.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
    commands=[x['item']['command'] for x in events if x.get('type')=='item.completed' and x.get('item',{}).get('type')=='command_execution']
    before={x['path']:x['sha256'] for x in result['before']}
    after={x['path']:x['sha256'] for x in result['after']}
    changed=[x for x in before if before[x]!=after.get(x)]
    added=sorted(set(after)-set(before))
    assert not changed
    row={'case':name,'target_digest':DIGEST,'exit_code':result['exit_code'],'timed_out':result['timed_out'],'changed_original_files':changed,'added_files':added,'commands':commands,'status':'NOT_RUN' if result['timed_out'] else 'UNASSESSED'}
    if name=='routing-description':
        final=(attempt/'output/final.txt').read_text(encoding='utf-8')
        assert result['exit_code']==0 and not result['timed_out'] and not added and not commands
        answers=re.findall(r'\| [1-5]\. .*? \| (Yes|No) \|',final)
        assert answers==['Yes','Yes','Yes','No','No'],answers
        assert 'Propose' in final and 'Author' in final and 'Review' in final
        row.update(status='PASS',checks=['Description-only classifications match five held-out expected answers','No tool commands or project writes'],limitation='Classification only; does not prove host discovery or completion of selected workflows.')
    elif name.startswith('review-'):
        assert result['timed_out']
        row.update(checks=['Original variant and both parent inputs unchanged','No published review output before timeout'],limitation='Required semantic disposition and proposed revision are unperformed; absence of writes before timeout is not complete no-rebase assurance.')
    else:
        project=Path(result['cwd'])
        assert result['timed_out']
        target=project/'skills/brief-note/SKILL.md'
        text=target.read_text(encoding='utf-8')
        assert 'one-sentence summary followed by two bullets' in text and 'Preserve dates and names' in text
        assert 'Ask for missing paragraph text' in text
        runs=list((project/'docs/plan/skill-authorings/brief-note').glob('*/authoring-record.json'))
        assert len(runs)==1
        run=runs[0].parent
        record=json.loads(runs[0].read_bytes())
        assert record['operation']=='import' and record['authoring_state']=='AUTHORED'
        assert record['validation_status']==record['testing_status']=='NOT_PERFORMED'
        request=json.loads((run/'validation-request.json').read_bytes())
        assert request['authoring_record']['sha256']==hashlib.sha256(runs[0].read_bytes()).hexdigest()
        assert target.read_bytes()==(run/'baseline/SKILL.md').read_bytes()==(run/'candidate/SKILL.md').read_bytes()
        row.update(checks=['Imported prose retains source summary/bullet/date/name/missing-input behavior','Original Claude source unchanged','Published target equals captured candidate and baseline','Import AUTHORED with quality NOT_PERFORMED','Manual request binds actual authoring-record bytes'],limitation='Published artifacts are partial positive evidence; process timed out with no final handoff, so complete BAT-17 import remains NOT_RUN.')
    rows.append(row)
(RUN/'reports/native-final04-assessment.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
for row in rows:
    print(row['case'],row['status'],'commands',len(row['commands']),'added',len(row['added_files']))
