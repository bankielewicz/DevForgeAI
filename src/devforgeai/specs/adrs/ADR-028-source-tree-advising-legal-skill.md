# ADR-028: Source Tree Update for advising-legal Skill

**Status:** Accepted
**Date:** 2026-03-03
**Decision Makers:** Bryan (Product Owner)
**Epic:** EPIC-076 (Legal & Compliance)

## Context

EPIC-076 introduces a new `advising-legal` skill with progressive disclosure references and a `/legal-check` command. The custody chain audit (stories-544-546-547) identified that `src/claude/skills/advising-legal/` is not registered in source-tree.md, which is an immutable context file requiring ADR approval for changes.

The `devforgeai/specs/business/legal/` output directory is already documented in source-tree.md (line 405), so no change is needed there.

## Decision

Update `devforgeai/specs/context/source-tree.md` to:

1. Add `advising-legal/` skill entry under `.claude/skills/` with its references directory structure
2. Update the skill count from "20 skills" to "21 skills" in the `.claude/skills/` comment

## Rationale

- All framework skills must be registered in source-tree.md for discoverability and constraint enforcement
- STORY-544, STORY-546, and STORY-547 all reference this skill path
- The skill follows the standard pattern: `SKILL.md` + `references/` subdirectory

## Consequences

- Source-tree.md accurately reflects the new skill
- `src/claude/skills/` comment updated to "21 skills" (matching the new count after `advising-legal` addition)
- Story implementations for EPIC-076 can proceed without source-tree violations

## References

- Custody chain audit: `devforgeai/qa/audit/custody-chain-audit-stories-544-546-547.md` (Finding F-001)
- EPIC-076: `devforgeai/specs/Epics/EPIC-076-legal-compliance.epic.md`
- ADR-017: Gerund-Object Naming Convention (skill naming)
