# Proposed validation policy revision VPR-2

Status: **Reviewable draft; not accepted, implemented or evaluated.** Supersedes VPR-1 as a proposal only. Earlier draft commit: 5eaa7c081fe34e3f97cd965b7d5d0ec300775bf9. Original selected skill/specification source: 9970e92db7d824dea0c49e1a61a122480f2aa8b5. The [source inventory](source-inventory.json) retains exact original references, all cases, the historical allocation and this revision's audit. No operational skill or runtime is changed.

Validation status: Not performed. Hook status: Design only.

## 1. Purpose and three distinct decisions

Routine validation should make bounded maintenance deliverable. Full qualification establishes a broader, exact-candidate evidence claim. Neither substitutes for the owner's authority.

| Decision | Evidence and authority | Permitted claim |
| --- | --- | --- |
| Accept and install a scoped Routine update | Routine PASS, the eligibility conditions below, and the existing owner's installation/adoption authority. One ordinary owner decision can cover acceptance and installation; prior conditional authorization need not be requested again. | “Update D to candidate X was accepted for scope S after Routine validation under policy P.” |
| Fully qualify a candidate/environment | Full qualification PASS covering the complete applicable requirements for exact candidate X and environment E. Human acceptance remains a separate fact, though the owner may record both in one decision. | “Candidate X met Full qualification requirements Q in environment E.” |
| Make a release or support claim requiring Full | The declared release/support contract explicitly requires Full, the claim asserts qualification for new bytes/environment, or it introduces a genuinely new supported capability/environment contract. Current matching Full evidence and the owner's release authority are required. | The precise supported/qualified scope backed by that evidence. |

A routine update may be accepted and installed without Full merely because it is being adopted, installed, versioned, tagged or distributed within an already accepted scope. It cannot carry a “fully qualified” claim for its new bytes. If a release contract requires Full, routine distribution cannot be used to bypass that contract. Record the actual requested claim, rather than inferring one from the word “release.”

## 2. Policy selection and routine adoption eligibility

Select **Routine** when the requested work is a bounded update to an identified owner-accepted baseline, the changed requirements and their dependencies are understood, and the intended use remains inside that accepted capability/environment scope. The word “validate” is neutral: inspect the requested scope and available change/base evidence. Ask only if an unresolved claim or scope would change the selection. Do not default to Full solely because that word appears.

Select **Full** for first qualification; an explicitly requested qualification; a genuinely new supported environment/capability scope; consequential changes to authority, enforcement or receiving-transfer semantics; a release/support contract that requires it; or impact that remains unbounded after the compatibility/impact assessment. First qualification remains Full even if earlier unqualified local use or Routine results exist.

After Routine PASS, an owner may accept and install the update when all of the following hold:

- The exact baseline, update, accepted scope and authorized destination are identified; all selected required evidence is complete and current.
- No unresolved required failure, missing observation, incompatibility, consequential cumulative interaction or Full trigger affects the intended adoption scope.
- Installation preserves the reviewed package bytes, selected resources, effective controls and supported destination mapping; required post-install identity/resource/compatibility checks complete before enabling the affected use.
- The decision records that these new bytes are routinely accepted, with their qualification status and limits. If the baseline has no Full qualification, that absence remains visible; Routine cannot manufacture it.

The owner can authorize installation conditional on these checks in the original maintenance assignment. A mismatch blocks the affected use and invokes the existing recovery/rollback arrangement; it does not require a new ceremonial approval for every successful check. If there is no identified accepted baseline or bounded scope, do not invent one to issue Routine PASS. Safe partial diagnostics can still proceed with an honest limitation.

## 3. Lineage and cumulative changes

Keep two separate identities in the existing results/acceptance record: the **last fully qualified candidate/environment** (or absent/unknown) and the **current routinely accepted candidate**. Link subsequent Routine decisions and evidence from the qualified anchor, or from the explicitly accepted unqualified baseline when none is qualified. Never move the qualified anchor on Routine PASS.

At every Routine update, mechanically compute the immediate diff and the cumulative diff from that anchor; include changes to effective configuration, installation and client/provider behavior. Review the union of affected requirements and transitive dependencies, not just the newest patch. Check interactions between trigger promises, instructions, resources, outputs, trust/authority and transfer. Prior observations may be referenced only where their exact input/capability scope remains unchanged and their freshness condition still holds; they are not relabeled as full evidence for different bytes.

An unresolved interaction, a new authority/transfer meaning, an unsupported capability or an unbounded cumulative effect triggers Full or blocks adoption pending resolution. Several demonstrably independent spelling/resource/prompt corrections can remain Routine with combined regression coverage. There is no arbitrary “Full after N edits” rule, and accepting one routine edit does not reset the cumulative anchor or erase qualification debt.

## 4. Enforced phases with conditional coverage

**W1, all six phases P1–P6 and all twelve tasks T01–T12 remain Enforced.** Every task has a result or an explicit conditional-coverage/dependency disposition. Unselected observations never become PASS.

| Phase/tasks | Routine obligation | Full obligation |
| --- | --- | --- |
| P1 / T01–T02 | Bind owner, baseline/candidate, accepted scope, requested claim, policy version, immediate/cumulative impact and selected evidence. | Bind the same facts and the complete applicable qualification assertion/observation map. |
| P2 / T03 | All applicable S001–S013 source checks; affected mechanical regressions; required installed identity and compatibility checks. | Complete applicable deterministic/mechanical coverage. |
| P3 / T04 | One fresh independent AI review of changed and dependent clauses, the coverage decision and R01–R10 invariants. Keep per-criterion evidence/outcomes; detailed review focuses on the affected anchors. | Independent AI review of all applicable candidate/contract anchors. A separate reviewer per criterion is not required. |
| P4 / T05 | Establish the selected environment and actual boundaries where native work is required; otherwise record the applicable no-native decision. | Establish every required native environment/attempt and dependency. |
| P4 / T06 | C observations for affected installed resources and prerequisites of selected native behavior. | All applicable C assertions, with permitted sharing described below. |
| P4 / T07 | Affected B normal/edge/failure behavior; paired candidate/baseline evidence where behavior or comparative claims require it. | All applicable B assertions and required candidate/baseline comparisons. |
| P4 / T08 | Affected activation categories and negatives selected by the impact rules. | Complete applicable explicit/direct/indirect/near-miss activation coverage. |
| P5 / T09 | Bind actual evidence, selection, gaps, freshness, cumulative impact and Routine adoption eligibility. | Bind complete applicable qualification coverage and limits. |
| P6 / T10–T12 | Deliver results, bounded repair/enhancement guidance and an honest prepared handoff, including adoption/qualification distinction. | Deliver the same plus the qualification disposition and required target receiving-transfer evidence already observed in P4. |

R01–R10 retain their existing rubric meanings and separate records. The focused reviewer checks authority, supplied-data boundaries, provenance, completion, failure paths and enforcement/handoff invariants even when not edited. Do not invent NOT_APPLICABLE for unreviewed applicable anchors. If context is insufficient, expand the review within its allocation or retain unavailable evidence.

Use the existing plan/results fields with one versioned selection map: required; not selected by accepted Routine policy; or genuinely not applicable to scope. Each exclusion cites the impact rule and evidence. Unselected native outcomes stay NOT_RUN; a genuine scope exclusion retains NOT_APPLICABLE. P4 completion without native selection means its selection obligation was satisfied, not that native behavior passed. The same independent T04 review assesses the selection; do not add another review round merely to approve its own map.

C prerequisites remain tied to the exact installed candidate and environment. Under accepted Routine rules, a reviewed unselected-B task decision can precede selected A after matching C; it is not B PASS. Selected prerequisite failures cannot be relabeled as exclusions after observation. Full keeps required C/B/A dependency ordering; evidence sharing cannot satisfy an earlier gate using a later observation.

## 5. Versioned change-impact rules

Take the union of matching rules and every affected regression/negative branch. Inspect both immediate and cumulative impact. Requirements, not a desired cost, determine applicability.

| Rule | Trigger | Required coverage / escalation |
| --- | --- | --- |
| CI-01 | Spelling, layout or commentary with no changed instruction, metadata meaning, resource resolution or output contract. | Complete applicable deterministic checks and focused independent review; no native run unless review finds semantic impact. Routine adoption eligible. |
| CI-02 | Trigger description, invocation wording or selection exposure changes. | Matching C; affected explicit/direct/indirect/near-miss A cases, including the adjacent exclusion boundary; B if promised behavior changes. Routine eligible when supported scope/controls remain bounded. |
| CI-03 | Resource path, dependency, helper, template, packaging or output destination changes. | Deterministic resolution/identity and mechanical regressions; actual affected installed C path and downstream B behavior; A only if discovery can change. Apply CI-06 for transfer semantics. |
| CI-04 | Bounded prompt/workflow, clarification, output-quality or failure-handling change inside accepted scope. | C prerequisites, affected normal/edge/negative B cases and prior failures; matched candidate/baseline arms when the behavior changes or a comparison is claimed. One bounded independent batch may grade both arms with separate judgments. Add A for selection impact. |
| CI-05 | Consequential authority, permission, trust, enforcement, gate or evidence-authenticity semantics change. | Full for adoption of that changed contract; mechanical denial/identity tests, independent semantic review and representative actual native control behavior. Focused diagnostics alone do not authorize the affected adoption. |
| CI-06 | Receiving prerequisites, accepted output meaning, receipt authority, transfer/completion semantics change. | Full for adoption of the changed contract; producer/consumer contract checks plus actual eligible producer-to-receiver transfer and required failure paths. A spelling fix in handoff prose follows CI-01 when semantics are unchanged. |
| CI-07 | Client/provider/installation/configuration change. | Apply CP-01–CP-04 below. Names or version numbers alone prove neither incompatibility nor compatibility. |
| CI-08 | Requirements, case/oracle or grading meaning changes. | Explicit specification decision before use; preserve original expectations/results and rerun affected assertions under a new revision. No silent weakening or retrospective PASS. |
| CI-09 | Unbounded impact or unresolved cumulative interaction. | Full or insufficient evidence; no Routine adoption while the affected claim remains unbounded. Multiple bounded edits alone do not trigger Full. |

## 6. Compatibility before escalation

Treat an environment as an explicit capability contract, not a version string. Compare provider/backend/model behavior, installation/discovery paths, resource resolution, tool/event schemas, output/usage capture, approval and sandbox behavior, authentication/state separation, and the APIs actually used by the skill. Mechanically record unchanged fields; investigate only changed or unknown dependencies.

- **CP-01 — Bound the change:** retain old/new client/provider/installer identities and effective configuration; use applicable official change information and local interface/source evidence. Map every changed/unknown capability to affected assertions. A new version label with identical relevant bytes is not a behavior change; changed executable bytes need compatibility evidence.
- **CP-02 — Mechanical compatibility:** check used schemas, resource/install mapping, parsing and control predicates with relevant deterministic regressions and negative inputs. These checks establish mechanical behavior only. Documentation or a version probe cannot establish effective native controls.
- **CP-03 — Actual compatibility:** for a changed executable client/provider/installer, observe a representative exact-installed load and completed bounded task, plus the applicable denial/failure/activation probe for each affected control or selection capability. Add affected paired B cases when provider/model behavior can change output quality. Record actual source visibility, capture completeness and any effective tool/configuration differences. Existing valid observations may cover unchanged components with explicit scope; an unknown changed component cannot be inferred compatible.
- **CP-04 — Decide:** Routine adoption is eligible if the used capabilities remain within the accepted environment contract, the affected compatibility/behavior observations pass, and trust, authority, enforcement and transfer meanings are unchanged. Use Full for a genuinely new provider/platform/install mechanism or supported capability contract without an established equivalence basis, consequential control/transfer change, or remaining unbounded impact. A compatible client patch or equivalent provider routing/configuration change can therefore remain Routine. A wholly new model/provider is not made equivalent by calling it a patch.

Do not run every compatibility permutation automatically. Select the distinct used capabilities and failure conditions whose change could affect this skill. A post-install check may share the same actual load/task observation when identities, conditions, timing and required outputs match.

## 7. Evidence allocation and Full qualification

Full means complete applicable **assertion coverage**, not an immutable number of calls or a fresh qualification of every child fixture. The [allocation audit](qualification-allocation-audit.md) explains all 1,099 historical proposed units and 907 fresh profiles. Original cases and assertions remain intact; proposed evidence-selection changes are explicit in the [requirement diff](requirement-diff.md).

Use deterministic tests for mechanical parsing, hashes, schemas, counters, graph/deadline rules and replay/mismatch handling. Use independent AI judgment for meaning, scope preservation, reasoning quality, instruction/data boundaries and artifact adequacy. Use actual native execution for what a skill selects, reads, creates, refuses, transfers or reports in its target environment and for representative integrations. A synthetic transcript can test a detector/reducer; it cannot prove a live clean negative, effective isolation, callback origin or receiving invocation.

Permit one observation to cover multiple assertions only when the frozen input/candidate/environment, prompt conditions, visibility, time/order and required evidence all match. Keep a separate result for every assertion and disclose correlated observations/sample counts. For incompatible fixture variants, changed targets, opposite arms or implicit activation needing an unforced prompt, retain distinct runs. Do not reuse a writable worker history as if it were a fresh independent attempt.

One fresh grader can assess a bounded pair or compatible batch with separate per-arm/assertion judgments, neutral labels where possible, adequate complete context and disclosed order/arm leakage. The grader must be independent of authors/measured workers. Deterministic mechanics need not receive a second AI grade. A child-output grade and a parent's interpretation of that output are different assertions: combine their review only when the reviewer can assess both from the proper raw evidence without circular self-review or premature gates. No recursive grader-of-grader campaign is required.

For validator self-evaluation, keep actual outer native observations where the source case asserts validator behavior, including all explicitly native workspace-allocation cases. Select inner work from the actual requested subtask and assertions. A generic validation request does not itself require a complete 17-run inner qualification. Real evidence bundles can be reused for adjudication cases when their exact scope matches; synthetic bundles are permitted only for explicitly synthetic/error-handling assertions. Retain representative actual nested review, result-return, failure reporting and receiving integration, and every source assertion that explicitly demands real inner execution. The audit does not authorize deleting any case or substitute fixture evidence for native claims.

## 8. Exact results and claims

Individual PASS, FAIL, NOT_RUN, COULD_NOT_RUN and NOT_APPLICABLE retain their meanings. A complete report may honestly contain failed or unavailable evidence. A failing baseline does not itself fail a conforming candidate, but a missing required baseline prevents completion of that comparison.

**Routine PASS:** accepted policy selection; complete required deterministic checks and focused independent AI review; all selected native/compatibility assertions, pairs and grades complete; no unresolved required candidate/protocol failure or missing observation; valid current and cumulative bindings. It establishes only the named update's compliance under the selected coverage. It can support scoped acceptance and installation under section 2. It does not confer Full qualification, general improvement, cross-environment support or unobserved activation.

**Full qualification PASS:** complete applicable deterministic, independent semantic and actual native assertion coverage, required candidate/baseline comparisons, controls and target receiving transfer; no required candidate/protocol failure or missing observation; current exact candidate/environment bindings. It supports the precise qualification claim, subject to sampling limits. Human adoption/release authority and broader support remain separate.

Receiving evidence must use eligible output actually produced by the measured target, delivered to the named receiver, with observed loading and the required completed action or expected negative disposition. A prepared handoff, receipt alone or handcrafted replacement output cannot establish that transfer. This target integration is observed in P4 before T09 adjudication. The evaluator's own prepared T12 handoff does not start another qualification chain.

Keep policy/version, selected assertions, observed outcomes, validation disposition, current routine acceptance and last qualified identity in existing plan/results/handoff records. Derive status and coverage mechanically where possible. Required failure means revise; otherwise missing required evidence means insufficient evidence; complete evidence means suitable for the stated policy/scope. Do not summarize routinely accepted bytes as fully qualified.

## 9. Authentication and evidence isolation

Independent evidence requires appropriate separation of task inputs, writable workspace/output, history/memory and reviewer context. It does **not** inherently require a new browser login per generation, continuation or fresh context. Authentication identifies an account/session; it does not establish review independence or filesystem isolation.

Official documentation describes cached login reuse, automatic token refresh, and file/OS credential-store choices. This supports reuse as a lifecycle capability, not proof of isolated evidence. [Authentication](https://learn.chatgpt.com/docs/auth#login-caching) [Credential storage](https://learn.chatgpt.com/docs/auth#credential-storage). CODEX_HOME also contains configuration, history and other state; pointing isolated work at an ordinary shared home is not a safe inference. [Configuration/state locations](https://learn.chatgpt.com/docs/config-file/config-advanced#config-and-state-locations).

For future native allocation, prefer a supported operator-owned authentication lifecycle outside measured worker access, with fresh evidence contexts/workspaces and verified state separation. Reuse a valid session or its supported refresh without copying credential bytes. Possible native arrangements are a dedicated authenticated host with fresh separated threads, or an OS credential store with independently mapped state roots. **The isolation of these combinations and cross-CODEX_HOME credential-store behavior remain unresolved here.** An ephemeral thread or disabled history setting alone does not prove absence of shared memory, configuration or tool access to prior state.

The retained local 0.153.4 protocol describes an external ChatGPT token input as unstable/internal-only; it is not an approved reuse mechanism. Do not implement a token bridge, symlink/copy authentication files, expose the ordinary global home, or infer an available enterprise entitlement. If no supported combination meets the selected native evidence boundary, distinct authorized sign-ins may be necessary per independent authentication realm, with continuations reusing their parent lifecycle. Record why and assess practicality before allocating; do not assume 907 profiles imply 907 browser authorizations.

The [staged pilot](pilot-allocation.md) distinguishes its already authenticated host-context Stage A from later native isolation questions and quantifies the unresolved authentication burden. No authentication, credential inspection or state modification occurred in this specification task.

## 10. Decision examples

All examples assume the proposed policy is accepted/available, the named observations actually pass, and ordinary owner authority exists. They are expected decisions, not executed results.

| Change | Policy / required evidence | Adoption eligibility | Permitted claim |
| --- | --- | --- | --- |
| Spelling-only correction | Routine CI-01: deterministic suite, focused independent invariants/meaning check; no native test if meaning/path unchanged. | Eligible after Routine PASS and exact installed-byte checks. | Scoped correction accepted; new bytes not fully qualified. |
| Bounded prompt-behavior fix | Routine CI-04: C, affected normal/edge/negative cases, earlier failures, candidate/baseline pair and independent grades. | Eligible if accepted scope/controls and cumulative meaning remain bounded. | Named behavior fix passed observed cases; improvement only if predeclared comparison supports it. |
| Trigger-description change | Routine CI-02: C, affected explicit/direct/indirect/near-miss A; B for changed promises. | Eligible within the existing capability boundary. | Activation verified for the named queries; no universal selection claim. |
| Resource-path correction | Routine CI-03: mechanical resolution, exact installed C resolution and affected output/task path. | Eligible when the installed mapping and affected behavior pass. | Corrected resource path verified in the selected installation. |
| Compatible client patch | Routine CI-07/CP: documented/interface impact, relevant mechanical checks, exact installed load/completed-task smoke and affected control/negative probes. | Eligible only with observed bounded compatibility; version alone is insufficient. | Compatibility verified for used capabilities on the new client; old qualified identity remains historical. |
| Consequential hook/authority change | Full CI-05: deterministic control/denial tests, independent semantic review and actual native enforcement integration. | Routine diagnostics do not authorize adoption of the changed contract. | Full qualification only after complete required evidence; no enforcement claim from prose. |
| Receiving-transfer contract change | Full CI-06: producing behavior, consumer requirements, actual eligible-output transfer and failure cases. | Requires matching Full evidence for the new transfer semantics. | The exact transfer contract was exercised; a prepared handoff alone is insufficient. |
| Several accumulated Routine edits | Routine if the anchor-to-current dependency/interaction review and union of affected regressions remain bounded; Full if authority, supported scope or transfer meaning changes or impact stays unknown. | Eligible only after cumulative checks, not solely because each individual edit once passed. | Current update chain accepted for its scope; the last fully qualified anchor is unchanged. |

## 11. Funding and stages

The original ledger is closed at **24 charged / 24 approved / zero remaining**. No pilot can be funded from that exhausted allowance. This authoring request authorizes the present root specification work, not additional delegated model/reviewer calls. None was dispatched. Provider usage for this root authoring work was not measured and is not claimed to be zero. The preserved attempt ledger is not a subscription-usage meter.

Separately proposed, unapproved allocations: **R2-REVIEW: one independent review generation, 20 minutes including preparation/closeout; CMP-2 Stage A: two generations, 30 minutes including operator work/closeout.** Each generation is bounded at 600 seconds; zero retries. If both are expressly approved and fully used, they add three charges, making the historical-plus-new total 27; the original 24-entry ledger remains intact. Approval of one does not approve the other or a later stage. These are scheduling bounds, not estimates of subscription consumption. No implementation allowance or enlarged Full campaign is requested here.

Later paired authoring, interactive and nested stages are contingent proposals for specific measured gaps, with their own allocation decisions. Stage A requires neither policy implementation nor new authentication/unsupported transport. A cost stage produces no Routine PASS or Full qualification result. Missing internal request/token usage remains NOT_OBSERVABLE; dispatch counts and time ceilings do not substitute for consumption measurements.

## 12. Enforcement, maintenance and review boundary

Use existing runtime ownership and H1–H5 responsibilities: bind versioned selection and authority; check deterministic/independent-review prerequisites; enforce required native dependencies; derive honest disposition; retain deliverables and creation-time handoff facts. The model supplies substantive impact and semantic reasoning; the protected runtime owns mechanical checks, counters, transitions and receipts. The owner controls acceptance. No worker may self-issue authority or change its criteria to pass.

Extend the existing plan/results records rather than inventing a new approval chain. Generate manifests, diffs, case mappings, identity/freshness checks, usage fields and status summaries mechanically; obtain independent semantic judgment once at the relevant boundary. Reuse valid raw observations with exact scope instead of repeated setup or repeated reviewer ceremonies. Errors block only the dependent action/claim while independent reporting continues. Unknown policy versions cannot authorize exclusions. These new semantics remain a design until their separately owned implementation and checks exist; the policy does not remove current gates by declaration.

A single explicit owner review decision may accept this coherent specification revision and its identified evidence-rule changes. Execution funding is separate and may be included only when explicitly selected. No per-row approval rounds or recursive reviews are required. All original cases, expectations, historical outcomes, timing deviations and earlier draft bytes remain available. The [requirement diff](requirement-diff.md) identifies preserved, changed and unresolved requirements. The [prepared handoff](prepared-handoff.md) records authoring completion only.
