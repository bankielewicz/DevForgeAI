#!/bin/bash
##############################################################################
# Test Suite: STORY-374 AC#5 - No orphan daemon processes
# Purpose: Verify the reference file documents PID file management:
#          - Daemon PID recorded when started
#          - Daemon left running (user-managed per EPIC-058)
#          - PID file at .treelint/daemon.pid verified to match running process
#          - Stale PID file (dead process) is cleaned up
#          - Orphaned socket file cleanup
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

# AC#5 Test 1: PID file location documented (.treelint/daemon.pid)
test_pid_file_location_documented() {
    [ -f "$REF_FILE" ] && grep -q 'daemon.pid' "$REF_FILE"
}

# AC#5 Test 2: Daemon PID recorded when started
test_pid_recorded_on_start() {
    [ -f "$REF_FILE" ] && grep -qi 'PID.*record\|record.*PID\|store.*PID\|PID.*file' "$REF_FILE"
}

# AC#5 Test 3: PID file verified to match running process
test_pid_verification_documented() {
    [ -f "$REF_FILE" ] && grep -qi 'kill -0\|verify.*PID\|PID.*match\|process.*alive\|check.*PID' "$REF_FILE"
}

# AC#5 Test 4: Stale PID file detection documented (dead process)
test_stale_pid_detection() {
    [ -f "$REF_FILE" ] && grep -qi 'stale.*PID\|dead.*process\|PID.*dead\|stale.*file' "$REF_FILE"
}

# AC#5 Test 5: Stale PID file cleanup (removal) documented
test_stale_pid_cleanup() {
    [ -f "$REF_FILE" ] && grep -qi 'clean.*PID\|remov.*PID\|delet.*PID\|PID.*clean\|PID.*remov' "$REF_FILE"
}

# AC#5 Test 6: Orphaned socket file cleanup documented (daemon.sock)
test_orphaned_socket_cleanup() {
    [ -f "$REF_FILE" ] && grep -q 'daemon.sock' "$REF_FILE"
}

# AC#5 Test 7: Socket cleanup when no process attached documented
test_socket_no_process_cleanup() {
    [ -f "$REF_FILE" ] && grep -qi 'orphan.*socket\|socket.*orphan\|socket.*clean\|socket.*remov' "$REF_FILE"
}

# AC#5 Test 8: Daemon left running after workflow (user-managed lifecycle)
test_daemon_left_running() {
    [ -f "$REF_FILE" ] && grep -qi 'left running\|daemon.*running.*after\|no.*stop\|not.*stop\|user.*managed' "$REF_FILE"
}

# AC#5 Test 9: No treelint daemon stop issued by framework
test_no_daemon_stop_by_framework() {
    [ -f "$REF_FILE" ] && grep -qi 'no.*daemon stop\|MUST NOT.*stop\|never.*stop\|framework.*not.*stop' "$REF_FILE"
}

# AC#5 Test 10: Cleanup happens before daemon start attempts
test_cleanup_before_start() {
    [ -f "$REF_FILE" ] && grep -qi 'cleanup.*before.*start\|before.*start.*clean\|pre-start.*clean\|clean.*before' "$REF_FILE"
}

# Run all tests
echo "============================================================"
echo "STORY-374 AC#5: No orphan daemon processes"
echo "============================================================"

run_test "PID file location (.treelint/daemon.pid)" test_pid_file_location_documented
run_test "Daemon PID recorded on start" test_pid_recorded_on_start
run_test "PID verified to match running process" test_pid_verification_documented
run_test "Stale PID detection (dead process)" test_stale_pid_detection
run_test "Stale PID file cleanup" test_stale_pid_cleanup
run_test "Orphaned socket file (daemon.sock)" test_orphaned_socket_cleanup
run_test "Socket cleanup when no process attached" test_socket_no_process_cleanup
run_test "Daemon left running after workflow" test_daemon_left_running
run_test "No daemon stop issued by framework" test_no_daemon_stop_by_framework
run_test "Cleanup before daemon start attempts" test_cleanup_before_start

echo ""
echo "============================================================"
echo "Results: $TESTS_PASSED/$TESTS_RUN passed, $TESTS_FAILED failed"
echo "============================================================"

exit $TESTS_FAILED
