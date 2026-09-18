"""Fresh post-repair QA, independent retained oracles, installed coverage only."""
import ast
import json
import os
from pathlib import Path
import sys
from harness import RUN, ROOT, TARGET, LOADED, CHECKER, SPECS, read, write, save, ref, sha, inventory, execute

BUILD=ROOT/'docs/plan/skill-adaptive-implementations/skill-validator/20260913T211315150947Z'
CONFIRM=ROOT/'docs/plan/skill-validations/skill-validator/20260913T201813155594Z'

def prepare():
    candidate=json.loads(read(BUILD/'candidate-manifest.json'))
    current=inventory(TARGET)
    assert candidate['files']==current['files']
    save(RUN/'source-manifest.json',current)
    for r in current['files']: write(RUN/'source'/r['path'],read(TARGET/r['path']))
    for name,digest in SPECS.items():
        original=ROOT/'docs/plan'/name
        assert sha(read(original))==digest
        write(RUN/'inputs'/name,read(original))
    write(RUN/'inputs/revision-spec.md',read(CONFIRM/'revision-spec.md'))
    save(RUN/'inputs/loaded-evaluator-before.json',inventory(LOADED))
    save(RUN/'inputs/companion-before.json',inventory(ROOT/'src/agents/skills/skill-builder'))
    save(RUN/'inputs/harness-reuse.json',{'base':str(CONFIRM),'copied_files':['harness.py','probes.py','subset_control.py','audit_fixtures.py'],'old_fixed_run':'RUN is derived from __file__; copies bind the new QA root. No original scripts are executed in place. Historical harness.setup() is not invoked; this prepare routine pins the delivered 76-file snapshot.','expectations':'Unchanged selected case expectations; original R/P fixtures remain read-only at their original paths. H11 is freshly constructed and preplanned.'})
    declarations=[]
    for r in current['files']:
        if r['path'].startswith('scripts/') and r['path'].endswith('.py'):
            ast.parse(read(TARGET/r['path']),filename=r['path'])
            declarations.append(r['path'])
    save(RUN/'coverage/denominator-before-run.json',{'source':str(TARGET/'scripts'),'files':declarations,'exclusions':[],'baseline':'All first-party executable Python support scripts; executed-line baseline and branches separately. No coverage aliasing of temporary copies to original paths. Native Windows only; not Rust coverage.','collector':'Already installed coverage.py 7.9.0; startup hook under synthetic QA root only.','thresholds':{'line':95,'required_case_pass_rate':95}})
    config='[run]\nbranch = True\nparallel = True\ndata_file = '+str(RUN/'coverage/.coverage')+'\nsource = '+str(TARGET/'scripts')+'\n[report]\nshow_missing = True\n'
    write(RUN/'coverage/coverage.ini',config)
    write(RUN/'coverage/startup/sitecustomize.py','import coverage\ncoverage.process_startup()\n')
    print('Pinned',current['package_digest'],'and',len(declarations),'source scripts before QA.')

def collect():
    os.environ['COVERAGE_PROCESS_START']=str(RUN/'coverage/coverage.ini')
    startup=str(RUN/'coverage/startup')
    os.environ['PYTHONPATH']=startup+(os.pathsep+os.environ['PYTHONPATH'] if os.environ.get('PYTHONPATH') else '')

def probes():
    collect()
    import probes as suite
    suite.prepare()
    suite.run()
    execute('SUBSET-WRAPPER',[sys.executable,'-B','-X','utf8',str(RUN/'subset_control.py')])
    execute('FIXTURE-AUDIT',[sys.executable,'-B','-X','utf8',str(RUN/'audit_fixtures.py')])

def regression():
    collect()
    execute('FULL-REGRESSION',[sys.executable,'-B','-X','utf8','-m','unittest','discover','-s','src/agents/skills/skill-validator/tests','-v'])

def support():
    collect()
    execute('STRUCTURAL',[sys.executable,'-B','-X','utf8',str(CHECKER),str(RUN/'source')])
    execute('BOUND-EVALUATOR',[sys.executable,'-B','-X','utf8',str(TARGET/'scripts/run_evaluation.py'),'--package-root',str(TARGET),'--candidate-root',str(RUN/'source'),'--cases',str(RUN/'source/evals/cases.jsonl'),'--output',str(RUN/'bound-evaluation.jsonl'),'--run-id',RUN.name,'--profile','legacy-import-v1'])
    execute('READBACK',[sys.executable,'-B','-X','utf8',str(LOADED/'scripts/observe.py'),'readback','--source',str(TARGET),'--manifest',str(RUN/'source-manifest.json')])

def coverage():
    config=str(RUN/'coverage/coverage.ini')
    for cid,args in [('COVERAGE-COMBINE',['combine','--rcfile',config,'--keep']),('COVERAGE-JSON',['json','--rcfile',config,'-o',str(RUN/'coverage/coverage.json')]),('COVERAGE-REPORT',['report','--rcfile',config])]:
        execute(cid,[sys.executable,'-B','-X','utf8','-m','coverage',*args])
    totals=json.loads(read(RUN/'coverage/coverage.json'))['totals']
    print(json.dumps(totals))

if __name__=='__main__': globals()[sys.argv[1]]()
