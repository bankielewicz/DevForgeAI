"""Bounded final package readback; only refresh authorized builder manifest."""
import json
from pathlib import Path
from preserve import capture, save, sha

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[4]
BUILDER = ROOT / 'src/agents/skills/skill-builder'
initial = json.loads((RUN / 'builder-before.json').read_text())
current = capture(BUILDER)
assert not current['exclusions']
manifest = {'schema_version': 'authoring-package-v1', 'artifacts': {
    row['path']: row['sha256'] for row in current['files'] if row['path'] != 'package-manifest.json'}}
(BUILDER / 'package-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
final = capture(BUILDER)
save(RUN / 'builder-final.json', final)
before = {r['path']: r['sha256'] for r in initial['files']}
after = {r['path']: r['sha256'] for r in final['files']}
save(RUN / 'source-delta.json', {
    'changed': [p for p in before if p in after and before[p] != after[p]],
    'added': [p for p in after if p not in before],
    'removed': [p for p in before if p not in after]})
expected_inputs = json.loads((RUN / 'input-hashes.json').read_text())
actual_inputs = {p: sha((ROOT / p).read_bytes()) for p in expected_inputs}
assert expected_inputs == actual_inputs
save(RUN / 'input-readback.json', actual_inputs)
for name, relative in [('companion', 'src/agents/skills/skill-validator'), ('operational-builder', '.agents/skills/skill-builder'), ('operational-validator', '.agents/skills/skill-validator')]:
    observed = capture(ROOT / relative)
    save(RUN / (name + '-after.json'), observed)
    old = json.loads((RUN / (name + '-before.json')).read_text())
    print(name, 'UNCHANGED' if old == observed else 'CHANGED_EXTERNALLY', observed['package_digest'])
    if name.startswith('operational'):
        assert old == observed
issues = []
import re
for row in final['files']:
    data = (BUILDER / row['path']).read_bytes()
    text = data.decode('utf-8')
    if re.search(r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b', text, re.I):
        issues.append(row['path'] + ': concrete UUID')
    for marker in ('C:\\Projects\\DevForgeAI', 'C:/Projects/DevForgeAI', 'C:\\Users\\bryan', '/home/bryan'):
        if marker in text:
            issues.append(row['path'] + ': original root constant')
save(RUN / 'identity-scan.json', {'status': 'PASS' if not issues else 'FAIL', 'issues': issues, 'files_checked': len(final['files']), 'method': 'UUID literal and known original root scan plus descriptor/runtime manual review; generic schemas may name project_id.'})
assert not issues
print('builder', final['package_digest'], len(final['files']))
