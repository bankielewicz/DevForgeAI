---
id: STORY-270
title: XML AC Parsing Logic for Verification Subagent
type: feature
epic: EPIC-046
sprint: SPRINT-8
status: QA Approved
points: 3
depends_on: ["STORY-269"]
priority: High
assigned_to: Unassigned
created: 2026-01-19
format_version: "2.5"
---

# Story: XML AC Parsing Logic for Verification Subagent

## Description

**As a** verification subagent,
**I want** to parse XML-tagged acceptance criteria from story files,
**so that** I can systematically verify each AC one-by-one against source code.

## Acceptance Criteria

### AC#1: XML AC Block Detection

**Given** a story file with XML acceptance criteria format,
**When** the subagent reads the story file,
**Then** it correctly identifies and extracts all `<acceptance_criteria id="ACX">` blocks.

---

### AC#2: Given/When/Then Extraction

**Given** an extracted XML AC block,
**When** the subagent parses the block content,
**Then** it extracts `<given>`, `<when>`, and `<then>` child elements into structured data.

---

### AC#3: Source Files Hint Extraction

**Given** an XML AC block with optional `<verification>` element,
**When** the subagent parses the block,
**Then** it extracts `<source_files>` hints (if provided) for targeted inspection.

---

### AC#4: HALT on Missing XML Format

**Given** a story file WITHOUT XML AC format (legacy format),
**When** the subagent attempts to parse acceptance criteria,
**Then** it HALTs with error: "Story lacks required XML AC format. Update story to XML format per EPIC-046."

---

### AC#5: Multi-AC Story Support

**Given** a story file with 1-20 acceptance criteria,
**When** the subagent parses all AC blocks,
**Then** it returns a structured list of all ACs with their Given/When/Then and verification hints.

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "DataModel"
      name: "AcceptanceCriterion"
      purpose: "Structured representation of parsed AC"
      fields:
        - name: "id"
          type: "String"
          constraints: "Required, format: AC1, AC2, etc."
          description: "Unique identifier for the AC"
          test_requirement: "Test: Verify id matches regex ^AC\\d+$"
        - name: "given"
          type: "String"
          constraints: "Required"
          description: "Initial context/state"
          test_requirement: "Test: Verify given is non-empty string"
        - name: "when"
          type: "String"
          constraints: "Required"
          description: "Action/event that occurs"
          test_requirement: "Test: Verify when is non-empty string"
        - name: "then"
          type: "String"
          constraints: "Required"
          description: "Expected outcome"
          test_requirement: "Test: Verify then is non-empty string"
        - name: "source_files"
          type: "Array<String>"
          constraints: "Optional, relative paths"
          description: "Hints for source files to inspect"
          test_requirement: "Test: Verify source_files are relative paths (no absolute)"
        - name: "test_file"
          type: "String"
          constraints: "Optional"
          description: "Expected test file location"
          test_requirement: "Test: Verify test_file matches tests/STORY-XXX/ pattern"
        - name: "coverage_threshold"
          type: "Integer"
          constraints: "Optional, 0-100"
          description: "Coverage percentage target"
          test_requirement: "Test: Verify coverage_threshold is 0-100 if present"

  business_rules:
    - id: "BR-001"
      rule: "XML AC format is REQUIRED (no fallback to legacy)"
      trigger: "During story parsing"
      validation: "Story contains at least one <acceptance_criteria> block"
      error_handling: "HALT with specific error message if missing"
      test_requirement: "Test: Verify HALT when no XML AC blocks found"
      priority: "Critical"
    - id: "BR-002"
      rule: "AC IDs must be unique within story"
      trigger: "During AC collection"
      validation: "No duplicate id attributes"
      error_handling: "Warn on duplicate, use first occurrence"
      test_requirement: "Test: Verify duplicate AC IDs are detected"
      priority: "High"
    - id: "BR-003"
      rule: "Given/When/Then are mandatory for each AC"
      trigger: "During AC parsing"
      validation: "All three elements present and non-empty"
      error_handling: "Mark AC as incomplete, log warning"
      test_requirement: "Test: Verify incomplete AC flagged correctly"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Parse story file with 20 ACs"
      metric: "< 500ms for parsing"
      test_requirement: "Test: Parse 20-AC story file within 500ms"
      priority: "Medium"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "Handle malformed XML gracefully"
      metric: "No exceptions, return parse error"
      test_requirement: "Test: Malformed XML returns structured error, not exception"
      priority: "High"
```

---

## Technical Limitations

```yaml
technical_limitations: []
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Parse single AC: < 50ms
- Parse 20 ACs: < 500ms
- Story file read: < 100ms

### Reliability

**Error Handling:**
- Malformed XML: Return structured error (not exception)
- Missing elements: Mark AC incomplete, continue parsing
- HALT: Only when story has NO XML AC format

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-269:** AC Compliance Verifier Subagent Creation
  - **Why:** Parsing logic is implemented within the subagent
  - **Status:** Backlog

### Technology Dependencies

None (uses Claude's native XML understanding)

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** Parse story with 3-5 well-formed XML ACs
2. **Edge Cases:**
   - Story with 1 AC (minimum)
   - Story with 20 ACs (maximum)
   - AC with optional verification hints
   - AC without verification hints
3. **Error Cases:**
   - Story with no XML ACs (legacy format) → HALT
   - Malformed XML → structured error
   - Missing Given/When/Then → incomplete flag

---

## Acceptance Criteria Verification Checklist

### AC#1: XML AC Block Detection

- [x] Subagent identifies `<acceptance_criteria>` tags - **Phase:** 3 - **Evidence:** ac-compliance-verifier.md lines 67-79
- [x] Extracts id attribute correctly - **Phase:** 3 - **Evidence:** ac-compliance-verifier.md lines 77-79

### AC#2: Given/When/Then Extraction

- [x] Extracts `<given>` element - **Phase:** 3 - **Evidence:** ac-compliance-verifier.md lines 81-98
- [x] Extracts `<when>` element - **Phase:** 3 - **Evidence:** ac-compliance-verifier.md lines 81-98
- [x] Extracts `<then>` element - **Phase:** 3 - **Evidence:** ac-compliance-verifier.md lines 81-98

### AC#3: Source Files Hint Extraction

- [x] Extracts `<verification>` block when present - **Phase:** 3 - **Evidence:** ac-compliance-verifier.md lines 100-115
- [x] Extracts `<source_files>` list - **Phase:** 3 - **Evidence:** ac-compliance-verifier.md lines 112-114
- [x] Handles missing verification block gracefully - **Phase:** 3 - **Evidence:** ac-compliance-verifier.md line 114

### AC#4: HALT on Missing XML Format

- [x] Detects absence of XML AC format - **Phase:** 3 - **Evidence:** ac-compliance-verifier.md lines 139-154
- [x] HALTs with specific error message - **Phase:** 3 - **Evidence:** ac-compliance-verifier.md lines 145-153

### AC#5: Multi-AC Story Support

- [x] Parses stories with 1-20 ACs - **Phase:** 3 - **Evidence:** ac-compliance-verifier.md lines 162-185
- [x] Returns structured list of all ACs - **Phase:** 3 - **Evidence:** ac-compliance-verifier.md lines 166-178

---

**Checklist Progress:** 12/12 items complete (100%)

---

## Definition of Done

### Implementation
- [x] XML AC parsing logic in subagent system prompt - Completed: ac-compliance-verifier.md lines 43-186
- [x] Given/When/Then extraction working - Completed: ac-compliance-verifier.md lines 81-98
- [x] Source files hint extraction working - Completed: ac-compliance-verifier.md lines 100-115
- [x] HALT behavior on legacy format - Completed: ac-compliance-verifier.md lines 139-154

### Quality
- [x] All 5 acceptance criteria have passing tests - Completed: 5 test files in devforgeai/tests/STORY-270/
- [x] Handles 1-20 ACs correctly - Completed: ac-compliance-verifier.md line 185 documents 1-20 AC range
- [x] Error messages are clear and actionable - Completed: ac-compliance-verifier.md lines 145-153 with specific error message

### Testing
- [x] Unit tests for XML parsing - Completed: test_ac1_xml_block_detection.sh, test_ac2_given_when_then_extraction.sh
- [x] Unit tests for edge cases - Completed: test_ac3_source_files_hint_extraction.sh, test_ac4_halt_on_missing_xml.sh
- [x] Integration test with real story file - Completed: test_ac5_multi_ac_support.sh with multi-AC scenarios

### Documentation
- [x] XML AC format documented - Completed: ac-compliance-verifier.md lines 50-65 with complete XML schema
- [x] HALT error message documented - Completed: ac-compliance-verifier.md lines 145-153 with exact error text

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-01-19
**Branch:** main

- [x] XML AC parsing logic in subagent system prompt - Completed: ac-compliance-verifier.md lines 43-186
- [x] Given/When/Then extraction working - Completed: ac-compliance-verifier.md lines 81-98
- [x] Source files hint extraction working - Completed: ac-compliance-verifier.md lines 100-115
- [x] HALT behavior on legacy format - Completed: ac-compliance-verifier.md lines 139-154
- [x] All 5 acceptance criteria have passing tests - Completed: 5 test files in devforgeai/tests/STORY-270/
- [x] Handles 1-20 ACs correctly - Completed: ac-compliance-verifier.md line 185 documents 1-20 AC range
- [x] Error messages are clear and actionable - Completed: ac-compliance-verifier.md lines 145-153 with specific error message
- [x] Unit tests for XML parsing - Completed: test_ac1_xml_block_detection.sh, test_ac2_given_when_then_extraction.sh
- [x] Unit tests for edge cases - Completed: test_ac3_source_files_hint_extraction.sh, test_ac4_halt_on_missing_xml.sh
- [x] Integration test with real story file - Completed: test_ac5_multi_ac_support.sh with multi-AC scenarios
- [x] XML AC format documented - Completed: ac-compliance-verifier.md lines 50-65 with complete XML schema
- [x] HALT error message documented - Completed: ac-compliance-verifier.md lines 145-153 with exact error text

### TDD Workflow Summary

**Phase 02 (Red): Test-First Design**
- Generated 5 test files covering all 5 acceptance criteria
- Tests placed in devforgeai/tests/STORY-270/
- Test runner: run-all-tests.sh with summary reporting

**Phase 03 (Green): Implementation**
- Implemented XML AC parsing protocol in ac-compliance-verifier.md
- Added 6-step XML parsing workflow (detect, extract GWT, extract hints, build model, HALT check, multi-AC)
- AcceptanceCriterion data model with all required fields

**Phase 04 (Refactor): Code Quality**
- Structured documentation with clear sections
- Business rules (BR-001 through BR-003) documented
- Error handling with graceful degradation

**Phase 05 (Integration): Full Validation**
- Integration test validates end-to-end AC parsing
- Multi-AC support verified (1-20 ACs)

### Files Created/Modified

**Modified:**
- .claude/agents/ac-compliance-verifier.md (XML AC Parsing Protocol section added)

**Created:**
- devforgeai/tests/STORY-270/test_ac1_xml_block_detection.sh
- devforgeai/tests/STORY-270/test_ac2_given_when_then_extraction.sh
- devforgeai/tests/STORY-270/test_ac3_source_files_hint_extraction.sh
- devforgeai/tests/STORY-270/test_ac4_halt_on_missing_xml.sh
- devforgeai/tests/STORY-270/test_ac5_multi_ac_support.sh
- devforgeai/tests/STORY-270/run-all-tests.sh

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-19 14:35 | claude/devforgeai-story-creation | Created | Story created from EPIC-046 Feature 1.2 | STORY-270.story.md |
| 2026-01-19 19:27 | claude/test-automator | Red (Phase 02) | Tests generated for all 5 ACs | devforgeai/tests/STORY-270/*.sh |
| 2026-01-19 19:55 | claude/backend-architect | Green (Phase 03) | XML AC parsing protocol implemented | .claude/agents/ac-compliance-verifier.md |
| 2026-01-19 20:03 | claude/refactoring-specialist | Refactor (Phase 04) | Code quality improvements, documentation | .claude/agents/ac-compliance-verifier.md |
| 2026-01-19 20:05 | claude/integration-tester | Integration (Phase 05) | Integration validation complete | devforgeai/tests/STORY-270/run-all-tests.sh |
| 2026-01-19 20:10 | claude/opus | DoD Update (Phase 07) | Development complete, DoD validated | STORY-270.story.md |
| 2026-01-19 20:27 | claude/qa-result-interpreter | QA Deep | PASSED: 3/3 validators, 0 blocking violations | STORY-270-qa-report.md |

## Notes

**Design Decisions:**
- XML format chosen over markdown headers for machine-readable parsing
- HALT on legacy format enforces migration (no graceful degradation per user preference)
- Optional verification hints allow progressive adoption

**References:**
- EPIC-046: AC Compliance Verification System
- EPIC-046 Requirements: Section 4 (Data Model)
