"""Read-only exact-path, protected-byte and JSONL evidence reference audit."""
import hashlib
import json
from pathlib import Path
import re
import sys
RUN = Path(__file__).resolve().parent
sys.path.insert(0, str(RUN / 'bundle'))
import graders


def audit(name):
    base = RUN / 'trials' / name
    plan = graders.load((base / 'plan.json').read_bytes())
    project = Path(plan['permitted_write_root'])
    attempt_paths = sorted(base.glob('attempt-*/result.json'))
    if not attempt_paths:
        return {'trial_id': name, 'status': 'NOT_RUN', 'reason': 'No completed attempt receipt.'}
    result = graders.load(attempt_paths[-1].read_bytes())
    effects = graders.load((attempt_paths[-1].parent / 'effects.json').read_bytes())
    rows = graders.load((attempt_paths[-1].parent / 'after.json').read_bytes())['files']
    report = {'trial_id': name, 'attempts': [p.parent.name for p in attempt_paths], 'termination': result['termination'],
              'exit_status': result['exit_status'], 'immutable_changes': effects['immutable_changes'],
              'selected_evidence_value': plan['selected_evidence_value'], 'selected_root_is_directory': (project / plan['selected_evidence_value']).is_dir(),
              'receipt_count': 0, 'references_checked': 0, 'unsupported_rows': [], 'problems': [], 'receipts': []}
    for row in rows:
        rel = row['path']
        if not rel.endswith('.jsonl') or rel.startswith(('trial-skill/', '.trial-output/')):
            continue
        path = graders.safe_file(project, rel)
        for number, line in enumerate(path.read_bytes().splitlines(), 1):
            value = graders.load(line)
            if not isinstance(value, dict) or not {'command', 'result'} <= value.keys():
                report['unsupported_rows'].append([rel, number])
                continue
            report['receipt_count'] += 1
            report['receipts'].append({'path': rel, 'line': number, 'attempt_id': value.get('attempt_id'), 'stage': value.get('stage'), 'result': value['result'], 'exit_code': value.get('exit_code')})
            needed = {'attempt_id','working_directory','started_at','ended_at','stdout','stderr','candidate'}
            missing = sorted(needed - value.keys())
            if missing:
                report['problems'].append({'receipt': rel, 'line': number, 'missing_fields': missing})
            refs = []
            def visit(item):
                if isinstance(item, dict):
                    if 'path' in item and 'sha256' in item:
                        refs.append((item['path'], item['sha256']))
                    if item.get('manifest_path') and item.get('manifest_sha256'):
                        refs.append((item['manifest_path'], item['manifest_sha256']))
                    for child in item.values():
                        visit(child)
                elif isinstance(item, list):
                    for child in item:
                        visit(child)
            visit(value)
            for raw, expected in refs:
                if not isinstance(expected, str) or not re.fullmatch('[0-9a-fA-F]{64}', expected):
                    report['problems'].append({'receipt': rel, 'line': number, 'reason': 'Invalid digest'})
                    continue
                candidates = {(project / raw).absolute(), (path.parent / raw).absolute()}
                candidates = {p for p in candidates if p.is_relative_to(project) and p.is_file()}
                matched = [p for p in candidates if graders.sha(graders.safe_file(project, p.relative_to(project).as_posix()).read_bytes()) == expected.lower()]
                if len(matched) != 1:
                    report['problems'].append({'receipt': rel, 'line': number, 'reference': raw, 'matching_candidates': len(matched)})
                else:
                    report['references_checked'] += 1
            if value['result'] == 'PASS' and value.get('exit_code') != 0:
                report['problems'].append({'receipt': rel, 'line': number, 'reason': 'PASS without observed exit0'})
    return report


if __name__ == '__main__':
    names = sys.argv[1:] or [p['trial_id'] for p in graders.load((RUN / 'native-plan.json').read_bytes())['trials']]
    print(json.dumps([audit(name) for name in names], ensure_ascii=False, indent=2))
