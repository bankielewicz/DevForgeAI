"""Fresh continuation orchestration; never writes to skill packages or prior evidence."""
import concurrent.futures
import importlib.util
import json
from pathlib import Path
import shutil
import sys

RUN = Path(__file__).resolve().parent.parent
ROOT = RUN.parents[4]
PRIOR = RUN.with_name('20260914T0117324130584Z')
LOADED = ROOT / '.agents/skills/skill-validator'
SPEC = importlib.util.spec_from_file_location('retained_harness', PRIOR / 'qa_harness.py')
h = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(h)
h.RUN = RUN
TARGET = ROOT / 'src/agents/skills/dev'
IDS = ['DV-01','DV-02','DV-03-python','DV-03-javascript','DV-05','DV-08','DV-14','RV-04']
BUDGET = 900

def save(p,v):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf-8',newline='\n') as f:
        f.write(v if isinstance(v,str) else json.dumps(v,ensure_ascii=False,indent=2)+'\n')

def load(p):
    return json.loads(p.read_bytes())

def copy_file(src,dst):
    data=src.read_bytes()
    dst.parent.mkdir(parents=True,exist_ok=True)
    with dst.open('xb') as f: f.write(data)
    assert dst.read_bytes()==data

def setup():
    result=h.execute('intake',[sys.executable,'-B','-X','utf8',str(LOADED/'scripts/authoring_intake.py'),
        '--request',str(ROOT/'docs/plan/skill-authorings/dev/20260914T0117324130584Z/validation-request.json'),
        '--request-sha256','034887a39a8b5f12e0ca3bb27e2f87cba48b4f0f74335071ef2baf6b77d525af'])
    if result['exit_status']!=0: raise ValueError('Rejected intake')
    current=load(RUN/'source-manifest.json')
    old=load(PRIOR/'source-manifest.json')
    assert current['files']==old['files'] and current['package_digest']==old['package_digest']
    verified=[]
    for row in load(PRIOR/'final-artifact-manifest.json')['files']:
        src=PRIOR/row['path']
        assert h.sha(src.read_bytes())==row['sha256'] and src.stat().st_size==row['bytes'], str(src)
        verified.append(row)
    save(RUN/'inputs/prior-final-readback.json',{'prior_root':str(PRIOR),'verified':verified,'package_match':True})
    # Raw prior inputs and record families are explicitly data under inputs/.
    snap=h.inventory(PRIOR/'inputs',RUN/'inputs/prior-inputs')
    save(RUN/'inputs/prior-inputs-custody.json',snap)
    for name in ['sources.json','rule-set.json','workflow-map.json','checks.jsonl','case-observations-final.json',
                 'semantic-review-final.json','findings.json','handoff.json','validation-report.md',
                 'final-artifact-manifest.json','source-manifest.json','qa_harness.py','native_campaign.py']:
        copy_file(PRIOR/name,RUN/'inputs/prior-records'/name)
    for name in ['authoring_intake.py','observe.py','adaptive_observe.py','adaptive_contracts.py','text_resources.py']:
        copy_file(LOADED/'scripts'/name,RUN/'inputs/checker'/name)
    for name in ['adaptive-validation.md','rules.md','reporting.md','trials.md','set-trials.md']:
        copy_file(LOADED/'references'/name,RUN/'inputs/checker-references'/name)
    # Pin before new observations. Source references retain exact original input bytes.
    for name in ['sources.json','rule-set.json','workflow-map.json']:
        doc=load(PRIOR/name)
        def rebase(v):
            if isinstance(v,dict):
                for k,x in v.items():
                    if k=='run_id': v[k]=RUN.name
                    elif k in ('path','snapshot_path') and isinstance(x,str) and x.startswith('inputs/'):
                        v[k]='inputs/prior-inputs/'+x[7:]
                    else: rebase(x)
            elif isinstance(v,list):
                for x in v: rebase(x)
        rebase(doc)
        save(RUN/name,doc)
    request=ROOT/'docs/plan/skill-authorings/dev/20260914T0117324130584Z/validation-request.json'
    copy_file(request,RUN/'inputs/validation-request.json')
    copy_file(PRIOR/'host_probe.py',RUN/'inputs/host_probe.py')
    h.execute('host-probe',[sys.executable,'-B','-X','utf8',str(RUN/'inputs/host_probe.py')])
    plans=[]
    for name in IDS:
        old_plan=load(PRIOR/'trials'/name/'plan.json')
        fixture=Path(old_plan['fixture_origin'])
        actual=h.inventory(fixture)
        assert actual['files']==old_plan['fixture_manifest']['files'], name+' fixture changed'
        project=RUN/'trials'/name/'project'
        before=h.inventory(fixture,project)
        h.inventory(RUN/'source',project/'trial-skill/dev')
        (project/'.trial-output').mkdir()
        prompt=old_plan['task_prompt'].replace(old_plan['permitted_write_root'],str(project))
        plan=dict(old_plan,permitted_write_root=str(project),task_prompt=prompt,timeout_seconds=BUDGET,
                  fixture_manifest=before,predecessor_plan=str(PRIOR/'trials'/name/'plan.json'),
                  native_command=[shutil.which('codex'),'exec','--cd',str(project),'--sandbox','workspace-write',
                                  '--skip-git-repo-check','--json','--output-last-message',
                                  str(project/'.trial-output/final-001.txt'),'-'],
                  budget='One explicitly requested fresh attempt; 900 seconds; no automatic retry; no model override.')
        save(RUN/'trials'/name/'plan.json',plan)
        save(RUN/'trials'/name/'prompt.txt',prompt)
        plans.append({'trial_id':name,'case_id':plan['case_id'],'plan':str(RUN/'trials'/name/'plan.json'),
                      'prompt_sha256':h.sha(prompt.encode('utf-8'))})
    save(RUN/'inputs/native-plan.json',{'trials':plans,'timeout_seconds':BUDGET,'maximum_concurrent':2,
         'model_selection':'Inherited existing configured selection; no CLI model override.',
         'retry_policy':'No automatic retries. Sandbox startup failure requires explicit retained host escalation.',
         'isolation':'Workspace-write child policy and before/after observations; no independently proven OS isolation.',
         'case_denominator':23,'alias':{'RV-01':'DV-17'}})
    save(RUN/'inputs/layout-plan.json',{'raw_families':['inputs/','trials/'],
        'outer_records':'Only schema-1 records and run-relative references.',
        'external_bundle':'Separate sibling evaluation root with its own verifier; no change to evaluator source.',
        'record_checker':'Unchanged loaded observe.py records over whole new schema-1 run.',
        'carry_forward':'Only byte-verified prior PASS cases, same candidate, inputs, fixtures and prerequisites; explicitly labeled historical executions.'})
    save(RUN/'inputs/authorization.json',{'user_request':'Continue exact bound validation request and remaining work. Preserve evidence. No repair or installation.',
         'writes':['fresh run','fresh sibling evaluation data','disposable native trials'],
         'native_cases':IDS,'timeout_seconds':BUDGET,'no_model_override':True,'installation':'NOT_PERFORMED',
         'framework_acceptance':'NOT_EVALUATED'})
    print('SETUP_COMPLETE',RUN,flush=True)

def trial(name,attempt='001'):
    plan=load(RUN/'trials'/name/'plan.json')
    project=Path(plan['permitted_write_root'])
    base=RUN/'trials'/name/('attempt-'+attempt)
    before=h.inventory(project)
    save(base/'before.json',before)
    argv=list(plan['native_command'])
    argv[-2]=str(project/'.trial-output'/('final-'+attempt+'.txt'))
    result=h.execute(name+'-'+attempt,argv,cwd=project,stdin=plan['task_prompt'],timeout=BUDGET)
    after=h.inventory(project)
    save(base/'after.json',after)
    old={r['path']:r for r in before['files']}; new={r['path']:r for r in after['files']}
    changed=[p for p in sorted(old.keys()|new.keys()) if old.get(p)!=new.get(p)]
    protected=['trial-skill/','AGENTS.md','spec.md','consumer.md','unrelated.txt','delivery-draft.md']
    save(base/'effects.json',{'changed_paths':changed,'immutable_changes':[p for p in changed if any(p==x or p.startswith(x) for x in protected)],
         'exclusions':after['exclusions'],'command_receipt':str(RUN/'commands'/(name+'-'+attempt)/'command.json')})
    save(base/'result.json',result)
    print('COMPLETED',name,result['termination'],result['exit_status'],flush=True)

if __name__=='__main__':
    if sys.argv[1]=='setup': setup()
    elif sys.argv[1]=='batch':
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            futures=[pool.submit(trial,name) for name in sys.argv[2:]]
            for f in concurrent.futures.as_completed(futures): f.result()
    elif sys.argv[1]=='escalated':
        for name in sys.argv[2:]: trial(name,'002')
    else: trial(sys.argv[1])

