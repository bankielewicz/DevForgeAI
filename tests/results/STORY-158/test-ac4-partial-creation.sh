#!/bin/bash

###############################################################################
# Test: AC#4 - Handle Partial Story Creation
#
# Acceptance Criteria:
#   Given some recommendations had story creation failures
#   When updating the RCA document
#   Then only successfully created stories are linked; failed recommendations remain unmarked
#
# Test Approach:
#   1. ARRANGE: Create test RCA with 3 recommendations but only 2 stories created
#   2. ACT: Execute RCA linking with partial story map
#   3. ASSERT: Verify only REC-1 and REC-2 are linked; REC-3 remains unmarked
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
TEST_NAME="AC#4: Handle Partial Story Creation"
FIXTURE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/fixtures" && pwd)"
SAMPLE_RCA="${FIXTURE_DIR}/sample-rca.md"
TEST_DIR="/tmp/test-rca-ac4-$$"

# Ensure fixture exists
if [[ ! -f "$SAMPLE_RCA" ]]; then
    echo -e "${RED}FAIL${NC}: Fixture not found: $SAMPLE_RCA"
    exit 1
fi

# ============================================================================
# ARRANGE: Setup test environment with partial story map
# ============================================================================
arrange_test() {
    mkdir -p "$TEST_DIR"
    cp "$SAMPLE_RCA" "$TEST_DIR/test-rca.md"

    echo "Test Environment Setup:"
    echo "  Test Directory: $TEST_DIR"
    echo "  Test RCA File: $TEST_DIR/test-rca.md"
    echo ""
    echo "Story Creation Status (Partial):"
    echo "  REC-1: Story CREATED (STORY-155)"
    echo "  REC-2: Story CREATED (STORY-156)"
    echo "  REC-3: Story FAILED (no story ID)"
    echo ""
    echo "Expected Linking Result:"
    echo "  - REC-1 should be linked to STORY-155"
    echo "  - REC-2 should be linked to STORY-156"
    echo "  - REC-3 should remain unmarked (no story)"
}

# ============================================================================
# ACT: Execute RCA linking with partial story map
# ============================================================================
execute_linking() {
    local rca_file="$TEST_DIR/test-rca.md"

    echo ""
    echo "Executing RCA linking with PARTIAL story map..."
    echo "  REC-1 → STORY-155 (SUCCESS)"
    echo "  REC-2 → STORY-156 (SUCCESS)"
    echo "  REC-3 → (FAILURE - no story)"

    # Attempt to call the linking command with only successful stories
    if command -v rca-link-stories &> /dev/null; then
        rca-link-stories "$rca_file" --stories REC-1:STORY-155 REC-2:STORY-156
    else
        echo "INFO: rca-link-stories command not found (expected - no implementation yet)"
    fi

    return 0
}

# ============================================================================
# ASSERT: Verify only successful stories are linked
# ============================================================================
assert_partial_linking() {
    local rca_file="$TEST_DIR/test-rca.md"
    local test_passed=true

    echo ""
    echo "Assertions:"

    # ASSERTION 1: REC-1 should be linked to STORY-155
    if grep -q "REC-1.*STORY-155" "$rca_file"; then
        echo "  ✓ PASS: REC-1 is linked to STORY-155"
    else
        echo "  ✗ FAIL: REC-1 is not linked to STORY-155"
        test_passed=false
    fi

    # ASSERTION 2: REC-2 should be linked to STORY-156
    if grep -q "REC-2.*STORY-156" "$rca_file"; then
        echo "  ✓ PASS: REC-2 is linked to STORY-156"
    else
        echo "  ✗ FAIL: REC-2 is not linked to STORY-156"
        test_passed=false
    fi

    # ASSERTION 3: REC-3 should NOT have a story reference
    if ! grep -q "REC-3.*STORY" "$rca_file"; then
        echo "  ✓ PASS: REC-3 has no story reference (as expected)"
    else
        echo "  ✗ FAIL: REC-3 should not have a story reference"
        test_passed=false
    fi

    # ASSERTION 4: Verify exact pattern for REC-1
    if grep -E "REC-1.*(See )?STORY-155" "$rca_file" > /dev/null; then
        echo "  ✓ PASS: REC-1 reference format correct"
    else
        echo "  ✗ FAIL: REC-1 reference format incorrect"
        test_passed=false
    fi

    # ASSERTION 5: Verify exact pattern for REC-2
    if grep -E "REC-2.*(See )?STORY-156" "$rca_file" > /dev/null; then
        echo "  ✓ PASS: REC-2 reference format correct"
    else
        echo "  ✗ FAIL: REC-2 reference format incorrect"
        test_passed=false
    fi

    # ASSERTION 6: Verify exactly 2 story references exist (not 3)
    local story_count=$(grep -o "STORY-[0-9]\+" "$rca_file" | sort -u | wc -l)
    if [[ $story_count -eq 2 ]]; then
        echo "  ✓ PASS: Exactly 2 story references found (REC-3 not linked)"
    else
        echo "  ✗ FAIL: Expected 2 story references, found $story_count"
        test_passed=false
    fi

    # ASSERTION 7: Verify REC-3 description is unchanged
    if grep -q "Description of third recommendation" "$rca_file"; then
        echo "  ✓ PASS: REC-3 description unchanged"
    else
        echo "  ✗ FAIL: REC-3 description was modified"
        test_passed=false
    fi

    # ASSERTION 8: Verify checklist format for REC-1
    if grep -E "^- \[ \] REC-1.*STORY-155" "$rca_file" > /dev/null; then
        echo "  ✓ PASS: Checklist entry for REC-1 has correct format"
    else
        echo "  ✗ FAIL: Checklist entry for REC-1 format incorrect"
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
    execute_linking || true  # Don't fail on missing command
    echo ""

    # Assert phase
    if assert_partial_linking; then
        echo ""
        echo -e "${GREEN}RESULT: PASS${NC}"
        TEST_RESULT=0
    else
        echo ""
        echo -e "${RED}RESULT: FAIL${NC}"
        TEST_RESULT=1
    fi

    # Debug: Show linking results
    echo ""
    echo "Actual linking results (for debugging):"
    echo "----------------------------------------"
    echo "Story references found:"
    grep -o "STORY-[0-9]\+" "$TEST_DIR/test-rca.md" | sort -u || echo "(None found)"
    echo ""
    echo "Recommendation status:"
    grep -E "^- \[ \] REC-" "$TEST_DIR/test-rca.md" || echo "(No checklist items found)"
    echo "----------------------------------------"
    echo ""

    # Cleanup
    cleanup

    return $TEST_RESULT
}

# Run main function and exit with result
main
exit $?
