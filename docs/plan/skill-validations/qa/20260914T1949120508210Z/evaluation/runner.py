"""Run independent evidence-vector checks and account for all skill scenarios.

Native scenarios never pass from vectors or from missing artifacts. Each native
result needs a completed attempt, independently reviewed artifacts and trace.
This run deliberately leaves missing behavioral evidence unqualified.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
from graders import metric, ordered_trace, reduce_cases, report_contract

ROOT=Path(__file__).resolve().parents[1]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def reference(path):
    return {'path':path.relative_to(ROOT).as_posix(),'sha256':digest(path)}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    output=Path(args.output).resolve()
    output.relative_to(ROOT)
    if output.exists():
        raise ValueError('Refusing to overwrite an existing JSONL attempt')
    binding=json.loads((ROOT/'evaluation/bundle-manifest.json').read_bytes())
    for item in binding['inputs']:
        if digest(ROOT/item['path']) != item['sha256']:
            raise ValueError('Bundle input changed: '+item['path'])
    vectors=json.loads((ROOT/'evaluation/fixtures.json').read_bytes())
    results=[]
    for vector in vectors:
        function={'metric':metric,'ordered_trace':ordered_trace,'reduce_cases':reduce_cases,'report_contract':report_contract}[vector['function']]
        actual=function(*vector['args'],**vector.get('kwargs',{}))
        results.append(dict(schema_version='qa-eval-result-v1',case_id=vector['id'],kind='grader-control',required=True,result='PASS' if actual==vector['expected'] else 'FAIL',expected=vector['expected'],observed=actual,reason='Independent evidence-vector oracle; does not execute the QA skill.',evidence=[reference(ROOT/'evaluation/fixtures.json')]))
    catalog=json.loads((ROOT/'case-catalog.json').read_bytes())
    for case in catalog:
        folder=ROOT/'trials'/case['case_id']
        attempts=sorted(folder.glob('attempt-[0-9][0-9][0-9].json')) if folder.exists() else []
        observations=[json.loads(p.read_bytes()) for p in attempts]
        result='NOT_RUN'
        reason='Required native variants have no completed behavioral evidence; fixture/campaign implementation remains outstanding.'
        if observations:
            reason='Native attempt(s) retained; '+('; '.join('timeout' if x['timeout'] else 'exit '+str(x['exit_code']) for x in observations))+'. Incomplete attempts cannot qualify the scenario.'
        results.append(dict(schema_version='qa-eval-result-v1',case_id=case['case_id'],kind='skill-scenario',required=True,result=result,expected=case['expected'],observed={'attempts':len(attempts),'completed_scenario':False},reason=reason,evidence=[reference(p) for p in attempts]+[reference(ROOT/'case-catalog.json')]))
    for row in results:
        assert set(row)=={'schema_version','case_id','kind','required','result','expected','observed','reason','evidence'}
        assert row['result'] in ('PASS','FAIL','NOT_RUN','ERROR')
    ids=[x['case_id'] for x in results]
    assert len(ids)==len(set(ids))
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('x',encoding='utf-8',newline='\n') as stream:
        for row in results:
            stream.write(json.dumps(row,ensure_ascii=False,allow_nan=False)+'\n')
    summary={kind:{status:sum(x['kind']==kind and x['result']==status for x in results) for status in ['PASS','FAIL','NOT_RUN','ERROR']} for kind in ['grader-control','skill-scenario']}
    print(json.dumps({'counts':summary,'skill_outcome':reduce_cases([(x['case_id'],x['result']) for x in results if x['kind']=='skill-scenario']),'framework_acceptance':'NOT_EVALUATED'},indent=2))
    return 1 if any(x['result']=='FAIL' for x in results) else 2 if any(x['result'] in ('NOT_RUN','ERROR') for x in results) else 0

if __name__=='__main__':
    sys.exit(main())
