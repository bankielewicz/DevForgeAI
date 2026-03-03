# STORY-163 Test Suite

## Overview

This test suite validates the RCA cross-reference updates for STORY-163: "RCA-011 Cross-Reference Update (RCA-009)". The tests verify that RCA-009 and RCA-011 documents are properly cross-referenced and that the recurrence pattern is documented.

## Test Files

### test_ac1_rca009_status_updated.sh
**Validates:** Acceptance Criteria 1 - RCA-009 Status Updated

**Given:** `devforgeai/RCA/RCA-009-skill-execution-incomplete-workflow.md`
**When:** The status line (line 7) is reviewed
**Then:** It should show the RCA-011 reference with date, story, and root cause

**Test Logic:**
1. Checks that RCA-009 file exists
2. Extracts line 7 (status line)
3. Verifies it contains all required elements:
   - "Recurred - See RCA-011"
   - "2025-11-19"
   - "STORY-044"
   - "same root cause"

### test_ac2_rca011_cross_reference.sh
**Validates:** Acceptance Criteria 2 - RCA-011 Cross-Reference

**Given:** `devforgeai/RCA/RCA-011-mandatory-tdd-phase-skipping.md`
**When:** The "Related RCAs" section is reviewed
**Then:** It should include reference to RCA-009 with relationship explanation

**Test Logic:**
1. Checks that RCA-011 file exists
2. Extracts the Related RCAs section (approximately 8 lines)
3. Verifies it contains all required elements:
   - "RCA-009"
   - "same root cause"
   - "Incomplete Skill Workflow"

### test_ac3_recurrence_pattern_documented.sh
**Validates:** Acceptance Criteria 3 - Recurrence Pattern Documented

**Given:** Both RCA documents (RCA-009 and RCA-011)
**When:** The root cause sections are compared
**Then:** Both should explicitly note the recurring pattern requiring systemic fix

**Test Logic:**
1. Verifies both RCA files exist
2. Checks RCA-009 contains:
   - "recurring" or "recurrence" or "pattern"
3. Checks RCA-011 contains:
   - "systemic" (mentioned in conclusion)
   - "recurring" or "recurrence" or "same root cause"
4. Verifies both documents explain the root cause:
   - Visual markers ignored
   - Lack of enforcement

## Running the Tests

### Run all tests:
```bash
bash tests/STORY-163/test_ac1_rca009_status_updated.sh
bash tests/STORY-163/test_ac2_rca011_cross_reference.sh
bash tests/STORY-163/test_ac3_recurrence_pattern_documented.sh
```

### Run with results summary:
```bash
cd /mnt/c/Projects/DevForgeAI2

TEST_RESULTS=""
for test in tests/STORY-163/test_*.sh; do
    if bash "$test" > /dev/null 2>&1; then
        echo "✓ $(basename $test)"
    else
        echo "✗ $(basename $test)"
    fi
done
```

## Test Results

| Test | Status | Notes |
|------|--------|-------|
| test_ac1_rca009_status_updated.sh | PASSED | RCA-009 status line correctly updated |
| test_ac2_rca011_cross_reference.sh | PASSED | RCA-011 Related RCAs section includes RCA-009 reference |
| test_ac3_recurrence_pattern_documented.sh | PASSED | Both documents document recurrence pattern |

## Coverage

- **AC-1:** RCA-009 Status Updated - 100%
- **AC-2:** RCA-011 Cross-Reference - 100%
- **AC-3:** Recurrence Pattern Documented - 100%

## TDD Red Phase Compliance

These tests follow Test-Driven Development (TDD) Red phase principles:

1. **Tests are declarative** - Each test clearly states what it validates
2. **Tests are independent** - No shared state between tests
3. **Tests are repeatable** - Can run in any order
4. **Tests verify acceptance criteria** - Direct mapping to AC-1, AC-2, AC-3
5. **Tests use shell scripts** - Appropriate for documentation file validation

## References

- Story: `devforgeai/specs/Stories/STORY-163-rca-011-cross-reference-update.story.md`
- RCA-009: `devforgeai/RCA/RCA-009-skill-execution-incomplete-workflow.md`
- RCA-011: `devforgeai/RCA/RCA-011-mandatory-tdd-phase-skipping.md`
