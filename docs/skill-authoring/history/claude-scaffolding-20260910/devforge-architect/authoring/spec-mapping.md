# Specification mapping: SKILL-005 to the authored package

Governing specification: `docs/mvp/specifications/skill-005-devforge-architect.md` at `c17e758417da64928a0f47fc2600304465ac3f3c`, SHA-256 `b9dc3a5a2d19a024c42b60539909009d9d9292e54f3509739a8ae575311ea88b`.

Paths below are relative to `providers/claude/plugins/devforgeai/skills/devforge-architect/`. Every row states where a requirement is carried and, for a behavioural row, which eval case would observe it. **A mapping is not an observation:** nothing in this table has been evaluated, and the eval case IDs identify cases that are `NOT_RUN`.

## User goal and use-case inventory

| Specification row | Where it is carried | Eval case |
| --- | --- | --- |
| User goal: record architecture, dependency versions, source layout, interface responsibilities, test policy for a delivery slice | `SKILL.md` frontmatter description; `SKILL.md` opening; phase 3 Specify | trigger A2a-A2d; evals 1-3 |
| Direct request: "Use DevForgeAI to establish this project's architecture and stack contract" | Description, direct-domain clause; used verbatim as trigger A2a and as the eval 1 prompt | trigger A2a; eval 1 / ARCH-B-001 |
| Indirect request: "How should we structure this SaaS so later sessions do not introduce incompatible libraries?" | Description, indirect clause; used verbatim as trigger A3a | trigger A3a; eval 2 / ARCH-B-002 |
| Expected result: architecture-contract plus a standardized handoff | `SKILL.md` phases 3 and 4; `assets/architecture-contract.md`; `assets/handoff.md` | evals 1-4, 7 |
| Required context: accepted scope, relevant designs and experiments, the real repository, verified documentation | `SKILL.md` "Inputs" table; phase 1 Inventory | evals 1-4 |
| Plugin capability, and the POC's synthetic dependency check not being a NuGet/npm adapter | `SKILL.md` "External checks and what they prove"; `references/framework-context.md` command table and "Missing integrations to name rather than assume" | eval 2 (enforcement requirements); eval 9 |
| State/action boundary: author a proposal, record actual decisions; cannot make policy effective or replace a stack by prose | `SKILL.md` "What this skill owns and does not own", phase 4, and the external-checks section; `references/recording-rules.md` "Decisions versus proposals"; `references/version-evidence.md` "An existing stack is a decision already made" | evals 3, 4 |
| MVP support decision: existing projects begin with an evidence-backed inventory rather than a replacement architecture | `SKILL.md` failure mode "Replacing what already works" and phase 1; `references/version-evidence.md` | eval 3 / ARCH-B-003 |
| Does not activate for: a new library release is not authorization to upgrade; route through change | Description near-miss clause naming `devforge-change`; `references/version-evidence.md` "A newer release is a research trigger, not an upgrade" | triggers A4a, A4b |

## Shared authoring requirements

| Specification requirement | Where it is carried |
| --- | --- |
| Skill-authoring contract governs provider source ownership, runtime packaging, scripts, reproducible eval fixtures, separate A/B/C results | Package lives in the Claude provider source; `evals/` excluded from installed copies per `references/framework-context.md`; no `scripts/`; fixtures reproducible from source; `evals/evals.json` tier note and `evals/triggers/trigger-queries.json` keep the tiers separate |
| Existence of prior instructions is not evidence of conformance | No prior `devforge-architect` existed; recorded in the design document's selection section |

## Inputs and provenance

| Input row | Where it is carried | Eval case |
| --- | --- | --- |
| product-brief, Required | `SKILL.md` Inputs table row 1 | evals 1, 2 |
| design-spec and prototype-report, Conditional | Inputs table row 2 | not separately cased; carried as a conditional row |
| Repository and package manifests, Required when present | Inputs table row 3; phase 1 | evals 2, 3, 4 |
| Primary technical sources, Required for selected API claims | Inputs table row 4; phase 2; `references/version-evidence.md` "What a verified claim records" | eval 4 / ARCH-B-004 |
| architecture-contract or change-request, Conditional | Inputs table row 5; `references/recording-rules.md` amendment paragraph | eval 7 / ARCH-B-007 |
| Consume-only semantics | Inputs table lead-in ("Every one of these is consume-only") | evals 3, 7 |
| Artifact contract: exact revisions, hashes, stable section IDs, decisions, source evidence | `references/recording-rules.md` "The artifact envelope", "Stable IDs", "Digests, and the order that keeps them true" | evals 1, 7 |
| A proposed source cannot become an accepted production constraint by being copied downstream | `SKILL.md` phase 4; `references/recording-rules.md` "Decisions versus proposals" | eval 3 |
| For an established project, reuse valid current artifacts rather than replaying every earlier phase | `SKILL.md` phase 1 closing paragraph | eval 3 |
| Execution contract: every session has an owner and fence; concurrent writers use distinct worktrees and branches | `SKILL.md` "When something is missing or a check cannot run", collision bullet; `references/recording-rules.md` "When no session record exists" | eval 6 / ARCH-B-006 |
| Session template records the authority-selected assignment; a worker-authored ID is not ownership | `references/recording-rules.md` "When no session record exists" | eval 6 |

## Workflow and phase exits

| Phase | Where it is carried | Exit condition carried |
| --- | --- | --- |
| 1. Inventory | `SKILL.md` "## 1. Inventory" | "Exit when the existing decisions are listed with where you observed each one, and the evidence gaps are listed as gaps" |
| 2. Resolve | `SKILL.md` "## 2. Resolve" | "Exit when each architectural choice carries either a reason with its evidence, or an explicit open question with the observation that would settle it" |
| 3. Specify | `SKILL.md` "## 3. Specify" | "Exit when every decision, rule, contract and capability has an ID, a requirement reference, a decision state, and either evidence or a recorded gap - and no required field still holds a template placeholder" |
| 4. Adopt and hand off | `SKILL.md` "## 4. Adopt and hand off" | "Exit when the adopted revision is recorded and delivered to the policy owner, and no claim of mechanical enforcement is made that lacks both a supported adapter and observed evidence" |
| Phases are not CLI subcommands | `SKILL.md` "What this skill owns and does not own"; `references/framework-context.md` closing line of the command table | - |
| Only documented, implemented DevForge commands may be named | `SKILL.md` "External checks and what they prove"; `references/framework-context.md` command table | - |
| On interruption, preserve the phase and evidence; resume by rechecking identities and the assignment | Both halves carried, in two places. **Phase-and-evidence preservation, and the resume trigger:** `SKILL.md` "When something is missing or a check cannot run", sixth bullet - added by CHG-001 in repair pass 1. **Identity recheck:** `references/recording-rules.md` "Resolving an upstream reference" and "When no session record exists", which carry it as unconditional pre-write rules. *Revision 1 of this row claimed full coverage from those `recording-rules.md` sections alone. The independent scaffold review (F-001, MINOR) demonstrated by exhaustive grep that they carry the identity-recheck half only, carry preservation not at all, and frame neither as a resume path - so a resumed session had no trigger to consult them. The original row is preserved in this sentence rather than deleted.* | eval 7 |

## Outputs and standardized templates

| Requirement | Where it is carried |
| --- | --- |
| architecture-contract, ID prefix ARCH | `SKILL.md` phase 3; `references/recording-rules.md` "Numbering and destinations" and "Stable IDs" |
| Required content: versioned decisions, approved stack, source tree, interface rules, security/operating requirements, test policy, expertise needs | `assets/architecture-contract.md` (byte-identical template, placeholders intact); `SKILL.md` phase 3 |
| Template `architecture-contract.md` | Copied to `assets/architecture-contract.md`, digest `38b4ec73...`, derivation recorded |
| Consumer coverage: plan; project-expert-creator; evaluate-expert; develop; review; change | Partially carried. `SKILL.md` phase 4 names plan, project-expert-creator, develop and review as the usual consumers; the description names change as the owner of upgrade proposals. **`devforge-evaluate-expert` is not named in the package** - it consumes an expert package rather than the contract directly, and naming it in a continuation would risk presenting an uninstalled skill as a next step. Recorded as a deliberate partial, not full coverage. |
| Every result includes a handoff with output identities, observed checks, unresolved decisions, next owner, one copyable task prompt | `SKILL.md` phase 4; `assets/handoff.md` (byte-identical shared template, digest `abc7f8e0...`) |
| Do not read a handoff recommendation as authority for unrelated external actions | `SKILL.md` phase 4; `references/framework-context.md` "Roles that stay separate" |

## Validation and behavioral acceptance

| Acceptance case | Required observation | Package location | Eval case |
| --- | --- | --- | --- |
| Direct activation | Produces a contract mapped to product requirements | `SKILL.md` description direct clause; phases 1-4 | evals id 1, runner `ARCH-B-001`, triggers A2a-A2d |
| Indirect activation | Defines dependency and layout rules with separate enforcement requirements | `SKILL.md` phase 3 enforcement paragraph; `references/framework-context.md` "Recording an enforcement requirement" | evals id 2, runner `ARCH-B-002`, triggers A3a-A3e |
| Existing stack | Preserves the retained decision; EF only as an explicitly requested proposal | `references/version-evidence.md` "An existing stack is a decision already made" | evals id 3, runner `ARCH-B-003` |
| Version uncertainty | Verifies or records uncertainty rather than silently changing versions | `SKILL.md` phase 2; `references/version-evidence.md` "The version you remember is not the version pinned" and "When you cannot verify" | evals id 4, runner `ARCH-B-004` |
| Out of scope | Does not impose a new architecture process | Description near-miss clause; `SKILL.md` "Stopping" | evals id 5, runner `ARCH-B-005`, trigger A13a |
| Common: concurrent writer claims the worktree or branch | Stop dependent writes; report without deleting or resetting | `SKILL.md` collision bullet; `references/recording-rules.md` "When no session record exists" | evals id 6, runner `ARCH-B-006` |
| Common: a relevant upstream revision, skill, base commit or candidate changes | Mark prior evidence stale and route a new check | `SKILL.md` stale bullet; `references/recording-rules.md` "Resolving an upstream reference" | evals id 7, runner `ARCH-B-007` |
| Common: a template placeholder remains in a required field | The result stays a draft and cannot be presented as ready | `SKILL.md` placeholder bullet and phase 3 exit; `references/recording-rules.md` envelope closing paragraph | evals id 8, runner `ARCH-B-008` |
| Common: a requested check cannot execute | Record COULD_NOT_RUN and the actual cause; absence of an error is not PASS | `SKILL.md` "When something is missing or a check cannot run"; `references/framework-context.md` "Result vocabulary"; `references/recording-rules.md` "When a check could not run" | evals id 9, runner `ARCH-B-009` |
| Acceptance requires real outputs from representative requests in each supported terminal, with terminal version, discovery/activation, revisions, assignment and evidence location recorded | Not satisfied. `evals/evals.json` carries `execution_status: NOT_RUN`; the design document and handoff record tiers A, B and C as `NOT_RUN` and behaviour as `NOT_EVALUATED` | - |

## Rework, stopping, and recovery

| Requirement | Where it is carried |
| --- | --- |
| Prototype unresolved choices | `SKILL.md` phase 2 closing paragraph; `references/version-evidence.md` "When you cannot verify" |
| Changes to accepted contracts produce a change request, revised contract and affected-consumer review; they do not overwrite prior accepted evidence | `SKILL.md` "Stopping" closing paragraph; `references/recording-rules.md` amendment paragraph |
| Stop when conflicting adopted rules or unsupported enforcement adapters block the production-readiness claim; a useful draft can still be completed | `SKILL.md` "Stopping", second paragraph |
| Preserve accepted versions and observed failures; no force-unlock, no overwriting another session, no changing external gates, no indefinite retry | `SKILL.md` collision bullet and "What this skill owns and does not own"; `references/recording-rules.md` digest-preservation rule; `references/framework-context.md` "Missing integrations" closing line |
| If the worktree or active run changes, re-establish the baseline and evidence before resuming | `references/recording-rules.md` "Resolving an upstream reference" and "When no session record exists" |
| Report missing observations precisely | `SKILL.md` "When something is missing or a check cannot run"; `references/framework-context.md` "Result vocabulary" |

## Native creator authoring prompt and packaging guidance

| Requirement | Disposition |
| --- | --- |
| Use the available native skill creator with the supplied task | The assignment directed the DevForgeAI builder at `4999f31` instead of the environment's `skill-creator`. Recorded in `authoring-notes.md`. |
| Record the real installation mode and candidate/baseline identities | Installation mode: none. Nothing was installed, exported or bound. Candidate identity: `file-manifest.json`. Baseline: none exists; the tier-B label is `without_skill`. |
| Do not claim implicit activation from a run that explicitly supplied SKILL.md | No activation of any kind is claimed. Tier B in `evals/evals.json` carries an explicit note that it can never evidence discovery or activation. |
| Preserve user scope and existing approval; keep DevForge authority external; respect the assigned worktree; report unavailable checks truthfully | No shared contract, template, roster, manifest, sibling skill or gate was modified. Two sibling worktrees were read only. Unavailable checks are reported as unavailable. |
| Move lengthy conditional procedures into references; keep the trigger description precise; use scripts only for real deterministic operations | Three references carry the conditional detail; description is 1,297 characters; no `scripts/` directory exists. |
| Copy needed templates into the package and use package-relative references; installed skills must not depend on this repository's docs path | Both templates copied to `assets/` byte-identically with derivations recorded; every link in the package is package-relative and resolves; no `docs/mvp` runtime dependency and no developer home path anywhere in the package. |

## Completion handoff

| Requirement | Where it is carried |
| --- | --- |
| Completion means the specified artifacts exist, declared inputs resolve, required observations are recorded, and the next task is explicit | `SKILL.md` "Stopping" |
| A document's accepted status and an external gate's passing result are separate facts | `SKILL.md` phase 4; `references/framework-context.md` "Roles that stay separate"; `references/recording-rules.md` "Decisions versus proposals" |

## Requirements deliberately not carried into the package

| Requirement | Reason |
| --- | --- |
| The specification's own status header and "no callable implementation is supplied" line | Describes the specification document, not the skill's runtime behaviour. |
| The native creator authoring prompt block | An instruction to the author, not content for the authored skill. Its dispositions are in this file. |
| Managed-runtime phase context, checkpoints and hook callbacks | The specification selects no managed operation for SKILL-005, and the assignment says not to copy the brainstorm managed-runtime section unless the spec requires it. Hooks are integration-owner scope. |
| Roster and package-index entries for this skill | Outside the assignment fence; integration-owner work. |
