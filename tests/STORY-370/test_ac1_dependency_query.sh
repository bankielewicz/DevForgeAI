#!/bin/bash
##############################################################################
# Test Suite: STORY-370 AC#1 - Successful dependency query returns callers/callees
# Purpose: Verify treelint deps --calls --symbol <name> --format json output
#          contains symbol, callers, and callees fields with correct structure
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

# AC#1 Test 1: Reference file exists for dependency query service
test_dependency_query_ref_exists() {
    [ -f "$REF_FILE" ]
}

# AC#1 Test 2: Reference file documents treelint deps --calls command
test_deps_calls_command_documented() {
    [ -f "$REF_FILE" ] && grep -q 'treelint deps --calls' "$REF_FILE"
}

# AC#1 Test 3: Reference file documents --symbol flag usage
test_symbol_flag_documented() {
    [ -f "$REF_FILE" ] && grep -q '\-\-symbol' "$REF_FILE"
}

# AC#1 Test 4: Reference file documents --format json flag
test_format_json_flag_documented() {
    [ -f "$REF_FILE" ] && grep -q '\-\-format json' "$REF_FILE"
}

# AC#1 Test 5: JSON response specifies symbol field in output
test_json_output_symbol_field() {
    [ -f "$REF_FILE" ] && grep -q '"symbol"' "$REF_FILE"
}

# AC#1 Test 6: JSON response specifies callers array in output
test_json_output_callers_field() {
    [ -f "$REF_FILE" ] && grep -q '"callers"' "$REF_FILE"
}

# AC#1 Test 7: JSON response specifies callees array in output
test_json_output_callees_field() {
    [ -f "$REF_FILE" ] && grep -q '"callees"' "$REF_FILE"
}

# AC#1 Test 8: Caller entries have name field
test_caller_entry_name_field() {
    [ -f "$REF_FILE" ] && grep -q '"name"' "$REF_FILE"
}

# AC#1 Test 9: Caller entries have file field
test_caller_entry_file_field() {
    [ -f "$REF_FILE" ] && grep -q '"file"' "$REF_FILE"
}

# AC#1 Test 10: Caller entries have line field
test_caller_entry_line_field() {
    [ -f "$REF_FILE" ] && grep -q '"line"' "$REF_FILE"
}

# Run all tests
echo "============================================================"
echo "STORY-370 AC#1: Successful dependency query returns callers/callees"
echo "============================================================"

run_test "Reference file exists" test_dependency_query_ref_exists
run_test "treelint deps --calls command documented" test_deps_calls_command_documented
run_test "--symbol flag documented" test_symbol_flag_documented
run_test "--format json flag documented" test_format_json_flag_documented
run_test "JSON output specifies symbol field" test_json_output_symbol_field
run_test "JSON output specifies callers array" test_json_output_callers_field
run_test "JSON output specifies callees array" test_json_output_callees_field
run_test "Caller entry has name field" test_caller_entry_name_field
run_test "Caller entry has file field" test_caller_entry_file_field
run_test "Caller entry has line field" test_caller_entry_line_field

echo ""
echo "============================================================"
echo "Results: $TESTS_PASSED/$TESTS_RUN passed, $TESTS_FAILED failed"
echo "============================================================"

exit $TESTS_FAILED
