"""Fresh attempts after an audit-harness layout error; original attempts retained.

The original harness put second runs under project/edit/docs/plan, outside the
builder's required project/docs/plan. Correct only fixture layout; no SUT edits.
"""
import json
from pathlib import Path
import test_independent as t

t.SUITE = t.RUN / 'fixtures' / 'followup-02'
t.RESULTS = []
original_check = t.check

def check(case, *args, **kwargs):
    return original_check('v2-' + case, *args, **kwargs)

def author_begin(case, c, folder):
    cp = t.put(folder / 'input-contract.json', c)
    runroot = Path(c['project_root']) / 'docs/plan' / (folder.name + '-run')
    result = check(case, t.PY + [t.BUILDER / 'scripts/authoring.py','begin','--contract',cp,'--run-root',runroot], 0, 'state','STAGED')
    if not result or result.get('state') != 'STAGED':
        raise RuntimeError('Setup did not stage; dependent case must remain NOT_RUN: ' + case)
    return runroot

t.check = check
t.author_begin = author_begin

def main():
    t.SUITE.mkdir(parents=True,exist_ok=False)
    t.author_cases()
    folder=t.SUITE/'records';folder.mkdir()
    e,ep,p,pp,s,sp=t.base_records(folder)
    t.put(Path(p['members'][0]['target_root'])/'user.txt','Occupied user destination')
    t.inspect('set-A-preflight-fails',sp,1,True)
    t.set_cases(folder,p,pp,s,sp)
    t.put(t.RUN/'followup-results.json',t.RESULTS)
    print(json.dumps({'total':len(t.RESULTS),'pass':sum(r['status']=='PASS' for r in t.RESULTS),'fail':sum(r['status']=='FAIL' for r in t.RESULTS)}))

if __name__=='__main__':main()
