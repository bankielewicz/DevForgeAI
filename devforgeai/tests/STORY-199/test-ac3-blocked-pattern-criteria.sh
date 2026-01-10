#!/bin/bash
################################################################################
# Test AC#3: Blocked Pattern Criteria
#
# Purpose: Verify README.md documents blocked pattern criteria
#
# Acceptance Criteria:
# - Given the README.md
# - When a maintainer reads the documentation
# - Then they understand which commands must remain blocked
#   (rm -rf, sudo, git push, npm publish, curl/wget)
#
# Technical Specification:
# - DOC-003: Document blocked pattern criteria
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
RESULTS_FILE="${SCRIPT_DIR}/test-ac3-results.json"

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_TOTAL=0
EXIT_CODE=0

echo ""
echo "=============================================================="
echo "TEST AC#3: Blocked Pattern Criteria"
echo "=============================================================="
echo ""

# Pre-check: File exists
if [ ! -f "$TARGET_FILE" ]; then
    echo -e "${RED}FAIL${NC}: README.md not found at ${TARGET_FILE}"
    echo "  Run test-ac1-readme-creation.sh first"
    cat > "${RESULTS_FILE}" << EOF
{
  "test_name": "AC3: Blocked Pattern Criteria",
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

# Test 1: DOC-003 - Contains Blocked Patterns section header
echo -n "Test 1: DOC-003 - Contains 'Blocked Patterns' section... "
((TESTS_TOTAL++))
if grep -qiE "^##+ .*Block.*Pattern|^##+ .*Never.*Approve|^##+ .*Dangerous" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Section header containing 'Blocked Patterns' or similar"
    echo "  Actual: Blocked Patterns section not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Test 2: Documents rm -rf as blocked
echo -n "Test 2: Documents 'rm -rf' as blocked command... "
((TESTS_TOTAL++))
if grep -qE "rm -rf|rm.*-rf|force.*delete|recursive.*remove" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of 'rm -rf' as blocked"
    echo "  Actual: rm -rf not found in blocked patterns"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Test 3: Documents sudo as blocked
echo -n "Test 3: Documents 'sudo' as blocked command... "
((TESTS_TOTAL++))
if grep -qiE "\bsudo\b|superuser|root.*access|elevated.*privilege" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of 'sudo' as blocked"
    echo "  Actual: sudo not found in blocked patterns"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Test 4: Documents git push as blocked
echo -n "Test 4: Documents 'git push' as blocked command... "
((TESTS_TOTAL++))
if grep -qE "git push|push.*remote|force.*push" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of 'git push' as blocked"
    echo "  Actual: git push not found in blocked patterns"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Test 5: Documents npm publish as blocked
echo -n "Test 5: Documents 'npm publish' as blocked command... "
((TESTS_TOTAL++))
if grep -qE "npm publish|publish.*package|package.*registry" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of 'npm publish' as blocked"
    echo "  Actual: npm publish not found in blocked patterns"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Test 6: Documents curl/wget as blocked (network operations)
echo -n "Test 6: Documents 'curl/wget' as blocked commands... "
((TESTS_TOTAL++))
if grep -qiE "\bcurl\b|\bwget\b|network.*download|external.*fetch|http.*request" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of 'curl/wget' as blocked"
    echo "  Actual: curl/wget not found in blocked patterns"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Test 7: Contains explanation of why patterns are blocked
echo -n "Test 7: Contains explanation of why patterns are blocked... "
((TESTS_TOTAL++))
if grep -qiE "dangerous|destructive|irreversible|security|risk|unsafe|never.*approve" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Explanation of risks/dangers"
    echo "  Actual: No risk/danger explanation found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Test 8: Contains at least 5 blocked command examples
echo -n "Test 8: Contains at least 5 blocked command examples... "
((TESTS_TOTAL++))
# Count unique blocked patterns mentioned
BLOCKED_COUNT=0
grep -qiE "rm -rf" "$TARGET_FILE" 2>/dev/null && ((BLOCKED_COUNT++)) || true
grep -qiE "\bsudo\b" "$TARGET_FILE" 2>/dev/null && ((BLOCKED_COUNT++)) || true
grep -qiE "git push" "$TARGET_FILE" 2>/dev/null && ((BLOCKED_COUNT++)) || true
grep -qiE "npm publish" "$TARGET_FILE" 2>/dev/null && ((BLOCKED_COUNT++)) || true
grep -qiE "\bcurl\b" "$TARGET_FILE" 2>/dev/null && ((BLOCKED_COUNT++)) || true
grep -qiE "\bwget\b" "$TARGET_FILE" 2>/dev/null && ((BLOCKED_COUNT++)) || true
grep -qiE "chmod" "$TARGET_FILE" 2>/dev/null && ((BLOCKED_COUNT++)) || true
grep -qiE "git reset.*--hard" "$TARGET_FILE" 2>/dev/null && ((BLOCKED_COUNT++)) || true

if [ "$BLOCKED_COUNT" -ge 5 ]; then
    echo -e "${GREEN}PASS${NC} (found ${BLOCKED_COUNT} blocked patterns)"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: At least 5 blocked patterns documented"
    echo "  Actual: Found ${BLOCKED_COUNT} blocked patterns"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Summary
echo ""
echo "=============================================================="
echo "SUMMARY: AC#3 Blocked Pattern Criteria Tests"
echo "=============================================================="
echo -e "Total Tests:  ${TESTS_TOTAL}"
echo -e "Passed:       ${GREEN}${TESTS_PASSED}${NC}"
echo -e "Failed:       ${RED}${TESTS_FAILED}${NC}"
echo ""

if [ ${EXIT_CODE} -eq 0 ]; then
    echo -e "${GREEN}ALL AC#3 TESTS PASSED${NC}"
else
    echo -e "${RED}SOME AC#3 TESTS FAILED${NC}"
fi
echo ""

# Write results to JSON
cat > "${RESULTS_FILE}" << EOF
{
  "test_name": "AC3: Blocked Pattern Criteria",
  "total_tests": ${TESTS_TOTAL},
  "passed": ${TESTS_PASSED},
  "failed": ${TESTS_FAILED},
  "exit_code": ${EXIT_CODE},
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

exit ${EXIT_CODE}
