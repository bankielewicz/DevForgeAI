# DevForgeAI POC

DevForgeAI is an adaptive, spec-driven software engineering framework in development. Use the [adaptive design](docs/mvp/roster.md#adaptive-design) to describe its intended identity while preserving the current POC and draft capability status. Adaptation means selecting relevant workflows and context, creating or refreshing needed expertise, and reevaluating affected work under accepted specifications and recorded authority. Ground capability claims in observed evidence for the relevant scope and provider.

This repository owns conversational workflows, skills, agent definitions, examples, and project expertise. Its companion repository is https://github.com/bankielewicz/DevForge and owns the Rust CLI, policy, tests, and GitHub workflows.

Work from the user's task and applicable skill. Capture brainstorming suggestions as proposals; preserve accepted project decisions and their source revisions. Use project-specific facts and verified library references when authoring expert skills. A provenance binding is not evidence of expert behavior.

When working on this framework or a generated project, do not change sibling DevForge gates or policy to make a candidate pass. Report a contract defect to its owner. Framework maintenance explicitly requested by the user may change framework sources; application work may not silently change its governing framework.

Canonical framework skill sources are provider-specific: providers/claude/plugins/devforgeai/skills and providers/codex/plugins/devforgeai/skills. Work only in the provider and skill named by your assignment. Claude plugin agents are in providers/claude/plugins/devforgeai/agents; Codex subagent templates remain in providers/codex/agents. Per-skill agents/openai.yaml is optional Codex metadata, not a subagent. Installed copies and exported plugins are generated artifacts, never alternative canonical sources.

For skill authoring, read docs/mvp/skill-authoring-contract.md and the relevant specification/templates. Shared contracts and installer integration have one integration owner; report ambiguities rather than changing them from a skill-only assignment. Authored eval inputs live under the skill's evals directory, while run outputs live in the assigned provider evaluation workspace. No package or file-hash check certifies native activation or behavioral quality.

The POC is Linux/WSL2 and local-only. Read docs/POC.md for commands, actual guarantees, and remaining evaluation work.

## Learned behavior: bounded delivery

Apply [keeping delivery bounded](docs/learned-behaviors/bounded-delivery.md) when specifications or validation/integration work expand faster than progress toward the user's outcome. Keep a concrete finish line, accepted requirements, exclusions and total remaining delivery path in the existing plan.

Justify added work with an observed blocker, the requirement it serves, simpler alternatives, expected evidence and bounded cost. Carry settled decisions forward. When a model over-expands the specification, consolidate necessary blockers, defer optional generalization, and narrow its assignment. Request a material scope or funding change only after making the decision concrete; continue unaffected authorized work.

Preserve accepted checks, ownership, budgets and historical results. Guidance cannot activate a proposed Routine policy, bypass Full qualification, or turn a prepared handoff into operational completion. Distinguish justified iteration from recursive review, setup overhead, stale recaps and premature simplification. Reuse the existing plan/report rather than adding a workflow for controlling workflows.
