"""Read and archive actual supplementary fixtures; do not alter prior evidence."""
from pathlib import Path
import hashlib
import json

base = Path(__file__).resolve().parent
root = Path(r'C:\Users\bryan\AppData\Local\Temp\meeting-actions-files-forward-e80c26780a8841b4b5d4ad3556985916')
expected = json.loads((base.parent / 'expected.json').read_text(encoding='utf-8'))
fixture = json.loads((base.parent / 'fixture.json').read_text(encoding='utf-8'))
hashes = {}
for source in root.rglob('*'):
    if source.is_file():
        data = source.read_bytes()
        relative = source.relative_to(root)
        target = base / 'actual-files' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        hashes[relative.as_posix()] = {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}
text = (root / 'résumé actions 東京.md').read_text(encoding='utf-8')
checks = {
    'selected_skill_same_bytes': hashes['meeting-actions/SKILL.md']['sha256'] == fixture['source_sha256'],
    'input_matches_locked_fixture_bytes': hashes['notes original.md']['sha256'] == fixture['input_sha256'],
    'Unicode_spaced_literal_output_path': (root / 'résumé actions 東京.md').is_file(),
    'table_columns_and_supported_row': text.splitlines() == ['| Action | Owner | Due date |', '| --- | --- | --- |', '| Publish the status update | Lena | Friday |'],
    'blocked_destination_is_still_directory': (root / 'blocked destination.md').is_dir(),
    'sentinel_matches_original_fixture': (root / 'blocked destination.md' / 'sentinel.txt').read_bytes() == (base.parent / 'files-001' / 'fixture-after' / 'blocked destination.md' / 'sentinel.txt').read_bytes(),
    'no_alternate_output': set(hashes) == {'notes original.md', 'résumé actions 東京.md', 'blocked destination.md/sentinel.txt', 'meeting-actions/SKILL.md'},
}
result = {'root': str(root), 'hashes': hashes, 'artifact_checks': checks, 'all_artifact_checks_pass': all(checks.values()), 'limits': 'Independent actual-file verification only. Delivery messages, attempted failure, and executor readback require separate command/conversation receipts.'}
(base / 'actual-file-verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=True, indent=2))
