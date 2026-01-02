---
id: STORY-187
title: Extend Story ID Pattern to Support STORY-1000+
type: bugfix
epic: EPIC-033
priority: LOW
points: 1
status: Backlog
created: 2025-12-31
source: STORY-148 framework enhancement analysis
---

# STORY-187: Extend Story ID Pattern to Support STORY-1000+

## User Story

**As a** DevForgeAI user,
**I want** story IDs to support 4+ digits,
**So that** the framework doesn't break when story count exceeds 999.

## Background

Current pattern `^STORY-\d{3}$` rejects STORY-1000 and higher.

## Acceptance Criteria

### AC-1: Pattern Extended
**Given** phase_state.py
**Then** pattern changed to `^STORY-\d{3,}$`

### AC-2: Existing IDs Still Valid
**Then** STORY-001 through STORY-999 still valid

### AC-3: 4+ Digit IDs Valid
**Then** STORY-1000, STORY-9999, STORY-10000 all valid

### AC-4: Error Message Updated
**Then** error message reflects new pattern

### AC-5: Backward Compatible
**Then** no breaking changes

## Technical Specification

### Files to Modify
- `installer/phase_state.py`

### Implementation
```python
# Line 41: Change from
STORY_ID_PATTERN = re.compile(r"^STORY-\d{3}$")
# To
STORY_ID_PATTERN = re.compile(r"^STORY-\d{3,}$")
```

## Definition of Done

- [ ] Pattern changed to `^STORY-\d{3,}$`
- [ ] STORY-001 to STORY-999 still valid
- [ ] STORY-1000+ now valid
- [ ] Error message updated
- [ ] Unit test for STORY-1000 added

## Effort Estimate
- **Points:** 1
- **Estimated Hours:** 15 minutes

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | claude/opus | Story created from STORY-148 framework enhancement |
