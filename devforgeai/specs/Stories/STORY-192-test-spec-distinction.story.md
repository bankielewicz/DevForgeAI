---
id: STORY-192
title: Distinguish Test Specifications from Executable Tests
type: refactor
epic: EPIC-033
priority: LOW
points: 1
status: Backlog
created: 2025-12-31
source: STORY-155 framework enhancement analysis
---

# STORY-192: Distinguish Test Specifications from Executable Tests

## User Story

**As a** DevForgeAI developer,
**I want** test-automator to distinguish test types,
**So that** "75 tests passing" isn't misleading for specification files.

## Background

For Slash Commands, "tests" are specification documents, not executable tests.

## Acceptance Criteria

### AC-1: Implementation Type Detected
**Given** test-automator invocation
**Then** detects Slash Command vs Code implementation

### AC-2: Slash Commands Get Specifications
**Then** Slash Commands generate "Test Specification Document"

### AC-3: Code Gets Executable Tests
**Then** Code implementations generate "Executable unit tests"

### AC-4: Terminology Updated
**Then** Phase 02: "Test Specification Generated" for Slash Commands

### AC-5: Output Naming Distinguished
**Then** TEST-SPECIFICATION.md vs test_*.py

## Technical Specification

### Files to Modify
- `.claude/agents/test-automator.md`
- `.claude/skills/devforgeai-development/phases/phase-02-test-first.md`

### Implementation
```markdown
## Test Type Detection

IF implementation_type == "Slash Command (.md)":
  Generate: Test Specification Document (not executable)
  Output: TEST-SPECIFICATION.md

IF implementation_type == "Code (Python/JS/etc)":
  Generate: Executable unit tests
  Output: test_*.py or *.test.js
```

## Definition of Done

- [ ] Implementation type detection added
- [ ] Slash Commands generate specifications
- [ ] Code generates executable tests
- [ ] Phase 02 terminology updated
- [ ] Output naming distinguished

## Effort Estimate
- **Points:** 1
- **Estimated Hours:** 45 minutes

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | claude/opus | Story created from STORY-155 framework enhancement |
