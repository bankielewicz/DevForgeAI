#!/bin/bash
##############################################################################
# Test Suite: STORY-373 AC#2 - JSON output parsed and validated against schema
# Purpose: Verify parsing logic for treelint map JSON response handles
#          valid structures, rank ordering, array length validation,
#          and malformed JSON gracefully
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

# AC#2 Test 1: Parsing section exists in reference file
test_parsing_section_exists() {
    [ -f "$REF_FILE" ] && grep -qi 'pars' "$REF_FILE"
}

# AC#2 Test 2: Symbols array documented as sorted by ascending rank (rank 1 first)
test_symbols_sorted_ascending_rank() {
    [ -f "$REF_FILE" ] && grep -qi 'ascending.*rank\|rank.*ascending\|sorted.*rank\|rank 1.*first' "$REF_FILE"
}

# AC#2 Test 3: Each symbol requires all four fields (name, type, rank, references)
test_four_required_fields() {
    [ -f "$REF_FILE" ] && grep -q '"name"' "$REF_FILE" && grep -q '"type"' "$REF_FILE" && grep -q '"rank"' "$REF_FILE" && grep -q '"references"' "$REF_FILE"
}

# AC#2 Test 4: total_symbols equals length of symbols array validation documented
test_total_symbols_equals_array_length() {
    [ -f "$REF_FILE" ] && grep -qi 'total_symbols.*equals\|total_symbols.*length\|total_symbols.*count\|length.*symbols.*array' "$REF_FILE"
}

# AC#2 Test 5: total_files is a positive integer validation documented
test_total_files_positive_integer() {
    [ -f "$REF_FILE" ] && grep -qi 'total_files.*positive\|total_files.*integer\|total_files.*greater' "$REF_FILE"
}

# AC#2 Test 6: Malformed JSON triggers structured error (not crash)
test_malformed_json_error_handling() {
    [ -f "$REF_FILE" ] && grep -qi 'malformed.*error\|invalid.*JSON\|JSON.*error\|malformed.*JSON' "$REF_FILE"
}

# AC#2 Test 7: Schema validation guidance documented
test_schema_validation_documented() {
    [ -f "$REF_FILE" ] && grep -qi 'schema\|validation\|validated' "$REF_FILE"
}

# AC#2 Test 8: name field type documented as string
test_name_field_type_string() {
    [ -f "$REF_FILE" ] && grep -qi 'name.*string' "$REF_FILE"
}

# AC#2 Test 9: rank field type documented as positive integer
test_rank_field_type_integer() {
    [ -f "$REF_FILE" ] && grep -qi 'rank.*positive\|rank.*integer\|rank.*number' "$REF_FILE"
}

# AC#2 Test 10: references field type documented as non-negative integer
test_references_field_type() {
    [ -f "$REF_FILE" ] && grep -qi 'references.*non-negative\|references.*integer\|references.*count\|references.*number' "$REF_FILE"
}

# AC#2 Test 11: Truncated/partial JSON handling documented
test_truncated_json_handling() {
    [ -f "$REF_FILE" ] && grep -qi 'truncated\|partial.*response\|incomplete.*JSON' "$REF_FILE"
}

# Run all tests
echo "============================================================"
echo "STORY-373 AC#2: JSON output parsed and validated against schema"
echo "============================================================"

run_test "Parsing section exists in reference" test_parsing_section_exists
run_test "Symbols sorted by ascending rank" test_symbols_sorted_ascending_rank
run_test "Four required fields per symbol" test_four_required_fields
run_test "total_symbols equals array length" test_total_symbols_equals_array_length
run_test "total_files is positive integer" test_total_files_positive_integer
run_test "Malformed JSON triggers structured error" test_malformed_json_error_handling
run_test "Schema validation documented" test_schema_validation_documented
run_test "name field type is string" test_name_field_type_string
run_test "rank field type is positive integer" test_rank_field_type_integer
run_test "references field type documented" test_references_field_type
run_test "Truncated JSON handling documented" test_truncated_json_handling

echo ""
echo "============================================================"
echo "Results: $TESTS_PASSED/$TESTS_RUN passed, $TESTS_FAILED failed"
echo "============================================================"

exit $TESTS_FAILED
