"""Verify exact delivered references, preserved history and completed session receipts."""
import datetime
import hashlib
import json
from pathlib import Path
import re

from prepare_continuation import RUN, PRIOR, PROJECT, put

ROOT = RUN.with_name(RUN.name + '-records')
SUPPLEMENT = RUN.with_name(RUN.name + '-supplemental')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked_ref(value, base):
    path = Path(value['path'])
    path = path if path.is_absolute() else base / path
    assert path.is_file() and digest(path) == value['sha256'], str(path)
    return path


def main():
    required = ['source-manifest.json', 'source-after-manifest.json', 'origin-record.json', 'sources.json', 'rule-set.json', 'workflow-map.json', 'checks.jsonl', 'findings.json', 'validation-report.md', 'enforcement-recommendations.md', 'handoff.json', 'command-log.md', 'assessment.json', 'metrics.json', 'input-readback.json', 'operational-readback.json']
    for relative in required:
        assert (ROOT / relative).is_file(), relative
    manifest = json.loads((ROOT / 'source-manifest.json').read_bytes())
    target = PROJECT / 'src/agents/skills/story-create'
    expected = {row['path'] for row in manifest['files']}
    assert expected == {path.relative_to(target).as_posix() for path in target.rglob('*') if path.is_file()}
    for row in manifest['files']:
        assert digest(target / row['path']) == row['sha256']
        assert digest(ROOT / 'source' / row['path']) == row['sha256']
    assert manifest['files'] == json.loads((ROOT / 'source-after-manifest.json').read_bytes())['files']
    inputs = json.loads((RUN / 'inputs/index.json').read_bytes())
    for row in inputs:
        assert digest(Path(row['original_path'])) == row['sha256']
    operational = json.loads((ROOT / 'operational-readback.json').read_bytes())
    for value in operational['files']:
        checked_ref(value, ROOT)
    bundle_counts = {}
    for base in [PRIOR, RUN]:
        bundle = json.loads((base / 'evaluation-bundle-manifest.json').read_bytes())
        for row in bundle['files']:
            assert (base / row['path']).stat().st_size == row['bytes']
            assert digest(base / row['path']) == row['sha256'], row['path']
        bundle_counts[base.name] = len(bundle['files'])
    declaration = json.loads((RUN / 'continuation-plan.json').read_bytes())
    checked_ref(declaration['prior_report'], RUN)
    for value in declaration['prior_receipts']:
        checked_ref(value, RUN)
    rows = [json.loads(line) for line in (ROOT / 'checks.jsonl').read_text(encoding='utf-8').splitlines()]
    count = 0
    for row in rows:
        assert row['result'] in ('PASS', 'NOT_APPLICABLE')
        for value in row['evidence']:
            checked_ref(value, ROOT)
            count += 1
    native = json.loads((RUN / 'native-assessment.json').read_bytes())
    assert len(native) == 18 and len({row['case_id'] for row in native}) == 18
    history = json.loads((RUN / 'native-attempt-history.json').read_bytes())['attempts']
    assert len(history) == 25 and sum(row['result'] == 'PASS' for row in history) == 18
    for row in history:
        checked_ref(row['receipt'], RUN)
    for row in native:
        assert row['result'] == 'PASS' and row['cleanup'] == 'VERIFIED' and row['input_unchanged']
        checked_ref(row['attempt'], RUN)
        for value in row['evidence']:
            checked_ref(value, RUN)
        result = json.loads((RUN / ('receipt-check-' + row['case_id'] + '.stdout.txt')).read_bytes())
        assert result['outcome'] != 'INVALID'
    family = json.loads((SUPPLEMENT / 'inputs/authoring-family-assessment.json').read_bytes())
    for key in ['request', 'baseline', 'authoring_record', 'intake', 'assessment']:
        checked_ref(family[key], SUPPLEMENT)
    assert family['outcome'] == 'PASS' and family['target_digest'] == manifest['package_digest']
    handoff = json.loads((ROOT / 'handoff.json').read_bytes())
    for key in ['original_manifest', 'origin', 'findings', 'report']:
        checked_ref(handoff[key], ROOT)
    assert handoff['builder_readiness'] == 'NO_CHANGE' and handoff['proposed_spec'] is None
    assert json.loads((ROOT / 'findings.json').read_bytes())['findings'] == []
    assessment = json.loads((ROOT / 'assessment.json').read_bytes())
    assert assessment['overall_assessment'] == 'PASS' and assessment['assessment_completed']
    assert assessment['framework_acceptance'] == 'NOT_EVALUATED'
    assert assessment['required_coverage']['required_evaluated'] == assessment['required_coverage']['required_total']
    metrics = json.loads((ROOT / 'metrics.json').read_bytes())
    assert metrics['Windows']['required_pass'] == metrics['Windows']['required_total'] == 62
    assert metrics['Linux']['required_pass'] == metrics['Linux']['required_total'] == 31
    assert metrics['overall_declared_target_cases'] == {'passing': 93, 'required': 93, 'pass_rate': 100.0}
    for platform in ['Windows', 'Linux']:
        value = metrics[platform]
        assert value['line_coverage'] == 100 * value['line_covered'] / value['line_total'] >= 95
        assert value['branch_coverage'] == 100 * value['branches_covered'] / value['branches_total']
    # Actual N12 files must be the unchanged inputs delivered to the N13 consumer.
    qa_oracle = json.loads((RUN / 'trials/N13/expected.json').read_bytes())
    for pair in qa_oracle['source_handoff']:
        source = checked_ref(pair['producer'], RUN)
        consumer = checked_ref(pair['consumer'], RUN)
        assert source.read_bytes() == consumer.read_bytes()
    acl = json.loads((RUN / 'trials/G02/acl-readback.json').read_bytes())
    assert acl['original_entries_retained'] and acl['explicit_deny_count'] == 0
    closed = json.loads((RUN / 'sessions-closed.json').read_bytes())
    assert closed['active_native_handles'] == 0 and all(row['exit_code'] == 0 for row in closed['sessions'])
    readers = []
    for name in ['legacy', 'adaptive']:
        candidates = sorted(RUN.glob(name + '-records-*.execution.json'))
        assert candidates
        receipt = json.loads(candidates[-1].read_bytes())
        assert receipt['exit_code'] == 0
        stdout = candidates[-1].with_name(candidates[-1].name.replace('.execution.json', '.stdout.txt'))
        parsed = json.loads(stdout.read_bytes())
        assert parsed.get('errors', []) == []
        readers.append({'name': name, 'execution': str(candidates[-1]), 'sha256': digest(candidates[-1]), 'status': parsed.get('status')})
    links = []
    for match in re.finditer(r'\[[^\]]+\]\(([^)]+)\)', (ROOT / 'validation-report.md').read_text(encoding='utf-8')):
        link = match[1]
        if link.startswith('https://'):
            continue
        assert (ROOT / link).resolve().exists(), link
        links.append(link)
    put(RUN / 'final-delivery-audit.json', {'schema_version': 'story-delivery-audit-v1', 'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'result': 'MATCH', 'assessment': 'PASS', 'target_digest': manifest['package_digest'], 'target_files_unchanged': len(manifest['files']), 'original_inputs_unchanged': len(inputs), 'operational_files_unchanged': operational['checked'], 'bundle_files_unchanged': bundle_counts, 'check_evidence_refs_verified': count, 'native_adverse_cases': 18, 'retained_attempts': len(history), 'earlier_nonpass_attempts': sum(row['result'] != 'PASS' for row in history), 'required_target_cases': 93, 'actual_producer_consumer_files_identical': len(qa_oracle['source_handoff']), 'required_packet_files_present': required, 'local_report_links_checked': links, 'report_sha256': digest(ROOT / 'validation-report.md'), 'handoff_sha256': digest(ROOT / 'handoff.json'), 'record_readers': readers, 'active_native_handles': 0, 'active_handles_basis': closed, 'framework_acceptance': 'NOT_EVALUATED', 'limitation': 'Byte integrity, arithmetic and documented completion observations; no protected framework authority or universal behavior claim.'})
    print(json.dumps({'result': 'MATCH', 'assessment': 'PASS', 'required_target_cases': 93, 'native_adverse_cases': 18, 'bundles': bundle_counts, 'report': str(ROOT / 'validation-report.md')}))


if __name__ == '__main__':
    main()
