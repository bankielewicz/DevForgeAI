"""Bounded recorder for QA-owned offline Rust commands; never uses a shell."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parent
CANDIDATE = Path('C:/Projects/DevForgeAI/devforgeai/experiments/codex-worker-probe-logging')
CARGO = Path('C:/Users/bryan/.cargo/bin/cargo.exe')
parser = argparse.ArgumentParser()
parser.add_argument('attempt')
parser.add_argument('action', choices=['build','list','coverage','fmt','clippy','supplement','independent','lock','independent-build'])
parser.add_argument('--case')
args = parser.parse_args()
if (ROOT / 'STOP.json').exists():
    raise SystemExit('Terminal QA stop is present; no command launched.')
for name in ['candidate-manifest.json', 'input-manifest.json', 'preserved-manifest.json']:
    for item in json.loads((ROOT / name).read_text()):
        if hashlib.sha256(Path(item['path']).read_bytes()).hexdigest() != item['sha256']:
            raise SystemExit('Identity drift: ' + item['path'])
attempt = ROOT / 'attempts' / args.attempt
attempt.mkdir(parents=True, exist_ok=False)
env = os.environ.copy()
overrides = {'CARGO_TARGET_DIR': str(ROOT / 'build-target'),
             'WF_TEST_EVIDENCE': str(attempt / 'fixtures')}
cwd = CANDIDATE
tail = ['--offline','--locked','--manifest-path', str(CANDIDATE / 'Cargo.toml')]
timeout = 180
if args.action == 'independent-build':
    command = [str(CARGO), 'test', '--offline', '--locked', '--manifest-path', str(ROOT / 'qa-harness/Cargo.toml'), '--test', 'independent', '--no-run']
    overrides['CARGO_TARGET_DIR'] = str(ROOT / 'independent-target')
elif args.action == 'lock':
    command = [str(CARGO), 'generate-lockfile', '--offline', '--manifest-path', str(ROOT / 'qa-harness/Cargo.toml')]
elif args.action == 'build':
    command = [str(CARGO), 'build', *tail, '--bins']
elif args.action == 'list':
    command = [str(CARGO), 'test', *tail, '--all-targets', '--', '--list']
elif args.action == 'coverage':
    command = [str(CARGO), 'llvm-cov', *tail, '--all-targets', '--json',
               '--output-path', str(ROOT / 'coverage.json'),
               '--ignore-filename-regex', r'[/\\]tests[/\\]',
               '--fail-under-lines', '95', '--', '--test-threads=1']
    overrides['CARGO_LLVM_COV_TARGET_DIR'] = str(ROOT / 'coverage-target')
    timeout = 420
elif args.action == 'fmt':
    command = [str(CARGO), 'fmt', '--all', '--manifest-path', str(CANDIDATE / 'Cargo.toml'), '--', '--check']
    timeout = 60
elif args.action == 'clippy':
    command = [str(CARGO), 'clippy', *tail, '--all-targets', '--', '-D', 'warnings']
elif args.action == 'supplement':
    manifest = Path('C:/Projects/DevForgeAI/docs/plan/framework-worker-logging/20260917T014842Z-dev/qa-harness/Cargo.toml')
    command = [str(CARGO), 'test', '--offline','--locked','--manifest-path',str(manifest),'--test','raw-windows-capture','--','--test-threads=1']
    overrides['CARGO_TARGET_DIR'] = str(ROOT / 'supplemental-target')
else:
    if not args.case:
        raise SystemExit('Independent execution needs an exact case name.')
    manifest = ROOT / 'qa-harness/Cargo.toml'
    command = [str(CARGO),'test','--offline','--locked','--manifest-path',str(manifest),'--test','independent','--',args.case,'--exact','--test-threads=1']
    overrides['CARGO_TARGET_DIR'] = str(ROOT / 'independent-target')
    overrides['QA_PEER'] = str(ROOT / 'build-target/debug/protocol-peer.exe')
    overrides['QA_PROBE'] = str(ROOT / 'build-target/debug/devforgeai-codex-worker-probe.exe')
env.update(overrides)
now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
receipt = {'attempt':args.attempt,'action':args.action,'case':args.case,'argv':command,'cwd':str(cwd),
           'platform':'Windows x64, native C: filesystem', 'environment_overrides':overrides,
           'started_utc':now(),'timeout_seconds':timeout,
           'executable_sha256':hashlib.sha256(CARGO.read_bytes()).hexdigest(),
           'plan_sha256':hashlib.sha256((ROOT/'plan.md').read_bytes()).hexdigest()}
(attempt/'launch.json').write_text(json.dumps(receipt,indent=2)+'\n')
start = time.monotonic()
with (attempt/'stdout.txt').open('xb') as stdout, (attempt/'stderr.txt').open('xb') as stderr:
    process = subprocess.Popen(command,cwd=cwd,env=env,stdin=subprocess.DEVNULL,
                               stdout=stdout,stderr=stderr,creationflags=subprocess.CREATE_NO_WINDOW)
    receipt['owned_pid'] = process.pid
    (attempt/'process.json').write_text(json.dumps({'pid':process.pid,'argv':command,'started_utc':receipt['started_utc']},indent=2)+'\n')
    try:
        receipt['exit_code'] = process.wait(timeout=timeout)
        receipt['timed_out'] = False
    except subprocess.TimeoutExpired:
        receipt['timed_out'] = True
        containment = subprocess.run(['C:/Windows/System32/taskkill.exe','/PID',str(process.pid),'/T','/F'],
                                    capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW,timeout=30)
        (attempt/'containment.stdout.txt').write_bytes(containment.stdout)
        (attempt/'containment.stderr.txt').write_bytes(containment.stderr)
        receipt['containment_exit_code'] = containment.returncode
        receipt['exit_code'] = process.wait(timeout=30)
receipt['ended_utc'] = now()
receipt['elapsed_seconds'] = time.monotonic()-start
receipt['outputs'] = [{'path':str(attempt/name),'bytes':(attempt/name).stat().st_size,
                       'sha256':hashlib.sha256((attempt/name).read_bytes()).hexdigest()} for name in ['stdout.txt','stderr.txt']]
(attempt/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
print((attempt/'stdout.txt').read_text(errors='replace')[-5000:])
print((attempt/'stderr.txt').read_text(errors='replace')[-2000:])
raise SystemExit(receipt['exit_code'] if not receipt['timed_out'] else 124)
