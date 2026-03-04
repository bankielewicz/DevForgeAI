# ADR-031: Source Tree Update for legal-check Command

**Status:** Accepted
**Date:** 2026-03-03
**Decision Makers:** Bryan (Product Owner)
**Epic:** EPIC-076 (Legal & Compliance)

## Context

STORY-546 (`/legal-check Command and Skill Assembly`) defines a new slash command at `src/claude/commands/legal-check.md` that delegates to the `advising-legal` skill. The `/validate-stories` context validation (2026-03-03) flagged this command as missing from source-tree.md's commands directory listing.

ADR-028 authorized the `advising-legal` skill addition to source-tree.md but did not include the corresponding `/legal-check` command entry.

## Decision

Update `devforgeai/specs/context/source-tree.md` to:

1. Add `legal-check.md` entry to the `.claude/commands/` section (alphabetical order, after `import-feedback.md`)
2. Update the command count from "27 commands" to "28 commands" in the section comment

## Rationale

- All slash commands must be registered in source-tree.md for constraint enforcement
- STORY-546 AC#1 references `src/claude/commands/legal-check.md` as the implementation target
- The command follows the thin-invoker pattern: delegates to `advising-legal` skill with zero business logic

## Consequences

- Source-tree.md accurately reflects the new command
- STORY-546 can proceed without source-tree violations
- Command count reflects actual inventory

## References

- STORY-546: `/legal-check Command and Skill Assembly`
- ADR-028: Source Tree Update for advising-legal Skill
- EPIC-076: Legal & Compliance
