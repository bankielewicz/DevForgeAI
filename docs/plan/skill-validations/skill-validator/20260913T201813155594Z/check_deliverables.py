"""Read-back of isolated legacy/new evidence records, with retained attempts."""
import json
import sys
from harness import RUN, LOADED, read, write, save, ref, execute

case_results=json.loads(read(RUN/'probe-results.json'))+[json.loads(read(RUN/'results/H11.json'))]
for r in case_results:
    cid=r['case_id']
    write(RUN/'supplemental-records'/f'{cid}.json',read(RUN/'commands'/cid/'stdout.txt'))
for cid,program,root in [('LEGACY-RECORDS','observe.py',RUN/'member-records'),('ADAPTIVE-RECORDS','adaptive_observe.py',RUN/'supplemental-records')]:
    rec=execute(cid,[sys.executable,'-B','-X','utf8',str(LOADED/'scripts'/program),'records','--run-root',str(root)])
    print(cid,rec['exit'],flush=True)
