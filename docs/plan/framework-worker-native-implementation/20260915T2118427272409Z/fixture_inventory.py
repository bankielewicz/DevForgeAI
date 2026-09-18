"""Locate retained synthetic admission fixtures from this development time window."""
import datetime
import json
from record import ROOT, WORK, sha, write

def timestamp(path,field):
    return datetime.datetime.fromisoformat(json.loads(path.read_text())[field]).timestamp()
start=timestamp(ROOT/'10-identity-red/receipt.json','start')
end=timestamp(ROOT/'04-coverage/receipt.json','end')
roots=[]
for root in sorted((WORK/'docs/plan/framework-worker-trials').glob('NI-admission-*')):
    if start <= root.stat().st_ctime <= end:
        files=[{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(root.rglob('*')) if p.is_file()]
        roots.append({'path':str(root),'created_epoch':root.stat().st_ctime,'files':files})
write('external-synthetic-fixtures.json',{'selection':'NI-admission test prefix and recorded developer command time window',
    'start_epoch':start,'end_epoch':end,'native_codex_trial':False,'roots':roots})
print(json.dumps({'retained_synthetic_roots':len(roots)}))
