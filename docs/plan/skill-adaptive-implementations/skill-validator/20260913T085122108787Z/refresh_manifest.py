"""Refresh current package executable-artifact manifest; preserve prior copy."""
import hashlib
import json
from capture import ROOT, RUN, scan

root = ROOT / 'src/agents/skills/skill-validator'
path = root / 'evals/build-manifest.json'
before = path.read_bytes()
revision = hashlib.sha256(before).hexdigest()
archive = RUN / ('build-manifest-before-' + revision + '.json')
if not archive.exists():
    archive.write_bytes(before)
value = json.loads(before)
value['artifacts'] = {row['path']:row['sha256'] for row in scan(root)['files'] if row['path'] != 'evals/build-manifest.json'}
path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Current package manifest refreshed; prior manifest retained: '+str(archive))
