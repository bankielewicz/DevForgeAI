---
id: STORY-226
title: Analyze Command Sequence Patterns for Workflow Discovery
type: feature
epic: EPIC-034
sprint: Backlog
status: QA Approved
points: 3
depends_on: ["STORY-225"]
priority: Medium
assigned_to: TBD
created: 2025-01-02
format_version: "2.5"
---

# Story: Analyze Command Sequence Patterns for Workflow Discovery

## Description

**As a** Framework Maintainer,
**I want** to identify high-frequency command sequences,
**so that** I can optimize workflows and create automation opportunities.

## Acceptance Criteria

### AC#1: N-gram Sequence Extraction

**Given** history.jsonl command entries,
**When** analyzing sequences,
**Then** 2-gram and 3-gram command sequences are extracted with frequency counts.

---

### AC#2: Success Rate Correlation

**Given** extracted command sequences,
**When** calculating metrics,
**Then** success rate is computed for each sequence (successful completions / total attempts).

---

### AC#3: Top Patterns Report

**Given** analyzed sequences,
**When** generating report,
**Then** top 10 sequences by frequency are displayed with success rates.

---

## Definition of Done

### Implementation
- [x] N-gram extraction logic in session-miner
- [x] Success rate calculation
- [x] Report formatting in insights skill

### Quality
- [x] All 3 acceptance criteria verified
- [x] Patterns are actionable (not obvious)

---

## Implementation Notes

- [x] N-gram extraction logic in session-miner - Completed: session-miner.md lines 417-540
- [x] Success rate calculation - Completed: session-miner.md lines 453-474
- [x] Report formatting in insights skill - Completed: SKILL.md lines 58-61, 123, 253-260
- Added 2-gram (bigram) and 3-gram (trigram) sliding window extraction
- Tie-breaking for equal frequency: alphabetical order of first command
- Added command-patterns to /insights command VALID_QUERY_TYPES
- Created 12 tests: 6 unit, 2 integration, 4 edge cases
- All tests pass (100% pass rate)

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2025-01-02 | claude/story-creation-skill | Created | Story created for EPIC-034 Feature 3 | STORY-226-command-sequence-patterns.story.md |
| 2026-01-04 | claude/test-automator | Red (Phase 02) | Tests generated | tests/STORY-226/*.sh |
| 2026-01-04 | claude/backend-architect | Green (Phase 03) | N-gram implementation | .claude/agents/session-miner.md |
| 2026-01-04 | claude/refactoring-specialist | Refactor (Phase 04) | Documentation consistency | .claude/skills/devforgeai-insights/SKILL.md |
| 2026-01-04 | claude/opus | DoD (Phase 07) | Status updated to Dev Complete | STORY-226-command-sequence-patterns.story.md |
| 2026-01-04 | claude/qa-result-interpreter | QA Deep | Passed: 100% tests, 0 blocking violations | STORY-226-qa-report.md |
