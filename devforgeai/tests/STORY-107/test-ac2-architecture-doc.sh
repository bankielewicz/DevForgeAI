#!/bin/bash

#################################################################################
# Test AC2: Architecture Documentation
# Purpose: Verify Architecture Documentation completeness
#
# Acceptance Criteria:
# - File exists: docs/architecture/hook-system-design.md
# - Contains: Mermaid diagram (```mermaid block)
# - Contains: hook invocation flow diagram
# - Contains: context extraction architecture
# - Contains: integration points documentation
# - Contains: data flow documentation
#################################################################################


# Test configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
ARCH_DOC_FILE="${PROJECT_ROOT}/docs/architecture/hook-system-design.md"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTS_FILE="${SCRIPT_DIR}/test-ac2-results.json"
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
echo "TEST AC2: Architecture Documentation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test 1: File exists
echo "Test 1: Architecture doc file exists at ${ARCH_DOC_FILE}"
((TESTS_TOTAL++))
if [ -f "${ARCH_DOC_FILE}" ]; then
    echo -e "${GREEN}✓ PASS${NC}: File exists"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: File does not exist"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi
echo ""

# If file doesn't exist, remaining tests will fail
if [ ! -f "${ARCH_DOC_FILE}" ]; then
    echo -e "${YELLOW}Skipping content tests - file does not exist${NC}"
    echo ""
    # Write results to JSON
    cat > "${RESULTS_FILE}" << EOF
{
  "test_name": "AC2: Architecture Documentation",
  "total_tests": ${TESTS_TOTAL},
  "passed": ${TESTS_PASSED},
  "failed": ${TESTS_FAILED},
  "exit_code": ${EXIT_CODE},
  "test_results": [
    {
      "test": "File exists",
      "result": "FAIL",
      "message": "Architecture doc file not found"
    }
  ]
}
EOF
    exit ${EXIT_CODE}
fi

# Test 2: Contains Mermaid diagram code block
echo "Test 2: Contains Mermaid diagram (\`\`\`mermaid block)"
((TESTS_TOTAL++))
if grep -q '```mermaid' "${ARCH_DOC_FILE}"; then
    echo -e "${GREEN}✓ PASS${NC}: Mermaid diagram code block found"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Mermaid diagram code block not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi
echo ""

# Test 3: Contains hook invocation flow documentation
echo "Test 3: Contains hook invocation flow diagram/documentation"
((TESTS_TOTAL++))
if grep -qi "hook.*flow\|invocation.*flow\|hook.*sequence\|flow.*diagram" "${ARCH_DOC_FILE}"; then
    echo -e "${GREEN}✓ PASS${NC}: Hook invocation flow documentation found"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Hook invocation flow documentation not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi
echo ""

# Test 4: Contains context extraction architecture documentation
echo "Test 4: Contains context extraction architecture documentation"
((TESTS_TOTAL++))
if grep -qi "context.*extract\|extraction.*archit\|extracting.*context" "${ARCH_DOC_FILE}"; then
    echo -e "${GREEN}✓ PASS${NC}: Context extraction architecture documentation found"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Context extraction architecture documentation not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi
echo ""

# Test 5: Contains integration points documentation
echo "Test 5: Contains integration points documentation"
((TESTS_TOTAL++))
if grep -qi "integration.*point\|integrate.*with\|interact.*with\|connect" "${ARCH_DOC_FILE}"; then
    echo -e "${GREEN}✓ PASS${NC}: Integration points documentation found"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Integration points documentation not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi
echo ""

# Test 6: Contains data flow documentation
echo "Test 6: Contains data flow documentation"
((TESTS_TOTAL++))
if grep -qi "data.*flow\|flow.*data\|data.*path\|operation.*feedback\|feedback.*storage" "${ARCH_DOC_FILE}"; then
    echo -e "${GREEN}✓ PASS${NC}: Data flow documentation found"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: Data flow documentation not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "SUMMARY: AC2 Architecture Documentation Tests"
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
  "test_name": "AC2: Architecture Documentation",
  "total_tests": ${TESTS_TOTAL},
  "passed": ${TESTS_PASSED},
  "failed": ${TESTS_FAILED},
  "exit_code": ${EXIT_CODE},
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

exit ${EXIT_CODE}
