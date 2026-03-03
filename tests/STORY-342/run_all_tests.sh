#!/bin/bash
# STORY-342: Run All Acceptance Criteria Tests
# Tests Long-Term Memory Layer implementation

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
export PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$SCRIPT_DIR/../.." && pwd)}"

echo "========================================"
echo "  STORY-342: Long-Term Memory Layer"
echo "  Acceptance Criteria Test Suite"
echo "========================================"
echo ""
echo "Project Root: $PROJECT_ROOT"
echo "Test Directory: $SCRIPT_DIR"
echo ""

PASSED=0
FAILED=0
TOTAL=7

run_test() {
    local test_name=$1
    local test_file=$2

    echo "----------------------------------------"
    echo "Running: $test_name"
    echo "----------------------------------------"

    if bash "$SCRIPT_DIR/$test_file"; then
        ((PASSED++))
        echo "Result: PASSED"
    else
        ((FAILED++))
        echo "Result: FAILED"
    fi
    echo ""
}

# Run all AC tests
run_test "AC#1: ADR Prerequisite" "test_ac1_adr_prerequisite.sh"
run_test "AC#2: tdd-patterns.md" "test_ac2_tdd_patterns.sh"
run_test "AC#3: friction-catalog.md" "test_ac3_friction_catalog.sh"
run_test "AC#4: success-patterns.md" "test_ac4_success_patterns.sh"
run_test "AC#5: Pattern Detection" "test_ac5_pattern_detection.sh"
run_test "AC#6: Emerging Patterns" "test_ac6_emerging_patterns.sh"
run_test "AC#7: Confidence Levels" "test_ac7_confidence_levels.sh"

# Summary
echo "========================================"
echo "  Test Summary"
echo "========================================"
echo "Total:  $TOTAL"
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "All tests PASSED!"
    exit 0
else
    echo "Some tests FAILED. Implementation incomplete."
    exit 1
fi
