"""Operator-driven native checks; fixture answers never expose evaluator identity.

The root evaluator supplies observed answers through an external inbox. This is
agent-operated native evidence, not the owner's personal review or installation.
"""
from __future__ import annotations
import argparse, datetime, hashlib, json, os, shutil, subprocess, tempfile, time
from pathlib import Path
from native_contract_eval import ContractServer, PACKAGE, REPO, inventory, save, sha, verify
from native_documents_updater_eval import git_state

M1 = "$devforgeai:prd BRN-001 — It's our MVP, piloted with our own coordinator and volunteers on real volunteer data, so the operating context is internal."
SPECS = [
    ('partial-text','prd/writes-prd-from-brn',M1,'default',['PRD-VER-11-partial-text','PRD-BEH-10-identity-disclosure']),
    ('partial-tool','prd/writes-prd-from-brn',M1,'plan',['PRD-VER-11-partial-tool']),
    ('stop-save-yes','prd/writes-prd-from-brn',M1,'default',['PRD-VER-11-stop-save-yes']),
    ('stop-save-no','prd/writes-prd-from-brn',M1,'default',['PRD-VER-11-stop-save-no']),
    ('approved-extension','prd/extension-keeps-review-history','$devforgeai:prd BRN-002','default',['PRD-VER-12-approved-extension','PRD-VER-12-all-processed']),
    ('shared-constraint','prd/extension-keeps-review-history','$devforgeai:prd BRN-002 — write a new PRD for it. It runs on the same hosted services as PRD-001.','default',['PRD-VER-12-shared-constraint']),
    ('unknown-brn','prd/extension-keeps-review-history','$devforgeai:prd BRN-009','default',['PRD-VER-12-unknown-brn']),
    ('malformed-brn','prd/extension-keeps-review-history','$devforgeai:prd BRN-002','default',['PRD-VER-12-malformed-brn']),
    ('failed-extension','prd/failed-extension-stays-in-review','$devforgeai:prd BRN-002','default',['PRD-VER-12-failed-extension']),
    ('local-budget','prd/writes-prd-from-brn',M1,'default',['PRD-VER-23-local-budget']),
    ('invalid-local','prd/writes-prd-from-brn',M1,'default',['PRD-VER-23-invalid-local']),
    ('policy-sv01','prd/writes-prd-from-brn','$devforgeai:prd BRN-001. Proceed without questions.','default',['PRD-VER-23-SV-01']),
    ('policy-sv02','prd/writes-prd-from-brn','$devforgeai:prd BRN-001. Proceed without questions.','default',['PRD-VER-23-SV-02']),
    ('policy-sv06','prd/writes-prd-from-brn','$devforgeai:prd BRN-001. Proceed without questions.','default',['PRD-VER-23-SV-06']),
    ('policy-calendar','prd/writes-prd-from-brn','$devforgeai:prd BRN-001. Proceed without questions.','default',['PRD-VER-23-calendar']),
    ('policy-unavailable','prd/writes-prd-from-brn','$devforgeai:prd BRN-001. Proceed without questions.','default',['PRD-VER-23-validator-unavailable']),
    ('accepted-decision-failure','architecture/failed-amendment-stays-in-review','$devforgeai:architecture PRD-001 — amend ARCH-001; I confirm the amend outcome.','default',['ARCH-VER-12-i-accepted-decision-failure']),
    ('failed-supersession','manual/failed-supersession',"$devforgeai:architecture PRD-001 — amend ARCH-001; I confirm the amend outcome. We're dropping Auth0 for sign-in.",'default',['ARCH-VER-19-failed-supersession']),
]

def freeze(e):
    main=verify(e);m=e/'manual';m.mkdir(exist_ok=False)
    shutil.copyfile(Path(__file__),m/'native_contract_manual.py')
    entries=[]
    policy=REPO/'src/staging/examples/policy-two-orgs'
    for name,fixture,prompt,mode,ids in SPECS:
        base=m/'definitions'/name;base.mkdir(parents=True)
        scaffold=(PACKAGE/'tests/manual/architecture/failed-supersession/scaffold.sh' if fixture.startswith('manual/') else e/'definitions'/fixture/'scaffold.sh')
        shutil.copyfile(scaffold,base/'scaffold.sh')
        seed=base/'workspace';seed.mkdir()
        p=subprocess.run(['bash',str(base/'scaffold.sh')],cwd=seed,text=True,capture_output=True)
        save(base/'scaffold-result.json',{'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr});p.check_returncode()
        if name=='malformed-brn':
            b=seed/'docs/specs/brainstorm/BRN-002.md';s=b.read_text();assert '    disposition: promoted' in s
            b.write_text(s.replace('    disposition: promoted','  disposition promoted'))
        if name in {'local-budget','invalid-local'}:
            b=seed/'.codex/devforgeai.local.md';b.parent.mkdir()
            b.write_text('---\ndevforgeai_local: 1\ninterview.max_calls: '+('5' if name=='local-budget' else '50\narchitecture.mandated_platforms: x')+'\n---\n')
        if name.startswith('policy-'):
            pd=seed/'docs/specs/policy';pd.mkdir(parents=True)
            a=(policy/'org-a/POL-001.md').read_text();b=(policy/'org-b/POL-001.md').read_text()
            if name=='policy-sv01':a=a.replace('id: SET-02','id: SET-01')
            if name=='policy-sv02':(pd/'POL-002.md').write_text(b.replace('POL-001','POL-002'))
            if name=='policy-sv06':a=b.replace('status: approved','status: draft')
            if name=='policy-calendar':
                assert 'updated: 2026-09-01' in a;a=a.replace('updated: 2026-09-01','updated: 2026-13-45')
            if name=='policy-unavailable':a=b
            (pd/'POL-001.md').write_text(a)
        entries.append({'name':name,'fixture':fixture,'source_scaffold_sha256':sha(scaffold),'initial_prompt':prompt,'initial_mode':mode,'obligations':ids,'workspace_files':inventory(seed),'status':'NOT_RUN'})
    plan={'candidate_sha256':main['candidate_sha256'],'source_commit':main['source_commit'],'native_plan_sha256':sha(e/'plan.json'),
          'driver_sha256':sha(m/'native_contract_manual.py'),'definitions':inventory(m/'definitions'),'scenarios':entries,
          'operator':'Root Codex evaluator inspects actual native responses and supplies fixture-user answers; owner acceptance remains pending.',
          'tool_branch':'Native request_user_input requires Plan mode. Preserve Plan interview evidence, then explicitly switch to Default for writing. Do not count planning alone as a completed write.',
          'identity':'Do not inject model or session identity. Compare only after the attempt.',
          'remaining_static':['PRD-VER-12-size','ARCH-VER-12-f-shared-files']}
    save(m/'plan.json',plan);print(json.dumps({'scenarios':len(entries),'plan':str(m/'plan.json')}))

def status(out,phase,**extra):
    v={'phase':phase,'time':datetime.datetime.now(datetime.timezone.utc).isoformat(),**extra}
    save(out/'status.json',v);print(json.dumps(v),flush=True)

def wait_json(path,timeout=3600):
    deadline=time.monotonic()+timeout
    while time.monotonic()<deadline:
        if path.is_file():return json.loads(path.read_text())
        time.sleep(.5)
    raise TimeoutError('No operator response at '+str(path))

def start(e,name,single):
    main=verify(e);m=e/'manual';plan=json.loads((m/'plan.json').read_text())
    assert plan['native_plan_sha256']==sha(e/'plan.json')
    assert plan['definitions']==inventory(m/'definitions')
    assert plan['driver_sha256']==sha(Path(__file__))
    spec=next(s for s in plan['scenarios'] if s['name']==name)
    out=m/'attempts'/name;out.mkdir(parents=True,exist_ok=False)
    parent=Path(tempfile.mkdtemp(prefix='dfai-contract-manual-'));cwd=parent/'project'
    shutil.copytree(m/'definitions'/name/'workspace',cwd)
    local=parent/'devforgeai';shutil.copytree(e/'candidate',local)
    if name in {'approved-extension','accepted-decision-failure','failed-supersession'}:
        for args in [['git','init','-q'],['git','add','-A'],['git','-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','fixture baseline']]:
            subprocess.run(args,cwd=cwd,check=True,capture_output=True)
    if name=='policy-unavailable':
        shim=parent/'shim';shim.mkdir();(shim/'jsonschema.py').write_text('raise ImportError("hidden by manual fixture", name="jsonschema")\n')
        os.environ['PYTHONPATH']=str(shim)
        save(out/'process-environment.json',{'PYTHONPATH':str(shim),'shim_sha256':sha(shim/'jsonschema.py'),'scope':'native child process only; no installed libraries changed'})
    save(out/'before.json',inventory(cwd));save(out/'git-before.json',git_state(cwd));shutil.copytree(cwd,out/'before-workspace',ignore=shutil.ignore_patterns('.git'))
    save(out/'binding.json',{'candidate_sha256':main['candidate_sha256'],'manual_plan_sha256':sha(m/'plan.json'),'scenario':spec,'scratch_parent':str(parent),'scratch_workspace':str(cwd)})
    server=None;turn=0;outcomes=[]
    try:
        server=ContractServer(out,cwd);server.setup(cwd,'plugin',local)
        cmd={'prompt':spec['initial_prompt'],'mode':spec['initial_mode']}
        while True:
            turn+=1;t=out/'turns'/f'{turn:02}';t.mkdir(parents=True)
            save(t/'input.json',cmd);server.mode=cmd.get('mode','default');qnum=0;eventstart=len(server.events)
            def answer(params):
                nonlocal qnum
                qnum+=1;save(t/f'question-{qnum:02}.json',params)
                status(out,'awaiting_tool_answer',turn=turn,question=qnum,questions=params.get('questions',[]))
                return wait_json(out/'inbox'/f'answer-{turn:02}-{qnum:02}.json')['answers']
            status(out,'running',turn=turn,mode=server.mode)
            outcome=server.turn(cmd['prompt'],timeout=1800,question_answer=None if single else answer)
            save(t/'result.json',outcome);save(t/'after.json',inventory(cwd));save(t/'git-after.json',git_state(cwd))
            shutil.copytree(cwd,t/'workspace',ignore=shutil.ignore_patterns('.git'))
            items=[x['params']['item'] for x in server.events[eventstart:] if x.get('method')=='item/completed']
            finals=[x.get('text','') for x in items if x.get('type')=='agentMessage' and x.get('phase')!='commentary']
            (t/'final-reply.txt').write_text('\n\n'.join(finals)+'\n');outcomes.append({'turn':turn,'status':outcome.get('status')})
            status(out,'awaiting_operator',turn=turn,native_status=outcome.get('status'),reply='\n\n'.join(finals))
            if single:break
            cmd=wait_json(out/'inbox'/f'next-{turn:02}.json')
            if cmd.get('action')=='finish':break
    except Exception as exc:
        save(out/'error.json',{'error':repr(exc)});status(out,'harness_error',error=repr(exc))
    finally:
        if server:server.close()
        save(out/'after.json',inventory(cwd));save(out/'git-after.json',git_state(cwd))
        shutil.copytree(cwd,out/'workspace',ignore=shutil.ignore_patterns('.git'))
        save(out/'result.json',{'turns':outcomes,'threadId':getattr(server,'thread',None),'model':getattr(server,'model',None),'runtime_candidate_unchanged':inventory(local)==inventory(e/'candidate'),'manual_plan_sha256':sha(m/'plan.json'),'error':(out/'error.json').exists()})
        status(out,'sealed',turns=outcomes)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['freeze','start']);p.add_argument('--evidence',required=True,type=Path);p.add_argument('--scenario');p.add_argument('--single',action='store_true');a=p.parse_args()
    if a.action=='freeze':freeze(a.evidence.resolve())
    else:start(a.evidence.resolve(),a.scenario,a.single)

if __name__=='__main__':main()
