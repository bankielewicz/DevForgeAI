#!/bin/bash
##############################################################################
# Test Suite: STORY-373 AC#5 - Error handling for treelint unavailable,
#                               empty codebase, and stale index
# Purpose: Verify structured error objects for all failure modes, Grep fallback,
#          and staleness detection logic documentation
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

# AC#5 Test 1: treelint_unavailable error type documented
test_treelint_unavailable_error() {
    [ -f "$REF_FILE" ] && grep -q 'treelint_unavailable' "$REF_FILE"
}

# AC#5 Test 2: empty_codebase error type documented
test_empty_codebase_error() {
    [ -f "$REF_FILE" ] && grep -q 'empty_codebase' "$REF_FILE"
}

# AC#5 Test 3: stale_index error type documented
test_stale_index_error() {
    [ -f "$REF_FILE" ] && grep -q 'stale_index' "$REF_FILE"
}

# AC#5 Test 4: daemon_not_running error type documented
test_daemon_not_running_error() {
    [ -f "$REF_FILE" ] && grep -q 'daemon_not_running' "$REF_FILE"
}

# AC#5 Test 5: index_corrupted error type documented
test_index_corrupted_error() {
    [ -f "$REF_FILE" ] && grep -q 'index_corrupted' "$REF_FILE"
}

# AC#5 Test 6: unknown_error type documented as catch-all
test_unknown_error_type() {
    [ -f "$REF_FILE" ] && grep -q 'unknown_error' "$REF_FILE"
}

# AC#5 Test 7: Structured error contains error_type field
test_error_type_field() {
    [ -f "$REF_FILE" ] && grep -q 'error_type' "$REF_FILE"
}

# AC#5 Test 8: Structured error contains human-readable message
test_error_contains_message() {
    [ -f "$REF_FILE" ] && grep -qi 'message' "$REF_FILE"
}

# AC#5 Test 9: Exit code 127 triggers treelint_unavailable
test_exit_code_127_handling() {
    [ -f "$REF_FILE" ] && grep -q '127' "$REF_FILE"
}

# AC#5 Test 10: Grep fallback documented when Treelint unavailable
test_grep_fallback_documented() {
    [ -f "$REF_FILE" ] && grep -qi 'grep.*fallback\|fallback.*grep' "$REF_FILE"
}

# AC#5 Test 11: Fallback chain order documented (daemon -> CLI -> Grep)
test_fallback_chain_order() {
    [ -f "$REF_FILE" ] && grep -qi 'daemon.*CLI.*Grep\|3-tier\|three-tier\|fallback chain' "$REF_FILE"
}

# AC#5 Test 12: Fallback results marked with data source tier
test_fallback_source_marking() {
    [ -f "$REF_FILE" ] && grep -q 'grep-approximation\|treelint-cli\|treelint-daemon\|data_source' "$REF_FILE"
}

# AC#5 Test 13: Stale index detection via mtime comparison documented
test_stale_index_mtime_detection() {
    [ -f "$REF_FILE" ] && grep -qi 'mtime\|modification.*time\|staleness.*detect\|index.*older\|stale.*detect' "$REF_FILE"
}

# AC#5 Test 14: Stale index returns results with staleness warning flag
test_stale_index_warning_flag() {
    [ -f "$REF_FILE" ] && grep -qi 'stale.*warning\|staleness.*flag\|stale_index.*true\|warning.*stale' "$REF_FILE"
}

# AC#5 Test 15: 15-second timeout documented for Bash invocations
test_timeout_15_seconds() {
    [ -f "$REF_FILE" ] && grep -q '15.*second\|15s\|15000\|timeout.*15' "$REF_FILE"
}

# AC#5 Test 16: Grep fallback returns alphabetical listing with references: 0
test_grep_fallback_alphabetical() {
    [ -f "$REF_FILE" ] && grep -qi 'alphabetical\|references.*0\|grep.*approximation' "$REF_FILE"
}

# AC#5 Test 17: Empty codebase handled as valid success (BR-003)
test_empty_codebase_valid_success() {
    [ -f "$REF_FILE" ] && grep -qi 'empty.*valid\|0.*symbols.*success\|not.*error.*empty\|total_symbols.*0' "$REF_FILE"
}

# AC#5 Test 18: Error handling section exists in reference file
test_error_handling_section() {
    [ -f "$REF_FILE" ] && grep -qi 'error.*handling\|error.*recovery\|failure.*mode' "$REF_FILE"
}

# Run all tests
echo "============================================================"
echo "STORY-373 AC#5: Error handling and fallback chain"
echo "============================================================"

run_test "treelint_unavailable error type" test_treelint_unavailable_error
run_test "empty_codebase error type" test_empty_codebase_error
run_test "stale_index error type" test_stale_index_error
run_test "daemon_not_running error type" test_daemon_not_running_error
run_test "index_corrupted error type" test_index_corrupted_error
run_test "unknown_error catch-all type" test_unknown_error_type
run_test "error_type field in structured error" test_error_type_field
run_test "Human-readable message in error" test_error_contains_message
run_test "Exit code 127 handling" test_exit_code_127_handling
run_test "Grep fallback documented" test_grep_fallback_documented
run_test "Fallback chain order (daemon->CLI->Grep)" test_fallback_chain_order
run_test "Fallback results marked with source" test_fallback_source_marking
run_test "Stale index mtime detection" test_stale_index_mtime_detection
run_test "Stale index warning flag" test_stale_index_warning_flag
run_test "15-second timeout documented" test_timeout_15_seconds
run_test "Grep fallback returns alphabetical with refs=0" test_grep_fallback_alphabetical
run_test "Empty codebase is valid success (BR-003)" test_empty_codebase_valid_success
run_test "Error handling section exists" test_error_handling_section

echo ""
echo "============================================================"
echo "Results: $TESTS_PASSED/$TESTS_RUN passed, $TESTS_FAILED failed"
echo "============================================================"

exit $TESTS_FAILED
