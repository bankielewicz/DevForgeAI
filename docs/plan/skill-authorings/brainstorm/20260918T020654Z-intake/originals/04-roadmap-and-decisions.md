---
id: DFF-12
status: planning-baseline
implementation_readiness: not-ready
updated: 2026-09-17
---

# Roadmap, decisions and unresolved questions

[Framework index](index.md) · [Retained enhancement discussion](../../plan/devforgeai-adaptive-framework-enhancement-notes.md)

## Scope and status

This record owns the planning sequence and disposition of decisions, not runtime authority. The authorized delivery is the connected documentation baseline. It does not implement the framework, install skills/agents, alter existing QA policy, repair the index application or change a remote host.

The core must work within supported Codex and an individual ChatGPT Pro subscription. Any feature requiring unverified host behavior, extra LLM/API billing, Enterprise privileges, persistent autonomous workers or a stronger OS boundary than is actually provisioned is not implementation-ready. Record the exact dependency and blocked claim. An optional extension cannot become an undocumented core prerequisite.

## Decision register

| ID | Decision / disposition | Governing document |
| --- | --- | --- |
| DEC-01 | Confirmed: portable across managed project languages, stacks and domains; DevForgeAI runtime implementation remains Rust | DFF-01/04 |
| DEC-02 | Confirmed: guide useful work with guardrails; do not mandate every reasoning step or a fixed waterfall | DFF-01/02 |
| DEC-03 | Confirmed: managed projects select policy; DevForgeAI's own engineering requirements remain in force for this repository | DFF-04/08 |
| DEC-04 | Confirmed: core, project variants and expertise retain distinct responsibility and lineage | DFF-05 |
| DEC-05 | Confirmed: one connected artifact/dependency model; preserve independent QA and its repair handoff | DFF-02/03/08 |
| DEC-06 | Confirmed: preserve earlier story/subagent/phase/Rust ideas for review, including objections and superseded assumptions | Enhancement notes |
| DEC-07 | Confirmed: story count follows selected capabilities/dependencies; no global numeric cap or one story per acceptance row | DFF-03 |
| DEC-08 | Selected in earlier bounded proposal: Windows-first protected authority, collecting separately qualified Windows/WSL/Linux evidence | DFF-07/11; not a universal installation requirement |
| DEC-09 | Selected in earlier proposal: phase-transition control, not brokerage of every draft mutation | DFF-07; concrete core workflow still unresolved |
| DEC-10 | Selected then constrained by cost concerns: bounded continuation, and revalidation after test changes | DFF-06/07/08; exact triggering/budget/invalidation needs review |
| DEC-11 | Proposed after adversarial review: one story owner by default, with specialists where independence or parallelism earns its cost | DFF-06; not a mandated four-agent process |
| DEC-12 | Confirmed documentation requirement: customizable agent attributes, model/effort and inheritance/compatibility limits must be recorded | DFF-06 and captured schema |
| DEC-13 | Proposed: separate expert-health dimensions and bounded realignment; no composite competence score or automatic operational rewriting | DFF-09 |
| DEC-14 | Confirmed latest constraint: supported Codex + individual Pro only for base operation; no aspirational capabilities outside those confines | DFF-01/11 |
| DEC-15 | Confirmed: ambiguity is retained with affected work and a resolution question; it is not silently guessed or mislabeled ready | This register and each capability's open decisions |
| DEC-16 | Confirmed continuation: keep runtime/MVP/evaluation specifications subordinate to this framework; preserve alternatives in planning notes rather than copy the foundation | Index; enhancement notes sections 9–12 |
| DEC-17 | Selected direction to specify: headless Rust workflow engine with dispatch, accessed through Codex; no custom terminal. Assisted mode is a distinct reduced alternative, not silent fulfillment | DFF-RUNTIME-01; adapter/support remains open |
| DEC-18 | Selected needs: durable obligations, incremental progress, project context and recoverable work. Database counts and role/workflow file splits remain proposals requiring justification | DFF-RUNTIME-01; DFF-10 |
| DEC-19 | Confirmed evaluation goal: improve independently verified outcomes within declared conditions; no demonstrated competitive ranking or universal superiority | DFF-EVAL-01 |
| DEC-20 | Confirmed next step: preserve discussion and define MVP scope/acceptance plus evaluation together; finalize one bounded implementation contract before a fresh coding session | DFF-MVP-01/02; next-session handoff |
| DEC-21 | Selected documentation, 2026-09-17: phase 1 is brainstorm in an optional discovery route; no existing numbered phase 0 was found and no mandatory phase 0 is introduced | DFF-02; DFF-WF-01 |
| DEC-22 | User-selected names: brainstorm -> prd-create -> prd-review; work planning and story creation follow sufficient selected requirements/design, with alternate entry routes preserved | DFF-02 |
| DEC-23 | Documented intake distinction: setup, selected work and product discovery have separate ownership but may share one conversation and reuse supplied answers | DFF-02/04/11; MVP-01 |
| DEC-24 | Specified first brainstorm packaging: ordinary standalone skill with a reusable core responsibility; no adaptive descriptor/binding exception is inserted into existing schemas | DFF-WF-01; DFF-05; AMB-12 remains open generally |
| DEC-25 | Documented readiness target: zero known unresolved blocking ambiguities for selected work; no claim of absolute certainty or calibrated AI-completion probability | DFF-03; future persisted schema remains open |
| DEC-26 | Documented continuity: provenance, dependency-aware parallel work, combined-candidate QA, authorized delivery and feedback during work; existing skill scopes and MIG-01/02/03 remain intact | DFF-03/04/08/09/11 |

## Ambiguity register

Open questions are intentional planning outcomes. The blocked item is the affected implementation/readiness claim, not all independent planning. No row means permission to invent the missing behavior. Resolution updates the owning document and records evidence, rationale and remaining limits here.

| ID | Exact unresolved question | Resolution evidence / owner | Blocked claim |
| --- | --- | --- | --- |
| AMB-01 | Which Codex version/backend and Pro-accessible features form the first supported profile? | DFF-06/11: native profile/hook trials, current official docs, actual account capability observations | Universal custom-agent/hook compatibility |
| AMB-02 | Which model/effort combinations and usage telemetry can this profile actually expose? | DFF-06: supported model listing and explicit successful/denied configuration observations; no secrets | Guaranteed model availability, exact cost/budget enforcement or unlimited continuation |
| AMB-03 | How can the selected local host provision protected state/operator identity without relying on Enterprise features? | DFF-07/11: concrete OS principal/IPC/ACL design, explicit installation authority, denied-write qualification | Protected acceptance/receipt claims; advisory work remains possible |
| AMB-04 | Which initial workflow responsibilities and entry routes form the first release, and what makes their inputs sufficient? | DFF-02-Q1..Q3 plus a new-product and brownfield walkthrough | Finished core workflow/schema and implicit route automation |
| AMB-05 | What exact identifiers, schemas and transition predicates bind an epic, story, defect, candidate and run? | DFF-03-Q1..Q3, DFF-07: producer/consumer examples and failure cases | An implemented workflow interpreter or deterministic story scheduler |
| AMB-06 | How are conflicting stakeholder requirements and authorized policy amendments resolved and attributed? | DFF-04: explicit source/precedence and amendment contract | Guessing business truth or weakening effective standards |
| AMB-07 | What independence is needed for each QA/human assessment, and how is it established within a single-user Pro installation? | DFF-08-Q1..Q4 and DFF-07: threat/ownership boundary plus executable provenance checks | Treating a named subagent as a protected independent principal |
| AMB-08 | When does a test correction invalidate Red/Green or other evidence, without forcing unnecessary cycles or rewriting chronology? | DFF-08/06: changed assertion, fixture-only and formatting-only examples with exact dependencies | Automatic restart of all TDD phases after any test edit |
| AMB-09 | What constitutes useful continuation progress, what is the limit, and how are interruption, usage exhaustion and uncertain effects handled? | DFF-06/07: bounded native trial with preserved open work and no repeated blind command | A reliable autonomous keep-working controller |
| AMB-10 | When is a distinct expert/package justified versus shared references, and who owns its evidence baseline? | DFF-05: one core, one justified specialization, a real handoff and lineage review | Automatic expert generation for every organizational title |
| AMB-11 | How are stable assertions, health denominators, independent labels, review triggers and limits represented? | DFF-09: changed rule, unchanged control and incompatible-handoff observations | A validated slippage score, monitoring service or automatic realignment |
| AMB-12 | How does advisory/uninstalled expertise coexist with the current adaptive binding-required contract? | DFF-05/11: explicit version/compatibility decision | Silently bypassing existing binding checks |
| AMB-13 | How do package ownership, updates, rollback, relocation and uninstall preserve user modifications? | DFF-11: exact effect/manifest/schema contract and disposable failure scenarios | A portable installer/updater |
| AMB-14 | Which Git/GitHub integrations are available without extra LLM/API/Enterprise dependencies and how are downstream decisions trusted? | DFF-11: explicit project/service prerequisites and local deterministic/remote test boundary | An always-on hosted Codex CI service or unconfigured merge protection |
| AMB-15 | Which checkpoint and context references are sufficient after compaction without reloading everything or hiding failures? | DFF-10: cold resume with changed input and missing evidence | Guaranteed memory or lossless model understanding |
| AMB-16 | Which documented Codex interface and support category can supply Rust-owned worker dispatch under Pro, including permissions, progress, cancellation and worker lifetime? | DFF-RUNTIME-01 with AMB-01/02/09: bounded feasibility contract, version/profile observations and exact scope decision; native success cannot override experimental production limits | Implemented or production-supported orchestration; silently substituting Rust-assisted mode |
| AMB-17 | What project/checkout identities, storage ownership, transaction boundaries, cursor/restore semantics and data lifecycles are required for the first unit? | DFF-RUNTIME-01/DFF-10 with AMB-03/05/15: concrete schemas and crash/replay/missing-artifact cases; measured workload before contention-driven splits | A fixed DB topology, protected home storage, cross-host shared SQLite or claimed I/O improvement |
| AMB-18 | Which cohort, comparators, runner/oracles, budgets, repetitions, uncertainty method, eligibility rule and improvement margin define the first fair comparison? | DFF-EVAL-01 EVAL-Q1..Q6: frozen pilot inputs and independent judging procedure, then separately defined ranking campaign | Executable benchmark readiness, invented costs, scores or superiority |
| AMB-19 | Which smallest useful unit, exact Rust package/source/test destination and dependency versions form the first coding contract? | DFF-MVP-01 and next-session handoff: current source inventory, complete bounded contract and executable acceptance oracles | Coding the entire planning baseline or replacing the existing index package by assumption |
| AMB-20 | How do project versus checkout identity, package availability and binding placement support concurrent worktrees under an absolute-root binding contract? | DFF-03/11 with AMB-17: versioned compatibility decision, separate-root/concurrent-update/preservation cases | Claiming parallel binding-required execution from copied bindings or Git worktrees alone |
| AMB-21 | Which pre-binding setup entry point, exact Rust operations and recovery contract create the first valid binding without requiring it first? | DFF-11 with AMB-12/13: standalone bootstrap or selected versioned contract, concrete effects and failure cases | An implemented project-setup-and-activation skill, first-use auto-binding or Python authority fallback |

## Discovery workflow disposition, 2026-09-17

The user selected documentation of the intake/setup/discovery discussion and the first workflow specification, then explicitly chose the names brainstorm -> prd-create -> prd-review. A scoped search of the pre-edit framework Markdown found no numbered phase 0 or phase 1. [DFF-WF-01](workflows/phase-1-brainstorm-spec.md) now specifies phase 1 as a portable discovery skill with a revisioned Markdown brief, explicit handoff dispositions, 14 requirements and 20 future independent assessment cases. This is a documentation result, not an authored skill or executed assessment.

This narrows AMB-04 only for discovery inputs and the brief-to-PRD handoff. Full PRD creation/review contracts, broad work-item/readiness schemas, automated routing and protected transitions remain unresolved or separately selected work. Standalone first-version packaging avoids adding a new setup dependency to brainstorm; it does not bypass story-create checks, add binding_required to dev, alter closed adaptive schemas or close AMB-12 generally.

The applicable owner documents now record: intake at three levels; iterative architecture/PRD/prototype work; useful rather than mandatory constitutional files; canonical provenance; scoped readiness and uncalibrated-score limits; shared-contract/resource ownership for parallel work; optional sprints; combined-candidate and applicable UI QA; existing delivery authorization; and continuous feedback. Setup uses the existing project-binding-v1 interface while AMB-13/20/21 retain the missing installation/bootstrap/worktree behavior. MIG-01/02/03 are unchanged.

[Input identities and before snapshots](../../plan/framework-discovery-planning/20260918T014059438Z/inputs-before.json) preserve the earlier documents. Prior runtime, source, operational skills, specifications outside the selected framework documents and retained evidence are not rewritten by this work. Historical manifests still bind their original bytes; a later consumer must select and verify the revision it actually uses.

## Compatibility and migration register

### First worker contract disposition, 2026-09-15

[DFF-WORKER-FEAS-01 v1.0.0](runtime/codex-worker-feasibility-v1.md) and its [coding handoff](../../plan/framework-worker-coding-handoff.md) resolve AMB-19 **for the isolated offline harness only**. Its own local request/identity/journal contract supplies bounded AMB-05/17 decisions; its one-turn lifetime and no-replay inspection supply bounded AMB-09/15 decisions. They do not settle general workflow schemas, production lifetime or persistence topology.

AMB-16 selects installed Codex 0.154.0 app-server over stdio for nonproduction investigation; its generated schema was captured locally. The interface remains experimental/unsupported for production, and the actual Pro/model/permission profile under AMB-01/02 is untested. AMB-03/07 protected authority/independence remain open. AMB-04/06 still own actual OrderDesk business semantics; the probe's synthetic transition table does not decide them. AMB-18 receives one fixed feasibility fixture and resource limit, without resolving comparative ranking or runner qualification. AMB-08/12 and all unrelated ambiguities retain their earlier scope.

The earlier ambiguity rows remain the full-framework questions. Read this scoped disposition with them; none is globally closed by a protocol prototype. [Discovery and documentation evidence](../../plan/framework-worker-contract/20260915T151300Z/verification.md) records ten matched handoff input hashes, tool versions, warnings and unperformed native checks.

### Existing migration questions

| ID | Observed issue | Required disposition |
| --- | --- | --- |
| MIG-01 | Current dev derives project thresholds; current qa fixes >=95% minima and forbids all confirmed first-party mock decorators | Specify project-policy integration and independently validate any later skill change; current packages remain unchanged |
| MIG-02 | Current qa stops a run for valid subthreshold metrics/integrity triggers; dev can continue independent authorized remediation | Model role/mode-specific transitions and handoffs; do not flatten into one generic retry loop |
| MIG-03 | Existing adaptive records are closed schemas; variant update review does not fully define expert evidence-baseline updates | Select versioned extension/migration with retained history, not opportunistic extra fields |
| MIG-04 | The index package exists, but the protected authority remains design-only; query extension is a separate selected contract | Inventory actual behavior before reuse; never rename index observations into acceptance |
| MIG-05 | Historical workflows contain fixed phase counts, shell enforcement and environment assumptions | Extract needed responsibilities only; no automatic port of claimed enforcement or legacy commands |

## Planning iterations and dependency order

| Iteration | Bounded outcome | Prerequisites / exit evidence |
| --- | --- | --- |
| I1 Foundation | Vocabulary, Codex/Pro profile boundary, policy selection and lifecycle handoffs | This baseline; resolve essential AMB-01/04/06 for two walkthroughs |
| I2 Work contracts | Requirement accounting, proportional decomposition, work IDs and selected-scope dependencies | I1; apply to one bounded existing specification and challenge proposed splits |
| I3 Delivery and guardrails | One complete implementation/QA/repair path, current-candidate evidence and exact protected boundary | I1/I2; resolve relevant AMB-03/05/07/08/09, not all future integrations |
| I4 Adaptation | One grounded expert/variant, useful agent customization and evidence-based maintenance | I1/I2 and evidence contract from I3; resolve relevant AMB-02/10/11/12 |
| I5 Integration | Concrete installation/host contract, continuity and selected end-to-end qualification plan | Stable selected contracts; resolve relevant AMB-13/14/15 and remaining host gaps |

These are planning increments, not five compulsory runtime stages or five implementation epics. Parallel independent definition work is permitted; dependent implementation waits for its actual decisions. Every iteration ends with current decisions, preserved gaps, updated links and a bounded next task. Do not generate a large backlog before its contracts and dependency boundaries are understood.

## Next session task

For the discovery work stream, the next selectable authoring input is [DFF-WF-01](workflows/phase-1-brainstorm-spec.md); the next workflow specification is prd-create, followed by prd-review. Selecting this documentation task does not automatically select skill authoring or either later specification. Their required consumers and review boundaries are recorded in DFF-02 and DFF-WF-01.

The earlier [MVP planning handoff](../../plan/framework-mvp-next-session.md), [DFF-WORKER-FEAS-01 v1.0.0](runtime/codex-worker-feasibility-v1.md) and its [scoped coding handoff](../../plan/framework-worker-coding-handoff.md) remain a separate runtime work stream. Native Pro trials remain separately selected and profile-dependent. Inspect current candidate/evidence before that work; do not begin implementation from this entire planning directory.

The earlier I1 checks remain prerequisites where relevant: trace fictional OrderDesk cancellation/race and the minimal new-product entry with unresolved stakeholder needs; identify artifact producers/consumers, permissible reuse and policy provenance. These checks now feed the bounded [MVP scope](mvp/scope.md), not another broad brainstorming cycle. Inspect supported Codex/Pro interfaces and current Rust source without changing operational configuration. Return exact selected contract identities, resolved/open AMB IDs and the coding handoff. I1–I5 above remain a dependency map, not an instruction to complete every future design before one ready unit can be coded.

## Documentation verification and continuation discipline

The [original foundation verification](../../plan/framework-foundation/20260915T111940Z/verification.md) is historical evidence for the earlier document bytes. [Current MVP planning verification](../../plan/framework-mvp-planning/20260915T145455Z/verification.md) records the continuation's link/readback checks, selected input preservation and independent review. Documentation checks do not establish TDD, native coverage, subscription-wide support or framework acceptance. Future sessions inspect actual current files and evidence before promoting any capability's status. Original specifications and evaluation attempts remain retained.
