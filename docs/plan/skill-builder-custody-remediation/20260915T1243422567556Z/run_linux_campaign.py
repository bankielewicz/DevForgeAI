"""Run disjoint Linux test batches and native trials, retaining each owned attempt."""
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[3]
SNAPSHOT = Path('/tmp/devforgeai-regression-v3-root-20260915T131000Z')
REL = Path('docs/plan/skill-builder-custody-remediation/20260915T1243422567556Z/regression')
REG = SNAPSHOT / REL
OUT = RUN / 'linux-campaign-001'
OUT.mkdir(exist_ok=False)
native_root = Path('/tmp/devforgeai-custody-native-20260915T1243422567556Z')
native_script = RUN / 'native/native_trials.py'
jobs = []
for name, modules in [
    ('linux-legacy', ['test_remediation', 'test_legacy_maintenance', 'test_acceptance_edges', 'test_final_contract_edges']),
    ('linux-authoring', ['test_design', 'test_authoring', 'test_authoring_safeguards']),
    ('linux-adaptive-stage', ['test_builder_adaptive', 'test_runtime_original', 'test_stage_integrity.StageIntegrityTests', 'test_prewrite_destination'])]:
    jobs.append((name, [sys.executable, '-B', '-X', 'utf8', str(REG / 'launch.py'), name, '--modules', *modules]))
for name in ['linux-simple-v3', 'linux-branching-v3']:
    jobs.append((name, [sys.executable, '-B', '-X', 'utf8', str(native_script), '--root', str(native_root),
        '--source', str(ROOT / 'src/agents/skills/skill-builder'), '--codex', '/home/bryan/.local/bin/codex', '--case', name]))


def execute(job):
    name, command = job
    start = time.monotonic()
    # Children impose their own 120-second case ceilings and native tree cleanup.
    with (OUT / (name + '.stdout.txt')).open('xb') as out, (OUT / (name + '.stderr.txt')).open('xb') as err:
        result = subprocess.run(command, cwd='/tmp', stdout=out, stderr=err)
    receipt = {'name': name, 'argv': command, 'cwd': '/tmp', 'exit_code': result.returncode,
               'seconds': time.monotonic() - start}
    (OUT / (name + '.receipt.json')).write_text(json.dumps(receipt, indent=2))
    if name.endswith('-v3') and (native_root / name).exists():
        shutil.copytree(native_root / name, OUT / name)
    print(json.dumps(receipt), flush=True)
    return receipt


with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(execute, jobs))
for name, args in [('combine', ['linux-combined', 'linux-legacy', 'linux-authoring', 'linux-adaptive-stage']),
                   ('grade', ['linux-combined'])]:
    execute((name, [sys.executable, '-B', '-X', 'utf8', str(REG / (name + '.py')), *args]))
shutil.copytree(REG, OUT / 'regression')
(OUT / 'results.json').write_text(json.dumps(results, indent=2))
print('Linux attempt evidence retained at ' + str(OUT), flush=True)
