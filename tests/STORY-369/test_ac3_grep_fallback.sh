#!/bin/bash
##############################################################################
# Test Suite: STORY-369 AC#3 - Grep Fallback for Unsupported Languages
# Purpose: Verify fallback section exists, uses native Grep, warning messaging
# Phase: TDD Red - All tests expected to FAIL before implementation
##############################################################################

set -o pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
REF_FILE="${PROJECT_ROOT}/src/claude/docs/agents/anti-pattern-scanner/phase5-treelint-detection.md"

run_test() {
    local test_name=$1
    local test_func=$2
    TESTS_RUN=$((TESTS_RUN + 1))
    echo -e "\n[Test $TESTS_RUN] $test_name"
    if $test_func; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        echo -e "${GREEN}PASSED${NC}"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        echo -e "${RED}FAILED${NC}"
    fi
}

# AC#3 Test 1: Fallback section exists in reference file
test_fallback_section_exists() {
    [ -f "$REF_FILE" ] && grep -qi 'fallback' "$REF_FILE"
}

# AC#3 Test 2: Fallback uses native Grep tool (not Bash grep)
test_native_grep_tool() {
    [ -f "$REF_FILE" ] && grep -q 'Grep(pattern=' "$REF_FILE"
}

# AC#3 Test 3: Warning-level messaging (not HALT) on fallback
test_warning_not_halt() {
    if [ ! -f "$REF_FILE" ]; then
        return 1
    fi
    # Must contain warning-level messaging
    grep -qi 'warning' "$REF_FILE" || return 1
    # Fallback section must NOT contain HALT on Treelint failure
    # Extract fallback section and verify no HALT instruction
    local fallback_content
    fallback_content=$(sed -n '/[Ff]allback/,/^##/p' "$REF_FILE" 2>/dev/null)
    if echo "$fallback_content" | grep -qi 'HALT'; then
        return 1
    fi
    return 0
}

# AC#3 Test 4: Distinguishes empty results from command failure (BR-002)
test_empty_vs_failure_distinction() {
    [ -f "$REF_FILE" ] && grep -q 'exit code 0\|empty results\|zero matches' "$REF_FILE"
}

##############################################################################
# Execute Tests
##############################################################################

echo "=== STORY-369 AC#3: Grep Fallback for Unsupported Languages ==="
echo "Reference: $REF_FILE"
echo ""

run_test "Fallback section exists in reference file" test_fallback_section_exists
run_test "Fallback uses native Grep tool (Grep(pattern=...))" test_native_grep_tool
run_test "Warning-level messaging on fallback (not HALT)" test_warning_not_halt
run_test "Distinguishes empty results from command failure" test_empty_vs_failure_distinction

echo ""
echo "=== Results: $TESTS_PASSED/$TESTS_RUN passed, $TESTS_FAILED failed ==="
exit $TESTS_FAILED
