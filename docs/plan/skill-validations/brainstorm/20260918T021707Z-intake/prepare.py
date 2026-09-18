"""Capture the selected validation inputs without modifying either skill."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys

ROOT = Path('C:/Projects/DevForgeAI')
RUN = ROOT / 'docs/plan/skill-validations/brainstorm/20260918T021707Z'
VAL = ROOT / '.agents/skills/skill-validator'
REQUEST = ROOT / 'docs/plan/skill-authorings/brainstorm/20260918T020654Z/validation-request.json'
TARGET = ROOT / 'src/agents/skills/brainstorm'
sys.path.insert(0, str(VAL / 'scripts'))
import observe

def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode() if not isinstance(value, bytes) else value
    with path.open('xb') as stream:
        stream.write(data)

def command(name, argv, timeout=120):
    start = dt.datetime.now(dt.timezone.utc).isoformat()
    result = subprocess.run(argv, cwd=ROOT, capture_output=True, timeout=timeout)
    save(RUN / 'observations' / (name + '.stdout.txt'), result.stdout)
    save(RUN / 'observations' / (name + '.stderr.txt'), result.stderr)
    save(RUN / 'observations' / (name + '.command.json'), dict(argv=argv,cwd=str(ROOT),started_at=start,ended_at=dt.datetime.now(dt.timezone.utc).isoformat(),exit_code=result.returncode,timeout_seconds=timeout))
    print(name, result.returncode, result.stdout.decode('utf-8',errors='replace')[:900])
    return result

def main():
    argv=[sys.executable,'-B','-X','utf8',str(VAL/'scripts/observe.py'),'snapshot','--source',str(TARGET),'--output',str(RUN)]
    start=dt.datetime.now(dt.timezone.utc).isoformat()
    result=subprocess.run(argv,cwd=ROOT,capture_output=True,timeout=120)
    if not RUN.exists():
        raise RuntimeError(result.stderr.decode())
    save(RUN/'observations/snapshot.stdout.txt',result.stdout)
    save(RUN/'observations/snapshot.stderr.txt',result.stderr)
    save(RUN/'observations/snapshot.command.json',dict(argv=argv,cwd=str(ROOT),started_at=start,exit_code=result.returncode,timeout_seconds=120))
    if result.returncode:
        raise RuntimeError('Incomplete snapshot retained')
    save(RUN/'inputs/validation-request.json',REQUEST.read_bytes())
    # Capture dependencies as data; imports still use the selected operational checker.
    refs=[]
    request=json.loads(REQUEST.read_bytes())
    for item in request['specification_refs']+[request['authoring_record'],request['target_manifest']]:
        path=observe.safe_path(item['path']); data=observe.read_stable(path)
        assert observe.sha256(data)==item['sha256'], str(path)
        relative=path.relative_to(ROOT).as_posix()
        saved=RUN/'inputs/project'/relative
        save(saved,data)
        refs.append(dict(original_path=str(path),snapshot_path=saved.relative_to(RUN).as_posix(),sha256=item['sha256']))
    for directory in ('scripts','references','assets','schemas'):
        base=VAL/directory
        files,excluded=observe.inventory(base)
        assert not excluded, excluded
        for rel,path,info in files:
            save(RUN/'inputs/validator'/directory/rel,observe.read_stable(path,info))
    save(RUN/'inputs/validator/SKILL.md',(VAL/'SKILL.md').read_bytes())
    checker=Path('C:/Users/bryan/.codex/skills/.system/skill-creator/scripts/quick_validate.py')
    save(RUN/'inputs/checker/quick_validate.py',checker.read_bytes())
    save(RUN/'inputs/input-bindings.json',refs)
    import yaml
    save(RUN/'environment.json',dict(cwd=str(ROOT),os=platform.platform(),python=sys.version,python_path=sys.executable,pyyaml=yaml.__version__,shell='PowerShell 7 (host)',codex=shutil.which('codex'),git_state='NOT_AVAILABLE: git reports not a repository',target=str(TARGET),required_platforms=['Windows/PowerShell'],package_executable_lines=0,package_coverage='NOT_APPLICABLE',utility_timeout_seconds=120,native_timeout_seconds=600,authorization='Independent disposable evaluation only; no source repair, real operational promotion, install, startup edits, production data or framework acceptance.',capture_limits=dict(files=2000,bytes=33554432),exclusions=[]))
    command('authoring-intake',[sys.executable,'-B','-X','utf8',str(VAL/'scripts/authoring_intake.py'),'--request',str(REQUEST),'--request-sha256','0efea184aa672a004d9c8dc05fc19ee6b3c3cae85c0654794a5be2029a467c6b'])
    command('codex-version',[shutil.which('codex'),'--version'])
    command('codex-help',[shutil.which('codex'),'exec','--help'])
    save(RUN/'inputs/preparation.py',Path(__file__).read_bytes())
    print('RUN',RUN)

if __name__=='__main__':
    main()
