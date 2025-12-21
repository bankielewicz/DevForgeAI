---
id: STORY-099
title: Baseline Metrics Collection
epic: EPIC-016
sprint: Sprint-6
status: Backlog
points: 5
priority: Medium
assigned_to: Unassigned
created: 2025-12-01
format_version: "2.1"
---

# Story: Baseline Metrics Collection

## Description

**As a** framework maintainer,
**I want** to capture baseline accuracy metrics before implementing evidence-based grounding, including rule violations, hallucinations, and citation usage for 10 representative operations (3x /dev, 3x /qa, 2x /create-story, 2x architecture questions),
**so that** I can measure improvement against the 2x hallucination reduction target and validate the effectiveness of evidence-based grounding implementation.

## Acceptance Criteria

### AC#1: Baseline Metrics Collection for /dev Operations

**Given** 3 representative /dev command executions have been performed
**When** the baseline collection process runs
**Then** the metrics document captures for each operation:
- Operation timestamp (ISO 8601 format)
- Story ID processed
- Rule violations count (with specific rule numbers from CLAUDE.md Critical Rules 1-11)
- Hallucinations observed (count with descriptions of each instance)
- Citations used (Y/N for each recommendation, total count)
- Operation duration in seconds

---

### AC#2: Baseline Metrics Collection for /qa Operations

**Given** 3 representative /qa command executions have been performed
**When** the baseline collection process runs
**Then** the metrics document captures for each operation:
- Operation timestamp (ISO 8601 format)
- Story ID validated
- Validation mode (light/deep)
- Rule violations count (with specific rule numbers)
- Hallucinations observed (count with descriptions)
- Citations used (Y/N count)
- QA pass/fail outcome

---

### AC#3: Baseline Metrics Collection for /create-story Operations

**Given** 2 representative /create-story command executions have been performed
**When** the baseline collection process runs
**Then** the metrics document captures for each operation:
- Operation timestamp (ISO 8601 format)
- Feature description provided
- Story ID generated
- Rule violations count
- Hallucinations observed (count with descriptions)
- Citations used (Y/N count)
- Acceptance criteria count generated

---

### AC#4: Baseline Metrics Collection for Architecture Questions

**Given** 2 representative architecture questions have been answered
**When** the baseline collection process runs
**Then** the metrics document captures for each question:
- Question timestamp (ISO 8601 format)
- Question text (verbatim)
- Context files referenced (list of files)
- Rule violations count
- Hallucinations observed (count with descriptions)
- Citations used (Y/N count, with citation format compliance Y/N)
- Files read during response (count)

---

### AC#5: Baseline Document Generation

**Given** all 10 operations have been collected
**When** the baseline document is generated
**Then** the file `devforgeai/metrics/baseline-YYYY-MM-DD.md` is created containing:
- Summary statistics (total violations, hallucinations, citation rate)
- Per-operation breakdown (10 entries)
- Categorized issues (rule violations by rule number, hallucination types)
- Baseline date and framework version
- Operations tested list with timestamps
- Aggregate metrics: violation rate (%), hallucination rate (%), citation compliance rate (%)

---

### AC#6: Metrics Directory Structure

**Given** the `devforgeai/metrics/` directory does not exist
**When** baseline collection is initiated
**Then** the directory structure is created:
- `devforgeai/metrics/` directory created
- `devforgeai/metrics/baseline-YYYY-MM-DD.md` file created
- `devforgeai/metrics/README.md` with usage instructions created
- File permissions set appropriately (644 for files, 755 for directory)

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "BaselineMetricsConfig"
      file_path: "devforgeai/metrics/README.md"
      dependencies: []
      requirements:
        - id: "CONF-001"
          description: "Define baseline file format and field definitions"
          testable: true
          test_requirement: "Test: README.md exists and contains all field descriptions from AC5"
          priority: "High"
        - id: "CONF-002"
          description: "Provide usage examples for manual baseline capture"
          testable: true
          test_requirement: "Test: README includes step-by-step guide for capturing each operation type"
          priority: "Medium"

    - type: "DataModel"
      name: "BaselineMetricsDocument"
      file_path: "devforgeai/metrics/baseline-YYYY-MM-DD.md"
      dependencies: []
      requirements:
        - id: "DM-001"
          description: "Include YAML frontmatter with metadata (format_version, capture_date, framework_version)"
          testable: true
          test_requirement: "Test: Document starts with valid YAML frontmatter containing required fields"
          priority: "Critical"
        - id: "DM-002"
          description: "Include summary statistics section with aggregate metrics"
          testable: true
          test_requirement: "Test: Document contains '## Summary Statistics' with total_operations, rule_violations_total, hallucinations_total, citation_rate_percent"
          priority: "Critical"
        - id: "DM-003"
          description: "Include per-operation breakdown for all 10 operations"
          testable: true
          test_requirement: "Test: Document contains 10 operation entries under '## Operations' with required fields per AC1-AC4"
          priority: "Critical"
        - id: "DM-004"
          description: "Include categorized issues section"
          testable: true
          test_requirement: "Test: Document contains '## Categorized Issues' with violations_by_rule and hallucination_types subsections"
          priority: "High"

    - type: "Configuration"
      name: "MetricsDirectoryStructure"
      file_path: "devforgeai/metrics/"
      dependencies: []
      requirements:
        - id: "CONF-003"
          description: "Create metrics directory with proper permissions"
          testable: true
          test_requirement: "Test: Directory exists with 755 permissions (owner rwx, group/other rx)"
          priority: "High"
        - id: "CONF-004"
          description: "Handle pre-existing directory gracefully"
          testable: true
          test_requirement: "Test: If directory exists, no error thrown; if file exists with same name as baseline, append version suffix"
          priority: "Medium"

  business_rules:
    - id: "BR-001"
      rule: "Exactly 10 operations must be recorded (3 /dev + 3 /qa + 2 /create-story + 2 architecture questions)"
      test_requirement: "Test: Document is marked incomplete if operation count < 10"
    - id: "BR-002"
      rule: "All timestamps must be ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)"
      test_requirement: "Test: Regex validation rejects malformed timestamps"
    - id: "BR-003"
      rule: "Rule violations must reference specific rule numbers (1-11) from CLAUDE.md Critical Rules"
      test_requirement: "Test: Generic 'rule violation' without number is flagged as invalid"
    - id: "BR-004"
      rule: "Each hallucination description must be minimum 10 words explaining what was incorrect"
      test_requirement: "Test: Descriptions under 10 words trigger validation warning"
    - id: "BR-005"
      rule: "Citation count must be non-negative integer (not blank, null, or negative)"
      test_requirement: "Test: Validation rejects blank, null, or negative citation counts"
    - id: "BR-006"
      rule: "Aggregate metrics must be within bounds (0-100% for rates)"
      test_requirement: "Test: Rates outside 0-100 range trigger validation error"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Baseline document generation time"
      metric: "< 5 seconds after all 10 operations recorded"
      test_requirement: "Test: Time document generation, assert < 5000ms"
    - id: "NFR-002"
      category: "Performance"
      requirement: "Individual operation metric capture overhead"
      metric: "< 100ms per operation"
      test_requirement: "Test: Measure metric logging time, assert < 100ms"
    - id: "NFR-003"
      category: "Security"
      requirement: "File permissions for baseline documents"
      metric: "644 (owner rw, group/other r)"
      test_requirement: "Test: Check file permissions after creation"
    - id: "NFR-004"
      category: "Security"
      requirement: "No sensitive data in baseline documents"
      metric: "Zero API keys, tokens, or credentials"
      test_requirement: "Test: Scan document for common secret patterns (API_KEY, TOKEN, etc.)"
    - id: "NFR-005"
      category: "Reliability"
      requirement: "Atomic writes for baseline file"
      metric: "Write to temp file, then rename (prevent corruption)"
      test_requirement: "Test: Simulate write failure mid-operation, verify no partial files"
    - id: "NFR-006"
      category: "Maintainability"
      requirement: "Test coverage for metrics collection code"
      metric: ">= 85% line coverage"
      test_requirement: "Test: Run coverage report, assert >= 85%"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Document Generation:**
- Baseline document generation: < 5 seconds after all 10 operations recorded
- Individual operation metric capture: < 100ms overhead per operation
- File write operations: < 500ms for baseline document creation

**Memory:**
- Memory footprint: < 5MB for metrics collection state during operation logging

---

### Security

**File Permissions:**
- Baseline files: 644 permissions (owner read/write, group/other read-only)
- Metrics directory: 755 permissions (owner rwx, group/other rx)

**Data Protection:**
- No sensitive data: Baseline documents must not contain API keys, tokens, or user credentials
- Sanitize operation logs before writing to baseline
- Path traversal prevention: File paths validated to prevent writing outside `devforgeai/metrics/`

---

### Reliability

**Error Handling:**
- Atomic writes: Write to temp file, then rename to prevent corruption
- Backup on overwrite: If baseline file exists, create `.backup` copy before overwriting
- Error recovery: If write fails, preserve metrics in memory and retry up to 3 times with 1-second intervals
- Graceful degradation: If metrics directory creation fails, log warning and continue operations

---

### Maintainability

**Documentation:**
- README.md in metrics directory explains baseline format, fields, and usage
- Self-describing format: Each field in baseline document includes inline description on first occurrence

**Validation:**
- Baseline document can be validated against schema using validation script
- Test coverage: Metrics collection code achieves minimum 85% line coverage

---

## Edge Cases

1. **Partial Operation Completion:** If an operation fails mid-execution (e.g., /dev fails at Phase 3), capture partial metrics up to the failure point with a "Status: Incomplete" flag. Include failure reason and phase reached. Do not discard partial data.

2. **Zero Violations/Hallucinations Scenario:** If an operation completes with zero rule violations and zero hallucinations, record explicit "0" values (not blank or N/A) to establish a valid baseline data point.

3. **Pre-existing Metrics Directory:** If `devforgeai/metrics/` already exists (from prior runs), append date suffix to avoid overwriting (e.g., `baseline-2025-12-01-v2.md` if `baseline-2025-12-01.md` exists).

4. **Ambiguous Hallucination Classification:** When an inaccurate statement could be classified as either "rule violation" or "hallucination," use these criteria:
   - Rule violation: Statement contradicts explicit text in CLAUDE.md Critical Rules 1-11
   - Hallucination: Statement presents invented facts not present in any project file

5. **Citation Format Variations:** Accept multiple valid citation formats during baseline collection:
   - `(Source: file.md, lines X-Y)` - Full format
   - `(See: file.md)` - Abbreviated format
   - Inline file references without formal citation structure

6. **Long-Running Operations:** If an operation exceeds 10 minutes, record a "Duration: >600s" flag and note timeout condition.

---

## Data Validation Rules

1. **Operation Count:** Exactly 10 operations must be recorded (3 /dev + 3 /qa + 2 /create-story + 2 architecture questions). Document is incomplete if count < 10.

2. **Timestamp Format:** All timestamps must be ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ). Reject malformed timestamps.

3. **Rule Violation References:** Rule violations must reference specific rule numbers (1-11) from CLAUDE.md Critical Rules section.

4. **Hallucination Descriptions:** Each hallucination must include a description of minimum 10 words explaining what was incorrect.

5. **Citation Count Non-Negative:** Citation used counts must be non-negative integers.

6. **File Path Format:** Baseline file path must match pattern `devforgeai/metrics/baseline-\d{4}-\d{2}-\d{2}(-v\d+)?\.md`.

7. **Aggregate Metric Bounds:** Violation rate, hallucination rate, citation compliance rate: 0-100%.

8. **Story ID Format:** For /dev and /qa operations, Story ID must match pattern `STORY-\d{3}`.

---

## Dependencies

### Prerequisite Stories

None - This is the foundational story for EPIC-016.

### External Dependencies

None - No external services required.

### Technology Dependencies

None - Uses existing markdown file capabilities.

---

## Test Strategy

### Unit Tests

**Coverage Target:** 85%+ for metrics collection logic

**Test Scenarios:**
1. **Happy Path:** Successfully capture metrics for all 10 operation types
2. **Edge Cases:**
   - Zero violations/hallucinations
   - Partial operation completion
   - Pre-existing directory
3. **Error Cases:**
   - Invalid timestamp format
   - Missing required fields
   - File permission errors

---

### Integration Tests

**Coverage Target:** 80%+

**Test Scenarios:**
1. **End-to-End Collection:** Execute all 10 operations and verify baseline document
2. **Directory Creation:** Verify proper directory structure creation
3. **File Overwrite Handling:** Test backup creation on existing file

---

## Acceptance Criteria Verification Checklist

### AC#1: Baseline Metrics Collection for /dev Operations

- [ ] /dev operation 1 metrics captured - **Phase:** 2 - **Evidence:** baseline document entry
- [ ] /dev operation 2 metrics captured - **Phase:** 2 - **Evidence:** baseline document entry
- [ ] /dev operation 3 metrics captured - **Phase:** 2 - **Evidence:** baseline document entry
- [ ] All required fields present (timestamp, story ID, violations, hallucinations, citations, duration) - **Phase:** 4 - **Evidence:** validation test

### AC#2: Baseline Metrics Collection for /qa Operations

- [ ] /qa operation 1 metrics captured - **Phase:** 2 - **Evidence:** baseline document entry
- [ ] /qa operation 2 metrics captured - **Phase:** 2 - **Evidence:** baseline document entry
- [ ] /qa operation 3 metrics captured - **Phase:** 2 - **Evidence:** baseline document entry
- [ ] Validation mode recorded (light/deep) - **Phase:** 4 - **Evidence:** validation test

### AC#3: Baseline Metrics Collection for /create-story Operations

- [ ] /create-story operation 1 metrics captured - **Phase:** 2 - **Evidence:** baseline document entry
- [ ] /create-story operation 2 metrics captured - **Phase:** 2 - **Evidence:** baseline document entry
- [ ] Feature description and AC count recorded - **Phase:** 4 - **Evidence:** validation test

### AC#4: Baseline Metrics Collection for Architecture Questions

- [ ] Architecture question 1 metrics captured - **Phase:** 2 - **Evidence:** baseline document entry
- [ ] Architecture question 2 metrics captured - **Phase:** 2 - **Evidence:** baseline document entry
- [ ] Question text and context files recorded - **Phase:** 4 - **Evidence:** validation test

### AC#5: Baseline Document Generation

- [ ] Summary statistics section generated - **Phase:** 2 - **Evidence:** baseline document
- [ ] Per-operation breakdown present (10 entries) - **Phase:** 2 - **Evidence:** baseline document
- [ ] Aggregate metrics calculated correctly - **Phase:** 4 - **Evidence:** validation test

### AC#6: Metrics Directory Structure

- [ ] Directory created with 755 permissions - **Phase:** 2 - **Evidence:** ls -la output
- [ ] README.md created - **Phase:** 2 - **Evidence:** file exists
- [ ] Baseline file created with 644 permissions - **Phase:** 2 - **Evidence:** ls -la output

---

**Checklist Progress:** 0/20 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] Metrics directory structure created (devforgeai/metrics/)
- [ ] README.md with format documentation created
- [ ] Baseline document template implemented
- [ ] All 10 operation types captured (3 /dev, 3 /qa, 2 /create-story, 2 architecture)
- [ ] Summary statistics calculated correctly
- [ ] Per-operation breakdown complete

### Quality
- [ ] All 6 acceptance criteria have passing tests
- [ ] Edge cases covered (partial completion, zero violations, pre-existing directory)
- [ ] Data validation enforced (timestamp format, rule numbers, non-negative counts)
- [ ] NFRs met (< 5s generation, < 100ms overhead, 644/755 permissions)
- [ ] Code coverage >= 85% for metrics collection logic

### Testing
- [ ] Unit tests for metric capture
- [ ] Unit tests for validation rules
- [ ] Integration tests for document generation
- [ ] Integration tests for directory handling

### Documentation
- [ ] README.md in devforgeai/metrics/ with usage guide
- [ ] Inline field descriptions in baseline document
- [ ] Format version documented

---

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Notes

**Design Decisions:**
- Using markdown format for human readability and version control compatibility
- Manual capture process (not automated) to ensure accurate observation of Claude behavior
- YAML frontmatter for machine-parseable metadata

**Research Reference:**
- RESEARCH-001: Claude Code Memory Management Best Practices (2025-11-30)
- Location: `devforgeai/research/shared/RESEARCH-001-claude-memory-best-practices.md`

**Related Stories:**
- STORY-100: Accuracy Tracking Log Setup (creates ongoing tracking log template)
- Feature 2 depends on this story completing first (baseline needed for comparison)

---

**Story Template Version:** 2.1
**Last Updated:** 2025-12-01
