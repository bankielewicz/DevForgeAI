"""Bind the selected correction and retained evidence before independent retest."""
import hashlib
import json
import os
import stat
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = Path('C:/Projects/DevForgeAI')
DEV = PROJECT / 'docs/plan/framework-worker-logging/20260917T102726Z-dev-qa-fixes'
OLD = PROJECT / 'docs/plan/framework-worker-logging/20260917T023835Z-qa'
CANDIDATE = PROJECT / 'devforgeai/experiments/codex-worker-probe-logging-qa-fixes'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def entry(path):
    return {'path': str(path), 'bytes': path.stat().st_size, 'sha256': sha(path)}


def verify(items):
    for item in items:
        actual = entry(Path(item['path']))
        assert all(actual[key] == item[key] for key in actual), item['path']


def write(name, value):
    with (ROOT / name).open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=True)
        stream.write('\n')


assert sha(DEV / 'handoff-manifest.json') == '1e4e0800a737f07d658a50383ccdf98c6aa5237c73675d2539ccb7689065f9f5'
assert sha(OLD / 'handoff-manifest.json') == '0c6949f4379e7c469643f34ad6d4b1f664f48177f8865d12dfedd7cbe901019e'
for base in [DEV, OLD]:
    manifest = read(base / 'handoff-manifest.json')
    for item in manifest['entries'].values():
        assert item['required_path'] == item['path']
    verify(manifest['entries'].values())
    evidence = read(base / 'evidence-manifest.json')
    verify(evidence['files'])
    if 'binaries' in evidence:
        verify(evidence['binaries'])

candidate = read(DEV / 'candidate-manifest.json')
verify(candidate)
files = []
for current, directories, names in os.walk(CANDIDATE, followlinks=False):
    for name in directories + names:
        path = Path(current) / name
        assert not (getattr(path.lstat(), 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT), str(path)
    files.extend(str(Path(current) / name) for name in names)
assert set(files) == {item['path'] for item in candidate}
assert len(candidate) == 68
old_candidate = read(OLD / 'candidate-manifest.json')
preserved = old_candidate + read(OLD / 'preserved-manifest.json')
verify(preserved)
verify(read(OLD / 'input-manifest.json'))
old_by_relative = {str(Path(item['path']).relative_to(PROJECT / 'devforgeai/experiments/codex-worker-probe-logging')).replace('\\','/'): item for item in old_candidate}
changed = []
for item in candidate:
    relative = item['relative_path']
    before = old_by_relative.get(relative)
    if not before or before['sha256'] != item['sha256']:
        changed.append({'relative_path': relative, 'before': before, 'after': item})
assert {item['relative_path'] for item in changed} == {'README.md','src/journal.rs','tests/inspection_consistency.rs'}
assert changed == [{key: item[key] for key in ['relative_path','before','after']} for item in read(DEV / 'changed-file-manifest.json')]

input_paths = {str(Path(item['path'])) for item in read(OLD / 'input-manifest.json')}
for base in [DEV, OLD]:
    input_paths.add(str(base / 'handoff-manifest.json'))
    input_paths.add(str(base / 'final-readback.json'))
    input_paths.update(item['path'] for item in read(base / 'handoff-manifest.json')['entries'].values())
for item in read(DEV / 'specification-bindings.json'):
    input_paths.add(item['path'])
for path in (OLD / 'qa-harness').iterdir():
    if path.is_file():
        input_paths.add(str(path))
for name in ['run_command.py','measure.py']:
    input_paths.add(str(OLD / name))
for path in (DEV / 'supplemental-harness').iterdir():
    if path.is_file():
        input_paths.add(str(path))
write('candidate-manifest.json', [{key: item[key] for key in ['path','bytes','sha256']} for item in candidate])
write('preserved-manifest.json', preserved)
write('input-manifest.json', [entry(Path(path)) for path in sorted(input_paths)])
write('specification-bindings.json', read(DEV / 'specification-bindings.json'))
write('changed-files.json', changed)
write('source-denominator.json', [entry(path) for path in sorted((CANDIDATE / 'src').glob('*.rs'))])
write('preservation-manifests.json', [entry(base / name) for base,name in [(OLD,'evidence-manifest.json'),(DEV,'evidence-manifest.json')]])
write('intake-verification.json', {
    'timestamp_utc': datetime.now(timezone.utc).isoformat(),
    'supplied_handoff_sha256_verified': sha(DEV / 'handoff-manifest.json'),
    'candidate_files': len(candidate), 'changed_files': [item['relative_path'] for item in changed],
    'preserved_source_files': len(preserved), 'input_files': len(input_paths),
    'old_qa_evidence_files': len(read(OLD / 'evidence-manifest.json')['files']),
    'development_evidence_files': len(read(DEV / 'evidence-manifest.json')['files']),
    'problems': [], 'git_metadata': 'absent', 'platform': 'Windows x64 / native C: filesystem',
    'defect_states': {'QA-LOG-01': 'FIX_REPORTED', 'QA-LOG-02': 'FIX_REPORTED'},
    'native_codex': 'NOT_RUN', 'framework_acceptance': 'NOT_EVALUATED'
})
print(json.dumps(read(ROOT / 'intake-verification.json'), indent=2))
