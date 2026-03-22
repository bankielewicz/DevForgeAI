---
id: STORY-281
title: XML AC Migration Guide
type: documentation
epic: EPIC-046
sprint: SPRINT-8
status: QA Approved
points: 3
depends_on: ["STORY-279", "STORY-280"]
priority: High
assigned_to: Unassigned
created: 2026-01-19
format_version: "2.5"
---

# Story: XML AC Migration Guide

## Description

**As a** framework developer,
**I want** a guide for migrating existing stories to XML format,
**so that** I can update my stories to use the new verification system.

## Acceptance Criteria

### AC#1: Guide File Creation

**Given** the need for migration documentation,
**When** documentation is created,
**Then** a new file `docs/guides/ac-xml-migration-guide.md` is created.

---

### AC#2: Before/After Examples

**Given** the migration guide,
**When** viewing the examples section,
**Then** it includes clear before (markdown) and after (XML) examples for each AC pattern.

---

### AC#3: Regex Patterns for Automation

**Given** the migration guide,
**When** viewing the automation section,
**Then** it includes regex patterns for automated detection and conversion (if applicable).

---

### AC#4: Validation Checklist

**Given** the migration guide,
**When** completing a migration,
**Then** it includes a validation checklist to verify migration success.

---

### AC#5: Story Count Impact

**Given** the migration guide,
**When** viewing the scope section,
**Then** it documents the estimated story count requiring migration.

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "Migration Guide"
      file_path: "docs/guides/ac-xml-migration-guide.md"
      required_keys:
        - key: "before_after_examples"
          type: "markdown"
          required: true
          validation: "Contains markdown → XML examples"
          test_requirement: "Test: Verify examples present"
        - key: "regex_patterns"
          type: "markdown"
          required: true
          validation: "Contains regex for detection"
          test_requirement: "Test: Verify regex patterns"
        - key: "validation_checklist"
          type: "markdown"
          required: true
          validation: "Contains checklist items"
          test_requirement: "Test: Verify checklist present"

  business_rules:
    - id: "BR-001"
      rule: "Guide must cover all AC patterns"
      trigger: "During guide creation"
      validation: "Examples for happy path, error, edge cases"
      error_handling: "Add missing patterns"
      test_requirement: "Test: Verify pattern coverage"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Usability"
      requirement: "Guide is actionable"
      metric: "Developer can migrate story in < 10 minutes"
      test_requirement: "Test: Time a sample migration"
      priority: "Medium"
```

---

## Non-Functional Requirements (NFRs)

### Usability

**Migration Time:**
- Single story: < 10 minutes
- Clear step-by-step instructions

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-279:** XML Schema Design
- [x] **STORY-280:** Story Template Update

---

## Test Strategy

### Structural Tests (Documentation Type)

**Coverage Target:** 95%+

**Test Scenarios:**
1. **Content Exists:** Grep for required sections
2. **Examples Valid:** Parse before/after examples
3. **Checklist Complete:** Verify checklist items

---

## Acceptance Criteria Verification Checklist

### AC#1: Guide File Creation

- [x] File exists at docs/guides/ - **Phase:** 3 - **Evidence:** docs/guides/ac-xml-migration-guide.md created

### AC#2: Before/After Examples

- [x] Markdown AC example - **Phase:** 3 - **Evidence:** "Markdown Format (Before)" sections with `### AC#` examples
- [x] XML AC example - **Phase:** 3 - **Evidence:** "XML Format (After)" sections with `<acceptance_criteria>` blocks
- [x] Clear transformation shown - **Phase:** 3 - **Evidence:** Side-by-side examples in 3 scenarios

### AC#3: Regex Patterns

- [x] Detection patterns included - **Phase:** 3 - **Evidence:** "Regex Patterns for Detection" section with bash grep commands
- [x] Conversion patterns (if applicable) - **Phase:** 3 - **Evidence:** "Migration Patterns" section with step-by-step guidance

### AC#4: Validation Checklist

- [x] Checklist section exists - **Phase:** 3 - **Evidence:** "Validation Checklist" section with Pre/During/Post checklists
- [x] Checklist items actionable - **Phase:** 3 - **Evidence:** 15 actionable checkbox items

### AC#5: Story Count Impact

- [x] Scope section exists - **Phase:** 3 - **Evidence:** "Scope and Impact" section header
- [x] Story count documented - **Phase:** 3 - **Evidence:** "276 stories" total, "~193 stories" requiring migration

---

**Checklist Progress:** 10/10 items complete (100%)

---

## Definition of Done

### Implementation
- [x] Guide file created
- [x] Before/after examples included
- [x] Regex patterns documented
- [x] Validation checklist created
- [x] Story count documented

### Quality
- [x] All 5 acceptance criteria have passing tests
- [x] Guide is clear and actionable
- [x] Examples are correct

### Testing
- [x] Structural tests for content
- [x] Sample migration test

### Documentation
- [x] Guide linked from CLAUDE.md or README

---

## Implementation Notes

- [x] Guide file created - Completed: docs/guides/ac-xml-migration-guide.md
- [x] Before/after examples included - Completed: 3 progressive examples (minimal, with implements, with verification)
- [x] Regex patterns documented - Completed: "Regex Patterns for Detection" section with bash grep commands
- [x] Validation checklist created - Completed: 15 actionable items (Pre/During/Post migration)
- [x] Story count documented - Completed: 276 total stories, ~193 requiring migration
- [x] All 5 acceptance criteria have passing tests - Completed: test-ac1 through test-ac5 all PASS
- [x] Guide is clear and actionable - Completed: ToC, step-by-step patterns, troubleshooting
- [x] Examples are correct - Completed: Validated against coding-standards.md XML AC schema
- [x] Structural tests for content - Completed: 5 bash tests in devforgeai/tests/STORY-281/
- [x] Sample migration test - Completed: test-sample-migration.sh validates workflow
- [x] Guide linked from CLAUDE.md or README - Completed: Added to CLAUDE.md Quick Reference table

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-19 15:30 | claude/devforgeai-story-creation | Created | Story created from EPIC-046 Feature 3.3 | STORY-281.story.md |
| 2026-01-19 | claude/test-automator | Red (Phase 02) | Generated 5 structural tests for documentation ACs | devforgeai/tests/STORY-281/test-ac*.sh |
| 2026-01-19 | claude/backend-architect | Green (Phase 03) | Created migration guide with all 5 AC requirements | docs/guides/ac-xml-migration-guide.md |
| 2026-01-19 | claude/refactoring-specialist | Refactor (Phase 04) | Clarified COMP indexing, simplified backward compatibility note | docs/guides/ac-xml-migration-guide.md |
| 2026-01-19 | claude/opus | Deferral (Phase 06) | Added sample migration test, linked guide in CLAUDE.md | test-sample-migration.sh, CLAUDE.md |
| 2026-01-19 | claude/opus | DoD Update (Phase 07) | Marked all 12 DoD items complete, updated Implementation Notes | STORY-281.story.md |
| 2026-01-19 | claude/qa-result-interpreter | QA Deep | PASSED: 100% traceability, 6/6 tests, 1/1 validators | STORY-281-qa-report.md |

## Notes

**Design Decisions:**
- Story type is "documentation" (skips Phase 05 Integration)
- Regex patterns enable potential automation
- Validation checklist ensures complete migration

**References:**
- EPIC-046: AC Compliance Verification System
- US-3.3 from requirements specification
