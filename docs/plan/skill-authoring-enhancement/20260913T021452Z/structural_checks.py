import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import datetime as dt
RUN = Path(__file__).resolve().parent
OUT = RUN / sys.argv[1]
OUT.mkdir()
ROOT = RUN.parents[3]
checker = Path('C:/Users/bryan/.codex/skills/.system/skill-creator/scripts/quick_validate.py')
observer = ROOT / '.agents/skills/skill-validator/scripts/observe.py'
source_root = ROOT / 'src/agents/skills' if 'delivered' in sys.argv[2:] else RUN / 'candidate'
for name in ('skill-builder','skill-validator'):
    shutil.copytree(source_root / name, OUT / 'input-packages' / name)
shutil.copy2(checker, OUT / 'installed-quick-validate.py')
shutil.copy2(observer, OUT / 'operational-observe.py')
observations = []
for name in ('skill-builder','skill-validator'):
    source = source_root / name
    for label, tool in (('structure', observer),('skill-creator', checker)):
        command = [sys.executable,'-B','-X','utf8',str(tool)] + (['structure','--source',str(source)] if label=='structure' else [str(source)])
        stem = name + '-' + label
        plan = {'command':command,'cwd':str(ROOT),'executor':'operational skill-validator assessment','expected':'No required structural mismatches','input_package':str(source),'tool_sha256':hashlib.sha256(tool.read_bytes()).hexdigest(),'timeout_seconds':120,'started':dt.datetime.now(dt.timezone.utc).isoformat()}
        (OUT / (stem+'-plan.json')).write_text(json.dumps(plan,indent=2))
        result = subprocess.run(command,capture_output=True,timeout=120)
        (OUT / (stem+'-stdout.txt')).write_bytes(result.stdout)
        (OUT / (stem+'-stderr.txt')).write_bytes(result.stderr)
        observations.append({'package':name,'check':label,'exit_code':result.returncode,'stdout':result.stdout.decode('utf-8')})
(OUT / 'result.json').write_text(json.dumps(observations,indent=2))
print(json.dumps(observations))
