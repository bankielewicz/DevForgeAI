#!/bin/bash
##############################################################################
# Test Suite: STORY-370 AC#5 - Performance validation under 200ms
# Purpose: Verify reference file documents 200ms performance requirement
#          and timing measurement guidance for dependency queries
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
REF_FILE="${PROJECT_ROOT}/src/claude/skills/devforgeai-development/references/treelint-dependency-query.md"

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

# AC#5 Test 1: 200ms performance target documented
test_200ms_target_documented() {
    [ -f "$REF_FILE" ] && grep -q '200.*ms\|200ms' "$REF_FILE"
}

# AC#5 Test 2: Performance applies to symbols with <50 callers/callees
test_50_callers_threshold() {
    [ -f "$REF_FILE" ] && grep -q '50.*callers\|50.*callees\|fewer than 50' "$REF_FILE"
}

# AC#5 Test 3: Wall-clock time measurement documented
test_wall_clock_measurement() {
    [ -f "$REF_FILE" ] && grep -q 'wall.clock\|elapsed\|timing\|wall-clock' "$REF_FILE"
}

# AC#5 Test 4: JSON parsing completes within 10ms documented
test_10ms_parsing_target() {
    [ -f "$REF_FILE" ] && grep -q '10.*ms\|10ms.*pars' "$REF_FILE"
}

# AC#5 Test 5: Grep fallback performance within 500ms documented
test_500ms_grep_fallback() {
    [ -f "$REF_FILE" ] && grep -q '500.*ms\|500ms.*fallback\|grep.*500' "$REF_FILE"
}

# AC#5 Test 6: Performance section exists in reference
test_performance_section_exists() {
    [ -f "$REF_FILE" ] && grep -qi 'performance\|NFR\|non-functional' "$REF_FILE"
}

# Run all tests
echo "============================================================"
echo "STORY-370 AC#5: Performance validation under 200ms"
echo "============================================================"

run_test "200ms performance target documented" test_200ms_target_documented
run_test "<50 callers/callees threshold" test_50_callers_threshold
run_test "Wall-clock time measurement" test_wall_clock_measurement
run_test "10ms JSON parsing target" test_10ms_parsing_target
run_test "500ms Grep fallback target" test_500ms_grep_fallback
run_test "Performance section exists" test_performance_section_exists

echo ""
echo "============================================================"
echo "Results: $TESTS_PASSED/$TESTS_RUN passed, $TESTS_FAILED failed"
echo "============================================================"

exit $TESTS_FAILED
