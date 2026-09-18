"""Read-only package capture for updated validator/builder compatibility."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[3]
STAMP = RUN.name
VALIDATOR = ROOT / '.agents/skills/skill-validator'
sys.path.insert(0, str(VALIDATOR / 'scripts'))
import observe

def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)

targets = {'validator-loaded':VALIDATOR, 'validator-development':ROOT/'src/agents/skills/skill-validator', 'builder-loaded':ROOT/'.agents/skills/skill-builder', 'builder-development':ROOT/'src/agents/skills/skill-builder'}
manifests = {}
for name, path in targets.items():
    manifests[name] = observe.make_manifest(observe.safe_path(path))
    save(RUN / 'inputs' / (name + '-manifest.json'), manifests[name])
    print(name, manifests[name]['package_digest'], len(manifests[name]['files']))
for name, source in [('skill-validator',VALIDATOR), ('skill-builder',targets['builder-development'])]:
    output = ROOT/'docs/plan/skill-validations'/name/STAMP
    command = [sys.executable,'-B','-X','utf8',str(VALIDATOR/'scripts/observe.py'),'snapshot','--source',str(source),'--output',str(output)]
    result = subprocess.run(command,capture_output=True,timeout=120)
    save(RUN/'inputs'/(name+'-snapshot-command.json'),{'command':command,'exit_code':result.returncode})
    (RUN/'inputs'/(name+'-snapshot-stdout.json')).write_bytes(result.stdout)
    assert result.returncode == 0, result.stderr
for name in ['skill-builder-adaptive-enhancement-spec.md','skill-validator-adaptive-enhancement-spec.md']:
    source = ROOT/'docs/plan'/name
    data = source.read_bytes()
    (RUN/'inputs'/name).write_bytes(data)
    print(name, hashlib.sha256(data).hexdigest())
import yaml
save(RUN/'environment.json',{'schema_version':'1','os':platform.platform(),'python':sys.version,'executable':sys.executable,'pyyaml':yaml.__version__,'shell':'PowerShell','started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'boundary':'Read-only selected packages; fresh disposable test roots only. No installation or repair.'})
rules = (VALIDATOR/'references/adaptive-validation.md').read_bytes()
(RUN/'inputs/adaptive-validation.md').write_bytes(rules)
(RUN/'inputs/rules-snapshot.json').write_bytes((VALIDATOR/'assets/rules-snapshot.json').read_bytes())
save(RUN/'plan.json',{'schema_version':'1','run_id':STAMP,'scope':'Updated validator compatibility with updated builder; self-assessment plus independent differential tests. No package changes.', 'selected_rules_sha256':hashlib.sha256(rules).hexdigest(),'cases':[
{'id':'C01','oracle':'Shared schemas have identical declared contracts; positive and negative records agree.'},
{'id':'C02','oracle':'Changed core bytes with equal requirements allow review_updates PROPOSED and reject NO_CHANGE.'},
{'id':'C03','oracle':'Existing core with explicit Markdown requirement inventory is consumed without a new core resource requirement.'},
{'id':'C04','oracle':'Delivered role and parent lineage must agree with selected proposal.'},
{'id':'C05','oracle':'Actual authored member manual packet is consumed; stale target rejects.'},
{'id':'C06','oracle':'Full set and eligible subset preserve exact members, dependencies and omissions.'},
{'id':'C07','oracle':'Required failure dominates incomplete; counts include unknown exactly once; schema families remain distinct.'},
{'id':'C08','oracle':'Cold updated validator reaches a truthful bounded intake/report from a supplied raw handoff, no repairs.'}],
'timeout_seconds':120,'native_policy':'Existing auth/model, supported flags, workspace-write; retain timeouts, no bypass.', 'scope_note':'This is compatibility validation, not rerunning builder authoring campaigns or closing every prior builder-native gap.'})
