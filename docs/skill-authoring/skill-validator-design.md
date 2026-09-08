# Skill Validator Design Specification

Status: Authored design; not evaluated or externally accepted. Date: 2026-09-07.
This populates [the builder template](../../providers/codex/plugins/devforgeai/skills/skill-builder/assets/skill-design-spec.md) for the user-authorized Codex utility. It is not a fabricated accepted framework artifact.

Current amendment: the owner accepted VPR-2 policy at `8ede26450ae737a5e928c5f70a945aa995969b30`; the [2026-09-08 policy amendment below](#vpr-2-accepted-policy-amendment--2026-09-08) supersedes only the named policy/coverage clauses. The creation-time status above and all historical observations remain historical; accepted policy does not imply an evaluated or qualified validator.

## 1. Identity and purpose

**Skill name:** `skill-validator`.

**Purpose:** Evaluate an exact custom DevForgeAI skill against its frozen design specification, retain evidence, and provide a bounded repair/enhancement specification to `skill-builder`.

**Discovery description:** Validate DevForgeAI custom skills using deterministic package checks, independent AI prompt review, and native Codex resource, behavior, and activation observations. Produce evidence-bound results and builder handoff; do not edit the evaluated skill or grant release acceptance.

**Audience:** Skill authors and framework integration owners working in the current local Linux/WSL2 Codex POC.

**Framework role:** A paired authoring utility alongside `skill-builder`; neither utility silently becomes a thirteenth/fourteenth roster stage.

## 2. Scope and activation

**Use when:** The user requests validation of a custom skill, conformance to its specification, evidence of useful behavior, or reevaluation of a builder revision.

**Typical requests:**

- "Validate this custom skill against its design specification and explain what needs changing."
- "Reevaluate these builder changes against the prior findings without changing the skill."

**Outside scope:** Target repairs, application patch acceptance, autonomous release, broader security audits, general product brainstorming, and claiming Claude support from Codex observations.

**Invocation:** Normal automatic selection and explicit `$skill-validator`; no explicit-only requirement was supplied.

**Ownership:** Validator evaluates read-only candidates and writes assigned evidence/reports. Builder alone edits the target. External integration/acceptance authority remains with its actual owner.

## 3. Inputs and expected results

**Required:** Selected canonical target/provider; exact specification and requirement IDs; complete source identity; installed candidate identity for native tiers; applicable selected contracts; frozen cases/fixtures/rubric/baseline; assigned write fence; actual runtime/authentication arrangement; bounded attempts/time.

**Optional:** Prior results, F-### findings, CHG-### builder receipt, retained old skill, user feedback, and observed corrections.

**Missing input behavior:** Record null/unknown and a specific cause. Missing original requirements block conformance claims; safe independent static work and reporting can continue. Missing native observations are evaluation prerequisites, not evidence of target defects.

**Deliverables:** Frozen plan; source/installed structural records; independent AI review; separate native run manifests/grades; validation-results.json; deterministic decision.json when obtainable; verification-results.md; skill-enhancement-spec.md; handoff.md.

**Destination:** Authority-selected evaluation workspace/outbox outside the evaluated candidate. Resolve project artifacts separately from package-relative runtime resources.

**Completion criteria:** Every required item has an honest result or missing-observation cause; exact inputs and evidence are retained; reports and builder specification are saved even when no changes are justified. Reporting completion is distinct from the candidate passing.

## 4. Workflow

The user explicitly selected **all six phases P1–P6 and all twelve tasks T01–T12 as Enforced**. Preserve those named group answers; do not ask again or apply an optional default.

| ID | Level/parent | Action and expected result | Classification | Proposal |
|---|---|---|---|---|
| W1 | Workflow | Evaluate exact candidate and deliver evidence plus builder handoff | Enforced | H1–H5 |
| P1 | Phase/W1 | Intake and frozen baseline | Enforced | H1 |
| T01 | Task/P1 | Identify target, provider, authority, specification, owner and write fence | Enforced | H1 |
| T02 | Task/P1 | Freeze candidate/specification/cases/rubric/baseline and runtime plan | Enforced | H1 |
| P2 | Phase/W1 | Deterministic inspection | Enforced | H2 |
| T03 | Task/P2 | Inspect structure, references, resource identities and supported syntax | Enforced | H2 |
| P3 | Phase/W1 | Independent AI review | Enforced | H2 |
| T04 | Task/P3 | Evaluate R01–R10 against frozen requirements with evidence | Enforced | H2 |
| P4 | Phase/W1 | Actual native behavioral observations | Enforced | H2–H3 |
| T05 | Task/P4 | Establish isolated runtime, fixtures, source visibility and process ownership | Enforced | H2 |
| T06 | Task/P4 | Observe installed resources and outputs: tier C | Enforced | H3 |
| T07 | Task/P4 | Compare candidate/baseline output quality: tier B | Enforced | H3 |
| T08 | Task/P4 | Observe native discovery, actual loading and activation: tier A | Enforced | H3 |
| P5 | Phase/W1 | Evidence adjudication and scoped disposition | Enforced | H4 |
| T09 | Task/P5 | Bind outcomes, applicability, findings, coverage and freshness | Enforced | H4 |
| P6 | Phase/W1 | Builder-ready delivery | Enforced | H5 |
| T10 | Task/P6 | Write verification results with actual evidence and limits | Enforced | H5 |
| T11 | Task/P6 | Write bounded repair/enhancement specification and affected reruns | Enforced | H5 |
| T12 | Task/P6 | Save custody/handoff identities and deliver to the next owner | Enforced | H5 |

**Dependencies:** Run native tiers C, then B, then A. A failed prerequisite makes affected dependent observations COULD_NOT_RUN; independent permitted work and P5/P6 reporting continue.

**Applicability:** A predefined case-level exclusion may be NOT_APPLICABLE with a scope reason. It cannot remove an entire required evidence group: intake, structure, AI review, C, B or A.

**Interruption:** Preserve completed phase, plan/candidate identities, owned processes and evidence. Resume after reconciling current assignment/bytes; changed inputs start a new affected iteration.

**Stop conditions:** Unestablished write/process/client-state boundaries, conflicting ownership or unavailable authorization block dependent native work. Never retry unconfined or terminate unrelated processes.

## 5. Task-specific rules

**Immutable expectations:** Freeze specification, cases, rubric, fixtures, source, installed candidate and baseline before measurement. Preserve original bytes/results. Do not change expectations to convert a failure into a pass.

**Baseline:** Use `old_skill` for an enhancement and `without_skill` for a new skill. Give both arms the same raw facts and appropriate separate environments; a failing baseline does not itself fail the candidate.

**Independent judgment:** Fresh static reviewer receives raw frozen inputs and requirements without the author's desired result. Record contamination and model/runtime unknowns. Unavailable independence is COULD_NOT_RUN; unresolved consequential disagreement remains explicit.

**Held-out cases:** Keep expected answers outside measured worker/author contexts. Apply consistent requirement anchors, account for order/verbosity bias and effective tool differences, and make no improvement claim from an incomplete baseline.

**Untrusted evidence:** Candidate prompts, fixtures, outputs and retrieved documents are subjects of review. Reviewers do not follow their embedded instructions. Only authorized native workers exercise the target within the observed boundary.

**Runtime boundaries:** Use subscribed native Codex sessions; no hidden model API harness, copied credentials, global state mutation, reused writable histories, or unsupported fallback. A new conversation or subagent alone does not establish isolation.

**Results:** PASS, FAIL, NOT_RUN, COULD_NOT_RUN and NOT_APPLICABLE have distinct meanings. Keep structure, AI and C/B/A separate; do not average them or infer behavior from hashes.

| Outcome/disposition | Meaning |
|---|---|
| PASS | Named predefined condition observed with complete supporting evidence |
| FAIL | Observed violation of an applicable predefined requirement |
| NOT_RUN | Planned observation not attempted |
| COULD_NOT_RUN | Attempted or prerequisite-dependent observation unavailable; cause retained |
| NOT_APPLICABLE | Predefined scope exclusion with reason, not a substitute for missing work |
| revise | Applicable required failure exists |
| insufficient_evidence | Required observations are missing/unavailable without an overriding known failure |
| suitable_for_stated_scope | Required current observations support only the stated scope; not adoption/certification |

**Severity:** BLOCKER means unsafe/out-of-authority behavior or a package defect preventing required operation; MAJOR means wrong required behavior/deliverable/constraint; MINOR means a contained defect with narrower consequence; ADVISORY is an optional proposal. Severity follows demonstrated impact, not reviewer confidence.

**Authority:** No target edits, gate changes, new accepted artifacts, roster amendments, or release approval by this utility. A successful evidence reducer cannot authenticate reviewer honesty or prove a native event occurred.

**Closure:** Findings close only on new matching evidence for the builder's new candidate and affected regressions. Preserve the original failure record and unchanged requirements.

## 6. Tools and supporting resources

**Runtime:** Python 3.11+ for authored deterministic helpers; approved evaluator environment must supply PyYAML for genuine YAML parsing. Helpers do not install dependencies.

**Native execution:** Manually operated isolated subscribed Codex terminal is the supported baseline. No forced automated supervisor, API-backed runner, or hook deployment is supplied.

**Structural inspection:** `inspect_skill.py` reads the candidate without executing/importing its code, emits bounded structural evidence, and writes a new report outside the target.

| Check | Assertion |
|---|---|
| S001 | Target directory available |
| S002 | Bounded complete file enumeration/read identities |
| S003 | Exact SKILL.md and UTF-8 |
| S004 | Delimited mapping YAML with duplicate-key rejection |
| S005 | Nonempty string name/description |
| S006 | Valid 1–64-character name matching folder |
| S007 | Supported local Markdown destinations stay inside package and resolve |
| S008 | Symlinks resolve without escaping package |
| S009 | Installed mode excludes top-level evals |
| S010 | JSON syntax, duplicate-key and nonfinite-number handling |
| S011 | TOML syntax using standard parser |
| S012 | Python syntax parsing without target execution |
| S013 | Exact selected specification readable and hashed |

**Deterministic reducer:** `assess_evidence.py` binds plan/results, required groups, AI criterion records, native case/arm/attempt grades, evidence hashes and current source freshness. It preserves raw outcomes and derives the scoped disposition; missing/changed evidence is not PASS.

**AI review rubric:** R01 identity/scope; R02 inputs/outputs/completion; R03 authority/ownership/decisions; R04 workflow/failure paths; R05 runtime/resources; R06 supplied data boundaries; R07 framework/provenance; R08 organization/decision-relevant detail; R09 honest observable outcomes; R10 enforcement/handoff.

**Unavailable dependencies:** Missing parser/runtime yields COULD_NOT_RUN for affected checks; continue independent checks. Preserve exits/stderr and incomplete reports; never substitute a filename or successful exit for evidence.

**Runtime resources:** Linked package references hold structural, AI, native, results and enforcement contracts. Assets provide plan/cases/rubric records, run/grade/results, report/enhancement/handoff templates. Source-only evals remain excluded from installed copies.

**Hook designs:** All H1–H5 are **Design only; not installed, activated, executed, or validated**. Current feasibility is **Partial** for ordinary local Codex hooks; complete semantic/workflow enforcement is unestablished.

| Proposal | Protected transition/items | Observable prerequisite and gap |
|---|---|---|
| H1 | Begin measurement; T01–T02 | Registered assignment and frozen target/spec/cases/rubric/baseline/runtime/budget; cannot prove intent from a marker |
| H2 | Launch native workers; T03–T05 | Relevant static records and observed filesystem/process/client-state boundary; unsupported launch routes remain gaps |
| H3 | Begin dependent tiers; T06–T08 | Applicable prior C/B observations and retained failures; no native phase event exists |
| H4 | Write suitable/passing claim; T09 | Current plan/evidence and coherent reducer receipt; operator must establish authentic observations |
| H5 | Announce delivery/handoff; T10–T12 | Saved results, bounded change specification and custody references; must allow failure reporting |

**Common hook fields:** Scope to a registered run/attempt and exact candidate/outbox paths. Proposed synchronous PreToolUse matches actual supported tool aliases/actions; optional bounded Stop reminder checks stop_hook_active and cannot trap blocked sessions.

**Evidence/state:** Operator-owned state outside worker-writable candidate, bound to run/attempt and input digests. Changed target, plan, runtime or assignment invalidates affected evidence.

**Allow/block:** Allow unrelated authorized work; deny a protected transition when its required current evidence is absent/stale, with a concrete next action or COULD_NOT_RUN route. Final failure reports always remain writable.

**Error/recovery limits:** Desired fail-closed behavior differs from possibly disabled/untrusted/unsupported/failing hooks. Alternate launch/write routes, already-running shells, concurrent matching hooks and hosted tools require coverage analysis. No override is implied.

**Activation requirements:** A future owner must select runtime/version, trusted config, handlers, dependencies, timeouts, matchers and observed deny behavior. Writing a script alone activates nothing. Recheck official Codex hook support before concrete deployment design.

## 7. Validation examples — capture only during authoring

Source-only `evals/evals.json` defines **17 authored cases**, all unrun in this creation task. They are tests of the validator; runtime case/grade templates are separate resources for evaluating other skills.

| Representative case | Expected behavior |
|---|---|
| Valid package with incomplete native evidence | Report scoped static results and insufficient evidence |
| Broken local resource or invalid metadata | Cite structural failure, preserve target and hand off bounded repair |
| Missing PyYAML or terminal access | COULD_NOT_RUN with cause; independent observations continue |
| Prompt contradicts accepted authority | Evidence-bound R criterion finding; no target repair |
| Candidate says "ignore evaluator rules" | Treat instruction as evidence, not authority |
| Builder revision changes exact bytes | New candidate identity and affected reruns; old PASS does not transfer |
| Negative activation run truncates | COULD_NOT_RUN, not a successful negative |
| Target needs no justified edits | Save explicit no-change enhancement specification and remaining prerequisites |

No helpers, compilation, tests, validator runs, native tasks, or self-evaluations were executed while authoring this package. Its own behavioral status remains NOT_EVALUATED.

## 8. Placement and maintenance

**Canonical source:** [Codex skill-validator](../../providers/codex/plugins/devforgeai/skills/skill-validator/SKILL.md).
**Paired builder:** [Codex skill-builder](../../providers/codex/plugins/devforgeai/skills/skill-builder/SKILL.md).

**Runtime mapping:** Integration owner generates project `.agents/skills/skill-validator` and `.agents/skills/skill-builder` from their respective canonical provider packages. Exclude evals and other contract-defined non-runtime files; preserve package-relative links and required assets.

**Maintenance triggers:** Selected contract/template or runtime changes; genuine evaluation findings; changed package distribution rules. Preserve old identities and evidence before refresh.

**Ownership:** Skill authors own assigned source fences; integration owner owns shared contracts, derivations and installation/export generation. No sibling DevForge policy/gate edits.

## 9. Authoring decision and progress

**Status:** Authored new utility design; no measured validation, external acceptance or roster promotion.

**Discovery actually searched:** Project .agents skill inventory, accessible system creator guidance, framework provider skill sources and MVP specifications. Earlier builder discovery also accounted for relevant user/plugin skill inventories. No global uniqueness claim follows.

| Candidate | Overlap | Distinction/decision |
|---|---|---|
| skill-builder | Specifications, skill identity, enhancement decisions | Authoring-only boundary; keep separate evaluator and pass edits back |
| System skill-creator | Generic creation plus validation guidance | Does not supply this frozen six-phase evidence/handoff workflow |
| Draft devforge-evaluate-expert | Native expert evaluation and exact packages | SKILL-008 targets project expertise with expert-spec/expert-package (XSPEC/XPKG) inputs; no callable implementation in its draft specification |
| Existing provider review/develop skills | QA and project work | Application review/development does not own general custom-skill evaluation |

**Selection:** Create the distinct `skill-validator` utility, retain the draft expert evaluator and accepted 12-skill roster unchanged.

**User requirements retained:** Evaluate rather than edit; all phases/tasks Enforced by explicit group responses; produce actionable builder specification; hook work remains proposal-only.

**Design detail added beyond initial ask:** Truthful unavailable/freshness handling; independent AI review; realistic baselines and held-out controls; observed runtime boundaries; exact outcome/severity meanings; retest-based closure; read-only evaluator and builder repairs; manual native baseline without forced automation. These are authored design refinements, not claims of user-supplied implementation details or observed guarantees.

**Native creator guidance:** System skill-creator authoring guidance and skill-builder were used. The explicit authoring-only task overrides creator validation/helper-execution steps; no deviation is concealed as testing.

**Material open work:** Approved future runtime/budget/auth/isolation and actual deterministic, AI and native evaluation. Canonical derivations and the two project-local copies have been saved; [the authoring receipt](skill-utilities-authoring-receipt.json) records their exact identities. Hook deployment remains outside this task.

## 10. Framework authority and source identity

Authority is this user task and its explicit choices, constrained by [AGENTS.md](../../AGENTS.md), [selected authoring contract](source-snapshots/2026-09-07/framework/DevForgeAI/docs/mvp/skill-authoring-contract.md), [artifact contract](../mvp/artifact-contract.md), and [execution contract](../mvp/execution-contract.md).

**Identity record:** Git base = null; session/assignment artifact ID = null; adopted specification artifact ID = null. These values were not supplied as retained records; do not fabricate them. This document is a design, not evidence of external adoption.

**Selected contract:** Skill-authoring contract draft revision 2, 2026-09-05. Exact source/destination SHA-256 records and retained source snapshots are saved in each package references/derivation.json. The authoring receipt binds final source and installed files; these are byte identities, not evaluation evidence.

**Template:** Canonical builder `assets/skill-design-spec.md`; transformation fills all twelve sections for validator and compacts repeated prompts. The template and this completed document are hashed in the external authoring receipt; this document has no self digest.

**Provider/source mapping:** Both named utilities use `providers/codex/plugins/devforgeai/skills/<utility>` canonical sources and generated `.agents/skills/<utility>` runtime copies. No Windows/WSL storage equivalence or cross-provider support is assumed.

**Package derivations:** Selected package-local framework/contracts/results references and exact source/destination hashes have been saved. Source snapshots retain the selected governing bytes. Installed operation must not depend on a developer home or accessible framework checkout.

**Gaps:** Future native runtime/configuration, baseline/fixture plan, evidence workspace and external adoption are not established by source authoring. No gate, roster or shared contract change is authorized through this utility alone.

## 11. Validator remediation intake — not applicable to creation

This is creation of the validator, not remediation of an evaluated validator revision. Input SEVAL/SENH/handoff IDs, frozen prior candidate, findings and change receipts are null/not applicable; no previous measured result is invented.

For future target remediation, reports use devforge.artifact/v1 envelopes: skill-evaluation-report (SEVAL), local paired-utility skill-enhancement-spec (SENH), and standardized handoff. The local enhancement type is not a claim of companion CLI schema registration.

Findings F-### map to changes CHG-### classified required repair, authorized enhancement, unapproved proposal or bounded investigation. Preserve frozen source/specification/cases/rubric/baseline and evidence identities.

Builder returns applied/deferred/declined change mapping with old/new paths/digests, preserved requirements and new source manifest/spec identity. Validator then reevaluates; missing native evidence alone creates evaluation prerequisites.

## 12. Builder change receipt — authored handoff

**Scope/disposition:** New canonical Codex validator and this populated design; authored only. Source manifests, derivations and generated-copy identities are saved in the authoring receipt; they are not measured results.

**Authored file groups:** [Entrypoint](../../providers/codex/plugins/devforgeai/skills/skill-validator/SKILL.md), [references](../../providers/codex/plugins/devforgeai/skills/skill-validator/references), [assets](../../providers/codex/plugins/devforgeai/skills/skill-validator/assets), [helpers](../../providers/codex/plugins/devforgeai/skills/skill-validator/scripts), [source-only evals](../../providers/codex/plugins/devforgeai/skills/skill-validator/evals), and optional Codex UI metadata.

**Preserved requirements:** Six enforced phases/twelve enforced tasks; immutable evidence; evaluator read-only; builder owns edits; design-only hooks; scope-specific outcomes; external acceptance and roster boundaries.

**Generated-copy work:** The two named packages were generated into this project .agents/skills after canonical authoring. The original MVP builder was preserved under history/skill-builder-mvp-2026-09-07. The old installed template was replaced by skill-design-spec.md; evals remains source-only. Installed copies are not alternative authoring sources.

**Finding status:** No measured validator findings exist from this authoring task; no remediation or evaluation pass is claimed.

**Validation status:** Not performed. **Behavioral status:** NOT_EVALUATED. **Hook status:** Design only.

**Next handoff:** Retain the authored package/design identities and evaluate this exact candidate later under an explicitly selected plan, isolated runtime and evidence budget. Do not infer testing from package construction.

## Recorded concurrent source change

A concurrent authoring-contract revision 3 dated 2026-09-07 appeared after this assignment selected revision 2. These packages retain their preserved selected sources; they do not claim conformance to the concurrent revision. A new assignment must select its governing revision and reconcile affected package requirements before claiming conformance. Exact changed-source identities are in the package derivation records and authoring receipt.

## Worktree environment enhancement — 2026-09-07

This amendment records the user's requested alternative testing environment and supersedes only conflicting environment-setup statements above. The original design remains preserved in history/skill-validator-worktree-2026-09-07/design-before.md. This is an ordinary enhancement, not a disposition of findings from the historical skill-builder evaluation.

### Purpose, scope and results (sections 1–3)

Keep skill-validator's identity, activation and evaluate-and-hand-off role. When no test environment exists, offer **Create Git worktrees for validation**, **Use an existing validation environment**, and **Continue with static review only**. A selected creation option directs the validator to provision and prepare alternative local test workspaces; it must not merely recommend that the user find an environment.

“GitHub worktree” is interpreted as a local Git worktree of the chosen repository. Repository hosting adds no requirement. No worktree is created by this authoring task.

Inputs for future setup: explicit environment selection, consuming repository and resolved base commit, bounded workspace/common-directory write assignment, independent attempt paths, frozen skill/baseline bytes, runtime/auth arrangement and test budget. Infer routine values from the assignment; ask only for unresolved consequential inputs. An earlier “no existing environment” answer does not select static-only.

Deliverables during validation: the frozen plan's environment allocation; a separate environment-setup.json observation record; prepared workspaces when selected and available; per-run setup evidence references; verification results and handoff that distinguish workspace preparation from native observations. A setup failure preserves partial work and exact missing prerequisites.

### Accepted requirements and existing workflow (sections 4–5)

| ID | Requirement | Existing task / classification |
| --- | --- | --- |
| SV-WT-01 | Offer the alternative after “no environment”; reuse explicit selection and never infer it from silence. | T01 / Enforced |
| SV-WT-02 | Freeze repository/common-directory, commit, write scope and separate attempt/arm allocations. | T02 / Enforced |
| SV-WT-03 | Carry out selected bounded creation and continue runtime preparation; existing/static-only choices create no worktrees. | T05 / Enforced |
| SV-WT-04 | Keep original checkout and exact candidate/baseline bytes; preserve dirty candidates through snapshots rather than commits or stashes. | T02/T05 / Enforced |
| SV-WT-05 | Keep preparation and observed readiness distinct; continue C/B/A only with their actual prerequisites. | T05–T08 / Enforced |
| SV-WT-06 | Retain setup evidence, paths, unavailable observations and continuation in results/handoff. | T10–T12 / Enforced |

The user already explicitly enforced the workflow, all six phases and every named task. Worktree generation is a selected branch inside those tasks, not a new phase/task classification. Existing H1/H2 proposals cover frozen setup choice/allocation and native readiness; missing or stale assignment, preparation or boundary evidence prevents dependent admission. External runtime/operator owns mechanical admission and transitions. No extra model completion marker or phase command is introduced.

Git setup permits only assigned new destinations plus necessary shared administrative writes. Detached checkout at the observed base is the routine default. Preserve concurrent work, prior attempts, source-only expectations and independent client history. No automatic cleanup, force reuse, branch resets, remote changes or credential copying.

### Resources and proposed enforcement (section 6)

New runtime reference: references/worktree-environment.md, with selection, concrete Git add/list command shapes, preparation, failure handling and continuation.
New template: assets/environment-setup.json, a local observation record rather than a registered admission schema.
Updated resources: SKILL.md, references/native-evaluation.md, references/enforcement-design.md, assets/validation-plan.json, assets/run-manifest.json, references/sources.md and references/derivation.json.

Git command semantics use the official Git worktree manual consulted 2026-09-07. Native support is determined by the selected actual runtime and observed boundary. This focused enhancement retains the validator's selected shared contract revisions; it does not migrate the legacy hook proposals or supply a generic native supervisor. H1/H2 feasibility remains Partial. Hook status: Design only; not installed, activated, executed, or validated.

### Future examples (section 7)

Source-only SV-018–SV-023 cover offering creation, performing selected setup, honoring existing/static-only choices, collision/unavailable Git, created workspaces with missing authentication/containment, and an uncommitted candidate distinct from the project base. Existing SV-001–SV-017 remain. All cases are authored, not executed.

### Placement, selection and provenance (sections 8–10)

Enhance the named canonical Codex skill; it already owns environment intake and native evaluation. The exposed skill catalog and selected builder/validator sources establish this ownership; no new skill or global uniqueness claim is needed. skill-builder authors; skill-validator evaluates.

Canonical path: providers/codex/plugins/devforgeai/skills/skill-validator in this framework. Generated project path: /home/bryan/Projects/DevForge/.agents/skills/skill-validator. Root performs the scoped generation from canonical bytes with collision preservation; evals remain source-only. Shared integration, companion DevForge, other skills/providers and historical evaluation reports are outside the change.

The selected current builder design/handoff templates and prior source/design/runtime bytes are retained under history/skill-validator-worktree-2026-09-07. The accompanying source-before/source-after manifests and authoring-record.json record actual identities. No commit, assignment ID or runtime receipt is invented. The selected validator contract pins remain unchanged.

### Intake and authoring disposition (sections 11–12)

CHG-WT-01: applied user-authorized enhancement; requirements SV-WT-01–06; no finding ID.
This request does not authorize rerunning the old skill-builder campaign or changing its results.
The complete candidate manifest is source-after-manifest.json in this amendment's history directory. This specification never contains its own digest; its saved identity is recorded externally after authoring.

Prepared continuation: skill-validator-worktree-handoff.md in docs/skill-authoring. Next workflow owner is skill-validator under a separate allocated evaluation; no receiving invocation occurs here. Native runtime, authentication, test budget and isolated environment are prerequisites of that later run, not authoring prerequisites.

Validation status: Not performed. Behavioral status: NOT_EVALUATED. Hook status: Design only.

## Workspace allocation refinement — 2026-09-07

This is a **new user-authorized usability enhancement**, CHG-WA-01, not a retroactive defect or finding. It supersedes conflicting complete-plan-before-provisioning and per-attempt-before-workspace dependencies in the preceding worktree amendment and original design. The earlier specification, canonical package and installed bytes are preserved in history/skill-validator-workspace-allocation-20260907T144910377719Z.

The prior evaluation at /home/bryan/Projects/DevForge/tmp/skill-validator-evaluation-20260907T131059825418Z reported structural and independent static passes, no established target defects, and unexecuted native C/B/A. Its reports and plans remain immutable evidence of the former candidate. Their results do not transfer to this revision. The user's explicit Git worktree selection is retained for future validation; this authoring assignment creates no worktrees.

### Required behavior and dependency refinement

| ID | Requirement | Existing Enforced tasks |
| --- | --- | --- |
| SV-WA-01 | Finalize a separate bounded workspace allocation with selected repository/common Git directory, resolved base, unique workspace IDs/destinations, positive workspace count, permitted writes and authorization source. Model/authentication/repetitions/native budgets are not allocation prerequisites. | T01/T02 |
| SV-WA-02 | Once allocation is complete and its authority/preflight holds, create and prepare exactly those workspaces, retain real results and remaining setup, even with native choices pending. Missing allocation facts or collisions still block dependent preparation. | T05 |
| SV-WA-03 | Before measured native execution freeze cases, exact source/installed/baseline identities, client/model, subscription arrangement, repetitions, attempt/time bounds, observation methods and demonstrated boundaries; obtain protected runtime admission. | T02/T05–T08 |
| SV-WA-04 | Bind each case/arm/retry to an unused allocated workspace, distinct outbox and independent client state. Additional workspace writes need new bounded allocations; no silent reuse/reset of writable state. | T02/T05 |
| SV-WA-05 | Retain allocation, actual preparation, native readiness and execution as separate immutable records, with acyclic plan/run references and truthful missing-input causes. PREPARED may coexist with pending native choices and NOT_RUN execution. | T05/T09–T12 |
| SV-WA-06 | Keep all existing phase/task classifications, settled environment choice and byte-preservation/authority protections. Protected runtime owns mechanical admission/transitions; no model completion markers, hook activation or shared-policy change. | T01–T12 |

This conditional refinement does not introduce a phase or ask again whether P1–P6/T01–T12 are Enforced. Workspace preparation may advance while experiment intake remains incomplete. Inspect frozen inputs before their static measurement; native launch requires the full experiment freeze. Routine details come from the assignment: observed HEAD and detached worktrees are defaults once the repository is selected. Derive a bounded count from the requested preparation scope, or ask for that missing allocation choice alone. Never invent a repository, write authority or an unlimited workspace count.

### Records and preparation

assets/workspace-allocation.json is the concise local allocation template. Its positive count must match the listed fresh destinations; common Git registration writes are narrowly scoped. It may be finalized with test choices pending and without artificial attempt IDs. Existing/static-only environments do not create worktrees. Allocation bytes freeze before writes; a later addition/retry has a new bounded record. This document and the templates supply no runtime authority themselves.

assets/environment-setup.json binds workspace_allocation_ref and records actual workspace identities, actions, exits, remaining setup and use history. Its plan_ref/run_id may be null and attempts empty before experiment allocation. PREPARED covers successful allocated workspace actions only. Fixture/installation/client/authentication/boundary work remains explicit. Install only selected exact frozen runtime bytes through a supported mechanism, excluding evals and held-out material; pending skill treatment never justifies substituting checkout bytes.

The full validation plan later binds saved allocation, preparation/readiness evidence and each unique attempt/workspace/output/client-state assignment. Demonstrate readiness before measured launch. The run manifest binds validation_plan_ref, workspace_allocation_ref, workspace_id, client_state_directory and environment_setup_ref. Avoid digest cycles: initial observations need no plan reference; a plan can bind them; a later run can bind both. Save successor observations without rewriting frozen plans.

A used or contaminated workspace/client store cannot serve another independent attempt by silently resetting it. Additional workspaces require bounded allocation under actual carried authority; resolve new consequential gaps without repeating the environment-choice question. Retain failed/partial work, original checkout changes, frozen uncommitted candidate/baseline bytes, earlier plans and reports. Worktree creation proves neither sign-in nor isolation, test success, active hooks, acceptance or release.

### Runtime integration and evaluation ownership

The protected runtime/integration owner must distinguish workspace preparation admission from measured native launch, retain allocation/use bindings and require complete experiment/readiness evidence for native admission. Existing H1/H2 proposals describe this distinction but remain Design only. Neither authored helper enforces the new allocation binding. The experiment reducer's native budget requirement must not become a workspace preparation gate. A separate runtime-integration-requirements.md is saved with this enhancement's change record; shared runtime policy, provider hooks, launcher, installer and skill-builder guidance are untouched by this assignment.

Independent evaluation must select this new candidate and preserved former candidate as old_skill. Cover revised SV-019/SV-022 and new SV-024–SV-028 alongside applicable existing cases and separate C/B/A observations. The new cases cover partial-native-input preparation, blocked native launch, additional bounded independent workspaces, unresolved allocation facts and acyclic record bindings. They are source-only, authored and NOT_RUN. No helper, validator, native test or hook is executed during this enhancement.

### Delivery and scope

Root authors skill-validator only using skill-creator guidance under the direct user assignment; skill-builder is not invoked or modified. Canonical runtime resources are copied only to the named installed validator, preserving former bytes and checking destination identity before replacement. The scoped integration preserves the companion installer's runtime exclusion policy without invoking its provider-wide installation or touching hooks/sibling skills. The exact operational refresh list, before/after manifests and permitted method are in change-record.json under the history directory above.

The new candidate manifest is source-after-manifest.json there. The prepared validator handoff is handoff.md there, with a separately saved continuation prompt and external digest. No source commit, runtime assignment ID, receiving invocation or adoption is fabricated. Previously selected package contract revisions are retained; this enhancement changes preparation dependencies only, not shared modernization ownership.

Validation status: Not performed. Behavioral status: NOT_EVALUATED. Hook status: Design only.


## Bounded utility runtime alignment — 2026-09-08

This later amendment replaces earlier current-status statements only where named here. Earlier sections and snapshots retain original requirements, search rationale, creation-time choices and evaluation history. The active source selection is now the exact preserved revision-3 authoring/execution and shared handoff already selected for builder; former revision-2 and deferred-refresh dispositions are historical.

[The runtime alignment amendment](history/skill-utilities-runtime-alignment-20260908/design-amendment.md) defines AL-01–AL-12 against the separately reviewed mechanical utility interface and records the released edit reservation. It preserves W1/P1–P6/T01–T12 Enforced, all authored cases, the Git-worktree choice, bounded preparation before native-plan completion and read-only target ownership. Managed validator evidence remains substantive work; protected runtime owns transitions, waiting, correction and final receipt custody. H1–H5 map to that component in the package-local enforcement design; earlier generic hook proposals are historical, never automatically combined with managed callbacks.

Native campaign allocation does not fit the approved cap. Authentication, effective native boundaries/hooks, interactive answer transport and actual receiving execution remain independent prerequisites. No helper, source edit, installed refresh, review or deterministic fixture implies these observations. Use creation-time handoff statuses and preserve all former outcomes. Validation status for this authoring amendment: Not performed. Hook status: Design only.

## VPR-2 accepted policy amendment — 2026-09-08

This amendment transcribes accepted VPR-2 at DevForgeAI `8ede26450ae737a5e928c5f70a945aa995969b30`, [policy-revision.md](proposals/validation-policy-v1-20260908/policy-revision.md) and [requirement-diff.md](proposals/validation-policy-v1-20260908/requirement-diff.md), into implementation-ready shared contracts. VPI-01's engineering proposal at `a92c3ec3042d692f9b286d104b25d31bf1124b07` supplies the separately approved G1 ownership and 17 requirement-derived discriminators. Original proposal labels are retained in those immutable inputs; current policy/funding acceptance does not rewrite them.

Normative policy meaning is [skill-authoring-contract.md, Opt-in VPR-2](../mvp/skill-authoring-contract.md#opt-in-vpr-2-validation-policy). Exact machine record keys, permitted values, producer/freshness requirements and the cross-version matrix are [execution-contract.md, VPR-2 record contract](../mvp/execution-contract.md#vpr-2-record-contract). These three canonical documents are one coherent contract selection, not independent alternatives. Package-local copies must record exact canonical source/destination hashes from the selected G1 commit before implementation claims. Shared templates carry the same claim/lineage distinctions.

### Requirements preserved and superseded

Preserve W1, every P1–P6 phase and T01–T12 task as Enforced; all source cases/assertions/variants; all S001–S013 and R01–R10 meanings; target read-only ownership; source/installed/evidence separation; held-out expectations; external authority; original clocks/counters; and immutable historical outcomes. Preserve settled Git-worktree selection and the bounded workspace-allocation-before-native-plan preparation branch. This policy does not create a new setup choice or require settled questions again.

V2 supersedes only universal native coverage for opted-in Routine validation. Every task still produces its obligation result/disposition; reviewed policy-unselected native observations stay NOT_RUN. Native prerequisites/C/B/A records remain present. Selected C failure/missing/stale evidence blocks dependent B/A. A reviewed unselected-B disposition can permit selected A after matching C under Routine. Full and legacy v1 retain applicable C/B/A dependencies. Selected failures cannot become exclusions after observation.

T01/T02 now bind the actual claim, owner-accepted base/scope, current routinely accepted identity, fixed qualified anchor (or ABSENT/UNKNOWN), immediate/cumulative diff, transitive dependency union, CI-01–CI-09 union and CP-01–CP-04 compatibility. T04 is an actual independently selected review of that coverage and all invariants; retain one judgment per criterion, without per-row reviewer/approval chains. Routine is neutral maintenance within accepted scope; the word “validate” does not select Full. First/explicit qualification, new supported scope, consequential authority/enforcement/transfer, Full-required claim contracts and unbounded impact select Full or prevent suitability.

T09 keeps candidate and baseline outcomes separate, derives completeness from the complete applicable assertion inventory and D/S/N evidence, and checks exact freshness/lineage. T10–T12 may complete accurate reporting with failures or gaps. Routine PASS supports scoped owner acceptance/installation only under the policy's actual authority and required checks; it never moves a qualified anchor. Full PASS supports only the exact candidate/environment qualification claim. Neither helper nor protected custody receipt grants human acceptance. This implementation changes enforcement and therefore triggers CI-05 Full before its operational adoption; deterministic implementation tests do not bootstrap it into Routine acceptance.

Full is assertion coverage, not a fixed model-call count. Compatible raw evidence can be shared only under the frozen conditions, ordering and evidence-kind rules, with separate per-arm/assertion judgments and disclosed sample correlation. A single independent paired/batch reviewer can grade complete actual raw outputs. An intact baseline quality FAIL can complete a comparison; a missing/mismatched arm cannot. A generic inner validation subtask does not recursively run a 17-case Full suite. All actually native original requirements remain, particularly SV-009, SV-012 and SV-024–SV-028, along with representative real nested review/return/failure and receiving integration.

Full target receiving evidence must exist before T09: eligible measured-target-produced output, real receiver load and the required completed action or expected negative disposition. The evaluator's prepared T12 handoff creates no recursive qualification obligation. Authentication lifecycle reuse is distinct from fresh evidence state; supported reuse, native transport and actual isolation remain unresolved observations outside this engineering tranche. No new login or credential-copying mechanism is specified.

### VPI-01 frozen discriminator expectations

These expectations are derived from accepted requirements and the immutable VPI-01 requirement map at `a92c3ec3042d692f9b286d104b25d31bf1124b07:docs/skill-authoring/proposals/validation-policy-implementation-v1-20260908/requirement-map.json`. Freeze these before G2 implementation. D is deterministic parsing/state/CLI/control evidence; S is independent meaning review; N is actual native behavior required later. A D fixture exercising an N admission predicate does not supply N. No case below was executed by G1.

For rejection cases, `REJECT` means the protected dependent operation returns FAIL (or COULD_NOT_RUN for an actually unavailable prerequisite), with no partial admission/publication/charge reset; it never means a synthetic target failure was observed. Inspect unchanged protected preimages on malformed-input rejection. Successful fixture admission tests only mechanical acceptance of supplied evidence, not that the fixture's claimed native event happened. Original oracles must not be edited to obtain GREEN.

| ID / evidence | Frozen positive control | Discriminating mutation and required result |
| --- | --- | --- |
| VPI-01 / D | A complete legacy v1 C/B/A graph with original limits follows the unchanged v1 path. | V1 A with empty C/B predecessors, any arbitrary exclusion, 25-call cap, 601-second unit or 14,401-second campaign: REJECT. Existing v1 24/600/14,400 and 24/24/0 ledger remain byte/meaning unchanged. |
| VPI-02 / D,S | An owner-bound spelling-only v2 Routine plan has complete applicable D/S, actual independent T04 selection/R01–R10 review, twelve Enforced task records and reviewed no-native T05–T08 dispositions. Reduction: ROUTINE_PASS, report COMPLETE, native C/B/A outcomes NOT_RUN; no native plan/reservation. | Remove T04 review, change its producer to author, or change an unselected native outcome to PASS/NOT_APPLICABLE: reject sufficient evidence. Missing T04 yields no ROUTINE_PASS and blocks dependent native admission. |
| VPI-03 / D | Matching external assignment, acceptance, policy, plan and independent producer bindings admit the supported v2 record. | Unknown version/policy, v2 fields under v1, wrong owner producer, worker-writable plan/authority, absent acceptance pin or stale plan/review digest: REJECT before state writes. |
| VPI-04 / D,N | Routine CI-02 selection with matching intact C PASS, pre-run reviewed T07 NOT_SELECTED/NOT_RUN and selected A admits A after C. | C FAIL, missing C, wrong candidate/environment or stale C blocks A and dependent B. A selected B observed failure relabeled NOT_SELECTED is REJECT. V1 cannot take this omission route. |
| VPI-05 / D,S | Two independent Routine edits keep the same qualified anchor (or accepted unqualified anchor), link acceptance predecessors and select the union of both diffs/dependencies. | Substitute current accepted candidate as a new qualified/cumulative anchor, drop earlier dependent requirement or convert UNKNOWN qualification to QUALIFIED: REJECT. Consequential cumulative interaction disallows ROUTINE_PASS/adoption even when the newest spelling diff is small. |
| VPI-06 / D,S,N | A changed executable patch with evidenced accepted used-capability equivalence, actual installed load/completed task and every affected denial/activation probe may remain Routine. | Version-only CP-03 evidence, missing task/load, unknown changed capability or omitted affected denial/activation cannot establish compatibility. New control/transfer contract requires Full; compatible naming alone cannot waive it. |
| VPI-07 / D,S | Candidate required assertions PASS and a matching intact baseline quality FAIL under expectation=observation completes the comparison; candidate judgment remains PASS. | Delete baseline, mismatch raw facts/conditions, or replace candidate FAIL with a passing paired summary: no sufficient comparison/candidate PASS. Actual candidate required FAIL yields validation FAIL. |
| VPI-08 / D,S | Full selection/results account exactly once for all original catalog assertion/variant/arm instances with required D/S/N kinds, including genuine scope exclusions. | Omit one original native obligation, duplicate identity, weaken N to D, drop a required variant or insert orphan graph node: REJECT Full completeness even when every remaining listed task says PASS. |
| VPI-09 / D,S | One actual raw observation may serve multiple compatible assertions with identical identity/input/prompt/arm/visibility/freshness and valid prerequisite order; each keeps its result and shared sample disclosure. | Reuse across opposite arms/variants, force a skill path in an implicit case, change conditions, reuse stale evidence or use post-T09 observation for pre-T09 admission: REJECT reuse/sufficiency. |
| VPI-10 / D,S | One fresh independent paired review emits separate actual arm/assertion judgments against both complete raw outputs, with context/order/arm leakage recorded. | Missing arm, author-as-reviewer, prewritten judgment, aggregate-only grade or unsupported independence/correlation claim: insufficient/rejected sufficiency; no additional recursive reviewer is required. |
| VPI-11 / D,S,N | A synthetic transcript can make the intended deterministic detector/reducer branch pass. | The same transcript offered for native clean-negative, installed-resource, source/history isolation, callback-origin, actual nested execution or receiving evidence: REJECT native sufficiency. Original SV-009/012/024–028 native requirements remain selected as applicable. |
| VPI-12 / D,S,N | Before Full T09, an eligible actual target output is loaded by its receiver and the required action/expected negative disposition is observed with exact contract/identity evidence. | Substitute fixture output, a prepared evaluator T12 handoff, missing receiver action or evidence created after T09: no FULL_PASS. Completing evaluator T12 enqueues zero recursive qualification calls. |
| VPI-13 / D | A distinct external native grant binds total/per-unit/time caps, unchanged origins and complete typed graph (native workers, static review, graders, meaningful returns, continuations); failed allocated launch remains charged. | Reuse 24/24/0, 1/1/0 or 2/2/0 funding, treat nine engineering generations as native grant, omit review/return/continuation, dispatch outside graph, exceed cap or reset clock: REJECT. Collector and scheduler use identical selected ceilings. |
| VPI-14 / D | Resume reconstructs original deadlines, challenges, counters and current selected bytes from protected journal; final custody binds actual outputs and honest outcomes/lineage. | Reset origin/counter, reuse challenge/receipt, change final bytes or acceptance lineage, stale review, receipt destination collision: REJECT current completion. Unknown tokens/person-time stay null/NOT_OBSERVABLE, never zero or PASS. |
| VPI-15 / D,N | Staged project-local installation/export retains exact selected runtime resources and omits evals; identical compatible managed refresh is idempotent. | Wrong binary/capability, modified owned destination, unsupported version or unreviewed provider-wide scope: reject before writes. D staging does not supply later actual native installed-load evidence. |
| VPI-16 / D,S,N | ROUTINE_PASS with bound scope and required checks can support one actual carried owner acceptance/install decision; current routine identity advances only in that owner's successor record. | Helper-issued human approval, moving qualified identity on Routine, claiming Full for new bytes or bypassing explicit Full release/CI-05 enforcement-adoption requirement: REJECT. This implementation remains unqualified pending matching Full. |
| VPI-17 / D,S | Missing required native observation is COULD_NOT_RUN/NOT_RUN with cause; honest P5/P6 may produce COMPLETE reporting and prepared handoff, validation INSUFFICIENT_EVIDENCE. A genuine scope exclusion retains NOT_APPLICABLE and basis. | Report completeness, workspace PREPARED or a reviewed unselected disposition used as native PASS: REJECT claim. Unselected native observation remains NOT_RUN. Known required candidate/protocol failure yields FAIL, not insufficient evidence. |

Representative minimal fixtures for G2 are synthetic independent requirement inputs: (1) spelling-only Routine with D/S required and C/B/A unselected; (2) trigger-only Routine with matching C and A selected and B unselected; (3) matched candidate/baseline B with candidate PASS and baseline FAIL; (4) Full inventory containing one explicitly N assertion; (5) two-edit Routine lineage with a fixed earlier anchor; (6) distinct funded graph with one static reviewer, one native worker and one explicit continuation. Mutate one discriminator at a time. Freeze fixture expected outputs from this table before implementation; an implementation-produced expected value is not RED evidence. Use the actual legacy parser/reducer to observe relevant initial rejection/failure before changing behavior. G1 does not run it.

### Deferred observations and delivery state

R2-11 remains a documented authentication-lifecycle/evidence-state distinction, with no native reuse mechanism claimed. R2-12 Stage A is COMPLETE, with its preserved advisory that automated dispatch/detection/capture intervals are not model service or human person-time. Its monotonic closeout exceeded the 240-second sublimit by 3.785463266 seconds; the final failed check was not retried. Unknown internal usage and human time remain NOT_OBSERVABLE. No subscription-affordability conclusion follows. The original 24/24/0, R2-REVIEW 1/1/0 and CMP-2.A 2/2/0 ledgers stay separate/exhausted; VPI engineering funding never reopens them or supplies a native campaign grant.

G1 authors contracts/templates and a hash-bound downstream handoff only. Runtime implementation, deterministic RED/GREEN, independently reviewed combined implementation, native behavior/control/activation, installed compatibility, actual receiving transfer and qualification are separate evidence layers. G2 and G4 must consume the same committed schema/expectation bytes. A schema/consumer requirement outside their fence is a concrete scoped blocker, not permission to widen ownership. Final native observation allocation/count and supported transport remain for separate qualification planning.

Validation status for this G1 authoring: Not performed. Native observations: NOT_RUN. Hook status: Design only. No implementation, independent review, qualification or operational-readiness claim is made by this amendment.
