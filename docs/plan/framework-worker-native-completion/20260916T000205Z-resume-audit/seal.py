"""Bind supplemental handoff files without modifying prior evidence."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORK = ROOT.parents[3]
QA = WORK / 'docs/plan/framework-worker-native-completion-qa/20260915T2325371896643Z'
paths = {'qa_report': QA / 'qa-report.md', 'original_fix_handoff': QA / 'dev-handoff.md',
         'qa_fix': ROOT / 'qa-fix.md', 'dev_invocation': ROOT / 'dev-invocation.md',
         'identity_readback': ROOT / 'readback.json', 'readback_helper': ROOT / 'readback.py',
         'manifest_helper': ROOT / 'seal.py'}
entries = {}
for name, path in paths.items():
    data = path.read_bytes()
    entries[name] = {'required_path': str(path), 'actual_path': str(path.resolve()),
                     'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
                     'required_equals_actual': path == path.resolve()}
target = ROOT / 'handoff-manifest.json'
target.write_text(json.dumps({'kind': 'supplemental-manual-handoff', 'scope': 'QA-F-COV-01',
    'entries': entries, 'original_campaign_status': 'STOPPED/FAIL', 'new_assignment_selected': False,
    'self_exclusion': 'This manifest cannot contain its own digest.'}, indent=2) + '\n', encoding='utf-8')
readback = json.loads(target.read_text(encoding='utf-8'))
assert readback['entries'] == entries
assert all(entry['required_equals_actual'] for entry in entries.values())
print(json.dumps({'manifest': str(target), 'entries': len(entries),
                  'sha256': hashlib.sha256(target.read_bytes()).hexdigest(), 'readback_matches': True}))
