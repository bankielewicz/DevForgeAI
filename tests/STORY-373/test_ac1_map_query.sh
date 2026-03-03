#!/bin/bash
##############################################################################
# Test Suite: STORY-373 AC#1 - Successful map query returns ranked symbols
# Purpose: Verify treelint map --ranked --format json output documentation
#          specifies symbols array with name, type, rank, references fields
#          plus total_symbols and total_files top-level fields
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

# AC#1 Test 1: Reference file exists for repository map service
test_repository_map_ref_exists() {
    [ -f "$REF_FILE" ]
}

# AC#1 Test 2: Reference file documents treelint map --ranked command
test_map_ranked_command_documented() {
    [ -f "$REF_FILE" ] && grep -q 'treelint map --ranked' "$REF_FILE"
}

# AC#1 Test 3: Reference file documents --format json flag
test_format_json_flag_documented() {
    [ -f "$REF_FILE" ] && grep -q '\-\-format json' "$REF_FILE"
}

# AC#1 Test 4: JSON response specifies symbols array in output
test_json_output_symbols_array() {
    [ -f "$REF_FILE" ] && grep -q '"symbols"' "$REF_FILE"
}

# AC#1 Test 5: Each symbol entry has name field (string)
test_symbol_entry_name_field() {
    [ -f "$REF_FILE" ] && grep -q '"name"' "$REF_FILE"
}

# AC#1 Test 6: Each symbol entry has type field (function/class/method/variable)
test_symbol_entry_type_field() {
    [ -f "$REF_FILE" ] && grep -q '"type"' "$REF_FILE"
}

# AC#1 Test 7: Type field documents valid values (function, class, method, variable)
test_symbol_type_valid_values() {
    [ -f "$REF_FILE" ] && grep -q 'function' "$REF_FILE" && grep -q 'class' "$REF_FILE" && grep -q 'method' "$REF_FILE" && grep -q 'variable' "$REF_FILE"
}

# AC#1 Test 8: Each symbol entry has rank field (positive integer, 1 = most important)
test_symbol_entry_rank_field() {
    [ -f "$REF_FILE" ] && grep -q '"rank"' "$REF_FILE"
}

# AC#1 Test 9: Rank field documented as 1 = most important
test_rank_one_most_important() {
    [ -f "$REF_FILE" ] && grep -q 'rank.*1.*most\|1.*most.*important\|rank 1.*highest' "$REF_FILE"
}

# AC#1 Test 10: Each symbol entry has references field (non-negative integer count)
test_symbol_entry_references_field() {
    [ -f "$REF_FILE" ] && grep -q '"references"' "$REF_FILE"
}

# AC#1 Test 11: total_symbols top-level field documented
test_total_symbols_field() {
    [ -f "$REF_FILE" ] && grep -q '"total_symbols"' "$REF_FILE"
}

# AC#1 Test 12: total_files top-level field documented
test_total_files_field() {
    [ -f "$REF_FILE" ] && grep -q '"total_files"' "$REF_FILE"
}

# AC#1 Test 13: Example JSON response documented showing all fields
test_example_json_response() {
    [ -f "$REF_FILE" ] && grep -q '"symbols"' "$REF_FILE" && grep -q '"total_symbols"' "$REF_FILE" && grep -q '"total_files"' "$REF_FILE"
}

# AC#1 Test 14: Treelint index requirement (.treelint/index.db) documented
test_index_requirement_documented() {
    [ -f "$REF_FILE" ] && grep -q 'index.db\|\.treelint' "$REF_FILE"
}

# Run all tests
echo "============================================================"
echo "STORY-373 AC#1: Successful map query returns ranked symbols"
echo "============================================================"

run_test "Reference file exists" test_repository_map_ref_exists
run_test "treelint map --ranked command documented" test_map_ranked_command_documented
run_test "--format json flag documented" test_format_json_flag_documented
run_test "JSON output specifies symbols array" test_json_output_symbols_array
run_test "Symbol entry has name field" test_symbol_entry_name_field
run_test "Symbol entry has type field" test_symbol_entry_type_field
run_test "Type field valid values documented" test_symbol_type_valid_values
run_test "Symbol entry has rank field" test_symbol_entry_rank_field
run_test "Rank 1 = most important documented" test_rank_one_most_important
run_test "Symbol entry has references field" test_symbol_entry_references_field
run_test "total_symbols top-level field" test_total_symbols_field
run_test "total_files top-level field" test_total_files_field
run_test "Example JSON response shows all fields" test_example_json_response
run_test "Treelint index requirement documented" test_index_requirement_documented

echo ""
echo "============================================================"
echo "Results: $TESTS_PASSED/$TESTS_RUN passed, $TESTS_FAILED failed"
echo "============================================================"

exit $TESTS_FAILED
