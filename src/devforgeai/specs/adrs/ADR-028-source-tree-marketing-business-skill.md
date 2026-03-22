# ADR-028: Source Tree Update for Marketing-Business Skill

**Date:** 2026-03-03
**Status:** Accepted
**Acceptance Date:** 2026-03-03
**Deciders:** Solo Developer, DevForgeAI Framework
**Tags:** source-tree, skills, commands, EPIC-075, STORY-539, STORY-540, STORY-541, STORY-542, STORY-543

## Context

EPIC-075 (Marketing & Customer Acquisition) introduces a new `marketing-business` skill and `/marketing-plan` command. Five stories (STORY-539 through STORY-543) reference the following paths that are not yet documented in `devforgeai/specs/context/source-tree.md`:

1. **Skill path:** `src/claude/skills/marketing-business/` (SKILL.md + references/)
2. **Command path:** `src/claude/commands/marketing-plan.md`
3. **Output directory:** `devforgeai/specs/business/marketing/` (go-to-market.md, positioning.md)

Custody chain audit `devforgeai/qa/audit/custody-chain-audit-stories-539-543.md` finding F-002 (MEDIUM) identified this gap as a pre-sprint blocker: `/dev` Phase 01 Pre-Flight validates all file paths against source-tree.md and will HALT if these paths are missing.

## Decision

1. **Add `marketing/`** subdirectory under `devforgeai/specs/business/` in the source tree listing.
2. **Add `marketing-plan.md`** to the `.claude/commands/` listing.
3. **Update EPIC references** in the business outputs rule to include EPIC-075.
4. **Bump version** to 4.7.

## Rationale

1. Source-tree.md must document all framework components to prevent Phase 01 Pre-Flight failures and QA anti-pattern-scanner structure violation false positives.
2. The `marketing-business` skill follows existing patterns: skill in `src/claude/skills/`, command in `src/claude/commands/`, outputs in `devforgeai/specs/business/`.
3. The `marketing/` output directory parallels existing `market-research/`, `legal/`, and `operations/` subdirectories under `devforgeai/specs/business/`.

## Consequences

### Positive
- `/dev` Phase 01 Pre-Flight will not halt on EPIC-075 story file paths
- QA anti-pattern-scanner will recognize marketing-business skill files as documented
- Clear output location for marketing artifacts (go-to-market.md, positioning.md)

### Negative
- None significant — additive change only

### Risks
- None — follows established patterns for skill/command/output registration

## Alternatives Considered

1. **Skip source-tree update, use --ignore flag** — Rejected. Bypassing Pre-Flight undermines the purpose of source-tree.md as the canonical file location registry.

## Enforcement

### Context File Updates Required

| File | Change | Type |
|------|--------|------|
| `devforgeai/specs/context/source-tree.md` | Add marketing/ directory, marketing-plan.md command, update EPIC refs, bump version | Update |

### Affected Stories

| Story | Impact |
|-------|--------|
| STORY-539 | Unblocked: `src/claude/skills/marketing-business/references/go-to-market-framework.md` now documented |
| STORY-540 | Unblocked: `src/claude/skills/marketing-business/references/positioning-strategy.md` now documented |
| STORY-541 | Unblocked: `src/claude/commands/marketing-plan.md` and `src/claude/skills/marketing-business/SKILL.md` now documented |
| STORY-542 | Unblocked: `src/claude/skills/marketing-business/references/customer-discovery-workflow.md` now documented |
| STORY-543 | Unblocked: `src/claude/skills/marketing-business/references/content-channel-strategy.md` now documented |

### New Artifacts

| Artifact | Location |
|----------|----------|
| ADR-028 | `devforgeai/specs/adrs/ADR-028-source-tree-marketing-business-skill.md` |
