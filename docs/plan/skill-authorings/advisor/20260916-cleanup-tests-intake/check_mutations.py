"""Check new assertions against isolated intentionally broken transport copies."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

RUN = Path(__file__).resolve().parent.parent / '20260916-cleanup-tests'
BASE = RUN / 'candidate'
OUTPUT = RUN / 'maintenance/mutations'
OUTPUT.mkdir(exist_ok=False)
variants = [
    ('suppress-read-error', 'events.put((name, "error", str(error)))', 'pass',
     'test_read_oserror_after_real_bytes_retains_bytes_and_denies_advice'),
    ('lose-wait-interruption',
     'interrupted = True\n            errors.append("cleanup wait interrupted")',
     'errors.append("cleanup wait interrupted")',
     'test_interrupted_wait_retries_and_reaps_real_child'),
    ('suppress-close-error', 'errors.append("pipe close failed: " + str(error))', 'pass',
     'test_pipe_close_oserror_preserves_evidence_and_closes_other_pipe'),
    ('hide-undrained-queue',
     'errors.append("captured stream queue was not fully drained within cleanup ceiling")',
     'pass', 'test_cleanup_deadline_reports_undrained_queue_instead_of_losing_evidence_silently'),
]
source = (BASE / 'scripts/advisor_stream.py').read_text(encoding='utf-8')
results = []
environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
for name, old, new, test in variants:
    assert source.count(old) == 1, name
    destination = OUTPUT / name
    shutil.copytree(BASE, destination)
    path = destination / 'scripts/advisor_stream.py'
    path.write_text(source.replace(old, new), encoding='utf-8')
    command = [sys.executable, '-B', '-X', 'utf8', '-m', 'unittest', 'discover',
               '-s', str(destination / 'tests'), '-p', 'test_cleanup.py', '-k', test, '-v']
    result = subprocess.run(command, cwd=Path('C:/Projects/DevForgeAI'), env=environment,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
    (destination / 'stdout.txt').write_bytes(result.stdout)
    (destination / 'stderr.txt').write_bytes(result.stderr)
    caught = (result.returncode == 1 and b'FAIL:' in result.stderr
              and b'AssertionError' in result.stderr and b'ERROR:' not in result.stderr)
    results.append({'mutation': name, 'test': test, 'command': command,
                    'exit_code': result.returncode, 'assertion_detected': caught,
                    'mutated_source_sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
(OUTPUT / 'results.json').write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')
print(json.dumps(results, indent=2))
raise SystemExit(0 if all(result['assertion_detected'] for result in results) else 1)
