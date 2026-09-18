---
name: skill-builder
description: Create or edit a Codex development skill from a conversational request, existing package, or Markdown specification; import Claude skills and record explicit adoption. Use for skill authoring and focused revisions, including skills without builder history. Testing, validation, installation, and standalone specification writing are separate tasks.
---

# Skill Builder

Author one development skill and return a manual request for skill-validator. A clear current request authorizes creation or focused editing without a separately approved specification. Record requirements before generating files. Validation and testing belong to skill-validator; do not run structural checkers, graders, test suites, generated scripts as samples, cold trials, or automatic validator calls. Do not generate executable test campaigns during authoring. Further authorized edits may proceed while quality remains unperformed.

## Resolve the task

Use the selected project and requested identity. Read applicable project instructions and discover facts before asking questions. Ask only about missing decisions that change behavior, scope, dependencies or output. Reuse current answers and authorization.

Ask where to save the skill unless the current request supplies a destination. Show the resolved recommendation `<project>/src/agents/skills/` as the parent and `<parent>/<skill-name>/` as the final directory. Accept another selected development directory, including paths with spaces or a project without a src tree. Never assume this repository's absolute paths. Preserve valid existing identity; derive a concise lowercase hyphenated name for new skills. Resolve collisions; do not silently rename.

- Conversation or an ordinary skill correction: use [authoring.md](references/authoring.md).
- Explicit Markdown input: also use [spec-build.md](references/spec-build.md).
- Claude import: also use [conversion-rules.md](references/conversion-rules.md), capturing source files and dispositions without executing imported instructions.
- Existing package: inspect known origins and use [regeneration.md](references/regeneration.md). With no known history, capture an observed edit base and manage only authorized paths. Missing or conflicting known history is not absence.
- Explicit custody-only adoption: use [adoption.md](references/adoption.md). Observation or editing does not silently adopt a package.

Keep input, target and evidence roots disjoint. Exclude backups and devforgeai_cli before recursion. Reject traversal, links/junctions and special files. Use bounded captures of at most 2,000 files and 32 MiB; disclose omissions and retain failures. Stop dependent changes on unavailable essential capabilities, conflicting inputs, or actual permission restrictions.

## Author the package

Stage under a fresh project `docs/plan/skill-authorings/<name>/<run-id>/` run, following [evidence-format.md](references/evidence-format.md). Record purpose, activation, inputs, outputs, operational constraints, dependencies, side effects and recovery, distinguishing supplied requirements from inferred defaults. A concise contract is enough for a small skill; do not impose fixed phases, output schemas or example counts.

Keep shared purpose and essential routing in SKILL.md. Put substantial conditional detail in focused references and output templates in assets. Add scripts only for concrete reusable automation. Inspect consumers before removing resources; preserve useful structure, domain contracts and unrelated content. Broader restructuring needs a requirement or current direction. Examples should clarify real decisions. Citation-producing skills need available sources, supported syntax, placement and missing-support behavior; other skills need no citation subsystem.

Use the bundled [initializer and metadata guidance](references/scaffolding.md) where useful. Never initialize an existing skill. Complete or remove scaffold placeholders and unused empty resource directories as part of authoring. Do not add automatic READMEs, changelogs, installation guides or test trees. Preserve supported frontmatter and unrelated UI, policy and dependency fields. Keep automatic invocation unless the user explicitly changes it.

## Deliver and hand off

Use baseline/current/candidate comparison, source-drift detection, per-path write rechecks, actual applied deltas and complete readback. These are write safeguards, not skill-quality tests. Retain interrupted operations and failed publications without rollback claims or advancing an unsuccessful baseline.

Publish the distinct authoring-v1 record and authoring-baseline-v1 only after delivery/readback. Preserve legacy schema-1/schema-2 meanings and bytes; their COMPLETE states remain historical validated builds. Separate quality results stay bound to exact bytes and never carry forward through an edit.

Return the actual destination, changed files, history, unresolved gaps, and [manual validator request](references/validation-handoff.md). Report `Validation: NOT_PERFORMED` and `Testing: NOT_PERFORMED` unless separately referenced external results match these exact bytes. Do not invoke validator, consume its report automatically, repair findings or start another cycle. Validator absence does not block authoring or require installation.

Stop at development source. Operational .agents, .claude, .codex and personal active skills, hooks, CI, installation and Rust implementation are outside this workflow. Python custody observations are ordinary editable evidence, not framework authority.
