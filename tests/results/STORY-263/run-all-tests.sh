#!/bin/bash
# STORY-263: Run all tests for gaps.json auto-detection feature
# TDD Red Phase - All tests expected to FAIL (feature not yet implemented)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STORY_ID="STORY-263"

echo "========================================================================"
echo "  ${STORY_ID}: gaps.json Auto-Detection Tests"
echo "  TDD Red Phase - Tests should FAIL (feature not implemented)"
echo "========================================================================"
echo ""
echo "Test Directory: ${SCRIPT_DIR}"
echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Track results
TOTAL_TESTS=0
TESTS_PASSED=0
TESTS_FAILED=0

# Run each test file
for test_file in "${SCRIPT_DIR}"/test-*.sh; do
    if [[ -f "${test_file}" && "${test_file}" != *"run-all-tests.sh" ]]; then
        ((TOTAL_TESTS++))
        test_name=$(basename "${test_file}" .sh)

        echo ""
        echo "--------------------------------------------------------------------"
        echo "Running: ${test_name}"
        echo "--------------------------------------------------------------------"

        # Run the test
        bash "${test_file}"
        exit_code=$?

        if [[ ${exit_code} -eq 0 ]]; then
            ((TESTS_PASSED++))
            echo ""
            echo "[PASSED] ${test_name}"
        else
            ((TESTS_FAILED++))
            echo ""
            echo "[FAILED] ${test_name}"
        fi
    fi
done

# Summary
echo ""
echo "========================================================================"
echo "  TEST SUMMARY: ${STORY_ID}"
echo "========================================================================"
echo ""
echo "  Total Tests:  ${TOTAL_TESTS}"
echo "  Passed:       ${TESTS_PASSED}"
echo "  Failed:       ${TESTS_FAILED}"
echo ""

# TDD Red phase expectation
if [[ ${TESTS_FAILED} -gt 0 ]]; then
    echo "  STATUS: TDD RED PHASE CONFIRMED"
    echo "          Tests failing as expected (feature not implemented)"
    echo ""
    echo "  Next: Implement Phase 01.0.3 in dev.md to make tests pass"
else
    echo "  STATUS: UNEXPECTED - All tests passed!"
    echo "          Either feature is already implemented or tests are incorrect"
fi

echo ""
echo "========================================================================"

# Exit with failure count (for CI integration)
exit ${TESTS_FAILED}
