"""Independent strict JSONL accounting against pre-execution named inventories."""
import hashlib
import json
from pathlib import Path
from prepare_validation import ROOT,put,ref
def pairs(values):
    out={}
    for key,value in values:
        if key in out:raise ValueError('Duplicate key: '+key)
        out[key]=value
    return out
def read(path):return json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
results=[]
for name,expected_file,field in [('independent-tests','expected.json',None),('regressions','expected.json',None),('adaptive-regressions','plan.json','expected'),('linux-checks','plan.json','expected')]:
    folder=ROOT/'observations'/name
    expected=read(folder/expected_file)
    if field:expected=expected[field]
    rows=[json.loads(line,object_pairs_hook=pairs) for line in (folder/'results.jsonl').read_text(encoding='utf-8').splitlines()]
    keys=[r['case_id'] for r in rows]
    errors=[]
    if len(keys)!=len(set(keys)):errors.append('Duplicate case results')
    if set(keys)!=set(expected):errors.append('Missing or unexpected case IDs')
    for row in rows:
        if not set(row) <= {'case_id','result','detail','elapsed_seconds'} or not {'case_id','result','detail'}<=set(row):errors.append('Invalid row fields')
        if row['result'] not in ['PASS','FAIL','ERROR','NOT_RUN']:errors.append('Invalid result')
        if not isinstance(row['detail'],str):errors.append('Invalid detail')
    results.append({'inventory':name,'required':len(expected),'raw_passing':sum(r['result']=='PASS' for r in rows),'nonpasses':[r['case_id'] for r in rows if r['result']!='PASS'],'accounting_errors':errors,'expected_ref':ref(str((folder/expected_file).relative_to(ROOT)).replace('\\','/')),'observed_ref':ref(str((folder/'results.jsonl').relative_to(ROOT)).replace('\\','/'))})
put('observations/deterministic-accounting.json',{'result':'PASS' if all(not r['accounting_errors'] for r in results) else 'FAIL','meaning':'Accounting integrity only; retained raw nonpasses are not changed to passes. Corrected harness observations are separate.','inventories':results})
bundle=read(ROOT/'evaluation-bundle-manifest.json')
bundle['artifacts'].append(ref('grade_evidence.py'))
put('evaluation-bundle-manifest.json',bundle)
print(json.dumps({'accounting_errors':sum(len(r['accounting_errors']) for r in results),'raw_case_rows':sum(r['required'] for r in results),'raw_nonpasses':sum(len(r['nonpasses']) for r in results)}))
