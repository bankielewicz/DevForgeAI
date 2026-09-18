---
name: skill-builder
description: >
  Authors Claude Code skill packages — create, edit, scaffold, convert, regenerate,
  adopt, or propose a project skill set — and returns a manual assessment request
  instead of testing its own output. Use whenever the user wants to build a new skill,
  fix or extend an existing one, convert a Codex or other-host skill package to Claude
  Code, edit a skill that has no builder history, or recommend a set of skills for a
  project. Also use when the user describes the capability they want without calling it
  a "skill". Testing, validation, installation and standalone specification writing are
  separate tasks that this skill deliberately does not perform.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Bash(python:*)
  - Bash(python3:*)
---

# Skill Builder

Author development skills and return manual assessment requests. A clear current request authorizes creation or focused editing without a separately approved specification. Proposal and update review produce evidence and recommendations only. Record requirements before generating files. Validation and testing belong to a separate independent assessment; do not run structural checkers, graders, test suites, generated scripts as samples, or cold trials. Do not generate executable test campaigns during authoring. Further authorized edits may proceed while quality remains unperformed.

Two of those boundaries are structural rather than asserted, and that distinction matters: `Task` and `Skill` are absent from `allowed-tools`, so this workflow cannot spawn workers or invoke an assessor even if a later instruction asks it to. The Python allowance is wider than the contract — it admits any interpreter command, not only the bundled custody helpers. Treat "only the bundled helpers" as an obligation you keep, not a rule the allowlist enforces.

## Resolve the task

Use the selected project and requested identity. Read applicable project instructions and discover facts before asking questions. Ask only about missing decisions that change behavior, scope, dependencies or output. Reuse current answers and authorization.

Resolve the destination before destination-dependent work, in this order, and carry no baked-in default past the first step that answers:

1. **The current request.** A supplied destination answers the question outright.
2. **The project's own instructions.** Read `CLAUDE.md`, `AGENTS.md` or equivalent for a stated skills location. A project that declares where its skills live has already decided; treat that as policy input, not a suggestion to weigh. Some projects keep authored source in a development tree and install elsewhere — follow what the project says, do not infer a convention from this package's own location.
3. **Observed layout.** Where do this project's existing skills actually live?
4. **Ask,** using `AskUserQuestion`. This is the one decision worth the tool: the options are known and the answer blocks everything downstream. Offer `<project>/.claude/skills/` as the Claude Code convention alongside any development tree discovered in step 3, and say which evidence produced each option.

Show the resolved parent and `<parent>/<skill-name>/` as the final directory. Accept any selected directory, including paths with spaces. Never assume a particular repository layout or absolute path, and never assume the destination that was right in the last project is right in this one. Preserve valid existing identity; derive a concise lowercase hyphenated name for new skills. Resolve collisions; do not silently rename.

The destination is whatever the selected contract's `target_root` names; there is no fixed list of forbidden directories. Prepare requirements and inspect an existing package while waiting for the destination answer.

- Conversation or an ordinary skill correction: use [authoring.md](references/authoring.md).
- Explicit Markdown input: also use [spec-build.md](references/spec-build.md).
- Other-host import, commonly a Codex package: also use [conversion-rules.md](references/conversion-rules.md), capturing source files and dispositions without executing imported instructions.
- Existing package: inspect known origins and use [regeneration.md](references/regeneration.md). With no known history, capture an observed edit base and manage only authorized paths. Missing or conflicting known history is not absence.
- Explicit custody-only adoption: use [adoption.md](references/adoption.md). Observation or editing does not silently adopt a package.
- Project framework recommendation (`propose`), explicitly selected proposal members (`author_set`), or a selected variant against changed core/project inputs (`review_updates`): use [adaptation.md](references/adaptation.md). A combined propose-and-author request may already authorize the unchanged selected members; prepare the concrete proposal first. Do not infer a set from all installed skills.

For adaptive members, load [adaptive-contracts.md](references/adaptive-contracts.md) and [project-binding.md](references/project-binding.md) before staging. Preserve reusable core bytes by authoring a distinctly named variant; ground expertise in actual domain evidence. Adaptive source contains no concrete framework identity or installation root. The generic runtime check precedes product operations; authoring itself needs no installed binding.

Keep input, target and evidence roots disjoint. Exclude backups and devforgeai_cli before recursion. Reject traversal, links/junctions and special files. Use bounded captures of at most 2,000 files and 32 MiB; disclose omissions and retain failures. Stop dependent changes on unavailable essential capabilities, conflicting inputs, or actual permission restrictions.

## Author the package

For create, edit, import and specification builds, prepare the external behavior design using [workflow-design.md](references/workflow-design.md) before staging. Bind the completed design and original requirements in the contract inputs, and pass the same file to `authoring.py begin --design`. For selected adaptive sets, do this per authored member. Record observable completion, output delivery, resource consumers, relevant adverse conditions and supplied execution limits. Missing behavior decisions block dependent work; open questions do not resolve them. Custody-only adoption, proposals and update reviews retain their existing scope.

Stage under a fresh project `docs/plan/skill-authorings/<name>/<run-id>/` run, following [evidence-format.md](references/evidence-format.md). Record purpose, activation, inputs, outputs, operational constraints, dependencies, side effects and recovery, distinguishing supplied requirements from inferred defaults. A concise contract is enough for a small skill; do not impose fixed phases, output schemas or example counts.

Keep shared purpose and essential routing in SKILL.md. Put substantial conditional detail in focused references and output templates in assets. Add scripts only for concrete reusable automation. Inspect consumers before removing resources; preserve useful structure, domain contracts and unrelated content. Broader restructuring needs a requirement or current direction. Examples should clarify real decisions. Citation-producing skills need available sources, supported syntax, placement and missing-support behavior; other skills need no citation subsystem.

Claude Code keeps all host-read metadata in the SKILL.md frontmatter, so authoring the frontmatter is authoring the metadata — there is no separate UI file, and a converted package should not keep one. The description carries the entire trigger: the body is not in context when the host decides whether to load the skill, so "when to use" information belongs in the description or it is invisible. `allowed-tools` is a real capability boundary and therefore the right place to express a constraint that would otherwise be prose asking the model to restrain itself. Read [claude-frontmatter.md](references/claude-frontmatter.md) before writing or editing any frontmatter.

Use the bundled [initializer and metadata guidance](references/scaffolding.md) where useful. Never initialize an existing skill. Complete or remove scaffold placeholders and unused empty resource directories as part of authoring. Do not add automatic READMEs, changelogs, installation guides or test trees. Preserve supported frontmatter and unrelated project-local fields. Keep automatic invocation unless the user explicitly changes it.

## Deliver and hand off

Use baseline/current/candidate comparison, source-drift detection, per-path write rechecks, actual applied deltas and complete readback. These are write safeguards, not skill-quality tests. Retain interrupted operations and failed publications without rollback claims or advancing an unsuccessful baseline.

Publish the distinct authoring-v1 record and authoring-baseline-v1 only after delivery/readback. Preserve legacy schema-1/schema-2 meanings and bytes; their COMPLETE states remain historical validated builds. Separate quality results stay bound to exact bytes and never carry forward through an edit.

Return the actual destination, changed files, history, unresolved gaps, and [manual assessment request](references/validation-handoff.md). Report `Validation: NOT_PERFORMED` and `Testing: NOT_PERFORMED` unless separately referenced external results match these exact bytes. Do not consume an assessment report automatically, repair findings or start another cycle. An assessor's absence does not block authoring or require installation.

Report source action (created, edited or unchanged) separately from AUTHORED/PARTIAL/BLOCKED, with actual publication and design-capture references, outstanding evaluation obligations, next owner and concrete next action. Unchanged source, AUTHORED and delivered handoff do not establish evaluated-build completion. Authored design is distinct from observed behavior; an assessor constructs independent fixtures and oracles from original requirements.

The boundary is the action, not the directory. Writing the package files into the selected destination is authoring, and that destination is normally the project's live skills directory. Everything that makes the skill *operate* is installation and stays outside this workflow: hooks, settings registration, CI wiring, plugin assembly, MCP configuration, personal active-skill folders and Rust implementation. Authoring a package into a skills directory does not authorize configuring the host around it. Python custody observations are ordinary editable evidence, not framework authority.
