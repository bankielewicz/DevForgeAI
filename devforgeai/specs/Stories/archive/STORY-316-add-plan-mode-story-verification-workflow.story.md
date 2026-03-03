---
id: STORY-316
title: Add Ground Truth Verification to Plan Mode Workflows
type: documentation
epic: null
sprint: Backlog
status: QA Approved
points: 1
depends_on: ["STORY-315"]
priority: High
created: 2026-01-25
updated: 2026-01-25
format_version: "2.7"
source_rca: RCA-028
source_recommendation: REC-2
---

# STORY-316: Add Ground Truth Verification to Plan Mode Workflows

## Description

**As a** DevForgeAI user or Claude agent creating stories from plan files,
**I want** mandatory verification requirements in plan mode workflows,
**so that** even when skill usage is bypassed, ground truth verification still occurs.

**Source:** RCA-028 (Manual Story Creation Ground Truth Validation Failure)

---

## Provenance

```xml
<provenance>
  <origin document="RCA-028" section="Recommendations">
    <quote>"HIGH: REC-2 - Add Ground Truth Verification to Plan Mode Workflows"</quote>
    <line_reference>devforgeai/RCA/RCA-028-manual-story-creation-ground-truth-validation-failure.md, lines 253-302</line_reference>
    <quantified_impact>Ensures verification even when skill bypassed</quantified_impact>
  </origin>
  <decision rationale="Defense in depth">
    <selected>Create new rule file with verification requirements</selected>
    <rejected>Rely only on CLAUDE.md guidance (single point of failure)</rejected>
    <trade_off>Additional file to maintain, but provides fallback protection</trade_off>
  </decision>
</provenance>
```

---

## Acceptance Criteria

### AC#1: Rule file created at correct location

```xml
<acceptance_criteria id="AC1">
  <given>DevForgeAI framework</given>
  <when>Plan mode story creation occurs</when>
  <then>Rule file exists at src/claude/rules/workflow/plan-mode-story-creation.md</then>
  <verification>
    <source_files>
      <file hint="Rule file">src/claude/rules/workflow/plan-mode-story-creation.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Target file verification documented

```xml
<acceptance_criteria id="AC2">
  <given>The plan-mode-story-creation.md rule file</given>
  <when>Read by Claude agent</when>
  <then>It contains verification step: "Read(file_path=file)" for each target file with HALT on not found</then>
  <verification>
    <source_files>
      <file hint="Rule file">src/claude/rules/workflow/plan-mode-story-creation.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

---

### AC#3: source-tree.md verification documented

```xml
<acceptance_criteria id="AC3">
  <given>The plan-mode-story-creation.md rule file</given>
  <when>Read by Claude agent</when>
  <then>It contains verification step: Compare test paths against source-tree.md patterns</then>
  <verification>
    <source_files>
      <file hint="Rule file">src/claude/rules/workflow/plan-mode-story-creation.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Git status check for deleted files documented

```xml
<acceptance_criteria id="AC4">
  <given>The plan-mode-story-creation.md rule file</given>
  <when>Read by Claude agent</when>
  <then>It contains verification step: Check git status for deleted files ("D " prefix)</then>
  <verification>
    <source_files>
      <file hint="Rule file">src/claude/rules/workflow/plan-mode-story-creation.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Documentation"
      name: "Plan Mode Story Creation Rule"
      file_path: "src/claude/rules/workflow/plan-mode-story-creation.md"
      requirements:
        - id: "DOC-001"
          description: "Create rule file with Pre-Flight Verification section"
          testable: true
          test_requirement: "Test: File exists at src/claude/rules/workflow/plan-mode-story-creation.md"
          priority: "Critical"
        - id: "DOC-002"
          description: "Document target file verification with Read() and HALT"
          testable: true
          test_requirement: "Test: Grep for 'Verify Target Files Exist' and 'HALT'"
          priority: "Critical"
        - id: "DOC-003"
          description: "Document source-tree.md verification"
          testable: true
          test_requirement: "Test: Grep for 'source-tree.md' and 'test_path'"
          priority: "High"
        - id: "DOC-004"
          description: "Document git status deleted file check"
          testable: true
          test_requirement: "Test: Grep for 'git status' and 'deleted'"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "Any verification failure must HALT story creation"
      test_requirement: "Test: HALT trigger clearly documented"
```

---

## Content to Create

**File:** `src/claude/rules/workflow/plan-mode-story-creation.md`

```markdown
# Plan Mode Story Creation Verification

**Purpose:** Ensure ground truth verification when creating stories from plan specifications

**Trigger:** Before creating ANY story file from plan specifications

**Reference:** RCA-028 (Manual Story Creation Ground Truth Validation Failure)

---

## Pre-Flight Verification (MANDATORY)

Before creating ANY story file from plan specifications, execute these verification steps:

### 1. Verify Target Files Exist

```
FOR each file in story.files_to_modify:
  Read(file_path=file)

  IF file doesn't exist (Read fails):
    HALT: """
    ❌ CRITICAL: Target file not found

    File: {file}
    Story: {story_id}

    Cannot create story with invalid file reference.
    Either:
    1. Fix the file path in plan specifications
    2. Remove the reference if file no longer needed
    3. Create the file if it should exist
    """
```

### 2. Verify Test Paths Against source-tree.md

```
Read(file_path="devforgeai/specs/context/source-tree.md")

FOR each test_path in story.test_files:
  IF test_path pattern not found in source_tree.md:
    HALT: """
    ❌ CRITICAL: Test path not in source-tree.md

    Path: {test_path}
    Story: {story_id}

    Test paths must follow patterns documented in source-tree.md.
    Either:
    1. Use a documented test path pattern
    2. Update source-tree.md to include this pattern (requires ADR)
    """
```

### 3. Check Git Status for Deleted Files

```
Review git status header in conversation context

Extract deleted files: lines matching "^D " or "^ D " pattern

FOR each referenced_file in story:
  IF referenced_file in deleted_files:
    HALT: """
    ❌ CRITICAL: Referenced file is deleted

    File: {referenced_file}
    Git Status: D (deleted)
    Story: {story_id}

    Cannot reference deleted files in story specifications.
    Either:
    1. Update story to use existing file
    2. Document that file needs to be recreated
    3. Remove reference from story
    """
```

---

## HALT Trigger Summary

**If ANY verification fails:**
- Do NOT create story file
- Display specific error message
- Suggest using `/create-story` skill instead (has built-in validation)

**Success Criteria:**
- All target files exist and readable
- All test paths match source-tree.md patterns
- No references to deleted files

---

## Reference

- **RCA-028:** Manual Story Creation Ground Truth Validation Failure
- **citation-requirements.md:** Read-Quote-Cite-Verify protocol
- **source-tree.md:** Canonical test path patterns
```

---

## Definition of Done

### Implementation
- [x] Rule file created at src/claude/rules/workflow/plan-mode-story-creation.md - Completed: File created with 90 lines documenting all verification steps
- [x] Three verification steps documented - Completed: Sections 1 (Target Files), 2 (Test Paths), 3 (Git Status) all present
- [x] HALT triggers clearly specified - Completed: 4 HALT triggers documented with clear error messages
- [x] Error messages actionable - Completed: Each HALT includes resolution options (fix, remove, or create)

### Testing
- [x] File exists at correct location - Completed: test -f confirms file at src/claude/rules/workflow/plan-mode-story-creation.md
- [x] Grep confirms all verification steps present - Completed: 12/12 validation tests pass (TEST-SPECIFICATION.md)
- [x] Manual test: Create plan with invalid reference, verify guidance triggers - Completed: Validation documented in devforgeai/tests/STORY-316/manual-test-invalid-reference.md, all patterns verified via grep

### Documentation
- [x] RCA-028 updated with "Implemented in: STORY-316" - Completed: RCA-028 line 255 contains "**Implemented in:** STORY-316"

---

## AC Verification Checklist

### AC#1: Rule file created
- [x] File exists at correct path - **Phase:** 3 - **Evidence:** File exists at src/claude/rules/workflow/plan-mode-story-creation.md (90 lines)

### AC#2: Target file verification
- [x] Read() and HALT documented - **Phase:** 3 - **Evidence:** Lines 19, 22: Read(file_path=file) and HALT trigger

### AC#3: source-tree.md verification
- [x] Pattern comparison documented - **Phase:** 3 - **Evidence:** Lines 30-43: source-tree.md verification with HALT

### AC#4: Git status check
- [x] Deleted file check documented - **Phase:** 3 - **Evidence:** Lines 45-62: "D " pattern check with HALT

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-01-26
**Branch:** main

- [x] Rule file created at src/claude/rules/workflow/plan-mode-story-creation.md - Completed: File created with 90 lines documenting all verification steps
- [x] Three verification steps documented - Completed: Sections 1 (Target Files), 2 (Test Paths), 3 (Git Status) all present
- [x] HALT triggers clearly specified - Completed: 4 HALT triggers documented with clear error messages
- [x] Error messages actionable - Completed: Each HALT includes resolution options (fix, remove, or create)
- [x] File exists at correct location - Completed: test -f confirms file at src/claude/rules/workflow/plan-mode-story-creation.md
- [x] Grep confirms all verification steps present - Completed: 12/12 validation tests pass (TEST-SPECIFICATION.md)
- [x] Manual test: Create plan with invalid reference, verify guidance triggers - Completed: Validation documented in devforgeai/tests/STORY-316/manual-test-invalid-reference.md
- [x] RCA-028 updated with "Implemented in: STORY-316" - Completed: RCA-028 line 255 contains "**Implemented in:** STORY-316"

### TDD Workflow Summary

**Phase 02 (Red):** Generated test specification document with 12 validation tests for Markdown structure
**Phase 03 (Green):** Created rule file with 3 verification steps and 4 HALT triggers
**Phase 04 (Refactor):** Improved documentation structure, added version info and full reference paths
**Phase 05 (Integration):** Validated cross-references (4/4 files exist), file location correct
**Phase 06 (Deferral):** No deferrals - user chose to implement manual test immediately

### Files Created

- `src/claude/rules/workflow/plan-mode-story-creation.md` (90 lines)
- `devforgeai/tests/STORY-316/TEST-SPECIFICATION.md` (test spec)
- `devforgeai/tests/STORY-316/run-tests.sh` (test runner)
- `devforgeai/tests/STORY-316/manual-test-invalid-reference.md` (manual test validation)

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-25 | claude/opus | Created | Story created from RCA-028 REC-2 | STORY-316 |
| 2026-01-26 | claude/opus | DoD Update (Phase 07) | Development complete, all DoD items validated | STORY-316, src/claude/rules/workflow/plan-mode-story-creation.md |
| 2026-01-26 | claude/qa-result-interpreter | QA Deep | PASSED: 12/12 tests, 0 violations, 100% traceability | - |

---

## Notes

**Source RCA:** RCA-028: Manual Story Creation Ground Truth Validation Failure
**Recommendation ID:** REC-2 (HIGH)
**Estimated Effort:** 1 hour
**Depends on:** STORY-315 (CLAUDE.md guidance should be in place first)

**References:**
- devforgeai/RCA/RCA-028-manual-story-creation-ground-truth-validation-failure.md
- src/claude/rules/workflow/
