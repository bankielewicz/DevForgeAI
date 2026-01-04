#!/bin/bash

# STORY-169: RCA-013 Phase Validation Checkpoint
# AC#3: Phase 4 (Integration Testing/Phase 05) Validation Checkpoint
# Status: TDD Red (should FAIL - checkpoint not yet enhanced with explicit validation)
#
# This test verifies that Phase 05 (Integration Testing) contains explicit validation
# checkpoint logic that verifies:
# - integration-tester invoked
# - HALT if any check fails

set -e

# Load test library
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/test-lib.sh"

echo "========================================================================"
echo "STORY-169 AC#3: Phase 05 (Integration Testing) Validation Checkpoint"
echo "========================================================================"
echo ""

# Test 1: Phase 05 file exists
echo "Test 1: Phase 05 integration file exists"
assert_file_exists "$PHASE_05_FILE" "phase-05-integration.md should exist"

# Test 2: Validation Checkpoint section exists
echo ""
echo "Test 2: Validation Checkpoint section exists in Phase 05"
PHASE_05_CONTENT=$(cat "$PHASE_05_FILE" 2>/dev/null || echo "")
# Accept either "## Validation Checkpoint" or "## Phase 05 Validation Checkpoint"
if echo "$PHASE_05_CONTENT" | grep -qE "## (Phase 05 )?Validation Checkpoint"; then
    echo -e "${GREEN}PASS${NC} Phase 05 should have Validation Checkpoint section"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Phase 05 should have Validation Checkpoint section"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 3: Checkpoint verifies integration-tester invoked
echo ""
echo "Test 3: Checkpoint verifies integration-tester invocation"
assert_pattern_exists "$PHASE_05_FILE" \
    "integration-tester" \
    "Checkpoint should verify integration-tester invoked"

# Test 4: Checkpoint has explicit HALT on failure logic
echo ""
echo "Test 4: Checkpoint has explicit HALT logic for missing subagents"
if grep -qE "(HALT.*workflow|IF.*UNCHECKED.*HALT|HALT.*if.*check.*fail)" "$PHASE_05_FILE"; then
    echo -e "${GREEN}PASS${NC} Phase 05 has HALT logic for checkpoint failures"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Phase 05 missing explicit HALT logic for checkpoint failures"
    echo "  Expected: HALT instruction when validation checkpoint fails"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 5: NEW - Verify explicit subagent invocation verification template exists
# Per RCA-013 REC-3: Checkpoint should explicitly check for Task() calls
echo ""
echo "Test 5: Phase 05 has explicit subagent invocation verification template"
if grep -qE "Phase.*05.*Validation Checkpoint|### Phase 05 Validation Checkpoint" "$PHASE_05_FILE" && \
   grep -qE "verify.*Task\(\).*call|check.*for.*Task\(\)|invoked.*check" "$PHASE_05_FILE"; then
    echo -e "${GREEN}PASS${NC} Phase 05 has explicit subagent invocation verification"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAIL${NC} Phase 05 missing explicit subagent invocation verification template"
    echo "  Expected: Verification that checks for Task() call in conversation"
    echo "  Per Technical Spec: 'verify: integration-tester invoked (check for Task() call)'"
    TESTS_RUN=$((TESTS_RUN + 1))
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Print summary
print_test_summary "AC#3: Phase 05 Validation Checkpoint Tests"
exit_with_result
