#!/bin/bash
##############################################################################
# Test Suite: STORY-369 AC#5 - Performance Validation
# Purpose: Verify performance target (<100ms) and stats.elapsed_ms documented
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

# AC#5 Test 1: Performance target (<100ms) documented
test_performance_target() {
    [ -f "$REF_FILE" ] && grep -q '100ms\|100 ms\|< 100' "$REF_FILE"
}

# AC#5 Test 2: stats.elapsed_ms field referenced
test_elapsed_ms_field() {
    [ -f "$REF_FILE" ] && grep -q 'stats\.elapsed_ms\|elapsed_ms' "$REF_FILE"
}

##############################################################################
# Execute Tests
##############################################################################

echo "=== STORY-369 AC#5: Performance Validation ==="
echo "Reference: $REF_FILE"
echo ""

run_test "Performance target (<100ms) documented in reference file" test_performance_target
run_test "stats.elapsed_ms field referenced" test_elapsed_ms_field

echo ""
echo "=== Results: $TESTS_PASSED/$TESTS_RUN passed, $TESTS_FAILED failed ==="
exit $TESTS_FAILED
