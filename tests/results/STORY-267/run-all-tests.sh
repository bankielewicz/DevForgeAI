#!/bin/bash
# STORY-267: Run All Acceptance Criteria Tests
# Document Language-Agnostic Runtime Smoke Test in Deep Validation Workflow Reference
#
# This script runs all 5 AC tests and provides a summary

# Note: No 'set -e' - we need to run all tests even if some fail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STORY_ID="STORY-267"

echo "================================================================"
echo "  ${STORY_ID} - Complete Test Suite"
echo "  Document Language-Agnostic Runtime Smoke Test"
echo "================================================================"
echo ""
echo "Test Directory: ${SCRIPT_DIR}"
echo "Target File: .claude/skills/devforgeai-qa/references/deep-validation-workflow.md"
echo ""
echo "Running all acceptance criteria tests..."
echo ""

# Track overall results
TOTAL_PASSED=0
TOTAL_FAILED=0
FAILED_TESTS=()

# Function to run a test and capture result
run_test() {
    local TEST_FILE="$1"
    local AC_NAME="$2"

    echo "----------------------------------------------------------------"
    echo "Running: ${AC_NAME}"
    echo "----------------------------------------------------------------"

    if bash "${SCRIPT_DIR}/${TEST_FILE}"; then
        ((TOTAL_PASSED++))
        echo ""
    else
        ((TOTAL_FAILED++))
        FAILED_TESTS+=("${AC_NAME}")
        echo ""
    fi
}

# Run all tests
run_test "test-ac1-section-exists.sh" "AC#1: Section 1.4 Runtime Smoke Test Exists"
run_test "test-ac2-all-languages.sh" "AC#2: All 6 Supported Languages Documented"
run_test "test-ac3-project-type-detection.sh" "AC#3: Project Type Detection Logic"
run_test "test-ac4-output-formats.sh" "AC#4: Success/Failure Output Formats"
run_test "test-ac5-extensibility-pattern.sh" "AC#5: Extensibility Pattern"

# Final Summary
echo ""
echo "================================================================"
echo "  ${STORY_ID} - FINAL SUMMARY"
echo "================================================================"
echo ""
echo "  Acceptance Criteria Passed: ${TOTAL_PASSED}/5"
echo "  Acceptance Criteria Failed: ${TOTAL_FAILED}/5"
echo ""

if [[ ${TOTAL_FAILED} -gt 0 ]]; then
    echo "  Failed Tests:"
    for FAILED in "${FAILED_TESTS[@]}"; do
        echo "    - ${FAILED}"
    done
    echo ""
fi

# Calculate coverage percentage
COVERAGE=$((TOTAL_PASSED * 100 / 5))
echo "  Test Coverage: ${COVERAGE}%"
echo ""

if [[ ${TOTAL_FAILED} -eq 0 ]]; then
    echo "================================================================"
    echo "  OVERALL RESULT: ALL TESTS PASSED"
    echo "================================================================"
    exit 0
else
    echo "================================================================"
    echo "  OVERALL RESULT: TESTS FAILED (TDD Red Phase)"
    echo "  These tests should FAIL until documentation is implemented."
    echo "================================================================"
    exit 1
fi
