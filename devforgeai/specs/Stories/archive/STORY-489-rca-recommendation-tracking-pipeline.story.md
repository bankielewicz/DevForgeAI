---
id: STORY-489
title: RCA Recommendation-to-Story Tracking Pipeline
type: feature
epic: null
sprint: Backlog
status: QA Approved ✅
points: 2
depends_on: []
priority: High
advisory: false
source_gap: null
source_story: null
source_rca: "RCA-039"
source_recommendation: "REC-4"
assigned_to: DevForgeAI AI Agent
created: 2026-02-22
format_version: "2.9"
---

# Story: RCA Recommendation-to-Story Tracking Pipeline

## Description

**As a** framework maintainer completing an RCA,
**I want** the RCA skill to automatically prompt for story creation or debt tracking for each CRITICAL/HIGH recommendation after the RCA document is written,
**so that** RCA recommendations are never left as untracked documentation — preventing the root cause identified in RCA-039 where RCA-033's recommendation was documented but never implemented for 27 days.

## Provenance

```xml
<provenance>
  <origin document="RCA-039" section="REC-4">
    <quote>"The framework has no mechanism to track RCA recommendation implementation. RCA documents are created as standalone .md files but recommendations are never automatically converted to stories."</quote>
    <line_reference>RCA-039 lines 247-283</line_reference>
    <quantified_impact>RCA-033 REC-2 was open for 27 days without implementation, causing RCA-039 recurrence</quantified_impact>
  </origin>
</provenance>
```

## Acceptance Criteria

### AC#1: Phase 7.5 Added to RCA Skill

```xml
<acceptance_criteria id="AC1">
  <given>the devforgeai-rca skill has Phase 7 (Completion Report) as its final phase</given>
  <when>the skill file is inspected after implementation</when>
  <then>a "Phase 7.5: Recommendation-to-Story Pipeline" section exists after Phase 7 and before the Error Handling section</then>
  <verification>
    <source_files>
      <file hint="RCA skill">src/claude/skills/devforgeai-rca/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-489/test_ac1_phase_exists.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#2: Prompts for CRITICAL/HIGH Recommendations Only

```xml
<acceptance_criteria id="AC2">
  <given>an RCA with 2 CRITICAL, 1 HIGH, 1 MEDIUM, and 1 LOW recommendation</given>
  <when>Phase 7.5 executes</when>
  <then>AskUserQuestion is invoked exactly 3 times (once per CRITICAL/HIGH recommendation), and MEDIUM/LOW recommendations are skipped with informational note</then>
  <verification>
    <source_files>
      <file hint="RCA skill Phase 7.5">src/claude/skills/devforgeai-rca/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-489/test_ac2_priority_filter.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#3: Three Action Options Per Recommendation

```xml
<acceptance_criteria id="AC3">
  <given>Phase 7.5 is processing a CRITICAL recommendation</given>
  <when>AskUserQuestion is displayed</when>
  <then>three options are presented: "Create story now" (displays /create-story command), "Add to technical debt register" (appends to technical-debt-register.md), "Skip" (acknowledged, no action)</then>
  <verification>
    <source_files>
      <file hint="RCA skill Phase 7.5">src/claude/skills/devforgeai-rca/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-489/test_ac3_action_options.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#4: Debt Register Append Works

```xml
<acceptance_criteria id="AC4">
  <given>user selects "Add to technical debt register" for a recommendation</given>
  <when>Phase 7.5 processes the selection</when>
  <then>an entry is appended to devforgeai/technical-debt-register.md with the RCA number, recommendation ID, priority, title, and "Source: RCA-NNN REC-N" provenance</then>
  <verification>
    <source_files>
      <file hint="debt register">devforgeai/technical-debt-register.md</file>
    </source_files>
    <test_file>tests/STORY-489/test_ac4_debt_append.sh</test_file>
  </verification>
</acceptance_criteria>
```

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  dual_path_sync:
    note: "Per source-tree.md dual-path architecture, development happens in src/ tree."
    source_paths:
      - "src/claude/skills/devforgeai-rca/SKILL.md"
    operational_paths:
      - ".claude/skills/devforgeai-rca/SKILL.md"
    test_against: "src/"

  components:
    - type: "Configuration"
      name: "rca-phase-7-5"
      file_path: "src/claude/skills/devforgeai-rca/SKILL.md"
      required_keys:
        - key: "Phase 7.5 section"
          type: "string"
          required: true
          validation: "Phase 7.5 exists after Phase 7"
          test_requirement: "Test: Grep for 'Phase 7.5' in SKILL.md"

  business_rules:
    - id: "BR-001"
      rule: "Only CRITICAL and HIGH recommendations trigger prompts"
      trigger: "Phase 7.5 execution"
      validation: "MEDIUM/LOW recommendations skipped"
      error_handling: "Display informational note for skipped recommendations"
      test_requirement: "Test: MEDIUM recommendation does not trigger AskUserQuestion"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Reliability"
      requirement: "Phase 7.5 failure does not prevent RCA completion"
      metric: "RCA document already written in Phase 5"
      test_requirement: "Test: Phase 7.5 error → RCA still valid"
      priority: "High"
```

## Technical Limitations

```yaml
technical_limitations: []
```

## Dependencies

### Prerequisite Stories
- None

## Test Strategy

### Unit Tests
**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** RCA with CRITICAL recs → prompted for each
2. **Edge Cases:** All LOW recs → no prompts; user selects Skip for all; debt register missing
3. **Error Cases:** Phase 7.5 fails → RCA document still valid

## Acceptance Criteria Verification Checklist

- [x] Phase 7.5 exists in SKILL.md - **Phase:** 3
- [x] Only CRITICAL/HIGH prompted - **Phase:** 2
- [x] Three options per prompt - **Phase:** 2
- [x] Debt register append works - **Phase:** 2

**Checklist Progress:** 4/4 items complete (100%)

## Definition of Done

### Implementation
- [x] Phase 7.5 section added to devforgeai-rca SKILL.md
- [x] AskUserQuestion loop for CRITICAL/HIGH recommendations
- [x] Three options: create story, add to debt, skip
- [x] Debt register append logic
- [x] MEDIUM/LOW skip with informational note

### Dual-Path Sync
- [x] File modified in src/claude/skills/ (source of truth)
- [x] File synced to .claude/skills/ (operational) — Complete
- [x] Tests run against src/ tree

### Quality
- [x] All 4 acceptance criteria have passing tests

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-23

- [x] Phase 7.5 section added to devforgeai-rca SKILL.md - Completed: Added "Phase 7.5: Recommendation-to-Story Pipeline" section between Phase 7 and Error Handling
- [x] AskUserQuestion loop for CRITICAL/HIGH recommendations - Completed: Priority filtering extracts CRITICAL/HIGH recs for interactive prompts
- [x] Three options: create story, add to debt, skip - Completed: AskUserQuestion presents 3 options with appropriate actions
- [x] Debt register append logic - Completed: Edit-based append to technical-debt-register.md with Source: RCA-NNN REC-N provenance
- [x] MEDIUM/LOW skip with informational note - Completed: Skipped recs display "Skipping {count} MEDIUM/LOW recommendations (informational only)"
- [x] File modified in src/claude/skills/ (source of truth) - Completed: src/claude/skills/devforgeai-rca/SKILL.md modified
- [x] Tests run against src/ tree - Completed: All 17 assertions pass across 4 test files
- [x] All 4 acceptance criteria have passing tests - Completed: AC#1-4 all PASS with HIGH confidence

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| Phase 02 (Red) | ✅ Complete | 4 test files, 17 assertions, all RED |
| Phase 03 (Green) | ✅ Complete | Phase 7.5 added, all 17 tests GREEN |
| Phase 04 (Refactor) | ✅ Complete | Minor improvements, tests still pass |
| Phase 4.5 (AC Verify) | ✅ Complete | 4/4 ACs PASS |
| Phase 05 (Integration) | ✅ Complete | All integration points verified |
| Phase 5.5 (AC Verify) | ✅ Complete | 4/4 ACs PASS (final) |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/skills/devforgeai-rca/SKILL.md | Modified | +~100 (Phase 7.5 section) |
| tests/STORY-489/test_ac1_phase_exists.sh | Created | 53 |
| tests/STORY-489/test_ac2_priority_filter.sh | Created | 51 |
| tests/STORY-489/test_ac3_action_options.sh | Created | 51 |
| tests/STORY-489/test_ac4_debt_append.sh | Created | 48 |
| tests/STORY-489/run_all_tests.sh | Created | 25 |

## Change Log

**Current Status:** Dev Complete

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-22 | /create-stories-from-rca | Created | Story created from RCA-039 REC-4 (ROOT CAUSE fix) | STORY-489.story.md |

## Notes

**Design Decisions:**
- This is the ROOT CAUSE fix from RCA-039 — without tracking, RCA recommendations decay into dead documentation
- Phase 7.5 (not Phase 8) because the RCA document is already complete in Phase 5; this is a post-completion action
- /create-stories-from-rca command already exists — Phase 7.5 reminds users to use it, not replaces it
- Failure isolation: Phase 7.5 errors don't invalidate the RCA document

**References:**
- [RCA-039](devforgeai/RCA/RCA-039-dual-path-architecture-validation-gap.md) (REC-4, ROOT CAUSE)
- [/create-stories-from-rca](.claude/commands/create-stories-from-rca.md) (existing command)

---

Story Template Version: 2.9
Last Updated: 2026-02-22
