"""Inspected maintenance command runner with fresh retained attempts, 120s cap."""
import argparse
import datetime
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[4]
BUILDER = ROOT / 'src/agents/skills/skill-builder'
VALIDATOR = ROOT / 'src/agents/skills/skill-validator'
PINNED = RUN / 'assessment-owner/skill-validator'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('suite', choices=['helpers', 'legacy', 'legacy-pinned', 'authoring', 'structure', 'quick', 'host'])
    args = parser.parse_args()
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    attempt = RUN / 'attempts' / (stamp + '-' + args.suite)
    attempt.mkdir(parents=True, exist_ok=False)
    env = os.environ.copy()
    temp = attempt / 'temp'
    temp.mkdir()
    env.update(TMP=str(temp), TEMP=str(temp), TMPDIR=str(temp), PYTHONDONTWRITEBYTECODE='1', AUTHORING_BUILDER_ROOT=str(BUILDER), ADAPTIVE_TEST_ROOT=str(attempt / 'fixtures'))
    py = [sys.executable, '-B', '-X', 'utf8']
    commands = {
        'helpers': py + [str(RUN / 'test_adaptive.py')],
        'legacy': py + ['-m', 'unittest', 'discover', '-s', str(VALIDATOR / 'tests'), '-v'],
        'legacy-pinned': py + ['-m', 'unittest', 'discover', '-s', str(PINNED / 'tests'), '-v'],
        'authoring': py + ['-m', 'unittest', 'discover', '-s', str(VALIDATOR / 'tests'), '-p', 'test_authoring.py', '-v'],
        'structure': py + [str(PINNED / 'scripts/observe.py'), 'structure', '--source', str(BUILDER)],
        'quick': py + [r'C:\Users\bryan\.codex\skills\.system\skill-creator\scripts\quick_validate.py', str(BUILDER)],
        'host': ['codex', '--version'],
    }
    command = commands[args.suite]
    receipt = {'suite': args.suite, 'command': command, 'cwd': str(ROOT), 'timeout_seconds': 120, 'started_at_utc': stamp, 'permitted_write_root': str(attempt), 'executor': sys.executable}
    (attempt / 'plan.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
    try:
        result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, timeout=120)
        stdout, stderr = result.stdout, result.stderr
        receipt.update(exit_code=result.returncode, timed_out=False)
    except subprocess.TimeoutExpired as exc:
        stdout, stderr = exc.stdout or b'', exc.stderr or b''
        receipt.update(exit_code=None, timed_out=True)
    except OSError as exc:
        stdout, stderr = b'', str(exc).encode()
        receipt.update(exit_code=None, timed_out=False, status='NOT_RUN')
    (attempt / 'stdout.txt').write_bytes(stdout)
    (attempt / 'stderr.txt').write_bytes(stderr)
    receipt['ended_at_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00', 'Z')
    (attempt / 'receipt.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
    print(str(attempt))
    print(json.dumps(receipt))
    print(stdout.decode('utf-8', errors='replace')[-1200:])
    print(stderr.decode('utf-8', errors='replace')[-9000:])
    return receipt.get('exit_code') if receipt.get('exit_code') is not None else 2


if __name__ == '__main__':
    sys.exit(main())
