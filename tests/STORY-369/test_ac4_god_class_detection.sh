#!/bin/bash
##############################################################################
# Test Suite: STORY-369 AC#4 - God Class Detection Using Class-Method Correlation
# Purpose: Verify class-function correlation, line range containment, >20 threshold
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

# AC#4 Test 1: Class-to-function correlation instructions present
test_correlation_instructions() {
    [ -f "$REF_FILE" ] && grep -qi 'correlat' "$REF_FILE"
}

# AC#4 Test 2: Uses line range containment for method-to-class mapping
test_line_range_containment() {
    [ -f "$REF_FILE" ] && grep -qi 'line.*range\|within.*class.*range\|falls.*within\|containment' "$REF_FILE"
}

# AC#4 Test 3: God class threshold >20 methods for Treelint mode
test_god_class_threshold_20() {
    [ -f "$REF_FILE" ] && grep -q '20.*method\|>20\|> 20' "$REF_FILE"
}

# AC#4 Test 4: Standalone function handling documented
test_standalone_function_handling() {
    [ -f "$REF_FILE" ] && grep -qi 'standalone.*function\|function.*outside.*class\|module.*level' "$REF_FILE"
}

##############################################################################
# Execute Tests
##############################################################################

echo "=== STORY-369 AC#4: God Class Detection Using Class-Method Correlation ==="
echo "Reference: $REF_FILE"
echo ""

run_test "Class-to-function correlation instructions present" test_correlation_instructions
run_test "Uses line range containment for method-to-class mapping" test_line_range_containment
run_test "God class threshold set to >20 methods for Treelint mode" test_god_class_threshold_20
run_test "Standalone function handling documented" test_standalone_function_handling

echo ""
echo "=== Results: $TESTS_PASSED/$TESTS_RUN passed, $TESTS_FAILED failed ==="
exit $TESTS_FAILED
