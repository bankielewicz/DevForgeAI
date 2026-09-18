import datetime as dt
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
RUN=Path(__file__).resolve().parent
ROOT=RUN.parents[3]
OUT=RUN/'assessments'
OUT.mkdir()
CMD=RUN/'assessment-commands'
CMD.mkdir()
observer=ROOT/'.agents/skills/skill-validator/scripts/observe.py'
def command(label,args):
    argv=[sys.executable,'-B','-X','utf8',str(observer),*args]
    (CMD/(label+'-plan.json')).write_text(json.dumps({'command':argv,'cwd':str(ROOT),'executor':'primary author following preserved operational skill-validator','timeout_seconds':120,'expected':'Complete snapshot or matching readback of selected delivered bytes'},indent=2))
    p=subprocess.run(argv,capture_output=True,timeout=120)
    (CMD/(label+'-stdout.json')).write_bytes(p.stdout)
    (CMD/(label+'-stderr.txt')).write_bytes(p.stderr)
    (CMD/(label+'-exit.json')).write_text(json.dumps({'exit_code':p.returncode}))
    if p.returncode: raise RuntimeError(p.stderr.decode())
    return json.loads(p.stdout)
for name in ('skill-builder','skill-validator'):
    out=OUT/name
    target=ROOT/'src/agents/skills'/name
    command(name+'-snapshot',['snapshot','--source',str(target),'--output',str(out)])
    inputs=out/'inputs'; inputs.mkdir()
    for source in ['skill-builder-authoring-enhancement-spec.md','openai-build-skills-live.md','implementation-authorization.txt']:
        shutil.copy2(RUN/'inputs'/source,inputs/source)
    shutil.copytree(RUN/'inputs/operational-validator',inputs/'operational-validator')
    shutil.copytree(RUN/'inputs/skill-creator',inputs/'skill-creator')
    shutil.copy2(RUN/'assessment-plans'/(name+'.json'),inputs/'assessment-plan.json')
    shutil.copy2(RUN/'authoring'/name/'authoring-record.json',inputs/'authoring-record-raw.json')
    shutil.copy2(RUN/'authoring'/name/'validation-request.json',inputs/'validation-request-raw.json')
    sources=[]
    for ident,relative,original,fresh in [
      ('spec','inputs/skill-builder-authoring-enhancement-spec.md',str(ROOT/'docs/plan/skill-builder-authoring-enhancement-spec.md'),'digest_verified'),
      ('creator','inputs/skill-creator/SKILL.md','C:/Users/bryan/.codex/skills/.system/skill-creator/SKILL.md','installed_snapshot'),
      ('openai-skills','inputs/openai-build-skills-live.md','https://learn.chatgpt.com/docs/build-skills','live_verified')]:
        sources.append({'source_id':ident,'original_path':original,'retrieved_at_utc':None,'sha256':hashlib.sha256((out/relative).read_bytes()).hexdigest(),'snapshot_path':relative,'sections':['Selected authoring and format guidance'],'freshness':fresh})
    (out/'sources.json').write_text(json.dumps({'schema_version':'1','run_id':name+'-delivered','target_name':name,'sources':sources},indent=2))
    plan=json.loads((inputs/'assessment-plan.json').read_text())
    for rule in plan['rules']:
        source=sources[2] if rule['rule_id']=='FORMAT' else sources[0]
        rule['source_refs']=[{'path':source['snapshot_path'],'sha256':source['sha256'],'source_id':source['source_id'],'locator':'Required SKILL.md and optional resources' if rule['rule_id']=='FORMAT' else 'Section 5 acceptance scenarios; Sections 2-4 authoring and migration'}]
    (out/'rule-set.json').write_text(json.dumps({'schema_version':'1','run_id':name+'-delivered','target_name':name,'rules':plan['rules']},indent=2))
    result=command(name+'-initial-readback',['readback','--source',str(target),'--manifest',str(out/'source-manifest.json')])
    (out/'source-after-manifest.json').write_text(json.dumps(result['manifest'],indent=2))
print('Captured delivered packages, retained operational validator, and pinned final assessment rules.')
