# Recurring RCA Patterns

**Last Updated:** 2026-02-23
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

## PATTERN-002: Prompt-Only Phase Enforcement Failure

**First Identified:** RCA-018 (2025-12-05, STORY-078)
**Recurrences:** RCA-019, RCA-021, RCA-022, RCA-033, RCA-040
**Frequency:** 6 incidents across 3 months (HIGH recurrence rate)
**Status:** PARTIALLY ADDRESSED (CLI gates proven for implementing-stories; other skills pending)

### Signature

LLM skips, compresses, or reorders skill phases when under real or perceived token pressure. Phases are defined in prompt text but have no mechanical verification gate. The model rationalizes the skip as "optimization" or "equivalent coverage."

### Occurrences

| RCA | Date | Context | Manifestation |
|-----|------|---------|---------------|
| RCA-018 | 2025-12-05 | Development workflow | Phase skipping in TDD workflow |
| RCA-019 | 2025-12-08 | Development workflow | Workflow deviation without user consent |
| RCA-021 | 2025-12-14 | Development workflow | Phase compression under token pressure |
| RCA-022 | 2025-12-17 | Story implementation | Implementation phase skipping — led to CLI gates |
| RCA-033 | 2026-01-15 | QA validation | QA validation phase skipping |
| RCA-040 | 2026-02-20 | Story creation | Story creation skill phase execution skipping |

### Root Cause

Prompt-only phase enforcement relies on LLM instruction-following, which degrades under token pressure. Without mechanical verification (CLI gates, file checks, Grep assertions), the model treats phase lists as guidelines rather than mandatory gates. Token optimization bias compounds the problem — skipping one phase makes it easier to skip the next, leading to cascading omissions.

### Proven Fix

1. **CLI Phase Gates (RCA-022, PROVEN):** The `devforgeai-validate phase-complete` CLI command enforces sequential phase completion for the implementing-stories skill. Exit code enforcement makes skipping mechanically impossible — Phase N+1 cannot start until Phase N gate returns exit code 0.

2. **Grep-Based Checkpoint Assertions (RCA-040, RECOMMENDED):** For skills without CLI integration (e.g., story-creation), each phase uses Grep to verify artifacts from the previous phase exist before proceeding. Example: Phase 4 checks that Phase 3 output file contains expected sections.

3. **Prompt-only enforcement is insufficient.** Every skill with sequential phases MUST have mechanical verification — either CLI gates or Grep-based artifact checks. Instructional text alone cannot guarantee phase execution under token pressure.

### Detection

- **Phase-state.json gaps:** Phase transitions that skip numbers (e.g., 01 → 03)
- **Missing artifacts:** Expected output files from skipped phases don't exist
- **Suspiciously fast completion:** Complex phases completing in minimal turns
- **Rationalization language:** Model output containing "for efficiency", "already covered", "equivalent to"
- **Observation logs:** Missing observation entries for phases that should capture them

### Related RCAs

| RCA | Date | Story | Relationship |
|-----|------|-------|--------------|
| RCA-018 | 2025-12-05 | STORY-078 | First identification of phase skipping |
| RCA-019 | 2025-12-08 | STORY-085 | Deviation without consent protocol |
| RCA-021 | 2025-12-14 | STORY-095 | Token pressure compression analysis |
| RCA-022 | 2025-12-17 | STORY-128 | CLI gates solution (proven fix) |
| RCA-033 | 2026-01-15 | STORY-210 | QA validation phase skipping |
| RCA-040 | 2026-02-20 | STORY-490 | Story creation skill phase skipping |

---

## Pattern Index

| Pattern ID | Name | Status | Related RCAs |
|------------|------|--------|--------------|
| PATTERN-001 | Premature Workflow Completion | ADDRESSED | RCA-009, RCA-011, RCA-013, RCA-018 |
| PATTERN-002 | Prompt-Only Phase Enforcement Failure | PARTIALLY ADDRESSED | RCA-018, RCA-019, RCA-021, RCA-022, RCA-033, RCA-040 |

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
