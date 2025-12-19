#!/bin/bash

#################################################################################
# Test AC4: Migration Guide
# Purpose: Verify Migration Guide completeness
#
# Acceptance Criteria:
# - File exists: docs/guides/feedback-migration-guide.md
# - Contains: prerequisites section
# - Contains: step-by-step setup instructions
# - Contains: config file locations
# - Contains: upgrade path from manual to automatic hooks
# - Contains: rollback instructions
#################################################################################


# Test configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
MIGRATION_FILE="${PROJECT_ROOT}/docs/guides/feedback-migration-guide.md"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTS_FILE="${SCRIPT_DIR}/test-ac4-results.json"
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
echo "TEST AC4: Migration Guide"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test 1: File exists
echo "Test 1: Migration guide file exists at ${MIGRATION_FILE}"
((TESTS_TOTAL++))
if [ -f "${MIGRATION_FILE}" ]; then
    echo -e "${GREEN}✓ PASS${NC}: File exists"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: File does not exist"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi
echo ""

# If file doesn't exist, remaining tests will fail
if [ ! -f "${MIGRATION_FILE}" ]; then
    echo -e "${YELLOW}Skipping content tests - file does not exist${NC}"
    echo ""
    # Write results to JSON
    cat > "${RESULTS_FILE}" << EOF
{
  "test_name": "AC4: Migration Guide",
  "total_tests": ${TESTS_TOTAL},
  "passed": ${TESTS_PASSED},
  "failed": ${TESTS_FAILED},
  "exit_code": ${EXIT_CODE},
  "test_results": [
    {
      "test": "File exists",
      "result": "FAIL",
      "message": "Migration guide file not found"
    }
  ]
}
EOF
    exit ${EXIT_CODE}
fi

# Test 2: Contains prerequisites section
echo "Test 2: Contains prerequisites section"
((TESTS_TOTAL++))
if grep -qi "prerequisite\|requirement\|before.*start\|setup.*require" "${MIGRATION_FILE}"; then
    echo -e "${GREEN}✓ PASS${NC}: Prerequisites section found"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Prerequisites section not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi
echo ""

# Test 3: Contains step-by-step setup instructions
echo "Test 3: Contains step-by-step setup instructions"
((TESTS_TOTAL++))
if grep -qi "step\|instruction\|setup\|how.*to\|follow.*these" "${MIGRATION_FILE}"; then
    echo -e "${GREEN}✓ PASS${NC}: Step-by-step setup instructions found"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Step-by-step setup instructions not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi
echo ""

# Test 4: Contains config file locations
echo "Test 4: Contains config file locations"
((TESTS_TOTAL++))
if grep -qi "config.*file\|location\|path\|directory\|\.env\|\.json" "${MIGRATION_FILE}"; then
    echo -e "${GREEN}✓ PASS${NC}: Config file locations documentation found"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Config file locations documentation not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi
echo ""

# Test 5: Contains upgrade path from manual to automatic hooks
echo "Test 5: Contains upgrade path from manual to automatic hooks"
((TESTS_TOTAL++))
if grep -qi "upgrade\|manual.*automatic\|automatic.*hook\|transition\|from.*manual" "${MIGRATION_FILE}"; then
    echo -e "${GREEN}✓ PASS${NC}: Upgrade path documentation found"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Upgrade path documentation not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi
echo ""

# Test 6: Contains rollback instructions
echo "Test 6: Contains rollback instructions"
((TESTS_TOTAL++))
if grep -qi "rollback\|revert\|undo\|go.*back\|previous.*version" "${MIGRATION_FILE}"; then
    echo -e "${GREEN}✓ PASS${NC}: Rollback instructions found"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Rollback instructions not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "SUMMARY: AC4 Migration Guide Tests"
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
  "test_name": "AC4: Migration Guide",
  "total_tests": ${TESTS_TOTAL},
  "passed": ${TESTS_PASSED},
  "failed": ${TESTS_FAILED},
  "exit_code": ${EXIT_CODE},
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

exit ${EXIT_CODE}
