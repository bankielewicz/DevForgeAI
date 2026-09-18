# Current user authorization (verbatim task)

Use $skill-builder to author the standalone Codex development skill named dev from the specification below. This is an authorized skill-authoring task; proceed through publication and readback without stopping at a plan.

PROJECT
C:\Projects\DevForgeAI

BUILDER
C:\Projects\DevForgeAI\.agents\skills\skill-builder\SKILL.md

SPECIFICATION
C:\Projects\DevForgeAI\docs\specs\dev-skill-spec.md

Expected specification SHA-256:
b9783ca08d86fa734c89ce76623ff6c45b2640781d3955f16ea54ea659c7b265

DESTINATION
C:\Projects\DevForgeAI\src\agents\skills\dev

1. Establish context

Read applicable AGENTS.md instructions, the selected skill-builder instructions and relevant references, and the entire specification.

Use the explicit specification path. Do not rely on automatic name-based lookup, previous conversations, or memory.

Verify the specification hash before authoring. If it differs, report the discrepancy and stop dependent writes; do not restore or silently substitute another version.

Inspect the destination before writing. If it contains existing work, preserve it and inspect its identity and provenance. Do not initialize over an existing package, silently rename the skill, or overwrite unrelated content.

The destination and skill name are already selected; do not ask for them again.

2. Author the skill

Implement all DEV-001 through DEV-026 requirements faithfully.

The resulting dev skill must:
- Work in a cold Codex CLI session with explicitly selected specifications and project instructions.
- Support single and dependent multi-document specifications.
- Derive language, architecture, technology stack, source layout, commands, quality thresholds, and platforms from runtime project inputs.
- Resolve constitutional decisions from existing evidence and ask about material gaps.
- Inspect existing functionality before introducing potentially duplicate implementations.
- Execute authorized product development through red, green, refactor, integration, and QA.
- Retain traceability, real execution evidence, checkpoints, and honest delivery status.
- Resume safely after interruption or changed inputs.
- Operate without a mandatory DevForgeAI installation, project binding, index service, MCP server, or plugin.

Keep the skill named dev. Do not embed these authoring paths, the authoring project's Rust choice, its numeric thresholds, application specification names, or expected CLI details as universal runtime defaults.

Keep specification section 1.1 and its concrete authoring handoff out of generated runtime instructions.

Use a concise SKILL.md, focused references, and useful templates. Add helper scripts only where the specification justifies concrete reusable automation. Do not add unused scaffolds, automatic READMEs, changelogs, plugin manifests, operational bindings, or executable evaluation campaigns.

3. Preserve responsibility boundaries

This session authors the skill package. The resulting dev skill is allowed and required to implement products and execute their tests.

Do not copy skill-builder's authoring-only testing restrictions into dev as a prohibition against product TDD or QA.

Conversely, do not execute skill-quality checks, graders, test suites, generated scripts as samples, or cold-session trials during this authoring task. Do not invoke $skill-validator automatically.

The skill's evaluated build requires a separately owned, digest-bound Python JSONL runner, deterministic graders, fixtures, expected results, schema, and manifest. Identify that mandatory validation bundle in the handoff. Do not omit the obligation or claim that authoring alone satisfies it.

Python supplies evaluation evidence. Compiled Rust retains DevForgeAI framework authority; no generated helper may replace its gates or acceptance decisions.

4. Publish with custody evidence

Follow skill-builder's authoring and evidence contracts:
- Use a fresh, disjoint authoring run directory.
- Capture specification identity and requirements before generation.
- Preserve existing content and interrupted attempts.
- Perform source-drift and per-path write rechecks.
- Record actual applied changes and complete delivered-file readback.
- Publish authoring-v1 and authoring-baseline-v1 only after successful delivery/readback.
- Return a manual validation-request packet bound to the exact delivered package.

These custody checks are required write safeguards, not permission to run a skill-validation campaign.

5. Stop at the authorized boundary

Do not build the application described by any example specification.
Do not change the governing specification or skill-builder.
Do not install the skill or modify operational .agents, .claude, .codex, hooks, CI, startup settings, or personal active skills.
Do not create, publish, or install the future plugin.
Do not claim that $DevForgeAI:dev invocation is supported without separate host verification.

If a material contradiction or missing capability prevents faithful authoring, identify the affected requirement and minimum resolution needed. Continue independent authorized work where possible; do not invent requirements or produce ceremonial completion.

FINAL RESPONSE

Return:
- Actual package destination and changed files.
- Authoring record, baseline, and package digest.
- Requirement-to-resource mapping.
- Unresolved gaps and any mandatory evaluation artifacts still pending.
- Exact manual validator packet path and digest.
- A copyable next-step prompt for separately invoking $skill-validator.

Report:
Validation: NOT_PERFORMED
Testing: NOT_PERFORMED
Installation: NOT_PERFORMED
Framework acceptance: NOT_EVALUATED

Distinguish completed authoring from the still-unperformed evaluation and installation.

