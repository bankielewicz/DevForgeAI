"""Supplemental exact-command product QA; not another cold native trial."""
import continue_evaluation as c
from pathlib import Path
import shutil
import sys
base=c.RUN/'trials/DV-03-javascript'
project=base/'project'
attempt=sys.argv[1]
assert (base/'attempt-002/result.json').exists(),'Wait for native task finalization before independent host check'
before=c.h.inventory(project)
cmd=[shutil.which('node'),'--test']
c.save(c.RUN/'trials/javascript-host-qa'/('plan-'+attempt+'.json'),{
 'check_id':'DV-03-JS-HOST-QA','candidate':before,'command':cmd,'working_directory':str(project),
 'expected':'Six existing node:test cases pass with node --test; no source or test changes.',
 'timeout_seconds':120,'permitted_write_root':str(c.RUN/'commands'/('javascript-host-qa-'+attempt)),
 'authority':'Read-only product QA on completed disposable candidate. Does not rewrite native sandbox ERROR or claim cold-session completion.',
 'retry':'A host-access retry is only for the observed sandbox EPERM; retain each attempt.'})
record=c.h.execute('javascript-host-qa-'+attempt,cmd,cwd=project,timeout=120)
after=c.h.inventory(project)
c.save(c.RUN/'trials/javascript-host-qa'/('readback-'+attempt+'.json'),{
 'before':before,'after':after,'unchanged':before['files']==after['files'],'command_receipt':record})
assert before['files']==after['files'],'Unexpected candidate mutation'
print('SUPPLEMENTAL_HOST_QA',record['termination'],record['exit_status'])

