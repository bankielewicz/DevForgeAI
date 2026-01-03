# STORY-166: RCA-012 AC Header Documentation Clarification - Test Generation Report

## Summary

Generated comprehensive failing test suite for STORY-166 documentation validation.

**Test Status: ALL TESTS FAILING (RED STATE - TDD)**

All tests intentionally fail because the documentation content does not yet exist in CLAUDE.md. This is the expected RED phase of Test-Driven Development.

---

## Test Suite Overview

| Test File | AC | Purpose | Status |
|-----------|-----|---------|--------|
| `test-ac1-claude-md-header-clarification.sh` | AC#1 | Validate CLAUDE.md contains AC header clarification section | FAILING |
| `test-ac2-comparison-table.sh` | AC#2 | Validate comparison table for AC headers, checklist, and DoD | FAILING |
| `test-ac3-historical-story-guidance.sh` | AC#3 | Validate guidance for older story format (### 1. [ ]) | FAILING |

**Total Tests: 3**
**Total Test Cases: 16**

---

## Detailed Test Breakdown

### AC#1: CLAUDE.md Updated with AC Header Clarification

**File:** `/mnt/c/Projects/DevForgeAI2/tests/STORY-166/test-ac1-claude-md-header-clarification.sh`

**Test Cases:**

1. **CLAUDE.md file exists**
   - Status: PASSING
   - Purpose: Verify file is readable

2. **Section explaining AC headers vs tracking exists**
   - Status: FAILING
   - Reason: Section "Acceptance Criteria vs. Tracking Mechanisms" not found
   - What it checks: Grep for patterns like "acceptance criteria", "tracking", "definitions"

3. **AC headers documented as definitions, not trackers**
   - Status: FAILING
   - Reason: Documentation about AC header definition/immutability not found
   - What it checks: Patterns like "definitions", "not trackers", "immutable"

4. **Documentation about why AC headers never marked complete**
   - Status: FAILING
   - Reason: Explanation missing
   - What it checks: Patterns like "never marked complete", "never meant to be checked"

5. **Reference to Definition of Done (DoD) for completion status**
   - Status: FAILING
   - Reason: DoD guidance not found
   - What it checks: Patterns like "definition of done", "dod section", "actual completion status"

---

### AC#2: Table Comparing Elements

**File:** `/mnt/c/Projects/DevForgeAI2/tests/STORY-166/test-ac2-comparison-table.sh`

**Test Cases:**

1. **CLAUDE.md file exists**
   - Status: PASSING
   - Purpose: Verify file is readable

2. **Comparison table header exists**
   - Status: FAILING
   - Expected: `| Element | Purpose | Checkbox Behavior |`
   - What it checks: Exact table header pattern

3. **AC Headers row in table**
   - Status: FAILING
   - Expected: AC Headers | Define what to test | Never marked complete
   - What it checks: Table row with correct content for AC Headers

4. **AC Checklist row in table**
   - Status: FAILING
   - Expected: AC Checklist | Track progress | Marked during TDD
   - What it checks: Table row with correct content for AC Checklist

5. **Definition of Done row in table**
   - Status: FAILING
   - Expected: Definition of Done | Official record | Marked in Phase 4.5-5 Bridge
   - What it checks: Table row with Phase 4.5-5 Bridge reference

6. **Table uses Markdown pipe format**
   - Status: FAILING
   - Purpose: Verify table structure is valid
   - What it checks: Multiple lines containing pipe characters

---

### AC#3: Historical Story Guidance

**File:** `/mnt/c/Projects/DevForgeAI2/tests/STORY-166/test-ac3-historical-story-guidance.sh`

**Test Cases:**

1. **CLAUDE.md file exists**
   - Status: PASSING
   - Purpose: Verify file is readable

2. **Historical guidance section exists**
   - Status: FAILING
   - Reason: Section about older stories not found
   - What it checks: Patterns like "older stories", "template v2", "vestigial"

3. **Reference to ### 1. [ ] checkbox format**
   - Status: FAILING
   - Reason: Old format not documented
   - What it checks: Reference to old checkbox syntax from template v2.0

4. **Explanation that old checkboxes should never be checked**
   - Status: FAILING
   - Reason: Explanation missing
   - What it checks: Patterns like "never meant to be checked", "never check old"

5. **Guidance to look at DoD section for old stories**
   - Status: FAILING
   - Reason: Cross-reference missing
   - What it checks: Guidance pointing to Definition of Done section

---

## Test Framework Details

**Test Type:** Bash shell scripts
**Test Framework:** GNU grep with pattern matching
**Test Location:** `/mnt/c/Projects/DevForgeAI2/tests/STORY-166/`

### Test Design Patterns

**Pattern Matching Strategy:**

Tests use case-insensitive grep patterns (`grep -iq`) to detect documentation content:

```bash
# Example: Test AC header definitions
if ! grep -iq "ac.*headers.*definitions\|definitions.*not.*trackers" "$CLAUDE_MD_PATH"; then
    echo "FAIL: Content not found"
    exit 1
fi
```

**Why Grep Pattern Matching:**

1. **Non-prescriptive:** Tests don't dictate exact wording, just presence of key concepts
2. **Flexible:** Works with different documentation formats
3. **Intent-based:** Validates intent (AC headers are definitions) not exact text
4. **Maintainable:** Easy to adjust patterns as documentation evolves

---

## Running the Tests

### Run All Tests
```bash
bash tests/STORY-166/test-ac1-claude-md-header-clarification.sh
bash tests/STORY-166/test-ac2-comparison-table.sh
bash tests/STORY-166/test-ac3-historical-story-guidance.sh
```

### Run with Exit Code Check
```bash
bash tests/STORY-166/test-ac1-claude-md-header-clarification.sh && echo "PASS" || echo "FAIL"
```

### Run Test Suite
```bash
# Run all tests and show summary
for test in tests/STORY-166/test-*.sh; do
    bash "$test" && echo "✓ ${test##*/}" || echo "✗ ${test##*/}"
done
```

---

## Expected Failures (RED State)

### Test Execution Output

```
Running: AC#1: CLAUDE.md Updated with AC Header Clarification
===========================================

PASS: CLAUDE.md file exists
FAIL: CLAUDE.md does not contain section explaining AC headers vs tracking
Expected section title containing: 'Acceptance Criteria' and 'Tracking Mechanisms'
```

All 3 tests fail with exit code 1 (failure), which is **expected and correct** for TDD Red phase.

---

## Coverage Summary

| Acceptance Criteria | Test File | Coverage |
|-------------------|-----------|----------|
| AC#1: Header Clarification | test-ac1-*.sh | 5 test cases covering all requirements |
| AC#2: Comparison Table | test-ac2-*.sh | 6 test cases covering table structure and content |
| AC#3: Historical Guidance | test-ac3-*.sh | 5 test cases covering old format guidance |

**Total Test Coverage:** 16 test cases across 3 acceptance criteria

---

## Next Steps (Green Phase - Implementation)

To make tests pass, implement the following in CLAUDE.md:

### 1. Add AC Header Clarification Section

Add new subsection under "Story Progress Tracking" with:
- Explanation that AC headers are **definitions**, not progress trackers
- Clear statement that AC headers should **never be marked complete**
- Reference to Definition of Done (DoD) as the actual completion tracker

### 2. Add Comparison Table

Insert table with 3 rows:

```markdown
| Element | Purpose | Checkbox Behavior |
|---------|---------|-------------------|
| AC Headers | Define what to test (immutable) | Never marked complete |
| AC Verification Checklist | Track granular progress | Marked during TDD phases |
| Definition of Done | Official completion record | Marked in Phase 4.5-5 Bridge |
```

### 3. Add Historical Story Guidance

Document that:
- Older stories (template v2.0) may have `### 1. [ ]` checkbox format
- These checkboxes are "vestigial" (leftover from old template)
- They should **never be checked**
- Look at DoD section for actual completion status in old stories

---

## Test Quality Characteristics

### Advantages of This Test Approach

1. **Documentation-First:** Tests verify documentation quality, not code
2. **Intent-Based:** Tests focus on concept presence, not exact wording
3. **Maintainable:** Grep patterns are simple and easy to modify
4. **Fast Execution:** Simple pattern matching, no external dependencies
5. **Clear Feedback:** Test output clearly shows what's missing

### Test Independence

Each test runs independently with:
- No external dependencies
- No shared state
- No execution order requirements
- Idempotent test execution

### Anti-Patterns Avoided

- ❌ NOT checking for exact line numbers (too brittle)
- ❌ NOT checking exact formatting (too rigid)
- ❌ NOT using HTML parsing (unnecessary complexity)
- ✅ Using concept-based pattern matching (flexible and maintainable)

---

## Files Generated

```
/mnt/c/Projects/DevForgeAI2/
├── tests/
│   └── STORY-166/
│       ├── test-ac1-claude-md-header-clarification.sh  (3198 bytes)
│       ├── test-ac2-comparison-table.sh                (3152 bytes)
│       └── test-ac3-historical-story-guidance.sh       (2905 bytes)
└── STORY-166-TEST-GENERATION-REPORT.md               (This file)
```

---

## Acceptance Criteria Verification

### AC#1: Header Clarification Tests
- [x] Test verifies CLAUDE.md section exists
- [x] Test verifies AC headers documented as definitions
- [x] Test verifies explanation of "never marked complete"
- [x] Test verifies DoD reference

### AC#2: Comparison Table Tests
- [x] Test verifies table header format
- [x] Test verifies AC Headers row exists
- [x] Test verifies AC Checklist row exists
- [x] Test verifies Definition of Done row exists
- [x] Test verifies Markdown pipe table format

### AC#3: Historical Guidance Tests
- [x] Test verifies guidance section exists
- [x] Test verifies ### 1. [ ] format reference
- [x] Test verifies "never check" explanation
- [x] Test verifies DoD guidance for old stories

---

## Test Execution Protocol

**TDD Red Phase (Current):**
- [x] Tests created and failing ✓
- [x] Failure messages clear and actionable ✓
- [x] All 3 tests execute successfully (all exit with failure code 1) ✓

**Next: TDD Green Phase (Implementation):**
- Implement CLAUDE.md content
- Tests should pass when documentation is added
- All 3 tests should exit with code 0 (success)

---

## References

- **Story:** `devforgeai/specs/Stories/STORY-166-rca-012-ac-header-documentation.story.md`
- **Tech Stack:** `devforgeai/specs/context/tech-stack.md` (Bash testing, grep patterns)
- **Test Location:** `tests/STORY-166/` (per source-tree.md)
- **RCA Source:** `devforgeai/RCA/RCA-012/ANALYSIS.md` (REC-2)

---

## Test Metadata

- **Story ID:** STORY-166
- **Test Count:** 3 test files, 16 test cases
- **Test Type:** Documentation validation (bash/grep)
- **Status:** All failing (RED state - expected)
- **Generated:** 2025-01-03
- **Framework:** TDD (Test-Driven Development)
- **Phase:** Phase 02 - Test-First (Red)

