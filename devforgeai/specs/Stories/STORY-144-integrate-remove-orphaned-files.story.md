---
id: STORY-144
title: Integrate or Remove Orphaned Files
epic: EPIC-030
sprint: Backlog
status: Backlog
points: 3
depends_on: []
priority: High
assigned_to: TBD
created: 2025-12-22
format_version: "2.3"
---

# Story: Integrate or Remove Orphaned Files

## Description

**As a** framework maintainer,
**I want** to review orphaned files (user-input-integration-guide.md, brainstorm-data-mapping.md) and integrate valuable content or remove redundant files,
**so that** the codebase is clean with clear justification for every file in the repository.

## Acceptance Criteria

### AC#1: user-input-integration-guide.md reviewed and resolved

**Given** user-input-integration-guide.md exists as an orphaned file,
**When** the file is reviewed for value and redundancy,
**Then** one of the following actions is taken:
- **If valuable:** Content integrated into user-input-guidance.md Section 5 (Skill Integration Guide)
- **If redundant:** File deleted with reason documented in commit message
- **If unclear:** Review time-boxed to 30 minutes, default to delete if no clear value

---

### AC#2: brainstorm-data-mapping.md reviewed and resolved

**Given** brainstorm-data-mapping.md exists as an orphaned file,
**When** the file is reviewed for value and redundancy,
**Then** one of the following actions is taken:
- **If valuable:** Content integrated into brainstorm-handoff-workflow.md
- **If redundant:** File deleted with reason documented in commit message
- **If unclear:** Review time-boxed to 30 minutes, default to delete if no clear value

---

### AC#3: No unreferenced files remain in references directory

**Given** ideation skill references directory has been cleaned,
**When** a reference check is performed (grep for filename in SKILL.md and workflow files),
**Then** every file in the references directory is referenced at least once in SKILL.md or a workflow file.

---

### AC#4: Commit message documents justification

**Given** orphaned files have been resolved (integrated or deleted),
**When** changes are committed,
**Then** commit message includes:
- List of files affected
- Action taken (integrated/deleted)
- Justification for each file

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  reference_files:
    skill_definition: ".claude/skills/devforgeai-ideation/SKILL.md"
    user_input_guidance: ".claude/skills/devforgeai-ideation/references/user-input-guidance.md"
    brainstorm_handoff: ".claude/skills/devforgeai-ideation/references/brainstorm-handoff-workflow.md"

  orphaned_files_verified:
    description: "Files verified to exist during story creation (2025-12-22)"
    files:
      - path: ".claude/skills/devforgeai-ideation/references/user-input-integration-guide.md"
        status: "exists"
        target_if_valuable: "user-input-guidance.md Section 5"
      - path: ".claude/skills/devforgeai-ideation/references/brainstorm-data-mapping.md"
        status: "exists"
        target_if_valuable: "brainstorm-handoff-workflow.md"

  components:
    - type: "Configuration"
      name: "user-input-integration-guide.md"
      file_path: ".claude/skills/devforgeai-ideation/references/user-input-integration-guide.md"
      requirements:
        - id: "CFG-001"
          description: "Review file for value vs redundancy"
          testable: true
          test_requirement: "Test: File either integrated or deleted"
          priority: "High"
        - id: "CFG-002"
          description: "If valuable, integrate into user-input-guidance.md Section 5"
          testable: true
          test_requirement: "Test: Content preserved if valuable"
          priority: "Medium"

    - type: "Configuration"
      name: "brainstorm-data-mapping.md"
      file_path: ".claude/skills/devforgeai-ideation/references/brainstorm-data-mapping.md"
      requirements:
        - id: "CFG-003"
          description: "Review file for value vs redundancy"
          testable: true
          test_requirement: "Test: File either integrated or deleted"
          priority: "High"
        - id: "CFG-004"
          description: "If valuable, integrate into brainstorm-handoff-workflow.md"
          testable: true
          test_requirement: "Test: Content preserved if valuable"
          priority: "Medium"

  business_rules:
    - id: "BR-001"
      rule: "Review must be time-boxed to 30 minutes per file"
      test_requirement: "Test: Decision made within time limit"

    - id: "BR-002"
      rule: "Default action is delete if value unclear after time-box"
      test_requirement: "Test: Clear decision documented for each file"

    - id: "BR-003"
      rule: "All files in references directory must be referenced somewhere"
      test_requirement: "Test: Grep for each filename returns at least one match in SKILL.md or workflow files"

    - id: "BR-004"
      rule: "Commit message must document justification for each file action"
      test_requirement: "Test: Commit message includes action and reasoning"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Maintainability"
      requirement: "Clean codebase with no orphaned files"
      metric: "Zero unreferenced files in references directory"
      test_requirement: "Test: All files referenced in SKILL.md or workflows"

    - id: "NFR-002"
      category: "Reliability"
      requirement: "Content preservation for valuable files"
      metric: "100% content preserved when integrating"
      test_requirement: "Test: Compare original content with integrated content"
```

## Technical Limitations

```yaml
technical_limitations: []
# No technical limitations identified for this story
```

## Edge Cases

1. **File contains unique content not found elsewhere:** If orphaned file has unique guidance not in any other file, must integrate rather than delete.

2. **Partial redundancy:** If file is 50% redundant and 50% unique, integrate unique portions and delete the file.

3. **Referenced but not indexed:** If file is referenced in code but not in SKILL.md index, add to index instead of deleting.

4. **Circular references:** If orphaned file references another orphaned file, review both together to avoid broken references.

## Data Validation Rules

1. **Time-box enforcement:** Review each file for maximum 30 minutes before making decision.

2. **Reference check pattern:** Use `grep -r "filename.md"` to check if file is referenced.

3. **Content comparison:** When integrating, verify no content loss by comparing original and integrated text.

4. **Commit format:** Commit message must follow format:
   ```
   chore(ideation): resolve orphaned reference files

   - user-input-integration-guide.md: [INTEGRATED/DELETED] - [reason]
   - brainstorm-data-mapping.md: [INTEGRATED/DELETED] - [reason]
   ```

## Non-Functional Requirements

### Maintainability
- Zero orphaned files after completion
- All files in references directory are documented in SKILL.md
- Clear file organization with no redundancy

### Traceability
- Commit message documents action and justification
- Integration preserves original content

## UI Specification

N/A - This story involves file cleanup and documentation. No user interface changes required.

## Definition of Done

### Implementation
- [ ] user-input-integration-guide.md reviewed (30 min max)
- [ ] Decision made: integrate or delete user-input-integration-guide.md
- [ ] If integrated: content merged into user-input-guidance.md
- [ ] If deleted: file removed
- [ ] brainstorm-data-mapping.md reviewed (30 min max)
- [ ] Decision made: integrate or delete brainstorm-data-mapping.md
- [ ] If integrated: content merged into brainstorm-handoff-workflow.md
- [ ] If deleted: file removed

### Quality
- [ ] No unreferenced files in references directory
- [ ] All remaining files referenced in SKILL.md
- [ ] Content preserved if integrated

### Testing
- [ ] Grep for each orphaned filename returns zero matches (deleted)
- [ ] Or grep confirms integrated content exists in target file

### Documentation
- [ ] Commit message documents action and justification for each file
- [ ] Story file updated with implementation notes

## Implementation Notes

*To be filled during development*

### Review Results (To Be Completed)

**user-input-integration-guide.md:**
- Review Duration: _____ minutes
- Decision: [ ] Integrate / [ ] Delete
- Reason: _____

**brainstorm-data-mapping.md:**
- Review Duration: _____ minutes
- Decision: [ ] Integrate / [ ] Delete
- Reason: _____

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Acceptance Criteria Verification Checklist

### AC#1: user-input-integration-guide.md reviewed and resolved
- [ ] File reviewed within 30-minute time-box
- [ ] Value assessment completed
- [ ] Action taken (integrate/delete)
- [ ] If integrated: content in user-input-guidance.md Section 5
- [ ] If deleted: file removed from repository

### AC#2: brainstorm-data-mapping.md reviewed and resolved
- [ ] File reviewed within 30-minute time-box
- [ ] Value assessment completed
- [ ] Action taken (integrate/delete)
- [ ] If integrated: content in brainstorm-handoff-workflow.md
- [ ] If deleted: file removed from repository

### AC#3: No unreferenced files remain in references directory
- [ ] Grep for each reference file confirms at least one reference
- [ ] SKILL.md lists all reference files

### AC#4: Commit message documents justification
- [ ] Commit message includes file list
- [ ] Action documented for each file
- [ ] Justification provided
