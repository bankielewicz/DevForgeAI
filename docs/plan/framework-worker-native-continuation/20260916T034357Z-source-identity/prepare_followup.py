"""Retain stale-input denial and prepare one disjoint no-work inspection."""
import hashlib
import json
from pathlib import Path
import shutil
import record

ROOT = Path(__file__).resolve().parent
FOLLOW = ROOT/'current-rules-preflight'
prior = json.loads((ROOT/'preflight-001/receipt.json').read_text())
events = [json.loads(line) for line in (ROOT/'preflight-001/stdout.bin').read_bytes().splitlines()]
assert prior['native_exit_code'] == 3 and not prior['timed_out'] and prior['candidate_unchanged']
assert prior['child_guard_matched_names'] == [] and prior['harness_stopped']
assert [e['kind'] for e in events] == ['admitted','terminal']
assert events[-1]['data']['reason'] == 'profile_unqualified'
assert events[-1]['data']['worker_exit_code'] is None and events[-1]['data']['tree_stopped'] is True
old = json.loads((ROOT/'source-observation-002/stdout.bin').read_bytes())
new = json.loads((ROOT/'source-observation-003-diagnostic/stdout.bin').read_bytes())
old_entries = {e['path']:e for e in old['entries']}
new_entries = {e['path']:e for e in new['entries']}
changes = [{'before':old_entries.get(p), 'after':new_entries.get(p)}
           for p in sorted(old_entries.keys() | new_entries.keys()) if old_entries.get(p) != new_entries.get(p)]
assert len(changes) == 1
change = changes[0]
assert change['before']['path'].endswith('\\rules\\default.rules')
rule_bytes = Path(change['after']['path']).read_bytes()
prefix_matches = hashlib.sha256(rule_bytes[:change['before']['bytes']]).hexdigest() == change['before']['sha256']
assert prefix_matches and hashlib.sha256(rule_bytes).hexdigest() == change['after']['sha256']
suffix = rule_bytes[change['before']['bytes']:]
assert b'advisor-run-002' in suffix and b'advisor_run.py' in suffix
bindings = json.loads((ROOT/'bindings.json').read_text())
assert record.sha256(Path(bindings['candidate_manifest'])) == bindings['candidate_manifest_sha256']
assert record.package_manifest() == json.loads(Path(bindings['candidate_manifest']).read_text())
assert record.sha256(Path(bindings['binary'])) == bindings['binary_sha256']
FOLLOW.mkdir(exist_ok=False)
trial = record.WORKSPACE/'docs/plan/framework-worker-trials/20260916T120406Z-current-rules-preflight'
trial.mkdir(exist_ok=False)
fixture = trial/'fixture'
fixture.mkdir()
(fixture/'task.json').write_bytes((record.PACKAGE/'tests/fixtures/task.json').read_bytes())
assert record.sha256(fixture/'task.json') == bindings['task_sha256']
bindings['fixture'] = str(fixture)
bindings['selected_operation'] = 'preflight after verified host-rule append; no thread or turn'
with (FOLLOW/'bindings.json').open('x',encoding='utf-8') as out:
    json.dump(bindings,out,indent=2); out.write('\n')
shutil.copyfile(ROOT/'record.py',FOLLOW/'record.py')
capture = (ROOT/'capture_preflight.py').read_text()
capture = capture.replace("ROOT/'source-observation-002/stdout.bin'", "ROOT/'source-observation-001/stdout.bin'")
capture = capture.replace("assert record.package_manifest()", "assert record.sha256(Path(bindings['candidate_manifest'])) == bindings['candidate_manifest_sha256']\nassert record.package_manifest()")
with (FOLLOW/'capture_preflight.py').open('x',encoding='utf-8') as out:
    out.write(capture)
preparer = (ROOT/'prepare_preflight.py').read_text()
preparer = preparer.replace("ROOT/'source-observation-002/stdout.bin'", "ROOT/'source-observation-001/stdout.bin'")
preparer = preparer.replace("assert record.sha256(inventory_path) == '2029d7889cd4054d2791fd0e55684dae48ac0c37aac12710e068aad858a1fbad'", "receipt = json.loads((ROOT/'source-observation-001/receipt.json').read_text())\nassert receipt['native_exit_code'] == 0 and receipt['candidate_unchanged'] and not receipt['timed_out']\nassert record.sha256(inventory_path) == receipt['stdout_sha256']")
with (FOLLOW/'prepare_preflight.py').open('x',encoding='utf-8') as out:
    out.write(preparer)
value = {'created_utc':record.utc_now(),'prior_attempt':str(ROOT/'preflight-001/receipt.json'),
         'prior_attempt_native_exit':3, 'prior_codex_spawned':False,
         'inventory_changes':changes, 'prior_rules_are_exact_prefix':prefix_matches,
         'added_bytes':len(suffix), 'added_bytes_sha256':hashlib.sha256(suffix).hexdigest(),
         'added_bytes_reference_approved_advisor_retry':True,
         'operation':'one fresh preflight with current source bindings, same frozen worker and policy',
         'reason':'Host approval appended a rule after collection; bind the actual current source without changing it',
         'model_trial_attempts_consumed':0, 'further_automatic_preflight_attempts_selected':0,
         'review_findings':'all false; no human attestation', 'parent_or_stored_credentials_changed':False,
         'followup_root':str(FOLLOW), 'fixture':str(fixture)}
with (ROOT/'preflight-source-drift.json').open('x',encoding='utf-8') as out:
    json.dump(value,out,indent=2); out.write('\n')
print(json.dumps(value))
