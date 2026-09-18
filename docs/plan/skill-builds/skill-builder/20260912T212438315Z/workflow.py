"""Bounded authorized evidence operations. Each CLI stage has fresh receipts."""
import datetime as dt
import json
import platform
import subprocess
import sys
from pathlib import Path
from preflight import ROOT, RUN, PACKET, TARGET, capture, sha
from prepare_origin import ORIGIN

BUILDER = ROOT / '.agents/skills/skill-builder'
CHECKER = Path('C:/Users/bryan/.codex/skills/.system/skill-creator/scripts/quick_validate.py')
RID = RUN.name
PY = [sys.executable, '-B', '-X', 'utf8']
AUTH = '''Use $skill-builder from C:\\Projects\\DevForgeAI\\.agents\\skills\\skill-builder\\SKILL.md. Complete the reviewed correction to the skill-builder development package, establish the required provenance through the applicable workflow, and then revalidate the delivered result.
I approve the exact revision specification identified above, including REV-001 through REV-003.
This instruction authorizes: The specified development-package revision. Required evidence capture, evaluation, disposable verification trials, and readback. Explicit adoption if the applicable verified history requires that operation. Fresh validation after successful delivery.
If no valid baseline exists and adoption is appropriate, this instruction explicitly authorizes adoption and management of the exact 36 paths listed in the digest-bound source manifest. Preserve all target bytes during adoption.
Use the assessment's origin record and retained specifications. If adoption requires a standalone as-observed origin specification, prepare it from the verified current bytes, retain the known defect, and have an independent agent review its fidelity before using it.
Make only the correction prescribed by the approved specification: Replace the stale three actual trials summary in references/evidence-format.md with the specified reference to all applicable required independent forward trials. Update only the corresponding artifact digest in evals/build-manifest.json.
Approved revision specification SHA-256: 9b8570392db9ed2128a71d820ba3710f58a000749db3f0ca0b780e33da28248c. Recorded manifest SHA-256: b6f1611978c00ec7a9898e01d93fe83a4f06bf4ad8a7d4a4f3931f9d421c81a6. Recorded target package digest: dab87685715689251365514f5c0f3df5c2a9b66c5367bf065ad62c903e8dfca3.
Selected verbatim authorization passages plus exact user-selected identities; the full conversation is the authorization source.'''

def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream: stream.write(data)
def js(path, value): write(path, (json.dumps(value, indent=2, ensure_ascii=False)+'\n').encode())
def read(path): return json.loads(path.read_bytes())
def ref(root, path): return {'path': path.relative_to(root).as_posix(), 'sha256': sha(path.read_bytes())}
def treecopy(source, dest):
    rows, excluded = capture(source)
    assert not excluded
    for r in rows:
        data = (source/r['path']).read_bytes()
        assert sha(data) == r['sha256']
        write(dest/r['path'], data)
    assert capture(dest)[0] == rows
    return rows
def unchanged():
    rows, excluded = capture(TARGET)
    assert not excluded and rows == read(PACKET/'source-manifest.json')['files'], 'SOURCE_CHANGED target'
    check_inputs()
    return rows
def check_inputs():
    for filename, digest in [('revision-spec.md','9b8570392db9ed2128a71d820ba3710f58a000749db3f0ca0b780e33da28248c'), ('source-manifest.json','b6f1611978c00ec7a9898e01d93fe83a4f06bf4ad8a7d4a4f3931f9d421c81a6')]:
        assert sha((PACKET/filename).read_bytes()) == digest, 'SOURCE_CHANGED '+filename
def command(base, label, args, fixtures=(), expected=0):
    trial = base/'commands'/label
    trial.mkdir(parents=True, exist_ok=False)
    snapshots=[]
    for i, item in enumerate(fixtures):
        item=Path(item)
        dest=trial/'inputs'/str(i)
        if item.is_dir():
            rows=treecopy(item,dest)
            snapshots.append({'original':str(item),'snapshot':str(dest),'files':rows})
        else:
            write(dest/item.name,item.read_bytes())
            snapshots.append({'original':str(item),'snapshot':str(dest/item.name),'sha256':sha(item.read_bytes())})
    plan={'schema_version':'1','case_id':label,'command':list(map(str,args)),'cwd':str(ROOT),'timeout_seconds':120,'expected_exit':expected,'input_snapshots':snapshots,'permitted_write_root':str(base),'start_planned':now()}
    js(trial/'plan.json',plan)
    started=now()
    try:
        result=subprocess.run(list(map(str,args)),cwd=ROOT,capture_output=True,timeout=120)
        out,err,code=result.stdout,result.stderr,result.returncode
    except subprocess.TimeoutExpired as exc:
        out,err,code=exc.stdout or b'',exc.stderr or b'',None
    write(trial/'stdout.txt',out); write(trial/'stderr.txt',err)
    observation={'schema_version':'1','started':started,'finished':now(),'exit_code':code,'expected_exit':expected,'stdout_sha256':sha(out),'stderr_sha256':sha(err)}
    js(trial/'attempt-001.json',observation)
    print(label,code,out.decode('utf-8',errors='replace')[:1200],err.decode('utf-8',errors='replace')[:1200],flush=True)
    assert code==expected, 'command did not match: '+label
    return out,trial

def adoption_prepare():
    rows=unchanged()
    assert (RUN/'independent-history/history-review.json').exists(), 'history review prerequisite'
    review_dir=ORIGIN/'independent-origin-review'
    assert review_dir.is_dir(), 'independent origin review prerequisite'
    # Root checks signed-to-byte review conclusions before this stage.
    root=ORIGIN/'candidate'; ev=root/'adoption/evidence'
    treecopy(ORIGIN/'origin-inputs',ev/'origin-inputs')
    treecopy(review_dir,ev/'origin-review')
    treecopy(RUN/'independent-history',ev/'history-review')
    treecopy(TARGET,ev/'snapshot'); treecopy(TARGET,root/'adoption/destination')
    js(ev/'snapshot-manifest.json',{'schema_version':'1','files':rows})
    js(ev/'managed-manifest.json',{'schema_version':'1','files':rows})
    write(ev/'authorization.txt',AUTH.encode())
    for name in ['validation-report.md','handoff.json','origin-record.json','revision-spec.md','source-manifest.json','findings.json']:
        write(ev/'selected-assessment'/name,(PACKET/name).read_bytes())
    origin=ev/'origin-inputs/origin-spec.md'
    current=unchanged()
    js(ev/'source-readback.json',{'schema_version':'1','run_id':RID+'-adoption','target_root':str(TARGET),'before':rows,'after':current,'spec_before_sha256':sha(origin.read_bytes()),'spec_after_sha256':sha((ORIGIN/'origin-inputs/origin-spec.md').read_bytes()),'outcome':'UNCHANGED'})
    record={'schema_version':'1','record_kind':'adoption','run_id':RID+'-adoption','target_name':'skill-builder','target_root':str(TARGET),'project_root':str(ROOT),'captured_at_utc':now(),'historical_origin':'unknown','snapshot_root':'adoption/evidence/snapshot','snapshot_manifest':ref(root,ev/'snapshot-manifest.json'),'managed_manifest':ref(root,ev/'managed-manifest.json'),'managed_paths':[r['path'] for r in rows],'retained_user_paths':[],'origin_spec':ref(root,origin),'origin_spec_input':{'resolved_path':str(ORIGIN/'origin-inputs/origin-spec.md'),'bytes':len(origin.read_bytes()),'sha256':sha(origin.read_bytes())},'authorization':{'instruction':AUTH,'target_root':str(TARGET),'managed_manifest_sha256':sha((ev/'managed-manifest.json').read_bytes()),'origin_spec_sha256':sha(origin.read_bytes())},'prior_evidence':[ref(root,ev/'selected-assessment/origin-record.json')],'quality_evidence':[ref(root,ev/'selected-assessment/validation-report.md'),ref(root,ev/'selected-assessment/findings.json')],'source_readback':ref(root,ev/'source-readback.json'),'known_defects':['F-8c43eca6259d05a2153068b5d5b29495d0c208229c2a19f49bc71355d8df2d1f: stale three-trial reporting summary retained unchanged.']}
    js(ev/'adoption-request.json',{'operation':'adopt','record':record})
    out,_=command(ORIGIN,'adoption-plan',PY+[BUILDER/'scripts/build_evidence.py','adoption-plan','--snapshot-root',root,'--request','adoption/evidence/adoption-request.json'],[root,BUILDER])
    write(ev/'adoption-record.json',out)
    command(ORIGIN,'structural',PY+[CHECKER,TARGET],[TARGET,CHECKER])
    cases=ORIGIN/'adoption-cases.jsonl'
    write(cases,(json.dumps({'case_id':'adopt-exact-36','grader_id':'adoption_consistency','params':{'evidence':'adoption/evidence','destination':'adoption/destination'},'expected':'PASS'})+'\n').encode())
    evaluator=root/'adoption/evidence/snapshot'
    command(ORIGIN,'adoption-v1',PY+[evaluator/'scripts/run_evaluation.py','--package-root',evaluator,'--candidate-root',root,'--cases',cases,'--output',ORIGIN/'adoption-results.jsonl','--run-id',RID+'-adoption','--profile','adoption-v1'],[root,cases])
    assert all(r['status']=='PASS' for r in map(json.loads,(ORIGIN/'adoption-results.jsonl').read_text().splitlines()))
    measured,_=capture(root)
    prior_snapshot=ORIGIN/'commands/adoption-v1/inputs/0'
    assert measured==capture(prior_snapshot)[0], 'evaluator input drift'
    js(ORIGIN/'evaluated-input-readback.json',{'outcome':'UNCHANGED','files':measured,'results':ref(ORIGIN,ORIGIN/'adoption-results.jsonl')})

def adoption_publish():
    root=ORIGIN/'candidate'; ev=root/'adoption/evidence'
    assert read(ORIGIN/'evaluated-input-readback.json')['outcome']=='UNCHANGED'
    assert capture(root)[0]==read(ORIGIN/'evaluated-input-readback.json')['files']
    rows=unchanged()
    assert (ORIGIN/'origin-inputs/origin-spec.md').read_bytes()==(ev/'origin-inputs/origin-spec.md').read_bytes()
    pointer={'schema_version':'2','run_id':RID+'-adoption','target_name':'skill-builder','origin':{'kind':'adopted',**ref(root,ev/'adoption-record.json')},'baseline':[{'path':r['path'],'sha256':r['sha256']} for r in rows]}
    js(ev/'active-baseline.json',pointer)
    assert read(ev/'active-baseline.json')==pointer
    js(ORIGIN/'publication-readback.json',{'schema_version':'1','published_at':now(),'publication':'PUBLISHED','readback':'UNCHANGED','pointer':ref(root,ev/'active-baseline.json'),'record':ref(root,ev/'adoption-record.json'),'target_files':unchanged(),'evaluation':ref(ORIGIN,ORIGIN/'adoption-results.jsonl'),'relative_reference_root':str(root)})
    write(ORIGIN/'adoption-report.md',b'# Adoption observation\n\nRecording: ADOPTED. Publication: PUBLISHED, with successful readback. All 36 authorized managed files and target bytes remain unchanged. Historical origin remains unknown; the stale three-trial reporting defect remains. Installed structural checker and adoption-v1 each exited 0. See commands/, adoption-results.jsonl and publication-readback.json. No generated baseline or skill-quality PASS is claimed.\n')
    print('Adoption published and read back; target unchanged.')

def contract_prepare():
    assert read(ORIGIN/'publication-readback.json')['publication']=='PUBLISHED'
    rows=unchanged()
    root=RUN/'working'; ev=root/'revision/evidence'
    treecopy(ORIGIN/'candidate',root)
    # Carry the complete original relative layout without rewriting history.
    for name in ['revision-spec.md','handoff.json','source-manifest.json','validation-report.md','origin-record.json']:
        write(root/'revision/inputs'/name,(PACKET/name).read_bytes())
    write(root/'revision/inputs/authorization.txt',AUTH.encode())
    inputs=[]
    for ident,name,role in [('approved-spec','revision-spec.md','spec'),('selected-handoff','handoff.json','handoff'),('approved-manifest','source-manifest.json','manifest'),('authorization','authorization.txt','authorization')]:
        path=root/'revision/inputs'/name
        original=PACKET/name if name!='authorization.txt' else path
        inputs.append({'id':ident,'path':path.relative_to(root).as_posix(),'resolved_path':str(original),'role':role,'bytes':len(path.read_bytes()),'sha256':sha(path.read_bytes())})
    spec=(PACKET/'revision-spec.md').read_bytes()
    allpaths=[r['path'] for r in rows]
    reqs=[]
    for ident,paths,method,expected in [('REV-001',['references/evidence-format.md'],'Contextual review and exact literal delta','Approved row links all applicable required independent trials; detailed four families and routing unchanged.'),('REV-002',allpaths,'Complete B/C/N/delivered path and byte comparison','Exactly two authorized files differ, no additions/removals, all other bytes preserved.'),('REV-003',['evals/build-manifest.json'],'Installed structural checker and explicit revision-spec-v2 evaluation','Manifest changes only corresponding artifact digest; profile/grader/script/schema identities retained.')]:
        start=spec.index((ident+' (required').encode()); end=spec.index(b'\n',start)
        reqs.append({'id':ident,'origin':'source','text':spec[start:end].decode().strip(),'source_refs':[{'input_id':'approved-spec','start_byte':start,'end_byte':end,'sha256':sha(spec[start:end])}],'artifact_paths':paths,'verification':[{'method':method,'expected':expected}]})
    contract={'schema_version':'1','mode':'spec_build','target_name':'skill-builder','inputs':inputs,'authorization':{'instruction':AUTH,'inputs':[{'id':i['id'],'sha256':i['sha256']} for i in inputs]},'purpose':'Apply only approved REV-001 wording correction and REV-003 manifest digest while preserving the entire observed package contract under REV-002. Adopted origin supplies B; no optional enhancements.','activation':{'positive':['Explicit approved specification revision of existing skill-builder from verified published adoption.'],'excluded':['Validation-only invocation','New-package spec-v1 build','Optional enhancements','Operational installation']},'requirements':reqs,'artifacts':[{'path':p,'role':'entrypoint' if p=='SKILL.md' else p.split('/')[0],'requirement_ids':[r['id'] for r in reqs if p in r['artifact_paths']],'purpose':'Preserve exact observed interface and behavior; only selected editorial row and corresponding digest may change.'} for p in allpaths],'workers':[{'role':'origin_fidelity','responsibility':'Independent byte-bound as-observed origin review before adoption','write_scope':'external review evidence only','isolation':'Task assignment, not enforced process isolation.'}],'dependencies':[{'name':'Python','observed':platform.python_version(),'purpose':'Required existing evaluator; no new runtime behavior.'},{'name':'PyYAML','purpose':'Already available for installed checker.'},{'name':'host delegation','purpose':'Independent fidelity review and bounded fresh validation trials available.'}]}
    js(ev/'build-contract.json',contract)
    js(RUN/'contract-created.json',{'timestamp':now(),'contract':ref(root,ev/'build-contract.json'),'candidate_generated':False,'adoption_publication':ref(ORIGIN,ORIGIN/'publication-readback.json'),'applicability':{'structural':'required candidate and delivery','revision-spec-v2':'required candidate, delivered bytes and publication','changed_scripts':'NOT_APPLICABLE: zero changed scripts','four_family_enhancement_campaign':'NOT_APPLICABLE to wording-only revision; substantial-change condition absent; requirements preserved byte-for-byte','fresh_validation':'required after delivery; separate bounded independent cold workflow and predeclared routing assessment'}})
    print('Digest-bound contract created before candidate generation.')

def candidate_generate():
    root=RUN/'working'; ev=root/'revision/evidence'
    assert ref(root,ev/'build-contract.json')==read(RUN/'contract-created.json')['contract']
    rows=unchanged()
    treecopy(root/'adoption/evidence/snapshot',root/'revision/B')
    treecopy(TARGET,root/'revision/C')
    treecopy(TARGET,root/'revision/N')
    treecopy(TARGET,root/'revision/after')
    path=root/'revision/N/references/evidence-format.md'
    old=path.read_bytes()
    needle=b'| Independent forward trials | `NOT_PERFORMED`, `PASSED`, `FAILED`; builder enhancements require the three actual trials in the evaluation reference. |'
    replacement=b'| Independent forward trials | `NOT_PERFORMED`, `PASSED`, `FAILED`; builder enhancements require all applicable independent forward trials specified in [evaluation.md](evaluation.md#required-forward-trials-for-builder-enhancements). |'
    assert old.count(needle)==1
    new=old.replace(needle,replacement)
    path.write_bytes(new)
    manifest=root/'revision/N/evals/build-manifest.json'
    before=manifest.read_bytes()
    assert before.count(sha(old).encode())==1
    manifest.write_bytes(before.replace(sha(old).encode(),sha(new).encode()))
    nrows=capture(root/'revision/N')[0]
    delta=[r['path'] for r in nrows if r!=next(b for b in rows if b['path']==r['path'])]
    assert delta==['evals/build-manifest.json','references/evidence-format.md']
    js(RUN/'candidate-delta.json',{'timestamp':now(),'changed_paths':delta,'before':rows,'candidate':nrows,'edit':'one literal row replacement and one SHA-256 substitution; no newline normalization'})
    origin=ref(root,root/'adoption/evidence/adoption-record.json')
    pointer=ref(root,root/'adoption/evidence/active-baseline.json')
    request={'schema_version':'2','run_id':RID,'baseline':'revision/B','current':'revision/C','candidate':'revision/N','after':'revision/after','required_paths':[r['path'] for r in rows],'owned_paths':[r['path'] for r in rows],'prior_origin':{'kind':'adopted',**origin},'adoption_origin':origin,'baseline_before':pointer,'baseline_after':pointer}
    js(ev/'revision-request.json',request)
    out,_=command(RUN,'revision-plan',PY+[BUILDER/'scripts/build_evidence.py','revision-plan','--snapshot-root',root,'--request','revision/evidence/revision-request.json'],[root,BUILDER])
    write(ev/'revision-plan.json',out)
    command(RUN,'candidate-structural',PY+[CHECKER,root/'revision/N'],[root/'revision/N',CHECKER])
    provenance(root,False,'Candidate structural check exited 0; B/C/N preview PLANNED; target remains unchanged.',root/'revision/C')
    evaluate('candidate',root,root/'revision/N')

def provenance(root,complete,observation,destination):
    ev=root/'revision/evidence'; contract=read(ev/'build-contract.json')
    outputs=capture(destination)[0]; n={r['path']:r for r in capture(root/'revision/N')[0]}
    obs={'schema_version':'1','run_id':RID,'target_name':'skill-builder','outputs':[{'path':r['path'],'sha256':r['sha256']} for r in outputs],'observed_at':now(),'observation':observation}
    js(ev/'preceding-observation.json',obs)
    origin=ref(root,root/'adoption/evidence/adoption-record.json')
    obj={'schema_version':'2','run_id':RID,'mode':'spec_build','target_name':'skill-builder','builder_manifest_sha256':sha((root/'revision/N/evals/build-manifest.json').read_bytes()),'contract_sha256':sha((ev/'build-contract.json').read_bytes()),'inputs':[{'id':i['id'],'sha256':i['sha256']} for i in contract['inputs']],'dependencies':contract['dependencies'],'outputs':[{'path':r['path'],'sha256':r['sha256'],'ownership':'generated','baseline_path':'revision/N/'+r['path'],'baseline_sha256':n[r['path']]['sha256']} for r in outputs],'mappings':[{'requirement_id':r['id'],'artifact_paths':r['artifact_paths'],'evidence_ids':['preceding-observation']} for r in contract['requirements']],'evidence':[{'id':'preceding-observation',**ref(root,ev/'preceding-observation.json')}],'prior_origin':{'kind':'adopted',**origin},'adoption_origin':origin,'result':'COMPLETE' if complete else 'INCOMPLETE'}
    js(ev/'build-provenance.json',obj)

def evaluate(label,root,evaluator):
    cases=RUN/(label+'-cases.jsonl')
    rows=[{'case_id':label+'-links','grader_id':'package_links','params':{'path':'revision/N' if label=='candidate' else 'revision/after'},'expected':'PASS'},{'case_id':label+'-traceability','grader_id':'build_traceability_v2','params':{'evidence':'revision/evidence','destination':'revision/after'},'expected':'PASS'},{'case_id':label+'-revision','grader_id':'revision_consistency_v2','params':{'path':'revision/evidence/revision-plan.json'},'expected':'PASS'}]
    write(cases,(''.join(json.dumps(r)+'\n' for r in rows)).encode())
    command(RUN,label+'-revision-spec-v2',PY+[evaluator/'scripts/run_evaluation.py','--package-root',evaluator,'--candidate-root',root,'--cases',cases,'--output',RUN/(label+'-results.jsonl'),'--run-id',RID+'-'+label,'--profile','revision-spec-v2'],[root,cases,evaluator])
    assert capture(root)[0]==capture(RUN/'commands'/(label+'-revision-spec-v2')/'inputs/0')[0]
    js(RUN/(label+'-input-readback.json'),{'outcome':'UNCHANGED','inputs':capture(root)[0],'results':ref(RUN,RUN/(label+'-results.jsonl'))})

def next_stage(source,dest):
    rows,excluded=capture(source)
    assert not excluded
    omitted={'revision/evidence/build-provenance.json','revision/evidence/preceding-observation.json','revision/evidence/revision-plan.json'}
    for row in rows:
        if row['path'] in omitted or row['path'].startswith('revision/after/'):
            continue
        data=(source/row['path']).read_bytes()
        assert sha(data)==row['sha256']
        write(dest/row['path'],data)

def deliver():
    source=RUN/'working'
    assert read(RUN/'candidate-input-readback.json')['outcome']=='UNCHANGED'
    assert capture(source)[0]==read(RUN/'candidate-input-readback.json')['inputs']
    before=unchanged()
    assert before==capture(source/'revision/C')[0]
    delta=read(RUN/'candidate-delta.json')['changed_paths']
    assert delta==['evals/build-manifest.json','references/evidence-format.md']
    receipt={'schema_version':'1','started':now(),'target':str(TARGET),'before':before,'applied_paths':[],'mutations':[],'status':'IN_PROGRESS'}
    js(RUN/'delivery-before.json',receipt)
    try:
        for rel in delta:
            target=TARGET/rel
            assert target.resolve().is_relative_to(TARGET.resolve())
            assert target.read_bytes()==(source/'revision/C'/rel).read_bytes(),'SOURCE_CHANGED affected path'
            data=(source/'revision/N'/rel).read_bytes()
            target.write_bytes(data)
            receipt['applied_paths'].append(rel)
            assert target.read_bytes()==data
            receipt['mutations'].append({'path':rel,'timestamp':now(),'sha256':sha(data),'readback':'UNCHANGED'})
        after,excluded=capture(TARGET)
        assert not excluded and after==capture(source/'revision/N')[0]
        check_inputs()
        receipt.update(status='DELIVERED_AWAITING_EVALUATION',after=after,finished=now())
    except Exception as exc:
        receipt.update(status='PARTIAL',error=repr(exc),after=capture(TARGET)[0],finished=now())
        js(RUN/'delivery-attempt-001.json',receipt)
        raise
    js(RUN/'delivery-attempt-001.json',receipt)
    root=RUN/'delivered-stage'; next_stage(source,root)
    treecopy(TARGET,root/'revision/after')
    plan=read(source/'revision/evidence/revision-plan.json')
    plan.update(status='PARTIAL',applied_paths=delta,baseline_advanced=False,readback_passed=False,evaluation_passed=False)
    js(root/'revision/evidence/revision-plan.json',plan)
    command(RUN,'delivered-structural',PY+[CHECKER,TARGET],[TARGET,CHECKER])
    provenance(root,False,'Actual two-file delivery read back; structural checker exited 0. Intermediate PARTIAL machine state prevents success before delivered evaluation.',TARGET)
    evaluate('delivered',root,TARGET)
    assert capture(TARGET)[0]==after
    js(RUN/'delivered-readback.json',{'schema_version':'1','timestamp':now(),'outcome':'UNCHANGED','files':after,'spec_sha256':sha((PACKET/'revision-spec.md').read_bytes()),'actual_delta':delta,'structural_exit':0,'revision_profile_exit':0,'prior_baseline_advanced':False})

def publish_revision():
    source=RUN/'delivered-stage'
    actual=read(RUN/'delivered-readback.json')
    assert actual['outcome']=='UNCHANGED'
    check_inputs()
    assert capture(TARGET)[0]==actual['files']==capture(source/'revision/N')[0]
    assert capture(source)[0]==read(RUN/'delivered-input-readback.json')['inputs']
    root=RUN/'published'; next_stage(source,root)
    treecopy(TARGET,root/'revision/after')
    ev=root/'revision/evidence'
    provenance(root,True,'Actual target delivery and installed structural checker passed; delivered revision-spec-v2 exited 0; complete live target and approved inputs re-read unchanged before publication.',TARGET)
    pointer={'schema_version':'2','run_id':RID,'target_name':'skill-builder','origin':{'kind':'generated',**ref(root,ev/'build-provenance.json')},'baseline':[{'path':r['path'],'sha256':r['sha256']} for r in capture(root/'revision/N')[0]]}
    js(ev/'active-baseline.json',pointer)
    assert read(ev/'active-baseline.json')==pointer
    plan=read(source/'revision/evidence/revision-plan.json')
    plan.update(status='APPLIED',readback_passed=True,evaluation_passed=True,baseline_advanced=True,baseline_after=ref(root,ev/'active-baseline.json'))
    js(ev/'revision-plan.json',plan)
    js(RUN/'pointer-publication-readback.json',{'schema_version':'1','timestamp':now(),'publication':'PUBLISHED','readback':'UNCHANGED','reference_root':str(root),'pointer':ref(root,ev/'active-baseline.json'),'provenance':ref(root,ev/'build-provenance.json'),'target_files':capture(TARGET)[0]})
    evaluate('published',root,TARGET)
    assert capture(TARGET)[0]==actual['files']
    check_inputs()
    js(RUN/'final-delivery-readback.json',{'schema_version':'1','timestamp':now(),'outcome':'UNCHANGED','files':capture(TARGET)[0],'published_inputs_unchanged':True,'publication_profile_exit':0,'applied_paths':actual['actual_delta'],'provenance':ref(root,ev/'build-provenance.json'),'pointer':ref(root,ev/'active-baseline.json')})
    print('Delivered, evaluated, read back and published. Fresh validation remains.')

def environment():
    import importlib.metadata
    import shutil
    cli=shutil.which('codex')
    output,_=command(RUN,'cli-identification',[cli,'--version'],[]) if cli else (b'Unavailable',None)
    js(RUN/'environment.json',{'schema_version':'1','timestamp':now(),'os':platform.platform(),'python':sys.version,'pyyaml':importlib.metadata.version('PyYAML'),'host_shell':'PowerShell 7; exact PSVersion captured in shell-identification command','codex_cli':cli,'cli_identification':output.decode(errors='replace').strip(),'checker':str(CHECKER),'checker_sha256':sha(CHECKER.read_bytes()),'builder':str(BUILDER),'host_task_capability':'collaboration spawn_agent and followup_task used for independent history/fidelity and fresh validation','qualification':'CLI identity only; no native activation or Rust qualification','writable_scope':'Project development target exact two-file change plus fresh external evidence/disposable trials.'})
    command(RUN,'shell-identification',['C:/Program Files/PowerShell/7/pwsh.exe','-NoProfile','-Command','$PSVersionTable | ConvertTo-Json'],[])

if __name__=='__main__':
    {'adoption-prepare':adoption_prepare,'adoption-publish':adoption_publish,'contract':contract_prepare,'candidate':candidate_generate,'deliver':deliver,'publish':publish_revision,'environment':environment}[sys.argv[1]]()
