"""Collect installed coverage.py evidence, including original-path subprocesses."""
import os
from pathlib import Path
import sys
from qa_harness import RUN,TARGET,execute,save

folder=RUN/'coverage'
folder.mkdir(exist_ok=False)
config=folder/'coverage.ini'
config.write_text('[run]\nbranch = True\nparallel = True\ndata_file = '+str(folder/'.coverage')+'\nsource = '+str(TARGET/'scripts')+'\n[report]\nshow_missing = True\n',encoding='utf-8')
startup=folder/'startup'; startup.mkdir()
(startup/'sitecustomize.py').write_text('import coverage\ncoverage.process_startup()\n',encoding='utf-8')
save(folder/'denominator-before-run.json',{'source':str(TARGET/'scripts'),'files':[str(p) for p in sorted((TARGET/'scripts').glob('*.py'))],'exclusions':[],'baseline':'Executed lines in all nine target Python support scripts; branch coverage separately. This is not executable Rust framework coverage. Mutated/copy-path fixture scripts are not aliased to pristine target paths.','collection':'Installed coverage 7.9.0 via startup under this run; no target edits. Child shutdown required to flush data; suite failures and subprocess gaps retained.'})
os.environ['COVERAGE_PROCESS_START']=str(config)
os.environ['PYTHONPATH']=str(startup)+(os.pathsep+os.environ['PYTHONPATH'] if os.environ.get('PYTHONPATH') else '')
execute('coverage-regression-001',['python','-B','-X','utf8','-m','unittest','discover','-s','src/agents/skills/skill-validator/tests','-v'])
del os.environ['COVERAGE_PROCESS_START']
os.environ.pop('PYTHONPATH',None)
execute('coverage-combine-001',['python','-B','-X','utf8','-m','coverage','combine','--rcfile',str(config),'--keep'])
execute('coverage-json-001',['python','-B','-X','utf8','-m','coverage','json','--rcfile',str(config),'-o',str(folder/'coverage.json')])
execute('coverage-report-001',['python','-B','-X','utf8','-m','coverage','report','--rcfile',str(config)])
