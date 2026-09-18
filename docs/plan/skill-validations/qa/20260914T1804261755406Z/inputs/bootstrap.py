"""Capture selected custody and pin policy before observations; evidence only."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys

RUN = Path(__file__).resolve().parents[1]
ROOT = RUN.parents[4]
VALIDATOR = ROOT / '.agents/skills/skill-validator'
AUTHOR = ROOT / 'docs/plan/skill-authorings/qa/20260914T1748018341005Z'
sys.path.insert(0, str(VALIDATOR / 'scripts'))
import observe

def write(path, value):
    p = RUN / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def ref(path):
    p = RUN / path
    return {'path': path, 'sha256': observe.sha256(p.read_bytes())}

def command(name, args):
    start = dt.datetime.now(dt.timezone.utc).isoformat()
    p = subprocess.run(args, cwd=ROOT, capture_output=True, timeout=120)
    (RUN / 'observations').mkdir(exist_ok=True)
    (RUN / f'observations/{name}.stdout').write_bytes(p.stdout)
    (RUN / f'observations/{name}.stderr').write_bytes(p.stderr)
    write(f'observations/{name}.receipt.json', {'command':args,'cwd':str(ROOT),'started':start,'ended':dt.datetime.now(dt.timezone.utc).isoformat(),'exit_code':p.returncode,'timeout_seconds':120})
    print(name, p.returncode, p.stdout.decode('utf-8', errors='replace')[:300])
    return p

def main():
    captures = []
    selected = [(ROOT/'docs/specs/qa-skill-spec.md','inputs/qa-skill-spec.md'), (ROOT/'AGENTS.md','inputs/AGENTS.md')]
    selected += [(AUTHOR / n, 'inputs/authoring/' + n) for n in ['validation-request.json','authoring-record.json','contract.json','delivered-manifest.json','publication-readback.json','authoring-notes.md','manual-validator-request.md'] if (AUTHOR/n).exists()]
    selected += [(VALIDATOR / n,'inputs/validator/'+n) for n in ['SKILL.md','references/adaptive-validation.md','references/rules.md','references/reporting.md','references/trials.md','references/set-trials.md','references/text-resource-checks.md','references/handoff.md','assets/openai-yaml-guidance.md','assets/rules-snapshot.json','scripts/observe.py','scripts/authoring_intake.py','scripts/adaptive_observe.py','scripts/adaptive_contracts.py','scripts/text_resources.py']]
    checker = Path('C:/Users/bryan/.codex/skills/.system/skill-creator/scripts/quick_validate.py')
    selected.append((checker,'inputs/checker/quick_validate.py'))
    # Follow only explicit custody references, never recursively scan authoring directories.
    seen = set()
    while selected:
        source, dest = selected.pop(0)
        source = observe.safe_path(source)
        if str(source) in seen:
            continue
        seen.add(str(source))
        raw = observe.read_stable(source)
        out = RUN/dest
        out.parent.mkdir(parents=True,exist_ok=True)
        out.write_bytes(raw)
        captures.append({'original_path':str(source),**ref(dest)})
        if source.suffix == '.json' and AUTHOR in source.parents:
            def walk(v):
                if isinstance(v,dict):
                    if set(v) == {'path','sha256'}:
                        p = observe.safe_path(v['path'])
                        if observe.sha256(observe.read_stable(p)) != v['sha256']:
                            raise ValueError('Stale custody reference '+str(p))
                        selected.append((p,'inputs/custody/'+observe.sha256(str(p).encode())[:12]+'-'+p.name))
                    else:
                        for x in v.values(): walk(x)
                elif isinstance(v,list):
                    for x in v: walk(x)
            walk(observe.strict_json(raw))
    write('inputs/capture-index.json', captures)
    assert observe.sha256((RUN/'inputs/qa-skill-spec.md').read_bytes()) == '6378025552bbbc4bfdaff8f1d3d14443cfacf44986f51f98845797b116b53e03'
    import yaml
    config = Path('C:/Users/bryan/.codex/config.toml')
    config_raw = config.read_text(encoding='utf-8') if config.exists() else ''
    # Record only configuration key names relevant to native effects; never values or credentials.
    config_keys = [line.split('=')[0].strip() for line in config_raw.splitlines() if '=' in line and any(x in line.split('=')[0].lower() for x in ['hook','model','sandbox','approval'])]
    write('environment.json', {'os':platform.platform(),'python':sys.version,'python_executable':sys.executable,'pyyaml':yaml.__version__,'shell':'PowerShell','codex':shutil.which('codex'),'config_effect_key_names':config_keys,'git_present':(ROOT/'.git').exists(),'authorization':'Validate only selected qa package; synthetic trial/evidence writes; no repair/install/dev/production QA.','task_runner':'Installed Codex CLI; native capability subject to first retained trial. Collaboration runner available for description-only routing per trials.md.','scope':'Windows-native package assessment; other platform behavior is a separate observation.','checker':str(checker),'checker_sha256':observe.sha256(checker.read_bytes())})
    av = (RUN/'inputs/validator/references/adaptive-validation.md').read_text(encoding='utf-8')
    import re
    rules = []
    for line in av.splitlines():
        if not line.startswith('| AV-'): continue
        cells = [v.strip() for v in line.strip('|').split('|')]
        rid = cells[0]
        adaptive = rid.startswith('AV-A')
        rules.append({'rule_id':rid,'revision':'2026-09-12','title':cells[-1], 'source_refs':[{**ref('inputs/validator/references/adaptive-validation.md'),'source_id':'av','locator':rid}], 'authority_class':'project_policy','applicability':'not_applicable' if adaptive else 'applicable','method':'semantic','expected_observation':cells[-1],'required':True,'limitation':'Ordinary standalone skill; adaptive/set rules do not apply.' if adaptive else 'Semantic adjudication and native trials are separate from helper output.'})
    spec = (RUN/'inputs/qa-skill-spec.md').read_text(encoding='utf-8')
    for match in re.finditer(r'\*\*(QA-\d+) — ([^*]+)\*\*',spec):
        rid,title = match.groups()
        rules.append({'rule_id':rid,'revision':'1.0','title':title,'source_refs':[{**ref('inputs/qa-skill-spec.md'),'source_id':'qa-spec','locator':rid}],'authority_class':'project_policy','applicability':'applicable','method':'semantic','expected_observation':'Conform to the complete '+rid+' clause in the pinned specification.','required':True,'limitation':'Static conformance does not establish behavioral QV scenarios.'})
    write('rule-set.json',{'schema_version':'1','run_id':RUN.name,'target_name':'qa','rules':rules})
    write('sources.json',{'schema_version':'1','run_id':RUN.name,'target_name':'qa','sources':[{'source_id':sid,'original_path':str(path),'retrieved_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'sha256':ref(dest)['sha256'],'snapshot_path':dest,'sections':['complete'],'freshness':'snapshot_only'} for sid,path,dest in [('av',VALIDATOR/'references/adaptive-validation.md','inputs/validator/references/adaptive-validation.md'),('qa-spec',ROOT/'docs/specs/qa-skill-spec.md','inputs/qa-skill-spec.md'),('project',ROOT/'AGENTS.md','inputs/AGENTS.md')]]})
    intake = command('intake',[sys.executable,'-B','-X','utf8',str(VALIDATOR/'scripts/authoring_intake.py'),'--request',str(AUTHOR/'validation-request.json'),'--request-sha256','86c446405103010123b2bf5a0278f6986aaf8e70dab82304d8cc577c18f34bc4'])
    if intake.returncode: raise SystemExit('Rejected handoff; do not proceed as bound assessment')
    command('structure',[sys.executable,'-B','-X','utf8',str(VALIDATOR/'scripts/observe.py'),'structure','--source',str(RUN/'source')])
    command('checker',[sys.executable,'-B','-X','utf8',str(checker),str(RUN/'source')])
    command('adaptive-package',[sys.executable,'-B','-X','utf8',str(VALIDATOR/'scripts/adaptive_observe.py'),'package','--source',str(RUN/'source')])
    command('codex-version',[shutil.which('codex'),'--version'])
    command('codex-help',[shutil.which('codex'),'exec','--help'])

if __name__ == '__main__': main()
