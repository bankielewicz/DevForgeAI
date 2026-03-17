# Discovering Problems - Shared Reference Strategy

## Architecture

This skill shares reference files with the original `brainstorming` skill rather than duplicating them. Phase files load references via `Read()` paths from the existing brainstorming skill directory.

This follows the same pattern established by `spec-driven-dev`, which reads references from `implementing-stories/references/` rather than maintaining copies.

**Rationale:**
- Single source of truth prevents content drift
- Updates to brainstorming references automatically apply to discovering-problems
- Reduces maintenance burden and file count

## Reference File Mapping

| Phase File | Loads From |
|------------|------------|
| phase-01-stakeholder-discovery.md | `.claude/skills/brainstorming/references/stakeholder-discovery-workflow.md` |
| phase-02-problem-exploration.md | `.claude/skills/brainstorming/references/problem-exploration-workflow.md` |
| phase-03-opportunity-mapping.md | `.claude/skills/brainstorming/references/opportunity-mapping-workflow.md` |
| phase-04-constraint-discovery.md | `.claude/skills/brainstorming/references/constraint-discovery-workflow.md` |
| phase-05-hypothesis-formation.md | `.claude/skills/brainstorming/references/hypothesis-formation-workflow.md` |
| phase-06-prioritization.md | `.claude/skills/brainstorming/references/prioritization-workflow.md` |
| phase-07-synthesis.md | `.claude/skills/brainstorming/references/handoff-synthesis-workflow.md` |

## Shared References (All Phases)

| Reference | Purpose |
|-----------|---------|
| `.claude/skills/brainstorming/references/session-checkpoint-workflow.md` | Checkpoint/resume logic |
| `.claude/skills/brainstorming/references/user-interaction-patterns.md` | AskUserQuestion templates |
| `.claude/skills/brainstorming/references/error-handling.md` | Error recovery and degradation |
| `.claude/skills/brainstorming/references/output-templates.md` | Document formatting (Phase 07) |

## Template Assets (Phase 07)

| Template | Purpose |
|----------|---------|
| `.claude/skills/brainstorming/assets/templates/brainstorm-template.md` | Main output document |
| `.claude/skills/brainstorming/assets/templates/readme-brainstorm-template.md` | Optional README artifact |
| `.claude/skills/brainstorming/assets/templates/claude-md-template.md` | Optional CLAUDE.md artifact |
| `.claude/skills/brainstorming/assets/templates/gitignore-template.md` | Optional .gitignore artifact |

## Anti-Skip Enforcement Note

Per-phase reference loading is a deliberate anti-skip mechanism. Each phase file contains a `## Reference Loading [MANDATORY]` section that loads the specific reference file for that phase.

**Consolidated loading is explicitly forbidden.** Loading all references at once enables token optimization bias, which is the root cause of phase skipping. Each phase loads only what it needs, when it needs it.

(Source: `.claude/skills/spec-driven-qa/references/README.md` - "Consolidated loading enables token optimization bias")
