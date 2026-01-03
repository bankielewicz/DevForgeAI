---
id: STORY-226
title: Analyze Command Sequence Patterns for Workflow Discovery
type: feature
epic: EPIC-034
sprint: Backlog
status: Backlog
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
- [ ] N-gram extraction logic in session-miner
- [ ] Success rate calculation
- [ ] Report formatting in insights skill

### Quality
- [ ] All 3 acceptance criteria verified
- [ ] Patterns are actionable (not obvious)

---

## Implementation Notes

*Pending implementation*

---

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2025-01-02 | claude/story-creation-skill | Created | Story created for EPIC-034 Feature 3 | STORY-226-command-sequence-patterns.story.md |
