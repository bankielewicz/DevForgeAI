"""Retain bounded development command attempts; evidence only."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--timeout', type=int, default=180)
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    root = Path(__file__).resolve().parent / args.name
    root.mkdir(exist_ok=False)
    start = datetime.now(timezone.utc).isoformat()
    clock = time.monotonic()
    try:
        process = subprocess.run(command, cwd=Path.cwd(), stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=args.timeout, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
        out, err, code, failure = process.stdout, process.stderr, process.returncode, None
    except subprocess.TimeoutExpired as error:
        out, err, code, failure = error.stdout or b'', error.stderr or b'', None, 'TIMEOUT'
    except OSError as error:
        out, err, code, failure = b'', b'', None, str(error)
    (root/'stdout.txt').write_bytes(out)
    (root/'stderr.txt').write_bytes(err)
    value = {'command':command,'cwd':str(Path.cwd()),'started_utc':start,
        'finished_utc':datetime.now(timezone.utc).isoformat(),'duration_seconds':time.monotonic()-clock,
        'timeout_seconds':args.timeout,'exit_code':code,'harness_error':failure,
        'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_sha256':hashlib.sha256(err).hexdigest(),
        'host':platform.platform(),'architecture':platform.machine(),'python':sys.version,'executable':sys.executable}
    (root/'receipt.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(value))
    return code if code is not None else 2

if __name__ == '__main__':
    raise SystemExit(main())
