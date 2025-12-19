#!/bin/bash

#################################################################################
# Test AC1: User Guide
# Purpose: Verify User Guide documentation completeness
#
# Acceptance Criteria:
# - File exists: docs/guides/feedback-system-user-guide.md
# - Contains: enable/disable hooks documentation
# - Contains: configuration options (trigger modes, conversation settings)
# - Contains: common use cases examples
# - Contains: feedback conversation flow explanation
#################################################################################

# Test configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
USER_GUIDE_FILE="${PROJECT_ROOT}/docs/guides/feedback-system-user-guide.md"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTS_FILE="${SCRIPT_DIR}/test-ac1-results.json"
EXIT_CODE=0

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# JSON results tracking
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_TOTAL=0

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST AC1: User Guide"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test 1: File exists
echo "Test 1: User Guide file exists at ${USER_GUIDE_FILE}"
((TESTS_TOTAL++))
if [ -f "${USER_GUIDE_FILE}" ]; then
    echo -e "${GREEN}✓ PASS${NC}: File exists"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: File does not exist"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi
echo ""

# If file doesn't exist, remaining tests will fail
if [ ! -f "${USER_GUIDE_FILE}" ]; then
    echo -e "${YELLOW}Skipping content tests - file does not exist${NC}"
    echo ""
    # Write results to JSON
    cat > "${RESULTS_FILE}" << EOF
{
  "test_name": "AC1: User Guide",
  "total_tests": ${TESTS_TOTAL},
  "passed": ${TESTS_PASSED},
  "failed": ${TESTS_FAILED},
  "exit_code": ${EXIT_CODE},
  "test_results": [
    {
      "test": "File exists",
      "result": "FAIL",
      "message": "User guide file not found"
    }
  ]
}
EOF
    exit ${EXIT_CODE}
fi

# Test 2: Contains enable/disable hooks documentation
echo "Test 2: Contains enable/disable hooks documentation"
((TESTS_TOTAL++))
if grep -qi "enable.*hook\|disable.*hook\|turning.*on\|turning.*off" "${USER_GUIDE_FILE}"; then
    echo -e "${GREEN}✓ PASS${NC}: Enable/disable hooks documentation found"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Enable/disable hooks documentation not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi
echo ""

# Test 3: Contains configuration options documentation
echo "Test 3: Contains configuration options (trigger modes, conversation settings)"
((TESTS_TOTAL++))
HAS_CONFIG=0
if grep -qi "config\|trigger.*mode\|conversation.*setting\|frequency\|skip.*behavior" "${USER_GUIDE_FILE}"; then
    HAS_CONFIG=1
fi
if [ $HAS_CONFIG -eq 1 ]; then
    echo -e "${GREEN}✓ PASS${NC}: Configuration options documentation found"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Configuration options documentation not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi
echo ""

# Test 4: Contains common use cases examples
echo "Test 4: Contains common use cases examples"
((TESTS_TOTAL++))
if grep -qi "example\|use case\|scenario\|how to" "${USER_GUIDE_FILE}"; then
    echo -e "${GREEN}✓ PASS${NC}: Common use cases examples found"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Common use cases examples not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi
echo ""

# Test 5: Contains feedback conversation flow explanation
echo "Test 5: Contains feedback conversation flow explanation"
((TESTS_TOTAL++))
if grep -qi "conversation.*flow\|feedback.*flow\|how.*feedback\|feedback.*process" "${USER_GUIDE_FILE}"; then
    echo -e "${GREEN}✓ PASS${NC}: Feedback conversation flow explanation found"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Feedback conversation flow explanation not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "SUMMARY: AC1 User Guide Tests"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "Total Tests:  ${TESTS_TOTAL}"
echo -e "Passed:       ${GREEN}${TESTS_PASSED}${NC}"
echo -e "Failed:       ${RED}${TESTS_FAILED}${NC}"
echo ""
if [ ${EXIT_CODE} -eq 0 ]; then
    echo -e "${GREEN}✓ ALL TESTS PASSED${NC}"
else
    echo -e "${RED}✗ SOME TESTS FAILED${NC}"
fi
echo ""

# Write results to JSON
cat > "${RESULTS_FILE}" << EOF
{
  "test_name": "AC1: User Guide",
  "total_tests": ${TESTS_TOTAL},
  "passed": ${TESTS_PASSED},
  "failed": ${TESTS_FAILED},
  "exit_code": ${EXIT_CODE},
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

exit ${EXIT_CODE}
