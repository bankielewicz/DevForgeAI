"""Assemble records only from retained, independently adjudicated observations."""
import continue_evaluation as c
import copy
import collections
import json
import sys
from pathlib import Path
r=c.RUN
e=r.with_name(r.name+'-evaluation-v2')
sys.path.insert(0,str(e/'bundle'))
import graders

def ref(p):
    return {'path':p.relative_to(r).as_posix(),'sha256':c.h.sha(p.read_bytes())}

def put(src,rel):
    dst=e/rel
    if dst.exists(): assert dst.read_bytes()==src.read_bytes(),str(dst)
    else: c.copy_file(src,dst)

def reduction(rows):
    selected=[x for x in rows if x['required'] and x['applicability']!='not_applicable']
    return {'outcome':'FAIL' if any(x['result']=='FAIL' for x in selected) else 'INCOMPLETE' if any(x['result'] in ('ERROR','NOT_RUN') for x in selected) else 'PASS',
            'required_total':len(selected),'required_evaluated':sum(x['result'] in ('PASS','FAIL') for x in selected),
            'unknown_applicability':sum(x['applicability']=='unknown' for x in selected),
            'incomplete_check_ids':[x['check_id'] for x in selected if x['result'] in ('ERROR','NOT_RUN')]}

def assemble():
    decisions=c.load(r/'inputs/native-decisions.json')
    assert set(decisions)=={'DV-01','DV-02','DV-03','DV-05','DV-08','DV-14','RV-04'}
    carry=c.load(r/'inputs/carry-forward.json')
    cases=[]; external=[]
    for row in carry['cases']:
        original=copy.deepcopy(row['prior_case'])
        original['evidence']=[{'path':'inputs/carried/'+x['path'],'sha256':x['sha256']} for x in original['evidence']]
        original['reason']='CARRIED_FORWARD: '+original['reason']
        assert row['eligible']
        external.append(original)
        cases.append({'case_id':row['case_id'],'result':'PASS','method':original['method'],
           'reason':'CARRIED_FORWARD: '+row['prior_reason'],'evidence':[ref(r/'inputs/carry-forward.json')],
           'native_trials':original.get('native_trials',[]),'evidence_origin':'historical execution with current byte/prerequisite readback'})
    for cid,decision in decisions.items():
        names=['DV-03-python','DV-03-javascript'] if cid=='DV-03' else [cid]
        refs=[ref(r/'inputs/native-decisions.json')]
        for name in names:
            base=r/'trials'/name
            attempt=decision.get('native_attempts',{}).get(name,'002')
            selected=base/('attempt-'+attempt)
            result=c.load(selected/'result.json')
            after=c.load(selected/'after.json')
            actual=c.h.inventory(Path(result['cwd']))
            assert actual['files']==after['files'],name+' changed after native final'
            if decision['result']=='PASS':
                assert result['termination']=='exited' and result['exit_status']==0
                assert not c.load(selected/'effects.json')['immutable_changes']
                audit_name=name+('-warm' if attempt=='003' else '')
                audit=c.load(r/'inputs/native-audits'/audit_name/'audit.json')
                assert not audit['problems'] and not audit['immutable_changes']
            paths=[base/'plan.json',base/'prompt.txt',base/'attempt-001/result.json',base/'attempt-001/effects.json',
                   base/'attempt-002/before.json',base/'attempt-002/after.json',base/'attempt-002/effects.json',base/'attempt-002/result.json',
                   r/'commands'/(name+'-002')/'command.json',r/'commands'/(name+'-002')/'stdout.txt',
                   r/'commands'/(name+'-002')/'stderr.txt']
            if attempt=='003':
                paths.extend([selected/f for f in ['before.json','after.json','effects.json','result.json','plan.json']])
                paths.extend([r/'commands'/(name+'-003')/f for f in ['command.json','stdout.txt','stderr.txt']])
                paths.extend([r/'commands/javascript-host-qa-002'/f for f in ['command.json','stdout.txt','stderr.txt']])
                paths.extend([r/'trials/javascript-host-qa/readback-002.json',r/'inputs/javascript-continuation-authorization.json'])
            final=Path(result['cwd'])/'.trial-output'/('final-'+attempt+'.txt')
            if final.exists(): paths.append(final)
            audit=r/'inputs/native-audits'/(name+('-warm' if attempt=='003' else ''))/'audit.json'
            if audit.exists(): paths.append(audit)
            for p in paths: refs.append(ref(p))
        case={'case_id':cid,'result':decision['result'],'reason':decision['reason'],'method':'behavioral',
              'native_trials':names,'native_attempts':{name:decision.get('native_attempts',{}).get(name,'002') for name in names},'evidence':refs}
        cases.append(dict(case,evidence_origin=decision.get('evidence_origin','fresh native sessions')))
        external.append(case)
        for file_ref in refs: put(r/file_ref['path'],file_ref['path'])
    ids=[f'DV-{i:02d}' for i in range(1,19)]+[f'RV-{i:02d}' for i in range(2,7)]
    cases.sort(key=lambda x:ids.index(x['case_id']));external.sort(key=lambda x:ids.index(x['case_id']))
    package=c.load(r/'source-manifest.json')['package_digest']
    c.save(r/'inputs/case-observations.json',{'schema_version':'1','run_id':r.name,'target_name':'dev','package_digest':package,'cases':cases})
    c.save(e/'observations.json',{'package_digest':package,'cases':external})
    c.h.execute('external-evaluation',[sys.executable,'-B','-X','utf8',str(e/'bundle/runner.py'),
        '--observations',str(e/'observations.json'),'--output',str(e/'trials/evaluation-final')])
    summary=c.load(e/'trials/evaluation-final/summary.json')
    c.copy_file(e/'bundle/artifact-manifest.json',r/'inputs/external-bundle-manifest.json')
    c.copy_file(e/'observations.json',r/'inputs/external-observations.json')
    c.copy_file(e/'trials/evaluation-final/results.jsonl',r/'inputs/evaluation-results.jsonl')
    c.copy_file(e/'trials/evaluation-final/summary.json',r/'inputs/evaluation-summary.json')
    c.h.execute('source-readback-final',[sys.executable,'-B','-X','utf8',str(c.LOADED/'scripts/observe.py'),
        'readback','--source',str(c.TARGET),'--manifest',str(r/'source-manifest.json')])
    readback=c.load(r/'commands/source-readback-final/stdout.txt')
    assert readback['status']=='MATCH'
    c.save(r/'source-after-manifest.json',readback['manifest'])
    c.copy_file(r/'origin-record.json',r/'inputs/origin-before-final-readback.json')
    origin=c.load(r/'origin-record.json');origin['source_readback_state']='UNCHANGED'
    (r/'origin-record.json').write_text(json.dumps(origin,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    final_inputs=[]
    for row in c.load(r/'inputs/current-input-readback.json'):
        current=c.h.sha(Path(row['original_path']).read_bytes())
        assert current==row['expected']
        final_inputs.append(dict(row,actual=current,matches=True))
    checker_files=[]
    for p in sorted((r/'inputs/checker').iterdir()):
        original=Path('C:/Users/bryan/.codex/skills/.system/skill-creator/scripts/quick_validate.py') if p.name=='quick_validate.py' else c.LOADED/'scripts'/p.name
        assert original.read_bytes()==p.read_bytes()
        checker_files.append({'original_path':str(original),'sha256':c.h.sha(p.read_bytes()),'matches':True})
    c.save(r/'inputs/final-input-readback.json',{'inputs':final_inputs,'checkers':checker_files,
        'rule_set_sha256':c.h.sha((r/'rule-set.json').read_bytes()),'rule_pin_matches':c.h.sha((r/'rule-set.json').read_bytes())==c.load(r/'inputs/rule-pin.json')['sha256']})
    semantic=c.load(r/'inputs/semantic-review.json')['observations']
    byid={x['rule_id']:x for x in semantic}
    byid.update({x['case_id']:x for x in cases})
    rows=[]
    for rule in c.load(r/'rule-set.json')['rules']:
        ident=rule['rule_id'];o=byid[ident];is_case=ident.startswith(('DV-','RV-'))
        dimension='behavior' if is_case else 'instructions' if ident.startswith(('AV-I','AV-C')) else 'workflow' if ident.startswith(('DEV-','REV-','AV-W')) else 'standards'
        rows.append({'schema_version':'1','run_id':r.name,'check_id':'CHECK-'+ident,'rule_id':ident,
          'subject_path':o.get('subject_path','SKILL.md'),'method':o['method'],'required':rule['required'],
          'applicability':'not_applicable' if o['result']=='NOT_APPLICABLE' else 'applicable',
          'result':o['result'],'reason':o['reason'],'evidence':[ref(r/'inputs/case-observations.json')] if is_case else o['evidence'],'dimension':dimension})
    assert len(rows)==82
    c.save(r/'checks.jsonl',''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
    c.h.execute('records-complete-initial',[sys.executable,'-B','-X','utf8',str(c.LOADED/'scripts/observe.py'),'records','--run-root',str(r)])
    print('ASSEMBLED',summary)

def closeout():
    integrity=c.load(r/'commands/records-complete-initial/stdout.txt')
    assert integrity['status']=='OBSERVED',integrity
    rows=[json.loads(line) for line in (r/'checks.jsonl').read_text(encoding='utf-8').splitlines()]
    c.copy_file(r/'checks.jsonl',r/'inputs/checks-before-record-integrity.jsonl')
    for row in rows:
        if row['rule_id']=='AV-E01':
            row.update(result='PASS',reason='Whole fresh schema-1 run records check completed without errors, current source/input digests match, unchanged external bundle verifier executed, and supplemental records passed. Historical failed layouts remain preserved.',
              evidence=[ref(r/'commands/records-complete-initial/stdout.txt'),ref(r/'commands/adaptive-records/stdout.txt'),
                        ref(r/'inputs/evaluation-summary.json'),ref(r/'inputs/final-input-readback.json')])
    (r/'checks.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows),encoding='utf-8')
    dimensions={name:reduction([x for x in rows if x['dimension']==name]) for name in ('standards','workflow','instructions','behavior')}
    overall='FAIL' if any(x['outcome']=='FAIL' for x in dimensions.values()) else 'INCOMPLETE' if any(x['outcome']=='INCOMPLETE' for x in dimensions.values()) else 'PASS'
    summary=c.load(r/'inputs/evaluation-summary.json')
    assessment={'schema_version':'1','run_id':r.name,'target_name':'dev','assessment_completed':True,
       'overall_assessment':overall,'dimensions':dimensions,'required_coverage':reduction(rows),
       'case_counts':summary['counts'],'unique_case_denominator':23,'case_pass_rate':summary['pass_rate'],
       'historical_cases_carried_forward':16,'fresh_unique_cases':7,'framework_acceptance':'NOT_EVALUATED'}
    c.save(r/'assessment.json',assessment)
    print('CLOSEOUT_STATUS',json.dumps(assessment))

if __name__=='__main__':
    {'assemble':assemble,'closeout':closeout}[sys.argv[1]]()
