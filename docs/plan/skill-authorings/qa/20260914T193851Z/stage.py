"""Apply the selected prose/template extension to the captured candidate only."""
from pathlib import Path
import re

RUN = Path(__file__).resolve().parent
CANDIDATE = RUN / 'candidate'
spec = (RUN / 'inputs/0').read_text(encoding='utf-8-sig')

def clause(number):
    marker = '**QAP-' + str(number).zfill(3)
    block = spec[spec.index(marker):]
    return re.split(r'\n(?=\*\*QAP-|## [0-9])', block, maxsplit=1)[0].strip()

def read(name):
    return (CANDIDATE / name).read_text(encoding='utf-8')

def replace(text, old, new):
    if text.count(old) != 1:
        raise ValueError('Edit anchor must occur once: ' + old[:100])
    return text.replace(old, new, 1)

def write(name, text):
    # Preserve original CRLF representation throughout retained prose.
    (CANDIDATE / name).write_bytes(text.replace('\r\n', '\n').replace('\n', '\r\n').encode('utf-8'))

name = 'SKILL.md'
s = read(name)
start = s.index('Default to **plan**')
end = s.index('## Preserve evidence and ownership')
s = s[:start] + '''Default to **run** for an ordinary product QA request, including this skill with selected product specifications alone. Require the project, selected specifications/stories, scope and applicable rules. Bind current source including relevant local changes unless another candidate is selected; a saved plan is not required for a full run. A sprint needs its selected story set or an unambiguous scope manifest. Read dependency references for context without selecting their deliverables. A general QA question or pasted procedure alone does not initiate tests.

**Plan** means an explicit test-plan, planning-only or no-execution request: inspect and write selected planning/report artifacts without product builds, tests, executable harness generation or product-state mutation. Host planning/write restrictions override desired run intent; report unsaved artifacts where writes are prohibited. **Execute** selects a saved plan and candidate. **Retest** selects a corrected candidate and defect set with a saved or newly derived bounded plan. These are conversational intents, not CLI flags. Never promote earlier planning-only intent into execution or automatically invoke dev or another QA session.

An ordinary full QA request authorizes necessary inspection, isolated QA fixtures/harnesses, local builds, tests, instrumentation, reports and cleanup of QA-owned disposable state within the selected scope and host permissions. Preserve existing session authorization. Discover before asking for essential missing decisions or additional effects; continue independent permitted work while a decision is pending. Installation, persistent startup/service changes, deployment, migrations, destructive real-data actions and new remote targets need applicable authorization. Use host approval mechanisms when required.

## Follow the selected workflow

1. Read [intake and planning](references/intake-planning.md). Bind exact input/candidate bytes and literal output paths, inventory every selected criterion and design independent oracles. Use [the test-plan template](assets/test-plan-template.md). Declare each check READY or BLOCKED with prerequisites/dependents, authorized preparation and complete metric collection boundaries. Plan NEEDS_INPUT blocks only dependent work, not the ready independent subset.
2. Read [execution and integrity](references/execution-integrity.md) and [assessment](references/assessment.md). Save/read back the plan, then inspect selected first-party code, tests and evidence processing for integrity failures before product tests; inspect new QA helpers before use. Explicit plan mode remains read-only inspection/design plus allowed plan/report writes and ends with the planning-only handoff.
3. For run, execute or retest, recheck identity and effects. After plan readback and applicable integrity inspection, give a brief progress update and proceed into ready preparation/execution in the same invocation. Do not ask the user to select the plan just generated or end with an execute prompt while ready independent work remains. Preserve candidate bytes and prior attempts; QA must not repair product source or developer tests.
4. Classify each issue using demonstrated behavior. Confirmed integrity failure, valid completed subthreshold metric, or critical authorization/security/data-preservation defect immediately stops the whole test run. Launch no further tests, builds, coverage campaigns or investigative reproductions; safely contain owned in-flight work and preserve remaining NOT_RUN obligations with the trigger ID. Ordinary mandatory defects retain eventual FAIL while safe independent checks continue. Local prerequisite/harness gaps block dependents only; uncontained safety/ownership or identity problems stop the run. Apply these rules as new material/results arrive.
5. Assess valid evidence. Both first-party executed-line coverage and required **unit-test** pass rate must meet >=95%, or stricter project floors, per required platform and overall. Keep other test categories and applicable project-wide suite thresholds separate. Do not finalize partial collection as a failing percentage. FAIL takes precedence over INCOMPLETE; PASS requires all mandatory obligations, integrity and valid metrics with no required gaps.
6. Read [reporting, restart and user handoff](references/reporting-handoff.md). Fill [the QA report](assets/qa-report-template.md) for every completed, stopped, blocked or planning-only invocation; on FAIL also fill [the qa-fix packet](assets/qa-fix-template.md). Read back artifacts at the bound destination and deliver the outcome-specific handoff after ready work is exhausted or a genuine stop/blocker prevents continuation. Report exact delivery failures without changing destination silently.

Track intent, plan readiness, execution status (NOT_STARTED/IN_PROGRESS/COMPLETED/STOPPED) and verdict separately. Explicit planning-only uses NOT_EVALUATED as a non-verdict marker, never NOT_EXECUTED as a verdict. A full run can establish FAIL from confirmed static evidence with execution NOT_STARTED. Gaps alone yield INCOMPLETE; a stopped run never claims complete testing.

''' + s[end:]
write(name, s)

name = 'agents/openai.yaml'
s = replace(read(name), 'Use $qa to plan independent QA for the selected specifications and development candidate.', 'Use $qa to perform independent QA against the selected specifications and current development candidate.')
write(name, s)

name = 'references/intake-planning.md'
s = read(name)
start = s.index('**QA-002')
end = s.index('Accept optional development handoff')
s = s[:start] + '''**QA-002 / QAP-001 — Modes.**

''' + clause(1).split('**QAP-001 — Intent and mode.** ', 1)[1] + '''

Explicit planning-only permits relevant read-only inspection and selected plan/evidence/report writes. It does not run product tests/builds, generate executable harnesses, install dependencies or mutate product state. It reports NOT_EVALUATED as a non-verdict marker. Do not automatically invoke dev or another QA session.

**QA-003 — Runtime inputs.** Require selected project identity, explicit specification/story document(s), requested scope/intent and applicable instructions. A full run binds the current candidate and generates its plan during intake; it needs no previously saved plan. Explicit execute revalidates the selected saved plan and candidate. Retest requires the corrected candidate and defect set with an existing or newly derived bounded plan. Planning-only may inspect intended behavior before implementation exists; identify the missing candidate/build prerequisite for affected cases.

''' + s[end:]
s = replace(s, '## Establish the candidate and evidence baseline', clause(2) + '\n\n## Establish the candidate and evidence baseline')
s = replace(s, 'Planning output status is READY or NEEDS_INPUT; it is not a product QA verdict. Static defects discovered during planning may be recorded as confirmed findings, but planning alone must not be presented as completed QA execution. Save the plan and its identity, then perform the final handoff phase. Do not automatically run it.', clause(3) + '\n\n' + clause(4))
s = replace(s, 'Static findings may be confirmed during planning, but the plan remains READY or NEEDS_INPUT and any planning report uses NOT_EXECUTED.', 'Static findings may be confirmed during intake; explicit planning-only reports use NOT_EVALUATED as a non-verdict marker. Full runs can establish FAIL from confirmed static findings with execution NOT_STARTED; apply issue classification and stop rules before proceeding.')
s = replace(s, 'Follow [the final user handoff](reporting-handoff.md) after saving and reading back the plan. Under host Plan mode, return the unsaved plan in conversation and identify saving/binding as a prerequisite to a file-based execute handoff.', 'After plan readback and applicable integrity inspection, a full run proceeds to ready preparation/execution under QAP-004. Use [reporting and handoff](reporting-handoff.md) at actual completion, terminal stop, or exhaustion of permitted work. Explicit planning-only ends with plan/report handoff. Under host planning/write restrictions, return unsaved content in conversation and identify saving/binding and execution permission as applicable prerequisites.')
write(name, s)

name = 'references/execution-integrity.md'
s = replace(read(name), 'In plan mode, use these procedures for read-only inspection and test design only. Execution actions require the selected plan, candidate and permitted effects.', 'In explicit plan mode, use these procedures for read-only inspection and test design only; findings do not create a product verdict in that mode. Full run generates/binds its plan and candidate internally; execute/retest revalidate their selections. Execution requires the bound plan, candidate and permitted effects.\n\n' + clause(5))
s = replace(s, '## Execute the selected plan', '## Classify issues and control continuation\n\n' + clause(6) + '\n\n' + clause(8) + '\n\n' + clause(9) + '\n\n## Execute the selected plan')
s = replace(s, 'Before executing, reread the selected plan, candidate, rules, and evidence paths.', 'Before executing, reread the bound plan (generated in this full run or explicitly selected), candidate, rules, and evidence paths. After plan readback and applicable integrity inspection, proceed to ready authorized preparation/execution in the same invocation; do not request selection of a newly generated plan.')
s = replace(s, 'Retry only within current authorization and plan budgets; do not silently repeat consumed or irreversible actions.', 'Retry only within current authorization and plan budgets before any terminal stop; retain failed attempts, inspect changed QA helpers and do not silently repeat consumed or irreversible actions. A terminal integrity/metric/critical stop forbids further repair, tests or reproductions in this run.')
s = replace(s, 'Track authorized retry budgets independently of case counts.', 'Track authorized retry budgets independently of case counts. Record ordered launch/decision observations (timestamps or sequence IDs), trigger issue IDs, affected dependents and in-flight disposition so later review can distinguish work already running from a forbidden post-stop launch.')
write(name, s)

name = 'references/assessment.md'
s = read(name)
s = replace(s, '**QA-019 — Verdict.** Execution produces one product QA verdict:', clause(7) + '\n\n' + clause(10) + '\n\n**QA-019 — Verdict.** Run/execute/retest produces one product QA verdict, including a full run assessed on confirmed static evidence before tests start:')
s = replace(s, 'below-threshold measured metric', 'valid completed below-threshold metric')
s = replace(s, 'Before execution, declare eligible source inventory/exclusions and the unique required unit-case inventory for each platform.', 'Before collection, declare eligible source inventory/exclusions, the unique required unit-case inventory for each platform, all tests contributing to each coverage measurement, and its terminal completion conditions. Schedule meaningful integrity and complete metric evidence as early as dependencies allow; do not execute a knowingly partial coverage subset to manufacture an early percentage.')
s = replace(s, 'For every platform and overall scope, report integer numerator/denominator, the exact ratio and an unrounded decision.', 'For every valid completed platform/overall measurement, report integer numerator/denominator, the exact ratio and an unrounded decision. For incomplete/unavailable collection, report retained counts and remaining obligations as partial evidence, with no final percentage or threshold decision.')
s = replace(s, 'Required unit skips/errors/blocked/unexecuted cases remain nonpassing cases in the denominator; retries are attempts of the same case, never extra cases or erased evidence.', 'At valid suite finalization, required unit skips/errors and other terminal nonpasses remain in the denominator; an unfinished suite cannot treat not-yet-executed cases as an early measured failure. Always retain required blocked/unexecuted obligations in the inventory and report. Retries are attempts of the same case, never extra cases or erased evidence.')
s += '\nApplicable project-wide suite pass-rate requirements remain independently required; declare their inventory and report their counts separately from the required unit-test metric. Satisfying the unit floor does not substitute for those project rules.\n'
write(name, s)

name = 'references/reporting-handoff.md'
s = read(name)
s = replace(s, 'Generate the runtime report using', 'For every completed, stopped, blocked or explicit planning-only invocation, generate the runtime report using')
s = replace(s, 'The remediation owner is `dev`, never `qa`.', 'The remediation owner is `dev`, never `qa`. Identify the exact defective artifact and ownership: a QA-authored prohibited/gamed helper still produces a terminal integrity FAIL and scoped dev remediation handoff, not a false accusation against application source. Separate prerequisite/harness gaps from confirmed artifact defects.')
s = replace(s, 'For low coverage, identify uncovered files/ranges and missing meaningful tests;', 'For valid completed deficient coverage, identify bound uncovered files/ranges and missing meaningful behavior tests; missing coverage instead names the unavailable collector/prerequisite, not an invented low-coverage defect;')
start = s.index('| Plan READY |')
end = s.index('\n\n**QA-024', start)
s = s[:start] + '''| Explicit plan READY | End with actual plan/report locations and an optional resolved later execute prompt; no automatic execution. |
| Explicit plan NEEDS_INPUT | End with plan/report or exact host write restriction, unresolved inputs, affected cases and owners. |
| Full run with ready independent work | Internal continuation; proceed under QAP-004, not a final execute handoff. |
| Run/execute/retest FAIL | Report and fix packet for all confirmed defects; manual dev prompt. QA performs no product repair. |
| Run/execute/retest INCOMPLETE | Report exact blockers, affected cases and owners; provide a resolved resume request when inputs permit. |
| Run/execute/retest PASS | Report and project-defined downstream review; no invented release permission. |''' + s[end:]
s = replace(s, 'After plan/report/fix publication and readback, end with a concrete end-user handoff.', 'After runnable work completes or a genuine terminal/blocking condition exhausts permitted work, publish/read back required artifacts and end with a concrete end-user handoff. Explicit planning-only ends after its plan/report. A ready full run must not end at plan publication.')
s = replace(s, 'For READY, select the actual saved plan, candidate, specification identities, evidence destination and intended test effects; this proposes a later execute invocation and does not authorize it itself.', 'For explicit planning-only READY, an optional later execute prompt selects the actual saved plan, candidate, specification identities, evidence destination and intended test effects; it does not itself authorize execution. Full-run READY is an internal continuation, never a final prompt requesting selection of its own plan.')
s = replace(s, 'Any write/readback failure remains explicit and no affected artifact is described as delivered.', 'Any write/readback failure remains explicit and no affected artifact is described as delivered. In conversation give the available findings, exact undelivered artifacts, original destination, failure and next recovery action. Do not silently substitute another destination. A confirmed FAIL remains FAIL despite incomplete report delivery.')
s += '''
## Continuation records and legacy inputs

''' + clause(13).replace('both selected specification identities', 'all selected specification identities') + '''

Keep issue IDs/classifications, demonstrated impact, trigger evidence and terminal/nonterminal decisions in report/fix records. Record intent, plan readiness, execution status and product verdict separately. A stop before execution can retain NOT_STARTED with the stop decision recorded; a started run stopped early uses STOPPED. COMPLETED only means scheduled execution processing ended. Retain affected dependents, remaining NOT_RUN obligations, partial/complete collection status, owned-operation shutdown and artifact-delivery outcomes. Explicit plan has no product verdict (NOT_EVALUATED marker); full-run static findings can establish FAIL without tests.

## Separate package evaluation

QA-026 / QAP-014: This skill's evaluated-build completeness requires a separate skill-validator task binding exact skill and selected specification bytes to a Python JSONL runner, deterministic graders, independent fixtures, expected results, schema, runtime/dependency information and artifact manifests/digests. The bundle may remain external to the runtime package. Missing artifacts or unexecuted required evaluations leave completeness unproven. Graders assess retained traceability, accounting, stop ordering, identities and handoff fields; behavioral trials must observe continuation and test-launch ordering, not merely keywords. Package source readback is not skill acceptance. Python produces evidence only; protected framework phase/gate/validator/mutation/acceptance decisions remain compiled Rust where required by the selected project. No installed service is an intrinsic prerequisite for portable product QA.
'''
write(name, s)

name = 'assets/test-plan-template.md'
s = read(name)
s = replace(s, '- Plan/run identity and requested mode: [values]', '- Plan/run identity and invocation intent: [run/plan/execute/retest; explicit selection or ordinary-run default]\n- Automatic-continuation eligibility and basis: [ready permitted work, applicable host/user restrictions, integrity prerequisites; full run does not await selection of its own plan]\n- Execution status: [NOT_STARTED/IN_PROGRESS/COMPLETED/STOPPED; separate from readiness/verdict]')
s = replace(s, '[allowed scope; pending execution selection/effects]', '[allowed scope and source of existing authorization; only genuinely additional effects pending]')
s = replace(s, '- Checkpoint and next safe action: [input/plan/candidate bindings, completed/planned work, owned process/fixture state, remaining permissions]', '- Checkpoint and next safe action: [all selected input/plan/candidate bindings, intent, completed attempts, issue/stop decisions, per-check readiness, remaining work, owned process/fixture state and permissions]')
s = replace(s, '- Preconditions, entry conditions and environment:', '- Readiness: [READY or BLOCKED with basis; known executable preparation is READY]\n- Prerequisite references, blockers and affected dependents: [IDs, exact missing input/tool/permission/oracle and owner, or none]\n- Authorized preparation: [fixture/harness/instrumentation tasks, known inputs, discovered procedures, permitted outputs and completion evidence; not missing user input merely because uncreated]\n- Preconditions, entry conditions and environment:')
s = replace(s, '- Effective coverage and unit pass floors:', '- Collection scopes and completion conditions: [all contributing case/platform IDs per coverage measurement, usable collector output for full denominator; complete terminal required-unit outcomes before final unit ratio]\n- Partial/crashed collection handling: [unavailable final metric; retain counts and unexecuted obligations, continue only permitted work]\n- Applicable project-wide suite thresholds: [separate required inventory, counts and floor; do not mix categories into unit rate]\n- Effective coverage and unit pass floors:')
s = replace(s, '## Entry, exit and final user handoff', '''## Stop classification and owned operations

- Issue rules: INTEGRITY_FAILURE, METRIC_FAILURE from valid complete measurement, and CRITICAL_PRODUCT_DEFECT stop the whole test run. MANDATORY_PRODUCT_DEFECT retains final FAIL and permits independent safe checks. EXECUTION_SAFETY_BLOCKER stops affected activity, whole run if uncontained. PREREQUISITE_OR_HARNESS_GAP blocks dependents; ADVISORY does not block.
- Critical impact basis: [authorization/security boundary or unintended loss/corruption of required preserved data; expected isolated destructive behavior excluded]
- Owned in-flight operations: [process/fixture identities, cancellation contract and bounded safe shutdown/drain]
- Stop procedure: [ordered trigger/launch records; no new tests/builds/coverage/reproductions after terminal decision; only containment, necessary safe cleanup, evidence, assessment and reporting]
- Remaining cases: [NOT_RUN with trigger issue ID; preserve already observed FAIL/ERROR and partial metrics]
- Local continuation: [unaffected READY case IDs and dependency/safety/oracle basis; no repair after terminal stop]

## Entry, exit and final user handoff''')
s = replace(s, '[selected concrete plan/candidate, identity checks, allowed effects and prerequisites]', '[bound generated-or-selected plan/candidate, readback, integrity inspection, identity/effect checks and per-check prerequisites]')
s = replace(s, 'measured subthreshold metric', 'valid completed subthreshold metric')
s = replace(s, '[later QA execute or prerequisite resolution]', '[internal full-run continuation while ready work remains; final planning-only handoff, dev on FAIL, prerequisite owner on INCOMPLETE, or project-defined review on PASS]')
s = replace(s, '[complete actual plan/candidate/specification selection and effects; for READY only, otherwise exact missing decisions]', '[optional later execute prompt only for explicit planning-only with grounded prerequisites; resolved resume/defect/downstream handoff at actual final disposition; no second approval for ready full run]')
s = replace(s, '- Product QA verdict: NOT_EXECUTED. Framework acceptance: NOT_EVALUATED. Release authorization: [separate supplied decision or not granted].', '- Product QA verdict: [explicit planning-only: NOT_EVALUATED non-verdict marker; full-run outcome in QA report: PASS/FAIL/INCOMPLETE, including static FAIL with execution NOT_STARTED; never NOT_EXECUTED as verdict].\n- Framework acceptance: NOT_EVALUATED. Release authorization: [separate supplied decision or not granted].')
write(name, s)

name = 'assets/qa-report-template.md'
s = read(name)
s = replace(s, '[identity; plan/execute/retest]', '[identity; run/plan/execute/retest]\n- Plan readiness: [READY/NEEDS_INPUT; basis and blocked IDs]\n- Execution status: [NOT_STARTED/IN_PROGRESS/COMPLETED/STOPPED; COMPLETED is not PASS]')
s = replace(s, '[PASS/FAIL/INCOMPLETE; planning-only uses NOT_EXECUTED]', '[PASS/FAIL/INCOMPLETE; explicit planning-only uses NOT_EVALUATED as a non-verdict marker; static full-run FAIL may have execution NOT_STARTED]')
s = replace(s, '- Unavailable platforms or measurements: [cases and reasons]', '- Unavailable platforms or measurements: [cases and reasons]\n- Collection scope and completion evidence per metric/platform: [contributing cases, terminal outcomes, collector usability and bound denominator]\n- Complete versus partial/unavailable metrics: [valid final counts/ratio or retained partial counts with no final percentage/threshold decision]\n- Applicable project-wide suite threshold results: [separate inventory, counts, floor and evidence]\n- Metric-trigger decision: [valid completed measurement, exact floor comparison, issue ID or none; no second collection after terminal stop]')
s = replace(s, '| Defect/gap ID | Criterion/policy | Severity/impact | Confirmed failure or missing evidence | Owner | Evidence |', '| Defect/gap ID | Criterion/policy | Issue class and demonstrated impact | Confirmed failure or missing evidence | Exact artifact and owner | Evidence |')
s = replace(s, '## Disposition', '''## Continuation, stopping and remaining obligations
- Observation/decision order: [stable issue/case/attempt IDs, timestamps or sequence and actual test-launch records]
- Continuation/stop decision: [terminal/nonterminal, classification, trigger ID/evidence, governing requirement and demonstrated impact]
- Reclassifications: [original observation, revised class and evidence-backed reason or none]
- Affected/blocked dependents and reasons: [case IDs and prerequisite/trigger references]
- Independent checks continued: [IDs and identity/safety/readiness/oracle basis or none]
- In-flight work at stop: [owned operation identities, safe cancellation or bounded shutdown/drain and observed disposition]
- Tests stopped and still required: [case IDs; NOT_RUN with trigger ID; preserve observed FAIL/ERROR]
- Partial metrics, remaining fixtures and uncertainty: [actual observations; stopped run never claims complete testing]
- Cleanup: [QA-owned state, necessary actions, results/errors and unresolved state; no claimed unobserved cleanup]

## Disposition''')
s = replace(s, '## End-user handoff', '''## Artifact delivery
- Original evidence selection and bound artifact paths: [literal destinations and role map]
- Required versus actual delivery/readback: [plan/report/fix/checkpoint/external manifest, hashes or exact failure/undelivered status]
- Final external manifest: [path and exact entry names for mutually referencing file hashes; no circular self-hash]
- Recovery action for failed writes/readback: [exact artifacts, original destination and owner/action; no silent substitution; confirmed FAIL retained]

## End-user handoff''')
s = replace(s, '- Next action:', '- Next owner: [dev, prerequisite owner, QA resume, or project-defined downstream reviewer]\n- Next action:')
write(name, s)

name = 'assets/qa-fix-template.md'
s = read(name)
s = replace(s, '- Severity and demonstrated impact: [facts]', '- Issue classification and terminal/nonterminal disposition: [INTEGRITY_FAILURE/METRIC_FAILURE/CRITICAL_PRODUCT_DEFECT/MANDATORY_PRODUCT_DEFECT; trigger evidence and ordered decision]\n- Severity and demonstrated impact: [facts, governing requirement; no unsupported critical label]\n- Exact defective artifact ownership: [application/developer-test/QA-created helper or evidence processing, verified path and scoped remediation responsibility]')
s = replace(s, '- QA retest conditions: [exact observations needed to establish resolution]', '- QA retest conditions: [explicit corrected-candidate retest selection, exact independent observations, affected regressions and invalidated integrity/metric collections to reestablish; no automatic repair/retest]\n- Tests stopped and still required: [case/attempt IDs, preserved FAIL/ERROR, remaining NOT_RUN with trigger IDs and partial metric obligations]\n- Containment and safe cleanup state: [owned operations and actual disposition; no further reproductions after terminal stop]')
write(name, s)
print('Staged prose/template edits in nine existing resources; no quality checks executed.')
