"""Development evidence recorder; no framework authority or acceptance decision."""
import datetime
import hashlib
import json
import os
import pathlib
import platform
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
PROJECT = ROOT.parents[3]
PACKAGE = PROJECT / 'devforgeai/experiments/codex-worker-probe'


def identity(path):
    data = path.read_bytes()
    return {'path': str(path), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


if sys.argv[1] == 'inputs':
    checks = []
    for name in ('delivery-manifest.json', 'schema-manifest.json'):
        manifest = PROJECT / 'docs/plan/framework-worker-contract/20260915T151300Z' / name
        for entry in json.loads(manifest.read_bytes()):
            actual = identity(PROJECT / entry['path'])
            checks.append({'manifest': identity(manifest), 'expected': entry, 'actual': actual,
                           'matches': all(entry[k] == actual[k] for k in ('bytes', 'sha256'))})
    for name in ('devforgeai/Cargo.toml', 'devforgeai/Cargo.lock'):
        checks.append({'preserve': identity(PROJECT / name)})
    (ROOT / 'input-checks.json').write_text(json.dumps(checks, indent=2), encoding='utf-8')
    print(json.dumps({'matched': sum(c.get('matches', False) for c in checks), 'expected': 335}))
else:
    attempt, stage, *argv = sys.argv[1:]
    dest = ROOT / attempt
    dest.mkdir(exist_ok=False)
    paths = [p for p in PACKAGE.rglob('*') if p.is_file() and 'target' not in p.relative_to(PACKAGE).parts]
    manifest = [identity(p) for p in sorted(paths)]
    manifest_path = dest / 'candidate.json'
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    executable = shutil.which(argv[0])
    start = now()
    with (dest / 'stdout.txt').open('wb') as out, (dest / 'stderr.txt').open('wb') as err:
        env = os.environ.copy()
        env['WF_TEST_EVIDENCE'] = str(dest / 'runs')
        result = subprocess.run(argv, cwd=PACKAGE, stdout=out, stderr=err, check=False, env=env)
    receipt = {'attempt_id': attempt, 'stage': stage, 'argv': argv, 'working_directory': str(PACKAGE),
               'executable': identity(pathlib.Path(executable)), 'platform': platform.platform(),
               'parent_shell': 'PowerShell 7', 'filesystem': 'native Windows C:',
               'started_at': start, 'ended_at': now(), 'exit_code': result.returncode,
               'candidate': identity(manifest_path), 'stdout': identity(dest / 'stdout.txt'),
               'stderr': identity(dest / 'stderr.txt'), 'outcome': 'observed-exit'}
    (dest / 'receipt.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
    with (ROOT / 'executions.jsonl').open('a', encoding='utf-8') as stream:
        stream.write(json.dumps(receipt) + '\n')
    print(json.dumps(receipt))
    print((dest / 'stdout.txt').read_text(encoding='utf-8', errors='replace')[-12000:])
    print((dest / 'stderr.txt').read_text(encoding='utf-8', errors='replace')[-12000:])
    sys.exit(result.returncode)
