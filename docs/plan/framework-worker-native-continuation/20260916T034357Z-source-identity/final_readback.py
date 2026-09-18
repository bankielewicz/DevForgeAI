"""Evidence readback only; do not make a protected acceptance decision."""
import json
import os
from pathlib import Path
import record

ROOT = Path(__file__).resolve().parent
FOLLOW = ROOT/'current-rules-preflight'
DEV = record.WORKSPACE/'docs/plan/framework-worker-source-identity/20260916T021843Z-dev'
QA = record.WORKSPACE/'docs/plan/framework-worker-source-identity-qa/20260916T021843Z-retest'
bindings = json.loads((ROOT/'bindings.json').read_text())
manifest = json.loads(Path(bindings['candidate_manifest']).read_text())
assert record.sha256(Path(bindings['candidate_manifest'])) == bindings['candidate_manifest_sha256']
actual = record.package_manifest()
assert actual == manifest
inputs = json.loads((DEV/'selected-inputs-final.json').read_text())
changes = [{'path':r['path'],'expected_sha256':r['sha256'],'actual_sha256':record.sha256(record.WORKSPACE/r['path'])}
           for r in inputs if record.sha256(record.WORKSPACE/r['path']) != r['sha256']]
assert [r['path'] for r in changes] == ['AGENTS.md']
assert changes[0]['actual_sha256'] == '3b8e2a112c438b536ab59db2abbcfd6e08ebdd7f41caa13cdf6d5c49866fab86'
assert record.sha256(QA/'qa-report.md') == bindings['qa_report_sha256']
assert record.sha256(QA/'artifact-index.json') == bindings['qa_index_sha256']
assert record.sha256(Path(bindings['binary'])) == bindings['binary_sha256']
assert record.sha256(DEV/'artifact-manifest.json') == 'c8d537420e79156f5b147789e35948b7577e587bce5b837a9564d21e96b3de9e'
receipt_errors = []
receipt_count = 0
for path in ROOT.rglob('receipt.json'):
    receipt = json.loads(path.read_text())
    if 'stdout_sha256' not in receipt:
        continue
    receipt_count += 1
    for name in ['stdout','stderr']:
        stream = path.parent/(name+'.bin')
        if record.sha256(stream) != receipt[name+'_sha256'] or stream.stat().st_size != receipt[name+'_bytes']:
            receipt_errors.append(str(stream))
assert not receipt_errors
before = (FOLLOW/'source-observation-001/stdout.bin').read_bytes()
after = (FOLLOW/'source-readback-final/stdout.bin').read_bytes()
assert before == after
inventory = json.loads(after)
events = [json.loads(line) for line in (FOLLOW/'preflight-001/stdout.bin').read_bytes().splitlines()]
assert len(events) == 7 and events[3]['kind'] == 'server_started'
terminal = events[-1]['data']
assert terminal['reason'] == 'profile_unqualified' and terminal['tree_stopped'] and terminal['fixture_unchanged']
assert terminal['thread_id'] is None and terminal['turn_id'] is None
assert not any(e['kind'] == 'worker_event' and 'preflight' in e['data'] for e in events)
inspect = json.loads((ROOT/'inspect-native-preflight/stdout.bin').read_bytes())
assert inspect['events'] == events and inspect['truncated_tail'] == 0 and inspect['state'] == 'blocked'
trials = []
for selected in [ROOT,FOLLOW]:
    local = json.loads((selected/'bindings.json').read_text())
    fixture = Path(local['fixture'])
    assert sorted(p.name for p in fixture.iterdir()) == ['task.json']
    assert record.sha256(fixture/'task.json') == local['task_sha256']
    assert (fixture.parent/'run/journal.jsonl').read_bytes() == (selected/'preflight-001/stdout.bin').read_bytes()
    trials.append({'fixture':str(fixture),'task_sha256':record.sha256(fixture/'task.json'),
                   'run_dir':str(fixture.parent/'run'),'journal_sha256':record.sha256(fixture.parent/'run/journal.jsonl')})
advisor = record.WORKSPACE/'docs/plan/advisor-runs/20260916T034812Z-8d3c2a'
advisor_results = []
for attempt in [1,2]:
    folder = advisor/f'attempt-{attempt:03d}'
    execution = json.loads((folder/'execution.json').read_text())
    for name in ['stdout','stderr']:
        assert record.sha256(folder/(name+'.txt')) == execution[name+'_sha256']
    raw = json.loads((folder/'stdout.txt').read_text())
    assert not (folder/'response.md').exists()
    advisor_results.append({'attempt':attempt,'execution_status':execution['execution_status'],
                            'response_status':execution['response_status'],'verdict':execution['verdict'],
                            'terminal_reason':raw['terminal_reason'],'reported_cost_usd':raw['total_cost_usd']})
value = {'observed_utc':record.utc_now(),'candidate_files':len(actual),'candidate_unchanged':True,
         'candidate_manifest_sha256':bindings['candidate_manifest_sha256'],
         'selected_inputs_unchanged_count':len(inputs)-len(changes),'selected_input_changes':changes,
         'governing_worker_specs_unchanged':4,'qa_report_and_index_unchanged':True,
         'binary_sha256':bindings['binary_sha256'],'developer_artifact_manifest_sha256':record.sha256(DEV/'artifact-manifest.json'),
         'verified_stream_receipts':receipt_count,'stream_errors':receipt_errors,
         'post_spawn_source_inventory_identical':True,'source_inventory_sha256':record.sha256(FOLLOW/'source-readback-final/stdout.bin'),
         'inventory_counts':{state:sum(e['state']==state for e in inventory['entries']) for state in ['file','directory_index','absent']},
         'approved_junction_count':len(inventory['junctions']), 'native_preflight_terminal':terminal,
         'fixtures':trials,'advisor_attempts':advisor_results,
         'preflight_attempts':2,'codex_process_starts':1,'WN_trial_passes':0,'WN_trial_denominator':2,
         'WN_trial_attempts':0,'native_qualification':'INCOMPLETE','framework_acceptance':'NOT_EVALUATED',
         'no_further_native_launch_selected':True,
         'denial_detail':'No passing config observation or closed predicate reason; do not attribute to account/hooks/plugins/network or a product defect.'}
record.atomic_json(ROOT/'candidate-final.json',actual)
with (ROOT/'final-readback.json').open('x',encoding='utf-8') as stream:
    json.dump(value,stream,indent=2); stream.write('\n')
print(json.dumps(value))
