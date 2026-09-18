"""Independent argv-only bounded command recorder; no target imports."""
import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from capture import RUN, sha

def run(case, argv, cwd=None, stdin=None, expected=None, env=None, timeout=120):
    dest = RUN / 'commands' / case
    dest.mkdir(parents=True, exist_ok=False)
    before = {'case': case, 'argv': [str(x) for x in argv], 'cwd': str(cwd or RUN), 'timeout_seconds': timeout, 'permitted_write_root': str(RUN), 'expected': expected, 'start_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'stdin_sha256': sha(stdin.encode('utf-8')) if stdin else None}
    (dest / 'command.json').write_text(json.dumps(before, indent=2) + '\n', encoding='utf-8')
    if stdin:
        (dest / 'stdin.txt').write_text(stdin, encoding='utf-8')
    start = time.monotonic()
    try:
        p = subprocess.Popen([str(x) for x in argv], cwd=cwd or RUN, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        try:
            out, err = p.communicate(stdin.encode('utf-8') if stdin else None, timeout=timeout)
            timed_out = False
        except subprocess.TimeoutExpired:
            if os.name == 'nt':
                kill = subprocess.run(['taskkill.exe', '/PID', str(p.pid), '/T', '/F'], capture_output=True, timeout=10)
                (dest / 'termination.txt').write_bytes(kill.stdout + kill.stderr)
            else:
                p.kill()
            out, err = p.communicate(timeout=10)
            timed_out = True
        result = {'exit': p.returncode, 'timeout': timed_out}
    except OSError as exc:
        out, err = b'', str(exc).encode('utf-8')
        result = {'exit': None, 'timeout': False, 'launch_error': str(exc)}
    (dest / 'stdout.txt').write_bytes(out)
    (dest / 'stderr.txt').write_bytes(err)
    result.update({'end_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'elapsed_seconds': time.monotonic() - start, 'stdout_sha256': sha(out), 'stderr_sha256': sha(err)})
    (dest / 'result.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    return result, out.decode('utf-8', errors='replace'), err.decode('utf-8', errors='replace')

if __name__ == '__main__':
    case = sys.argv[1]
    result, out, err = run(case, sys.argv[2:], expected='Tool identification only; no acceptance claim')
    print(json.dumps(result))
    print(out)
    print(err)
