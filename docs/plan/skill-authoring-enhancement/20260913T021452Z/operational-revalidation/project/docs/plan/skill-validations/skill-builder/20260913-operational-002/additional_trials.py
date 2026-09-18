import contextlib
import datetime as dt
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch
import yaml

R=Path(__file__).parent.resolve()
sys.path.insert(0,str(R/'source/scripts'))
import authoring as a
def save(p,x): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def ref(p): return {'path':p.relative_to(R).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def make(cid,op='create',name='demo-skill'):
    d=R/'trials'/cid; d.mkdir(); project=d/'project'; project.mkdir(); target=project/'selected development'/name
    c=dict(schema_version='authoring-contract-v1',run_id=cid,project_root=str(project),target_root=str(target),target_name=name,operation=op,authorization='Current revalidation request authorizes synthetic disposable assessment effects in this case.',history_review='no_known_history',change_paths=['SKILL.md'],requirements=[{'origin':'user','outcome':'Synthetic authoring case','artifacts':['SKILL.md']}],capabilities=[],expected_outputs=[],side_effects=[],inputs=[],known_issues=[])
    return d,project,target,c,project/'docs/plan/authoring-001'
def call(d,command):
    i=len(list(d.glob('attempt-*.json')))+1
    tag=f'attempt-{i:03d}'
    before=a.manifest(a.files(d/'project')); start=now()
    p=subprocess.run(command,cwd=d,capture_output=True,timeout=120)
    (d/(tag+'.stdout.txt')).write_bytes(p.stdout); (d/(tag+'.stderr.txt')).write_bytes(p.stderr)
    save(d/(tag+'.before.json'),before); save(d/(tag+'.after.json'),a.manifest(a.files(d/'project')))
    save(d/(tag+'.json'),dict(command=command,cwd=str(d),start_utc=start,end_utc=now(),exit_code=p.returncode,timeout=False,stdout=ref(d/(tag+'.stdout.txt')),stderr=ref(d/(tag+'.stderr.txt')),before=ref(d/(tag+'.before.json')),after=ref(d/(tag+'.after.json'))))
    return p
def cli(*args): return [sys.executable,'-B','-X','utf8',str(R/'source/scripts/authoring.py'),*map(str,args)]

# All inputs and independent expectations precede their first executed helper.
d,project,target,c,run=make('synthetic-import','import','csv-summary')
src=d/'claude-source'; (src/'scripts').mkdir(parents=True); (src/'references').mkdir()
front={'name':'csv-summary','description':'Summarize a supplied CSV into a JSON row count and header list. Use for a quick CSV inventory.','compatibility':'Requires Python 3.10 or later; local files only.','license':'MIT','metadata':{'author':'Synthetic Analyst','version':'1.2'},'model':'sonnet'}
body='\n# CSV summary\n\nRead a user-selected CSV. Ask for its path if absent. Use Read to inspect [the output contract](references/output.md). Run `python scripts/summarize.py INPUT` only when using this skill. Do not overwrite input. Return the JSON or a concrete parse error.\n'
(src/'SKILL.md').write_text('---\n'+yaml.safe_dump(front,sort_keys=False)+'---\n'+body,encoding='utf-8')
(src/'references/output.md').write_text('# Output contract\n\nReturn a JSON object with integer row_count and string-array headers. Missing input or invalid CSV returns a clear error without changing files.\n',encoding='utf-8')
(src/'scripts/summarize.py').write_text('import csv,json,sys\nwith open(sys.argv[1],newline="",encoding="utf-8") as f:\n    reader=csv.reader(f)\n    headers=next(reader,[])\n    print(json.dumps({"row_count":sum(1 for row in reader),"headers":headers}))\n',encoding='utf-8')
prompt='Import the supplied local Claude csv-summary skill into '+str(target)+'. Keep its CSV output behavior, local-file boundary and useful source metadata/resources. Return the authored development package and manual validator request. Do not run the imported skill or install it.'
(d/'task-prompt.txt').write_text(prompt,encoding='utf-8')
source_bytes=a.files(src); save(d/'source-before-manifest.json',a.manifest(source_bytes))
c.update(change_paths=list(source_bytes),inputs=[a.reference(src/p) for p in source_bytes],requirements=[{'origin':'user','outcome':'Import the selected CSV summarizer preserving its output contract and local-only effects; adapt Claude host instructions.','artifacts':list(source_bytes)}],capabilities=['read local CSV','execute bundled standard-library Python when the authored skill is later used'],expected_outputs=['JSON row_count and headers'],side_effects=['Reads explicitly selected local CSV during later skill use; no input writes'])
save(d/'contract.json',c)
save(d/'plan.json',dict(schema_version='1',case_id='synthetic-import',requirement_ids=['AB-008','AB-009','AB-014','INSTRUCTIONS'],fixtures=[ref(d/'source-before-manifest.json'),ref(d/'task-prompt.txt'),ref(d/'contract.json')],executor='Assessment agent performs a transparent host walkthrough using bundled authoring CLI; not an independent/blind builder agent',commands=[cli('begin','--contract',d/'contract.json','--run-root',run),cli('publish','--run-root',run)],harness=ref(Path(__file__)),expected='Preserve name, description, compatibility, license, metadata and resource bytes/output contract; remove Claude model override and adapt Read; do not execute imported script/checker/tests/validator. Publish digest-bound handoff with NOT_PERFORMED quality.',timeout_seconds=120,permitted_write_root=str(d)))
p1=call(d,cli('begin','--contract',d/'contract.json','--run-root',run))
assert p1.returncode==0
candidate=run/'candidate'
for path,content in source_bytes.items():
    out=candidate/path; out.parent.mkdir(parents=True,exist_ok=True); out.write_bytes(content)
new_front=dict(front); new_front.pop('model')
new_body=body.replace('Use Read to inspect','Use available local-file tools to inspect')
(candidate/'SKILL.md').write_text('---\n'+yaml.safe_dump(new_front,sort_keys=False)+'---\n'+new_body,encoding='utf-8')
save(d/'dispositions.json',{'SKILL.md':'Preserve supported metadata/output semantics; remove source-provider model and translate Read tool wording.','references/output.md':'Preserve exact bytes.','scripts/summarize.py':'Preserve exact bytes; do not execute during authoring.'})
p2=call(d,cli('publish','--run-root',run))
header=yaml.safe_load((target/'SKILL.md').read_text().split('---')[1])
record=json.loads((run/'authoring-record.json').read_text())
request=json.loads((run/'validation-request.json').read_text())
passed=p2.returncode==0 and header==new_front and all((target/p).read_bytes()==data for p,data in source_bytes.items() if p!='SKILL.md') and a.files(src)==source_bytes and record['authoring_state']=='AUTHORED' and record['validation_status']==record['testing_status']=='NOT_PERFORMED' and request['package_digest']==a.manifest(a.files(target))['package_digest']
save(d/'result.json',dict(case_id='synthetic-import',result='PASS' if passed else 'FAIL',metadata_preserved=header==new_front,source_unchanged=a.files(src)==source_bytes,imported_script_execution='NOT_RUN, as required during authoring',validator_invocation='NOT_RUN, manual request only',authoring_state=record['authoring_state'],handoff_digest_matches=request['package_digest']==a.manifest(a.files(target))['package_digest'],limitation='The assessment agent knows the prior findings. This is a realistic synthetic host walkthrough, not independent native/cold model execution.'))

d,project,target,c,run=make('record-write-failure')
save(d/'contract.json',c)
save(d/'plan.json',dict(schema_version='1',case_id='record-write-failure',requirement_ids=['CUSTODY','AB-014'],fixtures=[ref(d/'contract.json')],executor='Python direct helper API with bounded one-file save fault',command=[sys.executable,'-B','-X','utf8',str(__file__)],harness=ref(Path(__file__)),expected='After a real target write, injected authoring-record save OSError returns PARTIAL with actual SKILL.md applied path and delivered manifest, retains publication-failure, and publishes no usable baseline.',fault='Raise OSError only when save path basename is authoring-record.json; all other saves use original implementation.',timeout_seconds=120,permitted_write_root=str(d)))
p=call(d,cli('begin','--contract',d/'contract.json','--run-root',run)); assert p.returncode==0
(run/'candidate/SKILL.md').write_bytes(b'---\nname: demo-skill\ndescription: Fault recovery fixture\n---\nSynthetic content\n')
before=a.manifest(a.files(project)); start=now(); original=a.save
def fault(path,value):
    if path.name=='authoring-record.json': raise OSError('synthetic record publication write failure')
    return original(path,value)
stdout,stderr=io.StringIO(),io.StringIO()
with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr),patch.object(a,'save',side_effect=fault):
    result=a.publish(run)
save(d/'attempt-002.before.json',before); save(d/'attempt-002.after.json',a.manifest(a.files(project)))
(d/'attempt-002.stdout.txt').write_text(stdout.getvalue(),encoding='utf-8'); (d/'attempt-002.stderr.txt').write_text(stderr.getvalue(),encoding='utf-8')
save(d/'attempt-002.json',dict(command='authoring.publish(run) under the exact scoped save patch in additional_trials.py',executor='Python API call',cwd=str(d),start_utc=start,end_utc=now(),exit_code=None,api_return=result,timeout=False,stdout=ref(d/'attempt-002.stdout.txt'),stderr=ref(d/'attempt-002.stderr.txt'),before=ref(d/'attempt-002.before.json'),after=ref(d/'attempt-002.after.json')))
failure=json.loads((run/'publication-failure.json').read_text())
passed=result['state']=='PARTIAL' and result['applied_paths']==['SKILL.md'] and failure==result and not (run/'publication-readback.json').exists() and result['delivered_manifest']==a.manifest(a.files(target))
save(d/'result.json',dict(case_id='record-write-failure',result='PASS' if passed else 'FAIL',observed=result,retained_failure=failure,no_usable_publication=not (run/'publication-readback.json').exists()))
print(json.dumps({'synthetic_import':json.loads((R/'trials/synthetic-import/result.json').read_text()),'record_write_failure':json.loads((d/'result.json').read_text())},indent=2))
