#!/bin/bash

##############################################################################
# Test Suite: STORY-179 AC#5 - Complete Constraint Template & Code Snippets
#
# AC#5: Complete Constraint Template with Code Snippet Rule
#   Given: Response Constraints section in phase files
#   When: reading the complete constraint block
#   Then: all 4 constraint rules MUST be present including "No code snippets"
#
# Expected Template:
#   **Response Constraints:**
#   - Limit response to 500 words maximum
#   - Use bullet points, not paragraphs
#   - Only include actionable findings
#   - No code snippets unless essential
#
# Test Strategy:
#   - Verify all 4 constraint lines appear together
#   - Verify "No code snippets" rule is present
#   - Verify constraint template exists in each phase file
##############################################################################

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# File paths
PROJECT_ROOT="/mnt/c/Projects/DevForgeAI2"
PHASE_02="${PROJECT_ROOT}/.claude/skills/devforgeai-development/phases/phase-02-test-first.md"
PHASE_03="${PROJECT_ROOT}/.claude/skills/devforgeai-development/phases/phase-03-implementation.md"
PHASE_04="${PROJECT_ROOT}/.claude/skills/devforgeai-development/phases/phase-04-refactoring.md"
PHASE_05="${PROJECT_ROOT}/.claude/skills/devforgeai-development/phases/phase-05-integration.md"

##############################################################################
# Helper Functions
##############################################################################

run_test() {
    local test_name="$1"
    local test_description="$2"

    TESTS_RUN=$((TESTS_RUN + 1))

    echo ""
    echo -e "${YELLOW}Test $TESTS_RUN: $test_name${NC}"
    echo "Description: $test_description"
    echo "---"
}

assert_grep_match() {
    local pattern="$1"
    local file="$2"
    local test_name="$3"

    if grep -qi "$pattern" "$file" 2>/dev/null; then
        echo -e "${GREEN}PASSED${NC}: Pattern '$pattern' found in $(basename $file)"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}FAILED${NC}: Pattern '$pattern' NOT found in $(basename $file)"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

assert_file_exists() {
    local file="$1"

    if [[ ! -f "$file" ]]; then
        echo -e "${RED}FAILED${NC}: File $file does not exist"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    else
        echo -e "${GREEN}PASSED${NC}: File $(basename $file) exists"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    fi
}

# Check if all 4 constraint rules exist in a file
check_complete_template() {
    local file="$1"
    local missing=0

    if ! grep -qi "500 words" "$file" 2>/dev/null; then
        echo "  Missing: 500 words maximum"
        missing=$((missing + 1))
    fi

    if ! grep -qi "bullet point" "$file" 2>/dev/null; then
        echo "  Missing: bullet points instruction"
        missing=$((missing + 1))
    fi

    if ! grep -qi "actionable" "$file" 2>/dev/null; then
        echo "  Missing: actionable findings"
        missing=$((missing + 1))
    fi

    if ! grep -qi "code snippet" "$file" 2>/dev/null; then
        echo "  Missing: code snippets rule"
        missing=$((missing + 1))
    fi

    return $missing
}

##############################################################################
# AC#5 Test Cases - Complete Constraint Template
##############################################################################

echo ""
echo "============================================================================"
echo " STORY-179 AC#5: Complete Constraint Template with Code Snippet Rule"
echo "============================================================================"
echo ""

# Test 5.1: Verify phase-02 contains "No code snippets" rule
run_test \
    "test_ac5_phase02_code_snippets" \
    "Verify phase-02-test-first.md contains 'code snippet' rule"
assert_file_exists "$PHASE_02"
assert_grep_match "code snippet" "$PHASE_02" "Phase 02 code snippets"

# Test 5.2: Verify phase-03 contains "No code snippets" rule
run_test \
    "test_ac5_phase03_code_snippets" \
    "Verify phase-03-implementation.md contains 'code snippet' rule"
assert_file_exists "$PHASE_03"
assert_grep_match "code snippet" "$PHASE_03" "Phase 03 code snippets"

# Test 5.3: Verify phase-04 contains "No code snippets" rule
run_test \
    "test_ac5_phase04_code_snippets" \
    "Verify phase-04-refactoring.md contains 'code snippet' rule"
assert_file_exists "$PHASE_04"
assert_grep_match "code snippet" "$PHASE_04" "Phase 04 code snippets"

# Test 5.4: Verify phase-05 contains "No code snippets" rule
run_test \
    "test_ac5_phase05_code_snippets" \
    "Verify phase-05-integration.md contains 'code snippet' rule"
assert_file_exists "$PHASE_05"
assert_grep_match "code snippet" "$PHASE_05" "Phase 05 code snippets"

# Test 5.5: Verify "unless essential" qualifier
run_test \
    "test_ac5_unless_essential_qualifier" \
    "Verify 'unless essential' qualifier appears with code snippet rule"
count=0
for file in "$PHASE_02" "$PHASE_03" "$PHASE_04" "$PHASE_05"; do
    if grep -qi "unless essential" "$file" 2>/dev/null; then
        count=$((count + 1))
    fi
done

if [[ $count -ge 1 ]]; then
    echo -e "${GREEN}PASSED${NC}: 'unless essential' qualifier found in $count file(s)"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAILED${NC}: 'unless essential' qualifier NOT found in any phase file"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 5.6: Verify complete template in phase-02
run_test \
    "test_ac5_phase02_complete_template" \
    "Verify phase-02-test-first.md has all 4 constraint rules"
TESTS_RUN=$((TESTS_RUN + 1))
if check_complete_template "$PHASE_02"; then
    echo -e "${GREEN}PASSED${NC}: phase-02-test-first.md has complete constraint template"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAILED${NC}: phase-02-test-first.md missing constraint rules"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 5.7: Verify complete template in phase-03
run_test \
    "test_ac5_phase03_complete_template" \
    "Verify phase-03-implementation.md has all 4 constraint rules"
TESTS_RUN=$((TESTS_RUN + 1))
if check_complete_template "$PHASE_03"; then
    echo -e "${GREEN}PASSED${NC}: phase-03-implementation.md has complete constraint template"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAILED${NC}: phase-03-implementation.md missing constraint rules"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 5.8: Verify complete template in phase-04
run_test \
    "test_ac5_phase04_complete_template" \
    "Verify phase-04-refactoring.md has all 4 constraint rules"
TESTS_RUN=$((TESTS_RUN + 1))
if check_complete_template "$PHASE_04"; then
    echo -e "${GREEN}PASSED${NC}: phase-04-refactoring.md has complete constraint template"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAILED${NC}: phase-04-refactoring.md missing constraint rules"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

# Test 5.9: Verify complete template in phase-05
run_test \
    "test_ac5_phase05_complete_template" \
    "Verify phase-05-integration.md has all 4 constraint rules"
TESTS_RUN=$((TESTS_RUN + 1))
if check_complete_template "$PHASE_05"; then
    echo -e "${GREEN}PASSED${NC}: phase-05-integration.md has complete constraint template"
    TESTS_PASSED=$((TESTS_PASSED + 1))
else
    echo -e "${RED}FAILED${NC}: phase-05-integration.md missing constraint rules"
    TESTS_FAILED=$((TESTS_FAILED + 1))
fi

##############################################################################
# Summary Report
##############################################################################

echo ""
echo "============================================================================"
echo "Test Summary Report - AC#5: Complete Constraint Template"
echo "============================================================================"
echo "Total Tests Run:    $TESTS_RUN"
echo -e "Tests Passed:       ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed:       ${RED}$TESTS_FAILED${NC}"
echo "============================================================================"

if [[ $TESTS_FAILED -eq 0 ]]; then
    echo -e "${GREEN}SUCCESS: All AC#5 tests passed${NC}"
    exit 0
else
    echo -e "${RED}FAILURE: AC#5 test failures detected - Complete template not present${NC}"
    exit 1
fi
