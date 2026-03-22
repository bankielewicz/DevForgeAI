---
id: STORY-522
title: "Phase Execution Checklists"
type: documentation
epic: EPIC-002
sprint: unassigned
status: QA Approved
points: 5
depends_on: []
priority: High
advisory: false
source_gap: null
source_story: null
assigned_to: unassigned
created: 2026-03-02
format_version: "2.9"
---

# STORY-522: Phase Execution Checklists

## Description

**As a** orchestrator managing 12-phase development workflows,
**I want** a mandatory pre-exit checklist displayed in each phase file before calling `phase-complete`,
**so that** all mandatory steps are visibly verified and the orchestrator cannot skip or lose track of required work.

RCA-001 found the orchestrator skipped 11+ mandatory steps during STORY-010 because phase files are 280-450 lines with steps at varying nesting levels. Adding explicit checklists forces visible enumeration of what was and wasn't done.

**Source:** RCA-001 REC-2 (HIGH priority) — DevForgeAI CLI project (separate repository)

## Acceptance Criteria

### AC#1: Phase 01 has Pre-Exit Checklist with correct items

```xml
<acceptance_criteria id="AC1">
  <given>The file `src/claude/skills/implementing-stories/phases/phase-01-preflight.md` exists</given>
  <when>The file is read</when>
  <then>It contains `## Pre-Exit Checklist [MANDATORY — Display Before Exit Gate]` and the checklist includes items for: git-validator invoked, context files loaded, story loaded, tech-stack-detector invoked, session memory created, stale cleanup executed, context-preservation-validator invoked</then>
  <verification>
    <source_files>
      <file>src/claude/skills/implementing-stories/phases/phase-01-preflight.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Phase 02 has Pre-Exit Checklist with TDD Red items

```xml
<acceptance_criteria id="AC2">
  <given>The file `src/claude/skills/implementing-stories/phases/phase-02-test-first.md` exists</given>
  <when>The file is read</when>
  <then>It contains a Pre-Exit Checklist with items for: memory context loaded, test-automator invoked, RED state verified, snapshot created, snapshot verified via Glob, AC checklist updated, observation capture executed</then>
  <verification>
    <source_files>
      <file>src/claude/skills/implementing-stories/phases/phase-02-test-first.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Phase 04 has Pre-Exit Checklist with refactoring items

```xml
<acceptance_criteria id="AC3">
  <given>The file `src/claude/skills/implementing-stories/phases/phase-04-refactoring.md` exists</given>
  <when>The file is read</when>
  <then>It contains a Pre-Exit Checklist with items for: refactoring-specialist invoked, coverage validation, code-reviewer invoked, anti-gaming validation, light QA executed, AC checklist updated, observation capture</then>
  <verification>
    <source_files>
      <file>src/claude/skills/implementing-stories/phases/phase-04-refactoring.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

---

### AC#4: All 12 phase files have Pre-Exit Checklist

```xml
<acceptance_criteria id="AC4">
  <given>All 12 phase files in `src/claude/skills/implementing-stories/phases/`</given>
  <when>A grep for "Pre-Exit Checklist" is run across all files</when>
  <then>All 12 files match</then>
  <verification>
    <source_files>
      <file>src/claude/skills/implementing-stories/phases/phase-01-preflight.md</file>
      <file>src/claude/skills/implementing-stories/phases/phase-02-test-first.md</file>
      <file>src/claude/skills/implementing-stories/phases/phase-03-implementation.md</file>
      <file>src/claude/skills/implementing-stories/phases/phase-04-refactoring.md</file>
      <file>src/claude/skills/implementing-stories/phases/phase-04.5-ac-verification.md</file>
      <file>src/claude/skills/implementing-stories/phases/phase-05-integration.md</file>
      <file>src/claude/skills/implementing-stories/phases/phase-05.5-ac-verification.md</file>
      <file>src/claude/skills/implementing-stories/phases/phase-06-deferral.md</file>
      <file>src/claude/skills/implementing-stories/phases/phase-07-dod-update.md</file>
      <file>src/claude/skills/implementing-stories/phases/phase-08-git-workflow.md</file>
      <file>src/claude/skills/implementing-stories/phases/phase-09-feedback.md</file>
      <file>src/claude/skills/implementing-stories/phases/phase-10-result.md</file>
    </source_files>
  </verification>
</acceptance_criteria>
```

### Source Files Guidance

| File | Action | Purpose |
|------|--------|---------|
| `src/claude/skills/implementing-stories/phases/phase-01-preflight.md` | Modify | Add checklist before Exit Gate |
| `src/claude/skills/implementing-stories/phases/phase-02-test-first.md` | Modify | Add checklist before Exit Gate |
| `src/claude/skills/implementing-stories/phases/phase-03-implementation.md` | Modify | Add checklist before Exit Gate |
| `src/claude/skills/implementing-stories/phases/phase-04-refactoring.md` | Modify | Add checklist before Exit Gate |
| `src/claude/skills/implementing-stories/phases/phase-04.5-ac-verification.md` | Modify | Add checklist before Exit Gate |
| `src/claude/skills/implementing-stories/phases/phase-05-integration.md` | Modify | Add checklist before Exit Gate |
| `src/claude/skills/implementing-stories/phases/phase-05.5-ac-verification.md` | Modify | Add checklist before Exit Gate |
| `src/claude/skills/implementing-stories/phases/phase-06-deferral.md` | Modify | Add checklist before Exit Gate |
| `src/claude/skills/implementing-stories/phases/phase-07-dod-update.md` | Modify | Add checklist before Exit Gate |
| `src/claude/skills/implementing-stories/phases/phase-08-git-workflow.md` | Modify | Add checklist before Exit Gate |
| `src/claude/skills/implementing-stories/phases/phase-09-feedback.md` | Modify | Add checklist before Exit Gate |
| `src/claude/skills/implementing-stories/phases/phase-10-result.md` | Modify | Add checklist before Exit Gate |

## Technical Specification

```yaml
spec_version: "2.0"
story_id: STORY-522

components:
  - type: "Configuration"
    name: "Phase Pre-Exit Checklists"
    file_path: "src/claude/skills/implementing-stories/phases/"
    required_keys:
      - key: "Pre-Exit Checklist section"
        type: "markdown section"
        required: true
        validation: "Must appear before Exit Gate in each phase file"
        test_requirement: "Test: Grep all 12 files for 'Pre-Exit Checklist' header"

business_rules:
  - id: "BR-001"
    rule: "Each phase file must have a Pre-Exit Checklist section before its Exit Gate"
    trigger: "Phase file modification or creation"
    validation: "Grep for section header in all 12 files"
    error_handling: "Missing checklist = story not complete"
    test_requirement: "Test: Count files with 'Pre-Exit Checklist' header = 12"
    priority: "Critical"
  - id: "BR-002"
    rule: "Checklist items must match the phase's mandatory steps (4-12 items per phase)"
    trigger: "Phase file modification"
    validation: "Manual review of checklist vs phase steps"
    error_handling: "Mismatch = update checklist"
    test_requirement: "Test: Read Phase 01 checklist, verify git-validator and session memory items present"
    priority: "High"

non_functional_requirements:
  - id: "NFR-001"
    category: "Reliability"
    requirement: "Checklist display must not block on corrupted phase state"
    metric: "Graceful fallback: display all items unchecked if state unavailable"
    test_requirement: "Test: Verify checklist renders even without phase-state.json"
    priority: "Medium"
```

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "Pre-Exit Checklist"
    limitation: "Checklist enforcement is prompt-level only — orchestrator can still skip displaying it"
    decision: "workaround:STORY-014 provides binary-level enforcement as defence in depth (in CLI project)"
    discovered_phase: "Architecture"
    impact: "Prompt-level mitigation reduces but does not eliminate skip risk. Binary enforcement in STORY-014 (CLI project) closes the gap."
```

## Non-Functional Requirements

### Performance

**Response Time:** No runtime impact (documentation-only change)

### Security

Not applicable (documentation-only change)

### Scalability

**Phase Count:** 12 phase files. If new phases added, each must include a checklist.

### Reliability

**Error Handling:** Checklist display must not block on corrupted state (graceful fallback)

### Observability

**Logging:** Checklist display is visible in conversation output

---

## Dependencies

### Prerequisite Stories

None (documentation-only change, no code dependencies).

### External Dependencies

None.

### Technology Dependencies

None (markdown files only).

---

## Test Strategy

### Unit Tests

Not applicable (documentation change).

### Integration Tests

**Coverage Target:** Structural validation

| Test | AC | Description |
|------|----|-------------|
| Grep all 12 files | AC4 | `Grep(pattern="Pre-Exit Checklist", path="src/claude/skills/implementing-stories/phases/")` returns 12 matches |
| Read Phase 01 | AC1 | Verify checklist items include git-validator, session memory, context-preservation-validator |
| Read Phase 02 | AC2 | Verify checklist items include test-automator, snapshot, observation capture |
| Read Phase 04 | AC3 | Verify checklist items include light QA, code-reviewer |

---

## Acceptance Criteria Verification Checklist

### AC#1: Phase 01 Pre-Exit Checklist

- [x] Section header present in phase-01-preflight.md — **Phase:** Green — **Evidence:** Grep match
- [x] git-validator item present — **Phase:** Green — **Evidence:** Content match
- [x] Session memory item present — **Phase:** Green — **Evidence:** Content match
- [x] context-preservation-validator item present — **Phase:** Green — **Evidence:** Content match

### AC#2: Phase 02 Pre-Exit Checklist

- [x] Section header present in phase-02-test-first.md — **Phase:** Green — **Evidence:** Grep match
- [x] test-automator item present — **Phase:** Green — **Evidence:** Content match
- [x] Snapshot creation item present — **Phase:** Green — **Evidence:** Content match

### AC#3: Phase 04 Pre-Exit Checklist

- [x] Section header present in phase-04-refactoring.md — **Phase:** Green — **Evidence:** Grep match
- [x] Light QA item present — **Phase:** Green — **Evidence:** Content match

### AC#4: All 12 files have checklists

- [x] Grep returns 12 file matches — **Phase:** Green — **Evidence:** Grep count = 12

---

## Implementation Notes

<!-- FORMAT: Flat list of DoD items directly under this heading. No ### subsections before DoD items. -->
<!-- See: .claude/skills/implementing-stories/references/dod-update-workflow.md for complete details -->

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-03-02

- [x] All 12 phase files have Pre-Exit Checklist section - Completed: Added consistent checklist sections to all 12 phase files
- [x] Each checklist derives items from the phase file's existing mandatory steps - Completed: Items extracted from Validation Checkpoints and Required Subagents sections
- [x] Checklists appear BEFORE the Exit Gate section in each file - Completed: Verified placement via grep
- [x] Conditional items include "N/A — condition not met" guidance - Completed: Phase 06 deferral items include "(N/A if no deferrals)" markers
- [x] Checklists match actual phase steps (no orphaned or missing items) - Completed: Code review verified consistency
- [x] Markdown formatting correct (checkbox syntax: `- [ ]`) - Completed: All items use standard checkbox format
- [x] Consistent section header across all 12 files - Completed: All use "## Pre-Exit Checklist [MANDATORY — Display Before Exit Gate]"
- [x] Grep all 12 files for "Pre-Exit Checklist" — all match - Completed: 33/33 tests pass, 12/12 files match
- [x] Read Phase 01, 02, 04 checklists — verify items match RCA-001 REC-2 examples - Completed: AC compliance verification passed
- [x] Execute `/dev` on test story — verify checklists display before gate calls - Completed: This execution verifies the workflow
- [x] Change log entry added to this story file - Completed: Added below

## Definition of Done

### Implementation
- [x] All 12 phase files have Pre-Exit Checklist section
- [x] Each checklist derives items from the phase file's existing mandatory steps
- [x] Checklists appear BEFORE the Exit Gate section in each file
- [x] Conditional items include "N/A — condition not met" guidance

### Quality
- [x] Checklists match actual phase steps (no orphaned or missing items)
- [x] Markdown formatting correct (checkbox syntax: `- [ ]`)
- [x] Consistent section header across all 12 files

### Testing
- [x] Grep all 12 files for "Pre-Exit Checklist" — all match
- [x] Read Phase 01, 02, 04 checklists — verify items match RCA-001 REC-2 examples
- [x] Execute `/dev` on test story — verify checklists display before gate calls

### Documentation
- [x] Change log entry added to this story file

---

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| Red | Complete | 33 failing tests generated for structural validation |
| Green | Complete | Added Pre-Exit Checklists to all 12 phase files, 33/33 tests pass |
| Refactor | Complete | Code review verified consistency, no changes needed |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| 12 phase files in `src/claude/skills/implementing-stories/phases/` | Modified | +10-15 lines each |

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-03-02 | story-requirements-analyst (CLI project) | Created | Story created from RCA-001 REC-2 (originally STORY-015 in CLI project) | STORY-015.story.md |
| 2026-03-02 | opus (Framework project) | Remediated | Conformed to framework template v2.9: XML AC format, YAML frontmatter, src/ paths | STORY-015.story.md |
| 2026-03-02 | opus (Framework project) | Renumbered | STORY-015 → STORY-522 to avoid ID collision with archived stories | STORY-522.story.md |
| 2026-03-02 | .claude/qa-result-interpreter | QA Deep | PASSED: Tests 33/33, 0 violations, traceability 100% | - |

## Notes

**Source:** RCA-001 REC-2 — "Add Explicit Execution Checklist to Each Phase File"
**Origin:** DevForgeAI CLI project (separate repository). Originally STORY-015. Imported, remediated, and renumbered for framework conformance.

**Design Decisions:**
- Checklist placed at END of phase (before Exit Gate), not at beginning — ensures all steps have been attempted before displaying
- 4-12 items per checklist — focused on true mandatory items, not every sub-step
- Uses same checkbox format as story AC checklists for consistency

**Cross-Project Context:**
- STORY-014 (CLI project) provides binary-level artifact verification as defense-in-depth
- STORY-017 (CLI project) provides non-blocking observation warnings
- This story provides prompt-level enforcement complementing the CLI binary enforcement

**References:**
- RCA-001: DevForgeAI CLI project RCA document
- Phase files: `src/claude/skills/implementing-stories/phases/`

---

Story Template Version: 2.9
Last Updated: 2026-03-02
