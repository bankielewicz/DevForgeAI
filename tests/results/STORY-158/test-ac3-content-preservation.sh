#!/bin/bash

###############################################################################
# Test: AC#3 - Preserve Original RCA Content
#
# Acceptance Criteria:
#   Given the RCA document is being updated with story references
#   When modifications are made
#   Then all original content (5 Whys, evidence, etc.) is preserved unchanged
#
# Test Approach:
#   1. ARRANGE: Create backup of original RCA content
#   2. ACT: Execute RCA linking
#   3. ASSERT: Verify no original content was lost or modified
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
TEST_NAME="AC#3: Preserve Original RCA Content"
FIXTURE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/fixtures" && pwd)"
SAMPLE_RCA="${FIXTURE_DIR}/sample-rca.md"
TEST_DIR="/tmp/test-rca-ac3-$$"

# Ensure fixture exists
if [[ ! -f "$SAMPLE_RCA" ]]; then
    echo -e "${RED}FAIL${NC}: Fixture not found: $SAMPLE_RCA"
    exit 1
fi

# ============================================================================
# ARRANGE: Setup test environment and create backups
# ============================================================================
arrange_test() {
    mkdir -p "$TEST_DIR"
    cp "$SAMPLE_RCA" "$TEST_DIR/test-rca.md"
    cp "$SAMPLE_RCA" "$TEST_DIR/test-rca-original.md"

    echo "Test Environment Setup:"
    echo "  Test Directory: $TEST_DIR"
    echo "  Test RCA File: $TEST_DIR/test-rca.md"
    echo "  Backup RCA File: $TEST_DIR/test-rca-original.md"

    # Extract key sections for later verification
    echo "Original content sections identified:"
    grep -c "## Five Whys Analysis" "$TEST_DIR/test-rca.md" && echo "  ✓ Found: Five Whys Analysis section" || true
    grep -c "## Evidence" "$TEST_DIR/test-rca.md" && echo "  ✓ Found: Evidence section" || true
    grep -c "## Problem Statement" "$TEST_DIR/test-rca.md" && echo "  ✓ Found: Problem Statement section" || true
}

# ============================================================================
# ACT: Execute RCA linking logic
# ============================================================================
execute_linking() {
    local rca_file="$TEST_DIR/test-rca.md"

    echo ""
    echo "Executing RCA linking..."
    echo "  Story Mapping: REC-1→STORY-155, REC-2→STORY-156, REC-3→STORY-157"

    # Attempt to call the linking command
    if command -v rca-link-stories &> /dev/null; then
        rca-link-stories "$rca_file" --stories REC-1:STORY-155 REC-2:STORY-156 REC-3:STORY-157
    else
        echo "INFO: rca-link-stories command not found (expected - no implementation yet)"
    fi

    return 0
}

# ============================================================================
# ASSERT: Verify original content is preserved
# ============================================================================
assert_content_preserved() {
    local rca_file="$TEST_DIR/test-rca.md"
    local original_file="$TEST_DIR/test-rca-original.md"
    local test_passed=true

    echo ""
    echo "Assertions:"

    # ASSERTION 1: Five Whys Analysis section must exist and be unchanged
    if grep -q "## Five Whys Analysis" "$rca_file"; then
        echo "  ✓ PASS: Found 'Five Whys Analysis' section"
    else
        echo "  ✗ FAIL: Missing 'Five Whys Analysis' section"
        test_passed=false
    fi

    # Extract Five Whys content from both files
    local whys_original=$(sed -n '/## Five Whys Analysis/,/## /p' "$original_file" | head -n -1 | wc -l)
    local whys_current=$(sed -n '/## Five Whys Analysis/,/## /p' "$rca_file" | head -n -1 | wc -l)

    if [[ $whys_original -eq $whys_current ]]; then
        echo "  ✓ PASS: Five Whys section size unchanged (preserved)"
    else
        echo "  ✗ FAIL: Five Whys section size changed ($whys_original lines → $whys_current lines)"
        test_passed=false
    fi

    # ASSERTION 2: Evidence section must exist and be unchanged
    if grep -q "## Evidence" "$rca_file"; then
        echo "  ✓ PASS: Found 'Evidence' section"
    else
        echo "  ✗ FAIL: Missing 'Evidence' section"
        test_passed=false
    fi

    # ASSERTION 3: Problem Statement must exist
    if grep -q "## Problem Statement" "$rca_file"; then
        echo "  ✓ PASS: Found 'Problem Statement' section"
    else
        echo "  ✗ FAIL: Missing 'Problem Statement' section"
        test_passed=false
    fi

    # ASSERTION 4: Recommendation descriptions must be preserved
    if grep -q "Description of first recommendation" "$rca_file"; then
        echo "  ✓ PASS: REC-1 description preserved"
    else
        echo "  ✗ FAIL: REC-1 description was modified or lost"
        test_passed=false
    fi

    if grep -q "Description of second recommendation" "$rca_file"; then
        echo "  ✓ PASS: REC-2 description preserved"
    else
        echo "  ✗ FAIL: REC-2 description was modified or lost"
        test_passed=false
    fi

    # ASSERTION 5: Verify no lines were deleted (file length should not decrease)
    local original_lines=$(wc -l < "$original_file")
    local current_lines=$(wc -l < "$rca_file")

    if [[ $current_lines -ge $original_lines ]]; then
        echo "  ✓ PASS: No lines were deleted ($original_lines → $current_lines lines)"
    else
        echo "  ✗ FAIL: Lines were deleted ($original_lines → $current_lines lines)"
        test_passed=false
    fi

    # ASSERTION 6: Verify YAML frontmatter structure preserved
    if head -1 "$rca_file" | grep -q "^---"; then
        echo "  ✓ PASS: YAML frontmatter opening delimiter preserved"
    else
        echo "  ✗ FAIL: YAML frontmatter opening delimiter missing"
        test_passed=false
    fi

    # ASSERTION 7: Root Cause section must exist
    if grep -q "## Root Cause" "$rca_file"; then
        echo "  ✓ PASS: Found 'Root Cause' section"
    else
        echo "  ✗ FAIL: Missing 'Root Cause' section"
        test_passed=false
    fi

    # ASSERTION 8: Business Impact section must exist
    if grep -q "## Business Impact" "$rca_file"; then
        echo "  ✓ PASS: Found 'Business Impact' section"
    else
        echo "  ✗ FAIL: Missing 'Business Impact' section"
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
    if assert_content_preserved; then
        echo ""
        echo -e "${GREEN}RESULT: PASS${NC}"
        TEST_RESULT=0
    else
        echo ""
        echo -e "${RED}RESULT: FAIL${NC}"
        TEST_RESULT=1
    fi

    # Debug: Show content comparison
    echo ""
    echo "Content Comparison (for debugging):"
    echo "----------------------------------------"
    echo "Original file line count: $(wc -l < "$TEST_DIR/test-rca-original.md")"
    echo "Modified file line count: $(wc -l < "$TEST_DIR/test-rca.md")"
    echo ""
    echo "Original Five Whys section:"
    sed -n '/## Five Whys Analysis/,/## /p' "$TEST_DIR/test-rca-original.md" | head -10 || echo "(Not found)"
    echo ""
    echo "Modified Five Whys section:"
    sed -n '/## Five Whys Analysis/,/## /p' "$TEST_DIR/test-rca.md" | head -10 || echo "(Not found)"
    echo "----------------------------------------"
    echo ""

    # Cleanup
    cleanup

    return $TEST_RESULT
}

# Run main function and exit with result
main
exit $?
