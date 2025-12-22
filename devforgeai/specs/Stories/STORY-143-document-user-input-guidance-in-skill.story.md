---
id: STORY-143
title: Document user-input-guidance.md in SKILL.md
epic: EPIC-030
sprint: Backlog
status: Backlog
points: 2
depends_on: []
priority: High
assigned_to: TBD
created: 2025-12-22
format_version: "2.3"
---

# Story: Document user-input-guidance.md in SKILL.md

## Description

**As a** developer using the ideation skill,
**I want** to know when to load user-input-guidance.md from the SKILL.md reference file index,
**so that** I can leverage the 15 elicitation patterns and 28 AskUserQuestion templates for complete requirements gathering.

## Acceptance Criteria

### AC#1: SKILL.md Reference Files section updated

**Given** the SKILL.md file has a "Reference Files" section,
**When** user-input-guidance.md is added to the index,
**Then** the section includes:
- File name: user-input-guidance.md
- Line count: ~898 lines
- Description: Framework-internal guidance for eliciting complete requirements
- Key contents: 15 elicitation patterns, 28 AskUserQuestion templates, NFR quantification table

---

### AC#2: Phase 1 workflow references user-input-guidance.md

**Given** SKILL.md documents the Phase 1 (Discovery & Problem Understanding) workflow,
**When** the workflow instructions are reviewed,
**Then** Phase 1 includes:
- Step 0.5 instruction to load user-input-guidance.md (loaded before discovery questions)
- Error-tolerant loading pattern (graceful degradation if file missing)
- Read command example: `Read(file_path=".claude/skills/devforgeai-ideation/references/user-input-guidance.md")`

---

### AC#3: Cross-reference to skill integration section

**Given** user-input-guidance.md Section 5 contains skill integration guidance,
**When** SKILL.md references user-input-guidance.md,
**Then** the reference includes a pointer to Section 5 for:
- devforgeai-ideation integration patterns
- devforgeai-story-creation integration patterns
- Other skill integration guidance

---

### AC#4: Documentation completeness validated

**Given** all reference files should be documented in SKILL.md,
**When** validation checks SKILL.md completeness,
**Then** user-input-guidance.md appears in the reference file listing with accurate line count and description.

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  reference_files:
    skill_to_modify: ".claude/skills/devforgeai-ideation/SKILL.md"
    user_input_guidance: ".claude/skills/devforgeai-ideation/references/user-input-guidance.md"
    discovery_workflow: ".claude/skills/devforgeai-ideation/references/discovery-workflow.md"

  components:
    - type: "Configuration"
      name: "SKILL.md"
      file_path: ".claude/skills/devforgeai-ideation/SKILL.md"
      requirements:
        - id: "CFG-001"
          description: "Add user-input-guidance.md to Reference Files section"
          testable: true
          test_requirement: "Test: Grep for 'user-input-guidance.md' in SKILL.md returns match"
          priority: "Critical"
        - id: "CFG-002"
          description: "Add Step 0.5 in Phase 2 to load user-input-guidance.md"
          testable: true
          test_requirement: "Test: Phase 2 section contains Step 0.5 with Read command"
          priority: "Critical"
        - id: "CFG-003"
          description: "Include cross-reference to Section 5 skill integration"
          testable: true
          test_requirement: "Test: Reference includes skill integration pointer"
          priority: "Medium"

  business_rules:
    - id: "BR-001"
      rule: "All reference files must be documented in SKILL.md Reference Files section"
      test_requirement: "Test: user-input-guidance.md listed in Reference Files"

    - id: "BR-002"
      rule: "Loading user-input-guidance.md must be error-tolerant (graceful degradation)"
      test_requirement: "Test: Step 0.5 includes try/catch or conditional loading pattern"

    - id: "BR-003"
      rule: "Line count must be accurate (within 10% of actual)"
      test_requirement: "Test: Documented line count matches actual file (wc -l)"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Maintainability"
      requirement: "Documentation completeness"
      metric: "100% of reference files documented in SKILL.md"
      test_requirement: "Test: All reference files in directory listed in SKILL.md"

    - id: "NFR-002"
      category: "Performance"
      requirement: "Guidance loading overhead"
      metric: "< 500ms additional load time for user-input-guidance.md"
      test_requirement: "Test: Phase 1 execution time within acceptable range"
```

## Technical Limitations

```yaml
technical_limitations: []
# No technical limitations identified for this story
```

## Edge Cases

1. **user-input-guidance.md file missing:** If the file doesn't exist, the Step 0.5 loading must gracefully degrade and continue with baseline questioning logic.

2. **Line count changes:** When user-input-guidance.md is updated in the future, the SKILL.md reference must indicate approximate line count (e.g., "~898 lines") to avoid requiring updates for minor changes.

3. **Section references incorrect:** If Section 5 is reorganized in user-input-guidance.md, cross-references should use section titles not numbers for stability.

## Data Validation Rules

1. **File path format:** Reference must use correct path: `.claude/skills/devforgeai-ideation/references/user-input-guidance.md`

2. **Pattern count accuracy:** Document "15 elicitation patterns" and "28 AskUserQuestion templates" - verify these counts match actual file content.

3. **Section numbering:** Reference Section 5 by title ("Skill Integration Guide") for stability.

## Non-Functional Requirements

### Maintainability
- Documentation stays in sync with file content
- Line counts approximate to avoid frequent updates
- Section references by title, not number

### Performance
- Loading user-input-guidance.md adds minimal overhead (<500ms)
- Selective loading pattern available for large files

## UI Specification

N/A - This story modifies documentation only. No user interface changes required.

## Definition of Done

### Implementation
- [ ] SKILL.md Reference Files section includes user-input-guidance.md entry
- [ ] Phase 2 includes Step 0.5 with Read command for user-input-guidance.md
- [ ] Cross-reference to Section 5 (Skill Integration Guide) added
- [ ] Error-tolerant loading pattern documented

### Quality
- [ ] Line count verified against actual file (wc -l)
- [ ] Pattern counts verified (15 patterns, 28 templates)
- [ ] No broken references in SKILL.md

### Testing
- [ ] Manual test: SKILL.md renders correctly with new content
- [ ] Validation: Grep confirms user-input-guidance.md referenced in SKILL.md

### Documentation
- [ ] Story file updated with implementation notes

## Implementation Notes

*To be filled during development*

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Acceptance Criteria Verification Checklist

### AC#1: SKILL.md Reference Files section updated
- [ ] user-input-guidance.md added to Reference Files section
- [ ] File description accurate
- [ ] Line count documented (~898 lines)
- [ ] Key contents listed (patterns, templates, NFR table)

### AC#2: Phase 1 workflow references user-input-guidance.md
- [ ] Step 0.5 added to Phase 1
- [ ] Read command example included
- [ ] Error-tolerant loading pattern documented

### AC#3: Cross-reference to skill integration section
- [ ] Pointer to Section 5 included
- [ ] Skill integration guidance referenced

### AC#4: Documentation completeness validated
- [ ] user-input-guidance.md appears in reference file listing
- [ ] Line count and description accurate
