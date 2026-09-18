import json,os,pathlib,sys
from run_checks import command
R=pathlib.Path(__file__).resolve().parent
(R/'coverage-merged').mkdir()
env=dict(os.environ,COVERAGE_FILE=str(R/'coverage-merged/.coverage'))
command('coverage-merge-corrected',[sys.executable,'-B','-X','utf8','-m','coverage','combine','--keep',str(R/'coverage')],env=env)
command('coverage-merged-json',[sys.executable,'-B','-X','utf8','-m','coverage','json','--rcfile',str(R/'coverage.ini'),'-o',str(R/'coverage-merged/coverage.json')],env=env)
d=json.loads((R/'coverage-merged/coverage.json').read_text())
print(json.dumps(d['totals']))
command('organization',[sys.executable,'-B','-X','utf8',str(R/'source/scripts/standards_observe.py'),'--source',str(R/'source')])

