"""Measure original runtime with the same retained synthetic binding inputs."""
import json
import sys
from evidence import RUN, PACKAGE, command, dump

rows=[]
for path in sorted((RUN/'regression-final/commands').glob('v2-binding-*/command.json')):
    prior=json.loads(path.read_text())
    argv=prior['argv']
    label='direct-'+prior['case']
    current=[sys.executable,'-B','-X','utf8','-m','coverage','run','--append','--branch','--data-file='+str(RUN/'coverage-runtime-final'),'--source='+str(PACKAGE),str(PACKAGE/'assets/adaptive-runtime/check_project_binding.py'),*argv[5:]]
    dump(RUN/'runtime-plans'/(label+'.json'),{'expected':prior['expected'],'input_command_receipt':str(path),'purpose':'Same binding cases executed against original template path for coverage; copied-template cases remain separately retained.'})
    code=command(label,current)
    observed=json.loads((RUN/'commands'/label/'stdout.txt').read_text())
    expected=prior['expected']
    passed=code==expected['exit'] and observed.get(expected['field'])==expected['value']
    rows.append({'case':label,'status':'PASS' if passed else 'FAIL','exit':code,'expected':expected['value'],'actual':observed})
dump(RUN/'runtime-results.json',rows)
print(json.dumps({'cases':len(rows),'passed':sum(r['status']=='PASS' for r in rows)}))
sys.exit(0 if all(r['status']=='PASS' for r in rows) else 1)
