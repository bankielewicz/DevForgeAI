"""Retain prior identities and reconstruct fresh unfinished scenarios without resetting them."""
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

RUN=Path(__file__).resolve().parent
PROJECT=RUN.parents[4]
PRIOR=RUN.with_name('20260917T185301Z')
VALIDATOR=PROJECT/'.agents/skills/skill-validator'
CODEX=Path('C:/Users/bryan/AppData/Local/Programs/OpenAI/Codex/bin/codex.exe')
TIMEOUT=1800

def put(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf-8',newline='\n') as stream:
        stream.write(value if isinstance(value,str) else json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n')

def ref(path):return {'path':str(path.resolve()),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}

def copy_file(source,dest,sha=None):
    data=source.read_bytes()
    if sha:assert hashlib.sha256(data).hexdigest()==sha,str(source)
    dest.parent.mkdir(parents=True,exist_ok=True)
    with dest.open('xb') as stream:stream.write(data)
    assert source.read_bytes()==dest.read_bytes()

def new_binding(project):
    return {'schema_version':'project-binding-v1','project_id':str(uuid.uuid4()),'project_root':str(project.resolve()),'revision':1,'bindings':[{'name':'story-create','package_path':'.agents/skills/story-create','package_digest':json.loads((RUN/'source-manifest.json').read_bytes())['package_digest'],'role':'core','selected':True}],'updated_at_utc':datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}

def plan(project,ident,prompt,requirements,expected_outputs,mutable=(),dependencies=None):
    case=project.parent
    put(case/'prompt.txt',prompt)
    dependencies=dependencies or {}
    value={'schema_version':'trial-plan-v1','case_id':ident,'kind':'native','argv':[str(CODEX),'exec','--cd',str(project),'--sandbox','workspace-write','--skip-git-repo-check','--json','--output-last-message',str(project/'.trial-output/final.txt'),'-'],'cwd':str(project),'permitted_write_root':str(project),'inputs':[ref(p) for p in sorted(project.rglob('*')) if p.is_file() and not any(p==project/m or p.is_relative_to(project/m) for m in mutable)],'prompt':ref(case/'prompt.txt'),'requirement_ids':requirements,'dependencies':list(dependencies),'dependency_attempts':dependencies,'timeout_seconds':TIMEOUT,'expected_outputs':expected_outputs}
    put(case/'plan.json',value)
    return value

def main():
    assert not (PROJECT/'.git').exists()
    old_manifest=json.loads((PRIOR/'source-manifest.json').read_bytes())
    new_manifest=json.loads((RUN/'source-manifest.json').read_bytes())
    assert old_manifest['files']==new_manifest['files'] and old_manifest['package_digest']==new_manifest['package_digest']
    originals=json.loads((PRIOR/'inputs/index.json').read_bytes())
    for row in originals:
        assert ref(Path(row['original_path']))['sha256']==row['sha256']
        copy_file(PRIOR/row['path'],RUN/row['path'],row['sha256'])
    copy_file(PRIOR/'inputs/index.json',RUN/'inputs/index.json')
    operational=[]
    for path in sorted((PRIOR/'evaluator').rglob('*')):
        if not path.is_file():continue
        rel=path.relative_to(PRIOR/'evaluator')
        original=Path('C:/Users/bryan/.codex/skills/.system/skill-creator/scripts/quick_validate.py') if rel.as_posix()=='installed-creator-quick_validate.py' else VALIDATOR/rel
        assert original.read_bytes()==path.read_bytes(),str(original)
        copy_file(path,RUN/'evaluator'/rel)
        operational.append(ref(original))
    for relative in ['rule-set.json','sources.json','guidance/openai-build-skills.md','semantic-review.md']:
        copy_file(PRIOR/relative,RUN/relative)
    receipts=[];diagnostic=[]
    for ident in ['N02','N03','N04','N05','N10','N12']:
        old=PRIOR/'trials'/ident
        result=json.loads((old/'attempt-001/result.json').read_bytes())
        assert result['timeout'] and result['cleanup']=='VERIFIED' and result['input_unchanged']
        receipts.append(ref(old/'attempt-001/result.json'))
        events=[]
        for line in (old/'attempt-001/stdout.txt').read_text(encoding='utf-8').splitlines():
            try:events.append(json.loads(line))
            except ValueError:pass
        messages=[e.get('item',{}).get('text','') for e in events if e.get('item',{}).get('type')=='agent_message']
        diagnostic.append({'case_id':ident,'timeout_seconds':600,'events':len(events),'terminal_turn_completed':any(e.get('type')=='turn.completed' for e in events),'last_progress_message':messages[-1] if messages else None,'changed_paths':result['changed_paths'],'limitation':'Event stream lacks complete per-event timing; no measured attribution of total time or root cause.'})
        oldplan=json.loads((old/'plan.json').read_bytes())
        expected=json.loads((old/'expected.json').read_bytes())
        init=expected.get('fixture_inputs',oldplan['inputs'])
        project=RUN/'trials'/ident/'project'
        for row in init:
            source=Path(row['path'])
            copy_file(source,project/source.relative_to(old/'project'),row['sha256'])
        (project/'backlog').mkdir(exist_ok=True)
        (project/'.trial-output').mkdir(exist_ok=True)
        bound=project/'.agents/devforgeai/project-binding.json'
        if bound.exists():bound.write_text(json.dumps(new_binding(project),indent=2)+'\n',encoding='utf-8')
        prompt=(old/'prompt.txt').read_text(encoding='utf-8').replace((old/'project').as_posix(),project.as_posix()).replace(str(old/'project'),str(project))
        value=plan(project,ident,prompt,oldplan['requirement_ids'],oldplan['expected_outputs'],mutable=['input/epic.md'] if ident=='N02' else [],dependencies=oldplan.get('dependency_attempts',{}))
        put(project.parent/'expected.json',{'case_id':ident,'prior_oracle':ref(old/'expected.json'),'oracle':expected.get('oracle',expected.get('expected')),'fixture_inputs':[ref(p) for p in sorted(project.rglob('*')) if p.is_file()],'prior_attempt':ref(old/'attempt-001/result.json'),'comparison':'Same selected task, original baseline files, candidate, model and effect scope. Paths and synthetic operational identity relocated; selected timeout is 1800 seconds. No prior produced output copied into a cold replay.'})
    put(RUN/'timeout-review.json',diagnostic)
    put(RUN/'continuation-plan.json',{'schema_version':'story-validation-continuation-v1','run_id':RUN.name,'prior_report':ref(PRIOR.with_name(PRIOR.name+'-records')/'validation-report.md'),'target_digest':new_manifest['package_digest'],'authorization':'User: continue with validation until its complete. Fresh disposable native attempts and remaining failure scenarios; no target/operational repair or installation.','timeout_selection':{'old_native_seconds':600,'new_native_seconds':TIMEOUT,'utility_seconds':120,'rationale':'Six retained attempts reached the default while still drafting/verifying. Select a bounded 30-minute window before fresh execution, rather than alter any started attempt. This is not a product performance criterion.','limits':'One declared fresh replay for each unfinished case; further attempts require a diagnosed localized problem and recorded selection. No silent ceiling change.'},'required_remaining_cases':['N02','N03','N04','N05','N10','N12','N13','G01','G02','G03'],'prior_pass_cases':['N01','N06','N07','N08','N09','N11','N14','N15'],'prior_receipts':receipts,'selected_rule_set':ref(RUN/'rule-set.json'),'operational_inputs':operational,'native_concurrency':2,'source_files_unchanged':16,'original_input_files_unchanged':len(originals),'status':'PREPARED','interpretation':'Count each logical required case once in current assessment; preserve earlier attempt outcomes and distinguish continuation evidence from historical campaign results.'})
    for name,args in [('codex-version',[str(CODEX),'--version']),('codex-help',[str(CODEX),'exec','--help'])]:
        result=subprocess.run(args,capture_output=True,timeout=120)
        put(RUN/(name+'.stdout.txt'),result.stdout.decode('utf-8'))
        put(RUN/(name+'.stderr.txt'),result.stderr.decode('utf-8'))
        put(RUN/(name+'.execution.json'),{'argv':args,'exit_code':result.returncode})
        assert result.returncode==0
    print(json.dumps({'run':str(RUN),'native_timeout_seconds':TIMEOUT,'fresh_replays':6,'target_digest':new_manifest['package_digest'],'preserved_inputs':len(originals)}))

if __name__=='__main__':main()
