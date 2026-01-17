# TEST-SPECIFICATION: STORY-268

## Story: Integrate AC Verification Checklist Real-Time Updates into TDD Workflow

**Test Type:** Structural Validation (Markdown Specifications)
**Implementation Type:** Slash Command/Skill Reference Files (.md)
**Output Type:** Test Specification Document (not executable unit tests)

---

## Test Suite Overview

This test suite validates that the 6 TDD phase reference files are correctly integrated with the AC Verification Checklist real-time update workflow.

### Files Under Test

| Phase | File | Expected Step | Status |
|-------|------|---------------|--------|
| Phase 02 (Red) | `tdd-red-phase.md` | Step 5 | EXISTS |
| Phase 03 (Green) | `tdd-green-phase.md` | Step 4 | EXISTS |
| Phase 04 (Refactor) | `tdd-refactor-phase.md` | Step 6 | NEEDS IMPLEMENTATION |
| Phase 05 (Integration) | `integration-testing.md` | Step 3/4 | EXISTS |
| Phase 06 (Deferral) | `phase-06-deferral-challenge.md` | Step 7 | NEEDS IMPLEMENTATION |
| Phase 08 (Git) | `git-workflow-conventions.md` | Section | EXISTS (review needed) |

---

## Acceptance Criteria Test Mapping

### AC#1: tdd-red-phase.md Integration (Phase 02)
**Test File:** `test-ac1-red-phase-integration.sh`

**Validates:**
- [x] Step 5 header exists with "AC Checklist" mention
- [x] Reference to `ac-checklist-update-workflow.md`
- [x] `Read()` call to workflow file
- [x] Graceful skip text "DoD-only tracking"
- [x] Progress display "AC Progress" pattern
- [x] Phase marker reference (Phase: 1)
- [x] Grep pattern for AC items

**Expected Result:** PASS (already implemented)

---

### AC#2: tdd-green-phase.md Integration (Phase 03)
**Test File:** `test-ac2-green-phase-integration.sh`

**Validates:**
- [x] Step 4 header exists with "AC Checklist" mention
- [x] Reference to `ac-checklist-update-workflow.md`
- [x] `Read()` call to workflow file
- [x] Graceful skip text "DoD-only tracking"
- [x] Progress display "AC Progress" pattern
- [x] Phase marker reference (Phase: 2)
- [x] Grep pattern for AC items
- [x] Implementation metrics mentioned

**Expected Result:** PASS (already implemented)

---

### AC#3: tdd-refactor-phase.md Integration (Phase 04)
**Test File:** `test-ac3-refactor-phase-integration.sh`

**Validates:**
- [ ] Step 6 header exists with "AC Checklist" mention
- [ ] Reference to `ac-checklist-update-workflow.md`
- [ ] `Read()` call to workflow file
- [ ] Graceful skip text "DoD-only tracking"
- [ ] Progress display "AC Progress" pattern
- [ ] Phase marker reference (Phase: 3)
- [ ] Grep pattern for AC items
- [ ] Quality items mentioned (complexity, duplication, pattern compliance)

**Expected Result:** FAIL (Step 6 needs to be added after Step 5)

**Implementation Note:** The checkpoint at line 417 references Step 6 but the actual step content needs to be added.

---

### AC#4: integration-testing.md Integration (Phase 05)
**Test File:** `test-ac4-integration-testing-integration.sh`

**Validates:**
- [x] Step 3/4 header exists with "AC Checklist" mention
- [x] Reference to `ac-checklist-update-workflow.md`
- [x] `Read()` call to workflow file
- [x] Graceful skip text "DoD-only tracking"
- [x] Progress display "AC Progress" pattern
- [x] Phase marker reference (Phase: 4)
- [x] Grep pattern for AC items
- [x] Integration/coverage items mentioned

**Expected Result:** PASS (already implemented)

---

### AC#5: phase-06-deferral-challenge.md Integration (Phase 06)
**Test File:** `test-ac5-deferral-challenge-integration.sh`

**Validates:**
- [ ] Step 7 header exists with "AC Checklist" mention
- [ ] Reference to `ac-checklist-update-workflow.md`
- [ ] `Read()` call to workflow file
- [ ] Graceful skip text "DoD-only tracking"
- [ ] Progress display "AC Progress" pattern
- [ ] Phase marker reference (Phase: 4.5)
- [ ] Grep pattern for AC items
- [ ] Deferral validation items mentioned

**Expected Result:** FAIL (Step 7 needs to be added after Step 6.5)

**Implementation Note:** The checkpoint at line 1240 references Step 7 but the actual step content needs to be added.

---

### AC#6: git-workflow-conventions.md Integration (Phase 08)
**Test File:** `test-ac6-git-workflow-integration.sh`

**Validates:**
- [x] AC Checklist Updates section for Phase 08
- [x] Reference to `ac-checklist-update-workflow.md`
- [x] `Read()` call to workflow file
- [ ] Graceful skip text "DoD-only tracking"
- [x] Progress display "AC Progress" pattern
- [x] Phase marker reference (Phase: 5)
- [x] Grep pattern for AC items
- [x] Deployment readiness items mentioned
- [x] Final checklist summary (100%)

**Expected Result:** PARTIAL PASS (some elements exist, review needed)

---

### AC#7: Backward Compatibility
**Test File:** `test-ac7-backward-compatibility.sh`

**Validates across all 6 files:**
- [ ] "DoD-only tracking" graceful skip message
- [ ] AC Checklist absence detection
- [ ] Graceful continuation logic

**Also validates workflow document:**
- [x] Backward Compatibility section exists
- [x] Older format handling documented

**Expected Result:** FAIL for files without full implementation

---

### AC#8: Progress Display with Running Total
**Test File:** `test-ac8-progress-display.sh`

**Validates across all 6 files:**
- [ ] "AC Progress" display pattern
- [ ] Running total format (X/Y items)
- [ ] Percentage display
- [ ] Items checked indicator

**Also validates git-workflow-conventions.md:**
- [x] Phase-by-phase contribution summary
- [x] 100% completion indicator
- [x] Final AC Checklist completion message

**Expected Result:** PARTIAL PASS (varies by file)

---

## Test Execution

### Run All Tests
```bash
cd /mnt/c/Projects/DevForgeAI2/tests/results/STORY-268
chmod +x *.sh
./run-all-tests.sh
```

### Run Individual Test
```bash
./test-ac1-red-phase-integration.sh
./test-ac3-refactor-phase-integration.sh  # Expected to fail
./test-ac5-deferral-challenge-integration.sh  # Expected to fail
```

---

## Expected Test Results Before Implementation

| Test | Expected |
|------|----------|
| AC#1 (Red Phase) | PASS |
| AC#2 (Green Phase) | PASS |
| AC#3 (Refactor Phase) | FAIL |
| AC#4 (Integration) | PASS |
| AC#5 (Deferral) | FAIL |
| AC#6 (Git Workflow) | PARTIAL |
| AC#7 (Backward Compat) | FAIL |
| AC#8 (Progress Display) | PARTIAL |

---

## Implementation Requirements

### Files to Modify

1. **tdd-refactor-phase.md** (AC#3)
   - Add Step 6 section after Step 5 (Light QA)
   - Include: Read() call, Grep pattern, graceful skip, progress display
   - Reference Phase: 3 for AC items

2. **phase-06-deferral-challenge.md** (AC#5)
   - Add Step 7 section after Step 6.5
   - Include: Read() call, Grep pattern, graceful skip, progress display
   - Reference Phase: 4.5 for AC items

3. **git-workflow-conventions.md** (AC#6)
   - Review existing section (lines 228-272)
   - Ensure graceful skip text present
   - Verify progress display format

---

## Test Pattern Used

**Structural Testing for Markdown Specifications**

Tests validate:
1. Section headers exist (structural)
2. Required references present (dependency)
3. Required patterns match (contract)
4. Graceful degradation text (compatibility)

Tests do NOT validate:
- Narrative content wording
- Documentation commentary
- Implementation behavior (no runtime)

---

## Related Documents

- Story: `/mnt/c/Projects/DevForgeAI2/devforgeai/specs/Stories/STORY-268-ac-verification-checklist-real-time-updates.story.md`
- Workflow: `/mnt/c/Projects/DevForgeAI2/.claude/skills/devforgeai-development/references/ac-checklist-update-workflow.md`
- Test Directory: `/mnt/c/Projects/DevForgeAI2/tests/results/STORY-268/`

---

**Generated:** 2026-01-16
**Test Framework:** Bash shell scripts (pattern tests using grep)
**Total Tests:** 8 test files (56+ individual assertions)
