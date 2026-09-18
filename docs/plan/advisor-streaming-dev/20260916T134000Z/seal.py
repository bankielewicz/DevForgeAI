"""Verify delivery links and preserved boundaries, then hash fresh development evidence."""
import hashlib
import json
from pathlib import Path
import re

ROOT = Path('C:/Projects/DevForgeAI')
HERE = Path(__file__).resolve().parent
readback = json.loads((HERE/'final-readback.json').read_text())
source = ROOT/'src/agents/skills/advisor'
expected = {row['path']:row['sha256'] for row in readback['files']}
actual = {p.relative_to(source).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
          for p in source.rglob('*') if p.is_file()}
assert actual == expected
before = json.loads((ROOT/'docs/plan/skill-authorings/advisor/20260916T134000Z-streaming-intake/preservation-before.json').read_text())
operational = ROOT/'.agents/skills/advisor'
assert {p.relative_to(operational).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
        for p in operational.rglob('*') if p.is_file()} == before['operational']
assert hashlib.sha256((ROOT/'advisor-test.ps1').read_bytes()).hexdigest() == before['example']['sha256']
links = re.findall(r'\]\(([^)]+)\)', (HERE/'delivery.md').read_text(encoding='utf-8'))
for link in links:
    assert (HERE/link).is_file(), link
rows = sorted([{'path':p.relative_to(HERE).as_posix(),'bytes':p.stat().st_size,
                'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
               for p in HERE.rglob('*') if p.is_file() and p.name != 'artifact-manifest.json'],key=lambda row:row['path'])
value = {'schema':'advisor-development-evidence-v1','files':rows,
         'source_package_digest':readback['package_digest'],'source_unchanged':True,
         'operational_unchanged':True,'user_example_unchanged':True,'delivery_links_verified':len(links)}
with (HERE/'artifact-manifest.json').open('x',encoding='utf-8') as stream:
    json.dump(value,stream,indent=2)
    stream.write('\n')
assert all(hashlib.sha256((HERE/row['path']).read_bytes()).hexdigest() == row['sha256'] for row in rows)
print(json.dumps({'evidence_files':len(rows),'source_files':len(actual),'links_verified':len(links),'readback':'MATCH'}))
