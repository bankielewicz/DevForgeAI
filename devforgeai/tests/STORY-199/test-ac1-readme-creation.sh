#!/bin/bash
################################################################################
# Test AC#1: README Creation
#
# Purpose: Verify README.md file exists at .claude/hooks/README.md
#
# Acceptance Criteria:
# - Given the `.claude/hooks/` directory
# - When documentation is created
# - Then a README.md file exists with complete hook documentation
#
# Technical Specification:
# - DOC-001: Purpose section exists
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
RESULTS_FILE="${SCRIPT_DIR}/test-ac1-results.json"

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_TOTAL=0
EXIT_CODE=0

echo ""
echo "=============================================================="
echo "TEST AC#1: README Creation"
echo "=============================================================="
echo ""

# Test 1: README.md file exists
echo -n "Test 1: README.md exists at .claude/hooks/README.md... "
((TESTS_TOTAL++))
if [ -f "$TARGET_FILE" ]; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: File exists at ${TARGET_FILE}"
    echo "  Actual: File not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Skip remaining tests if file doesn't exist
if [ ! -f "$TARGET_FILE" ]; then
    echo ""
    echo -e "${YELLOW}Skipping content tests - README.md does not exist${NC}"
    echo ""

    # Write results to JSON
    cat > "${RESULTS_FILE}" << EOF
{
  "test_name": "AC1: README Creation",
  "total_tests": ${TESTS_TOTAL},
  "passed": ${TESTS_PASSED},
  "failed": ${TESTS_FAILED},
  "exit_code": ${EXIT_CODE},
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "test_results": [
    {
      "test": "README.md file exists",
      "result": "FAIL",
      "message": "File not found at .claude/hooks/README.md"
    }
  ]
}
EOF
    exit ${EXIT_CODE}
fi

# Test 2: File is not empty
echo -n "Test 2: README.md is not empty... "
((TESTS_TOTAL++))
if [ -s "$TARGET_FILE" ]; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: File contains content"
    echo "  Actual: File is empty"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Test 3: Contains main title header
echo -n "Test 3: Contains main title header (# DevForgeAI or # Pre-Tool-Use Hook)... "
((TESTS_TOTAL++))
if grep -qE "^# (DevForgeAI|Pre-Tool-Use Hook)" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: H1 header with 'DevForgeAI' or 'Pre-Tool-Use Hook'"
    echo "  Actual: No matching H1 header found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Test 4: DOC-001 - Contains Purpose section
echo -n "Test 4: DOC-001 - Contains '## Purpose' section... "
((TESTS_TOTAL++))
if grep -qE "^## Purpose" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Section header '## Purpose' exists"
    echo "  Actual: Purpose section not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Test 5: Purpose section has content
echo -n "Test 5: Purpose section contains meaningful content... "
((TESTS_TOTAL++))
if grep -qiE "(pre-tool-use|hook|auto-approve|workflow|commands|bash)" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Purpose section contains hook-related terminology"
    echo "  Actual: No hook-related content found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Summary
echo ""
echo "=============================================================="
echo "SUMMARY: AC#1 README Creation Tests"
echo "=============================================================="
echo -e "Total Tests:  ${TESTS_TOTAL}"
echo -e "Passed:       ${GREEN}${TESTS_PASSED}${NC}"
echo -e "Failed:       ${RED}${TESTS_FAILED}${NC}"
echo ""

if [ ${EXIT_CODE} -eq 0 ]; then
    echo -e "${GREEN}ALL AC#1 TESTS PASSED${NC}"
else
    echo -e "${RED}SOME AC#1 TESTS FAILED${NC}"
fi
echo ""

# Write results to JSON
cat > "${RESULTS_FILE}" << EOF
{
  "test_name": "AC1: README Creation",
  "total_tests": ${TESTS_TOTAL},
  "passed": ${TESTS_PASSED},
  "failed": ${TESTS_FAILED},
  "exit_code": ${EXIT_CODE},
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

exit ${EXIT_CODE}
