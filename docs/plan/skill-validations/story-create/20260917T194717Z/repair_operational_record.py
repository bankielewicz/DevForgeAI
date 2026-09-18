"""Preserve the rejected index and encode verified operational snapshots relatively."""
import datetime
import hashlib
import json
from pathlib import Path

from prepare_continuation import RUN, put, ref

root = RUN.with_name(RUN.name + '-records')
path = root / 'operational-readback.json'
before = path.read_bytes()
retained = RUN / 'record-repair-001/operational-readback.before.json'
retained.parent.mkdir(parents=True, exist_ok=True)
with retained.open('xb') as stream:
    stream.write(before)
record = json.loads(before)
rows = []
for index, item in enumerate(record['files']):
    original = Path(item['path'])
    data = original.read_bytes()
    assert hashlib.sha256(data).hexdigest() == item['sha256']
    captured = root / 'inputs/operational-capture' / f'{index:03}' / original.name
    captured.parent.mkdir(parents=True, exist_ok=True)
    with captured.open('xb') as stream:
        stream.write(data)
    assert captured.read_bytes() == original.read_bytes()
    rows.append({'path': captured.relative_to(root).as_posix(), 'sha256': item['sha256'], 'bytes': len(data), 'original_path': str(original)})
record.update(files=rows, observed_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
path.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
put(RUN / 'record-repair-001/repair.json', {'schema_version': 'story-record-assembly-correction-v1', 'rejected_record': ref(retained), 'corrected_record': ref(path), 'originals_and_copies_verified': len(rows), 'reason': 'Legacy record reader requires normalized relative file references. Original absolute host locations now use informational original_path, with actual snapshot bytes captured under inputs/operational-capture. No target or operational bytes changed.', 'retained_failure': ref(RUN / 'legacy-records-001.stdout.txt')})
with (root / 'command-log.md').open('a', encoding='utf-8') as stream:
    stream.write('\nFinal legacy reader attempt 001 rejected 76 absolute references in the newly assembled operational-readback index. The index was retained before correction; all 76 live originals were rechecked and copied into relative evidence paths, with original_path retained separately. Adaptive reader 001 passed. Subsequent reader results are retained without overwriting the initial mismatch. This was a record-shape assembly error, not a target behavior defect.\n')
print(json.dumps({'result': 'CORRECTED', 'operational_originals_and_copies_verified': len(rows), 'prior_record_retained': str(retained)}))
