"""Bounded maintenance receipts; evidence only, never framework authority."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import stat
import subprocess
import sys

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[4]
PACKAGE = ROOT / 'src/agents/skills/skill-builder'
SPEC_NAMES = ('skill-builder-adaptive-enhancement-spec.md', 'skill-validator-adaptive-enhancement-spec.md', 'skill-builder-authoring-enhancement-spec.md', 'skill-builder-independent-qa-prompt.md')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def manifest(root, synthetic=False):
    rows, pending, total = [], [root], 0
    while pending:
        for path in sorted(pending.pop().iterdir()):
            rel = path.relative_to(root).as_posix()
            info = path.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
                raise ValueError('link/reparse point: ' + rel)
            if not synthetic and any(p.casefold() in {'.git', '.env', 'node_modules', '__pycache__', 'devforgeai_cli', '.venv', 'target', 'dist', 'build'} or 'backup' in p.casefold() for p in path.relative_to(root).parts):
                raise ValueError('excluded path: ' + rel)
            if stat.S_ISDIR(info.st_mode):
                pending.append(path)
                continue
            if not stat.S_ISREG(info.st_mode) or len(rows) >= 2000 or total + info.st_size > 32 * 1024 * 1024:
                raise ValueError('capture boundary: ' + rel)
            data = path.read_bytes()
            if len(data) != info.st_size:
                raise ValueError('source changed: ' + rel)
            total += len(data)
            rows.append({'path': rel, 'bytes': len(data), 'sha256': sha(data)})
    return sorted(rows, key=lambda row: row['path'])


def identity():
    rows = manifest(PACKAGE)
    digest = sha(json.dumps(rows, ensure_ascii=False, separators=(',', ':')).encode('utf-8'))
    return {'files': rows, 'package_digest': digest, 'specifications': {n: sha((ROOT / 'docs/plan' / n).read_bytes()) for n in SPEC_NAMES}}


def capture():
    value = identity()
    assert value['package_digest'] == '338c70995e72637e0ce84991be110d6a371ab6965faf4009d570156ea0e13cf2', value['package_digest']
    assert value['specifications'][SPEC_NAMES[0]] == '8fa6fae0625c5edd41cf8bca539a07e9d5fb1f1b90998feaf0be48814fa40a59'
    assert value['specifications'][SPEC_NAMES[1]] == 'f08a5f745235e969c8186731c187bdc5150d8f92cc8d140d0deb6812e7ecaf42'
    for row in value['files']:
        destination = RUN / 'source-before' / row['path']
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open('xb') as stream:
            stream.write((PACKAGE / row['path']).read_bytes())
    for name in SPEC_NAMES:
        destination = RUN / 'specifications' / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open('xb') as stream:
            stream.write((ROOT / 'docs/plan' / name).read_bytes())
    dump(RUN / 'initial-receipt.json', value)
    dump(RUN / 'environment.json', {'python': sys.version, 'executable': sys.executable, 'platform': platform.platform(), 'cwd': str(Path.cwd()), 'at': datetime.datetime.now(datetime.timezone.utc).isoformat()})
    dump(RUN / 'coverage-scope.json', {'denominator': 'All first-party executable Python lines in development skill-builder, including new helpers; no first-party exclusions.', 'platforms': ['Windows', 'Linux'], 'line_floor': 95, 'required_case_pass_floor': 95, 'branch': 'Reported separately', 'authority': 'Development evidence only'})
    print(json.dumps({'files': len(value['files']), 'digest': value['package_digest']}))


def command(label, argv):
    folder = RUN / 'commands' / label
    folder.mkdir(parents=True, exist_ok=False)
    before = identity()
    dump(folder / 'command.json', {'argv': argv, 'cwd': str(ROOT), 'timeout_seconds': 120, 'start': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'source_before': before})
    for script in RUN.glob('*.py'):
        (folder / script.name).write_bytes(script.read_bytes())
    try:
        result = subprocess.run(argv, cwd=ROOT, capture_output=True, timeout=120)
        code, out, err, timeout = result.returncode, result.stdout, result.stderr, False
    except subprocess.TimeoutExpired as exc:
        code, out, err, timeout = None, exc.stdout or b'', exc.stderr or b'', True
    (folder / 'stdout.txt').write_bytes(out)
    (folder / 'stderr.txt').write_bytes(err)
    dump(folder / 'result.json', {'exit': code, 'timeout': timeout, 'finish': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'source_after': identity(), 'source_unchanged': before == identity()})
    print(out.decode('utf-8', errors='replace'))
    print(err.decode('utf-8', errors='replace'))
    print('EXIT', code, 'TIMEOUT', timeout)
    return code if code is not None else 124


if __name__ == '__main__':
    if sys.argv[1] == 'capture':
        capture()
    else:
        sys.exit(command(sys.argv[1], sys.argv[2:]))
