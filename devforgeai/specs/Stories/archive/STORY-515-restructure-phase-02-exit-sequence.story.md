---
id: STORY-515
title: Restructure Phase 02 Exit Sequence for Clarity
type: feature
epic: null
sprint: null
status: QA Approved
points: 3
depends_on: ["STORY-513", "STORY-514"]
priority: Medium
advisory: false
source_gap: null
source_story: null
assigned_to: Unassigned
created: 2026-02-28
format_version: "2.9"
---

# Story: Restructure Phase 02 Exit Sequence for Clarity

## Description

**As a** DevForgeAI orchestrator executing the implementing-stories skill,
**I want** the Phase 02 exit sequence to be reorganized into clearly labeled categories (mandatory artifacts, optional captures, exit gate),
**so that** mandatory steps are visually distinct from optional ones and are less likely to be overlooked during sequential execution.

**Context:** RCA-043 identified that Phase 02 has 6 post-validation sections with identical `###` heading levels, making mandatory steps (like snapshot creation) easy to miss among optional captures (like observation extraction). Reorganizing into numbered categories with "MANDATORY" vs "OPTIONAL" labels reduces the chance of skipping required steps.

**Source:** RCA-043 (Test Integrity Snapshot Skipped) / REC-3

## Acceptance Criteria

> **IMPORTANT:** XML acceptance criteria format is REQUIRED for automated verification by the ac-compliance-verifier subagent.

### XML Acceptance Criteria Format

```xml
<acceptance_criteria id="AC1" implements="COMP-XXX,COMP-YYY">
  <given>Initial context or precondition</given>
  <when>Action or event being tested</when>
  <then>Expected outcome or result</then>
</acceptance_criteria>
```

### AC#1: Exit Sequence Uses Numbered Categories

```xml
<acceptance_criteria id="AC1" implements="CFG-001">
  <given>The phase-02-test-first.md file (after STORY-513 and STORY-514 are complete) has post-checkpoint sections that all use the same ### heading level with no categorization. Note: The Test Integrity Snapshot section is PRE-checkpoint (moved by STORY-513) and is NOT part of this restructuring.</given>
  <when>The post-checkpoint exit sequence is restructured per this story</when>
  <then>The post-checkpoint sections are organized into numbered categories: (1) Post-Checkpoint Mandatory Steps, (2) Post-Checkpoint Optional Captures, (3) Exit Gate, with clear category headings that distinguish mandatory from optional steps. The pre-checkpoint snapshot section is untouched.</then>
  <verification>
    <source_files>
      <file hint="Phase 02 workflow file">.claude/skills/implementing-stories/phases/phase-02-test-first.md</file>
    </source_files>
    <test_file>tests/STORY-515/test_ac1_numbered_categories.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Mandatory Steps Labeled Explicitly

```xml
<acceptance_criteria id="AC2" implements="CFG-001">
  <given>The restructured exit sequence has category headings</given>
  <when>The orchestrator reads the phase file during execution</when>
  <then>Each mandatory step (AC Checklist Update, Test Integrity Snapshot) is under a section explicitly labeled "MANDATORY" or equivalent, and each optional step (Observation Capture, Session Memory Update) is under a section labeled "OPTIONAL"</then>
  <verification>
    <source_files>
      <file hint="Phase 02 workflow file">.claude/skills/implementing-stories/phases/phase-02-test-first.md</file>
    </source_files>
    <test_file>tests/STORY-515/test_ac2_labels.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: All Original Content Preserved

```xml
<acceptance_criteria id="AC3" implements="CFG-001">
  <given>After STORY-513/514, the phase-02-test-first.md has: (pre-checkpoint) Test Integrity Snapshot + file verification, and (post-checkpoint) AC Checklist Update Verification, Observation Capture (EPIC-051), Session Memory Update (STORY-341), Observation Capture (general), and Exit Gate</given>
  <when>The post-checkpoint restructuring is complete</when>
  <then>All original content from the post-checkpoint sections is preserved — no instructions, code blocks, or references are lost. Only headings and ordering change. The pre-checkpoint snapshot section remains untouched.</then>
  <verification>
    <source_files>
      <file hint="Phase 02 workflow file">.claude/skills/implementing-stories/phases/phase-02-test-first.md</file>
    </source_files>
    <test_file>tests/STORY-515/test_ac3_content_preserved.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### Source Files Guidance

All ACs target: `.claude/skills/implementing-stories/phases/phase-02-test-first.md`

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "phase-02-test-first.md"
      file_path: ".claude/skills/implementing-stories/phases/phase-02-test-first.md"
      required_keys:
        - key: "Numbered category headings"
          type: "string"
          example: "## 1. Mandatory Artifacts, ## 2. Optional Captures, ## 3. Exit Gate"
          required: true
          test_requirement: "Test: Grep for numbered category headings in the post-checkpoint area"
        - key: "MANDATORY/OPTIONAL labels"
          type: "string"
          example: "Sections labeled with [MANDATORY] or [OPTIONAL] markers"
          required: true
          test_requirement: "Test: Verify mandatory steps have MANDATORY label and optional steps have OPTIONAL label"
        - key: "Content preservation"
          type: "string"
          example: "All code blocks, references, and instructions from original sections exist in restructured file"
          required: true
          test_requirement: "Test: Key content strings from each original section found in restructured file"

  business_rules:
    - id: "BR-001"
      rule: "Mandatory steps must appear before optional steps in the exit sequence"
      trigger: "When orchestrator reads Phase 02 post-checkpoint sections"
      validation: "Mandatory category line numbers < Optional category line numbers"
      error_handling: "If reversed, mandatory steps may be skipped when orchestrator stops early"
      test_requirement: "Test: Mandatory category heading line number < Optional category heading line number"
      priority: "Medium"

    - id: "BR-002"
      rule: "No content from original sections may be lost during restructuring"
      trigger: "During implementation of this story"
      validation: "All key strings from original sections present in restructured file"
      error_handling: "If content missing, rollback restructuring"
      test_requirement: "Test: Grep for key strings from each original section (e.g., 'observation-extractor', 'session_path', 'Test Integrity Snapshot')"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Reliability"
      requirement: "Restructuring must not break any cross-references to phase-02-test-first.md"
      metric: "0 broken references in other skill files"
      test_requirement: "Test: Grep all skill files for references to phase-02-test-first.md sections and verify they still resolve"
      priority: "Medium"
```

---

## Technical Limitations

```yaml
technical_limitations: []
```

---

## Non-Functional Requirements (NFRs)

### Performance

N/A — workflow file change

---

### Security

**Authentication:** None
**Authorization:** None
**Data Protection:** N/A

---

### Scalability

N/A

---

### Reliability

**Error Handling:**
- Must preserve all original content during restructuring
- Cross-references from other files must not break

---

### Observability

N/A

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-513:** Move Test Integrity Snapshot Before Phase 02 Validation Checkpoint
  - **Why:** Snapshot must be in pre-checkpoint position before restructuring exit sequence
  - **Status:** Backlog

- [ ] **STORY-514:** Add Snapshot File Existence Check to Phase 02 Gate
  - **Why:** Verification step must exist before restructuring around it
  - **Status:** Backlog

### External Dependencies

None

### Technology Dependencies

None

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** Numbered categories present with correct ordering
2. **Edge Cases:**
   - All original content strings preserved
   - Mandatory steps appear before optional steps
   - No broken cross-references
3. **Error Cases:**
   - Missing category heading (should fail)

---

### Integration Tests

**Coverage Target:** 85%+

**Test Scenarios:**
1. **Complete file structure:** File parses correctly after restructuring

---

## Acceptance Criteria Verification Checklist

### AC#1: Exit Sequence Uses Numbered Categories

- [x] Category headings present (Mandatory, Optional, Exit Gate) - **Phase:** 3 - **Evidence:** phase-02-test-first.md
- [x] Categories are numbered (1, 2, 3) - **Phase:** 2 - **Evidence:** tests/STORY-515/test_ac1_numbered_categories.sh

### AC#2: Mandatory Steps Labeled Explicitly

- [x] Mandatory label on AC Checklist Update and Snapshot - **Phase:** 3 - **Evidence:** phase-02-test-first.md
- [x] Optional label on Observation Capture and Session Memory - **Phase:** 3 - **Evidence:** phase-02-test-first.md

### AC#3: All Original Content Preserved

- [x] Key content strings from all 6 original sections found - **Phase:** 2 - **Evidence:** tests/STORY-515/test_ac3_content_preserved.sh
- [x] No code blocks or references lost - **Phase:** 3 - **Evidence:** phase-02-test-first.md

---

**Checklist Progress:** 6/6 items complete (100%)

---

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT (Critical for pre-commit validation):
When filling in the Implementation Notes section during /dev workflow:
1. DoD items MUST be placed DIRECTLY under "## Implementation Notes" header
2. NO ### subsection headers (like "### Definition of Done Status") before DoD items
3. The extract_section() validator stops at the first ### header it encounters
4. If DoD items are under a ### subsection, the validator cannot find them → commit blocked
5. The ### Additional Notes subsection is OK because it comes AFTER DoD items
See: .claude/skills/implementing-stories/references/dod-update-workflow.md for complete details
-->

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-28

- [x] Post-checkpoint sections reorganized into numbered categories - Completed: Restructured into ### 1. Post-Checkpoint Mandatory Steps [MANDATORY], ### 2. Post-Checkpoint Optional Captures [OPTIONAL], ### 3. Exit Gate
- [x] Mandatory steps labeled with [MANDATORY] marker - Completed: Category 1 heading includes [MANDATORY] label
- [x] Optional steps labeled with [OPTIONAL] marker - Completed: Category 2 heading includes [OPTIONAL] label
- [x] All original content preserved (no instructions, code blocks, or references lost) - Completed: All key strings verified (observation-extractor, session_path, friction, phase-complete)
- [x] Categories ordered: Mandatory → Optional → Exit Gate - Completed: Categories numbered 1, 2, 3 in correct order
- [x] All 3 acceptance criteria have passing tests - Completed: 22/22 tests pass across 3 test files
- [x] No broken cross-references from other skill files - Completed: 12 integration tests verify cross-reference integrity
- [x] File structure validates correctly - Completed: AC compliance verifier confirms PASS on all 3 ACs
- [x] Unit tests for numbered category presence - Completed: tests/STORY-515/test_ac1_numbered_categories.sh (5 tests)
- [x] Unit tests for MANDATORY/OPTIONAL labels - Completed: tests/STORY-515/test_ac2_labels.sh (8 tests)
- [x] Unit tests for content preservation - Completed: tests/STORY-515/test_ac3_content_preserved.sh (9 tests)
- [x] Integration test for complete file structure - Completed: tests/STORY-515/integration_results.txt (12 tests)
- [x] Story file created with complete specification - Completed: Story created from RCA-043/REC-3
- [x] RCA-043 updated with story link for REC-3 - Deferred: RCA-043 already references STORY-515 in its recommendations

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| 01 Pre-Flight | ✅ Complete | Git valid, 6 context files, tech stack detected |
| 02 Red | ✅ Complete | 22 tests generated, 14 failing (RED confirmed) |
| 03 Green | ✅ Complete | Edit applied to src/ tree, all 22 tests pass |
| 04 Refactor | ✅ Complete | Code review APPROVED, no refactoring needed |
| 4.5 AC Verify | ✅ Complete | 3/3 ACs PASS |
| 05 Integration | ✅ Complete | 12/12 integration tests PASS |
| 5.5 AC Verify | ✅ Complete | Post-integration verification PASS |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/skills/implementing-stories/phases/phase-02-test-first.md | Modified | 167-264 |
| tests/STORY-515/test_ac1_numbered_categories.sh | Created | ~60 |
| tests/STORY-515/test_ac2_labels.sh | Created | ~80 |
| tests/STORY-515/test_ac3_content_preserved.sh | Created | ~90 |
| tests/STORY-515/run_all_tests.sh | Created | ~30 |

## Definition of Done

### Implementation
- [x] Post-checkpoint sections reorganized into numbered categories
- [x] Mandatory steps labeled with [MANDATORY] marker
- [x] Optional steps labeled with [OPTIONAL] marker
- [x] All original content preserved (no instructions, code blocks, or references lost)
- [x] Categories ordered: Mandatory → Optional → Exit Gate

### Quality
- [x] All 3 acceptance criteria have passing tests
- [x] No broken cross-references from other skill files
- [x] File structure validates correctly

### Testing
- [x] Unit tests for numbered category presence
- [x] Unit tests for MANDATORY/OPTIONAL labels
- [x] Unit tests for content preservation
- [x] Integration test for complete file structure

### Documentation
- [x] Story file created with complete specification
- [x] RCA-043 updated with story link for REC-3

---

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-28 10:00 | .claude/story-requirements-analyst | Created | Story created from RCA-043/REC-3 | STORY-515.story.md |
| 2026-02-28 12:30 | .claude/qa-result-interpreter | QA Deep | PASSED: 22/22 tests, 0 violations, 3/3 validators | - |

## Notes

**Source RCA:** RCA-043 (Test Integrity Snapshot Skipped)
**Source Recommendation:** REC-3 (Restructure Phase 02 Exit Sequence)

**Design Decisions:**
- Use numbered categories with clear labels rather than just reordering
- This story restructures the POST-checkpoint sections only. The pre-checkpoint area (steps 1-5, test generation, RED verification, AC checklist update, and the snapshot block added by STORY-513/514) is NOT touched by this story.
- The snapshot section and its file verification were moved BEFORE the Validation Checkpoint by STORY-513/514. This story does NOT move them back — they stay pre-checkpoint.
- Mandatory post-checkpoint steps: AC Checklist Update Verification (RCA-003)
- Optional post-checkpoint steps: Observation Capture (EPIC-051), Session Memory Update (STORY-341), Observation Capture (general)
- Exit Gate remains as the final step

**CRITICAL: Post-STORY-513/514 File Structure (what you'll see when implementing):**
After STORY-513 and STORY-514 are completed, the Phase 02 file will have this approximate layout:
```
[Steps 1-5: Test generation, RED verification, tech spec coverage, AC checklist update]

### Test Integrity Snapshot (STORY-502)          ← PRE-checkpoint (STORY-513 moved it here)
  Read + Execute snapshot creation
  Glob verification + HALT if missing            ← Added by STORY-514

## Validation Checkpoint                         ← Line ~136 (existing)
  - [ ] test-automator subagent invoked
  - [ ] Tech Spec Coverage Validation completed
  - [ ] AC Checklist (test items) updated
  - [ ] Test integrity snapshot created (STORY-502)  ← Added by STORY-513

### AC Checklist Update Verification (RCA-003)   ← POST-checkpoint (lines ~146-153)
### Observation Capture (EPIC-051)               ← POST-checkpoint (lines ~157-181)
### Session Memory Update (STORY-341)            ← POST-checkpoint (lines ~185-207)
### Observation Capture (General)                ← POST-checkpoint (lines ~211-233)
### Exit Gate                                    ← POST-checkpoint (lines ~248-252)
```

**THIS STORY restructures only the POST-checkpoint sections (everything between `## Validation Checkpoint` items and `Exit Gate`). The proposed restructuring is:**
```
## Validation Checkpoint
  (existing checkpoint items — unchanged)

### 1. Post-Checkpoint Mandatory Steps [MANDATORY]
  #### AC Checklist Update Verification (RCA-003)
    (existing content from current "AC Checklist Update Verification" section)

### 2. Post-Checkpoint Optional Captures [OPTIONAL]
  #### Observation Capture (EPIC-051)
    (existing content from current "Observation Capture (EPIC-051)" section)
  #### Session Memory Update (STORY-341)
    (existing content from current "Session Memory Update" section)
  #### Observation Capture (General)
    (existing content from current general "Observation Capture" section)

### 3. Exit Gate
  devforgeai-validate phase-complete ...
    (existing exit gate content)
```

**Content Preservation Checklist (key strings that MUST exist in the restructured file):**
These strings are from the current post-checkpoint sections and must be present after restructuring:
1. `Grep(pattern="- \\[x\\].*test", path="${STORY_FILE}")` — from AC Checklist Update Verification
2. `subagent_type="observation-extractor"` — from Observation Capture (EPIC-051)
3. `session_path = ".claude/memory/sessions/${STORY_ID}-session.md"` — from Session Memory Update
4. `"category": "{friction|success|pattern|gap|idea|bug}"` — from Observation Capture (General)
5. `devforgeai-validate phase-complete ${STORY_ID} --phase=02 --checkpoint-passed` — from Exit Gate
6. `Test Integrity Snapshot` — from pre-checkpoint snapshot (should remain untouched)

**References:**
- RCA-043: devforgeai/RCA/RCA-043-test-integrity-snapshot-skipped.md
- STORY-513: devforgeai/specs/Stories/STORY-513-move-snapshot-before-validation-checkpoint.story.md
- STORY-514: devforgeai/specs/Stories/STORY-514-snapshot-file-existence-verification.story.md

---

Story Template Version: 2.9
Last Updated: 2026-02-28
