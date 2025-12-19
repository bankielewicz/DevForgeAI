#!/bin/bash

#################################################################################
# Test AC5: Inline Code Documentation
# Purpose: Verify inline code documentation completeness
#
# Acceptance Criteria:
# - File exists: .claude/skills/devforgeai-feedback/README.md
# - Contains: quick start section
# - Contains: feature overview
# - Python docstrings exist in src/context_extraction.py public functions
# - Python docstrings exist in adaptive_questioning_engine.py public methods
#################################################################################


# Test configuration
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
SKILL_README="${PROJECT_ROOT}/.claude/skills/devforgeai-feedback/README.md"
CONTEXT_EXTRACTION="${PROJECT_ROOT}/src/context_extraction.py"
ADAPTIVE_QUESTIONING="${PROJECT_ROOT}/.claude/scripts/devforgeai_cli/feedback/adaptive_questioning_engine.py"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESULTS_FILE="${SCRIPT_DIR}/test-ac5-results.json"
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
echo "TEST AC5: Inline Code Documentation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test 1: Skill README exists
echo "Test 1: Skill README exists at ${SKILL_README}"
((TESTS_TOTAL++))
if [ -f "${SKILL_README}" ]; then
    echo -e "${GREEN}✓ PASS${NC}: File exists"
    ((TESTS_PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}: File does not exist"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi
echo ""

# Test 2: README contains quick start section
echo "Test 2: Skill README contains quick start section"
((TESTS_TOTAL++))
if [ -f "${SKILL_README}" ]; then
    if grep -qi "quick.*start\|getting.*start\|start.*here" "${SKILL_README}"; then
        echo -e "${GREEN}✓ PASS${NC}: Quick start section found"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC}: Quick start section not found"
        ((TESTS_FAILED++))
        EXIT_CODE=1
    fi
else
    echo -e "${YELLOW}⊘ SKIP${NC}: README does not exist"
fi
echo ""

# Test 3: README contains feature overview
echo "Test 3: Skill README contains feature overview"
((TESTS_TOTAL++))
if [ -f "${SKILL_README}" ]; then
    if grep -qi "feature\|overview\|capability\|what.*is\|introduction" "${SKILL_README}"; then
        echo -e "${GREEN}✓ PASS${NC}: Feature overview found"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC}: Feature overview not found"
        ((TESTS_FAILED++))
        EXIT_CODE=1
    fi
else
    echo -e "${YELLOW}⊘ SKIP${NC}: README does not exist"
fi
echo ""

# Test 4: context_extraction.py has docstrings for public functions
echo "Test 4: context_extraction.py has docstrings for public functions"
((TESTS_TOTAL++))
if [ -f "${CONTEXT_EXTRACTION}" ]; then
    # Count public functions (def name() not starting with _)
    PUBLIC_FUNCTIONS=$(grep -c "^def [^_]" "${CONTEXT_EXTRACTION}" || echo "0")

    # Count docstrings (triple quotes or triple double quotes)
    DOCSTRINGS=$(grep -c '"""' "${CONTEXT_EXTRACTION}" || echo "0")

    if [ "${PUBLIC_FUNCTIONS}" -gt 0 ] && [ "${DOCSTRINGS}" -gt 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}: Found ${PUBLIC_FUNCTIONS} public functions with docstrings"
        ((TESTS_PASSED++))
    elif [ "${PUBLIC_FUNCTIONS}" -gt 0 ]; then
        echo -e "${RED}✗ FAIL${NC}: Found ${PUBLIC_FUNCTIONS} public functions but no docstrings"
        ((TESTS_FAILED++))
        EXIT_CODE=1
    else
        echo -e "${YELLOW}⚠ WARNING${NC}: No public functions found in context_extraction.py"
        ((TESTS_FAILED++))
        EXIT_CODE=1
    fi
else
    echo -e "${RED}✗ FAIL${NC}: File does not exist: ${CONTEXT_EXTRACTION}"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi
echo ""

# Test 5: adaptive_questioning_engine.py has docstrings for public methods
echo "Test 5: adaptive_questioning_engine.py has docstrings for public methods"
((TESTS_TOTAL++))
if [ -f "${ADAPTIVE_QUESTIONING}" ]; then
    # Count public methods (def name() not starting with _)
    PUBLIC_METHODS=$(grep -c "def [^_]" "${ADAPTIVE_QUESTIONING}" || echo "0")

    # Count docstrings (triple quotes)
    DOCSTRINGS=$(grep -c '"""' "${ADAPTIVE_QUESTIONING}" || echo "0")

    if [ "${PUBLIC_METHODS}" -gt 0 ] && [ "${DOCSTRINGS}" -gt 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}: Found ${PUBLIC_METHODS} public methods with docstrings"
        ((TESTS_PASSED++))
    elif [ "${PUBLIC_METHODS}" -gt 0 ]; then
        echo -e "${RED}✗ FAIL${NC}: Found ${PUBLIC_METHODS} public methods but no docstrings"
        ((TESTS_FAILED++))
        EXIT_CODE=1
    else
        echo -e "${YELLOW}⚠ WARNING${NC}: No public methods found in adaptive_questioning_engine.py"
        ((TESTS_FAILED++))
        EXIT_CODE=1
    fi
else
    echo -e "${RED}✗ FAIL${NC}: File does not exist: ${ADAPTIVE_QUESTIONING}"
    ((TESTS_FAILED++))
    EXIT_CODE=1
fi
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "SUMMARY: AC5 Inline Code Documentation Tests"
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
  "test_name": "AC5: Inline Code Documentation",
  "total_tests": ${TESTS_TOTAL},
  "passed": ${TESTS_PASSED},
  "failed": ${TESTS_FAILED},
  "exit_code": ${EXIT_CODE},
  "context_extraction_functions": "${PUBLIC_FUNCTIONS}",
  "adaptive_questioning_methods": "${PUBLIC_METHODS}",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

exit ${EXIT_CODE}
