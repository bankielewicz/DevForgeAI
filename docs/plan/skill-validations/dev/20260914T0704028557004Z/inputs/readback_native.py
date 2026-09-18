"""Independent readback of already completed trial destination receipts."""
import continue_evaluation as c
from pathlib import Path
import sys
for name in sys.argv[1:]:
    base=c.RUN/'trials'/name
    plan=c.load(base/'plan.json');project=Path(plan['permitted_write_root'])
    original=project/plan['selected_evidence_value']
    inventory=c.h.inventory(project)
    records=[]
    for row in inventory['files']:
        p=project/row['path']
        if p.name!='readback.json' or not p.is_relative_to(original): continue
        doc=c.load(p);problems=[];checked=[]
        if doc.get('selected_evidence_value')!=plan['selected_evidence_value']: problems.append('Original selected value mismatch')
        for key in ['resolved_evidence_root','required_root','observed_root']:
            if key in doc and Path(doc[key])!=original: problems.append(key+' mismatch')
        for output in doc.get('files',doc.get('outputs',[])):
            if not isinstance(output,dict) or 'required_path' not in output: continue
            actual=Path(output.get('actual_path',output.get('observed_path','')))
            required=Path(output['required_path'])
            if actual!=required or not actual.is_relative_to(project): problems.append('Path mismatch '+str(actual)); continue
            if not actual.is_file(): problems.append('Missing '+str(actual)); continue
            digest=c.h.sha(actual.read_bytes())
            if digest!=output['sha256'].lower(): problems.append('Digest mismatch '+str(actual))
            checked.append({'actual_path':str(actual),'sha256':digest})
        records.append({'readback_file':str(p),'files_checked':len(checked),'checks':checked,'problems':problems})
    outcome={'trial_id':name,'original_selection':plan['selected_evidence_value'],'original_root':str(original),
             'records':records,'limitations':['Only supported explicit required/actual file rows checked; prose and unsupported schemas remain manual.',
               'Selected project after-manifest and receipt audits are separate observations.']}
    c.save(c.RUN/'inputs/native-audits'/name/'destination-readback.json',outcome)
    print(name,[{'files_checked':x['files_checked'],'problems':x['problems']} for x in records])

