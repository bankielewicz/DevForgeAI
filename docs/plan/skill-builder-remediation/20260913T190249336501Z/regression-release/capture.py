"""Audit-owned no-follow bounded capture. No skill code imported."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import stat
import sys

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[4]
EXCLUDED = {'.git', 'node_modules', '.venv', 'venv', 'target', 'dist', 'build', '__pycache__', 'backups', 'backup', 'devforgeai_cli'}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def inventory(root):
    rows, omissions = [], []
    def visit(directory):
        entries = sorted(os.scandir(directory), key=lambda e: e.name)
        for entry in entries:
            p = Path(entry.path)
            rel = p.relative_to(root).as_posix()
            st = entry.stat(follow_symlinks=False)
            if st.st_file_attributes & 0x400 if hasattr(st, 'st_file_attributes') else stat.S_ISLNK(st.st_mode):
                raise ValueError('link/reparse rejected: ' + str(p))
            if entry.name.lower() in EXCLUDED or entry.name.lower().startswith('.env') or entry.name.lower().endswith(('.pem', '.key', '.pfx')) or entry.name in {'id_rsa', 'id_ed25519', 'project-binding.json'}:
                omissions.append({'path': rel, 'reason': 'excluded before read'})
                continue
            if stat.S_ISDIR(st.st_mode):
                visit(p)
            elif stat.S_ISREG(st.st_mode):
                if len(rows) + 1 > 2000 or sum(r['bytes'] for r in rows) + st.st_size > 32 * 1024 * 1024:
                    raise ValueError('capture limit: ' + str(root))
                data = p.read_bytes()
                rows.append({'path': rel, 'bytes': len(data), 'sha256': sha(data)})
            else:
                raise ValueError('special file: ' + str(p))
    visit(root)
    return sorted(rows, key=lambda r: r['path']), omissions

def digest(rows):
    return sha(json.dumps(rows, ensure_ascii=False, separators=(',', ':')).encode('utf-8'))

def save(name, value):
    (RUN / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

def main():
    target = ROOT / 'src/agents/skills/skill-builder'
    rows, omissions = inventory(target)
    phase = 'final' if '--final' in sys.argv else 'initial'
    save(phase + '-manifest.json', rows)
    specs = {}
    for name in ('skill-builder-adaptive-enhancement-spec.md', 'skill-validator-adaptive-enhancement-spec.md', 'skill-builder-independent-qa-prompt.md', 'skill-builder-authoring-enhancement-spec.md'):
        source = ROOT / 'docs/plan' / name
        specs[name] = sha(source.read_bytes())
        if phase == 'initial':
            dest = RUN / 'inputs' / name
            dest.parent.mkdir(exist_ok=True)
            dest.write_bytes(source.read_bytes())
    if phase == 'initial':
        for row in rows:
            dest = RUN / 'snapshot' / row['path']
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes((target / row['path']).read_bytes())
        (RUN / 'inputs/AGENTS.md').write_bytes((ROOT / 'AGENTS.md').read_bytes())
    result = {'phase': phase, 'at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'target': str(target), 'files': len(rows), 'bytes': sum(r['bytes'] for r in rows), 'package_digest': digest(rows), 'omissions': omissions, 'spec_hashes': specs, 'python': sys.version, 'executable': sys.executable, 'os': platform.platform(), 'capture_limits': {'files': 2000, 'bytes': 33554432}, 'preservation_scope': 'Selected builder exact bytes and selected input specifications. Excluded packages not read or executed; no claims of independent full inventory of those packages.'}
    if phase == 'final':
        result['source_unchanged'] = rows == json.loads((RUN / 'initial-manifest.json').read_text(encoding='utf-8'))
    save(phase + '-receipt.json', result)
    print(json.dumps(result, indent=2))
    print('\n'.join(f"{r['path']} {r['bytes']}" for r in rows))

if __name__ == '__main__':
    main()
