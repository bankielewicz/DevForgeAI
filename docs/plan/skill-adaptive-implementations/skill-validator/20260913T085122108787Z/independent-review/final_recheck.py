"""Read-only unchanged-fixture confirmation for independent findings IR-20..23."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

def main():
    root=Path(__file__).resolve().parent
    out=root/'attempt-05'
    out.mkdir(exist_ok=False)
    helper=root.parents[5]/'src/agents/skills/skill-validator/scripts/adaptive_observe.py'
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in helper.parent.glob('*.py')}
    (out/'script-hashes.json').write_text(json.dumps(hashes,indent=2),encoding='utf-8')
    for ident in ['IR-20','IR-21','IR-22','IR-23']:
        fixture=root/('attempt-04' if ident=='IR-23' else 'attempt-03')/ident/'set'
        command=[sys.executable,'-B','-X','utf8',str(helper),'records','--run-root',str(fixture)]
        result=subprocess.run(command,cwd=root,capture_output=True,timeout=120)
        case=out/ident
        case.mkdir()
        (case/'stdout.json').write_bytes(result.stdout)
        (case/'stderr.txt').write_bytes(result.stderr)
        (case/'receipt.json').write_text(json.dumps({'command':command,'exit_code':result.returncode},indent=2),encoding='utf-8')
        print(ident,result.returncode,json.loads(result.stdout)['status'])

if __name__=='__main__':
    main()
