# Discovering Problems - Shared Reference Strategy

## Architecture

This skill maintains its own local reference files. Phase files load references via `Read()` paths from the `spec-driven-brainstorming` skill directory.

This follows the same pattern established by `spec-driven-dev`, which reads references from its own skill directory rather than cross-referencing other skills.

**Rationale:**
- Self-contained skill with no cross-skill dependencies
- References can evolve independently of the original brainstorming skill
- Clear ownership and maintenance boundaries

## Reference File Mapping

| Phase File | Loads From |
|------------|------------|
| phase-01-stakeholder-discovery.md | `.claude/skills/spec-driven-brainstorming/references/stakeholder-discovery-workflow.md` |
| phase-02-problem-exploration.md | `.claude/skills/spec-driven-brainstorming/references/problem-exploration-workflow.md` |
| phase-03-opportunity-mapping.md | `.claude/skills/spec-driven-brainstorming/references/opportunity-mapping-workflow.md` |
| phase-04-constraint-discovery.md | `.claude/skills/spec-driven-brainstorming/references/constraint-discovery-workflow.md` |
| phase-05-hypothesis-formation.md | `.claude/skills/spec-driven-brainstorming/references/hypothesis-formation-workflow.md` |
| phase-06-prioritization.md | `.claude/skills/spec-driven-brainstorming/references/prioritization-workflow.md` |
| phase-07-synthesis.md | `.claude/skills/spec-driven-brainstorming/references/handoff-synthesis-workflow.md` |

## Shared References (All Phases)

| Reference | Purpose |
|-----------|---------|
| `.claude/skills/spec-driven-brainstorming/references/session-checkpoint-workflow.md` | Checkpoint/resume logic |
| `.claude/skills/spec-driven-brainstorming/references/user-interaction-patterns.md` | AskUserQuestion templates |
| `.claude/skills/spec-driven-brainstorming/references/error-handling.md` | Error recovery and degradation |
| `.claude/skills/spec-driven-brainstorming/references/output-templates.md` | Document formatting (Phase 07) |

## Template Assets (Phase 07)

| Template | Purpose |
|----------|---------|
| `.claude/skills/spec-driven-brainstorming/assets/templates/brainstorm-template.md` | Main output document |
| `.claude/skills/spec-driven-brainstorming/assets/templates/readme-brainstorm-template.md` | Optional README artifact |
| `.claude/skills/spec-driven-brainstorming/assets/templates/claude-md-template.md` | Optional CLAUDE.md artifact |
| `.claude/skills/spec-driven-brainstorming/assets/templates/gitignore-template.md` | Optional .gitignore artifact |

## Anti-Skip Enforcement Note

Per-phase reference loading is a deliberate anti-skip mechanism. Each phase file contains a `## Reference Loading [MANDATORY]` section that loads the specific reference file for that phase.

**Consolidated loading is explicitly forbidden.** Loading all references at once enables token optimization bias, which is the root cause of phase skipping. Each phase loads only what it needs, when it needs it.

(Source: `.claude/skills/spec-driven-qa/references/README.md` - "Consolidated loading enables token optimization bias")
