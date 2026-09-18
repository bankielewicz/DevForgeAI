"""Linux native helper suite through WSL, fresh evidence and fixed 120s bound."""
import datetime
import json
from pathlib import Path
import subprocess
import sys

RUN = Path(__file__).resolve().parent
stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
attempt = RUN / 'attempts' / (stamp + '-linux')
attempt.mkdir(parents=True, exist_ok=False)
def linux(path):
    return '/mnt/c/' + str(path)[3:].replace(chr(92), '/')
cleanup = ['wsl', '-d', 'Ubuntu', '--exec', 'python3', '-B', '-X', 'utf8', linux(RUN / 'linux_cleanup.py')]
cleanup_result = subprocess.run(cleanup, capture_output=True, timeout=20)
(attempt / 'cleanup.stdout').write_bytes(cleanup_result.stdout)
(attempt / 'cleanup.stderr').write_bytes(cleanup_result.stderr)
# A Linux-side timeout contains the trial even if the Windows launcher exits.
# Keep expensive 2,001-file mount tests with their retained timeout; select the
# distinct portable binding/path cases for this follow-up without raising caps.
command = ['wsl', '-d', 'Ubuntu', '--exec', '/usr/bin/timeout', '--signal=TERM', '--kill-after=5s', '110s', '/usr/bin/env', 'ADAPTIVE_TEST_ROOT=' + linux(attempt / 'fixtures'), 'python3', '-B', '-X', 'utf8', linux(RUN / 'test_adaptive.py'), 'AdaptiveTests.test_BAT07_runtime_binding_matrix', 'AdaptiveTests.test_BAT07_ambiguous_core_variants', 'AdaptiveTests.test_BAT06_portability_identity_and_unbound', 'AdaptiveTests.test_BAT15_excluded_file_and_usage', 'AdaptiveTests.test_BAT02_link_rejection']
receipt = {'command': command, 'timeout_seconds': 120, 'started_at_utc': stamp, 'permitted_write_root': str(attempt)}
(attempt / 'plan.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
try:
    result = subprocess.run(command, capture_output=True, timeout=120)
    receipt.update(exit_code=result.returncode, timed_out=False)
    stdout, stderr = result.stdout, result.stderr
except subprocess.TimeoutExpired as exc:
    receipt.update(exit_code=None, timed_out=True)
    stdout, stderr = exc.stdout or b'', exc.stderr or b''
(attempt / 'stdout.txt').write_bytes(stdout)
(attempt / 'stderr.txt').write_bytes(stderr)
(attempt / 'receipt.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
print(str(attempt))
print(json.dumps(receipt))
print(stderr.decode('utf-8', errors='replace')[-6000:])
sys.exit(receipt['exit_code'] if receipt['exit_code'] is not None else 2)
