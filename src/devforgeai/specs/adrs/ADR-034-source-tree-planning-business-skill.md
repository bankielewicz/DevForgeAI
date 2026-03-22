# ADR-034: Source Tree Update for planning-business Skill

**Status:** Accepted
**Date:** 2026-03-04
**Decision Makers:** Bryan (Product Owner)
**Epic:** EPIC-073 (Business Planning & Viability)

## Context

STORY-531 (Lean Canvas Guided Workflow), STORY-532 (Milestone Planning), and STORY-533 (Business Model Pattern Matching) created a planning-business skill with the following files:

1. `src/claude/skills/planning-business/SKILL.md`
2. `src/claude/skills/planning-business/references/lean-canvas-workflow.md`
3. `src/claude/skills/planning-business/references/milestone-generator.md`
4. `src/claude/skills/planning-business/references/business-model-patterns.md`
5. `src/claude/skills/planning-business/references/viability-scoring.md`

These paths are not registered in `devforgeai/specs/context/source-tree.md`. The QA anti-pattern-scanner flagged this as a HIGH structure violation during STORY-533 deep QA retest.

## Decision

Update `devforgeai/specs/context/source-tree.md` to:

1. Add `planning-business/` skill entry in the skills section (alphabetical order, after `marketing-business/`)
2. List SKILL.md and all 4 reference files
3. Update version from 5.4 to 5.5

## Rationale

- All skills must be registered in source-tree.md for constraint enforcement
- STORY-531/532/533 created these files as part of EPIC-073 business planning capabilities
- Prevents anti-pattern-scanner HIGH violations for stories extending the planning-business skill
- Follows precedent set by ADR-032 (coaching-entrepreneur) and ADR-033 (marketing-business)

## Consequences

- Source-tree.md accurately reflects the planning-business skill
- Future EPIC-073 stories (STORY-534, STORY-535) can reference these paths without validation warnings
- Anti-pattern-scanner structure violation resolved

## References

- STORY-531: Lean Canvas Guided Workflow
- STORY-532: Milestone Planning
- STORY-533: Business Model Pattern Matching
- EPIC-073: Business Planning & Viability
