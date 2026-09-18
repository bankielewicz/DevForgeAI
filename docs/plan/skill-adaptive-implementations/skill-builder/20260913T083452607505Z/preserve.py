"""Bounded maintenance capture. Inspect before execution; never reads bindings."""
import hashlib
import json
import os
from pathlib import Path
import platform
import stat
import sys

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
EXCLUDED = {'.git', 'node_modules', '.venv', 'venv', 'target', 'dist', 'build', '__pycache__', 'devforgeai_cli', 'backups', 'backup'}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)

def capture(root, destination=None):
    rows, exclusions, pending, total = [], [], [root], 0
    if not root.exists():
        return {'absent': True}
    while pending:
        directory = pending.pop()
        entries = sorted(directory.iterdir())
        for path in entries:
            rel = path.relative_to(root).as_posix()
            info = path.lstat()
            if path.name.casefold() in EXCLUDED or 'backup' in path.name.casefold() or path.name.startswith('.env') or path.suffix in ('.pem', '.key') or rel.endswith('devforgeai/project-binding.json'):
                exclusions.append(rel)
                continue
            if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
                exclusions.append(rel + ' [link]')
                continue
            if stat.S_ISDIR(info.st_mode):
                pending.append(path)
                continue
            if not stat.S_ISREG(info.st_mode):
                raise ValueError('special file')
            total += info.st_size
            if len(rows) >= 2000 or total > 32 * 1024 * 1024:
                raise ValueError('capture ceiling')
            data = path.read_bytes()
            after = path.stat()
            if (info.st_size, info.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
                raise ValueError('source changed')
            rows.append({'path': rel, 'bytes': len(data), 'sha256': sha(data)})
            if destination:
                output = destination / rel
                output.parent.mkdir(parents=True, exist_ok=True)
                with output.open('xb') as stream:
                    stream.write(data)
    rows.sort(key=lambda row: row['path'])
    digest = sha(json.dumps(rows, ensure_ascii=False, separators=(',', ':')).encode())
    return {'files': rows, 'package_digest': digest, 'exclusions': exclusions}

if __name__ == '__main__':
    targets = {'builder': 'src/agents/skills/skill-builder', 'companion': 'src/agents/skills/skill-validator', 'operational-builder': '.agents/skills/skill-builder', 'operational-validator': '.agents/skills/skill-validator'}
    for name, relative in targets.items():
        result = capture(ROOT / relative, RUN / 'before' / name if name == 'builder' else None)
        save(RUN / (name + '-before.json'), result)
        print(name, result.get('package_digest'), len(result.get('files', [])))
    inputs = {}
    for relative in ['AGENTS.md', 'docs/plan/skill-builder-adaptive-enhancement-spec.md', 'docs/plan/skill-validator-adaptive-enhancement-spec.md', 'docs/plan/skill-builder-authoring-enhancement-spec.md']:
        source = ROOT / relative
        data = source.read_bytes()
        dest = RUN / 'inputs' / source.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open('xb') as stream:
            stream.write(data)
        inputs[relative] = sha(data)
    save(RUN / 'input-hashes.json', inputs)
    save(RUN / 'environment.json', {'platform': platform.platform(), 'python': sys.version, 'executable': sys.executable, 'cwd': str(ROOT), 'shell': 'PowerShell', 'agent': 'Codex GPT-6 primary', 'boundary': 'workspace-write; no OS isolation claim'})
