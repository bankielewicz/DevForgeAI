import json,os,pathlib,sys
from run_checks import command
R=pathlib.Path(__file__).resolve().parent
ROOT=pathlib.Path('C:/Projects/DevForgeAI')
dependency=R/'inputs/builder-dependency'
command('dependency-snapshot',[sys.executable,'-B','-X','utf8',str(ROOT/'.agents/skills/skill-validator/scripts/observe.py'),'snapshot','--source',str(ROOT/'src/agents/skills/skill-builder'),'--output',str(dependency)])
plan={'reason':'First discovery could not import two modules with documented AUTHORING_BUILDER_ROOT dependency. These test methods have not executed; run them once with pinned dependency. No successful cases repeated. Preserve initial loader errors.','dependency_manifest':str(dependency/'source-manifest.json'),'scope':'Validator-owned synthetic integration regressions only; companion source remains unchanged and is not assessed.','coverage':'Same predeclared validator scripts denominator; dependency code excluded as external to selected package.'}
(R/'integration-continuation-plan.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=os.pathsep.join([str(R/'instrumentation'),str(R/'source/tests')]),COVERAGE_PROCESS_START=str(R/'coverage.ini'),AUTHORING_BUILDER_ROOT=str(dependency/'source'),TEMP=str(R/'temp'),TMP=str(R/'temp'))
command('integration-missing',[sys.executable,'-B','-X','utf8','-m','unittest','test_authoring','test_authoring_safeguards','-v'],120,env)
command('coverage-final-combine',[sys.executable,'-B','-X','utf8','-m','coverage','combine','--keep',str(R/'coverage')],env=dict(os.environ,COVERAGE_FILE=str(R/'coverage/.coverage-final')))
command('coverage-final-json',[sys.executable,'-B','-X','utf8','-m','coverage','json','--rcfile',str(R/'coverage.ini'),'-o',str(R/'coverage/coverage-final.json')],env=dict(os.environ,COVERAGE_FILE=str(R/'coverage/.coverage-final')))

