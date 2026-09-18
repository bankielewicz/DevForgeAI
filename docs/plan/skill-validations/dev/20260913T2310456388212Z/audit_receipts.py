"""Inspect native JSONL receipt references; historical candidate contents are not current source."""
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / '20260913T2136389781471Z/bundle'))
import graders

def audit():
    reports = []
    for folder in sorted((ROOT / 'commands').iterdir()):
        command = graders.load((folder / 'command.json').read_bytes())
        if command['termination'] == 'not-started':
            continue
        project = Path(command['cwd'])
        result = {'trial': folder.name, 'files': [], 'receipt_count': 0,
                  'references_checked': 0, 'uppercase_hex_references': 0,
                  'unsupported_rows': [], 'problems': []}
        for path in sorted(project.rglob('*.jsonl')):
            if 'trial-skill' in path.parts or '.trial-output' in path.parts:
                continue
            result['files'].append(path.relative_to(project).as_posix())
            for number, line in enumerate(path.read_bytes().splitlines(), 1):
                row = graders.load(line)
                if not isinstance(row, dict) or not {'attempt_id', 'command', 'result'} <= row.keys():
                    result['unsupported_rows'].append([path.relative_to(project).as_posix(), number])
                    continue
                result['receipt_count'] += 1
                refs = []
                def visit(value):
                    if isinstance(value, dict):
                        if 'path' in value and 'sha256' in value:
                            refs.append((value['path'], value['sha256']))
                        if value.get('manifest_path') and value.get('manifest_sha256'):
                            refs.append((value['manifest_path'], value['manifest_sha256']))
                        for child in value.values():
                            visit(child)
                    elif isinstance(value, list):
                        for child in value:
                            visit(child)
                visit(row)
                for raw, expected in refs:
                    if not isinstance(expected, str) or not re.fullmatch('[0-9a-fA-F]{64}', expected):
                        result['problems'].append({'receipt': str(path), 'line': number, 'reason': 'Invalid digest encoding'})
                        continue
                    if expected != expected.lower():
                        result['uppercase_hex_references'] += 1
                    candidates = { (project / raw).absolute(), (path.parent / raw).absolute() }
                    candidates = {p for p in candidates if p.is_relative_to(project) and p.is_file()}
                    matched = []
                    for candidate in candidates:
                        safe = graders.safe_file(project, candidate.relative_to(project).as_posix())
                        if hashlib.sha256(safe.read_bytes()).hexdigest() == expected.lower():
                            matched.append(candidate)
                    if len(matched) != 1:
                        result['problems'].append({'receipt': str(path), 'line': number, 'reference': raw, 'matching_candidates': len(matched)})
                    else:
                        result['references_checked'] += 1
                if row['result'] == 'PASS' and row.get('exit_code') != 0:
                    result['problems'].append({'receipt': str(path), 'line': number, 'reason': 'PASS without observed exit 0'})
        reports.append(result)
    return reports

if __name__ == '__main__':
    rows = audit()
    if len(sys.argv) > 1:
        with Path(sys.argv[1]).open('x', encoding='utf-8') as stream:
            json.dump(rows, stream, ensure_ascii=False, indent=2)
    print(json.dumps(rows, ensure_ascii=False, indent=2))
