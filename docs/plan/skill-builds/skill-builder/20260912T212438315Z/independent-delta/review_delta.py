"""Independent read-only comparison of the approved editorial candidate."""
import datetime
import difflib
import hashlib
import json
from pathlib import Path
import re
import stat

RUN = Path(__file__).resolve().parent.parent
PROJECT = RUN.parents[4]
REVISION = RUN / 'working' / 'revision'
ASSESSMENT = PROJECT / 'docs/plan/skill-validations/skill-builder/20260912T161842Z'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def read(path):
    for ancestor in (path, *path.parents):
        info = ancestor.lstat()
        assert not stat.S_ISLNK(info.st_mode) and not (getattr(info, 'st_file_attributes', 0) & 0x400), str(ancestor)
    return path.read_bytes()

def inventory(root):
    pending, rows = [root], []
    while pending:
        entries = sorted(pending.pop().iterdir())
        for entry in entries:
            assert not re.search(r'(^|[-_.])backups?($|[-_.])|devforgeai_cli', entry.name.lower()), str(entry)
            info = entry.lstat()
            assert not stat.S_ISLNK(info.st_mode) and not (getattr(info, 'st_file_attributes', 0) & 0x400), str(entry)
            if stat.S_ISDIR(info.st_mode):
                pending.append(entry)
            else:
                assert stat.S_ISREG(info.st_mode), str(entry)
                data = read(entry)
                rows.append({'path': entry.relative_to(root).as_posix(), 'bytes': len(data), 'sha256': sha(data)})
    return sorted(rows, key=lambda row: row['path'])

spec = read(ASSESSMENT / 'revision-spec.md')
assert sha(spec) == '9b8570392db9ed2128a71d820ba3710f58a000749db3f0ca0b780e33da28248c'
manifest_data = read(ASSESSMENT / 'source-manifest.json')
assert sha(manifest_data) == 'b6f1611978c00ec7a9898e01d93fe83a4f06bf4ad8a7d4a4f3931f9d421c81a6'
manifest = json.loads(manifest_data)
rows = {name: inventory(REVISION / name) for name in ('B', 'C', 'N')}
assert rows['B'] == rows['C'] == manifest['files']
assert all(len(value) == 36 for value in rows.values())
assert [row['path'] for row in rows['B']] == [row['path'] for row in rows['N']]
changed = [before['path'] for before, after in zip(rows['B'], rows['N']) if before != after]
assert changed == ['evals/build-manifest.json', 'references/evidence-format.md']
reference = 'references/evidence-format.md'
old = b'| Independent forward trials | `NOT_PERFORMED`, `PASSED`, `FAILED`; builder enhancements require the three actual trials in the evaluation reference. |'
new = b'| Independent forward trials | `NOT_PERFORMED`, `PASSED`, `FAILED`; builder enhancements require all applicable independent forward trials specified in [evaluation.md](evaluation.md#required-forward-trials-for-builder-enhancements). |'
assert new.replace(b'`', b'') in spec
before = read(REVISION / 'B' / reference)
after = read(REVISION / 'N' / reference)
assert before.count(old) == 1 and before.replace(old, new) == after
manifest_before = read(REVISION / 'B/evals/build-manifest.json')
manifest_after = read(REVISION / 'N/evals/build-manifest.json')
assert manifest_before.count(sha(before).encode()) == 1
assert manifest_before.replace(sha(before).encode(), sha(after).encode()) == manifest_after
delta = json.loads(read(RUN / 'candidate-delta.json'))
assert delta['changed_paths'] == changed and delta['before'] == rows['B']
results = [json.loads(line) for line in read(RUN / 'candidate-results.jsonl').splitlines()]
cases = [json.loads(line) for line in read(RUN / 'candidate-cases.jsonl').splitlines()]
assert len(results) == len(cases) == 3
assert {row['grader_id'] for row in results} == {'package_links', 'build_traceability_v2', 'revision_consistency_v2'}
assert all(row['profile'] == 'revision-spec-v2' and row['status'] == 'PASS' and row['expectation_met'] is True and row['error'] is None for row in results)
assert all(row['cases_sha256'] == sha(read(RUN / 'candidate-cases.jsonl')) for row in results)
evaluation = read(REVISION / 'N/references/evaluation.md')
assert evaluation == read(REVISION / 'B/references/evaluation.md')
section = evaluation.decode().split('## Required forward trials for builder enhancements', 1)[1].split('## Report results', 1)[0]
assert len(re.findall(r'^\d\. ', section, flags=re.M)) == 4
assert 'Separately evaluate routing' in section
observed = {'schema_version': '1', 'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'reviewer': '/root/origin_fidelity', 'spec_sha256': sha(spec), 'baseline_package_digest': manifest['package_digest'], 'candidate_package_digest': sha(json.dumps(rows['N'], ensure_ascii=False, separators=(',', ':')).encode()), 'file_count_each': 36, 'B_equals_C_equals_approved_snapshot': True, 'changed_paths': changed, 'exact_required_row_only': True, 'exact_corresponding_manifest_digest_only': True, 'four_family_and_separate_routing_byte_identical': True, 'delta_rows_match': True, 'candidate_results': [{key: row[key] for key in ('case_id', 'grader_id', 'profile', 'status', 'expected', 'expectation_met')} for row in results], 'evidence_digests': {name: sha(read(RUN / name)) for name in ('candidate-delta.json', 'candidate-results.jsonl', 'candidate-cases.jsonl')}, 'candidate_rows': rows['N'], 'diffs': {path: ''.join(difflib.unified_diff(read(REVISION / 'B' / path).decode().splitlines(True), read(REVISION / 'N' / path).decode().splitlines(True), fromfile='B/' + path, tofile='N/' + path)) for path in changed}, 'conclusion': 'No discrepancy in exact authorized editorial candidate delta.', 'limitations': ['Read-only candidate review; evaluator results inspected and case bytes bound, not re-executed.', 'No delivered-target readback, provenance publication, fresh skill validation or acceptance claim from this review.']}
print(json.dumps(observed, indent=2))
