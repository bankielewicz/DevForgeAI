import datetime as dt
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import yaml

R = Path(__file__).parent.resolve()
S = R / 'source'
sys.path.insert(0, str(S / 'scripts'))
import authoring as a

def save(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def ref(p):
    return {'path': p.relative_to(R).as_posix(), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}

def stamp():
    return dt.datetime.now(dt.timezone.utc).isoformat()

save(R / 'environment.json', {'python': sys.version, 'platform': platform.platform(), 'pyyaml': yaml.__version__, 'shell': 'PowerShell 7', 'host': 'Codex task agent explicitly loading operational validator', 'delegation': 'not authorized', 'native_activation': 'NOT_RUN', 'installed_checker': 'NOT_RUN: request limits local reads to selected builder, operational validator and specification; personal checker outside selected inputs', 'write_root': str(R), 'read_only_target': str(R.parents[5] / 'skill-builder')})
sources = [dict(source_id='spec', original_path=str(R.parents[6] / 'inputs/skill-builder-authoring-enhancement-spec.md'), retrieved_at_utc=stamp(), snapshot_path='inputs/enhancement-spec.md', sha256=ref(R/'inputs/enhancement-spec.md')['sha256'], sections=['2', '3', '4', '5'], freshness='live_verified'), dict(source_id='standard', url='https://agentskills.io/specification', retrieved_at_utc=stamp(), snapshot_path='inputs/official-refresh.json', sha256=ref(R/'inputs/official-refresh.json')['sha256'], sections=['Frontmatter', 'name field', 'compatibility field'], freshness='snapshot_only', note='Exact prior assessment live retrieval reused without a new network refresh')]
save(R/'sources.json', {'schema_version':'1', 'run_id':R.name, 'sources':sources})
rules=[]
for ident,title,method,source in [('FMT','Valid package metadata','deterministic','standard'),('AB-009','Preserve valid identities','behavioral','spec'),('AB-008','Preserve unrelated UI metadata and invocation','behavioral','spec'),('AB-014','Honest authoring completion','behavioral','spec'),('CUSTODY','Parse inputs and preserve write custody','behavioral','spec'),('HISTORY','Preserve history, ownership and untested revision','behavioral','spec'),('INSTRUCTIONS','Consistent authoring-only workflow and preserved metadata','semantic','spec'),('WORKFLOW','Complete routed authoring workflows','semantic','spec'),('NATIVE','Acceptance workflow execution distinct from helper checks','behavioral','spec')]:
    path='inputs/enhancement-spec.md' if source=='spec' else 'inputs/official-refresh.json'
    rules.append(dict(rule_id=ident,revision='1',title=title,source_refs=[dict(**ref(R/path),source_id=source,locator='Sections 2-5' if source=='spec' else 'name/frontmatter fields')],authority_class='format_requirement' if source=='standard' else 'project_policy',applicability='applicable',method=method,expected_observation=title,required=True,limitation='Builder applicable requirements only; helper execution is not native model execution.'))
save(R/'rule-set.json', {'schema_version':'1','run_id':R.name,'rules':rules})
save(R/'rules-pinned.json', {'rule_set':ref(R/'rule-set.json'), 'pinned_at_utc':stamp(), 'note':'Before behavioral attempts; structural observation already collected as raw helper evidence.'})

CASES = {
 'create-repeat': ('HISTORY', 'Creation in a selected path with spaces and second untested edit publish AUTHORED with exact handoff.'),
 'observed-conflict': ('HISTORY', 'Observed edit preserves unrelated bytes; later divergent managed changes block without overwriting user bytes.'),
 'out-of-scope': ('CUSTODY', 'Candidate modification outside change_paths is rejected before target mutation.'),
 'source-drift': ('CUSTODY', 'Source changed after begin stops publish and retains after evidence.'),
 'name-64': ('AB-009', 'A valid existing 64-character identity remains editable without renaming.'),
 'malformed-contract': ('CUSTODY', 'known_issues=null is rejected before target writes with retained error evidence.'),
 'metadata': ('AB-008', 'Focused display edit preserves dependencies/policy/interface extras; explicit policy option changes only invocation; invalid option does not mutate.'),
 'initialize': ('WORKFLOW', 'Initializer creates only selected resources and refuses occupied destination with unchanged bytes.'),
 'adopt': ('HISTORY', 'Explicit adoption preserves target and next edit records prior origin adopted.'),
 'input-drift': ('CUSTODY', 'Changed referenced authoring input blocks publish before target writes.')
}
for cid,(rid,expected) in CASES.items():
    d=R/'trials'/cid
    d.mkdir(parents=True)
    project=d/'project with spaces'; project.mkdir()
    target=project/'custom skills'/'demo-skill'
    operation='create' if cid in ('create-repeat','input-drift','malformed-contract') else 'edit'
    if cid=='name-64': target=project/'custom skills'/('a'*64)
    if operation=='edit':
        target.mkdir(parents=True)
        (target/'SKILL.md').write_text('---\nname: '+target.name+'\ndescription: Synthetic assessment fixture.\n---\nBefore\n',encoding='utf-8')
        (target/'retained.txt').write_bytes(b'untouched user bytes\x00\xff')
    if cid=='adopt': operation='adopt'
    c=dict(schema_version='authoring-contract-v1',run_id=cid+'-001',project_root=str(project),target_root=str(target),target_name=target.name,operation=operation,authorization='Synthetic disposable assessment; author only SKILL.md in this case target.',history_review='no_known_history',change_paths=['SKILL.md'],requirements=[{'origin':'user','outcome':'Change synthetic instruction to After','artifacts':['SKILL.md']}],capabilities=[],expected_outputs=['Authored synthetic skill'],side_effects=[],inputs=[],known_issues=[])
    if cid=='malformed-contract': c['known_issues']=None
    if cid=='input-drift':
        inp=d/'input.md'; inp.write_text('Original contract input',encoding='utf-8'); c['inputs']=[a.reference(inp)]
    save(d/'contract.json',c)
    save(d/'fixture-before.json',a.manifest(a.files(target)) if target.exists() else a.manifest({}))
    save(d/'plan.json',dict(schema_version='1',case_id=cid,requirement_ids=[rid],fixtures=[ref(d/'contract.json'),ref(d/'fixture-before.json')],expected_outputs=expected,expected_effects='Only synthetic case descendants. Preserve failures; no retries.',executor='Python subprocess running selected snapshot helpers',exact_command=[sys.executable,'-B','-X','utf8',str(__file__)],procedure='Case branch '+cid+' in captured assessment_trials.py',timeout_seconds=120,permitted_write_root=str(d),input_package=ref(R/'source-manifest.json'),harness=ref(Path(__file__))))

results=[]
counts={}
def call(cid, script, *args):
    d=R/'trials'/cid
    n=counts.get(cid,0)+1; counts[cid]=n
    before=a.manifest(a.files(d/'project with spaces'))
    command=[sys.executable,'-B','-X','utf8',str(S/'scripts'/script),*map(str,args)]
    start=stamp()
    try:
        p=subprocess.run(command,cwd=d,capture_output=True,timeout=120)
        code=p.returncode; out=p.stdout; err=p.stderr; timeout=False
    except subprocess.TimeoutExpired as e:
        code=None; out=e.stdout or b''; err=e.stderr or b''; timeout=True
    label=f'attempt-{n:03d}'
    (d/(label+'.stdout.txt')).write_bytes(out); (d/(label+'.stderr.txt')).write_bytes(err)
    save(d/(label+'.before.json'),before)
    save(d/(label+'.after.json'),a.manifest(a.files(d/'project with spaces')))
    save(d/(label+'.json'),dict(schema_version='1',case_id=cid,command=command,cwd=str(d),start_utc=start,end_utc=stamp(),exit_code=code,timeout=timeout,stdout=ref(d/(label+'.stdout.txt')),stderr=ref(d/(label+'.stderr.txt')),before=ref(d/(label+'.before.json')),after=ref(d/(label+'.after.json'))))
    return code,out.decode('utf-8',errors='replace'),err.decode('utf-8',errors='replace')

for cid,(rid,expected) in CASES.items():
    d=R/'trials'/cid; c=json.loads((d/'contract.json').read_text()); target=Path(c['target_root']); run=Path(c['project_root'])/'docs/plan/authoring-001'
    observed={}
    if cid=='metadata':
        (target/'agents').mkdir()
        value={'interface':{'display_name':'Original','short_description':'Original description preserved here','default_prompt':'Use $demo-skill','icon_small':'./icon.svg'},'policy':{'allow_implicit_invocation':False,'extra':'keep'},'dependencies':{'tools':[{'type':'mcp','value':'synthetic'}]}}
        y=target/'agents/openai.yaml'; y.write_text(yaml.safe_dump(value),encoding='utf-8'); save(d/'metadata-fixture.json',value)
        code,*_=call(cid,'generate_openai_yaml.py',target,'--interface','display_name=Changed')
        wanted=json.loads(json.dumps(value)); wanted['interface']['display_name']='Changed'
        focused=code==0 and yaml.safe_load(y.read_text())==wanted
        code,*_=call(cid,'generate_openai_yaml.py',target,'--allow-implicit-invocation','true')
        wanted['policy']['allow_implicit_invocation']=True
        explicit=code==0 and yaml.safe_load(y.read_text())==wanted
        old=y.read_bytes(); code,*_=call(cid,'generate_openai_yaml.py',target,'--interface','unknown=x')
        passed=focused and explicit and code!=0 and y.read_bytes()==old
        observed={'focused_preserved':focused,'explicit_only_requested_change':explicit,'invalid_option_rejected':code!=0}
    elif cid=='initialize':
        stage=Path(c['project_root'])/'staging parent'
        code,*_=call(cid,'init_skill.py','scaffold-skill','--path',stage,'--resources','references')
        fresh=stage/'scaffold-skill'; first=a.files(fresh)
        code2,*_=call(cid,'init_skill.py','scaffold-skill','--path',stage)
        passed=code==0 and code2!=0 and first==a.files(fresh) and set(first)=={'SKILL.md','agents/openai.yaml'} and (fresh/'references').is_dir()
        observed={'creation_exit':code,'occupied_exit':code2,'files':list(first),'occupied_unchanged':first==a.files(fresh)}
    else:
        code,out,err=call(cid,'authoring.py','begin','--contract',d/'contract.json','--run-root',run)
        observed['begin_exit']=code
        if code!=0:
            passed=(cid=='malformed-contract' and not target.exists())
            observed['begin_error']=err
        else:
            if cid!='adopt': (run/'candidate/SKILL.md').write_text('---\nname: '+target.name+'\ndescription: Synthetic assessment fixture.\n---\nAfter\n',encoding='utf-8')
            if cid=='out-of-scope': (run/'candidate/retained.txt').write_bytes(b'wrong outside scope')
            if cid=='source-drift': (target/'SKILL.md').write_bytes(b'user drift after capture')
            if cid=='input-drift': (d/'input.md').write_text('Changed source',encoding='utf-8')
            code,out,err=call(cid,'authoring.py','publish','--run-root',run)
            observed.update(publish_exit=code,publish_stdout=out,publish_stderr=err)
            record=json.loads((run/'authoring-record.json').read_text()) if (run/'authoring-record.json').exists() else None
            observed['record_exists']=record is not None
            if cid=='malformed-contract':
                passed=code!=0 and not target.exists()
                observed['target_exists']=target.exists(); observed['target_files']=list(a.files(target)) if target.exists() else []
            elif cid in ('out-of-scope','source-drift','input-drift'):
                passed=code!=0 and record is not None and not record['applied_paths'] and not (run/'publication-readback.json').exists()
            else:
                passed=code==0 and record['authoring_state']=='AUTHORED' and record['validation_status']=='NOT_PERFORMED' and record['testing_status']=='NOT_PERFORMED'
                if cid in ('create-repeat','observed-conflict','adopt'):
                    if cid=='observed-conflict': (target/'SKILL.md').write_bytes(b'user divergent edit')
                    second=dict(c,run_id=cid+'-002',operation='edit',history_review='Verified just-published authoring baseline',prior=a.reference(run/'authoring-baseline.json'))
                    save(d/'contract-second.json',second); run2=run.parent/'authoring-002'
                    b,*_=call(cid,'authoring.py','begin','--contract',d/'contract-second.json','--run-root',run2)
                    (run2/'candidate/SKILL.md').write_bytes(b'second authorized candidate')
                    p,o,e=call(cid,'authoring.py','publish','--run-root',run2)
                    rr=json.loads((run2/'authoring-record.json').read_text())
                    observed.update(second_begin=b,second_publish=p,second_state=rr['authoring_state'],second_origin=rr['prior_origin'])
                    if cid=='observed-conflict': passed &= p!=0 and target.joinpath('SKILL.md').read_bytes()==b'user divergent edit' and rr['authoring_state']=='BLOCKED'
                    else: passed &= p==0 and rr['validation_status']=='NOT_PERFORMED' and (cid!='adopt' or rr['prior_origin']['kind']=='adopted')
                if (target/'retained.txt').exists(): passed &= (target/'retained.txt').read_bytes()==b'untouched user bytes\x00\xff'
    row=dict(case_id=cid,rule_id=rid,result='PASS' if passed else 'FAIL',expected=expected,observed=observed)
    save(d/'result.json',row); results.append(row)
save(R/'trial-results.json',{'schema_version':'1','results':results})
print(json.dumps(results,indent=2))
