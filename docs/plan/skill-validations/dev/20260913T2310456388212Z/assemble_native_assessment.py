"""Assemble retained observations and explicit semantic adjudications; no skill repairs."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import shutil
import sys
import native_trials as n

ROOT, PROJECT, PRIOR = n.RUN, n.PROJECT, n.PRIOR
OLD = PRIOR / 'assessment'
SHORT = ROOT.parent / '20260913T2210193529778Z'
observe, h = n.observe, n.h
h.RUN = ROOT / 'verification'
sys.path.insert(0, str(PRIOR / 'bundle'))
import graders

def load(path):
    return graders.load(path.read_bytes())

def save(name, value):
    n.save(ROOT / name, value)

def ref(path):
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': graders.sha(path.read_bytes())}

def copy(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        assert dst.read_bytes() == src.read_bytes(), str(dst)
    else:
        with dst.open('xb') as stream:
            stream.write(src.read_bytes())

def line(path, text):
    i = next(i for i, value in enumerate(path.read_text(encoding='utf-8').splitlines(), 1) if text in value)
    return {'line_start': i, 'line_end': i}

# Recheck original evidence and current input bytes before carrying results forward.
prior_audit = []
for root, manifest_name in [(PRIOR, 'artifact-ledger.json'), (SHORT, 'retained-artifact-manifest.json')]:
    manifest = load(root / manifest_name)
    for row in manifest['files']:
        assert graders.sha(graders.safe_file(root, row['path']).read_bytes()) == row['sha256'], row['path']
    prior_audit.append({'original_root': str(root), 'manifest_sha256': graders.sha((root / manifest_name).read_bytes()), 'files_checked': len(manifest['files']), 'result': 'MATCH'})
for row in load(PRIOR / 'inputs/input-index.json'):
    assert graders.sha(observe.read_stable(observe.safe_path(row['original_path']))) == row['snapshot']['sha256'], row['original_path']
for relative, path, info in observe.inventory(OLD / 'inputs')[0]:
    copy(path, ROOT / 'inputs' / relative)
for name in ['sources.json', 'rule-set.json', 'workflow-map.json', 'semantic-observations.json', 'input-binding-audit.json']:
    value = load(OLD / name)
    value['run_id'] = ROOT.name
    if name == 'semantic-observations.json':
        value['requirements'][-1]['reason'] = 'Mandatory validator bundle exists and was executed; native trials now have retained results. Evaluated-build readiness remains unsatisfied by DV-17 failure and rejected DV-16 handoff.'
        value['resource_adjudication'] += ' Authorized cold trials are now retained in this linked run; native command selection is separately assessed.'
    save(name, value)
copy(SHORT / 'observations/independent-routing.json', ROOT / 'inputs/independent-routing.json')
copy(SHORT / 'inputs/routing-plan.json', ROOT / 'inputs/routing-plan.json')
copy(SHORT / 'FIRST-BATCH-RESULT.json', ROOT / 'inputs/first-batch-result.json')
copy(PRIOR / 'FINAL-RECEIPT.json', ROOT / 'inputs/static-final-receipt.json')
save('inputs/prior-preservation-audit.json', prior_audit)

plans = load(ROOT / 'native-plan.json')['trials']
by_case = {}
effects = []
for plan in plans:
    name = plan['trial_id']
    base = ROOT / 'trials' / name
    command = load(ROOT / 'commands' / (name + '-001') / 'command.json')
    assert command['termination'] == 'exited' and command['exit_status'] == 0, name
    assert (Path(command['cwd']) / '.trial-output/final-001.txt').is_file(), name
    before = load(base / 'attempt-001/before.json')
    after = load(base / 'attempt-001/after.json')
    current = h.inventory(Path(command['cwd']))
    assert after['files'] == current['files'], name
    effect = load(base / 'attempt-001/effects.json')
    assert not effect['immutable_changes'] and not effect['exclusions'], name
    # Every source/fixture byte at native launch was bound to its original plan.
    initial = {x['path']: x for x in before['files']}
    for row in load(base / 'plan.json')['fixture_manifest']['files']:
        assert initial[row['path']] == row, (name, row['path'])
    by_case.setdefault(plan['case_id'], []).append(name)
    effects.append({'trial_id': name, 'result': 'MATCH', 'immutable_changes': [], 'final_fixture_readback': 'MATCH', 'changed_paths': effect['changed_paths']})
save('inputs/native-effects-audit.json', effects)

reasons = {
    'DV-01': 'Cold selected single specification produced real integer-add behavior, context, preserved inputs and seven passing final unittest cases after intended red and green.',
    'DV-02': 'Both selected contracts implemented in dependency order; protocol owns encoding, client imports it; thirteen final tests include real producer-consumer integration, negative and empty cases.',
    'DV-03': 'Separate Python/lib/tests and JavaScript/engine/checks projects used their own runtime and commands. Python six tests passed. Node four direct tests passed; cold task retained node --test EPERM as PARTIAL. Separate approved validator node --test check then passed 4/4 without fixture changes. This is bounded portability evidence, not universal language support.',
    'DV-04': 'Read existing differently named accumulate and its test before reuse decision; batch_total delegates to it. Passing characterization distinguished from eight new red failures; all nine final cases pass.',
    'DV-05': 'Asked for unresolved storage/runtime/interface decisions, delivered independent source-qualified requirements and acceptance proposals, and created no persistence implementation or constitution.',
    'DV-06': 'Read both selected contracts; identified A-1 string versus B-1 integer conflict without inventing precedence; stopped dependent implementation and asked which contract governs.',
    'DV-07': 'Absent unselected service and missing interface identified; no dependency implementation or installation; retained BLOCKED delivery and exact prerequisite needed.',
    'DV-08': 'Used ordinary terminal discovery despite absent optional index; independent add implementation passed eight tests, but missing mandatory publication authority remained blocked with no publication or fallback acceptance.',
    'DV-09': 'Retained passing existing characterization separately from 38 intended assertion failures, nine-test green and ten-test final QA after justified no-change refactor review. No initial passing test was relabeled red.',
    'DV-10': 'Existing unavailable-dependency import error classified as setup ERROR rather than valid red. Separate focused missing-behavior red and six-test green retained; full-suite error remained visible and delivery PARTIAL.',
    'DV-11': 'Synthetic supplied QA analyzed as 1/3 passing, one NOT_RUN and one mandatory FAIL; 949/1000 = 94.9% remained below 95%. No product execution or false COMPLETE claimed.',
    'DV-12': 'Seven Windows tests passed for real product implementation; required unavailable macOS GUI check stayed NOT_RUN and overall delivery PARTIAL. No macOS qualification performed.',
    'DV-13': 'Detected changed specification hash, invalidated synthetic old evidence, preserved checkpoint/evidence and other-actor source comment, and ran fresh seven-test product checks. Unknown unattributable job remained UNKNOWN and was not replayed. Real interrupted-process recovery is not proved by this synthetic fixture.',
    'DV-14': 'Delivered plan only with source-qualified requirements and future verification; created no product source/tests, installer or startup change, and preserved original inputs.',
    'DV-15': 'Original deterministic portable-resource audit remains bound to unchanged eleven-file package, with separate complete semantic review. No product roots/commands/bindings embedded.',
    'DV-16': 'Bundle artifacts and current product-QA ownership are observed, but accepted manual-handoff prerequisite remains blocked by exact contract/request target_root spelling mismatch. Rejection retained; full case NOT_RUN.',
    'DV-17': 'FAIL: exact prompt and spec R-2 select custom receipts/. Cold task silently wrote receipts/, misquoted the selection in context, and declared R-2 VERIFIED and overall COMPLETE. Required destination does not exist. Valid product tests and receipt hashes do not satisfy output mapping.',
    'DV-18': 'Explicit bracketed Unicode spec and project path containing spaces, Omega and literal dollar sign were preserved on Windows. Five product tests passed. Initial cp1252 console error was retained and UTF-8 output enabled; path data was not reinterpreted. Linux native behavior remains untested.'
}
results = []
for i in range(1, 19):
    cid = f'DV-{i:02d}'
    evidence = []
    for name in by_case.get(cid, []):
        base = ROOT / 'trials' / name
        project = Path(load(base / 'plan.json')['permitted_write_root'])
        evidence += [ref(base / 'plan.json'), ref(base / 'prompt.txt'), ref(ROOT / 'commands' / (name + '-001') / 'command.json'), ref(ROOT / 'commands' / (name + '-001') / 'stdout.txt'), ref(base / 'attempt-001/effects.json'), ref(project / '.trial-output/final-001.txt')]
        for path in sorted(project.rglob('*')):
            if path.is_file() and path.name in ('delivery.md', 'context.md', 'context-plan.md', 'executions.jsonl', 'execution-record.jsonl', 'qa-analysis.json', 'qa-analysis.md', 'analysis-execution.json') and 'trial-skill' not in path.parts:
                evidence.append(ref(path))
    if cid == 'DV-03':
        evidence += [ref(ROOT / 'verification/commands/node-001/command.json'), ref(ROOT / 'verification/commands/node-001/stdout.txt')]
    if cid in ('DV-15', 'DV-16'):
        evidence += [ref(ROOT / 'inputs/bundle-attempt-001/results.jsonl'), ref(ROOT / 'inputs/bundle/artifact-manifest.json'), ref(ROOT / 'input-binding-audit.json')]
    results.append({'schema_version': 'dev-native-review-v1', 'case_id': cid, 'required': True, 'result': 'FAIL' if cid == 'DV-17' else 'NOT_RUN' if cid == 'DV-16' else 'PASS', 'method': 'deterministic plus semantic' if cid == 'DV-15' else 'semantic review of real cold execution' if cid != 'DV-16' else 'prerequisite blocked', 'reason': reasons[cid], 'evidence': evidence})
save('native-case-results.jsonl', ''.join(json.dumps(x, ensure_ascii=False) + '\n' for x in results))
metrics = graders.metrics(results)
manifest = load(PRIOR / 'bundle/artifact-manifest.json')
artifact_count = graders.verify_refs(PRIOR / 'bundle', manifest['artifacts'])
graders.verify_refs(PRIOR, manifest['input_refs'])
package = load(ROOT / 'source-manifest.json')
assert graders.verify_package(ROOT / 'source', package) == manifest['package_digest']
assert not graders.portable_scan(ROOT / 'source', package)
save('evaluation-summary.json', {'schema_version': 'dev-evaluation-summary-v2', 'run_id': ROOT.name, 'metrics': metrics, 'bundle_artifacts_verified': artifact_count, 'bundle_status': 'CREATED_AND_EXECUTED', 'native_model_sessions': 17, 'native_model_sessions_exited_zero': 17, 'native_timeouts_this_run': 0, 'prior_model_timeouts': 17, 'prior_host_start_errors': 1, 'independent_description_classification': '8/8', 'native_implicit_activation': 'NOT_RUN', 'assessment': 'FAIL', 'evaluated_build_complete': False, 'framework_acceptance': 'NOT_EVALUATED', 'grading': 'Primary validator semantic adjudication of retained native streams/artifacts; original deterministic graders verify bundle/package bindings and reduce required cases. Python results have no framework authority.'})

# Preserve existing finding identity; add the observed output-selection violation.
findings = load(OLD / 'findings.json')
findings['run_id'] = ROOT.name
anchor = 'Capture context with [context.md](../assets/context.md) before production changes.'
context = ROOT / 'source/references/context.md'
actual_anchor = next(s for s in context.read_text(encoding='utf-8').splitlines() if 'Capture context' in s)
fid, identity = observe.finding_identity('DEV-007', 'references/context.md', actual_anchor, 0)
case17 = next(r for r in results if r['case_id'] == 'DV-17')
findings['findings'].append({'finding_id': fid, 'identity': identity, 'rule_id': 'DEV-007', 'category': 'workflow_bug', 'severity': 'major', 'subject_path': 'references/context.md', 'locator': line(context, 'Capture context'), 'source_refs': [dict(ref(ROOT / 'inputs/inputs/06-dev-skill-spec.md'), source_id='dev-spec', locator='DEV-007, DEV-020, DEV-022; DV-17')], 'observation_refs': case17['evidence'], 'description': 'One cold DV-17 execution silently shortened the literal selected evidence directory custom receipts/ to receipts/, then claimed the output-location requirement VERIFIED and overall COMPLETE. Existing instructions require selected destinations; this is an observed workflow compliance failure, not proof that the wording always fails.', 'user_impact': 'Required outputs are absent at the user-selected location and completion evidence falsely claims that requirement was met.', 'proposed_correction': 'Retain the literal selected destination with source locator, resolve it as one path value, validate all concrete output paths against it before writes, and verify the exact destination requirement before completion claims. Preserve portable routing and avoid a fixed directory or mandatory helper.', 'preserved_requirements': ['DEV-001 through DEV-026', 'user precedence and already supplied authorization', 'no fixed product path', 'raw evidence and earlier attempts preserved', 'no framework acceptance authority'], 'verification_cases': ['DV-17 fresh literal custom receipts path', 'quoted Unicode and metacharacter evidence path', 'explicit destination versus default evidence directory', 'deliberately wrong mapped destination prevents VERIFIED/COMPLETE'], 'disposition': 'proposed'})
save('findings.json', findings)
save('inputs/native-extension-binding.json', {'schema_version': 'dev-evaluation-extension-v1', 'package_digest': package['package_digest'], 'governing_spec_sha256': 'b9783ca08d86fa734c89ce76623ff6c45b2640781d3955f16ea54ea659c7b265', 'original_bundle_root': str(PRIOR / 'bundle'), 'original_bundle_manifest_sha256': graders.sha((PRIOR / 'bundle/artifact-manifest.json').read_bytes()), 'artifacts': [ref(ROOT / name) for name in ('native_trials.py', 'inputs/qa_harness.py', 'native-plan.json', 'extension-policy.json', 'launch-selection.json', 'inputs/prior-scenarios.jsonl', 'inputs/bundle/expected-results.json', 'inputs/bundle/evidence.schema.json', 'inputs/bundle/runtime.json', 'inputs/bundle/runner.py', 'inputs/bundle/graders.py', 'native-case-results.jsonl', 'evaluation-summary.json', 'inputs/native-receipt-audit.json', 'inputs/native-effects-audit.json')], 'limitation': 'Semantic case adjudications are not deterministic proofs; original bundle and native extension retain distinct execution records.'})

# Reuse complete unchanged source/rule review, but reduce behavior using current evidence.
checks = [graders.load(x) for x in (OLD / 'checks.jsonl').read_bytes().splitlines()]
for c in checks:
    c['run_id'] = ROOT.name
    if c['check_id'].startswith('DV-'):
        row = next(r for r in results if r['case_id'] == c['check_id'])
        c.update(result=row['result'], reason=row['reason'], method='semantic' if row['case_id'] != 'DV-15' else 'deterministic', evidence=[ref(ROOT / 'native-case-results.jsonl'), *row['evidence']])
    elif c['rule_id'] == 'DEV-026':
        c.update(reason='Bundle created/executed and cold coverage retained; rejected DV-16 handoff and DV-17 failure prevent evaluated-build completion.', evidence=[ref(ROOT / 'evaluation-summary.json'), ref(ROOT / 'input-binding-audit.json')])
    elif c['rule_id'] == 'AV-W01':
        c.update(result='FAIL', reason='Cold workflow exercised; output-location and false-completion failure observed in DV-17.', evidence=[ref(ROOT / 'native-case-results.jsonl')])
    elif c['rule_id'] == 'AV-W02':
        c.update(result='PASS', reason=reasons['DV-13'] + ' This required bounded scenario does not qualify real asynchronous recovery.', evidence=[ref(ROOT / 'native-case-results.jsonl')])
    elif c['rule_id'] == 'AV-F03':
        c.update(reason='Description semantic review plus independent unlabeled classification passed 8/8; native implicit activation NOT_RUN.', evidence=[ref(ROOT / 'inputs/independent-routing.json'), ref(ROOT / 'inputs/routing-plan.json')])
    else:
        # Rebind only records rewritten under the new identity; captured observations stay exact.
        for e in c['evidence']:
            if e['path'] == 'semantic-observations.json':
                e['sha256'] = ref(ROOT / e['path'])['sha256']
        if c['rule_id'] == 'AV-I04':
            c['reason'] = 'Instructions honor prior authorization and isolate dependent gaps; actual cases now separately exercise missing decisions, scope and authority.'
save('checks.jsonl', ''.join(json.dumps(c, ensure_ascii=False) + '\n' for c in checks))
dimensions = {d: observe.reduce_checks([c for c in checks if c['dimension'] == d]) for d in observe.DIMENSIONS}
save('assessment.json', {'schema_version': '1', 'run_id': ROOT.name, 'target_name': 'dev', 'assessment_completed': True, 'overall_assessment': 'FAIL', 'dimensions': {d: x['outcome'] for d, x in dimensions.items()}, 'required_coverage': observe.reduce_checks(checks), 'packet_status': 'REJECTED', 'assessment_scope': 'Standalone exact package/specification, linked static bundle and authorized fresh native trials', 'framework_acceptance': 'NOT_EVALUATED'})
save('inputs/assembly-state.json', {'new_finding_id': fid, 'prior_finding_id': findings['findings'][0]['finding_id'], 'dimensions': dimensions, 'metrics': metrics})
print(json.dumps({'metrics': metrics, 'dimensions': dimensions, 'new_finding_id': fid}, indent=2))
