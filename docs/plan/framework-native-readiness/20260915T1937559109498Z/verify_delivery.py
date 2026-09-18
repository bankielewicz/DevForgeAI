"""Documentation/link/byte checks only. No product tests, installs or acceptance."""
import datetime,hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent
WORK=Path('C:/Projects/DevForgeAI')
SPECS=[WORK/'docs/specs/framework/runtime'/n for n in ['codex-worker-native-readiness-v1.md','acceptance-authority-v1.md','acceptance-worker-evidence-v1.md']]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(n,v):(ROOT/n).write_text(json.dumps(v,indent=2)+'\n')
checks=[]
def check(name,good,detail=None):
    checks.append({'name':name,'pass':bool(good),'detail':detail})
    if not good:write('verification.json',checks);raise SystemExit('Document verification failed: '+name)

candidate=read(ROOT/'candidate-before.json')
after=[{'path':r['path'],'expected':r['sha256'],'actual':sha(r['path']),'matches':sha(r['path'])==r['sha256']} for r in candidate]
write('candidate-after.json',after);check('candidate32 unchanged',len(after)==32 and all(x['matches'] for x in after))
inputs=read(ROOT/'input-identities.json')
after=[{'path':r['path'],'expected':r['sha256'],'actual':sha(r['path']),'matches':sha(r['path'])==r['sha256']} for r in inputs]
write('input-after.json',after);check('original specifications and instructions unchanged',all(x['matches'] for x in after))
sources=read(ROOT/'profile-source-inventory.json')
observations=[]
for r in sources:
    p=Path(r['path'])
    observations.append({'path':r['path'],'matches':sha(p)==r['sha256'] if 'sha256' in r and p.is_file() else p.exists()==r.get('exists',True),'actual_sha256':sha(p) if p.is_file() else None})
write('profile-source-after.json',observations)
check('profile source readback recorded',len(observations)==len(sources),{'drift':[r['path'] for r in observations if not r['matches']]})
launcher=read(ROOT/'launcher-identity.json')
check('pinned physical executable remains same bytes',sha(launcher['physical']['path'])==launcher['physical']['sha256'])
for name in ['codex-version','codex-help','app-server-help']:
    r=read(ROOT/(name+'.receipt.json'))
    check(name+' succeeded and output bound',r['exit']==0 and sha(ROOT/(name+'.stdout.txt'))==r['stdout_sha256'] and sha(ROOT/(name+'.stderr.txt'))==r['stderr_sha256'])
inventory=read(ROOT/'authority-worker-inventory.proposed.json')
check('authority inventory32 source package files',len(inventory['candidate_files'])==32)
check('authority inventory28 unique mandatory groups',len(inventory['required_cases'])==len({x['case_id'] for x in inventory['required_cases']})==28 and all(x['mandatory'] for x in inventory['required_cases']))
check('authority inventory50 unique tests and6 units',len(inventory['tests'])==len({x['name'] for x in inventory['tests']})==50 and sum(x['level']=='unit' for x in inventory['tests'])==6)
check('authority inventory8 source paths and1 zero-line module',len(inventory['source_files'])==8 and sum(x['zero_executable'] for x in inventory['source_files'])==1)
check('operator selected attested import',read(ROOT/'operator-selection.json')['selection']=='operator_attested_import')
request_fields={'schema_version','project_id','checkout_id','work_id','run_id','candidate_sha256','checkout_root','run_dir','worker_executable','worker_sha256','adapter','scenario','profile'}
for code in ['WN-01','WN-02']:
    b=ROOT/'trials'/code;r=read(b/'request.draft.json');v=read(b/'profile-review.unqualified.json')
    check(code+' closed v1 draft and byte-bound fixture/review',set(r)==request_fields and r['candidate_sha256']==sha(b/'task.json') and r['profile']['review_sha256']==sha(b/'profile-review.unqualified.json'))
    check(code+' review remains explicitly unqualified',all(x is False for x in v['findings'].values()))
    check(code+' run directory not created',not Path(r['run_dir']).exists())
    for name in ['task.json','prompt.txt','expected.json','output-schema.json']:
        check(code+' original '+name+' unchanged',sha(b/name)==sha(WORK/'docs/specs/framework/runtime/fixtures/codex-worker-v1'/name))
native=SPECS[0].read_text();auth=SPECS[1].read_text()
check('twelve native readiness criteria',len(set(re.findall(r'^\| (NI-T\d+) \|',native,re.M)))==12)
check('twenty authority qualification groups',len(set(re.findall(r'^\| (AU-\d+) \|',auth,re.M)))==20)
check('authority explicitly incorporates owner selection','user explicitly selected **operator-attested evidence first**' in auth)
docs=SPECS+list(ROOT.glob('*.md'))
for p in docs:
    for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
        if target.startswith(('https://','http://','#')):continue
        raw=target.split('#',1)[0]
        check('link '+p.name+' -> '+raw,(p.parent/raw).resolve().exists())
    check('no unresolved template slots in '+p.name,not any(x in p.read_text() for x in ['[PATH / CANDIDATE]','<project>','TODO','[SPECIFICATION PATHS]']))
for p in ROOT.rglob('*.json'):
    read(p)
check('all new JSON files parse',True)
write('verification.json',{'kind':'documentation/readback only','executed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'passed':sum(x['pass'] for x in checks),'total':len(checks),'runtime_tests':'NOT_RUN; no product implementation changed','native_trials':'NOT_RUN','framework_acceptance':'NOT_EVALUATED'})
paths=SPECS+[p for p in ROOT.rglob('*') if p.is_file() and p.name not in ['delivery-manifest.json','delivery-readback.json']]
manifest=[{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(set(paths))]
write('delivery-manifest.json',manifest)
readback=[{'path':r['path'],'matches':sha(r['path'])==r['sha256']} for r in read(ROOT/'delivery-manifest.json')]
assert all(x['matches'] for x in readback)
write('delivery-readback.json',{'manifest_sha256':sha(ROOT/'delivery-manifest.json'),'all_match':True,'entries':readback})
print(json.dumps({'document_checks':len(checks),'passed':sum(x['pass'] for x in checks),'delivery_entries':len(readback),'delivery_manifest_sha256':sha(ROOT/'delivery-manifest.json'),'profile_drift':[x['path'] for x in observations if not x['matches']],'source_unchanged':32,'native':'NOT_RUN','framework_acceptance':'NOT_EVALUATED'}))
