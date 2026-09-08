# Proposed validation policy revision VPR-1

Status: **PROPOSED — awaiting explicit specification acceptance.** Authored 2026-09-08. This is an amendment for review, not an operative policy or a validation result.

Validation status: Not performed. Hook status: Design only.

## 1. Identity and purpose

Extend the existing `skill-validator` specification with two validation policies: **Routine validation** for bounded change verification and **Full qualification** for the complete applicable campaign. The validator remains an evaluator of exact, read-only candidates; `skill-builder` remains the author. Human acceptance and release decisions remain external.

The selected source is DevForgeAI commit `9970e92db7d824dea0c49e1a61a122480f2aa8b5`. The governing design is [skill-validator-design.md](../../skill-validator-design.md), read with the [runtime alignment amendment](../../history/skill-utilities-runtime-alignment-20260908/design-amendment.md). The [source inventory](source-inventory.json) binds original requirements, cases and prior records. Concurrent uncommitted shared-contract edits are preserved and are not selected by this proposal. The original design's authored/unaccepted status is retained; this proposal does not invent earlier human acceptance.

## 2. When each policy applies

| Policy | Selection rule | Permitted result claim |
| --- | --- | --- |
| Routine | A named local iteration with a complete, reviewable impact map; all applicable change rules below fit a bounded selection; no Full trigger is being claimed satisfied. | The named changes meet the named requirements under the recorded checks and selected native observations. |
| Full qualification | First qualification of a skill; first qualification for a provider/client/installation configuration; a request to qualify, adopt or release a candidate; a consequential change to authority, trust, enforcement or transfer semantics; or impact that cannot be bounded. | The exact candidate meets the complete applicable qualification requirements in the tested environment, with stated sampling and evidence limits. |

Routine can supply intermediate feedback for an unqualified candidate, including while a Full trigger is outstanding. Its report must carry `qualification_required: true` and the reason. It cannot discharge that trigger or authorize an adoption/release claim. A new version of the provider/client or installation mechanism needs Full qualification before support is claimed for that configuration; unchanged capabilities can still receive explicitly scoped routine feedback.

Select Full for an ambiguous generic validation request unless the request and impact record explicitly establish a Routine iteration. A user-requested Full campaign cannot be reduced to Routine because of cost, unavailable tools or the current budget. Report its missing evidence instead. Unknown impact, conflicting requirements, a missing comparison base or an unreviewable dependency closure prevents a Routine PASS.

Accumulated edits are compared both with the immediate previous candidate and the last qualified candidate, when one exists. An individually small edit does not hide a cumulative change to a protected contract. Absence of a prior qualification is recorded as `absent`, never inferred from a structural or Routine PASS.

## 3. Required inputs and selection record

T01–T02 additionally bind the accepted policy revision and exact bytes; requested claim; candidate and comparison-base identities; last qualification identity/status; changed requirements and paths; transitive dependency map; environment changes; and a coverage row for every original case and every R01–R10 criterion. Coverage rows identify the triggering rule, selected cases/arms/variants, rationale, prerequisites, and evidence required for closure.

Use separate fields for **selection** and **observed outcome**. Proposed selection values are `required`, `not_selected_by_routine_policy`, and `not_applicable_to_scope`. A policy exclusion needs an accepted policy rule, exact change evidence and an independent reviewer's agreement. A scope exclusion needs the pre-existing case applicability predicate and its evidence. An unselected case has no observed PASS; its observation remains NOT_RUN. NOT_APPLICABLE retains its original scope meaning.

Selection is frozen before observation. Discovering an omitted affected requirement invalidates that selection: retain it, issue a new affected iteration, and preserve all earlier evidence. Budgets constrain admission, not which requirement is applicable. Required independent review, model continuations, nested workers, graders, retries and receiving calls must be counted before admission.

## 4. Required coverage and enforced phases

**W1, P1–P6 and T01–T12 remain Enforced.** This revision changes conditional coverage inside tasks; it does not make phases optional. No required phase disappears from the plan, phase record or final report.

| Phase / task | Routine required work | Full qualification required work |
| --- | --- | --- |
| P1 / T01–T02 | Bind authority, exact inputs, impact closure, policy and complete selection record. | Bind authority, exact inputs and the complete applicable campaign. |
| P2 / T03 | Run all source structural checks S001–S013, with genuine existing applicability rules. Inspect selected installed packages when installation is involved. Execute additional relevant deterministic regression checks under an authorized evaluation allocation. | Same source checks plus all applicable installed/resource and deterministic regression checks. |
| P3 / T04 | Fresh independent review of the change, its transitive context and all R01–R10 invariant anchors. Examine every criterion; focus detailed review on changed or dependent clauses. Every criterion retains its own evidence/outcome. | Fresh independent review of all applicable R01–R10 anchors across the complete candidate. |
| P4 / T05 | Produce and discharge the native selection decision. If native work is selected, establish the actual isolation, resource visibility, ownership, readiness and budgets for every selected attempt. If none is selected, retain the independently reviewed no-native decision and its rule evidence. | Establish actual isolation, visibility, ownership, readiness and budgets for the entire applicable native campaign. |
| P4 / T06 | Perform C observations needed by selected native cases; every new installed candidate/environment used by B or A needs matching C evidence. | Perform all applicable C cases for every required candidate/installation/environment stratum. |
| P4 / T07 | Run affected B cases and candidate/baseline pairs selected by the rules below, including affected negative and previous failure cases. | Run all applicable B cases and their required candidate/baseline arms, variants and independent semantic grades. |
| P4 / T08 | Run the A categories affected by selection/activation changes; retain the decision for every category. | Run the complete applicable explicit, direct, indirect and near-miss/negative A set. |
| P5 / T09 | Bind selection, actual outcomes, gaps, freshness and precise Routine claim; independently assess the selection rationale. | Bind complete applicable coverage, actual outcomes, gaps and precise qualification claim. |
| P6 / T10–T12 | Deliver results, bounded repair/enhancement specification and an honest prepared handoff, including unselected coverage and qualification debt. | Deliver the same artifacts and, when transfer is part of the skill's required contract, evidence of actual receiving execution and its disposition. |

For Routine T04, always inspect R01 scope, R02 completion, R03 authority, R04 phase/failure transitions, R05 resource routing, R06 supplied-data boundaries, R07 provenance, R08 accessibility of relevant instructions, R09 honest outcomes and R10 enforcement/handoff. These are the existing rubric IDs. Every applicable anchor affected by the change gets detailed examination; unchanged anchors get an explicit invariant check against the selected base and dependency map. Unreviewed applicable criteria are unavailable, not PASS or a fabricated scope exclusion. Missing context expands the review or blocks a Routine PASS.

If no C/B/A observation is selected, T06–T08 still produce separate selection/outcome records; P4 may close only as **selection obligation satisfied — no native observation selected**. This is not a native success result. If any native observation is required, an empty or missing run record cannot close that obligation.

## 5. Explicit change-impact rules

Take the union of every matching rule. Select all cases asserting affected requirements and all cases downstream of affected inputs, outputs, resources or transitions. Include prior failures for those requirements. A single convenient example is not enough when distinct affected failure branches exist.

| Rule | Change / evidence needed to apply it | Required Routine native coverage; escalation |
| --- | --- | --- |
| CI-01 | Spelling, formatting or non-operative commentary only; independent review confirms no changed instruction, metadata, resource resolution, example semantics or output meaning. | No native observations. All source deterministic checks and focused independent AI review still required. |
| CI-02 | Discovery name/description, invocation instructions, selection examples or registration exposure. | C for exact installation; A explicit invocation, direct request, indirect request and near-miss/negative cases for each affected boundary; B for any changed promised behavior. A new provider/client/installation support claim triggers Full. |
| CI-03 | Installed paths, dependencies, helpers, templates, assets, packaging or output destination. | C for every changed resource/path and relevant unavailable-dependency branch; affected downstream B cases. Add A where discovery/loading can change. Output-contract or trust changes also match CI-05/06. |
| CI-04 | Workflow, prompt semantics, missing-input handling or output quality. | C prerequisites; every affected normal, edge and negative B branch, including earlier failures, in candidate and preserved `old_skill` arms (or `without_skill` for a new target). Add affected A categories if selection meaning changes. Unknown dependency closure triggers Full. |
| CI-05 | Authority, write/process/client-state boundary, supplied-data trust, accepted decisions, enforcement, evidence reducer, gate or runtime transport semantics. | Routine diagnostics may run affected C/B/A and denial/failure cases, but Full is required before qualification or adoption of the changed contract. No Routine exemption can weaken a protected prerequisite. |
| CI-06 | Handoff shape, consumer prerequisites, receipt meaning, completion/transfer rules or receiving-skill contract. | Affected producing cases, delivery/failure cases and actual receiving-transfer exercise using eligible output from that producer; required fresh receiver and grading are counted. Full remains required before qualification/adoption of the transfer change. |
| CI-07 | Case/fixture/rubric/applicability or requirements change. | Preserve the earlier oracle and results. Review the proposed requirement change before use; rerun every affected observation under a new identified iteration. Weakened acceptance criteria require explicit specification acceptance; uncertainty triggers Full. |
| CI-08 | Unresolved interactions between changes, unknown effects, unexplained cumulative drift, an unobserved relevant environment change or missing base. | Do not issue Routine PASS. Select Full or report insufficient evidence until impact can be established. No inference of equivalence from equal filenames or a model assertion. |

C remains a prerequisite for B and A on the matching candidate/environment. In an accepted Routine plan that selects A but no B, the independently reviewed B-selection record discharges only the B task's selection obligation; the proposed policy-aware gate may then admit A after matching C. It must not call this B PASS. If B is selected, preserve its required safe dependency conditions; a failed or unavailable selected prerequisite cannot be converted into an exclusion after observation. Full retains its complete applicable C, then B, then A sequence. These conditional transitions require the versioned implementation in section 8; they are not supported merely by this proposal.

Preserve independently permitted work and P5/P6 failure reporting when a dependency is unavailable. A comparison's failing baseline is retained and does not by itself fail a conforming candidate; an incomplete baseline prevents a comparative conclusion and prevents completion of a required pair.

## 6. Exact meaning of passing results

An individual PASS still means a predefined condition was observed with complete supporting evidence. FAIL, NOT_RUN, COULD_NOT_RUN and NOT_APPLICABLE retain their meanings. Reporting completion remains separate from passing.

**Routine PASS** requires: valid accepted Routine selection; complete deterministic checks; independent focused AI review and approved impact coverage; all selected native cases, required pairs and grades complete; no applicable required candidate or evaluation-protocol failure; no missing required observation; and exact current bindings. The claim is: “For candidate X and changes D, requirements R passed coverage C under policy P in environment E.” It does not establish whole-skill native behavior, implicit activation when untested, qualification, release acceptance, cross-provider support or general improvement. Native groups without selection remain explicitly unobserved.

**Full qualification PASS** requires: deterministic and full independent AI evidence; every applicable original mandatory C/B/A case, variant, arm, prerequisite/control and independent grade; all required receiving-transfer evidence; no applicable required candidate or evaluation-protocol failure or missing observation; and current exact bindings. The claim is: “Candidate X met the complete applicable qualification requirements Q under policy P in environment E.” It supports the owner's qualification review, not automatic acceptance, certification, guaranteed behavior for unseen inputs or immunity from sampling limits. An improvement claim additionally needs the predeclared comparison criterion and complete, comparable arms.

Receiving-transfer evidence means the eligible producer output was actually delivered through the selected transfer mechanism to the named receiver; the receiver loaded the correct inputs and completed the required bounded action or produced the required observed negative disposition. A prepared handoff file, admission receipt or a separately invented receiver fixture cannot substitute. If required receiving evidence is missing, Full qualification cannot pass. Outcome expectations for deliberate negative cases remain case-specific; they are not rewritten to require success.

This is a native P4 exercise of the skill-under-test's transfer contract, completed before the evaluator's T09 qualification adjudication. P6 reports that evidence. The evaluator's own newly prepared T12 handoff does not recursively create another qualification campaign or receiving chain; any further receiving action needs its separately selected scope and allocation.

The proposed report has separate `policy`, `selection_status`, `validation_disposition`, `qualification_status`, `coverage`, `observations`, and `acceptance_status` fields. Qualification status identifies the exact last qualified bytes as current/stale/absent/unknown; Routine PASS never promotes new bytes into that record. Required failure yields `revise`; otherwise missing required evidence yields `insufficient_evidence`; complete evidence yields `suitable_for_stated_scope` with the policy-qualified claim above. Do not emit an unqualified “validated” or “all tests pass” summary.

## 7. Future validation examples — capture only

| Input | Required proposed behavior |
| --- | --- |
| Correct a spelling error without changing meaning. | Routine: all deterministic checks, focused independent AI and explicit no-native decision; no C/B/A PASS invented. |
| Change a trigger description. | CI-02 selects all affected A categories and C; near-miss timeout stays unavailable. |
| Fix a resource link or change a template field. | CI-03 selects actual installed resolution and dependent output cases; a source link check cannot replace C. |
| Change a clarification branch. | CI-04 selects the affected normal, missing-input and error branches in both arms. |
| Change who may approve a transition. | CI-05 records Full required even if focused diagnostic cases pass. |
| Change handoff output and run a receiver against a handcrafted substitute. | CI-06 receiving evidence remains missing; Full cannot pass. |
| Budget exhausted or a required grader unavailable. | Preserve required coverage and charges; report insufficient evidence. |
| Evaluate a legacy plan or load an unaccepted policy ID. | Apply the originally selected requirements; deny new exclusion semantics. |
| Discover a missed dependency after a Routine result. | Preserve the original result, mark its affected claim stale and freeze a new iteration. |

## 8. Tools, enforcement and implementation ownership

This proposal supplies no runnable schema, gate, hook or controller amendment. The currently selected reducer/runtime must not be fed these draft fields as if they were supported. An unsupported accepted policy remains non-executable until its implementation and required independent verification exist.

H1–H5 retain their existing protected runtime ownership, selected event/matcher/configuration arrangements and uncovered-path limits. Proposed additions: H1 binds policy acceptance, selection and complete budget before admission (W1/P1/T01–T02); H2 requires deterministic/AI and coverage decisions (P2/P3/T03–T05); H3 checks typed required-native dependencies or the accepted no-native decision (P4/T06–T08); H4 rejects unsupported claims and binds all observations (P5/T09); H5 requires failure/limit-aware deliverables and creation-time handoff facts (P6/T10–T12). Every existing enforced item remains mapped.

Each proposed gate reads owner-controlled evidence tied to the run, policy, candidate and exact prerequisite. Missing, stale, wrong-owner or malformed evidence blocks the dependent claim/action, with a specific reason; independent reporting remains available. A worker-written selection cannot grant itself exemption. Recovery requires corrected input or a newly accepted selection within the existing budget and deadline. No override, new event, hook installation or semantic honesty guarantee is created. Feasibility of these new semantics is unverified; enforcement is requested, not claimed active.

After explicit specification acceptance, the DevForgeAI owner would update the canonical validator entrypoint, native/results/enforcement references, plan/result assets, deterministic reducer and proposed selection-regression cases. Shared contract changes need their designated integration owner. DevForge owns runtime/parser/admission implementation and receipts. Generated installed copies refresh only after reviewed source integration. All such work needs its own existing or explicitly supplied authority and budget; this document grants neither.

## 9. Measurement pilot relationship

The [pilot allocation](pilot-allocation.md) is a separate, bounded **cost measurement** experiment. It samples common cost components; it is neither Routine PASS evidence for this revision nor Full qualification of either utility. Its specimens, grades and incidental resource/activation observations cannot close original mandatory cases. Policy acceptance, pilot design acceptance and pilot execution authorization are separate recorded decisions.

## 10. Preserved cases, results and budget

All 28 original SV-001–SV-028 cases remain byte-identical, with their original assertions and statuses. All builder cases, native variants, controls and receiving requirements in the preserved complete allocation remain intact. Full qualification retains the complete applicable inventory. Routine adds a selection overlay only after acceptance; it does not delete those cases from the catalog.

Historical FAIL, NOT_RUN, COULD_NOT_RUN, timing deviations, contaminated/late attempts and reviews keep their original inputs and policy. There is no retroactive recalculation, promotion, refund or rewriting of a failed case. A new accepted policy creates a new plan/iteration; it does not mutate the original 1,099-unit proposal or make it the cost of every future change.

The current approved limits remain **24 counted calls, 600 seconds per whole attempt and 14,400 seconds per campaign**. The preserved ledger has **24 charged and zero remaining**. Earlier requests to enlarge the budget remain unapproved. This revision proposes no increase or reset. Acceptance alone cannot fund a pilot, implementation, independent AI review or native run.

## 11. Acceptance and activation

The review decision must identify this proposal revision and its final SHA-256 manifest, and record accepted/rejected/deferred items in the [requirement diff](requirement-diff.md). Until explicit specification acceptance, every current mandatory case and required evidence group remains operative under its original selected specification.

After acceptance, implementation, independent checks, source/installation selection and a separately authorized execution allocation are still required. Legacy plans retain legacy semantics. The accepted specification can be available for authoring without falsely claiming the runtime enforces it. Do not merge this proposal into active requirements, refresh operational skills, authenticate clients or execute the pilot as a consequence of merely receiving review comments.

## 12. Authoring receipt and prepared transfer

Only this proposal directory and its external custody records were authored. Existing source skills, active specification, cases, runtime, installed copies and historical evidence were preserved. Authorship and document readback do not establish independent review, validation or acceptance. The [prepared handoff](prepared-handoff.md) identifies the next owner and unresolved execution conditions; no receiving skill was invoked.
