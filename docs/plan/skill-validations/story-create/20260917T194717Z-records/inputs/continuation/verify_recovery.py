"""Independent raw-byte checks for the completed synthetic truncation case."""
import hashlib
import json
from pathlib import Path

from prepare_continuation import RUN, put, ref

case = RUN / 'trials/G03'
expected = json.loads((case / 'expected.json').read_bytes())
before = Path(expected['fault']['retained_partial']['path'])
after = case / 'project/backlog/STORY-010.story.md'
prefix = before.read_bytes()
assert len(prefix) == expected['fault']['partial_bytes']
assert hashlib.sha256(prefix).hexdigest() == expected['fault']['partial_sha256']
assert after.read_bytes().startswith(prefix)
unchanged = []
for row in expected['fixture_inputs']:
    path = Path(row['path'])
    if path == after:
        continue
    assert ref(path)['sha256'] == row['sha256'], str(path)
    unchanged.append(ref(path))
assert sorted(p.name for p in (case / 'project/backlog').glob('*.story.md')) == ['STORY-010.story.md']
assert not (case / 'project/docs/restore-guide.md').exists()
put(case / 'recovery-byte-check.json', {'schema_version': 'story-recovery-byte-check-v1', 'result': 'MATCH', 'original_prefix_bytes': len(prefix), 'original_prefix': ref(before), 'completed_story': ref(after), 'other_original_files_unchanged': unchanged, 'same_path_and_id_only': True, 'future_guide_absent': True, 'limitation': 'Independent persisted-byte observations for this declared synthetic truncation only.'})
print(json.dumps({'result': 'MATCH', 'prefix_bytes': len(prefix), 'unchanged_other_files': len(unchanged), 'story_sha256': ref(after)['sha256']}))
