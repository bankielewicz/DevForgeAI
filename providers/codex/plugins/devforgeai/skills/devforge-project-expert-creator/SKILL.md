---
name: devforge-project-expert-creator
description: "Design, create, or enhance Codex workflow skills and project experts through focused Q&A, existing-skill discovery, phased authoring, and a DevForgeAI specification; apply frozen evaluator findings to canonical source. Authors candidates and prepared handoffs; does not test or validate skills."
---

# DevForge Project Expert Creator

Turn a concrete workflow need or supplied evaluator findings into a populated specification and a new skill, focused enhancement, or justified reuse. This is the independent Codex implementation of SKILL-007. Same-named Claude packages are separate provider implementations.

## Scope and authority

Author instructions and supporting resources only. Do not run target skills, helper scripts, tests, validators, linters, compilation, or evaluations, directly or through another agent. Collect cases for a separate evaluator. Source reads, file identities and successful writes are authoring observations, not validation evidence. A target skill may itself perform validation when that is its requested purpose.

Write only the assigned canonical provider/skill source. Preserve accepted decisions, IDs, classifications, API versions, prior evidence, invocation policy and unrelated behavior. Installed copies and exports are generated artifacts. Do not edit shared contracts, sibling gates, the roster, another skill or provider to make a candidate pass. Reconcile source or ownership drift before affected writes.

Rust in DevForge CLI owns authoritative phase state, transitions, gates, validators, mutation permission and acceptance. Mandatory Python evaluation JSONL runners and deterministic graders produce evidence only; Rust verifies their identities, format and coverage before acceptance. Hook proposals are design only: no executable handlers, active configuration, installation, activation or enforcement claims. Missing runtime support limits the dependent claim; file organization does not implement a gate.

## Phase map and progressive loading

All five identities and their required actions remain **Enforced**. These are stable workflow names, not CLI commands. Read only the current phase and references needed for its work. Each phase links to its continuation; do not load all phases or references upfront. On resumption, recover the saved phase, assignment and source identities, then load that phase. Required work still applies when detail is deferred.

| Phase | Required actions | Instructions |
| --- | --- | --- |
| Intake | Recover task, authority, provider, source identities and write fence. | [01 Intake](phases/01-intake.md) |
| Selection | Discover expertise; justify reuse, enhancement or creation; resolve collisions. | [02 Selection](phases/02-selection.md) |
| Design | Focused Q&A; preserve constraints/API versions; record design, classifications and hook proposals. | [03 Design](phases/03-design.md) |
| Authoring | Author only the canonical candidate and preserve unrelated behavior and grounded references. | [04 Authoring](phases/04-authoring.md) |
| PreparedTransfer | Save candidate/specification/change record and actionable evaluator handoff with limits. | [05 PreparedTransfer](phases/05-prepared-transfer.md) |

Resolve linked files relative to the containing file, rooted in the loaded skill package; resolve project artifact/output locations separately. Framework workflows use their task and governing contracts; project experts use applicable architecture, code and pinned APIs. Do not require unrelated application architecture for a framework refactor.

## Invocation, completion and stops

Preserve normal implicit discovery. The user initiates the receiving skill and relevant commands; this creator never evaluates, binds or installs its target, invokes the evaluator automatically, or grants acceptance. Read [manual operation](references/manual-operation.md) when command ownership, artifact mapping or evaluation/adoption policy matters. Managed v1 IDs remain skill-builder and skill-validator; the package name admits no new adapter. Load [managed authoring](references/managed-authoring.md) only for an actual managed assignment or affected recovery question. No advance/resume/complete fallback, scheduler or automatic repair loop.

Stop affected work for missing material input/classification, conflicting authority, source drift or a write-fence collision; retain evidence and continue independent authorized authoring. Unknown identities or runtime capabilities remain unknown with a reason. Do not reopen settled decisions or add an approval ceremony.

At completion, transfer or recovery, save the full evidence and prepared handoff before using the [completion summary](assets/completion-summary.md). Report actual authoring outcome, useful result, primary artifact/handoff links, material decision or blocker, and one immediate action with its owner. **Validation status: Not performed.** **Hook status: Design only** when applicable. Prepared transfer is not receiver execution, native activation, installation or acceptance.
