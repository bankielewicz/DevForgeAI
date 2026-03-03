# ADR-023: Add src/claude/rules/ to Distribution Source Tree

## Status

Accepted

## Date

2026-02-23

## Context

DevForgeAI maintains a dual-path architecture (Source: devforgeai/specs/context/source-tree.md, lines 558-578): operational folders (`.claude/`, `devforgeai/`) and distribution source (`src/`). The `src/claude/` directory mirrors `.claude/` for installer deployment to external projects.

Currently, `src/claude/` includes `agents/`, `commands/`, `skills/`, `memory/`, and `scripts/` — but omits `rules/`. The operational `.claude/rules/` directory exists with subdirectories `core/`, `workflow/`, `security/`, and `conditional/`, containing framework rules that govern development workflows.

STORY-491 (EPIC-084: Structured Diagnostic Capabilities) creates a new rule file at `src/claude/rules/workflow/diagnosis-before-fix.md`. This path is not documented in source-tree.md, causing a context validation failure.

Rules are framework components equivalent to skills, agents, and commands — they should be distributable to external projects via the installer.

## Decision

Add `src/claude/rules/` to the `src/` distribution structure in source-tree.md, mirroring the operational `.claude/rules/` directory structure:

```
src/claude/rules/
├── core/            # Critical rules (always apply)
├── workflow/        # TDD and story lifecycle rules
├── security/        # Security and compliance rules
└── conditional/     # Path-specific rules (activate by file type)
```

## Rationale

1. **Consistency with dual-path architecture**: Every other `.claude/` subdirectory (`agents/`, `commands/`, `skills/`, `memory/`, `scripts/`) has a corresponding `src/claude/` mirror. Rules are the only omission.
2. **Installer completeness**: External projects using DevForgeAI should receive framework rules (commit validation, TDD workflow, diagnosis-before-fix) alongside skills and agents.
3. **Unblocks STORY-491**: The diagnosis-before-fix rule needs a valid `src/` path for development and testing per source-tree.md's mandate that changes are made in `src/` (source of truth).

### Alternatives Rejected

- **Keep rules only in operational `.claude/rules/`**: Rejected because it breaks the dual-path pattern and means rules cannot be distributed to external projects.
- **Move the rule to a different location**: Rejected because `.claude/rules/workflow/` is the canonical location for workflow rules.

## Consequences

### Positive

- STORY-491 and future stories can reference `src/claude/rules/` paths without validation failures
- Installer can deploy rules to external projects
- Complete parity between `src/claude/` and `.claude/` structures

### Negative

- Slightly increases `src/` directory size (rules are small Markdown files)

### Neutral

- Existing operational `.claude/rules/` files unchanged
- No impact on existing skills, agents, or commands

## Implementation Notes

- Update `devforgeai/specs/context/source-tree.md` to add `src/claude/rules/` with subdirectories
- Source copies of rules placed in `src/claude/rules/` following same structure as `.claude/rules/`
- Installer deploy logic should include `rules/` alongside `agents/`, `commands/`, `skills/`

## Enforcement

- Context validation (`/validate-stories`) will now accept `src/claude/rules/` paths
- Source-tree.md serves as the canonical reference for valid paths

## References

- STORY-491: Create Root-Cause-Diagnosis Skill, Diagnostic-Analyst Subagent, and Diagnosis-Before-Fix Rule
- EPIC-084: Structured Diagnostic Capabilities
- source-tree.md: Dual-Location Architecture (lines 558-578)
- source-tree.md: `src/` Distribution Source (lines 805-836)

---

**ADR Template Version:** 1.0
**Created:** 2026-02-23
**Author:** DevForgeAI AI Agent
**Epic:** EPIC-084
