"""Read-only exact origin/snapshot verification for independent fidelity review."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import stat

ROOT = Path(__file__).resolve().parent.parent
INPUTS = ROOT / 'origin-inputs'
ASSESSMENT = ROOT.parents[2] / 'skill-validations' / 'skill-builder' / '20260912T161842Z'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def measure(path):
    for ancestor in (path, *path.parents):
        info = ancestor.lstat()
        assert not stat.S_ISLNK(info.st_mode) and not (getattr(info, 'st_file_attributes', 0) & 0x400), str(ancestor)
    data = path.read_bytes()
    return {'path': str(path), 'bytes': len(data), 'sha256': sha(data)}

def inventory(root):
    pending = [root]
    rows = []
    while pending:
        directory = pending.pop()
        entries = sorted(directory.iterdir())
        for entry in entries:
            assert not re.search(r'(^|[-_.])backups?($|[-_.])|devforgeai_cli', entry.name.lower()), str(entry)
            info = entry.lstat()
            assert not stat.S_ISLNK(info.st_mode) and not (getattr(info, 'st_file_attributes', 0) & 0x400), str(entry)
            if stat.S_ISDIR(info.st_mode):
                pending.append(entry)
            else:
                assert stat.S_ISREG(info.st_mode), str(entry)
                row = measure(entry)
                row['path'] = entry.relative_to(root).as_posix()
                rows.append(row)
    rows.sort(key=lambda item: item['path'])
    assert len(rows) <= 2000 and sum(row['bytes'] for row in rows) <= 32 * 1024 * 1024
    return rows

manifest_path = INPUTS / 'source-manifest.json'
manifest = json.loads(manifest_path.read_bytes())
rows = inventory(INPUTS / 'observed-package')
assert rows == manifest['files'] and len(rows) == 36
digest = sha(json.dumps(rows, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode('utf-8'))
assert digest == manifest['package_digest'] == 'dab87685715689251365514f5c0f3df5c2a9b66c5367bf065ad62c903e8dfca3'
manifest_measure = measure(manifest_path)
assert manifest_measure['sha256'] == 'b6f1611978c00ec7a9898e01d93fe83a4f06bf4ad8a7d4a4f3931f9d421c81a6'
origin_record = json.loads((ASSESSMENT / 'origin-record.json').read_bytes())
specs = []
for ref in [origin_record['specification'], *origin_record['additional_specifications']]:
    row = measure(INPUTS / 'specs' / Path(ref['path']).name)
    assert row['sha256'] == ref['sha256']
    assert row['sha256'] == measure(ASSESSMENT / ref['path'])['sha256']
    specs.append(row)
print(json.dumps({'schema_version': '1', 'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'origin': measure(INPUTS / 'origin-spec.md'), 'manifest': manifest_measure, 'snapshot_file_count': len(rows), 'snapshot_package_digest': digest, 'snapshot_rows': rows, 'retained_specifications': specs, 'snapshot_exact_match': True, 'specifications_match_selected_assessment': True, 'limitations': ['Static independent fidelity review and rehash only; no adoption, workflow trial, generated provenance, quality acceptance, native activation, or target mutation.']}, indent=2))
