---
id: STORY-155
title: RCA Document Parsing
type: feature
epic: EPIC-032
priority: Medium
points: 5
depends_on: []
status: Backlog
created: 2025-12-25
---

# STORY-155: RCA Document Parsing

## User Story

**As a** DevForgeAI automation engineer,
**I want** to parse RCA markdown documents and extract structured recommendation data with priority levels, effort estimates, and success criteria,
**So that** I can automatically convert high-priority recommendations into executable development stories without manual transcription.

## Acceptance Criteria

### AC#1: Parse RCA Frontmatter and Extract Metadata

**Given** an RCA markdown file exists at `devforgeai/RCA/RCA-NNN-*.md` with YAML frontmatter
**When** the parser reads the file and extracts frontmatter between opening and closing `---` markers
**Then** the parser returns a structured object containing: id, title, date, severity (CRITICAL/HIGH/MEDIUM/LOW), status, and reporter fields

### AC#2: Extract Recommendations with Priority Levels

**Given** an RCA file contains multiple recommendations under section headers (e.g., `### REC-N: PRIORITY - Title`)
**When** the parser scans the markdown body and identifies all recommendation sections
**Then** the parser extracts each recommendation as: id (REC-N), priority, title, description, and returns them in document order

### AC#3: Extract Effort Estimates

**Given** a recommendation section contains an effort estimate (e.g., `**Effort Estimate:** X hours` or `**Effort Estimate:** Y story points`)
**When** the parser identifies the effort field
**Then** the parser returns effort_hours (integer) and effort_points (integer, optional), converting story points to hours using 1 point = 4 hours

### AC#4: Extract Success Criteria

**Given** a recommendation section contains a `**Success Criteria:**` subsection with checklist items
**When** the parser identifies success criteria blocks
**Then** the parser extracts all success criteria items as a list and associates them with the parent recommendation

### AC#5: Filter Recommendations by Effort Threshold

**Given** a complete RCA document has been parsed with all recommendations extracted
**When** the caller invokes the parser with a filter parameter `effort_threshold_hours: 2`
**Then** the parser returns only recommendations where effort_hours >= threshold, sorted by priority (CRITICAL first, then HIGH, MEDIUM, LOW)

## Technical Specification

```yaml
technical_specification:
  version: "2.0"
  components:
    - type: Service
      name: RCAParser
      path: .claude/commands/create-stories-from-rca.md
      description: Parse RCA markdown files and extract structured recommendation data
      dependencies:
        - Read tool (file access)
        - Regex patterns (markdown parsing)
      test_requirement: Parser extracts all recommendations from valid RCA file with correct metadata

    - type: DataModel
      name: RCADocument
      description: Structured representation of parsed RCA file
      fields:
        - name: id
          type: string
          format: "RCA-NNN"
          required: true
        - name: title
          type: string
          required: true
        - name: date
          type: date
          format: "YYYY-MM-DD"
          required: true
        - name: severity
          type: enum
          values: [CRITICAL, HIGH, MEDIUM, LOW]
          required: true
        - name: status
          type: enum
          values: [OPEN, IN_PROGRESS, RESOLVED]
          required: true
        - name: recommendations
          type: array
          items: Recommendation
          required: true
      test_requirement: Data model validates all required fields and rejects invalid formats

    - type: DataModel
      name: Recommendation
      description: Individual recommendation extracted from RCA
      fields:
        - name: id
          type: string
          format: "REC-N"
          required: true
        - name: priority
          type: enum
          values: [CRITICAL, HIGH, MEDIUM, LOW]
          required: true
        - name: title
          type: string
          required: true
        - name: description
          type: string
          required: true
        - name: effort_hours
          type: integer
          minimum: 1
          required: false
        - name: effort_points
          type: integer
          minimum: 1
          required: false
        - name: success_criteria
          type: array
          items: string
          required: false
      test_requirement: Recommendation model captures all fields from RCA recommendation sections

  business_rules:
    - id: BR-001
      name: Effort Threshold Filter
      description: Only recommendations with effort >= threshold are returned
      test_requirement: Filter with threshold=2 excludes recommendations with effort <2 hours

    - id: BR-002
      name: Priority Sorting
      description: Results sorted by priority (CRITICAL > HIGH > MEDIUM > LOW)
      test_requirement: Recommendations returned in priority order within each RCA

    - id: BR-003
      name: Story Point Conversion
      description: Convert story points to hours using 1 point = 4 hours
      test_requirement: "5 points" converts to 20 hours for threshold comparison

  non_functional_requirements:
    - category: Performance
      requirement: Parse single RCA file in <500ms
      metric: execution_time < 500ms
      test_requirement: Parse 10KB RCA file completes in under 500ms

    - category: Reliability
      requirement: Graceful degradation on malformed sections
      metric: No exceptions on missing optional fields
      test_requirement: Parser handles RCA with missing effort field without error

    - category: Maintainability
      requirement: Parser implemented in command markdown (no external code)
      metric: Zero external dependencies
      test_requirement: Parser works with only Claude Code native tools
```

## Edge Cases

1. **Missing frontmatter:** RCA file has no YAML frontmatter. Parser extracts ID from filename and logs warning.

2. **No recommendations:** RCA file exists but contains no `### REC-N:` sections. Parser returns empty recommendations array.

3. **Missing effort estimate:** Recommendation has no `**Effort Estimate:**` field. Parser returns null for effort_hours.

4. **Malformed priority:** Priority value is not valid enum. Parser defaults to MEDIUM and logs warning.

5. **Multiple RCA files:** Directory contains multiple RCA files. Parser processes specified file only.

6. **Special characters in title:** Recommendation title contains markdown formatting. Parser extracts clean text.

## Non-Functional Requirements

- **Performance:** Parse time <500ms per RCA file
- **Reliability:** Graceful degradation on malformed sections (partial results with warnings)
- **Maintainability:** Parser logic in command markdown, no external dependencies
- **Security:** Read-only file access, no code execution from RCA content

## Definition of Done

### Implementation
- [ ] RCA frontmatter parsing implemented
- [ ] Recommendation section extraction implemented
- [ ] Priority extraction with validation implemented
- [ ] Effort estimate extraction with conversion implemented
- [ ] Success criteria extraction implemented
- [ ] Effort threshold filtering implemented
- [ ] Priority sorting implemented

### Quality
- [ ] All 5 acceptance criteria have passing tests
- [ ] Edge cases handled with graceful degradation
- [ ] No console errors or warnings in normal operation
- [ ] Code follows DevForgeAI coding standards

### Testing
- [ ] Unit tests for frontmatter parsing
- [ ] Unit tests for recommendation extraction
- [ ] Unit tests for filtering and sorting
- [ ] Integration test with real RCA file (RCA-022)

### Documentation
- [ ] Parser logic documented in command file
- [ ] Usage examples in command help text

## AC Verification Checklist

### AC#1: Parse RCA Frontmatter
- [ ] Read RCA file from devforgeai/RCA/
- [ ] Extract YAML between --- markers
- [ ] Parse id, title, date, severity, status fields
- [ ] Handle missing optional fields gracefully

### AC#2: Extract Recommendations
- [ ] Identify ### REC-N: sections
- [ ] Extract priority from header
- [ ] Extract title from header
- [ ] Extract description from body

### AC#3: Extract Effort Estimates
- [ ] Find **Effort Estimate:** line
- [ ] Parse hours value
- [ ] Parse story points if present
- [ ] Convert points to hours (1pt = 4hrs)

### AC#4: Extract Success Criteria
- [ ] Find **Success Criteria:** subsection
- [ ] Parse checklist items (- [ ] format)
- [ ] Associate with parent recommendation

### AC#5: Filter by Effort Threshold
- [ ] Accept threshold parameter
- [ ] Filter recommendations by effort_hours >= threshold
- [ ] Sort by priority (CRITICAL > HIGH > MEDIUM > LOW)
- [ ] Return filtered and sorted list

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-25 | DevForgeAI | Story created via /create-missing-stories batch mode |
