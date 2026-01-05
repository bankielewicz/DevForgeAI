#!/bin/bash
# STORY-174: Run All Tests
#
# Executes all AC tests for STORY-174 and reports results
#
# Usage: ./run_all_tests.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_COUNT=0
PASS_COUNT=0
FAIL_COUNT=0

echo "=============================================="
echo "STORY-174: Execution-Mode Frontmatter Tests"
echo "=============================================="
echo ""
echo "Running TDD Red Phase tests (all should FAIL)..."
echo ""

# Find and run all test scripts
for TEST_FILE in "${SCRIPT_DIR}"/test_ac*.sh; do
    if [[ -f "${TEST_FILE}" ]]; then
        TEST_NAME=$(basename "${TEST_FILE}")
        ((TEST_COUNT++))

        echo "----------------------------------------------"
        echo "Running: ${TEST_NAME}"
        echo "----------------------------------------------"

        # Run test and capture exit code
        if bash "${TEST_FILE}"; then
            ((PASS_COUNT++))
            echo ""
            echo "Result: PASS"
        else
            ((FAIL_COUNT++))
            echo ""
            echo "Result: FAIL (expected in TDD Red phase)"
        fi
        echo ""
    fi
done

echo "=============================================="
echo "TEST SUMMARY"
echo "=============================================="
echo "Total Tests: ${TEST_COUNT}"
echo "Passed:      ${PASS_COUNT}"
echo "Failed:      ${FAIL_COUNT}"
echo ""

if [[ ${FAIL_COUNT} -gt 0 ]]; then
    echo "TDD Red Phase Status: CORRECT"
    echo "Tests are failing as expected. Ready for implementation."
    exit 0  # Exit 0 because failing tests are expected in Red phase
else
    echo "WARNING: All tests passed!"
    echo "This is unexpected in TDD Red phase."
    echo "Either implementation already exists or tests are incorrect."
    exit 1  # Exit 1 because passing tests are unexpected
fi
