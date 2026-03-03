#!/bin/bash
##############################################################################
# Test Suite: STORY-369 AC#6 - Progressive Disclosure Compliance
# Purpose: Verify reference file exists, core file line count, references table
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
AGENT_FILE="${PROJECT_ROOT}/src/claude/agents/anti-pattern-scanner.md"
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

# AC#6 Test 1: phase5-treelint-detection.md reference file exists
test_reference_file_exists() {
    [ -f "$REF_FILE" ]
}

# AC#6 Test 2: anti-pattern-scanner.md line count <= 706 (701 baseline + 5 max)
test_line_count_within_budget() {
    local line_count
    line_count=$(wc -l < "$AGENT_FILE" 2>/dev/null)
    [ -n "$line_count" ] && [ "$line_count" -le 706 ]
}

# AC#6 Test 3: Progressive Disclosure References table lists new file
test_references_table_entry() {
    grep -q 'phase5-treelint-detection' "$AGENT_FILE"
}

##############################################################################
# Execute Tests
##############################################################################

echo "=== STORY-369 AC#6: Progressive Disclosure Compliance ==="
echo "Agent: $AGENT_FILE"
echo "Reference: $REF_FILE"
echo ""

run_test "phase5-treelint-detection.md reference file created" test_reference_file_exists
run_test "anti-pattern-scanner.md line count <= 706" test_line_count_within_budget
run_test "Progressive Disclosure References table lists new file" test_references_table_entry

echo ""
echo "=== Results: $TESTS_PASSED/$TESTS_RUN passed, $TESTS_FAILED failed ==="
exit $TESTS_FAILED
