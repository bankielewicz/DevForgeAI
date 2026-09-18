---
id: DFF-12
status: planning-baseline
implementation_readiness: not-ready
updated: 2026-09-15
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

## Compatibility and migration register

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

Select I1. Read index, foundation, core-workflows, project-context-and-policy and the relevant ambiguity rows. Trace (a) fictional OrderDesk cancellation before/after dispatch plus its race invariant and (b) a new-product idea with unresolved stakeholder needs. Identify necessary artifacts, their consumers and readiness conditions; explicitly show which upstream activities can be reused or omitted. Resolve first-release workflow responsibilities and policy provenance. Inspect supported Codex/Pro surfaces needed by that route without changing operational configuration. Return updated owned documents, resolved/open decision IDs, and the next bounded contract task. Do not implement a runtime or install agents as a side effect.

## Documentation verification and continuation discipline

Link/readback checks and adversarial walkthrough findings are recorded in [verification](../../plan/framework-foundation/20260915T111940Z/verification.md). Documentation checks do not establish TDD, native coverage, subscription-wide support or framework acceptance. Future sessions inspect actual current files and evidence before promoting any capability's status. Original specifications and evaluation attempts remain retained.
