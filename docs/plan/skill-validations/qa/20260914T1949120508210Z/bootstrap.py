"""Retain selected validation inputs and read-only tool observations."""
import datetime
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
sys.path.insert(0, str(VALIDATOR / 'scripts'))
import observe

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

def run(name, args, timeout=120):
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    result = subprocess.run(args, cwd=PROJECT, capture_output=True, timeout=timeout)
    folder = ROOT / 'observations'
    folder.mkdir(exist_ok=True)
    (folder / (name + '.stdout')).write_bytes(result.stdout)
    (folder / (name + '.stderr')).write_bytes(result.stderr)
    write(folder / (name + '.receipt.json'), dict(command=args,cwd=str(PROJECT),started=start,ended=datetime.datetime.now(datetime.timezone.utc).isoformat(),exit_code=result.returncode,timeout_seconds=timeout))
    print(name, result.returncode, result.stdout.decode('utf-8',errors='replace')[:350])
    return result

if __name__ == '__main__':
    assert PROJECT == Path('C:/Projects/DevForgeAI')
    request = PROJECT / 'docs/plan/skill-authorings/qa/20260914T193851Z/validation-request.json'
    packet = json.loads(request.read_bytes())
    author = json.loads(Path(packet['authoring_record']['path']).read_bytes())
    refs = [dict(path=str(request),sha256='40ac8bd62b6e0d8b1216acef54d487f38e5708655dc7cfe5ca5dde6cac3aaa2f'),packet['target_manifest'],packet['authoring_record'],author['contract'],*packet['specification_refs']]
    rows = []
    for i, ref in enumerate(refs):
        original = observe.safe_path(ref['path'])
        raw = observe.read_stable(original)
        assert hashlib.sha256(raw).hexdigest() == ref['sha256'], str(original)
        dest = ROOT / 'inputs' / (f'{i:02d}-' + original.name)
        dest.parent.mkdir(exist_ok=True)
        dest.write_bytes(raw)
        rows.append(dict(original_path=str(original),snapshot_path=dest.relative_to(ROOT).as_posix(),sha256=ref['sha256']))
    write(ROOT/'input-bindings.json', rows)
    for rel in ['SKILL.md','references/adaptive-validation.md','references/rules.md','assets/rules-snapshot.json','scripts/observe.py','scripts/authoring_intake.py','scripts/adaptive_observe.py','scripts/adaptive_contracts.py','scripts/text_resources.py']:
        dest = ROOT / 'inputs/validator' / rel
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes((VALIDATOR/rel).read_bytes())
    checker = Path('C:/Users/bryan/.codex/skills/.system/skill-creator/scripts/quick_validate.py')
    (ROOT/'inputs/quick_validate.py').write_bytes(checker.read_bytes())
    write(ROOT/'preservation-before.json', {'operational_qa':observe.make_manifest(PROJECT/'.agents/skills/qa'),'validator':observe.make_manifest(VALIDATOR)})
    write(ROOT/'environment.json',dict(os=platform.platform(),python=sys.version,python_executable=sys.executable,shell='PowerShell',git_metadata=(PROJECT/'.git').exists(),execution_boundary='Windows workspace sandbox; child containment subject to host; no bypass',authorization='Independent development qa validation; synthetic local trials and fresh evidence only; no source repair, installation, external writes or dependency installation'))
    run('authoring-intake',[sys.executable,'-B','-X','utf8',str(VALIDATOR/'scripts/authoring_intake.py'),'--request',str(request),'--request-sha256',refs[0]['sha256']])
    run('cli-version',[shutil.which('codex'),'--version'])
    run('cli-help',[shutil.which('codex'),'exec','--help'])
