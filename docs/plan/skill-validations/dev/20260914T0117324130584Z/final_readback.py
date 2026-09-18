"""Read actual selected inputs and final record bytes; no package mutation."""
from closeout_records import RUN, load, save, ref
import datetime as dt
import hashlib
import json
from pathlib import Path
import sys


def inputs():
    rows = []
    for entry in load(RUN / 'inputs/input-index.json'):
        actual = Path(entry['original_path']).read_bytes()
        captured = (RUN / entry['snapshot']['path']).read_bytes()
        expected = entry['snapshot']['sha256']
        rows.append({'original_path': entry['original_path'], 'captured_reference': entry['snapshot'],
                     'actual_sha256': hashlib.sha256(actual).hexdigest(), 'matches': actual == captured and hashlib.sha256(actual).hexdigest() == expected})
    value = {'captured_at_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'status': 'MATCH' if all(r['matches'] for r in rows) else 'SOURCE_CHANGED', 'inputs': rows}
    save(RUN / 'inputs/final-input-readback.json', value)
    print(json.dumps(value, ensure_ascii=False))
    if value['status'] != 'MATCH':
        raise SystemExit(1)


def receipt():
    names = ['validation-report.md', 'checks.jsonl', 'findings.json', 'handoff.json', 'assessment.json', 'source-manifest.json', 'source-after-manifest.json',
             'origin-record.json', 'sources.json', 'rule-set.json', 'workflow-map.json', 'command-log.md', 'semantic-review-final.json', 'case-observations-final.json',
             'inputs/final-input-readback.json', 'inputs/schema1-collection-custody.json', 'inputs/schema1-collection-custody-complete.json', 'bundle/artifact-manifest.json', 'trials/evaluation-final/results.jsonl',
             'trials/evaluation-final/summary.json', 'commands/records-mixed-final/stdout.txt', 'commands/records-schema1-final/stdout.txt', 'commands/records-schema1-complete-final/stdout.txt', 'commands/audit-native-final/stdout.txt']
    # Read complete bytes from every selected delivered record, strict parse machine forms,
    # and decode all textual artifacts. This does not infer semantic success from a digest.
    rows = []
    for name in names:
        path = RUN / name
        data = path.read_bytes()
        text = data.decode('utf-8')
        if path.suffix == '.json':
            json.loads(text)
        elif path.suffix == '.jsonl':
            for line in text.splitlines():
                json.loads(line)
        rows.append({'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    manifest = {'schema_version': 'validation-artifact-readback-v1', 'run_id': RUN.name, 'readback_at_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
                'scope': 'Final delivered assessment records listed explicitly; raw attempt trees remain bound by final case references and before/after manifests.', 'files': rows}
    save(RUN / 'final-artifact-manifest.json', manifest)
    assessment = load(RUN / 'assessment.json')
    value = {'schema_version': 'dev-validation-receipt-v1', 'run_id': RUN.name, 'created_at_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
             'target_package_digest': load(RUN / 'source-manifest.json')['package_digest'], 'assessment_completed': True,
             'assessment': assessment['overall_assessment'], 'scenario_counts': assessment['case_counts'], 'unique_required_scenarios': 23,
             'required_rule_coverage': assessment['required_coverage'], 'source_readback': 'UNCHANGED', 'input_readback': load(RUN / 'inputs/final-input-readback.json')['status'],
             'artifact_readback': ref(RUN / 'final-artifact-manifest.json'), 'validation_report': ref(RUN / 'validation-report.md'),
             'bundle': ref(RUN / 'bundle/artifact-manifest.json'), 'handoff': ref(RUN / 'handoff.json'),
             'full_records_checker': 'MISMATCH; unresolved mixed-family scope; supported collection does not replace this failure',
             'validation': 'PERFORMED', 'testing': 'PERFORMED_WITH_INCOMPLETE_REQUIRED_CASES', 'installation': 'NOT_PERFORMED', 'framework_acceptance': 'NOT_EVALUATED'}
    save(RUN / 'FINAL-RECEIPT.json', value)
    actual = (RUN / 'FINAL-RECEIPT.json').read_bytes()
    assert json.loads(actual) == value
    print(json.dumps({'final_receipt': ref(RUN / 'FINAL-RECEIPT.json'), 'report': ref(RUN / 'validation-report.md'), 'artifact_manifest': ref(RUN / 'final-artifact-manifest.json')}, indent=2))


if __name__ == '__main__':
    {'inputs': inputs, 'receipt': receipt}[sys.argv[1]]()
