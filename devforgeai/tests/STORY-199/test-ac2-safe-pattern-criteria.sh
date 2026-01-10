#!/bin/bash
################################################################################
# Test AC#2: Safe Pattern Criteria
#
# Purpose: Verify README.md documents safe pattern selection criteria
#
# Acceptance Criteria:
# - Given the README.md
# - When a maintainer reads the documentation
# - Then they understand which commands are safe to auto-approve
#   (read-only, framework ops, navigation, non-destructive)
#
# Technical Specification:
# - DOC-002: Document safe pattern selection criteria
################################################################################

set -uo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
TARGET_FILE="${PROJECT_ROOT}/.claude/hooks/README.md"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTS_FILE="${SCRIPT_DIR}/test-ac2-results.json"

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_TOTAL=0
EXIT_CODE=0

echo ""
echo "=============================================================="
echo "TEST AC#2: Safe Pattern Criteria"
echo "=============================================================="
echo ""

# Pre-check: File exists
if [ ! -f "$TARGET_FILE" ]; then
    echo -e "${RED}FAIL${NC}: README.md not found at ${TARGET_FILE}"
    echo "  Run test-ac1-readme-creation.sh first"
    cat > "${RESULTS_FILE}" << EOF
{
  "test_name": "AC2: Safe Pattern Criteria",
  "total_tests": 1,
  "passed": 0,
  "failed": 1,
  "exit_code": 1,
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "test_results": [{"test": "Pre-check: File exists", "result": "FAIL"}]
}
EOF
    exit 1
fi

# Test 1: DOC-002 - Contains Safe Patterns section header
echo -n "Test 1: DOC-002 - Contains 'Safe Patterns' section... "
((TESTS_TOTAL++))
if grep -qiE "^##+ .*Safe.*Pattern" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Section header containing 'Safe Patterns'"
    echo "  Actual: Safe Patterns section not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Test 2: Documents read-only commands
echo -n "Test 2: Documents read-only commands as safe... "
((TESTS_TOTAL++))
if grep -qiE "read[-_]?only|read operations" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of 'read-only' as safe criteria"
    echo "  Actual: Read-only criteria not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Test 3: Documents framework operations
echo -n "Test 3: Documents framework operations as safe... "
((TESTS_TOTAL++))
if grep -qiE "framework|devforgeai|framework.op" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of 'framework operations' as safe"
    echo "  Actual: Framework operations criteria not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Test 4: Documents navigation commands
echo -n "Test 4: Documents navigation commands as safe... "
((TESTS_TOTAL++))
if grep -qiE "navigation|navigate|cd |pwd|ls " "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of 'navigation' commands as safe"
    echo "  Actual: Navigation criteria not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Test 5: Documents non-destructive operations
echo -n "Test 5: Documents non-destructive operations as safe... "
((TESTS_TOTAL++))
if grep -qiE "non[-_]?destructive|no.*(data|file|system).*loss|safe.*operation|not.*modify" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of 'non-destructive' as safe criteria"
    echo "  Actual: Non-destructive criteria not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Test 6: Contains examples of safe commands
echo -n "Test 6: Contains examples of safe commands... "
((TESTS_TOTAL++))
# Look for common safe command examples like git status, ls, pwd, cat, etc.
if grep -qE "(git status|git log|git diff|git branch|ls |pwd|cat |head |tail |grep )" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Examples of safe commands (git status, ls, pwd, etc.)"
    echo "  Actual: No safe command examples found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Test 7: Contains selection criteria explanation
echo -n "Test 7: Contains selection criteria explanation... "
((TESTS_TOTAL++))
if grep -qiE "criteria|why.*safe|rationale|reason|principle" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Explanation of selection criteria or rationale"
    echo "  Actual: No selection criteria explanation found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Summary
echo ""
echo "=============================================================="
echo "SUMMARY: AC#2 Safe Pattern Criteria Tests"
echo "=============================================================="
echo -e "Total Tests:  ${TESTS_TOTAL}"
echo -e "Passed:       ${GREEN}${TESTS_PASSED}${NC}"
echo -e "Failed:       ${RED}${TESTS_FAILED}${NC}"
echo ""

if [ ${EXIT_CODE} -eq 0 ]; then
    echo -e "${GREEN}ALL AC#2 TESTS PASSED${NC}"
else
    echo -e "${RED}SOME AC#2 TESTS FAILED${NC}"
fi
echo ""

# Write results to JSON
cat > "${RESULTS_FILE}" << EOF
{
  "test_name": "AC2: Safe Pattern Criteria",
  "total_tests": ${TESTS_TOTAL},
  "passed": ${TESTS_PASSED},
  "failed": ${TESTS_FAILED},
  "exit_code": ${EXIT_CODE},
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

exit ${EXIT_CODE}
