"""Read-only completeness grader for this campaign's retained unittest JSONL."""
import argparse
import json
from pathlib import Path

def grade(folder):
    expected=json.loads((folder/'expected-results.json').read_text())
    rows=[json.loads(line) for line in (folder/'results.jsonl').read_text().splitlines()]
    ids=[row['case_id'] for row in rows]
    errors=[]
    if len(ids)!=len(set(ids)):errors.append('Duplicate executed case identity')
    if set(ids)!=set(expected):errors.append('Executed inventory differs from frozen expected inventory')
    for row in rows:
        if set(row)!={'case_id','result','seconds','details'}:errors.append('Invalid result fields')
        if row['result'] not in ('PASS','FAIL','ERROR','NOT_RUN'):errors.append('Invalid result state')
        if row['result']!=expected.get(row['case_id']):errors.append(row['case_id']+': '+row['result'])
    passed=sum(row['result']=='PASS' and row['case_id'] in expected for row in rows)
    return dict(outcome='FAIL' if errors else 'PASS',required=len(expected),passed=passed,
                percent=100*passed/len(expected) if expected else 0,errors=errors,
                authority='Evaluation evidence only')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('folder',type=Path);args=parser.parse_args()
    result=grade(args.folder);print(json.dumps(result,indent=2));raise SystemExit(0 if result['outcome']=='PASS' else 1)
