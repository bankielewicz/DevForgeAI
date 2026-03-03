---
id: STORY-305
title: Refactor Complex Nested Conditional Logic in Phase 06 Step 6.6
type: refactor
epic: null
sprint: Backlog
status: QA Approved
points: 1
depends_on: ["STORY-304"]
priority: Medium
assigned_to: null
created: 2026-01-20
format_version: "2.6"
source: framework-enhancement
recommendation_source: STORY-286 QA Advisory Violations Analysis
---

# Story: Refactor Complex Nested Conditional Logic in Phase 06 Step 6.6

## Description

**As a** DevForgeAI framework maintainer,
**I want** to refactor the 11 nested conditional branches in Step 6.6 (Technical Debt Register Update Workflow) into focused helper workflows,
**so that** cyclomatic complexity is reduced, testability improves, and each file has a single responsibility.

**Background:**
The Step 6.6 workflow (to be extracted per STORY-304) contains **11 nested conditional branches** across subsections 6.6.1-6.6.11. This high cyclomatic complexity increases bug surface area and makes the logic harder to understand and maintain.

**Verified Evidence:**
- Source: devforgeai/feedback/ai-analysis/STORY-286/2026-01-20-qa-advisory-violations.md
- Conditional count: 11 branches identified
- Severity: MEDIUM (per QA advisory)

**Dependency:** This story depends on STORY-304 (Extract Technical Debt Register Workflow) being completed first, as the refactoring targets the newly extracted file.

## Acceptance Criteria

### AC#1: ID Generation Logic Extracted

```xml
<acceptance_criteria id="AC1" implements="DOC-001">
  <given>Step 6.6.3 (DEBT-NNN ID Generation) contains collision loop and empty register handling</given>
  <when>The refactoring is performed</when>
  <then>A new helper file technical-debt-id-generation.md exists containing the ID generation logic with 2-3 focused conditionals</then>
  <verification>
    <source_files>
      <file hint="New helper file">src/claude/skills/devforgeai-development/references/technical-debt-id-generation.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Type Derivation Logic Extracted

```xml
<acceptance_criteria id="AC2" implements="DOC-002">
  <given>Step 6.6.4 contains 4 conditional branches for type derivation (Story Split, Scope Change, External Blocker, default)</given>
  <when>The refactoring is performed</when>
  <then>A new helper file technical-debt-type-derivation.md exists containing the pattern matching logic for debt type classification</then>
  <verification>
    <source_files>
      <file hint="New helper file">src/claude/skills/devforgeai-development/references/technical-debt-type-derivation.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Atomic Write Logic Extracted

```xml
<acceptance_criteria id="AC3" implements="DOC-003">
  <given>Steps 6.6.7-6.6.9 contain write, rollback, and error handling logic</given>
  <when>The refactoring is performed</when>
  <then>A new helper file technical-debt-atomic-write.md exists containing the atomic write and rollback logic</then>
  <verification>
    <source_files>
      <file hint="New helper file">src/claude/skills/devforgeai-development/references/technical-debt-atomic-write.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Main Workflow Updated with Helper References

```xml
<acceptance_criteria id="AC4" implements="DOC-004">
  <given>The technical-debt-register-workflow.md file (created by STORY-304) contains all Step 6.6 logic inline</given>
  <when>The refactoring is performed</when>
  <then>The main workflow file is updated to reference the three helper files with proper cross-reference format, reducing its complexity</then>
  <verification>
    <source_files>
      <file hint="Main workflow with references">src/claude/skills/devforgeai-development/references/technical-debt-register-workflow.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Cyclomatic Complexity Reduced

```xml
<acceptance_criteria id="AC5" implements="NFR-001">
  <given>The original Step 6.6 had 11 conditional branches in one file</given>
  <when>The refactoring distributes logic across 4 files</when>
  <then>Each file has no more than 4 conditional branches (maximum cyclomatic complexity of 5 per file)</then>
  <verification>
    <source_files>
      <file hint="Main workflow">src/claude/skills/devforgeai-development/references/technical-debt-register-workflow.md</file>
      <file hint="ID generation">src/claude/skills/devforgeai-development/references/technical-debt-id-generation.md</file>
      <file hint="Type derivation">src/claude/skills/devforgeai-development/references/technical-debt-type-derivation.md</file>
      <file hint="Atomic write">src/claude/skills/devforgeai-development/references/technical-debt-atomic-write.md</file>
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
    - type: "Configuration"
      name: "technical-debt-id-generation.md"
      file_path: "src/claude/skills/devforgeai-development/references/technical-debt-id-generation.md"
      required_keys: []
      requirements:
        - id: "DOC-001"
          description: "Extract ID generation logic from Step 6.6.3 including empty register check, max ID extraction, and collision loop"
          testable: true
          test_requirement: "Test: File contains DEBT-NNN generation algorithm with collision handling"
          priority: "High"
          implements_ac: ["AC#1"]

    - type: "Configuration"
      name: "technical-debt-type-derivation.md"
      file_path: "src/claude/skills/devforgeai-development/references/technical-debt-type-derivation.md"
      required_keys: []
      requirements:
        - id: "DOC-002"
          description: "Extract type derivation pattern matching from Step 6.6.4 including Story Split, Scope Change, External Blocker detection"
          testable: true
          test_requirement: "Test: File contains IF/ELIF pattern matching for 4 debt types"
          priority: "High"
          implements_ac: ["AC#2"]

    - type: "Configuration"
      name: "technical-debt-atomic-write.md"
      file_path: "src/claude/skills/devforgeai-development/references/technical-debt-atomic-write.md"
      required_keys: []
      requirements:
        - id: "DOC-003"
          description: "Extract atomic write workflow from Steps 6.6.7-6.6.9 including backup, write, verify, and rollback logic"
          testable: true
          test_requirement: "Test: File contains atomic write sequence with rollback mechanism"
          priority: "High"
          implements_ac: ["AC#3"]

    - type: "Configuration"
      name: "technical-debt-register-workflow.md (modified)"
      file_path: "src/claude/skills/devforgeai-development/references/technical-debt-register-workflow.md"
      required_keys: []
      requirements:
        - id: "DOC-004"
          description: "Update main workflow to delegate to helper files via cross-references"
          testable: true
          test_requirement: "Test: Main file contains 3 cross-references to helper files"
          priority: "High"
          implements_ac: ["AC#4"]

  business_rules:
    - id: "BR-001"
      rule: "Each helper file must be self-contained with its own purpose statement"
      trigger: "During file creation"
      validation: "Each file starts with Purpose section"
      error_handling: "Add missing Purpose section"
      test_requirement: "Test: Each helper file has '## Purpose' heading"
      priority: "High"

    - id: "BR-002"
      rule: "Cross-references must follow coding-standards.md format"
      trigger: "When inserting references in main workflow"
      validation: "Format matches: 'For full details, see: [filename](path) (Section Name)'"
      error_handling: "Fix format before completion"
      test_requirement: "Test: Grep pattern matches template"
      priority: "High"

    - id: "BR-003"
      rule: "No functional behavior change to technical debt register workflow"
      trigger: "After refactoring complete"
      validation: "Workflow produces identical output before and after"
      error_handling: "Revert if behavior changes"
      test_requirement: "Test: Manual execution produces same DEBT-NNN entry"
      priority: "Critical"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Maintainability"
      requirement: "Reduce cyclomatic complexity per file"
      metric: "Maximum 4 conditional branches per file (down from 11 in one file)"
      test_requirement: "Test: Count IF/ELIF/ELSE patterns in each file"
      priority: "High"

    - id: "NFR-002"
      category: "Maintainability"
      requirement: "Improve single responsibility compliance"
      metric: "Each file has exactly one purpose (ID generation, type derivation, or atomic write)"
      test_requirement: "Test: File name matches content purpose"
      priority: "Medium"
```

---

## Technical Limitations

```yaml
technical_limitations: []
# No technical limitations identified
```

---

## Non-Functional Requirements (NFRs)

### Maintainability

**Cyclomatic Complexity:**
- Before: 11 conditional branches in one file
- After: Maximum 4 branches per file across 4 files
- Target: No file exceeds cyclomatic complexity of 5

**Single Responsibility:**
- Main workflow: Orchestration and sequencing
- ID generation: DEBT-NNN generation algorithm
- Type derivation: Pattern matching for debt classification
- Atomic write: File write with rollback

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-304:** Extract Technical Debt Register Workflow from Phase 06 Reference File
  - **Why:** This story refactors the file created by STORY-304
  - **Status:** QA Approved

### External Dependencies

None.

### Technology Dependencies

None.

---

## Test Strategy

### Unit Tests

**Coverage Target:** N/A (documentation story)

**Validation Scenarios:**
1. **File Existence:** All 3 helper files exist
2. **Content Correctness:** Each helper contains appropriate logic
3. **Complexity Check:** Each file has ≤4 conditional branches
4. **Cross-References:** Main file references all 3 helpers

---

### Integration Tests

**Coverage Target:** N/A (documentation story)

**Workflow Continuity Test:**
1. Execute Step 6.6 workflow with a deferred DoD item
2. Verify all helper files load correctly
3. Verify DEBT-NNN entry created correctly
4. Verify identical output to pre-refactor behavior

---

## Acceptance Criteria Verification Checklist

**Purpose:** Real-time progress tracking during implementation.

### AC#1: ID Generation Logic Extracted

- [x] Create technical-debt-id-generation.md - **Phase:** Implementation - **Evidence:** file exists
- [x] Extract 6.6.3 content - **Phase:** Implementation - **Evidence:** collision loop present

### AC#2: Type Derivation Logic Extracted

- [x] Create technical-debt-type-derivation.md - **Phase:** Implementation - **Evidence:** file exists
- [x] Extract 6.6.4 content - **Phase:** Implementation - **Evidence:** 4 type patterns present

### AC#3: Atomic Write Logic Extracted

- [x] Create technical-debt-atomic-write.md - **Phase:** Implementation - **Evidence:** file exists
- [x] Extract 6.6.7-6.6.9 content - **Phase:** Implementation - **Evidence:** rollback logic present

### AC#4: Main Workflow Updated

- [x] Add cross-references to 3 helper files - **Phase:** Implementation - **Evidence:** grep count = 3

### AC#5: Complexity Reduced

- [x] Verify ≤4 conditionals per file - **Phase:** Verification - **Evidence:** 4/4/3/4 conditionals per file

---

**Checklist Progress:** 9/9 items complete (100%)

---

## Definition of Done

### Implementation
- [x] Helper file technical-debt-id-generation.md created
- [x] Helper file technical-debt-type-derivation.md created
- [x] Helper file technical-debt-atomic-write.md created
- [x] Main workflow updated with cross-references

### Quality
- [x] All 5 acceptance criteria have passing verification
- [x] Each file has ≤4 conditional branches
- [x] Cross-references follow coding-standards.md format
- [x] No functional behavior change

### Testing
- [x] Manual verification of workflow execution
- [x] File existence checks pass
- [x] Complexity validation passes

### Documentation
- [x] Each helper file has Purpose section
- [x] Change log updated

---

## Implementation Notes

- [x] Helper file technical-debt-id-generation.md created - Completed: 2026-01-24
- [x] Helper file technical-debt-type-derivation.md created - Completed: 2026-01-24
- [x] Helper file technical-debt-atomic-write.md created - Completed: 2026-01-24
- [x] Main workflow updated with cross-references - Completed: 2026-01-24
- [x] All 5 acceptance criteria have passing verification - Completed: 2026-01-24
- [x] Each file has ≤4 conditional branches - Completed: 2026-01-24
- [x] Cross-references follow coding-standards.md format - Completed: 2026-01-24
- [x] No functional behavior change - Completed: 2026-01-24
- [x] Manual verification of workflow execution - Completed: 2026-01-24
- [x] File existence checks pass - Completed: 2026-01-24
- [x] Complexity validation passes - Completed: 2026-01-24
- [x] Each helper file has Purpose section - Completed: 2026-01-24
- [x] Change log updated - Completed: 2026-01-24

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-20 14:55 | /recommendations-triage | Created | Story created from STORY-286 QA advisory recommendations | STORY-305.story.md |
| 2026-01-24 | /dev | Dev Complete | Refactored 11 nested conditionals into 3 helper files | technical-debt-id-generation.md (NEW), technical-debt-type-derivation.md (NEW), technical-debt-atomic-write.md (NEW), technical-debt-register-workflow.md (MODIFIED) |
| 2026-01-24 | claude/qa-result-interpreter | QA Deep | PASSED: 100% traceability, 0 violations, all 5 ACs verified | STORY-305-qa-report.md |

## Notes

**Source Recommendation:**
This story was generated from the `/recommendations-triage` command processing the STORY-286 QA Advisory Violations Analysis. The MEDIUM severity finding identified 11 nested conditionals increasing cyclomatic complexity.

**Design Decisions:**
- Split by logical grouping: ID generation, type derivation, atomic write
- Keep main workflow as orchestrator that delegates to helpers
- Maintain identical functional behavior (pure refactor)

**Dependency Note:**
This story MUST be executed after STORY-304 completes, as it refactors the file created by that story.

**References:**
- devforgeai/feedback/ai-analysis/STORY-286/2026-01-20-qa-advisory-violations.md (source recommendation)
- coding-standards.md lines 224-264 (cross-reference format)

---

**Story Template Version:** 2.6
**Last Updated:** 2026-01-20
