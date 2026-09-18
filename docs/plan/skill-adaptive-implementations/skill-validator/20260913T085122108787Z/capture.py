"""Bounded maintenance capture; reviewed before execution. Never captures bindings."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import stat
import sys

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
EXCLUDE = {'.git', 'node_modules', '.venv', 'venv', 'target', 'dist', 'build', '__pycache__', 'devforgeai_cli'}

def digest(data):
    return hashlib.sha256(data).hexdigest()

def scan(root, copy=None):
    rows, exclusions, pending = [], [], [root]
    total = 0
    if not root.exists():
        return {'root': str(root), 'absent': True, 'files': []}
    while pending:
        current = pending.pop()
        for path in sorted(current.iterdir()):
            rel = path.relative_to(root).as_posix()
            info = path.lstat()
            if path == RUN or path.name in EXCLUDE or 'backup' in path.name.lower() or path.suffix in ('.bak', '.pem', '.key') or path.name.startswith('.env') or ('devforgeai' in path.parts and '.agents' in path.parts):
                exclusions.append(rel)
                continue
            if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
                exclusions.append(rel)
                continue
            if stat.S_ISDIR(info.st_mode):
                pending.append(path)
            elif stat.S_ISREG(info.st_mode):
                total += info.st_size
                if len(rows) >= 2000 or total > 32 * 1024 * 1024:
                    raise ValueError('capture ceiling: ' + str(root))
                data = path.read_bytes()
                rows.append({'path': rel, 'bytes': len(data), 'sha256': digest(data)})
                if copy:
                    target = copy / rel
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(data)
            else:
                raise ValueError('special file: ' + str(path))
    rows.sort(key=lambda x: x['path'])
    return {'root': str(root), 'files': rows, 'excluded': exclusions, 'package_digest': digest(json.dumps(rows, ensure_ascii=False, separators=(',', ':')).encode())}

def save(name, value):
    path = RUN / name
    if path.exists():
        raise ValueError('no overwrite: ' + str(path))
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')

if __name__ == '__main__':
    mode = sys.argv[1]
    targets = {'validator': ROOT / 'src/agents/skills/skill-validator', 'builder': ROOT / 'src/agents/skills/skill-builder', 'operational-agents': ROOT / '.agents', 'operational-claude': ROOT / '.claude', 'operational-codex': ROOT / '.codex'}
    for name, root in targets.items():
        save(mode + '-' + name + '.json', scan(root, RUN / 'before-source' if mode == 'before' and name == 'validator' else None))
    if mode == 'before':
        (RUN / 'inputs').mkdir()
        for name in ('skill-validator-adaptive-enhancement-spec.md', 'skill-builder-adaptive-enhancement-spec.md'):
            shutil.copyfile(ROOT / 'docs/plan' / name, RUN / 'inputs' / name)
        shutil.copyfile(ROOT / 'AGENTS.md', RUN / 'inputs/AGENTS.md')
        save('environment.json', {'platform': platform.platform(), 'python': sys.version, 'executable': sys.executable, 'cwd': str(ROOT), 'utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'shell': 'PowerShell', 'codex': shutil.which('codex'), 'boundary': 'workspace-write; no claim of child OS isolation'})
    print(json.dumps({'mode': mode, 'run': str(RUN), 'targets': list(targets)}))
