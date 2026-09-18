"""Retain byte-bound intake observations; no package writes."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import stat

ROOT = Path('C:/Projects/DevForgeAI')
RUN = Path(__file__).resolve().parent
PACKET = ROOT / 'docs/plan/skill-validations/skill-builder/20260912T161842Z'
TARGET = ROOT / 'src/agents/skills/skill-builder'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def capture(root):
    rows, excluded = [], []
    for ancestor in [root, *root.parents]:
        info = ancestor.lstat()
        assert not (stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400), str(ancestor)
    pending = [root]
    while pending:
        directory = pending.pop()
        for item in sorted(directory.iterdir()):
            info = item.lstat()
            relative = item.relative_to(root).as_posix()
            if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
                excluded.append({'path': relative, 'reason': 'link/reparse point'})
            elif item.name.lower() in {'backup', 'backups', 'devforgeai_cli'}:
                excluded.append({'path': relative, 'reason': 'excluded boundary'})
            elif stat.S_ISDIR(info.st_mode):
                pending.append(item)
            elif stat.S_ISREG(info.st_mode):
                assert len(rows) < 2000 and sum(r['bytes'] for r in rows) + info.st_size <= 32 * 1024 * 1024
                data = item.read_bytes()
                rows.append({'path': relative, 'bytes': len(data), 'sha256': sha(data)})
            else:
                raise ValueError('special file: ' + relative)
    return sorted(rows, key=lambda r: r['path']), excluded

if __name__ == '__main__':
    expected = {'revision-spec.md': '9b8570392db9ed2128a71d820ba3710f58a000749db3f0ca0b780e33da28248c', 'source-manifest.json': 'b6f1611978c00ec7a9898e01d93fe83a4f06bf4ad8a7d4a4f3931f9d421c81a6'}
    inputs = {name: {'expected': digest, 'actual': sha((PACKET / name).read_bytes())} for name, digest in expected.items()}
    recorded = json.loads((PACKET / 'source-manifest.json').read_bytes())
    current, excluded = capture(TARGET)
    before = {r['path']: r for r in recorded['files']}
    after = {r['path']: r for r in current}
    differences = [{'path': path, 'recorded': before.get(path), 'current': after.get(path)} for path in sorted(before.keys() | after.keys()) if before.get(path) != after.get(path)]
    result = {'schema_version': '1', 'timestamp': dt.datetime.now(dt.timezone.utc).isoformat(), 'target_root': str(TARGET), 'inputs': inputs, 'recorded_package_digest': recorded['package_digest'], 'files': current, 'excluded_boundaries': excluded, 'differences': differences, 'outcome': 'UNCHANGED' if not differences and not excluded and all(r['expected'] == r['actual'] for r in inputs.values()) else 'SOURCE_CHANGED'}
    output = RUN / 'preflight.json'
    with output.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps({'outcome': result['outcome'], 'file_count': len(current), 'differences': differences, 'inputs': inputs}, indent=2))
