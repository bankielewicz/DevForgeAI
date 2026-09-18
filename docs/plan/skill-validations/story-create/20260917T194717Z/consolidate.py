"""Assemble the selected continuation only after every required case has evidence."""
import copy
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from prepare_continuation import RUN, PRIOR, PROJECT, put

ROOT = RUN.with_name(RUN.name + '-records')
OLD = PRIOR.with_name(PRIOR.name + '-records')
SUPPLEMENT = RUN.with_name(RUN.name + '-supplemental')
VALIDATOR = PROJECT / '.agents/skills/skill-validator/scripts'
sys.path.insert(0, str(VALIDATOR))
import observe

REPLAY = {'N02', 'N03', 'N04', 'N05', 'N10', 'N12'}
NEW = REPLAY | {'N13', 'G01', 'G02', 'G03'}
CASES = [f'N{i:02}' for i in range(1, 16)] + ['G01', 'G02', 'G03']
DESCRIPTIONS = {
    'N01': 'Complete single documentation story',
    'N02': 'Complete three-outcome batch; blocked planning gap retained',
    'N03': 'Selected architecture seed and UI obligations',
    'N04': 'Exact recommendation verification; malformed and absent selections',
    'N05': 'RCA condition/provenance and deferred-gap obligations',
    'N06': 'Missing binding stops without product effects',
    'N07': 'Existing-ID collision preserves bytes',
    'N08': 'Proposal-only planning without writes',
    'N09': 'Duplicate seed islands rejected; embedded instructions inert',
    'N10': 'Dependency cycle remains blocked; selected drafts retained',
    'N11': 'Completed-task resume without duplicate story',
    'N12': 'Actual story consumed by development to create the guide',
    'N13': 'Actual development guide consumed by independent QA',
    'N14': 'Implicit skill selection and missing-binding stop',
    'N15': 'Pending-link resume with changed source; existing stories preserved',
    'G01': 'Concurrent epic change preserved during live link update',
    'G02': 'Real Windows denied create reported without alternate delivery',
    'G03': 'Owned truncated story completed at the same path and ID',
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ref(path, relative=False):
    return {'path': path.relative_to(ROOT).as_posix() if relative else str(path.resolve()), 'sha256': digest(path)}


def retain(path):
    destination = ROOT / 'inputs/continuation' / path.relative_to(RUN)
    if not destination.exists():
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open('xb') as stream:
            stream.write(path.read_bytes())
    assert digest(destination) == digest(path)
    return ref(destination, True)


def run_observer(name, argv):
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    result = subprocess.run(argv, cwd=PROJECT, capture_output=True, timeout=120)
    put(RUN / (name + '.stdout.txt'), result.stdout.decode('utf-8'))
    put(RUN / (name + '.stderr.txt'), result.stderr.decode('utf-8'))
    put(RUN / (name + '.execution.json'), {'started_at': started, 'argv': argv, 'cwd': str(PROJECT), 'exit_code': result.returncode})
    assert result.returncode == 0, (name, result.stderr.decode('utf-8'))
    return json.loads(result.stdout)


def main():
    declaration = json.loads((RUN / 'continuation-plan.json').read_bytes())
    manifest = json.loads((ROOT / 'source-manifest.json').read_bytes())
    assert manifest['package_digest'] == declaration['target_digest']
    assert set(declaration['required_remaining_cases']) == NEW
    assert digest(ROOT / 'rule-set.json') == declaration['selected_rule_set']['sha256']
    # Recheck every final native receipt; old attempts remain entirely read-only.
    native = []
    for ident in CASES:
        base = RUN if ident in NEW else PRIOR
        case = base / 'trials' / ident
        number = '002' if ident in REPLAY or ident == 'N01' else '001'
        attempt = case / ('attempt-' + number)
        receipt = json.loads((attempt / 'result.json').read_bytes())
        assert receipt['outcome'] == 'PASS' and not receipt['timeout']
        assert receipt['cleanup'] == 'VERIFIED' and receipt['input_unchanged']
        check = run_observer('receipt-check-' + ident, [sys.executable, '-B', '-X', 'utf8', str(VALIDATOR / 'trial_runner.py'), 'check', '--attempt', str(attempt)])
        assert check.get('outcome') != 'INVALID', ident
        semantic = case / 'semantic-review.md' if ident in NEW else PRIOR / 'trials/native-semantic-review.md'
        evidence = [ref(attempt / 'result.json'), ref(case / 'expected.json'), ref(semantic)]
        if ident in NEW:
            assert 'Result: **PASS**' in semantic.read_text(encoding='utf-8'), ident
            grade = json.loads((case / 'artifact-grade-001.json').read_bytes())
            assert grade['result'] == 'PASS' and not grade['issues'], ident
            for artifact in grade['artifacts']:
                assert digest(Path(artifact['artifact']['path'])) == artifact['artifact']['sha256']
            evidence.append(ref(case / 'artifact-grade-001.json'))
            for path in sorted(case.rglob('*')):
                if not path.is_file():
                    continue
                if path.is_relative_to(case / 'project'):
                    relative = path.relative_to(case / 'project').as_posix()
                    if not relative.startswith(('backlog/', 'evidence/', 'docs/', 'input/', '.trial-output/')):
                        continue
                retain(path)
        native.append({'case_id': ident, 'result': 'PASS', 'observation': DESCRIPTIONS[ident], 'evidence_run': base.name, 'attempt': ref(attempt / 'result.json'), 'elapsed_seconds': receipt['elapsed_seconds'], 'timeout': False, 'exit_code': receipt['exit_code'], 'cleanup': receipt['cleanup'], 'input_unchanged': receipt['input_unchanged'], 'evidence': evidence})
    put(RUN / 'native-assessment.json', native)
    history = []
    for base in [PRIOR, RUN]:
        for path in sorted((base / 'trials').glob('*/attempt-*/result.json')):
            result = json.loads(path.read_bytes())
            history.append({'case_id': result['case_id'], 'run_id': base.name, 'attempt': path.parent.name, 'result': result['outcome'], 'timeout': result['timeout'], 'exit_code': result['exit_code'], 'cleanup': result['cleanup'], 'receipt': ref(path)})
    put(RUN / 'native-attempt-history.json', {'schema_version': 'story-native-attempt-history-v1', 'attempts': history, 'interpretation': 'Every retained launched attempt is listed. The declared case denominator counts each logical case once; retries never erase this history or add required-case credit.'})

    # Readbacks apply to original selected bytes, not just copied snapshots.
    readback = run_observer('source-readback', [sys.executable, '-B', '-X', 'utf8', str(VALIDATOR / 'observe.py'), 'readback', '--source', str(PROJECT / 'src/agents/skills/story-create'), '--manifest', str(ROOT / 'source-manifest.json')])
    assert readback['status'] == 'MATCH'
    put(ROOT / 'source-after-manifest.json', readback['manifest'])
    retain(RUN / 'source-readback.stdout.txt')
    inputs = json.loads((RUN / 'inputs/index.json').read_bytes())
    for item in inputs:
        assert digest(Path(item['original_path'])) == item['sha256'], item['original_path']
    put(ROOT / 'input-readback.json', {'schema_version': '1', 'checked': len(inputs), 'changed': [], 'result': 'MATCH'})
    operational = copy.deepcopy(declaration['operational_inputs'])
    for package, caseid in [('dev', 'N12'), ('qa', 'N13')]:
        copied = RUN / 'trials' / caseid / 'project/.agents/skills' / package
        current = PROJECT / '.agents/skills' / package
        files, excluded = observe.inventory(copied)
        assert not excluded
        live, excluded = observe.inventory(current)
        assert not excluded and {r[0] for r in live} == {r[0] for r in files}
        for relative, path, info in files:
            assert digest(current / relative) == digest(path)
            operational.append(ref(current / relative))
    for item in operational:
        assert digest(Path(item['path'])) == item['sha256']
    put(ROOT / 'operational-readback.json', {'schema_version': '1', 'checked': len(operational), 'result': 'MATCH', 'files': operational})
    origin = json.loads((ROOT / 'origin-record.json').read_bytes())
    origin['source_readback_state'] = 'UNCHANGED'
    (ROOT / 'origin-record.json').write_text(json.dumps(origin, indent=2) + '\n', encoding='utf-8')

    for pattern in ['*.py', '*.ps1', '*controls*.txt', '*controls*.json', '*plan.json', '*amendment.json', '*review.json', '*preflight*.json', 'intake.*', 'receipt-check-*']:
        for path in RUN.glob(pattern):
            if path.is_file():
                retain(path)
    for path in (RUN / 'evaluation').glob('*'):
        if path.is_file():
            retain(path)
    retain(RUN / 'native-assessment.json')
    retain(RUN / 'native-attempt-history.json')

    rows = [json.loads(line) for line in (OLD / 'checks.jsonl').read_text(encoding='utf-8').splitlines()]
    for row in rows:
        row['run_id'] = RUN.name
        # Fresh snapshot metadata has a different digest despite identical source rows.
        # Preserve an old check's historical evidence instead of rebinding its hash silently.
        for value in row['evidence']:
            current = ROOT / value['path']
            if digest(current) != value['sha256']:
                original = OLD / value['path']
                assert digest(original) == value['sha256']
                historical = ROOT / 'inputs/prior-records' / value['path']
                if not historical.exists():
                    historical.parent.mkdir(parents=True, exist_ok=True)
                    with historical.open('xb') as stream:
                        stream.write(original.read_bytes())
                assert digest(historical) == value['sha256']
                value['path'] = historical.relative_to(ROOT).as_posix()
        ident = row['check_id']
        if ident in NEW:
            case = RUN / 'trials' / ident
            attempt = case / ('attempt-002' if ident in REPLAY else 'attempt-001')
            row.update(result='PASS', reason=DESCRIPTIONS[ident] + '; completed receipt, actual artifacts/effects and primary semantic review concur.', evidence=[retain(attempt / 'result.json'), retain(attempt / 'stdout.txt'), retain(case / 'expected.json'), retain(case / 'artifact-grade-001.json'), retain(case / 'semantic-review.md')])
        elif ident == 'grader-controls':
            row.update(reason='21/21 artifact controls, including longer backtick and tilde fences; three genuine red assertion failures retained. Evaluator-only credit.', evidence=[retain(RUN / 'evaluation/red.stderr.txt'), retain(RUN / 'evaluation/green.stderr.txt')])
        elif ident == 'AV-E01-assessment':
            row['reason'] = 'Exact source/specification/operational bytes rechecked; original failed/incomplete attempts retained. All declared native/adverse obligations now have completed scoped observations; inherited-host and platform limits remain explicit.'
            row['evidence'].append(retain(RUN / 'native-assessment.json'))
        else:
            row['reason'] += ' Reused from ' + PRIOR.name + ' for identical candidate and selected contracts; original evidence timestamps retained.'
    rows.append({'schema_version': '1', 'run_id': RUN.name, 'check_id': 'fault-controls', 'rule_id': 'AV-E01', 'subject_path': 'SKILL.md', 'method': 'deterministic', 'required': True, 'applicability': 'applicable', 'result': 'PASS', 'reason': '6/6 independent fault controls, after retained assertion-red and sandbox setup failure; evaluator-only credit.', 'evidence': [retain(RUN / 'fault-controls-red.stderr.txt'), retain(RUN / 'fault-controls-green.stderr.txt'), retain(RUN / 'fault-controls-green-002.stderr.txt')], 'dimension': 'standards'})
    with (ROOT / 'checks.jsonl').open('x', encoding='utf-8', newline='\n') as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False) + '\n')
    dimensions = {name: observe.reduce_checks([row for row in rows if row['dimension'] == name]) for name in observe.DIMENSIONS}
    assert all(value['outcome'] == 'PASS' for value in dimensions.values())
    put(ROOT / 'findings.json', {'schema_version': '1', 'run_id': RUN.name, 'target_name': 'story-create', 'findings': []})
    prior_finding = json.loads((OLD / 'findings.json').read_bytes())['findings'][0]
    put(ROOT / 'inputs/continuation/finding-comparison.json', {'schema_version': 'story-finding-comparison-v1', 'prior_finding': ref(OLD / 'findings.json'), 'finding_id': prior_finding['finding_id'], 'result': 'RESOLVED_FOR_DECLARED_SCOPE', 'basis': 'The same ten missing evidence obligations have now completed against the unchanged package; original INCOMPLETE assessment remains historical.', 'cases': [row for row in native if row['case_id'] in NEW], 'source_correction': None})
    metrics = {
        'Windows': {'helper_unit_pass': 30, 'helper_unit_required': 30, 'helper_cli_pass': 14, 'helper_cli_required': 14, 'native_pass': 15, 'native_required': 15, 'adverse_pass': 3, 'adverse_required': 3, 'required_pass': 62, 'required_total': 62, 'required_pass_rate': 100.0, 'line_covered': 239, 'line_total': 240, 'line_coverage': 100 * 239 / 240, 'branches_covered': 36, 'branches_total': 38, 'branch_coverage': 100 * 36 / 38},
        'Linux': {'helper_unit_pass': 30, 'helper_unit_required': 30, 'symlink_pass': 1, 'symlink_required': 1, 'required_pass': 31, 'required_total': 31, 'required_pass_rate': 100.0, 'line_covered': 239, 'line_total': 240, 'line_coverage': 100 * 239 / 240, 'branches_covered': 36, 'branches_total': 38, 'branch_coverage': 100 * 36 / 38, 'native_workflow': 'NOT_RUN; outside this declared native Windows scope'},
        'overall_declared_target_cases': {'passing': 93, 'required': 93, 'pass_rate': 100.0},
        'grader_controls': {'passing': 21, 'required': 21, 'target_credit': False},
        'fault_controls': {'passing': 6, 'required': 6, 'target_credit': False},
        'routing_classification': {'passing': 12, 'required': 12, 'target_credit': False},
        'thresholds': {'line_minimum': 95, 'required_pass_rate_minimum': 95, 'full_target_pass_floor': 'MET', 'interpretation': 'Each declared target case counted once. Historical attempt failures remain separate. Branch coverage is separately reported; no branch minimum was selected.'},
        'coverage_basis': 'Reused raw Windows/Linux executed-line measurements for identical first-party check_project_binding.py bytes: 240 executable lines, no exclusions. This is helper coverage, not model instruction coverage or Rust framework qualification.'
    }
    put(ROOT / 'metrics.json', metrics)
    assessment = {'schema_version': '1', 'run_id': RUN.name, 'target_name': 'story-create', 'assessment_completed': True, 'overall_assessment': 'PASS', 'dimensions': dimensions, 'required_coverage': observe.reduce_checks(rows), 'framework_acceptance': 'NOT_EVALUATED'}
    put(ROOT / 'assessment.json', assessment)
    put(ROOT / 'enforcement-recommendations.md', '# Enforcement recommendation review\n\nNo new candidates. Authoring instructions, editable binding checks and Python evaluation remain evidence only. No hook, CI policy, operational binding, protected Rust authority or framework acceptance was installed or changed. The earlier limitation was missing execution evidence, now supplied for the declared scope; a gate or status flag could not substitute for those observations.\n')
    put(ROOT / 'command-log.md', '# Commands and retained outcomes\n\nWorking directory: C:/Projects/DevForgeAI, except the disposable native project cwd in each bound plan. Windows Python 3.10.11, Codex CLI 0.154.0, inherited gpt-6-astra/max. Exact argv, prompts, timestamps, exit codes and cleanup are retained in raw plans, execution receipts and streams.\n\n- Continuation intake and snapshot: BOUND, exact unchanged package/request/rule-set.\n- `run_trials.py N02 N03 N04 N05 N10 N12`: six fresh cold replays using the original pretrial inputs, with 1800 seconds selected before launch. Two main workers.\n- `run_adverse.py G01 G02 G03`: sequential live concurrent-change, OS-denial and synthetic-truncation cases; scheduling amendment permits three total active trials.\n- `prepare_qa_consumer.py`, then `run_trials.py N13`: actual completed N12 guide and original story copied unchanged to a cold operational QA consumer.\n- `evaluation/run_controls.py`: red exit 1 (three genuine assertions), green exit 0 (21/21).\n- `run_fault_controls.py`: red exit 1 (two genuine assertions), first green sandbox setup error retained, approved second green exit 0 (6/6).\n- `evaluation/grade_case.py <case>`: mechanical artifact observations plus separately retained primary semantic reviews. Consumer verdicts are independently checked against actual files.\n- Final `trial_runner.py check` for all 18 selected native/adverse receipts, `observe.py readback`, original input and operational hashes: retained separately.\n- Record readers and final delivery audit run after all report references exist; their outputs remain outside the legacy capsule.\n\nEarlier 600-second timeouts and the N01 startup failure remain unchanged in the prior run. No running limit was changed, no source repaired, no provider/model/auth change made and no sandbox bypass selected. The 1800-second replay limit is a declared observation window, not a product performance guarantee. Original helper/routing/control attempts retain their original dates and outcomes.\n\nACL cleanup: the injected explicit deny was removed. Later readback retains all original entries with one additional inherited allow; exact SDDL equality is not claimed. ACL record serialization emitted a depth warning for nested identity metadata, while saved/actual SDDL and difference fields remain complete. No unsupported cause is assigned. Exploratory path lookup errors and broad-output truncation are not target failures; load-bearing artifacts were reread at their actual paths.\n')

    with (ROOT / 'command-log.md').open('a', encoding='utf-8') as stream:
        stream.write('\nAssembly preflight 001 found seven old check references still pointing at the fresh snapshot manifest, whose capture metadata produces a different file digest. Preflight 002 verified all 153 historical references after preserving the old manifest under inputs/prior-records. Both manifests have identical 16 source rows and package digest. This was an evidence-reference assembly correction, not a target defect; both observations are retained.\n')

    lines = ['# story-create 0.1.0 validation', '', '**PASS for the declared validation scope. All previously missing required native and adverse cases now have completed evidence.** No confirmed package defect remains in this assessment.', '',
             f'Target: `{PROJECT / "src/agents/skills/story-create"}`. Package digest: `{manifest["package_digest"]}`. Selected rule-set digest: `{digest(ROOT / "rule-set.json")}`. All applicable mandatory checks in that rule set passed for these exact package bytes.', '',
             '## Assessment dimensions', '', '| Dimension | Outcome | Required evaluated / total |', '| --- | --- | --- |']
    lines += [f'| {name} | {value["outcome"]} | {value["required_evaluated"]}/{value["required_total"]} |' for name, value in dimensions.items()]
    lines += ['| Enforcement recommendations | No new candidates | Descriptive review; no authority claim |', '',
              '## Required execution evidence', '',
              '- Windows: **62/62 required cases = 100%**: 30 helper unit cases, 14 actual helper CLI cases, 15 native workflow cases and 3 adverse cases.',
              '- Linux helper scope: **31/31 = 100%**: 30 unit cases and one symlink rejection. Native Linux model workflows remain outside the declared scope and were not run.',
              '- Overall declared target cases: **93/93 = 100%**. A required case is counted once; retries and evaluator controls add no target credit.',
              '- First-party helper executed-line coverage on each platform: **239/240 = 99.583333%**, with no source exclusions. Branch coverage: **36/38 = 94.736842%**, separately reported. The selected 95% line-coverage and required-case-rate floors are both met. These are helper measurements, not coverage of prose or Rust framework code.',
              '- Artifact grader controls: **21/21**; fault controls: **6/6**; independent description classifications: **12/12**. N14 additionally observed one implicit native selection. No universal activation or model-independence claim follows.', '',
              '## Completed native and adverse cases', '', '| Case | Result | Observed behavior | Evidence run | Seconds |', '| --- | --- | --- | --- | --- |']
    lines += [f'| {row["case_id"]} | PASS | {row["observation"]} | {row["evidence_run"]} | {row["elapsed_seconds"]:.3f} |' for row in native]
    lines += ['', f'The [attempt history](inputs/continuation/native-attempt-history.json) retains {len(history)} launched attempts across both runs: {sum(row["result"] == "PASS" for row in history)} completed passes and {sum(row["result"] != "PASS" for row in history)} earlier nonpasses. These attempt counts are separate from the declared unique-case denominator.', '', 'The eight earlier passes are reused only after rechecking the same candidate, contract and original receipt identities. The ten continuation cases have fresh completed receipts and primary artifact/effect reviews. N12 consumed the actual N01 story; N13 consumed the actual completed N12 guide. No hand-authored substitute was inserted for either producer. G03 uses a declared synthetic truncation of an actual prior story; G01 qualifies the observed concurrent-edit ordering, not every possible interleaving.', '',
              '## Earlier incompleteness and preservation', '',
              f'The [earlier assessment](../{OLD.name}/validation-report.md) remains INCOMPLETE as originally delivered. Six 600-second attempts timed out, their QA consumer was blocked, and three adverse cases had not run. On the user\'s continuation request, an 1800-second window was selected before fresh attempts; their old limits, outputs and failures were preserved. No performance cause or source defect is inferred from a timeout alone.', '',
              'The earlier evidence-limitation finding is resolved for its original ten-case scope in [the comparison record](inputs/continuation/finding-comparison.json). No source correction or revision specification is proposed. The [handoff](handoff.json) is NO_CHANGE; it authorizes no installation or mutation.', '',
              f'All {len(manifest["files"])} target files, {len(inputs)} selected original inputs and {len(operational)} captured operational/evaluator files rechecked unchanged. The authored origin and custody remain distinct from qualification; no generated/adopted history was fabricated. The original helper setup/measurement failures and all new evaluator red/setup attempts remain retained.', '',
              '## Limits and evidence locations', '',
              'Cold CLI sessions inherited host configuration and some memory access; they were not fully isolated or model-independent. The declared workflows ran on Windows; Linux evidence covers the helper only. Rendered product UI, product runtime behavior, exhaustive filesystem/interleaving coverage and tokenizer measurements were not selected. The source rules were pinned from the prior same-day capture and were not silently replaced during continuation.', '',
              'The real denied-write trial left no story or alternate delivery. Its supervisor removed the injected deny rule. Later ACL readback retains the original entries plus one inherited allow entry, so exact final SDDL equality is not claimed and no cause is assigned. This cleanup observation does not negate the directly observed native denial handling.', '',
              f'See [checks](checks.jsonl), [metrics](metrics.json), [workflow map](workflow-map.json), [raw continuation](../{RUN.name}/), [native consolidation](../{RUN.name}/native-assessment.json), [evaluation bundle](../{RUN.name}/evaluation-bundle-manifest.json), [supplemental custody/resource observations](../{SUPPLEMENT.name}/), and [command log](command-log.md). Current check records and historical reused evidence are stored separately inside the packet.', '',
              'Official guidance was captured from [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills); adaptive contracts and numeric floors are repository requirements. Record readers validate supported shapes and byte references only; primary review supplies semantic adjudication. **Framework acceptance: NOT_EVALUATED.** This result completes the selected validation and does not confer protected Rust acceptance or guarantee future executions.']
    put(ROOT / 'validation-report.md', '\n'.join(lines) + '\n')
    handoff = copy.deepcopy(json.loads((OLD / 'handoff.json').read_bytes()))
    handoff.update(run_id=RUN.name, original_manifest=ref(ROOT / 'source-manifest.json', True), origin=ref(ROOT / 'origin-record.json', True), findings=ref(ROOT / 'findings.json', True), report=ref(ROOT / 'validation-report.md', True), builder_readiness='NO_CHANGE', readiness_reasons=['All declared validation obligations completed for the unchanged package. No confirmed source correction or revision specification is proposed. No builder execution, installation or framework acceptance is authorized.'])
    put(ROOT / 'handoff.json', handoff)

    adaptive = json.loads((PRIOR.with_name(PRIOR.name + '-supplemental') / 'adaptive-observations.json').read_bytes())
    adaptive['run_id'] = RUN.name
    adaptive['limitations'].append('Resource/binding observations reused for verified identical bytes and pinned rules; new native completion evidence resides in the continuation capsule.')
    put(SUPPLEMENT / 'adaptive-observations.json', adaptive)
    family = json.loads((PRIOR.with_name(PRIOR.name + '-supplemental') / 'inputs/authoring-family-assessment.json').read_bytes())
    family.update(run_id=RUN.name, intake=ref(RUN / 'intake.stdout.txt'), assessment=ref(ROOT / 'assessment.json'), outcome='PASS')
    put(SUPPLEMENT / 'inputs/authoring-family-assessment.json', family)

    # The manifest is not self-referential. Later reader/audit receipts are separately bound.
    files, excluded = observe.inventory(RUN)
    assert not excluded, excluded
    bundle_files = [{'path': relative, 'bytes': path.stat().st_size, 'sha256': digest(path)} for relative, path, info in files]
    put(RUN / 'evaluation-bundle-manifest.json', {'schema_version': 'story-evaluation-bundle-v1', 'run_id': RUN.name, 'captured_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'target_digest': manifest['package_digest'], 'prior_bundle': ref(PRIOR / 'evaluation-bundle-manifest.json'), 'scope': 'All current raw continuation files: runner, graders, plans, fixtures, expected results, native JSONL events, runtime/receipt/effect evidence, semantic reviews and retained failed controls. This manifest and subsequently created orchestration, record-reader, final-audit and completion receipts are excluded and separately retained and checked.', 'files': bundle_files, 'first_party_framework_authority': False})
    print(json.dumps({'assessment': 'PASS', 'native_adverse': len(native), 'required_cases': 93, 'operational_files': len(operational), 'bundle_files': len(bundle_files), 'required_checks': assessment['required_coverage']}))


if __name__ == '__main__':
    main()
