#!/bin/bash
##############################################################################
# Test Suite: STORY-369 AC#2 - JSON Parsing of Treelint Search Results
# Purpose: Verify reference file documents parsing of 4 required JSON fields
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

# AC#2 Test 1: JSON parsing references name field
test_json_name_field() {
    [ -f "$REF_FILE" ] && grep -qi 'name' "$REF_FILE" && grep -q '`name`\|"name"\|name.*field' "$REF_FILE"
}

# AC#2 Test 2: JSON parsing references file field
test_json_file_field() {
    [ -f "$REF_FILE" ] && grep -q '`file`\|"file"\|file.*field\|file.*path' "$REF_FILE"
}

# AC#2 Test 3: JSON parsing references lines field
test_json_lines_field() {
    [ -f "$REF_FILE" ] && grep -q '`lines`\|"lines"\|lines.*field\|lines.*range\|line.*range' "$REF_FILE"
}

# AC#2 Test 4: JSON parsing references signature field
test_json_signature_field() {
    [ -f "$REF_FILE" ] && grep -q '`signature`\|"signature"\|signature.*field' "$REF_FILE"
}

##############################################################################
# Execute Tests
##############################################################################

echo "=== STORY-369 AC#2: JSON Parsing of Treelint Results ==="
echo "Reference: $REF_FILE"
echo ""

run_test "JSON parsing references name field" test_json_name_field
run_test "JSON parsing references file field" test_json_file_field
run_test "JSON parsing references lines field" test_json_lines_field
run_test "JSON parsing references signature field" test_json_signature_field

echo ""
echo "=== Results: $TESTS_PASSED/$TESTS_RUN passed, $TESTS_FAILED failed ==="
exit $TESTS_FAILED
