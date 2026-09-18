"""Render manual findings/report from sealed case observations and actual command records."""
from closeout_records import RUN, load, save, ref
from collections import Counter
import datetime as dt
import hashlib
import json
import sys


def finding(rule, anchor, description, correction, refs, cases):
    identity = [rule, 'SKILL.md', anchor, 0]
    return {'finding_id': 'F-' + hashlib.sha256(json.dumps(identity, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest(),
            'identity': identity, 'rule_id': rule, 'category': 'input_evidence_limitation', 'severity': 'major',
            'subject_path': 'SKILL.md', 'locator': 'Assessment execution capability, not a source defect location',
            'source_refs': next(r['source_refs'] for r in load(RUN / 'rule-set.json')['rules'] if r['rule_id'] == rule),
            'observation_refs': refs, 'description': description, 'user_impact': 'The full required assessment cannot be reported as passing.',
            'proposed_correction': correction, 'preserved_requirements': ['Preserve current package, old attempts, exact denominator and failed command evidence.'],
            'verification_cases': cases, 'disposition': 'deferred'}


def handoff():
    assessment = load(RUN / 'assessment.json')
    cases = load(RUN / 'case-observations-final.json')['cases']
    incomplete = [c['case_id'] for c in cases if c['result'] in ('NOT_RUN', 'ERROR')]
    findings = [finding('AV-E01', 'Mixed-family records scope limitation',
                        'The unchanged full-run schema1 records observer interprets external bundle-relative paths and raw snapshot nested file rows as run-relative record references; initial command exited 1 with 184 errors. Dedicated bundle integrity succeeds separately. This is a validator/tool scope mismatch, not evidence of an altered dev package.',
                        'Minimum separate evaluator correction: declare a canonical storage/collection boundary that keeps foreign-schema bundle and raw snapshot envelopes under excluded inputs/trials while validating them with their own bound verifier, or add family-aware reference resolution to the validator. Then run the full declared record scope in a fresh retained assessment. Do not rewrite this run or substitute its supported-subset result for the failed full command.',
                        [ref(RUN / 'commands/records-mixed-initial/stdout.txt')], ['AV-E01'])]
    if incomplete:
        findings.append(finding(incomplete[0], 'Required cold execution incomplete',
                                'Required cold cases remain incomplete after bounded native attempts; exact model-capacity, timeout and platform command failures remain in the case observations and raw streams. Partial product tests do not establish completed case qualification.',
                                'When the selected model has capacity and required host tools can execute, explicitly select a new retained run for incomplete cases. Do not overwrite or silently retry these attempts, switch models, or inherit historical PASS outcomes.',
                                [ref(RUN / 'inputs/case-observations-final.json')], incomplete))
    failed = [c for c in cases if c['result'] == 'FAIL']
    for case in failed:
        findings.append(finding(case['case_id'], 'Observed required case failure', case['reason'],
                                'Separately review the exact retained case evidence to determine a bounded correction before another authored revision.',
                                [ref(RUN / 'inputs/case-observations-final.json')], [case['case_id']]))
    save(RUN / 'findings.json', {'schema_version': '1', 'run_id': RUN.name, 'target_name': 'dev', 'findings': findings})
    save(RUN / 'handoff.json', {'schema_version': '1', 'run_id': RUN.name, 'target_name': 'dev',
                              'target_package_digest': load(RUN / 'source-manifest.json')['package_digest'],
                              'builder_readiness': 'BLOCKED', 'proposal_review_state': 'not_needed',
                              'selected_finding_ids': [], 'deferred_finding_ids': [f['finding_id'] for f in findings],
                              'proposed_spec': None, 'baseline_reference': None, 'adoption_required': False,
                              'authoring_family_basis': ref(RUN / 'inputs/authoring-family-supplement.json'),
                              'source_manifest': ref(RUN / 'source-manifest.json'), 'source_after_manifest': ref(RUN / 'source-after-manifest.json'),
                              'assessment': ref(RUN / 'assessment.json'), 'evaluation_bundle': ref(RUN / 'inputs/bundle-manifest-final.json'),
                              'unresolved_decisions': ['Required native execution and mixed-family evidence-checker compatibility remain incomplete. No new source repair is justified solely by capacity/timeouts.'],
                              'preservation_boundaries': ['No skill-source repairs, operational updates, installation, plugin, framework gate, or application development outside disposable fixtures.'],
                              'installation': 'NOT_PERFORMED', 'framework_acceptance': 'NOT_EVALUATED'})


def report():
    assessment = load(RUN / 'assessment.json')
    cases = load(RUN / 'case-observations-final.json')['cases']
    summary = load(RUN / 'trials/evaluation-final/summary.json')
    mixed = load(RUN / 'commands/records-mixed-final/stdout.txt')
    subset = load(RUN / 'commands/records-schema1-complete-final/stdout.txt')
    counts = Counter(c['result'] for c in cases)
    commands = []
    for path in sorted((RUN / 'commands').glob('*/command.json')):
        record = load(path)
        commands.append((path.parent.name, record))
    command_lines = ['# Actual command log', '', 'This lists commands captured by the assessment harness through record-check closeout. Manual file inspection and final receipt publication use parent terminal operations and are not inferred as product tests. All native attempts remain retained. Native trial limit: 360 seconds, at most two concurrently, inherited model configuration, no automatic retries. DV-17/RV-02 attempt002 followed explicitly approved escalation after attempt001 host-start Access denied; no trial outcome was erased.', '']
    for name, record in commands:
        command_lines.extend(['## ' + name, '', '- Started: ' + record['started_at_utc'], '- Termination / exit: ' + str(record['termination']) + ' / ' + str(record.get('exit_status')), '- Working directory: `' + record['cwd'] + '`', '- Actual argument vector: `' + json.dumps(record['argv'], ensure_ascii=False) + '`', '- Evidence: [command.json](commands/' + name + '/command.json), [stdout](commands/' + name + '/stdout.txt), [stderr](commands/' + name + '/stderr.txt)', ''])
    save(RUN / 'command-log.md', '\n'.join(command_lines))
    rows = ['| Case | Result | Observed reason |', '| --- | --- | --- |']
    rows += ['| ' + c['case_id'] + ' | ' + c['result'] + ' | ' + c['reason'].replace('|', '\\|').replace('\n', ' ') + ' |' for c in cases]
    dims = '\n'.join('- ' + name + ': ' + data['outcome'] + ' (' + str(data['required_evaluated']) + '/' + str(data['required_total']) + ' applicable required checks evaluated).' for name, data in assessment['dimensions'].items())
    text = f'''# Independent dev assessment

Assessment: **{assessment['overall_assessment']}**. Assessment completed with retained execution limits; this is not a passing evaluated build.

Package: `C:/Projects/DevForgeAI/src/agents/skills/dev`  
Package SHA-256: `{load(RUN / 'source-manifest.json')['package_digest']}`  
Exact current authoring request passed mandatory intake (`BOUND`). Original specification and revision were explicitly selected and verified; current source readback is unchanged. [Input identity](inputs/input-index.json), [intake](commands/intake/stdout.txt), [readback](commands/source-readback-final/stdout.txt), [input readback](inputs/final-input-readback.json).

## Original regression outcome

DV-17 / alias RV-01 passed a real new cold session using the original unquoted `Evidence destination: custom receipts/.` prompt. Evidence appeared under the exact selected root; final actual-versus-required readback and raw execution references were independently inspected. RV-02 also passed with literal spaces, Unicode, brackets and dollar sign. DV-16 passed mandatory current packet intake and separately owned bundle binding/execution; actual dev product TDD/QA was observed. Historical successes were not carried forward as current passes.

## Coverage and dimensions

Declared rules: 82 = 26 DEV requirements + 4 REV requirements + 29 AV rules + 23 unique scenarios. RV-01 aliases DV-17 and is counted once. Source-level semantic checks and cold behavior are separate rows. Eleven optional/adaptive checks are explicitly inapplicable; applicable required coverage is {assessment['required_coverage']['required_evaluated']}/{assessment['required_coverage']['required_total']}. No unknown applicability is hidden.

{dims}
- Enforcement recommendations: descriptive only; no new authority implementation or acceptance.

Unique scenario result: **{counts.get('PASS', 0)} PASS, {counts.get('FAIL', 0)} FAIL, {counts.get('NOT_RUN', 0)} NOT_RUN, {counts.get('ERROR', 0)} ERROR of 23**, pass rate `{100 * counts.get('PASS', 0) / 23:.8f}%`. Nonpasses remain in the denominator. This rate is below the repository 95% minimum when incomplete cases remain. Framework executed-line coverage for this instruction/template-only dev package is not applicable; validator runner coverage is not substituted for product or framework coverage. Root's separate builder QA evidence is outside this dev denominator.

## Case observations

{chr(10).join(rows)}

## Evaluation artifacts and limitations

The mandatory Python JSONL runner, deterministic graders, raw fixtures, expected results, JSON schema, dependency/runtime information and artifact manifest exist in [bundle/](bundle/artifact-manifest.json). The runner was actually executed against this package, verified bound artifact/reference digests, enforced unique case counts and validated output schema. [Final results](trials/evaluation-final/results.jsonl), [summary](trials/evaluation-final/summary.json), [manual observations](case-observations-final.json), [recorded commands](command-log.md). Python supplies evidence only. Compiled Rust retains DevForgeAI gate and acceptance authority.

The final native-receipt audit found no mismatched supported references or protected-input changes. DV-18 includes one separately reviewed preliminary console-error row outside the audit's supported command schema: it honestly retains missing timestamps/local stream capture and points to the actual native tool transcript. Its later path handling and product execution were verified; the preliminary row is not relabeled as complete product evidence. [Audit output](commands/audit-native-final/stdout.txt).

The full unchanged schema1 records checker returned **{mixed['status']}**, exit 1, with {len(mixed['errors'])} errors: [full output](commands/records-mixed-final/stdout.txt). Its path rules interpret the external bundle's bundle-relative references and raw snapshot envelope as ordinary run-relative schema1 records. The first supported collection also failed because my collector omitted source files lacking direct check references; [that failure remains retained](commands/records-schema1-final/stdout.txt). A fresh complete-source supported-schema1 exact-byte collection returned **{subset['status']}**, exit {load(RUN / 'commands/records-schema1-complete-final/command.json')['exit_status']}: [complete subset output](commands/records-schema1-complete-final/stdout.txt), [collection custody](inputs/schema1-collection-custody-complete.json). The bundle verifier and subset result complement the failed full-run result; they do not replace it. AV-E01 remains ERROR and standards assessment remains INCOMPLETE. This is an evaluator scope limitation, not a demonstrated dev package defect.

Native Windows Codex CLI trials used the inherited configured model, existing authenticated connection, 360-second per-attempt limit and two-session maximum. Initial Access denied attempts are preserved alongside explicit approved host-start escalation. Selected-model capacity failures and genuine timeout terminations were not retried or converted into passes. DV-03 JavaScript's required `node --test` command could not spawn child processes (EPERM); direct-node alternate results do not satisfy that selected required command. Partial products and honest blocking reports are retained. No implicit auto-discovery/activation claim follows from explicit skill selection; independent description routing is a limited observation only. Native non-Windows qualification, GUI, installation, plugin namespacing, framework acceptance, actual token consumption and local tokenizer count with an unavailable cache are unperformed.

Sources: explicitly captured specification/revision and dated local rule catalog, with official skill guidance refreshed during this assessment at [OpenAI skill guidance](https://learn.chatgpt.com/docs/build-skills). The refresh corroborates metadata, description triggers, progressive disclosure and optional resources; it does not silently replace the frozen rule set. [Refresh evidence](inputs/official-guidance-refresh.json), [source bindings](sources.json), [rule set](rule-set.json), [semantic observations](semantic-review-final.json), [workflow](workflow-map.json).

## Handoff

No new dev repair specification is fabricated for host capacity/time limits. [Findings](findings.json) retain execution and evaluator compatibility gaps; [handoff](handoff.json) is BLOCKED for a full passing evaluation. Minimum next step: resolve selected-model capacity/required host-command execution and explicitly select a fresh run for incomplete cases, preserving all attempts; separately resolve the validator mixed-record-family compatibility contract. A new attempt never rewrites these results or removes failed/incomplete cases from this run's denominator.

Validation: PERFORMED — {assessment['overall_assessment']}  
Testing: PERFORMED — required case coverage incomplete  
Installation: NOT_PERFORMED  
Framework acceptance: NOT_EVALUATED
'''
    save(RUN / 'validation-report.md', text)


if __name__ == '__main__':
    {'handoff': handoff, 'report': report}[sys.argv[1]]()
