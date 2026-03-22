---
id: STORY-494
title: Add Full Read Mandatory Markers to Story Creation Skill Read Directives
type: feature
epic: null
sprint: Backlog
status: QA Approved
points: 2
depends_on: []
priority: Medium
advisory: false
source_gap: null
source_story: null
assigned_to: null
created: 2026-02-23
format_version: "2.9"
---

# Story: Add Full Read Mandatory Markers to Story Creation Skill Read Directives

## Description

**As a** DevForgeAI skill agent executing the story creation workflow,
**I want** explicit "FULL READ MANDATORY — do not use offset/limit" comments on all 23 Read() directives in devforgeai-story-creation SKILL.md,
**so that** the intent of full file loading is unambiguous and partial reads are explicitly prohibited.

**Source:** RCA-040 (Story Creation Skill Phase Execution Skipping), REC-3

## Acceptance Criteria

### AC#1: All Read() directives have FULL READ MANDATORY comment

```xml
<acceptance_criteria id="AC1" implements="COMP-001">
  <given>The devforgeai-story-creation SKILL.md contains 23 Read() directives across 8 phases</given>
  <when>Each Read() directive is examined</when>
  <then>Each Read() line or its immediately preceding line contains the comment "FULL READ MANDATORY — do not use offset/limit"</then>
  <verification>
    <source_files>
      <file hint="Skill definition (src)">src/claude/skills/devforgeai-story-creation/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-494/test_ac1_full_read_markers.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Read directive count matches after modification

```xml
<acceptance_criteria id="AC2" implements="COMP-001">
  <given>SKILL.md had 23 Read() directives before modification</given>
  <when>The markers are added</when>
  <then>SKILL.md still has exactly 23 Read() directives (no directives added or removed) and each has a corresponding FULL READ MANDATORY marker</then>
  <verification>
    <source_files>
      <file hint="Skill definition (src)">src/claude/skills/devforgeai-story-creation/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-494/test_ac2_directive_count.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: No existing content modified beyond comment additions

```xml
<acceptance_criteria id="AC3">
  <given>The existing SKILL.md content</given>
  <when>FULL READ MANDATORY comments are added</when>
  <then>Only comment lines are added; no existing lines are modified, removed, or reordered</then>
  <verification>
    <source_files>
      <file hint="Skill definition (src)">src/claude/skills/devforgeai-story-creation/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-494/test_ac3_no_content_modified.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "Full Read Mandatory Markers"
      file_path: "src/claude/skills/devforgeai-story-creation/SKILL.md"
      requirements:
        - id: "COMP-001"
          description: "Add FULL READ MANDATORY comment to each of the 23 Read() directives in SKILL.md"
          testable: true
          test_requirement: "Test: Grep for 'FULL READ MANDATORY' count equals 23, Grep for 'Read(file_path=' count equals 23"
          priority: "Medium"
          implements_ac: ["AC#1", "AC#2"]

  business_rules:
    - id: "BR-001"
      rule: "Comments are additive only — no existing SKILL.md content modified"
      test_requirement: "Test: Diff before/after shows only added lines (+ prefix), no removed lines (- prefix)"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Reliability"
      requirement: "Comment marker complements REC-1 mechanical checkpoints"
      metric: "Prompt-level + mechanical enforcement = defense in depth"
      test_requirement: "Test: Verify markers present alongside checkpoint gates"
```

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "Prompt-only enforcement"
    limitation: "Comments alone cannot prevent partial reads — they complement REC-1 mechanical gates"
    decision: "workaround:Defense in depth with REC-1 checkpoints"
    discovered_phase: "Architecture"
    impact: "Low — markers reduce ambiguity but depend on REC-1 for enforcement"
```

## Non-Functional Requirements (NFRs)

### Performance

- Zero runtime impact (comments only)

---

### Security

- No code changes, comments only

---

### Scalability

- Pattern applies to any skill with Read() directives

---

### Reliability

- Complements REC-1 mechanical checkpoints for defense in depth

---

### Observability

- Markers are Greppable for audit: `Grep(pattern="FULL READ MANDATORY")`

---

## Dependencies

### Prerequisite Stories

None (can be implemented independently of STORY-492).

### External Dependencies

None.

### Technology Dependencies

None.

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** Count of FULL READ MANDATORY markers equals 23
2. **Edge Cases:** Markers on inline comments vs preceding-line comments both valid
3. **Error Cases:** Missing marker on any Read() directive → test fails

---

### Integration Tests

**Coverage Target:** 85%+

**Test Scenarios:**
1. **Skill still functional:** Story creation skill executes normally with markers present

---

## Acceptance Criteria Verification Checklist

**Purpose:** Real-time progress tracking during TDD implementation.

### AC#1: All Read() directives have FULL READ MANDATORY comment

- [ ] 23 FULL READ MANDATORY markers present - **Phase:** 1 - **Evidence:** test file
- [ ] Each marker associated with a Read() directive - **Phase:** 1 - **Evidence:** test file

### AC#2: Read directive count matches after modification

- [ ] 23 Read() directives remain - **Phase:** 1 - **Evidence:** test file
- [ ] 1:1 ratio of markers to directives - **Phase:** 1 - **Evidence:** test file

### AC#3: No existing content modified

- [ ] Only added lines in diff - **Phase:** 1 - **Evidence:** git diff

---

**Checklist Progress:** 0/5 items complete (0%)

---

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT (Critical for pre-commit validation):
When filling in the Implementation Notes section during /dev workflow:
1. DoD items MUST be placed DIRECTLY under "## Implementation Notes" header
2. NO ### subsection headers before DoD items
See: src/claude/skills/implementing-stories/references/dod-update-workflow.md for complete details
-->

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-23

- [x] FULL READ MANDATORY comment added to all 23 Read() directives - Completed: Added 25 HTML comment markers (actual count is 25, story spec said 23 but file had 25 directives) to src/claude/skills/devforgeai-story-creation/SKILL.md
- [x] No existing SKILL.md content modified or removed - Completed: Only additive comment lines inserted, all original content preserved
- [x] Comments clearly state "do not use offset/limit" - Completed: Each marker reads "FULL READ MANDATORY — do not use offset/limit"
- [x] All 3 acceptance criteria have passing tests - Completed: 3 test files with 8 assertions, all passing
- [x] Marker count verified (23) - Completed: Verified 25 markers (actual count), 1:1 ratio with Read() directives
- [x] No content regressions - Completed: Integration tests confirm file structure intact
- [x] Unit tests for marker count - Completed: test_ac1_full_read_markers.sh validates count=25
- [x] Unit tests for directive-marker pairing - Completed: test_ac1 validates each Read() has preceding marker
- [x] All tests passing (100% pass rate) - Completed: 8/8 assertions pass across 3 test files
- [x] RCA-040 linked in story notes - Completed: Story references RCA-040 REC-3 in Notes section

## Definition of Done

### Implementation
- [x] FULL READ MANDATORY comment added to all 23 Read() directives
- [x] No existing SKILL.md content modified or removed
- [x] Comments clearly state "do not use offset/limit"

### Quality
- [x] All 3 acceptance criteria have passing tests
- [x] Marker count verified (23)
- [x] No content regressions

### Testing
- [x] Unit tests for marker count
- [x] Unit tests for directive-marker pairing
- [x] All tests passing (100% pass rate)

### Documentation
- [x] RCA-040 linked in story notes

---

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| Red | ✅ Complete | 3 test files, 8 assertions (all failing) |
| Green | ✅ Complete | 25 FULL READ MANDATORY markers added |
| Refactor | ✅ Complete | No refactoring needed (comment-only changes) |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/skills/devforgeai-story-creation/SKILL.md | Modified | +25 comment lines |
| tests/STORY-494/test_ac1_full_read_markers.sh | Created | ~71 lines |
| tests/STORY-494/test_ac2_directive_count.sh | Created | ~54 lines |
| tests/STORY-494/test_ac3_no_content_modified.sh | Created | ~71 lines |
| tests/STORY-494/run_all_tests.sh | Created | ~30 lines |

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-23 | .claude/story-requirements-analyst | Created | Story created from RCA-040 REC-3 | STORY-494.story.md |
| 2026-02-23 | .claude/qa-result-interpreter | QA Deep | PASSED: 8/8 tests, 0 violations, 3/3 validators | - |

## Notes

**Source RCA:** RCA-040 (Story Creation Skill Phase Execution Skipping)
**Source Recommendation:** REC-3 (Add "FULL READ MANDATORY" Markers)

**Design Decisions:**
- Comment format chosen for Greppability and unambiguous intent
- Complements STORY-492 (mechanical checkpoints) for defense in depth

**Related RCAs:**
- RCA-040: Story Creation Skill Phase Execution Skipping

**References:**
- `src/claude/skills/devforgeai-story-creation/SKILL.md` (target file)

---

Story Template Version: 2.9
Last Updated: 2026-02-23
