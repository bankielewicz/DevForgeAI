# DevForgeAI MVP authoring specifications

Status: DRAFT design package, revision 2, refreshed 2026-09-05 UTC. Requested deliverables: an MVP roster and provenance diagram, a specification for each skill, and standardized upstream/downstream documents. This package supplies those authoring artifacts. It creates no new callable skills and changes no gates.

Start with the [roster and Mermaid provenance diagram](roster.md), then the [use-case inventory](use-case-inventory.md). The [artifact contract](artifact-contract.md) defines common document fields and provenance; the [execution contract](execution-contract.md) defines native sessions, worktrees, authority, hooks, CI, and recovery.

The [skill authoring contract](skill-authoring-contract.md) governs provider sources, package contents, and separate discovery, output-quality, and installed-resource evaluation. Existing draft instructions require alignment with this revision.

## Skill specifications

| ID | Specification | Templates | Current implementation |
| --- | --- | --- | --- |
| SKILL-001 | [devforge-brainstorm](specifications/skill-001-devforge-brainstorm.md) | [output templates](templates/devforge-brainstorm/) | Draft instructions exist; expanded behavior unevaluated |
| SKILL-002 | [devforge-define-product](specifications/skill-002-devforge-define-product.md) | [output templates](templates/devforge-define-product/) | Proposed; not implemented |
| SKILL-003 | [devforge-design](specifications/skill-003-devforge-design.md) | [output templates](templates/devforge-design/) | Proposed; not implemented |
| SKILL-004 | [devforge-prototype](specifications/skill-004-devforge-prototype.md) | [output templates](templates/devforge-prototype/) | Proposed; not implemented |
| SKILL-005 | [devforge-architect](specifications/skill-005-devforge-architect.md) | [output templates](templates/devforge-architect/) | Proposed; not implemented |
| SKILL-006 | [devforge-plan](specifications/skill-006-devforge-plan.md) | [output templates](templates/devforge-plan/) | Proposed; not implemented |
| SKILL-007 | [devforge-project-expert-creator](specifications/skill-007-devforge-project-expert-creator.md) | [output templates](templates/devforge-project-expert-creator/) | Draft instructions exist; expanded behavior unevaluated |
| SKILL-008 | [devforge-evaluate-expert](specifications/skill-008-devforge-evaluate-expert.md) | [output templates](templates/devforge-evaluate-expert/) | Proposed; not implemented |
| SKILL-009 | [devforge-develop](specifications/skill-009-devforge-develop.md) | [output templates](templates/devforge-develop/) | Draft instructions exist; expanded behavior unevaluated |
| SKILL-010 | [devforge-review](specifications/skill-010-devforge-review.md) | [output templates](templates/devforge-review/) | Draft instructions exist; expanded behavior unevaluated |
| SKILL-011 | [devforge-release](specifications/skill-011-devforge-release.md) | [output templates](templates/devforge-release/) | Proposed; not implemented |
| SKILL-012 | [devforge-change](specifications/skill-012-devforge-change.md) | [output templates](templates/devforge-change/) | Proposed; not implemented |

There are 12 specifications, 17 skill-output templates, 2 shared workflow templates, and 4 additional skill-authoring templates. Each specification includes a user-centered use case, inputs, phases with exits, outputs, provenance, behavioral acceptance cases, rework, and a native creator authoring prompt.

## Readiness facts

| Area | Current evidence / requirement |
| --- | --- |
| Existing POC | Four draft skills, example experts, a Rust gate/installer fixture implementation; see [POC scope](../POC.md). |
| This authoring package | Documents and templates only; no semantic model evaluation is implied. |
| Native terminal acceptance | Required independently for Codex and Claude; currently not demonstrated for this full roster. |
| Worktree control | Required for concurrent writers; operator-managed Git worktrees are the baseline; no automated lease service is claimed. |
| Structural artifact validation | This package defines the contract; the existing POC does not yet validate this complete envelope or artifact graph. |
| Outbox and report transport | Explicit outbox would need implementation; operator-saved terminal reports are the baseline when worker writes are restricted. |
| Hooks | Optional future adapters; actual provider coverage/trust/error behavior must be tested. |
| CI | Deterministic DevForge CI is in scope; the API-key-based Codex Action path is deferred. |

## Use with native authoring tools

Use a native skill creator to implement one specification at a time. Copy only that skill's needed templates/references into the plugin package and make resource links package-relative. Use the plugin creator for distribution metadata and the actual installation flow. Test the installed package rather than assuming the source folder is what the model sees.

Longer role-specific guidance belongs in supporting references; instructions should emphasize the result and consequential boundaries. The [prompting and provider source notes](research/source-notes.md) record how the user-supplied documentation shaped this package.

## You are here

| Work | Owner | State | Next action | Completion evidence |
| --- | --- | --- | --- | --- |
| Roster, skill specifications, and templates | Framework author | Draft package | Review the linked use-case and artifact boundaries | Accepted design revision, if adopted |
| First native skill proof | Assigned Claude/Codex authors and evaluators | Brainstorm draft migrated; evaluation pending | Align SKILL-001 with the authoring contract, then run C/B/A per provider | Actual installation, native discovery, outputs, and scoped reports |
| Governed story proof | Worker plus external operator | Partial POC machinery exists | Apply SKILL-009/010 to the exact evaluated context | Matching RED/GREEN and QA evidence |
| Concurrent sessions and integration | External operator plus workers | Specified, not certified | Exercise separate worktrees and a combined candidate | Ownership, collision, and integration evidence |

Ordered continuation: align and evaluate SKILL-001 in separate assigned provider worktrees; implement SKILL-002 consuming its ledger; then build project-expert creation/evaluation and exercise one governed story before expanding the roster.

## Validation history

The [initial report](validation/20260904-initial-authoring.json) covers only its original file hashes. Its full document bytes were preserved by the migration owner before edits. The [current structural report](validation.json) records checks against the refreshed package. Neither report establishes native behavior. Consult package-index.json for the provider-specific draft/implementation state.
