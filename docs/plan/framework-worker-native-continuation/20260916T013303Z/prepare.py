"""Prepare a read-only compiled inventory observation on the frozen QA candidate."""
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORK = Path(r'C:\Projects\DevForgeAI')
DEV = WORK/'docs/plan/framework-worker-native-completion/20260916T003840Z-dev'
QA = WORK/'docs/plan/framework-worker-native-completion-qa/20260916T003840Z-retest'
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
manifest_path = DEV/'candidate-manifest.json'
assert sha(manifest_path)=='c27d8ce1742ba7cd0955f0bd18aded8de5f14c898c989654d7298835c3256f9e'
manifest = json.loads(manifest_path.read_text())
for item in manifest:
    assert sha(Path(item['path']))==item['sha256'],item['path']
inputs = json.loads((DEV/'inputs-manifest.json').read_text())
for item in inputs:
    assert sha(Path(item['path']))==item['sha256'],item['path']
for name,expected in [('artifact-manifest.json','404cbff08f72b75402b4f5e11d01e032ea5b2311da006f2a114fd467f1391109'),('qa-report.md','6b989e180f9e85cd475835aff72eb96ab780dffeb76a9352df6a21dd70eb5793')]:
    assert sha(QA/name)==expected
receipt = json.loads((QA/'03-full-tests/receipt.json').read_text())
assert receipt['native_exit_code']==0 and receipt['candidate_matches_frozen_after']
binary = QA/'target/debug/devforgeai-codex-worker-probe.exe'
assert binary.is_file()
task = WORK/'devforgeai/experiments/codex-worker-probe/tests/fixtures/task.json'
trial = WORK/'docs/plan/framework-worker-trials/20260916T013303Z-source-observation'
trial.mkdir(exist_ok=False)
fixture = trial/'fixture'
fixture.mkdir()
(fixture/'task.json').write_bytes(task.read_bytes())
shutil.copyfile(DEV/'record.py',ROOT/'record.py')
value = {'candidate_manifest':str(manifest_path),'candidate_manifest_sha256':sha(manifest_path),'candidate_files':len(manifest),
    'input_files':len(inputs),'binary':str(binary),'binary_sha256':sha(binary),'build_receipt':str(QA/'03-full-tests/receipt.json'),
    'build_receipt_sha256':sha(QA/'03-full-tests/receipt.json'),'fixture':str(fixture),'task_sha256':sha(fixture/'task.json'),
    'selected_operation':'profile-sources','native_model_trial_attempts':0}
with (ROOT/'bindings.json').open('x',encoding='utf-8') as stream:
    json.dump(value,stream,indent=2)
print(json.dumps(value))
