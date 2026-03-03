#!/bin/bash
##############################################################################
# Test Suite: STORY-374 AC#6 - Daemon query performance validation
# Purpose: Verify the reference file documents that daemon mode queries
#          complete in less than 5 milliseconds (p95), confirming the
#          performance benefit that justified daemon usage.
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

# AC#6 Test 1: Daemon query latency target documented (< 5ms)
test_5ms_target_documented() {
    [ -f "$REF_FILE" ] && grep -q '5ms\|5 ms\|< 5.*ms\|5 millisecond' "$REF_FILE"
}

# AC#6 Test 2: p95 percentile metric documented
test_p95_metric_documented() {
    [ -f "$REF_FILE" ] && grep -qi 'p95\|95th.*percentile\|95.*percentile' "$REF_FILE"
}

# AC#6 Test 3: Daemon mode vs CLI mode performance comparison documented
test_daemon_vs_cli_comparison() {
    [ -f "$REF_FILE" ] && grep -qi 'daemon.*vs.*CLI\|CLI.*vs.*daemon\|performance.*comparison\|40x\|improvement' "$REF_FILE"
}

# AC#6 Test 4: CLI mode latency documented (~200ms)
test_cli_latency_documented() {
    [ -f "$REF_FILE" ] && grep -q '200ms\|200 ms\|~200ms' "$REF_FILE"
}

# AC#6 Test 5: .treelint/index.db SQLite index requirement documented
test_sqlite_index_requirement() {
    [ -f "$REF_FILE" ] && grep -q 'index.db' "$REF_FILE"
}

# AC#6 Test 6: Wall-clock time measurement method documented
test_wall_clock_measurement() {
    [ -f "$REF_FILE" ] && grep -qi 'wall.*clock\|elapsed.*time\|latency.*measure\|measure.*time' "$REF_FILE"
}

# AC#6 Test 7: Performance benefit justification for daemon usage
test_performance_justification() {
    [ -f "$REF_FILE" ] && grep -qi 'performance.*benefit\|benefit.*daemon\|faster.*daemon\|speed.*advantage' "$REF_FILE"
}

# Run all tests
echo "============================================================"
echo "STORY-374 AC#6: Daemon query performance validation"
echo "============================================================"

run_test "5ms latency target documented" test_5ms_target_documented
run_test "p95 percentile metric" test_p95_metric_documented
run_test "Daemon vs CLI performance comparison" test_daemon_vs_cli_comparison
run_test "CLI mode latency (~200ms)" test_cli_latency_documented
run_test "SQLite index requirement (index.db)" test_sqlite_index_requirement
run_test "Wall-clock measurement method" test_wall_clock_measurement
run_test "Performance benefit justification" test_performance_justification

echo ""
echo "============================================================"
echo "Results: $TESTS_PASSED/$TESTS_RUN passed, $TESTS_FAILED failed"
echo "============================================================"

exit $TESTS_FAILED
