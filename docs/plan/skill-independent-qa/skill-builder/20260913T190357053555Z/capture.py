from pathlib import Path
import hashlib
import json
import os
import stat
import sys

RUN = Path(__file__).resolve().parent
SOURCE = RUN.parents[4] / 'src/agents/skills/skill-builder'

def manifest(root, copy_to=None):
    rows = []
    total = 0
    queue = [root]
    while queue:
        directory = queue.pop()
        entries = sorted(directory.iterdir(), key=lambda p: p.name)
        for path in entries:
            info = path.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
                raise ValueError('reparse/link: ' + str(path))
            relative = path.relative_to(root).as_posix()
            if any(p.casefold() in {'.git', '.venv', 'venv', 'node_modules', 'target', 'dist', 'build', '__pycache__', 'backups', 'devforgeai_cli'} or p.startswith('.env') for p in path.relative_to(root).parts):
                raise ValueError('unexpected excluded material: ' + relative)
            if stat.S_ISDIR(info.st_mode):
                queue.append(path)
                continue
            if not stat.S_ISREG(info.st_mode):
                raise ValueError('special: ' + relative)
            total += info.st_size
            if len(rows) >= 2000 or total > 32 * 1024 * 1024:
                raise ValueError('capture limit')
            data = path.read_bytes()
            assert len(data) == info.st_size
            rows.append({'path': relative, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
            if copy_to:
                target = copy_to / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
    rows.sort(key=lambda r: r['path'])
    digest = hashlib.sha256(json.dumps(rows, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
    return {'package_digest': digest, 'files': len(rows), 'bytes': total, 'manifest': rows}

if __name__ == '__main__':
    final = '--final' in sys.argv
    result = manifest(SOURCE, RUN / ('source-final/skill-builder' if final else 'source/skill-builder'))
    assert result['package_digest'] == ('ecb5f8056f18e1d9889de0c829a7e8e48a6feafe1b8f29bc09718d226eb20099' if final else '464acfdce47c7784062c488ad75f6b31adf303ba1f3cb12143ef76842ff6a926'), result
    (RUN / ('source-final-receipt.json' if final else 'source-receipt.json')).write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(result['package_digest'], result['files'], result['bytes'])
