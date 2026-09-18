"""Read-only CLI confirmation of the two established QA-09 findings."""
import hashlib,json,subprocess,time,datetime
from pathlib import Path
root=Path(__file__).resolve().parent
exe=root/'build-target/debug/devforgeai-codex-worker-probe.exe'
out=root/'attempts/24-cli-confirm'
out.mkdir(exist_ok=False)
manifest=json.loads((root/'binary-manifest.json').read_text(encoding='utf-8-sig'))
assert hashlib.sha256(exe.read_bytes()).hexdigest()==next(v['sha256'] for v in manifest if v['path']==str(exe))
results=[]
for label,fixture in [('QA-LOG-01','qa09rE4EEf'),('QA-LOG-02','qa09cCNcpd')]:
    run=root/'attempts/16-qa09/fixtures'/fixture/'run'
    before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in run.iterdir() if p.is_file()}
    args=[str(exe),'inspect','--run-dir',str(run),'--after','0','--limit','100']
    start=time.monotonic()
    result=subprocess.run(args,cwd='C:/Projects/DevForgeAI',capture_output=True,timeout=15,creationflags=subprocess.CREATE_NO_WINDOW)
    (out/(label+'.stdout.json')).write_bytes(result.stdout)
    (out/(label+'.stderr.txt')).write_bytes(result.stderr)
    observed=json.loads(result.stdout)
    after={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in run.iterdir() if p.is_file()}
    results.append({'issue':label,'argv':args,'cwd':'C:/Projects/DevForgeAI','exit_code':result.returncode,'state':observed['state'],
                    'elapsed_seconds':time.monotonic()-start,'unchanged':before==after,'run':str(run)})
    assert before==after
(out/'receipt.json').write_text(json.dumps({'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'executable_sha256':hashlib.sha256(exe.read_bytes()).hexdigest(),'results':results},indent=2))
print(json.dumps(results,indent=2))

