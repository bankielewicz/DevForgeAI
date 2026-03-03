#!/bin/bash

###############################################################################
# Test: AC#5 - Update RCA Status Field
#
# Acceptance Criteria:
#   Given all recommendations have been converted to stories
#   When updating the RCA document
#   Then the status field in YAML frontmatter is updated to "IN_PROGRESS"
#        if all recommendations have stories
#
# Test Approach:
#   1. ARRANGE: Create test RCA with status: OPEN and complete story map
#   2. ACT: Execute RCA linking with all recommendations mapped
#   3. ASSERT: Verify YAML status field changed from OPEN to IN_PROGRESS
#
# IMPORTANT: This test is EXPECTED TO FAIL initially (TDD Red phase)
#            No implementation exists yet
###############################################################################

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test configuration
TEST_NAME="AC#5: Update RCA Status Field"
FIXTURE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/fixtures" && pwd)"
SAMPLE_RCA="${FIXTURE_DIR}/sample-rca.md"
TEST_DIR="/tmp/test-rca-ac5-$$"

# Ensure fixture exists
if [[ ! -f "$SAMPLE_RCA" ]]; then
    echo -e "${RED}FAIL${NC}: Fixture not found: $SAMPLE_RCA"
    exit 1
fi

# ============================================================================
# ARRANGE: Setup test environment with complete story map
# ============================================================================
arrange_test() {
    mkdir -p "$TEST_DIR"
    cp "$SAMPLE_RCA" "$TEST_DIR/test-rca-complete.md"
    cp "$SAMPLE_RCA" "$TEST_DIR/test-rca-partial.md"

    echo "Test Environment Setup:"
    echo "  Complete Map: $TEST_DIR/test-rca-complete.md"
    echo "  Partial Map: $TEST_DIR/test-rca-partial.md"
    echo ""
    echo "Initial Status in both files:"
    grep "^status:" "$TEST_DIR/test-rca-complete.md" || echo "  (status field not found)"
    echo ""
    echo "Test Scenario A (Complete): All recommendations have stories"
    echo "  REC-1 → STORY-155"
    echo "  REC-2 → STORY-156"
    echo "  REC-3 → STORY-157"
    echo "  Expected: status should change to IN_PROGRESS"
    echo ""
    echo "Test Scenario B (Partial): Some recommendations lack stories"
    echo "  REC-1 → STORY-155"
    echo "  REC-2 → STORY-156"
    echo "  REC-3 → (no story)"
    echo "  Expected: status should remain OPEN"
}

# ============================================================================
# ACT: Execute RCA linking - Complete scenario
# ============================================================================
execute_linking_complete() {
    local rca_file="$TEST_DIR/test-rca-complete.md"

    echo ""
    echo "TEST SCENARIO A: Complete Story Map"
    echo "Executing RCA linking with COMPLETE story map..."
    echo "  REC-1 → STORY-155 (SUCCESS)"
    echo "  REC-2 → STORY-156 (SUCCESS)"
    echo "  REC-3 → STORY-157 (SUCCESS)"

    # Attempt to call the linking command
    if command -v rca-link-stories &> /dev/null; then
        rca-link-stories "$rca_file" --stories REC-1:STORY-155 REC-2:STORY-156 REC-3:STORY-157
    else
        echo "INFO: rca-link-stories command not found (expected - no implementation yet)"
    fi

    return 0
}

# ============================================================================
# ACT: Execute RCA linking - Partial scenario
# ============================================================================
execute_linking_partial() {
    local rca_file="$TEST_DIR/test-rca-partial.md"

    echo ""
    echo "TEST SCENARIO B: Partial Story Map"
    echo "Executing RCA linking with PARTIAL story map..."
    echo "  REC-1 → STORY-155 (SUCCESS)"
    echo "  REC-2 → STORY-156 (SUCCESS)"
    echo "  REC-3 → (FAILURE - no story)"

    # Attempt to call the linking command with only 2 stories
    if command -v rca-link-stories &> /dev/null; then
        rca-link-stories "$rca_file" --stories REC-1:STORY-155 REC-2:STORY-156
    else
        echo "INFO: rca-link-stories command not found (expected - no implementation yet)"
    fi

    return 0
}

# ============================================================================
# ASSERT: Verify status field updates correctly
# ============================================================================
assert_status_update() {
    local complete_file="$TEST_DIR/test-rca-complete.md"
    local partial_file="$TEST_DIR/test-rca-partial.md"
    local test_passed=true

    echo ""
    echo "Assertions:"

    # ASSERTION 1: Complete scenario - status should be IN_PROGRESS
    local complete_status=$(grep "^status:" "$complete_file" | cut -d: -f2 | xargs)
    if [[ "$complete_status" == "IN_PROGRESS" ]]; then
        echo "  ✓ PASS: Status updated to IN_PROGRESS in complete scenario"
    else
        echo "  ✗ FAIL: Status is '$complete_status', expected 'IN_PROGRESS' (complete scenario)"
        test_passed=false
    fi

    # ASSERTION 2: Partial scenario - status should remain OPEN
    local partial_status=$(grep "^status:" "$partial_file" | cut -d: -f2 | xargs)
    if [[ "$partial_status" == "OPEN" ]]; then
        echo "  ✓ PASS: Status remains OPEN in partial scenario"
    else
        echo "  ✗ FAIL: Status is '$partial_status', expected 'OPEN' (partial scenario)"
        test_passed=false
    fi

    # ASSERTION 3: Verify status is in YAML frontmatter (first 10 lines)
    if head -10 "$complete_file" | grep -q "^status: IN_PROGRESS"; then
        echo "  ✓ PASS: Status field is in YAML frontmatter"
    else
        echo "  ✗ FAIL: Status field not found in YAML frontmatter"
        test_passed=false
    fi

    # ASSERTION 4: Verify YAML format is preserved (key: value)
    if grep -qE "^status: (OPEN|IN_PROGRESS|CLOSED)$" "$complete_file"; then
        echo "  ✓ PASS: YAML status format is correct"
    else
        echo "  ✗ FAIL: YAML status format is incorrect"
        test_passed=false
    fi

    # ASSERTION 5: Verify no extra whitespace in status value
    local complete_status_raw=$(grep "^status:" "$complete_file")
    if [[ "$complete_status_raw" == "status: IN_PROGRESS" ]]; then
        echo "  ✓ PASS: Status value has correct formatting (no extra whitespace)"
    else
        echo "  ✗ FAIL: Status value formatting is incorrect: '$complete_status_raw'"
        test_passed=false
    fi

    # ASSERTION 6: Partial scenario - verify status line exists and equals OPEN
    if grep -q "^status: OPEN$" "$partial_file"; then
        echo "  ✓ PASS: Partial scenario status line is exactly 'status: OPEN'"
    else
        echo "  ✗ FAIL: Partial scenario status line format incorrect"
        test_passed=false
    fi

    # ASSERTION 7: Verify YAML frontmatter structure still valid (starts and ends with ---)
    if head -1 "$complete_file" | grep -q "^---"; then
        echo "  ✓ PASS: YAML frontmatter opening preserved"
    else
        echo "  ✗ FAIL: YAML frontmatter opening missing"
        test_passed=false
    fi

    return $([ "$test_passed" = true ] && echo 0 || echo 1)
}

# ============================================================================
# CLEANUP: Remove temporary test files
# ============================================================================
cleanup() {
    rm -rf "$TEST_DIR"
}

# ============================================================================
# MAIN: Run test
# ============================================================================
main() {
    echo ""
    echo "============================================================================"
    echo "TEST: $TEST_NAME"
    echo "============================================================================"
    echo ""

    # Arrange phase
    arrange_test
    echo ""

    # Act phase
    execute_linking_complete || true  # Don't fail on missing command
    execute_linking_partial || true
    echo ""

    # Assert phase
    if assert_status_update; then
        echo ""
        echo -e "${GREEN}RESULT: PASS${NC}"
        TEST_RESULT=0
    else
        echo ""
        echo -e "${RED}RESULT: FAIL${NC}"
        TEST_RESULT=1
    fi

    # Debug: Show status fields
    echo ""
    echo "Actual status fields (for debugging):"
    echo "----------------------------------------"
    echo "Complete scenario (should be IN_PROGRESS):"
    grep "^status:" "$TEST_DIR/test-rca-complete.md" || echo "  (Not found)"
    echo ""
    echo "Partial scenario (should be OPEN):"
    grep "^status:" "$TEST_DIR/test-rca-partial.md" || echo "  (Not found)"
    echo ""
    echo "YAML frontmatter comparison:"
    echo "Complete file first 5 lines:"
    head -5 "$TEST_DIR/test-rca-complete.md"
    echo ""
    echo "Partial file first 5 lines:"
    head -5 "$TEST_DIR/test-rca-partial.md"
    echo "----------------------------------------"
    echo ""

    # Cleanup
    cleanup

    return $TEST_RESULT
}

# Run main function and exit with result
main
exit $?
