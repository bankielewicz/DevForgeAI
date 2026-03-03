---
id: STORY-271
title: Source Code Inspection Workflow for AC Verification
type: feature
epic: EPIC-046
sprint: SPRINT-8
status: QA Approved
points: 3
depends_on: ["STORY-270"]
priority: High
assigned_to: Unassigned
created: 2026-01-19
format_version: "2.5"
---

# Story: Source Code Inspection Workflow for AC Verification

## Description

**As a** verification subagent,
**I want** to read and inspect actual source code files,
**so that** I can verify the code implements the AC requirements with documented evidence.

## Acceptance Criteria

### AC#1: Source File Loading via Read Tool

**Given** an AC with source_files hints (or derived locations),
**When** the subagent begins verification,
**Then** it uses Read() tool to load the source file contents for inspection.

---

### AC#2: Implementation Pattern Search

**Given** loaded source code and AC requirements,
**When** the subagent analyzes the code,
**Then** it searches for implementation patterns that match the AC's Given/When/Then requirements.

---

### AC#3: Specific Evidence Documentation

**Given** found implementation patterns,
**When** the subagent completes inspection,
**Then** it documents evidence including: file path, line numbers, and relevant code snippets.

---

### AC#4: Source File Discovery Without Hints

**Given** an AC WITHOUT source_files hints,
**When** the subagent needs to locate implementation,
**Then** it uses Glob() and Grep() to discover likely source files based on AC keywords.

---

### AC#5: Multiple File Inspection

**Given** an AC that spans multiple source files,
**When** the subagent verifies the AC,
**Then** it inspects all relevant files and aggregates evidence across them.

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "DataModel"
      name: "SourceInspectionResult"
      purpose: "Evidence from source code inspection"
      fields:
        - name: "ac_id"
          type: "String"
          constraints: "Required"
          description: "AC being verified"
          test_requirement: "Test: Verify ac_id matches source AC"
        - name: "files_inspected"
          type: "Array<FileEvidence>"
          constraints: "Required, minimum 1"
          description: "List of inspected files with evidence"
          test_requirement: "Test: Verify at least 1 file inspected per AC"
        - name: "implementation_found"
          type: "Boolean"
          constraints: "Required"
          description: "Whether implementation matching AC was found"
          test_requirement: "Test: Verify boolean is set correctly"
        - name: "confidence"
          type: "String"
          constraints: "Enum: HIGH, MEDIUM, LOW"
          description: "Confidence level in verification"
          test_requirement: "Test: Verify confidence is valid enum value"

    - type: "DataModel"
      name: "FileEvidence"
      purpose: "Evidence from single file inspection"
      fields:
        - name: "file_path"
          type: "String"
          constraints: "Required, relative path"
          description: "Path to inspected file"
          test_requirement: "Test: Verify path is relative (no absolute)"
        - name: "lines"
          type: "Array<Integer>"
          constraints: "Optional"
          description: "Relevant line numbers"
          test_requirement: "Test: Verify line numbers are positive integers"
        - name: "code_snippet"
          type: "String"
          constraints: "Optional, max 500 chars"
          description: "Relevant code excerpt"
          test_requirement: "Test: Verify snippet < 500 chars"
        - name: "match_type"
          type: "String"
          constraints: "Enum: DIRECT, INFERRED, PARTIAL"
          description: "How well code matches AC"
          test_requirement: "Test: Verify match_type is valid enum"

  business_rules:
    - id: "BR-001"
      rule: "All evidence must reference specific file locations"
      trigger: "During evidence documentation"
      validation: "Every FileEvidence has file_path set"
      error_handling: "Fail verification if no file evidence"
      test_requirement: "Test: Verify verification fails without file evidence"
      priority: "Critical"
    - id: "BR-002"
      rule: "Discovery fallback when no hints provided"
      trigger: "When source_files hint is empty"
      validation: "Subagent uses Glob/Grep to find files"
      error_handling: "Mark as LOW confidence if discovery-based"
      test_requirement: "Test: Verify discovery mode sets LOW/MEDIUM confidence"
      priority: "High"
    - id: "BR-003"
      rule: "Read-only inspection (no modifications)"
      trigger: "During all inspection operations"
      validation: "Only Read, Grep, Glob tools used"
      error_handling: "N/A - enforced by tool restriction"
      test_requirement: "Test: Verify no Write/Edit in inspection workflow"
      priority: "Critical"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Inspect single file"
      metric: "< 2 seconds per file"
      test_requirement: "Test: Single file inspection completes in 2s"
      priority: "Medium"
    - id: "NFR-002"
      category: "Performance"
      requirement: "Total inspection per AC"
      metric: "< 15 seconds for AC with 5 files"
      test_requirement: "Test: 5-file AC inspection in 15s"
      priority: "Medium"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Single file Read(): < 500ms
- Grep search: < 1s per pattern
- Total per-AC inspection: < 15s (for 5 files)

### Reliability

**Error Handling:**
- File not found: Log warning, continue with other files
- Empty file: Log as inspected with no evidence
- Large file (>10K lines): Inspect first 2000 lines, note limitation

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-270:** XML AC Parsing Logic
  - **Why:** Need parsed AC with Given/When/Then to know what to look for
  - **Status:** Backlog

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** Inspect file with clear implementation
2. **Edge Cases:**
   - No source_files hints (discovery mode)
   - Multiple files per AC
   - Implementation across multiple files
3. **Error Cases:**
   - Source file not found
   - Empty source file
   - Very large source file

---

## Acceptance Criteria Verification Checklist

### AC#1: Source File Loading

- [x] Read() tool loads file content - **Phase:** 3 - **Evidence:** Step 1 in Source Code Inspection Workflow
- [x] Handles file not found gracefully - **Phase:** 3 - **Evidence:** Error handling documented in workflow

### AC#2: Implementation Pattern Search

- [x] Searches for AC-related patterns - **Phase:** 3 - **Evidence:** Step 2 with Grep patterns
- [x] Identifies implementation matches - **Phase:** 3 - **Evidence:** Match type classification table

### AC#3: Evidence Documentation

- [x] Documents file path - **Phase:** 3 - **Evidence:** FileEvidence.file_path field documented
- [x] Documents line numbers - **Phase:** 3 - **Evidence:** FileEvidence.lines field documented
- [x] Documents code snippets - **Phase:** 3 - **Evidence:** FileEvidence.code_snippet field documented

### AC#4: Discovery Without Hints

- [x] Uses Glob() for file discovery - **Phase:** 3 - **Evidence:** Discovery fallback workflow with Glob patterns
- [x] Uses Grep() for content search - **Phase:** 3 - **Evidence:** Discovery fallback workflow with Grep
- [x] Sets lower confidence for discovery - **Phase:** 3 - **Evidence:** BR-002 enforcement documented

### AC#5: Multiple File Inspection

- [x] Inspects multiple files per AC - **Phase:** 3 - **Evidence:** Step 4 multi-file workflow
- [x] Aggregates evidence - **Phase:** 3 - **Evidence:** SourceInspectionResult with files_inspected array

---

**Checklist Progress:** 14/14 items complete (100%)

---

## Definition of Done

### Implementation
- [x] Source file loading via Read() implemented - Completed: Step 1 in Source Code Inspection Workflow section
- [x] Pattern search workflow implemented - Completed: Step 2 with Given/When/Then pattern search
- [x] Evidence documentation with file/line/snippet - Completed: FileEvidence data model with all fields
- [x] Discovery fallback with Glob/Grep - Completed: Step 1 fallback workflow documented

### Quality
- [x] All 5 acceptance criteria have passing tests - Completed: 9/9 tests passing (100%)
- [x] Evidence includes specific line numbers - Completed: FileEvidence.lines field documented
- [x] Confidence levels correctly assigned - Completed: Step 5 with HIGH/MEDIUM/LOW enum

### Testing
- [x] Unit tests for file inspection - Completed: test-ac1-source-file-loading.sh
- [x] Unit tests for discovery mode - Completed: test-ac4-discovery-without-hints.sh
- [x] Integration test with real source files - Completed: Integration validation passed

### Documentation
- [x] Inspection workflow documented in subagent prompt - Completed: ## Source Code Inspection Workflow section added

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent (claude/opus)
**Implemented:** 2026-01-19
**Branch:** main

- [x] Source file loading via Read() implemented - Completed: Step 1 in Source Code Inspection Workflow section
- [x] Pattern search workflow implemented - Completed: Step 2 with Given/When/Then pattern search
- [x] Evidence documentation with file/line/snippet - Completed: FileEvidence data model with all fields
- [x] Discovery fallback with Glob/Grep - Completed: Step 1 fallback workflow documented
- [x] All 5 acceptance criteria have passing tests - Completed: 9/9 tests passing (100%)
- [x] Evidence includes specific line numbers - Completed: FileEvidence.lines field documented
- [x] Confidence levels correctly assigned - Completed: Step 5 with HIGH/MEDIUM/LOW enum
- [x] Unit tests for file inspection - Completed: test-ac1-source-file-loading.sh
- [x] Unit tests for discovery mode - Completed: test-ac4-discovery-without-hints.sh
- [x] Integration test with real source files - Completed: Integration validation passed
- [x] Inspection workflow documented in subagent prompt - Completed: ## Source Code Inspection Workflow section added

### TDD Workflow Summary

**Phase 02 (Red): Test-First Design**
- Generated 9 comprehensive tests covering all 5 acceptance criteria
- Tests placed in devforgeai/tests/STORY-271/
- All tests follow Bash validation pattern
- Test framework: Bash scripting (Claude Code native)

**Phase 03 (Green): Implementation**
- Implemented Source Code Inspection Workflow section via backend-architect subagent
- Added FileEvidence and SourceInspectionResult data models
- Added discovery fallback, confidence levels, and performance requirements
- All 9 tests passing (100% pass rate)

**Phase 04 (Refactor): Code Quality**
- Code review passed with minor suggestions (non-blocking)
- Refactoring specialist identified potential consolidation (optional)
- All tests remain green after review

**Phase 05 (Integration): Full Validation**
- Integration testing verified cross-component interactions
- Data flow validated: XML AC Parsing → Source Inspection → Verification Report
- No regressions introduced

### Files Created/Modified

**Modified:**
- .claude/agents/ac-compliance-verifier.md (Source Code Inspection Workflow added)

**Created:**
- devforgeai/tests/STORY-271/run-all-tests.sh
- devforgeai/tests/STORY-271/test-ac1-source-file-loading.sh
- devforgeai/tests/STORY-271/test-ac2-implementation-pattern-search.sh
- devforgeai/tests/STORY-271/test-ac3-evidence-documentation.sh
- devforgeai/tests/STORY-271/test-ac4-discovery-without-hints.sh
- devforgeai/tests/STORY-271/test-ac5-multiple-file-inspection.sh
- devforgeai/tests/STORY-271/test-br001-file-location-required.sh
- devforgeai/tests/STORY-271/test-br002-discovery-fallback.sh
- devforgeai/tests/STORY-271/test-br003-read-only-inspection.sh
- devforgeai/tests/STORY-271/test-nfr001-performance.sh

### Test Results

- **Total tests:** 9
- **Pass rate:** 100%
- **Coverage:** All 5 ACs + 3 BRs + 1 NFR covered

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-19 14:40 | claude/devforgeai-story-creation | Created | Story created from EPIC-046 Feature 1.3 | STORY-271.story.md |
| 2026-01-19 | claude/test-automator | Red (Phase 02) | Tests generated: 9 tests covering all ACs | devforgeai/tests/STORY-271/*.sh |
| 2026-01-19 | claude/backend-architect | Green (Phase 03) | Source Inspection Workflow implemented | .claude/agents/ac-compliance-verifier.md |
| 2026-01-19 | claude/code-reviewer | Refactor (Phase 04) | Code review completed | ac-compliance-verifier.md |
| 2026-01-19 | claude/integration-tester | Integration (Phase 05) | Integration validation passed | integration-validation-STORY-271.json |
| 2026-01-19 | claude/opus | DoD Update (Phase 07) | Development complete, DoD validated | STORY-271.story.md |
| 2026-01-19 | claude/qa-result-interpreter | QA Deep | PASSED: 9/9 tests, 0 violations, 3/3 validators | STORY-271-qa-report.md |

## Notes

**Design Decisions:**
- Discovery fallback enables verification even without explicit hints
- Confidence levels (HIGH/MEDIUM/LOW) communicate reliability of verification
- Line number evidence enables precise audit trail

**References:**
- EPIC-046: AC Compliance Verification System
- US-1.3 from requirements specification
