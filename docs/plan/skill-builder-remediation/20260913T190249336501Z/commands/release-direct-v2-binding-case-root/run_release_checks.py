"""Fresh final-byte regression execution, preserving every earlier attempt."""
import json
import os
import sys
from evidence import RUN, PACKAGE, command, dump

os.environ['REMEDIATION_ATTEMPT'] = 'release'
base = [sys.executable, '-B', '-X', 'utf8']
driver = str(RUN/'regression-01/coverage_driver.py')
for label, script in [('legacy','test_legacy_maintenance.py'),('edges','test_acceptance_edges.py')]:
    command('release-'+label, base+['-m','coverage','run','--branch','--source='+str(PACKAGE),'--data-file='+str(RUN/('coverage-release-'+label)),driver,str(RUN/script)])
command('release-maintenance',base+[str(RUN/'regression-release/run_maintenance.py')])
rows=[]
for path in sorted((RUN/'regression-release/commands').glob('v2-binding-*/command.json')):
    prior=json.loads(path.read_text())
    label='release-direct-'+prior['case']
    expected=prior['expected']
    argv=base+['-m','coverage','run','--append','--branch','--data-file='+str(RUN/'coverage-release-runtime'),'--source='+str(PACKAGE),str(PACKAGE/'assets/adaptive-runtime/check_project_binding.py'),*prior['argv'][5:]]
    dump(RUN/'runtime-plans'/(label+'.json'),{'expected':expected,'input_command_receipt':str(path)})
    code=command(label,argv)
    observed=json.loads((RUN/'commands'/label/'stdout.txt').read_text())
    passed=code==expected['exit'] and observed.get(expected['field'])==expected['value']
    rows.append({'case':label,'status':'PASS' if passed else 'FAIL','exit':code,'expected':expected,'actual':observed})
dump(RUN/'runtime-release-results.json',rows)
print(json.dumps({'runtime_cases':len(rows),'passed':sum(r['status']=='PASS' for r in rows)}))
