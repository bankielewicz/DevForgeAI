"""Execute bound JSONL observations through deterministic evidence graders.

No target or actor execution; native trial runners are retained under inputs/.
Semantic conclusions are identified as primary-validator adjudications.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
from graders import metric, reduce_cases, verify_reference

def strict_pairs(pairs):
    result={}
    for key,value in pairs:
        if key in result: raise ValueError('Duplicate JSON key')
        result[key]=value
    return result

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'),object_pairs_hook=strict_pairs,parse_constant=lambda value: (_ for _ in ()).throw(ValueError('Nonfinite JSON')))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-root',required=True)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    root=Path(args.run_root).resolve()
    bundle=root/'evaluation'
    manifest=read(bundle/'bundle-manifest.json')
    for reference in manifest['artifacts']:
        if not verify_reference(root,reference): raise ValueError('Bundle artifact changed: '+reference['path'])
    source=read(root/'source-manifest.json')
    rows=[]
    for row in source['files']:
        p=root/'source'/row['path']
        raw=p.read_bytes()
        if len(raw)!=row['bytes'] or hashlib.sha256(raw).hexdigest()!=row['sha256']: raise ValueError('Source changed')
        rows.append({'path':row['path'],'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
    digest=hashlib.sha256(json.dumps(rows,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
    if digest!=manifest['package_digest'] or digest!=source['package_digest']: raise ValueError('Package binding mismatch')
    cases=read(bundle/'cases.json')
    observations=[]
    for line in (bundle/'observations.jsonl').read_text(encoding='utf-8').splitlines():
        if not line.strip(): continue
        row=json.loads(line,object_pairs_hook=strict_pairs)
        if set(row)!={'case_id','result','reason','method','evidence'}: raise ValueError('Observation schema mismatch')
        if not row['reason'] or row['method'] not in ('deterministic','semantic','behavioral'): raise ValueError('Missing observation basis')
        if row['result'] in ('PASS','FAIL') and not row['evidence']: raise ValueError('Claim lacks evidence')
        for reference in row['evidence']:
            if not verify_reference(root,reference): raise ValueError('Observation evidence changed')
        observations.append(row)
    summary=reduce_cases(cases,observations)
    observed={row['case_id']:row for row in observations}
    output=Path(args.output)
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('x',encoding='utf-8') as stream:
        for case in cases:
            row=observed.get(case['case_id'],{'case_id':case['case_id'],'result':'NOT_RUN','reason':'No observation supplied','method':'behavioral','evidence':[]})
            stream.write(json.dumps({'schema_version':'qa-evaluation-result-v1','package_digest':digest,**row},ensure_ascii=False)+'\n')
        stream.write(json.dumps({'schema_version':'qa-evaluation-summary-v1','package_digest':digest,**summary,'framework_acceptance':'NOT_EVALUATED'})+'\n')
    print(json.dumps(summary))
    return 1 if summary['failed'] else 2 if summary['unperformed'] else 0

if __name__=='__main__':
    try: sys.exit(main())
    except (ValueError,OSError,KeyError,TypeError) as error:
        print(type(error).__name__+': '+str(error),file=sys.stderr)
        sys.exit(2)
