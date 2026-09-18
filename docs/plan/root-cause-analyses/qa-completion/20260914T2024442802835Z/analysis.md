# Root-cause analysis: QA authoring versus evaluated completion

This analysis finds a status-reporting and evidence-reconciliation failure in my previous response. I established that the requested source revision already existed, then led with that narrow accomplishment. I did not make the unresolved evaluated-build outcome the primary disposition. The authoring result was real; complete behavioral qualification was not established. The appropriate current statement is: **source authoring is complete for the retained revision; independent evaluation is INCOMPLETE, with 0/42 complete scenarios qualified; no runtime source defect is confirmed; framework acceptance is NOT_EVALUATED.**

This is an analysis and a set of proposed corrections, not a new skill validation, source repair, framework implementation, or evaluation continuation. Only this fresh RCA directory was written. The dev and validator skills supplied with the request were inspected as evidence and recommendation targets; their implementation/evaluation workflows were not launched. The selected builder workflow had required a manual validation handoff and prohibited running validation itself. Preserving that boundary was correct.

## Evidence and claim boundaries

The [capture manifest](source-manifest.json) binds 47 selected files, 757,213 bytes, including exact snapshots of specifications, authoring records, validator records, native traces, dev instructions/templates, and the Rust design. Its source locators identify the originals; links below identify the retained RCA snapshots. No capture omissions occurred within that explicit list. This was not a whole-repository audit. Original conversation quotations below come from this thread, not from reconstructed runtime logs.

The relevant package digest is `bb9b461276a959fe5278117b6687b3edce1342149ae2dd1b5ea82fb03e1d38ed`, nine files and 79,946 bytes. The [authoring packet](inputs/09-validation-request.json), [my readback](inputs/12-readback.json), and [validation report](inputs/13-validation-report.md) identify that same package. The extension's QAP-014 explicitly separates authoring from evaluated-build completeness and says source readback is not skill acceptance; the companion QA-026 requires the separate evaluation bundle and executed evidence. See [extension](inputs/03-qa-skill-postmvp-spec.md) and [baseline](inputs/02-qa-skill-spec.md).

My actual previous response said “The post-MVP extension was already authored” and “No package edits were needed.” It also explicitly reported Validation and Testing as NOT_PERFORMED and independent evaluation as outstanding. I did **not** issue a literal COMPLETE/PASS or framework acceptance claim. The supported error is therefore the breadth and prominence of my conclusion and its missing cross-workflow status reconciliation. It would be inaccurate to rewrite this incident as a fabricated passing test result or evidence that the source was never authored.

“No source defect confirmed” also does not prove there is no source defect. It means the available assessment does not justify a specific repair. My no-edit conclusion was a source-authoring judgment, not a behavioral qualification result.

## Timeline and what was knowable

All times are UTC on 2026-09-14. Receipt times are execution evidence; report filesystem timestamps are supplemental observations, not an authoritative audit clock.

| Time | Retained fact | Consequence |
| --- | --- | --- |
| Run label 19:38:51 | The [prior delivery](inputs/10-DELIVERY.md) records the post-MVP revision and manual handoff. | This label identifies the authoring run; it is not an exact publication timestamp. |
| 19:49:51 | Validator authoring intake returned exit 0 in the [command log](inputs/15-command-log.md). | Validation had begun against matching bytes. |
| 19:57:41–19:59:41 | [QPV-01 attempt 002](inputs/23-attempt-002.json) reached its 120-second ceiling. | The first incomplete native attempt existed before my readback. |
| 20:00:52.794342 | [My readback receipt](inputs/12-readback.json) records EXISTING_AUTHORED_DELIVERY_UNCHANGED. | I verified custody and stopped authoring; I did not inspect the validation run. |
| 20:04:12–20:06:13 | [QPV-02 attempt 002](inputs/26-attempt-002.json) timed out. | This result was later than my readback. |
| 20:06:13–20:08:13 | [QPV-06 attempt 002](inputs/29-attempt-002.json) timed out after identifying prohibited decorators. | This result was also later than my readback. |
| 20:12:35 | The JSONL evaluator returned exit 2, recorded in the command log. | The complete-scenario reduction was INCOMPLETE. |
| 20:15:11 | Final preservation checks were recorded; the report's observed creation/modification time was 20:15:11. | The final report was later than my readback. |

I cannot claim I ignored a completed final report at 20:00:52; it was produced later. I did miss the opportunity to discover and report an ongoing matching validation run and its already-recorded timeout. The available timeline does not timestamp my final conversation message precisely; it timestamps the evidence operation on which that response relied.

## What the validation actually established

The [full report](inputs/13-validation-report.md) distinguishes evidence classes correctly:

| Evidence class | Result | What it establishes |
| --- | --- | --- |
| Structural and record checks | Passing checks reported | Supported package/record properties, not completed native behavior. |
| Grader implementation tests | 29/29 passed | Tests of the evaluator's grading code. |
| Focused grader coverage | 44/44 executed lines; 32/32 branches | Only `evaluation/graders.py`, not the entire harness or target skill. |
| JSONL grader controls | 28/28 passed | Expected control outcomes; a different inventory from the 29 implementation tests. |
| Complete skill scenarios | 0/42 qualified; all 42 NOT_RUN as complete scenarios | Three attempted pilots did not finish; 39 IDs were not separately attempted. This is not 42 confirmed failures. |
| Required assessment checks | 14/61 evaluated | Separate from the 42-scenario inventory; behavior dimension is 0/43 because assessment rules and scenario IDs are different inventories. |
| Runtime-source findings | No confirmed defect | No evidence-backed source revision was proposed. |
| Aggregate | INCOMPLETE | Evaluated-build completeness remains unproven. |

The native integrity fixture correctly triggered direct and resolved-alias mock detection and a declared stop. No subsequent test launch appears in the retained trace. That partial observation does not satisfy the required report/fix delivery. The [handoff](inputs/16-handoff.json) reports builder readiness BLOCKED because of missing evaluation evidence, with `proposed_spec: null` and review state `not_needed`; this is not an instruction to repair the source or evidence that a user rejected a proposed repair.

## Root cause and five whys

The root cause of the misleading completion impression was **using source-authoring closure as the leading answer to an outcome that also depends on separate behavioral qualification**. A contributing cause was the absence of a bounded cross-workflow status lookup before that answer. The evidence supports this operational explanation; it does not establish an internal psychological diagnosis.

| Why | Evidence-backed answer | Prevention that follows |
| --- | --- | --- |
| 1. Why did the response sound as though the work was done? | I led with “already authored” and “no package edits,” leaving missing evaluation as a later qualification. | Lead with the status of the requested outcome and separately name the completed authoring scope. |
| 2. Why did I conclude no further authoring work was needed? | Current package/specification bytes matched a published baseline, and the inspected instructions contained the requested extension. | Preserve this useful no-edit decision, but do not let it stand in for verified behavior. |
| 3. Why was verification not part of that leading conclusion? | The [readback script](inputs/11-readback.py) reads authoring references/manifests and hashes. It has no validator-report, scenario-inventory, or execution-outcome input. | Treat that result as byte custody only; resolve verification obligations separately before delivery. |
| 4. Why was missing verification merely handed off? | Builder was correctly restricted to authoring and manual handoff, but I did not pair that boundary with a complete statement of outstanding outcome, active evaluation, owner and next action. | Ending the current owner's authorized work must preserve unresolved obligations explicitly, without running another owner's workflow. |
| 5. Why could those narrower facts support an overbroad impression? | Completion remained a model-composed narrative. No executed cross-workflow reduction tied that narrative to the complete required evidence inventory. Existing prose already warns against the substitution. | Apply a deterministic claim/evidence reduction and report its scope; reserve protected acceptance for qualified Rust authority. |

The third why does not identify a defect in the custody helper: it intentionally performs custody rather than quality evaluation. The failure was in how I used and communicated its limited result. The fifth why describes this observed path, not proof that every DevForgeAI workflow lacks enforcement.

### Separate causal chain: why qualification remained incomplete

Three permitted native pilot commands exhausted the selected 120-second budget before required outputs were delivered. Initial attempt-001 initialization errors had been retained and attempt-002 runs were separately approved. Those distinct failures must not be collapsed into one product defect. The [trial policy](inputs/21-trials.md) calls 120 seconds a default execution ceiling, overridable by an explicit recorded trial requirement; it is not a universal QA-product response-time requirement.

The native observations show repeated resource inspection before delivery: six completed commands in QPV-01, eight in QPV-02, and six in QPV-06. Inspection overhead, workflow length, model response latency, and orchestration overhead are plausible contributing hypotheses. The retained observations do not isolate their contributions, establish a source defect, or prove a larger budget would finish. No controlled timing comparison was run in this RCA. Do not prescribe a shorter skill, a different model, or a larger timeout as a confirmed remedy.

The remaining 39 scenarios also need fixture/campaign work. Increasing the budget on three pilots cannot itself complete the required 42-scenario campaign. The record does not prove the 39 unattempted scenarios were impossible to execute.

## Concrete recommendations for dev

The development and operational versions of all eight inspected dev resources have identical captured hashes. The existing [failure-delivery instructions](inputs/35-failure-delivery.md) already prohibit COMPLETE with unperformed required QA. The [implementation reference](inputs/34-implementation.md) already requires actual native checks, and the [delivery template](inputs/37-delivery.md) already lists required checks and gaps. Adding another general “verify before complete” warning would not address the branch that failed here.

The following are proposed, bounded edits to `src/agents/skills/dev/`. No edits were applied. Authoring/testing this skill package remains separate from dev's ownership of ordinary product QA. Operational copies require a separate authorized installation step.

| ID / development file | Exact behavior to add | Observable output / failure handling |
| --- | --- | --- |
| D-01 `references/implementation.md`, after reuse assessment | When requested behavior already exists, retain it and enter the same requirement-verification path used after new implementation. Do not manufacture red by breaking correct code. Reuse prior checks only after candidate, spec, test, tool/platform and scope bindings are confirmed. Run missing in-scope product checks under existing authorization. | Slice record says `source_action: reuse` or `no_change`; traceability still lists every required check. Missing checks prevent overall COMPLETE even when `changed_paths` is empty. |
| D-02 `references/context.md` and `assets/traceability.md` | Separate each requirement's implementation state from its verification state. Preserve its ID, specification locator/hash, required platforms, required methods, case IDs, evidence references and unmet obligations. An implementation path/resource mapping satisfies only the implementation column. | No row becomes verified solely because a path exists or a hash matches. Missing oracle/method/platform stays an explicit gap. |
| D-03 `references/evidence-resume.md` | Before final reporting, inspect explicitly linked evidence and the selected target's established evidence directory for matching completed or active runs. Match candidate/spec/scope identities, not just newest filenames. Read existing records without invoking their producer, consuming a new approval, changing results, or repairing findings. | Record consulted paths/hashes, snapshot time, active or completed state, and conflicts. If discovery is ambiguous, inaccessible, or concurrent, say so and limit the claim to the observed snapshot. Never claim “never evaluated” from “not evaluated in this invocation.” |
| D-04 `references/failure-delivery.md` | Apply the COMPLETE/PARTIAL/BLOCKED decision before every final response, including no-change, reused-source and resumed branches. Report source outcome, verification outcome and external acceptance separately. For own in-scope product QA, continue available work; for a separately owned evaluation, preserve handoff and overall unproven status. | Leading sentence states actual scope and unresolved outcome. BLOCKED requires identifying why no remaining selected work can proceed; one unavailable platform does not block independent ready work. |
| D-05 `assets/delivery.md` | Add `source_action`, `verification_outcome`, `evidence_as_of`, `required_inventory_ref`, `qualified/required counts by evidence class`, `active/conflicting runs`, and `remaining owner/action`. Keep existing overall development status and external acceptance fields. | “No changes” and “report delivered” cannot serve as overall status. Counts of grader self-tests, controls, product units and native scenarios are separately labeled. |
| D-06 `assets/checkpoint.md` and `references/evidence-resume.md` | For a timed-out or interrupted operation retain attempt ID, exact command, selected timeout, start/end, last observed stage, owned process state, available artifacts, missing outputs, next safe action and retry authorization basis. | A checkpoint can resume justified work; it cannot turn a partial attempt into a passing whole scenario or erase the earlier timeout. |

For D-03, a read-only lookup is not permission to automatically invoke skill-validator, adopt its proposal, or launch repairs. Do not change builder's authoring-only ownership to fix this incident. For an ordinary dev product task, its own required tests remain dev's responsibility; no package validator is introduced as a product-test prerequisite.

Proposed addition to dev's final-report rule, ready for a later authoring task:

> Apply requirement accounting even when no source edits are needed. State the source result and verification result separately. Existing files, matching hashes, successful packaging, an AUTHORED record, or a completed report cannot satisfy a required behavioral check. Reconcile relevant current evidence without executing another owner's workflow. Continue required product QA within current authorization; otherwise name the exact remaining obligations, owner and blocker. Use COMPLETE only under the existing complete-evidence rule. Lead the final response with that scope-qualified disposition.

## Framework prevention within terminal constraints

### F-01: Separate status dimensions in evidence and consumers

Keep authoring-v1 meanings unchanged. Add a separate completion assessment keyed by candidate digest, specification digests, selected-scope digest, required-case inventory digest, policy identity and required platform set. Retain independent fields for source delivery, evidence availability, evaluation outcome and protected framework acceptance. Include evidence snapshot time, unresolved case IDs, active run IDs and concrete next owner/action. Missing fields or unknown schema versions are invalid input, not defaults to success.

A successful authoring record may support another authorized edit while evaluation remains INCOMPLETE. A completed report may report FAIL or INCOMPLETE. A no-change source decision must not set evaluation PASS. Neither phase progression nor external acceptance may be inferred from those local records.

### F-02: Implement the following reduction in compiled Rust

This is an implementation contract, not an available command. The currently inspected Cargo package is `devforgeai-index`; its [README](inputs/06-README.md) and [library](inputs/07-lib.rs) expressly exclude framework acceptance authority. The [Rust authority design](inputs/04-devforgeai-codex-rust-enforcement-design.md), especially sections 4–8, specifies the separate protected authority. This RCA does not claim it exists or qualify it. Do not add protected policy decisions to Python or repurpose the index daemon as authority.

Inputs: an explicitly selected required inventory; protected policy/build identity for authoritative use; exact candidate/spec/test/fixture/grader digests; platform and tool bindings; every cited attempt and required output; intended completion claim; prior accepted authority revision when requesting a protected transition. Inputs are local file references or the design's authenticated local service request; no MCP/browser dependency.

Output: a machine-readable assessment containing each missing, invalid, failed, conflicting, stale or unexecuted obligation with its reason and source reference; independent source/evaluation states; input digests; and the permitted scope of any completion claim. An authoritative receipt, if allowed, is issued only by the service under its protected policy. A standalone draft report remains evidence.

Deterministic rules, in order:

1. Reject duplicate keys, unknown schemas, invalid references, escaping paths, mismatched bytes, conflicting duplicate case outcomes, and absent/unresolved required inventory. Do not reduce malformed evidence as PASS. An input failure cannot erase a separately retained confirmed defect.
2. Match evidence to the selected candidate/spec/test/fixture/tool/platform and permitted policy. Mark mismatched evidence stale; retain it as history. Distinguish source manifest equality from proof of execution.
3. For each required case, demand the predeclared observations and output artifacts from its actual attempts. No attempt, timeout, unknown termination, incomplete required report/fix, or unavailable platform leaves it unqualified. A negative fixture can qualify when it produces the expected rejection and all its required outputs; it need not return product PASS.
4. Count unique required cases, including required nonpasses. Keep unit, scenario, helper/control, native/platform and code-coverage inventories separate. A helper or control cannot fill a native case slot. Retry history cannot add cases or erase unresolved failures.
5. For an assessment with valid inputs, a confirmed mandatory failure yields FAIL; otherwise missing required evidence yields INCOMPLETE; only complete satisfying evidence yields PASS. Independently evaluate each valid metric under the selected project's exact threshold and denominator policy. A numeric floor never waives a mandatory missing scenario.
6. Permit development COMPLETE only when every selected deliverable and mandatory check is satisfied and no required work remains. Distinguish that from authorized protected acceptance. If the required authority is unavailable, issue no authority receipt; local work may continue where permitted, with external acceptance NOT_EVALUATED.

These checks cannot establish semantic truth merely by reading agent-authored JSON. The future authority must bind a trusted required inventory, run or authenticate the actual producers under its approved policy, independently inspect referenced observations, and qualify its adapters. An unsigned model assertion `scenario_passed: true` is insufficient. Freeform chat cannot be made universally truthful by a shell hook. Consumers of authoritative completion must verify the service receipt or query protected service state; a workspace file named COMPLETE is not that state.

Implementation boundaries remain explicit: this analysis does not select a new authority crate destination, IPC schema version or installation identity. Those decisions belong to the separately selected authority specification/implementation task; F-02 is not an implementation-ready service package by itself. The reduction and acceptance obligations above can be implemented and tested through Rust unit/integration tests and local terminal commands once that scope is selected. No unimplemented CLI invocation is presented as runnable here.

### F-03: Make bounded evaluation planning accountable

Before a native campaign, declare per-case workflow stages, outputs, whole-command ceiling, child-operation bounds, allowed effects and attempt policy. Distinguish a harness safety ceiling from a specification performance limit. A ceiling timeout alone is incomplete evidence; a failed specified response-time requirement requires a valid measurement against that explicit requirement.

Use a declared feasibility pilot to measure stage timestamps and delivered artifacts, preserving its result even if it times out. A subsequent budget change is a new recorded trial requirement and authorization decision where required; it does not modify the original result. Instrument observable tool/test launches and artifact writes through the terminal harness. After a terminal product-test stop, permit only the specified containment, cleanup, evidence and report/fix work; after parent timeout, only known-owned recovery is permitted. A report merely announcing intent is not a delivered report.

For this campaign specifically, an authorized continuation must recheck the exact source/spec/bundle identities, retain both prior attempts, choose justified budgets, complete the remaining 39 scenario fixtures and all required variants, and obtain complete outputs for the three incomplete pilots. Unchanged identities may use the validator's selected-resume contract; changed inputs require a fresh linked run. No budget value or passing outcome is prescribed by this RCA.

## Required acceptance cases for the proposed prevention work

These are future test obligations, not executed tests or claims that the changes are installed. Skill instruction changes are authored in development source and independently evaluated. Rust behavioral implementation follows repository red → green → refactor → QA against its actual selected manifest/lockfile, with the repository's >=95% executed-line coverage and >=95% required-case pass rate, plus every mandatory invariant. Missing tools/coverage/native host evidence remain unperformed.

| Case | Exact fixture/trigger | Required observation |
| --- | --- | --- |
| RCA-01 No-change gap | Existing source/spec hashes match; one selected required native case lacks complete output. | Source action is no_change; development is not COMPLETE; missing case/owner/action are identified. Ordinary dev runs the missing case if authorized and ready. |
| RCA-02 Authoring-only boundary | Matching AUTHORED record; 42 required scenario slots, zero qualified; authoring-only request. | Authoring delivery may be complete; evaluated build is explicitly incomplete. No validator, repair or installation is auto-invoked. |
| RCA-03 Wrong evidence class | Supply 29 passing grader self-tests and 28 passing controls with no complete skill scenarios. | Counts remain three separate inventories; qualified scenarios remain 0/42. |
| RCA-04 Partial negative workflow | Correct mock detection/stop with no later test launch, but required report/fix absent. | Preserve the partial correct behavior; whole scenario remains unqualified. No invented source defect from timeout alone. |
| RCA-05 Active/newer evidence | Matching authoring exists; matching validation is active with one timed-out attempt and no final report. | State active/incomplete evidence as of read time, do not claim never tested or invent the future final verdict. A later completed report is a new observation. |
| RCA-06 Stale/conflicting evidence | A PASS report binds another candidate or two incompatible records bind one execution identity. | Stale result cannot qualify current bytes; conflict is surfaced and blocks qualification. No newest-filename-wins rule. |
| RCA-07 Retry accounting | Retained timeout, then an authorized new attempt completes against the selected candidate. | Original timeout stays; case counted once; full required observations and unresolved-flakiness policy determine qualification. |
| RCA-08 No fabricated red | Existing correct product passes current required tests without source edits. | Record reused implementation and actual verification; do not modify product to force a failure. COMPLETE remains possible when every selected obligation is met. |
| RCA-09 Independent work | One required platform unavailable, another has ready authorized checks. | Execute independent work; retain the missing platform and do not claim overall COMPLETE. Do not label all remaining work impossible without evidence. |
| RCA-10 Rust authority unavailable | Local records say COMPLETE but required protected service cannot be reached. | No acceptance receipt or protected transition; useful permitted draft work can continue. |
| RCA-11 Literal terminal paths | Local candidate/evidence paths contain spaces and Unicode; missing/wrong destination variant. | Native argument passing preserves full paths; exact required artifacts are read back. Missing/misplaced output leaves its obligation unverified. |
| RCA-12 Complete authorized outcome | Current complete inventory, authentic execution evidence, required outputs, qualifying metrics/platforms, no mandatory gaps. | Development COMPLETE is permitted. Protected acceptance is separate and requires its actual qualified authority. |

## Corrected handoff and remaining work

For the QA package, the correct next owner is skill-validator for separately selected continuation of incomplete evaluation. No dev source-remediation request is justified until a specific source defect is demonstrated. The already delivered source and prior failures should remain intact. The report's readiness BLOCKED describes the missing evaluation prerequisite; it must not imply all unattempted fixture work is technically impossible.

For preventing this reporting failure, the immediate change target is the dev development instruction/template set listed in D-01–D-06, with independent skill evaluation after authoring. The framework changes are F-01–F-03, with compiled Rust owning protected decisions. These are recommendations only. This RCA completes the requested analysis; it does not complete QA native evaluation or implement the prevention controls.

My corrected user-facing status would be: “The requested QA source revision is already authored and unchanged. Its evaluated build is INCOMPLETE: 0/42 complete scenarios are qualified after three bounded pilot timeouts. No source defect is confirmed. Continue independent evaluation under its retained identity and budget rules; no source repair or installation is currently justified.”
