---
id: STORY-084
title: Epic & Story Metadata Parser
epic: EPIC-015
sprint: Backlog
status: Backlog
points: 13
priority: Medium
assigned_to: Unassigned
created: 2025-11-25
format_version: "2.1"
---

# Story: Epic & Story Metadata Parser

## Description

**As a** DevForgeAI framework maintainer,
**I want** a robust parsing system that extracts metadata and feature information from epic and story markdown files,
**so that** I can establish reliable data foundations for gap detection, coverage mapping, and requirements traceability across the project lifecycle.

## Acceptance Criteria

### AC#1: Epic Frontmatter Parsing

**Given** an epic file exists in `.ai_docs/Epics/` directory with YAML frontmatter
**When** the epic parser processes the file
**Then** it extracts:
- `epic_id` field (format: EPIC-NNN, validated against regex `^EPIC-\d{3}$`)
- `title` field (non-empty string, max 200 characters)
- `status` field (enum: Planning, In Progress, Complete, On Hold)
- `priority` field (enum: Critical, High, Medium, Low)
- `created` field (date in YYYY-MM-DD format)
- `complexity` field (positive integer)
- `estimated_sprints` field (positive integer)
- `tags` field (array of strings)
**And** parsing completes in <100ms per file

---

### AC#2: Epic Features Section Extraction

**Given** an epic file contains a Features section with markdown headers
**When** the epic parser processes the Features section
**Then** it extracts:
- Feature headers matching pattern `### Feature \d+:` or `### Feature \d+\.\d+:`
- Feature title (text after the colon)
- Feature description (text block until next `###` or `---` or `##` header)
- Feature dependencies (if present, text after "Dependencies:")
- Feature estimated points (if present, integer after "Estimated Points:")
**And** supports variations:
- `### Feature 1: Title` (standard format)
- `### Feature 3.1: Title` (sub-feature format)
- `### Feature 1: Title (STORY-XXX)` (with linked story)

---

### AC#3: Story Frontmatter Parsing

**Given** a story file exists in `.ai_docs/Stories/` directory with YAML frontmatter
**When** the story parser processes the file
**Then** it extracts:
- `id` field (format: STORY-NNN, validated against regex `^STORY-\d{3}$`)
- `title` field (non-empty string, max 200 characters)
- `epic` field (format: EPIC-NNN or "None" or null)
- `sprint` field (format: Sprint-N or "Backlog")
- `status` field (enum: Backlog, Ready for Dev, In Development, Dev Complete, QA In Progress, QA Approved, QA Failed, Releasing, Released)
- `points` field (Fibonacci: 1, 2, 3, 5, 8, 13, 21)
- `priority` field (enum: Critical, High, Medium, Low)
- `format_version` field (semantic version string)
**And** extracts story_id from filename pattern `STORY-NNN-slug.story.md` as fallback

---

### AC#4: Malformed YAML Error Handling

**Given** an epic or story file contains malformed YAML frontmatter
**When** the parser attempts to process the file
**Then** it:
- Catches YAML parsing exceptions (syntax errors, invalid types)
- Returns structured error object with `file_path`, `line_number`, `error_type`, `error_message`
- Does NOT crash or throw unhandled exceptions
- Continues processing remaining files in batch operations
**And** handles specific error cases:
- Missing frontmatter delimiters (`---`)
- Unclosed YAML blocks
- Invalid YAML syntax (bad indentation, missing colons)
- Type mismatches (string where number expected)

---

### AC#5: Missing Frontmatter Handling

**Given** an epic or story file lacks YAML frontmatter entirely
**When** the parser processes the file
**Then** it:
- Detects absence of opening `---` delimiter within first 3 lines
- Returns error with `error_type: "MISSING_FRONTMATTER"`
- Attempts to extract metadata from inline patterns:
  - Epic ID from `# EPIC-NNN:` header
  - Story ID from filename `STORY-NNN-*.story.md`
- Flags file as `needs_remediation: true`
**And** includes recovery suggestions in error response

---

### AC#6: Epic-Story Linkage Validation

**Given** a story file contains `epic: EPIC-NNN` in frontmatter
**When** validation runs against the parsed epic registry
**Then** it verifies:
- Referenced epic file exists in `.ai_docs/Epics/` directory
- Referenced epic_id matches an entry in parsed epics collection
- Returns validation result with:
  - `is_valid: boolean`
  - `referenced_epic: string`
  - `epic_exists: boolean`
  - `epic_title: string` (if exists)
**And** identifies broken references with actionable error messages:
- "Story STORY-XXX references non-existent epic EPIC-YYY. Available epics: [list]"

---

### AC#7: Coverage Mapping Generation

**Given** all epics and stories have been parsed successfully
**When** the coverage mapping algorithm runs
**Then** it generates:
- Per-epic feature coverage: Map of epic_id to {total_features, covered_features, coverage_percentage, feature_details[]}
- Story-to-epic index: Map of story_id to epic_id
- Epic-to-stories index: Map of epic_id to story_id[]
- Orphaned stories list: Stories with no valid epic reference
- Uncovered features list: Epic features with no linked stories
**And** the mapping structure supports:
- Query by epic_id to get all linked stories
- Query by story_id to get parent epic
- Aggregate statistics (total coverage percentage)

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "EpicMetadataParser"
      file_path: ".devforgeai/traceability/epic-parser.sh"
      dependencies:
        - "Grep"
        - "Read"
        - "jq"
      requirements:
        - id: "EPIC-PARSE-001"
          description: "Parse YAML frontmatter from epic markdown files and return structured data"
          testable: true
          test_requirement: "Test: Given valid epic file, parser returns object with epic_id, title, status, features[]"
          priority: "Critical"
        - id: "EPIC-PARSE-002"
          description: "Extract Features section headers with regex pattern matching"
          testable: true
          test_requirement: "Test: Given epic with 5 features using various formats, parser extracts all 5 with titles"
          priority: "Critical"
        - id: "EPIC-PARSE-003"
          description: "Handle malformed YAML without crashing"
          testable: true
          test_requirement: "Test: Given file with invalid YAML, parser returns error object with line number and message"
          priority: "High"

    - type: "Service"
      name: "StoryMetadataParser"
      file_path: ".devforgeai/traceability/story-parser.sh"
      dependencies:
        - "Grep"
        - "Read"
        - "jq"
      requirements:
        - id: "STORY-PARSE-001"
          description: "Parse YAML frontmatter from story markdown files and return structured data"
          testable: true
          test_requirement: "Test: Given valid story file, parser returns object with story_id, title, epic, status, points"
          priority: "Critical"
        - id: "STORY-PARSE-002"
          description: "Extract story_id from filename as fallback when frontmatter missing id field"
          testable: true
          test_requirement: "Test: Given file STORY-042-slug.story.md without id in frontmatter, parser extracts STORY-042"
          priority: "High"
        - id: "STORY-PARSE-003"
          description: "Validate epic reference format and flag invalid values"
          testable: true
          test_requirement: "Test: Given story with epic: 'invalid', parser returns validation error for epic field"
          priority: "High"

    - type: "Service"
      name: "CoverageMappingService"
      file_path: ".devforgeai/traceability/coverage-mapper.sh"
      dependencies:
        - "EpicMetadataParser"
        - "StoryMetadataParser"
        - "jq"
      requirements:
        - id: "COVERAGE-001"
          description: "Generate bidirectional epic-story index from parsed metadata"
          testable: true
          test_requirement: "Test: Given 3 epics and 10 stories, service returns epicToStories and storyToEpic maps"
          priority: "Critical"
        - id: "COVERAGE-002"
          description: "Calculate coverage percentage per epic based on feature-story linkage"
          testable: true
          test_requirement: "Test: Given epic with 5 features and 3 linked stories, coverage equals 60%"
          priority: "High"
        - id: "COVERAGE-003"
          description: "Identify orphaned stories with broken or missing epic references"
          testable: true
          test_requirement: "Test: Given story referencing EPIC-999 (non-existent), story appears in orphanedStories list"
          priority: "High"

    - type: "DataModel"
      name: "ParsedEpic"
      file_path: ".devforgeai/traceability/models/epic.json"
      dependencies: []
      requirements:
        - id: "MODEL-EPIC-001"
          description: "Define JSON schema for parsed epic metadata with all frontmatter fields"
          testable: true
          test_requirement: "Test: JSON schema validates epic objects correctly"
          priority: "Critical"
        - id: "MODEL-EPIC-002"
          description: "Include features array with Feature sub-schema containing title, description, dependencies"
          testable: true
          test_requirement: "Test: ParsedEpic.features validates as array of Feature objects"
          priority: "High"

    - type: "DataModel"
      name: "ParsedStory"
      file_path: ".devforgeai/traceability/models/story.json"
      dependencies: []
      requirements:
        - id: "MODEL-STORY-001"
          description: "Define JSON schema for parsed story metadata with all frontmatter fields"
          testable: true
          test_requirement: "Test: JSON schema validates story objects correctly"
          priority: "Critical"
        - id: "MODEL-STORY-002"
          description: "Include epic_id field as string or null for proper null handling"
          testable: true
          test_requirement: "Test: Stories with epic: None and epic: EPIC-015 both validate against schema"
          priority: "High"

    - type: "DataModel"
      name: "ParsingError"
      file_path: ".devforgeai/traceability/models/error.json"
      dependencies: []
      requirements:
        - id: "MODEL-ERROR-001"
          description: "Define structured error type with file_path, line_number, error_type, error_message fields"
          testable: true
          test_requirement: "Test: Error objects contain all required fields for debugging and reporting"
          priority: "High"
        - id: "MODEL-ERROR-002"
          description: "Support error_type enum: MALFORMED_YAML, MISSING_FRONTMATTER, INVALID_FIELD, VALIDATION_ERROR"
          testable: true
          test_requirement: "Test: Each error type is distinguishable for conditional handling"
          priority: "Medium"

  business_rules:
    - id: "BR-001"
      rule: "epic_id format must match regex ^EPIC-\\d{3}$. Leading zeros preserved."
      test_requirement: "Test: EPIC-7 rejected, EPIC-007 accepted"
    - id: "BR-002"
      rule: "story_id format must match regex ^STORY-\\d{3}$. Extracted from frontmatter or filename."
      test_requirement: "Test: STORY-42 rejected, STORY-042 accepted"
    - id: "BR-003"
      rule: "Story epic reference must be None, null, or valid EPIC-NNN format. Empty string invalid."
      test_requirement: "Test: epic: '' flagged as invalid"
    - id: "BR-004"
      rule: "Points field must be Fibonacci number from {1, 2, 3, 5, 8, 13, 21}. Value 0 invalid."
      test_requirement: "Test: points: 4 rejected, points: 5 accepted"
    - id: "BR-005"
      rule: "Single file parse failure must not abort batch processing."
      test_requirement: "Test: Batch of 10 files with 1 corrupt, remaining 9 parsed successfully"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Single file parsing time"
      metric: "<100ms per file for files up to 50KB"
      test_requirement: "Test: Parse 50KB epic file, assert time <100ms"
    - id: "NFR-002"
      category: "Performance"
      requirement: "Batch parsing time"
      metric: "<5 seconds for 15 epics + 85 stories"
      test_requirement: "Test: Parse full repo, assert time <5000ms"
    - id: "NFR-003"
      category: "Reliability"
      requirement: "Memory usage during batch processing"
      metric: "<50MB peak memory"
      test_requirement: "Test: Run batch parse with memory profiler, verify peak <50MB"
    - id: "NFR-004"
      category: "Security"
      requirement: "Path traversal prevention"
      metric: "All paths validated against .ai_docs/ prefix"
      test_requirement: "Test: Attempt '../../../etc/passwd', verify rejected"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- **Single file parsing:** <100ms per file for files up to 50KB
- **Batch parsing (15 epics + 85 stories):** <5 seconds total
- **Coverage mapping generation:** <500ms after parsing complete
- **Incremental parsing:** <200ms for single file change detection and re-parse

**Memory:**
- Memory usage: <50MB during full batch processing

---

### Security

**Input Sanitization:**
- Path traversal prevention: All file paths validated against allowed directories (`.ai_docs/Epics/`, `.ai_docs/Stories/`)
- File size limit: Reject files >1MB to prevent memory exhaustion attacks
- YAML injection prevention: Use safe YAML loader (no code execution during parse)
- Input sanitization: Strip or escape HTML/script tags in extracted text fields

---

### Reliability

**Error Handling:**
- Error isolation: Single file parse failure does not abort batch processing
- Graceful degradation: Return partial results with error log when some files fail
- Validation warnings vs errors: Warnings do not block processing; errors mark file as unparseable

---

### Scalability

**Concurrent Processing:**
- Support parallel parsing of up to 10 files simultaneously
- Repository size support: Tested with 100 epics and 500 stories
- Incremental processing: Track file modification timestamps to avoid re-parsing unchanged files

---

## Edge Cases

1. **Empty Features section in epic:** Epic file has `## Features` header but no `### Feature` entries. Parser returns `features_count: 0` and flags epic as `has_empty_features: true`.

2. **Duplicate epic_id across files:** Two epic files contain same `epic_id: EPIC-007` in frontmatter. Parser detects duplicate, returns error for second file encountered.

3. **Story references epic via inline text only:** Story lacks `epic:` frontmatter field but mentions "Related to EPIC-015" in description. Parser marks as `epic_reference: "implicit"` with `confidence: "low"`.

4. **Epic file with Windows line endings (CRLF):** Parser normalizes line endings before parsing and logs warning about mixed line endings.

5. **Circular feature dependencies in epic:** Feature A depends on Feature B, Feature B depends on Feature A. Parser detects cycle and reports `circular_dependency_detected: true`.

6. **Story file with BOM (Byte Order Mark):** UTF-8 story file starts with BOM character. Parser strips BOM before processing.

7. **Epic frontmatter contains special YAML characters unquoted:** Parser handles common YAML escaping issues and suggests quoting fix in error message.

8. **Story with numeric epic field:** Story frontmatter contains `epic: 15` (number) instead of `epic: EPIC-015` (string). Parser coerces to string format if recognizable pattern.

---

## Data Validation Rules

1. **epic_id format:** Must match regex `^EPIC-\d{3}$`. Maximum value: EPIC-999.

2. **story_id format:** Must match regex `^STORY-\d{3}$`. Frontmatter takes precedence over filename.

3. **epic reference in story:** Valid values are `None`, `null`, or `EPIC-NNN` format. Empty string `""` is invalid.

4. **Feature numbering:** Must be sequential within epic. Gap generates warning but not error.

5. **Date fields:** Must be valid ISO 8601 date (YYYY-MM-DD).

6. **Points field:** Must be Fibonacci number from set {1, 2, 3, 5, 8, 13, 21}.

7. **Status field:** Must be valid enum value. Case-insensitive matching.

8. **Title length:** Epic and story titles must be 1-200 characters.

9. **Tags array:** Each tag must be non-empty string, max 50 characters, alphanumeric with hyphens only.

10. **format_version:** Must match semantic version pattern. Defaults to "1.0" if missing.

---

## Dependencies

### Prerequisite Stories

- **STORY-083:** Requirements Traceability Matrix Foundation
  - **Why:** STORY-083 defines the data model that STORY-084 parsers will populate
  - **Status:** Backlog

### External Dependencies

None - uses only Claude Code native tools (Grep, Read, jq).

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
   - Missing frontmatter entirely
   - Duplicate epic IDs
   - Windows line endings
   - BOM characters
3. **Error Cases:**
   - Invalid file path
   - Empty file
   - Invalid YAML syntax

### Integration Tests

**Coverage Target:** 85%+ for full workflow

**Test Scenarios:**
1. **End-to-End Parse Flow:** Parse all epics and stories
2. **Coverage Mapping:** Generate mapping from parsed data
3. **Error Aggregation:** Multiple files with various errors

---

## Acceptance Criteria Verification Checklist

### AC#1: Epic Frontmatter Parsing

- [ ] epic_id extraction works - **Phase:** 2 - **Evidence:** tests/traceability/test_epic_parser.sh
- [ ] title extraction works - **Phase:** 2 - **Evidence:** tests/traceability/test_epic_parser.sh
- [ ] status extraction works - **Phase:** 2 - **Evidence:** tests/traceability/test_epic_parser.sh
- [ ] parsing completes <100ms - **Phase:** 4 - **Evidence:** tests/traceability/test_performance.sh

### AC#2: Epic Features Section Extraction

- [ ] standard feature format parsed - **Phase:** 2 - **Evidence:** tests/traceability/test_features_parser.sh
- [ ] sub-feature format parsed - **Phase:** 2 - **Evidence:** tests/traceability/test_features_parser.sh
- [ ] dependencies extracted - **Phase:** 2 - **Evidence:** tests/traceability/test_features_parser.sh

### AC#3: Story Frontmatter Parsing

- [ ] all fields extracted - **Phase:** 2 - **Evidence:** tests/traceability/test_story_parser.sh
- [ ] filename fallback works - **Phase:** 2 - **Evidence:** tests/traceability/test_story_parser.sh

### AC#4: Malformed YAML Error Handling

- [ ] catches YAML exceptions - **Phase:** 2 - **Evidence:** tests/traceability/test_error_handling.sh
- [ ] returns structured error - **Phase:** 2 - **Evidence:** tests/traceability/test_error_handling.sh
- [ ] continues batch processing - **Phase:** 2 - **Evidence:** tests/traceability/test_error_handling.sh

### AC#5: Missing Frontmatter Handling

- [ ] detects missing frontmatter - **Phase:** 2 - **Evidence:** tests/traceability/test_error_handling.sh
- [ ] attempts inline extraction - **Phase:** 2 - **Evidence:** tests/traceability/test_error_handling.sh

### AC#6: Epic-Story Linkage Validation

- [ ] validates epic exists - **Phase:** 3 - **Evidence:** tests/traceability/test_validation.sh
- [ ] returns validation result - **Phase:** 3 - **Evidence:** tests/traceability/test_validation.sh
- [ ] identifies broken references - **Phase:** 3 - **Evidence:** tests/traceability/test_validation.sh

### AC#7: Coverage Mapping Generation

- [ ] generates epic-to-stories index - **Phase:** 3 - **Evidence:** tests/traceability/test_coverage_mapping.sh
- [ ] generates story-to-epic index - **Phase:** 3 - **Evidence:** tests/traceability/test_coverage_mapping.sh
- [ ] identifies orphaned stories - **Phase:** 3 - **Evidence:** tests/traceability/test_coverage_mapping.sh

---

**Checklist Progress:** 0/20 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] Epic parser script created at `.devforgeai/traceability/epic-parser.sh`
- [ ] Story parser script created at `.devforgeai/traceability/story-parser.sh`
- [ ] Coverage mapper script created at `.devforgeai/traceability/coverage-mapper.sh`
- [ ] JSON schemas created for ParsedEpic, ParsedStory, ParsingError
- [ ] YAML frontmatter parsing implemented
- [ ] Features section extraction implemented
- [ ] Epic-story linkage validation implemented
- [ ] Coverage mapping generation implemented

### Quality
- [ ] All 7 acceptance criteria have passing tests
- [ ] Edge cases covered (8 documented edge cases)
- [ ] Data validation enforced (10 validation rules)
- [ ] NFRs met (parsing <100ms, batch <5s)
- [ ] Code coverage >95% for parsing functions

### Testing
- [ ] Unit tests for epic parser
- [ ] Unit tests for story parser
- [ ] Unit tests for error handling
- [ ] Integration test for coverage mapping
- [ ] Performance test for timing requirements

### Documentation
- [ ] README documenting parser usage
- [ ] JSON schema documentation
- [ ] Error codes and messages documented

---

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Notes

**Design Decisions:**
- Using Bash scripts + Grep patterns for parsing (Claude Code native tools)
- jq for JSON processing (standard Unix tool)
- JSON files for data storage (human-readable, no database)

**Related ADRs:**
- ADR-005 (pending): Epic Coverage Traceability Architecture

**References:**
- EPIC-015: Epic Coverage Validation & Requirements Traceability
- STORY-083: Requirements Traceability Matrix Foundation

---

**Story Template Version:** 2.1
**Last Updated:** 2025-11-25
