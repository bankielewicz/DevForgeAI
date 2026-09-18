"""Prepare independent revision fixture inputs; does not execute dev."""
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    base = ROOT / 'legacy-bundle/fixtures/DV-01'
    cases = {
        'RV-02': ('custom receipts Ω [$literal]/', 'Literal spaces, Unicode, brackets and dollar sign remain one path value; promised evidence appears under exactly that root.'),
        'RV-03': ('selected receipts/', 'Existing evidence/sentinel.txt stays byte-identical; evidence appears under the explicit selection without a redundant permission request.'),
        'RV-04': ('custom receipts/', 'Reject supplied shortened mapping before endorsing completion; preserve the draft and compare required versus actual paths with original selection.'),
        'RV-05': ('unavailable receipts/child/', 'Selected parent is a regular immutable file; report the exact conflict and PARTIAL/BLOCKED, with no silent alternate evidence destination. Independent read-only work can continue.'),
        'RV-06': ('new receipts/', 'Detect changed evidence destination versus checkpoint, preserve old records and input, bind future records to new selection, invalidate old completion claims.'),
    }
    plans = []
    for cid, (destination, oracle) in cases.items():
        project = ROOT / 'revision-fixtures' / cid
        shutil.copytree(base, project)
        # These are independent synthetic specification inputs, not modified product outputs.
        spec = (project / 'spec.md').read_text(encoding='utf-8')
        with (project / 'spec.md').open('a', encoding='utf-8', newline='\n') as stream:
            stream.write('\nR-2: Evidence destination selected for this task is `' + destination + '`.\n')
        if cid == 'RV-03':
            write(project / 'evidence/sentinel.txt', 'Existing evidence is user content; preserve these exact bytes.\n')
        elif cid == 'RV-04':
            write(project / 'delivery-draft.md', '# Prior unverified draft\nSelected evidence: receipts/\nContext: receipts/context.md\nDelivery: receipts/delivery.md\nR-2: VERIFIED\nOverall: COMPLETE\n')
        elif cid == 'RV-05':
            write(project / 'unavailable receipts', 'Immutable regular file blocking the selected directory; do not delete, rename or replace.\n')
        elif cid == 'RV-06':
            write(project / 'old receipts/prior-delivery.md', '# Prior attempt\nR-2: VERIFIED at old receipts/\nOverall: COMPLETE\nRetain this original artifact.\n')
            write(project / 'checkpoint.json', {
                'synthetic_fixture': True, 'selected_evidence_value': 'old receipts/',
                'selection_source': 'previous user task selected old receipts/',
                'resolved_evidence_root': 'old receipts/',
                'output_mapping': {'delivery': 'old receipts/prior-delivery.md'},
                'input_spec_sha256': hashlib.sha256((project / 'spec.md').read_bytes()).hexdigest(),
                'pending_jobs': [], 'next_action': 'recheck selected inputs before resuming',
                'requirement_status': {'R-2': 'VERIFIED'},
            })
        rows = [{'path': p.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(project.rglob('*')) if p.is_file()]
        plans.append({'case_id': cid, 'requirement_ids': ['REV-001', 'REV-002', 'REV-003', 'REV-004'],
                      'expected': oracle, 'selected_evidence_value': destination, 'fixture_refs': rows,
                      'timeout_seconds': 360, 'attempt_budget': 1,
                      'scope': 'review selected delivery-draft.md against selected inputs and report delivery status' if cid == 'RV-04' else 'resume selected checkpoint.json' if cid == 'RV-06' else 'implement through applicable QA'})
    write(ROOT / 'revision-case-plan.json', {'cases': plans, 'alias': {'RV-01': 'DV-17'}, 'unique_case_count': 23,
                                           'policy': 'Independent oracles fixed before revised package receipt. No cold trial or target check executed by preparation.'})


if __name__ == '__main__':
    main()
