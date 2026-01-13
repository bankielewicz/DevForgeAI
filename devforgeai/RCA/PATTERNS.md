# Recurring RCA Patterns

**Last Updated:** 2025-01-13
**Version:** 1.0

This document catalogs recurring failure patterns identified through Root Cause Analysis (RCA). Each pattern includes detection indicators and prevention strategies.

---

## PATTERN-001: Premature Workflow Completion

**First Identified:** RCA-009 (2025-11-14, STORY-027)
**Recurrences:** RCA-013 (2025-11-22, STORY-057), RCA-018 (2025-12-05, STORY-078)
**Frequency:** 3 incidents in 21 days (HIGH recurrence rate)
**Status:** ADDRESSED (CLI gates + self-check implemented)

### Behavior

Claude completes early phases (01-05) of TDD workflow but skips late phases (06-10), which are administrative/validation phases, declaring workflow "COMPLETE" despite:
- TodoWrite list showing phases as "pending"
- DoD completion <100%
- Story status not updated
- No git commit of story file

### Root Cause

Missing enforcement for administrative phases. Claude's execution model prioritizes "implementation complete" signals (tests passing, code written) over "administrative complete" signals (DoD updated, story committed), leading to systematic early termination.

### Detection Indicators

**For User:**
- Workflow displays "COMPLETE" but todo list shows pending phases
- Story file not updated (status still "Backlog" or "In Development")
- No git commit containing story file
- DoD items not marked [x]

**For Claude (self-detection):**
- About to display "Workflow Complete" banner
- TodoWrite shows <10 phases completed
- Run self-check before declaring complete (STORY-204)

### Prevention Strategy

**Implemented Solutions:**
1. CLI validation gates (`devforgeai-validate phase-complete`) - STORY-203
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
