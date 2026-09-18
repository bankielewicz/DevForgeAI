"""Seal and verify the completed QA evidence without modifying product or old evidence."""
import hashlib
import json
import os
import re
import stat
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent
PROJECT = Path('C:/Projects/DevForgeAI')
CANDIDATE = PROJECT / 'devforgeai/experiments/codex-worker-probe-logging-qa-fixes'
OLD = ROOT.parent / '20260917T023835Z-qa'
DEV = ROOT.parent / '20260917T102726Z-dev-qa-fixes'


def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def binding(path):
    return {'path': str(path), 'bytes': path.stat().st_size, 'sha256': sha(path)}


def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write(name, value):
    with (ROOT / name).open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=True)
        stream.write('\n')


def verify(items):
    for item in items:
        actual = binding(Path(item['path']))
        assert actual == {key: item[key] for key in ['path', 'bytes', 'sha256']}, item['path']


manifest_names = [
    'candidate-manifest.json', 'preserved-manifest.json', 'input-manifest.json',
    'specification-bindings.json', 'helper-manifest.json', 'binary-manifest.json',
    'independent-binary-manifest.json',
]
for name in manifest_names:
    verify(load(ROOT / name))
assert sha(DEV / 'handoff-manifest.json') == '1e4e0800a737f07d658a50383ccdf98c6aa5237c73675d2539ccb7689065f9f5'
assert sha(OLD / 'handoff-manifest.json') == '0c6949f4379e7c469643f34ad6d4b1f664f48177f8865d12dfedd7cbe901019e'
old_evidence_counts = []
for previous in [OLD, DEV]:
    evidence = load(previous / 'evidence-manifest.json')
    verify(evidence['files'])
    verify(evidence.get('binaries', []))
    old_evidence_counts.append({'root': str(previous), 'verified_regular_files': len(evidence['files']), 'verified_binaries': len(evidence.get('binaries', []))})
v2 = load(ROOT / 'cli-helper-v2-binding.json')
assert sha(Path(v2['Path'])) == v2['Hash'].lower()
matrix = load(ROOT / 'cli-matrix-plan-v2.json')
assert matrix['entries'] == load(ROOT / 'cli-matrix-plan.json')['entries']
assert matrix['script_sha256'] == sha(ROOT / 'cli_matrix_v2.py')
for path, digest in matrix['protected_seed_files'].items():
    assert sha(Path(path)) == digest, path

checkpoint = load(ROOT / 'checkpoint.json')
assert checkpoint['execution_status'] == 'COMPLETED' and checkpoint['verdict'] == 'PASS'
assert checkpoint['remaining_required_cases'] == [] and checkpoint['owned_pending_invocations'] == []
verify([checkpoint['report'], checkpoint['candidate_manifest'], checkpoint['input_manifest'], checkpoint['plan_binding'], checkpoint['specifications'], checkpoint['case_results'], checkpoint['attempt_index'], checkpoint['defect_lifecycle'], checkpoint['criterion_results']])
metrics = load(ROOT / 'metrics.json')
assert metrics['passed'] == metrics['required_cases'] == 178
assert metrics['unit_passed'] == metrics['unit_required'] == 49
assert (metrics['line_covered'], metrics['line_count']) == (3872, 4057)
assert sha(ROOT / 'coverage.json') == metrics['coverage_sha256']
assert len(load(ROOT / 'attempt-index.json')) == 23
assert not (ROOT / 'STOP.json').exists() and not (ROOT / 'qa-fix.md').exists()
cases = load(ROOT / 'case-results.json')
assert len(cases) == 178 and all(item['status'] == 'PASS' for item in cases)
case_ids = {item['id'] for item in cases}
criteria = load(ROOT / 'criterion-results.json')
assert len(criteria) == 21
for row in criteria:
    assert set(row['cases']) <= case_ids
    assert row['status'] == ('NOT_APPLICABLE' if not row['cases'] else 'PASS')
    for name in row['evidence']:
        assert (ROOT / name).is_file(), name
findings = load(ROOT / 'findings.json')
assert {item['id']: item['state'] for item in findings} == {'QA-LOG-01': 'VERIFIED_FIXED', 'QA-LOG-02': 'VERIFIED_FIXED'}
for item in findings:
    verify([item['candidate_manifest'], item['runtime_source'], item['rebuilt_probe']])
for item in load(ROOT / 'defect-lifecycle.json'):
    assert [transition['state'] for transition in item['transitions']] == ['OPEN', 'FIX_REPORTED', 'VERIFIED_FIXED']
    verify([transition['evidence'] for transition in item['transitions']])

report = (ROOT / 'qa-report.md').read_text(encoding='utf-8')
assert 'VERIFIED_FIXED' in report and 'NOT_EVALUATED' in report
assert '<project>' not in report and 'TODO' not in report
prompt = (ROOT / 'next-review-prompt.txt').read_text(encoding='utf-8')
assert prompt.rstrip() in report and str(CANDIDATE) in prompt
links = []
for destination in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)', re.sub(r'```.*?```', '', report, flags=re.DOTALL)):
    parts = urlsplit(destination.strip().strip('<>'))
    if parts.scheme or not parts.path:
        continue
    target = (ROOT / unquote(parts.path)).resolve()
    assert target.is_file(), destination
    links.append({'destination': destination, 'resolved': str(target), 'exists': True})
write('publication-review.json', {
    'timestamp_utc': datetime.now(timezone.utc).isoformat(),
    'report': binding(ROOT / 'qa-report.md'), 'criteria': len(criteria),
    'case_ids_verified': len(case_ids), 'local_links': links, 'broken_links': [],
    'lifecycle_bindings_verified': True, 'prior_evidence_verified': old_evidence_counts,
    'protected_seed_files_verified': len(matrix['protected_seed_files']), 'problems': [],
})

# Never traverse Windows reparse points, including owned fixture junctions.
excluded = {'evidence-manifest.json', 'handoff-manifest.json', 'final-readback.json'}
files, reparse_points = [], []
for current, directories, names in os.walk(ROOT, followlinks=False):
    base = Path(current)
    safe = []
    for name in sorted(directories):
        path = base / name
        if base == ROOT and name.endswith('-target'):
            continue
        if getattr(path.lstat(), 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT:
            reparse_points.append({'path': str(path), 'target': os.readlink(path), 'traversed': False})
        else:
            safe.append(name)
    directories[:] = safe
    for name in sorted(names):
        path = base / name
        if base == ROOT and name in excluded:
            continue
        if getattr(path.lstat(), 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT:
            reparse_points.append({'path': str(path), 'target': os.readlink(path), 'traversed': False})
            continue
        files.append(binding(path))

binaries = []
for name in ['build-target', 'coverage-target', 'independent-target', 'supplemental-target']:
    target = ROOT / name
    for current, directories, names in os.walk(target, followlinks=False):
        base = Path(current)
        directories[:] = sorted(child for child in directories if child != 'build' and not getattr((base / child).lstat(), 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT)
        for filename in sorted(names):
            path = base / filename
            if path.suffix.lower() == '.exe' and not getattr(path.lstat(), 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                binaries.append(binding(path))
write('evidence-manifest.json', {
    'timestamp_utc': datetime.now(timezone.utc).isoformat(),
    'scope': 'All regular retained evidence outside Cargo target directories; produced product/test executable identities separately bound. Reparse points recorded without traversal. Build-script executables and Cargo intermediates excluded.',
    'files': files, 'binaries': binaries, 'reparse_points': reparse_points,
    'excluded_self_and_final_bindings': sorted(excluded),
})

entry_names = [
    'qa-report.md', 'next-review-prompt.txt', 'checkpoint.json', 'checkpoint-before-execution.json',
    'plan.md', 'plan-binding.json', 'candidate-manifest.json', 'changed-files.json',
    'input-manifest.json', 'preserved-manifest.json', 'specification-bindings.json',
    'required-cases.json', 'case-results.json', 'criterion-results.json', 'findings.json',
    'defect-lifecycle.json', 'metrics.json', 'source-denominator.json', 'coverage.json',
    'coverage-analysis.json', 'package-results.json', 'original-defect-retest.json',
    'integrity.md', 'harness-gap-01.md', 'documentation-review.json', 'publication-review.json',
    'attempt-index.json', 'intake-verification.json', 'final-preservation.json',
    'helper-manifest.json', 'helper-provenance.json', 'binary-manifest.json',
    'independent-binary-manifest.json', 'cli-helper-v2-binding.json',
    'cli-matrix-plan.json', 'cli-matrix-plan-v2.json', 'rt-01-observations.json',
    'rt-02-observations.json', 'evidence-manifest.json',
]
manifest = {
    'qa_run': ROOT.name, 'intent': 'retest', 'project': str(PROJECT),
    'platform': 'Windows x64 / native C: / native PowerShell',
    'original_evidence_selection': str(ROOT.parent),
    'required_destination': str(ROOT), 'actual_destination': str(ROOT),
    'plan_readiness': 'READY', 'execution_status': 'COMPLETED', 'verdict': 'PASS',
    'candidate_root': str(CANDIDATE),
    'development_handoff': binding(DEV / 'handoff-manifest.json'),
    'original_qa_handoff': binding(OLD / 'handoff-manifest.json'),
    'defect_states': {'QA-LOG-01': 'VERIFIED_FIXED', 'QA-LOG-02': 'VERIFIED_FIXED'},
    'open_findings': [], 'remaining_required_cases': [],
    'native_codex': 'NOT_RUN', 'framework_acceptance': 'NOT_EVALUATED',
    'entries': {name: {'required_path': str(ROOT / name), **binding(ROOT / name)} for name in entry_names},
}
write('handoff-manifest.json', manifest)
actual = load(ROOT / 'handoff-manifest.json')
assert actual == manifest
for name, item in actual['entries'].items():
    assert item['required_path'] == item['path'] == str(ROOT / name)
    verify([item])
sealed = load(ROOT / 'evidence-manifest.json')
verify(sealed['files'])
verify(sealed['binaries'])
for name in manifest_names:
    verify(load(ROOT / name))
result = {
    'timestamp_utc': datetime.now(timezone.utc).isoformat(), 'status': 'READBACK_VERIFIED',
    'handoff_manifest': binding(ROOT / 'handoff-manifest.json'),
    'required_destination': str(ROOT), 'actual_destination': str(ROOT),
    'verified_handoff_entries': len(entry_names), 'verified_evidence_files': len(files),
    'verified_executables': len(binaries), 'untraversed_reparse_points': len(reparse_points),
    'candidate_files_unchanged': 68, 'preserved_source_files_unchanged': 183,
    'input_files_unchanged': 108, 'prior_evidence_unchanged': old_evidence_counts,
    'report_sha256': sha(ROOT / 'qa-report.md'), 'errors': [],
    'execution_status': 'COMPLETED', 'verdict': 'PASS',
    'defect_states': {'QA-LOG-01': 'VERIFIED_FIXED', 'QA-LOG-02': 'VERIFIED_FIXED'},
    'native_codex': 'NOT_RUN', 'framework_acceptance': 'NOT_EVALUATED',
}
write('final-readback.json', result)
assert load(ROOT / 'final-readback.json') == result
print(json.dumps(result, indent=2))
