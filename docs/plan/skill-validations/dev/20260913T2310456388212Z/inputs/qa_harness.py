"""Independent read-only QA orchestration. Outputs confined to this run."""
import argparse
import datetime as dt
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import shutil
import stat
import subprocess
import sys
import time

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[4]
TARGET = ROOT / 'src/agents/skills/skill-validator'
LOADED = ROOT / '.agents/skills/skill-validator'
PRIOR = ROOT / 'docs/plan/skill-adaptive-implementations/skill-validator/20260913T085122108787Z'
EXCLUDE = {'.git', 'node_modules', '.venv', 'venv', 'target', 'dist', 'build', '__pycache__', 'devforgeai_cli'}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def now():
    return dt.datetime.now(dt.timezone.utc).isoformat().replace('+00:00', 'Z')

def inventory(root, capture=None):
    root = Path(root).absolute()
    for p in [root, *root.parents]:
        s = p.lstat()
        if stat.S_ISLNK(s.st_mode) or getattr(s, 'st_file_attributes', 0) & 0x400:
            raise ValueError('Unsafe root ancestor: ' + str(p))
    rows, omitted, enumerations = [], [], []
    total = 0
    def walk(directory):
        nonlocal total
        entries = sorted(os.scandir(directory), key=lambda e: e.name)
        enumerations.append({'directory': str(Path(directory).relative_to(root)), 'entries': [e.name for e in entries]})
        for e in entries:
            p = Path(e.path)
            rel = p.relative_to(root).as_posix()
            if e.name in EXCLUDE or 'backup' in e.name.lower() or e.name.lower().endswith(('.bak', '.pyc', '.pyo')) or e.name.startswith('.env') or e.name.lower().endswith(('.pem', '.key')):
                omitted.append({'path': rel, 'reason': 'excluded before reading'})
                continue
            s = e.stat(follow_symlinks=False)
            if e.is_symlink() or getattr(s, 'st_file_attributes', 0) & 0x400:
                raise ValueError('Unsafe link: ' + str(p))
            if stat.S_ISDIR(s.st_mode):
                walk(p)
            elif stat.S_ISREG(s.st_mode):
                if any(c in rel for c in ('\\', '\x00')) or any(c in ('', '.', '..') for c in rel.split('/')):
                    raise ValueError('Invalid relative path')
                total += s.st_size
                if len(rows) >= 2000 or total > 32 * 1024 * 1024:
                    raise ValueError('Capture ceiling exceeded')
                data = p.read_bytes()
                rows.append({'path': rel, 'bytes': len(data), 'sha256': sha(data)})
                if capture:
                    dst = Path(capture) / rel
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    dst.write_bytes(data)
                    assert dst.read_bytes() == data
            else:
                raise ValueError('Special file: ' + str(p))
    walk(root)
    rows.sort(key=lambda r: r['path'])
    return {'root': str(root), 'files': rows, 'package_digest': sha(json.dumps(rows, ensure_ascii=False, separators=(',', ':')).encode('utf-8')), 'file_count': len(rows), 'bytes': total, 'exclusions': omitted, 'enumerations': enumerations}

def execute(name, argv, cwd=ROOT, timeout=120, stdin=None):
    out = RUN / 'commands' / name
    out.mkdir(parents=True, exist_ok=False)
    env = os.environ.copy()
    temp = RUN / 'trials' / 'temp' / name
    temp.mkdir(parents=True, exist_ok=False)
    env.update(TEMP=str(temp), TMP=str(temp), TMPDIR=str(temp), PYTHONDONTWRITEBYTECODE='1')
    record = {'argv': [str(x) for x in argv], 'cwd': str(cwd), 'started_at_utc': now(), 'timeout_seconds': timeout, 'environment_overrides': {k: env[k] for k in ('TEMP','TMP','TMPDIR','PYTHONDONTWRITEBYTECODE')}, 'stdin': stdin, 'termination': 'not-started'}
    save(out / 'command.json', record)
    start = time.monotonic()
    with (out / 'stdout.txt').open('wb') as stdout, (out / 'stderr.txt').open('wb') as stderr:
        try:
            p = subprocess.Popen(record['argv'], cwd=cwd, env=env, stdin=subprocess.PIPE if stdin else subprocess.DEVNULL, stdout=stdout, stderr=stderr)
            record['pid'] = p.pid
            try:
                p.communicate(stdin.encode('utf-8') if stdin else None, timeout=timeout)
                record.update(exit_status=p.returncode, termination='exited')
            except subprocess.TimeoutExpired:
                if os.name == 'nt':
                    k = subprocess.run(['taskkill', '/PID', str(p.pid), '/T', '/F'], capture_output=True, timeout=15)
                    (out / 'termination-stdout.txt').write_bytes(k.stdout)
                    (out / 'termination-stderr.txt').write_bytes(k.stderr)
                    record['tree_termination_exit'] = k.returncode
                else:
                    p.kill()
                p.wait(timeout=15)
                record.update(exit_status=p.returncode, termination='timeout')
        except Exception as e:
            record.update(exit_status=None, termination='runner-error', error=str(e))
    record.update(ended_at_utc=now(), elapsed_seconds=time.monotonic()-start)
    save(out / 'command.json', record)
    print(json.dumps({'attempt': name, **record}, ensure_ascii=False))
    return record

def preflight():
    hashes = {}
    for name, expected in [('skill-validator-adaptive-enhancement-spec.md', 'f08a5f745235e969c8186731c187bdc5150d8f92cc8d140d0deb6812e7ecaf42'), ('skill-builder-adaptive-enhancement-spec.md', '8fa6fae0625c5edd41cf8bca539a07e9d5fb1f1b90998feaf0be48814fa40a59')]:
        p = ROOT / 'docs/plan' / name
        actual = sha(p.read_bytes())
        hashes[name] = {'expected': expected, 'actual': actual, 'matches': actual == expected}
        if actual != expected:
            save(RUN / 'contract-hashes.json', hashes)
            raise ValueError('Contract changed; stop')
        (RUN / 'inputs').mkdir(exist_ok=True)
        (RUN / 'inputs' / name).write_bytes(p.read_bytes())
    save(RUN / 'contract-hashes.json', hashes)
    for name, p in [('target', TARGET), ('loaded-evaluator', LOADED), ('companion', ROOT / 'src/agents/skills/skill-builder')]:
        manifest = inventory(p, RUN / 'inputs' / name)
        save(RUN / (name + '-before.json'), manifest)
        print(name, manifest['file_count'], manifest['package_digest'], manifest['bytes'], manifest['exclusions'])
    prior = inventory(PRIOR)
    save(RUN / 'prior-evidence-before.json', prior)
    save(RUN / 'environment.json', {'time_utc': now(), 'platform': platform.platform(), 'python': sys.version, 'python_executable': sys.executable, 'codex': shutil.which('codex'), 'root': str(ROOT), 'loaded_evaluator': str(LOADED), 'target': str(TARGET), 'packages': {n: (importlib.metadata.version(n) if importlib.util.find_spec(n.replace('-', '_')) else None) for n in ['yaml','coverage','tiktoken']}})

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['preflight', 'exec', 'readback'])
    parser.add_argument('name', nargs='?')
    parser.add_argument('argv', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.action == 'preflight':
        preflight()
    elif args.action == 'exec':
        execute(args.name, args.argv)
    else:
        for name, p in [('target', TARGET), ('loaded-evaluator', LOADED), ('companion', ROOT / 'src/agents/skills/skill-builder'), ('prior-evidence', PRIOR)]:
            current = inventory(p)
            save(RUN / (name + '-after.json'), current)
            old = json.loads((RUN / (name + '-before.json')).read_text(encoding='utf-8'))
            print(name, current['package_digest'], 'UNCHANGED' if current['files'] == old['files'] else 'CHANGED')
