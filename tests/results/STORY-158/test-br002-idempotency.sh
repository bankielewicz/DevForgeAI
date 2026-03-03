#!/bin/bash

###############################################################################
# Test: BR#002 - Idempotency
#
# Business Rule:
#   Idempotency: Re-running command does not duplicate links
#
# Test Description:
#   Given RCA linking has already been applied
#   When the RCA linking command is executed again
#   Then the file remains unchanged; no duplicate story references are added
#
# Test Approach:
#   1. ARRANGE: Create test RCA and execute linking (first run)
#   2. ACT: Capture file contents, then execute linking again (second run)
#   3. ASSERT: Verify file contents are identical; no duplicates
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
TEST_NAME="BR#002: Idempotency - Re-running does not duplicate links"
FIXTURE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/fixtures" && pwd)"
SAMPLE_RCA="${FIXTURE_DIR}/sample-rca.md"
TEST_DIR="/tmp/test-rca-idempotency-$$"

# Ensure fixture exists
if [[ ! -f "$SAMPLE_RCA" ]]; then
    echo -e "${RED}FAIL${NC}: Fixture not found: $SAMPLE_RCA"
    exit 1
fi

# ============================================================================
# ARRANGE: Setup test environment
# ============================================================================
arrange_test() {
    mkdir -p "$TEST_DIR"
    cp "$SAMPLE_RCA" "$TEST_DIR/test-rca.md"

    echo "Test Environment Setup:"
    echo "  Test Directory: $TEST_DIR"
    echo "  Test RCA File: $TEST_DIR/test-rca.md"
    echo ""
    echo "Test Plan:"
    echo "  1. Execute RCA linking (PASS 1)"
    echo "  2. Capture file hash and content"
    echo "  3. Execute RCA linking again (PASS 2)"
    echo "  4. Compare file hash and content"
    echo "  5. Verify no duplicates exist"
}

# ============================================================================
# ACT: Execute RCA linking - First pass
# ============================================================================
execute_linking_pass_1() {
    local rca_file="$TEST_DIR/test-rca.md"

    echo ""
    echo "PASS 1: First RCA linking execution"
    echo "Executing RCA linking..."
    echo "  REC-1 → STORY-155"
    echo "  REC-2 → STORY-156"
    echo "  REC-3 → STORY-157"

    # Attempt to call the linking command
    if command -v rca-link-stories &> /dev/null; then
        rca-link-stories "$rca_file" --stories REC-1:STORY-155 REC-2:STORY-156 REC-3:STORY-157
    else
        echo "INFO: rca-link-stories command not found (expected - no implementation yet)"
    fi

    return 0
}

# ============================================================================
# ACT: Capture file state after first pass
# ============================================================================
capture_state_pass_1() {
    local rca_file="$TEST_DIR/test-rca.md"

    echo ""
    echo "Capturing file state after PASS 1..."

    # Calculate hash of file
    if command -v md5sum &> /dev/null; then
        md5sum "$rca_file" > "$TEST_DIR/hash-pass1.txt"
        echo "  File MD5: $(cat "$TEST_DIR/hash-pass1.txt")"
    else
        sha256sum "$rca_file" > "$TEST_DIR/hash-pass1.txt"
        echo "  File SHA256: $(cat "$TEST_DIR/hash-pass1.txt")"
    fi

    # Copy file for comparison
    cp "$rca_file" "$TEST_DIR/test-rca-pass1.md"
    echo "  File size: $(wc -c < "$rca_file") bytes"
    echo "  Line count: $(wc -l < "$rca_file") lines"

    # Count story references
    local story_count=$(grep -o "STORY-[0-9]\+" "$rca_file" | wc -l)
    echo "  Story references: $story_count"
}

# ============================================================================
# ACT: Execute RCA linking - Second pass
# ============================================================================
execute_linking_pass_2() {
    local rca_file="$TEST_DIR/test-rca.md"

    echo ""
    echo "PASS 2: Second RCA linking execution (idempotency test)"
    echo "Executing RCA linking again with same parameters..."
    echo "  REC-1 → STORY-155"
    echo "  REC-2 → STORY-156"
    echo "  REC-3 → STORY-157"

    # Attempt to call the linking command again
    if command -v rca-link-stories &> /dev/null; then
        rca-link-stories "$rca_file" --stories REC-1:STORY-155 REC-2:STORY-156 REC-3:STORY-157
    else
        echo "INFO: rca-link-stories command not found (expected - no implementation yet)"
    fi

    return 0
}

# ============================================================================
# ACT: Capture file state after second pass
# ============================================================================
capture_state_pass_2() {
    local rca_file="$TEST_DIR/test-rca.md"

    echo ""
    echo "Capturing file state after PASS 2..."

    # Calculate hash of file
    if command -v md5sum &> /dev/null; then
        md5sum "$rca_file" > "$TEST_DIR/hash-pass2.txt"
        echo "  File MD5: $(cat "$TEST_DIR/hash-pass2.txt")"
    else
        sha256sum "$rca_file" > "$TEST_DIR/hash-pass2.txt"
        echo "  File SHA256: $(cat "$TEST_DIR/hash-pass2.txt")"
    fi

    # Copy file for comparison
    cp "$rca_file" "$TEST_DIR/test-rca-pass2.md"
    echo "  File size: $(wc -c < "$rca_file") bytes"
    echo "  Line count: $(wc -l < "$rca_file") lines"

    # Count story references
    local story_count=$(grep -o "STORY-[0-9]\+" "$rca_file" | wc -l)
    echo "  Story references: $story_count"
}

# ============================================================================
# ASSERT: Verify idempotency
# ============================================================================
assert_idempotency() {
    local pass1_file="$TEST_DIR/test-rca-pass1.md"
    local pass2_file="$TEST_DIR/test-rca-pass2.md"
    local test_passed=true

    echo ""
    echo "Assertions:"

    # ASSERTION 1: File hashes should be identical
    local hash_pass1=$(cat "$TEST_DIR/hash-pass1.txt" | cut -d' ' -f1)
    local hash_pass2=$(cat "$TEST_DIR/hash-pass2.txt" | cut -d' ' -f1)

    if [[ "$hash_pass1" == "$hash_pass2" ]]; then
        echo "  ✓ PASS: File content identical after second run (hashes match)"
    else
        echo "  ✗ FAIL: File content changed after second run"
        echo "    Pass 1 hash: $hash_pass1"
        echo "    Pass 2 hash: $hash_pass2"
        test_passed=false
    fi

    # ASSERTION 2: Files should be byte-for-byte identical using diff
    if diff -q "$pass1_file" "$pass2_file" > /dev/null 2>&1; then
        echo "  ✓ PASS: File contents are byte-for-byte identical (diff passed)"
    else
        echo "  ✗ FAIL: File contents differ between passes (diff failed)"
        test_passed=false
    fi

    # ASSERTION 3: Story reference count should be identical
    local count_pass1=$(grep -o "STORY-[0-9]\+" "$pass1_file" | wc -l)
    local count_pass2=$(grep -o "STORY-[0-9]\+" "$pass2_file" | wc -l)

    if [[ $count_pass1 -eq $count_pass2 ]]; then
        echo "  ✓ PASS: Story reference count unchanged ($count_pass1 references)"
    else
        echo "  ✗ FAIL: Story reference count changed ($count_pass1 → $count_pass2)"
        test_passed=false
    fi

    # ASSERTION 4: No duplicate story references should exist
    local unique_stories=$(grep -o "STORY-[0-9]\+" "$pass2_file" | sort -u | wc -l)
    if [[ $unique_stories -eq 3 ]]; then
        echo "  ✓ PASS: Only 3 unique story references (no duplicates)"
    else
        echo "  ✗ FAIL: Expected 3 unique story references, found $unique_stories"
        test_passed=false
    fi

    # ASSERTION 5: Checklist items should not be duplicated
    local rec1_count=$(grep -c "^- \[ \] REC-1" "$pass2_file" || echo 0)
    if [[ $rec1_count -eq 1 ]]; then
        echo "  ✓ PASS: REC-1 checklist item not duplicated ($rec1_count occurrence)"
    else
        echo "  ✗ FAIL: REC-1 checklist item duplicated ($rec1_count occurrences)"
        test_passed=false
    fi

    local rec2_count=$(grep -c "^- \[ \] REC-2" "$pass2_file" || echo 0)
    if [[ $rec2_count -eq 1 ]]; then
        echo "  ✓ PASS: REC-2 checklist item not duplicated ($rec2_count occurrence)"
    else
        echo "  ✗ FAIL: REC-2 checklist item duplicated ($rec2_count occurrences)"
        test_passed=false
    fi

    # ASSERTION 6: Line count should not increase on second run
    local lines_pass1=$(wc -l < "$pass1_file")
    local lines_pass2=$(wc -l < "$pass2_file")

    if [[ $lines_pass1 -eq $lines_pass2 ]]; then
        echo "  ✓ PASS: Line count unchanged ($lines_pass1 lines)"
    else
        echo "  ✗ FAIL: Line count changed ($lines_pass1 → $lines_pass2 lines)"
        test_passed=false
    fi

    # ASSERTION 7: File size should not change
    local size_pass1=$(wc -c < "$pass1_file")
    local size_pass2=$(wc -c < "$pass2_file")

    if [[ $size_pass1 -eq $size_pass2 ]]; then
        echo "  ✓ PASS: File size unchanged ($size_pass1 bytes)"
    else
        echo "  ✗ FAIL: File size changed ($size_pass1 → $size_pass2 bytes)"
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
    execute_linking_pass_1 || true
    capture_state_pass_1
    echo ""

    execute_linking_pass_2 || true
    capture_state_pass_2
    echo ""

    # Assert phase
    if assert_idempotency; then
        echo ""
        echo -e "${GREEN}RESULT: PASS${NC}"
        TEST_RESULT=0
    else
        echo ""
        echo -e "${RED}RESULT: FAIL${NC}"
        TEST_RESULT=1
    fi

    # Debug: Show file comparison
    echo ""
    echo "File comparison (for debugging):"
    echo "----------------------------------------"
    echo "Diff output (should be empty for identical files):"
    diff "$TEST_DIR/test-rca-pass1.md" "$TEST_DIR/test-rca-pass2.md" || echo "  (Files differ - see above)"
    echo ""
    echo "Story references in Pass 2:"
    grep -o "STORY-[0-9]\+" "$TEST_DIR/test-rca-pass2.md" | sort | uniq -c
    echo "----------------------------------------"
    echo ""

    # Cleanup
    cleanup

    return $TEST_RESULT
}

# Run main function and exit with result
main
exit $?
