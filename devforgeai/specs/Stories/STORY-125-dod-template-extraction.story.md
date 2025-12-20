---
id: STORY-125
title: DoD Template Extraction
type: feature
status: Backlog
priority: HIGH
story-points: 3
epic: EPIC-025
sprint: null
created: 2025-12-20
assignee: null
depends-on: []
---

# STORY-125: DoD Template Extraction

## User Story

**As a** DevForgeAI developer
**I want** a minimal Implementation Notes template (~20 lines)
**So that** I don't need to read 768 lines of dod-update-workflow.md to format DoD items correctly

## Background

The current `dod-update-workflow.md` is 768 lines for a conceptually simple requirement: add an Implementation Notes section with DoD item status. This complexity creates cognitive overhead for developers and makes the workflow harder to follow.

**Source File:** `.claude/skills/devforgeai-development/references/dod-update-workflow.md` (768 lines)

**Observation from STORY-114:** The core pattern is simple but buried in extensive error handling and edge case documentation.

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Template extraction may miss edge cases | Keep dod-update-workflow.md as comprehensive reference, template is minimal |
| Pre-commit validation too strict | Include tolerance for minor formatting variations |
| Existing story files fail new validation | Run validation against all existing stories before release |

## Acceptance Criteria

### AC#1: Template File Created
**Given** the DevForgeAI templates directory exists
**When** this story is implemented
**Then** a new file exists at `.claude/skills/devforgeai-development/assets/templates/implementation-notes-template.md`
**And** the file is 25 lines or fewer

### AC#2: Template Contains Required Sections
**Given** the implementation notes template file
**When** I read its contents
**Then** it contains:
- `## Implementation Notes` header
- `**Developer:**` field
- `**Implemented:**` field (date)
- `**Branch:**` field
- `### Definition of Done Status` subsection
- Completed item format: `- [x] {item} - Completed: {evidence}`
- Deferred item format: `- [ ] {item} - Deferred: {justification} (See: {STORY-XXX})`

### AC#3: dod-update-workflow.md References Template
**Given** the dod-update-workflow.md reference file
**When** I search for template reference
**Then** it contains a reference to the template file path
**And** it does NOT duplicate the full template inline

### AC#4: Pre-Commit Hook Validates Against Template
**Given** a story file with Implementation Notes section
**When** pre-commit hook runs
**Then** it validates the format matches the template structure
**And** it provides clear error messages if format is incorrect

### AC#5: Backward Compatibility
**Given** existing story files with Implementation Notes sections
**When** pre-commit hook runs
**Then** all existing valid formats continue to pass validation

## Technical Specification

### Files to Create
| File | Purpose | Max Lines |
|------|---------|-----------|
| `.claude/skills/devforgeai-development/assets/templates/implementation-notes-template.md` | Minimal template | 25 |

### Files to Modify
| File | Changes |
|------|---------|
| `.claude/skills/devforgeai-development/references/dod-update-workflow.md` | Add template reference, remove inline duplication |

### Template Content
```markdown
## Implementation Notes

**Developer:** {DEVELOPER_NAME}
**Implemented:** {YYYY-MM-DD}
**Branch:** {BRANCH_NAME}

### Definition of Done Status

<!-- For each completed DoD item: -->
- [x] {DoD item text} - Completed: {brief evidence of completion}

<!-- For each deferred DoD item: -->
- [ ] {DoD item text} - Deferred: {technical justification} (See: STORY-XXX)

### Additional Notes

{Optional: Any implementation notes, decisions made, or context for future developers}
```

## Test Strategy

### Test Files Location
`devforgeai/tests/STORY-125/`

### Test Cases
| Test ID | Description | Type |
|---------|-------------|------|
| test-ac1-template-exists.sh | Verify template file exists and is ≤25 lines | Bash |
| test-ac2-template-sections.sh | Verify all required sections present | Bash |
| test-ac3-reference-check.sh | Verify dod-update-workflow.md references template | Bash |
| test-ac4-validation-format.sh | Verify pre-commit validates against template | Bash |
| test-ac5-backward-compat.sh | Verify existing story files pass validation | Bash |

## Definition of Done

### Implementation
- [ ] Template file created at specified path
- [ ] Template is 25 lines or fewer
- [ ] All required sections present in template
- [ ] dod-update-workflow.md updated with template reference
- [ ] Inline template duplication removed from dod-update-workflow.md

### Quality
- [ ] All 5 test cases pass
- [ ] No regression in existing story file validation
- [ ] Template format documented

### Documentation
- [ ] Template usage instructions in dod-update-workflow.md
- [ ] Error messages reference template location

## Out of Scope

- Rewriting entire dod-update-workflow.md (only adding reference)
- Changing pre-commit hook logic (only validation target)
- Modifying existing story files
