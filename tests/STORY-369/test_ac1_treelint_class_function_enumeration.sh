#!/bin/bash
##############################################################################
# Test Suite: STORY-369 AC#1 - Treelint Integration for Class and Function Enumeration
# Purpose: Verify anti-pattern-scanner.md Phase 5 loads Treelint reference file
#          and reference file contains class/function search instructions
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
AGENT_FILE="${PROJECT_ROOT}/src/claude/agents/anti-pattern-scanner.md"
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

# AC#1 Test 1: anti-pattern-scanner.md Phase 5 contains Read() for phase5-treelint-detection.md
test_phase5_read_pointer() {
    grep -q 'Read.*phase5-treelint-detection' "$AGENT_FILE"
}

# AC#1 Test 2: Reference file contains treelint search --type class instruction
test_treelint_class_search() {
    [ -f "$REF_FILE" ] && grep -q 'treelint search.*--type class' "$REF_FILE"
}

# AC#1 Test 3: Reference file contains treelint search --type function instruction
test_treelint_function_search() {
    [ -f "$REF_FILE" ] && grep -q 'treelint search.*--type function' "$REF_FILE"
}

# AC#1 Test 4: Uses --format json flag for class search
test_format_json_class() {
    [ -f "$REF_FILE" ] && grep -q 'treelint search.*--type class.*--format json' "$REF_FILE"
}

# AC#1 Test 5: Uses --format json flag for function search
test_format_json_function() {
    [ -f "$REF_FILE" ] && grep -q 'treelint search.*--type function.*--format json' "$REF_FILE"
}

##############################################################################
# Execute Tests
##############################################################################

echo "=== STORY-369 AC#1: Treelint Class/Function Enumeration ==="
echo "Target: $AGENT_FILE"
echo "Reference: $REF_FILE"
echo ""

run_test "Phase 5 contains Read() for phase5-treelint-detection.md" test_phase5_read_pointer
run_test "Reference file contains treelint search --type class" test_treelint_class_search
run_test "Reference file contains treelint search --type function" test_treelint_function_search
run_test "Uses --format json for class search" test_format_json_class
run_test "Uses --format json for function search" test_format_json_function

echo ""
echo "=== Results: $TESTS_PASSED/$TESTS_RUN passed, $TESTS_FAILED failed ==="
exit $TESTS_FAILED
