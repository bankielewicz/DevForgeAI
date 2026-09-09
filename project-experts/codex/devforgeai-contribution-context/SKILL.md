---
name: devforgeai-contribution-context
description: Recover selected records, authority and next steps when starting or resuming a DevForgeAI contribution, or prepare its checkpoint handoff. Use for contribution context recovery and transfer, not ordinary implementation with complete context or final semantic acceptance.
---

# DevForgeAI contribution context

Recover the bounded task from shared records, identify the next permitted action, and return control to the calling workflow. DevForgeAI's intended identity is adaptive and spec-driven; its POC and draft capabilities require scoped evidence. This skill does not establish production expertise, perform the contribution, integrate Git changes, or launch evaluation.

## Select the mode and assignment

Use the caller's task locator and selected project/authority roots, including still-applicable prior authorization. A usable assignment can suffice without an incoming handoff. Do not search for a more permissive owner or root.

- **Orient/resume:** starting, resuming, or checking readiness ordinarily returns concise context in-session. No outbox or new HANDOFF is required. Reuse unchanged records without writes.
- **Checkpoint/transfer:** an explicit checkpoint/transfer request, pause needing durable recovery, ownership release, or governing workflow's required closeout calls for a saved handoff. After recovery, read [checkpoint guidance](references/checkpoint.md).

Establish the recovery task separately from the underlying contribution; identify provider, assigned role, actual owner, assignment state, worktree, branch/base and fences. A Codex provider does not imply architect authority. For workers, select their assigned provider source/package and protect shared, peer and companion paths. For an architect, inspect relevant worker assignments, distinct candidates and integration dependencies, without inheriting worker-private reasoning.

If assignment facts are missing or contradictory, expose the specific gap. An accepted-looking label, historic producer, latest timestamp or suggested continuation does not grant ownership. Conversely, an observably authorized bootstrap task is not invalid solely because SESSION metadata is absent: retain its real authorization, collision observations and unknown fields without inventing a session or base.

## Resolve only the needed context

Read selected rules, decisions, task excerpts and necessary dependencies. For each consumed reference, match its artifact/project identity where supplied, revision, selected store and locator, full SHA-256 and relevant section IDs/headings against actual bytes. Use the selected preserved revision when newer worktree bytes conflict; identify the difference and affected continuation without silently adopting the newer version. Do not invent missing identity fields.

Carry valid prior delegation with its scope and current applicability; a fresh request need not repeat it. Where authority is absent, expired, revoked or unresolved, stop the dependent action. Follow supplied in-scope references to decisions, assignments, packages, candidate manifests, findings and receipts. Exclude unrelated history, credentials and peer-private deliberations.

If a required record is inaccessible, retain the known expected locator/digest, the failed resolution and the facts left unverified. A similarly named accessible file is not a substitute. Unknown required records are not automatically NOT_APPLICABLE. Ask for only the consequential missing information; independently authorized recovery/reporting may continue.

## Reconstruct state and return one continuation

Keep four things distinct: context recovered, underlying task state, recorded check outcomes, and independent acceptance. Bind observations to exact candidate/export/run identities. Attribute a reported PASS to its producer; reconcile obvious conflicts with referenced findings or receipts without regrading transcripts or certifying implementation semantics. Preserve open finding IDs and historical failures, including incomplete delivery. A later receipt does not repair a frozen earlier trial.

Use only PASS, FAIL, NOT_RUN, COULD_NOT_RUN and NOT_APPLICABLE for check outcomes, with scope and cause. Readiness for a specific next action is a separate assessment. Successful recovery may correctly find the contribution blocked; failed or unavailable underlying checks retain their own outcomes. Source hashes and package presence do not establish installed identity, activation, behavior or acceptance. Disclose missing required expertise; do not invent a package or require nonessential expertise.

For **orient/resume**, return the identified task/role, selected record references, readiness or material gaps, and **one next action** with owner (or unresolved-owner gap), prerequisites, output location if needed, and completion evidence. A concise response may reference a pinned manifest rather than repeat every digest; an abbreviated digest is never an exact receipt. No new files merely to restate unchanged facts. Return control so the caller can continue already authorized work without another permission round. This response does not waive another workflow's required closeout.

For **checkpoint/transfer**, use the linked checkpoint guidance and the authorized output path. Do not invent an outbox if none is permitted. Recovery itself grants no target-write, assignment, integration, policy-change or external-message permission.

For maintenance only, [derivation metadata](references/derivation.json) identifies the selected source basis and template refresh triggers. Mutable owners, task IDs, current outcomes and manifests belong in supplied records, not this skill.
