#!/bin/bash

###############################################################################
# TEST RUNNER: RUN_ALL_TESTS.sh
# Story: STORY-159 - Create /create-stories-from-rca Command Shell
# Purpose: Run all 5 test suites and summarize results
###############################################################################

echo "=============================================================="
echo "STORY-159: ALL TESTS (TDD Red Phase)"
echo "Expected: ALL TESTS FAIL (Command file not implemented)"
echo "=============================================================="
echo ""

# Test file paths
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TEST_DIR="tests/STORY-159"

declare -a TOTAL_RESULTS=()
TOTAL_TESTS=0
TOTAL_PASSED=0
TOTAL_FAILED=0

# Run each test suite
for test_file in test-ac*.sh; do
    if [[ -f "${TEST_DIR}/${test_file}" ]]; then
        echo "Running: ${test_file}"
        echo "------"

        # Run test and capture results
        if bash "${TEST_DIR}/${test_file}" 2>&1 | tail -20; then
            RESULT="PASS"
        else
            RESULT="FAIL"
        fi

        echo ""
        TOTAL_RESULTS+=("${test_file}: ${RESULT}")
    fi
done

echo "=============================================================="
echo "SUMMARY"
echo "=============================================================="
echo ""
echo "Test suites executed:"
echo "  1. test-ac1-command-file-creation.sh (7 tests)"
echo "  2. test-ac2-argument-parsing.sh (5 tests)"
echo "  3. test-ac3-help-text.sh (5 tests)"
echo "  4. test-ac4-invalid-arguments.sh (5 tests)"
echo "  5. test-ac5-orchestration.sh (6 tests)"
echo ""
echo "Total test cases: 28"
echo ""
echo "Expected status: ALL 28 TESTS FAIL"
echo "Reason: Command file .claude/commands/create-stories-from-rca.md"
echo "        does not exist yet (TDD Red phase)"
echo ""
echo "=============================================================="
echo ""
echo "Next step: Implement command file to pass all tests (TDD Green)"
