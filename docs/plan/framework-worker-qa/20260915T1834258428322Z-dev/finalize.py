"""Readback and arithmetic only; development evidence, never framework authority."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import datetime

ROOT = Path(__file__).resolve().parent
GREEN = ROOT.with_name('20260915T1834258428322Z-green')
OLD = ROOT.with_name('20260915T1800141514833Z')
WORK = Path('C:/Projects/DevForgeAI')
PACKAGE = WORK / 'devforgeai/experiments/codex-worker-probe'

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(name, value): (ROOT/name).write_text(json.dumps(value,indent=2),encoding='utf-8')
def identity(p): return {'path':str(p.resolve()),'bytes':p.stat().st_size,'sha256':sha(p)}

old = {e['path']:e for e in read(OLD/'selected-manifest.json')}
candidate = read(GREEN/'selected-manifest.json')
for e in candidate: assert sha(e['path']) == e['sha256'], e['path']
write('candidate-manifest.json',candidate)
write('changed-files.json',[{'path':e['path'],'before_sha256':old.get(e['path'],{}).get('sha256'),'after_sha256':e['sha256']} for e in candidate if old.get(e['path'],{}).get('sha256')!=e['sha256']])
# Bind final bytes as well as hashes, for a cold retest without restoring sources.
for e in candidate:
    source=Path(e['path']); destination=ROOT/'candidate-snapshot'/source.relative_to(PACKAGE)
    destination.parent.mkdir(parents=True,exist_ok=True)
    if destination.exists(): assert sha(destination)==e['sha256']
    else: shutil.copyfile(source,destination)

assert sha(OLD/'handoff-manifest.json') == 'b40d23c3f5751881ca563bbd47c8ce82330420aed3e0e273c13f67f54017daf6'
inputs=[{'role':'user-pinned-handoff',**identity(OLD/'handoff-manifest.json')}]
for prop,e in read(OLD/'handoff-manifest.json').items():
    p=Path(e['actual_path']); actual=sha(p)
    inputs.append({'role':prop,**identity(p),'expected_sha256':e['sha256'],'matches':actual==e['sha256']})
for e in read(OLD/'boundary-after.json'):
    p=Path(e['path']);inputs.append({'role':'boundary',**identity(p),'expected_sha256':e['expected'],'matches':sha(p)==e['expected']})
for p in [WORK/'.agents/skills/dev/SKILL.md',*sorted((WORK/'.agents/skills/dev/references').glob('*.md'))]:
    inputs.append({'role':'dev-guidance',**identity(p)})
assert all(e.get('matches',True) for e in inputs)
write('input-readback.json',inputs)
contract=[]
for name in ['delivery-manifest.json','schema-manifest.json']:
    for e in read(WORK/'docs/plan/framework-worker-contract/20260915T151300Z'/name):
        p=WORK/e['path'];contract.append({**e,'actual_sha256':sha(p),'matches':sha(p)==e['sha256']})
assert all(e['matches'] for e in contract)
write('contract-readback-final.json',contract)

inventory = read(OLD/'test-inventory.json')
for name in re.findall(r'#\[test\]\s*fn (\w+)',(PACKAGE/'tests/remediation.rs').read_text()):
    inventory.append({'file':str(PACKAGE/'tests/remediation.rs'),'name':name,'category':'remediation','level':'integration/API'})
write('test-inventory.json',inventory)
metrics={}
for label in ['01-tests','04-coverage']:
    receipt=read(GREEN/label/'receipt.json');assert receipt['exit_code']==0
    text=(GREEN/label/'stdout.txt').read_text(encoding='utf-8')
    outcomes=dict(re.findall(r'^test (\w+) \.\.\. (\w+)$',text,re.M))
    assert len(outcomes)==len(inventory),(label,len(outcomes),len(inventory))
    groups={}
    for kind in ['mandatory','supplemental','remediation']:
        names=[e['name'] for e in inventory if e['category']==kind]
        groups[kind]={'passed':sum(outcomes.get(n)=='ok' for n in names),'required':len(names),'results':{n:outcomes.get(n,'NOT_RUN') for n in names}}
    units=[e['name'] for e in inventory if e['level']=='unit']
    metrics[label]={'groups':groups,'unit_passed':sum(outcomes.get(n)=='ok' for n in units),'unit_required':len(units),'receipt':str(GREEN/label/'receipt.json')}
coverage=read(GREEN/'coverage.json')
files=[]
for data in coverage['data']:
    for f in data['files']:
        p=Path(f['filename'])
        if p.is_relative_to(PACKAGE/'src'):
            files.append({'path':str(p),'sha256':sha(p),'lines':f['summary']['lines'],'branches':f['summary']['branches']})
covered=sum(f['lines']['covered'] for f in files);total=sum(f['lines']['count'] for f in files)
metrics['coverage']={'covered':covered,'total':total,'percent':100*covered/total,'files':files,'denominator':'all executable src lines; no runtime exclusions','branch_status':'NOT_RUN: installed stable collector labels branch coverage unstable'}
results=[read(p) for p in sorted((GREEN/'independent-attempts').glob('*/result.json'))]
write('copied-iq-results.json',results)
iq={}
for n in range(1,6):
    selected=[e for e in results if Path(e['cwd']).name.startswith(f'IQ-{n:02d}')]
    iq[f'IQ-{n:02d}']={'passed':sum(e['pass'] for e in selected),'required':len(selected),'raw_group_pass':all(e['pass'] for e in selected)}
iq['IQ-06']={'status':'PASS within developer review scope','evidence':'ownership-review.md and copied IQ-03 held-handle results'}
passed=20+sum(v['raw_group_pass'] for k,v in iq.items() if k!='IQ-06')+1
metrics['original_26_group_raw']={'passed':passed,'required':26,'percent':100*passed/26,'groups':iq,'caveat':'IQ-02 raw FAIL retained: timeout returns contract exit 6; helper expected 4. No independent closure or raw result rewrite.'}
write('metrics.json',metrics)
bins=[]
for directory in [GREEN/'target/debug',GREEN/'independent-target/debug',GREEN/'target/llvm-cov-target/debug']:
    if directory.exists():
        for p in sorted(directory.glob('*.exe')): bins.append(identity(p))
        for p in sorted((directory/'deps').glob('*.exe')): bins.append(identity(p))
write('build-identities.json',bins)
profiles=[identity(p) for p in sorted((GREEN/'target').rglob('*')) if p.is_file() and p.suffix in ('.profraw','.profdata')]
write('raw-profile-identities.json',profiles)
write('artifact-identities.json',[identity(GREEN/'coverage.json'),identity(GREEN/'selected-manifest.json')])
receipts=[]
for root in [ROOT,GREEN]:
    for p in sorted(root.glob('*/receipt.json')):
        receipts.append({'record_path':str(p),'record_sha256':sha(p),'host_record':str(ROOT/'host.json'),**read(p)})
    for p in sorted(root.glob('independent-attempts/*/result.json')):
        receipts.append({'record_path':str(p),'record_sha256':sha(p),'host_record':str(ROOT/'host.json'),'stage':'red' if root==ROOT else 'green/developer-regression',**read(p)})
(ROOT/'execution-records.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in receipts),encoding='utf-8')
print(json.dumps({'candidate_sha256':sha(ROOT/'candidate-manifest.json'),'changed':len(read(ROOT/'changed-files.json')),'coverage':metrics['coverage'],'raw_scope':metrics['original_26_group_raw'],'binaries':len(bins),'profiles':len(profiles)},indent=2))
