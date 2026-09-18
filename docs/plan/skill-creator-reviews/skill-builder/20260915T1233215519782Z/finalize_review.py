"""Retain exact fixture bytes and write the bounded review result."""
import hashlib
import json
from pathlib import Path
import shutil

RUN = Path(__file__).resolve().parent
ROOT = Path(r'C:\Projects\DevForgeAI')


def inventory(path):
    rows = []
    for p in path.rglob('*'):
        if p.is_file():
            data = p.read_bytes()
            rows.append({'path': p.relative_to(path).as_posix(), 'bytes': len(data),
                         'sha256': hashlib.sha256(data).hexdigest()})
    return sorted(rows, key=lambda row: row['path'])


retained = []
for row in (json.loads(line) for line in (RUN / 'fixture-paths.jsonl').read_text().splitlines()):
    source = Path(row['project'])
    destination = RUN / 'fixtures' / row['test'].split('.')[-1]
    shutil.copytree(source, destination)
    retained.append(dict(row, retained=str(destination), exact_copy=inventory(source) == inventory(destination)))
(RUN / 'retained-fixtures.json').write_text(json.dumps(retained, indent=2), encoding='utf-8')
forward = Path(r'C:\Users\bryan\AppData\Local\Temp\meeting-actions-forward-20260915T123432373Z')
shutil.copytree(forward, RUN / 'forward-fixture')
history = forward / 'docs/plan/skill-authorings/meeting-actions/001'
publication = json.loads((history / 'publication-readback.json').read_bytes())
reference_checks = {}
for name in ['authoring_record', 'baseline', 'request']:
    value = publication[name]
    reference_checks[name] = hashlib.sha256(Path(value['path']).read_bytes()).hexdigest() == value['sha256']
delivered = forward / 'src/agents/skills/meeting-actions/SKILL.md'
forward_check = {'publication_state': publication['state'], 'reference_checks': reference_checks,
    'candidate_equals_delivered': (history / 'candidate/SKILL.md').read_bytes() == delivered.read_bytes(),
    'retained_copy_exact': inventory(forward) == inventory(RUN / 'forward-fixture'),
    'begin_exit': (forward / 'begin-exit.txt').read_text(encoding='utf-8-sig').strip(),
    'publish_exit': (forward / 'publish-exit.txt').read_text(encoding='utf-8-sig').strip()}
(RUN / 'forward-readback.json').write_text(json.dumps(forward_check, indent=2), encoding='utf-8')
package = ROOT / 'src/agents/skills/skill-builder'
before = json.loads((RUN / 'source-before.json').read_bytes())
op_before = json.loads((RUN / 'operational-before.json').read_bytes())
preservation = {'source_unchanged': inventory(package) == before['files'],
    'operational_unchanged': inventory(ROOT / '.agents/skills/skill-builder') == op_before['files']}
(RUN / 'final-preservation.json').write_text(json.dumps(preservation, indent=2), encoding='utf-8')
files = inventory(RUN)
(RUN / 'evidence-manifest.json').write_text(json.dumps(files, indent=2), encoding='utf-8')
print(json.dumps({'fixtures': len(retained), 'all_exact': all(row['exact_copy'] for row in retained),
                  'preservation': preservation, 'evidence_files': len(files)}))
