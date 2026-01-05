---
id: STORY-177
title: Add Atomic Story Status Update Protocol to QA Skill
type: bugfix
epic: EPIC-033
priority: HIGH
points: 2
status: Dev Complete
created: 2025-12-31
source: STORY-153 framework enhancement analysis
---

# STORY-177: Add Atomic Story Status Update Protocol to QA Skill

## User Story

**As a** DevForgeAI framework user,
**I want** the QA skill to use an atomic update protocol for story status changes,
**So that** YAML frontmatter and Status History table remain consistent.

## Background

Light QA can update Status History table without updating YAML frontmatter `status:` field, creating divergence.

## Acceptance Criteria

### AC#1: YAML Frontmatter Updated First
**Given** QA skill updates status
**Then** YAML frontmatter `status:` field updated FIRST

### AC#2: Verification with Grep
**Given** frontmatter updated
**Then** Grep verification confirms new status before proceeding

### AC#3: History Entry After Verification
**Given** verification succeeds
**Then** Status History entry appended ONLY AFTER verification

### AC#4: Single Edit Sequence
**Given** both updates required
**Then** both in single Edit sequence when possible

### AC#5: Rollback on Failure
**Given** verification fails
**Then** rollback restores original value, no history append

### AC#6: Protocol Documented
**Given** implementation complete
**Then** documented in Step 3.4 of SKILL.md

## Technical Specification

### Files to Modify
- `.claude/skills/devforgeai-qa/SKILL.md`

### Atomic Update Protocol
```
1. Read current status from YAML frontmatter
2. Edit YAML frontmatter status field
3. Grep verify new status in frontmatter
4. Edit append history entry (only if step 3 passes)
5. Rollback: Restore original if verification fails
```

## Definition of Done

- [x] YAML frontmatter update first
- [x] Grep verification added
- [x] Conditional history append
- [x] Rollback mechanism implemented
- [x] Protocol documented in Step 3.4
- [x] All 6 ACs have tests

## Implementation Notes

- [x] YAML frontmatter update first - Completed: Step 2 in atomic protocol ensures YAML status edited first
- [x] Grep verification added - Completed: Step 3 uses Grep to verify status after Edit
- [x] Conditional history append - Completed: Step 4 only executes after Step 3 verification passes
- [x] Rollback mechanism implemented - Completed: Step 5 restores original status if verification fails
- [x] Protocol documented in Step 3.4 - Completed: Full 5-step protocol with code examples in SKILL.md
- [x] All 6 ACs have tests - Completed: tests/STORY-177/ contains 7 test files (31 assertions total)

## Effort Estimate
- **Points:** 2
- **Estimated Hours:** 45 minutes

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | claude/opus | Story created from STORY-153 framework enhancement |
| 2026-01-05 | claude/test-automator | Red (Phase 02): Generated 7 test files for 6 ACs |
| 2026-01-05 | claude/backend-architect | Green (Phase 03): Implemented atomic protocol in SKILL.md |
| 2026-01-05 | claude/opus | Dev Complete (Phase 07): All DoD items completed |
