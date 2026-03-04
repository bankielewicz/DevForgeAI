# ADR-029: Source Tree Update for operating-business Skill

**Status:** Accepted
**Date:** 2026-03-03
**Decision Makers:** Bryan (Product Owner)
**Epic:** EPIC-078 (Operations & Launch)

## Context

EPIC-078 introduces a new `operating-business` skill with progressive disclosure references and an `/ops-plan` command. The custody chain audit (stories-554-558) identified that `src/claude/skills/operating-business/` and `src/claude/commands/ops-plan.md` are not registered in source-tree.md, which is an immutable context file requiring ADR approval for changes.

The `devforgeai/specs/business/operations/` output directory is already documented in source-tree.md, so no change is needed there.

## Decision

Update `devforgeai/specs/context/source-tree.md` to:

1. Add `operating-business/` skill entry under `.claude/skills/` with its references directory structure
2. Add `ops-plan.md` command entry under `.claude/commands/`
3. Update the skill count comment to reflect the new total

## Rationale

- All framework skills must be registered in source-tree.md for discoverability and constraint enforcement
- STORY-554 through STORY-558 all reference `src/claude/skills/operating-business/` paths
- STORY-556 references `src/claude/commands/ops-plan.md`
- The skill follows the standard pattern: `SKILL.md` + `references/` subdirectory
- Pattern is consistent with ADR-028 (advising-legal skill, researching-market skill)

## Consequences

- Source-tree.md accurately reflects the new skill and command
- All 5 EPIC-078 stories pass source-tree context validation
- No impact on existing skills or commands
