"""Bounded development evidence capture; never a policy or acceptance authority."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
WORK = Path('C:/Projects/DevForgeAI')
PACKAGE = WORK / 'devforgeai/experiments/codex-worker-probe'
CARGO = Path('C:/Users/bryan/.cargo/bin/cargo.exe')

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def capture(label, args, timeout=180):
    attempt = ROOT / label
    attempt.mkdir(exist_ok=False)
    manifest = [{'path': str(p.relative_to(PACKAGE)).replace('\\', '/'),
                 'bytes': p.stat().st_size, 'sha256': sha(p)}
                for p in sorted(PACKAGE.rglob('*'))
                if p.is_file() and 'target' not in p.relative_to(PACKAGE).parts]
    manifest_path = attempt / 'candidate-manifest.json'
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    env = os.environ.copy()
    env['CARGO_TARGET_DIR'] = str(ROOT / 'target')
    env['WF_TEST_EVIDENCE'] = str(attempt / 'fixtures')
    receipt = {'argv': [str(x) for x in args], 'cwd': str(PACKAGE),
               'executable_sha256': sha(args[0]),
               'start': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'candidate_manifest_sha256': sha(manifest_path),
               'target': env['CARGO_TARGET_DIR'], 'fixture_root': env['WF_TEST_EVIDENCE']}
    start = time.monotonic()
    with (attempt / 'stdout.bin').open('wb') as out, (attempt / 'stderr.bin').open('wb') as err:
        child = subprocess.Popen([str(x) for x in args], cwd=PACKAGE, env=env,
                                 stdout=out, stderr=err, stdin=subprocess.DEVNULL)
        receipt['owned_pid'] = child.pid
        try:
            receipt['exit_code'] = child.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            receipt['timeout_seconds'] = timeout
            cleanup = subprocess.run(
                ['C:/Windows/System32/taskkill.exe', '/PID', str(child.pid), '/T', '/F'],
                capture_output=True, timeout=20)
            (attempt / 'containment.bin').write_bytes(cleanup.stdout + cleanup.stderr)
            receipt['containment_exit_code'] = cleanup.returncode
            receipt['exit_code'] = child.wait(timeout=20)
    receipt['elapsed_seconds'] = time.monotonic() - start
    receipt['end'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    receipt['stdout_sha256'] = sha(attempt / 'stdout.bin')
    receipt['stderr_sha256'] = sha(attempt / 'stderr.bin')
    (attempt / 'receipt.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
    print(json.dumps(receipt), flush=True)
    return receipt['exit_code']

if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise SystemExit('usage: record.py LABEL CARGO_ARGS...')
    if sys.argv[2] == '--rustfmt-owned':
        args = [CARGO.with_name('rustfmt.exe'), '--edition', '2024', '--check',
                PACKAGE / 'src/request.rs', PACKAGE / 'tests/support/review_v2_cases.rs']
    else:
        args = [CARGO, *sys.argv[2:]]
    raise SystemExit(capture(sys.argv[1], args))
