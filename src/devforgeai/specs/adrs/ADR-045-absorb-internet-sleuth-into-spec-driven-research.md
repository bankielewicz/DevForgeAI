# ADR-045: Absorb Internet-Sleuth-Integration into Spec-Driven-Research

## Status

**Accepted** (2026-03-20)

## Context

The `internet-sleuth-integration` skill directory (`.claude/skills/internet-sleuth-integration/`) contains 6 reference/asset files used by the `internet-sleuth` subagent via progressive disclosure. However, it has no `SKILL.md` entry point — making it an incomplete skill that cannot be invoked standalone.

The `spec-driven-research` skill (invoked via `/research`) already delegates to the `internet-sleuth` subagent in Phase 02. The reference files in `internet-sleuth-integration` serve the subagent regardless of which skill triggers it (ideation, architecture, or research).

Maintaining a separate incomplete skill directory creates:
- Orphaned skill folder listed as "INCOMPLETE" in skills-reference.md
- Confusion about where research references live
- Empty `src/` mirror path (files never mirrored)
- Unnecessary entry in source-tree.md

## Decision

Absorb all 6 files from `internet-sleuth-integration/` into `spec-driven-research/` under a new `references/sleuth-methodology/` subdirectory (5 reference files) and `assets/templates/` (1 template, renamed).

File mapping:
- `internet-sleuth-integration/references/research-principles.md` -> `spec-driven-research/references/sleuth-methodology/research-principles.md`
- `internet-sleuth-integration/references/discovery-mode-methodology.md` -> `spec-driven-research/references/sleuth-methodology/discovery-mode-methodology.md`
- `internet-sleuth-integration/references/repository-archaeology-guide.md` -> `spec-driven-research/references/sleuth-methodology/repository-archaeology-guide.md`
- `internet-sleuth-integration/references/competitive-analysis-patterns.md` -> `spec-driven-research/references/sleuth-methodology/competitive-analysis-patterns.md`
- `internet-sleuth-integration/references/skill-coordination-patterns.md` -> `spec-driven-research/references/sleuth-methodology/skill-coordination-patterns.md`
- `internet-sleuth-integration/assets/research-report-template.md` -> `spec-driven-research/assets/templates/sleuth-report-template.md`

Update all path references in:
- `internet-sleuth` subagent (12 Read() paths)
- `skills-reference.md` (remove incomplete entry)
- `source-tree.md` (remove old entry)

Delete the empty `internet-sleuth-integration/` directory.

## Consequences

**Positive:**
- Eliminates orphaned incomplete skill directory
- Centralizes all research assets under one skill
- Cleaner source-tree.md and skills-reference.md
- The `internet-sleuth` subagent continues to function identically (only paths change)

**Negative:**
- Requires updating 12 path references in the internet-sleuth subagent
- Test files referencing old paths need updating
- Historical stories (STORY-035, STORY-036) reference old paths (acceptable — they're archived)

**Neutral:**
- spec-driven-ideation, spec-driven-architecture, spec-driven-brainstorming need NO changes (they reference the subagent by name, not by file path)
- The `internet-sleuth` subagent itself is NOT being removed or modified functionally
