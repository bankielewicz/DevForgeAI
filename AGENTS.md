# DevForgeAI POC

## Identity and ownership

DevForgeAI is an adaptive, spec-driven software engineering framework in development. Use the [adaptive design](docs/mvp/roster.md#adaptive-design) to describe its intended identity while preserving current POC and draft status. Adaptation selects relevant workflows and context, creates or refreshes needed expertise, and reevaluates affected work under accepted specifications and recorded authority. Ground capability claims in observed evidence for the relevant scope and provider.

This repository owns conversational workflows, skills, agents, examples, and project expertise. Companion [DevForge](https://github.com/bankielewicz/DevForge) owns the Rust CLI, policy, protected runtime, tests, and GitHub workflows. Keep substantive conversational behavior in skills; protected runtime owns mechanical transitions, checks, and receipts.

## Decisions and canonical sources

Work from the user's task and applicable skill. Capture brainstorming suggestions as proposals; preserve human-accepted project decisions and their source revisions. Use project-specific facts and verified library references when authoring expert skills. Provenance does not prove expert behavior.

Do not change sibling DevForge gates or policy to make a candidate pass. Report contract defects to their owner. Explicit framework maintenance may change framework sources; application work cannot silently change its governing framework.

Canonical skill sources are provider-specific: `providers/claude/plugins/devforgeai/skills` and `providers/codex/plugins/devforgeai/skills`. Edit only the assigned provider and skill. Claude plugin agents live in `providers/claude/plugins/devforgeai/agents`; Codex subagent templates remain in `providers/codex/agents`. Per-skill `agents/openai.yaml` is optional Codex metadata, not a subagent. Installed copies and exported plugins are generated, never alternative canonical sources.

For skill authoring, read `docs/mvp/skill-authoring-contract.md` and applicable specifications/templates. Authored eval inputs belong in the skill's `evals` directory; run outputs belong in the assigned provider evaluation workspace.

## Concurrent sessions

At session start, verify repository, worktree, branch, HEAD, write scope, and existing changes. Parallel implementation sessions use separate worktrees and branches with distinct outputs. Shared contracts and installer integration have one integration owner; report ambiguity rather than expanding a skill-only assignment.

Preserve others' changes. Workers must not commit, rebase, reset, or merge a shared checkout; its designated integration owner handles authorized integration. Recheck owned files and required pins before writes and handoff. Unexpected drift stops the affected action. Never silently repin frozen evidence or overwrite concurrent work.

## Verification and completion

Keep authoring, static checks, native activation/behavior, runtime admission, and human acceptance distinct. Package or hash checks do not certify native behavior. Consequential changes require independent review of specified bytes without reviewer edits. Documentation-only edits need content/link/diff review, not native evaluation.

Rust CLI maintenance follows TDD in the companion repository under its guide. Explicit no-execution allocations override general testing instructions.

Apply clocks and deadlines only when allocated; include preparation, waiting, and closeout, and never reset them or fabricate observations. Handoffs identify changes, checks, unresolved work, and the next owner. Exact paths, SHA-256 bindings, and full readback are required when the custody contract specifies them.

The POC is Linux/WSL2 and local-only. Read `docs/POC.md` for commands, actual guarantees, and remaining evaluation work.

## Learned behavior: bounded delivery

Apply [keeping delivery bounded](docs/learned-behaviors/bounded-delivery.md) when specifications or validation/integration work expand faster than progress toward the user's outcome. Keep a concrete finish line, accepted requirements, exclusions and total remaining delivery path in the existing plan.

Justify added work with an observed blocker, the requirement it serves, simpler alternatives, expected evidence and bounded cost. Carry settled decisions forward. When a model over-expands the specification, consolidate necessary blockers, defer optional generalization, and narrow its assignment. Request a material scope or funding change only after making the decision concrete; continue unaffected authorized work.

Preserve accepted checks, ownership, budgets and historical results. Guidance cannot activate a proposed Routine policy, bypass Full qualification, or turn a prepared handoff into operational completion. Distinguish justified iteration from recursive review, setup overhead, stale recaps and premature simplification. Reuse the existing plan/report rather than adding a workflow for controlling workflows.
