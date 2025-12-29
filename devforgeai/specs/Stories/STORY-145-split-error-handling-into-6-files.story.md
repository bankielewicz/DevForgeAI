---
id: STORY-145
title: Split error-handling.md into 6 Error-Type Files
epic: EPIC-030
sprint: Backlog
status: Dev Complete
points: 6
depends_on: []
priority: High
assigned_to: claude/opus
created: 2025-12-22
format_version: "2.3"
---

# Story: Split error-handling.md into 6 Error-Type Files

## Description

**As a** developer debugging errors,
**I want** to load ONLY the error type I'm handling (token efficiency),
**so that** I can quickly find relevant recovery procedures without loading the entire 1,062-line error-handling.md file.

## Acceptance Criteria

### AC#1: error-handling.md split into 6 error-type files

**Given** error-handling.md contains ~1,062 lines covering multiple error types,
**When** the file is split by error type,
**Then** 6 new files are created:
1. `error-type-1-incomplete-answers.md` (~180 lines)
2. `error-type-2-artifact-failures.md` (~200 lines)
3. `error-type-3-complexity-errors.md` (~150 lines)
4. `error-type-4-validation-failures.md` (~180 lines)
5. `error-type-5-constraint-conflicts.md` (~170 lines)
6. `error-type-6-directory-issues.md` (~180 lines)

---

### AC#2: Each error-type file is self-contained

**Given** an error-type file exists (e.g., error-type-1-incomplete-answers.md),
**When** the file is loaded during error handling,
**Then** it contains:
- Error detection logic (when does this error occur?)
- Recovery procedures (self-heal → retry → report)
- Example scenarios
- Related patterns (cross-reference to other error types if needed)

---

### AC#3: Master index file created

**Given** error-handling.md has been split into 6 files,
**When** developers need to identify which error type they're experiencing,
**Then** `error-handling-index.md` exists with:
- Decision tree: "Which error type am I experiencing?"
- Quick reference table mapping symptoms to error types
- Links to each of the 6 error-type files

---

### AC#4: SKILL.md references updated

**Given** SKILL.md previously referenced single error-handling.md,
**When** the "Error Handling" section is updated,
**Then** it lists all 6 error-type files instead of the single file.

---

### AC#5: All original content preserved

**Given** error-handling.md contained ~1,062 lines,
**When** content is distributed across 6 files + index,
**Then** total line count across all 7 files equals or exceeds original (no content loss).

---

### AC#6: Each file stays under 250 lines

**Given** target file size is <250 lines for maintainability,
**When** line counts are checked for each error-type file,
**Then** no file exceeds 250 lines.

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  reference_files:
    skill_to_modify: ".claude/skills/devforgeai-ideation/SKILL.md"
    error_handling_source: ".claude/skills/devforgeai-ideation/references/error-handling.md"

  source_file_verified:
    description: "Error-handling.md verified during story creation (2025-12-22)"
    file_path: ".claude/skills/devforgeai-ideation/references/error-handling.md"
    line_count: 1062
    status: "verified - exactly 1,062 lines"

  files_to_create:
    - path: ".claude/skills/devforgeai-ideation/references/error-type-1-incomplete-answers.md"
      target_lines: "~180"
    - path: ".claude/skills/devforgeai-ideation/references/error-type-2-artifact-failures.md"
      target_lines: "~200"
    - path: ".claude/skills/devforgeai-ideation/references/error-type-3-complexity-errors.md"
      target_lines: "~150"
    - path: ".claude/skills/devforgeai-ideation/references/error-type-4-validation-failures.md"
      target_lines: "~180"
    - path: ".claude/skills/devforgeai-ideation/references/error-type-5-constraint-conflicts.md"
      target_lines: "~170"
    - path: ".claude/skills/devforgeai-ideation/references/error-type-6-directory-issues.md"
      target_lines: "~180"
    - path: ".claude/skills/devforgeai-ideation/references/error-handling-index.md"
      target_lines: "~50"
      description: "Decision tree index to 6 error-type files"

  components:
    - type: "Configuration"
      name: "error-type-1-incomplete-answers.md"
      file_path: ".claude/skills/devforgeai-ideation/references/error-type-1-incomplete-answers.md"
      requirements:
        - id: "CFG-001"
          description: "Contains detection logic, recovery procedures, examples for incomplete answer errors"
          testable: true
          test_requirement: "Test: File exists with required sections"
          priority: "Critical"
        - id: "CFG-002"
          description: "File size < 250 lines"
          testable: true
          test_requirement: "Test: wc -l < 250"
          priority: "High"

    - type: "Configuration"
      name: "error-type-2-artifact-failures.md"
      file_path: ".claude/skills/devforgeai-ideation/references/error-type-2-artifact-failures.md"
      requirements:
        - id: "CFG-003"
          description: "Contains detection logic, recovery procedures, examples for artifact failure errors"
          testable: true
          test_requirement: "Test: File exists with required sections"
          priority: "Critical"
        - id: "CFG-004"
          description: "File size < 250 lines"
          testable: true
          test_requirement: "Test: wc -l < 250"
          priority: "High"

    - type: "Configuration"
      name: "error-type-3-complexity-errors.md"
      file_path: ".claude/skills/devforgeai-ideation/references/error-type-3-complexity-errors.md"
      requirements:
        - id: "CFG-005"
          description: "Contains detection logic, recovery procedures, examples for complexity errors"
          testable: true
          test_requirement: "Test: File exists with required sections"
          priority: "Critical"
        - id: "CFG-006"
          description: "File size < 250 lines"
          testable: true
          test_requirement: "Test: wc -l < 250"
          priority: "High"

    - type: "Configuration"
      name: "error-type-4-validation-failures.md"
      file_path: ".claude/skills/devforgeai-ideation/references/error-type-4-validation-failures.md"
      requirements:
        - id: "CFG-007"
          description: "Contains detection logic, recovery procedures, examples for validation failure errors"
          testable: true
          test_requirement: "Test: File exists with required sections"
          priority: "Critical"
        - id: "CFG-008"
          description: "File size < 250 lines"
          testable: true
          test_requirement: "Test: wc -l < 250"
          priority: "High"

    - type: "Configuration"
      name: "error-type-5-constraint-conflicts.md"
      file_path: ".claude/skills/devforgeai-ideation/references/error-type-5-constraint-conflicts.md"
      requirements:
        - id: "CFG-009"
          description: "Contains detection logic, recovery procedures, examples for constraint conflict errors"
          testable: true
          test_requirement: "Test: File exists with required sections"
          priority: "Critical"
        - id: "CFG-010"
          description: "File size < 250 lines"
          testable: true
          test_requirement: "Test: wc -l < 250"
          priority: "High"

    - type: "Configuration"
      name: "error-type-6-directory-issues.md"
      file_path: ".claude/skills/devforgeai-ideation/references/error-type-6-directory-issues.md"
      requirements:
        - id: "CFG-011"
          description: "Contains detection logic, recovery procedures, examples for directory issue errors"
          testable: true
          test_requirement: "Test: File exists with required sections"
          priority: "Critical"
        - id: "CFG-012"
          description: "File size < 250 lines"
          testable: true
          test_requirement: "Test: wc -l < 250"
          priority: "High"

    - type: "Configuration"
      name: "error-handling-index.md"
      file_path: ".claude/skills/devforgeai-ideation/references/error-handling-index.md"
      requirements:
        - id: "CFG-013"
          description: "Contains decision tree for error type identification"
          testable: true
          test_requirement: "Test: File contains decision tree section"
          priority: "Critical"
        - id: "CFG-014"
          description: "Links to all 6 error-type files"
          testable: true
          test_requirement: "Test: All 6 error-type files referenced"
          priority: "Critical"

    - type: "Configuration"
      name: "SKILL.md"
      file_path: ".claude/skills/devforgeai-ideation/SKILL.md"
      requirements:
        - id: "CFG-015"
          description: "Error Handling section lists all 6 error-type files"
          testable: true
          test_requirement: "Test: SKILL.md references 6 error-type files"
          priority: "Critical"

  business_rules:
    - id: "BR-001"
      rule: "No content loss during split (total lines >= original)"
      test_requirement: "Test: Sum of all file line counts >= 1,062"

    - id: "BR-002"
      rule: "Each error-type file must be self-contained"
      test_requirement: "Test: Each file has detection, recovery, examples sections"

    - id: "BR-003"
      rule: "Cross-references use relative links"
      test_requirement: "Test: Links use format [Text](error-type-N-name.md)"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Token efficiency through selective loading"
      metric: "Load only 150-250 tokens for specific error type vs 1,062 for full file"
      test_requirement: "Test: Single error-type file < 250 lines"

    - id: "NFR-002"
      category: "Maintainability"
      requirement: "Manageable file sizes"
      metric: "Each file < 250 lines"
      test_requirement: "Test: wc -l for each file"
```

## Technical Limitations

```yaml
technical_limitations: []
# No technical limitations identified for this story
```

## Edge Cases

1. **Content overlap between error types:** Some errors may have overlapping recovery procedures. Use cross-references rather than duplicating content.

2. **Error type not matching any category:** Include a "General Errors" section in the index pointing to the most relevant error-type file.

3. **Line count variance:** Target line counts are approximate. Actual distribution may vary based on content organization.

4. **Original file references elsewhere:** If error-handling.md is referenced outside ideation skill, update those references to point to index.

## Data Validation Rules

1. **Total content preserved:** Sum of lines across 7 new files >= original 1,062 lines.

2. **File naming convention:** Files must follow pattern `error-type-N-description.md` where N is 1-6.

3. **Required sections per file:**
   - ## Error Detection
   - ## Recovery Procedures
   - ## Example Scenarios
   - ## Related Patterns (optional)

4. **Index structure:** Decision tree must use bullet points or numbered steps for clarity.

## Non-Functional Requirements

### Performance
- Selective loading: Single error-type file <250 lines vs full 1,062 lines
- Token efficiency: 4x-7x reduction in tokens when loading single error type

### Maintainability
- Each file independently maintainable
- Clear file organization by error category
- Easy to add new error types (create error-type-7-*.md)

### Reliability
- No content loss during split
- All cross-references resolve correctly
- Index provides clear decision path

## UI Specification

N/A - This story involves file restructuring and documentation. No user interface changes required.

## Definition of Done

### Implementation
- [x] error-handling.md content analyzed and categorized
- [x] error-type-1-incomplete-answers.md created (175 lines)
- [x] error-type-2-artifact-failures.md created (177 lines)
- [x] error-type-3-complexity-errors.md created (201 lines)
- [x] error-type-4-validation-failures.md created (248 lines)
- [x] error-type-5-constraint-conflicts.md created (223 lines)
- [x] error-type-6-directory-issues.md created (182 lines)
- [x] error-handling-index.md created with decision tree (139 lines)
- [x] SKILL.md Error Handling section updated (lines 257-316)
- [x] Original error-handling.md retained for reference

### Quality
- [x] Total line count >= 1,062 (1,345 lines - content enhanced)
- [x] Each error-type file < 250 lines
- [x] Each file has required sections (detection, recovery, examples)
- [x] All cross-references resolve correctly

### Testing
- [x] Line count validation: wc -l for each file
- [x] Content comparison: original topics covered in new files
- [x] Link validation: all relative links work

### Documentation
- [x] Story file updated with implementation notes

## Implementation Notes

- [x] error-handling.md content analyzed and categorized - Completed: 2025-12-29
- [x] error-type-1-incomplete-answers.md created (175 lines) - Completed: 2025-12-29
- [x] error-type-2-artifact-failures.md created (177 lines) - Completed: 2025-12-29
- [x] error-type-3-complexity-errors.md created (201 lines) - Completed: 2025-12-29
- [x] error-type-4-validation-failures.md created (248 lines) - Completed: 2025-12-29
- [x] error-type-5-constraint-conflicts.md created (223 lines) - Completed: 2025-12-29
- [x] error-type-6-directory-issues.md created (182 lines) - Completed: 2025-12-29
- [x] error-handling-index.md created with decision tree (139 lines) - Completed: 2025-12-29
- [x] SKILL.md Error Handling section updated (lines 257-316) - Completed: 2025-12-29
- [x] Original error-handling.md retained for reference - Completed: 2025-12-29
- [x] Total line count >= 1,062 (1,345 lines - content enhanced) - Completed: 2025-12-29
- [x] Each error-type file < 250 lines - Completed: 2025-12-29
- [x] Each file has required sections (detection, recovery, examples) - Completed: 2025-12-29
- [x] All cross-references resolve correctly - Completed: 2025-12-29
- [x] Line count validation: wc -l for each file - Completed: 2025-12-29
- [x] Content comparison: original topics covered in new files - Completed: 2025-12-29
- [x] Link validation: all relative links work - Completed: 2025-12-29
- [x] Story file updated with implementation notes - Completed: 2025-12-29

**Developer:** claude/opus
**Implemented:** 2025-12-29

### Content Distribution (Actual)

| Error Type | File | Lines | Content Topics |
|------------|------|-------|----------------|
| 1 | error-type-1-incomplete-answers.md | 175 | Vague answers, missing details, follow-ups |
| 2 | error-type-2-artifact-failures.md | 177 | File creation, write failures, permissions |
| 3 | error-type-3-complexity-errors.md | 201 | Tier calculation, dimension validation |
| 4 | error-type-4-validation-failures.md | 248 | Schema errors, quality validation |
| 5 | error-type-5-constraint-conflicts.md | 223 | Context file violations, brownfield |
| 6 | error-type-6-directory-issues.md | 182 | Path errors, missing directories |
| Index | error-handling-index.md | 139 | Decision tree, quick reference |

## Workflow Status

- [x] Architecture phase complete
- [x] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Acceptance Criteria Verification Checklist

### AC#1: error-handling.md split into 6 error-type files
- [x] 6 error-type files created
- [x] Files follow naming convention
- [x] All 6 files present in references directory

### AC#2: Each error-type file is self-contained
- [x] error-type-1 has detection, recovery, examples
- [x] error-type-2 has detection, recovery, examples
- [x] error-type-3 has detection, recovery, examples
- [x] error-type-4 has detection, recovery, examples
- [x] error-type-5 has detection, recovery, examples
- [x] error-type-6 has detection, recovery, examples

### AC#3: Master index file created
- [x] error-handling-index.md exists
- [x] Decision tree present
- [x] Quick reference table included
- [x] Links to all 6 files

### AC#4: SKILL.md references updated
- [x] Error Handling section updated
- [x] All 6 error-type files listed
- [x] Index file referenced

### AC#5: All original content preserved
- [x] Total lines >= 1,062 (1,345 actual)
- [x] All error types covered
- [x] No topics missing

### AC#6: Each file stays under 250 lines
- [x] error-type-1: 175 lines (< 250)
- [x] error-type-2: 177 lines (< 250)
- [x] error-type-3: 201 lines (< 250)
- [x] error-type-4: 248 lines (< 250)
- [x] error-type-5: 223 lines (< 250)
- [x] error-type-6: 182 lines (< 250)
