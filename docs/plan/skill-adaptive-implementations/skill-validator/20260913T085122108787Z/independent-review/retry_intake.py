"""New attempts correcting the review harness manifest serialization, not candidate output."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'attempt-02'
HELPER=ROOT.parents[5]/'src/agents/skills/skill-validator/scripts/adaptive_observe.py'

def main():
    OUT.mkdir(exist_ok=False)
    reason='Attempt 01 IR-11 used sorted manifest object keys in package digest. Existing observe.compact preserves schema manifest key order path,bytes,sha256. Correct synthetic inputs in fresh attempt; retain original cases/results. This is an oracle harness correction, not a target repair.'
    (OUT/'reason.txt').write_text(reason,encoding='utf-8')
    value=json.loads((ROOT/'fixtures/IR-11/request.json').read_text(encoding='utf-8'))
    for member in value['members']:
        manifest=json.loads(Path(member['package']['manifest']['path']).read_text(encoding='utf-8'))
        member['package']['package_digest']=hashlib.sha256(json.dumps(manifest,separators=(',',':'),ensure_ascii=False).encode('utf-8')).hexdigest()
    rows=[]
    for ident in ['IR-11','IR-12','IR-13','IR-14','IR-15']:
        candidate=copy.deepcopy(value)
        if ident=='IR-12': candidate['members'].append(copy.deepcopy(candidate['members'][0]))
        if ident=='IR-13': candidate['members'][1]['depends_on']=['C']
        if ident=='IR-14': candidate['unknown']=True
        if ident=='IR-15': candidate['members'][0]['package']['package_digest']='0'*64
        case=OUT/ident
        case.mkdir()
        request=case/'request.json'
        request.write_text(json.dumps(candidate,indent=2),encoding='utf-8')
        command=[sys.executable,'-B','-X','utf8',str(HELPER),'intake-set','--request',str(request),'--request-sha256',hashlib.sha256(request.read_bytes()).hexdigest()]
        result=subprocess.run(command,cwd=case,capture_output=True,timeout=120)
        (case/'stdout.json').write_bytes(result.stdout)
        (case/'stderr.txt').write_bytes(result.stderr)
        row={'id':ident,'command':command,'exit_code':result.returncode,'observation':json.loads(result.stdout)}
        (case/'receipt.json').write_text(json.dumps(row,indent=2),encoding='utf-8')
        rows.append(row)
    (OUT/'results-summary.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
    print(json.dumps([{'id':r['id'],'exit_code':r['exit_code'],'status':r['observation']['status']} for r in rows],indent=2))

if __name__=='__main__':
    main()
