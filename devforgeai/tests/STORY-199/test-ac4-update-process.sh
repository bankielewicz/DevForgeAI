#!/bin/bash
################################################################################
# Test AC#4: Update Process Documentation
#
# Purpose: Verify README.md documents the 7-step update process
#
# Acceptance Criteria:
# - Given the README.md
# - When a maintainer needs to add new patterns
# - Then they can follow a 7-step process:
#   1. Run analysis
#   2. Review candidates
#   3. Validate safety
#   4. Add patterns
#   5. Test
#   6. Commit
#   7. Monitor
#
# Technical Specification:
# - DOC-004: Document 7-step update process
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
RESULTS_FILE="${SCRIPT_DIR}/test-ac4-results.json"

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_TOTAL=0
EXIT_CODE=0

echo ""
echo "=============================================================="
echo "TEST AC#4: Update Process Documentation"
echo "=============================================================="
echo ""

# Pre-check: File exists
if [ ! -f "$TARGET_FILE" ]; then
    echo -e "${RED}FAIL${NC}: README.md not found at ${TARGET_FILE}"
    echo "  Run test-ac1-readme-creation.sh first"
    cat > "${RESULTS_FILE}" << EOF
{
  "test_name": "AC4: Update Process Documentation",
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

# Test 1: DOC-004 - Contains Update Process section header
echo -n "Test 1: DOC-004 - Contains 'Update Process' section... "
((TESTS_TOTAL++))
if grep -qiE "^##+ .*Update.*Process|^##+ .*Adding.*Pattern|^##+ .*How.*to.*Add" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Section header containing 'Update Process' or similar"
    echo "  Actual: Update Process section not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Test 2: Contains numbered steps (at least 7)
echo -n "Test 2: Contains numbered steps (at least 7)... "
((TESTS_TOTAL++))
# Count numbered list items (1., 2., etc.)
STEP_COUNT=$(grep -cE "^[0-9]+\." "$TARGET_FILE" 2>/dev/null || echo "0")
if [ "$STEP_COUNT" -ge 7 ]; then
    echo -e "${GREEN}PASS${NC} (found ${STEP_COUNT} numbered steps)"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: At least 7 numbered steps"
    echo "  Actual: Found ${STEP_COUNT} numbered steps"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Test 3: Step 1 - Run analysis
echo -n "Test 3: Documents 'run analysis' step... "
((TESTS_TOTAL++))
if grep -qiE "run.*analys|analyz|pattern.*analysis|execute.*analysis|STORY-198" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Step for running analysis"
    echo "  Actual: Analysis step not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Test 4: Step 2 - Review candidates
echo -n "Test 4: Documents 'review candidates' step... "
((TESTS_TOTAL++))
if grep -qiE "review.*candidate|candidate.*pattern|evaluate.*result|examine" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Step for reviewing candidates"
    echo "  Actual: Review candidates step not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Test 5: Step 3 - Validate safety
echo -n "Test 5: Documents 'validate safety' step... "
((TESTS_TOTAL++))
if grep -qiE "validat.*safe|safety.*check|verify.*safe|assess.*risk|safe.*criteria" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Step for validating safety"
    echo "  Actual: Validate safety step not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Test 6: Step 4 - Add patterns
echo -n "Test 6: Documents 'add patterns' step... "
((TESTS_TOTAL++))
if grep -qiE "add.*pattern|insert.*pattern|update.*hook|modify.*pattern|implement.*pattern" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Step for adding patterns"
    echo "  Actual: Add patterns step not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Test 7: Step 5 - Test
echo -n "Test 7: Documents 'test' step... "
((TESTS_TOTAL++))
if grep -qiE "test.*pattern|verify.*work|run.*test|validate.*behavior|manual.*test" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Step for testing"
    echo "  Actual: Test step not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Test 8: Step 6 - Commit
echo -n "Test 8: Documents 'commit' step... "
((TESTS_TOTAL++))
if grep -qiE "commit.*change|git commit|version.*control|save.*change|document.*change" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Step for committing changes"
    echo "  Actual: Commit step not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Test 9: Step 7 - Monitor
echo -n "Test 9: Documents 'monitor' step... "
((TESTS_TOTAL++))
if grep -qiE "monitor|observe|watch.*behavior|track.*result|follow.*up|verify.*production" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${RED}FAIL${NC}"
    echo "  Expected: Step for monitoring"
    echo "  Actual: Monitor step not found"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi

# Test 10: Contains reference to analysis tool (STORY-198)
echo -n "Test 10: References analysis tool (STORY-198)... "
((TESTS_TOTAL++))
if grep -qE "STORY-198|command.*pattern.*analysis|analyze.*command|pattern.*analyz" "$TARGET_FILE" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((TESTS_PASSED++))
else
    echo -e "${YELLOW}WARN${NC}"
    echo "  Expected: Reference to STORY-198 analysis tool"
    echo "  Actual: No explicit STORY-198 reference found"
    # Don't fail - this is a SHOULD, not MUST
    ((TESTS_PASSED++))
fi

# Summary
echo ""
echo "=============================================================="
echo "SUMMARY: AC#4 Update Process Documentation Tests"
echo "=============================================================="
echo -e "Total Tests:  ${TESTS_TOTAL}"
echo -e "Passed:       ${GREEN}${TESTS_PASSED}${NC}"
echo -e "Failed:       ${RED}${TESTS_FAILED}${NC}"
echo ""

if [ ${EXIT_CODE} -eq 0 ]; then
    echo -e "${GREEN}ALL AC#4 TESTS PASSED${NC}"
else
    echo -e "${RED}SOME AC#4 TESTS FAILED${NC}"
fi
echo ""

# Write results to JSON
cat > "${RESULTS_FILE}" << EOF
{
  "test_name": "AC4: Update Process Documentation",
  "total_tests": ${TESTS_TOTAL},
  "passed": ${TESTS_PASSED},
  "failed": ${TESTS_FAILED},
  "exit_code": ${EXIT_CODE},
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

exit ${EXIT_CODE}
