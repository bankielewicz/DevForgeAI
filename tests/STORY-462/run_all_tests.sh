#!/bin/bash
# Run all STORY-462 tests
# Story: STORY-462 - Handle Special Cases and Cleanup
# Generated: 2026-02-21
# TDD Phase: RED - All tests expected to FAIL before implementation

PROJECT_ROOT="${PROJECT_ROOT:-/mnt/c/Projects/DevForgeAI2}"
export PROJECT_ROOT

TESTS_DIR="$PROJECT_ROOT/src/tests/STORY-462"
TOTAL_PASSED=0
TOTAL_FAILED=0

echo "======================================================="
echo "  STORY-462 Test Suite - Handle Special Cases Cleanup"
echo "  TDD Phase: RED (tests should FAIL before implementation)"
echo "======================================================="
echo ""

run_test_file() {
    local test_file="$1"
    local test_name
    test_name=$(basename "$test_file")

    echo "--- Running: $test_name ---"
    bash "$test_file"
    local exit_code=$?

    if [ $exit_code -eq 0 ]; then
        echo "  >>> SUITE PASS: $test_name"
        ((TOTAL_PASSED++))
    else
        echo "  >>> SUITE FAIL: $test_name"
        ((TOTAL_FAILED++))
    fi
    echo ""
}

run_test_file "$TESTS_DIR/test_ac1_audit_w3_skill.sh"
run_test_file "$TESTS_DIR/test_ac2_dev_backup_deleted.sh"
run_test_file "$TESTS_DIR/test_ac3_orchestrate_trimmed.sh"
run_test_file "$TESTS_DIR/test_ac4_rca_stories_trimmed.sh"
run_test_file "$TESTS_DIR/test_ac5_fix_story_unchanged.sh"
run_test_file "$TESTS_DIR/test_ac6_backward_compat_output.sh"
run_test_file "$TESTS_DIR/test_ac7_governance_preserved.sh"
run_test_file "$TESTS_DIR/test_ac8_askuser_placement.sh"
run_test_file "$TESTS_DIR/test_ac9_audit_skill_complete.sh"

echo "======================================================="
echo "  OVERALL RESULTS"
echo "  Test suites passed: $TOTAL_PASSED"
echo "  Test suites failed: $TOTAL_FAILED"
echo "======================================================="

[ $TOTAL_FAILED -eq 0 ] && exit 0 || exit 1
