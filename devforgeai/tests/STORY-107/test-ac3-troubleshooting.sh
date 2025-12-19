#!/bin/bash

#################################################################################
# Test AC3: Troubleshooting Guide
# Purpose: Verify Troubleshooting Guide completeness
#
# Acceptance Criteria:
# - File exists: docs/guides/feedback-troubleshooting.md
# - Contains: common issues section
# - Contains: how to check if hooks are enabled
# - Contains: hook invocation logs documentation
# - Contains: FAQ section (minimum 10 entries)
#################################################################################


# Test configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TROUBLESHOOT_FILE="${PROJECT_ROOT}/docs/guides/feedback-troubleshooting.md"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTS_FILE="${SCRIPT_DIR}/test-ac3-results.json"
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
echo "TEST AC3: Troubleshooting Guide"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test 1: File exists
echo "Test 1: Troubleshooting guide file exists at ${TROUBLESHOOT_FILE}"
((TESTS_TOTAL++))
if [ -f "${TROUBLESHOOT_FILE}" ]; then
    echo -e "${GREEN}✓ PASS${NC}: File exists"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: File does not exist"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi
echo ""

# If file doesn't exist, remaining tests will fail
if [ ! -f "${TROUBLESHOOT_FILE}" ]; then
    echo -e "${YELLOW}Skipping content tests - file does not exist${NC}"
    echo ""
    # Write results to JSON
    cat > "${RESULTS_FILE}" << EOF
{
  "test_name": "AC3: Troubleshooting Guide",
  "total_tests": ${TESTS_TOTAL},
  "passed": ${TESTS_PASSED},
  "failed": ${TESTS_FAILED},
  "exit_code": ${EXIT_CODE},
  "test_results": [
    {
      "test": "File exists",
      "result": "FAIL",
      "message": "Troubleshooting guide file not found"
    }
  ]
}
EOF
    exit ${EXIT_CODE}
fi

# Test 2: Contains common issues section
echo "Test 2: Contains common issues section"
((TESTS_TOTAL++))
if grep -qi "common.*issue\|issue.*section\|problem\|troubleshoot" "${TROUBLESHOOT_FILE}"; then
    echo -e "${GREEN}✓ PASS${NC}: Common issues section found"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Common issues section not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi
echo ""

# Test 3: Contains how to check if hooks are enabled
echo "Test 3: Contains how to check if hooks are enabled"
((TESTS_TOTAL++))
if grep -qi "check.*hook\|enabled\|verify.*hook\|hook.*status\|is.*hook" "${TROUBLESHOOT_FILE}"; then
    echo -e "${GREEN}✓ PASS${NC}: Hook enable check documentation found"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Hook enable check documentation not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi
echo ""

# Test 4: Contains hook invocation logs documentation
echo "Test 4: Contains hook invocation logs documentation"
((TESTS_TOTAL++))
if grep -qi "log\|invocation.*log\|debug\|view.*log\|check.*log" "${TROUBLESHOOT_FILE}"; then
    echo -e "${GREEN}✓ PASS${NC}: Hook invocation logs documentation found"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Hook invocation logs documentation not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi
echo ""

# Test 5: Contains FAQ section with minimum 10 entries
echo "Test 5: Contains FAQ section (minimum 10 entries)"
((TESTS_TOTAL++))

# Check if FAQ section exists
if grep -qi "^##.*FAQ\|^#.*FAQ\|frequently.*asked" "${TROUBLESHOOT_FILE}"; then
    # Count FAQ entries (look for Q/A patterns, dashes, or numbered items under FAQ)
    FAQ_COUNT=$(grep -E "^[-*] |^[0-9]+\.|^Q:|^\*\*Q" "${TROUBLESHOOT_FILE}" | wc -l)

    if [ "${FAQ_COUNT}" -ge 10 ]; then
        echo -e "${GREEN}✓ PASS${NC}: FAQ section found with ${FAQ_COUNT} entries"
        ((TESTS_PASSED++))
    else
        echo -e "${YELLOW}⚠ WARNING${NC}: FAQ section found but only ${FAQ_COUNT} entries (need ≥10)"
        ((TESTS_FAILED++))
        EXIT_CODE=1
    fi
else
    echo -e "${RED}✗ FAIL${NC}: FAQ section not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "SUMMARY: AC3 Troubleshooting Guide Tests"
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
  "test_name": "AC3: Troubleshooting Guide",
  "total_tests": ${TESTS_TOTAL},
  "passed": ${TESTS_PASSED},
  "failed": ${TESTS_FAILED},
  "exit_code": ${EXIT_CODE},
  "faq_entries_found": "${FAQ_COUNT}",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

exit ${EXIT_CODE}
