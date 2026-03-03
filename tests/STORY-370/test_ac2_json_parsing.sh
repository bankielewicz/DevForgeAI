#!/bin/bash
##############################################################################
# Test Suite: STORY-370 AC#2 - JSON output parsed into structured result
# Purpose: Verify parsing logic for treelint deps JSON response handles
#          valid structures and malformed JSON gracefully
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

# AC#2 Test 1: Parsing section exists in reference file
test_parsing_section_exists() {
    [ -f "$REF_FILE" ] && grep -qi 'pars' "$REF_FILE"
}

# AC#2 Test 2: Symbol name extracted as string from parsed result
test_parsed_symbol_name_string() {
    [ -f "$REF_FILE" ] && grep -q 'symbol.*string' "$REF_FILE"
}

# AC#2 Test 3: Callers parsed as list of objects
test_parsed_callers_list() {
    [ -f "$REF_FILE" ] && grep -q 'callers.*list\|callers.*array' "$REF_FILE"
}

# AC#2 Test 4: Callees parsed as list of objects
test_parsed_callees_list() {
    [ -f "$REF_FILE" ] && grep -q 'callees.*list\|callees.*array' "$REF_FILE"
}

# AC#2 Test 5: Each caller has name (string) field documented
test_caller_name_type_string() {
    [ -f "$REF_FILE" ] && grep -q 'name.*string' "$REF_FILE"
}

# AC#2 Test 6: Each caller has file (relative path) field documented
test_caller_file_relative_path() {
    [ -f "$REF_FILE" ] && grep -q 'file.*relative\|file.*path' "$REF_FILE"
}

# AC#2 Test 7: Each caller has line (positive integer) field documented
test_caller_line_positive_integer() {
    [ -f "$REF_FILE" ] && grep -q 'line.*positive\|line.*integer\|line.*number' "$REF_FILE"
}

# AC#2 Test 8: Malformed JSON triggers structured error (not crash)
test_malformed_json_error_handling() {
    [ -f "$REF_FILE" ] && grep -q 'malformed.*error\|invalid.*JSON\|JSON.*error' "$REF_FILE"
}

# AC#2 Test 9: Example valid JSON response documented
test_example_json_response() {
    [ -f "$REF_FILE" ] && grep -q '"symbol".*:' "$REF_FILE"
}

# Run all tests
echo "============================================================"
echo "STORY-370 AC#2: JSON output parsed into structured result"
echo "============================================================"

run_test "Parsing section exists in reference" test_parsing_section_exists
run_test "Symbol name extracted as string" test_parsed_symbol_name_string
run_test "Callers parsed as list of objects" test_parsed_callers_list
run_test "Callees parsed as list of objects" test_parsed_callees_list
run_test "Caller name type is string" test_caller_name_type_string
run_test "Caller file is relative path" test_caller_file_relative_path
run_test "Caller line is positive integer" test_caller_line_positive_integer
run_test "Malformed JSON triggers structured error" test_malformed_json_error_handling
run_test "Example valid JSON response documented" test_example_json_response

echo ""
echo "============================================================"
echo "Results: $TESTS_PASSED/$TESTS_RUN passed, $TESTS_FAILED failed"
echo "============================================================"

exit $TESTS_FAILED
