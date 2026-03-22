# ADR-033: Source Tree Update for marketing-business Skill

**Status:** Accepted
**Date:** 2026-03-04
**Decision Makers:** Bryan (Product Owner)
**Epic:** EPIC-075 (Marketing & Customer Acquisition)

## Context

STORY-539 (Go-to-Market Strategy Builder) created a new skill directory:

1. `src/claude/skills/marketing-business/references/go-to-market-framework.md`
2. `src/claude/skills/marketing-business/references/channel-selection-matrix.md`

These paths are not registered in `devforgeai/specs/context/source-tree.md`. QA validation flagged two HIGH violations:
- Skill directory `marketing-business` not registered in source-tree.md
- Missing `SKILL.md` for marketing-business skill directory

## Decision

Update `devforgeai/specs/context/source-tree.md` to:

1. Add `marketing-business/` skill entry in the skills section (alphabetical order, after `implementing-stories/`)
2. Update version from 5.3 to 5.4

Create `src/claude/skills/marketing-business/SKILL.md` with proper YAML frontmatter.

## Rationale

- All skills must be registered in source-tree.md for constraint enforcement
- All skill directories must contain a SKILL.md per source-tree.md rules
- STORY-539 created these files as part of EPIC-075 marketing capabilities

## Consequences

- Source-tree.md accurately reflects the new skill
- QA re-validation will pass structure violation checks
- Future EPIC-075 stories can reference marketing-business skill without validation warnings

## References

- STORY-539: Go-to-Market Strategy Builder
- EPIC-075: Marketing & Customer Acquisition
- Source: devforgeai/specs/context/source-tree.md (rules at lines 660-676)
