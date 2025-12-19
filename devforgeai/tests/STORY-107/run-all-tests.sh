#!/bin/bash

#################################################################################
# STORY-107 Test Suite Runner
# Purpose: Execute all tests for STORY-107 and generate summary report
#################################################################################

set -e

# Test configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SUMMARY_FILE="${SCRIPT_DIR}/test-summary.json"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Make test scripts executable
chmod +x "${SCRIPT_DIR}"/*.sh

# Initialize summary counters
TOTAL_TESTS=0
TOTAL_PASSED=0
TOTAL_FAILED=0
TEST_RESULTS=()

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║          STORY-107 Test Suite Execution                        ║"
echo "║     Documentation and User Guide Updates                        ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Starting test execution at $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Array of test files to execute
TEST_FILES=(
    "test-ac1-user-guide.sh"
    "test-ac2-architecture-doc.sh"
    "test-ac3-troubleshooting.sh"
    "test-ac4-migration-guide.sh"
    "test-ac5-inline-docs.sh"
    "test-links-verification.sh"
)

# Track overall exit code
OVERALL_EXIT_CODE=0

# Execute each test
for test_file in "${TEST_FILES[@]}"; do
    TEST_PATH="${SCRIPT_DIR}/${test_file}"

    if [ -f "${TEST_PATH}" ]; then
        echo ""
        echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${BLUE}Executing: ${test_file}${NC}"
        echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo ""

        # Run test and capture exit code
        if bash "${TEST_PATH}"; then
            TEST_STATUS="PASS"
            ((TOTAL_PASSED++))
        else
            TEST_STATUS="FAIL"
            ((TOTAL_FAILED++))
            OVERALL_EXIT_CODE=1
        fi

        # Parse results from JSON file if it exists
        RESULTS_FILE="${SCRIPT_DIR}/${test_file%.sh}-results.json"
        if [ -f "${RESULTS_FILE}" ]; then
            TEST_PASSED=$(grep -o '"passed":[0-9]*' "${RESULTS_FILE}" | cut -d: -f2)
            TEST_TOTAL=$(grep -o '"total_tests":[0-9]*' "${RESULTS_FILE}" | cut -d: -f2)
            TOTAL_TESTS=$((TOTAL_TESTS + TEST_TOTAL))

            TEST_RESULTS+=("${test_file}:${TEST_PASSED}/${TEST_TOTAL}:${TEST_STATUS}")
        fi

        echo ""
    fi
done

# Generate summary report
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                     Test Execution Summary                      ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo -e "Total Test Cases: ${TOTAL_TESTS}"
echo -e "Passed:          ${GREEN}${TOTAL_PASSED}${NC}"
echo -e "Failed:          ${RED}${TOTAL_FAILED}${NC}"
echo ""

# Display individual test results
echo "Test Results:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
for result in "${TEST_RESULTS[@]}"; do
    TEST_NAME="${result%%:*}"
    REST="${result#*:}"
    COUNTS="${REST%%:*}"
    TEST_STATUS="${REST##*:}"

    if [ "${TEST_STATUS}" = "PASS" ]; then
        STATUS_DISPLAY="${GREEN}✓ PASS${NC}"
    else
        STATUS_DISPLAY="${RED}✗ FAIL${NC}"
    fi

    printf "%-45s %s (%s)\n" "${TEST_NAME}" "${STATUS_DISPLAY}" "${COUNTS}"
done
echo ""

# Calculate and display coverage
if [ ${TOTAL_TESTS} -gt 0 ]; then
    COVERAGE=$((TOTAL_PASSED * 100 / TOTAL_TESTS))
    echo "Overall Coverage: ${COVERAGE}%"
    echo ""
fi

# Final result
echo "╔════════════════════════════════════════════════════════════════╗"
if [ ${OVERALL_EXIT_CODE} -eq 0 ]; then
    echo -e "║                  ${GREEN}ALL TESTS PASSED ✓${NC}                        ║"
else
    echo -e "║                  ${RED}SOME TESTS FAILED ✗${NC}                       ║"
fi
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Write comprehensive summary to JSON
cat > "${SUMMARY_FILE}" << EOF
{
  "story_id": "STORY-107",
  "story_title": "Documentation and User Guide Updates",
  "execution_timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "total_tests": ${TOTAL_TESTS},
  "total_passed": ${TOTAL_PASSED},
  "total_failed": ${TOTAL_FAILED},
  "overall_coverage": "${COVERAGE}%",
  "exit_code": ${OVERALL_EXIT_CODE},
  "test_files": [
EOF

# Add test file details
first=true
for result in "${TEST_RESULTS[@]}"; do
    TEST_NAME="${result%%:*}"
    REST="${result#*:}"
    COUNTS="${REST%%:*}"
    TEST_STATUS="${result##*:}"

    if [ "$first" = false ]; then
        echo "," >> "${SUMMARY_FILE}"
    fi
    first=false

    echo -n "    {\"test_file\": \"${TEST_NAME}\", \"counts\": \"${COUNTS}\", \"status\": \"${TEST_STATUS}\"}" >> "${SUMMARY_FILE}"
done

cat >> "${SUMMARY_FILE}" << EOF

  ],
  "phase": "TDD Red (Tests should be failing - implementation not yet complete)",
  "notes": "This is the RED phase of TDD. Tests are expected to fail because documentation files do not exist yet. Once implementation creates the required documentation files, these tests should pass."
}
EOF

echo "Summary report written to: ${SUMMARY_FILE}"
echo ""

exit ${OVERALL_EXIT_CODE}
