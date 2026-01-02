---
id: STORY-177
title: Add Atomic Story Status Update Protocol to QA Skill
type: bugfix
epic: EPIC-033
priority: HIGH
points: 2
status: Backlog
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

- [ ] YAML frontmatter update first
- [ ] Grep verification added
- [ ] Conditional history append
- [ ] Rollback mechanism implemented
- [ ] Protocol documented in Step 3.4
- [ ] All 6 ACs have tests

## Effort Estimate
- **Points:** 2
- **Estimated Hours:** 45 minutes

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | claude/opus | Story created from STORY-153 framework enhancement |
