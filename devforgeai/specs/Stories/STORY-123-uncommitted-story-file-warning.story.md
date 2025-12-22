---
id: STORY-123
title: Uncommitted Story File Warning
epic: EPIC-024
sprint: Sprint-8
status: In Development
points: 3
depends_on:
  - STORY-121
priority: Medium
assigned_to: TBD
created: 2025-12-20
format_version: "2.2"
---

# Story: Uncommitted Story File Warning

## Description

**As a** developer with multiple uncommitted story files,
**I want** preflight validation to warn me about story file conflicts,
**So that** I understand the impact of 169 uncommitted changes and can focus on current story.

This story implements EPIC-024 Feature 4: Add story-specific conflict detection to preflight validation, distinguishing "your story" vs "other stories" with clear guidance.

**Depends On:** STORY-121 (uses DEVFORGEAI_STORY scoping concept)

## Acceptance Criteria

### AC#1: Preflight Detects Uncommitted Story Files

**Given** a developer runs `/dev STORY-114` with 169 uncommitted changes including multiple `.story.md` files,
**When** preflight validation executes (Step 0.8: Story File Isolation Check),
**Then** it detects all uncommitted `.story.md` files via `git status --porcelain | grep '\.story\.md$'`.

---

### AC#2: Current Story Distinguished from Others

**Given** uncommitted story files exist,
**When** warning is displayed,
**Then** it clearly shows "Your story: STORY-114 (will be modified)" separate from "Other uncommitted stories: 21 files".

---

### AC#3: Count and Range of Other Stories Shown

**Given** STORY-100 through STORY-113 and STORY-115 through STORY-119 are uncommitted,
**When** warning is displayed,
**Then** it shows "Other uncommitted stories: 21 files" with ranges like "STORY-100 through STORY-113 (14 files)" and "STORY-115 through STORY-119 (7 files)".

---

### AC#4: User Prompted with Options

**Given** warning is displayed,
**When** preflight presents AskUserQuestion,
**Then** user can choose: "Continue with scoped commits (recommended)", "Commit other stories first", or "Show me the list".

---

### AC#5: Integration with Story-121 Scoping

**Given** user selects "Continue with scoped commits",
**When** `/dev` proceeds to TDD phases,
**Then** commits are automatically scoped to current story via DEVFORGEAI_STORY env var (from STORY-121).

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Preflight Validation"
      name: "Step 1.8: Story File Isolation Check (NEW)"
      file_path: ".claude/skills/devforgeai-development/references/preflight-validation.md"
      insertion_point: "After Step 1.7, before Step 2"
      purpose: "Warn about uncommitted story files that may conflict"

    - type: "Shell Script Logic"
      purpose: "Detect uncommitted story files"
      implementation: |
        # Get current story ID from /dev argument
        CURRENT_STORY=$1  # e.g., STORY-114

        # Find all uncommitted .story.md files
        UNCOMMITTED_STORIES=$(git status --porcelain | grep '\.story\.md$' | awk '{print $2}' | sed 's|devforgeai/specs/Stories/STORY-||' | sed 's|-.*||')

        # Separate current vs other stories
        OTHER_STORIES=$(echo "$UNCOMMITTED_STORIES" | grep -v "^${CURRENT_STORY}$" || true)
        OTHER_COUNT=$(echo "$OTHER_STORIES" | wc -l)

        if [ "$OTHER_COUNT" -gt 0 ]; then
          Display warning with story ranges
          Ask user for action

  warning_display:
    format: "Box with +------+ borders"
    content:
      - title: "WARNING: UNCOMMITTED STORY FILES DETECTED"
      - current_story: "Your story: STORY-114 (will be modified by this /dev run)"
      - other_count: "Other uncommitted stories: 21 files"
      - ranges: "- STORY-100 through STORY-113 (14 files)"
      - ranges_cont: "- STORY-115 through STORY-119 (7 files)"
      - impact: "Git commits will include ONLY your story (scoped)"
      - impact_cont: "Pre-commit validation will focus on STORY-114"
      - impact_cont2: "Other story files remain uncommitted"

  user_options:
    - option: "Continue with scoped commits (recommended)"
      effect: "Proceeds with DEVFORGEAI_STORY=STORY-114 env var set"
      integration: "Uses STORY-121 scoping"
    - option: "Commit other stories first (I'll do this manually)"
      effect: "HALTS with message: 'Please commit other stories, then re-run /dev'"
    - option: "Show me the list of uncommitted files"
      effect: "Lists all uncommitted story files with git status output"

  data_extraction:
    - method: "git status --porcelain"
      parse: "Extract .story.md files from output"
      result: "List of uncommitted story IDs"
    - method: "Range detection"
      parse: "Detect consecutive story numbers (e.g., 100-113)"
      result: "Human-readable range format"
```

## Non-Functional Requirements

| Requirement | Target | Justification |
|-------------|--------|---------------|
| Detection latency | <100ms | Minimal preflight delay |
| Accuracy | 100% for story file detection | Must correctly identify all .story.md files |
| User clarity | Clear visual separation | Distinguish current story from others |

## Test Strategy

### Unit Tests
- **Test 1:** Correctly parse git status output for .story.md files
- **Test 2:** Separate current story from other stories
- **Test 3:** Count other uncommitted stories
- **Test 4:** Format story ranges (100-113, 115-119)

### Integration Tests
- **Test 5:** Warning displays when uncommitted stories exist
- **Test 6:** Warning includes correct story counts and ranges
- **Test 7:** User can select "Continue with scoped commits"
- **Test 8:** DEVFORGEAI_STORY env var set when proceeding (integration with STORY-121)
- **Test 9:** "Commit other stories first" option HALTs workflow appropriately
- **Test 10:** "Show me the list" option displays full git status output

### Edge Cases
- **Test 11:** No uncommitted stories (skips warning)
- **Test 12:** Only current story uncommitted (no warning)
- **Test 13:** Non-consecutive story numbers (ranges formatted correctly, e.g., 100-105, 110-115)
- **Test 14:** Single uncommitted other story (displays as "STORY-115" not range)

## Definition of Done

### Implementation
- [ ] `.claude/skills/devforgeai-development/references/preflight-validation.md` updated with Step 1.8
- [ ] Story file detection logic implemented in shell
- [ ] Range detection algorithm implemented
- [ ] Warning display formatted with visual clarity
- [ ] AskUserQuestion integrated with 3 options
- [ ] DEVFORGEAI_STORY env var set when "Continue" selected (integration with STORY-121)

### Quality
- [ ] All unit tests passing (4 tests)
- [ ] All integration tests passing (6 tests)
- [ ] All edge cases handled (4 tests)
- [ ] No performance impact on preflight (detects in <100ms)

### Testing
- [ ] Manual test: 169 uncommitted changes, warning displays correctly
- [ ] Manual test: Story ranges formatted properly (100-113, not 100-113 for each)
- [ ] Manual test: User selects "Continue", subsequent commits scoped to STORY-114
- [ ] Manual test: No warning when only current story uncommitted
- [ ] Manual test: "Show me the list" displays accurate git status output

### Documentation
- [ ] preflight-validation.md documents Step 1.8 with examples
- [ ] Comments explain range detection algorithm
- [ ] Examples show warning for different scenarios (2 uncommitted, 50 uncommitted, etc.)

### Release
- [ ] All tests passing
- [ ] Integration with STORY-121 verified
- [ ] Edge cases handled
- [ ] Ready for QA validation

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2025-12-22
**Status:** In Development

*Implementation details will be added during TDD workflow execution.*

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released
