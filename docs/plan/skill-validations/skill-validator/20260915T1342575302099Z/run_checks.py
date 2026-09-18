import datetime,json,os,pathlib,subprocess,sys,time
R=pathlib.Path(__file__).resolve().parent
ROOT=pathlib.Path('C:/Projects/DevForgeAI')
PY=sys.executable
OPS=ROOT/'.agents/skills/skill-validator/scripts'
def command(name,args,timeout=120,env=None):
    d=R/'commands'/name;d.mkdir(parents=True,exist_ok=False)
    plan={'argv':args,'cwd':str(ROOT),'timeout_seconds':timeout,'start_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    (d/'plan.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
    start=time.monotonic()
    with (d/'stdout.txt').open('wb') as out,(d/'stderr.txt').open('wb') as err:
        try:
            p=subprocess.run(args,cwd=ROOT,env=env,stdout=out,stderr=err,stdin=subprocess.DEVNULL,timeout=timeout)
            state={'exit_code':p.returncode,'timed_out':False}
        except subprocess.TimeoutExpired:state={'exit_code':None,'timed_out':True}
    state.update(elapsed_seconds=time.monotonic()-start,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    (d/'result.json').write_text(json.dumps(state,indent=2),encoding='utf-8')
    print(name,json.dumps(state),flush=True)
    return state
if __name__=='__main__':
    command('creator',[PY,'-B','-X','utf8','C:/Users/bryan/.codex/skills/.system/skill-creator/scripts/quick_validate.py',str(R/'source')])
    command('structure',[PY,'-B','-X','utf8',str(OPS/'observe.py'),'structure','--source',str(R/'source')])
    command('package',[PY,'-B','-X','utf8',str(OPS/'adaptive_observe.py'),'package','--source',str(R/'source')])
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(R/'instrumentation'),COVERAGE_PROCESS_START=str(R/'coverage.ini'),TEMP=str(R/'temp'),TMP=str(R/'temp'))
    command('regression',[PY,'-B','-X','utf8','-m','unittest','discover','-s',str(R/'source/tests'),'-v'],600,env)
    command('coverage-combine',[PY,'-B','-X','utf8','-m','coverage','combine','--keep',str(R/'coverage')],env=dict(os.environ,COVERAGE_FILE=str(R/'coverage/.coverage')))
    command('coverage-json',[PY,'-B','-X','utf8','-m','coverage','json','--rcfile',str(R/'coverage.ini'),'-o',str(R/'coverage/coverage.json')])

