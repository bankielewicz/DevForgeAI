---
id: STORY-280
title: Story Template Update for XML AC Format
type: feature
epic: EPIC-046
sprint: SPRINT-8
status: QA Approved
points: 3
depends_on: ["STORY-279"]
priority: High
assigned_to: Unassigned
created: 2026-01-19
format_version: "2.5"
---

# Story: Story Template Update for XML AC Format

## Description

**As a** framework maintainer,
**I want** the story template to use XML AC format,
**so that** new stories have machine-readable acceptance criteria.

## Acceptance Criteria

### AC#1: Template File Update

**Given** the story template at `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`,
**When** it is updated,
**Then** the Acceptance Criteria section uses XML format with `<acceptance_criteria>` blocks.

---

### AC#2: Example XML AC Included

**Given** the updated template,
**When** a developer views the template,
**Then** it includes a complete example XML AC with all optional elements.

---

### AC#3: Source Files Guidance

**Given** the updated template,
**When** viewing the verification section,
**Then** it includes guidance for populating `<source_files>` hints.

---

### AC#4: Backward Compatibility Note

**Given** the updated template,
**When** viewing changelog/notes,
**Then** it documents that legacy markdown AC format is NOT supported by verification.

---

### AC#5: Template Version Bump

**Given** the updated template,
**When** metadata is updated,
**Then** template_version is bumped to "2.6" with changelog entry.

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "Story Template"
      file_path: ".claude/skills/devforgeai-story-creation/assets/templates/story-template.md"
      required_keys:
        - key: "template_version"
          type: "string"
          example: "2.6"
          required: true
          validation: "Version bumped from 2.5"
          test_requirement: "Test: Verify template_version is 2.6"
        - key: "xml_ac_section"
          type: "markdown"
          required: true
          validation: "Contains <acceptance_criteria> example"
          test_requirement: "Test: Grep for acceptance_criteria XML"
        - key: "source_files_guidance"
          type: "markdown"
          required: true
          validation: "Contains guidance for source_files"
          test_requirement: "Test: Grep for source_files guidance"

  business_rules:
    - id: "BR-001"
      rule: "Template must include complete XML AC example"
      trigger: "During template review"
      validation: "Example includes id, given, when, then, verification"
      error_handling: "Add missing elements"
      test_requirement: "Test: Verify example completeness"
      priority: "High"
    - id: "BR-002"
      rule: "Template must document no legacy support"
      trigger: "During template update"
      validation: "Note states markdown AC not supported by verification"
      error_handling: "Add note"
      test_requirement: "Test: Grep for backward compatibility note"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Maintainability"
      requirement: "Template stays under 800 lines"
      metric: "< 800 lines"
      test_requirement: "Test: Count lines in template"
      priority: "Medium"
```

---

## Non-Functional Requirements (NFRs)

### Maintainability

**Template Size:**
- Under 800 lines
- Clear section separation

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-279:** XML Schema Design
  - **Why:** Template must follow defined schema
  - **Status:** Backlog

---

## Test Strategy

### Structural Tests

**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** Template contains XML AC example
2. **Edge Cases:**
   - Long AC text
   - Multiple source files
3. **Error Cases:**
   - Missing required example elements

---

## Acceptance Criteria Verification Checklist

### AC#1: Template File Update

- [ ] XML format in AC section - **Phase:** 3 - **Evidence:** Grep result
- [ ] `<acceptance_criteria>` blocks present - **Phase:** 3 - **Evidence:** Grep result

### AC#2: Example XML AC Included

- [ ] Complete example present - **Phase:** 3 - **Evidence:** Content review
- [ ] All optional elements shown - **Phase:** 3 - **Evidence:** Element check

### AC#3: Source Files Guidance

- [ ] Guidance for source_files - **Phase:** 3 - **Evidence:** Grep result
- [ ] Examples of hints - **Phase:** 3 - **Evidence:** Content review

### AC#4: Backward Compatibility Note

- [ ] Note about legacy format - **Phase:** 3 - **Evidence:** Grep result
- [ ] Clear statement of no support - **Phase:** 3 - **Evidence:** Content review

### AC#5: Template Version Bump

- [ ] Version is 2.6 - **Phase:** 3 - **Evidence:** YAML check
- [ ] Changelog entry added - **Phase:** 3 - **Evidence:** Changelog section

---

**Checklist Progress:** 0/11 items complete (0%)

---

## Definition of Done

### Implementation
- [x] Template updated with XML AC format
- [x] Example XML AC included
- [x] Source files guidance added
- [x] Backward compatibility note added
- [x] Version bumped to 2.6

### Quality
- [x] All 5 acceptance criteria have passing tests
- [x] Template under 800 lines
- [x] Example is complete

### Testing
- [x] Structural tests for content
- [x] Version validation test

### Documentation
- [x] Template changelog updated

---

## Implementation Notes

- [x] Template updated with XML AC format
- [x] Example XML AC included
- [x] Source files guidance added
- [x] Backward compatibility note added
- [x] Version bumped to 2.6
- [x] All 5 acceptance criteria have passing tests
- [x] Template under 800 lines
- [x] Example is complete
- [x] Structural tests for content
- [x] Version validation test
- [x] Template changelog updated

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-19 15:25 | claude/devforgeai-story-creation | Created | Story created from EPIC-046 Feature 3.2 | STORY-280.story.md |
| 2026-01-19 15:27 | claude/test-automator | Red (Phase 02) | Tests generated for 5 ACs + 1 NFR | devforgeai/tests/STORY-280/*.sh |
| 2026-01-19 15:30 | claude/opus | Green (Phase 03) | Template updated with XML AC format | story-template.md |
| 2026-01-19 15:31 | claude/refactoring-specialist | Refactor (Phase 04) | Fixed footer version info | story-template.md |
| 2026-01-19 15:32 | claude/integration-tester | Integration (Phase 05) | All integration tests pass | story-template.md |
| 2026-01-19 15:33 | claude/opus | DoD Update (Phase 07) | Marked all DoD items complete | STORY-280.story.md |
| 2026-01-19 16:05 | claude/qa-result-interpreter | QA Deep | PASSED: 6/6 tests, 0 violations, 96% quality | STORY-280-qa-report.md |

## Notes

**Design Decisions:**
- Version 2.6 (incremental from 2.5)
- Clear NO legacy support stance per user requirement
- Guidance helps developers populate hints

**References:**
- EPIC-046: AC Compliance Verification System
- US-3.2 from requirements specification
- Current template: v2.5
