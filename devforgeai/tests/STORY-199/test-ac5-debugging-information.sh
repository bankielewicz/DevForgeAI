#!/bin/bash
################################################################################
# Test AC#5: Debugging Information
#
# Purpose: Verify README.md documents debugging resources
#
# Acceptance Criteria:
# - Given the README.md
# - When a maintainer needs to debug the hook
# - Then they know where to find logs and analysis tools
#
# Technical Specification:
# - DOC-005: Document debugging resources (log locations, tools)
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
RESULTS_FILE="${SCRIPT_DIR}/test-ac5-results.json"

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_TOTAL=0
EXIT_CODE=0

echo ""
echo "=============================================================="
echo "TEST AC#5: Debugging Information"
echo "=============================================================="
echo ""

# Pre-check: File exists
if [ ! -f "$TARGET_FILE" ]; then
    echo -e "${RED}FAIL${NC}: README.md not found at ${TARGET_FILE}"
    echo "  Run test-ac1-readme-creation.sh first"
    cat > "${RESULTS_FILE}" << EOF
{
  "test_name": "AC5: Debugging Information",
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

# Test 1: DOC-005 - Contains Debugging section header
echo -n "Test 1: DOC-005 - Contains 'Debugging' section... "
((TESTS_TOTAL++))
if grep -qiE "^##+ .*Debug|^##+ .*Troubleshoot|^##+ .*Diagnos" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Section header containing 'Debugging' or 'Troubleshooting'"
    echo "  Actual: Debugging section not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Test 2: Documents log locations
echo -n "Test 2: Documents log locations... "
((TESTS_TOTAL++))
if grep -qiE "log.*location|log.*file|\.log\b|log.*path|where.*log|find.*log" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of log locations"
    echo "  Actual: Log location documentation not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Test 3: References analysis tool (STORY-198)
echo -n "Test 3: References analysis tool (STORY-198)... "
((TESTS_TOTAL++))
if grep -qE "STORY-198|analysis.*tool|command.*pattern.*analys|pattern.*analyz" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Reference to STORY-198 analysis tool"
    echo "  Actual: Analysis tool reference not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Test 4: Contains debugging commands or procedures
echo -n "Test 4: Contains debugging commands or procedures... "
((TESTS_TOTAL++))
if grep -qiE "debug.*command|check.*log|view.*log|tail.*log|inspect|diagnose|troubleshoot" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Debugging commands or procedures"
    echo "  Actual: No debugging procedures found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Test 5: Documents common issues or error scenarios
echo -n "Test 5: Documents common issues or error scenarios... "
((TESTS_TOTAL++))
if grep -qiE "common.*issue|error|problem|fail|not.*work|issue|troubleshoot" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Documentation of common issues"
    echo "  Actual: No common issues documented"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Test 6: Contains hook file location reference
echo -n "Test 6: Contains hook file location reference... "
((TESTS_TOTAL++))
if grep -qE "\.claude/hooks|hooks.*directory|hook.*location|pre-tool-use" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Reference to .claude/hooks location"
    echo "  Actual: Hook location reference not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Test 7: Contains enable/disable debugging information
echo -n "Test 7: Contains enable/disable debugging guidance... "
((TESTS_TOTAL++))
if grep -qiE "enable.*debug|disable.*hook|turn.*off|bypass|skip.*hook|verbose" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${YELLOW}WARN${NC}"
    echo "  Expected: Guidance on enabling/disabling debug mode"
    echo "  Actual: Enable/disable guidance not found (non-blocking)"
    # Don't fail - this is nice-to-have
    ((TESTS_PASSED++))
fi

# Summary
echo ""
echo "=============================================================="
echo "SUMMARY: AC#5 Debugging Information Tests"
echo "=============================================================="
echo -e "Total Tests:  ${TESTS_TOTAL}"
echo -e "Passed:       ${GREEN}${TESTS_PASSED}${NC}"
echo -e "Failed:       ${RED}${TESTS_FAILED}${NC}"
echo ""

if [ ${EXIT_CODE} -eq 0 ]; then
    echo -e "${GREEN}ALL AC#5 TESTS PASSED${NC}"
else
    echo -e "${RED}SOME AC#5 TESTS FAILED${NC}"
fi
echo ""

# Write results to JSON
cat > "${RESULTS_FILE}" << EOF
{
  "test_name": "AC5: Debugging Information",
  "total_tests": ${TESTS_TOTAL},
  "passed": ${TESTS_PASSED},
  "failed": ${TESTS_FAILED},
  "exit_code": ${EXIT_CODE},
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

exit ${EXIT_CODE}
