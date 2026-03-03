#!/bin/bash
##############################################################################
# Test Suite: STORY-370 AC#3 - Error handling for symbol-not-found, daemon-not-running
# Purpose: Verify structured error objects for all failure modes and Grep fallback
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

# AC#3 Test 1: symbol_not_found error type documented
test_symbol_not_found_error() {
    [ -f "$REF_FILE" ] && grep -q 'symbol_not_found' "$REF_FILE"
}

# AC#3 Test 2: daemon_not_running error type documented
test_daemon_not_running_error() {
    [ -f "$REF_FILE" ] && grep -q 'daemon_not_running' "$REF_FILE"
}

# AC#3 Test 3: treelint_unavailable error type documented
test_treelint_unavailable_error() {
    [ -f "$REF_FILE" ] && grep -q 'treelint_unavailable' "$REF_FILE"
}

# AC#3 Test 4: unknown_error type documented as catch-all
test_unknown_error_type() {
    [ -f "$REF_FILE" ] && grep -q 'unknown_error' "$REF_FILE"
}

# AC#3 Test 5: Structured error contains error_type field
test_error_type_field() {
    [ -f "$REF_FILE" ] && grep -q 'error_type' "$REF_FILE"
}

# AC#3 Test 6: Structured error contains original symbol name
test_error_contains_symbol_name() {
    [ -f "$REF_FILE" ] && grep -q 'symbol.*queried\|original.*symbol\|queried_symbol' "$REF_FILE"
}

# AC#3 Test 7: Structured error contains human-readable message
test_error_contains_message() {
    [ -f "$REF_FILE" ] && grep -q 'message\|error_message' "$REF_FILE"
}

# AC#3 Test 8: Grep fallback documented when Treelint unavailable
test_grep_fallback_documented() {
    [ -f "$REF_FILE" ] && grep -qi 'grep.*fallback\|fallback.*grep' "$REF_FILE"
}

# AC#3 Test 9: Fallback chain order documented (daemon -> CLI -> Grep)
test_fallback_chain_order() {
    [ -f "$REF_FILE" ] && grep -q 'daemon.*CLI.*Grep\|3-tier\|three-tier\|fallback chain' "$REF_FILE"
}

# AC#3 Test 10: Exit code 127 triggers treelint_unavailable
test_exit_code_127_handling() {
    [ -f "$REF_FILE" ] && grep -q '127' "$REF_FILE"
}

# AC#3 Test 11: 5-second timeout documented for Bash invocations
test_timeout_5_seconds() {
    [ -f "$REF_FILE" ] && grep -q '5.*second\|5000\|timeout' "$REF_FILE"
}

# AC#3 Test 12: Fallback results marked with source tier
test_fallback_source_marking() {
    [ -f "$REF_FILE" ] && grep -q 'grep-approximation\|treelint-cli\|treelint-daemon\|source.*tier\|data_source' "$REF_FILE"
}

# Run all tests
echo "============================================================"
echo "STORY-370 AC#3: Error handling for failures and fallback"
echo "============================================================"

run_test "symbol_not_found error type documented" test_symbol_not_found_error
run_test "daemon_not_running error type documented" test_daemon_not_running_error
run_test "treelint_unavailable error type documented" test_treelint_unavailable_error
run_test "unknown_error type documented" test_unknown_error_type
run_test "error_type field in structured error" test_error_type_field
run_test "Structured error contains original symbol" test_error_contains_symbol_name
run_test "Structured error contains message" test_error_contains_message
run_test "Grep fallback documented" test_grep_fallback_documented
run_test "Fallback chain order (daemon->CLI->Grep)" test_fallback_chain_order
run_test "Exit code 127 handling" test_exit_code_127_handling
run_test "5-second timeout documented" test_timeout_5_seconds
run_test "Fallback results marked with source" test_fallback_source_marking

echo ""
echo "============================================================"
echo "Results: $TESTS_PASSED/$TESTS_RUN passed, $TESTS_FAILED failed"
echo "============================================================"

exit $TESTS_FAILED
