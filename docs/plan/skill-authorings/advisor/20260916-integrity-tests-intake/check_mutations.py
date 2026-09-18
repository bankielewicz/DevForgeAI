"""Remove one guard in each isolated copy; require its precise test to fail."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

RUN = Path(__file__).resolve().parent.parent / '20260916-integrity-tests'
BASE = RUN / 'candidate'
OUTPUT = RUN / 'maintenance/mutations'
OUTPUT.mkdir(exist_ok=False)
variants = [
    ('receipt-raw', 'raise ValueError("Prior stream receipt disagrees with raw output: " + key)',
     'test_receipt_cost_disagreeing_with_raw_stream_is_rejected'),
    ('launch-receipt', 'raise ValueError("Prior launch record disagrees with receipt")',
     'test_launch_version_disagreeing_with_receipt_is_rejected_after_rehash'),
    ('envelope-raw', 'raise ValueError("Prior final envelope disagrees with raw output")',
     'test_final_envelope_disagreeing_with_raw_stream_is_rejected_after_rehash'),
    ('stray-response', 'raise ValueError("Unexpected prior extracted response")',
     'test_failed_attempt_with_stray_extracted_response_is_rejected'),
    ('stream-format', 'raise ValueError("Invalid prior stream format")',
     'test_stream_receipt_with_extra_field_is_rejected'),
]
source = (BASE / 'scripts/advisor_run.py').read_text(encoding='utf-8')
results = []
environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
for name, old, test in variants:
    assert source.count(old) == 1, name
    destination = OUTPUT / name
    shutil.copytree(BASE, destination)
    path = destination / 'scripts/advisor_run.py'
    path.write_text(source.replace(old, 'pass'), encoding='utf-8')
    command = [sys.executable, '-B', '-X', 'utf8', '-m', 'unittest', 'discover',
               '-s', str(destination / 'tests'), '-p', 'test_integrity.py', '-k', test, '-v']
    result = subprocess.run(command, cwd=Path('C:/Projects/DevForgeAI'), env=environment,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
    (destination / 'stdout.txt').write_bytes(result.stdout)
    (destination / 'stderr.txt').write_bytes(result.stderr)
    caught = (result.returncode == 1 and b'AssertionError: ValueError not raised' in result.stderr
              and b'ERROR:' not in result.stderr)
    results.append({'guard': name, 'test': test, 'command': command,
                    'exit_code': result.returncode, 'guard_removal_detected': caught,
                    'mutated_source_sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
(OUTPUT / 'results.json').write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')
print(json.dumps(results, indent=2))
raise SystemExit(0 if all(result['guard_removal_detected'] for result in results) else 1)
