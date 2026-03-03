#!/bin/bash
# STORY-216: Run All Tests
# Executes all acceptance criteria tests for STORY-216
#
# TDD Red Phase: All tests should FAIL initially
# After implementation: All tests should PASS

# Note: Do NOT use set -e here - we want to run all tests even if some fail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=============================================="
echo "STORY-216: Phase 0 Completion Enforcement Tests"
echo "=============================================="
echo ""
echo "Target: .claude/skills/devforgeai-qa/SKILL.md"
echo "Story: Add Phase 0 Step 0.5 Enforcement for Deep Mode"
echo "Source: RCA-021 REC-2"
echo ""
echo "=============================================="
echo ""

TOTAL=4
PASSED=0
FAILED=0

# Function to run a test and track results
run_test() {
    local test_name=$1
    local test_file=$2

    echo "----------------------------------------"
    echo "Running: $test_name"
    echo "----------------------------------------"

    if bash "$test_file"; then
        echo ""
        echo ">>> PASSED: $test_name"
        ((PASSED++))
    else
        echo ""
        echo ">>> FAILED: $test_name"
        ((FAILED++))
    fi
    echo ""
}

# Run all tests
run_test "AC-1: Section Placement" "test-ac1-section-placement.sh"
run_test "AC-2: Verification Logic" "test-ac2-verification-logic.sh"
run_test "AC-3: Success Message" "test-ac3-success-message.sh"
run_test "AC-4: Exact Text (RCA-021)" "test-ac4-exact-text.sh"

# Summary
echo "=============================================="
echo "TEST SUMMARY"
echo "=============================================="
echo ""
echo "Total Tests: $TOTAL"
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "=============================================="
    echo "RESULT: ALL TESTS PASSED"
    echo "=============================================="
    echo ""
    echo "Story implementation complete!"
    exit 0
else
    echo "=============================================="
    echo "RESULT: $FAILED TEST(S) FAILED"
    echo "=============================================="
    echo ""
    echo "TDD Red Phase: Tests correctly failing before implementation"
    echo ""
    echo "Next steps:"
    echo "1. Implement Phase 0 Completion Enforcement section in SKILL.md"
    echo "2. Add section after 'Phase 0 Marker Write' (around line 311)"
    echo "3. Use exact text from RCA-021 REC-2 (lines 215-233)"
    echo "4. Re-run tests to verify implementation"
    exit 1
fi
