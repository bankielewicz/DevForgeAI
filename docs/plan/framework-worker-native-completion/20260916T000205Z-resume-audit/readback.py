"""Read identities only. No product tests, repairs, or acceptance decisions."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORK = ROOT.parents[3]
PRIOR = ROOT.parent / '20260915T2306060954875Z'
QA = WORK / 'docs/plan/framework-worker-native-completion-qa/20260915T2325371896643Z'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


results = {}
for name in ['candidate-manifest.json', 'inputs-manifest.json']:
    entries = json.loads((PRIOR / name).read_text(encoding='utf-8'))
    results[name] = [{'path': entry['path'], 'expected_sha256': entry['sha256'],
                      'actual_sha256': sha(Path(entry['path'])),
                      'matches': sha(Path(entry['path'])) == entry['sha256']} for entry in entries]

receipts = []
for name, expected in [
    ('qa-report.md', '0cea59ae0461aec0530ee144d8bae340dba7208bec9ad03c97bb8cd1802d1095'),
    ('dev-handoff.md', 'fbb6926a4b3a67433f06a7c12e48a24a013249402c2cc7e1b868eb3e2c4c075c'),
    ('artifact-manifest.json', '886f2c630a03183df3557d9fc58a24075b3af440ade7e00c398e5c5a8fa6b1c5')]:
    actual = sha(QA / name)
    receipts.append({'path': str(QA / name), 'expected_sha256': expected,
                     'actual_sha256': actual, 'matches': actual == expected})

errors = [entry['path'] for rows in list(results.values()) + [receipts] for entry in rows if not entry['matches']]
data = {'timestamp_utc': datetime.now(timezone.utc).isoformat(), 'operation': 'read-only source/handoff identity audit',
        'candidate_and_inputs': results, 'retained_qa_artifacts': receipts, 'errors': errors,
        'previous_goal_turn': 'progress: implementation, independent QA, terminal coverage evidence and failure handoff',
        'current_progress': 'resolved manual remediation/retest prompt and current source identity readback',
        'goal_complete': False, 'qa_campaign': 'STOPPED', 'finding': 'QA-F-COV-01',
        'new_dev_assignment_selected': False, 'native_attempts_consumed': 0,
        'next_action': 'User explicitly selects the separate development remediation and independent retest assignment.'}
(ROOT / 'readback.json').write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'candidate_files': len(results['candidate-manifest.json']), 'input_files': len(results['inputs-manifest.json']),
                  'qa_artifacts': len(receipts), 'mismatches': len(errors)}))
raise SystemExit(bool(errors))
