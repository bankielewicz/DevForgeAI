# ADR-030: Source Tree Update for managing-finances Skill

**Status:** Accepted
**Date:** 2026-03-03
**Decision Makers:** Bryan (Product Owner)
**Epic:** EPIC-077 (Financial Planning & Modeling)

## Context

EPIC-077 introduces a new `managing-finances` skill with progressive disclosure references, a `/financial-model` command, and a `financial-modeler` subagent. The validate-stories audit (STORY-549 through STORY-553) identified that the following paths are not registered in source-tree.md:

- `src/claude/skills/managing-finances/` (skill directory with references)
- `src/claude/commands/financial-model.md` (thin delegator command)
- `src/claude/agents/financial-modeler.md` (projection subagent)
- `devforgeai/specs/business/financial/` (output directory for projections.md, pricing-model.md, funding-strategy.md)

Source-tree.md is an immutable context file requiring ADR approval for changes (ADR-021).

## Decision

Update `devforgeai/specs/context/source-tree.md` to:

1. Add `managing-finances/` skill entry under `.claude/skills/` with its references directory structure
2. Add `financial-model.md` command entry under `.claude/commands/`
3. Add `financial-modeler.md` subagent entry under `.claude/agents/`
4. Add EPIC-077 to the business planning outputs allowlist
5. Bump version from 5.0 to 5.1

## Rationale

- All framework skills must be registered in source-tree.md for discoverability and constraint enforcement
- STORY-549 through STORY-553 all reference `src/claude/skills/managing-finances/` paths
- STORY-551 references `src/claude/commands/financial-model.md` and `src/claude/agents/financial-modeler.md`
- The skill follows the standard pattern: `SKILL.md` + `references/` subdirectory with progressive disclosure
- Pattern is consistent with ADR-028 (advising-legal, marketing-business) and ADR-029 (operating-business)

## Consequences

### Positive

- Source-tree.md accurately reflects all EPIC-077 components
- All 5 EPIC-077 stories (STORY-549 through STORY-553) pass source-tree context validation
- No impact on existing skills, commands, or subagents

### Negative

- None
