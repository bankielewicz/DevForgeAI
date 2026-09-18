"""Prepare an explicitly unqualified review for compiled read-only preflight."""
import json
from pathlib import Path
import record

ROOT = Path(__file__).resolve().parent
bindings = json.loads((ROOT/'bindings.json').read_text())
inventory_path = ROOT/'source-observation-002/stdout.bin'
inventory = json.loads(inventory_path.read_bytes())
assert record.sha256(inventory_path) == '2029d7889cd4054d2791fd0e55684dae48ac0c37aac12710e068aad858a1fbad'
assert record.sha256(Path(bindings['binary'])) == bindings['binary_sha256']
assert record.package_manifest() == json.loads(Path(bindings['candidate_manifest']).read_text())
policy_path = record.PACKAGE/'src/restrictive-launch-policy.json'
policy = json.loads(policy_path.read_text())
assert record.sha256(policy_path) == '1dbc48c4a3627f7c5fc7a996935ec507426e4cd90adac058eb81100ac9b526b5'
identity = json.loads((record.PACKAGE/'src/native-executable-identity.json').read_text())
fixture = Path(bindings['fixture'])
assert record.sha256(fixture/'task.json') == bindings['task_sha256']
assert not (fixture.parent/'run').exists()
review = {
    'schema_version': 2,
    'reviewer': 'Codex evidence preparation; all findings UNQUALIFIED; not a human operator attestation',
    'trial_selection_ref': str(record.WORKSPACE/'docs/specs/framework/runtime/codex-worker-source-identity-v1.md'),
    'codex_sha256': identity['executable_sha256'],
    'checkout_root': str(fixture), 'model': 'gpt-6-astra', 'effort': 'high',
    'profile_sources': [{'path': e['path'], 'sha256': e['sha256']} for e in inventory['entries'] if e['state'] == 'file'],
    'findings': {'native_read_only_available': False, 'no_external_tool_or_hook_effects': False,
                 'codex_managed_chatgpt': False, 'no_custom_provider': False},
    'launch_policy_id': policy['policy_id'], 'launch_policy_sha256': record.sha256(policy_path),
    'source_inventory_ref': str(inventory_path), 'source_inventory_sha256': record.sha256(inventory_path),
}
def write(name, value):
    with (ROOT/name).open('x', encoding='utf-8') as out:
        json.dump(value,out,indent=2); out.write('\n')
write('preflight-review.unqualified.json',review)
request = {
    'schema_version': 2, 'project_id': 'DevForgeAI', 'checkout_id': 'source-identity-preflight',
    'work_id': 'native-profile-inspection', 'run_id': fixture.parent.name,
    'candidate_sha256': bindings['task_sha256'], 'checkout_root': str(fixture),
    'run_dir': str(fixture.parent/'run'), 'worker_executable': identity['physical_executable'],
    'worker_sha256': identity['executable_sha256'], 'adapter': identity['adapter'], 'scenario': 'complete',
    'profile': {'model': 'gpt-6-astra', 'effort': 'high',
                'review_ref': str(ROOT/'preflight-review.unqualified.json'),
                'review_sha256': record.sha256(ROOT/'preflight-review.unqualified.json'),
                'launch_policy_id': policy['policy_id'], 'launch_policy_sha256': record.sha256(policy_path)}
}
write('preflight-request.json',request)
write('preflight-input-bindings.json', {
    'request_sha256': record.sha256(ROOT/'preflight-request.json'),
    'review_sha256': record.sha256(ROOT/'preflight-review.unqualified.json'),
    'source_inventory_sha256': record.sha256(inventory_path),
    'physical_sources': len(review['profile_sources']),
    'all_findings_false': all(v is False for v in review['findings'].values()),
    'purpose': 'Inputs only for preflight; do not authorize run, model work or framework acceptance',
    'native_model_trials_consumed': 0,
})
print((ROOT/'preflight-input-bindings.json').read_text())
