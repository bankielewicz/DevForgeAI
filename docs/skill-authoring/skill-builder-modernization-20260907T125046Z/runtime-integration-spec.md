# Prepared builder/validator runtime integration specification

Status: prepared implementation requirements, not an executed handoff, runtime adapter, hook activation or acceptance. Allocated next owner: DevForge protected-runtime/integration owner, as assigned by SENH revision 3. Personal owner identity, external execution assignment, runtime version/build and implementation worktree/fence are not supplied; the receiving owner must bind these before protected writes. This document does not grant them.

## Scope and authority

Implement CHG-001 and CHG-003 runtime portions and coordinate CHG-002 validator refresh under separately allocated ownership. The current user authorizes this specification and builder-owned source changes only. Preserve SB01–SB10, historical F-001/F-002 MINOR findings, old static outcomes and native COULD_NOT_RUN records. SENH-v3 does not retroactively replace their original evaluation inputs.

Selected inputs are in selected-inputs/ with exact hashes in input-record.json. Current authoring and execution contracts are revision 3, matching the amendment's preserved modernization source digests. The shared handoff source is docs/mvp/templates/shared/handoff.md, the same governing path used by validator, now explicitly selected at its current bytes. Validator's older copy is unchanged; its controlled refresh belongs to its author. Prior builder bytes/derivation are in before/skill-builder and before-manifest.json.

## Responsibility allocation

| Owner | Deliverable |
| --- | --- |
| Builder skill | Useful Q&A, search/comparison, specification and candidate content, decision/proposal distinctions, change dispositions and prepared handoff using package-local template |
| DevForge runtime owner | Utility adapter/state schema, admission, evidence predicates, phase transitions, waiting, bounded correction, immutable journal, final-byte checks and authoritative receipt publication/readback |
| DevForgeAI shared integration owner | Selected contract and provider packaging/schema reconciliation, installation/export and one effective callback per event; coordinate validator source author |
| Validator source author | Controlled revision-3 resource/instruction refresh, six-phase semantic evidence interface; preserve independent evaluation responsibility |
| Separately allocated evaluator/operator | Deterministic and native evidence, including effective configuration, denial, continuation and delivery observations |
| User/acceptance owner | Actual scope/classification/adoption and external acceptance decisions |

No author edits shared policy to pass, self-approves a gate, launches receiving skills from a prepared prompt or claims a reducer authenticates native execution.

## Builder admission and transitions

This is a required adapter design, not a claim of actual allowed transitions in the current brainstorm implementation. Do not coerce utility work into Recover/Explore/Record/Focus. Reuse shared artifact schemas and protected journal mechanisms where their semantics fit; allocate/version any utility extension with the schema owner before implementation.

The builder's original full standalone design is unavailable. The recovered SB01–SB10 specify substantive obligations and asking Optional/Enforced for unclassified target items; they do not supply a universal builder phase classification matrix. Preserve that missing-input fact. The following adapter content states name existing work, not newly adopted user classifications. Admission must bind the actual task's preserved classifications and conditional applicability. Unknown classification affecting a dependent action leaves that action unadmitted, with useful independent authoring permitted. No per-phase approval ceremony is introduced.

| State | Concrete evidence supplied by skill | Proposed normal next state and runtime predicate |
| --- | --- | --- |
| Intake | Selected request/authority, target/provider, accepted input locators, material gaps and write scope | Selection only with resolved target ownership and bound inputs |
| Selection | Actual search locations and candidates, comparison and selected reuse/enhance/create rationale | Design with accepted selection; bounded remediation may reuse retained search explicitly |
| Design | Requirement content, source-backed decisions, preserved item IDs/classifications, missing questions, enforcement proposals and intended artifacts | Authoring when consequential inputs and applicable required decisions are resolved |
| Authoring | Actual skill/spec paths, change mapping and prior-byte preservation | Prepared transfer when required outputs and supplied evidence exist and bind the admitted task |
| Prepared transfer | Handoff content, next owner/prerequisites, actual saved outputs, honest absent observations | READY only if every applicable required predicate/evidence is current; receiving invocation remains separate |

Runtime allows no arbitrary forward jump. Reuse or bounded remediation can consume retained evidence instead of redoing settled Q&A, only through an owner-selected applicability mapping; the model cannot self-exclude required work. Optional items require explicit applicability/skip basis and are never silently promoted to Enforced. Material scope/input changes invalidate affected downstream evidence and require a newly bound assignment or owner-authorized recovery, not model rewind of accepted state. Read-only discussion does not create a managed handoff.

Any phase may enter WAITING_USER with question ID, affected dependency and evidence of the consequential gap. A new user message returns context for the pending phase, not automatic admission: the answer must resolve that question and adoption must have a real source. Unrelated answers retain waiting. Independent permitted work may continue. Failure, expiry, unavailable authority and exhausted correction leave dependent workflow incomplete; a failure/recovery handoff may preserve content without a successful transition receipt.

## Validator adapter and preserved classifications

The selected existing skill-validator-design.md explicitly classifies W1, P1–P6 and T01–T12 Enforced. Preserve those named groups, not a parent-derived assumption:

| Phase | Tasks | Required evidence / allowed dependency |
| --- | --- | --- |
| P1 Intake | T01 identify authority/target; T02 freeze inputs/plan | Actual assignment and selected candidate/spec/cases/rubric/baseline/runtime/budget bindings before P2 |
| P2 Deterministic inspection | T03 | Saved scoped inspection records before dependent measurement |
| P3 Independent AI review | T04 | Producer-bound rubric/evidence records; semantic judgment does not grant gate authority |
| P4 Native observations | T05 isolation; T06 C; T07 B; T08 A | Observed prerequisites and authenticated producer records; normal order C then B then A |
| P5 Adjudication | T09 | Bound raw outcomes, applicability, missing observations and scope; no self-issued release PASS |
| P6 Reporting/transfer | T10 results; T11 enhancement specification; T12 custody/handoff | Actual saved artifacts and next owner; runtime independently controls final identity/receipt |

Normal phase dependency is P1→P2→P3→P4→P5→P6. Missing native prerequisites block dependent execution but allow P5/P6 incomplete-evidence reporting with original causes; this exception is not a passing evaluation or exclusion of Enforced tasks. Runtime must distinguish report completion from required evidence satisfaction and acceptance. Retain all planned C/B/A outcomes separately. Older H1–H5 PreToolUse/Stop proposals must be reconciled as traceable requirements against the managed events, not blindly activated alongside them.

## Protected context and checkpoint evidence

Supply task/assignment ID, owner identity, workflow/schema version, current phase and journal sequence, accepted input manifest, installed package identity, permitted output paths, evidence schema, unpredictable one-use challenge, original absolute deadline, remaining correction budget and protected receipt destination. Exact utility schema ID is unallocated; do not claim brainstorm-session/v1 accepts these new phases. Use devforge.artifact/v1 for human-readable handoffs and existing locator/manifest conventions. The producer does not select its own authoritative paths or deadline.

Evidence must bind the supplied task, phase, sequence, challenge and input snapshot; include actual artifact locators and sections, adopted-decision sources, unresolved-question dependencies and scoped producer observations. Model declarations remain untrusted. Runtime reads actual final bytes and checks permitted paths, existence, schema requirements, identities, freshness and the allocated producer/assignment of evidence. A valid locator is not semantic proof; semantic review consumes the underlying content with its own recorded producer/limits. Native records need independently established execution custody; a log digest or reducer-declared PASS alone cannot authenticate them.

Protect runtime executable, accepted inputs/journal, state, challenge issuance and receipt store from worker writes. Reject missing, invalid, stale, replayed, wrong-task, wrong-phase and wrong-producer evidence, changed inputs, missing retained output baselines and path substitutions including symlink escape. Bind waiting to the question and unchanged deadline. Select bounded correction limits at admission (the current brainstorm contract permits one correction per phase); do not silently reuse limits or reset budgets on resume. Exhaustion/expiry prevents dependent completion and retains diagnostics.

## Completion and callback reconciliation

Before utility adapter deployment, inspect the selected runtime implementation and official documentation for the actual installed Codex version. This authoring task makes no fresh native capability claim. Existing source declarations are synchronous SessionStart, UserPromptSubmit, Stop and SessionEnd, with no conditional matcher. Proposed coverage: SessionStart admits context; UserPromptSubmit supplies pending context without certifying an answer; Stop inspects evidence and controls bounded continuation/READY receipt; SessionEnd records lifecycle outcomes without inventing successful delivery. The receiving owner must establish actual event coverage, trust, response semantics and errors. Feasibility: Partial at shared architecture level; utility adapter and native coverage Unknown/unobserved. Proposal status: Design only; not installed, activated, executed, or validated.

Bind the existing six-field runtime requirement only where compatible; any schema/version change is shared-owner work. Exclude duplicate effective callbacks across project/plugin/global configuration during admission. Fail closed for an admitted managed task if transport/configuration or authority is unavailable; an inactive/unmanaged task must not claim enforcement. Preserve unrelated configuration. Do not add worker-controlled callback sources or a receipt-helper fallback.

On a qualifying Stop after required predicates reach READY, runtime reopens actual artifacts, computes final identities, preserves inspected bytes, exclusively creates the selected external receipt, reads back its complete bytes and verifies targets before returning its locator/full digest. Receipt references the prepared handoff, which excludes its own digest and is never rewritten to claim later events. Changed bytes prevent a current completion claim. Repeated Stop rechecks and may reemit the same immutable receipt only when applicable; collisions never overwrite. Preserve committed task result independently of later process failure. Record publication, response transport, native turn completion, receiving invocation and rendered human delivery separately. SOCKET_WRITE_COMPLETED cannot mean rendered delivery. Actual invocation requires separately allocated receiving execution and matching observation; a next-session prompt is insufficient.

## Required future evidence; not executed here

| Case | Required observation |
| --- | --- |
| Typical builder Q&A/search/remediation | Useful scoped artifacts; no repeated settled interview; decisions distinguished from proposals |
| Missing or unrelated user answer | WAITING_USER persists; dependent action blocked; no deadline reset |
| Required phase skipped / marker-only completion | Admission denied; no completion receipt |
| Missing/stale/replayed/wrong-phase/wrong-owner evidence | Rejected against protected state with bounded correction |
| Modified inputs, symlink/path escape, changed final bytes | Dependent completion prevented; prior accepted snapshot preserved |
| Correction exhausted / deadline expired / recovery | Incomplete result with retained cause; no budget reset or fabricated success |
| Receipt collision, duplicate Stop or later drift | Exclusive publication; current recheck before reemission; old record retained |
| Native disabled/duplicate/failed callback or transport | Observed denial/continuation semantics and one effective callback; no inferred enforcement |
| Validator unavailable C/B/A | Separate COULD_NOT_RUN/NOT_RUN causes and complete reporting, no suitability/acceptance inflation |
| Valid bounded builder→validator transfer | Correct artifacts, independently observed receipt and separately evidenced receiving invocation |

Evaluate deterministic mechanics, substantive behavior, native integration and delivery separately on newly allocated frozen inputs. Preserve all historical failures. Implementation completion requires owner-bound adapter/schema/source artifacts and separate test evidence; native conformance additionally requires actual callback/receipt delivery observations. Nothing in this prepared specification performs those actions.
