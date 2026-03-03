#!/bin/bash
##############################################################################
# Test Suite: STORY-374 AC#1 - Daemon status check before Treelint queries
# Purpose: Verify the reference file documents that the integration layer
#          executes treelint daemon status --format json before queries,
#          parses the response for running/stopped/unknown states, and
#          proceeds with the appropriate code path based on that state
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
REF_FILE="${PROJECT_ROOT}/src/claude/skills/devforgeai-development/references/treelint-daemon-lifecycle.md"

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

# AC#1 Test 1: Reference file exists for daemon lifecycle management
test_daemon_lifecycle_ref_exists() {
    [ -f "$REF_FILE" ]
}

# AC#1 Test 2: Reference file documents treelint daemon status command
test_daemon_status_command_documented() {
    [ -f "$REF_FILE" ] && grep -q 'treelint daemon status' "$REF_FILE"
}

# AC#1 Test 3: Reference file documents --format json flag for status check
test_status_format_json_documented() {
    [ -f "$REF_FILE" ] && grep -q 'treelint daemon status --format json' "$REF_FILE"
}

# AC#1 Test 4: Status check returns JSON with status field
test_status_json_field_documented() {
    [ -f "$REF_FILE" ] && grep -q '"status"' "$REF_FILE"
}

# AC#1 Test 5: Running state is documented as valid status value
test_running_state_documented() {
    [ -f "$REF_FILE" ] && grep -qi 'running' "$REF_FILE"
}

# AC#1 Test 6: Stopped state is documented as valid status value
test_stopped_state_documented() {
    [ -f "$REF_FILE" ] && grep -qi 'stopped' "$REF_FILE"
}

# AC#1 Test 7: Unknown state is documented as valid status value
test_unknown_state_documented() {
    [ -f "$REF_FILE" ] && grep -qi 'unknown' "$REF_FILE"
}

# AC#1 Test 8: Status check executes BEFORE Treelint queries (pre-flight)
test_status_check_before_queries() {
    [ -f "$REF_FILE" ] && grep -qi 'before.*quer\|pre-flight\|status check.*first\|first.*status' "$REF_FILE"
}

# AC#1 Test 9: Status check has 200ms timeout documented
test_status_check_timeout_documented() {
    [ -f "$REF_FILE" ] && grep -q '200.*ms\|200ms' "$REF_FILE"
}

# AC#1 Test 10: Code path branching based on daemon state documented
test_state_based_code_path() {
    [ -f "$REF_FILE" ] && grep -qi 'running.*proceed\|stopped.*prompt\|code path\|branching\|decision' "$REF_FILE"
}

# AC#1 Test 11: JSON parsing of daemon status response documented
test_json_parsing_documented() {
    [ -f "$REF_FILE" ] && grep -qi 'pars.*json\|json.*pars\|json response' "$REF_FILE"
}

# Run all tests
echo "============================================================"
echo "STORY-374 AC#1: Daemon status check before Treelint queries"
echo "============================================================"

run_test "Reference file exists" test_daemon_lifecycle_ref_exists
run_test "treelint daemon status command documented" test_daemon_status_command_documented
run_test "--format json for status check documented" test_status_format_json_documented
run_test "JSON status field documented" test_status_json_field_documented
run_test "Running state documented" test_running_state_documented
run_test "Stopped state documented" test_stopped_state_documented
run_test "Unknown state documented" test_unknown_state_documented
run_test "Status check before queries (pre-flight)" test_status_check_before_queries
run_test "200ms timeout for status check" test_status_check_timeout_documented
run_test "Code path branching based on state" test_state_based_code_path
run_test "JSON parsing of status response" test_json_parsing_documented

echo ""
echo "============================================================"
echo "Results: $TESTS_PASSED/$TESTS_RUN passed, $TESTS_FAILED failed"
echo "============================================================"

exit $TESTS_FAILED
