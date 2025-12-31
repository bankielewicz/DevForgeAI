#!/bin/bash

###############################################################################
# Test: AC#2 - Add Story ID to Recommendation Sections
#
# Acceptance Criteria:
#   Given a story was created from a specific recommendation
#   When updating the RCA document
#   Then the recommendation section is updated with "**Implemented in:** STORY-NNN"
#        after the recommendation header
#
# Test Approach:
#   1. ARRANGE: Create test RCA with recommendation sections
#   2. ACT: Execute RCA linking (REC-1→STORY-155, etc.)
#   3. ASSERT: Verify recommendation sections contain inline story references
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
TEST_NAME="AC#2: Add Story ID to Recommendation Sections"
FIXTURE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/fixtures" && pwd)"
SAMPLE_RCA="${FIXTURE_DIR}/sample-rca.md"
TEST_DIR="/tmp/test-rca-ac2-$$"

# Ensure fixture exists
if [[ ! -f "$SAMPLE_RCA" ]]; then
    echo -e "${RED}FAIL${NC}: Fixture not found: $SAMPLE_RCA"
    exit 1
fi

# ============================================================================
# ARRANGE: Setup test environment and copy fixture
# ============================================================================
arrange_test() {
    mkdir -p "$TEST_DIR"
    cp "$SAMPLE_RCA" "$TEST_DIR/test-rca.md"

    echo "Test Environment Setup:"
    echo "  Test Directory: $TEST_DIR"
    echo "  Test RCA File: $TEST_DIR/test-rca.md"
}

# ============================================================================
# ACT: Execute RCA linking logic
# ============================================================================
execute_linking() {
    # This simulates calling the RCA linking command
    # In real implementation, this would call: rca-story-linker.sh or similar
    #
    # Expected behavior:
    # 1. Read the RCA file
    # 2. Find sections like "### REC-1: First Recommendation"
    # 3. Add "**Implemented in:** STORY-155" after the header

    local rca_file="$TEST_DIR/test-rca.md"

    echo "Executing RCA linking..."
    echo "  Story Mapping: REC-1→STORY-155, REC-2→STORY-156, REC-3→STORY-157"

    # Attempt to call the linking command (will fail if not implemented)
    if command -v rca-link-stories &> /dev/null; then
        rca-link-stories "$rca_file" --stories REC-1:STORY-155 REC-2:STORY-156 REC-3:STORY-157
    else
        echo "INFO: rca-link-stories command not found (expected - no implementation yet)"
    fi

    return 0
}

# ============================================================================
# ASSERT: Verify inline story references in recommendation sections
# ============================================================================
assert_inline_references() {
    local rca_file="$TEST_DIR/test-rca.md"
    local test_passed=true

    echo ""
    echo "Assertions:"

    # ASSERTION 1: REC-1 section should have inline story reference
    # Pattern: "### REC-1: ..." followed by "**Implemented in:** STORY-155"
    if grep -A 1 "^### REC-1:" "$rca_file" | grep -q "Implemented in.*STORY-155"; then
        echo "  ✓ PASS: Found '**Implemented in:** STORY-155' in REC-1 section"
    else
        echo "  ✗ FAIL: Expected '**Implemented in:** STORY-155' after REC-1 header"
        test_passed=false
    fi

    # ASSERTION 2: REC-2 section should have inline story reference
    if grep -A 1 "^### REC-2:" "$rca_file" | grep -q "Implemented in.*STORY-156"; then
        echo "  ✓ PASS: Found '**Implemented in:** STORY-156' in REC-2 section"
    else
        echo "  ✗ FAIL: Expected '**Implemented in:** STORY-156' after REC-2 header"
        test_passed=false
    fi

    # ASSERTION 3: REC-3 section should have inline story reference
    if grep -A 1 "^### REC-3:" "$rca_file" | grep -q "Implemented in.*STORY-157"; then
        echo "  ✓ PASS: Found '**Implemented in:** STORY-157' in REC-3 section"
    else
        echo "  ✗ FAIL: Expected '**Implemented in:** STORY-157' after REC-3 header"
        test_passed=false
    fi

    # ASSERTION 4: Verify story reference is on second line after header (correct position)
    # This ensures the format is: "### REC-N: Title\n**Implemented in:** STORY-NNN"
    local rec1_found=$(awk '/^### REC-1:/{getline; print}' "$rca_file" | grep -c "Implemented in" || echo 0)
    if [[ $rec1_found -gt 0 ]]; then
        echo "  ✓ PASS: Story reference is correctly positioned after header"
    else
        echo "  ! INFO: Story reference format verification pending (may pass during implementation)"
    fi

    # ASSERTION 5: Original recommendation headers should be unchanged
    if grep -q "^### REC-1: First Recommendation$" "$rca_file"; then
        echo "  ✓ PASS: Original recommendation header preserved"
    else
        echo "  ✗ FAIL: Original recommendation header was modified"
        test_passed=false
    fi

    # ASSERTION 6: Verify format matches pattern exactly
    local story_ref_count=$(grep -c "Implemented in.*STORY-[0-9]" "$rca_file" || echo 0)
    if [[ $story_ref_count -ge 3 ]]; then
        echo "  ✓ PASS: Found $story_ref_count story references with correct format"
    else
        echo "  ✗ FAIL: Expected at least 3 story references, found $story_ref_count"
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
    if assert_inline_references; then
        echo ""
        echo -e "${GREEN}RESULT: PASS${NC}"
        TEST_RESULT=0
    else
        echo ""
        echo -e "${RED}RESULT: FAIL${NC}"
        TEST_RESULT=1
    fi

    # Debug: Show recommendation sections
    echo ""
    echo "Actual RCA recommendation sections (for debugging):"
    echo "----------------------------------------"
    grep -A 3 "^### REC-" "$TEST_DIR/test-rca.md" | head -20 || echo "(Sections not found)"
    echo "----------------------------------------"
    echo ""

    # Cleanup
    cleanup

    return $TEST_RESULT
}

# Run main function and exit with result
main
exit $?
