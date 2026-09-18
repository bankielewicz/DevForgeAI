# Independent QA Test Plan

Fill every field with actual values or a concrete missing/inapplicable reason. Repeat case sections as needed. READY execution steps have no unresolved slots. This is a plan, not an executed QA result.

## Identity, selection and authorization

- Plan/run identity and invocation intent: [run/plan/execute/retest; explicit selection or ordinary-run default]
- Automatic-continuation eligibility and basis: [ready permitted work, applicable host/user restrictions, integrity prerequisites; full run does not await selection of its own plan]
- Execution status: [NOT_STARTED/IN_PROGRESS/COMPLETED/STOPPED; separate from readiness/verdict]
- Planning status: [READY or NEEDS_INPUT and exact basis]
- Project identity, host, shell and filesystem: [actual values]
- Selected iteration/sprint/release-candidate scope: [explicit selection; story manifest if needed]
- Specification/story inputs: [literal paths, hashes, requirement locators]
- Candidate source identity: [commit plus dirty/untracked binding, or scoped first-party manifest; missing prerequisite if absent]
- Build/package identity and source correspondence: [artifact references/hashes or missing prerequisite]
- Dependencies/locks and available services: [versions, identities, state]
- Applicable instructions and architecture/stack/source/testing/data decisions: [references and decisions]
- Development handoff, baseline, known defects and claimed gaps: [references; distinguish claims from confirmed findings]
- Requested effects and existing authorization: [allowed scope and source of existing authorization; only genuinely additional effects pending]
- Explicit exclusions and dependency boundaries: [requirements-based reasons]

## Output and checkpoint binding

- selected_evidence_value and selection source: [literal supplied/policy/established selection]
- Resolved evidence root: [actual full host path]
- Fresh run/attempt destination: [actual path]
- Role-to-path map: [plan, source/build manifests, criterion/case maps, receipts, raw coverage/test reports, findings, QA report, qa-fix, checkpoint and final handoff manifest]
- Plan digest binding: [external manifest/path, completed after final plan readback; no self-hash]
- Checkpoint and next safe action: [all selected input/plan/candidate bindings, intent, completed attempts, issue/stop decisions, per-check readiness, remaining work, owned process/fixture state and permissions]

## Acceptance inventory and risks

| Source-qualified criterion | Exact required behavior / source passage | Mandatory or advisory | Risks / priority | Cases | Independent oracle | Evidence required | Unresolved decisions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [ID and source identity] | [behavior] | [classification] | [risk] | [IDs] | [requirement-derived observation] | [artifacts] | [exact gap or none] |

- Inventory completeness: [all selected clauses including errors, state, recovery, concurrency, compatibility, platforms, documentation and nonfunctional obligations]
- No-ID/duplicate-ID handling: [source-bound local locators or qualified IDs]
- Ambiguous/conflicting requirements: [exact clauses, decision needed, affected cases and owner]
- Advisory improvements: [outside-scope items or none]

## Environment and capability matrix

| Required platform / host | Runtime/tools and discovered versions | Build/test/coverage capability | Services / permissions | Native or visual evidence needed | Readiness and missing prerequisite |
| --- | --- | --- | --- | --- | --- |
| [platform] | [values] | [actual discovery and command source] | [values] | [cases] | [ready or exact gap] |

## Required case inventory

| Stable case ID | Category | Criterion IDs | Required platforms | Provenance | Risk / priority | Applicable scope / exclusion reason |
| --- | --- | --- | --- | --- | --- | --- |
| [ID] | [unit/integration/acceptance/regression/native/setup] | [IDs] | [platforms] | [developer-provided/independent QA/manual native] | [priority] | [scope] |

### Case [stable ID]

- Criterion/source and assertion claim: [exact references and behavior]
- Required platform, category and priority: [values]
- Readiness: [READY or BLOCKED with basis; known executable preparation is READY]
- Prerequisite references, blockers and affected dependents: [IDs, exact missing input/tool/permission/oracle and owner, or none]
- Authorized preparation: [fixture/harness/instrumentation tasks, known inputs, discovered procedures, permitted outputs and completion evidence; not missing user input merely because uncreated]
- Preconditions, entry conditions and environment: [versions, dependency/service state, permissions]
- Fixture/data identity: [inputs and hashes; safe synthetic data where appropriate]
- Isolation and side effects: [authorized QA/output paths, disposable state, candidate-preservation method]
- Procedure: [ordered exact discovered commands/actions, shell, working directory, timeouts and budgets]
- Command provenance: [inspected manifest/documentation and tool discovery; arguments quoted as data]
- Expected observations and independent oracle: [normal/negative/boundary outputs or state, requirement basis]
- Existing assertion limitations: [what developer tests establish and what remains to prove]
- Selected negative control / sensitivity check: [justification, deliberately incorrect behavior to detect, disposable-copy authorization; or justified not selected]
- Actual observations and case status: [NOT_RUN during planning; populated during execution]
- Evidence: [planned receipt/log/raw-report paths, case/attempt IDs and required hashes]
- Cleanup and uncertain-effect recovery: [owned state, safe cleanup, observation after timeout]
- Retry rules: [current authorization, bounded attempts, no duplicate case counting]

## Test-integrity inspection

- First-party implementation/test/QA-helper inventory and omissions: [bound scope]
- Language syntax/import/alias/re-export/wrapper/factory inspection: [performed findings versus planned work]
- Mock decorators or analogous attributes: [confirmed occurrences, bounded clean evidence or incomplete areas]
- Gaming checks: [assertion content, swallowed errors, skipped counts, fake boundaries, denominator/report manipulation, unjustified suppression]
- Legitimate setup/isolation distinctions: [claim limits; no setup-only acceptance credit]
- Unresolved dynamic behavior: [exact gap, owner and affected claims]

## Metrics and accounting declared before execution

- Executed-line source denominator and exclusions: [eligible first-party files/lines, tool, rules; no uncovered behavior removed]
- Per-platform source inventories and overall aggregation: [compatible counts and candidate bindings; no cross-platform substitution]
- Required unit-case denominator: [complete unique case/platform inventory including required skipped/blocked/unexecuted cases]
- Missing required unit tests: [gaps; inspected suite size alone is not completeness evidence]
- Collection scopes and completion conditions: [all contributing case/platform IDs per coverage measurement, usable collector output for full denominator; complete terminal required-unit outcomes before final unit ratio]
- Partial/crashed collection handling: [unavailable final metric; retain counts and unexecuted obligations, continue only permitted work]
- Applicable project-wide suite thresholds: [separate required inventory, counts and floor; do not mix categories into unit rate]
- Effective coverage and unit pass floors: [each >=95% or stricter project requirement; record lower-policy mismatch]
- Calculation: 100 * executed eligible lines / all eligible executable lines; 100 * passing required unit cases / all required unit cases.
- Raw report locations and collector commands: [discovered commands and output bindings; unavailable if absent]
- Precision and attempts: [integer counts, unrounded threshold decision, retained attempts, each case counted once for final candidate]
- Separate branch coverage and acceptance/integration/regression/native accounting: [method and report paths]
- Current measurements: [NOT_RUN; no zero/unresolved denominator treated as 100%]

## Existing evidence proposed for reuse

| Evidence / hash | Candidate and tool/platform binding | Claimed criteria | Validity or drift assessment | Reuse reason / limitation |
| --- | --- | --- | --- | --- |
| [reference or none] | [binding] | [IDs] | [assessment] | [reason] |

## Stop classification and owned operations

- Issue rules: INTEGRITY_FAILURE, METRIC_FAILURE from valid complete measurement, and CRITICAL_PRODUCT_DEFECT stop the whole test run. MANDATORY_PRODUCT_DEFECT retains final FAIL and permits independent safe checks. EXECUTION_SAFETY_BLOCKER stops affected activity, whole run if uncontained. PREREQUISITE_OR_HARNESS_GAP blocks dependents; ADVISORY does not block.
- Critical impact basis: [authorization/security boundary or unintended loss/corruption of required preserved data; expected isolated destructive behavior excluded]
- Owned in-flight operations: [process/fixture identities, cancellation contract and bounded safe shutdown/drain]
- Stop procedure: [ordered trigger/launch records; no new tests/builds/coverage/reproductions after terminal decision; only containment, necessary safe cleanup, evidence, assessment and reporting]
- Remaining cases: [NOT_RUN with trigger issue ID; preserve already observed FAIL/ERROR and partial metrics]
- Local continuation: [unaffected READY case IDs and dependency/safety/oracle basis; no repair after terminal stop]

## Entry, exit and final user handoff

- Execution entry conditions: [bound generated-or-selected plan/candidate, readback, integrity inspection, identity/effect checks and per-check prerequisites]
- Verdict rules: FAIL for confirmed mandatory failure, valid completed subthreshold metric, prohibited mock decorator, gaming or unresolved confirmed regression; otherwise INCOMPLETE for required missing evidence; PASS only with all obligations and both floors satisfied per platform and overall. Use the stop classifications above to decide immediate stopping versus continued independent work.
- Remaining planning gaps and owner: [exact decisions/capabilities and affected cases]
- Source/plan drift and resume policy: [stop affected checks, invalidate affected evidence, preserve attempts]
- Publication/readback: [required-versus-actual literal paths and hashes; unsaved if host Plan mode]
- Open in Claude Code: [resolved project and correct host/environment]
- Next action/owner: [internal full-run continuation while ready work remains; final planning-only handoff, dev on FAIL, prerequisite owner on INCOMPLETE, or project-defined review on PASS]
- Skill availability observation: [skills actually listed in the session]
- Copyable session prompt: [optional later execute prompt only for explicit planning-only with grounded prerequisites; resolved resume/defect/downstream handoff at actual final disposition; no second approval for ready full run]
- Product QA verdict: [explicit planning-only: NOT_EVALUATED non-verdict marker; full-run outcome in QA report: PASS/FAIL/INCOMPLETE, including static FAIL with execution NOT_STARTED; never NOT_EXECUTED as verdict].
- Framework acceptance: NOT_EVALUATED. Release authorization: [separate supplied decision or not granted].
