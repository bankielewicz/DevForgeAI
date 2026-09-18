"""Bind the qualified candidate and prepare the already-selected source observation.

This is evidence preparation, not protected acceptance or native launch authority.
"""
import hashlib
import json
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORK = Path(r'C:\Projects\DevForgeAI')
DEV = WORK/'docs/plan/framework-worker-source-identity/20260916T021843Z-dev'
QA = WORK/'docs/plan/framework-worker-source-identity-qa/20260916T021843Z-retest'
PACKAGE = WORK/'devforgeai/experiments/codex-worker-probe'

def sha(path):
    result = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024*1024), b''):
            result.update(chunk)
    return result.hexdigest()

def write(name, value):
    with (ROOT/name).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')

assert sha(QA/'qa-report.md') == 'b2e8304c07a89a7c155669e1d0a9e9b93c8f5a0ac966b567fca1fee461b7f2d0'
assert sha(QA/'artifact-index.json') == 'cbb0f150f80282a3e3490fd4ec150c1645ab71cad026b07cfb6888b77f93eb5c'
index = json.loads((QA/'artifact-index.json').read_text())
assert len(index['entries']) == index['entry_count'] == 312
files = reparses = 0
for row in index['entries']:
    relative = Path(row['path'])
    assert not relative.is_absolute() and '..' not in relative.parts
    path = QA/relative
    stat = path.lstat()
    if row['kind'] == 'file':
        assert not stat.st_file_attributes & 0x400, str(path)
        assert stat.st_size == row['bytes'] and sha(path) == row['sha256'], str(path)
        files += 1
    else:
        assert row['kind'] == 'reparse' and stat.st_file_attributes & 0x400
        assert stat.st_reparse_tag == row['reparse_tag'] and os.readlink(path) == row['target']
        reparses += 1
checkpoint = json.loads((QA/'checkpoint.json').read_text())
assert checkpoint['verdict'] == 'PASS' and checkpoint['execution_status'] == 'COMPLETED'
assert not checkpoint['owned_processes']
manifest = DEV/'candidate-manifest.json'
assert sha(manifest) == '3108f976f7d51b734ab995ebf729302ef74a4386ddaafb5561cddbd6f588d65c'
candidate = json.loads(manifest.read_text())
assert len(candidate) == 56
for row in candidate:
    assert row['kind'] == 'file' and sha(PACKAGE/row['path']) == row['sha256'], row['path']
inputs = json.loads((DEV/'selected-inputs-final.json').read_text())
for row in inputs:
    assert sha(WORK/row['path']) == row['sha256'], row['path']
binary = QA/'target-original/debug/devforgeai-codex-worker-probe.exe'
assert sha(binary) == 'b63a0dfb0a48adfc5977a75d145fa766345a9d948e99b3a5bbdf5d5ce74079b2'
task = PACKAGE/'tests/fixtures/task.json'
assert sha(task) == 'b35366b508eea199c12142a8a4a8d13a083426c35c4b9ebaf9f0ccf168eeab3a'
trial = WORK/'docs/plan/framework-worker-trials/20260916T034357Z-source-observation'
trial.mkdir(exist_ok=False)
fixture = trial/'fixture'
fixture.mkdir()
(fixture/'task.json').write_bytes(task.read_bytes())
assert sha(fixture/'task.json') == sha(task)
shutil.copyfile(DEV/'record.py', ROOT/'record.py')
value = {'candidate_manifest': str(manifest), 'candidate_manifest_sha256': sha(manifest),
         'candidate_files': len(candidate), 'selected_input_count': len(inputs),
         'qa_report': str(QA/'qa-report.md'), 'qa_report_sha256': sha(QA/'qa-report.md'),
         'qa_index': str(QA/'artifact-index.json'), 'qa_index_sha256': sha(QA/'artifact-index.json'),
         'qa_index_verified_files': files, 'qa_index_verified_reparses': reparses,
         'binary': str(binary), 'binary_sha256': sha(binary), 'fixture': str(fixture),
         'task_sha256': sha(task), 'selected_operation': 'profile-sources',
         'native_model_trial_attempts': 0, 'framework_acceptance': 'NOT_EVALUATED'}
write('bindings.json', value)
print(json.dumps(value))
