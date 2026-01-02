---
id: STORY-210
title: Create PATTERNS.md Knowledge Base for Recurring RCA Patterns
type: documentation
epic: EPIC-033
priority: LOW
points: 1
status: Backlog
created: 2025-01-01
source: RCA-018 REC-5
depends_on: []
---

# STORY-210: Create PATTERNS.md Knowledge Base for Recurring RCA Patterns

## User Story

**As a** DevForgeAI maintainer reviewing RCAs,
**I want** a PATTERNS.md file documenting recurring failure patterns,
**So that** I can quickly recognize patterns and apply known solutions.

## Background

RCA-018 is the 3rd RCA documenting premature workflow completion (RCA-009, RCA-013, RCA-018). This recurring pattern should be documented for future reference to enable faster recognition and resolution.

**Source RCA:** `devforgeai/RCA/RCA-018-development-skill-phase-completion-skipping.md`

**Pattern History:**
- RCA-009 (2025-11-14): First identification of phase skipping
- RCA-011 (2025-11-19): Phase 1 Step 4 skipping specifically
- RCA-013 (2025-11-22): Late-phase skipping (4.5-7)
- RCA-018 (2025-12-05): Comprehensive analysis of all missing checkpoints

**Desired State:**
- PATTERNS.md file documents recurring patterns
- Each pattern has detection indicators and prevention strategies
- Cross-references to related RCAs
- Metrics for pattern tracking

## Acceptance Criteria

### AC-1: PATTERNS.md File Created

**Given** the RCA directory structure
**When** PATTERNS.md is created
**Then** it exists at `devforgeai/RCA/PATTERNS.md`

---

### AC-2: Pattern Template Structure

**Given** the PATTERNS.md file
**When** documenting a pattern
**Then** each pattern includes:
- Pattern ID (PATTERN-NNN)
- First identified (RCA reference)
- Recurrences (list of related RCAs)
- Behavior description
- Root cause summary
- Detection indicators (for user and Claude)
- Prevention strategy
- Metrics

---

### AC-3: Premature Workflow Completion Pattern Documented

**Given** the PATTERNS.md file
**When** pattern PATTERN-001 is documented
**Then** it includes:
- Pattern ID: PATTERN-001
- Name: Premature Workflow Completion
- First Identified: RCA-009 (2025-11-14, STORY-027)
- Recurrences: RCA-013, RCA-018
- Behavior: Claude completes early phases but skips late phases
- Root cause: Missing enforcement for administrative phases
- Solution: CLI validation gates + TodoWrite integration + self-check

---

### AC-4: Detection Indicators for Both User and Claude

**Given** the pattern documentation
**When** listing detection indicators
**Then** separate sections exist for:

**For User:**
- Workflow displays "COMPLETE" but todo list shows pending phases
- Story file not updated
- No git commit

**For Claude (self-detection):**
- About to display "Workflow Complete" banner
- TodoWrite shows <10 phases completed
- Run self-check before declaring complete

---

### AC-5: Related RCAs Cross-Referenced

**Given** the pattern documentation
**When** listing related RCAs
**Then** each RCA is linked with relationship description:
```
### Related RCAs

- **RCA-009:** First identification of pattern
- **RCA-011:** Phase 1 specific fix
- **RCA-013:** Late-phase pattern identified
- **RCA-018:** Comprehensive solution
```

## Technical Specification

### Files to Create

| File | Description |
|------|-------------|
| `devforgeai/RCA/PATTERNS.md` | Recurring RCA patterns knowledge base |

### File Location

Per source-tree.md: `devforgeai/RCA/` is the correct location for RCA-related documentation.

### PATTERNS.md Template

```markdown
# Recurring RCA Patterns

**Last Updated:** 2025-01-01
**Version:** 1.0

This document catalogs recurring failure patterns identified through Root Cause Analysis (RCA). Each pattern includes detection indicators and prevention strategies.

---

## PATTERN-001: Premature Workflow Completion

**First Identified:** RCA-009 (2025-11-14, STORY-027)
**Recurrences:** RCA-013 (2025-11-22, STORY-057), RCA-018 (2025-12-05, STORY-078)
**Frequency:** 3 incidents in 21 days (HIGH recurrence rate)
**Status:** ADDRESSED (CLI gates + self-check implemented)

### Behavior

Claude completes implementation phases (01-05) of TDD workflow but skips administrative/validation phases (06-10), declaring workflow "COMPLETE" despite:
- TodoWrite list showing phases as "pending"
- DoD completion <100%
- Story status not updated
- No git commit of story file

### Root Cause

Missing enforcement for late-stage phases. Claude's execution model prioritizes "implementation complete" signals (tests passing, code written) over "administrative complete" signals (DoD updated, story committed), leading to systematic early termination.

### Detection Indicators

**For User:**
- Workflow displays "COMPLETE" but todo list shows pending phases
- Story file not updated (status still "Backlog" or "In Development")
- No git commit containing story file
- DoD items not marked [x]

**For Claude (self-detection):**
- About to display "Workflow Complete" banner
- Run Workflow Completion Self-Check (STORY-204)
- If <10 phases completed → You're about to violate this pattern

### Prevention Strategy

**Implemented Solutions:**
1. CLI validation gates (`devforgeai-validate phase-complete`) - STORY-XXX
2. TodoWrite integration with gates (STORY-203)
3. Workflow Completion Self-Check (STORY-204)
4. Phase Resumption Protocol (STORY-205)

**Monitoring:**
- Track: Count of "workflow incomplete" user reports
- Target: Zero incidents per sprint
- Escalation: If recurs after fix, investigate architectural issue

### Metrics

- **Incident Rate (Pre-Fix):** 3 incidents / 21 days = 1 incident per week
- **Impact:** HIGH (blocks user work, requires intervention)
- **Fix Availability:** CLI gates + self-check implemented
- **Post-Fix Target:** Zero incidents per month

### Related RCAs

| RCA | Date | Story | Relationship |
|-----|------|-------|--------------|
| RCA-009 | 2025-11-14 | STORY-027 | First identification |
| RCA-011 | 2025-11-19 | STORY-044 | Phase 1 Step 4 specific |
| RCA-013 | 2025-11-22 | STORY-057 | Late-phase pattern (4.5-7) |
| RCA-018 | 2025-12-05 | STORY-078 | Comprehensive analysis |

---

## Pattern Index

| Pattern ID | Name | Status | Related RCAs |
|------------|------|--------|--------------|
| PATTERN-001 | Premature Workflow Completion | ADDRESSED | RCA-009, RCA-011, RCA-013, RCA-018 |

---

## Adding New Patterns

When a recurring pattern is identified:

1. **Create pattern entry** with next ID (PATTERN-NNN)
2. **Document behavior** - What specifically happens?
3. **Identify root cause** - Use 5 Whys from RCA
4. **List detection indicators** - For user AND Claude
5. **Define prevention strategy** - With story references
6. **Cross-reference RCAs** - All related documents
7. **Set metrics** - Incident rate, target, monitoring

---

**REMEMBER:** This patterns knowledge base is for the framework itself. Projects using DevForgeAI may have their own patterns documentation for project-specific recurring issues.
```

## Definition of Done

### Implementation
- [ ] PATTERNS.md file created at `devforgeai/RCA/PATTERNS.md`
- [ ] PATTERN-001 (Premature Workflow Completion) documented
- [ ] Detection indicators for user and Claude included
- [ ] Related RCAs cross-referenced
- [ ] Pattern Index section added
- [ ] "Adding New Patterns" guide included

### Testing
- [ ] Verify file location matches source-tree.md
- [ ] Verify all RCA references are accurate
- [ ] Verify story references are correct

### Documentation
- [ ] Update RCA-018 with implementation status

## Effort Estimate

- **Points:** 1
- **Estimated Hours:** 30 minutes
  - Create file with content: 20 minutes
  - Review and verify: 10 minutes

## Related

- **RCA:** RCA-018-development-skill-phase-completion-skipping.md
- **Recommendation:** REC-5 (Add Pattern to RCA Knowledge Base)
- **Related Patterns:** PATTERN-001 (Premature Workflow Completion)

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-01-01 | claude/opus | Story created from RCA-018 REC-5 |
