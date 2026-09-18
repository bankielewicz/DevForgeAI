"""Reduce retained helper executions; this does not execute product or skill trials."""
import json
import hashlib
from pathlib import Path
import re
import sys


def sha(data):
    return hashlib.sha256(data).hexdigest()


def grade_execution(receipt, stderr, expected_count):
    if receipt.get('exit_code') != 0:
        raise ValueError('execution failed')
    summary = re.search(r'^Ran (\d+) tests? in ', stderr, re.MULTILINE)
    if not summary or int(summary.group(1)) != expected_count:
        raise ValueError('test count mismatch')
    if not re.search(r'^OK\s*$', stderr, re.MULTILINE):
        raise ValueError('suite did not pass')
    rows = re.findall(r'^(test_\S+ \([^\r\n]+\)) \.\.\. ([^\r\n]+)', stderr, re.MULTILINE)
    if len({name for name, _ in rows}) != len(rows):
        raise ValueError('duplicate case identifiers')
    if len(rows) != expected_count or any(state != 'ok' for _, state in rows):
        raise ValueError('case outcomes incomplete')
    return {'passed': len(rows), 'required': expected_count}


def bound_bytes(reference):
    path = Path(reference['path'])
    if not path.is_absolute() or '..' in path.parts:
        raise ValueError('invalid absolute reference')
    for p in [path, *path.parents]:
        if p.is_symlink() or (p.exists() and getattr(p.lstat(), 'st_file_attributes', 0) & 0x400):
            raise ValueError('link/reparse point')
    data = path.read_bytes()
    if sha(data) != reference['sha256']:
        raise ValueError('digest mismatch: ' + str(path))
    return data


def package_rows(root):
    pending, rows, total = [root], [], 0
    while pending:
        for p in sorted(pending.pop().iterdir()):
            if p.name.lower() in {'.git', '__pycache__', 'backup', 'backups', 'devforgeai_cli'} or 'backup' in p.name.lower():
                raise ValueError('excluded content prevents complete package binding')
            if p.is_symlink() or getattr(p.lstat(), 'st_file_attributes', 0) & 0x400:
                raise ValueError('link/reparse point')
            if p.is_dir():
                pending.append(p)
            elif p.is_file():
                data = p.read_bytes()
                total += len(data)
                if total > 32 * 1024 * 1024 or len(rows) >= 2000:
                    raise ValueError('package capture ceiling')
                rows.append({'path': p.relative_to(root).as_posix(), 'bytes': len(data), 'sha256': sha(data)})
            else:
                raise ValueError('special file')
    return sorted(rows, key=lambda row: row['path'])


def grade_coverage(data, expected):
    file = data['files'][expected['file']]
    s = file['summary']
    if s['excluded_lines'] != 0 or s['num_statements'] != expected['total_statements']:
        raise ValueError('coverage denominator/exclusion mismatch')
    if len(file['executed_lines']) != s['covered_lines'] or len(file['missing_lines']) + s['covered_lines'] != s['num_statements']:
        raise ValueError('coverage line accounting mismatch')
    if 100 * s['covered_lines'] < expected['minimum_line_percent'] * s['num_statements']:
        raise ValueError('coverage below required floor')
    return {'executed_lines': s['covered_lines'], 'total_lines': s['num_statements'],
            'line_percent': 100 * s['covered_lines'] / s['num_statements'],
            'covered_branch_arcs': s['covered_branches'], 'total_branch_arcs': s['num_branches']}


def run(manifest_path, expected_digest):
    manifest = json.loads(bound_bytes({'path': str(manifest_path), 'sha256': expected_digest}))
    artifacts = {}
    for row in manifest['artifacts']:
        if row['id'] in artifacts:
            raise ValueError('duplicate artifact identifier')
        artifacts[row['id']] = bound_bytes(row['reference'])
    if package_rows(Path(manifest['builder_root'])) != manifest['builder_files']:
        raise ValueError('builder package changed')
    expected = json.loads(artifacts['expected'])
    schema = json.loads(artifacts['result_schema'])
    import jsonschema
    scenarios = [json.loads(line) for line in artifacts['scenarios'].decode().splitlines() if line]
    if len({s['id'] for s in scenarios}) != len(scenarios) or set(expected) != {s['id'] for s in scenarios}:
        raise ValueError('scenario identity mismatch')
    results = []
    for case in scenarios:
        if case['kind'] == 'retained_unittest':
            details = grade_execution(json.loads(artifacts[case['receipt']]), artifacts[case['stderr']].decode('utf-8'), expected[case['id']]['required_count'])
        elif case['kind'] == 'retained_coverage':
            details = grade_coverage(json.loads(artifacts[case['coverage']]), expected[case['id']])
        else:
            raise ValueError('unknown scenario kind')
        row = {'schema_version': 'helper-evidence-result-v1', 'case_id': case['id'], 'status': 'PASS',
               'assessment_kind': 'retained_evidence_reduction', 'manifest_sha256': expected_digest,
               'details': details, 'framework_acceptance': 'NOT_EVALUATED'}
        jsonschema.validate(row, schema)
        results.append(row)
    # Emit only after all bindings and reductions succeed.
    return results


if __name__ == '__main__':
    try:
        for row in run(Path(sys.argv[1]).absolute(), sys.argv[2]):
            print(json.dumps(row))
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(json.dumps({'status': 'FAIL', 'assessment_kind': 'retained_evidence_reduction', 'error': str(exc)}))
        sys.exit(1)
