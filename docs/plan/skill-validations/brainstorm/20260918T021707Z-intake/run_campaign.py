"""Launch predeclared independent disposable sessions; preserve each receipt."""
from prepare import *
from concurrent.futures import ThreadPoolExecutor, as_completed

def execute(ident):
    root=RUN/'trials'/ident
    for mode,args in [('seal',['--plan',str(root/'plan.json'),'--attempt',str(root/'attempt-001')]),('run',['--attempt',str(root/'attempt-001')]),('check',['--attempt',str(root/'attempt-001')])]:
        argv=[sys.executable,'-B','-X','utf8',str(VAL/'scripts/trial_runner.py'),mode,*args]
        start=dt.datetime.now(dt.timezone.utc).isoformat()
        result=subprocess.run(argv,cwd=ROOT,capture_output=True,timeout=650)
        save(root/(mode+'.stdout.txt'),result.stdout)
        save(root/(mode+'.stderr.txt'),result.stderr)
        save(root/(mode+'.command.json'),dict(argv=argv,cwd=str(ROOT),started_at=start,ended_at=dt.datetime.now(dt.timezone.utc).isoformat(),exit_code=result.returncode,timeout_seconds=650))
        if mode=='seal' and result.returncode:
            return ident,'SEAL_ERROR'
    receipt=json.loads((root/'attempt-001/result.json').read_bytes())
    return ident,{key:receipt[key] for key in ('exit_code','timeout','cleanup','input_unchanged','elapsed_seconds')}

if __name__=='__main__':
    identifiers=json.loads((RUN/'inputs/campaign-trial-list.json').read_bytes())
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures=[pool.submit(execute,ident) for ident in identifiers]
        for future in as_completed(futures):
            print(json.dumps(future.result()),flush=True)
