"""Keep disposable preparation, execution and archival in one WSL invocation."""
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

RUN = Path(__file__).resolve().parent
SNAPSHOT = Path('/tmp/devforgeai-regression-v3-same-process-002')
REL = Path('docs/plan/skill-builder-custody-remediation/20260915T1243422567556Z/regression')
REG = SNAPSHOT / REL
OUT = RUN / 'linux-regression-002'
OUT.mkdir(exist_ok=False)


def execute(name, command):
    start = time.monotonic()
    with (OUT / (name + '.stdout.txt')).open('xb') as stdout, (OUT / (name + '.stderr.txt')).open('xb') as stderr:
        result = subprocess.run(command, cwd='/tmp', stdout=stdout, stderr=stderr, timeout=150)
    receipt = {'argv': command, 'cwd': '/tmp', 'exit_code': result.returncode,
               'seconds': time.monotonic() - start}
    (OUT / (name + '.receipt.json')).write_text(json.dumps(receipt, indent=2))
    print(json.dumps({'name': name, **receipt}), flush=True)
    return result.returncode


prep = execute('prepare', [sys.executable, '-B', '-X', 'utf8', str(RUN / 'regression/linux_prepare.py'), str(SNAPSHOT)])
if prep:
    sys.exit(prep)
jobs = [
    ('linux-legacy', ['test_remediation', 'test_legacy_maintenance', 'test_acceptance_edges', 'test_final_contract_edges']),
    ('linux-authoring', ['test_design', 'test_authoring', 'test_authoring_safeguards']),
    ('linux-adaptive-stage', ['test_builder_adaptive', 'test_runtime_original', 'test_stage_integrity.StageIntegrityTests', 'test_prewrite_destination'])]


def batch(job):
    name, modules = job
    return execute(name, [sys.executable, '-B', '-X', 'utf8', str(REG / 'launch.py'), name, '--modules', *modules])


with ThreadPoolExecutor(max_workers=3) as executor:
    codes = list(executor.map(batch, jobs))
combine = execute('combine', [sys.executable, '-B', '-X', 'utf8', str(REG / 'combine.py'),
    'linux-combined', *[name for name, _ in jobs]])
grade = execute('grade', [sys.executable, '-B', '-X', 'utf8', str(REG / 'grade.py'), 'linux-combined'])
shutil.copytree(REG, OUT / 'regression')
shutil.copytree(SNAPSHOT / 'docs/plan/skill-independent-qa', OUT / 'linux-fixture-inputs')
print(json.dumps({'batch_codes': codes, 'combine': combine, 'grade': grade, 'retained': str(OUT)}), flush=True)
sys.exit(0 if not any(codes) and not combine and not grade else 1)
