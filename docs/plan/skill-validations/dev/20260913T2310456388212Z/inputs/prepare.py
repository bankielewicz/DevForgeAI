"""Prepare bounded, run-local validation inputs and retain command receipts."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[4]
VALIDATOR = PROJECT / '.agents/skills/skill-validator'
AUTHOR = PROJECT / 'docs/plan/skill-authorings/dev/20260913T2114525120037Z'
EXPECTED = '7ebe47919c03b654614dcfa5ff288c0e58a3870615582e798780c74e8cfa15d6'
sys.path.insert(0, str(VALIDATOR / 'scripts'))
import observe

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + '\n' if not isinstance(value, str) else value)

def ref(path):
    return {'path':path.relative_to(ROOT).as_posix(), 'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}

def run(name, args):
    start = dt.datetime.now(dt.timezone.utc).isoformat()
    result = subprocess.run(args, cwd=PROJECT, capture_output=True, timeout=120)
    folder = ROOT / 'observations'
    folder.mkdir(exist_ok=True)
    (folder / (name+'.stdout')).write_bytes(result.stdout)
    (folder / (name+'.stderr')).write_bytes(result.stderr)
    receipt = {'command':args,'cwd':str(PROJECT),'start':start,'end':dt.datetime.now(dt.timezone.utc).isoformat(),'exit_code':result.returncode,'timeout_seconds':120,'stdout':ref(folder/(name+'.stdout')),'stderr':ref(folder/(name+'.stderr'))}
    write(folder/(name+'.receipt.json'),receipt)
    print(name, result.returncode, result.stdout.decode('utf-8',errors='replace')[:900])
    return result

if __name__ == '__main__':
    inputs = ROOT / 'inputs'
    inputs.mkdir(exist_ok=True)
    paths = [AUTHOR/'validation-request.json', AUTHOR/'manual-validator-prompt.md', AUTHOR/'validation-obligations.md', AUTHOR/'authoring-record.json', AUTHOR/'contract.json', AUTHOR/'baseline-manifest.json', PROJECT/'docs/specs/dev-skill-spec.md', PROJECT/'AGENTS.md']
    paths += [VALIDATOR/'SKILL.md', VALIDATOR/'references/adaptive-validation.md', VALIDATOR/'references/rules.md', VALIDATOR/'assets/rules-snapshot.json']
    identity = []
    for i,path in enumerate(paths):
        data = observe.read_stable(observe.safe_path(path))
        dest = inputs / (f'{i:02d}-'+path.name)
        dest.write_bytes(data)
        identity.append({'original_path':str(path),'snapshot':ref(dest)})
    write(inputs/'input-index.json',identity)
    result = run('authoring-intake',[sys.executable,'-B','-X','utf8',str(VALIDATOR/'scripts/authoring_intake.py'),'--request',str(AUTHOR/'validation-request.json'),'--request-sha256',EXPECTED])
    if result.returncode:
        raise SystemExit('Stale intake retained; do not use packet as current readiness.')
    write(ROOT/'capabilities.json',{'platform':platform.platform(),'python':sys.version,'python_executable':sys.executable,'shell':'PowerShell','filesystem':'Windows C: native','codex':shutil.which('codex'),'network_trials':'NOT_AUTHORIZED by selected packet; pending separate current authorization','allowed_effects':['fresh validation evidence','disposable synthetic fixtures'],'prohibited_effects':['target repair','operational changes','plugin','example application','external writes','credentials'],'coverage_denominator':'No first-party executable framework code changed or selected; framework line/branch coverage NOT_RUN, not a passing percentage.'})
    run('python-dependencies',[sys.executable,'-B','-X','utf8','-c','import sys,yaml,importlib.util; print(sys.version); print("PyYAML",yaml.__version__); print("tiktoken",bool(importlib.util.find_spec("tiktoken"))); print("coverage",bool(importlib.util.find_spec("coverage")))'])
    run('codex-version',[shutil.which('codex'),'--version'])
    run('codex-exec-help',[shutil.which('codex'),'exec','--help'])
    rules = []
    spec = (inputs/'06-dev-skill-spec.md').read_text(encoding='utf-8')
    import re
    for match in re.finditer(r'\*\*(DEV-\d{3}) — ([^*]+)\*\*(.*?)(?=\n\*\*DEV-|\n## |\Z)',spec,re.S):
        rules.append({'rule_id':match[1],'revision':'1','title':match[2],'source_refs':[dict(ref(inputs/'06-dev-skill-spec.md'),source_id='dev-spec',locator=match[1])],'authority_class':'project_policy','applicability':'applicable','method':'semantic','expected_observation':match[0],'required':True,'limitation':'Static contract assessment separated from native behavior.'})
    av = (inputs/'09-adaptive-validation.md').read_text(encoding='utf-8')
    for line in av.splitlines():
        if not line.startswith('| AV-'): continue
        parts = [p.strip() for p in line.strip('|').split('|')]
        ident, method, expected = parts[:3]
        na = ident.startswith('AV-A') or ident=='AV-F04'
        rules.append({'rule_id':ident,'revision':'2026-09-12','title':ident,'source_refs':[dict(ref(inputs/'09-adaptive-validation.md'),source_id='av-catalog',locator=ident)],'authority_class':'project_policy','applicability':'not_applicable' if na else 'applicable','method':'behavioral' if ident in ('AV-W01','AV-W02') else 'semantic','expected_observation':expected,'required':True,'limitation':'Ordinary standalone skill; no adaptive contract, set, or optional host metadata.' if na else 'Deterministic observations need separate semantic adjudication.'})
    assert len([r for r in rules if r['rule_id'].startswith('DEV-')]) == 26
    assert len([r for r in rules if r['rule_id'].startswith('AV-')]) == 29
    write(ROOT/'rule-set.json',{'schema_version':'1','run_id':ROOT.name,'target_name':'dev','rules':rules})
    write(ROOT/'sources.json',{'schema_version':'1','run_id':ROOT.name,'target_name':'dev','sources':[{'source_id':f'input-{i}','original_path':row['original_path'],'retrieved_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'sha256':row['snapshot']['sha256'],'snapshot_path':row['snapshot']['path'],'sections':'complete retained input','freshness':'current_local'} for i,row in enumerate(identity)]})
    run('structure',[sys.executable,'-B','-X','utf8',str(VALIDATOR/'scripts/observe.py'),'structure','--source',str(ROOT/'source')])
    run('creator-check',[sys.executable,'-B','-X','utf8','C:/Users/bryan/.codex/skills/.system/skill-creator/scripts/quick_validate.py',str(ROOT/'source')])
    run('package',[sys.executable,'-B','-X','utf8',str(VALIDATOR/'scripts/adaptive_observe.py'),'package','--source',str(ROOT/'source'),'--tokenizer','tiktoken','--encoding','cl100k_base'])
