"""Read-only, stdlib checks of handoff Outcome cells and explicitly claimed files."""
import argparse
import hashlib
import json
from pathlib import Path

ALLOWED = {'PASS', 'FAIL', 'NOT_RUN', 'COULD_NOT_RUN', 'NOT_APPLICABLE'}


def outcomes(text):
    rows = []
    active = False
    tables = 0
    for number, line in enumerate(text.splitlines(), 1):
        if not line.strip().startswith('|'):
            active = False
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if cells[:2] == ['Check', 'Outcome']:
            active = True
            tables += 1
            continue
        separator = bool(cells) and all('-' in cell and set(cell) <= {'-', ':', ' '} for cell in cells)
        if active and len(cells) > 1 and not separator:
            rows.append({'line': number, 'outcome': cells[1],
                         'result': 'PASS' if cells[1] in ALLOWED else 'FAIL'})
    return {'tables': tables, 'rows': rows,
            'result': 'PASS' if tables and rows and all(x['result'] == 'PASS' for x in rows) else 'FAIL'}


def check(project, handoff, receipt=None, claims=()):
    result = {'scope': 'Outcome vocabulary, explicit file existence and receipt digest resolution only',
              'semantic_claim_review': 'NOT_EVALUATED', 'receipt_status': 'NOT_RUN', 'files': []}
    code = 0
    try:
        if not project.is_absolute() or not handoff.is_absolute():
            raise ValueError('project and handoff paths must be absolute')
        result['outcome_cells'] = outcomes(handoff.read_text(encoding='utf-8'))
        if result['outcome_cells']['result'] != 'PASS':
            code = 1
        for path in claims:
            target = path if path.is_absolute() else project / path
            ok = target.is_file() and target.stat().st_size > 0
            result['files'].append({'claim': str(path), 'result': 'PASS' if ok else 'FAIL'})
            if not ok:
                code = 1
        if receipt is not None:
            receipt = receipt if receipt.is_absolute() else project / receipt
            if not receipt.is_file():
                result['receipt_status'] = 'FAIL'
                result['receipt_cause'] = 'Requested receipt does not exist as a file'
                code = 1
            else:
                result['receipt_status'] = 'COULD_NOT_RUN'
                document = json.loads(receipt.read_text(encoding='utf-8'))
                entries = document.get('files') if isinstance(document, dict) else None
                valid = isinstance(entries, list) and bool(entries)
                covers_handoff = False
                for row in entries if isinstance(entries, list) else []:
                    ok = isinstance(row, dict) and isinstance(row.get('path'), str) and isinstance(row.get('sha256'), str)
                    path = row.get('path') if isinstance(row, dict) else None
                    if ok:
                        target = Path(path)
                        target = target if target.is_absolute() else project / target
                        ok = target.resolve() != receipt.resolve() and target.is_file()
                        if ok:
                            data = target.read_bytes()
                            ok = bool(data) and hashlib.sha256(data).hexdigest() == row['sha256']
                            covers_handoff = covers_handoff or (ok and target.resolve() == handoff.resolve())
                    valid = valid and ok
                    result['files'].append({'receipt_target': path, 'result': 'PASS' if ok else 'FAIL'})
                valid = valid and covers_handoff
                result['receipt_covers_handoff'] = covers_handoff
                result['receipt_status'] = 'PASS' if valid else 'FAIL'
                if not valid:
                    code = 1
    except (OSError, UnicodeError, ValueError) as exc:
        result['check_error'] = str(exc)
        code = 2
    result['result'] = 'PASS' if code == 0 else 'FAIL' if code == 1 else 'COULD_NOT_RUN'
    return code, result


def main():
    parser = argparse.ArgumentParser(description='Check Markdown Check/Outcome tables and optional JSON receipt files. No prose, provenance or adoption validation. Exit 0: requested checks pass; 1: observed mismatch/missing file; 2: unreadable/invalid check input.')
    parser.add_argument('--project', required=True, type=Path)
    parser.add_argument('--handoff', required=True, type=Path)
    parser.add_argument('--receipt', type=Path, help='JSON with nonempty files list of path/sha256 entries')
    parser.add_argument('--claim', type=Path, action='append', default=[], help='Explicitly claimed saved file; repeat as needed')
    args = parser.parse_args()
    code, result = check(args.project, args.handoff, args.receipt, args.claim)
    print(json.dumps(result, indent=2))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
