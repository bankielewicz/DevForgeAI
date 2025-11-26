---
id: STORY-083
title: Requirements Traceability Matrix Foundation
epic: EPIC-015
sprint: Backlog
status: Backlog
points: 13
priority: Medium
assigned_to: Unassigned
created: 2025-11-25
format_version: "2.1"
---

# Story: Requirements Traceability Matrix Foundation

## Description

**As a** DevForgeAI framework maintainer,
**I want** a data model and parsing infrastructure that can extract and validate relationships between requirements, epics, sprints, and stories,
**so that** I can verify requirements coverage, detect orphaned stories, identify missing linkages, and maintain a reliable traceability matrix across the entire project lifecycle.

## Acceptance Criteria

### AC#1: Epic Frontmatter Parsing

**Given** an epic file exists in `.ai_docs/Epics/` directory
**When** the parsing infrastructure processes the epic file
**Then** it extracts:
- `epic_id` field (format: EPIC-NNN) from YAML frontmatter or inline metadata
- `title` field from frontmatter
- Features section content (text between `## Features` and next `##` header)
- Stories table content (text between `## Stories` and next `##` header or EOF)
**And** stores the extracted data in a structured format (JSON file or associative array)

---

### AC#2: Story Epic Reference Parsing

**Given** a story file exists in `.ai_docs/Stories/` directory
**When** the parsing infrastructure processes the story file
**Then** it extracts:
- `story_id` from filename pattern (STORY-NNN-slug.story.md)
- `epic:` field value from YAML frontmatter (line starting with `epic:`)
- Story title from `title:` field in frontmatter
**And** handles edge cases:
- `epic: None` (standalone story, no epic linkage)
- `epic: EPIC-NNN` (linked to specific epic)
- Missing `epic:` field (should be flagged as incomplete metadata)

---

### AC#3: Relationship Data Structure

**Given** parsed epic and story data exists
**When** the data model is populated
**Then** it creates a queryable structure containing:
- `epics`: Map of epic_id to {title, features_count, story_ids[], file_path}
- `stories`: Map of story_id to {title, epic_id, status, file_path}
- `orphaned_stories`: List of story_ids with no valid epic reference
- `unlinked_epics`: List of epic_ids with no stories
**And** the structure is persisted to `.devforgeai/traceability/requirements-matrix.json`

---

### AC#4: Epic Reference Validation

**Given** a story references an epic via `epic: EPIC-NNN`
**When** validation runs against the requirements matrix
**Then** it verifies:
- The referenced epic file exists in `.ai_docs/Epics/`
- The epic_id matches an entry in the epics data structure
- Bidirectional consistency: story appears in epic's Stories section (if present)
**And** reports validation failures with specific error messages:
- "Story STORY-XXX references non-existent epic EPIC-YYY"
- "Epic EPIC-XXX Stories section missing STORY-YYY (story references this epic)"

---

### AC#5: Orphaned Story Detection

**Given** the requirements matrix is populated
**When** orphan detection runs
**Then** it identifies stories where:
- `epic:` field is missing entirely (incomplete metadata)
- `epic: None` (intentionally standalone - not an error, but tracked)
- `epic: EPIC-NNN` where EPIC-NNN does not exist (broken reference)
**And** categorizes results:
- `intentionally_standalone`: Stories with `epic: None`
- `broken_references`: Stories referencing non-existent epics
- `missing_metadata`: Stories without `epic:` field

---

### AC#6: Batch Processing Performance

**Given** a repository containing 15 epics and 85 stories
**When** full parsing and validation executes
**Then** complete processing finishes in <5 seconds
**And** incremental updates (single file changed) complete in <500ms
**And** memory usage remains <50MB during processing

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "RequirementsTraceabilityParser"
      file_path: ".devforgeai/traceability/parse-requirements.sh"
      dependencies:
        - "Grep"
        - "Read"
        - "jq"
      requirements:
        - id: "COMP-001"
          description: "Parse epic YAML frontmatter and extract epic_id, title fields"
          testable: true
          test_requirement: "Test: Parse EPIC-015 file, verify epic_id='EPIC-015' extracted from frontmatter"
          priority: "Critical"
        - id: "COMP-002"
          description: "Parse story YAML frontmatter and extract epic: field value"
          testable: true
          test_requirement: "Test: Parse STORY-007 file, verify epic_ref='EPIC-002' extracted"
          priority: "Critical"
        - id: "COMP-003"
          description: "Extract features section from epic files between ## Features and next ## header"
          testable: true
          test_requirement: "Test: Parse EPIC-015, verify features_count >= 7 extracted"
          priority: "High"
        - id: "COMP-004"
          description: "Handle malformed YAML gracefully - log error, continue processing"
          testable: true
          test_requirement: "Test: File with unclosed quote logs error, doesn't crash, other files still processed"
          priority: "High"
        - id: "COMP-005"
          description: "Detect orphaned stories with broken epic references"
          testable: true
          test_requirement: "Test: Story with epic: EPIC-999 appears in validation.broken_references"
          priority: "High"

    - type: "DataModel"
      name: "RequirementsMatrix"
      file_path: ".devforgeai/traceability/requirements-matrix.json"
      dependencies: []
      requirements:
        - id: "DATA-001"
          description: "Store epics map with epic_id as key, containing title, file_path, linked_stories array"
          testable: true
          test_requirement: "Test: JSON contains epics.EPIC-015.linked_stories array"
          priority: "Critical"
        - id: "DATA-002"
          description: "Store stories map with story_id as key, containing title, epic_ref, status, file_path"
          testable: true
          test_requirement: "Test: JSON contains stories.STORY-007.epic_ref field"
          priority: "Critical"
        - id: "DATA-003"
          description: "Include validation section with orphaned_stories, broken_references, unlinked_epics arrays"
          testable: true
          test_requirement: "Test: JSON contains validation.orphaned_stories array (may be empty)"
          priority: "High"
        - id: "DATA-004"
          description: "Include version and generated_at metadata fields"
          testable: true
          test_requirement: "Test: JSON contains version='1.0.0' and generated_at ISO timestamp"
          priority: "Low"

    - type: "Configuration"
      name: "TraceabilityConfig"
      file_path: ".devforgeai/traceability/config.json"
      dependencies: []
      requirements:
        - id: "CFG-001"
          description: "Define regex patterns for epic_id (^EPIC-\\d{3}$) and story_id (^STORY-\\d{3}$)"
          testable: true
          test_requirement: "Test: Config contains epic_id_pattern and story_id_pattern with valid regex"
          priority: "Medium"
        - id: "CFG-002"
          description: "Allow customization of epics_dir and stories_dir paths"
          testable: true
          test_requirement: "Test: Config contains epics_dir='.ai_docs/Epics' default"
          priority: "Low"

  business_rules:
    - id: "BR-001"
      rule: "Epic ID must match pattern ^EPIC-\\d{3}$ (e.g., EPIC-001, EPIC-015)"
      test_requirement: "Test: EPIC-1 rejected, EPIC-001 accepted"
    - id: "BR-002"
      rule: "Story ID must match pattern ^STORY-\\d{3}$ extracted from filename"
      test_requirement: "Test: STORY-007-slug.story.md extracts STORY-007"
    - id: "BR-003"
      rule: "Story epic: field must be either 'None' (standalone) or valid EPIC-NNN format"
      test_requirement: "Test: epic: INVALID-123 flagged as broken reference"
    - id: "BR-004"
      rule: "Single file parse failure must not abort entire batch - continue processing"
      test_requirement: "Test: Corrupted file 1 of 10, remaining 9 still processed"
    - id: "BR-005"
      rule: "Running parser twice with no changes produces identical output (idempotent)"
      test_requirement: "Test: Two consecutive runs produce byte-identical JSON"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Full repository parse completes within time limit"
      metric: "<5 seconds for 15 epics and 85 stories"
      test_requirement: "Test: time parse-requirements.sh, assert <5000ms"
    - id: "NFR-002"
      category: "Performance"
      requirement: "Incremental update time for single file change"
      metric: "<500ms for single file update"
      test_requirement: "Test: Modify one file, re-run, assert <500ms"
    - id: "NFR-003"
      category: "Scalability"
      requirement: "Support future growth without timeout"
      metric: "<15 seconds for 100 epics and 500 stories"
      test_requirement: "Test: Generate 100 mock epics, 500 mock stories, run parser, assert <15s"
    - id: "NFR-004"
      category: "Reliability"
      requirement: "Memory usage during full parse operation"
      metric: "<50MB peak memory"
      test_requirement: "Test: Run with memory profiler, verify peak <50MB"
    - id: "NFR-005"
      category: "Security"
      requirement: "No path traversal vulnerability"
      metric: "File paths validated against .ai_docs/ prefix"
      test_requirement: "Test: Attempt '../../../etc/passwd' path, verify rejected"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- **Full parse:** <5 seconds for 15 epics and 85 stories (current repo size)
- **Incremental update:** <500ms for single file change detection and update
- **Scalability target:** <15 seconds for 100 epics and 500 stories

**Memory:**
- Memory footprint: <50MB peak during full parse operation
- File I/O: Maximum 2 reads per file (initial parse + validation if needed)

---

### Security

**Input Sanitization:**
- All file paths validated against `.ai_docs/` directory prefix (no path traversal)
- No shell injection: File paths passed through shell commands use proper quoting

**Access Control:**
- Read-only operations: Parser does not modify source files
- Writes only to `.devforgeai/traceability/` directory
- Operates with current user permissions; no elevated privileges required

---

### Scalability

**File Handling:**
- File count: Tested up to 500 stories and 100 epics (5x current size)
- File size: Individual files up to 500KB handled without timeout
- Concurrent access: Parser locks output JSON during write (advisory lock, 5-second timeout)

---

### Reliability

**Error Handling:**
- Single file parse failure does not abort entire batch; continue processing remaining files
- All parse errors logged with file path, line number (if applicable), and error category
- Corrupt JSON output file auto-rebuilt from source on next full parse

**Idempotency:**
- Running parser twice with no file changes produces identical output

**Graceful Degradation:**
- If Grep unavailable, fallback to Read + line-by-line parsing (10x slower but functional)

---

## Edge Cases

1. **Malformed YAML Frontmatter:** Story or epic file has invalid YAML syntax (unclosed quotes, invalid characters, improper indentation). Parser must not crash; instead, log error with file path and line number, mark file as `parse_error` in data structure, continue processing remaining files.

2. **Missing or Empty `epic:` Field:** Story file has no `epic:` line at all, or has `epic:` with no value. Distinguish between "field absent" (metadata incomplete) and "field empty" (likely error). Both should be flagged but categorized differently.

3. **Epic File Without YAML Frontmatter:** Some older epic files may use inline metadata (e.g., `epic_id: EPIC-003` on line 2 without `---` delimiters). Parser should attempt pattern-based extraction as fallback when YAML frontmatter is not detected.

4. **Stories Section Format Variations:** Epic's Stories section may be:
   - Markdown table (`| STORY-001 | Title | Points |`)
   - Bullet list (`- STORY-001: Title`)
   - Mixed format or absent entirely
   Parser must handle all variations using flexible Grep patterns.

5. **Duplicate Story IDs:** Two story files with same STORY-NNN prefix (e.g., `STORY-001-feature-a.story.md` and `STORY-001-feature-b.story.md`). Parser must detect and report conflict, store both with disambiguation.

6. **Circular or Self-References:** Story file contains `epic: STORY-XXX` (referencing a story instead of epic). Validation must detect and flag as invalid reference type.

7. **File Encoding Issues:** Files with non-UTF-8 encoding or BOM markers. Parser should handle gracefully, attempt UTF-8 decoding first, fallback to latin-1 if needed.

8. **Empty Files:** Story or epic file exists but has no content. Parser must detect and categorize as `empty_file` rather than crashing.

9. **Deleted Epic with Existing Story References:** Epic file is deleted but stories still reference it. Validation must catch this bidirectional inconsistency.

10. **Large Files:** Epic files >100KB (containing extensive technical specifications). Parser must not timeout; streaming approach if needed.

---

## Data Validation Rules

1. **Epic ID Format:** Must match pattern `^EPIC-\d{3}$` (EPIC- followed by exactly 3 digits). Examples: `EPIC-001`, `EPIC-015`. Invalid: `EPIC-1`, `EPIC-0001`, `epic-001`, `EPIC_001`.

2. **Story ID Format:** Must match pattern `^STORY-\d{3}$` (STORY- followed by exactly 3 digits). Extracted from filename before first hyphen after number.

3. **Frontmatter YAML Structure:** Must be delimited by `---` on line 1 and another `---` before content. Fields within frontmatter must follow YAML syntax (key: value).

4. **Required Epic Fields:** `title` is required; `epic_id` is required but may be inferred from filename if missing from content.

5. **Required Story Fields:** `title`, `epic` (may be `None`), `status`, `priority`, `points` in frontmatter.

6. **File Path Validation:**
   - Epic files: `.ai_docs/Epics/EPIC-NNN-*.epic.md`
   - Story files: `.ai_docs/Stories/STORY-NNN-*.story.md`

7. **Epic Reference Value:** Must be either `None` (literal string) or valid EPIC-NNN format.

---

## Dependencies

### Prerequisite Stories

None - this is the foundational story for EPIC-015.

### External Dependencies

None - uses only Claude Code native tools (Grep, Read, Write, Bash).

### Technology Dependencies

- **jq:** JSON processing (standard CLI tool)
  - Purpose: Parse and format JSON output
  - Approved: Yes (standard Unix tool)

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for parsing functions

**Test Scenarios:**
1. **Happy Path:** Parse valid epic and story files with complete frontmatter
2. **Edge Cases:**
   - Malformed YAML frontmatter
   - Missing epic: field
   - Epic without YAML frontmatter (inline metadata)
   - Stories section format variations
   - Duplicate story IDs
3. **Error Cases:**
   - Non-existent file path
   - Empty file
   - Invalid UTF-8 encoding

### Integration Tests

**Coverage Target:** 85%+ for full workflow

**Test Scenarios:**
1. **End-to-End Parse Flow:** Parse all epics and stories in test fixtures
2. **Validation Integration:** Run validation on populated matrix
3. **Performance Test:** Time full parse of real repository

---

## Acceptance Criteria Verification Checklist

### AC#1: Epic Frontmatter Parsing

- [ ] epic_id extraction works - **Phase:** 2 - **Evidence:** tests/traceability/test_epic_parsing.sh
- [ ] title extraction works - **Phase:** 2 - **Evidence:** tests/traceability/test_epic_parsing.sh
- [ ] features section extraction works - **Phase:** 2 - **Evidence:** tests/traceability/test_epic_parsing.sh
- [ ] stories table extraction works - **Phase:** 2 - **Evidence:** tests/traceability/test_epic_parsing.sh

### AC#2: Story Epic Reference Parsing

- [ ] story_id from filename works - **Phase:** 2 - **Evidence:** tests/traceability/test_story_parsing.sh
- [ ] epic: field extraction works - **Phase:** 2 - **Evidence:** tests/traceability/test_story_parsing.sh
- [ ] handles epic: None - **Phase:** 2 - **Evidence:** tests/traceability/test_story_parsing.sh
- [ ] handles missing epic: field - **Phase:** 2 - **Evidence:** tests/traceability/test_story_parsing.sh

### AC#3: Relationship Data Structure

- [ ] epics map populated correctly - **Phase:** 2 - **Evidence:** tests/traceability/test_data_model.sh
- [ ] stories map populated correctly - **Phase:** 2 - **Evidence:** tests/traceability/test_data_model.sh
- [ ] JSON persisted to correct path - **Phase:** 2 - **Evidence:** tests/traceability/test_data_model.sh

### AC#4: Epic Reference Validation

- [ ] validates epic file exists - **Phase:** 3 - **Evidence:** tests/traceability/test_validation.sh
- [ ] detects broken references - **Phase:** 3 - **Evidence:** tests/traceability/test_validation.sh
- [ ] reports specific error messages - **Phase:** 3 - **Evidence:** tests/traceability/test_validation.sh

### AC#5: Orphaned Story Detection

- [ ] detects intentionally standalone - **Phase:** 3 - **Evidence:** tests/traceability/test_orphan_detection.sh
- [ ] detects broken references - **Phase:** 3 - **Evidence:** tests/traceability/test_orphan_detection.sh
- [ ] detects missing metadata - **Phase:** 3 - **Evidence:** tests/traceability/test_orphan_detection.sh

### AC#6: Batch Processing Performance

- [ ] full parse <5 seconds - **Phase:** 4 - **Evidence:** tests/traceability/test_performance.sh
- [ ] incremental update <500ms - **Phase:** 4 - **Evidence:** tests/traceability/test_performance.sh
- [ ] memory <50MB - **Phase:** 4 - **Evidence:** tests/traceability/test_performance.sh

---

**Checklist Progress:** 0/18 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] Parser script created at `.devforgeai/traceability/parse-requirements.sh`
- [ ] Configuration file created at `.devforgeai/traceability/config.json`
- [ ] JSON output schema implemented for requirements-matrix.json
- [ ] Epic frontmatter parsing implemented with Grep patterns
- [ ] Story epic: field parsing implemented
- [ ] Orphaned story detection implemented
- [ ] Error handling for malformed files implemented

### Quality
- [ ] All 6 acceptance criteria have passing tests
- [ ] Edge cases covered (10 documented edge cases)
- [ ] Data validation enforced (7 validation rules)
- [ ] NFRs met (performance <5s, memory <50MB)
- [ ] Code coverage >95% for parsing functions

### Testing
- [ ] Unit tests for epic parsing
- [ ] Unit tests for story parsing
- [ ] Unit tests for validation logic
- [ ] Integration test for full parse workflow
- [ ] Performance test for timing requirements

### Documentation
- [ ] README in `.devforgeai/traceability/` explaining usage
- [ ] JSON schema documented
- [ ] Error codes and messages documented

---

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Notes

**Design Decisions:**
- Using Bash script + jq for JSON processing (no external dependencies beyond standard tools)
- JSON file for data storage (simple, human-readable, no database required)
- Grep patterns for extraction (Claude Code native tool, efficient)

**Related ADRs:**
- ADR-005 (pending): Epic Coverage Traceability Architecture

**References:**
- EPIC-015: Epic Coverage Validation & Requirements Traceability
- RESEARCH-002: Epic Coverage Traceability (feasibility analysis)

---

**Story Template Version:** 2.1
**Last Updated:** 2025-11-25
