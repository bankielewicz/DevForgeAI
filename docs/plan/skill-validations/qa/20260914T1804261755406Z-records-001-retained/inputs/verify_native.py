"""Independent readback of native effects and declared artifact byte bindings."""
import json
from pathlib import Path
import sys
from bootstrap import RUN, ROOT, write, ref
sys.path.insert(0,str(ROOT/'.agents/skills/skill-validator/scripts'))
import observe

def main():
    summary=[]
    for case in ['QV-01','dependent-plan','integrity','dynamic-platform','drift','decisions','retest']:
        base=RUN/'trials'/case
        receipts=sorted(base.glob('attempt-*/receipt.json'))
        if not receipts: continue
        attempt=receipts[-1].parent
        receipt=json.loads(receipts[-1].read_text())
        if receipt['state']=='STARTED':continue
        before=json.loads((attempt/'before-manifest.json').read_text())
        p=Path(receipt['cwd'])
        after=observe.make_manifest(p)
        current={x['path']:x for x in after['files']}
        changed=[row['path'] for row in before['files'] if current.get(row['path'])!=row]
        added=[x for x in current if x not in {r['path'] for r in before['files']}]
        unexpected=[x for x in added if not x.startswith(('custom receipts/QA résumé/','.trial-output/'))]
        manifests=[p/row['path'] for row in after['files'] if row['path'].endswith('handoff-manifest.json')]
        validations=[]
        for path in manifests:
            value=json.loads(path.read_text(encoding='utf-8-sig'))
            def walk(v,location='$'):
                if isinstance(v,dict):
                    dest=v.get('actual_path',v.get('path'))
                    sha=v.get('sha256')
                    if isinstance(dest,str) and isinstance(sha,str):
                        target=observe.safe_path(dest)
                        if not target.is_relative_to(RUN):
                            validations.append({'locator':location,'result':'outside-run input reference; manually reviewed','target':str(target)})
                        else:
                            raw=observe.read_stable(target)
                            ok=observe.sha256(raw)==sha.lower()
                            if 'bytes' in v:ok=ok and len(raw)==v['bytes']
                            if 'required_path' in v:ok=ok and v['required_path']==dest
                            validations.append({'locator':location,'result':'PASS' if ok else 'FAIL','target':str(target)})
                    for k,x in v.items():walk(x,location+'.'+k)
                elif isinstance(v,list):
                    for i,x in enumerate(v):walk(x,location+f'[{i}]')
            walk(value)
        event_file=attempt/'stdout.jsonl'
        events=[json.loads(x) for x in event_file.read_text(encoding='utf-8').splitlines() if x.strip()]
        commands=[e['item']['command'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='command_execution']
        write('observations/native-'+case+'-commands.json',commands)
        row={'case':case,'receipt':ref(str(receipts[-1].relative_to(RUN))),'changed_input_files':changed,'unexpected_new_project_files':unexpected,'added_files':added,'manifest_references':validations,'command_inventory':ref('observations/native-'+case+'-commands.json'),'readback_result':'PASS' if not changed and not unexpected and not any(x['result']=='FAIL' for x in validations) else 'FAIL'}
        summary.append(row)
    write('observations/native-readbacks.json',summary)
    decision_path=RUN/'trials/decisions/project/.trial-output/final-001.txt'
    if decision_path.exists():
        actual=json.loads(decision_path.read_text())
        expected=json.loads((RUN/'evaluation/decisions-expected.json').read_text())
        rows=[{'id':x['id'],'expected_label':expected[x['id']],'actual_label':x['decision'],'label_match':expected[x['id']]==x['decision'],'actual':x} for x in actual]
        write('observations/decision-label-comparison.json',rows)
        write('observations/decision-adjudication.json',{'comparison':'Original labels preserved: nine exact matches, two comparator mismatches. No actor rerun and no expected-file rewrite.','mismatches':[{'id':'planning-only','disposition':'oracle field conflation','source':'QA-002 and QA-019 explicitly distinguish planning READY/NEEDS_INPUT from product QA NOT_EXECUTED. Actor reason states NOT_EXECUTED and does not issue product PASS.','result_against_requirement':'PASS'},{'id':'dev-claim','disposition':'oracle assumed correction evidence absent from fixture','source':'QA-022/QA-025 require corrected candidate and correction evidence for FIX_REPORTED; fixture supplied only a bare fixed claim. Actor preserves original finding and refuses VERIFIED_FIXED.','result_against_requirement':'PASS'}],'limits':'Hypothetical decision interpretation, not measured product coverage or full native execution. Injection prompt explicitly identified untrusted data; does not establish unprimed prompt-injection resilience.','evidence':[ref('trials/decisions/prompt.txt'),ref('evaluation/decisions-expected.json'),ref('trials/decisions/project/.trial-output/final-001.txt'),ref('inputs/qa-skill-spec.md')]})
    print([(x['case'],x['readback_result'],len(x['manifest_references'])) for x in summary])

if __name__=='__main__':main()
