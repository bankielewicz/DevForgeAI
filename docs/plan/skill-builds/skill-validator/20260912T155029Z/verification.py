import datetime, json, os, shutil, subprocess, sys
from pathlib import Path
from bootstrap import ROOT, PROJECT, inventory, digest, write

BUILDER=PROJECT/'.agents/skills/skill-builder'
CHECKER=Path('C:/Users/bryan/.codex/skills/.system/skill-creator/scripts/quick_validate.py')
def reference(p,base=ROOT): return {'path':p.relative_to(base).as_posix(),'sha256':digest(p.read_bytes())}
def copy_package(source,dest):
    manifest=inventory(source); assert not manifest['excluded_boundaries'], manifest['excluded_boundaries']
    dest.mkdir(parents=True,exist_ok=False)
    for r in manifest['files']:
        p=dest/r['path']; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes((source/r['path']).read_bytes())
    assert inventory(dest)['files']==manifest['files']
    return manifest
def execute(label,args,cwd=PROJECT,timeout=120,env=None):
    folder=ROOT/'commands'/label; folder.mkdir(parents=True,exist_ok=False)
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write(folder/'planned.json',{'argv':[str(a) for a in args],'cwd':str(cwd),'timeout_seconds':timeout,'start_utc':start})
    try:
        p=subprocess.run([str(a) for a in args],cwd=cwd,capture_output=True,text=True,encoding='utf-8',timeout=timeout,env=env)
        out,err,code=p.stdout,p.stderr,p.returncode; state='exited'
    except subprocess.TimeoutExpired as exc:
        out=exc.stdout or b''; err=exc.stderr or b''
        out=out.decode('utf-8',errors='replace') if isinstance(out,bytes) else out
        err=err.decode('utf-8',errors='replace') if isinstance(err,bytes) else err
        code=None; state='timeout'
    (folder/'stdout.txt').write_text(out,encoding='utf-8'); (folder/'stderr.txt').write_text(err,encoding='utf-8')
    receipt={'argv':[str(a) for a in args],'cwd':str(cwd),'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':code,'state':state,'stdout':reference(folder/'stdout.txt'),'stderr':reference(folder/'stderr.txt')}
    write(folder/'result.json',receipt)
    with (ROOT/'command-log.md').open('a',encoding='utf-8') as f:
        f.write('\n## '+label+'\n\nExact argv/cwd/timestamps/streams: ['+label+'](commands/'+label+'/result.json). Exit '+str(code)+'; '+state+'.\n')
    print(json.dumps({'command':label,'exit':code,'stdout_tail':out[-700:],'stderr_tail':err[-500:]}))
    return code,folder

def evaluate(label,source,completed=False):
    # Every invocation receives its own bounded immutable input tree and case file.
    folder=ROOT/'evaluations'/label; folder.mkdir(parents=True,exist_ok=False)
    snap=folder/'snapshot'; snap.mkdir()
    measured=copy_package(source,snap/'destination')
    baseline_name='generated-baseline' if completed else 'baseline'
    copy_package(source,snap/baseline_name)
    (snap/'inputs').mkdir(); (snap/'evidence').mkdir()
    for name in ['skill-validator-spec.md','authorization.txt']:
        (snap/'inputs'/name).write_bytes((ROOT/'inputs'/name).read_bytes())
    contract=(ROOT/'build-contract.json').read_bytes(); (snap/'evidence/build-contract.json').write_bytes(contract)
    outputs=[{'path':r['path'],'sha256':r['sha256']} for r in measured['files']]
    checker_code,checker_folder=execute(label+'-structural',[sys.executable,'-B','-X','utf8',CHECKER,snap/'destination'])
    # Named structural result is preceding evidence. Byte inventory/readback supplements its limited semantics.
    observed={'schema_version':'1','run_id':'20260912T155029Z','target_name':'skill-validator','outputs':outputs,'structural_command':json.loads((checker_folder/'result.json').read_text(encoding='utf-8')),'source_manifest':measured,'source_readback_equal':inventory(source)['files']==measured['files'],'interpretation':'Structural observation and measured-byte accounting only; external case execution map reports semantic/task evidence.'}
    write(snap/'evidence/preceding-observations.json',observed)
    c=json.loads(contract)
    provenance={'schema_version':'1','run_id':'20260912T155029Z','mode':'spec_build','target_name':'skill-validator','builder_manifest_sha256':digest((BUILDER/'evals/build-manifest.json').read_bytes()),'contract_sha256':digest(contract),'inputs':[{'id':i['id'],'sha256':i['sha256']} for i in c['inputs']],'dependencies':c['dependencies'],'outputs':[{'path':r['path'],'sha256':r['sha256'],'ownership':'generated','baseline_path':baseline_name+'/'+r['path'],'baseline_sha256':r['sha256']} for r in measured['files']],'mappings':[{'requirement_id':r['id'],'artifact_paths':r['artifact_paths'],'evidence_ids':['preceding-observations']} for r in c['requirements']],'evidence':[{'id':'preceding-observations','path':'evidence/preceding-observations.json','sha256':digest((snap/'evidence/preceding-observations.json').read_bytes())}],'prior_build':None,'result':'COMPLETE' if completed else 'INCOMPLETE'}
    if completed:
        (snap/'evidence/build-verification-observations.json').write_bytes((ROOT/'build-verification-observations.json').read_bytes())
        provenance['evidence'].append({'id':'build-verification','path':'evidence/build-verification-observations.json','sha256':digest((snap/'evidence/build-verification-observations.json').read_bytes())})
        for row in provenance['mappings']: row['evidence_ids'].append('build-verification')
    write(snap/'evidence/build-provenance.json',provenance)
    cases=[{'case_id':'validator-links','grader_id':'package_links','params':{'path':'destination'},'expected':'PASS'},{'case_id':'validator-traceability','grader_id':'build_traceability','params':{'evidence':'evidence','destination':'destination'},'expected':'PASS'}]
    casefile=folder/'cases.jsonl'; casefile.write_text(''.join(json.dumps(x)+'\n' for x in cases),encoding='utf-8')
    before=inventory(snap); write(folder/'input-before-manifest.json',before)
    write(folder/'case-before.json',reference(casefile))
    code,receipt=execute(label+'-spec-v1',[sys.executable,'-B','-X','utf8',BUILDER/'scripts/run_evaluation.py','--package-root',BUILDER,'--candidate-root',snap,'--cases',casefile,'--output',folder/'results.jsonl','--run-id','20260912T155029Z-'+label,'--profile','spec-v1'])
    after=inventory(snap); write(folder/'input-after-manifest.json',after)
    equal=before['files']==after['files']; assert equal
    write(folder/'readback.json',{'input_unchanged':equal,'case_unchanged':reference(casefile)==json.loads((folder/'case-before.json').read_text()),'source_unchanged':inventory(source)['files']==measured['files'],'structural_exit':checker_code,'evaluator_exit':code})
    return code,folder

if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='evaluate': evaluate(sys.argv[2],Path(sys.argv[3]))
    elif mode=='checker': execute(sys.argv[2],[sys.executable,'-B','-X','utf8',CHECKER,Path(sys.argv[3])])
