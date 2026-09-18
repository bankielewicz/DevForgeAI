"""Local development evidence recorder; never framework authority."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
PACKAGE = REPO / 'devforgeai/experiments/codex-worker-probe'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def manifest():
    return [{'path': p.relative_to(PACKAGE).as_posix(), 'bytes': p.stat().st_size,
             'sha256': digest(p)} for p in sorted(PACKAGE.rglob('*'))
            if p.is_file() and 'target' not in p.relative_to(PACKAGE).parts]

def write(path, value):
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')

def freeze(label):
    entries = manifest()
    write(ROOT / f'{label}-manifest.json', entries)
    for entry in entries:
        destination = ROOT / f'{label}-snapshot' / entry['path']
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open('xb') as stream:
            stream.write((PACKAGE / entry['path']).read_bytes())
    return entries

if __name__ == '__main__':
    if sys.argv[1] == 'freeze':
        entries = freeze(sys.argv[2])
        print(json.dumps({'files': len(entries), 'sha256': digest(ROOT / f'{sys.argv[2]}-manifest.json')}))
    else:
        attempt, stage, *args = sys.argv[1:]
        destination = ROOT / 'attempts' / attempt
        destination.mkdir(parents=True, exist_ok=False)
        write(destination / 'candidate.json', manifest())
        executable = shutil.which(args[0])
        assert executable
        env = os.environ.copy()
        env['CARGO_TARGET_DIR'] = str(ROOT / 'target')
        env['CARGO_LLVM_COV_TARGET_DIR'] = str(ROOT / f'coverage-target-{attempt}')
        env['WF_TEST_EVIDENCE'] = str(destination / 'fixtures')
        receipt = {'attempt': attempt, 'stage': stage, 'executable': executable,
                   'executable_sha256': digest(Path(executable)), 'arguments': args[1:],
                   'cwd': str(PACKAGE), 'platform': platform.platform(),
                   'filesystem': 'Windows NTFS', 'environment_overrides': {k: env[k] for k in
                   ['CARGO_TARGET_DIR', 'CARGO_LLVM_COV_TARGET_DIR', 'WF_TEST_EVIDENCE']},
                   'candidate_sha256': digest(destination / 'candidate.json'),
                   'started_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   'timeout_seconds': 600}
        write(destination / 'started.json', receipt)
        start = time.monotonic()
        with (destination / 'stdout.txt').open('xb') as stdout, (destination / 'stderr.txt').open('xb') as stderr:
            try:
                result = subprocess.run([executable, *args[1:]], cwd=PACKAGE, env=env,
                                        stdout=stdout, stderr=stderr, timeout=600)
                receipt['exit_code'] = result.returncode
                receipt['outcome'] = 'observed_exit'
            except subprocess.TimeoutExpired:
                receipt['exit_code'] = None
                receipt['outcome'] = 'timeout'
        receipt['seconds'] = time.monotonic() - start
        receipt['ended_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        receipt['stdout_sha256'] = digest(destination / 'stdout.txt')
        receipt['stderr_sha256'] = digest(destination / 'stderr.txt')
        write(destination / 'receipt.json', receipt)
        with (ROOT / 'executions.jsonl').open('a', encoding='utf-8') as stream:
            stream.write(json.dumps(receipt) + '\n')
        print(json.dumps(receipt))
        print((destination / 'stdout.txt').read_text(encoding='utf-8', errors='replace')[-4000:])
        print((destination / 'stderr.txt').read_text(encoding='utf-8', errors='replace')[-4000:])
        sys.exit(receipt['exit_code'] if receipt['exit_code'] is not None else 124)
