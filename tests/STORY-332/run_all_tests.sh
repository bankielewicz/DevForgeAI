#!/bin/bash
# Test Runner: STORY-332 - All Acceptance Criteria Tests
# Story: Refactor session-miner.md with Progressive Disclosure
#
# Usage: bash tests/STORY-332/run_all_tests.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$PROJECT_ROOT"

echo "=============================================="
echo "  STORY-332: Progressive Disclosure Refactor"
echo "  Running All Acceptance Criteria Tests"
echo "=============================================="
echo ""
echo "Project Root: $PROJECT_ROOT"
echo "Test Directory: $SCRIPT_DIR"
echo ""

# Track overall results
TOTAL_TESTS=6
PASSED_TESTS=0
FAILED_TESTS=0

# Run each test and track results
run_test() {
    local test_name=$1
    local test_file=$2

    echo "----------------------------------------------"
    echo "Running: $test_name"
    echo "----------------------------------------------"

    if bash "$test_file"; then
        echo ""
        echo ">>> $test_name: PASSED"
        ((PASSED_TESTS++))
    else
        echo ""
        echo ">>> $test_name: FAILED"
        ((FAILED_TESTS++))
    fi
    echo ""
}

# Run all AC tests
run_test "AC#1 - Core File Size Compliance" "$SCRIPT_DIR/test_ac1_core_file_size.sh"
run_test "AC#2 - Reference Directory Structure" "$SCRIPT_DIR/test_ac2_reference_directory.sh"
run_test "AC#3 - Reference Loading Instructions" "$SCRIPT_DIR/test_ac3_reference_loading.sh"
run_test "AC#4 - Functionality Preservation" "$SCRIPT_DIR/test_ac4_functionality_preservation.sh"
run_test "AC#5 - Observation Capture Section" "$SCRIPT_DIR/test_ac5_observation_capture.sh"
run_test "AC#6 - Operational Copy Synchronization" "$SCRIPT_DIR/test_ac6_sync_verification.sh"

# Final Summary
echo "=============================================="
echo "  STORY-332 TEST SUMMARY"
echo "=============================================="
echo ""
echo "  Acceptance Criteria Tests: $TOTAL_TESTS"
echo "  Passed: $PASSED_TESTS"
echo "  Failed: $FAILED_TESTS"
echo ""

if [[ $FAILED_TESTS -eq 0 ]]; then
    echo "  OVERALL STATUS: ALL TESTS PASSED"
    echo ""
    echo "  The session-miner.md refactoring is complete and"
    echo "  meets all acceptance criteria."
    exit 0
else
    echo "  OVERALL STATUS: $FAILED_TESTS TEST(S) FAILED"
    echo ""
    echo "  TDD Phase: RED (failing tests as expected)"
    echo "  Next: Implement the refactoring to make tests pass"
    exit 1
fi
