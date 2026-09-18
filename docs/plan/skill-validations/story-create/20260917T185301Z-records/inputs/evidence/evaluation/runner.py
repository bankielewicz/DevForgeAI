"""Read frozen JSONL cases, execute helper argv, and retain honest observations."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def manifest(root):
    return [{'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(root.rglob('*')) if p.is_file()]

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cases',required=True)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    cases_path=Path(args.cases).resolve();out=Path(args.output).resolve()
    out.mkdir(parents=True,exist_ok=False)
    cases=[json.loads(line) for line in cases_path.read_text(encoding='utf-8').splitlines() if line.strip()]
    if not cases or len({v['case_id'] for v in cases})!=len(cases):raise ValueError('Unique nonempty case inventory required')
    rows=[]
    for case in cases:
        if set(case)!={'case_id','argv','cwd','project_root','expected','inputs','timeout_seconds'}:raise ValueError('Unexpected case fields')
        evidence=out/case['case_id'];evidence.mkdir()
        root=Path(case['project_root']);before=manifest(root)
        for item in case['inputs']:
            if sha(Path(item['path']))!=item['sha256']:raise ValueError('Changed sealed input')
        started=datetime.datetime.now(datetime.timezone.utc).isoformat();tick=time.monotonic()
        result=subprocess.run(case['argv'],cwd=case['cwd'],stdin=subprocess.DEVNULL,capture_output=True,timeout=case['timeout_seconds'])
        (evidence/'stdout.txt').write_bytes(result.stdout);(evidence/'stderr.txt').write_bytes(result.stderr)
        after=manifest(root)
        expected=case['expected'];issues=[]
        if result.returncode!=expected['exit_code']:issues.append('exit_code')
        observed=None
        if 'reason_code' in expected:
            try:observed=json.loads(result.stdout)
            except (ValueError,UnicodeError):issues.append('invalid_json')
            if observed is not None:
                for key in ['reason_code','status']:
                    if observed.get(key)!=expected[key]:issues.append(key)
                if observed.get('details')!=[]:issues.append('unsanitized_details')
        if before!=after:issues.append('read_only_effects')
        record={'schema_version':'story-eval-result-v1','case_id':case['case_id'],'result':'FAIL' if issues else 'PASS','issues':issues,'argv':case['argv'],'cwd':case['cwd'],'started_at':started,'elapsed_seconds':time.monotonic()-tick,'exit_code':result.returncode,'observation':observed,'before':before,'after':after,'inputs':case['inputs']}
        (evidence/'receipt.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
        rows.append(record)
    with (out/'results.jsonl').open('x',encoding='utf-8',newline='\n') as stream:
        for row in rows:stream.write(json.dumps(row,ensure_ascii=True)+'\n')
    summary={'required':len(rows),'passing':sum(r['result']=='PASS' for r in rows),'failing':sum(r['result']=='FAIL' for r in rows),'cases_sha256':sha(cases_path),'framework_acceptance':'NOT_EVALUATED'}
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary))
    return 0 if not summary['failing'] else 1

if __name__=='__main__':raise SystemExit(main())
