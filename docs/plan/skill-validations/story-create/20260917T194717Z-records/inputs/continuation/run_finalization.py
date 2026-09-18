"""Retain exact finalization commands and every real assembly attempt."""
import datetime
import json
import subprocess
import sys
import time

from prepare_continuation import RUN, PROJECT, put

phase = sys.argv[1]
attempt = sys.argv[2]
assert phase in {'consolidate', 'final_delivery_audit'}
assert len(attempt) == 3 and attempt.isdecimal()
stem = phase.replace('_', '-') + '-' + attempt
assert not (RUN / (stem + '.execution.json')).exists()
argv = [sys.executable, '-B', '-X', 'utf8', str(RUN / (phase + '.py'))]
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
clock_start = time.monotonic()
result = subprocess.run(argv, cwd=PROJECT, capture_output=True, timeout=120)
put(RUN / (stem + '.stdout.txt'), result.stdout.decode('utf-8'))
put(RUN / (stem + '.stderr.txt'), result.stderr.decode('utf-8'))
put(RUN / (stem + '.execution.json'), {'argv': argv, 'cwd': str(PROJECT), 'started_at': started, 'ended_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'elapsed_seconds': time.monotonic() - clock_start, 'timeout_seconds': 120, 'exit_code': result.returncode})
print(result.stdout.decode('utf-8'))
print(result.stderr.decode('utf-8'), file=sys.stderr)
raise SystemExit(result.returncode)
