"""Read-only audit of the retained forward trial inputs and results."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
project = root / 'retained-project'
state = json.loads((root / 'trial-state.json').read_text())
records = []
files = [p for p in project.rglob('*evaluation.jsonl') if not p.name.startswith('evaluation-cases-')]
for output in files:
    snapshot = output.parent / 'evaluation-snapshots' / output.stem
    cases = output.parent / ('evaluation-cases-' + output.stem + '.jsonl')
    for line in output.read_text(encoding='utf-8').splitlines():
        record = json.loads(line)
        assert record['status'] == 'PASS' and record['expectation_met'] and record['error'] is None
        assert record['build_manifest_sha256'] == state['builder_manifest_sha256']
        assert record['cases_sha256'] == hashlib.sha256(cases.read_bytes()).hexdigest()
        for name, expected in record['candidate_digests'].items():
            assert hashlib.sha256((snapshot / name).read_bytes()).hexdigest() == expected
        records.append(record)

manifest = json.loads((root / 'retained-project-manifest.json').read_text())
expected = {row['path']: row['sha256'] for row in manifest['files']}
actual = {p.relative_to(project).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in project.rglob('*') if p.is_file()}
assert actual == expected

live_source = Path(state['project']) / 'raw/claude-receipt-summary'
source_baseline = json.loads((project / 'docs/plan/skill-imports/receipt-summary/initial/snapshot/evidence/source-manifest.json').read_text())
original = {r['path']: r['sha256'] for r in source_baseline['files']}
after = {p.relative_to(live_source).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in live_source.rglob('*') if p.is_file()}
assert original == after

commands = [json.loads(line) for line in (root / 'commands.jsonl').read_text().splitlines()]
summary = {'captured_at_utc': datetime.now(timezone.utc).isoformat(), 'evaluation_invocations': len(files), 'grader_observations': len(records), 'by_profile': dict(Counter(r['profile'] for r in records)), 'all_observations_passed': True, 'retained_files': len(actual), 'retained_copy_digests_verified': True, 'all_evaluator_candidate_and_case_digests_verified': True, 'live_import_source_files_and_digests_unchanged': True, 'terminal_commands': len(commands), 'structural_checks': sum(r['purpose'] == 'Skill Creator structural check' for r in commands), 'script_executions': sum('summarize.py' in ' '.join(r['argv']) for r in commands), 'expected_conflict_proposals': sum(r['expected_exit_code'] == 1 for r in commands), 'unexpected_exit_codes': sum(r['exit_code'] != r['expected_exit_code'] for r in commands), 'builder_manifest_sha256': state['builder_manifest_sha256']}
(root / 'final-readback-audit.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
print(json.dumps(summary))
