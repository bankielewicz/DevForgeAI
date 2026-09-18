import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
RUN=Path(__file__).resolve().parent
ROOT=RUN.parents[3]
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'src/agents/skills/skill-builder/scripts'))
import authoring as a
tests=json.loads((RUN/'checks-005-delivered/result.json').read_text())
assert tests['successful'] and tests['tests']==202 and tests['skipped']==0
supplement=json.loads((RUN/'checks-006-authoring-inputs/result.json').read_text())
assert supplement['successful'] and supplement['tests']==28
structural=json.loads((RUN/'structural-003-delivered/result.json').read_text())
assert all(r['exit_code']==0 for r in structural)
scope=json.loads((RUN/'scope-readback.json').read_text())
assert not scope['unauthorized'] and scope['excluded_before']==scope['excluded_after']
routing=RUN/'independent-trials/routing'
expected=json.loads((routing/'expectations.json').read_text())
observed=json.loads((routing/'observed.json').read_text())
assert expected==observed
raw_before=json.loads((RUN/'workspace-before.json').read_text())['files']
evidence={'full_regression':tests,'supplemental_authoring_input_capture':supplement,'structural':[{'package':r['package'],'check':r['check'],'exit_code':r['exit_code']} for r in structural],'routing':{'matched':len(expected),'total':len(expected),'native_activation':'NOT_RUN'},'scope':{'changed_files':len(scope['changed']),'unauthorized':scope['unauthorized'],'excluded_boundaries':scope['excluded_after'],'inventoried_before_files':len(raw_before)},'targets':{},'input_readback':{},'trials':{}}
for source in [ROOT/'docs/plan/skill-builder-authoring-enhancement-spec.md',*(ROOT/'docs/codex').glob('*.md')]:
    relative=source.relative_to(ROOT).as_posix()
    actual=a.digest(source.read_bytes())
    assert actual==raw_before[relative]['sha256']
    evidence['input_readback'][relative]=actual
creator=Path('C:/Users/bryan/.codex/skills/.system/skill-creator')
for rel in ('SKILL.md','scripts/init_skill.py','scripts/generate_openai_yaml.py','scripts/quick_validate.py','license.txt','references/openai_yaml.md'):
    assert (creator/rel).read_bytes()==(RUN/'inputs/skill-creator'/rel).read_bytes()
    evidence['input_readback']['installed-skill-creator/'+rel]=a.digest((creator/rel).read_bytes())
for name in ('skill-builder','skill-validator'):
    target=ROOT/'src/agents/skills'/name
    current=a.files(target)
    assert current==a.files(RUN/'candidate'/name)
    assert current==a.files(RUN/'checks-005-delivered/input-packages'/name)
    assert current==a.files(RUN/'assessments'/name/'source')
    evidence['targets'][name]=a.manifest(current)
    packet=RUN/'authoring'/name/'validation-request.json'
    cmd=[sys.executable,'-B','-X','utf8',str(ROOT/'src/agents/skills/skill-validator/scripts/authoring_intake.py'),'--request',str(packet),'--request-sha256',a.digest(packet.read_bytes())]
    stem=RUN/(name+'-delivered-intake')
    a.save(stem.with_suffix('.plan.json'),{'command':cmd,'executor':'operational-validator-owned deterministic invocation of enhanced development intake','expected':'BOUND exact delivered packet; no quality verdict from intake','timeout_seconds':120,'inputs':{'request':str(packet),'request_sha256':a.digest(packet.read_bytes()),'package_digest':a.manifest(current)['package_digest']}})
    p=subprocess.run(cmd,capture_output=True,timeout=120)
    stem.with_suffix('.stdout.json').write_bytes(p.stdout)
    stem.with_suffix('.stderr.txt').write_bytes(p.stderr)
    assert p.returncode==0,p.stderr
    evidence['targets'][name]['intake']=json.loads(p.stdout)['status']
for case in ('conversation','observed-edit','material-ambiguity','import-script','untested-revision','enhanced-validator'):
    folder=RUN/'independent-trials'/case
    response=folder/'response.md'
    trace=folder/'trace.md'
    assert response.exists() and trace.exists()
    entry={'response_sha256':a.digest(response.read_bytes()),'trace_sha256':a.digest(trace.read_bytes()),'response_locator':str(response),'trace_locator':str(trace)}
    if (folder/'skill-builder').exists():
        snapshot=a.files(folder/'skill-builder')
        current=a.files(ROOT/'src/agents/skills/skill-builder')
        entry['input_package_digest']=a.manifest(snapshot)['package_digest']
        entry['differences_from_delivered']=sorted(p for p in set(snapshot)|set(current) if snapshot.get(p)!=current.get(p))
    evidence['trials'][case]=entry
old=RUN/'independent-trials/observed-edit/input-target'
now=RUN/'independent-trials/observed-edit/project/Development skills/daily-brief'
assert (old/'references/series.md').read_bytes()==(now/'references/series.md').read_bytes()
import yaml
original=yaml.safe_load((old/'agents/openai.yaml').read_text())
edited=yaml.safe_load((now/'agents/openai.yaml').read_text())
expected_ui=json.loads(json.dumps(original));expected_ui['interface']['display_name']='Daily Notes Brief'
assert edited==expected_ui
importcase=RUN/'independent-trials/import-script'
assert (importcase/'source/decimal-ledger/scripts/total.py').read_bytes()==(importcase/'project/skills under review/decimal-ledger/scripts/total.py').read_bytes()
assert 'graders.py' not in [p.name for p in (ROOT/'src/agents/skills/skill-builder/scripts').iterdir()]
assert not (ROOT/'src/agents/skills/skill-builder/tests').exists()
assert not (ROOT/'src/agents/skills/skill-builder/evals').exists()
a.save(RUN/'verification-summary.json',evidence)
print(json.dumps({'full_tests':tests,'structural':'4/4','routing':'14/14','target_digests':{k:v['package_digest'] for k,v in evidence['targets'].items()},'unauthorized_changes':len(scope['unauthorized']),'excluded_boundaries':len(scope['excluded_after'])}))
