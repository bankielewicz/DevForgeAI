"""Frozen SPEC-002 v2 / SPEC-003 v4 trials using the installed native Codex host.

No installation or saved configuration changes. All attempts remain in evidence.
Definitions, native protocol, inputs and outputs are separated from runtime skills.
"""
from __future__ import annotations
import argparse, concurrent.futures, hashlib, json, shutil, subprocess, tempfile, time, threading
from pathlib import Path
import yaml
from native_documents_updater_eval import EXE, Server, git_state, inventory, save

PACKAGE=Path(__file__).resolve().parents[1]
REPO=PACKAGE.parents[2]
EXPECTED={'prd':29,'architecture':16}
MANUAL=['PRD-VER-11-partial-tool','PRD-VER-11-partial-text','PRD-VER-11-stop-save-yes',
        'PRD-VER-11-stop-save-no','PRD-VER-12-approved-extension','PRD-VER-12-all-processed',
        'PRD-VER-12-shared-constraint','PRD-VER-12-unknown-brn','PRD-VER-12-malformed-brn',
        'PRD-VER-12-failed-extension','PRD-VER-12-size','PRD-VER-23-local-budget',
        'PRD-VER-23-invalid-local','PRD-VER-23-SV-01','PRD-VER-23-SV-02','PRD-VER-23-SV-06',
        'PRD-VER-23-calendar','PRD-VER-23-validator-unavailable','PRD-BEH-10-identity-disclosure',
        'ARCH-VER-12-f-shared-files','ARCH-VER-12-i-accepted-decision-failure',
        'ARCH-VER-19-failed-supersession']

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def manifest_digest(value):
    return hashlib.sha256(''.join(f'{p}\0{h}\n' for p,h in sorted(value.items())).encode()).hexdigest()
def runtime_inventory(root):
    return {p:h for p,h in inventory(root).items() if p.startswith(('.codex-plugin/','skills/'))}
def body(path):
    match=__import__('re').match(r'\A---\s*\n(.*?)\n---\s*\n(.*)\Z',path.read_text(),__import__('re').S)
    if not match: raise ValueError(f'Missing frontmatter: {path}')
    return yaml.safe_load(match[1]),match[2].strip()

class ContractServer(Server):
    def setup(self,cwd,arm,candidate=None):
        self.rpc('skills/extraRoots/set',{'extraRoots':[str(candidate/'skills')] if candidate else []})
        catalog=self.rpc('skills/list',{'cwds':[str(cwd)],'forceReload':True})
        save(self.e/'skills-list.json',catalog)
        entries=[s for group in catalog.get('data',[]) for s in group.get('skills',[])]
        selected=[s for s in entries if candidate and Path(s.get('path','')).is_relative_to(candidate/'skills')]
        if arm=='plugin' and {s['name'].split(':')[-1] for s in selected}!={'prd','architecture','brainstorm','documents-updater'}:
            raise RuntimeError('Exact four-skill runtime missing from native catalog')
        if arm=='baseline' and selected: raise RuntimeError('Candidate in baseline')
        disabled=[{'path':s['path'],'enabled':False} for s in entries if s not in selected]
        started=self.rpc('thread/start',{'cwd':str(cwd),'ephemeral':True,'sandbox':'workspace-write',
            'approvalPolicy':'never','config':{'skills.config':disabled,'features.memories':False}})
        save(self.e/'thread-start.json',started)
        self.thread=started['thread']['id']; self.model=started.get('model'); self.started=started
        save(self.e/'catalog-selection.json',{'selected':[s['path'] for s in selected],'disabled':disabled})

def freeze(evidence):
    if evidence.exists(): raise RuntimeError('Evidence path exists; preserve it')
    dirty=subprocess.check_output(['git','status','--porcelain'],cwd=REPO,text=True)
    if dirty: raise RuntimeError('Freeze requires a committed clean source tree')
    evidence.mkdir(parents=True)
    candidate=evidence/'candidate'
    shutil.copytree(PACKAGE/'.codex-plugin',candidate/'.codex-plugin')
    shutil.copytree(PACKAGE/'skills',candidate/'skills')
    tasks=[]
    for skill,count in EXPECTED.items():
        suite=PACKAGE/'evals'/skill
        cases=sorted(p.name for p in suite.iterdir() if p.is_dir() and (p/'prompt.md').is_file())
        assert len(cases)==count,(skill,cases)
        shutil.copytree(suite,evidence/'definitions'/skill)
        for repeat in range(1,4):
            for case in cases:
                meta,_=body(suite/case/'prompt.md')
                ver=next(t.upper() for t in meta['tags'] if t.startswith('ver-'))
                for arm in ['plugin','baseline']:
                    tasks.append({'skill':skill,'case':case,'verification':ver,'arm':arm,'repeat':repeat,
                                  'mode':'plan' if skill=='architecture' and case=='existing-arch-not-duplicated' else 'default',
                                  'status':'NOT_RUN'})
    for name in ['native_contract_eval.py','native_documents_updater_eval.py','grade_contract_eval.py']:
        shutil.copyfile(PACKAGE/'tests'/name,evidence/name)
    runtime=runtime_inventory(candidate)
    plan={'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),
        'baseline':'f69fee275860bcd68c6be632478552fa34d6f00b','candidate_files':runtime,'candidate_sha256':manifest_digest(runtime),
        'definitions':inventory(evidence/'definitions'),'codex_executable':EXE,
        'resolved_executable':str(Path(EXE).resolve()),'executable_sha256':sha(Path(EXE).resolve()),
        'codex_version':subprocess.check_output([EXE,'--version'],text=True).strip(),
        'harness_files':{name:sha(evidence/name) for name in ['native_contract_eval.py','native_documents_updater_eval.py','grade_contract_eval.py']},
        'threshold':0.8,'repetitions':3,'trial_count':270,'trials':tasks,'manual':[{'id':s,'status':'NOT_RUN'} for s in MANUAL],
        'isolation':'Unique temporary parent per trial; all four runtime skills in plugin arm; no candidate in baseline. Other skills, saved plugins, MCP servers and memories disabled in child processes. Workspace-write and approvalPolicy never; not an OS-hermetic read boundary. Raw evidence/graders outside consuming project.',
        'identity':'No production identity injection; compare host metadata only in evaluator. Unavailable remains an open qualification obligation.',
        'score_contract':'Original graders and thresholds; binary conformance per repetition needs 3/3. Partial source-check score is shown separately. Missing evidence and mandatory failures cannot be averaged away.',
        'documentation':'https://learn.chatgpt.com/docs/app-server'}
    save(evidence/'plan.json',plan)
    print(json.dumps({'frozen':str(evidence),'candidate_sha256':plan['candidate_sha256'],'trials':len(tasks)}),flush=True)

def verify(evidence):
    plan=json.loads((evidence/'plan.json').read_text())
    assert runtime_inventory(PACKAGE)==plan['candidate_files'],'Runtime source drift'
    assert inventory(evidence/'candidate')==plan['candidate_files'],'Frozen candidate drift'
    assert inventory(evidence/'definitions')==plan['definitions'],'Frozen definitions drift'
    assert sha(Path(EXE).resolve())==plan['executable_sha256'],'Executable drift'
    for name,h in plan['harness_files'].items(): assert sha(PACKAGE/'tests'/name)==h,(name,'harness drift')
    return plan

def preflight(evidence):
    verify(evidence)
    out=evidence/'preflight';out.mkdir(exist_ok=False)
    for arm in ['plugin','baseline']:
        parent=Path(tempfile.mkdtemp(prefix='dfai-contract-preflight-'));cwd=parent/'project';cwd.mkdir()
        local=parent/'devforgeai'
        if arm=='plugin': shutil.copytree(evidence/'candidate',local)
        server=None
        try:
            server=ContractServer(out/arm,cwd);server.setup(cwd,arm,local if arm=='plugin' else None)
            save(out/arm/'result.json',{'status':'CATALOG_PASS','model':server.model,'thread':server.thread})
        except Exception as exc:
            save(out/arm/'result.json',{'status':'HARNESS_FAILURE','error':repr(exc)})
            raise
        finally:
            if server: server.close()
    print('Both arm catalog preflights passed; no model turn launched.',flush=True)

def trial(task,evidence,plan_hash,stop):
    identity=f"{task['skill']}--{task['case']}--{task['arm']}--{task['repeat']}"
    out=evidence/'matrix'/identity
    if stop.is_set(): return
    out.mkdir(parents=True,exist_ok=False)
    parent=Path(tempfile.mkdtemp(prefix='dfai-contract-eval-'));cwd=parent/'project';cwd.mkdir()
    local=parent/'devforgeai'
    if task['arm']=='plugin': shutil.copytree(evidence/'candidate',local)
    case=evidence/'definitions'/task['skill']/task['case']
    meta,prompt=body(case/'prompt.md');(out/'prompt.md').write_text(prompt+'\n')
    r=(subprocess.run(['bash',str(case/'scaffold.sh')],cwd=cwd,text=True,capture_output=True)
       if (case/'scaffold.sh').is_file() else subprocess.CompletedProcess([],0,'No scaffold declared by this case.',''))
    save(out/'scaffold.json',{'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
    save(out/'before.json',inventory(cwd));save(out/'git-before.json',git_state(cwd))
    shutil.copytree(cwd,out/'before-workspace',ignore=shutil.ignore_patterns('.git'))
    start=time.monotonic();server=None
    try:
        r.check_returncode();server=ContractServer(out,cwd)
        server.setup(cwd,task['arm'],local if task['arm']=='plugin' else None)
        if task['mode']=='plan': server.mode='plan'
        result=server.turn(prompt,timeout=int(meta.get('timeout_seconds',1200)))
        result.update(threadId=server.thread,model=server.model)
    except Exception as exc: result={'status':'harness_error','error':repr(exc)}
    finally:
        if server: server.close()
    result.update({k:v for k,v in task.items() if k!='status'},elapsed_seconds=round(time.monotonic()-start,3),
                  plan_sha256=plan_hash,scratch_parent=str(parent),scratch_workspace=str(cwd))
    save(out/'result.json',result);save(out/'after.json',inventory(cwd));save(out/'git-after.json',git_state(cwd))
    shutil.copytree(cwd,out/'workspace',ignore=shutil.ignore_patterns('.git'))
    if task['arm']=='plugin':save(out/'runtime-candidate-check.json',{'unchanged':inventory(local)==inventory(evidence/'candidate')})
    if any(s in json.dumps(result).lower() for s in ['usage limit','quota exceeded','insufficient_quota','usage_limit_reached']):
        stop.set();save(evidence/'platform-stop.json',{'trial':identity,'result':result,'remaining':'NOT_RUN; platform limit, no automatic retries'})
    print(json.dumps({'trial':identity,'status':result['status'],'elapsed':result['elapsed_seconds']}),flush=True)

def matrix(evidence,jobs):
    plan=verify(evidence)
    assert all(json.loads((evidence/'preflight'/arm/'result.json').read_text())['status']=='CATALOG_PASS' for arm in ['plugin','baseline'])
    assert not (evidence/'matrix').exists(),'No retries in a frozen campaign'
    stop=threading.Event();plan_hash=sha(evidence/'plan.json')
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
        futures=[pool.submit(trial,task,evidence,plan_hash,stop) for task in plan['trials']]
        for future in concurrent.futures.as_completed(futures):future.result()
    save(evidence/'matrix-complete.json',{'candidate_unchanged':runtime_inventory(PACKAGE)==plan['candidate_files'],
         'attempted':len(list((evidence/'matrix').glob('*/result.json'))),'planned':len(plan['trials']),
         'platform_stop':stop.is_set()})

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('action',choices=['freeze','preflight','matrix'])
    parser.add_argument('--evidence',required=True,type=Path);parser.add_argument('--jobs',type=int,default=4)
    args=parser.parse_args();evidence=args.evidence.resolve()
    if args.action=='matrix':matrix(evidence,args.jobs)
    else:globals()[args.action](evidence)
