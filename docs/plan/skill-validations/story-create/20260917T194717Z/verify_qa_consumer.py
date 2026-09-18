"""Check the real consumer, its current product inputs and finalized evidence bytes."""
import json
from pathlib import Path
import re

from prepare_continuation import RUN, put, ref

case = RUN / 'trials/N13'
project = case / 'project'
evidence = project / 'evidence/qa/run-20260917T203658Z'
receipt = json.loads((case / 'attempt-001/result.json').read_bytes())
assert receipt['outcome'] == 'PASS' and receipt['cleanup'] == 'VERIFIED' and receipt['input_unchanged']
expected = json.loads((case / 'expected.json').read_bytes())
for pair in expected['source_handoff']:
    for item in pair.values():
        assert ref(Path(item['path']))['sha256'] == item['sha256']
    assert Path(pair['producer']['path']).read_bytes() == Path(pair['consumer']['path']).read_bytes()
baseline = json.loads((evidence / 'supplied-files.before.json').read_bytes())
assert len(baseline['files']) == 14
for item in baseline['files']:
    path = project / item['path']
    assert path.stat().st_size == item['bytes'] and ref(path)['sha256'] == item['sha256']
manifest = json.loads((evidence / 'handoff-manifest.json').read_bytes())
assert manifest['qa_verdict'] == 'PASS' and manifest['framework_acceptance'] == 'NOT_EVALUATED'
for item in manifest['artifacts']:
    path = (project / item['path']).resolve()
    assert path.is_relative_to(project.resolve())
    assert path.stat().st_size == item['bytes'] and ref(path)['sha256'] == item['sha256']
    assert item['readback'] == 'VERIFIED'
results = json.loads((evidence / 'review-results.json').read_bytes())
assert results['qa_verdict'] == 'PASS' and len(results['cases']) == 6
assert all(row['status'] == 'PASS' for row in results['cases'])
assert results['counts']['satisfied_acceptance_criteria'] == results['counts']['selected_acceptance_criteria'] == 5
assert not results['findings'] and not results['open_gaps']
after = json.loads((evidence / 'supplied-files.after.json').read_bytes())
assert not after['changed_supplied_files'] and not after['additions_outside_evidence'] and not after['reparse_points']
checkpoint = json.loads((evidence / 'checkpoint.json').read_bytes())
assert not checkpoint['remaining_required_checks'] and not checkpoint['open_defects'] and not checkpoint['open_gaps']
report = project / 'evidence/qa/qa-report.md'
links = []
for match in re.finditer(r'\[[^\]]+\]\(([^)]+)\)', report.read_text(encoding='utf-8')):
    target = (report.parent / match[1]).resolve()
    assert target.is_relative_to(project.resolve()) and target.exists(), match[1]
    links.append(match[1])
put(case / 'consumer-integrity.json', {'schema_version': 'story-consumer-integrity-v1', 'result': 'MATCH', 'actual_producer_files_unchanged': len(expected['source_handoff']), 'supplied_files_unchanged': 14, 'qa_evidence_artifacts_verified': len(manifest['artifacts']), 'documentation_cases_passed': 6, 'selected_acceptance_criteria_satisfied': 5, 'report': ref(report), 'manifest': ref(evidence / 'handoff-manifest.json'), 'local_report_links': links, 'limitation': 'Byte and receipt checks supplement primary source/content review; no framework acceptance.'})
print(json.dumps({'result': 'MATCH', 'producer_files': 5, 'supplied_files': 14, 'qa_artifacts': len(manifest['artifacts']), 'qa_cases': 6, 'local_links': len(links)}))
