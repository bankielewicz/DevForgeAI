---
id: STORY-231
title: Mine Anti-Pattern Occurrences from Sessions
type: feature
epic: EPIC-034
sprint: Backlog
status: Backlog
points: 2
depends_on: ["STORY-229"]
priority: Medium
assigned_to: TBD
created: 2025-01-02
format_version: "2.5"
---

# Story: Mine Anti-Pattern Occurrences from Sessions

## Description

**As a** Framework Analyst,
**I want** to detect usage of framework anti-patterns,
**so that** I can track violation frequency and consequences.

## Acceptance Criteria

### AC#1: Anti-Pattern Matching

**Given** session commands,
**When** matching against anti-patterns.md rules,
**Then** violations are detected: Bash for file ops, assumptions, size violations.

---

### AC#2: Violation Counting

**Given** detected violations,
**When** aggregating,
**Then** count per pattern type is reported.

---

### AC#3: Consequence Tracking

**Given** anti-pattern usage,
**When** analyzing subsequent entries,
**Then** correlation with errors is tracked (did violation cause error?).

---

## Definition of Done

### Implementation
- [ ] Anti-pattern rule matching
- [ ] Violation counting
- [ ] Consequence correlation

### Quality
- [ ] All 3 acceptance criteria verified
- [ ] 100% pattern match coverage

---

## Implementation Notes

*Pending implementation*

---

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2025-01-02 | claude/story-creation-skill | Created | Story created for EPIC-034 Feature 4 | STORY-231-anti-pattern-mining.story.md |
