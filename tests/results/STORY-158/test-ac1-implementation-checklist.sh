#!/bin/bash

###############################################################################
# Test: AC#1 - Update RCA Implementation Checklist with Story References
#
# Acceptance Criteria:
#   Given stories have been created from RCA recommendations
#   When updating the RCA document
#   Then the Implementation Checklist section is updated with story references
#        (e.g., "- [ ] REC-1: See STORY-155")
#
# Test Approach:
#   1. ARRANGE: Create test RCA with original Implementation Checklist
#   2. ACT: Call RCA linking with story map (REC-1→STORY-155, REC-2→STORY-156)
#   3. ASSERT: Verify checklist is updated with story references
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
TEST_NAME="AC#1: Update RCA Implementation Checklist with Story References"
FIXTURE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/fixtures" && pwd)"
SAMPLE_RCA="${FIXTURE_DIR}/sample-rca.md"
TEST_DIR="/tmp/test-rca-ac1-$$"

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
    # This simulates calling the RCA linking command with story map
    # In real implementation, this would call: rca-story-linker.sh or similar
    #
    # For now, simulate what the linking should do:
    # 1. Read the RCA file
    # 2. Find "## Implementation Checklist" section
    # 3. Update lines: "- [ ] REC-N" to "- [ ] REC-N: See STORY-NNN"

    local rca_file="$TEST_DIR/test-rca.md"

    # Build story mapping from recommendations
    declare -A story_map
    story_map["REC-1"]="STORY-155"
    story_map["REC-2"]="STORY-156"
    story_map["REC-3"]="STORY-157"

    # This is a placeholder - in real implementation, this would be actual code
    # that modifies the RCA file. For testing purposes, we expect:
    # - COMMAND to fail (no implementation yet)
    # - OR file unchanged (linking not applied)

    echo "Executing RCA linking..."
    echo "  Story Mapping: REC-1→STORY-155, REC-2→STORY-156, REC-3→STORY-157"

    # Attempt to call the linking command (will fail if not implemented)
    if command -v rca-link-stories &> /dev/null; then
        rca-link-stories "$rca_file" --stories REC-1:STORY-155 REC-2:STORY-156 REC-3:STORY-157
    else
        # Command doesn't exist yet (expected in TDD Red phase)
        echo "INFO: rca-link-stories command not found (expected - no implementation yet)"
    fi

    return 0
}

# ============================================================================
# ASSERT: Verify checklist was updated with story references
# ============================================================================
assert_checklist_updated() {
    local rca_file="$TEST_DIR/test-rca.md"
    local test_passed=true

    echo ""
    echo "Assertions:"

    # ASSERTION 1: Checklist should contain "REC-1: See STORY-155"
    if grep -qE -- '- \[.\] REC-1: See STORY-155' "$rca_file"; then
        echo "  ✓ PASS: Found '- [ ] REC-1: See STORY-155' in Implementation Checklist"
    else
        echo "  ✗ FAIL: Expected '- [ ] REC-1: See STORY-155' not found"
        test_passed=false
    fi

    # ASSERTION 2: Checklist should contain "REC-2: See STORY-156"
    if grep -qE -- '- \[.\] REC-2: See STORY-156' "$rca_file"; then
        echo "  ✓ PASS: Found '- [ ] REC-2: See STORY-156' in Implementation Checklist"
    else
        echo "  ✗ FAIL: Expected '- [ ] REC-2: See STORY-156' not found"
        test_passed=false
    fi

    # ASSERTION 3: Original format should NOT exist (replaced by linked version)
    # This regex checks for "- [ ] REC-1" NOT followed by ": See STORY"
    if grep -E -- '^- \[.\] REC-[0-9]+$' "$rca_file" | grep -v "STORY" > /dev/null; then
        echo "  ✗ FAIL: Found original format '- [ ] REC-N' (should be updated)"
        test_passed=false
    else
        echo "  ✓ PASS: Original format not found (successfully replaced)"
    fi

    # ASSERTION 4: Verify format is correct (line should match exact pattern)
    if grep -qE -- '^- \[.\] REC-[0-9]+: See STORY-[0-9]+$' "$rca_file"; then
        echo "  ✓ PASS: Checklist format matches expected pattern"
    else
        echo "  ✗ FAIL: Checklist format does not match expected pattern"
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
    if assert_checklist_updated; then
        echo ""
        echo -e "${GREEN}RESULT: PASS${NC}"
        TEST_RESULT=0
    else
        echo ""
        echo -e "${RED}RESULT: FAIL${NC}"
        TEST_RESULT=1
    fi

    # Debug: Show actual file content
    echo ""
    echo "Actual RCA file content (for debugging):"
    echo "----------------------------------------"
    cat "$TEST_DIR/test-rca.md" | grep -A 10 "## Implementation Checklist" || echo "(Section not found)"
    echo "----------------------------------------"
    echo ""

    # Cleanup
    cleanup

    return $TEST_RESULT
}

# Run main function and exit with result
main
exit $?
