"""Terminate only an owned timed-out Linux trial, identified by exact script/env."""
import os
from pathlib import Path
import signal

run = Path(__file__).resolve().parent
script = str(run / 'test_adaptive.py')
matched = []
for entry in Path('/proc').iterdir():
    if not entry.name.isdigit():
        continue
    try:
        command = (entry / 'cmdline').read_bytes().split(b'\0')
        if script.encode() not in command:
            continue
        values = (entry / 'environ').read_bytes().split(b'\0')
        prefix = ('ADAPTIVE_TEST_ROOT=' + str(run / 'attempts') + '/').encode()
        if any(x.startswith(prefix) and x.endswith(b'-linux/fixtures') for x in values):
            matched.append(int(entry.name))
    except (FileNotFoundError, PermissionError):
        continue
for pid in matched:
    os.kill(pid, signal.SIGTERM)
print({'owned_timed_out_trial_pids_terminated': matched})
