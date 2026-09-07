"""One-time authorized scoped generation; not a validator or native test helper."""
from pathlib import Path
import hashlib
import json
import os

history = Path(__file__).resolve().parent
assignment = json.loads((history / 'refresh-assignment.json').read_text())
source = Path(assignment['source'])
destination = Path(assignment['destination'])

def digest(data):
    return hashlib.sha256(data).hexdigest()

def inventory(root):
    for parent in (root, *root.parents):
        if parent.is_symlink():
            raise RuntimeError('Symlink ancestor: ' + str(parent))
    result = {}
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            raise RuntimeError('Symlink: ' + str(path))
        if path.is_file():
            result[str(path.relative_to(root))] = digest(path.read_bytes())
    return result

before = json.loads(Path(assignment['before_installed_manifest']).read_text())
after = json.loads(Path(assignment['expected_installed_manifest']).read_text())
source_manifest = json.loads(Path(assignment['source_manifest']).read_text())
if inventory(source) != source_manifest:
    raise RuntimeError('Canonical source collision')
if inventory(destination) != before:
    raise RuntimeError('Installed destination collision')
if set(before) - set(after):
    raise RuntimeError('Unassigned removal; refusing refresh')

with (history / 'refresh-execution.jsonl').open('x') as journal:
    def record(value):
        journal.write(json.dumps(value) + '\n')
        journal.flush()
    record({'event': 'preflight', 'source_manifest': assignment['source_manifest'], 'installed_before': assignment['before_installed_manifest'], 'changed_files': assignment['changed_files']})
    for relative in assignment['changed_files']:
        data = (source / relative).read_bytes()
        if digest(data) != source_manifest[relative]:
            raise RuntimeError('Source changed before copy: ' + relative)
        target = destination / relative
        for parent in (target, *target.parents):
            if parent.is_symlink():
                raise RuntimeError('Destination symlink: ' + str(parent))
        target.parent.mkdir(parents=True, exist_ok=True)
        if relative in before:
            fd = os.open(target, os.O_RDWR | os.O_NOFOLLOW)
            with os.fdopen(fd, 'r+b') as stream:
                if digest(stream.read()) != before[relative]:
                    raise RuntimeError('Concurrent installed edit: ' + relative)
                stream.seek(0)
                stream.write(data)
                stream.truncate()
                stream.flush()
                os.fsync(stream.fileno())
        else:
            with target.open('xb') as stream:
                stream.write(data)
        if target.read_bytes() != data:
            raise RuntimeError('Installed readback mismatch: ' + relative)
        record({'event': 'refreshed', 'path': str(target), 'sha256': after[relative]})
    observed = inventory(destination)
    if observed != after or inventory(source) != source_manifest:
        raise RuntimeError('Final source or installed collision; preserve partial refresh')
    with (history / 'installed-after-manifest.json').open('x') as stream:
        json.dump(observed, stream, indent=2)
        stream.write('\n')
    record({'event': 'refresh_complete', 'runtime_files': len(observed), 'changed_files': len(assignment['changed_files']), 'validation_status': 'NOT_PERFORMED', 'hook_status': 'DESIGN_ONLY'})
print('Refreshed', len(assignment['changed_files']), 'validator files;', len(after), 'runtime files. No hooks or sibling writes.')
