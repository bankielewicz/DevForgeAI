---
id: STORY-205
title: Create Subagent Design Guidance Document
type: documentation
epic: EPIC-033-framework-enhancement-triage-q4-2025
sprint: Backlog
status: Backlog
points: 2
depends_on: ["STORY-203", "STORY-204"]
priority: Medium
assigned_to: Unassigned
created: 2026-01-01
source_rca: RCA-017
source_recommendation: REC-3
format_version: "2.5"
---

# Story: Create Subagent Design Guidance Document

## Description

**As a** DevForgeAI framework developer creating new subagents,
**I want** clear guidance on which context files each subagent type should read before file operations,
**so that** future subagent designers don't repeat the source-tree.md validation omission.

**Context from RCA-017:**
test-automator was created before systematic context validation was enforced across all subagents. Future subagent designers need clear guidance on:
- Which context files to read for each subagent type
- The critical rule that ALL Write() calls must be preceded by source-tree.md validation
- Examples of correct and incorrect patterns

**Documentation Gap:**
Currently, subagent design guidance is fragmented across:
- source-tree.md (lines 501-548) - Subagent location rules
- architecture-constraints.md (lines 46-63) - Subagent design constraints
- anti-patterns.md (various categories) - What NOT to do

This story consolidates guidance into a single authoritative document.

## Acceptance Criteria

### AC#1: Guidance Document Created

**Given** the `.claude/` directory
**When** this story is complete
**Then** a new file exists at `.claude/SUBAGENT-DESIGN-GUIDE.md`

---

### AC#2: Context File Validation Checklist Included

**Given** the guidance document
**When** a developer reads it
**Then** they find a checklist specifying which context files each subagent type should read:

**For ALL subagents:**
- tech-stack.md - Technology constraints

**For File-Generation Subagents (using Write/Edit tools):**
- source-tree.md - Validate output file paths (CRITICAL)
- dependencies.md - Verify no forbidden dependencies
- tech-stack.md - Validate technology choices

**For Code-Generation Subagents:**
- coding-standards.md - Follow code patterns
- architecture-constraints.md - Respect layer boundaries
- anti-patterns.md - Avoid forbidden patterns

**For Specification/Documentation Subagents:**
- tech-stack.md - Aligned with locked technologies
- dependencies.md - No external packages (if framework component)
- source-tree.md - Correct file locations

---

### AC#3: Critical Rule for Write() Operations Documented

**Given** the guidance document
**When** a developer reads the "Before ANY Write() call" section
**Then** they find:
- The critical rule: ALWAYS read source-tree.md before Write()
- Validation logic example
- HALT pattern for violations
- Example of correct vs incorrect approach

---

### AC#4: Template for Pre-Generation Validation Provided

**Given** the guidance document
**When** a developer needs to add validation to a new subagent
**Then** they can copy the Pre-Generation Validation template directly:

```markdown
**Pre-Generation Validation:**

Read(file_path="devforgeai/specs/context/source-tree.md")

Determine correct directory for output files:
- Extract directory patterns from source-tree.md
- Validate all planned file_path parameters match constraints

HALT if validation fails:
"""
❌ SOURCE-TREE CONSTRAINT VIOLATION
...
"""
```

---

### AC#5: Examples of Correct and Incorrect Patterns Included

**Given** the guidance document
**When** a developer reads the Examples section
**Then** they find:
- ❌ Wrong example (Write without validation)
- ✅ Correct example (Read source-tree.md then validate then Write)
- Explanation of why the wrong pattern causes issues (reference to RCA-017)

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Documentation"
      name: "SUBAGENT-DESIGN-GUIDE.md"
      file_path: ".claude/SUBAGENT-DESIGN-GUIDE.md"
      requirements:
        - id: "DOC-001"
          description: "Create document with YAML frontmatter"
          testable: true
          test_requirement: "Test: File exists and has valid frontmatter"
          priority: "High"
        - id: "DOC-002"
          description: "Include Context File Validation Checklist"
          testable: true
          test_requirement: "Test: Section '## Context File Validation Checklist' exists"
          priority: "Critical"
        - id: "DOC-003"
          description: "Include Critical Rule section"
          testable: true
          test_requirement: "Test: Section 'Before ANY Write() call' exists"
          priority: "Critical"
        - id: "DOC-004"
          description: "Include Pre-Generation Validation template"
          testable: true
          test_requirement: "Test: Code block with template exists"
          priority: "High"
        - id: "DOC-005"
          description: "Include Examples section with correct/incorrect patterns"
          testable: true
          test_requirement: "Test: Sections with ✅ and ❌ examples exist"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "Document is authoritative source for subagent design guidance"
      trigger: "When creating new subagents"
      validation: "CLAUDE.md references this document for subagent creation"
      error_handling: "N/A - documentation"
      test_requirement: "Test: Document referenced in relevant locations"
      priority: "Medium"

    - id: "BR-002"
      rule: "Document follows framework documentation standards"
      trigger: "Document creation"
      validation: "Markdown format, LOCKED status, version number"
      error_handling: "N/A - documentation"
      test_requirement: "Test: Verify document structure matches standards"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Maintainability"
      requirement: "Document is concise and scannable"
      metric: "< 300 lines total"
      test_requirement: "Test: wc -l < 300"
      priority: "Medium"

    - id: "NFR-002"
      category: "Usability"
      requirement: "Template is copy-paste ready"
      metric: "Developer can copy template in < 30 seconds"
      test_requirement: "Test: Manual review"
      priority: "High"
```

---

## Technical Limitations

```yaml
technical_limitations: []
# Documentation story - no technical limitations
```

---

## Non-Functional Requirements (NFRs)

### Maintainability

**Conciseness:**
- Document under 300 lines
- Focused on actionable guidance, not exhaustive detail

**Updates:**
- Document updated when new context files added
- Document updated when new subagent types introduced

### Usability

**Scannability:**
- Clear section headers
- Checklists for quick reference
- Copy-paste ready templates

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-203:** Add source-tree.md Validation to test-automator Phase 2
  - **Why:** Establishes the pattern documented in the guide
  - **Status:** Backlog

- [ ] **STORY-204:** Update ALL File-Generation Subagents with source-tree.md Validation
  - **Why:** Demonstrates pattern application across subagents
  - **Status:** Backlog

---

## Test Strategy

### Unit Tests

(Documentation story - verification tests only)

**Test Scenarios:**
1. File exists at `.claude/SUBAGENT-DESIGN-GUIDE.md`
2. Document contains required sections
3. Document under 300 lines

**Test File Location:** `tests/STORY-205/test-subagent-design-guide.sh`

---

### Integration Tests

**Test Scenarios:**
1. Manual review: Developer unfamiliar with subagents can follow guide
2. Template copy-paste works correctly

---

## Acceptance Criteria Verification Checklist

### AC#1: Guidance Document Created

- [ ] File created at `.claude/SUBAGENT-DESIGN-GUIDE.md` - **Phase:** 3 - **Evidence:** file exists

### AC#2: Context File Validation Checklist Included

- [ ] "## Context File Validation Checklist" section exists - **Phase:** 3 - **Evidence:** grep
- [ ] All subagent checklist present - **Phase:** 3 - **Evidence:** content review
- [ ] File-Generation checklist present - **Phase:** 3 - **Evidence:** content review
- [ ] Code-Generation checklist present - **Phase:** 3 - **Evidence:** content review
- [ ] Documentation checklist present - **Phase:** 3 - **Evidence:** content review

### AC#3: Critical Rule for Write() Operations Documented

- [ ] "Before ANY Write() call" section exists - **Phase:** 3 - **Evidence:** grep
- [ ] Critical rule statement present - **Phase:** 3 - **Evidence:** content review
- [ ] HALT pattern example included - **Phase:** 3 - **Evidence:** content review

### AC#4: Template for Pre-Generation Validation Provided

- [ ] Code block with template present - **Phase:** 3 - **Evidence:** content review
- [ ] Template is copy-paste ready - **Phase:** 5 - **Evidence:** manual test

### AC#5: Examples of Correct and Incorrect Patterns Included

- [ ] ❌ Wrong example present - **Phase:** 3 - **Evidence:** grep "❌"
- [ ] ✅ Correct example present - **Phase:** 3 - **Evidence:** grep "✅"
- [ ] RCA-017 reference included - **Phase:** 3 - **Evidence:** grep "RCA-017"

---

**Checklist Progress:** 0/14 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] SUBAGENT-DESIGN-GUIDE.md created at `.claude/`
- [ ] Document has YAML frontmatter with Status: LOCKED and Version
- [ ] Context File Validation Checklist section complete
- [ ] Critical Rule section with HALT pattern
- [ ] Pre-Generation Validation template (copy-paste ready)
- [ ] Examples section with correct/incorrect patterns
- [ ] RCA-017 referenced as motivation for the guide

### Quality
- [ ] All 5 acceptance criteria verified
- [ ] Document under 300 lines
- [ ] Document follows framework documentation standards

### Testing
- [ ] File existence verified
- [ ] Required sections verified via grep
- [ ] Manual review by developer unfamiliar with subagents

### Documentation
- [ ] Self-documenting (this IS the documentation deliverable)
- [ ] Cross-reference added to CLAUDE.md subagent section (optional)

---

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-01 12:00 | claude/devforgeai-story-creation | Created | Story created from RCA-017 REC-3 | STORY-205-subagent-design-guidance-document.story.md |

## Notes

**Design Decisions:**
- Single document rather than updating multiple existing files
- Checklist format for quick reference
- Template is copy-paste ready for immediate use

**Source RCA:**
- RCA-017: test-automator Source Tree Constraint Violation
- Recommendation: REC-3 (MEDIUM priority)
- Expected Impact: Prevents future subagent designers from omitting context file validation

**Document Structure:**
```markdown
# Subagent Design Guide

## Context File Validation Checklist
### For ALL Subagents
### For File-Generation Subagents
### For Code-Generation Subagents
### For Documentation Subagents

## Critical Rule: Before ANY Write() Call
### Validation Template
### HALT Pattern

## Examples
### ❌ Wrong (RCA-017 Pattern)
### ✅ Correct (With Validation)

## References
```

---

**Story Template Version:** 2.5
**Last Updated:** 2026-01-01
