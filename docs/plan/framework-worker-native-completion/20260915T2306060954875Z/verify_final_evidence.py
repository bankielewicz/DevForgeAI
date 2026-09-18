"""Read retained evidence only; never run tests or issue acceptance."""
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
WORK = ROOT.parents[3]
QA = WORK / 'docs/plan/framework-worker-native-completion-qa/20260915T2325371896643Z'
PACKAGE = WORK / 'devforgeai/experiments/codex-worker-probe'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def save(name, value):
    (ROOT / name).write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


errors = []
receipts = []
for label in ['03-full-tests', '04-policy-oracle', '05-format', '06-clippy', '08a-coverage']:
    directory = QA / label
    receipt = read(directory / 'receipt.json')
    stream_matches = {}
    for stream in ['stdout', 'stderr']:
        path = directory / (stream + '.bin')
        matches = digest(path) == receipt[stream + '_sha256'] and path.stat().st_size == receipt[stream + '_bytes']
        stream_matches[stream] = matches
        if not matches:
            errors.append(label + ':' + stream)
    receipts.append({'label': label, 'native_exit_code': receipt['native_exit_code'],
                     'duration_seconds': receipt['duration_monotonic_ns'] / 1_000_000_000,
                     'candidate_unchanged': receipt['candidate_unchanged'],
                     'streams_match': stream_matches, 'receipt_sha256': digest(directory / 'receipt.json')})
    if receipt['native_exit_code'] != 0 or not receipt['candidate_unchanged']:
        errors.append(label + ':receipt')

coverage_path = QA / '08a-coverage/coverage.json'
coverage = read(coverage_path)
declared = {str(Path(e['path']).resolve()).casefold(): e for e in read(ROOT / 'source-denominator.json')['source_files']}
files = []
excluded = []
seen = set()
for dataset in coverage['data']:
    for entry in dataset['files']:
        path = Path(entry['filename']).resolve()
        key = str(path).casefold()
        if key not in declared:
            excluded.append(str(path))
            continue
        if key in seen:
            errors.append('duplicate coverage source:' + str(path))
        seen.add(key)
        summary = entry['summary']
        files.append({'path': str(path), 'lines': summary['lines'], 'branches': summary.get('branches')})

covered = sum(e['lines']['covered'] for e in files)
count = sum(e['lines']['count'] for e in files)
missing = [entry['path'] for key, entry in declared.items() if key not in seen]
if any(Path(path).name != 'lib.rs' for path in missing):
    errors.append('missing executable source coverage')
if (covered, count) != (2852, 3103):
    errors.append('coverage differs from independent QA measurement')

output = (QA / '03-full-tests/stdout.bin').read_text(encoding='utf-8')
test_results = re.findall(r'test result: \w+\. (\d+) passed; (\d+) failed; (\d+) ignored;', output)
totals = {name: sum(int(row[index]) for row in test_results) for index, name in enumerate(['passed', 'failed', 'ignored'])}
if totals != {'passed': 89, 'failed': 0, 'ignored': 0}:
    errors.append('test summary mismatch')

result = {'kind': 'retained-evidence-readback-only', 'candidate_manifest_sha256': digest(ROOT / 'candidate-manifest.json'),
          'qa_root': str(QA), 'receipts': receipts, 'rust_test_functions': totals,
          'coverage': {'raw_path': str(coverage_path), 'raw_sha256': digest(coverage_path), 'covered_lines': covered,
                       'executable_lines': count, 'percent': 100 * covered / count, 'meets_95_percent': covered * 100 >= count * 95,
                       'files': files, 'declared_files_without_reported_executable_lines': missing,
                       'excluded_resolved_paths': sorted(set(excluded))}, 'errors': errors}
save('qa-evidence-readback.json', result)
print(json.dumps({'errors': errors, 'test_functions': totals, 'covered_lines': covered, 'executable_lines': count,
                  'percent': 100 * covered / count, 'meets_95_percent': covered * 100 >= count * 95}))
raise SystemExit(bool(errors))
