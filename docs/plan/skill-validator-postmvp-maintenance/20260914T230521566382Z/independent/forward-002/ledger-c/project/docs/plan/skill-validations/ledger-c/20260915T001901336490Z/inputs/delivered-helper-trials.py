"""Independent fixed-oracle helper trials, run once through the sealed runner."""
import datetime, hashlib, json, subprocess, sys
from pathlib import Path

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def grade(case, code, stdout, stderr, output, preserved, changes):
    ok=preserved and not (set(changes)-{case['output']})
    if case['kind']=='valid':
        try: actual=json.loads(output)
        except (ValueError,TypeError): actual=None
        ok=ok and code==0 and not stderr and type(actual) is dict and set(actual)=={'total'} and type(actual['total']) is int and actual['total']==case['total']
    elif case['kind']=='help': ok=ok and code==0 and 'input' in stdout.lower() and 'output' in stdout.lower() and not output
    else: ok=ok and code!=0 and bool(stderr.strip()) and output is None
    return bool(ok)

if __name__=='__main__':
    root=Path.cwd(); config=json.loads(Path(sys.argv[1]).read_text()); results=[]
    for case in config['cases']:
        folder=root/case['id']; inp=folder/'input file.json'; dest=folder/case['output']
        before={p.name:digest(p) for p in folder.iterdir() if p.is_file()}
        if case['kind']=='help': args=['--help']
        elif case['kind']=='args': args=[]
        else: args=[str(inp if case['kind']!='missing' else folder/'absent.json'),str(dest)]
        argv=[sys.executable,'-B','-S',config['helper'],*args]
        start=datetime.datetime.now(datetime.timezone.utc).isoformat()
        proc=subprocess.run(argv,cwd=folder,input=b'',capture_output=True,timeout=120)
        after={p.name:digest(p) for p in folder.iterdir() if p.is_file()}
        changed=sorted(k for k in before.keys()|after.keys() if before.get(k)!=after.get(k))
        preserved=all(after.get(k)==v for k,v in before.items() if k!=case['output'] or case['kind']=='alias')
        # Alias output already existed as input: grade absence of NEW output separately.
        out=dest.read_text(encoding='utf-8') if dest.exists() and case['kind']!='alias' else None
        result={'case_id':case['id'],'requirements':case['requirements'],'argv':argv,'cwd':str(folder),'timeout_seconds':120,'started_at':start,'ended_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':proc.returncode,'stdout':proc.stdout.decode('utf-8'),'stderr':proc.stderr.decode('utf-8'),'before':before,'after':after,'changed_paths':changed,'preserved':preserved,'output':out}
        result['result']='PASS' if grade(case,proc.returncode,result['stdout'],result['stderr'],out,preserved,changed) else 'FAIL'
        results.append(result)
    (root/'results.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in results),encoding='utf-8')
    (root/'summary.json').write_text(json.dumps({'total':len(results),'passed':sum(r['result']=='PASS' for r in results),'failed':sum(r['result']=='FAIL' for r in results)}),encoding='utf-8')
