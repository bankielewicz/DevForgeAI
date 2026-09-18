"""QA evidence capture only; no framework policy or acceptance authority."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
WORK = Path('C:/Projects/DevForgeAI')
PACKAGE = WORK / 'devforgeai/experiments/codex-worker-probe'
CARGO = Path('C:/Users/bryan/.cargo/bin/cargo.exe')

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def write(name, value):
    (ROOT / name).write_text(json.dumps(value, indent=2), encoding='utf-8')

def capture(label, args, cwd=PACKAGE, timeout=300, extra=None):
    attempt = ROOT / label
    attempt.mkdir(exist_ok=False)
    manifest = [{'path': str(p), 'bytes': p.stat().st_size, 'sha256': sha(p)}
                for p in sorted(PACKAGE.rglob('*'))
                if p.is_file() and 'target' not in p.relative_to(PACKAGE).parts]
    (attempt / 'candidate-manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    env = os.environ.copy()
    env['CARGO_TARGET_DIR'] = str(ROOT / 'target')
    env['WF_TEST_EVIDENCE'] = str(attempt / 'fixtures')
    if extra:
        env.update(extra)
    receipt = {'argv': [str(x) for x in args], 'cwd': str(cwd),
               'executable_sha256': sha(args[0]), 'start': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'candidate_manifest_sha256': sha(attempt / 'candidate-manifest.json'),
               'target': env['CARGO_TARGET_DIR'], 'fixture_root': env['WF_TEST_EVIDENCE']}
    start = time.monotonic()
    with (attempt / 'stdout.txt').open('wb') as out, (attempt / 'stderr.txt').open('wb') as err:
        child = subprocess.Popen([str(x) for x in args], cwd=cwd, env=env, stdout=out, stderr=err, stdin=subprocess.DEVNULL)
        receipt['owned_pid'] = child.pid
        try:
            receipt['exit_code'] = child.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            receipt['timeout'] = timeout
            # Only the live process tree launched by this recorder is contained.
            cleanup = subprocess.run(['C:/Windows/System32/taskkill.exe', '/PID', str(child.pid), '/T', '/F'], capture_output=True, timeout=20)
            (attempt / 'containment.txt').write_bytes(cleanup.stdout + cleanup.stderr)
            receipt['exit_code'] = child.wait(timeout=20)
    receipt['elapsed_seconds'] = time.monotonic() - start
    receipt['end'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    receipt['stdout_sha256'] = sha(attempt / 'stdout.txt')
    receipt['stderr_sha256'] = sha(attempt / 'stderr.txt')
    (attempt / 'receipt.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
    print(json.dumps(receipt), flush=True)
    return receipt

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'capture':
        capture(sys.argv[2], [CARGO, *sys.argv[3:]], timeout=360)
    elif mode == 'environment':
        bindings = []
        for name in ['delivery-manifest.json', 'schema-manifest.json']:
            source = WORK / 'docs/plan/framework-worker-contract/20260915T151300Z' / name
            for entry in json.loads(source.read_text(encoding='utf-8-sig')):
                actual = sha(WORK / entry['path'])
                bindings.append({**entry, 'actual_sha256': actual, 'matches': actual == entry['sha256']})
        write('contract-readback.json', bindings)
        write('environment.json', {'platform': platform.platform(), 'machine': platform.machine(), 'python': sys.version,
              'cwd': str(WORK), 'filesystem': 'Windows native C: local filesystem', 'git_present': (WORK/'.git').exists(),
              'contract_files': len(bindings), 'contract_mismatches': sum(not x['matches'] for x in bindings)})
        for label, args in [('cargo-version',[CARGO,'--version']),('rustc-version',[CARGO.with_name('rustc.exe'),'-vV']),
                            ('format-version',[CARGO,'fmt','--version']),('clippy-version',[CARGO,'clippy','--version']),
                            ('coverage-version',[CARGO,'llvm-cov','--version']),('coverage-help',[CARGO,'llvm-cov','--help'])]:
            capture(label,args,timeout=30)
    elif mode == 'test':
        capture('01-tests',[CARGO,'test','--locked','--offline','--all-targets'],timeout=360)
    elif mode == 'format':
        capture('02-format',[CARGO,'fmt','--all','--','--check'],timeout=60)
    elif mode == 'clippy':
        capture('03-clippy',[CARGO,'clippy','--locked','--offline','--all-targets','--','-D','warnings'],timeout=180)
    elif mode == 'coverage':
        capture('04-coverage',[CARGO,'llvm-cov','--locked','--offline','--all-targets','--json','--output-path',ROOT/'coverage.json'],timeout=360)
    else:
        raise SystemExit('unknown capture selection')
