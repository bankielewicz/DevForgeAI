---
id: STORY-156
title: Interactive Recommendation Selection
type: feature
epic: EPIC-032
priority: Medium
points: 4
depends_on: ["STORY-155"]
status: Dev Complete
created: 2025-12-25
---

# STORY-156: Interactive Recommendation Selection

## User Story

**As a** DevForgeAI developer,
**I want** to interactively select which RCA recommendations to convert to stories,
**So that** I maintain control over story creation and can prioritize which fixes to implement first.

## Acceptance Criteria

### AC#1: Display Recommendation Summary Table

**Given** an RCA document has been parsed with multiple recommendations
**When** the command displays the parsed recommendations
**Then** a formatted table shows: REC ID, Priority, Title, Effort Estimate for each recommendation

### AC#2: Multi-Select Recommendations via AskUserQuestion

**Given** the recommendation summary table is displayed
**When** the user is prompted to select recommendations
**Then** AskUserQuestion presents options with multiSelect: true, allowing selection of multiple recommendations

### AC#3: Handle Select All Option

**Given** the user wants to convert all eligible recommendations
**When** the user selects "All recommendations" option
**Then** all recommendations meeting the effort threshold are selected for story creation

### AC#4: Handle Select None (Cancel)

**Given** the user decides not to create any stories
**When** the user selects "None - cancel" option
**Then** the command exits gracefully with message "No recommendations selected. Exiting."

### AC#5: Pass Selection to Batch Story Creation

**Given** the user has selected one or more recommendations
**When** the selection is confirmed
**Then** the selected recommendations are passed to the batch story creation phase with all metadata preserved

## Technical Specification

```yaml
technical_specification:
  version: "2.0"
  components:
    - type: Service
      name: RecommendationSelector
      path: .claude/commands/create-stories-from-rca.md
      description: Display recommendations and collect user selection
      dependencies:
        - AskUserQuestion tool
        - STORY-155 RCAParser output
      test_requirement: Selector displays all recommendations and captures user selection correctly

    - type: Configuration
      name: SelectionOptions
      description: AskUserQuestion configuration for recommendation selection
      fields:
        - name: question
          value: "Which recommendations should be converted to stories?"
        - name: header
          value: "Select Recommendations"
        - name: multiSelect
          value: true
        - name: options
          value: Dynamic list from parsed recommendations + "All" + "None"
      test_requirement: AskUserQuestion displays with correct options and multiSelect enabled

  business_rules:
    - id: BR-001
      name: Minimum One Selection
      description: At least one recommendation must be selected (or explicit cancel)
      test_requirement: Empty selection without cancel triggers re-prompt

    - id: BR-002
      name: Preserve Metadata
      description: Selected recommendations retain all parsed metadata for story creation
      test_requirement: Selected recommendations include priority, effort, success criteria

  non_functional_requirements:
    - category: Usability
      requirement: Clear table format with aligned columns
      metric: Table readable in terminal width 80+ chars
      test_requirement: Table displays correctly in standard terminal

    - category: Performance
      requirement: Display immediately after parsing
      metric: No additional file reads or processing
      test_requirement: Selection prompt appears within 1 second of parsing
```

## Edge Cases

1. **Single recommendation:** RCA has only one eligible recommendation. Still display selection prompt (allow cancel).

2. **All filtered out:** All recommendations have effort < threshold. Display "No recommendations meet effort threshold" and exit.

3. **User selects "Other":** User types custom selection. Parse as comma-separated REC IDs.

4. **Invalid selection:** User types invalid REC ID. Log warning and ignore invalid entries.

## Non-Functional Requirements

- **Usability:** Table format with aligned columns, readable in 80-char terminal
- **Performance:** Selection prompt appears within 1 second of parsing
- **Accessibility:** Clear labels and descriptions for each option

## Definition of Done

### Implementation
- [x] Recommendation summary table display implemented (Phase 6)
- [x] AskUserQuestion with multiSelect configured (Phase 7)
- [x] All recommendations option implemented (Phase 7, 8)
- [x] None-cancel option implemented (Phase 7, 8)
- [x] Selection passed to batch creation phase (Phase 9)

### Quality
- [x] All 5 acceptance criteria have passing tests (50/50 tests pass)
- [x] Table format verified in terminal (80-char width compatible)
- [x] Edge cases handled gracefully (4 new edge cases documented)

### Testing
- [x] Unit test for table formatting (tests/results/STORY-156/test_ac1_display_recommendation_summary_table.sh)
- [x] Unit test for selection parsing (tests/results/STORY-156/test_ac2_multiselect_via_askuserquestion.sh)
- [x] Integration test with AskUserQuestion (validated via integration-tester subagent)

### Documentation
- [x] Selection flow documented in command help (added 5-step flow in header)

## Implementation Notes

- [x] Recommendation summary table display implemented (Phase 6)
- [x] AskUserQuestion with multiSelect configured (Phase 7)
- [x] All recommendations option implemented (Phase 7, 8)
- [x] None-cancel option implemented (Phase 7, 8)
- [x] Selection passed to batch creation phase (Phase 9)
- [x] All 5 acceptance criteria have passing tests (50/50 tests pass)
- [x] Table format verified in terminal (80-char width compatible)
- [x] Edge cases handled gracefully (4 new edge cases documented)
- [x] Unit test for table formatting
- [x] Unit test for selection parsing
- [x] Integration test with AskUserQuestion
- [x] Selection flow documented in command help

**Developer:** claude/opus
**Implemented:** 2025-12-30

### TDD Workflow Summary

- **Red Phase:** 60 tests generated, 30+ failures confirmed
- **Green Phase:** All 50 AC tests passing (100%)
- **Refactor Phase:** Helper function extracted, comments simplified
- **Integration Phase:** STORY-155 dependency validated, data contracts verified

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-25 | DevForgeAI | Story created via /create-missing-stories batch mode |
| 2025-12-30 | claude/opus | TDD implementation complete - Phases 6-9 added to create-stories-from-rca.md |
