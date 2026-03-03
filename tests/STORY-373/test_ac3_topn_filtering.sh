#!/bin/bash
##############################################################################
# Test Suite: STORY-373 AC#3 - Top-N symbol filtering for context optimization
# Purpose: Verify Top-N filtering logic documentation including default K=50,
#          clamping rules (BR-004), field preservation, and total_symbols
#          retention for coverage ratio calculation
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
REF_FILE="${PROJECT_ROOT}/src/claude/skills/devforgeai-development/references/treelint-repository-map.md"

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

# AC#3 Test 1: Top-N filtering section exists in reference file
test_topn_section_exists() {
    [ -f "$REF_FILE" ] && grep -qi 'top-N\|top.N\|top N\|filtering' "$REF_FILE"
}

# AC#3 Test 2: Default K=50 documented
test_default_k_50() {
    [ -f "$REF_FILE" ] && grep -q 'default.*50\|K.*50\|50.*default' "$REF_FILE"
}

# AC#3 Test 3: Only K highest-ranked symbols returned (rank 1 through K)
test_k_highest_ranked_returned() {
    [ -f "$REF_FILE" ] && grep -qi 'highest.*ranked\|rank 1.*through\|top.*K.*symbols\|first.*K.*symbols' "$REF_FILE"
}

# AC#3 Test 4: Filtered result preserves all fields per symbol
test_filtered_preserves_fields() {
    [ -f "$REF_FILE" ] && grep -qi 'preserv.*fields\|all fields.*preserved\|retain.*fields' "$REF_FILE"
}

# AC#3 Test 5: total_symbols reflects full codebase count (not filtered count)
test_total_symbols_full_count() {
    [ -f "$REF_FILE" ] && grep -qi 'total_symbols.*full\|total_symbols.*entire\|total_symbols.*original\|coverage.*ratio' "$REF_FILE"
}

# AC#3 Test 6: Coverage ratio formula documented (K/total_symbols)
test_coverage_ratio_documented() {
    [ -f "$REF_FILE" ] && grep -qi 'coverage.*ratio\|K/total\|K.*divided\|context.*coverage' "$REF_FILE"
}

# AC#3 Test 7: K=0 clamped to 1 (BR-004)
test_k_zero_clamped_to_1() {
    [ -f "$REF_FILE" ] && grep -qi 'K.*0.*clamp\|clamp.*1\|minimum.*1\|K < 1.*becomes 1' "$REF_FILE"
}

# AC#3 Test 8: K > 10000 clamped to 10000 (BR-004)
test_k_over_10000_clamped() {
    [ -f "$REF_FILE" ] && grep -qi '10000\|10,000\|maximum.*K\|K.*cap' "$REF_FILE"
}

# AC#3 Test 9: Non-integer K values rejected with validation error (BR-004)
test_non_integer_k_rejected() {
    [ -f "$REF_FILE" ] && grep -qi 'non-integer.*reject\|validation.*error\|invalid.*K\|integer.*required' "$REF_FILE"
}

# AC#3 Test 10: K > total_symbols returns all symbols (edge case)
test_k_greater_than_total() {
    [ -f "$REF_FILE" ] && grep -qi 'K.*greater.*total\|K.*exceed\|K.*more.*than.*total\|all.*symbols.*returned' "$REF_FILE"
}

# AC#3 Test 11: K=1 returns single most important symbol (edge case)
test_k_equals_1() {
    [ -f "$REF_FILE" ] && grep -qi 'K.*1.*single\|single.*symbol\|K=1\|one.*symbol' "$REF_FILE"
}

# AC#3 Test 12: Configurable K parameter documented
test_configurable_k_parameter() {
    [ -f "$REF_FILE" ] && grep -qi 'configurable\|override\|parameter.*K\|custom.*K' "$REF_FILE"
}

# Run all tests
echo "============================================================"
echo "STORY-373 AC#3: Top-N symbol filtering for context optimization"
echo "============================================================"

run_test "Top-N filtering section exists" test_topn_section_exists
run_test "Default K=50 documented" test_default_k_50
run_test "K highest-ranked symbols returned" test_k_highest_ranked_returned
run_test "Filtered result preserves all fields" test_filtered_preserves_fields
run_test "total_symbols reflects full codebase count" test_total_symbols_full_count
run_test "Coverage ratio formula documented" test_coverage_ratio_documented
run_test "K=0 clamped to 1 (BR-004)" test_k_zero_clamped_to_1
run_test "K > 10000 clamped to 10000 (BR-004)" test_k_over_10000_clamped
run_test "Non-integer K rejected (BR-004)" test_non_integer_k_rejected
run_test "K > total_symbols returns all (edge case)" test_k_greater_than_total
run_test "K=1 returns single symbol (edge case)" test_k_equals_1
run_test "Configurable K parameter" test_configurable_k_parameter

echo ""
echo "============================================================"
echo "Results: $TESTS_PASSED/$TESTS_RUN passed, $TESTS_FAILED failed"
echo "============================================================"

exit $TESTS_FAILED
