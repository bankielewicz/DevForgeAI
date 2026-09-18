"""Read-only receipt inspection and independently adjudicated case assembly."""
import continue_evaluation as c
import importlib.util
import sys
from pathlib import Path
sys.path.insert(0,str(c.PRIOR/'bundle'))
spec=importlib.util.spec_from_file_location('old_audit',c.PRIOR/'audit_native.py')
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a);a.RUN=c.RUN
report=a.audit('DV-03-javascript')
assert report['exit_status']==0 and not report['problems'] and not report['immutable_changes']
c.save(c.RUN/'inputs/native-audits/DV-03-javascript-warm/audit.json',report)

def visit(value,project,checked):
    if isinstance(value,list):
        for row in value: visit(row,project,checked)
    elif isinstance(value,dict):
        required=value.get('required_path',value.get('required'))
        actual=value.get('actual_path',value.get('actual',value.get('observed_path')))
        if isinstance(required,str) and isinstance(actual,str) and 'sha256' in value:
            assert required==actual, (required,actual)
            p=Path(actual); assert p.is_relative_to(project) and p.is_file()
            assert c.h.sha(p.read_bytes())==value['sha256'].lower(),str(p)
            checked.append({'actual_path':str(p),'sha256':c.h.sha(p.read_bytes())})
        elif 'path' in value and 'sha256' in value and Path(value['path']).is_absolute():
            p=Path(value['path']);assert p.is_relative_to(c.RUN) and p.is_file()
            assert c.h.sha(p.read_bytes())==value['sha256'].lower(),str(p)
            checked.append({'actual_path':str(p),'sha256':c.h.sha(p.read_bytes())})
        for child in value.values(): visit(child,project,checked)

for name,files in {
    'RV-04':['custom receipts/readback.json'],
    'DV-08':['evidence/readback.json'],
    'DV-03-javascript':['evidence/readback.json','evidence/continuation-003-readback.json','evidence/continuation-003-verification.json'],
}.items():
    project=c.RUN/'trials'/name/'project';checked=[]
    for f in files: visit(c.load(project/f),project,checked)
    assert checked,name
    c.save(c.RUN/'inputs/native-audits'/name/'final-readback-review.json',{'trial_id':name,'records':files,'checked':checked,'count':len(checked),'problems':[],'limitation':'Supported explicit path/hash rows; whole project manifests and semantic review separately verified.'})
    print('READBACK',name,len(checked))

decisions=c.load(c.RUN/'inputs/native-decisions-initial.json')
decisions['RV-04']={'result':'PASS','reason':'Fresh cold session rejected the supplied unverified COMPLETE draft and stale receipts/ mapping, reread original custom receipts/ selection, retained draft and all protected inputs, completed real missing-behavior red then unchanged eight-method green/QA, and delivered under the exact required root with independent literal-path and digest readback.'}
decisions['DV-03']={'result':'PASS','reason':'Composite scoped portability evidence: Python cold session completed ten unittest methods plus five integration cases. JavaScript cold session retained genuine direct-node red/green and correctly reported required node --test worker EPERM as incomplete. A separately authorized exact host node --test run passed six of six tests on the unchanged candidate. One explicitly approved 600-second warm continuation verified actual host streams, all 41 prior project files and prerequisites, preserved every earlier file and four host receipts, then completed delivery using five new evidence files only. Warm continuation exited in 193.641 seconds; no model/product changes or further test reruns. This does not establish JavaScript worker execution inside the sandbox or an entirely cold successful JavaScript delivery.',
    'native_attempts':{'DV-03-python':'002','DV-03-javascript':'003'},
    'evidence_origin':'fresh Python and JavaScript cold sessions plus separately authorized Windows host QA and approved warm JavaScript delivery'}
c.save(c.RUN/'inputs/native-decisions.json',decisions)
print('DECISIONS',len(decisions))
