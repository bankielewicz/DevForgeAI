"""Final artifact readback and immutable evidence ledger; no target modifications."""
import json
import re
import sys
import urllib.parse
import native_trials as n

ROOT = n.RUN
sys.path.insert(0, str(n.PRIOR / 'bundle'))
import graders

def load(name):
    return graders.load((ROOT / name).read_bytes())

def ref(name):
    return {'path': name, 'sha256': graders.sha((ROOT / name).read_bytes())}

record_check = load('verification/commands/records-002/stdout.txt')
assert not record_check['errors'] and record_check['overall_assessment'] == 'FAIL'
for row in load('inputs/native-extension-binding.json')['artifacts']:
    graders.verify_refs(ROOT, [row])
results = [graders.load(line) for line in (ROOT / 'native-case-results.jsonl').read_bytes().splitlines()]
for row in results:
    graders.verify_refs(ROOT, row['evidence'])
metrics = graders.metrics(results)
assert metrics['passing'] == 16 and metrics['counts']['FAIL'] == 1 and metrics['counts']['NOT_RUN'] == 1
receipts = load('inputs/native-receipt-audit.json')
assert not any(row['problems'] or row['unsupported_rows'] for row in receipts)
links = []
for name in ('validation-report.md', 'revision-spec.md'):
    content = (ROOT / name).read_text(encoding='utf-8')
    assert len(re.findall(r'^```', content, re.M)) % 2 == 0
    for target in re.findall(r'\]\(([^)]+)\)', content):
        if target.startswith(('http:', 'https:')):
            continue
        relative = urllib.parse.unquote(target.split('#')[0].strip('<>'))
        path = ROOT / relative
        assert path.exists() and path.resolve().is_relative_to(ROOT), (name, relative)
        links.append({'document': name, 'target': relative, 'exists': True})
proposal = (ROOT / 'revision-spec.md').read_text(encoding='utf-8')
assert set(re.findall(r'\*\*(DEV-\d{3})', proposal)) == {f'DEV-{i:03d}' for i in range(1, 27)}
assert all(f'**REV-{i:03d}' in proposal for i in range(1, 5))
assert all(f'RV-{i:02d}' in proposal for i in range(1, 7))
source = n.observe.make_manifest(n.PROJECT / 'src/agents/skills/dev')
assert source['package_digest'] == load('source-manifest.json')['package_digest']
input_count = 0
for row in load('input-readback.json')['checks']:
    assert graders.sha(n.observe.read_stable(n.observe.safe_path(row['original_path']))) == row['expected_sha256']
    input_count += 1
prior_count = 0
for root, name in [(n.PRIOR, 'artifact-ledger.json'), (ROOT.parent / '20260913T2210193529778Z', 'retained-artifact-manifest.json')]:
    manifest = graders.load((root / name).read_bytes())
    for row in manifest['files']:
        assert graders.sha(graders.safe_file(root, row['path']).read_bytes()) == row['sha256']
        prior_count += 1
n.save(ROOT / 'final-artifact-review.json', {'schema_version': '1', 'run_id': ROOT.name, 'target_name': 'dev', 'review': 'Primary validator self-review; no independent semantic correctness guarantee', 'local_links_checked': links, 'complete_proposal_requirement_ids': 'DEV-001..026 and REV-001..004', 'proposed_fix_cases': 'RV-01..06, future execution NOT_RUN', 'case_accounting': metrics, 'native_jsonl_receipts_checked': sum(x['receipt_count'] for x in receipts), 'native_receipt_hash_references_checked': sum(x['references_checked'] for x in receipts), 'receipt_audit_limits': 'JSONL receipts only; DV-11 JSON analysis record reviewed separately; no statistical provenance or OS isolation claim', 'schema_record_references_checked': record_check['references_checked'], 'schema_errors': [], 'source_readback': 'MATCH', 'current_input_hashes_rechecked': input_count, 'prior_sealed_files_rechecked': prior_count, 'active_owned_jobs': [], 'timestamp': n.h.now()})
manifest = n.observe.make_manifest(ROOT)
assert manifest['complete'] and not manifest['excluded_boundaries']
n.save(ROOT / 'retained-artifact-manifest.json', manifest)
receipt = {'schema_version': 'dev-validation-final-v2', 'run_id': ROOT.name, 'target_name': 'dev', 'assessment_completed': True, 'assessment': 'FAIL', 'validation': 'PERFORMED', 'testing': 'PERFORMED_WITH_REQUIRED_FAILURE_AND_GAP', 'installation': 'NOT_PERFORMED', 'framework_acceptance': 'NOT_EVALUATED', 'package_digest': source['package_digest'], 'request_sha256': '7ebe47919c03b654614dcfa5ff288c0e58a3870615582e798780c74e8cfa15d6', 'specification_sha256': 'b9783ca08d86fa734c89ce76623ff6c45b2640781d3955f16ea54ea659c7b265', 'mandatory_bundle': 'CREATED_AND_EXECUTED; evaluated-build qualification FAIL/INCOMPLETE', 'metrics': metrics, 'report': ref('validation-report.md'), 'checks': ref('checks.jsonl'), 'findings': ref('findings.json'), 'proposal': ref('revision-spec.md'), 'handoff': ref('handoff.json'), 'artifact_review': ref('final-artifact-review.json'), 'artifact_manifest': ref('retained-artifact-manifest.json'), 'schema_check': ref('verification/commands/records-002/stdout.txt'), 'ledger_exclusions': ['retained-artifact-manifest.json itself', 'FINAL-RECEIPT.json created after ledger'], 'builder_readiness': 'BLOCKED', 'proposal_review': 'pending', 'owned_running_jobs': [], 'finalized_at': n.h.now()}
n.save(ROOT / 'FINAL-RECEIPT.json', receipt)
for row in manifest['files']:
    assert graders.sha(graders.safe_file(ROOT, row['path']).read_bytes()) == row['sha256'], row['path']
for key in ('report', 'checks', 'findings', 'proposal', 'handoff', 'artifact_review', 'artifact_manifest', 'schema_check'):
    graders.verify_refs(ROOT, [receipt[key]])
print(json.dumps({'status': 'SEALED', 'ledger_files': len(manifest['files']), 'ledger_bytes': sum(row['bytes'] for row in manifest['files']), 'manifest_sha256': receipt['artifact_manifest']['sha256'], 'receipt_sha256': graders.sha((ROOT / 'FINAL-RECEIPT.json').read_bytes()), 'proposal_sha256': receipt['proposal']['sha256'], 'metrics': metrics}, indent=2))
