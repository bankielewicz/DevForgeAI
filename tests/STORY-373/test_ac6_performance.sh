#!/bin/bash
##############################################################################
# Test Suite: STORY-373 AC#6 - Performance validation under 10 seconds
# Purpose: Verify reference file documents performance requirements:
#          <10s for large codebases (100K files), <2s for small (<10K files),
#          <5ms daemon mode, <50ms JSON parsing, <5ms Top-N filtering,
#          <3s Grep fallback, and 15s timeout
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

# AC#6 Test 1: Performance section exists in reference file
test_performance_section_exists() {
    [ -f "$REF_FILE" ] && grep -qi 'performance\|NFR\|non-functional' "$REF_FILE"
}

# AC#6 Test 2: <10 seconds for large codebases (100,000 files) documented
test_10_seconds_large_codebase() {
    [ -f "$REF_FILE" ] && grep -qi '10.*second\|10s\|< 10' "$REF_FILE"
}

# AC#6 Test 3: 100,000 files threshold documented
test_100k_files_threshold() {
    [ -f "$REF_FILE" ] && grep -q '100,000\|100000\|100K' "$REF_FILE"
}

# AC#6 Test 4: <2 seconds for small codebases (<10,000 files) documented
test_2_seconds_small_codebase() {
    [ -f "$REF_FILE" ] && grep -qi '2.*second\|2s.*small\|< 2' "$REF_FILE"
}

# AC#6 Test 5: 10,000 files threshold for small codebase documented
test_10k_files_threshold() {
    [ -f "$REF_FILE" ] && grep -q '10,000\|10000\|10K' "$REF_FILE"
}

# AC#6 Test 6: <5ms daemon mode query documented
test_5ms_daemon_mode() {
    [ -f "$REF_FILE" ] && grep -qi '5.*ms.*daemon\|daemon.*5.*ms\|< 5ms' "$REF_FILE"
}

# AC#6 Test 7: <50ms JSON parsing target documented
test_50ms_json_parsing() {
    [ -f "$REF_FILE" ] && grep -qi '50.*ms.*pars\|pars.*50.*ms\|< 50ms' "$REF_FILE"
}

# AC#6 Test 8: <5ms Top-N filtering target documented
test_5ms_topn_filtering() {
    [ -f "$REF_FILE" ] && grep -qi '5.*ms.*filter\|filter.*5.*ms\|top-N.*5' "$REF_FILE"
}

# AC#6 Test 9: <3 seconds Grep fallback target documented
test_3_seconds_grep_fallback() {
    [ -f "$REF_FILE" ] && grep -qi '3.*second.*grep\|grep.*3.*second\|fallback.*3' "$REF_FILE"
}

# AC#6 Test 10: Wall-clock time measurement guidance documented
test_wall_clock_measurement() {
    [ -f "$REF_FILE" ] && grep -qi 'wall.clock\|elapsed\|timing\|wall-clock' "$REF_FILE"
}

# AC#6 Test 11: 15-second timeout to prevent hanging documented
test_15_second_timeout() {
    [ -f "$REF_FILE" ] && grep -q '15.*second\|15s\|timeout.*15\|15000' "$REF_FILE"
}

# AC#6 Test 12: 50,000 symbols scalability target documented
test_50k_symbols_scalability() {
    [ -f "$REF_FILE" ] && grep -q '50,000\|50000\|50K.*symbol' "$REF_FILE"
}

# Run all tests
echo "============================================================"
echo "STORY-373 AC#6: Performance validation under 10 seconds"
echo "============================================================"

run_test "Performance section exists" test_performance_section_exists
run_test "<10s for large codebases (100K files)" test_10_seconds_large_codebase
run_test "100,000 files threshold documented" test_100k_files_threshold
run_test "<2s for small codebases (<10K files)" test_2_seconds_small_codebase
run_test "10,000 files threshold documented" test_10k_files_threshold
run_test "<5ms daemon mode query" test_5ms_daemon_mode
run_test "<50ms JSON parsing target" test_50ms_json_parsing
run_test "<5ms Top-N filtering target" test_5ms_topn_filtering
run_test "<3s Grep fallback target" test_3_seconds_grep_fallback
run_test "Wall-clock time measurement" test_wall_clock_measurement
run_test "15-second timeout documented" test_15_second_timeout
run_test "50,000 symbols scalability" test_50k_symbols_scalability

echo ""
echo "============================================================"
echo "Results: $TESTS_PASSED/$TESTS_RUN passed, $TESTS_FAILED failed"
echo "============================================================"

exit $TESTS_FAILED
