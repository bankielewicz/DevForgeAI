"""Finalize evidence bindings after independent QA stops; no product execution."""
import hashlib
import json
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
WORK = ROOT.parents[3]
QA = WORK / 'docs/plan/framework-worker-native-completion-qa/20260915T2325371896643Z'
EFFECTIVE = ROOT.parent / '20260915T2310034070895Z-effective-dev'


def bind(path):
    return {'path': str(path), 'bytes': path.stat().st_size,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def save(name, value):
    (ROOT / name).write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


required = [QA / name for name in ['qa-report.md', 'dev-handoff.md', 'artifact-manifest.json', 'denominators.md',
                                  'test-integrity.md', 'failed-attempts.md', 'checkpoint.json']]
for path in required:
    if not path.is_file():
        raise SystemExit('QA evidence not finalized: ' + str(path))

qa_manifest_path = QA / 'artifact-manifest.json'
if bind(qa_manifest_path)['sha256'] != '886f2c630a03183df3557d9fc58a24075b3af440ade7e00c398e5c5a8fa6b1c5':
    raise SystemExit('QA manifest differs from independently delivered digest')
qa_manifest = json.loads(qa_manifest_path.read_text(encoding='utf-8'))
qa_mismatches = []
for entry in qa_manifest['entries']:
    path = QA / entry['path']
    actual = bind(path)
    if actual['sha256'] != entry['sha256'] or actual['bytes'] != entry['bytes']:
        qa_mismatches.append(entry['path'])
save('qa-artifact-manifest-readback.json', {'manifest': bind(qa_manifest_path),
     'entries_checked': len(qa_manifest['entries']), 'mismatches': qa_mismatches})
if qa_mismatches:
    raise SystemExit('QA artifact readback mismatch')

effective_files = []
reparses = []
for directory, dirs, files in os.walk(EFFECTIVE, followlinks=False):
    accepted = []
    for name in dirs:
        path = Path(directory) / name
        if path.lstat().st_file_attributes & 0x400:
            reparses.append(str(path))
        elif name != 'target':
            accepted.append(name)
    dirs[:] = accepted
    for name in files:
        path = Path(directory) / name
        if path.lstat().st_file_attributes & 0x400:
            reparses.append(str(path))
        else:
            effective_files.append(bind(path))

save('external-evidence-bindings.json', {'qa': [bind(path) for path in required],
     'qa_raw_coverage': bind(QA / '08a-coverage/coverage.json'),
     'effective_profile_development': sorted(effective_files, key=lambda e: e['path']),
     'reparses_not_followed': reparses,
     'note': 'QA artifact-manifest binds its retained artifacts; effective-dev target is retained but excluded from this non-build inventory.'})

save('final-checkpoint.json', {'status': 'FAIL', 'phase': 'independent QA mandatory stop; failure handoff delivered',
     'candidate_manifest': bind(ROOT / 'candidate-manifest.json'), 'coverage': {'covered_lines': 2852, 'executable_lines': 3103,
     'percent': '91.91105381888495004834031582', 'minimum_percent': 95, 'status': 'FAIL'},
     'rust_functions': {'passed': 89, 'required': 89}, 'unit_functions': {'passed': 20, 'required': 20},
     'wf_parents': {'passed': 20, 'required': 20},
     'native_trials': {'passed': 0, 'required': 2, 'attempts_consumed': 0, 'status': 'NOT_RUN'},
     'framework_acceptance': 'NOT_EVALUATED', 'authority': 'deferred outside worker scope',
     'owned_running_processes': [], 'source_edits_after_freeze': False,
     'next_action': 'Separate development assignment for coverage gaps, then fresh independent QA. Native prerequisites remain unresolved.',
     'historical_attempts_preserved': True})

links = []
for name in ['delivery.md', 'handoff.md', 'native-prerequisite.md']:
    for link in re.findall(r'\]\(([^)]+)\)', (ROOT / name).read_text(encoding='utf-8')):
        if '://' in link:
            continue
        target = (ROOT / link.split('#', 1)[0]).resolve()
        # These are produced immediately afterwards by readback.py.
        deferred = target.name in {'post-qa-source-readback.json', 'post-qa-inputs-readback.json', 'evidence-manifest.json'}
        links.append({'document': name, 'target': str(target), 'exists': target.exists(), 'deferred_to_readback': deferred})
save('delivery-link-readback.json', links)
missing = [entry for entry in links if not entry['exists'] and not entry['deferred_to_readback']]
print(json.dumps({'qa_bindings': len(required) + 1, 'effective_dev_bindings': len(effective_files), 'missing_document_links': missing}))
raise SystemExit(bool(missing))
